---
name: part03-experience
description: "Part 03: 클로드코드 체험하기 (신 커리큘럼 v3). 4챕터 10클립 — Ch 01 이론 1 + Ch 02 데이터 3 + Ch 03 콘텐츠 3 + Ch 04 웹사이트 3. BUILD 5단계 + 자유 실습 + WRAP 패턴. '/part03', 'Part 03', '체험하기' 요청에 사용."
---

# Part 03: 클로드코드 체험하기

이 스킬이 호출되면 아래 규칙을 반드시 따른다.

---

## 신 커리큘럼 v3 — Part 03 구성 (4챕터 / 10클립)

| Ch | Clip | 실습 # | 제목 | 유형 | 패턴 |
|---|:-:|:-:|---|---|---|
| **Ch 01 — 이론** | **1** | — | 대화 패턴 5단계 | 이론 | 5단계 × (EXPLAIN+CHECK) + 시나리오 + BUILD 매핑 |
| **Ch 02 — 데이터** | **2** | 5 | 데이터 분석 | 실습 | BUILD 5단계 (B→U→I→L→D) + WRAP |
|  | **3** | 6 | 보고서 작성 | 실습 | 동일 |
|  | **4** | 7 | 대시보드 만들기 | 실습 | 동일 |
| **Ch 03 — 콘텐츠** | **5** | 8 | 자료 리서치 | 실습 | 동일 |
|  | **6** | 9 | 카드뉴스 만들기 | 실습 | 동일 |
|  | **7** | 10 | 리모션 영상 | 실습 | 동일 |
| **Ch 04 — 웹사이트** | **8** | 11 | 포트폴리오 기획 | 실습 | 동일 |
|  | **9** | 12 | 포트폴리오 수정 | 실습 | 동일 |
|  | **10** | 13 | Vercel 배포 | 실습 | 동일 (절차적) |

---

## References 파일 맵

| Clip | 파일 |
|:-:|---|
| Clip 1 | `references/clip01-conversation-pattern.md` |
| Clip 2 | `references/clip02-data-analysis.md` |
| Clip 3 | `references/clip03-report.md` |
| Clip 4 | `references/clip04-dashboard.md` |
| Clip 5 | `references/clip05-research.md` |
| Clip 6 | `references/clip06-cardnews.md` |
| Clip 7 | `references/clip07-video.md` |
| Clip 8 | `references/clip08-portfolio-plan.md` |
| Clip 9 | `references/clip09-portfolio-fix.md` |
| Clip 10 | `references/clip10-vercel-deploy.md` |

---

## 핵심 패턴 — 자동 셋업 → 안내 → 영상 보면서 따라하기 → WRAP

이론 클립(Clip 1)을 제외한 모든 실습 클립은 다음 흐름:

```
[자동 셋업]  스킬이 mkdir + 이전 클립 결과물 cp 자동 실행 + 결과 한 줄 보고
   ↓
[안내]      오늘 할 거 + STEP 1~5 흐름 (한 메시지)
   ↓
[영상 따라]  학생이 영상 보면서 STEP 1~5 진행 (스킬 SLEEP)
   ↓ (트리거: 완료 / /wrap / 끝 / 다음 클립)
[WRAP]      파일 검증 + README 자동 + progress.json + 다음 안내
```

5 STEP 흐름은 BUILD 1:1 매핑 (1 셋업 → 2 B질문 → 3 U기획 → 4 I만들기 → 5 L+D검토수정). 스킬은 단계별로 끊어가며 묻지 않음 — **자동 셋업자 + 안내자 + 결과 정리자** 역할만.

### 자동 셋업 의무 (실습 클립 전체 — Clip 2~10)

**각 클립 reference 파일에는 `## 자동 셋업` 섹션이 있다.** 스킬이 클립 reference를 로드한 직후, 다음 순서로 동작한다:

1. **reference의 `## 자동 셋업` 섹션 안 Bash 코드 블록을 Bash 도구로 즉시 실행** — 학생에게 명령을 보여주는 게 아니라 스킬이 직접 실행
   - `mkdir -p ~/fastcampus-cc/my-work/실습NN-제목/`
   - 이전 클립 결과물 cp (있으면)
   - sample_csv·이미지 등 강의 자료 폴백 cp (필요 시 `~/fastcampus-cc/40-mock-data/`에서)
