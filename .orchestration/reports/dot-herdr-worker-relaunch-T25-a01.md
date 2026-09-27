# Report: dot-herdr-worker-relaunch-T25-a01

- Worker: claude-standard-dot-a005 (claude-opus-5-5, high), pane `wF:p2`
- Status: **ready_for_review** (round 2). The round-1 blocker was cleared by the orchestrator's `668ff64`. I rebased the branch onto it and force-pushed once, as allowed. CI is fully green on the final head, and the previously skipped steps (shfmt, ShellCheck, Python unit tests, bats) all ran and passed on all three runners.
- **Final head: `f9b158a` (`f9b158a00695142df743ace4121f6b64048514a4`)**, a rebase of round-1 commit `3be4656` onto origin/main `668ff64` with no content change.
- task_rev verified: sha256 of the task file at origin/main `8b0f68f` = `bb37c81eec7617052c186b849647f43c676988fb13de21ab0466ee2efa16d51e` (matches). The worktree was clean before starting.
- Branch `feat/herdr-worker-relaunch`: the final base is origin/main `668ff64` and the **final head is `f9b158a`**. Round 1 was commit `3be4656` (`3be46563bf21c9e509c825d3f4357c235661a0ef`) on `8b0f68f`; round 2 rebased it with no content change.
- PR: https://github.com/mryfmo/dotfiles/pull/186 (not merged)
- Evidence: `.orchestration/validation/dot-herdr-worker-relaunch-T25-a01.md`

[memory:decision] T25: worker relaunch and the one-workspace-per-pair invariant are enforced in herdr-agents itself (`--restart-worker` plus a full-mode duplicate guard), documented in README, ruled in agmsg-orchestration.md, and checked by the validator and unit tests (operator 2026-09-27). CompactionDB id `692f51c0-2d96-4fdb-9cd9-2bf1ea57aa28`.

## Root cause of the observed duplicate workspace

I confirmed it with read-only `herdr workspace list` / `pane list`. The live pair workspace `wF` is labeled `dotfiles`, because attach mode keeps the workspace's own label. `find_existing_workspace` matched only the full-mode label `dotfiles agents`, so full mode never found `wF` and created a new workspace. The agentless worker pane was a side issue.

[memory:failure] herdr-agents full mode found existing pairs only by the `<dir> agents` label. Pairs built by attach mode therefore produced a duplicate workspace. T25 fixed this with a lookup based on pane evidence (2026-09-27).

A second live finding: `wF:p2` (this worker) was labeled `claude-orchestrator`. With `worker_kind=claude`, the Claude `SessionStart` hook runs `herdr-agents --attach` inside the worker pane, and attach renamed that pane as if it were the orchestrator. T25 guards this.

## Changes (all within allowed_files)

1. `home/dot_local/bin/common/executable_herdr-agents`
   - `find_managed_workspaces` replaces `find_existing_workspace`. A workspace is managed for DIR when it has the full-mode label and a pane in DIR, or when it has a `claude-orchestrator` pane in DIR. `single_managed_workspace` exits 2 with teardown instructions (`herdr agent prompt <pane> "/exit"`, then `herdr workspace close <id>`) when more than one matches. Full mode and restart mode both use it.
   - `--restart-worker [DIR]` locates the worker pane in this order: the registered `<kind>-worker-<ws>` agent, then the single pane labeled `<kind>-worker`, then an agentless pane. It restricts to the worker's tab and requires exactly the `claude-orchestrator` pane plus the worker pane (`attach_panes_are_unambiguous`); otherwise it exits 2. `restart_worker_in_pane` then runs `herdr agent prompt <pane> "/exit"` only when the pane has an agent, and calls `start_worker_agent … true`. That function waits (bounded) for the shell prompt and resolves the profile args through `resolve_worker_profile` / `MODEL_PROFILE_<P>_CLAUDE_ARGS`, including the trust-dialog handling. Restart mode never creates panes or workspaces. It exits 2 when DIR has no managed workspace, the worker pane is missing, or the tab is ambiguous or unmanaged. It does not require the `claude` CLI unless the worker kind is claude.
   - Full-mode guard: when the registered worker is gone, full mode first reuses the single labeled `<kind>-worker` pane. If that pane is agentless, it goes through the same `restart_worker_in_pane` path. If the pane still has a running agent, it is left alone. Otherwise the existing empty-pane or split fallback applies. Unmanaged panes (for example `files`) are still left untouched.
   - Claude-worker correctness: `has_claude_pane` and the layout-repair orchestrator lookup now exclude the worker pane, so a claude worker no longer counts as the orchestrator. Attach mode exits 0 without renaming when `HERDR_PANE_ID` is the registered worker pane.
   - The usage text, header shdoc (`@description`, `@option --restart-worker`, `@example`) and the new functions' shdoc are in English.
