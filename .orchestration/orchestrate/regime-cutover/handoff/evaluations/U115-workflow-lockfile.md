# U115 Workflow lockfile evaluation (plan P-35, research V4-4)

Measured on 2026-10-29 (UTC) with `gh version 2.103.2 (2026-10-23)` and the extension `gh actions-lock` `v0.4.0` (the `gh extension list` line below), in a worktree at `origin/main` `e91edfa7228b02397e59817bccabf8604883b343`. This file is a record. Nothing in it runs.

## Question

Does `.github/workflows/actions.lock` replace or supplement the SHA pins in this repository's eleven workflows, and what should the coordinator do with Dependabot #548 (astral-sh/setup-uv 10.2.0 to 10.3.2) and #549 (jdx/mise-action 4.3.0 to 5.2.2)?

Short answer. Today the lockfile cannot supplement the pins: the extension that writes it also rewrites every `uses:` line from `@<40-hex>` to `@<tag>`, so the repository would trade its own SHA invariant (`tests/unit/test_workflow_security.py:133-145`) for the runner's lockfile check. The measured gain is one transitive dependency. Defer the lockfile. Adopt both Dependabot bumps as units, each for a reason from its release notes, not because the bot opened them. The owner touched neither PR.

## Commands run

Every command of CHANGE 1 to 3 of the brief, in the order run, with its output pasted whole. Network calls ran under `perl -e 'alarm 120; exec @ARGV'`, shown as `perl -e alarm 120; exec @ARGV` or `N` in the echoed command line. Two edits to pasted output, both named here. In the `--no-fix` block the extension's run-log path starts with the home directory, written here as `~`, because the handoff rules forbid an absolute home path in the file. The two mise-action release notes are Markdown with their own `##` headings, so each of their lines is indented by one space; otherwise the heading check of this file would count them.

### Extension, installed under a scratch `XDG_DATA_HOME`

`export XDG_DATA_HOME="$TMPDIR/U115-gh-data"` preceded every `gh extension` and `gh actions-lock` call. The first `gh extension list` ran before the install and printed nothing.

```text
$ gh extension list (before)
exit=0
$ gh extension install github/gh-actions-lock
exit=0
$ gh extension list
gh actions-lock	github/gh-actions-lock	v0.4.0
```

```text
$ gh actions-lock --help
Lock and verify GitHub Actions dependencies to protect your workflows
from supply chain attacks.

Actions are resolved by mutable tags and branches at runtime. This
extension pins every direct and transitive dependency to an immutable
commit SHA in a per-repo lockfile at .github/workflows/actions.lock,
so changes are visible in pull request diffs and tampered or hijacked
actions are caught before they run.

Scans all workflows under .github/workflows/ by default and fixes
what it can — pinning every resolvable action and updating the
lockfile. Pass --no-fix for a read-only check that writes nothing.

HOST AND AUTHENTICATION

Supported targets are github.com and GitHub Enterprise Cloud with data
residency (*.ghe.com). GitHub Enterprise Server (GHES) is not supported.

In a tenant repository checkout, authenticate with
gh auth login --hostname TENANT.ghe.com, then run gh actions-lock.

Host selection: --hostname, then GH_HOST, then the current repository
(GH_REPO or a remote on a host known to gh), then github.com.
For github.com and *.ghe.com, GH_TOKEN takes precedence over GITHUB_TOKEN
and stored per-host credentials.
--hostname selects the host; it does not override token variables.

On *.ghe.com, actions from public github.com repositories are read with
GH_ACTIONS_LOCK_GITHUB_COM_TOKEN, else the login from
gh auth login --hostname github.com, else anonymously (60 requests/hour
per IP). GH_TOKEN and GITHUB_TOKEN are never sent to github.com.

If an unintended token override causes authentication to fail, check
stored tenant credentials without exposing tokens:
  env -u GH_TOKEN -u GITHUB_TOKEN gh auth status --hostname TENANT.ghe.com

For setup and troubleshooting:
  https://github.com/github/gh-actions-lock#github-enterprise-cloud-with-data-residency

REF NARROWING

When a new workflow is first pinned and uses a partial version ref
like actions/checkout@v4, the lockfile narrows it to the highest
matching full semver tag (e.g. v4.2.1). Full semver tags are
effectively immutable — unlike major/minor splats, they almost never
move once published, so the pinned SHA stays valid longer between
lockfile refreshes.

Only freshly pinned refs are narrowed — already-locked deps are not
touched. Only refs that parse as semantic versions (v4, v3.2) are
candidates; branch names (main, canary) and non-version tags are
never narrowed because the latest semver release in a repo may have
nothing to do with the ref the workflow intended.
Pass --no-narrow to disable this behavior entirely.

--json selects the output format only (independent of --no-fix);
structured results go to stdout and progress to stderr:

  gh actions-lock --no-fix --json 2>/dev/null | jq .valid

ENVIRONMENT

GH_ACTIONS_LOCK_REPO_ROOT names the repository root instead of
searching parent directories for .git. Set it when relocking a
partial checkout without .git. $/ actions resolve against it, and
the directory must exist and contain the workflows.

GH_ACTIONS_LOCK_GITHUB_COM_TOKEN is a github.com token for reading
public github.com actions on *.ghe.com, for CI where there is no gh
login. A GHE.com job's GITHUB_TOKEN is issued by the tenant and doesn't
work on github.com. Use a fine-grained token with no permissions. It is
never sent to the tenant, or used when github.com is the selected host.

RUN LOGS

Every run except --verify-local saves its full --json output, plus the
repository and whether the run succeeded (with its error, if any), to
<user cache dir>/gh-actions-lock/logs/ (on macOS,
~/Library/Caches/gh-actions-lock/logs). Failed runs print the path.
Logs are kept for 14 days, up to 50. Attach the log to bug reports.

Usage:
  actions-lock [<workflow-path>...] [flags]

Examples:
# Verify all workflows and fix what's fixable
$ gh actions-lock

# Verify a specific workflow
$ gh actions-lock .github/workflows/ci.yml

# Read-only check for CI integration (writes nothing, exits 1 if invalid)
$ gh actions-lock --no-fix --json=valid,findings

# All fields as JSON
$ gh actions-lock --json


Flags:
      --accept-moved                               Re-resolve deps flagged as ref-moved or unreachable-pin to their current live SHA
  -A, --allow-all-runners                          Deprecated no-op: runner restrictions have been removed
      --allow-runners strings                      Deprecated no-op: runner restrictions have been removed
  -h, --help                                       help for actions-lock
      --hostname string                            GitHub hostname to query (defaults to GH_HOST, current repo host, or github.com)
      --ignore-local-actions ./…                 Warn instead of failing when a local ./… action uses remote actions the lockfile can't cover
      --json fields[="valid,findings,workflows"]   Output JSON with the specified fields (valid,findings,workflows,dependencies,pins)
      --migrate-local-actions uses: ./…          Rewrite same-repo uses: ./… actions to the inherently-pinned `uses: $/…` form, in workflows and in-repo action files
      --no-fix                                     Read-only: report findings without modifying workflows or the lockfile
      --no-interactive                             Run without interactive prompts
      --no-narrow                                  Keep mutable version refs (e.g. v4) instead of narrowing to full semver (e.g. v4.2.1).
                                                   Only refs that parse as semantic versions are narrowed (v4, v4.2); branch names
                                                   like 'main' or non-version tags are never narrowed because a full semver tag is
                                                   far more likely to resolve to exactly one commit for its entire lifetime.
      --no-onboard                                 Refuse to onboard new workflows or actions; only re-pin already-tracked entries
      --profile dir                                Enable profiling: write trace, CPU profile, and HTTP log to dir
      --relock                                     Re-resolve every ref and advance moved ones (e.g. main, v4) to their current upstream SHA; leaves unreachable pins as errors
      --verify                                     Frozen check: run the same checks as the default without writing; fails if the lockfile is incomplete or the runner would reject a pin
      --verify-local                               Offline lockfile coverage check: verify every action ref has a lockfile entry.
                                                   No network calls, no authentication, no file writes — ideal for pre-commit hooks.
                                                   It does not check that the entries are trustworthy; use --verify in CI for that.
  -v, --version                                    version for actions-lock
exit=0
```

### Lockfile measurements, from the worktree root

`--help` lists `--no-fix` as "Read-only: report findings without modifying workflows or the lockfile", so that mode ran first. It writes nothing, so it also produces no lockfile to read. The writing run followed, so CHANGE 2 could measure the lockfile content, the `uses:` rewrite and the test, and the revert then restored the tree.

Read-only check. Exit 1 is the extension's report that nothing is locked yet.

```text
$ perl -e alarm 120; exec @ARGV gh actions-lock --no-fix --no-interactive
Scanning 11 workflows
6 actions are pinned to a bare SHA without a tag ref
↳ run `gh actions-lock` to pin to tagged releases
11 of 11 workflows failed
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
  used in workflow but not pinned in lockfile (actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
  ↳ .github/workflows/agent-assets.yml
  ↳ .github/workflows/apply-check.yml
  ↳ .github/workflows/docs-check.yml
  ↳ .github/workflows/docs.yml
  ↳ .github/workflows/drift-watch.yml
  ↳ .github/workflows/macos.yaml
  ↳ .github/workflows/private-bootstrap.yaml
  ↳ .github/workflows/regime.yml
  ↳ .github/workflows/remote.yaml
  ↳ .github/workflows/test.yaml
  ↳ .github/workflows/ubuntu.yaml
✗ Not pinned astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7
  used in workflow but not pinned in lockfile (astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7
  used in workflow but not pinned in lockfile (astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7
  used in workflow but not pinned in lockfile (astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7
  used in workflow but not pinned in lockfile (astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7
  used in workflow but not pinned in lockfile (astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7
  used in workflow but not pinned in lockfile (astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
  ↳ .github/workflows/agent-assets.yml
  ↳ .github/workflows/docs-check.yml
  ↳ .github/workflows/docs.yml
  ↳ .github/workflows/drift-watch.yml
  ↳ .github/workflows/regime.yml
  ↳ .github/workflows/test.yaml
✗ Not pinned jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c
  used in workflow but not pinned in lockfile (jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c
  used in workflow but not pinned in lockfile (jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c
  used in workflow but not pinned in lockfile (jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c
  used in workflow but not pinned in lockfile (jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c
  used in workflow but not pinned in lockfile (jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
  ↳ .github/workflows/docs-check.yml
  ↳ .github/workflows/docs.yml
  ↳ .github/workflows/macos.yaml
  ↳ .github/workflows/test.yaml
  ↳ .github/workflows/ubuntu.yaml
✗ Not pinned webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555
  used in workflow but not pinned in lockfile (webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555
  used in workflow but not pinned in lockfile (webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
✗ Not pinned webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555
  used in workflow but not pinned in lockfile (webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
  ↳ .github/workflows/macos.yaml
  ↳ .github/workflows/private-bootstrap.yaml
  ↳ .github/workflows/ubuntu.yaml
✗ Not pinned benchmark-action/github-action-benchmark@4322e5726e6334590d251fc4f92bec0efafc45dc
  used in workflow but not pinned in lockfile (benchmark-action/github-action-benchmark@4322e5726e6334590d251fc4f92bec0efafc45dc)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
  ↳ .github/workflows/macos.yaml
✗ Not pinned codecov/codecov-action@303a32d7a59b442fa8d48b6a1cc6825c09c847a5
  used in workflow but not pinned in lockfile (codecov/codecov-action@303a32d7a59b442fa8d48b6a1cc6825c09c847a5)
  see: https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md#not-pinned
  ↳ .github/workflows/test.yaml
Re-run without --no-fix to apply fixes.
Run log: ~/Library/Caches/gh-actions-lock/logs/run-20261029-151018-3199662212.json
exit=1
```

The tree after the read-only check: unchanged.

```text
$ git status --porcelain
exit=0
```

The writing run.