2. **셋업 결과를 학생에게 한 줄로 보고** — 어떤 폴더 만들었고 어떤 파일 가져왔는지. 누락된 게 있으면 "⚠" 표시 + 안내
3. **그 다음에 `## 진행 안내` 섹션을 한 메시지로 출력** + SLEEP 모드로 전환

**셋업이 실패해도 진행 안내는 계속 출력** — 학생이 막히면 그때 "도와줘"로 되돌아옴.

**금지**:
- 학생에게 mkdir / cp 명령을 직접 치라고 시키지 말 것 (자동 셋업이 처리)
- 자동 셋업 Bash 실행을 생략하고 진행 안내만 출력하지 말 것

### 진행 원칙

1. **시작 시 전체 흐름을 한 메시지로 안내** — BUILD 5단계 핵심 한 줄씩(B/U/I/L/D) + 시작 4단계(폴더·자료·CC 실행·완료 트리거)
2. **자유 실습 중 스킬 개입 X** — 학생이 명시적으로 도움 요청(`막혔어요`/`도와줘`)할 때만 짧은 도움 안내
3. **WRAP 트리거**: `완료`, `/wrap`, `끝`, `다음 클립`
4. **회고**: 자유 입력 (AskUserQuestion 없이 — "한 줄 회고 입력해주세요")

### AskUserQuestion 사용 위치 (제한)

| 위치 | 용도 |
|---|---|
| SKILL.md 시작 — 챕터 선택 (1차) | 4 챕터 라우팅 |
| SKILL.md — 클립 선택 (2차) | 챕터 선택 후 클립 분기 |
| 이론 reference (clip01) — CHECK 퀴즈 | 5단계 EXPLAIN+CHECK 5개 + BUILD 매핑 + 종합 (총 7개) |

**실습 reference (clip02-clip10)에서는 AskUserQuestion 사용 X.** 회고도 자유 입력으로 받음.

### 일관성 vs 자율성 양립 원리

| 변수 | 학생마다 다름 | 스킬이 일관되게 잡음 |
|------|:-:|---|
| 주제·소재·BUILD 진행 방식 | ✓ | — |
| 결과물 저장 위치·README 형식 | — | ✓ (`my-work/실습NN-.../`) |
| 진도 추적 | — | ✓ (`progress.json`) |
| 다음 클립 연결 안내 | — | ✓ (WRAP 끝에 자동) |

### AskUserQuestion 공통 운영 규칙 (모든 CHECK·BUILD 호출)

1. **옵션 개수 한도** ⚠️ 도구 강제: `options` 배열은 **2~4개**. 5개 이상이면 InputValidationError로 호출 거부됨.
2. **자유 입력 옵션 추가 금지**: 도구가 자동으로 "Other" 빌트인 옵션을 항상 제공. 별도로 `{"label": "자유 입력", ...}` 라인을 추가하면 한도(4개)만 낭비. 사용자는 Other를 통해 자유 텍스트 입력 가능.
3. **셔플**: `options` 배열을 호출 직전 무작위로 섞어서 제시. 정답·동일 옵션이 항상 같은 위치에 오면 안 됨. "강사와 동일" 메타 옵션은 셔플 대상에서 제외하고 항상 마지막에 고정.
4. **정답 매칭**: 인덱스(②/③) 금지. 항상 라벨 텍스트로 비교. 응답 라벨은 NFC 정규화 + 트림 후 비교.
5. **한글 안전성** (깨짐 방지):
   - 모든 `question`/`header`/`label`/`description` 호출 직전 NFC 정규화
   - 제로폭 문자(U+200B 등)·smart quotes·비표준 공백 제거 (sanitize 통과 필수)
   - 이모지 절대 금지 (옵션 라벨에서 깨짐 사고 잦음)
   - 길이: `header` 한글 12자 / `label` 40자 / `description` 60자 이내
   - **예외**: 이론 클립의 CHECK 퀴즈 정답 옵션처럼 학습 의미상 더 길어야 하는 경우 `label` 80자까지 허용 (BUILD 단계 옵션은 40자 엄수)
   - 빈 `description` 키 생략 (`""` 금지)
   - 줄바꿈·탭 금지, 한 줄 텍스트만
