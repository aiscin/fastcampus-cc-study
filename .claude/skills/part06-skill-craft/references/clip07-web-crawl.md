# Clip 7 — 웹 크롤링 스킬 ★ insane-search로 KREAM 트렌드 리포트 (실습 28, 30분)

> 페르소나 메모 — A(마케터): KREAM 트렌드 응용 직관 / B(PO): 경쟁 가격표 모니터링 / C(영업): 본인 고객사 공지 자동 수집

## 자동 셋업

```bash
mkdir -p ~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습28-웹크롤링스킬/trend-report/
mkdir -p ~/fastcampus-cc/.claude/skills/fashion-trend/
echo "✓ 진도 폴더 + fashion-trend 스킬 폴더 (trend-report) 준비 완료"
echo "ℹ insane-search 플러그인 설치 필요 — 아래 [사전 준비] 참고"
```

## 브리핑

**API 없는 사이트도 자동화** — insane-search 플러그인이 WAF·CAPTCHA·로그인 벽을 4단계 적응형으로 우회. 시연 — KREAM 남성 신발 트렌드 → 다크 에디토리얼 매거진 HTML 리포트.

> ⚠️ 크롤링 주의 한 줄 — robots.txt·이용약관 확인, 과도한 요청 자제(딜레이), 개인정보·로그인 영역 제외, 수집 데이터는 본인 분석용으로만. (상업 사이트 우회는 본인 책임)

```
[사전 준비] insane-search 플러그인 설치 (2줄, API 키 불필요)
   /plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
   /plugin install insane-search

[STEP 1] 워크플로우 잡기
   "KREAM에서 키워드의 남녀 인기순을 가져와서 어떤 브랜드가 뜨는지 분석해 트렌드 리포트 만들려는데, 어떻게 워크플로우를 구성해야 할까?"
   → 정보 수집 방법(안티봇 우회 포함) + 분석 방법 + 리포트 구성까지 단계별 정리
[STEP 2] 보완 + 실행 가능 단계 정의
   정리된 단계 보완 → 링크 안 받고 키워드만 받아 sort=male_popularity / female_popularity 두 URL 조립 / 수집은 insane-search / 분석·리포트는 AI로 분리 (AskUserQuestion 키워드·성별 인터랙티브)
[STEP 3] 스킬로 만들기
   fashion-trend 스킬 — URL 조립 → insane-search 수집(직접) → 날짜별 저장 → 남녀 비교 분석 → HTML 리포트 오케스트레이션
[STEP 4] 만든 스킬로 테스트·검증
   "요즘 인기 반팔티 브랜드 트렌드" 호출 → AskUserQuestion(키워드·남/여/둘다) → 남녀 비교 HTML 트렌드 리포트
[STEP 5] 본인 업계 응용 + 주기 실행으로 트렌드 "변화" 추적 (쿠팡·11번가·고객사 공지 등 어디든 같은 패턴)
```

**핵심 메시지** — 그냥 'KREAM 크롤링 스킬 만들어줘' 하지 마세요. **'특정 사이트에서 정보 가져와서 분석해 트렌드 리포트 만들려는데, 어떻게 워크플로우를 구성해야 할까?'**로 출발해야 — 정보 수집 방법(안티봇 우회 포함)부터 분석까지 워크플로우가 잡힙니다. KREAM처럼 봇 차단 사이트도 insane-search가 **막히면 다음 단계로 올려가며** 알아서 우회 — 설치만 하면 자연어로 물어보는 순간 자동 발동. 본인 업계 — 쿠팡·11번가·고객사 공지 — 어디든 같은 패턴.

> 📌 **스크래핑은 직접** — 실제 페이지 수집은 학습자가 직접 해본 영역(이전 클립 경험)이므로, 이 문서는 **"이렇게 활용할 수 있다"는 패턴 안내**만 한다. 떠먹이지 말고 아래 URL 조립·수집 패턴을 보여준 뒤 학습자가 직접 insane-search로 긁게 한다.

**KREAM 검색 URL 조립 규칙** — 링크는 미리 안 받는다. **키워드 하나만 받아** 성별별 정렬 URL 2개를 조립:

```
https://kream.co.kr/search?keyword={키워드}&tab=products&sort={정렬}
                            └ URL인코딩 (예: 반팔티)        └ male_popularity / female_popularity

남성: ...?keyword=반팔티&tab=products&sort=male_popularity
여성: ...?keyword=반팔티&tab=products&sort=female_popularity
```

→ 이 두 URL을 insane-search로 각각 스크래핑 → 상품명·브랜드·가격·거래량 추출 → **남녀 인기 브랜드 비교**가 트렌드 인사이트.

**insane-search 4단계 적응형 우회** (앞 단계가 막혀야 다음 단계로 escalate):

