---
task: dotfiles-T128-chain-github-scripts-followup-a02
head: c87546e9b8f5093206d9f504d66998e21516f302
pr: 375
base: 1eac64a832ade83f9e149be6a329f7e8fa20180f
started: 2026-10-19T20:22:03Z
finished: 2026-10-19T20:24:40Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Cover the new CI baseline exemption in the threat table — scripts/lint-comparisons-baseline.tsv:62-62

```text
The preflight logic passed syntax, ShellCheck, and targeted checks, but the CI exemption lacks required threat-table coverage. The full unit suite was not run in the read-only sandbox.

Review comment:

- [P2] Cover the new CI baseline exemption in the threat table — scripts/lint-comparisons-baseline.tsv:62-62
  This PR adds an exemption to `scripts/lint-comparisons-baseline.tsv`, which determines whether the required unit check passes, but neither `allowed_files` nor `threat_table` covers that file. The exemption therefore changes a CI control without the required per-path disposition. Amend the task scope and add a threat-table row for the baseline change, as required by [AGENTS.md:78](AGENTS.md#L78).
The preflight logic passed syntax, ShellCheck, and targeted checks, but the CI exemption lacks required threat-table coverage. The full unit suite was not run in the read-only sandbox.

Review comment:

- [P2] Cover the new CI baseline exemption in the threat table — scripts/lint-comparisons-baseline.tsv:62-62
  This PR adds an exemption to `scripts/lint-comparisons-baseline.tsv`, which determines whether the required unit check passes, but neither `allowed_files` nor `threat_table` covers that file. The exemption therefore changes a CI control without the required per-path disposition. Amend the task scope and add a threat-table row for the baseline change, as required by [AGENTS.md:78](AGENTS.md#L78).
```
