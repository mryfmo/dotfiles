---
reviewed_at: 2026-10-11T07:23:26Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4
task: dotfiles-T128-task-review-a7-a01
round: 1
files:
  - dotfiles-T128-worker-stop-and-watch-a01@381cb9a15b29b0403d584042c7d83219fa22fd96df56d498ac9b562f19fed441
verdicts:
  dotfiles-T128-worker-stop-and-watch-a01: "revise: 1 the PONG reason= field is not in the message contract; 2 the 30-minute watch must not read as the sleep loop the SKILL forbids"
---

# Task-file review: dotfiles-T128-worker-stop-and-watch-a01 (plan 006 Phase A7), one round

Stop condition against design v16 at 15957fbc, A1/A2 on PR 318's head aeb6c5ad, and A3's counting rule.

1. No contradiction with the design: INV-6's counts, thresholds, mandatory point and early signal are untouched; A7-1 adds a worker-side stop as procedure and A7-2 an orchestrator watch, both outside the hashed keys, as the task says. The worker's two counts are INV-6's Bot-head rule and plan 006's S1 class rule in A3's own words (chatgpt-codex-connector[bot] comments with a P0 or P1 badge grouped by original_commit_id after the first RESULT's head; first three words of the title, badge stripped, lower-cased), so the worker and the script count the same thing. A7-1 keeps the A2 cap ("whichever limit comes first"), and its insertion point and A7-2's replaced sentence exist verbatim on the PR head (the step-15 bullet once; step 7 identical on main and on the head, line 154 and 161).
2. Premises: premise 2 holds (line 203 on the PR head); premise 3 holds (report lines 10 and 21); premise 1's gh half is unverifiable from this seat and its read_at query is the delivery evidence the SKILL itself names, so it is not the forbidden count path.
3. allowed_files complete: the SKILL and the docs test; the rule file is untouched at its word budget; the test module already slices "Worker Playbook" and "Orchestrator Playbook" (lines 72-73), so the two section-scoped tests are possible as written. after: names the two tasks that must land first (the same SKILL file; the script the rule invokes).
4. Threat table: the three rows are a03's, real, with a03's compensating controls.
5. Items:
   - R1: A7-1's stop message is AGMSG-PONG v1 … status=blocked reason=S1|INV-6, and the Message Contract defines the PONG as status=alive|blocked note=<short-note>. Either carry the counts, heads and thread ids in note= (no contract change), or add reason= to the Liveness messages line in the same PR (the SKILL is in allowed_files); say which, or the worker asks. The stop gate reads only status=, so either form lets the worker's seat idle after the PONG.
   - R2: A7-2 reads "every 30 minutes after a TASK, list the PR's commits, the Bot's reviews and the check runs … and the task's PONGs". The SKILL's "Regime activation and progress" forbids ad-hoc polling sleep loops and pane reads for completion; A7-2 is a stall watch from GitHub and history, which that rule allows, but the sentence should say how the cadence runs (a scheduled check, a Monitor on the PR's checks, or the orchestrator's next action, never a foreground sleep) and that completion is still detected only from the RESULT, so the two paragraphs do not read against each other.
6. Note, not an item: herdr-agents --remove-worker <worktree> --force discards nothing committed, and the worker has pushed by construction when the watch fires; the acceptance record naming the PING id and the stop is the right trace.

Verdict ready once R1 and R2 are applied; neither touches a hashed sentence.
