# Clip 03 — kkirikkiri (자연어로 AI 팀 구성하기)

> Part 04 / Ch 01 / Clip 03 (실습 16) | 예상 시간: ~18분
> 결과물: Agent Teams 개념 정리 + 본인 직무 다관점 진단 리포트 + 1-2순위 정리
> 패턴: **BUILD 없음 — 도움 받기 시연** (Part 04 전체 공통)

---

## 자동 셋업

```bash
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

WORK_DIR="$ROOT/50-my-work/Part04-강화하기/실습16-AI팀구성"
mkdir -p "$WORK_DIR"

echo "✓ $WORK_DIR 준비 완료"
echo "  kkirikkiri가 만들 리포트는 .kkirikkiri/ 디렉토리에 자동 저장됩니다."
echo "  WRAP 단계에서 이 폴더로 핵심 결과물 복사됩니다."
```

셋업 결과 한 줄 보고 후 아래 **kkirikkiri 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## kkirikkiri 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 한 줄 | Agent Teams 기능을 자연어 한 문장으로 쉽게 쓰게 만든 스킬 |
| 강점 | 다관점 동시 분석 (한 사람이 못 보는 영역까지) |
| 호출 | `/kkirikkiri [원하는 것 한 문장]` |
| 산출물 | 마크다운 리포트 (각 페르소나 의견 + 종합 우선순위) |

### Agent Teams vs kkirikkiri

| 구분 | Agent Teams 직접 | kkirikkiri |
|---|---|---|
| 호출 | 자연어 요청 매번 직접 작성 | `/kkirikkiri 한 문장` |
| 팀 구성 | 직접 페르소나·역할 정의 | 인터뷰 2-3개 → 자동 |
| 환경 스캔 | 수동 | 자동 (Codex·Gemini CLI·기존 에이전트 감지) |
| 검증 | 직접 점검 | 검증 루프 자동 (최대 3라운드 재시도) |
| 메모리 | 직접 관리 | `.kkirikkiri/` 자동 생성·관리 |

### 동작 흐름

```
[자연어 한 문장]
   ↓
1. 인터뷰 2-3개 (목적·작업 유형·깊이)
   ↓
2. 팀 자동 구성 (전문가 페르소나 3-5명)
   ↓
3. 병렬 실행 — 4명이 동시에 작업
   ↓
4. 팀장 결과 통합 → 마크다운 리포트
```

### 사전 조건 — Agent Teams 환경변수 활성화

`~/.claude/settings.json`에 추가:

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

저장 후 클로드코드 **재시작 필수**. (kkirikkiri의 환경 점검 스크립트가 자동 안내)

### 핵심 메시지

> Agent Teams는 클로드코드 자체 기능. kkirikkiri는 그걸 스킬로 쉽게 쓰게 만든 것.
> Part 06에서 본인이 만들 스킬도 같은 형태.

---

## 진행 안내

```
✓ 50-my-work/Part04-강화하기/실습16-AI팀구성/ 준비 완료

오늘 할 거 (~18분)
- docs-guide로 클로드코드의 Agent Teams 기능 먼저 알아보기
- kkirikkiri가 Agent Teams를 어떻게 쉽게 쓰게 해주는지 이해
- Agent Teams 환경변수 활성화 (~/.claude/settings.json)
- /kkirikkiri로 본인 직무 다관점 진단 받기
- 우선순위 1-2개 → 1-2순위 정리
- 영상 보면서 진행하시고 끝나면 `완료` 또는 `/wrap` 입력

5단계 흐름:
1. /docs-guide로 Agent Teams 개념 확인
2. kkirikkiri = Agent Teams를 스킬로 쉽게 (비교 + 스킬 본질)
3. 환경변수 활성화 (settings.json + 재시작)
4. /kkirikkiri 호출 + 본인 직무 입력 → 다관점 진단
5. 우선순위 1-2개 → 1-2순위 정리 정리

강사 시연 시나리오: 코스메틱 브랜드 마케터, 바디 미스트 신제품 SNS 캠페인 기획
여러분은 본인 직무로 바꿔서 같은 흐름으로 진행하시면 됩니다.
```

---

## kkirikkiri 인터뷰 응답 가이드

| 질문 | 답 |
|---|---|
| Q1. 제품/서비스 | 본인 직무·업무 설명 그대로 자유 입력 |
| Q2. 작업 유형 | **"디스커버리"** (병목 발굴 + 방향성) |
| Q3. 깊이 | **"제대로"** (체계적 분석) |

---

## 본인 직무 입력 가이드

본인 일을 자유롭게 입력. 구체적일수록 결과 풍부.

**좋은 예시:**
- "스타트업 코스메틱 마케터, 바디 미스트 신제품 SNS 캠페인 기획 중"
- "B2B 영업 매니저, 분기 신규 고객 발굴 캠페인 준비 중"
- "HR 담당, 신입 온보딩 프로그램 새로 만드는 중"

**약한 예시 (재요청 권장):**
- "마케터" / "직장인" / "사무직" — 너무 추상적

