# AGMSG-TASK dotfiles-T128-design-review-a01

Drafted 2026-10-11 by the orchestrator seat (`claude-deep-dot`, w5:p1). A design review on the `review` profile, in a separate context, of the T128 regime-v3 design before any implementing task is dispatched. The design was drafted by the orchestrator under a recorded bootstrap exception (operator decision 2026-10-11), so this review is the only independent check it gets before dispatch: your findings against the orchestrator's reasoning, thresholds, scope or honesty are expected. Read-only: no repository file changes, no branch, no PR. Kind: review; Claude seat on the `review` profile in `.claude/worktrees/worker-d`.

## What to review

`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` (front matter: threat model R1-R8, trust anchors, INV-1..INV-12, premises; body: finding, root causes, principles, audit stages, enforcement map, waves, thresholds, residuals).

Context, in this order: `.orchestration/validation/dotfiles-T128-regime-v3-a01-research/baseline.md` (the measured numbers), `…/practice-evidence.md`, `…/claude-code-factsheet.md`, `…/codex-factsheet.md`, `…/github-factsheet.md` (fact sheets compiled 2026-10-11 from official pages; each bullet cites its URL), the superseded designs `.orchestration/tasks/dotfiles-T126-regime-v2-a01.md` and `.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md` with their receipts, the two reset records `.orchestration/acceptance/dotfiles-T124-wave1-task-validator-a01-design-reset.md` and `…-wave3b-audit-grammar-a01-design-reset.md`, and the scripts the enforcement map names: `scripts/require-crit-review.py`, `scripts/agent-stop-gate.sh`, `scripts/check-regime-boundary.sh`, `scripts/pr-feedback.py`, `.github/workflows/test.yaml`, the `--audit` path in `home/dot_local/bin/common/executable_herdr-agents`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`. The closed reference branches `origin/feat/task-validator` (PR #313) and `origin/feat/audit-grammar` (PR #314) show what the reset abandons; read them only as far as question 5 needs.

## Standing

Treat every claim in the design as untrusted until checked: against the fact sheets (spot-check at least the Claude Code headless and hooks pages, the Codex hooks page, and GitHub's required-status-checks troubleshooting page with WebFetch), against the scripts (does `require-crit-review.py` really need only history-anchored additions? can `agent-stop-gate.sh` count `amendment=` and `status=question` from the rows it already reads? does the `changes` job pattern in `test.yaml` let a `pull_request_target` job report success for an `.orchestration`-only diff?), and against the baseline numbers (recompute at least one row from `history.sh dotfiles-conformance`).

## Questions, each with a verdict and a reason

1. Per invariant INV-1..INV-12: testable as written; enforcement point the earliest mandatory one; closes the threat it maps to. `INV-n: accepted` or `INV-n: rejected: <what is wrong and what would be right>`.
2. Which failure modes of T118, T119 and T124 W1/W3b (amendment accretion, bespoke parser bypass loop, oversized PR, waiver instead of reset, orchestrator self-disposition, audit as serial queue) still pass under this design? Name each with the invariant that should catch it.
3. `pull_request_target` as the main-pinned check (trust anchor 3, INV-1/2/8, residual 2): is the stated safety discipline (read PR files as data, check out main's scripts, `contents: read`, never execute PR content) sufficient on a public repository, and is anything in the `regime` job as described executable from the PR?
4. The reset rule and the redesign author (INV-6, P6): are the counts the right signals, can the orchestrator game them (split rounds, relabel amendments, re-dispatch under a new id, answer a question as a "note"), is the bootstrap exception under which this very document was written acceptable and bounded, and is dropping the `redesign` profile (T124 v4) in favour of "another context on the review profile" a loss?
5. Ponytail check on the waves: is each wave within INV-2's caps as described, is anything in V1-V6 still a bespoke mechanism where a library, platform feature or existing script would do, and what from PR #313 or #314 should be salvaged that the design drops?
6. Audit staging (section 4): are the stages and tiers right, is "once per RESULT head, never for evidence-only revisions" safe given the literature the design cites, and is the auditor's input set (invariants, premises, orchestrator artifacts) complete?
7. The premises block (INV-4): check at least three premises by re-running their commands or re-fetching their pages; report any that do not hold.
8. Anything the design should not do (over-reach, a rule that will block legitimate work, a rule the machinery cannot enforce reliably, a threshold the baseline contradicts).

## Output

Write `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md` in the main checkout (through the permission gate, the allowed artifact path) with front matter `reviewed_at: <UTC ISO>`, `reviewer: <your agmsg identity>`, `profile: review`, `session: <session id>`, `design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@<whole-file sha256>`, `design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)`, `task: dotfiles-T128-design-review-a01`, `round: 1`; then one line per invariant; then the answers to questions 2-8 with `file:line` or URL references; then a final line `Design verdict: accept | revise | reject`. Keep it under 400 lines; no other file. Then send `AGMSG-RESULT v1 task_id=dotfiles-T128-design-review-a01 status=ready_for_review verdict=<accept|revise|reject> receipt=<path>` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w5:p1 "<single line>"`. max_turns=10.

Forbidden: editing any tracked file; creating a branch or PR; running installers or `make update`; anything outside the sandbox except writing the receipt and the dispatch. A question for the orchestrator goes as `AGMSG-PONG v1 task_id=dotfiles-T128-design-review-a01 status=question note=<one line>`; proceed on your stated default without waiting.

## Paths

Every path in this task resolves in the main checkout `~/Workspace/dotfiles` (its `main` at `d29ce4c1`), which is read-only for you except the receipt. Your worktree `worker-d` sits on an old branch; do not read scripts from it.

## Round 2 (orchestrator, 2026-10-11)

Round 1 accepted (verdict `revise`; every finding adopted). Review v2 of the same design file (whole-file sha256 in the AGMSG-TASK `design_sha256=`), as its section 10 asks: confirm each round-1 correction is applied as written (F1-F9 and every INV rejection), check that nothing new in v2 reopens a finding, spot-check the reset records' corrected header lines, and answer per invariant. Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round2.md` with `round: 2` and `previous:` naming the round-1 receipt. Same output rules, same RESULT line with `round=2`. max_turns=8.

## Round 3 (orchestrator, 2026-10-11)

Round 2 accepted (verdict `revise`; its five section-4 edits adopted as v3). Confirm each as a diff confirmation against v3 (whole-file sha256 in the AGMSG-TASK `design_sha256=`): the `implementing_tasks` map and the design-on-main precondition (INV-2), `revise.yaml` beside a byte-identical task.md (INV-3, INV-8, INV-12, V3c, V2b), the question threshold and the audit-JSON record match (INV-6), V3a as an operator PR with all hook counting and V3b/V3c routed by source, the legacy list excluded from the cap, the `workflow_dispatch` premise, the stage-3 sentence, the latest-TASK token in INV-1. Per invariant and `Design verdict:` as before. Receipt: `.orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round3.md` with `round: 3` and `previous:` the round-2 receipt. RESULT with `round=3`. max_turns=6.
