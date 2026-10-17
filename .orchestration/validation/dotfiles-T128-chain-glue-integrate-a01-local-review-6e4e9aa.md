---
task: dotfiles-T128-chain-glue-integrate-a01
head: 6e4e9aa1bbbbac7828c1bdea86cb2dfe68f719ea
pr: 372
base: 1d41812678366506151579ce3e2ac96b20e8d4b5
started: 2026-10-16T22:13:26Z
finished: 2026-10-16T22:17:41Z
findings: 4
engine: codex review --base main (profile review, read-only)
---

- [P1] Disable forced formatting for machine-readable gh output — scripts/orchestrator/chain-integrate.sh:154-156
- [P2] Add a threat row for main-checkout script integrity — .orchestration/dotfiles-T128-chain-glue-integrate-a01/task.md:23-24
- [P2] Retry when required checks have not appeared yet — scripts/orchestrator/chain-integrate.sh:108-109
- [P2] Verify the review checkout's local main reference — scripts/orchestrator/chain-integrate.sh:88-88

```text
The chain can reject healthy integrations and review against a stale base in an accepted checkout configuration. Syntax and ShellCheck passed; runtime tests were not executed in the read-only sandbox.

Full review comments:

- [P1] Disable forced formatting for machine-readable gh output — scripts/orchestrator/chain-integrate.sh:154-156
  Herdr panes export `CLICOLOR_FORCE=1`, but these direct `gh` calls inherit it. Consequently, comment objects can contain ANSI color sequences, making the generated comments file invalid JSON and causing `fill_sweep.py` to abort healthy integrations. Disable forced color and terminal formatting for these calls, as `scripts/pr-feedback.py::gh_env` already does.

- [P2] Retry when required checks have not appeared yet — scripts/orchestrator/chain-integrate.sh:108-109
  Immediately after `update-branch`, GitHub may expose the new head before registering its check runs. In that interval, `gh pr checks --watch` exits 1 with `no checks reported` rather than waiting, so this code incorrectly aborts a healthy chain as failed CI. Retry that condition until checks appear, while continuing to reject actual check failures.

- [P2] Verify the review checkout's local main reference — scripts/orchestrator/chain-integrate.sh:88-88
  For an independent review clone, which these preconditions and tests permit, fetching `origin main` updates `origin/main` but leaves its local `main` branch unchanged. After the base advances, `local-review.sh` still computes its comparison and invokes Codex with `--base main`, so it reviews already-merged base changes alongside the PR. Align or verify that local reference against the trusted main checkout, or require a linked worktree sharing its references.

- [P2] Add a threat row for main-checkout script integrity — .orchestration/dotfiles-T128-chain-glue-integrate-a01/task.md:23-24
  The new tracked-file and `diff HEAD -- scripts` checks protect a separate trust boundary: checkout contents executed with orchestrator credentials. This table covers the branch name and binary resolution, but neither it nor the canonical task contains a row for script-content integrity. Add a row tied to `test_integrate_refuses_a_main_checkout_script_that_is_not_heads` and update both task copies, as required by [AGENTS.md:78](AGENTS.md#L78).
The chain can reject healthy integrations and review against a stale base in an accepted checkout configuration. Syntax and ShellCheck passed; runtime tests were not executed in the read-only sandbox.

Full review comments:

- [P1] Disable forced formatting for machine-readable gh output — scripts/orchestrator/chain-integrate.sh:154-156
  Herdr panes export `CLICOLOR_FORCE=1`, but these direct `gh` calls inherit it. Consequently, comment objects can contain ANSI color sequences, making the generated comments file invalid JSON and causing `fill_sweep.py` to abort healthy integrations. Disable forced color and terminal formatting for these calls, as `scripts/pr-feedback.py::gh_env` already does.

- [P2] Retry when required checks have not appeared yet — scripts/orchestrator/chain-integrate.sh:108-109
  Immediately after `update-branch`, GitHub may expose the new head before registering its check runs. In that interval, `gh pr checks --watch` exits 1 with `no checks reported` rather than waiting, so this code incorrectly aborts a healthy chain as failed CI. Retry that condition until checks appear, while continuing to reject actual check failures.

- [P2] Verify the review checkout's local main reference — scripts/orchestrator/chain-integrate.sh:88-88
  For an independent review clone, which these preconditions and tests permit, fetching `origin main` updates `origin/main` but leaves its local `main` branch unchanged. After the base advances, `local-review.sh` still computes its comparison and invokes Codex with `--base main`, so it reviews already-merged base changes alongside the PR. Align or verify that local reference against the trusted main checkout, or require a linked worktree sharing its references.

- [P2] Add a threat row for main-checkout script integrity — .orchestration/dotfiles-T128-chain-glue-integrate-a01/task.md:23-24
  The new tracked-file and `diff HEAD -- scripts` checks protect a separate trust boundary: checkout contents executed with orchestrator credentials. This table covers the branch name and binary resolution, but neither it nor the canonical task contains a row for script-content integrity. Add a row tied to `test_integrate_refuses_a_main_checkout_script_that_is_not_heads` and update both task copies, as required by [AGENTS.md:78](AGENTS.md#L78).
```
