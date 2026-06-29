## Model selection and ccgate

- Use the smallest Claude Code model that is adequate for the task. Do not keep using Opus or other premium models for a stream of simple reads, searches, formatting, or straightforward local edits.
- ccgate is a PermissionRequest gate, not a model router. Its `provider.model` is the small classifier used for permission decisions, not the active Claude Code task model.
- Claude Code PermissionRequest payloads do not expose the active model to ccgate. Enforce model choice through settings and agent rules; use ccgate for tool-action safety and feedback.
- If ccgate denies an operation because the requested action is broad, destructive, privileged, network-executing, or too wide for a single permission unit, narrow the operation or switch to a more appropriate model before retrying.
- Inspect `ccgate claude metrics --details 5` periodically and tune rules from real fallthrough and deny patterns instead of adding broad stop-only rules.
