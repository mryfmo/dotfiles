---
format: 2
task_id: dotfiles-T128-process-rules-redesign-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-process-rules-redesign-a01 — the reset redesign for PR #318's threat-table rule

Drafted 2026-10-11 05:1xZ by the orchestrator seat. Plan 006 S1 and design INV-6 fired on `dotfiles-T128-process-rules-a01` (PR #318, worker `claude-standard-dot-a003`): the same finding class three times on one artifact (the Codex Bot: thread 4240290387 "the disposition regex accepts an empty payload" on `9a46c3c4`, 4240321113 "`residual: none`" on `ac3794f9`, 4240334094 "`out-of-scope: none` or a wrong owner" on `6635030f`), and Bot P1 on two heads after the first RESULT. INV-6 releases the stop only through a reset record naming a redesign whose design RESULT comes from an identity other than the task's author. You are that identity; this is read-only.

## Orchestrator's re-examination (input, not the answer)

The rule text in `home/dot_agents/skills/agmsg-orchestration/SKILL.md` ("Review and integration invariants", the `threat_table` bullet at the PR head) states a grammar in prose: a regex for `disposition`, then fix by fix a non-empty payload, then "not `none`" for `residual`, then the same for `out-of-scope`. Prose cannot close a grammar, and each fix invites the next probe. The operator's rule is that a repeated finding means the specification is wrong, not that another patch is due.

## What to produce

The replacement text for that one bullet (and, if needed, the matching sentence in `AGENTS.md` "### Orchestration records and trust-boundary code" and the test tokens in `tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_a_trust_boundary_task_carries_a_threat_table`), under these constraints:

1. The prose names the three forms and what each must carry (`closed: <a tests/<file>::<name> selector>`, `residual: <the compensating control>`, `out-of-scope: <the owning task id>`) and carries no regex and no enumeration of forbidden payloads.
2. Shape is validated by `schemas/task.json` in wave V1 (state the three shape rules V1 must implement: a `closed` selector names a test present in the PR tree; an `out-of-scope` owner is a task id in the design's `implementing_tasks`; a `residual` payload is a non-empty sentence). Substance is judged by the task-file reviewer, the Bot and the auditor against the diff (a `closed` row whose test does not close it; a `residual` row whose control does not exist), as `AGENTS.md` already asks.
3. Smaller than the current text where possible; every sentence testable by a token assertion.

Read the current text on the PR head (`git -C ~/Workspace/dotfiles show origin/docs/regime-pattern:home/dot_agents/skills/agmsg-orchestration/SKILL.md`, same for `AGENTS.md` and the test module, after `git fetch`) and the three Bot threads (`gh api repos/mryfmo/dotfiles/pulls/comments/<id>` if `gh` works from your seat; the thread titles above otherwise).

## Output

`.orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md` in the main checkout with the usual header, the replacement paragraph(s) verbatim in fenced blocks, one line `redesign_sha256: <sha256 of this receipt file's fenced content>` is not required; the receipt's whole-file sha256 goes into your RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a01 status=ready_for_review verdict=redesign receipt=<path> receipt_sha256=<sha256> note=<one line>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator writes the reset record naming your RESULT and relays the text verbatim to the worker as the redesign task. max_turns=4. Forbidden: editing tracked files; branches; PRs.
