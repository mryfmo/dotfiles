# T85: UA 知識グラフ増分更新(#140 反映)

task_id: T85
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: housekeeping (repo rule: graph rebuilds are worker tasks)
depends: T84c (accepted); main at b48d52c

## Work order

1. Incremental UA update for sources changed by #140 (zsh trio,
   modify*private* renames, update-agent-assets resolver, doctor drift
   check, lifecycle.bats). No full re-analysis.
2. Pin meta.gitCommitHash to current main HEAD (b48d52c) — a mainline
   commit, so no post-squash re-pin will be needed (T83b/#139 rule).
3. Preserve-or-reconstruct edges per the T83b merge invariant: full
   removed-edge classification vs the parent graph, restore every
   relationship whose endpoints survive; validator success=true.
4. Do NOT commit (orchestrator commits at acceptance).

## Allowed files

.ua/\*\* plus artifact paths (T85 set).

## Forbidden actions

git commit; git push; chezmoi apply; bats; full re-analysis; source
edits.

## Completion / RESULT contract

Five artifacts; memory add only if a durable decision emerges;
effects=none; cost line.
Reply `AGMSG-RESULT v1 task_id=T85`. max_turns=12.
