---
reviewed_at: 2026-10-10T21:15:46Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b91e8bb407e1019196eade22604fac30801bfce173a95416e9176ca8917b352f
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 1
---

# Design review: dotfiles-T128-regime-v3-a01, round 1

Reviewed from a fresh context seated at .claude/worktrees/worker-d, every path read in the main checkout at main d29ce4c1. Read: the design, baseline.md, practice-evidence.md, method-draft.md, the three fact sheets, T126, T124, both reset records, require-crit-review.py, agent-stop-gate.sh, check-regime-boundary.sh, pr-feedback.py, test.yaml, the --audit path of executable_herdr-agents, .claude/settings.json, the file lists of origin/feat/task-validator (52bb69fc) and origin/feat/audit-grammar (9fc521fe). Re-ran: premises 1, 3, 6 and the history counts for T124 W1, T124 W3b and T119. Fetched: the Claude Code headless, hooks and best-practices pages, the Codex hooks page, GitHub's troubleshooting-required-status-checks and events-that-trigger-workflows pages. Not verified: the live ruleset (gh api failed on TLS inside the sandbox and the task forbids an out-of-sandbox read); the Bot P1 head count on PR 314; the per-message usage format of session transcripts.

## 1. Invariants

INV-1: rejected: the CI job has no input. The task file is orchestrator-authored, lives untracked in the main checkout until the boundary commit, and INV-8 puts only worker evidence on the branch; at PR time the implementing task file is on neither the base nor the head, so "validates every task file the PR adds or changes" validates nothing for the PR it governs. Right: the AGMSG-TASK carries task_sha256=; the worker's first commit copies the task file to .orchestration/<task id>/task.md; the regime job validates that copy against main's schemas/task.json; the host gate compares its sha256 with the token in history. Also: the regime check only binds once the ruleset lists it as required; name that operator action in V1's acceptance record.

INV-2: rejected: the wave table breaks the rule it implements. "One task invariant per PR": V1 carries INV-1 and INV-2, V3 carries INV-3, INV-4, INV-6 and INV-10, V5 carries INV-8 and INV-9 (design lines 142-146). Either the unit is "one implementing task's declared invariant set" (then say so and the CI check compares the PR's task.md invariant ids with the design's implementing_tasks entry), or V3 and V5 split. Second gap: the seven required checks of test.yaml run on pull_request (test.yaml:11), so a PR still edits the workflow that runs INV-12's unit tests (R8 stays open there); the regime job should refuse a PR that changes .github/workflows/** unless its task.md is design tier and lists the file.

INV-3: rejected: "fails on the previous head" and "the fix turns green" are not gate-checkable; the gate cannot run tests on an earlier head. Mechanical core: the ACCEPTANCE status=revise carries check=<tests/...::name | ci:<job> | repro:<id>>; the RESULT's validation file carries the same id with pasted output; the regime job verifies the named test exists on the head and differs from the previous RESULT head (git diff <prev head> <head> -- <test file> non-empty). State that; the rest is the worker's evidence.

INV-4: rejected: internally inconsistent. "the orchestrator may amend once" allows one amendment; "a third amendment withdraws" allows two; INV-6 and section 7 say two. Fix the count once (INV-6 is the counter, INV-4 the trigger). Second: "counted from AGMSG-TASK amendment= messages" is the relabel path INV-12 names; count every AGMSG-TASK for the task_id after the first (history: T124 W1 10 TASK sends, 8 with amendment=; W3b 10 and 5; T119 10 and 8). Third: "withdraws the task to design" names no enforcement point; it is INV-6's Stop block and merge backstop, so say so.

INV-5: rejected: (a) the gate today takes the verdict by regex from the .last.md companion (require-crit-review.py:30-31, 638-665) and accepts not-applicable for every finding whatever its category (require-crit-review.py:698-710); replacing that with the schema JSON, the AGMSG-AUDIT sha256 lookup and the orchestration/conformance lock is a change to an existing evidence rule, and no wave names it (V2 is runner and schema, V3 the reset backstop, V4 the design-review anchor, V5 accept-task.py). P4's "gains only history-anchored checks; nothing removed except REVIEW_TREE" is false on its own terms, and REVIEW_TREE does not exist on main (it was PR 313's). (b) The AGMSG-AUDIT record names no sending identity; the runner runs on the orchestrator's host, so say honestly that the anchor prevents edits after the record, not fabrication before it, and name the identity. (c) "started automatically when ... the Codex Bot has reviewed the head" has no timeout; the SKILL's 15-minute bot: none rule must carry over or a head the Bot skips stalls stage 3 (Bot re-review per push is UNVERIFIED in codex-factsheet.md:55). (d) "never for an evidence-only revision" conflicts with audit_name_error, which requires the audit sha to prefix HEAD (require-crit-review.py:614-615): an evidence-only commit moves HEAD and the gate refuses the earlier audit. Right: the gate accepts an audit of an earlier head when git diff --quiet <audited> <HEAD> -- . ':!.orchestration' holds; assign it to a wave. (e) "rationale written before the verdict" is a prompt instruction, not a schema property: strict JSON schema does not order generation, and PR 314's schema lists verdict first.

