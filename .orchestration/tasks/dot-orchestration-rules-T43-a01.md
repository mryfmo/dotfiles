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

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`;
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

## Orchestrator amendment r4 (2026-10-01; dispatched as AGMSG-ACCEPTANCE status=revise)

r3 (12d3f80 → head 681957f) is correct on its three items (orchestrator
re-derivation: real data exit 1 / 8 regressions, self-compare 0, bad ref 2,
permgate row 25; audit of 12d3f80: Verdict correct). The Codex GitHub review
of 681957f adds two items; fix both in one round on `feat/orchestration-rules-T43`:

1. **Renames fail open (P1, `executable_ua-symbol-coverage:118`).** An old
   path absent at REF is `explained` (`gone`), and its renamed successor has
   `old == 0`, so a rename whose symbols the new graph drops exits 0. Reproduced
   claim: rename `pkg/a.py` (2 defs) → `pkg/b.py`, new graph has only a file
   node for `pkg/b.py` → `a.py explained`, `b.py ok`, `regressions: 0`.
   Fix: detect renames before exempting a disappearance. Preferred shape: add
   `--old-ref <previous-graph-rev>` (the previous graph's `.ua/meta.json`
   `gitCommitHash`), run `git diff --name-status -M --diff-filter=R <old-ref>
   <repo-ref>` once, and for each rename compare the old path's old count
   against the new path's new count under the `min(old, defs at REF)` rule
   (row shows `renamed → <new path>`); a genuine deletion stays `gone`/
   `explained`. When `--repo-ref` is given without `--old-ref`, an absent old
   path with symbols is a REGRESSION (fail closed), not `explained`. Update
   docstring/usage/argparse help, the rule bullet, the Codex mirror, the SKILL
   sentence and the README to name both refs. Tests: rename preserving symbols →
   `ok`; rename dropping symbols → `REGRESSION`, exit 1; deletion with
   `--old-ref` → `explained`; absent path without `--old-ref` → `REGRESSION`.
2. **Codex managed PATH omits `~/.local/bin/common` (P1, codex/AGENTS.md:71).**
   `[shell_environment_policy] set PATH` renders from
   `home/dot_agents/agent-config.yaml:122` without that directory. On this
   machine Codex runs commands through `zsh -lc`, and `home/dot_zshenv`
   prepends the directory, so the helper resolves today (orchestrator test:
   `env -i PATH=<rendered> zsh -lc 'command -v herdr-agents'` → found; `sh -c`
   → not found). The managed PATH must not depend on that: append
   `{{ .chezmoi.homeDir }}/.local/bin/common` after `.local/bin` in the
   `shell_environment_policy.set.PATH` value, regenerate the rendered Codex
   config(s) (`make render-check` green), and update any test pinning that
   string. allowed_files += `home/dot_agents/agent-config.yaml` (that one
   line), the generated Codex config template(s) the generator owns, and
   `tests/unit/test_generate_agent_configs.py`.

Already fixed, no action: the re-anchored "uv-script" comment at
`executable_ua-symbol-coverage:55` is 12d3f80's fix (`"uv run" in first`).

Validation: exit codes captured directly; paste the four new test names from
`make unit-test`, `make render-check`, `make validate-agent-assets`, the real
data run (72b8901 graph vs c3afc7a graph, `--old-ref 72b8901 --repo-ref
c3afc7a`, expect `regressions: 8`, exit 1) and the self-compare. Keep PR #214;
push without `-u`.

## Orchestrator amendment r5 (2026-10-01; dispatched as AGMSG-ACCEPTANCE status=revise)

r4 (6b53337) is correct on both items (orchestrator re-derivation: real data
`--old-ref 72b8901 --repo-ref c3afc7a` exit 1 / 8, self-compare 0, `--old-ref`
alone 2; audit of 6b53337: Verdict correct). The Codex GitHub review of
6b53337 adds two findings whose common root cause is that the gate lets an
**undercounted or absent def-line count explain a loss**. Fix the root cause,
not the two symptoms, in one round on `feat/orchestration-rules-T43`:

1. **Unchanged source cannot explain a loss.** With `--old-ref`, when a path's
   blob is identical at OLD and REF (`git rev-parse OLD:path` ==
   `git rev-parse REF:path`), any decrease in its symbol count is a
   `REGRESSION` regardless of the def-like count (row note `source unchanged`).
   This closes the whole class the reviewer's Ruby example belongs to
   (`private def` uncounted → `defs == 2` explains `3 → 2`), and every other
   grammar gap, because a source the graph refresh did not touch cannot have
   lost a definition. Keep the `min(old, defs)` rule for changed files.
2. **Ruby visibility prefixes** (P2, `:43`): extend `RUBY_DEF` to
   `^\s*(?:(?:private|protected|public)\s+)?(?:def|class|module)\s+\S+`. One
   regex change; one test (unchanged Ruby file with `private def`, graph drops
   the private method → `REGRESSION`, exit 1; the pre-fix negative check must
   show it was `explained`).
3. **Source-backed new paths with zero symbols fail closed** (P1, `:103`, the
   reviewer's second option). A path present in the new graph and absent from
   the old graph, existing at REF with an integer def-like count ≥ 1 and a new
   symbol count of 0, is a `REGRESSION` (row `| path | 0 | 0 | N | REGRESSION |`
   with note `new file, no symbols`). This catches a move plus rewrite below
   git's rename threshold (delete/add pair, successor has defs but no nodes),
   which item 1 cannot see. Ceiling to document in the docstring: a moved and
   rewritten file that keeps *some* nodes is judged only by this zero check.
   Test: the reviewer's reproduction (`a.py` → `b.py` with 80 added lines and
   only a file node for `b.py`) → exit 1.

No CLI change; rule/SKILL/mirror/README wording unchanged unless the exit
semantics text needs the two new REGRESSION reasons (one clause each).
Validation as before, every exit captured directly. Real data
(`--old-ref 72b8901 --repo-ref c3afc7a`): paste the full table; rows that turn
from `explained` into `REGRESSION` under item 1 are expected (source is
identical between those revisions, so every decrease is a real T41
under-extraction) — list them in the report. Self-compare must stay 0.
allowed_files unchanged from r4. Keep PR #214; push without `-u`.

## Orchestrator amendment r6 (2026-10-01; dispatched as AGMSG-ACCEPTANCE status=revise after T48)

r5 (c878b0d) is correct on its three items (re-derived; audit: correct). The
Codex GitHub review of c878b0d adds a P1 (`:184`, a source-backed new path
with 2 defs and 1 node is `ok`) and a P2 (`:52`, shell names with `?` etc. are
not matched, so a changed shell file can have a loss `explained`). Both are
instances of the same remaining design flaw: **a regex def-line count is still
allowed to explain a loss (changed files) or to pass a new file**. Remove that
role once and for all; one commit on `feat/orchestration-rules-T43`:

1. **Def-line counts never explain.** A decrease on any path that exists at
   REF is `REGRESSION`, full stop — including changed files where the count
   dropped. The only `explained` outcomes are structural git facts under
   `--old-ref`: the path is absent at REF and not renamed (`gone`, deletion),
   or it is renamed and the successor's new count ≥ the old count (`renamed →`).
   A renamed path whose successor has fewer symbols is `REGRESSION`. Without
   `--old-ref`, every decrease is `REGRESSION` (as today). The rule text
   already allows acceptance when the validation "cites the source change
   behind each decrease", so a legitimate function deletion in a changed file
   is flagged and cited, not silently explained.
2. **Def-line counts only flag.** For a path new to the graph that exists at
   REF with an integer def-like count, `REGRESSION` when `new < defs` (note
   `new file, <new> of <defs> defs`); the r5 zero-symbol check is the special
   case. Keep the `def-like lines` column as information on every row.
3. **Shell names:** `SHELL_DEF` accepts any non-space, non-`()` characters in
   the name (`function\s+\S+` and `^\s*[^\s()]+\s*\(\)`), so `foo?`, `foo@bar`
   and friends count. One test.
4. Docstring: rewrite the explanation paragraph around the two principles
   above (structural facts explain; counts only flag) and drop the ceilings
   that no longer apply. Rule/SKILL/mirror/README: the phrase "or cites the
   source change behind each decrease" stays; add nothing else unless a
   sentence now contradicts the semantics.
5. Tests: the r2 cases `partial deletion fully accounted → explained` and
   `unchanged source` keep their inputs but the first now expects
   `REGRESSION` (state this in the report); add the `:184` reproduction (new
   `b.py`, 2 defs, 1 node → `REGRESSION`, exit 1) and the shell-name test.
   Negative check against c878b0d for the new tests.

Validation as before, exits captured directly. Real data (`--old-ref 72b8901
--repo-ref c3afc7a`): expect the same 8 regressions (no explained rows exist on
that data). Self-compare 0. allowed_files unchanged. Keep PR #214; push
without `-u`.

## Orchestrator amendment r6-b (2026-10-01 01:3xZ, before the r6 RESULT; PONG msg 562)

The worker measured that in the accepted graph 138 of 185 grammar files already
have fewer function/class nodes than def-like lines, and that r6 item 2
(`new < defs` ⇒ REGRESSION for new paths) fires on `scripts/pr-feedback.py` and
`tests/unit/test_pr_feedback.py` in the real-data run (10 instead of 8). The
def-line heuristic systematically overcounts relative to UA nodes, so
`new < defs` is not a usable gate; my r6 item 2 was miscalibrated.

- Revert item 2 to the r5 rule: a path new to the graph is `REGRESSION` only
  when it exists at REF with ≥ 1 def-like line and **zero** symbols (`new
  file, no symbols`). Keep items 1 (def counts never explain) and 3 (shell name
  characters) exactly as implemented.
- Docstring: state the measured ceiling — partial under-extraction of a
  brand-new file is not detectable by the def-line count (138/185 files of the
  accepted graph have symbols < def-like lines), so only the zero-symbol case
  is flagged; the `def-like lines` column stays informational.
- Tests: drop or invert the `:184` reproduction (2 defs, 1 node) so it pins the
  documented behaviour (`ok`), keep the zero-symbol test.
- Report: include the 138/185 measurement and the command that produced it.
- Real data must be back to `regressions: 8`; self-compare 0.

The Codex `:184` P1 is then dispositioned not-applicable on this measurement,
not fixed; that is the orchestrator's call and goes in the acceptance record.

## Orchestrator amendment r7 (2026-10-01; dispatched as AGMSG-ACCEPTANCE status=revise)

r6/r6-b (afb2c9d, 56f308c) verified: real data 8 (all `source unchanged`),
self-compare 0, 627 tests; audit of 56f308c correct. Three findings remain —
one from the audit of afb2c9d, two from the Codex GitHub review of 56f308c —
all about what the def-line count sees. Fix in one commit on
`feat/orchestration-rules-T43`:

1. **Comment lines are not definitions** (audit P2, `:53`). `def_lines` skips
   lines whose first non-blank character is `#` for every grammar
   (`#disabled() { :; }` must not count). Test: a new shell file with one real
   function and one commented-out one → defs 1.
