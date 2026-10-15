# Report: dotfiles-T128-orchestrator-tools-followup-a01

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/orchestrator-tools-followup`. It was cut with `--no-track` from `origin/main` at `727180db`, boundary (15). The earlier branches `tools/gate-wrapper-path` and `tools/chain-github-scripts` are left as they are.
- **Task copy.** The task file's sha256 `ae208bef…` matches the TASK's `task_sha256`. It is copied byte-identical to `.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/task.md` and holds no home path. Both premises replay as `present` (validation §1).
- **Commits.**
  - `0bb86ab8`: the five fixes and their tests.
  - Then this evidence.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## The owned rows

Item 1's whole definition is the section `## Owned by dotfiles-T128-orchestrator-tools-followup-a01` of `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md` as read from `origin/main`.

- **22 rows.** By the record's `id<TAB>class` grammar the section holds 22 rows (validation §2). Boundary (15), `727180db`, added the last three.
- **A count to check.** The TASK note says 23. No other line under the heading matches the grammar.
- **They reduce to five defects.** 15 of the 22 rows name one of five defects that were still in the code. Five more were already fixed on `origin/main`, and two name orchestration files outside `allowed_files`.

| # | Row | Class | What it names | Disposition |
|--:|---|---|---|---|
| 1 | `local:9ad0c15:3` | advisory-p2 | boundary.sh: deleted `.orchestration` files abort the copy | `fixed:0bb86ab8` (D1) |
| 2 | `local:9ad0c15:4` | advisory-p2 | ff-main.sh: a locally deleted tracked file aborts the move | `fixed:0bb86ab8` (D2) |
| 3 | `4260535916` | deleted-path-handling | Bot, PR #346, boundary.sh:44: the same as row 1 | `fixed:0bb86ab8` (D1) |
| 4 | `4260535924` | deleted-path-handling | Bot, PR #346, ff-main.sh:38: the same as row 2 | `fixed:0bb86ab8` (D2) |
| 5 | `local:7b574d3:1` | advisory-p2 | boundary.sh: deletions, and a rename copies only its new path | `fixed:0bb86ab8` (D1) |
| 6 | `audit:7b574d3:1` | trust-boundary-dispositions | fill_sweep.py:60: review bodies and issue comments filled whatever they say | `fixed:c586f20d` (on main before this task) |
| 7 | `audit:7b574d3:2` | trust-boundary-dispositions | fill_sweep.py:49: any account's reply supplies a disposition | `fixed:c586f20d` (on main before this task) |
| 8 | `audit:7b574d3:3` | stale-evidence | orch-audit.sh:72: a rerun can accept a stale receipt | `fixed:c586f20d` (on main before this task) |
| 9 | `audit:7b574d3:4` | deleted-path-handling | boundary.sh:44: the same as row 1 | `fixed:0bb86ab8` (D1) |
| 10 | `audit:7b574d3:5` | deleted-path-handling | ff-main.sh:37: the same as row 2 | `fixed:0bb86ab8` (D2) |
| 11 | `audit:7b574d3:6` | search-procedure | the a02 acceptance record lacked the counter output and the records search | proposed `fixed:df044557` (the orchestrator's boundary (13) pasted both) |
| 12 | `audit:7b574d3:7` | evidence-claim | the a02 report's CompactionDB identifiers lack their command output | proposed `not-applicable:` (below) |
| 13 | `local:8576645:1` | advisory-p2 | boundary.sh: the same as row 1 | `fixed:0bb86ab8` (D1) |
| 14 | `local:8576645:2` | advisory-p2 | ff-main.sh: the same as row 2 | `fixed:0bb86ab8` (D2) |
| 15 | `audit:8576645:2` | disposition-key | fill_sweep.py:68: one extra.tsv row on a check run's URL fills every annotation of the run | `fixed:0bb86ab8` (D4) |
| 16 | `local:046901b:1` | advisory-after-last-round | boundary.sh: the same as row 1 | `fixed:0bb86ab8` (D1) |
| 17 | `local:046901b:2` | advisory-after-last-round | ff-main.sh: the same as row 2 | `fixed:0bb86ab8` (D2) |
| 18 | `audit:046901b:1` | trust-boundary-dispositions | fill_sweep.py:67: a badge-free review at `changes_requested` is filled as "without a finding" | `fixed:0bb86ab8` (D3) |
| 19 | `audit:046901b:2` | disposition-key | fill_sweep.py:68: the same as row 15 | `fixed:0bb86ab8` (D4) |
| 20 | `local:f48593d:2` | advisory-p2 | orch-gate.sh: a failure after the head's checkout skips the restore | `fixed:28eec93c` (on main before this task) |
| 21 | `audit:6847aa9:1` | path-shim-discovery | orch-gate.sh: the gate's PATH can reach a mise shim | `fixed:5ec86052` (on main before this task, PR #355) |
| 22 | `audit:a235637:1` | trap-restores-on-refusal | orch-gate.sh:63: a shims refusal still moves the review worktree to origin/main | `fixed:0bb86ab8` (D5) |

In a row id `<source>:<head>:<n>`, n is the n-th finding in that review's header list or that audit's final message (validation §3).

### The rows already fixed on `origin/main` (validation §4)

- **Rows 6 to 8** were a02's three post-round audit P1 findings. a05 fixed them on PR #346, which merged as `c586f20d`:
  - row 6: the badge rule, under `test_fill_sweep_leaves_a_badged_review_body_a_gap`;
  - row 7: `--orchestrator-login` and `ignored-reply`, under `test_fill_sweep_ignores_a_disposition_reply_from_another_login`;
  - row 8: the exclusion of this head's audit files, their removal, and the `-newer` check, under `test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt`.
- **Row 20.** PR #350 landed orch-gate.sh as `28eec93c` with the trap before the head's checkout, under `test_orch_gate_restores_the_review_worktree_when_setup_fails`.
- **Row 21** is PR #355, `5ec86052`, with its three tests in `tests/unit/test_orch_gate_path.py`.

### The two orchestration rows

- **Row 11 (`audit:7b574d3:6`)** names `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md`. That record is the orchestrator's and is outside `allowed_files`. The counter output and the records search the finding asked for are in it at lines 41 to 48, pasted by `df044557`, boundary (13). The proposed disposition is `fixed:df044557`.
- **Row 12 (`audit:7b574d3:7`)** names the a02 report, which is outside `allowed_files`, so the line cannot be changed here.
  - **The claims.** The report's lines 82 and 107 claim two memory identifiers.
  - **No lookup.** The seat cannot look them up: the sandboxed `memory list` in the main checkout fails with `contextdb: [Errno 1] Operation not permitted` (validation §4). The Playbook sanctions only `memory add` outside the sandbox.
  - **Proposed disposition:** `not-applicable:the named file is the a02 report, outside this task's allowed_files, and the identifiers can be checked only by a read of the main checkout's CompactionDB, which the seat's sandbox refuses; evidence=git show origin/main:.orchestration/reports/dotfiles-T128-orchestrator-tools-a02.md | grep -nE '9ac653b5|b4cc3273'`.
  - **The orchestrator's check.** It can confirm the identifiers with `uv run --no-project .claude/hooks/contextdb_cli.py memory list` in the main checkout.
  - **This task's own record** carries the executed `memory add` command and its output (the main-checkout copy of this report).

## The five fixes (`0bb86ab8`)

### D1: `scripts/orchestrator/boundary.sh` (rows 1, 3, 5, 9, 13, 16)

- **The root cause.** `git status --short | awk '{print $NF}'` gave one path per entry and dropped the entry's nature. The copy loop then ran `cp` on a deleted path and aborted under `set -e`. A rename gave only its new path, so the old path stayed in the boundary worktree.
- **The listing.** The script now lists `git status --porcelain -z --no-renames --untracked-files=all -- .orchestration`. These paths are unquoted, and a rename appears as its old path's deletion plus its new path.
- **Each path.** A present path is copied as before. A missing path is deleted in the boundary worktree with `git -C <tree> rm -q --ignore-unmatch`, so the header's "nothing is removed with `rm`" still holds.
- **The masker** gets the copies only, and does not run when there are only deletions.
- **The header** now names the new command.
- **The test** is `test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path`. The setup tracks three files on origin, deletes one and `git mv`s another.
  - **The commit** shows `D gone.md`, `A new.md`, `D old.md` (with `--no-renames`).
  - **The branch's tree** is `kept.md` and `new.md`.
  - **The masker's file arguments** are `new.md` alone.

### D2: `scripts/orchestrator/ff-main.sh` (rows 2, 4, 10, 14, 17)

- **The root cause.** `git diff -z --name-only` lists a locally deleted tracked file, and the unconditional `mv` on it aborted the run.
- **The split.** The list now splits into present paths, moved aside as before, and missing paths.
- **The missing paths.** `git checkout --` restores them with the tracked ones, so the fast-forward can run even when `origin/main` changes them. After the merge, whether it was refused or not, each one still present is deleted again and listed as `deleted: <path>`.
- **The ERR trap** also names the deleted paths it restored.
- **The header** now says `rm` touches its `$TMPDIR` directory and the locally deleted files.
  - **The choice.** I used plain `rm`, not `git rm`, so the deletion stays unstaged, as the user had it.
- **The test** is `test_ff_main_keeps_a_local_deletion_across_the_fast_forward`.
  - **The setup.** The tracked file is deleted locally while `origin/main` changes it.
  - **The fast-forward** lands, and the file is still absent.
  - **A refused fast-forward** leaves it absent too.

### D3: `scripts/orchestrator/fill_sweep.py`, the review levels (row 18)

- **The root cause.** `NEUTRAL` named levels only for annotations and statuses, so any badge-free review got the rule "review object without a finding". That included `changes_requested`.
- **The fix.** `NEUTRAL` now has `review` and `codex_review` at `commented`, so a review at any other level stays a gap.
  - **The levels.** The other levels pr-feedback.py gives are the review state lowercased: `changes_requested`, `approved`, `dismissed`.
  - **The approach.** This is the allowlist form the annotation and status rules already use.
- **The docstring** says so.
- **The test** is `test_fill_sweep_fills_only_a_commented_review`. Of four plain reviews and two of the Bot's (body `Codex Review`), only the two at `commented` are filled.
- **A changed fixture.** The badged-review test's two review fixtures gain `"level": "commented"`, the field pr-feedback.py gives every review. Without it a review has no level and is now a gap.

### D4: `scripts/orchestrator/fill_sweep.py`, the shared keys (rows 15, 19)

- **The root cause.** The extra.tsv key was the URL's fragment. The annotations of one check run share the run's URL, and so do the run's own `check_run` item and statuses with a null URL. One row therefore filled every one of them.
- **A shared key takes no row.** A fragment that more than one item shares now takes no extra.tsv row. The script prints `shared-key <key> item-<n>` for each item a row would have matched.
- **The item id.** Every item also answers to `item-<n>`, its index in the sweep. A shared item's GAP line is named by that id, and its evidence command is `jq '.items[<n>]'`.
- **Unchanged.** Items with a unique URL behave as before.
- **The test** is `test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id`.
  - **The fixture.** There are three annotations on one run URL: warning, failure and notice.
  - **A URL row.** It fills none of them, and the script names all three. The warning and the failure stay gaps, and the notice takes its rule with `.items[2]`.
  - **Two `item-<n>` rows** fill the warning and the failure.

### D5: `scripts/orchestrator/orch-gate.sh` (row 22)

- **The root cause.** The EXIT trap always ran `clean` and `checkout -qf --detach origin/main`. The shims refusal comes after the trap and before the head's checkout, so a refusal moved a clean review worktree that had been elsewhere.
- **The fix.** `moved=1` is set right before the head's checkout, and the trap restores only when it is set. The private directory is always removed, as before.
- **The header** now says so.
- **The test** is `test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout`.
  - **The setup.** The review worktree is detached at the PR head, a clean worktree that is not at `origin/main`, and a `mise` stub answers a `shims` path.
  - **The run** exits 2, and the review worktree's HEAD and status are unchanged.
  - **The gate** never ran.
- **The other module.** The task does not allow `tests/unit/test_orch_gate_path.py`, so I left it unchanged. Its three tests still pass (validation §5).

## Proofs and size

- **Tests.**
  - `test_orchestrator_tools.py`: 45 tests OK, the 40 of `origin/main` plus the five new ones.
  - The neighbouring modules `test_orch_gate_path.py`, `test_regime_counters.py` and `test_chain_github_scripts.py`: 33 tests OK.
- **Linters.** shellcheck, shfmt, ruff check and ruff format are clean (validation §5).
- **Mutation proofs.** 11 mutants, all killed (validation §6).
  - M1, M2 and M5 are `origin/main`'s scripts.
  - M3, M4, M6, M7, M8, M10 and M11 each undo one part of a fix.
  - M9 sets the flag before the binaries are resolved.
- **Caps (INV-2).** 5 files outside `.orchestration/` (of 15), 66 added lines outside `tests/` (of 500), 102 under `tests/` (of 1000) (validation §7).
- **The repository validator** passes on `0bb86ab8` (validation §8).

## Threat table

| Row | Where it is bounded |
|---|---|
| boundary.sh, ff-main.sh, fill_sweep.py, orch-gate.sh | exactly the owned rows above: D1 to D5, each with its test and its mutants |
| the other allowed scripts (orch-audit.sh, acceptance-front-matter.py, codex-review.sh, design-keydiff.py, replay.sh, dispatch.sh, bus-read.sh, three-repeat.sh, regime-counters.sh) | unchanged; no owned row names a defect in them that is still present |
| tests/unit/test_orchestrator_tools.py | five new tests and two fixture fields (D3); nothing else |
| tests/unit/test_regime_counters.py | unchanged |
| the task copy | byte-identical, sha256 `ae208bef…` (validation §1) |
| environment inputs | no new binary. boundary.sh adds `git rm` and `cut`, both in the row's list (git, coreutils), and drops `xargs` from that line |
| new or renamed scripts | none |

## Notes for the orchestrator

- **fill_sweep.py's output gains two forms.**
  - `shared-key <key> item-<n>` is printed when an extra.tsv row matches a shared fragment.
  - A GAP line for a shared item is named `item-<n>`.
  - **A tighter rule.** An `approved` or `dismissed` review is now a gap, just as a `changes_requested` one is.
- **ff-main.sh prints `deleted: <path>`** for each local deletion it keeps.
- **Two rows wait on your decision.** Rows 11 and 12 carry proposed dispositions only, because the files they name are outside this task's `allowed_files`.
- **The Understand-Anything stale-graph hook** did not fire in this task. plan-mode-used: no.

## CompactionDB

The main-checkout `memory add` runs after CI, with the masked main-checkout copy. Its exact command and output go into the main-checkout copy of this report.

- [memory:decision] The tools lineage's owned rows close in `0bb86ab8`:
  - boundary.sh lists `git status --porcelain -z --no-renames` and `git rm`s missing paths in the boundary worktree;
  - ff-main.sh restores local deletions for the fast-forward and deletes them again;
  - fill_sweep.py fills a review only at `commented`, and a URL fragment shared by several items takes no extra.tsv row (`item-<n>` names one);
  - orch-gate.sh's trap restores the review worktree only after the head's checkout started.
- [memory:failure] `git status --short | awk '{print $NF}'` drops what an entry is. A deletion then reaches `cp` and aborts, and a rename leaves its old path behind. List with `--porcelain -z --no-renames` and split present from missing paths.

## Bot and CI

The PR opens after this evidence commit. The CI result and the Bot's review of the final head go into the main-checkout copy and the RESULT.
