---
format: 2
task_id: dotfiles-T129-integration-seat-result-gate-cap-a01
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/dot_local/bin/common/executable_herdr-agents
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - home/dot_config/claude/rules/agmsg-orchestration.md
  - scripts/orchestrator/integrate-seat.sh
  - scripts/orchestrator/result-precheck.sh
  - tests/unit/test_integration_seat.py
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/**
after: []
threat_table:
  - control: "the PR edits home/dot_agents/agent-config.yaml in one place (a new top-level key worker_cap: 4 beside worker_kind; no claude.* or codex.* block changes)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap"
  - control: "the PR edits home/dot_local/bin/common/executable_herdr-agents (--add-worker reads worker_cap from the manifest and refuses the seat that would exceed it, counting the worker identities registered at worktrees of the repository)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap"
  - control: "the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md in the named sentences only (the two seat-count sentences, the exemption bullet, the integration-seat role paragraph, the thread sentence of Worker Playbook step 15, the step-10 pointer)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat"
  - control: "the PR edits home/dot_config/claude/rules/agmsg-orchestration.md in the Delegation and Acceptance bullets only (the exemption list and the integration sentence), a rules file every Claude seat reads"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat"
  - control: "the PR adds scripts/orchestrator/integrate-seat.sh (item 1: the chain a seated integration worker runs for one PR, each step one existing script, writing the integration record and sending the integration RESULT)"
    disposition: "closed: tests/unit/test_integration_seat.py::test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges"
  - control: "the PR adds scripts/orchestrator/result-precheck.sh (item 2: the worker-side receipt and the orchestrator-side verification that refuse a RESULT whose head is not ready)"
    disposition: "closed: tests/unit/test_integration_seat.py::test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt"
  - control: "the PR adds tests/unit/test_integration_seat.py (the two tests above, fixtures written by the test, stub gh and stub scripts on PATH, a temporary git repository)"
    disposition: "residual: fixtures and stubs written by the test; the audit reads each case against items 1 and 2"
  - control: "the PR edits tests/unit/test_herdr_agents.py (the cap test and the text-consistency test above)"
    disposition: "residual: the tests run herdr-agents as a subprocess with stub identities and read the SKILL, the rule and the manifest from the checkout; the audit reads each case against item 3"
  - control: "the inputs of integrate-seat.sh and result-precheck.sh as a trust boundary (PR-controlled content: the PR diff, Bot thread bodies, check-run conclusions, the RESULT line's fields, the task id, the PR number and the head sha they take as arguments)"
    disposition: "closed: tests/unit/test_integration_seat.py::test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the two scripts and herdr-agents as subprocesses on fixtures in a temporary directory with stub gh, stub identities and stub scripts on PATH, and import only the standard library; nothing is imported into another process; no live seat, pane or GitHub object is touched by a test"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run bash, git, gh, jq and the main checkout's orchestrator scripts as the glue runs them today; the manifest key is read with the same yaml reader herdr-agents already uses"
  - control: new or renamed scripts
    disposition: "residual: 2 new scripts under scripts/orchestrator, both named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5), by the orchestrator alone; integrate-seat.sh contains no merge command and the Claude worker deny rules keep gh pr merge from the seat"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10); under item 1 the integration seat runs it and records the new head"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: the SKILL on origin/main carries two seat-count sentences (about three concurrent workers; at most three workers in total), both out of step with the four seats of today, so item 3 replaces them with the manifest value
    command: 'git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -nE ''about three concurrent workers|at most three workers'' | cut -d: -f1'
    output: |-
      31
      38
  - claim: the manifest on origin/main has no worker cap key and herdr-agents enforces none, so item 3 adds both
    command: printf '%s\n' "$(git show origin/main:home/dot_agents/agent-config.yaml | /usr/bin/grep -c '^worker_cap:')" "$(git show origin/main:home/dot_local/bin/common/executable_herdr-agents | /usr/bin/grep -c 'worker_cap')"
    output: |-
      0
      0
  - claim: the SKILL on origin/main keeps thread resolution from the worker (the sentence item 1 changes for the integration seat)
    command: git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c 'The worker resolves no thread'
    output: |-
      1
  - claim: no pre-RESULT gate exists on origin/main (no result-precheck script), so item 2 adds one
    command: git show origin/main:scripts/orchestrator/result-precheck.sh > /dev/null 2>&1 && echo present || echo absent
    output: |-
      absent
---

# AGMSG-TASK dotfiles-T129-integration-seat-result-gate-cap-a01 — the integration seat, the pre-RESULT gate and the numeric worker cap (plan 023 PR F4, one PR)

Written 2026-10-17 by the orchestrator seat from the operator's directive of 2026-10-17 21:32 JST (throughput; one batch, approved). Basis stated there: of 98 ACCEPTANCE lines today 34 were revise, 42 pending-integration and 22 accepted; one task took 9 to 15 round trips (#375 open for 10.9 hours); code PRs merge at about one per hour, serially, none since 16:57 JST; at 21:19 two seats were idle waiting on the orchestrator and now all four are; under the strict up-to-date policy every merge sends every in-flight PR back through update-branch, CI and the Bot wait; the orchestrator's single turns over 47 minutes are the serial point. Routing (Orchestrator Playbook step 3): no file of this task is a Claude permission boundary (no `claude.permissions`, `claude.sandbox` or `claude.hooks` block, no permgate, no rendered settings), so the free Claude seat takes it; the rule and SKILL are shared prose. Worker: claude-standard-dot-a006 (worker-f). Sequencing: this PR goes before dotfiles-T129-orchestrator-load-mechanisms-a01 (F3, queued on a004), which edits the same Delegation and Acceptance bullets; F3 is amended after this PR merges (its item 3, the background `integrate.sh`, is re-scoped to this PR's integration-seat entry). `scripts/validate-agent-assets.py` and its test are in flight in PR #389 and in dotfiles-T130-claude-sandbox-integration-a01, so the cap-to-text consistency check of item 3 is a unit test here, not a validator rule (pairwise-disjoint files); the operator may move it later.

## Goal

A seated integration worker runs everything between a worker's RESULT and the merge except the acceptance judgment, the audit's dispositions and the merge command; a worker's RESULT is refused mechanically when its head is not ready; the number of seats is a manifest value that `herdr-agents --add-worker` enforces and the texts repeat exactly.

## Files

1. `scripts/orchestrator/integrate-seat.sh <task> <pr> [--owner <followup task id>]` (new): the chain the integration seat runs for one PR, each step one command under `set -e`, each an existing script run from the seat's own worktree at `origin/main`: `gh pr update-branch` when the PR's base is behind `origin/main` (recorded as the new head; the Bot wait restarts from it only when the diff head changed), the CI wait (`gh pr checks --watch`, restarted on "no checks reported"), the Bot wait of Worker Playbook step 15 (the reviews and top-level comments of the head, 15 minutes at most, listed at most every 30 seconds), the sweep (`scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json`), the local review once per head (`scripts/orchestrator/local-review.sh`, with `scripts/orchestrator/local-advisory.sh` for the P2 of the owner rule), the dispositions (`fixed:<sha>` from the RESULT's thread list; `not-applicable:advisory P2 owned by <owner>` for a later review's P2 or a first review's P2 outside the C-50 case; a P0/P1 without `fixed:` stops the chain), the thread replies and resolution (`scripts/orchestrator/resolve-threads.sh <pr> <dispositions.tsv> - <sweep.json>`), the receipt (`review-receipt` in the glue's crit-data shape, from the seat's summary of the diff) and the record block (`scripts/orchestrator/acceptance-front-matter.py`, or the glue's `record-block.py` where the gate still reads it). It never runs the audit (the orchestrator's `orch-audit.sh` or `herdr-agents --audit`), the gate or `gh pr merge`; it writes `.orchestration/validation/<task>-integration-<sha7>.md` (every step's command, rc and pasted output, the final head, the sweep and receipt paths) and ends by sending `AGMSG-RESULT v1 task_id=<task> kind=integration status=ready_for_audit head=<sha> record=<that file>` to the orchestrator with `agmsg-dispatch`, or `status=blocked step=<name> rc=<n>` at the first failing step. The orchestrator then runs the audit on that head, dispositions its findings, runs the gate and merges with `gh pr merge --squash --match-head-commit <audited head>`: the only three integration steps left to it.
2. `scripts/orchestrator/result-precheck.sh run <task> <pr> <head>` (new; run by the worker before its RESULT) checks, each with its pasted command and output: (a) the task copy on the branch has the dispatched sha256 (the TASK line's `task_sha256`, read from the bus); (b) every changed file is inside `allowed_files`; (c) the caps of the task's Check hold (`git diff --numstat origin/main...<head>`); (d) every command of the Check has its output in the validation file; (e) CI is green on `<head>`; (f) the Bot's review of `<head>` exists, or the 15-minute wait is recorded; (g) every P0/P1 thread on the head is `fixed:<sha>` or listed `open:` with `bot_rounds=2`, and every P2 has a proposed disposition; (h) `scripts/orchestrator/local-review.sh` ran on the head with no P0/P1, or its lines are filed; (i) the audit dry run: the task-level audit prompt run read-only against the head with `codex exec --sandbox read-only` when `codex` is on PATH and reachable, its verdict pasted, otherwise the line `audit-dry-run: unavailable (<reason>)`. It writes `.orchestration/<task>/precheck-<sha7>.md` with every check as `ok` or `missing`, and (h) and (i) also as `unavailable (<reason>)` when the seat has no codex (a Claude seat cannot run the local review or the audit dry run; Amendment 2), and exits 1 on any `missing`, naming them; the RESULT line carries `precheck=<sha256 of that file>`. `result-precheck.sh verify <task> <result line>` (run by the orchestrator, or by `scripts/orchestrator/bus-read.sh` on each RESULT where it is simplest) recomputes the receipt's hash from the branch, requires every check `ok` or `unavailable` (never `missing`), and prints `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise reason=precheck:<the missing checks> next_action=run-result-precheck-and-resend` for the orchestrator to send mechanically, exit 1; exit 0 when the RESULT may be reviewed. The refusal is mechanical: no judgment, no text.
3. The worker cap. `home/dot_agents/agent-config.yaml` gains `worker_cap: 4` (one key beside `worker_kind`; the value is today's four seats; about six is a later decision after items 1 and 2 show their effect). `herdr-agents --add-worker` counts the worker identities registered at worktrees of the repository (one name per worktree, `identities.sh <worktree> <type>` as the Stop checklist counts them) and refuses the seat that would exceed the cap with one line naming the cap and the seats. `tests/unit/test_herdr_agents.py` gains `test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap` (stub identities at four worktrees: the fifth add refuses, a remove then allows) and `test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat` (the SKILL's two seat-count sentences carry the manifest value spelled as a number and the words `worker_cap`; the SKILL's exemption bullet and the rule's Delegation bullet name the integration seat and list only the three orchestrator steps; the step-15 sentence names the integration seat as the thread resolver). The texts: `home/dot_agents/skills/agmsg-orchestration/SKILL.md` lines 31 and 38 (the seat-count sentences) say "at most `worker_cap` workers (4 in the manifest today)"; lines 33 and 34 (the delegation sentence and the exemption bullet) say that integration runs on the integration seat through `integrate-seat.sh` and that the orchestrator acts directly only for agmsg/herdr control-plane operations and evidence-sync bookkeeping, the acceptance judgment with the audit and its dispositions, and the final gate and merge; Worker Playbook step 15's "The worker resolves no thread" becomes "The implementing worker resolves no thread; the integration seat does, with the recorded dispositions"; Orchestrator Playbook step 10 gains one sentence pointing at `integrate-seat.sh` for sub-steps 1 and 3 and keeps 2, 4 and 5. `home/dot_config/claude/rules/agmsg-orchestration.md`: the Delegation bullet's exemption list becomes the three steps above; the Acceptance bullet keeps acceptance and the audit dispositions with the orchestrator and names the integration seat for the sweep, the local review and the thread resolution. No other sentence changes; no procedure is written twice (the scripts are the procedure).

## Out of scope

The GitHub merge queue (evaluated after item 1), raising the cap to about six (after items 1 to 3), the integration seat's seating itself (the operator seats it with `herdr-agents --add-worker <worktree> --kind <kind>` within the cap), F3's amendment (the orchestrator, after this PR merges), any change to `scripts/validate-agent-assets.py` (in flight elsewhere), the audit (stays the orchestrator's), the ruleset.

## Check

`uv run python -m unittest tests/unit/test_integration_seat.py tests/unit/test_herdr_agents.py -v` green, `shellcheck scripts/orchestrator/integrate-seat.sh scripts/orchestrator/result-precheck.sh home/dot_local/bin/common/executable_herdr-agents` and `shfmt -d` on the two new scripts clean, `make validate-agent-assets` (exit 0) pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 260 changed lines (added plus deleted) outside `tests/` and `.orchestration/`, excluding `home/dot_agents/skills/agmsg-orchestration/SKILL.md` and `home/dot_config/claude/rules/agmsg-orchestration.md` (text) (Amendment 2, D-cap-F4: the three items of the directive in one PR measure 249 in lint-clean code), and 1000 added lines under `tests/` (INV-2). `result-precheck.sh run` is run on this PR's own head before the RESULT and its receipt is the first use of item 2.

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition; the #390 branch stays in the worktree for its own integration). The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written (the ruleset's checks, the Bot's review and the one P0/P1 fix round, the C-50 case for a first review's small P2, C-59 and C-61, the orchestrator's audit, gate and merge), with `dotfiles-T129-integration-seat-result-gate-cap-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears, C-51) and `task_copy=<sha256 of .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/task.md>` plus `precheck=<sha256>` in the RESULT.

## Amendment 1 (round 1, 2026-10-17T12:5xZ)

M-20261017-07 (the #386 chains 2 and 3 of today): gh colors its JSON when the calling shell sets `CLICOLOR_FORCE` (it wins over `NO_COLOR`), and the glue's fill step hid the parser's crash behind `|| true`. Both new scripts of this task, `scripts/orchestrator/integrate-seat.sh` and `scripts/orchestrator/result-precheck.sh`, export `CLICOLOR_FORCE=0 FORCE_COLOR=0 NO_COLOR=1` right after `set -euo pipefail`, so every gh and jq call they or their children make emits plain text, and no step of theirs hides a parser's exit status (`|| true` only where the task names an optional step, the Bot wait). One test case in `tests/unit/test_integration_seat.py` runs `integrate-seat.sh` with `CLICOLOR_FORCE=1` in the environment and a stub gh that colors its output when that variable is set, and asserts the sweep step still parses (correction C-62). Nothing else changes.

## Amendment 2 (round 1, 2026-10-17T13:1xZ)

a006's caps question (PONG 13:13:41Z): the full spec in tested, lint-clean code measures 249 changed lines outside tests and the two text files (integrate-seat.sh 122, result-precheck.sh 106, herdr-agents 18, manifest 3) against the Check's 200. Decided by default (D-cap-F4): option A, the cap is 260 for this PR; the directive fixed one PR with the three items, and the audit reads the whole diff. a006's declared readings stand: `worker_cap` read by sed from the deployed `~/.agents/agent-config.yaml` (herdr-agents has no yaml reader), a missing key meaning no cap plus one stderr line (an old deployment is not blocked, the line names the missing key); `allowed_files` read by sed as plain items; (g) reads the RESULT's thread tokens `<id>:<P>:<disposition>` from report.md. One correction: (h) and (i) are three-state, `ok`, `unavailable (<reason>)` or `missing`, and `verify` refuses only `missing`, so a Claude seat's RESULT is not refused for lacking codex. Nothing else changes.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-integration-seat-result-gate-cap-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
premise 4: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-a01.md
```
