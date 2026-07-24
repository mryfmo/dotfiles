# T22 Learning Triage

## Candidate

- Modify-script health checks should use semantic comparison for structured
  formats only when the target is explicitly identified as structured; keep
  byte comparison for text/TOML paths whose modifier defines exact output.
- For externally rewritten hook arrays, retain semantically equal current
  entries in their current order and append only missing managed entries. This
  preserves writer serialization while keeping missing-entry drift detectable.

## Evidence

- Herdr reordered SessionStart entries and JSON object keys without changing
  values.
- Focused tests failed before the hook merge and JSON comparison changes.
- 184 unit tests and two live update/doctor cycles passed afterward.
- A different model value still failed the semantic doctor check.

## Decision

Reusable and validated, but not promoted by this worker. The orchestrator may
merge these rules into modify-script guidance if they are not already covered.

## After-acceptance note

The T21 parity guard assumed the feature content was still present as
uncommitted changes in main. T22 restored main to its clean pre-feature state
after the live E2E, so an identical-content guard against merged
`origin/main` cannot pass without a different synchronization precondition.
No reusable rule was promoted by this worker.

The revised instruction used the appropriate clean-tree precondition and an
`--ff-only` merge. This completed safely and confirmed the distinction above.
