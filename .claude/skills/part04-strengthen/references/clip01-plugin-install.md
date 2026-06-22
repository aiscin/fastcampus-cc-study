# Clip 01 — 플러그인 설치하기

> Part 04 / Ch 01 / Clip 01 (실습 14) | 예상 시간: ~15분
> 결과물: 마켓플레이스 추가 + 플러그인 3개(docs-guide / kkirikkiri / vibe-sunsang) 설치
> 패턴: **BUILD 없음 — 따라하기 시연** (설치 클립이라 5단계 적용 X)

---

## 자동 셋업

스킬 호출 직후 아래 Bash를 즉시 실행 (사용자에게 명령 보여주는 게 아니라 스킬이 직접).

```bash
if [ -d "$HOME/fastcampus-cc" ]; then
  ROOT="$HOME/fastcampus-cc"
else
  ROOT="$(pwd)"
fi

WORK_DIR="$ROOT/50-my-work/Part04-강화하기/실습14-플러그인설치"
mkdir -p "$WORK_DIR"

echo "✓ $WORK_DIR 준비 완료"
```

셋업 결과 한 줄 보고 후 아래 **플러그인 개념 브리핑 + 진행 안내**를 한 메시지로 출력 + SLEEP.

---

## 플러그인 개념 브리핑 (스킬이 시작 시 먼저 띄워줌)

> 학습자가 영상 보기 전에 한 번 읽고 시작.

### 한 줄 정의

| 항목 | 내용 |
|---|---|
| 공식 정의 | "Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams." |
| 한국어 풀이 | 클로드코드 확장 요소들을 한 묶음으로 패키징해서, GitHub 등으로 다른 사람과 주고받을 수 있게 만든 배포 단위 |
| 본질 | 앱스토어에서 앱 받아 쓰듯, 클로드코드에 기능을 추가 |

### 플러그인의 구성요소

| 구성요소 | 위치 | 한 줄 설명 |
|---|---|---|
| 슬래시 명령 (Commands) | `commands/*.md` | `/명령어`로 직접 호출 |
| 스킬 (Skills) | `skills/*/SKILL.md` | 자동화 작업 흐름 |
| 서브에이전트 (Agents) | `agents/*.md` | 특정 작업용 AI 페르소나 |
| Hook | `hooks/*.json` | 이벤트 자동화 |
| MCP 서버 | `.mcp.json` | 외부 서비스 연결 |
| LSP 서버 | `lsp/*` | 코드 자동완성·정의 점프 |

> 실제로는 슬래시 명령 + 스킬이 가장 많이 쓰임. 일부는 서브에이전트까지.

### 공유 메커니즘

```
[제작자]                              [사용자]
명령·스킬·에이전트   →   [GitHub]   →   /plugin TUI
한 묶음 push                          → 마켓플레이스 추가
                                      → 플러그인 검색·설치
```

한 번 마켓플레이스 추가하면 그 안의 플러그인 여러 개 골라 설치 가능.

### 마켓플레이스

| 항목 | 내용 |
|---|---|
| 정의 | 플러그인 카탈로그 |
| 출처 | GitHub 저장소 / Git URL / 로컬 / 원격 URL |
| 사용 흐름 | (1) 마켓플레이스 추가 → (2) 개별 플러그인 설치 |

### 보안

| 항목 | 내용 |
|---|---|
| 공식 경고 | "Plugins are highly trusted components that can execute arbitrary code on your machine with your user privileges." |
| 권장 | 신뢰할 수 있는 출처에서만 설치 (검증된 마켓플레이스) |

### 공식 문서 출처

- 플러그인 생성: https://code.claude.com/docs/en/plugins.md
- 플러그인 설치/마켓플레이스: https://code.claude.com/docs/en/discover-plugins.md
- 플러그인 기술 레퍼런스: https://code.claude.com/docs/en/plugins-reference.md

---

## 진행 안내

```
✓ 50-my-work/Part04-강화하기/실습14-플러그인설치/ 준비 완료

오늘 할 거 (~15분)
- 플러그인: 클로드코드 확장 요소 묶음. 앱스토어처럼 설치해서 쓰는 친구들
- /plugin TUI로 GPTaku 마켓플레이스 추가 + 플러그인 3개 설치
- 영상 보면서 진행하시고 끝나면 `완료` 또는 `/wrap` 입력

TUI 4단계 흐름:
1. /plugin 입력 → TUI 열림
2. Marketplaces 탭 → GPTaku URL 등록
3. Discover 탭 → docs-guide / kkirikkiri / vibe-sunsang 순차 설치
4. Installed 탭 확인 + 슬래시 명령 호출 테스트
```

---

## 절차 — TUI 따라하기

| 단계 | 입력 | 화면 |
|---|---|---|
| 1 | `/plugin` 입력 | TUI 열림 (Discover / Installed / Marketplaces / Errors 탭) |
| 2 | Marketplaces 탭 → Add marketplace | URL 입력란 표시 |
| 3 | `https://github.com/fivetaku/gptaku_plugins.git` 입력 | 마켓플레이스 등록 완료 |
| 4 | Discover 탭 → docs-guide 선택 → Install | 설치 진행 + 권한 요청 시 Y |
| 5 | 같은 방식으로 kkirikkiri 설치 | — |
| 6 | 같은 방식으로 vibe-sunsang 설치 | — |
| 7 | Installed 탭에서 3개 설치 확인 | docs-guide / kkirikkiri / vibe-sunsang ✓ |
| 8 | TUI 닫고 `/docs-guide`, `/kkirikkiri`, `/vibe-sunsang` 한 번씩 호출 | 각 플러그인 응답 확인 |

