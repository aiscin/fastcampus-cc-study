# Clip 02 — 커맨드 & 서브에이전트 (스킬의 재료들 알아보기)

> Part 05 / Ch 01 / Clip 02 (실습 19) | 예상 시간: ~20분
> 결과물: `/study-progress` 커맨드 + `practice-coach` 서브에이전트 + agent-agency 패턴 분석 + 진도 보고서 + 평가 리포트
> 패턴: **실습** — 강사 1줄 입력 → 학생 같은 줄 입력 → 결과 같이 확인

---

## 자동 셋업

스킬 호출 직후 아래 Bash를 즉시 실행 (사용자에게 명령 보여주는 게 아니라 스킬이 직접).

```bash
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

# 50-my-work 메타 폴더 준비
WORK_DIR="$ROOT/50-my-work/Part05-뜯어보기/실습19-커맨드서브에이전트"
mkdir -p "$WORK_DIR"

# 강의 워크스페이스의 .claude 하위 폴더 보장
mkdir -p "$STUDY_DIR/.claude/commands"
mkdir -p "$STUDY_DIR/.claude/agents"

echo "✓ $WORK_DIR 준비 완료"
echo "✓ ~/fastcampus-cc/.claude/{commands,agents}/ 준비 완료"
```

셋업 결과 한 줄 보고 후 아래 **3가지 자산 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## 3가지 자산 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 자산 | 비유 | 한 줄 | 파일 구조 |
|---|---|---|---|
| **슬래시 커맨드** | 매크로 | 자주 치는 긴 프롬프트를 `/이름` 한 줄로 호출 | `.claude/commands/이름.md` (파일 1개) |
| **서브에이전트** | 전문가 | 특정 분야 전담 직원 — 자연어로 자동 위임 | `.claude/agents/이름.md` (파일 1개) |
| **스킬** (Part 06) | 매뉴얼 | 작업 절차서 — 여러 단계 자동화 | `.claude/skills/이름/SKILL.md` (폴더 + 추가 파일) |

### 가족 관계 (구성요소가 아니라 가족)

```
세 자산은 독립적이고 조합 가능:
- 스킬에서 서브에이전트 호출 가능 (context: fork)
- 서브에이전트가 스킬 미리 로드 가능 (skills 필드)
- 커맨드와 스킬은 사실상 통합됨 (둘 다 / 호출)

오늘은 두 개(커맨드 + 서브에이전트), 매뉴얼(스킬)은 Part 06.
```

### 동작 흐름

```
[슬래시 커맨드]
  사용자가 /이름 명시 → frontmatter description + 본문 + $ARGUMENTS 치환 → AI에 전달

[서브에이전트]
  사용자 자연어 입력 → Claude가 description 매칭 → 자동 위임 → 별도 컨텍스트에서 실행 → 요약만 메인에 반환
```

### 핵심 메시지

> 오늘 만든 두 자산은 강의 끝까지 (Part 06/07) 계속 활용된다.
> 강의 끝나도 본인 업무에 평생 응용 가능한 영구 자산.

---

## 진행 안내

```
✓ 50-my-work/Part05-뜯어보기/실습19-커맨드서브에이전트/ 준비 완료
✓ ~/fastcampus-cc/.claude/{commands,agents}/ 준비 완료

오늘 할 거 (~20분)
- 3가지 자산 가족 관계 인지 (커맨드/서브에이전트/스킬)
- 슬래시 커맨드 = 매크로: /study-progress 만들기
- 서브에이전트 = 전문가: agent-agency 레포 분석 → practice-coach 만들기
- 실습으로 진행 (강사 1줄 입력 → 학생 같은 줄 입력 → 결과 같이 확인)
- 진행 끝나면 `완료` 또는 `/wrap` 입력

6단계 흐름 (모두 ~/fastcampus-cc/ 안에서):
1. 강의 워크스페이스 .claude/commands/stuck.md 한 번 뜯어보기 (REFERENCE - 수정 X)
2. /study-progress 만들기 + 호출 (~/fastcampus-cc/.claude/commands/study-progress.md)
3. agent-agency 레포 분석 (engineering-code-reviewer.md 1개 깊이)
4. practice-coach 만들기 + 자동 위임 테스트 (~/fastcampus-cc/.claude/agents/practice-coach.md)
5. 3가지 자산 비교 정리
6. 다음 클립 예고

★ 강의 워크스페이스 (~/fastcampus-cc/) 절대 수정 X
  모든 변경은 ~/fastcampus-cc/ 안에서만
```

