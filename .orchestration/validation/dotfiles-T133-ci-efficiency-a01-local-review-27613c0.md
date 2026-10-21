---
task: dotfiles-T133-ci-efficiency-a01
head: 27613c0c1ea978de1f0250a4a254de07fa543e98
pr: 409
base: 99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
started: 2026-10-18T06:26:14Z
finished: 2026-10-18T06:30:58Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P2] Reject superseded PR heads before rerunning CI — scripts/orchestrator/ci-rerun.sh:69-70
- [P2] Test the production flake registry before marking it closed — .orchestration/dotfiles-T133-ci-efficiency-a01/task.md:27-28
- [P2] Validate timed-out jobs before requesting a failed-job rerun — scripts/orchestrator/ci-rerun.sh:71-71

```text
The rerun helper can cancel newer PR checks and retry unclassified failures. The production flake registry also lacks the coverage claimed by its threat-table disposition.

Full review comments:

- [P2] Reject superseded PR heads before rerunning CI — scripts/orchestrator/ci-rerun.sh:69-70
  If a known-flake run for PR head A is retried after head B starts, this code accepts A without checking whether it is still current. Both runs share the new PR concurrency group, so rerunning A can cancel B's required checks through `cancel-in-progress: true`. Reject superseded PR heads before reserving or rerunning them.

- [P2] Validate timed-out jobs before requesting a failed-job rerun — scripts/orchestrator/ci-rerun.sh:71-71
  For a run containing a matching flake and an unrelated `timed_out` job, this filter validates only the flake. However, `gh run rerun --failed` also restarts timed-out jobs, so the unrelated timeout is retried without a signature match or ledger entry. Account for every failed conclusion the endpoint will restart and refuse runs containing unclassified failures.

- [P2] Test the production flake registry before marking it closed — .orchestration/dotfiles-T133-ci-efficiency-a01/task.md:27-28
  The cited test replaces `.github/flakes.yaml` with its own `FLAKES` fixture and never reads the checked-in registry. It therefore passes even if the production regex becomes invalid or matches arbitrary failures, so it does not close this row as required by [AGENTS.md:78](AGENTS.md#L78). Add coverage using the production registry and recorded log, or declare an accurate residual control.
The rerun helper can cancel newer PR checks and retry unclassified failures. The production flake registry also lacks the coverage claimed by its threat-table disposition.

Full review comments:

- [P2] Reject superseded PR heads before rerunning CI — scripts/orchestrator/ci-rerun.sh:69-70
  If a known-flake run for PR head A is retried after head B starts, this code accepts A without checking whether it is still current. Both runs share the new PR concurrency group, so rerunning A can cancel B's required checks through `cancel-in-progress: true`. Reject superseded PR heads before reserving or rerunning them.

- [P2] Validate timed-out jobs before requesting a failed-job rerun — scripts/orchestrator/ci-rerun.sh:71-71
  For a run containing a matching flake and an unrelated `timed_out` job, this filter validates only the flake. However, `gh run rerun --failed` also restarts timed-out jobs, so the unrelated timeout is retried without a signature match or ledger entry. Account for every failed conclusion the endpoint will restart and refuse runs containing unclassified failures.

- [P2] Test the production flake registry before marking it closed — .orchestration/dotfiles-T133-ci-efficiency-a01/task.md:27-28
  The cited test replaces `.github/flakes.yaml` with its own `FLAKES` fixture and never reads the checked-in registry. It therefore passes even if the production regex becomes invalid or matches arbitrary failures, so it does not close this row as required by [AGENTS.md:78](AGENTS.md#L78). Add coverage using the production registry and recorded log, or declare an accurate residual control.
```
