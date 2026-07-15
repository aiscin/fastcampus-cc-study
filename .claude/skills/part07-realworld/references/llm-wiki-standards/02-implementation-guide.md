# LLM Wiki 완전 해부 — 정의부터 구현까지 (강의용 레퍼런스)

> 작성: 2026-06-03 · 용도: 최종 프로젝트 LLM Wiki 강의 설계
> 출처 등급: ★1차(Karpathy 원문·실제 GitHub 레포 README) / ☆보조(블로그·2차)
> 1차 출처: Karpathy gist(2026-04-04), ekadetov/llm-wiki, Ar9av/obsidian-wiki(1.7k★), AgriciDaniel/claude-obsidian
> ⚠️ 검증 강도 표기: **[확정]** = 1차 출처 다수 일치 / **[약함]** = 단일·약한 출처(강의에서 단정 금지)

---

## 1. LLM Wiki란 무엇인가 [확정]

**한 줄 정의**: 질문할 때마다 RAG를 다시 돌리는 대신, 지식을 **한 번** 상호 연결된 마크다운 파일로 "컴파일"해두고, **LLM이 그 위키를 계속 최신 상태로 유지**하는 *지속적·복리적(compounding) 지식 베이스*.

- **시초**: Andrej Karpathy가 2026년 4월 4일 공개한 gist의 "LLM Wiki 패턴".
- **사상적 뿌리**: Vannevar Bush의 **Memex**(1945) — 개인이 큐레이션한 지식 저장소 + 문서 간 연결. Bush가 못 푼 "누가 이 연결을 유지보수하나?"를 **LLM이 지치지 않고** 대신한다는 게 핵심.
- **형태**: 특정 제품이 아니라 **패턴**. Obsidian 볼트 + 코딩 에이전트(Claude Code/Cursor/Codex/Hermes 등) 조합으로 구현.

> Karpathy 원문 인용: *"The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping."* → 그 bookkeeping을 LLM이 한다.

---

## 2. 왜 RAG가 아니라 LLM Wiki인가 (강의 핵심 내러티브) [확정]

| | 일반 RAG / 벡터DB | LLM Wiki |
|---|---|---|
| 지식 처리 시점 | **쿼리 때마다** 청크 검색·조합 | **수집 때 한 번** 합성·교차링크 |
| 축적성 | 없음 (매번 처음부터) | **복리적** — 답이 위키에 쌓임 |
| 5개 문서 종합 질문 | 매번 조각을 다시 긁어모음 | 이미 합성된 페이지를 읽음 |
| 저장 형태 | 임베딩 벡터(블랙박스) | 사람이 읽는 **마크다운**(소유·이식 가능) |
| 모순/갭 | 검색 결과에 그냥 섞임 | lint가 **모순·고아·갭을 명시** |

> Karpathy 원문: *"Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up."*

**핵심 슬로건**: "RAG는 매번 검색한다. LLM Wiki는 한 번 이해하고 계속 키운다."

**단, 솔직한 한계 [약함→정직하게]**: "벡터DB 대비 정량적 우위(토큰 N배 절감, recall %)"는 단일 블로그 출처뿐이라 강의에서 수치로 단정하면 안 됨. **정성적 차이(축적성·소유성·설명가능성)**로 설득하는 게 안전.

---

## 3. 아키텍처 — 3계층 + 운영 파일 [확정]

Karpathy가 제시한 **3계층**:

```
① Raw sources (원본)   ← 불변. LLM은 읽기만.
        ↓ 컴파일
② The Wiki (위키)      ← LLM이 100% 소유·생성·유지하는 마크다운
        ↑ 규칙 참조
③ The Schema (스키마)  ← CLAUDE.md: 위키 구조 규칙 + 워크플로우 정의
```

- **① Raw**: 원본 자료 그대로. "LLM이 절대 수정하지 않음"이 불변식(immutable).
- **② Wiki**: 소스 요약 페이지, 개념 페이지, 인물/엔티티 페이지, 저장된 쿼리 답변. 전부 `[[위키링크]]`로 상호 연결.
- **③ Schema (CLAUDE.md)**: "위키 구조 규칙이 뭔가? 새 자료 들어오면 어떤 단계를 거치나?"를 적어둔 **에이전트 작업 지시서**. → LLM Wiki의 두뇌.

