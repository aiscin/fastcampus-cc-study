# Clip 2 — 워크스페이스 만들기 — 제대로 작동하는지 점검까지 ★ (실습·따라치기, ~25분, 실습 33)

> 페르소나 메모 — A(마케터): "내 워크스페이스가 1분 만에 생긴다" 피날레를 빨리 예고 / B(PO): 점검 점수 리포트가 핵심 / C(영업): "어겨도 막히고, 점수로 확인하고, 찍어내준다" 3단 안심

## 자동 셋업

```bash
mkdir -p ~/fastcampus-cc/50-my-work/Part07-실전/실습33-워크스페이스구축/
echo "✓ 진도 폴더 준비. 빌더 본체는 별도 폴더에 짓는다 (예: ~/workspace-builder)"
```

## 브리핑 — 이 클립이 특별한 이유

clip-01 설계도 5줄을 실물로 만든다. 그런데 그냥 워크스페이스 하나가 아니라, **워크스페이스를 점검하고 새로 만들어주는 작업실(워크스페이스 빌더)**을 짓는다. 끝에는 이 빌더가 **수강생 본인의 설계도로 업무용 워크스페이스를 찍어준다.** (빌더 = 하네스를 만드는 하네스 — "메타하네스" 용어 사용 가능)

**핵심 메시지** — 만들고 끝이 아니다. **일부러 어겨봐서 막히는 걸 눈으로 보고, /audit 점수로 검증한 다음**에야 믿고 맡긴다. clip-01의 검증·갭 메우기(내비 에코)가 여기서 도구가 된다. 한 줄: **어기는 건 막히고, 시키는 건 되고, 필요한 건 찍어낸다.**

**하네스 닥터 스킬 4종 (clip-02에서 라이브 빌드 — Part 06에서 배운 스킬 만들기를 그대로 써먹는 자리. 미리 완성품 배포 X, 참고 표준만 스킬 내장):**

| 스킬 | 하는 일 | 층 |
|---|---|---|
| **harness-audit** | 워크스페이스를 설계 기준으로 점검 → 점수 + 부족한 곳 TOP3 | 검토 |
| **instruction-tuner** | CLAUDE.md·규칙을 또렷하게 + "이건 스킬로 빼라" 분리 추천 | 지시 층 보강 |
| **guard-installer** | 훅(차단·백업)과 권한을 진단하고 설치 | 강제 층 보강 |
| **breach-test** | 금지 행동을 자동으로 시도해 방어 작동을 검증 | 강제 층 검증 |

→ 검토 하나, 지시 층 보강 하나, 강제 층 설치 하나, 강제 층 검증 하나. **clip-01의 두 층이 그대로 도구가 된 것.** 라이브 빌드 구조·닥터별 스펙은 `references/harness-standards/00-doctor-build-specs.md` (harness-audit 1종 정석 + 나머지 3종 묶음).

### 닥터 빌드 기준집 (스킬 내장)

> 4종 + /new-workspace를 만들 때 각 닥터의 채점·진단 기준은 `references/harness-standards/` 12편에서 가져온다(스킬 내장 — 별도 경로 의존 없음). 빌드 시 각 닥터의 `references/`에 해당 표준만 증류해 self-contained로.

| 닥터 | 기준 표준 |
|---|---|
| **harness-audit** | `harness-standards/09-validation-principles.md`(P0/P1/P2 채점) + `01-harness-concepts.md`(7축) |
| **instruction-tuner** | `02-instruction-surface.md` + `07-context-economy.md` + `03-routing-descriptions.md` |
| **guard-installer** | `05-hooks-recovery.md` + `06-security-pii.md` |
| **breach-test** | `05-hooks-recovery.md` + `09-validation-principles.md`(양성/음성 픽스처) |
| **/new-workspace** | `04-structure-naming.md` + `08-build-workflow.md` + `01-harness-concepts.md`(쌓는 순서) |

**/audit 리포트 양식**: 7축 점수(지시 층 3칸=CLAUDE.md·스킬/커맨드·서브에이전트 / 강제 층 1칸=훅·권한 / 뼈대 2칸=목적·폴더 / 운영 1칸=검증·이력) + "크게 묶으면 두 층" 표기. STEP 4 발화와 1:1.

## STEP 흐름 (따라치기)

```
[STEP 1] 지시 층 ① — 빈 폴더 + 짧은 CLAUDE.md (5분)
   질문하기 → 구조 제안받기 → "만들기 전에 보여줘" → 생성
   ※ CLAUDE.md는 짧게(수첩) — 정체성 + 설계 기준 4가지 + 금지 한두 개. 긴 절차는 전부 스킬로
   ※ PARA 콜백: 학습 워크스페이스(fastcampus-cc)가 이미 이 구조
[STEP 2] 지시 층 ② — 하네스 닥터 4종 라이브 빌드 + /audit 커맨드 (5분)
   harness-audit 1종 정석(Part 06 방식: 질문→SKILL.md 구조 확인→생성) → 나머지 3종 "같은 구조, 각자 기준 표준 보고" 묶음 → /audit 입구
   ※ 기준 표준은 `references/harness-standards/`에 내장 — 닥터가 그걸 보고 만들어진다
   ※ /new-workspace 커맨드는 여기서 안 만든다 (STEP 5, 작업실 완성 후)
[STEP 3] 강제 층 — guard-installer로 설치 + 일부러 어겨보기 ★피크 (5분)
   차단 화면 확인 → "방금 손으로 한 어겨보기를 자동화한 게 breach-test"
   ※ 강제 층의 두 얼굴: 막는 것(차단) + 되돌리는 것(백업)
[STEP 4] 검증 — /audit 점수 리포트 2건 (4분)
   빌더 자체 + 학습 워크스페이스(fastcampus-cc). "말이 아니라 점검표가 증거"
   낮은 점수 = 실패가 아니라 다음 보강 지점. 하네스는 부족이 보일 때마다 한 칸씩
[STEP 5] 피날레 — /new-workspace에 설계도 5줄 → 내 업무용 워크스페이스 생성 (2분)
   "오늘 만든 건 워크스페이스 하나가 아니라, 워크스페이스를 만드는 능력"
```

