# Validation: dot-ci-runner-label-pin-T58-a01

- PR: #229 https://github.com/mryfmo/dotfiles/pull/229
- Head SHA: 88f797360b3d7b590e5e5d1e56f9c0b1b842d88e (base origin/main 3c4c2cec)

## Grounding grep before editing (verbatim)

```
$ git grep -n -E 'ubuntu-latest' -- .github scripts tests README.md Makefile
.github/workflows/agent-assets.yml:18:    runs-on: ubuntu-latest
.github/workflows/docs.yml:28:    runs-on: ubuntu-latest
.github/workflows/remote.yaml:20:          - os: ubuntu-latest
.github/workflows/remote.yaml:22:          - os: ubuntu-latest
.github/workflows/remote.yaml:80:          - os: ubuntu-latest
.github/workflows/remote.yaml:82:          - os: ubuntu-latest
.github/workflows/test.yaml:18:    runs-on: ubuntu-latest
.github/workflows/test.yaml:85:        os: [ubuntu-latest, macos-14]
.github/workflows/test.yaml:136:          elif [ "${OS}" == "ubuntu-latest" ]; then
.github/workflows/test.yaml:238:          if [ "${OS}" = "ubuntu-latest" ]; then
.github/workflows/test.yaml:275:          if [ "${OS}" == "ubuntu-latest" ]; then
.github/workflows/test.yaml:348:        if: ${{ needs.changes.outputs.should_test == 'true' && matrix.os == 'ubuntu-latest' && !endsWith(github.actor, '[bot]') }}
.github/workflows/test.yaml:355:        if: ${{ needs.changes.outputs.should_test == 'true' && matrix.os == 'ubuntu-latest' && !endsWith(github.actor, '[bot]') }}
.github/workflows/test.yaml:382:        os: [ubuntu-latest, macos-14]
.github/workflows/ubuntu.yaml:37:    runs-on: ubuntu-latest
README.md:938:        {"context": "test (ubuntu-latest, server)"},
README.md:939:        {"context": "test (ubuntu-latest, client)"},
README.md:941:        {"context": "public-bootstrap (ubuntu-latest, server)"},
README.md:942:        {"context": "public-bootstrap (ubuntu-latest, client)"},
scripts/run_unit_test.sh:30:    elif [ "${OS}" == "ubuntu-latest" ]; then
scripts/run_unit_test.sh:56:    elif [ "${OS}" == "ubuntu-latest" ] && { [ "${SYSTEM}" == "client" ] || [ "${SYSTEM}" == "server" ]; }; then
tests/unit/test_pr_feedback.py:87:                    "name": "test (ubuntu-latest, server)",
tests/unit/test_pr_feedback.py:130:                "message": "The ubuntu-latest label will migrate to Ubuntu 26",
tests/unit/test_supply_chain_policy.py:461:        self.assertIn("ubuntu-latest", workflow)
```

## Task validation commands after editing (verbatim)

```
$ git grep -n -E 'ubuntu-latest' -- .github scripts tests README.md Makefile
tests/unit/test_pr_feedback.py:130:                "message": "The ubuntu-latest label will migrate to Ubuntu 26",
(exit 0)
$ git diff origin/main --stat
 .github/workflows/agent-assets.yml     |  2 +-
 .github/workflows/docs.yml             |  2 +-
 .github/workflows/remote.yaml          |  8 ++++----
 .github/workflows/test.yaml            | 23 +++++++++++++++--------
 .github/workflows/ubuntu.yaml          |  2 +-
 README.md                              |  8 ++++----
 scripts/run_unit_test.sh               |  4 ++--
 tests/unit/test_pr_feedback.py         |  2 +-
 tests/unit/test_supply_chain_policy.py |  2 +-
 9 files changed, 30 insertions(+), 23 deletions(-)
(exit 0)
$ shellcheck scripts/run_unit_test.sh
(exit 0)
$ mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d scripts/run_unit_test.sh
(exit 0)
$ command -v actionlint && actionlint .github/workflows/test.yaml .github/workflows/remote.yaml .github/workflows/agent-assets.yml .github/workflows/docs.yml .github/workflows/ubuntu.yaml
actionlint not installed
$ make unit-test
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 718 tests in 160.276s

OK (skipped=2)
(exit 0)
$ make validate-agent-assets
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01.md
agent asset validation ok
(exit 0)
```

