---
task: dotfiles-T133-worker-write-boundary-a02
head: 79ea98a33f9bcb8da4f75142adcb458a2ba27a85
pr: 431
base: ba318e5369b14a79d6f515e87b685c9bcb30c12e
started: 2026-10-20T01:07:22Z
finished: 2026-10-20T01:15:34Z
findings: 4
engine: codex review --base main (profile review, read-only)
---

- [P1] Allow the manifest-generated advisor option for Claude workers — home/dot_local/bin/common/executable_herdr-agents:486-488
- [P1] Preserve the runtime dependencies of the attachment hook — home/dot_claude/modify_private_settings.json:243-245
- [P2] Migrate the legacy PreToolUse handler when adding the guard — home/.chezmoitemplates/claude-settings-managed.json:159-160
- [P2] Screen existing main-local hooks before replacing them — home/dot_claude-worker/modify_private_settings.json:391-394

```text
The patch breaks default Claude worker startup and Herdr attachment. Configuration updates can also delete custom hooks and retain duplicate legacy handlers. Targeted read-only reproductions confirmed these issues; the full test suite was not run.

Full review comments:

- [P1] Allow the manifest-generated advisor option for Claude workers — home/dot_local/bin/common/executable_herdr-agents:486-488
  The committed `standard` and `deep` Claude profiles generate `--advisor fable`, but this allowlist rejects that option and exits 2 before spawning. Since the manifest defaults to a Claude worker with the standard profile, ordinary `herdr-agents --add-worker` now fails. Admit the supported advisor pair while continuing to reject configuration-source overrides, consistent with the [canonical profile rule](/Users/a0004262/.codex/AGENTS.md#L46-L47).

- [P1] Preserve the runtime dependencies of the attachment hook — home/dot_claude/modify_private_settings.json:243-245
  Inside Herdr, the clean prefix removes `HERDR_AGENTS_LAYOUT`, bypassing the managed-pane shortcut, and restricts PATH to `/usr/bin:/bin`. The attachment payload then requires `herdr` by bare name, although this repository installs it through mise. Reproducing that environment returns 127 with `herdr command not found`, preventing orchestrator attachment and seat claiming. Preserve the necessary launch state and make the trusted Herdr executable reachable; this changes agent-hook behavior covered by [AGENTS.md:71](AGENTS.md#L71).

- [P2] Screen existing main-local hooks before replacing them — home/dot_claude-worker/modify_private_settings.json:391-394
  On a main checkout without an existing Claude worker, `bootstrap_agmsg` reaches this `--delivery` branch without preflight. Replacing the entire `hooks` object silently deletes existing non-delivery handlers, including local PermissionRequest and Stop safety checks. Migrate only recognized delivery hooks, or refuse unknown handlers before writing, rather than removing local policy during bootstrap ([AGENTS.md:71](AGENTS.md#L71)).

- [P2] Migrate the legacy PreToolUse handler when adding the guard — home/.chezmoitemplates/claude-settings-managed.json:159-160
  Existing user settings already contain `~/.claude/hooks/enforce-uv.sh`. Because `merge_hooks` has no PreToolUse ownership predicate, upgrading appends this guarded handler instead of replacing the legacy one. Both then execute for every Bash call, and the unguarded handler remains active even where the new guard suppresses execution. Add ownership-aware migration for the exact legacy and guarded forms, with an upgrade test ([AGENTS.md:71](AGENTS.md#L71)).
The patch breaks default Claude worker startup and Herdr attachment. Configuration updates can also delete custom hooks and retain duplicate legacy handlers. Targeted read-only reproductions confirmed these issues; the full test suite was not run.

Full review comments:

- [P1] Allow the manifest-generated advisor option for Claude workers — home/dot_local/bin/common/executable_herdr-agents:486-488
  The committed `standard` and `deep` Claude profiles generate `--advisor fable`, but this allowlist rejects that option and exits 2 before spawning. Since the manifest defaults to a Claude worker with the standard profile, ordinary `herdr-agents --add-worker` now fails. Admit the supported advisor pair while continuing to reject configuration-source overrides, consistent with the [canonical profile rule](/Users/a0004262/.codex/AGENTS.md#L46-L47).

- [P1] Preserve the runtime dependencies of the attachment hook — home/dot_claude/modify_private_settings.json:243-245
  Inside Herdr, the clean prefix removes `HERDR_AGENTS_LAYOUT`, bypassing the managed-pane shortcut, and restricts PATH to `/usr/bin:/bin`. The attachment payload then requires `herdr` by bare name, although this repository installs it through mise. Reproducing that environment returns 127 with `herdr command not found`, preventing orchestrator attachment and seat claiming. Preserve the necessary launch state and make the trusted Herdr executable reachable; this changes agent-hook behavior covered by [AGENTS.md:71](AGENTS.md#L71).

- [P2] Screen existing main-local hooks before replacing them — home/dot_claude-worker/modify_private_settings.json:391-394
  On a main checkout without an existing Claude worker, `bootstrap_agmsg` reaches this `--delivery` branch without preflight. Replacing the entire `hooks` object silently deletes existing non-delivery handlers, including local PermissionRequest and Stop safety checks. Migrate only recognized delivery hooks, or refuse unknown handlers before writing, rather than removing local policy during bootstrap ([AGENTS.md:71](AGENTS.md#L71)).

- [P2] Migrate the legacy PreToolUse handler when adding the guard — home/.chezmoitemplates/claude-settings-managed.json:159-160
  Existing user settings already contain `~/.claude/hooks/enforce-uv.sh`. Because `merge_hooks` has no PreToolUse ownership predicate, upgrading appends this guarded handler instead of replacing the legacy one. Both then execute for every Bash call, and the unguarded handler remains active even where the new guard suppresses execution. Add ownership-aware migration for the exact legacy and guarded forms, with an upgrade test ([AGENTS.md:71](AGENTS.md#L71)).
```
