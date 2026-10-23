---
id: M-20261021-04
date: 2026-10-21
classes: [unhashed-requirement-change, hand-typed-chain]
severity: P2
---

# TASK 2863's note waived a probe the task text requires

**What happened.** The dispatch line of `dotfiles-T133-worker-sandbox-exclusions-a02` (TASK 2863, 2026-10-20 14:21Z) carried the note "no sandboxed dispatch probe required" while the dispatched text (line 103) requires the worker's Codex probe; amendment 1 changed only the cache setup. The task-level audit of c8c712f1 (PR #448) reported the inconsistency between the executed procedure and the reviewed contract (finding 2).

**What the rules say.** C-119 (a revise that changes a requirement carries `amendment=N` with the hashed text), C-123 (a pinned base changes only through a hashed amendment); the text is the contract, the line is addressing.

**Why the rules did not fire.** pre-send.sh's caller-contradiction check (C-112) reads the text; nothing compares the dispatch line's `note=` against the text's requirements. This is the third instance of a requirement changed by a message rather than an amendment (C-119, C-123, now the dispatch note), so the class is re-planned rather than patched.

**Mechanism.** C-125: send-task.sh refuses a TASK or ACCEPTANCE line whose `note=` or `reason=` names a requirement of the text as waived, skipped, not required or replaced (keyword check against the text's Check and Completion sections) unless the line carries `amendment=N`; the orchestrator writes the requirement change into the text and hashes it. Until the repository version (R1-9), the glue version runs on every send.
