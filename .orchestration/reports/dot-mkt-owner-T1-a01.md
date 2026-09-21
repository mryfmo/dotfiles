# dot-mkt-owner-T1-a01 report

status: ready_for_review
cost: n/a

## Result

- Renamed `home/dot_agents/plugins/marketplace.json` to `create_marketplace.json` and changed the generator manifest, validator, focused test, and documentation references.
- Added a target-exists conditional to `home/.chezmoiignore`. Fresh machines receive the generated seed; after the target exists, chezmoi no longer changes or checks its runtime-owned contents or mode.
- The narrowly approved `home/dot_agents/agent-config.yaml` change is exactly one hunk: `plugins.marketplace_path` changed from `home/dot_agents/plugins/marketplace.json` to `home/dot_agents/plugins/create_marketplace.json`. Every other manifest section is byte-identical.
- Kept the existing post-Crit chmod unchanged as requested; no shell lifecycle behavior was expanded.

## F1 writer conclusion

The concrete operator-machine 0664 writer remains **UNIDENTIFIED**. Credential-free `adh-test` runs excluded these tested candidates:

- Codex 0.150.1 `exec`: no mode, mtime, or content change.
- Claude 2.1.251 `--version` and `-p`: no mode, mtime, or content change.
- Crit 0.20.2: rewrote the existing file without changing 0644; first creation under umask 002 also created 0644.

Authenticated interactive Codex/Claude TUI sessions were not exercised and remain a residual hypothesis. No false writer attribution is claimed.

## F2/F3 acceptance

- Fresh-machine VM path created mode 0644 seed content byte-identical to the generated source.
- Existing-machine VM transition preserved runtime-only content and mode 0664 exactly and emitted zero drift warnings.
- Orchestrator approved injecting the operator-observed 0664 state because no pinned candidate reproduced it. Literal `make update` before and after that state both exited 0; the second emitted `drift-warning-count=0`, and final `chezmoi status` was clean.
- All scratch users and homes were removed.

## Validation

- Focused test-first check passed.
- Generated agent configs are current and agent asset validation passes.
- All 364 Python unit tests pass.
- `git diff --check` passes.
- Local Bats was not run by policy.
- Crit-data review approval `r_132f11` is resolved; the final review gate passes.
- Full evidence: `.orchestration/validation/dot-mkt-owner-T1-a01.md`.

## Durable decision

[memory:decision] Seed runtime-owned marketplace state with chezmoi `create_`, then conditionally ignore the target once it exists; `create_` alone still participates in mode/state handling and does not complete the ownership handoff.

CompactionDB decision ID: `51b71540-dc8a-4e3b-8d8c-b5be91c6b6b4`.

## Constraints honored

- No commit, push, local Bats, login, credential transfer, mise config/lock edit, or new top-level directory.
- VM access used only `limactl shell adh-test`.
- Repository edits stayed within the issued scope plus the three narrowly approved files.
