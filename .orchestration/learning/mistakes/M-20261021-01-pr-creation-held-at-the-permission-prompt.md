---
id: M-20261021-01
date: 2026-10-21
classes: [gate-bound-mutation, idle-stall]
severity: P1
---

# A PR creation routed outside the sandbox waited six hours at the permission prompt

**What happened.** At 2026-10-20T15:12:57Z (00:12 JST) the orchestrator ran `gh pr create` for boundary 26 (#447) with the sandbox disabled, following the 2026-10-12 host note that `gh` fails TLS inside the sandbox. The auto-mode classifier did not approve the mutation and escalated to the human prompt; the operator was away, and the command returned at 21:26:58Z (06:26 JST). For six hours no other command ran: a013's committed head (PONG 2904, 15:13Z) was not transported, #447's CI result (`Agent assets` failure, 15:2xZ) was not read, a008's and a011's RESULTs were not integrated, the hourly progress update lapsed, and the a04 reset text's C-80 review did not start.

**What the rules say.** "Ask blocks, hold first" (session memory): before anything that can block on the operator, send the holds and start the independent work. Design 5.14 item 10 and the agmsg-orchestration rule: the orchestrator's own commands run inside its sandbox, with the unsandboxed path reserved for what the sandbox denies.

**Why the rules did not fire.** The TLS note was treated as current without re-measuring (run, do not recall applies to premises about the environment too); the previous unsandboxed `gh` reads in the same hour had returned at once, so the mutation was expected to return at once as well; the difference (the classifier approves reads and escalates mutations) was not in any note.

**Mechanism.** C-122: every GitHub call runs inside the sandbox (measured 2026-10-21 06:27 JST: `gh api`, `gh run list`, `gh pr create` rc 0 inside the sandbox; the job-log download needs `allowed_domains` for `results-receiver.actions.githubusercontent.com`); the memory note is corrected with the measurement; an unsandboxed call is used only for commands the sandbox denies (`herdr-agents`, `codex exec`) and never for a mutation while the operator is away; before any unavoidable gate-bound call the holds and PINGs go out first.
