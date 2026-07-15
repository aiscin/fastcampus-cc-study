# Clip 07 — 트렌드 대시보드 만들기: 터진 영상을 잡아내는 화면으로 (실습 38) ★

> Part 07 / CH 03 바이브코딩 / Clip 07 (실습 38) | 예상 시간: ~35분
> 결과물: 로컬에서 도는 **Outlier 분석 대시보드**(`trendboard/` — 7페이지 + Edge Function + 수집 데이터 + AI 요약)
> 패턴: **자동 셋업 → 브리핑 → 생성·연결·수집·검증 → WRAP**
> 페르소나 메모 — A(마케터): "2배 터진 영상" 한눈에 / B(PO): 수집→지표 계산→테이블 / C(영업): 채널별 성과 비교
> 사양 정본(스킬 내장): `references/trendboard-standards/` (04 STEP 3~7, BUILD-PROCESS) → clip-06 자동 셋업이 `trendboard/_spec/`에 복사해둠

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

WORK_DIR="$ROOT/50-my-work/Part07-실전/실습38-대시보드"
mkdir -p "$WORK_DIR"

TB="$ROOT/trendboard"
mkdir -p "$TB"

# 강사 결과 화면(녹화/캡처) 위치 안내 — 막힐 때 "이렇게 나온다"만 보여주기용.
# ※ 공유 DB가 아니다. 각 수강생은 자기 Supabase·자기 키로 연동하고, 데이터도 자기 DB에 쌓는다.
SHOTS="$ROOT/.claude/skills/part07-realworld/seed-trendboard/preview-shots"
[ -d "$SHOTS" ] && echo "✓ 강사 결과 화면 있음: $SHOTS (막히면 결과 먼저 공개)" || echo "  (강사 결과 화면 없음 — 준비 선택)"

echo "✓ $WORK_DIR 진도 폴더 준비 완료"
echo "✓ trendboard/ 작업 폴더 — 여기서 kkirikkiri가 코드 생성 → 내 Supabase에 연결"
```

> ⚠ **강사 사전 준비(1회)**: ① 채널 등록→수집→Outlier 표시까지 1회 완주 ② Gemini 요약 1회 실측 ③ 강사 자기 환경 결과 화면 캡처/녹화(`seed-trendboard/preview-shots/`) — 라이브가 막혀도 결과부터 보여주기. **(강사 DB를 공유하는 게 아니라, 각 수강생은 자기 Supabase에 연동)**

셋업 결과를 한 줄로 보고한 뒤, 아래 **브리핑 + 진행 안내**를 한 메시지로 출력하고 SLEEP.

---

## 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 오늘 하는 것

| 항목 | 내용 |
|---|---|
| 무엇 | clip-06에서 깐 DB 뼈대에 **kkirikkiri로 코드 생성** + **클로드코드로 연결·수집** |
| 끝 그림 | "이건 채널 평균 2.2배 터졌다"가 숫자로 뜨는 Outlier 대시보드가 로컬에서 돈다 |
| clip-06과 관계 | 06에서 만든 PRD 사양서 + 스키마 위에 코드를 얹는 날 |

### kkirikkiri는 "한 방 완성 버튼"이 아니다 (핵심)

| | kkirikkiri (생성) | 클로드코드 (연결·운영) |
|---|---|---|
| 하는 일 | 프론트 7페이지 + Edge Function 코드 생성 | Supabase 연결·배포·수집·디버깅 |
| 한계 | 인프라 연결·키·체인 검증은 못 함 | 만든 걸 굴리며 고침 |

> 코드 생성은 kkirikkiri, **굴리는 건 우리.** 한 방에 완벽히 안 나와도 정상 — 연결하며 고치는 그 단계가 바이브코딩의 본체다.

### 오늘 도는 흐름 — 생성 → 연결 → 검증

| 단계 | 하는 일 |
|---|---|
| 생성 | /kkirikkiri로 코드 통째 생성 |
| 연결 | Supabase 연결 + Edge Function 배포 + Gemini 키 |
| 수집·검증 | 채널 등록 → collect-data → Outlier 대시보드 → AI 요약 |

### 라이브 + 강사 화면 (둘을 섞음)

| | 내용 |
|---|---|
| **라이브** | kkirikkiri 생성 → **내 Supabase 연결** → 수집을 따라치기 (각자 자기 것) |
| **강사 화면** | 막히면 강사가 자기 환경에서 돌린 결과 화면(녹화)으로 "이렇게 나온다"만 |

> ⚠ 각 수강생은 **자기 Supabase·자기 키**로 연동한다 — 강사 DB 공유 X. 개인 대시보드라 데이터도 각자 자기 DB에 쌓인다.
> 라이브 수집이 시간 걸리거나 막히면 강사 화면으로 결과만 보여주고, 수집은 백그라운드로 두고 진행.

### 핵심 메시지

> **막히면 로그 기반.** Score 0(avg_views 아직 0), 키워드 안 뜸(Gemini 키 미저장), 403(API 미활성).
> 에러 로그를 그대로 붙여넣고 "고쳐줘" — 추측 말고 로그로. 이게 바이브코딩 디버깅이다.

---

## 진행 안내

```
✓ trendboard/ 작업 폴더 + 50-my-work 진도 폴더 준비

