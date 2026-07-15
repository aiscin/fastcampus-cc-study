#!/usr/bin/env python3
"""tts_and_timing.py — 나레이션 스크립트 → 씬별 mp3 + 타이밍 (결정론 단계).

05-tts-script.md의 '## 씬 N' 헤더로 씬을 나눠, 각 씬 텍스트를 OpenAI TTS로 mp3 변환하고
ffprobe로 길이를 재서 card-timings.json으로 저장한다. Remotion이 이 타이밍으로 씬 길이를 맞춘다.

같은 스크립트 → 같은 음성·타이밍을 보장하려고 분리했다. 나레이션 카피는 SKILL.md(AI)가 쓴다.

사용:
  python3 tts_and_timing.py <workdir> [--voice nova] [--model tts-1] [--only 1,3]
"""
import argparse, json, os, re, subprocess, sys
from pathlib import Path


def load_key():
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    here = Path(__file__).resolve()
    for parent in [here] + list(here.parents):
        env = parent / ".env"
        if env.is_file():
            for line in env.read_text(encoding="utf-8").splitlines():
                m = re.match(r"\s*OPENAI_API_KEY\s*=\s*(.+)", line)
                if m:
                    return m.group(1).strip().strip('"').strip("'")
    sys.exit("✗ OPENAI_API_KEY 없음")


def parse_script(md_path):
    """'## 씬 N — 제목' 헤더 기준으로 (번호, 제목, 텍스트) 추출."""
    scenes = []
    cur = None
    for line in Path(md_path).read_text(encoding="utf-8").splitlines():
        h = re.match(r"##\s*씬\s*(\d+)\s*[—\-–]?\s*(.*)", line.strip())
        if h:
            if cur:
                scenes.append(cur)
            cur = {"no": int(h.group(1)), "title": h.group(2).strip(), "text": ""}
        elif cur is not None and line.strip() and not line.startswith(("#", ">")):
            cur["text"] += (" " if cur["text"] else "") + line.strip()
    if cur:
        scenes.append(cur)
    return scenes


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-of", "json", "-show_format", str(path)],
        capture_output=True, text=True)
    return round(float(json.loads(out.stdout)["format"]["duration"]), 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("--voice", default="nova")
    ap.add_argument("--model", default="tts-1")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    work = Path(args.workdir).expanduser().resolve()
    scenes = parse_script(work / "05-tts-script.md")
    only = {int(x) for x in args.only.split(",")} if args.only else None
    adir = work / "audio"; adir.mkdir(exist_ok=True)

    from openai import OpenAI
    client = OpenAI(api_key=load_key())

    timings = []
    print(f"▶ {len(scenes)}씬 TTS (voice={args.voice}, model={args.model})")
    for s in scenes:
        if only and s["no"] not in only:
            continue
        out = adir / f"card-{s['no']:02d}.mp3"
        try:
            with client.audio.speech.with_streaming_response.create(
                model=args.model, voice=args.voice, input=s["text"],
                speed=args.speed, response_format="mp3") as resp:
                resp.stream_to_file(out)
            d = duration(out)
            timings.append({"no": s["no"], "title": s["title"], "sec": d,
                            "text": s["text"], "file": f"audio/card-{s['no']:02d}.mp3"})
            print(f"  ✓ 씬 {s['no']:2d}  {d:>5.2f}s  {s['title'][:16]}")
        except Exception as e:
            print(f"  ✗ 씬 {s['no']}: {type(e).__name__}: {str(e)[:140]}")

    timings.sort(key=lambda x: x["no"])
    total = round(sum(t["sec"] for t in timings), 2)
    (work / "card-timings.json").write_text(
        json.dumps({"total_sec": total, "voice": args.voice, "scenes": timings},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"→ card-timings.json (총 {total}s)")


if __name__ == "__main__":
    main()
