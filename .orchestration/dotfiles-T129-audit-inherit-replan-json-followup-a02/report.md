---
task_id: dotfiles-T129-audit-inherit-replan-json-followup-a02
seat: claude-standard-dot-a008
branch: tools/audit-inherit-followup-a02
base: 3e41e36a
pr: pending
test_commits: 495f51b3 f75c1137 02b6eec1
fix_commits: 9b59a3bc cdfd3ee5
code_head: 02b6eec1
task_sha256: 5f33a507b1ad6d6da09ed06f2a828dc1ae3fcdff39a4a6d000372ba04a684150
---

# Report: dotfiles-T129-audit-inherit-replan-json-followup-a02 (the F1 lineage's owner task)

- **Seat:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. The AGMSG-TASK arrived at 2026-10-18T22:33:03Z with `task_sha256=5f33a507…`. The dispatched file and the branch copy `task.md` match byte for byte (validation §1).
- **Branch:** a fresh `tools/audit-inherit-followup-a02`, made with `git switch -c … --no-track origin/main` at `3e41e36a`. PR #418's branch is untouched.
  - origin/main has since moved to `740772ef` (#416). That commit touches none of this task's files (`scripts/update-agent-assets.sh`, `executable_remove-agent-asset`, their tests and #416's records).
- **The owned rows** come from `.orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a01.md` (validation §2):
  - `audit:274a536:1` (= `local:274a536:1`, schema-drift);
  - `audit:274a536:2` (= `local:274a536:2`, fail-open-on-error);
  - `audit:274a536:5` (duplicate-count).
- **Sources read for the finding text:** the audit `…-audit-274a536.md.last.md` and the local review `…-local-review-274a536.md`.
- **Records-form lessons this owner carries:**
  - Cap ranges are written as merge-base...code head (§8), per `audit:274a536:3`.
  - The receipt's `reviewer:` field holds one allowlisted word, per `audit:274a536:4`.

## The owned rows

| Row | Script | Change | Test (red: validation §4 and §4b; green: §5) |
|---|---|---|---|
| audit:274a536:1 | `scripts/regime-counters.sh` | S1's `re-plan=present` follows the gate's `record_field_errors()` and `acceptance-front-matter.py`. The whole `replans` object must be `{<class slug>: exactly specification, design, implementation, verification, each a string with text after str.strip()}`. One malformed entry under any class therefore makes the class's re-plan missing, just as it makes the gate reject the block. Absent `replans` counts as empty; any other non-object, `false` included, is malformed. The slug test is `^[a-z0-9-]+\z`, because jq's `$` also matches before a final newline. The text test is a jq class of the 29 characters Python's `str.strip()` removes; jq's `\s` misses U+001C to U+001F. | `tests/unit/test_regime_counters.py::RegimeCountersTest::test_s1_applies_the_gate_s_exact_replan_schema`, with these cases: an extra key; a malformed entry under another class; a class that is no slug; a class key with a trailing newline; replans false; each of the 29 characters as a part that only `str.strip()` empties; and the 29 plus a letter or any of four format characters `str.isspace()` rejects (U+200B, U+180E, U+2060, U+FEFF) as present |
| audit:274a536:2 | `scripts/orchestrator/chain-integrate.sh` | Inheritance also needs a parent verdict the gate accepts. The script checks the last non-blank line of the parent's `.md.last.md` against `AUDIT_VERDICT` and requires `correct`, or `incorrect` with a `[P0-P3]` line (`AUDIT_FINDING`). A blocked, empty or finding-less parent result takes the fresh-audit path, so the "head already audited" trap of the finding cannot arise. | `tests/unit/test_chain_glue.py::ChainIntegrateTest::test_inheritance_requires_a_parent_verdict_the_gate_accepts`, with these cases: blocked; empty; incorrect without a finding; and a verdict followed by another line. Each subtest counts its own audit. |
| audit:274a536:5 | `scripts/orchestrator/ledger-check.py` | The needed ids are deduplicated in order (`dict.fromkeys`). An original audit and its inherited copy then count each finding once and print one GAP line. | `tests/unit/test_task_checkers.py::TaskCheckersTest::test_ledger_check_counts_an_audit_and_its_inherited_copy_once` |

Nothing outside the owned rows changed. The shdoc headers of both shell scripts name the new conditions.

## Worker review

The worker review is recorded in `dotfiles-T129-audit-inherit-replan-json-followup-a02-worker-crit.json` and its receipt.

- **Round 1** covered `origin/main..9b59a3bc` and returned `Verdict: incorrect`: one P2 and three P3, all inside row 1 or this change. The round fixed them all, with the tests in `f75c1137` (red at `9b59a3bc`, §4b) and the fixes in `cdfd3ee5`.
- The reviewer also named two pre-existing gaps that this change does not widen, both left to the advisory-P2 owner `…-followup-a03` if the audit reports them:
  - the ledger-class `$` at `regime-counters.sh:142`;
  - duplicate JSON keys inside `replans`, which jq cannot see.
- **Round 2** covered `9b59a3bc..cdfd3ee5`, with the same reviewer and its context kept, and returned `Verdict: correct`.
  - Findings 1 to 4 are closed, and 12 of 13 mutants are caught.
  - The surviving mutant adds U+200B to the text class, the P3. It is caught since `02b6eec1`: the present control now also appends four format characters (validation §5a). That commit is test-only and is the code head.

## Red before this task, not this task's

`tests/unit/test_require_crit_review.py` fails 136 subtests in this seat's sandbox, on this branch and on a scratch worktree at origin/main alike (validation §6 and §6a).

- **The failure is the seat's git environment.** The module's fixture `git commit` fails because commit signing is on and the sandbox denies reading the signing key. `init.defaultBranch` is also unset. The message `--base 'main' does not resolve to a commit`, which an earlier draft of this report named as the cause, is only the downstream symptom.
- **With the environment fixed it passes.** Run at the code head with `commit.gpgsign=false` and `init.defaultBranch=main` as git config environment variables, the module passes 98 of 98 (§6b).
- This PR changes neither the gate nor its test, and the PR's CI `test` jobs run the module.

## Caps (validation §8, merge-base 3e41e36a...code head 02b6eec1)

- **Outside `tests/` and `.orchestration/`:** 26 of 200.
  - `regime-counters.sh`: 11 added, 5 deleted.
  - `chain-integrate.sh`: 7 added, 2 deleted.
  - `ledger-check.py`: 1 added.
- **`tests/`:** 69 of 1000.
  - `test_chain_glue.py`: 31.
  - `test_regime_counters.py`: 26.
  - `test_task_checkers.py`: 12.

cost: n/a
