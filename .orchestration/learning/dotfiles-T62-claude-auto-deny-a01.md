# dotfiles-T62-claude-auto-deny-a01 — learning

Validated: Claude Code ignores `permissions.defaultMode: auto` in project and local settings; it must be in user or managed settings. A matching explicit ask rule still prompts in auto mode, so publish rules should be deny rules when prompting is not the desired policy.

Applied to: user-level Claude settings policy tasks.
