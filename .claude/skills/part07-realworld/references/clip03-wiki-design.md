# Clip 03 — LLM Wiki 이해하고 내 지식베이스 설계 + 뼈대 세우기 (실습 34)

> Part 07 / CH 02 LLM Wiki / Clip 03 (실습 34) | 예상 시간: ~22분
> 결과물: 위키 아키텍처 설계도 1장 + 빈 위키 뼈대(`llm-wiki/` raw/ wiki/ CLAUDE.md — 자료는 아직 0)
> 패턴: **자동 셋업 → 브리핑 → 설계 + 뼈대 → WRAP**
> 페르소나 메모 — A(마케터): RAG·벡터DB 용어 부담이라 비유로 빠르게 / B(PO): 4동사 루프 구조를 또렷이 / C(영업): "내 자료가 쌓일수록 똑똑해진다" 가치

---

## 자동 셋업

스킬 호출 직후 아래 Bash를 즉시 실행 (사용자에게 명령을 보여주는 게 아니라 스킬이 직접).

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

WORK_DIR="$ROOT/50-my-work/Part07-실전/실습34-위키설계"
mkdir -p "$WORK_DIR"

# 강의 다이어그램(있으면) 복사 — RAG / LLM Wiki 아키텍처
ASSET="$ROOT/.claude/skills/part07-realworld/assets/clip-diagrams"
cp "$ASSET/rag-architecture.png" "$ASSET/llm-wiki-architecture.png" "$WORK_DIR/" 2>/dev/null && echo "✓ 강의 다이어그램(RAG·LLM Wiki) 복사"

echo "✓ $WORK_DIR 진도 폴더 준비 완료"
echo "  오늘 결과물: 위키 설계도 1장 + 빈 위키 뼈대(llm-wiki/)"
echo "  위키 본체는 fastcampus-cc 밖 별도 워크스페이스 $WIKI 에 만듭니다 (진도 README만 50-my-work에)"
```

셋업 결과를 한 줄로 보고한 뒤, 아래 **브리핑 + 진행 안내**를 한 메시지로 출력하고 SLEEP.

---

## 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 한 줄 | AI가 내 자료를 읽어서 마크다운 위키를 직접 짓고, 자료가 늘 때마다 계속 고쳐주는 지식베이스 |
| 본질 | 검색처럼 매번 찾는 게 아니라, **한 번 정리한 게 쌓여서 쓸수록 똑똑해짐** |
| 출처 | 안드레이 카파시가 정리한 패턴 (개인이 만든 게 아님) |

### 검색(RAG)과 뭐가 다른가

| | 검색 기반 (RAG) | LLM Wiki |
|---|---|---|
| 처리 시점 | 질문할 때마다 조각을 새로 찾음 | 자료 넣을 때 한 번 정리·연결 |
| 축적 | 안 쌓임 (조각을 찾을 뿐, 이해·연결이 누적 안 됨) | 쌓임 (정리·답이 누적) |
| 도구 | 보통 검색·벡터DB로 거듦 | 기본은 마크다운 폴더 (커지면 검색 선택적 추가) |

> RAG가 나쁜 게 아니라 **규모로 선을 긋는 것** — 수십~수백·천 개는 마크다운으로 충분하고, 더 커지면 그때 검색을 더한다(clip-05에서 다룸). 벡터DB 깊이 설명은 X (비개발자 부담).

### 아키텍처 — 세 칸 (3계층)

| 칸 | 역할 | 비유 |
|---|---|---|
| `raw/` | 원본 자료. **AI는 읽기만, 안 고침** | 박물관 유리장 |
| `wiki/` | AI가 만든 정리 페이지 (인물·작품·개념) | 정리된 서가 |
| `CLAUDE.md` | 정리 규칙 = 위키의 두뇌 (schema) | 사서 매뉴얼 |

> **중심에서 일하는 건 클로드코드다** — CLAUDE.md(규칙)를 읽고, raw를 읽어 wiki를 쓰고, 질문에 답한다. `CLAUDE.md`는 **clip-02에서 배운 그 CLAUDE.md 방식** — 위키 폴더 안 `llm-wiki/CLAUDE.md`로 두면 위키의 두뇌(정리 규칙)가 된다. 출처는 각 페이지 frontmatter의 `sources:`에 단다(별도 sources 파일 아님).

### Part 6 콜백 — 스킬이 이미 미니 위키였다

> Part 6에서 스킬 만들 때 사실 같은 골격을 이미 만졌다 — 규칙서(SKILL.md)에 필요한 자료(references)를 붙여 **필요할 때만 골라 읽게** 한 것. (위키도 똑같이 index 보고 필요한 페이지만 읽음)
> LLM Wiki는 거기에 ① 원본(raw)에서 스스로 정리 ② 페이지끼리 `[[링크]]` ③ 계속 자라는 루프를 더한 것.
> 즉 새 패러다임이 아니라 **이미 만들어온 걸 목적 하나로 조립**한 것 — Part 7 전체 메시지의 연장.

### 만들기(init) → 4동사 루프 — 오늘 어디까지

> **init은 처음 한 번만** 하는 뼈대 세우기(루프 아님). 그 빈 뼈대 위에서 아래 4동사가 돈다.

| 단계 | 하는 일 | 어느 클립 |
|---|---|---|
| **만들기(init)** · 1회 | 빈 위키 뼈대(폴더 + 규칙서) 세우기 | **오늘(clip-03) 여기까지** |
| ┄ 4동사 루프 ┄ | | |
| 투입(ingest) | raw/에 자료 넣기 | clip-04 |
| 정리(compile) | AI가 raw → wiki 페이지 생성 | clip-04 |
| 질문(query) | 위키에 묻고, 좋은 답은 다시 위키에 저장 | clip-04 |
| 점검(lint) | 끊긴 링크·중복·모순 정리 | clip-05 |

### 핵심 메시지

> 검색은 매번 처음부터 긁어모으고, LLM Wiki는 한 번 이해한 걸 계속 키운다.
> 심지어 **질문해서 나온 답도 위키에 쌓인다** — 그 장면은 다음 클립에서 직접 만든다.
> 오늘은 **설계도 + 빈 뼈대**까지. 자료 채우기는 다음 클립.
> 옵시디언 같은 별도 앱 불필요 — 클로드코드가 직접 폴더를 읽고 쓴다.

### 공식 출처

- Karpathy LLM Wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## 진행 안내

```
✓ 50-my-work/Part07-실전/실습34-위키설계/ 진도 폴더 준비