6. **fallback**: 한글 깨짐 발생 시 라벨을 `"A. 짧은 단어"` `"B. 짧은 단어"` 형태로 단축 후 재호출.

---

## 결과물 저장 규칙 ★

모든 실습 결과물은 `my-work/실습{NN}-{제목}/`에 저장.

| Clip | 폴더 |
|:-:|---|
| Clip 2 | `my-work/실습05-데이터분석/` |
| Clip 3 | `my-work/실습06-보고서작성/` |
| Clip 4 | `my-work/실습07-대시보드/` |
| Clip 5 | `my-work/실습08-자료리서치/` |
| Clip 6 | `my-work/실습09-카드뉴스/` |
| Clip 7 | `my-work/실습10-리모션영상/` |
| Clip 8 | `my-work/실습11-포트폴리오기획/` |
| Clip 9 | `my-work/실습12-포트폴리오수정/` |
| Clip 10 | `my-work/실습13-Vercel배포/` |

WRAP 단계에서 자동 생성:
- 결과물 파일들
- `README.md` — 날짜, 모델, 모드, BUILD 단계별 선택 기록, 핵심 발견/회고
- `progress.json` 업데이트 — 해당 실습 번호 추가
- **회고 AskUserQuestion** — 4 옵션 + 자유 입력 (인상적 발견·근거 효과·교차 검증·자유) → README "핵심 발견"에 기록

### progress.json 스키마 (이 스킬이 사용·수정하는 키)

| 키 | 타입 | 의미 |
|---|---|---|
| `current_clip` | string\|null | 진행 중 클립. WRAP 완료 시 null |
| `practice_completed` | array | 완료한 실습 번호 (예: `["실습 5", "실습 6"]`) |
| `theory_completed` | array | 완료한 이론 클립 (예: `["Part03-Clip1-대화패턴5단계"]`) |
| `completed_parts` | array | 완료한 Part (예: `["Part 03"]`) |
| `level` | string | 현재 레벨 ("AI Starter" → "AI Intermediate") |
| `last_activity` | string | ISO 8601 타임스탬프 |
| `deployed_url` | string | (선택) Clip 10 Vercel 배포 URL |

---

## 시작

**1단계: progress.json 확인 — 진행 상태 파악**

워크스페이스 루트의 `~/fastcampus-cc/progress.json`을 Read로 읽는다. 다음 필드 확인:
- `theory_completed`: 완료한 이론 클립 (예: `["Part03-Clip1-대화패턴5단계"]`)
- `practice_completed`: 완료한 실습 (예: `["실습 5", "실습 6"]`)
- `current_clip`: 진행 중 클립 (재진입용)

각 Clip 1-10이 완료됐는지 매핑:
- Clip 1: `theory_completed`에 "Part03-Clip1" 포함 여부
- Clip 2-10: `practice_completed`에 "실습 5"~"실습 13" 포함 여부

**2단계: 분기 로직**

```
IF current_clip 있음:
   → "Clip N에서 멈춘 게 있어요. 이어서 진행할까요? 아니면 다른 클립 시작?"
     [이어가기 / 다른 클립 / 처음부터]

ELIF 모든 클립 완료 (10/10):
   → Part 03 완료 메시지 + /part04 안내

ELIF 미진행 클립 4개 이하:
   → 직접 클립 선택 (한 번에 클립 4개 옵션)

ELSE 미진행 클립 5개 이상:
   → 1차: "다음 추천 / 챕터 묶음 / 처음부터" 3 옵션
   → 2차: 선택에 따라 분기
```

**3단계: 직접 클립 선택 (미진행 4개 이하)**

미진행 클립 목록을 그대로 옵션으로 (각 옵션에 진행 상태·예상 시간 명시):

