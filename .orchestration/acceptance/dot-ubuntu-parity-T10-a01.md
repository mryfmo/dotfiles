# dot-ubuntu-parity-T10-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot (adversarial re-derivation)
evidence:
  - 4 commits reviewed; scope within allowed_files (15 non-artifact files)
  - independent re-run: format clean / validate ok / unit-test 376 OK ×2 consecutive
    (one transient FAILED(1) observed once immediately after RESULT, not reproduced in 2 reruns — noted, watch in CI)
  - worker independently caught and fixed a correctness bug in MY task spec: sprig default() cannot
    distinguish explicit false from unset (bool zero value) — hasKey-or form verified with full
    execute-template matrix. Task-spec error acknowledged orchestrator-side.
  - worker also caught doctor fixture regression (optional-warning count) during its own validation
  - RESULT delivered via the corrected Monitor+watch.sh path (design-conformant delivery verified)
conduct_note:
  - msg35 read_at set 9s after send by an unidentified reader (no inbox.sh claude-deep-dot in worker's
    top-level transcript; fork-level suspected, unproven). watch.sh delivery verified read-only/high-water
    — reads by third parties cannot cause loss. read_at for claude-deep-dot treated as unreliable.
cost: n/a
