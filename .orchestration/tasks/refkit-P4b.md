# AGMSG-TASK refkit-P4b (linter batch 2): E086 state-aware, `proposed-on`, W160, E063 step vocabulary, forbidden_terms

Covers plan task P4-04 (C-06) and P8-04 (F-06 linter side). Sources: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md` §10/§11. Prerequisite: your branch `feat/references-kit-v4-p3` (3af64f0 or later) already contains all tools (P2-A/B/C) and ADR-0003/0004. A parallel worker is editing `examples/**`, `ut/UT_SAMPLE.md`, `ct/CT_SAMPLE.md`, `ut/UT_GUIDE.md` — do not touch those. Note: `selftest` compares mutation results against a per-copy baseline (P2-C); the tree baseline currently fails only on stale generated artefacts (E153/E120/E121/E103) — that is expected and must not be 'fixed' by regenerating them here. Lint: `uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py …`.

## Scope (allowed_files)
`references/tools/kit_lint.py`, `references/adr/ADR_GUIDE.md` (§3 手順 9 and 4 章 front matter row: remove the 「次版」 notes and state the implemented rules), `references/adr/ADR_TEMPLATE.md` (add `proposed-on`), `references/adr/ADR-0003-*.md` and `ADR-0004-*.md` (add `proposed-on: "2026-09-23"` to front matter only), `references/kit.toml` (`[gherkin].forbidden_terms` += 「障害が起きている」), `references/bdd/BDD_GUIDE.md` §3 (one sentence naming E063), `references/03_CONVENTIONS.md` (§4 supersedes row wording only), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P4b.md`.

## Rules to implement
1. E086 (supersede links): let X.supersedes contain Y.
   - Y must exist (else E086).
   - If X.status == proposed: Y.superseded-by may be null or X; Y.status may be accepted or superseded. No error for a missing back-link.
   - If X.status in {accepted, deprecated, superseded}: require Y.status == superseded and Y.superseded-by == X (else E086 with a message naming both files).
   - Any Y.superseded-by == Z requires Z to exist and Z.supersedes ∋ Y (else E086).
   - A document with status superseded must have superseded-by set (else E085/E087 whichever exists for vocabulary; add E088 if none fits — check existing codes first).
2. `proposed-on`: required key for ADRs whose status is proposed; optional otherwise (accepted ADRs written before the key existed must not fail). `date` remains required.
3. W160: for every FR with 優先度 Must, warn when no UT/CT/E2E/UAT/PT test condition lists it in 由来 AND no NVT lists it as 対象. Report the FR IDs. (Warning, not error, because 06 §5 phrases the reverse rule as a smell.)
4. selftest: mutations for (a) proposed successor without back-link → no E086, (b) accepted successor without back-link → E086, (c) superseded-by pointing to a missing file → E086, (d) proposed ADR without `proposed-on` → the new error, (e) a Must FR with no test condition and no NVT → W160.
5. E063 (step vocabulary registry): normalise each Gherkin step (numbers and quoted strings → `<…>`), and require it to appear in the BDD document's 3 章 ステップ語彙表 (same normalisation); error names the step and line. Selftest mutation: an unregistered step.
6. `selftest` completeness guard from P2-B must still pass (new codes need mutations).

## Validation file must contain verbatim
`git diff --stat`; `kit_lint.py check` on the tree (E086 must NOT fire for ADR-0003/0004 proposed with ADR-0001/0002 already marked superseded — if the P4 docs set back-links early, confirm the rule accepts that); `selftest` output; `git show --stat HEAD`; contextdb output.

## Editing discipline
Bash/python writes; intended hunks only.

## Commit
`fix(references/tools): state-aware supersede check, proposed-on, and W160 for untested Must requirements`.

## Forbidden
push; pr-create; editing ADR bodies; weakening existing checks; regenerating generated artefacts.

max_turns=30
