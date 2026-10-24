# U41b The tailscale case tracks no package and its teardown leaves tailscale installed — brief (U41 residual)

GOAL
`main` e7bb65b5 (U41) merged at b1f1337c one minute before the worker pushed caa748cf, the fix for Codex P2 4367052733: `install/ubuntu/client/tailscale.sh` defines no `PACKAGES`, so the tailscale case passes an empty list to `install_real_packages`, tracks nothing, and its teardown leaves tailscale installed on the runner. This unit lands exactly that fix.

SCOPE
One branch `test/tailscale-case-tracks-nothing` from `origin/main` (e7bb65b5 or later) carrying exactly the content of caa748cf: `tests/install/ubuntu/client/tailscale.bats` and `tests/install/helpers/apt_record.bash` (the empty-list guard), +10/-3. Nothing else.

ACCEPTANCE
1. `git diff origin/main..HEAD --stat` shows the two files, +10/-3; the diff equals `git show caa748cf` modulo context (paste the `diff <(git show caa748cf --format= ) <(git diff origin/main..HEAD)` result or the two stats).
2. CI green on the head; the `test (ubuntu-24.04, client)` Bats step shows the tailscale case `ok` and the teardown removing tailscale (the step log lines pasted); `grep -c '^ok'` still 151.
3. PR body `Program-Unit: regime-cutover/U41b`, the Codex disposition line (`fixed:<sha>` for 4367052733 on PR #498 and this PR), the footer; pre-RESULT five-point self-check; orchestrator verdict.

TIMEBOX
20 minutes.

FORBIDDEN
No other change; no merge, rebase, force-push, PR close; no omp subagent.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 23).

ADDENDUM (orchestrator-sari, 2026-10-24T12:2xZ): the brief's `Program-Unit: regime-cutover/U41b` was wrong; `scripts/orchestrator/regime-ci.py:20` accepts `U[0-9]+` only, so the regime check failed at ef3f82d7 ("no Program-Unit line"). The PR body's line is `Program-Unit: regime-cutover/U41` (the parent id, the U25d precedent); the unit id stays U41b in the records and the commit message.
