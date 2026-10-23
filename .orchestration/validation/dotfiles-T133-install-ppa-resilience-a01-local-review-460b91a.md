---
task: dotfiles-T133-install-ppa-resilience-a01
head: 460b91a5de63719e1cf45447442e506bafca676e
pr: 454
base: d06d94fd8eedcd0770c1c80c2b1596ec36109ef8
started: 2026-10-22T06:11:13Z
finished: 2026-10-22T06:19:01Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Handle PPA failures in the dependency-phase index refresh — install/ubuntu/client/ghostty.sh:79-82
- [P2] Preserve the apt refresh before installing misc packages — home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl:8-9

```text
The reordered installation can fail against stale package indexes, and the outage fallback misses the initial refresh on retries. Both cases can still abort chezmoi apply.

Full review comments:

- [P2] Preserve the apt refresh before installing misc packages — home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl:8-9
  On an existing client with stale apt indexes, moving Ghostty to `run_after_` removes the refresh that previously preceded `install_misc`. The changed misc wrapper runs again because its content changed, while unchanged `run_once_` scripts remain skipped. Since `install_misc` only runs `apt-get install`, it can request obsolete package versions and fail with HTTP 404, aborting apply before this new script runs. Preserve an index refresh before the misc installation.

- [P2] Handle PPA failures in the dependency-phase index refresh — install/ubuntu/client/ghostty.sh:79-82
  When a previous skip leaves the PPA configured and apt uses `APT::Update::Error-Mode=any`, a continuing PPA outage makes the next apply exit 100 inside `install_ghostty_dependencies`, before reaching these guarded calls. That function's initial refresh reads the configured PPA too, so the new fallback does not consistently protect retries. Apply PPA-aware handling to that refresh while retaining fatal Ubuntu dependency errors, and test a retry with the PPA already configured.
The reordered installation can fail against stale package indexes, and the outage fallback misses the initial refresh on retries. Both cases can still abort chezmoi apply.

Full review comments:

- [P2] Preserve the apt refresh before installing misc packages — home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl:8-9
  On an existing client with stale apt indexes, moving Ghostty to `run_after_` removes the refresh that previously preceded `install_misc`. The changed misc wrapper runs again because its content changed, while unchanged `run_once_` scripts remain skipped. Since `install_misc` only runs `apt-get install`, it can request obsolete package versions and fail with HTTP 404, aborting apply before this new script runs. Preserve an index refresh before the misc installation.

- [P2] Handle PPA failures in the dependency-phase index refresh — install/ubuntu/client/ghostty.sh:79-82
  When a previous skip leaves the PPA configured and apt uses `APT::Update::Error-Mode=any`, a continuing PPA outage makes the next apply exit 100 inside `install_ghostty_dependencies`, before reaching these guarded calls. That function's initial refresh reads the configured PPA too, so the new fallback does not consistently protect retries. Apply PPA-aware handling to that refresh while retaining fatal Ubuntu dependency errors, and test a retry with the PPA already configured.
```
