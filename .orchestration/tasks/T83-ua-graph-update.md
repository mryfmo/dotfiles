# T83: Understand-Anything 知識グラフ増分更新(Pi pivot + context diet 反映)

task_id: T83
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: housekeeping (repo rule: graph rebuilds go to a Codex worker under the regime)

## Work order

1. Run the incremental Understand-Anything update for this repo with
   `$understand` (incremental — the graph exists; do NOT run a full
   re-analysis). Sources changed since the last graph commit: Pi pivot
   removals/renames (#135/#136) and the context-diet doc moves (#137).
2. Verify `.ua/meta.json` gitCommitHash equals current HEAD afterward
   and that removed Pi files no longer appear as graph nodes.
3. Do NOT commit (orchestrator commits `.ua/` at acceptance).
   `.ua/intermediate/` and `.ua/diff-overlay.json` stay uncommitted per
   the repo's gitignore rule.

## Allowed files

`.ua/**` plus artifact paths (T83 set).

## Forbidden actions

git commit; git push; chezmoi apply; bats; full re-analysis; source
edits.

## Completion / RESULT contract

Five artifacts; memory add only if a durable decision emerges (else
state none); effects=none; cost line.
Reply `AGMSG-RESULT v1 task_id=T83`. max_turns=12.
