# Clip 05 — 한계와 개선: 하위 인덱스 → 하이브리드 RAG로 직접 고치기 (실습 36) ★

> Part 07 / CH 02 LLM Wiki / Clip 05 (실습 36) | 예상 시간: ~40분
> 결과물: ① 타입별 하위 인덱스(계층 MOC) ② 개선 전/후 비교 ③ 하이브리드 RAG(키워드+시멘틱) + 회고
> 패턴: **자동 셋업 → 브리핑 → 하위 인덱스 → 개선 확인 → 하이브리드 RAG → WRAP**
> 정본 설계서: `~/llm-wiki/30-reports/2026-06-14-rag-index-design.md` (Part A 하위 인덱스 + Part B RAG) — 이 클립은 그 설계서를 **직접 구현**한다.
> 페르소나 메모 — A(마케터): "전/후를 눈으로" / B(PO): 하위 인덱스가 곧 RAG의 컬렉션이라는 연결 / C(영업): "여기까진 인덱스로, 여기부턴 RAG" 선 긋기

---

## 자동 셋업

스킬 호출 직후 아래 Bash를 즉시 실행 (사용자에게 명령을 보여주는 게 아니라 스킬이 직접). **clip-04에서 채운 위키를 그대로 쓴다. 한계는 지난 클립에서 이미 확인했으니, 오늘은 바로 고친다.**

```bash
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
elif [ -d "$HOME/Desktop/fastcampus-cc" ]; then
  ROOT="$HOME/Desktop/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

# LLM Wiki = 별도 워크스페이스 (fastcampus-cc 밖)
if [ -d "$HOME/llm-wiki" ]; then WIKI="$HOME/llm-wiki"
elif [ -d "$HOME/Desktop/llm-wiki" ]; then WIKI="$HOME/Desktop/llm-wiki"
else WIKI="$HOME/llm-wiki"; fi
WORK_DIR="$ROOT/50-my-work/Part07-실전/실습36-위키개선"
mkdir -p "$WORK_DIR"

# 위키 폴더는 환경마다 wiki/ 또는 40-wiki/ — 둘 다 대응
if [ -d "$WIKI/40-wiki" ]; then WP="$WIKI/40-wiki"; elif [ -d "$WIKI/wiki" ]; then WP="$WIKI/wiki"; else WP="$WIKI"; fi

# 강의 비교 다이어그램(있으면) 복사
ASSET="$ROOT/.claude/skills/part07-realworld/assets/clip-diagrams"
cp "$ASSET/rag-vs-wiki-decision.png" "$WORK_DIR/" 2>/dev/null && echo "✓ 결정 가이드 다이어그램 복사"

# RAG 구현 레퍼런스 문서 복사
REFDOC="$ROOT/.claude/skills/part07-realworld/assets/clip05-rag-implementation.md"
cp "$REFDOC" "$WORK_DIR/" 2>/dev/null && echo "✓ RAG 구현 레퍼런스 문서 복사"

echo "✓ $WORK_DIR 진도 폴더 준비 완료"
echo "  위키 페이지: $(find "$WP" -name '*.md' 2>/dev/null | wc -l | tr -d ' ')장"
echo "  원본 기사(raw): $(find "$WIKI" -path '*raw*' -name '*.md' 2>/dev/null | wc -l | tr -d ' ')편"
echo "  설계서: $([ -f "$WIKI/30-reports/2026-06-14-rag-index-design.md" ] && echo '있음 — 오늘 이걸 구현' || echo '없음(clip-04에서 먼저 생성 권장)')"
echo "  오늘: 한계 재현은 끝 → 하위 인덱스 → 개선 확인 → 하이브리드 RAG(키워드+시멘틱)"
```

> ⚠ **강사 준비(1회)** — 2가지:
> - **대량 위키**: `seed-movie-wiki/raw` 1,000편을 컴파일한 위키를 강사 PC `llm-wiki/`에 깔아 둔다. 수강생도 같은 규모로 직접 구현한다(강사 시연이 아니라 수강생이 직접 한다). 15편 규모면 인덱스 분할·RAG의 효과가 안 보이므로 1,000편이 전제.
> - **임베딩 키**: 시멘틱 검색에 **Gemini API 키**(`GEMINI_API_KEY`)가 필요하다. clip-04/Part06에서 이미 발급했으면 재사용. 없으면 Phase 3 시작 전에 발급 안내.

셋업 결과를 한 줄로 보고한 뒤, 아래 **브리핑 + 진행 안내**를 한 메시지로 출력하고 SLEEP.

