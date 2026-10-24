review_surface: crit-data
reviewer: claude
review_source: .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a02/dotfiles-T129-normalised-comparison-lint-followup-a02-worker-crit.json
review_outcome: addressed

The reviewer was a fresh general-purpose subagent of the worker seat. It worked read-only and was given the task with amendment 1, the two records' owned rows, the audit text and the commit range, not the worker's conclusions.

Crit reports no review file or daemon in this worktree (no Plan Mode was used), so the AGENTS.md fallback applies: an independent read-only review in the crit-data shape.

- **The one pre-push round**, the task's limit, covered `51ba5801..607d4485` and returned `Verdict: incorrect`, with one P1, five P2 and P3 items.
- **Fixed in `5b6c5a8a`,** each with a fixture form red at `607d4485` (validation §4b) and a mutant that its fixture kills (§5a):
  - the P1, a shrinking literal view in the jq scanner;
  - `if`/`end` as one operand;
  - whole shell words for `pgrep` and `grep`;
  - markers past a closing quote, and on any line of a continued statement;
  - multi-line double-quoted programs;
  - three P3s.
- **Residuals (P3, recorded):** a double-quoted program starting with an expansion; escaped joins through `sorted` or a set comprehension, refused conservatively.
- **The reviewer's own checks:**
  - all fixtures red at main's lint and green at the head;
  - every mutant of the nine gap fixes killed;
  - the `--all` tree comparison agrees with validation §8;
  - `--list-rules`, the caps and ruff are clean.

This is worker process evidence, not reviewer authentication and not the task-level audit. The fix round counts toward INV-6. The orchestrator owns the audit, the sweep, the dispositions, the gate and the merge.
