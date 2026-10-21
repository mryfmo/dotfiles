---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "shims-on-path",
      "id": "audit:99c37ca:401"
    },
    {
      "class": "happy-path-closing-test",
      "id": "audit:99c37ca:402"
    },
    {
      "class": "repo-binding",
      "id": "audit:99c37ca:403"
    },
    {
      "class": "empty-result-passes",
      "id": "audit:99c37ca:404"
    },
    {
      "class": "contract-restatement",
      "id": "audit:72882ac:401"
    },
    {
      "class": "contract-restatement",
      "id": "audit:72882ac:402"
    },
    {
      "class": "contract-restatement",
      "id": "audit:72882ac:403"
    },
    {
      "class": "contract-restatement",
      "id": "audit:72882ac:404"
    },
    {
      "class": "contract-restatement",
      "id": "audit:72882ac:405"
    }
  ],
  "pr": null,
  "replans": {
    "contract-restatement": {
      "design": "the text's threat rows for environment and executables point at the shared contract tests, not at per-text restatements, so a C-80 review judges the tool-specific rows only",
      "implementation": "after #436 and #431 merge, one re-authoring that replaces lines 25, 27, 61, 64 and 77 with references to the landed tests and binding",
      "specification": "a task text for a tool that runs git and gh names the trusted-execution contract by reference (design 5.14 items 2, 7, 9 and the contract tests of #436, the binding of #431) and states only what is specific to the tool",
      "verification": "C-80 round 3 reports no contract-class finding, and pre-send passes."
    }
  },
  "searches": [],
  "task": "dotfiles-T133-result-evidence-check-a01"
}
---

# Acceptance record: dotfiles-T133-result-evidence-check-a01

Lineage: promotion of the orchestrator glue `result-evidence-check.sh` (RESULT evidence precheck: the worker's own full-suite base/candidate comparison and the head's CI as read by the orchestrator; M-20261020-04, C-113). Distinct from plan 024 P1-5's `dotfiles-T133-result-precheck-*` lineage (PR #411).

- 2026-10-20T10:00Z-11:04Z: a first draft was authored by the review profile under the id `dotfiles-T133-result-precheck-a01`, which is P1-5's lineage; its `cp` overwrote the dispatched a01 text (restored from HEAD at 11:13Z, 109 lines, sha 05caa77f…) and its C-80 review was filed under that id (M-20261020-06, C-116: pre-send.sh now refuses an id in use). Draft kept as `result-evidence-check-a01-draft-under-wrong-id.md` (90 lines, sha 99c37ca7…).
- 2026-10-20T11:05Z-11:09Z: C-80 round 1 of that draft (`…-result-evidence-check-a01-text-security-99c37ca.md.last.md`, moved) `Verdict: incorrect`, four P2: (1) line 76 the test launcher puts mise shims (`command -v uv`) first while line 68 needs a PATH-selected fake `gh`; (2) line 25 `test_validation_at_head` cannot close the in-process-effects row; (3) line 63 the CI query binds no repository (`GH_REPO`, a fork with the same sha); (4) line 63 an empty run list passes and the 20-run page is not complete. The glue took (3) and (4) at once (`GH_REPO= gh run list --repo mryfmo/dotfiles --limit 100`, empty list refused).
- 2026-10-20T11:15Z: the text is re-authored under this id by the review profile (`result-evidence-check-a01-prompt.md`) with the four findings closed in the text; C-80 round 2 follows, then pre-send and dispatch to an idle Claude seat.

text-security:99c37ca:1	shims-on-path
text-security:99c37ca:2	happy-path-closing-test
text-security:99c37ca:3	repo-binding
text-security:99c37ca:4	empty-result-passes
- 2026-10-20T11:22Z-11:26Z: re-authored text installed (99 lines, self cap 110, pre-send OK, checker OK, C-107 cap sentence 70/200), sha256 72882ac26eee47a82239bf816ebdb3512103cb5fd845458642966674934cfef6. C-80 round 2 (`…-text-security-72882ac.md.last.md`) `Verdict: incorrect`, five new P2 after the four of round 1 were closed: (1) line 25 the hostile-`GIT_DIR` test covers one of the `GIT_*` overrides; (2) line 27 sanitising the test launcher binds no production executable (`git`, `python3`, `gh` resolve through PATH at run time); (3) line 61 reading the shared repository honours replacement refs; (4) line 64 `GH_HOST` still selects the host; (5) line 77 the sandbox-only instruction has no effective-policy prerequisite. Every one is a restatement of the trusted-execution contract (design 5.14 items 2, 7, 9) that the contract tests (#436) and the executable binding (#431) are landing on main. HOLD under D-024-37: the text is not amended again (nine contract findings over two rounds would be the third repetition of one class, STOP S1); it is re-plannied as a contract-referencing text once #436 and #431 merge, and the glue serves the orchestrator meanwhile.

text-security:72882ac:1	contract-restatement
text-security:72882ac:2	contract-restatement
text-security:72882ac:3	contract-restatement
text-security:72882ac:4	contract-restatement
text-security:72882ac:5	contract-restatement
re-plan: contract-restatement (rows text-security:72882ac:1-5; the four round-1 rows were closed by the re-authoring) — specification: a task text for a tool that runs git and gh names the trusted-execution contract by reference (design 5.14 items 2, 7, 9 and the contract tests of #436, the binding of #431) and states only what is specific to the tool; design: the text's threat rows for environment and executables point at the shared contract tests, not at per-text restatements, so a C-80 review judges the tool-specific rows only; implementation: after #436 and #431 merge, one re-authoring that replaces lines 25, 27, 61, 64 and 77 with references to the landed tests and binding; verification: C-80 round 3 reports no contract-class finding, and pre-send passes.
- 2026-10-20T12:20Z: lineage withdrawn (D-024-46): it was outside plan 024, overlapped P1-5, and its C-80 reviews were out of C-80's scope (security: false). The two checks move to `dotfiles-T133-result-precheck-followup-a01` as items; the glue stays orchestrator-side. The task text `.orchestration/tasks/dotfiles-T133-result-evidence-check-a01.md` is removed from the tasks directory (never dispatched) and kept under `.agents/worklog/orchestrator-glue/result-evidence-check-a01-text.md`.
