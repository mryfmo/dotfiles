# refkit-P0-01 learning triage

[memory:decision] Validated reusable fact: `scripts/validate-agent-assets.py` enforces a
_closed_ set of `model_profiles` names (`validate_agent_manifest`, ~line 535) — adding any
new named profile (not just `adh`-style pinned ones) requires updating that check and its
unit-test fixtures (`tests/unit/test_validate_agent_assets.py::write_valid_agent_manifest`)
in the same change, even when a task's `allowed_files` only lists the manifest and
generator outputs. Future "add a model profile" tasks should list the validator and its
tests in `allowed_files` up front to avoid a mid-task scope-confirmation round trip.

Disposition: recorded in CompactionDB (see `.orchestration/reports/refkit-P0-01.md`). No
skill promotion performed — this is a one-line addition to the existing
agent-config-orchestration knowledge, not a new reusable procedure.
