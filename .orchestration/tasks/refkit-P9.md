# AGMSG-TASK refkit-P9: 生成物と証跡の再生成、90 の数値記入、SHA256SUMS

Covers plan tasks P9-01 … P9-05 (第 2 部 §11). Prerequisite: everything through P8 merged on your branch; the orchestrator gives the base commit. This is the only task allowed to regenerate `04_TRACEABILITY.md`, `features/`, `evidence/*.json` and `SHA256SUMS.txt`.

## Toolchain (record every version in the validation file)
- Lint venv: `uv run --python 3.12 --with gherkin-official --with PyYAML` (records gherkin-official 42.x).
- Example venv: `references/examples/flowapprove_core/.venv` (pytest, hypothesis, pytest-bdd, coverage, mutmut, playwright). Note its gherkin-official is pinned by pytest-bdd (29.x) — record both and say which command ran in which environment.
- Mermaid: `references/.mermaid/11` and `.mermaid/12`; pin the versions you record (`npm ls --prefix … mermaid`); if 11.x drifted from the last run, re-install the exact version you record.

## Order (each step's full output goes verbatim into the validation file)
1. `kit_lint.py extract` (markdown mode → marked `.feature` files).
2. `kit_lint.py trace` → `04_TRACEABILITY.md`.
3. `render_mermaid.py --mermaid-dir <11> --output evidence/mermaid_render.json` then `--mermaid-dir <12>` (or however P2-C merged the two runs) — sandbox ON.
4. `run_examples.py --mutation` in the example venv → `evidence/example_tests.json` (durations, true branch coverage, mutation).
5. `kit_lint.py check --json evidence/kit_lint_check.json` → 0 errors / 0 warnings required. If anything fails, fix the *cause* in the owning artefact only if it is a generated artefact; otherwise stop, report `blocked` with the error, do not edit documents.
6. `kit_lint.py selftest --json evidence/kit_lint_selftest.json` → all detected, `uncovered_codes: []`.
7. `portability_test.py` → passed (with mermaid rendered, since playwright is available in the example venv — run it with that interpreter).
8. Fill `90_VALIDATION_REPORT.md` `{{P9}}` placeholders and the 実行結果 tables in UT/CT_SAMPLE from the evidence (numbers only; every number must appear in your validation output). BDD_SAMPLE `last_run`/`automation` per the evidence.
9. `SHA256SUMS.txt` regenerated over every file under `references/` except `archive/`, `.mermaid/`, `.venv/`, caches, and `SHA256SUMS.txt` itself; `sha256sum -c` passes.
10. Commit: `chore(references): regenerate traceability, features and evidence for kit v4`.

## Scope (allowed_files)
`references/04_TRACEABILITY.md`, `references/features/**`, `references/evidence/**`, `references/SHA256SUMS.txt`, `references/90_VALIDATION_REPORT.md`, `references/ut/UT_SAMPLE.md`, `references/ct/CT_SAMPLE.md`, `references/bdd/BDD_SAMPLE.md` (front matter `automation`/`last_run`/7 章 実行結果 only), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P9.md`.

## Forbidden
push; pr-create; editing any other document or tool (report blockers instead); `--allow-no-sandbox`; inventing numbers.

max_turns=40
