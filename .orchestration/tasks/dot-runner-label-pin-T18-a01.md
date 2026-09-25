# AGMSG-TASK dot-runner-label-pin-T18-a01: pin GitHub runner images explicitly (plan Phase G.3)

Evidence: every ubuntu job on PRs #178/#180 carries the notice "The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026" (actions/runner-images#14748). The workflows use `ubuntu-latest` and `macos-14`; the Dockerfile and installers target Ubuntu 24.04.

Repo: nested worktree, branch `chore/runner-label-pin` after T17. You are `claude-standard-dot-a003`.

## Required changes
1. Replace `ubuntu-latest` with `ubuntu-24.04` in every workflow matrix/`runs-on` (`test.yaml`, `agent-assets.yml`, `docs.yml`, `remote.yaml`, `ubuntu.yaml`, `macos.yaml` as applicable) so CI matches the supported OS, and add a comment referencing the migration issue. Keep `macos-14` unless the installers document another version.
2. Add the runner images to the asset manifest (T15) as declared inputs (`ci.runners`) so Renovate/doctor can track them (Renovate `github-runners` manager if available; document).
3. Bats/installer assumptions that depend on the distro (apt package names, PPAs) unchanged; note in README that the CI OS is pinned and that a deliberate Ubuntu 26 migration is a separate task.

## Validation
`gh pr checks` green; annotations no longer contain the migration notice (paste); pr-feedback JSON with dispositions.

## allowed_files
`.github/workflows/*.y*ml`, the asset manifest, README, artefacts.

## Artefacts / Done signal
Standard five + pr-feedback JSON. `[memory:decision]`: "CI runner images are pinned explicitly (ubuntu-24.04, macos-14) and declared in the asset manifest". RESULT via send.sh. max_turns=15.

## Added item (12:36Z): statusline smoke-test timeout is a recurring CI flake
Evidence: PR #182 run 36135142111, step "Smoke-test statusline tools without network": `subprocess.TimeoutExpired: Command ['.../npm-ccstatusline/2.2.30/bin/ccstatusline', '--version'] timed out after 5 seconds` (scripts/check-statusline-tools.py:25-43), while main runs 36135228178 (12:29Z) and 36123944643 passed the same step. Root cause: a fixed 5 s budget for a cold Node CLI start on a shared runner. Fix at the root, not by rerunning: measure the cold-start distribution on ubuntu-24.04/macos-14 (paste), then either warm the binary once before timing, raise the budget to a justified value with a comment, or make the smoke check assert the version from the installed package metadata (`mise where` + package.json) instead of executing the CLI when only the version is needed. Add a unit test for the chosen behaviour. Every rerun of a flaky job must be dispositioned with this task id in the PR's pr-feedback JSON.
