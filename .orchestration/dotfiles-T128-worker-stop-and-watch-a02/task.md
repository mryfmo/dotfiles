---
format: 2
task_id: dotfiles-T128-worker-stop-and-watch-a02
kind: docs
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/fixtures/regime/worker-step-15.md
  - tests/fixtures/regime/orchestrator-step-7.md
  - tests/fixtures/regime/message-contract.md
  - .orchestration/dotfiles-T128-worker-stop-and-watch-a02/**
after: [dotfiles-T128-process-rules-a05, dotfiles-T128-regime-counters-a02]
reset_of: [dotfiles-T128-worker-stop-and-watch-a01]
threat_table:
  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, the rules Claude seats follow once it is applied
    disposition: "residual: the applied copy changes only after the merge and the operator's make update; before the merge the orchestrator's diff review and the audit from main judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each rule sentence with a token that fails when the sentence is removed"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py, the module that pins its own rule sentences, so it controls the oracle as well as the text
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the prose diff; main-tests is no control here, because the module is declared and would run only in dormant-contract mode"
  - control: the task-file copies on the branch (.orchestration/dotfiles-T128-worker-stop-and-watch-a01/task.md and .orchestration/dotfiles-T128-worker-stop-and-watch-a02/task.md)
    disposition: "residual: each copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the reset record names the a02 file's hash and the review seat's verdict=accept on it"
  - control: the three golden fixtures of the sections this task edits (tests/fixtures/regime/worker-step-15.md, tests/fixtures/regime/orchestrator-step-7.md and tests/fixtures/regime/message-contract.md), which test_regime_rule_sections_are_pinned_whole compares byte for byte, so the PR controls that oracle together with the text
    disposition: "residual: the fixture diff is read beside the SKILL diff by the orchestrator and the task-level audit; a fixture edit without the matching SKILL edit, or the reverse, fails the test"
  - control: review-derived text (Bot finding titles, class names, thread ids) that the worker places into AGMSG-PONG and AGMSG-RESULT notes and that agmsg-dispatch or send.sh then carries as a shell argument or body
    disposition: "residual: before anything review-derived enters a note the worker reduces it: a class name to [a-z0-9-], a thread id to digits, a Bot title never (only its reduced class); a note therefore holds only the fixed words S1|INV-6, counts, reduced class names and digits, so the inline agmsg-dispatch argument step 11 prescribes carries no review text, and nothing taken from a review body is executed (Bot thread 4244128851)"
  - control: herdr-agents --remove-worker --force on a crossed cap, an orchestrator in-process effect that step 7 triggers from GitHub and history state
    disposition: "residual: before any removal the orchestrator re-reads the PR number from the task's branch (gh pr list --head), compares the identity's registered worktree with the TASK's repo=, re-derives the counts from a fresh listing, preserves the stopped worktree's evidence and logs the removal in the acceptance record; the session runs auto mode (defaultMode: auto, ask: []), so the human prompt for this command is the settings ask rule of plan 007 T710 once it lands, not a property of this task (audit of 3a54d340 finding 2; plan 007 M-8, C-11)"
premises:
  - claim: "on 2026-10-11 the V0 worker kept fixing Bot findings through seven Bot-reviewed heads of PR 317, four of them after its park at 03:09Z, and never read the halt and park messages, because the only stop in Worker Playbook step 15 was the Bot's silence; the loop ended by despawn at 04:12Z"
    command: "gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[]|select(.user.type==\"Bot\")|[.commit_id[0:8],.submitted_at]|@tsv'; sqlite3 ~/.agents/skills/agmsg/db/messages.db \"select id, created_at, coalesce(read_at,'UNREAD') from messages where id in (407,408)\""
    output: |-
      32fe9a36	2026-10-11T02:37:13Z
      56ca6c69	2026-10-11T02:52:38Z
      de138f65	2026-10-11T03:03:00Z
      f6528bba	2026-10-11T03:10:28Z
      98f1d250	2026-10-11T03:24:14Z
      2602f575	2026-10-11T03:43:58Z
      e314c502	2026-10-11T04:04:13Z
      407|2026-10-11T03:27:02Z|UNREAD
      408|2026-10-11T03:46:22Z|UNREAD
  - claim: "Worker Playbook step 15 on PR 318's head already has the worker list the Bot's reviews and top-level comments of its head with gh api (through the permission gate, as every gh call of a Claude seat), so a worker-side count of Bot P0/P1 heads and thread classes needs no new sandbox exit"
    command: "git show origin/docs/regime-pattern:home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep -n 'Then list the Bot' | cut -c1-400"
    output: |-
      203:    - Then list the Bot's reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.type=="Bot" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot" an
  - claim: "scripts/regime-counters.sh (PR 319) reads the whole team history through the storage facade and its --history-only mode ran from the worker worktree in the A3 worker's own validation, so a worker can run it before a push without GitHub"
    command: "grep -n 'storage_history\\|live store\\|from the worktree\\|--history-only' .orchestration/reports/dotfiles-T128-regime-counters-a01.md | head -4 | cut -c1-200"
    output: |-
      10:1. `scripts/regime-counters.sh` (new, 149 lines, shdoc header, shellcheck and shfmt clean). `<task id> [--team] [--pr] [--history-only] [--reset-hash <sha256>] [--history-file <tsv>] [--github-file
      21:- invariant: INV-6 → scripts/regime-counters.sh:85 (history through `storage_history`, the whole team, no `--limit`; schema guard :83)
---

# AGMSG-TASK dotfiles-T128-worker-stop-and-watch-a02 — Phase A7, the reset continuation: the worker stops itself, the orchestrator watches

Plan 006 Phase A7 (operator's question 2026-10-11 07:0xZ: is there a rule that stops a worker on repeated findings and makes the orchestrator watch?). Review tier by INV-1 (the SKILL is listed by name): prose, the docs test, one schema audit of the final head. Dispatched only after `dotfiles-T128-process-rules-a03` (the same SKILL file) and `dotfiles-T128-regime-counters-a02` (the script the rule names) are on `main`. Claude seat, the free standard worktree, branch `docs/worker-stop-and-watch` from `origin/main`. Nothing here changes a hashed design sentence: INV-6's counts, thresholds, mandatory point (the merge gate) and early signal (the orchestrator's Stop hook) stay as they are; this task adds the worker's own stop and the orchestrator's watch as SKILL procedure, and leaves hook-level enforcement to V3a.

a02 is the INV-6 reset continuation of `dotfiles-T128-worker-stop-and-watch-a01` (reset record `.orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a01-design-reset.md`: RESULT 664, the revise-round RESULT 666, and a second revise RESULT would be revises 2), written by the review seat (`dotfiles-T128-worker-stop-and-watch-redesign-a01`). Same worker (`claude-standard-dot-a003`), same branch and PR (`docs/worker-stop-and-watch`, #323), continuing from head `e924c5df`, where A7-1 to A7-3 stand as the revise round left them; A7-4 below carries the three text changes the fourth Bot pass asked for. Thread 4244248692 (a threat row for the forced removal) is answered by the sixth row: the forced removal is an orchestrator in-process effect that step 7 triggers from GitHub and history state, so it has a row like any other controlled effect (SKILL line 71), and its residual names the pre-removal verification and the permission mode as they are (auto; the ask rule is plan 007 T710), not a human-only gate.

## A7-1 Worker Playbook step 15: the worker's own stop

Insert, before the bullet "Fix P0/P1 findings, inline or review-body, with a fix commit and start over from the push, at most twice":

- Before each fix commit the worker lists every top-level Codex Bot review comment of the PR (`gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments`, not only the current head's), every Codex Bot review body that carries a P0 or P1 badge (`…/pulls/<n>/reviews`, attributed to the review's `commit_id`, counted toward the fix cap and the classes, never INV-6's heads, which the gate derives from `review_comment` items only), and the PR's commits (`…/pulls/<n>/commits`), keeps only the comments whose `original_commit_id`, and the review bodies whose `commit_id`, is at or after the task's first commit on the PR (the task.md copy; a reset successor therefore never inherits its predecessor's heads or classes, inline or review-body, which the reset record discharged), and counts two things: the distinct heads after its first RESULT's head that carry a Codex Bot P0 or P1 finding (the rule `scripts/regime-counters.sh` applies: `original_commit_id` of `chatgpt-codex-connector[bot]` comments whose title carries a P0 or P1 badge, in the PR's commit order), and the Bot thread title classes on the PR (the first three words of the title line, badge stripped, lower-cased). When the heads reach 2 (INV-6) or a class reaches 3 (plan 006 S1), the worker fixes nothing more: it sends `AGMSG-PONG v1 task_id=<id> status=blocked note=S1|INV-6;heads=<n>;classes=<class:count,…>;threads=<ids>` (the contract's `status=blocked` with everything inside its `note=`, semicolon-separated; no new field) and waits. The two stops release differently: after an S1 stop the worker resumes only on an ACCEPTANCE that follows plan 006 S1 (the orchestrator's re-examination at `xhigh`, a cause record under `.orchestration/learning/`, and a changed task or plan step), never for a fourth round of the same class; after an INV-6 stop the worker stays stopped until INV-6's own release exists, a reset record naming a redesign by another context or the operator's waiver, never a disposition. The A2 cap of two fix rounds stays; whichever limit comes first ends the fixing.
- Before each push the worker runs `scripts/regime-counters.sh <task id> --history-only` from its worktree and pastes the count line into its validation file; an `S2:` line there is the same stop.

## A7-2 Orchestrator Playbook step 7: the watch

Replace "Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls." with:

- Track `max_turns` and watch every in-flight task from GitHub and history, never from panes, at the orchestrator's own action boundaries and at least every 30 minutes after a TASK: list the PR's commits, the Bot's reviews, its top-level review comments and the check runs (`gh api repos/{owner}/{repo}/pulls/<n>/commits`, `…/reviews`, `…/pulls/<n>/comments`, `gh pr checks <n>`; once A3 is on `main`, `scripts/regime-counters.sh <task id> --pr <n>` gives the same counts in one line) and the task's PONGs in history, so an INV-6 head count crossed by a worker that ignores its PING is seen from the inline P0/P1 threads. The cadence mechanism is one bounded background wait of at most 30 minutes per task between reads, never a foreground sleep loop; the watch reads state and never detects completion, which stays the RESULT's arrival through the Monitor or turn delivery. 45 minutes without a push, a PONG or a RESULT is a stall: send `AGMSG-PING v1` and wait one turn. A worker whose PING stays unread while it keeps pushing past the A2 cap or past an INV-6 count is stopped with `herdr-agents --remove-worker <worktree> --force` and the seat is re-created for the next task; the acceptance record names the PING id and the stop.

## A7-4 The three text changes of the fourth Bot pass on `e924c5df` (this reset)

Each replacement is stated against the SKILL as it stands on `e924c5df`; the fixture of each section is updated in the same commit.

1. Thread 4244248703, step 15 (the listing bullet): replace "every Codex Bot review body that carries a P0 or P1 badge (`gh api --paginate …/pulls/<n>/reviews`, attributed to the review's `commit_id`, counted toward the fix cap and the classes, never INV-6's heads, which the gate derives from `review_comment` items only)" with "every Codex Bot review body that carries a badge, P0 to P3 (`gh api --paginate …/pulls/<n>/reviews`, attributed to the review's `commit_id`, counted toward the classes at any priority and toward the fix cap at P0 or P1, never INV-6's heads, which the gate derives from `review_comment` items only)". The class count thus reads every badged Codex finding on the PR since the task's first commit, inline or review-body; the fix cap and INV-6's head count stay P0/P1, the heads inline `review_comment` items. Token: in `test_the_worker_stops_itself_on_repeated_findings`, replace "counted toward the fix cap and the classes, never INV-6's heads" with "counted toward the classes at any priority and toward the fix cap at P0 or P1, never INV-6's heads" and add "carries a badge, P0 to P3".
2. Thread 4244272551, step 7: replace "and, for INV-6's audit-head component (which `scripts/regime-counters.sh` prints as `audits=unknown`), the task's audit documents `.orchestration/validation/<task>-audit-<sha7>.json` in the main checkout, each counted only when its sha256 matches its `AGMSG-AUDIT` record," with "and INV-6's audit-head component read as the counters bullet prescribes (the script's `audits=` when it prints one; otherwise the record's pasted reading of the source INV-6 names for it, or of the interim record the orchestrator used in its place),". The sentence names no file format; the counters bullet owns that reading. Token: in `test_the_orchestrator_watches_from_github_and_history`, add "read as the counters bullet prescribes" and remove any token taken from the replaced clause.
3. Thread 4244248706, Message Contract v1: the RESULT line becomes `AGMSG-RESULT v1 task_id=<id> status=ready_for_review|blocked head=<full sha>` and the `AGMSG-RESULT v1` fields paragraph gains the sentence "`head=<full sha>` is mandatory: the first RESULT's head is INV-6's baseline, the sha the counters read." Token: a sibling of `test_question_pongs_are_in_the_contract`, `test_result_head_is_in_the_contract`, asserts "head=<full sha>" and "the first RESULT's head is INV-6's baseline" in the Message Contract section; `tests/fixtures/regime/message-contract.md` is updated in the same commit.

## History

a01 (PR #323) went through two Bot fix rounds and one revise round (RESULTs 664 and 666; class-count scope under plan 006 S1 reverted to the Codex Bot's items); the fourth Bot pass on `e924c5df` left four P2 threads, three of them text changes, and the RESULT carrying them would be revises 2, so a01 was reset under INV-6 and the review seat's redesign (`dotfiles-T128-worker-stop-and-watch-redesign-a01`) is this file, a01 plus A7-4 and the bookkeeping.

## A7-3 Tests

Step 15, step 7 and the Message Contract are pinned whole by a05's item 10 (`tests/fixtures/regime/worker-step-15.md`, `orchestrator-step-7.md`, `message-contract.md`, compared by `test_regime_rule_sections_are_pinned_whole`): the same commit that changes the sections updates the three fixtures to the new text, and the RESULT lists them (a declared change, INV-12).

`tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest` gains two tests, section-scoped like the others: `test_the_worker_stops_itself_on_repeated_findings` (tokens in step 15: "fixes nothing more", "`status=blocked note=S1|INV-6`", "whichever limit comes first ends the fixing", "never a disposition", "never for a fourth round of the same class", "not only the current head's", "and the review bodies whose `commit_id`, is at or after the task's first commit on the PR", "counted toward the fix cap and the classes, never INV-6's heads", "`--history-only`") and `test_the_orchestrator_watches_from_github_and_history` (tokens in the Orchestrator Playbook: "at least every 30 minutes after a TASK", "`…/pulls/<n>/comments`", "never detects completion, which stays the RESULT's arrival", "45 minutes without a push, a PONG or a RESULT is a stall", "`herdr-agents --remove-worker <worktree> --force`"). Each fails when its sentence is removed.

## Validation

`prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md`; `uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v`; removal proofs for every token A7-3 and A7-4 pin; `test_regime_rule_sections_are_pinned_whole` green with the three fixtures updated in the same commit; the premises re-run and pasted (the gh one from outside the sandbox).

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-worker-stop-and-watch-a02/task.md` (the `…-a01/` directory stays as history); evidence beside it.

## Completion

From `e924c5df`, one commit for the task copy, the three text changes of A7-4, the three fixtures and the tokens; CI; the Bot wait under the A2 cap and under A7-1 itself (a further finding of the `class-count-scope` kind, that the worker's count is narrower than S1's scope, is reported with its class, not fixed); artifacts at the `expected_*` paths of the TASK message; `memory add`; `AGMSG-RESULT v1 task_id=dotfiles-T128-worker-stop-and-watch-a02 … head=<full sha> reset_of=dotfiles-T128-worker-stop-and-watch-a01` via `agmsg-dispatch dotfiles-conformance <you> claude-deep-dot w5:p1`, with the complete `--history-only` output pasted, listing 4244248703, 4244272551 and 4244248706 as `fixed:<that sha>` and every earlier thread as RESULT 666 listed them. max_turns=6. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.