오늘 할 거
- LLM Wiki = AI가 짓고 유지하는 마크다운 지식베이스 (검색과 달리 쌓인다)
- raw / wiki / CLAUDE.md 세 칸 구조 + 4동사 루프 이해
- 내 위키 설계도 4칸 채우기
- clip-02 빌더로 빈 위키 뼈대 찍기 (자료는 다음 클립)
- 영상 보면서 진행, 끝나면 `완료` 또는 `/wrap`

2단계 흐름:
1. 위키 설계도 4칸 채우기 (무슨 자료 / raw / wiki 주제 / 정리 규칙)
2. clip-02 빌더로 빈 위키 뼈대 세우기 (raw/ wiki/ CLAUDE.md)
```

---

## 절차 — 설계 + 뼈대 (영상 보면서 진행)

### Phase 1. 위키 설계도 채우기 (말로 — 클로드코드 화면 아직 X)

설계도는 네 줄. 강사는 영화로 예시를 보여주고, 학생은 본인 주제로 채운다.

```
1. 무슨 자료를 모을까:   (예: 영화 감상 / 마케팅 사례 / 내 분야 자료)
2. raw에 넣을 것:        (원본 형태 — md·기사·메모)
3. wiki 페이지 주제:     (엔티티 단위 — 인물·작품·개념·프레임워크)
4. 정리 규칙(CLAUDE.md): (페이지 frontmatter에 description:·sources: 필수 / 같은 대상은 같은 이름 / [[링크]])
```

| 칸 | 강사 예시(영화) | 학생 |
|---|---|---|
| 1 자료 | 영화 감상 + 인물·작품 정보 | 본인 주제 |
| 2 raw | 감상 메모, 기사 | 본인 원본 |
| 3 wiki 주제 | 인물 / 작품 / 장르 | 본인 엔티티 |
| 4 규칙 | frontmatter에 `description:`·`sources:`, 같은 사람=같은 이름, `[[링크]]` | 동일 원칙 |

> **규칙 4번의 "한 줄 설명(description)"이 중요** — 나중에 위키가 커지면 이 설명만 보고 필요한 페이지를 찾는다(clip-05). 그래서 처음부터 규칙서에 박아둔다.

### Phase 2. clip-02 빌더로 빈 위키 뼈대 세우기 (클로드코드)

설계도가 채워지면, clip-02에서 만든 워크스페이스 빌더를 다시 꺼내 빈 뼈대를 찍는다. **"~해줘"가 아니라 "~하려는데 어떻게?" 패턴.**

**복사용 입력 (강사·학생 동시):**
```
지난 시간에 배운 워크스페이스 만드는 방식으로, 영화 자료를 정리할 LLM Wiki를 별도 워크스페이스(~/llm-wiki)로 하나 만들려고 해. fastcampus-cc 안이 아니라 독립 폴더로.
raw / wiki 폴더랑, 정리 규칙을 적을 CLAUDE.md까지 — 자료는 아직 안 넣고 빈 뼈대만.
CLAUDE.md엔 "각 위키 페이지 frontmatter에 description(본문 기반 한 줄)과 sources(출처)를 단다"는 규칙도 넣어줘.
지식베이스 아키타입으로 잡으려는데 어떻게 하면 좋을까?
```

| 확인 | 내용 |
|---|---|
| 폴더 | `llm-wiki/raw/`, `llm-wiki/wiki/` 생성됨 |
| 두뇌 | `llm-wiki/CLAUDE.md`에 설계도 4번 규칙(`description:`·`sources:`·이름·`[[링크]]`)이 들어감 |
| 자료 | **아직 0** — 빈 위키 (매장 오픈 전 진열장만 갖춘 상태) |

> clip-02 빌더가 없거나 안 떠도 괜찮다 — "빌더 없이 그냥 raw/ wiki/ 폴더랑 CLAUDE.md 규칙서만 직접 만들어줘"로 폴백.
> 자료 채우기(투입·정리·질문)는 다음 클립에서 한 바퀴 돈다.

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| "RAG·벡터DB가 뭐예요?" | "자료를 잘게 잘라 그때그때 찾는 방식. 우리 규모엔 과해서 안 쓴다고 설명해줘" |
| "옵시디언 깔아야 해요?" | "아니요. 클로드코드가 직접 파일을 읽고 써요. 그래프는 나중에 그려달라고 하면 됨" |
| 빈 뼈대인데 자료부터 넣으려 함 | "오늘은 뼈대까지예요. 투입은 다음 클립" |
| CLAUDE.md(schema)가 안 와닿음 | "clip-02에서 배운 CLAUDE.md 방식 그대로, 위키 폴더 안 llm-wiki/CLAUDE.md가 규칙서라고 짚어줘" |
| clip-02 빌더가 없음/안 뜸 | "빌더 없이 raw/ wiki/ 폴더랑 CLAUDE.md 규칙서만 직접 만들어줘" |
| 빌더가 폴더를 엉뚱한 곳에 만듦 | "llm-wiki 위치를 다시 잡아줘" |

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
[ -d "$WIKI/raw" ] && [ -d "$WIKI/wiki" ] && echo "위키 뼈대 ✓" || echo "뼈대 미완성 ✗"
[ -f "$WIKI/CLAUDE.md" ] && echo "schema(CLAUDE.md) ✓" || echo "CLAUDE.md 없음 ✗"
```

