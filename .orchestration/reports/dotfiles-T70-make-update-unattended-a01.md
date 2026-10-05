# dotfiles-T70-make-update-unattended-a01 — report (status: ready_for_review)

Worker: `claude-standard-dot-a006` (Claude Code, `standard`), worktree `.claude/worktrees/worker-d`.
PR: https://github.com/mryfmo/dotfiles/pull/238 — branch `fix/make-update-unattended` — head `229a2ec1986581d8b3ed369ab9895aab9f597951`, one commit on `origin/main` c6de5156 (main has not moved; the branch is up to date).
Task file revisions verified: `360d8aa8…` (dispatch) and `bc0e79e9…` (revision pong-decision-1).

## Changes

1. **`Makefile` `update`:** a failing `herdr status server --json`, a jq rejection (malformed, non-string, multiple, or missing status) and an unknown status now all print `Herdr server unreachable; skipping config reload.` to stderr and continue, so `agmsg-bootstrap` still runs. The two former `exit 1` blocks became one `if … || …; then server_status=unreachable` that falls into the `*)` arm, which no longer exits. The `running`/`protocol_mismatch`, reload-failure (`exit 1` kept, outside scope), `not_running` and Herdr-absent paths are unchanged. A short comment block above `update:` defines the operator phase and the unattended `make update` (item 4).
2. **`install/ubuntu/common/apparmor_userns.sh` `install_profile`:** `sudo -n true 2>/dev/null || { echo "apparmor bwrap-userns profile pending: run 'sudo -v && bash install/ubuntu/common/apparmor_userns.sh'" >&2; return 0; }`, followed by `sudo -n install …` and `sudo -n apparmor_parser …` (`grep -c 'sudo -n'` = 3). Per PONG decision 1 the remedy names the standalone script. The `Loaded AppArmor profile …` line moved from `main` into `install_profile`: with `set -Eeuo pipefail` the guard has to `return 0`, and `main` would otherwise print "Loaded" for a pending profile. A real `sudo -n install`/`apparmor_parser` failure still exits non-zero.
3. **`scripts/check-tools.sh`:** per decision 1(2), no new `warn_optional`. Only the existing REQUIRED failure's stale "(chezmoi apply installs it)" became "(sudo -v && bash install/ubuntu/common/apparmor_userns.sh)".
4. **`scripts/upgrade-tools.sh` `upgrade_mise_self`:** `mise self-update --yes "${mise_pin#v}"`, where `mise_pin="$(asset_manifest_pin mise "${repo_root}")" || return 1`. VERIFY: mise v2026.9.13 `src/cli/self_update.rs` builds the tag as `.map(|v| format!("v{v}"))` (line 693, pasted in validation) for a user-supplied VERSION, so the manifest's `v2026.9.13` must be passed as `2026.9.13`. Self-update runs before the release-asset pin bump, so it targets the committed pin; a bumped pin takes effect on the next run after merge.

## Tests (named, as the task asks)

- `tests/install/common/lifecycle.bats`: "update fails when Herdr status fails" became "update skips reload when Herdr status fails" (exit 0 plus the skip line). "rejects missing or unknown" became "skips reload for missing or unknown" and loops over all five unreadable fixtures. These run in CI only (local bats forbidden): the `test (*)` jobs pass.
- `tests/unit/test_apparmor_userns.py` pins the apparmor text:
  - the copy/reload call list now starts with `sudo -n true`;
  - new `test_installer_leaves_the_profile_pending_without_cached_sudo` (exit 0, only `sudo -n true`, remedy on stderr, no "Loaded");
  - `test_installer_fails_when_loading_the_profile_fails` now fails at `sudo -n install`;
  - the doctor "profile missing" assertion pins the new remedy text and keeps `req=1 opt=0`.
- `tests/unit/test_runtime_health.py`:
  - new `test_upgrade_self_updates_mise_to_the_manifest_pin`;
  - `grep` added to the minimal-PATH `test_upgrade_skips_ccr_notice_when_gh_is_unavailable`, because `asset_manifest_pin` pipes through `grep`. Without it that test failed with `grep: command not found` → `required failure: mise self-update`.