---

## 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 한 줄 | 한계는 지난 클립에서 봤다 — 오늘은 **하위 인덱스**로 검색을 쪼개고, 그 위에 **하이브리드 RAG**(키워드+시멘틱)를 올려 직접 고친다 |
| 태도 | 한계는 봤으니, 오늘은 직접 고쳐서 작동시킨다 |
| 선 긋기 | 어디까지 **하위 인덱스**(설치 0)로 되고, 어디부터 **RAG**(임베딩·벡터DB)가 필요한지 솔직하게 |

### 왜 지금 RAG인가 (정직 가드)

> 우리 입장은 "어지간한 규모면 인덱스로 충분, 정말 커지면 RAG"였다. 코퍼스가 원본 1,000편 + 엔티티 수백~천 단위로 커졌으니, 설계서가 예고한 'RAG 도입 트리거'를 이제 넘었다. 원칙을 어기는 게 아니라 예고한 시점에 도입하는 것이다.

### 결정 가이드 다이어그램 — 언제 무엇을 쓰나

> `실습36-위키개선/rag-vs-wiki-decision.png` 한 장 요약. **규모로 선을 긋는다.**

| 쓰는 것 | 언제 (다이어그램 내용) |
|---|---|
| **LLM Wiki** | 수백~수천 규모 / 쓸수록 쌓여서 똑똑해짐 / 마크다운이라 내 컴퓨터에 저장됨 / 여러 문서 종합이 미리 정리돼 있음 / 정리·검증 결과가 위키에 남음 |
| **RAG·벡터DB** | 수만~수십만 규모 / 원문 그대로가 중요할 때 / 방금 넣은 자료도 바로 검색 / 빨리·싸게 만들어야 할 때 / 요약 말고 원문을 찾을 때 |
| **하이브리드** | 정리·종합은 Wiki가, 대량 원문 검색은 RAG가 / 커지면 설명 임베딩(ChromaDB) / 규모 커지면 검색 켜기 |

> 선 긋기: 수백~수천은 마크다운+검색으로 충분, 수만 넘어가면 그때 임베딩/RAG.

### 오늘의 개선 — 3단 (전부 본인 직접)

| 단계 | 하는 일 | 도구 | 설치 |
|---|---|---|---|
| ① 하위 인덱스 | 평면 index → **타입별 `{type}/index.md`** + 라우터. 동명충돌(Dune 영화 vs 시리즈)을 경로 한정 링크로 해소 | 마크다운만 | **0** |
| ② 개선 확인 | "봉준호 영화" → `people/index.md`만 펼침. 전(평면 전체)/후(타입 인덱스) 비교 | — | 0 |
| ③ 하이브리드 RAG | 페이지를 임베딩해 **시멘틱 검색** + **키워드(BM25) 검색**을 동시에 돌려 점수 병합 | Gemini 임베딩 + 로컬 벡터DB | 필요 |

### 핵심 연결 — 하위 인덱스가 곧 RAG의 컬렉션

> 타입 = RAG 메타데이터 facet. 하위 인덱스를 타입(works/people/series/concepts/sources)으로 쪼개두면, 그게 그대로 RAG의 컬렉션·필터가 된다. 그래서 ①이 ③의 기초다 — 둘은 따로가 아니라 같은 "타입 네임스페이스"를 공유한다. (정본 설계서 §B-6)

### 하이브리드 검색이 왜 둘 다 필요한가 (③ 메커니즘)

| 방식 | 강점 | 약점 |
|---|---|---|
| **시멘틱(의미·임베딩)** | "씁쓸한 가족 드라마 같은 거" 모호 질문 | 고유명사·정확한 제목엔 약함 |
| **키워드(렉시컬·BM25)** | "기생충", 음차 표기, 정확한 제목 | 의미 유사엔 약함 |
| **하이브리드(둘 점수 병합)** | 서로의 약점을 메움 | — |

### 핵심 메시지

> ① 하위 인덱스만으로도 동명충돌·tiered-read 낭비가 즉시 해소된다 — **설치 0.**
> ② 거기에 RAG를 올리면 키워드로 안 잡히는 의미 질문, 설명 목록조차 다 못 읽는 규모까지 커버된다.
> ③ 단, RAG도 만능이 아니다 — top-K(가져오는 개수)·임베딩 품질(한국어면 멀티링구얼 필수)·**설명(summary) 품질**에 따라 빠질 수 있다. 그래서 ①에서 description을 잘 써둔 게 ③의 정확도를 좌우한다.

