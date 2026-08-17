# T83b Report

Status: `ready_for_review`

cost: n/a

`effects=none`

T83b corrects the two PR #138 P2 findings without a full re-analysis or rule regrowth.

## Result

- Replaced one freshness sentence in each Claude/Codex policy document: exact meta/HEAD equality remains current, and a differing hash also remains current when every intervening path is under `.ua/` or `.orchestration/`; grep fallback now occurs only for a missing graph or an actual source-path change.
- The two policy documents remain 8 and 68 lines respectively; each diff is exactly one replaced line.
- Compared every semantic edge in `df85b37` with the accepted T83 graph (`ebadef6`). All 31 removed edges had surviving endpoints.
- Restored 23 relationships verified in live source. The remaining eight were direct `documents` edges from the dieted seven-line agmsg core rule to individual scripts; they remain removed because the rule no longer names or documents those scripts and delegates detail to the skill.
- Restored the named `check-inbox.sh -> whoami.sh` and `check-inbox.sh -> config.sh` dependencies and all ten template-to-`whoami.sh`/`join.sh` documentation edges.
- Graph counts changed from 1,200 nodes / 934 edges to 1,200 nodes / 957 edges. Fingerprints for the two changed policy documents were rebuilt with the bundled UA builder and merged with LOAD-PATCH-SAVE.

The official UA core validator returns `success=true` with zero issues; deterministic checks report no dangling endpoints, duplicate semantic edges, missing named edges, or fingerprint mismatches.

## Project memory

[memory:decision] UA freshness accepts graph/evidence-only commits between the analyzed hash and HEAD, and incremental graph replacement must audit the complete removed-edge set and restore every still-supported relationship whose endpoints survive.

Recorded as `37d677fb-f13f-4f9f-9076-b666e2beadcf` with:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T83b: Treat a UA graph as current when meta.gitCommitHash equals HEAD or every intervening path is under .ua/ or .orchestration/; incremental LOAD-PATCH-SAVE graph merges must diff parent edges and restore every source-verified relationship whose endpoints survive.'
```

Integration note: because the freshness rule intentionally treats source-changing commits as stale, the orchestrator should commit the two policy-source changes before the graph/evidence-only commit that records their refreshed graph state.

