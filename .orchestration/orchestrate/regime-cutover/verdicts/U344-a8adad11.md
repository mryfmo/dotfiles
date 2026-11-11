## Findings

- P1 (high) [f2 s10] scripts/orchestrator/seat-settings-render.sh:76: Both levers source this helper before its self-check; injected shell code runs outside the sandbox even when the pin later rejects the file.
- P1 (medium) [f1 s10] scripts/orchestrator/hcom-seat:3414: The launch hashes acp-broker and then executes its mutable pathname, allowing a replacement between those steps to run unpinned code outside the sandbox.
- P2 (high) [f1 s5] scripts/orchestrator/hcom-seat:3416: A Unix socket exists after bind but before listen; checking only -S can start dsh before the broker accepts connections.
- P2 (high) [f10 s3] tests/unit/test_hcom_seat_dsh.py:806: The new broker lifecycle test never injects a failed pin read, hash, or abnormal stop status, leaving those safety decisions without the required failure-injection test.
- P2 (high) [f10 s3] tests/unit/test_acp_broker.py:2432: The cited producer-injection test never fails seat_settings_rows_json or seat_settings_json, so it does not test the new renderer failure paths.
- P2 (high) [f10 s3] scripts/orchestrator/README.md:151: The PR threat table uses different required column names, lacks rows for several changed paths, and marks the broker-pin risk closed without a failing test selector.

## Reproduced

- A temporary altered copy of seat-settings-render.sh printed INJECTED_BEFORE_PIN before exiting 2 on its SHA-256 mismatch; the repository was unchanged.
- test_the_levers_install_byte_identical_and_pinned passed.
- bash -n, shellcheck -x, and git diff --check passed for the changed shell files.
- Focused router tests could not exercise the launch: the fixture's /usr/bin/python3 failed through the host's broken Xcode shim.
- The shared-writer integration test could not complete: Unix socket bind in the permitted scratch directory returned EPERM.
- Offline generate-agent-configs.py --check could not run because PyYAML was unavailable in the permitted cache.

## Notes

The checkout remained clean. Integration-test failures above reflect this audit environment, not additional code findings.

Blocking: 2
Filed: 1
Verdict: incorrect
