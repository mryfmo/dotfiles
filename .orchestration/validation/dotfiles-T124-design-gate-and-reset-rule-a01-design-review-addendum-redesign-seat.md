---
written_at: 2026-10-10T09:20:00Z
reviewer: claude-review-dot-a002
profile: review
session: 76641dce-e0d5-4654-b475-8f2ebdbf8cc9
design: .orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md@d31c1bb73c9568e6d65b8a55d9160d1f32d3b0167405297b85466928d38ffe0f
task: dotfiles-T124-design-review-a01
kind: addendum
operator_direction: 2026-10-10 「提案の方法で」(the redesign runs on a separate seat; the orchestrator's own effort is never changed mid-session)
---

# Addendum: the design redo after an INV-5 reset runs on a `redesign` seat

Operator question (2026-10-10): when findings repeat, can the orchestrator's effort be raised to xhigh for the redo and returned to high afterwards, mechanically. Answer given and adopted by the operator: not by changing the orchestrator session; the redo runs on a separate seat whose profile carries the higher effort, so the raise and the return are the seat's lifetime. Reasons recorded in the conversation: T119's failure was a wrong premise held by one context, and T124 round 1 showed that an independent context at the same model and effort found 7 of 8 invariants wrong, so independence is the lever; INV-3 needs the redo's provenance in agmsg history, which a seat gives and a session-local effort change or a subagent does not; the seat is the regime's existing unit of model and effort control, so nothing needs to be "returned".

Claude Code facts checked for the record (code.claude.com/docs, 2026-10-10): `effortLevel` hot-reloads but the `--effort` launch flag herdr-agents passes outranks it; hooks cannot change effort; effort changes keep the prompt cache on Fable 5.1 since v2.1.260 (model changes do not); skill and subagent frontmatter `effort:` is a per-task override. None of this is needed for the seat approach; it is why the session-local approaches were set aside.

## Changes to fold into design v4

1. `model_profiles.redesign` in `home/dot_agents/agent-config.yaml`: `claude: { model: claude-fable-5-1, effort: xhigh }` and a codex entry as the renderer requires (mirror `deep`'s codex model at `xhigh`). Identity convention already encodes the profile: `claude-redesign-dot-aNNN` / `codex-redesign-dot-aNNN`, so the profile is machine-readable from the identity name in history.
2. INV-5 release path, made concrete: the `…-design-reset.md` record carries `redesign_task=<id>` and `redesign_seat=<identity>`; the orchestrator seats the redo with `herdr-agents --add-worker .claude/worktrees/redesign --kind claude --profile redesign` and dispatches an `AGMSG-TASK` of a new `kind: design` whose deliverable is the superseding design task file (`format: 2`, written at its main-checkout path through the permission gate, as review receipts are today) and an `AGMSG-RESULT`. The orchestrator never writes the superseding design itself. The gate and the validator accept a reset only when history holds that RESULT from an identity whose name carries `-redesign-`, before the implementing `AGMSG-TASK`; the design then goes through INV-3's review by a `-review-` identity as any design does. The seat is removed with `--remove-worker` once the design RESULT is accepted.
3. INV-1 `kind` gains `design` (no PR, same front matter minus `waves`).
4. Stop gate reason line (wave 3a) names the command: `reset rule reached for <task id>: write .orchestration/acceptance/<id>-design-reset.md and seat the redo with herdr-agents --add-worker .claude/worktrees/redesign --kind claude --profile redesign`.
5. Rule text `home/dot_config/claude/rules/model-selection.md`: add "a design redo after an INV-5 reset runs on the `redesign` profile seat; the orchestrator's model and effort never change mid-session"; correct the cache sentence to "a mid-session model switch invalidates the prompt cache (an effort change keeps it on Fable 5.1)". SKILL Orchestrator Playbook gets the reset procedure once; the rule cites it.
6. INV-8 test: a reset record whose `redesign_seat` has no matching `-redesign-` RESULT in history is refused.

## Waves

Items 1, 3 and 5 are prose and manifest and fit wave 1 (or a small wave 1b if wave 1 is already dispatched); item 2's gate and validator parts go to 2b and wave 1 respectively; item 4 to 3a. Routing note for item 1: `model_profiles` is not one of the Claude- or Codex-boundary blocks the routing rule names, but it renders into both runtimes' configs; operator decides, default a Claude seat.

Effort for the `redesign` profile: `xhigh` per the operator's original ask; the operator may lower it later in the manifest without any other change.
