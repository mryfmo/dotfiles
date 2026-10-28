# CI reliability (V4) and the supply-chain pins

Research for the regime-cutover remediation, exploration angle "verification-phase CI reliability and the supply-chain pins". Every external claim carries its URL and was read on 2026-10-28 (JST) unless the line says otherwise. Every repository claim names the file and line read in `~/Workspace/dotfiles` at origin/main 65f630b6. Lines marked **inferred** are the researcher's reading, not a measured fact.

Proposals are numbered V4-1 to V4-10 and written out in section 7 in the brief grammar, with two considered and rejected items listed after them. Section 8 lists every source.

## Summary

| Item                  | Current vendor recommendation                                                                                             | Repository today                                                                    | Verdict                                                                                                                                                  | Proposal                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| macos-14 retirement   | Retired 2026-11-02, eight October brownouts, move to `macos-15` or `macos-latest` (macos-26)                              | Every macOS job on the explicit label `macos-15`                                    | U64b matches. No `-latest` label anywhere, so `macos-latest` drift does not apply                                                                        | V4-1 (next retirement watch) |
| Azure apt mirror      | Issue #14823 open, mirror-side fault, GitHub staff workaround is to delete the Azure line from `/etc/apt/apt-mirrors.txt` | `scripts/ci/drop-azure-apt-mirror.py` before the first apt use in all four apt jobs | U102 matches the staff workaround. #15040 (public archive stalls at index refresh) is not covered by the drop, and no apt call has its own bound         | V4-2                         |
| `timeout-minutes`     | Job default 360 min, step max 360                                                                                         | Every job bounded, the two long bats steps bounded                                  | Matches. The apt and brew install steps carry no step bound                                                                                              | V4-2                         |
| `concurrency`         | One group per logical unit, `cancel-in-progress` or `queue`                                                               | Eight of eleven workflows                                                           | macos.yaml, ubuntu.yaml and private-bootstrap.yaml have none                                                                                             | V4-3                         |
| Action pinning        | Workflow lockfile (preview 2026-10-14) supersedes SHA pins where adopted, else full SHA                                   | Every `uses:` is a full SHA with a version comment                                  | Matches the fallback. Lockfile not evaluated                                                                                                             | V4-4                         |
| Dependabot            | github-actions ecosystem, cooldown, groups                                                                                | Weekly, cooldown 3 days, minor and patch grouped                                    | Matches. #548 and #549 untriaged since 2026-10-25                                                                                                        | V4-4                         |
| `pull_request_target` | Default policy blocks it in public repositories from 2026-12-02                                                           | `regime.yml` uses it, never checks out the head, read-only token                    | Design matches the hardening list. The repository is public, so the check stops on 2026-12-02 without an explicit event policy                           | V4-5                         |
| Bats                  | `BATS_TEST_TIMEOUT` has an open fail-path hang in 1.13.0 and 1.14.0 (#1206)                                               | A Python wrapper names the stalled test from the `cat` stream and signals nothing   | U99 matches the vendor state. Bats itself is unpinned across hosts and CI (1.10.0 apt, 1.13.0 apt on 26.04, 1.14.0 brew) while `config.toml` pins 1.14.0 | V4-6, V4-7                   |
| npm `min-release-age` | Added in npm 11.10.0 (2026-02-11), days, `min-release-age-exclude` exempts names                                          | `~/.npmrc` sets 3, mise sets 72h, no exemption                                      | Matches. The ccusage 20.0.38 failure was a cooldown edge, not a missing publish (measured below)                                                         | V4-8                         |
| mise pinning          | Commit `mise.lock`, install with `--locked`, bump on a schedule                                                           | No lockfile, `latest` for most tools, exact pins with reasons for held tools        | Partial. CI resolves `latest` fresh on every run, hosts reuse installed matches                                                                          | V4-9                         |
| git maintenance       | 2.55 made background maintenance hold `maintenance.lock`, 2.56 deflaked its own tests by disabling auto-detach            | Scratch repositories disable maintenance in config and environment                  | U100 matches, and upstream adopted the same mechanism                                                                                                    | none                         |
| chezmoi externals     | `refreshPeriod`, `checksum.*`, `urls` fallbacks, `--refresh-externals`, no retry or timeout setting                       | A curl prefetch writes verified archives into chezmoi's cache                       | U96 is not vendor-documented. It depends on an undocumented cache layout read from one chezmoi version                                                   | V4-10                        |

## 1. Runner images (actions/runner-images)

### 1.1 macos-14 retirement and brownouts

Vendor statements:

- Issue [#13518](https://github.com/actions/runner-images/issues/13518) (opened 2026-01-11, still open, last updated 2026-10-11): deprecation began 2026-07-06, images "fully unsupported by November 2nd, 2026". Brownouts, each 14:00 UTC to 00:00 UTC the next day: October 5, 12, 16, 19, 23, 26, 29 and 30. Labels `macos-14`, `macos-14-large`, `macos-14-xlarge` "will be terminated with an error". Mitigation named: `macos-latest`, `macos-15` or `macos-26`.
- Changelog [GitHub Actions: macOS 14 runner image retirement](https://github.blog/changelog/2026-10-01-github-actions-macos-14-runner-image-retirement) (2026-10-01): the same dates, plus "GitHub may reduce macOS 14 runner capacity" before retirement, and the replacement list `macos-latest` (`macos-26`), `macos-15`, `macos-latest-xlarge` (`macos-26-xlarge`), `macos-15-xlarge`.

Repository today:

- `.github/workflows/test.yaml:34` matrix `os: [ubuntu-24.04, macos-15]`, line 37 excludes the macOS server row.
- `.github/workflows/macos.yaml:67` matrix `os: [macos-15]`, line 68 comment "Apple silicon". Lines 147-148 record that the benchmark series "MacOS benchmark" holds macos-14 data and ends with that image's retirement (U64b).
- `.github/workflows/remote.yaml` and `private-bootstrap.yaml` matrix rows name `macos-15` (remote.yaml lines 29-35 region, private-bootstrap.yaml lines 54-60 region).
- No workflow uses `macos-latest`, `ubuntu-latest` or `macos-14` as a label. The two remaining `macos-14` strings are comments (`test.yaml:459`, `macos.yaml:148`).
- Ruleset 24397953 required contexts are the macos-15 names since 2026-10-26 (decisions.tsv row `G10-done`).

Verdict: U64b matches the current recommendation. The repository chose the explicit label, which the runner-images README recommends for anyone who wants to avoid the `-latest` migration ("To avoid unwanted migration, users can specify a specific OS version", [README, Latest Migration Process](https://github.com/actions/runner-images#latest-migration-process)).

### 1.2 macos-15, macos-26 and the `macos-latest` default

Vendor statements:

- Issue [#14167](https://github.com/actions/runner-images/issues/14167) (closed): `macos-latest` moved to macOS 26 between 2026-06-15 and 2026-07-15. A GitHub engineer confirmed on 2026-07-22: "the migration to macos-latest is complete, and the label now uses macOS 26 images". The issue's table lists the breaking differences (Xcode 26.4.1 default, Clang 21, Node 24 default, Ruby 3.4, npm 11.12.1, OpenSSL 3.6.2).
- Changelog [GitHub Actions: Upcoming image migrations](https://github.blog/changelog/2026-05-14-github-actions-upcoming-image-migrations/) (2026-05-14): "To continue using macOS 15, you can target the `macos-15` label directly."
- [README Available Images](https://github.com/actions/runner-images#available-images) on 2026-10-28: macOS 26 arm64 is `macos-latest`, `macos-26` or `macos-26-xlarge`. macOS 15 arm64 is `macos-15` or `macos-15-xlarge`. macOS 14 rows carry the deprecated badge. The x64 macOS 15 labels are `macos-15-large` and `macos-15-intel`.
- Support policy (same README, "Software and Image Support"): "We support (at maximum) 2 GA images and 1 beta image at a time. We begin the deprecation process of the oldest image label once the newest OS image label has been released to GA."
- The [Announcement label](https://github.com/actions/runner-images/labels/Announcement) listed 12 open announcements on 2026-10-28. None announces a macOS 15 deprecation.

Verdict: after 2026-11-02 the two GA macOS images are 15 and 26, so macos-15 is the next label the policy deprecates once a macOS 27 image reaches GA (**inferred** from the policy, no date exists). The repository's weekly drift watch (`.github/workflows/drift-watch.yml:1-9` comment, `scripts/drift-watch.py`) already reads "open runner-image announcements that mention a label in use", so the announcement will surface in the tracking issue when it is filed. Nothing to change now beyond V4-1, which records the watch condition in the store so the next coordinator does not re-derive it.

### 1.3 ubuntu-24.04, ubuntu-26.04 and `ubuntu-latest`

Vendor statements:

- Issue [#14747](https://github.com/actions/runner-images/issues/14747) (2026-09-17): Ubuntu 26.04 and 26.04 Arm64 generally available, labels `ubuntu-26.04` and `ubuntu-26.04-arm`.
- Issue [#14748](https://github.com/actions/runner-images/issues/14748) (2026-09-17, open, 86 comments): `ubuntu-latest` moves from 24.04 to 26.04 "over a period of several weeks beginning October 19, 2026 ... complete the migration by November 19, 2026". Mitigation: pin `ubuntu-24.04`.
- Changelog [Ubuntu 26 generally available and latest migration](https://github.blog/changelog/2026-09-17-ubuntu-26-generally-available-and-latest-migration/) (2026-09-17): "Ubuntu 26.04 includes updated, and in some cases removed, tools and tool versions compared to earlier images."
- Issue [#14254](https://github.com/actions/runner-images/issues/14254): Ubuntu 22.04 deprecation begins 2026-09-17, fully unsupported 2027-04-17 (the issue says "April 17th", **inferred** as 2027 from the September start).
- README table on 2026-10-28 still shows `ubuntu-latest` on the Ubuntu 24.04 row, consistent with a migration in progress.

Repository today:

- Every Ubuntu job names `ubuntu-24.04` explicitly (`test.yaml:34`, `ubuntu.yaml:65`, `macos.yaml:35`, `remote.yaml` matrix, `drift-watch.yml:25`, `regime.yml:24`, `docs.yml:30`, `docs-check.yml:32`, `agent-assets.yml:25`, `apply-check.yml:24`, `private-bootstrap.yaml:20`).
- `test.yaml:39-44` adds a non-required `ubuntu-26.04` client canary with `continue-on-error` (line 50) and the comment "Adopt it by changing the explicit label above once it is green".
- The canary has been red on the Azure mirror stalls (U102 note in `units.tsv`: "#559 on ubuntu-26.04") and the ghostty 796 s outlier (`decisions.tsv` row `U99-job-timeout`).

Verdict: the `ubuntu-latest` migration does not touch this repository. The canary is the right shape. The remaining question is when to promote the canary, which depends on 1.4.

### 1.4 The Azure apt mirror (#14823, #15040, #15142)

Status as of 2026-10-28:

- [#14823](https://github.com/actions/runner-images/issues/14823) "apt stays on a slow azure.archive.ubuntu.com node for 20 min; the #14594 timeout only covers stalls". Opened 2026-09-30, **open**, last updated 2026-10-28T04:47Z, 13 comments. Facts in the issue: the image sets `Acquire::Retries "1"` and `Acquire::http::Timeout "15"` (from #14594), the timeout fires only when no data arrives for 15 s, and "apt has no minimum-throughput setting". GitHub staff on 2026-10-01: "we're aware of this issue and are currently working on the case". A runner-images engineer on 2026-10-27: the westus and westus3 endpoints "serve archives at 40 to 75 kB/s from every runner region we tried", other regions 20 to 90 MB/s. A GitHub Actions engineer on 2026-10-27T19:52Z: "a problem with the mirror itself and not Actions runners. We're working with Canonical", and at 20:52Z: "`azure.archive.ubuntu.com` is back to healthy". A contributor noted the image's apt configuration "is bypassing the cache" and promised a PR. The last comment (2026-10-28) asks for a post-mortem so reporters can "undo the mitigations we've added, including disabling the Azure mirrors entirely".
- **The image did not fix it.** No release note or comment says the image changed. The fix on 2026-10-27 was on the mirror side.
- Recommended workaround, stated twice by runner-images staff: in [#15142](https://github.com/actions/runner-images/issues/15142) (closed 2026-10-27 as a duplicate of #14823) the engineer gives this shape:

```yaml
- name: Install packages
  timeout-minutes: 6
  run: |
    sudo apt-get update
    if ! timeout 90 sudo apt-get install --yes --download-only $pkgs; then
      sudo sed -i '/azure\.archive\.ubuntu\.com/d' /etc/apt/apt-mirrors.txt
      sudo apt-get install --yes --download-only $pkgs
    fi
    sudo apt-get install --yes $pkgs
```

A reporter in #14823 (2026-10-22) deletes the line after a stalled attempt. The original reporter serves archives from an Actions cache checked against the index's SHA256.

- [#15040](https://github.com/actions/runner-images/issues/15040) (opened 2026-10-22, **open**, no comments): `apt-get update` on image 20261012.334.1 in westus3 ignored the Azure mirror, fell back to `https://archive.ubuntu.com`, and then printed nothing for 15 min 28 s until cancellation. The reporter could not tell whether bytes were flowing. This is a different symptom from #14823: the public archive, during the index refresh, after the failover the repository's drop forces.

Repository today:

- `scripts/ci/drop-azure-apt-mirror.py:1-19` documents the mechanism and cites #14823. It deletes the Azure line, refuses an empty list, reads back and compares byte for byte, exits 1 on any read or write failure.
- Called before the first apt use in all four apt jobs: `test.yaml:164-168`, `ubuntu.yaml:83-85`, `remote.yaml:136-139`, `private-bootstrap.yaml:158-161`. `tests/unit/test_apt_mirror.py:35-45` pins the job set and checks the order.
- No apt call carries its own bound. `test.yaml:191` (`sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby`) runs inside the "Install tools" step, which has no `timeout-minutes`. `test.yaml:450` runs `apt-get update` again inside "Run Python unit tests", also without a step bound. The U99 bound lint (`decisions.tsv` row `treadmill-u99-scanner`) covers `curl` and `wget` only.
- The budgets in `tests/unit/test_apt_mirror.py:41-52` (`PRE_STEP_BUDGET = 480`, `OTHER_TESTS_BUDGET = 300`, `FILES_STEP_BUDGET = 300`) are hand-measured constants that stand in for step bounds.

Verdict on U102: it matches the issue's workaround and is slightly stricter than the staff variant (the drop is unconditional rather than after a 90 s failed attempt). Two gaps remain:

1. The #15040 class. After the drop every apt call goes to `archive.ubuntu.com`, which the one report shows can also go silent during `apt-get update`. The only bound is the job's `timeout-minutes` (45 min on `test`), so such a stall eats the budget that U99 and U102 sized so that a stalled bats test is named first (`test.yaml:47-49`, `tests/unit/test_apt_mirror.py` `BoundOrderTest`). A silent `apt-get update` in "Install tools" would cancel the job at 45 min with no diagnosis.
2. No exit condition. The drop has no expiry or re-check. Once #14823 closes, the repository keeps serving from the slower public archive without noticing. The drift watch reads announcements, not issues.

Proposal V4-2 bounds every apt call with `timeout` plus `-o Acquire::http::Timeout` and `-o Acquire::Retries`, and records the re-check condition.

### 1.5 Announced software removals

Open announcements on 2026-10-28 ([label page](https://github.com/actions/runner-images/labels/Announcement)): [#14856](https://github.com/actions/runner-images/issues/14856) default OpenSSL 3 to 4 on macOS 26 and Xcode 27 (2026-10-06), [#14745](https://github.com/actions/runner-images/issues/14745) Android NDK 28 removed and 30 added (2026-09-17), [#14818](https://github.com/actions/runner-images/issues/14818) MySQL 8.0 to 8.4 on Windows, [#14826](https://github.com/actions/runner-images/issues/14826) Android CMake on Windows 11 Arm, plus the image-management announcements above. None names a tool the repository's jobs use (the jobs install their own bats, chezmoi, mise, uv, ruby gems and the pinned lint tools). The OpenSSL change applies to macOS 26, which the repository does not run. **Inferred:** no removal affects the repository today.

The other image-level change relevant to the repository is the certificate trust issue [#15018](https://github.com/actions/runner-images/issues/15018) (2026-10-21, eMudhra intermediates, CVE-2026-111943), which the drift watch would not catch because it is not an Announcement. Out of scope here, noted for the security angle.

## 2. GitHub Actions workflow practice

### 2.1 `timeout-minutes`

Vendor statement ([Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), read 2026-10-28): `jobs.<job_id>.timeout-minutes` "The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360". `jobs.<job_id>.steps[*].timeout-minutes` "The maximum number of minutes to run the step before killing the process. Maximum: 360 for both GitHub-hosted and self-hosted runners. Fractional values are not supported."

Repository today: every job sets a bound. `test.yaml:49` 45 (with the measured rationale on lines 47-48), `macos.yaml:36` 5 and `:70` 60, `ubuntu.yaml:67` 60, `remote.yaml:39` 30, `private-bootstrap.yaml:21` 5 and `:64` 30, `drift-watch.yml:26` 10, `regime.yml:25` 10, `docs.yml:32` 15, `docs-check.yml:33` 15, `agent-assets.yml:27` 10, `apply-check.yml:26` 15. Step bounds: `test.yaml:508` 35 on "Run unit test", `macos.yaml:172` and `ubuntu.yaml:141` 25 on "Test file existence". The wrapper's own text (`scripts/ci/run-bats.py:11-13`) names `timeout-minutes` and the runner as the only hard stop, by design (decisions row `premise-u99-supervisor`).

Gap: the network-heavy steps before the bats step ("Install tools", "Install statusline tools", "Install Claude Code", "Run the omp TypeScript tests", "Run Python unit tests") have no step bound, so the only attribution of a stall there is the job cancel at 45 min. Covered by V4-2.

### 2.2 `concurrency` and `cancel-in-progress`

Vendor statement (same page): "Use `concurrency` to ensure that only a single job or workflow using the same concurrency group will run at a time." `cancel-in-progress: true` cancels the running one, and it "can be an expression". A `queue` property now exists (`queue: max` cannot combine with `cancel-in-progress: true`).

Repository today: `test.yaml:17-19`, `remote.yaml:15-17`, `agent-assets.yml:16-18`, `apply-check.yml:15-17` use the pattern "a pull request's newer head cancels its older run, a main push is grouped by commit and never cancelled". `drift-watch.yml:15-17` fixed group, no cancel. `regime.yml:15-17` per PR, cancel. `docs.yml:21-23` and `docs-check.yml:23-25` per ref or PR, cancel.

Missing: `macos.yaml`, `ubuntu.yaml` and `private-bootstrap.yaml` have no `concurrency` block. `macos.yaml:61-65` serialises rows inside one run with `max-parallel: 1` because "every row pushes to the same benchmark repository", but two runs from two pushes to main can still push concurrently (**inferred** from the absence of a group). Proposal V4-3.

### 2.3 `actions/cache`

Vendor statements: the [dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) documents key matching, the `setup-*` actions that cache npm, pip, gems and Go, the note "don't store any sensitive information ... Anyone with read access can create a pull request on a repository and access the contents of a cache", and the low-trust rule: runs on `pull_request_target`, `issue_comment` and `workflow_run` get read-only cache access in the default branch scope unless `cache-mode: write` is declared. The [actions/cache README](https://github.com/actions/cache) (v6 current) lists `SEGMENT_DOWNLOAD_TIMEOUT_MINS` (default 10) as the stuck-download guard. Neither page offers an apt cache. The #14823 reporter built one by hand with SHA256 checks against the index.

Repository today: no direct `actions/cache` use. `jdx/mise-action` with `cache: true` (`test.yaml:265-270`, `macos.yaml:161-166`, `ubuntu.yaml:122-127`, `docs.yml:50-55`, `docs-check.yml:51-56`) caches mise's data directory keyed on the config hash, which covers the statusline npm tools. `astral-sh/setup-uv` runs with `enable-cache: false` everywhere.

Verdict: do not add an apt cache. The install tests exist to exercise real apt installs (`tests/unit/test_apt_mirror.py:30-34`), and a cache would test the cache. The npm tools are already cached through mise-action. No proposal.

### 2.4 Pinning actions, the lockfile, and the tj-actions incident

Vendor statements:

- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use), "Using third-party actions": "The best measure is to lock your workflow dependencies with a lockfile. This records the exact commit for every action your workflows depend on, including transitive dependencies, and verifies the identity of each source repository at run time. This is the strongest protection available, and supersedes SHA pinning for repositories that adopt it." For repositories that cannot: "Pin actions to a full-length commit SHA ... When selecting a SHA, you should verify it is from the action's repository and not a repository fork." Also: "Dependabot only creates alerts for vulnerable actions that use semantic versioning and will not create alerts for actions pinned to SHA values."
- [Workflow dependency lockfiles](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles) (public preview): `.github/workflows/actions.lock`, generated by `gh actions-lock`, records `ref`, `commit`, `owner_id`, `repo_id` per dependency, covers transitive action dependencies, "For repositories that adopt a lockfile, SHA pinning within workflow files is no longer necessary."
- Changelog [GitHub Actions workflow lockfiles in public preview](https://github.blog/changelog/2026-10-14-github-actions-workflow-lockfiles-in-public-preview) (2026-10-14): available on Free plans, onboard workflows one at a time, a stale-lockfile check "including in a CI check", Dependabot regenerates the entry in the same PR, a "Require lockfile" policy exists.
- The motivating case: advisory [GHSA-mrrh-fwg8-r2c3 / CVE-2025-30066](https://github.com/advisories/GHSA-mrrh-fwg8-r2c3): between 2025-03-14 and 2025-03-15 "attackers retroactively modified multiple version tags" of tj-actions/changed-files to commit 0e58ed8671d6b60d0890c21b07f8835ace038e67, which dumped Runner Worker memory to the logs, "impacting over 23,000 repositories". Tags moved, SHAs did not. This is the event behind the "full-length SHA" guidance and the lockfile's `owner_id`/`repo_id` check.

Repository today: every `uses:` is a full SHA with a version comment: `actions/checkout@3d3c42e5…` v7 (`test.yaml:66` and every other workflow), `jdx/mise-action@c2a87611…` v4 (`test.yaml:265`), `astral-sh/setup-uv@c18668ad…` v10.2.0 (`test.yaml:442`), `codecov/codecov-action@303a32d7…` v7 (`test.yaml:540`), `webfactory/ssh-agent@e8387483…` v0.10.0 (`macos.yaml:78`, `ubuntu.yaml:74`, `private-bootstrap.yaml:154`), `benchmark-action/github-action-benchmark@4322e572…` v1 (`macos.yaml:145`). `.github/dependabot.yml:1-18` configures the github-actions ecosystem weekly on Monday, `cooldown.default-days: 3`, label `dependencies`, and one group `minor-and-patch` with `update-types: [minor, patch]`. The [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) confirms both keys and states a default cooldown of 3 days applies to version updates even when not configured.

Open since 2026-10-25T10:18Z (measured with `gh pr list`): #548 "bump astral-sh/setup-uv from 10.2.0 to 10.3.2 in the minor-and-patch group" and #549 "bump jdx/mise-action from 4.3.0 to 5.2.2" (a major, so ungrouped). The handoff lists them as untriaged, "each is a unit with a brief if adopted".

Gap: the SHA pins protect the direct `uses:` lines only. Transitive dependencies of the pinned actions (what `actions/checkout` or `codecov-action` themselves `uses:`) are not pinned by anything the repository controls. The lockfile closes that and adds the source identity check. It is a public preview "subject to change", which is the reason to evaluate rather than adopt blind. Proposal V4-4.

### 2.5 `permissions:` least privilege

Vendor statement ([Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)): "It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents. The permissions can then be increased, as required, for individual jobs."

Repository today: every workflow sets a top-level `permissions:` block. `contents: read` in `test.yaml:21-22`, `macos.yaml:28-29`, `ubuntu.yaml:28-29`, `remote.yaml:19-20`, `private-bootstrap.yaml:12-13`, `regime.yml:19-20`, `docs-check.yml:27-28`, `agent-assets.yml:20-21`, `apply-check.yml:19-20`. `drift-watch.yml:19-21` adds `issues: write` for its one tracking issue. `docs.yml:25-26` grants `contents: write` at workflow level for the one deploy job (equivalent to job level since the workflow has one job).

Verdict: matches. No proposal.

### 2.6 `pull_request_target`

Vendor statements ([Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)):

- The workflow and any `actions/checkout` without `ref` come from the base's default branch, so "No code from the fork is executed by default". Risk begins when the workflow checks out and runs the head.
- Hardening list: restrict the token and secrets, understand cache read-only scope, ephemeral compute, CodeQL. `actions/checkout` now refuses fork head refs unless `allow-unsafe-pr-checkout: true`.
- **Default policy:** "For public repositories that do not already have an applicable Actions event policy, GitHub adds a default policy that blocks workflows triggered by `pull_request_target`." Currently in evaluate mode. "On December 2, 2026, GitHub will enforce the default policy for affected repositories that were using the default `pull_request_target` policy before general availability." To keep using it: "create or update an applicable Actions event policy that explicitly allows `pull_request_target`."
- "Can you use `pull_request` instead?" The docs say yes when no secret access is needed.

Repository today: `regime.yml:11-13` triggers on `pull_request_target` for PRs into main. Lines 1-9 explain the design: the base's `scripts/orchestrator/regime-ci.py` reads the PR's diff and body, the head is fetched as data into `refs/regime/pr-head` and never checked out, the body reaches the script through an environment variable, the token is `contents: read` (lines 19-20), no secret is used, and `cancel-in-progress: true` (line 17). `gh repo view` on 2026-10-28 reports the repository `PUBLIC`.

Verdict: the workflow follows every item on the hardening list. `pull_request` is not a substitute here. The point of the check is that the verifier code comes from main, so a PR cannot edit `regime-ci.py` or the workflow to pass itself. Under `pull_request` both would come from the merge commit (**inferred** from the docs' description of which commit each event runs). The gap is administrative and dated: without an explicit event policy the `regime` check stops running on 2026-12-02. If the operator adds `regime` to the required contexts (gate G10 in `regime.yml:9`) before then, every PR blocks. Proposal V4-5.

### 2.7 `GITHUB_STEP_SUMMARY`

Vendor statement ([Workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#adding-a-job-summary)): `core.summary` is "Accessible using environment file `GITHUB_STEP_SUMMARY`", Markdown appended per step is shown on the run's summary page.

Repository today: used for the skip reasons (`test.yaml:162`, `remote.yaml:134`), the missing-secrets notice (`macos.yaml:56`, `ubuntu.yaml:56`, `private-bootstrap.yaml:41`) and the drift report (`drift-watch.yml:44`). The bats wrapper writes its `not ok ... # timeout` line and the process-tree diagnosis to stdout only (`scripts/ci/run-bats.py:131-135`), so the one line a reader needs after a cancelled job sits inside a 35 minute step log.

Gap: small. Proposal V4-7 adds the summary write to the wrapper.

## 3. Bats 1.14 and the U99 wrapper

### 3.1 What the vendor documents

From [Writing tests](https://bats-core.readthedocs.io/en/stable/writing-tests.html) (stable, Bats 1.14.0):

- `$BATS_TEST_TIMEOUT` "is the number of seconds after which a test (including setup) will be aborted and marked as failed. Updates to this value in `setup()` or `@test` cannot change the running timeout countdown, so the latest useful update location is `setup_file()`."
- `setup_file` and `teardown_file` "run once before the first test's `setup` and after the last test's `teardown` for the containing file. Variables that are exported in `setup_file` will be visible to all following functions".
- "File descriptor 3 (read this if Bats hangs)": a background child that inherits FD 3 blocks Bats until it exits. "close FD 3 explicitly when running any command that may launch long-running child processes".

From [Usage](https://bats-core.readthedocs.io/en/stable/usage.html): `-T, --timing` "Add timing information to tests". `--print-output-on-failure` "Automatically print the value of `$output` on failed tests". `-j, --jobs <jobs>` "Number of parallel jobs (requires GNU parallel or shenwei356/rush)", with the caveats "Ordering of parallelised tests is not guaranteed" and "the results of a file only become visible after it has been finished" unless `--no-parallelize-across-files`. `--formatter cat` is the raw extended stream the wrapper reads.

From the [changelog](https://github.com/bats-core/bats-core/blob/master/docs/CHANGELOG.md): 1.14.0 (2026-07-21) added `--errexit`, made `run` honour `set -e` ("ATTENTION ... might constitute a breaking change"), and "exit with error when no tests are found. Use `--allow-empty-suite` to revert". 1.13.0 (2025-11-07) "fix `BATS_TEST_TIMEOUT` (#1160): not stopping processes under `run`, prolonging skipped tests". Unreleased: "`--jobs` now aborts when GNU parallel is unavailable instead of failing later".

Issue state:

- [#1020](https://github.com/bats-core/bats-core/issues/1020) "BATS_TEST_TIMEOUT not honoured by run": closed 2025-11-06, fixed in 1.13.0. A child of `run` was not killed and held Bats' pipe open, so the suite hung. This is still the behaviour of 1.10.0, the apt package on ubuntu-24.04.
- [#1206](https://github.com/bats-core/bats-core/issues/1206) "BATS_TEST_TIMEOUT hangs full duration on fast-failing tests in 1.13.0": **open**, Priority High, Confirmed. Reproduced on 1.14.0 on 2026-09-25 ("fail.bats ~0.15s without, ~7.3s with `BATS_TEST_TIMEOUT=7`"). Root cause named (a `declare -r` scoped local, the watchdog is never signalled). Fix PR #1226 open. The reporter's workaround is a suite-level `timeout(1)`, which "loses per-test granularity".

So the vendor's per-test timeout is unusable on the three Bats versions CI meets today, for two different reasons. How Bats names a stalled test when the timeout does work: the pretty formatter prints `✗ name [timeout: 1s]` and `failed due to timeout` (expected output quoted in #1020).

### 3.2 What the repository does

- `scripts/run_unit_test.sh:17-39`: `run_bats` runs `python3 -I -S scripts/ci/run-bats.py "$@"`. Lines 19-22 give the reasons not to use `BATS_TEST_TIMEOUT`, citing #1020 for 1.10.0 and #1206 for 1.13.0 and 1.14.0. Both citations are accurate on 2026-10-28.
- `scripts/ci/run-bats.py:97-164`: runs `bats --formatter cat`, turns each `begin <n> <name>` line into `running: <n> <name>` (lines 110-113), resets a per-test deadline on `begin` and on any line outside a test (lines 112, 122-123), prints `not ok <n> <name> # timeout after <s> s (BATS_PER_TEST_TIMEOUT)` plus a `ps` tree with wchan (lines 64-94, 130-136) and exits 124. It signals nothing (docstring lines 11-13). Default bound 600 s (line 29, with the measurement behind it on lines 25-28). A plan of `1..0` or none fails (lines 160-163), which duplicates 1.14.0's new default for the older Bats releases.
- Flags in use: `--print-output-on-failure` on `macos.yaml:181` and `ubuntu.yaml:152`. The `common.bats` call on `ubuntu.yaml:150` passes no flags. `--timing` and `--jobs` appear nowhere (grep over `scripts/run_unit_test.sh`, the workflows and the Makefile). GNU `parallel` is installed on both images (`test.yaml:187,191`) but not used by Bats.
- `tests/unit/test_apt_mirror.py:260-262` asserts no workflow sets `BATS_PER_TEST_TIMEOUT`, so the wrapper's default governs. `BoundOrderTest` checks `2 × bound + OTHER_TESTS_BUDGET` fits under the 35 minute step.
- Bats itself: `brew install bats-core` (`test.yaml:187`, `macos.yaml:174`) and `apt-get install -y bats` (`test.yaml:191`) in CI, while `home/dot_mise/config.toml:46-51` pins `http:bats` 1.14.0 with a sha256 for hosts. The commented block `ubuntu.yaml:129-135` shows an older intent to install from source. So CI runs 1.10.0 on ubuntu-24.04, 1.13.0 on ubuntu-26.04 and the Homebrew 1.14.0 on macOS, and hosts run the pinned 1.14.0.

### 3.3 Comparison and gaps

U99's design is the correct response to the vendor state: an external watchdog on the extended stream, naming the test by its `begin` line, with the runner's step and job bounds as the only kill path. The decisions row `premise-u99-supervisor` records why in-wrapper killing was removed. Nothing in the 1.14.0 docs or the open issues offers a vendor mechanism that does the same.

Gaps:

1. **Bats version skew is the U97 class again.** 1.14.0 changed `run` to honour `set -e`, a documented breaking change. A test that passes under 1.10.0 on ubuntu-24.04 can fail under 1.14.0 on a host or on macOS, in the same way the ShellCheck 0.9.0 versus 0.11.0 skew produced SC2015 in CI twice (U97 note in `units.tsv`). The pin exists (`config.toml:46-51`) and `scripts/ci/install-pinned-lint-tools.sh` is the pattern. Proposal V4-6.
2. **No timing data.** The bound constants in `tests/unit/test_apt_mirror.py:41-52` and `run-bats.py:25-29` are measured by hand from logs. `--timing` puts a duration on each result line of the stream, so the slowest test per run can be read mechanically and the constants re-checked. **Inferred:** the exact suffix form in the `cat` stream needs one measured run before a parser depends on it. Proposal V4-7.
3. **Summary.** The timeout line and diagnosis do not reach `GITHUB_STEP_SUMMARY` (section 2.7). Proposal V4-7.
4. **`--jobs`** is not recommended here. The install tests do real apt installs and share the machine, which is the dependency case the docs warn about. No proposal.

## 4. npm and mise

### 4.1 npm `min-release-age`

Vendor statements:

- Introduced in npm CLI 11.10.0, released 2026-02-11, PR #8965 "add min-release-age" ([release notes](https://github.com/npm/cli/releases/tag/v11.10.0)).
- [Config reference](https://docs.npmjs.com/cli/v11/using-npm/config#min-release-age) (docs for 11.21.1 on 2026-10-28): `min-release-age` "Default: null, Type: null or Number", a relative number of days complementing `before`. "If `before` and `min-release-age` are both set in the same source, `before` wins ... Across sources, the standard precedence applies (cli > env > project > user > global)". When the window blocks an `npm audit fix` result, npm "keeps the vulnerable version, warns, and exits with a non-zero code". `min-release-age-exclude` is "A list of package names or `minimatch` glob patterns that are exempt ... Only the named package is exempt; its own dependencies still follow the release-age policy unless they also match a pattern." Neither value "is exported to the environment for child processes".

Repository today: `home/dot_npmrc:1` `min-release-age=3`. `home/dot_mise/config.toml:107` `minimum_release_age = "72h"` and `:110` the same for self-update. `scripts/lib/github-release.sh:12-14` `GITHUB_RELEASE_MIN_AGE_HOURS=72` "the same 72 hours as minimum_release_age ... Change both together". `.github/dependabot.yml:1-2` names the three as one window. `scripts/upgrade-tools.sh:328-343` (U89) asks npm for the window and the registry for the publish time before a rebuild and refuses a version younger than the window plus 60 s. `decisions.tsv` row `treadmill-u89-exclude` chose no exemption list. The mise docs confirm the backend behaviour the repository relies on: "The `npm:` and `pypi:` backends also pass the cutoff to the package manager for unpinned transitive dependencies" ([settings, minimum_release_age](https://mise.jdx.dev/configuration/settings.html#minimum_release_age)), and "Exact versions such as `node@22.5.0`, and versions recorded in `mise.lock`, are not filtered."

Verdict: matches. The four windows are equal (3 days, 72 h) and the no-exemption decision follows the docs' warning that an exemption does not cover a package's dependencies.

### 4.2 `npm ci` versus `npm install` for pinned tools

Vendor statement ([npm-ci](https://docs.npmjs.com/cli/v11/commands/npm-ci)): `npm ci` requires an existing `package-lock.json` or `npm-shrinkwrap.json`, errors when the lock and `package.json` disagree, removes `node_modules` first, "can only install entire projects at a time", "will never write to `package.json` or any of the package-locks". It is a project command. A global CLI install (`npm install -g <pkg>` or a tarball) has no project lock, so `npm ci` does not apply.

Repository today: `scripts/update-agent-assets.sh:1577-1579` installs the verified omp tarball with `npm install -g --prefix`, noting "The verified local tarball has no registry release date, so npm's min-release-age ... applies only to the dependencies it resolves". `home/dot_agents/agent-config.yaml:1206` records that the tarball "ships no npm-shrinkwrap.json, so its dependencies resolve at install time". The statusline tools install through mise's npm backend with `package_manager = "npm"` (`config.toml:112-113`).

Verdict: `npm ci` is not available for these installs. The lock-equivalent for a mise-managed npm tool is `mise.lock` format 2, which "records each npm tool's full dependency graph" but only "with the embedded aube installer" ([npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html), [lockfile, dependency graphs](https://mise.jdx.dev/dev-tools/mise-lock.html#dependency-graphs)). With `package_manager = "npm"` the lock records the version only (**inferred** from the backend table on that page). See V4-9.

### 4.3 The ccusage 20.0.38 class, measured

The repository's record (`units.tsv` U42, `config.toml:28-29`): "npm:ccusage 20.0.38 cleared the 72h cooldown at 10:49Z and installs without its linux-x64 native binary (job 120853039189)", held at 20.0.37 "until a release restores it".

Registry facts read on 2026-10-28 (`registry.npmjs.org`, the `time` map of each package):

| Package                         | 20.0.37 published    | 20.0.38 published    | 20.0.39 published    |
| ------------------------------- | -------------------- | -------------------- | -------------------- |
| `ccusage`                       | 2026-10-19T20:02:04Z | 2026-10-21T10:49:51Z | 2026-10-21T17:22:02Z |
| `@ccusage/ccusage-linux-x64`    | 2026-10-19T20:01:25Z | 2026-10-21T10:54:25Z | 2026-10-21T17:21:03Z |
| `@ccusage/ccusage-darwin-arm64` | 2026-10-19T20:01:00Z | 2026-10-21T10:51:59Z | 2026-10-21T17:25:03Z |
| `@ccusage/ccusage-linux-arm64`  | 2026-10-19T20:01:17Z | 2026-10-21T10:49:01Z | 2026-10-21T17:21:05Z |

`ccusage@20.0.38` declares all six platform packages at `20.0.38` under `optionalDependencies` (registry manifest, `dist.fileCount` 5, built by `scripts/ensure-native-binary.nu`). Every platform package has a 20.0.38 release today. Releases 20.0.39 to 20.0.45 all exist with their platform packages.

The failing run (measured with `gh run view 40087404553` and the jobs API): run created 2026-10-24T10:49:01Z, job `test (ubuntu-24.04, client)` step "Install statusline tools" ran 10:49:49Z to 10:49:54Z, step "Smoke-test statusline tools without network" failed at 10:49:58Z.

Reading: at 10:49:49Z on 2026-10-24, `ccusage@20.0.38` was 72 h old by seconds (published 10:49:51Z three days earlier, the install started at 10:49:49Z and resolved within the next five seconds), so the 72 h cutoff admitted it. `@ccusage/ccusage-linux-x64@20.0.38` was 4 min 34 s short of 72 h, so the same cutoff, passed to npm for transitive dependencies, excluded it. npm's documented rule for `optionalDependencies` is "proceed if it cannot be found or fails to install" ([package.json reference](https://docs.npmjs.com/cli/v11/configuring-npm/package-json#optionaldependencies)), so the install succeeded without the native binary, and the smoke test caught the missing binary. **Inferred:** the precise filter was mise's 72 h cutoff passed to npm, since the runner has no `~/.npmrc` from the repository (the CI job copies only `config.toml`, `test.yaml:259-261`). Either window gives the same result because 72 h equals 3 days.

So the class is not "published without a platform binary". It is: a release of several packages published minutes apart, met by a per-package release-age cutoff inside that skew window, where the late package is optional and therefore skipped without error. It recurs for any such tool on any job that starts in the skew window after the cutoff. The repository's smoke test is the right fail-closed guard. The pin's reason text is wrong and the hold could have been lifted on 2026-10-24T10:54:25Z.

`--omit=optional` is the opposite lever (it prevents optional dependencies from installing at all). npm has no flag that makes an optional dependency mandatory, so presence has to be checked after install, as the smoke test does. Proposal V4-8 corrects the reason, keeps the exact-pin policy for tools with native optional dependencies, and moves the check before the install.

### 4.4 mise pinning, `mise.lock`, `mise prune`, `latest`

Vendor statements ([Lockfile (mise.lock)](https://mise.jdx.dev/dev-tools/mise-lock.html), [Version requests](https://mise.jdx.dev/dev-tools/versions.html), [mise prune](https://mise.jdx.dev/cli/prune.html), [Dev tools](https://mise.jdx.dev/dev-tools/)):

- "`mise.lock` records the exact versions that the requests in `mise.toml` resolved to, with download URLs and checksums where the backend provides them. Commit it next to `mise.toml` so every machine and CI job installs the same tools." `mise install --locked` "fails instead of resolving a version when the lockfile has no matching entry". `lockfile = true` in a config file turns on automatic creation. Format version 2 locks npm and PyPI dependency graphs in `.mise/locks/`. `mise lock --bump` moves the lock within the requests, "For automated updates, run it on a schedule and open a pull request". `jdx/mise-action` "adds `--locked` itself when the repository has a `mise.lock`". "A version recorded in `mise.lock` installs even when it is newer than `minimum_release_age`". The page carries no experimental badge (only `mise deps` is marked experimental elsewhere), so in 2026 the lockfile is a documented, supported feature.
- Global config: "If `~/.config/mise/config.toml` is a symlink into a dotfiles repository ... Run `mise lock --global` from inside the repository to write `~/dotfiles/mise.lock`", and the global lockfile lives beside the global config.
- `latest`: "The release the tool's backend considers newest." Resolution order: lockfile entry, alias expansion, "If an installed version matches the request, mise uses it. A newly published release does not change your environment until you install or upgrade", then the backend. "Do not assume `latest` is the highest semantic version".
- `mise prune` "deletes installed versions that none of [the tracked configs] selects", `--dry-run` previews, and after `mise upgrade` the replaced version is pruned after `upgrade.prune_after`.
- `minimum_release_age` default is 24h for every backend, the repository's 72h overrides it.

Repository today: `home/dot_mise/config.toml` is the global config rendered to `~/.config/mise/config.toml`. Lines 3-43 request `latest` for node, rust, python, bun, chezmoi, claude-code, codex, sandbox-runtime and the rest. Held tools carry exact versions and a reason: ccstatusline 2.2.32 (line 26-27), ccusage 20.0.37 (28-29), prettier 3.9.10 (32-33), pnpm 12.8.1 (34-36), and the `http:` tools bats 1.14.0, gcloud 590.0.0, shellcheck 0.11.0, shfmt 3.14.1, ruff 0.17.2 with per-platform sha256 (46-103). No `mise.lock` exists (glob on 2026-10-28). CI copies the config into `RUNNER_TEMP/statusline-mise/mise.toml` and installs from the copy (`test.yaml:259-279`), so CI resolves every `latest` fresh on each run, while a host reuses its installed match until `make update`. The comments say "as hosts get it" (`test.yaml:267`, `:277`), which holds for the cutoff but not for the resolved version (**inferred** from the resolution order above).

Gaps:

1. CI and hosts can run different versions of every `latest` tool on the same day. A lockfile is the vendor's answer, with `mise lock --bump` on a schedule as the update path. The complication is that the config is chezmoi-managed: a `mise.lock` beside it would be rewritten by `mise upgrade` on the host, which chezmoi then reports as drift, unless the lockfile is itself the source of truth and hosts never upgrade outside a PR. That is a workflow change for the operator, not a CI fix. Proposal V4-9 is an evaluation unit with a measured `mise lock --global --dry-run` output, not an adoption.
2. The `http:` pins are already lockfile-equivalent (exact version, URL and sha256 per platform), which is why U97 could make them the one reviewed pin for hosts and CI.

## 5. git 2.55 and 2.56

Release notes read from the git repository ([2.55.0](https://github.com/git/git/blob/master/Documentation/RelNotes/2.55.0.adoc), released 2026-06-29, and [2.56.0](https://github.com/git/git/blob/master/Documentation/RelNotes/2.56.0.adoc), released 2026-09-28, dates from the git-scm.com manual page headers).

2.55, relevant lines:

- "`git maintenance` that goes background did not use the lockfile to prevent multiple maintenance processes from running at the same time, which has been corrected (ps/maintenance-daemonize-lockfix)." This is the change behind U100: since 2.55 the detached maintenance holds `.git/objects/maintenance.lock`, which `tests/unit/scratch_git.py:4-10` cites and measured ("after three commits the lock was there in 187 of 200 fresh repositories, and in none with maintenance.auto=false").
- "The fsmonitor daemon has been implemented for Linux." Relevant to U101's `-c core.fsmonitor=false` on the index read: a Linux host can now run the daemon too, so the P3 channel exists on both platforms.
- "`git ls-files --modified` and `git ls-files --deleted` have been optimized to filter with pathspec before calling lstat()". No behavioural change for U101's listing.
- "`git config foo.bar=baz` ... Give advice when giving an error message." No exit-code change.

2.56, relevant lines:

- "Various tests in `t7900-maintenance.sh` have been updated to use a throwaway repository, and auto-detaching of maintenance tasks is now disabled for these tests to fix flaky races with concurrent background maintenance jobs (ps/t7900-deflake-maintenance)." Upstream met the U100 race in its own suite and closed it with `maintenance.autoDetach=false`, one of the four settings `scratch_git.py:12-16` applies. Vendor confirmation of the mechanism.
- "Configuration file locking has been updated to retry for a short period, avoiding failures when multiple processes attempt to update the configuration simultaneously."
- "The `[includeIf "condition"]` conditional inclusion facility for configuration files has been taught to use the location of the worktree in its condition." One more config channel of the P3 kind, already neutralised by `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1` in U101's design.
- "`git maintenance` triggered `rerere gc` in unappropriate times and interfered with `git rebase` etc. too much. The conditions `rerere gc` gets triggered have been tweaked."
- Option parsing "has been updated to exit with 0 (instead of 129) when the help option is requested directly". Not a `git config` read path.
- Nothing changes `git config` exit codes.

`git config` exit codes ([git-config, 2.56.0](https://git-scm.com/docs/git-config)): "The section or key is invalid (ret=1), no section or name was provided (ret=2), the config file is invalid (ret=3), the config file cannot be written (ret=4), you try to unset an option which does not exist (ret=5), you try to unset/set an option for which multiple lines match (ret=5), or you try to use an invalid regexp (ret=6)." `get` "Returns error code 1 if key is not present." "If the repository configuration file is missing or unreadable, `git config` will exit with a non-zero error code." So the Codex finding on U101 (exit 3 read as unset) was a real misread: 3 means the config file is invalid, which the round-10 fix now refuses by name (handoff `01-program-status.md`, round 10).

`git maintenance` ([manual, 2.56.0](https://git-scm.com/docs/git-maintenance)): `register` "will also disable foreground maintenance by setting `maintenance.auto = false`", and by default "only `maintenance.gc.enabled` is true".

Repository today: `tests/unit/scratch_git.py:12-27` sets `maintenance.auto=false`, `maintenance.autoDetach=false`, `gc.autoDetach=false`, `gc.auto=0` through `GIT_CONFIG_COUNT` triples and writes them into each scratch repository's own config (`git_init`, `git_clone`, `quiet_repository`). `scripts/ci/unittest-shards.py:11-13` and `:118` pass `quiet_git_env` to every shard. The U100 verdict confirms an AST sweep over call sites.

Verdict: U100 matches the mechanism upstream itself chose in 2.56, and goes further (no maintenance at all in scratch repositories, where that is correct). No proposal.

## 6. chezmoi externals and U96

Vendor statements ([.chezmoiexternal format](https://www.chezmoi.io/reference/special-files/chezmoiexternal-format/), [global flags](https://www.chezmoi.io/reference/command-line-flags/global/), [configuration variables](https://www.chezmoi.io/reference/configuration-file/variables/)):

- "For `file` and `archive` externals, chezmoi will cache downloaded URLs. The optional duration `refreshPeriod` field specifies how often chezmoi will re-download the URL. The default is zero meaning that chezmoi will never re-download unless forced." Suggested periods 24h, 168h, 672h.
- Checksum fields: `checksum.sha256`, `checksum.sha384`, `checksum.sha512`, `checksum.size`. "If any of the optional `checksum.sha256`, `checksum.sha384`, or `checksum.sha512` fields are set, chezmoi will verify that the downloaded data has the given checksum."
- `urls`: "Extra URLs to try, in order ... the first URL that succeeds is used."
- `-R, --refresh-externals [always|auto|never]`: `auto` (the default) re-downloads only when older than the refresh period, `never` downloads "only if no cached external is available".
- `cacheDir` is the one cache setting. The configuration reference lists no retry count, retry delay, HTTP timeout or minimum speed for externals, and the flags page lists only `--progress`. A grep of both pages for "retry", "retries" and "timeout" finds nothing about externals.

Repository today:

- `home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl:7-38`: every archive external has `checksum.sha256` and `refreshPeriod: "720h"`.
- `scripts/lib/chezmoi-externals.sh:8-17` (copied into `setup.sh:276-...`, kept equal by `tests/unit/test_chezmoi_externals.py`): chezmoi keeps the cache in `<cacheDir>/external/<sha256 of the URL>` "(chezmoi 2.73.3 internal/chezmoi/sourcestate.go:1921-1942)", a dropped transfer "surfaces as a bare `chezmoi: unexpected EOF` ... and nothing retries it". `prefetch_chezmoi_externals` downloads each single-URL http(s) external with `curl --connect-timeout 30 --speed-limit 1024 --speed-time 60 --max-time 900` (lines 103-106), retries an allowlist of transient failures, verifies the sha256 before writing the cache entry, and leaves `urls` externals to chezmoi (decisions row `treadmill-u96-fallback`). `Makefile:121-122` runs it before `chezmoi apply`. CI applies with `--refresh-externals=never --exclude=scripts,externals` (`test.yaml:495-496`, `scripts/apply-check.sh:146-148`).

Is U96 the vendor-recommended approach? No. chezmoi documents no retry, no timeout and no prefetch hook, so the vendor's levers are exactly the ones the repository already uses in the declarations (checksums, refresh period, `urls`). U96 adds a layer that chezmoi does not describe, keyed on a cache layout read from one version's source. That is a reasonable engineering answer to "nothing retries it", and the U96 verdict confirms it is correct for 2.73.3. The risk is silent decoupling: CI and `setup.sh` install "the newest release at least 72 hours old" (`test.yaml:200-204`), so the chezmoi version floats while the prefetch's assumption about `<cacheDir>/external/<sha256 of the URL>` is fixed. If a chezmoi release moves or re-keys the cache, the prefetch still exits 0, chezmoi downloads again without retry, and the EOF class returns without any test going red.

Proposal V4-10 adds a check that the prefetch is actually consumed: after the prefetch, run chezmoi against the externals under a network-denied sandbox (the repository already has `unshare --net` and `sandbox-exec` patterns in `test.yaml:385-394`) and fail when chezmoi reaches for the network. A filed upstream feature request for retry and timeout settings is the vendor-aligned long-term path and is noted, not specified.

## 7. Proposed units

Each proposal is one unit and one PR, in the brief grammar the handoff uses. Line references are at 65f630b6.

### V4-1 Record the next image retirement conditions

- GOAL: the store names, before anyone has to re-derive it, what ends the current image choices.
- SCOPE: one `decisions.tsv` row by the coordinator and one line in the drift-watch tracking issue body template if it has one (`scripts/drift-watch.py`, read-only check first). No workflow change.
- CHANGE: the row states: macos-14 retired 2026-11-02 (#13518), `macos-15` is the next label the two-GA policy deprecates once a macOS 27 image is GA (inferred, no date), `ubuntu-24.04` stays supported with `ubuntu-latest` moving to 26.04 by 2026-11-19 (#14748), the `ubuntu-26.04` canary (`test.yaml:42-50`) is promoted when it is green for two consecutive weeks after #14823 closes.
- ACCEPTANCE: the row exists, the drift watch run after it still exits 0 or 3, nothing else changes.
- VERIFY: `make drift` locally.

### V4-2 Bound every apt call and record the mirror re-check

- GOAL: a silent apt call (the #15040 class, on the public archive after the drop) is cut and named inside its step, not by the 45 minute job cancel, and the repository knows when to retire the drop.
- SCOPE: `.github/workflows/test.yaml` (lines 191, 450, 536), `ubuntu.yaml` and `remote.yaml` and `private-bootstrap.yaml` only through `setup.sh`'s installers (`install/ubuntu/**`, which U99 already bounded for curl and wget), `tests/unit/test_apt_mirror.py`, `scripts/ci/drop-azure-apt-mirror.py` docstring.
- CHANGE: (1) every workflow `apt-get update` and `apt-get install` line runs as `timeout --kill-after=10 <N> sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 ...` with `N` measured per step from passing logs plus margin, and the "Install tools" and "Run Python unit tests" steps get `timeout-minutes` equal to the sum of their bounds plus margin. (2) `tests/unit/test_apt_mirror.py` gains a rule, in the closed-world style of the U99 scanner, that every `apt-get` token in a workflow `run:` sits on a line that carries the exact bound form or is in an exemption table with a reason. (3) The drop script's docstring and the `decisions.tsv` row name the re-check: when #14823 is closed, measure three `test (ubuntu-24.04, client)` runs with the drop disabled and retire it if none stalls.
- ACCEPTANCE: the new test fails before and passes after, `BoundOrderTest` still passes with the new step bounds, one passing run per Ubuntu row in the PR body with the step times.
- VERIFY: `uv run --no-project python -m unittest tests.unit.test_apt_mirror`, ShellCheck 0.11.0 and `shfmt -i 4 -sr -d` on nothing (YAML only) or on any touched installer.
- FORBIDDEN: no change to `run-bats.py`'s bound, no caching of apt archives.

### V4-3 Concurrency groups for the three remaining workflows

- GOAL: two pushes to main cannot run two benchmark pushes at once, and a pull request's newer head cancels its older bootstrap run on the macOS and Ubuntu install workflows.
- SCOPE: `.github/workflows/macos.yaml`, `ubuntu.yaml`, `private-bootstrap.yaml`, `tests/unit/test_workflow_orchestration_skip.py` if it pins the concurrency text of the other workflows (check with `grep -n cancel-in-progress tests/unit/`).
- CHANGE: `macos.yaml` and `ubuntu.yaml` get the exact block of `test.yaml:17-19` (PR head cancels, main grouped by sha, never cancelled). `private-bootstrap.yaml` runs only on push, schedule and dispatch, so it gets `group: private-bootstrap-${{ github.sha }}` with `cancel-in-progress: false`. For the benchmark push, `macos.yaml` additionally gets a job-level `concurrency` on `build` with the fixed group `macos-benchmark` and `cancel-in-progress: false`, so main runs queue behind each other, as the docs describe for a shared resource.
- ACCEPTANCE: `actionlint` or the repository's workflow test passes, one run of each workflow green, the PR body quotes the docs sentence on `concurrency` and the `max-parallel: 1` comment at `macos.yaml:61-65` is updated to name the run-level group.
- VERIFY: the unit tests that read the workflows, `gh run list` for the three workflows after merge.

### V4-4 Evaluate the workflow lockfile and triage the two Dependabot PRs

- GOAL: decide, with measured output, whether `.github/workflows/actions.lock` replaces or supplements the SHA pins, and land or close #548 and #549.
- SCOPE: a scratch branch for `gh actions-lock` output (no commit of the lockfile in this unit), a `decisions.tsv` row, the two Dependabot PRs as separate units if adopted (the handoff already says each pin bump is a unit).
- CHANGE: run `gh actions-lock` on a scratch checkout and paste the generated lockfile in the PR body or decisions row with the transitive dependencies it found that the SHA pins do not cover. Record the preview status ("subject to change") and the plan availability (Free plans since 2026-10-14). For #549 (mise-action 4.3.0 to 5.2.2, a major), read the mise-action README for the v5 input changes (the README on 2026-10-28 documents `minimum_release_age`, `cache_restore_retry_budget`, `cache_save_retry_budget`, `auto_update`) and name which inputs the three call sites need.
- ACCEPTANCE: a decision row with adopt, defer or reject and the evidence, and both Dependabot PRs moved out of untriaged (merged through a unit or closed with a reason).
- VERIFY: none in CI for the evaluation, the normal CI for any adopted bump.

### V4-5 Keep `regime` running past 2026-12-02

- GOAL: the `pull_request_target` check does not silently stop when GitHub enforces the default event policy on public repositories.
- SCOPE: an operator step (repository admin) creating an Actions event policy that allows `pull_request_target` for this repository, a `gates.md` row, and a unit test asserting the workflow's safety invariants so the policy allowance is backed by code.
- CHANGE: (1) the operator creates the policy before 2026-12-02 through the repository's Actions settings or the policies REST API (the docs page links both), and records the date in `gates.md`. (2) `tests/unit/test_workflow_orchestration_skip.py` or a new `tests/unit/test_regime_workflow.py` asserts for `regime.yml`: the trigger is `pull_request_target` with `branches: [main]`, `permissions` is exactly `contents: read`, every `actions/checkout` step has `ref: refs/heads/${{ github.base_ref }}` and `persist-credentials: false`, no step contains `allow-unsafe-pr-checkout`, the only fetch of the head is into `refs/regime/pr-head`, and `PR_BODY` reaches the script through `env:` and never inside `run:` text.
- ACCEPTANCE: the test fails on a copy of the workflow with `ref:` removed and passes on the real one, the gates row names the policy and its date.
- VERIFY: `uv run --no-project --with pyyaml python -m unittest tests.unit.test_regime_workflow`.

### V4-6 One Bats for hosts and CI

- GOAL: every CI job and every host runs Bats 1.14.0 from the one reviewed pin, as U97 did for ShellCheck and shfmt, so the 1.14.0 `run` and `set -e` change cannot pass locally and fail in CI or the reverse.
- SCOPE: `.github/workflows/test.yaml` (lines 187 and 191 lose `bats-core` and `bats`), `macos.yaml:174`, `ubuntu.yaml:129-135` (the dead comment block is removed), `scripts/ci/install-pinned-lint-tools.sh` (accept `bats` as a third tool, `http:bats`), `scripts/ci/pinned-tool-version.sh` (accept `bats`, prefix `Bats `), `scripts/run_unit_test.sh:19-22` (the rationale keeps #1020 for hosts without the pin and drops the 1.10.0 clause once CI no longer meets it), `tests/unit/test_pinned_lint_tools.py`.
- CHANGE: the "Put the pinned ShellCheck and shfmt on PATH" step (`test.yaml:400-407`) becomes "Put the pinned ShellCheck, shfmt and Bats on PATH", and `run_bats` refuses any other Bats version through `pinned-tool-version.sh` before it runs. The files-test steps in `macos.yaml` and `ubuntu.yaml` install Bats the same way (they already run mise-action with `install: true`).
- ACCEPTANCE: every `Run unit test` and `Test file existence` log prints `Bats 1.14.0`, the bats-core brew and apt installs are gone from the workflows, the unit tests pass under 1.14.0 on all three images (a failure here is the skew made visible and is fixed in the same unit, in the test, never by relaxing the pin).
- VERIFY: `scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml bats shellcheck shfmt`, CI on all rows.

### V4-7 Timing and summary from the Bats wrapper

- GOAL: the slowest test of every run is readable from the log without hand measurement, and a stalled test's name and diagnosis appear on the run summary page.
- SCOPE: `scripts/ci/run-bats.py`, `scripts/run_unit_test.sh` (pass `--timing`), `tests/unit/test_apt_mirror.py` (the budget constants gain a comment pointing at the timing lines, no value change), `tests/unit/test_run_bats.py` if it exists (check with `ls tests/unit | grep -i bats`).
- CHANGE: (1) `run_bats` passes `--timing`. (2) The wrapper parses the duration suffix Bats 1.14.0 prints on each result line in the `cat` stream (measure the exact form on one run first and pin it in a test fixture), keeps the maximum, and prints `slowest: <n> <name> <ms>` after the plan. (3) When `GITHUB_STEP_SUMMARY` is set, the wrapper appends the `not ok ... # timeout` line and the diagnosis block to it, and on success appends the slowest line. Nothing else changes, the wrapper still signals nothing.
- ACCEPTANCE: a test feeds a recorded `cat` stream with timing suffixes and a synthetic stall and asserts stdout, exit 124 and the summary file content, one CI run shows the slowest line on the summary page.
- VERIFY: `uv run --no-project python -m unittest tests.unit.test_run_bats tests.unit.test_apt_mirror`.

### V4-8 Cooldown skew for multi-package npm tools

- GOAL: a release whose platform package is published minutes after its meta package cannot install without the binary on a job that starts inside the skew, and the held pins state the measured cause.
- SCOPE: `home/dot_mise/config.toml:26-29` (reason text), `scripts/check-statusline-tools.py` or the "Install statusline tools" step in `test.yaml:272-279`, `tests/unit/test_statusline_tools.py`, `scripts/upgrade-tools.sh:328-343` (reuse `npm_release_age_verdict`, do not duplicate it).
- CHANGE: (1) the two Held reasons name the facts: `ccusage@20.0.38` published 2026-10-21T10:49:51Z, its linux-x64 package 10:54:25Z, the install at 2026-10-24T10:49:49Z fell between the two cutoffs, npm skipped the optional package, and the hold is a policy for tools with native optional dependencies, not a wait for a fixed release. (2) Before `mise install npm:ccusage` and `npm:ccstatusline`, a check reads `npm view <pkg>@<version> optionalDependencies time --json` and refuses to install a version whose platform package for the runner (`os`/`cpu` named in the package) is younger than the window plus the U89 60 s margin, printing the two timestamps. The check is the same strict reader as U89 (every unparsable answer is a refusal). (3) The smoke test keeps failing when the binary is missing, as the last guard.
- ACCEPTANCE: a unit test with a frozen clock at 2026-10-24T10:49:49Z and the recorded registry `time` maps reproduces the refusal, and passes at 10:54:26Z, CI green with the current pins.
- VERIFY: `uv run --no-project python -m unittest tests.unit.test_statusline_tools`, ShellCheck 0.11.0 and `shfmt -i 4 -sr -d` on any touched shell.
- FORBIDDEN: no `min-release-age-exclude`, no `--omit=optional`, no change to the 72 h windows.

### V4-9 Evaluate `mise.lock` for the global config

- GOAL: decide whether CI and hosts should install the versions one committed lockfile records, instead of each resolving `latest` on its own clock.
- SCOPE: a `decisions.tsv` row and a PR body, no lockfile committed in this unit.
- CHANGE: run `mise lock --global --dry-run` from the repository checkout (per the lockfile docs' dotfiles section) and paste the result, then answer in the row: where the lockfile lives under chezmoi (the rendered `~/.config/mise/mise.lock` would be rewritten by host upgrades and show as chezmoi drift), whether `make update` becomes `mise lock --bump` in a PR followed by `mise install --locked` on hosts, how the CI copy step (`test.yaml:259-261`) carries the lockfile and `.mise/locks/`, and whether `package_manager = "npm"` (no dependency graph) or the embedded aube installer (graph recorded) is wanted. Note that a locked version bypasses `minimum_release_age` (docs), so the 72 h policy moves to the bump schedule.
- ACCEPTANCE: a row with adopt, defer or reject and the measured output.
- VERIFY: none beyond the dry run.

### V4-10 Prove the prefetch is consumed

- GOAL: a chezmoi release that changes its externals cache layout turns the U96 prefetch into a visible failure instead of a silent return to the EOF class.
- SCOPE: `scripts/lib/chezmoi-externals.sh` (and its copy in `setup.sh`, kept equal by `tests/unit/test_chezmoi_externals.py`), `Makefile:121-123`, `.github/workflows/remote.yaml` bootstrap step, `tests/unit/test_chezmoi_externals.py`.
- CHANGE: after `prefetch_chezmoi_externals`, a new function runs `chezmoi --refresh-externals=never status` on the externals only, under the network-denied form the repository already uses (`unshare --net` on Linux, `sandbox-exec` with `(deny network*)` on macOS, `test.yaml:385-394`), and fails with a one-line reason when chezmoi exits non-zero or prints `unexpected EOF`, `dial`, or `Get "http` (a closed list, in a table). The function also records the chezmoi version it ran under in its output so the log names the version a layout change arrived with.
- ACCEPTANCE: a fixture test with a stub chezmoi that ignores the cache reproduces the failure, the real check passes on both bootstrap rows, the PR body states that chezmoi documents no retry or timeout setting (link to the two reference pages) and that the prefetch is therefore repository-specific.
- VERIFY: `uv run --no-project python -m unittest tests.unit.test_chezmoi_externals`, ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, `scripts/ci/masked-dirname-check.sh`.

### V4-11 and V4-12 (not proposed)

Two items were considered and rejected: an apt archive cache (section 2.3, it would test the cache instead of the install) and `bats --jobs` (section 3.3, the install tests share the machine). They are listed so the next reader does not re-open them without new evidence.

## 8. Sources

All read on 2026-10-28 (JST).

Runner images:

- https://github.com/actions/runner-images/issues/13518
- https://github.blog/changelog/2026-10-01-github-actions-macos-14-runner-image-retirement
- https://github.com/actions/runner-images/issues/14167
- https://github.blog/changelog/2026-05-14-github-actions-upcoming-image-migrations/
- https://github.com/actions/runner-images#available-images
- https://github.com/actions/runner-images/issues/14747
- https://github.com/actions/runner-images/issues/14748
- https://github.blog/changelog/2026-09-17-ubuntu-26-generally-available-and-latest-migration/
- https://github.com/actions/runner-images/issues/14254
- https://github.com/actions/runner-images/issues/14823
- https://github.com/actions/runner-images/issues/15040
- https://github.com/actions/runner-images/issues/15142
- https://github.com/actions/runner-images/labels/Announcement
- https://github.com/actions/runner-images/issues/14856, /14745, /14818, /14826, /15018

GitHub Actions docs and the incident:

- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
- https://github.com/actions/cache
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles
- https://github.blog/changelog/2026-10-14-github-actions-workflow-lockfiles-in-public-preview
- https://github.com/advisories/GHSA-mrrh-fwg8-r2c3
- https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions
- https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference
- https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#adding-a-job-summary
- https://github.com/jdx/mise-action

Bats:

- https://bats-core.readthedocs.io/en/stable/usage.html
- https://bats-core.readthedocs.io/en/stable/writing-tests.html
- https://github.com/bats-core/bats-core/blob/master/docs/CHANGELOG.md
- https://github.com/bats-core/bats-core/issues/1020
- https://github.com/bats-core/bats-core/issues/1206

npm and mise:

- https://github.com/npm/cli/releases/tag/v11.10.0
- https://docs.npmjs.com/cli/v11/using-npm/config
- https://docs.npmjs.com/cli/v11/commands/npm-ci
- https://docs.npmjs.com/cli/v11/configuring-npm/package-json#optionaldependencies
- https://registry.npmjs.org/ccusage, https://registry.npmjs.org/@ccusage%2Fccusage-linux-x64, the darwin-arm64 and linux-arm64 packages (the `time` maps)
- https://mise.jdx.dev/dev-tools/mise-lock.html
- https://mise.jdx.dev/dev-tools/versions.html
- https://mise.jdx.dev/dev-tools/
- https://mise.jdx.dev/cli/prune.html
- https://mise.jdx.dev/configuration/settings.html#minimum_release_age
- https://mise.jdx.dev/dev-tools/backends/npm.html

git:

- https://github.com/git/git/blob/master/Documentation/RelNotes/2.55.0.adoc
- https://github.com/git/git/blob/master/Documentation/RelNotes/2.56.0.adoc
- https://git-scm.com/docs/git-config
- https://git-scm.com/docs/git-maintenance

chezmoi:

- https://www.chezmoi.io/reference/special-files/chezmoiexternal-format/
- https://www.chezmoi.io/reference/command-line-flags/global/
- https://www.chezmoi.io/reference/configuration-file/variables/

Repository files read (all at 65f630b6): `.github/workflows/*.yaml` and `*.yml`, `.github/dependabot.yml`, `scripts/ci/run-bats.py`, `scripts/ci/drop-azure-apt-mirror.py`, `scripts/ci/install-pinned-lint-tools.sh`, `scripts/ci/pinned-tool-version.sh`, `scripts/ci/unittest-shards.py`, `scripts/run_unit_test.sh`, `scripts/lib/chezmoi-externals.sh`, `scripts/lib/github-release.sh`, `scripts/upgrade-tools.sh`, `scripts/update-agent-assets.sh`, `scripts/apply-check.sh`, `tests/unit/scratch_git.py`, `tests/unit/test_apt_mirror.py`, `home/dot_mise/config.toml`, `home/dot_npmrc`, `home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl`, `Makefile`, and the store's `units.tsv`, `ledger.tsv`, `decisions.tsv`, `verdicts/U96-e677eabf.md`, `verdicts/U100-39268743.md`. Measured with `gh`: repository visibility, open Dependabot PRs, run 40087404553 and job 120853039189 timings.
