# Validation: dotfiles-T74-bootstrap-dead-code-a01

- **task_rev:** `sha256:66b87608d58c990f29800fc59a1330887194e0fbc9d560649f2bd2920549793b`. `sha256sum` of the task file in the main checkout matches.
- **Branch:** `chore/bootstrap-dead-code` from `origin/main` 138e6a72.
- **PR:** #247, https://github.com/mryfmo/dotfiles/pull/247.
- **Commits:**
  - `2487b05a`: the deletions.
  - `c0ea3e7f`: keep the external config's platform guard (Codex P2).
- **Final head:** `c0ea3e7f1b150f43e6841642038cc62b290653c6`.

## Re-verification before deleting (`git grep` on 138e6a72, excluding .orchestration, .ua, reviews, vendor)

```
## arm64/run           -> install/macos/arm64/run.sh:3,15 (only itself)
## restart_shell / get_system_from_chezmoi -> setup.sh:369,375,377,393,398,408 (only the family and the commented call)
## chezmoi-private init -> Makefile:37; tests/install/common/lifecycle.bats:235 (the skip test)
## chezmoiexternal      -> .github/workflows/test.yaml:336-337 (fixture cleanup, kept); home/.chezmoiexternal.yaml.tmpl:1,3,5; tests/unit/test_supply_chain_policy.py (common.yaml.tmpl only)
## flake / should_nix / nix/ -> test.yaml:21,80-84,415-437; test_supply_chain_policy.py:461-477; flake.nix; nix/**; prose in docs/plans/nix-*.md and plans/004-*.md (not edited)
$ grep -rn -i 'nix\b|flake|cachix' .github renovate.json scripts (other than test.yaml) -> no output
$ wc -c home/.chezmoitemplates/chezmoiexternal.d/*
1499 common.yaml.tmpl / 0 macos.yaml.tmpl / 0 ubuntu.yaml.tmpl
```

## Validation commands (verbatim; unit tests run in the Claude sandbox; run on `2487b05a`, the deletion commit)

```
$ git log -1 --format=%H
2487b05ac22281ddc8c0866c4e805585ac10887e
$ git diff origin/main --stat
 .github/workflows/test.yaml                        | 31 --------
 Makefile                                           |  6 --
 flake.lock                                         | 71 -----------------
 flake.nix                                          | 91 ----------------------
 home/.chezmoiexternal.yaml.tmpl                    |  7 --
 .../chezmoiexternal.d/macos.yaml.tmpl              |  0
 .../chezmoiexternal.d/ubuntu.yaml.tmpl             |  0
 install/macos/arm64/run.sh                         | 18 -----
 nix/home-manager/default.nix                       | 28 -------
 nix/nix-darwin/default.nix                         | 47 -----------
 nix/shared/packages.nix                            | 30 -------
 setup.sh                                           | 35 ---------
 tests/install/common/lifecycle.bats                |  5 +-
 tests/unit/test_supply_chain_policy.py             | 25 ------
 14 files changed, 2 insertions(+), 392 deletions(-)
$ git ls-files | grep -E '^(flake\.|nix/|install/macos/arm64/run\.sh|home/\.chezmoitemplates/chezmoiexternal\.d/(macos|ubuntu))' ; echo "rc=$?"
rc=1
$ grep -rn "restart_shell\|chezmoi-private init\|should_nix\|get_system_from_chezmoi" setup.sh Makefile .github ; echo "rc=$?"
rc=1
$ grep -rn 'arm64/run' home install setup.sh Makefile .github tests ; echo "rc=$?"
rc=1
$ bash -n setup.sh; echo rc=$?
rc=0
$ chezmoi --source $PWD/home --config <tmp: data.system=client, data.email=ci@example.invalid> --persistent-state <tmp> execute-template < home/.chezmoiexternal.yaml.tmpl | head -5   (the task's --init flags do not point execute-template at this source; this renders the worktree source)
".emacs.d":
  type: "archive"
  url: "https://github.com/syl20bnr/spacemacs/archive/530c17d62e4ccca09087a2f142752b21000658fb.tar.gz"
  checksum:
    sha256: "ba040a5d04a6d37c821274eea1f1e4c26d146e2f65057b4d15f4741159071260"
$ make -n init
chezmoi init --apply --verbose
$ make unit-test (tail -3)
Ran 700 tests in 160.737s

OK (skipped=1)
$ make validate-agent-assets > log; echo exit=$?   (in the worktree)
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
$ mise x node npm:prettier -- prettier --check .github/workflows/test.yaml
Checking formatting...
All matched files use Prettier code style!
```

