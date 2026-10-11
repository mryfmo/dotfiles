# Regime v3: the method (draft for operator approval, 2026-10-11)

Status: orchestrator draft after the 2026-10-10 halt. Not a task file yet; nothing dispatched.
Inputs: measured baseline (baseline.md); fact sheets on Claude Code 2.1.293, Codex CLI 0.161.0, GitHub, and the research literature (scratchpad/*factsheet*.md, evidence-sheet-2026-10-11.md).

## 1. Finding: the fix program tripped its own reset rule

By T126 INV-6 as written: W1 (PR #313) 8 amendments (limit 4), 2 revises (limit 2); W3b (PR #314) Bot P1 on two post-RESULT heads. The orchestrator was drafting a waiver for #313 instead of resetting. T120 was reset only on the operator's question. The regime is therefore reset here, by its own rule, and the method below is its redesign.

## 2. Root causes (data + evidence)

RC1 Rounds without a deterministic verifier. Revise rounds are judged by models re-reading models (Bot -> worker -> auditor -> orchestrator). Evidence: intrinsic self-correction degrades after round 1 (Huang 2023); a second review round on the same artifact adds ~62% more false positives (2603.16244); multi-round review degrades with rounds (MCR-Bench). Baseline: T118 20 revises, 8 audits; T119 5 revises, 4 audits.
RC2 Hand-written parsers at trust boundaries. 33 of 52 Bot threads on #313 are bypass findings against a 503-line validator with its own YAML parser and a 316-line glob matcher, written to avoid PyYAML, which the Makefile and CI already install with `uv run --with pyyaml`. The premise was false; the finding surface is unbounded by construction.
RC3 PR scope. #313: 20 files, +2,642 lines; #312: 37 files, +3,191. Google: 100 lines reasonable, 1,000 too large; ~90% of Google changes touch <10 files. T126's own 15-file limit was exceeded by its first wave.
RC4 Task text grown by Q&A. #313: 6 questions -> 8 amendments; T119: 8 -> 8; T120: 8 amendments, zero RESULTs. A task that needs an amendment per question was dispatched under-researched; amending keeps the wrong premise (T119 Amendments 7-8 changed the principle; six rounds followed).
RC5 The orchestrator is unaudited and dispositions findings about itself (T119 audit-finding 2). Kept from T124/T126: auditor scope over orchestrator artifacts; orchestration/conformance findings released only by the operator.
RC6 Reset existed as prose and as a rule the orchestrator could waive. Evidence from the vendor: "corrected more than twice on the same issue ... /clear and start fresh with a more specific prompt" (code.claude.com best-practices).

## 3. Principles (each names what it reuses and what it deletes)

P1 One deterministic fact per round. A revise round is admissible only when it adds a new deterministic check (a failing unit test, a CI check, a reproduction command with pasted output) that the fix then turns green. A finding that cannot be turned into a check is dispositioned, not iterated. Reuses: tests/unit, CI, `pr-feedback.py`. Deletes: free-form revise rounds.
P2 Declarative over imperative at every trust boundary. Task files, audit verdicts, design-review receipts and evidence records are JSON-Schema documents validated by the `jsonschema` library (PyYAML for YAML front matter). Model outputs are produced under schema (`codex exec --output-schema`, server-side strict; `claude -p --json-schema`). Deletes: the bespoke YAML parser, glob NFA, prose verdict grammar, regex parsing of `.last.md`.
P3 Small, one-invariant PRs, enforced in CI. Hard caps: 15 changed files and 500 added lines outside `tests/` and `.orchestration/`; one task invariant per PR. Over the cap is not a finding, it is a split. Reuses: GitHub required checks. Deletes: waves declared inside a task file.
P4 Main-pinned mechanical checks run in CI. A `pull_request_target` workflow (runs main's workflow file; eligible as a required status check; required workflows are org-only) runs main's validators against the PR's files read as data (never executing PR code). Checks: task-file schema, PR caps, evidence presence and shape, worker evidence committed on the branch. The host-side gate keeps only what needs local state: agmsg history anchors (design RESULT before TASK, audit record for the head), reset counts, permgate window. Deletes: REVIEW_TREE and the gate-from-main apparatus for the mechanical part.
P5 Research before dispatch; questions end the task, not amend it. A task file carries `premises:` with the command and pasted output that verified each premise. A worker `PONG status=question` is a specification defect: the orchestrator answers once (amendment 1) or, on the second question, withdraws the task and returns it to design. Amendment cap: 2 (count from history; the third is a reset). Deletes: the amendment-per-question practice.
P6 Reset is mechanical, loop-time, and released only by the operator or a redesign by another context. Counters from agmsg history and GitHub (never from orchestrator files): revises >= 2; amendments >= 2 (P5); Bot P0/P1 on 2 post-RESULT heads; audit P0-P1 implementation finding on 2 heads. Trigger blocks the orchestrator's Stop (Claude Stop hook; Codex `[hooks].Stop` exists too) and the merge. Release: a reset record naming a redesign task written by a separate context (`review` profile seat or headless fresh-context run), or `DESIGN_RESET_WAIVED_BY=<operator>` typed by the operator, visible in the acceptance record, boundary PR body and `check-regime-boundary`. Framing: Western Electric "2 of 3" rule, a signal to investigate, with the investigation being the redesign.
P7 Audit staging by tier; the auditor never serializes the pipeline.
   tier docs (prose only): CI + Bot; no audit; worker `express`; 1 revise.
   tier review (scripts, hooks, tests): CI + Bot each push; one schema audit per RESULT head; 2 revises then reset.
   tier design (install/, gate scripts, permission/sandbox, credential paths): design review before code (fresh context, schema receipt) + review-tier pipeline + invariant map in the audit + permgate window.
   The audit: starts automatically when CI is green and the Bot has reviewed the head; `codex exec --output-schema` read-only in a detached worktree at the head (fallback `claude -p --json-schema --permission-mode plan`), pool of 2, at most once per head, never for evidence-only revisions; receives the task's invariants (judges without a reference are lenient: 2607.12885) and the orchestrator's artifacts; reasons in a `rationale` field before the verdict (format restriction degrades reasoning: 2408.02442); flags only gaps that affect correctness or the stated invariants (vendor warning on over-reporting). Measured: 4 audits ~= 1.3 h of T119's 11.1 h; the rounds were the bottleneck, so P1 and P6 are the throughput levers, the pool and auto-start remove the queue.
P8 Cost is measured, not estimated. Headless runs: `total_cost_usd` (`claude -p --output-format json`), `turn.completed.usage` (`codex exec --json`), `--max-budget-usd` caps. Seats: `~/.claude/projects/<slug>/<session>.jsonl` per-message `usage` (observed: cache_read_input_tokens etc.; format internal to Claude Code), Codex rollout `token_count` events. Acceptance record: rounds, amendments, wall time, audits, Bot threads, tokens by seat. Per-tier budget; over budget pauses for an operator decision. Model routing stays in `model_profiles` (worker standard, review review, audit audit, docs express).
P9 Parallelism with disjoint files, early push. Up to 3 workers; first push (draft PR) within 30 minutes so CI and the Bot see the design early; idle detection from history.

## 4. Disposition of the in-flight work

- PR #313 (W1): closed unmerged, kept as reference. Salvage: the process-tier table, the format-2 key set, the test ideas. Replacement: `schemas/task.json` + ~80-line `validate-task.py` (jsonschema + PyYAML) + CI job.
- PR #314 (W3b): closed unmerged, kept as reference. Salvage: `schemas/audit.json`, the AGENTS.md Audit text, the agmsg AUDIT record idea. Replacement: ~100-line runner.
- PR #315 (T120): already reset; stays closed-as-reference per its reset record.
- Worker seats: removed (`herdr-agents --remove-worker --force` after the branches are pushed); reseated per wave.

## 5. Waves (each: one invariant, <= 15 files, <= 500 added non-test lines, its own fresh review of the task file before dispatch)

V1 task schema + validator + CI `regime` job (schema, caps, evidence shape) [review tier -> design tier because it is a gate script; design review first].
V2 audit schema + thin runner + AGENTS.md Audit section (auditor's standing over orchestrator artifacts, categories, JSON) + the `AGMSG-AUDIT` history record.
V3 reset counters in the Stop hook and the host gate; operator waiver visibility; premises block and amendment cap in the validator.
V4 design-review runner (fresh-context headless, schema receipt, history anchor) replacing the resident review seat for design reviews.
V5 acceptance automation and cost fields (sweep -> dispositions -> record -> gate -> merge command); budgets per tier.
V6 permgate session_id/cwd (operator-routed, Codex security profile review).
Prose (SKILL, rules, README) changes ride in the wave they describe, sections disjoint.

## 6. Thresholds (operator may change)

revise 2; amendments 2; Bot P0/P1 heads 2 (post-RESULT); audit implementation P0-P1 heads 2; PR 15 files / 500 added non-test lines; first push 30 min; idle 20 min; workers 3; audit pool 2; audit once per head.

## 7. Open decisions for the operator

D1 Reset #313/#314 (close as reference, rebuild small) vs waive and continue them.
D2 Who writes the redesign task files: (a) orchestrator drafts under a recorded bootstrap exception, a fresh-context review run must accept before dispatch; (b) a `review`-profile seat authors them (no ad-hoc flags needed; slower).
D3 Mechanical checks in CI via `pull_request_target` (main-pinned, required check) + host gate for history-anchored rules; vs host-only gate as in T126.
D4 Thresholds in section 6.
