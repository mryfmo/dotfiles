## Findings

- P2 (high) [f2 s4] scripts/orchestrator/hcom-seat:3482: A TERM after broker_copy_dir is set but before broker_pid is assigned makes the signal trap skip copy cleanup; the launch exits with the private broker copy left behind.
- P2 (high) [f10 s3] tests/unit/test_hcom_seat_dsh.py:866: The new copy and pin safety reads in broker_copy_make and renderer_source lack failure-injection tests for failed stat, copy and pin reads.
- P2 (high) [f10 s2] home/dot_local/bin/common/executable_hcom-seat:1: The PR threat table groups multiple changed executable paths into one row, contrary to its required one-row-per-changed-path coverage.
- P3 (high) [f10 s2] scripts/orchestrator/README.md:151: The threat table marks the README prose risk closed using only a Prettier check, which cannot fail when the launch claim is factually wrong.

## Reproduced

- A direct run of the head's foreground_signal trap with broker_copy_dir set and broker_pid empty exited on TERM and left the copy directory present.
- bash -n on the three changed shell sources and git diff --check both exited 0.
- Python byte comparison and SHA-256 checks found the hcom-seat, acp-broker and renderer installed copies identical to their sources and matching their manifest pins.
- Focused unit tests could not reach their assertions in this audit sandbox: the host's git or Python shims require a missing xcrun, and the broker test's Unix socket bind returned EPERM.
- git status --short showed a clean head a65bc8ed76a1631d9c9fe53f070b3d01d1c68954.

## Notes

The changed source and PR contract were assessable despite the local test environment limits. No P0 or P1 finding reaches weight 10.

Blocking: 0
Filed: 1
Verdict: correct