2. `README.md` (herdr-agents section): one paragraph covering the one-workspace-per-pair invariant and what counts as managed, a warning never to run full mode from inside the pair, `herdr-agents --restart-worker [DIR]` and when to use it (after a `worker_profile` or `worker_kind` change), its exit-2 cases, the attach self-guard, and how to tear down a stray workspace.
3. `home/dot_config/claude/rules/agmsg-orchestration.md`: one bullet requiring worker (re)launches to go through herdr-agents modes, with no full mode inside a pair and a profile change activated via `--restart-worker` using args from `~/.agents/model-profiles.env`.
4. `scripts/validate-agent-assets.py`: next to the worker_kind README check, validation fails with `README.md must document herdr-agents --restart-worker for worker relaunches` when the token is missing.
5. Tests
   - `tests/unit/test_herdr_agents.py`: 6 new tests. (a) `--restart-worker` sends `/exit`, then starts `claude-worker-w-old` in the same pane `w-old:p2` with `--model opus --effort high`, with no split or create. (b) It exits 2 with no managed workspace. It refuses a tab that contains an unmanaged pane. (c) Full mode in an attach-labeled workspace (`project`) starts the worker in the agentless `claude-worker` pane, with no create, split, or orchestrator restart. Full and restart modes both exit 2 on duplicate managed workspaces. Attach from the worker pane does not relabel it. The helpers gained `label` / `extra_workspace_ids` and positional mode args. (d) All 84 existing tests still pass (90 total). All 7 new test cases (6 methods, one with two subtests) FAIL against the origin/main script: this mutation check is in the validation file.
   - `tests/unit/test_validate_agent_assets.py`: the fixture README includes the token, and a new test shows a README without `--restart-worker` fails validation.
   - `tests/install/common/lifecycle.bats`: untouched. Its herdr assertions cover `herdr server reload-config` only, so nothing conflicts with the guard.

## Round 2 (after AGMSG-ACCEPTANCE revise, message 353)

- `git fetch origin` and `git rebase origin/main` onto `668ff64` (`chore(mise): sync ccusage pins to 20.0.23 …`) ran with no conflicts. The result is `f9b158a`.
- Force push, run once: `git push --force-with-lease=refs/heads/feat/herdr-worker-relaunch:3be46563bf21c9e509c825d3f4357c235661a0ef origin feat/herdr-worker-relaunch`, output `+ 3be4656...f9b158a (forced update)`, exit 0.
- Local checks before the push: `make unit-test` passed 447 tests with 1 skipped and exit 0 (the statusline failure is gone after the rebase). `make validate-agent-assets` passed. `shellcheck` gave exit 0. `shfmt -i 4 -sr -d` (the CI version, 3.14.1) printed no diff for herdr-agents. CI's shfmt glob does not cover `home/`; I ran it anyway.
- CI on `f9b158a`: all 12 checks pass and `nix` is skipping. Run 36283112037 shows `Smoke-test statusline tools`, `Run shfmt`, `Run ShellCheck`, `Run Python unit tests`, and `Run unit test` (bats) succeeding on `test (ubuntu-latest, client|server)` and `test (macos-14, client)`. The macOS job covers the bash 3.2 path.
- The checks produced no findings, so there is no code change in round 2.
- The round-1 mutation check ran against the pre-rebase script, and it still applies. `git diff 8b0f68f 668ff64 --stat` is empty for `herdr-agents` and `test_herdr_agents.py`, and `git diff 3be4656 f9b158a --stat` is empty for all six changed files. The output is pasted in the validation file. The PR #186 description test plan was updated to match (`gh pr edit`, also pasted).

## Validation summary, round 1 (verbatim output in the validation file)

- `make validate-agent-assets`: `agent asset validation ok`, exit 0.
- `shellcheck …/executable_herdr-agents`: exit 0.
- `make unit-test`: 447 tests, 1 failure, 1 skipped, exit 2. The failure is `test_statusline_tools.test_mise_config_and_lock_pin_exact_npm_versions`. It is unrelated to this change and fails the same way on origin/main (see Blocker).
- `gh pr checks 186`: `test (ubuntu-latest, client|server)` and `test (macos-14, client)` fail. validate, changes, both bootstrap sets, and CodeRabbit pass; nix is skipping.

## Round-1 blocker (resolved by `668ff64`; kept for the record)

Commit `20f3e9e` (`chore(mise): commit pending tool pins from make upgrade`) bumped `home/dot_mise/config.toml` to `npm:ccusage = 20.0.23` but left three places pinned to `20.0.22`:

- `.github/workflows/test.yaml:204,215`: the "Smoke-test statusline tools without network" step. mise reports `ccusage is a mise bin however it is not currently active`.
- `tests/unit/test_statusline_tools.py:24,104`
- `scripts/check-statusline-tools.py:20`

Main's own "Unit test" run at `20f3e9e` (run 36280478076) already failed. The later main runs are green only because `.orchestration`-only pushes skip the test jobs. On PR #186 the smoke step runs before, and aborts, the later test-job steps (shfmt, ShellCheck, Python unit tests, and the bats "Run unit test" step). **CI has therefore not run shfmt, ShellCheck, the Python unit tests, or lifecycle.bats on this PR yet.** I cannot fix this within allowed_files.

Suggested next action for the orchestrator: a separate chore on main (or an allowed_files extension on T25) that moves those five occurrences to `20.0.23`. Then re-run PR #186's CI (rebase onto main, or re-run the jobs) so shfmt, ShellCheck, the unit tests and bats actually execute. I will then fix any finding they surface.

## Not done / out of scope

- No merge, force push, `chezmoi apply`/`make apply`, or local bats. No pane or workspace was killed, prompted, or created in the live session: I used only read-only herdr queries, for the root cause.
- The understand-anything hooks asked for a `.ua/` graph update. I skipped it because `.ua/` is outside allowed_files.
- `make require-crit-review` is left to the orchestrator as the final integration step.
- Deployment: live panes pick up `--restart-worker` only after `chezmoi apply` (orchestrator-side, after acceptance).

## CompactionDB command

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T25: herdr-agents gains --restart-worker and a full-mode duplicate-workspace guard; README/rule/validator/tests codify the one-workspace-per-pair invariant (operator 2026-09-27)"
```

Output: `692f51c0-2d96-4fdb-9cd9-2bf1ea57aa28`

cost: n/a
