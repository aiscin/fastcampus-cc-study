#!/usr/bin/env bash
# gen_bgm.sh — 저작권 무관한 잔잔한 앰비언트 BGM 합성 (ffmpeg 사인 패드)
# 코드 진행 C–Am–F–G ×2, 로우패스 + 가벼운 리버브. 사용: gen_bgm.sh <out.mp3> [초]
set -e
OUT="$1"; LEN="${2:-53}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
SEG=8      # 코드 길이(초)
XF=1.5     # 크로스페이드(초)

# 코드별 4음(저음 root + 트라이어드) — 따뜻하게
chord(){ # $1 name, $2..$5 freqs
  ffmpeg -y -loglevel error \
    -f lavfi -i "sine=frequency=$2:duration=$SEG" \
    -f lavfi -i "sine=frequency=$3:duration=$SEG" \
    -f lavfi -i "sine=frequency=$4:duration=$SEG" \
    -f lavfi -i "sine=frequency=$5:duration=$SEG" \
    -filter_complex "[0][1][2][3]amix=inputs=4:normalize=1,tremolo=f=0.13:d=0.18,lowpass=f=1500,aformat=channel_layouts=stereo" \
    "$TMP/$1.wav"
}
chord c1 130.81 261.63 329.63 392.00   # C
chord a1 110.00 220.00 261.63 329.63   # Am
chord f1 174.61 220.00 261.63 349.23   # F
chord g1  98.00 196.00 246.94 293.66   # G

# C Am F G ×2 순서로 크로스페이드 이어붙임
ORDER=(c1 a1 f1 g1 c1 a1 f1 g1)
cp "$TMP/${ORDER[0]}.wav" "$TMP/cur.wav"
for i in $(seq 1 $((${#ORDER[@]}-1))); do
  ffmpeg -y -loglevel error -i "$TMP/cur.wav" -i "$TMP/${ORDER[$i]}.wav" \
    -filter_complex "acrossfade=d=$XF:c1=tri:c2=tri" "$TMP/next.wav"
  mv "$TMP/next.wav" "$TMP/cur.wav"
done

# 마스터: 가벼운 리버브 + 전체 페이드 인/아웃 + 길이 맞춤
ffmpeg -y -loglevel error -i "$TMP/cur.wav" \
  -af "aecho=0.8:0.85:55:0.35,volume=0.9,afade=t=in:st=0:d=2,afade=t=out:st=$((LEN-3)):d=3,atrim=0:$LEN" \
  -ar 44100 -b:a 160k "$OUT"
echo "✓ BGM → $OUT ($(ffprobe -v quiet -of csv=p=0 -show_entries format=duration "$OUT" | cut -d. -f1)s)"
