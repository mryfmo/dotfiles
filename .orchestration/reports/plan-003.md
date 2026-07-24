# Plan 003 executor report

## Result

- Status: DONE
- Final PR head: `22f9ec0b914e357923a241ec9f02d82e44da9409`
- Merge: PR #69, `69e2338489e22d5279ca3fdf6917f0cbe5950400`
- Branch/worktree: `orchestrator/plan-003` at `/private/tmp/dotfiles-plan-003`
- Base: `c3e69ade4d3700b4d624416ce2e5d59b31dce191`
- Push/PR/merge: completed; https://github.com/mryfmo/dotfiles/pull/69

Final independent acceptance is recorded in
`.orchestration/acceptance/plan-003-final-pr.md` with verdict `ACCEPT`.
All 15 exact-head visible checks and all six post-merge workflows passed.

## Files

- `.github/workflows/remote.yaml`
- `README.md`
- `home/.chezmoi.yaml.tmpl`
- `install/ubuntu/common/dependencies.sh`
- `setup.sh`
- `tests/install/common/setup.bats`
- `tests/install/ubuntu/common/dependencies.bats`
- `tests/install/ubuntu/common/dependencies_unit.bats`

## Phase and task completion

- Phase 1, A001-A003: package tests now model exact `dpkg-query` status for installed, absent, and partial packages; production uses that single oracle and orders one APT update before each non-empty batched install. Sudo bootstrap reuses that update.
- A004: local shell/Python gates passed. Ubuntu client/server Bats proof is authored but intentionally not run locally; GitHub CI proof awaits an authorized push.
- Phase 2, A005-A007: `fetch_url` prefers curl, falls back to wget, emits one deterministic no-fetcher error, and handles both Homebrew and chezmoi text downloads. Installer text is captured in a checked assignment before execution; partial output from a nonzero fetch is not executed. The wget-only Linux fixture covers init/status/diff/apply.
- Phase 3, A008-A010: tests cover clean, first-column drift, second-column-only target state, failed status/diff/apply, hashes, and modes. Init/update are allowed to change source/config state; drift/status/diff failures do not mutate destination targets. Fake apply mutates a target before failing, and the nonzero result is asserted without rollback. README documents the same boundary and recovery.
- Phase 4, A011-A013: public and optional private jobs are separated. The public Ubuntu client/server and macOS client matrix checks out the tested revision, uses a temporary HOME without secrets, validates checkout/source SHA equality, and protects three sentinels.
- A014: branch-locality assertions and SHA logging are implemented. The temporary-marker PR experiment and workflow-log confirmation were not run because push/PR creation was forbidden.
- Phase 5, A015-A017: exact client/server/macOS role render cases and invalid persisted/prompted cases were added; the config input boundary accepts only `client` or `server` before YAML output.
- A018: all permitted local gates passed. Bats, push, and GitHub matrix acceptance remain for the orchestrator after authorization.

## Deviations and limitations

- No Bats command was run locally, per repository and task policy.
- No GitHub CI, fork/Dependabot run, temporary PR marker run, push, PR, or merge is claimed.
- `actionlint` and `yamllint` were unavailable and were not installed. The workflow passed the available Ruby YAML parser and manual/static workflow audit.
- The first Ruby YAML call used a Ruby-newer `aliases:` keyword and failed on system Ruby 2.6; the compatible `YAML.load_file` call then passed.
- The first Crit receipt used a descriptive suffix after `approved`; the guard requires the exact enum and correctly rejected it. The receipt was changed to `review_outcome: approved`, then the evidence gate passed.

## STOP-condition audit

- Chezmoi v2.70.5 help and the official status documentation agree that column 1 is last-written versus actual state; no parser STOP.
- Public macOS uses `${{ runner.temp }}/dotfiles-home`; no real runner HOME isolation STOP identified.
- Public bootstrap uses no private credential in its job; runtime network behavior awaits CI but no clean-image credential requirement was introduced.
- Role allowlist exists only at `home/.chezmoi.yaml.tmpl` and in tests; no duplication STOP.
- Plan 001 is merged at `3826729`, an ancestor of the task base; no dependency STOP.

## Negative-risk assessment

The change removes forced overwrites, blocks CI apply outside the isolated HOME, preserves unmanaged sentinels, prevents destination-target mutation before apply, returns nonzero on partial apply failure, and rejects invalid roles before persistence. It intentionally provides no apply rollback. Remaining risk is execution-environment compatibility in the unrun GitHub Bats/public matrix, especially local-checkout cloning and clean macOS bootstrap behavior; the workflow contains direct SHA, role, file, hash, and mode assertions to expose those failures.

## Adversarial review round 1 revision

- Addressed every finding in `plan-003-review-round-1.md` in a new commit; the original commit was not amended.
- `dpkg-query` exit 1/non-installed state is missing, while exit 2 is fatal and propagates without APT calls.
- Fake PATH tools resolve host commands with `command -v`, including `cat`; no `/bin/find` assumption remains.
- Workflow permissions are top-level `contents: read`, and both checkouts use `persist-credentials: false`.
- Crit data has resolved revision record `r_2d91af`; the receipt gate passed before commit.
