# Validation: dotfiles-T75-shell-dead-code-a01

- **task_rev:** `sha256:d182a15ee3cbd922cad9b36fe914b2c04babd50dffd11e3d2db5415045af1b1b`. `sha256sum` of the task file in the main checkout matches.
- **Branch:** `chore/shell-dead-code` from `origin/main` 40d9eb6c.
- **PR:** #244, https://github.com/mryfmo/dotfiles/pull/244.
- **Commits:**
  - `ef5742f9`: the change.
  - `fa5f5a3f`: `gh pr update-branch` merge of `main` 57885db1 (T67).
- **Final head:** `fa5f5a3feebec477836d317ea1a70c33af49e0ea`.

## Re-verification before deleting (repo-wide `git grep -F`, excluding .orchestration, .ua, reviews, vendor; on 40d9eb6c)

```
## alias/client.sh / alias/server.sh       -> no path reference; sheldon client/common.toml:40 use = ['client.sh'], server.toml use = ['server.sh']
## history.sh  -> home/dot_bash/client/bashrc:129-130 (sourcing); tests/unit/test_runtime_health.py:57 (fixture); tests/unit/test_check_agent_runtime.py (agmsg's own scripts/history.sh, unrelated)
## cache.sh    -> home/dot_bash/client/bashrc:149-150; tests/files/macos.bats:21; tests/files/ubuntu.bats:23,57,67,74-82; tests/unit/test_runtime_health.py:58
## setup-python-env -> only the file itself
## tango       -> tests/files/common.bats:8
## hoge / fuga -> home/dot_config/git/ignore:4-5
## chezmoi-notify -> home/dot_config/sheldon/plugin_sources/server.toml:52-53 [plugins.chezmoi-notify]   <-- LIVE on servers; NOT deleted
## activate zsh -> sheldon common.toml:123 (duplicate), dot_zprofile:26 (--shims), dot_zshrc:10 (before `sheldon source` at :39)
$ grep -rn tmux home
home/dot_local/bin/common/executable_dev:7,19,25,30 (only the dev script itself)
```

Deploy scope (`home/.chezmoitemplates/chezmoiignore.d`):
- `.local/bin/server` is ignored on macos and ubuntu/client, so it is deployed only on ubuntu servers.
- `.bash/client/bashrc` is ignored on ubuntu/server.
- `home/dot_bash/server/bashrc` runs `command -v zsh > /dev/null && exec zsh` (for a non-dumb TERM) and sources nothing.
- So the client bashrc's `server/history.sh` and `server/cache.sh` sourcing never finds the files, and on servers no zsh or sheldon config sources them.

## Validation commands (verbatim, on the final head; unit tests run in the Claude sandbox)

```
$ git log -1 --format=%H
fa5f5a3feebec477836d317ea1a70c33af49e0ea
$ git diff origin/main --stat
 home/dot_bash/client/bashrc                        |  7 -----
 home/dot_config/alias/client.sh                    | 10 --------
 home/dot_config/alias/server.sh                    |  4 ---
 home/dot_config/git/ignore                         |  2 --
 .../sheldon/plugin_sources/client/common.toml      |  9 -------
 home/dot_config/sheldon/plugin_sources/common.toml |  7 -----
 home/dot_config/sheldon/plugin_sources/server.toml |  9 -------
 home/dot_config/tango.yml                          |  7 -----
 home/dot_local/bin/common/executable_dev           | 13 ++--------
 .../bin/common/executable_setup-python-env         | 30 ----------------------
 home/dot_local/bin/server/cache.sh                 | 13 ----------
 home/dot_local/bin/server/history.sh               | 27 -------------------
 tests/files/common.bats                            |  1 -
 tests/files/macos.bats                             |  2 +-
 tests/files/ubuntu.bats                            | 14 +++++-----
 tests/unit/test_runtime_health.py                  |  2 --
 16 files changed, 10 insertions(+), 147 deletions(-)
$ git ls-files | grep -E 'alias/(client|server)\.sh|server/(history|cache)\.sh|setup-python-env|tango\.yml|chezmoi-notify'; echo "exit=$?"
home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh
exit=0
$ grep -c "hoge\|fuga" home/dot_config/git/ignore
0
$ grep -rn "activate zsh" home | grep -vc shims
1
$ grep -rn "history.sh\|cache.sh\|tango\|chezmoi-notify\|setup-python-env" home tests; echo "exit=$?"
home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh:4:# chezmoi-notify: Asynchronous update check plugin for chezmoi for Starship
home/dot_config/sheldon/plugin_sources/server.toml:43:[plugins.chezmoi-notify]
home/dot_config/sheldon/plugin_sources/server.toml:44:local = "~/.config/zsh/plugins/chezmoi-notify"
home/dot_config/sheldon/plugin_sources/common.toml:112:[plugins.zsh-history-shell-options]
tests/unit/test_check_agent_runtime.py:499:            "shared skill directory is missing files: agmsg/scripts/history.sh",
tests/unit/test_check_agent_runtime.py:514:        source = source_root / "dot_agents/skills/agmsg/scripts/executable_history.sh"
tests/unit/test_check_agent_runtime.py:520:        target = home / ".agents/skills/agmsg/scripts/history.sh"
tests/unit/test_check_agent_runtime.py:551:                {Path("agmsg/scripts/history.sh"): source.read_text()},
tests/unit/test_check_agent_runtime.py:553:                {Path("agmsg/scripts/history.sh"): source},
exit=0
$ make unit-test (tail -3)
Ran 726 tests in 163.218s

OK (skipped=2)
```

