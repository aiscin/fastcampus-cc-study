---
name: part05-disassemble
description: "Part 05: 클로드코드 뜯어보기 (신 커리큘럼 v3.2). 1챕터 5클립 — CLAUDE.md / 커맨드+서브에이전트 / MCP+CLI / Hook / GitHub. Clip 1은 별도 학습 워크스페이스(~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/) 만들기 실습, Clip 2~5는 강의 워크스페이스(~/fastcampus-cc/) 자체에 커맨드·에이전트·MCP·Hook을 추가하며 실습. '/part05', 'Part 05', '뜯어보기' 요청에 사용."
---

# Part 05: 클로드코드 뜯어보기

이 스킬이 호출되면 아래 규칙을 반드시 따른다.

---

## 신 커리큘럼 v7.1 — Part 05 구성 (1챕터 / 5클립)

| Ch | Clip | 실습 # | 제목 (PDF·시트 공식 형식) | 시간 | 패턴 |
|---|:-:|:-:|---|---|---|
| **Ch 01 — 클로드코드 뜯어보기** | **1** | 18 | CLAUDE.md — AI에게 업무 매뉴얼 쓰기 | ~20분 | 실습 (자동 셋업 + 영상 보면서 진행) |
|  | **2** | 19 | 커맨드 & 서브에이전트 — 스킬의 재료들 알아보기 | ~20분 | 실습 |
|  | **3** | 20 | MCP & CLI — 외부 도구 연결하기 | ~30분 | 실습 |
|  | **4** | 21 | Hook — 자동화의 방아쇠 설정하기 | ~20분 | 실습 |
|  | **5** | 22 | GitHub — git-teacher로 백업하기 | ~20분 | 실습 |

**Part 05 핵심 framing**: **Clip 1만** 별도 학습 워크스페이스(`~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/`)를 만들어 CLAUDE.md 실습 (강의 후에도 학생이 혼자 공부할 공간). **Clip 2~5는 강의 워크스페이스(`~/fastcampus-cc/`) 자체에** 커맨드/에이전트/MCP/Hook을 추가하며 실습 — 결과물은 `50-my-work/Part05-뜯어보기/실습NN-제목/`에 기록.

---

## References 파일 맵

| Clip | 파일 |
|:-:|---|
| Clip 1 | `references/clip01-claude-md.md` |
| Clip 2 | `references/clip02-command-subagent.md` |
| Clip 3 | `references/clip03-mcp-cli.md` |
| Clip 4 | `references/clip04-hook.md` |
| Clip 5 | `references/clip05-github.md` |

---

## Seed 워크스페이스

학생용 학습 워크스페이스 시드는 이 스킬 안에 포함되어 있다 — 자기완결성 (외부 의존 X).

```
.claude/skills/part05-disassemble/
├── SKILL.md
├── seed-my-cc-study/        ← 학생에게 자동 복사될 시드
│   ├── README.md
│   ├── 10-curriculum/
│   ├── 20-concepts/
│   ├── 30-resources/
│   ├── 40-ideas/
│   └── sandbox/
└── references/
    └── clip01-claude-md.md
```

각 클립의 `## 자동 셋업` Bash가 시드를 `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/`로 복사한다 (Clip 1만). 이후 클립은 같은 폴더에서 작업.

---

## 핵심 패턴 — 자동 셋업 → 실습 진행 → WRAP

```
[자동 셋업]      Clip 1: 시드 cp → ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/
                Clip 2~5: 진도 폴더 + 강의 워크스페이스 .claude/ 하위 자동 준비
   ↓
[브리핑 + 안내]  CLAUDE.md 정의·동작 흐름 + 단계 흐름 (한 메시지)
   ↓
[실습]      강사 1줄 입력 → 학생도 같은 줄 입력 → 결과 같이 확인 → 다음 단계
   ↓ (트리거: 완료 / /wrap / 끝 / 다음 클립)
[WRAP]          파일 검증 + README 자동 + progress.json + 다음 안내
```

각 클립은 자기 시간 (Clip 1 = 20분 / Clip 2 = 20분 / Clip 3 = 30분 / Clip 4 = 20분 / Clip 5 = 20분).

### 자동 셋업 의무 (모든 클립)

각 클립 reference 파일에 `## 자동 셋업` 섹션이 있다. 스킬이 클립 reference를 로드한 직후:

1. **reference의 `## 자동 셋업` Bash를 즉시 실행**
   - Clip 1: 시드 워크스페이스를 `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/`로 복사 (이미 있으면 백업 후 새로)
   - Clip 2~5: `~/fastcampus-cc/.claude/`, `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습NN-제목/` 자동 생성. Clip 1 결과물(my-cc-study) 의존 없음
