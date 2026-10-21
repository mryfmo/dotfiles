---
task: dotfiles-T133-task-generator-plan-check-a06-checker
head: 21f52c79336580d40b7c94bb4254ad2d28c2a791
pr: 440
base: 230b36767eec123f90dcd79edca76993d9bb9de7
started: 2026-10-20T12:28:33Z
finished: 2026-10-20T12:38:11Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350

```text
The new authenticated API dependency breaks the existing regime CI caller, and two coverage gaps allow incomplete threat tables to pass. Targeted read-only probes confirmed these issues; the full test suite was not run.

Full review comments:

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
  After this checker lands on main, `.github/workflows/regime.yml` invokes it through `regime-ci.py` without setting `GH_TOKEN` or `GITHUB_TOKEN`. Fresh runners have no GitHub CLI login, so tasks referencing a design or requiring C8/C9 lookups now fail: unauthenticated `gh api` exits 4, and regime-ci reports `no verdict`. Supply the workflow token alongside this change and cover that caller environment in a regression test.

- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350
  With both `scripts/` and `scripts/orchestrator/task-consistency-check.py` allowed, a table containing only the child file's row passes. This prefix check credits that row to the directory, while the new `hits()` logic correctly credits it only to the child; consequently, nothing requires a row controlling the rest of `scripts/`. Validate coverage against each entry's own row, preserving the one-row-per-entry requirement in [AGENTS.md:78](AGENTS.md#L78).

- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
  For an allowed `*.md` scope, adding a concrete row for `AGENTS.md` makes C12 pass even without a row for the existing `CLAUDE.md`. That file controls Claude's instruction import and recovery behavior, as established by [AGENTS.md:5–6](AGENTS.md#L5-L6), so it is not ordinary documentation. Scoped instruction files such as `vendor/compactiondb/AGENTS.md` are likewise missed. Include these instruction files in applied-file classification so wildcard scopes require concrete threat rows.
The new authenticated API dependency breaks the existing regime CI caller, and two coverage gaps allow incomplete threat tables to pass. Targeted read-only probes confirmed these issues; the full test suite was not run.

Full review comments:

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
  After this checker lands on main, `.github/workflows/regime.yml` invokes it through `regime-ci.py` without setting `GH_TOKEN` or `GITHUB_TOKEN`. Fresh runners have no GitHub CLI login, so tasks referencing a design or requiring C8/C9 lookups now fail: unauthenticated `gh api` exits 4, and regime-ci reports `no verdict`. Supply the workflow token alongside this change and cover that caller environment in a regression test.

- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350
  With both `scripts/` and `scripts/orchestrator/task-consistency-check.py` allowed, a table containing only the child file's row passes. This prefix check credits that row to the directory, while the new `hits()` logic correctly credits it only to the child; consequently, nothing requires a row controlling the rest of `scripts/`. Validate coverage against each entry's own row, preserving the one-row-per-entry requirement in [AGENTS.md:78](AGENTS.md#L78).

- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
  For an allowed `*.md` scope, adding a concrete row for `AGENTS.md` makes C12 pass even without a row for the existing `CLAUDE.md`. That file controls Claude's instruction import and recovery behavior, as established by [AGENTS.md:5–6](AGENTS.md#L5-L6), so it is not ordinary documentation. Scoped instruction files such as `vendor/compactiondb/AGENTS.md` are likewise missed. Include these instruction files in applied-file classification so wildcard scopes require concrete threat rows.
```
