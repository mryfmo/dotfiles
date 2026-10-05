# T33h report — dot-permgate-codex-stdin-T33h-a01 (revision 1)

- worker: `claude-standard-dot-a005`; orchestrator: `claude-remediation-dot`
- worktree: `~/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `fix/permgate-codex-stdin` from `origin/main` = `a4bddfc`
- task_rev: sha256 `15857f6d1deb08f5afeb9fa280f761bea3cf6a127aad8737ea848cf07dede14b`, checked
- cleanup: deleted the local branch `fix/ua-core-build-shim` (was `02fdac1`, merged as `2b30a21`), as the task allows
- PR: https://github.com/mryfmo/dotfiles/pull/203, head `6bc5918808b71b802c74bc35064e78079f7b9712`
- status: ready_for_review. CI is green on head 6bc5918: all checks pass except nix, which was skipped. Verbatim `gh pr checks 203` output is in the validation file.

## Changes

1. **`home/dot_local/bin/common/executable_permgate` `classify()`.** Added
   `stdin=subprocess.DEVNULL` to the codex `subprocess.run`, the branch that
   passes `--output-last-message`, with a two-line comment. This is 3 added
   lines and nothing else. The claude branch (`input=prompt`), timeouts,
   prompts and the policy are unchanged.
2. **`bench`.** No separate change is needed. `run_bench` calls the same
   `classify(agent, subject, policy)` (line 697), and so does the
   PermissionRequest hook path (line 612). There is one code path, so one
   fix covers both.
3. **`tests/unit/test_permgate.py`.** New
   `test_codex_classifier_never_reads_the_callers_open_stdin`:
   - A fake codex that **also reads stdin to EOF**, like the pre-T33d
     fixture, runs through `permgate bench`.
   - The test gives that subprocess an `os.pipe()` read end as stdin and
     keeps the write end open. This makes the old failure deterministic in
     any runner, CI included, without relying on how the suite was launched.
   - It asserts codex gets `status_counts == {"classified": 5}`, with the
     full codex result as the failure message.
   - The T33d argv-prompt fixture stays the default fake.
   - **Why bench.** The hook path feeds permgate its payload on stdin
     (`input=`), which reaches EOF. A stdin-reading fake therefore passes
     there even on the old code. Only `bench` exposes the inherited-stdin
     dependency, which is why the test goes through `bench`.

## Proof (verbatim in the validation file)

- **Before**, unmodified permgate, confirmed by `git diff --quiet` against
  origin/main: the new case reports `AssertionError: {'timeout': 5} !=
  {'classified': 5}`, with latencies of about 202 ms (the 0.2 s fixture
  timeout), and **FAILED**. Under `sleep 20 |` it also FAILED.
- **After**: the new case is **OK**, both plain and under `sleep 20 |`.
  The whole `tests.unit.test_permgate` module under `sleep 20 |` gives
  44 tests OK (1 skipped).
- `make unit-test` gives 512 OK, and `make validate-agent-assets` is ok.

## CompactionDB

[memory:decision] T33h: permgate runs the codex classifier with `stdin=subprocess.DEVNULL`
so hook classification never depends on the caller's stdin (operator 2026-09-28, from the
T33d diagnosis).

Id `91474b74-4710-4fa5-b5c5-af23653ec661`; the output is in the validation
file.

## Effects

None outside the repository.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
