# Validation: dotfiles-T73-tool-versions-from-config-a01

- **task_rev:** `sha256:e4368247a59ceeaeb2e100ee171aa2f8d858bbb76e953b4433b0d567529bfb25`. `sha256sum` of the task file in the main checkout matches.
- **Branch:** `chore/tool-versions-from-config` from `origin/main` 523fda06.
- **PR:** #241, https://github.com/mryfmo/dotfiles/pull/241.
- **Commits:**
  - `60688d49`: the change.
  - `b63c6b7d`: `gh pr update-branch` merge of `main` 3a0816e6, which is T89 (#239).
- **Final head:** `b63c6b7d30dbe067c0c04afe6bd89497915c75bb`.

## Validation commands (verbatim, on the final head; unit tests run in the Claude sandbox)

```
$ git log -1 --format=%H
b63c6b7d30dbe067c0c04afe6bd89497915c75bb
$ git diff origin/main --stat
 .github/workflows/test.yaml            | 10 ++++------
 scripts/check-statusline-tools.py      | 13 ++++++++++---
 tests/unit/test_aws_cli_acquisition.py | 20 +++++++++++---------
 tests/unit/test_statusline_tools.py    | 15 ++++++++++-----
 4 files changed, 35 insertions(+), 23 deletions(-)
$ grep -rn "2\.2\.30\|20\.0\.24\|FB5DB77F" .github scripts tests; echo "exit=$?"
exit=1
$ uv run python -m unittest tests.unit.test_statusline_tools tests.unit.test_aws_cli_acquisition 2>&1 | tail -3
Ran 15 tests in 0.151s

OK
$ make unit-test (tail -3)
Ran 722 tests in 163.682s

OK (skipped=2)
```

The grep pattern's fingerprint prefix `FB5DB77F` is the real prefix of `AWS_CLI_FINGERPRINT="FB5DB77FD5C118B80511ADA8A6310ACC4672475C"` (install/ubuntu/common/aws_cli.sh:14). Pin values are unchanged: `home/dot_mise/config.toml` lines 28–29 still read `"npm:ccstatusline" = "2.2.30"` and `"npm:ccusage" = "20.0.24"`, outside the grep scope.

## The workflow's name-based mise calls resolve the configured versions (local, a copy of config.toml + mise.lock, as the CI job makes)

```
$ mise -C <copy> where npm:ccstatusline / npm:ccusage
~/.local/share/mise/installs/npm-ccstatusline/2.2.30
~/.local/share/mise/installs/npm-ccusage/20.0.24
$ mise -C <copy> install --locked --dry-run npm:ccstatusline npm:ccusage
mise npm:ccstatusline@2.2.30     ⇢ already installed
mise npm:ccusage@20.0.24         ⇢ already installed
rc=0
$ mise -C <copy> which ccstatusline
~/.local/share/mise/installs/npm-ccstatusline/2.2.30/bin/ccstatusline
$ PATH=<mise node>:$PATH python3 scripts/check-statusline-tools.py --ccstatusline $(mise -C <copy> which ccstatusline) --ccusage $(mise -C <copy> which ccusage); echo exit=$?
exit=0
expected_versions() {'ccstatusline': '2.2.30', 'ccusage': '20.0.24'}
```

## make validate-agent-assets (run in the main checkout, which is on main)

```
$ make validate-agent-assets; echo exit=$?
exit=0
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: crit review server still running (pgrep -f 'crit _serve')
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-e (herdr-agents --remove-worker)
agent asset validation ok
(untracked .orchestration WARN lines omitted; the boundary commit is the orchestrator's)
```

## Codex review

| Head | Result |
|---|---|
| `60688d49` | 👍 2026-10-04T00:45:32Z, no inline finding |
| `b63c6b7d` (final, the merge of main) | 👍 2026-10-04T00:49:55Z, no inline finding |

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T73 (operator 2026-10-03): ccstatusline/ccusage versions are read from home/dot_mise/config.toml by the statusline smoke script, its unit test and the CI workflow (no `@version` literals), and the awscli fingerprint test reads the installer; pins have one declaration.'
b02665cb-ccee-482d-9ff8-c933438c2de6
```

## CI, mergeable_state and branch (final head `b63c6b7d`)

```
$ gh pr checks 241
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
$ gh api repos/mryfmo/dotfiles/pulls/241 --jq '.mergeable_state'
clean
$ gh api repos/mryfmo/dotfiles/compare/main...chore/tool-versions-from-config
behind_by=0 ahead_by=2
$ statusline steps of run 37166014981 (gh api …/actions/runs/37166014981/jobs)
test (macos-14, client) | Prepare exact statusline tool config | success
test (macos-14, client) | Setup mise for statusline smoke | success
test (macos-14, client) | Install exact statusline tools | success
test (macos-14, client) | Smoke-test statusline tools without network | success
test (ubuntu-26.04, client) | Prepare exact statusline tool config | success
test (ubuntu-26.04, client) | Setup mise for statusline smoke | success
test (ubuntu-26.04, client) | Install exact statusline tools | success
test (ubuntu-26.04, client) | Smoke-test statusline tools without network | success
test (ubuntu-24.04, client) | Prepare exact statusline tool config | success
test (ubuntu-24.04, client) | Setup mise for statusline smoke | success
test (ubuntu-24.04, client) | Install exact statusline tools | success
test (ubuntu-24.04, client) | Smoke-test statusline tools without network | success
test (ubuntu-24.04, server) | Prepare exact statusline tool config | success
test (ubuntu-24.04, server) | Setup mise for statusline smoke | success
test (ubuntu-24.04, server) | Install exact statusline tools | success
test (ubuntu-24.04, server) | Smoke-test statusline tools without network | success
```
