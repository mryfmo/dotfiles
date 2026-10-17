# Learning triage: dotfiles-T130-claude-sandbox-integration-followup-a01

These are candidates only; nothing is promoted.

1. [memory:decision] Security documentation of a rendered setting is written from the rendering (the template, one block per OS), with a pasted check that every value the prose names is in the rendering and every rendered value is in the prose; the live machine's settings are not a source (the operator's `make update` may lag the merge, as it did here).
2. [memory:decision] A sentence about Claude Code's own behaviour (how `excludedCommands` matches, what `allowUnsandboxedCommands` does, how a host outside `allowedDomains` is handled under `auto`) carries an upstream quote in the validation file with the page and heading; the previous text's "matches the first word" and "other hosts prompt" were paraphrases that had drifted from the page.
3. [memory:failure] A value check written in a hurry matched `Bash(gh pr merge:*)` with `pr \S+` and captured the trailing `:*)`, so the check failed on correct prose; the regex now matches the subcommand letters only. A check that gates a commit is itself read once before it is trusted.
