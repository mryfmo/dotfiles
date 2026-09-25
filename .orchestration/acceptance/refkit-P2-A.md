# refkit-P2-A acceptance record

status: accepted (2026-09-23T10:1xZ)
reviewer: claude-remediation-dot (orchestrator, adversarial review)

## Verified independently (orchestrator runs on the committed tree 03a4215 and on a scratch copy)
- `kit_lint.py check` on the tree: passed. `selftest`: passed, 34/34 detected (orchestrator run, JSON in scratchpad).
- Scratch re-derivation of E-01: switched BDD_SAMPLE to `gherkin_source: feature`, appended a line to FEAT-008.feature, ran `extract` → 8×E123, FEAT-008 sha256 unchanged (243d3740a113 before and after). `mirror` then `check` passed. Back in markdown mode with an unmarked FEAT-099.feature: `extract` reports E122 and the file survives; regenerated features carry the marker line.
- Diff review: deletion is restricted to marker-bearing orphans; E121 compares with the marker stripped so v3's shipped features still pass; E018 replaces the ValueError; version guard precedes the `tomllib` import; selftest default now requires exactly one regex match (FIXTURE_AMBIGUOUS otherwise); the three re-anchored mutations remain single-point mutations of the same kind.
- Documentation diffs are limited to the allowed sections; 02_RESEARCH_AND_DECISIONS.md untouched as instructed (proposal for the 判断表 row is in the report → P8-03).

## Notes for later tasks
- Running `extract` in markdown mode now rewrites `features/*.feature` with the marker, which changes FEAT-004.feature bytes and makes E153 (example_tests.json input hash) fire until P9 regenerates the evidence. Expected; P9 must run `extract` before `run_examples.py`.
- Worker reported that its Edit/Write tools trigger a post-write formatter that rewrites whole files (tables, CJK spacing) and broke template↔sample header parity once. Future task files instruct workers to apply edits so that `git diff` contains only the intended hunks (Bash/python writes or a formatter-disabled path) and to inspect `git diff --stat` before committing.

cost: n/a (worker reported n/a)
