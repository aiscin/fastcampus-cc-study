---
name: part07-realworld
description: "Part 07: 클로드코드 실전 활용하기 (v8 정합). 3개 캡스톤 프로젝트 — ① 하네스 엔지니어링으로 워크스페이스 짓기(clip-01·02) ② LLM Wiki 대화로 자라는 지식베이스(clip-03·04·05) ③ 유튜브 트렌드 대시보드(clip-06·07·08) + Part 8 성장 리포트. 핵심 framing: '하네스는 새 패러다임일 뿐 — 여러분은 Part 5·6에서 이미 부품을 다 만들어왔다. 오늘은 목적 하나로 조립한다.' 두 층 모델(지시 층=CLAUDE.md·스킬·커맨드 / 강제 층=훅·권한 설정) + 검증·갭 메우기(내비 비유). '/part07', 'Part 07', '실전 활용', '워크스페이스 만들기', 'LLM Wiki', '유튜브 대시보드' 요청에 사용."
---

# Part 07: 클로드코드 실전 활용하기 ★ 캡스톤

이 스킬이 호출되면 아래 규칙을 반드시 따른다.

---

## 커리큘럼 — Part 07 구성 (3프로젝트 / 8클립 + Part 8 1클립 — v8.2 정합)

> 학습 아크: **환경 → 지식 → 서비스** (규모가 커지는 흐름). Part 5(부품)·6(스킬) 자산을 전부 재료로 재활용.

| CH | Clip | 제목 | 유형 | 패턴 |
|---|:-:|---|---|---|
| **CH 01 — 워크스페이스 (하네스)** | **1** | 하네스 엔지니어링이란? + 워크스페이스 설계 | 이론·설계 | 설계도 1장 |
|  | **2** | 워크스페이스 만들기 — 점검까지 ★ | 실습(따라치기) | 빌더: 지시 층→닥터 4종→강제 층·어겨보기→/audit→/new-workspace |
| **CH 02 — LLM Wiki** | **3** | LLM Wiki란? + 아키텍처 잡기 | 이론·설계 | 위키 설계도 |
|  | **4** | 위키 짓기 — 투입부터 질문까지 ★ | 실습(따라치기) | 투입→정리→질문·기록→(그래프) |
|  | **5** | 한계와 개선 — 하위 인덱스→하이브리드 RAG로 고치기 ★ | 실습 | 하위 인덱스→개선 확인→하이브리드 RAG(키워드+시멘틱) |
| **CH 03 — 바이브코딩 (유튜브 Outlier 대시보드, 원본)** | **6** | 설계하기 — PRD 쓰고 데이터 기반 깔기 | 기획·설계 | show-me-the-prd→구체화→키3종→스키마 |
|  | **7** | 만들기 — 터진 영상 잡아내는 화면으로 ★ | 실습(따라치기) | kkirikkiri 생성→연결→수집→Outlier→Gemini |
|  | **8** | 배포하기 — 매시간 도는 서비스로 ★ | 실습(따라치기) | Trends→Vercel→EdgeFn→pg_cron→개선 |
| **Part 8** | — | 성장 리포트 + AI Native 여정 | 마무리 토크 | vibe-sunsang |

---

## Part 07 핵심 framing — 두 가지 메타 메시지 (v8.2)

1. **"하네스는 새 패러다임일 뿐, 이미 만들어왔다"** — 하네스 엔지니어링 = AI가 내 의도대로 동작하도록 지침·동작 방식을 지정해 원하는 결과물을 만들게 하는 것. **그리고 한 번 지정하고 끝이 아니라, 지정한 대로 동작하는지 확인하고 의도↔결과 갭을 메꾸는 것까지가 하네스** (서울→부산 내비 비유 — 경로 지정 + 이탈 시 재안내). Part 05 CLAUDE.md·커맨드·훅, Part 06 스킬이 전부 하네스 부품. 오늘은 **목적 하나로 조립**한다.
2. **두 층 모델** — **지시 층**(말로 가르친 것 = 훈련: CLAUDE.md·스킬·커맨드) + **강제 층**(장치로 막는 것 = 목줄: 훅·권한 설정). **지시는 부탁, 강제는 장치.** 둘 다 갖춰야 믿고 맡긴다. (백업 훅은 clip-02 guard-installer에서 "되돌리는 장치"로 등장)

**3프로젝트 = "만든 것을 묶어 내 것으로 완성":**
- ① 워크스페이스: 내 업무 전용 작업 환경(하네스)
- ② LLM Wiki: 쌓일수록 똑똑해지는 지식 자산 (벡터DB 없이 마크다운, Obsidian 불필요)
- ③ 유튜브 대시보드: **매시간 도는 공개 분석 서비스** (Supabase 백엔드 + Outlier Score, `/show-me-the-prd`→`/kkirikkiri` 바이브코딩, 매시간 pg_cron)

---

## 자산 사슬 (Part 5·6 → Part 7)