INV-6: rejected: (a) the loop-time block is soft on both runtimes: Claude's Stop hook has an 8-consecutive-continuation cap that resets on any tool call (hooks page, Stop section), and Codex's decision: block "doesn't reject the turn" but injects a continuation prompt (learn.chatgpt.com/docs/hooks). The merge backstop in the gate is therefore the mandatory point and the Stop hook the early signal; the invariant says the reverse. (b) The Bot count "on two heads" is not computable from the sweep JSON: pr-feedback.py records commit_id on review items only (pr-feedback.py:199) and nothing on review_comment items; the collector change (T124 wave 2a's original_commit_id) is in no wave. (c) The audit count needs the audit JSONs, which are orchestrator files in the main checkout; name the source. (d) The Stop hook runs with timeout 5 and a 3 s history budget (.claude/settings.json; agent-stop-gate.sh:209-212): history counts fit, GitHub counts do not; split the counts by source. (e) "re-dispatch ... is a boundary violation" names no detector; T124 v3 INV-5 had one (a closed-unmerged PR whose task has no reset record; a task over a threshold with no accepted record) in check-regime-boundary.sh; restore it in V3.

INV-7: accepted. Notes: the canonical hash covers five front-matter keys; sections 4 to 9 (stages, enforcement map, waves, thresholds) are outside it, so the wave table can change after review without a new one; add that to INV-12's gaming paths or hash implementing_tasks together with the wave file list. Bootstrap: this receipt carries a whole-file sha256, so V1's AGMSG-TASK is anchored by that form; V4's gate check must accept both forms for this design or V1 needs a second review.

INV-8: accepted. Notes: add the task.md copy (INV-1 above); the gate's path rules (feedback_path_error, orchestration_path_error) already fit, because the orchestrator's records stay under .orchestration/validation and acceptance; the "final head" with worker evidence committed is what INV-5 (d) above must handle.

INV-9: rejected: "whose breach pauses the task for an operator decision" names no mechanism that pauses; the enforcement map puts cost in accept-task.py and the boundary warning, which run after the fact. Say "the acceptance record names the operator decision and the boundary check warns", or name the Stop-hook check with its budget source. Per-message usage in session transcripts is UNVERIFIED in claude-code-factsheet.md:75; the premises block does not cover it.

INV-10: rejected: the stop gate reads history rows as from, to, body with no timestamp (agent-stop-gate.sh:65), and a push is GitHub state the 5 s hook cannot fetch; neither the 30-minute first push nor the 20-minute idle is computable where INV-10 places them. Right: history.sh timestamps for the TASK time, gh pr view for the first push, both in check-regime-boundary.sh and accept-task.py; the Stop hook can at most read the TASK time once the awk carries the timestamp column.

INV-11: accepted. Note: permgate records input_hash and no session_id or cwd today (executable_permgate:161, 219), consistent with the design; the sandbox record the gate compares against is the one INV-8 commits on the branch.

INV-12: accepted. Notes: add the gaming paths this review names (a TASK without amendment=, an evidence-only relabel of a code change, a wave-table rewrite after review, a Bot-skipped head that never starts its audit).

## 2. Failure modes that still pass (Q2)

- Amendment accretion (T119, T124 W1, T120): passes while INV-4 counts only amendment= tokens; a plain AGMSG-TASK, a poke or a note carries the same text. INV-4 should catch it by counting every TASK after the first.
- Bespoke parser bypass loop (PR 313): closed for the validator by INV-1 (jsonschema plus PyYAML). Not closed for V2's audit-head.sh and audit-watch.sh and V5's accept-task.py, which are new code at the same boundary; INV-2 bounds their size, not their kind. INV-1's principle (no hand-written parser at a trust boundary) should be stated as a rule the auditor checks per PR.
- Oversized PR (PR 312, 313): closed by INV-2 once regime is a required check; open until the ruleset lists it.
- Waiver instead of reset (PR 313 round 2): open until V3; after V3 the Stop block is soft (INV-6 (a)) and the merge backstop is the catch. INV-6 should name the backstop as mandatory.
- Orchestrator self-disposition (T119 audit-finding 2): passes today and after V2, because audit_disposition_errors accepts not-applicable for any category (require-crit-review.py:698-710) and no wave changes it. INV-5 should catch it; assign the lock to V3 or V5.
- Audit as serial queue (T119): closed by the pool and auto-start in INV-5, subject to the Bot-wait timeout (INV-5 (c)).

## 3. pull_request_target as the main-pinned check (Q3)

The discipline is sufficient on a public repository if the job keeps main at the workspace root and never checks out the PR head there. Confirmed: pull_request_target is an eligible event for required checks and an if-skipped job reports Success (troubleshooting page), so the changes pattern transfers; GITHUB_SHA under pull_request_target is the last commit on the default branch (events page), so actions/checkout's default ref is main, and the diff range must come from github.event.pull_request.head.sha against its merge-base with main, not from github.sha as test.yaml:38-48 does. Executable surface, each to be excluded in regime.yml: actions/checkout with ref: head.sha at the root; uv run without --no-project (it reads a PR-controlled pyproject.toml); yaml.load instead of safe_load; make or any script invoked from a PR tree; a dependency file read from the PR. Read PR files as git show <head>:<path> or into a subdirectory never on PATH, with permissions: contents: read and no secrets. One residual the design does not state: a PR that changes regime.yml is checked by main's copy, never its own, so a regime.yml change has no pre-merge exercise; name the way it is tested (a workflow_dispatch dry run or the unit test of its script) before V1 lands. The merge commit is irrelevant here: checks are evaluated on the test merge commit when it has a status, else the head (troubleshooting page).

## 4. Reset rule and redesign author (Q4)

Counts: revises should be counted as RESULTs for the task_id minus one (worker-authored; a split round without a revise ACCEPTANCE still produces a RESULT); amendments as TASKs after the first (INV-4); Bot heads need original_commit_id on inline items (INV-6 (b)); audit heads are fine once the JSONs are named. Gaming: split rounds and relabelled amendments are closed by those two counts; re-dispatch under a new id needs the boundary detector (INV-6 (e)); a question answered as a note still counts because the worker's PONG status=question is in history, so the orchestrator cannot suppress it. Bootstrap exception: trust anchor 5 says a reset is released only by another context or the operator; T128 was written by claude-deep-dot, who dispatched the abandoned tasks, and the reset records call it a "bootstrap exception" in prose, which is R5's shape. Bounded only if the records carry the operator form the design itself specifies (DESIGN_RESET_WAIVED_BY with the 2026-10-11 decision), this receipt is the only release, and no further orchestrator-authored design follows under T128. Both reset records name claude-review-dot-a004 as the pre-dispatch reviewer; history holds the TASK to claude-review-dot-a001 (2026-10-10T21:04:16Z); correct the records before they are committed. Dropping the redesign profile: review is claude-fable-5-1 at effort high (agent-config.yaml:41), the same model and effort as deep (agent-config.yaml:44), so the lever is exactly and only a separate context; the evidence supports that (T124 round 1; practice-evidence.md:60, cross-model vs same-model fresh not significant), and T124 v4's xhigh had no measured benefit. Not a loss; state the equality so nobody reads "review profile" as a different model.

## 5. Ponytail on the waves (Q5)

Caps: V1 (seven files, schema plus about 80 lines plus workflow) and V2 fit; V3 edits agent-stop-gate.sh, require-crit-review.py, the manifest, its rendered codex-config-managed.toml, validate-task.py and check-regime-boundary.sh, within 15 files but four invariants (INV-2 above); V5's accept-task.py has no size estimate and T125's draft is the risk. Still bespoke where a platform feature or script exists: audit-watch.sh polls CI and the Bot, which gh pr checks --watch plus the SKILL's existing Bot list loop already do; make it a Makefile target around those, not a daemon. design-review.sh and audit-head.sh are thin wrappers and fine at about 100 lines. Salvage the design drops: PR 313's scripts/legacy-task-ids.txt (310 ids, only shrinks) is a simpler grandfather than "format-2 and tier stamping", and its 41 test names in tests/unit/test_validate_task.py are the test ideas; PR 314's scripts/schemas/audit.json already matches INV-5's field set and is named; PR 314's pre-push hardening (evidence staged and installed only once masked; the fallback claude limited to the .orchestration dir and the worktree, PONG of 2026-10-10T12:36:42Z) belongs in V2's runner; PR 313's home/dot_codex/modify_private_redesign.config.toml is correctly dropped with the profile. scripts/lib/ holds only shell today (asset-manifest.sh, github-release.sh, installer-pins.sh), so high_risk_paths.py is a new module, not a move.

## 6. Audit staging (Q6)

Stages and tiers are right with one tier error: docs tier is "prose-only allowed_files", which puts the regime's own rule text (home/dot_config/claude/rules/*.md, the SKILL, AGENTS.md) on CI plus Bot with no audit; PR 313 thread 4237594826 raised this exact point. Rule prose the machinery cites belongs in review tier by an explicit list. "Once per RESULT head, never for evidence-only revisions" is safe under the cited literature (2607.24604: bind verifier evidence to the exact code state) only with the tree-equality check of INV-5 (d); without it "evidence-only" is an orchestrator assertion. Input set: add the previous round's audit JSON and the acceptance record's dispositions (MCR-Bench's re-flagging failure, practice-evidence.md:59), and the head's pr-feedback JSON; the permgate window is listed for design tier only, which matches INV-11's coverage. Order the schema so findings precede verdict and keep the reasoning instruction in the prompt (INV-5 (e)).