Expected-vs-actual for the task's checks:
- **`git ls-files | grep …`:** expected no matches, got one: `chezmoi-notify.plugin.zsh`, deliberately kept (it is live on servers through `server.toml:43-44`).
- **`grep -rn "history.sh\|cache.sh\|tango\|chezmoi-notify\|setup-python-env" home tests`:** expected no matches, got only three groups:
  - the kept `chezmoi-notify` plugin and its `server.toml` entry;
  - `zsh-history-shell-options`, a regex false positive (`.` matches `-`);
  - agmsg's own `scripts/history.sh` in `tests/unit/test_check_agent_runtime.py`, unrelated.

## Lint of the edited shell files

```
$ shellcheck home/dot_bash/client/bashrc   (gcc format, line numbers dropped, origin/main vs branch)
before=10 after=8
--- only before:
home/dot_bash/client/bashrc: note: Not following: ../../dot_local/bin/server/cache.sh was not specified as input (see shellcheck -x). [SC1091]
home/dot_bash/client/bashrc: note: Not following: ../../dot_local/bin/server/history.sh was not specified as input (see shellcheck -x). [SC1091]
--- only after:
$ mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_dev home/dot_bash/client/bashrc
shfmt=0
```

## make validate-agent-assets (run in the main checkout, which is on main): FAILS on an orchestrator file, not on this change

```
$ make validate-agent-assets; echo exit=$?
uv run --with pyyaml scripts/validate-agent-assets.py
ERROR: possible committed secret in .orchestration/validation/dotfiles-T67-audit-task-level-a01-review-receipt.md
make: *** [Makefile:168: validate-agent-assets] エラー 1
vaa_exit=2
(untracked .orchestration WARN lines omitted)
```

The flagged file is untracked: 907 bytes, written 10:48 local, an orchestrator review receipt for T67. It is outside this task, and I did not open or edit it. Earlier in this session the same command passed (T67 validation, before that receipt existed).

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T75 (operator 2026-10-03): dead shell files (empty alias files, never-sourced history/cache, setup-python-env, tango.yml, chezmoi-notify, hoge/fuga ignores, the duplicate sheldon mise activation, the dev tmux branch) are deleted; a login zsh activates mise once.'
cf4744c8-9c09-42e6-a47f-7b44b2134329
```

## CI, mergeable_state, branch and Codex (final head `fa5f5a3f`)

```
$ gh pr checks 244
CodeRabbit	pass
changes	pass
nix	skipping
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
$ gh api repos/mryfmo/dotfiles/pulls/244 --jq '.mergeable_state'
blocked
$ gh api repos/mryfmo/dotfiles/compare/main...chore/shell-dead-code
behind_by=0 ahead_by=2
$ review comments on PR 244 (id, original commit, title)
4175747919 ef5742f9 **  Retire deployed files through chezmoiremove**
$ Codex on fa5f5a3f (pushed 2026-10-04T01:52:00Z): 60 polls x 15 s, no review and no +1 reaction
bot: none (merge head); ef5742f9: 1 P2 (above), not changed (see report)
```

`blocked` is only the unresolved Codex P2 thread 4175747919 (proposed follow-up, `.chezmoiremove` is outside allowed_files).

## Revise round 1 (task_rev `sha256:4a14d05c1fdf50ae3159a30c60770458660e261f2869f461c535a0f523781d4e`): head `339c1496`

```
$ git log -1 --format=%H
339c1496e8689c32e3a8cede1e36892165b746e1
$ git diff origin/main --stat
 home/.chezmoiremove                                |  6 +++++
 home/dot_bash/client/bashrc                        |  7 -----
 home/dot_config/alias/client.sh                    | 10 --------
 home/dot_config/alias/server.sh                    |  4 ---
 home/dot_config/git/ignore                         |  2 --
 .../sheldon/plugin_sources/client/common.toml      |  9 -------
 home/dot_config/sheldon/plugin_sources/common.toml |  7 -----
 home/dot_config/sheldon/plugin_sources/server.toml |  9 -------
 home/dot_config/tango.yml                          |  7 -----
 home/dot_local/bin/common/executable_dev           | 13 ++--------
 .../bin/common/executable_setup-python-env         | 30 ----------------------
 home/dot_local/bin/server/cache.sh                 | 13 ----------
 home/dot_local/bin/server/history.sh               | 27 -------------------
 tests/files/common.bats                            |  1 -
 tests/files/macos.bats                             |  2 +-
 tests/files/ubuntu.bats                            | 14 +++++-----
 tests/unit/test_chezmoiremove_agmsg.py             | 25 ++++++++++++++++++
 tests/unit/test_runtime_health.py                  |  2 --
 18 files changed, 41 insertions(+), 147 deletions(-)
