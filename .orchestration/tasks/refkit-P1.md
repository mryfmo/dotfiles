# AGMSG-TASK refkit-P1: import kit v3 as the v4 baseline tree and reproduce its validation

Covers plan tasks P1-01, P1-02, P1-03, P1-04, P1-05 and P0-03 (baseline reproduction). Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/ai-references-vivid-sparrow.md` (第 2 部 §3 and P0-03). The findings referenced below (A-01 … E-02) are in 第 1 部 of the same file — read section A and E before starting.

## Objective
Replace the current flat, mixed-generation `references/` layout with the single v3 kit tree, archive the zips with checksums, and reproduce the kit's own validation (`kit_lint`, examples, Mermaid) on this machine so we know the real baseline (versions, results) before any content changes.

## Inputs (read-only, outside your worktree)
`/home/moriya/Workspace/dotfiles/references/` in the MAIN worktree (untracked there). It contains 30 loose `.md` files and 4 zips: `PRD_ADR_BDD.zip`, `PRD_ADR_BDD_Kit_v2_20260919.zip`, `PRD_ADR_BDD_TEST_Kit_v3_20260919.zip`, `TestSuite.zip`. Do not modify anything in the main worktree.

## Scope (allowed_files, all inside /home/moriya/Workspace/dotfiles-w1)
- `references/**` (new tree), `.gitignore`
- `.orchestration/reports/refkit-P1.md`, `.orchestration/validation/refkit-P1.md`, `.orchestration/sandboxes/refkit-P1.md`, `.orchestration/learning/refkit-P1.md`, `.orchestration/autoskill/runs/refkit-P1.md`

## Steps
### P1-02 archive first
1. `mkdir -p references/archive` and copy the 4 zips there unchanged. Create `references/archive/SHA256SUMS.txt` (`sha256sum *.zip`) and `references/archive/README.md` stating, in Japanese: provenance of each zip (v2 = kit 2.0.0, v3 = kit 3.0.0, `PRD_ADR_BDD.zip` = flat v2 docs + nested v2 kit zip, `TestSuite.zip` = flat v3 test docs + nested v3 kit zip; the nested zips are byte-identical to the standalone ones), the observed timestamp facts (kit entries stamped JST 16:40 / 17:24–17:25 on 2026-09-19; outer zips created 2026-09-23), and that these archives are history only and the canonical content is the tree in `references/`.
### P1-01 import
2. Extract `prd_adr_bdd_test_kit_v3/` from the v3 zip so that its contents land directly under `references/` (i.e. `references/00_README.md`, `references/prd/…`, `references/tools/…`, etc.). Verify: `cd references && sha256sum -c SHA256SUMS.txt` → every line OK.
3. Do NOT copy any of the 30 loose `.md` files (they are all byte-identical copies of v2 or v3 files; see 第 1 部 A provenance table). Verify no file named `*_TEST_SUITE.md` or containing `DEVISIONS` exists under `references/`.
4. Run the link scan below from `references/` and paste its output; expected: zero `DANGLING`.
```bash
python3 - <<'PY'
import re,glob,os
for p in sorted(glob.glob('**/*.md',recursive=True)):
    for m in re.finditer(r'\]\(([^)#\s]+)(#[^)]*)?\)',open(p,encoding='utf-8').read()):
        t=m.group(1)
        if t.startswith('http'): continue
        q=os.path.normpath(os.path.join(os.path.dirname(p),t))
        if not os.path.exists(q): print('DANGLING',p,'->',t)
