[P2] High confidence scripts/agent-stop-gate.sh:153 — Without `timeout`, a slow history read runs past the configured five-second Stop hook limit. Claude then cancels the hook without a blocking decision, allowing the seat to stop with pending work. Checking the deadline between teams cannot interrupt the stalled read. Preserve a portable hard timeout. [Hook timeout semantics](https://code.claude.com/docs/en/hooks#timeouts).

The committed loop reproduced this: a six-second read emitted no blocking output before five seconds; a fast read correctly exited 2. [CI passed](https://github.com/mryfmo/dotfiles/actions/runs/37170566965), but the changed decorator skips the slow-store test when `timeout` is absent, leaving this regression uncovered.

📝 まとめ: Audited only `cb3ded43`; found one timeout regression. No files changed.

Verdict: incorrect