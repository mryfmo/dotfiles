# dot-mkt-owner-T1-a01 learning triage

## Candidate reusable rule

[memory:failure] A chezmoi `create_` source ensures a file exists but can still participate in mode/state handling. For a true one-time seed whose contents and mode become runtime-owned, conditionally ignore the target once it exists.

[memory:failure] Do not call `chezmoi state delete` from a `run_once_before` script during apply; the child command waits on the persistent-state lock held by its parent apply.

## Disposition

- Recorded as validated Codex worklog learning in `.agents/worklog/codex/learn/20260921_191640_learn.md` and indexed in `learn_index.md`.
- Not promoted to a repository skill; the rule is narrow and the worklog entry is sufficient.
