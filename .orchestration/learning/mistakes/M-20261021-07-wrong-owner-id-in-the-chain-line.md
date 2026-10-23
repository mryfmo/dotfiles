# M-20261021-07 — the #440 chain line named a non-existent owner task

- When: 2026-10-21 07:28Z–07:40Z (operator-run chain for PR #440, head c439b63c).
- What: the line handed to the operator named the owner `dotfiles-T133-task-generator-plan-check-a06-checker-followup-a01`; the lineage's owner file is `dotfiles-T133-task-generator-plan-check-followup-a01`. chain-integrate.sh checks the owner file only after the local review, so the run spent 12 minutes of codex review before `exit 15`.
- Root cause: the owner id was composed from the task id by analogy (the pre-send lineage's owner is `…-pre-send-check-followup-a01`) instead of being read from `.orchestration/tasks/`; no step validated the line before it was handed over (the operator's `!` run is now the codex route, so every typo costs an operator action).
- Mechanism: `.agents/worklog/orchestrator-glue/chain-line.sh <task> <pr> <owner> [extra]` refuses when the task text, the owner file or the extra TSV is missing or the PR is not open with required checks green, and prints the exact line otherwise (probed: refused on the wrong owner, printed on the right one). Every chain line handed to the operator comes from it.
- Cost: one operator action and 12 minutes; the local review of c439b63c is cached and reused by the re-run.
