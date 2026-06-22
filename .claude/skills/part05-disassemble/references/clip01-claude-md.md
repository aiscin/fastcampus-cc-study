# Clip 01 — CLAUDE.md (AI에게 업무 매뉴얼 쓰기)

> Part 05 / Ch 01 / Clip 01 (실습 18) | 예상 시간: ~20분
> 결과물: `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/CLAUDE.md` (인터뷰로 본인 맞게 다듬은 학습 워크스페이스 매뉴얼)
> 패턴: **자동 셋업 → 도입 브리핑 → 실습 진행 → WRAP** (Part 04 공통 패턴)

---

## 자동 셋업

스킬 호출 직후 아래 Bash를 즉시 실행 (사용자에게 명령 보여주는 게 아니라 스킬이 직접).

```bash
# 강의 워크스페이스 루트 찾기
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
elif [ -d "$HOME/Desktop/fastcampus-cc" ]; then
  ROOT="$HOME/Desktop/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

SEED="$ROOT/.claude/skills/part05-disassemble/seed-my-cc-study"
TARGET="$ROOT/50-my-work/Part05-뜯어보기/my-cc-study"

# 이미 존재하면 백업 (덮어쓰기 방지)
if [ -d "$TARGET" ]; then
  BACKUP="$ROOT/50-my-work/Part05-뜯어보기/my-cc-study.bak.$(date +%Y%m%d-%H%M%S)"
  mv "$TARGET" "$BACKUP"
  echo "기존 ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/ → $BACKUP 백업"
fi

# 시드 복사
cp -r "$SEED" "$TARGET"

# 진도 폴더
WORK_DIR="$ROOT/50-my-work/Part05-뜯어보기/실습18-CLAUDEmd"
mkdir -p "$WORK_DIR"

echo "✓ ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/ 시드 복사 완료 (CLAUDE.md만 일부러 빠진 상태)"
echo "✓ $WORK_DIR 진도 폴더 준비 완료"
ls "$TARGET"
```

셋업 결과 한 줄 보고 후 아래 **CLAUDE.md 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## CLAUDE.md 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 공식 정의 | "CLAUDE.md is a special file that Claude Code automatically pulls into context when starting a conversation." |
| 한국어 풀이 | 워크스페이스에 두는 약속 노트. 새 세션 시작할 때마다 AI가 자동으로 읽음 |
| 본질 | "이 폴더에서 일할 땐 이렇게 해"라는 매뉴얼 한 장 |

### 위치 2가지

| 위치 | 적용 범위 |
|---|---|
| **워크스페이스 루트 `CLAUDE.md`** | 그 폴더에서만 (프로젝트별 규칙) |
| **`~/.claude/CLAUDE.md`** | 모든 프로젝트에 공통 (본인 전반 규칙) |

### 강의 워크스페이스 CLAUDE.md (REFERENCE — 절대 수정 X)

지금까지 강의가 한국어로 답하고, `50-my-work`에 자동 저장하고, `막혔어요`로 진단된 건 강의 워크스페이스 CLAUDE.md 덕분. 이 파일은 보기만 하고 수정 X.

핵심 섹션 3개:
- **기본 규칙** — 한국어 / 쉬운 말 / 시각적 결과물
- **자연어 트리거** — `막혔어요` → `/stuck` 매핑 같은 거
- **결과물 저장 규칙** — `50-my-work/...` 자동 저장

### 오늘 만들 것

`~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/` (방금 자동 생성됨)에 본인 맞춤 CLAUDE.md를 만든다.
- `/init` 으로 자동 초안 생성
- 인터뷰로 본인 직업/스타일 반영해서 다듬기
- 이 폴더는 강의 끝나고도 본인 학습 워크스페이스로 계속 사용

### 핵심 메시지

> CLAUDE.md 한 파일로 워크스페이스 동작이 결정된다.
> 강의 워크스페이스의 CLAUDE.md는 강사가 만든 것 — 학생은 본인 학습 워크스페이스에 본인 CLAUDE.md를 만들어 봄.

### 공식 문서 출처

- CLAUDE.md 메모리: https://docs.claude.com/en/docs/claude-code/memory
- /init 명령: https://docs.claude.com/en/docs/claude-code/cli-reference

---

## 진행 안내

