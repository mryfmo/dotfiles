# refkit-P1 learning triage

[memory:decision] Validated reusable fact: `references/tools/render_mermaid.py` supports
an `--output` flag (default `evidence/mermaid_render.json`), so baseline reproduction of
Mermaid rendering can be redirected cleanly without ever touching the tracked evidence
file. `references/tools/run_examples.py` has **no** such flag — it always writes
`evidence/example_tests.json` under the kit root — so reproducing example-test/mutation
results against an already-committed kit tree requires the copy-then-`git checkout --`
(or, pre-commit, zip-reextraction) restore dance described in the task file. Future
baseline-reproduction tasks against this kit should budget for that asymmetry.

[memory:decision] Validated reusable fact (root cause for finding E-02): the kit's
`gherkin-official` version discrepancy between prose reports (42.0.1) and shipped
`evidence/kit_lint_check.json` (29.0.0) reproduces deterministically from environment
composition, not evidence corruption — installing `gherkin-official` directly resolves
current PyPI latest (42.0.1), while installing it as `pytest-bdd`'s transitive dependency
resolves an older, pytest-bdd-constrained release (29.0.0) that exactly matches the
shipped evidence number. Confirmed by installing both ways in this task.

Disposition: recorded in CompactionDB (see `.orchestration/reports/refkit-P1.md`). No
skill promotion performed — these are kit-specific facts, not a new reusable procedure
for this repository.