---

## 막히면

| 증상 | 도움 요청 멘트 |
|---|---|
| `/plugin` 입력해도 TUI 안 열림 | "클로드코드 버전 업데이트하는 법 알려줘" |
| GitHub URL 등록 실패 | "마켓플레이스 추가가 안 되는데 어떻게 해야 해?" |
| 설치 중 권한 요청 반복 | Y로 진행 (신뢰할 수 있는 마켓플레이스만) |
| Installed 탭에 안 보임 | "/reload-plugins 또는 클로드코드 재시작해야 할까?" |
| 슬래시 명령 호출 시 응답 없음 | "/plugin 목록에서 상태 확인하고 재설치 알려줘" |
| 잘못 설치한 플러그인 제거 | "/plugin uninstall로 제거하는 법 알려줘" |

`막혔어요` / `도와줘`로 도움 요청 가능. 그 외는 자유 진행.

---

## 완료 트리거

`완료` / `/wrap` / `끝` / `다음 클립` 입력 → WRAP 자동 진행.

---

## WRAP 자동 처리

트리거 받으면 스킬이 다음을 순서대로 실행:

### 1. 결과물 검증

`/plugin` Installed 탭 또는 명령 출력으로 확인:
- docs-guide 설치 ✓
- kkirikkiri 설치 ✓
- vibe-sunsang 설치 ✓

3개 다 없으면 어떤 게 빠졌는지 안내 후 재설치 권유.

### 2. README.md 자동 작성

`50-my-work/Part04-강화하기/실습14-플러그인설치/README.md`:

```markdown
# 실습 14 — 플러그인 설치하기

- 완료 시각: {ISO8601}
- 모델·모드 정보
- 마켓플레이스: gptaku_plugins (github.com/fivetaku/gptaku_plugins)

## 플러그인 개념 정리 (공식 문서 기반)

### 한 줄 정의
| 항목 | 내용 |
|---|---|
| 공식 정의 | "Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams." |
| 한국어 풀이 | 클로드코드 확장 요소들을 한 묶음으로 패키징해서, GitHub 등으로 다른 사람과 주고받을 수 있게 만든 배포 단위 |
| 본질 | 내가 만든 명령·스킬·에이전트를 한 줄 설치로 누구나 쓰게 만드는 것 |

### 플러그인 구성요소
| 구성요소 | 위치 | 한 줄 설명 |
|---|---|---|
| 슬래시 명령 | commands/*.md | /명령어로 직접 호출 |
| 스킬 | skills/*/SKILL.md | 자동화 작업 흐름 |
| 서브에이전트 | agents/*.md | 특정 작업용 AI 페르소나 |
| Hook | hooks/*.json | 이벤트 자동화 |
| MCP 서버 | .mcp.json | 외부 서비스 연결 |
| LSP 서버 | lsp/* | 코드 자동완성·정의 점프 |

### 마켓플레이스 = 플러그인 카탈로그
- 한 번 추가하면 그 안의 플러그인 여러 개 골라 설치 가능
- 사용 흐름: (1) 마켓플레이스 추가 → (2) 개별 플러그인 설치

### 보안
- 공식 경고: "Plugins are highly trusted components that can execute arbitrary code on your machine with your user privileges."
- 신뢰할 수 있는 출처에서만 설치

## 설치한 플러그인
- docs-guide — 공식 문서 기반 답변 (다음 클립)
- kkirikkiri — AI 에이전트 팀 자동 구성 (클립 03)
- vibe-sunsang — 사용 패턴 점검 (클립 04)

## 진행 절차 (BUILD 없음, TUI 따라하기)
1. /plugin TUI 열기
2. Marketplaces 탭 → GPTaku URL 등록
3. Discover 탭 → 3개 순차 설치
4. Installed 탭 확인 + 슬래시 명령 호출

## 공식 문서 출처
- https://code.claude.com/docs/en/plugins.md
- https://code.claude.com/docs/en/discover-plugins.md
- https://code.claude.com/docs/en/plugins-reference.md

## 핵심 발견 / 회고
{사용자 자유 입력}
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 14"],
  "installed_plugins": ["docs-guide", "kkirikkiri", "vibe-sunsang"],
  "current_clip": null,
  "last_activity": "{ISO8601}"
}
```

### 4. 회고 한 줄

자유 입력으로 받기:

> "이번 클립에서 가장 인상적이었던 거 한 줄로 적어주세요."

### 5. 다음 클립 안내

```
실습 14 완료. 마켓플레이스 추가 + 플러그인 3개 설치됐습니다.

다음은 Clip 02 — docs-guide로 공식 문서 기반 정확한 답변 받기.
시작하려면 /part04 다시 호출하세요.
```

---

## 진행 원칙

- **자동 셋업 후 SLEEP**: 진행 안내를 한 번에 출력하고 사용자가 영상 보면서 직접 진행
- **BUILD 없음**: 설치 따라하기 클립이라 5단계 적용 X
- **TUI 우선**: 명령어 직접 입력보다 `/plugin` TUI 흐름 권장 (입문자 진입 장벽 낮춤)
- **자유 실습 중 개입 X**: 명시적 도움 요청에만 응답
- **WRAP은 트리거 후 진행**: `완료` 안 하면 자동 정리 X
- **AskUserQuestion 사용 X**: 회고도 자유 입력
