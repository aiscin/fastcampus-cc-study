#!/usr/bin/env python3
# audio-to-doc — Gemini 전사 + 화자 분리 (결정론 단계: 같은 오디오 → 같은 전사)
# 표준 라이브러리만 사용 (pip 설치 불필요). Gemini REST API 직접 호출.
#
# 사용법:
#   python3 transcribe_gemini.py <오디오파일경로> [출력디렉토리]
#
# 동작:
#   1. .env 에서 GEMINI_API_KEY 로드 (워크스페이스 루트)
#   2. 파일 크기 판단 — 20MB 미만 inline / 이상 Files API 업로드(+ACTIVE 폴링)
#   3. gemini-3.5-flash 로 전사 + 화자 분리(distinct speakers) + MM:SS 타임스탬프
#   4. 구조화 출력 [{speaker, time, text}] 을 stdout(JSON) + transcript_raw.txt 로 저장
#
# 에러는 stderr, 결과 JSON은 stdout.

import sys
import os
import json
import base64
import time
import mimetypes
from pathlib import Path
from urllib import request, error

MODEL = "gemini-3.5-flash"          # 공식문서(ai.google.dev/gemini-api/docs/audio) 확인값
API_ROOT = "https://generativelanguage.googleapis.com"
INLINE_LIMIT = 20 * 1024 * 1024     # 20MB — 미만 inline, 이상 Files API (공식 기준)
POLL_TIMEOUT = 600                  # Files API ACTIVE 대기 최대 10분
POLL_INTERVAL = 5

PROMPT = (
    "이 오디오를 한국어로 전사해줘. 서로 다른 발화자를 구별해서 "
    "Speaker 1, Speaker 2 처럼 라벨링하고, 각 발화 구간의 시작 시각을 MM:SS 형식으로 표기해줘. "
    "결과는 [{speaker, time, text}] 형태의 JSON 배열로만 출력해줘."
)

RESPONSE_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "speaker": {"type": "STRING"},
            "time": {"type": "STRING"},
            "text": {"type": "STRING"},
        },
        "required": ["speaker", "time", "text"],
    },
}

MIME_MAP = {
    ".mp3": "audio/mp3", ".wav": "audio/wav", ".flac": "audio/flac",
    ".aac": "audio/aac", ".ogg": "audio/ogg", ".aiff": "audio/aiff",
    ".m4a": "audio/mp4", ".mp4": "audio/mp4",
}


def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def load_api_key():
    """워크스페이스 루트의 .env 에서 GEMINI_API_KEY 를 읽는다."""
    # 환경변수 우선
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    # 스크립트 위치 기준 루트(.claude/skills/audio-to-doc/scripts → 4단계 위) + 홈 폴백
    candidates = [
        Path(__file__).resolve().parents[4] / ".env",
        Path.home() / "fastcampus-cc" / ".env",
        Path.cwd() / ".env",
    ]
    for env_path in candidates:
        if env_path.is_file():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("GEMINI_API_KEY=") or line.upper().startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    die("[설정 필요] .env 에 GEMINI_API_KEY=... 를 추가한 뒤 다시 실행해줘. "
        "(발급: https://aistudio.google.com/apikey)")


def guess_mime(path):
    ext = Path(path).suffix.lower()
    if ext in MIME_MAP:
        return MIME_MAP[ext]
    mt, _ = mimetypes.guess_type(path)
    return mt or "audio/mpeg"


def http_json(url, payload, method="POST", headers=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8")), dict(resp.headers)
    except error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        if e.code == 429:
            die("[한도 초과] Gemini 무료 한도(분당/일일)를 초과했어. 잠시 후 다시 시도하거나 유료 키를 연결해줘.")
        die(f"[API 오류 {e.code}] {body[:500]}")
    except error.URLError as e:
        die(f"[네트워크 오류] Gemini 서버에 연결할 수 없어: {e.reason}")


def transcribe_inline(path, mime, key):
    audio_b64 = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    url = f"{API_ROOT}/v1beta/models/{MODEL}:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [
            {"text": PROMPT},
            {"inline_data": {"mime_type": mime, "data": audio_b64}},
        ]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
        },
    }
    result, _ = http_json(url, payload)
    return extract_text(result)


