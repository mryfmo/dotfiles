---
task: dotfiles-T133-permission-guard-gate-a04
head: 911f5202e61a2e46f527fcd9a4eda0041e97410a
pr: 420
base: 86ea98848b595f53e0afcf8f298ebda311a51dcf
started: 2026-10-19T02:11:52Z
finished: 2026-10-19T02:18:35Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Sanitize the environment used by checkout identity checks — home/dot_claude/hooks/executable_gh-merge-gate.sh:78-79
- [P2] Authorize merges without requiring a post-merge dispatch — home/dot_claude/hooks/executable_gh-merge-gate.sh:138-140

```text
The hook permits inherited Git environment variables to bypass checkout binding and requires a post-merge notification before allowing normal merges. Focused read-only reproductions confirmed both behaviors; the full test suite was not run.

Full review comments:

- [P1] Sanitize the environment used by checkout identity checks — home/dot_claude/hooks/executable_gh-merge-gate.sh:78-79
  If the Claude session inherits `GIT_DIR` and `GIT_WORK_TREE` pointing at the primary checkout, these subprocesses report that checkout regardless of the payload cwd. I reproduced `canonical_checkout()` accepting this linked review worktree under those overrides. Consequently, an otherwise eligible merge or ready creation can bypass the primary-checkout restriction. Only tool resolution uses `env -i`; sanitize the environment of the actual checks too. The environment-control threat row does not mitigate this bypass ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Authorize merges without requiring a post-merge dispatch — home/dot_claude/hooks/executable_gh-merge-gate.sh:138-140
  The required integration sequence writes the acceptance record, runs the gate, merges, and only then sends `AGMSG-ACCEPTANCE status=accepted` ([AGENTS.md:44](AGENTS.md#L44)). Thus a correctly prepared first merge has no accepted dispatch yet and this condition always asks, defeating prompt-free merges. `acceptance-front-matter.py` preserves dispatch history but does not create that event. Use pre-merge acceptance evidence here, or update the protocol coherently rather than requiring its final notification beforehand.
The hook permits inherited Git environment variables to bypass checkout binding and requires a post-merge notification before allowing normal merges. Focused read-only reproductions confirmed both behaviors; the full test suite was not run.

Full review comments:

- [P1] Sanitize the environment used by checkout identity checks — home/dot_claude/hooks/executable_gh-merge-gate.sh:78-79
  If the Claude session inherits `GIT_DIR` and `GIT_WORK_TREE` pointing at the primary checkout, these subprocesses report that checkout regardless of the payload cwd. I reproduced `canonical_checkout()` accepting this linked review worktree under those overrides. Consequently, an otherwise eligible merge or ready creation can bypass the primary-checkout restriction. Only tool resolution uses `env -i`; sanitize the environment of the actual checks too. The environment-control threat row does not mitigate this bypass ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Authorize merges without requiring a post-merge dispatch — home/dot_claude/hooks/executable_gh-merge-gate.sh:138-140
  The required integration sequence writes the acceptance record, runs the gate, merges, and only then sends `AGMSG-ACCEPTANCE status=accepted` ([AGENTS.md:44](AGENTS.md#L44)). Thus a correctly prepared first merge has no accepted dispatch yet and this condition always asks, defeating prompt-free merges. `acceptance-front-matter.py` preserves dispatch history but does not create that event. Use pre-merge acceptance evidence here, or update the protocol coherently rather than requiring its final notification beforehand.
```
