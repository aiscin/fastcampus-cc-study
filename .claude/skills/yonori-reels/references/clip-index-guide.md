# 클립 인덱스 가이드 (Step 5 클립 선별용 — 여행 폴더당 1회 구축)

> 목적: 클립 선별이 전체 작업의 최대 병목(수동 검색+프레임 육안 확인 반복)이었다.
> 여행 폴더마다 인덱스 CSV를 **한 번만** 만들어두면 이후 릴스는 인덱스 조회로 끝난다 = 토큰·시간 대폭 절약.

## 기기별 시간 규칙 (2026-07-07 튀르키예 3,555파일 실측)

| 기기 (하위폴더) | 파일명 패턴 | 파일명 시각 | LastWriteTime | 판정 규칙 |
|---|---|---|---|---|
| 삼성 핸드폰 (성수핸드폰/여리핸드폰) | `YYYYMMDD_HHMMSS` | **현지 시각** | 한국 시각 (현지+6h, 튀르키예 기준) | 파일명으로 현지 일정 매칭 |
| 아이폰 | `YYYYMMDDHHMMSS_IMG_nnnn` | ≈ **한국 시각** | 복사 시점일 수 있음 | 파일명 −(시차)로 현지 환산 |
| 드론 (DJI) | `dji_fly_YYYYMMDD_HHMMSS_...` | ≈ **한국 시각** | 백업 시각 | 파일명 −(시차)로 현지 환산. `video_low_quality` = 720p 백업본 ⚠️ |
| 고프로 | `GX...` | 시각 정보 없음 | **백업일 (무의미)** | 시각 불명 — 내용으로만 판정 |
| 카메라 (IMG_nnnn.JPG) | 순번만 | 시각 정보 없음 | 대체로 한국 시각 | LWT −(시차) 추정, 신뢰 낮음 |

⚠️ 시차는 여행지마다 다르다 — 튀르키예 = 한국−6h. 새 여행 인덱스 구축 시 시차부터 확인.

## 구축 절차 (WSL에서 F: 등 미마운트 드라이브)

1. PowerShell로 파일 목록 덤프 (1회):
```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command '[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-ChildItem -Path "F:\...\여행폴더" -Recurse -File | ForEach-Object { $_.FullName + "`t" + $_.Length + "`t" + $_.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss") }' > listing.tsv
```
2. 인덱스 생성:
```bash
python3 scripts/index_clips.py --listing listing.tsv --tz-offset -6 --out clip-index.csv
```
3. `clip-index.csv`를 여행 폴더 대응 위치(예: `50-my-work/reels/_index/{여행명}.csv`)에 저장 — 이후 모든 릴스가 재사용.

## 사용 규칙 (토큰 절약)

- 장면 후보 검색은 **CSV 조회만**으로 좁힌다 (일정표의 날짜·시간대와 대조)
- 프레임 추출 육안 확인은 **최종 매핑 후보만, 장면당 1컷, 360px 축소본** — 같은 프레임 재확인 금지
- `low_quality=1`(해상도<1080p) 클립은 매핑표에 ⚠️ 표시하고 고화질 원본 존재 여부를 사용자에게 확인
