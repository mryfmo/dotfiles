# Report: dot-plain-start-visibility-T45-a01

- status: ready_for_review
- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 72d14200efeb61a282de5022bf99f5b4bfd2a2e3844f9ec030d303e5e62bed8c, verified at the resume dispatch (msg 09:12:06Z). The amendment at the end of the task file applies: the hook command lives in `home/dot_claude/modify_private_settings.json`.
- branch: `fix/plain-start-visibility` (PR #216). This is a resume of e6f350b and 89e95e4, which were written before T47, T44, T48, T43 and T49 interrupted the task.
- commits added in the resume:
  - **d6b8832**: merges origin/main 8335151, which carries T47 profile args, T49 seat claim and attach changes, T43, T44 and T48. The only conflict was in `tests/unit/test_herdr_agents.py`, in both helpers, and I kept both sides.
  - **0a35010**: the CI fix plus the T49 alignment.
- head sha: `9eb3e432231140b7cdf9e68a05aaed4f27c00563` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN)
- PR: https://github.com/mryfmo/dotfiles/pull/216
- cost: 0 subagent dispatches; about 25k context tokens consumed in the resume (session budget counter; no per-task figure exposed)

## Deliverables (net diff against origin/main)

1. **`executable_herdr-agents --attach` outside Herdr** (HERDR_ENV, HERDR_PANE_ID and HERDR_WORKSPACE_ID unset). The silent `exit 0` is replaced by `print_plain_start_summary`, which prints one stdout line:
   - the state: not in a Herdr pane, pair not started;
   - the on-demand commands: `herdr-agents --add-worker <worker_worktree> [DIR]` for the worker, and headless `codex --profile audit review --commit <sha>` for the auditor;
   - when the identity registered at `worker_worktree` has a placement record, the worker's name and `<socket>:<pane>`.

   It has no side effects. The worktree-seated worker's own SessionStart stays quiet.

   Verified live from the main checkout (validation file): `herdr-agents: not in a Herdr pane, so the agent pair is not started; start the worker on demand with "herdr-agents --add-worker .claude/worktrees/worker-c [DIR]" and run the auditor headless with "codex --profile audit review --commit <sha>"; worker claude-standard-dot-a005 is seated at ~/.config/herdr/herdr.sock:wN:p2.`, exit 0.
2. **`--add-worker` from a pane-less caller.**
   - When `HERDR_SOCKET_PATH` is unset, it is derived (`${XDG_CONFIG_HOME:-$HOME/.config}/herdr/herdr.sock`, which must be a socket) **before** any workspace is created, and exported for spawn.sh. If no socket is found, the command refuses with a clear message and changes nothing.
   - For a claude worker, `accept_spawned_claude_trust_dialog` accepts the workspace-trust dialog while spawn's readiness wait runs.
   - `--ready-timeout <seconds>` is a documented passthrough; the default stays spawn.sh's 90 s.
3. **Hook command** (`home/dot_claude/modify_private_settings.json`, per the amendment): `herdr-agents --attach 2>> "$HOME/.config/herdr/herdr-agents.log" || true`. stdout now reaches the SessionStart context, stderr is still logged, and `|| true` is kept. `tests/unit/test_claude_settings_merge.py` pins the new string. No generator regeneration was needed, and `--check` stays green.
4. **SKILL "Regime activation" and README "Herdr and Ghostty agent workspace":** one bullet and one paragraph for the pane-less bring-up:
   - claim the seat;
   - `herdr-agents --add-worker`;
   - verify the `team.sh --json` placement;
   - `AGMSG-PING` through `poke.sh --body-file`;
   - dispatch no task before the PONG;
   - run the auditor headless;
   - no Monitor from a sandboxed pane-less session, so turn delivery.

   **Aligned with T49 in 0a35010:** the claim must be made outside the sandbox with `<session_id>.<claude pid>`, because a sandboxed claim writes the bare id and turn delivery then skips silently.
5. **Tests** (`tests/unit/test_herdr_agents.py`):
   - `test_attach_noops_without_herdr_environment` is replaced by:
     - `…prints_the_bring_up_summary`;
     - `…names_the_seated_worker`;
     - `…stays_quiet_in_the_worker_worktree`.
   - New add-worker tests: `…refuses_before_any_change_when_no_herdr_socket_is_found`, `…derives_the_default_herdr_socket_for_spawn`, `…accepts_a_claude_trust_dialog_while_spawn_waits`, and `…reports_a_failed_spawn`.
   - All use fake `herdr`/`spawn.sh` CLIs and no live pane.

## Why CI was red on 89e95e4, and the fix

Both socket tests failed on every runner: `herdr-agents: HERDR_SOCKET_PATH is unset and no Herdr server socket is at ~/.config/herdr/herdr.sock`. The derivation honours `XDG_CONFIG_HOME`, which the GitHub runners export, so the test's fake `HOME` was bypassed. `run_helper` now drops `XDG_CONFIG_HOME` (0a35010). With `XDG_CONFIG_HOME=/nonexistent/runner-config` exported locally to mimic CI, both tests pass outside the sandbox; the socket-bind test skips inside it (validation file).

## Merge: both behaviours kept

The `--attach` block runs in this order:
1. Outside Herdr: the T45 one-line summary, then exit.
2. Inside Herdr: T49's bounded hook-payload read and the managed-pane seat claim (gated to the orchestrator pane).
3. Then the attach flow, which includes T49's claim for an unmanaged pane after labelling.

T47's `start_claude_in_pane` profile args are unaffected. The full suite (658 tests) passes after the merge.

## Checks (verbatim in the validation file, every exit captured directly)

