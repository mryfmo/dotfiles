---
task: dotfiles-T133-install-ppa-resilience-a01
head: e6b645fcdb6174ffd28eb6bb4b467ca3dd2d7cfc
pr: 454
base: d06d94fd8eedcd0770c1c80c2b1596ec36109ef8
started: 2026-10-22T03:47:17Z
finished: 2026-10-22T03:53:38Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Check package state before skipping installation — install/ubuntu/client/ghostty.sh:67-69
- [P2] Preserve non-fetch errors accompanying PPA warnings — install/ubuntu/client/ghostty.sh:55-57

```text
The new logic can permanently skip an incomplete installation and incorrectly suppress unrelated apt failures. Both behaviors were reproduced with Bash fixtures comparing the base and changed implementations.

Full review comments:

- [P2] Check package state before skipping installation — install/ubuntu/client/ghostty.sh:67-69
  `dpkg -s` also succeeds for packages left unpacked or half-configured after an interrupted installation. The new guard therefore makes every subsequent apply return success without allowing apt to finish installing Ghostty. Check that the reported status is `install ok installed`, rather than relying only on dpkg's exit code, and cover an unpacked package in the fixture.

- [P2] Preserve non-fetch errors accompanying PPA warnings — install/ubuntu/client/ghostty.sh:55-57
  When a guarded apt step reports a Ghostty fetch warning alongside a hard error without `Failed to fetch` in its text, such as an unsigned-repository error, this filter discards the hard error and returns 75 despite apt exiting 100. `install_ghostty` then incorrectly reports success and labels the failure a temporary PPA outage. Rule out other fatal diagnostics before suppressing the failure; the current mixed-source fixture only covers additional fetch errors.
The new logic can permanently skip an incomplete installation and incorrectly suppress unrelated apt failures. Both behaviors were reproduced with Bash fixtures comparing the base and changed implementations.

Full review comments:

- [P2] Check package state before skipping installation — install/ubuntu/client/ghostty.sh:67-69
  `dpkg -s` also succeeds for packages left unpacked or half-configured after an interrupted installation. The new guard therefore makes every subsequent apply return success without allowing apt to finish installing Ghostty. Check that the reported status is `install ok installed`, rather than relying only on dpkg's exit code, and cover an unpacked package in the fixture.

- [P2] Preserve non-fetch errors accompanying PPA warnings — install/ubuntu/client/ghostty.sh:55-57
  When a guarded apt step reports a Ghostty fetch warning alongside a hard error without `Failed to fetch` in its text, such as an unsigned-repository error, this filter discards the hard error and returns 75 despite apt exiting 100. `install_ghostty` then incorrectly reports success and labels the failure a temporary PPA outage. Rule out other fatal diagnostics before suppressing the failure; the current mixed-source fixture only covers additional fetch errors.
```
