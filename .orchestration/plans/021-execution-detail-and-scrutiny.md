# Plan 021: plan 020 subdivided (who does what, in what order), with the scrutiny for contradictions, ambiguities, errors and omissions

> Draft for the operator (2026-10-13 13:10Z). Nothing executed. "O" = orchestrator seat (me, under the regime's exemptions: task files, records, acceptance, integration, control plane). "W" = a seated worker (repository mutations). "OP" = the operator only (settings outside the repository, Claude-boundary rule text by the routing rule, `make update`, restarts, decisions on standing rules). Every OP item is listed once, at the moment it is due.

## Part A: the subdivided steps

### Step 1: P2 becomes advisory without changing any standing rule yet

| # | Sub-step | Who | Detail | Verifiable output |
|---|---|---|---|---|
| 1.1 | Owner task per lineage | O | Three one-page task files from one template: `dotfiles-T128-playbook-rules-followup-a01` (exists, pair-confirmed), `dotfiles-T128-orchestrator-tools-followup-a01`, `dotfiles-T128-gate-evidence-followup-a01`; item 1 = the rows under the heading `## Owned by <task id>` in the lineage's acceptance record; `after:` the lineage's last task | checker C1–C10 OK; one parallel pair round (seat + Codex) |
| 1.2 | Advisory section in acceptance records | O | Every P2 (Bot, local review, audit) goes under `## Owned by <followup id>` as `<id>\t<class>`; the sweep disposition reads `not-applicable:advisory P2 owned by <followup id>; evidence=git show origin/main:<task file> \| grep -n 'item 1'`; the reply on the thread says the same; the thread is resolved | sweep gaps 0; threads resolved |
| 1.3 | Automatic disposition | O | `fill_sweep.py`: a Codex review comment whose badge is P2 or P3 and whose PR maps to a follow-up id (a 3-line map file) gets the 1.2 disposition; P0/P1 stay manual | the fill prints the count of advisory rows |
| 1.4 | Counting | O (interim) → OP (rule) | Until plan 007's S6/S7 wording is amended, the orchestrator counts classes over non-advisory rows only and says so in each record; the amendment itself is OP's decision in step 8 | the record's class table names the rows it excludes |
| 1.5 | One boundary | O | Boundary (12) lands 1.1's two new files and the template; nothing else waits on it except step 5's dispositions | PR merged; `git show origin/main:<file>` for both |

### Step 2: the Codex Bot reviews once

| # | Sub-step | Who | Detail | Verifiable output |
|---|---|---|---|---|
| 2.1 | Read the current trigger | OP | app.chatgpt.com/settings/code-review → repository `mryfmo/dotfiles` → "Review trigger" (and Personal preferences → Automatic review, if the repository follows it); tell the orchestrator the current value | the value, pasted into the record by O |
| 2.2 | Set "On PR open" | OP | the repository trigger (not "every push", not "Smart"); the security review trigger set to "Whenever code review runs" or off | the value |
| 2.3 | Verify | O | the next pushed head of an open PR gets no review within 20 minutes; a manual `@codex review` still works | the ledger line |

### Step 3: main stays still under open PRs

| # | Sub-step | Who | Detail | Verifiable output |
|---|---|---|---|---|
| 3.1 | Cadence | O | records reach main once per day at most (boundary (12) in step 1 is today's; boundary (13) after the three PRs merge is tomorrow's unless the operator asks otherwise) | boundary count |
| 3.2 | Serial integration | O | one PR in integration at a time: #328 → #329 → #346; the next starts only after the previous merge and its fast-forward | the ledger shows no overlap |
| 3.3 | Expected update-branch cost | O | #328: none (the worker merges main in its round); #329: one; #346: one (after #329). Each is one CI run; no review (step 2) | CI runs per PR |

### Step 4: the deterministic merge rule, applied as the chain's stop conditions

| # | Sub-step | Who | Detail | Verifiable output |
|---|---|---|---|---|
| 4.1 | Conditions | O | required checks green; every review thread resolved; one audit of the final head with each P0/P1 finding dispositioned (fixed in the one round, or the PR stops); P2 advisory per step 1; the gate's four evidence files present | gate rc=0 |
| 4.2 | The one fix round | O/W | all P0/P1 known at the time (Bot's single review, the local review's single run, the pre-round audit) go in one `status=revise`; the post-round audit's new P0/P1, if any, stop the PR (INV-6's reset path), never a second round | revises ≤ 1 per PR |
| 4.3 | No text review for in-flight PRs | O | the confirmed texts stand; the only text change in flight is #328's amendment 1 (already confirmed) | — |