```text
$ perl -e alarm 120; exec @ARGV gh actions-lock --no-interactive
Scanning 11 workflows
Planning pins
Pinned 6 actions (+ 1 transitive) across 11 workflows
  actions/checkout@v7.0.1 (3d3c42e)
    └─ .github/workflows/agent-assets.yml
    └─ .github/workflows/apply-check.yml
    └─ .github/workflows/docs-check.yml
    └─ .github/workflows/docs.yml
    └─ .github/workflows/drift-watch.yml
    └─ .github/workflows/macos.yaml
    └─ .github/workflows/private-bootstrap.yaml
    └─ .github/workflows/regime.yml
    └─ .github/workflows/remote.yaml
    └─ .github/workflows/test.yaml
    └─ .github/workflows/ubuntu.yaml
  astral-sh/setup-uv@v10.2.0 (c18668a)
    └─ .github/workflows/agent-assets.yml
    └─ .github/workflows/docs-check.yml
    └─ .github/workflows/docs.yml
    └─ .github/workflows/drift-watch.yml
    └─ .github/workflows/regime.yml
    └─ .github/workflows/test.yaml
  jdx/mise-action@v4.3.0 (c2a8761)
    └─ .github/workflows/docs-check.yml
    └─ .github/workflows/docs.yml
    └─ .github/workflows/macos.yaml
    └─ .github/workflows/test.yaml
    └─ .github/workflows/ubuntu.yaml
  webfactory/ssh-agent@v0.10.0 (e838748)
    └─ .github/workflows/macos.yaml
    └─ .github/workflows/private-bootstrap.yaml
    └─ .github/workflows/ubuntu.yaml
  benchmark-action/github-action-benchmark@v1.22.2 (4322e57)
    └─ .github/workflows/macos.yaml
  codecov/codecov-action@v7.1.1 (303a32d)
    └─ .github/workflows/test.yaml
Transitive dependencies (from composite actions):
  actions/github-script@ed59741 via codecov/codecov-action@v7.1.1
exit=0
```

The tree after the writing run: eleven modified workflows and one untracked lockfile.

```text
$ git status --porcelain
 M .github/workflows/agent-assets.yml
 M .github/workflows/apply-check.yml
 M .github/workflows/docs-check.yml
 M .github/workflows/docs.yml
 M .github/workflows/drift-watch.yml
 M .github/workflows/macos.yaml
 M .github/workflows/private-bootstrap.yaml
 M .github/workflows/regime.yml
 M .github/workflows/remote.yaml
 M .github/workflows/test.yaml
 M .github/workflows/ubuntu.yaml
?? .github/workflows/actions.lock
exit=0
```

The workflow diff. Every `@<40-hex> # v<n>` reference became `@v<x.y.z>`.

```text
$ git diff -- .github/workflows
diff --git a/.github/workflows/agent-assets.yml b/.github/workflows/agent-assets.yml
index 0d61a5a5..4b16785a 100644
--- a/.github/workflows/agent-assets.yml
+++ b/.github/workflows/agent-assets.yml
@@ -31,12 +31,12 @@ jobs:
         run: git config --global init.defaultBranch main

       - name: Checkout repository
-        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+        uses: actions/checkout@v7.0.1
         with:
           persist-credentials: false

       - name: Setup uv
-        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+        uses: astral-sh/setup-uv@v10.2.0
         with:
           enable-cache: false

diff --git a/.github/workflows/apply-check.yml b/.github/workflows/apply-check.yml
index 8b427ca0..d068a2c4 100644
--- a/.github/workflows/apply-check.yml
+++ b/.github/workflows/apply-check.yml
@@ -26,7 +26,7 @@ jobs:
     timeout-minutes: 15

     steps:
-      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+      - uses: actions/checkout@v7.0.1
         with:
           persist-credentials: false

diff --git a/.github/workflows/docs-check.yml b/.github/workflows/docs-check.yml
index 3a970b12..8617b9e8 100644
--- a/.github/workflows/docs-check.yml
+++ b/.github/workflows/docs-check.yml
@@ -37,18 +37,18 @@ jobs:
         run: git config --global init.defaultBranch main

       - name: Checkout repository
-        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+        uses: actions/checkout@v7.0.1
         with:
           fetch-depth: 0
           persist-credentials: false

       - name: Setup uv
-        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+        uses: astral-sh/setup-uv@v10.2.0
         with:
           enable-cache: false

       - name: Setup mise
-        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+        uses: jdx/mise-action@v4.3.0
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
diff --git a/.github/workflows/docs.yml b/.github/workflows/docs.yml
index 4ddf3005..de009afd 100644
--- a/.github/workflows/docs.yml
+++ b/.github/workflows/docs.yml
@@ -36,18 +36,18 @@ jobs:
         run: git config --global init.defaultBranch main

       - name: Checkout repository
-        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+        uses: actions/checkout@v7.0.1
         with:
           fetch-depth: 0
           persist-credentials: false

       - name: Setup uv
-        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+        uses: astral-sh/setup-uv@v10.2.0
         with:
           enable-cache: false

       - name: Setup mise
-        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+        uses: jdx/mise-action@v4.3.0
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
diff --git a/.github/workflows/drift-watch.yml b/.github/workflows/drift-watch.yml
index a261909f..ea0cb83d 100644
--- a/.github/workflows/drift-watch.yml
+++ b/.github/workflows/drift-watch.yml
@@ -25,10 +25,10 @@ jobs:
     runs-on: ubuntu-24.04
     timeout-minutes: 10
     steps:
-      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+      - uses: actions/checkout@v7.0.1
         with:
           persist-credentials: false
-      - uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+      - uses: astral-sh/setup-uv@v10.2.0
         with:
           enable-cache: false
       - name: Run the drift watch
diff --git a/.github/workflows/macos.yaml b/.github/workflows/macos.yaml
index 9758a2a4..95521cd1 100644
--- a/.github/workflows/macos.yaml
+++ b/.github/workflows/macos.yaml
@@ -91,12 +91,12 @@ jobs:

     steps:
       - name: Set up SSH agent and add the private deploy key for the private dotfiles repo
-        uses: webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555 # v0.10.0
+        uses: webfactory/ssh-agent@v0.10.0
         with:
           ssh-private-key: ${{ secrets.PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY }}

       - name: Checkout repository
-        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+        uses: actions/checkout@v7.0.1
         with:
           persist-credentials: false

@@ -158,7 +158,7 @@ jobs:

       - name: Store benchmark result
         if: ${{ env.HAS_BENCHMARK_TOKEN == 'true' }}
-        uses: benchmark-action/github-action-benchmark@4322e5726e6334590d251fc4f92bec0efafc45dc # v1
+        uses: benchmark-action/github-action-benchmark@v1.22.2
         with:
           # Each image keeps its own series, so runner hardware never mixes in one; the historic
           # "MacOS benchmark" series holds macos-14 data and ends with that image's retirement (U64b).
@@ -174,7 +174,7 @@ jobs:
           alert-comment-cc-users: "@mryfmo"
           benchmark-data-dir-path: "."

-      - uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+      - uses: jdx/mise-action@v4.3.0
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
diff --git a/.github/workflows/private-bootstrap.yaml b/.github/workflows/private-bootstrap.yaml
index 7cc5e11e..7ad18150 100644
--- a/.github/workflows/private-bootstrap.yaml
+++ b/.github/workflows/private-bootstrap.yaml
@@ -81,7 +81,7 @@ jobs:
           mkdir -p "${RUNNER_TEMP}/dotfiles-home"
           printf 'HOME=%s/dotfiles-home\n' "${RUNNER_TEMP}" >> "${GITHUB_ENV}"

-      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+      - uses: actions/checkout@v7.0.1
         with:
           fetch-depth: 0
           persist-credentials: false
@@ -160,7 +160,7 @@ jobs:

       - name: Set up the private deploy key
         if: ${{ steps.decide.outputs.should_run == 'true' }}
-        uses: webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555 # v0.10.0
+        uses: webfactory/ssh-agent@v0.10.0
         with:
           ssh-private-key: ${{ secrets.PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY }}

diff --git a/.github/workflows/regime.yml b/.github/workflows/regime.yml
index e07f5e9a..f975828b 100644
--- a/.github/workflows/regime.yml
+++ b/.github/workflows/regime.yml
@@ -24,14 +24,14 @@ jobs:
     runs-on: ubuntu-24.04
     timeout-minutes: 10
     steps:
-      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+      - uses: actions/checkout@v7.0.1
         with:
           fetch-depth: 0
           # The base branch's tip at run time: the event's recorded base sha can lag the branch (on PR #420 it was the
           # head's fork point, from before this verifier; ci:39185982423:1). The pull request cannot move this branch.
           ref: refs/heads/${{ github.base_ref }}
           persist-credentials: false
-      - uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+      - uses: astral-sh/setup-uv@v10.2.0
         with:
           enable-cache: false
       - name: Fetch the pull request's head as data
diff --git a/.github/workflows/remote.yaml b/.github/workflows/remote.yaml
index ed237491..7db4886e 100644
--- a/.github/workflows/remote.yaml
+++ b/.github/workflows/remote.yaml
@@ -47,7 +47,7 @@ jobs:
           mkdir -p "${RUNNER_TEMP}/dotfiles-home"
           printf 'HOME=%s/dotfiles-home\n' "${RUNNER_TEMP}" >> "${GITHUB_ENV}"

-      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+      - uses: actions/checkout@v7.0.1
         with:
           fetch-depth: 0
           persist-credentials: false
diff --git a/.github/workflows/test.yaml b/.github/workflows/test.yaml
index 5257882a..a402d058 100644
--- a/.github/workflows/test.yaml
+++ b/.github/workflows/test.yaml
@@ -63,7 +63,7 @@ jobs:
         run: git config --global init.defaultBranch main

       - name: Checkout repository
-        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+        uses: actions/checkout@v7.0.1
         with:
           fetch-depth: 0
           persist-credentials: false
@@ -262,7 +262,7 @@ jobs:

       - name: Setup mise for statusline smoke
         if: ${{ steps.decide.outputs.should_test == 'true' }}
-        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+        uses: jdx/mise-action@v4.3.0
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
@@ -439,7 +439,7 @@ jobs:

       - name: Setup uv
         if: ${{ steps.decide.outputs.should_test == 'true' }}
-        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+        uses: astral-sh/setup-uv@v10.2.0
         with:
           enable-cache: false

@@ -537,7 +537,7 @@ jobs:

       - name: Upload coverage to Codecov
         if: ${{ steps.decide.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}
-        uses: codecov/codecov-action@303a32d7a59b442fa8d48b6a1cc6825c09c847a5 # v7
+        uses: codecov/codecov-action@v7.1.1
         env:
           CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
         with:
diff --git a/.github/workflows/ubuntu.yaml b/.github/workflows/ubuntu.yaml
index a266d8d2..9db9a0bf 100644
--- a/.github/workflows/ubuntu.yaml
+++ b/.github/workflows/ubuntu.yaml
@@ -76,12 +76,12 @@ jobs:

     steps:
       - name: Set up SSH agent and add the private deploy key for the private dotfiles repo
-        uses: webfactory/ssh-agent@e83874834305fe9a4a2997156cb26c5de65a8555 # v0.10.0
+        uses: webfactory/ssh-agent@v0.10.0
         with:
           ssh-private-key: ${{ secrets.PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY }}

       - name: Checkout repository
-        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
+        uses: actions/checkout@v7.0.1
         with:
           persist-credentials: false

@@ -124,7 +124,7 @@ jobs:
           after_local_change="$(cksum "${HOME}/.zprofile")"
           [ "${after_local_change}" = "${before_local_change}" ]

-      - uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+      - uses: jdx/mise-action@v4.3.0
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
exit=0
```

The lockfile whole.