---

## 단계별 진행 가이드

### STEP 1. 강의 워크스페이스 커맨드 한 번 뜯어보기 (2분, REFERENCE only)

**[목적]** 표준 슬래시 커맨드가 어떻게 생겼는지 실물 1개 보기. 수정 X.

**[보여줄 파일]** `~/fastcampus-cc/.claude/commands/stuck.md`

**[짚을 것]**
1. frontmatter `description` — Claude가 자동 매칭에 쓰는 키워드
2. 본문 — AI에게 줄 프롬프트 (평소 채팅창 입력과 동일)
3. `$ARGUMENTS` — 사용자 입력 치환 자리
4. 파일명 = 커맨드명 규칙 (`stuck.md` → `/stuck`)

---

### STEP 2. /study-progress 만들기 (4분)

**[목적]** 강의 진도를 자동 정리하는 슬래시 커맨드 만들기. 실습.

**[Claude Code 입력]**

```text
~/fastcampus-cc/.claude/commands/study-progress.md 파일 만들어줘.

목적: 강의 진도를 정리하는 슬래시 커맨드.

동작:
- ~/fastcampus-cc/progress.json을 읽어 완료한 실습 번호와 레벨 확인
- ~/fastcampus-cc/50-my-work/ 폴더를 스캔해서 만든 결과물 목록 정리
- 다음 형식으로 보고서 출력:
  ## 이번 주 진도
  - 완료한 실습:
  - 만든 결과물:
  - 현재 레벨:
  - 다음 추천:

frontmatter:
- description에 "강의 진도 정리" 키워드 포함

본문 끝에 $ARGUMENTS 자리 마련 — 사용자가 추가 메모 입력할 수 있게.
```

**[검증]** 안티그래비티에서 `~/fastcampus-cc/.claude/commands/study-progress.md` 열어 frontmatter + 본문 + `$ARGUMENTS` 확인.

**[호출 테스트]** 클로드코드 재시작 후 `/study-progress` 입력 → 진도 보고서 출력 확인.

---

### STEP 3. agent-agency 레포 분석 (3분)

**[목적]** 표준 서브에이전트 1개 깊이 분석해서 패턴 추출.

**[보여줄 자료]**
- 레포: `https://github.com/msitarzewski/agency-agents` (95k stars, MIT, 22 카테고리)
- 분석 대상: `engineering/engineering-code-reviewer.md`

**[Claude Code 입력]**

```text
/docs-guide:docs-guide 이 서브에이전트 파일의 구조와 패턴 분석해줘:

https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-code-reviewer.md

특히 다음을 정리:
1. frontmatter에 어떤 필드들이 있고 각각 무슨 역할인지
2. 본문 섹션 구조 (어떤 순서로 뭐가 들어가는지)
3. 자동 위임이 잘 되도록 description을 어떻게 썼는지

결과를 ~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습19-커맨드서브에이전트/agent-agency-pattern.md 에 저장.
```

**[추출되어야 할 패턴]**
- frontmatter 5필드: `name` / `description` / `color` / `emoji` / `vibe`
- 본문 5섹션: Identity & Memory / Core Mission / Critical Rules / Review Checklist / Communication Style
- description 패턴: "Expert {분야} who {핵심 동작}, focused on {목표}"

---

### STEP 4. practice-coach 만들기 + 자동 위임 테스트 (5분)

**[목적]** 분석한 패턴 그대로 본인 학습 코치 서브에이전트 만들기.

**[Claude Code 입력]**

```text
~/fastcampus-cc/.claude/agents/practice-coach.md 파일 만들어줘.

방금 분석한 engineering-code-reviewer.md 패턴 그대로 따라서:

frontmatter:
- name: practice-coach
- description: Claude Code 강의 실습 결과물을 평가하고 다음 단계를 추천합니다. "내 실습 평가해줘", "다음 뭐 해야 해?", "잘하고 있나?" 같은 요청에 자동 발동.
- tools: Read, Glob
- color: green
- emoji: 🎯
- vibe: Evaluates like a supportive mentor — celebrates wins, points growth areas without judgment.

본문 섹션 5개 (분석한 패턴 그대로):
1. Identity & Memory — 클로드코드 학습 코치 역할
2. Core Mission — 평가 기준 5가지 (실습 완료도 / 결과물 품질 / 대화 패턴 / 다음 단계 / 격려 포인트)
3. Critical Rules — 잘한 점 먼저 / 구체적 근거 / 다음 단계 명확하게 / 격려 톤
4. Review Checklist — 🔴 핵심 누락 / 🟡 개선 / 💭 보너스
5. Communication Style — 한국어 존댓말, 친근하게, 끝에 다음 행동 1개 제안
```

