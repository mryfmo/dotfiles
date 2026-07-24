# T13 learning triage

## Validated observations

- Global Claude rule files in this repository use one `##` heading and direct bullets; a separate preamble or nested section structure is unnecessary.
- The resident-worker regime and identity rules fit in one 14-line rule without omitting operational constraints.
- Branch creation after writing an untracked file preserves the requested unstaged state while ensuring the branch starts at `main`.
- Files under `home/dot_config/claude/rules/` require matching `home/dot_claude/rules/symlink_*.md.tmpl` wiring to load through `~/.claude/rules`.
- `.chezmoi.sourceDir` already points at the public source-state `home/` directory, so symlink templates must start with `/dot_config/...`, not `/home/dot_config/...`.

## Promotion decision

No separate project learn entry is needed. The reusable policy is already captured in the new global rule file and should be judged during orchestrator acceptance.
