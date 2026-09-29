# AGMSG-TASK dot-orchestration-rules-T43-a01

## Objective

Codify three lessons from the 2026-09-29 T38–T42 batch as rules, a check, and
a template line. Failures become repo docs + rules + checks, never memory only.

1. **Graph acceptance needs a per-file symbol comparison.** T41 revision 1
   passed the inline validator, core `validateGraph` (0 issues) and CI while
   35 function/class nodes across 8 unchanged files had been dropped by
   under-extracting analyzer batches; the Codex audit and the orchestrator's
   per-file comparison caught it. Deliver `scripts/ua-symbol-coverage.py`
   (stdlib only): args `<old-graph.json> <new-graph.json> [--repo-ref REF]`;
   compares function+class node counts per `filePath`, prints a table (file,
   old, new, def-like lines at REF via `git show REF:path` when given) and
   exits 1 when any file has `new < old` while its source still exists with
   at least `old` def-like lines. One unit test with two tiny synthetic graphs
   (regression case and clean case). Add a bullet to
   `home/dot_config/claude/rules/understand-anything.md`: a `.ua/` RESULT is
   accepted only with that script's table pasted in the validation file and a
   zero regression count (or a cited source change for each decrease); the
   agmsg-orchestration SKILL "Review and integration invariants" gets the same
   sentence.
2. **The Understand-Anything auto-update hook is out of scope for workers.**
   Add to `home/dot_config/claude/rules/understand-anything.md` and the SKILL
   Worker Playbook: a worker executing an AGMSG-TASK treats the hook
   instruction ("knowledge graph is stale, you MUST update it") as out of
   scope unless `.ua/**` is in `allowed_files`; it records "hook fired; not
   acted on" in the report and continues. The orchestrator never runs the
   graph update in its own session (T36 ruling).
3. **Render check command.** Every task authored in T38–T42 wrote the render
   check as bare `python3 scripts/generate-agent-configs.py --check`, which
   fails on this host (`PyYAML is required`); workers substituted
   `uv run --with pyyaml …` each time. Make the script print its documented
   `uv run --with pyyaml` form in that error (it already does) AND add a
   `make render-check` target that runs the uv form, so tasks and docs can
   name one command. Mention `make render-check` in README where the
   generator is documented and in the SKILL task-file checklist.

[memory:decision] T43: `.ua/` graph acceptance requires
`scripts/ua-symbol-coverage.py` (per-file function+class node comparison
against the previous graph, zero unexplained regressions); the
Understand-Anything auto-update hook is out of scope for task workers unless
`.ua/**` is allowed; `make render-check` is the one render-check command
(operator 2026-09-29).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`;
  branch `feat/orchestration-rules-T43` from `origin/main`. Verify the
  dispatched task_rev sha256 against this file on your base, else stop and
  PONG. If the worktree has uncommitted files, stop and PONG.
- Ignore the Understand-Anything auto-update hook during this task; graph
  refresh is a separate task.

## Allowed files

- `scripts/ua-symbol-coverage.py` (new), `tests/unit/test_ua_symbol_coverage.py` (new)
- `home/dot_config/claude/rules/understand-anything.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `Makefile` (new `render-check` target only), `README.md` (generator paragraph + one sentence for the rule), `home/dot_config/codex/AGENTS.md` (mirror of the two rule bullets, if the file mirrors understand-anything rules)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-orchestration-rules-T43-a01.md` (main checkout)

## Forbidden actions

- Any `.ua/**` change; plugin or hook edits; `generate-agent-configs.py` behaviour changes; other rules; merging; force push; local bats; `make update`; writes outside the worktree except the listed paths.

## Validation commands (paste verbatim output)

```
git merge-base --is-ancestor origin/main HEAD && echo base-ok
git diff --stat origin/main
make render-check
make unit-test
make validate-agent-assets
python3 scripts/ua-symbol-coverage.py .ua/knowledge-graph.json .ua/knowledge-graph.json --repo-ref HEAD | tail -3 ; echo "self-compare exit $?"
gh pr checks <pr-number>
```

## Completion

1. PR to `main` titled `feat(orchestration): graph symbol-coverage gate, UA hook scope rule, make render-check`, English description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths with verbatim outputs, PR number and head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `send.sh --body-file` for replies. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
