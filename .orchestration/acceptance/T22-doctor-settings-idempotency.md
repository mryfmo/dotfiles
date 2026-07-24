# Acceptance: T22 doctor settings idempotency

Status: accepted round 1 (2026-07-23) — next_action=merge sent

## Adversarial verification (orchestrator, independently re-derived)

- Scope integrity: branch diff touches exactly the 4 allowed files
  (modify_private_settings.json, check-agent-runtime.py, 2 test files).
- Drift detection preserved: `same_modified(json_target=True)` compares
  `json.loads(modify(current)) == json.loads(current)` — dict key order is
  tolerated (Python dict equality), hook ARRAY order and managed values remain
  significant; `test_json_modifier_rejects_real_value_drift` and
  `test_content_drift_still_fails` pin this. Codex/TOML targets stay byte-exact.
- Order preservation: `test_current_session_start_order_is_preserved`,
  `test_managed_hook_object_key_order_is_preserved`,
  `test_reordered_but_equal_current_is_byte_identical`, plus retained
  `test_merge_is_idempotent` / byte-identity property.
- CI: `gh pr checks 89` all pass, 1 conditional skip (nix), 0 fail. 184 unit
  tests in worker log; suite re-run by CI.
- Live evidence consistency: worker's two `make update` + doctor cycles ran the
  BRANCH doctor/modify from its worktree against live $HOME (main's unfixed
  doctor still shows the settings error, as expected pre-merge) — coherent.
- Final proof deferred to post-merge: orchestrator re-runs
  `make update && ./scripts/check-agent-runtime.py` twice on merged main.

## Final (round 2)

- Revised sync executed: ff-only merge c1bfdbd -> 92faa35; tracked tree clean; T22 worktree/branch removed.
- Orchestrator independent proof: own `make update` then doctor => only the known pre-existing agmsg/db-flue-pi error remains; Claude settings idempotency confirmed fixed end-to-end.
- T22 accepted and closed 2026-07-23.