- `tests/install/common/lifecycle.bats:273` (`grep -q 'mise self-update --yes'`) still matches the pinned line and is unchanged.

## Validation summary

All outputs are verbatim in `.orchestration/validation/dotfiles-T70-make-update-unattended-a01.md`:
- local gates: `make unit-test` 715 OK (2 skipped); `make validate-agent-assets` ok; shellcheck, shfmt and `bash -n` clean;
- CI: `gh pr checks 238` all pass (nix skipped);
- `mergeable_state` = `blocked`: the bot threads below are unresolved, and threads are not to be resolved by the worker.

## Codex Bot review (head 229a2ec1): two P2, no P0/P1

- `4175388164` Makefile:87 asks README.md:177-180 to describe the warning-and-skip Herdr behaviour.
- `4175388165` apparmor_userns.sh:62 asks README.md:295-300 to describe the pending profile and the manual remedy.
- Proposed disposition for both: `not-applicable: README.md is a T70 forbidden file and the task assigns README wording to T83; carry both README passages into T83`. They are correct about README drift, so T83 must take them. No fix commit was made.

## Reporting notes

- Not run (forbidden): `make update`/`make upgrade`/`make apply`, local bats. The live acceptance (`sudo -K; script -q /dev/null make update`, `herdr server stop; make update`) is the operator's.
- An ad-hoc local check of the Herdr recipe with a fake `herdr` was denied by the permission gate and not retried. CI `lifecycle.bats` is the evidence for that branch.
- The live `~/.claude/settings.json` and every other `home/**` file were untouched.

[memory:decision] dotfiles-T70 (operator 2026-10-03): `make update` converges unattended: Herdr unreachable is a skipped reload, apparmor profile installation uses `sudo -n` with a doctor warning instead of a password prompt, and `make upgrade` keeps mise at the manifest pin; interactive steps belong to the operator phase (`./setup.sh`, `sudo -v` before `make update` when installers changed).

CompactionDB, run in the main checkout outside the sandbox (its state dir is read-only from this worktree's sandbox):

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] text above, verbatim>"
1b3e2eaf-7bed-4b48-a234-dda7568b32b3
```

Note: the operator's decision text says "with a doctor warning". Per PONG decision 1(2) the doctor signal for a missing profile is the existing required failure, not a warning. The memory text was recorded verbatim as the task requires; the orchestrator may want to amend it at consolidation.

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)

## Revise round 1 (task_rev a98960c7…): README passages fixed in the PR

- Fix commit `95acd5b6` `docs(readme): describe the unreachable-Herdr skip and the pending AppArmor profile` changes only `README.md` (9+/3-). `make update` now "fails on reload errors other than `protocol_mismatch`" and, when the Herdr status cannot be read or is unknown, prints `Herdr server unreachable; skipping config reload.` and continues. The AppArmor paragraph says the installer uses `sudo -n` and never prompts. Without cached sudo credentials the profile stays pending, `make doctor` reports it missing, and the remedy is `sudo -v && bash install/ubuntu/common/apparmor_userns.sh` from the repository root. It notes that `make update` does not retry it. `prettier --check README.md` passes, and no test pins the replaced README text (checked by grep).
- `main` moved to `a575b3cc` (#236), so `gh pr update-branch 238` made the final head `71f48b303a716b1f7026f682f96c5e423b4aebea`. On it, CI is all pass (nix skipped), local `make unit-test` (715 OK) and `make validate-agent-assets` pass, and the branch is up to date with `main`.
- Codex Bot: no new review or inline comment on the round-1 heads. It reacted `+1` on the PR at 2026-10-03T23:46:14Z, after the 95acd5b6/71f48b30 pushes; per its own PR note, it comments when it has suggestions and otherwise reacts 👍. The waiting window ended 23:58Z.
- Bot findings `4175388164` and `4175388165`: proposed disposition `fixed:95acd5b6` (README root cause fixed in this PR). Threads left unresolved per the task. `mergeable_state` stays `blocked` until the orchestrator resolves them.
