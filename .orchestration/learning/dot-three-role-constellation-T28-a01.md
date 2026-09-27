# T28 learning triage

## Candidate

codex-cli 0.157.1 silently ignores an unknown `--profile <name>` (no error;
base config applies), so "the flag was accepted" proves nothing. Verify a
profile layer by probing with an existing profile and reading the session
header (`model:`, `sandbox:`, `reasoning effort:`) under a short `timeout`,
e.g. `timeout 8 codex --profile security review --commit HEAD </dev/null`.
The global `--profile` flag must precede the subcommand
(`codex --profile audit review --commit <sha>`); `codex review --help` has no
`--profile`.

## Disposition

Candidate only. Do not promote automatically. Relevant to the orchestrator's
first live `codex --profile audit review` after apply: confirm the header shows
`model: gpt-6-astra`, `sandbox: read-only`, `reasoning effort: high`.
