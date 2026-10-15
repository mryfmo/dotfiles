---
task: dotfiles-T128-chain-review-scripts-a01
head: b6ce4ffabe0e66a102e224e75be575a501c5a793
pr: 357
base: ec94dc56305f55df470a4b1d4215ad272418beac
started: 2026-10-14T13:20:02Z
finished: 2026-10-14T13:20:48Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Fail closed when the review process exits nonzero — scripts/orchestrator/local-review.sh:61-61
- [P2] Verify the full commit before reusing a cached review — scripts/orchestrator/local-review.sh:27-28

```text
The review wrapper can cache a failed review as a successful zero-finding result and can reuse evidence belonging to a different commit after a short-hash collision. Both defects undermine the reliability of the integration review gate.

Full review comments:

- [P1] Fail closed when the review process exits nonzero — scripts/orchestrator/local-review.sh:61-61
  When Codex fails before producing findings—for example due to initialization, configuration, or runtime errors—this branch logs the failure but still writes `findings: 0` and exits successfully. That artifact is then cached, so subsequent integration attempts treat an incomplete review as a clean review; preserve the nonzero status and avoid creating a reusable success artifact.

- [P2] Verify the full commit before reusing a cached review — scripts/orchestrator/local-review.sh:27-28
  When two reviewed commits for the same task share their first seven hexadecimal characters, the second invocation finds the first commit's artifact and returns its findings without validating the recorded `head:`. Fixed-length seven-character prefixes are not guaranteed unique, so compare the artifact's full head with the requested commit or key the file by the full hash.
The review wrapper can cache a failed review as a successful zero-finding result and can reuse evidence belonging to a different commit after a short-hash collision. Both defects undermine the reliability of the integration review gate.

Full review comments:

- [P1] Fail closed when the review process exits nonzero — scripts/orchestrator/local-review.sh:61-61
  When Codex fails before producing findings—for example due to initialization, configuration, or runtime errors—this branch logs the failure but still writes `findings: 0` and exits successfully. That artifact is then cached, so subsequent integration attempts treat an incomplete review as a clean review; preserve the nonzero status and avoid creating a reusable success artifact.

- [P2] Verify the full commit before reusing a cached review — scripts/orchestrator/local-review.sh:27-28
  When two reviewed commits for the same task share their first seven hexadecimal characters, the second invocation finds the first commit's artifact and returns its findings without validating the recorded `head:`. Fixed-length seven-character prefixes are not guaranteed unique, so compare the artifact's full head with the requested commit or key the file by the full hash.
```
