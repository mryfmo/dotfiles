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