### 실제 폴더 구조 (ekadetov/llm-wiki 1차 출처) [확정]

```
~/ObsidianVault/03-Resources/<wiki-name>/
├── raw/                  ← 불변 소스 (LLM 미편집)
│   ├── articles/         ← 텍스트 소스 문서
│   └── attachments/      ← 이미지
├── wiki/                 ← LLM 소유 페이지
│   ├── index.md          ← 카탈로그 (★가장 먼저 읽는 입구)
│   ├── queries/          ← 저장된 쿼리 답변
│   └── <concept>.md      ← 개념/엔티티 페이지
├── outputs/reports/      ← 날짜별 lint 리포트
├── CLAUDE.md             ← 위키 스키마 및 컨벤션 (=③ Schema)
├── log.md                ← append-only 작업 로그
├── .gitignore
└── qmd.yml               ← 하이브리드 검색(BM25+벡터) 설정
```

**핵심 파일 4종**:
- `CLAUDE.md` — 페이지 템플릿·작성 규칙·워크플로우(스키마 그 자체)
- `index.md` — 모든 페이지 + 한 줄 요약 + 메타. **쿼리 시 LLM이 첫 번째로 읽는 진입점**(= MOC 역할)
- `log.md` — `## [2026-04-02] ingest | Article Title` 형식의 append-only 타임라인
- `qmd.yml` — BM25+벡터 하이브리드 검색 설정(선택. 작은 위키는 index.md 직접 읽기로 폴백)

---

## 4. 운영 파이프라인 — 4대 동사 [확정]

Karpathy 원형은 **ingest / query / lint** 3동사. 실제 구현(ekadetov)은 ingest를 **수집/컴파일로 분리**해 4동사로 운영:

> **init (1회 부트스트랩 — 루프 밖)**: 4동사가 돌기 전에 빈 위키 뼈대(raw/ wiki/ CLAUDE.md)를 *한 번* 세우는 단계. 반복 동사가 아니므로 4동사와 구분한다. (강의: clip-03=init, clip-04=ingest/compile/query, clip-05=lint)

### ① `ingest` — 원본을 raw/에 저장만
```
/llm-wiki:wiki ingest https://example.com/article
```
→ `raw/articles/`에 저장. **위키 페이지는 안 만듦**(관심사 분리). 입력: URL·md·PDF·전사·이미지 등.

### ② `compile` — 원본을 위키로 변환
```
/llm-wiki:wiki compile
```
→ 미컴파일 원본을 읽어 **소스 요약 페이지 + 개념 페이지 + 인물 페이지** 생성/갱신 → `index.md` 갱신 → git 커밋.
> Karpathy 원형에선 ingest 한 동사 안에 "읽기→요약→관련 페이지 10~15개 갱신→인덱스 갱신→로그 기록"이 다 들어감.

### ③ `query` — 위키에 질문
```
/llm-wiki:wiki query "X와 Y의 관계는?"
```
→ 검색(qmd 또는 index.md) → 관련 페이지 읽기 → `[[위키링크]]` 인용과 함께 답 합성 → **좋은 답은 `queries/`에 새 페이지로 저장**(탐색 결과도 복리 축적).

### ④ `lint` — 위키 건강검진
```
/llm-wiki:wiki lint
```
→ **죽은 링크, 고아 페이지(인바운드 링크 0), 누락 섹션, 페이지 간 모순, 오래된 내용, 인덱스 불일치** 검사 + 자동 수정 가능한 건 수정.

> **강의 포인트**: 이 4동사를 "수집→정제→질문→점검" 루프로 가르치면 비개발자도 직관적. LLM Wiki의 전부가 이 루프다.

### 대안 파이프라인 — 4단계 (Ar9av/obsidian-wiki) [확정]
한 번의 ingest가 내부적으로 4 stage를 거치는 변형:
1. **Ingest** — 원본 직접 소비(전처리 없음)
2. **Pull Information** — 개념·엔티티·주장·관계·열린질문 추출, 노이즈 버리고 신호만. frontmatter에 1~2문장 요약(미리보기용)
3. **Merge** — 기존 페이지와 통합(있으면 갱신, 진짜 새 거면 생성). **중복 금지**, 출처를 frontmatter에 추적
4. **Schema** — 카테고리 일관성·위키링크 유효성·인덱스 갱신을 유지하며 구조가 **유기적으로 창발**

