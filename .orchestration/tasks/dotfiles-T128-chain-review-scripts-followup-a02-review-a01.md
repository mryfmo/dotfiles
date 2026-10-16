---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a02-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a02-review-a01 — confirm the task text `dotfiles-T128-chain-review-scripts-followup-a02` (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-15 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a02.md` (untracked; its sha256 is the `owner_task_sha256` of the TASK line), the second owner task of the chain-review-scripts lineage: `local-review.sh` refuses an `env -S` shebang remainder it cannot split as env does (a quote or a backslash), the audit of PR #364's 2e3ff49 and its local review. The task dispatches after PR #364 merges and boundary (16); its two premises read `0` today by design. One round, fixed stop condition; round 2 (2026-10-15 09:0xZ) after the review seat's round 1 (the refused set widened to the four -S features, the stdout line, the record aligned), the Codex half having confirmed round 1.

## Stop condition

1. Item 1 describes the one change correctly against `scripts/orchestrator/local-review.sh` at PR #364's head (the round-3 shebang branch, lines 91-98: the `-S` remainder split with `read -r -a`) and against the audit text (`…-audit-2e3ff49.md.last.md`, finding 1) and the local review (`…-local-review-2e3ff49.md`): the whole `-S` string holding a double quote, a single quote, a backslash, a dollar sign or a word starting with `#` is refused with exit 2 and a stdout line (the script's refusal convention) before the checkout, nothing written, the worktree untouched; plain words split as today; the alternative (a faithful `env -S` parser) is out of scope and said so; the failure mode is fail closed.
2. Item 2's test name appears verbatim in the closed row; its five cases (a double-quoted argument, a single-quoted one, a backslash escape, a `${X}` expansion, a `#` word) assert exit 2, the stdout line, the worktree at `main`, no file and the stub interpreter never run; the round-3 plain-word case stays.
3. The threat table has one row per `allowed_files` entry, the shebang-line row as the non-path control, the generic rows verbatim from `.orchestration/templates/task-short.md`, and the new-scripts row saying no new script; no sentence states an unlanded mechanism as present; the Completion clause is plan 020 step 4's with correction C-50's small-P2 revise rule qualified by INV-6's counts; the cap sentence reads outside `tests/` and outside `.orchestration/`; `allowed_files` is pairwise-disjoint from every in-flight task (the tools a02's `boundary.sh`, `fill_sweep.py` and `test_orchestrator_tools.py`; the chain-github a02's `resolve-threads.sh` and its test module; the seat-liveness owner task's launcher and its test module; the settings-hook dedupe task; the pane-open follow-up: none names `local-review.sh` or `tests/unit/test_chain_review_scripts.py`).
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-chain-review-scripts-followup-a02.md: OK`), the mask check (`masked 0 match(es)`), and its two premises replay from this checkout (`origin/main` fetched): `0`, `0` today (both become `1` after PR #364's merge and boundary (16), the dispatch condition).

## Output

`.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a02-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-chain-review-scripts-followup-a02: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-followup-a02-review-a01 round=1 verdict=confirm|revise owner_task_sha256=<sha> validation=<path>`.