## 7. Premises (Q7)

1. Holds for PyYAML (Makefile:189, 203; agent-assets.yml:35), does not hold as stated for jsonschema: no --with jsonschema exists in Makefile or any workflow; the premise's pasted output names only pyyaml. Unverified, not refuted; V1 adds the dependency and the premise should say so.
2. Holds: the troubleshooting page lists push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; the events page: "This event runs in the context of the default branch of the base repository", GITHUB_SHA "Last commit on default branch".
3. Holds: codex-cli 0.161.0; codex exec --help lists --output-schema <FILE>; codex exec --full-auto fails with "unexpected argument '--full-auto' found"; codex exec -a never fails with "unexpected argument '-a' found".
4. Holds: headless page: "In bare mode, Claude Code never reads OAuth credentials or the system keychain"; "Without --bare, a -p session runs the hooks in a project's .claude/settings.json"; "the structured output in the structured_output field"; "If the run reaches its --max-budget-usd cap, Claude Code stops the remaining background work".
5. Holds verbatim: "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run /clear and start fresh with a more specific prompt that incorporates what you learned."
6. Holds: the four T119 audit files are dated 11:48, 13:55, 15:52, 17:23 local; history: first TASK 2026-10-09T21:26:24Z, accepted ACCEPTANCE 2026-10-10T08:32:16Z, 11.1 h.
7. Holds for the event list (Stop is listed) and weakens the use made of it: the Codex page says decision: "block" "doesn't reject the turn" and exit 2 writes "the continuation reason"; see INV-6 (a).

