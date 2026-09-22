# dot-ubuntu-parity-T6-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot
evidence:
  - 7813ebc removes exactly the ineffective templated block; unit-test 376 OK verbatim in validation
  - CompactionDB decision (ignore-beats-remove semantics) registered with verbatim command
  - empirically proven on spark-9e8d: entry was live during a successful apply and files persisted
cost: n/a