### 용어 30초 정리 (몰라도 됨, 궁금하면)

| 말 | 뜻 (우리 식으로) |
|---|---|
| 하위 인덱스(MOC) | 타입별로 쪼갠 목차 페이지 — 사람·에이전트가 먼저 읽는 진입점 |
| 임베딩 | 글을 의미가 담긴 **숫자 벡터**로 바꾼 것 |
| 벡터 DB | 그 임베딩을 저장·검색하는 곳 (예: **ChromaDB**, **sqlite-vec**, **Supabase pgvector**) |
| 시멘틱 검색 | 질문을 임베딩으로 바꿔 **의미로** 찾기 |
| 키워드 검색(BM25) | 단어 일치로 찾기 (고유명사·정확 제목에 강함) |
| RAG | 검색해 온 근거로 답하는 방식 (오늘은 시멘틱+키워드 하이브리드) |

> **CH03 연결:** 오늘 쓰는 벡터DB 기능을, 곧 CH03 유튜브 대시보드의 **Supabase가 pgvector로** 똑같이 품고 있다 — 도구만 다르고 원리는 같다.

### 공식 출처

- 정본 설계서: `~/llm-wiki/30-reports/2026-06-14-rag-index-design.md`
- Karpathy LLM Wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Gemini 임베딩(`gemini-embedding-001`, 멀티링구얼): https://ai.google.dev/gemini-api/docs/embeddings
- ChromaDB: https://docs.trychroma.com · sqlite-vec: https://github.com/asg017/sqlite-vec
- Supabase pgvector(CH03 연결): https://supabase.com/docs/guides/database/extensions/pgvector

---

## 진행 안내

```
✓ 50-my-work/Part07-실전/실습36-위키개선/ 진도 폴더 준비
✓ clip-04에서 채운 llm-wiki/ 사용 · 정본 설계서(rag-index-design) 구현

오늘 할 거 (~40분) — 한계 확인은 끝, 바로 개선
1. 하위 인덱스 만들기 — 평면 index를 타입별로 쪼개고 동명충돌 해소 (설치 0)
2. 개선 확인 — 타입 인덱스만 펼쳐 답하기, 전/후 비교
3. 하이브리드 RAG — 임베딩으로 시멘틱 + BM25 키워드 동시 검색, 점수 병합
- 영상 보면서 진행, 끝나면 `완료` 또는 `/wrap`

흐름:
1. 하위 인덱스 (타입별 MOC + 라우터)
2. 개선 확인 (people/index만 펼침 — 전/후)
3. 하이브리드 RAG 구현 (시멘틱+키워드)
4. 경계 + 정직 가드
```

---

## 절차 — 하위 인덱스 → 개선 확인 → 하이브리드 RAG (영상 보면서 진행)

### Phase 1. 하위 인덱스 만들기 — 타입별 계층 MOC (12분) · 본인 직접 · 설치 0

평면 `index.md` 하나에 모든 타입이 섞여 있어 ① 동명충돌(`Dune` 영화 vs 시리즈)이 비결정적이고 ② 어떤 질문이든 전체 목록을 1차로 읽는다. 이걸 **타입별 하위 인덱스 + 최상위 라우터**로 쪼갠다. (설계서 Part A)

**만드는 구조:**
```
40-wiki/
  index.md           # 최상위 = 라우터(카탈로그 아님): 타입별 하위 인덱스 링크 + 동명충돌 안내표
  works/index.md     # 작품만 (각 줄 description = 페이지 summary 단일출처)
  people/index.md    # 인물만
  series/index.md    # 시리즈만
  concepts/index.md  # 개념만
  sources/index.md   # (이미 존재) 원본 기사
```

**복사용 입력:**
```
평면 index.md를 타입별 하위 인덱스로 쪼개줘. works/people/series/concepts 각각 {type}/index.md를 만들고, 각 줄 description은 그 페이지의 summary를 단일 출처로 써. 최상위 index.md는 카탈로그가 아니라 타입별 하위 인덱스로 보내는 라우터로 바꾸고, Dune(영화 works vs 시리즈 series)처럼 같은 이름이 두 타입에 있는 건 동명충돌 안내표로 정리하고 본문 링크는 [[works/Dune|Dune]]·[[series/Dune|Dune]]처럼 경로 한정 위키링크로 바꿔줘.
```
| 확인 | `{type}/index.md`가 타입별로 생기고, 최상위 index가 라우터로 바뀜. `Dune` 같은 동명이 타입별로 분리됨 |

