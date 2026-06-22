---
name: check-level
description: "현재 레벨 확인 — AI Starter ~ AI Native."
---

# /check-level

현재 학생 레벨과 다음 레벨까지 필요한 진도를 보여줍니다.

## 4단계 레벨 시스템

| Lv | 이름 | 달성 조건 |
|----|------|----------|
| 1 | **AI Starter** | 시작 (지금) |
| 2 | **AI Intermediate** | Part 03 완료 — 대화로 결과물 만드는 사람 |
| 3 | **AI Advanced** | Part 06 완료 — 직접 스킬 만드는 사람 |
| 4 | **AI Native** | Part 07 완료 — AI 없이 못 사는 사람 |

## 동작

1. `progress.json`의 `level` + `completed_parts` 읽기
2. 현재 레벨 표시 + 한 줄 설명
3. 다음 레벨까지 남은 Part 안내

## 출력 예시

```
🎯 현재 레벨: AI Starter (Lv.1)

지금은 시작 단계 — 환경 세팅 중이에요.

다음 레벨: AI Intermediate (Lv.2)
- 조건: Part 03 완료
- 남은 것: Part 02, Part 03

진행하려면: /part02
```

## 메타

각 레벨 도달 시 축하 메시지 + 다음 단계 hook.
