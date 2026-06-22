#!/usr/bin/env bash
# SessionStart hook: progress.json을 읽어 진도 요약을 출력한다.
# 핵심: plain text 대신 JSON으로 출력한다.
#   - systemMessage           → 사용자 화면에 직접 표시 (이게 "안 뜨던" 문제의 해결책)
#   - hookSpecificOutput.additionalContext → Claude에게 배경 정보로 전달
# 끄려면 settings.json의 SessionStart 블록을 지우면 된다.
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
PROG="$ROOT/progress.json"
[ -f "$PROG" ] || exit 0

python3 - "$PROG" <<'PY'
import json, sys

try:
    prog = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    sys.exit(0)

done = set(prog.get("practice_completed", []))
clips = [
    ("실습 18", "Clip 1 (CLAUDE.md)"),
    ("실습 19", "Clip 2 (커맨드+에이전트)"),
    ("실습 20", "Clip 3 (MCP+CLI)"),
    ("실습 21", "Clip 4 (Hook)"),
    ("실습 22", "Clip 5 (GitHub)"),
]
p5_done = [name for key, name in clips if key in done]
nxt = next((name for key, name in clips if key not in done), None)
parts = prog.get("completed_parts", [])

lines = [
    "안녕하세요! 오늘도 화이팅",
    f"- 레벨: {prog.get('level', '-')}",
    f"- 완료한 Part: {', '.join(parts) if parts else '아직 없음'}",
    f"- 진행 중: {prog.get('current_part', '-')}",
    f"- Part 05 완료 클립: {', '.join(p5_done) if p5_done else '아직 없음'}",
]
if nxt:
    lines.append(f"- 다음 추천: {nxt} — /part05 입력")
else:
    lines.append("- 다음 추천: Part 05 완료! 🎉 /part06 입력")

text = "\n".join(lines)

# JSON 출력: systemMessage(사용자 화면) + additionalContext(모델 컨텍스트)
print(json.dumps({
    "continue": True,
    "systemMessage": text,
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": text,
    },
}, ensure_ascii=False))
PY
