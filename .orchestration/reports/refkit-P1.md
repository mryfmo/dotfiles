# refkit-P1 report

Status: ready_for_review

## Result

Replaced the flat, mixed-generation `references/` layout with the single v3 kit tree
(imported from `PRD_ADR_BDD_TEST_Kit_v3_20260919.zip`), archived all 4 distributed zips
under `references/archive/` with their own `SHA256SUMS.txt` and a Japanese provenance
README, dropped the 30 loose duplicate `.md` files, added `references/README.md` and
`.gitignore` hygiene, and reproduced the kit's own validation on this machine
(kit_lint check + selftest, portability_test, the flowapprove_core example tests +
mutation testing, Mermaid rendering under mermaid 11.x/12.x) without touching any
committed evidence bytes.

## Baseline table (tool → version → result)

| Tool                                                     | Version used here                                                                            | Result                                                                                                                                           |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Python (kit_lint / portability_test)                     | 3.12.3 (via `uv run --python 3.12`)                                                          | —                                                                                                                                                |
| gherkin-official (kit_lint direct install)               | **42.0.1**                                                                                   | `kit_lint.py check`: passed                                                                                                                      |
| gherkin-official (pytest-bdd's dependency, example venv) | **29.0.0**                                                                                   | (see mismatch below)                                                                                                                             |
| PyYAML                                                   | 6.0.3                                                                                        | —                                                                                                                                                |
| `kit_lint.py check`                                      | —                                                                                            | passed, 0 errors/0 warnings; stats match 90_VALIDATION_REPORT.md exactly (FR 28, NFR 9, rules 23, SCN 41, expanded 68, figures 20, documents 31) |
| `kit_lint.py selftest`                                   | —                                                                                            | passed; baseline passed; **30/30** mutations detected                                                                                            |
| `portability_test.py`                                    | —                                                                                            | passed; only warning **W102** (Mermaid evidence absent, expected — portability test never runs the Mermaid renderer)                             |
| Python (example venv)                                    | 3.12.3                                                                                       | —                                                                                                                                                |
| pytest                                                   | 9.1.1                                                                                        | UT 125/125, CT 29/29                                                                                                                             |
| hypothesis                                               | 6.168.0                                                                                      | —                                                                                                                                                |
| pytest-bdd                                               | 8.1.0                                                                                        | —                                                                                                                                                |
| coverage                                                 | 7.16.1                                                                                       | UT branch_coverage_percent 44.4%, CT 88.4%                                                                                                       |
| mutmut                                                   | 3.8.0                                                                                        | 68 mutants, **67 killed**, 1 survivor (`flowapprove.domain.x_next_state__mutmut_1`), score 98.5%                                                 |
| node                                                     | v26.9.0                                                                                      | —                                                                                                                                                |
| mermaid                                                  | 11.17.2 and 12.0.0 (installed via unpinned `mermaid@11`/`mermaid@12`, per task instructions) | 20/20 diagrams ok for both, negative-diagram rejection true                                                                                      |
| playwright                                               | 1.63.0                                                                                       | —                                                                                                                                                |
| Chromium (playwright build)                              | 153.0.8010.12 (playwright chromium v1243)                                                    | used for both mermaid runs, no failures                                                                                                          |

## Mismatch list vs `90_VALIDATION_REPORT.md` / `evidence/*.json`

- **E-02 gherkin-official version, root cause identified.** `01_ADVERSARIAL_REVIEW.md:10`,
  `90_VALIDATION_REPORT.md:10,45`, `02_RESEARCH_AND_DECISIONS.md` §S09 all state
  "gherkin-official 42.0.1", but the kit's own shipped `evidence/kit_lint_check.json`
  records `"gherkin-official": "29.0.0"`. Reproducing both code paths on this machine
  explains the split: installing `gherkin-official` directly (as `kit_lint.py check` does
  here, via `uv run --with gherkin-official`) resolves the current PyPI release, **42.0.1**.
  Installing `pytest-bdd` (as the example-test venv does, for `run_examples.py`) pulls
  `gherkin-official` as a transitive dependency, which resolves to an older, `pytest-bdd`-
  constrained release, **29.0.0** — exactly the shipped evidence's number. So the kit's own
  `evidence/kit_lint_check.json` appears to have been produced in an environment that also
  had `pytest-bdd` (or an equivalent constraint) installed alongside `kit_lint.py`'s direct
  dependencies, while the prose reports describe a different, unconstrained environment.
  Both numbers are real observations from this machine, not a stale/corrupted evidence
  file; the discrepancy is an environment-provenance gap in the kit itself (per finding
  E-02), not something this import task can or should fix (`edit-kit-content` is forbidden).
- **Mermaid version drift (expected, not a defect).** The kit's shipped
  `evidence/mermaid_render.json` was produced with mermaid `11.14.0`/`12.0.0`; this task's
  step explicitly says to `npm install mermaid@11` / `mermaid@12` (unpinned), which
  resolved to the current `11.17.2`/`12.0.0` on this machine. Render results are identical
  (20/20 ok, both versions) despite the 11.x patch drift.
- **No other mismatches found.** `kit_lint.py check` stats, `selftest` (30/30, same
  mutation list), `portability_test.py` (status/warnings/stats), and
  `run_examples.py --mutation` (UT 125/125, CT 29/29, mutation 68/67/98.5%, same single
  survivor) all reproduce byte-for-byte identical results to the kit's own shipped
  evidence and `90_VALIDATION_REPORT.md`'s claimed figures.

## Effects and reverse mapping

`effects=playwright-chromium`: `python -m playwright install chromium` (run from the
`examples/flowapprove_core/.venv` interpreter) downloaded Chromium build 1243
(`153.0.8010.12`), FFmpeg build 1011, and Chrome Headless Shell build 1243 under
`~/.cache/ms-playwright/`. Reverse mapping:

```
rm -rf ~/.cache/ms-playwright/chromium-1243 ~/.cache/ms-playwright/chromium_headless_shell-1243 ~/.cache/ms-playwright/ffmpeg-1011
```

No other effect outside the worktree was produced; the example venv
(`references/examples/flowapprove_core/.venv`) and the two `.mermaid/` npm installs are
inside the worktree and gitignored (never committed).

## Evidence-preservation note

`tools/run_examples.py` has no output-redirect option — it always writes
`evidence/example_tests.json` under the kit root. Since `references/` was not yet
committed or staged when this ran, `git checkout --` had nothing to restore from; instead
the mutated file was copied to `/tmp/refkit-baseline/example_tests.json` and
`references/evidence/example_tests.json` was overwritten with the original bytes
re-extracted from `references/archive/PRD_ADR_BDD_TEST_Kit_v3_20260919.zip` (hash verified
against `SHA256SUMS.txt`). `tools/render_mermaid.py` does support `--output`, so its run
was pointed at `/tmp/refkit-baseline/mermaid_render.json` directly and the tracked
`evidence/mermaid_render.json` was never touched (hash verified unchanged before and after).
`sha256sum -c references/SHA256SUMS.txt` passes for all 58 files at commit time.

## Commit

`d3281dee4e5329fe5c95b162f7c9f4a92b3d3c5b` on `feat/references-kit-v4`:
`feat(references): import documentation kit v3 as the v4 baseline tree` (66 files changed,
8997 insertions).

## CompactionDB

`[memory:decision] references/ is the single v3-derived kit tree (v4 in progress); zips
live in references/archive with SHA256SUMS; loose duplicates removed`

Memory ID: `746ce0e8-4f37-475e-b548-fc3bb4fe724f`

Exact command and output in `.orchestration/validation/refkit-P1.md`.

cost: n/a