---

## 5. 메타데이터 · 위키링크 · 인덱스(MOC) [확정]

- **위키링크 `[[...]]`**: 페이지 간 연결 = 그래프의 엣지. Obsidian 그래프뷰로 토폴로지 시각화.
- **frontmatter**: 1~2문장 요약(미리보기·tiered read용), 출처(provenance), 태그/카테고리. Dataview로 동적 테이블 생성.
- **index.md = MOC(Map of Contents)**: 전체 페이지 카탈로그 + 한 줄 요약. **LLM이 쿼리 때 가장 먼저 읽는 입구**. 사람도 여기서 위키를 항해.
- **provenance 추적(Ar9av)**: extracted/inferred/ambiguous로 "이 지식이 어디서 왔나" 표기 → 설명가능성.

---

## 6. "1만 노드 중 수십 개만 읽는" 효율 구조 [약함 — 정직 표기]

**원리(정성적, 합의된 부분)**: 에이전트는 위키 전체를 로드하지 않는다. **tiered read(계층적 읽기)**:
```
1) index.md(카탈로그) 먼저 → 2) 제목·태그·요약만 스캔 →
3) 정말 필요한 페이지 본문만 열기
```
→ 볼트가 커져도 쿼리당 읽는 양이 거의 평탄. `[[위키링크]]`를 따라 관련 노드 수십 개만 회수.

**Work Directory 분할**: 에이전트별/프로젝트별 전용 폴더로 컨텍스트 격리 → 각 에이전트는 자기 영역만 봄.

**⚠️ 단정 금지**: "쿼리당 4,000~5,000 토큰, ~100% recall, 1만 테이블까지 스케일" 같은 **정량 수치는 단일 블로그/단일 arxiv에만** 등장하고 다관점 검증 탈락. 강의에선 "전체를 안 읽고 index→요약→본문 순으로 필요한 것만 연다"는 **메커니즘**까지만 설명하고, 수치는 "내 볼트로 직접 측정해보자"로 실습화하는 게 안전.

---

## 7. 검색 / GraphRAG 연동 [부분 확정]

- **qmd**(확정): BM25 + 벡터 **하이브리드 검색** + LLM 리랭킹. `qmd.yml`로 설정, MCP 또는 CLI 트랜스포트. 작은 위키는 끄고 `index.md` 직접 읽기로 폴백.
- **그래프 내보내기(Ar9av, 확정)**: `wiki-export` 스킬로 **JSON / GraphML / Neo4j / HTML** 출력 → 여기서 진짜 GraphRAG로 연결 가능.
- **GraphRAG (연구 배경 — 강의 미채택)**: 위키링크가 이미 그래프라 GraphRAG로 확장하는 연구 흐름은 있으나(정량 우위 주장은 블로그 출처라 단정 금지), **우리 강의는 graph 검색을 채택하지 않는다**(아래 ⚠ 항목 참조). 이 절은 연구 배경 참고용.
- **⚠ 우리 강의는 graph 검색을 다루지 않는다 (확정)**: 백링크 따라가기(graph-walk)도, 풀 GraphRAG(엔티티추출·커뮤니티탐지·그래프DB)도 **강의 범위 밖**. 검색은 ① 클로드코드의 **설명(description) 기반 선별**(clip-05, 수강생 직접) → ② 대규모면 **설명 임베딩 검색(ChromaDB)**(강사 시연)으로만 간다. `[[위키링크]]`는 페이지 연결과 HTML 시각화 용도로만 남긴다(검색 메커니즘 아님).

---

## 8. Obsidian + Claude Code 구현 — 단계별 [확정]

> ⚠ **아래 설치 절차는 원본 레포(ekadetov) 참고용 — 우리 강의는 이대로 하지 않는다.** 우리 방식은 이 절 끝의 "★ 우리 강의 = Obsidian-free" 박스 참조(Node·Obsidian 볼트·플러그인 설치 없음, clip-02 빌더로 골격만 세움).

실제 설치/사용(ekadetov 원본 레포 기준 — 참고용):

