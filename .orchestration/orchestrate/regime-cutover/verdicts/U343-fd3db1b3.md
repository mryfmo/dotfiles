## Findings

- P1 (high) [f3 s7] scripts/orchestrator/acp-broker:1581: TERM after slot creation but before the reaper forks kills the handler and strands the slot; reproduced during the clone.
- P1 (high) [f2 s8] scripts/orchestrator/acp-broker:1657: A record-helper failure after rename leaves a visible record, so the handler starts omp without a reaper and strands its slot; reproduced with injected fsync failure.
- P1 (medium) [f2 s10] scripts/orchestrator/acp-broker:1264: A header name can select another seat's writable state directory; a hard-linked launch log passes the symlink check and makes the unsandboxed broker append to a protected file.
- P2 (high) [f2 s5] scripts/orchestrator/acp-seat:234: After final-record rename, an fsync failure makes the handler exit 2 while the client trusts the existing status=0 record and returns 0; reproduced.
- P2 (high) [f2 s4] tests/unit/test_acp_broker.py:831: The Threat table marks termination cleanup closed using this test, but it signals only after the reaper starts and misses the reproduced pre-reaper slot leak.
- P2 (high) [f2 s4] tests/unit/test_acp_broker.py:1154: The helper-failure test injects a pin mismatch but never a post-rename failure, so its Threat table evidence does not close the producer-status risk.
- P2 (medium) [f2 s4] scripts/orchestrator/acp-broker:1156: The header-field read still discards its exit status and cannot distinguish a failed here-string read from malformed input; earlier carried P2 row 1156 remains.
- P3 (high) [f1 s3] scripts/orchestrator/acp-broker:1028: A failed record unlink is logged but the cleanup returns success, allowing broker exit 0 with records remaining; earlier carried P3 row 1028 remains.
- P3 (high) [f1 s2] scripts/orchestrator/acp-broker:26: The header says the Router can connect to the socket, while this head renders an empty allowUnixSockets list; earlier carried P3 row 26 remains.

## Reproduced

- git verified head fd3db1b3, the 18-path changeset, and a clean worktree; git diff --check passed.
- bash -n passed for acp-broker and hcom-seat; five deployed copies matched their sources, five manifest pins matched, and five Python files parsed.
- tests.unit.test_acp_record_place: 13 tests passed, one skipped.
- Direct broker connection against scratch files: a hard link at the selected launch-log path caused the broker to append to its separate target and exit 0.
- Direct broker connection with a delayed clone: TERM after slot creation returned -15 and left the acp slot present.
- Scratch-copy failure injection after running-record rename: the broker started omp, exited 2, and left the acp slot present.
- Scratch-copy failure injection after final-record rename: the handler exited 2, but the record said status=0 and acp-seat.read_record returned 0.
- The focused socket integration test could not start its listener because the audit sandbox denied Unix-socket bind with EPERM.

## Notes

The direct reproductions used scratch fixtures and copies; no repository files were edited. The audit sandbox prevented a full socket test and a real srt run.

Blocking: 3
Filed: 5
Verdict: incorrect