```text
$ cat .github/workflows/actions.lock
# This file is machine-generated by `gh actions-lock`.
# Do not edit by hand; run `gh actions-lock` to update.
# Docs: https://gh.io/actions-lockfile
version: 'v0.0.3'
workflows:
    '.github/workflows/agent-assets.yml':
        - 'actions/checkout@v7.0.1'
        - 'astral-sh/setup-uv@v10.2.0'
    '.github/workflows/apply-check.yml':
        - 'actions/checkout@v7.0.1'
    '.github/workflows/docs-check.yml':
        - 'actions/checkout@v7.0.1'
        - 'astral-sh/setup-uv@v10.2.0'
        - 'jdx/mise-action@v4.3.0'
    '.github/workflows/docs.yml':
        - 'actions/checkout@v7.0.1'
        - 'astral-sh/setup-uv@v10.2.0'
        - 'jdx/mise-action@v4.3.0'
    '.github/workflows/drift-watch.yml':
        - 'actions/checkout@v7.0.1'
        - 'astral-sh/setup-uv@v10.2.0'
    '.github/workflows/macos.yaml':
        - 'actions/checkout@v7.0.1'
        - 'benchmark-action/github-action-benchmark@v1.22.2'
        - 'jdx/mise-action@v4.3.0'
        - 'webfactory/ssh-agent@v0.10.0'
    '.github/workflows/private-bootstrap.yaml':
        - 'actions/checkout@v7.0.1'
        - 'webfactory/ssh-agent@v0.10.0'
    '.github/workflows/regime.yml':
        - 'actions/checkout@v7.0.1'
        - 'astral-sh/setup-uv@v10.2.0'
    '.github/workflows/remote.yaml':
        - 'actions/checkout@v7.0.1'
    '.github/workflows/test.yaml':
        - 'actions/checkout@v7.0.1'
        - 'astral-sh/setup-uv@v10.2.0'
        - 'codecov/codecov-action@v7.1.1'
        - 'jdx/mise-action@v4.3.0'
    '.github/workflows/ubuntu.yaml':
        - 'actions/checkout@v7.0.1'
        - 'jdx/mise-action@v4.3.0'
        - 'webfactory/ssh-agent@v0.10.0'
dependencies:
    'actions/checkout@v7.0.1':
        ref: 'v7.0.1'
        commit: 'sha1-3d3c42e5aac5ba805825da76410c181273ba90b1'
        owner_id: 44036562
        repo_id: 197814629
    'actions/github-script@ed597411d8f924073f98dfc5c65a23a2325f34cd':
        ref: 'v8.0.0'
        commit: 'sha1-ed597411d8f924073f98dfc5c65a23a2325f34cd'
        owner_id: 44036562
        repo_id: 205262760
    'astral-sh/setup-uv@v10.2.0':
        ref: 'v10.2.0'
        commit: 'sha1-c18668ad3cf93ea998bef934396af7bb5c839dc7'
        owner_id: 115962839
        repo_id: 846733598
    'benchmark-action/github-action-benchmark@v1.22.2':
        ref: 'v1.22.2'
        commit: 'sha1-4322e5726e6334590d251fc4f92bec0efafc45dc'
        owner_id: 91769432
        repo_id: 219665796
    'codecov/codecov-action@v7.1.1':
        ref: 'v7.1.1'
        commit: 'sha1-303a32d7a59b442fa8d48b6a1cc6825c09c847a5'
        owner_id: 8226205
        repo_id: 200299178
        uses:
            - 'actions/github-script@ed597411d8f924073f98dfc5c65a23a2325f34cd'
    'jdx/mise-action@v4.3.0':
        ref: 'v4.3.0'
        commit: 'sha1-c2a87611a18de5b3828c5652fe268e992400cb5c'
        owner_id: 216188
        repo_id: 738284564
    'webfactory/ssh-agent@v0.10.0':
        ref: 'v0.10.0'
        commit: 'sha1-e83874834305fe9a4a2997156cb26c5de65a8555'
        owner_id: 135788
        repo_id: 208510314
exit=0
```

The repository's workflow test module with the lockfile and the rewritten workflows present.

```text
$ uv run --no-project --with pyyaml python -m unittest tests.unit.test_workflow_security
.....F..........
======================================================================
FAIL: test_external_actions_use_full_commit_shas (tests.unit.test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/tmp/dotfiles-wt/U115/tests/unit/test_workflow_security.py", line 145, in test_external_actions_use_full_commit_shas
    self.assertEqual([], mutable)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
AssertionError: Lists differ: [] != ['agent-assets.yml:34: actions/checkout@v7[1210 chars]3.0']

Second list contains 27 additional elements.
First extra element 0:
'agent-assets.yml:34: actions/checkout@v7.0.1'

Diff is 1343 characters long. Set self.maxDiff to None to see it.

----------------------------------------------------------------------
Ran 16 tests in 0.238s

FAILED (failures=1)
exit=1
```

The revert, as SCOPE prescribes.

```text
$ git checkout -- .github/workflows
exit=0
```

```text
$ git clean -f -- .github/workflows/actions.lock
Removing .github/workflows/actions.lock
exit=0
```

The tree after the revert: clean.

```text
$ git status --porcelain
exit=0
```

The Actions permissions endpoint the how-to's IMPORTANT note is about.

```text
$ perl -e alarm 120; exec @ARGV gh api repos/mryfmo/dotfiles/actions/permissions
{"message":"You must have repository read permissions or have the repository Actions policies fine-grained permission.","documentation_url":"https://docs.github.com/rest/actions/permissions#get-github-actions-permissions-for-a-repository","status":"403"}gh: You must have repository read permissions or have the repository Actions policies fine-grained permission. (HTTP 403)
exit=1
```

### Dependabot reads, read-only

```text
$ N gh pr view 548 --json number,title,state,createdAt,headRefName,baseRefName,mergeable,files,statusCheckRollup,body
{"baseRefName":"main","body":"Bumps the minor-and-patch group with 1 update in the / directory: [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv).\n\nUpdates `astral-sh/setup-uv` from 10.2.0 to 10.3.2\n<details>\n<summary>Release notes</summary>\n<p><em>Sourced from <a href=\"https://github.com/astral-sh/setup-uv/releases\">astral-sh/setup-uv's releases</a>.</em></p>\n<blockquote>\n<h2>v10.3.2 🌈 update known checksums for 0.13.5</h2>\n<h2>Changes</h2>\n<h2>🧰 Maintenance</h2>\n<ul>\n<li>chore: update known checksums for 0.13.5 @<a href=\"https://github.com/apps/github-actions\">github-actions[bot]</a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1103\">#1103</a>)</li>\n</ul>\n<h2>📚 Documentation</h2>\n<ul>\n<li>docs: update version references to v10.3.1 @<a href=\"https://github.com/apps/github-actions\">github-actions[bot]</a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1102\">#1102</a>)</li>\n</ul>\n<h2>v10.3.1 🌈 preserve cache error class names in save-cache bundle</h2>\n<h2>Changes</h2>\n<p>This release includes a fix so that multiple concurrent workflows trying to upload the same cache no longer warn</p>\n<p><code>##[warning]Failed to save: Unable to reserve cache with key ..., another job may be creating this cache.</code></p>\n<h2>🐛 Bug fixes</h2>\n<ul>\n<li>fix: preserve cache error class names in save-cache bundle <a href=\"https://github.com/dannyward630\"><code>@​dannyward630</code></a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1093\">#1093</a>)</li>\n</ul>\n<h2>🧰 Maintenance</h2>\n<ul>\n<li>chore: update known checksums for 0.13.4 @<a href=\"https://github.com/apps/github-actions\">github-actions[bot]</a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1099\">#1099</a>)</li>\n<li>chore: update known checksums for 0.13.2/0.13.3 @<a href=\"https://github.com/apps/github-actions\">github-actions[bot]</a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1098\">#1098</a>)</li>\n<li>chore: update known checksums for 0.13.1 @<a href=\"https://github.com/apps/github-actions\">github-actions[bot]</a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1094\">#1094</a>)</li>\n<li>Verify npm dependency signatures before builds <a href=\"https://github.com/zaniebot\"><code>@​zaniebot</code></a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1027\">#1027</a>)</li>\n</ul>\n<h2>📚 Documentation</h2>\n<ul>\n<li>docs: cache-dependency-glob matches relative to the working directory <a href=\"https://github.com/flange-ipb\"><code>@​flange-ipb</code></a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1092\">#1092</a>)</li>\n<li>docs: update version references to v10.3.0 @<a href=\"https://github.com/apps/github-actions\">github-actions[bot]</a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1090\">#1090</a>)</li>\n</ul>\n<h2>⬆️ Dependency updates</h2>\n<ul>\n<li>chore(deps): roll up Dependabot updates <a href=\"https://github.com/eifinger\"><code>@​eifinger</code></a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1101\">#1101</a>)</li>\n</ul>\n<h2>v10.3.0 🌈 Add Python architecture selection</h2>\n<h2>Changes</h2>\n<p>This release adds the <code>python-arch</code> input to select a Python architecture independently of the Python version. With <code>uv</code> 0.13.0 or later, set <code>python-arch: x86_64</code> to use x64 Python on Windows ARM64 runners.</p>\n<p>It also includes embedded checksums for <code>uv</code> releases through 0.13.0.</p>\n<ul>\n<li>Use macOS 15 runners for tests <a href=\"https://github.com/charliermarsh\"><code>@​charliermarsh</code></a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1081\">#1081</a>)</li>\n</ul>\n<h2>🚀 Enhancements</h2>\n<ul>\n<li>Add <code>python-arch</code> support <a href=\"https://github.com/zanieb\"><code>@​zanieb</code></a> (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1079\">#1079</a>)</li>\n</ul>\n<!-- raw HTML omitted -->\n</blockquote>\n<p>... (truncated)</p>\n</details>\n<details>\n<summary>Commits</summary>\n<ul>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/07a047e608db84b3d8c06cd9a7c7dcc9c355c18e\"><code>07a047e</code></a> chore: update known checksums for 0.13.5 (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1103\">#1103</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/e1b85369e72750369c935b004eccf97311bdf5dc\"><code>e1b8536</code></a> docs: update version references to v10.3.1 (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1102\">#1102</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/18d369b23da25a81e9458561248e1aafff6a70fa\"><code>18d369b</code></a> chore(deps): roll up Dependabot updates (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1101\">#1101</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/4ad2329c1e377d882fcae221cd1d17e7c0ad788e\"><code>4ad2329</code></a> chore: update known checksums for 0.13.4 (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1099\">#1099</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/4bc6759c82322ff7efa28de54a45404ca6869912\"><code>4bc6759</code></a> chore: update known checksums for 0.13.2/0.13.3 (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1098\">#1098</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/c97f06e356bcca1b426f396ef93ec35ce149ce7b\"><code>c97f06e</code></a> fix: preserve cache error class names in save-cache bundle (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1093\">#1093</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/8ca4be000bfa5f8e6aaa01d8470878c90aa728d3\"><code>8ca4be0</code></a> chore: update known checksums for 0.13.1 (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1094\">#1094</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/b627d85691ead579b598a36169571b1c7123526f\"><code>b627d85</code></a> docs: cache-dependency-glob matches relative to the working directory (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1092\">#1092</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/f8c88970fcd8fff8e97bc62edc5f5c073a0527fe\"><code>f8c8897</code></a> Verify npm dependency signatures before builds (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1027\">#1027</a>)</li>\n<li><a href=\"https://github.com/astral-sh/setup-uv/commit/f64d32b1cd6cc11405a74665b3dfb7bb86fea9f0\"><code>f64d32b</code></a> docs: update version references to v10.3.0 (<a href=\"https://redirect.github.com/astral-sh/setup-uv/issues/1090\">#1090</a>)</li>\n<li>Additional commits viewable in <a href=\"https://github.com/astral-sh/setup-uv/compare/c18668ad3cf93ea998bef934396af7bb5c839dc7...07a047e608db84b3d8c06cd9a7c7dcc9c355c18e\">compare view</a></li>\n</ul>\n</details>\n<br />\n","createdAt":"2026-10-25T10:18:00Z","files":[{"path":".github/workflows/agent-assets.yml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/docs-check.yml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/docs.yml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/drift-watch.yml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/regime.yml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/test.yaml","additions":1,"deletions":1,"changeType":"MODIFIED"}],"headRefName":"dependabot/github_actions/minor-and-patch-d7d93b8548","mergeable":"MERGEABLE","number":548,"state":"OPEN","statusCheckRollup":[{"__typename":"CheckRun","completedAt":"2026-10-26T01:41:14Z","conclusion":"FAILURE","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254987990/job/121354803430","name":"test (ubuntu-24.04, client)","startedAt":"2026-10-26T01:35:52Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:36:19Z","conclusion":"FAILURE","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254986021/job/121354852838","name":"regime","startedAt":"2026-10-26T01:36:04Z","status":"COMPLETED","workflowName":"regime"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:36:14Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254988051/job/121354803529","name":"validate","startedAt":"2026-10-26T01:35:52Z","status":"COMPLETED","workflowName":"Agent assets"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:36:28Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254987985/job/121354803220","name":"apply-container","startedAt":"2026-10-26T01:35:51Z","status":"COMPLETED","workflowName":"Apply check"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:36:39Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254988056/job/121354803581","name":"build","startedAt":"2026-10-26T01:35:52Z","status":"COMPLETED","workflowName":"Docs build"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:36:02Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254988030/job/121354803638","name":"public-bootstrap (ubuntu-24.04, client)","startedAt":"2026-10-26T01:35:52Z","status":"COMPLETED","workflowName":"Snippet install"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:39:58Z","conclusion":"FAILURE","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254987990/job/121354803252","name":"test (ubuntu-24.04, server)","startedAt":"2026-10-26T01:35:52Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:36:01Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254988030/job/121354803595","name":"public-bootstrap (ubuntu-24.04, server)","startedAt":"2026-10-26T01:35:51Z","status":"COMPLETED","workflowName":"Snippet install"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:44:52Z","conclusion":"FAILURE","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254987990/job/121354803404","name":"test (macos-15, client)","startedAt":"2026-10-26T01:35:53Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:36:09Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254988030/job/121354803502","name":"public-bootstrap (macos-15, client)","startedAt":"2026-10-26T01:35:53Z","status":"COMPLETED","workflowName":"Snippet install"},{"__typename":"CheckRun","completedAt":"2026-10-26T01:39:49Z","conclusion":"FAILURE","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40254987990/job/121354803442","name":"test (ubuntu-26.04, client)","startedAt":"2026-10-26T01:35:51Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"StatusContext","context":"CodeRabbit","startedAt":"2026-10-26T01:35:54Z","state":"SUCCESS","targetUrl":""},{"__typename":"CheckRun","completedAt":"2026-10-26T01:35:48Z","conclusion":"SUCCESS","detailsUrl":"https://dashboard.gitguardian.com","name":"GitGuardian Security Checks","startedAt":"2026-10-26T01:35:47Z","status":"COMPLETED","workflowName":""}],"title":"chore(deps): bump astral-sh/setup-uv from 10.2.0 to 10.3.2 in the minor-and-patch group across 1 directory"}
exit=0
```

