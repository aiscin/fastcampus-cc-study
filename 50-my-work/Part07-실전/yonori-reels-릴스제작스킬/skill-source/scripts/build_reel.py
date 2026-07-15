#!/usr/bin/env python3
"""릴스 영상 조립 파이프라인: edge-tts → 묵음 트림 → 클립 정규화 → 조립 → ASS 자막 번인.

사용: python3 build_reel.py --manifest manifest.json --out final.mp4

manifest.json 스키마:
{
  "narration": "none",                   // 선택: "tts"(기본) | "none" = 목소리 미포함(사용자가 추후 직접 녹음)
  "guide_audio": true,                   // 선택: narration=none일 때 녹음 참고용 TTS 가이드 트랙을 별도 파일로 생성
  "voice": "ko-KR-SunHiNeural",          // 선택, 기본 선히 (guide_audio에도 사용)
  "keep_clip_audio": 0.25,               // 선택, 현장음 볼륨(0=제거). tts모드 기본 0 / none모드 기본 1.0
  "scenes": [
    {
      "tts_text": "3발 캐리어를, 양손이랑 발로, 끌고 다닌 적 있음?",  // 발음표기 적용된 한글 텍스트
      "subtitle": "캐리어 3개 끌고 다닌 적?",                        // 자막(축약형), 빈 문자열이면 자막 없음
      "clip": "/path/to/clip1.mp4",                                  // 이 장면에 쓸 클립
      "duration": 2.4                                                // narration=none일 때 필수: 장면 길이(초, 발화 공식 값)
    }, ...
  ]
}

화질 규칙(사용자 지정 2026-07-07): 색보정·필터 금지. scale은 lanczos(저화질 소스 업스케일 품질 확보), CRF 18.

실측 반영 사항(2026-07-06 검증):
- edge-tts는 파일마다 뒤 ~0.9초 묵음을 붙임 → silenceremove로 트림 (장면당 죽은 공기 방지)
- edge-tts 출력은 24kHz mono → 44.1kHz stereo 리샘플
- 이 환경 ffmpeg static build에 drawtext 없음 → 자막은 ASS(libass) 단일 경로
- 클립 규격 제각각 → scale+crop+setsar+fps 정규화 후 재인코딩 concat
"""
import argparse
import asyncio
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

W, H, FPS = 1080, 1920, 30
FONT = "Malgun Gothic"


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FFMPEG_FAIL: {' '.join(cmd[:6])}...\n{r.stderr[-1500:]}", file=sys.stderr)
        sys.exit(1)


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True)
    return float(r.stdout.strip())


async def tts(text: str, voice: str, out: Path) -> None:
    import edge_tts
    await edge_tts.Communicate(text, voice).save(str(out))


def make_narration(text: str, voice: str, workdir: Path, idx: int) -> Path:
    """TTS 생성 → 앞뒤 묵음 트림 → 44.1kHz 스테레오 wav."""
    raw = workdir / f"nar{idx}_raw.mp3"
    asyncio.run(tts(text, voice, raw))
    trimmed = workdir / f"nar{idx}.wav"
    # 앞 묵음 제거 + (뒤집기 → 앞 묵음 제거 → 다시 뒤집기)로 뒤 0.9초 고정 묵음 제거
    run(["ffmpeg", "-y", "-i", str(raw), "-af",
         "silenceremove=start_periods=1:start_threshold=-45dB,"
         "areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
         "apad=pad_dur=0.15",  # 문장 사이 최소 간격
         "-ar", "44100", "-ac", "2", str(trimmed)])
    return trimmed


def norm_vf(dur: float) -> str:
    # 보정 필터 금지(원본 톤 유지) — 기하 변환만. lanczos = 저화질 소스 업스케일 품질
    return (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={W}:{H},setsar=1,fps={FPS},"
            f"tpad=stop_mode=clone:stop_duration={dur + 2}")  # 클립이 짧으면 마지막 프레임 유지


def make_segment_novoice(clip: Path, dur: float, keep_audio: float,
                         workdir: Path, idx: int) -> Path:
    """나레이션 없이 클립을 지정 길이의 정규화 세그먼트로 만든다 (현장음 유지)."""
    seg = workdir / f"seg{idx}.mp4"
    vf = norm_vf(dur)
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", str(clip), "-filter_complex",
         f"[0:v]{vf}[v];[0:a]volume={keep_audio},aresample=44100,apad[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}",
         "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", str(seg)],
        capture_output=True, text=True)
    if r.returncode == 0:
        return seg
    # 오디오 트랙이 없는 클립(지도 그래픽 등) → 무음 트랙 합성
    run(["ffmpeg", "-y", "-i", str(clip), "-f", "lavfi",
         "-i", "anullsrc=r=44100:cl=stereo",
         "-filter_complex", f"[0:v]{vf}[v]",
         "-map", "[v]", "-map", "1:a", "-t", f"{dur:.3f}",
         "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", str(seg)])
    return seg


