---
id: M-20261020-08
date: 2026-10-20
classes: [checker-exit-unchecked]
severity: P2
---

# A TASK was dispatched after pre-send had refused the text (second occurrence of the M-20261020-03 class)

**What happened.** Pasting the Checks block into `dotfiles-T133-worker-sandbox-exclusions-a01.md` took the file from 124 to 129 lines against its own cap of 125. pre-send.sh refused (`over self cap: refused`, exit 1), but the dispatch step piped its output through `tail -n 3`, never read the exit code, computed the sha of the refused bytes and dispatched TASK 2840 to a013 (read at 13:31:24Z). Amendment 1 (the cap sentence 125 -> 135, one number) followed through the new gate.

**What the rules say.** C-100 and M-20261020-03: the dispatch is preceded by the text's checks on the final bytes, and a failed step stops the chain of steps; the Checks block is part of the dispatched bytes, so the cap must leave room for it.

**Why the rules did not fire.** The mechanism of M-20261020-03 was a convention (`|| exit 1`, positive step checks) inside ad-hoc shell blocks, not a tool: a new block written in a hurry omitted it. pre-send.sh's self-cap check also counts the Checks block the orchestrator pastes after the author lines, so a text sized to its author lines fails after the paste.

**Mechanism.** `send-task.sh` (C-118) is the only path to dispatch a TASK line: pre-send on text and line, exit-code gate, line sha equal to text sha, then dispatch and the stored message id. Its first run caught its own defect (a `task_sha256=` grep that matched `previous_task_sha256=`) by refusing, which is the behaviour wanted. The review-profile briefs now ask for a self cap with room for the Checks block (the a06 text's 246 of 250 is the model).