```text
$ N gh pr view 549 --json number,title,state,createdAt,headRefName,baseRefName,mergeable,files,statusCheckRollup,body
{"baseRefName":"main","body":"Bumps [jdx/mise-action](https://github.com/jdx/mise-action) from 4.3.0 to 5.2.2.\n<details>\n<summary>Release notes</summary>\n<p><em>Sourced from <a href=\"https://github.com/jdx/mise-action/releases\">jdx/mise-action's releases</a>.</em></p>\n<blockquote>\n<h2>v5.2.2: Include conf.d config fragments in the cache key</h2>\n<p>The cache key now includes mise <code>conf.d/*.toml</code> config fragments, so changing one of them invalidates the cache.</p>\n<h2>Fixed</h2>\n<ul>\n<li><strong>Editing a <code>conf.d</code> fragment now invalidates the cache.</strong> mise can load config from single-file fragments in <code>conf.d/</code> directories, but the action didn't hash those files when it built the cache key. As a result, adding or changing tools in a fragment could restore an outdated cache. The cache key now also hashes <code>conf.d/*.toml</code> files under <code>.config/mise/</code>, <code>.mise/</code> and <code>mise/</code>. If your repo already uses these fragments, the cache will miss once after you upgrade. (<a href=\"https://redirect.github.com/jdx/mise-action/pull/698\">#698</a> by <a href=\"https://github.com/rileymichael\"><code>@​rileymichael</code></a>)</li>\n</ul>\n<h2>New Contributors</h2>\n<ul>\n<li><a href=\"https://github.com/rileymichael\"><code>@​rileymichael</code></a> made their first contribution in <a href=\"https://redirect.github.com/jdx/mise-action/pull/698\">#698</a></li>\n</ul>\n<p><strong>Full Changelog</strong>: <a href=\"https://github.com/jdx/mise-action/compare/v5.2.1...v5.2.2\">https://github.com/jdx/mise-action/compare/v5.2.1...v5.2.2</a></p>\n<h2>v5.2.1: Require the signed packslip for mise 2026.9.3 and later</h2>\n<p>The action now refuses to install mise 2026.9.3 or later if the release's signed packslip is missing. This closes a gap where verification could be downgraded to the weaker checksum check.</p>\n<h2>Fixed</h2>\n<ul>\n<li><strong>A missing packslip no longer weakens the check on recent mise releases.</strong> v5.2.0 started checking the mise binary against the release's signed <code>packslip.sigstore.json</code>. If that file wasn't found, though, the action quietly fell back to the minisign-signed <code>SHASUMS256</code> checksums. Anyone who could hide the file could force the weaker check. Every mise release from 2026.9.3 on includes a packslip, so for those versions a missing bundle now stops the install with an error like this:\n<pre><code>mise v2026.10.11 must ship a signed packslip, but https://github.com/jdx/mise/releases/download/v2026.10.11/packslip.sigstore.json was not found\n</code></pre>\nReleases before 2026.9.3 don't include a packslip, so they're still checked against the signed checksums. A version string that isn't three dot-separated numbers also requires a packslip. If you set the <code>sha256</code> input, it still takes precedence over both checks. A packslip that fails verification still never falls back to the checksums. (<a href=\"https://redirect.github.com/jdx/mise-action/pull/695\">#695</a> by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a>)</li>\n</ul>\n<p><strong>Full Changelog</strong>: <a href=\"https://github.com/jdx/mise-action/compare/v5.2.0...v5.2.1\">https://github.com/jdx/mise-action/compare/v5.2.0...v5.2.1</a></p>\n<h2>v5.2.0: Periodic cache rebuilds, signed packslip verification, and monorepo installs</h2>\n<p>The default cache key now rolls over every 30 days, so long-lived caches pick up newer mise releases. The action also checks the downloaded mise binary against the release's signed packslip, and it runs <code>mise install --monorepo</code> automatically in monorepos. <strong>Existing caches miss once after you upgrade</strong>, because the default cache key format has changed.</p>\n<h2>Added</h2>\n<ul>\n<li><strong>The cache is rebuilt every 30 days by default.</strong> GitHub never evicts a cache that keeps getting hits. Before this release, an active repo could keep the same mise binary and tools for months, until a config file changed. The default cache key now includes a period suffix (<code>-p&lt;N&gt;</code>), so the cache is rebuilt from scratch at least once per period. All repos roll over on the same calendar boundary. Use the new <code>cache_max_age_days</code> input to change the period, or set it to <code>0</code> to keep the old key that never expires. Custom <code>cache_key</code> templates can use the new <code>{{cache_period}}</code> variable, which <code>{{default}}</code> already includes. A custom key that doesn't use it behaves as before. On self-hosted runners that keep mise data between runs, you may also need <code>auto_update: true</code> to pick up a newer mise. (<a href=\"https://redirect.github.com/jdx/mise-action/pull/689\">#689</a> by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a>, fixes <a href=\"https://redirect.github.com/jdx/mise-action/issues/688\">#688</a>)\n<pre lang=\"yaml\"><code>- uses: jdx/mise-action@v5\n  with:\n    cache_max_age_days: 14 # default 30; 0 disables periodic rebuilds\n</code></pre>\n</li>\n<li><strong>Throttled cache restores and saves can be retried.</strong> Before this release, when GitHub's cache service returned HTTP 429, the action gave up right away: a restore counted as a miss and a save was skipped. The new <code>cache_restore_retry_budget</code> and <code>cache_save_retry_budget</code> inputs set how long the action may wait. Each retry waits for the <code>Retry-After</code> value plus some random jitter. Once the budget runs out, the action falls back to the old behavior. Retries apply to the main cache, the post-step save and the binary cache. Real cache misses and reservation conflicts are never retried. Both budgets default to <code>0s</code> (no retries). <code>@actions/cache</code> doesn't report 429 errors directly, so the action detects throttling from its warning messages. If those messages change in a future <code>@actions/cache</code> release, throttling won't be detected and nothing will be retried. (<a href=\"https://redirect.github.com/jdx/mise-action/pull/692\">#692</a> by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a>, fixes <a href=\"https://redirect.github.com/jdx/mise-action/issues/691\">#691</a>)\n<pre lang=\"yaml\"><code>- uses: jdx/mise-action@v5\n  with:\n    cache_restore_retry_budget: 60s\n    cache_save_retry_budget: 120s\n</code></pre>\n</li>\n<li><strong>The latest mise binary can fall back to a second download source.</strong> When the action downloads the latest mise version, it can fall back between GitHub and mise.jdx.dev if the first source fails. The <code>fetch_from_github</code> setting decides which source it tries first. Pinned versions and <code>minimum_release_age</code> installs are only downloaded from GitHub. The binary is still checked against the signed checksums for the resolved version, whichever source it came from. (<a href=\"https://redirect.github.com/jdx/mise-action/pull/692\">#692</a> by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a>)</li>\n<li><strong>The mise binary is checked against its signed packslip.</strong> If a mise release includes <code>packslip.sigstore.json</code>, the action checks the downloaded binary against it. The bundle must be signed by mise's release workflow for that exact tag. After a successful check, the log shows <code>Verified &lt;asset&gt; against the signed packslip</code>. If the check fails, the install stops instead of falling back to a weaker check. Releases without a packslip use the existing minisign and <code>SHASUMS256</code> check. An explicit <code>sha256</code> input still takes precedence. (<a href=\"https://redirect.github.com/jdx/mise-action/pull/693\">#693</a> by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a>)</li>\n<li><strong>Monorepo-aware installs.</strong> If your mise config sets <code>[monorepo].config_roots</code>, the action now adds <code>--monorepo</code> to <code>mise install</code>, so tools configured anywhere in the monorepo get installed. Repos without that setting aren't affected. To opt out, set <code>monorepo: false</code>. (<a href=\"https://redirect.github.com/jdx/mise-action/pull/679\">#679</a> by <a href=\"https://github.com/zeitlinger\"><code>@​zeitlinger</code></a>)</li>\n</ul>\n<h2>Fixed</h2>\n<!-- raw HTML omitted -->\n</blockquote>\n<p>... (truncated)</p>\n</details>\n<details>\n<summary>Changelog</summary>\n<p><em>Sourced from <a href=\"https://github.com/jdx/mise-action/blob/main/CHANGELOG.md\">jdx/mise-action's changelog</a>.</em></p>\n<blockquote>\n<h1>Changelog</h1>\n<hr />\n<h2><a href=\"https://github.com/jdx/mise-action/compare/v5.2.2..v5.2.3\">5.2.3</a> - 2026-10-23</h2>\n<h3>🐛 Bug Fixes</h3>\n<ul>\n<li><strong>(cache)</strong> hash mise config files without walking the workspace (<a href=\"https://redirect.github.com/jdx/mise-action/issues/703\">#703</a>) by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/703\">#703</a></li>\n</ul>\n<hr />\n<h2><a href=\"https://github.com/jdx/mise-action/compare/v5.2.1..v5.2.2\">5.2.2</a> - 2026-10-21</h2>\n<h3>🐛 Bug Fixes</h3>\n<ul>\n<li>hash conf.d config fragments in cache key (<a href=\"https://redirect.github.com/jdx/mise-action/issues/698\">#698</a>) by <a href=\"https://github.com/rileymichael\"><code>@​rileymichael</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/698\">#698</a></li>\n</ul>\n<h3>New Contributors</h3>\n<ul>\n<li><a href=\"https://github.com/rileymichael\"><code>@​rileymichael</code></a> made their first contribution in <a href=\"https://redirect.github.com/jdx/mise-action/pull/698\">#698</a></li>\n</ul>\n<hr />\n<h2><a href=\"https://github.com/jdx/mise-action/compare/v5.2.0..v5.2.1\">5.2.1</a> - 2026-10-19</h2>\n<h3>🐛 Bug Fixes</h3>\n<ul>\n<li>require the signed packslip for mise 2026.9.3 and later (<a href=\"https://redirect.github.com/jdx/mise-action/issues/695\">#695</a>) by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/695\">#695</a></li>\n</ul>\n<hr />\n<h2><a href=\"https://github.com/jdx/mise-action/compare/v5.1.2..v5.2.0\">5.2.0</a> - 2026-10-16</h2>\n<h3>🚀 Features</h3>\n<ul>\n<li><strong>(cache)</strong> rebuild the cache every 30 days by default (<a href=\"https://redirect.github.com/jdx/mise-action/issues/689\">#689</a>) by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/689\">#689</a></li>\n<li><strong>(cache)</strong> retry throttled cache restores and saves (<a href=\"https://redirect.github.com/jdx/mise-action/issues/692\">#692</a>) by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/692\">#692</a></li>\n<li>verify the mise binary against its signed packslip (<a href=\"https://redirect.github.com/jdx/mise-action/issues/693\">#693</a>) by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/693\">#693</a></li>\n</ul>\n<h3>🐛 Bug Fixes</h3>\n<ul>\n<li>export the PATH entries mise reports with mise env --paths (<a href=\"https://redirect.github.com/jdx/mise-action/issues/685\">#685</a>) by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/685\">#685</a></li>\n</ul>\n<h3>🔍 Other Changes</h3>\n<ul>\n<li>Use monorepo install when configured (<a href=\"https://redirect.github.com/jdx/mise-action/issues/679\">#679</a>) by <a href=\"https://github.com/zeitlinger\"><code>@​zeitlinger</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/679\">#679</a></li>\n<li>Change minimum age for auto-merging release PRs by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a> in <a href=\"https://github.com/jdx/mise-action/commit/b511e8dec14aeeaeeac996371d336fcc5d0a6bed\">b511e8d</a></li>\n</ul>\n<h3>📚 Documentation</h3>\n<ul>\n<li>tell release workflows not to use the cache (<a href=\"https://redirect.github.com/jdx/mise-action/issues/682\">#682</a>) by <a href=\"https://github.com/jdx\"><code>@​jdx</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/682\">#682</a></li>\n<li>explain caching mise downloads instead of installs (<a href=\"https://redirect.github.com/jdx/mise-action/issues/686\">#686</a>) by <a href=\"https://github.com/zeitlinger\"><code>@​zeitlinger</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/686\">#686</a></li>\n<li>use resolved Windows downloads cache path (<a href=\"https://redirect.github.com/jdx/mise-action/issues/690\">#690</a>) by <a href=\"https://github.com/zeitlinger\"><code>@​zeitlinger</code></a> in <a href=\"https://redirect.github.com/jdx/mise-action/pull/690\">#690</a></li>\n</ul>\n<!-- raw HTML omitted -->\n</blockquote>\n<p>... (truncated)</p>\n</details>\n<details>\n<summary>Commits</summary>\n<ul>\n<li><a href=\"https://github.com/jdx/mise-action/commit/8418fedb1110381a0d3ba51a7a415d7c1b884550\"><code>8418fed</code></a> chore: release v5.2.2 (<a href=\"https://redirect.github.com/jdx/mise-action/issues/699\">#699</a>)</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/bb33e9b1d04daa1d198342413fd3702ef2d1de98\"><code>bb33e9b</code></a> chore(deps): update communique, hk in mise.lock (<a href=\"https://redirect.github.com/jdx/mise-action/issues/700\">#700</a>)</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/0cc9f843d6d05e847c460bf6b36b9f7c7c04727a\"><code>0cc9f84</code></a> fix: hash conf.d config fragments in cache key (<a href=\"https://redirect.github.com/jdx/mise-action/issues/698\">#698</a>)</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/7ce9a0247dc5311b87936f6190a78320299230ef\"><code>7ce9a02</code></a> chore(deps): lock file maintenance (<a href=\"https://redirect.github.com/jdx/mise-action/issues/697\">#697</a>)</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/fc42bcc7ddbf51124c30f95a877a0c5168a3bfde\"><code>fc42bcc</code></a> chore: release v5.2.1 (<a href=\"https://redirect.github.com/jdx/mise-action/issues/696\">#696</a>)</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/720e96afaf7f84d94fc5ff7d76cbee788fa20eed\"><code>720e96a</code></a> fix: require the signed packslip for mise 2026.9.3 and later (<a href=\"https://redirect.github.com/jdx/mise-action/issues/695\">#695</a>)</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/9b200bcecbfd6303e69a4a261b2e09e3757440a7\"><code>9b200bc</code></a> chore: release v5.2.0 (<a href=\"https://redirect.github.com/jdx/mise-action/issues/680\">#680</a>)</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/b511e8dec14aeeaeeac996371d336fcc5d0a6bed\"><code>b511e8d</code></a> Change minimum age for auto-merging release PRs</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/887d1f43266da23235f0fb82165ac68fcac39839\"><code>887d1f4</code></a> docs: use resolved Windows downloads cache path (<a href=\"https://redirect.github.com/jdx/mise-action/issues/690\">#690</a>)</li>\n<li><a href=\"https://github.com/jdx/mise-action/commit/93c62ad75cd417c639763e02ab55eda7edb57426\"><code>93c62ad</code></a> chore: replace prettier with oxfmt (<a href=\"https://redirect.github.com/jdx/mise-action/issues/694\">#694</a>)</li>\n<li>Additional commits viewable in <a href=\"https://github.com/jdx/mise-action/compare/c2a87611a18de5b3828c5652fe268e992400cb5c...8418fedb1110381a0d3ba51a7a415d7c1b884550\">compare view</a></li>\n</ul>\n</details>\n<br />\n\n\n[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=jdx/mise-action&package-manager=github_actions&previous-version=4.3.0&new-version=5.2.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)\n\nDependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.\n\n[//]: # (dependabot-automerge-start)\n[//]: # (dependabot-automerge-end)\n\n---\n\n<details>\n<summary>Dependabot commands and options</summary>\n<br />\n\nYou can trigger Dependabot actions by commenting on this PR:\n- `@dependabot rebase` will rebase this PR\n- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it\n- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency\n- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)\n- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)\n- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)\n\n\n</details>","createdAt":"2026-10-25T10:18:16Z","files":[{"path":".github/workflows/docs-check.yml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/docs.yml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/macos.yaml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/test.yaml","additions":1,"deletions":1,"changeType":"MODIFIED"},{"path":".github/workflows/ubuntu.yaml","additions":1,"deletions":1,"changeType":"MODIFIED"}],"headRefName":"dependabot/github_actions/jdx/mise-action-5.2.2","mergeable":"MERGEABLE","number":549,"state":"OPEN","statusCheckRollup":[{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:38Z","conclusion":"FAILURE","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184217051/job/121141464842","name":"regime","startedAt":"2026-10-25T10:18:22Z","status":"COMPLETED","workflowName":"regime"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:32Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218871/job/121141469788","name":"validate","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"Agent assets"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:48Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218889/job/121141470007","name":"build","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"Docs build"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:26Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218893/job/121141469757","name":"secrets","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"MacOS"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:35Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218883/job/121141469765","name":"public-bootstrap (ubuntu-24.04, client)","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"Snippet install"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:25Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218890/job/121141469815","name":"secrets","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"Ubuntu"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:24:00Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218908/job/121141470234","name":"test (ubuntu-24.04, client)","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:33Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218883/job/121141470069","name":"public-bootstrap (ubuntu-24.04, server)","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"Snippet install"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:21:08Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218908/job/121141470355","name":"test (ubuntu-24.04, server)","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:29:03Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218883/job/121141469991","name":"public-bootstrap (macos-14, client)","startedAt":"2026-10-25T10:28:49Z","status":"COMPLETED","workflowName":"Snippet install"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:33:38Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218908/job/121141470163","name":"test (macos-14, client)","startedAt":"2026-10-25T10:29:54Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:27:12Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218883/job/121141470124","name":"public-bootstrap (macos-15, client)","startedAt":"2026-10-25T10:27:00Z","status":"COMPLETED","workflowName":"Snippet install"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:46:32Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218908/job/121141470322","name":"test (macos-15, client)","startedAt":"2026-10-25T10:41:04Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:23:29Z","conclusion":"SUCCESS","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218908/job/121141470238","name":"test (ubuntu-26.04, client)","startedAt":"2026-10-25T10:18:23Z","status":"COMPLETED","workflowName":"Unit test"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:26Z","conclusion":"SKIPPED","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218893/job/121141487155","name":"build","startedAt":"2026-10-25T10:18:26Z","status":"COMPLETED","workflowName":"MacOS"},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:25Z","conclusion":"SKIPPED","detailsUrl":"https://github.com/mryfmo/dotfiles/actions/runs/40184218890/job/121141485617","name":"build","startedAt":"2026-10-25T10:18:26Z","status":"COMPLETED","workflowName":"Ubuntu"},{"__typename":"StatusContext","context":"CodeRabbit","startedAt":"2026-10-25T10:18:25Z","state":"SUCCESS","targetUrl":""},{"__typename":"CheckRun","completedAt":"2026-10-25T10:18:21Z","conclusion":"SUCCESS","detailsUrl":"https://dashboard.gitguardian.com","name":"GitGuardian Security Checks","startedAt":"2026-10-25T10:18:20Z","status":"COMPLETED","workflowName":""}],"title":"chore(deps): bump jdx/mise-action from 4.3.0 to 5.2.2"}
exit=0
```