**[자동 위임 테스트]**

```text
지금까지 한 실습들 평가해줘. ~/fastcampus-cc/50-my-work/ 폴더 보고.
```

→ Claude가 `practice-coach` 자동 위임 → 별도 컨텍스트에서 평가 → 메인 대화엔 요약만 반환

**[검증]** 평가 리포트가 `잘한 점 / 개선 제안 / 다음 단계 / 격려 한 줄` 4섹션으로 출력되는지 확인.

---

### STEP 5. 3가지 자산 비교 정리 (1.5분)

**[Claude Code 입력]**

```text
오늘 만든 /study-progress와 practice-coach,
그리고 Part 06에서 만들 스킬을 비교 표로 정리해줘.

관점:
- 호출 방식 (명시 vs 자동)
- 파일 구조 (파일 vs 폴더)
- 컨텍스트 (메인 vs 분리)
- 만든 시점

저장: ~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습19-커맨드서브에이전트/three-assets-comparison.md
```

---

### STEP 6. 마무리 + 다음 클립 예고 (0.5분)

> 다음 클립은 MCP & CLI — 외부 도구를 클로드코드에 꽂는 방법.
> 오늘 만든 practice-coach도 외부 데이터 끌어오면 더 강력해진다.

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| `/study-progress` 호출 안 됨 | "클로드코드 재시작 안 했나? exit 후 claude 재실행 알려줘" |
| 호출은 되는데 빈 보고서 | 정상 — 강의 초반은 데이터 적음. "초반이라 OK" |
| `$ARGUMENTS` 작동 안 함 | "대문자 ARGUMENTS 정확한지 확인" |
| agent-agency 레포 fetch 실패 | "engineering-code-reviewer.md 본문을 직접 보여줘" 또는 강사 사전 캡처 자료 활용 |
| `practice-coach` 자동 위임 안 됨 | "description에 자연어 트리거 키워드(평가/다음 단계/잘하고 있나) 추가" |
| 자동 위임 대신 메인에서 처리 | "tools에 Read, Glob 명시되어 있는지 확인" |
| 평가 리포트가 일반론적 | "tools 없어서 파일 못 읽는다 — frontmatter 확인" |
| 강의 워크스페이스에 만들고 싶음 | "그건 REFERENCE라 수정 X. ~/fastcampus-cc/ 안에서만 작업" |
| 직접 호출 vs 자동 위임 헷갈림 | "직접: @practice-coach 평가해줘 / 자동: 그냥 평가해줘" |
| 본인 직무 다른 카테고리 분석하고 싶음 | "marketing/, design/, sales/ 등 어디든 OK. 패턴 동일" |
| 한글 이름 만들고 싶음 | "한글도 작동하지만 한영 전환이 시연 흐름 끊음. 표준은 영문 kebab-case" |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리

### 1. 결과물 검증

다음 파일들 존재 확인:
- `~/fastcampus-cc/.claude/commands/study-progress.md`
- `~/fastcampus-cc/.claude/agents/practice-coach.md`
- `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습19-커맨드서브에이전트/agent-agency-pattern.md`
- `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습19-커맨드서브에이전트/three-assets-comparison.md`

빠진 게 있으면 어떤 게 빠졌는지 안내.

### 2. README.md 자동 작성

`~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습19-커맨드서브에이전트/README.md`:

```markdown
# 실습 19 — 커맨드 & 서브에이전트 (스킬의 재료들)

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 강의 워크스페이스: ~/fastcampus-cc/

## 3가지 자산 가족 관계

| 자산 | 비유 | 호출 | 파일 구조 | 컨텍스트 |
|---|---|---|---|---|
| 슬래시 커맨드 | 매크로 | /이름 명시 | 파일 1개 | 메인과 같음 |
| 서브에이전트 | 전문가 | 자연어 자동 위임 | 파일 1개 | 분리됨 |
| 스킬 (Part 06) | 매뉴얼 | 자연어 자동 발동 | 폴더 + 추가 파일 | forked 가능 |

세 자산은 독립적이고 조합 가능. 구성요소가 아니라 가족.

## 만든 자산 (~/fastcampus-cc/)

### /study-progress 커맨드
- 위치: ~/fastcampus-cc/.claude/commands/study-progress.md
- 역할: 강의 진도 자동 정리 (progress.json + 50-my-work 스캔)
- frontmatter: description (강의 진도 정리 키워드)
- 변수: $ARGUMENTS (사용자 추가 메모)

### practice-coach 서브에이전트
- 위치: ~/fastcampus-cc/.claude/agents/practice-coach.md
- 역할: 강의 실습 결과물 평가 + 다음 단계 추천
- 자동 위임 트리거: "평가해줘", "다음 뭐 해야 해?", "잘하고 있나?"
- tools: Read, Glob
- 패턴: agent-agency 레포 engineering-code-reviewer.md 분석 후 적용

## agent-agency 레포 분석 결과
- URL: https://github.com/msitarzewski/agency-agents (95k stars, MIT)
- 분석 대상: engineering-code-reviewer.md
- frontmatter 5필드: name / description / color / emoji / vibe
- 본문 5섹션: Identity / Mission / Rules / Checklist / Communication
- description 패턴: "Expert {분야} who {핵심 동작}, focused on {목표}"

## 자동 위임 첫 호출 결과 요약
{practice-coach가 첫 호출에서 보여준 평가 리포트 핵심 한 줄}

## 6단계 진행 (실습)
- 1 강의 워크스페이스 stuck.md 뜯기 (REFERENCE)
- 2 /study-progress 만들기 + 호출
- 3 agent-agency 레포 분석
- 4 practice-coach 만들기 + 자동 위임 테스트
- 5 3가지 자산 비교 정리
- 6 다음 클립 예고

## 평생 활용 응용 가이드
- /study-progress 패턴 → /weekly-report, /sales-summary 등 본인 업무 매크로
- practice-coach 패턴 → code-reviewer, proposal-evaluator 등 본인 분야 코치
- agent-agency 레포는 200+ 에이전트 청사진. 새 직무/프로젝트마다 카테고리 골라서 변형

## Part 06 빌드업
- 오늘 만든 두 자산이 Part 06에서 SKILL.md(매뉴얼)로 발전
- /study-progress → 자동 진도 트래킹 스킬
- practice-coach → 스킬 안에서 호출 가능한 에이전트

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

`~/fastcampus-cc/progress.json`:

```json
{
  "practice_completed": [..., "실습 19"],
  "current_clip": null,
  "last_activity": "{ISO8601}",
  "commands_created": [..., "study-progress"],
  "agents_created": [..., "practice-coach"]
}
```

### 4. 회고 한 줄

자유 입력으로 받기:

> "오늘 만든 두 자산(커맨드와 서브에이전트) 중 어디에 가장 끌렸는지, 본인 업무에 어떻게 응용할지 한 줄로 적어주세요."

받은 텍스트를 README의 "핵심 발견 / 회고" 섹션에 기록.

### 5. 다음 클립 안내

```
실습 19 완료. 클로드코드 3가지 자산 중 두 개(커맨드 + 서브에이전트)를
~/fastcampus-cc/ 안에 영구 자산으로 만들었습니다.

✓ /study-progress — 강의 진도 자동 정리 매크로
✓ practice-coach — 실습 평가 코치 (자동 위임)

이 두 자산은 Part 06/07 끝까지 계속 활용되고,
강의 끝나도 본인 업무에 평생 응용 가능합니다.

다음은 Clip 03 — MCP & CLI로 외부 도구 연결.
시작하려면 /part05 다시 호출하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 번에 출력하고 사용자가 실습으로 진행
- **실습 진행 방식**: 강사 1줄 입력 → 학생 같은 줄 입력 → 결과 같이 확인. STOP 분리 패턴 금지
- **강의 워크스페이스 절대 수정 X**: 모든 변경은 `~/fastcampus-cc/`에서만. STEP 1만 강의 워크스페이스 파일을 보여주는데, 보기만 함
- **자유 진행 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **영문 kebab-case 강제**: 커맨드/에이전트 이름은 영문. 한글 만들려고 하면 한영 전환 흐름 끊김 안내
- **"~해줘" 패턴 금지 / "~하려는데 어떻게 해?" 패턴 강제**
- **3가지 자산 가족 관계 강조**: 구성요소가 아니라 독립적이고 조합 가능한 가족
- **Part 06 사슬 명시**: WRAP에서 오늘 만든 두 자산이 Part 06에서 매뉴얼(스킬)로 발전됨을 안내
