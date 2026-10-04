# Acceptance: dotfiles-T70-make-update-unattended-a01

- **Decision:** ACCEPTED after one revise round. PR #238 squash-merged to `main` as `523fda06` (final head `71f48b303a716b1f7026f682f96c5e423b4aebea`, substantive commits 229a2ec1 and 95acd5b6; base `c6de5156`, update-branch onto `a575b3cc`). Merged without `--delete-branch`; worker-d holds `fix/make-update-unattended`.
- **Worker:** `claude-standard-dot-a006` (worker-d). task_rev `360d8aa8…` → `bc0e79e9…` (PONG decision 1) → `a98960c7…` (revise round 1); all matched. Parallel wave 1 with T64 (a005) and T65 (a007); pulled forward from Phase 3 because it was independent of every in-flight task.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 3, dotfiles-T70 (principle 8: the lifecycle converges unattended).

## What was accepted (8 files, +85/−36)

- `Makefile` `update`: a failing, unparsable or unknown `herdr status server --json` becomes `unreachable` → `Herdr server unreachable; skipping config reload.` and the target continues to `agmsg-bootstrap`; running/protocol_mismatch/not_running/absent paths unchanged; operator-phase definition as a comment block.
- `install/ubuntu/common/apparmor_userns.sh`: `sudo -n true` guard leaves the profile pending with the standalone remedy `sudo -v && bash install/ubuntu/common/apparmor_userns.sh` (PONG decision 1: the chezmoi `run_onchange` wrapper records the skipped run and does not rerun on identical content); `sudo -n install`/`apparmor_parser`; the `Loaded…` line moved into `install_profile`.
- `scripts/check-tools.sh`: the REQUIRED failure for a missing profile is kept (the Claude sandbox cannot run without it); only its stale remedy text changed (decision 1(2): no duplicate `warn_optional`).
- `scripts/upgrade-tools.sh`: `mise self-update --yes "${mise_pin#v}"` from `asset_manifest_pin mise` (VERIFY: mise `self_update.rs` prepends `v`).
- Tests: `lifecycle.bats` skip-and-continue cases; `test_apparmor_userns.py` pending/failing/remedy cases; `test_runtime_health.py` pin test and `grep` on the minimal PATH.
- README (95acd5b6): the Herdr warning-and-skip behaviour and the pending-profile remedy, fixing the two Codex P2s at the root (README was added to the allowed files in revise round 1 rather than deferring to T83).

## Audit

| commit | verdict | findings → disposition |
|---|---|---|
| 229a2ec1 | incorrect | P2 README:179 Herdr contract → fixed:95acd5b6; P2 README:297 profile promise → fixed:95acd5b6 |
| 95acd5b6 | correct | — |

## Codex Bot / sweep

- 2 threads (both README drift) fixed in 95acd5b6, replied and resolved; Bot thumbs-up on 95acd5b6 with no new finding. Sweep (head 71f48b30): 13 items, 0 failure/warning, all dispositioned.

## Gate

- `.claude/worktrees/orchestrator-review` at 71f48b30 with evidence copies: `BASE=origin/main PR_FEEDBACK_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` exit 0; copies removed.

## CompactionDB

- Worker decision `1b3e2eaf-7bed-4b48-a234-dda7568b32b3` (recorded verbatim, says "doctor warning"); amended at acceptance: the doctor signal for a missing profile is the existing required failure (see the acceptance-time `memory add`).

## Operator follow-up (live acceptance)

- After `make update`: `sudo -K; script -q /dev/null make update` exits 0 with no password prompt; `herdr server stop; make update` exits 0; if `make doctor` reports the profile missing, run `sudo -v && bash install/ubuntu/common/apparmor_userns.sh` once.