```text
$ N gh pr diff 548
diff --git a/.github/workflows/agent-assets.yml b/.github/workflows/agent-assets.yml
index 46abec31b..2474c3fef 100644
--- a/.github/workflows/agent-assets.yml
+++ b/.github/workflows/agent-assets.yml
@@ -36,7 +36,7 @@ jobs:
           persist-credentials: false

       - name: Setup uv
-        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+        uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
         with:
           enable-cache: false

diff --git a/.github/workflows/docs-check.yml b/.github/workflows/docs-check.yml
index 3a970b127..acee9c3d8 100644
--- a/.github/workflows/docs-check.yml
+++ b/.github/workflows/docs-check.yml
@@ -43,7 +43,7 @@ jobs:
           persist-credentials: false

       - name: Setup uv
-        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+        uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
         with:
           enable-cache: false

diff --git a/.github/workflows/docs.yml b/.github/workflows/docs.yml
index 4ddf30057..6332b20f8 100644
--- a/.github/workflows/docs.yml
+++ b/.github/workflows/docs.yml
@@ -42,7 +42,7 @@ jobs:
           persist-credentials: false

       - name: Setup uv
-        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+        uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
         with:
           enable-cache: false

diff --git a/.github/workflows/drift-watch.yml b/.github/workflows/drift-watch.yml
index a261909fa..2e64defd6 100644
--- a/.github/workflows/drift-watch.yml
+++ b/.github/workflows/drift-watch.yml
@@ -28,7 +28,7 @@ jobs:
       - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
         with:
           persist-credentials: false
-      - uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+      - uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
         with:
           enable-cache: false
       - name: Run the drift watch
diff --git a/.github/workflows/regime.yml b/.github/workflows/regime.yml
index e07f5e9a9..0819d241f 100644
--- a/.github/workflows/regime.yml
+++ b/.github/workflows/regime.yml
@@ -31,7 +31,7 @@ jobs:
           # head's fork point, from before this verifier; ci:39185982423:1). The pull request cannot move this branch.
           ref: refs/heads/${{ github.base_ref }}
           persist-credentials: false
-      - uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+      - uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
         with:
           enable-cache: false
       - name: Fetch the pull request's head as data
diff --git a/.github/workflows/test.yaml b/.github/workflows/test.yaml
index cdb715537..c2ceaf2d8 100644
--- a/.github/workflows/test.yaml
+++ b/.github/workflows/test.yaml
@@ -427,7 +427,7 @@ jobs:

       - name: Setup uv
         if: ${{ steps.decide.outputs.should_test == 'true' }}
-        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
+        uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
         with:
           enable-cache: false

exit=0
```

