# T8 verbatim investigation evidence

## Final scope check

```sh
rg -n 'should_nix|flake.nix|flake.lock|nix/' .github/workflows/test.yaml
```

Exit: 0

```text
21:      should_nix: ${{ steps.filter.outputs.should_nix }}
72:          if git diff --name-only "${diff_range}" | grep -Eq '^(flake\.(nix|lock)$|nix/)'; then
73:            echo "should_nix=true" >> "${GITHUB_OUTPUT}"
75:            echo "should_nix=false" >> "${GITHUB_OUTPUT}"
376:    if: ${{ needs.changes.outputs.should_nix == 'true' }}

```

## Final scope check

```sh
git status --short
```

Exit: 0

```text
?? .orchestration/autoskill/runs/dot-dependabot-verify-T8-a01.md
?? .orchestration/learning/dot-dependabot-verify-T8-a01.md
?? .orchestration/reports/dot-dependabot-verify-T8-a01.md
?? .orchestration/sandboxes/dot-dependabot-verify-T8-a01.md
?? .orchestration/tasks/dot-dependabot-verify-T8-a01.md
?? .orchestration/validation/dot-dependabot-verify-T8-a01.md

```

## Final scope check

```sh
git diff --cached --stat
```

Exit: 0

```text

```

## Final scope check

```sh
git diff --stat
```

Exit: 0

```text

```

Outputs are preserved as returned, including ANSI sequences. Empty fences mean no output; exit status is recorded separately. No local Bats or Nix commands beyond availability detection were run.

## 1. Command

```sh
gh pr view 155 --repo mryfmo/dotfiles --json url,title,headRefName,headRefOid,baseRefName,state,files
```

Exit: 0

```text
[1;37m{[m
  [1;34m"baseRefName"[m[1;37m:[m [32m"main"[m[1;37m,[m
  [1;34m"files"[m[1;37m:[m [1;37m[[m
    [1;37m{[m
      [1;34m"path"[m[1;37m:[m [32m".github/workflows/agent-assets.yml"[m[1;37m,[m
      [1;34m"additions"[m[1;37m:[m 1[1;37m,[m
      [1;34m"deletions"[m[1;37m:[m 1[1;37m,[m
      [1;34m"changeType"[m[1;37m:[m [32m"MODIFIED"[m
    [1;37m}[m[1;37m,[m
    [1;37m{[m
      [1;34m"path"[m[1;37m:[m [32m".github/workflows/docs.yml"[m[1;37m,[m
      [1;34m"additions"[m[1;37m:[m 1[1;37m,[m
      [1;34m"deletions"[m[1;37m:[m 1[1;37m,[m
      [1;34m"changeType"[m[1;37m:[m [32m"MODIFIED"[m
    [1;37m}[m[1;37m,[m
    [1;37m{[m
      [1;34m"path"[m[1;37m:[m [32m".github/workflows/test.yaml"[m[1;37m,[m
      [1;34m"additions"[m[1;37m:[m 1[1;37m,[m
      [1;34m"deletions"[m[1;37m:[m 1[1;37m,[m
      [1;34m"changeType"[m[1;37m:[m [32m"MODIFIED"[m
    [1;37m}[m
  [1;37m][m[1;37m,[m
  [1;34m"headRefName"[m[1;37m:[m [32m"dependabot/github_actions/astral-sh/setup-uv-10.1.0"[m[1;37m,[m
  [1;34m"headRefOid"[m[1;37m:[m [32m"01c8bdd3ba593b83d2a960ebde3bcaf0c044c4c0"[m[1;37m,[m
  [1;34m"state"[m[1;37m:[m [32m"OPEN"[m[1;37m,[m
  [1;34m"title"[m[1;37m:[m [32m"chore(deps): bump astral-sh/setup-uv from 7.6.0 to 10.2.0"[m[1;37m,[m
  [1;34m"url"[m[1;37m:[m [32m"https://github.com/mryfmo/dotfiles/pull/155"[m
[1;37m}[m
```

## 2. Command

```sh
gh pr view 125 --repo mryfmo/dotfiles --json url,title,headRefName,headRefOid,baseRefName,state,files
```

Exit: 0

```text
[1;37m{[m
  [1;34m"baseRefName"[m[1;37m:[m [32m"main"[m[1;37m,[m
  [1;34m"files"[m[1;37m:[m [1;37m[[m
    [1;37m{[m
      [1;34m"path"[m[1;37m:[m [32m".github/workflows/test.yaml"[m[1;37m,[m
      [1;34m"additions"[m[1;37m:[m 1[1;37m,[m
      [1;34m"deletions"[m[1;37m:[m 1[1;37m,[m
      [1;34m"changeType"[m[1;37m:[m [32m"MODIFIED"[m
    [1;37m}[m
  [1;37m][m[1;37m,[m
  [1;34m"headRefName"[m[1;37m:[m [32m"dependabot/github_actions/cachix/install-nix-action-31.11.1"[m[1;37m,[m
  [1;34m"headRefOid"[m[1;37m:[m [32m"60c1be401180e96684903424bc4f8fc9567acd98"[m[1;37m,[m
  [1;34m"state"[m[1;37m:[m [32m"OPEN"[m[1;37m,[m
  [1;34m"title"[m[1;37m:[m [32m"chore(deps): bump cachix/install-nix-action from 31.10.7 to 31.11.1"[m[1;37m,[m
  [1;34m"url"[m[1;37m:[m [32m"https://github.com/mryfmo/dotfiles/pull/125"[m
[1;37m}[m
```

## 3. Command

```sh
gh run view 34730808923 --repo mryfmo/dotfiles --log-failed
```

Exit: 0