뼈대가 없으면 어디서 멈췄는지 안내 후 Phase 2 재시도 권유.

### 2. README.md 자동 작성

`50-my-work/Part07-실전/실습34-위키설계/README.md`:

```markdown
# 실습 34 — LLM Wiki 설계 + 뼈대 세우기

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 위키 경로: ~/llm-wiki/ (별도 워크스페이스, fastcampus-cc 밖)

## LLM Wiki 핵심 (브리핑 요약)
- 검색(RAG)은 매번 찾고 안 쌓임 / LLM Wiki는 한 번 정리한 게 쌓임
- 3계층: raw(원본·불변) / wiki(AI 정리) / CLAUDE.md(규칙=두뇌)
- init(1회) → 4동사 루프: 투입 → 정리 → 질문 → 점검
- 페이지마다 한 줄 설명(description)·출처 규칙 (나중에 검색의 기반)

## 내 위키 설계도
1. 모을 자료: {입력}
2. raw: {입력}
3. wiki 주제: {입력}
4. 정리 규칙: {입력}

## 오늘 만든 것
- 빈 위키 뼈대(llm-wiki/ raw/ wiki/ CLAUDE.md) — 자료는 다음 클립에서 투입

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 34"],
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

### 4. 회고 한 줄

> "검색과 LLM Wiki의 차이, 한 줄로 적어주세요."

자유 입력으로 받아 README의 "핵심 발견 / 회고"에 기록.

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 브리핑+진행 안내를 한 메시지로 출력하고 영상 따라 진행
- **실습 진행 방식**: 강사 1줄 입력 → 학생 1줄 입력 → 결과 같이 확인. STOP 분리 X (따라치기)
- **"~해줘" 금지 / "~하려는데 어떻게?" 강제** (memory: feedback_ask_how_pattern)
- **오늘 범위는 뼈대까지** — 자료 투입·정리·질문은 clip-04, 점검은 clip-05
- **description 규칙을 꼭 심기** — 페이지마다 한 줄 설명, 나중에 검색(clip-05)의 기반
- **자유 진행 중 개입 X**: 명시적 도움 요청(`막혔어요`/`도와줘`)에만 응답
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **IDE는 안티그래비티**: VS Code 언급 X
- **정량 수치 단정 금지**: "토큰 N배 절감·recall %" 같은 단정 X — 정성적 가치(축적·소유·설명가능)로
