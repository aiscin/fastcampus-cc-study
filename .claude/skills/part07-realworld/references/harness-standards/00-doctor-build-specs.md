# 하네스 닥터 빌드 스펙 (clip-02 라이브 빌드용)

> clip-02에서 **워크스페이스 빌더 안에 닥터 4종 + /audit·/new-workspace를 그 자리에서 만든다.** 미리 완성품을 배포하지 않는다 — Part 06에서 배운 스킬 만들기를 실제로 써먹는 자리.
> 각 닥터는 같은 폴더의 표준(`01`~`10`)을 references로 빨아들여 self-contained로 짓는다.

## 라이브 빌드 구조 (시간 관리)

4종을 다 풀로 만들면 세그먼트가 터진다. **harness-audit 하나만 자세히(교보재) → 나머지 3종은 "같은 방식, 각자 기준 문서 보고" 묶음 생성.**

```
STEP 2-a  harness-audit 1종 정석 빌드 — 질문→스펙 확인→SKILL.md+references 생성→열어보기 (Part 06 그대로)
STEP 2-b  나머지 3종(tuner·guard·breach) "같은 구조로, 각자 기준 표준 보고 만들어줘" 묶음 생성
STEP 2-c  /audit 커맨드(harness-audit 입구) 생성 — 얇은 wrapper
※ /new-workspace 커맨드는 STEP 5에서 (작업실 완성 후)
```

복사용 입력:
- 2-a: `Part 06에서 배운 대로 스킬을 만들 건데, harness-audit부터 만들어줘. references/harness-standards/09(검증)랑 01(7축)을 기준으로, 워크스페이스를 점검해서 7축 점수랑 부족한 곳 TOP3를 주는 스킬로. 만들기 전에 SKILL.md 구조부터 보여줘.`
- 2-b: `나머지 셋도 같은 구조로 만들어줘 — instruction-tuner(02·07·03 기준), guard-installer(05·06 기준), breach-test(05·09 기준). 각자 references에 해당 표준만 넣어서 self-contained로.`
- 2-c: `harness-audit를 부르는 /audit 커맨드를 점검 입구로 만들어줘.`

---

## 닥터 4종 스펙

각 스펙 = SKILL.md frontmatter(name·description) + 트리거 + 읽을 표준 + SKILL.md 절차 + 출력. 빌드는 이 표를 따라 생성한다.

### 1. harness-audit (검토) ★ 정석 빌드 대상

| 항목 | 값 |
|---|---|
| name | `harness-audit` |
| description | "워크스페이스를 설계 기준으로 점검해 7축 점수와 부족한 곳 TOP3를 낸다. '/audit', '워크스페이스 점검', '하네스 점수' 요청에 사용." |
| 트리거 | `/audit`, 점검, 진단, 점수 |
| 읽을 표준 | `09-validation-principles.md`(채점 모델) + `01-harness-concepts.md`(7축) |
| SKILL.md 절차 | ① 대상 워크스페이스 스캔(grep/카운트 — 결정론) ② 7축별 점검: 지시 층 3축(CLAUDE.md 존재·정체성 / 스킬·커맨드 description / 서브에이전트), 강제 층 1축(훅·권한), 뼈대 2축(목적·폴더 넘버링), 운영 1축(검증·변경 이력) ③ P0/P1/P2 가중치로 등급 ④ 부족한 곳 TOP3 + 보강 닥터 추천 |
| 출력 | **7축 점수표 + "크게 묶으면 두 층" 표기 + 등급(F/A) + TOP3 보강 제안.** LLM 감상 아닌 grep/카운트 기반 |

### 2. instruction-tuner (지시 층 보강)

| 항목 | 값 |
|---|---|
| name | `instruction-tuner` |
| description | "CLAUDE.md·규칙을 또렷하게 다듬고, 매 세션 불필요한 긴 절차는 '스킬로 빼라' 추천한다. 지시 층 보강 요청에 사용." |
| 읽을 표준 | `02-instruction-surface.md` + `07-context-economy.md` + `03-routing-descriptions.md` |
| SKILL.md 절차 | ① CLAUDE.md 길이·중복·모호 표현 점검 ② 매 세션 불변식 아닌 것 골라 "스킬로 분리" 제안(수첩은 얇게) ③ 커맨드·스킬 description에 트리거 발화 있는지 점검 |
| 출력 | 또렷해진 CLAUDE.md diff + 분리 추천 목록 |

### 3. guard-installer (강제 층 설치)

| 항목 | 값 |
|---|---|
| name | `guard-installer` |
| description | "훅(차단·백업)과 권한을 진단하고 settings.json에 설치한다. 강제 층 구축 요청에 사용." |
| 읽을 표준 | `05-hooks-recovery.md`(Recovery-First) + `06-security-pii.md` |
| SKILL.md 절차 | ① 비가역 자원 식별(삭제·외부 전송·PII) ② 막는 장치(차단 훅·권한) + 되돌리는 장치(백업 훅) 세트 설치 ③ PII/시크릿은 사고 안 기다리고 처음부터 |
| 출력 | settings.json 훅 + "막기+되돌리기" 설치 리포트 |

### 4. breach-test (강제 층 검증)

| 항목 | 값 |
|---|---|
| name | `breach-test` |
| description | "금지 행동을 자동으로 시도해 방어가 작동하는지 검증한다. '어겨보기', 방어 검증 요청에 사용." |
| 읽을 표준 | `05-hooks-recovery.md` + `09-validation-principles.md`(양성/음성 픽스처) |
| SKILL.md 절차 | ① 금지 행동 목록화(삭제·폴더 밖 수정 등) ② 각각 일부러 시도 ③ 차단되면 통과, 안 되면 실패 ④ "전부 차단됨" 리포트 |
| 출력 | 어겨보기 결과표(각 금지 행동 × 차단 여부) |

---

## 커맨드 (라이브 빌드 — 얇은 wrapper)

| 커맨드 | 시점 | 역할 |
|---|---|---|
| `/audit` | STEP 2-c | harness-audit 스킬 호출 입구 |
| `/new-workspace` | **STEP 5 (작업실 완성 후)** | 설계도 5줄 받아 새 워크스페이스 생성. 04·08·01 표준 기준. 점검할 닥터·지킬 장치가 다 갖춰진 뒤에야 단다 |

## 빌드 후 확인 (촬영 전 리허설)

- [ ] 닥터 4종 SKILL.md가 Part 06 학생 스킬과 같은 구조인지(열어보기 장면용)
- [ ] /audit 리포트가 **7축 + 두 층 묶음** 양식으로 나오는지
- [ ] breach-test가 실제로 차단을 잡아내는지(양성 픽스처)
