# AGMSG-TASK refkit-P2-C: Mermaid scope/type checks, run_examples measurement fixes, Chromium sandbox default

Covers plan tasks P2-03, P2-08, P2-09 (第 2 部 §4). Findings: E-06, E-07, E-13, G-14, E-16. Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md`. Sources: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md` (§5 coverage.py JSON fields and formula, §7 pytest JUnit `time`, §14 Mermaid diagram keywords/securityLevel, §4 mutmut config keys). Work in `/home/moriya/Workspace/dotfiles-w1`, `references/`, branch `feat/references-kit-v4`, on top of refkit-P2-B.

## Scope (allowed_files)
`references/tools/kit_lint.py`, `references/tools/render_mermaid.py`, `references/tools/run_examples.py`, `references/kit.toml`, `references/03_CONVENTIONS.md` (§7 only), `references/examples/flowapprove_core/pyproject.toml` (`[tool.mutmut]`, pytest markers only), `references/tools/README.md`, `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P2-C.md`.

## P2-03 one fence extractor, same document set, diagram-type check (E-06, E-07)
1. Move fence extraction into one function used by both `render_mermaid.py` and `check_mermaid` (accept column-0 ``` and ~~~, 4+ backticks, indented fences as CommonMark defines them). Both consumers iterate the same document set: the union of `[docs]` globs from `kit.toml` (render_mermaid must read kit.toml instead of `ROOT.rglob('*.md')`).
2. `kit.toml`: `[mermaid] allowed_types = ["flowchart", "sequenceDiagram", "stateDiagram-v2"]`; new error E104 when a fence's first non-directive line is not one of them (cite Mermaid docs for the type keywords; treat `flowchart TD/LR` etc. as `flowchart`; reject `graph`, `stateDiagram` (v1), `classDiagram`…). Update 03 §7.
3. selftest mutations: mermaid block in a Markdown outside the globs (no E103), `~~~mermaid` fence (no E103, still rendered and hashed), `classDiagram` (E104).

## P2-08 run_examples measurement (E-13, G-14)
4. Use `[sys.executable, '-m', 'pytest' | 'coverage' | 'mutmut']`; catch `subprocess.TimeoutExpired` → `status: timeout` in the JSON; read the mutation target from `pyproject.toml [tool.mutmut]` (use the key the current mutmut docs define — see sources §4 — and update pyproject accordingly); record per-test durations from pytest's JUnit XML (`--junitxml`), and record `pytest`, `hypothesis`, `pytest-bdd`, `coverage`, `mutmut` versions.
5. Coverage: run with `--branch`; from `coverage json` take `covered_branches`/`num_branches` → `branch_coverage_percent` (true branch %), and `percent_covered` → `line_and_branch_percent`; document both keys in tools/README.md with the formula quoted from the sources.
6. Do not commit a regenerated `evidence/example_tests.json` in this task (P9 regenerates everything); run the script writing to `/tmp/refkit-p2c/` (add an `--out` option if missing) and paste the JSON summary.

## P2-09 Chromium sandbox default (E-16)
7. Remove `--no-sandbox` from the default Chromium launch; add `--allow-no-sandbox` which, when passed, re-adds it and records `"no_sandbox": true` in `mermaid_render.json`. Verify on this machine that all 20 diagrams render with the sandbox enabled using `references/.mermaid/11/node_modules/mermaid` and `.../12/...` (write output to `/tmp/refkit-p2c/`, do not commit new evidence).

## Validation file must contain verbatim
`git diff --stat`; `kit_lint.py check` (0/0); `selftest` output; `render_mermaid.py` runs for 11.x and 12.x with the sandbox on (20/20); `run_examples.py --mutation --out /tmp/refkit-p2c/example_tests.json` output and the JSON's summary block; `git show --stat HEAD`; contextdb memory-add output.

## Commit
`fix(references/tools): unify mermaid scope, enforce diagram types, measure branch coverage and durations, default to sandboxed chromium`.

## Editing discipline
Your Edit/Write tools may run a post-write formatter that rewrites whole files (table realignment, CJK spacing) and can break template↔sample exact-match checks. Apply edits so that `git diff` contains only the intended hunks (e.g. Bash/python writes), and inspect `git diff --stat` and `git diff` before committing. Never commit formatter noise.

## Forbidden
push; pr-create; editing outside scope; committing regenerated evidence; weakening checks; new dependencies beyond those already used by the tools.

max_turns=50