> 수강생은 분할 알고리즘을 짜는 게 아니라 **"타입별로 쪼개고 동명은 경로로 구분해"라고 묻는 법**을 익힌다. 동명충돌 해소(경로 한정 링크)가 이번 단계의 핵심 성과다.

### Phase 2. 개선 확인 — 타입 인덱스만 펼쳐 답하기 (8분) · 본인 직접

전체를 읽지 않고 **라우터 → 해당 타입 인덱스만** 펼쳐 답하게 한다. 전(평면 전체 읽기)/후(타입 인덱스) 차이를 눈으로 본다.

**복사용 입력:**
```
"봉준호 영화의 특징"을 답하는데, 최상위 index(라우터)를 먼저 읽고 관련 타입의 하위 인덱스만 펼쳐서 후보를 고른 다음 그 페이지들만 읽고 답해줘. 어떤 인덱스를 읽었는지랑 출처도 같이.
```
| 확인 | 인물 질문이라 `people/index.md`(+필요시 works) 위주로만 펼침 → 작품·시리즈 전체를 안 읽음. 빠르고 노이즈 적음. 동명충돌도 안 생김 |

| | 전 (평면 전체 읽기) | 후 (타입 인덱스만) |
|---|---|---|
| 읽는 양 | 전체 목록 | 관련 타입만 |
| 속도 | 느림 | 빠름 |
| 동명충돌 | 있음 | 없음 (타입 분리) |
| 설치 | 0 | 0 |

> 여기까지가 **설치 0으로 되는 개선**이다. "어지간하면 여기서 멈춰도 된다"는 선을 분명히 한다.

### Phase 3. 하이브리드 RAG 구현 — 시멘틱 + 키워드 (15분) · 본인 직접 · 임베딩 키 필요

설명 목록조차 버겁거나 의미 질문("씁쓸한 가족 드라마")을 잡으려면, 페이지를 **임베딩**해 시멘틱 검색을 올리고, 동시에 **키워드(BM25)** 검색을 돌려 **점수를 병합**한다. (설계서 Part B)

**구현 사양 (설계서 정본):**

| 항목 | 값 |
|---|---|
| 인덱싱 단위 | **2-tier 청킹** — 요약 tier(페이지 summary 1청크) + 본문 tier(섹션별 1청크). 원본 소스 1,000편도 인덱싱(롱테일 회수) |
| 컬렉션 분리 | 타입별(works/people/series/concepts/sources) — 동명충돌의 RAG판 해소. Phase 1 하위 인덱스와 같은 네임스페이스 |
| 메타데이터 facet | `page, type, title(정본), aka[], year, genres[], series[], tier, sources[], chunk_section` → type/tier 필터 |
| 임베딩 모델 | **`gemini-embedding-001`** (멀티링구얼 — 한/영 혼재 필수). 색인 `RETRIEVAL_DOCUMENT` / 쿼리 `RETRIEVAL_QUERY` task_type 구분 필수 |
| 저장소 | 로컬 경량 — **ChromaDB / sqlite-vec** (수천 벡터 규모). 위키 옆 `.rag/`에 저장, git 무시 |
| 검색 | **하이브리드** = 시멘틱(벡터) + 키워드(BM25) 점수 병합 + type/tier 필터. 타입 컬렉션에서 못 찾으면 `sources`로 폴백 |
| 쿼리 파이프라인 | ① alias 정규화·의도/타입 추론 → ② 하이브리드 검색 → ③ 리랭크(상위 k) → ④ 후보 페이지 tiered read + [[링크]] 1홉 → ⑤ 근거로만 답 + 정본 인용 |

**복사용 입력 (① 인덱스 구축):**
```
.rag/ 폴더에 RAG 인덱스를 만들어줘. 위키 페이지와 원본 소스를 2-tier(요약=summary 한 청크, 본문=섹션별 청크)로 쪼개고, 타입(works/people/series/concepts/sources)별 컬렉션으로 나눠서 Gemini gemini-embedding-001로 임베딩해(색인은 RETRIEVAL_DOCUMENT). 청크마다 page·type·title·year·tier·sources 메타데이터를 붙여줘. 저장은 로컬 벡터DB로.
```

