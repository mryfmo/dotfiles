# Validation: dotfiles-T117-upgrade-outside-canonical-clone-a01

Worker `claude-standard-dot-a001`, worktree `.claude/worktrees/worker-c`, PR #308. Every block is verbatim command output; the head each block ran on is named in its heading.

## 0. Branch and head (final head 8e7a1866)

```
$ git log --oneline origin/main..HEAD; git rev-parse HEAD; git status --short
8e7a1866 docs(upgrade): seat the pins worker for the working clone and derive the update path
b2b7be60 fix(upgrade): follow the removed agmsg-bootstrap line and tighten pins prose
6000cfb4 feat(upgrade): run make upgrade in a pins worktree, never in the canonical clone
8e7a1866ecde41ef5726e3b74aa6864a91aee21b
```

## 1. shellcheck (8e7a1866)

```
$ shellcheck scripts/upgrade-tools.sh; echo "rc=$?"
rc=0
```

## 2. Scratch guard check (8e7a1866)

Script `scratchpad/t117-guard-check.sh` (passing cases source the script and call only `require_pins_checkout`; the canonical case runs the whole script with a PATH that has no package manager):

```bash
#!/usr/bin/env bash
# Scratch check of require_pins_checkout. Pass cases source the script and call
# only the guard, so no upgrade phase can run; the canonical case runs the
# script itself with a PATH that has no package managers.
set -u
src="$1"
s="$(mktemp -d "${TMPDIR:-/tmp}/t117-guard.XXXXXX")"
mkdir -p "$s/bin"
printf '#!/bin/sh\n[ "$1" = source-path ] && printf "%%s\\n" "$FAKE_SOURCE"\n' > "$s/bin/chezmoi"
chmod +x "$s/bin/chezmoi"
export PATH="$s/bin:/usr/bin:/bin" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
g() { git -c user.name=t -c user.email=t@t -C "$@"; }
mkrepo() {
    mkdir -p "$1/scripts" "$1/home"
    cp "$src" "$1/scripts/upgrade-tools.sh"
    printf 'pins\n' > "$1/tracked"
    g "$1" init -q && g "$1" add tracked && g "$1" commit -q -m base && g "$1" update-ref refs/remotes/origin/main HEAD
}
guard() { (cd "$1" && bash -c 'source scripts/upgrade-tools.sh; require_pins_checkout' 2>&1); echo "rc=$?"; }

mkrepo "$s/canon"
mkrepo "$s/other"
export FAKE_SOURCE="$s/canon/home"

echo "== 1 canonical clone, full script run"
(cd "$s/canon" && bash scripts/upgrade-tools.sh 2>&1); echo "rc=$?"
echo "== 2 canonical clone + CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 (guard only)"
CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 guard "$s/canon"
echo "== 3 other repo, clean at origin/main (guard only)"
guard "$s/other"
echo "== 4 other repo, untracked file only (guard only)"
touch "$s/other/untracked"
guard "$s/other"
echo "== 5 other repo, tracked edit (guard only)"
printf 'edited\n' > "$s/other/tracked"
guard "$s/other"
echo "== 6 other repo, tracked edit + override (guard only)"
CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 guard "$s/other"
g "$s/other" checkout -q -- tracked
echo "== 7 other repo, HEAD one commit past origin/main (guard only)"
g "$s/other" commit -q --allow-empty -m next
guard "$s/other"
echo "== 8 not a git checkout (guard only)"
mkdir -p "$s/plain/scripts" && cp "$src" "$s/plain/scripts/upgrade-tools.sh"
guard "$s/plain"
echo "== 9 chezmoi absent, other repo clean (guard only)"
rm "$s/bin/chezmoi"
g "$s/other" reset -q --hard origin/main
guard "$s/other"
rm -rf "$s"
```

Output:

