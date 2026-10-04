# Report: dotfiles-T75-shell-dead-code-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `chore/shell-dead-code` from `origin/main` 40d9eb6c.
- **task_rev:** `d182a15e…`, matched.
- **PR:** #244, https://github.com/mryfmo/dotfiles/pull/244.
- **Commits:**
  - `ef5742f9`: the change.
  - `fa5f5a3f`: `gh pr update-branch` with `main` 57885db1 (T67).
- **Final head:** `fa5f5a3f`.
  - **CI:** green; 13 pass including CodeRabbit (the `tests/files` bats run in CI), and `nix` is skipped.
  - **Branch:** up to date with `main` 57885db1 (behind_by=0).
  - **Codex:** `bot: none` on the merge head within 15 minutes; one P2 on `ef5742f9`.
  - **`mergeable_state`:** `blocked`, only by that unresolved P2 thread 4175747919.

## Done (items 1–6, 8)

1. **Alias files:** `alias/client.sh` and `alias/server.sh` are deleted, with their `[plugins.alias]` blocks in sheldon `client/common.toml` and `server.toml`. `alias/common.sh` stays.
2. **`server/history.sh` and `server/cache.sh`:** deleted, with their sourcing lines in `home/dot_bash/client/bashrc`.
   - Deploy scope verified: `.local/bin/server` exists only on ubuntu servers, and there `.bashrc` is `dot_bash/server/bashrc`, which only runs `exec zsh`.
   - The `prompt.sh`, `aliases.sh` and `secrets.sh` sourcing lines are kept, as is `dot_profile:2`.
3. **`executable_setup-python-env`:** deleted (no references).
4. **`dot_config/tango.yml`:** deleted, with its `tests/files/common.bats` line.
5. **Git ignore:** the `*hoge*` and `*fuga*` patterns are deleted from `home/dot_config/git/ignore`.
6. **mise:** the `[plugins.mise]` block is deleted from sheldon `common.toml`. `dot_zshrc:10` activates mise before `sheldon source` (`:39`), and `dot_zprofile:26 --shims` stays. `grep -rn "activate zsh" home | grep -vc shims` returns 1.
8. **`dev`:** the tmux branch is deleted after `grep -rn tmux home` found only the dev script itself. The `@description` texts drop the tmux mention, and the autoload self-call stays.

**Test pins changed:**
- **`tests/files/ubuntu.bats`:** the ubuntu-server representative manifest, the idempotent-apply targets and the removed-target case move from `server/cache.sh` to `server/ssh_agent.sh`, which is still deployed on servers and sourced by sheldon. So does the ubuntu-client `assert_absent`.
- **`tests/files/macos.bats`:** its `assert_absent` moves the same way.
- **`tests/unit/test_runtime_health.py`:** no longer creates the two deleted fixture files.
- **Other names:** nothing else in `tests/`, `scripts/` or `.github/` names a deleted path.

## Not done, with reasons (for the orchestrator)

- **Item 7, `zsh/plugins/chezmoi-notify/`: NOT deleted.** The task says it is "not referenced by any sheldon toml", but `home/dot_config/sheldon/plugin_sources/server.toml:52-53` (`:43-44` after this change) loads it as `[plugins.chezmoi-notify]`. It is live on servers, and the p10k segment covers only clients. Deleting it would remove a running server feature, so I re-verified and kept it, as the task's "re-verify before deleting and report any reference" asks. Consequences:
  - `git ls-files | grep …` and the `grep -rn … chezmoi-notify` validation still match that file.
  - If you still want it gone, the server sheldon entry must go with it.
  - The CompactionDB decision text is the task's verbatim, so it still lists chezmoi-notify as deleted.
- **Codex P2 "Retire deployed files through chezmoiremove" (comment 4175747919, on `ef5742f9`): not changed. Proposed as a follow-up.**
  - Deleting the source leaves the deployed targets on existing machines: `~/.local/bin/common/setup-python-env` stays runnable, and `~/.config/alias/{client,server}.sh`, `~/.config/tango.yml` and the servers' `~/.local/bin/server/{history,cache}.sh` remain.
  - `home/.chezmoiremove` is outside this task's allowed files, so I did not edit it. The PR body carries the same operator note.
  - Proposed follow-up: list those five targets in `home/.chezmoiremove`. That file already retires `start-cognee-mcp` and the ccgate files the same way.

## Findings

- **`make validate-agent-assets` currently fails in the main checkout:** `ERROR: possible committed secret in .orchestration/validation/dotfiles-T67-audit-task-level-a01-review-receipt.md`.
  - That file is an untracked orchestrator review receipt for T67, written 10:48 local. It is not part of this change, and I did not open or edit it.
  - It will trip the boundary commit's `make validate-agent-assets` until it is masked or fixed.
- **`grep … history.sh` false positives:** the regex also matches `zsh-history-shell-options` (`.` matches `-`) and agmsg's own `scripts/history.sh` in `tests/unit/test_check_agent_runtime.py`. Neither is related to this change.
- **Live acceptance (operator, after merge and `make update`):** `zsh -lic 'echo $PATH' | tr : '\n' | grep -c mise/shims` → 1, as the task states.

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T75 (operator 2026-10-03): dead shell files (empty alias files, never-sourced history/cache, setup-python-env, tango.yml, chezmoi-notify, hoge/fuga ignores, the duplicate sheldon mise activation, the dev tmux branch) are deleted; a login zsh activates mise once.'
cf4744c8-9c09-42e6-a47f-7b44b2134329
```

[memory:decision] dotfiles-T75 (operator 2026-10-03): dead shell files (empty alias files, never-sourced history/cache, setup-python-env, tango.yml, chezmoi-notify, hoge/fuga ignores, the duplicate sheldon mise activation, the dev tmux branch) are deleted; a login zsh activates mise once.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T75-shell-dead-code-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T75-shell-dead-code-a01.md`
- learning: `.orchestration/learning/dotfiles-T75-shell-dead-code-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T75-shell-dead-code-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).

## Revise round 1 (task_rev `4a14d05c…`): commit `339c1496`

1. **Codex P2 4175747919, fixed at the root:** `home/.chezmoiremove` now retires the six deleted targets:
   - `.config/alias/client.sh`
   - `.config/alias/server.sh`
   - `.config/tango.yml`
   - `.local/bin/common/setup-python-env`
   - `.local/bin/server/history.sh`
   - `.local/bin/server/cache.sh`

   Content pins: no test pinned `.chezmoiremove` content in a way the additions break.
   - `tests/install/common/lifecycle.bats:448` greps the ccgate entry.
   - `tests/unit/test_validate_agent_assets.py` writes its own fixture file.
   - `validate-agent-assets.py` requires only the agmsg entry and refuses installer-owned paths; none of the new entries is one.

   New test `ChezmoiRemoveRetiredShellFilesTest` in `tests/unit/test_chezmoiremove_agmsg.py`: each of the six targets is listed and has no remaining source under `home/`. It fails on all six with the `origin/main` file. The existing `chezmoi apply` test passes with the extended file. A scratch `chezmoi apply` removed exactly the six files and kept `alias/common.sh`, `common/dev` and `server/ssh_agent.sh`. 727 tests OK.
2. **`chezmoi-notify`:** stays (the decision text is amended at acceptance).
3. One commit; final head `339c1496`.
   - **CI:** green (13 pass, `nix` skipped).
   - **Branch:** up to date with `main` 57885db1.
   - **Codex:** 👍 at 02:19:14Z with no new thread.
   - **`mergeable_state`:** `blocked`, only by the P2 thread 4175747919, which is now fixed and left for the orchestrator.
