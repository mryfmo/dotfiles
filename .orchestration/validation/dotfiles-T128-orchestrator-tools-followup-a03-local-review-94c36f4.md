---
task: dotfiles-T128-orchestrator-tools-followup-a03
head: 94c36f40e3d21822020cd20d704844595a9ca2de
pr: 374
base: 58303c37a2ac7854ba7f8d4032b5ee2b9c28776e
started: 2026-10-17T04:56:25Z
finished: 2026-10-17T05:01:27Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Bootstrap the same cache used by the isolated probe — scripts/orchestrator/dispatch.sh:217-219
- [P2] Reject one-row history windows before sending — scripts/orchestrator/dispatch.sh:340-341

```text
Cache initialization can leave TASK dispatch permanently blocked, and an accepted window setting guarantees post-send recording failure. Shell syntax and read-only reproductions were checked; the full test suite was not run in the read-only sandbox.

Full review comments:

- [P2] Bootstrap the same cache used by the isolated probe — scripts/orchestrator/dispatch.sh:217-219
  When `UV_CACHE_DIR` or `XDG_CACHE_HOME` selects another cache and the pinned home cache is empty, the recommended `make validate-agent-assets` warms the caller-selected cache, not the one dispatch uses. Retrying therefore still exits 2 and blocks every TASK. The new real-uv tests also encounter this mismatch on fresh runners with relocated caches. Provide a bootstrap command that uses the same pinned cache, interpreter and index settings while preserving dispatch's offline isolation.

- [P2] Reject one-row history windows before sending — scripts/orchestrator/dispatch.sh:340-341
  With `BUS_READ_WINDOW=1` and a nonempty bus, this validation accepts the setting, but the alignment can only try `j=0`: a different new row produces no fit, while an identical row reports no addition. Every successful dispatch consequently sends the message and then exits 1 without recording it. Reject windows smaller than two before sending, rather than discovering this unsupported configuration after delivery.
Cache initialization can leave TASK dispatch permanently blocked, and an accepted window setting guarantees post-send recording failure. Shell syntax and read-only reproductions were checked; the full test suite was not run in the read-only sandbox.

Full review comments:

- [P2] Bootstrap the same cache used by the isolated probe — scripts/orchestrator/dispatch.sh:217-219
  When `UV_CACHE_DIR` or `XDG_CACHE_HOME` selects another cache and the pinned home cache is empty, the recommended `make validate-agent-assets` warms the caller-selected cache, not the one dispatch uses. Retrying therefore still exits 2 and blocks every TASK. The new real-uv tests also encounter this mismatch on fresh runners with relocated caches. Provide a bootstrap command that uses the same pinned cache, interpreter and index settings while preserving dispatch's offline isolation.

- [P2] Reject one-row history windows before sending — scripts/orchestrator/dispatch.sh:340-341
  With `BUS_READ_WINDOW=1` and a nonempty bus, this validation accepts the setting, but the alignment can only try `j=0`: a different new row produces no fit, while an identical row reports no addition. Every successful dispatch consequently sends the message and then exits 1 without recording it. Reject windows smaller than two before sending, rather than discovering this unsupported configuration after delivery.
```
