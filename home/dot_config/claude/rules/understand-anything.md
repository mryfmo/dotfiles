## Understand-Anything

- Use Understand-Anything (`understand-anything@understand-anything`) for a repo-local knowledge graph: `/understand`, `/understand-dashboard`, `/understand-chat`, `/understand-domain`, `/understand-knowledge` (Codex: `$understand`). Never run the token-heavy initial `/understand` in the interactive deep session; delegate it to a worker or a cheaper profile.
- In the dotfiles repository, refresh the graph only with `/understand --full`, as a worker task the operator asks for at a regime boundary; incremental updates cannot publish here (README "Agent review and permission assets"), so the graph is stale between refreshes by design.
- Output lives in `.ua/` (legacy `.understand-anything/`). Commit it except `.ua/intermediate/` and `.ua/diff-overlay.json`, which the target repository's `.gitignore` lists.
- Before repo-wide exploration or symbol searches, query `.ua/knowledge-graph.json` first when it is current: `.ua/meta.json` `gitCommitHash` equals `git rev-parse HEAD`, or `git diff --name-only <hash>..HEAD` lists only `.ua/` and `.orchestration/` paths. Otherwise use grep.
- Graph rebuilds mutate the repository, so under the agmsg regime they are worker tasks. Acceptance needs the `ua-symbol-coverage` table, and a worker leaves the plugin's "graph is stale" hook prompt alone unless `.ua/**` is in its `allowed_files` (agmsg-orchestration SKILL).
- `make update` installs and updates the plugin; restart Claude Code afterwards.
