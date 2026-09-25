# Validation: remote-diff-01

All blocks below are verbatim stdout+stderr of the command in the heading, executed in `/home/moriya/Workspace/dotfiles` on 2026-09-25 by claude-standard-dot-a001.

## 1. Remote and local refs

### `git -C /home/moriya/Workspace/dotfiles ls-remote origin refs/heads/main`

```text
3303fbca15ef355a66c5f57fff47b59bd1e25130	refs/heads/main
```

### `git rev-list --left-right --count main...origin/main`

```text
0	0
```

### `git reflog show --date=iso main -5`

```text
3303fbc main@{2026-09-25 15:24:54 +0900}: pull --ff-only: Fast-forward
455455e main@{2026-09-23 16:35:17 +0900}: clone: from https://github.com/mryfmo/dotfiles.git
```

## 2. Commit list and range stats

### `git log --reverse --format='%h %cI %an %s' 455455e..3303fbc`

```text
3a530b1 2026-09-24T12:37:30+09:00 mryfmo Add files via upload
7e35d78 2026-09-24T12:39:23+09:00 mryfmo Delete PRD_ADR_BDD.zip
c5193e4 2026-09-24T12:39:37+09:00 mryfmo Delete TestSuite.zip
22e5c9f 2026-09-25T09:59:38+09:00 mryfmo fix(update): converge herdr SessionStart matcher, report unmerged index, dedupe agmsg identities (#170)
d377ad0 2026-09-25T10:00:27+09:00 mryfmo chore(mise): upgrade tool pins via make upgrade (#171)
0aafdb9 2026-09-25T10:29:27+09:00 mryfmo Add files via upload
f78666a 2026-09-25T10:32:03+09:00 mryfmo Delete jev-all-engines.zip
cd61a88 2026-09-25T10:41:14+09:00 mryfmo fix(mise): stop make upgrade and mise from writing into the main checkout (#172)
c11035f 2026-09-25T10:42:10+09:00 mryfmo fix(update): tolerate a herdr protocol mismatch on reload; align docs and dev image (#174)
c5240c3 2026-09-25T10:52:40+09:00 mryfmo feat(agmsg): add agmsg-dispatch to send, wake an idle worker, and verify receipt (#173)
f95074a 2026-09-25T10:55:36+09:00 mryfmo chore(orchestration): sync 2026-09-25 session (T1 convergence, T2 pins, T3 mise symlink, T4 agmsg-dispatch, T5 ua-refresh, herdr-sheldon a02)
60c1be4 2026-09-25T03:54:27+00:00 dependabot[bot] chore(deps): bump cachix/install-nix-action from 31.10.7 to 31.11.1
3d6eb8d 2026-09-25T03:54:32+00:00 dependabot[bot] chore(deps): bump actions/checkout from 7.0.0 to 7.0.1
01c8bdd 2026-09-25T03:54:38+00:00 dependabot[bot] chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0
cb28a55 2026-09-25T03:54:41+00:00 dependabot[bot] chore(deps): bump jdx/mise-action from 4.2.0 to 4.3.0
8276e9d 2026-09-25T13:02:01+09:00 mryfmo fix(herdr): enable experimental kitty graphics for terminal tool panes (#146)
efc2bb2 2026-09-25T13:05:26+09:00 dependabot[bot] chore(deps): bump codecov/codecov-action from 7.0.0 to 7.1.1 (#159)
5b4fd8b 2026-09-25T13:14:43+09:00 mryfmo fix(validate): skip nested git worktrees in the repo-wide scans (#176)
9baed29 2026-09-25T13:16:55+09:00 mryfmo docs(adh): add the ADH Integrated Plan input baseline (#175)
d6cfed2 2026-09-25T13:18:26+09:00 mryfmo chore(orchestration): sync T6 adh-baseline and T7 validator-worktrees records
01073f2 2026-09-25T14:01:48+09:00 mryfmo chore(deps): bump actions/checkout from 7.0.0 to 7.0.1 (#103)
3a8c7d3 2026-09-25T14:01:48+09:00 mryfmo chore(deps): bump jdx/mise-action from 4.2.0 to 4.3.0 (#154)
6775bb7 2026-09-25T14:02:37+09:00 mryfmo chore(orchestration): sync T8 dependabot-verify records
127e27b 2026-09-25T14:27:46+09:00 mryfmo chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0 (#155)
d906b00 2026-09-25T14:31:30+09:00 mryfmo chore(deps): bump cachix/install-nix-action from 31.10.7 to 31.11.1 (#125)
b277a51 2026-09-25T15:17:39+09:00 mryfmo chore(ua): full knowledge-graph rebuild at d906b00; exclude .orchestration and reviews (#177)
3303fbc 2026-09-25T15:18:04+09:00 mryfmo chore(orchestration): sync T9 ua-full-rebuild records
```

### `git log --graph --format='%h %p | %s' 455455e..3303fbc`

```text
* 3303fbc b277a51 | chore(orchestration): sync T9 ua-full-rebuild records
* b277a51 d906b00 | chore(ua): full knowledge-graph rebuild at d906b00; exclude .orchestration and reviews (#177)
*   d906b00 127e27b 60c1be4 | chore(deps): bump cachix/install-nix-action from 31.10.7 to 31.11.1 (#125)
|\  
| * 60c1be4 f95074a | chore(deps): bump cachix/install-nix-action from 31.10.7 to 31.11.1
* |   127e27b 6775bb7 01c8bdd | chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0 (#155)
|\ \  
| * | 01c8bdd f95074a | chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0
| |/  
* | 6775bb7 3a8c7d3 | chore(orchestration): sync T8 dependabot-verify records
* |   3a8c7d3 01073f2 cb28a55 | chore(deps): bump jdx/mise-action from 4.2.0 to 4.3.0 (#154)
|\ \  
| * | cb28a55 f95074a | chore(deps): bump jdx/mise-action from 4.2.0 to 4.3.0
| |/  
* |   01073f2 d6cfed2 3d6eb8d | chore(deps): bump actions/checkout from 7.0.0 to 7.0.1 (#103)
|\ \  
| * | 3d6eb8d f95074a | chore(deps): bump actions/checkout from 7.0.0 to 7.0.1
| |/  
* | d6cfed2 9baed29 | chore(orchestration): sync T6 adh-baseline and T7 validator-worktrees records
* | 9baed29 5b4fd8b | docs(adh): add the ADH Integrated Plan input baseline (#175)
* | 5b4fd8b efc2bb2 | fix(validate): skip nested git worktrees in the repo-wide scans (#176)
* | efc2bb2 8276e9d | chore(deps): bump codecov/codecov-action from 7.0.0 to 7.1.1 (#159)
* | 8276e9d f95074a | fix(herdr): enable experimental kitty graphics for terminal tool panes (#146)
|/  
* f95074a c5240c3 | chore(orchestration): sync 2026-09-25 session (T1 convergence, T2 pins, T3 mise symlink, T4 agmsg-dispatch, T5 ua-refresh, herdr-sheldon a02)
* c5240c3 c11035f | feat(agmsg): add agmsg-dispatch to send, wake an idle worker, and verify receipt (#173)
* c11035f cd61a88 | fix(update): tolerate a herdr protocol mismatch on reload; align docs and dev image (#174)
* cd61a88 f78666a | fix(mise): stop make upgrade and mise from writing into the main checkout (#172)
* f78666a 0aafdb9 | Delete jev-all-engines.zip
* 0aafdb9 d377ad0 | Add files via upload
* d377ad0 22e5c9f | chore(mise): upgrade tool pins via make upgrade (#171)
* 22e5c9f c5193e4 | fix(update): converge herdr SessionStart matcher, report unmerged index, dedupe agmsg identities (#170)
* c5193e4 7e35d78 | Delete TestSuite.zip
* 7e35d78 3a530b1 | Delete PRD_ADR_BDD.zip
* 3a530b1 455455e | Add files via upload
```

### `git log --reverse --format='%h %aI | %cI | %an / %cn' 455455e..3303fbc`

```text
3a530b1 2026-09-24T12:37:30+09:00 | 2026-09-24T12:37:30+09:00 | mryfmo / GitHub
7e35d78 2026-09-24T12:39:23+09:00 | 2026-09-24T12:39:23+09:00 | mryfmo / GitHub
c5193e4 2026-09-24T12:39:37+09:00 | 2026-09-24T12:39:37+09:00 | mryfmo / GitHub
22e5c9f 2026-09-25T09:59:38+09:00 | 2026-09-25T09:59:38+09:00 | mryfmo / GitHub
d377ad0 2026-09-25T10:00:27+09:00 | 2026-09-25T10:00:27+09:00 | mryfmo / GitHub
0aafdb9 2026-09-25T10:29:27+09:00 | 2026-09-25T10:29:27+09:00 | mryfmo / GitHub
f78666a 2026-09-25T10:32:03+09:00 | 2026-09-25T10:32:03+09:00 | mryfmo / GitHub
cd61a88 2026-09-25T10:41:14+09:00 | 2026-09-25T10:41:14+09:00 | mryfmo / GitHub
c11035f 2026-09-25T10:42:10+09:00 | 2026-09-25T10:42:10+09:00 | mryfmo / GitHub
c5240c3 2026-09-25T10:52:40+09:00 | 2026-09-25T10:52:40+09:00 | mryfmo / GitHub
f95074a 2026-09-25T10:55:36+09:00 | 2026-09-25T10:55:36+09:00 | mryfmo / mryfmo
60c1be4 2026-09-25T03:54:27+00:00 | 2026-09-25T03:54:27+00:00 | dependabot[bot] / GitHub
3d6eb8d 2026-09-25T03:54:32+00:00 | 2026-09-25T03:54:32+00:00 | dependabot[bot] / GitHub
01c8bdd 2026-09-25T03:54:38+00:00 | 2026-09-25T03:54:38+00:00 | dependabot[bot] / GitHub
cb28a55 2026-09-25T03:54:41+00:00 | 2026-09-25T03:54:41+00:00 | dependabot[bot] / GitHub
8276e9d 2026-09-25T13:02:01+09:00 | 2026-09-25T13:02:01+09:00 | mryfmo / GitHub
efc2bb2 2026-09-25T13:05:26+09:00 | 2026-09-25T13:05:26+09:00 | dependabot[bot] / GitHub
5b4fd8b 2026-09-25T13:14:43+09:00 | 2026-09-25T13:14:43+09:00 | mryfmo / GitHub
9baed29 2026-09-25T13:16:55+09:00 | 2026-09-25T13:16:55+09:00 | mryfmo / GitHub
d6cfed2 2026-09-25T13:18:26+09:00 | 2026-09-25T13:18:26+09:00 | mryfmo / mryfmo
01073f2 2026-09-25T14:01:48+09:00 | 2026-09-25T14:01:48+09:00 | mryfmo / mryfmo
3a8c7d3 2026-09-25T14:01:48+09:00 | 2026-09-25T14:01:48+09:00 | mryfmo / mryfmo
6775bb7 2026-09-25T14:02:37+09:00 | 2026-09-25T14:02:37+09:00 | mryfmo / mryfmo
127e27b 2026-09-25T14:27:46+09:00 | 2026-09-25T14:27:46+09:00 | mryfmo / mryfmo
d906b00 2026-09-25T14:31:30+09:00 | 2026-09-25T14:31:30+09:00 | mryfmo / mryfmo
b277a51 2026-09-25T15:17:39+09:00 | 2026-09-25T15:17:39+09:00 | mryfmo / GitHub
3303fbc 2026-09-25T15:18:04+09:00 | 2026-09-25T15:18:04+09:00 | mryfmo / mryfmo
```

### `git diff --stat 455455e 3303fbc | tail -1`

```text
 323 files changed, 172779 insertions(+), 26973 deletions(-)
```

### `git diff --stat 455455e 3303fbc -- . ':!.orchestration' ':!reviews' ':!.ua'`

```text
 .github/workflows/agent-assets.yml                 |   4 +-
 .github/workflows/docs.yml                         |   6 +-
 .github/workflows/macos.yaml                       |   4 +-
 .github/workflows/remote.yaml                      |   4 +-
 .github/workflows/test.yaml                        |  22 +--
 .github/workflows/ubuntu.yaml                      |   4 +-
 Dockerfile                                         |  12 +-
 Makefile                                           |  15 +-
 README.md                                          |  43 ++++--
 .../.chezmoitemplates/claude-settings-managed.json |   2 +-
 home/dot_agents/README.md                          |   2 +-
 home/dot_agents/agent-config.yaml                  |   2 +-
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   4 +-
 home/dot_config/herdr/config.toml                  |   5 +
 home/dot_config/mise/config.toml.tmpl              |   1 +
 home/dot_config/mise/mise.lock.tmpl                |   1 +
 home/dot_config/mise/symlink_config.toml.tmpl      |   1 -
 home/dot_config/mise/symlink_mise.lock.tmpl        |   1 -
 .../dot_local/bin/common/executable_agmsg-dispatch | 100 +++++++++++++
 home/dot_local/bin/common/executable_herdr-agents  |   1 +
 home/dot_mise/config.toml                          |  12 +-
 home/dot_mise/mise.lock                            |  60 ++++----
 home/dot_zshrc                                     |   1 +
 scripts/check-statusline-tools.py                  |   2 +-
 scripts/lib/installer-pins.sh                      |  12 +-
 scripts/update-agent-assets.sh                     |   8 +-
 scripts/upgrade-tools.sh                           |  23 ++-
 scripts/validate-agent-assets.py                   |  13 ++
 tests/install/common/lifecycle.bats                |  26 +++-
 tests/install/common/mise.bats                     |   2 +-
 tests/unit/test_agmsg_dispatch.py                  | 165 +++++++++++++++++++++
 tests/unit/test_claude_settings_merge.py           |  25 ++++
 tests/unit/test_herdr_agents.py                    |  14 ++
 tests/unit/test_runtime_health.py                  | 113 ++++++++++++++
 tests/unit/test_statusline_tools.py                |  10 +-
 tests/unit/test_supply_chain_policy.py             |  46 +++++-
 tests/unit/test_validate_agent_assets.py           |  33 +++++
 37 files changed, 692 insertions(+), 107 deletions(-)
```

### `git diff --numstat 455455e 3303fbc | awk '{split($3,a,"/"); d=(a[1] ~ /^(home|tests|scripts|\.github)$/ && a[2]!="") ? a[1]"/"a[2] : a[1]; add[d]+=$1; del[d]+=$2; n[d]++} END {for (d in n) printf "%-40s %4d files +%d -%d\n", d, n[d], add[d], del[d]}' | sort`

```text
.github/workflows                           6 files +22 -22
.orchestration                             84 files +19912 -0
.ua                                         4 files +38129 -26866
Dockerfile                                  1 files +8 -4
Makefile                                    1 files +13 -2
README.md                                   1 files +29 -14
home/.chezmoitemplates                      1 files +1 -1
home/dot_agents                             3 files +4 -4
home/dot_config                             5 files +7 -2
home/dot_local                              2 files +101 -0
home/dot_mise                               2 files +36 -36
home/dot_zshrc                              1 files +1 -0
reviews                                   198 files +114046 -0
scripts/check-statusline-tools.py           1 files +1 -1
scripts/lib                                 1 files +6 -6
scripts/update-agent-assets.sh              1 files +4 -4
scripts/upgrade-tools.sh                    1 files +22 -1
scripts/validate-agent-assets.py            1 files +13 -0
tests/install                               2 files +24 -4
tests/unit                                  7 files +400 -6
```

## 3. Per-commit `git show --stat` (27 commits, oldest first)

### `git show --stat=200 --format='%h %s' 3a530b1`

```text
3a530b1 Add files via upload

 PRD_ADR_BDD.zip | Bin 0 -> 166869 bytes
 TestSuite.zip   | Bin 0 -> 266316 bytes
 2 files changed, 0 insertions(+), 0 deletions(-)
```

### `git show --stat=200 --format='%h %s' 7e35d78`

```text
7e35d78 Delete PRD_ADR_BDD.zip

 PRD_ADR_BDD.zip | Bin 166869 -> 0 bytes
 1 file changed, 0 insertions(+), 0 deletions(-)
```

### `git show --stat=200 --format='%h %s' c5193e4`

```text
c5193e4 Delete TestSuite.zip

 TestSuite.zip | Bin 266316 -> 0 bytes
 1 file changed, 0 insertions(+), 0 deletions(-)
```

### `git show --stat=200 --format='%h %s' 22e5c9f`

```text
22e5c9f fix(update): converge herdr SessionStart matcher, report unmerged index, dedupe agmsg identities (#170)

 Makefile                                            |  4 +++-
 home/.chezmoitemplates/claude-settings-managed.json |  2 +-
 home/dot_agents/agent-config.yaml                   |  2 +-
 home/dot_agents/skills/agmsg-orchestration/SKILL.md |  2 +-
 home/dot_local/bin/common/executable_herdr-agents   |  1 +
 tests/install/common/lifecycle.bats                 | 10 ++++++++++
 tests/unit/test_claude_settings_merge.py            | 25 +++++++++++++++++++++++++
 tests/unit/test_herdr_agents.py                     | 14 ++++++++++++++
 tests/unit/test_runtime_health.py                   | 22 ++++++++++++++++++++++
 9 files changed, 78 insertions(+), 4 deletions(-)
```

### `git show --stat=200 --format='%h %s' d377ad0`

```text
d377ad0 chore(mise): upgrade tool pins via make upgrade (#171)

 .github/workflows/test.yaml         |  8 ++++----
 home/dot_mise/config.toml           | 12 ++++++------
 home/dot_mise/mise.lock             | 60 ++++++++++++++++++++++++++++++------------------------------
 scripts/check-statusline-tools.py   |  2 +-
 scripts/lib/installer-pins.sh       | 12 ++++++------
 tests/install/common/mise.bats      |  2 +-
 tests/unit/test_statusline_tools.py | 10 +++++-----
 7 files changed, 53 insertions(+), 53 deletions(-)
```

### `git show --stat=200 --format='%h %s' 0aafdb9`

```text
0aafdb9 Add files via upload

 jev-all-engines.zip | Bin 0 -> 17606234 bytes
 1 file changed, 0 insertions(+), 0 deletions(-)
```

### `git show --stat=200 --format='%h %s' f78666a`

```text
f78666a Delete jev-all-engines.zip

 jev-all-engines.zip | Bin 17606234 -> 0 bytes
 1 file changed, 0 insertions(+), 0 deletions(-)
```

### `git show --stat=200 --format='%h %s' cd61a88`

```text
cd61a88 fix(mise): stop make upgrade and mise from writing into the main checkout (#172)

 README.md                                     |  1 +
 home/dot_config/mise/config.toml.tmpl         |  1 +
 home/dot_config/mise/mise.lock.tmpl           |  1 +
 home/dot_config/mise/symlink_config.toml.tmpl |  1 -
 home/dot_config/mise/symlink_mise.lock.tmpl   |  1 -
 home/dot_zshrc                                |  1 +
 scripts/upgrade-tools.sh                      | 23 ++++++++++++++++++++++-
 tests/install/common/lifecycle.bats           |  4 ++--
 tests/unit/test_runtime_health.py             | 91 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/unit/test_supply_chain_policy.py        | 46 +++++++++++++++++++++++++++++++++++++++++++++-
 10 files changed, 164 insertions(+), 6 deletions(-)
```

### `git show --stat=200 --format='%h %s' c11035f`

```text
c11035f fix(update): tolerate a herdr protocol mismatch on reload; align docs and dev image (#174)

 Dockerfile                          | 12 ++++++++----
 Makefile                            | 11 ++++++++++-
 README.md                           | 42 ++++++++++++++++++++++++++++--------------
 home/dot_agents/README.md           |  2 +-
 scripts/update-agent-assets.sh      |  8 ++++----
 tests/install/common/lifecycle.bats | 12 +++++++++++-
 6 files changed, 62 insertions(+), 25 deletions(-)
```

### `git show --stat=200 --format='%h %s' c5240c3`

```text
c5240c3 feat(agmsg): add agmsg-dispatch to send, wake an idle worker, and verify receipt (#173)

 home/dot_agents/skills/agmsg-orchestration/SKILL.md |   2 +-
 home/dot_local/bin/common/executable_agmsg-dispatch | 100 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/unit/test_agmsg_dispatch.py                   | 165 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 266 insertions(+), 1 deletion(-)
```

### `git show --stat=200 --format='%h %s' f95074a`