```bash
# 0. 사전: Node.js 18+, Git, Obsidian 볼트(~/ObsidianVault/03-Resources/)
# 1. 플러그인 설치
claude plugin install /path/to/llm-wiki

# 2. 위키 초기화 → raw/ wiki/ CLAUDE.md 자동 생성 + git 추적
/llm-wiki:wiki init my-topic

# 3. 자료 수집 (Obsidian Web Clipper로 raw/에 저장해도 됨)
/llm-wiki:wiki ingest https://example.com/article

# 4. 위키로 컴파일 (요약·개념·인물 페이지 + index 갱신 + 커밋)
/llm-wiki:wiki compile

# 5. 질문 (인용 포함 답 + queries/에 저장)
/llm-wiki:wiki query "핵심 개념 3개를 비교해줘"

# 6. 주기적 점검
/llm-wiki:wiki lint
```

다른 구현(Ar9av)은 `pip install obsidian-wiki` 또는 `npx skills add Ar9av/obsidian-wiki`로 깔고 `/wiki-setup → /wiki-ingest → /wiki-query → /wiki-lint`. **15+ 에이전트(Claude Code/Cursor/Windsurf/Codex/Gemini/Hermes…)** 호환, setup.sh가 각 에이전트 디렉터리에 스킬 심볼릭링크.

**Obsidian 부가도구(전부 선택 — 우리 강의는 안 씀)**: Web Clipper(웹→md), Graph View(구조 시각화), Dataview(frontmatter 쿼리), Marp(슬라이드), Git(버전관리 자동).

> ### ★ 우리 강의 = Obsidian-free (확정)
> - **엔진 = 안티그래비티 안의 Claude Code + 마크다운 + git.** Obsidian은 *뷰어 스킨*일 뿐 엔진이 아니다(Karpathy: 도구는 abstract).
> - 위키는 **`workspaces/fastcampus-cc` 폴더 안에 그대로** 산다 — 별도 볼트/앱 설치·전환 없음.
> - **소비자가 에이전트**다. Claude Code는 grep/read로 위키를 회수하지 그래프뷰를 눈으로 안 본다 → GUI 불필요.
> - Obsidian 기능 대체: 그래프뷰→**"그래프 그려줘"로 Mermaid/HTML 즉석 렌더 후 브라우저** · 백링크→`grep "[[페이지명]]"` · Clipper→Claude Code URL fetch=ingest · Dataview→"표로 보여줘".
> - Obsidian은 **"이미 쓰는 사람이면 같은 폴더 열면 끝(마이그레이션 0)"**이라는 *이식성 각주*로만 등장. → 안 써도 그래프까지 전부 동작.

---

## 9. 우리 강의/최종 프로젝트 설계 제언

1. **3계층(raw/wiki/schema)을 첫 시간에 못박기** — LLM Wiki의 정체성. raw 불변 + wiki는 LLM 소유 + CLAUDE.md가 두뇌.
2. **4동사 루프(ingest→compile→query→lint)로 커리큘럼 뼈대** — 각 동사가 한 클립/한 실습. 비개발자도 "수집→정제→질문→점검"으로 이해.
3. **"왜 RAG가 아닌가"를 정성적으로** 설득(축적성·소유성·설명가능성). 수치 단정 회피.
4. **효율은 메커니즘(tiered read + index 진입점 + 위키링크 회수)까지만** 설명하고, 정량은 "직접 측정 실습"으로.
5. **검색이 더 필요해지면 설명(description) 임베딩 검색(ChromaDB)** — graph/GraphRAG는 **강의에서 다루지 않는다**(§7은 연구 배경 참고용일 뿐).
6. **차별화**: 경쟁 강의(①비개발자/오프라인, ⑥멀티에이전트/Discord, ②Hermes 자기진화) 대비, 우리는 "비개발자가 **따라치며** 3계층·4동사로 *동작하는* 위키를 끝까지 완주"하는 따라치기 완주형.

---

## 출처
- ★ Karpathy 원본 gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- ★ ekadetov/llm-wiki (Claude Code 플러그인): https://github.com/ekadetov/llm-wiki
- ★ Ar9av/obsidian-wiki (1.7k★, 4-stage, 멀티에이전트): https://github.com/Ar9av/obsidian-wiki
- ★ AgriciDaniel/claude-obsidian: https://github.com/AgriciDaniel/claude-obsidian
- ☆ 보조(정량 주장은 미검증): decodethefuture.org, smartscope.blog, mindstudio.ai, flur.ee 등
