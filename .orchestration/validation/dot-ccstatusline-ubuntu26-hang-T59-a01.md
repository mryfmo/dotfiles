# Validation: dot-ccstatusline-ubuntu26-hang-T59-a01

- PR: #230 https://github.com/mryfmo/dotfiles/pull/230
- Final head: cc19dd4c (full SHA below); diagnostics commits 6e0faeba, 1e280118, 50588cfc (all reverted by cc19dd4c)

## Task validation commands (verbatim)

```
$ git diff origin/main --stat
 .github/workflows/test.yaml       | 13 ++++++++++++-
 tests/unit/test_runtime_health.py |  5 +++--
 2 files changed, 15 insertions(+), 3 deletions(-)
(exit 0)
$ git log --oneline origin/main..HEAD
cc19dd4c fix(ci): run the statusline smoke on mise's pinned node, fix the no-tar PATH guard
50588cfc ci(diag): TEMPORARY T59 round 3, page-cache evidence for the cold node start
1e280118 ci(diag): TEMPORARY T59 round 2, cold-order ccstatusline --version diagnostics
6e0faeba ci(diag): TEMPORARY T59 ccstatusline --version timing on the ubuntu-26.04 canary
$ git grep -n -c "T59 diag\|TEMPORARY T59" -- .github; echo $?   # no diagnostics left on the final head
1
$ make unit-test
----------------------------------------------------------------------
Ran 718 tests in 160.067s

OK (skipped=2)
(exit 0)
$ make validate-agent-assets
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01.md
agent asset validation ok
(exit 0)
$ make render-check   # not run: agent-config.yaml and settings were not touched
```

## gh pr checks 230 on the final head (verbatim, unsandboxed)

```
$ gh pr checks 230
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37076377562/job/111067109855	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37076377561/job/111067110093	
private-bootstrap (ubuntu-24.04, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37076377561/job/111067110072	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37076377561/job/111067109834	
public-bootstrap (macos-14, client)	pass	6m23s	https://github.com/mryfmo/dotfiles/actions/runs/37076377561/job/111067110091	
test (macos-14, client)	pass	5m17s	https://github.com/mryfmo/dotfiles/actions/runs/37076377562/job/111067151471	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37076377562/job/111067152276	
public-bootstrap (ubuntu-24.04, client)	pass	8m50s	https://github.com/mryfmo/dotfiles/actions/runs/37076377561/job/111067110159	
public-bootstrap (ubuntu-24.04, server)	pass	7m10s	https://github.com/mryfmo/dotfiles/actions/runs/37076377561/job/111067110157	
test (ubuntu-24.04, client)	pass	7m1s	https://github.com/mryfmo/dotfiles/actions/runs/37076377562/job/111067151449	
test (ubuntu-24.04, server)	pass	4m19s	https://github.com/mryfmo/dotfiles/actions/runs/37076377562/job/111067151430	
test (ubuntu-26.04, client)	pass	7m19s	https://github.com/mryfmo/dotfiles/actions/runs/37076377562/job/111067151416	
validate	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37076377572/job/111067109781	
(exit 0)
$ gh run view 37076377562 --json conclusion -q .conclusion
success
$ gh pr view 230 --json number,url,headRefOid,state,isDraft -q ...
#230 https://github.com/mryfmo/dotfiles/pull/230 cc19dd4c84e500ec617b95752032e3b3c86c424a OPEN draft=false
$ gh run view --job 111067151416 --log | grep -iE 'ccstatusline|statusline|timed out'   # passing canary (statusline step headers; the smoke itself prints nothing on success)
test (ubuntu-26.04, client)	﻿2026-10-02T23:12:05.6354515Z ##[group]Run statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
test (ubuntu-26.04, client)	﻿2026-10-02T23:12:05.6668717Z ##[group]Run jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c
test (ubuntu-26.04, client)	2026-10-02T23:12:07.1907216Z ##[group]Running mise --version
test (ubuntu-26.04, client)	2026-10-02T23:12:07.2065175Z ##[group]Running mise ls
test (ubuntu-26.04, client)	﻿2026-10-02T23:12:07.2658241Z ##[group]Run mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"
test (ubuntu-26.04, client)	﻿2026-10-02T23:12:10.3503270Z ##[group]Run set -euo pipefail
$ ... | grep -ciE "timed out|TimeoutExpired|exceeded the 5-second"
0
```

## Root-cause evidence (diagnostic job logs, verbatim excerpts)

### Diagnostics 1: run 37072287780, job 111054323730 (6e0faeba). Every variant was fast once warmed, and the real smoke step PASSED after these warm calls.

```
 T59 bin=/home/runner/.local/share/mise/installs/npm-ccstatusline/2.2.30/bin/ccstatusline real=/home/runner/.local/share/mise/installs/npm-ccstatusline/2.2.30/lib/node_modules/ccstatusline/dist/ccstatusline.js
 T59 shebang=#!/usr/bin/env node
 T59 node=/home/runner/.local/share/mise/shims/node v24.21.0
 T59 net node --version: rc=0 secs=.022508747 out=v24.21.0 
 T59 net ccstatusline --version: rc=0 secs=.434949940 out=2.2.30 
 T59 nonet node --version: rc=0 secs=.031713201 out=v24.21.0 
 T59 nonet ccstatusline --version: rc=0 secs=.224754468 out=2.2.30 
 T59 nonet+lo ccstatusline --version: rc=0 secs=.221033138 out=2.2.30 
 T59 nonet noproxy ccstatusline --version: rc=0 secs=.218284412 out=2.2.30 
 T59 nonet node bundle direct: rc=0 secs=.211809281 out=2.2.30 
$ grep "Smoke-test statusline" step for errors in the same job:
0
```