```
== 1 canonical clone, full script run
make upgrade refused: /tmp/claude-501/t117-guard.nHfkP1/canon is the canonical chezmoi clone, which stays pull/apply only; run it in a pins worktree of the working clone (herdr-agents --add-worker .claude/worktrees/pins, then make -C <working clone>/.claude/worktrees/pins upgrade) and land the diff through a pull request
rc=2
== 2 canonical clone + CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 (guard only)
rc=0
== 3 other repo, clean at origin/main (guard only)
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
warning: git fetch origin main failed; comparing with the last-fetched origin/main
rc=0
== 4 other repo, untracked file only (guard only)
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
warning: git fetch origin main failed; comparing with the last-fetched origin/main
rc=0
== 5 other repo, tracked edit (guard only)
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
warning: git fetch origin main failed; comparing with the last-fetched origin/main
make upgrade refused: /tmp/claude-501/t117-guard.nHfkP1/other is dirty or behind origin/main; in the pins worktree run git switch -c <branch> --no-track origin/main (or git reset --hard origin/main on its own branch) first
rc=2
== 6 other repo, tracked edit + override (guard only)
rc=0
== 7 other repo, HEAD one commit past origin/main (guard only)
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
warning: git fetch origin main failed; comparing with the last-fetched origin/main
make upgrade refused: /tmp/claude-501/t117-guard.nHfkP1/other is dirty or behind origin/main; in the pins worktree run git switch -c <branch> --no-track origin/main (or git reset --hard origin/main on its own branch) first
rc=2
== 8 not a git checkout (guard only)
rc=0
== 9 chezmoi absent, other repo clean (guard only)
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
warning: git fetch origin main failed; comparing with the last-fetched origin/main
rc=0
```

## 3. mise probe in a scratch worktree (8e7a1866)

Sources the script in a detached scratch worktree and calls `mise trust --yes` (as line ~265 does), `run_mise_with_isolated_git_config ls --current` with `MISE_CONFIG_DIR` at that worktree's `home/dot_mise` (first 8 rows), and `apply_upgraded_mise_config`. The same probe ran first on b37937ca, before the guard existed; that output follows the rerun. The rerun reuses the trust record the first run wrote in the same `MISE_STATE_DIR`.

```
probe worktree: /tmp/claude-501/t117-probe (HEAD 8e7a1866)
MISE_STATE_DIR=/tmp/claude-501/t117-mise-state MISE_CACHE_DIR=/tmp/claude-501/t117-mise-cache
chezmoi source-path: ~/.local/share/chezmoi/home
MISE_CONFIG_DIR=/tmp/claude-501/t117-probe/home/dot_mise
mise WARN  No untrusted config files found.
trust rc=0
age                            1.3.2             /tmp/claude-501/t117-probe/home/dot_mise/config.toml  1.3.2
aqua:micro-editor/micro        2.0.15            /tmp/claude-501/t117-probe/home/dot_mise/config.toml  2.0.15
aqua:mikefarah/yq              4.54.1            /tmp/claude-501/t117-probe/home/dot_mise/config.toml  4.54.1
aqua:watchexec/watchexec       2.7.3             /tmp/claude-501/t117-probe/home/dot_mise/config.toml  2.7.3
bun                            1.4.2             /tmp/claude-501/t117-probe/home/dot_mise/config.toml  1.4.2
cargo:eza                      0.23.5            /tmp/claude-501/t117-probe/home/dot_mise/config.toml  0.23.5
cargo:pueue                    4.0.4             /tmp/claude-501/t117-probe/home/dot_mise/config.toml  4.0.4
chezmoi                        2.73.0            /tmp/claude-501/t117-probe/home/dot_mise/config.toml  2.73.0
ls rc=0
pins updated in /tmp/claude-501/t117-probe; ~/.config/mise follows after merge and make update
apply rc=0
probe worktree removed
```

First run, on b37937ca (same commands):