```text
test (macos-14, client)	UNKNOWN STEP	﻿2026-09-13T01:33:16.5368190Z Current runner version: '2.337.0'
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5384850Z ##[group]Runner Image Provisioner
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5385420Z Hosted Compute Agent
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5385880Z Version: 20260828.587
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5386480Z Commit: abac92662cab4cc7352de4f9f9d2e2419aad9c29
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5387050Z Build Date: 2026-08-28T16:44:25Z
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5387650Z Worker ID: {3f3a3fb5-47e6-4fe6-9a5c-65176ec5d1b9}
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5388180Z Azure Region: westus
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5388620Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5389560Z ##[group]Operating System
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5390080Z macOS
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5390420Z 14.8.9
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5390820Z 23J631
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5391260Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5391710Z ##[group]Runner Image
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5392270Z Image: macos-14-arm64
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5392750Z Version: 20260831.0302.1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5393740Z Included Software: https://github.com/actions/runner-images/blob/macos-14-arm64/20260831.0302/images/macos/macos-14-arm64-Readme.md
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5394920Z Image Release: https://github.com/actions/runner-images/releases/tag/macos-14-arm64%2F20260831.0302
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5395760Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5396690Z ##[group]GITHUB_TOKEN Permissions
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5398030Z Contents: read
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5398420Z Metadata: read
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5399030Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5400730Z Secret source: Dependabot
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5401500Z Cache mode: write
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5402000Z Prepare workflow directory
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5816300Z Prepare all required actions
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.5851360Z Getting action download info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:16.9119590Z Download action repository 'actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0' (SHA:9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:17.1569800Z Download action repository 'jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d' (SHA:e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:17.9892350Z Download action repository 'astral-sh/setup-uv@bec219d24cd3e171d82865faccec33120bb574f4' (SHA:bec219d24cd3e171d82865faccec33120bb574f4)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:18.7419590Z Download action repository 'codecov/codecov-action@fb8b3582c8e4def4969c97caa2f19720cb33a72f' (SHA:fb8b3582c8e4def4969c97caa2f19720cb33a72f)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:19.2907300Z Getting action download info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:19.3906070Z Download action repository 'actions/github-script@ed597411d8f924073f98dfc5c65a23a2325f34cd' (SHA:ed597411d8f924073f98dfc5c65a23a2325f34cd)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.0633250Z Complete job name: test (macos-14, client)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1275600Z ##[group]Run git config --global init.defaultBranch main
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1277970Z ^[[36;1mgit config --global init.defaultBranch main^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1392060Z shell: /bin/bash -e {0}
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1393070Z env:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1393670Z   OS: macos-14
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1394220Z   SYSTEM: client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1394960Z   CODECOV_FLAGS: macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1396900Z   CODECOV_NAME: codecov-dotfiles-macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1403050Z   GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.1404660Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2971680Z ##[group]Run actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2972550Z with:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2973090Z   persist-credentials: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2973700Z   repository: mryfmo/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2978370Z   token: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2978880Z   ssh-strict: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2979410Z   ssh-user: git
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2979940Z   clean: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2980500Z   sparse-checkout-cone-mode: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2981110Z   fetch-depth: 1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2981650Z   fetch-tags: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2982200Z   show-progress: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2982770Z   lfs: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2983300Z   submodules: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2983890Z   set-safe-directory: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2984540Z   allow-unsafe-pr-checkout: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2985200Z env:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2986240Z   OS: macos-14
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2986740Z   SYSTEM: client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2987330Z   CODECOV_FLAGS: macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2987990Z   CODECOV_NAME: codecov-dotfiles-macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2992750Z   GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.2993370Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.5992040Z Syncing repository: mryfmo/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.5993630Z ##[group]Getting Git version info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.5994420Z Working directory is '/Users/runner/work/dotfiles/dotfiles'
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.5995600Z [command]/opt/homebrew/bin/git version
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6011740Z git version 2.55.0
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6025600Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6030210Z Copying '/Users/runner/.gitconfig' to '/Users/runner/work/_temp/40791898-c880-46c7-abf8-b8a587391dbd/.gitconfig'
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6035230Z Temporarily overriding HOME='/Users/runner/work/_temp/40791898-c880-46c7-abf8-b8a587391dbd' before making global git config changes
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6036900Z Adding repository directory to the temporary git global config as a safe directory
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6038440Z [command]/opt/homebrew/bin/git config --global --add safe.directory /Users/runner/work/dotfiles/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6079570Z Deleting the contents of '/Users/runner/work/dotfiles/dotfiles'
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6081950Z ##[group]Determining repository object format
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6083150Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6084030Z ##[group]Initializing the repository
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6085570Z [command]/opt/homebrew/bin/git init /Users/runner/work/dotfiles/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6238180Z Initialized empty Git repository in /Users/runner/work/dotfiles/dotfiles/.git/
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6244300Z [command]/opt/homebrew/bin/git remote add origin https://github.com/mryfmo/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6295190Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6296240Z ##[group]Disabling automatic garbage collection
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6297250Z [command]/opt/homebrew/bin/git config --local gc.auto 0
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6456390Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6457350Z ##[group]Setting up auth
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6458180Z Removing SSH command configuration
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6460880Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp core\.sshCommand
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.6505390Z [command]/opt/homebrew/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.7109030Z Removing HTTP extra header
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.7116320Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.7154260Z [command]/opt/homebrew/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.7597430Z Removing includeIf entries pointing to credentials config files
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.7600300Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.7634810Z [command]/opt/homebrew/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.8114790Z [command]/opt/homebrew/bin/git config --file /Users/runner/work/_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config http.https://github.com/.extraheader AUTHORIZATION: basic ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.8173460Z [command]/opt/homebrew/bin/git config --local includeIf.gitdir:/Users/runner/work/dotfiles/dotfiles/.git.path /Users/runner/work/_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.8226590Z [command]/opt/homebrew/bin/git config --local includeIf.gitdir:/Users/runner/work/dotfiles/dotfiles/.git/worktrees/*.path /Users/runner/work/_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.8267340Z [command]/opt/homebrew/bin/git config --local includeIf.gitdir:/github/workspace/.git.path /github/runner_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.8306380Z [command]/opt/homebrew/bin/git config --local includeIf.gitdir:/github/workspace/.git/worktrees/*.path /github/runner_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.8342860Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.8343770Z ##[group]Fetching the repository
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:20.8347080Z [command]/opt/homebrew/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +b33aae52b51f3f9ad635a662472d6a1e93ab4099:refs/remotes/pull/155/merge
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6783050Z From https://github.com/mryfmo/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6784270Z  * [new ref]         b33aae52b51f3f9ad635a662472d6a1e93ab4099 -> pull/155/merge
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6786940Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6788090Z ##[group]Determining the checkout info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6789290Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6791300Z [command]/opt/homebrew/bin/git sparse-checkout disable
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6851580Z [command]/opt/homebrew/bin/git config --local --unset-all extensions.worktreeConfig
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6887830Z ##[group]Checking out the ref
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.6889800Z [command]/opt/homebrew/bin/git checkout --progress --force refs/remotes/pull/155/merge
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.8638490Z HEAD is now at b33aae5 Merge 1b1b976459e80e7025ba0f7ac535b36c356d1a33 into fdfa5f042e2e00a27a8320e5f37f749c422e8d91
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.8647880Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.8734020Z [command]/opt/homebrew/bin/git log -1 --format=%H
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.8764380Z b33aae52b51f3f9ad635a662472d6a1e93ab4099
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.8769690Z ##[group]Removing auth
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.8770020Z Removing SSH command configuration
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.8772490Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp core\.sshCommand
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.8815130Z [command]/opt/homebrew/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.9329440Z Removing HTTP extra header
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.9336000Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.9383730Z [command]/opt/homebrew/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.9864900Z Removing includeIf entries pointing to credentials config files
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.9866970Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:21.9909790Z includeif.gitdir:/Users/runner/work/dotfiles/dotfiles/.git.path
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0011200Z includeif.gitdir:/Users/runner/work/dotfiles/dotfiles/.git/worktrees/*.path
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0112550Z includeif.gitdir:/github/workspace/.git.path
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0151150Z includeif.gitdir:/github/workspace/.git/worktrees/*.path
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0152630Z [command]/opt/homebrew/bin/git config --local --get-all includeif.gitdir:/Users/runner/work/dotfiles/dotfiles/.git.path
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0153480Z /Users/runner/work/_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0155290Z [command]/opt/homebrew/bin/git config --local --unset includeif.gitdir:/Users/runner/work/dotfiles/dotfiles/.git.path /Users/runner/work/_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0156800Z [command]/opt/homebrew/bin/git config --local --get-all includeif.gitdir:/Users/runner/work/dotfiles/dotfiles/.git/worktrees/*.path
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0157570Z /Users/runner/work/_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0158880Z [command]/opt/homebrew/bin/git config --local --unset includeif.gitdir:/Users/runner/work/dotfiles/dotfiles/.git/worktrees/*.path /Users/runner/work/_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0160280Z [command]/opt/homebrew/bin/git config --local --get-all includeif.gitdir:/github/workspace/.git.path
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0184770Z /github/runner_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0190290Z [command]/opt/homebrew/bin/git config --local --unset includeif.gitdir:/github/workspace/.git.path /github/runner_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0226940Z [command]/opt/homebrew/bin/git config --local --get-all includeif.gitdir:/github/workspace/.git/worktrees/*.path
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0259490Z /github/runner_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0310230Z [command]/opt/homebrew/bin/git config --local --unset includeif.gitdir:/github/workspace/.git/worktrees/*.path /github/runner_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0353290Z [command]/opt/homebrew/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0796790Z Removing credentials config '/Users/runner/work/_temp/git-credentials-aa2e97a9-acb8-434d-86dd-f1cfc707913c.config'
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0801620Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0912140Z ##[group]Run if [ "${OS}" == "macos-14" ]; then
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0912490Z ^[[36;1mif [ "${OS}" == "macos-14" ]; then^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0912920Z ^[[36;1m  # GitHub macOS runners can include preconfigured taps that Homebrew^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0913350Z ^[[36;1m  # warns about during install operations. Trust them explicitly so CI^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0913820Z ^[[36;1m  # logs stay warning-clean as Homebrew tightens tap trust defaults.^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0914180Z ^[[36;1m  brew trust aws/tap azure/bicep || true^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0914420Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0914660Z ^[[36;1m  # `bashcov` on macOS must use Homebrew Bash (>=5) to avoid the^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0915070Z ^[[36;1m  # system Bash 3.2 parser limitations that produced empty coverage.^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0915500Z ^[[36;1m  # `gawk` is available for shell tooling used by the test suite.^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0915930Z ^[[36;1m  # `chezmoi` is installed so Bats can render chezmoi templates^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0916350Z ^[[36;1m  # behaviorally instead of grepping template syntax.^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0916720Z ^[[36;1m  brew install bash bats-core chezmoi gawk parallel shellcheck shfmt^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0917010Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0917190Z ^[[36;1melif [ "${OS}" == "ubuntu-latest" ]; then^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0917520Z ^[[36;1m  # Ruby is required for bashcov/simplecov formatters. Install chezmoi^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0917910Z ^[[36;1m  # explicitly so template tests can verify rendered behavior.^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0918380Z ^[[36;1m  sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby shellcheck shfmt^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0918780Z ^[[36;1m  chezmoi_version=2.70.5^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0919080Z ^[[36;1m  artifact="chezmoi_${chezmoi_version}_linux_amd64.tar.gz"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0919540Z ^[[36;1m  base_url="https://github.com/twpayne/chezmoi/releases/download/v${chezmoi_version}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0919990Z ^[[36;1m  curl -fsSL "${base_url}/${artifact}" -o "${RUNNER_TEMP}/${artifact}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0920510Z ^[[36;1m  curl -fsSL "${base_url}/chezmoi_${chezmoi_version}_checksums.txt" \^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0920890Z ^[[36;1m    | grep "  ${artifact}$" \^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0921180Z ^[[36;1m    | (cd "${RUNNER_TEMP}" && sha256sum --check --strict)^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0921610Z ^[[36;1m  tar -xzf "${RUNNER_TEMP}/${artifact}" -C "${RUNNER_TEMP}" chezmoi^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0922100Z ^[[36;1m  sudo install -m 0755 "${RUNNER_TEMP}/chezmoi" /usr/local/bin/chezmoi^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0922400Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0922550Z ^[[36;1melse^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0922970Z ^[[36;1m  echo "${OS} and ${SYSTEM} are not supported" >&2^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0923220Z ^[[36;1m  exit 1^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0923380Z ^[[36;1mfi^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0923530Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0923730Z ^[[36;1mfiles_test_chezmoi="$(command -v chezmoi)"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0923990Z ^[[36;1mcase "${files_test_chezmoi}" in^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0924220Z ^[[36;1m  /*/mise/shims/*|"")^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0924580Z ^[[36;1m    echo "Files test chezmoi must resolve outside mise shims: ${files_test_chezmoi:-missing}" >&2^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0924940Z ^[[36;1m    exit 1^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0925110Z ^[[36;1m    ;;^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0925260Z ^[[36;1m  /*) ;;^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0925420Z ^[[36;1m  *)^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0925690Z ^[[36;1m    echo "Files test chezmoi must be an absolute path: ${files_test_chezmoi}" >&2^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0926060Z ^[[36;1m    exit 1^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0926220Z ^[[36;1m    ;;^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0926380Z ^[[36;1mesac^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0926560Z ^[[36;1mtest -x "${files_test_chezmoi}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0926880Z ^[[36;1mprintf 'FILES_TEST_CHEZMOI=%s\n' "${files_test_chezmoi}" >> "${GITHUB_ENV}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0927190Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0927440Z ^[[36;1m# Install coverage tooling as user gems and expose gem bin dir on PATH^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0928050Z ^[[36;1m# before installation so RubyGems can expose executables immediately.^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0928430Z ^[[36;1m# `--no-document` keeps CI faster and deterministic.^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0928780Z ^[[36;1mgem_bin_dir="$(ruby -r rubygems -e 'puts Gem.user_dir')/bin"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0929100Z ^[[36;1mecho "${gem_bin_dir}" >> "${GITHUB_PATH}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0929360Z ^[[36;1mexport PATH="${gem_bin_dir}:${PATH}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0929680Z ^[[36;1mgem install --user-install --no-document bashcov --version 3.3.0^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0930100Z ^[[36;1mgem install --user-install --no-document simplecov-cobertura --version 3.1.0^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0982970Z shell: /bin/bash -e {0}
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0983160Z env:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0983310Z   OS: macos-14
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0983470Z   SYSTEM: client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0983650Z   CODECOV_FLAGS: macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0983940Z   CODECOV_NAME: codecov-dotfiles-macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0985880Z   GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:22.0986060Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:23.7132470Z Already trusted tap: aws/tap
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:23.7141970Z Already trusted tap: azure/bicep
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.5946060Z ^[[32m==>^[[0m ^[[1mDownloading bottle manifests^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6054770Z ✔︎ Bottle Manifest bash (5.3.15)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6056120Z ✔︎ Bottle Manifest bats-core (1.14.0)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6056410Z ✔︎ Bottle Manifest chezmoi (2.72.1)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6056810Z ✔︎ Bottle Manifest gawk (5.4.1)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6057160Z ✔︎ Bottle Manifest parallel (20260722)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6057450Z ✔︎ Bottle Manifest shellcheck (0.11.0)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6057830Z ✔︎ Bottle Manifest shfmt (3.14.0)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6058120Z ^[[34m==>^[[0m ^[[1mWould install 7 formulae:^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6058600Z bash bats-core chezmoi gawk parallel shellcheck shfmt
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6490850Z ^[[34m==>^[[0m ^[[1mWould install 1 dependency for bash:^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.6491210Z ncurses
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:24.7210180Z ^[[32m==>^[[0m ^[[1mFetching downloads for: ^[[32mbash^[[39m, ^[[32mbats-core^[[39m, ^[[32mchezmoi^[[39m, ^[[32mgawk^[[39m, ^[[32mparallel^[[39m, ^[[32mshellcheck^[[39m and ^[[32mshfmt^[[39m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.3185910Z ✔︎ Bottle bats-core (1.14.0)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.4083620Z ✔︎ Bottle gawk (5.4.1)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.4185170Z ✔︎ Bottle Manifest ncurses (6.6)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.4285620Z ✔︎ Bottle parallel (20260722)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.4299020Z ✔︎ Bottle bash (5.3.15)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.4497080Z ✔︎ Bottle shfmt (3.14.0)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.4722130Z ✔︎ Bottle chezmoi (2.72.1)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.5212130Z ✔︎ Bottle shellcheck (0.11.0)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.9868770Z ✔︎ Bottle ncurses (6.6)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.9972660Z ^[[32m==>^[[0m ^[[1mInstalling bash dependency: ^[[32mncurses^[[39m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:25.9988210Z ^[[34m==>^[[0m ^[[1mPouring ncurses--6.6.arm64_sonoma.bottle.tar.gz^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.4783750Z 🍺  /opt/homebrew/Cellar/ncurses/6.6: 4,086 files, 10.3MB
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.4786250Z ^[[32m==>^[[0m ^[[1mInstalling ^[[32mbash^[[39m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.4800550Z ^[[34m==>^[[0m ^[[1mPouring bash--5.3.15.arm64_sonoma.bottle.tar.gz^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.6913210Z 🍺  /opt/homebrew/Cellar/bash/5.3.15: 172 files, 13MB
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.6925940Z ^[[34m==>^[[0m ^[[1mPouring bats-core--1.14.0.all.bottle.tar.gz^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.7150870Z 🍺  /opt/homebrew/Cellar/bats-core/1.14.0: 28 files, 180.8KB
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.7164580Z ^[[34m==>^[[0m ^[[1mPouring chezmoi--2.72.1.arm64_sonoma.bottle.tar.gz^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.8048500Z 🍺  /opt/homebrew/Cellar/chezmoi/2.72.1: 9 files, 37.6MB
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.8349740Z ^[[34m==>^[[0m ^[[1mPouring gawk--5.4.1.arm64_sonoma.bottle.tar.gz^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.9517260Z 🍺  /opt/homebrew/Cellar/gawk/5.4.1: 107 files, 7.7MB
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.9545340Z ^[[34m==>^[[0m ^[[1mPouring parallel--20260722.all.bottle.tar.gz^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:26.9926560Z 🍺  /opt/homebrew/Cellar/parallel/20260722: 94 files, 5.5MB
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.0052910Z ^[[34m==>^[[0m ^[[1mPouring shellcheck--0.11.0.arm64_sonoma.bottle.1.tar.gz^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9441900Z 🍺  /opt/homebrew/Cellar/shellcheck/0.11.0: 8 files, 70.7MB
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9543290Z ^[[34m==>^[[0m ^[[1mPouring shfmt--3.14.0.arm64_sonoma.bottle.tar.gz^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9644900Z 🍺  /opt/homebrew/Cellar/shfmt/3.14.0: 8 files, 3.5MB
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9673390Z ^[[32m==>^[[0m ^[[1mCaveats^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9675520Z Bash completion has been installed to:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9677300Z   /opt/homebrew/etc/bash_completion.d
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9677790Z ^[[34m==>^[[0m ^[[1mbash^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9678490Z DEFAULT_LOADABLE_BUILTINS_PATH: /opt/homebrew/lib/bash:/usr/local/lib/bash:/usr/lib/bash:/opt/local/lib/bash:/usr/pkg/lib/bash:/opt/pkg/lib/bash:.
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9679210Z ^[[34m==>^[[0m ^[[1mgawk^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9679830Z GNU "awk" has been installed as "gawk".
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9680330Z If you need to use it as "awk", you can add a "gnubin" directory
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9680850Z to your PATH from your ~/.bashrc and/or ~/.zshrc like:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9681190Z 
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9681470Z     PATH="/opt/homebrew/opt/gawk/libexec/gnubin:$PATH"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9681970Z ^[[34m==>^[[0m ^[[1mparallel^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9687650Z To use the --csv option, the Perl Text::CSV module has to be installed.
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9688960Z You can install it via:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:27.9689970Z   perl -MCPAN -e'install Text::CSV'
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:28.9492180Z Successfully installed simplecov_json_formatter-0.1.4
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:28.9492600Z Successfully installed simplecov-html-0.13.2
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:28.9493020Z Successfully installed docile-1.4.1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:28.9493360Z Successfully installed simplecov-0.22.0
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:28.9493740Z Successfully installed bashcov-3.3.0
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:28.9494060Z 5 gems installed
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.4950500Z Successfully installed simplecov-cobertura-3.1.0
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5046670Z 1 gem installed
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5124460Z ##[group]Run statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5125040Z ^[[36;1mstatusline_mise_dir="${RUNNER_TEMP}/statusline-mise"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5125390Z ^[[36;1mmkdir -p "${statusline_mise_dir}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5125830Z ^[[36;1mcp home/dot_mise/config.toml "${statusline_mise_dir}/mise.toml"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5126190Z ^[[36;1mcp home/dot_mise/mise.lock "${statusline_mise_dir}/mise.lock"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5149760Z shell: /opt/homebrew/bin/bash -e {0}
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5150210Z env:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5150440Z   OS: macos-14
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5150690Z   SYSTEM: client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5150880Z   CODECOV_FLAGS: macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5151250Z   CODECOV_NAME: codecov-dotfiles-macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5154520Z   GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5154880Z   FILES_TEST_CHEZMOI: /opt/homebrew/bin/chezmoi
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5155260Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5802790Z ##[group]Run jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5804220Z with:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5804380Z   version: 2026.7.5
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5804640Z   install: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5804830Z   cache: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5805000Z   bootstrap: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5805200Z   cache_save: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5805370Z   cache_key_prefix: mise-v1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5805560Z   experimental: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5805740Z   log_level: info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5805890Z   reshim: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5806270Z   add_shims_to_path: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5808280Z   github_token: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5808470Z   fetch_from_github: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5808700Z   env: true
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5808860Z   wings_enabled: false
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5809190Z env:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5809350Z   OS: macos-14
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5809520Z   SYSTEM: client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5809700Z   CODECOV_FLAGS: macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5809990Z   CODECOV_NAME: codecov-dotfiles-macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5812740Z   GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5812980Z   FILES_TEST_CHEZMOI: /opt/homebrew/bin/chezmoi
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.5813290Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:29.7535320Z ##[group]Restoring mise cache
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:30.1137020Z mise cache not found for mise-v1-macos-arm64-macos14-2026.7.5-1bbb65a7bcad82e4d599613cb9638d2ea0b5c715d71e4fc308c00b1c2543cd82
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:30.1139550Z ##[group]Download mise@2026.7.5
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:30.1153410Z [command]/opt/homebrew/bin/zstd --version
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:30.1178110Z *** Zstandard CLI (64-bit) v1.5.7, by Yann Collet ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:30.1190130Z Using curl to download mise
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.8965400Z [command]/bin/mv /var/folders/s6/5hzmn6lx4dz5nxs7k_0slzph0000gn/T/mise/bin/mise /Users/runner/.local/share/mise/bin/mise
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.8994310Z ##[group]Setting env vars
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.8994590Z Setting MISE_LOG_LEVEL=info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.8997610Z Setting MISE_GITHUB_TOKEN=***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.8998000Z Setting MISE_TRUSTED_CONFIG_PATHS=/Users/runner/work/dotfiles/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.8998480Z Setting MISE_YES=1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.8999280Z Adding /Users/runner/.local/share/mise/shims to PATH
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9001160Z ##[group]Running mise --version
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9013770Z [command]/Users/runner/.local/share/mise/bin/mise --version
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9195380Z 2026.7.5 macos-arm64 (2026-07-09)
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9269710Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9270010Z ##[group]Running mise ls
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9280170Z [command]/Users/runner/.local/share/mise/bin/mise ls
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9391540Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9392310Z ##[group]Exporting mise environment variables
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9528520Z [command]/Users/runner/.local/share/mise/bin/mise env --json
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9649340Z {
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9652180Z   "PATH": "/Users/runner/.local/share/mise/shims:/Users/runner/.local/share/mise/bin:/Users/runner/.local/share/gem/ruby/3.3.0/bin:/opt/homebrew/lib/ruby/gems/3.3.0/bin:/opt/homebrew/opt/ruby@3.3/bin:/Users/runner/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/runner/.cargo/bin:/usr/local/opt/curl/bin:/usr/local/bin:/usr/local/sbin:/Users/runner/bin:/Users/runner/.yarn/bin:/Users/runner/Library/Android/sdk/tools:/Users/runner/Library/Android/sdk/platform-tools:/Library/Frameworks/Python.framework/Versions/Current/bin:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/usr/bin:/bin:/usr/sbin:/sbin:/Users/runner/.dotnet/tools"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9654650Z }
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9659030Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9724010Z ##[group]Run mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9724440Z ^[[36;1mmise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9724790Z ^[[36;1mmise -C "${RUNNER_TEMP}/statusline-mise" install --locked \^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9725280Z ^[[36;1m  npm:ccstatusline@2.2.27 \^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9725510Z ^[[36;1m  npm:ccusage@20.0.19^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9740100Z shell: /opt/homebrew/bin/bash -e {0}
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9740310Z env:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9740450Z   OS: macos-14
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9740610Z   SYSTEM: client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9740770Z   CODECOV_FLAGS: macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9741000Z   CODECOV_NAME: codecov-dotfiles-macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9742960Z   GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9743160Z   FILES_TEST_CHEZMOI: /opt/homebrew/bin/chezmoi
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9743390Z   MISE_LOG_LEVEL: info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9745140Z   MISE_GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9745460Z   MISE_TRUSTED_CONFIG_PATHS: /Users/runner/work/dotfiles/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9745730Z   MISE_YES: 1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9747450Z   PATH: /Users/runner/.local/share/mise/shims:/Users/runner/.local/share/mise/bin:/Users/runner/.local/share/gem/ruby/3.3.0/bin:/opt/homebrew/lib/ruby/gems/3.3.0/bin:/opt/homebrew/opt/ruby@3.3/bin:/Users/runner/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/runner/.cargo/bin:/usr/local/opt/curl/bin:/usr/local/bin:/usr/local/sbin:/Users/runner/bin:/Users/runner/.yarn/bin:/Users/runner/Library/Android/sdk/tools:/Users/runner/Library/Android/sdk/platform-tools:/Library/Frameworks/Python.framework/Versions/Current/bin:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/usr/bin:/bin:/usr/sbin:/sbin:/Users/runner/.dotnet/tools
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:32.9749370Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:33.0062120Z ^[[2mmise^[[0m trusted /Users/runner/work/_temp/statusline-mise
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:33.0283590Z ^[[2mmise^[[0m ^[[34mnpm:ccusage^[[0m@20.0.19 [1/3] install
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:33.0284020Z ^[[2mmise^[[0m ^[[34mnpm:ccstatusline^[[0m@2.2.27 [1/3] install
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.0899050Z ^[[2mmise^[[0m ^[[34mnpm:ccstatusline^[[0m@2.2.27 [1/3] added 1 package in 640ms
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.1729430Z ^[[2mmise^[[0m ^[[34mnpm:ccstatusline^[[0m@2.2.27 ^[[38;5;10m✓^[[0m installed
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.7302320Z ^[[2mmise^[[0m ^[[34mnpm:ccusage^[[0m@20.0.19 [1/3] added 2 packages in 1s
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.7402940Z ^[[2mmise^[[0m ^[[34mnpm:ccusage^[[0m@20.0.19 [1/3] 1 package is looking for funding
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.7461290Z ^[[2mmise^[[0m ^[[34mnpm:ccusage^[[0m@20.0.19 [1/3]   run `npm fund` for details
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8163900Z ^[[2mmise^[[0m ^[[34mnpm:ccusage^[[0m@20.0.19 ^[[38;5;10m✓^[[0m installed
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8325900Z ##[group]Run set -euo pipefail
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8326160Z ^[[36;1mset -euo pipefail^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8326340Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8326540Z ^[[36;1mstatusline_mise_dir="${RUNNER_TEMP}/statusline-mise"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8326920Z ^[[36;1mccstatusline_bin="$(mise -C "${statusline_mise_dir}" which ccstatusline)"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8327300Z ^[[36;1mccusage_bin="$(mise -C "${statusline_mise_dir}" which ccusage)"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8327740Z ^[[36;1mccstatusline_root="$(mise -C "${statusline_mise_dir}" where npm:ccstatusline@2.2.27)"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8328200Z ^[[36;1mccusage_root="$(mise -C "${statusline_mise_dir}" where npm:ccusage@20.0.19)"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8328490Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8328640Z ^[[36;1mcase "${ccstatusline_bin}" in^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8337550Z ^[[36;1m  "${ccstatusline_root}"/*) ;;^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8337900Z ^[[36;1m  *) echo "ccstatusline did not resolve from mise's exact install" >&2; exit 1 ;;^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8338260Z ^[[36;1mesac^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8338460Z ^[[36;1mcase "${ccusage_bin}" in^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8338680Z ^[[36;1m  "${ccusage_root}"/*) ;;^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8338960Z ^[[36;1m  *) echo "ccusage did not resolve from mise's exact install" >&2; exit 1 ;;^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8339260Z ^[[36;1mesac^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8339400Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8339590Z ^[[36;1msmoke_home="${RUNNER_TEMP}/statusline-smoke-home"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8339880Z ^[[36;1mmkdir -p "${smoke_home}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8340080Z ^[[36;1msmoke=(^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8340430Z ^[[36;1m  /usr/bin/env^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8340610Z ^[[36;1m  "HOME=${smoke_home}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8340800Z ^[[36;1m  "PATH=${PATH}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8341020Z ^[[36;1m  "HTTP_PROXY=http://127.0.0.1:1"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8341250Z ^[[36;1m  "HTTPS_PROXY=http://127.0.0.1:1"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8341460Z ^[[36;1m  NO_PROXY=^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8341660Z ^[[36;1m  python3 scripts/check-statusline-tools.py^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8341920Z ^[[36;1m  --ccstatusline "${ccstatusline_bin}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8342160Z ^[[36;1m  --ccusage "${ccusage_bin}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8342340Z ^[[36;1m)^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8342470Z ^[[36;1m^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8342630Z ^[[36;1mif [ "${OS}" = "ubuntu-latest" ]; then^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8342920Z ^[[36;1m  sudo unshare --net -- sh -c 'test -z "$(ip route show)"'^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8343200Z ^[[36;1m  sudo unshare --net -- "${smoke[@]}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8343430Z ^[[36;1melif [ "${OS}" = "macos-14" ]; then^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8343720Z ^[[36;1m  sandbox_profile='(version 1)(allow default)(deny network*)'^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8344050Z ^[[36;1m  if /usr/bin/sandbox-exec -p "${sandbox_profile}" \^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8344420Z ^[[36;1m    python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0))'; then^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8344830Z ^[[36;1m    echo "macOS network-denial oracle unexpectedly bound a socket" >&2^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8345140Z ^[[36;1m    exit 1^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8345280Z ^[[36;1m  fi^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8345500Z ^[[36;1m  /usr/bin/sandbox-exec -p "${sandbox_profile}" "${smoke[@]}"^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8345770Z ^[[36;1melse^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8345930Z ^[[36;1m  echo "${OS} is not supported" >&2^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8346140Z ^[[36;1m  exit 1^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8346280Z ^[[36;1mfi^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8360050Z shell: /opt/homebrew/bin/bash -e {0}
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8360240Z env:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8360390Z   OS: macos-14
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8360520Z   SYSTEM: client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8360680Z   CODECOV_FLAGS: macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8360890Z   CODECOV_NAME: codecov-dotfiles-macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8362750Z   GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8362920Z   FILES_TEST_CHEZMOI: /opt/homebrew/bin/chezmoi
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8363130Z   MISE_LOG_LEVEL: info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8364800Z   MISE_GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8365260Z   MISE_TRUSTED_CONFIG_PATHS: /Users/runner/work/dotfiles/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8365520Z   MISE_YES: 1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8367150Z   PATH: /Users/runner/.local/share/mise/shims:/Users/runner/.local/share/mise/bin:/Users/runner/.local/share/gem/ruby/3.3.0/bin:/opt/homebrew/lib/ruby/gems/3.3.0/bin:/opt/homebrew/opt/ruby@3.3/bin:/Users/runner/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/runner/.cargo/bin:/usr/local/opt/curl/bin:/usr/local/bin:/usr/local/sbin:/Users/runner/bin:/Users/runner/.yarn/bin:/Users/runner/Library/Android/sdk/tools:/Users/runner/Library/Android/sdk/platform-tools:/Library/Frameworks/Python.framework/Versions/Current/bin:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/usr/bin:/bin:/usr/sbin:/sbin:/Users/runner/.dotnet/tools
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:34.8368850Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.0685260Z Traceback (most recent call last):
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.0685810Z   File "<string>", line 1, in <module>
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.0686240Z     import socket; s = socket.socket(); s.bind(("127.0.0.1", 0))
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.0686730Z                                         ~~~~~~^^^^^^^^^^^^^^^^^^
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.0687120Z PermissionError: [Errno 1] Operation not permitted
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7119170Z ##[group]Run git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7119700Z ^[[36;1mgit ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d^[[0m
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7133550Z shell: /opt/homebrew/bin/bash -e {0}
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7133750Z env:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7133870Z   OS: macos-14
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7134220Z   SYSTEM: client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7134370Z   CODECOV_FLAGS: macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7134600Z   CODECOV_NAME: codecov-dotfiles-macos-14-client
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7136380Z   GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7136560Z   FILES_TEST_CHEZMOI: /opt/homebrew/bin/chezmoi
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7136780Z   MISE_LOG_LEVEL: info
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7138390Z   MISE_GITHUB_TOKEN: ***
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7138630Z   MISE_TRUSTED_CONFIG_PATHS: /Users/runner/work/dotfiles/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7138890Z   MISE_YES: 1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7140520Z   PATH: /Users/runner/.local/share/mise/shims:/Users/runner/.local/share/mise/bin:/Users/runner/.local/share/gem/ruby/3.3.0/bin:/opt/homebrew/lib/ruby/gems/3.3.0/bin:/opt/homebrew/opt/ruby@3.3/bin:/Users/runner/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/runner/.cargo/bin:/usr/local/opt/curl/bin:/usr/local/bin:/usr/local/sbin:/Users/runner/bin:/Users/runner/.yarn/bin:/Users/runner/Library/Android/sdk/tools:/Users/runner/Library/Android/sdk/platform-tools:/Library/Frameworks/Python.framework/Versions/Current/bin:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/usr/bin:/bin:/usr/sbin:/sbin:/Users/runner/.dotnet/tools
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7142150Z ##[endgroup]
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7503200Z diff scripts/upgrade-tools.sh.orig scripts/upgrade-tools.sh
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7503690Z --- scripts/upgrade-tools.sh.orig
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7503930Z +++ scripts/upgrade-tools.sh
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7504270Z @@ -398,7 +398,7 @@
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7504430Z          return 1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7504580Z      }
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7504780Z  
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7504970Z -    if ! cat > "${pins}" << EOF; then
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7505210Z +    if ! cat > "${pins}" << EOF
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7505410Z  #!/usr/bin/env bash
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7505750Z  # shellcheck disable=SC2034 # Variables are consumed by the scripts that source this file.
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7506100Z  
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7506270Z @@ -417,6 +417,7 @@
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7506540Z  TERMINAL_BROWSER_PIN_VERSION="$(sed -n 1p <<< "${tb_pin}")"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7506890Z  TERMINAL_BROWSER_INSTALLER_SHA256="$(sed -n 2p <<< "${tb_pin}")"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7507160Z  EOF
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7507290Z +    then
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7507540Z          printf 'warning: unable to write %s; keeping current pins\n' "${pins}" >&2
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7507860Z          return 1
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7508180Z      fi
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7519040Z ##[error]Process completed with exit code 1.
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.7628770Z Post job cleanup.
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8344110Z [command]/opt/homebrew/bin/git version
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8382660Z git version 2.55.0
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8396860Z Copying '/Users/runner/.gitconfig' to '/Users/runner/work/_temp/1e8bcb34-4231-4dc9-8eb1-d2a9cf5d8245/.gitconfig'
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8402690Z Temporarily overriding HOME='/Users/runner/work/_temp/1e8bcb34-4231-4dc9-8eb1-d2a9cf5d8245' before making global git config changes
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8403690Z Adding repository directory to the temporary git global config as a safe directory
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8406030Z [command]/opt/homebrew/bin/git config --global --add safe.directory /Users/runner/work/dotfiles/dotfiles
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8446970Z Removing SSH command configuration
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8451670Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp core\.sshCommand
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8493740Z [command]/opt/homebrew/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8985330Z Removing HTTP extra header
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.8989470Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.9026280Z [command]/opt/homebrew/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.9481960Z Removing includeIf entries pointing to credentials config files
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.9485410Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:35.9520770Z [command]/opt/homebrew/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
test (macos-14, client)	UNKNOWN STEP	2026-09-13T01:33:36.0567330Z Cleaning up orphan processes
```

