---
task: dotfiles-T133-ci-efficiency-followup-a01
head: 76ab18e8c7b64fdaac126453072d5230fe1f9c56
pr: 421
base: 86ea98848b595f53e0afcf8f298ebda311a51dcf
started: 2026-10-19T02:29:06Z
finished: 2026-10-19T02:31:07Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Replace the invalid workflow-input residual control — .orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md:38-39

```text
Read-only structural checks and path-predicate probes passed, but the required threat table contains an invalid compensating control. Full fixture-based tests were not rerun because the sandbox is read-only.

Review comment:

- [P2] Replace the invalid workflow-input residual control — .orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md:38-39
  This PR changes three workflows, including required-check skip decisions, but this residual control assumes no workflow file is allowed to change. That premise contradicts both `allowed_files` and the diff, while the statement about `ci-rerun.sh` does not mitigate risks in the modified workflow inputs. Replace it with an applicable compensating control, as required by [AGENTS.md:78](AGENTS.md#L78).
Read-only structural checks and path-predicate probes passed, but the required threat table contains an invalid compensating control. Full fixture-based tests were not rerun because the sandbox is read-only.

Review comment:

- [P2] Replace the invalid workflow-input residual control — .orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md:38-39
  This PR changes three workflows, including required-check skip decisions, but this residual control assumes no workflow file is allowed to change. That premise contradicts both `allowed_files` and the diff, while the statement about `ci-rerun.sh` does not mitigate risks in the modified workflow inputs. Replace it with an applicable compensating control, as required by [AGENTS.md:78](AGENTS.md#L78).
```
