# AGMSG-TASK refkit-P2-B: kit_lint — configurable IDs, multi-document support, evidence-bound `passed`, structured E158, generic selftest, honest portability test

Covers plan tasks P2-02, P2-04, P2-05, P2-06 (第 2 部 §4). Findings: F-02, E-11, E-12, E-04/D-03, E-10, E-03, E-09, E-15. Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md`. Sources: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md`. Work in `/home/moriya/Workspace/dotfiles-w1`, `references/`, branch `feat/references-kit-v4`, on top of refkit-P2-A's commit. Lint invocation: `uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py …`.

## Scope (allowed_files)
`references/tools/kit_lint.py`, `references/tools/portability_test.py`, `references/kit.toml`, `references/03_CONVENTIONS.md` (§3, §5 only), `references/bdd/BDD_TEMPLATE.md` (front matter only), `references/bdd/BDD_SAMPLE.md` (front matter only), `references/ut/UT_TEMPLATE.md`, `references/ct/CT_TEMPLATE.md`, `references/st/ST_TEMPLATE.md`, `references/uat/UAT_TEMPLATE.md` (the 実行結果 table shape only), the matching `*_SAMPLE.md` (same table only), `references/tools/README.md`, `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P2-B.md`.

## P2-02 IDs and multiple documents (F-02, E-11, E-12)
1. Add `[ids] prefix = ""` to `kit.toml`. Build the `ID` regex from an explicit allow-list of kinds (`FR|NFR|GOAL|KPI|GRD|EVID|ACT|RISK|NVT|ADR|FEAT|RULE|SCN|Q|UT|CT|E2E|UAT|PT|PER`) plus the optional prefix; `E2E-001` must match, `SHA-256`, `APP-001`, `SPEC-001` must not. Derive `ITEM` from the same table. Update `03 §3` to describe `[ids].prefix` and delete the sentence telling users to edit `kit_lint.py`.
2. E150/E151: evaluate over the union of all UAT documents, not per document.
3. `prd` may list several PRDs: run the PRD checks per document and check FR/NFR/GOAL/KPI/GRD/NVT ID uniqueness across all PRDs (E030). `trace` emits one section per PRD.
4. selftest mutations: prefixed IDs ignored when prefix unset (must be an error, not silence), UAT split in two documents (must pass), duplicate FR-001 across two PRDs (E030), `SHA-256` in prose (no error).

## P2-04 evidence-bound `passed` (E-04, D-03)
5. Remove the `'evidence' in d.meta` condition: any document with `last_run` in {passed, failed} must carry `evidence:` pointing at an existing file (E155). Add `evidence:` to `BDD_TEMPLATE.md` front matter (comment: 実行証跡の JSON。`last_run` が passed/failed のとき必須) and set `evidence: ../evidence/example_tests.json` in `BDD_SAMPLE.md`. Update 03 §5. selftest mutation: BDD passed without evidence → E155.

## P2-05 structured E158 (E-10)
6. Define a fixed 実行結果 table for UT/CT/ST/UAT templates (columns exactly: `項目 | 値 | 証跡のキー`), where 証跡のキー names the JSON path in the evidence file (e.g. `ut.passed`, `ut.total`, `ut.branch_coverage_percent`, `mutation.killed`, `mutation.total`). E158 parses that table and compares each value numerically with the evidence JSON; a mismatch names the row. Rewrite the corresponding tables in UT_SAMPLE/CT_SAMPLE (values copied from the current `evidence/example_tests.json`; keep every number you cannot find in the evidence out of the table and mention it in the report — P7 will fix the prose). ST/UAT samples get the table with `not_run` values. selftest mutations: +1 on a count (E158), same number elsewhere in prose (no error).

## P2-06 generic selftest and honest portability test (E-03, E-09, E-15)
7. Rewrite `MUTATIONS` so each targets template structure (headings, table headers, front-matter keys, Gherkin keywords) and is located by structure, not by sample-specific strings. Missing fixture → `skipped` (reported separately, not counted as `failed`).
8. Build the list of all `E…`/`W…` codes emitted by the linter (regex over `self.err(`/`self.warn(` calls at startup) and make selftest fail if any code lacks at least one mutation. Add mutations until the set is complete (current uncovered list is in 第 1 部 E-15).
9. `portability_test.py`: copy the shipped `kit.toml` and only rewrite paths; keep `[vocab.*]`, `[tests]`, `[evidence]`, `[ids]`; fill placeholders `{{a｜b}}` with the first alternative; generate a minimal test project (one `test_*.py` with the names used in the UT/CT templates) so `[tests]` checks run; run `trace`, `extract`, `render_mermaid.py --mermaid-dir <use references/.mermaid/11/node_modules/mermaid if present, else skip with an explicit note>`, `check`; every exit code must be 0 (or the recorded skip).

## Validation file must contain verbatim
`git diff --stat`; `kit_lint.py check` on the tree (0 errors, 0 warnings — if E158 now fails because UT/CT sample tables were rewritten, fix the tables, never the check); `selftest --json /tmp/...` (all codes covered, all detected, skipped list empty on this tree); `portability_test.py` full output; the ID regex unit demonstration (a short python snippet showing matches for `E2E-001`, `PAY-FR-001` with prefix, and non-matches for `SHA-256`, `APP-001`); `git show --stat HEAD`; contextdb memory-add output.

## Commit
`fix(references/tools): configurable ids, multi-doc lint, evidence-bound results, complete selftest` (+ body, `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`).

## Editing discipline
Your Edit/Write tools may run a post-write formatter that rewrites whole files (table realignment, CJK spacing) and can break template↔sample exact-match checks. Apply edits so that `git diff` contains only the intended hunks (e.g. Bash/python writes), and inspect `git diff --stat` and `git diff` before committing. Never commit formatter noise.

## Forbidden
push; pr-create; editing outside scope; regenerating 04/features/evidence; weakening checks; new dependencies.

max_turns=50
