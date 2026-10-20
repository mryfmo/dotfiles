---
task: dotfiles-T129-normalised-comparison-lint-followup-a02
head: 1950a4de087261dbfe5bac526de9b9285f7717af
pr: 432
base: 1eac64a832ade83f9e149be6a329f7e8fa20180f
started: 2026-10-19T20:54:19Z
finished: 2026-10-19T20:56:38Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Add a threat-table row for the CI baseline exemption — scripts/lint-comparisons-baseline.tsv:62-62

```text
Reviewed the initial candidate c87546e9 after another process switched the worktree to main. Syntax, ShellCheck, and focused preflight probes passed, but the CI exemption lacks required threat-table coverage; full unit tests were not run in the read-only sandbox.

Review comment:

- [P2] Add a threat-table row for the CI baseline exemption — scripts/lint-comparisons-baseline.tsv:62-62
  This exemption changes the CI-enforced comparison check, but `scripts/lint-comparisons-baseline.tsv` is absent from both `allowed_files` and `threat_table` in the task. The rebase-repair report mentions authorization but supplies no threat disposition for this control. Record the baseline-file amendment and its corresponding threat-table row before acceptance, as required by [AGENTS.md:78](AGENTS.md#L78).
Reviewed the initial candidate c87546e9 after another process switched the worktree to main. Syntax, ShellCheck, and focused preflight probes passed, but the CI exemption lacks required threat-table coverage; full unit tests were not run in the read-only sandbox.

Review comment:

- [P2] Add a threat-table row for the CI baseline exemption — scripts/lint-comparisons-baseline.tsv:62-62
  This exemption changes the CI-enforced comparison check, but `scripts/lint-comparisons-baseline.tsv` is absent from both `allowed_files` and `threat_table` in the task. The rebase-repair report mentions authorization but supplies no threat disposition for this control. Record the baseline-file amendment and its corresponding threat-table row before acceptance, as required by [AGENTS.md:78](AGENTS.md#L78).
```
