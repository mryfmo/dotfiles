# Report: dotfiles-T128-orchestrator-tools-a05

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on PR #346's branch `tools/orchestrator-scripts-2`, continuing from `7b574d32`. That head and every commit before it stay (validation §1).
- Task file sha256 `eaac8e4b…` matches the TASK's `task_sha256`. It is copied byte-identical to `.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md`. The a02 task copy and evidence records are not edited.
- The delta is items 7 to 9 with their tests (`608b38a2`), this task copy, and this evidence. a02's items 1 to 6 stand as implemented at `7b574d32`. PR-B (`acceptance-front-matter.py`, `orch-gate.sh`) waits for PR-A's merge.

## Items 7 to 9 (`608b38a2`)

| Item | Finding (the audit of `7b574d32`) | Fix | Closing test |
|---|---|---|---|
| 7 | P1 `fill_sweep.py:49`: a thread reply by any account that is not the Codex Bot supplied a disposition, the latest reply winning | A reply supplies a disposition only when its author is `--orchestrator-login <login>`. A reply by any other login is printed as `ignored-reply <comment id> <login>` and supplies nothing. The option is required, given once, and must match `^[A-Za-z0-9-]{1,39}$`; otherwise the script exits 2 before reading or writing a file. The login appears nowhere in the script | `test_fill_sweep_ignores_a_disposition_reply_from_another_login` (F1 to F5) |
| 8 | P1 `fill_sweep.py:60`: the rule table auto-dispositioned `review`, `codex_review` and `issue_comment` items whatever their body carried | No rule applies to a body that carries `![P<n> Badge](` with `<n>` in 0 to 3. The item stays a gap unless `extra.tsv` has its row. The neutral-level rule stays for badge-free annotations and statuses. A bare `P0`, as in the review summary's hidden `"blockingSeverityThreshold":"P0"`, is not a badge | `test_fill_sweep_leaves_a_badged_review_body_a_gap` (F6, F7) |
| 9 | P1 `orch-audit.sh:62` to 72: the lineage copy brought this head's earlier receipt into the review checkout, and the receipt was removed in the main checkout only | Before the run:<br>- this head's receipt and `.last.md` are removed in both checkouts;<br>- the lineage copy skips them;<br>- a timestamp file is written with `mktemp`.<br>After the run, the script exits 3 unless `.last.md` exists, is non-empty, and is newer than that file (`find -newer`). | `test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt` (A1, A2; it fails against `7b574d32`, validation §4) |

Two changes go beyond the items' literal text, both on purpose:

- **Item 7's own-reply rule.** At `7b574d32` an item took this rule when it was a review comment by any non-bot account whose body starts with `Disposition (orchestrator`. That is the same trust gap as the reply path, so the rule now requires `author` (the sweep's login field) to equal `--orchestrator-login`. A look-alike comment by another login is a gap. The item 7 test covers it (F3).
- **Item 8's badge gate.** The gate sits on the one line that picks a rule, so it applies to every rule source, the own-reply rule included, not only the five sources item 8 names. An orchestrator reply that quoted a badge would become a gap that `extra.tsv` fills. That is the safe direction.

Item 9's test runs three times with stubbed codex modes:

- `codex-silent` exits 0 and writes nothing. The earlier receipt is in the main checkout and tracked on `origin/main`, so the review checkout has it too.
- `codex-stale` writes a receipt dated 2000.
- The normal mode writes a fresh receipt.

The first two must exit 3 with no verdict line and leave the review checkout clean. The third must print the verdict. That third run also shows `find -newer` resolves a write a few milliseconds after the timestamp, on macOS here; CI covers Linux.

Mutation proofs (validation §3):

- 11 mutants: 9 killed by assertions, 2 survived.
- A3 (the review-checkout `rm`) and A4 (the lineage skip) survive alone because the other guards cover them.
- A2 (the review `rm` and the freshness check both removed) is killed.
- Validation §3 explains each survivor.

## The size cap

The drafted fixes first came to 506 added lines outside `tests/`, 6 over the cap of 500. The task does not allow moving a script out of PR-A: a02's items 1 to 6 stand as implemented, and no new branch or PR is made for PR-A. So the two files under edit were tightened, with no behavior change:

