# Clip 06 — 트렌드 대시보드 설계하기: PRD 쓰고 데이터 기반 깔기 (실습 37)

> Part 07 / CH 03 바이브코딩 / Clip 06 (실습 37) | 예상 시간: ~30분
> 결과물: PRD 4종(`/show-me-the-prd`) + 키 2종(YouTube·Gemini) 발급 + Supabase(MCP 자동) 스키마(테이블 7 + `video_details` 뷰)
> 패턴: **자동 셋업 → 브리핑 → 설계·구체화·키·스키마 → WRAP**
> 페르소나 메모 — A(마케터): "터진 영상 자동 감지" 쓸모 / B(PO): 매시간 수집→Outlier 구조 / C(영업): 업계 채널 성과 모니터링
> 사양 정본(스킬 내장): `references/trendboard-standards/` (00·01·02·03·BUILD-PROCESS + schema.sql). 자동 셋업이 `trendboard/_spec/`에 복사 → 모든 수강생이 **동일 컨텍스트**로 시작

---

## 자동 셋업

스킬 호출 직후 아래 Bash를 즉시 실행 (사용자에게 명령을 보여주는 게 아니라 스킬이 직접).

```bash
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
elif [ -d "$HOME/Desktop/fastcampus-cc" ]; then
  ROOT="$HOME/Desktop/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

WORK_DIR="$ROOT/50-my-work/Part07-실전/실습37-트렌드설계"
mkdir -p "$WORK_DIR"

TB="$ROOT/trendboard"                        # 앱 본체 (clip-07에서 kkirikkiri가 채움)
mkdir -p "$TB/_spec"

# 사양 문서 + 스키마를 작업 폴더에 복사 (구체화·스키마 적용에 사용 — clip-04 시드 패턴)
STD="$ROOT/.claude/skills/part07-realworld/references/trendboard-standards"
if [ -d "$STD" ]; then
  # ① 진도 폴더 밑에 기준집 전체를 trendboard-standards/로 복사 (수강생 포트폴리오 사본)
  cp -R "$STD" "$WORK_DIR/trendboard-standards"
  # ② 앱 작업 폴더 _spec/에 사양 문서 + 스키마를 평면 복사 (구체화·스키마 적용용)
  cp "$STD"/*.md "$TB/_spec/" 2>/dev/null
  cp "$STD/assets/schema.sql" "$TB/_spec/" 2>/dev/null
  echo "✓ 기준집을 $WORK_DIR/trendboard-standards/ 에 복사 ($(ls "$WORK_DIR/trendboard-standards"/*.md 2>/dev/null | wc -l | tr -d ' ')종)"
  echo "✓ 사양 문서 + schema.sql을 trendboard/_spec/에 복사 ($(ls "$TB/_spec"/*.md 2>/dev/null | wc -l | tr -d ' ')종)"
else
  echo "⚠ trendboard-standards 기준집이 없습니다 — 스킬 설치 확인 필요"
fi

echo "✓ $WORK_DIR 진도 폴더 준비 완료"
echo "✓ 앱 작업 폴더 trendboard/ 준비 (코드는 clip-07에서 생성)"
echo "  오늘 결과물: PRD 4종 + 키 2종(YouTube·Gemini) + Supabase(MCP 자동) 스키마"
```

> ⚠ **강사 사전 준비(1회)**: 키 2종(YouTube·Gemini) 발급 + Supabase 커넥터(MCP) 연결을 미리 완주(403·RLS 함정 체크) + schema.sql을 MCP로 1회 적용해 흐름 검증 + 추적 채널 5개 선정. **(수강생도 각자 자기 Supabase 커넥터로 연결·적용)**

셋업 결과를 한 줄로 보고한 뒤, 아래 **브리핑 + 진행 안내**를 한 메시지로 출력하고 SLEEP.

---

