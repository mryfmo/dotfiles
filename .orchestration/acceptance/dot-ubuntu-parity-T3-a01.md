# dot-ubuntu-parity-T3-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot (adversarial re-derivation)
evidence:
  - 10 commits bb6e0f3..e7f1e9e (+14a23b7 artifacts) reviewed; diff scope exactly within allowed_files
  - independent re-run: make format clean / validate-agent-assets ok / unit-test 376 OK (skipped=1)
  - B10 checksum double-verified in validation (direct sha256sum == release SHA-256.txt == committed value)
  - B7 .chezmoiremove templated guard verified; B9 units + run_onchange hash-trigger pattern sound
  - B2b stale lock block removed, supply-chain suite green; B0b makes make format green repo-wide
  - CompactionDB decisions caa48801-c710-49c9-916e-8075a992929d, 20114ee0-f0a9-4be1-930d-b1f3fdf8922b registered
notes:
  - extra fixup commit 6df6aa1 (checksum-block count) reviewed and endorsed
  - run_onchange reachability check may skip on a degraded user manager — verify at apply phase (list-timers)
cost: n/a
