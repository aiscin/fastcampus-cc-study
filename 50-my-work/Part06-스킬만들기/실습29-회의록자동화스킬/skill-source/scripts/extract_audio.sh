#!/usr/bin/env bash
# audio-to-doc — 오디오 확보 (결정론 단계)
# 유튜브 URL 이면 yt-dlp 로 음성 추출, 로컬 파일이면 그대로 사용.
# 두 경우 모두 ffmpeg 로 16kHz mono mp3 로 통일해 전사 품질을 맞춘다.
#
# 사용법: extract_audio.sh <유튜브URL|로컬오디오경로> [출력디렉토리]
# 출력:  stdout 마지막 줄에 변환된 오디오 파일 절대경로
set -euo pipefail

err() { echo "$@" >&2; }

if [[ $# -lt 1 ]]; then
  err "사용법: extract_audio.sh <유튜브URL|로컬오디오경로> [출력디렉토리]"
  exit 1
fi

INPUT="$1"
OUT_DIR="${2:-$(pwd)}"
mkdir -p "$OUT_DIR"

# 임시 작업 폴더 — 동시 실행 충돌 방지 + 종료 시 정리
WORK="$(mktemp -d "${TMPDIR:-/tmp}/audio_to_doc.XXXXXX")"
cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

command -v ffmpeg >/dev/null 2>&1 || { err "[필요] ffmpeg 설치 필요: sudo apt install ffmpeg"; exit 1; }

SRC=""
if [[ "$INPUT" =~ ^https?:// ]]; then
  # 유튜브/웹 URL → 음성 추출
  command -v yt-dlp >/dev/null 2>&1 || { err "[필요] yt-dlp 설치 필요: pip install yt-dlp"; exit 1; }
  err "▶ 유튜브 음성 추출 중..."
  if ! yt-dlp -x --audio-format mp3 --audio-quality 0 --no-playlist \
        -o "$WORK/audio.%(ext)s" "$INPUT" >&2; then
    err "[추출 실패] 삭제·멤버십 전용·지역 제한·봇 차단 영상일 수 있어. URL을 확인해줘."
    exit 1
  fi
  SRC="$(ls "$WORK"/audio.* 2>/dev/null | head -1)"
  [[ -n "$SRC" ]] || { err "[추출 실패] 다운로드된 오디오를 찾을 수 없어."; exit 1; }
else
  # 로컬 파일 — yt-dlp 건너뜀
  [[ -f "$INPUT" ]] || { err "[입력 오류] 파일을 찾을 수 없어: $INPUT"; exit 1; }
  SRC="$INPUT"
fi

# 길이 사전 측정 — 9.5시간(Gemini 한도) 초과 경고
if command -v ffprobe >/dev/null 2>&1; then
  DUR="$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$SRC" 2>/dev/null || echo 0)"
  DUR_INT="${DUR%.*}"
  if [[ "${DUR_INT:-0}" -gt 34200 ]]; then
    err "[주의] 오디오가 9.5시간을 넘어 한 번에 전사가 안 될 수 있어. 분할이 필요해."
  fi
fi

BASE="$(basename "${SRC%.*}")"
OUT_FILE="$OUT_DIR/${BASE}_16k.mp3"
err "▶ 16kHz mono 변환 중..."
if ! ffmpeg -y -i "$SRC" -ar 16000 -ac 1 "$OUT_FILE" >&2 2>&1; then
  err "[변환 실패] 파일이 손상됐거나 지원하지 않는 포맷일 수 있어."
  exit 1
fi

echo "$OUT_FILE"
