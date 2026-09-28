# T33c learning triage

## Candidates

1. Understand-Anything's `prepare-incremental.mjs` forces FULL_UPDATE once
   more than 30 files change structurally. A long-stale graph (68 commits
   here) therefore costs a full rebuild of about 40 dispatches. Refreshing
   the graph at every accepted task keeps it incremental.
2. Running `/understand` from a Claude worktree redirects output to the
   main checkout by default. Set `UNDERSTAND_NO_WORKTREE_REDIRECT=1` when
   the graph must be committed on the worktree's branch.
3. The skill's first plugin-root candidate is the Claude plugin cache, which
   ships without `packages/core/dist`. Build the core once in
   `~/.understand-anything-plugin` and point scripts there.
4. Plugin 2.9.7 merge gaps: `.bats` files are not recognised as tests, and
   `link_tests` indexes only `file:` nodes. Plugin extraction gap: shell
   functions with a subshell `( … )` body are missed. All three are upstream
   issue candidates.
5. Phase 7 cleanup writes `.ua/.trash-*`, which this repo's `.gitignore`
   does not cover. Either add `.ua/.trash-*/` to `.gitignore` in a future
   task or keep skipping that step.

6. **Revision 2.** Before committing, always run the plugin core's
   `validateGraph` (`packages/core/dist/index.js`, the path `loadGraph` and
   the dashboard use) on `.ua/knowledge-graph.json`, and require
   `nodesOut == nodesIn` and `edgesOut == edgesIn`. The skill's inline
   Phase 6 validator checks only presence and references, not field types.
   An LLM analyzer put prose into `lineRange`, a numeric tuple in the
   schema; that passed merge, assemble review and inline validation, then
   silently dropped 2 nodes and 42 edges at load time. A 15-line wrapper
   (`.ua/tmp/ua-core-validate.mjs` in this run) is enough.

## Promotion

None. These are candidates only.
