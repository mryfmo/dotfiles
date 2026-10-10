---
reviewed_at: 2026-10-10T21:29:22Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@61b0a812c699e57c13713057571a5883044039a0414e2fdc3dca7913421e5f85
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 2
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md
---

# Design review: dotfiles-T128-regime-v3-a01, round 2

Same reviewer, same seat, the design re-read in full at the hash above against the round-1 receipt. Re-ran: premise 1 as restated (uv run --no-project --with jsonschema --with pyyaml: 4.26.0 6.0.3), premise 8 (the named transcript: 5168 usage entries, last one with input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens), premise 9 (history.sh default 20 rows; the --limit 600 form and the positional "" 600 form both print the whole history, 266 rows at review time). Read both reset records' headers. Fetched the events-that-trigger-workflows page for workflow_dispatch. Not verified: the two Bot thread ids in the W3b reset record (GitHub unreachable from the sandbox); whether history.sh honours --limit as a flag beyond the row count matching the positional form.

## 1. Round-1 corrections

Every F1-F9 item and every INV rejection is applied as written: the task.md copy with task_sha256 and the workflow-edit refusal (INV-1, lines 44, 142); the per-task invariant set (INV-2, line 45); check= with the CI existence-and-diff step (INV-3, lines 46, 144); the single amendment count over every TASK and the consistent threshold (INV-4, line 47); the gate changes assigned to V2b, V3a and V4, the 15-minute Bot wait, the tree-equality rule, the audit identity, the schema order and the honest anchor statement (INV-5, line 48; P4, line 116); the merge backstop as the mandatory point, original_commit_id, the audit-JSON source, the hook's history-only counts, the boundary detector (INV-6, line 49); INV-9 and INV-10 out of the Stop hook (lines 52-53); rule prose in the review tier (line 134); premise 1 restated and three premises added (lines 57-59, 75-83); the Q5 salvage list, make audit-head in place of a daemon, the regime.yml discipline (line 188), the test.yaml residual (line 189), the bootstrap stated in the waiver form (line 190). Both reset records now name claude-review-dot-a001 with the TASK timestamp, carry DESIGN_RESET_WAIVED_BY=operator with the scope "T128 design only", and the W3b record cites threads 4237434169 and 4237652017.

## 2. Invariants

INV-1: accepted. Note: each amendment changes the task file; say the gate compares the copy with the latest AGMSG-TASK's task_sha256 and that the worker recommits the copy after each amendment.

INV-2: rejected: "its task.md invariant ids equal the design's implementing_tasks entry for that task" is not computable: implementing_tasks (lines 9-21) is a flat list of task ids with no invariant per entry; the mapping exists only in section 6 prose, outside the hashed keys. Right: implementing_tasks becomes a map {task id: [INV ids]} inside the hashed keys. Second gap: the regime job needs the design file on the runner, and the design is untracked in the main checkout until a boundary commit (git status at review time: untracked). State the precondition: the design reaches main through a boundary PR before the implementing TASK is dispatched and the regime job fails closed when the design named by the task.md copy is absent from main; or copy the design to the branch beside task.md, anchored by the review RESULT's design_sha256= in history.

INV-3: rejected: it contradicts INV-1. INV-1 anchors the branch copy of task.md to task_sha256= in history (line 44); the INV-3 enforcement row has the worker append a revise: list to that same copy (line 144), so the first revise round breaks the hash the gate checks, and V1 and V3c would ship incompatible rules. Right: the worker's revise list is a sibling file (.orchestration/<task id>/revise.yaml) that the regime job reads; task.md stays byte-identical to the dispatched file.

INV-4: accepted. Note: the question count now lives in INV-6 without a threshold (below).

INV-5: accepted. Note: section 4's paragraph (line 136) still says stage 3 "starts without the orchestrator" while the table (line 131) starts it with make audit-head; say the orchestrator runs it on RESULT arrival and that the pool, once-per-head and tree-equality rules are what remove the queue.

INV-6: rejected: "PONG status=question" is listed among the history counts (line 49) with no threshold in INV-6 or section 7 (line 175); v1 had "a second question". Right: state 2, or say questions count only through the TASKs that answer them and remove the item. Note: the audit-heads count reads .orchestration/validation/<task>-audit-<sha7>.json from the main checkout; require the JSON's sha256 to match its AGMSG-AUDIT record before counting, as INV-5 does for the verdict, or the orchestrator can edit a finding away.

INV-7: accepted. Fixing INV-2 and INV-3 changes hashed keys, so INV-7 itself requires a round 3; it can be a diff confirmation.

INV-8: accepted. Note: the revise.yaml of INV-3 lands under the same directory.

INV-9: accepted. Premise 8 holds as re-run.

INV-10: accepted.

INV-11: accepted.

INV-12: accepted. Note: add "a revise list appended to the hashed task.md" to the gaming paths once INV-3 is fixed.

## 3. New in v2 that reopens a finding

- Routing (F2's companion). V3b (line 163) is "Claude seat" and edits agent-stop-gate.sh, Claude's own Stop hook source; P10 (line 122) routes a Claude-boundary source to a Codex seat, and the SKILL names the auto-mode classifier's refusal of such a change on a Claude seat. V3a (line 162) puts the same file, the Codex Stop entry and the gate in one PR, three boundaries, which makes it an operator PR by construction; say so instead of "Claude seat for that part". V3a and V3b both implement the early-signal counts in agent-stop-gate.sh; assign the hook counting once (V3a) and leave V3b the schema, validator and SKILL text. V3c (line 164) is "Claude seat" and edits "the gate's validation-file line" in require-crit-review.py, an operator-routed source under P10; move that line to V2b or route V3c to the operator.
- Caps (F2). V1 (line 158) carries scripts/legacy-task-ids.txt at 310 lines outside tests/, plus the schema, validator, module and workflow, which is over INV-2's 500 added lines. Round 1 recommended the list as the simpler grandfather, so this is a cost the round-1 note did not weigh. Right: exclude the list from the line count as data by rule in pr-caps.sh, or revert to the format-2 key grandfather; name one.
- Premise. V1's regime.yml test plan (lines 158, 187) relies on workflow_dispatch; the events page: "This event will only trigger a workflow run if the workflow file exists on the default branch." The stated sequence (merge unlisted, dry run from main against a closed PR, then list as required) is consistent with it; add it to the premises since V1 depends on it.
- Evidence hygiene. Premise 8's command (line 79) embeds a transcript path in the home directory's slug form; run the masker on the design before the boundary commit, since the validator rejects home-directory paths under .orchestration/**.

## 4. Edits that make round 3 a confirmation

1. implementing_tasks as a map of task id to invariant ids (INV-2), and the design-on-main precondition or branch copy for the regime job.
2. revise.yaml beside task.md; task.md byte-identical to the dispatched file (INV-3, line 144, V3c).
3. A question threshold in INV-6 and section 7, or the item removed.
4. V3a as an operator PR; hook counting in V3a only; V3b and V3c routed by the sources they touch.
5. legacy-task-ids.txt excluded from the line cap or dropped; the workflow_dispatch premise added; the section 4 sentence fixed; the latest-TASK token named in INV-1.

Everything round 1 asked for is in v2; the three rejections are contradictions v2 introduced while applying it, each a one-line change, and INV-7's own rule requires the re-review once the hashed keys change.

Design verdict: revise
