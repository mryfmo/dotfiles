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

## Round 4 (orchestrator, 2026-10-11)

v4: V1 split into V1 (validation only) and V1c (CI check) on operator direction relayed by your PONG of 22:01Z; `implementing_tasks` gains `dotfiles-T128-v1c-regime-ci-check-a01: [INV-1]`; wave order V1, V1c, V1b, …; section 7 cap wording aligned with INV-2; receipt pointer round 4. Confirm those four edits as a diff check (whole-file sha256 in the AGMSG-TASK). Receipt `…-design-review-round4.md`, `round: 4`, `previous:` round 3. RESULT with `round=4`. max_turns=5.

## Round 5 (orchestrator, 2026-10-11)

v5 changes INV-3 only: `check=` is a test selector or `repro:<id>` with command and output in revise.yaml; the `ci:<job>` form is gone (Codex Bot thread 4239305441 on PR #316). Confirm as a diff check; receipt `…-design-review-round5.md`, `round: 5`, `previous:` round 4; RESULT with `round=5`. max_turns=4.

## Round 6 (orchestrator, 2026-10-11)

v6 adopts the Codex Bot's ten findings on boundary head c1e2582b: INV-1 (literal first segment, wildcard tier by prefix, legacy ids only under .orchestration/tasks/ on main), INV-2 (sentences byte-for-byte), INV-3 (previous_head in ACCEPTANCE and revise.yaml, cross-checked by the host gate), INV-5 (instruction root and schema from main, worktree as --add-dir data), INV-7 (a Claude and a Codex review per design hash), INV-12 (five gaming paths), stage-0 row, section 10. Confirm the six changed invariants and the new INV-7 against the Bot threads 4239399740-4239399761 on PR #316. Receipt `…-design-review-round6.md`, `round: 6`, `previous:` round 5; RESULT with `round=6`. A Codex read-only review of the same hash runs in parallel as `…-design-review-round6-codex.md`. max_turns=5.

## Round 7 (orchestrator, 2026-10-11)

v7 changes INV-7 as round 6 asked (Codex review = codex exec read-only under a codex-review identity with its own receipt and RESULT; the Bot review is swept feedback), the enforcement row and V4 accordingly, and adds the bare-mode skills premise. Confirm INV-7 and that nothing else moved. Receipt `…-design-review-round7.md`, `round: 7`, `previous:` round 6; RESULT with `round=7`. max_turns=4.

## Round 8 (orchestrator, 2026-10-11)

v8 answers the first Codex review (round 7, reject): INV-1, 3, 4, 5, 6, 9, 10, 12 changed as section 10 lists; one Codex P2 (bare-mode skills) refuted from the headless page. Review the eight changed invariants and section 9's one-account residual; say whether the ask-rule waiver is the strongest friction the machine offers or whether a stronger anchor exists. Receipt `…-design-review-round8.md`, `round: 8`, `previous:` round 7; RESULT with `round=8`. max_turns=6.

## Round 9 (orchestrator, 2026-10-11)

Supersedes round 8 if still open. v9 answers the second Codex review: INV-2 (1000-line cap under tests/), INV-3 (exact selector run on both heads in a required `revise-check` job), INV-4 (every premise dispositioned by each reviewer and the auditor), INV-5 (`.claude/**` refusal inside the invariant), INV-10 (draft PR created_at; `after` prerequisites), INV-12 (`main-tests` required job, V5c), two enforcement rows. Review the six changed invariants and the new V5c; disposition every premise in your receipt (holds|fails|unverifiable) as INV-4 now asks. Receipt `…-design-review-round9.md`, `round: 9`; RESULT with `round=9`. max_turns=6.

## Round 10 (orchestrator, 2026-10-11)

Supersedes round 9 if still open. v10 folds your round 8 (INV-1 owner and row, INV-5 stale-manifest wording, your sandbox-write-roots anchor) and Codex round 9 (INV-5 refusal restored after a silently failed edit, INV-12 contract-first with V0 main-tests first, the 2026-11-02 pull_request_target policy). Review INV-1, 2, 5, 6, 12, the new V0 and the contract-first rule; disposition every premise (holds|fails|unverifiable). Receipt `…-design-review-round10.md`, `round: 10`; RESULT with `round=10`. max_turns=6.

## Round 11 (orchestrator, 2026-10-11)

Supersedes round 10 if still open. v11 changes INV-12 (the union of your round-9 rule and Codex round 10: main modules for undeclared scripts, dormant REGIME_CONTRACT=1 contracts for declared ones, contract PRs required for design-tier waves) and INV-1 (record location is the guard, ask rule second layer). Review those two, V0 as rewritten, and confirm the rest unchanged; disposition every premise. Receipt `…-design-review-round11.md`, `round: 11`; RESULT with `round=11`. max_turns=6.

## Round 12 (orchestrator, 2026-10-11)

v12 adds your two INV-12 clauses (promotion by removing the decorator; an empty contract fails a design-tier implementation PR) to INV-12 and V0. Confirmation only; receipt `…-design-review-round12.md`, `round: 12`; RESULT with `round=12`. max_turns=4.

## Round 13 (orchestrator, 2026-10-11)

v13 adds the Codex round-12 clause to INV-12 (main-tests fails an implementation PR whose declared test module still carries a contract marker). Confirmation; receipt `…-design-review-round13.md`, `round: 13`; RESULT with `round=13`. max_turns=4.
