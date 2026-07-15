# Clip 08 — 트렌드 대시보드 배포하기: 매시간 알아서 도는 서비스로 (실습 39) ★

> Part 07 / CH 03 바이브코딩 / Clip 08 (실습 39) | 예상 시간: ~35분
> 결과물: 배포 URL(Vercel) + 매시간 자동 수집(pg_cron) + 트렌드 화면 + 개선
> 패턴: **자동 셋업 → 브리핑 → 트렌드·배포·cron·개선 → WRAP**
> 페르소나 메모 — A(마케터): 공개 URL "내 분석 도구가 인터넷에" / B(PO): pg_cron 매시간 수집 운영 / C(영업): "매시간 알아서 쌓이는" 데이터 자산
> 사양 정본(스킬 내장): `references/trendboard-standards/05-배포와자동화.md` (04 STEP 8~9) → `trendboard/_spec/`에 복사돼 있음

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

WORK_DIR="$ROOT/50-my-work/Part07-실전/실습39-배포자동화"
mkdir -p "$WORK_DIR"

TB="$ROOT/trendboard"
[ -d "$TB/src" ] && echo "✓ clip-07 대시보드 발견: $TB" || echo "⚠ trendboard/ 코드 없음 — clip-07 먼저 필요"

echo "✓ $WORK_DIR 진도 폴더 준비 완료"
echo "  Vercel·GitHub 로그인 필요. 자동화는 Supabase pg_cron(매시간)"
```

> ⚠ **강사 사전 준비(1회)**: ① 미리 배포해둔 데모 URL ② pg_cron 1회 실행 로그 ③ 외부 cron(cron-job.org) 대체안 ④ Edge Function 배포·Secrets 1회 실측.

셋업 결과를 한 줄로 보고한 뒤, 아래 **브리핑 + 진행 안내**를 한 메시지로 출력하고 SLEEP.

---

## 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 오늘 하는 것

| 항목 | 내용 |
|---|---|
| 무엇 | 로컬 분석 대시보드를 **공개 URL + 매시간 자동 수집 서비스로** |
| 끝 그림 | 내 분석 도구가 인터넷에 있고, 안 켜도 매시간 데이터가 쌓인다 |
| clip-07과 관계 | 07에서 만든 로컬 대시보드를 배포·운영으로 끌어올리는 날 |

### 단순 갱신이 아니라 "시계열 운영"

| | 단순 재배포 | **TrendBoard 운영** |
|---|---|---|
| 무엇이 도나 | 정적 페이지 다시 올림 | **매시간 조회수 찍어 시계열 누적** |
| 효과 | 최신 내용 | **데이터 쌓일수록 Outlier 정확** |
| 자동화 위치 | 내 컴퓨터 | **Supabase pg_cron (클라우드, 안 켜도 됨)** |

> 백엔드가 있는 원본이라 **서버 cron이 정답.** collect-data 하나만 매시간 부르면 generate-tags·extract-trends까지 체인으로 돈다.

### 오늘 도는 흐름

| 단계 | 하는 일 |
|---|---|
| 트렌드 마무리 | extract-trends + 키워드 랭킹·바 차트 |
| 배포 | GitHub + Vercel 공개 URL |
| 자동화 | Edge Function 배포 + 매시간 pg_cron |
| 개선 | 쓰면서 말로 (배지·필터) |

### 핵심 메시지

> 프론트엔 anon 키만, **비밀 키(service_role·YouTube·Gemini)는 백엔드에.**
> cron 하나로 "한 번 만든 앱"이 "매시간 도는 분석 서비스"가 된다 — 세 번째 프로젝트의 완성.

---

## 진행 안내

```
✓ 50-my-work/Part07-실전/실습39-배포자동화/ 진도 폴더 준비

오늘 할 거 (~35분)
- Trends 화면 마무리 → Vercel 배포 → 매시간 자동 수집(pg_cron) → 개선
- 공개 URL로 어디서든 접속 / 안 켜도 매시간 데이터 갱신
- 영상 보면서 진행, 끝나면 `완료` 또는 `/wrap`

