# Learning: dotfiles-T80-codex-command-hooks-a01

- **Verify against the machine-readable reference the repository already names.** The rendered template's `#:schema` URL carries the authoritative `HooksToml` event list. It differed from the task's list in both directions: `Notification` is absent, and `Interrupt` and `SubagentStart` are present.
- **`x or []` swallows malformed values.** Default only a missing key, so a falsey non-list is reported, not ignored (Codex P2).
- **An equality check of parsed tables subsumes a count check,** and also catches edited fields.
- **Event-specific limits live in the prose reference, not the schema.** The schema's `timeout` is a plain uint64, while the hooks page caps SessionEnd and Interrupt at 3 seconds. Check both sources.