```json
{
  "questions": [{
    "question": "어느 클립을 진행할까요?",
    "header": "남은 클립",
    "options": [
      {"label": "Clip N — {제목} (~분)", "description": "{한 줄 설명}"}
    ],
    "multiSelect": false
  }]
}
```

옵션은 미진행 클립만, 최대 4개. 5개 이상이면 4단계로.

**4단계: 4개 초과 시 라우팅 (다음 추천 / 챕터 / 처음)**

```json
{
  "questions": [{
    "question": "Part 03 — 어떻게 진행할까요?",
    "header": "Part 03 시작",
    "options": [
      {"label": "다음 진행: Clip N — {제목}", "description": "진행 상태 기반 다음 추천 클립"},
      {"label": "챕터로 보기", "description": "Ch 01 이론 / Ch 02 데이터 / Ch 03 콘텐츠 / Ch 04 웹사이트 중 선택"},
      {"label": "특정 클립 직접 — 번호 입력", "description": "Clip 1-10 중 직접 번호 입력"}
    ],
    "multiSelect": false
  }]
}
```

선택 처리:
- "다음 진행" → 그 클립 reference 바로 읽기
- "챕터로 보기" → 5단계 (챕터 선택)
- "특정 클립 직접" → 자유 입력으로 번호 받음 → 해당 reference 읽기

**5단계: 챕터 선택 (4단계에서 "챕터로 보기" 선택 시만)**

미진행 클립 있는 챕터만 표시 (각 챕터 라벨에 진도 표기 — 예: "Ch 02 데이터 [1/3 진행]"):

```json
{
  "questions": [{
    "question": "어느 챕터로?",
    "header": "챕터 선택",
    "options": [
      {"label": "Ch 01 이론 [상태]", "description": "대화 패턴 5단계"},
      {"label": "Ch 02 데이터 [N/3]", "description": "분석 → 보고서 → 대시보드"},
      {"label": "Ch 03 콘텐츠 [N/3]", "description": "리서치 → 카드뉴스 → 영상"},
      {"label": "Ch 04 웹사이트 [N/3]", "description": "포트폴리오 기획 → 수정 → 배포"}
    ],
    "multiSelect": false
  }]
}
```

이미 모두 완료한 챕터는 옵션에서 제외 (한도 4개 내에서 자동 정리).

**6단계: 챕터 안 클립 선택 (5단계 후, 미완료 클립만)**

해당 챕터에서 미완료 클립만 옵션. 챕터당 최대 3 클립 + 1 메타 = 4 한도 충족.

선택한 클립의 reference 파일을 읽고 진행 안내를 출력한다.

---

### 미진행 클립 매핑 (참고)

| Clip | 실습 # | 완료 키 |
|:-:|:-:|---|
| 1 (이론) | — | `theory_completed`에 "Part03-Clip1-대화패턴5단계" |
| 2 | 5 | `practice_completed`에 "실습 5" |
| 3 | 6 | "실습 6" |
| 4 | 7 | "실습 7" |
| 5 | 8 | "실습 8" |
| 6 | 9 | "실습 9" |
| 7 | 10 | "실습 10" |
| 8 | 11 | "실습 11" |
| 9 | 12 | "실습 12" |
| 10 | 13 | "실습 13" |

---

## Part 03 완료 시 (Clip 10 WRAP 끝나면)

1. progress.json 업데이트:
   - `completed_parts`에 "Part 03" 추가
   - `practice_completed`에 "실습 5-13" 기록
   - `level`: "AI Starter" → "AI Intermediate" 승급
   - `current_clip`: null
   - `last_activity`: 현재 시각

2. 완료 안내:
   ```
   Part 03 완료! AI Intermediate로 승급했습니다.

   ✓ Ch 01 이론: 대화 패턴 5단계 체득
   ✓ Ch 02 데이터: 분석 → 보고서 → 대시보드
   ✓ Ch 03 콘텐츠: 리서치 → 카드뉴스 → 영상
   ✓ Ch 04 웹사이트: 기획 → 수정 → Vercel 배포

   결과물 7개 + 공개 URL 1개를 손에 쥐었습니다.

   다음은 Part 04 — 플러그인으로 능력 강화. /part04 입력하세요.
   ```
