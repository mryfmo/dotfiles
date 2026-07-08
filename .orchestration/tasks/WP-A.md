# WP-A: Remove tmux installation path

task_id: WP-A
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpa

## Objective

Completely remove the tmux/TPM installation path from this chezmoi-managed dotfiles repo. tmux is being removed from the repo entirely (config removal is handled by another task; do NOT touch config files).

## Changes (exhaustive — do all, nothing else)

DELETE these files:

- install/macos/common/tmux.sh
- install/ubuntu/common/tmux.sh
- install/common/tpm.sh
- home/.chezmoiscripts/macos/run_once_08-install-tmux.sh.tmpl
- home/.chezmoiscripts/ubuntu/run_once_08-install-tmux.sh.tmpl
- tests/install/macos/common/tmux.bats
- tests/install/ubuntu/common/tmux.bats
- tests/install/ubuntu/common/tmux_unit.bats
- tests/install/common/tpm.bats
- tests/install/ubuntu/common/tpm.bats

EDIT:

- nix/shared/packages.nix: remove the `tmux` entry (around line 24). Keep everything else intact.

Check: if any bats helper/loader under tests/ enumerates the deleted files by name (e.g. a suite list), update it. Do not touch other tests.

## Allowed files (edit boundary)

Only the files listed above, plus your artifact paths below. Nothing else.

## Forbidden actions

git commit; git push; chezmoi apply; running bats (CI-only per AGENTS.md); adding dependencies; editing files outside allowed_files; deleting or editing tmux CONFIG files (home/dot_tmux\*) — that is WP-B's job.

## Validation (run and capture output)

1. `ls` each deleted path → confirm gone
2. `grep -rn "tmux\|tpm" install/ home/.chezmoiscripts/ nix/ tests/install/ || true` → only hits must be unrelated (report any remaining hits with justification)
3. `git status --porcelain` → only expected deletions/edits

## Expected artifacts (write to these exact paths)

- report: .orchestration/reports/WP-A.md (what you did, any deviations)
- validation: .orchestration/validation/WP-A.txt (command outputs)
- sandbox: .orchestration/sandboxes/WP-A.md (record: codex exec --sandbox workspace-write fallback, OpenSandbox not installed)
- learning: .orchestration/learning/WP-A.md (reusable learnings or "none")
- autoskill: .orchestration/autoskill/runs/WP-A.md (record "not-used")

## Done signal

After writing all artifacts, run:

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpa orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-A status=ready_for_review report=.orchestration/reports/WP-A.md validation=.orchestration/validation/WP-A.txt sandbox=.orchestration/sandboxes/WP-A.md learning=.orchestration/learning/WP-A.md autoskill=.orchestration/autoskill/runs/WP-A.md"
```

If blocked, still write report+validation explaining the blocker and send the same message with status=blocked.

max_turns: 30