- Part 5 `CLAUDE.md`(실습18) → 모든 Part 07 클립의 지시 층 머리 + ②에서 위키 규칙서로 재활용
- Part 5 커맨드/에이전트(실습19) → ① /weekly 같은 워크스페이스 커맨드 패턴
- Part 5 Hook(실습21, trash-guard) → ① 강제 층 (삭제 차단·CLAUDE.md 백업)
- Part 6 9 스킬 → ① 워크스페이스에 배치 / ③ `/show-me-the-prd`(PRD 4종)·`/kkirikkiri`(에이전트 팀 코드 생성)로 바이브코딩
- ① 워크스페이스 → ② LLM Wiki가 그 안에 삶 → ③ 대시보드도 같은 워크스페이스에서

→ Part 8에서 "Part 5 자산 6종 + Part 6 9 스킬 + Part 7 3프로젝트 = 본인 평생 도구·환경" 정리.

---

## References 파일 맵

> 이론 클립(clip-01·03)도 **설계도 1장**을 남기므로 가이드 포함(설계도 채우기 중심). 실습 클립은 따라치기 + WRAP.

| Clip | 파일 |
|:-:|---|
| Clip 1 (하네스·워크스페이스 설계) | `references/clip01-workspace-design.md` |
| Clip 2 (워크스페이스 구축 ★) | `references/clip02-workspace-build.md` |
| Clip 3 (LLM Wiki 설계) | `references/clip03-wiki-design.md` |
| Clip 4 (위키 짓기 ★) | `references/clip04-wiki-build.md` |
| Clip 5 (한계·개선 ★) | `references/clip05-wiki-improve.md` |
| Clip 6 (유튜브 설계 — PRD·키·스키마) | `references/clip06-youtube-prd.md` |
| Clip 7 (만들기 — Outlier 대시보드 ★) | `references/clip07-youtube-dashboard.md` |
| Clip 8 (배포 — 매시간 자동수집 ★) | `references/clip08-youtube-deploy.md` |

---

## 하네스 표준 기준집 (clip-02 닥터 4종 빌드용)

> `references/harness-standards/` — 워크스페이스 설계·점검의 원리 표준 12편(스킬 내장). clip-02에서 **하네스 닥터 4종 + /new-workspace**를 만들 때 각 닥터의 채점·진단 기준이 여기서 나온다. 가르칠 땐 두 층, 점검할 땐 7축 — 7축 모델은 01에 있다.

| 표준 | 닥터 매핑 |
|---|---|
| `harness-standards/01-harness-concepts.md` | 공용 — 7-layer 모델·strength ladder·쌓는 순서 (audit·new-workspace) |
| `harness-standards/02-instruction-surface.md` | **instruction-tuner** — CLAUDE.md 작성 원리 |
| `harness-standards/03-routing-descriptions.md` | **instruction-tuner** — 커맨드/스킬 description 라우팅 |
| `harness-standards/04-structure-naming.md` | **/new-workspace** — 폴더 넘버링·네이밍 |
| `harness-standards/05-hooks-recovery.md` | **guard-installer** + **breach-test** — 훅·Recovery-First |
| `harness-standards/06-security-pii.md` | **guard-installer** — PII/시크릿 3중 방어 |
| `harness-standards/07-context-economy.md` | **instruction-tuner** — 컨텍스트 예산(수첩은 얇게) |
| `harness-standards/08-build-workflow.md` | **/new-workspace** — 빈 폴더→운영 빌드 순서 |
| `harness-standards/09-validation-principles.md` | **harness-audit** — P0/P1/P2 가중치·결정론 채점(/audit 점수의 원전) |
| `harness-standards/10-delegation-design.md` | 공용 — 위임 설계 (서브에이전트는 증거 있을 때만) |
| `harness-standards/ANTI-PATTERNS.md` · `SELF-CHECK.md` | 공용 — 안티패턴·자가 점검 |

**용어 주의:** 표준은 "메타하네스"·"7-layer" 용어를 쓴다. **사용 허용** (clip-02 빌더 = 메타하네스). 7축은 슬라이드가 아니라 /audit 리포트 양식으로 등장하고, 발화로 "크게 묶으면 두 층"으로 연결한다.

---

## LLM Wiki 표준 기준집 (clip-03·04·05 위키 빌드용)

> `references/llm-wiki-standards/` — LLM Wiki 개념·구현 리서치(스킬 내장, Karpathy gist·ekadetov/llm-wiki·Ar9av 1차 출처). CH 02에서 위키를 설계·빌드할 때 개념 정의·아키텍처·운영 루프의 원전이 여기서 나온다.

| 표준 | 쓰는 곳 |
|---|---|
| `llm-wiki-standards/01-concept-map-and-direction.md` | 7층 개념 지도(L0~L6) + 확정 방향(끝점 L4·Obsidian-free·워크스페이스 콜백) + MUST/OPTION. clip-03 설계의 골격 |
| `llm-wiki-standards/02-implementation-guide.md` | 3계층(raw/wiki/schema)·4동사(ingest/compile/query/lint)·tiered read·폴더 구조·출처 등급. clip-04·05 빌드의 원전 |

