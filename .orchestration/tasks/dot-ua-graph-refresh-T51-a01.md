# AGMSG-TASK dot-ua-graph-refresh-T51-a01

Drafted 2026-10-02. Worker-c (`claude-standard-dot-a005`), branch
`chore/ua-graph-refresh` from `origin/main` (ef9e5be or later). Verify the
dispatched task_rev sha256 against this file; else stop and PONG blocked.

## Objective

The Understand-Anything knowledge graph is stale: `.ua/meta.json`
`gitCommitHash` is 72b8901 while `origin/main` is ef9e5be, and
`git diff --name-only 72b8901..ef9e5be` lists 31 paths outside `.ua/` and
`.orchestration/` (T43–T50: `executable_herdr-agents`, `check-regime-boundary.sh`,
`check-agent-runtime.py`, `validate-agent-assets.py`, `require-crit-review.py`,
`pr-feedback.py`, tests, rules, SKILL, README, manifest). The SessionStart and
PostToolUse hooks report it on every commit. Under the regime a graph refresh
mutates the repository, so it is this task, not an orchestrator action.

Refresh the graph **incrementally** with the plugin's own procedure
(`~/.claude/plugins/cache/understand-anything/understand-anything/2.9.7/hooks/auto-update-prompt.md`,
or the installed version's equivalent): `prepare-incremental.mjs` from
`72b890157078c583f45d71a61ee6eba0df86afb5`, `compute-batches.mjs` for the
changed files, file-analyzer only for those batches with `previousSymbols`,
`merge-batch-graphs.py`, the symbol retry if `incremental-symbol-report.json`
lists unresolved files, architecture/tour only if the plan says
`ARCHITECTURE_UPDATE`, then `finalize-incremental.mjs`. If the plan says
`FULL_UPDATE`, stop and PONG `status=blocked` with the plan file pasted — a
full analysis is a separate decision.

## Deliverables

1. Updated tracked `.ua/` files only: `knowledge-graph.json`,
   `fingerprints.json`, `meta.json` (`gitCommitHash` = the branch's base
   commit on `origin/main`), and `config.json`/`.understandignore` only if the
   procedure changes them. `.ua/intermediate/`, `.ua/tmp/` and
   `.ua/diff-overlay.json` stay gitignored and uncommitted.
2. Acceptance gate evidence (rule `home/dot_config/claude/rules/understand-anything.md`):
   the full table from
   `bash home/dot_local/bin/common/executable_ua-symbol-coverage
<old-graph> <new-graph> --old-ref 72b8901 --repo-ref <new meta gitCommitHash>`
   (the installed `ua-symbol-coverage` is absent until the operator's
   `chezmoi update`; the repo copy is the same script), where `<old-graph>`
   is `git show 72b8901:.ua/knowledge-graph.json` saved to a scratch file.
   Every `flag` row is explained in the report with the structural git fact
   (deleted/moved file, removed definitions) or treated as a defect to fix by
   re-analyzing that file.
3. Report: the plan action, files re-analyzed, deleted/ignored/cosmetic
   counts, whether architecture/tour ran, node/edge counts before and after,
   and the `incremental-symbol-report.json` summary (no still-present or
   unknown omissions).
4. `[memory:decision]` T51: the `.ua/` graph is refreshed incrementally from
   `meta.gitCommitHash` to the current main head by a worker task whenever the
   hooks report it stale; acceptance needs the `ua-symbol-coverage` table with
   every flag explained (operator 2026-10-02).

## Allowed files

- `.ua/knowledge-graph.json`, `.ua/fingerprints.json`, `.ua/meta.json`
  (`.ua/config.json`, `.ua/.understandignore` only if the procedure changes them)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-graph-refresh-T51-a01.md`
- `.agents/worklog/**` waived.

## Forbidden actions

Editing any source, test, rule, skill, hook or README; `/understand --full`
or any whole-codebase analysis; committing `.ua/intermediate/`, `.ua/tmp/` or
`.ua/diff-overlay.json`; hand-editing graph JSON; touching other worktrees;
`.orchestration/acceptance/**`; merge; force-push; `--delete-branch`; local
`bats`; `make update`/`upgrade`.

## Validation (verbatim output)

`node … prepare-incremental.mjs` plan summary, `python … merge-batch-graphs.py`
result, `node … finalize-incremental.mjs` report, the `ua-symbol-coverage`
table, `python3 -c "import json; d=json.load(open('.ua/knowledge-graph.json')); print(len(d['nodes']), len(d['edges']))"`
before and after, `git status --short .ua`, `make validate-agent-assets`,
`gh pr view <n> --json url,headRefOid,mergeStateStatus`, `gh pr checks <n>`,
and the CompactionDB `memory add --kind decision --scope project` command.

## Completion

English PR to `main`, CI green on Linux and macOS, artifacts at the expected
paths, `AGMSG-RESULT v1` with `cost:` in the report. max_turns=40.