오늘 할 거 (~35분)
- /kkirikkiri로 코드 생성 → 클로드코드로 연결·수집 → 터진 영상 잡아내기
- Score 정렬·Ch.Avg 배율로 Outlier 확인 / Gemini로 영상 요약
- 막히면 로그 보고 고치기 (바이브코딩 디버깅)
- 영상 보면서 진행, 끝나면 `완료` 또는 `/wrap`

6단계 흐름:
1. /kkirikkiri — 코드 생성 (프론트 7 + Edge Function 6)
2. Supabase 연결 — MCP 프로젝트 + .env.local + 스키마 확인
3. Edge Function 배포 + Gemini 키(Admin)
4. 채널 등록 → collect-data 수집 (디버깅)
5. Outlier 대시보드 검증 (지표 공식)
6. Gemini 요약 + 말로 개선
```

---

## 절차 — 생성·연결·수집·검증 (영상 보면서 진행)

### Phase 1. `/kkirikkiri`로 코드 생성 (7분)

한 줄씩 시키는 게 아니라 에이전트 팀에 통째로 맡긴다. clip-06 통합 사양서를 받아 화면·함수를 나눠 만든다.

**복사용 입력:**
```
/kkirikkiri clip-06에서 정리한 통합 사양서대로 TrendBoard를 구현해줘. Vite+React+TS+shadcn 다크 7페이지, Edge Function 6종, schema.sql 마이그레이션. 03의 DO/DON'T 지켜.
```

| 확인 | 7페이지 + 사이드바 골격 / Edge Function 6종 코드 생성 (불완전해도 정상 — 다음 Phase에서 연결) |

### Phase 2. Supabase 연결 (5분)

**복사용 입력:**
```
사양대로 Supabase 연결하자. 프로젝트 없으면 MCP로 만들고, URL·anon 키를 .env.local에 넣어줘(.gitignore 추가). 클라이언트 확인하고, clip-06에서 적용한 schema.sql 스키마가 video_details 뷰까지 맞는지 확인해줘.
```

| 확인 | `.env.local` gitignore 포함(공개 가능한 anon만) / video_details 뷰 select 에러 없음 |

### Phase 3. Edge Function 배포 + Gemini 키 (5분)

**복사용 입력:**
```
Edge Function 6종을 MCP로 배포해줘. SUPABASE_URL·SERVICE_ROLE_KEY는 자동 주입이라 설정 불필요 — YOUTUBE_API_KEY만 Secret으로 넣는 법(대시보드/CLI) 알려줘. 앱 띄워서 Admin 로그인(기본 trendboard2026, 바로 변경)하고 Gemini 키 저장하자.
```

> ⚠ 여기 한 곳만 수동: `YOUTUBE_API_KEY` Secret 등록은 MCP로 안 됨(대시보드 Edge Functions → Secrets / `supabase secrets set`).

| 확인 | 함수 6종 배포(MCP) / YOUTUBE_API_KEY Secret 등록 / Admin 로그인 → Gemini 키 저장 / anon으로 gemini_api_key 안 보임(RLS) |

### Phase 4. 채널 등록 → 수집 (디버깅 핵심) ★ (7분)

**복사용 입력:**
```
테스트 채널 5개 등록하고 collect-data를 수동 실행해줘. videos·video_snapshots 채워지고 avg_views>0, generate-tags 체인으로 content_summaries에 키워드 생기는지 확인. 안 되면 Edge Function 로그 보고 고쳐줘.
```

| 확인 | videos/snapshots 채워짐 / avg_views>0 / content_summaries에 키워드 / Shorts·Long 구분 |

> 라이브 수집이 느리거나 막히면 강사 결과 화면 공개 — "이렇게 데이터가 차면 다음 화면이 이렇게 됩니다." (수집은 내 Supabase에 백그라운드로)

### Phase 5. Outlier 대시보드 검증 (5분)

**복사용 입력:**
```
Outliers 페이지에서 Score 정렬·Ch.Avg 배율·필터가 맞는지 확인해줘. outlierScore가 (views/avg)*10+vsRatio인지(단순 배율×10 아님), Tier 랭킹, content_tags 컬러 배지까지.
```

| 확인 | Score 내림차순 정렬 / Ch.Avg 배율 초록 / Format 필터 / Tier "#1 of N" |

### Phase 6. Gemini 요약 + 말로 개선 (3분)

**복사용 입력:**
```
generate-tags로 요약 없는 영상에 한 줄 요약·키워드·태그를 생성해서 테이블에 컬러 배지로 보여줘. (개선) Mega Outlier(5x↑)는 빨간 배지, 썸네일 더 크게.
```

| 확인 | content_summaries에 요약/키워드 / 테이블에 컬러 배지 / 말로 시킨 UI 개선 반영 |

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| kkirikkiri 결과 불완전 | "정상이에요. 연결하면서 클로드코드로 고쳐요. 한 방 기대 X" |
| Score 전부 0 | "avg_views가 아직 0. collect-data 1~2회 더 돌면 채워져요(신규 채널 정상)" |
| 키워드 배지 안 뜸 | "Admin에 Gemini 키 저장했는지 → generate-tags 호출 (summarize-videos 아님)" |
| YouTube 403 | "YouTube Data API v3 활성·쿼터 확인. search.list 쓰면 안 돼요" |
| 라이브가 너무 느림 | "강사 결과 화면으로 먼저 보여주고, 내 수집은 백그라운드로 두고 진행" |

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
[ -d "$TB/src/pages" ] && echo "프론트 페이지 ✓" || echo "프론트 없음 ✗"
[ -d "$TB/supabase/functions" ] && echo "Edge Function ✓" || echo "함수 없음 ✗"
echo "→ Outliers 페이지에서 Score 정렬 + 키워드 배지 직접 확인"
```