- `orch-audit.sh`'s `@description` is rewrapped at one width, with the new facts added.
- Its lineage loop uses `[[ … ]] || continue` in place of `if … fi`.
- `fill_sweep.py`'s disposition count is one named line plus its `print`, in place of a four-line call.

The result is 497 added lines outside `tests/` and 493 under it, in 12 files outside `.orchestration/` (validation §2). No other file was touched for the cap.

## Results

- `test_orchestrator_tools.py`: 30 tests OK. `test_regime_counters.py`: 27 tests OK.
- shellcheck 0.11.0, shfmt 3.14.1 (`-i 4 -sr`), ruff format and ruff check: clean.
- The two existing `fill_sweep.py` tests now pass `--orchestrator-login`, since the option is required. They share a `sweep`/`fill_sweep` helper. The codex stub gained the `codex-silent` and `codex-stale` modes, and its default behaviour is unchanged.

## Bot threads on PR #346 (main-checkout copy only)

Read after the push (validation §6). The Bot posted no review and no comment on `1089ed24` in the 20 minutes after the push. Its three threads, all opened on `1287af34`, are the whole list:

| Thread | Finding | Proposed disposition |
|---|---|---|
| 4260535901 (P1) | `dispatch.sh:80`: a tab-separated TASK bypassed the required-field guard | `fixed:3544d195` (a02's revise round) |
| 4260535916 (P2) | `boundary.sh:44`: deleted paths | `not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a01 (row deleted-path-handling); evidence=git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md \| grep -n 4260535916` |
| 4260535924 (P2) | `ff-main.sh:38`: deleted local paths | `not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a01 (row deleted-path-handling); evidence=git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md \| grep -n 4260535924` |

The evidence command prints the thread's row under `## Owned by dotfiles-T128-orchestrator-tools-followup-a01` (lines 23 and 24 of that record at `origin/main`). The worker resolves no thread.

## Not done, or outside scope

- PR-B: after PR-A merges.
- The full `tests/unit` discover is left to CI (validation §4).
- Understand-Anything hook: did not fire. plan-mode-used: no.

cost: n/a

## CI and CompactionDB (main-checkout copy only)

- CI on `1089ed24`: all 13 checks pass (validation §5).
- `memory add` in the main checkout printed `6774fddf-7a98-4761-9754-715f81e25701`.

## Revise round on `8576645c` (`5582fa3c`)

- The audit's P1 (`dispatch.sh:80` against `regime-counters.sh:115`): dispatch.sh accepts a tab or a whitespace run between tokens (`[[:blank:]]+` in its header check, `read -ra` for the tokens). The counters split each history body on one space, so such AGMSG-TASK, RESULT and PONG lines escaped the INV-6 counts.
- The fix, `scripts/regime-counters.sh:115`, has two steps:
  1. It undoes the escapes that `read_history`'s `jq @tsv` adds: `\t`, `\n`, `\r` and `\\`, in one left-to-right pass, so an escaped backslash before a `t` stays a backslash and a `t`. Without this step a tab read from the store arrives as the two characters `\t` and never splits.
  2. It splits on runs of whitespace (`\s+`) and drops empty tokens, as `read -ra` does.

  Line 9 of the description says so. `--list-tasks` uses the same `rows` definition.
- The test is `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_tab_separated_task_counts_as_an_amendment`. It runs through the storage facade (`store()`), the path a live read takes, and expects tasks 3, amendments 2, results 1, questions 1. Its history holds:
  - a TASK with a tab between the kind and `v1`;
  - a TASK with two spaces and a tab;
  - a RESULT with a leading tab;
  - a PONG with two tabs and a trailing tab;
  - a PONG whose `\tstatus=question` is a backslash and a `t`, not a tab.
- Mutation proofs (validation §7): four mutants, all killed:
  - the single-space split, which is the code at `8576645c`;
  - no unescape;
  - empty tokens kept;
  - an unescape of `\t` alone.
- Size, against the INV-2 caps: 499 added lines outside tests (cap 500), 507 under tests (cap 1000), and 12 files outside `.orchestration` (cap 15). The fix edits two existing lines in place.
- The three P2 (the fill_sweep URL key, the record, the report claim): no change, per the ACCEPTANCE.
- Seen, not changed: `scripts/agent-stop-gate.sh:277` also splits each history body on one space (`split($3, w, " ")`). It is not in allowed_files and it is a Claude-boundary hook, so routing it is the orchestrator's call.
