# AGMSG-ACCEPTANCE dot-orchestration-rules-T33a-a01

RESULT 2026-09-28T04:09:18Z from claude-standard-dot-a005 (worker-c, claude-opus-5-5 high, --advisor fable): revision 2, status=ready_for_review, PR #196 head 87980763c76860721d2a61b52fb42d22b3d15856, branch docs/orchestration-rules-T33a from origin/main ca4af19.

## Revision history

- Rev1 dispatched 03:0xZ. Worker PONG blocked (03:21Z): the Codex crit mirror is `home/dot_config/codex/AGENTS.md`, outside the allowed "under home/dot_agents or home/dot_codex" wording, and it contradicted the Claude rule (browser fallback when crit data is unavailable, `crit share` listed as routine, empty heading with misplaced bullets). Correct fail-closed behavior: it did not edit and asked for a ruling while proceeding with items 1/2/3/5.
- Rev2 (245d014): option A approved — edit the Codex AGENTS.md crit passages; item 4 rewritten with the four concrete edits (a–d).

## Adversarial review (orchestrator, from origin refs)

- task_rev 4ba24d22… (rev2) matches the task file at origin/main 245d014; the PR does not touch `.orchestration/tasks/`.
- Diff scope: 4 files (+14/−9): SKILL, Claude agmsg rule, Claude crit rule (one bullet, shared verbatim — permitted by the allowed-files clause), Codex AGENTS.md (crit passages only, Japanese kept). No scripts, tests, manifests, or hooks touched. Two commits, both English.
- Item 1 (inbox discipline): present in SKILL "Identity, delivery, and storage" and as a Claude-rule bullet, with the retirement condition (worker pane inside its own worktree). Matches the diagnosis in `.orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md`.
- Item 2 (fail-closed): Claude-rule bullet plus SKILL Worker Playbook step 4 — PONG blocked with exact command and boundary; agent-to-agent approval forbidden; only the human answers a permission prompt. Placement in the Worker Playbook is better than the section the task named.
- Item 3 (batch pre-screen): both files; acceptance authority explicitly unmoved; per-RESULT records kept.
- Item 4 (Codex crit alignment): both "Crit data を取得できない場合" browser fallbacks removed and replaced by the agent-side-evidence sentence; `crit share` made explicit-request-only; Plan Mode session close added; the empty "Crit レビューの利用方針" heading deleted and the two misplaced bullets moved under "Crit レビュー運用". Non-crit sentences unchanged (diff shows no other hunks). The Claude crit rule received the same share/close bullet so both sides are literally aligned.
- Item 5 (no pane probes): SKILL "Regime activation" bullet extended with the read-only probe ban and the `--help`/fake-CLI alternative.
- Validation: `make validate-agent-assets` ok; `make unit-test` 490 OK (skipped=1) on the final run; PR CI 12/12 pass (nix skipped). One-off failure of `test_permgate.PermgateTest.test_bench_runs_five_layer_two_fixtures` (`0 != 5`) on the first run, passing alone and on the full rerun: the test uses fake CLIs and reads nothing this PR touches; CI passed. Dispositioned as pre-existing flakiness — LEARNING CANDIDATE for a small task to make the permgate bench test deterministic (not a T33a defect).
- CompactionDB: 29569eaf-79a9-4d22-9fd4-7ae23029b6c7 present in the main-checkout DB.
- Refutation attempts found no correctness, security, or omission issue; the text changes carry no runtime behavior.

## Pre-merge Codex audit (head 8798076, gpt-6-astra, read-only, VISIBLE LANE — first pre-merge use of `herdr-agents --audit`)

Evidence: `.orchestration/validation/dot-orchestration-rules-T33a-a01-audit.md` (tee'd by the audit tab wJ:t3; `Audit exit: 0`). One P2: the "substitute agent-side review evidence when Crit data is unavailable" clause (now mirrored into the Codex AGENTS.md) names no evidence format that `make require-crit-review` accepts, so the fallback would leave completion blocked. Orchestrator verification: the guard (`crit_data_errors`) validates shape only — a non-empty JSON list of records with string `id`/`body`/`scope`, `resolved: true`, and one review-scope record — so the fallback IS satisfiable with hand-written records in that shape; the defect is documentation, and it pre-exists in the Claude rule (`crit-review.md` line 8, unchanged by this PR). ACCEPTED as a real gap surfaced by the mirroring → revision 3 (item 6): state the format in all three crit texts and in AGENTS.md "Agent Review Evidence"; guard unchanged.

**Decision on revision 2: REVISE (one consolidated round).**

## Revision 3 — ACCEPTED (2026-09-28)

RESULT 2026-09-28T04:26:56Z: revision 3, PR #196 head 489c83be0e1f6cd2344acd9e6b6191f2c26b3f8d, one commit 489c83b (+4/−3 across AGENTS.md, SKILL, Claude crit rule, Codex AGENTS.md).

- Item 6 verified against the guard source: the stated shape (non-empty string `id`/`body`/`scope`, `resolved: true`, one `scope: "review"` or path-bound `line`/`file` record) and receipt fields (`review_surface: crit-data`, `reviewer: claude-code|claude|codex`, `review_source`, `review_outcome: approved|addressed`) are exactly what `crit_data_errors`/`agent_review_errors` accept. Guard unchanged (diff confirms). Wording consistent across the four files; Japanese kept in the Codex mirror.
- Validation: validate-agent-assets ok; unit-test run 1 failed the same permgate bench test (`0 != 5`), run 2 490 OK — second observation of the flake, fixture timeout is 0.2 s with Python fake CLIs → tasked as dot-permgate-bench-flake-T33d-a01. PR CI 12/12 pass.
- Visible-lane Codex audit of 489c83b: "no actionable regressions; in-memory checks confirmed the documented review, line, and file records pass validation" — evidence `.orchestration/validation/dot-orchestration-rules-T33a-a01-audit-rev3.md`.

### Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-orchestration-rules-T33a-a01-receipt.md (resolved review-scope approval record r_85fda2, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-orchestration-rules-T33a-a01-crit.json).

**Decision: ACCEPTED.** Merge #196 --squash (no --delete-branch while worker-c holds the branch); deploy with a full `chezmoi apply` from the canonical clone (rules, SKILL, Codex AGENTS.md are $HOME targets); then dispatch T33b.

[memory:decision] T33a accepted 2026-09-28: agmsg-orchestration rule/SKILL gain the interim worker inbox discipline (inbox.sh at each milestone; retires when worker panes launch in their own worktree), the fail-closed task convention (PONG blocked, never agent-to-agent approval), auditor pre-screening for batched RESULTs, a read-only pane-probe ban, and Codex crit guidance aligned to the Claude no-web-UI rule; the guard-accepted fallback evidence format (crit-shaped JSON records, resolved true, review-scope record, crit-data receipt) is documented in all crit texts and AGENTS.md. PR #196 squash-merged.

cost: n/a (worker report gives no token figures)
