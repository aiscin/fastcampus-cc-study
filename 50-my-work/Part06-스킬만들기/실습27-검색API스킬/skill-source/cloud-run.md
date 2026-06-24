# naver-news — 클라우드 무인 발행 런북 (Cloud Routine 전용)

이 문서는 `/schedule` 클라우드 루틴이 매일 자동 실행할 때 따르는 **무인(unattended) 흐름**이다.
로컬 대화형(SKILL.md STEP 0의 AskUserQuestion)과 다르다 — **사람이 없으므로 질문 금지, 고정값 사용**.

## 실행 환경 전제
- Anthropic 클라우드에서 레포가 이미 클론된 상태로 시작한다.
- 네이버 키는 **환경변수** `NAVER_CLIENT_ID` / `NAVER_CLIENT_SECRET` 로 주어진다 (로컬 `.env` 없음).
  `fetch_news.py`의 `load_env()`가 환경변수를 먼저 읽으므로 그대로 동작한다.
- 작업 디렉토리 = 레포 루트.

## 무인 흐름 (순서대로)

### 1. 의존성 설치
```bash
python3 -m pip install --user --break-system-packages -r .claude/skills/naver-news/requirements.txt
```
실패해도 진행 가능(holidays 없으면 주말+증시전용만 판정). 단 로그에 남긴다.

### 2. 뉴스 수집 (고정값 — 질문하지 않음)
```bash
python3 .claude/skills/naver-news/scripts/fetch_news.py --sort date
```
기간은 요일 기반 자동(월=주말포함). `--sort date`(최신순) 고정.

### 3. 게이트 체크 (발행 여부 결정)
- `market_closed == true` → **발행하지 않고 종료**. 휴장 사유를 로그로 남긴다. (장이 안 열린 날은 종목 뉴스가 의미 없음)
- `has_error == true` 이고 exit code 1(데이터 0건+에러) → **발행하지 않고 종료**. 에러 원인 로그.
- 일부 종목만 실패(데이터 있음) → 진행하되 뉴스레터 상단에 "일부 수집 실패" 한 줄 표시.

### 4. 분석 + HTML 생성 (SKILL.md STEP 2~4 그대로, 단 질문 없이)
- 종목별 호재/악재 분류 + **근거 문장 인용 필수**, 애매하면 ⚪중립.
- `unverified:true`(C급 단독) → "(미확인)" 표기.
- 오늘의 PICK + TL;DR 3줄 + 면책(헤더·PICK·푸터).
- 스타일은 `newsletter/assets/style.css` 를 링크(`../../assets/style.css`).

### 5. 저장 + 누적
- `50-my-work/Part06-스킬만들기/실습27-검색API스킬/newsletter/{YYYY}/{MM}/{YYYYMMDD}-반도체.html` (폴더 없으면 mkdir -p).
- `newsletter/index.html` 맨 위에 오늘치 링크 **upsert**(같은 날짜 중복 금지).
- 전체 0건이어도 "뉴스 없는 날" 템플릿으로 발행(단 3번 게이트로 종료된 경우는 예외).

### 6. 커밋 + 푸시 (GitHub Pages 갱신)
```bash
git add "50-my-work/Part06-스킬만들기/실습27-검색API스킬/newsletter/"
git commit -m "newsletter: $(date +%Y-%m-%d) 반도체"
git push origin main
```
푸시가 성공해야 GitHub Pages에 반영된다. 푸시 실패 시 원인을 로그로 남긴다.

## 절대 하지 마
- AskUserQuestion 호출 (무인 — 멈춤)
- `.env` 파일을 git add (키 유출)
- 휴장일/수집실패인데 빈 뉴스레터 강제 발행
