# AGMSG-TASK dot-permgate-bench-flake-T33d-a01

## Objective

`tests/unit/test_permgate.py::PermgateTest::test_bench_runs_five_layer_two_fixtures`
failed twice on 2026-09-28 in the first full `make unit-test` run of the T33a
worktree (`successful_classifications: 0 != 5` for one agent) and passed alone
and on immediate full reruns each time. CI did not fail, but a test that
flips under load erodes the mutation-baseline discipline.

Do this in order and report each step:

1. Reproduce under load (e.g. run the full suite with the permgate tests
   pinned last, or run the bench test while a CPU-bound loop occupies the
   cores) and capture the failing benchmark JSON: which agent, which
   `status_counts` (`timeout`, `error`, …), which latencies. Paste it.
2. Diagnose from the JSON, not from guesswork. Likely mechanism: the fake
   CLIs are Python interpreter processes; interpreter startup under load can
   exceed the fixture policy's `timeout_seconds`, so `classify` returns
   `None` with status `timeout`. Confirm or refute.
3. Fix in the TEST FIXTURE only (`tests/unit/test_permgate.py`): e.g. give the
   fake-CLI policy the maximum headroom the validator allows (`0 <
   timeout_seconds <= 8`) for tests that assert successful classification,
   and make the bench assertion print `status_counts` on failure. Do not
   change `home/dot_local/bin/common/executable_permgate` or the shipped
   policy unless step 2 proves a product defect — in that case stop and
   PONG with the evidence before editing product code.
4. Prove it: the reproduction from step 1 no longer fails (paste), and the
   full suite passes twice in a row.

[memory:decision] T33d: the permgate bench unit test flaked under load
because fake-CLI interpreter startup exceeded the fixture policy timeout;
fixed in the test fixture (max validator-allowed headroom for fake CLIs,
status_counts in the failure message), product code untouched (operator
2026-09-28).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c test/permgate-bench-flake origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `tests/unit/test_permgate.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-permgate-bench-flake-T33d-a01.md` (main checkout)

## Forbidden actions

- Changing `executable_permgate`, `permgate-policy.yaml`, hooks, manifests,
  or any file outside allowed_files without a prior PONG ruling; merging;
  force push; local bats; `make apply`/`chezmoi apply`; writes outside the
  worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
python3 -m unittest tests.unit.test_permgate -k bench   (before and after, under load)
make unit-test   (twice)
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   and the PR number/head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above (adjust the mechanism wording to what step 2 actually proved) — paste command and output.
4. `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
