# AGMSG-TASK dotfiles-T75-shell-dead-code-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 4, dotfiles-T75). Queued for the next free worker; its files are disjoint from T65 (stop gate), T66 (permgate), T67 (herdr-agents/README audit section), T88 (rule/SKILL/docs test).

## Objective

Principle 9: delete shell code and configuration that never runs or runs twice. Each item below was verified by the orchestrator's exploration (references counted excluding `.orchestration/`, `.ua/`, `.claude/worktrees/`, `reviews/`, `vendor/`); re-verify before deleting and report any reference you find.

1. `home/dot_config/alias/client.sh` (comments only) and `alias/server.sh` (one comment): delete, and drop their sheldon entries (`home/dot_config/sheldon/plugin_sources/client/common.toml:38-41`, `server.toml:33-36`).
2. `home/dot_local/bin/server/history.sh` and `cache.sh`: sourced only from `home/dot_bash/client/bashrc:128-130, 148-150`, but deployed only on servers (chezmoiignore) whose bashrc only `exec zsh`, so they never run. Delete both and the sourcing lines.
3. `home/dot_local/bin/common/executable_setup-python-env` (0 references): delete.
4. `home/dot_config/tango.yml` (only `tests/files/common.bats:8`): delete file and test line.
5. `home/dot_config/git/ignore:4-5` (`*hoge*`, `*fuga*`): delete.
6. Duplicate `mise activate zsh` in `home/dot_config/sheldon/plugin_sources/common.toml:121-123`: delete (keep `dot_zshrc:9-11` and `dot_zprofile:26 --shims`); a login zsh must activate mise once.
7. `home/dot_config/zsh/plugins/chezmoi-notify/` (not referenced by any sheldon toml; the p10k segment covers the client): delete.
8. `home/dot_local/bin/common/executable_dev:25-31` (tmux branch): delete only if `grep -rn tmux home` finds no other tmux use (VERIFY; keep lines 34-35, the autoload self-call).

Keep: `prompt.sh`/`aliases.sh` sourcing lines (private-layer files, `test_runtime_health.py:74-86`), `dot_profile:2`.

[memory:decision] dotfiles-T75 (operator 2026-10-03): dead shell files (empty alias files, never-sourced history/cache, setup-python-env, tango.yml, chezmoi-notify, hoge/fuga ignores, the duplicate sheldon mise activation, the dev tmux branch) are deleted; a login zsh activates mise once.

## Repo / branch

- Work ONLY in your own worktree (worker-c for a005). `git fetch origin`; `git switch -c chore/shell-dead-code origin/main` (40d9eb6c or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- the files named above and their sheldon/bashrc/test references; `tests/files/common.bats`; any `tests/files/*.bats` or unit test that pins a deleted path (name it)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T75-shell-dead-code-a01.md` (main checkout)

## Forbidden actions

- Anything under `home/dot_agents`, `home/dot_claude`, `home/dot_codex`, `home/dot_local/bin/common/executable_herdr-agents`, `scripts/`, `README.md`; `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
git ls-files | grep -E 'alias/(client|server)\.sh|server/(history|cache)\.sh|setup-python-env|tango\.yml|chezmoi-notify'; echo "exit=$?"   # expect no matches
grep -c "hoge\|fuga" home/dot_config/git/ignore                                  # 0
grep -rn "activate zsh" home | grep -vc shims                                     # 1
grep -rn "history.sh\|cache.sh\|tango\|chezmoi-notify\|setup-python-env" home tests; echo "exit=$?"   # expect no matches
make unit-test
make validate-agent-assets
gh pr checks <pr-number>        # tests/files bats run in CI
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

Live acceptance (operator, after merge and `make update`, both hosts): `zsh -lic 'echo $PATH' | tr : '\n' | grep -c mise/shims` → 1.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings and repeat; close your crit server if Plan Mode opened one; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## Revise round 1 (2026-10-04T02:08Z RESULT on fa5f5a3f)

1. **Codex P2 4175747919 (deployed targets stay on existing machines):** valid; fix at the root in this PR. `home/.chezmoiremove` is added to the allowed files: list the retired targets `.config/alias/client.sh`, `.config/alias/server.sh`, `.config/tango.yml`, `.local/bin/common/setup-python-env`, `.local/bin/server/history.sh`, `.local/bin/server/cache.sh` (the file already retires `start-cognee-mcp` and the ccgate files this way). Check whether `tests/files/*.bats` or a unit test pins `.chezmoiremove` content and update it.
2. **Item 7 (`chezmoi-notify`):** your re-verification stands; `server.toml` loads it, so it stays. The decision text is amended at acceptance.
3. One commit; push; wait for the Codex review of the new head; new RESULT; do not resolve threads.
