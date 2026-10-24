# U45 The `uninstall_*` installer functions have no caller in the test suite — brief (U41 residual)

GOAL
U41 (PR #498) rewrote the client Bats teardowns so they remove only what their case installed; since then no case calls the installers' `uninstall_*` functions, and none ever asserted them (overview.md residuals index, row 1). After this unit every `uninstall_*` function in `install/**` is either asserted by a recorded-call test (the `record_apt_calls` pattern of `tests/install/helpers/apt_record.bash`: the function asks the package manager to remove exactly its install set, and a mutation that drops a package fails the case) or recorded as dead with its removal scheduled, so the suite no longer carries code nobody checks.

SCOPE
One branch `test/uninstall-functions-asserted` from `origin/main` (718407db or later). May write: `tests/install/**/*.bats` and `tests/install/helpers/*` (new recorded-call cases per installer group); `README.md` one line in the test section if the helper's use changes. No change to `install/**` in this unit: a dead `uninstall_*` function is listed in the PR body with the grep evidence, and its removal becomes a follow-up row the orchestrator schedules (installers are audit-seat territory).

CHANGE
1. Inventory first: `git grep -n -E '^(uninstall_[a-z0-9_]+)\(\)' -- install/` and, per function, its callers across the repository (`git grep -n -w <name> -- . ':!.orchestration'`); paste the table (function, file, callers, disposition: `assert` or `dead`).
2. For every `assert` row: a recorded-call case that sources the installer, replaces the privilege wrapper and the package manager with the recording stubs, calls the function, and asserts the removal command names exactly the install set the matching `install_*` function uses (the two sets compared in the test, not hard-coded twice); one permanent mutation case per file (an `uninstall_*` that drops a package fails).
3. For every `dead` row: the PR body lists it with the callers grep showing none; no code change.

ACCEPTANCE
1. The inventory table in the PR body with pasted grep output; every function has a disposition.
2. `grep -c '^ok'` in the client Bats CI step rises by the number of new cases and `not ok` stays 0 (the CI log lines pasted); no real `apt-get` or `dpkg` call added (the step's time stays within 10 s of the U41b run: paste both).
3. CI green on the head; PR body `Program-Unit: regime-cutover/U45`, a threat table (tests only: say so; the stubs never run the package manager), the footer; pre-RESULT five-point self-check; orchestrator verdict (tests only).

TIMEBOX
60 minutes.

FORBIDDEN
No change under `install/**`; no local Bats reported as evidence (CI's Bats jobs are the record); no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 24).
