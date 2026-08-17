# T83 Learning

## Triage

- A graph's stored commit hash may predate a later graph-only corrective commit. For incremental scope, use the latest commit that materially changed graph content, while still advancing graph/meta/fingerprint hashes to current HEAD.
- When a feature is introduced and removed between graph-content commits, the net baseline diff does not expose its deleted paths. Verify removal against the deletion commit's own inventory.
- The bundled fingerprint builder may reorder the full store. LOAD-PATCH-SAVE keeps the incremental diff bounded while retaining authoritative fingerprints for changed files.

## Decision

No new durable project memory was added. These are task-local applications of the existing incremental graph and fingerprint-preservation rules.

