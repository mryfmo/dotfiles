# refkit-P2-B acceptance record

status: accepted (2026-09-23T11:3xZ) after one narrow revise; final commit 8520649
reviewer: claude-remediation-dot

## Verified independently (ef7f611)
- `check`: passed, 0/0. `selftest`: 104/104 detected, `uncovered_codes: []`, no skipped on this tree. `portability_test.py`: passed (mermaid skipped in the orchestrator's interpreter, recorded explicitly).
- ID allow-list + `[ids] prefix`, multi-PRD with cross-doc E030, E150/E151 over the UAT union, E155 unconditional (BDD_TEMPLATE/BDD_SAMPLE gained `evidence:`), structured 実行結果 tables in the four templates/samples with values matching `evidence/example_tests.json` keys (`ut.*`, `ct.*`, `mutation.{total→mutants,killed,score_percent}` all resolve).
- `evidence/portability_test.json` regeneration accepted: it is the script's own output, and the task required running the rewritten script.
- Document diffs are limited to the intended hunks (no formatter noise); the worker caught and undid one Edit-tool reformat before committing.

## Refuted (blocking, narrow)
- **E158 silently skips unresolvable keys.** `kit_lint.py` ~line 486: `have = evidence_value(key); if have is None: continue`. Orchestrator scratch test: changing UT_SAMPLE's row to `| UT合格 | 999 | ut.pased |` still yields `check: passed`. A typo or a wrong section in 証跡のキー therefore turns a verified number into an unverified one without any signal — the same class of hole E158 was rewritten to close.

## Required revision
1. When the document's `evidence` resolves to the configured evidence file and its `doc_type` level exists in that file, an unresolvable 証跡のキー must be an error (pick an unused code, e.g. E159, message naming the row and key). Rows may be skipped only when the document's level is absent from the evidence (ST/UAT `not_run` case) — keep that path explicit.
2. Add a selftest mutation for the new code (typo'd key) and keep `uncovered_codes: []`.
3. Update `tools/README.md` (table/key section) accordingly. Amend/append commit on `feat/references-kit-v4`; re-send RESULT with the scratch demonstration (`ut.pased` → new error).

cost: n/a

## Round 2: accepted
- 8520649 adds E159 (unresolvable 証跡のキー when the document's level exists in the evidence) plus a selftest mutation. Orchestrator scratch test: `ut.pased` now fails with `E159 ut/UT_SAMPLE.md: UT合格: 証跡のキー 'ut.pased' を証跡から解決できない`; tree check still passes; selftest 105/105, uncovered [].
