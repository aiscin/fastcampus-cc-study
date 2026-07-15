---
description: 오늘의 메일·일정·뉴스를 한 번에 모아 아침 브리핑을 만든다 (morning-briefing 스킬 실행)
---

# /morning-briefing

morning-briefing 스킬을 즉시 실행한다. 자연어("모닝 브리핑") 대신 명시적으로 부를 때 쓴다.

## 실행
1. morning-briefing 스킬(`.claude/skills/morning-briefing/SKILL.md`)의 워크플로우를 그대로 따른다.
2. STEP 1 `scripts/gather.py`로 메일·일정 수집 → STEP 2 daily-news 재호출로 뉴스 → STEP 3 정리 → STEP 4 대화 브리핑 + md 저장.
3. 인수(`$ARGUMENTS`)가 있으면 참고한다:
   - 날짜 지정(예: "어제") → 해당 날짜 기준으로 일정/저장 파일명 조정.
   - "메일만" / "뉴스만" → 해당 소스만 브리핑.
   - 없으면 오늘 기준 전체 3소스 브리핑.

$ARGUMENTS
