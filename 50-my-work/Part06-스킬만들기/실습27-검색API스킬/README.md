# 실습 27 — 검색 API 스킬 ★ 네이버 뉴스 → 반도체 종목 뉴스레터

> 페르소나 — A(마케터): 브랜드 모니터링 / B(PO): 경쟁 동향 / C(영업): 고객사 동향
> 완료: 2026-06-25 · 모델: Claude Opus 4.8 · 모드: Plan/Edit

## 무엇을 만들었나
네이버 검색 API로 **반도체 보유종목 일일 주식 뉴스레터**를 자동 생성하는 `naver-news` 스킬.
종목·업황 뉴스를 모아 → 종목별 호재/악재 분류(근거 인용) → 모바일 HTML 뉴스레터로 발행.

**워치리스트**: 마이크로컨텍솔(098120) · 씨엠티엑스(388210) · 이노테크(469610) — 전부 코스닥 반도체.

## 메타 흐름대로 진행 (그냥 "만들어줘" X)
1. **워크플로우 잡기** — "키워드 뉴스 모아서 뉴스레터, 어떻게 구성?"
2. **전문가 토론으로 디벨롭** (kkirikkiri) — 반도체 애널리스트·증권 분석가·콘텐츠 전략가 3인 → "뉴스 검색만으론 부족(공시·지표 필요), 근거 인용 강제, 오늘의 PICK/TL;DR" 등 보강
3. **스킬화** — `fetch_news.py`(결정론: 수집·기간계산·태깅·정제) + `SKILL.md`(AI: 분석·HTML)
4. **테스트·검증·개선** (skillers-suda 4인 점검) — 워치리스트 외부화·HTTP 에러 처리·매크로 상한·**오태깅 경계매칭**·멱등성·컴플라이언스 강화

## 스크립트 분리 패턴 (CH02 모범)
| 영역 | 담당 | 이유 |
|---|---|---|
| 수집·기간계산·종목태깅·정제·등급·휴장판정 | 🐍 `fetch_news.py` | 같은 입력 → 같은 결과 (재현성) |
| 호재/악재 판단·요약·HTML 디자인 | 🤖 `SKILL.md`(AI) | 맥락 해석·유연성 |

## 결과물
- `.claude/skills/naver-news/` — SKILL.md · watchlist.json(config) · requirements.txt · cloud-run.md · scripts/(fetch_news.py · generate_newsletter.py)
- `newsletter/` — 6/19·22·23·24 4일치 HTML + index.html(누적) + assets/style.css(공유)
- `.github/workflows/newsletter.yml` — 평일 07:30 KST 자동 발행(보류, [[naver-news-auto-publish]] 참조)

## 핵심 디테일 (부딪혀야 아는 것)
- **공휴일 ≠ 증시 휴장일** — 근로자의날(5/1)·연말폐장(12/31)은 법정공휴일 아닌데 증시 휴장 → `holidays` 라이브러리 + 보충 규칙. graceful fallback 포함.
- **오태깅** — "이노테크홀"(건물명) 같은 합성어를 정규식 경계+조사 매칭으로 차단.
- **클라우드 ≠ 외부 API** — `/schedule` 클라우드 루틴은 네이버 egress 차단 → GitHub Actions로 우회.
- **비공개 레포 → Pages 불가** → public 전환.

## Part 5 자산 사슬
- 실습20 .env 패턴(TourAPI) → NAVER 키 보관 재사용
- 실습22 GitHub 백업 → 스킬·뉴스레터 push + Pages 발행
- clip-05 trip-advisor → .env + Python 스크립트 분리 패턴 그대로 + HTML 한 단계 더

## 회고
(생략)