## 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 한 줄 | 여러 유튜브 채널 영상 성과를 **매시간 수집**해 "채널 평균 대비 터진 영상(Outlier)"을 숫자로 잡아내는 분석 대시보드 |
| 본질 | 새 영상 모아보기가 아니라 **성과 분석** — "평소보다 몇 배 터졌나"를 자동 감지 |
| 이번 프로젝트 | 세 번째 캡스톤. **원본/풀버전** — 백엔드(Supabase) + API 키 필요 |

### 단순 요약 다이제스트와 뭐가 다른가

| | 단순 다이제스트 | **TrendBoard (원본)** |
|---|---|---|
| 보여주는 것 | 새 영상 요약 | **Outlier Score·Ch.Avg 배율·V/S Ratio·트렌드** |
| 저장 | 파일 한 장 | **Supabase — 매시간 시계열 누적** |
| 필요한 것 | 없음 | **백엔드 + 키 2종(YouTube·Gemini) + Supabase 커넥터(MCP)** |

> "평소를 알아야 터졌다를 안다." 그래서 매시간 조회수를 쌓는 백엔드가 필요하다 (LLM Wiki의 누적 원리와 같은 결).

### 핵심 지표 — Outlier Score

| 지표 | 식 | 뜻 |
|---|---|---|
| Ch.Avg 배율 | `views / 채널평균` | 평균보다 몇 배 (2.2x) |
| V/S Ratio | `views / 구독자 × 100` | 구독자 밖으로 퍼진 정도 |
| **Outlier Score** | `(views/평균)×10 + V/S Ratio` | 정렬 기준 점수 |

### 오늘 어디까지 — 설계 + 셋업

| 단계 | 하는 일 | 어느 클립 |
|---|---|---|
| **PRD·구체화·키·스키마** | 설계도 + 키 발급 + DB 깔기 | **오늘(clip-06) 여기까지** |
| 코드 생성·연결 | kkirikkiri 생성 + 수집·Outlier | clip-07 |
| 배포·자동화 | Vercel + 매시간 cron | clip-08 |

### 핵심 메시지

> 바이브코딩은 PRD부터 — 근데 직접 쓰지 않고 **`/show-me-the-prd`로 만든다.**
> PRD는 사람마다 다르게 나오니, **미리 깔아둔 공통 사양(`_spec/`)으로 구체화**해 모두 같은 출발선에 선다.
> 그래야 다음 클립 kkirikkiri가 누구 환경에서나 제대로 만든다.
> 그리고 솔직히 — 이번엔 **키가 필요하다.** 단 Supabase는 클로드코드가 MCP로 자동 — 손으로 받는 건 **YouTube·Gemini 2종뿐.** 대신 결과물이 진짜 제품급. 키 발급은 이 클립에 몰아서 끝낸다.

### 스킬 콜백

> Part 6에서 만든 스킬처럼, 오늘도 **스킬에 일을 시킨다** — `/show-me-the-prd`가 PRD를, 다음 클립 `/kkirikkiri`가 코드를. 내가 한 줄 타이핑할수록 스킬이 더 한다.

---

## 진행 안내

```
✓ 50-my-work/Part07-실전/실습37-트렌드설계/ 진도 폴더 준비
✓ trendboard/ 앱 폴더 준비 (코드는 다음 클립)

오늘 할 거 (~30분)
- /show-me-the-prd로 PRD 4종 자동 생성 → 실제 사양으로 구체화
- API 키 2종(YouTube·Gemini) 발급 + Supabase는 MCP로 자동 생성
- schema.sql 적용해 DB 기반(테이블 7 + 뷰) 깔기
- 영상 보면서 진행, 끝나면 `완료` 또는 `/wrap`

4단계 흐름:
1. /show-me-the-prd — PRD 4종 (범위 좁히기)
2. 구체화 — PRD에 실제 동작 사양 박기 (kkirikkiri 입력용)
3. 키 발급 — YouTube Data API / Gemini (Supabase는 MCP 자동)
4. schema.sql 적용 — 테이블 7 + video_details 뷰
```

