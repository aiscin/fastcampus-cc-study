# Clip 04 — vibe-sunsang 사용 패턴 점검

> Part 04 / Ch 01 / Clip 04 (실습 17) | 예상 시간: ~17분
> 결과물: 본인 사용 패턴 진단 리포트 + Part 05 시작 전 보완 영역 1-2개
> 패턴: **BUILD 없음 — 도움 받기 시연** (Part 04 전체 공통, 마지막 클립)

---

## 자동 셋업

```bash
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

WORK_DIR="$ROOT/50-my-work/Part04-강화하기/실습17-AI활용점검"
mkdir -p "$WORK_DIR"

echo "✓ $WORK_DIR 준비 완료"
```

셋업 결과 한 줄 보고 후 아래 **vibe-sunsang 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## vibe-sunsang 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 한 줄 | 본인 대화 로그 → 분석 → 6축 레벨·강점·약점·다음 한 걸음 진단 |
| 강점 | 객관적 셀프 진단 (혼자서는 안 보이는 사용 패턴) |
| 호출 | `/vibe-sunsang 시작` → `변환` → `멘토링` |
| 산출물 | 진단 리포트 (v2 6축 레벨 + 강점·약점·안티패턴 + 다음 한 걸음) |

### 동작 흐름

```
[학습자]
   ↓
1. 시작 (~/vibe-sunsang/ 워크스페이스 1회 설정)
   ↓
2. 변환 (클로드코드 JSONL 로그 → 마크다운)
   ↓
3. 멘토링 또는 성장 (변환된 로그 분석 + 코칭)
   ↓
4. 진단 리포트 (6축 레벨 + 강점·약점 + 다음 한 걸음)
```

### v2 6축 레벨 시스템

| 축 | 측정 내용 |
|---|---|
| DECOMP (작업 분해) | 큰 작업을 작은 단위로 쪼개는 능력 |
| VERIFY (검증) | 받은 결과를 깊이 있게 점검 |
| ORCH (오케스트레이션) | 도구·에이전트를 조합해서 활용 |
| FAIL (실패 복구) | 막혔을 때 다시 풀어가는 능력 |
| CTX (컨텍스트 제공) | 배경·제약·예시 충분 제공 |
| META (메타 인지) | 본인 사용 패턴 자기 인식 |

각 축 0.5 단위 7단계로 진단.

### 명령

| 명령 | 동작 |
|---|---|
| `/vibe-sunsang 시작` | 첫 사용 시 워크스페이스 설정 |
| `/vibe-sunsang 변환` | 이번 주 대화 로그 변환 |
| `/vibe-sunsang 멘토링` | AI 활용 패턴 코칭 |
| `/vibe-sunsang 성장` | 성장 리포트 (장기 추세) |
| `/vibe-sunsang 지식` | 6축 시스템·개념 학습 |

### 핵심 메시지

> Part 02부터 여기까지 쌓인 본인 대화 로그를 6축으로 객관 진단.
> 받은 보완 영역 1-2개가 다음 학습 우선순위가 됨.

---

## 진행 안내

```
✓ 50-my-work/Part04-강화하기/실습17-AI활용점검/ 준비 완료

오늘 할 거 (~17분) — Part 04 마지막 클립
- vibe-sunsang으로 내 클로드코드 사용 패턴 진단받기
- Part 02~04 로그 분석 → 6축 레벨 + 강점·약점·안티패턴
- Part 05 보완 영역 1-2개 받기
- 영상 보면서 진행하시고 끝나면 `완료` 또는 `/wrap` 입력

3단계 흐름:
1. /vibe-sunsang 시작     (처음 한 번만 — 워크스페이스 설정)
2. /vibe-sunsang 변환     (대화 로그 → 마크다운)
3. /vibe-sunsang 멘토링   (진단 + 코칭)
```

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| `/vibe-sunsang` 인식 안 됨 | "/plugin Installed 탭 확인하고 vibe-sunsang 재설치 알려줘" |
| 시작 단계 멈춤 | "권한 요청 와도 Y로 진행" |
| 변환 결과 너무 적음 | 정상 — 더 사용 후 다시 가능 |
| 멘토링 결과 일반적 | 자유 실습 더 하고 재시도 |
| 6축 의미 모름 | `/vibe-sunsang 지식`으로 6축 상세 학습 |
| 보완 영역 5개+ | "1-2개만 추려달라" 재요청 |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행. 이 클립이 Part 04 마지막이라 WRAP 시 Part 04 완료 처리도 함께.

---

## WRAP 자동 처리

### 1. 결과물 검증 + 복사

```bash
ROOT="$HOME/fastcampus-cc"
WORK_DIR="$ROOT/50-my-work/Part04-강화하기/실습17-AI활용점검"
VS_DIR="$HOME/vibe-sunsang"

if [ -d "$VS_DIR/reports" ]; then
  cp "$VS_DIR/reports"/mentor-*.md "$WORK_DIR/" 2>/dev/null
  echo "✓ vibe-sunsang 리포트 복사 완료"
fi
```