**복사용 입력 (② 하이브리드 검색 적용):**
```
이제 질문을 받으면 키워드(BM25) 검색과 시멘틱(임베딩) 검색을 동시에 돌려서 점수를 병합하고, type/tier로 필터한 다음 상위 후보 페이지만 읽어서 답하게 해줘. 쿼리는 RETRIEVAL_QUERY로 임베딩하고, 타입 컬렉션에서 못 찾으면 sources로 폴백해. "씁쓸한 가족 드라마 같은 한국 영화"로 한번 검색해봐.
```
| 확인 | 키워드로는 안 잡히는 의미 질문이 시멘틱으로 회수되고, 정확한 제목·고유명사는 키워드로 보강됨 → 병합 결과로 답 + 출처 인용 |

> **정직 가드:** 하이브리드도 만능이 아니다 — top-K·임베딩 모델 품질·**summary 품질**에 좌우된다. 그래서 Phase 1에서 description(summary)을 본문 기반으로 충실히 써둔 게 여기서 정확도를 만든다. "토큰 N배·recall %" 같은 정량 단정은 하지 말고, 전/후를 직접 보여준다.

### Phase 4. 경계 + 정직 가드 (5분)

```
[선 긋기]
- 하위 인덱스(Phase 1·2): 설치 0. 동명충돌·tiered-read 낭비 해소. 어지간한 규모는 여기서 충분.
- 하이브리드 RAG(Phase 3): 의미 질문·롱테일 회수·설명 목록조차 버거운 규모. 임베딩·벡터DB 필요.
- 더 커지면: 관리형(Gemini File Search 등) 또는 Supabase pgvector(CH03에서 또 만남).
```

| | 평면 전체 읽기 | 하위 인덱스 | 하이브리드 RAG |
|---|---|---|---|
| 속도 | 느림 | 빠름 | 빠름 |
| 동명충돌 | 있음 | 해소 | 해소(타입 컬렉션) |
| 의미 질문 | 약함 | 약함 | 강함 |
| 롱테일 회수 | 누락 | 페이지 있어야 | 소스 청크로 회수 |
| 설치 | 0 | 0 | 임베딩·벡터DB |

> 마무리: "인덱스로 먼저 고치고, 모자라면 RAG. 느려지거나 빠지면 그게 다음 단계로 갈 신호 — 숫자보다 체감으로 판단."

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| "검색 명령을 직접 쳐야 하나요?" | "아니요. 클로드코드한테 '타입 인덱스만 펼쳐 답해'·'하이브리드로 검색해' 하면 안에서 알아서 합니다" |
| "Gemini 키가 없어요" | "Phase 3 시멘틱 검색에만 필요해요. Phase 1·2(하위 인덱스)는 키 없이 됩니다 — 키 발급 안내해줄게요" |
| "하위 인덱스랑 RAG는 따로인가요?" | "아니요, 타입(works/people…)이 곧 RAG 컬렉션이라 하위 인덱스가 RAG의 기초가 돼요" |
| "Dune이 영화/시리즈 섞여요" | "경로 한정 링크 [[works/Dune]]·[[series/Dune]]랑 타입 컬렉션 분리로 해소된다고 짚어줘" |
| "한국어 검색이 이상해요" | "임베딩을 멀티링구얼(gemini-embedding-001)로, 색인/쿼리 task_type을 맞춰야 한다고 설명해줘" |
| "키워드만/의미만 쓰면 안 되나요?" | "고유명사는 키워드, 모호 질문은 시멘틱이 강해서 둘을 병합해야 서로 약점을 메워요" |
| "회사 자료는 수십만 건인데요" | "그건 관리형(File Search)·pgvector로 갈 신호 — CH03 Supabase에서 또 만나요" |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리

### 1. 결과물 검증

```bash
ROOT="${ROOT:-$HOME/fastcampus-cc}"
if [ -d "$HOME/llm-wiki" ]; then WIKI="$HOME/llm-wiki"
elif [ -d "$HOME/Desktop/llm-wiki" ]; then WIKI="$HOME/Desktop/llm-wiki"
else WIKI="$HOME/llm-wiki"; fi
if [ -d "$WIKI/40-wiki" ]; then WP="$WIKI/40-wiki"; elif [ -d "$WIKI/wiki" ]; then WP="$WIKI/wiki"; else WP="$WIKI"; fi
WORK_DIR="$ROOT/50-my-work/Part07-실전/실습36-위키개선"

[ -f "$WORK_DIR/README.md" ] && echo "회고 기록 ✓" || echo "README 작성 필요"
echo "타입별 하위 인덱스:"
for t in works people series concepts sources; do
  [ -f "$WP/$t/index.md" ] && echo "  ✓ $t/index.md" || echo "  · $t/index.md 없음"
done
[ -d "$WIKI/.rag" ] && echo "RAG 인덱스(.rag/) ✓" || echo "RAG 인덱스 미구축(Phase 3 안 함 — Phase 1·2만으로도 OK)"
```

