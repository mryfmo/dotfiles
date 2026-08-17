# T83b Learning

## Validated learning

1. A graph-carrying commit is necessarily newer than the hash stored inside its graph. Freshness therefore needs path semantics, not exact equality alone: intervening `.ua/**` and `.orchestration/**` changes do not stale the graph, while any other path does.
2. Incremental node replacement must audit incoming as well as outgoing edges. Pruning incident edges and trusting changed-file analyzers loses relationships sourced by unchanged nodes.
3. Endpoint survival is necessary but not sufficient for restoration: the context diet intentionally removed eight direct script-documentation relationships even though both endpoint nodes remain.

## Apply to

- Future UA incremental merges: compute the complete parent/current semantic edge diff and classify every removed edge before save.
- Future graph freshness checks: use the documented exact-hash-or-graph/evidence-only predicate.

The durable decision was recorded in project memory; no new repository learn-index entry is added because T83b's policy documents and orchestration evidence are the authoritative application points.

