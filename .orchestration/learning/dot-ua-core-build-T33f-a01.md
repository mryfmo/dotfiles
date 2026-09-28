# T33f learning triage

## Candidates

1. A "copy build outputs from another install" provisioning step must check
   that the outputs exist at the source, or build them there. Marketplace
   plugin checkouts are git content and never contain `dist` or
   `node_modules`, so a silent `[ -d src ] || continue` copy loop
   provisions nothing without any warning.
2. To pin an npm-distributed CLI in mise here, use the `npm:` backend
   (`"npm:<pkg>" = "<ver>"` plus a two-line `[[tools."npm:<pkg>"]]` lock
   entry). It needs no per-platform checksums, unlike the aqua entries, so
   the pin can be added without running `mise install`. Check the 7-day
   window with the GitHub releases `published_at`.
3. `update-agent-assets.sh` has a `BASH_SOURCE` guard, so unit tests can
   source it under a restricted PATH and call individual functions with
   fake CLIs. That is a cheap way to test lifecycle functions without
   running the whole updater.

## Promotion

None. These are candidates only.
