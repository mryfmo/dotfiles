# AGMSG-TASK refkit-P2-A: kit_lint — implement `gherkin_source`, remove the destructive `extract`, fix crash paths, document prerequisites

Covers plan tasks P2-01, P2-07, P2-10 (第 2 部 §4). Findings: E-01, E-08, E-14, E-17, F-03 (第 1 部). Plan file: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md`. Primary sources you may cite: `/home/moriya/Workspace/dotfiles/.orchestration/reports/P0-04-sources.md` (Gherkin Reference, Python `tomllib`, PEP 723). If a needed fact is not there, fetch the official page yourself with WebFetch and add a dated quote to your report; never rely on memory.

Work in `/home/moriya/Workspace/dotfiles-w1` on branch `feat/references-kit-v4`, from the `references/` directory. Run the linter with `uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py …`.

## Scope (allowed_files)
`references/tools/kit_lint.py`, `references/tools/README.md` (new), `references/00_README.md` (§使い方 only), `references/03_CONVENTIONS.md` (§2, §8 only), `references/bdd/BDD_GUIDE.md` (§5 「正本の移管」 row only), `references/bdd/BDD_TEMPLATE.md` (front-matter comment for `gherkin_source` only), `references/05_AI_AGENT_INSTRUCTIONS.md` (the `render_mermaid.py` line only), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P2-A.md`.

## P2-01 `gherkin_source` (E-01, F-03)
Current state: `kit_lint.py` never reads `gherkin_source`; `run()` always treats Markdown fences as the source; `extract` executes `for old in fdir.glob('*.feature'): old.unlink()` (≈line 500), deleting every `.feature` in `features_dir` — including hand-maintained ones after a team has migrated to `.feature` as canonical, which the templates (`BDD_TEMPLATE.md:11`) and conventions (`03 §2`, `02 §2`) explicitly offer.
Required behaviour:
1. Read `gherkin_source` from each BDD document's front matter (`markdown` | `feature`; anything else → new error E124).
2. `markdown` mode: `extract` writes `features/FEAT-nnn.feature` for each fence with a first-line marker comment after `# language:` (e.g. `# generated-by: kit_lint extract — do not edit; source: bdd/BDD_SAMPLE.md`). It may delete only files that carry that marker and no longer correspond to a fence. A `.feature` without the marker in `features_dir` → error E122 and no deletion. `check` keeps E121 (fence ≠ generated file).
3. `feature` mode: `extract` refuses with E123 (message says to run `mirror`). New subcommand `mirror` rewrites the Markdown fences from `features/*.feature` (strip the marker line if present) and leaves everything else in the Markdown untouched. `check` compares fence ↔ `.feature` and reports E121 when they differ, pointing at `mirror`.
4. Do NOT edit `02_RESEARCH_AND_DECISIONS.md` in this task (a parallel task owns it); instead put the wording you propose for the 判断表 row 「Gherkin の置き場」 (mention of `mirror`) in your report under 「02 への反映案」. Gherkin parsing continues to use `gherkin-official` for both sides (public parser; cite the Gherkin Reference for `.feature` being the canonical Cucumber artefact and for `# language:` placement).
5. `selftest`: add mutations (a) `gherkin_source: feature` + run extract → E123, (b) unmarked `.feature` present in markdown mode → E122 and the file survives, (c) edit a fence after `mirror` in feature mode → E121. Each mutation must be detected.
6. Demonstrate in the validation file, on a throw-away copy under `/tmp/refkit-p2a/`: switch `BDD_SAMPLE.md` to `gherkin_source: feature`, hand-edit `features/FEAT-008.feature`, run `extract` (must fail with E123, file untouched — show `sha256sum` before/after), run `mirror`, then `check` (must pass), then hand-edit the fence and `check` (must fail E121).

## P2-07 crash paths and prerequisites (E-08, E-14)
7. `_check_links` (≈line 152): `target.relative_to(self.root.resolve())` raises `ValueError` for a link that resolves outside the root. Report it as a new error E018 (`ルート外へのリンク`) instead of crashing. Add a selftest mutation with a `../../` link to an existing file outside the root.
8. Add an explicit Python-version guard at import time: if `sys.version_info < (3, 11)`, print a one-line message naming the requirement (`tomllib` was added in Python 3.11 — cite the docs) and exit 2. Same guard in `render_mermaid.py`, `run_examples.py`, `portability_test.py` is out of scope for this task (those files belong to P2-C/P2-B); mention it in the report as a follow-up.
9. Create `references/tools/README.md` (Japanese): prerequisites (Python ≥ 3.11 with the reason and citation; `gherkin-official`, `PyYAML`; optional: `playwright` + npm `mermaid` for `render_mermaid.py`, `pytest`/`hypothesis`/`pytest-bdd`/`coverage`/`mutmut` for `run_examples.py`), the recommended `uv run --with …` invocation, each subcommand with its errors, the meaning of `gherkin_source` modes, and the marker line format. Link it from `00_README.md` §使い方 step 3 and from `03_CONVENTIONS.md` §8. In `05_AI_AGENT_INSTRUCTIONS.md` change the line `python tools/render_mermaid.py` to include `--mermaid-dir <mermaid パッケージ>`.

## P2-10 selftest strictness (E-17)
10. In `selftest`, restore the v2 rule: a mutation regex must match exactly once (`n == 1`); `n > 1` is reported as `FIXTURE_AMBIGUOUS` and counts as a selftest failure.

## Validation file must contain verbatim
`git diff --stat`, full output of `kit_lint.py check` (must be 0 errors / 0 warnings on the tree — note: 04/features/evidence are still v3's; if E121 fires because your marker line changes the generated `.feature` bytes, do NOT commit regenerated features here; instead make the marker optional-on-compare (compare ignoring the marker line) so that v3's shipped features still pass, and say so), full `selftest --json` output, the /tmp demonstration transcript, `python3.10`-style guard check (simulate with `uv run --python 3.10 …` if a 3.10 interpreter is available via uv; else state unavailable), `git show --stat HEAD`, contextdb memory-add output.

## Commit
`fix(references/tools): implement gherkin_source modes and stop extract from deleting features` (+ body; `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`). One commit for this task.

## Forbidden
push; pr-create; editing files outside scope; regenerating `04_TRACEABILITY.md`/`evidence/`; weakening or deleting existing checks; adding dependencies beyond `gherkin-official`/`PyYAML`.

max_turns=40
