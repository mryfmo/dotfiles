# T85 Validation

## Incremental scope

- Baseline graph: 1,200 nodes / 957 edges.
- Changed active paths: 19 (the #140 shell/config/Python/Bats/test set).
- Pruned baseline fragment: 1,050 retained nodes / 715 retained edges.
- Fresh analyzer output: 144 nodes / 245 edges across three batches.
- Current-source recovery: 10 short `update-agent-assets.sh` function nodes with extractor-backed line ranges.
- Final graph: 1,204 nodes / 974 edges.
- No source files, Bats suites, or full-analysis phases were executed or modified.

## Complete removed-edge classification

Machine-readable audit: `.ua/intermediate/t85-edge-audit.json`.

```text
parent removed edges: 242
freshly emitted:      222
restored:              20
endpoint deleted:       0
unclassified:           0
```

Every mapped endpoint that remains in current source is present. The five renamed config endpoints were mapped to `modify_private_*`; ten short shell-function nodes omitted by the semantic significance filter were reconstructed from the bundled extractor before their relationships were restored.

## Graph checks

```text
UA core validateGraph: success=true, issues=0
independent validator: issues=0, warnings=380
duplicate semantic edges: 0
dangling edges: 0
file-level nodes: 736
layer assignments: 736 total / 736 unique
tour: 13 sequential steps, all node IDs valid
old profile graph IDs: 0
new profile graph IDs: 5
old profile fingerprint paths: 0
new profile fingerprint paths: 5
```

Node types: service 2, pipeline 6, document 376, config 49, file 288, resource 15, function 436, class 32.

Edge types: related 83, configures 5, documents 46, contains 483, depends_on 22, calls 27, exports 249, imports 46, tested_by 13.

Layer counts: managed-home 243, bootstrap 26, automation 32, quality 46, infrastructure 9, documentation 344, project-config 15, contextdb 21.

## Fingerprints and metadata

```text
changed fingerprints generated: 19
merged fingerprint store: 721
meta analyzedFiles: 721
graph.project.gitCommitHash: b48d52c1fadb1808669ced3343aa25055709079b
meta.gitCommitHash:          b48d52c1fadb1808669ced3343aa25055709079b
fingerprints.gitCommitHash:  b48d52c1fadb1808669ced3343aa25055709079b
git diff --check: pass
```

All `.ua/knowledge-graph.json`, `.ua/meta.json`, and `.ua/fingerprints.json` files parse as JSON.