매주 하는 일 5-7개 정도 적기. 너무 적으면 분석 빈약, 너무 많으면 산만.

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| `/kkirikkiri` 인식 안 됨 | "/plugin Installed 탭 확인하고 kkirikkiri 재설치 알려줘" |
| Agent Teams 환경변수 안 잡힘 | "settings.json에 추가하고 클로드코드 재시작해야 하는지 확인" |
| 인터뷰 옵션 헷갈림 | "디스커버리 + 제대로 두 가지만 골라" |
| 팀 구성이 강사 시연과 다름 | 정상 — 본인 입력에 따라 팀 다르게 구성 |
| 병렬 실행 5분+ 소요 | 정상 — 차 한잔 마시며 대기 |
| 리포트 결과 일반론적 | "내 직무·업무 더 구체적으로 다시 설명" 재요청 |
| 우선순위 결정 어려움 | "주 4시간 이상 절감 + 본인 자신감 있는 영역" 기준 |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리

### 1. 결과물 검증 + 복사

```bash
ROOT="$HOME/fastcampus-cc"
WORK_DIR="$ROOT/50-my-work/Part04-강화하기/실습16-AI팀구성"
KKIRI_DIR="$ROOT/.kkirikkiri"

if [ -d "$KKIRI_DIR/reports" ]; then
  cp "$KKIRI_DIR/reports"/*.md "$WORK_DIR/" 2>/dev/null
  echo "✓ kkirikkiri 리포트 복사 완료"
else
  echo "⚠ kkirikkiri 리포트가 없어요. STEP 4 진행 확인."
fi
```

`agent-teams-overview.md` + `discovery-report.md` + `priority-summary.md` 존재 확인.

### 2. README.md 자동 작성

`50-my-work/Part04-강화하기/실습16-AI팀구성/README.md`:

```markdown
# 실습 16 — kkirikkiri로 자연어 AI 팀 구성하기

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 본인 직무: {사용자 입력}

## Agent Teams 개념 (docs-guide로 확인)
- 클로드코드 자체 기능 (experimental)
- 환경변수 활성화 후 자연어로 팀 호출
- Team Lead + 독립 팀원 + 공유 태스크 + 메시지 시스템

## kkirikkiri = Agent Teams를 스킬로 쉽게
| 구분 | Agent Teams 직접 | kkirikkiri |
|---|---|---|
| 호출 | 자연어 매번 직접 작성 | /kkirikkiri 한 문장 |
| 팀 구성 | 직접 정의 | 인터뷰 → 자동 |
| 검증 | 직접 점검 | 검증 루프 자동 |
| 메모리 | 직접 관리 | .kkirikkiri/ 자동 |

## 자동 구성된 팀
- 팀장 (Lead)
- {팀원 1}
- {팀원 2}
- {팀원 3}

## 받은 우선순위 (Part 06에서 만들 스킬 청사진)
1. {1순위 자동화 후보 + 한 줄 동작 설명}
2. {2순위 자동화 후보 + 한 줄 동작 설명}

## 5단계 진행 (BUILD 없음)
- 1 docs-guide로 Agent Teams 개념 확인
- 2 kkirikkiri 본질 + 스킬이 어떻게 동작하는지
- 3 settings.json 환경변수 활성화
- 4 /kkirikkiri 호출 + 본인 직무 입력 → 다관점 진단
- 5 우선순위 1-2개 → 1-2순위 정리

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 16"],
  "current_clip": null,
  "last_activity": "{ISO8601}",
  "priorities_for_part06": [
    {"rank": 1, "skill_name": "{후보}", "description": "{한 줄 동작}"},
    {"rank": 2, "skill_name": "{후보}", "description": "{한 줄 동작}"}
  ]
}
```

`priorities_for_part06`은 Part 06 시작 시 자동으로 참고됨.

### 4. 회고 한 줄

자유 입력으로 받기:

> "이번 클립에서 가장 인상적이었던 진단 한 줄로 적어주세요."

받은 텍스트를 README의 "핵심 발견 / 회고" 섹션에 기록.

### 5. 다음 클립 안내

```
실습 16 완료. Agent Teams 개념 + kkirikkiri = 스킬로 쉽게 + 다관점 진단까지.

받은 우선순위 1-2개는 progress.json에 기록되어,
Part 06(스킬 만들기) 시작할 때 자동으로 참고됩니다.

다음은 Clip 04 — vibe-sunsang으로 본인 사용 패턴 점검 (Part 04 마지막).
시작하려면 /part04 다시 호출하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 번에 출력하고 사용자가 영상 보면서 직접 진행
- **BUILD 없음**: Part 04 전체 공통
- **자유 실습 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **변동성 인정**: 학습자 입력에 따라 팀 구성·결과 다름. 흐름만 일관 유지
- **Part 06 사슬 명시**: WRAP에서 받은 우선순위가 Part 06에서 만들 스킬 청사진임을 안내
- **특정 브랜드명 X**: 강의본문에는 특정 브랜드(탬버린즈 등) 노출 X. 강사 머릿속 참고만
