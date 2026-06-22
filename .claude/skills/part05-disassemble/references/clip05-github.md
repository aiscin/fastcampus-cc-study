# Clip 05 — GitHub (git-teacher로 백업하기)

> Part 05 / Ch 01 / Clip 05 (실습 22) | 예상 시간: ~20분
> 결과물: 학습 워크스페이스(`~/fastcampus-cc/`) 전체를 GitHub Private repo로 백업 + 한국어 자연어 git 사용
> 패턴: **실습** — 강사 1줄 입력 → 학생 같은 줄 입력 → 결과 같이 확인

---

## 자동 셋업

스킬 호출 직후 아래 Bash를 즉시 실행 (사용자에게 명령 보여주는 게 아니라 스킬이 직접).

```bash
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

# 50-my-work 메타 폴더 준비
WORK_DIR="$ROOT/50-my-work/Part05-뜯어보기/실습22-GitHub"
mkdir -p "$WORK_DIR"

# 백업 대상 자산 확인
echo "✓ $WORK_DIR 준비 완료"
echo ""
echo "백업 대상 자산 (~/fastcampus-cc/):"
ls -la "$STUDY_DIR" 2>/dev/null | grep -E "CLAUDE|\\.claude|\\.mcp|sandbox" | awk '{print "  - " $NF}'

# git / gh CLI 확인
echo ""
echo "필수 도구 확인:"
command -v git && echo "  ✓ git $(git --version | awk '{print $3}')" || echo "  ✗ git 미설치 (Part 02에서 설치됐어야 함)"
command -v gh && echo "  ✓ gh $(gh --version | head -1 | awk '{print $3}')" || echo "  ⚠ gh 미설치 — git-teacher가 자동 안내"

# git-teacher 설치 여부
if [ -d "$HOME/.claude/plugins/cache/gptaku-plugins/git-teacher" ]; then
  echo "  ✓ git-teacher 플러그인 설치됨"
else
  echo "  ℹ git-teacher 미설치 — STEP 1에서 설치 진행"
fi
```

셋업 결과 한 줄 보고 후 아래 **GitHub & git-teacher 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## GitHub & git-teacher 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 한 줄 | 본인 워크스페이스를 GitHub에 영구 백업 + 어디서나 접근 |
| 비유 | Google Drive (자동 동기) vs Git (수동 동기 — commit + push 두 단계) |
| 사용 도구 | git-teacher 플러그인 (한국어 자연어로 git 사용) |
| 결과 | GitHub Private repo + commit 히스토리 |

### Google Drive vs Git

| Google Drive | Git |
|---|---|
| 자동 동기 — 저장하면 바로 클라우드 | 수동 동기 — 저장(commit) + 업로드(push) 두 단계 |
| 한 번 로그인 끝 | repo마다 commit + push |
| 폴더 공유 | repo Collaborators / Pull Request |
| 버전 자동 보존 | commit 히스토리 — 의도적으로 만들기 |

**핵심 차이 하나:** Google Drive는 자동, Git은 **수동**.

### git-teacher 자연어 트리거

| 한국어 | git 명령 |
|---|---|
| "깃 시작해줘" | git init + .gitignore + GitHub 연결 |
| "저장해줘" | git add + git commit (자연어 메시지 자동) |
| "올려줘" | git push (필요 시 repo 자동 생성) |
| "검토 요청해줘" | gh pr create (선택 — 협업 시) |

### 핵심 메시지

> **본인 워크스페이스 = GitHub 영구 백업.** 다른 컴퓨터에서 `git clone`만 하면 같은 환경 재현. git-teacher는 평생 활용 가능한 자산.

---

## 진행 안내

```
✓ 50-my-work/Part05-뜯어보기/실습22-GitHub/ 준비 완료
✓ ~/fastcampus-cc/ 백업 대상 자산 확인 완료

오늘 할 거 (~20분)
- Google Drive vs Git 비유 (자동 vs 수동 동기)
- git-teacher 플러그인 설치 + 한국어 자연어 git 사용
- 학습 워크스페이스 전체를 GitHub Private repo로 백업
- 수정 → 재저장 루프 한 번
- Part 05 전체 마무리

5단계 흐름:
1. 비유 + git-teacher 설치
2. "깃 시작해줘" — setup + GitHub 계정 연결
3. "저장해줘" — 첫 commit
4. "올려줘" — GitHub push
5. 수정 → 재저장 루프

★ GitHub 계정 미보유면 강의 중 가입 (1-2분)
★ Private repo 권장 (settings.json에 개인 정보 가능성)
★ 강의 워크스페이스 (~/fastcampus-cc/) 절대 백업 X
  본인 백업은 ~/fastcampus-cc/만
```