2. **셋업 결과를 한 줄로 보고**
3. **`## 브리핑` (한 줄 정의·동작 흐름·핵심 메시지) + `## 진행 안내` 섹션을 한 메시지로 출력** + SLEEP 모드

### 진행 원칙 (메모리 가이드라인 반영)

1. **실습 진행 방식** — 강사가 1줄 입력하면 학생도 같은 줄 입력. STOP 분리 패턴 금지 (memory: feedback_followalong_practice.md)
2. 시작 시 진행 안내를 한 메시지로 출력 — 학습자가 영상 보기 전 한 번 읽고 시작
3. 자유 진행 중 스킬 개입 X — 사용자가 명시적 도움 요청(`막혔어요`/`도와줘`)할 때만
4. WRAP 트리거: `완료`, `/wrap`, `끝`, `다음 클립`
5. 회고: 자유 입력 (AskUserQuestion 없이)
6. **"~해줘" 패턴 금지 / "~하려는데 어떻게 해?" 패턴 강제** (memory: feedback_ask_how_pattern.md)
7. **강의 워크스페이스 기존 자산은 수정 X** — 기존 CLAUDE.md / 강의 스킬 파일은 보호. Clip 2~5에서 추가하는 본인 자산(`.claude/commands/`, `agents/`, `.mcp.json`, `.claude/settings.json`)은 강의 워크스페이스에 자유 추가

### AskUserQuestion 사용 위치 (제한)

| 위치 | 용도 |
|---|---|
| SKILL.md 시작 — 클립 선택 | 5 클립 라우팅 |

실습 reference (clip01~05)에서는 AskUserQuestion 사용 X. 회고도 자유 입력.

---

## 결과물 저장 규칙 ★

Part 05의 결과물은 두 곳에 저장:

1. **Clip 1만**: `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/CLAUDE.md` (학습 워크스페이스의 첫 결과물)
2. **Clip 2~5**: 강의 워크스페이스 자체에 자산 추가 (`~/fastcampus-cc/.claude/commands/`, `agents/`, `.mcp.json`, `.claude/settings.json`)
3. **공통**: `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습{NN}-{제목}/README.md` = 진도 기록

| Clip | 실제 산출물 위치 | 50-my-work 메타 |
|:-:|---|---|
| Clip 1 | `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/CLAUDE.md` | `실습18-CLAUDEmd/README.md` |
| Clip 2 | `~/fastcampus-cc/.claude/commands/`, `agents/` | `실습19-커맨드서브에이전트/README.md` |
| Clip 3 | `~/fastcampus-cc/.mcp.json` | `실습20-MCP-CLI/README.md` |
| Clip 4 | `~/fastcampus-cc/.claude/settings.json` | `실습21-Hook/README.md` |
| Clip 5 | GitHub repo URL | `실습22-GitHub/README.md` |

WRAP 단계에서 자동 생성:
- 클립별 결과물 파일들 (Clip 1: my-cc-study/CLAUDE.md, Clip 2~5: 강의 워크스페이스 자산)
- `50-my-work/.../README.md` — 날짜·모델·모드·진행 기록·핵심 발견/회고
- `progress.json` 업데이트 — 해당 실습 번호 추가

### progress.json 스키마 (이 스킬이 사용·수정하는 키)

| 키 | 타입 | 의미 | 기록 위치 |
|---|---|---|---|
| `current_clip` | string\|null | 진행 중 클립 | 모든 클립 |
| `practice_completed` | array | 완료한 실습 번호 (예: `["실습 18", "실습 19"]`) | 모든 클립 |
| `my_cc_study_path` | string | 학생 워크스페이스 경로 (기본 `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study`) | Clip 1 |
| `my_cc_study_initialized` | boolean | Clip 1 자동 셋업 완료 여부 | Clip 1 |
| `commands_created` | array | Clip 2에서 만든 커스텀 커맨드 이름들 | Clip 2 |
| `agents_created` | array | Clip 2에서 만든 서브에이전트 이름들 | Clip 2 |
| `mcp_installed` | array | Clip 3에서 설치한 MCP 이름들 | Clip 3 |
| `hooks_created` | array | Clip 4에서 만든 Hook 이름들 | Clip 4 |
| `github_repo` | string\|null | Clip 5 백업 대상 GitHub URL | Clip 5 |
| `completed_parts` | array | 완료한 Part (예: `["Part 04", "Part 05"]`) | Clip 5 (Part 05 마지막) |
| `level` | string | 현재 레벨 ("AI Intermediate" 유지) | Clip 5 |
| `last_activity` | string | ISO 8601 타임스탬프 | 모든 클립 |

---

## 시작

**1단계: progress.json 확인**

워크스페이스 루트의 `progress.json`을 Read로 읽는다. 다음 필드 확인:
- `practice_completed`
- `my_cc_study_initialized` (Clip 1 완료 여부)
- `current_clip` (재진입용)

