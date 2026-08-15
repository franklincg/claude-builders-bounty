# Claude Code destructive-command guard

A `PreToolUse` hook for Bash commands. It blocks a small set of destructive patterns before execution and records each blocked attempt in `~/.claude/hooks/blocked.log`.

## Blocks

- `rm -rf` / `rm -fr`
- `DROP TABLE`
- `git push --force`, `--force-with-lease`, or `-f`
- `TRUNCATE`
- `DELETE FROM` without a `WHERE` clause

Normal Bash commands are allowed through unchanged.

## Install

From this directory:

```bash
bash install.sh
```

Restart Claude Code after installation so the hook configuration is reloaded.

## Test

```bash
python3 test_hook.py
```

The hook reads Claude Code hook JSON from stdin. A blocked Bash command is logged with UTC timestamp, attempted command, project path, and reason, then exits with status `2` and prints a clear explanation to stderr. Allowed commands exit `0`.

No secrets or command output are logged; only the attempted command metadata required for the guard is recorded.
