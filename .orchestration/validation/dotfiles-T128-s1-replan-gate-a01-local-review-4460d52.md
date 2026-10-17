---
task: dotfiles-T128-s1-replan-gate-a01
head: 4460d525612b8869f852d2a1d23160c54c272ae4
pr: 382
base: 58303c37a2ac7854ba7f8d4032b5ee2b9c28776e
started: 2026-10-17T04:04:06Z
finished: 2026-10-17T04:07:37Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Use one version-independent tokenizer for both re-plan checks — scripts/regime-counters.sh:177-177

```text
The counter and integration gate disagree on the same re-plan prerequisite under mixed Unicode-table versions. This was reproduced with installed runtimes; the full test suite was not rerun in the read-only sandbox.

Review comment:

- [P2] Use one version-independent tokenizer for both re-plan checks — scripts/regime-counters.sh:177-177
  With macOS jq 1.7.1 and Python 3.14+, a re-plan line containing `design` immediately followed by U+1C89 produces contradictory results: the counter reports `re-plan=present`, but the gate rejects it. jq's older Unicode table treats that character as a separator, while Python includes it in the word. This contradicts the shared grammar promised by the task's re-plan threat-table control ([AGENTS.md:78](AGENTS.md#L78)). Use a shared tokenizer or version-independent boundaries, with a regression test for this mixed-version case.
The counter and integration gate disagree on the same re-plan prerequisite under mixed Unicode-table versions. This was reproduced with installed runtimes; the full test suite was not rerun in the read-only sandbox.

Review comment:

- [P2] Use one version-independent tokenizer for both re-plan checks — scripts/regime-counters.sh:177-177
  With macOS jq 1.7.1 and Python 3.14+, a re-plan line containing `design` immediately followed by U+1C89 produces contradictory results: the counter reports `re-plan=present`, but the gate rejects it. jq's older Unicode table treats that character as a separator, while Python includes it in the word. This contradicts the shared grammar promised by the task's re-plan threat-table control ([AGENTS.md:78](AGENTS.md#L78)). Use a shared tokenizer or version-independent boundaries, with a regression test for this mixed-version case.
```
