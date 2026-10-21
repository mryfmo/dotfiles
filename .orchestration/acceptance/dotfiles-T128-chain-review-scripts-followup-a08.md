---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "hash-binding",
      "id": "audit:23f5144:1"
    },
    {
      "class": "worker-sandbox-discipline",
      "id": "audit:23f5144:2"
    },
    {
      "class": "tool-environment",
      "id": "audit:23f5144:3"
    },
    {
      "class": "excluded-command-trusts-sandbox-context",
      "id": "audit:23f5144:4"
    }
  ],
  "pr": null,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T128-chain-review-scripts-followup-a08"
}
---

# Acceptance record: dotfiles-T128-chain-review-scripts-followup-a08
- 2026-10-20T09:35Z: reset text of the a07 lineage (D-024-41; Item 3: review content from a private clone; security: true) written whole by the review profile (`t128-a08-reset-prompt.md`), 102 lines, pre-send OK (sha256 23f5144a…). C-80 round 1 (`…-text-security-23f5144.md`) `Verdict: incorrect`, four P1 of the trusted-execution family: a preserved review cache lets a planted `head:`/`findings: 0` artifact bypass Item 3; a same-UID worker can write the private clone under TMPDIR (mode 0700 does not exclude same-UID); no bound clean parent at chain-integrate.sh's call site; the Linux `gh *` exclusion contradicts the sandbox premise. Disposition: D-024-37 applies: the text is held until #436 (the trusted-execution contract) and #431 (P1-15) land, then references them (C-88) and takes one round; PR #439 stays open at a644a7d9; a011 holds (PING `t128-a07-hold2.txt`).
text-security:23f5144:1	hash-binding
text-security:23f5144:2	worker-sandbox-discipline
text-security:23f5144:3	tool-environment
text-security:23f5144:4	excluded-command-trusts-sandbox-context