PY
```
### P1-04 hygiene
5. Append to the repo `.gitignore` (keep existing content):
```
# references kit: local toolchains and test artefacts
references/.mermaid/
references/examples/flowapprove_core/.venv/
references/examples/flowapprove_core/.hypothesis/
references/examples/flowapprove_core/mutants/
references/examples/flowapprove_core/.coverage
references/**/__pycache__/
references/**/.pytest_cache/
```
6. Write `references/README.md` (Japanese): purpose of the directory; the canonical content is the kit tree (version 4.0.0 in progress, based on 3.0.0); `archive/` is history; how to run the checks (pointing to `00_README.md` and `tools/`); note that Python ≥ 3.11 is required by `tools/` (they use `tomllib`).
### P0-03 / P1-05 baseline reproduction (no content edits)
7. Toolchain via uv only (never `pip install` into a system interpreter; never write outside the worktree except the effects below):
   - Lint: `cd references && uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check --json /tmp/refkit-baseline/kit_lint_check.json` and `… selftest --json /tmp/refkit-baseline/kit_lint_selftest.json`. Then `python tools/portability_test.py` the same way. Record exit codes.
   - Examples: create the venv with `uv venv --python 3.12 references/examples/flowapprove_core/.venv` and `uv pip install --python <that venv> pytest hypothesis pytest-bdd coverage mutmut`; then, with that venv's `bin` first on PATH, run `python tools/run_examples.py --mutation` from `references/` but with the output redirected to `/tmp/refkit-baseline/example_tests.json` if the script supports an output option; if it only writes `evidence/example_tests.json`, run it, copy the result to `/tmp/refkit-baseline/`, and then `git checkout -- references/evidence/example_tests.json` so the committed baseline evidence stays v3's. State clearly which it was.
   - Mermaid: `mkdir -p references/.mermaid/11 references/.mermaid/12`; `npm install --prefix references/.mermaid/11 mermaid@11` and `npm install --prefix references/.mermaid/12 mermaid@12` (record the exact resolved versions from `npm ls`); `uv pip install --python <venv> playwright` and `python -m playwright install chromium` (this writes the browser under `~/.cache/ms-playwright` — declare it as effect `playwright-chromium` with reverse mapping `rm -rf ~/.cache/ms-playwright/chromium-<build>`); run `python tools/render_mermaid.py --mermaid-dir references/.mermaid/11/node_modules/mermaid` (and 12) with output redirected to `/tmp/refkit-baseline/` if supported, else same checkout-restore approach as above.
   - `pip index versions` / `npm view` are NOT needed here.
8. Compare with v3's shipped evidence and report: versions actually used (gherkin-official, PyYAML, pytest, hypothesis, pytest-bdd, coverage, mutmut, playwright, Chromium, mermaid 11.x/12.x, node, python), check errors/warnings, selftest detected count, portability result, UT/CT pass counts, mutation killed/total, per-figure render success. Note every mismatch with `90_VALIDATION_REPORT.md` and `evidence/*.json` (we already know v3's `kit_lint_check.json` says gherkin-official 29.0.0 while the report says 42.0.1 — finding E-02).
### Commit
9. `git status` must show only: `references/**` (tree + archive + README), `.gitignore`. Nothing under `.mermaid/`, `.venv/`, `mutants/`, `__pycache__` may be tracked. Commit on `feat/references-kit-v4`:
   `feat(references): import documentation kit v3 as the v4 baseline` with a body listing what was imported, what was archived, and that loose duplicates were dropped; end with `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
10. CompactionDB: `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] references/ is the single v3-derived kit tree (v4 in progress); zips live in references/archive with SHA256SUMS; loose duplicates removed"` and paste command + output.

## Forbidden actions
push; pr-create; chezmoi-apply; writes under $HOME other than the declared playwright browser cache; system pip; editing any kit document content (this task is import + measurement only); regenerating and committing new `04_TRACEABILITY.md`/`features/`/`evidence/` (baseline evidence must stay v3's bytes: `sha256sum -c SHA256SUMS.txt` must still pass at commit time); commits on main.

## Validation file must contain verbatim
`sha256sum -c` outputs (kit and archive), the link-scan output, `git status --short` before commit, `git show --stat HEAD`, every tool command with its full stdout/stderr and exit code, `npm ls --prefix … mermaid`, version prints (`python --version`, `uv pip list --python <venv>`), and the contextdb command output.

## Report must contain
the baseline table (tool → version → result), the mismatch list vs v3 report/evidence, effects with reverse mapping, commit hash, `cost:` line.

max_turns=40