Outlier 테이블이 안 뜨면 어느 Phase에서 멈췄는지 안내 후 재시도 권유.

### 2. README.md 자동 작성

`50-my-work/Part07-실전/실습38-대시보드/README.md`:

```markdown
# 실습 38 — 트렌드 대시보드 만들기 (Outlier 분석)

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 앱 경로: ~/fastcampus-cc/trendboard/

## 오늘 한 것
1. /kkirikkiri — 코드 생성 (7페이지 + Edge Function 6)
2. Supabase 연결 + Edge Function 배포 + Gemini 키
3. 채널 등록 → collect-data 수집
4. Outlier 대시보드 검증 (Score·Ch.Avg 배율)
5. Gemini 요약 + 키워드 배지

## 생성 vs 연결
- kkirikkiri = 코드 생성 / 클로드코드 = 연결·수집·디버깅
- 한 방에 안 나옴 → 로그 기반으로 고침

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 38"],
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

### 4. 회고 한 줄

> "kkirikkiri 생성과 클로드코드 연결, 역할 차이를 한 줄로 적어주세요."

자유 입력으로 받아 README의 "핵심 발견 / 회고"에 기록.

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 브리핑+진행 안내를 한 메시지로 출력하고 영상 따라 진행
- **실습 진행 방식**: 강사 1줄 입력 → 학생 1줄 입력 → 결과 같이 확인. STOP 분리 X (따라치기)
- **"~해줘" 금지 / "~하려는데 어떻게?" 강제** (memory: feedback_ask_how_pattern) — 단 `/kkirikkiri` 등 스킬 호출·복사용 입력은 실제 동작 프롬프트라 명령형 허용
- **각 수강생은 자기 Supabase·자기 키로 연동** — 강사 DB 공유 X. 각자 자기 것을 만드는 개인 대시보드
- **kkirikkiri는 생성까지, 연결은 클로드코드** — "한 방 완성" 포장 금지
- **막히면 로그 기반 디버깅** — 에러 로그 그대로 붙여넣고 고치기
- **느린 수집은 강사 결과 화면으로** — 라이브가 막히면 결과부터 보여주고 내 수집은 백그라운드
- **자유 진행 중 개입 X**: 명시적 도움 요청(`막혔어요`/`도와줘`)에만 응답
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **IDE는 안티그래비티**: VS Code 언급 X
- **search.list 금지·목업 금지·service_role 노출 금지**
