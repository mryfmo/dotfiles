---
task_id: dotfiles-T133-install-ppa-resilience-a01
seat: claude-standard-dot-a008
pr: 454
branch: tools/install-ppa-resilience-a01
merge_base: 7da0cdfab9de9fbea673b82379acd4e317115065
test_commits: 53f31406 24210a2b
fix_commits: 74b3a2d9 dc1ee465
task_sha256: 45fb80f66c9ca36ef5dc3595d516404b64b6060fab4bd2a2c3b7e3174a83488f
---

# Report: dotfiles-T133-install-ppa-resilience-a01, an unreachable Ghostty PPA never fails the apply

- **Producer:** worker (Claude seat, worktree worker-f).
- **Branch:** fresh from `origin/main` `7da0cdfa`.
- **A pause:** the task was parked for the PR #378 round-4 Bot fix round, with its tree clean and pushed, and resumed after it.

## Item 1: `install/ubuntu/client/ghostty.sh` (+31/−4)

- **`ppa_step <command…>`:** runs one PPA step and passes its output through.
  - When the step fails and its output holds `Failed to fetch https://ppa.launchpadcontent.net/` or `http://…` (`grep -F`), it returns 75.
  - Any other failure returns 1.
- **`install_ghostty`:**
  - runs `install_ghostty_dependencies` as today, outside the helper, so a failed archive install still fails the apply;
  - then runs `add_ghostty_ppa`, `apt-get update` and `apt-get install -y ghostty` through `ppa_step`;
  - on 75, prints `ghostty not installed: ppa:mkasberg/ghostty-ubuntu is unreachable; the next make update retries`, removes nothing, and returns 0;
  - on any other status, fails.
- **Kept:** `PACKAGES`, `DEPENDENCY_PACKAGES`, the `sudo --preserve-env` form and the shdoc comments.
- **The first fix, `74b3a2d9`:** it matched with `grep -E` on the interpolated host. The comparison lint refused that (R6, an identifier in a regex), and the unit job of `74b3a2d9` failed on `test_the_changed_files_are_clean_against_the_baseline`. `dc1ee465` switched to the two fixed strings.

## Item 2: `tests/install/ubuntu/client/ghostty.bats` (+56/−2)

- **The live test:** `[ubuntu-client] ghostty` runs the real installer once and requires exit 0.
  - When the output carries the retry line, `dpkg -s ghostty` must fail, which covers both absent and half-installed.
  - Otherwise `dpkg -s ghostty` must succeed.
  - It prints the branch it took.
- **The fakes:** `APT_FAKES` are shell functions for `sudo`, `add-apt-repository` and `apt-get`, in the style of `zed.bats`. `FAIL` picks the 503 step, either `update` after the PPA is added or `pool` on `install ghostty`, or a non-PPA `archive` failure. The fakes print apt's own `E: Failed to fetch … 503` lines.
- **Three cases:**
  - an unreachable PPA never fails the apply;
  - a failed PPA package download never fails the apply;
  - a non-PPA apt failure still fails the apply.
- **A fixture fix:** the first fake read `$3` under the installer's `set -u`, and `24210a2b` changed it to `${3-}`. That was found by running the fake harness in plain bash, not Bats, before the red run.
- **Kept:** the PACKAGES and DEPENDENCY_PACKAGES tests.

## Red and green (GitHub Actions, `test (ubuntu-24.04, client)`; validation §1, §2)

- **Red at `24210a2b`, the tests on main's installer:** https://github.com/mryfmo/dotfiles/actions/runs/39689531953/job/119532238630
  - `not ok 9 … an unreachable PPA never fails the apply` and `not ok 10 … a failed PPA package download never fails the apply`, each on `[ "${status}" -eq 0 ]` (main's installer exits 100);
  - `ok 11 … a non-PPA apt failure still fails the apply`.
- **Green at `dc1ee465`:** https://github.com/mryfmo/dotfiles/actions/runs/39692046991/job/119540330184
  - ok 6 to 11;
  - the live test took `# branch: the PPA answered; ghostty must be installed`.
- **Pairs:**
  - behaviour: `24210a2b` red to `dc1ee465` green;
  - lint: `74b3a2d9` red (R6) to `dc1ee465` green.

## Check (validation §3)

- **The installer:** `bash -n`, `shellcheck` and `shfmt -i 4 -sr -d` exit 0, and the comparison lint exits 0.
- **Caps, from merge-base `7da0cdfa`:** 35 of 80 outside `tests/` and `.orchestration/`, and 58 of 120 under `tests/`.
- **Bats:** never run locally; the plain-bash smoke of the fakes is in §4.

## Residuals

- **Detection:** it reads apt's `Failed to fetch <url>` text for the PPA host. A Launchpad API failure inside `add-apt-repository` (the key fetch from api.launchpad.net) is not covered, and still fails.
- **A pool outage:** it leaves the PPA configured, which the next `make update` reuses.

cost: n/a

## Revise 2 (AGMSG-ACCEPTANCE status=revise round=2 amendment=3, 2026-10-22T02:33:03Z; previous head 44134e36)

- **Producer:** worker (Claude seat).
- **The audit:** the task-level audit of `44134e36` found five P2s, four of them in this task's scope. Amendment 3 (`bc6a455f…`, now the task copy) adds Item 3 and the three checks.
- **The base:** main was merged first, at `7b21659e`, as merge commit `51668a16`.
- **Commits:** the red tests are `ae120581` and the fix is `ed76b740`.

| Finding | Fix | Fixture (`tests/install/ubuntu/client/ghostty.bats`), red at ae120581, green at ed76b740 |
| --- | --- | --- |
| an exit-0 `apt-get update` with a failed PPA index missed the skip | `ppa_step` classifies by output, whatever the exit: when every `Failed to fetch` line names `ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/`, it returns 75 | `an apt-get update that reports a failed PPA index without a non-zero exit is an outage` (red: exit 1, the install attempted) |
| any Launchpad fetch line made a mixed failure a success | a fetch failure from any other source, the Ubuntu archive or another PPA on the same host, keeps apt's own status | `a fetch failure from another host stays fatal even when the PPA also failed` (red: exit 0 with the retry line, for both cases) |
| a skipped install was never retried (the caller was a `run_once_` script) | the step moves to `home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl`, with the same guard as `run_after_05-client-install-zed.sh.tmpl`. The misc `run_once_` script drops the include, and the installer returns 0 at once when `dpkg -s ghostty` succeeds | `the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it` (red: no template), and `an installed ghostty is left as it is` (red: apt called) |
| validation.md was not verbatim | rewritten: every command with its output, JSON as JSON, the lint red run included (§3) | n/a |

- **The fifth finding:** the deferral in the acceptance record is the orchestrator's.
- **Checks:**
  - CI at `ed76b740` passes ok 6 to 15 in the ubuntu-24.04 client job;
  - `bash -n`, `shellcheck`, `shfmt -i 4 -sr -d` and the comparison lint exit 0.
- **Caps, from merge-base `7b21659e`:** 59 of 110 outside `tests/` and `.orchestration/`, and 107 of 160 under `tests/`.
- **The `regime` failure:** on `ed76b740` it came only from the stale task copy, which predated amendment 3's `allowed_files`. The records commit carries the amended copy.
