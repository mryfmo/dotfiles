# AGMSG-TASK dotfiles-T128-task-review-v1-v2-a01

Drafted 2026-10-11 by the orchestrator seat. The T128 design (accepted round 3) requires each wave's task file to be read by a fresh context before dispatch. Review three task files against the accepted design `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` (sha256 b2bfad90…): `.orchestration/tasks/dotfiles-T128-v1-task-schema-a01.md`, `.orchestration/tasks/dotfiles-T128-v1b-pr-caps-a01.md`, `.orchestration/tasks/dotfiles-T128-v2-audit-schema-and-runner-a01.md`. Read-only; one receipt file; Claude seat on the review profile in worker-d; every path in the main checkout.

## Questions, each with a verdict

1. Does each task implement exactly the invariant the design's `implementing_tasks` map assigns to it, with the invariant sentence copied verbatim, and nothing from another wave?
2. Are the `allowed_files` complete for what the task asks (grep the repository for every touch point: tests that pin the SKILL's headless-audit form, the manifest renderer, Makefile targets) and do they stay within INV-2's caps (15 files; estimate the added lines outside tests/, .orchestration/ and the data list)?
3. Does each premise hold (re-run at least two per file), and is any premise missing that the task relies on?
4. Routing: is each task's seat consistent with P10 (no Claude-boundary source on a Claude seat; no gate source outside operator routing)?
5. Ponytail: anything in the task that asks for a bespoke mechanism where a library, platform feature or existing script would do; anything under-specified that would produce a worker question (INV-4: a question is a specification defect, so name it now).
6. Contradictions between the task text and the design (for example the task.md copy, revise.yaml, the dry-run sequence, the `make audit-head` form, the audit identity).

## Output

`.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01.md` with front matter `reviewed_at`, `reviewer`, `profile`, `session`, and one `<task id>@<sha256>` line per file; per file `verdict: ready | revise: <items>`; then the answers with `file:line` references; under 250 lines. Then `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-v1-v2-a01 status=ready_for_review verdicts=<v1:…;v1b:…;v2:…> receipt=<path>` via `agmsg-dispatch dotfiles-conformance <you> claude-deep-dot w5:p1 "<line>"`. max_turns=8. Forbidden: editing any tracked file; branch; PR; `make update`.

## Round 2 (orchestrator, 2026-10-11)

All thirteen items adopted (V1-1..5, V1b-1..3, V2-1..5), plus the premise outputs re-run and pasted. Confirm as a diff check against the new file hashes in the AGMSG-TASK; same receipt shape at `.orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round2.md`; per file `verdict: ready | revise: <items>`. max_turns=5.

## Round 3 (orchestrator, 2026-10-11)

After design v4: review `dotfiles-T128-v1-task-schema-a01` (now validation only, five files), the new `dotfiles-T128-v1c-regime-ci-check-a01` (the CI check, after V1), and the receipt-pointer change in `dotfiles-T128-v1b-pr-caps-a01` and `dotfiles-T128-v2-audit-schema-and-runner-a01` (round 4). Same six questions for V1c in full; diff check for the other three. Receipt `…-task-review-v1-v2-a01-round3.md`; per file `verdict: ready | revise: <items>`. RESULT with `round=3`. max_turns=6.

## Round 4 (orchestrator, 2026-10-11)

Diff check of V1c (V1c-1, V1c-2, and the Bot-driven steps (b) and (c): exactly one task.md per PR, every changed path outside .orchestration/ within allowed_files) and V2 (Bot-driven: mask before hashing, reused-worktree validation, fallback isolation with --bare or disableAllHooks, the overlap sentence). V1 and V1b unchanged. Receipt `…-task-review-v1-v2-a01-round4.md`; RESULT with `round=4`. max_turns=4.