### Diagnostics 2: run 37073281320, job 111057641867 (1e280118). Cold order with a fresh HOME per case: only the very first node run is slow, there are no network syscalls, and the mise shim resolves to SYSTEM node.

```
 T59 mise=/home/runner/.local/share/mise/bin/mise 2026.9.12 linux-x64 (2026-09-20)
 T59 resolv= nameserver 127.0.0.53 options edns0 trust-ad search hofw3xyzloau3bb0znavhgxo5a.qrox.internal.cloudapp.net 
 T59 nsswitch-hosts=hosts:          files dns
 T59 cold strace ccstatusline rc=0 lines=4601
 T59 cold total 2.80s over 4601 lines
 T59 key 2965  22:36:31.037397 execve("/usr/local/bin/node", ["/usr/local/bin/node", "/home/runner/.local/share/mise/i"..., "--version"], 0x651414e87b20 /* 62 vars */ <unfinished ...>
 T59 cold nonet node shim trace: rc=0 secs=.031833915
 T59   | TRACE  1 [src/shims.rs:335] shim[node] SYSTEM /usr/local/bin/node
 T59 cold nonet ccstatusline no-shims PATH: rc=0 secs=.214163535
 T59 cold nonet ccstatusline MISE_OFFLINE=1: rc=0 secs=.218493952
 T59 cold nonet ccstatusline again (2nd fresh home): rc=0 secs=.220217366
 T59 warm-home nonet ccstatusline (reuse last home): rc=0 secs=.219085572
$ grep -cE "connect\(|sendto\(|recvfrom\(.*:53" in the cold strace key lines:
0
```

### Diagnostics 3: run 37074296650, job 111060649072 (50588cfc). Page-cache residency: the system node is not resident until the cold run reads it; the pinned node is already resident.

```
 ##[group]Run set -u
 shell: /usr/bin/bash -e {0}
 env:
   OS: ubuntu-26.04
   SYSTEM: client
   CODECOV_FLAGS: ubuntu-26.04-client
   CODECOV_NAME: codecov-dotfiles-ubuntu-26.04-client
   GITHUB_TOKEN: ***
   FILES_TEST_CHEZMOI: /usr/local/bin/chezmoi
   MISE_LOG_LEVEL: info
   MISE_GITHUB_TOKEN: ***
   MISE_TRUSTED_CONFIG_PATHS: /home/runner/work/dotfiles/dotfiles
   MISE_YES: 1
 ##[endgroup]
 T59 system node=-rwxrwxrwx 1 root root 126595440 Sep 27 21:32 /usr/local/bin/node pinned=/home/runner/.local/share/mise/installs/node/26.10.0/bin/node
 T59 fincore before any run:
 T59         RES PAGES      SIZE FILE
 T59           0     0 126595440 /usr/local/bin/node
 T59   149712896 36551 149711504 /home/runner/.local/share/mise/installs/node/26.10.0/bin/node
 T59     3018752   737   3018224 /home/runner/.local/share/mise/installs/npm-ccstatusline/2.2.30/lib/node_modules/ccstatusline/dist/ccstatusline.js
 T59 cold nonet ccstatusline --version, pinned node first on PATH: rc=0 secs=.218119513 out=2.2.30 
 T59 fincore after pinned-node run:
 T59         RES PAGES      SIZE FILE
 T59           0     0 126595440 /usr/local/bin/node
 T59   149712896 36551 149711504 /home/runner/.local/share/mise/installs/node/26.10.0/bin/node
 T59     3018752   737   3018224 /home/runner/.local/share/mise/installs/npm-ccstatusline/2.2.30/lib/node_modules/ccstatusline/dist/ccstatusline.js
 T59 cold nonet ccstatusline --version, PATH as in the smoke (system node): rc=0 secs=.619051396 out=2.2.30 
 T59 fincore after system-node run:
 T59         RES PAGES      SIZE FILE
 T59    54837248 13388 126595440 /usr/local/bin/node
 T59   149712896 36551 149711504 /home/runner/.local/share/mise/installs/node/26.10.0/bin/node
 T59     3018752   737   3018224 /home/runner/.local/share/mise/installs/npm-ccstatusline/2.2.30/lib/node_modules/ccstatusline/dist/ccstatusline.js
 T59 warm nonet ccstatusline --version, PATH as in the smoke: rc=0 secs=.230761691 out=2.2.30 
```

### Original failure: run 37064146970, job 111027711303 (750cc4a9, before any change)

```
Smoke-test statusline tools without network	2026-10-02T21:01:10.5459477Z     raise TimeoutExpired(
Smoke-test statusline tools without network	2026-10-02T21:01:10.5461683Z subprocess.TimeoutExpired: Command '['/home/runner/.local/share/mise/installs/npm-ccstatusline/2.2.30/bin/ccstatusline', '--version']' timed out after 5 seconds
```

### Second canary failure: run 37072287780, job 111054323730

```
 FileExistsError: [Errno 17] File exists: '/bin/grub-ntldr-img' -> '/tmp/runtime-health-test-58kcnb35/no-tar-bin/grub-ntldr-img'
 FAILED (errors=1, skipped=1)
```

## CompactionDB (main checkout, unsandboxed)

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T59 (operator 2026-10-03): the Ubuntu 26.04 canary stays non-required but must be green; a canary failure is fixed at its root (here `ccstatusline --version` hanging without network on the 26.04 image), never dispositioned repeatedly.'
e547c5a4-c593-47a6-bb13-3eff3f99ea7d
(exit 0)
```