```text
f95074a chore(orchestration): sync 2026-09-25 session (T1 convergence, T2 pins, T3 mise symlink, T4 agmsg-dispatch, T5 ua-refresh, herdr-sheldon a02)

 .orchestration/acceptance/dot-agmsg-dispatch-T4-a01.md         |   28 ++
 .orchestration/acceptance/dot-docs-align-T1-a01.md             |   16 +
 .orchestration/acceptance/dot-herdr-sheldon-T1-a01.md          |   16 +
 .orchestration/acceptance/dot-herdr-sheldon-T1-a02.md          |   16 +
 .orchestration/acceptance/dot-mise-symlink-T3-a01.md           |   31 ++
 .orchestration/acceptance/dot-ua-refresh-T5-a01.md             |   16 +
 .orchestration/acceptance/dot-update-convergence-T1-a01.md     |   36 ++
 .orchestration/acceptance/dot-upgrade-pins-T2-a01.md           |   30 ++
 .orchestration/autoskill/runs/dot-agmsg-dispatch-T4-a01.md     |    5 +
 .orchestration/autoskill/runs/dot-docs-align-T1-a01.md         |    3 +
 .orchestration/autoskill/runs/dot-herdr-sheldon-T1-a01.md      |    3 +
 .orchestration/autoskill/runs/dot-herdr-sheldon-T1-a02.md      |    2 +
 .orchestration/autoskill/runs/dot-mise-symlink-T3-a01.md       |    7 +
 .orchestration/autoskill/runs/dot-ua-refresh-T5-a01.md         |    5 +
 .orchestration/autoskill/runs/dot-update-convergence-T1-a01.md |    5 +
 .orchestration/autoskill/runs/dot-upgrade-pins-T2-a01.md       |    4 +
 .orchestration/learning/dot-agmsg-dispatch-T4-a01.md           |    5 +
 .orchestration/learning/dot-docs-align-T1-a01.md               |    5 +
 .orchestration/learning/dot-herdr-sheldon-T1-a01.md            |    3 +
 .orchestration/learning/dot-herdr-sheldon-T1-a02.md            |    2 +
 .orchestration/learning/dot-mise-symlink-T3-a01.md             |    8 +
 .orchestration/learning/dot-ua-refresh-T5-a01.md               |    5 +
 .orchestration/learning/dot-update-convergence-T1-a01.md       |    6 +
 .orchestration/learning/dot-upgrade-pins-T2-a01.md             |    6 +
 .orchestration/reports/dot-agmsg-dispatch-T4-a01.md            |   46 +++
 .orchestration/reports/dot-docs-align-T1-a01.md                |   33 ++
 .orchestration/reports/dot-herdr-sheldon-T1-a01.md             |   32 ++
 .orchestration/reports/dot-herdr-sheldon-T1-a02.md             |   25 ++
 .orchestration/reports/dot-mise-symlink-T3-a01.md              |   46 +++
 .orchestration/reports/dot-ua-refresh-T5-a01.md                |   47 +++
 .orchestration/reports/dot-update-convergence-T1-a01.md        |   31 ++
 .orchestration/reports/dot-upgrade-pins-T2-a01.md              |  113 ++++++
 .orchestration/sandboxes/dot-agmsg-dispatch-T4-a01.md          |    5 +
 .orchestration/sandboxes/dot-docs-align-T1-a01.md              |    9 +
 .orchestration/sandboxes/dot-herdr-sheldon-T1-a01.md           |    9 +
 .orchestration/sandboxes/dot-herdr-sheldon-T1-a02.md           |    2 +
 .orchestration/sandboxes/dot-mise-symlink-T3-a01.md            |    6 +
 .orchestration/sandboxes/dot-ua-refresh-T5-a01.md              |    5 +
 .orchestration/sandboxes/dot-update-convergence-T1-a01.md      |    4 +
 .orchestration/sandboxes/dot-upgrade-pins-T2-a01.md            |    3 +
 .orchestration/tasks/dot-agmsg-dispatch-T4-a01.md              |   46 +++
 .orchestration/tasks/dot-docs-align-T1-a01.md                  |   58 +++
 .orchestration/tasks/dot-herdr-sheldon-T1-a01.md               |   62 +++
 .orchestration/tasks/dot-herdr-sheldon-T1-a02.md               |   23 ++
 .orchestration/tasks/dot-mise-symlink-T3-a01.md                |   40 ++
 .orchestration/tasks/dot-ua-refresh-T5-a01.md                  |   20 +
 .orchestration/tasks/dot-update-convergence-T1-a01.md          |   80 ++++
 .orchestration/tasks/dot-upgrade-pins-T2-a01.md                |   29 ++
 .orchestration/validation/dot-agmsg-dispatch-T4-a01.md         | 1580 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 .orchestration/validation/dot-docs-align-T1-a01.md             |  188 +++++++++
 .orchestration/validation/dot-herdr-sheldon-T1-a01.md          |  154 ++++++++
 .orchestration/validation/dot-herdr-sheldon-T1-a02.md          |  714 +++++++++++++++++++++++++++++++++
 .orchestration/validation/dot-mise-symlink-T3-a01.md           | 2423 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 .orchestration/validation/dot-ua-refresh-T5-a01.md             |  211 ++++++++++
 .orchestration/validation/dot-update-convergence-T1-a01.md     | 2778 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 .orchestration/validation/dot-upgrade-pins-T2-a01.md           | 2321 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 56 files changed, 11406 insertions(+)
```

### `git show --stat=200 --format='%h %s' 60c1be4`

```text
60c1be4 chore(deps): bump cachix/install-nix-action from 31.10.7 to 31.11.1

 .github/workflows/test.yaml | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### `git show --stat=200 --format='%h %s' 3d6eb8d`

```text
3d6eb8d chore(deps): bump actions/checkout from 7.0.0 to 7.0.1

 .github/workflows/agent-assets.yml | 2 +-
 .github/workflows/docs.yml         | 2 +-
 .github/workflows/macos.yaml       | 2 +-
 .github/workflows/remote.yaml      | 4 ++--
 .github/workflows/test.yaml        | 6 +++---
 .github/workflows/ubuntu.yaml      | 2 +-
 6 files changed, 9 insertions(+), 9 deletions(-)
```

### `git show --stat=200 --format='%h %s' 01c8bdd`

```text
01c8bdd chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0

 .github/workflows/agent-assets.yml | 2 +-
 .github/workflows/docs.yml         | 2 +-
 .github/workflows/test.yaml        | 2 +-
 3 files changed, 3 insertions(+), 3 deletions(-)
```

### `git show --stat=200 --format='%h %s' cb28a55`

```text
cb28a55 chore(deps): bump jdx/mise-action from 4.2.0 to 4.3.0

 .github/workflows/docs.yml    | 2 +-
 .github/workflows/macos.yaml  | 2 +-
 .github/workflows/test.yaml   | 2 +-
 .github/workflows/ubuntu.yaml | 2 +-
 4 files changed, 4 insertions(+), 4 deletions(-)
