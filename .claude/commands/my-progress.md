---
name: my-progress
description: "현재 진행률 확인. progress.json을 읽고 보기 좋게 정리."
---

# /my-progress

학생의 현재 강의 진행 상태를 한눈에 보여줍니다.

## 동작

1. `progress.json` 읽기
2. 다음 정보를 보기 좋게 정리해 출력:
   - 현재 레벨
   - 완료한 Part 개수 / 전체
   - 완료한 실습 번호들
   - 만든 자산 (스킬/커맨드/hook)
   - 마지막 활동일

## 출력 예시

```
📊 진행 상태

레벨: AI Starter (Lv.1)

완료한 Part: 1/9
✓ Part 01 인트로
○ Part 02 시작하기 (진행 중 — 실습 3 완료)
○ Part 03 ~ 09 미시작

완료한 실습: 3개 / 40개
✓ 실습 1 (Mac 환경 설치)
✓ 실습 2 (Windows 환경 설치 - 영상 시청만)
✓ 실습 3 (첫 실행 - 폴더 정리)

만든 자산:
- 스킬: 0개
- 커맨드: 0개
- hook: 0개

마지막 활동: 2026-04-27 14:30
```

## 메타

- progress.json이 없으면: "아직 시작 전이에요. /part02 입력하시면 시작합니다." 안내
- 완료 기준: progress.json의 `practice_completed` 배열에 추가됐는지
