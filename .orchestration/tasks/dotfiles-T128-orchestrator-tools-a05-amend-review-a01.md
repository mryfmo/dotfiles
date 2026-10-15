---
format: 2
task_id: dotfiles-T128-orchestrator-tools-a05-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-a05-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-orchestrator-tools-a05` (review seat half; Codex headless runs the same check)

Drafted 2026-10-14 (the TASK line's bus time is the dispatch time) by the orchestrator seat. The task-level audit of PR #350's head f48593d6 (`.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-audit-f48593d.md.last.md`) found the orch-gate.sh threat row stale against the implementation (the wrapper runs the trusted gate module, not the head's make; the audit calls that stronger and asks for the row and item 1 to be amended) and a P1: uv's interpreter discovery lets a PR-supplied `.python-version` name an executable that runs before the trusted gate; the operator's decision A (acceptance record, 01:17Z) releases one fix round under this amendment. Amended file: `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md`, sha256 `aa6f6b359a9bba9fa79450f0ed915d6d5b72b1a94a90773c0790a1deb87ca740`; the pre-amendment copy is on `main` (`eaac8e4b`).

## What changed (amendment 1)

1. The threat row whose control begins "the PR adds scripts/orchestrator/orch-gate.sh": control and disposition replaced. The wrapper runs this checkout's gate module (`scripts/require-crit-review.py`, equal to origin/main's, with the validator it loads) under an interpreter resolved in this checkout before the review worktree is entered, with the review worktree as its working tree and exactly the gate's inputs; never the head's make, Makefile, `.python-version`, `uv.toml` or any interpreter the head can choose. Disposition `closed: tests/unit/test_orchestrator_tools.py::test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree` (the audit of f48593d6: P1 at orch-gate.sh:67, P2 at the task's row).
2. Item 1's `orch-audit.sh … and orch-gate.sh` bullet gains one sentence saying the same (amendment 1).
3. A `## Change of 2026-10-14` section at the end: the row (1), the bullet (2), the fix round of PR #350 released by the operator's decision A (interpreter pinned before any command uses the review worktree as cwd; a cleanup trap before the head checkout; the two tests `test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree` and `test_orch_gate_restores_the_review_worktree_when_setup_fails`), and a note that premise 2's dispatch-time output (`75:…`) now reads line 77 after PR #328 with the sentence unchanged.
Nothing else: `git diff --stat origin/main -- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md` prints `1 file changed, 10 insertions(+), 3 deletions(-)`.

## Stop condition

1. The diff of the task file against its copy on `main` contains only what the list above says.
2. For each behaviour the amendment adds or changes in a script or a procedure, name the threat row that covers it; a new effect on a gate input (an acceptance record, a sweep JSON, an audit receipt), on the bus or on the host has its own row with a closing test, added by this amendment (C-28, M-20261012-29). An amendment that adds behaviour without its row is `revise`.
3. Each closed row's named test closes its risk and the test names appear verbatim in the task's test item; the wording agrees with the rule sentences and the sibling tasks it cites.
4. The file passes C1 to C10 and C7b (the orchestrator pasted OK) and `amend-sweep.sh` for the superseded terms (pasted); `reset_of`, the copy rows and the evidence directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-orchestrator-tools-a05-amend-review-a01.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-orchestrator-tools-a05: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-a05-amend-review-a01 verdict=confirm|revise amended_task_sha256=aa6f6b359a9bba9fa79450f0ed915d6d5b72b1a94a90773c0790a1deb87ca740 validation=<path>`.

## Round 2 (orchestrator, after the round-1 RESULTs)

Round 1: the Codex half confirmed on aa6f6b35 (receipt `-codex.md`, 01:20:26Z); the seat's round 1 (validation sha f3018bfc, 01:24:15Z) asked four changes, all applied: (1) P1: a second closed row on `scripts/orchestrator/orch-gate.sh` for the cleanup trap (restores the review worktree to origin/main when a later step fails), closed by `test_orch_gate_restores_the_review_worktree_when_setup_fails`; (2) P2: item 2 names the amendment's two tests; (3) P2: the item-1 clause that still described the make form carries "(superseded by amendment 1 …)" before it; (4) P3: this brief's id reads `-amend-review-a01` throughout. `git diff --stat origin/main` on the task file: `1 file changed, 13 insertions(+), 4 deletions(-)`; input checker `OK`; the superseded-phrase sweep clean. Same four stop conditions on the new hash (the round-2 TASK line's `amended_task_sha256`).

## Round 3 (orchestrator, after the round-2 RESULTs)

Round 2: the seat confirmed on 5d6e4332 (01:28:13Z); the Codex half (receipt `-codex-r2.md`, 01:28:40Z) found one P2: the trap row claimed interruption as well as failure while its test exercises a failing `cp` only. Applied: the row's control now covers a failing later step only and says a signal is outside the row and its test; nothing else changed (`git diff --stat origin/main` on the task file unchanged in shape). Same four stop conditions on the new hash (the round-3 TASK line's `amended_task_sha256`).
