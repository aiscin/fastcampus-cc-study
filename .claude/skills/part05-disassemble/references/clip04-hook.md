# Clip 04 — Hook (자동화의 방아쇠 설정하기)

> Part 05 / Ch 01 / Clip 04 (실습 21) | 예상 시간: ~20분
> 결과물: ~/fastcampus-cc/.claude/settings.json에 Hook 3개 (Stop 알림음 + SessionStart 환영 + PreToolUse 안전장치)
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
WORK_DIR="$ROOT/50-my-work/Part05-뜯어보기/실습21-Hook"
mkdir -p "$WORK_DIR"

# 강의 워크스페이스의 .claude 디렉토리 보장
mkdir -p "$STUDY_DIR/.claude"

# 운영체제 감지 (강사 시연 시 본인 OS 안내용)
OS=$(uname -s)
echo "✓ $WORK_DIR 준비 완료"
echo "✓ ~/fastcampus-cc/.claude/ 디렉토리 확인됨"
echo "ℹ 운영체제: $OS"
if [ "$OS" = "Darwin" ]; then
  echo "  Mac: afplay /System/Library/Sounds/Glass.aiff 사용"
elif [ "$OS" = "Linux" ]; then
  echo "  Linux: notify-send 또는 paplay 사용"
else
  echo "  Windows: powershell -c \"[console]::beep(500,300)\" 사용"
fi
```

셋업 결과 한 줄 보고 후 아래 **Hook 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## Hook 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 한 줄 | 이벤트 발생 시 자동 실행되는 셸 명령 |
| 비유 | 스마트홈 — "문 열리면 불 켜짐" |
| 위치 | `~/fastcampus-cc/.claude/settings.json` |
| 형식 | JSON — `hooks.{이벤트명}.[{matcher, hooks: [{type, command}]}]` |

### 5가지 이벤트

| 이벤트 | 언제 발생 | 활용 예 |
|--------|---------|--------|
| `UserPromptSubmit` | 메시지 입력 직후 | 로깅, 키워드 검사 |
| `PreToolUse` | 도구 실행 직전 | 위험 명령 차단 |
| `PostToolUse` | 도구 실행 완료 후 | 결과 알림, 자동 포매팅 |
| `Stop` | AI 응답 완료 | 알림음, 상태 저장 |
| `SessionStart` | 세션 시작/재개 | 환영 메시지, TODO 출력 |

### 오늘 만들 Hook 3종

| 결 | Hook | 이벤트 | 효과 |
|---|---|---|---|
| **편의** | stop-alert | Stop | 응답 완료 시 알림음 |
| **습관** | session-welcome | SessionStart | 세션 시작 환영 + 진도 안내 |
| **안전** | rm-guard | PreToolUse (Bash) | `rm -rf /` 등 위험 명령 차단 |

### 핵심 메시지

> **'매번 수동'을 '알아서 자동'으로.** Hook은 본인 작업 흐름의 안전망이자 가속기.

---

## 진행 안내

```
✓ 50-my-work/Part05-뜯어보기/실습21-Hook/ 준비 완료
✓ ~/fastcampus-cc/.claude/ 디렉토리 확인됨

오늘 할 거 (~20분)
- Hook = 이벤트가 일어나면 자동 실행되는 동작
- 5가지 이벤트 인지 (PreToolUse / PostToolUse / Stop / Notification / SessionStart)
- Hook 3개 직접 설정 (편의·습관·안전)
- 실습 (강사 입력 → 같은 입력 → 결과 같이 확인)

5단계 흐름:
1. Hook 개념 + 5가지 이벤트
2. Stop hook — AI 응답 완료 알림음 (편의)
3. SessionStart hook — 세션 시작 환영 (습관)
4. PreToolUse hook — 위험 명령 차단 (안전)
5. Hook 3종 정리

★ 강의 워크스페이스 (~/fastcampus-cc/) 절대 수정 X
  모든 변경은 ~/fastcampus-cc/.claude/settings.json 에서만