### Step 5: close the three PRs (the first measurement)

| # | Sub-step | Who | Detail | Verifiable output |
|---|---|---|---|---|
| 5.0 | Ledger script | O | `pr-cost.sh <pr>`: rounds (Bot reviews, local reviews, revises), threads by priority, resets, first push → merge wall; one line appended to `.orchestration/metrics/pr-cost.tsv` | three lines by the end of step 5 |
| 5.1 | #328 resume | O → W | lift the hold with `AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-playbook-rules-a04 status=revise` referencing the first RESULT (2026-10-12 16:04Z) and the amendment file already on main (TASK 935's hash); never a second TASK line (that would count as amendment 2 under INV-6) | the worker's RESULT with the new head |
| 5.2 | #328 integrate | O | update-branch none (the worker merges main); CI; no Bot review (step 2); local review once; sweep (13 old rows + 3 new `fixed:` + advisory rows); receipt; audit; dispositions; thread resolution; sweep re-run; gate; `gh pr merge --squash --match-head-commit`; ff; ACCEPTANCE accepted | merged sha |
| 5.3 | #329 integrate | O | a002 holds at 21badcd7: update-branch (one CI run); local review once; the record gets its 20 ledger rows (classes from titles) and advisory rows; receipt; audit; dispositions; resolution; sweep; gate; merge; ff; ACCEPTANCE accepted to a002 | merged sha |
| 5.4 | #346 resume and integrate | O → W → O | lift a002/a003's hold for a02 PR-A with a PING ("resume: send your RESULT"); mark the draft ready (the Bot's one review); the same chain | merged sha |
| 5.5 | Daily boundary (13) | O | the three acceptance records, the ledger, the receipts | merged |
| 5.6 | Apply | OP | `make update` (needs the clean checkout 5.5 leaves) then restart Claude Code: #328's SKILL text takes effect only then | the applied SKILL contains the 20-minute sentence |

### Step 6: tools before any further rule

| # | Sub-step | Who | Detail | Verifiable output |
|---|---|---|---|---|
| 6.1 | a02 PR-B | W (a003) | acceptance-front-matter.py + orch-gate.sh + tests on the new gate; the orchestrator writes the a02 record's JSON block by hand once (the writer does not exist yet) | merged under steps 1–4 |
| 6.2 | T704 | O (text) → W | the checkers promoted into `scripts/`; its task text in the step-7 short format with a hand-written minimal threat table (the exception: the generator is what it builds) | merged |
| 6.3 | Retire the scratchpad chain | O | each chain step replaced by `scripts/orchestrator/*`; the scratchpad keeps only glue with no logic | the next integration's log names repository scripts only |

### Step 7: the unit of change (after 6.2)

| # | Sub-step | Who | Detail | Verifiable output |
|---|---|---|---|---|
| 7.1 | Template | O | `.orchestration/templates/task-short.md`: goal (one sentence), files, out of scope, one end-to-end check command, the checker-generated threat table | file on main |
| 7.2 | Caps | O (practice) → OP (rule, step 8) | one mechanism per PR, ≤ 200 changed lines outside tests; text review one parallel round; overflow becomes the next PR's items | ledger |

### Step 8: one amendment of the standing rules and the design (one operator action)

