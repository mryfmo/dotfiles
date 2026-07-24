# T23 learning triage

## Candidate

- For Herdr-hosted TUI workers, send wake text and Enter atomically with
  `herdr pane run`; separate text and Enter calls race the composer.
- Treat messages.db `read_at` as the delivery oracle, and restart a pane only
  after an atomic wake remains verifiably undelivered.

## Evidence

- The task records three consecutive failures with separate text/Enter and
  first-attempt success with `pane run`.
- The shared guidance now states the atomic command and verification oracle in
  both the playbook and Pitfalls sections.
- Generator, 184 unit tests, asset validation, Crit-data review, and CI passed.

## Decision

Reusable and validated, but not promoted by this worker. The task itself lands
the rule in the canonical shared orchestration skill.

## After acceptance

The canonical rule was merged and local main synchronized with a clean-tree
`--ff-only` update. No additional learning candidate was promoted.
