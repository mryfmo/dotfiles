# Learning triage

Date: 2026-10-06
Validated: worker_github_config_dir resolves the manifest path and expands a leading ~/ without reading credentials. Tests with an empty hosts.yml at a customized path with spaces verify silent continuation. Missing-file tests pin exact stderr notice and unchanged stdout/status in all three requested modes.

Plan updates: retain existing file-presence/operator-provisioning boundary; do not infer authentication success from an existing file. No rule promotion. CompactionDB task decision is recorded by orchestrator (Codex seat).