---

## 단계별 진행 가이드

### STEP 1. 비유 + git-teacher 설치 (3분)

**[목적]** Google Drive vs Git 비유로 핵심 차이 이해 + git-teacher 플러그인 설치.

**[Claude Code 입력 — 마켓플레이스 추가]** (강의 워크스페이스에서)

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
```

**[Claude Code 입력 — 플러그인 설치]**

```
/plugin install git-teacher
```

**[활성화]** `exit` → `claude` 재시작.

---

### STEP 2. "깃 시작해줘" — setup + GitHub 계정 연결 (4분)

**[목적]** 학습 워크스페이스를 git 프로젝트로 초기화 + GitHub 계정 연결.

**[작업 위치 변경]** 안티그래비티 새 창에서 `~/fastcampus-cc/` 열고 통합 터미널에서 `claude` 실행.

**[Claude Code 입력]** (학습 워크스페이스 클로드코드에)

```
깃 시작해줘
```

**[git-teacher 자동 5 STEP]**
1. Git 설치 확인
2. GitHub CLI(gh) 확인 — 미설치면 설치 명령 안내 (Mac: `brew install gh` / Win: `winget install --id GitHub.cli`)
3. `gh auth login` 인증 (브라우저 OAuth)
4. `git init` 실행
5. `.gitignore` 자동 생성 (민감 파일 제외 — `.DS_Store`, `*.log`, `node_modules/` 등)

**[GitHub 계정 미보유 학생 안내]** `https://github.com/signup` 1-2분 가입 후 다시 시도.

---

### STEP 3. "저장해줘" — 첫 commit (4분)

**[목적]** 지금까지 만든 자산을 한 번에 commit.

**[Claude Code 입력]**

```
저장해줘
```

**[git-teacher 자동 분석]**
- `~/fastcampus-cc/` 변경 사항 감지
- CLAUDE.md / commands/ / agents/ / .mcp.json / settings.json / sandbox/ 식별
- 자연어 commit 메시지 자동 생성 (예: "init: Part 05 학습 자산 — CLAUDE.md, 커맨드, 서브에이전트, MCP, Hook")

**[학생 컨펌]** Y / 또는 메시지 수정 요청.

**[검증]**

```bash
git log --oneline | head
```

→ 첫 commit 해시 + 메시지 확인.

---

### STEP 4. "올려줘" — GitHub push (3분)

**[목적]** GitHub Private repo 자동 생성 + 첫 push.

**[Claude Code 입력]**

```
올려줘
```

**[git-teacher 자동 진행]**
- repo 이름 제안: `fastcampus-cc`
- 공개 설정: **Private** (권장)
- `gh repo create fastcampus-cc --private` 자동 실행
- `git remote add origin` + `git push -u origin main`
- 완료 후 GitHub URL 제시

**[검증]** 브라우저에서 GitHub URL 열어서 파일 확인. 본인 모든 자산 업로드 확인.

**[Private 안내]** 본인만 보임. 팀 공유 필요 시 GitHub Settings → Collaborators 추가.

---

### STEP 5. 수정 → 재저장 루프 (2분)

**[목적]** 일상 git 활용 흐름 — 수정 → "저장하고 올려줘" 한 번에.

**[작업]** 안티그래비티에서 `~/fastcampus-cc/CLAUDE.md` 한 줄 추가 (예: "오늘 학습 완료: Part 05").

**[Claude Code 입력]**

```
방금 CLAUDE.md 수정한 거 저장하고 GitHub에 올려줘
```

**[git-teacher 자동 진행]**
- 변경 감지 (`git diff`)
- 자동 commit 메시지 생성 (예: "update: 학습 진도 메모 추가")
- commit + push 한 번에

