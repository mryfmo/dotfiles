# T33g report — dot-ua-core-build-shim-T33g-a01 (revision 2)

- worker: `claude-standard-dot-a005`; orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `fix/ua-core-build-shim` from `origin/main` = `4bc28b7`, with no rebase; revision 2 was continued on the same branch
- task_rev:
  - rev1 sha256 `0c9f8d5b6f60bac2d060d3ae6650262e5258eca474e7ee284e9786d86579e23d` at `4bc28b7`
  - rev2 sha256 `8d79bbf4c3c491f5dc1e3c65487868d62f229999e37c96de2f091e32f695674e` at `553038c`
  - both checked
- PR: https://github.com/mryfmo/dotfiles/pull/202
  - commits: `2f012d2` (item 1) and `02fdac1` (item 2)
  - head: `02fdac1bfed4eb40537accd0c24c11beb29d0d59`
- status: ready_for_review. CI is green on head 02fdac1, including the `test` jobs that run the updated lifecycle.bats; all checks pass except nix, which was skipped. Verbatim `gh pr checks 202` output is in the validation file.

## Process

- **Item 2 blocker.** `tests/install/common/lifecycle.bats` copies the real
  `Makefile` into a fixture and asserts the exact `make update` call
  sequence:
  - L117–127 check full-output equality;
  - L130–133 inject a failure by exact args and grep the exact line.

  Adding `npm:pnpm` would break those CI cases, and lifecycle.bats was
  outside rev1's allowed files. I sent a scoped
  `AGMSG-PONG status=blocked` and continued with item 1.
- **Ruling.** Revision 2 (11:32:00Z) approved option A: update those two
  expectations. lifecycle.bats was added to the allowed files, limited to
  the two cases.

## Changes

1. **`scripts/update-agent-assets.sh`** (`build_understand_anything_core`).
   - **Order.** The pnpm resolution order is now: `mise` present → always
     `mise exec npm:pnpm -- pnpm …`; otherwise `pnpm` on PATH; otherwise the
     WARN.
   - **Why.** A mise shim can exist before the pinned version is installed.
     That was T33f's live failure: `mise ERROR No version is set for shim:
     pnpm`. `mise exec` installs the pin on demand.
   - **Unchanged.** WARN-never-fail and the shared freshness guard. The
     shdoc explains the reason.
2. **`Makefile`**, `update` recipe:
   `mise install --locked npm:ccstatusline npm:ccusage npm:pnpm`, appended
   to the same line, which is the existing pattern. The shim is therefore
   backed after every `make update`.
3. **`tests/install/common/lifecycle.bats`** (rev2, the two approved cases
   only). The full-output equality expectation, the failure-injection args
   and its `grep -q '^…$'` now include ` npm:pnpm`. The Node-failure case
   (`! grep -q '^mise install --locked npm:'`) is unaffected. Bats was not
   run locally, per repo policy; CI runs it.
4. **`README.md`.** The core-build sentence now says pnpm runs "through
   `mise exec`, which installs the pin on demand".
5. **`tests/unit/test_update_agent_assets_ua_core.py`.**
   - (a) `test_prefers_mise_exec_over_an_unbacked_pnpm_shim`: a fake `pnpm`
     that prints `mise ERROR No version is set for shim: pnpm` and exits 1,
     plus a fake `mise` whose `exec npm:pnpm -- pnpm …` works. The build
     goes through `mise exec`, prints no WARN, and the dist is copied.
   - (b) `test_uses_path_pnpm_only_when_mise_is_absent`.
   - (c) `test_make_update_installs_the_pinned_pnpm`: `make -n -f Makefile
     update` contains the new line. This is the same pattern as the
     existing `test_make_update_and_upgrade_include_agmsg_bootstrap`.
   - **Mutation baselines** (verbatim in the validation file):
     - Script tests against the unmodified origin/main script: **1 failure**,
       (a). It reproduces the live failure exactly: the shim error, then
       `WARN: Understand-Anything core build failed`. (b) passes on both
       versions, as a regression guard.
     - The Makefile test against the unmodified origin/main Makefile:
       **1 failure**.
   - After both commits, 12/12 pass in this file, `make unit-test` gives
     511 OK, `make validate-agent-assets` is ok, and `shellcheck -x` and
     `shfmt` are clean.

## Not run / orchestrator-side

- No real `update-agent-assets.sh`, `make update`, `mise install`/`exec`,
  `pnpm` or network install was run. `make -n` is a dry run that prints the
  recipe. Live verification (`make update` with the pin uninstalled and
  dist moved aside) is orchestrator-side.
- The understand-anything auto-update prompts after each commit were not
  run; they are outside allowed_files.

## CompactionDB

[memory:decision] T33g: the Understand-Anything core build always invokes pnpm through
`mise exec npm:pnpm` when mise exists (shim presence is not tool presence), and `make
update` installs `npm:pnpm` explicitly, so a fresh pin is usable on the same run
(operator 2026-09-28, from the T33f live-verification failure).

Id `01d0e8e8-bbcc-4b3b-8597-0675f952bfdc`; the output is in the validation
file. The T33f decision `fff493a7…` ("using a mise-pinned pnpm") remains
accurate and was not retracted.

## Effects

None executed. The shipped `make update` will install `npm:pnpm` 12.4.1
through mise. To remove it: `mise uninstall npm:pnpm`, and revert the pin.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
