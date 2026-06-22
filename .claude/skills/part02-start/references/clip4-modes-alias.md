# Clip 4: 모드 + cc Alias

> Claude Code의 권한 모드 (Shift+Tab + /powerup) + Bypass 추가 + cc Alias로 빠른 실행 + Part 02 마무리.
>
> 📖 공식 문서: https://code.claude.com/docs/ko/permission-modes

---

## Phase 1 — 권한 모드 전체 학습 (Shift+Tab → /powerup → Bypass)

### EXPLAIN

Clip 3에서 폴더 정리할 때 AI가 뭔가 할 때마다 "이거 해도 돼?" 물어봤죠? 그게 **기본 모드**예요. 매번 허락을 구합니다.

근데 매번 물어보면 좀 느리잖아요? 그래서 **권한 모드**가 여러 가지 있습니다. 자동차 기어라고 생각하시면 편해요.

#### 1단계 — Shift+Tab으로 모드 사이클 보기

Claude Code 실행 상태에서 `Shift+Tab` 한 번 눌러보세요. 모드가 바뀌고 Status Line에 표시됩니다.

```
Default → Accept-edits → Plan → 다시 Default ...
```

(Bypass는 사이클에 없음 — 별도 활성화 필요. 아래에서 설명)

#### 2단계 — `/powerup`으로 각 모드 자세히 학습

`/powerup` 실행 → "권한 모드" 토픽 선택. Claude Code가 직접 4가지 모드를 인터랙티브로 설명해줍니다. 강사는 옆에서 자동차 기어 비유로 보강:

| 모드 | powerup 설명 (요약) | 자동차 기어 비유 |
|---|---|---|
| **Default** | 모든 행동마다 "할까요?" 물어봄 | 수동 기어 — 안전, 느림 |
| **Accept-edits** | 안전한 파일 편집은 자동 수락, 위험한 건 물어봄 | 자동 기어 — **입문자 추천 기본** |
| **Plan** | 실행 전 계획부터 보여줌 | 네비게이션 — 복잡한 일 시작할 때 |
| **Auto** | 위험한 것만 물어보고 알아서 진행 | 풀 자동 — Max 사용자 ★ |

#### 3단계 — Bypass 모드 (powerup엔 없음, 추가 설명)

**Bypass = 안 물어보고 전부 실행** (레이싱 모드).

**활성화 방법**:
```bash
# 실행 시 플래그
claude --dangerously-skip-permissions
```

또는 Shift+Tab 사이클을 확장하는 별도 설정.

**활용 시나리오**:
- 신뢰 가능한 반복 작업 (대량 파일 처리, 빌드 자동화 등)
- 격리된 환경 (sandbox, 테스트 컨테이너)

**주의**: 입문자엔 첫날부터 권장 X. **"이런 강력한 도구가 있다"**만 인지하고, 익숙해지면 본인 책임 하에 활용. 강사는 본인 사용 케이스 공유.

> 💡 강의 기본 권장: **Pro 사용자 → Accept-edits / Max 사용자 → Auto / 익숙해진 후 → Bypass (선택적)**

### EXECUTE

1. Claude Code 실행 → `Shift+Tab` 한 번씩 눌러서 사이클 확인
2. `/powerup` 입력 → "권한 모드" 토픽 선택 → 강의 보면서 따라가기
3. 각자 환경에 맞는 모드로 세팅:
   - Pro 사용자: **Accept-edits**
   - Max 사용자: **Auto** (Opus 4.7 모델 사용 시)
   - Bypass는 처음엔 선택 X

확인 질문:

```json
{
  "questions": [{
    "question": "지금 Claude Code 모드를 무엇으로 세팅하셨나요?",
    "header": "모드 확인",
    "options": [
      {"label": "Accept-edits ✓", "description": "Pro 사용자 추천 — 안전한 편집은 자동 수락"},
      {"label": "Auto ✓", "description": "Max 사용자 — 위험한 것만 물어봄"},
      {"label": "Plan", "description": "복잡한 작업 전 계획부터"},
      {"label": "Default (기본)", "description": "매번 물어봄 — 처음엔 OK"},
      {"label": "Bypass", "description": "안 물어봄 — 책임 하에 사용"}
    ],
    "multiSelect": false
  }]
}
```

