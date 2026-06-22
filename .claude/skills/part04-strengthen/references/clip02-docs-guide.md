# Clip 02 — docs-guide (모르는 도구를 처음 쓰기 전 정확히 이해하기)

> Part 04 / Ch 01 / Clip 02 (실습 15) | 예상 시간: ~18분
> 결과물: docs-guide 답변 2건 + 일반 답변과 비교 표 + 클로드코드 시너지 발견 + 새 도구 학습 적용 정리
> 패턴: **BUILD 없음 — 도움 받기 시연** (Part 04 전체 공통)

---

## 자동 셋업

스킬 호출 직후 아래 Bash를 즉시 실행 (사용자에게 명령 보여주는 게 아니라 스킬이 직접).

```bash
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

WORK_DIR="$ROOT/50-my-work/Part04-강화하기/실습15-공식문서확인"
mkdir -p "$WORK_DIR"

echo "✓ $WORK_DIR 준비 완료"
```

셋업 결과 한 줄 보고 후 아래 **docs-guide 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## docs-guide 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 한 줄 | 공식 문서 fetch 후 답변 생성. 출처 표기. |
| 차이 | 일반 답변(추측, 출처 없음) → docs-guide(공식 문서 grounded, 출처·버전 명시) |
| 호출 | `/docs-guide [라이브러리] [질문]` 또는 자연어로 |
| 지원 | 68+ 라이브러리 (Vercel·Supabase·Next.js·React·Tailwind·FastAPI 등) |

### 동작 흐름

```
[학습자 입력]
   ↓
1. 라이브러리 식별 (지원 목록 매칭)
   ↓
2. 공식 문서 실시간 fetch (llms.txt 인덱스 또는 직접)
   ↓
3. fetch한 내용 기반으로만 답변 생성
   ↓
4. 답변 끝에 source/version/method 표기
```

### 핵심 메시지

> 모르는 도구는 docs-guide로 먼저 이해한 다음에 쓰기.

---

## 진행 안내

```
✓ 50-my-work/Part04-강화하기/실습15-공식문서확인/ 준비 완료

오늘 할 거 (~18분)
- docs-guide: 모르는 도구를 처음 쓰기 전 공식 문서 기반으로 이해
- 시연 주제: Vercel 알아보기 (Part 03 clip-10에서 썼던 도구가 뭐였는지)
- 영상 보면서 진행하시고 끝나면 `완료` 또는 `/wrap` 입력

5단계 흐름:
1. 일반 답변 받기 (Vercel 자체) → vercel-overview-plain.md
2. /docs-guide vercel — Vercel 정의 + 6 카테고리 → vercel-overview-docs.md
3. /docs-guide vercel — 클로드코드 시너지 깊이 → vercel-claude-synergy.md
4. 5관점 비교 → comparison.md
5. 새 도구 학습 습관 정리

핵심 메시지: 모르는 도구는 docs-guide로 먼저 이해한 다음에 쓰기.
            깊이 들어가면 클로드코드와의 시너지까지 발견된다.
```

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| `/docs-guide` 인식 안 됨 | "/plugin Installed 탭 확인하고 docs-guide 재설치 알려줘" |
| docs-guide 답변에 source 없음 | 해당 라이브러리 미지원 — 다른 도구 (Supabase·Tailwind·Next.js 등) |
| Vercel 답변 차이 작음 | "Supabase 알아보기" 또는 본인이 자주 만지는 도구로 변경 |
| STEP 3 agent-resources fetch 실패 | URL 변경 또는 일시 장애 — STEP 3 생략 가능. STEP 4·5만 진행 |
| 답변 너무 김 | "핵심만 5줄로 요약 다시" 재요청 |
| 출처 URL 클릭 안 됨 | 마우스 오른쪽 클릭 → 링크 열기 또는 URL 복사 |
| 본인 다른 도구로 응용 | 본인이 최근에 처음 써본 도구 / 앞으로 쓸 도구 골라 같은 흐름 |
| 다른 도구도 클로드코드 시너지 있나? | docs-guide로 "X에서 클로드코드와의 시너지" 물어보기 |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리

### 1. 결과물 검증

`vercel-overview-plain.md`, `vercel-overview-docs.md`, `vercel-claude-synergy.md`, `comparison.md` 네 파일 존재 확인. 없으면 어떤 게 빠졌는지 안내.

### 2. README.md 자동 작성

`50-my-work/Part04-강화하기/실습15-공식문서확인/README.md`:

```markdown
# 실습 15 — docs-guide로 모르는 도구 알아보기 + 클로드코드 시너지 발견

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 시연 주제: {Vercel 알아보기 또는 사용자 변경 주제}

## docs-guide 한 줄 정의 & 동작 흐름

### 한 줄 정의
| 항목 | 내용 |
|---|---|
| 한 줄 | 공식 문서 fetch 후 답변 생성. 출처 표기. |
| 차이 | 일반 답변(추측) → docs-guide(공식 문서 grounded) |
| 깊이 | 단순 사용법 → 클로드코드 시너지까지 발견 가능 |
| 호출 | /docs-guide [라이브러리] [질문] |
| 지원 | 68+ 라이브러리 |

### 동작 흐름
1. 라이브러리 식별 (지원 목록 매칭)
2. 공식 문서 실시간 fetch (llms.txt 인덱스 또는 직접)
3. fetch한 내용 기반으로만 답변 생성
4. 답변 끝에 source/version/method 표기

## 결과물
- vercel-overview-plain.md — 일반 클로드코드 답변
- vercel-overview-docs.md — docs-guide 답변 (정의 + 6 카테고리)
- vercel-claude-synergy.md — docs-guide 추가 답변 (클로드코드 시너지 5가지)
- comparison.md — 5관점 비교 표

## 5관점 비교
| 관점 | plain | docs-guide |
|------|-------|------------|
| 정의 정확성 | △ | ✓ |
| 기능 범위 | △ | ✓ |
| 출처 명시 | ❌ | ✓ |
| 버전 명시 | ❌ | ✓ |
| 추측 흔적 | △ | ✓ |

## 클로드코드 ↔ Vercel 시너지 (STEP 3에서 발견)
1. llms-full.txt — 공식 가이드에 "Claude Code: Use the WebFetch tool" 명시
2. Vercel MCP 서버 — 클로드코드가 Vercel 계정 직접 접속 (배포 로그·도메인 등)
3. AI Gateway — 모델 라우팅 (Claude Code·OpenAI Codex 명시 지원)
4. Skills.sh — 18+ AI 에이전트 지원 (Claude Code 포함)
5. CLI Workflows — 클로드코드용 검증된 작업 레시피

## 5단계 진행 (BUILD 없음)
- 1 일반 답변: Vercel 자체 묻기 → vercel-overview-plain.md
- 2 docs-guide 답변: Vercel 정의 + 6 카테고리 → vercel-overview-docs.md
- 3 docs-guide 깊이: 클로드코드 시너지 → vercel-claude-synergy.md
- 4 5관점 비교: comparison.md
- 5 적용 정리: 새 도구 학습 습관 + 시너지 검증

## 새 도구 학습 습관 (반복 적용 가이드)
- 처음 쓰는 도구·라이브러리 호출 직전 → docs-guide로 먼저 이해
- 바이브코딩 중 클로드코드가 새 라이브러리 import 했을 때 → 정확히 확인
- 라이브러리 버전 업그레이드 후 동작 안 할 때 → 최신 문법 확인
- 기능·옵션·메서드 시그니처 정확히 알아야 할 때
- ★ 도구 선택 단계 — 클로드코드 시너지 확인 (agent-resources / MCP / llms.txt)

## 공식 문서 출처
- {docs-guide 답변에서 받은 source URL}
- {agent-resources URL}

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 15"],
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

### 4. 회고 한 줄

자유 입력으로 받기:

> "가장 인상적이었던 차이 또는 시너지 한 줄로 적어주세요."

받은 텍스트를 README의 "핵심 발견 / 회고" 섹션에 기록.

### 5. 다음 클립 안내

```
실습 15 완료. 모르는 도구를 docs-guide로 정확히 이해하는 흐름을 체험했고,
깊이 들어가서 클로드코드 시너지까지 발견했습니다.

핵심 메시지: 앞으로 만날 모든 새 도구(Supabase·OpenAI SDK 등)에
같은 흐름 — "쓰기 전에 docs-guide로 먼저 이해 + 시너지 검증" — 를 적용하시면 됩니다.

다음은 Clip 03 — kkirikkiri로 본인 일에 AI 어떻게 쓸지 다관점 진단.
시작하려면 /part04 다시 호출하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 번에 출력하고 사용자가 영상 보면서 직접 진행
- **BUILD 없음**: Part 04 전체 공통 — 도움 받기 체험이라 5단계 적용 X
- **자유 실습 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **반복 적용 메시지 강조**: 시연 주제(Vercel)는 예시. 핵심은 "새 도구 학습 습관 + 시너지 검증"
- **STEP 3 fallback**: agent-resources fetch 실패해도 STEP 4·5만 진행 가능 (시간 단축)
