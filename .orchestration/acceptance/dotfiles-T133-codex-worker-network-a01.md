---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-codex-worker-network-a01"
}
---

# Acceptance record: dotfiles-T133-codex-worker-network-a01

The Codex-side item of plan 024 P1-15 (D-024-17a: the two Codex worker profiles gain sandbox network access so gh and git push run inside the sandbox), split out of worker-write-boundary-a01 for routing (a Codex seat must not edit its own boundary source; a Claude seat implements it). Text designed by the review-profile context (`.agents/worklog/orchestrator-glue/redesign/codex-net-a01.md`, prompt `codex-net-a01-design-prompt.md`).

- 2026-10-19T06:29Z: design output installed as the task text; checker OK; measurements added (C-79: source analogue 2 renderer lines + 1 manifest line → about 20, cap 40; test analogue 37 lines).
- 2026-10-19T06:47Z: C-80 first review (`…-text-security-cf5efd5.md`): `Verdict: incorrect`: P1 (the dispatch prerequisite was P1-15 merged, not installed and the seat re-seated, so a Claude worker could keep the platform gh exclusion and old hook bindings at first execution); P2 (the modify-script merger replaces managed tables wholesale, so adding the network table could drop writable_roots and the exclude_* keys while the scoping test passes). Both fixed in the text: deployment readiness as the prerequisite with evidence pasted in Checks; a preservation fixture test added to the closed rows; test cap 100 (two tests of the 37-line shape).
- 2026-10-19T07:19Z: C-80 second review (`…-text-security-5076362.md`): `Verdict: correct`. Dispatch waits for its prerequisite: P1-15 merged, applied by `make update`, effective settings recorded, the taking seat re-seated.
text-security:cf5efd5:1	deployment-readiness
text-security:cf5efd5:2	table-merge-preservation
