---
task_id: fix-chezmoi-pycache-modify-exec
worker: codex-gpt55-high
promote: false
---

# Learning Triage

## Reusable Learning

- Chezmoi treats `modify_` source-state prefixes as modifies even when the file is ignored by git; ignored bytecode under `home/` can still be walked by chezmoi unless it is covered by `chezmoiignore`.
- `--exclude=scripts` excludes run scripts, not modify entries.
- In this repo, `uv run pytest tests/unit/` is not currently runnable without installing pytest; `uv run python -m unittest discover tests/unit` exercises the existing unit tests without dependency changes.

## Promotion Decision

Do not promote a new rule from this worker. The task requested a triage artifact only.
