# dot-ubuntu-parity-T11-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot (adversarial re-derivation)
evidence:
  - single commit b5f49a4; scope exactly 4 non-artifact files
  - independent re-run: format clean / validate ok / unit-test 383 OK (7 new; 65 pre-existing
    herdr-agents tests unchanged and passing = default-kind byte-identical behavior proven)
  - trust-dialog auto-accept, kind-scoped require_command, deprecated-alias precedence all test-covered
  - deliberate non-changes (generic attach helpers, both-kind bootstrap identity loop) reviewed and endorsed
cost: n/a
