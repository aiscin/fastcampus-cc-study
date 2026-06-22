# Clip 03 — MCP & CLI (외부 도구 연결하기)

> Part 05 / Ch 01 / Clip 03 (실습 20) | 예상 시간: ~30분
> 결과물: Playwright MCP 설정(.mcp.json) + gws CLI 인증 + 스크린샷/추출 데이터/일정/메일 조회 결과
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
WORK_DIR="$ROOT/50-my-work/Part05-뜯어보기/실습20-MCP-CLI"
mkdir -p "$WORK_DIR"

# 강의 워크스페이스 sandbox 폴더 보장 (스크린샷·추출 결과 저장 위치)
mkdir -p "$STUDY_DIR/sandbox"

# Playwright MCP 사전 다운로드 안내 (선택)
echo "✓ $WORK_DIR 준비 완료"
echo "✓ ~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/ 준비 완료"
echo ""
echo "ℹ Playwright MCP 첫 실행 시 패키지 다운로드(~수십 MB)가 발생합니다."
echo "  강사 사전 설치를 권장합니다: npx @playwright/mcp@latest --help"
```

셋업 결과 한 줄 보고 후 아래 **MCP & CLI 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## MCP & CLI 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 한 번 읽고 시작.

### 한 줄 정의

| 자산 | 비유 | 한 줄 | 연결 위치 |
|---|---|---|---|
| **MCP** (Model Context Protocol) | AI에 꽂는 소켓 | 외부 서비스를 표준 규격으로 AI가 다루게 함 | `.mcp.json` |
| **CLI** (Command Line Interface) | AI가 직접 호출하는 도구 | 시스템에 설치된 명령줄 도구를 AI가 자연어로 부름 | 시스템 PATH |

### 동작 흐름

```
[MCP]
  사용자 자연어 → Claude → MCP 서버 → 외부 서비스 → 결과 → Claude → 사용자

[CLI]
  사용자 자연어 → Claude → bash 명령 작성 → CLI 도구 → 외부 서비스 → 결과 → Claude → 사용자
```

### 오늘 꽂을 두 도구

| 도구 | 종류 | 역할 |
|---|---|---|
| **Playwright** | MCP | 브라우저 자동화 (페이지 열기, 스크린샷, 데이터 추출) |
| **gws CLI** | CLI | Google Workspace 9개 서비스 (Gmail/Calendar/Drive/Sheets/Docs/Slides/Tasks/Chat/Meet) |

### 핵심 메시지

> **외부 도구 1개 꽂으면 능력이 한 단계 확장된다.** MCP·CLI 모두 본인 워크스페이스 영구 자산으로 쌓인다.

---

## 진행 안내

```
✓ 50-my-work/Part05-뜯어보기/실습20-MCP-CLI/ 준비 완료
✓ ~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/ 준비 완료

오늘 할 거 (~30분)
- MCP & CLI = 외부 도구 연결 두 방식
- MCP 시연: Playwright (브라우저 자동화)
- CLI 시연: gws CLI (Google Workspace)
- 실습 (강사 입력 → 같은 입력 → 결과 같이 확인)

5단계 흐름:
1. MCP 개념 + Playwright MCP 설치 (.mcp.json 생성)
2. Playwright로 웹페이지 스크린샷 + 데이터 추출
3. CLI 개념 + gws CLI 설치 (강사 인증 시연)
4. gws CLI로 일정/메일 조회
5. MCP vs CLI 비교 정리

★ 인증이 필요한 부분(gws OAuth)은 강사 시연만 봐도 OK
  본인 인증은 자가 진행 가능
★ 강의 워크스페이스 (~/fastcampus-cc/) 절대 수정 X
  모든 변경은 ~/fastcampus-cc/ 안에서만
