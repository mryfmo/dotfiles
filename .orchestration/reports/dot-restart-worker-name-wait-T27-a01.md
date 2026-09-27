# T27 report — dot-restart-worker-name-wait-T27-a01

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`
- branch: `fix/restart-worker-name-wait` (base `origin/main` = `02a0069`)
- task_rev: sha256 `ac90ed8328b939f3f2672e1ea7100628de0b1d650378afd0ce2b2088401bd4cf`
  verified against the task file on `origin/main` and again on the branch base
  (see validation file)
- PR: https://github.com/mryfmo/dotfiles/pull/189, head `fcc188c9f882dc5b512712dc3b712c89bba525c2`
- status: ready_for_review; CI green on head fcc188c (all checks pass, nix skipping; verbatim in validation file)

## Changes

1. `home/dot_local/bin/common/executable_herdr-agents`
   - New `wait_for_agent_name_release` (shdoc, English), placed after
     `wait_for_agent_ready`. It polls `herdr agent list` and succeeds once
     `.result.agents | type == "array" and all(.[]; .name != $name)` is true.
     A herdr failure, a jq failure, empty output, or a non-array shape all count
     as "still taken" for that poll.
   - The bound is `HERDR_AGENTS_NAME_RELEASE_POLLS` (default 30) ×
     `HERDR_AGENTS_NAME_RELEASE_INTERVAL` (default 1s). Both are test seams;
     production defaults are unchanged from the task spec (~30s).
   - It prints one stderr line, `Waited for herdr agent registration <name> to
clear.`, only when the name cleared after at least one poll iteration
     (`poll > 0`).
   - `start_agent_in_pane` gets a new first arm in the existing
     `case "${agent_output}"`: `*agent_name_taken*` calls
     `wait_for_agent_name_release`, then retries `herdr agent start` exactly
     once. Because `case` runs a single arm, a failed retry cannot fall into the
     timeout retry arm. If the name never clears, the original
     `agent_name_taken` output reaches the unchanged
     `Failed to start %s agent %s: %s`. If the retry fails, that same message
     shows the retry's output.
   - The `*agent_not_ready*` check, the timeout arm, and the shell-prompt
     refusal are all unchanged. `restart_worker_in_pane` is unchanged.
   - The shdoc of `start_agent_in_pane` gets one added clause.
2. `README.md`: in the `--restart-worker` paragraph, one clause about the bounded
   wait for a stale same-name registration (`agent_name_taken` race) followed by
   a single retry.
3. `.orchestration/learning/rule_candidates/herdr-worker-relaunch.md`:
   Addendum 5 is marked resolved by T27. This file is committed on the PR branch
   (it is not tagged main-checkout in allowed_files).
4. `tests/unit/test_herdr_agents.py`: the fake herdr gains an `agent list` branch
   plus state files `agent-start-name-taken.txt` (a one-shot `agent_name_taken`
   start failure) and `agent-list-taken-polls.txt` (the number of polls that
   still show the name; `-1` means forever). `run_helper` pops the two seam env
   vars. New tests:
   - (a) `test_restart_worker_waits_for_stale_registration_then_retries_once`:
     `--restart-worker`, name held for 2 polls. Asserts rc 0, `agent list` ≥ 3
     (counted from the call log), exactly 2 identical starts, and the stderr
     wait line.
   - (b) `test_agent_name_taken_gives_up_after_bounded_wait`: full mode, name
     held forever, seams set to 3 polls and a 0s interval. Asserts rc ≠ 0,
     exactly 3 polls, 1 start, the truthful failure message, and no wait line.
     It runs in milliseconds.
   - (c) `test_successful_agent_start_does_not_poll_agent_list`: normal full
     mode. Asserts no `agent list` calls and no wait line.

## Evidence summary (verbatim outputs in the validation file)

- Mutation baseline on the unmodified script: (a) FAIL (rc 1,
  `Failed to start claude agent claude-worker-w-old: agent_name_taken: …`,
  which reproduces the live failure) and (b) FAIL (`0 != 3` agent list polls).
  (c) passes, as expected for a regression guard.
- After the fix: all 3 targeted tests pass, `make unit-test` passes 458 tests
  (OK, skipped=1), `make validate-agent-assets` is OK, and shellcheck and
  `shfmt --indent 4 --space-redirects --diff` (the Makefile `format` flags) are
  clean.
- No local bats was run.

## Durable facts

[memory:decision] T27: start_agent_in_pane handles agent_name_taken via bounded
herdr agent list polling until the stale registration clears, then one retry;
wait emits a stderr line only when it fired (operator 2026-09-27).

CompactionDB (run from the main checkout):

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T27: start_agent_in_pane handles agent_name_taken via bounded herdr agent list polling until the stale registration clears, then one retry; wait emits a stderr line only when it fired (operator 2026-09-27)"
```

The output (memory ID) is `dcadc0c4-a62c-4d12-af4e-372b9fd87a8b`, also pasted
in the validation file.

## Disclosures / deviations

- Plan mode was active at session start, so the harness required a plan file,
  which was written at
  `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/agmsg-new-message-363-tender-cook.md`
  (main checkout). That is a write outside the worktree and outside the listed
  `.orchestration` paths. It is untracked worklog content and was not
  committed.
- After the commit, the understand-anything PostToolUse hook asked for an
  incremental `.ua/` graph update. It was skipped because `.ua/` is outside
  `allowed_files`. A graph refresh remains a separate worker task.
- `make require-crit-review` was not run; it stays orchestrator-side per the
  regime.
- The live `--restart-worker` E2E was not run by the worker. The stderr wait
  line exists so that the orchestrator's live E2E can tell "race absorbed"
  apart from "no race".

cost: n/a
