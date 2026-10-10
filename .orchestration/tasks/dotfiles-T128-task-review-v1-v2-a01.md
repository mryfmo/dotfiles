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

## Round 5 (orchestrator, 2026-10-11)

R4-1 was already applied (all four pointers name round 5); R4-2: item 3 gains `--manifest <path>` for tests and item 6 uses it. One-line diff check of V1c; receipt `…-task-review-v1-v2-a01-round5.md`; RESULT with `round=5`. max_turns=3.

## Round 6 (orchestrator, 2026-10-11)

After design v6: diff check of V1 (legacy binding to .orchestration/tasks/, --no-grandfather, literal first segment, wildcard tier rule, tests), V1b (sentence comparison), V1c (--no-grandfather on branch copies), V2 (instruction root and schema from main, --add-dir worktree), all four pointing at the round-6 receipt with v6 sentences verbatim. Receipt `…-task-review-v1-v2-a01-round6.md`; RESULT with `round=6`. max_turns=4.

## Round 7 (orchestrator, 2026-10-11)

Supersedes round 6 if still open: the four files now point at the round-7 receipt with v7 sentences; V2 additionally refuses the claude fallback when the head changes .claude/skills/** (round-6 INV-5 note) with its premise and test. Diff check against the round-6 items plus that change. Receipt `…-task-review-v1-v2-a01-round7.md`; RESULT with `round=7`. max_turns=4.

## Round 8 (orchestrator, 2026-10-11)

After design v8: V1 and V1c carry INV-1 v8 verbatim, V2 INV-5 v8 verbatim plus the `inputs` manifest in the schema, V1b unchanged but pointer; all four point at round 8. Diff check. Receipt `…-task-review-v1-v2-a01-round8.md`; RESULT with `round=8`. max_turns=4.

## Round 9 (orchestrator, 2026-10-11)

Supersedes round 8 if still open. After design v9: V1 adds the `after` key; V1b adds the tests_added cap; V2 refuses any `.claude/**` change for the fallback and adds the `premises` map to the schema; V1c pointer only. Diff check; receipt `…-task-review-v1-v2-a01-round9.md`; RESULT with `round=9`. max_turns=4.

## Round 10 (orchestrator, 2026-10-11)

Supersedes round 9 if still open. After design v10: V1 and V1c carry INV-1 v10, V1b INV-2 v10 (contract-task mapping), V2 INV-5 v10 plus the runner-computed manifest; V1c names the Actions event policy action. Diff check; receipt `…-task-review-v1-v2-a01-round10.md`; RESULT with `round=10`. max_turns=4.

## Round 10 addendum (orchestrator, 2026-10-11)

A fifth file joins the review: `.orchestration/tasks/dotfiles-T128-v0-main-tests-a01.md` (wave V0, INV-12, the first implementing wave). Full six-question review for V0; include it in the round-10 receipt.

## Round 11 (orchestrator, 2026-10-11)

Supersedes round 10 if still open. Five files: V0 (two-mode main-tests, contract decorator, INV-12 v11), V1 and V1c (INV-1 v11), V1b and V2 (pointer only). Full review for V0, diff check for the rest; receipt `…-task-review-v1-v2-a01-round11.md`; RESULT with `round=11`. max_turns=5.

## Round 12 (orchestrator, 2026-10-11)

Supersedes round 11 if still open. V0 carries INV-12 v12 and the two new sentences (steps 1(b), 1b, 3(b2), 4); the other four files move pointer only. Diff check; receipt `…-task-review-v1-v2-a01-round12.md`; RESULT with `round=12`. max_turns=4.

## Round 13 (orchestrator, 2026-10-11)

V0 rewritten with R11-1 (main tests overlaid on a git-archive copy of the PR tree), R11-2 (declared modules from the task's tests/unit entries; undeclared mode runs every other main module), R11-3 (task.md read with PyYAML), step 1(c) promotion check and test (b3); the ROOT premise added (34/34). Other four files: pointer and INV sentence only. Full check of V0, diff for the rest; receipt `…-task-review-v1-v2-a01-round13.md`; RESULT with `round=13`. max_turns=5.

## Round 14 (orchestrator, 2026-10-11)

Codex Bot findings on boundary head 8be11e65 folded into V0 (ast-based decorator detection with alias cases, test b4) and V2 (inputs snapshotted and hashed before the model runs and re-checked after; premises keys must equal 1..N; join/send/leave serialized by a lock for pooled runs; tests). Design unchanged (15daca85). Diff check of V0 and V2; receipt `…-task-review-v1-v2-a01-round14.md`; RESULT with `round=14`. max_turns=4.

## Round 15 (orchestrator, 2026-10-11)

R14-1 (tier from the stamped `tier:` key, missing stamp treated as design; `scripts/lib/contract_markers.py` helper allowed) and the V2 notes (string keys; no line figure). Diff check of V0 and V2; receipt `…-task-review-v1-v2-a01-round15.md`; RESULT with `round=15`. max_turns=3.
