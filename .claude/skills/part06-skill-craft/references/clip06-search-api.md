# Clip 6 — 검색 API 스킬 ★ 네이버 뉴스 → 뉴스레터 HTML + AskUserQuestion 인터랙티브 (실습 27, 20분)

> 페르소나 메모 — A(마케터): 본인 브랜드 모니터링 자동화 / B(PO): 경쟁 키워드 + 트렌드 인사이트 / C(영업): 고객사 동향 자동 수집

## 자동 셋업

```bash
mkdir -p ~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습27-검색API스킬/newsletter/
mkdir -p ~/fastcampus-cc/.claude/skills/naver-news/scripts/
echo "✓ 진도 폴더 + naver-news 스킬 폴더 (scripts + newsletter) 준비 완료"
```

> **누적 발행 모드** — 매일 자동 갱신되는 GitHub Pages 뉴스레터까지 만든다면, `newsletter/` 안에 **`index.html`(누적 목록 페이지)** 도 함께 초기화한다. 날짜별 파일이 쌓이고, index.html이 그 링크를 모은다.

## 브리핑

**검색 API + 뉴스레터 HTML 자동 생성**. clip-05 .env + Python 스크립트 분리 패턴 그대로 재사용 + 한 단계 더 (HTML 디자인).

```
[사전 준비] 네이버 개발자센터(developers.naver.com) 키 발급 → 애플리케이션 등록 시 사용 API='검색' + 비로그인 오픈 API 'WEB 설정' + URL 'http://localhost' (Client ID + Secret) + .env에 NAVER_CLIENT_ID/SECRET 보관

[STEP 1] 워크플로우 잡기
   "네이버 검색 API로 키워드 뉴스 모아서 뉴스레터 만들려는데, 어떻게 워크플로우를 구성해야 할까?"
   → 단계별 워크플로우 정리
[STEP 2] 보완 + 실행 가능 단계 정의
   정리된 단계 살펴보고 보완 → 클로드코드가 실제로 할 수 있는 단계로 다듬기 (API 호출·24h 필터·HTML 클린 분리)
[STEP 3] 스킬로 만들기
   naver-news 스킬 + scripts/fetch_news.py 분리 (Python)
[STEP 4] 만든 스킬로 테스트·검증
   "클로드코드 뉴스레터 만들어줘" + AskUserQuestion 답변 (정렬 + 시간) → HTML 뉴스레터
   ※ 단, 무인 자동(루틴) 모드면 AskUserQuestion 못 씀 → '최신순 + 24h' 고정값으로 분기
[STEP 5] 본인 키워드 응용 + clip-05·06 공통 패턴 정리
[STEP 6] (선택) 매일 자동 발행 — GitHub Pages + 루틴 등록
   ① index.html 누적 로직: 오늘치 HTML 생성 + index.html 맨 위에 링크 한 줄 추가
   ② GitHub Pages 켜기 (Settings → Pages → Source = main) → 누적 목록을 웹에서 확인
   ③ 키는 로컬 .env가 아니라 클라우드 환경변수(NAVER_CLIENT_ID/SECRET)로 등록 — 루틴은 로컬 .env 못 봄
   ④ /schedule로 매일 정해진 시간 루틴 등록 (커밋·푸시까지 프롬프트에 포함)
```

**핵심 메시지** — 단순 검색 결과 5개 던지지 말고 **뉴스레터로 자동 정리**. 그냥 'naver-news 스킬 만들어줘' 하지 마세요. **'키워드 뉴스 모아서 뉴스레터 만들려는데, 어떻게 워크플로우를 구성해야 할까?'**로 출발. 카테고리 그룹핑 + 트렌드 인사이트 + 모바일 반응형 HTML 디자인까지. 본인 일에 마케터(브랜드 모니터링)·PO(경쟁 동향)·영업(고객사 동향) 그대로 응용.

**AskUserQuestion 인터랙티브**: Q1 정렬(최신순/관련도순) → Q2 시간 범위(6h/24h/48h, 최신순일 때만). **스킬도 호출 시점에 사용자에게 물어보는 패턴**.

**clip-05·06 공통 패턴 (학생 체득)**:

| 단계 | trip-advisor (clip-05) | naver-news (clip-06) |
|------|---------------------|----------------|
| 키 발급 | 공공데이터포털 TourAPI | 네이버 개발자센터 |
| .env 보관 | TOURAPI_SERVICE_KEY | NAVER_CLIENT_ID/SECRET |
| Python 스크립트 | tour_api.py (5 액션) | fetch_news.py (검색+필터) |
| 인터랙티브 | 자연어 입력 | AskUserQuestion 2단 |
| 산출 | 마크다운 가이드 | HTML 뉴스레터 |

**Part 5 자산 사슬**: clip-05 .env + Python 스크립트 분리 패턴 그대로 재활용 + 실습 21 trash-guard.

## 단계 안내

| Phase | 내용 |
|------|------|
| A (1.5분) | 도입 — 검색 결과 X → 뉴스레터로 |
| 사전 준비 | 네이버 개발자센터 키 발급 (등록 시 사용 API='검색' + 'WEB 설정' + URL `http://localhost`) → Client ID/Secret + `.env` 보관 (clip-05 패턴 통일) |
| B-1 (3분) | STEP 1 워크플로우 잡기 — "키워드 뉴스 → 뉴스레터 만들려는데 어떻게 구성해야 할까?" |
| B-2 (3분) | STEP 2 보완 + 클로드코드가 실제로 할 수 있는 단계로 정의 (API 호출·HTML 클린 분리) |
| B-3 (4분) | STEP 3 naver-news 스킬화 + `fetch_news.py` 분리 |
| B-4 (3분) | STEP 4 만든 스킬로 테스트·검증 — "클로드코드 뉴스레터 만들어줘" + AskUserQuestion 2단 |
| B-5 (2분) | STEP 5 HTML 뉴스레터 브라우저 펼침 + 본인 키워드 응용 + clip-05·06 공통 패턴 정리 |
| B-6 (선택) | STEP 6 매일 자동 발행 — index.html 누적 + GitHub Pages 켜기 + 클라우드 환경변수 키 등록 + `/schedule` 루틴 (커밋·푸시 포함) |
| C (1분) | 마무리 — 외부 API 두 번째 패턴 |
| D (0.5분) | WRAP |

## WRAP

1. 결과물 검증 — `naver-news/SKILL.md` + `scripts/fetch_news.py` + `.env` + `newsletter/{YYYYMMDD}-{키워드}.html` (+ 누적 모드면 `newsletter/index.html`)
2. README — clip-05 vs clip-06 공통 패턴 표 + 본인 키워드 1개 후보
3. progress.json — `practice_completed`에 27, `skills_created`에 `naver-news`
4. 회고 — "본인 모니터링 키워드 한 줄"
5. (선택) 자동 발행 검증 — GitHub Pages URL(`https://{유저}.github.io/{repo}/newsletter/`) 열림 + 등록한 루틴 ID 확인
6. 다음 — "clip-07 Scrapling으로 KREAM 크롤링 + 트렌드 HTML"
