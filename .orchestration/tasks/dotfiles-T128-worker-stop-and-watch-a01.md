---
format: 2
task_id: dotfiles-T128-worker-stop-and-watch-a01
kind: docs
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/unit/test_agmsg_orchestration_docs.py
after: [dotfiles-T128-process-rules-a03, dotfiles-T128-regime-counters-a02]
threat_table:
  - control: the PR edits the SKILL that Claude seats follow once it is applied
    disposition: "residual: the applied copy changes only after the merge and the operator's make update; before the merge the orchestrator's diff review and the audit from main judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each rule sentence with a token that fails when the sentence is removed"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py, the module that pins its own rule sentences, so it controls the oracle as well as the text
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the prose diff; main-tests is no control here, because the module is declared and would run only in dormant-contract mode"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-worker-stop-and-watch-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance)"
premises:
  - claim: "on 2026-10-11 the V0 worker kept fixing Bot findings through seven Bot-reviewed heads of PR 317, six of them after its park at 03:09Z, and never read the halt and park messages, because the only stop in Worker Playbook step 15 was the Bot's silence; the loop ended by despawn at 04:12Z"
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

# AGMSG-TASK dotfiles-T128-worker-stop-and-watch-a01 — Phase A7: the worker stops itself, the orchestrator watches

Plan 006 Phase A7 (operator's question 2026-10-11 07:0xZ: is there a rule that stops a worker on repeated findings and makes the orchestrator watch?). Review tier by INV-1 (the SKILL is listed by name): prose, the docs test, one schema audit of the final head. Dispatched only after `dotfiles-T128-process-rules-a03` (the same SKILL file) and `dotfiles-T128-regime-counters-a02` (the script the rule names) are on `main`. Claude seat, the free standard worktree, branch `docs/worker-stop-and-watch` from `origin/main`. Nothing here changes a hashed design sentence: INV-6's counts, thresholds, mandatory point (the merge gate) and early signal (the orchestrator's Stop hook) stay as they are; this task adds the worker's own stop and the orchestrator's watch as SKILL procedure, and leaves hook-level enforcement to V3a.

## A7-1 Worker Playbook step 15: the worker's own stop

Insert, before the bullet "Fix P0/P1 findings, inline or review-body, with a fix commit and start over from the push, at most twice":

- Before each fix commit the worker lists every top-level Codex Bot review comment of the PR (`gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments`, not only the current head's) and the PR's commits (`…/pulls/<n>/commits`), and counts two things: the distinct heads after its first RESULT's head that carry a Codex Bot P0 or P1 finding (the rule `scripts/regime-counters.sh` applies: `original_commit_id` of `chatgpt-codex-connector[bot]` comments whose title carries a P0 or P1 badge, in the PR's commit order), and the Bot thread title classes on the PR (the first three words of the title line, badge stripped, lower-cased). When the heads reach 2 (INV-6) or a class reaches 3 (plan 006 S1), the worker fixes nothing more: it sends `AGMSG-PONG v1 task_id=<id> status=blocked note=S1|INV-6 heads=<n> classes=<class:count,…> threads=<ids>` (the contract's `status=blocked` with its `note=`; no new field) and waits. The two stops release differently: after an S1 stop the orchestrator's ACCEPTANCE decides (a reset, a disposition or a threat-table row); after an INV-6 stop the worker stays stopped until INV-6's own release exists, a reset record naming a redesign by another context or the operator's waiver, never a disposition. The A2 cap of two fix rounds stays; whichever limit comes first ends the fixing.
- Before each push the worker runs `scripts/regime-counters.sh <task id> --history-only` from its worktree and pastes the count line into its validation file; an `S2:` line there is the same stop.

## A7-2 Orchestrator Playbook step 7: the watch

Replace "Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls." with:

- Track `max_turns` and watch every in-flight task from GitHub and history, never from panes, at the orchestrator's own action boundaries and at least every 30 minutes after a TASK: list the PR's commits, the Bot's reviews and the check runs (`gh api repos/{owner}/{repo}/pulls/<n>/commits`, `…/reviews`, `gh pr checks <n>`) and the task's PONGs in history. The cadence mechanism is one bounded background wait of at most 30 minutes per task between reads, never a foreground sleep loop; the watch reads state and never detects completion, which stays the RESULT's arrival through the Monitor or turn delivery. 45 minutes without a push, a PONG or a RESULT is a stall: send `AGMSG-PING v1` and wait one turn. A worker whose PING stays unread while it keeps pushing past the A2 cap or past an INV-6 count is stopped with `herdr-agents --remove-worker <worktree> --force` and the seat is re-created for the next task; the acceptance record names the PING id and the stop.

## A7-3 Tests

`tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest` gains two tests, section-scoped like the others: `test_the_worker_stops_itself_on_repeated_findings` (tokens in step 15: "fixes nothing more", "`status=blocked note=S1|INV-6`", "whichever limit comes first ends the fixing", "never a disposition", "not only the current head's", "`--history-only`") and `test_the_orchestrator_watches_from_github_and_history` (tokens in the Orchestrator Playbook: "at least every 30 minutes after a TASK", "never detects completion, which stays the RESULT's arrival", "45 minutes without a push, a PONG or a RESULT is a stall", "`herdr-agents --remove-worker <worktree> --force`"). Each fails when its sentence is removed.

## Validation

`prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md`; `uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v`; removal proofs for the ten tokens; the premises re-run and pasted (the gh one from outside the sandbox).

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-worker-stop-and-watch-a01/task.md`; evidence beside it.

## Completion

Draft PR within 30 minutes; `gh pr ready <n>` before the Bot wait; CI; the Bot wait under the A2 cap and under A7-1 itself (this PR is the first on which the worker counts); artifacts at the `expected_*` paths of the TASK message; `memory add`; RESULT via `agmsg-dispatch dotfiles-conformance <you> claude-deep-dot w5:p1` with the `--history-only` line pasted. max_turns=6. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.
