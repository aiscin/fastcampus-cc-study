---
name: part04-strengthen
description: "Part 04: 클로드코드 강화하기 (신 커리큘럼 v3.2). 1챕터 4클립 — 플러그인 설치 + GPTaku 3종 체험 (docs-guide / kkirikkiri / vibe-sunsang). BUILD 없음 — 도움 받기 체험 패턴. '/part04', 'Part 04', '강화하기' 요청에 사용."
---

# Part 04: 클로드코드 강화하기

이 스킬이 호출되면 아래 규칙을 반드시 따른다.

---

## 신 커리큘럼 v3.2 — Part 04 구성 (1챕터 / 4클립)

| Ch | Clip | 실습 # | 제목 (PDF 공식 형식) | 유형 | 패턴 |
|---|:-:|:-:|---|---|---|
| **Ch 01 — 플러그인 활용** | **1** | 14 | 플러그인 설치하기 | 이론+실습 | TUI 따라하기 (BUILD 없음) |
|  | **2** | 15 | docs-guide — 공식 문서 기반으로 정확한 답변 받기 | 실습 | 4단계 (BUILD 없음) |
|  | **3** | 16 | kkirikkiri — 자연어로 AI 팀 구성하기 | 실습 | 5단계 (BUILD 없음) |
|  | **4** | 17 | vibe-sunsang — 내 AI 활용 점검받기 | 실습 | 3단계 (BUILD 없음) |

**Part 04 핵심 framing**: 결과물 만들기 X, **플러그인 도움 받기** O. BUILD 5단계 적용 안 함. Part 03(BUILD 적용)과 차이 존재.

---

## References 파일 맵

| Clip | 파일 |
|:-:|---|
| Clip 1 | `references/clip01-plugin-install.md` |
| Clip 2 | `references/clip02-docs-guide.md` |
| Clip 3 | `references/clip03-kkirikkiri.md` |
| Clip 4 | `references/clip04-vibe-sunsang.md` |

---

## 핵심 패턴 — 자동 셋업 → 진행 안내 → 영상 보면서 따라하기 → WRAP

```
[자동 셋업]      스킬이 mkdir + (필요 시) 결과물 cp 자동 실행 + 결과 한 줄 보고
   ↓
[브리핑 + 안내]  플러그인 정의 표·동작 흐름 + 단계 흐름 (한 메시지)
   ↓
[영상 따라]      사용자가 영상 보면서 진행 (스킬 SLEEP)
   ↓ (트리거: 완료 / /wrap / 끝 / 다음 클립)
[WRAP]          파일 검증 + README 자동 + progress.json + 다음 안내
```

각 클립은 자기만의 단계 수 (Clip 01 = TUI 4단계 / Clip 02 = 4단계 / Clip 03 = 5단계 / Clip 04 = 3단계).

### 자동 셋업 의무 (모든 클립)

각 클립 reference 파일에 `## 자동 셋업` 섹션이 있다. 스킬이 클립 reference를 로드한 직후:

1. **reference의 `## 자동 셋업` Bash를 즉시 실행**
   - `mkdir -p ~/fastcampus-cc/50-my-work/Part04-강화하기/실습NN-제목/`
   - 필요 시 이전 결과물 cp
2. **셋업 결과를 한 줄로 보고**
3. **`## XXX 브리핑` (한 줄 정의·동작 흐름·핵심 메시지) + `## 진행 안내` 섹션을 한 메시지로 출력** + SLEEP 모드
   - 브리핑 섹션이 있는 reference: 모든 클립 (clip01 = 플러그인 개념 / clip02 = docs-guide / clip03 = kkirikkiri / clip04 = vibe-sunsang)

### 진행 원칙

1. 시작 시 진행 안내를 한 메시지로 출력 — 학습자가 영상 보기 전 한 번 읽고 시작
2. 자유 실습 중 스킬 개입 X — 사용자가 명시적 도움 요청(`막혔어요`/`도와줘`)할 때만
3. WRAP 트리거: `완료`, `/wrap`, `끝`, `다음 클립`
4. 회고: 자유 입력 (AskUserQuestion 없이)

### AskUserQuestion 사용 위치 (제한)

| 위치 | 용도 |
|---|---|
| SKILL.md 시작 — 클립 선택 | 4 클립 라우팅 |

실습 reference (clip01-clip04)에서는 AskUserQuestion 사용 X. 회고도 자유 입력.

---

## 결과물 저장 규칙 ★

모든 실습 결과물은 `50-my-work/Part04-강화하기/실습{NN}-{제목}/`에 저장.

| Clip | 폴더 |
|:-:|---|
| Clip 1 | `50-my-work/Part04-강화하기/실습14-플러그인설치/` |
| Clip 2 | `50-my-work/Part04-강화하기/실습15-공식문서확인/` |
| Clip 3 | `50-my-work/Part04-강화하기/실습16-AI팀구성/` |
| Clip 4 | `50-my-work/Part04-강화하기/실습17-AI활용점검/` |

