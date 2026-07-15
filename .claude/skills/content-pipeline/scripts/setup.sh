#!/usr/bin/env bash
# setup.sh — content-pipeline Step 0: 작업 폴더 생성 + 환경·폰트 점검/확보
# 사용: setup.sh "<주제>"   → 마지막 줄에 WORKDIR=<경로> 출력
set -uo pipefail
TOPIC="${1:-콘텐츠}"

# 프로젝트 루트 = 이 스크립트에서 4단계 위 (.claude/skills/content-pipeline/scripts)
HERE="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$HERE/.." && pwd)"
ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"

# 주제 슬러그(공백→-, 특수문자 제거) + 날짜
SLUG="$(echo "$TOPIC" | tr ' ' '-' | tr -cd '[:alnum:]가-힣_-' | cut -c1-40)"
DATE="$(date +%F)"
WORK="$ROOT/50-my-work/Part06-스킬만들기/실습31-콘텐츠파이프라인스킬/${SLUG}-${DATE}"
mkdir -p "$WORK/images" "$WORK/audio" "$WORK/fonts"

echo "▶ content-pipeline 셋업"
echo "  작업 폴더: $WORK"

# OPENAI_API_KEY
if grep -q "OPENAI_API_KEY=." "$ROOT/.env" 2>/dev/null; then echo "  ✓ OPENAI_API_KEY"; else echo "  ℹ OPENAI_API_KEY 없음 (이미지·음성 단계 전까지는 진행 가능)"; fi

# 도구
for t in python3 node ffmpeg; do command -v "$t" >/dev/null 2>&1 && echo "  ✓ $t" || echo "  ℹ $t 없음"; done

# 렌더용 한글·이모지 폰트 (fontconfig) — Windows 폰트 재사용
mkdir -p "$HOME/.local/share/fonts"
if ! fc-list :lang=ko 2>/dev/null | grep -qi "malgun\|nanum\|pretendard\|black han"; then
  for f in malgun.ttf malgunbd.ttf seguiemj.ttf; do
    [ -f "/mnt/c/Windows/Fonts/$f" ] && cp -n "/mnt/c/Windows/Fonts/$f" "$HOME/.local/share/fonts/" 2>/dev/null
  done
  fc-cache -f >/dev/null 2>&1
fi

# 웹폰트(카드 HTML @font-face용) — 스킬 번들에서 복사, 없으면 다운로드
SRC_FONTS="$SKILL_DIR/remotion/public/fonts"
need_dl=0
for f in Pretendard-Regular.woff2 Pretendard-SemiBold.woff2 Pretendard-Bold.woff2 Pretendard-Black.woff2 BlackHanSans-Regular.ttf; do
  if [ -f "$SRC_FONTS/$f" ]; then cp -n "$SRC_FONTS/$f" "$WORK/fonts/" 2>/dev/null
  elif [ ! -f "$WORK/fonts/$f" ]; then need_dl=1; fi
done
if [ "$need_dl" = "1" ]; then
  B="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/woff2"
  for w in Regular SemiBold Bold Black; do
    [ -f "$WORK/fonts/Pretendard-$w.woff2" ] || curl -sL --fail -o "$WORK/fonts/Pretendard-$w.woff2" "$B/Pretendard-$w.woff2" 2>/dev/null || true
  done
  [ -f "$WORK/fonts/BlackHanSans-Regular.ttf" ] || curl -sL --fail -o "$WORK/fonts/BlackHanSans-Regular.ttf" \
    "https://github.com/google/fonts/raw/main/ofl/blackhansans/BlackHanSans-Regular.ttf" 2>/dev/null || true
fi
ls "$WORK/fonts"/*.woff2 >/dev/null 2>&1 && echo "  ✓ 웹폰트(Pretendard·BlackHanSans)" || echo "  ℹ 웹폰트 확보 실패 — Step 4 전 재확인"

echo "  ✓ 셋업 완료"
echo "WORKDIR=$WORK"
