# refkit-P1 acceptance record

status: accepted (2026-09-23T09:4xZ)
reviewer: claude-remediation-dot (orchestrator, adversarial review)

## Verified independently
- Commit d3281de: 66 files = 57 kit files + SHA256SUMS + 4 zips + archive/{README,SHA256SUMS} + references/README.md + .gitignore. `git ls-files` contains no .venv/.mermaid/__pycache__/mutants. `sha256sum -c` passes for the kit (58 lines) and for archive/ (4/4).
- No loose duplicates remain; top-level .md files are the 8 v3 files + README.md. Link scan pasted: zero DANGLING.
- Reproduced evidence (/tmp/refkit-baseline/example_tests.json) compared field-by-field with the shipped evidence: identical except timestamps/durations/hashes. The "44.4% / 88.4%" branch figures are the shipped package-level values (domain.py 100%, service.py 0% under UT), not a regression.
- E-02 root cause confirmed: `pytest-bdd 8.1.0` requires `gherkin-official>=29,<30`, so a venv containing pytest-bdd resolves 29.0.0; a standalone install resolves 42.0.1. The shipped kit_lint_check.json was produced in the former; the prose claims the latter. Recorded for P8-03/P9.
- Effects: playwright-chromium declared with a concrete reverse mapping.

## Notes for later tasks
- `kit_lint check` now counts 31 documents because `references/README.md` matches `other = ["*.md"]`; acceptable, README passed lint. P2-B should decide whether READMEs belong in `other` or are excluded explicitly.
- Mermaid 11.x resolved to 11.17.2 (unpinned install) — P9 must pin the versions it records.

cost: n/a (worker reported n/a)