## gh pr checks 229 (verbatim, unsandboxed)

```
$ gh pr checks 229
test (ubuntu-26.04, client)	fail	49s	https://github.com/mryfmo/dotfiles/actions/runs/37064146970/job/111027711303	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build (client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/37064147012/job/111027668008	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37064147012/job/111027667788	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37064146970/job/111027713474	
changes	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37064146970/job/111027667716	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37064146921/job/111027667753	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37064146921/job/111027667791	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37064146921/job/111027667532	
public-bootstrap (macos-14, client)	pass	8m26s	https://github.com/mryfmo/dotfiles/actions/runs/37064146921/job/111027667970	
public-bootstrap (ubuntu-24.04, client)	pass	8m58s	https://github.com/mryfmo/dotfiles/actions/runs/37064146921/job/111027667721	
public-bootstrap (ubuntu-24.04, server)	pass	6m34s	https://github.com/mryfmo/dotfiles/actions/runs/37064146921/job/111027667810	
test (macos-14, client)	pass	5m16s	https://github.com/mryfmo/dotfiles/actions/runs/37064146970/job/111027711426	
test (ubuntu-24.04, client)	pass	7m47s	https://github.com/mryfmo/dotfiles/actions/runs/37064146970/job/111027711300	
test (ubuntu-24.04, server)	pass	4m24s	https://github.com/mryfmo/dotfiles/actions/runs/37064146970/job/111027711402	
validate	pass	15s	https://github.com/mryfmo/dotfiles/actions/runs/37064146885/job/111027667265	
(exit 1)
$ gh run view 37064146970 --json conclusion,jobs -q ...   # the test workflow run stays green with the canary red (continue-on-error)
run conclusion: success
changes: success
test (ubuntu-24.04, client): success
test (ubuntu-26.04, client): failure
test (ubuntu-24.04, server): success
test (macos-14, client): success
nix: skipped
$ gh pr view 229 --json number,url,headRefOid,state,mergeStateStatus -q ...
#229 https://github.com/mryfmo/dotfiles/pull/229 88f797360b3d7b590e5e5d1e56f9c0b1b842d88e OPEN UNSTABLE
```

## Canary result: test (ubuntu-26.04, client), job 111027711303 (verbatim excerpts)

```
$ gh run view --job 111027711303 --log | grep -m3 -E "Image: |Version: |Image Release"
2026-10-02T21:00:22.9071423Z Version: 20260901.588
2026-10-02T21:00:22.9087384Z Image: ubuntu-26.04
2026-10-02T21:00:22.9088560Z Version: 20260927.149.1
2026-10-02T21:00:22.9094092Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu26%2F20260927.149
$ gh run view --job 111027711303 --log | grep -E "##\[error\]|TimeoutExpired"
Smoke-test statusline tools without network	2026-10-02T21:01:10.5459477Z     raise TimeoutExpired(
Smoke-test statusline tools without network	2026-10-02T21:01:10.5461683Z subprocess.TimeoutExpired: Command '['~/.local/share/mise/installs/npm-ccstatusline/2.2.30/bin/ccstatusline', '--version']' timed out after 5 seconds
Smoke-test statusline tools without network	2026-10-02T21:01:10.5623152Z ##[error]Process completed with exit code 1.
```

## CompactionDB (main checkout, unsandboxed)

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T58 (operator 2026-10-02): CI runner labels are explicit (`ubuntu-24.04`, `macos-14`), never `*-latest`; a new OS image is adopted through a non-required canary cell first, then by changing the explicit label.'
e6bdb8d4-9297-4616-998d-b7a108578112
(exit 0)
```
