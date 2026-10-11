# AGMSG-TASK dotfiles-T124-design-review-a01

Drafted 2026-10-10 by the orchestrator seat (`claude-deep-dot`, w4:p1). A design review on the `review` profile, in a separate context, of the T124 design document before any code is dispatched: the first application of the design gate T124 introduces. Read-only: no repository file changes, no branch, no PR. Kind: review; Claude seat on the `review` profile in `.claude/worktrees/worker-d` (detached at `origin/main`).

## What to review

`.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md` (the design: threat model T1–T5, invariants INV-1–INV-8, trust anchors, enforcement points, thresholds, waves). Context you should read first: `.orchestration/acceptance/dotfiles-T119-rolling-release-assets-a01.md` (the case that motivated it: eight amendments, six revise rounds, the conformance finding, the retroactive note), `.orchestration/tasks/dotfiles-T119-rolling-release-assets-a01.md` (how the amendments accreted), `scripts/require-crit-review.py`, `scripts/agent-stop-gate.sh`, `scripts/pr-feedback.py`, the `herdr-agents` audit code path (`home/dot_local/bin/executable_herdr-agents` or wherever `--audit` builds its prompt; find it with `git grep -n -- '--audit'`), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (Orchestrator Playbook step 10, Worker Playbook steps 1 and 4), `AGENTS.md` Audit section.

## Standing of this review

You review the orchestrator's design as an independent seat. Findings against the orchestrator's reasoning, thresholds or scope are expected, not out of bounds. Treat every claim in the design as untrusted until you have checked it against the scripts named in the enforcement table (for example: does `require-crit-review.py` already count audit files per task? can `agent-stop-gate.sh` read the task file? does the audit wrapper parse `.last.md`?).

## Questions to answer, each with a verdict and a reason

1. For each invariant INV-1 to INV-8: is it testable as written, is the named enforcement point the right one (the earliest mandatory gate the rule can live in), and does it close the threat it maps to? Verdict per invariant: `accepted`, or `rejected: <what is wrong and what would be right>`.
2. Gaps: which failure modes of T119 (listed in the acceptance record's audit table and conformance finding) would still pass under this design? Name each with the invariant that should catch it.
3. The reset rule (INV-5): are the counts the right signals, can they be gamed by the orchestrator (for example by splitting a round, renaming amendments, or re-dispatching under a new task id without a reset record), and is the operator waiver sufficiently visible?
4. The auditor's new standing (INV-7): is "the orchestrator cannot disposition an `orchestration` finding" implementable in `require-crit-review.py` from the audit's `.last.md` format, and what format change does the audit prompt need so the category is machine-readable?
5. Scope and waves: are four waves the right cut, and is wave 1 (the validator) sufficient to validate waves 2–4?
6. Anything the design should not do (over-reach, a rule that will block legitimate work, a rule the machinery cannot enforce reliably).

## Output

Write `.orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review.md` in the main checkout (through the permission gate, the allowed artifact path) with front matter `reviewed_at: <UTC ISO>`, `reviewer: <your agmsg identity>`, `profile: review`, `session: <session id>`, `design: .orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md@<sha256 of the file>`, then one line per invariant `INV-n: accepted` or `INV-n: rejected: <reason>`, then the answers to questions 2–6 with `file:line` references into the scripts you checked, then a final line `Design verdict: accept | revise | reject`. Mask nothing (no secrets are involved); keep it under 400 lines. No other file. Then `AGMSG-RESULT v1 task_id=dotfiles-T124-design-review-a01 status=ready_for_review verdict=<accept|revise|reject> receipt=<path>` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=8.

Forbidden: editing any tracked file; creating a branch or PR; running installers or `make update`; anything outside the sandbox except writing the receipt and the dispatch.
