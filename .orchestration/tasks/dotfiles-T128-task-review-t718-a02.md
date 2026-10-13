---
format: 2
task_id: dotfiles-T128-task-review-t718-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-review-t718-a02 — task-file review of `dotfiles-T128-orchestrator-tools-a02` (review seat half; Codex headless runs the same check on the same hash)

Drafted 2026-10-13 01:40Z by the orchestrator seat under plan 012 option B: the second slice of T718, the nine scripts the first slice (`dotfiles-T128-orchestrator-tools-a01`, reviewed 01:25Z) left out. File: `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md`; its sha256 is in the TASK line. Design: `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` (v22, receipt round 22). Dispatch happens after a01 merges (`after:`), so the review may precede that merge.

## Stop condition (one round)

1. No contradiction with the design (`kind: code`; `scripts/orchestrator/` on no design-tier list; INV-2 caps in Validation; the gate and the audit runner untouched: `orch-gate.sh` and `orch-audit.sh` only assemble inputs and call `make require-crit-review` and the audit runner).
2. The premises hold when replayed (the `command:` lines, executor's binaries; C-18).
3. `allowed_files` covers every touch point of the nine scripts and their tests; nothing of the first slice's three scripts is re-specified here, and the counters' S1 line is touched only by item 3's ledger-shape guard (added in round 5 after PR #336 thread 4255079204).
4. Threat rows at the SKILL row unit (C7, C7b), the closed row's test name verbatim in item 2, and the environment-inputs row names every host binary and package the nine scripts use (git, gh, make, codex, shasum, uv; `fill_sweep.py` and `acceptance-front-matter.py` read and write the acceptance record's JSON block with the standard library, as amendment 1 of `dotfiles-T128-gate-evidence-a03` defines it; C-26).
5. C1 to C10 pass (the orchestrator pasted `OK`); `acceptance-front-matter.py` is specified against the amended a03 contract (JSON block, identity triple), not the superseded YAML wording.

## Output

