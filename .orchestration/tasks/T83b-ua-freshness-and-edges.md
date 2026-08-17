# T83b: UA 鮮度判定意味論の是正+置換ノードのエッジ復元 (PR #138 review)

task_id: T83b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: housekeeping (PR #138 P2 x2, orchestrator-triaged REAL)
depends: T83 (accepted)
branch: chore/ua-graph-t83 (already checked out in the main worktree)

[memory: decision — The UA graph freshness check treats the graph as current when every commit between meta.gitCommitHash and HEAD touches only .ua/ or .orchestration/ paths (exact hash equality is unsatisfiable for graph-carrying commits); and incremental LOAD-PATCH-SAVE merges must preserve or reconstruct every edge whose 両 endpoints survive, verified by an edge diff against the parent graph.]

## Finding 1 (P2): graph-only commits are permanently "stale"

meta.gitCommitHash necessarily records the commit the graph was built
at; the commit that ADDS the graph is its child, so the exact-equality
freshness rule in home/dot_config/codex/AGENTS.md and
home/dot_config/claude/rules/understand-anything.md marks every fresh
graph stale and permanently routes agents to grep.

### Fix (root cause = the check's semantics, not the hash)

Amend BOTH policy docs: compare meta.gitCommitHash with HEAD; if they
differ, the graph is still current when `git diff --name-only
<hash>..HEAD` contains only `.ua/` and/or `.orchestration/` paths; fall
back to grep only when actual sources changed. Keep the wording to one
sentence per doc (do not regrow the dieted files; the codex AGENTS.md
line lives in its kept Understand-Anything section).

## Finding 2 (P2): merge dropped live cross-file edges

The T83 merge replaced changed-file nodes but lost edges from unchanged
nodes to replaced nodes (e.g. check-inbox.sh -> whoami.sh at line 50,
check-inbox.sh -> config.sh at 79-80; command templates -> join.sh /
whoami.sh).

### Fix (root cause = merge invariant, not the two named edges)

1. Diff the parent-commit graph (git show df85b37:.ua/knowledge-graph.json
   or the pre-T83 version from git history) against the current graph:
   enumerate EVERY removed edge.
2. Classify each: endpoint-deleted (Pi removal — legitimate) vs
   both-endpoints-alive. For the latter, verify the underlying
   relationship in the source; restore every edge whose relationship
   still holds. Record the full classification table in the validation
   artifact (no sampling).
3. Confirm the two named cases restored; re-run the UA core validator
   (success=true) and note node/edge counts before/after.

## Allowed files

.ua/\*\*, home/dot_config/codex/AGENTS.md,
home/dot_config/claude/rules/understand-anything.md, artifact paths
(T83b set).

## Forbidden actions

git commit; git push; chezmoi apply; bats; full re-analysis; rule
regrowth beyond the one-sentence semantics fix.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line.
Reply `AGMSG-RESULT v1 task_id=T83b`. max_turns=15.