def make_guide_audio(nars: list[Path], durs: list[float], workdir: Path, out: Path) -> None:
    """녹음 참고용 가이드 트랙: 장면별 TTS를 장면 길이에 맞춰 패딩 후 이어붙인 별도 오디오."""
    padded = []
    for i, (nar, dur) in enumerate(zip(nars, durs)):
        p = workdir / f"guide{i}.wav"
        run(["ffmpeg", "-y", "-i", str(nar), "-af", "apad",
             "-t", f"{dur:.3f}", str(p)])
        padded.append(p)
    lst = workdir / "guide_list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in padded), encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:a", "aac", "-b:a", "128k", str(out)])


def make_segment(clip: Path, narration: Path, keep_audio: float,
                 workdir: Path, idx: int) -> tuple[Path, float]:
    """클립을 나레이션 길이에 맞춰 정규화된 세그먼트로 만든다."""
    dur = probe_duration(narration)
    seg = workdir / f"seg{idx}.mp4"
    vf = norm_vf(dur)
    if keep_audio > 0:
        # 현장음 + 나레이션 믹스 (클립에 오디오 없으면 실패할 수 있음 → 호출부에서 폴백)
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", str(clip), "-i", str(narration),
             "-filter_complex",
             f"[0:v]{vf}[v];[0:a]volume={keep_audio},aresample=44100[a0];"
             f"[a0][1:a]amix=inputs=2:duration=longest:normalize=0[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "128k", "-ar", "44100", str(seg)],
            capture_output=True, text=True)
        if r.returncode == 0:
            return seg, dur
        # 클립에 오디오 트랙이 없는 경우 → 나레이션만으로 폴백
    run(["ffmpeg", "-y", "-i", str(clip), "-i", str(narration),
         "-filter_complex", f"[0:v]{vf}[v]",
         "-map", "[v]", "-map", "1:a", "-t", f"{dur:.3f}",
         "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-ar", "44100", str(seg)])
    return seg, dur


def ass_time(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def make_ass(scenes: list[dict], durations: list[float], out: Path) -> None:
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV
Style: Default,{FONT},64,&H00FFFFFF,&H00000000,&H80000000,-1,3,1,2,60,60,250

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines, t = [], 0.0
    for scene, dur in zip(scenes, durations):
        sub = scene.get("subtitle", "").strip()
        if sub:
            end = t + max(dur, 1.5)  # 최소 표시 1.5초
            text = sub.replace("\n", "\\N")
            lines.append(f"Dialogue: 0,{ass_time(t)},{ass_time(end)},Default,,0,0,0,,{text}")
        t += dur
    out.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", default="final.mp4")
    args = ap.parse_args()

    mf = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    voice = mf.get("voice", "ko-KR-SunHiNeural")
    no_voice = mf.get("narration", "tts") == "none"
    keep_audio = float(mf.get("keep_clip_audio", 1.0 if no_voice else 0))
    guide = bool(mf.get("guide_audio")) and no_voice
    scenes = mf["scenes"]
    if not scenes:
        print("ERROR: scenes 비어 있음", file=sys.stderr)
        return 1
    for i, s in enumerate(scenes):
        if not Path(s["clip"]).exists():
            print(f"ERROR: 장면 {i+1} 클립 없음: {s['clip']}", file=sys.stderr)
            return 1
        if no_voice and not s.get("duration"):
            print(f"ERROR: narration=none인데 장면 {i+1}에 duration 없음", file=sys.stderr)
            return 1

    workdir = Path(tempfile.mkdtemp(prefix="reel_"))
    try:
        segs, durs, nars = [], [], []
        for i, s in enumerate(scenes):
            if no_voice:
                dur = float(s["duration"])
                seg = make_segment_novoice(Path(s["clip"]), dur, keep_audio, workdir, i)
                if guide:
                    nars.append(make_narration(s["tts_text"], voice, workdir, i))
            else:
                nar = make_narration(s["tts_text"], voice, workdir, i)
                seg, dur = make_segment(Path(s["clip"]), nar, keep_audio, workdir, i)
            segs.append(seg)
            durs.append(dur)
            print(f"scene {i+1}/{len(scenes)}: {dur:.2f}s", file=sys.stderr)

        guide_out = None
        if guide:
            guide_out = Path(args.out).with_name(Path(args.out).stem + "_guide.m4a")
            make_guide_audio(nars, durs, workdir, guide_out)

        # 동일 스펙 세그먼트 → concat demuxer 안전
        lst = workdir / "list.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
        base = workdir / "base.mp4"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
             "-c", "copy", str(base)])

        ass = workdir / "subs.ass"
        make_ass(scenes, durs, ass)
        # ass 필터 경로 escape: 작업경로에 특수문자 없도록 workdir(영문 temp) 사용
        run(["ffmpeg", "-y", "-i", str(base), "-vf", f"ass={ass.as_posix()}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
             "-c:a", "copy", "-movflags", "+faststart", str(Path(args.out))])

        total = sum(durs)
        result = {"ok": True, "out": args.out,
                  "duration_sec": round(total, 2),
                  "scenes": len(scenes), "resolution": f"{W}x{H}",
                  "narration": "none" if no_voice else "tts"}
        if guide_out:
            result["guide_audio"] = str(guide_out)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