**[검증]** GitHub repo 페이지 새로고침 → 새 commit 반영 확인.

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| `gh` 명령 없음 | "GitHub CLI 설치하려는데 어떻게 해?" → Mac: `brew install gh` / Win: `winget install --id GitHub.cli` |
| `gh auth login` 인증 실패 | "gh auth logout 후 재인증하려는데 어떻게 해?" |
| `git push` permission 거부 | "remote URL이 잘못된 거 같아 — 다시 설정하려는데 어떻게 해?" |
| `.gitignore` 잘못 설정 — 중요 파일 제외 | "`.gitignore` 열어서 수정하려는데 어떻게 해?" |
| 대용량 파일 push 거부 (100MB+) | "sandbox 스크린샷이 큰 거 같아 — `.gitignore` 추가하려는데 어떻게 해?" |
| Private인데 Public으로 실수 생성 | "GitHub Settings → Change visibility → Private" |
| 커밋 메시지 영어/엉망 | "한국어 + 명확하게 다시 만들려는데 어떻게 해?" → amend |
| API 키 같은 거 실수로 올림 | **즉시 키 revoke** + "API 키 노출됐어, 즉시 대응 방법" |
| GitHub 계정 없음 | `https://github.com/signup` 가입 후 재시도 |
| 강의 워크스페이스 백업 시도 | "그건 강의 워크스페이스. 본인 백업은 ~/fastcampus-cc/만" |
| git 처음이라 무서움 | "git-teacher가 다 안내해줘요. 명령어 외울 필요 없음" |
| commit 메시지 의미 모름 | git-teacher 자동 한국어 메시지 활용 |
| Pull Request 헷갈림 | "검토 요청 — 이번엔 안 다룸. 팀 협업할 때 추가 학습" |
| GitHub repo 삭제하고 싶음 | "GitHub Settings 하단 → Delete this repository" |
| 클로드코드에서 gh login 안 됨 | gh login은 인터랙티브 — 터미널 직접 실행 필요 |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리 (Part 05 마지막 클립 — 완료 처리 포함)

### 1. 결과물 검증

다음 항목 확인:
- `~/fastcampus-cc/.git/` 디렉토리 존재 (git 초기화)
- `~/fastcampus-cc/.gitignore` 존재
- `git log --oneline` 결과 — 최소 2개 commit (init + update)
- GitHub repo URL 응답 (HTTP 200)
- `gh repo view {유저명}/fastcampus-cc --json visibility` → "PRIVATE"

빠진 게 있으면 어떤 게 빠졌는지 안내.

### 2. README.md 자동 작성

`~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습22-GitHub/README.md`:

```markdown
# 실습 22 — GitHub (git-teacher로 백업하기)

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 강의 워크스페이스: ~/fastcampus-cc/
- GitHub repo: https://github.com/{유저명}/fastcampus-cc (Private)

## Google Drive vs Git
| Google Drive | Git |
|---|---|
| 자동 동기 | 수동 동기 (commit + push) |
| 한 번 로그인 | repo마다 작업 |

핵심 차이: 자동 vs 수동.

## git-teacher 자연어 트리거
| 한국어 | 동작 |
|---|---|
| "깃 시작해줘" | git init + .gitignore + GitHub 연결 |
| "저장해줘" | git add + git commit |
| "올려줘" | git push |

## 백업한 자산 (~/fastcampus-cc/)
- CLAUDE.md (Clip 1) — 본인 컨텍스트 매뉴얼
- .claude/commands/ (Clip 2) — /study-progress 등
- .claude/agents/ (Clip 2) — practice-coach 등
- .mcp.json (Clip 3) — Playwright MCP
- .claude/settings.json (Clip 4) — Hook 3개
- sandbox/ (Clip 3) — 스크린샷·일정·메일

## 5단계 진행 (실습)
- 1 비유 + git-teacher 설치
- 2 "깃 시작해줘" — setup
- 3 "저장해줘" — 첫 commit
- 4 "올려줘" — GitHub push
- 5 수정 → 재저장 루프

## 평생 활용 응용 가이드
- 모든 작업 폴더에 같은 패턴 — git init → commit → push
- 다른 컴퓨터에서 `git clone {URL}` → 같은 환경 재현
- 팀 협업 — Collaborators 추가 / Pull Request
- 회사 코드/문서 GitHub 관리

## Part 05 전체 정리
| Clip | 자산 | 위치 |
|---|---|---|
| 1 | CLAUDE.md | ~/fastcampus-cc/CLAUDE.md |
| 2 | 커맨드 + 서브에이전트 | ~/fastcampus-cc/.claude/{commands,agents}/ |
| 3 | MCP & CLI | ~/fastcampus-cc/.mcp.json + gws CLI 인증 |
| 4 | Hook | ~/fastcampus-cc/.claude/settings.json |
| 5 | GitHub 백업 | https://github.com/{유저명}/fastcampus-cc |

## Part 06 빌드업
- 오늘 만든 5개 자산 → 본인 스킬로 발전
- /study-progress + practice-coach + Hook + MCP를 묶은 자동화

## 핵심 발견 / 회고
{사용자 자유 입력 — Part 05 전체 회고}
```

