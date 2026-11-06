# Security audit report: dotfiles at 0b475694e95f2061dffa73563c7036260dfa11d6

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the diff c41954630b9701da70840171804aef919fafb20b..0b475694e95f2061dffa73563c7036260dfa11d6 (unit U226, branch `fix/dsh-build-commit-input`). The diff touches seven files:
- `home/dot_agents/agent-config.yaml`
- `scripts/lib/installer-pins.sh`
- `scripts/update-agent-assets.sh`
- `scripts/generate-agent-configs.py`
- `tests/unit/test_update_agent_assets.py`
- `tests/unit/test_generate_agent_configs.py`
- `tests/unit/test_network_bounds.py`

Every top-level directory and the repository's root files are seeded as `out_of_scope` ledger units, with the reason. No coverage claim is made for them.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, a post-wave critic, a final-clean critic, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code was built, tested or executed: the task forbids it, and the seat provides no empty allowlisted environment or explicit resource limits. Every ledger check is a source check.

**Independence gap.** The platform's delegation tool (Task) and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave, the post-wave critic and the final-clean critic all ran in the parent agent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** This seat's state root holds no earlier run, and the `sweep` seat's records are not readable from this containment. No prior ledger was available, so there are no carried confirmations and no changed-source revalidations.

**Deferred.** Nothing. **Out of scope:** 13 units (12 directory or root-file units, plus one critic-raised unit; see section 7).

## 2. Security posture

No candidate survives the scoped hunt. The U226 change pins the tag's commit in the reviewed manifest, renders it into a tracked shell constant that CI checks for drift, and validates it to 40 lowercase hex before the updater reads or downloads anything. It then exports it only as the build's `DSH_CLIENT_COMMIT_HASH`.

Upstream's build treats that value as public build metadata. In the installed upstream tree, `scripts/client-build-environment.ts:52-63` re-validates it as hex and keeps 7 characters. No input is selected by it. Integrity of the installed code still rests on the unchanged sha256 pin of the tag archive (`scripts/update-agent-assets.sh:2141-2148`).

## 3. Confirmed findings

None.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None. No source-grounded lead depends on a fact outside the source.

## 6. Hardening notes and positive patterns

These are not findings: none has an affected principal across a boundary.

### Hardening

1. **`ref_commit` is not bound to `pin`.** A tag bump that moves `pin` and `sha256` but not `ref_commit` builds with the old commit as its label. This is metadata only; the sha256 still binds the bytes. A validator rule, or the bump procedure in the manifest's `reason`, could require `ref_commit` to change whenever `pin` does (`home/dot_agents/agent-config.yaml:1366-1369`).
2. **The render path does not apply the 40-hex rule.** `render_asset_constants` checks `ref_commit` only against the plain-value rule (`scripts/generate-agent-configs.py:353-354`), not the 40-hex rule that `--set-asset` (`:305-306`) and the updater (`scripts/update-agent-assets.sh:1967`) apply. A hand-edited, non-hex `ref_commit` passes CI and is refused only on the host at install time (fail closed, exit 1). A validator rule for its shape would move that failure into CI.
3. **The build inherits the operator's whole environment.** Upstream embeds every `DSH_CLIENT_*` variable into the browser artifacts (installed tree `scripts/client-build-environment.ts:13-14`, `:122`). This predates U226, whose only change on that line is the commit's prefix assignment (`scripts/update-agent-assets.sh:2169`). Running the build under an allowlisted environment would bound it. It is recorded as an `out_of_scope` ledger unit for a later full run.

### Positive patterns

- **The environment cannot substitute the pin.** `installer-pins.sh` is sourced after the environment (`scripts/update-agent-assets.sh:51`), and the prefix assignment overrides an inherited `DSH_CLIENT_COMMIT_HASH` (`:2169`).
- **The refusal fails closed before any other work** (`:1967-1970`). It has failure-injection tests for an empty, unset or malformed value, which assert no `curl` call (`tests/unit/test_update_agent_assets.py`).
- **The receipt is JSON data.** It is written through `jq --args` (`scripts/lib/asset-manifest.sh:74-75`). Its only reader pattern-matches recorded commands and never runs them (`home/dot_local/bin/common/executable_remove-agent-asset:260-290`).
- **The network-bounds exemption is keyed by the exact whole line** (`tests/unit/test_network_bounds.py:103-106`, `:540`), so the edited record line exempts nothing else.
- **Removing the `git rev-parse HEAD` fallback** also removes the build's dependence on whatever git repository might enclose the install tree.

## 7. Coverage summary

From `coverage-ledger.json` (19 units):

| Status | Units |
|---|---|
| covered | 6 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 13 |

The six covered units, each owned by `parent-hunter` with source checks:
1. the manifest commit as a build input (supply chain: mutable and unbound build inputs);
2. `DSH_COMMIT` at its shell and receipt sinks (injection);
3. the updater's fail-closed ordering (business logic);
4. `--set-asset ref_commit` (injection);
5. the render into `installer-pins.sh` (generated-source provenance);
6. the changed test modules (obvious things).

The 13 out-of-scope units are `.claude`, `.github`, `.orchestration`, `.ua`, `docs`, `home`, `install`, `plans`, `scripts`, `tests` and `vendor` (each for its unchanged paths), the repository root files, and the critic-raised build-environment unit.

**Excluded companions.** Web/auth, client-side, AI/LLM, cloud, protocol, resource exhaustion, data isolation, desktop/IPC and memory safety are excluded, each with its reason in the ledger. The diff has none of those surfaces.

**Critic results.** The post-wave critic raised one gap outside the diff (the build's inherited environment), recorded as `out_of_scope`. The final-clean critic found no further work. Neither critic was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