```
probe worktree: /tmp/claude-501/t117-probe (HEAD b37937ca)
MISE_STATE_DIR=/tmp/claude-501/t117-mise-state MISE_CACHE_DIR=/tmp/claude-501/t117-mise-cache
chezmoi source-path: ~/.local/share/chezmoi/home
MISE_CONFIG_DIR=/tmp/claude-501/t117-probe/home/dot_mise
mise trusted /private/tmp/claude-501/t117-probe
trust rc=0
age                            1.3.2             /tmp/claude-501/t117-probe/home/dot_mise/config.toml  1.3.2
aqua:micro-editor/micro        2.0.15            /tmp/claude-501/t117-probe/home/dot_mise/config.toml  2.0.15
aqua:mikefarah/yq              4.54.1            /tmp/claude-501/t117-probe/home/dot_mise/config.toml  4.54.1
aqua:watchexec/watchexec       2.7.3             /tmp/claude-501/t117-probe/home/dot_mise/config.toml  2.7.3
bun                            1.4.2             /tmp/claude-501/t117-probe/home/dot_mise/config.toml  1.4.2
cargo:eza                      0.23.5            /tmp/claude-501/t117-probe/home/dot_mise/config.toml  0.23.5
cargo:pueue                    4.0.4             /tmp/claude-501/t117-probe/home/dot_mise/config.toml  4.0.4
chezmoi                        2.73.0            /tmp/claude-501/t117-probe/home/dot_mise/config.toml  2.73.0
ls rc=0
pins updated in /tmp/claude-501/t117-probe; ~/.config/mise follows after merge and make update
apply rc=0
probe worktree removed
```

## 4. Upgrade unit tests (8e7a1866)

```
$ uv run python -m unittest tests.unit.test_runtime_health -k upgrade 2>&1 | tail -3
Ran 9 tests in 35.406s

FAILED (failures=2)
```

The two failures are sandbox-only and fail identically on origin/main b37937ca in this sandbox (from the full-suite logs of §6):

```
$ grep -E "^(FAIL|ERROR): test_upgrade" base.log; echo ---; grep -E "^(FAIL|ERROR): test_upgrade" final.log
FAIL: test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts)
FAIL: test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only)
---
FAIL: test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts)
FAIL: test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only)
```

## 5. Boundary-check and Makefile tests (8e7a1866)

These scratch-repo tests commit, which fails in this sandbox on both trees (signing key read-denied, git commit rc 128); hiding the user's global git config runs them as CI does:

```
$ GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest tests.unit.test_herdr_agents -k canonical -k agmsg_bootstrap 2>&1 | tail -3
Ran 11 tests in 11.012s

OK
```

## 6. Full unit suite

### 6a. Local, final head 8e7a1866 vs origin/main b37937ca, same sandbox

```
$ make unit-test 2>&1 | tail -3   # final head

FAILED (failures=119, errors=103, skipped=2)
make: *** [unit-test] Error 1
$ make unit-test 2>&1 | tail -3   # origin/main b37937ca in a scratch detached worktree

FAILED (failures=119, errors=103, skipped=2)
make: *** [unit-test] Error 1
$ comm -23 final.ids base.ids   # failing test ids only on the final head
$ comm -13 final.ids base.ids   # failing test ids only on origin/main
$ wc -l < final.ids; wc -l < base.ids
     193
     193
```

### 6b. First head 6000cfb4: one new failure, local and CI agree

```
$ comm -23 head.ids base.ids   # 6000cfb4 vs origin/main, local
FAIL: test_make_update_and_upgrade_include_agmsg_bootstrap
$ gh run view 37886882673 --log-failed | grep -E 'FAIL: |AssertionError: .make agmsg|Ran [0-9]+ tests|FAILED \('
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-09T05:08:46.3649260Z FAIL: test_make_update_and_upgrade_include_agmsg_bootstrap (test_herdr_agents.HerdrAgentsTest.test_make_update_and_upgrade_include_agmsg_bootstrap) (target='upgrade')
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-09T05:08:46.3659401Z AssertionError: 'make agmsg-bootstrap' not found in "make[1]: Entering directory '~/work/dotfiles/dotfiles'\n./scripts/upgrade-tools.sh \nmake[1]: Leaving directory '~/work/dotfiles/dotfiles'\n"
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-09T05:08:46.3660606Z Ran 880 tests in 168.176s
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-09T05:08:46.3660796Z FAILED (failures=1)
```

Fixed by Amendment 2 in b2b7be60 (test_make_update_includes_and_upgrade_excludes_agmsg_bootstrap); §5 runs it.

