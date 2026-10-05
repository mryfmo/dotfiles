# T81b learning triage
Date: 2026-10-05
Learnings: No-follow directory construction needs fd-relative mkdir/open/fchmod. Python SQLite accepts a filename and canonicalizes fd aliases, so portable stdlib cannot promise lifetime binding against same-user post-construction swaps. Preserve parent directory permissions while securing only the owned subtree. Discovery start paths enter sys.path, so import local test support before runtime modules to avoid host tests-package shadowing.
Plan Updates: Adopted explicit bounded construction contract; residual documented in README/CHANGELOG/shdoc. No rule or skill promotion.

Round1: installer idempotence requires semantic identity matching rather than positional replacement when managed groups can be reordered. Managed script basenames permit interpreter/path upgrades without moving the group. uv run --no-project bypasses project environment synchronization; it can still inspect settings and warn about malformed pyproject files. Offline unavailable-dependency comparison verified the narrower guarantee.

Round1 health retention: truncation must share an exclusive lock with appends, and an empty log must retain its inode so waiting appenders do not write to an unlinked file. Health-path failure must occur before destructive event pruning. Generated uv commands need an explicit uv prerequisite even when core runtime is stdlib-only.

Decision5: stdlib does not imply cross-platform availability. fcntl must not sit on a shared module import path when import/help should remain portable. Explicit Linux/macOS-only contract resolves unsupported Windows runtime expectations; failing locking before writes preserves the safety contract. No Windows no-follow implementation or unlocked fallback was introduced.

Round2: preserve a function docstring before inserted executable statements. Quarantine retention is concurrent maintenance: tolerate a disappeared entry across both stat and unlink, but keep other failures visible. Deterministic interleaving tests cover continued cleanup and event retention; check inbox at handoff so late scope instructions are not missed.
