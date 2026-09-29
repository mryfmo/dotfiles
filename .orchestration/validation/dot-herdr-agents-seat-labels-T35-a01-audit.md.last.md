- [P2] high `home/dot_local/bin/common/executable_herdr-agents:435` The suffix filter excludes supported solo Codex identities such as `codex-standard-dot`. After upstream self-naming, restart cannot find that worker and full-mode healing creates a duplicate. The parent correctly recognizes it.
- [P2] high `home/dot_local/bin/common/executable_herdr-agents:432` Sourcing the generated profiles in the caller’s shell overwrites explicit worker settings. Reproduced `express` becoming `standard` and `codex` becoming `claude`; bootstrap consequently skips Codex delivery hooks even though the cached worker kind still launches Codex.

Both regressions were reproduced using parent/commit functions with mocked inputs. Syntax and whitespace checks passed. Reported CI could not be independently verified because GitHub access failed; live-session verification remains pending.

📝 まとめ: Audited only `903c9fa`; found two regressions. No files changed.

Verdict: incorrect