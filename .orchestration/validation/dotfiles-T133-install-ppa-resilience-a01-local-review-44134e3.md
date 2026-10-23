---
task: dotfiles-T133-install-ppa-resilience-a01
head: 44134e36c167ab57a6ca048b2dd75ff7431b87f8
pr: 454
base: 7da0cdfab9de9fbea673b82379acd4e317115065
started: 2026-10-22T01:36:58Z
finished: 2026-10-22T01:43:28Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P2] Detect failed index downloads when apt exits zero — install/ubuntu/client/ghostty.sh:52-53
- [P2] Keep skipped installations eligible for the next apply — install/ubuntu/client/ghostty.sh:68-70
- [P2] Preserve non-PPA errors in mixed apt failures — install/ubuntu/client/ghostty.sh:53-53

```text
Successful skips prevent the advertised chezmoi retry. The fallback also misses warning-only index failures and incorrectly suppresses unrelated errors when apt reports mixed failures.

Full review comments:

- [P2] Keep skipped installations eligible for the next apply — install/ubuntu/client/ghostty.sh:68-70
  After a package-download outage, returning success lets `home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl` finish and be recorded as completed by chezmoi. Subsequent `make update` calls do not rerun that unchanged script, so Ghostty remains absent after the PPA recovers despite the promised retry. Move the retryable installation into a repeatable entrypoint or otherwise preserve a pending retry.

- [P2] Detect failed index downloads when apt exits zero — install/ubuntu/client/ghostty.sh:52-53
  During a transient index-download failure, `apt-get update` can print `W: Failed to fetch ...` and still exit zero. This early return ignores that outage. On a fresh installation without a cached Ghostty index, the subsequent install fails with `Unable to locate package ghostty`, which does not match the fallback, so the apply and live test still fail. Handle this warning-only update outcome; the new fixture only models exit 100.

- [P2] Preserve non-PPA errors in mixed apt failures — install/ubuntu/client/ghostty.sh:53-53
  If `apt-get install ghostty` reports both a Ghostty PPA download failure and an Ubuntu archive failure for a required dependency, this check returns 75 solely because one line matches. The caller then exits successfully, suppressing the unrelated apt failure that previously failed the apply. Only tolerate failures attributable exclusively to the PPA outage, and add a mixed-failure fixture; the current archive fixture fails before reaching this helper.
Successful skips prevent the advertised chezmoi retry. The fallback also misses warning-only index failures and incorrectly suppresses unrelated errors when apt reports mixed failures.

Full review comments:

- [P2] Keep skipped installations eligible for the next apply — install/ubuntu/client/ghostty.sh:68-70
  After a package-download outage, returning success lets `home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl` finish and be recorded as completed by chezmoi. Subsequent `make update` calls do not rerun that unchanged script, so Ghostty remains absent after the PPA recovers despite the promised retry. Move the retryable installation into a repeatable entrypoint or otherwise preserve a pending retry.

- [P2] Detect failed index downloads when apt exits zero — install/ubuntu/client/ghostty.sh:52-53
  During a transient index-download failure, `apt-get update` can print `W: Failed to fetch ...` and still exit zero. This early return ignores that outage. On a fresh installation without a cached Ghostty index, the subsequent install fails with `Unable to locate package ghostty`, which does not match the fallback, so the apply and live test still fail. Handle this warning-only update outcome; the new fixture only models exit 100.

- [P2] Preserve non-PPA errors in mixed apt failures — install/ubuntu/client/ghostty.sh:53-53
  If `apt-get install ghostty` reports both a Ghostty PPA download failure and an Ubuntu archive failure for a required dependency, this check returns 75 solely because one line matches. The caller then exits successfully, suppressing the unrelated apt failure that previously failed the apply. Only tolerate failures attributable exclusively to the PPA outage, and add a mixed-failure fixture; the current archive fixture fails before reaching this helper.
```