| # | Sub-step | Who | Detail | Verifiable output |
|---|---|---|---|---|
| 8.1 | Draft | O | one patch with: plan 007 S6/S7 (advisory rows excluded; S7 asks asynchronous with a default; blocking only for P0), SKILL step 10 and 15 and `pr-integration.md` (P2 advisory with owner, one fix round, the merge rule, "no rule names an unlanded mechanism"), AGENTS.md's review bullet, and the design's INV-6 (resets only on a failed deterministic check or an unfixed P0/P1; P2 never counts) | patch file + `make render-check` |
| 8.2 | Design review | O | one design-review round (seat + Codex in parallel) on the INV-6 sentence | receipt |
| 8.3 | Apply | OP | the rules files are Claude-boundary (routing rule): the operator applies the patch and opens the PR, or seats a Codex worker for it; one PR | merged; `make update`; restart |

### Step 9: merge queue (optional, last)

| # | Sub-step | Who | Detail |
|---|---|---|---|
| 9.1 | Availability | OP | Settings → Rules → the ruleset: is "Require merge queue" offered for this user-owned public repository? |
| 9.2 | CI | W | `merge_group` trigger in the required workflows (workflow files: threat rows) |
| 9.3 | Ruleset | OP | Require merge queue on; strict up-to-date off |

## Part B: scrutiny (what would have broken, and the fix in the plan)

| # | Issue found | Kind | Resolution in Part A |
|---|---|---|---|
| S1 | "P2 advisory" conflicts with the operator's standing rule "not-applicable only with a refutation or an owner on main" | contradiction | 1.1–1.2: every advisory P2 has an owner task on main; no rule changes until 8.1 |
| S2 | Plan 007 S6/S7 count ledger classes regardless of priority, so advisory rows would still trigger S1/S7 | contradiction | 1.4 interim exclusion stated in each record; 8.1 amends the rule (OP decision) |
| S3 | Re-sending TASK 935 to lift the hold would be amendment 2 under INV-6 ("AGMSG-TASKs after the first") and trip the reset | error | 5.1 uses a revise ACCEPTANCE referencing the first RESULT; no second TASK line |
| S4 | "One fix round" and "audit of the final head" conflict when the post-round audit finds a P0/P1 | ambiguity | 4.2: a surviving P0/P1 stops the PR (reset), never a second round |
| S5 | If step 2 is not done before 5.1, #328's amendment head gets a Bot review; one more P1 head reaches INV-6's two (count now 1) | risk | 2.2 before 5.1; if OP declines, the risk is stated in the record and #328 proceeds anyway |
| S6 | Step 7's generated threat table needs T704, whose own task text cannot use it | circularity | 6.2 exception stated |
| S7 | Rule text (SKILL, rules, AGENTS.md) is Claude-boundary: the orchestrator and Claude workers may not edit it | routing | 8.3 one operator patch, batched, instead of per-step rule edits |
| S8 | `make update` refuses a dirty main checkout; records are dirty between boundaries | mechanics | 5.6 after 5.5; `make update` only after a boundary |
| S9 | The local review is a second sampler; running it on every head re-adds findings | consistency | 4.2: once per PR final head; its P2 advisory; idempotent per head already |
| S10 | a002 idle since 05:39Z | omission | 5.3 uses it for #329's acceptance lines; after that it takes T704 or is removed |
| S11 | Draft PRs are not reviewed by the Bot; marking #346 ready triggers its one review | mechanics | 5.4 marks it ready deliberately |
| S12 | "At most one fix round per PR" is ambiguous for PRs with history | ambiguity | counted from the step's adoption; #328's amendment round is its one |
| S13 | The gate's audit grammar has no `fixed:`; an audit P2 needs a `not-applicable:` line | consistency | 1.2's wording fits the grammar |
| S14 | `resolve-threads.sh` replies must carry the owner wording | consistency | 1.2 |
| S15 | The strict rule forces one CI run per PR after each merge of a sibling | cost, bounded | 3.3 lists them: two runs in total |
| S16 | The scratchpad scripts remain the chain until 6.3, with known debts (the ff masker log) | debt | 6.3; no new scratchpad logic meanwhile |
| S17 | INV-2 caps for #329 | check | the fixtures split (#340) kept #329 within the caps per its validation; re-checked at 5.3 |
| S18 | Owner task files are orchestrator-authored | rule check | task files are the orchestrator's by the regime; boundaries are its exemption |
| S19 | After step 2, the chain's Bot wait must not block on a review that will never come | mechanics | integrate-prep's `BOT_WAIT_MAX` set low for update-branch heads; the sweep still lists old threads |
| S20 | Records staying local for a day | risk | files on disk, committed daily; acceptable |

