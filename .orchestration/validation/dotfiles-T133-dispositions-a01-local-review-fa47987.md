---
task: dotfiles-T133-dispositions-a01
head: fa47987b408927c507bfadec6115ebdfceb0a110
pr: 419
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T20:52:06Z
finished: 2026-10-18T20:57:14Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Reject test refutations that execute only skipped tests — scripts/orchestrator/dispositions.py:131-132
- [P2] Return a not-applicable demand for upstream-only changes — scripts/orchestrator/dispositions.py:102-103

```text
The verifier accepts skipped tests as refutations and can block valid dispositions after upstream-only changes. Targeted read-only checks reproduced both issues; the full suite was not run because it creates temporary files.

Full review comments:

- [P2] Reject test refutations that execute only skipped tests — scripts/orchestrator/dispositions.py:131-132
  `unittest` exits zero for skip-only runs, so this accepts evidence without executing a behavioral check. For example, the existing `ChezmoiRemoveAgmsgTest` is skipped when `chezmoi` is absent—which the gate's private PATH guarantees—but is recorded as verified with `exit 0: OK (skipped=1)`. With `DISPOSITIONS_REQUIRE_REFUTATION=1`, a finding can therefore be dismissed without testing it. Require at least one non-skipped passing test and cover this case before treating the threat-table row as closed ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Return a not-applicable demand for upstream-only changes — scripts/orchestrator/dispositions.py:102-103
  After a PR incorporates newer `main` changes, `commit..head` can contain a covering hunk whose commits are all excluded by `^base`. Git then successfully returns an empty log, but this branch raises `Hold`, making strict `orch-gate.sh` refuse even when the saved not-applicable disposition has valid test or source evidence. An empty eligible log means there is no PR fix candidate, not that history is unreadable. Return the not-applicable demand here and reserve `Hold` for actual Git failures.
The verifier accepts skipped tests as refutations and can block valid dispositions after upstream-only changes. Targeted read-only checks reproduced both issues; the full suite was not run because it creates temporary files.

Full review comments:

- [P2] Reject test refutations that execute only skipped tests — scripts/orchestrator/dispositions.py:131-132
  `unittest` exits zero for skip-only runs, so this accepts evidence without executing a behavioral check. For example, the existing `ChezmoiRemoveAgmsgTest` is skipped when `chezmoi` is absent—which the gate's private PATH guarantees—but is recorded as verified with `exit 0: OK (skipped=1)`. With `DISPOSITIONS_REQUIRE_REFUTATION=1`, a finding can therefore be dismissed without testing it. Require at least one non-skipped passing test and cover this case before treating the threat-table row as closed ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Return a not-applicable demand for upstream-only changes — scripts/orchestrator/dispositions.py:102-103
  After a PR incorporates newer `main` changes, `commit..head` can contain a covering hunk whose commits are all excluded by `^base`. Git then successfully returns an empty log, but this branch raises `Hold`, making strict `orch-gate.sh` refuse even when the saved not-applicable disposition has valid test or source evidence. An empty eligible log means there is no PR fix candidate, not that history is unreadable. Return the not-applicable demand here and reserve `Hold` for actual Git failures.
```
