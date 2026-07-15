# TrendBoard 빌드 가이드 — 유튜브 트렌드 분석 대시보드 (원본/풀버전)

> 클로드코드와 대화하면서 **원본 수준(Supabase + Outlier Score + 매시간 자동 수집)** 의
> 유튜브 트렌드 분석 대시보드를 처음부터 끝까지 만드는 가이드.
> 패스트캠퍼스 클로드코드 강의 — Part 7 「바이브코딩」 세 번째 프로젝트용.

---

## 무엇을 만드나

여러 유튜브 채널을 등록하면, **매시간 자동으로** 영상 성과(조회수·좋아요·댓글)를 수집해
DB에 쌓고, **채널 평균 대비 얼마나 터졌는지(Outlier)** 를 자동으로 계산해서 한눈에 보여주는 웹 대시보드.

핵심 화면 7개:

| 페이지 | 하는 일 |
|--------|---------|
| **Overview** | 전체 요약 — 채널/영상 수, 이번 주 Outlier, 트렌드 1위, Score 추이 차트 |
| **Channels** | 채널 등록/삭제/활성토글 (URL 붙여넣으면 자동 메타데이터 로드) |
| **Videos** | 전체 영상 테이블 (최신순) |
| **Outliers** ★ | 앱의 핵심 — "평소보다 터진 영상"을 Score/Ch.Avg 배율로 정렬·필터 |
| **Trends** | 키워드 트렌드 랭킹 + 성장률 + 바 차트 |
| **Strategy** | (선택) AI가 데이터 보고 콘텐츠 전략 제안 |
| **Admin** | Gemini API 키 등 설정 관리 (비밀번호 게이트) |

---

## "원본"과 "단순판"의 차이 (왜 이 가이드인가)

강의 진행안에는 yt-dlp + 정적 HTML로 만드는 **단순판**도 있다. 이 가이드는 그보다 한 단계 위인 **원본/풀버전**이다.

| | 단순판 | **이 가이드 (원본)** |
|---|---|---|
| 데이터 | yt-dlp로 새 영상 자막 | YouTube Data API로 조회수/좋아요/댓글 시계열 |
| 분석 | 내용 요약만 | **Outlier Score, Ch.Avg 배율, V/S Ratio, Tier 랭킹** |
| 저장 | JSON 파일 | **Supabase(PostgreSQL) — 매시간 스냅샷 누적** |
| AI 요약 | 빌드 시 1회 | Gemini로 신규 영상 자동 요약 + 키워드/태그 |
| 자동화 | 매일 재배포 | **매시간 cron — 수집→요약→트렌드 체인** |
| 필요한 가입/키 | GitHub, Vercel | + Supabase, Google Cloud(YouTube), Google AI Studio(Gemini) |

> 한 줄 요약: **단순판 = "뭐 올라왔나" / 원본 = "뭐가 평소보다 터졌나"를 숫자로 분석.**

---

## 기술 스택

| 영역 | 선택 |
|------|------|
| 프론트엔드 | React + TypeScript + Vite |
| UI | Tailwind CSS + shadcn/ui (다크 테마 기본) |
| 차트 | Recharts |
| DB/백엔드 | Supabase (PostgreSQL + Edge Functions + pg_cron) |
| 영상 데이터 | YouTube Data API v3 |
| AI 요약 | Google Gemini (gemini-2.5-flash-lite) |
| 배포 | Vercel (+ GitHub) |
| 빌더 | **바이브코딩** — `/show-me-the-prd`(PRD) + `/kkirikkiri`(코드 생성) + 클로드코드(연결·배포) |

예상 비용: 개인용 기준 **월 $0~5** (Supabase Free, Gemini 무료 티어, YouTube API 무료 쿼터).

---

## 진행 방식 — 바이브코딩 2단 흐름

이 프로젝트는 **코드를 손으로 타이핑하지 않는다.** 스킬과 클로드코드에게 *무엇을* 만들지 말로 설명하면
파일을 쓰고, 마이그레이션을 돌리고, Edge Function을 배포하고, Vercel에 올린다.

```
[Phase 1 — 생성]
  /show-me-the-prd   → PRD 4종 자동 생성 (제품/데이터/단계/스펙)
       ↓ 구체화      → 그 PRD를 "실제 동작 사양"으로 못박기
  /kkirikkiri        → 에이전트 팀이 코드 생성  ┐ 생성되는 동안
       (동시에)       → YouTube·Gemini 키 발급    ┘ 키 받기 (Supabase는 MCP 자동)

[Phase 2 — 연결·운영]  ※ 클로드코드와 한 STEP씩
  Supabase 연결 → Edge Function 배포 → 수집·검증(디버깅) → Vercel 배포 + 매시간 cron
```

> ⚠️ **kkirikkiri는 "한 방 완성 버튼"이 아니다.** 코드 생성은 잘하지만 Supabase 연결·배포·키 연결·체인
> 검증은 Phase 2에서 클로드코드와 직접 한다. 만든 걸 굴리며 고치는 그 단계가 바이브코딩의 본체다.

---

## 문서 구성 (이 폴더)

```
00-사전준비.md       ← YouTube·Gemini 키 발급 + Supabase MCP 연결 (Phase 1과 병렬로)
01-PRD.md            ← show-me-the-prd가 뽑을 PRD의 시드/정답 레퍼런스
02-데이터모델.md      ← DB 테이블 7 + video_details 뷰 + 지표 공식 (구체화·검증용 사양)
03-기술스택과규칙.md  ← DO/DON'T + 환경변수 + API 쿼터 (kkirikkiri 가드레일)
BUILD-PROCESS.md ★   ← 실제 소스 분석 기반 빌드 프로세스·체인·공식 (구체화의 핵심 사양)
04-빌드가이드.md ★    ← 2단 워크플로우 STEP (show-me-the-prd → kkirikkiri → 연결·배포), 핵심
05-배포와자동화.md    ← Vercel 배포 + 매시간 자동 수집(cron) + 보안
06-트러블슈팅.md      ← 막힐 때 증상별 해결 / 테스트 채널
assets/schema.sql    ← Supabase에 적용하는 전체 스키마 (실제 코드와 일치)
```

**시작:** `00`으로 키 발급을 걸어두고 → `04`를 펴서 Phase 1 STEP 1부터.
`02`·`03`·`BUILD-PROCESS`는 STEP 2(구체화)·Phase 2(검증)에서 사양으로 쓴다.

> ℹ️ **레퍼런스 소스는 막판 참조용이다.** Phase 2에서 특정 부분이 도저히 안 풀릴 때만, 그 한 파일을 열어
> 내 코드와 대조한다(STEP 9). 처음부터 소스를 열면 바이브코딩이 아니라 베끼기가 된다.

---

## 완성 기준 (이게 되면 끝)

- [ ] 유튜브 채널 5개 이상 등록 → 매시간 자동 수집이 동작
- [ ] Outliers 페이지에서 "채널 평균 2x 이상 터진 영상"이 정렬·필터됨
- [ ] 영상마다 AI 요약 + 키워드 태그가 보임
- [ ] Trends에서 이번 주 뜨는 키워드 랭킹이 보임
- [ ] Vercel 공개 URL로 다른 기기에서 접속 가능
- [ ] 내가 안 켜도 매시간 데이터가 갱신됨