★ 운영체제별 명령 차이 — Mac/Linux/Windows
```

---

## 단계별 진행 가이드

### STEP 1. Hook 개념 + 5가지 이벤트 (3분)

**[목적]** Hook 정의 + 5가지 이벤트 한 줄씩 인지.

**[보여줄 자료]** 위 "5가지 이벤트" 표 + 일상 비유 (스마트홈).

**[Part 06 빌드업 멘트]** "Hook도 settings.json도 다 영구 자산. 강의 끝나도 본인 환경 그대로."

---

### STEP 2. Stop hook — AI 응답 완료 알림음 (4분)

**[목적]** 첫 Hook 설정 — 편의 결.

**[Claude Code 입력]** (Mac 기준 — Windows/Linux는 멘트 바꿔서)

```text
~/fastcampus-cc/.claude/settings.json에 Stop hook을 추가하려는데 어떻게 해?
AI 응답이 끝나면 Mac의 afplay로 알림음 재생.
```

**[검증]** 안티그래비티에서 `~/fastcampus-cc/.claude/settings.json` 열어 확인.

**[활성화]** 클로드코드 재시작 (`exit` → `claude`) — Hook은 시작 시 로드.

**[테스트]**

```text
1+1 뭐야?
```

→ 응답 끝날 때 Glass 사운드 울림.

---

### STEP 3. SessionStart hook — 세션 시작 환영 (4분)

**[목적]** 두 번째 Hook 설정 — 습관 결.

**[Claude Code 입력]**

```text
~/fastcampus-cc/.claude/settings.json에 SessionStart hook도 추가하려는데 어떻게 해?
세션 시작 시 클립 02에서 만든 /study-progress 결과를 자동으로 한 번 보여주고,
"안녕하세요!" 인사도.
```

**[검증]** settings.json에 SessionStart 블록 추가 확인.

**[활성화]** 재시작.

**[테스트]** 시작 즉시 환영 메시지 + 진도 안내 출력.

---

### STEP 4. PreToolUse hook — 위험 명령 차단 (3분)

**[목적]** 세 번째 Hook 설정 — 안전 결.

**[Claude Code 입력]**

```text
~/fastcampus-cc/.claude/settings.json에 PreToolUse hook도 추가하려는데 어떻게 해?
Bash 도구 실행 직전에 — 명령어에 'rm -rf /' 또는 'sudo rm'이 포함되면 차단.
exit 2로 차단하고 'BLOCKED: dangerous command'를 출력.
```

**[검증]** settings.json에 PreToolUse 블록 추가 + matcher: "Bash" 확인.

**[활성화]** 재시작.

**[안전 테스트]**

```text
'rm -rf /' 명령을 bash로 실행해줘 (테스트 — 실제 실행 안 됨)
```

→ Hook이 발동되어 BLOCKED 출력. 실행 안 됨.

---

### STEP 5. Hook 3종 정리 (2분)

**[Claude Code 입력]**

```text
오늘 만든 Hook 3개를 비교 표로 정리해줘.

관점:
- 결 (편의/습관/안전)
- 이벤트
- matcher
- 명령 (한 줄)
- 효과

저장: ~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습21-Hook/hooks-summary.md
```

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| Stop hook 설정했는데 알림 안 울림 | "클로드코드 재시작 안 했나? exit 후 claude 재실행" |
| macOS afplay 권한 오류 | "시스템 설정 → 개인정보 보호 → 사운드 접근 허용" |
| Windows에서 afplay 안 됨 | "Mac 전용 — powershell -c \"[console]::beep(500,300)\"로 교체하려는데 어떻게 해?" |
| Linux에서 afplay 안 됨 | "Mac 전용 — notify-send 또는 paplay로 교체하려는데 어떻게 해?" |
| Hook이 너무 자주 울려서 거슬림 | "matcher를 특정 도구로 제한하거나 일시 비활성화하려는데 어떻게 해?" |
| JSON 문법 오류 | "settings.json 문법 검증하고 고쳐주려는데 어떻게 해?" |
| settings.json 안 열림 | "안티그래비티에서 ~/fastcampus-cc/ 열고 .claude/ 펼치기" |
| 위험한 Hook 설정 실수 | "settings.json에서 해당 Hook 블록 삭제 후 재시작" |
| Hook 삭제 방법 모름 | "settings.json에서 해당 이벤트 블록만 제거" |
| 강의 워크스페이스 settings.json 수정 시도 | "그건 REFERENCE라 수정 X. ~/fastcampus-cc/.claude/settings.json에서만" |
| PreToolUse 너무 광범위 차단 | "matcher를 특정 명령에만 한정하려는데 어떻게 해?" |
| `$TOOL_INPUT` 작동 안 함 | "Claude Code 버전 확인 — 최신 버전에서 사용 가능" |
| SessionStart hook 시작 느림 | "echo 같은 가벼운 명령만. 무거운 명령(gws CLI 호출 등) 빼기" |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리

### 1. 결과물 검증

다음 파일들 존재 확인:
- `~/fastcampus-cc/.claude/settings.json` (Hook 3개 다 들어있는지 — Stop / SessionStart / PreToolUse)
- `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습21-Hook/hooks-summary.md` (비교 정리)

설정 파일 검증:

```bash
python3 -c "import json; d=json.load(open('$STUDY_DIR/.claude/settings.json')); h=d.get('hooks',{}); print('Hook 이벤트:', list(h.keys()))"
# 출력 예: Hook 이벤트: ['Stop', 'SessionStart', 'PreToolUse']
```

3개 이벤트 다 있어야 통과. 없으면 어떤 게 빠졌는지 안내.

### 2. README.md 자동 작성

`~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습21-Hook/README.md`:

```markdown
# 실습 21 — Hook (자동화의 방아쇠 설정하기)

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 강의 워크스페이스: ~/fastcampus-cc/
- 운영체제: {Mac / Windows / Linux}