```
👆 모드 세팅 끝나면 "다음"이라고 입력해주세요.
```

---

## Phase 2 — cc Alias 설정 + Part 02 완료

### EXPLAIN

매번 `claude` 다 치는 거 귀찮잖아요. 짧은 별명(alias)을 붙여줍니다.

#### 추천 alias 3종

| 별명 | 명령 | 용도 |
|---|---|---|
| **`cc`** | `claude` | 기본 실행 |
| **`ccd`** | `claude --dangerously-skip-permissions` | Bypass 모드로 바로 시작 (반복 작업·신뢰 작업) |
| **`ccr`** | `claude --resume --dangerously-skip-permissions` | 이전 세션 이어서 + Bypass |

> 💡 `ccd`/`ccr`은 Bypass 모드 자동 활성화이니 본인 책임 하에 사용하세요. 입문자는 `cc`만 써도 충분합니다.

| OS | 설정 파일 |
|---|---|
| Mac | `~/.zshrc` |
| Windows WSL | `~/.bashrc` |

### EXECUTE

#### 1단계 — 어떤 alias를 설정할지 선택

먼저 클로드코드 종료:
```
/exit  또는  Ctrl+C
```

`AskUserQuestion`으로 alias 설정 옵션 제시:

```json
{
  "questions": [{
    "question": "어떤 alias 패키지를 설치할까요?",
    "header": "Alias 선택",
    "options": [
      {"label": "기본 — cc만 (입문자 추천)", "description": "claude 실행만"},
      {"label": "풀 패키지 — cc + ccd + ccr", "description": "기본 + Bypass 단축 + Resume Bypass"},
      {"label": "커스텀 — 별명 직접 입력", "description": "cc 말고 다른 이름으로 (예: clc, claudie 등)"},
      {"label": "건너뛰기 — 이미 설정함", "description": "본인 .zshrc/.bashrc 이미 손봤음"}
    ],
    "multiSelect": false
  }]
}
```

#### 2단계 — 선택에 따라 명령 안내

OS 자동 감지 (`uname -s` → Darwin이면 Mac, Linux이면 WSL/Linux). 적절한 rc 파일에 추가.

**기본 (cc만)** — Mac 예시:
```bash
echo 'alias cc="claude"' >> ~/.zshrc
source ~/.zshrc
```

**풀 패키지 (cc + ccd + ccr)** — Mac 예시:
```bash
cat >> ~/.zshrc << 'EOF'
alias cc='claude'
alias ccd='claude --dangerously-skip-permissions'
alias ccr='claude --resume --dangerously-skip-permissions'
EOF
source ~/.zshrc
```

**커스텀** — 자연어로 동작 설명 → 적절한 명령 생성:

사용자에게 자유 입력 요청:
> "어떤 별명으로, 어떤 동작을 하게 만드시겠어요? 자유롭게 설명해주세요. 예시:
> - '별명 plc로 plan 모드 바로 시작하고 싶어요'
> - 'cca로 Auto 모드 시작'
> - 'cco로 Opus 모델 사용'
> - 'ccs로 이전 세션 이어서'"

스킬이 입력 분석 → 적절한 `claude` 옵션 조합으로 alias 명령 생성:

| 사용자 의도 | 생성할 alias |
|---|---|
| Plan 모드 바로 | `alias plc='claude --permission-mode plan'` |
| Auto 모드 바로 | `alias cca='claude --permission-mode auto'` |
| Opus 모델 | `alias cco='claude --model opus'` |
| Resume + Bypass | `alias ccs='claude --resume --dangerously-skip-permissions'` |

