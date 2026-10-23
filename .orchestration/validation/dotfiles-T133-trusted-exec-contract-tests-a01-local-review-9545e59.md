---
task: dotfiles-T133-trusted-exec-contract-tests-a01
head: 9545e59f4a91aae36cd850c4645d29c366845844
pr: 436
base: 118daafa4610549d3bc280800cf8b1d36fb851dc
started: 2026-10-20T02:20:06Z
finished: 2026-10-20T02:24:26Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Give worker-root writes a distinct timestamp baseline — tests/unit/trusted_exec_contract.py:109-111

```text
The shared probe can incorrectly report that a worker-root file was untouched after a write. Two read-only unit checks passed; the fixture-based suite could not be rerun in this sandbox.

Review comment:

- [P2] Give worker-root writes a distinct timestamp baseline — tests/unit/trusted_exec_contract.py:109-111
  On filesystems with coarse modification timestamps, an immediate same-length overwrite can preserve the file's inode, size and mtime. Because writing does not advance its atime, `assert_untouched()` then passes despite the worker-root write. The individual write controls change the length or inode, so they miss this case. Initialize mtime to a distinguishable sentinel, as already done for atime, and add a same-length overwrite control.
The shared probe can incorrectly report that a worker-root file was untouched after a write. Two read-only unit checks passed; the fixture-based suite could not be rerun in this sandbox.

Review comment:

- [P2] Give worker-root writes a distinct timestamp baseline — tests/unit/trusted_exec_contract.py:109-111
  On filesystems with coarse modification timestamps, an immediate same-length overwrite can preserve the file's inode, size and mtime. Because writing does not advance its atime, `assert_untouched()` then passes despite the worker-root write. The individual write controls change the length or inode, so they miss this case. Initialize mtime to a distinguishable sentinel, as already done for atime, and add a same-length overwrite control.
```