**복사용 입력:**
1. `여기를 '워크스페이스를 점검하고 새로 만들어주는 작업실'로 만들려는데, 폴더 구조랑 CLAUDE.md를 어떻게 잡으면 좋을까? 지난번에 배운 설계 기준 — 목적·지시 층·강제 층·검증 — 이 작업실의 규칙이 됐으면 해.`
2. `좋아, 그 구조로 가자. 만들기 전에 최종 폴더 트리랑 CLAUDE.md부터 보여줘.`
3. `Part 06에서 배운 대로 harness-audit 스킬부터 만들어줘 — references/harness-standards의 09랑 01 기준, 워크스페이스를 점검해 7축 점수랑 부족한 곳 TOP3를 주는 스킬로. 만들기 전에 SKILL.md 구조부터 보여줘.` → `나머지 셋도 같은 구조로 — instruction-tuner(02·07·03), guard-installer(05·06), breach-test(05·09) 기준.` → `harness-audit를 부르는 /audit 커맨드를 점검 입구로 만들어줘.`
4. `guard-installer로 이 작업실에 안전장치를 걸어줘 — 삭제 차단 훅, CLAUDE.md 자동 백업 훅, 폴더 밖 수정은 승인받기.`
5. `테스트야. 90-archive에 있는 아무 파일이나 하나 삭제해봐.` ← 차단 확인용
6. `/audit — 이 워크스페이스를 설계 기준으로 점검해줘.`
7. `/audit — 학습 워크스페이스(fastcampus-cc)를 점검해줘.`
8. `/new-workspace — 설계도대로 만들어줘: 목적은 ___, 아키타입은 ___, 폴더는 ___, 규칙은 ___, 강제 층은 ___.` ← 본인 설계도 5줄 그대로

**Part 5·6 자산 사슬:** CLAUDE.md 작성법(실습18)=지시 층 / 스킬 구조(Part06)=닥터 4종이 같은 구조(열어보기) / trash-guard Hook(실습21)=강제 층의 원형.

## 단계 안내

| Phase | 내용 |
|------|------|
| A (2분) | 도입 — "워크스페이스, 하나만 쓰진 않을 거잖아요" → 빌더 예고 |
| B-1 (5분) | STEP 1 빈 폴더 + 짧은 CLAUDE.md + PARA 콜백 |
| B-2 (5분) | STEP 2 닥터 4종 **라이브 빌드**(1 정석+3 묶음) + /audit 입구 |
| B-3 (5분) | STEP 3 guard-installer + **일부러 어겨보기** ★피크 |
| B-4 (4분) | STEP 4 /audit 2건 (빌더 + 학습 워크스페이스) |
| B-5 (2분) | STEP 5 /new-workspace 피날레 |
| C·D (3분) | 마무리 — 3박자 정리 + "닥터 4종도 제 기준, 깎아 쓰세요" + workmate 스타터 선물 |

## 에러 대응

| 상황 | 대응 |
|------|------|
| "닥터 4종을 다 라이브로 만들면 너무 길지 않아요?" | harness-audit 1종만 정석으로, 나머지 3종은 "같은 구조로" 묶음 생성 — 기준 표준이 references에 내장돼 있어 한 줄 입력으로 빠르게 |
| "직접 만든다고요?" | "Part 06에서 배운 그대로예요. 닥터도 결국 SKILL.md + references 스킬이라, 표준 문서만 있으면 그 자리에서 만들어집니다 — 그게 오늘의 핵심" |
| /audit 점수가 낮음 | 낮은 게 실패가 아니라 다음 보강 지점 — tuner·guard-installer가 그래서 있다 |
| "빌더가 제 업무에 무슨 소용?" | 빌더가 찍어내는 게 전부 본인 업무용 — 업무가 늘 때마다 1분에 새 워크스페이스 |
| 어겨보기 안 막힘 | settings.json 위치 확인 → 클로드코드 재시작. 막힐 때까진 방어장치 없는 상태 |
| /new-workspace 결과 이상 | 설계도 다섯 줄을 빼먹지 말고 그대로 — 목적·아키타입·폴더·규칙·강제 층 |

## WRAP

트리거 (`완료` / `/wrap`):
1. 결과물 검증 — **3개**: 빌더(짧은 CLAUDE.md + 닥터 4종 + 훅) / /audit 리포트 2건 / **빌더가 찍어준 내 업무용 워크스페이스**
2. README.md — 워크스페이스 목적 + 건 장치 + "어겨봤더니 막혔다" 한 줄
3. progress.json — `practice_completed`에 33, `projects_completed`에 `workspace`
4. 회고 — "닥터 4종과 점검 기준도 강사 기준일 뿐 — 내 일엔 어떤 검사를 추가/수정할까" 한 줄
5. 배포 자산 — **workmate 스타터** (강사 실사용 업무 비서 워크스페이스 클린 카피): 받아서 `/onboarding`으로 개인화, 그대로 쓰지 말고 깎아 쓰기. 첫 사용법으로 "/audit으로 점검" 추천
6. 다음 — "clip-03 — 두 번째 프로젝트 LLM Wiki. **방금 찍어낸 내 워크스페이스 안에** 짓는다. 그 CLAUDE.md가 위키 규칙서"
