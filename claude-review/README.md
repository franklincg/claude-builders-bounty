# Claude Review CLI

Dependency-free Python CLI for bounty #4.

## Requirements

- Python 3.9+
- GitHub CLI (`gh`) installed and authenticated

## Usage

```bash
python claude_review.py --pr https://github.com/owner/repo/pull/123
```

The command prints structured Markdown with:

- Summary of changes
- Identified risks
- Improvement suggestions
- Confidence score (Low / Medium / High)

## Validation

The implementation was syntax-checked with `python -m py_compile claude_review.py` and executed against two real GitHub PRs. Their captured outputs are included in `samples/`.

No GitHub token is stored or printed by this tool; authentication is delegated to the local `gh` CLI.
