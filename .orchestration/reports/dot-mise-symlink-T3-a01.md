# dot-mise-symlink-T3-a01
status: ready_for_review
cost: n/a

Branch: fix/mise-config-not-live-symlink; worktree: .claude/worktrees/mise-symlink, created from origin/main without rebasing onto PR170/PR171.

## Changes
- Replaced the two mise symlink templates with regular-file include templates. Both render byte-identical to the unchanged home/dot_mise source pair.
- upgrade-tools.sh sets MISE_CONFIG_DIR to the executing script's checkout home/dot_mise unless explicitly overridden, and exports MISE_CEILING_PATHS at the checkout boundary for all lifecycle subprocesses. The existing isolated-XDG wrapper retains the scoped config directory.
- Added the requested zsh comment and README/script documentation. Updated lifecycle grep checks.
- Added a fake-mise full upgrade fixture with legacy live symlinks, covering default and explicit config-dir override. Added real chezmoi rendering and temporary-destination migration coverage proving subsequent runtime-file writes cannot mutate source.

## Validation
393 unit tests pass. The final full suite includes the migration test; a duplicate shadowed definition caused by an interrupted tool retry was removed afterward and the unchanged migration test plus diff check rerun successfully.
Before the production fix, spill assertions and managed-file assertion failed. After the fix, a macOS /var versus /private/var test-path mismatch was corrected using resolve(); both spill cases pass.
ShellCheck, shfmt -i 4 -sr, asset validator, diff check, and Crit evidence gate pass. Native mise config ls lists only the checkout's source config (sandbox denied optional cache/tracking writes but config discovery completed successfully). Both direct chezmoi execute-template | cmp checks pass. Temporary chezmoi apply replaces existing symlinks with regular files; writing applied copies leaves fixture source unchanged.
The source pin pair has no diff. No local Bats, real operator-home apply, make update, commit, push, or PR mutation. The new regular templates are untracked and must be included in integration.

## Why the ceiling is necessary
MISE_CONFIG_DIR alone was insufficient in T2: ancestor discovery could still load ~/.config/mise/config.toml. A read-only native probe showed that setting MISE_CEILING_PATHS to this checkout excludes that ancestor while retaining the selected global config. Exporting both at script scope also covers bare mise exec/where/trust calls, not only the isolated wrapper. The explicit MISE_CONFIG_DIR override remains supported and tested.
References: [mise configuration](https://mise.jdx.dev/configuration.html), [mise settings](https://mise.jdx.dev/configuration/settings.html).

## Durable fact
[memory:decision] ~/.config/mise is an applied copy of home/dot_mise; make upgrade mutates its own checkout's pins (or the explicit config-dir override), without discovering parent live configs.
Executed in canonical main:
```sh
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "The mise config and lock under ~/.config/mise are applied regular-file copies of home/dot_mise. make upgrade scopes mise configuration and ancestor discovery to its own checkout, preserving an explicit MISE_CONFIG_DIR override; native config discovery and temporary-home spill/render/apply fixtures validate source isolation."
```
Memory ID: df6ec653-428f-4459-93fb-18d1c611af8d.

## Integration and limits
Orchestrator owns adversarial acceptance and commit/CI. Runtime symlinks on the operator machine remain unchanged until an authorized later chezmoi apply; no live migration was performed here. The two removed symlink templates remain recoverable from Git history and are replaced by regular templates, not deleted configuration data.
Review receipt: .claude/worktrees/mise-symlink/.agents/worklog/codex/dot-mise-symlink-T3-a01-review.md.

## PR172 revision (2026-09-25)
status: ready_for_review
cost: n/a

Addressed both bot findings in the existing mise-symlink worktree without commit/push. Converted the zsh @description into an ordinary inline comment. Successful upgrade now compares the invoking checkout physically with the git toplevel of chezmoi source-path; only equality applies the two HOME/.config/mise/config.toml and mise.lock targets. Other checkouts print the specified merge/make-update notice. Prior required failures skip apply; apply failure propagates as a required failure.

Four fake-chezmoi scenarios were red-first: canonical success, different source checkout, prior upgrade failure and apply failure. Full suite: 394 passed. Shellcheck -x, shfmt, validator, diff and Crit receipt gate passed. No real HOME apply, local Bats, pin edits, commit or push.
Review evidence: .claude/worktrees/mise-symlink/.agents/worklog/codex/t3-revise-crit.json (receipt alongside).

[memory:decision] Canonical successful upgrade refreshes only the two applied mise files; worktree changes wait for merge and make update.
Memory command (canonical repo): `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'PR172 revision: after successful make upgrade, apply only ~/.config/mise/config.toml and mise.lock when the invoking checkout physically equals the git toplevel of chezmoi source-path. Other worktrees defer applied-copy refresh until merge and make update; required upgrade failures skip apply and apply failure makes upgrade fail.'`
Memory ID: 9f3a9912-50db-4674-8bd5-25b3c828148d.
