# Plan 004 Validation Evidence

## Repository

- Base: `69e2338489e22d5279ca3fdf6917f0cbe5950400`
- Head: `208aeb3cce50b3a4925768c3c90ee043a7b40f75`
- Commit: `208aeb3 feat(supply-chain): pin and verify external inputs`
- Source status after commit: clean.

## Passing local gates

| Validation | Result |
|---|---|
| `make unit-test` | PASS, 100 tests |
| `make validate-agent-assets` | PASS |
| ShellCheck on changed shell entrypoints | PASS |
| shfmt diff on changed shell entrypoints | PASS, no diff |
| Bash syntax on changed shell entrypoints | PASS |
| PyYAML parse of six workflows and Dependabot | PASS |
| immutable external Action scan | PASS, no matches |
| rolling mise scan | PASS, no matches |
| remote pipe-to-shell scan | PASS, no matches |
| live latest-release template scan | PASS, no matches |
| Nix 25.05 release-policy scan | PASS, no input/doc command matches |
| `git diff --check` | PASS |
| strict mise dry-run with mise 2026.7.5 | PASS |
| strict mise dry-run with pinned bootstrap mise 2026.5.9 | PASS |
| Crit-data guard | PASS with resolved record `r_c2dd1f` |

## Reproducibility and provenance

- `mise lock -g --platform linux-x64,linux-arm64,macos-x64,macos-arm64` ran twice with 133/133 platform entries, zero skipped, no warnings/errors, and identical final SHA-256 `b85e207137e77d5d6b3464171652e2d878baec8ebb2a63f9b86c4fa9d412264e`; config completeness and strict install tests passed.
- Sheldon rendered client configuration into an isolated HOME, cloned all ten repositories at their exact `rev`, and produced identical lock SHA-256 `43cb4f286ad9344654d046deb51054c458486691a097b2e42dc8c2f0836d309e` twice with no unused-key warning.
- crates.io metadata and downloaded Sheldon crate both reported `43a2d8fc0be4474cfe2d603992c7e9765c9a0f87465aabcfc0603c1de4290b4d`; packaged `Cargo.lock` was present.
- Homebrew pinned installer bytes matched `99287f194a8b3c9e6b0203a11a5fa54518be57209343e6bb954dec4635796d9d`.
- Nerd Font and LINE Seed downloads matched all committed external SHA-256 values.
- `gh` verified each Action SHA against its tag/branch and verified every Sheldon revision belongs to its declared repository.

## Adversarial results

- Temporarily changing only `ubuntu.yaml` from `contents: read` to `contents: write` failed the exact-map test naming expected/read versus actual/write; reverted and green.
- Temporarily restoring `node = "latest"` failed the rolling-version test; reverted and green.
- Actual Sheldon 0.8.5 warned that `commit` was unused; replacing it with `rev` caused lock output to show each exact SHA.
- A wrong chezmoi external checksum returned nonzero while preserving the existing destination sentinel.
- Corrupt/missing installer checksum paths do not execute the fixture payload.
- Strict mise dry-run rejected the temporarily incomplete yq lock even though `mise lock` had exited zero after API rate exhaustion; authenticated regeneration repaired all four entries.

## Crit-data

- `crit status --json` located `/Users/mryfmo/.crit/reviews/dc1955a5d7dc/review.json`.
- `crit comments --all --json` was saved inside the Plan 004 worktree at `.agents/worklog/codex/crit-plan-004.json`.
- Evidence contains one substantive resolved review record and no unresolved comments.
- Receipt: `.agents/worklog/codex/crit-plan-004-receipt.md` with `review_surface: crit-data`, `reviewer: codex`, `review_outcome: addressed`.

## Not run / limitation

- Bats and public bootstrap matrices: CI-only by repository policy; no push authorization.
- Nix lock/evaluation: `nix` and Docker are unavailable. `flake.lock` is deliberately absent and A030/A031 remain incomplete.
- After an authorized push and draft PR, the PR workflow generates and uploads a lock from both GitHub-hosted OS runners, evaluates all declared outputs, then intentionally fails until the generated lock is committed. (`workflow_dispatch` becomes independently usable only after that trigger exists on the default branch.)
