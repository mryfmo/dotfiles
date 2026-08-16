# T62c: Add the omitted update_compactiondb function node (PR #130 bot finding)

task_id: T62c
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

[memory: decision — A refreshed UA node family must enumerate ALL function nodes of the file; T62b's updater refresh omitted update_compactiondb (scripts/update-agent-assets.sh:646-651), which is now added with its contains edge.]

## Finding (chatgpt-codex-connector on PR #130, orchestrator-triaged REAL)

The refreshed update-agent-assets.sh node family omits a function node
for `update_compactiondb` (defined at scripts/update-agent-assets.sh:
646-651): the graph jumps from `update_codex_understand_anything`
directly to `main` with no node or `contains` edge, so the CompactionDB
updater behavior is unnavigable despite being mentioned in the `main`
summary and covered by the fingerprint.

## Fix (exact)

1. Work on the chore/ua-shell-sources branch state (the orchestrator will
   supply the current .ua files in the MAIN worktree — they are the same
   content that PR #130 carries; edit them in the main worktree as
   usual).
2. Add the `update_compactiondb` function node following the exact schema
   of its sibling updater function nodes (id convention, summary, line
   range 646-651 or the actual current range — verify against the file),
   plus the same `contains` edge shape from the file node.
3. Audit the rest of the refreshed family for ANY other function defined
   in update-agent-assets.sh that lacks a node (list every function via
   grep '^function \|^[a-z_]\*() {' and diff against the node set; report
   the audit table). Fix any additional omission the audit finds — the
   root cause is an incomplete enumeration, not just one missing entry.
4. Update counts in meta if the schema tracks them; graph must parse.

## Allowed files

.ua/\*\* plus your artifact paths (T62c five artifacts).

## Forbidden actions

git commit; git push; chezmoi apply; bats; changes outside .ua/ and
artifacts.

## Validation

1. JSON parse of all three .ua files.
2. Audit table: every function in update-agent-assets.sh vs node
   presence — all covered after the fix.
3. Node/edge counts before vs after.
4. `git status --porcelain` -> only .ua/\*\* + artifacts.

## Completion / RESULT contract

Five artifacts (T62c set); memory add with the decision fact;
effects=none.
Reply `AGMSG-RESULT v1 task_id=T62c status=ready_for_review`. max_turns=15.
