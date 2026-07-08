# WP-H: Fix CI bats failure in lifecycle.bats (deleted-script grep)

task_id: WP-H
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wph

## Objective

PR #61 CI failed: `tests/install/common/lifecycle.bats` test 21
"[common] Homebrew upgrade filters forbidden formulae without installed-dependent side effects"
greps `scripts/update-codex-statusline-tools.sh`, which was deleted in WP-F.

CI log evidence: `grep -q 'brew list --cask codexbar' scripts/update-codex-statusline-tools.sh` failed with status 2 (No such file or directory).

## Changes (exhaustive — do all, nothing else)

EDIT tests/install/common/lifecycle.bats:

- In test 21, remove ONLY the five grep lines targeting `scripts/update-codex-statusline-tools.sh` (lines ~106-110, all mentioning codexbar). KEEP the five preceding grep assertions against `scripts/upgrade-tools.sh` (lines ~101-105) — that logic still exists.
- Then scan the WHOLE file for any other reference to files deleted in this PR (update-codex-statusline-tools.sh, tmux/tpm/hermes install scripts, dot_tmux\*, private_dot_hermes, hermes-config-base.yaml, hermes-agent-orchestration) and remove such assertions if found. Report what you find.

## Allowed files (edit boundary)

Only tests/install/common/lifecycle.bats, plus your artifact paths.

## Forbidden actions

git commit; git push; chezmoi apply; running bats locally (CI-only policy); dependency changes; editing any other file.

## Validation (run and capture output)

1. `grep -n "update-codex-statusline-tools\|codexbar" tests/install/common/lifecycle.bats || true` → zero hits
2. `bash -n` is not applicable to bats; instead show `sed -n '95,115p' tests/install/common/lifecycle.bats` to evidence the surgical edit
3. `git diff --stat tests/install/common/lifecycle.bats` → only this file

## Expected artifacts (write to these exact paths)

- report: .orchestration/reports/WP-H.md
- validation: .orchestration/validation/WP-H.txt
- sandbox: .orchestration/sandboxes/WP-H.md (record: codex workspace-write fallback)
- learning: .orchestration/learning/WP-H.md (note the cross-WP ownership gap that caused this)
- autoskill: .orchestration/autoskill/runs/WP-H.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wph orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-H status=ready_for_review report=.orchestration/reports/WP-H.md validation=.orchestration/validation/WP-H.txt sandbox=.orchestration/sandboxes/WP-H.md learning=.orchestration/learning/WP-H.md autoskill=.orchestration/autoskill/runs/WP-H.md"
```

max_turns: 20