| Phase | 방식 | 비고 |
|------|------|------|
| Phase 0 | 특수 엔드포인트 인덱스 확인 | 가장 가벼움 |
| Phase 1 | WebFetch · Jina Reader · User-Agent 변형 | 경량 탐침 |
| Phase 2 | TLS 핑거프린트 위장 (쿠키·헤더 신원 모방) | curl_cffi |
| Phase 3 | Playwright 전체 브라우저 렌더링 | JS 챌린지 대응 |

> "어떤 방법도 미리 배제하지 마라 — 사이트는 바뀌고, 지금은 그 방법이 통할 수도 있다."

**기존 도구 대비**:

| 도구 | 안티봇 우회 | 설치 | 비고 |
|------|----------|------|------|
| `requests` / BeautifulSoup | ❌ | pip | 정적 페이지·차단 취약 |
| Playwright (MCP) | △ | 무거움 | 기본 Chromium 단일 방식 |
| **insane-search** | ✅ 4단계 적응형 | **플러그인 2줄, API 키 X** | 막히면 단계 올림·한국 사이트 내장(네이버·쿠팡·fmkorea) |

**왜 라이브러리 대신 플러그인인가** — pip 설치·브라우저 다운로드·셀렉터 작성이 없습니다. 깔고 자연어로 물으면 끝. curl_cffi·feedparser·yt-dlp 같은 의존성도 필요 시 자동 설치. Twitter·Reddit·Bluesky·HackerNews는 플랫폼 API로, 한국 사이트는 네이버 검색·쿠팡·fmkorea를 내장 지원.

**트렌드 인사이트**: 단순 데이터 X. 패션 에디터 관점 분석 (브랜드 동향·가격대·시즌) + **남녀 인기 브랜드 비교**. 본인 업계에 그대로 응용.

**날짜 파일명 기준** — 주기적으로 쌓아 트렌드 "변화"를 추적하려면 네이밍 규칙 고정이 필수:

```
원본 데이터  artifacts/kream-{키워드}-{성별}-{YYYY-MM-DD}.md     예: kream-반팔티-남성-2026-05-25.md
리포트       trend-report/{YYYY-MM-DD}-{키워드}-{성별}.html        예: 2026-05-25-반팔티-남성.html
```

→ 날짜 prefix로 정렬·비교가 일관됨. **주기 실행 = 트렌드 변화 추적** — 날짜별로 쌓이면 순위 변동이 보임(예: 6/01 스투시 1위↑·무신사스탠다드 신규 진입). `/schedule`로 "매주 월요일 자동 수집"을 걸면 추적이 자동화. 리포트에 **(선택) 직전 스냅샷 대비 순위 변동 섹션** 추가 가능.

**Part 5 자산 사슬**: clip-05 스킬 구조화 패턴 + 실습 21 trash-guard.

## 단계 안내

| Phase | 내용 |
|------|------|
| A (2분) | 도입 — API 없는 사이트 + insane-search 플러그인 소개 |
| 사전 준비 | insane-search 플러그인 설치 2줄 (크롤링 주의 한 줄은 브리핑에 포함) |
| B-1 (3분) | STEP 1 워크플로우 잡기 — "KREAM에서 키워드의 남녀 인기순 가져와 브랜드 트렌드 분석하려는데 어떻게 구성해야 할까?" |
| B-2 (3분) | STEP 2 보완 + 클로드코드가 실제로 할 수 있는 단계로 정의 (키워드→URL 2개 조립 / 수집은 insane-search / 분석은 AI 분리) |
| B-3 (5분) | STEP 3 fashion-trend 스킬화 — URL 조립 → insane-search 수집(직접) → 날짜별 저장 → 남녀 비교 분석 → HTML |
| B-4 (8분) | STEP 4 만든 스킬로 테스트·검증 — "반팔티" 키워드 + AskUserQuestion(남/여/둘다) + 남녀 비교 HTML 리포트 |
| B-5 (3분) | STEP 5 본인 업계 응용 + 주기 실행(/schedule)으로 트렌드 변화 추적 |
| C (1분) | 마무리 — API 없는 사이트도 30초에 |
| D (1분) | WRAP |

## WRAP

1. 결과물 검증 — `fashion-trend/SKILL.md` + `artifacts/kream-{키워드}-{성별}-{YYYY-MM-DD}.md`(수집 원본) + `trend-report/{YYYY-MM-DD}-{키워드}-{성별}.html` (날짜 파일명 기준 준수)
2. README — insane-search 플러그인 패턴 + KREAM URL 조립 규칙 + 본인 업계 사이트 1개 후보
3. progress.json — `practice_completed`에 28, `skills_created`에 `fashion-trend`
4. 회고 — "본인 업계 크롤링 + 주기 실행으로 트렌드 변화 추적 한 줄"
5. 다음 — "clip-08 audio-to-doc (회의록 메인 + 유튜브 시연 우회)"