## 7. CompactionDB (main checkout, through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T117 (orchestrator 2026-10-09): `make upgrade` never runs in the canonical chezmoi clone (the script refuses, `CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1` overrides); the operator runs it in the pins worktree `.claude/worktrees/pins` seated with `herdr-agents --add-worker`, the worker there commits the changed files as the pins PR, and the canonical clone is pull and apply only, so its autostash never carries anything.'; echo "decision rc=$?"; uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dotfiles-T112/T114 (orchestrator 2026-10-09): running `make upgrade` in the canonical clone left an uncommitted pins diff whose `mise.lock` checksum lines differed from the carried PR; the next `git pull --rebase --autostash` conflicted and the clone needed a hand repair on 2026-10-09.'; echo "failure rc=$?"
ac3bdd3e-b1b0-4c5f-a394-37fc5e4fb71d
decision rc=0
f02c683a-798f-4279-a556-2a96dfcf931a
failure rc=0
```

## 8. CI on the final head 8e7a1866

```
$ gh pr checks 308
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37889179147/job/113685971728	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37889179138/job/113685971983	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37889179138/job/113685971908	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37889179138/job/113685971910	
public-bootstrap (macos-14, client)	pass	9m0s	https://github.com/mryfmo/dotfiles/actions/runs/37889179138/job/113685972010	
public-bootstrap (ubuntu-24.04, client)	pass	9m46s	https://github.com/mryfmo/dotfiles/actions/runs/37889179138/job/113685971779	
public-bootstrap (ubuntu-24.04, server)	pass	7m45s	https://github.com/mryfmo/dotfiles/actions/runs/37889179138/job/113685971591	
test (macos-14, client)	pass	5m24s	https://github.com/mryfmo/dotfiles/actions/runs/37889179147/job/113686012769	
test (ubuntu-24.04, client)	pass	7m38s	https://github.com/mryfmo/dotfiles/actions/runs/37889179147/job/113686012708	
test (ubuntu-24.04, server)	pass	4m11s	https://github.com/mryfmo/dotfiles/actions/runs/37889179147/job/113686012726	
test (ubuntu-26.04, client)	pass	8m0s	https://github.com/mryfmo/dotfiles/actions/runs/37889179147/job/113686012699	
validate	pass	1m30s	https://github.com/mryfmo/dotfiles/actions/runs/37889179144/job/113685971533	
```

## 9. Validator, render check, formatters (8e7a1866)

```
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-worker-review-receipt.md
WARN: regime-boundary: worker still seated at .claude/worktrees/worker-c (herdr-agents --remove-worker .claude/worktrees/worker-c)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a001 (herdr-agents --remove-worker)
agent asset validation ok
rc=0
$ make render-check; echo "rc=$?"
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
rc=0
$ mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/claude/rules/agmsg-orchestration.md 2>&1 | tail -2   # run via mise -C <empty dir> as CI does
Checking formatting...
All matched files use Prettier code style!
$ shfmt -i 4 -sr -d scripts/upgrade-tools.sh scripts/check-regime-boundary.sh; ruff format --config ruff.toml --check tests/unit/test_runtime_health.py tests/unit/test_herdr_agents.py   # via mise -C <empty dir>
shfmt rc=0
2 files already formatted
ruff rc=0
```

## 10. Codex Bot reviews and threads

All six threads are P2; none is P0/P1. Three were raised on 6000cfb4 and three on b2b7be60; the final diff head 8e7a1866 drew no Bot review within 15 minutes. Dispositions are in the report.

```
$ gh api --paginate repos/mryfmo/dotfiles/pulls/308/reviews --jq '.[]|select(.user.type=="Bot")|[.user.login,.commit_id,.submitted_at,.state]|@tsv'
chatgpt-codex-connector[bot]	6000cfb45da1df8caabfb12fdb92adad35f8b766	2026-10-09T05:12:41Z	COMMENTED
chatgpt-codex-connector[bot]	b2b7be60fe42c11c95240d0b16b4bad28031244e	2026-10-09T05:22:26Z	COMMENTED
$ gh api --paginate repos/mryfmo/dotfiles/pulls/308/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.original_commit_id,.path,(.line // .original_line // "-"),(.body|capture("(?<p>P[0-3]) Badge").p // "none"),(.body|capture("\*\*(?<t>[^*]+)\*\*").t // "")]|@tsv'
4226831987	6000cfb45da1df8caabfb12fdb92adad35f8b766	README.md	154	P2	<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Switch to the working clone before seating the pins worker
4226831998	6000cfb45da1df8caabfb12fdb92adad35f8b766	home/dot_agents/skills/agmsg-orchestration/SKILL.md	68	P2	<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Scope the acceptance comparison to upgrade-produced paths
4226832007	6000cfb45da1df8caabfb12fdb92adad35f8b766	scripts/upgrade-tools.sh	716	P2	<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Allow a failed upgrade to be resumed safely
4226889615	b2b7be60fe42c11c95240d0b16b4bad28031244e	scripts/upgrade-tools.sh	713	P2	<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Refuse upgrades when the origin fetch fails
4226889624	b2b7be60fe42c11c95240d0b16b4bad28031244e	README.md	167	P2	<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Resolve the configured source clone before updating
4226889631	b2b7be60fe42c11c95240d0b16b4bad28031244e	scripts/upgrade-tools.sh	704	P2	<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Fail closed when the canonical source cannot be resolved
$ bounded Bot wait on the final head 8e7a1866 (30 s interval, 15 min)
head committed 2026-10-09T05:33:39Z; deadline 05:48:39Z
bot: none (15 minutes after the final head)
comments: none

```

# Revise round 1 (head c6cd343f)

## R1.0 Branch and head

```
$ git log --oneline 8e7a1866..HEAD; git rev-parse HEAD; git status --short
c6cd343f fix(upgrade): refuse a failed fetch and an unresolvable chezmoi source
c6cd343f8eeae6f25dd9cccd30445b2a522d0605
```

## R1.1 shellcheck

```
$ shellcheck scripts/upgrade-tools.sh; echo "rc=$?"
rc=0
```

## R1.2 Scratch guard check

Updated script `scratchpad/t117-guard-check.sh`: every repo pushes to a local bare origin, so the fetch succeeds offline; passing cases still source the script and call only `require_pins_checkout`.

```bash
#!/usr/bin/env bash
# Scratch check of require_pins_checkout. Passing cases source the script and
# call only the guard, so no upgrade phase can run; the canonical case runs the
# script itself with a PATH that has no package managers. Each repo pushes to a
# local bare origin, so the guard's fetch succeeds offline.
set -u
src="$1"
s="$(mktemp -d "${TMPDIR:-/tmp}/t117-guard.XXXXXX")"
mkdir -p "$s/bin"
printf '#!/bin/sh\n[ -n "${FAKE_CHEZMOI_FAIL:-}" ] && exit 1\n[ "$1" = source-path ] && printf "%%s\\n" "$FAKE_SOURCE"\n' > "$s/bin/chezmoi"
chmod +x "$s/bin/chezmoi"
export PATH="$s/bin:/usr/bin:/bin" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
g() { git -c user.name=t -c user.email=t@t -C "$@"; }
mkrepo() {
    mkdir -p "$1/scripts" "$1/home"
    cp "$src" "$1/scripts/upgrade-tools.sh"
    printf 'pins\n' > "$1/tracked"
    git init -q --bare "$1.origin.git"
    g "$1" init -q && g "$1" add tracked && g "$1" commit -q -m base &&
        g "$1" remote add origin "$1.origin.git" && g "$1" push -q origin HEAD:main
}
guard() { (cd "$1" && bash -c 'source scripts/upgrade-tools.sh; require_pins_checkout' 2>&1); echo "rc=$?"; }

mkrepo "$s/canon"
mkrepo "$s/other"
mkdir -p "$s/not-a-checkout"
export FAKE_SOURCE="$s/canon/home"

echo "== 1 canonical clone, full script run"
(cd "$s/canon" && bash scripts/upgrade-tools.sh 2>&1); echo "rc=$?"
echo "== 2 canonical clone + CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 (guard only)"
CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 guard "$s/canon"
echo "== 3 other repo, clean at origin/main (guard only)"
guard "$s/other"
echo "== 4 other repo, untracked file only (guard only)"
touch "$s/other/untracked"
guard "$s/other"
echo "== 5 other repo, tracked edit (guard only)"
printf 'edited\n' > "$s/other/tracked"
guard "$s/other"
echo "== 6 other repo, tracked edit + override (guard only)"
CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 guard "$s/other"
g "$s/other" checkout -q -- tracked
echo "== 7 other repo, HEAD one commit past origin/main (guard only)"
g "$s/other" commit -q --allow-empty -m next
guard "$s/other"
g "$s/other" reset -q --hard origin/main
echo "== 8 other repo, origin/main moved upstream since HEAD (guard only)"
g "$s/canon" commit -q --allow-empty -m upstream && g "$s/canon" push -q "$s/other.origin.git" HEAD:main --force
guard "$s/other"
g "$s/other" reset -q --hard origin/main
echo "== 9 other repo, fetch fails: origin unreachable (guard only)"
g "$s/other" remote set-url origin "$s/missing.git"
guard "$s/other"
echo "== 10 other repo, fetch fails + override (guard only)"
CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 guard "$s/other"
g "$s/other" remote set-url origin "$s/other.origin.git"
echo "== 11 chezmoi on PATH but source-path exits 1 (guard only)"
FAKE_CHEZMOI_FAIL=1 guard "$s/other"
echo "== 12 chezmoi source-path names a directory that is not a git checkout (guard only)"
FAKE_SOURCE="$s/not-a-checkout" guard "$s/other"
echo "== 13 not a git checkout (guard only)"
mkdir -p "$s/plain/scripts" && cp "$src" "$s/plain/scripts/upgrade-tools.sh"
guard "$s/plain"
echo "== 14 chezmoi absent, other repo clean (guard only)"
mv "$s/bin/chezmoi" "$s/chezmoi.off"
guard "$s/other"
rm -rf "$s"
```

Output:

```
$ bash scratchpad/t117-guard-check.sh scripts/upgrade-tools.sh   # c6cd343f
== 1 canonical clone, full script run
make upgrade refused: /tmp/claude-501/t117-guard.f8KZ2H/canon is the canonical chezmoi clone, which stays pull/apply only; run it in a pins worktree of the working clone (herdr-agents --add-worker .claude/worktrees/pins, then make -C <working clone>/.claude/worktrees/pins upgrade) and land the diff through a pull request
rc=2
== 2 canonical clone + CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 (guard only)
rc=0
== 3 other repo, clean at origin/main (guard only)
rc=0
== 4 other repo, untracked file only (guard only)
rc=0
== 5 other repo, tracked edit (guard only)
make upgrade refused: /tmp/claude-501/t117-guard.f8KZ2H/other is dirty or behind origin/main; in the pins worktree run git switch -c <branch> --no-track origin/main (or git reset --hard origin/main on its own branch) first
rc=2
== 6 other repo, tracked edit + override (guard only)
rc=0
== 7 other repo, HEAD one commit past origin/main (guard only)
make upgrade refused: /tmp/claude-501/t117-guard.f8KZ2H/other is dirty or behind origin/main; in the pins worktree run git switch -c <branch> --no-track origin/main (or git reset --hard origin/main on its own branch) first
rc=2
== 8 other repo, origin/main moved upstream since HEAD (guard only)
make upgrade refused: /tmp/claude-501/t117-guard.f8KZ2H/other is dirty or behind origin/main; in the pins worktree run git switch -c <branch> --no-track origin/main (or git reset --hard origin/main on its own branch) first
rc=2
== 9 other repo, fetch fails: origin unreachable (guard only)
fatal: '/tmp/claude-501/t117-guard.f8KZ2H/missing.git' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
make upgrade refused: git fetch origin main failed in /tmp/claude-501/t117-guard.f8KZ2H/other, so origin/main cannot be verified fresh; restore network or credentials and rerun (CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 skips the guard)
rc=2
== 10 other repo, fetch fails + override (guard only)
rc=0
== 11 chezmoi on PATH but source-path exits 1 (guard only)
make upgrade refused: chezmoi source-path could not be resolved in /tmp/claude-501/t117-guard.f8KZ2H/other, so the canonical clone cannot be told apart from this checkout (CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 skips the guard)
rc=2
== 12 chezmoi source-path names a directory that is not a git checkout (guard only)
make upgrade refused: chezmoi source-path could not be resolved in /tmp/claude-501/t117-guard.f8KZ2H/other, so the canonical clone cannot be told apart from this checkout (CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 skips the guard)
rc=2
== 13 not a git checkout (guard only)
rc=0
== 14 chezmoi absent, other repo clean (guard only)
rc=0
```

## R1.3 Upgrade unit tests

The two FAIL lines are the sandbox baseline failures of §4 (identical on origin/main); the unlabelled line is a docstring wrap of an `ok` test in verbose mode.

```
$ uv run python -m unittest tests.unit.test_runtime_health -k upgrade -v 2>&1 | grep -E "^test_upgrade|^Ran|^OK|^FAILED"
test_upgrade_applies_mise_only_from_successful_canonical_checkout (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_applies_mise_only_from_successful_canonical_checkout) ... ok
test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts) ... FAIL
test_upgrade_changes_checkout_not_live_mise_symlink_target (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_changes_checkout_not_live_mise_symlink_target) ... ok
test_upgrade_github_extensions_are_warning_only (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only) ... FAIL
test_upgrade_refuses_the_canonical_clone_and_a_dirty_or_stale_checkout (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_refuses_the_canonical_clone_and_a_dirty_or_stale_checkout) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_self_updates_mise_to_the_manifest_pin (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_the_manifest_pin) ... ok
test_upgrade_skips_unavailable_mise_self_update (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_upgrade_uses_current_mise_node_after_runtime_replacement (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
Ran 9 tests in 45.061s
FAILED (failures=2)
```

## R1.4 Boundary-check and Makefile tests

```
$ GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest tests.unit.test_herdr_agents -k canonical -k agmsg_bootstrap 2>&1 | tail -3
Ran 11 tests in 12.057s

OK
```

## R1.5 Validator, render check, formatters

```
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T117-upgrade-outside-canonical-clone-a01.md
WARN: regime-boundary: worker still seated at .claude/worktrees/worker-c (herdr-agents --remove-worker .claude/worktrees/worker-c)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a001 (herdr-agents --remove-worker)
agent asset validation ok
rc=0
$ make render-check; echo "rc=$?"
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
rc=0
$ prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/claude/rules/agmsg-orchestration.md; shfmt -i 4 -sr -d scripts/upgrade-tools.sh; ruff format --config ruff.toml --check tests/unit/test_runtime_health.py   # via mise -C <empty dir>
Checking formatting...
All matched files use Prettier code style!
shfmt rc=0
1 file already formatted
ruff rc=0
```

## R1.6 CI on c6cd343f

```
$ gh pr checks 308
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37891183473/job/113692255582	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37891183461/job/113692256023	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37891183461/job/113692255978	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37891183461/job/113692255950	
public-bootstrap (macos-14, client)	pass	10m36s	https://github.com/mryfmo/dotfiles/actions/runs/37891183461/job/113692256011	
public-bootstrap (ubuntu-24.04, client)	pass	9m9s	https://github.com/mryfmo/dotfiles/actions/runs/37891183461/job/113692255716	
public-bootstrap (ubuntu-24.04, server)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/37891183461/job/113692255916	
test (macos-14, client)	pass	4m59s	https://github.com/mryfmo/dotfiles/actions/runs/37891183473/job/113692299926	
test (ubuntu-24.04, client)	pass	7m30s	https://github.com/mryfmo/dotfiles/actions/runs/37891183473/job/113692299950	
test (ubuntu-24.04, server)	pass	4m17s	https://github.com/mryfmo/dotfiles/actions/runs/37891183473/job/113692300368	
test (ubuntu-26.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/37891183473/job/113692299934	
validate	pass	1m29s	https://github.com/mryfmo/dotfiles/actions/runs/37891183482/job/113692255642	
```

## R1.7 Full unit suite on c6cd343f vs origin/main b37937ca (same sandbox)

```
$ make unit-test 2>&1 | tail -3   # c6cd343f

FAILED (failures=119, errors=103, skipped=2)
make: *** [unit-test] Error 1
$ comm -23 r1.ids base.ids   # failing test ids only on c6cd343f vs origin/main b37937ca
$ comm -13 r1.ids base.ids   # failing test ids only on origin/main
$ wc -l < r1.ids; wc -l < base.ids
     193
     193
```

## R1.8 Codex Bot wait on c6cd343f

```
$ bounded Bot wait on c6cd343f (reviews by commit_id, top-level comments by original_commit_id; 30 s interval, 15 min)
head committed 2026-10-09T05:58:57Z; deadline 06:13:57Z
bot: none (15 minutes after the final head)
comments: none

```