```

### `git show --stat=200 --format='%h %s' 8276e9d`

```text
8276e9d fix(herdr): enable experimental kitty graphics for terminal tool panes (#146)

 home/dot_config/herdr/config.toml | 5 +++++
 1 file changed, 5 insertions(+)
```

### `git show --stat=200 --format='%h %s' efc2bb2`

```text
efc2bb2 chore(deps): bump codecov/codecov-action from 7.0.0 to 7.1.1 (#159)

 .github/workflows/test.yaml | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### `git show --stat=200 --format='%h %s' 5b4fd8b`

```text
5b4fd8b fix(validate): skip nested git worktrees in the repo-wide scans (#176)

 scripts/validate-agent-assets.py         | 13 +++++++++++++
 tests/unit/test_validate_agent_assets.py | 33 +++++++++++++++++++++++++++++++++
 2 files changed, 46 insertions(+)
```

### `git show --stat=200 --format='%h %s' 9baed29`

```text
9baed29 docs(adh): add the ADH Integrated Plan input baseline (#175)

 reviews/ADH_Integrated_Plan/CHANGELOG_JA.md                                                  |     9 +
 reviews/ADH_Integrated_Plan/DESIGN_JA.md                                                     |  2216 ++++++++
 reviews/ADH_Integrated_Plan/DOCUMENT_VALIDATION.md                                           |     5 +
 reviews/ADH_Integrated_Plan/INTEGRATED_PLAN_JA.md                                            | 13041 +++++++++++++++++++++++++++++++++++++++++++++
 reviews/ADH_Integrated_Plan/MODEL_OPTIMIZATION_JA.md                                         |    47 +
 reviews/ADH_Integrated_Plan/PACKAGE_MANIFEST.json                                            |   988 ++++
 reviews/ADH_Integrated_Plan/PLAN_QA.json                                                     |   501 ++
 reviews/ADH_Integrated_Plan/README_JA.md                                                     |     5 +
 reviews/ADH_Integrated_Plan/REVISION_GUIDE_JA.md                                             |    23 +
 reviews/ADH_Integrated_Plan/SHA256SUMS                                                       |   197 +
 reviews/ADH_Integrated_Plan/START_HERE.md                                                    |    32 +
 reviews/ADH_Integrated_Plan/artifacts/L10_EVAL.md                                            |    20 +
 reviews/ADH_Integrated_Plan/artifacts/L1_BRD.md                                              |    24 +
 reviews/ADH_Integrated_Plan/artifacts/L2_PRD.md                                              |    32 +
 reviews/ADH_Integrated_Plan/artifacts/L3_REQ.md                                              |   318 ++
 reviews/ADH_Integrated_Plan/artifacts/L4_ACCEPTANCE.md                                       |   423 ++
 reviews/ADH_Integrated_Plan/artifacts/L5_ARCH_ADR.md                                         |    37 +
 reviews/ADH_Integrated_Plan/artifacts/L6_SPEC.md                                             |    24 +
 reviews/ADH_Integrated_Plan/artifacts/L7_TEST.md                                             |    22 +
 reviews/ADH_Integrated_Plan/artifacts/L8_IPLAN.md                                            |    16 +
 reviews/ADH_Integrated_Plan/artifacts/L9_CHG.md                                              |    12 +
 reviews/ADH_Integrated_Plan/artifacts/README.md                                              |    18 +
 reviews/ADH_Integrated_Plan/contracts/OPERATION_INDEX.md                                     |    44 +
 reviews/ADH_Integrated_Plan/contracts/STACK_CONTRACT_NOTES.md                                |    15 +
 reviews/ADH_Integrated_Plan/contracts/document-graph.schema.json                             |   146 +
 reviews/ADH_Integrated_Plan/contracts/guardrails.schema.json                                 |   371 ++
 reviews/ADH_Integrated_Plan/contracts/model-execution.schema.json                            |   909 ++++
 reviews/ADH_Integrated_Plan/contracts/operation_inventory.json                               |   298 ++
 reviews/ADH_Integrated_Plan/contracts/requirements.json                                      |   247 +
 reviews/ADH_Integrated_Plan/contracts/stack-integration.schema.json                          |   660 +++
 reviews/ADH_Integrated_Plan/docs/00_WBS_INDEX.md                                             |    38 +
 reviews/ADH_Integrated_Plan/docs/01_SCOPE_AND_BASELINE.md                                    |    52 +
 reviews/ADH_Integrated_Plan/docs/02_ROLES_AND_AGMSG.md                                       |    76 +
 reviews/ADH_Integrated_Plan/docs/03_BOOTSTRAP_AND_RUN_ORDER.md                               |    95 +
 reviews/ADH_Integrated_Plan/docs/04_SPECIFICATION_COMPLETIONS.md                             |    59 +
 reviews/ADH_Integrated_Plan/docs/05_VERIFICATION_STANDARD.md                                 |    84 +
 reviews/ADH_Integrated_Plan/docs/06_ENVIRONMENT_AND_NATIVE.md                                |    86 +
 reviews/ADH_Integrated_Plan/docs/07_COMPLETION_AND_RELEASE.md                                |    89 +
 reviews/ADH_Integrated_Plan/docs/08_CODING_AND_COMMANDS.md                                   |    61 +
 reviews/ADH_Integrated_Plan/docs/09_RECOVERY_AND_HANDOFF.md                                  |    60 +
 reviews/ADH_Integrated_Plan/docs/10_API_COMPLETION_PLAN.md                                   |    64 +
 reviews/ADH_Integrated_Plan/docs/11_ACCEPTANCE_FIXTURES.md                                   |    60 +
 reviews/ADH_Integrated_Plan/docs/12_DOCUMENT_USE_AND_DELIVERY.md                             |    16 +
 reviews/ADH_Integrated_Plan/docs/13_TASK_PROTOCOL_AND_CHECKPOINT.md                          |    66 +
 reviews/ADH_Integrated_Plan/docs/14_MODEL_CONTEXT_AND_SKILLS.md                              |    35 +
 reviews/ADH_Integrated_Plan/docs/15_MODEL_EVALUATION_AND_ROLLOUT.md                          |    19 +
 reviews/ADH_Integrated_Plan/docs/16_V4_RUNBOOK.md                                            |    35 +
 reviews/ADH_Integrated_Plan/docs/17_COMPONENT_CATALOG.md                                     |   597 +++
 reviews/ADH_Integrated_Plan/evaluation/DOCUMENT_GUARDRAIL_PROTOCOL.md                        |    40 +
 reviews/ADH_Integrated_Plan/evaluation/EXPERIMENT_PROTOCOL.md                                |    75 +
 reviews/ADH_Integrated_Plan/evaluation/V4_INTEGRATION_PROTOCOL.md                            |    29 +
 reviews/ADH_Integrated_Plan/evaluation/control_prompts/CLAUDE_LEAD.md                        |    32 +
 reviews/ADH_Integrated_Plan/evaluation/control_prompts/CLAUDE_REVIEWER.md                    |    24 +
 reviews/ADH_Integrated_Plan/evaluation/control_prompts/CODEX_WORKER.md                       |    28 +
 reviews/ADH_Integrated_Plan/evaluation/control_prompts/VERIFIER_RUNBOOK.md                   |    24 +
 reviews/ADH_Integrated_Plan/evaluation/knowledge_cases.json                                  |   165 +
 reviews/ADH_Integrated_Plan/evaluation/quality_cases.json                                    |   136 +
 reviews/ADH_Integrated_Plan/evaluation/run_matrix.json                                       |  1523 ++++++
 reviews/ADH_Integrated_Plan/evaluation/skill-routing-cases.json                              |   776 +++
 reviews/ADH_Integrated_Plan/evaluation/stack_skill_routing_cases.json                        |   202 +
 reviews/ADH_Integrated_Plan/examples/README.md                                               |    11 +
 reviews/ADH_Integrated_Plan/examples/guard_decision.example.json                             |    31 +
 reviews/ADH_Integrated_Plan/examples/guard_qualification.example.json                        |    13 +
 reviews/ADH_Integrated_Plan/examples/model_profile.example.json                              |    24 +
 reviews/ADH_Integrated_Plan/examples/operation_intent.example.json                           |    19 +
 reviews/ADH_Integrated_Plan/examples/stack_KnowledgeQuery.example.json                       |    22 +
 reviews/ADH_Integrated_Plan/examples/stack_LearningCandidate.example.json                    |    14 +
 reviews/ADH_Integrated_Plan/examples/stack_QualityPlan.example.json                          |    22 +
 reviews/ADH_Integrated_Plan/examples/stack_ReleaseSet.example.json                           |    22 +
 reviews/ADH_Integrated_Plan/examples/task_packet.example.json                                |   105 +
 reviews/ADH_Integrated_Plan/profiles/README.md                                               |     5 +
 reviews/ADH_Integrated_Plan/profiles/model_profiles.json                                     |    96 +
 reviews/ADH_Integrated_Plan/prompts/CLAUDE_LEAD.md                                           |    18 +
 reviews/ADH_Integrated_Plan/prompts/CLAUDE_REVIEWER.md                                       |    16 +
 reviews/ADH_Integrated_Plan/prompts/CODEX_WORKER.md                                          |    18 +
 reviews/ADH_Integrated_Plan/prompts/COMMON_CONTRACT.md                                       |    14 +
 reviews/ADH_Integrated_Plan/prompts/VERIFIER_RUNBOOK.md                                      |    16 +
 reviews/ADH_Integrated_Plan/registers/acceptance_scenarios.json                              |   653 +++
 reviews/ADH_Integrated_Plan/registers/artifact_catalog.json                                  |    98 +
 reviews/ADH_Integrated_Plan/registers/artifact_graph.json                                    | 28120 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reviews/ADH_Integrated_Plan/registers/authority_map.json                                     |   249 +
 reviews/ADH_Integrated_Plan/registers/component_catalog.json                                 |   663 +++
 reviews/ADH_Integrated_Plan/registers/cross_contract_flows.json                              |   256 +
 reviews/ADH_Integrated_Plan/registers/document_contracts.json                                |   357 ++
 reviews/ADH_Integrated_Plan/registers/document_guardrail_test_mapping.json                   |  2773 ++++++++++
 reviews/ADH_Integrated_Plan/registers/execution_status.json                                  |   568 ++
 reviews/ADH_Integrated_Plan/registers/generated_views.json                                   |   336 ++
 reviews/ADH_Integrated_Plan/registers/guard_applicability.json                               |   282 +
 reviews/ADH_Integrated_Plan/registers/guardrails.json                                        |  2071 ++++++++
 reviews/ADH_Integrated_Plan/registers/integrated_contracts.json                              |  1731 ++++++
 reviews/ADH_Integrated_Plan/registers/integration_traceability.json                          |  1098 ++++
 reviews/ADH_Integrated_Plan/registers/legacy_addon_mapping.json                              |   902 ++++
 reviews/ADH_Integrated_Plan/registers/model_optimization_contracts.json                      |   865 +++
 reviews/ADH_Integrated_Plan/registers/model_optimization_traceability.json                   |   393 ++
 reviews/ADH_Integrated_Plan/registers/phases.json                                            |    82 +
 reviews/ADH_Integrated_Plan/registers/prior_findings.json                                    |   331 ++
 reviews/ADH_Integrated_Plan/registers/requirement_traceability.json                          |  4805 +++++++++++++++++
 reviews/ADH_Integrated_Plan/registers/revision_delta.json                                    |   348 ++
 reviews/ADH_Integrated_Plan/registers/runtime_requirements.json                              |    33 +
 reviews/ADH_Integrated_Plan/registers/skill_routes.json                                      |   171 +
 reviews/ADH_Integrated_Plan/registers/source_check_mapping.json                              |   288 +
 reviews/ADH_Integrated_Plan/registers/structured_requirements.json                           |   619 +++
 reviews/ADH_Integrated_Plan/registers/upstream_instruction_adaptation.json                   |   214 +
 reviews/ADH_Integrated_Plan/registers/v4_integration_checks.json                             |   343 ++
 reviews/ADH_Integrated_Plan/registers/verification_cases.json                                | 10138 +++++++++++++++++++++++++++++++++++
 reviews/ADH_Integrated_Plan/registers/work_packages.json                                     |  6810 ++++++++++++++++++++++++
 reviews/ADH_Integrated_Plan/skill-pack/README.md                                             |    16 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-design-choice/SKILL.md                     |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-design-choice/references/workflow.md       |    13 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-environment-repair/SKILL.md                |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-environment-repair/references/workflow.md  |    13 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-failure-diagnosis/SKILL.md                 |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-failure-diagnosis/references/workflow.md   |    13 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-independent-review/SKILL.md                |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-independent-review/references/workflow.md  |    13 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-integration-review/SKILL.md                |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-integration-review/references/workflow.md  |    13 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-knowledge-context/SKILL.md                 |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-knowledge-context/references/workflow.md   |     7 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-quality-check/SKILL.md                     |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-quality-check/references/workflow.md       |     7 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-requirements/SKILL.md                      |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-requirements/references/workflow.md        |    13 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-schema-migration/SKILL.md                  |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-schema-migration/references/workflow.md    |    13 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-task-implementation/SKILL.md               |    10 +
 reviews/ADH_Integrated_Plan/skill-pack/skills/adh-task-implementation/references/workflow.md |    13 +
 reviews/ADH_Integrated_Plan/sources/DOCUMENT_GUARDRAIL_SOURCES.md                            |    20 +
 reviews/ADH_Integrated_Plan/sources/MODEL_SOURCES.md                                         |    51 +
 reviews/ADH_Integrated_Plan/sources/README.md                                                |    50 +
 reviews/ADH_Integrated_Plan/sources/V4_SOURCES.md                                            |   147 +
 reviews/ADH_Integrated_Plan/sources/api_v1_snapshot.json                                     |  3034 +++++++++++
 reviews/ADH_Integrated_Plan/sources/document_guardrail_sources.json                          |   150 +
 reviews/ADH_Integrated_Plan/sources/dsh_sources.json                                         |   178 +
 reviews/ADH_Integrated_Plan/sources/input_provenance.json                                    |    42 +
 reviews/ADH_Integrated_Plan/sources/model_optimization_sources.json                          |   118 +
 reviews/ADH_Integrated_Plan/sources/prior_source_index.json                                  |   106 +
 reviews/ADH_Integrated_Plan/sources/v2_integration_delta_history.json                        |  1332 +++++
 reviews/ADH_Integrated_Plan/sources/v3_input_provenance.json                                 |    13 +
 reviews/ADH_Integrated_Plan/sources/v4_input_provenance.json                                 |    23 +
 reviews/ADH_Integrated_Plan/sources/v4_sources.json                                          |   172 +
 reviews/ADH_Integrated_Plan/spec/00_DECISION.md                                              |    31 +
 reviews/ADH_Integrated_Plan/spec/01_REQUIREMENTS.md                                          |    60 +
 reviews/ADH_Integrated_Plan/spec/02_ARCHITECTURE.md                                          |    97 +
 reviews/ADH_Integrated_Plan/spec/03_INTEGRATED_CONTRACTS.md                                  |   526 ++
 reviews/ADH_Integrated_Plan/spec/04_STATE_SEQUENCES.md                                       |    74 +
 reviews/ADH_Integrated_Plan/spec/05_OPERATIONS_NFR.md                                        |    56 +
 reviews/ADH_Integrated_Plan/spec/06_MODEL_OPTIMIZATION.md                                    |   117 +
 reviews/ADH_Integrated_Plan/spec/07_MODEL_CONTRACTS.md                                       |   175 +
 reviews/ADH_Integrated_Plan/spec/08_DOCUMENT_GRAPH.md                                        |   133 +
 reviews/ADH_Integrated_Plan/spec/09_GUARDRAILS.md                                            |   622 +++
 reviews/ADH_Integrated_Plan/spec/10_CHANGE_AND_REGATE.md                                     |    35 +
 reviews/ADH_Integrated_Plan/spec/11_DISTRIBUTION_AND_COMPOSITION.md                          |    51 +
 reviews/ADH_Integrated_Plan/spec/12_KNOWLEDGE_AND_CONTEXT.md                                 |    43 +
 reviews/ADH_Integrated_Plan/spec/13_QUALITY_AND_TOOLCHAIN.md                                 |    51 +
 reviews/ADH_Integrated_Plan/spec/14_LIFECYCLE_LEARNING_AND_REGATE.md                         |    35 +
 reviews/ADH_Integrated_Plan/traceability/DOCUMENT_AND_GUARDRAILS.md                          |    41 +
 reviews/ADH_Integrated_Plan/traceability/DOCUMENT_GRAPH.md                                   |     5 +
 reviews/ADH_Integrated_Plan/traceability/GUARDRAIL_MATRIX.md                                 |    30 +
 reviews/ADH_Integrated_Plan/traceability/INTEGRATION_PROVENANCE.md                           |    24 +
 reviews/ADH_Integrated_Plan/traceability/MODEL_OPTIMIZATION.md                               |    16 +
 reviews/ADH_Integrated_Plan/traceability/PRIOR_FINDINGS.md                                   |    24 +
 reviews/ADH_Integrated_Plan/traceability/REQUIREMENTS.md                                     |    41 +
 reviews/ADH_Integrated_Plan/traceability/V4_INTEGRATION_MAP.md                               |   116 +
 reviews/ADH_Integrated_Plan/verification/VERIFICATION_CATALOG.md                             |  5483 +++++++++++++++++++
 reviews/ADH_Integrated_Plan/verification/VERIFICATION_INDEX.md                               |   198 +
 reviews/ADH_Integrated_Plan/work_packages/WP00.md                                            |   191 +
 reviews/ADH_Integrated_Plan/work_packages/WP01.md                                            |   204 +
 reviews/ADH_Integrated_Plan/work_packages/WP02.md                                            |   228 +
 reviews/ADH_Integrated_Plan/work_packages/WP03.md                                            |   265 +
 reviews/ADH_Integrated_Plan/work_packages/WP04.md                                            |   268 +
 reviews/ADH_Integrated_Plan/work_packages/WP05.md                                            |   193 +
 reviews/ADH_Integrated_Plan/work_packages/WP06.md                                            |   368 ++
 reviews/ADH_Integrated_Plan/work_packages/WP07.md                                            |   221 +
 reviews/ADH_Integrated_Plan/work_packages/WP08.md                                            |   291 +
 reviews/ADH_Integrated_Plan/work_packages/WP09.md                                            |   242 +
 reviews/ADH_Integrated_Plan/work_packages/WP10.md                                            |   254 +
 reviews/ADH_Integrated_Plan/work_packages/WP11.md                                            |   210 +
 reviews/ADH_Integrated_Plan/work_packages/WP12.md                                            |   210 +
 reviews/ADH_Integrated_Plan/work_packages/WP13.md                                            |   250 +
 reviews/ADH_Integrated_Plan/work_packages/WP14.md                                            |   377 ++
 reviews/ADH_Integrated_Plan/work_packages/WP15.md                                            |   270 +
 reviews/ADH_Integrated_Plan/work_packages/WP16.md                                            |   230 +
 reviews/ADH_Integrated_Plan/work_packages/WP17.md                                            |   294 ++
 reviews/ADH_Integrated_Plan/work_packages/WP18.md                                            |   310 ++
 reviews/ADH_Integrated_Plan/work_packages/WP19.md                                            |   242 +
 reviews/ADH_Integrated_Plan/work_packages/WP20.md                                            |   307 ++
 reviews/ADH_Integrated_Plan/work_packages/WP21.md                                            |   257 +
 reviews/ADH_Integrated_Plan/work_packages/WP22.md                                            |   336 ++
 reviews/ADH_Integrated_Plan/work_packages/WP23.md                                            |   263 +
 reviews/ADH_Integrated_Plan/work_packages/WP24.md                                            |   337 ++
 reviews/ADH_Integrated_Plan/work_packages/WP25.md                                            |   348 ++
 reviews/ADH_Integrated_Plan/work_packages/WP26.md                                            |   465 ++
 reviews/ADH_Integrated_Plan/work_packages/WP27.md                                            |   171 +
 reviews/ADH_Integrated_Plan/work_packages/WP28.md                                            |   359 ++
 reviews/ADH_Integrated_Plan/work_packages/WP29.md                                            |   309 ++
 reviews/ADH_Integrated_Plan/work_packages/WP30.md                                            |   330 ++
 reviews/ADH_Integrated_Plan/work_packages/WP31.md                                            |   283 +
 198 files changed, 114046 insertions(+)
```

### `git show --stat=200 --format='%h %s' d6cfed2`

```text
d6cfed2 chore(orchestration): sync T6 adh-baseline and T7 validator-worktrees records

 .orchestration/acceptance/dot-adh-baseline-T6-a01.md            |   9 ++
 .orchestration/acceptance/dot-validator-worktrees-T7-a01.md     |  11 ++
 .orchestration/autoskill/runs/dot-adh-baseline-T6-a01.md        |   5 +
 .orchestration/autoskill/runs/dot-validator-worktrees-T7-a01.md |   2 +
 .orchestration/learning/dot-adh-baseline-T6-a01.md              |   5 +
 .orchestration/learning/dot-validator-worktrees-T7-a01.md       |   2 +
 .orchestration/reports/dot-adh-baseline-T6-a01.md               |  36 ++++++
 .orchestration/reports/dot-validator-worktrees-T7-a01.md        |  23 ++++
 .orchestration/sandboxes/dot-adh-baseline-T6-a01.md             |   5 +
 .orchestration/sandboxes/dot-validator-worktrees-T7-a01.md      |   2 +
 .orchestration/tasks/dot-adh-baseline-T6-a01.md                 |  22 ++++
 .orchestration/tasks/dot-validator-worktrees-T7-a01.md          |  29 +++++
 .orchestration/validation/dot-adh-baseline-T6-a01.md            | 877 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 .orchestration/validation/dot-validator-worktrees-T7-a01.md     | 665 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 14 files changed, 1693 insertions(+)
```

### `git show --stat=200 --format='%h %s' 01073f2`

```text
01073f2 chore(deps): bump actions/checkout from 7.0.0 to 7.0.1 (#103)

 .github/workflows/agent-assets.yml | 2 +-
 .github/workflows/docs.yml         | 2 +-
 .github/workflows/macos.yaml       | 2 +-
 .github/workflows/remote.yaml      | 4 ++--
 .github/workflows/test.yaml        | 6 +++---
 .github/workflows/ubuntu.yaml      | 2 +-
 6 files changed, 9 insertions(+), 9 deletions(-)
```

### `git show --stat=200 --format='%h %s' 3a8c7d3`

```text
3a8c7d3 chore(deps): bump jdx/mise-action from 4.2.0 to 4.3.0 (#154)

 .github/workflows/docs.yml    | 2 +-
 .github/workflows/macos.yaml  | 2 +-
 .github/workflows/test.yaml   | 2 +-
 .github/workflows/ubuntu.yaml | 2 +-
 4 files changed, 4 insertions(+), 4 deletions(-)
```

### `git show --stat=200 --format='%h %s' 6775bb7`

```text
6775bb7 chore(orchestration): sync T8 dependabot-verify records

 .orchestration/acceptance/dot-dependabot-verify-T8-a01.md     |   10 +
 .orchestration/autoskill/runs/dot-dependabot-verify-T8-a01.md |    4 +
 .orchestration/learning/dot-dependabot-verify-T8-a01.md       |    4 +
 .orchestration/reports/dot-dependabot-verify-T8-a01.md        |   59 +++
 .orchestration/sandboxes/dot-dependabot-verify-T8-a01.md      |    4 +
 .orchestration/tasks/dot-dependabot-verify-T8-a01.md          |   26 ++
 .orchestration/validation/dot-dependabot-verify-T8-a01.md     | 2953 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 7 files changed, 3060 insertions(+)
```

### `git show --stat=200 --format='%h %s' 127e27b`

```text
127e27b chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0 (#155)

 .github/workflows/agent-assets.yml | 2 +-
 .github/workflows/docs.yml         | 2 +-
 .github/workflows/test.yaml        | 2 +-
 3 files changed, 3 insertions(+), 3 deletions(-)
```

### `git show --stat=200 --format='%h %s' d906b00`

```text
d906b00 chore(deps): bump cachix/install-nix-action from 31.10.7 to 31.11.1 (#125)

 .github/workflows/test.yaml | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

### `git show --stat=200 --format='%h %s' b277a51`

```text
b277a51 chore(ua): full knowledge-graph rebuild at d906b00; exclude .orchestration and reviews (#177)

 .ua/.understandignore    |     2 +
 .ua/fingerprints.json    | 20691 ++++++++++++++++++++++++++++++++++-------------------------------------------
 .ua/knowledge-graph.json | 44294 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------
 .ua/meta.json            |     8 +-
 4 files changed, 38129 insertions(+), 26866 deletions(-)
```

### `git show --stat=200 --format='%h %s' 3303fbc`

```text
3303fbc chore(orchestration): sync T9 ua-full-rebuild records

 .orchestration/acceptance/dot-ua-full-T9-a01.md     |    9 +
 .orchestration/autoskill/runs/dot-ua-full-T9-a01.md |    3 +
 .orchestration/learning/dot-ua-full-T9-a01.md       |    7 +
 .orchestration/reports/dot-ua-full-T9-a01.md        |   65 +++
 .orchestration/sandboxes/dot-ua-full-T9-a01.md      |    3 +
 .orchestration/tasks/dot-ua-full-T9-a01.md          |   21 +
 .orchestration/validation/dot-ua-full-T9-a01.md     | 3645 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 7 files changed, 3753 insertions(+)
```

## 4. Merge commits: no manual resolution (combined diff line count)

### `for m in 01073f2 3a8c7d3 127e27b d906b00; do echo "$m parents=$(git log -1 --format=%p $m) cc-lines=$(git show --cc --format= $m | wc -l)"; done`

```text
01073f2 parents=d6cfed2 3d6eb8d cc-lines=0
3a8c7d3 parents=01073f2 cb28a55 cc-lines=0
127e27b parents=6775bb7 01c8bdd cc-lines=0
d906b00 parents=127e27b 60c1be4 cc-lines=0
```

### `git log -1 --format=%B 01c8bdd`

```text
chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0

Bumps [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv) from 7.6.0 to 10.2.0.
- [Release notes](https://github.com/astral-sh/setup-uv/releases)
- [Commits](https://github.com/astral-sh/setup-uv/compare/37802adc94f370d6bfd71619e3f0bf239e1f3b78...c18668ad3cf93ea998bef934396af7bb5c839dc7)

---
updated-dependencies:
- dependency-name: astral-sh/setup-uv
  dependency-version: 10.1.0
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] <support@github.com>
```

## 5. Dependabot pin before/after

### `for h in 60c1be4 3d6eb8d 01c8bdd cb28a55 efc2bb2; do echo "== $(git log -1 --format='%h %s' $h)"; git show --format= -U0 $h | grep -E '^(\+\+\+|[-+] )'; done`

```text
== 60c1be4 chore(deps): bump cachix/install-nix-action from 31.10.7 to 31.11.1
+++ b/.github/workflows/test.yaml
-        uses: cachix/install-nix-action@a49548c11d9846ad46ecc0115273879b045f001c # v31
+        uses: cachix/install-nix-action@13d8dd58da0234aa297dedd986986ccb8e7f3e24 # v31
== 3d6eb8d chore(deps): bump actions/checkout from 7.0.0 to 7.0.1
+++ b/.github/workflows/agent-assets.yml
-        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+++ b/.github/workflows/docs.yml
-        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+++ b/.github/workflows/macos.yaml
-        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+++ b/.github/workflows/remote.yaml
-      - uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
-      - uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+++ b/.github/workflows/test.yaml
-        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
-        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
-        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+++ b/.github/workflows/ubuntu.yaml
-        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
== 01c8bdd chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0
+++ b/.github/workflows/agent-assets.yml
-        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
+        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+++ b/.github/workflows/docs.yml
-        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
+        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+++ b/.github/workflows/test.yaml
-        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
+        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
== cb28a55 chore(deps): bump jdx/mise-action from 4.2.0 to 4.3.0
+++ b/.github/workflows/docs.yml
-        uses: jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d # v4
+        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+++ b/.github/workflows/macos.yaml
-      - uses: jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d # v4
+      - uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+++ b/.github/workflows/test.yaml
-        uses: jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d # v4
+        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+++ b/.github/workflows/ubuntu.yaml
-      - uses: jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d # v4
+      - uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
== efc2bb2 chore(deps): bump codecov/codecov-action from 7.0.0 to 7.1.1 (#159)
+++ b/.github/workflows/test.yaml
-        uses: codecov/codecov-action@fb8b3582c8e4def4969c97caa2f19720cb33a72f # v7
+        uses: codecov/codecov-action@303a32d7a59b442fa8d48b6a1cc6825c09c847a5 # v7
```

## 6. Zip blobs

### `for h in 3a530b1 7e35d78 c5193e4 0aafdb9 f78666a; do git show --raw --format="%h %s" $h; done`

```text
3a530b1 Add files via upload

:000000 100644 0000000 2f6540e A	PRD_ADR_BDD.zip
:000000 100644 0000000 22536c5 A	TestSuite.zip
7e35d78 Delete PRD_ADR_BDD.zip

:100644 000000 2f6540e 0000000 D	PRD_ADR_BDD.zip
c5193e4 Delete TestSuite.zip

:100644 000000 22536c5 0000000 D	TestSuite.zip
0aafdb9 Add files via upload

:000000 100644 0000000 049a02e A	jev-all-engines.zip
f78666a Delete jev-all-engines.zip

:100644 000000 049a02e 0000000 D	jev-all-engines.zip
```

### `for spec in 3a530b1:PRD_ADR_BDD.zip 3a530b1:TestSuite.zip 0aafdb9:jev-all-engines.zip; do b=$(git rev-parse $spec); echo "$spec blob=$b size=$(git cat-file -s $b)"; git log --all --format="  %h %s" --find-object=$b; done`

```text
3a530b1:PRD_ADR_BDD.zip blob=2f6540e873e60e1cdec40ac3822219f29f3ca755 size=166869
  7e35d78 Delete PRD_ADR_BDD.zip
  3a530b1 Add files via upload
  d3281de feat(references): import documentation kit v3 as the v4 baseline tree
3a530b1:TestSuite.zip blob=22536c53365c5af36cccc96932f65a8c26485dcb size=266316
  c5193e4 Delete TestSuite.zip
  3a530b1 Add files via upload
  d3281de feat(references): import documentation kit v3 as the v4 baseline tree
0aafdb9:jev-all-engines.zip blob=049a02e95400e085d81abb05ec7a23b7b5021655 size=17606234
  f78666a Delete jev-all-engines.zip
  0aafdb9 Add files via upload
```

### `git branch -a --contains d3281de; git show --raw --format="%h %cI %s" d3281de | grep -E "d3281de|2f6540e|22536c5"`

```text
+ feat/references-kit-v4
+ feat/references-kit-v4-p3
d3281de 2026-09-23T18:28:37+09:00 feat(references): import documentation kit v3 as the v4 baseline tree
:000000 100644 0000000 2f6540e A	references/archive/PRD_ADR_BDD.zip
:000000 100644 0000000 22536c5 A	references/archive/TestSuite.zip
```

### `git ls-tree -r 3303fbc --name-only | grep -i '\.zip$'; git diff --quiet 455455e 3303fbc -- archive && echo 'archive unchanged in range'`

```text
archive/CompactionDB-2.0.0.zip
archive unchanged in range
```

## 7. W1/W2 fork point, overlap, merge-tree

### `git -C /home/moriya/Workspace/dotfiles-w1 log -1 --format="W1 %H %s" HEAD; git -C /home/moriya/Workspace/dotfiles-w2 log -1 --format="W2 %H %s" HEAD`

```text
W1 126e465c99d1dc6f90b9f48d57ada0b3f0391e14 merge: integrate PRD/ADR/BDD/test-doc remediation (refkit-P3, P4, P5, P7, P0-05) into feat/references-kit-v4
W2 3af64f0bb9c0d987b03c0926e382c61e71a36823 docs(references): reconcile conventions and common docs with the integrated kit v4 (part 2)
```

### `git merge-base 3303fbc 126e465; git merge-base 3303fbc 3af64f0; git merge-base --is-ancestor 126e465 3af64f0 && echo "126e465 is ancestor of 3af64f0"`

```text
455455ef8b53eefb49bfadb679600c30485eaf26
455455ef8b53eefb49bfadb679600c30485eaf26
126e465 is ancestor of 3af64f0
```

### `for w in 126e465 3af64f0; do echo "== overlap 455455e..3303fbc vs 455455e..$w"; comm -12 <(git diff --name-only 455455e 3303fbc | sort) <(git diff --name-only 455455e $w | sort); done; git diff --stat 126e465 3af64f0 -- home/dot_agents/agent-config.yaml scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py; echo "W2-over-W1 diff on 3 files: exit=$?"`

```text
== overlap 455455e..3303fbc vs 455455e..126e465
home/dot_agents/agent-config.yaml
scripts/validate-agent-assets.py
tests/unit/test_validate_agent_assets.py
== overlap 455455e..3303fbc vs 455455e..3af64f0
home/dot_agents/agent-config.yaml
scripts/validate-agent-assets.py
tests/unit/test_validate_agent_assets.py
W2-over-W1 diff on 3 files: exit=0
```

### `git merge-tree --write-tree --name-only 3303fbc 3af64f0; echo exit=$?`

```text
b43e36b7b68443222ff15227929dc64930572c12
exit=0
```

### `git merge-tree --write-tree --name-only 3303fbc 126e465; echo exit=$?`

```text
9f6de75883ea7737f2bb5561b9ead737581d2adf
exit=0
```

### `for t in b43e36b 9f6de75; do echo "tree $t:"; for f in home/dot_agents/agent-config.yaml scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py; do echo "  $(git rev-parse $t:$f) $f"; done; done`

```text
tree b43e36b:
  83143e58f4cfa6b4b4b2055965735d5633eb43c2 home/dot_agents/agent-config.yaml
  fe96abf899942f413d0a3567c2e062513b758d79 scripts/validate-agent-assets.py
  30b944130dfb67ebf7240efcb6fd6fe033a74ab1 tests/unit/test_validate_agent_assets.py
tree 9f6de75:
  83143e58f4cfa6b4b4b2055965735d5633eb43c2 home/dot_agents/agent-config.yaml
  fe96abf899942f413d0a3567c2e062513b758d79 scripts/validate-agent-assets.py
  30b944130dfb67ebf7240efcb6fd6fe033a74ab1 tests/unit/test_validate_agent_assets.py
```

### `git show b43e36b:scripts/validate-agent-assets.py | grep -n -E '^def (is_nested_git_tree|validate_no_removed_claude_skill|git_visible_files|validate_no_obvious_secrets)|^@cache|^from functools'`

```text
11:from functools import cache
1044:@cache
1045:def is_nested_git_tree(directory: Path) -> bool:
1052:def validate_no_removed_claude_skill() -> None:
1086:def git_visible_files(root: Path) -> list[Path] | None:
1114:def validate_no_obvious_secrets() -> None:
```

### `git show b43e36b:tests/unit/test_validate_agent_assets.py | grep -n -E 'def (test_recursive_scans_skip_nested_git_trees_only|test_agent_manifest_rejects_missing_remediation_profile|test_secret_scan_ignores_gitignored_files|test_secret_scan_checks_git_visible_files)'`

```text
48:    def test_recursive_scans_skip_nested_git_trees_only(self) -> None:
229:    def test_agent_manifest_rejects_missing_remediation_profile(self) -> None:
530:    def test_secret_scan_ignores_gitignored_files(self) -> None:
538:    def test_secret_scan_checks_git_visible_files(self) -> None:
```

### `git check-ignore -v .claude/worktrees/x`

```text
.git/info/exclude:11:**/.claude/worktrees/	.claude/worktrees/x
```

## 8. GitHub timeline

### `gh api 'repos/mryfmo/dotfiles/events?per_page=40' --jq '.[] | select(.type=="PushEvent" or .type=="PullRequestEvent") | [.created_at, .type, (.payload.action // ""), (.payload.ref // ""), (.payload.before // "" | .[0:7]), (.payload.head // "" | .[0:7]), ((.payload.number // .payload.pull_request.number // "")|tostring)] | @tsv' | sort`

```text
2026-09-25T00:50:44Z	PushEvent		refs/heads/fix/update-convergence	e3ca2b8	1b822f2	
2026-09-25T00:50:46Z	PushEvent		refs/heads/chore/upgrade-pins	8c67b3a	73a03ae	
2026-09-25T00:59:40Z	PushEvent		refs/heads/main	c5193e4	22e5c9f	
2026-09-25T01:00:55Z	PushEvent		refs/heads/gh-pages	27e1f42	b8483df	
2026-09-25T01:25:41Z	PushEvent		refs/heads/fix/mise-config-not-live-symlink	124c089	e914b82	
2026-09-25T01:29:32Z	PushEvent		refs/heads/main	d377ad0	0aafdb9	
2026-09-25T03:54:28Z	PushEvent		refs/heads/dependabot/github_actions/cachix/install-nix-action-31.11.1	379a6f2	60c1be4	
2026-09-25T03:54:39Z	PushEvent		refs/heads/dependabot/github_actions/astral-sh/setup-uv-10.1.0	1b1b976	01c8bdd	
2026-09-25T04:02:03Z	PushEvent		refs/heads/main	f95074a	8276e9d	
2026-09-25T04:05:26Z	PullRequestEvent	merged				159
2026-09-25T04:05:27Z	PushEvent		refs/heads/main	8276e9d	efc2bb2	
2026-09-25T04:14:44Z	PullRequestEvent	merged				176
2026-09-25T04:14:45Z	PushEvent		refs/heads/main	efc2bb2	5b4fd8b	
2026-09-25T04:15:12Z	PushEvent		refs/heads/gh-pages	95433b2	4a05ab1	
2026-09-25T04:15:12Z	PushEvent		refs/heads/gh-pages	95433b2	4a05ab1	
2026-09-25T04:16:55Z	PullRequestEvent	merged				175
2026-09-25T04:16:56Z	PushEvent		refs/heads/main	5b4fd8b	9baed29	
2026-09-25T05:02:08Z	PullRequestEvent	merged				154
2026-09-25T05:02:09Z	PullRequestEvent	merged				103
2026-09-25T05:02:35Z	PushEvent		refs/heads/gh-pages	4a05ab1	2048bf1	
2026-09-25T05:02:40Z	PushEvent		refs/heads/main	3a8c7d3	6775bb7	
2026-09-25T05:27:49Z	PullRequestEvent	merged				155
2026-09-25T05:28:19Z	PushEvent		refs/heads/gh-pages	2048bf1	50bf6d4	
2026-09-25T05:31:33Z	PullRequestEvent	merged				125
2026-09-25T06:08:11Z	PullRequestEvent	opened				177
2026-09-25T06:17:40Z	PullRequestEvent	merged				177
2026-09-25T06:17:41Z	PushEvent		refs/heads/main	d906b00	b277a51	
```

### `gh api 'repos/mryfmo/dotfiles/activity?ref=refs/heads/main&per_page=50' --jq '.[] | select(.timestamp >= "2026-09-23T07:00:00Z") | [.timestamp, .activity_type, (.before[0:7]), (.after[0:7]), .actor.login] | @tsv' | sort`

```text
2026-09-24T03:37:31Z	push	455455e	3a530b1	mryfmo
2026-09-24T03:39:24Z	push	3a530b1	7e35d78	mryfmo
2026-09-24T03:39:37Z	push	7e35d78	c5193e4	mryfmo
2026-09-25T00:59:38Z	pr_merge	c5193e4	22e5c9f	mryfmo
2026-09-25T01:00:28Z	pr_merge	22e5c9f	d377ad0	mryfmo
2026-09-25T01:29:32Z	push	d377ad0	0aafdb9	mryfmo
2026-09-25T01:32:03Z	push	0aafdb9	f78666a	mryfmo
2026-09-25T01:41:15Z	pr_merge	f78666a	cd61a88	mryfmo
2026-09-25T01:42:10Z	pr_merge	cd61a88	c11035f	mryfmo
2026-09-25T01:52:40Z	pr_merge	c11035f	c5240c3	mryfmo
2026-09-25T01:55:39Z	push	c5240c3	f95074a	mryfmo
2026-09-25T04:02:01Z	pr_merge	f95074a	8276e9d	mryfmo
2026-09-25T04:05:26Z	pr_merge	8276e9d	efc2bb2	mryfmo
2026-09-25T04:14:44Z	pr_merge	efc2bb2	5b4fd8b	mryfmo
2026-09-25T04:16:55Z	pr_merge	5b4fd8b	9baed29	mryfmo
2026-09-25T04:18:28Z	push	9baed29	d6cfed2	mryfmo
2026-09-25T05:02:07Z	push	d6cfed2	3a8c7d3	mryfmo
2026-09-25T05:02:39Z	push	3a8c7d3	6775bb7	mryfmo
2026-09-25T05:27:48Z	push	6775bb7	127e27b	mryfmo
2026-09-25T05:31:32Z	push	127e27b	d906b00	mryfmo
2026-09-25T06:17:40Z	pr_merge	d906b00	b277a51	mryfmo
2026-09-25T06:18:06Z	push	b277a51	3303fbc	mryfmo
```

## 9. CompactionDB memory add

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "リモート差分の基準点は 455455e（clone 時点 = W1/W2 分岐点）、取り込みは 2026-09-25 15:24:54 JST の ff-only pull（455455e..3303fbc）"
dfdd3df7-6dc1-4264-aedf-22e1f9aaef75
```

### `python3 .claude/hooks/contextdb_cli.py memory search 455455e`

```text
dfdd3df7-6dc1-4264-aedf-22e1f9aaef75 [project/decision] リモート差分の基準点は 455455e（clone 時点 = W1/W2 分岐点）、取り込みは 2026-09-25 15:24:54 JST の ff-only pull（455455e..3303fbc）
```

## 10. Supplementary evidence for report claims

### `git show --format='%h %s%n%b' 22e5c9f`

```text
22e5c9f fix(update): converge herdr SessionStart matcher, report unmerged index, dedupe agmsg identities (#170)
* fix(update): converge herdr SessionStart matcher, report unmerged index, dedupe agmsg identities

`make update` regressed on the operator machine in three ways that all
traced to convergence bugs rather than transient state:

- The managed Claude settings template defined the herdr-agent-state.sh
  SessionStart entry with matcher "*", while the herdr integration
  installer rewrites the same entry with
  "^(startup|resume|clear|compact|fork)$". Every run flipped it back and
  forth. Use the herdr canonical regex in the template so both writers
  converge on identical content.
- The pull guard reported "tracked files have staged or unstaged changes;
  run git pull" when the index held unmerged stages, but git pull refuses
  in that state. Detect `git ls-files -u` first and say so.
- The agmsg bootstrap flagged "Multiple ... identities" whenever one
  identity name was registered in more than one team, because it counted
  identities.sh rows instead of distinct names. Dedupe on the name column.

Red-first regressions added for all three (unit + CI-only bats).

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* fix(agent-config): move the herdr SessionStart matcher change to the manifest source

The managed settings template is generated from agent-config.yaml; the
Agent assets validate job flagged the hand-edited template as stale.
Change the matcher at its source so regeneration is a no-op.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* fix(update): check unmerged index before branch metadata; align skill identity rule

Codex review P2s on #170: a conflicted rebase leaves the branch name
empty, so the unmerged-index notice must precede the branch/upstream
checks; and the agmsg-orchestration skill now counts distinct identity
names, matching the herdr-agents dedupe.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>

diff --git a/Makefile b/Makefile
index d9a875d..e4ea632 100644
--- a/Makefile
+++ b/Makefile
@@ -46,7 +46,9 @@ update:
 	@branch="$$(git branch --show-current 2>/dev/null || true)"; \
 	upstream="$$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"; \
 	reason=""; \
-	if [ "$$branch" != main ]; then \
+	if [ -n "$$(git ls-files -u)" ]; then \
+		reason="index has unmerged files; resolve the conflict (git add/commit or git reset) before pulling"; \
+	elif [ "$$branch" != main ]; then \
 		reason="current branch is $${branch:-detached}, not main"; \
 	elif [ "$$upstream" != origin/main ]; then \
 		reason="upstream is $${upstream:-unset}, not origin/main"; \
diff --git a/home/.chezmoitemplates/claude-settings-managed.json b/home/.chezmoitemplates/claude-settings-managed.json
index c8229e6..72750d5 100644
--- a/home/.chezmoitemplates/claude-settings-managed.json
+++ b/home/.chezmoitemplates/claude-settings-managed.json
@@ -43,7 +43,7 @@
     ],
     "SessionStart": [
       {
-        "matcher": "*",
+        "matcher": "^(startup|resume|clear|compact|fork)$",
         "hooks": [
           {
             "type": "command",
diff --git a/home/dot_agents/agent-config.yaml b/home/dot_agents/agent-config.yaml
index 73ba08d..167a347 100644
--- a/home/dot_agents/agent-config.yaml
+++ b/home/dot_agents/agent-config.yaml
@@ -175,7 +175,7 @@ claude:
       timeout: 10
       status_message: Evaluating permission request
     session_start:
-      - matcher: "*"
+      - matcher: "^(startup|resume|clear|compact|fork)$"
         hooks:
           - type: command
             # Must stay byte-identical to herdr's own SessionStart entry after
diff --git a/home/dot_agents/skills/agmsg-orchestration/SKILL.md b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
index b77a046..776523a 100644
--- a/home/dot_agents/skills/agmsg-orchestration/SKILL.md
+++ b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
@@ -27,7 +27,7 @@ Use this skill for structured multi-agent work where a Claude Code orchestrator
 
 - Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to resident Codex workers, with at most one resident worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
 - A parallel assignment is valid only when every concurrent worker has all four of: (1) its own git worktree registered as its agmsg `project`; (2) the shared default agmsg store for same-repository work, never a per-worker `AGMSG_STORAGE_PATH`, because identity-addressed delivery and worktree-specific `whoami` already isolate inboxes and one activation watcher observes every RESULT/PONG without extra watchers (which `watch.sh` actas locking cannot support for one claimed identity); (3) an `-aNNN` identity suffix on every concurrent worker, including the first; and (4) an AGMSG-TASK whose expanded `allowed_files` are pairwise disjoint from all other in-flight tasks. The orchestrator verifies disjointness and performs all cross-worktree merge, rebase, and conflict integration.
-- At parallel-worker teardown, run `delivery.sh set off <type> <worker worktree path>` to stop every watcher on that exact path, then `leave.sh <team> <worker identity>` for each finished worker. The last member of a task-scoped team leaves so the team is deleted while message history remains. Verify with `identities.sh <project> <type>`: one line is healthy, multiple lines are leftover registrations that trigger the herdr-agents ambiguity warning at attach and must be cleaned with `leave.sh`, and zero for a project that should remain active must be restored with `join.sh`, never leave-side edits.
+- At parallel-worker teardown, run `delivery.sh set off <type> <worker worktree path>` to stop every watcher on that exact path, then `leave.sh <team> <worker identity>` for each finished worker. The last member of a task-scoped team leaves so the team is deleted while message history remains. Verify with `identities.sh <project> <type>` by counting distinct identity names in the second TSV column: one distinct name is healthy, including multiple rows for that name across teams. More than one distinct name indicates leftover identities that trigger the herdr-agents ambiguity warning at attach and must be cleaned with `leave.sh`; preserve legitimate multi-team memberships of the retained name. Zero names for a project that should remain active must be restored with `join.sh`, never leave-side edits.
 
 ## Identity, delivery, and storage
 
diff --git a/home/dot_local/bin/common/executable_herdr-agents b/home/dot_local/bin/common/executable_herdr-agents
index 719ac77..d12c554 100644
--- a/home/dot_local/bin/common/executable_herdr-agents
+++ b/home/dot_local/bin/common/executable_herdr-agents
@@ -558,6 +558,7 @@ function bootstrap_agmsg() {
         if ! identity_list="$("${identities}" "${workdir}" "${agent_type}" 2>> "${log_file}")"; then
             continue
         fi
+        identity_list="$(printf '%s\n' "${identity_list}" | cut -f 2 | sort -u)"
         if [[ -z ${identity_list} ]]; then
             printf 'No agmsg %s identity for %s; run: %s/join.sh <team> <agent-name> %s "%s"\n' \
                 "${agent_label}" "${workdir}" "${scripts}" "${agent_type}" "${workdir}" >&2
diff --git a/tests/install/common/lifecycle.bats b/tests/install/common/lifecycle.bats
index d9a97c2..b6f374e 100644
--- a/tests/install/common/lifecycle.bats
+++ b/tests/install/common/lifecycle.bats
@@ -24,6 +24,7 @@ function run_update_fixture() {
     local git_upstream="${9:-origin/feature/test}"
     local git_dirty="${10:-0}"
     local git_pull_exit="${11:-0}"
+    local git_unmerged="${12:-0}"
     local fixture="${BATS_TEST_TMPDIR}/update-${BATS_TEST_NUMBER}"
 
     mkdir -p "${fixture}/bin" "${fixture}/scripts" \
@@ -50,6 +51,7 @@ case "\$*" in
     "branch --show-current") printf '%s\n' '${git_branch}' ;;
     "rev-parse --abbrev-ref --symbolic-full-name @{upstream}") printf '%s\n' '${git_upstream}' ;;
     "diff --quiet"|"diff --cached --quiet") exit ${git_dirty} ;;
+    "ls-files -u") if [ ${git_unmerged} -eq 1 ]; then printf '100644 conflict 1\\tfile\\n'; fi ;;
     "pull --ff-only") printf 'git pull --ff-only\n' >> "${fixture}/calls"; exit ${git_pull_exit} ;;
 esac
 EOF
@@ -95,6 +97,14 @@ EOF
     [[ "$output" == *"Notice: local source not pulled (tracked files have staged or unstaged changes); run 'git -C ${UPDATE_FIXTURE_PHYSICAL} pull' to fetch remote updates."* ]]
 }
 
+@test "[common] update reports unmerged files before the dirty notice" {
+    run_update_fixture running 0 0 0 0 0 "" main origin/main 1 0 1
+    [ "$status" -eq 0 ]
+    ! grep -q '^git pull --ff-only$' "${UPDATE_FIXTURE}/calls"
+    [[ "$output" == *"index has unmerged files; resolve the conflict (git add/commit or git reset) before pulling"* ]]
+    [[ "$output" != *"tracked files have staged or unstaged changes"* ]]
+}
+
 @test "[common] update reloads a running Herdr server exactly once" {
     run_update_fixture running
     [ "$status" -eq 0 ]
diff --git a/tests/unit/test_claude_settings_merge.py b/tests/unit/test_claude_settings_merge.py
index 6b3dd91..bd6024a 100644
--- a/tests/unit/test_claude_settings_merge.py
+++ b/tests/unit/test_claude_settings_merge.py
@@ -406,6 +406,31 @@ class ClaudeSettingsMergeTest(unittest.TestCase):
         self.assertEqual(json.loads(output)["effortLevel"], "high")
         self.assertTrue(output.endswith("\n"))
 
+    def test_real_template_preserves_herdr_matcher_and_converges(self) -> None:
+        managed = json.loads(
+            (ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()
+        )
+        canonical_matcher = "^(startup|resume|clear|compact|fork)$"
+        current = json.dumps({
+            "hooks": {"SessionStart": [{
+                "matcher": canonical_matcher,
+                "hooks": [{
+                    "type": "command",
+                    "command": f"bash '{self.home_dir}/.claude/hooks/herdr-agent-state.sh' session",
+                    "timeout": 10,
+                }],
+            }]},
+        })
+
+        once = self.merge(managed, current)
+        state_entries = [
+            entry for entry in json.loads(once)["hooks"]["SessionStart"]
+            if any("herdr-agent-state.sh" in hook["command"] for hook in entry["hooks"])
+        ]
+        self.assertEqual(len(state_entries), 1)
+        self.assertEqual(state_entries[0]["matcher"], canonical_matcher)
+        self.assertEqual(self.merge(managed, once), once)
+
     def test_trailing_newline(self) -> None:
         output = self.merge({"model": "managed", "enabledPlugins": {}}, "")
 
diff --git a/tests/unit/test_herdr_agents.py b/tests/unit/test_herdr_agents.py
index e2bd12b..e633e5c 100644
--- a/tests/unit/test_herdr_agents.py
+++ b/tests/unit/test_herdr_agents.py
@@ -998,6 +998,20 @@ printf 'herdr %s\\n' "$*" >> {self.calls_path}
             )
         )
 
+    def test_bootstrap_accepts_same_identity_in_multiple_teams(self) -> None:
+        scripts = self.install_agmsg_fakes(
+            identities_output="team-a\tcodex-worker\nteam-b\tcodex-worker",
+            claude_identities_output="team-a\tclaude-deep-dot\nteam-b\tclaude-deep-dot",
+        )
+        self.write_agmsg_turn_hook(scripts)
+        self.write_agmsg_claude_hooks(scripts)
+
+        result = self.run_agmsg_bootstrap_helper()
+
+        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
+        self.assertNotIn("Multiple agmsg", result.stderr)
+        self.assertNotIn("No agmsg", result.stderr)
+
     def test_bootstrap_only_warns_for_multiple_claude_identities(self) -> None:
         scripts = self.install_agmsg_fakes(
             claude_identities_output=(
diff --git a/tests/unit/test_runtime_health.py b/tests/unit/test_runtime_health.py
index 43140bb..4c049e8 100644
--- a/tests/unit/test_runtime_health.py
+++ b/tests/unit/test_runtime_health.py
@@ -575,6 +575,7 @@ EOF
         branch: str = "main",
         upstream: str = "origin/main",
         dirty: bool = False,
+        unmerged: bool = False,
     ) -> tuple[subprocess.CompletedProcess[str], Path]:
         repo = self.temp_dir / f"update-{'dirty' if dirty else 'clean'}"
         home = repo / "home"
@@ -589,6 +590,7 @@ EOF
                 "branch --show-current") printf '{branch}\\n' ;;
                 "rev-parse --abbrev-ref --symbolic-full-name @{{upstream}}") printf '{upstream}\\n' ;;
                 "diff --quiet"|"diff --cached --quiet") exit {int(dirty)} ;;
+                "ls-files -u") if [ {int(unmerged)} -eq 1 ]; then printf '100644 conflict 1\\tfile\\n'; fi ;;
                 "pull --ff-only") printf 'git pull --ff-only\\n' >> "$TEST_LOG" ;;
             esac
             """,
@@ -643,6 +645,26 @@ EOF
         )
         self.assertIn(" pull' to fetch remote updates.", result.stdout)
 
+    def test_make_update_reports_unmerged_index_before_dirty_notice(self) -> None:
+        result, log = self.update_fixture(dirty=True, unmerged=True)
+
+        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
+        self.assertNotIn("git pull --ff-only", log.read_text())
+        self.assertIn(
+            "index has unmerged files; resolve the conflict "
+            "(git add/commit or git reset) before pulling",
+            result.stdout,
+        )
+        self.assertNotIn("tracked files have staged or unstaged changes", result.stdout)
+
+    def test_make_update_reports_unmerged_feature_branch_before_branch_notice(self) -> None:
+        result, log = self.update_fixture(branch="feature/x", unmerged=True)
+
+        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
+        self.assertNotIn("git pull --ff-only", log.read_text())
+        self.assertIn("index has unmerged files", result.stdout)
+        self.assertNotIn("current branch is", result.stdout)
+
     def test_agent_launchers_do_not_hardcode_model_ids(self) -> None:
         herdr = (ROOT / "home/dot_local/bin/common/executable_herdr-agents").read_text()
         fanout = (
```

### `git show --format='%h %s%n%b' d377ad0`

```text
d377ad0 chore(mise): upgrade tool pins via make upgrade (#171)
* chore(mise): upgrade tool pins via make upgrade

Regenerated on a clean origin/main branch with `make upgrade`; no hand
edits. Every exact-version consumer moves with the pin.

- dotenvx 2.26.1 -> 2.28.0
- herdr 0.9.0 -> 0.9.1
- bash-language-server 5.6.0 -> 5.8.0
- @anthropic-ai/claude-code 2.1.280 -> 2.1.282
- ccstatusline 2.2.29 -> 2.2.30, ccusage 20.0.20 -> 20.0.22
  (also in .github/workflows/test.yaml, scripts/check-statusline-tools.py,
  tests/unit/test_statusline_tools.py)
- crit v0.20.2 -> v0.20.3, zed v1.20.2 -> v1.21.0 with Linux SHA256s
  verified against the GitHub release asset digests

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* test(mise): assert the herdr pin exists instead of a literal version

Removes the last exact-version consumer that had to move with every
`make upgrade`.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>

diff --git a/.github/workflows/test.yaml b/.github/workflows/test.yaml
index e4033d3..1dc72ee 100644
--- a/.github/workflows/test.yaml
+++ b/.github/workflows/test.yaml
@@ -196,8 +196,8 @@ jobs:
           mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"
           mise -C "${RUNNER_TEMP}/statusline-mise" install --locked node
           mise -C "${RUNNER_TEMP}/statusline-mise" install --locked \
-            npm:ccstatusline@2.2.29 \
-            npm:ccusage@20.0.20
+            npm:ccstatusline@2.2.30 \
+            npm:ccusage@20.0.22
 
       - name: Smoke-test statusline tools without network
         if: ${{ needs.changes.outputs.should_test == 'true' }}
@@ -207,8 +207,8 @@ jobs:
           statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
           ccstatusline_bin="$(mise -C "${statusline_mise_dir}" which ccstatusline)"
           ccusage_bin="$(mise -C "${statusline_mise_dir}" which ccusage)"
-          ccstatusline_root="$(mise -C "${statusline_mise_dir}" where npm:ccstatusline@2.2.29)"
-          ccusage_root="$(mise -C "${statusline_mise_dir}" where npm:ccusage@20.0.20)"
+          ccstatusline_root="$(mise -C "${statusline_mise_dir}" where npm:ccstatusline@2.2.30)"
+          ccusage_root="$(mise -C "${statusline_mise_dir}" where npm:ccusage@20.0.22)"
 
           case "${ccstatusline_bin}" in
             "${ccstatusline_root}"/*) ;;
diff --git a/home/dot_mise/config.toml b/home/dot_mise/config.toml
index 71d8931..d503b01 100644
--- a/home/dot_mise/config.toml
+++ b/home/dot_mise/config.toml
@@ -8,7 +8,7 @@ age = "1.3.2"
 bun = "1.4.2"
 chezmoi = "2.72.2"
 cmake = "4.4.3"
-dotenvx = "2.26.1"
+dotenvx = "2.28.0"
 "cargo:eza" = "0.23.5"
 fd = "10.3.0"
 jq = "1.8.2"
@@ -21,18 +21,18 @@ shellcheck = "0.11.0"
 shfmt = "3.14.1"
 "aqua:watchexec/watchexec" = "2.7.3"
 
-"npm:@anthropic-ai/claude-code" = { version = "2.1.280", allow_builds = ["@anthropic-ai/claude-code"] }
+"npm:@anthropic-ai/claude-code" = { version = "2.1.282", allow_builds = ["@anthropic-ai/claude-code"] }
 "npm:@openai/codex" = "0.156.1"
-"npm:bash-language-server" = "5.6.0"
-"npm:ccstatusline" = "2.2.29"
-"npm:ccusage" = "20.0.20"
+"npm:bash-language-server" = "5.8.0"
+"npm:ccstatusline" = "2.2.30"
+"npm:ccusage" = "20.0.22"
 "npm:pyright" = "1.1.414"
 "npm:fast-cli" = "5.2.0"
 
 "github:x-motemen/ghq" = "1.10.1"
 "github:d-kuro/gwq" = "0.1.1"
 "github:cli/cli" = "2.101.0"
-"github:ogulcancelik/herdr" = "0.9.0"
+"github:ogulcancelik/herdr" = "0.9.1"
 "github:shuntaka9576/blocc" = { version = "0.6.0", os = ["linux/x64"] }
 
 "cargo:pueue" = "4.0.4"
diff --git a/home/dot_mise/mise.lock b/home/dot_mise/mise.lock
index f068ba1..e744071 100644
--- a/home/dot_mise/mise.lock
+++ b/home/dot_mise/mise.lock
@@ -229,28 +229,28 @@ url = "https://github.com/Kitware/CMake/releases/download/v4.4.3/cmake-4.4.3-mac
 url_api = "https://api.github.com/repos/Kitware/CMake/releases/assets/529577557"
 
 [[tools.dotenvx]]
-version = "2.26.1"
+version = "2.28.0"
 backend = "aqua:dotenvx/dotenvx"
 
 [tools.dotenvx."platforms.linux-arm64"]
-checksum = "sha256:b5465a32e2f625ebcc6015253b7a67ef1c0367a57d832187d564b6b4708a130c"
-url = "https://github.com/dotenvx/dotenvx/releases/download/v2.26.1/dotenvx-2.26.1-linux-aarch64.tar.gz"
-url_api = "https://api.github.com/repos/dotenvx/dotenvx/releases/assets/565572525"
+checksum = "sha256:d31270b20a5895c8fdd2c5209ef10506bfb9bc620791cdd67d822f89ef3faa1c"
+url = "https://github.com/dotenvx/dotenvx/releases/download/v2.28.0/dotenvx-2.28.0-linux-aarch64.tar.gz"
+url_api = "https://api.github.com/repos/dotenvx/dotenvx/releases/assets/568780480"
 
 [tools.dotenvx."platforms.linux-x64"]
-checksum = "sha256:6e35999d06755acc1af310cee344e48245d4bf2cdd31ecee4856bbf81c2c67dc"
-url = "https://github.com/dotenvx/dotenvx/releases/download/v2.26.1/dotenvx-2.26.1-linux-amd64.tar.gz"
-url_api = "https://api.github.com/repos/dotenvx/dotenvx/releases/assets/565572524"
+checksum = "sha256:d5e4401c9880ecaf83b101afc918f4aebb7c2c2ec16b67a41addd1fce12fbe6a"
+url = "https://github.com/dotenvx/dotenvx/releases/download/v2.28.0/dotenvx-2.28.0-linux-amd64.tar.gz"
+url_api = "https://api.github.com/repos/dotenvx/dotenvx/releases/assets/568780474"
 
 [tools.dotenvx."platforms.macos-arm64"]
-checksum = "sha256:81e07b1b3a34d6ee138b5ac53b618870c6a71b7ded782ee6aa11e67111d928e7"
-url = "https://github.com/dotenvx/dotenvx/releases/download/v2.26.1/dotenvx-2.26.1-darwin-arm64.tar.gz"
-url_api = "https://api.github.com/repos/dotenvx/dotenvx/releases/assets/565572547"
+checksum = "sha256:eb7156249da3044e907b1c85111d7fc6e08b62665c3cc96bd23f54c64c9e39c0"
+url = "https://github.com/dotenvx/dotenvx/releases/download/v2.28.0/dotenvx-2.28.0-darwin-arm64.tar.gz"
+url_api = "https://api.github.com/repos/dotenvx/dotenvx/releases/assets/568780475"
 
 [tools.dotenvx."platforms.macos-x64"]
-checksum = "sha256:1b22976f18590cc226d21b01a3deda2f0ae9dfe8c96ce3c4e8153c44c4e01763"
-url = "https://github.com/dotenvx/dotenvx/releases/download/v2.26.1/dotenvx-2.26.1-darwin-amd64.tar.gz"
-url_api = "https://api.github.com/repos/dotenvx/dotenvx/releases/assets/565572521"
+checksum = "sha256:537131fbdf0b5a495167bb7b2b0760751664831bae7dd9c68fac2e35bc4f8ef7"
+url = "https://github.com/dotenvx/dotenvx/releases/download/v2.28.0/dotenvx-2.28.0-darwin-amd64.tar.gz"
+url_api = "https://api.github.com/repos/dotenvx/dotenvx/releases/assets/568780496"
 
 [[tools.fd]]
 version = "10.3.0"
@@ -329,31 +329,31 @@ url = "https://github.com/d-kuro/gwq/releases/download/v0.1.1/gwq_Darwin_x86_64.
 url_api = "https://api.github.com/repos/d-kuro/gwq/releases/assets/410341155"
 
 [[tools."github:ogulcancelik/herdr"]]
-version = "0.9.0"
+version = "0.9.1"
 backend = "github:ogulcancelik/herdr"
 
 [tools."github:ogulcancelik/herdr"."platforms.linux-arm64"]
-checksum = "sha256:9c8db20fb7e7427b138d5367113f1621ffd319f2f65d6f009e2594029115f0d2"
-url = "https://github.com/herdrdev/herdr/releases/download/v0.9.0/herdr-linux-aarch64"
-url_api = "https://api.github.com/repos/herdrdev/herdr/releases/assets/549270160"
+checksum = "sha256:f4ccf4de745f2cb9a39a983e9ba3703dad50ec2a58dea83026ceab721bbd8d9e"
+url = "https://github.com/herdrdev/herdr/releases/download/v0.9.1/herdr-linux-aarch64"
+url_api = "https://api.github.com/repos/herdrdev/herdr/releases/assets/568559680"
 provenance = "github-attestations"
 
 [tools."github:ogulcancelik/herdr"."platforms.linux-x64"]
-checksum = "sha256:4fa1a01158dd8043da92d31b270780b0dcc10603038d9b61cac4d81ab63fb71f"
-url = "https://github.com/herdrdev/herdr/releases/download/v0.9.0/herdr-linux-x86_64"
-url_api = "https://api.github.com/repos/herdrdev/herdr/releases/assets/549270163"
+checksum = "sha256:2a02fed16beb651ef006e1d43f048f652ca4dc58ad053cd2d44450563d5c54b7"
+url = "https://github.com/herdrdev/herdr/releases/download/v0.9.1/herdr-linux-x86_64"
+url_api = "https://api.github.com/repos/herdrdev/herdr/releases/assets/568559679"
 provenance = "github-attestations"
 
 [tools."github:ogulcancelik/herdr"."platforms.macos-arm64"]
-checksum = "sha256:32b53df09872628059c789a69f02a6b8e29e14ddf26711421f3463f70c1aef17"
-url = "https://github.com/herdrdev/herdr/releases/download/v0.9.0/herdr-macos-aarch64"
-url_api = "https://api.github.com/repos/herdrdev/herdr/releases/assets/549270162"
+checksum = "sha256:5fc7a7e7adfaca56fa80aa89dcb025693357268dab8285b9ce2d08a2313c89de"
+url = "https://github.com/herdrdev/herdr/releases/download/v0.9.1/herdr-macos-aarch64"
+url_api = "https://api.github.com/repos/herdrdev/herdr/releases/assets/568559677"
 provenance = "github-attestations"
 
 [tools."github:ogulcancelik/herdr"."platforms.macos-x64"]
-checksum = "sha256:d0c920b2a126a74809fa1491411c9a097a44786cac9c2ca51b818a995581cf16"
-url = "https://github.com/herdrdev/herdr/releases/download/v0.9.0/herdr-macos-x86_64"
-url_api = "https://api.github.com/repos/herdrdev/herdr/releases/assets/549270161"
+checksum = "sha256:053be0639935fe54ab5efbdb46651054e4f6a753a5b43153c88bd6912bce1e94"
+url = "https://github.com/herdrdev/herdr/releases/download/v0.9.1/herdr-macos-x86_64"
+url_api = "https://api.github.com/repos/herdrdev/herdr/releases/assets/568559678"
 provenance = "github-attestations"
 
 [[tools."github:shuntaka9576/blocc"]]
@@ -510,7 +510,7 @@ checksum = "sha256:06b2e742ed9025dc84adc830243b3f731956eac9c321bccd0ede384209af0
 url = "https://nodejs.org/dist/v26.9.0/node-v26.9.0-darwin-x64.tar.gz"
 
 [[tools."npm:@anthropic-ai/claude-code"]]
-version = "2.1.280"
+version = "2.1.282"
 backend = "npm:@anthropic-ai/claude-code"
 
 [tools."npm:@anthropic-ai/claude-code".options]
@@ -521,15 +521,15 @@ version = "0.156.1"
 backend = "npm:@openai/codex"
 
 [[tools."npm:bash-language-server"]]
-version = "5.6.0"
+version = "5.8.0"
 backend = "npm:bash-language-server"
 
 [[tools."npm:ccstatusline"]]
-version = "2.2.29"
+version = "2.2.30"
 backend = "npm:ccstatusline"
 
 [[tools."npm:ccusage"]]
-version = "20.0.20"
+version = "20.0.22"
 backend = "npm:ccusage"
 
 [[tools."npm:fast-cli"]]
diff --git a/scripts/check-statusline-tools.py b/scripts/check-statusline-tools.py
index 3bb6192..21e2a58 100644
--- a/scripts/check-statusline-tools.py
+++ b/scripts/check-statusline-tools.py
@@ -17,7 +17,7 @@ CLAUDE_STATUS = {
     "session_id": "offline-test",
     "transcript_path": "/private/tmp/nonexistent.jsonl",
 }
-EXPECTED_VERSIONS = {"ccstatusline": "2.2.29", "ccusage": "20.0.20"}
+EXPECTED_VERSIONS = {"ccstatusline": "2.2.30", "ccusage": "20.0.22"}
 
 
 def run(command: list[str], stdin: str | None = None) -> subprocess.CompletedProcess[str]:
diff --git a/scripts/lib/installer-pins.sh b/scripts/lib/installer-pins.sh
index 6c7c74e..0ce8110 100644
--- a/scripts/lib/installer-pins.sh
+++ b/scripts/lib/installer-pins.sh
@@ -15,9 +15,9 @@ TERMINAL_CODE_PIN_VERSION="v0.3.4"
 TERMINAL_CODE_INSTALLER_SHA256="026192e9f377af44f48c1c1e9f008c081369013d96901e5bff898f210272813c"
 TERMINAL_BROWSER_PIN_VERSION="v0.11.1"
 TERMINAL_BROWSER_INSTALLER_SHA256="accb57252d6e7dde513db2a473c008d71897cf72feaaecd58c5042821d1d63f9"
-CRIT_PIN_VERSION="v0.20.2"
-CRIT_LINUX_AMD64_SHA256="d2907008164fada5bd5221ffd37ed125c181280cec3ed74465e526ea7d25d20a"
-CRIT_LINUX_ARM64_SHA256="833dd8145e5b47c06d88af80f8b6505159693742aadefcf400f923d7bc6c3b11"
-ZED_PIN_VERSION="v1.20.2"
-ZED_LINUX_AMD64_SHA256="647dc85e09fcd99cd175365a89b7b70ccf96469c4844eb8ae6eb83dfa82f7600"
-ZED_LINUX_ARM64_SHA256="715a5252234522bc9e8e4a8c1f9b462cf7bb2881eed23b7c8ae650b41c24aa6f"
+CRIT_PIN_VERSION="v0.20.3"
+CRIT_LINUX_AMD64_SHA256="d3a348770e828f9f1710501735504107d1eccb195f29cacdffed92f75b6abba1"
+CRIT_LINUX_ARM64_SHA256="5a779fa202a1c7e8a1a6c5b05b4afa3a098b77c0c25103b0daf1d899f6d766ff"
+ZED_PIN_VERSION="v1.21.0"
+ZED_LINUX_AMD64_SHA256="b79a992e960ed4067cb2b50d66789ed8618eeb1780ed6a0f8f1e71dd80f74200"
+ZED_LINUX_ARM64_SHA256="69eff51b22203be7a4d0fd9df0864a8abd4d5183e8fb9aafa2af57f3cd42b9a3"
diff --git a/tests/install/common/mise.bats b/tests/install/common/mise.bats
index fbe6f29..9eea75e 100644
--- a/tests/install/common/mise.bats
+++ b/tests/install/common/mise.bats
@@ -132,7 +132,7 @@ install --locked --before ${DEFAULT_NPM_MIN_RELEASE_AGE_DAYS}d" ]
 }
 
 @test "[common] herdr is installed by mise on Linux and macOS" {
-    run grep -F '"github:ogulcancelik/herdr" = "0.9.0"' home/dot_mise/config.toml
+    run grep -E '^"github:ogulcancelik/herdr" = "[^"]+"$' home/dot_mise/config.toml
     [ "${status}" -eq 0 ]
 }
 
diff --git a/tests/unit/test_statusline_tools.py b/tests/unit/test_statusline_tools.py
index 2c3011e..02dc335 100644
--- a/tests/unit/test_statusline_tools.py
+++ b/tests/unit/test_statusline_tools.py
@@ -21,8 +21,8 @@ CLAUDE_SETTINGS = ROOT / "home/.chezmoitemplates/claude-settings-managed.json"
 CI_WORKFLOW = ROOT / ".github/workflows/test.yaml"
 INTEGRATION_SMOKE = ROOT / "scripts/check-statusline-tools.py"
 EXPECTED_TOOLS = {
-    "npm:ccusage": "20.0.20",
-    "npm:ccstatusline": "2.2.29",
+    "npm:ccusage": "20.0.22",
+    "npm:ccstatusline": "2.2.30",
 }
 
 
@@ -100,8 +100,8 @@ class StatuslineToolsTest(unittest.TestCase):
 
         for token in (
             node_install,
-            "npm:ccstatusline@2.2.29",
-            "npm:ccusage@20.0.20",
+            "npm:ccstatusline@2.2.30",
+            "npm:ccusage@20.0.22",
             'mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"',
             "sudo unshare --net",
             "/usr/bin/sandbox-exec",
@@ -111,7 +111,7 @@ class StatuslineToolsTest(unittest.TestCase):
         ):
             self.assertIn(token, workflow)
         self.assertLess(
-            workflow.index(node_install), workflow.index("npm:ccstatusline@2.2.29")
+            workflow.index(node_install), workflow.index("npm:ccstatusline@2.2.30")
         )
         for token in (
             '"display_name": "Claude"',
```

### `git show --format='%h %s%n%b' cd61a88`

```text
cd61a88 fix(mise): stop make upgrade and mise from writing into the main checkout (#172)
* fix(mise): stop make upgrade and mise from writing into the main checkout

`~/.config/mise/{config.toml,mise.lock}` were chezmoi symlinks into the
main checkout's home/dot_mise, and upgrade-tools.sh resolved mise's
config dir to ~/.config/mise. Any `make upgrade` (from any worktree) or
ad-hoc `mise upgrade` therefore mutated main's committed pins, which is
how the pair stayed dirty across sessions and produced the 2026-09-22
autostash conflict.

- Render ~/.config/mise/* as regular files that include home/dot_mise/*
  (byte-identical) instead of symlinks.
- upgrade-tools.sh scopes mise to the executing checkout: MISE_CONFIG_DIR
  defaults to <checkout>/home/dot_mise (explicit override kept) and
  MISE_CEILING_PATHS stops ancestor discovery from reaching a live home
  config, which MISE_CONFIG_DIR alone did not prevent.
- Fixtures: fake-mise upgrade with legacy live symlinks (default and
  override) proves the symlink target is untouched; chezmoi render and
  apply fixtures prove copies replace symlinks and later runtime writes
  never reach the source tree.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* fix(upgrade): apply the upgraded mise pins to the live copy from the canonical checkout

Codex review on #172: with ~/.config/mise now an applied copy, a
successful `make upgrade` left shells on the old pins until `make
update`. When the executing checkout is the chezmoi source tree, the
upgrade now ends by applying just the two managed mise files; from any
other checkout it prints that the live copy follows after merge and
`make update`. Also turns the zshrc note into a plain inline comment.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>

diff --git a/README.md b/README.md
index 23a6ec0..f55ac3e 100644
--- a/README.md
+++ b/README.md
@@ -426,6 +426,7 @@ content hash, including when a newly committed script first reaches an existing
 machine through `make update`.
 Do not use `make reset` as the normal update path; it clears chezmoi's script state so one-time installers can run again intentionally.
 Tool versions in `home/dot_mise/config.toml` are exact and backed by `mise.lock`. Updates occur only through `make upgrade` with a reviewed config and lock diff.
+`make upgrade` edits the current checkout's `home/dot_mise`; `~/.config/mise` is an applied copy, not a live symlink into the source tree.
 For `npm:` tools, mise owns the version, lock entry, and isolated install
 prefix, while the npm CLI performs installation through
 `settings.npm.package_manager = "npm"`. Do not install Claude Code or Codex
diff --git a/home/dot_config/mise/config.toml.tmpl b/home/dot_config/mise/config.toml.tmpl
new file mode 100644
index 0000000..3868603
--- /dev/null
+++ b/home/dot_config/mise/config.toml.tmpl
@@ -0,0 +1 @@
+{{ include "dot_mise/config.toml" -}}
diff --git a/home/dot_config/mise/mise.lock.tmpl b/home/dot_config/mise/mise.lock.tmpl
new file mode 100644
index 0000000..6a59fe3
--- /dev/null
+++ b/home/dot_config/mise/mise.lock.tmpl
@@ -0,0 +1 @@
+{{ include "dot_mise/mise.lock" -}}
diff --git a/home/dot_config/mise/symlink_config.toml.tmpl b/home/dot_config/mise/symlink_config.toml.tmpl
deleted file mode 100644
index 7fdb260..0000000
--- a/home/dot_config/mise/symlink_config.toml.tmpl
+++ /dev/null
@@ -1 +0,0 @@
-{{ .chezmoi.sourceDir }}/dot_mise/config.toml
diff --git a/home/dot_config/mise/symlink_mise.lock.tmpl b/home/dot_config/mise/symlink_mise.lock.tmpl
deleted file mode 100644
index f864123..0000000
--- a/home/dot_config/mise/symlink_mise.lock.tmpl
+++ /dev/null
@@ -1 +0,0 @@
-{{ .chezmoi.sourceDir }}/dot_mise/mise.lock
diff --git a/home/dot_zshrc b/home/dot_zshrc
index 34beb04..d6d086f 100644
--- a/home/dot_zshrc
+++ b/home/dot_zshrc
@@ -48,6 +48,7 @@ claude-update() {
 
     # Update claude-code to the true latest via mise, bypassing the npm
     # `min-release-age` cooldown for THIS install only.
+    # This updates the applied copy; commit tool pins only via make upgrade.
     npm_config_min_release_age=0 mise upgrade "npm:@anthropic-ai/claude-code"
     claude_prefix="$(mise where "npm:@anthropic-ai/claude-code")"
     claude_version="$(mise current "npm:@anthropic-ai/claude-code")"
diff --git a/scripts/upgrade-tools.sh b/scripts/upgrade-tools.sh
index 2dbef3a..01bca51 100755
--- a/scripts/upgrade-tools.sh
+++ b/scripts/upgrade-tools.sh
@@ -7,9 +7,14 @@
 #   intentional lifecycle command. The default mode upgrades user-level tooling
 #   and Homebrew-managed packages when those managers are available. Pass
 #   `--system` to include operating-system package upgrades such as apt.
+#   Upgrades edit this checkout's home/dot_mise; ~/.config/mise is an applied copy.
 
 set -Eeuo pipefail
 
+repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
+export MISE_CONFIG_DIR="${MISE_CONFIG_DIR:-${repo_root}/home/dot_mise}"
+export MISE_CEILING_PATHS="${repo_root}"
+
 include_system=false
 DEFAULT_FORBIDDEN_HOMEBREW_FORMULAE="node node@* python python@* python3 pip npm pnpm yarn claude"
 required_failures=0
@@ -183,7 +188,7 @@ function run_mise_with_isolated_git_config() {
     local mise_config_dir
     local status
 
-    mise_config_dir="${MISE_CONFIG_DIR:-${XDG_CONFIG_HOME:-${HOME%/}/.config}/mise}"
+    mise_config_dir="${MISE_CONFIG_DIR}"
     isolated_xdg_config_home="$(mktemp -d "${TMPDIR:-/tmp}/mise-git-config.XXXXXX")"
     GIT_CONFIG_NOSYSTEM=1 \
         GIT_CONFIG_GLOBAL=/dev/null \
@@ -572,6 +577,19 @@ USAGE
     done
 }
 
+#
+# @description Apply updated mise pins only from the configured chezmoi checkout.
+function apply_upgraded_mise_config() {
+    local source_path source_root
+    if source_path="$(chezmoi source-path 2> /dev/null)" &&
+        source_root="$(git -C "$source_path" rev-parse --show-toplevel 2> /dev/null)" &&
+        [ "$(cd "$source_root" && pwd -P)" = "$(cd "$repo_root" && pwd -P)" ]; then
+        chezmoi apply "${HOME}/.config/mise/config.toml" "${HOME}/.config/mise/mise.lock"
+    else
+        printf 'pins updated in %s; ~/.config/mise follows after merge and make update\n' "$repo_root"
+    fi
+}
+
 #
 # @description Run explicit upgrades for managed tooling.
 # @arg $@ string Command-line arguments.
@@ -589,6 +607,9 @@ function main() {
     run_optional_phase "GitHub CLI extension upgrade" upgrade_gh_extensions
     run_optional_phase "CCR adoption gate notice" report_ccr_adoption_gates
     run_required_phase "apt system upgrade" upgrade_apt_packages
+    if [ "${required_failures}" -eq 0 ]; then
+        run_required_phase "apply upgraded mise config" apply_upgraded_mise_config
+    fi
 
     printf '\nUpgrade summary: required failures: %d; optional warnings: %d\n' \
         "${required_failures}" "${optional_warnings}"
diff --git a/tests/install/common/lifecycle.bats b/tests/install/common/lifecycle.bats
index b6f374e..5879cd5 100644
--- a/tests/install/common/lifecycle.bats
+++ b/tests/install/common/lifecycle.bats
@@ -278,8 +278,8 @@ herdr server reload-config" ]
     grep -q 'GIT_CONFIG_NOSYSTEM=1' scripts/upgrade-tools.sh
     grep -q 'GIT_CONFIG_GLOBAL=/dev/null' scripts/upgrade-tools.sh
     grep -q 'XDG_CONFIG_HOME="${isolated_xdg_config_home}"' scripts/upgrade-tools.sh
-    grep -q 'mise_config_dir="${MISE_CONFIG_DIR:-${XDG_CONFIG_HOME:-${HOME%/}/.config}/mise}"' scripts/upgrade-tools.sh
-    grep -q 'MISE_CONFIG_DIR="${mise_config_dir}"' scripts/upgrade-tools.sh
+    grep -Fq 'export MISE_CONFIG_DIR="${MISE_CONFIG_DIR:-${repo_root}/home/dot_mise}"' scripts/upgrade-tools.sh
+    grep -Fq 'export MISE_CEILING_PATHS="${repo_root}"' scripts/upgrade-tools.sh
     grep -q 'rm -rf "${isolated_xdg_config_home}"' scripts/upgrade-tools.sh
     grep -q 'run_mise_with_isolated_git_config ls --current --no-header' scripts/upgrade-tools.sh
     grep -q 'MISE_LOCKED=0 run_mise_with_isolated_git_config upgrade --bump --yes --before 7d "${mise_tool}"' scripts/upgrade-tools.sh
diff --git a/tests/unit/test_runtime_health.py b/tests/unit/test_runtime_health.py
index 4c049e8..94ab0ca 100644
--- a/tests/unit/test_runtime_health.py
+++ b/tests/unit/test_runtime_health.py
@@ -1104,6 +1104,17 @@ EOF
             """,
         )
         self.executable(bin_dir / "apt-get", "exit 0\n")
+        self.executable(
+            bin_dir / "chezmoi",
+            """
+            printf 'chezmoi %s\\n' "$*" >> "$TEST_LOG"
+            if [ "$1" = source-path ]; then
+                printf '%s\\n' "$TEST_CHEZMOI_SOURCE"
+            else
+                [ "${FAIL_PHASE}" != chezmoi_apply ]
+            fi
+            """,
+        )
         log = repo / "commands.log"
         env = {
             **os.environ,
@@ -1111,9 +1122,89 @@ EOF
             "HOME": str(home),
             "PATH": f"{bin_dir}:/usr/bin:/bin",
             "TEST_LOG": str(log),
+            "TEST_CHEZMOI_SOURCE": str(self.temp_dir / "other-source/home"),
         }
         return repo, env
 
+    def test_upgrade_applies_mise_only_from_successful_canonical_checkout(self) -> None:
+        cases = ((True, "none"), (False, "none"), (True, "uv"), (True, "chezmoi_apply"))
+        for canonical, fail_phase in cases:
+            with self.subTest(canonical=canonical, fail_phase=fail_phase):
+                repo, env = self.upgrade_fixture(f"apply-{canonical}-{fail_phase}")
+                env["FAIL_PHASE"] = fail_phase
+                source_repo = repo if canonical else repo / "other-source"
+                (source_repo / "home").mkdir(parents=True, exist_ok=True)
+                initialized = self.run_test_command(
+                    ["git", "init", str(source_repo)], cwd=repo, env=env
+                )
+                self.assertEqual(0, initialized.returncode, initialized.stderr)
+                env["TEST_CHEZMOI_SOURCE"] = str(source_repo / "home")
+                result = self.run_test_command(
+                    ["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env
+                )
+                self.assertEqual(
+                    0 if fail_phase == "none" else 1,
+                    result.returncode,
+                    result.stdout + result.stderr,
+                )
+                calls = Path(env["TEST_LOG"]).read_text()
+                if canonical and fail_phase != "uv":
+                    self.assertIn(
+                        f"chezmoi apply {env['HOME']}/.config/mise/config.toml {env['HOME']}/.config/mise/mise.lock",
+                        calls,
+                    )
+                else:
+                    self.assertNotIn("chezmoi apply", calls)
+                if not canonical:
+                    self.assertIn(
+                        f"pins updated in {repo.resolve()}; ~/.config/mise follows after merge and make update",
+                        result.stdout,
+                    )
+
+    def test_upgrade_changes_checkout_not_live_mise_symlink_target(self) -> None:
+        for override in (False, True):
+            with self.subTest(override=override):
+                repo, env = self.upgrade_fixture(f"symlink-{override}")
+                main_config = self.temp_dir / f"main-{override}"
+                main_config.mkdir()
+                checkout_config = repo / "home/dot_mise"
+                checkout_config.mkdir()
+                selected_config = repo / "override" if override else checkout_config
+                selected_config.mkdir(exist_ok=True)
+                live_config = Path(env["HOME"]) / ".config/mise"
+                live_config.mkdir(parents=True)
+                for name in ("config.toml", "mise.lock"):
+                    (main_config / name).write_text("main-original\n")
+                    (selected_config / name).write_text("checkout-original\n")
+                    (live_config / name).symlink_to(main_config / name)
+                env.pop("MISE_CONFIG_DIR", None)
+                env.pop("MISE_CEILING_PATHS", None)
+                if override:
+                    env["MISE_CONFIG_DIR"] = str(selected_config)
+                original_mise = repo / "bin/mise-original"
+                (repo / "bin/mise").rename(original_mise)
+                self.executable(
+                    repo / "bin/mise",
+                    f"""
+                    if [ "$1" = upgrade ] || [ "$1" = use ]; then
+                        target="${{MISE_CONFIG_DIR:-$HOME/.config/mise}}"
+                        [ "${{MISE_CEILING_PATHS:-}}" = "{repo.resolve()}" ] || target="$HOME/.config/mise"
+                        printf 'generated config\\n' > "$target/config.toml"
+                        printf 'generated lock\\n' > "$target/mise.lock"
+                    fi
+                    exec "{original_mise}" "$@"
+                    """,
+                )
+                result = self.run_test_command(
+                    ["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env
+                )
+                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
+                for name in ("config.toml", "mise.lock"):
+                    self.assertEqual((main_config / name).read_text(), "main-original\n")
+                    self.assertNotEqual(
+                        (selected_config / name).read_text(), "checkout-original\n"
+                    )
+
     def test_upgrade_required_failures_are_nonzero_and_independent(self) -> None:
         cases = (
             ("homebrew", "Darwin", []),
diff --git a/tests/unit/test_supply_chain_policy.py b/tests/unit/test_supply_chain_policy.py
index f7d3045..3b8f542 100644
--- a/tests/unit/test_supply_chain_policy.py
+++ b/tests/unit/test_supply_chain_policy.py
@@ -184,7 +184,51 @@ install_starship
         self.assertIn("locked = true", config)
         self.assertIn("lockfile = true", config)
         self.assertTrue((ROOT / "home/dot_mise/mise.lock").is_file())
-        self.assertTrue((ROOT / "home/dot_config/mise/symlink_mise.lock.tmpl").is_file())
+        for name in ("config.toml", "mise.lock"):
+            self.assertFalse((ROOT / f"home/dot_config/mise/symlink_{name}.tmpl").exists())
+            template = ROOT / f"home/dot_config/mise/{name}.tmpl"
+            self.assertTrue(template.is_file())
+            with tempfile.TemporaryDirectory() as temporary:
+                config = Path(temporary) / "chezmoi.toml"
+                config.write_text("")
+                result = subprocess.run(
+                    ["chezmoi", "--config", str(config), "--source", str(ROOT / "home"),
+                     "execute-template", template.read_text()],
+                    check=True, capture_output=True,
+                )
+            self.assertEqual(result.stdout, (ROOT / f"home/dot_mise/{name}").read_bytes())
+
+    def test_mise_apply_replaces_live_symlinks_with_independent_copies(self):
+        with tempfile.TemporaryDirectory() as temporary:
+            fixture = Path(temporary)
+            source = fixture / "source"
+            destination = fixture / "home"
+            managed = source / "dot_config/mise"
+            applied = destination / ".config/mise"
+            pins = source / "dot_mise"
+            for directory in (managed, applied, pins):
+                directory.mkdir(parents=True)
+            for name in ("config.toml", "mise.lock"):
+                (pins / name).write_bytes((ROOT / f"home/dot_mise/{name}").read_bytes())
+                (managed / f"{name}.tmpl").write_text(
+                    (ROOT / f"home/dot_config/mise/{name}.tmpl").read_text()
+                )
+                (applied / name).symlink_to(pins / name)
+            config = fixture / "chezmoi.toml"
+            config.write_text("")
+            subprocess.run(
+                ["chezmoi", "--config", str(config), "--source", str(source),
+                 "--destination", str(destination), "--persistent-state", str(fixture / "state.boltdb"),
+                 "apply", "--force"],
+                check=True, capture_output=True,
+            )
+            for name in ("config.toml", "mise.lock"):
+                self.assertFalse((applied / name).is_symlink())
+                self.assertEqual((applied / name).read_bytes(), (pins / name).read_bytes())
+                (applied / name).write_text("runtime-only change\n")
+                self.assertEqual(
+                    (pins / name).read_bytes(), (ROOT / f"home/dot_mise/{name}").read_bytes()
+                )
 
     def test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts(self):
         with (ROOT / "home/dot_mise/config.toml").open("rb") as config_file:
```

### `git show --format='%h %s%n%b' c11035f`

```text
c11035f fix(update): tolerate a herdr protocol mismatch on reload; align docs and dev image (#174)
- `make update` captures the herdr reload output and treats only a
  `protocol_mismatch` failure (CLI pinned ahead of a still-running server)
  as recoverable: it prints the restart/manual-reload instruction and
  continues; every other reload error still fails.
- README lifecycle, Crit, and herdr-agents sections now match the current
  implementation (pane split + agent start with worker_kind, gh extension
  convergence, CompactionDB sync, final agmsg bootstrap).
- Dockerfile moves to ubuntu:24.04, drops apt bats (CI-only policy), and
  reuses the image's default UID/GID 1000 account.
- update-agent-assets.sh header describes its actual duties; parity policy
  numbering is sequential.

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>

diff --git a/Dockerfile b/Dockerfile
index b56ef87..80512e2 100644
--- a/Dockerfile
+++ b/Dockerfile
@@ -1,4 +1,4 @@
-FROM ubuntu:22.04
+FROM ubuntu:24.04
 
 ARG USERNAME=mryfmo
 ARG USER_UID=1000
@@ -11,15 +11,19 @@ RUN apt-get update && \
     apt-get install -y --no-install-recommends \
     curl \
     git \
-    bats \
     sudo \
     tzdata \
     parallel \
     build-essential \
     ca-certificates
 
-RUN groupadd --gid $USER_GID $USERNAME \
-    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -G sudo -s /bin/bash \
+RUN existing_group="$(getent group "$USER_GID" | cut -d: -f1)" \
+    && if [ -n "$existing_group" ]; then groupmod --new-name "$USERNAME" "$existing_group"; else groupadd --gid "$USER_GID" "$USERNAME"; fi \
+    && existing_user="$(getent passwd "$USER_UID" | cut -d: -f1)" \
+    && if [ -n "$existing_user" ]; then usermod --login "$USERNAME" --home "/home/$USERNAME" --move-home --gid "$USER_GID" "$existing_user"; else useradd --uid "$USER_UID" --gid "$USER_GID" -m "$USERNAME" -s /bin/bash; fi \
+    && usermod --append --groups sudo "$USERNAME" \
+    && mkdir -p "/home/$USERNAME/.local/share/chezmoi" \
+    && chown -R "$USER_UID:$USER_GID" "/home/$USERNAME" \
     && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
 
 USER $USERNAME
diff --git a/Makefile b/Makefile
index e4ea632..9610418 100644
--- a/Makefile
+++ b/Makefile
@@ -86,7 +86,16 @@ update:
 		exit 1; \
 	fi; \
 	case "$$server_status" in \
-		running) herdr server reload-config ;; \
+		running) \
+			if reload_output="$$(herdr server reload-config 2>&1)"; then \
+				[ -z "$$reload_output" ] || printf '%s\n' "$$reload_output"; \
+			else \
+				[ -z "$$reload_output" ] || printf '%s\n' "$$reload_output" >&2; \
+				case "$$reload_output" in \
+					*protocol_mismatch*) printf '%s\n' "Herdr was updated; restart the server with 'herdr server stop' or recreate the Ghostty session, then run 'herdr server reload-config' manually." >&2 ;; \
+					*) exit 1 ;; \
+				esac; \
+			fi ;; \
 		not_running) echo "Herdr server is not running; skipping config reload." ;; \
 		*) echo "Unknown or missing Herdr server status: $${server_status:-<missing>}" >&2; exit 1 ;; \
 	esac
diff --git a/README.md b/README.md
index f55ac3e..c287a42 100644
--- a/README.md
+++ b/README.md
@@ -129,7 +129,7 @@ bash -c "$(curl -fsLS https://raw.githubusercontent.com/mryfmo/dotfiles/main/set
 # sourceDir.
 cd "$(git -C "$(chezmoi source-path)" rev-parse --show-toplevel)"
 
-# Update and apply managed dotfiles without upgrading tools.
+# Update and apply committed pinned state without advancing tool pins.
 make update
 
 # Inspect the current tool state without modifying it.
@@ -157,10 +157,14 @@ reason and the exact manual `git -C <repo> pull` command, then continues with
 the local source; a failed fast-forward pull also warns and continues. It then
 ensures the locked Node/npm runtime is installed before the two locked
 statusline tools required by the applied config, without upgrading other tools.
-After assets are refreshed, it reloads a running Herdr server, skips reload when
-the server is reported as not running or the command is unavailable, and fails
-on ambiguous status or reload errors. After
-correcting a reload error, run `herdr server reload-config` manually.
+The asset refresh also converges configured GitHub CLI extensions and syncs the
+vendored CompactionDB tree. It then reloads a running Herdr server, skips reload
+when the server is reported as not running or the command is unavailable, and
+fails on ambiguous status or reload errors other than `protocol_mismatch`. A
+protocol mismatch after updating Herdr prints instructions to stop and restart
+the server (or recreate the Ghostty session), then continues successfully; run
+`herdr server reload-config` manually after restarting. Finally,
+`make agmsg-bootstrap` converges repository-scoped agent message delivery hooks.
 
 Weekly model-usage measurement is informational and never changes
 `model_profiles`. Capture or report usage manually with:
@@ -184,7 +188,8 @@ Any model-profile decision still requires manual quality review and a PR.
 
 ### Agent review and permission assets
 
-`make update` also refreshes agent-managed assets after `chezmoi apply`.
+`make update` also refreshes agent-managed assets, configured GitHub CLI
+extensions, and the vendored CompactionDB tree after `chezmoi apply`.
 The generated `create_marketplace.json` seeds `~/.agents/plugins/marketplace.json`
 only when it is missing; plugin runtimes own later content and mode changes.
 This includes the Crit integrations, the Ponytail (`ponytail@ponytail`) plugin,
@@ -201,7 +206,10 @@ linked skill); Codex runtime files are provisioned from the version-matched Clau
 On Linux, Crit itself is installed from the pinned amd64 or arm64 GitHub
 release binary after SHA-256 verification; macOS continues to use Homebrew.
 Both Linux checksums and the version live in `scripts/lib/installer-pins.sh`
-and are refreshed by `make upgrade`.
+and are refreshed by `make upgrade`. Linux lifecycle checks inspect the
+authoritative `~/.local/bin/crit` directly, prepend `~/.local/bin` to `PATH`,
+and run `hash -r` so an older ambient Crit cannot shadow it. If that managed
+binary is missing, `REPAIR=1 make doctor` can restore it.
 
 The zenbu-labs terminal tools — terminal-code (`tode`) and `terminal-browser` —
 install through their sha256-verified upstream curl installers, pinned by
@@ -302,8 +310,10 @@ lifecycle: dedicated workspace creation, pane wait/prompt handling, layout
 repair, and attach-mode healing. A claude worker also gets an unattended
 `Down`+`Enter` sent to its workspace-trust dialog on first start, since that
 dialog otherwise defaults to "No" and exits. Attach mode renames the current
-Claude pane, starts the worker with `--split right` when it is missing, and
-repairs pane order (Claude left) and the 50/50 ratio, refusing any repair
+Claude pane, creates a missing worker pane with
+`herdr pane split <claude-pane> --direction right --cwd <worktree>`, then starts
+the worker with `herdr agent start <name> --kind <worker_kind> --pane <id>`.
+It repairs pane order (Claude left) and the 50/50 ratio, refusing any repair
 when the layout is ambiguous or contains unmanaged panes. Unmanaged panes —
 such as a legacy `files` pane restored from a pre-two-pane persisted session
 — are deliberately preserved, never closed, split, or reused. Full mode
@@ -324,9 +334,11 @@ follows `interactive_profile` in `home/dot_agents/agent-config.yaml`,
 escalating with `/model` and `/effort` only at task boundaries. Parallelism
 never adds panes
 to this workspace: one git worktree equals one resident worker in its own
-tab/workspace (started with `herdr agent start <agent-name> --cwd <worktree>`), completion
-is detected only through agmsg RESULT messages, and about three concurrent
-workers is the practical supervision ceiling.
+tab/workspace. Its pane receives the worktree through
+`herdr pane split <pane> --direction right --cwd <worktree>`, and its worker
+starts with `herdr agent start <name> --kind <worker_kind> --pane <id>`.
+Completion is detected only through agmsg RESULT messages, and about three
+concurrent workers is the practical supervision ceiling.
 
 New workspaces no longer create a persistent files pane; `prefix+f` opens the
 on-demand `herdr-file-viewer` popup instead. A legacy `files` pane restored
@@ -352,8 +364,10 @@ that Ghostty does not auto-start Herdr, `herdr-session`, bare `herdr` routing in
 Ghostty, argumented `herdr` routing in Ghostty, bare `herdr` routing outside
 Ghostty, and the Herdr `prefix+alt+a` command binding. Its sandbox E2E fakes
 Herdr deeply enough to execute fake Claude Code and Codex commands, verifies
-Claude Code is run in the root pane, Codex is started with `--split right` under the
-`codex-worker-${workspace_id}` Herdr agent name, covers existing workspace
+Claude Code is run in the root pane, and verifies a right-side worker pane is
+created with `pane split --direction right --cwd` before
+`agent start --kind <worker_kind> --pane` launches the
+`<worker_kind>-worker-${workspace_id}` Herdr agent. It also covers existing workspace
 focus and missing-agent repair paths, verifies the session entrypoint still
 attaches after `herdr-agents` failure, and proves agmsg is usable by sending a
 message from fake Claude Code to fake Codex through a temporary agmsg database.
diff --git a/home/dot_agents/README.md b/home/dot_agents/README.md
index 7e78409..f23409b 100644
--- a/home/dot_agents/README.md
+++ b/home/dot_agents/README.md
@@ -34,7 +34,7 @@ Generated files include:
 5. Public dotfiles must not contain token literals. Credential-bearing servers inherit environment variables or refer to private configuration only.
 6. Claude plugins are not enabled by `settings.json` unless this repository also installs the marketplace/plugin. Shared workflows should live in skills first.
 7. Do not hand-edit generated files unless you immediately move the change back into `agent-config.yaml` and regenerate.
-9. For implementation tasks shared between Codex and Claude Code, use separate worktrees or make one agent a reviewer; do not let both write to the same worktree. This is an operational guideline and is intentionally not enforced by `validate-agent-assets.py`.
+8. For implementation tasks shared between Codex and Claude Code, use separate worktrees or make one agent a reviewer; do not let both write to the same worktree. This is an operational guideline and is intentionally not enforced by `validate-agent-assets.py`.
 
 ## Codex runtime state
 
diff --git a/scripts/update-agent-assets.sh b/scripts/update-agent-assets.sh
index 924bb62..c605628 100755
--- a/scripts/update-agent-assets.sh
+++ b/scripts/update-agent-assets.sh
@@ -3,10 +3,10 @@
 # @file scripts/update-agent-assets.sh
 # @brief Install and refresh shared AI-agent plugins and skills.
 # @description
-#   Keeps Codex and Claude Code agent assets aligned with the dotfiles-managed
-#   skill tree. Skills are applied by chezmoi from `home/dot_agents/skills`;
-#   this script handles CLI-managed plugin marketplace refreshes and plugin
-#   installation that cannot be represented as plain files.
+#   Converges Codex and Claude Code marketplaces and plugins, GitHub CLI
+#   extensions, pinned Crit/tode/terminal-browser releases, the vendored
+#   CompactionDB tree, and Herdr integrations that cannot be represented as
+#   plain chezmoi-managed files.
 
 set -Eeuo pipefail
 
diff --git a/tests/install/common/lifecycle.bats b/tests/install/common/lifecycle.bats
index 5879cd5..d2b0b1e 100644
--- a/tests/install/common/lifecycle.bats
+++ b/tests/install/common/lifecycle.bats
@@ -25,6 +25,7 @@ function run_update_fixture() {
     local git_dirty="${10:-0}"
     local git_pull_exit="${11:-0}"
     local git_unmerged="${12:-0}"
+    local reload_output="${13:-}"
     local fixture="${BATS_TEST_TMPDIR}/update-${BATS_TEST_NUMBER}"
 
     mkdir -p "${fixture}/bin" "${fixture}/scripts" \
@@ -73,6 +74,7 @@ if [[ \$1 == status ]]; then
     esac
     exit ${status_exit}
 fi
+printf '%s\n' '${reload_output}' >&2
 exit ${reload_exit}
 EOF
     chmod +x "${fixture}/bin/chezmoi" "${fixture}/bin/git" "${fixture}/bin/mise" "${fixture}/bin/herdr" \
@@ -186,11 +188,19 @@ herdr server reload-config" ]
 }
 
 @test "[common] update propagates Herdr reload failure" {
-    run_update_fixture running 0 23
+    run_update_fixture running 0 23 0 0 0 "" feature/test origin/feature/test 0 0 0 "reload failed"
     [ "$status" -ne 0 ]
     [ "$(grep -c '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls")" -eq 1 ]
 }
 
+@test "[common] update tolerates a Herdr protocol mismatch and explains recovery" {
+    run_update_fixture running 0 23 0 0 0 "" feature/test origin/feature/test 0 0 0 \
+        "protocol_mismatch: client protocol 20 is older than server protocol 22"
+    [ "$status" -eq 0 ]
+    [[ "$output" == *"Herdr was updated; restart the server with 'herdr server stop' or recreate the Ghostty session, then run 'herdr server reload-config' manually."* ]]
+    [ "$(grep -c '^herdr server reload-config$' "${UPDATE_FIXTURE}/calls")" -eq 1 ]
+}
+
 @test "[common] update does not reload after apply or asset failure" {
     run_update_fixture running 0 0 19
     [ "$status" -ne 0 ]
```

### `git show --format='%h %s%n%b' c5240c3`

```text
c5240c3 feat(agmsg): add agmsg-dispatch to send, wake an idle worker, and verify receipt (#173)
* feat(agmsg): add agmsg-dispatch to send, wake an idle worker, and verify receipt

Codex turn-mode delivery only fires when a turn ends, so any message
sent to an idle worker sits unread until something starts a new turn.
Three stalls of 5-15 minutes in one session came from bare send.sh calls
to an idle pane. agmsg-dispatch sends through send.sh, wakes the pane
with a metadata-only inbox prompt when it is not working, and blocks
until that message's read_at is set (one retry, bounded timeout). The
orchestration skill now names it as the required path.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

* fix(agmsg-dispatch): validate the pane first, share one deadline, recheck status before retry

Codex review on #173: resolve the pane before send.sh so a bad pane id
inserts nothing; one AGMSG_DISPATCH_TIMEOUT budget across both waits with
a halfway status recheck (a pane that went idle after the send is now
woken); every post-send failure reports the sent message id so a retry
never duplicates; the skill keeps send.sh + read_at verification as the
path for pane-less workers.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>

diff --git a/home/dot_agents/skills/agmsg-orchestration/SKILL.md b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
index 776523a..20cbcea 100644
--- a/home/dot_agents/skills/agmsg-orchestration/SKILL.md
+++ b/home/dot_agents/skills/agmsg-orchestration/SKILL.md
@@ -115,7 +115,7 @@ AGMSG-PONG v1 task_id=<id> status=alive|blocked note=<short-note>
 3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns.
 4. Start worker panes if needed. With herdr, wake or prompt a worker with `herdr pane run <pane_id> "<text>"` (text plus Enter in one call). Do not use `pane send-text` followed by `send-keys Enter`; the separate Enter races the TUI composer and fails nondeterministically. After every wake, verify delivery via the messages.db `read_at` column and only escalate to a pane restart if a verified `pane run` wake stays undelivered.
 5. Configure delivery deliberately. `delivery.sh set turn` is useful for turn-end inbox checks; changing delivery mode can kill project watcher processes, so do it before starting long-running project watchers.
-6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`.
+6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. When the worker has a Herdr pane, use `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` for orchestrator messages, including acceptance and revisions: it validates the pane before sending, wakes an idle pane with a generic inbox prompt, and blocks until that message's `read_at` is set. It polls at most every five seconds within one `AGMSG_DISPATCH_TIMEOUT` budget (default 120 seconds), rechecks pane status halfway through for one possible retry, and reports the sent message ID on delivery failure; verify that receipt before resending. It honors `AGMSG_STORAGE_PATH`. A bare `send.sh` to an idle Herdr worker is a protocol violation; pane-less workers keep `send.sh <team> <from> <to> "<message>"` plus explicit `read_at` verification through their configured delivery path.
 7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
 8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
 9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
diff --git a/home/dot_local/bin/common/executable_agmsg-dispatch b/home/dot_local/bin/common/executable_agmsg-dispatch
new file mode 100644
index 0000000..9ba1976
--- /dev/null
+++ b/home/dot_local/bin/common/executable_agmsg-dispatch
@@ -0,0 +1,100 @@
+#!/usr/bin/env bash
+# @file agmsg-dispatch
+# @brief Send an agmsg message, wake an idle worker, and verify receipt.
+# @description Uses the installed agmsg storage helpers. Polls every five seconds
+#   for AGMSG_DISPATCH_TIMEOUT seconds (default 120), retrying an idle wake once.
+#   The retry shares the original deadline and rechecks the pane's current state.
+#   Only routing metadata, never the message body, is sent to the terminal.
+# @arg $1 string Team identifier.
+# @arg $2 string Sender identifier.
+# @arg $3 string Recipient identifier.
+# @arg $4 string Herdr pane identifier.
+# @arg $@ string Message words, joined with spaces.
+# @example agmsg-dispatch project claude codex w1:p2 'AGMSG-TASK v1 ...'
+set -euo pipefail
+
+usage='agmsg-dispatch <team> <from> <to> <pane_id> <message...>'
+if (($# < 5)); then
+    printf 'Usage: %s\n' "$usage" >&2
+    exit 1
+fi
+team=$1 from=$2 to=$3 pane=$4
+shift 4
+scripts="${HOME}/.agents/skills/agmsg/scripts"
+# shellcheck source=/dev/null
+source "$scripts/lib/identifier.sh"
+agmsg_validate_identifiers "$usage" "$team" "$from" "$to"
+timeout=${AGMSG_DISPATCH_TIMEOUT:-120}
+if [[ ! $timeout =~ ^[1-9][0-9]{0,5}$ ]]; then
+    printf 'agmsg-dispatch: timeout must be a positive integer up to 999999 seconds\n' >&2
+    exit 1
+fi
+# shellcheck source=/dev/null
+source "$scripts/lib/storage.sh"
+db=$(agmsg_db_path)
+
+# @description Resolve exactly one existing pane before sending or retrying.
+get_pane_status() {
+    herdr pane list | jq -er --arg pane "$pane" \
+        '[.result.panes[] | select(.pane_id == $pane)] | if length == 1 then .[0].agent_status | strings else empty end'
+}
+if ! pane_status=$(get_pane_status); then
+    printf 'agmsg-dispatch: pane not found or unavailable: %s\n' "$pane" >&2
+    exit 1
+fi
+if ! bash "$scripts/send.sh" "$team" "$from" "$to" "$*" > /dev/null 2>&1; then
+    printf 'agmsg-dispatch: send failed\n' >&2
+    exit 1
+fi
+# @description Identify an already-sent message on any subsequent failure.
+# shellcheck disable=SC2329 # Invoked indirectly by the EXIT trap.
+report_delivery_failure() {
+    if (($? != 0)); then
+        printf 'agmsg-dispatch: sent message %s; delivery failed or unread; verify receipt before resending\n' "${message_id:-unknown}" >&2
+    fi
+}
+trap 'report_delivery_failure' EXIT
+# ponytail: one sender per route; send.sh must return an id before concurrent same-route dispatch.
+message_id=$(sqlite3 -cmd '.timeout 5000' "$db" "SELECT max(id) FROM messages WHERE team='$team' AND from_agent='$from' AND to_agent='$to';")
+if [[ ! $message_id =~ ^[0-9]+$ ]]; then
+    printf 'agmsg-dispatch: sent message id not found\n' >&2
+    exit 1
+fi
+
+# @description Wake the worker with metadata and its actual inbox command.
+wake() {
+    herdr pane run "$pane" "agmsg: new message $message_id for $to — run ~/.agents/skills/agmsg/scripts/inbox.sh $team $to" > /dev/null
+}
+
+# @description Wait for this message's read receipt within the timeout.
+# @arg $1 integer Stop polling at this SECONDS value, capped by the shared deadline.
+wait_for_read() {
+    local until=$1 remaining receipt
+    while true; do
+        receipt=$(sqlite3 "$db" "SELECT read_at IS NOT NULL FROM messages WHERE id=$message_id;") || exit 1
+        if [[ $receipt == 1 ]]; then
+            return 0
+        fi
+        remaining=$((until - SECONDS))
+        ((remaining > 0)) || return 1
+        ((remaining <= 5)) || remaining=5
+        sleep "$remaining"
+    done
+}
+
+deadline=$((SECONDS + timeout))
+retry_at=$((SECONDS + timeout / 2))
+if [[ $pane_status != working ]]; then
+    wake
+fi
+if wait_for_read "$retry_at"; then
+    exit 0
+fi
+pane_status=$(get_pane_status)
+if [[ $pane_status != working ]]; then
+    wake
+fi
+if wait_for_read "$deadline"; then
+    exit 0
+fi
+exit 1
diff --git a/tests/unit/test_agmsg_dispatch.py b/tests/unit/test_agmsg_dispatch.py
new file mode 100644
index 0000000..b3f8a6d
--- /dev/null
+++ b/tests/unit/test_agmsg_dispatch.py
@@ -0,0 +1,165 @@
+"""Exercise dispatch with isolated storage and fake agent CLIs."""
+
+import os
+import shutil
+import sqlite3
+import subprocess
+import tempfile
+import time
+import unittest
+from pathlib import Path
+
+ROOT = Path(__file__).resolve().parents[2]
+SCRIPT = ROOT / "home/dot_local/bin/common/executable_agmsg-dispatch"
+LIB = ROOT / "home/dot_agents/skills/agmsg/scripts/lib"
+
+
+class AgmsgDispatchTest(unittest.TestCase):
+    def setUp(self):
+        self.temp = tempfile.TemporaryDirectory()
+        self.addCleanup(self.temp.cleanup)
+        self.root = Path(self.temp.name)
+        scripts = self.root / ".agents/skills/agmsg/scripts"
+        (scripts / "lib").mkdir(parents=True)
+        for name in ("storage.sh", "identifier.sh"):
+            shutil.copyfile(LIB / name, scripts / "lib" / name)
+        self.db = self.root / "alternate/messages.db"
+        self.db.parent.mkdir()
+        with sqlite3.connect(self.db) as db:
+            db.execute("""CREATE TABLE messages (
+                id INTEGER PRIMARY KEY AUTOINCREMENT, team TEXT NOT NULL,
+                from_agent TEXT NOT NULL, to_agent TEXT NOT NULL, body TEXT NOT NULL,
+                created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
+                read_at TEXT)""")
+        self.calls = self.root / "calls"
+        self.calls.write_text("")
+        self.write_script(scripts / "send.sh", r"""
+source "$(dirname "$0")/lib/storage.sh"
+body="${4//\'/\'\'}"
+sqlite3 "$(agmsg_db_path)" "INSERT INTO messages(team,from_agent,to_agent,body) VALUES ('$1','$2','$3','$body');"
+if [[ ${FAKE_STATUS} == working && ${FAKE_READ} == yes ]]; then
+    sqlite3 "$(agmsg_db_path)" "UPDATE messages SET read_at='read';"
+fi
+""")
+        bindir = self.root / "bin"
+        bindir.mkdir()
+        self.write_script(bindir / "herdr", """
+if [[ $1 == pane && $2 == list ]]; then
+    pane_status=$FAKE_STATUS
+    listed=$(cat "$FAKE_CALLS.list" 2>/dev/null || printf 0)
+    printf '%s' "$((listed + 1))" > "$FAKE_CALLS.list"
+    if [[ -n ${FAKE_AFTER_STATUS:-} && $listed -gt 0 ]]; then
+        pane_status=$FAKE_AFTER_STATUS
+    fi
+    printf '{"result":{"panes":[{"pane_id":"%s","agent_status":"%s"}]}}\n' "${FAKE_PANE:-w1:p1}" "$pane_status"
+else
+    printf '%s\n' "$*" >> "$FAKE_CALLS"
+    [[ ${FAKE_WAKE_FAIL:-no} != yes ]] || exit 9
+    if [[ $FAKE_READ == yes || ${FAKE_WAKE_READ:-no} == yes ]]; then
+        sqlite3 "$AGMSG_STORAGE_PATH/messages.db" "UPDATE messages SET read_at='read';"
+    fi
+fi
+""")
+        self.env = dict(os.environ, HOME=str(self.root),
+                        PATH=f"{bindir}:{os.environ['PATH']}",
+                        AGMSG_STORAGE_PATH=str(self.db.parent),
+                        AGMSG_DISPATCH_TIMEOUT="1", FAKE_CALLS=str(self.calls),
+                        FAKE_STATUS="idle", FAKE_READ="yes")
+
+    def write_script(self, path, body):
+        path.write_text("#!/usr/bin/env bash\nset -eu\n" + body)
+        path.chmod(0o755)
+
+    def dispatch(self):
+        return subprocess.run(
+            ["bash", str(SCRIPT), "team", "sender", "worker", "w1:p1",
+             "private-message-body"], env=self.env, capture_output=True,
+            text=True, timeout=10)
+
+    def test_idle_wakes_once_and_reads(self):
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 0, result.stderr)
+        calls = self.calls.read_text().splitlines()
+        self.assertEqual(len(calls), 1)
+        self.assertIn("inbox.sh team worker", calls[0])
+        self.assertNotIn("private-message-body", calls[0] + result.stdout + result.stderr)
+        with sqlite3.connect(self.db) as db:
+            self.assertEqual(db.execute("SELECT body FROM messages").fetchone()[0],
+                             "private-message-body")
+
+    def test_working_does_not_wake(self):
+        self.env["FAKE_STATUS"] = "working"
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 0, result.stderr)
+        self.assertEqual(self.calls.read_text(), "")
+
+    def test_unread_retries_once_then_fails(self):
+        self.env["FAKE_READ"] = "no"
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 1)
+        self.assertIn("unread", result.stderr)
+        self.assertEqual(len(self.calls.read_text().splitlines()), 2)
+        self.assertNotIn("private-message-body", result.stdout + result.stderr)
+
+    def test_working_unread_never_wakes(self):
+        self.env.update(FAKE_STATUS="working", FAKE_READ="no")
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 1)
+        self.assertIn("unread", result.stderr)
+        self.assertEqual(self.calls.read_text(), "")
+
+    def test_default_store_uses_shared_helper(self):
+        default_db = self.root / ".agents/skills/agmsg/db/messages.db"
+        default_db.parent.mkdir()
+        shutil.move(self.db, default_db)
+        del self.env["AGMSG_STORAGE_PATH"]
+        self.env["FAKE_STATUS"] = "working"
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 0, result.stderr)
+
+    def test_invalid_timeout_does_not_send(self):
+        self.env["AGMSG_DISPATCH_TIMEOUT"] = "1+1"
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 1)
+        with sqlite3.connect(self.db) as db:
+            self.assertEqual(db.execute("SELECT count(*) FROM messages").fetchone()[0], 0)
+
+    def test_worker_becoming_idle_after_send_is_woken(self):
+        self.env.update(FAKE_STATUS="working", FAKE_AFTER_STATUS="idle",
+                        FAKE_READ="no", FAKE_WAKE_READ="yes")
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 0, result.stderr)
+        self.assertEqual(len(self.calls.read_text().splitlines()), 1)
+
+    def test_retry_does_not_wake_newly_working_pane(self):
+        self.env.update(FAKE_AFTER_STATUS="working", FAKE_READ="no")
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 1)
+        self.assertEqual(len(self.calls.read_text().splitlines()), 1)
+
+    def test_timeout_is_one_shared_budget(self):
+        self.env.update(FAKE_READ="no", AGMSG_DISPATCH_TIMEOUT="2")
+        started = time.monotonic()
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 1)
+        self.assertLess(time.monotonic() - started, 3.0)
+        self.assertIn("sent message 1;", result.stderr)
+
+    def test_missing_pane_inserts_nothing(self):
+        self.env["FAKE_PANE"] = "w1:p9"
+        result = self.dispatch()
+        self.assertEqual(result.returncode, 1)
+        self.assertIn("pane", result.stderr)
+        with sqlite3.connect(self.db) as db:
+            self.assertEqual(db.execute("SELECT count(*) FROM messages").fetchone()[0], 0)
+
+    def test_wake_failure_identifies_sent_message(self):
+        self.env["FAKE_WAKE_FAIL"] = "yes"
+        result = self.dispatch()
+        self.assertNotEqual(result.returncode, 0)
+        self.assertIn("sent message 1;", result.stderr)
+        self.assertNotIn("private-message-body", result.stderr)
+
+
+if __name__ == "__main__":
+    unittest.main()
```

### `git show --format='%h %s%n%b' 8276e9d`

```text
8276e9d fix(herdr): enable experimental kitty graphics for terminal tool panes (#146)
terminal-code (tode) and terminal-browser render pages into their panes
with the kitty graphics protocol, but herdr disables kitty graphics for
attached clients by default, so their panes stay blank. Enable the
experimental flag in the managed config; `terminal-browser setup` writes
the same key to the deployed config, and carrying it in the source
prevents chezmoi drift from reverting it on the next make update.


Claude-Session: https://claude.ai/code/session_01KV6hCqbPkhuJKvwHsJV4fC

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>

diff --git a/home/dot_config/herdr/config.toml b/home/dot_config/herdr/config.toml
index eeee47e..2aab346 100644
--- a/home/dot_config/herdr/config.toml
+++ b/home/dot_config/herdr/config.toml
@@ -48,3 +48,8 @@ command = '''PLUGIN_DIR="$(herdr plugin list --json | jq -r '.result.plugins[] |
 switch_ascii_input_source_in_prefix = true
 reveal_hidden_cursor_for_cjk_ime = true
 cjk_ime_agents = ["claude", "codex", "gemini", "cursor", "opencode", "hermes"]
+# Required for terminal-code (tode) and terminal-browser to render inside
+# herdr panes; without it their panes stay blank. Takes effect on client
+# (re)attach. `terminal-browser setup` writes the same key to the deployed
+# config, so keeping it here prevents chezmoi drift reverting it.
+kitty_graphics = true
```

### `git show --format='%h %s%n%b' 5b4fd8b`

```text
5b4fd8b fix(validate): skip nested git worktrees in the repo-wide scans (#176)
validate-agent-assets.py walked ROOT.rglob("*") for the removed-skill
and obvious-secret scans, so every file of every worktree checked out
under .claude/worktrees/ was scanned again and the exact-path fixture
allowlist no longer matched, producing false "possible committed secret"
failures on any machine with an active worktree (CI has none and passed).
Skip any path inside a nested git tree; red-first unit case for both
scans with .git as a file and as a directory.

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>

diff --git a/scripts/validate-agent-assets.py b/scripts/validate-agent-assets.py
index 87a92fb..8cfc105 100644
--- a/scripts/validate-agent-assets.py
+++ b/scripts/validate-agent-assets.py
@@ -8,6 +8,7 @@ import json
 import re
 import subprocess
 import sys
+from functools import cache
 from pathlib import Path
 from typing import Any
 
@@ -1033,6 +1034,14 @@ def validate_generated_agent_configs() -> None:
         fail(result.stdout.strip() or "generated agent configs are stale")
 
 
+@cache
+def is_nested_git_tree(directory: Path) -> bool:
+    """Check directory ancestors for a Git boundary, excluding ROOT itself."""
+    if directory == ROOT:
+        return False
+    return (directory / ".git").exists() or is_nested_git_tree(directory.parent)
+
+
 def validate_no_removed_claude_skill() -> None:
     removed_skill = "high-impact" + "-journal-publishing"
     matches = []
@@ -1041,6 +1050,8 @@ def validate_no_removed_claude_skill() -> None:
             continue
         if any(part in {".git", "site", "__pycache__"} for part in path.parts):
             continue
+        if is_nested_git_tree(path.parent):
+            continue
         if removed_skill in path.read_text(errors="ignore"):
             matches.append(path)
     if matches:
@@ -1082,6 +1093,8 @@ def validate_no_obvious_secrets() -> None:
             continue
         if any(part in {".git", "site", "__pycache__"} for part in path.parts):
             continue
+        if is_nested_git_tree(path.parent):
+            continue
         if path.relative_to(ROOT) in compactiondb_dummy_secret_fixtures:
             continue
         text = read_scannable_text(path)
diff --git a/tests/unit/test_validate_agent_assets.py b/tests/unit/test_validate_agent_assets.py
index e3c3f73..02bf6ae 100644
--- a/tests/unit/test_validate_agent_assets.py
+++ b/tests/unit/test_validate_agent_assets.py
@@ -44,6 +44,39 @@ class ValidateAgentAssetsTest(unittest.TestCase):
         self.module.ROOT = self.old_root
         shutil.rmtree(self.temp_dir)
 
+    def test_recursive_scans_skip_nested_git_trees_only(self) -> None:
+        (self.temp_dir / ".git").mkdir()
+        cases = (
+            ("validate_no_removed_claude_skill", "high-impact" + "-journal-publishing"),
+            ("validate_no_obvious_secrets", "ghp_" + "x" * 25),
+        )
+        for marker_kind in ("file", "directory"):
+            for scan_name, token in cases:
+                with self.subTest(marker_kind=marker_kind, scan=scan_name):
+                    nested = self.temp_dir / marker_kind / scan_name
+                    nested.mkdir(parents=True)
+                    marker = nested / ".git"
+                    if marker_kind == "file":
+                        marker.write_text("gitdir: /unused/worktree-metadata\n")
+                    else:
+                        marker.mkdir()
+                    deep_file = nested / "deep" / "nested.txt"
+                    deep_file.parent.mkdir()
+                    deep_file.write_text(token)
+                    scan = getattr(self.module, scan_name)
+                    with contextlib.redirect_stderr(io.StringIO()):
+                        scan()
+                    top_file = self.temp_dir / "top.txt"
+                    top_file.write_text(token)
+                    try:
+                        stderr = io.StringIO()
+                        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
+                            scan()
+                        self.assertIn("top.txt", stderr.getvalue())
+                        self.assertNotIn("nested.txt", stderr.getvalue())
+                    finally:
+                        top_file.unlink()
+
     def write_codex_config(
         self, sandbox_workspace_write: str, projects_toml: str = ""
     ) -> None:
```

### `git log -1 --format='%h %s%n%b' f95074a`

```text
f95074a chore(orchestration): sync 2026-09-25 session (T1 convergence, T2 pins, T3 mise symlink, T4 agmsg-dispatch, T5 ua-refresh, herdr-sheldon a02)
Task IDs covered: dot-update-convergence-T1-a01, dot-upgrade-pins-T2-a01,
dot-mise-symlink-T3-a01, dot-agmsg-dispatch-T4-a01, dot-ua-refresh-T5-a01
(blocked: FULL_UPDATE needs operator authorization), dot-herdr-sheldon-T1-a02
closing dot-herdr-sheldon-T1-a01 and dot-docs-align-T1-a01. Code landed via
PRs #170-#174.

Review: .agents/worklog/claude/orchestration-sync-2026-09-25-receipt.md

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

```

### `git log -1 --format='%h %s%n%b' d6cfed2`

```text
d6cfed2 chore(orchestration): sync T6 adh-baseline and T7 validator-worktrees records
Task IDs covered: dot-adh-baseline-T6-a01 (PR #175), dot-validator-worktrees-T7-a01
(PR #176). Review: .agents/worklog/claude/orchestration-sync-2026-09-25b-receipt.md

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

```

### `git log -1 --format='%h %s%n%b' 6775bb7`

```text
6775bb7 chore(orchestration): sync T8 dependabot-verify records
Task IDs covered: dot-dependabot-verify-T8-a01 (verdicts for #155 and #125).
Review: .agents/worklog/claude/orchestration-sync-2026-09-25c-receipt.md

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

```

### `git log -1 --format='%h %s%n%b' 3303fbc`

```text
3303fbc chore(orchestration): sync T9 ua-full-rebuild records
Task IDs covered: dot-ua-full-T9-a01 (graph merged via PR #177).
Review: .agents/worklog/claude/orchestration-sync-2026-09-25d-receipt.md

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

```

### `git log -1 --format='%h %s%n%b' 9baed29`

```text
9baed29 docs(adh): add the ADH Integrated Plan input baseline (#175)
Versions reviews/ADH_Integrated_Plan/ exactly as delivered: the READ-ONLY
input baseline for the ADH V4 program (AGENTS.md). All 197 SHA256SUMS
entries verify and every PACKAGE_MANIFEST.json file is present. No file
under it is edited; conflicts are handled as change requests in the ADH
program ledger, never here.

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
```

### `git log -1 --format='%h %s%n%b' b277a51`

```text
b277a51 chore(ua): full knowledge-graph rebuild at d906b00; exclude .orchestration and reviews (#177)
meta.json had been re-pinned by hand past the graph's real base (d91b835),
so incremental updates refused to run and a FULL_UPDATE was required.
Rebuilt with the plugin's full pipeline on current main. .orchestration/
(process records, previously a third of all nodes) and reviews/ (external
read-only baseline) are now excluded from the graph.

- 419 files analyzed (1,256 ignored); nodes 1,201 -> 1,399; edges 934 -> 2,398
- graph, fingerprints, and meta all pinned to d906b00 (worktree HEAD)
- inline validation: 0 issues; assemble-reviewer, architecture and tour run

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
```

### `git show --format= --dirstat=files,0 9baed29 | head; git show --format= --numstat 9baed29 -- reviews/ADH_Integrated_Plan/SHA256SUMS`

```text
   5.5% reviews/ADH_Integrated_Plan/artifacts/
   4.0% reviews/ADH_Integrated_Plan/contracts/
   9.0% reviews/ADH_Integrated_Plan/docs/
   2.0% reviews/ADH_Integrated_Plan/evaluation/control_prompts/
   4.0% reviews/ADH_Integrated_Plan/evaluation/
   5.0% reviews/ADH_Integrated_Plan/examples/
   1.0% reviews/ADH_Integrated_Plan/profiles/
   2.5% reviews/ADH_Integrated_Plan/prompts/
  14.6% reviews/ADH_Integrated_Plan/registers/
   0.5% reviews/ADH_Integrated_Plan/skill-pack/skills/adh-design-choice/references/
197	0	reviews/ADH_Integrated_Plan/SHA256SUMS
```

### `git show --format= --stat b277a51; git show --format= b277a51 -- .ua/meta.json .ua/.understandignore`

```text
 .ua/.understandignore    |     2 +
 .ua/fingerprints.json    | 20691 +++++++++------------
 .ua/knowledge-graph.json | 44294 +++++++++++++++++++++++++++++----------------
 .ua/meta.json            |     8 +-
 4 files changed, 38129 insertions(+), 26866 deletions(-)
diff --git a/.ua/.understandignore b/.ua/.understandignore
index 1263513..eb89a37 100644
--- a/.ua/.understandignore
+++ b/.ua/.understandignore
@@ -18,6 +18,8 @@ site/
 .DS_Store
 .agents/worklog/
 .agents/runs/
+.orchestration/
+reviews/
 *.pyc
 # .codex/
 # .crit/
diff --git a/.ua/meta.json b/.ua/meta.json
index 8d5840a..af73d1e 100644
--- a/.ua/meta.json
+++ b/.ua/meta.json
@@ -1,6 +1,6 @@
 {
-  "lastAnalyzedAt": "2026-08-29T09:12:43.546325+00:00",
-  "gitCommitHash": "13079e48cd4b86e0b57de6483303edef34ab5cce",
+  "lastAnalyzedAt": "2026-09-25T05:57:40.443Z",
+  "gitCommitHash": "d906b00bff8729625b895d6f7765e3186ab5bb86",
   "version": "1.0.0",
-  "analyzedFiles": 722
-}
\ No newline at end of file
+  "analyzedFiles": 419
+}
```

### `for h in f95074a d6cfed2 6775bb7 3303fbc; do echo "== $h"; git show --format= --name-only $h | cut -d/ -f2 | sort | uniq -c; done`

```text
== f95074a
      8 acceptance
      8 autoskill
      8 learning
      8 reports
      8 sandboxes
      8 tasks
      8 validation
== d6cfed2
      2 acceptance
      2 autoskill
      2 learning
      2 reports
      2 sandboxes
      2 tasks
      2 validation
== 6775bb7
      1 acceptance
      1 autoskill
      1 learning
      1 reports
      1 sandboxes
      1 tasks
      1 validation
== 3303fbc
      1 acceptance
      1 autoskill
      1 learning
      1 reports
      1 sandboxes
      1 tasks
      1 validation
```

### `git diff 455455e 126e465 -- home/dot_agents/agent-config.yaml scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py`

```text
diff --git a/home/dot_agents/agent-config.yaml b/home/dot_agents/agent-config.yaml
index 73ba08d..a66c944 100644
--- a/home/dot_agents/agent-config.yaml
+++ b/home/dot_agents/agent-config.yaml
@@ -52,6 +52,14 @@ model_profiles:
       model: gpt-daybreak-blue-latest
       model_reasoning_effort: high
       notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
+  remediation:
+    # references-kit remediation orchestrator: Fable 5.1 at reduced effort;
+    # workers stay on `standard`.
+    claude: { model: claude-fable-5-1, effort: medium }
+    codex:
+      model: gpt-5.6-terra
+      model_reasoning_effort: medium
+      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
   # ADH V4 program profile; fallback and effort downgrade are forbidden.
   # Edit here only; profiles/model_profiles.json is a validation view.
   adh:
diff --git a/scripts/validate-agent-assets.py b/scripts/validate-agent-assets.py
index 87a92fb..3fab06e 100644
--- a/scripts/validate-agent-assets.py
+++ b/scripts/validate-agent-assets.py
@@ -532,12 +532,19 @@ def validate_agent_manifest() -> dict[str, Any]:
         fail(f"{manifest_path} must enable the Crit Codex plugin")
     claude = manifest.get("claude", {})
     profiles = manifest.get("model_profiles", {})
-    required_profiles = {"express", "standard", "review", "deep", "security"}
+    required_profiles = {
+        "express",
+        "standard",
+        "review",
+        "deep",
+        "security",
+        "remediation",
+    }
     if not required_profiles <= set(profiles) or set(profiles) - required_profiles - {
         "adh"
     }:
         fail(
-            f"{manifest_path} must define the five base profiles and only the optional adh profile"
+            f"{manifest_path} must define the six base profiles and only the optional adh profile"
         )
     if profiles["security"].get("codex", {}).get("model") != "gpt-daybreak-blue-latest":
         fail(
@@ -1065,6 +1072,34 @@ def read_scannable_text(path: Path) -> str | None:
         return None
 
 
+def git_visible_files(root: Path) -> list[Path] | None:
+    """Every file `git` would let get committed from `root`: tracked files plus
+    untracked files not covered by .gitignore. Returns None (caller falls back to a
+    full filesystem walk) when `root` isn't a git repository or `git` is unavailable,
+    so a gitignored cache or virtualenv anywhere under `root` (e.g. an example
+    project's `.venv`) is never scanned."""
+    try:
+        result = subprocess.run(
+            [
+                "git",
+                "-C",
+                str(root),
+                "ls-files",
+                "-z",
+                "--cached",
+                "--others",
+                "--exclude-standard",
+            ],
+            capture_output=True,
+            check=False,
+        )
+    except OSError:
+        return None
+    if result.returncode != 0:
+        return None
+    return [root / part for part in result.stdout.decode("utf-8").split("\0") if part]
+
+
 def validate_no_obvious_secrets() -> None:
     allowed_secret_placeholders = {
         "GITHUB_PERSONAL_ACCESS_TOKEN",
@@ -1077,7 +1112,15 @@ def validate_no_obvious_secrets() -> None:
         Path("vendor/compactiondb/tests/test_redaction.py"),
         Path("vendor/compactiondb/.claude/contextdb/contextdb/redaction.py"),
     }
-    for path in ROOT.rglob("*"):
+    candidates = git_visible_files(ROOT)
+    if candidates is None:
+        print(
+            f"{ROOT} is not a git repository (or git is unavailable); "
+            "validate_no_obvious_secrets is scanning every file on disk instead",
+            file=sys.stderr,
+        )
+        candidates = list(ROOT.rglob("*"))
+    for path in candidates:
         if not path.is_file():
             continue
         if any(part in {".git", "site", "__pycache__"} for part in path.parts):
diff --git a/tests/unit/test_validate_agent_assets.py b/tests/unit/test_validate_agent_assets.py
index e3c3f73..e16cc45 100644
--- a/tests/unit/test_validate_agent_assets.py
+++ b/tests/unit/test_validate_agent_assets.py
@@ -8,6 +8,7 @@ import importlib.util
 import io
 import json
 import shutil
+import subprocess
 import sys
 import tempfile
 import unittest
@@ -85,7 +86,9 @@ class ValidateAgentAssetsTest(unittest.TestCase):
                                     {
                                         "type": "command",
                                         "command": command,
-                                        "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"],
+                                        "args": [
+                                            "${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"
+                                        ],
                                     }
                                 ],
                             }
@@ -155,7 +158,14 @@ class ValidateAgentAssetsTest(unittest.TestCase):
                 "claude": {"model": "claude-model", "effort": "high"},
                 "codex": {"model": "codex-model", "model_reasoning_effort": "high"},
             }
-            for name in ("express", "standard", "review", "deep", "security")
+            for name in (
+                "express",
+                "standard",
+                "review",
+                "deep",
+                "security",
+                "remediation",
+            )
         }
         profiles["security"]["codex"]["model"] = "gpt-daybreak-blue-latest"
         manifest = {
@@ -183,6 +193,13 @@ class ValidateAgentAssetsTest(unittest.TestCase):
         with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
             self.module.validate_agent_manifest()
 
+    def test_agent_manifest_rejects_missing_remediation_profile(self) -> None:
+        manifest = self.write_valid_agent_manifest()
+        del manifest["model_profiles"]["remediation"]
+
+        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
+            self.module.validate_agent_manifest()
+
     def test_agent_manifest_rejects_wrong_security_codex_model(self) -> None:
         manifest = self.write_valid_agent_manifest()
         manifest["model_profiles"]["security"]["codex"]["model"] = "gpt-5.6-sol"
@@ -474,6 +491,25 @@ class ValidateAgentAssetsTest(unittest.TestCase):
         with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
             self.module.validate_no_obvious_secrets()
 
+    def init_git_repo(self) -> None:
+        subprocess.run(["git", "init", "-q", str(self.temp_dir)], check=True)
+
+    def test_secret_scan_ignores_gitignored_files(self) -> None:
+        self.init_git_repo()
+        self.write_text_file(".gitignore", "ignored_secret.md\n")
+        self.write_text_file("tracked_clean.md", "nothing interesting here\n")
+        self.write_text_file("ignored_secret.md", "to" + 'ken = "real-secret"\n')
+
+        self.module.validate_no_obvious_secrets()
+
+    def test_secret_scan_checks_git_visible_files(self) -> None:
+        self.init_git_repo()
+        self.write_text_file(".gitignore", "ignored_secret.md\n")
+        self.write_text_file("visible_secret.md", "to" + 'ken = "real-secret"\n')
+
+        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
+            self.module.validate_no_obvious_secrets()
+
     def write_manifest(self, hook_command: str) -> None:
         path = self.temp_dir / "home/dot_agents/agent-config.yaml"
         path.parent.mkdir(parents=True, exist_ok=True)
```

### `git show b43e36b:home/dot_agents/agent-config.yaml | grep -n -E "^  remediation:|matcher: \"\\^\\(startup"`

```text
55:  remediation:
186:      - matcher: "^(startup|resume|clear|compact|fork)$"
```

### `git show b43e36b:scripts/validate-agent-assets.py | sed -n '1044,1068p;1114,1150p'`

```text
@cache
def is_nested_git_tree(directory: Path) -> bool:
    """Check directory ancestors for a Git boundary, excluding ROOT itself."""
    if directory == ROOT:
        return False
    return (directory / ".git").exists() or is_nested_git_tree(directory.parent)


def validate_no_removed_claude_skill() -> None:
    removed_skill = "high-impact" + "-journal-publishing"
    matches = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "site", "__pycache__"} for part in path.parts):
            continue
        if is_nested_git_tree(path.parent):
            continue
        if removed_skill in path.read_text(errors="ignore"):
            matches.append(path)
    if matches:
        fail(
            "removed Claude skill references remain: "
            + ", ".join(str(p.relative_to(ROOT)) for p in matches[:10])
        )
def validate_no_obvious_secrets() -> None:
    allowed_secret_placeholders = {
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "FIGMA_OAUTH_TOKEN",
    }
    # CompactionDB uses intentional dummy credentials to exercise its redaction boundary.
    compactiondb_dummy_secret_fixtures = {
        Path("vendor/compactiondb/validate.py"),
        Path("vendor/compactiondb/tests/test_migration.py"),
        Path("vendor/compactiondb/tests/test_redaction.py"),
        Path("vendor/compactiondb/.claude/contextdb/contextdb/redaction.py"),
    }
    candidates = git_visible_files(ROOT)
    if candidates is None:
        print(
            f"{ROOT} is not a git repository (or git is unavailable); "
            "validate_no_obvious_secrets is scanning every file on disk instead",
            file=sys.stderr,
        )
        candidates = list(ROOT.rglob("*"))
    for path in candidates:
        if not path.is_file():
            continue
        if any(part in {".git", "site", "__pycache__"} for part in path.parts):
            continue
        if is_nested_git_tree(path.parent):
            continue
        if path.relative_to(ROOT) in compactiondb_dummy_secret_fixtures:
            continue
        text = read_scannable_text(path)
        if text is None:
            continue
        sanitized = text
        for placeholder in allowed_secret_placeholders:
            sanitized = sanitized.replace(placeholder, "")
        if SECRET_PATTERN.search(sanitized):
            fail(f"possible committed secret in {path.relative_to(ROOT)}")
```

### `git show b43e36b:tests/unit/test_validate_agent_assets.py | grep -n -E '^import subprocess|def init_git_repo'`

```text
11:import subprocess
527:    def init_git_repo(self) -> None:
```

### `grep -c "    def test_" <(git show c5240c3:tests/unit/test_agmsg_dispatch.py)`

```text
11
```