Baseline recount from history.sh dotfiles-conformance "" 5000: T124 W1 TASK 10, amendment= 8, questions 6, RESULTs 2, revises 2; W3b 10, 5, 0, 1, 0; T119 10, 8, 8, 6, 5; all equal to baseline.md. Note for V3: history.sh defaults to 20 rows and silently truncates; a counter must use the storage facade as agent-stop-gate.sh does, or pass a limit.

## 8. What the design should not do (Q8)

- Do not place GitHub-sourced counts or push timing in the 5 s Stop hook (INV-6 (d), INV-10); they belong to the gate and the boundary check.
- Do not call the Stop block the enforcement point (INV-6 (a)); it is the early signal.
- Do not promise a budget "pause" without a mechanism (INV-9).
- The 500-added-line cap would have split T116 (+529), T118 (+881) and every later task; defensible, but say that it changes the unit of work, not only the review load.
- Section 10 names scratchpad files (claude-code-capabilities-factsheet.md, codex-fact-sheet.md, github-merge-gates-factsheet.md, evidence-sheet-2026-10-11.md, regime/baseline.md) that are not the repository paths under .orchestration/validation/dotfiles-T128-regime-v3-a01-research/; the receipt must be checkable from the repository, so cite those.
- Section 1 states W3b "Bot P1 on two post-RESULT heads"; the worker's PONG of 2026-10-10T12:36:42Z counted one head at that time, and the second (9fc521fe) is not verifiable from here; the reset record should cite the thread ids.

## 9. Document findings

- F1 INV-1 enforcement input (section 1).
- F2 INV-2 wave table versus one invariant per PR; test.yaml stays PR-editable.
- F3 INV-5 gate changes unassigned; category lock absent; Bot-wait timeout; evidence-only head versus audit sha prefix.
- F4 INV-6 soft Stop block on both runtimes; Bot head count not computable; boundary detector dropped.
- F5 INV-4 contradiction and relabel path.
- F6 INV-9 and INV-10 enforcement points not reachable from the Stop hook.
- F7 Reset records name the wrong reviewer identity; bootstrap exception in prose rather than the operator-waiver form.
- F8 Docs tier covers the regime's own rule prose.
- F9 Premise 1 overstates jsonschema availability.

The direction, the trust anchors and the thresholds are sound and the premises hold where checked; the rejections are enforcement gaps that a second round of this document closes without a new design.

Design verdict: revise
