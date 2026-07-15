# 실습31 — 콘텐츠 파이프라인 스킬 ★ Part 06 마지막

> 완료: 2026-07-04 · 모델: Claude Opus 4.8 · 모드: 대화형
> 만든 스킬: **content-pipeline** (딥리서치 → 카드뉴스 → 영상)

## 무엇을 만들었나

주제 한 마디 → **리서치·기획·이미지·카드뉴스·음성·BGM·영상**까지 6 STEP 풀 파이프라인을 구축하고, 그 노하우를 **재사용 스킬로 자산화**했다.

### 시연 산출물 (`kream-반팔티-2026-07-03/`)
| 파일 | 내용 |
|---|---|
| `01`~ / `02-plan.json` | 리서치 자료(실습28 재활용) + 카드뉴스 기획 |
| `card-news.html` + `preview/card-01~10.png` | 카드뉴스 10장 (실사진 하이브리드 · 흑백+레드) |
| `05-tts-script.md` + `audio/*.mp3` | 반말 나레이션(nova) 10씬 + 타이밍 |
| `bgm.mp3` | 저작권 무관 앰비언트 BGM |
| **`output.mp4`** | ★ 4:5 세로 영상 51.8초 — 라이브 HTML 등장 효과 + 자막 + BGM |

### 자산화한 스킬 (`.claude/skills/content-pipeline/`)
- `SKILL.md` — 리서치→카드뉴스 자동, 영상 옵션 오케스트레이터 (검증 8/8 PASS)
- `scripts/` — setup · generate_image · render_cards · tts_and_timing · gen_bgm · make_video (+옵션 fetch_kream_images)
- `remotion/` — 라이브 HTML 카드 렌더 + 프레임 구동 등장 효과
- `references/` — card-news-guide · image-prompt-generator

## 배운 핵심 (Part 06 메타 메시지)
- **자산화** — 만든 노하우를 스킬로 남겨 다음부터 한 마디로 재현
- **재호출 vs 자체제작** — 리서치=deep-research 재호출, 나머지=자체 스크립트
- **결정론은 스크립트 / 창작은 문서** — API·크롭·타이밍·렌더=코드, 기획·카피=AI
- **과금 방어 · 저작권 게이트 · 환경 폴백**(브라우저·포트·폰트)

## Part 5 자산 사슬
- 실습18 CLAUDE.md(한글·시각화 규칙) → 전 과정 컨텍스트
- deep-research 스킬(Part 06) → Step 1 재호출
- trash-guard hook(실습21) → rm 안전장치
- GitHub 백업(실습22) → 만든 스킬 묶음 백업 대상
