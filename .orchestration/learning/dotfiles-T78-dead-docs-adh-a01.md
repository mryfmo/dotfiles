# dotfiles-T78-dead-docs-adh-a01 — learning triage

1. **Deleting a directory leaves its exclusions behind in more than one tool config.** `reviews/` was excluded in both `.coderabbit.yaml` and `.prettierignore`, but only the first was named in the task. Grep every ignore and filter file (`.coderabbit.yaml`, `.prettierignore`, `.gitignore`, workflow `paths`) for the directory before declaring it gone.
2. **Deleting one line of a section can orphan the rest.** The Codex AGENTS.md learn section's other bullets referred back to the index line. Removing the section as a unit, confirmed by PONG, kept the file coherent.
3. **A pointer from a deployed command should use the deployed path.** `/commit` runs in any repository, so its pointer names `~/.agents/skills/...`, while repo-local docs (`plans/README.md`) use the source path.
