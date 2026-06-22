# Clip 3: 첫 실행 — 화면/슬래시/모델/powerup + 폴더 정리

> 수강생의 **첫 Claude Code 실습**.
> 5개 Phase를 순차적으로 진행한다 — 각 Phase가 끝나면 STOP, 사용자 "완료"/"다음" 입력 후 다음 Phase.
>
> 📖 공식 문서: https://code.claude.com/docs/ko/quickstart

---

## Phase 1 — 화면 둘러보기

### EXPLAIN

Claude Code 화면에서 보이는 기본 요소들을 짚어주세요. 이름만 알면 앞으로 강의에서 "여기 보세요" 할 때 헷갈리지 않습니다.

| 요소 | 위치 | 역할 |
|------|------|------|
| **프롬프트 입력 영역** | 화면 하단 입력창 | 여기에 자연어로 명령. Enter로 제출, Shift+Enter로 줄바꿈 |
| **Status Line** | 입력창 바로 아래 회색 바 | 현재 디렉토리 / 모델 / 컨텍스트 % / Git 브랜치 / 비용 한눈에 |
| **응답 영역** | 화면 위쪽 | Claude의 답변, 코드블록, 파일 변경 내역 표시 |
| **도구 호출 표시** | 응답 중간 | `[Read file]`, `[Bash]` 같이 Claude가 도구를 쓸 때 한 줄 요약으로 표시 |
| **Permission Prompt** | 도구 실행 직전 | 파일 수정/명령 실행 전 "허락할까요?" 다이얼로그 (y/n 또는 화살표) |
| **Spinner** | 응답 중 | 로고 옆 애니메이션 — "thinking", "still thinking" 등 진행 상태 |

> 💡 모드 표시도 Status Line에 있는데, 모드 자체 설명은 다음 클립(Clip 4)에서 자세히 다룹니다.

#### Status Line 커스터마이징 — `/statusline {요청}`

**Status Line은 기본적으로 비어있어요.** `/statusline` 명령 뒤에 **자연어로 어떻게 보고 싶은지 요청**하세요. `/statusline`만 치면 안 되고, 요청을 같이 적어야 클로드코드가 스크립트 만들어줍니다.

**참고용 예시 (영감만 — 본인이 보고 싶은 형태로 직접 작성하세요)**:

```
/statusline 모델, 현재 폴더, 컨텍스트 퍼센트 보여줘
/statusline 모델 이름이랑 누적 비용 표시해줘
/statusline 컨텍스트 사용량을 progress bar로 시각화해줘
/statusline 미니멀하게 — 모델 이름만
/statusline 모델, 폴더, git 브랜치, 컨텍스트, 비용 전부 다 보여줘
/statusline 모델은 빨간색, 컨텍스트는 노란색으로 표시해줘
```

→ 각 요청마다 클로드코드가 알맞은 스크립트 만들어주고 자동 적용. 마음에 안 들면 다른 요청으로 다시 덮어쓰면 됩니다.

> 📖 더 자세한 옵션: https://code.claude.com/docs/ko/statusline

### EXECUTE

지금 Claude Code 화면에서 직접 해보세요:

1. **UI 요소 위치 확인** — 프롬프트 입력창, Status Line 위치, 응답 영역 등 한 번씩 시선 보내기
2. **본인이 보고 싶은 Status Line 직접 작성**해서 `/statusline` 명령으로 입력 — 위 예시는 참고만, 자유롭게 본인 스타일로 (예: "git만 빼고 다 보여줘" / "지금 모델만 크게" 등 본인 입맛대로)

```
👆 화면 둘러보시고 본인 Status Line 직접 작성해서 적용해보셨으면 "다음"이라고 입력해주세요.
```

---

## Phase 2 — 슬래시 커맨드 핵심

### EXPLAIN

Claude Code에서 `/`로 시작하는 명령들이 있어요. 첫날에 알면 좋은 4개:

| 명령 | 역할 | 언제 쓰나 |
|------|------|----------|
| `/help` | 전체 슬래시 명령 목록 | 뭐가 있는지 모를 때 |
| `/clear` | 대화 기록 초기화 | 다른 주제로 넘어갈 때 |
| `/status` | 현재 설정 한눈에 (모델/계정/연결) | "지금 어떻게 돼있지?" |
| `/usage` | 토큰 사용량 + 비용 + 한도 | 한도 걱정되거나 비용 체크 |

> 💡 다른 명령들도 많은데 (`/compact`, `/resume`, `/rename` 등) `/help`로 한 번 쭉 훑어보면 충분합니다.