```text
$ N gh pr diff 549
diff --git a/.github/workflows/docs-check.yml b/.github/workflows/docs-check.yml
index 3a970b127..7a2d92fcb 100644
--- a/.github/workflows/docs-check.yml
+++ b/.github/workflows/docs-check.yml
@@ -48,7 +48,7 @@ jobs:
           enable-cache: false

       - name: Setup mise
-        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+        uses: jdx/mise-action@8418fedb1110381a0d3ba51a7a415d7c1b884550 # v5.2.2
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
diff --git a/.github/workflows/docs.yml b/.github/workflows/docs.yml
index d154ccc84..ecd330059 100644
--- a/.github/workflows/docs.yml
+++ b/.github/workflows/docs.yml
@@ -46,7 +46,7 @@ jobs:
           enable-cache: false

       - name: Setup mise
-        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+        uses: jdx/mise-action@8418fedb1110381a0d3ba51a7a415d7c1b884550 # v5.2.2
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
diff --git a/.github/workflows/macos.yaml b/.github/workflows/macos.yaml
index 4a640ae02..c5d90a6e5 100644
--- a/.github/workflows/macos.yaml
+++ b/.github/workflows/macos.yaml
@@ -157,7 +157,7 @@ jobs:
           alert-comment-cc-users: "@mryfmo"
           benchmark-data-dir-path: "."

-      - uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+      - uses: jdx/mise-action@8418fedb1110381a0d3ba51a7a415d7c1b884550 # v5.2.2
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
diff --git a/.github/workflows/test.yaml b/.github/workflows/test.yaml
index 2313c67f7..d041ef426 100644
--- a/.github/workflows/test.yaml
+++ b/.github/workflows/test.yaml
@@ -256,7 +256,7 @@ jobs:

       - name: Setup mise for statusline smoke
         if: ${{ steps.decide.outputs.should_test == 'true' }}
-        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+        uses: jdx/mise-action@8418fedb1110381a0d3ba51a7a415d7c1b884550 # v5.2.2
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
diff --git a/.github/workflows/ubuntu.yaml b/.github/workflows/ubuntu.yaml
index 5a6da5f5a..ccb9ba782 100644
--- a/.github/workflows/ubuntu.yaml
+++ b/.github/workflows/ubuntu.yaml
@@ -115,7 +115,7 @@ jobs:
           after_local_change="$(cksum "${HOME}/.zprofile")"
           [ "${after_local_change}" = "${before_local_change}" ]

-      - uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
+      - uses: jdx/mise-action@8418fedb1110381a0d3ba51a7a415d7c1b884550 # v5.2.2
         with:
           # The newest mise at least 72 hours old, as hosts get it (minimum_release_age).
           minimum_release_age: 72h
exit=0
```

The commit each tag points at in the action's own repository.

```text
$ N gh api repos/astral-sh/setup-uv/commits/v10.3.2 --jq .sha
07a047e608db84b3d8c06cd9a7c7dcc9c355c18e
exit=0
```

```text
$ N gh api repos/jdx/mise-action/commits/v5.2.2 --jq .sha
8418fedb1110381a0d3ba51a7a415d7c1b884550
exit=0
```

The release dates.

```text
$ N gh api repos/astral-sh/setup-uv/releases/tags/v10.3.2 --jq .published_at
2026-10-22T08:47:11Z
exit=0
```

```text
$ N gh api repos/jdx/mise-action/releases/tags/v5.2.2 --jq .published_at
2026-10-21T10:06:03Z
exit=0
```

Reads beyond the brief's list, taken because the PR body truncates the v5 release notes: the mise-action release list and the two notes the body cuts.

```text
$ N gh api repos/jdx/mise-action/releases?per_page=40 --jq .[] | [.tag_name, .published_at] | @tsv
v5.2.4	2026-10-27T10:06:24Z
v5.2.3	2026-10-24T10:05:40Z
v5.2.2	2026-10-21T10:06:03Z
v5.2.1	2026-10-19T10:05:53Z
v5.2.0	2026-10-16T11:27:18Z
v5.1.2	2026-10-12T10:12:40Z
v5.1.1	2026-10-04T15:41:50Z
v5.1.0	2026-10-04T01:05:24Z
v5.0.1	2026-09-30T22:37:15Z
v5.0.0	2026-09-28T19:34:33Z
v4.3.0	2026-08-25T10:08:22Z
v4.2.5	2026-08-13T10:23:24Z
v4.2.4	2026-08-01T10:32:01Z
v4.2.3	2026-07-24T18:57:59Z
v4.2.2	2026-07-24T10:40:22Z
v4.2.1	2026-07-16T18:18:20Z
v4.2.0	2026-06-17T18:29:05Z
v4.1.0	2026-06-04T17:08:23Z
v4.0.1	2026-03-22T16:06:57Z
v4.0.0	2026-03-13T11:16:19Z
v3.6.3	2026-03-06T16:15:05Z
v3.6.2	2026-03-02T09:46:11Z
v3.6.1	2026-01-20T12:33:13Z
v3.6.0	2026-01-18T19:58:40Z
v3.5.1	2025-11-24T12:04:35Z
v3.5.0	2025-11-21T10:42:57Z
v3.4.1	2025-11-13T10:54:00Z
v3.4.0	2025-10-31T15:44:18Z
v3.3.1	2025-10-06T11:22:00Z
v3.3.0	2025-10-03T11:56:47Z
v3.2.0	2025-08-22T14:42:44Z
v3.1.0	2025-08-19T16:04:29Z
v3.0.2	2025-08-18T16:59:08Z
v3.0.1	2025-08-18T16:55:53Z
v3.0.0	2025-08-18T16:35:00Z
v2.4.4	2025-07-27T19:01:49Z
v2.4.3	2025-07-27T18:49:05Z
v2.4.2	2025-07-24T06:13:09Z
v2.4.0	2025-07-12T11:23:55Z
v2.3.1	2025-06-25T16:55:38Z
exit=0
```

