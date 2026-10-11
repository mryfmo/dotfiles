---
format: 2
task_id: dotfiles-T128-process-rules-a01
kind: docs
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - AGENTS.md
  - tests/unit/test_agmsg_orchestration_docs.py
after: []
premises:
  - claim: "the T128 design phase produced over twenty design-review RESULTs (the count below is stamped with its time, it grows with every round) and the Codex Bot reviewed seven heads of PR 317 in one afternoon, one per fix round, six of them after the RESULT head 32fe9a36 (RESULT at 02:19Z), because no convergence rule, round cap or threat table existed; the operator directed on 2026-10-11 that the pattern be established before any further feature wave"
    command: "date -u +%FT%TZ; ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep -c 'AGMSG-RESULT v1 task_id=dotfiles-T128-design-review-a01'; gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[]|select(.user.type==\"Bot\")|[.commit_id[0:8],.submitted_at]|@tsv'"
    output: |-
      2026-10-11T04:13:28Z
      26
      32fe9a36	2026-10-11T02:37:13Z
      56ca6c69	2026-10-11T02:52:38Z
      de138f65	2026-10-11T03:03:00Z
      f6528bba	2026-10-11T03:10:28Z
      98f1d250	2026-10-11T03:24:14Z
      2602f575	2026-10-11T03:43:58Z
      e314c502	2026-10-11T04:04:13Z
  - claim: "the Codex Bot reviews non-draft PRs (its first review of PR 317 came 17 minutes after gh pr ready at 02:20Z and none during the draft hours before; a draft is reviewed only on an explicit @codex review comment), and it reads the Code Review Rules section of AGENTS.md"
    command: "gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[0].submitted_at'; grep -n 'Code Review Rules' AGENTS.md"
    output: |-
      2026-10-11T02:37:13Z
      67:## Code Review Rules
  - claim: "the regime rule file is at its 450-word budget, so the pattern's text lives in the SKILL and AGENTS.md"
    command: "wc -w home/dot_config/claude/rules/agmsg-orchestration.md"
    output: "     447 home/dot_config/claude/rules/agmsg-orchestration.md"

---

# AGMSG-TASK dotfiles-T128-process-rules-a01 — Phase A: the recommended pattern as regime rules (A1, A2, A4)

Plan 006 Phase A (operator direction 2026-10-11: establish the pattern first, then fix the problem areas with it). Review tier by INV-1 (the SKILL and AGENTS.md are listed in the review tier by name): prose, the docs test, and one schema audit of the final head; `kind: docs` because no code changes. Claude seat, `.claude/worktrees/worker-f`, branch `docs/regime-pattern` from `origin/main`. One PR.

## A1: SKILL, "Review and integration invariants" and Orchestrator Playbook step 3

1. Design review protocol: both reviewers (a fresh Claude context on the review profile and a Codex read-only run under a `codex-review` identity) are dispatched on the same design hash at the same time; the orchestrator revises once per pair of results and opens no round while one is open; at most three revision rounds, then the design is frozen with a residual list that becomes worker input; the review judges invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
2. Task-file review is one round with a fixed stop condition: no contradiction with the design, premises hold, `allowed_files` complete for the touch points grep finds, one invariant (a `-contract-a01` id maps to its implementing entry). Anything finer is the worker's and the implementation PR's.
3. A boundary PR synchronizes records at a boundary; it carries no task drafts under review and is never a prerequisite of a dispatch (the design-on-main precondition is met by any merged boundary that carries the design).
4. A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter (a list of `{control, disposition}` items whose `disposition` matches `^(closed|residual|out-of-scope): `; V1's `schemas/task.json` carries the key as optional, a note the V1 task file takes in Phase B): one row per thing the PR or the orchestrator controls (tree, task.md, test modules, workflow file, interpreter and environment files, in-process effects such as `SkipTest`, `os._exit` and module patching, new or renamed scripts, metadata separators), each marked `closed: <test selector>`, `residual: <compensating control>` or `out-of-scope: <owner>`. The table is the task's completion condition; reviewers and the Bot look for missing rows, and a missing row is added once (counted as an amendment) rather than fixed finding by finding.
5. Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` (A3) and pastes its output into the acceptance record; S1 (the same class three times) and S2 (INV-6 counts) are decided from that output.

## A2: SKILL, Worker Playbook step 15 (and the RESULT contract)

The PR is marked ready for review (`gh pr ready <n>`) before the Bot wait; when no Bot review of the final head arrives within 10 minutes the worker posts `@codex review` and waits the remaining window. P0/P1 Bot findings are fixed and re-pushed at most twice; the third Bot round is not fixed: the worker sends `AGMSG-RESULT … bot_rounds=3` with the open threads listed, and the orchestrator decides (threat-table row, disposition, or S1). A revise ACCEPTANCE carries `previous_head=` and one failing-test selector per finding; the worker records them in `.orchestration/<task id>/revise.yaml`.

## A4: `AGENTS.md`, "## Code Review Rules"

A subsection "Orchestration records and trust-boundary code": files under `.orchestration/**` are the regime's records and task specifications, reviewed by the regime's own reviewers; review them for secrets and home-directory paths only. For code the task marks as a trust boundary, review against the task's `threat_table`: report a row that is missing or a `closed` row whose test does not close it; do not re-raise a `residual` row (the compensating control is named there). Keep lint and formatting to CI.

## Validation

`prettier --check` on the two prose files; `tests/unit/test_agmsg_orchestration_docs.py` (extend it with one assertion per new rule: the round cap, the one-round task review, the threat-table requirement, the counters-before-acceptance rule, the Code Review Rules subsection; each fails when its sentence is removed); the premises re-run and pasted.

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-process-rules-a01/task.md`; evidence beside it.

## Completion

Draft PR within 30 minutes, `gh pr ready`, CI, Bot wait per A2, artifacts, `memory add`, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=8. Forbidden: any other file; `make update`; thread resolution.
