# T16 learning triage

## Candidate reusable rule

Herdr mutation commands such as `pane rename` emit JSON on stdout. A shell
function used in command substitution must redirect incidental mutation output
and reserve stdout for its documented return value; mocks should emit the real
JSON shape so output-channel pollution is testable.

`herdr pane list --workspace` is workspace-scoped and may include multiple
tabs, while `herdr pane layout --pane ID` is tab-scoped. Any attach-mode pane
accounting must first derive the current pane's `tab_id` and filter the
workspace list to that tab; otherwise unrelated second-tab panes can
incorrectly trigger ambiguity refusal.

Herdr visual pane order can be read from
`result.layout.panes[].rect.x`; validate unique numeric x-coordinates before
sorting. For a known three-pane set, selection-order repair needs at most two
`pane swap --source-pane ID --target-pane ID` calls and is naturally
idempotent when the first two positions already match.

## Validation

- Confirmed against the live read-only `herdr pane layout` JSON shape.
- Covered by fake-CLI unit tests for wrong, correct, ambiguous, multi-tab, and
  rename-stdout-pollution cases.
- No promotion performed; promotion decisions are outside this worker task.

## Plan impact

Future Herdr pane-order plans/tests should model layout JSON with
`result.layout.panes[].rect.x` and reject missing, nonnumeric, duplicate, or
unmanaged same-tab pane mappings before mutation. Workspace pane-list fixtures
must include `tab_id` and at least one multi-tab regression case.