```

---

## 단계별 진행 가이드

### STEP 1. MCP 개념 + Playwright MCP 설치 (5분)

**[목적]** MCP가 무엇인지 + 첫 MCP를 학생 워크스페이스에 연결.

**[Claude Code 입력]**

```text
~/fastcampus-cc/에 Playwright MCP를 연결하려는데 어떻게 해?
.mcp.json 파일 만들어서 연결해줘.
```

**[검증]** 안티그래비티에서 `~/fastcampus-cc/.mcp.json` 열어 다음 내용 확인:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**[활성화]** 클로드코드 재시작 (`exit` → `claude`) 후 시작 로그에서 `[MCP] ✓ playwright (active)` 확인.

---

### STEP 2. Playwright로 웹페이지 스크린샷 + 데이터 추출 (7분)

**[목적]** MCP의 시각적 결과물 체험 + 자동화 활용 감각.

**[Claude Code 입력 — 스크린샷]**

```text
Playwright로 https://news.hada.io 열어서 첫 페이지 스크린샷 찍고,
~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/hada-screenshot.png에 저장해줘.
```

**[Claude Code 입력 — 데이터 추출]**

```text
방금 그 페이지에서 상단 5개 게시물 제목만 뽑아서
~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/hada-titles.md에 리스트로 정리해줘.
```

**[검증]** 안티그래비티 파일 트리에서 `sandbox/` 폴더 열어 두 결과물 확인.

**[응용 가이드]** 본인 업무 응용 예시 — 경쟁사 가격 비교 / 공지사항 모니터링 / 리서치 페이지 캡처.

---

### STEP 3. CLI 개념 + gws CLI 설치 (강사 시연) (5분)

**[목적]** CLI 방식 이해 + Google Workspace 9개 서비스 연결.

**[강사 시연 — 설치]**

```bash
npm install -g @googleworkspace/cli
gws --version
```

**[강사 시연 — 인증]**

`gws auth setup`은 인터랙티브 TUI라 클로드코드 안에서 못 돌림 — 터미널에서 직접 실행.

5단계 인증 흐름:
1. gcloud CLI 확인
2. Google 계정 선택
3. GCP 프로젝트 생성 (예: `nopal-ws-XXXXXX`)
4. 9개 API 활성화 (Gmail/Calendar/Drive/Sheets/Docs/Slides/Tasks/Chat/Meet)
5. OAuth 클라이언트 ID 생성 + 테스트 사용자 추가 (필수!)

마지막에:

```bash
gws auth login
```

브라우저로 OAuth 페이지 → Google 로그인 → 권한 승인.

**[강사 시연 — 인증 확인]**

```bash
gws auth status
```

**[학생 안내]** 학생 본인 인증은 영상 후 자가 진행. 강사 시연만 봐도 STEP 4 이해 가능.

---

### STEP 4. gws CLI로 일정/메일 조회 (5분)

**[목적]** 인증된 gws CLI를 클로드코드가 자연어로 호출하는 흐름 체험.

**[Claude Code 입력 — 일정]**

```text
gws CLI로 오늘 내 캘린더 일정 확인해주려는데 어떻게 해?
조회 결과를 ~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/today-schedule.md에 정리해줘.
```

**[Claude Code 입력 — 메일]**

```text
gws CLI로 안 읽은 메일 중 최근 5개 제목만 정리해주려는데 어떻게 해?
~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/recent-mails.md에 저장.
```

**[검증]** 안티그래비티에서 두 마크다운 파일 확인. 본인 일정/메일 정리되었는지.

**[Part 06 빌드업 멘트]** "이걸 슬래시 커맨드 `/morning-briefing`으로 만들면 매일 똑같이. Part 06에서 그렇게 발전."

---

### STEP 5. MCP vs CLI 비교 정리 (2분)

**[Claude Code 입력]**

```text
오늘 꽂은 Playwright MCP와 gws CLI를 비교 표로 정리해줘.

관점:
- 비유 (소켓 vs 명령줄 도구)
- 연결 방식
- 호출 방식
- 장점
- 어떤 도구에 어울릴까

저장: ~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/mcp-vs-cli.md
```

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| `npx @playwright/mcp` 첫 실행 오래 걸림 | 정상 — 첫 실행만 2-3분, 이후 빠름 |
| `.mcp.json` 만들었는데 활성화 안 됨 | 클로드코드 재시작 (exit → claude). 시작 로그에 `[MCP] ✓ playwright` 확인 |
| Playwright 브라우저 다운로드 실패 | "npx playwright install chromium 직접 실행하려는데 어떻게 해?" |
| `gws auth setup` 클로드코드 안에서 안 됨 | 인터랙티브 TUI라 터미널 직접 실행 필수 |
| OAuth 403 액세스 차단 | 테스트 사용자 추가 누락 — OAuth 동의 화면 → "Test users" → 본인 Gmail 추가 |
| `invalid_scope` 에러 | API 너무 많이 활성화 — 9개만 정확히 (Drive/Sheets/Gmail/Calendar/Docs/Slides/Tasks/Chat/Meet) |
| gws 명령 못 찾음 | npm 글로벌 PATH — `which gws` 확인 후 `npm root -g` 경로 PATH 추가 |
| 본인 인증 안 한 상태 gws 호출 시도 | 정상 — 강사 시연만 본 경우. 자가 인증 후 재실행 |
| 스크린샷이 빈 페이지 | 사이트 로딩 지연 — "스크린샷 찍기 전 3초 대기" 추가 |
| 회사 네트워크 방화벽 | 개인 핫스팟 또는 사내 허용 도구 |
| 강의 워크스페이스에 .mcp.json 만들고 싶음 | "그건 REFERENCE라 수정 X. ~/fastcampus-cc/ 안에서만" |
| MCP 삭제 방법 | ".mcp.json에서 해당 블록 제거 후 재시작" |
| 시연 사이트(news.hada.io) 일시 장애 | 다른 공개 페이지로 대체 (예: github.com, anthropic.com) |

`막혔어요` / `도와줘`로 도움 요청 가능.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리

### 1. 결과물 검증

다음 파일들 존재 확인:
- `~/fastcampus-cc/.mcp.json` (Playwright MCP 등록)
- `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/hada-screenshot.png` (Playwright 스크린샷)
- `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/hada-titles.md` (Playwright 추출)
- `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/today-schedule.md` (gws 일정 — 인증된 학생만)
- `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/recent-mails.md` (gws 메일 — 인증된 학생만)
- `~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/mcp-vs-cli.md` (비교 정리)

빠진 게 있으면 어떤 게 빠졌는지 안내 (gws 결과물 없으면 "강사 시연만 보신 분들은 OK").

### 2. README.md 자동 작성

`~/fastcampus-cc/50-my-work/Part05-뜯어보기/실습20-MCP-CLI/README.md`:

```markdown
# 실습 20 — MCP & CLI (외부 도구 연결하기)

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 강의 워크스페이스: ~/fastcampus-cc/