각 Clip 1-5가 완료됐는지 매핑:
- Clip 1: `practice_completed`에 "실습 18"
- Clip 2: "실습 19"
- Clip 3: "실습 20"
- Clip 4: "실습 21"
- Clip 5: "실습 22"

**2단계: 분기 로직**

```
IF current_clip 있음:
   → "Clip N에서 멈춘 게 있어요. 이어서 진행할까요?"
     [이어가기 / 다른 클립 / 처음부터]

ELIF 모든 클립 완료 (5/5):
   → Part 05 완료 메시지 + /part06 안내

ELSE 미진행 클립 있음:
   → 직접 클립 선택 (한 번에 옵션 4개 한도)
```

**3단계: 직접 클립 선택**

```json
{
  "questions": [{
    "question": "어느 클립을 진행할까요?",
    "header": "Part 05 클립",
    "options": [
      {"label": "Clip 1 — CLAUDE.md", "description": "내 학습 워크스페이스 받고 /init + 인터뷰로 CLAUDE.md 만들기"},
      {"label": "Clip 2 — 커맨드 & 서브에이전트", "description": "/stuck 같은 커맨드 + 전문 에이전트 직접 만들기"},
      {"label": "Clip 3 — MCP & CLI", "description": "외부 도구 연결 (무료 MCP + Codex/Gemini 호출 체험)"},
      {"label": "Clip 4 — Hook", "description": "이벤트 자동화 (Stop hook 알림음 + 본인 hook)"}
    ],
    "multiSelect": false
  }]
}
```

(Clip 5는 다음 페이지 — 옵션 4개 한도라 첫 화면에 안 들어감. Clip 1~4 중 선택 후 5는 별도)

옵션은 미진행 클립만, 최대 4개. 이미 완료한 클립은 제외.

선택한 클립의 reference 파일을 읽고 **자동 셋업 → 진행 안내** 출력.

---

### 미진행 클립 매핑 (참고)

| Clip | 실습 # | 완료 키 |
|:-:|:-:|---|
| 1 | 18 | `practice_completed`에 "실습 18" |
| 2 | 19 | "실습 19" |
| 3 | 20 | "실습 20" |
| 4 | 21 | "실습 21" |
| 5 | 22 | "실습 22" |

---

## Part 05 완료 시 (Clip 5 WRAP 끝나면)

1. progress.json 업데이트:
   - `completed_parts`에 "Part 05" 추가
   - `practice_completed`에 "실습 18-22" 모두 기록 확인
   - `level`: "AI Intermediate" 유지 (Part 06 완료 시 "AI Advanced"로 승급)
   - `current_clip`: null
   - `last_activity`: 현재 시각

2. 완료 안내:
   ```
   Part 05 완료! 클로드코드의 5가지 핵심 구성요소(CLAUDE.md / 커맨드+에이전트 / MCP / Hook / GitHub)를 직접 만져봤습니다.

   ✓ Clip 1 CLAUDE.md — 내 학습 워크스페이스 + 본인 맞춤 매뉴얼
   ✓ Clip 2 커맨드 & 서브에이전트 — 반복 작업 단축키 + 전문 에이전트
   ✓ Clip 3 MCP & CLI — 외부 도구 연결
   ✓ Clip 4 Hook — 이벤트 자동화 방아쇠
   ✓ Clip 5 GitHub — 작업 백업 + 어디서나 접근

   ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/는 강의 끝나도 본인 클로드코드 공부 워크스페이스로 계속 사용하세요.

   다음은 Part 06 — 클로드코드 스킬 만들기. /part06 입력하세요.
   ```

---

## 강의 워크스페이스 사용 원칙

| 자산 | 위치 | 수정 가능 |
|---|---|---|
| 강의 워크스페이스 **기존 CLAUDE.md** | `~/fastcampus-cc/CLAUDE.md` | **❌ 수정 X** (강의 진행 의존) |
| 강의 워크스페이스 **기존 강의 스킬** | `~/fastcampus-cc/.claude/skills/part0X-*` 등 | **❌ 수정 X** |
| **Clip 2~5에서 추가하는 본인 자산** | `~/fastcampus-cc/.claude/commands/`, `agents/`, `.mcp.json`, `.claude/settings.json` | ✅ 자유 추가 |
| **Clip 1 학습 워크스페이스** | `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/` | ✅ 자유 수정 (Clip 1 한정) |

학생이 강의가 의존하는 **기존 CLAUDE.md / 강의 스킬 파일**을 수정하려고 하면 즉시 차단:

> "그건 강의가 의존하는 파일이라 수정하면 강의 진행이 깨져요. 본인 자산은 `.claude/commands/`나 `agents/`에 새 파일로 추가하시면 됩니다."
