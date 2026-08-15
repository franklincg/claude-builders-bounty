#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG = Path.home() / ".claude" / "hooks" / "blocked.log"

PATTERNS = [
    ("rm -rf", re.compile(r"(?i)(?:^|[;&|]\s*)rm\s+(?:-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*|-[A-Za-z]*f[A-Za-z]*r[A-Za-z]*)\b")),
    ("DROP TABLE", re.compile(r"(?i)\bDROP\s+TABLE\b")),
    ("git push --force", re.compile(r"(?i)\bgit\s+push\b[^\n;&|]*(?:--force(?:-with-lease)?|-f)\b")),
    ("TRUNCATE", re.compile(r"(?i)\bTRUNCATE(?:\s+TABLE)?\b")),
]
DELETE_RE = re.compile(r"(?is)\bDELETE\s+FROM\b(?P<body>.*?)(?:;|$)")


def dangerous(command: str):
    for label, rx in PATTERNS:
        if rx.search(command):
            return label
    for match in DELETE_RE.finditer(command):
        if not re.search(r"(?i)\bWHERE\b", match.group("body")):
            return "DELETE FROM without WHERE"
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        print(f"hook input error: {exc}", file=sys.stderr)
        return 0

    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}
    command = str(tool_input.get("command") or "")

    if tool_name and tool_name.lower() != "bash":
        return 0

    reason = dangerous(command)
    if not reason:
        return 0

    project = str(payload.get("cwd") or payload.get("project_dir") or "")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": command,
            "project_path": project,
            "reason": reason,
        }, ensure_ascii=False) + "\n")

    print(
        f"BLOCKED destructive command ({reason}). Use a safer, scoped alternative or request explicit human approval.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