$ cat home/.chezmoiremove
.codex/ccgate.jsonnet
.claude/ccgate.jsonnet
.local/bin/common/start-cognee-mcp
.claude/skills/agmsg/**
.config/alias/client.sh
.config/alias/server.sh
.config/tango.yml
.local/bin/common/setup-python-env
.local/bin/server/history.sh
.local/bin/server/cache.sh
$ grep -rn "chezmoiremove" tests  (content pins)
tests/install/common/lifecycle.bats:448:    grep -q '.codex/ccgate.jsonnet' home/.chezmoiremove
tests/unit/test_validate_agent_assets.py:398:        self.write_text_file("home/.chezmoiremove", ".claude/skills/agmsg/**\n")
tests/unit/test_validate_agent_assets.py:434:        self.write_text_file("home/.chezmoiremove", ".codex/ccgate.jsonnet\n")
tests/unit/test_validate_agent_assets.py:447:                self.write_text_file("home/.chezmoiremove", f".claude/skills/agmsg/**\n{pattern
tests/unit/test_chezmoiremove_agmsg.py:13:    """`chezmoi apply` with the repo's .chezmoiremove retires the stale agmsg symlink farm only.""
tests/unit/test_chezmoiremove_agmsg.py:21:            shutil.copy(ROOT / "home/.chezmoiremove", source / ".chezmoiremove")
tests/unit/test_chezmoiremove_agmsg.py:77:        entries = (ROOT / "home/.chezmoiremove").read_text().splitlines()
$ uv run python -m unittest -v tests.unit.test_chezmoiremove_agmsg
test_retired_targets_are_listed_and_have_no_source (tests.unit.test_chezmoiremove_agmsg.ChezmoiRemoveRetiredShellFilesTest.test_retired_targets_are_listed_and_have_no_source) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.024s

OK
$ (with home/.chezmoiremove from origin/main) uv run python -m unittest tests.unit.test_chezmoiremove_agmsg
FAIL: … (target=.config/alias/client.sh) / (.config/alias/server.sh) / (.config/tango.yml) / (.local/bin/common/setup-python-env) / (.local/bin/server/history.sh) / (.local/bin/server/cache.sh)
Ran 2 tests in 0.027s
FAILED (failures=6)
$ chezmoi --source <tmp src with the new .chezmoiremove> --destination <tmp home> apply --force; find <tmp home> -type f
(tmp home seeded with the six retired files plus .config/alias/common.sh, .local/bin/common/dev, .local/bin/server/ssh_agent.sh)
rc=0
./.config/alias/common.sh
./.local/bin/common/dev
./.local/bin/server/ssh_agent.sh
$ make unit-test (tail -3)
Ran 727 tests in 164.103s

OK (skipped=2)
```

## CI, mergeable_state, branch and Codex (revise-1 final head `339c1496`)

```
CodeRabbit	pass
changes	pass
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
validate	pass
nix	skipping
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
{
"baseRefOid": "57885db1d080325d78c444c386c58fc25646d22e",
"headRefOid": "339c1496e8689c32e3a8cede1e36892165b746e1",
"mergeStateStatus": "BLOCKED"
}
blocked
behind_by=0 ahead_by=3

$ Codex on 339c1496 (pushed 2026-10-04T02:16:38Z)
chatgpt-codex-connector[bot] +1 2026-10-04T02:19:14Z; no inline thread on this head
```

`blocked` is only the Codex P2 thread 4175747919 (fixed in `339c1496`), which is left for the orchestrator to resolve.