WRAP 단계에서 자동 생성:
- 결과물 파일들
- `README.md` — 날짜·모델·모드·진행 기록·핵심 발견/회고
- `progress.json` 업데이트 — 해당 실습 번호 추가

### progress.json 스키마 (이 스킬이 사용·수정하는 키)

| 키 | 타입 | 의미 | 기록 위치 |
|---|---|---|---|
| `current_clip` | string\|null | 진행 중 클립 | 모든 클립 |
| `practice_completed` | array | 완료한 실습 번호 (예: `["실습 14", "실습 15"]`) | 모든 클립 |
| `installed_plugins` | array | 설치한 플러그인 (`["docs-guide", "kkirikkiri", "vibe-sunsang"]`) | Clip 1 |
| `priorities_for_part06` | array | Clip 3 kkirikkiri 결과 — Part 06에서 만들 스킬 청사진 | Clip 3 |
| `current_levels` | object | Clip 4 vibe-sunsang 결과 — v2 6축 (`DECOMP`/`VERIFY`/`ORCH`/`FAIL`/`CTX`/`META`) | Clip 4 |
| `priorities_for_part05` | array | Clip 4 vibe-sunsang 결과 — Part 05 보완 영역 | Clip 4 |
| `completed_parts` | array | 완료한 Part (예: `["Part 03", "Part 04"]`) | Clip 4 (Part 04 마지막) |
| `level` | string | 현재 레벨 ("AI Intermediate" 유지) | Clip 4 |
| `last_activity` | string | ISO 8601 타임스탬프 | 모든 클립 |

---

## 시작

**1단계: progress.json 확인**

워크스페이스 루트의 `~/fastcampus-cc/progress.json`을 Read로 읽는다. 다음 필드 확인:
- `practice_completed`
- `installed_plugins` (Clip 1 완료 여부)
- `current_clip` (재진입용)

각 Clip 1-4가 완료됐는지 매핑:
- Clip 1: `practice_completed`에 "실습 14"
- Clip 2: "실습 15"
- Clip 3: "실습 16"
- Clip 4: "실습 17"

**2단계: 분기 로직**

```
IF current_clip 있음:
   → "Clip N에서 멈춘 게 있어요. 이어서 진행할까요?"
     [이어가기 / 다른 클립 / 처음부터]

ELIF 모든 클립 완료 (4/4):
   → Part 04 완료 메시지 + /part05 안내

ELSE 미진행 클립 있음:
   → 직접 클립 선택 (한 번에 옵션 4개 한도)
```

**3단계: 직접 클립 선택**

```json
{
  "questions": [{
    "question": "어느 클립을 진행할까요?",
    "header": "Part 04 클립",
    "options": [
      {"label": "Clip 1 — 플러그인 설치하기", "description": "TUI로 마켓플레이스 추가 + 3개 설치"},
      {"label": "Clip 2 — docs-guide 공식 문서 답변", "description": "일반 답변 vs docs-guide 5관점 비교 + 클로드코드 시너지"},
      {"label": "Clip 3 — kkirikkiri 자연어로 AI 팀 구성", "description": "Agent Teams를 스킬로 쉽게 + 본인 직무 다관점 진단"},
      {"label": "Clip 4 — vibe-sunsang 사용 패턴 점검", "description": "본인 사용 패턴 + Part 05 보완 영역"}
    ],
    "multiSelect": false
  }]
}
```

옵션은 미진행 클립만, 최대 4개. 이미 완료한 클립은 제외.

선택한 클립의 reference 파일을 읽고 **자동 셋업 → 진행 안내** 출력.

---

### 미진행 클립 매핑 (참고)

| Clip | 실습 # | 완료 키 |
|:-:|:-:|---|
| 1 | 14 | `practice_completed`에 "실습 14" |
| 2 | 15 | "실습 15" |
| 3 | 16 | "실습 16" |
| 4 | 17 | "실습 17" |

---

## Part 04 완료 시 (Clip 4 WRAP 끝나면)

1. progress.json 업데이트:
   - `completed_parts`에 "Part 04" 추가
   - `practice_completed`에 "실습 14-17" 모두 기록 확인
   - `level`: "AI Intermediate" 유지 (Part 06 완료 시 "AI Advanced"로 승급)
   - `current_clip`: null
   - `last_activity`: 현재 시각

2. 완료 안내:
   ```
   Part 04 완료! 클로드코드를 강화하는 플러그인 사용법을 익혔습니다.

   ✓ Clip 1 플러그인 설치 (docs-guide / kkirikkiri / vibe-sunsang)
   ✓ Clip 2 docs-guide — 공식 문서 기반으로 정확한 답변 받기
   ✓ Clip 3 kkirikkiri — 자연어로 AI 팀 구성하기
   ✓ Clip 4 vibe-sunsang — 내 AI 활용 점검받기

   받은 우선순위 + 보완 영역은 progress.json에 기록되어,
   Part 05/06 시작 시 자동으로 참고됩니다.

   다음은 Part 05 — 클로드코드 뜯어보기. /part05 입력하세요.
   ```