mentor-report.md + priorities-for-part05.md 존재 확인.

### 2. README.md 자동 작성

```markdown
# 실습 17 — vibe-sunsang으로 사용 패턴 점검

- 완료 시각: {ISO8601}
- 모델·모드 정보

## vibe-sunsang 정의 & 동작 흐름

### 한 줄 정의
| 항목 | 내용 |
|---|---|
| 한 줄 | 본인 대화 로그 → 분석 → 6축 레벨·강점·약점·다음 한 걸음 진단 |
| 강점 | 객관적 셀프 진단 (혼자서는 안 보이는 사용 패턴) |
| 호출 | /vibe-sunsang 시작 → 변환 → 멘토링 |
| 산출물 | 진단 리포트 (v2 6축 레벨 + 강점·약점·안티패턴 + 다음 한 걸음) |

### 동작 흐름
1. 시작 — 워크스페이스 설정 (1회만, ~/vibe-sunsang/ 생성 + 프로젝트 분류)
2. 변환 — 클로드코드 JSONL 로그 → 마크다운 변환
3. 멘토링 또는 성장 — 변환된 로그 분석 + 코칭
4. 진단 리포트 (6축 레벨 + 강점·약점 + 다음 한 걸음)

### 명령
- `/vibe-sunsang 시작`     — 첫 사용 시 워크스페이스 설정
- `/vibe-sunsang 변환`     — 이번 주 대화 로그 변환
- `/vibe-sunsang 멘토링`   — AI 활용 패턴 코칭
- `/vibe-sunsang 성장`     — 성장 리포트 (장기 추세)
- `/vibe-sunsang 지식`     — 6축 시스템·개념 학습

## v2 6축 레벨 시스템
| 축 | 측정 내용 |
|---|---|
| DECOMP (작업 분해) | 큰 작업을 작은 단위로 쪼개는 능력 |
| VERIFY (검증) | 받은 결과를 깊이 있게 점검 |
| ORCH (오케스트레이션) | 도구·에이전트를 조합해서 활용 |
| FAIL (실패 복구) | 막혔을 때 다시 풀어가는 능력 |
| CTX (컨텍스트 제공) | 배경·제약·예시 충분 제공 |
| META (메타 인지) | 본인 사용 패턴 자기 인식 |

각 축 0.5 단위 7단계로 진단.

## 워크스페이스 유형 (참고)
- Builder / Explorer / Designer / Operator
- vibe-sunsang이 프로젝트별로 자동 분류

## 진단 결과

### 6축 레벨 (v2)
- DECOMP : Lv {x}
- VERIFY : Lv {x}
- ORCH   : Lv {x}
- FAIL   : Lv {x}
- CTX    : Lv {x}
- META   : Lv {x}

### 강점·약점·안티패턴
- 강점: {1줄}
- 약점: {1줄}
- 안티패턴: {1줄}

## Part 05 시작 전 보완 영역
1순위: {보완 영역} → {해당 Part 05 클립}
2순위: {보완 영역} → {해당 Part 05 클립}

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트 (Part 04 완료 처리 포함)

```json
{
  "practice_completed": [..., "실습 17"],
  "current_levels": {
    "DECOMP": 3.5,
    "VERIFY": 2.5,
    "ORCH":   3.0,
    "FAIL":   3.5,
    "CTX":    3.0,
    "META":   4.0
  },
  "priorities_for_part05": [
    {"rank": 1, "area": "{보완 영역}", "target_clip": "Part 05 실습 18"},
    {"rank": 2, "area": "{보완 영역}", "target_clip": "Part 05 실습 21"}
  ],
  "completed_parts": [..., "Part 04"],
  "level": "AI Intermediate",
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

`priorities_for_part05`는 Part 05 시작 시 자동으로 참고됨.

### 4. 회고 한 줄

> "이번 클립에서 가장 인상적이었던 진단 한 줄로 적어주세요."

### 5. Part 04 완료 안내

```
실습 17 완료. Part 04 마무리입니다.

✓ Clip 01 플러그인 설치 (docs-guide / kkirikkiri / vibe-sunsang)
✓ Clip 02 docs-guide — 공식 문서 기반 정확한 답변 받기
✓ Clip 03 kkirikkiri — 자연어로 AI 팀 구성하기
✓ Clip 04 vibe-sunsang — 내 AI 활용 점검받기

받은 우선순위 + 보완 영역은 progress.json에 기록되어,
Part 05/06 시작 시 자동으로 참고됩니다.

다음은 Part 05 — 클로드코드 뜯어보기. /part05 입력하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 번에 출력하고 사용자가 영상 보면서 직접 진행
- **BUILD 없음**: Part 04 전체 공통 — 도움 받기 체험이라 5단계 적용 X
- **자유 실습 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **변동성 인정**: 본인 사용 패턴에 따라 결과 다름. 흐름만 일관
- **Part 04 완료 처리**: 이 클립이 마지막이라 WRAP에서 `completed_parts`에 "Part 04" 추가
