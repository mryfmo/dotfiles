---
task: dotfiles-T128-orchestrator-tools-followup-a03
head: f364b7d478ab100d56c80b6935b90ffcf72a99ab
pr: 374
base: 7722704731b6cd6155fbca51c61ff5a710eaacbd
started: 2026-10-17T05:16:59Z
finished: 2026-10-17T05:21:27Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Exclude impossible eviction from underfull history windows — scripts/orchestrator/dispatch.sh:303-304

```text
The history alignment can reject successful dispatches and omit their acceptance evidence. This was reproduced in memory using the actual recorder; Bash syntax and ShellCheck passed, but full tests were not run in the read-only sandbox.

Review comment:

- [P2] Exclude impossible eviction from underfull history windows — scripts/orchestrator/dispatch.sh:303-304
  When the bus contains two identical same-second rows, a successful send can be rejected: `pre=[A,A]` and `post=[A,A,B]` produces fits `j=1` and `j=2`. The second fit assumes eviction even though all three rows fit within the default 200-row window. Consequently, the recorder exits 1 after delivery and leaves the acceptance record unchanged; increasing the window cannot resolve this. Permit eviction only when the post-send window is full, and add an underfull-window regression test.
The history alignment can reject successful dispatches and omit their acceptance evidence. This was reproduced in memory using the actual recorder; Bash syntax and ShellCheck passed, but full tests were not run in the read-only sandbox.

Review comment:

- [P2] Exclude impossible eviction from underfull history windows — scripts/orchestrator/dispatch.sh:303-304
  When the bus contains two identical same-second rows, a successful send can be rejected: `pre=[A,A]` and `post=[A,A,B]` produces fits `j=1` and `j=2`. The second fit assumes eviction even though all three rows fit within the default 200-row window. Consequently, the recorder exits 1 after delivery and leaves the acceptance record unchanged; increasing the window cannot resolve this. Permit eviction only when the post-send window is full, and add an underfull-window regression test.
```
