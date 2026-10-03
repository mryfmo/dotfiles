# Dotfiles production-hardening implementation plans

Generated from the audit of commit `e7c2808` on 2026-07-11. These plans are
written for an executor that has no access to the audit conversation. Read the
selected plan completely, execute its atomic tasks in order, and do not infer
missing requirements. A STOP condition always wins over task completion.

## Global execution rules

- Work on one plan at a time in the order below. Do not combine plans in one PR.
- Before editing, run the plan's drift check and confirm a clean worktree.
- Add a failing regression test before changing non-trivial logic.
- Do not run Bats locally. Bats runs only in GitHub Actions, per repository
  instructions. Use Python unit tests and static checks locally.
- Do not commit `.agents/worklog/**`, coverage output, caches, or review evidence.
- Before committing a non-empty diff, run `make require-crit-review` and follow
  the repository's Crit-data receipt workflow when it requests review.
- Use Conventional Commits. Push and open/update a PR only when the operator
  explicitly requests it.
- After pushing, wait for every required CI check and every review bot. Fix all
  actionable failures and unresolved comments, rerun local gates, then merge
  only after all required checks are green and review threads are resolved.

## Phases, execution order, and status

| Phase | Plan | Outcome | Priority | Effort | Depends on | Status |
|---|---|---|---|---|---|---|
| 1 | [001](001-contain-starship-cleanup.md) | Starship tests cannot delete unrelated user binaries | P0 | S | — | DONE: PR #67, merge `3826729` |
| 1 | [002](002-make-review-evidence-non-vacuous.md) | Crit review evidence cannot be satisfied by `null` | P0 | S | — | DONE: PR #68, merge `c3e69ad` |
| 2 | [003](003-make-bootstrap-safe-and-publicly-testable.md) | Public bootstrap is dependency-correct, non-destructive, and tested from the PR | P1 | L | 001, 002 | DONE: PR #69, merge `69e2338` |
| 3 | [004](004-harden-and-lock-the-supply-chain.md) | Downloads, Actions, plugins, mise, externals, and Nix are pinned and verifiable | P1 | L | 002, 003 | DONE: PR #70, merge `fa76b4a` |
| 4 | [005](005-make-runtime-health-and-verification-truthful.md) | Runtime helpers self-heal, protect data, and report partial failures correctly | P1 | L | 002, 003, 004 | DONE: PR #72, merge `11d27f5` |

Status values: `TODO`, `IN PROGRESS`, `DONE`, `BLOCKED: <reason>`, or
`REJECTED: <reason>`.

## Audit finding coverage

Every finding from the 2026-07-11 audit is assigned exactly once below.

| ID | Finding | Plan / atomic tasks |
|---|---|---|
| F01 | Starship teardown can remove all of `~/.local/bin` | 001 / A001-A005 |
| F02 | Crit review accepts `null` evidence | 002 / A001-A007 |
| F03 | Public bootstrap CI tests `main`, not the PR | 003 / A011-A014 |
| F04 | Remote installers lack integrity verification | 004 / A001-A009 |
| F05 | GitHub Actions use mutable tags and excess permissions | 004 / A010-A019 |
| F06 | mise uses rolling versions without a lock | 004 / A020-A023 |
| F07 | Agent prompts/logs can be committed or read too broadly | 005 / A001-A004 |
| F08 | Ubuntu package detection confuses package and command names | 003 / A001-A004 |
| F09 | wget bootstrap still requires curl | 003 / A005-A007 |
| F10 | Nix inputs are unsupported and untested | 004 / A029-A033 |
| F11 | Bootstrap force-overwrites without preview/recovery | 003 / A008-A010 |
| F12 | Platform Bats files are empty/placeholders | 005 / A019-A023 |
| F13 | upgrade/doctor report success after required failures | 005 / A005-A010 |
| F14 | Linux system role accepts and persists invalid values | 003 / A015-A018 |
| F15 | Herdr files pane checks label, not Yazi liveness | 005 / A011-A014 |
| F16 | Herdr config updates do not reload the running server | 005 / A015-A018 |
| F17 | Statusline invokes `npx ...@latest` on its hot path | 005 / A024-A027 |
| F18 | chezmoi external evaluation depends on live GitHub APIs | 004 / A024-A028 |
| F19 | ShellCheck is absent from CI | 005 / A028-A031 |

Coverage invariant: `F01` through `F19` must each appear once. If an executor
splits or supersedes a plan, update this table without dropping or duplicating
an ID.

## Dependency rationale

- Plan 001 precedes bootstrap work because CI must be safe before expanding the
  Ubuntu Server test path.
- Plan 002 precedes broad changes because every later plan relies on the review
  gate as a real acceptance control.
- Plan 003 establishes a secret-free, PR-local bootstrap signal before Plan 004
  changes download and version resolution.
- Plan 004 pins the toolchain before Plan 005 asserts runtime behavior against
  those tools.

## Final program acceptance

- [x] Plans 001-005 are `DONE`; none is `BLOCKED` or `IN PROGRESS`.
- [x] F01-F19 are each linked to merged implementation and verification evidence.
- [x] `make unit-test` exits 0.
- [x] `make validate-agent-assets` exits 0.
- [x] `git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x` exits 0.
- [x] `shfmt --indent 4 --space-redirects --diff .` exits 0.
- [x] Secret-free public bootstrap runs from the PR checkout on Ubuntu client,
      Ubuntu server, and macOS client.
- [x] All required GitHub checks pass on the final PR.
- [x] All actionable bot comments and unresolved review threads are resolved.
- [x] A clean-machine canary completes `status -> preview -> apply -> verify` on every
      supported OS/system pair without deleting an unrelated sentinel file.

## Findings considered and rejected

- Root SSH access was not planned: the relevant setup is intentionally guarded
  for container usage, and the audit found no evidence that it affects a host.
- A new installer framework was rejected: existing shell scripts plus direct
  checksum verification are sufficient.
- A custom package/version service was rejected: mise lockfiles, GitHub commit
  SHAs, and upstream checksum files already cover the requirement.
