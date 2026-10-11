# Report: dotfiles-T119-rolling-release-assets-a01

- Worker: `claude-standard-dot-a001` (Claude Code, `standard`), worktree `.claude/worktrees/worker-c`
- Branch: `feat/rolling-release-assets` from `origin/main` `8d719629`
- PR: #312, head `36d87f6cf081f0de28f7a1f2cf93b894109a135d` (round 6; unchanged since round 5, which this round only documents). Commits:
  - f688336c: the change.
  - 50afc9b5: CI shellcheck 0.9.0 SC2015.
  - 89d9b982: Bot threads on f688336c.
  - 7903de38: ruff format.
  - 3cbcf388: Bot threads on 7903de38 — a patched gh, the token bound to github.com, whole release lists, AWS checked before a cache hit, precise pin reasons.
  - fd4ff82d: the update-branch merge by the orchestrator (main moved by #311).
  - 0d264db8: revise round 1, Bot threads on fd4ff82d — the credential out of xtrace, the broken same-version AWS CLI repaired.
  - 2453b1c9: revise round 2, the audit of 0d264db8 — release tags validated at the source and `make docker` without interpolation, exit-status-aware version probes, mise GPG at bootstrap and deferred attestations.
  - aa69c2a0: Amendment 7 and the Bot review of 2453b1c9 — Crit and starship pinned again, CI's mise cooled down, a self-updated Zed kept, the cleanup test's GPG stub.
  - f3c155ee: the Bot review of aa69c2a0 — attestation checks use mise's gh before an older system gh.
  - 674aaac0: the Bot review of f3c155ee — the staged AWS CLI must be the active one, and a failed Zed download keeps the installed Zed.
  - 19504fe5: revise round 3, the audit of 674aaac0 — chezmoi verified by attestation in CI and by `make docker` on the host, and the acquisition rule for starship, the AWS CLI and sheldon.
  - 16a64632: the CI failure of 19504fe5 — `install_sheldon` keeps cargo's own failure status.
  - e0fed47e: the CI failure of 16a64632 — the starship acquisition test gets a `sha256sum` on the macOS runner.
  - 8cb8a1d1: the Bot review of e0fed47e — unverified Docker images rebuilt, rolling assets need an independent check, the wgetrc trapped.
  - 73034ae4: the Bot review of 8cb8a1d1 — only a stable gh 2.93.0 or newer runs attestations.
  - 96253ea3: revise round 4, the audit of 73034ae4 — gh's verification report kept off the attestation helper's stdout.
  - 70361875: the Bot review of 96253ea3 — only a working AWS CLI stays when the archive is unreachable.
  - 50759078: Amendment 8 (the Bot review of 70361875) — no bootstrap binary runs before an independent check; reviewed fallback releases; the deferral retired.
  - 36d87f6c: the Bot review of 50759078 — Enterprise tokens kept off github.com, a newer mise kept on the fallback path, and gh's attestation as the check when mise's GPG inputs cannot be fetched.
- CI: 17/17 checks pass on 36d87f6c (validation §9), as on 73034ae4, 96253ea3, 70361875 and 50759078. All four `test` jobs verify chezmoi's GitHub release attestation in the chezmoi step. The three public-bootstrap jobs take the gh-ready path: `gpgv: Good signature` for mise's `SHASUMS256.asc` and `✓ Verification succeeded!` for mise and chezmoi before they run, with no fallback line (§15d). 19504fe5 and 16a64632 failed CI; both failures are fixed (§14d).
- Bot: the Codex Code Review of 36d87f6 completed at 2026-10-10T08:00:00Z with no review and no inline comment, and the connector reacted 👍, its sign that all reviews finished with no findings. Rechecked right before the RESULT (validation §10). All twenty-five Bot threads, raised on f688336c, 7903de38, fd4ff82d, 2453b1c9, aa69c2a0, f3c155ee, e0fed47e, 8cb8a1d1, 96253ea3, 70361875 and 50759078, are fixed at their root cause and named in the RESULT. The orchestrator resolved the first seven in round 1 and reported verifying and resolving seven interim threads in round 3. This seat cannot read resolution state (the gate refused `gh api graphql`) and resolves no thread.
- Status: ready_for_review

## What changed

**The rule (as corrected by Amendments 7 and 8).** Nothing an installer fetches runs before a verification independent of the release page has passed. A release asset resolves its newest release at install time only when its publisher provides such a verification and it can run before execution: a GitHub release attestation, a signature with a key whose fingerprint the manifest pins, or an immutable registry with its own index checksums. A checksum file from the same mutable release verifies the download, not the publisher, so it is only ever a second check. A GitHub release is the newest one that is not a draft or a prerelease and was published at least 72 hours ago (Amendment 1). That is the same window as `minimum_release_age` in `home/dot_mise/config.toml`, so a fresh bootstrap never installs a mise that `mise self-update` would refuse. Every other component keeps a reviewed pin with its sha256, and its `reason` says why. Where the check needs a tool a fresh host may lack (gh for mise's and chezmoi's attestations, gpg for mise's signature), the bootstrap installs a reviewed `fallback` release instead (Amendment 8).

| Asset                                             | Release                                                                                                                              | Mechanism, or reason for the pin                                                                                                                                                                                      |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mise bootstrap                                    | newest ≥ 72 h when gpg or an authenticated gh can verify it before it runs; otherwise the reviewed fallback v2026.10.3 (Amendment 8) | `SHASUMS256.asc` checked against the pinned release key, or the GitHub release attestation; the fallback's reviewed sha256 per platform; `SHASUMS256.txt` on every path                                               |
| chezmoi bootstrap                                 | newest ≥ 72 h when an authenticated gh can verify it before it runs; otherwise the reviewed fallback v2.73.0 (Amendment 8)           | the GitHub release attestation, or the fallback's reviewed sha256 per platform (its cosign signature needs cosign); the checksums file on every path. CI's chezmoi and `make docker` verify the attestation (round 3) |
| starship                                          | pinned v1.26.0 + sha256 (Amendment 7)                                                                                                | mutable releases with only `.sha256` sidecars (immutable=false, attestations 404): the reviewed sha256, then the sidecar                                                                                              |
| Crit                                              | pinned v0.22.0 + four sha256 (Amendment 7)                                                                                           | mutable releases with only `checksums.txt` (immutable=false, attestations 404): the reviewed sha256, then `checksums.txt`                                                                                             |
| Zed                                               | newest ≥ 72 h                                                                                                                        | the GitHub release attestation (in-toto release predicate) through `gh release verify-asset`, required: Zed publishes nothing else                                                                                    |
| sheldon                                           | newest crate                                                                                                                         | `cargo install --locked` against the crates.io index; no age choice                                                                                                                                                   |
| AWS CLI                                           | AWS's current archive                                                                                                                | AWS's GPG signature with the pinned key fingerprint; no age choice                                                                                                                                                    |
| Homebrew installer, Understand-Anything installer | pinned commit + sha256                                                                                                               | unsigned scripts, no checksum, no release                                                                                                                                                                             |
| tode, terminal-browser                            | pinned script + sha256                                                                                                               | zenbu-labs publishes tarball releases with no checksum file or attestation, and the `curl \| bash` scripts are unsigned; each script embeds and checks its payload sha256, so the script hash pins the payload too    |
| agmsg                                             | pinned tag, commit, archive sha256                                                                                                   | tags without release assets, checksums or attestations; the npm package's SLSA provenance covers only the `npx` bootstrapper                                                                                          |

**Pieces**

- `scripts/lib/github-release.sh` is new, with four functions:
  - `github_release_tag` reads the releases API (`?per_page=30`) through curl or wget. It parses the pretty-printed top-level fields with awk, so it needs no jq or Python. It returns only a tag matching `GITHUB_RELEASE_TAG_PATTERN` and fails with `unexpected release tag <tag> for <repo>` otherwise (round 2).
  - `github_release_list` authenticates with `GITHUB_TOKEN`, `GH_TOKEN` or `gh auth token --hostname github.com` when one is available (github.com only, after Bot thread 4235134122). The credential reaches curl on stdin (`-K -`) or wget through a private 0600 wgetrc (after Bot thread 4234992752), never the command line.
  - `github_release_attestation` runs `gh release verify-asset <tag> <file> --repo github.com/<repo>`. It returns 2, so each installer decides whether that is fatal, when `gh` is absent, not logged in to github.com (`gh auth status --hostname github.com`), or older than 2.93.0; for an older `gh` it prints why (GHSA-8xvp-7hj6-mcj9, after Bot thread 4235134105).
  - `github_release_verified_sha256` (round 3) downloads an asset and its checksum file, checks both and the attestation, and prints only the sha256 (round 4). Round 2's `github_release_defer_attestation` was retired by Amendment 8.
- `setup.sh` runs before the repository exists, so it carries a byte-identical copy between markers. `tests/unit/test_github_release.py` keeps the copy equal.
- The installers:
  - `install/common/mise.sh` and `setup.sh` (chezmoi) choose before downloading (Amendment 8).
    - With a check that can run before execution (gpg with the pinned key for mise; an authenticated stable gh for both), they resolve the newest cooled-down tag through the helper and verify it that way.
    - Otherwise they install the reviewed fallback (`MISE_FALLBACK_*` and `CHEZMOI_FALLBACK_*`, rendered from `assets.<name>.fallback`) and check it against its reviewed sha256.
    - The release's checksum file is checked on every path.
  - `install/ubuntu/server/starship.sh` installs the pinned release (`STARSHIP_PIN_VERSION` and two sha256, rendered from `assets.starship`), checks the reviewed sha256 and then the `.sha256` sidecar (Amendment 7).
  - `scripts/update-agent-assets.sh#ensure_crit_cli` installs the pinned release (`CRIT_PIN_VERSION` and four sha256 in `installer-pins.sh`, rendered from `assets.crit`), checks the reviewed sha256 and then `checksums.txt`, and checks that the staged binary reports the pin (Amendment 7). An installed binary at the pin needs no network.
  - `install/common/sheldon.sh` drops `--version`.
  - `install/ubuntu/common/aws_cli.sh` takes the unversioned archive and keeps the GPG and fingerprint check. It accepts whatever version AWS serves, but since 674aaac0 the postcondition requires that staged version to be the active CLI.
- **Zed (Amendments 2 and 3):**
  - `install/ubuntu/client/zed.sh` verifies with `gh release verify-asset`. The release predicate is `https://in-toto.io/attestation/release/v0.2`, which `gh attestation verify`'s SLSA default does not check.
  - Without an authenticated `gh` it prints `zed not installed: run make gh-auth, then make update` (or `zed <v> stays`) and exits 0. A failed attestation is the only hard failure.
  - An unreachable API never fails the apply. Amendment 3 listed only the installed case; the not-installed case exits 0 too, because the script now runs on every apply and would otherwise fail every offline apply on a client that never had Zed.
  - `run_once_52-client-install-zed.sh.tmpl` became `run_after_05-client-install-zed.sh.tmpl`. It runs after `run_once_after_02-install-mise.sh.tmpl`, which installs `gh` (`github:cli/cli`), and on every apply, so the hint is true. `scripts/check-tools.sh` reports a missing Zed on Linux clients with the same hint.
- **Every-apply wrappers (Bot thread 4234992747, Amendment 6).**
  - starship, sheldon and the AWS CLI rendered no changing pin any more, so their `run_once` wrappers would never rerun. They are now `run_after_10-install-starship`, `run_after_03-install-sheldon` and `run_after_04-install-aws-cli`.
  - Each installer skips when it is current:
    - starship compares `starship --version` with the resolved tag;
    - sheldon compares `sheldon --version` with `cargo search sheldon --limit 1`;
    - the AWS CLI compares the archive's ETag (HEAD) with the one recorded under `${XDG_STATE_HOME:-~/.local/state}/dotfiles/aws-cli-archive.etag` after the last verified install.
  - Each keeps the installed tool with a warning when offline. The mise bootstrap stays `run_once_after_02`, because `mise self-update` (T118) moves it.
- **Manifest, validator, generator.**
  - Rolling assets carry `release: latest` and an optional `attestation: when-gh-authenticated`.
  - The validator rejects:
    - a rolling asset on a source that cannot roll;
    - a rolling asset that records a `pin`, `ref`, `ref_commit`, `sha256` or `reason`, or renders a version;
    - a pinned release asset without a `reason`;
    - an unknown `attestation` value.
  - `generate-agent-configs.py` needed no change: it renders only `render:` entries. AWS keeps one, the fingerprint.
  - `scripts/lib/installer-pins.sh` keeps the tode, terminal-browser and (since Amendment 7) Crit pins; starship's render into its installer.
- **Elsewhere (Amendment 1):**
  - The four workflows run `jdx/mise-action` without `version`, with `minimum_release_age: 72h` since Amendment 7 (q12), so CI tests the mise a host can receive. Only `test.yaml`'s edited steps ran in this PR's CI: its `Setup mise for statusline smoke` and `Install tools` (the chezmoi step through the helper) passed in all four `test` jobs. The `macos.yaml` and `ubuntu.yaml` `build` jobs skip their mise step on a pull request, because the private integration is unavailable there, and `docs.yml` runs only on pushes to main, so those three edits first run after merge. No CI job runs actionlint.
  - `make docker` resolves the chezmoi tag through the helper, inside its recipe shell since round 2, so fetched text never becomes Make or shell source; `make -n docker` prints the resolving command and fetches nothing. The Dockerfile keeps the build arg.
  - The `test.yaml` chezmoi step resolves the tag through the helper. That job already exports `GITHUB_TOKEN` at job level, so the call is authenticated.
- The dead release-pin block in `scripts/upgrade-tools.sh` (`asset_manifest_pin`, `pick_windowed_pin`, `bump_release_asset_pins` and helpers, 140 lines) is deleted (Amendment 2). Its test is replaced by `tests/unit/test_github_release.py`; the old name no longer fits.
- README: the asset paragraph is rewritten to the rule, with a mechanism table and the pinned exceptions by name and reason. Two passages that became false are corrected (Amendment 5): the lifecycle note that the release assets keep pins until T119, and the Crit and zenbu-labs paragraphs.

## Research (validation §1)

- **mise:** `SHASUMS256.txt` (plus `.asc`/`.minisig`). Release attestation plus SLSA provenance.
- **chezmoi:** `checksums.txt` plus a sigstore bundle. Release attestations.
- **starship:** `.sha256` sidecars; no attestation.
- **crit:** `checksums.txt` (v0.21.1 and v0.22.0); no attestation.
- **zed:** release attestation only; no checksum file.
- **tode, terminal-browser:** `zenbu-labs/tode` and `zenbu-labs/terminal-browser` tarball releases; no checksum, no attestation (404).
- **agmsg:** no release assets; npm SLSA provenance for the bootstrapper.
- **Homebrew/install, Understand-Anything:** no releases.
- **AWS:** the unversioned archive and its `.sig` are served.
- **sheldon:** crates.io newest version.

## Scope changes, all amended by the orchestrator

- q1, Amendment 1: workflows, `make docker` and the Dockerfile.
- q2, Amendment 1: the 72-hour window.
- q3, Amendment 2: the dead block in `upgrade-tools.sh`.
- q4, Amendment 2: `gh release verify-asset`, and Zed exits 0 without an authenticated `gh`.
- q5, Amendment 3: one include line each in the mise and starship templates.
- q6, Amendment 3: Zed runs as `run_after_05`. The amendment-2 hint would have been false for a `run_once` script.
- q7, Amendment 4: `mise.bats`, `setup.bats`, `zed.bats`, `test_runtime_health.py`, `test_supply_chain_policy.py`.
- q8, Amendment 5: `check_tools.bats`.
- q9, Amendment 5: the README corrections.
- q10, Amendment 6: the three `run_after` wrappers and their skip logic.
- q11, Amendment 7: Bot 4236226700 — the task's rule corrected; Crit and starship pinned again.
- q12, Amendment 7: Bot 4236226697 — `minimum_release_age: 72h` on the four `mise-action` steps; Amendment 1's no-cooldown-in-CI withdrawn.

## Codex Bot threads

- **f688336c**, fixed in 89d9b982 (Amendment 6):
  - 4234992747 (P2): the rolling installers' `run_once` wrappers never rerun. The `run_after` wrappers above skip when current.
  - 4234992752 (P2): the wget fallback dropped the credential. It now goes through a private wgetrc.
  - 4234992757 (P2): a Zed or Crit binary that fails `--version` aborted the installer. The probes now treat it as not installed.
- **7903de38**, fixed in 3cbcf388:
  - 4235134105 (P1): `gh` 2.92.0 and earlier leak credentials to TUF mirrors in `gh release verify-asset` (GHSA-8xvp-7hj6-mcj9; advisory read: affected ≤ 2.92.0, patched 2.93.0). `github_attestation_ready` requires 2.93.0 and says so when it declines.
  - 4235134122 (P1): an unqualified `gh auth token` could send an Enterprise or `GH_HOST` credential to `api.github.com`. The helper now uses `--hostname github.com` for the token and the auth check, and `--repo github.com/<repo>`.
  - 4235134113 (P2): the AWS ETag cache hit trusted any executable. It now requires `verify_aws_cli_version`.
  - 4235134133 (P2): the parse relied on the caller's `pipefail`. The list is now fetched whole before parsing.
- **fd4ff82d**, fixed in 0d264db8 (Revise round 1):
  - 4235444419 (P1): the credential could show in an xtrace.
  - 4235444420 (P2): a broken same-version AWS CLI could not be repaired.
- **2453b1c9**, fixed in aa69c2a0 (Amendment 7):
  - 4236226700 (P1): a same-release `checksums.txt` is no trust anchor for mutable Crit releases. Crit is pinned again, with the reviewed sha256 first and `checksums.txt` second; starship, the same class, too.
  - 4236226692 (P1): the mise cleanup test faked `SHASUMS256.asc` while the runner has gpg. The fixture stubs `verify_mise_shasums_signature`.
  - 4236226697 (P2): CI's `mise-action` took the newest mise without the cooldown. All four steps set `minimum_release_age: 72h`.
  - 4236226689 (P2): Zed downgraded a Zed that had updated itself. An installed release at or past the resolved one stays, with one notice.
- **aa69c2a0**, fixed in f3c155ee:
  - 4236314005 (P2): with apt's older `gh` earlier on `PATH` than mise's shims, `github_attestation_ready` declined it, so Zed never installed. `github_attestation_ready` and `github_release_attestation` now put mise's shim directory first in a function-local `PATH`. That fixes the cause once for Zed, the upgrade-tools phase and both bootstraps. The caller's `PATH` is unchanged; `test_attestation_prefers_mise_gh_over_an_older_system_gh` fails against aa69c2a0's helper, which is identical to 2453b1c9's (validation §13k).
- **f3c155ee**, fixed in 674aaac0:
  - 4236358716 (P2): an interrupted AWS CLI update can leave the new version directory beside an older working CLI. Upstream `--update` skipped it, the version-agnostic postcondition accepted the older CLI, and `main` recorded the new ETag, so it was never repaired. The same-version directory is now removed whenever the active CLI does not run as the staged release, and the postcondition requires the staged version. The repair test now covers a broken active CLI and an older one. At f3c155ee it shows `Found same AWS CLI version … Skipping install.` then `Installed aws-cli/2.35.20.` (validation §13l).
  - 4236358718 (P2): a failed Zed archive download after a successful lookup failed every apply. `install_zed_release` returns 3 for it, and `main` keeps an installed Zed with a warning or prints a retry notice, exit 0, as offline. The tar status is pinned to 1 so tar's own 2 cannot pass for "gh not ready". A new `zed.bats` case covers it; the replay exits 22 at f3c155ee and 0 at 674aaac0 (validation §13l).
- **e0fed47e**, fixed in 8cb8a1d1:
  - 4236634557 (P2): `make docker` reused an image the previous recipe built, whose version label matched, so the new verification never ran. The Dockerfile now also labels `chezmoi.sha256`. The recipe reuses an image only when that label holds a 64-character sha256; an older image is rebuilt through the verification.
  - 4236634561 (P2): the validator let a rolling GitHub asset roll on `release-shasums` or `release-sha256` alone. A rolling asset now needs `github-release-attestation`, `gpg` or `cargo-locked`, or an `attestation` beside a checksum file.
  - 4236634564 (P2): the wget fallback's private wgetrc had no cleanup on interruption. It is now written inside a subshell whose EXIT trap removes it, with HUP, INT and TERM turned into exits. `test_an_interrupted_wget_never_strands_the_credential_file` kills the fetch mid-download.
  - The three new tests fail at e0fed47e inside the sandbox (validation §14e).
- **8cb8a1d1**, fixed in 73034ae4:
  - 4236690491 (P2): the gh version gate compared numerically, so `2.93.0-rc.1`, below the 2.93.0 fix in SemVer, passed it. `github_attestation_ready` now accepts only a plain `X.Y.Z` at or after 2.93.0. The prerelease case of `test_attestation_needs_an_authenticated_gh_and_fails_hard_on_a_bad_attestation` fails at 8cb8a1d1 inside the sandbox (validation §14e).
- **96253ea3**, fixed in 70361875:
  - 4236809940 (P2): with the ETag lookup offline, `main` accepted any executable `~/.local/bin/aws`, so a broken CLI passed with "the installed AWS CLI stays". It now requires `verify_aws_cli_version`, as the other two paths do, and fails with `no working AWS CLI is installed`. The new offline case of `test_main_keeps_an_installed_aws_cli_offline_and_fails_a_fresh_install` fails before the fix inside the sandbox (validation §15c).
- **70361875**, fixed in 50759078 (Amendment 8):
  - 4236835114 (P1): without an authenticated gh the chezmoi bootstrap ran an archive checked only against its own release's checksum file, and the later deferred attestation could not undo that. The fix is the Amendment 8 section below.
- **50759078**, fixed in 36d87f6c:
  - 4236901115 (P1): in a GitHub Enterprise job (`GITHUB_SERVER_URL` or `GH_HOST` naming another host), the release lookup sent that host's `GITHUB_TOKEN` or `GH_TOKEN` to `api.github.com`, and `gh` for github.com saw them too. `github_enterprise_context` detects that case. The lookup then ignores both variables and asks `gh auth token --hostname github.com` instead. Every `gh` call for github.com goes through `github_dotcom_gh`, which unsets them there. `setup.sh`'s copy follows.
  - 4236901122 (P2): on the fallback path, a mise that `mise self-update` had moved past the fallback was downgraded on the next bootstrap. An installed mise at or past the fallback now stays, with one line and no download. An older or broken one is replaced by the fallback. `mise_installed_version` is exit-status-aware, like the other probes.
  - 4236901128 (P2): when keys.openpgp.org or `SHASUMS256.asc` was unreachable, gpg's presence made the bootstrap fail even with an authenticated gh. `verify_mise_shasums_signature` now returns 3 for a key it could not fetch, and the bootstrap treats an unfetchable `.asc` the same way. With an authenticated gh, the release attestation is then the check, with a warning. Without gh, nothing installs. A bad signature or a wrong key still fails.
  - The three new tests fail at 50759078 inside the sandbox and pass at the head (validation §15e).
- 19504fe5, 73034ae4 and 36d87f6c drew no Bot finding (the Code Review completed with no review and no comment). Heads 50afc9b5, 89d9b982, 3cbcf388 and 0d264db8 drew no Bot review or comment. The worker resolves no thread.

## CI

- f688336c failed: shellcheck 0.9.0 on the runner reports SC2015 for the Crit checksum `A && B || C`. Shellcheck 0.11.0 here does not. Fixed in 50afc9b5.
- 50afc9b5 passed 16/16, including both bootstraps through the helper and the zed bats on Ubuntu clients.
- 89d9b982 failed the ruff format check: a `sed` edit after the last format run. Fixed in 7903de38.
- aa69c2a0 and f3c155ee passed 16/16.
- 2453b1c9 failed `Run Python unit tests` in `test (ubuntu-24.04, client)` and `test (ubuntu-26.04, client)`; the other two `test` jobs were cancelled. The one failure was `test_installer_cleanup_survives_mock_function_returns` (mise): `gpg: no valid OpenPGP data found` on the fixture's fake `.asc`. That test is in the local sandbox baseline (macOS `mktemp`), so the local run could not catch it. Same cause as Bot thread 4236226692; fixed in aa69c2a0.

## Tests

- **Python:**
  - `tests/unit/test_github_release.py` (26 tests; the later ones are listed under their revise rounds and Bot threads): the window, wget, both credential paths (curl on stdin, wget through a 0600 wgetrc that is removed), the github.com-bound `gh auth token`, a truncated download that yields no tag, the attestation outcomes (no gh, unauthenticated, verified, newer gh, failed, gh 2.92.0 declined, unreadable version) with `--repo github.com/…`, and the `setup.sh` copy.
  - `test_validate_agent_assets.py`: rolling and pinned rules.
  - `test_aws_cli_acquisition.py`: the unversioned archive; the postcondition requires the staged version to be active (674aaac0); the same-version repair for a broken or an older active CLI; a failed download that keeps a working CLI, fails without one, and a bad signature that always fails (round 3); and the ETag cases: skip on a match, reinstall a broken CLI behind a matching ETag, install and record a new ETag, keep an installed CLI offline, fail a fresh install offline.
  - `test_runtime_health.py`: Crit at the pin (the base's `…_is_pinned_atomic_and_recorded` names again). The fixture renders a fixture pin into its `installer-pins.sh`. Cases: a replaced release whose `checksums.txt` matches is refused; a bad `checksums.txt` is refused; a broken binary is replaced; one that prints the banner and exits 42 is replaced or never promoted; a failed download installs nothing.
  - `test_supply_chain_policy.py`:
    - no rolling installer (mise, Zed, chezmoi) carries a version constant, and each resolves through the helper;
    - Crit and starship carry a rendered pin;
    - the cleanup cases stub the lookup and the GPG check;
    - the every-apply cases: starship against its pin (current, a pin bump, missing, exits 42) and sheldon against the newest crate.
- **Bats** (CI only; each file runs in the `Run unit test` step of the `test (<os>, <system>)` jobs that match its tag):
  - `tests/install/common/mise.bats`, "[common] mise bootstrap resolves the newest cooled-down jdx/mise release" (replaces the version-floor test): all four `test` jobs.
  - `tests/install/common/setup.bats`: the two release-fixture cases serve a releases API page and a fake unauthenticated `gh`; since Amendment 8 that fake `gh` is authenticated and verifies, so those cases take the rolling path and assert the attestation call. A new case runs with no usable `gh` and asserts the reviewed fallback is fetched with no API call and refused by its sha256 (the fixture is not the reviewed archive), with nothing run. All four `test` jobs.
  - `tests/install/common/check_tools.bats`: the Crit banner, plus three `check_zed` cases. All four `test` jobs.
  - `tests/install/ubuntu/client/zed.bats`: rewritten with thirteen cases. They cover architecture, a verified install, the installed no-op, a broken binary replaced (silent, and since round 2 one that prints the current banner and exits 42), a self-updated newer Zed kept, a failed archive download that keeps or skips without failing, unauthenticated with and without an installed Zed, a failed attestation, an unreachable API, and the `run_after_05` script. Run by `test (ubuntu-24.04, client)` and `test (ubuntu-26.04, client)`.
  - `starship.bats` and `sheldon.bats` are unchanged and still valid. `install_starship` takes the tag as an argument and does not resolve it, so the checksum-failure case still exercises the checksum path. They run in `test (ubuntu-24.04, server)`.
- **Local `make unit-test`:** no branch-only failure except renames of baseline sandbox failures. The macOS `mktemp` ignores `TMPDIR`, and the sandbox refuses `/var/folders`:
  - `test_linux_crit_install_takes_the_cooled_down_release_atomically_and_records_it` and `test_darwin_crit_install_takes_the_cooled_down_release_atomically_and_records_it`, formerly `…_is_pinned_atomic_and_recorded` in the baseline;
  - `test_crit_replaces_an_installed_binary_that_cannot_report_its_version` (new), which fails on the same `mktemp`;
  - round 2: `test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails`, `test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails` and round 1's `test_main_repairs_a_broken_same_version_install_the_upstream_update_would_skip`, on the same `mktemp`. All six pass outside the sandbox (validation §13).
  - CI runs all three (validation §7, §9).
  - At the final head 36d87f6c, inside the sandbox: 925 tests, no failure outside the 8d719629 baseline, plain or with the TMPDIR `mktemp` shim (validation §15h).

## Risks and follow-ups

- An anonymous fresh bootstrap shares GitHub's 60-requests-per-hour limit per IP. Behind a busy NAT (this seat's sandbox egress hit it once), resolution fails until the window resets. `GITHUB_TOKEN` or a logged-in `gh` avoids it, the every-apply scripts keep installed tools, and CI exports a token.
- A fresh bootstrap without gh (and, for mise, without gpg) installs the reviewed fallback releases; their pins move only with a reviewed manifest bump, and mise self-update and mise's own chezmoi take over after the first run (Amendment 8). The attestation evidence for `gh release verify-asset` comes from CI, not from this seat, whose permission gate refuses `gh release verify-asset --help`. The help text is the manual page.
- With `gpg` and `gpgv` present, the mise bootstrap needs keys.openpgp.org and `SHASUMS256.asc`. Since 36d87f6c an outage of either falls back to the release attestation when `gh` is authenticated. Without `gh` it still fails and installs nothing, while a host without `gpg` in the same outage would install the reviewed fallback. That is a decision, not a gap: like a failed release lookup after a positive readiness check, which also fails rather than falling back, readiness means the tools are present, not that the network answers. The fallback is chosen only up front, before any release is fetched, so a fetch failure never trades the newest release for an older one mid-run. A committed key under `home/dot_local/share/`, the AWS CLI pattern, would remove that dependency; it is a new file outside the allowed files, so it is not added (scope gap, reported).
- Every apply now calls the GitHub API for Zed (clients), runs `cargo search` for sheldon, and sends one HEAD for the AWS CLI (Ubuntu). Each is one request. starship and Crit need no request while they are at their pins.
- PATH (AGENTS.md dotfiles safety): only the two attestation functions see mise's shim directory first, through a function-local `PATH`. The user's shell `PATH`, the installers' `PATH` and every other command are unchanged. On a host with both gh builds, attestations now run on mise's gh.
- Crit and starship move only when someone bumps their pin and its sha256 in the manifest. The orchestrator drafts the follow-up that makes starship roll again through mise's aqua backend (Amendment 7).

## Revise round 1 (orchestrator, Codex Bot on fd4ff82d, the update-branch head)

I first pulled the orchestrator's `gh pr update-branch` merge, fd4ff82d. The orchestrator replied to and resolved the seven earlier threads. Both new findings are fixed at the root in 0d264db8.

1. **4235444419 (P1): the credential could show in an xtrace.**
   - Under `DOTFILES_DEBUG` the callers run `set -x`, so `bearer=…` and the `printf` building the header wrote the token to the terminal or a captured log.
   - `github_release_list` now turns off a caller's xtrace before the credential is read and restores it afterwards on every path; the request itself moved into `github_release_fetch`. The `setup.sh` copy follows.
   - `test_an_xtrace_never_shows_the_credential_and_is_restored` runs the helper under `set -x` for curl with `GITHUB_TOKEN`, wget with `GH_TOKEN`, and the `gh auth token` fallback. It asserts the token appears nowhere in stderr, the fake still received the `Authorization` header, and xtrace is on again afterwards.
   - It fails against fd4ff82d for all three, with the token in the trace (validation §12).
2. **4235444420 (P2): the AWS repair could not replace a broken same-version tree.**
   - The upstream `aws/install --update` exits 0 without copying when the version directory exists ("Found same AWS CLI version … Skipping install.").
   - So with a matching ETag and a broken binary, every apply ran the installer, kept the broken tree and failed the postcondition.
   - The fix comes after the GPG signature and the staged CLI's own version check pass, and applies only when the installed CLI no longer runs: the installer removes that same-version directory (`${AWS_CLI_INSTALL_DIR}/v2/<version>`, the version strictly numeric) before the upstream install. A working install is never touched.
   - I chose the removal, the alternative the round allows, over a staging directory. The upstream installer writes absolute `current` and bin-dir symlinks, so a moved staging tree would point at the old location.
   - `test_main_repairs_a_broken_same_version_install_the_upstream_update_would_skip` sets up a recorded ETag, an installed `aws` that exits 42, and a fake upstream installer that skips an existing version directory. It asserts the CLI is replaced and the postcondition passes.
   - It fails against fd4ff82d with the upstream skip message and exit 42 (validation §12).

## Revise round 2 (orchestrator, audit of 0d264db8: `incorrect`, 1 P1 and 3 P2)

`git pull --ff-only origin feat/rolling-release-assets` was a no-op: `HEAD` and `FETCH_HEAD` were both 0d264db8. All four findings are fixed in 2453b1c9; every new test fails against 0d264db8 (validation §13).

1. **P1, a fetched tag reached shell source.**
   - Root cause: `github_release_tag` returned whatever the API named. It now accepts only `^v?[0-9]+(\.[0-9]+)*([-.+][0-9A-Za-z.-]+)?$` (`GITHUB_RELEASE_TAG_PATTERN`, named once, beside the other constants; the `setup.sh` copy follows), and otherwise prints `unexpected release tag <tag> for <repo>` to stderr and returns 1 with nothing on stdout. Every consumer (installers, `setup.sh`, `make docker`, the `test.yaml` step) is protected at the source.
   - `make docker` also stops interpolating: the recipe runs `chezmoi_version="$$(bash -c '…github_release_tag twpayne/chezmoi')"` and strips the `v` in its shell; the target-specific `$(shell …)` variable is gone. The workflow step and the Dockerfile already read the tag through a shell variable and an `ARG` used by `RUN`'s shell; they needed no change.
   - Tests: `test_tag_must_be_a_version_or_the_lookup_fails` (the auditor's `v$(printf${IFS}X)`, `;`, `..`, a space and `latest` refused; `2.73.0`, `-rc.1` and `+build.5` accepted) and `test_make_docker_never_runs_the_fetched_tag` (`make -n docker` prints the resolving command and fetches nothing; `make docker` with a tag `v$(touch${IFS}<marker>)` fails and creates no marker). At 0d264db8 the dry run printed the crafted command substitution, and the plain-bash replay created the marker (validation §13).
2. **P2, version probes trusted the banner of a failing binary.** `crit_version`, `zed_installed_version`, `sheldon_installed_version` and `starship_installed_version` now capture the output with its status (`output="$(… --version 2> /dev/null)" || return 0`) and print nothing unless the binary exits 0. Tests: Crit, an installed binary with the right banner that exits 42 is replaced, and a staged one is never promoted (`test_runtime_health.py`); starship and sheldon, the same case in the every-apply table (`test_supply_chain_policy.py`); Zed, a new `zed.bats` case (CI only), replayed in plain bash against both trees.
3. **P2, the bootstrap downgrade.**
   - (a) The listings (validation §13) show mise publishes `SHASUMS256.asc`, a clearsigned checksum file, plus minisign files; chezmoi publishes `chezmoi_2.73.0_checksums.txt.sigstore.json` and `chezmoi_cosign.pub`, a cosign signature a fresh host cannot verify. The task text says mise's own `install.sh` verifies the `.asc`; its line 225 is `# TODO: verify with minisign or gpg if available`, so the bootstrap follows mise's documentation instead: the release key `24853EC9F655CE80B48E6C3A8B81C9D17413A06D` on keys.openpgp.org. With `gpg` and `gpgv` present, `verify_mise_shasums_signature` fetches that key, requires exactly one primary key with the pinned fingerprint, validity `-` and no past expiry (AWS pattern), dearmors it into a private keyring, and takes the checksums from `gpgv --output -`, the signed text itself, never from `SHASUMS256.txt`. The fingerprint is `assets.mise.gpg_fingerprint`, rendered into `MISE_GPG_FINGERPRINT`. Decision: fail-closed. With gpg present, a failed key fetch, key check or signature stops the bootstrap; without gpg it uses `SHASUMS256.txt`.
   - (b) Retired by Amendment 8 (see there). As first built: when `github_release_attestation` returned 2, mise and chezmoi called `github_release_defer_attestation`. `scripts/upgrade-tools.sh` gains `verify_pending_attestations`, run right after Homebrew and before both mise phases. It sources the helper only when a record exists, so T118's upgrade fixtures in `test_runtime_health.py`, which copy the script without it, stay untouched. With gh not ready it prints one warning naming every pending tool and keeps the records. A verified record is removed. A failed one is a required failure naming the tool and the archive, and says to reinstall and then delete the record.
   - Decision: on a failed attestation `main` stops at once: `Upgrade summary: stopped at the pending release attestations; …`, exit 1. That departs from the record-and-continue of `run_required_phase` on purpose: a mise that failed its attestation must not run `mise self-update` or the tool phases. The README asset paragraph says all of this. The Zed path is unchanged (nothing installed without gh).
   - Tests: the deferral record (mise, no gh); the GPG path (good, bad signature with output streamed, wrong fingerprint, expired key, two primary keys); gh verifying and failing at install time; an unwritable record failing; the phase (no records, gh absent, one fails, all pass); and `main` stopping before mise. The `setup.bats` wget-only case now asserts the chezmoi deferral message, record and archive copy (CI only). A live scratch-HOME bootstrap shows the real key, a good signature and the deferral, with and without gpg; the phase then warns once (validation §13).
4. **P2, CompactionDB evidence.** Validation §13 now quotes the original `memory add` command and its output verbatim, from the session transcript at 2026-10-09T22:13:56Z. Both `echo … rc=$?` there report `tail`'s status, not uv's, so the ids are the evidence. A read-only `memory search` in the main checkout shows both ids.

Scope: every file is in the allowed files, the round's text or Amendment 7. That covers the `scripts/upgrade-tools.sh` phase and its call in `main`, the `make docker` recipe, `setup.bats` (the chezmoi fixture case) and `zed.bats`. No further file is edited. The committed-key alternative is reported under Risks.

### Amendment 7 and the Bot review of 2453b1c9 (aa69c2a0)

CI on 2453b1c9 failed in the mise cleanup fixture, and the Bot left four threads. The two that bear on the task's own wording went to the orchestrator as q11 and q12, with defaults. Amendment 7 accepted both and corrected the rule (above).

- **Crit and starship pinned (q11, 4236226700).**
  - Pins: `assets.crit` (v0.22.0, four sha256, rendered into `installer-pins.sh`) and `assets.starship` (v1.26.0, two sha256, rendered into `install/ubuntu/server/starship.sh`). Each has the reason Amendment 7 states. For every asset, GitHub's asset digest, the release's checksum file and a local hash of the download agree (validation §13).
  - Both installers check the reviewed sha256 first and the release's own checksum second. Both still skip when current, so a bump applies on the next `make update`.
  - starship no longer needs the release helper, so its wrapper drops the `github-release.sh` include and `update-agent-assets.sh` drops its source line. Both are back to their base form.
  - A replay serves a replaced binary with a `checksums.txt` that matches it: 2453b1c9 installs it, aa69c2a0 refuses it (`Crit checksum mismatch`, rc=1).
- **CI cooldown (q12, 4236226697).** `minimum_release_age: 72h` is set on the four `mise-action` steps. The pinned action's `action.yml` has that input (validation §13). `test_the_window_is_the_mise_cooldown` now requires it on every `mise-action` step; it fails at 2453b1c9 on `docs.yml`.
- **Zed (4236226689).** An installed Zed at or past the resolved release stays (`sort -V`); a newer one prints `zed <v> stays: it is newer than the cooled-down <tag> (Zed updates itself).` A new `zed.bats` case covers it (CI only). The plain-bash replay downgrades to 1.22.0 at 2453b1c9 and keeps 1.23.0 at aa69c2a0.
- **Cleanup fixture (4236226692).** The mise case stubs `verify_mise_shasums_signature`; the starship case's `starship_artifact` returns its own reviewed sha256.

## Revise round 3 (orchestrator, audit of 674aaac0: `incorrect`, 1 P1 and 2 P2)

The fetch showed no new commits (`HEAD` = `FETCH_HEAD` = 674aaac0). All three findings are fixed in 19504fe5 and 16a64632. The new tests fail against 674aaac0 inside the sandbox (validation §14b).

1. **P1: CI and Docker trusted chezmoi's same-release checksum file.**
   - CI: the `test.yaml` chezmoi step runs `github_release_attestation twpayne/chezmoi v<version> <archive>` after the checksum and fails closed, with no deferral. Its status 2 (gh absent, unauthenticated or older than 2.93.0) fails the step with that message. All four `test` jobs on 19504fe5 show `✓ Verification succeeded! chezmoi_2.73.0_… is present in release v2.73.0` (validation §14a).
   - Docker: `make docker` resolves the tag and asks Docker for its architecture (`docker version --format '{{ .Server.Arch }}'`; `docker is not reachable` otherwise). It then calls the new `github_release_verified_sha256`, which:
     - requires `github_attestation_ready` before downloading anything (status 2, and the recipe says `run make gh-auth, then make docker`);
     - downloads the archive and checksum file into a private temporary directory, checks the checksum, runs `gh release verify-asset`, and prints the verified sha256;
     - on any failure makes the recipe print `failed its checksum or release attestation; nothing was built`.
   - The recipe passes `CHEZMOI_VERSION` and `CHEZMOI_SHA256` as build args. The Dockerfile requires both and checks its own download against that sha256 alone, with no checksum file.
   - Tests:
     - `test_make_docker_verifies_chezmoi_on_the_host_and_passes_its_sha256` covers four cases: verified (the build arg equals the archive's sha256); attestation refused; checksum mismatch; gh not ready (the hint, nothing downloaded). No build runs in the last three.
     - `make -n docker` shows both args (validation §14c).
     - The workflow passes prettier, and CI ran it.
2. **P2: a failed download aborted the apply over a working tool.**
   - starship, the AWS CLI and sheldon follow the Zed rule. A download that fails after the lookup returns 3 inside the installer. `main` then keeps a working installed tool with one warning, exit 0, or fails when none is installed. A failed checksum, GPG signature, postcondition or cargo checksum always fails and installs nothing.
   - AWS: a kept CLI also keeps its old ETag record, so the next apply retries.
   - sheldon: cargo exits 101 for every error, so `install_sheldon` tees cargo's stderr into its private directory. Any mention of a checksum is verification, which keeps cargo's status, even inside cargo's `failed to download` wrapper. A recognised network error is acquisition (3). Anything else keeps cargo's own status, a 3 turned into 1.
   - 16a64632: the first version mapped those to 1. CI on 19504fe5 failed `test_installer_cleanup_preserves_failure_status`, which expects a failing cargo's 42. That test is in the local sandbox baseline (bare `mktemp -d`), so only CI ran it; validation §14d.
   - e0fed47e: CI on 16a64632 failed on the macos-14 runner, where `sha256sum` does not exist (exit 127 in the starship checksum case). The fixture adds a `shasum`-backed `sha256sum` when the host has none. The three touched modules were then run in the sandbox with `/sbin` and `/usr/sbin` removed from `PATH` (no `sha256sum`) and the `TMPDIR` shim.
   - Tests: `test_a_failed_download_keeps_a_working_tool_and_a_failed_check_never_does` (starship and sheldon) and `test_main_keeps_a_working_aws_cli_when_the_download_fails_and_never_on_a_bad_signature`. Each covers a working install, no install, and a verification failure. Their fixtures carry a `mktemp` that honours `TMPDIR`, so they run in the sandbox. The behaviour cases fail against 674aaac0 (exits 22 and 101); the verification cases pass on both, as regression guards.
3. **P2: the sandbox record's isolation claim was false.**
   - The record is rewritten from the session transcript: 129 out-of-sandbox commands, by action and by whether step 4 allows them, and the eight refusals with what followed (five reworked). It also says what those commands wrote, including the one unverified point (chezmoi's own file access in five `HOME`-less test subprocesses) and the downloaded Crit binary that ran outside. Validation §14g lists every one of those commands verbatim.
   - This round: no test, replay or download ran outside the sandbox. The Crit and AWS same-version fixtures now carry the same `TMPDIR` `mktemp`, so the full suite runs them inside, with no failure beyond the 8d719629 baseline.
   - The out-of-sandbox commands this round were `git fetch`, `git push`, `gh` and `agmsg-dispatch`, plus the artifact copy with the repository masker. One exception: a local Python edit of the scratch sandbox record went out in the same unsandboxed command as a `gh pr checks`; the record names it.
   - No refused command was reworked.

## Revise round 4 (orchestrator, audit of 73034ae4: `incorrect`, 3 P2)

The fetch showed no new commits (`HEAD` = `FETCH_HEAD` = 73034ae4).

1. **P2: `make docker` passed gh's report as the sha256.**
   - Cause: `gh release verify-asset` prints its verification report (`Calculated digest for …`, `✓ Verification succeeded! …`) on stdout. So `github_release_verified_sha256` printed those lines with the digest, and `make docker` passed all of them as `CHEZMOI_SHA256`, which the Dockerfile's strict checksum refuses.
   - Fix (96253ea3): `github_release_attestation` sends gh's stdout to stderr (`1>&2`), so every caller (installers, `setup.sh`, the CI step, the upgrade-tools phase, `make docker`) gets only the status. CI logs still show the report. The `setup.sh` copy follows.
   - Tests:
     - The fake `gh` in `test_github_release.py` now prints gh's two real lines on stdout.
     - The attestation test asserts the helper's stdout is empty.
     - The `make docker` test asserts the build arg is the digest line alone.
     - `github_release_verified_sha256` called directly must print exactly one 64-character line.
     - Both fail against 73034ae4 inside the sandbox (validation §15a).
2. **P2: the sandbox record's "no command wrote the repository except through `git push`" was false.**
   - The record now lists every out-of-sandbox command that wrote a tracked file or the repository's history, numbered as in validation §14g:
     - #83, #84, #85, #109, #111 and #113: Python rewrites plus `ruff format` of `tests/unit/test_supply_chain_policy.py`, `tests/unit/test_runtime_health.py`, `install/ubuntu/common/aws_cli.sh` and `tests/unit/test_aws_cli_acquisition.py`, each bundled with a test run;
     - #30: `ruff format` of a tracked test, then a commit;
     - #20, #25, #30, #35: `git add`/`git commit` bundled with pushes.
   - The record says which commits carry them: aa69c2a0, 674aaac0, 50afc9b5, 89d9b982, 7903de38 and 3cbcf388, all pushed and reviewed as part of the PR.
   - The inventory gains two rows for these. The "local python edit" row keeps its eight scratch-only commands, which I checked by hand.
3. **P2: conformance.** The orchestrator recorded the deviations in the acceptance record. This round ran outside the sandbox only step 4's cases: `git fetch`, `git push`, `gh` (with text filters only), the main-checkout CompactionDB `memory add`, the masked artifact copy and `agmsg-dispatch`. The record's round-5 line lists them, and validation §14g lists each command verbatim.

## Amendment 8 (Bot 4236835114 on 70361875, q13): nothing runs before an independent check

- **The finding.** Without an authenticated `gh`, the chezmoi bootstrap ran an archive checked only against its own release's checksum file. The deferred attestation at `make update` could not undo that execution. mise without gpg had the same gap, and a fresh macOS has neither tool. I asked q13 with a default, and the orchestrator accepted it.
- **The design (50759078).**
  - With a check that can run before execution, the bootstrap installs the newest cooled-down release, verified that way. For mise the check is gpg with the pinned release key (`mise_gpg_ready`) or an authenticated stable gh; for chezmoi, an authenticated stable gh.
  - Otherwise it installs a reviewed fallback, with no release lookup. The fallbacks are `assets.mise.fallback` (v2026.10.3, four platforms) and `assets.chezmoi-bootstrap.fallback` (v2.73.0, four platforms), each with a reason, rendered into `install/common/mise.sh` and `setup.sh`.
  - The reviewed sha256 is checked after the release's own checksum file, so a replaced release with a matching checksum file is refused.
  - The fallback digests are GitHub's asset digests for these immutable releases; all eight are pasted beside their release checksum line and manifest value in validation §16, and they agree. Two per tool are also the digests CI's attestation verified (mise linux-x64 and macos-arm64; chezmoi linux_amd64 and darwin_arm64; validation §15d).
- **Retired.** `github_release_defer_attestation`, the `pending-attestation` records and the `upgrade-tools.sh` phase are gone; `upgrade-tools.sh` is byte-identical to 0d264db8. Their tests went with them.
- **Validator.** A `release: latest` asset with `attestation: when-gh-authenticated` must record `fallback.pin`, `fallback.sha256` and `fallback.reason`, and `fallback` is refused elsewhere. `--set-asset` reaches `fallback.pin` and `fallback.sha256.<platform>`.
- **Tests:**
  - mise and `setup.sh` unit tests for the three cases: gh or gpg ready takes the rolling release; neither installs the fallback with no lookup; a fallback archive that misses its reviewed sha256 installs nothing;
  - the gpg and attestation failures, as before;
  - `mise.bats` and `setup.bats` cases for the fallback (CI only; the mise case replayed in plain bash in the sandbox);
  - the validator and `--set-asset` cases.
- **Live, inside the sandbox, at the final head** (validation §15b):
  - a scratch-HOME mise bootstrap with no gh and no gpg on `PATH` installs the reviewed mise 2026.10.3;
  - the same bootstrap again keeps that mise and fetches nothing (a curl that logs and fails is first on `PATH`; Bot 4236901122);
  - a curl wrapper that replaces the archive and rewrites its `SHASUMS256.txt` line is refused by the reviewed sha256;
  - chezmoi's fallback archive passes `setup.sh`'s checksum-file and reviewed-sha256 checks, and a tampered copy with a rewritten checksums line is refused by the reviewed sha256.
- README: the mise and chezmoi rows and the paragraph now describe this, including (36d87f6c) the kept newer mise and gh as the check when mise's GPG inputs cannot be fetched; the deferral text is gone.
- **The gh-ready path in CI** (validation §15d): on the final head the `test` and bootstrap jobs verify chezmoi's and mise's attestation before they run, and no job prints a fallback line.

## Revise round 5 (orchestrator, audit of 36d87f6c: `incorrect`, 2 P2, no implementation defect)

The fetch showed no new commits (`HEAD` = `FETCH_HEAD` = 36d87f6c). This round changes no tracked file, so the head stays 36d87f6c.

1. **P2: the eight fallback trust anchors were claimed, not shown.** Validation §16 now pastes them side by side for mise v2026.10.3 (macos-x64, macos-arm64, linux-x64, linux-arm64) and chezmoi v2.73.0 (darwin-amd64, darwin-arm64, linux-amd64, linux-arm64):
   - GitHub's asset digest from `gh api repos/<repo>/releases/tags/<tag> --jq '.assets[]|select(.name=="<asset>")|.digest'`, run outside the sandbox through the gate, printed to stdout and saved with the editor (§16a). Both releases report `immutable: true`.
   - The asset's line in the release's own checksum file (`SHASUMS256.txt`, `chezmoi_2.73.0_checksums.txt`), downloaded inside the sandbox; the files' own sha256 is printed with them (§16b).
   - The manifest value under `fallback.sha256`, with the two manifest blocks quoted (§16b), and the rendered constants in `install/common/mise.sh` and `setup.sh` (§16c).
   - All eight agree across all three sources. Nothing in the manifest changed. A self-check shows the comparison stops on a single changed character (§16c).
2. **P2: conformance.** The historical deviations stand as the acceptance record states them. The sandbox record's round-6 line says this round ran outside the sandbox only step 4's cases.

## Decisions

[memory:decision] dotfiles-T119 (orchestrator 2026-10-09): release-asset installers install the latest release verified by the publisher's own mechanism (attestation or signature first, checksum file second); only assets whose publisher offers nothing keep a pinned version and checksum with a stated reason; `render:` constants and `installer-pins.sh` exist only for those. Its "checksum file second" clause is superseded by Amendment 7, below.

[memory:decision] dotfiles-T119 Amendment 7 (orchestrator 2026-10-10): a release asset rolls only on a verification independent of the release page it is fetched from (a GitHub release attestation, a signature with a manifest-pinned key fingerprint, or an immutable registry with its own index checksums); a checksum file from the same mutable release is only a second, transport-level check. Crit (v0.22.0) and starship (v1.26.0) return to reviewed pins with per-platform sha256 and a reason. Supersedes the 'checksum file second' clause of 997c53f5. Round 2: with gpg and gpgv present the mise bootstrap verifies SHASUMS256.asc fail-closed; a bootstrap attestation that cannot run is deferred to pending-attestation/, and a failed one stops make update before any mise phase.

[memory:decision] dotfiles-T119 Amendment 8 (orchestrator 2026-10-10): nothing an installer fetches runs before a verification independent of the release page has passed; mise and chezmoi bootstraps take the newest cooled-down release only when gh (attestation) or, for mise, gpg with the pinned release key can verify it before it runs, otherwise a reviewed fallback release (`assets.<name>.fallback`: pin, per-platform sha256, reason, rendered), the same-release checksum file a second check; the deferred attestation is retired.

## CompactionDB

From the main checkout, through the permission gate, on 2026-10-09: the task decision line (id `997c53f5-244c-4ee8-be87-0e66131daedc`) and the amendments' decisions (id `f2e33997-ab7d-4dea-a50d-ddead9a6dcfb`). The commands and their output are quoted verbatim in validation §13, with a read-only `memory search` showing both ids. In round 3 the same way: the Amendment 7 decision, with round 2's fail-closed GPG and the stop at a failed deferred attestation (id `68c0a3fe-11b7-4053-a54a-4b2bd3d713af`; validation §13m quotes the command and output, and a read-only search shows the id). Round 5 added Amendment 8's decision (id `3431733a-2a5b-4c02-ac83-4592cc3a2af8`; validation §15f quotes the command and output).

## Hooks

- The Understand-Anything stale-graph hook did not fire. `.ua/` is not in allowed_files.
- No Plan Mode and no Crit plan review server were started.

## Review evidence

`.orchestration/validation/dotfiles-T119-rolling-release-assets-a01-worker-crit.json` and `-worker-review-receipt.md`. Crit data was unavailable, so the records hold the independent review (an advisor pass before the push and before the RESULT) with the Bot and CI findings, all resolved.

cost: n/a