### 3. progress.json 업데이트 (Part 05 완료 처리)

`~/fastcampus-cc/progress.json`:

```json
{
  "practice_completed": [..., "실습 22"],
  "current_clip": null,
  "last_activity": "{ISO8601}",
  "github_repo": "https://github.com/{유저명}/fastcampus-cc",
  "completed_parts": [..., "Part 05"],
  "level": "AI Intermediate"
}
```

`completed_parts`에 "Part 05" 추가 — Part 05 5클립 모두 완주.

### 4. 회고 한 줄 (Part 05 전체)

자유 입력으로 받기:

> "Part 05 5클립 통해 만든 자산(CLAUDE.md / 커맨드+서브에이전트 / MCP+CLI / Hook / GitHub 백업) 중 본인에게 가장 인상 깊었던 한 줄을 적어주세요."

받은 텍스트를 README의 "핵심 발견 / 회고" 섹션에 기록.

### 5. Part 05 완료 안내 + Part 06 예고

```
🎉 Part 05 완료!

클로드코드의 5가지 핵심 구성요소를 직접 만져보고
본인 학습 워크스페이스(~/fastcampus-cc/)에 영구 자산으로 쌓았습니다.

✓ Clip 1 CLAUDE.md — 본인 컨텍스트 매뉴얼
✓ Clip 2 커맨드 & 서브에이전트 — /study-progress + practice-coach
✓ Clip 3 MCP & CLI — Playwright + gws CLI
✓ Clip 4 Hook — 자동화 방아쇠 3개
✓ Clip 5 GitHub — 영구 백업 + git-teacher

GitHub URL: https://github.com/{유저명}/fastcampus-cc

이 워크스페이스는 강의 끝나도 본인 클로드코드 공부 / 업무 환경으로 계속 발전하세요.
다른 컴퓨터에서도 `git clone`만 하면 같은 환경 그대로.

다음은 Part 06 — 클로드코드 스킬 만들기 ★
오늘 만든 자산들을 본인 스킬로 발전시킵니다.
"이해 단계" 끝, "제작 단계" 시작.

시작하려면 /part06 입력하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 번에 출력하고 사용자가 실습으로 진행
- **실습 진행 방식**: 강사 1줄 입력 → 학생 같은 줄 입력 → 결과 같이 확인. STOP 분리 패턴 금지
- **강의 워크스페이스 절대 백업 X**: 본인 백업은 `~/fastcampus-cc/`만
- **Private repo 강제**: settings.json에 개인 정보 가능성 — 자동으로 Private 옵션
- **gh login은 강사 시연 방식**: 인터랙티브라 필요 시 학생 본인 터미널 직접 실행
- **자유 진행 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **"~해줘" 패턴 금지 / "~하려는데 어떻게 해?" 패턴 강제**
- **git-teacher 자연어 트리거 강제 활용**: "깃 시작해줘" / "저장해줘" / "올려줘" — 명령어 외우지 말기
- **Part 06 사슬 명시**: 오늘 만든 자산들이 스킬로 발전될 것임 안내
- **Part 05 완료 처리 의무**: completed_parts에 "Part 05" 추가 + 전체 회고
- **API 키 노출 즉시 대응**: 학생이 실수로 올린 경우 즉시 revoke + 히스토리 정리 안내
