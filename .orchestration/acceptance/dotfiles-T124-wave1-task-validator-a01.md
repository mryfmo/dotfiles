# Acceptance: dotfiles-T124-wave1-task-validator-a01

- **Decision:** PENDING (round 2 in progress). PR #313 `feat/task-validator` on main `d29ce4c1`; round-1 RESULT head `a11e3617` (11:55Z) with 43 Bot threads, 33 fixed in the PR and 10 open, all ten sent back as Revise round 1 (every one fixed at its root; the grandfather choice bound to a checked-in list of pre-format-2 task ids). Dispatched 2026-10-10 09:00Z after T118/T119 merged; Amendments 1–8 (gate source untouched and `REVIEW_TREE`, redesign-record validation, bind the canonical receipt now, tier stamp and `process_tiers`, six Bot fixes, `implementing_tasks` in the hash, the `redesign` profile defined in this PR, the profile set validated); design: T124 (canonical receipt `4163ac9b…`, four keys) under the accepted T126 regime v2 (round-4 receipt `1e3b9d12…`).
- **Worker:** `claude-standard-dot-a001` (worker-c, w4:p9).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; Bot thread replies and resolution.
- **Process notes to carry:** Amendment 4 (the tier stamp) and the first form of wave 3b's Amendment 3 rode on the T126 design before it had a receipt; T126 was then reviewed (three rounds, accepted) and the amendment stands. The T124 INV-5(d) count (Bot P1 on two heads) fired on pre-RESULT pushes of this PR under the v3 definition; T126 redefines (d) as heads after the first RESULT, a decision the orchestrator made in a document it authored while this PR was open and put to the operator as "in force unless the operator objects"; the operator saw it and did not object; this record names it so the exception is visible (T126 review round 1, F3). The Bot raised findings on every pre-RESULT head (eight heads); the worker's own misses: the review of 918a91b8 read late, Amendment 2 read 40 minutes late, one commit bundled with a push.
- **Origin:** operator direction 2026-10-10: when substantive findings repeat the design is wrong and a mechanism must force a redo; rules must be mechanical; the auditor must be able to find the orchestrator's mistakes.

## What is under acceptance (PR #313, final head named in the Decision line)

- `scripts/validate-task.py` (new): format-2 front matter (own PyYAML-free parser, kept equal to PyYAML on every accepted file), derived `security` and `tier` from the design tier with exact glob intersection (NFA), the canonical hash over `invariants`, `threat_model`, `trust_anchors` and `implementing_tasks`, the receipt bound to that hash plus a non-orchestrator reviewer and `Design verdict: accept`, `implementing_tasks` scope, design-reset records (acceptance directory only, lexical parent), `--print-tier`, `--print-design-hash`, legacy grandfather.
- `scripts/lib/high_risk_paths.py` (new): the review tier as a copy kept equal to the gate's constants by test, the explicit design tier, the glob NFA, the subset YAML parser.
- `scripts/check-regime-boundary.sh`: validates format-2 task files and reset records. `Makefile`: `REVIEW_TREE` (a top-level worktree of this repository). `home/dot_agents/agent-config.yaml`: `process_tiers` and `model_profiles.redesign` (rendered; the manifest validator's profile set gains it). Prose: SKILL (task authoring, worker step 1, gate from `main`), the agmsg-orchestration rule (one line), pr-integration and crit-review (the gate form), AGENTS.md, README.
- Evidence: 62 rule removals each failing its test (validation §5); suite in the sandbox at head and base; the T124 and T126 task files validate against the canonical receipts.

## Audit / sweep / gate

| scope | verdict |
|---|---|

- Sweep: (at the final head).
- Bot wait: findings on eight pre-RESULT heads (ce9d3dd2 … a11e3617), 33 fixed in the PR; ten open at the round-1 RESULT → Revise round 1.

## Parallelism

- Concurrent with T120 (worker-e) and T124 wave 3b (worker-f); shared code file `tests/unit/test_herdr_agents.py` in disjoint hunks (orchestrator exception recorded in all three tasks); later PRs take `gh pr update-branch`.

cost: (measured at acceptance per T126 INV-10: rounds, amendments, wall time from history, audit count)
