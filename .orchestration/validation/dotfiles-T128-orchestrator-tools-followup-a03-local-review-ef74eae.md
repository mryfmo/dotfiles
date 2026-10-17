---
task: dotfiles-T128-orchestrator-tools-followup-a03
head: ef74eaea9a94bff388b7c1027551a57797407b2f
pr: 374
base: f7847616970d6bd83739a75a65ad8f7c35e91462
started: 2026-10-17T00:37:46Z
finished: 2026-10-17T00:42:18Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Allow concurrent rows to interleave in timestamp-ordered history — scripts/orchestrator/dispatch.sh:283-284
- [P2] Exclude impossible evictions from underfull history windows — scripts/orchestrator/dispatch.sh:284-285

```text
The new alignment rejects valid sends under both concurrent timestamp-ordered insertion and underfull histories with repeated rows, leaving delivered messages unrecorded. Syntax and in-memory checks were performed; the full test suite was not run in the read-only environment.

Full review comments:

- [P2] Allow concurrent rows to interleave in timestamp-ordered history — scripts/orchestrator/dispatch.sh:283-284
  When another seat timestamps a message before the pre-send read but commits it afterward, agmsg's `storage_history` can insert that row before existing rows because it sorts by timestamp. For example, `pre=[B]` can become `post=[A,B,C]`, where C is this dispatch. This expression finds no fit, so the successfully delivered C is left unrecorded. Align retained rows without assuming all new messages form a suffix, or use stable bus sequence identifiers.

- [P2] Exclude impossible evictions from underfull history windows — scripts/orchestrator/dispatch.sh:284-285
  When a short history contains identical same-second rows, a valid append can be rejected as ambiguous. With the default window of 200, `pre=[A,A]` and `post=[A,A,C]` produce fits `[1,2]`, although a three-row history cannot have evicted any rows. The recorder therefore exits 1 and leaves the delivered C unrecorded. Pass the window capacity into the recorder and require zero evictions whenever the post-send history is below that capacity.
The new alignment rejects valid sends under both concurrent timestamp-ordered insertion and underfull histories with repeated rows, leaving delivered messages unrecorded. Syntax and in-memory checks were performed; the full test suite was not run in the read-only environment.

Full review comments:

- [P2] Allow concurrent rows to interleave in timestamp-ordered history — scripts/orchestrator/dispatch.sh:283-284
  When another seat timestamps a message before the pre-send read but commits it afterward, agmsg's `storage_history` can insert that row before existing rows because it sorts by timestamp. For example, `pre=[B]` can become `post=[A,B,C]`, where C is this dispatch. This expression finds no fit, so the successfully delivered C is left unrecorded. Align retained rows without assuming all new messages form a suffix, or use stable bus sequence identifiers.

- [P2] Exclude impossible evictions from underfull history windows — scripts/orchestrator/dispatch.sh:284-285
  When a short history contains identical same-second rows, a valid append can be rejected as ambiguous. With the default window of 200, `pre=[A,A]` and `post=[A,A,C]` produce fits `[1,2]`, although a three-row history cannot have evicted any rows. The recorder therefore exits 1 and leaves the delivered C unrecorded. Pass the window capacity into the recorder and require zero evictions whenever the post-send history is below that capacity.
```
