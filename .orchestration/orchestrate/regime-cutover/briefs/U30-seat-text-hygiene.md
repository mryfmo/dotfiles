# U30 Seat text hygiene: one command per bash call, bus lines without command names — brief

GOAL
The two policy false negatives of the first orchestrator-seat run stop recurring: the audit seat never loses a verdict to a compound command, and the orchestrator seat never has a TASK line refused because the prose in it names a denied command. Both are fixed where they arise, in the skills the seats follow and in the policies' README, with tests on the skill text.

SCOPE
One branch `docs/seat-text-hygiene` from `origin/main`. May write: `home/dot_agents/skills/hcom-audit/SKILL.md`, `home/dot_agents/skills/hcom-worker/SKILL.md`, `home/dot_agents/skills/hcom-orchestration/SKILL.md`, `home/dot_agents/omp/policies/README.md`, and the test that pins those skills' sentences (find it: `grep -rl hcom-audit tests/unit/ | head`; add one if none). Nothing else; no policy row changes.

CONTEXT (measured 2026-10-24, O1 run)
- audit-tomo ran `git rev-parse HEAD && git status --porcelain` and was denied by the catch-all (`Blocked by bash pattern: *`), answered `verdict=blocked note=policy-denied-head-and-clean-tree-verification` (bus row 467), and was re-tasked. The policy header says an `allow` must match the whole command and never a compound line (`src/tools/bash.ts:301-307`); the hcom-audit skill does not say "one command per bash call".
- orchestrator-zero's `hcom-dispatch … "AGMSG-TASK … gh pr comment …"` was denied by its own `*gh pr comment*` row because a `deny` matches any one segment of the command line, including quoted message text (pane read 2026-10-24T02:33Z). The hcom-orchestration skill does not say that bus lines carry ids, paths and short notes only and that prose belongs in a brief file.
- Both seats recovered (the orchestrator sent a plain-text TASK; the audit seat ran the two commands separately after a note), so this is a skill-text defect, not a policy defect.

ACCEPTANCE
1. hcom-audit SKILL "Audit" step 1 gains: "One command per bash call: your allow rows match a whole simple command, so `a && b`, `a; b`, `a | b` and a `$(…)` are refused by the catch-all. Run `git rev-parse HEAD` and `git status --porcelain` as two calls." The same sentence, adapted, in hcom-worker (its policy is deny-only, so there it is about deny rows matching any segment: never put a denied command's name inside a quoted argument).
2. hcom-orchestration SKILL step 2 gains: "A bus line carries the kind, `task_id`, `brief=` path, `head=`, `pr=` and a `note=` of at most one sentence without command names; any instruction longer than that goes into a brief or addendum file the line points at. A deny row of your own policy matches text inside the line."
3. Policies README gains a short "Text that policies see" paragraph with the two measured cases and bus rows 467 and the pane read.
4. The skill-text test pins the three new sentences; `make unit-test` green; CI green; PR body `Program-Unit: regime-cutover/U30`, footer.

TIMEBOX
45 minutes.

FORBIDDEN
No policy row changes; no edits outside SCOPE; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (line 20).

ADDENDUM (coordinator, 2026-10-24T05:1xZ): the findings hand-off
Measured in O2: after every `verdict=incorrect`, the worker asked the audit seat on the bus where the findings are (rows 1278, 1294, 1699, 1725) and the audit seat answered in PONG lines (1286, 1299, 1306, 1713, 1721, 1737): four to six extra bus rows per fix round. The audit seat cannot write files (its policy), so the hand-off belongs to the orchestrator. Add to ACCEPTANCE:
5. hcom-orchestration step 4 gains: after a VERDICT with findings, the orchestrator copies the audit seat's `status=findings` PONG text into `verdicts/U<n>-<head>.md` before it sends the fix TASK, and the fix TASK names that file (`brief=<verdicts path>` or `findings=<path>`); the worker reads findings from that file only. hcom-worker gains: a `verdict=incorrect` row is not addressed to you; wait for the orchestrator's fix TASK, never question the audit seat on the bus. hcom-audit gains: the findings PONG is sent once, immediately after the VERDICT line, with every finding's `file:line`, priority and the required fix in one message; scope questions are answered by the orchestrator, not by you.

ADDENDUM 2 (coordinator, 2026-10-24T05:3xZ): the first-pass gate
Measured in O1/O2: five units, five first audits not `correct` (U25 blocked then incorrect, U16 incorrect, U17 incorrect, U18 incorrect, U25d incorrect twice); each fix round costs the worker's turn plus 10 to 12 minutes of CI per push plus a re-audit, about 20 to 30 minutes, and the findings were always of the kinds AGENTS.md "Audit" lists (fail-open on a producer, missing threat table, a destructive step wider than its guard, an incomplete migration). The worker never reads that list before RESULT and the orchestrator checks only head, SCOPE and CI before tasking the audit. Add to ACCEPTANCE:
6. hcom-worker "Reply" gains a pre-RESULT self-check the worker pastes into its report: (a) every `allowed_files`/SCOPE path and non-path control has a threat-table row when the diff touches a trust boundary (AGENTS.md "Orchestration records and trust-boundary code"); (b) every safety decision reads its producer's exit status and has a failure-injection test (preferences.md line 21); (c) every destructive step is scoped to exactly what the brief authorizes and refuses the rest; (d) a migration changes the installed state through the real path, not only the generated baseline; (e) `make unit-test` and the asset validators ran locally (omp seats have no sandbox) and the summary lines are pasted. A RESULT without the pasted self-check is HELD by the orchestrator.
7. hcom-orchestration step 3 gains the same five checks as the orchestrator's pre-audit gate: a RESULT that fails one gets a `U<n>b` TASK naming the gap before any audit TASK, so the audit seat sees first passes that already meet the written standard.

ADDENDUM 3 (coordinator, 2026-10-24T06:2xZ): a merge error is not a merge failure
Measured on PR #484: the orchestrator seat's first `gh pr merge 484 --squash --match-head-commit 081463a2` got a GitHub 504; the merge had happened (squash b8fa3f00, 4 files, 05:12:01Z); the seat retried and GitHub produced a second, empty squash 4fb8490f (0 files, 05:13:39Z), which the PR now records as its merge commit. Content on `main` is correct once; the record names the empty commit. Add to ACCEPTANCE:
8. hcom-orchestration step 6 gains: after any error from the merge command, re-read `gh pr view <n> --json state,mergeCommit` before anything else; `MERGED` means the merge happened and its `mergeCommit` is the sha to record, so never run the merge command twice for one head; the ledger row names the commit that carries the diff (verify with `git diff <parent> <sha> --stat` non-empty).
