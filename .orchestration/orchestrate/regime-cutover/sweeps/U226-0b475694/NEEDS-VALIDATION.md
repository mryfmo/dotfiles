# Needs validation: dotfiles at 0b475694e95f2061dffa73563c7036260dfa11d6

No unresolved record exists in this run. No lead in the scoped hunt over the U226 diff depended on a fact outside the source or outside local observation.

One fact the hunt relied on comes from outside the target, and was read rather than assumed: how upstream's build consumes `DSH_CLIENT_COMMIT_HASH`. It was read from the operator's already-installed upstream tree (`scripts/client-build-environment.ts:52-63` there). It settled the question without a lead: the value is re-validated as hex and kept as 7 characters of public build metadata.

The one gap outside the diff, the build's inherited environment, is recorded as an `out_of_scope` ledger unit and a hardening note in `REPORT.md`. It is not a needs-validation lead.