def upload_file(path, mime, key):
    """Files API 리줌어블 업로드 → file_uri 반환."""
    size = os.path.getsize(path)
    start_url = f"{API_ROOT}/upload/v1beta/files?key={key}"
    start_req = request.Request(
        start_url,
        data=json.dumps({"file": {"display_name": Path(path).name}}).encode(),
        method="POST",
    )
    start_req.add_header("X-Goog-Upload-Protocol", "resumable")
    start_req.add_header("X-Goog-Upload-Command", "start")
    start_req.add_header("X-Goog-Upload-Header-Content-Length", str(size))
    start_req.add_header("X-Goog-Upload-Header-Content-Type", mime)
    start_req.add_header("Content-Type", "application/json")
    try:
        with request.urlopen(start_req, timeout=120) as resp:
            upload_url = resp.headers.get("X-Goog-Upload-URL")
    except error.HTTPError as e:
        die(f"[업로드 시작 실패 {e.code}] {e.read().decode('utf-8','ignore')[:400]}")
    if not upload_url:
        die("[업로드 실패] 업로드 URL을 받지 못했어.")

    print(f"  ↑ 업로드 중... ({size/1024/1024:.1f}MB)", file=sys.stderr)
    up_req = request.Request(upload_url, data=Path(path).read_bytes(), method="POST")
    up_req.add_header("Content-Length", str(size))
    up_req.add_header("X-Goog-Upload-Offset", "0")
    up_req.add_header("X-Goog-Upload-Command", "upload, finalize")
    with request.urlopen(up_req, timeout=600) as resp:
        info = json.loads(resp.read().decode("utf-8"))
    file_obj = info["file"]
    name, uri, state = file_obj["name"], file_obj["uri"], file_obj.get("state")

    # ACTIVE 될 때까지 폴링 (타임아웃)
    waited = 0
    while state != "ACTIVE":
        if state == "FAILED":
            die("[전사 실패] Gemini가 업로드 파일 처리에 실패했어.")
        if waited >= POLL_TIMEOUT:
            die(f"[타임아웃] {POLL_TIMEOUT}초 동안 파일이 준비되지 않았어.")
        time.sleep(POLL_INTERVAL)
        waited += POLL_INTERVAL
        print(f"  ⏳ 처리 대기 중... {waited}초", file=sys.stderr)
        stat, _ = http_json(f"{API_ROOT}/v1beta/{name}?key={key}", None, method="GET")
        state = stat.get("state")
    return uri


def transcribe_files_api(path, mime, key):
    file_uri = upload_file(path, mime, key)
    url = f"{API_ROOT}/v1beta/models/{MODEL}:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [
            {"text": PROMPT},
            {"file_data": {"mime_type": mime, "file_uri": file_uri}},
        ]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
        },
    }
    result, _ = http_json(url, payload)
    return extract_text(result)


def extract_text(result):
    try:
        cand = result["candidates"][0]
        return "".join(p.get("text", "") for p in cand["content"]["parts"])
    except (KeyError, IndexError):
        fb = result.get("promptFeedback", {})
        die(f"[응답 파싱 실패] 전사 결과를 받지 못했어. {json.dumps(fb)[:300]}")


def main():
    if len(sys.argv) < 2:
        die("사용법: python3 transcribe_gemini.py <오디오파일> [출력디렉토리]")
    audio = sys.argv[1]
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(audio).resolve().parent

    if not os.path.isfile(audio):
        die(f"[입력 오류] 파일을 찾을 수 없어: {audio}")

    key = load_api_key()
    mime = guess_mime(audio)
    size = os.path.getsize(audio)

    # 개인정보 고지 (실행 자체는 SKILL.md 흐름에서 사용자 동의 후 호출)
    print("⚠ 오디오가 Google(Gemini API)로 전송돼. 대외비 내용이면 중단할 것.", file=sys.stderr)
    print(f"  파일: {Path(audio).name} ({size/1024/1024:.1f}MB) · 모델: {MODEL}", file=sys.stderr)

    if size < INLINE_LIMIT:
        print("  방식: inline (20MB 미만)", file=sys.stderr)
        raw = transcribe_inline(audio, mime, key)
    else:
        print("  방식: Files API 업로드 (20MB 이상)", file=sys.stderr)
        raw = transcribe_files_api(audio, mime, key)

    # 구조화 결과 파싱 + 중간 산출물 보존 (요약 실패해도 원문은 남게)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "transcript_raw.json"
    raw_path.write_text(raw, encoding="utf-8")

    try:
        segments = json.loads(raw)
    except json.JSONDecodeError:
        die(f"[파싱 경고] 구조화 출력이 JSON이 아니야. 원문은 {raw_path} 에 저장했어.")

    # 평문 백업도 저장
    plain = "\n".join(f"[{s.get('time','')}] {s.get('speaker','')}: {s.get('text','')}"
                      for s in segments)
    (out_dir / "transcript_raw.txt").write_text(plain, encoding="utf-8")

    speakers = sorted({s.get("speaker", "") for s in segments})
    print(json.dumps({
        "ok": True,
        "model": MODEL,
        "speaker_count": len(speakers),
        "speakers": speakers,
        "segment_count": len(segments),
        "raw_json": str(raw_path),
        "raw_txt": str(out_dir / "transcript_raw.txt"),
        "segments": segments,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
