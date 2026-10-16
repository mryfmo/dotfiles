---
task: dotfiles-T128-seat-liveness-a01
head: d3bc745c7e7ee306f949fe85034bc79c9ff83fc1
pr: 367
base: 907522c2ac89c2096a91e70d9effb512886df681
started: 2026-10-15T08:15:41Z
finished: 2026-10-15T08:16:40Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Prepare the archive destination before removing the identity — home/dot_local/bin/common/executable_herdr-agents:1964-1966

```text
🤖 I read the AGENTS.md for mryfmo/dotfiles. The stale-removal flow can permanently orphan a placement record if its final archive operation fails after the identity has been removed.

Review comment:

- [P2] Prepare the archive destination before removing the identity — home/dot_local/bin/common/executable_herdr-agents:1964-1966
  When `run/stale` cannot be created or the subsequent `mv` fails, this path has already disabled delivery and successfully removed the identity via `leave.sh`; `set -e` then exits while the active `spawn.*` record remains. A retry cannot discover the seat through `identities.sh`, leaving exactly the orphaned placement record this option is intended to retire. Create/validate the destination before cleanup, or roll back/reorder the operations so an archive failure cannot leave identity and record state inconsistent.
🤖 I read the AGENTS.md for mryfmo/dotfiles. The stale-removal flow can permanently orphan a placement record if its final archive operation fails after the identity has been removed.

Review comment:

- [P2] Prepare the archive destination before removing the identity — home/dot_local/bin/common/executable_herdr-agents:1964-1966
  When `run/stale` cannot be created or the subsequent `mv` fails, this path has already disabled delivery and successfully removed the identity via `leave.sh`; `set -e` then exits while the active `spawn.*` record remains. A retry cannot discover the seat through `identities.sh`, leaving exactly the orphaned placement record this option is intended to retire. Create/validate the destination before cleanup, or roll back/reorder the operations so an archive failure cannot leave identity and record state inconsistent.
```
