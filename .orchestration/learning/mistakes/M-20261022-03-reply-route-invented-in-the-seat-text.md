# M-20261022-03 — the omp seat text invented a reply route three times instead of taking it from the bus contract

- When: 2026-10-22 08:46Z to 09:33Z (dotfiles-T129-hcom-omp-seat-a01, anchor rounds 1-3 by a011).
- What: round 1 named a TASK field (`reply_to`) no grammar defines; round 2 replied to the delivery's sender, which fails while the orchestrator is an external hcom sender (`ext_<name>` is not deliverable); round 3 replied on the team thread, which errors "Thread has no members" because nothing in C-1's text seeds the thread.
- Root cause: the orchestrator answered C-1's worker question Q2 with a thread design ("hcom-dispatch sends --thread team, bus-history reads msg_thread = team") as a PING and then treated that answer as C-1's text; C-2 was written against the PING, not against C-1's anchored bytes, and each round patched the seat side of a two-sided contract without reading hcom's membership rule (send.rs).
- Mechanism: a reply route, like any protocol property, lives in the bus text (C-1) with a fixture-store test that sends and reads both directions; a seat text cites it by task id and adds only its own half; an orchestrator answer that changes a protocol becomes an amendment of the owning text before any dependent text is written. Codified as C-135.
- Cost: three anchor rounds (about 45 minutes of the review seat) and the C-59 stop on the text.

classes: [reply-address, prose-specified-mechanism]