`.orchestration/validation/dotfiles-T128-task-review-t718-a02.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), then exactly one line `Task-file verdict: dotfiles-T128-orchestrator-tools-a02: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-t718-a02 verdict=confirm|revise reviewed_sha256=<sha> validation=<path>`.

## Note for the seat (orchestrator, 2026-10-13 01:44Z)

The Codex half already ran on an earlier hash and asked for two changes, both applied before your first look: `acceptance-front-matter.py <task> <sweep-json>` derives `head` from `git rev-parse HEAD` and `pr` from the sweep JSON (never arguments), and `allowed_files` enumerates the nine scripts with one threat row each (no `scripts/orchestrator/*`). The TASK line carries the file's sha256.

## Round 2 (orchestrator, 2026-10-13 01:5xZ)

The seat's round-1 RESULT (bus 807, on `cb53e687…`; its receipt file is absent on disk, `receipt_sha256=` empty, later written, receipt_sha256=b542e996…; the three P3s applied too: ff-main.sh's rm scope and record citation, the checker phrase C1 to C10 and C7b, the named sources of the ledger rows and the audit summary) and the Codex half (rounds 2 and 3 on `cb53e687…` and `91811afe…`) are applied: `acceptance-front-matter.py <task> <sweep-json> <pr-worktree>` takes `head` from the PR worktree's HEAD and refuses a sweep JSON with another head; `orch-gate.sh` passes the a03 gate's inputs and never `AUDIT_DISPOSITIONS`, `orch-audit.sh` names no scratchpad checker; the environment row names the masker's PyYAML under uv beside design-keydiff.py's; item 2 adds the `acceptance-front-matter.py` tests. The TASK line carries the file's sha256.

## Round 3 (orchestrator, 2026-10-13 01:5xZ)

The seat's round 2 (receipt_sha256=4f34925d…): the sweep JSON carries `head_sha`, not `head` (pr-feedback.py's keys: repo, pr, head_sha, base_ref, base_sha, generated_at, checks, items); the three places now say `head_sha`. The coreutils list is open and names awk, cat, cp, date, mkdir, mktemp, mv, rm, sed, sort, tr, xargs. The TASK line carries the file's sha256.

## Round 4 (orchestrator, 2026-10-13 01:5xZ)

The seat confirmed `304f60e3…` (round 3). The Codex half's round-4 receipt (on the earlier `b47ec90b…`) carried two P2s on `codex-review.sh` that the later hashes still had: it accepted any profile and had no reviewed-file or hash step, contradicting its threat row. Item 1 now specifies `codex-review.sh <reviewed-file> <prompt-template> <receipt-out> <transcript-out>` with the profile fixed to `review` inside the script and the hash computed and rendered (exit 2 without the placeholder); item 2 adds the two tests. `amend-sweep.sh` also found row 47 still saying "C1 to C6"; it says C1 to C10 and C7b. Sweep after the edit: no leftover of `C1 to C6`, `<profile>`, `sweep JSON's head`. The TASK line carries the file's sha256.

## Round 5 (orchestrator, 2026-10-13 05:4xZ)

The pair agreed on `79e1307f…` (round 4). Before dispatch the file gains item 3 (regime-counters.sh trusts an acceptance record's ledger block only when every row is an object with a string `id` and a `[a-z0-9-]` `class`, else no record; its test `test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects`), the two allowed files `scripts/regime-counters.sh` and `tests/unit/test_regime_counters.py`, and two threat rows, after PR #336 thread 4255079204 (P2) on the first slice (a second revise there would be INV-6's reset). Same stop condition; the sweep (shellcheck's glob command is the only `scripts/orchestrator/*` left) and C1 to C10 pass. The TASK line carries the file's sha256.

## Round 6 (orchestrator, 2026-10-13 05:4xZ)

The Codex half's round-7 receipt (on `7cfc7bd4…`) asked for `jq` in the environment row, since item 3 makes regime-counters.sh parse the ledger block with it; added. Same stop condition; the TASK line carries the file's sha256.

Round 6, continued: the seat's round 5 (receipt 21fe3e5d…) added: `after:` names a03 (a01 is reset; a03 is the task on PR #336 that shares the counters files); the disposition text on #336 carries the evidence clause (`not-applicable: owned by dotfiles-T128-orchestrator-tools-a02 item 3; evidence=grep -n '4255079204' <this file>`); Validation runs `test_regime_counters.py` too; `record-ignored:<reason>` is one of the script's fixed slugs. All applied with the jq row.

Round 7 note (05:4xZ): the Codex half's round 8 (on the jq-only hash) found two more: this stop condition's item 3 still forbade touching the counters (reworded above), and the guard's test did not cover a numeric or missing `id` (item 3's test now lists four ignored shapes and one read block). The TASK line carries the file's sha256.

Round 7 note, continued (05:4xZ): the Codex half's round 9 (P1): `acceptance-front-matter.py` had no rule for `searches` nor a way to supply `audit_findings`, so its record could fail the a04 gate. Item 1 now says: `searches` recomputed by the gate's rule; `audit_findings` from `--audit-dispositions <tsv>` (required when the audit is `incorrect`, refused otherwise; `n` a digit string); `dispatch` and existing ledger rows preserved; the writer refuses to write a block that fails the gate's field checks. Item 2 tests each. The TASK line carries the file's sha256.

## Round 8 (orchestrator, 2026-10-13 05:4xZ)

The seat confirmed round 7 (`cac9a9f1…`) with one P3; the Codex half (rounds 10 and 11) asked for a reason slug for an absent or non-string `id`. Both applied: the fixed slugs are `block-not-json`, `ledger-row-not-object`, `id-not-string`, `class-not-slug`; `acceptance-front-matter.py` imports the gate module's record validator (no re-implementation) and the in-process effects row names that import. Same stop condition; the TASK line carries the file's sha256.