2. **Python definitions come from `ast`, not a regex** (`:55`). For a path with
   the Python grammar, count `FunctionDef`, `AsyncFunctionDef` and `ClassDef`
   nodes with `ast.parse` (stdlib); fall back to `PYTHON_DEF` only on
   `SyntaxError`. A `def` inside a string literal then counts nothing. Test: a
   new file containing only `DOC = """\ndef not_a_real_function():\n"""` →
   defs 0, `ok`; the uv-shebang test keeps passing.
3. **A new grammar file missing from the graph fails closed** (`:159`). Paths
   that exist at REF, have a def grammar and ≥ 1 def-like line, and appear in
   neither graph are invisible today. Enumerate candidates with
   `git ls-tree -r -z REF` (extension match, or mode 100755 with a recognised
   shebang on line 1) and emit a `REGRESSION` row `| path | 0 | 0 | N | REGRESSION
   | missing from graph |` for each — **restricted to directories the new graph
   already covers** (some path in `new` shares the candidate's parent
   directory), so the graph's own include scope is respected without reading
   the plugin's ignore rules. Measure first on the accepted graph
   (`.ua/knowledge-graph.json` vs `.ua/meta.json` `gitCommitHash`): paste the
   list of such candidates; if it is non-empty, report it and apply the rule
   anyway only if every listed path is a genuine omission (else PONG with the
   list before committing). Test: new `b.py` with two functions, graph
   unchanged, `b.py` in a covered directory → `REGRESSION`, exit 1; the same
   file in an uncovered directory → no row.
