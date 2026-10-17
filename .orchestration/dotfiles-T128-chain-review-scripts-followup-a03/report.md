---
task_id: dotfiles-T128-chain-review-scripts-followup-a03
seat: claude-standard-dot-a002
branch: tools/chain-review-scripts-followup-a03
base: f7847616
code_commit: a311781d
test_commit: a1ddb211
lint_commit: 9da0897a
pr: 381
task_sha256: e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2
---

# Report: dotfiles-T128-chain-review-scripts-followup-a03

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/chain-review-scripts-followup-a03` from `origin/main` `f7847616` (PR #376). The PR #377 and #378 branches stay in the worktree, committed and pushed, until their acceptance.
- Task file: sha256 `e328a3fb…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 2026-10-17T00:43:08Z. All four premises replay equal (§2). No question and no amendment.

## What changed in `scripts/orchestrator/local-advisory.sh`

Validation §2a holds the diff.

- **(a), C-51:**
  - **Owner check:** after the exit 0 for a review without findings and before the heading, `.orchestration/tasks/<owner>.md` must exist. Otherwise the script prints `write the owner task <owner> first` and exits 2, and the record is untouched. The missing review file keeps its own exit 2 and message, and the `@exitcode 2` line names both.
  - **Evidence:** each `local-finding:` line's tail is `evidence=shasum -a 256 .orchestration/tasks/<owner>.md (<sha256>)`, with the file's hash at the time of writing.
- **(b), C-50:**
  - **Token:** a finding's token is the first match of `[A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?` in its line. The class excludes the backtick, so a backticked token reads as itself.
  - **Earlier findings:** the earlier files are the task's other `.orchestration/validation/<task>-local-review-*.md`, each numbered as the loop numbers its own (`grep -E '^- \[P[0-3]\]' | sort -u`, P0 and P1 included). Their findings are compared by exact token, through `awk '$1 == t'`.
  - **Class:** the new row takes the class of the last `local:<sha7'>:<n'>` row in the record for a matching finding, skipping rows classed `advisory-p2`. Its `local-finding:` parenthesis gains `; repeat of local:<sha7'>:<n'>`. Otherwise the class is `advisory-p2`, as before.
  - **Scope:** only the local review files and the `local:` rows.
- **The header** describes both. The P0/P1 stop, the heading and the once-only writes are unchanged.

## Tests

The module has 16 tests, all OK (validation §3): the fourteen on `origin/main` and two new ones.

| Row | Test |
|---|---|
| 1a | `test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file`. With no owner file: exit 2, `write the owner task t-followup-a01 first`, and the record byte-identical to the case's pre-run content. With the owner file: the line ends `; evidence=shasum -a 256 .orchestration/tasks/t-followup-a01.md (<sha256 of that file>)`. |
| 1b | `test_local_advisory_classes_a_repeat_by_the_earlier_row`. **Earlier reviews:** `aaaaaa1` has `scripts/x.sh:12` (row `quoting`) and `scripts/y.sh:3-5` (row `range-case`); `bbbbbb2` has `scripts/x.sh:12` (row `env-s-quoting`, later in the record). **Current review `cccccc3`:** `` `scripts/x.sh:12` `` gets `env-s-quoting`, the later row winning; `scripts/y.sh:3-5` gets `range-case`; `scripts/y.sh:3-9` gets `advisory-p2`, being another token; `scripts/z.sh:7` gets `advisory-p2`. The first two lines name `repeat of local:bbbbbb2:1` and `repeat of local:aaaaaa1:2`. A review without findings and no owner file exits 0 with no heading. |
| owned row `audit:40f3be4:2` | `test_local_advisory_matches_the_owner_heading_literally` gains the heading `## Owned by tXfollowup-a01 (x)` beside the near-misses. A regex match of `t.followup-a01` would take it as the owner's heading and write none; the literal match writes the owner's heading once. |

The two existing local-advisory tests, `test_local_advisory_records_p2_rows_and_stops_on_p0_p1` and the heading test, each gain the owner file the new check requires. The first one's expected `local-finding:` line takes the new evidence form. Nothing else in them changes.

**Mutation check** (validation §4): 6 mutants, each a literal replacement applied alone, all 6 caught; then the baseline of 16 tests passes. They are:
- the owner check off;
- the old `git show origin/main` evidence;
- the repeat class off;
- the first matching row winning instead of the last;
- the line-range part of the token removed;
- the heading matched as a regex.

The first pass, on `a311781d`, had two survivors:
- the range token, untested until the `y.sh:3-9` case was added in `a1ddb211`;
- a backtick strip with no effect, since the token class already excludes the backtick. The strip was removed in `a1ddb211`, so that mutant is gone.

## Readings, declared

- **The evidence's `(<sha256>)` tail** is item 1a's form, verbatim. Replayed as shell, the parenthesis is a syntax error, so a replay runs the command before it and compares with the hash in parenthesis.
- **"Latest matching head wins"** is read, per the TASK note, as the last matching `local:` row in the record. Rows are appended in review order, so the record's order is the heads' order.
- **A repeat row** is skipped when its class is `advisory-p2` itself, so an unclassed earlier row never overrides a classed one.

## Caps

Validation §5: outside `tests/` and `.orchestration/`, 1 file, 38 added and 5 deleted, so 43 changed lines (cap 200); under `tests/`, 60 added lines (cap 1000).

## CI and the Bot

- **The Bot:** PR #381 was marked ready at 00:48:01Z. No review came within 10 minutes, so `@codex review` was posted at 603 s (issue comment `6227663819`). The Bot answered with issue comment `6227679116` at 00:59:47Z, "Didn't find any major issues", Reviewed commit `d2b33025d0`, which was then the head. No thread.
- **CI on `d2b33025`:** `test (ubuntu-24.04, client)` failed at `Run ShellCheck` with SC2015 (info) on `local-advisory.sh:61`, the line `k=$((k + 1)) && t=$(token "$l") && earlier+=… || true`, and three `test` jobs were cancelled with it. The local ShellCheck 0.11.0 reports nothing there. `9da0897a` writes the line as an `if` with no change of behaviour. CI's own command, `git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x`, exits 0 locally. The 16 tests and the 6 mutants were re-run on it (validation §3 and §4). CI on the final head is in the RESULT.

## Not done, or outside scope

- `local-review.sh`, `sandbox-scan.sh` and `chain-integrate.sh` are unchanged.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
