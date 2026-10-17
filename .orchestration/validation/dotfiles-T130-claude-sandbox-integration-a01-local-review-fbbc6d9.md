---
task: dotfiles-T130-claude-sandbox-integration-a01
head: fbbc6d98008114bcd47021f7a59e6960bad756d0
pr: 392
base: e9bc99d2fe02b8e35b33350d1fd0a0cdc1185dbd
started: 2026-10-17T15:04:08Z
finished: 2026-10-17T15:10:13Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Handle existing non-npm omp entries before installing — scripts/update-agent-assets.sh:944-944
- [P2] Preserve the wheel referenced by uv's installation receipt — scripts/update-agent-assets.sh:989-989

```text
The installers introduce failures in subsequent uv upgrades and migration from existing omp installations. Review was pinned to the initial head b49da6d because the checkout changed during inspection.

Full review comments:

- [P2] Preserve the wheel referenced by uv's installation receipt — scripts/update-agent-assets.sh:989-989
  After installation, the EXIT trap deletes the wheel, but uv persists that local filename as hcom's source in its tool receipt. The next `make update` invokes `uv tool upgrade --all` through `upgrade_uv_tools`, which fails when it resolves the deleted source. Keep the verified wheel at a stable managed path and cover a subsequent upgrade in the tests.

- [P2] Handle existing non-npm omp entries before installing — scripts/update-agent-assets.sh:944-944
  If `~/.local/bin/omp` already contains a standalone executable or an external symlink, including a dangling one, npm refuses to replace it with `EEXIST`. This was reproducible with the existing external omp link using npm's read-only bin check. Consequently, an installation requiring this update aborts before hcom and the remaining asset refreshes. Handle migration of existing entries explicitly; the fake npm fixture currently overwrites them and misses this failure.
The installers introduce failures in subsequent uv upgrades and migration from existing omp installations. Review was pinned to the initial head b49da6d because the checkout changed during inspection.

Full review comments:

- [P2] Preserve the wheel referenced by uv's installation receipt — scripts/update-agent-assets.sh:989-989
  After installation, the EXIT trap deletes the wheel, but uv persists that local filename as hcom's source in its tool receipt. The next `make update` invokes `uv tool upgrade --all` through `upgrade_uv_tools`, which fails when it resolves the deleted source. Keep the verified wheel at a stable managed path and cover a subsequent upgrade in the tests.

- [P2] Handle existing non-npm omp entries before installing — scripts/update-agent-assets.sh:944-944
  If `~/.local/bin/omp` already contains a standalone executable or an external symlink, including a dangling one, npm refuses to replace it with `EEXIST`. This was reproducible with the existing external omp link using npm's read-only bin check. Consequently, an installation requiring this update aborts before hcom and the remaining asset refreshes. Handle migration of existing entries explicitly; the fake npm fixture currently overwrites them and misses this failure.
```
