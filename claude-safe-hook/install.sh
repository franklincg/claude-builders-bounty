#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$HOME/.claude/hooks"
cp "$(dirname "$0")/block_destructive.py" "$HOME/.claude/hooks/block_destructive.py"
chmod +x "$HOME/.claude/hooks/block_destructive.py"
python3 - <<'PY'
import json
from pathlib import Path

path = Path.home() / ".claude" / "settings.json"
data = json.loads(path.read_text()) if path.exists() and path.read_text().strip() else {}
hooks = data.setdefault("hooks", {})
pre = hooks.setdefault("PreToolUse", [])
entry = {
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/block_destructive.py"}],
}
if entry not in pre:
    pre.append(entry)
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(data, indent=2) + "\n")
print(f"configured {path}")
PY
