# AGMSG-TASK dot-ua-graph-refresh-T55-a01 (operator-requested full rebuild)

Drafted 2026-10-02 by the orchestrator seat (`claude-remediation-dot`). The
operator requested (2026-10-02, this session) a full rebuild of the
Understand-Anything knowledge graph as the semantic index for a whole-repository
review. Policy (T52, `.ua/config.json` `autoUpdate: false`): the graph is
refreshed only by operator-requested full rebuilds; incremental updates cannot
publish here (T51). Worker: `claude-standard-dot-a005` in
`~/Workspace/dotfiles/.claude/worktrees/worker-c`.

## Objective

Rebuild `.ua/` from scratch against current `origin/main` (940a3a2b or later)
with the installed Understand-Anything plugin (2.9.7): run `/understand --full`
(the plugin's full-analysis skill), not the incremental procedure. The graph
is currently at `gitCommitHash` 72b89015; 39 non-`.ua`/`.orchestration` paths
changed since then.

- Output stays in `.ua/`; commit `.ua/` except `.ua/intermediate/`,
  `.ua/tmp/` and `.ua/diff-overlay.json` (already gitignored).
- Keep `.ua/config.json` as is (`outputLanguage: en`, `autoUpdate: false`).
- After the build, `.ua/meta.json` `gitCommitHash` must equal your branch HEAD
  (never the pre-change base).

[memory:decision] T55 (operator 2026-10-02): the `.ua/` graph is rebuilt in full
as the semantic index before the whole-repository review of tools, libraries
and content; the orchestrator never runs the graph build in its own session.

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c chore/ua-graph-refresh-T55 origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG blocked. If the worktree has uncommitted files, stop and PONG.
- The Understand-Anything auto-update hook may fire; `.ua/**` is in your
  allowed files, so acting on it is in scope here.

## Allowed files

- `.ua/**` (except the three ignored paths)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-graph-refresh-T55-a01.md` (main checkout)

## Forbidden actions

- Any source, script, rule, test, manifest, or `.gitignore` change; merging;
  force push; local bats; `make apply`/`chezmoi apply`; writes outside the
  worktree except the listed `.orchestration` paths; LLM calls other than
  those the plugin's own skill performs inside your session; pushing `main`.

## Validation commands (paste verbatim output into the validation file)

```
jq -r .gitCommitHash .ua/meta.json
git rev-parse HEAD
git diff --name-only $(jq -r .gitCommitHash .ua/meta.json)..HEAD | head
git show origin/main:.ua/knowledge-graph.json > "$TMPDIR/kg-old.json"
ua-symbol-coverage "$TMPDIR/kg-old.json" .ua/knowledge-graph.json --old-ref 72b890157078c583f45d71a61ee6eba0df86afb5 --repo-ref "$(git rev-parse HEAD)"
python3 -c "import json;g=json.load(open('.ua/knowledge-graph.json'));print(len(g['nodes']),'nodes',len(g['edges']),'edges')"
git diff origin/main --stat | tail -3
gh pr checks <pr-number>
```

`ua-symbol-coverage` is on PATH from `~/.local/bin/common`. Acceptance
requires its table with zero regressions, or a cited source change behind
each decrease (`validateGraph` passing is not sufficient).

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs,
   the PR number and head SHA, node/edge counts before (885/1325) and after.
3. CompactionDB from the main checkout:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] text above>"`;
   paste command and output.
4. `AGMSG-RESULT v1` to the orchestrator via
   `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single-line RESULT>"`
   with all artifact paths; `cost:` line in the report. max_turns=40.

## Revise round 1 (orchestrator, 2026-10-02, after audit of 98bdf43)

Codex audit (`.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md`, Verdict: incorrect) found two P2 defects; the orchestrator reproduced both and extended the second:

1. **Prose in `lineRange`.** Two nodes carry a sentence instead of a numeric range: `file:home/dot_claude/hooks/executable_enforce-uv.sh` and `config:home/dot_claude/modify_private_settings.json` (knowledge-graph.json lines 8938 and 9146 at 98bdf43). Understand-Anything 2.9.7 rejects these fields at load and drops the two nodes plus their edges, which contradicts the reported "0 validation issues". Fix: move the prose to the node's notes field (`languageNotes` or `summary`), restore numeric `lineRange`, and run the plugin's own load/validate path (the one the dashboard and `/understand-chat` use), pasting its output.
2. **Lost `calls` edges.** Per-file outgoing `calls` edges old → new: `attach_comment_files.py` 28 → 0, `.claude/contextdb/contextdb/util.py` 17 → 0, `semantic.py` 1 → 0, and 8 more contextdb files decreased (`normalize.py` 20 → 16, `storage.py` 27 → 24, `redaction.py` 7 → 3, `recall.py` 5 → 3, `memory.py` 6 → 4, `recover_hook.py` 11 → 10, `config.py` 6 → 5, `paths.py` 4 → 3). None of these sources changed between 72b89015 and 940a3a2b. `ua-symbol-coverage` counts symbols, not edges, so it did not catch this. Fix: re-analyze the affected files so every call that exists in source is an edge again; where the analyzer cannot, say so per file.

Additional validation required in the revised validation file (verbatim output):

```
python3 - <<'PY'
import json,collections
O=json.load(open('/dev/stdin')) if False else None
PY
# Per-file outgoing `calls` edges, old graph (origin/main) vs new graph: a table with every file whose count decreased, or the line "no file lost outgoing calls edges". Use the same old/new graphs as ua-symbol-coverage.
# Count of nodes whose lineRange is not a two-integer range: must be 0.
# The plugin's load/validate output for the new graph.
```

Scope and rules unchanged: `.ua/**` only, same branch and PR #226, one new commit on top of 98bdf43 (no force push). Re-run `ua-symbol-coverage` and paste it. Send `AGMSG-RESULT v1 ... round=revise-1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (run it outside the sandbox: in this environment the excludedCommands entry did not take effect for either seat).
