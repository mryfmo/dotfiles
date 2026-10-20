---
task: dotfiles-T133-result-precheck-a04
head: 3838d0c6434490c3ce54f8344522d73829f7e655
pr: 411
base: 51ba580149fcace54a912358e7e87c5b07cd8760
started: 2026-10-19T12:41:47Z
finished: 2026-10-19T12:47:08Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Land checker support before sending --premises-sha — scripts/orchestrator/dispatch.sh:337-337
- [P2] Align the merge exemption with the regime CI verifier — scripts/orchestrator/dispatch.sh:230-231

```text
The current checker rejects the new dispatch argument, and the update-branch exemption conflicts with regime CI. Shell syntax, ShellCheck, and shfmt passed; repository-writing tests were not run in the read-only environment.

Full review comments:

- [P1] Land checker support before sending --premises-sha — scripts/orchestrator/dispatch.sh:337-337
  Against the specified base, `task-consistency-check.py` accepts only `--root` and positional task files. This invocation therefore exits with `unrecognized arguments: --premises-sha`, blocking every non-review TASK dispatch before sending anything. The tests replace the checker with permissive stubs, so they miss this incompatibility. Include the checker support or rebase onto the dependency before landing this caller change.

- [P2] Align the merge exemption with the regime CI verifier — scripts/orchestrator/dispatch.sh:230-231
  When an update-branch merge brings base changes outside the task's code entries, this gate permits retaining the old precheck. However, `scripts/orchestrator/regime-ci.py` still rejects any change between the tested commit and final head outside the task's evidence directory. Consequently, heads accepted here fail regime CI; this is reproducible on merge commit `15380731`. Update the verifier consistently, or require a fresh precheck until both consumers support this exemption.
The current checker rejects the new dispatch argument, and the update-branch exemption conflicts with regime CI. Shell syntax, ShellCheck, and shfmt passed; repository-writing tests were not run in the read-only environment.

Full review comments:

- [P1] Land checker support before sending --premises-sha — scripts/orchestrator/dispatch.sh:337-337
  Against the specified base, `task-consistency-check.py` accepts only `--root` and positional task files. This invocation therefore exits with `unrecognized arguments: --premises-sha`, blocking every non-review TASK dispatch before sending anything. The tests replace the checker with permissive stubs, so they miss this incompatibility. Include the checker support or rebase onto the dependency before landing this caller change.

- [P2] Align the merge exemption with the regime CI verifier — scripts/orchestrator/dispatch.sh:230-231
  When an update-branch merge brings base changes outside the task's code entries, this gate permits retaining the old precheck. However, `scripts/orchestrator/regime-ci.py` still rejects any change between the tested commit and final head outside the task's evidence directory. Consequently, heads accepted here fail regime CI; this is reproducible on merge commit `15380731`. Update the verifier consistently, or require a fresh precheck until both consumers support this exemption.
```
