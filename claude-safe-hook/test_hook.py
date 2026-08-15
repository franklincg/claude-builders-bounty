import importlib.util
from pathlib import Path

path = Path(__file__).with_name("block_destructive.py")
spec = importlib.util.spec_from_file_location("hook", path)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

blocked = [
    "rm -rf /tmp/x",
    "rm -fr ./build",
    "DROP TABLE users;",
    "git push origin main --force",
    "git push -f origin main",
    "TRUNCATE TABLE sessions;",
    "DELETE FROM users;",
    "delete from users ;",
]
allowed = [
    "rm -r ./build",
    "git push origin main",
    "SELECT * FROM users",
    "DELETE FROM users WHERE id = 1;",
    "echo safe",
]

for command in blocked:
    assert hook.dangerous(command), command
for command in allowed:
    assert not hook.dangerous(command), command

print("CLAUDE3_HOOK_TEST_PASS")
