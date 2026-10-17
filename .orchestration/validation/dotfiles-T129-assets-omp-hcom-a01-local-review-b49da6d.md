---
task: dotfiles-T129-assets-omp-hcom-a01
head: b49da6dd3c9e9a93301af4c0d3dd62b058852abf
pr: 388
base: e9bc99d2fe02b8e35b33350d1fd0a0cdc1185dbd
started: 2026-10-17T14:28:08Z
finished: 2026-10-17T14:31:59Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve the wheel referenced by uv's installation receipt — scripts/update-agent-assets.sh:989-989

```text
The hcom installer leaves uv referencing a deleted source archive, breaking later upgrade resolution. Shell static checks passed; live installation and upgrade tests were unavailable under the read-only and network restrictions.

Review comment:

- [P2] Preserve the wheel referenced by uv's installation receipt — scripts/update-agent-assets.sh:989-989
  After installation, the EXIT trap deletes the wheel, but uv records that local path as hcom's source in `uv-receipt.toml`. Subsequent `make update` runs invoke `uv tool upgrade --all` through `scripts/upgrade-tools.sh:424`; refreshing or re-resolving hcom, particularly after cache eviction, then fails because its source archive no longer exists. Retain the verified wheel at a stable managed path or persist an equivalent hash-verified source.
The hcom installer leaves uv referencing a deleted source archive, breaking later upgrade resolution. Shell static checks passed; live installation and upgrade tests were unavailable under the read-only and network restrictions.

Review comment:

- [P2] Preserve the wheel referenced by uv's installation receipt — scripts/update-agent-assets.sh:989-989
  After installation, the EXIT trap deletes the wheel, but uv records that local path as hcom's source in `uv-receipt.toml`. Subsequent `make update` runs invoke `uv tool upgrade --all` through `scripts/upgrade-tools.sh:424`; refreshing or re-resolving hcom, particularly after cache eviction, then fails because its source archive no longer exists. Retain the verified wheel at a stable managed path or persist an equivalent hash-verified source.
```
