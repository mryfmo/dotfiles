---
task: dotfiles-T133-hold-playbook-a01
head: 9f5eaeec4479f9782b80bd247f5d993db1533803
pr: 426
base: 3f240b129724e7b6e677df42c5cb095ebc0dafcd
started: 2026-10-19T07:22:12Z
finished: 2026-10-19T07:25:53Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P1] Land the class vocabulary before requiring it — scripts/orchestrator/hold-playbook.sh:129-129

```text
The helper's required vocabulary is not shipped, leaving its primary operation unusable from a clean checkout. Shell checks and direct coverage checks passed; filesystem-writing tests were not rerun in the read-only sandbox.

Review comment:

- [P1] Land the class vocabulary before requiring it — scripts/orchestrator/hold-playbook.sh:129-129
  On a clean checkout, `.orchestration/learning/classes.yaml` is absent from both this head and the base, so every valid invocation immediately exits 2 with `FileNotFoundError` instead of producing a replan. The recorded smoke check relies on an untracked file in another checkout, while the tests supply their own fixtures. Land the orchestrator-owned vocabulary as a tracked prerequisite so the shipped command can run.
The helper's required vocabulary is not shipped, leaving its primary operation unusable from a clean checkout. Shell checks and direct coverage checks passed; filesystem-writing tests were not rerun in the read-only sandbox.

Review comment:

- [P1] Land the class vocabulary before requiring it — scripts/orchestrator/hold-playbook.sh:129-129
  On a clean checkout, `.orchestration/learning/classes.yaml` is absent from both this head and the base, so every valid invocation immediately exits 2 with `FileNotFoundError` instead of producing a replan. The recorded smoke check relies on an untracked file in another checkout, while the tests supply their own fixtures. Land the orchestrator-owned vocabulary as a tracked prerequisite so the shipped command can run.
```