## 4. Command

```sh
command -v nix
```

Exit: 1

```text
```

## 5. Command

```sh
gh api repos/mryfmo/dotfiles/actions/runs/34730808923/jobs --jq '.jobs[] | {name,conclusion,steps:[.steps[]|select(.conclusion=="failure")|{name,number,conclusion}]}'
```

Exit: 0

```text
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"changes"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"failure"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (macos-14, client)"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"failure"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run `shfmt`"[m[1;38m,[m
[1;34m"number"[m[1;38m:[m 10
[1;38m}[m
[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"cancelled"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (ubuntu-latest, client)"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"cancelled"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (ubuntu-latest, server)"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"nix"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m[1;38m][m
[1;38m}[m
```

## 6. Command

```sh
gh api 'repos/astral-sh/setup-uv/releases?per_page=100' --jq '.[] | select(.tag_name|test("^v(8|9|10)\\.")) | {tag_name,html_url,body}'
```

Exit: 0

```text
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nThis release contains the known-checksum of the most recent uv releases and also disabled the uploading(saving) of the cache when in a merge queue since theses caches would almost never be used.\r\n\r\n## 🚀 Enhancements\r\n\r\n- Disable automatic cache saves for merge queues @eifinger (#1056)\r\n\r\n## 🧰 Maintenance\r\n\r\n- chore: update known checksums for 0.12.17 @[github-actions[bot]](https://github.com/apps/github-actions) (#1058)\r\n- chore: update known checksums for 0.12.16 @[github-actions[bot]](https://github.com/apps/github-actions) (#1057)\r\n- chore: update known checksums for 0.12.15 @[github-actions[bot]](https://github.com/apps/github-actions) (#1054)\r\n- chore: update known checksums for 0.12.14 @[github-actions[bot]](https://github.com/apps/github-actions) (#1053)\r\n- chore: update known checksums for 0.12.13 @[github-actions[bot]](https://github.com/apps/github-actions) (#1045)\r\n\r\n## 📚 Documentation\r\n\r\n- docs: update version references to v10.1.0 @[github-actions[bot]](https://github.com/apps/github-actions) (#1044)\r\n\r\n## ⬆️ Dependency updates\r\n\r\n- chore(deps): roll up Dependabot updates @eifinger (#1059)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v10.2.0"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v10.2.0"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nThis release adds more bheind the scene security improvements and also 2 small improvements.\r\n\r\n### NO_PROXY\r\n\r\nThis action now respects `no_proxy/NO_PROXY` environment variables which were previously ignored.\r\n\r\n### New output `python-runtime-id`\r\n\r\nThe new output `python-runtime-id` can be used to know which python version exactly was installed if you use `activate-environment`. See https://github.com/pyca/cryptography/pull/15572#discussion_r3913508686 for details on why this can be useful.\r\n\r\n## 🐛 Bug fixes\r\n\r\n- fix: respect no proxy directive @mj0nez (#1037)\r\n- Use JSON + a typed wrapper instead of TS codegen @woodruffw (#1025)\r\n\r\n## 🚀 Enhancements\r\n\r\n- Expose a Python \"identity\" output @woodruffw (#1036)\r\n- Verify downloads with astral-sh/versions checksums @zaniebot (#1033)\r\n\r\n## 🧰 Maintenance\r\n\r\n- chore: update known checksums for 0.12.12 @[github-actions[bot]](https://github.com/apps/github-actions) (#1041)\r\n- chore: update known checksums for 0.12.10/0.12.11 @[github-actions[bot]](https://github.com/apps/github-actions) (#1038)\r\n- chore: update known checksums for 0.12.9 @[github-actions[bot]](https://github.com/apps/github-actions) (#1035)\r\n- chore: update known checksums for 0.12.7/0.12.8 @[github-actions[bot]](https://github.com/apps/github-actions) (#1031)\r\n- chore: update known checksums for 0.12.6 @[github-actions[bot]](https://github.com/apps/github-actions) (#1030)\r\n- chore: update known checksums for 0.12.5 @[github-actions[bot]](https://github.com/apps/github-actions) (#1020)\r\n- Use self-repo syntax for all in-repo actions/reusable workflows @woodruffw (#1024)\r\n- Pin one-shot tools @woodruffw (#1022)\r\n- ci: remove obsolete direct push attempts @eifinger (#1019)\r\n\r\n## 📚 Documentation\r\n\r\n- docs: update version references to v10.0.1 @[github-actions[bot]](https://github.com/apps/github-actions) (#1018)\r\n\r\n## ⬆️ Dependency updates\r\n\r\n- chore(deps-dev): roll up Dependabot updates @eifinger (#1043)\r\n- Harden npm install defaults @zaniebot (#1026)\r\n- Add dependency cooldowns @woodruffw (#1021)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v10.1.0"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v10.1.0"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nThank you @arguile- for making this action more resilient.\r\n\r\n## 🐛 Bug fixes\r\n\r\n- Tolerate transient manifest timeouts @arguile- (#1016)\r\n\r\n## 🧰 Maintenance\r\n\r\n- chore: update known checksums for 0.12.4 @[github-actions[bot]](https://github.com/apps/github-actions) (#1017)\r\n\r\n## 📚 Documentation\r\n\r\n- docs: update version references to v10.0.0 @[github-actions[bot]](https://github.com/apps/github-actions) (#1014)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v10.0.1"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v10.0.1"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nAnother breaking release, directly after v9.0.0 but we think the added security justifies that.\r\n\r\n### Extra security by default\r\n\r\nIf you use the default `enable-cache: auto` this will now **DISABLE THE CACHE** to protect against cache poisoning for the following events:\r\n\r\n- `pull_request_target`\r\n- `workflow_run`\r\n- `release`\r\n\r\nYou can read the full reasoning in https://github.com/astral-sh/setup-uv/issues/984\r\n\r\n### `version: latest-known`\r\n\r\n```yaml\r\n- name: Install the latest version of uv known to setup-uv\r\n  uses: astral-sh/setup-uv@v10.0.0\r\n  with:\r\n    version: \"latest-known\"\r\n```\r\n\r\nThis will now install the latest version with a checksum that is known by this action. The [known `uv` checksums](https://github.com/astral-sh/setup-uv/blob/4f6036f71cec78afb113b323f220c9185d983c12/src/download/checksum/known-checksums.ts) are automatically updated but will take a release of this action to take effect. You won't be always using the latest & greatest but you will have an extra level of security.\r\n\r\n### Read python version from `.tool-versions`\r\n\r\n```yaml\r\n- name: Install uv based on the version defined in .tool-versions and also set python\r\n  uses: astral-sh/setup-uv@v10.0.0\r\n  with:\r\n    version-file: \"pyproject.toml\"\r\n```\r\n\r\nWill now also set the python version if it is defined in `.tool-versions`. You can read the details [in the docs](https://github.com/astral-sh/setup-uv/blob/main/docs/advanced-version-configuration.md#install-a-version-defined-in-a-requirements-or-config-file)\r\n\r\n## 🚨 Breaking changes\r\n\r\n- Disable automatic caching for sensitive events @eifinger (#992)\r\n\r\n## 🐛 Bug fixes\r\n\r\n- Reject paths in .tool-versions @eifinger (#1007)\r\n\r\n## 🚀 Enhancements\r\n\r\n- Read Python version from .tool-versions @eifinger (#996)\r\n- Add latest-known version selector @eifinger (#993)\r\n\r\n## 🧰 Maintenance\r\n\r\n- Require pull requests for Dependabot rollups @eifinger (#1005)\r\n- ci: pin Alpine container image @eifinger (#995)\r\n- chore: update known checksums for 0.12.3 @[github-actions[bot]](https://github.com/apps/github-actions) (#991)\r\n- chore: update known checksums for 0.12.2 @[github-actions[bot]](https://github.com/apps/github-actions) (#985)\r\n- chore: update known checksums for 0.12.1 @[github-actions[bot]](https://github.com/apps/github-actions) (#982)\r\n- chore: update known checksums for 0.12.0 @[github-actions[bot]](https://github.com/apps/github-actions) (#981)\r\n- chore: update known checksums for 0.11.31/0.11.32 @[github-actions[bot]](https://github.com/apps/github-actions) (#972)\r\n\r\n## 📚 Documentation\r\n\r\n- docs: update version references to v9.0.0 @[github-actions[bot]](https://github.com/apps/github-actions) (#971)\r\n\r\n## ⬆️ Dependency updates\r\n\r\n- chore(deps): roll up Dependabot updates @eifinger (#1013)\r\n- chore(deps): roll up Dependabot updates @eifinger (#1004)\r\n- chore(deps): roll up Dependabot updates @eifinger (#994)\r\n- chore(deps): bump zizmorcore/zizmor-action from 0.5.7 to 0.6.0 @[dependabot[bot]](https://github.com/apps/dependabot) (#976)\r\n- chore(deps): bump actions/checkout from 7.0.0 to 7.0.1 @[dependabot[bot]](https://github.com/apps/dependabot) (#980)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v10.0.0"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v10.0.0"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nThis release disables the default cache cache pruning to ease the load on the PyPi infrastructure.\r\nSince users might experience more GitHub Actions cache usage which might result in higher costs this is marked as a breaking change. To read more on why we did this (now) you can read the detailed analysis and reasoning in #967\r\n\r\nBesides this big breaking change we also have a small bugfix while building caches for linux distributions that behave a big different than the \"big ones\" and a speed up in version resolution by only reading the version manifest until a matching version is found saving runtime and network bandwith.\r\n\r\n## 🚨 Breaking changes\r\n\r\n- Change `prune-cache` default to `false` @charliermarsh (#967)\r\n\r\n## 🐛 Bug fixes\r\n\r\n- fix: fall back to distribution ID when os-release has no version field @cxzhong (#961)\r\n\r\n## 🚀 Enhancements\r\n\r\n- Speed up version client by partial response reads @eifinger (#807)\r\n\r\n## 🧰 Maintenance\r\n\r\n- chore: update known checksums for 0.11.30 @[github-actions[bot]](https://github.com/apps/github-actions) (#968)\r\n- chore: update known checksums for 0.11.29 @[github-actions[bot]](https://github.com/apps/github-actions) (#960)\r\n\r\n## 📚 Documentation\r\n\r\n- docs: update version references to v8.3.2 @[github-actions[bot]](https://github.com/apps/github-actions) (#949)\r\n\r\n## ⬆️ Dependency updates\r\n\r\n- chore(deps): roll up Dependabot updates @eifinger (#970)\r\n- chore(deps): roll up Dependabot updates @eifinger (#962)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v9.0.0"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v9.0.0"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nJust a maintenance release\r\n\r\n## 🧰 Maintenance\r\n\r\n- chore: update known checksums for 0.11.28 @[github-actions[bot]](https://github.com/apps/github-actions) (#947)\r\n\r\n## 📚 Documentation\r\n\r\n- docs: update version references to v8.3.1 @[github-actions[bot]](https://github.com/apps/github-actions) (#946)\r\n\r\n## ⬆️ Dependency updates\r\n\r\n- chore: roll up Dependabot updates @eifinger (#948)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v8.3.2"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v8.3.2"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nJust a maintenance release\r\n\r\n## 🧰 Maintenance\r\n\r\n- Change update-docs PR labels from 'update-docs' to 'documentation' @eifinger (#945)\r\n- chore: update known checksums for 0.11.27 @[github-actions[bot]](https://github.com/apps/github-actions) (#944)\r\n\r\n## 📚 Documentation\r\n\r\n- docs: update version references to v8.3.0 @[github-actions[bot]](https://github.com/apps/github-actions) (#939)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v8.3.1"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v8.3.1"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nThanks to @somaz94 you can now use the pinned version of uv itself in `uv.lock`. It gets picked up automatically.\r\nIf you have pinned another version of uv in your `uv.lock` you can use the inputs `version` or `version-source` to override this.\r\n\r\n## 🐛 Bug fixes\r\n\r\n- Strip environment markers from detected uv dependency pins @eifinger (#938)\r\n- Fix cache keys for Python version ranges @eifinger (#937)\r\n- fix: use BUILD\\_ID as backup for determining os version @hgaiser (#912)\r\n\r\n## 🚀 Enhancements\r\n\r\n- feat: support uv.lock as a version-file source @somaz94 (#918)\r\n\r\n## 🧰 Maintenance\r\n\r\n- ci: call docs update workflow from release @eifinger (#933)\r\n- chore: update known checksums for 0.11.26 @[github-actions[bot]](https://github.com/apps/github-actions) (#930)\r\n- chore: update known checksums for 0.11.25 @[github-actions[bot]](https://github.com/apps/github-actions) (#929)\r\n- chore: update known checksums for 0.11.24 @[github-actions[bot]](https://github.com/apps/github-actions) (#925)\r\n- chore: update known checksums for 0.11.23 @[github-actions[bot]](https://github.com/apps/github-actions) (#922)\r\n- chore: update known checksums for 0.11.22 @[github-actions[bot]](https://github.com/apps/github-actions) (#921)\r\n- chore: update known checksums for 0.11.21 @[github-actions[bot]](https://github.com/apps/github-actions) (#917)\r\n- chore: update known checksums for 0.11.20 @[github-actions[bot]](https://github.com/apps/github-actions) (#915)\r\n- chore: update known checksums for 0.11.19 @[github-actions[bot]](https://github.com/apps/github-actions) (#909)\r\n\r\n## 📚 Documentation\r\n\r\n- docs: update version references to v8.2.0 @KRRT7 (#932)\r\n- Add a threat model for setup-uv @zsol (#923)\r\n\r\n## ⬆️ Dependency updates\r\n\r\n- chore(deps): roll up Dependabot updates @eifinger (#936)\r\n- chore(deps): bump release-drafter/release-drafter from 7.3.1 to 7.4.0 @[dependabot[bot]](https://github.com/apps/dependabot) (#924)\r\n- chore(deps): bump actions/checkout from 6.0.2 to 7.0.0 @[dependabot[bot]](https://github.com/apps/dependabot) (#926)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v8.3.0"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v8.3.0"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nThis release brings two new inputs and a few bug fixes.\r\n\r\n### New inputs\r\n\r\nLets talk about the new inputs first.\r\n\r\n#### quiet\r\n\r\nPretty simple. It turns of all `info` loggings. Useful if you use this in a composite action and are not interested in all the details.\r\nIn the upcoming releases we will add log groups to fully implement support for \"less noise\"\r\n\r\n> [!NOTE]  \r\n> Warnings and errors are always logged.\r\n\r\n#### download-from-astral-mirror\r\n\r\nIn some cases you may want to directly use the fallback of checking for available versions and downloading releases from GitHub instead of using the astral.sh mirror. Setting `download-from-astral-mirror: false` allows you to do that.\r\n\r\n### Bugfixes\r\n\r\nWhen using the astral.sh mirror to query available versions and download releases (done by default) we now stop sending the GitHub token in the header. The mirror never looked at it but we shouldn't be handing out that data even if it is just a short lived token.\r\nAll other bugfixes try to limit the impact of failed GitHub queries due to retries and other faults.\r\n\r\nWe couldn't pinpoint all rootcauses yet but added more logging for error cases to track them down.\r\n\r\n## 🐛 Bug fixes\r\n\r\n- fix: report unexpected cache save failures @eifinger (#896)\r\n- fix: report unexpected setup failures @eifinger (#895)\r\n- fix: add timeout to fetch to prevent silent hangs @eifinger-bot (#883)\r\n- Limit GitHub tokens to github.com download URLs @zsol (#878)\r\n- increase libuv-workaround timeout to 100ms @eifinger (#880)\r\n\r\n## 🚀 Enhancements\r\n\r\n- Add quiet input to suppress info-level log output @eifinger (#898)\r\n- feat: add `download-from-astral-mirror` input @eifinger (#897)\r\n\r\n## 🧰 Maintenance\r\n\r\n- docs: update dependabot rollup biome guidance @eifinger (#902)\r\n- chore: update known checksums for 0.11.18 @[github-actions[bot]](https://github.com/apps/github-actions) (#899)\r\n- chore: update known checksums for 0.11.17 @[github-actions[bot]](https://github.com/apps/github-actions) (#892)\r\n- chore: update known checksums for 0.11.16 @[github-actions[bot]](https://github.com/apps/github-actions) (#889)\r\n- chore: update known checksums for 0.11.15 @[github-actions[bot]](https://github.com/apps/github-actions) (#885)\r\n- chore: update known checksums for 0.11.14 @[github-actions[bot]](https://github.com/apps/github-actions) (#879)\r\n- chore: update known checksums for 0.11.13 @[github-actions[bot]](https://github.com/apps/github-actions) (#877)\r\n- chore: update known checksums for 0.11.12 @[github-actions[bot]](https://github.com/apps/github-actions) (#876)\r\n- chore: update known checksums for 0.11.11 @[github-actions[bot]](https://github.com/apps/github-actions) (#873)\r\n- chore: update known checksums for 0.11.9/0.11.10 @[github-actions[bot]](https://github.com/apps/github-actions) (#871)\r\n- chore: update known checksums for 0.11.8 @[github-actions[bot]](https://github.com/apps/github-actions) (#867)\r\n- Bump setup-uv references to v8.1.0 SHA in docs @eifinger (#862)\r\n- Add update-docs.yml workflow @eifinger (#861)\r\n\r\n## ⬆️ Dependency updates\r\n\r\n- chore(deps): roll up dependabot updates @eifinger (#903)\r\n- chore(deps): roll up dependabot updates @eifinger (#901)\r\n- chore(deps): bump release-drafter/release-drafter from 7.3.0 to 7.3.1 @[dependabot[bot]](https://github.com/apps/dependabot) (#900)\r\n- chore(deps): bump eifinger/actionlint-action from 1.10.1 to 1.10.2 @[dependabot[bot]](https://github.com/apps/dependabot) (#842)\r\n- chore(deps): bump github/codeql-action from 4.35.4 to 4.36.0 @[dependabot[bot]](https://github.com/apps/dependabot) (#893)\r\n- chore(deps): bump zizmorcore/zizmor-action from 0.5.5 to 0.5.6 @[dependabot[bot]](https://github.com/apps/dependabot) (#891)\r\n- chore(deps): bump release-drafter/release-drafter from 7.2.0 to 7.3.0 @[dependabot[bot]](https://github.com/apps/dependabot) (#884)\r\n- chore(deps): bump zizmorcore/zizmor-action from 0.5.3 to 0.5.5 @[dependabot[bot]](https://github.com/apps/dependabot) (#888)\r\n- chore(deps): bump github/codeql-action from 4.35.3 to 4.35.4 @[dependabot[bot]](https://github.com/apps/dependabot) (#881)\r\n- chore(deps): bump github/codeql-action from 4.32.2 to 4.35.3 @[dependabot[bot]](https://github.com/apps/dependabot) (#875)\r\n- chore(deps): bump actions/setup-node from 6.3.0 to 6.4.0 @[dependabot[bot]](https://github.com/apps/dependabot) (#866)\r\n- chore(deps): bump zizmorcore/zizmor-action from 0.5.2 to 0.5.3 @[dependabot[bot]](https://github.com/apps/dependabot) (#864)\r\n- chore(deps): bump peter-evans/create-pull-request from 8.1.0 to 8.1.1 @[dependabot[bot]](https://github.com/apps/dependabot) (#863)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v8.2.0"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v8.2.0"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## Changes\r\n\r\nThis add the a new boolean input `no-project`.\r\nIt only makes sense to use in combination with `activate-environment: true` and will append `--no project` to the `uv venv` call. This is for example useful [if you have a pyproject.toml file with parts unparseable by uv](https://github.com/astral-sh/setup-uv/issues/854)\r\n\r\n## 🚀 Enhancements\r\n\r\n- Add input no-project in combination with activate-environment @eifinger (#856)\r\n\r\n## 🧰 Maintenance\r\n\r\n- fix: grant contents:write to validate-release job @eifinger (#860)\r\n- Add a release-gate step to the release workflow @zanieb (#859)\r\n- Draft commitish releases @eifinger (#858)\r\n- Add action-types.yml to instructions @eifinger (#857)\r\n- chore: update known checksums for 0.11.7 @[github-actions[bot]](https://github.com/apps/github-actions) (#853)\r\n- Refactor version resolving @eifinger (#852)\r\n- chore: update known checksums for 0.11.6 @[github-actions[bot]](https://github.com/apps/github-actions) (#850)\r\n- chore: update known checksums for 0.11.5 @[github-actions[bot]](https://github.com/apps/github-actions) (#845)\r\n- chore: update known checksums for 0.11.4 @[github-actions[bot]](https://github.com/apps/github-actions) (#843)\r\n- Add a release workflow @zanieb (#839)\r\n- chore: update known checksums for 0.11.3 @[github-actions[bot]](https://github.com/apps/github-actions) (#836)\r\n\r\n## 📚 Documentation\r\n\r\n- Update ignore-nothing-to-cache documentation @eifinger (#833)\r\n- Pin setup-uv docs to v8 @eifinger (#829)\r\n\r\n## ⬆️ Dependency updates\r\n\r\n- chore(deps): bump release-drafter/release-drafter from 7.1.1 to 7.2.0 @[dependabot[bot]](https://github.com/apps/dependabot) (#855)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v8.1.0"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v8.1.0"[m
[1;38m}[m
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"# This is the first immutable release of `setup-uv` 🥳 \r\nAll future releases are also immutable, if you want to know more about what this means checkout [the docs](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).\r\n\r\nThis release also has two breaking changes\r\n\r\n## New format for `manifest-file`\r\n\r\nThe previously deprecated way of defining a custom version manifest to control which `uv` versions are available and where to download them from got removed. The functionality is still there but you have to use the [new format](https://github.com/astral-sh/setup-uv/blob/main/docs/customization.md#format).\r\n\r\n## No more major and minor tags\r\n\r\nTo increase **security** even more we will **stop publishing minor tags**. You won't be able to use `@v8` or `@v8.0` any longer. We do this because pinning to major releases opens up users to supply chain attacks like what happened to [tj-actions](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/).\r\n\r\n> [!TIP]\r\n> Use the immutable tag as a version `astral-sh/setup-uv@v8.0.0`\r\n> Or even better the githash `astral-sh/setup-uv@cec208311dfd045dd5311c1add060b2062131d57`\r\n\r\n## 🚨 Breaking changes\r\n\r\n- Remove update-major-minor-tags workflow @eifinger (#826)\r\n- Remove deprecrated custom manifest @eifinger (#813)\r\n\r\n## 🧰 Maintenance\r\n\r\n- Shortcircuit latest version from manifest @eifinger (#828)\r\n- Simplify inputs.ts @eifinger (#827)\r\n- Bump release-drafter to v7.1.1 @eifinger (#825)\r\n- Refactor inputs @eifinger (#823)\r\n- Replace inline compile args with tsconfig @eifinger (#824)\r\n- chore: update known checksums for 0.11.2 @[github-actions[bot]](https://github.com/apps/github-actions) (#821)\r\n- chore: update known checksums for 0.11.1 @[github-actions[bot]](https://github.com/apps/github-actions) (#817)\r\n- chore: update known checksums for 0.11.0 @[github-actions[bot]](https://github.com/apps/github-actions) (#815)\r\n- Fix latest-version workflow check @eifinger (#812)\r\n- chore: update known checksums for 0.10.11/0.10.12 @[github-actions[bot]](https://github.com/apps/github-actions) (#811)\r\n"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/astral-sh/setup-uv/releases/tag/v8.0.0"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v8.0.0"[m
[1;38m}[m
```

## 7. Command

```sh
gh api repos/cachix/install-nix-action/releases/tags/v31.11.1 --jq '{tag_name,html_url,body}'
```

Exit: 0

```text
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## What's Changed\r\n* nix: 2.35.1 -> 2.35.2 by @github-actions[bot] in https://github.com/cachix/install-nix-action/pull/281\r\n  Fixes a crash ([`Assertion '!awake.empty()' failed`](https://github.com/NixOS/nix/issues/16005)) that could abort builds.\r\n\r\n\r\n**Full Changelog**: https://github.com/cachix/install-nix-action/compare/v31.11.0...v31.11.1"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/cachix/install-nix-action/releases/tag/v31.11.1"[m[1;38m,[m
[1;34m"tag_name"[m[1;38m:[m [32m"v31.11.1"[m
[1;38m}[m
```

## 8. Command

```sh
gh api repos/cachix/install-nix-action/compare/v31.10.7...v31.11.1 --jq '{html_url,commits:[.commits[]|{sha,message:.commit.message}],files:[.files[]|{filename,status,patch}]}'
```

Exit: 0

```text
[1;38m{[m
[1;34m"commits"[m[1;38m:[m [1;38m[[m
[1;38m{[m
[1;34m"message"[m[1;38m:[m [32m"nix: 2.34.8 -> 2.35.1"[m[1;38m,[m
[1;34m"sha"[m[1;38m:[m [32m"0247906e3a81152580edf10a53a0f6c191922535"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"message"[m[1;38m:[m [32m"Merge pull request #279 from cachix/create-pull-request/patch\n\nnix: 2.34.8 -> 2.35.1"[m[1;38m,[m
[1;34m"sha"[m[1;38m:[m [32m"630ae543ea3a38a9a4166f03376c02c50f408342"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"message"[m[1;38m:[m [32m"nix: 2.35.1 -> 2.35.2"[m[1;38m,[m
[1;34m"sha"[m[1;38m:[m [32m"6624a11f6c07674a3ff71d2431865aecf3587190"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"message"[m[1;38m:[m [32m"Merge pull request #281 from cachix/create-pull-request/patch\n\nnix: 2.35.1 -> 2.35.2"[m[1;38m,[m
[1;34m"sha"[m[1;38m:[m [32m"875018fe555aee647c21ea81888659240cd8e27b"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"message"[m[1;38m:[m [32m"fix(ci): skip latest installer on x86_64-darwin\n\nNix master no longer ships a binary for the platform."[m[1;38m,[m
[1;34m"sha"[m[1;38m:[m [32m"13d8dd58da0234aa297dedd986986ccb8e7f3e24"[m
[1;38m}[m
[1;38m][m[1;38m,[m
[1;34m"files"[m[1;38m:[m [1;38m[[m
[1;38m{[m
[1;34m"filename"[m[1;38m:[m [32m".github/workflows/test-per-system.yml"[m[1;38m,[m
[1;34m"patch"[m[1;38m:[m [32m"@@ -70,6 +70,8 @@ jobs:\n     - run: nix flake show github:NixOS/nixpkgs\n \n   latest-installer:\n+    # Nix master no longer provides binary tarballs for x86_64-darwin\n+    if: inputs.system != 'x86_64-darwin'\n     runs-on: ${{ inputs.runs-on }}\n     steps:\n     - uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7.0.0"[m[1;38m,[m
[1;34m"status"[m[1;38m:[m [32m"modified"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"filename"[m[1;38m:[m [32m"install-nix.sh"[m[1;38m,[m
[1;34m"patch"[m[1;38m:[m [32m"@@ -102,7 +102,7 @@ echo \"installer options: ${installer_options[*]}\"\n \n # There is --retry-on-errors, but only newer curl versions support that\n curl_retries=5\n-nix_version=2.34.8\n+nix_version=2.35.2\n while ! curl -sS -o \"$workdir/install\" -v --fail -L \"${INPUT_INSTALL_URL:-https://releases.nixos.org/nix/nix-${nix_version}/install}\"; do\n   sleep 1\n   ((curl_retries--))"[m[1;38m,[m
[1;34m"status"[m[1;38m:[m [32m"modified"[m
[1;38m}[m
[1;38m][m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/cachix/install-nix-action/compare/v31.10.7...v31.11.1"[m
[1;38m}[m
```

## 9. Command

```sh
git log --oneline 5ac784a..origin/main -- .github/workflows/test.yaml scripts/; rg -n -A10 -B3 'setup-uv|UV_PYTHON_INSTALL_DIR|nix eval|nix flake|install-nix-action' .github/workflows/*
```

Exit: 0

```text
5b4fd8b fix(validate): skip nested git worktrees in the repo-wide scans (#176)
efc2bb2 chore(deps): bump codecov/codecov-action from 7.0.0 to 7.1.1 (#159)
c11035f fix(update): tolerate a herdr protocol mismatch on reload; align docs and dev image (#174)
cd61a88 fix(mise): stop make upgrade and mise from writing into the main checkout (#172)
d377ad0 chore(mise): upgrade tool pins via make upgrade (#171)
455455e fix(compactiondb): store a machine-independent hook interpreter
4d4767b feat(agent-config): drive the herdr-agents worker kind from the manifest
212baf3 feat(setup): provision a per-machine ssh key for signing and push
d26fe77 feat(chezmoi): gate the private layer behind an init-time flag
1735147 feat(ubuntu): install zed on client from pinned release
2e032e1 fix(doctor): tolerate cowork-synced skills and own crit codex skills
61b7a37 fix(agents): key codex project trust to the chezmoi working tree
788ba3b fix(agents): close bot-review residuals and guard private bashrc sources (#169)
5aaaafb chore(mise): upgrade tool pins via make upgrade (#168)
.github/workflows/test.yaml-263-
.github/workflows/test.yaml-264-      - name: Setup uv
.github/workflows/test.yaml-265-        if: ${{ needs.changes.outputs.should_test == 'true' }}
.github/workflows/test.yaml:266:        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
.github/workflows/test.yaml-267-        with:
.github/workflows/test.yaml-268-          enable-cache: false
.github/workflows/test.yaml-269-
.github/workflows/test.yaml-270-      - name: Run Python unit tests
.github/workflows/test.yaml-271-        if: ${{ needs.changes.outputs.should_test == 'true' }}
.github/workflows/test.yaml-272-        run: |
.github/workflows/test.yaml-273-          if [ "${OS}" == "ubuntu-latest" ]; then
.github/workflows/test.yaml-274-            sudo apt-get update && sudo apt-get install -y jq zsh
.github/workflows/test.yaml-275-          elif [ "${OS}" == "macos-14" ]; then
.github/workflows/test.yaml-276-            command -v jq > /dev/null 2>&1 || brew install jq
--
.github/workflows/test.yaml-386-          persist-credentials: false
.github/workflows/test.yaml-387-
.github/workflows/test.yaml-388-      - name: Install Nix
.github/workflows/test.yaml:389:        uses: cachix/install-nix-action@a49548c11d9846ad46ecc0115273879b045f001c # v31
.github/workflows/test.yaml-390-
.github/workflows/test.yaml-391-      - name: Evaluate flake outputs
.github/workflows/test.yaml-392-        run: |
.github/workflows/test.yaml:393:          nix flake check --no-build --no-update-lock-file
.github/workflows/test.yaml:394:          nix eval --no-update-lock-file .#homeConfigurations.mryfmo-linux.activationPackage.drvPath
.github/workflows/test.yaml:395:          nix eval --no-update-lock-file .#homeConfigurations.mryfmo-darwin.activationPackage.drvPath
.github/workflows/test.yaml:396:          nix eval --no-update-lock-file .#darwinConfigurations.mryfmo-mac.system.drvPath
--
.github/workflows/docs.yml-37-          fetch-depth: 0
.github/workflows/docs.yml-38-
.github/workflows/docs.yml-39-      - name: Setup uv
.github/workflows/docs.yml:40:        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
.github/workflows/docs.yml-41-        with:
.github/workflows/docs.yml-42-          enable-cache: false
.github/workflows/docs.yml-43-
.github/workflows/docs.yml-44-      - name: Setup mise
.github/workflows/docs.yml-45-        uses: jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d # v4
.github/workflows/docs.yml-46-        with:
.github/workflows/docs.yml-47-          install: false
.github/workflows/docs.yml-48-          cache: true
.github/workflows/docs.yml-49-
.github/workflows/docs.yml-50-      - name: Trust mise config
--
.github/workflows/agent-assets.yml-27-          persist-credentials: false
.github/workflows/agent-assets.yml-28-
.github/workflows/agent-assets.yml-29-      - name: Setup uv
.github/workflows/agent-assets.yml:30:        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
.github/workflows/agent-assets.yml-31-        with:
.github/workflows/agent-assets.yml-32-          enable-cache: false
.github/workflows/agent-assets.yml-33-
.github/workflows/agent-assets.yml-34-      - name: Validate agent assets
.github/workflows/agent-assets.yml-35-        run: uv run --with pyyaml scripts/validate-agent-assets.py
.github/workflows/agent-assets.yml-36-
.github/workflows/agent-assets.yml-37-      - name: Check upstream documentation links
.github/workflows/agent-assets.yml-38-        if: ${{ github.event_name == 'schedule' || github.event_name == 'workflow_dispatch' }}
.github/workflows/agent-assets.yml-39-        run: |
.github/workflows/agent-assets.yml-40-          set -euo pipefail
```

## 10. Command

```sh
git log --oneline -S 'shfmt@3.14.1' -- .github/workflows/test.yaml
```

Exit: 0

```text
bf2110f chore(scripts): reformat heredoc-in-if for shfmt 3.14 (#158)
```

## 11. Command

```sh
gh api repos/mryfmo/dotfiles/actions/runs/34730808923 --jq '{head_sha,conclusion,html_url}'
```

Exit: 0

```text
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"failure"[m[1;38m,[m
[1;34m"head_sha"[m[1;38m:[m [32m"1b1b976459e80e7025ba0f7ac535b36c356d1a33"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/mryfmo/dotfiles/actions/runs/34730808923"[m
[1;38m}[m
```

## 12. Command

```sh
gh api repos/mryfmo/dotfiles/actions/runs/34730808923/jobs --jq '.jobs[] | {name,conclusion,steps:[.steps[]|{name,conclusion}]}'
```

Exit: 0

```text
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"changes"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Set up job"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Configure Git defaults"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Checkout repository"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Detect unit-test-relevant changes"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Post Checkout repository"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Complete job"[m
[1;38m}[m
[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"failure"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (macos-14, client)"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Set up job"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Configure Git defaults"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Checkout repository"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Skip full unit test run for unrelated changes"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Install tools"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Prepare exact statusline tool config"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup mise for statusline smoke"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Install exact statusline tools"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Smoke-test statusline tools without network"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"failure"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run `shfmt`"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run `ShellCheck`"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup uv"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run Python unit tests"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Prepare public dotfiles fixture"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run unit test"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup for Codecov"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Upload coverage to Codecov"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Post Checkout repository"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Complete job"[m
[1;38m}[m
[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"cancelled"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (ubuntu-latest, client)"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Set up job"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Configure Git defaults"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Checkout repository"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Skip full unit test run for unrelated changes"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Install tools"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Prepare exact statusline tool config"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup mise for statusline smoke"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Install exact statusline tools"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Smoke-test statusline tools without network"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run `shfmt`"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run `ShellCheck`"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup uv"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"cancelled"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run Python unit tests"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Prepare public dotfiles fixture"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run unit test"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup for Codecov"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Upload coverage to Codecov"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Post Setup uv"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Post Checkout repository"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Complete job"[m
[1;38m}[m
[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"cancelled"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (ubuntu-latest, server)"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Set up job"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Configure Git defaults"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Checkout repository"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Skip full unit test run for unrelated changes"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Install tools"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Prepare exact statusline tool config"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup mise for statusline smoke"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"cancelled"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Install exact statusline tools"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Smoke-test statusline tools without network"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run `shfmt`"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run `ShellCheck`"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup uv"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run Python unit tests"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Prepare public dotfiles fixture"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Run unit test"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Setup for Codecov"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Upload coverage to Codecov"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Post Checkout repository"[m
[1;38m}[m[1;38m,[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"Complete job"[m
[1;38m}[m
[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"nix"[m[1;38m,[m
[1;34m"steps"[m[1;38m:[m [1;38m[[m[1;38m][m
[1;38m}[m
```

## 13. Command

```sh
gh pr diff 155 --repo mryfmo/dotfiles
```

Exit: 0

```text
[1;37mdiff --git a/.github/workflows/agent-assets.yml b/.github/workflows/agent-assets.yml[m
[1;37mindex 645e6443..0288a573 100644[m
[1;37m--- a/.github/workflows/agent-assets.yml[m
[1;37m+++ b/.github/workflows/agent-assets.yml[m
@@ -27,7 +27,7 @@ jobs:
           persist-credentials: false
 
       - name: Setup uv
[31m-        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7[m
[32m+        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0[m
         with:
           enable-cache: false
 
[1;37mdiff --git a/.github/workflows/docs.yml b/.github/workflows/docs.yml[m
[1;37mindex faba1e0a..07a5524c 100644[m
[1;37m--- a/.github/workflows/docs.yml[m
[1;37m+++ b/.github/workflows/docs.yml[m
@@ -37,7 +37,7 @@ jobs:
           fetch-depth: 0
 
       - name: Setup uv
[31m-        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7[m
[32m+        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0[m
         with:
           enable-cache: false
 
[1;37mdiff --git a/.github/workflows/test.yaml b/.github/workflows/test.yaml[m
[1;37mindex 1dc72eef..969b74eb 100644[m
[1;37m--- a/.github/workflows/test.yaml[m
[1;37m+++ b/.github/workflows/test.yaml[m
@@ -263,7 +263,7 @@ jobs:
 
       - name: Setup uv
         if: ${{ needs.changes.outputs.should_test == 'true' }}
[31m-        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7[m
[32m+        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0[m
         with:
           enable-cache: false
 
```

## 14. Command

```sh
gh pr diff 125 --repo mryfmo/dotfiles
```

Exit: 0

```text
[1;37mdiff --git a/.github/workflows/test.yaml b/.github/workflows/test.yaml[m
[1;37mindex 1dc72eef..27a230d1 100644[m
[1;37m--- a/.github/workflows/test.yaml[m
[1;37m+++ b/.github/workflows/test.yaml[m
@@ -386,7 +386,7 @@ jobs:
           persist-credentials: false
 
       - name: Install Nix
[31m-        uses: cachix/install-nix-action@a49548c11d9846ad46ecc0115273879b045f001c # v31[m
[32m+        uses: cachix/install-nix-action@13d8dd58da0234aa297dedd986986ccb8e7f3e24 # v31[m
 
       - name: Evaluate flake outputs
         run: |
```

## 15. Command

```sh
gh pr checks 155 --repo mryfmo/dotfiles
```

Exit: 0

```text
CodeRabbit	pass	0		Review skipped: bot user not eligible for review
changes	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36092281398/job/107937032566	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36092281333/job/107937032491	
private-bootstrap (ubuntu-latest, client)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/36092281333/job/107937032516	
private-bootstrap (ubuntu-latest, server)	pass	3s	https://github.com/mryfmo/dotfiles/actions/runs/36092281333/job/107937032541	
public-bootstrap (macos-14, client)	pass	8m57s	https://github.com/mryfmo/dotfiles/actions/runs/36092281333/job/107937032589	
public-bootstrap (ubuntu-latest, client)	pass	8m24s	https://github.com/mryfmo/dotfiles/actions/runs/36092281333/job/107937032509	
public-bootstrap (ubuntu-latest, server)	pass	7m0s	https://github.com/mryfmo/dotfiles/actions/runs/36092281333/job/107937032358	
test (macos-14, client)	pass	1m46s	https://github.com/mryfmo/dotfiles/actions/runs/36092281398/job/107937057179	
test (ubuntu-latest, client)	pass	4m23s	https://github.com/mryfmo/dotfiles/actions/runs/36092281398/job/107937057133	
validate	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/36092281404/job/107937032592	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36092281398/job/107937058223	
test (ubuntu-latest, server)	pass	1m50s	https://github.com/mryfmo/dotfiles/actions/runs/36092281398/job/107937057111	
```

## 16. Command

```sh
gh pr checks 125 --repo mryfmo/dotfiles
```

Exit: 0

```text
CodeRabbit	pass	0		Review skipped: bot user not eligible for review
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36092266976/job/107936990136	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36092266948/job/107936990087	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36092266948/job/107936990358	
private-bootstrap (ubuntu-latest, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36092266948/job/107936990333	
public-bootstrap (macos-14, client)	pass	11m15s	https://github.com/mryfmo/dotfiles/actions/runs/36092266948/job/107936990346	
public-bootstrap (ubuntu-latest, client)	pass	8m1s	https://github.com/mryfmo/dotfiles/actions/runs/36092266948/job/107936990264	
public-bootstrap (ubuntu-latest, server)	pass	5m36s	https://github.com/mryfmo/dotfiles/actions/runs/36092266948/job/107936990350	
test (macos-14, client)	pass	1m40s	https://github.com/mryfmo/dotfiles/actions/runs/36092266976/job/107937018320	
test (ubuntu-latest, client)	pass	4m44s	https://github.com/mryfmo/dotfiles/actions/runs/36092266976/job/107937018344	
test (ubuntu-latest, server)	pass	2m1s	https://github.com/mryfmo/dotfiles/actions/runs/36092266976/job/107937018348	
validate	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/36092266916/job/107936990089	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36092266976/job/107937019451	
```

## 17. Command

```sh
gh api repos/cachix/install-nix-action/releases/tags/v31.11.0 --jq '{html_url,body}'
```

Exit: 0

```text
[1;38m{[m
[1;34m"body"[m[1;38m:[m [32m"## What's Changed\r\n* nix: 2.34.8 -> 2.35.1 by @github-actions[bot] in https://github.com/cachix/install-nix-action/pull/279\r\n   Release notes: https://discourse.nixos.org/t/nix-2-35-0-released/78914\r\n\r\n\r\n**Full Changelog**: https://github.com/cachix/install-nix-action/compare/v31.10.7...v31.11.0"[m[1;38m,[m
[1;34m"html_url"[m[1;38m:[m [32m"https://github.com/cachix/install-nix-action/releases/tag/v31.11.0"[m
[1;38m}[m
```

## 18. Command

```sh
git status --short
```

Exit: 0

```text
?? .orchestration/tasks/dot-dependabot-verify-T8-a01.md
```

## 19. Command

```sh
git show bf2110f -- .github/workflows/test.yaml scripts/upgrade-tools.sh
```

Exit: 0

```text
commit bf2110fd85debadd0a906361ed510c7fe2db6b0b
Author: mryfmo <mryfmo@gmail.com>
Date:   Sat Sep 19 22:02:35 2026 +0900

    chore(scripts): reformat heredoc-in-if for shfmt 3.14 (#158)
    
    * chore(scripts): reformat heredoc-in-if for shfmt 3.14
    
    shfmt 3.14 (now on CI runners and local mise) formats
    'cat > file << EOF; then' as a separate 'then' line after the heredoc.
    Mechanical 'shfmt -i 4 -sr -w' output only; no behavior change.
    Unblocks CI for open PRs (main's Unit test job fails on re-run with
    the newer shfmt without this).
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
    
    * ci(test): pin shfmt to 3.14.1 via mise
    
    brew (macos) and apt (ubuntu) ship divergent shfmt versions that
    disagree on heredoc-in-if formatting, so the same tree cannot satisfy
    both runners. Run the format check through 'mise x shfmt@3.14.1' and
    drop shfmt from the package-manager installs.
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
    
    ---------
    
    Co-authored-by: Claude Fable 5 <noreply@anthropic.com>

diff --git a/.github/workflows/test.yaml b/.github/workflows/test.yaml
index 1a91d79..9dabc82 100644
--- a/.github/workflows/test.yaml
+++ b/.github/workflows/test.yaml
@@ -129,12 +129,12 @@ jobs:
             # `gawk` is available for shell tooling used by the test suite.
             # `chezmoi` is installed so Bats can render chezmoi templates
             # behaviorally instead of grepping template syntax.
-            brew install bash bats-core chezmoi gawk parallel shellcheck shfmt
+            brew install bash bats-core chezmoi gawk parallel shellcheck
 
           elif [ "${OS}" == "ubuntu-latest" ]; then
             # Ruby is required for bashcov/simplecov formatters. Install chezmoi
             # explicitly so template tests can verify rendered behavior.
-            sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby shellcheck shfmt
+            sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby shellcheck
             chezmoi_version=2.70.5
             artifact="chezmoi_${chezmoi_version}_linux_amd64.tar.gz"
             base_url="https://github.com/twpayne/chezmoi/releases/download/v${chezmoi_version}"
@@ -251,7 +251,9 @@ jobs:
       - name: Run `shfmt`
         if: ${{ needs.changes.outputs.should_test == 'true' }}
         run: |
-          git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d
+          # shfmt is version-pinned via mise: brew/apt ship divergent versions
+          # (3.14 changed heredoc-in-if formatting) and unpinned runners disagree.
+          git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d
 
       - name: Run `ShellCheck`
         if: ${{ needs.changes.outputs.should_test == 'true' }}
diff --git a/scripts/upgrade-tools.sh b/scripts/upgrade-tools.sh
index 4ab990d..d161cf3 100755
--- a/scripts/upgrade-tools.sh
+++ b/scripts/upgrade-tools.sh
@@ -398,7 +398,7 @@ function bump_terminal_tool_pins() {
         return 1
     }
 
-    if ! cat > "${pins}" << EOF; then
+    if ! cat > "${pins}" << EOF
 #!/usr/bin/env bash
 # shellcheck disable=SC2034 # Variables are consumed by the scripts that source this file.
 
@@ -417,6 +417,7 @@ TERMINAL_CODE_INSTALLER_SHA256="$(sed -n 2p <<< "${tode_pin}")"
 TERMINAL_BROWSER_PIN_VERSION="$(sed -n 1p <<< "${tb_pin}")"
 TERMINAL_BROWSER_INSTALLER_SHA256="$(sed -n 2p <<< "${tb_pin}")"
 EOF
+    then
         printf 'warning: unable to write %s; keeping current pins\n' "${pins}" >&2
         return 1
     fi
```

## 20. Command

```sh
git show 5ac784a:.github/workflows/test.yaml | sed -n '130,230p'
```

Exit: 0

```text
            # `chezmoi` is installed so Bats can render chezmoi templates
            # behaviorally instead of grepping template syntax.
            brew install bash bats-core chezmoi gawk parallel shellcheck

          elif [ "${OS}" == "ubuntu-latest" ]; then
            # Ruby is required for bashcov/simplecov formatters. Install chezmoi
            # explicitly so template tests can verify rendered behavior.
            sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby shellcheck
            chezmoi_version=2.70.5
            artifact="chezmoi_${chezmoi_version}_linux_amd64.tar.gz"
            base_url="https://github.com/twpayne/chezmoi/releases/download/v${chezmoi_version}"
            curl -fsSL "${base_url}/${artifact}" -o "${RUNNER_TEMP}/${artifact}"
            curl -fsSL "${base_url}/chezmoi_${chezmoi_version}_checksums.txt" \
              | grep "  ${artifact}$" \
              | (cd "${RUNNER_TEMP}" && sha256sum --check --strict)
            tar -xzf "${RUNNER_TEMP}/${artifact}" -C "${RUNNER_TEMP}" chezmoi
            sudo install -m 0755 "${RUNNER_TEMP}/chezmoi" /usr/local/bin/chezmoi

          else
            echo "${OS} and ${SYSTEM} are not supported" >&2
            exit 1
          fi

          files_test_chezmoi="$(command -v chezmoi)"
          case "${files_test_chezmoi}" in
            /*/mise/shims/*|"")
              echo "Files test chezmoi must resolve outside mise shims: ${files_test_chezmoi:-missing}" >&2
              exit 1
              ;;
            /*) ;;
            *)
              echo "Files test chezmoi must be an absolute path: ${files_test_chezmoi}" >&2
              exit 1
              ;;
          esac
          test -x "${files_test_chezmoi}"
          printf 'FILES_TEST_CHEZMOI=%s\n' "${files_test_chezmoi}" >> "${GITHUB_ENV}"

          # Install coverage tooling as user gems and expose gem bin dir on PATH
          # before installation so RubyGems can expose executables immediately.
          # `--no-document` keeps CI faster and deterministic.
          gem_bin_dir="$(ruby -r rubygems -e 'puts Gem.user_dir')/bin"
          echo "${gem_bin_dir}" >> "${GITHUB_PATH}"
          export PATH="${gem_bin_dir}:${PATH}"
          gem install --user-install --no-document bashcov --version 3.3.0
          gem install --user-install --no-document simplecov-cobertura --version 3.1.0

      - name: Prepare exact statusline tool config
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
          mkdir -p "${statusline_mise_dir}"
          cp home/dot_mise/config.toml "${statusline_mise_dir}/mise.toml"
          cp home/dot_mise/mise.lock "${statusline_mise_dir}/mise.lock"

      - name: Setup mise for statusline smoke
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        uses: jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d # v4
        with:
          version: 2026.7.5
          install: false
          cache: true

      - name: Install exact statusline tools
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"
          mise -C "${RUNNER_TEMP}/statusline-mise" install --locked \
            npm:ccstatusline@2.2.27 \
            npm:ccusage@20.0.19

      - name: Smoke-test statusline tools without network
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          set -euo pipefail

          statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
          ccstatusline_bin="$(mise -C "${statusline_mise_dir}" which ccstatusline)"
          ccusage_bin="$(mise -C "${statusline_mise_dir}" which ccusage)"
          ccstatusline_root="$(mise -C "${statusline_mise_dir}" where npm:ccstatusline@2.2.27)"
          ccusage_root="$(mise -C "${statusline_mise_dir}" where npm:ccusage@20.0.19)"

          case "${ccstatusline_bin}" in
            "${ccstatusline_root}"/*) ;;
            *) echo "ccstatusline did not resolve from mise's exact install" >&2; exit 1 ;;
          esac
          case "${ccusage_bin}" in
            "${ccusage_root}"/*) ;;
            *) echo "ccusage did not resolve from mise's exact install" >&2; exit 1 ;;
          esac

          smoke_home="${RUNNER_TEMP}/statusline-smoke-home"
          mkdir -p "${smoke_home}"
          smoke=(
            /usr/bin/env
            "HOME=${smoke_home}"
            "PATH=${PATH}"
            "HTTP_PROXY=http://127.0.0.1:1"
            "HTTPS_PROXY=http://127.0.0.1:1"
            NO_PROXY=
            python3 scripts/check-statusline-tools.py
```

## 21. Command

```sh
sed -n '145,235p' .github/workflows/test.yaml
```

Exit: 0

```text
            tar -xzf "${RUNNER_TEMP}/${artifact}" -C "${RUNNER_TEMP}" chezmoi
            sudo install -m 0755 "${RUNNER_TEMP}/chezmoi" /usr/local/bin/chezmoi

          else
            echo "${OS} and ${SYSTEM} are not supported" >&2
            exit 1
          fi

          files_test_chezmoi="$(command -v chezmoi)"
          case "${files_test_chezmoi}" in
            /*/mise/shims/*|"")
              echo "Files test chezmoi must resolve outside mise shims: ${files_test_chezmoi:-missing}" >&2
              exit 1
              ;;
            /*) ;;
            *)
              echo "Files test chezmoi must be an absolute path: ${files_test_chezmoi}" >&2
              exit 1
              ;;
          esac
          test -x "${files_test_chezmoi}"
          printf 'FILES_TEST_CHEZMOI=%s\n' "${files_test_chezmoi}" >> "${GITHUB_ENV}"

          # Install coverage tooling as user gems and expose gem bin dir on PATH
          # before installation so RubyGems can expose executables immediately.
          # `--no-document` keeps CI faster and deterministic.
          gem_bin_dir="$(ruby -r rubygems -e 'puts Gem.user_dir')/bin"
          echo "${gem_bin_dir}" >> "${GITHUB_PATH}"
          export PATH="${gem_bin_dir}:${PATH}"
          gem install --user-install --no-document bashcov --version 3.3.0
          gem install --user-install --no-document simplecov-cobertura --version 3.1.0

      - name: Prepare exact statusline tool config
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
          mkdir -p "${statusline_mise_dir}"
          cp home/dot_mise/config.toml "${statusline_mise_dir}/mise.toml"
          cp home/dot_mise/mise.lock "${statusline_mise_dir}/mise.lock"

      - name: Setup mise for statusline smoke
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        uses: jdx/mise-action@e6a8b3978addb5a52f2b4cd9d91eafa7f0ab959d # v4
        with:
          version: 2026.9.12
          install: false
          cache: true

      - name: Install exact statusline tools
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"
          mise -C "${RUNNER_TEMP}/statusline-mise" install --locked node
          mise -C "${RUNNER_TEMP}/statusline-mise" install --locked \
            npm:ccstatusline@2.2.30 \
            npm:ccusage@20.0.22

      - name: Smoke-test statusline tools without network
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          set -euo pipefail

          statusline_mise_dir="${RUNNER_TEMP}/statusline-mise"
          ccstatusline_bin="$(mise -C "${statusline_mise_dir}" which ccstatusline)"
          ccusage_bin="$(mise -C "${statusline_mise_dir}" which ccusage)"
          ccstatusline_root="$(mise -C "${statusline_mise_dir}" where npm:ccstatusline@2.2.30)"
          ccusage_root="$(mise -C "${statusline_mise_dir}" where npm:ccusage@20.0.22)"

          case "${ccstatusline_bin}" in
            "${ccstatusline_root}"/*) ;;
            *) echo "ccstatusline did not resolve from mise's exact install" >&2; exit 1 ;;
          esac
          case "${ccusage_bin}" in
            "${ccusage_root}"/*) ;;
            *) echo "ccusage did not resolve from mise's exact install" >&2; exit 1 ;;
          esac

          smoke_home="${RUNNER_TEMP}/statusline-smoke-home"
          mkdir -p "${smoke_home}"
          smoke=(
            /usr/bin/env
            "HOME=${smoke_home}"
            "PATH=${PATH}"
            "HTTP_PROXY=http://127.0.0.1:1"
            "HTTPS_PROXY=http://127.0.0.1:1"
            NO_PROXY=
            python3 scripts/check-statusline-tools.py
            --ccstatusline "${ccstatusline_bin}"
            --ccusage "${ccusage_bin}"
          )

```

## 22. Command

```sh
sed -n '365,405p' .github/workflows/test.yaml
```

Exit: 0

```text
          name: ${{ env.CODECOV_NAME }}
          # Avoid language auto-discovery warnings for gcov/coverage.py in this
          # shell-only workflow; upload the explicit Cobertura report only.
          plugins: noop
          # Use the PyPI-distributed CLI in CI to avoid non-actionable GPG trust
          # warnings emitted by the standalone binary signature verifier.
          use_pypi: true
          verbose: false

  nix:
    needs: changes
    if: ${{ needs.changes.outputs.should_nix == 'true' }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-14]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7
        with:
          persist-credentials: false

      - name: Install Nix
        uses: cachix/install-nix-action@a49548c11d9846ad46ecc0115273879b045f001c # v31

      - name: Evaluate flake outputs
        run: |
          nix flake check --no-build --no-update-lock-file
          nix eval --no-update-lock-file .#homeConfigurations.mryfmo-linux.activationPackage.drvPath
          nix eval --no-update-lock-file .#homeConfigurations.mryfmo-darwin.activationPackage.drvPath
          nix eval --no-update-lock-file .#darwinConfigurations.mryfmo-mac.system.drvPath
```

## 23. Command

```sh
gh api repos/astral-sh/setup-uv/'contents/action.yml?ref=v7.6.0' -H 'Accept: application/vnd.github.raw+json'
```

Exit: 1

```text
invalid character 'a' in literal null (expecting 'u')
```

## 24. Command

```sh
gh api repos/astral-sh/setup-uv/'contents/action.yml?ref=v10.2.0' -H 'Accept: application/vnd.github.raw+json'
```

Exit: 1

```text
invalid character 'a' in literal null (expecting 'u')
```

## 25. Command

```sh
git ls-files .python-version .tool-versions uv.lock pyproject.toml
```

Exit: 0

```text
```

## 26. Command

```sh
gh api 'repos/astral-sh/setup-uv/contents/action.yml?ref=v7.6.0' --jq .content | base64 --decode
```

Exit: 0

```text
name: "astral-sh/setup-uv"
description:
  "Set up your GitHub Actions workflow with a specific version of uv."
author: "astral-sh"
inputs:
  version:
    description: "The version of uv to install e.g., `0.5.0` Defaults to the version in pyproject.toml or 'latest'."
    default: ""
  version-file:
    description: "Path to a file containing the version of uv to install. Defaults to searching for uv.toml and if not found pyproject.toml."
    default: ""
  python-version:
    description: "The version of Python to set UV_PYTHON to"
    required: false
  activate-environment:
    description: "Use uv venv to activate a venv ready to be used by later steps. "
    default: "false"
  venv-path:
    description: "Custom path for the virtual environment when using activate-environment. Defaults to '.venv' in the working directory."
    default: ""
  working-directory:
    description: "The directory to execute all commands in and look for files such as pyproject.toml"
    default: ${{ github.workspace }}
  checksum:
    description: "The checksum of the uv version to install"
    required: false
  github-token:
    description:
      "Used when downloading uv from GitHub releases."
    required: false
    default: ${{ github.token }}
  enable-cache:
    description: "Enable uploading of the uv cache"
    default: "auto"
  cache-dependency-glob:
    description:
      "Glob pattern to match files relative to the working directory to control
      the cache."
    default: |
      **/*requirements*.txt
      **/*requirements*.in
      **/*constraints*.txt
      **/*constraints*.in
      **/pyproject.toml
      **/uv.lock
      **/*.py.lock
  restore-cache:
    description: "Whether to restore the cache if found."
    default: "true"
  save-cache:
    description: "Whether to save the cache after the run."
    default: "true"
  cache-suffix:
    description: "Suffix for the cache key"
    required: false
  cache-local-path:
    description: "Local path to store the cache."
    default: ""
  prune-cache:
    description: "Prune cache before saving."
    default: "true"
  cache-python:
    description: "Upload managed Python installations to the Github Actions cache."
    default: "false"
  ignore-nothing-to-cache:
    description: "Ignore when nothing is found to cache."
    default: "false"
  ignore-empty-workdir:
    description: "Ignore when the working directory is empty."
    default: "false"
  tool-dir:
    description: "Custom path to set UV_TOOL_DIR to."
    required: false
  tool-bin-dir:
    description: "Custom path to set UV_TOOL_BIN_DIR to."
    required: false
  manifest-file:
    description: "URL to a custom manifest file. Supports the astral-sh/versions NDJSON format and the legacy JSON array format (deprecated)."
    required: false
  add-problem-matchers:
    description: "Add problem matchers."
    default: "true"
  resolution-strategy:
    description: "Resolution strategy to use when resolving version ranges. 'highest' uses the latest compatible version, 'lowest' uses the oldest compatible version."
    default: "highest"
outputs:
  uv-version:
    description: "The installed uv version. Useful when using latest."
  uv-path:
    description: "The path to the installed uv binary."
  uvx-path:
    description: "The path to the installed uvx binary."
  cache-hit:
    description: "A boolean value to indicate a cache entry was found"
  cache-key:
    description: "The cache key used for storing/restoring the cache"
  venv:
    description: "Path to the activated venv if activate-environment is true"
  python-version:
    description: "The Python version that was set."
  python-cache-hit:
    description: "A boolean value to indicate the Python cache entry was found"
runs:
  using: "node24"
  main: "dist/setup/index.cjs"
  post: "dist/save-cache/index.cjs"
  post-if: success()
branding:
  icon: "package"
  color: "black"
```

## 27. Command

```sh
gh api 'repos/astral-sh/setup-uv/contents/action.yml?ref=v10.2.0' --jq .content | base64 --decode
```

Exit: 0

```text
name: "astral-sh/setup-uv"
description:
  "Set up your GitHub Actions workflow with a specific version of uv."
author: "astral-sh"
inputs:
  version:
    description: "The version of uv to install, e.g., `0.5.0`, `latest`, or `latest-known`. Defaults to the version in pyproject.toml or `latest`."
    default: ""
  version-file:
    description: "Path to a file containing the version of uv to install, e.g., uv.toml, pyproject.toml, .tool-versions, requirements.txt or uv.lock. A selected .tool-versions file can also provide the Python version. Defaults to searching for uv.toml and if not found pyproject.toml."
    default: ""
  python-version:
    description: "The version of Python to set UV_PYTHON to. Overrides the Python version from .tool-versions."
    required: false
  activate-environment:
    description: "Use uv venv to activate a venv ready to be used by later steps. "
    default: "false"
  venv-path:
    description: "Custom path for the virtual environment when using activate-environment. Defaults to '.venv' in the working directory."
    default: ""
  no-project:
    description: "Pass --no-project when creating the venv with activate-environment."
    default: "false"
  working-directory:
    description: "The directory to execute all commands in and look for files such as pyproject.toml"
    default: ${{ github.workspace }}
  checksum:
    description: "The checksum of the uv version to install"
    required: false
  github-token:
    description:
      "Used when downloading uv from GitHub releases."
    required: false
    default: ${{ github.token }}
  enable-cache:
    description: "Enable the GitHub Actions cache for uv. 'auto' enables caching on GitHub-hosted runners except for release, tag push, pull_request_target, and workflow_run events."
    default: "auto"
  cache-dependency-glob:
    description:
      "Glob pattern to match files relative to the working directory to control
      the cache."
    default: |
      **/*requirements*.txt
      **/*requirements*.in
      **/*constraints*.txt
      **/*constraints*.in
      **/pyproject.toml
      **/uv.lock
      **/*.py.lock
  restore-cache:
    description: "Whether to restore the cache if found."
    default: "true"
  save-cache:
    description: "Whether to save the cache after the run. 'auto' disables saving for merge_group events."
    default: "auto"
  cache-suffix:
    description: "Suffix for the cache key"
    required: false
  cache-local-path:
    description: "Local path to store the cache."
    default: ""
  prune-cache:
    description: "Prune cache before saving."
    default: "false"
  cache-python:
    description: "Upload managed Python installations to the Github Actions cache."
    default: "false"
  ignore-nothing-to-cache:
    description: "Ignore when nothing is found to cache."
    default: "false"
  ignore-empty-workdir:
    description: "Ignore when the working directory is empty."
    default: "false"
  tool-dir:
    description: "Custom path to set UV_TOOL_DIR to."
    required: false
  tool-bin-dir:
    description: "Custom path to set UV_TOOL_BIN_DIR to."
    required: false
  manifest-file:
    description: "URL to a custom manifest file in the astral-sh/versions format."
    required: false
  download-from-astral-mirror:
    description: "Download uv from the Astral mirror instead of directly from GitHub Releases."
    default: "true"
  add-problem-matchers:
    description: "Add problem matchers."
    default: "true"
  quiet:
    description: "Suppress info-level log output. Only warnings and errors are shown."
    default: "false"
  resolution-strategy:
    description: "Resolution strategy to use when resolving version ranges. 'highest' uses the latest compatible version, 'lowest' uses the oldest compatible version."
    default: "highest"
outputs:
  uv-version:
    description: "The installed uv version. Useful when using latest."
  uv-path:
    description: "The path to the installed uv binary."
  uvx-path:
    description: "The path to the installed uvx binary."
  cache-hit:
    description: "A boolean value to indicate a cache entry was found"
  cache-key:
    description: "The cache key used for storing/restoring the cache"
  venv:
    description: "Path to the activated venv if activate-environment is true"
  python-version:
    description: "The Python version that was set."
  python-runtime-id:
    description: "An opaque identifier reported by uv for the activated venv's Python runtime. Empty when activate-environment is false."
  python-cache-hit:
    description: "A boolean value to indicate the Python cache entry was found"
runs:
  using: "node24"
  main: "dist/setup/index.cjs"
  post: "dist/save-cache/index.cjs"
  post-if: success()
branding:
  icon: "package"
  color: "black"
```

## 28. Command

```sh
git show 1b1b976459e80e7025ba0f7ac535b36c356d1a33:.github/workflows/test.yaml | sed -n '235,280p'
```

Exit: 0

```text
          if [ "${OS}" = "ubuntu-latest" ]; then
            sudo unshare --net -- sh -c 'test -z "$(ip route show)"'
            sudo unshare --net -- "${smoke[@]}"
          elif [ "${OS}" = "macos-14" ]; then
            sandbox_profile='(version 1)(allow default)(deny network*)'
            if /usr/bin/sandbox-exec -p "${sandbox_profile}" \
              python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0))'; then
              echo "macOS network-denial oracle unexpectedly bound a socket" >&2
              exit 1
            fi
            /usr/bin/sandbox-exec -p "${sandbox_profile}" "${smoke[@]}"
          else
            echo "${OS} is not supported" >&2
            exit 1
          fi

      - name: Run `shfmt`
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d

      - name: Run `ShellCheck`
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x

      - name: Setup uv
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        uses: astral-sh/setup-uv@bec219d24cd3e171d82865faccec33120bb574f4 # v10.1.0
        with:
          enable-cache: false

      - name: Run Python unit tests
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          if [ "${OS}" == "ubuntu-latest" ]; then
            sudo apt-get update && sudo apt-get install -y jq zsh
          elif [ "${OS}" == "macos-14" ]; then
            command -v jq > /dev/null 2>&1 || brew install jq
            command -v zsh > /dev/null 2>&1 || brew install zsh
          fi

          make unit-test

      - name: Prepare public dotfiles fixture
        if: ${{ needs.changes.outputs.should_test == 'true' }}
```

## 29. Command

```sh
git show origin/main:.github/workflows/test.yaml | sed -n '235,285p'
```

Exit: 0

```text

          if [ "${OS}" = "ubuntu-latest" ]; then
            sudo unshare --net -- sh -c 'test -z "$(ip route show)"'
            sudo unshare --net -- "${smoke[@]}"
          elif [ "${OS}" = "macos-14" ]; then
            sandbox_profile='(version 1)(allow default)(deny network*)'
            if /usr/bin/sandbox-exec -p "${sandbox_profile}" \
              python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0))'; then
              echo "macOS network-denial oracle unexpectedly bound a socket" >&2
              exit 1
            fi
            /usr/bin/sandbox-exec -p "${sandbox_profile}" "${smoke[@]}"
          else
            echo "${OS} is not supported" >&2
            exit 1
          fi

      - name: Run `shfmt`
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          # shfmt is version-pinned via mise: brew/apt ship divergent versions
          # (3.14 changed heredoc-in-if formatting) and unpinned runners disagree.
          git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d

      - name: Run `ShellCheck`
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x

      - name: Setup uv
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
        with:
          enable-cache: false

      - name: Run Python unit tests
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          if [ "${OS}" == "ubuntu-latest" ]; then
            sudo apt-get update && sudo apt-get install -y jq zsh
          elif [ "${OS}" == "macos-14" ]; then
            command -v jq > /dev/null 2>&1 || brew install jq
            command -v zsh > /dev/null 2>&1 || brew install zsh
          fi

          make unit-test

      - name: Prepare public dotfiles fixture
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          set -euo pipefail
```

## 30. Command

```sh
git merge-base --is-ancestor bf2110f 5ac784a
```

Exit: 0

```text
```

## 31. Command

```sh
gh api repos/mryfmo/dotfiles/actions/runs/36092281398/jobs --jq '.jobs[]|{name,conclusion,uv:[.steps[]|select(.name=="Setup uv")|.conclusion]}'
```

Exit: 0

```text
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"changes"[m[1;38m,[m
[1;34m"uv"[m[1;38m:[m [1;38m[[m[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (ubuntu-latest, server)"[m[1;38m,[m
[1;34m"uv"[m[1;38m:[m [1;38m[[m
[32m"success"[m
[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (ubuntu-latest, client)"[m[1;38m,[m
[1;34m"uv"[m[1;38m:[m [1;38m[[m
[32m"success"[m
[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"success"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"test (macos-14, client)"[m[1;38m,[m
[1;34m"uv"[m[1;38m:[m [1;38m[[m
[32m"success"[m
[1;38m][m
[1;38m}[m
[1;38m{[m
[1;34m"conclusion"[m[1;38m:[m [32m"skipped"[m[1;38m,[m
[1;34m"name"[m[1;38m:[m [32m"nix"[m[1;38m,[m
[1;34m"uv"[m[1;38m:[m [1;38m[[m[1;38m][m
[1;38m}[m
```

## 32. Command

```sh
gh api 'repos/astral-sh/setup-uv/git/trees/v10.2.0?recursive=1' --jq '.tree[].path | select(startswith("src/") and (test("input|python|cache")))'
```

Exit: 0

```text
src/cache
src/cache/restore-cache.ts
src/save-cache.ts
src/utils/inputs.ts
src/utils/python-runtime.ts
```

## 33. Command

```sh
git ls-files uv.toml
```

Exit: 0

```text
```

## 34. Command

```sh
git log -1 --format='%H %s' origin/main
```

Exit: 0

```text
d6cfed2bd65e498a180e0dbd6bca430cd032e40c chore(orchestration): sync T6 adh-baseline and T7 validator-worktrees records
```

## 35. Command

```sh
git show 5ac784a:.github/workflows/test.yaml | sed -n '235,267p'
```

Exit: 0

```text
          if [ "${OS}" = "ubuntu-latest" ]; then
            sudo unshare --net -- sh -c 'test -z "$(ip route show)"'
            sudo unshare --net -- "${smoke[@]}"
          elif [ "${OS}" = "macos-14" ]; then
            sandbox_profile='(version 1)(allow default)(deny network*)'
            if /usr/bin/sandbox-exec -p "${sandbox_profile}" \
              python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0))'; then
              echo "macOS network-denial oracle unexpectedly bound a socket" >&2
              exit 1
            fi
            /usr/bin/sandbox-exec -p "${sandbox_profile}" "${smoke[@]}"
          else
            echo "${OS} is not supported" >&2
            exit 1
          fi

      - name: Run `shfmt`
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          # shfmt is version-pinned via mise: brew/apt ship divergent versions
          # (3.14 changed heredoc-in-if formatting) and unpinned runners disagree.
          git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d

      - name: Run `ShellCheck`
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        run: |
          git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x

      - name: Setup uv
        if: ${{ needs.changes.outputs.should_test == 'true' }}
        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
        with:
          enable-cache: false
```

## 36. Command

```sh
date -Iseconds
```

Exit: 0

```text
2026-09-25T13:34:18+09:00
```

## 37. Command

```sh
gh api 'repos/astral-sh/setup-uv/contents/src/utils/inputs.ts?ref=v7.6.0' --jq .content | base64 --decode
```

Exit: 0

```text
import path from "node:path";
import * as core from "@actions/core";
import { getConfigValueFromTomlFile } from "./config-file";

export enum CacheLocalSource {
  Input,
  Config,
  Env,
  Default,
}

export const workingDirectory = core.getInput("working-directory");
export const version = core.getInput("version");
export const versionFile = getVersionFile();
export const pythonVersion = core.getInput("python-version");
export const activateEnvironment = core.getBooleanInput("activate-environment");
export const venvPath = getVenvPath();
export const checkSum = core.getInput("checksum");
export const enableCache = getEnableCache();
export const restoreCache = core.getInput("restore-cache") === "true";
export const saveCache = core.getInput("save-cache") === "true";
export const cacheSuffix = core.getInput("cache-suffix") || "";
export const cacheLocalPath = getCacheLocalPath();
export const cacheDependencyGlob = getCacheDependencyGlob();
export const pruneCache = core.getInput("prune-cache") === "true";
export const cachePython = core.getInput("cache-python") === "true";
export const ignoreNothingToCache =
  core.getInput("ignore-nothing-to-cache") === "true";
export const ignoreEmptyWorkdir =
  core.getInput("ignore-empty-workdir") === "true";
export const toolBinDir = getToolBinDir();
export const toolDir = getToolDir();
export const pythonDir = getUvPythonDir();
export const githubToken = core.getInput("github-token");
export const manifestFile = getManifestFile();
export const addProblemMatchers =
  core.getInput("add-problem-matchers") === "true";
export const resolutionStrategy = getResolutionStrategy();

function getVersionFile(): string {
  const versionFileInput = core.getInput("version-file");
  if (versionFileInput !== "") {
    const tildeExpanded = expandTilde(versionFileInput);
    return resolveRelativePath(tildeExpanded);
  }
  return versionFileInput;
}

function getVenvPath(): string {
  const venvPathInput = core.getInput("venv-path");
  if (venvPathInput !== "") {
    if (!activateEnvironment) {
      core.warning("venv-path is only used when activate-environment is true");
    }
    const tildeExpanded = expandTilde(venvPathInput);
    return normalizePath(resolveRelativePath(tildeExpanded));
  }
  return normalizePath(resolveRelativePath(".venv"));
}

function getEnableCache(): boolean {
  const enableCacheInput = core.getInput("enable-cache");
  if (enableCacheInput === "auto") {
    return process.env.RUNNER_ENVIRONMENT === "github-hosted";
  }
  return enableCacheInput === "true";
}

function getToolBinDir(): string | undefined {
  const toolBinDirInput = core.getInput("tool-bin-dir");
  if (toolBinDirInput !== "") {
    const tildeExpanded = expandTilde(toolBinDirInput);
    return resolveRelativePath(tildeExpanded);
  }
  if (process.platform === "win32") {
    if (process.env.RUNNER_TEMP !== undefined) {
      return `${process.env.RUNNER_TEMP}${path.sep}uv-tool-bin-dir`;
    }
    throw Error(
      "Could not determine UV_TOOL_BIN_DIR. Please make sure RUNNER_TEMP is set or provide the tool-bin-dir input",
    );
  }
  return undefined;
}

function getToolDir(): string | undefined {
  const toolDirInput = core.getInput("tool-dir");
  if (toolDirInput !== "") {
    const tildeExpanded = expandTilde(toolDirInput);
    return resolveRelativePath(tildeExpanded);
  }
  if (process.platform === "win32") {
    if (process.env.RUNNER_TEMP !== undefined) {
      return `${process.env.RUNNER_TEMP}${path.sep}uv-tool-dir`;
    }
    throw Error(
      "Could not determine UV_TOOL_DIR. Please make sure RUNNER_TEMP is set or provide the tool-dir input",
    );
  }
  return undefined;
}

function getCacheLocalPath():
  | {
      path: string;
      source: CacheLocalSource;
    }
  | undefined {
  const cacheLocalPathInput = core.getInput("cache-local-path");
  if (cacheLocalPathInput !== "") {
    const tildeExpanded = expandTilde(cacheLocalPathInput);
    return {
      path: resolveRelativePath(tildeExpanded),
      source: CacheLocalSource.Input,
    };
  }
  const cacheDirFromConfig = getCacheDirFromConfig();
  if (cacheDirFromConfig !== undefined) {
    return { path: cacheDirFromConfig, source: CacheLocalSource.Config };
  }
  if (process.env.UV_CACHE_DIR !== undefined) {
    core.info(`UV_CACHE_DIR is already set to ${process.env.UV_CACHE_DIR}`);
    return { path: process.env.UV_CACHE_DIR, source: CacheLocalSource.Env };
  }
  if (getEnableCache()) {
    if (process.env.RUNNER_ENVIRONMENT === "github-hosted") {
      if (process.env.RUNNER_TEMP !== undefined) {
        return {
          path: `${process.env.RUNNER_TEMP}${path.sep}setup-uv-cache`,
          source: CacheLocalSource.Default,
        };
      }
      throw Error(
        "Could not determine UV_CACHE_DIR. Please make sure RUNNER_TEMP is set or provide the cache-local-path input",
      );
    }
    if (process.platform === "win32") {
      return {
        path: `${process.env.APPDATA}${path.sep}uv${path.sep}cache`,
        source: CacheLocalSource.Default,
      };
    }
    return {
      path: `${process.env.HOME}${path.sep}.cache${path.sep}uv`,
      source: CacheLocalSource.Default,
    };
  }
}

function getCacheDirFromConfig(): string | undefined {
  for (const filePath of [versionFile, "uv.toml", "pyproject.toml"]) {
    const resolvedPath = resolveRelativePath(filePath);
    try {
      const cacheDir = getConfigValueFromTomlFile(resolvedPath, "cache-dir");
      if (cacheDir !== undefined) {
        core.info(`Found cache-dir in ${resolvedPath}: ${cacheDir}`);
        return cacheDir;
      }
    } catch (err) {
      const message = (err as Error).message;
      core.warning(`Error while parsing ${filePath}: ${message}`);
      return undefined;
    }
  }
  return undefined;
}

export function getUvPythonDir(): string {
  if (process.env.UV_PYTHON_INSTALL_DIR !== undefined) {
    core.info(
      `UV_PYTHON_INSTALL_DIR is already set to ${process.env.UV_PYTHON_INSTALL_DIR}`,
    );
    return process.env.UV_PYTHON_INSTALL_DIR;
  }
  if (process.env.RUNNER_ENVIRONMENT !== "github-hosted") {
    if (process.platform === "win32") {
      return `${process.env.APPDATA}${path.sep}uv${path.sep}python`;
    } else {
      return `${process.env.HOME}${path.sep}.local${path.sep}share${path.sep}uv${path.sep}python`;
    }
  }
  if (process.env.RUNNER_TEMP !== undefined) {
    return `${process.env.RUNNER_TEMP}${path.sep}uv-python-dir`;
  }
  throw Error(
    "Could not determine UV_PYTHON_INSTALL_DIR. Please make sure RUNNER_TEMP is set or provide the UV_PYTHON_INSTALL_DIR environment variable",
  );
}

function getCacheDependencyGlob(): string {
  const cacheDependencyGlobInput = core.getInput("cache-dependency-glob");
  if (cacheDependencyGlobInput !== "") {
    return cacheDependencyGlobInput
      .split("\n")
      .map((part) => part.trim())
      .map((part) => expandTilde(part))
      .map((part) => resolveRelativePath(part))
      .join("\n");
  }
  return cacheDependencyGlobInput;
}

function expandTilde(input: string): string {
  if (input.startsWith("~")) {
    return `${process.env.HOME}${input.substring(1)}`;
  }
  return input;
}

function normalizePath(inputPath: string): string {
  const normalized = path.normalize(inputPath);
  const root = path.parse(normalized).root;

  // Remove any trailing path separators, except when the whole path is the root.
  let trimmed = normalized;
  while (trimmed.length > root.length && trimmed.endsWith(path.sep)) {
    trimmed = trimmed.slice(0, -1);
  }

  return trimmed;
}

function resolveRelativePath(inputPath: string): string {
  const hasNegation = inputPath.startsWith("!");
  const pathWithoutNegation = hasNegation ? inputPath.substring(1) : inputPath;

  const resolvedPath = path.resolve(workingDirectory, pathWithoutNegation);

  core.debug(
    `Resolving relative path ${inputPath} to ${hasNegation ? "!" : ""}${resolvedPath}`,
  );
  return hasNegation ? `!${resolvedPath}` : resolvedPath;
}

function getManifestFile(): string | undefined {
  const manifestFileInput = core.getInput("manifest-file");
  if (manifestFileInput !== "") {
    return manifestFileInput;
  }
  return undefined;
}

function getResolutionStrategy(): "highest" | "lowest" {
  const resolutionStrategyInput = core.getInput("resolution-strategy");
  if (resolutionStrategyInput === "lowest") {
    return "lowest";
  }
  if (resolutionStrategyInput === "highest" || resolutionStrategyInput === "") {
    return "highest";
  }
  throw new Error(
    `Invalid resolution-strategy: ${resolutionStrategyInput}. Must be 'highest' or 'lowest'.`,
  );
}
```

## 38. Command

```sh
gh api 'repos/astral-sh/setup-uv/contents/src/utils/inputs.ts?ref=v10.2.0' --jq .content | base64 --decode
```

Exit: 0

```text
import fs from "node:fs";
import path from "node:path";
import * as core from "@actions/core";
import { getPythonVersionFromToolVersions } from "../version/tool-versions-file";
import { getConfigValueFromTomlFile } from "./config-file";
import * as log from "./logging";

export enum CacheLocalSource {
  Input,
  Config,
  Env,
  Default,
}

export interface CacheLocalPath {
  path: string;
  source: CacheLocalSource;
}

export type ResolutionStrategy = "highest" | "lowest";

export interface SetupInputs {
  workingDirectory: string;
  version: string;
  versionFile: string;
  pythonVersion: string;
  activateEnvironment: boolean;
  noProject: boolean;
  venvPath: string;
  checksum: string;
  enableCache: boolean;
  restoreCache: boolean;
  saveCache: boolean;
  cacheSuffix: string;
  cacheLocalPath?: CacheLocalPath;
  cacheDependencyGlob: string;
  pruneCache: boolean;
  cachePython: boolean;
  ignoreNothingToCache: boolean;
  ignoreEmptyWorkdir: boolean;
  toolBinDir?: string;
  toolDir?: string;
  pythonDir: string;
  githubToken: string;
  manifestFile?: string;
  downloadFromAstralMirror: boolean;
  addProblemMatchers: boolean;
  quiet: boolean;
  resolutionStrategy: ResolutionStrategy;
}

export function loadInputs(): SetupInputs {
  const workingDirectory = core.getInput("working-directory");
  const version = core.getInput("version");
  const versionFile = getVersionFile(workingDirectory);
  const pythonVersion = getPythonVersion(versionFile);
  const activateEnvironment = core.getBooleanInput("activate-environment");
  const noProject = core.getBooleanInput("no-project");
  const venvPath = getVenvPath(workingDirectory, activateEnvironment);
  const checksum = core.getInput("checksum");
  const enableCache = getEnableCache();
  const restoreCache = core.getInput("restore-cache") === "true";
  const saveCache = getSaveCache();
  const cacheSuffix = core.getInput("cache-suffix") || "";
  const cacheLocalPath = getCacheLocalPath(
    workingDirectory,
    versionFile,
    enableCache,
  );
  const cacheDependencyGlob = getCacheDependencyGlob(workingDirectory);
  const pruneCache = core.getInput("prune-cache") === "true";
  const cachePython = core.getInput("cache-python") === "true";
  const ignoreNothingToCache =
    core.getInput("ignore-nothing-to-cache") === "true";
  const ignoreEmptyWorkdir = core.getInput("ignore-empty-workdir") === "true";
  const toolBinDir = getToolBinDir(workingDirectory);
  const toolDir = getToolDir(workingDirectory);
  const pythonDir = getUvPythonDir();
  const githubToken = core.getInput("github-token");
  const manifestFile = getManifestFile();
  const downloadFromAstralMirror =
    core.getInput("download-from-astral-mirror") === "true";
  const addProblemMatchers = core.getInput("add-problem-matchers") === "true";
  const quiet = core.getInput("quiet") === "true";
  const resolutionStrategy = getResolutionStrategy();

  return {
    activateEnvironment,
    addProblemMatchers,
    cacheDependencyGlob,
    cacheLocalPath,
    cachePython,
    cacheSuffix,
    checksum,
    downloadFromAstralMirror,
    enableCache,
    githubToken,
    ignoreEmptyWorkdir,
    ignoreNothingToCache,
    manifestFile,
    noProject,
    pruneCache,
    pythonDir,
    pythonVersion,
    quiet,
    resolutionStrategy,
    restoreCache,
    saveCache,
    toolBinDir,
    toolDir,
    venvPath,
    version,
    versionFile,
    workingDirectory,
  };
}

function getVersionFile(workingDirectory: string): string {
  const versionFileInput = core.getInput("version-file");
  if (versionFileInput !== "") {
    const tildeExpanded = expandTilde(versionFileInput);
    return resolveRelativePath(workingDirectory, tildeExpanded);
  }
  return versionFileInput;
}

function getPythonVersion(versionFile: string): string {
  const pythonVersionInput = core.getInput("python-version");
  if (pythonVersionInput !== "") {
    return pythonVersionInput;
  }
  if (process.env.UV_PYTHON !== undefined && process.env.UV_PYTHON !== "") {
    return "";
  }
  if (versionFile === "" || !fs.existsSync(versionFile)) {
    return "";
  }

  try {
    return getPythonVersionFromToolVersions(versionFile) ?? "";
  } catch (err) {
    log.warning(
      `Error while parsing Python version from ${versionFile}: ${(err as Error).message}`,
    );
    return "";
  }
}

function getVenvPath(
  workingDirectory: string,
  activateEnvironment: boolean,
): string {
  const venvPathInput = core.getInput("venv-path");
  if (venvPathInput !== "") {
    if (!activateEnvironment) {
      log.warning("venv-path is only used when activate-environment is true");
    }
    const tildeExpanded = expandTilde(venvPathInput);
    return normalizePath(resolveRelativePath(workingDirectory, tildeExpanded));
  }
  return normalizePath(resolveRelativePath(workingDirectory, ".venv"));
}

function getEnableCache(): boolean {
  const enableCacheInput = core.getInput("enable-cache");
  if (enableCacheInput === "auto") {
    if (process.env.RUNNER_ENVIRONMENT !== "github-hosted") {
      return false;
    }

    const eventName = process.env.GITHUB_EVENT_NAME;
    const isTagPush =
      eventName === "push" && process.env.GITHUB_REF?.startsWith("refs/tags/");
    if (isTagPush) {
      log.info("Caching is disabled for tag pushes");
      return false;
    }
    if (
      eventName === "pull_request_target" ||
      eventName === "workflow_run" ||
      eventName === "release"
    ) {
      log.info(`Caching is disabled for the ${eventName} event`);
      return false;
    }

    return true;
  }
  return enableCacheInput === "true";
}

function getSaveCache(): boolean {
  const saveCacheInput = core.getInput("save-cache");
  if (saveCacheInput === "auto") {
    if (process.env.GITHUB_EVENT_NAME === "merge_group") {
      log.info("Cache saving is disabled for the merge_group event");
      return false;
    }
    return true;
  }
  return saveCacheInput === "true";
}

function getToolBinDir(workingDirectory: string): string | undefined {
  const toolBinDirInput = core.getInput("tool-bin-dir");
  if (toolBinDirInput !== "") {
    const tildeExpanded = expandTilde(toolBinDirInput);
    return resolveRelativePath(workingDirectory, tildeExpanded);
  }
  if (process.platform === "win32") {
    if (process.env.RUNNER_TEMP !== undefined) {
      return `${process.env.RUNNER_TEMP}${path.sep}uv-tool-bin-dir`;
    }
    throw Error(
      "Could not determine UV_TOOL_BIN_DIR. Please make sure RUNNER_TEMP is set or provide the tool-bin-dir input",
    );
  }
  return undefined;
}

function getToolDir(workingDirectory: string): string | undefined {
  const toolDirInput = core.getInput("tool-dir");
  if (toolDirInput !== "") {
    const tildeExpanded = expandTilde(toolDirInput);
    return resolveRelativePath(workingDirectory, tildeExpanded);
  }
  if (process.platform === "win32") {
    if (process.env.RUNNER_TEMP !== undefined) {
      return `${process.env.RUNNER_TEMP}${path.sep}uv-tool-dir`;
    }
    throw Error(
      "Could not determine UV_TOOL_DIR. Please make sure RUNNER_TEMP is set or provide the tool-dir input",
    );
  }
  return undefined;
}

function getCacheLocalPath(
  workingDirectory: string,
  versionFile: string,
  enableCache: boolean,
): CacheLocalPath | undefined {
  const cacheLocalPathInput = core.getInput("cache-local-path");
  if (cacheLocalPathInput !== "") {
    const tildeExpanded = expandTilde(cacheLocalPathInput);
    return {
      path: resolveRelativePath(workingDirectory, tildeExpanded),
      source: CacheLocalSource.Input,
    };
  }
  const cacheDirFromConfig = getCacheDirFromConfig(
    workingDirectory,
    versionFile,
  );
  if (cacheDirFromConfig !== undefined) {
    return { path: cacheDirFromConfig, source: CacheLocalSource.Config };
  }
  if (process.env.UV_CACHE_DIR !== undefined) {
    log.info(`UV_CACHE_DIR is already set to ${process.env.UV_CACHE_DIR}`);
    return { path: process.env.UV_CACHE_DIR, source: CacheLocalSource.Env };
  }
  if (enableCache) {
    if (process.env.RUNNER_ENVIRONMENT === "github-hosted") {
      if (process.env.RUNNER_TEMP !== undefined) {
        return {
          path: `${process.env.RUNNER_TEMP}${path.sep}setup-uv-cache`,
          source: CacheLocalSource.Default,
        };
      }
      throw Error(
        "Could not determine UV_CACHE_DIR. Please make sure RUNNER_TEMP is set or provide the cache-local-path input",
      );
    }
    if (process.platform === "win32") {
      return {
        path: `${process.env.APPDATA}${path.sep}uv${path.sep}cache`,
        source: CacheLocalSource.Default,
      };
    }
    return {
      path: `${process.env.HOME}${path.sep}.cache${path.sep}uv`,
      source: CacheLocalSource.Default,
    };
  }
}

function getCacheDirFromConfig(
  workingDirectory: string,
  versionFile: string,
): string | undefined {
  for (const filePath of [versionFile, "uv.toml", "pyproject.toml"]) {
    const resolvedPath = resolveRelativePath(workingDirectory, filePath);
    try {
      const cacheDir = getConfigValueFromTomlFile(resolvedPath, "cache-dir");
      if (cacheDir !== undefined) {
        log.info(`Found cache-dir in ${resolvedPath}: ${cacheDir}`);
        return cacheDir;
      }
    } catch (err) {
      const message = (err as Error).message;
      log.warning(`Error while parsing ${filePath}: ${message}`);
      return undefined;
    }
  }
  return undefined;
}

export function getUvPythonDir(): string {
  if (process.env.UV_PYTHON_INSTALL_DIR !== undefined) {
    log.info(
      `UV_PYTHON_INSTALL_DIR is already set to ${process.env.UV_PYTHON_INSTALL_DIR}`,
    );
    return process.env.UV_PYTHON_INSTALL_DIR;
  }
  if (process.env.RUNNER_ENVIRONMENT !== "github-hosted") {
    if (process.platform === "win32") {
      return `${process.env.APPDATA}${path.sep}uv${path.sep}python`;
    }
    return `${process.env.HOME}${path.sep}.local${path.sep}share${path.sep}uv${path.sep}python`;
  }
  if (process.env.RUNNER_TEMP !== undefined) {
    return `${process.env.RUNNER_TEMP}${path.sep}uv-python-dir`;
  }
  throw Error(
    "Could not determine UV_PYTHON_INSTALL_DIR. Please make sure RUNNER_TEMP is set or provide the UV_PYTHON_INSTALL_DIR environment variable",
  );
}

function getCacheDependencyGlob(workingDirectory: string): string {
  const cacheDependencyGlobInput = core.getInput("cache-dependency-glob");
  if (cacheDependencyGlobInput !== "") {
    return cacheDependencyGlobInput
      .split("\n")
      .map((part) => part.trim())
      .map((part) => expandTilde(part))
      .map((part) => resolveRelativePath(workingDirectory, part))
      .join("\n");
  }
  return cacheDependencyGlobInput;
}

function expandTilde(input: string): string {
  if (input.startsWith("~")) {
    return `${process.env.HOME}${input.substring(1)}`;
  }
  return input;
}

function normalizePath(inputPath: string): string {
  const normalized = path.normalize(inputPath);
  const root = path.parse(normalized).root;

  // Remove any trailing path separators, except when the whole path is the root.
  let trimmed = normalized;
  while (trimmed.length > root.length && trimmed.endsWith(path.sep)) {
    trimmed = trimmed.slice(0, -1);
  }

  return trimmed;
}

function resolveRelativePath(
  workingDirectory: string,
  inputPath: string,
): string {
  const hasNegation = inputPath.startsWith("!");
  const pathWithoutNegation = hasNegation ? inputPath.substring(1) : inputPath;

  const resolvedPath = path.resolve(workingDirectory, pathWithoutNegation);

  core.debug(
    `Resolving relative path ${inputPath} to ${hasNegation ? "!" : ""}${resolvedPath}`,
  );
  return hasNegation ? `!${resolvedPath}` : resolvedPath;
}

function getManifestFile(): string | undefined {
  const manifestFileInput = core.getInput("manifest-file");
  if (manifestFileInput !== "") {
    return manifestFileInput;
  }
  return undefined;
}

function getResolutionStrategy(): ResolutionStrategy {
  const resolutionStrategyInput = core.getInput("resolution-strategy");
  if (resolutionStrategyInput === "lowest") {
    return "lowest";
  }
  if (resolutionStrategyInput === "highest" || resolutionStrategyInput === "") {
    return "highest";
  }
  throw new Error(
    `Invalid resolution-strategy: ${resolutionStrategyInput}. Must be 'highest' or 'lowest'.`,
  );
}
```

## 39. Command

```sh
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T8: setup-uv PR155 old run34730808923 failed macOS shfmt before setup-uv; PermissionError is the expected network-denial oracle. Main bf2110f fixed heredoc formatting and pinned shfmt3.14.1. Current PR155 tests pass; cache-disabled SHA-pinned usage needs no v8-v10 adjustment. PR125 only updates installed Nix2.34.8 to2.35.2; no local nix and filtered CI skipped its job, so static compatibility verdict is not runtime proof.'
```

Exit: 0

```text
c14a8e35-136b-4807-b3c2-bc4f89aa1d47
```
