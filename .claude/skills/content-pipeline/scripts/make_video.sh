#!/usr/bin/env bash
# make_video.sh — 카드 PNG + 씬 음성 + 타이밍 → Remotion 9:16 릴스 (결정론 단계)
# 사용: make_video.sh <workdir>
set -e
WORK="$(cd "$1" && pwd)"
REM="$(cd "$(dirname "$0")/../remotion" && pwd)"

echo "▶ 에셋 준비 (라이브 HTML 카드)"
mkdir -p "$REM/public/audio" "$REM/public/fonts" "$REM/public/images" "$REM/out"
cp "$WORK"/audio/card-*.mp3 "$REM/public/audio/"
cp "$WORK"/fonts/*.woff2 "$WORK"/fonts/*.ttf "$REM/public/fonts/"
cp -r "$WORK"/images/. "$REM/public/images/"

# card-news.html → CSS + 카드 10개 추출 (url 경로를 /fonts·/images 로 재작성) → src/cards.json
python3 - "$WORK/card-news.html" "$REM/src/cards.json" <<'PY'
import sys, json, re
from bs4 import BeautifulSoup
html = open(sys.argv[1], encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")
css = soup.style.string or ""
def fix(t):
    t = t.replace("url('fonts/", "url('/fonts/").replace('url("fonts/', 'url("/fonts/')
    t = t.replace("url('images/", "url('/images/").replace('url("images/', 'url("/images/')
    t = t.replace('src="images/', 'src="/images/')
    return t
cards = [fix(str(s)) for s in soup.select("section.card")]
css = fix(css)
json.dump({"css": css, "cards": cards}, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
print(f"  ✓ cards.json (카드 {len(cards)}개, css {len(css)}자)")
PY

# 배경음악(있으면) + bgm 플래그를 timings에 주입해 src로 복사
BGM=0
if [ -f "$WORK/bgm.mp3" ]; then cp "$WORK/bgm.mp3" "$REM/public/bgm.mp3"; BGM=1; fi
python3 - "$WORK/card-timings.json" "$REM/src/timings.json" "$BGM" <<'PY'
import json,sys
src,dst,bgm=sys.argv[1],sys.argv[2],sys.argv[3]=="1"
d=json.load(open(src,encoding="utf-8")); d["bgm"]=bgm
json.dump(d,open(dst,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(f"  ✓ timings.json (씬 {len(d['scenes'])}개, bgm={bgm})")
PY

echo "▶ Remotion 렌더 (9:16)"
cd "$REM"
# Remotion 전용 브라우저 다운로드가 막히는 환경 → playwright 크로미움 재사용
BROWSER="$(find "$HOME/.cache/ms-playwright" -type f -name chrome 2>/dev/null | head -1)"
BR_FLAG=""
[ -n "$BROWSER" ] && BR_FLAG="--browser-executable=$BROWSER" && echo "  브라우저: $BROWSER"
# WSL에서 낮은 포트는 connect 타임아웃 → Remotion이 "사용 중"으로 오판. 비어있는 높은 포트를 직접 지정.
PORT="$(python3 -c "import socket;s=socket.socket();s.bind(('127.0.0.1',0));print(s.getsockname()[1]);s.close()")"
echo "  포트: $PORT"
npx remotion render CardReel out/output.mp4 --log=error --port="$PORT" \
  --concurrency=3 --timeout=120000 $BR_FLAG

cp "$REM/out/output.mp4" "$WORK/output.mp4"
echo "✓ 완료 → $WORK/output.mp4"
ffprobe -v quiet -of json -show_format "$WORK/output.mp4" 2>/dev/null | python3 -c "import sys,json; f=json.load(sys.stdin)['format']; print(f\"  길이 {float(f['duration']):.1f}s · {int(f['size'])//1024}KB\")"
