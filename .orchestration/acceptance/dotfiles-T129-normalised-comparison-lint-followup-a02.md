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
  "task": "dotfiles-T129-normalised-comparison-lint-followup-a02"
}
---

# Acceptance record: dotfiles-T129-normalised-comparison-lint-followup-a02

Owner task of a merged lineage; its owned rows are read from the predecessor acceptance record at dispatch. security: false; dispatched under D-024-25 to keep the seats on disjoint work while P1-15 completes.

- 2026-10-19T11:3xZ: dispatched to claude-standard-dot-a008 (worker-f; sha cb4a8f34d94c1905d7a759d26c087491908c057fc7257520af64b14f702801fb); counters pasted; no C-80 (security: false).
- 2026-10-19T11:39:00Z: a008 `status=question` q1 (the caps of the 10-17 text are infeasible on 51ba5801: the script is already 227 lines and the tokenizer re-plan adds code) q2 (the record holds four Bot rows, not ten). Root cause: a text written on 10-17 was dispatched without re-measuring its caps or re-reading its rows against today's main (a premise not probed; proposal 3). Amendment 1 (sha 4198ddc1b8b5e30a66c89ba01e4051a65758806f6d15d0e5dd495876902fca98): script-length cap removed; at most 350 changed lines outside tests excluding the baseline (227 + about 100 + margin); tests 1000; the 13 ids confirmed (four Bot rows, nine audit rows, two process rows). Dispatched 11:4xZ.
