---
format: 2
task_id: dotfiles-T126-w2b-herdr-audit-delegation-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round4.md
  design: .orchestration/tasks/dotfiles-T126-regime-v2-a01.md
allowed_files:
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - scripts/audit-watch.sh
  - tests/unit/test_audit_watch.py
  - README.md
invariants:
  INV-4: "the task-level audit is a headless, read-only, schema-validated run (codex exec --output-schema in a detached worktree; the fallback claude -p --json-schema runs with --bare and an API key, or, without one, under the managed hooks, which W2 shows harmless in a detached worktree) started automatically when CI is green on a pushed head and a Codex Bot review of that head exists, at most once per RESULT head; its JSON lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and a per-invariant map {holds|violated|not_applicable, path:line}; the orchestrator's task file, amendments, acceptance record and dispositions are in its input set; the runner records the JSON's sha256 in agmsg history under an audit identity (AGMSG-AUDIT v1 task_id= head= sha256=) before the gate reads it, and the gate requires that record for the audited head"
---

# AGMSG-TASK dotfiles-T126-w2b-herdr-audit-delegation-a01 — T126 W2b: `herdr-agents --audit` delegates to `audit-head.sh`; the audit watcher

Drafted 2026-10-10 by the orchestrator seat. Dispatched after W2 (PR #314) merges. Split out of W2 because the delegation rewrites the pane-run, marker, masking and verdict mechanics that about 33 tests in `tests/unit/test_herdr_agents.py` pin (four pin the pane command itself).

1. `herdr-agents --audit <sha> --task <id>`: the audit tab's command becomes `scripts/audit-head.sh <sha> --task <id> --out <path>`; the marker semantics follow `audit-head.sh`'s exit code (0 correct, 1 incorrect, 2 blocked, 3 runtime or schema failure, which the helper reports as `blocked`); the masker still runs on the rendered `.last.md`; the tab becomes optional (`--no-pane` runs `audit-head.sh` directly and tails nothing). Rewrite the pinned tests to the new contract one by one, keeping each test's intent (what it protected) in its docstring; delete none without saying why in the report.
2. `scripts/audit-watch.sh <pr>`: polls GitHub (interval 60 s) for a new head on the PR; when CI is green on it and a Codex Bot review of that head exists (any review object or review comment by `chatgpt-codex-connector[bot]` whose commit is that head), runs `audit-head.sh` for it unless an audit JSON for that head exists; stops when the PR closes; at most two audits run at once across watchers (a lock directory). Started by the orchestrator per PR; its own PID file so a second start is a no-op.
3. README: the audit section.
4. Tests with fakes for `gh`, `codex`, `claude`: the watcher starts one audit per head, waits for the Bot, respects the pool, stops on close; `herdr-agents --audit` delegation and marker mapping.

Forbidden: anything else; the gate scripts; `make update`; thread resolution. Standing Bot/CI rule and sandbox conduct apply; worker evidence under `.orchestration/<task id>/` on the branch (T126 INV-8).

## Repo / branch

A free seat after W2 merged: `git fetch origin`; `git switch -c feat/herdr-audit-delegation --no-track origin/main`.

## Completion

PR to `main` (English title `feat(audit): herdr-agents delegates to audit-head.sh; audit watcher per PR`), CI green, Bot wait, `invariant: INV-4 → …` lines, memory add, `AGMSG-RESULT v1 task_id=dotfiles-T126-w2b-herdr-audit-delegation-a01`. max_turns=12.
