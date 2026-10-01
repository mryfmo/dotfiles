[P1] high confidence home/dot_local/bin/common/executable_herdr-agents:470 Parallel `--resume`/`--continue` processes can share a session ID, so this condition releases another live process’s lock, takes its identity, and interrupts its inbox delivery. Require proof that the previous owner is stale; matching the session ID is insufficient.

A read-only comparison confirmed the parent rejects releasing a live owner while this commit permits it. Shell syntax and diff checks passed. CI was unreachable; available validation evidence covers an earlier commit.

📝 まとめ: Audited only `63d4e03`; found one lock-exclusivity regression. No files changed.

Verdict: incorrect