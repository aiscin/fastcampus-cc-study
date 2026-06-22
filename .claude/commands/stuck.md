---
name: stuck
description: "에러/문제 해결 가이드 — 어디서 뭐가 안 되는지 빠르게 진단."
---

# /막혔어요

학생이 실습 중 막혔을 때 호출. 빠르게 상황 진단하고 해결 안내.

## 동작

`AskUserQuestion`으로 어디서 막혔는지 물어보고 그 시점에 맞는 해결법 안내.

## 진단 흐름

### Step 1 — 어디서 막혔어요?

```json
{
  "questions": [{
    "question": "어디서 막히셨어요?",
    "header": "문제 진단",
    "options": [
      {"label": "설치 (Part 02 클립 1/2)", "description": "Homebrew, WSL, Claude Code 설치 단계"},
      {"label": "첫 실행 / 폴더 정리 (실습 3)", "description": "cc 안 켜짐, 분석 결과 이상 등"},
      {"label": "모드 / Alias (실습 4)", "description": "Shift+Tab, cc alias 안 됨"},
      {"label": "다른 실습 (Part 03 이상)", "description": "데이터 분석, 보고서, 카드뉴스 등"},
      {"label": "자유 입력", "description": "아래에 직접 설명할게요"}
    ],
    "multiSelect": false
  }]
}
```

### Step 2 — 구체 진단

선택한 단계에 따라:
- **설치**: 어떤 명령에서 어떤 에러? OS는? → 클립 1/2의 "예상 이슈 표" 참조 + 안티그래비티 챗에 물어보도록 안내
- **첫 실행**: cc 작동 여부 → 안 되면 alias 미설정 / claude path 문제
- **모드/Alias**: Shift+Tab 반응 / source 명령 후 재시도
- **Part 03 이상**: 해당 Part 가이드 스킬 (`/part03` 등) 호출 안내
- **자유 입력**: 사용자 설명 받고 맞춤 진단

## 핵심 원칙

- 학생을 책망하지 않음 — "막히는 게 정상이에요"
- 한 번에 한 단계씩 안내 — 풀 솔루션 던지기 X
- 안 되면 안티그래비티 챗 / `/help` / 영상 다시 보기 등 폴백 옵션 제시
- 마지막 옵션: "그래도 안 되면 슬랙 커뮤니티에 올려보세요" (해당되면)
