[P2] high home/dot_local/bin/common/executable_herdr-agents:1355 Unconditionally forcing Codex despawn prevents cleanup after a failed spawn: upstream registers the identity before creating its placement record, but forced despawn fails when that record is absent. Removal then exits before disabling delivery, leaving the team, or closing the workspace; retrying with `--force` also fails. Preserve graceful cleanup for an absent placement record.

Reproduced using upstream’s despawn dispatch: an absent record returns success normally and failure with force. Bash syntax and ShellCheck passed. GitHub connectivity failed, so the reported CI results remain independently unverified; live testing is explicitly deferred in the report.

📝 まとめ: Audited only `e226c27` without modifying files; found one cleanup regression requiring correction.
Verdict: incorrect