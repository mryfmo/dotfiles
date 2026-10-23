---
format: 2
task_id: dotfiles-T129-hcom-dispatch-bus-a02-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a02-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a02-review-a01 — independent review of the hcom-dispatch bus a02 text (plan 023 PR C stage 1)

Drafted 2026-10-22T05:35Z by the orchestrator seat. The a02 text resets a01 (2026-10-18) under design 5.14; its C-80 history: 17775c1 incorrect (3), d61a0f2 correct (author round 2), 5f9caa3 and 7c44fca and 2db29fc and 4a0347c incorrect on the generated Checks and the hcom execution path, 4de6705 correct. This is the one-round task-file review of the agmsg-orchestration SKILL.

## What to review

1. `.orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md` at sha256 `4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c` (164 lines) is the file you judge; compute the hash yourself and stop with `verdict=reject` if it differs.
2. No contradiction with plan 023 PR C stage 1 and design 5.14 items 1, 2, 9 and 10 as cited: the private namespace for every executable (constraint 1), the store identity (2), consumed bytes bound at execution (3), gh only through the gh-binding a02 contract (4), the marker history format with reader-side framing (5), `status=revise` as the key (6), and amendment 2's execution of hcom from the anchored checkout's private tool directory installed from the verified wheel with UV_TOOL_DIR and UV_TOOL_BIN_DIR.
3. Every `## Checks` line is a command with its output and exit status (generated at canonical main d06d94fd; the design digest in two stages; the write boundaries as members, rendered and deployed; the hcom realpath, entry digest, receipt and wheel digest); the premises match the front matter; `after:` names dotfiles-T133-gh-binding-a02.
4. `allowed_files` covers every touch point: grep for each changed script's basename over tests/unit and over scripts/lint-comparisons-baseline.tsv, and the updater target of amendment 2; a touch point outside the entries is a reject.
5. The threat table's shape rules by hand: `closed:` selectors as `tests/<file>::<name>`, `residual:` sentences of at least 20 characters naming an owner (dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 or dotfiles-T133-gh-binding-a02), one row per allowed_files entry, per non-path control and per orchestrator effect.
6. No `invariants` key, so no invariant entry.
7. Read only; no file changed, nothing dispatched, no network write.

## Output

`.orchestration/dotfiles-T129-hcom-dispatch-bus-a02-review-a01/review.md` with the hash, one line per item and the verdict, then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T129-hcom-dispatch-bus-a02-review-a01 status=ready_for_review round=1 verdict=accept|reject design_file=.orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md design_sha256=<the hash you computed> findings=<n> report=.orchestration/dotfiles-T129-hcom-dispatch-bus-a02-review-a01/review.md`, sent with `agmsg-dispatch dotfiles-conformance claude-standard-dot-a011 claude-deep-dot wW:p1 '<that line>'`.
