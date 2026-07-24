# PR #69 final acceptance review

**Verdict: ACCEPT**

PR: https://github.com/mryfmo/dotfiles/pull/69  
Reviewed head: `22f9ec0b914e357923a241ec9f02d82e44da9409`  
Reviewed range: `c3e69ade4d3700b4d624416ce2e5d59b31dce191...22f9ec0b914e357923a241ec9f02d82e44da9409` (`origin/main...HEAD`)  
Review date: 2026-07-11 (Asia/Tokyo)

## Prioritized findings

### P0–P2

None. I found no correctness, data-loss, trust-boundary, CI, or regression defect that should block merge.

### P3 / non-blocking observations

1. CodeRabbit's only exact-head review note is a low-value naming nit: `ensure_ccgate_cli` now makes a best-effort attempt and returns success when the optional binary remains absent. The behavior is intentional and correct; renaming it does not improve the acceptance boundary enough to justify churn.
2. The exact-head commit has a hidden Claude check suite (`78841658935`) left `queued` with zero check runs since creation. It is not exposed by `gh pr checks`, is not a required check, and GitHub reports the PR `MERGEABLE` / `CLEAN`. This is external app state, not a failing repository check.

## Acceptance evidence

### Exact scope and head

- `gh` was used first for the PR investigation. GitHub, the local checkout, and the requested review target all reported head `22f9ec0b914e357923a241ec9f02d82e44da9409`; base is `c3e69ade4d3700b4d624416ce2e5d59b31dce191`.
- The complete eight-commit range was reviewed, not only the final commit. It changes 10 files with 502 additions and 104 deletions. `git diff --check origin/main...HEAD` passed.
- The final commit removes the brittle rendered-config grep from `.github/workflows/remote.yaml`; role behavior is instead covered by template tests and end-to-end role-specific artifacts.

### Bootstrap data-loss boundary

- `setup.sh:214-225` initializes/pulls source state without `--force` and with `update --apply=false`. Official chezmoi behavior confirms that `init` applies only when `--apply` is supplied and `update --apply=false` pulls without applying.
- `setup.sh:237-257` fails closed on `status` failure, `diff` failure, or a non-space first status column before destination apply. This matches chezmoi's official status contract: column 1 is last-written versus actual state; column 2 is actual versus target/apply effect.
- `setup.sh:259-266` refuses CI apply unless `HOME` is below `RUNNER_TEMP`, and accurately warns that a failed apply may have completed earlier target operations. It does not claim rollback.
- `README.md:291-308` accurately narrows the guarantee: init/update may change source/config before the gate, pre-apply failures preserve destination targets, and apply is non-transactional.
- `tests/install/common/setup.bats:241-353` covers clean, target-only, local-drift, status-failure, diff-failure, and partial-apply-failure cases. It verifies source/config mutations separately, blocks apply on pre-apply failures, preserves an unrelated sentinel, and demonstrates the partial-apply limitation.

Official references:

- https://www.chezmoi.io/reference/commands/status/
- https://www.chezmoi.io/reference/commands/init/
- https://www.chezmoi.io/reference/commands/update/
- https://www.chezmoi.io/reference/commands/apply/

### Installer fetch and shell semantics

- `setup.sh:49-62` provides curl-first/wget-fallback checked downloads and fails when neither exists.
- Both composed installer call sites capture the download in an assignment and check its status before invoking a shell (`setup.sh:159-161`, `setup.sh:202-203`). Partial output from a failed transfer therefore cannot be executed.
- `tests/install/common/setup.bats:93-154` covers fetcher selection, absence of both tools, exact failure propagation, and non-execution of partial installer output.
- The Ubuntu client wrapper enables `set -Eeuo pipefail` and runs the Ghostty and misc includes in separate subshells (`home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl:1-13`). This isolates their duplicate readonly `PACKAGES` declarations while retaining outer fail-fast sequencing.
- Exact-head Ubuntu client logs show Ghostty installed first and gparted installed afterward, proving that both composed subshells rendered and executed successfully. Ubuntu server did not execute those client installers.

### Runner HOME, checkout-local SHA, roles, and config grep removal

- Both matrices create `HOME` under `RUNNER_TEMP` on the runner and export it through `GITHUB_ENV` before checkout (`.github/workflows/remote.yaml:33-40`, `:95-102`). Exact-head logs show `/home/runner/work/_temp/dotfiles-home`.
- Public bootstrap creates a branch at the checked-out event commit, gives chezmoi the local workspace and branch, then asserts the cloned source HEAD equals `GITHUB_SHA` (`.github/workflows/remote.yaml:42-74`). On this `pull_request` run, checkout and the assertion used merge ref `c2dc2b624c43bb7a92df2591e0996ec6bed55ad7`, which GitHub logged as merging exact head `22f9ec0...` into exact base `c3e69ad...`. This is the intended checkout-local SHA assertion.
- The removed config grep is not needed for correctness. `home/.chezmoi.yaml.tmpl:8-19` accepts only `client` or `server`, including persisted input, and fails before YAML output for anything else. `tests/install/common/setup.bats:3-46` covers both valid roles, macOS defaulting, invalid persisted values, typo, empty, and whitespace input.
- Public matrix jobs additionally require `.zshrc` for clients and `.bashrc` for servers (`.github/workflows/remote.yaml:69-73`). All Ubuntu client/server and macOS client jobs passed at exact head.

