# Acceptance: dotfiles-T75-shell-dead-code-a01

- **Decision:** ACCEPTED after one revise round. PR #244 squash-merged to `main` as `138e6a72` (final head `6ec1805319ba39892ae9bf0f4ac6e4c416137201`; substantive commits ef5742f9, 339c1496; base `40d9eb6c`, update-branch merges onto `57885db1`, `a5c30b6d`). Merged without `--delete-branch`; worker-c holds `chore/shell-dead-code`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `d182a15e…` → `4a14d05c…` (revise round 1); both matched. Parallel wave with T88 (a006) and T65 (a007).
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 4, dotfiles-T75 (principle 9: dead shell code).

## What was accepted

- Deleted: `alias/{client,server}.sh` with their sheldon blocks; `server/{history,cache}.sh` with their bashrc sourcing lines; `executable_setup-python-env`; `tango.yml` with its bats line; `*hoge*`/`*fuga*` git ignores; the duplicate `[plugins.mise]` activation in sheldon `common.toml` (login zsh activates mise once via `dot_zshrc`); the `dev` tmux branch.
- Revise round 1 (339c1496): `home/.chezmoiremove` retires the six deployed targets, with `ChezmoiRemoveRetiredShellFilesTest` pinning each entry and the absence of its source.
- Test pins moved from `server/cache.sh` to `server/ssh_agent.sh` (ubuntu/macos bats, runtime-health fixtures).

## Deviation accepted: chezmoi-notify kept

- The task listed `zsh/plugins/chezmoi-notify/` as unreferenced. The worker re-verified: sheldon `plugin_sources/server.toml` loads it as `[plugins.chezmoi-notify]`, so it is live on servers. Keeping it is correct; the task premise was wrong. The CompactionDB decision is amended below. Deleting it later needs the server sheldon entry removed in the same change.

## Orchestrator re-derivation

- Re-run by the orchestrator on `main` 138e6a72 after the merge: `git ls-files` matches none of the deleted paths except `chezmoi-notify`; each of the six `.chezmoiremove` entries appears once and has no source under `home/`; `grep -rn "activate zsh" home | grep -vc shims` → 1; `grep -c "hoge\|fuga" home/dot_config/git/ignore` → 0; `server.toml:43-44` still loads `chezmoi-notify`.
- Worker finding confirmed: the `grep … history.sh` acceptance regex also matches `zsh-history-shell-options` and agmsg's own `history.sh` in a unit test; neither is a dead-code reference.

## Audit / Bot / sweep / gate

| commit | verdict |
|---|---|
| ef5742f9 | incorrect: one P2 (deleted sources left deployed targets behind) → fixed at the root in 339c1496 |
| 339c1496 | correct (finding-free rationale recorded) |

- Codex Bot: P2 thread 4175747919 on ef5742f9 fixed in 339c1496, replied and resolved; thumbs-up on 339c1496 and on the final head 6ec18053 (02:35:42Z, pushed 02:32:22Z). Sweep (head 6ec18053): 9 items, 0 failure/warning, all dispositioned. Gate at 6ec18053 exit 0 with evidence copies, copies removed.
- The first merge attempt at fa5f5a3f/339c1496 was refused by the strict ruleset after T67/T66 landed; `gh pr update-branch` → CI → Bot → re-sweep → gate → merge.

## CompactionDB

- Worker decision `cf4744c8-9c09-42e6-a47f-7b44b2134329` (task verbatim, lists chezmoi-notify as deleted); amended by an orchestrator decision at acceptance: chezmoi-notify is kept because the server sheldon manifest loads it.

## Operator follow-up

- After `make update` on each host: `zsh -lic 'echo $PATH' | tr : '\n' | grep -c mise/shims` → 1; `chezmoi apply` removes the six retired targets.
- The validate-agent-assets secret-scan false positive the worker hit (T67 receipt file name matching `sk-…`) is T91, in flight at a005.