## Hook 정의
이벤트 발생 시 자동 실행되는 셸 명령. 스마트홈 같은 자동화.

## 5가지 이벤트
| 이벤트 | 언제 | 활용 |
|---|---|---|
| UserPromptSubmit | 메시지 입력 후 | 로깅 |
| PreToolUse | 도구 실행 직전 | 위험 명령 차단 |
| PostToolUse | 도구 실행 후 | 결과 알림 |
| Stop | 응답 완료 | 알림음 |
| SessionStart | 세션 시작 | 환영 |

## 만든 Hook 3종 (~/fastcampus-cc/.claude/settings.json)

### 1. stop-alert (편의)
- 이벤트: Stop
- matcher: *
- 명령: afplay /System/Library/Sounds/Glass.aiff
- 효과: AI 응답 완료 시 알림음 — 백그라운드 작업 알림용

### 2. session-welcome (습관)
- 이벤트: SessionStart
- matcher: *
- 명령: echo '안녕하세요! 오늘도 화이팅 — 진도 한 번 확인하실까요? /study-progress'
- 효과: 매일 클로드코드 켤 때마다 환영 + 진도 커맨드 안내

### 3. rm-guard (안전)
- 이벤트: PreToolUse
- matcher: Bash
- 명령: if grep -qE 'rm -rf /|sudo rm' <<< "$TOOL_INPUT"; then echo 'BLOCKED'; exit 2; fi
- 효과: 위험 명령 자동 차단 (자동 모드 안전망)

## 5단계 진행 (실습)
- 1 Hook 개념 + 5가지 이벤트
- 2 Stop hook 시연 (편의)
- 3 SessionStart hook 시연 (습관)
- 4 PreToolUse hook 시연 (안전)
- 5 Hook 3종 정리

## 평생 활용 응용 가이드
- settings.json = 작업 환경 DNA. 다른 컴퓨터에 복사하면 같은 환경 재현
- 본인 작업 흐름에 맞춰 Hook 추가 — 알림 / TODO / 안전장치
- 회사 작업 환경 셋업 시 settings.json 1개로 끝

## Part 06 빌드업
- 스킬에 Hook 심어서 자동화 고도화
- 예: 스킬 시작 시 hook으로 환경 검증 자동

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

`~/fastcampus-cc/progress.json`:

```json
{
  "practice_completed": [..., "실습 21"],
  "current_clip": null,
  "last_activity": "{ISO8601}",
  "hooks_created": [..., "stop-alert", "session-welcome", "rm-guard"]
}
```

### 4. 회고 한 줄

자유 입력으로 받기:

> "오늘 만든 Hook 3개 (편의/습관/안전) 중 본인 작업에 가장 쓸모있을 것 같은 결을 한 줄로 적어주세요."

받은 텍스트를 README의 "핵심 발견 / 회고" 섹션에 기록.

### 5. 다음 클립 안내

```
실습 21 완료. ~/fastcampus-cc/.claude/settings.json에 Hook 3개를 영구 자산으로 쌓았습니다.

✓ stop-alert (편의) — 응답 완료 알림음
✓ session-welcome (습관) — 세션 시작 환영
✓ rm-guard (안전) — 위험 명령 차단

settings.json 한 파일에 본인 작업 환경의 DNA가 담겼어요.
다른 컴퓨터에서도 그대로 재현 가능합니다.

다음은 Clip 05 — GitHub로 모든 자산 백업 (Part 05 마지막).
시작하려면 /part05 다시 호출하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 번에 출력하고 사용자가 실습으로 진행
- **실습 진행 방식**: 강사 1줄 입력 → 학생 같은 줄 입력 → 결과 같이 확인. STOP 분리 패턴 금지
- **강의 워크스페이스 절대 수정 X**: 모든 변경은 `~/fastcampus-cc/.claude/settings.json`에서만
- **운영체제별 명령 차이 안내**: 자동 셋업에서 OS 감지 후 본인 OS에 맞는 명령 안내
- **Hook 활성화는 재시작 필수**: 매번 settings.json 수정 후 `exit` + `claude`
- **자유 진행 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **"~해줘" 패턴 금지 / "~하려는데 어떻게 해?" 패턴 강제**
- **Hook 영문 이름 강제**: stop-alert / session-welcome / rm-guard 등 kebab-case
- **Part 06 사슬 명시**: Hook이 스킬과 결합되어 자동화 고도화될 것임 안내
- **안전 테스트는 위험 명령 명시 X로 시뮬레이션**: 학생이 진짜 `rm -rf /` 치지 않게 — Hook이 막는다는 사실만 보여주기