### Public/private trust split and token scope

- Workflow-wide permissions are explicitly `contents: read`; unspecified token permissions are therefore none (`.github/workflows/remote.yaml:12-13`). Both checkouts use `persist-credentials: false` (`:38-40`, `:100-102`).
- The built-in `GITHUB_TOKEN` is exposed to the actual bootstrap command only at step scope (`:42-45`, `:114-119`), allowing authenticated public release lookups without a persisted checkout credential or write permission.
- The public job has no repository private secret, private deploy key, or private email. Private-secret expressions and SSH setup exist only in `private-bootstrap` (`:76-125`). Private restoration requires both secret-presence flags and a non-Dependabot actor.
- GitHub's official model states that `pull_request` workflows from forks receive a read-only `GITHUB_TOKEN` and no repository secrets. Thus public fork PR validation still has the read token it needs, while the private steps fail closed. The exact-head run observed all three private jobs taking the explicit skip path with both flags false; no deploy key or email step ran.

Official references:

- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions
- https://docs.github.com/en/actions/concepts/security/compromised-runners
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- https://github.com/actions/checkout

### Package detection and optional ccgate semantics

- Ubuntu package detection queries each exact package name with `dpkg-query -W -f='${Status}'`, skips only exact `install ok installed`, treats exit 1 as absent, and propagates every other query failure (`install/ubuntu/common/dependencies.sh:51-77`). It refreshes apt only when packages are missing.
- `tests/install/ubuntu/common/dependencies*.bats` cover exact package inventory, all-installed early return, absent and partial states, update-before-install, sudo bootstrap, and fatal query status 2 with no apt call.
- `scripts/update-agent-assets.sh:248-265` tries existing ccgate, best-effort mise installation, retries discovery, then explicitly returns 0 when still missing. Under the script's `set -e`, this preserves optional runtime-verification semantics without hiding the diagnostic.

### Tests, docs, and regression surface

- Exact-head GitHub Actions exposed 15 PR checks, all successful: 6 Snippet install jobs, 4 Unit test jobs, 2 Ubuntu jobs, 1 macOS job, 1 Agent assets job, and CodeRabbit.
- Exact-head Actions history contains five workflow runs, all successful: Snippet install `29136185943`, Unit test `29136185937`, Ubuntu `29136185939`, macOS `29136185933`, and Agent assets `29136185982`.
- The Unit test matrix ran Bats in GitHub Actions on Ubuntu client/server and macOS client. Logs show the new role, fetch, data-boundary, and package tests passing; Python reported 86 tests passing; shfmt and agent asset validation passed.
- The public bootstrap matrix ran real installers on Ubuntu client/server and macOS client. All sentinel checksum/mode checks, role artifact checks, and checkout-local SHA assertions passed.
- Documentation explicitly covers recovery, source/config side effects, partial apply, no rollback, and rerun guidance (`README.md:291-308`). Shell changes retain concise English shdoc-compatible annotations where behavior changed.

## GitHub reviews, comments, and hidden suites

- `gh pr checks` reports all 15 visible checks passing.
- Commit check-suites API reports seven suites: five completed-success GitHub Actions suites, one completed-success CodeRabbit suite, and one queued Claude suite with zero runs. Legacy commit statuses total zero.
- CodeRabbit check output is success. Its top-level output reports one docstring-coverage warning; that generic warning is not actionable for this Bash/YAML-focused diff. The exact-head review contains only the non-blocking ccgate function-name nit described above.
- GraphQL reports `reviewThreads.totalCount = 0`; REST reports zero inline review comments. There are no unresolved or outdated review threads. The sole submitted review is CodeRabbit `COMMENTED` on exact head. `reviewDecision` is unset, not changes-requested.
- GitHub reports `mergeable = MERGEABLE`, `mergeStateStatus = CLEAN`.

## Observed and unobserved limitations

Observed:

- Exact-head public bootstrap completed on Ubuntu client, Ubuntu server, and macOS client.
- Sentinel content and modes survived; checkout-local merge SHA matched the chezmoi source; client/server output artifacts existed.
- GitHub-hosted Bats, Python tests, formatting, platform builds, agent validation, and CodeRabbit all passed.
- Private jobs skipped without secret setup when their secret-presence flags were false.

Not directly observed:

- Private restoration did not run at exact head because both private secrets were unavailable. Its conditional wiring was reviewed statically, but no exact-head private clone/apply execution evidence exists.
- No actual fork-origin PR run was available for this head. Fork safety is established from the workflow structure plus GitHub's official token/secret guarantees, not a live fork event.
- The hidden Claude suite never created a check run. It provides no review signal, positive or negative.
- Local Bats was intentionally not run. No source file, GitHub state, review thread, comment, branch, or commit was modified during this acceptance review.

## Merge readiness

**Ready to merge.** The requested bootstrap safety boundaries, runner isolation, exact checkout testing, public/private trust split, least-privilege token handling, installer failure semantics, optional ccgate behavior, exact package detection, role validation, tests, and documentation are coherent at exact head. The remaining observations are either explicitly non-required external app state or transparently documented coverage limits, not merge blockers.

REVIEW-RESULT v1 task_id=plan-003-final-pr verdict=ACCEPT head=22f9ec0b914e357923a241ec9f02d82e44da9409 report=.orchestration/acceptance/plan-003-final-pr.md