---

## 절차 — 설계·구체화·키·스키마 (영상 보면서 진행)

### Phase 1. `/show-me-the-prd`로 PRD 만들기 (6분)

PRD를 직접 쓰지 않고 스킬에 시킨다. 질문 5~6개에 답하면 PRD 4종(제품·데이터·단계·스펙)이 나온다.

**복사용 입력:**
```
/show-me-the-prd 유튜브 채널들 영상 성과를 매시간 수집해서 '채널 평균 대비 터진 영상(Outlier)'을 자동으로 잡아내고, 트렌드 키워드까지 보여주는 분석 대시보드를 만들고 싶어.
```

이어지는 질문 답(요지): 사용자=채널 추적하는 나 / 기능=채널등록·매시간수집·Outlier·AI요약·트렌드 / 안 만드는 것=로그인·결제·멀티플랫폼.

| 확인 | PRD 4종 생성 / 범위가 Outlier + 트렌드로 좁혀짐(욕심 X). `01-PRD.md`가 정답 레퍼런스 |

### Phase 2. PRD 구체화 — 공통 사양으로 수렴 ★ (6분)

> **왜 이 단계가 핵심인가.** `/show-me-the-prd`는 **사람마다 다른 PRD**를 만든다. 그대로 kkirikkiri에 넣으면
> 누군 되고 누군 안 된다(공식·함수·뷰가 제각각). 그래서 자동 셋업이 미리 깔아둔 **공통 사양(`trendboard/_spec/`)** 으로
> 수렴시켜 **모두가 동일한 컨텍스트**로 빌드를 시작한다. PRD 만드는 경험은 각자, 빌드 사양은 하나로.

`/show-me-the-prd`가 만든 PRD는 잘 만든 **이상형**이지 실제 동작 사양이 아니다. kkirikkiri가 제대로 만들려면 정확한 공식·함수·뷰를 박아야 한다. **강사 노하우 지점.**

**복사용 입력:**
```
방금 만든 PRD에 trendboard/_spec/의 02·03·BUILD-PROCESS 실제 사양을 박아줘 — video_details 뷰(컬럼 video_id·snapshot_at), Outlier Score=(views/avg)*10+vsRatio, AI 태깅은 generate-tags(summarize 아님), 체인은 collect-data→generate-tags→extract-trends. kkirikkiri에 줄 통합 사양서로 정리해줘.
```

| 확인 | outlierScore 공식 `+vsRatio` 포함 / AI 태깅 generate-tags 명시 / 뷰 컬럼명 보존 / 화면 7 + 체인 |

### Phase 3. 키 발급 + Supabase 연결 (10분)

진입장벽 구간. `00-사전준비.md` 보며 천천히 같이. **Supabase는 클로드코드가 MCP로 만든다** — 손으로 받는 건 YouTube·Gemini 2종뿐. **전부 각자 본인 계정·본인 프로젝트로** (강사 것 공유 X — 내 대시보드는 내 DB에).

| # | 어디서 | 받는 것 | 메모 |
|---|---|---|---|
| 1 | **Supabase (MCP)** | "trendboard 프로젝트 만들어줘" → 클로드코드가 생성 | URL·anon 자동 연결 / service_role은 자동 주입 |
| 2 | Google Cloud | **YouTube Data API v3 Enable** → API 키 | `YOUTUBE_API_KEY` (손으로) |
| 3 | Google AI Studio | Get API key | `GEMINI_API_KEY` (손으로) |

> 📌 Supabase 커넥터가 `/mcp`에 없으면 수동 폴백(`00-사전준비.md` §1).

| 확인 | YouTube·Gemini 키 메모 / Supabase 프로젝트 MCP 생성됨 / service_role은 백엔드 전용(자동 주입) 인지 |

### Phase 4. `schema.sql` 적용 (4분)

키를 받았으면 DB 뼈대를 깐다.