```
✓ ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/ 자동 생성 완료 (CLAUDE.md만 빠진 상태)
✓ 50-my-work/Part05-뜯어보기/실습18-CLAUDEmd/ 진도 폴더 준비

오늘 할 거 (~20분)
- CLAUDE.md = 워크스페이스 약속 노트. AI가 새 세션마다 자동으로 읽음
- ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/는 강의 워크스페이스랑 별개 — 강의 끝나도 계속 본인 학습용
- 영상 보면서 진행, 끝나면 `완료` 또는 `/wrap`

5단계 흐름:
1. 강의 워크스페이스 CLAUDE.md 같이 보기 (안티그래비티 에디터에서)
2. 안티그래비티 새 창에서 ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/ 열기 → claude 실행
3. /init 입력 → 자동 초안 생성
4. 인터뷰 요청 같이 입력 → 5개 질문 같이 답변
5. exit → claude 재시작 → 같은 질문으로 Before/After 비교
```

---

## 절차 — 실습 (영상 보면서 진행)

### Phase 1. 강의 워크스페이스 CLAUDE.md 같이 보기 (3분)

| 단계 | 내용 |
|---|---|
| 1 | 안티그래비티 에디터에서 강의 워크스페이스 루트의 `CLAUDE.md` 열기 |
| 2 | "기본 규칙" 섹션 짚기 — 한국어 / 쉬운 말 / 시각적 결과물 |
| 3 | "자연어 트리거" 표 짚기 — `막혔어요` → `/stuck` 매핑 |
| 4 | "결과물 저장 규칙" 짚기 — `50-my-work/...` 자동 저장 |
| 5 | **★강조: 이 파일은 절대 수정 X** |

### Phase 2. ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study 들어가서 /init (4분)

| 단계 | 입력 (강사·학생 동시) | 확인 |
|---|---|---|
| 1 | 안티그래비티 새 창 열기 → `Open Folder` → `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/` 선택 | 새 창에 학습 워크스페이스 표시 |
| 2 | 안티그래비티 터미널에서 `ls` | README, 10-curriculum, 20-concepts, 30-resources, 40-ideas, sandbox 확인 (CLAUDE.md 없음) |
| 3 | 같은 터미널에서 `claude` | Claude Code 실행 (학습 워크스페이스 컨텍스트) |
| 4 | `> /init` | 폴더 분석 시작 |
| 5 | 1분 정도 대기 | CLAUDE.md 초안 생성 + 저장 완료 |
| 6 | 안티그래비티에서 새로 만들어진 `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/CLAUDE.md` 열기 | 초안 내용 확인 |

### Phase 3. 인터뷰로 같이 다듬기 (10분)

**같이 입력 (학습 워크스페이스의 클로드코드에):**

```
내가 클로드코드 공부하는 사람이라는 맥락이 더 반영되도록
CLAUDE.md를 인터뷰로 보완해줘.

한 번에 하나씩 5개 질문 후 종료.
- 내 직업/배경
- 답변 스타일 선호 (쉬운 말? 예시 많이?)
- 결과물 포맷 선호 (표/리스트/문서)
- 자주 다룰 주제
- 피해야 할 것
```

**5개 질문 답변 가이드** (강사가 본인 답으로 시연 + 학생도 같은 타이밍에 본인 답 입력):

| Q | 답변 가이드 |
|---|---|
| Q1. 직업/배경 | 본인 직업 한 줄 (가상 프로필 OK — 예: 마케팅 기획자 / 콘텐츠 운영자 / 직장인) |
| Q2. 답변 스타일 | 한국어 존댓말 / 쉬운 말 / 예시 많이 등 본인 선호 |
| Q3. 결과물 포맷 | 표 / 리스트 / 문서 / 3줄 요약 등 본인 선호 |
| Q4. 자주 다룰 주제 | 본인 업무·관심 분야 |
| Q5. 피해야 할 것 | 너무 긴 답변 / 영어 전문용어 그대로 나열 / 추상적 설명 등 |

답변 끝나면 AI가 CLAUDE.md를 다듬어서 저장. 안티그래비티에서 `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/CLAUDE.md` 다시 열어 변경 확인.

### Phase 4. Before/After 비교 (3분)

| 단계 | 입력 | 결과 |
|---|---|---|
| 1 | `exit` | 학습 워크스페이스의 Claude Code 종료 |
| 2 | `claude` | 재시작 (CLAUDE.md 재로드) |
| 3 | `> 클로드코드 더 공부하려면 뭐부터 보면 좋을까?` | 본인 직업/스타일 반영된 답변 확인 |

