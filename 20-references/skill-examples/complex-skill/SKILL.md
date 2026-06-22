---
name: competitor-monitor
description: "경쟁사 모니터링 리포트를 생성합니다. '/경쟁사', '경쟁사 분석' 요청에 사용."
---

# 경쟁사 모니터링 스킬

이 스킬은 3개 블록으로 구성된다.

## Block 구성

| 블록 | 파일 | 내용 |
|------|------|------|
| Block 1 | `references/block1-collect.md` | 데이터 수집 |
| Block 2 | `references/block2-analyze.md` | 분석 |
| Block 3 | `references/block3-report.md` | 리포트 생성 |

## 순서

### Block 1: 데이터 수집
1. mock-data/ 에서 competitor-urls.md를 읽는다
2. 각 경쟁사의 최근 변화를 확인한다
3. 변화 내용을 정리한다

### Block 2: 분석
1. 수집된 데이터를 비교 분석한다
2. 우리와의 차이점을 정리한다
3. 위협/기회 요소를 분류한다

### Block 3: 리포트
1. 분석 결과를 리포트로 정리한다
2. 액션 아이템 3개를 제안한다
3. my-work/reports/ 에 저장한다

## 결과물

```markdown
# 경쟁사 모니터링 리포트

**작성일**: (자동)

## 주요 변화
(경쟁사별 변화 요약)

## 위협 요소
(우리에게 불리한 변화)

## 기회 요소
(우리가 활용할 수 있는 변화)

## 액션 아이템
1. (구체적 행동)
2. (구체적 행동)
3. (구체적 행동)
```