**복사용 입력:**
```
trendboard/_spec/schema.sql을 내 Supabase에 MCP 마이그레이션으로 적용해줘. 테이블 7개랑 video_details 뷰가 생겨야 해. 뷰 컬럼명(video_id·snapshot_at)은 바꾸지 마.
```

| 확인 | Table Editor에 7테이블 + `video_details` 뷰 / `select video_id, snapshot_at from video_details` 에러 없음 |

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| 키 발급이 너무 많음 | "이 클립에서 몰아서 끝내면 다신 안 해요. 00-사전준비 순서대로 같이 가요" |
| YouTube API 403 | "Google Cloud에서 YouTube Data API v3를 Enable 했는지 확인해줘" |
| service_role 키 어디 써요 | "지금은 메모만. 백엔드(Edge Function)에만 넣고 프론트·깃엔 절대 금지" |
| 스키마 적용 안 됨 | "Supabase 커넥터(/mcp) 연결 확인. 안 되면 SQL Editor에 schema.sql 직접 붙여넣기" |
| 기능 더 넣고 싶음 | "1차는 Outlier + 트렌드. 알림·멀티플랫폼은 06 문서 '더 나아가기'" |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리

### 1. 결과물 검증

```bash
ROOT="${ROOT:-$HOME/fastcampus-cc}"
TB="$ROOT/trendboard"
[ -d "$TB" ] && echo "trendboard/ 작업 폴더 ✓" || echo "작업 폴더 없음 ✗"
echo "→ Supabase Table Editor에서 7테이블 + video_details 뷰 직접 확인"
echo "→ 키 2종(YouTube·Gemini) 메모 + Supabase MCP 프로젝트 확인"
```

PRD 4종·키·스키마 중 빠진 게 있으면 해당 Phase 재시도 권유.

### 2. README.md 자동 작성

`50-my-work/Part07-실전/실습37-트렌드설계/README.md`:

```markdown
# 실습 37 — 트렌드 대시보드 설계 (PRD·키·스키마)

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 앱 경로: ~/fastcampus-cc/trendboard/ (코드는 clip-07에서 생성)

## 오늘 한 것
1. /show-me-the-prd — PRD 4종 생성
2. 구체화 — 실제 동작 사양 주입(통합 사양서)
3. 키 발급 — YouTube / Gemini (Supabase는 MCP 자동)
4. schema.sql 적용 — 테이블 7 + video_details 뷰

## 추적 채널 (5개)
{입력}

## 핵심 — 왜 백엔드가 필요한가
- 매시간 시계열을 쌓아야 "평소 대비 터졌다(Outlier)"를 안다

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 37"],
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

### 4. 회고 한 줄

> "단순 요약 다이제스트와 이 분석 도구의 차이, 한 줄로 적어주세요."

자유 입력으로 받아 README의 "핵심 발견 / 회고"에 기록.

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 브리핑+진행 안내를 한 메시지로 출력하고 영상 따라 진행
- **실습 진행 방식**: 강사 1줄 입력 → 학생 1줄 입력 → 결과 같이 확인. STOP 분리 X (따라치기)
- **"~해줘" 금지 / "~하려는데 어떻게?" 강제** (memory: feedback_ask_how_pattern) — 단 `/show-me-the-prd` 등 스킬 호출·복사용 입력은 실제 동작 프롬프트라 명령형 허용
- **오늘 범위는 설계+셋업까지** — 코드 생성은 clip-07, 배포는 clip-08
- **키 발급은 몰아서**: YouTube·Gemini 2종을 이 클립에서. Supabase는 MCP 자동. service_role은 비밀(프론트·깃 노출 금지)
- **자유 진행 중 개입 X**: 명시적 도움 요청(`막혔어요`/`도와줘`)에만 응답
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **IDE는 안티그래비티**: VS Code 언급 X
- **search.list 금지·목업 금지**: 실제 YouTube API + Supabase 연동만
