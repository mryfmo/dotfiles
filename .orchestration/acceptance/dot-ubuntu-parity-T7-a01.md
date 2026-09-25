# dot-ubuntu-parity-T7-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot
evidence:
  - all 4 failures reproduced verbatim before fixing; final targeted bats runs all ok (validation lines 168-183)
  - zed test failure correctly re-diagnosed (unmocked uname + real zed.sh mkdir/mv ordering bug), install script untouched per forbidden_actions
  - scope: tests only + artifacts
follow_up: T8 filed for the real zed.sh fresh-HOME bug (mv before mkdir -p)
cost: n/a
