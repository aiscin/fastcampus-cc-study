# AI 에이전트 워크스페이스 하네스 — 원리 표준 (Export Edition)

> 목적 특화 AI 에이전트 워크스페이스(Claude Code 기준)를 설계할 때 적용하는 원리 표준.

## 구성

| # | 문서 | 적용 레벨 | 한 줄 |
|---|------|----------|------|
| 01 | harness-concepts | Mandatory | 하네스 정의 + 7-layer 모델 + strength ladder |
| 02 | instruction-surface | Mandatory | CLAUDE.md 작성 원리 + Scale Modes |
| 03 | routing-descriptions | Mandatory | 라우팅 — description이 전부다 |
| 04 | structure-naming | Standard | 폴더 넘버링과 파일 네이밍 |
| 05 | hooks-recovery | Standard | 훅 이벤트 전모와 Recovery-First 설계 |
| 06 | security-pii | Mandatory | PII/시크릿 3중 방어와 비가역 안전 순서 |
| 07 | context-economy | Standard | 컨텍스트 예산 — 매 세션 로드되는 것의 경제학 |
| 08 | build-workflow | Standard | 빈 폴더에서 운영까지 — 구축 순서와 인터뷰 설계 |
| 09 | validation-principles | Standard | 검증 원리 — 눈이 아니라 기계로 |
| 10 | delegation-design | Optional | 위임 설계 — 서브에이전트는 증거가 있을 때만 |
| — | ANTI-PATTERNS | 참고 | 워크스페이스를 죽이는 실패 패턴 12종 |
| — | SELF-CHECK | 실습 | 레이어별 통합 점검 워크시트 (핵심 12 + 심화 11) |

적용 레벨: **Mandatory** = 모든 워크스페이스 / **Standard** = 기본 권장 / **Optional** = 조건 충족 시.

## 읽는 순서

1. **01 → 08** — 멘탈모델과 구축 순서. 나머지는 각 레이어의 상세.
2. 뼈대를 잡을 때: 01 §레이어 + 04 + 02
3. 하네스를 쌓을 때: 03 → 10 → 05 → 06 → 07
4. 검증과 진화: 09 → 08 §4
5. 구축 전후로 **SELF-CHECK**를 돌리고, 막히면 **ANTI-PATTERNS**에서 증상을 찾는다.

## 용어집

| 용어 | 정의 |
|------|------|
| 하네스 (harness) | AI가 의도대로 동작하게 하고 오작동 시 복귀하게 하는 통제 장치의 총합 |
| 지침 표면 (instruction surface) | 매 세션 로드되는 헌법 문서 (CLAUDE.md + rules) |
| 라우팅 | 사용자 자연어 → 커맨드/스킬/서브에이전트 선택. 신호는 description뿐 |
| 트리거 발화 | 사용자가 실제로 말할 "~해줘" 형태의 문장. description의 핵심 재료 |
| NOT-trigger | 발동하면 안 되는 경우와 대신 갈 곳을 description에 명시한 경계 |
| 도메인 살 | 위임 카드의 구체성 4종 — 정체성/방법/실패패턴/KPI |
| strength ladder | 하네스 강도의 단계 (basic → light → full → enforced)와 승격/강등 신호 |
| 게이트 | 통과 조건을 만족해야 다음으로 가는 차단점 (카드 생성 게이트, Stop 게이트 등) |
| recovery 계약 | 오작동 시 복귀 절차를 실행 전에 문서로 고정한 것 |
| 정본 (SSOT) | 같은 정보의 단일 출처. 나머지는 포인터로만 참조 |
| 복구 지점 | 되돌아갈 수 있는 상태 스냅샷 — 실무적으로는 커밋 |
| 닫힌 루프 | 생성 → 운영 → 실측 → 표준 반영 → 회귀 → 기록의 진화 사이클 |

## 범위

이 패키지는 원리 문서만 담는다. 생성 스크립트(generator), 검증 스크립트(validator),
작업 유형별 템플릿(아키타입), 운영 데이터는 포함되지 않는다.
SELF-CHECK가 구현 시 요구사항 역할을 한다.

---
*예시는 모두 가상 도메인이다 (온라인 베이커리 등).*
