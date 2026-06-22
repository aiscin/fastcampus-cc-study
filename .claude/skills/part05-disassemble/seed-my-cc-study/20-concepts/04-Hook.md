# Hook

> 한 줄 요약: 클로드코드가 특정 순간에 "이거 먼저 확인해줘"라고 하는 신호등

## 1. 한 줄로 말하면

Hook은 클로드코드의 작업 흐름 중에 특정 순간에 자동으로 실행되는 스크립트입니다.
마치 신호등처럼 "지금 이 작업을 해도 되나? 먼저 확인해봐!"라고 일을 멈추고 검사하는 거죠.

## 2. 왜 필요한가

- **위험한 명령 막기** — 예: "혹시 `rm -rf` 같은 위험한 코드 짤 거 아니야?" (자동 차단)
- **작업 전 자동 검증** — 예: 코드 저장하기 전에 테스트가 통과했나?
- **자동 흐름 만들기** — 예: 파일 저장하면 자동으로 포맷팅 도구 실행

## 3. Hook이 실행되는 순간들

| Hook 이름 | 언제 실행되나 | 역할 |
|---|---|---|
| PreToolUse | 도구 실행 **전** | 위험한 명령을 먼저 걸러냄 |
| PostToolUse | 도구 실행 **후** | 결과가 맞는지 확인 |
| SessionStart | 작업 시작할 때 | 환경 설정 (예: 환경변수 로드) |
| SessionEnd | 작업 끝날 때 | 정리 작업 (예: 임시 파일 삭제) |

## 4. 가장 단순한 예시

### 위험한 명령 막기
```bash
# ~/.claude/hooks/block-dangerous.sh
COMMAND=$(jq -r '.tool_input.command')

# rm -rf를 포함하면 차단
if echo "$COMMAND" | grep -q 'rm -rf'; then
  echo "DANGER: 이 명령어는 실행할 수 없습니다!"
  exit 1
fi
```

### settings.json에 연결하기
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous.sh"
          }
        ]
      }
    ]
  }
}
```

## 5. 강의에서 다루는 실습

- Part 5 실습 21에서 Hook을 직접 만들어 자동화 흐름을 구성해봅니다

## 6. 더 알아보기

- 공식 문서: https://docs.claude.com/en/docs/claude-code/hooks
- 관련 개념: [01-CLAUDE-md.md](01-CLAUDE-md.md) (프로젝트 설정)
- 관련 개념: [05-스킬과-플러그인.md](05-스킬과-플러그인.md) (기능 확장)

## 💡 꿀팁

Hook을 설정하기 위해 꼭 복잡한 스크립트를 쓸 필요는 없습니다.
시작은 단순하게:
1. 자주 실수하는 명령어는? → PreToolUse Hook으로 경고 띄우기
2. 코드 저장 후 매번 하는 일? → PostToolUse Hook으로 자동화

이렇게 점점 추가하다 보면, 실수 없는 자동화된 워크플로우가 완성됩니다!
