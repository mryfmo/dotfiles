# T33j learning triage

## Candidates

1. Before narrowing a shared wait helper, grep every caller for the
   condition the helper was written for. `process-info` says "shell is
   foreground" both before and after zsh enables its line editor. Only the
   drawn prompt separates those two states, so the new-pane callers still
   need it, while a reused pane does not.
2. Do not delegate a "last line" check to a matcher whose per-line or
   per-snapshot semantics you cannot observe. Read the snapshot and test
   the last non-blank line locally.
3. A fake that answers every `wait-output` with success hides snapshot-source
   bugs. Give the fake per-source content (a stale `visible`, a real
   `recent-unwrapped`), so tests can tell which snapshot the code trusts.

## Promotion

None. These are candidates only; promotion is the orchestrator's call.
