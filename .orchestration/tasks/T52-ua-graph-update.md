# T52: Incremental understand-anything graph update (housekeeping)

task_id: T52
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

## Goal

The repo-local understand-anything knowledge graph (.ua/) is stale
(meta gitCommitHash b0f30b5 vs current main) with real source changes
(scripts/\*.py, vendored compactiondb python, tests). Run the incremental
auto-update procedure so the graph reflects HEAD.

## Procedure

Follow the plugin's auto-update instructions at
/Users/mryfmo/.claude/plugins/cache/understand-anything/understand-anything/2.9.4/hooks/auto-update-prompt.md
(read it first; it is the authoritative procedure): structural
fingerprinting first, LLM analysis only for files with structural changes,
then update .ua/knowledge-graph.json and .ua/meta.json (set gitCommitHash
to current HEAD).

## Allowed files

.ua/\*\* (except leaving .ua/intermediate cleanup per the procedure), plus
your artifact paths (T52 five artifacts).

## Forbidden actions

git commit; git push; chezmoi apply; bats; changes outside .ua/ and
artifacts.

## Validation

1. .ua/meta.json gitCommitHash == `git rev-parse HEAD`.
2. python3 -c json.load on .ua/knowledge-graph.json and .ua/meta.json
   (both parse).
3. Node/edge counts before vs after in the validation artifact.
4. `git status --porcelain` -> only .ua/ paths + artifacts.

## Completion / RESULT contract

Five artifacts (T52). Reply AGMSG-RESULT v1 task_id=T52. max_turns=20.
