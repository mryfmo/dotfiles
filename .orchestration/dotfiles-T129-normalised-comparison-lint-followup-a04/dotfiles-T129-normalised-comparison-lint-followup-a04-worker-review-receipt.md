review_surface: crit-data
reviewer: claude
review_source: .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/dotfiles-T129-normalised-comparison-lint-followup-a04-worker-crit.json
review_outcome: addressed

The reviewer was a fresh general-purpose subagent of the worker seat. It worked read-only and was given the task with amendment 1, the commit range and the one deviation to judge, not the worker's conclusions.

Crit reports no review file or daemon in this worktree (no Plan Mode was used), so the AGENTS.md fallback applies: an independent read-only review in the crit-data shape.

- **The one pre-push round** covered `b24d3136..c929569b` and returned `Verdict: incorrect`, with one P2 and seven P3 items.
- **Fixed in `d74204e6`,** each with a fixture and a mutant that its fixture kills (validation §5, 34 of 34):
  - the P2, jq hit lines from decoded rather than source text;
  - the chain scope for markers and normalisers;
  - extglob literals;
  - JSON that is no `File` node;
  - iterative walks;
  - `${#name}`;
  - the two surviving mutants.
- **Kept as the task's Design text, recorded as a limit:** the heredoc exclusion also drops command substitutions inside unquoted bodies.
- **Judged sound, left to the orchestrator:** the lone-include `:` deviation from amendment 1's literal text.
- **The reviewer's own checks:**
  - its red run of the head's tests on b24d3136's lint;
  - the `--all` tree comparison (97 identical lines);
  - the caps (267 of 450, 244 of 1200 at `c929569b`);
  - about a dozen syntax probes (coproc, select, arithmetic for, process substitution, `$"…"`, empty `[ ]`).

This round is a04's correction round 1 of 2 under INV-6. This is worker process evidence, not reviewer authentication and not the task-level audit. The orchestrator owns the audit, the sweep, the dispositions, the gate and the merge.
