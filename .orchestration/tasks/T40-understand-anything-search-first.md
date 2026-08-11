# T40: Route agent search through the knowledge graph, enable auto-update, commit .ua baseline

## Objective

Make Claude Code and Codex consult the Understand-Anything knowledge graph
during routine repo exploration (search-first guidance), enable the plugin's
graph freshness hooks, and commit the `.ua/` baseline so both agents can read
it without re-analysis.

## Steps

Work on a new branch `feat/understand-anything-search-first` created from
current `main`; return to `main` when done; do not push.

### Commit 1 — `feat(agents): route agent search through the understand-anything graph`

1. `home/dot_config/claude/rules/understand-anything.md`: add a bullet:
   before repo-wide exploration or symbol searches in a repo that has
   `.ua/knowledge-graph.json`, query the graph first (node `summary` +
   `filePath` let you jump directly); check freshness via `meta.json`
   `gitCommitHash` vs `git rev-parse HEAD` and fall back to grep when stale
   or missing. English, match existing style.
2. `home/dot_config/codex/AGENTS.md` Understand-Anything section: add the
   equivalent bullet in Japanese, matching the section's style.
3. `scripts/generate-agent-configs.py` `render_claude_express_agent`: append
   one sentence to the prompt body: if `.ua/knowledge-graph.json` exists and
   its `meta.json` `gitCommitHash` matches HEAD, grep/read that graph first
   to locate nodes by `summary`/`filePath` before sweeping the tree.
4. Regenerate: `uv run --with pyyaml scripts/generate-agent-configs.py`
   (commit the regenerated `home/dot_claude/agents/express-explorer.md`).
5. `scripts/validate-agent-assets.py` `validate_understand_anything_assets`:
   add token `knowledge-graph.json` for the Claude rule and codex AGENTS.md
   checks (keeps the doc-enforcement pattern).
6. Validate: `uv run --with pyyaml scripts/validate-agent-assets.py` passes;
   `python3 -m py_compile` both scripts.

### Commit 2 — `chore(ua): commit knowledge graph baseline with auto-update`

7. `.gitignore` (repo root): add `.ua/intermediate/`, `.ua/tmp/`,
   `.ua/diff-overlay.json` (match existing file style/ordering).
8. `.ua/config.json`: add `"autoUpdate": true` (keep `outputLanguage`).
9. `git add .gitignore .ua/` — the ignore rules must leave exactly
   `.ua/config.json`, `.ua/.understandignore`, `.ua/knowledge-graph.json`,
   `.ua/fingerprints.json`, `.ua/meta.json` staged; verify with
   `git status --short .ua/` before committing.

## Forbidden actions

- No push, no PR ops, no merge.
- No edits beyond the files listed above.
- No re-running the analysis; commit the existing graph as-is.

## Validation (record output)

- `uv run --with pyyaml scripts/validate-agent-assets.py`
- `git show --stat` of both commits
- `git status --short .ua/` proving only the five intended files were staged
- grep of the new rule lines in all three doc/prompt targets

## Expected artifacts

- report: `.orchestration/reports/T40-understand-anything-search-first.md`
- validation: `.orchestration/validation/T40-understand-anything-search-first.md`
- sandbox: `.orchestration/sandboxes/T40-understand-anything-search-first.md`
- learning: `.orchestration/learning/T40-understand-anything-search-first.md`
- autoskill: `.orchestration/autoskill/runs/T40-understand-anything-search-first.md`

## Done signal

`AGMSG-RESULT v1 task_id=T40-understand-anything-search-first
status=ready_for_review|blocked` with all artifact paths. Max turns: 25.