## 외부 도구 연결 두 방식

| 자산 | 비유 | 한 줄 | 연결 위치 |
|---|---|---|---|
| MCP | AI에 꽂는 소켓 | 표준 규격으로 외부 서비스 다룸 | .mcp.json |
| CLI | AI가 직접 호출하는 도구 | 시스템 명령을 자연어로 부름 | 시스템 PATH |

## 오늘 꽂은 도구

### Playwright MCP
- 위치: ~/fastcampus-cc/.mcp.json
- 역할: 브라우저 자동화 (페이지 열기/스크린샷/데이터 추출)
- 시연 결과:
  - hada-screenshot.png — Hada News 첫 페이지
  - hada-titles.md — 상단 5개 게시물 제목 추출

### gws CLI
- 설치: `npm install -g @googleworkspace/cli`
- 역할: Google Workspace 9개 서비스 (Gmail/Calendar/Drive/Sheets/Docs/Slides/Tasks/Chat/Meet)
- 인증: 5단계 OAuth (강사 시연 / 학생 자가 진행)
- 시연 결과 (인증된 학생):
  - today-schedule.md — 오늘 캘린더 일정
  - recent-mails.md — 안 읽은 메일 5개

## MCP vs CLI 비교

(mcp-vs-cli.md 5관점 비교 표)

## 5단계 진행 (실습)
- 1 MCP 개념 + Playwright MCP 설치 (.mcp.json 생성)
- 2 Playwright로 스크린샷 + 데이터 추출
- 3 CLI 개념 + gws CLI 설치 (강사 인증 시연)
- 4 gws CLI로 일정/메일 조회
- 5 MCP vs CLI 비교 정리

## 평생 활용 응용 가이드
- MCP 패턴 → Notion/Slack/Linear 등 본인 회사 도구 연결
- CLI 패턴 → 본인 시스템 명령 자동화 (예: docker / git / aws)
- 외부 도구 + 슬래시 커맨드 = `/morning-briefing` 같은 본인 매크로

## Part 06 빌드업
- 오늘 꽂은 두 도구를 스킬에 묶어 자동화
- 예: `/morning-briefing` 스킬 = gws CLI + Playwright + 정리

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

`~/fastcampus-cc/progress.json`:

```json
{
  "practice_completed": [..., "실습 20"],
  "current_clip": null,
  "last_activity": "{ISO8601}",
  "mcp_installed": [..., "playwright"],
  "cli_installed": [..., "gws"]
}
```

### 4. 회고 한 줄

자유 입력으로 받기:

> "오늘 꽂은 두 도구(Playwright/gws CLI) 중 본인 업무에 어떤 게 더 쓸모있을 것 같은지 한 줄로 적어주세요."

받은 텍스트를 README의 "핵심 발견 / 회고" 섹션에 기록.

### 5. 다음 클립 안내

```
실습 20 완료. 외부 도구 연결의 두 가지 방식(MCP 소켓 + CLI 도구)을 직접 꽂아봤습니다.

✓ Playwright MCP — 브라우저 자동화
✓ gws CLI — Google Workspace 9개 서비스 (강사 시연)

이 두 도구는 ~/fastcampus-cc/에 영구 자산으로 쌓였고,
강의 끝나도 본인 업무에 응용 가능합니다.

다음은 Clip 04 — Hook으로 자동화 방아쇠 만들기.
시작하려면 /part05 다시 호출하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 번에 출력하고 사용자가 실습으로 진행
- **실습 진행 방식**: 강사 1줄 입력 → 학생 같은 줄 입력 → 결과 같이 확인. STOP 분리 패턴 금지
- **강의 워크스페이스 절대 수정 X**: 모든 변경은 `~/fastcampus-cc/`에서만
- **gws 인증은 강사 시연만 — 학생 자가 진행 OK**: 인증 안 한 학생도 STEP 4 흐름 이해 가능
- **자유 진행 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
- **"~해줘" 패턴 금지 / "~하려는데 어떻게 해?" 패턴 강제**
- **Part 06 사슬 명시**: 오늘 꽂은 두 도구가 스킬로 묶여 자동화될 것임을 안내
- **시연용 URL은 안전한 공개 페이지**: 강사 본인 블로그 / news.hada.io / github.com 등