→ 본인 맥락 인식한 응답 차이 체감.

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| `/init` 안 먹음 | "클로드코드 버전 업데이트하는 법 알려줘" |
| `/init` 결과가 영어로 나옴 | "한국어로 다시 써줘" |
| 인터뷰가 2개 질문에서 끝남 | "5개 다 채워줘" |
| Before/After 차이 안 느껴짐 | "더 구체적으로 다듬어줘" |
| 인터뷰 답변에 개인정보 걱정 | "민감 정보 빼고 가상 프로필로" |
| `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/`에 이미 있다고 백업됨 | 정상 (자동 셋업이 안전 백업) |
| 강의 워크스페이스 CLAUDE.md 실수 수정 | "git에서 복원하는 법 알려줘" |
| 안티그래비티 새 창 어떻게 여는지 모름 | "안티그래비티에서 폴더 새 창으로 여는 단축키 알려줘" |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

> WRAP 입력은 **강의 워크스페이스의 클로드코드**에서 한다 (스킬이 거기서 동작 중이라).

---

## WRAP 자동 처리

트리거 받으면 스킬이 다음을 순서대로 실행:

### 1. 결과물 검증

```bash
[ -f "$ROOT/50-my-work/Part05-뜯어보기/my-cc-study/CLAUDE.md" ] && echo "CLAUDE.md 존재 ✓" || echo "CLAUDE.md 없음 ✗"
wc -l "$ROOT/50-my-work/Part05-뜯어보기/my-cc-study/CLAUDE.md"
```

CLAUDE.md 없으면 어디서 멈췄는지 안내 후 재시작 권유.

### 2. README.md 자동 작성

`~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습18-CLAUDEmd/README.md`:

```markdown
# 실습 18 — CLAUDE.md

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 학습 워크스페이스 경로: ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/

## CLAUDE.md 정리 (공식 문서 기반)

### 한 줄 정의
| 항목 | 내용 |
|---|---|
| 공식 정의 | "CLAUDE.md is a special file that Claude Code automatically pulls into context when starting a conversation." |
| 한국어 풀이 | 워크스페이스에 두는 약속 노트. 새 세션 시작할 때마다 AI가 자동으로 읽음 |

### 위치 2가지
- 워크스페이스 루트 CLAUDE.md = 그 폴더에서만
- ~/.claude/CLAUDE.md = 모든 프로젝트 공통

## 만든 흐름
1. 강의 워크스페이스 CLAUDE.md 참고 (수정 X)
2. ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/ 시드 자동 받음 (스킬이 처리)
3. /init으로 자동 초안 생성
4. 인터뷰 5개 질문으로 본인 맞춤 다듬기
5. Before/After 같은 질문 비교

## 본인 CLAUDE.md 핵심 (요약)
- 직업: {Q1 답변}
- 답변 스타일: {Q2 답변}
- 결과물 포맷: {Q3 답변}
- 자주 다룰 주제: {Q4 답변}
- 피해야 할 것: {Q5 답변}

## 강의 후 활용
- ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/는 강의 끝나도 본인 클로드코드 공부 워크스페이스로 계속 사용
- 강의 워크스페이스(~/Desktop/fastcampus-cc/)는 절대 수정 X

## 공식 문서 출처
- https://docs.claude.com/en/docs/claude-code/memory
- https://docs.claude.com/en/docs/claude-code/cli-reference

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 18"],
  "my_cc_study_path": "~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study",
  "my_cc_study_initialized": true,
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

### 4. 회고 한 줄

> "이번 클립에서 가장 인상적이었던 거 한 줄로 적어주세요."

### 5. 다음 클립 안내

```
실습 18 완료. ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/CLAUDE.md가 본인 맞춤으로 저장됐습니다.

★ 오늘 후 안내:
- ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/는 강의 끝나도 계속 본인 학습용으로 쓸 폴더예요.
- 다음에 안티그래비티에서 ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/ 열고 claude 실행하면 바로 시작 가능.
- 강의 워크스페이스(~/Desktop/fastcampus-cc/)는 강의용 — 절대 수정 X.

다음은 Clip 02 — 커맨드 & 서브에이전트.
강의 워크스페이스의 /stuck 같은 커맨드가 어떻게 만들어졌는지 보고,
본인 커맨드도 ~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/.claude/commands/에 만듭니다.

시작하려면 /part05 다시 호출하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 메시지로 출력하고 영상 따라 진행
- **실습 진행 방식**: 강사 1줄 → 학생 1줄 → 결과 같이 확인. STOP 분리 X
- **강의 워크스페이스 절대 수정 X**: 모든 변경은 `~/fastcampus-cc/50-my-work/Part05-뜯어보기/my-cc-study/`에서만
- **자유 진행 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **IDE는 안티그래비티**: VS Code 언급 X — 안티그래비티 / 에디터 / 터미널 표현