## chezmoiexternal rendering, origin/main vs branch (this host: linux, idLike debian)

```
$ (2487b05a, common include alone) diff of rendered output vs origin/main, blank lines ignored
rendered output identical (ignoring blank lines) to origin/main
$ (c0ea3e7f, guard restored ahead of the include) same diff
rc=0
rendered output identical (ignoring blank lines) to origin/main
$ (c0ea3e7f template with the OS test forced false: darwin/linux replaced by plan9) | tail -1
chezmoi: template: stdin:2:5: executing "stdin" at <fail (printf "Unknown OS for client system: %s" .chezmoi.os)>: error calling fail: Unknown OS for client system: linux
```

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T74 (operator 2026-10-03): the unused bootstrap paths are deleted: `install/macos/arm64/run.sh`, the `make init` private-init branch, setup.sh'"'"'s disabled `restart_shell` family, the empty macOS/Ubuntu chezmoiexternal templates, and the whole nix flake with its CI job and test; bootstrap is `./setup.sh` + chezmoi only.'
9c4baa38-0730-4e71-b6a7-fcc6b06be80c
```

## Addendum 1 greps (task_rev `sha256:35ec2cb2…6107b`; run after the deletion was already pushed, because the addendum arrived later)

```
$ grep -rn chezmoi_private home/.chezmoiscripts
home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl:2:{{   include "../install/common/chezmoi_private.sh" }}
rc=0
$ grep -n chezmoi-private setup.sh ; echo rc=$?
rc=1
$ grep -rn 'make init' . --exclude-dir=.git --exclude-dir=.orchestration --exclude-dir=.agents --exclude-dir=.ua
home/dot_codex/rules/default.rules:172:    match=["make setup", "make init", "make update", "make apply", "make upgrade", "make watch", "make reset", "make clean", "make deploy"],
rc=0
```

Grep 3 disagrees with the literal expectation. README:640 is not matched (it reads "`make setup`, `init`, `update`"), and the only hit is the T63 execpolicy forbidden-rule example in `home/dot_codex/rules/default.rules:172`, which is not a caller. A blocked PONG with this evidence was sent at 2026-10-04T03:19:48Z.

## CI, mergeable_state, branch and Codex (final head `c0ea3e7f`)

```
pushed=2026-10-04T03:18:03Z polls=60
2487b05ac22281ddc8c0866c4e805585ac10887e	2026-10-04T03:13:29Z
CodeRabbit	pass
build	pass
build (client)	pass
build (server)	pass
changes	pass
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
{
"baseRefOid": "138e6a72847b159d1a72b9b50af4dd9126016f06",
"headRefOid": "c0ea3e7f1b150f43e6841642038cc62b290653c6",
"mergeStateStatus": "BLOCKED"
}
blocked
behind_by=0 ahead_by=2

(first two lines: the Codex poll on c0ea3e7f, 60 x 15 s, then the Bot reviews listed by commit: only 2487b05a at 03:13:29Z; bot: none on c0ea3e7f)
$ unresolved review threads
4175951412 **  Update Nix documentation after deleting the flake**
4175951414 **  Retain the external template's platform guard**
```

`blocked` is only these two P2 threads: 4175951414 `fixed:c0ea3e7f` and 4175951412 `not-applicable` (decision 1; the orchestrator replies). The `nix` check context is gone. The `build`, `build (client)` and `build (server)` contexts come from the workflow that the Makefile change triggers.
