---
task_id: fix-chezmoi-pycache-modify-exec
orchestrator: orchestrator-fable5
worker: codex-gpt55-high
status: accepted
---

# Acceptance

## Decision

Accepted. AGMSG-ACCEPTANCE v1 status=accepted sent 2026-07-08.

## Independent verification by orchestrator

- `chezmoi status` → exit 0, no `.pyc` exec format error, no pycache entries (only pre-existing `R` script markers and `MM .claude/settings.json` runtime drift).
- Recurrence guard re-tested independently: dummy `home/dot_codex/__pycache__/modify_private_config.cpython-311.pyc` created → `chezmoi status` exit 0 with no pycache entry → dummy removed. `**/__pycache__` / `**/*.pyc` in `chezmoiignore.d/common` are effective.
- `uv run python -m unittest discover tests/unit` → 51 tests OK; `find home -name '__pycache__'` → empty afterwards (dont_write_bytecode effective).
- Source `home/dot_codex/__pycache__/` and target `~/.codex/__pycache__/` both gone.
- `AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> make require-crit-review` → exit 0.

## Notes

- Orchestrator's own `make update` re-run stopped at an unrelated interactive prompt: `MM .claude/settings.json` ("has changed since chezmoi last wrote it") cannot be answered without a TTY. This drift was caused by the live Claude Code session rewriting settings.json after the worker's successful TTY apply (validation log shows worker's `make update` exit 0). Normal chezmoi drift UX, out of scope for this task.
- Diff left uncommitted per task constraints; commit/PR is the user's decision.
