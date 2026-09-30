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

## Orchestrator amendment r3 (2026-09-30T04:30Z; dispatched as AGMSG-ACCEPTANCE status=revise; task_rev of the original file is superseded by this file's sha256 at dispatch)

Codex GitHub review on 1843dd1 (PR #214) and the Codex audits of 99c1174 and
1843dd1 leave three confirmed items. Fix all three in one round on
`feat/orchestration-rules-T43`:

1. **Wrong `--repo-ref` semantics in the rule.** `def_lines(REF)` explains a
   decrease only when `new >= min(old, defs)`, so `--repo-ref <base>` (the
   pre-change source) turns every legitimate deletion into a REGRESSION. The
   ref must be the revision the new graph was built from (`.ua/meta.json`
   `gitCommitHash` of the new graph, normally `HEAD`). Change the bullet in
   `home/dot_config/claude/rules/understand-anything.md`, the Codex mirror
   `home/dot_config/codex/AGENTS.md`, the SKILL sentence, the script's usage
   text, and add one test: a file whose function is deleted at REF is
   `explained`, while the same graph loss with the source unchanged at REF is
   `REGRESSION`.
2. **The global rule mandates a repo-local script.** The rule is installed for
   every repository, but `scripts/ua-symbol-coverage.py` exists only here.
   Ship the helper on PATH as
   `home/dot_local/bin/common/executable_ua-symbol-coverage` (chezmoi applies it
   to `~/.local/bin/common`; shdoc/`@file` header not required for a Python
   executable but keep the module docstring) and make the rule, mirror, SKILL,
   README and the test import invoke/load that path. Delete `scripts/ua-symbol-coverage.py`
   (no duplicate). `make render-check` is unaffected.
3. **`uv run --script` executables are not recognised as Python.**
   `def_pattern` (script:48-51) matches only `.py` or `python` in line 1;
   `#!/usr/bin/env -S uv run --script` files (for example
   `home/dot_local/bin/common/executable_permgate`, 16 nodes) always report
   REGRESSION. Recognise a first line containing `uv run` as Python; add one
   test with that shebang.

Validation for r3: every exit code captured directly (`cmd; echo exit=$?`),
never after a pipe — the 1843dd1 audit rejected `| grep …; echo exit=$?` as
evidence. Re-run the real-data check (72b8901 graph vs c3afc7a graph,
`--repo-ref c3afc7a`) and paste the exit. allowed_files += the new executable
path; everything else unchanged. Keep the PR; push without `-u`.
