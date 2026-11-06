## Findings

- none

## Reproduced

- Homebrew Git confirmed the exact head, clean tree, three-file diff, and passing diff --check; the system Git launcher was unavailable.
- python3 -B -m unittest tests.unit.test_dsh_profile: all 10 tests passed.
- python3 -B -m unittest tests.unit.test_scratch_git tests.unit.test_dsh_hook_coverage: all 11 tests passed.
- Combined four-module run: 143 tests, 60 failure records, one skip. Follow-up isolated 59 failures in unchanged project-map hook tests involving denied Bash temporary files, and one unchanged test requiring the absent origin/main ref.
- In-memory regression checks: the new test passed on head and rejected the baseline, either row's removal, and either row's re-enabling.
- Base/head generator comparison across 100 outputs: only cordis.patch.yml changed; both generated thak files matched the renderer.
- Whole-render check using the Chezmoi fixture reported 15 stale outputs; its sorted mappings prevent faithful reproduction of make render-check without PyYAML.
- Ruff passed for both changed Python files and all 134 tracked Python files with caching disabled; the initial cached attempt was denied.
- Comparison lint passed for the renderer. Including the test module exposed an identical pre-existing R4 assertion at baseline line 142 and head line 148.

## Notes

No changeset findings: both API-key web rows use the existing disable form, the generator and artifact agree, and the regression test detects removal or re-enabling. The threat table covers the changed paths and controls. Installed DSH composition and CI claims could not be independently verified within this sandbox.

Blocking: 0
Filed: 0
Verdict: correct
