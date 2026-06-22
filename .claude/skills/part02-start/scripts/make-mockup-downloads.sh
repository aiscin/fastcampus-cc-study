#!/usr/bin/env bash
# Part 02 clip-03 (실습 3 — 다운로드 폴더 정리) 시연용 목업 파일 생성기
#
# 50+ 개의 다양한 확장자 파일을 자동 생성한다.
# clip-03 강사 시연 출력(파일 종류별 분류표)에 매칭되도록 분포 설계:
#   문서 (PDF/DOCX) ~ 36% / 이미지 (JPG/PNG) ~ 30% / 압축 (ZIP/RAR) ~ 12%
#   스프레드시트 (XLSX/CSV) ~ 14% / 기타 (PPTX/MD/TXT) ~ 8%
#
# 사용법:
#   bash make-mockup-downloads.sh                # 기본: 실제 다운로드 폴더 안 cc-demo 하위 폴더
#   bash make-mockup-downloads.sh --in-place     # 실제 다운로드 폴더에 직접 (강사 시연용 — 본인 파일과 섞임 주의)
#   bash make-mockup-downloads.sh ~/my-folder    # 사용자 지정 경로
#
# OS 자동 감지: macOS / Linux / WSL2 모두 ~/Downloads 인식

set -euo pipefail

# ===== OS 자동 감지 + 다운로드 경로 =====
detect_downloads_dir() {
  case "$(uname -s)" in
    Darwin)  echo "$HOME/Downloads" ;;          # macOS
    Linux)
      # WSL 감지: /proc/version에 microsoft가 있으면 WSL
      if grep -qi microsoft /proc/version 2>/dev/null; then
        # WSL: ~/Downloads 우선 (WSL 홈), 없으면 Windows 다운로드
        if [[ -d "$HOME/Downloads" ]]; then
          echo "$HOME/Downloads"
        else
          # Windows 사용자 폴더 추정
          local win_user
          win_user=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r' || echo "")
          if [[ -n "$win_user" && -d "/mnt/c/Users/$win_user/Downloads" ]]; then
            echo "/mnt/c/Users/$win_user/Downloads"
          else
            echo "$HOME/Downloads"
          fi
        fi
      else
        echo "$HOME/Downloads"
      fi
      ;;
    *) echo "$HOME/Downloads" ;;
  esac
}

# ===== 인자 파싱 =====
IN_PLACE=false
USER_DIR=""

for arg in "$@"; do
  case "$arg" in
    --in-place) IN_PLACE=true ;;
    -*) echo "[WARN] 알 수 없는 옵션: $arg" >&2 ;;
    *)  USER_DIR="$arg" ;;
  esac
done

DOWNLOADS_DIR=$(detect_downloads_dir)

if [[ -n "$USER_DIR" ]]; then
  OUT_DIR="$USER_DIR"
elif [[ "$IN_PLACE" == true ]]; then
  OUT_DIR="$DOWNLOADS_DIR"
else
  OUT_DIR="$DOWNLOADS_DIR/cc-demo"
fi

mkdir -p "$OUT_DIR"
cd "$OUT_DIR"

echo "[INFO] OS:           $(uname -s)"
echo "[INFO] Downloads:    $DOWNLOADS_DIR"
echo "[INFO] 생성 위치:    $OUT_DIR"
echo "[INFO] 파일 50+개를 다양한 확장자로 생성합니다."
echo ""

# ===== 파일 카탈로그 =====

# 문서 (PDF) — 12개
PDFS=(
  "report-Q1-2025.pdf"  "report-Q2-2025.pdf"  "report-Q3-2025.pdf"
  "manual_v2.pdf"  "invoice_2026_03.pdf"  "invoice_2026_04.pdf"
  "contract-draft.pdf"  "research-paper.pdf"  "tax-form-2025.pdf"
  "presentation-final.pdf"  "user-guide.pdf"  "ebook-claude-code.pdf"
)

# 문서 (DOCX) — 6개
DOCX=(
  "meeting-notes.docx"  "project-proposal.docx"  "resume-2026.docx"
  "thesis-draft.docx"  "weekly-report.docx"  "letter-template.docx"
)

# 이미지 (JPG) — 9개
JPGS=(
  "vacation-photo-1.jpg"  "vacation-photo-2.jpg"  "profile.jpg"
  "team-meeting.jpg"  "family.jpg"  "concert.jpg"
  "food-1.jpg"  "food-2.jpg"  "scenery.jpg"
)

# 이미지 (PNG) — 6개
PNGS=(
  "screenshot-2026-04-01.png"  "screenshot-2026-04-12.png"
  "logo-final.png"  "design-mockup.png"  "icon-set.png"  "diagram.png"
)

# 스프레드시트 (XLSX) — 5개
XLSX=(
  "budget-2026.xlsx"  "sales-data-Q1.xlsx"  "expense-report.xlsx"
  "inventory.xlsx"  "employee-list.xlsx"
)

# 스프레드시트 (CSV) — 2개
CSVS=(
  "customer-data.csv"  "logs-2026-04.csv"
)

# 압축파일 (ZIP) — 5개
ZIPS=(
  "backup-2026-03.zip"  "photos-trip.zip"  "old-projects.zip"
  "archive-2025.zip"  "source-code.zip"
)

# 압축파일 (RAR) — 1개 (다양성)
RARS=(
  "legacy-files.rar"
)

# 기타 — 4개
OTHERS=(
  "kickoff-deck.pptx"  "todo.md"  "notes.txt"  "license.txt"
)

# ===== 모두 생성 =====
ALL=("${PDFS[@]}" "${DOCX[@]}" "${JPGS[@]}" "${PNGS[@]}" "${XLSX[@]}" "${CSVS[@]}" "${ZIPS[@]}" "${RARS[@]}" "${OTHERS[@]}")

for f in "${ALL[@]}"; do
  printf 'mockup file for download folder demo\nfilename: %s\ngenerated: %s\n' "$f" "$(date)" > "$f"
done

# ===== 결과 요약 =====
TOTAL=${#ALL[@]}
echo "[DONE] 총 ${TOTAL}개 파일 생성 완료."
echo ""
echo "분포 (clip-03 강사 시연 출력 매칭):"
echo "  📄 문서 PDF:        ${#PDFS[@]}개"
echo "  📝 문서 DOCX:       ${#DOCX[@]}개"
echo "  🖼  이미지 JPG:      ${#JPGS[@]}개"
echo "  🖼  이미지 PNG:      ${#PNGS[@]}개"
echo "  📊 스프레드시트 XLSX: ${#XLSX[@]}개"
echo "  📊 스프레드시트 CSV:  ${#CSVS[@]}개"
echo "  📦 압축 ZIP:        ${#ZIPS[@]}개"
echo "  📦 압축 RAR:        ${#RARS[@]}개"
echo "  🗂  기타:            ${#OTHERS[@]}개 (PPTX/MD/TXT)"
echo ""
echo "총: ${TOTAL}개  ($(du -sh "$OUT_DIR" 2>/dev/null | cut -f1) 사용)"
echo ""
echo "[다음 단계] Claude Code 실습:"
echo "  cc"
echo "  >>> $OUT_DIR 정리하려는데 어떻게 해? 먼저 분석해서 어떻게 정리하면 좋을지 알려줘"
echo ""
echo "[참고] 정리 후 원래 상태로 되돌리려면:"
echo "  rm -rf \"$OUT_DIR\" && bash $0 ${USER_DIR:+\"$USER_DIR\"} ${IN_PLACE:+--in-place}"
