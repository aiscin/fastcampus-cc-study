# AskUserQuestion 퀴즈 형식 가이드

> Part 가이드 스킬에서 퀴즈/질문을 낼 때 이 형식을 따릅니다.

---

## 기본 형식

```json
{
  "questions": [{
    "question": "질문 내용",
    "header": "헤더 (카테고리/상황)",
    "options": [
      {"label": "선택지 1", "description": "부연 설명"},
      {"label": "선택지 2", "description": "부연 설명"},
      {"label": "선택지 3", "description": "부연 설명"}
    ],
    "multiSelect": false
  }]
}
```

---

## 퀴즈 유형별 예시

### 이해도 확인 퀴즈

```json
{
  "question": "CLAUDE.md는 어떤 역할을 하나요?",
  "header": "Part 3 퀴즈",
  "options": [
    {"label": "AI에게 나를 알려주는 파일", "description": ""},
    {"label": "코드를 실행하는 파일", "description": ""},
    {"label": "설정을 저장하는 파일", "description": ""},
    {"label": "잘 모르겠어요", "description": ""}
  ]
}
```

### 업무 유형 선택 (맞춤형 실습)

```json
{
  "question": "어떤 업무에 특화된 실습을 하고 싶으세요?",
  "header": "맞춤 실습",
  "options": [
    {"label": "문서 작성", "description": "보고서, 기획서, 정리 문서"},
    {"label": "데이터 분석", "description": "수치 분석, 차트, 비교 정리"},
    {"label": "콘텐츠 제작", "description": "블로그, SNS, 카드뉴스"},
    {"label": "종합", "description": "특정 분야 없이 전반적으로"}
  ]
}
```

### 실습 결과 확인

```json
{
  "question": "실습 결과가 어떤가요?",
  "header": "결과 확인",
  "options": [
    {"label": "잘 동작한다", "description": "예상대로 결과가 나왔어요"},
    {"label": "에러가 난다", "description": "오류 메시지가 나와요"},
    {"label": "결과가 기대와 다르다", "description": "동작은 하는데 원하는 게 아니에요"},
    {"label": "아직 안 해봤다", "description": ""}
  ]
}
```

---

## 원칙

1. 선택지는 3~6개 사이로 유지
2. "잘 모르겠어요" 또는 "기타" 선택지를 항상 포함
3. description은 선택에 도움이 될 때만 작성 (불필요하면 빈 문자열)
4. multiSelect는 기본 false (복수 선택이 의미 있을 때만 true)

---

## 자유 입력 폴백 규칙

AskUserQuestion 응답이 없거나 불명확한 경우:

```
처리 순서:
1. 입력이 없거나 불명확하면 기본값을 제시한다
2. "입력이 없어서 [기본값]으로 진행합니다. 괜찮으세요?" 안내
3. 수강생이 동의하면 기본값으로 진행
4. 수강생이 다른 값을 원하면 그 값으로 변경 후 진행
```

**기본값 기준:**
- 실습 주제 선택: "종합" 또는 가장 범용적인 옵션
- 운영체제 확인: "Mac"으로 가정 (가장 일반적)
- 결과물 형식: HTML 파일 (브라우저에서 바로 확인 가능)

**절대 하지 않는 것:** 입력이 없다고 무한 대기하거나 같은 질문을 반복하지 않는다.