하위 인덱스 분할이 안 됐으면 Phase 1을, 전/후 차이를 못 봤으면 Phase 2를 다시 짚어준다. Phase 3(RAG)은 키 여건에 따라 선택 — 못 했어도 Phase 1·2 완료면 클립 목표 달성으로 본다.

### 2. README.md 자동 작성

`50-my-work/Part07-실전/실습36-위키개선/README.md`:

```markdown
# 실습 36 — 위키 한계와 개선 (하위 인덱스 → 하이브리드 RAG)

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 위키 경로: ~/llm-wiki/ (별도 워크스페이스)
- 정본 설계서: ~/llm-wiki/30-reports/2026-06-14-rag-index-design.md

## 무엇을 고쳤나 (한계는 지난 클립에서 확인)
- ① 하위 인덱스: 평면 index → 타입별 {type}/index.md + 라우터. 동명충돌(Dune)을 경로 한정 링크로 해소 (설치 0)
- ② 개선 확인: 타입 인덱스만 펼쳐 답 → 전체 읽기 대비 빠름·노이즈↓·동명충돌 없음
- ③ 하이브리드 RAG: 페이지를 Gemini로 임베딩(시멘틱) + BM25(키워드) 점수 병합 + 타입 컬렉션 필터

## 핵심 연결
- 타입(works/people/series/concepts/sources) = 하위 인덱스 분할 단위 = RAG 컬렉션/필터
- 그래서 하위 인덱스가 RAG의 기초 (둘은 같은 타입 네임스페이스 공유)

## 선 긋기 (내 규모는?)
- 어지간한 규모: 하위 인덱스(설치 0)로 충분
- 의미 질문·롱테일·설명 목록조차 버거움: 하이브리드 RAG(임베딩+벡터DB)
- 더 커지면: 관리형(Gemini File Search) / Supabase pgvector(CH03)

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 36"],
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

### 4. 회고 한 줄

> "하위 인덱스(설치 0)로 충분한가요, 아니면 하이브리드 RAG까지 가야 하나요? 내 자료 규모로 한 줄 적어주세요."

자유 입력으로 받아 README의 "핵심 발견 / 회고"에 기록.

> **CH 02 마무리:** clip-03에서 뼈대 세우고 → clip-04에서 채우고 질문했고 → clip-05에서 한계를 하위 인덱스 + 하이브리드 RAG로 고쳤습니다. 마크다운 + 클로드코드 + 가벼운 임베딩으로 LLM Wiki를 마무리했습니다.
> 다음: clip-06 — 세 번째 프로젝트, 유튜브 트렌드 대시보드(여기서 Supabase pgvector로 RAG를 또 만납니다).

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 브리핑+진행 안내를 한 메시지로 출력하고 영상 따라 진행
- **전부 본인 직접**: 한계 재현은 지난 클립에서 끝 — 오늘은 하위 인덱스·개선 확인·하이브리드 RAG를 직접 구현한다. (강사 시연-only 아님)
- **단계별 설치 경계 분명히**: Phase 1·2 = 설치 0 / Phase 3 = 임베딩 키·벡터DB 필요. 키 없으면 Phase 1·2만으로도 클립 목표 달성
- **하위 인덱스 = RAG의 기초**: 타입이 곧 컬렉션 — 둘을 따로 가르치지 말고 연결한다
- **실습 진행 방식**: 강사 1줄 입력 → 학생 1줄 입력 → 결과 같이 확인. STOP 분리 X
- **"~해줘" 금지 / "~하려는데 어떻게?" 강제** (memory: feedback_ask_how_pattern) — 단 복사용 입력은 실제 동작 프롬프트라 명령형 허용
- **정직 가드**: 하이브리드도 만능 아님(top-K·임베딩 품질·summary 품질). RAG는 적이 아니라 규모로 선 긋기. "토큰 N배·recall %" 정량 단정 X — 전/후를 직접 보여줌. 코퍼스 1,000+는 설계서가 예고한 RAG 도입 트리거를 넘은 것이므로 도입은 원칙 준수
- **정본은 설계서**: `~/llm-wiki/30-reports/2026-06-14-rag-index-design.md`와 충돌하면 설계서를 따른다
- **자유 진행 중 개입 X**: 명시적 도움 요청에만 응답
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **IDE는 안티그래비티**: VS Code 언급 X
