#!/usr/bin/env python3
"""PreToolUse(Bash) hook: 'rm' 삭제를 가로채 휴지통으로 옮긴다.
- /mnt/* (Windows 드라이브) 파일 → Windows 진짜 휴지통 (PowerShell)
- WSL 네이티브 경로 → ~/.claude-trash/<타임스탬프>/ 로 이동
- 위험 경로(/, ~, /mnt 등)나 복잡한 명령은 안전하게 차단
원래 rm은 항상 막는다(이미 휴지통으로 옮겼으므로).
"""
import sys, json, os, shlex, glob, subprocess, datetime, shutil

META = ['|', ';', '&', '`', '$(', '>', '<', '\n']
DANGEROUS = {'/', '/mnt', '/mnt/c', '/mnt/d', '/home', '/usr', '/etc', '/root',
             os.path.expanduser('~')}


def allow():
    sys.exit(0)            # 통과 (아무것도 안 함)


def deny(msg):
    sys.stderr.write(msg)  # PreToolUse는 exit 2 + stderr로 도구를 막고 메시지를 Claude에 전달
    sys.exit(2)


def to_recycle_bin(winpath):
    """Windows 휴지통으로 보내기 (파일/폴더 자동 구분)."""
    esc = winpath.replace("'", "''")
    ps = (
        "Add-Type -AssemblyName Microsoft.VisualBasic; $p='" + esc + "'; "
        "if (Test-Path -PathType Container $p) {"
        "[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($p,'OnlyErrorDialogs','SendToRecycleBin')"
        "} else {"
        "[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($p,'OnlyErrorDialogs','SendToRecycleBin')}"
    )
    subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        allow()

    if data.get("tool_name") != "Bash":
        allow()

    cmd = (data.get("tool_input") or {}).get("command", "")
    cwd = data.get("cwd") or os.getcwd()
    has_meta = any(m in cmd for m in META)

    try:
        tokens = shlex.split(cmd.strip())
    except Exception:
        tokens = []

    # rm이 첫 토큰이 아니면: 복합 명령 속에 rm이 숨어있고 메타문자까지 있으면 차단, 아니면 통과
    if not tokens or tokens[0] != 'rm':
        if ' rm ' in (' ' + cmd + ' ') and has_meta:
            deny("⚠️ 삭제(rm)가 섞인 복합 명령이라 자동 휴지통 처리가 불안전해요. "
                 "안전을 위해 차단했어요. 단순 'rm <파일>' 형태로 하거나 직접 확인하세요.")
        allow()

    # 여기부터 tokens[0] == 'rm'
    if has_meta:
        deny("⚠️ 삭제 명령에 파이프/리다이렉트 등이 섞여 자동 휴지통 처리가 불안전해요. 차단했어요.")

    paths = [t for t in tokens[1:] if not t.startswith('-')]
    if not paths:
        allow()

    # glob 확장 + 절대경로화
    resolved = []
    for p in paths:
        p2 = os.path.expanduser(p)
        if not os.path.isabs(p2):
            p2 = os.path.join(cwd, p2)
        matches = glob.glob(p2)
        resolved.extend(matches if matches else [p2])

    trashed, skipped = [], []
    danger_norm = {d.rstrip('/') for d in DANGEROUS}
    for rp in resolved:
        ap = os.path.abspath(rp)
        if ap == '/' or ap.rstrip('/') in danger_norm:
            deny(f"⚠️ '{ap}'는 위험 경로라 삭제/휴지통 처리를 거부했어요.")
        if not os.path.exists(ap):
            skipped.append(ap)
            continue
        if ap.startswith('/mnt/'):
            win = subprocess.run(["wslpath", "-w", ap], capture_output=True, text=True).stdout.strip()
            try:
                to_recycle_bin(win)
                trashed.append(ap + "  (Windows 휴지통)")
            except subprocess.CalledProcessError as e:
                err = e.stderr.decode(errors='ignore') if e.stderr else ''
                deny(f"⚠️ 휴지통 이동 실패: {ap}\n{err}\n안전을 위해 삭제를 차단했어요.")
        else:
            trashdir = os.path.expanduser('~/.claude-trash/' +
                                          datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
            os.makedirs(trashdir, exist_ok=True)
            shutil.move(ap, trashdir)
            trashed.append(ap + "  → " + trashdir)

    if not trashed:
        allow()  # 옮길 게 없었음(파일 부재 등) → 원래 명령 그대로 진행

    msg = "🗑️ 직접 삭제 대신 휴지통으로 옮겼어요:\n"
    msg += "".join(f"  - {t}\n" for t in trashed)
    if skipped:
        msg += "존재하지 않아 건너뜀:\n" + "".join(f"  - {s}\n" for s in skipped)
    msg += "원래 rm은 실행하지 않았어요 (이미 휴지통 처리됨)."
    deny(msg)


if __name__ == "__main__":
    main()
