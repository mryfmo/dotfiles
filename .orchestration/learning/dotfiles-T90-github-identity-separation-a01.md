# T90 learning

[memory:failure] A shell variable exported in a spawn parent does not reach a Herdr daemon-created tab; verify the driver's tab creation and boot process environment. Codex inherit=core also drops GH_CONFIG_DIR unless explicitly set for tool commands.

[memory:failure] GitHub review IDs order creation, not necessarily submission: pending reviews can be submitted later. Approval state must use submitted_at and exact commit_id, with pagination and dismissal handling.

GitHub required approval limits pre-approval merging, not the identity of the merge actor after approval. HTTPS gh credential helper follows GH_CONFIG_DIR; SSH pushes follow SSH authentication and pushInsteadOf can route away from HTTPS.

Initial focused run overlapped file formatting and produced transient shell parse/test fixture failures; the final full test run uses stable source. Ruff's ambient broader lint configuration is not this repository's format-only policy; validate with --config ruff.toml.

Revise round 1: required approval also blocks PRs authored by the sole intended approver because GitHub rejects self-approval. Credential role separation, approval requirements and server-side merge restrictions must have a coordinated activation order that covers orchestrator-authored boundary PRs. T90b owns that design; T90 operator setup stops after doctor.