**연결 핵심:** 위키는 **clip-02 빌더로 찍은 "지식베이스" 아키타입 워크스페이스 안에** 산다. 그 워크스페이스의 CLAUDE.md가 곧 위키의 schema(③ 두뇌). 즉 CH 01(빌더) → CH 02(빌더로 지식베이스 워크스페이스 찍고 그 안에 위키)로 이어진다.

**정직성 가드:** "토큰 N배 절감·recall %·벡터DB보다 우월" 같은 **정량 수치 단정 금지**(단일 출처). 정성적 가치(축적성·소유성·설명가능성)로 설득하고, 효율은 "내 볼트로 측정" 실습으로.

---

## TrendBoard 표준 기준집 (clip-06·07·08 유튜브 대시보드 빌드용)

> `references/trendboard-standards/` — 실제 동작 앱(gptaku-trend) 소스를 분석해 추출한 빌드 사양(스킬 내장). CH 03에서 PRD 구체화·코드 생성·연결·배포의 정확한 공식·함수·뷰·체인이 여기서 나온다. clip-06 자동 셋업이 `trendboard/_spec/`로 복사한다.

| 표준 | 쓰는 곳 |
|---|---|
| `trendboard-standards/00-사전준비.md` | 키 3종(Supabase·YouTube·Gemini) 발급 — clip-06 Phase 3 |
| `trendboard-standards/01-PRD.md` | PRD 시드/정답 레퍼런스 — clip-06 Phase 1(/show-me-the-prd 답) |
| `trendboard-standards/02-데이터모델.md` | 테이블 7 + video_details 뷰 + Outlier 공식 — 구체화·검증 |
| `trendboard-standards/03-기술스택과규칙.md` | DO/DON'T + 환경변수 + 쿼터 — kkirikkiri 가드레일 |
| `trendboard-standards/BUILD-PROCESS.md` | 실제 체인·공식·의존순서(소스 분석) — 구체화의 핵심 사양 |
| `trendboard-standards/04-빌드가이드.md` | 2단 워크플로우(show-me-the-prd→kkirikkiri→연결) STEP |
| `trendboard-standards/05-배포와자동화.md` | Vercel + 매시간 pg_cron + 보안 — clip-08 |
| `trendboard-standards/06-트러블슈팅.md` | 증상별 해결 + 테스트 채널 — 막힐 때 |
| `trendboard-standards/assets/schema.sql` | 실행 가능한 전체 스키마(실제 마이그레이션 일치) — clip-06 Phase 4 |

**왜 미리 까나 (핵심):** `/show-me-the-prd`는 **수강생마다 다른 PRD**를 만든다 → 그대로 빌드하면 누군 되고 누군 안 된다. 그래서 공통 사양(`_spec/`)으로 **구체화 단계에서 수렴**시켜 **모두 동일 컨텍스트**로 시작한다. PRD 만드는 경험은 각자, 빌드 사양은 하나로.

**연결 핵심:** ③ 대시보드도 **clip-02 빌더로 찍은 워크스페이스 안에** 산다. 단순판(yt-dlp+정적HTML)이 아니라 **원본/풀버전**(Supabase 백엔드 + Outlier Score). 워크플로우는 `/show-me-the-prd`(PRD) → 구체화 → `/kkirikkiri`(코드 생성) → 클로드코드(연결·배포). 레퍼런스 소스는 **막판 참조용**(STEP 9), 처음부터 열면 베끼기가 된다.

**정직성 가드:** kkirikkiri 한 방에 백엔드·배포까지 안 된다 — "코드 생성은 kkirikkiri, 연결·운영은 클로드코드". service_role·YouTube·Gemini 키는 백엔드만(프론트·깃 노출 금지), search.list 금지, 목업 금지.

---

## 진행 규칙

- 입력 멘트는 **"~하려는데 어떻게 해?"** 패턴 강제 ("~만들어줘" 금지)
- STOP 분리 패턴 미사용 — **따라치기** 구조
- 결과물은 `~/fastcampus-cc/50-my-work/Part07-실전/실습NN-제목/`에 저장 (해당 reference의 자동 셋업이 폴더 생성)
- 단, ②·③ 프로젝트는 **별도 작업 폴더**(내 워크스페이스 / my-wiki / trendboard)에 짓고, 진도 README만 50-my-work에 남긴다
- ③ 유튜브 대시보드(clip-06·07·08)의 실제 동작 사양은 스킬 내장 `references/trendboard-standards/`다(자동 셋업이 `trendboard/_spec/`로 복사). 외부 `30-practice-design/.../trendboard-build-guide/`는 동일 내용의 제작 원본 — 사양이 충돌하면 스킬 내장본을 따른다
- progress.json — `practice_completed`·`projects_completed` 갱신
