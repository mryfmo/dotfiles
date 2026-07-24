# T18 learning triage

## Candidate reusable learning

Herdr can represent the same three-column visual layout with either nested
split topology:

- `((left | middle) | right)`
- `(left | (middle | right))`

`pane resize --amount` moves the selected boundary by a fraction of that
boundary's containing split width, not always the full tab width. Safe repair
therefore needs to validate the split rectangles, fix the outer boundary
first, re-read layout geometry, and then fix the inner boundary. Integer cell
rounding requires a small final tolerance.

Changing the files split ratio is insufficient when the source pane is only
half of an existing two-pane workspace. The post-split three-pane geometry
must also pass through the same topology-aware repair; otherwise a 50/50
workspace becomes approximately 50/33/17.

## Validation

- Verified on Herdr 0.7.3 in disposable workspaces.
- Covered by fake-CLI unit tests for both nested topologies and refusal cases.
- Confirmed through a real persisted `86/43/43` to `57/57/58` attach repair.

## Promotion

No skill or durable project learn was promoted. The orchestration task asks
only for learning triage; the orchestrator owns promotion decisions.
