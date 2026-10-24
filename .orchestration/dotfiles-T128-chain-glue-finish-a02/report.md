---
task_id: dotfiles-T128-chain-glue-finish-a02
seat: claude-standard-dot-a008
reset_of: dotfiles-T128-chain-glue-finish-a01
pr: 378
branch: tools/chain-glue-finish
head_at_dispatch: b09c88c6deaed78ca7c06bfb314cd52bff1123e8
merge_base: 4eafd890454e495fdb1d429734c5835e46c87652
test_commit: cf0aa46c
fix_commit: 4628fc06
task_sha256: ddb8c53f4bb98a9cd3dc1dfd75d4b65c09b4e548dc1ae9908f0d59bc661bd369
---

# Report: dotfiles-T128-chain-glue-finish-a02, chain-finish.sh's shim exclusions in the lint's normalised form

- **Producer:** worker (Claude seat, worktree worker-f).
- **Branch:** PR #378 continues on `tools/chain-glue-finish` from `b09c88c6`, and every a01 commit and artifact is kept. The local branch was an ancestor of that head and was fast-forwarded.

## Item 1: `scripts/orchestrator/chain-finish.sh` (+2/−2)

The two tests at lines 67 and 111, each `[[ ${found} == /* && ${found} != */shims/* ]]`, now read `[[ ${found} == /* && "$(realpath -- "${found%/*}" 2> /dev/null)/" != */shims/* ]]`.

- **The normalisation:** the statement normalises what it compares, the binary's directory resolved by `realpath`, in the form the comparison lint accepts. No allow marker is used.
- **Refusals:** a relative or empty `${found}` still fails `== /*`. A directory that resolves into a `shims/` directory is now refused as well.
- **Why the directory, not the file:** resolving the binary itself would let every mise shim through, since a shim is a symlink to the mise binary outside `shims/`. The directory keeps the exclusion's intent.
- **Unchanged:** the messages, exit codes and every other line are byte-identical.

## Item 2: the test (+15)

The new test is `ChainIntegrateTest::test_shim_exclusion_compares_the_resolved_path`.

- **Its cases:**
  - real binaries outside any `shims/` directory are accepted (the default run, exit 0);
  - a symlink under `shims/` that resolves outside it is refused with exit 10;
  - a path through a directory linked to `shims/` is refused with exit 10.
- **Red and green:**
  - red at `b09c88c6` on the behavioural assertion, the linked-directory case accepted with exit 0;
  - green at `4628fc06` (validation §1, §2).
- **What was already green:** the symlink-under-`shims/` case was already refused at `b09c88c6`, because the old test matched `*/shims/*` on the unresolved path. The linked-directory case is the behaviour that resolving the path adds.
- **The selector name:** the task text names `ChainGlueTest`, but the module's only class is `ChainIntegrateTest`. Neither an alias nor a subclass could make the name resolve without running every inherited test twice. So the test lives in `ChainIntegrateTest`, and the threat table's selector needs `ChainIntegrateTest`, an orchestrator amendment.
- **The lint pair:** `python3.15 -I scripts/lint-comparisons.py --changed scripts/orchestrator/chain-finish.sh` exits 1 at `b09c88c6` (R1 at :67 and :111) and 0 at `4628fc06`.

## Check (validation §2)

- **The two modules:** `python3.15 -m unittest tests.unit.test_chain_glue tests.unit.test_lint_comparisons -v` passes 42 tests.
- **The script:** `bash -n` and `shellcheck` exit 0.
- **The test:** `ruff check` exits 0.
- **Caps for this reset's own commits (`git diff --numstat b09c88c6 <head>`):**
  - 4 of 40 changed lines outside `tests/` and `.orchestration/`;
  - 15 of 120 under `tests/`.
- **PR-wide, from merge-base `4eafd890` (for attribution, not this reset's budget):** 178 changed lines outside `tests/` and `.orchestration/`, and 290 under `tests/`.

## Residuals

`realpath` resolves the directory at check time, so a directory relinked between the check and the run is not seen. Under the threat table this is accepted: the check is a guard against picking up mise shims, not a trust boundary.

cost: n/a

## Round 4: the Bot fix round (AGMSG-ACCEPTANCE status=revise round=4, 2026-10-21T22:50:55Z; previous head 2b586637)

- **Producer:** worker (Claude seat).
- **Why this round:** the sweep of `2b586637` found two Bot threads from the a01 rounds that were never dispositioned. Both are real in the current code. This is the text's one worker Bot fix round (Worker Playbook step 15); the text is unchanged.
- **Commits:** the red tests are `7dfe6b9d` and the fix is `afbe3d4d`.

| Thread | Fix in `scripts/orchestrator/chain-finish.sh` | Test (`ChainIntegrateTest::…`), red at 2b586637, green at afbe3d4d |
| --- | --- | --- |
| 4302085363 (P1) | `ff-main.sh` runs as `ff_run`: `env -i PATH=<the pre-merge links> HOME TMPDIR`, like `cost_run`. The link set gains `mktemp`, `dirname`, `mv`, `cp` and `rm`, which `ff-main.sh` calls | `test_finish_runs_ff_main_with_the_pre_merge_links`: ff-main's PATH was the inherited one; now it is the links directory, and a hook finds each of its commands there |
| 4302085368 (P2) | after the head check, before any GitHub write: `gh pr view --json baseRefName`, refusing with exit 10 and `PR <n> does not target main: <base>` unless the base is `main` | `test_finish_refuses_a_pr_whose_base_is_not_main`: exit 0 and the merge ran; now exit 10, with no thread resolved and no merge |

- **An updated test:** `test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head` now expects both read-only `gh` calls, head and base, before that refusal. Its intent, no GitHub write, is unchanged.
- **Checks:** `test_chain_glue` and `test_lint_comparisons` pass. `bash -n`, `shellcheck`, `ruff check` and the comparison lint exit 0.
- **Caps:**
  - PR-wide, from merge-base `4eafd890`: 183 of 200 outside `tests/` and `.orchestration/`, and 314 of 320 under `tests/`;
  - this round: +9/−4 and +26/−2.
- **Bot:** no `@codex review` was requested after the fix, because `gh pr comment` matches an ask rule this seat does not run.