### EXECUTE

지금 한 번씩 직접 입력해보세요:

```
/help        ← 어떤 명령들 있는지 쭉 보기
/status      ← 현재 모델·계정·연결 상태
/usage       ← 토큰 / 비용 / 한도
/clear       ← 화면 깨끗해짐
```

```
👆 명령들 한 번씩 눌러보시고, "다음"이라고 입력해주세요.
```

---

## Phase 3 — `/model` 모델 전환 + 디폴트 설정

### EXPLAIN

Claude는 여러 모델이 있어요. 작업 성격에 따라 바꿔 쓰면 좋아요.

| 모델 | 특징 | 언제 |
|------|------|------|
| **Sonnet** (기본) | 빠르고 균형 잡힘 | 대부분의 작업 |
| **Opus** | 가장 똑똑함, 느리고 비쌈 | 복잡한 분석·아키텍처·디버깅 |
| **Haiku** | 초고속, 저렴 | 간단한 조회·요약 |

#### 즉시 전환 (현재 세션만)

```
/model            ← 모델 선택 피커 열림
/model opus       ← 즉시 Opus로 전환
/model sonnet     ← 즉시 Sonnet으로
```

전환되면 Status Line의 모델명이 바뀝니다.

#### 기본값(디폴트) 영구 설정

매번 `/model` 안 치고 싶으면 `settings.json`에 박아두세요:

```bash
~/.claude/settings.json
```

```json
{
  "model": "opus"
}
```

저장 후 Claude Code 재시작하면 디폴트가 Opus로 바뀝니다.

> 📖 공식 문서: https://code.claude.com/docs/ko/model-config

### EXECUTE

1. `/model` 입력 → 피커에서 다른 모델 선택해보기
2. Status Line 보고 모델명 바뀌었는지 확인
3. (선택) 마음에 드는 모델로 `settings.json`에 디폴트 설정

```
👆 모델 한 번 바꿔보시고 "다음"이라고 입력해주세요. (디폴트 설정은 선택)
```

---

## Phase 4 — `/powerup` 인터랙티브 학습

### EXPLAIN

Claude Code에는 자기 자신을 가르쳐주는 도구가 있어요. `/powerup` — 대화형 레슨과 애니메이션 데모로 기능을 학습할 수 있습니다.

```
/powerup
```

실행하면 학습 가능한 토픽 목록이 떠요. 첫 실행자라면 한두 개 같이 해보면 감 잡기 좋습니다.

> 💡 이 강의에서 다 다루지 못하는 깊은 기능들도 powerup으로 직접 배울 수 있어요. 막힐 때마다 `/powerup` 한번 던져보세요.

### EXECUTE

`/powerup` 입력 → 토픽 1~2개 선택해서 따라해보세요.

```
👆 powerup 한번 체험하시고 "다음"이라고 입력해주세요.
```

---

## Phase 5 — 다운로드 폴더 정리 (자율 에이전트 4단계 + 5단계 흐름)

### EXPLAIN

이제 진짜 작업을 시켜봅시다. 클로드코드는 단순 챗봇이 아니라 **자율 에이전트**예요. 대화 한 줄을 받으면 4단계를 알아서 수행합니다.

```
STEP 1 분석    → 폴더 스캔 + 파일 종류별 분류
STEP 2 판단    → 어떻게 정리하면 좋을지 방안 제안
STEP 3 확인    → "정리 실행할까요?" (안전장치)
STEP 4 실행    → 파일 이동 + 정리 완료
```

**핵심 안전장치**: STEP 3에서 "할까요?" 물어봅니다. 함부로 실행 안 해요.

#### "어떻게 해?" 패턴 — 첫 실습부터 박는다

| ❌ 금지 | ✅ 권장 |
|---|---|
| "다운로드 폴더 정리해줘" | "다운로드 폴더 정리하려는데 어떻게 해? 먼저 분석해서 알려줘" |

"해줘"만 던지면 결과만 받고 끝나요. "어떻게 해?" 부터 물어보면 AI가 방법을 먼저 설명해줘요. 이해 → 동의 → 실행. **첫 실습부터 이 습관**.

### EXECUTE

#### 1) 폴더 상태 확인

`AskUserQuestion`으로 사용자에게:

```json
{
  "questions": [{
    "question": "다운로드 폴더에 정리할 파일이 충분히 있나요?",
    "header": "실습 준비",
    "options": [
      {"label": "예 — 내 다운로드 폴더로 진행", "description": "PDF/이미지/엑셀 등 다양한 종류 + 10개 이상 있어야 효과 좋음"},
      {"label": "아니오 — 시연용 mock 파일로 진행", "description": "50개 mock 파일을 ~/Downloads/cc-demo에 자동 생성해드려요 (PDF/이미지/엑셀/문서 mix)"}
    ],
    "multiSelect": false
  }]
}
```

#### 2) 시연용 mock 선택 시 자동 생성

```bash
bash "${SKILL_ROOT}/scripts/make-mockup-downloads.sh"
```

생성 결과:
- 위치: `~/Downloads/cc-demo/` (Mac/Linux/WSL 모두 자동 감지)
- 파일: 50개 (PDF 12 / DOCX 6 / JPG 9 / PNG 6 / XLSX 5 / CSV 2 / ZIP 5 / RAR 1 / 기타 4)

#### 3) 1단계 던지기 → 2단계 구체화 → 3단계 만들기

사용자가 Claude Code에 입력 (Auto 모드 권장):

**내 폴더로 진행**:
```
다운로드 폴더 정리하려는데 어떻게 해? 먼저 분석해서 어떻게 정리하면 좋을지 알려줘
```

**시연용 mock으로 진행**:
```
~/Downloads/cc-demo 정리하려는데 어떻게 해? 먼저 분석해서 어떻게 정리하면 좋을지 알려줘
```

→ Claude가 STEP 1 (분석) + STEP 2 (판단) 출력 → STEP 3 ("실행할까요?") 묻는 단계까지

→ 사용자가 OK → STEP 4 실행

#### 4) 4단계 검증 → 5단계 개선 (5단계 대화 패턴 hook)

기본 정리 끝난 후, 추가로 시켜보세요:

```
정리 결과 보여줘. 빠진 파일 있어?           ← 4단계 검증
PDF 폴더 안 파일들 날짜순으로 다시 정렬해줄래?  ← 5단계 개선
```

> 💡 이 흐름 — **던지기 → 구체화 → 만들기 → 검증 → 개선** — 이게 Part 03 Ch01에서 본 학습할 **대화 5단계 패턴**입니다. 미리 한번 체험해본 거예요.

```
👆 폴더 정리 다 끝나시면 "완료"라고 입력해주세요.
```

---

## QUIZ (Phase 5 끝난 뒤)

```json
{
  "questions": [{
    "question": "Claude Code가 자율 에이전트로서 '안전장치' 역할을 하는 단계는?",
    "header": "자율 에이전트 4단계 퀴즈",
    "options": [
      {"label": "STEP 1 분석", "description": "폴더 스캔 단계"},
      {"label": "STEP 2 판단", "description": "정리 방안 제안 단계"},
      {"label": "STEP 3 확인", "description": "'실행할까요?' 묻는 단계"},
      {"label": "STEP 4 실행", "description": "파일 이동 단계"}
    ],
    "multiSelect": false
  }]
}
```

**정답**: STEP 3 확인
**피드백**: "AI가 함부로 실행하지 않고 'OK 할까요?' 묻는 게 자율 에이전트의 핵심 안전장치예요. 여러분이 동의해야 실행됩니다."

---

## Clip 3 마무리

**1) 결과물 저장**

`50-my-work/Part02-시작하기/실습03-첫실행-폴더정리/` 자동 생성 후 `README.md`에 다음 기록:
- 완료 시각
- 사용 모델 (Sonnet / Opus 등)
- 사용 모드 (Default / Accept-edits 등)
- 정리한 폴더 (`~/Downloads/cc-demo` 또는 본인 다운로드)
- Before/After 요약 (몇 개 → 어떤 폴더 구조)
- 5단계 흐름 (검증/개선까지 했는지)

**2) progress.json 업데이트**

워크스페이스 루트의 `progress.json`:
- `current_clip`: "Clip 3 완료, Clip 4 대기"
- `practice_completed`에 "실습 3" 추가
- `last_activity`: 현재 시각

다음 안내:
```
Clip 3 완료!

✓ 화면 요소 인지 (Status Line, 입력창, 응답, 도구 호출, Permission)
✓ 슬래시 커맨드 3개 (/help, /clear, /compact)
✓ 모델 전환 (/model + 디폴트 설정)
✓ /powerup으로 자기 학습
✓ 다운로드 폴더 정리 — 자율 에이전트 4단계 + 5단계 대화 흐름 체험

다음은 Clip 4 — 4가지 모드 + cc Alias.
/part02 다시 호출하시면 Clip 4 선택할 수 있어요.
```
