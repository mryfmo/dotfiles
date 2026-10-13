# Acceptance: dotfiles-T128-playbook-rules-a04 (plan 007 T703, INV-6 successor of a03 after plan 010 option D) — in progress

- **Task:** `.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md` sha256 `e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254`, written by the review seat (`dotfiles-T128-playbook-rules-redesign-a03`, anchor 15:23:59Z); reset record `dotfiles-T128-playbook-rules-a03-design-reset.md`; C1 to C9 OK.
- **Worker:** `claude-standard-dot-a003` at `.claude/worktrees/worker-c`, continuing on `regime/playbook-rules` (PR #328, held at `fe34f7db`; PR head `e12872cd`).
- **Precondition:** the boundary commit that lands a04 and the reset record (INV-2).
- counters: run before the first acceptance action.
- cost: n/a (pending)
- dispatch (C-12 form; pasted 15:41Z): `  ○ [2026-10-12T15:40:52Z] claude-deep-dot → claude-standard-dot-a003: AGMSG-TASK v1 task_id=dotfiles-T128-playbook-rules-a04 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_fi`; preconditions met: boundary PR #333 merged 15:39:49Z as `3709a6d8` (a04 and the a03 reset record on main).
- 2026-10-12 16:04:45Z RESULT (bus 779): `status=ready_for_review head=2276a365`; CI 12 green; the worker's four a03 threads `fixed:beee078a`. 16:03:26Z Bot review 5493270947 on 2276a365: thread 4250028600 P1 (`SKILL.md:74`: the counters' S1 candidate is review-title text, the rule wants a slug). Class at disposition time: `search-procedure` (also `unlanded-mechanism-stated-as-present`), the next row after the third S1 cycle → S7, plan 012; M-20261012-23 / C-25. Counters 16:07:36Z: `tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0`.
- 2026-10-13 01:05Z operator: plan 012 option B. No ACCEPTANCE line to the worker yet: a04 is held unchanged until `dotfiles-T128-orchestrator-tools-a01` (T718's first slice: counters slug, three-repeat.sh, bus-read.sh, dispatch.sh) merges; then `gh pr update-branch 328`, Bot, sweep (4250028600 → `fixed:<T718 squash sha>`), audit, gate. The worker a003 takes T718 on a fresh branch meanwhile (its worktree keeps `regime/playbook-rules`).

- 01:45Z ACCEPTANCE sent to a003 (bus 809, created 01:48:18Z): `status=accepted` (head 2276a365 is the final text under plan 012 B; thread 4250028600 closes when T718 a01 lands; integration by the orchestrator after that merge; no worker action on a04). Sent because the Stop gate requires one ACCEPTANCE per RESULT and the deliverable itself needs no change.

- 10:12Z T718 first slice merged (a03c1daa); `integrate-328.sh a03c1daa`: update-branch to `7771082f` (09:58:25Z), CI 13 green, Bot review 5501887212 (10:03:30Z) with three new threads on the a04 rule text: 4257278283 (P1, SKILL.md:69, the task-file review's invariant check compares ids only where the design (regime-v3-a01:56) requires byte-for-byte sentence equality), 4257278271 (P2, SKILL.md:164, "thirty minutes" where the design (:64) limits worker idleness to 20; INV-10's 30 is the first-push deadline), 4257278276 (P2, SKILL.md:71, the row unit per `allowed_files` entry lets one wildcard row cover several trust-boundary scripts); the C-32 local review of 7771082f (`dotfiles-T128-playbook-rules-a04-local-review-7771082.md`): one P2 (SKILL.md:164, `history.sh --limit 1000` is not a complete read after compaction; a read at its limit must be refused or paginated). Lines 69, 71 and 164 follow the a04 task text (line 78: "thirty minutes", the "complete bus read … --limit"; the invariant check as ids), so the fixes need amendment 1 of a04 (INV-6: amendments=0, revises=0 before it) and one revise round; the G′ pattern of plan 016 applies: owner first (a follow-up rules task on main owns the residual P2 of the final head by ledger reference), then the fix under the guards on the same PR. S6 searches pasted below.

4257278283	design-mismatch
4257278271	design-mismatch
4257278276	threat-row-unit
local:7771082:1	default-limited-read

```text
$ /usr/bin/grep -rl 'classes:.*design-mismatch' .orchestration/learning/mistakes/
(no file)
$ /usr/bin/grep -rli -- 'design-mismatch' .orchestration/learning/mistakes/
(no file)
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- design-mismatch | grep -cE '^[0-9a-f]{8}-'
0
$ /usr/bin/grep -rl 'classes:.*threat-row-unit' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-14.md
$ /usr/bin/grep -rli -- 'threat-row-unit' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-29.md
.orchestration/learning/mistakes/M-20261012-14.md
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- threat-row-unit | grep -cE '^[0-9a-f]{8}-'
0
$ /usr/bin/grep -rl 'classes:.*default-limited-read' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-33.md
$ /usr/bin/grep -rli -- 'default-limited-read' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-33.md
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- default-limited-read | grep -cE '^[0-9a-f]{8}-'
0
$ scripts/regime-counters.sh dotfiles-T128-playbook-rules-a04 --pr 328
task=dotfiles-T128-playbook-rules-a04 tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=2276a365cba9f104cadd7cd82f3fb0bfec7dac21 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-12T15:40:52Z..2026-10-12T16:04:45Z (0:23) source=live
```

## Ledger (machine rows id<TAB>class; the lineage a01 → a04 on PR #328, classes assigned from the thread titles at 10:17Z; the four rows of 7771082f are above)

4247933544	threat-row-unit
4247933561	design-mismatch
4247933574	search-procedure
4248319926	search-procedure
4248319936	wall-clock
4248711363	unlanded-mechanism-stated-as-present
4248711371	unlanded-mechanism-stated-as-present
4249303398	search-procedure
4249303413	default-limited-read
4249303426	wall-clock
4249303433	search-procedure
4249414388	search-procedure
4250028600	search-procedure
- 10:21Z decision pending (plan 017; S7 by the letter: `design-mismatch` at three on the lineage ledger beside `search-procedure` at six): the G′ pattern as the default (amendment 1 + the owner task `dotfiles-T128-playbook-rules-followup-a01` + one revise), the pair review of both drafts running (seat TASK and Codex half). The checker's C10 hit on item 3 (`regime-counters.sh` beside `; evidence=<command>`) is on main's copy too (pre-existing, outside the amendment). The awaiting-merge marker for #328 was removed deliberately: the head moves with the amendment round, so boundary (11) may run before it.
- 10:30Z operator: plan 017 option G″ (the G′ pattern on this PR): amendment 1 + the owner task first on main, one revise round, residual P2 owned by `dotfiles-T128-playbook-rules-followup-a01`.
- 10:32Z pair round 1 on the drafts: seat `revise` (P2 the owner task's premise 2 counted rows that exist only in the working tree and item 1 named no greppable source; P3 the history paragraph's "thirty minutes" without a superseded marker; P3 item 4's clause vs the fixtures wildcard row), Codex `revise` on the amendment (the same history leftover) and `confirm` on the owner task. Applied: premise 2 is a presence check on origin/main; item 1 is the `## Owned by dotfiles-T128-playbook-rules-followup-a01` section of this record (`<id>\t<class>` rows) landed by the boundary after a04's merge, the dispatch condition stated; the superseded parenthetical on line 74; item 4's clause scoped to executed or applied wildcards (data wildcards keep one row). Round 2 sent 10:32:02Z (a04 `c5dbc2c3…`, owner `cb32794d…`).
- 10:33Z INV-6 with GitHub: `bot_p1_heads_after_result=1` (7771082f); a P1 on the amendment head would reach two (reset). The map agent's record check raised it; the counters inside the sandbox print `unknown` (no gh), outside they print the figure.
- 10:34Z pair-confirmed: a04 amendment 1 at `c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa`, the owner task at `cb32794d2bb939456e747230e012729d47c327946fbe07fe97d644969dc4fa42` (seat round 2, bus 933; Codex round 2). ACCEPTANCE sent; boundary (11) runs now, then the amendment line to a003.
- 14:01Z plan 021 step 5.1: resume line (bus 945, revise referencing RESULT 779) read 13:57:31Z; the worker merges origin/main (4e7a9b3a), applies amendment 1 (items 1, 4, 5, Completion) with the token tests, pushes; the Bot reviews on PR open only now (operator setting 13:3xZ), so the new head gets no Bot round; the local review runs once on it; dispositions: the P1 and two P2 threads and the local finding `fixed:<sha>`; any new P2 → advisory, owned by `dotfiles-T128-playbook-rules-followup-a01`.

local-finding: 7771082:1 fixed:e6602ca1 (local review of 7771082f, SKILL.md:164: the read refused at its limit, never a default-limited or silently truncated one)

## Owned by dotfiles-T128-playbook-rules-followup-a01 (advisory findings of the final head; plan 020 step 1.2; rows id<TAB>class)

local:65a3d71:1	rule-gap
audit:71eb920:1	procedure-migration (the SKILL step 10.4 gate command still names AUDIT_DISPOSITIONS; from the audit of PR #329's head)

local-finding: 65a3d71:1 not-applicable:P1 by the post-round local review (SKILL.md:164: the rule requires dispatch logging into the current acceptance record and the tools refuse a missing record, but no sentence says the orchestrator creates the record before the first dispatch); plan 021 S21: the local review is a sampler and not the acceptance authority, so this finding is referred as input to the audit of this head, which decides; if the audit raises it as P0/P1 the PR stops (plan 020 step 4.2), otherwise it is advisory and owned by dotfiles-T128-playbook-rules-followup-a01; evidence=sed -n 1,20p .orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-65a3d71.md

- 14:41Z audit of 65a3d71b (`dotfiles-T128-playbook-rules-a04-audit-65a3d71.md`): `Verdict: incorrect`, two P2, no P0/P1: (1) orchestration: thread 4250028600's `fixed:a03c1daa` cites a commit outside base..head (the gate rejects it); corrected to a `not-applicable` with evidence that the base contains the fix; (2) specification: the post-round local P1 (SKILL.md:164, the acceptance record's creation before the first dispatch is implicit) is judged advisory, owned by `dotfiles-T128-playbook-rules-followup-a01`, not merge-blocking; INV-2, INV-10, INV-12 hold on the head; all 47 documentation tests pass; CI 12 checks plus the CodeRabbit skip. Both dispositioned below; the chain continues to the gate and the merge.

audit:65a3d71:1	disposition-range
audit:65a3d71:2	rule-gap

audit-finding: 1 not-applicable:corrected in the sweep table at 14:41Z: thread 4250028600 now reads not-applicable with the evidence that T718's squash a03c1daa is an ancestor of this PR's base 4e7a9b3a (the gate accepts fixed:<sha> only inside base..head); the re-run sweep carries the corrected row; evidence=grep -n 4250028600 .orchestration/validation/dotfiles-T128-playbook-rules-a04-pr-feedback.json
audit-finding: 2 not-applicable:advisory per the audit itself (no P0/P1): the rule gap "the orchestrator creates the lineage's acceptance record before its first dispatch" is owned by dotfiles-T128-playbook-rules-followup-a01 (row local:65a3d71:1 under the owner heading of this record); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'
- 14:43:36Z **merged as `26909ee4`** (`gh pr merge --squash --match-head-commit 65a3d71b`) after the gate (rc=0; the sweep re-run after the 16 thread replies: 65 items, 0 gaps). ACCEPTANCE `accepted` sent to a003 (14:44Z). Cost line appended to `.orchestration/metrics/pr-cost.tsv`. The owner section carries one advisory row (local:65a3d71:1, the record-creation sentence) for `dotfiles-T128-playbook-rules-followup-a01`.