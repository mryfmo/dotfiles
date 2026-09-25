# dot-ubuntu-parity-T5-a01 — learning triage

## Reusable rule candidate

chezmoi runs `.chezmoiscripts` entries in target-name lexical order,
interleaved with target-state file application — NOT after all files are
applied. A `run_once_*`/`run_onchange_*` script that depends on a file
chezmoi itself manages (systemd units, config files, etc. under
`home/dot_config/**` or similar) must use the `_after_` variant
(`run_once_after_*`, `run_onchange_after_*`) so chezmoi defers it until
target-state application finishes. This repo already had one example
(`run_once_after_04-install-aws-cli.sh.tmpl`) before this task; T4's
`run_onchange_60-enable-usage-snapshot-timer.sh.tmpl` missed this and only
worked on machines where the unit files already existed from a prior apply,
which is why it passed on already-provisioned hosts but failed CI's fresh
bootstrap. Recorded as a CompactionDB `[memory:decision]` (id
`ebab46ec-b613-400d-91ac-2b2a0de8ee88`) — worth promoting to a written rule
if more `.chezmoiscripts` entries get added that reference chezmoi-managed
target files.

## Process note

Before branching per the task's instruction to work from `origin/main`
instead of this worktree's registered `feat/ubuntu-parity`, independently
verified (rather than trusting the task text alone) that `origin/main`
really did contain all of T2-T4's work — same commit subjects, different
hashes, confirming a rebase/re-apply. This is worth keeping as a standing
practice for any future task that asks a worker to change its registered
worktree's branch away from what it was assigned: verify the stated
precondition (e.g. "already merged") against the actual remote ref before
acting, rather than proceeding on the instruction's say-so alone — especially
since it otherwise contradicts every prior task's explicit "never checkout
away from feat/ubuntu-parity" environment note.

Not promoting either item to `skills/candidates/` — no reusable
Claude/Codex-facing skill workflow implied, just a project-specific chezmoi
convention and a general verification habit already covered by the worker
playbook's "read task_file first" pitfall.
