# T26 learning triage

## Candidate

Herdr pane lifecycle changes can be tested without touching the operator's
active workspace by using a unique named session plus a disposable directory.
Set `HERDR_SESSION` for every helper/API command, verify the resolved process
argv with `herdr pane process-info`, detach and reattach through
`herdr session attach`, then stop and delete only that named session.

## Disposition

Candidate only. Do not promote automatically; the existing Herdr E2E learn
entries already require disposable workspace evidence, and this is a narrower
execution technique.

