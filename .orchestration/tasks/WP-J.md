# WP-J: Make the real ghostty config chezmoi-managed

task_id: WP-J
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpj

## Problem (measured)

chezmoi deploys `home/dot_config/ghostty/config.ghostty` → `~/.config/ghostty/config.ghostty`, but ghostty only reads `~/.config/ghostty/config`, which is a hand-written file (2026-02-22) NOT managed by chezmoi. Result: dotfiles edits to ghostty config never take effect, and the working config is unmanaged (can be lost). A backup `config.bak.20260202-075601` also sits in that dir.

## Changes

1. CREATE `home/dot_config/ghostty/config` in the source with the CURRENT live `~/.config/ghostty/config` content as the base (read it; it includes font, macos-option-as-alt, secure-input settings, OSC52 clipboard rules, ctrl+shift+c/v keybinds, ssh shell-integration features — user-authored comments in Japanese must be preserved verbatim).
2. Merge in the still-useful entries that exist only in the old managed `config.ghostty` and do not conflict with the live baseline: `window-padding-x = 8`, `window-padding-y = 4`, `confirm-close-surface = true`, `shell-integration = detect`. For `shell-integration-features`, the live line wins (do not overwrite it). Add merged lines under a clearly commented section.
3. DELETE `home/dot_config/ghostty/config.ghostty` from the source.
4. Grep repo for `config.ghostty` (tests/, scripts/, chezmoiignore templates, docs, README) and fix references; report what you find.

Do NOT delete or touch the live files in $HOME (no chezmoi apply). Managed-state changes only.

## Allowed files (edit boundary)

home/dot_config/ghostty/\*\*, plus any reference-fix files found by the grep in step 4 that are not owned by WP-I/WP-K (report cross-owned findings instead of editing), plus your artifact paths.

## Forbidden actions

git commit; git push; chezmoi apply; running bats; dependency changes; editing $HOME files.

## Validation

1. `chezmoi diff ~/.config/ghostty/config` → shows only the merged additions relative to live (padding/confirm-close/shell-integration lines), nothing removed from the live baseline
2. grep for config.ghostty → zero unfixed references
3. `git status --porcelain` → only expected changes

## Expected artifacts

- report: .orchestration/reports/WP-J.md
- validation: .orchestration/validation/WP-J.txt
- sandbox: .orchestration/sandboxes/WP-J.md
- learning: .orchestration/learning/WP-J.md
- autoskill: .orchestration/autoskill/runs/WP-J.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpj orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-J status=ready_for_review report=.orchestration/reports/WP-J.md validation=.orchestration/validation/WP-J.txt sandbox=.orchestration/sandboxes/WP-J.md learning=.orchestration/learning/WP-J.md autoskill=.orchestration/autoskill/runs/WP-J.md"
```

max_turns: 25
