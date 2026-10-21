---
task: dotfiles-T133-worker-write-boundary-a02
head: c0f50fa1383416240ad28959dbc4635afa777175
pr: 431
base: 118daafa4610549d3bc280800cf8b1d36fb851dc
started: 2026-10-20T03:08:09Z
finished: 2026-10-20T03:17:57Z
findings: 4
engine: codex review --base main (profile review, read-only)
---

- [P1] Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243
- [P1] Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206
- [P2] Include parent-directory creation in the installation command — Makefile:213-213
- [P2] Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633

```text
The startup boundary accepts sandbox-widening project settings and misses managed skill inputs. The patch also introduces update and installation regressions; validation was limited to read-only probes and static checks.

Full review comments:

- [P1] Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206
  A worktree settings file containing `sandbox.excludedCommands: ["*"]` or `sandbox.filesystem.allowWrite: ["/"]` passes the complete preflight and remains unchanged. Claude merges these array settings across scopes, so generating empty worker exclusions does not remove the escape or broad write grant, even with the administrative policy installed. Reject noncanonical sandbox extensions before launching; the claimed restricted-write control does not mitigate this input ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243
  Enterprise skills reside under `<managed-root>/skills`, not `<managed-root>/.claude/skills`. Consequently, an existing `/etc/claude-code/skills/p/SKILL.md` or macOS equivalent—and its bundled plugin hooks—is never screened or added to the discovered plugin disables. Use `managed` as the loading root and test the real paths; the current fixtures repeat the incorrect directory, leaving the S12/S20 controls ineffective ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633
  During `make update`, `scripts/update-agent-assets.sh` still runs `herdr integration install claude` after chezmoi applies this guarded command. Herdr recognizes its own literal hook command, so replacing it here causes the installer to append the original unguarded SessionStart hook again. There is no subsequent Claude-settings reconciliation, leaving duplicate execution and managed-settings drift reported by `make doctor`. Update the installation sequence to preserve the guarded entry.

- [P2] Include parent-directory creation in the installation command — Makefile:213-213
  On a fresh CLI installation, `/etc/claude-code` or `/Library/Application Support/ClaudeCode` may not exist. The printed `sudo install -m 0644 ...` command does not create parent directories, so following it fails and leaves the administrative policy undeployed. Print a privileged directory-creation command before the file installation while keeping this target itself nonprivileged.
The startup boundary accepts sandbox-widening project settings and misses managed skill inputs. The patch also introduces update and installation regressions; validation was limited to read-only probes and static checks.

Full review comments:

- [P1] Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206
  A worktree settings file containing `sandbox.excludedCommands: ["*"]` or `sandbox.filesystem.allowWrite: ["/"]` passes the complete preflight and remains unchanged. Claude merges these array settings across scopes, so generating empty worker exclusions does not remove the escape or broad write grant, even with the administrative policy installed. Reject noncanonical sandbox extensions before launching; the claimed restricted-write control does not mitigate this input ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243
  Enterprise skills reside under `<managed-root>/skills`, not `<managed-root>/.claude/skills`. Consequently, an existing `/etc/claude-code/skills/p/SKILL.md` or macOS equivalent—and its bundled plugin hooks—is never screened or added to the discovered plugin disables. Use `managed` as the loading root and test the real paths; the current fixtures repeat the incorrect directory, leaving the S12/S20 controls ineffective ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633
  During `make update`, `scripts/update-agent-assets.sh` still runs `herdr integration install claude` after chezmoi applies this guarded command. Herdr recognizes its own literal hook command, so replacing it here causes the installer to append the original unguarded SessionStart hook again. There is no subsequent Claude-settings reconciliation, leaving duplicate execution and managed-settings drift reported by `make doctor`. Update the installation sequence to preserve the guarded entry.

- [P2] Include parent-directory creation in the installation command — Makefile:213-213
  On a fresh CLI installation, `/etc/claude-code` or `/Library/Application Support/ClaudeCode` may not exist. The printed `sudo install -m 0644 ...` command does not create parent directories, so following it fails and leaves the administrative policy undeployed. Print a privileged directory-creation command before the file installation while keeping this target itself nonprivileged.
```
