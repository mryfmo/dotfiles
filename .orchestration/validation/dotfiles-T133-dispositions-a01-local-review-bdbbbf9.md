---
task: dotfiles-T133-dispositions-a01
head: bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3
pr: 419
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T22:13:24Z
finished: 2026-10-18T22:17:35Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Verify test outcomes rather than arbitrary job output — scripts/orchestrator/dispositions.py:151-153
- [P2] Handle passing tests with interleaved diagnostic output — scripts/orchestrator/dispositions.py:152-153
- [P2] Preserve the full selector when identifying a test — scripts/orchestrator/dispositions.py:143-146

```text
The test-refutation verifier accepts fabricated or mismatched evidence and rejects some genuinely passing tests. Although PR #419's head CI passed 1,215 Python tests, direct reproductions confirmed these uncovered cases.

Full review comments:

- [P1] Verify test outcomes rather than arbitrary job output — scripts/orchestrator/dispositions.py:151-153
  PR-controlled code can print `test_disabled (test_proof.Proof.test_disabled) ... ok` and satisfy this regex even when that test is skipped. A green unittest run with a separate test printing that line reproduced `refutation.ok: true` for the skipped test. Under `--require-refutation`, an unexecuted test can therefore dismiss a finding. Use runner-controlled results and reject skipped, failed, or absent selections. The proposal-only test cited by the script's `closed` threat-table row does not close this boundary ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve the full selector when identifying a test — scripts/orchestrator/dispositions.py:143-146
  The path selector discards every directory component, and the dotted selector similarly discards parent modules. Consequently, `tests/missing/test_stub.py::test_pass` is accepted from a passing `test_stub.T.test_pass` log entry even when the selected file does not exist; this was reproduced directly. Resolve the selector against the accepted head and CI discovery root so evidence cannot identify a different or nonexistent test.

- [P2] Handle passing tests with interleaved diagnostic output — scripts/orchestrator/dispositions.py:152-153
  Unittest writes the test identifier before execution and its result afterward, so test diagnostics can separate them. In the [successful head CI log](https://github.com/mryfmo/dotfiles/actions/runs/39168116318/job/117795274272), `test_unknown_interactive_profile_fails` prints `... ERROR: ...` followed by a separate timestamped `ok`. This regex rejects that genuinely passing test, blocking its refutation when enforcement is enabled. Parse complete runner records or structured results instead of requiring the identifier and `ok` on one line.
The test-refutation verifier accepts fabricated or mismatched evidence and rejects some genuinely passing tests. Although PR #419's head CI passed 1,215 Python tests, direct reproductions confirmed these uncovered cases.

Full review comments:

- [P1] Verify test outcomes rather than arbitrary job output — scripts/orchestrator/dispositions.py:151-153
  PR-controlled code can print `test_disabled (test_proof.Proof.test_disabled) ... ok` and satisfy this regex even when that test is skipped. A green unittest run with a separate test printing that line reproduced `refutation.ok: true` for the skipped test. Under `--require-refutation`, an unexecuted test can therefore dismiss a finding. Use runner-controlled results and reject skipped, failed, or absent selections. The proposal-only test cited by the script's `closed` threat-table row does not close this boundary ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve the full selector when identifying a test — scripts/orchestrator/dispositions.py:143-146
  The path selector discards every directory component, and the dotted selector similarly discards parent modules. Consequently, `tests/missing/test_stub.py::test_pass` is accepted from a passing `test_stub.T.test_pass` log entry even when the selected file does not exist; this was reproduced directly. Resolve the selector against the accepted head and CI discovery root so evidence cannot identify a different or nonexistent test.

- [P2] Handle passing tests with interleaved diagnostic output — scripts/orchestrator/dispositions.py:152-153
  Unittest writes the test identifier before execution and its result afterward, so test diagnostics can separate them. In the [successful head CI log](https://github.com/mryfmo/dotfiles/actions/runs/39168116318/job/117795274272), `test_unknown_interactive_profile_fails` prints `... ERROR: ...` followed by a separate timestamped `ok`. This regex rejects that genuinely passing test, blocking its refutation when enforcement is enabled. Parse complete runner records or structured results instead of requiring the identifier and `ok` on one line.
```