## Part C: the operator's items, each at its moment

1. Now, before 5.1: read and set the Codex review trigger (2.1, 2.2) and tell me the values.
2. Now: decide 1.4's interim counting (advisory rows excluded from class counts until 8.1) — yes or no.
3. After 5.5: `make update` and restart Claude Code (5.6).
4. At step 8: apply the one patch of rules and design (8.3), then `make update` and restart.
5. At step 9 (optional): check merge-queue availability and set the ruleset.

Everything else is the orchestrator's or a worker's.

## Status

- 13:33Z Step 2 done by the operator (screenshot 22:29 JST before, "変更済" after): Codex code review for this repository: automatic review on, scope all PRs, trigger **Smart detection (experimental) → On PR open**, comprehensive review **on → off** (the source of the P2 threads: 31 of 66; Codex's default scope is P0/P1). Security review unchanged (automatic on, trigger on PR creation, severity floor high / manual medium). Verification 2.3 pending on the next pushed head.
- 13:33Z Step 1.4 (advisory rows excluded from the S7 class count until step 8 amends plan 007): no answer from the operator after two asks; proceeding on the stated default (excluded), recorded here and in each affected record; the operator may overrule at any time.
- Waiting for the operator's go to start step 1.

- 13:37Z Step 1.1 done: `dotfiles-T128-orchestrator-tools-followup-a01` and `dotfiles-T128-gate-evidence-followup-a01` written from their lineages' front matter, checker OK; 1.3 done: `fill_sweep.py` dispositions Codex P2/P3 as advisory owned by the PR's follow-up (map `followup-owners.tsv`: 328, 329, 346); step 5.0 `pr-cost.sh` written. The one pair round on the two files dispatched (seat + Codex in parallel).
- 13:41Z Codex round 1 on the owner tasks: two P1 (the owned section does not exist before acceptance; "empty" did not cover "missing"); applied to all three owner tasks; round 2 prepared (three hashes); Codex round 2 running; the seat's round 1 RESULT pending.
- 13:43Z Codex round 2: confirm on all three owner tasks (tools 44f746ce…, gate 4f68d63c…, playbook cb1d918a…; premises re-run match). The seat's round 1 (old hashes) still pending; round 2 (three hashes) goes to the seat on its RESULT. PR #329's record gained its 20 ledger rows (classes from titles).
- 13:50Z seat round 2: confirm on all three (bus 943; two P3 notes recorded as items for the next change: the brief's stop condition 1 did not list the path-row rewrite; the inherited non-path rows name a02's binaries and #329's tests, true once those land). Codex round 3 confirmed tools and gate and asked revise on the playbook file only because my prompt described its diff as one sentence; round 4 runs with the corrected prompt.
- 13:51Z step 1 done: the three owner tasks pair-confirmed (seat round 2, bus 943; Codex rounds 1 revise, 2 confirm, 3 confirm): tools ae208bef, gate 51c983df, playbook e22e0cc4. Boundary (12) runs now, then step 5.1.
- 14:01Z step 1.5 done: boundary (12) PR #348 merged (commit 13:56:40Z, observed by the chain 13:57:05Z) (main `4e7a9b3a`) with the three owner tasks, plans 018 to 021, the cost ledger; main checkout fast-forwarded, no dirty .orchestration file. Step 5.1 done: the #328 resume line (revise ACCEPTANCE 945 referencing RESULT 779 and the amended a04 on main c5dbc2c3…) read by a003 at 13:57:31Z; its one round is in progress. Step 2.3 (no Bot review on the pushed head) is checked at its push.
- 14:25Z step 2.3 verified: the worker pushed #328 head 65a3d71b at 14:03:49Z (87bce51e merge of origin/main 4e7a9b3a; e6602ca1 the amendment-1 sentences; 65a3d71b the task copy and revise-1 evidence); Bot reviews on it within 20 minutes = 0 (watcher, 14:24:31Z). CI 12 of 13 green at 14:24Z; the RESULT is pending.

- 14:33Z S21 (found at #328 5.2): plan 021 4.2 named the local review among the pre-round sources and only the post-round audit as the stop authority, while S9 ran the local review once on the final head; a P0/P1 from that post-round local run was not covered. Resolution, recorded before acting: the post-round local review is a sampler (RC1), not the acceptance authority; its P0/P1 is passed as input to the single audit of the head, which decides (its P0/P1 stops the PR; otherwise advisory, owned by the follow-up). Applied to #328 head 65a3d71b (local P1: the rule lacks "the orchestrator creates the acceptance record before the first dispatch").
- 14:44Z step 5.2 done: PR #328 (T703) merged 14:43:36Z as 26909ee4 after one revise round (14:03Z push), zero Bot reviews on the new head (step 2 holds), one local review (one P1, judged advisory by the audit), the audit (incorrect: two P2 dispositioned), thread resolution (16), gate rc=0. Two chain fixes on the way: finishing scripts accept a dispositioned incorrect audit; a transient GitHub API error on thread resolution was retried by re-running the idempotent step. Step 5.3 started: `integrate-329.sh 26909ee4` (update-branch, CI, local review, sweep, receipt, audit).
- 14:58Z step 5.3 in progress: #329 update-branched to 71eb920b (14:44:47Z), CI green, no Bot review (step 2 holds), local review 0 findings, sweep 37 items 0 gaps (all 20 Bot threads: 19 fixed on the branch, 1 not-applicable with evidence because T703 landed its fix on main first); the chain stopped on a tooling defect (macOS `seq 1 0` counts down, so a zero-finding local review failed the line check), fixed in the four scripts; receipt and audit running.
- 15:16Z step 5.3 done: PR #329 (T702) merged 15:15:01Z as 73f56c15 (update-branch head 71eb920b; no Bot review; local review 0; audit incorrect with two P2 dispositioned; 20 threads resolved). S22 found here: from this merge on, the gate on main requires the acceptance record to start with the JSON block (task, head, pr, ledger, searches recomputed by the gate over `classes:` lines, audit_findings with n as strings); until PR-B lands acceptance-front-matter.py the orchestrator writes the block by hand (done for #329; next for #346). Plan 007 Phase 1 closed. Step 5.4 started: `integrate-346.sh` (ready-for-review, update-branch, CI, the Bot's one review, local review, sweep, receipt, audit).
- 15:45Z step 5.4: the Bot's single review on ready-for-review (one P1, two P2) and the local review (two P1, two P2; one P1 shared); the one fix round sent to a003 for the two P1 (dispatch.sh tab-separated TASK guard; fill_sweep.py auto-dismissal of CI failures); four P2 advisory, owned by the tools follow-up.
- 16:19Z step 5.4 in progress: the revise head 7b574d32 passed CI; the local review found one P2 (boundary.sh deletions, already owned); sweep 10 items 0 gaps after the P1 row; three scratchpad-chain defects fixed on the way (the chain truncated the disposition table on re-runs; the audit precheck pulled sibling-slice audits of another PR into the lineage; the earlier macOS seq case): all S16 debt, retired with step 6.3. The audit of 7b574d32 is running; then the record block, gate, merge, the PR-B start line, boundary (13).
- 16:31Z step 5.4 stopped by the rule: the audit of 7b574d32 (a02 PR-A) found three P1 after the one round (fill_sweep.py review-body and issue-comment auto-dispositions; replies from any account supply dispositions; orch-audit.sh stale receipt), so plan 020 step 4.2 applies: no second round, INV-6's reset path (the review seat writes the successor with the three P1 as items; the worker continues on PR #346). The worker holds (ACCEPTANCE hold 16:31Z). Root cause: a02 item 1 made the orchestrator's scratchpad scripts the specification ("parameterised versions of the inputs"), so the scratchpad's trust gaps became the PR's; the successor re-specifies the trust rules instead of the inputs. The daily boundary (13) will carry the reset; the operator's make update (5.6) moves after the successor's merge.
- 16:52Z a05 pair-confirmed at eaac8e4b… (seat round 1, Codex on the same hash); reset record written (anchor bus 957); boundary (13) runs now, then the a05 line to a003.
- 18:00Z decision point (a05 Completion): the audit of #346's head 8576645c found a new P1 after the a05 round (dispatch.sh accepts tab or multi-space prefixes; regime-counters.sh:115 parses literal spaces, so such TASK lines escape INV-6's counts). Facts: a05 counters `results=1 revises=0` (INV-6 allows one revise under a05); the PR's one round of plan 020 was used under a02; three audits on three heads of this PR each found new P1 (7b574d32: 3, 8576645c: 1): the audit is a sampler too (RC1), an input to step 8 (scope the post-round audit to the fix diff). Options for the operator: A one revise round under a05 (about 45 min; then merge, any further P1 owned, no third round); B merge now with the P1 owned by the tools follow-up (latent until a tab-separated line is dispatched; the orchestrator's lines use spaces); C reset to a06 (about 1.5 h, the same sampling risk). Recommended A. Asked 18:00Z.
- 22:00Z operator: option A (one revise under a05, then merge whatever the next audit samples). Revise sent to a003 for the counters parser alignment.
- 22:21Z step 8 input: `scripts/agent-stop-gate.sh:277` (the Claude Stop hook) splits bus bodies on one space like the counters did; the same whitespace alignment belongs to the operator's rules/hook patch (Claude-boundary). The a05 revise RESULT (046901bc) is in integration.
- 22:35Z step 5.4 done: PR #346 merged 22:33:36Z as c586f20d (a05: one revise under the operator's option A; the final audit's P1 owned by the follow-up as decided). **Plan 020 step 5 complete: #328, #329, #346 merged.** Step 6.1 started: PR-B (acceptance-front-matter.py + orch-gate.sh) dispatched to a003 as a05's continuation on a fresh branch. Step 5.5/5.6: the next boundary (14) runs after 00:00Z (the daily cadence), then the operator's make update and restart.

## Step 8 inventory (collected 22:36Z; the one patch of rules and design, operator-applied)

- P2 advisory with an owner task; one fix round per PR; the post-round audit as the single authority; a surviving P0/P1 goes to the operator (the plan 020 merge rule) — SKILL step 10 and 15, `pr-integration.md`, AGENTS.md's review bullet.
- SKILL step 10.4: `AUDIT_DISPOSITIONS` retired for the record's `audit_findings` (the gate on main since 73f56c15); the record block's grammar (format 1; ledger ids are thread ids or `audit:<sha7>:<n>`, local-review rows stay in the prose).
- "No rule sentence names an unlanded mechanism" (M-19/C-21 class), and the standing items of the briefs (C-28, C-31, C-33) as SKILL text.
- Plan 007 S6/S7: advisory rows excluded from the class counts; S7 asks asynchronous with a default; blocking only for P0.
- Design INV-6: resets only on a failed deterministic check or an unfixed P0/P1; P2 never counts; the implementing_tasks map gains `dotfiles-T128-gate-evidence-followup-a01`; the post-round audit scoped to the fix diff (incremental), since audits sampled new P1 on four heads of PR #346.
- `scripts/agent-stop-gate.sh:277` (Claude Stop hook): split bus bodies on runs of whitespace like dispatch.sh and the counters (the worker's note, 22:20Z).
- The follow-up tasks' owner sections: the row location rule (the record the follow-up's item 1 names).
