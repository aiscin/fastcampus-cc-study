# 레퍼런스 — LLM Wiki RAG 구현 가이드 (실습 36)

> 이 문서는 실습 36에서 만든 하이브리드 RAG가 **안에서 실제로 어떻게 도는지** 정리한 참고 자료입니다.
> 명령어를 직접 칠 일은 없습니다 — 클로드코드한테 "이렇게 해줘"라고 하면 아래 과정을 알아서 처리합니다.
> 정본 설계서: `~/llm-wiki/30-reports/2026-06-14-rag-index-design.md`

---

## 한 문장 요약

위키 글들을 "의미가 담긴 숫자(임베딩)"로 바꿔 작은 검색 창고(`.rag/`)에 넣어두고, 질문이 오면
**의미 검색 + 단어 검색**을 같이 돌려 점수를 합쳐 가장 관련 있는 글만 찾아 읽고 답한다.

---

## 전체 그림 — 2단계

```
[A. 색인 만들기 — 한 번만, 미리]
 위키 페이지 + 원본 기사
        │  ① 잘게 쪼갠다 (2-tier 청킹)
        ▼
   글 조각(청크) 수천 개
        │  ② Gemini로 숫자 벡터로 변환 (임베딩)
        │  ③ 메타데이터(type/tier/...) 꼬리표 부착
        ▼
   .rag/ 벡터 창고에 저장  ← 타입별(works/people/...) 칸 분리

[B. 질문이 올 때 — 매번]
 "씁쓸한 가족 드라마 같은 한국영화"
        │  ④ 의미 검색(벡터) + 단어 검색(BM25) 동시
        ▼
   점수 병합 → 상위 후보 글 추림 (type/tier 필터)
        │  ⑤ 후보 페이지만 펼쳐 읽고 [[링크]] 1홉 보강
        ▼
   ⑥ 읽은 근거로만 답 + 정본 출처 인용
```

---

## A단계 — 색인 만들기

### ① 청킹 (2-tier) — 글을 왜 쪼개나
글을 통째로 숫자화하면 "대충 무슨 얘기"까지만 잡힌다. 그래서 두 겹으로 쪼갠다.

| 겹 | 단위 | 쓰임 |
|---|---|---|
| 요약 tier | 페이지 1장 = summary 1청크 | 빠른 후보 추리기 |
| 본문 tier | 섹션별(줄거리/평가/연결…) 1청크 | 정밀 회수·인용 |

- **원본 기사도 같이 인덱싱** → 위키 페이지가 없는 롱테일 엔티티(조연 등)도 기사 내용으로 검색됨.
- 청크마다 출처(page path + sources raw id) 보존 → 인용·provenance 유지.

### ② 임베딩 — 글을 숫자로
- 모델: **`gemini-embedding-001`** (멀티링구얼 — 한/영 혼재 필수: 기생충/Parasite).
- task_type 구분 필수: 색인 `RETRIEVAL_DOCUMENT` / 쿼리 `RETRIEVAL_QUERY`.
- alias 쿼리 확장 병행: "Parasite"→["Parasite","기생충"]로 정규화해 음차 고유명사 보완.

### ③ 메타데이터 facet — 검색·동명충돌의 핵심
각 청크에 부착: `{ page, type, title(정본), aka[], year, genres[], series[], provenance, tier, sources[], chunk_section }`
- **type** 필터 → `Dune`(work) vs `Dune`(series) 분리 = 동명충돌의 RAG판 해소.
- **tier** 필터 → 미검수(`tier:auto`) 후순위/제외.
- 이 type이 곧 Phase 1 하위 인덱스 폴더(works/people/...)와 **같은 네임스페이스**.

### ④ 저장 — 경량 로컬
- 수천 벡터 규모 → **ChromaDB / sqlite-vec / LanceDB** 충분 (서버 불필요).
- 위키 옆 `.rag/`에 저장, git 무시(파생물).

---

## B단계 — 질문이 올 때

### ④ 하이브리드 검색 — 왜 둘 다
| 방식 | 강점 | 약점 |
|---|---|---|
| 시멘틱(벡터) | "씁쓸한 가족 드라마" 모호 의미 | 정확한 제목·고유명사 약함 |
| 키워드(BM25) | "기생충", 정확 제목 | 의미 유사 약함 |
| 하이브리드(점수 병합) | 서로 약점 보완 | — |

- type/tier 필터 적용, 해당 타입 컬렉션에서 못 찾으면 `sources`로 폴백.

### ⑤⑥ 읽고 답하기 — 기존 원칙 그대로
- 상위 후보 페이지만 tiered read + `[[링크]]` 1홉 보강.
- 근거로만 답 + 정본 인용 + provenance. 근거 없으면 "위키에 없음" 또는 lazy-gen.
- **RAG가 바꾸는 건 '후보 찾기'(④)뿐** — 읽고·인용하고·근거 대는 원칙은 불변.

---

## 쿼리 파이프라인 (설계서 §B-5)

```
질문
 → ① alias 정규화 + 의도/타입 추론
 → ② 하이브리드 검색(벡터 + BM25 + type/tier 필터)
 → ③ 리랭크(상위 k)
 → ④ 후보 페이지 tiered read + [[링크]] 1홉
 → ⑤ 근거로만 답 + 정본 인용 + provenance
```

---

## 정직 가드 — RAG도 만능 아님
세 가지에 좌우된다:
1. **top-K** — 가져오는 개수
2. **임베딩 품질** — 한국어면 멀티링구얼 필수
3. **summary 품질** ← 가장 중요. Phase 1에서 description(summary)을 본문 기반으로 충실히 써둔 게 정확도를 만든다. 그래서 ①(하위 인덱스)이 ③(RAG)의 토대.

> "토큰 N배·recall %" 정량 단정 금지(단일 출처). 전/후를 직접 보여줘 판단.

---

## 선 긋기 (내 규모는?)

| 규모 | 도구 |
|---|---|
| 수백~수천 | 하위 인덱스(마크다운, 설치 0) |
| 의미 질문·롱테일·설명 목록조차 버거움 | 하이브리드 RAG(임베딩+벡터DB) |
| 수만~수십만 | 관리형(Gemini File Search) / Supabase pgvector |

> **CH03 연결:** 오늘 쓴 벡터DB를 유튜브 대시보드의 Supabase가 `pgvector`로 똑같이 품는다. 도구만 다르고 원리는 같다.

---

## 공식 출처
- 정본 설계서: `~/llm-wiki/30-reports/2026-06-14-rag-index-design.md`
- Gemini 임베딩(`gemini-embedding-001`, 멀티링구얼): https://ai.google.dev/gemini-api/docs/embeddings
- ChromaDB: https://docs.trychroma.com · sqlite-vec: https://github.com/asg017/sqlite-vec
- Supabase pgvector: https://supabase.com/docs/guides/database/extensions/pgvector
- Karpathy LLM Wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
