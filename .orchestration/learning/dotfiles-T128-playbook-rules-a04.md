# Learning triage: dotfiles-T128-playbook-rules-a04

These are candidates only; nothing is promoted. The candidates of a01 to a03 stand.

1. [memory:failure] `history.sh <team> --limit N` reads the whole history whatever N is. `--limit` lands in the agent slot, `storage_history` skips a dash-led agent, and the second `--limit` becomes a non-numeric limit, which means none. The positional `history.sh <team> '' N` is the documented form. A rule that prescribes a CLI form should name the documented one, verified by running it, not the one that happens to work.
2. [memory:decision] Splice long quoted rule sentences into the target file from the task file's own quoted spans (a scratch script that parses them), rather than retyping them. It removes transcription as a source of verbatim drift.