4단계 흐름:
1. Trends/Overview 마무리 (extract-trends)
2. GitHub + Vercel 배포 (공개 URL)
3. Edge Function 배포 + 매시간 pg_cron
4. 말로 기능 개선
```

---

## 절차 — 트렌드·배포·cron·개선 (영상 보면서 진행)

### Phase 1. Trends/Overview 마무리 (6분)

배포 전 화면 하나만 더 — 키워드 트렌드. video_details에서 실시간 집계한다(trend_topics 테이블 아님).

**복사용 입력:**
```
Trends 페이지랑 extract-trends 만들어줘. video_details에서 keywords 실시간 집계(24h/3D/7D/30D), 바 차트 + 랭킹. Overview도 카드·차트·최근 Outlier로 마무리.
```

| 확인 | 키워드 랭킹+성장률 색상 / 기간 탭 / 바 차트 / Overview 카드·차트 |

### Phase 2. GitHub + Vercel 배포 (7분)

**복사용 입력:**
```
이 프로젝트를 GitHub에 올리고 Vercel로 배포해줘. .env.local·node_modules가 .gitignore에 있는지 먼저 확인하고, Vercel 환경변수에 VITE_SUPABASE_URL·VITE_SUPABASE_PUBLISHABLE_KEY 넣는 법도 알려줘.
```

> ⚠ **Vercel엔 공개 가능한 `VITE_` 2개만**(URL·anon). 비밀 키(YouTube·service_role·Gemini)는 절대 Vercel/프론트 금지 — 그건 Phase 3에서 Supabase 백엔드 쪽에 넣는다. (Vercel 프론트 변수는 브라우저로 그대로 노출됨)

| 확인 | 공개 URL 발급 / 다른 기기에서 접속 / 프론트에 비밀 키 없음 |

### Phase 3. Edge Function 배포 + 매시간 pg_cron ★ (10분)

백엔드 함수 배포 + 매시간 자동 수집. 여기가 핵심.

**복사용 입력 (배포):**
```
Edge Function들(fetch-channel, collect-data, generate-tags, extract-trends, generate-strategy, manage-settings, verify-admin)을 MCP로 배포하고, YOUTUBE_API_KEY만 Secret으로 설정하는 법 알려줘(SUPABASE_URL·SERVICE_ROLE_KEY는 자동 주입이라 제외).
```

**복사용 입력 (cron):**
```
매시간 정각에 collect-data를 부르는 Supabase pg_cron 등록 SQL 만들어줘. 안 되면 cron-job.org로 외부 cron 거는 법도 알려줘.
```

| 확인 | 함수 배포 / pg_cron 등록 / 다음 정시에 데이터 갱신(체인 자동) |

### Phase 4. 말로 기능 개선 (6분)

며칠 쓰면 아쉬운 게 보인다 — 말로 고친다.

**복사용 입력:**
```
24시간 급상승 영상에 🔥 배지, 채널 카테고리 필터, Overview에 '이번 주 가장 터진 영상 3개'를 크게 보여줘.
```

| 확인 | 급상승 배지 / 카테고리 필터 / Top3 강조 — 운영하며 개선 |

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| Vercel 배포 막힘 | "Part 03 배포 복습. 클로드코드가 단계별로 안내" |
| 배포했는데 데이터 안 보임 | "Vercel에 VITE_SUPABASE_URL·PUBLISHABLE_KEY 등록 후 재배포" |
| pg_cron 안 됨 | "pg_net 확장 활성화, 안 되면 cron-job.org 외부 cron으로 동일 효과" |
| service_role 키 걱정 | "프론트·깃 절대 금지. Edge Function Secrets에만" |
| Supabase 일시중지 | "7일 무요청 때문. 매시간 cron이 돌면 자동 방지" |

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
[ -f "$TB/vercel.json" ] && echo "Vercel 설정 ✓" || echo "  (vercel.json 확인)"
echo "→ 공개 URL 접속 + 다음 정시 자동 갱신 직접 확인"
echo "→ pg_cron(또는 외부 cron) 등록 확인"
```

배포 URL이나 cron이 빠졌으면 해당 Phase 재시도 권유.

### 2. README.md 자동 작성

`50-my-work/Part07-실전/실습39-배포자동화/README.md`:

```markdown
# 실습 39 — 트렌드 대시보드 배포 (매시간 자동 수집)

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 공개 URL: {입력}

## 오늘 한 것
1. Trends/Overview 마무리 (extract-trends)
2. GitHub + Vercel 배포 → 공개 URL
3. Edge Function 배포 + 매시간 pg_cron
4. 말로 기능 개선

## 운영 구조
- cron이 collect-data 1콜 → generate-tags·extract-trends 체인 자동
- 안 켜도 매시간 시계열 누적 → Outlier 정확해짐
- 비밀 키는 백엔드, 프론트엔 anon만

## 세 프로젝트 완성
- 워크스페이스 → LLM Wiki → 트렌드 대시보드

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 39"],
  "projects_completed": [..., "trendboard"],
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

### 4. 회고 한 줄

> "일회성 앱을 매시간 도는 분석 서비스로 만든 핵심, 한 줄로 적어주세요."

자유 입력으로 받아 README의 "핵심 발견 / 회고"에 기록.

다음 안내 — "Part 8 — 성장 리포트 + AI Native 여정. 세 프로젝트를 다 만든 지금의 나를 점검."

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 브리핑+진행 안내를 한 메시지로 출력하고 영상 따라 진행
- **실습 진행 방식**: 강사 1줄 입력 → 학생 1줄 입력 → 결과 같이 확인. STOP 분리 X (따라치기)
- **"~해줘" 금지 / "~하려는데 어떻게?" 강제** (memory: feedback_ask_how_pattern) — 단 복사용 입력은 실제 동작 프롬프트라 명령형 허용
- **자동화는 백엔드 pg_cron** — "내 컴퓨터 cron"이 아니라 서버 cron(원본은 백엔드가 있음)
- **비밀 키는 백엔드만** — service_role·YouTube·Gemini는 프론트·깃 노출 금지
- **자유 진행 중 개입 X**: 명시적 도움 요청(`막혔어요`/`도와줘`)에만 응답
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **IDE는 안티그래비티**: VS Code 언급 X
- **세 프로젝트 완성 마무리**: Part 8 성장 리포트로 이어짐
