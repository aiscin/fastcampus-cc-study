---
name: weekly-report
description: "주간보고서를 자동으로 생성합니다. '/주간보고', '주간보고서' 요청에 사용."
---

# 주간보고서 생성 스킬

이 스킬이 호출되면 아래 순서로 주간보고서를 생성한다.

## 순서

1. 이번 주 작업 내용을 질문한다
2. 답변을 기반으로 주간보고서를 생성한다
3. 결과를 my-work/reports/ 에 저장한다

## 질문

AskUserQuestion으로 아래 질문을 한다:

```json
{
  "questions": [{
    "question": "이번 주에 한 일을 알려주세요 (여러 개 선택 가능)",
    "header": "주간보고서",
    "options": [
      {"label": "회의/미팅", "description": "참석한 회의나 미팅"},
      {"label": "문서 작성", "description": "작성하거나 수정한 문서"},
      {"label": "프로젝트 진행", "description": "프로젝트 관련 업무"},
      {"label": "기타", "description": "직접 입력"}
    ],
    "multiSelect": true
  }]
}
```

## 보고서 형식

```markdown
# 주간 업무 보고서

**보고자**: (CLAUDE.md에서 확인)
**기간**: (이번 주 월~금 자동 계산)

## 이번 주 주요 성과
(답변 기반 자동 생성)

## 다음 주 계획
(답변에서 추론)

## 이슈/건의사항
(있으면 기재, 없으면 "없음")
```
