# WP-C: Remove Hermes installation path

task_id: WP-C
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpc

## Objective

Remove the Hermes Agent installation path from this chezmoi-managed dotfiles repo. Hermes config/manifest/generator removal is WP-D; skills removal is WP-E (do NOT touch those).

## Changes (exhaustive — do all, nothing else)

DELETE:

- install/common/hermes.sh
- home/.chezmoiscripts/common/run_once_after_04-install-hermes.sh.tmpl
- tests/install/common/hermes.bats

EDIT:

- home/.chezmoi.yaml.tmpl: remove the `hermes:` block (lines ~29-30, `hermes:\n    install: true`). KEEP the `cognee:` block and everything else byte-identical.
- tests/install/common/lifecycle.bats: remove hermes-related test cases/references only; keep the rest of the file working.

Check: verify with `grep -rn "\.hermes\.install\|hermes" home/.chezmoiscripts/ home/.chezmoi.yaml.tmpl install/` that no template still references the removed `.hermes` data key (a leftover reference would break chezmoi templating).

## Allowed files (edit boundary)

Only the files listed above, plus your artifact paths below.

## Forbidden actions

git commit; git push; chezmoi apply; running bats; adding dependencies; editing home/private_dot_hermes/, home/dot_agents/, scripts/, Makefile, README (other tasks own those).

## Validation (run and capture output)

1. deleted paths gone
2. grep from the Check section → clean
3. `git status --porcelain` → only expected changes

## Expected artifacts (write to these exact paths)

- report: .orchestration/reports/WP-C.md
- validation: .orchestration/validation/WP-C.txt
- sandbox: .orchestration/sandboxes/WP-C.md (record: codex exec --sandbox workspace-write fallback)
- learning: .orchestration/learning/WP-C.md ("none" if nothing)
- autoskill: .orchestration/autoskill/runs/WP-C.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpc orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-C status=ready_for_review report=.orchestration/reports/WP-C.md validation=.orchestration/validation/WP-C.txt sandbox=.orchestration/sandboxes/WP-C.md learning=.orchestration/learning/WP-C.md autoskill=.orchestration/autoskill/runs/WP-C.md"
```

If blocked: same message with status=blocked, artifacts explaining why.

max_turns: 30
