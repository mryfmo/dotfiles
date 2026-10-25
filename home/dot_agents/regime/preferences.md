# Standing orders (paste verbatim into every spawn and resume)

Copied by `regime-init` from `~/.agents/regime/preferences.md`: the host-independent standing orders of the hcom regime. Add the program's own decisions below the list; the numbering is the reference in TASK lines and audits.

1. The program runs through the omp seats on the hcom bus: the orchestrator seat (`hcom-orchestration` skill) tasks the worker seat (`hcom-worker` skill) and verifies a head itself or with one fresh `omp-run.sh --role audit` run per head. A TASK line names the brief by its absolute path in the orchestrator's checkout.
2. `main` is PR-only. Never push to `main`. One branch per unit, one writer per worktree. Only the orchestrator merges, through `~/.local/bin/common/pr-merge.sh <pr> --records <store>`, which runs `gh pr merge --squash --match-head-commit <head sha>` only when CI is green on that head and the ledger's newest row for that full sha is `correct`.
3. No force-push, no rebase or retarget of a branch you do not own, no PR close, no `rm -rf` outside your own worktree or `$TMPDIR`, no edits outside the brief's SCOPE paths.
4. Never modify the real `~/.omp`, `~/.claude` settings or hooks, `~/.codex`, or the Keychain. Dry-run under a scratch `HOME`. A step that needs a browser login, the Keychain, or an interactive prompt is reported as an exact command for the operator, never run.
5. Every claim in a report carries pasted output or a `file:line`. A handout row for the operator carries two extra columns, `source` (doc or `file:line` defining the command's behaviour) and `dry-run` (a scratch-HOME run and its output, or `operator-only: <reason>`). An instrument that cannot show the failure it should detect is refused.
6. Secrets (tokens, keys, cookies) are never printed, logged, or written. Redact in receipts and reports.
7. Vendored third-party code enters the repo as a pinned tarball (sha256) plus `.patch` files, never as an edited copy.
8. Shell scripts carry shdoc comments in English. Tests assert behaviour the user observes. A known shortcut carries `shortcut: <limit>, <when to upgrade>`.
9. Network only to the hosts the brief names. Wrap any command that could block in `perl -e 'alarm <s>; exec @ARGV' …`.
10. The verifier of a unit runs in a fresh context and, where the tool allows, on a different model than the worker.
11. Respect TIMEBOX. On expiry, write partial findings and stop. Never wait on a human.
12. REPORT shape: status, branch, head sha, PR, verdict, what you ran (commands and pasted output), deviations from the brief, suggested follow-ups. Facts only.
13. Code, records, commit messages and PR descriptions are English.
14. CI must be green before a unit is `landed`. Bot review comments are fixed at root cause or dismissed with a pasted refutation; never suppressed.
15. Every program PR body carries its own line `Program-Unit: <program>/U<n>`.
16. Fail closed on every producer: a safety decision reads a producer's exit status and distinguishes "the read failed" from "the read returned nothing"; a read failure aborts the destructive step with a message naming the file; every such decision carries a failure-injection regression test. A `$(…)` or `<(…)` whose status is not checked is a defect, not a style point.
17. Residuals: a bot, CI or audit finding that is not fixed in the head is never silently "accepted". It becomes either a scheduled unit in `units.tsv` with a brief and a containment gate that holds until it lands (allowed for P2 and P3), or a permanent acceptance in the operator's own words in `decisions.tsv` (the only form allowed for a P1).
18. Before the RESULT line the worker pastes the five-point self-check: a threat-table row per SCOPE path and non-path control when the diff touches a trust boundary; each safety decision's producer status and its failure-injection test; each destructive step scoped to what the brief authorizes; a migration through the real path, not only the generated baseline; the local test and validator summary lines.
