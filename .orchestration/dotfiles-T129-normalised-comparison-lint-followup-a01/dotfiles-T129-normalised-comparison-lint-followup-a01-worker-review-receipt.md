review_surface: crit-data
reviewer: claude (a fresh general-purpose subagent of the worker seat, read-only, given the task file, the three Bot comments and the commit range, not the worker's conclusions)
review_source: .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/dotfiles-T129-normalised-comparison-lint-followup-a01-worker-crit.json
review_outcome: addressed

Crit reports no review file or daemon in this worktree (no Plan Mode was used), so the AGENTS.md fallback applies: an independent read-only review in the crit-data shape.

- Round 1 on 7c8e7484..37bf6a51: `Verdict: incorrect`, three P2 and two P3. Every record in the JSON is resolved: the two row-1 P2 by the re-plan in 1b56dc2b, with be2958cf's guard tests red at 37bf6a51 (validation §3b); `map(re.escape, …)` and the jq comment fixed in 1b56dc2b; the rest declared as residuals in report.md.
- Round 2 on 37bf6a51..1b56dc2b, same reviewer, context kept: `Verdict: correct`, four P3. The unbalanced-quote fail-open shape is fixed in bb60ee84 (tests in a0563644, red at 1b56dc2b, validation §3c); the joined-word option values (which the base misses too), the R3 object-key forms and the R6 forms are declared residuals in report.md. Its differential fuzz (845,325 lines) found no other shape the base reads and the head does not.

The reviewer ran the unit tests and the lint on each head, compared the base and the head `programs()` over every tracked shell file, and built its own fixtures under `$TMPDIR`; it edited nothing in the repository.

This is worker process evidence, not reviewer authentication and not the task-level audit: the orchestrator owns the sweep, the audit, the dispositions, the gate and the merge.
