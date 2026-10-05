# AGMSG-TASK dot-restart-worker-name-wait-T27-a01

## Objective

Fix the transient `agent_name_taken` failure found in the T26 live E2E
(acceptance addendum, 2026-09-27): right after `--restart-worker` exits the
old worker agent, its herdr agent registration (e.g. `claude-worker-<ws>`,
status Idle) can linger until herdr notices the process exit, so the
immediate `herdr agent start` with the same name fails with
`agent_name_taken`. A retry ~10s later succeeds. Make `herdr-agents` absorb
this race deterministically instead of relying on a manual retry.

Verified herdr API facts (orchestrator, read-only, 2026-09-27 — treat as
constraints, do not re-litigate):

- `herdr agent` has NO stop/remove/unregister subcommand.
- `herdr agent wait --until` accepts only idle/working/blocked/done/unknown;
  there is no "registration gone" state. The stale registration reports
  status Idle, so a `wait --until idle` SUCCEEDS on the stale entry —
  `wait_for_agent_ready` cannot be reused for this.
- `herdr agent list` prints JSON: `.result.agents[]` entries carry `name`
  (the registration name, absent for unregistered agents) and
  `agent_status`. Waiting for the name to disappear from that list is the
  only available release check.

[memory:decision] T27: start_agent_in_pane handles agent_name_taken by
polling `herdr agent list` (bounded, ~30x1s) until the stale registration
name clears, then retrying agent start once; the wait emits one stderr line
only when it actually waited (operator 2026-09-27).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`, then
  `git switch -c fix/restart-worker-name-wait origin/main`.
  (Base must contain this task's commit; verify the task_rev sha256 from the
  dispatch message against `.orchestration/tasks/dot-restart-worker-name-wait-T27-a01.md`
  on your base, else stop and PONG.)
- If the worktree has uncommitted files, stop and report via AGMSG-PONG.

## Changes

### 1. `home/dot_local/bin/common/executable_herdr-agents`

Fix location is FIXED (do not move it): `start_agent_in_pane` (currently
lines ~201-233), the shared function every agent start routes through. It
already has the pattern to follow: `*agent_not_ready*` → wait → return,
`*timeout*` → wait → retry once.

- Add a helper `wait_for_agent_name_release` (shdoc-documented, English):
  poll `herdr agent list` and succeed when `.result.agents[].name` no longer
  contains the given registration name (jq test; treat a herdr/jq failure as
  "still taken" for that poll). Bounded like `wait_for_agent_ready`:
  ~30 iterations with a short sleep (~1s; total bound ~30s). When the loop
  actually waited at least one iteration before the name cleared, print ONE
  stderr line, e.g.
  `Waited for herdr agent registration <name> to clear.` — observability so
  a live E2E can distinguish "race absorbed" from "no race occurred". No
  stderr line when the name was already free is acceptable because the
  helper is only invoked from the failure branch below (the start already
  failed once, so a wait always happened conceptually — still, emit the
  line only after at least one poll iteration to keep the normal path
  silent).
- In `start_agent_in_pane`'s failure handling, add an `*agent_name_taken*`
  branch (analogous to the existing `*agent_not_ready*` / `*timeout*`
  cases): call `wait_for_agent_name_release "${agent_name}"`; on success,
  retry `herdr agent start` exactly once and return its pane id on success.
  If the name never clears within the bound, or the retry fails, fall
  through to the existing truthful failure message
  (`Failed to start %s agent %s: %s`). Keep every existing branch and the
  fail-safe refusal semantics unchanged.
- `restart_worker_in_pane` needs no change (the fix lives in the shared
  function).
- Update the shdoc comment of `start_agent_in_pane` (one clause) and keep
  all comments English/shdoc-compatible.

### 2. `README.md`

In the `--restart-worker` paragraph, add one clause: the start path waits
bounded for a stale herdr agent registration of the same name to clear
(`agent_name_taken` race) before retrying once.

### 3. `.orchestration/learning/rule_candidates/herdr-worker-relaunch.md`

Mark Addendum 5 resolved: append one line stating the gap is fixed by T27
(`agent_name_taken` handled in `start_agent_in_pane` with bounded
wait-for-release + single retry), so the candidate no longer carries an open
tooling gap.

### 4. Tests — `tests/unit/test_herdr_agents.py`

Use the existing fake-herdr / state-file pattern from the T25/T26 tests.

- (a) Race absorbed: fake `herdr agent start` fails with `agent_name_taken`
  while the fake `agent list` still shows the name for N (>=2) polls, then
  clears it; assert the start ultimately succeeds, assert the fake was
  polled >= N times (count invocations via the state file — asserting
  success alone is NOT acceptable), and assert the stderr wait line
  appeared.
- (b) Never released: fake `agent list` keeps the name forever; assert the
  bounded wait gives up and the run fails with the truthful message
  (bounded: the test must not run for the full real-time 30s — shrink the
  bound via the seam the implementation provides, e.g. an iterations/sleep
  variable, without changing production defaults).
- (c) Normal path regression: a start that succeeds first try performs no
  `agent list` polling and emits no wait stderr line.
- Mutation baseline REQUIRED: run the new tests against the unmodified
  script and paste the FAILED output in the validation file before pasting
  the passing run.
- No local bats (repo policy).

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `README.md`
- `tests/unit/test_herdr_agents.py`
- `.orchestration/learning/rule_candidates/herdr-worker-relaunch.md`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-restart-worker-name-wait-T27-a01.md` (main checkout)

## Forbidden actions

- Any change to manifest/profiles (`agent-config.yaml`, generated env or
  settings), generator/validator scripts, other herdr-agents code paths
  (attach repair, workspace lookup, restart flow beyond the shared start
  function), permgate, hooks configs, dependencies, or
  `reviews/ADH_Integrated_Plan/`.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
   Watch CI to green.
2. Artifacts at the exact expected paths, validation with verbatim outputs
   (including the mutation baseline FAILED run) and the PR number/head SHA.
3. CompactionDB from the main checkout:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T27: start_agent_in_pane handles agent_name_taken via bounded herdr agent list polling until the stale registration clears, then one retry; wait emits a stderr line only when it fired (operator 2026-09-27)"`
   — paste command and output.
4. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