> ⚠️ 옵션 정확한 플래그명은 `claude --help`로 확인 후 적용. 모르는 옵션은 만들지 말고 사용자에게 다시 물어볼 것.

생성한 명령을 보여주고 확인 받은 후 `~/.zshrc` (또는 `~/.bashrc`)에 추가:
```bash
echo '{생성된 alias}' >> ~/.zshrc && source ~/.zshrc
```

> WSL은 모든 명령에서 `~/.zshrc` → `~/.bashrc`로 바꿔서 진행.

#### 3단계 — 작동 확인

설정한 별명을 터미널에 입력:
```bash
cc        # 또는 본인이 설정한 별명
```

→ 클로드코드 실행되면 성공.

```json
{
  "questions": [{
    "question": "별명 입력하니까 어떻게 됐나요?",
    "header": "Alias 확인",
    "options": [
      {"label": "클로드코드 실행됨 ✓", "description": "alias 설정 성공"},
      {"label": "command not found 에러", "description": "터미널 재시작 또는 source 명령 다시 실행"},
      {"label": "다른 프로그램이 실행됨", "description": "다른 alias가 차지 중 — 위 '커스텀'으로 다른 별명 시도"}
    ],
    "multiSelect": false
  }]
}
```

```
👆 별명 작동하시면 "완료"라고 입력해주세요.
```

---

## QUIZ (Phase 2 끝난 뒤)

```json
{
  "questions": [{
    "question": "이 강의에서 입문자가 기본으로 쓰면 좋은 권한 모드는?",
    "header": "Part 02 마무리 퀴즈",
    "options": [
      {"label": "Default", "description": "매번 허락 — 안전, 느림"},
      {"label": "Accept-edits", "description": "안전한 편집 자동 수락 — 입문자 기본"},
      {"label": "Plan", "description": "실행 전 계획부터"},
      {"label": "Auto", "description": "위험한 것만 물어봄 — Max 전용"},
      {"label": "Bypass", "description": "안 물어봄 — 익숙해진 후"}
    ],
    "multiSelect": false
  }]
}
```

**정답**: Accept-edits (Max 사용자라면 Auto도 OK)
**피드백**: "Accept-edits는 안전한 편집은 자동 수락하면서 위험한 건 물어보는 균형 잡힌 모드예요. 첫날부터 안심하고 쓸 수 있고, 강의 진행도 매끄럽습니다."

---

## Part 02 완료 처리

**1) 결과물 저장**

`50-my-work/Part02-시작하기/실습04-모드소개-Alias/` 자동 생성 후 `README.md`에 다음 기록:
- 완료 시각
- 사용한 모델
- 선택한 모드 (Default / Accept-edits / Plan / Auto / Bypass)
- cc Alias 설정 여부 (Mac zshrc / WSL bashrc)

**2) progress.json 업데이트**

워크스페이스 루트의 `progress.json`:

```json
{
  "completed_parts": ["Part 01", "Part 02"],
  "practice_completed": ["실습 1", "실습 2", "실습 3", "실습 4"],
  "environment": {
    "os": "macOS|WSL2 Ubuntu",
    "claude_version": "(claude --version 결과)",
    "alias_set": true,
    "preferred_mode": "Accept-edits|Auto|..."
  },
  "current_clip": null,
  "last_activity": "(현재 시각 ISO 8601)"
}
```

완료 메시지:
```
🎉 Part 02 완료!

✓ 실습 1, 2: 환경 설치 (강의 영상)
✓ 실습 3: 첫 실행 — 화면/슬래시/모델/powerup + 폴더 정리
✓ 실습 4: 권한 모드 (Default/Accept-edits/Plan/Auto + Bypass) + cc Alias

다음은 Part 03 — 본격적으로 대화로 결과물을 만들어봅니다.
데이터 분석, 보고서, 대시보드, 카드뉴스, 웹사이트까지. 전부 대화만으로요.

/part03 입력하세요.
```
