# WP-B: Remove tmux config deployment

task_id: WP-B
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpb

## Objective

Stop deploying all tmux configuration from this chezmoi-managed dotfiles repo and remove tmux-only deployed helpers. Installation-script removal is WP-A (do NOT touch install/, .chezmoiscripts/, nix/).

## Changes (exhaustive — do all, nothing else)

DELETE:

- home/dot_tmux.conf.tmpl
- home/dot_tmux.conf.d/ (entire directory)
- home/dot_tmux-powerlinerc
- home/dot_local/bin/common/executable_codex-statusline-tmux (tmux status bar helper, useless without tmux)

EDIT — remove now-stale tmux ignore entries from chezmoiignore templates:

- home/.chezmoitemplates/chezmoiignore.d/common (line ~5: `.tmux.conf.d/`)
- home/.chezmoitemplates/chezmoiignore.d/macos (lines ~3-4: tmux entries)
- home/.chezmoitemplates/chezmoiignore.d/ubuntu/server (lines ~9-11: tmux entries incl. `.tmux-powerlinerc`)
- home/.chezmoitemplates/chezmoiignore.d/ubuntu/client (line ~1: tmux entry)
  Remove ONLY tmux-related lines; keep all other ignore entries byte-identical.

EDIT — remove tmux deployment assertions from file-presence tests (keep files and all non-tmux assertions):

- tests/files/common.bats
- tests/files/macos.bats
- tests/files/ubuntu.bats

EDIT:

- home/dot_bash/client/bashrc (line ~129): remove the tmux history-sharing comment. If the comment documents an adjacent tmux-specific code block, remove that block too, but only if it is exclusively tmux-conditional; otherwise remove just the comment. Do not change non-tmux behavior.

Note: home/dot_local/bin/common/executable_dev uses tmux only behind `[[ -n ${TMUX} ]]` — leave it untouched.

## Allowed files (edit boundary)

Only the files listed above, plus your artifact paths below.

## Forbidden actions

git commit; git push; chezmoi apply; running bats; adding dependencies; editing install/, .chezmoiscripts/, nix/, scripts/, Makefile, README (other tasks own those).

## Validation (run and capture output)

1. deleted paths gone
2. `grep -rn "tmux" home/.chezmoitemplates/ tests/files/ home/dot_bash/ || true` → no tmux hits left (report any with justification)
3. `git status --porcelain` → only expected changes
4. If shell files were edited: `shfmt --indent 4 --space-redirects --diff <edited .sh/bashrc files> || true` and report

## Expected artifacts (write to these exact paths)

- report: .orchestration/reports/WP-B.md
- validation: .orchestration/validation/WP-B.txt
- sandbox: .orchestration/sandboxes/WP-B.md (record: codex exec --sandbox workspace-write fallback)
- learning: .orchestration/learning/WP-B.md ("none" if nothing)
- autoskill: .orchestration/autoskill/runs/WP-B.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpb orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-B status=ready_for_review report=.orchestration/reports/WP-B.md validation=.orchestration/validation/WP-B.txt sandbox=.orchestration/sandboxes/WP-B.md learning=.orchestration/learning/WP-B.md autoskill=.orchestration/autoskill/runs/WP-B.md"
```

If blocked: same message with status=blocked, artifacts explaining why.

max_turns: 30
