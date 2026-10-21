---
task: dotfiles-T133-task-generator-plan-check-a04
head: 7a201eab2e77596c9a7bc421162b2f3fde25f6f7
pr: 417
base: ba318e5369b14a79d6f515e87b685c9bcb30c12e
started: 2026-10-20T00:38:09Z
finished: 2026-10-20T00:43:25Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve trusted token authentication for GitHub CLI children — scripts/orchestrator/task-consistency-check.py:165-174
- [P2] Reject failed C14 probes even when stdout matches — scripts/orchestrator/task-consistency-check.py:418-422

```text
C14 accepts failed existence probes, and sanitized GitHub CLI launches lose token-based authentication. Full test suites were not run in the read-only sandbox.

Full review comments:

- [P2] Reject failed C14 probes even when stdout matches — scripts/orchestrator/task-consistency-check.py:418-422
  For an authorized premise such as `test -f scripts/missing.py` with an empty expected output, `rerun()` returns `('', 1, '')`, but `_code` is ignored and C14 reports success. I reproduced this with a nonexistent file. Check the probe's exit status as well as stdout so false existence premises cannot pass validation.

- [P2] Preserve trusted token authentication for GitHub CLI children — scripts/orchestrator/task-consistency-check.py:165-174
  On runners authenticated through `GH_TOKEN` or `GITHUB_TOKEN` without a saved GitHub CLI login, this reconstructed environment drops their only credential. The new canonical-main reads consequently fail at `gh api`, even when executable bindings, cache and interpreter are valid. Provide an explicit trusted authentication channel for the sanitized `gh` child rather than requiring a persisted host login.
C14 accepts failed existence probes, and sanitized GitHub CLI launches lose token-based authentication. Full test suites were not run in the read-only sandbox.

Full review comments:

- [P2] Reject failed C14 probes even when stdout matches — scripts/orchestrator/task-consistency-check.py:418-422
  For an authorized premise such as `test -f scripts/missing.py` with an empty expected output, `rerun()` returns `('', 1, '')`, but `_code` is ignored and C14 reports success. I reproduced this with a nonexistent file. Check the probe's exit status as well as stdout so false existence premises cannot pass validation.

- [P2] Preserve trusted token authentication for GitHub CLI children — scripts/orchestrator/task-consistency-check.py:165-174
  On runners authenticated through `GH_TOKEN` or `GITHUB_TOKEN` without a saved GitHub CLI login, this reconstructed environment drops their only credential. The new canonical-main reads consequently fail at `gh api`, even when executable bindings, cache and interpreter are valid. Provide an explicit trusted authentication channel for the sanitized `gh` child rather than requiring a persisted host login.
```
