# T87 Validation

## UA incremental update

- Source baseline: `607e6dc61e20075eb2e560b922d6cdcfae831fb2`.
- Current post-#147 HEAD: `d91b835021981a2fb604c61e2ef324f972cc8795`.
- Changed paths: `home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`.
- Decision: partial update; both paths classified structural.
- Replaced nodes: 3; fresh nodes: 3; node IDs unchanged.
- Official UA validation: success. The two auto-corrected fields are pre-existing baseline issues with exact issue parity.
- Independent checks: 1,201 unique nodes, 934 unique edges, 0 dangling edges, 737 unique layer assignments, valid tour references.
- Unchanged nodes, all edges, layers, and tour are JSON-identical to the baseline.
- Fingerprint store: 722 entries in the nested `files` envelope; extensionless shell remains conservative and Python retains structural analysis.
- `git diff --check`: pass.

## Pull-request scope and CI

Final `git show --stat` and `gh pr checks` outputs are recorded in the follow-up artifact update after all three PR numbers and green states exist.

## Boundary status

The final main-checkout `git status --short` audit is recorded after PR A's final push and exact untracked orchestration cleanup.
