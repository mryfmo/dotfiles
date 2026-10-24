# U43 The dead-owner lock test orders its setup before the holder — brief (U36 re-plan residual)

GOAL
U36 (PR #497) is HELD at 8154968d after its third incorrect verdict; the audit states that no production finding remains and names one P2 in a regression test (`verdicts/U36-8154968d.md`, F6). This unit removes that residual so U36 can leave HOLD and merge at this unit's head.

SCOPE
The same branch `feat/omp-first-operation` and PR #497. May write: `tests/unit/test_regime_start.py` only. No production file changes; the diff of every non-test file against 8154968d is empty and the RESULT says so with the command (`git diff --stat 8154968d -- . ':!tests/unit/test_regime_start.py'` prints nothing).

CHANGE
1. `test_a_dead_owner_releases_the_lock_at_once` (lines 444-450 at 8154968d): create `self.registry` (parents, exist_ok) before the `Popen` of `HOLDER`; keep the `held` handshake (`readline() == "held\n"`) before any assertion that depends on the lock being held.
2. Check every sibling test that spawns a holder or a paused pass for the same order (the registry or the lock's parent must exist before the child opens the lock file); fix the same way where found and name each in the RESULT.
3. Evidence: the test class run 20 times in a loop locally (`for i in $(seq 20); do uv run python -m unittest tests.unit.test_regime_start -k dead_owner -q || break; done`, exit status and the loop count pasted); the full file once.

ACCEPTANCE
1. The `Popen` of the holder comes after the registry `mkdir` in the named test; no other ordering of a child before its directory remains in the file (grep of `Popen(` against the preceding `mkdir` lines, pasted).
2. CI green on the new head in all four `test` cells; the non-test diff against 8154968d is empty.
3. RESULT with the five-point self-check at push time; the PR body gains one line under the U36c round naming this unit and the finding.

TIMEBOX
30 minutes.

FORBIDDEN
No production change, no `# noqa`/skip, no retry decorators; no merge, rebase, force-push, PR close; no omp subagent (the Task tool kills a seat on the claude-bridge route).

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 23).