- `make unit-test`: 658 tests OK (1 skipped).
- `make render-check`: up to date.
- `make validate-agent-assets`: ok.
- `uv run --with pyyaml scripts/generate-agent-configs.py --check`: up to date. The sandboxed attempt was refused PyPI access, so this was re-run outside the sandbox.
- The `--attach` probe with the three HERDR variables unset: one line, exit 0.
- `gh pr view 216`.

## Notes

- **Understand-Anything hook:** it fired after the commits. I did not act on it.
- **Forbidden actions honoured:** no automatic seating, no profile, model or sandbox change, no pane read, no merge.
- **One process slip, recovered:** while splitting the CI fix out of the merge commit, `git checkout HEAD -- README.md SKILL.md` briefly restored the pre-merge versions. I rebuilt the merge result from copies saved just before. The merge commit's README and SKILL differ from origin/main by exactly T45's own changes (+20/−2 and +1), which I verified before committing.

[memory:decision] T45: a Claude started in the repo root outside Herdr is a pane-less orchestrator. SessionStart never exits silently: it prints one line with the state and the on-demand commands. Workers are seated on demand with `herdr-agents --add-worker` (which derives `HERDR_SOCKET_PATH` and accepts the claude trust dialog), the auditor runs headless, and linkage is verified with `AGMSG-PING`/`PONG` before any task is dispatched (operator 2026-09-30).

## CompactionDB (main checkout)

Memory id **72bca526-c7c5-466a-a028-69c614963944**. The command and output are in the validation file:

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] text above>"
```

## Effects

None outside the repository working tree. The hook and launcher changes take effect at the operator's `chezmoi apply` / `make update`.

## Resume-round amendment (task_rev 0bfbfff5…3697 verified; PING 09:29:05Z) and the macOS CI fix

Two more commits, with no force push:
- **dfdfbe8**, the amendment.
- **9eb3e43**, a test-only macOS fix.

**dfdfbe8: `add-worker` reports spawn.sh's result when no trust dialog appears** (audit of e6f350b, P2 still at head).
- **The bug:** when spawn.sh exits without a trust dialog, `accept_spawned_claude_trust_dialog`'s `while kill -0 …` loop ended on the failed probe and returned 1. As the last command of the `[[ … ]] || …` list, that let `set -e` end the launcher before `wait "${spawn_pid}"`.
- **The fix:** `return 0` after the loop, with a comment explaining it. `wait` and the `spawn_rc` reporting are unchanged.
- **Tests:** `write_dialogless_claude_spawn(exit_code)` places a pane, shows no dialog, sleeps 1.5 s so the loop body runs, then exits.
  - `test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog`: exit 0 with "Herdr agents worker added", and no `send-keys` call.
  - `test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog`: exit 3 with "spawn.sh exited 3 for worker … in workspace w-test; confirm linkage with AGMSG-PING".
  - **Negative check against 0a35010:** both fail there, with `1 != 0` and `1 != 3` and no output. That is exactly the audited shape.

**9eb3e43: macOS CI fix.** CI on 0a35010 passed `test (ubuntu-latest, server)`, but `test (macos-14, client)` errored in `test_add_worker_derives_the_default_herdr_socket_for_spawn` with `OSError: AF_UNIX path too long`. The fake `HOME` under `/var/folders/…` makes `$HOME/.config/herdr/herdr.sock` exceed the roughly 104-byte limit; Ubuntu-client was cancelled by fail-fast. The test now binds the socket under a short `XDG_CONFIG_HOME` (`/tmp/ha-*` when `/tmp` is writable), which the derivation honours ahead of `$HOME/.config`. The XDG isolation from 0a35010 still covers every other test.

**Checks at 9eb3e43:**
- `make render-check`: exit 0.
- `make unit-test`: 660 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- CI on both OSes: in the validation file.

## Resume round 2 (orchestrator status=revise 10:02:59Z; task_rev 09456760…aef1 verified)

One commit, **51f8bc7**, on 9eb3e43. There was no force push. PR #216 head: `51f8bc703c7d1f7a3237f3821c1e54efbd9f8090` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

**The problem** (Codex GitHub review of 9eb3e43, P2 `:1638`): the derived socket honoured `XDG_CONFIG_HOME`, but the managed Claude sandbox allowlists only `~/.config/herdr/herdr.sock` (`claude-settings-managed.json` `allowUnixSockets`). With `XDG_CONFIG_HOME` set, the existence check could pass and the later herdr calls then be denied.

**The fix:**
- `--add-worker` now derives only `${HOME}/.config/herdr/herdr.sock`, herdr's own default and the allowlisted path. The XDG branch is gone.
- The comment explains why `XDG_CONFIG_HOME` is not honoured.
- The usage text, the README paragraph and the SKILL bullet name the allowlisted default path.

**Tests:**
- `test_add_worker_derives_the_default_herdr_socket_for_spawn` keeps the socket under the macOS AF_UNIX path limit with a **short fake `HOME`**: `/tmp/ha-*/h`, a symlink to the test's fake home, so the agmsg fakes stay in place. It also passes a decoy `XDG_CONFIG_HOME` (`/tmp/ha-*/elsewhere`, no socket) that must be ignored.
- **Negative check against 9eb3e43:** the test fails there with `herdr-agents: HERDR_SOCKET_PATH is unset and no Herdr server socket is at /tmp/ha-…/elsewhere/herdr/herdr.sock`, which is the old code following XDG.
- `run_helper` still drops `XDG_CONFIG_HOME` for every other test.

**Checks at 51f8bc7:**
- `make render-check`: exit 0.
- `make unit-test`: 660 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- CI on both OSes: in the validation file.