4. Docstring: one sentence per item; note that the `def-like lines` column
   for Python is now the `ast` count.

Validation as before, exits captured directly; real data must stay at 8,
self-compare at 0 (if item 3 adds rows on real data, list and explain each).
Negative check against 56f308c for the three new tests. allowed_files
unchanged. Keep PR #214; push without `-u`. Re-anchored comments `:76`
(uv shebang) and `:117` (low-similarity move) are already fixed; no action.

## Orchestrator amendment r8 (2026-10-01; dispatched as AGMSG-ACCEPTANCE status=revise)

r7 (72746d4) verified: comment skip, `ast` counting, missing-from-graph with
the measurement (no candidates at the graph's own revision; the two PR files
at HEAD are genuine omissions); real data 8, self-compare 0 with both refs at
the graph's `gitCommitHash`. No new Codex GitHub comments. The audit of
72746d4 (`…-audit-72746d4.md`) found two items; fix both in one commit:

1. **P2 `:173` fail closed on an unreadable candidate.** In
   `missing_from_graph`, the shebang probe reads `git show REF:path` and
   ignores a non-zero return: an unreadable extensionless executable is
   silently skipped and the run exits 0. Raise `CoverageError` (exit 2) when
   that `git show` fails, as `def_lines` already does. Test: monkeypatch or a
   fake `git` that fails for one 100755 path → exit 2, no table.
2. **P3 `:159` `source unchanged` note after a chmod-only change.** `blobs()`
   now returns `(mode, blob)` and the equality check compares the tuple, so a
   mode-only change suppresses the informational note although the bytes are
   identical. Compare blob ids only. Test: same blob, mode 100644 → 100755,
   symbol decrease → `REGRESSION | source unchanged`.

Validation as before; real data 8, self-compare 0 (both refs = graph
`gitCommitHash`). Negative check against 72746d4 for the two tests. Keep PR
#214; push without `-u`.
