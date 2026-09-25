# dot-mkt-mode-T1-a01 learning triage

## Promoted to worker learn

- Lima host mounts can present a host 0644 file as 0664 inside Ubuntu. Mode-sensitive validation must copy the relevant source into the VM-local filesystem and normalize its source mode before drawing conclusions.
- Chezmoi's created-file mode follows the invoking umask. A two-writer mode test must set each writer's observed umask independently rather than applying one global umask to the whole harness.

These facts were validated across failed reproductions and the final passing two-cycle proof. They are recorded in `.agents/worklog/codex/learn/20260921_171545_learn.md`.
