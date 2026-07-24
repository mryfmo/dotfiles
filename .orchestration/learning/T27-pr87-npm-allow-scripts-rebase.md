# T27 learning triage

## Decision

No new reusable learn file.

## Rationale

The scoped npm allow-scripts requirement is already captured in the validated learn record `20260723_082118_learn.md`. T27 confirmed that a stale PR can partially overlap later main changes; the correct rebase resolution is to retain main's implementation, discard duplicate insertions, and preserve only still-missing behavior plus regression coverage.

No skill or rule promotion was performed.