````text
 $ N gh api repos/jdx/mise-action/releases/tags/v5.0.0 --jq .body
 If you don't pin a `version`, mise-action now installs the newest stable mise release that is at least 24 hours old. Upgrading mise on a runner that already has it is also less likely to hit GitHub API rate limits.

 ## Breaking Changes

 ### `minimum_release_age` now defaults to `24h` ([#632](https://github.com/jdx/mise-action/pull/632) by @jdx)

 Before this release, `minimum_release_age` was an opt-in setting. It now defaults to `24h`. If you don't set `version`, the action picks the highest-numbered stable mise release published at least 24 hours ago. A mise release that just shipped won't be installed until it's a day old.

 To get the latest stable release right away, as in v4, set the delay to `0s`. You can also choose a longer delay:

 ```yaml
 - uses: jdx/mise-action@v5
   with:
     minimum_release_age: 0s   # or e.g. 7d
 ```

 - An explicit `version` input still takes precedence and skips the delay.
 - The setting applies only to the mise binary, not to tools installed by mise.
 - The action now gets the release list from a public CDN index (`releases.tsv` on mise.jdx.dev) instead of paging through the GitHub Releases API. Picking a release doesn't use GitHub API quota, even when an installed binary is reused. If the index is missing or malformed, the action fails instead of skipping the release-age check.
 - Replacing an older installed binary still runs `mise self-update`, which may call the GitHub API to fetch that exact release.

 ## Fixed

 - `mise self-update` now runs with `MISE_GITHUB_TOKEN`. When a runner already had a different mise version installed, the action runs `mise self-update` to switch versions. That GitHub API call used to go out without authentication, so busy shared or self-hosted runners could hit the rate limit and fail with `HTTP 403 RateLimitedError`. If you already set a token in your environment, the action leaves it unchanged. ([#619](https://github.com/jdx/mise-action/pull/619) by @hegde5)

 ## New Contributors

 * @hegde5 made their first contribution in [#619](https://github.com/jdx/mise-action/pull/619)

 **Full Changelog**: https://github.com/jdx/mise-action/compare/v4.3.0...v5.0.0
 exit=0
````

````text
 $ N gh api repos/jdx/mise-action/releases/tags/v5.1.0 --jq .body
 mise-action now reports the tool versions it installed as step outputs, can install mise plugins before tools, and can save the cache at the end of the job. Several caching fixes stop the action from downloading mise again on every run.

 ## Added

 - **Tool versions as step outputs.** After install, the action runs `mise ls --json --current` and sets a `versions` output. This is a JSON object of the active, installed tools. Each tool maps to a list of `{version, requested_version, install_path, source}` entries. Each tool also gets its own output with its resolved version, such as `steps.mise.outputs.node`. A tool only gets its own output if its name is a valid output name and isn't `cache-hit` or `versions`. Names like `npm:@scope/pkg` appear only in `versions`. If the action can't read the versions, it prints a warning and the step still succeeds. ([#655](https://github.com/jdx/mise-action/pull/655) by @jdx)
   ```yaml
   - uses: jdx/mise-action@v5
     id: mise
   - run: echo "node ${{ steps.mise.outputs.node }}"
   ```
 - **`plugins` input.** List plugins one per line as `name` or `name url`. Blank lines and `#` comments are ignored. The action runs `mise plugins install -y` for each one before `mise install`. Plugins that are already installed, for example restored from the cache, are left as they are. An unknown plugin fails the step. When `plugins` is set, its hash is added to the default cache key. Custom `cache_key` templates can use it as `{{plugins_hash}}`. If `plugins` is unset, existing cache keys don't change. ([#656](https://github.com/jdx/mise-action/pull/656) by @jdx)
   ```yaml
   - uses: jdx/mise-action@v5
     env:
       # needed for idiomatic files such as .yvmrc
       MISE_IDIOMATIC_VERSION_FILE_ENABLE_TOOLS: yarn
     with:
       plugins: |
         yarn
         php https://github.com/verzly/mise-php#latest
   ```
 - **`cache_save_post` input (opt-in, default `false`).** When enabled, the mise cache is saved in the action's post step instead of right after install. This way, tools installed by later steps are included in the cache, for example from monorepo sub-project configs or task-level tools. The setting only applies on a cache miss, because an existing cache entry can't be overwritten. The post step runs even if a later step fails. If the post-step save fails, the action prints a warning and the job doesn't fail. ([#649](https://github.com/jdx/mise-action/pull/649) by @jdx)
 - **`auto_update` input (default `false`).** See Changed below. ([#642](https://github.com/jdx/mise-action/pull/642) by @jdx)
 - The action now warns when you use the `mise_toml` input and a `.mise.toml` already exists in the working directory. mise loads `.mise.toml` before the `mise.toml` the action writes, so the input may have no effect. ([#654](https://github.com/jdx/mise-action/pull/654) by @jdx)

 ## Changed

 - **A cached mise is kept when `version` is unset.** Before, each new mise release made the action reject the cached binary in integrity verification and download mise again on every run until the cache key changed. Now the cached binary is kept until the cache key changes. The action verifies it against the signed checksums of the version recorded at install, without running it first. Caches saved before this release have no version record, so they are still verified against the latest release, and a tampered binary is still replaced. The integrity warning now includes the underlying error. To keep updating to newer releases as before, set `auto_update: true`. Each updated binary is cached under its own mise version, so each release is downloaded only once. An explicit `version` input works the same as before. ([#642](https://github.com/jdx/mise-action/pull/642) by @jdx)

 ## Fixed

 - **The cache is saved after a partial-match restore.** When the cache was restored from a key that only matched the prefix, the action never saved under the primary key, so it rebuilt the same tools on every run. Exact cache hits still skip the save. ([#646](https://github.com/jdx/mise-action/pull/646) by @jdx)
 - **Caches saved before this release no longer cause a download on every run.** These caches have no version record, so a cached binary is verified against the latest release. Once a newer mise shipped, the action downloaded mise again on every run. It now also saves the reinstalled binary in a cache keyed by mise version, so later runs restore that binary instead of downloading it. ([#648](https://github.com/jdx/mise-action/pull/648) by @jdx)
 - **Windows: mise installs without `unzip`.** The mise zip is now extracted with PowerShell's `Expand-Archive`. Self-hosted Windows runners that don't have `unzip`, such as fresh Windows 11 arm64 machines, can now install mise. ([#650](https://github.com/jdx/mise-action/pull/650) by @jdx)

 ## Documentation

 - New README guides cover matrix builds, using another cache action, and Rust caching:
   - Matrix builds: use `MISE_<TOOL>_VERSION` overrides and give each matrix entry its own `cache_key`.
   - Other cache actions: set `cache: false` and cache mise's data directory yourself.
   - Rust: explains why a restored cache can be missing Rust components such as `rustfmt`, with two workarounds. ([#654](https://github.com/jdx/mise-action/pull/654), [#651](https://github.com/jdx/mise-action/pull/651) by @jdx)

 **Full Changelog**: https://github.com/jdx/mise-action/compare/v5.0.1...v5.1.0
 exit=0
````

The failing `Unit test` run on #548's head (run 40254987990 of `test.yaml`, branch `dependabot/github_actions/minor-and-patch-d7d93b8548`, head `84b6f259ec0e1fcca1bd907e8c8140968babebe3`, from `gh run list --branch <branch> --workflow test.yaml`): its jobs and their failed steps. The cause is in the source excerpt under Measured facts.

```text
$ N gh api repos/mryfmo/dotfiles/actions/runs/40254987990/jobs --jq .jobs[] | [.name, .conclusion] | @tsv
test (ubuntu-24.04, server)	failure
test (macos-15, client)	failure
test (ubuntu-24.04, client)	failure
test (ubuntu-26.04, client)	failure
exit=0
```

```text
$ N gh api repos/mryfmo/dotfiles/actions/runs/40254987990/jobs --jq .jobs[] | select(.conclusion=="failure") | .steps[] | select(.conclusion=="failure") | [.name, .conclusion] | @tsv
Run Python unit tests	failure
Run Python unit tests	failure
Run Python unit tests	failure
Run Python unit tests	failure
exit=0
```

The two READMEs quoted below were fetched with `curl -sSfL` from `raw.githubusercontent.com`: `jdx/mise-action/main/README.md` (436 lines, exit 0) and `github/gh-actions-lock/main/README.md` (94 lines, exit 0). Neither is pasted whole; the sections that decide an answer are quoted in Measured facts.

### Repository reads, local

```text
$ grep -n 'workflow_call\|uses: .*\.ya\?ml@\|uses: \./' .github/workflows/*.y*ml
exit=1
```

```text
$ sed -n '133,145p' tests/unit/test_workflow_security.py
    def test_external_actions_use_full_commit_shas(self):
        mutable = []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                match = re.search(r"uses:\s+([^\s]+)", line)
                if not match:
                    continue
                reference = match.group(1)
                if reference.startswith(("./", "docker://")):
                    continue
                if not re.fullmatch(r"[^@]+@[0-9a-f]{40}", reference):
                    mutable.append(f"{path.name}:{number}: {reference}")
        self.assertEqual([], mutable)
```

```text
$ sed -n '190,195p' tests/unit/test_regime_ci.py
        steps = job["steps"]
        pins = [
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7",
        ]
        self.assertEqual(pins, [s["uses"] for s in steps if "uses" in s])
```

```text
$ sed -n '137,138p' tests/unit/test_regime_workflow.py
CHECKOUT_ACTION = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_UV_ACTION = "astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7"
```

```text
$ sed -n '901,903p' tests/unit/test_github_release.py
            text = workflow.read_text()
            steps = text.count("uses: jdx/mise-action@")
            self.assertEqual(steps, text.count("minimum_release_age: 72h\n"), workflow.name)
```

## Measured facts

### The six direct actions against the lockfile

The `commit` the lockfile recorded agrees with the SHA in every workflow (the `cat` block). The lockfile names each dependency by the tag the extension resolved for the SHA, not by the SHA the workflow had.

| Action                                   | SHA in the workflows (before the run)      | Lockfile `ref` | Lockfile `commit` (sha1-)                  | `owner_id` | `repo_id` | Agree |
| ---------------------------------------- | ------------------------------------------ | -------------- | ------------------------------------------ | ---------- | --------- | ----- |
| actions/checkout                         | `3d3c42e5aac5ba805825da76410c181273ba90b1` | `v7.0.1`       | `3d3c42e5aac5ba805825da76410c181273ba90b1` | 44036562   | 197814629 | yes   |
| astral-sh/setup-uv                       | `c18668ad3cf93ea998bef934396af7bb5c839dc7` | `v10.2.0`      | `c18668ad3cf93ea998bef934396af7bb5c839dc7` | 115962839  | 846733598 | yes   |
| jdx/mise-action                          | `c2a87611a18de5b3828c5652fe268e992400cb5c` | `v4.3.0`       | `c2a87611a18de5b3828c5652fe268e992400cb5c` | 216188     | 738284564 | yes   |
| webfactory/ssh-agent                     | `e83874834305fe9a4a2997156cb26c5de65a8555` | `v0.10.0`      | `e83874834305fe9a4a2997156cb26c5de65a8555` | 135788     | 208510314 | yes   |
| benchmark-action/github-action-benchmark | `4322e5726e6334590d251fc4f92bec0efafc45dc` | `v1.22.2`      | `4322e5726e6334590d251fc4f92bec0efafc45dc` | 91769432   | 219665796 | yes   |
| codecov/codecov-action                   | `303a32d7a59b442fa8d48b6a1cc6825c09c847a5` | `v7.1.1`       | `303a32d7a59b442fa8d48b6a1cc6825c09c847a5` | 8226205    | 200299178 | yes   |

### The transitive set the SHA pins do not cover

One `dependencies` entry is not one of the six:

| Dependency                                                     | `ref`    | `commit` (sha1-)                           | `owner_id` | `repo_id` | Reached through                 |
| -------------------------------------------------------------- | -------- | ------------------------------------------ | ---------- | --------- | ------------------------------- |
| actions/github-script@ed597411d8f924073f98dfc5c65a23a2325f34cd | `v8.0.0` | `ed597411d8f924073f98dfc5c65a23a2325f34cd` | 44036562   | 205262760 | codecov/codecov-action `v7.1.1` |

The five other direct actions declare no action dependency the extension could see. So the lockfile's extra coverage for this repository is exactly one commit, in the one step that runs only on the `ubuntu-24.04` row and never for a bot actor (`test.yaml:539`).

### The `uses:` rewrite

The writing run changed all 27 `uses:` lines in the eleven workflows (the `git status` and `git diff` blocks). Each `@<40-hex> # v<n>` reference became `@v<x.y.z>` with the comment removed, for example `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7` became `actions/checkout@v7.0.1`. The `--help` text calls the SHA form a problem: the `--no-fix` report's first finding is "6 actions are pinned to a bare SHA without a tag ref" with the hint "run `gh actions-lock` to pin to tagged releases". `--no-narrow` keeps a partial tag such as `v4` as written. No flag in `--help` keeps a SHA reference as written.

### The test with the lockfile present

`test_external_actions_use_full_commit_shas` failed with 27 findings, one per rewritten line (the test block, "Second list contains 27 additional elements"). The other 15 tests of the module passed. The module globs `*.y*ml` (`tests/unit/test_workflow_security.py:135`), so it did not read `actions.lock` as a workflow; the failure is the rewrite, not the lockfile. Two more tests hard-code the setup-uv and checkout SHAs of `regime.yml`: `tests/unit/test_regime_ci.py:190-195` asserts the exact `uses:` list, and `tests/unit/test_regime_workflow.py:137-138` holds the same two strings as fixture constants. Adopting the lockfile as the extension writes it means deleting or inverting the first test and rewriting the other two.

### Preview status and Dependabot behaviour, from the vendor pages

The network allowlist of this unit is `github.com`, `api.github.com`, `objects.githubusercontent.com` and `raw.githubusercontent.com`, so `docs.github.com` and `github.blog` were not read directly. The quotes below come from the research file `handoff/research/03-ci-reliability.md` lines 147 to 149, which cites these URLs, and from the brief's own quotes of the how-to, and from the extension README read directly.

- Concept page, <https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles> (public preview): the lockfile records `ref`, `commit`, `owner_id`, `repo_id` per dependency, covers transitive action dependencies, and "For repositories that adopt a lockfile, SHA pinning within workflow files is no longer necessary."
- Secure use reference, <https://docs.github.com/en/actions/reference/security/secure-use>: the lockfile "is the strongest protection available, and supersedes SHA pinning for repositories that adopt it"; for the SHA fallback, "verify it is from the action's repository and not a repository fork".
- Changelog of 2026-10-14, <https://github.blog/changelog/2026-10-14-github-actions-workflow-lockfiles-in-public-preview>: available on Free plans, workflows are onboarded one at a time, a stale-lockfile check exists "including in a CI check", Dependabot regenerates the entry in the same PR, and a "Require lockfile" policy exists.
- How-to, <https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies> (the URL from the extension README, line 81): step 4, "The extension changes more than the lockfile", and on Dependabot, "it also regenerates the matching lockfile entry in the same pull request". Both quotes are taken from the brief, not from the page. The first one is measured above: eleven workflows changed.
- Extension README, <https://github.com/github/gh-actions-lock> (read directly): the lockfile is written with format `version: 'v0.0.3'` (the `cat` block). Limitations: "Reusable workflows called at `jobs.<id>.uses` from another repository are not locked", "Container images are not locked", and "A lockfile change that moves a floating ref (`v4`, `main`) back to an older commit in its history isn't detected, so review lockfile diffs or pin exact tags." The README's Modes table names `--verify` for CI and `--verify-local` for pre-commit.

### The Actions permissions endpoint

`gh api repos/mryfmo/dotfiles/actions/permissions` returned HTTP 403, "You must have repository read permissions or have the repository Actions policies fine-grained permission." The host's token lacks that permission, so whether the repository runs an allowlist of tag-pinned entries, and so whether the how-to's IMPORTANT note applies, is not measured.

### #548, astral-sh/setup-uv 10.2.0 to 10.3.2

| Fact                                       | Value                                                                                                                                                                                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| State, base, mergeable                     | `OPEN`, `main`, `MERGEABLE`                                                                                                                                                                                                                       |
| Created                                    | `2026-10-25T10:18:00Z`                                                                                                                                                                                                                            |
| New SHA in the diff                        | `07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2`, six times                                                                                                                                                                                   |
| `repos/astral-sh/setup-uv/commits/v10.3.2` | `07a047e608db84b3d8c06cd9a7c7dcc9c355c18e`, equal to the diff, so the pin is the action's own repository at the named tag                                                                                                                         |
| `releases/tags/v10.3.2` published          | `2026-10-22T08:47:11Z`, 3 days 1 hour 31 minutes before the PR, inside the 3-day `cooldown.default-days` of `.github/dependabot.yml:10-11`                                                                                                        |
| CI on head `84b6f259`                      | `Unit test` failed on all four rows, `regime` failed, every other check green (the `pr view` block)                                                                                                                                               |
| Why `Unit test` failed                     | `tests/unit/test_regime_ci.py:193` asserts the old setup-uv SHA in `regime.yml` (the run's failed step is `Run Python unit tests`; the source excerpt is above)                                                                                   |
| Why `regime` failed                        | The body has no `Program-Unit:` line; standing order 17 says that check reads it, so a Dependabot body fails it                                                                                                                                   |
| Release notes content (the PR body)        | v10.3.0: `python-arch` input, checksums for uv through 0.13.0; v10.3.1: cache save fix for the "Unable to reserve cache" warning, checksums for 0.13.1 to 0.13.4, "Verify npm dependency signatures before builds"; v10.3.2: checksums for 0.13.5 |

Call sites, all six with `enable-cache: false` and no other input (measured from the workflows). No input changes name or meaning in the notes, so no call site needs a value change.

| Call site             | Inputs                |
| --------------------- | --------------------- |
| `test.yaml:442`       | `enable-cache: false` |
| `agent-assets.yml:39` | `enable-cache: false` |
| `docs-check.yml:46`   | `enable-cache: false` |
| `docs.yml:45`         | `enable-cache: false` |
| `drift-watch.yml:31`  | `enable-cache: false` |
| `regime.yml:34`       | `enable-cache: false` |

### #549, jdx/mise-action 4.3.0 to 5.2.2

| Fact                                     | Value                                                                                                                                                                                                                    |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| State, base, mergeable                   | `OPEN`, `main`, `MERGEABLE`                                                                                                                                                                                              |
| Created                                  | `2026-10-25T10:18:16Z`                                                                                                                                                                                                   |
| New SHA in the diff                      | `8418fedb1110381a0d3ba51a7a415d7c1b884550 # v5.2.2`, five times                                                                                                                                                          |
| `repos/jdx/mise-action/commits/v5.2.2`   | `8418fedb1110381a0d3ba51a7a415d7c1b884550`, equal to the diff                                                                                                                                                            |
| `releases/tags/v5.2.2` published         | `2026-10-21T10:06:03Z`, 4 days 0 hours 12 minutes before the PR. v5.2.3 (`2026-10-24T10:05:40Z`) was one day old at PR time, which is why the bot offered 5.2.2; v5.2.4 followed on `2026-10-27T10:06:24Z`               |
| CI on the head                           | Every check green except `regime` (same cause as #548); `MacOS build` and `Ubuntu build` skipped, as gate G13 records for the secret-gated workflows                                                                     |
| Breaking change of v5.0.0 (release note) | "`minimum_release_age` now defaults to `24h`"; an explicit `version` skips the delay; the release list comes from the public CDN index (`releases.tsv`), and a missing index fails the run instead of skipping the check |

Call sites, five, each with `minimum_release_age: 72h` and `cache: true` (measured from the workflows; research section 2.4 counted three):

| Call site              | `minimum_release_age` | `install` | `cache` |
| ---------------------- | --------------------- | --------- | ------- |
| `test.yaml:265-270`    | `72h`                 | `false`   | `true`  |
| `macos.yaml:177-180`   | `72h`                 | `true`    | `true`  |
| `ubuntu.yaml:127-130`  | `72h`                 | `true`    | `true`  |
| `docs.yml:50-54`       | `72h`                 | `false`   | `true`  |
| `docs-check.yml:51-55` | `72h`                 | `false`   | `true`  |

Per input the five sites use, against the README on `main` and the release notes:

| Input or behaviour                  | v5 state                                                                                                                                                                                                                                                                                                                                                                                                        | Value change needed at a site                                                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `minimum_release_age`               | Still documented (README "Minimum Release Age": "set `minimum_release_age` and omit `version`"); default now `24h`. All five sites set `72h`, so the v5 default never applies.                                                                                                                                                                                                                                  | None                                                                                                                                                            |
| `install: false`                    | Documented, default `true` (README line 21). Unchanged.                                                                                                                                                                                                                                                                                                                                                         | None                                                                                                                                                            |
| `cache: true`                       | Default `true`. v5.2.0: "Existing caches miss once after you upgrade, because the default cache key format has changed." v5.2.2 adds `conf.d/*.toml` to the key hash. One cold run per cache scope after the bump.                                                                                                                                                                                              | None                                                                                                                                                            |
| `cache_max_age_days`                | New in v5.2.0, default `30`: the key carries a period suffix and the cache is rebuilt at least every 30 days. `0` keeps the old never-expiring key.                                                                                                                                                                                                                                                             | None                                                                                                                                                            |
| Packslip for mise 2026.9.3 or later | v5.2.1: the action refuses a mise 2026.9.3 or later release whose signed `packslip.sigstore.json` is missing. Every release from 2026.9.3 on ships one. The sites install the newest release at least 72 h old, so every install is past 2026.9.3 and carries a packslip.                                                                                                                                       | None                                                                                                                                                            |
| `auto_update`                       | New in v5.1.0, default `false`. v5.1.0 "Changed": "A cached mise is kept when `version` is unset ... until the cache key changes." Before, a new release made the action download mise again. With `cache: true` and no `version`, CI's mise now lags the hosts' 72 h window by up to the key's life (30 days under v5.2.0). `auto_update: true` restores the follow-the-release behaviour, cached per version. | One addition to decide: `auto_update: true` at the five sites keeps the intent the comment states, "as hosts get it". The existing inputs need no value change. |
| `--monorepo`                        | v5.2.0 adds `--monorepo` to `mise install` only when the mise config sets `[monorepo].config_roots`. `home/dot_mise/config.toml` has no `monorepo` key (grep, no match).                                                                                                                                                                                                                                        | None                                                                                                                                                            |

`tests/unit/test_github_release.py:902-903` asserts that every `uses: jdx/mise-action@` step carries `minimum_release_age: 72h`; the bump keeps that true.

## Recommendation

**Lockfile: `defer`.** Three measured reasons. First, `gh actions-lock` v0.4.0 rewrites every SHA reference to a tag, so adopting the lockfile as written deletes the repository's own SHA invariant in three tests and leaves the pin check to the runner's lockfile enforcement, which this unit could not observe (no live run, no readable Actions policy). Second, the gain is one transitive commit, `actions/github-script@ed597411` under codecov-action, in one step of one matrix row. Third, the feature is a public preview with lockfile format `v0.0.3` and a README limitation about moved floating refs. The condition that changes this to `adopt`: the lockfile leaves preview, or the extension gains a mode that keeps `@<40-hex>` references so `test_external_actions_use_full_commit_shas` survives, and the repository's `actions/permissions` policy is readable so the allowlist interaction is known. Either way the adopting unit also adds `gh actions-lock --verify` to CI, as the README's Modes table prescribes. The condition that changes it to `reject`: the extension's rewrite stays mandatory after general availability.

**#548: `adopt as a unit`**, brief `briefs/U<n>-setup-uv-pin-10.3.2.md` (the coordinator assigns `n`). The reason from the notes: 10.3.0 to 10.3.2 embed the known checksums for uv 0.13.0 to 0.13.5, and the action's own build now verifies npm dependency signatures. The six sites set no `version`, so the pin that knows the current checksums is the one to run. The SHA is the action's own tag commit and the release is past the 3-day cooldown. The Dependabot head cannot go green on its own: `tests/unit/test_regime_ci.py:193` hard-codes the old SHA. The unit carries the six `uses:` lines with `# v10.3.2`, the new SHA at `tests/unit/test_regime_ci.py:193` and `tests/unit/test_regime_workflow.py:138`, `tests/unit/test_workflow_security.py` and `tests/unit/test_regime_ci.py` passing, and CI green on every row including the three secret-gated workflows (gate G13). The coordinator closes #548 as superseded once the unit lands.

**#549: `adopt as a unit`**, brief `briefs/U<n>-mise-action-pin-5.2.2.md`. The reason from the notes: v5.2.0 and v5.2.1 verify the mise binary against its signed packslip and refuse a missing one for 2026.9.3 or later, which the 72 h window always reaches. v5.2.0 also rolls the cache every 30 days, so a long-lived cache cannot keep one mise forever. The v5.0.0 breaking default is already set at all five sites. The SHA is the action's own tag commit and the release is past the cooldown. The unit carries the five `uses:` lines with `# v5.2.2` (or the newest tag older than 3 days at its date, re-read from the notes), one decision on `auto_update: true` at the five sites with its reason recorded in the comment, the one-time cache miss accepted in the body, `tests/unit/test_workflow_security.py` and `tests/unit/test_github_release.py` passing, and CI green on every row including the three secret-gated workflows (gate G13). The coordinator closes #549 as superseded once the unit lands.

The owner of this unit touched neither PR: no close, comment, review, merge, edit or rerun.

## Draft decisions row

| Field      | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ts`       | `2026-10-29T06:19:30Z`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `phase`    | `plan-P-35`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `decision` | workflow lockfile evaluation (plan P-35, research V4-4): defer; #548 adopt as a unit; #549 adopt as a unit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `why`      | gh actions-lock v0.4.0 rewrites every SHA-pinned uses: line to a tag and fails test_external_actions_use_full_commit_shas (27 findings); the lockfile adds one transitive dependency (actions/github-script via codecov-action) and is a public preview (format v0.0.3). #548: tag commit verified, released 2026-10-22, 10.3.x embeds the uv 0.13.x checksums, the Dependabot head fails test_regime_ci.py:193 which hard-codes the pin, so a unit carries the pin and the test. #549: tag commit verified, released 2026-10-21, the v5 breaking default (minimum_release_age 24h) is already set to 72h at all five sites, v5.1 keeps a cached mise until the key changes so the unit decides auto_update |
| `evidence` | `handoff/evaluations/U115-workflow-lockfile.md`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `result`   | proposed; the coordinator records and triages                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

The same row as one line with literal tab separators:

```text
2026-10-29T06:19:30Z	plan-P-35	workflow lockfile evaluation (plan P-35, research V4-4): defer; #548 adopt as a unit; #549 adopt as a unit	gh actions-lock v0.4.0 rewrites every SHA-pinned uses: line to a tag and fails test_external_actions_use_full_commit_shas (27 findings); the lockfile adds one transitive dependency (actions/github-script via codecov-action) and is a public preview (format v0.0.3). #548: tag commit verified, released 2026-10-22, 10.3.x embeds the uv 0.13.x checksums, the Dependabot head fails test_regime_ci.py:193 which hard-codes the pin, so a unit carries the pin and the test. #549: tag commit verified, released 2026-10-21, the v5 breaking default (minimum_release_age 24h) is already set to 72h at all five sites, v5.1 keeps a cached mise until the key changes so the unit decides auto_update	handoff/evaluations/U115-workflow-lockfile.md	proposed; the coordinator records and triages
```

## Left out

- A live run under the lockfile. No workflow ran with `actions.lock` present; the runner's enforcement, the `--verify` check in CI and the "stale lockfile" failure mode are unmeasured.
- The "Require lockfile" policy and the `actions/permissions` read. The how-to at <https://docs.github.com/en/actions/how-tos/administer/enforce-workflow-lockfiles> was not read (outside the network allowlist), and the permissions endpoint returned 403.
- Reusable workflows. The repository has none: no `workflow_call` trigger and no `jobs.<id>.uses` reference in the eleven workflows (the local grep, exit 1), so the README's reusable-workflow limitation does not apply today.
- The vendor pages on `docs.github.com` and `github.blog` themselves. Their quotes are taken from the research file and the brief, as stated under Measured facts.
- The setup-uv README and the setup-uv default for `version`. The adopting unit reads them.
- The `Unit test` log of #548 beyond the failed step name and the test named in the source. The log was located with a filter, so the conclusion rests on the source excerpt and the `jobs` block, not on the log line.
- The extension's run logs. Each `gh actions-lock` run wrote one JSON file under the user cache directory (`~/Library/Caches/gh-actions-lock/logs/`, the path in the `--no-fix` block). They were not read and not deleted.
