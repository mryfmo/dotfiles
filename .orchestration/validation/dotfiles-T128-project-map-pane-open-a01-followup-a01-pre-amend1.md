---
format: 2
task_id: dotfiles-T128-project-map-pane-open-a01-followup-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_claude/hooks/executable_project-map-reload.sh
  - tests/unit/test_generate_agent_configs.py
  - home/dot_config/claude/rules/project-map.md
  - home/dot_agents/skills/project-map/SKILL.md
  - .orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/**
after: [dotfiles-T128-project-map-reload-hook-followup-a01]
threat_table:
  - control: the PR edits home/dot_claude/hooks/executable_project-map-reload.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits tests/unit/test_generate_agent_configs.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), one test per row; the stub terminal-browser records its argv and answers the listing from a variable the test sets, the stub agent records its argv, nothing runs; the audit reads each case against item 1"
  - control: the PR edits home/dot_config/claude/rules/project-map.md only within the owned rows (item 1)
    disposition: "residual: prose read by the orchestrator at session start; a row that changes a sentence of the rule names the sentence; no other sentence changes"
  - control: the PR edits home/dot_agents/skills/project-map/SKILL.md only within the owned rows (item 1)
    disposition: "residual: prose read by the project-map agent; a row that changes a sentence of the SKILL names the sentence; the symlinked Claude copy follows the source"
  - control: "the agent-browser host daemon that the hook's --session project-map-reload starts or reuses on the first call (agent-browser keeps one daemon per session name in the user's session and ends it after its idle timeout, one hour by default); the hook neither configures nor kills it"
    disposition: "residual: one daemon for the fixed session name, started only when a map tab exists, holding the user's own CDP connection to the user's own browser and nothing else; it idles out on its own; the tests never start one (the agent binary is a stub); a stale daemon is visible in agent-browser session list and is the operator's to close"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests import scripts/generate-agent-configs.py as the existing module tests do and run the hook script as a subprocess with a stub terminal-browser on PATH; nothing else is imported"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the hook runs the same three executables as the merged hook, jq and terminal-browser on the user's PATH and the agent binary of TERMINAL_BROWSER_AGENT else the bundled one, with the open subcommand and the event's map path as its only variable argument (already matched to /.project-map/index.html); terminal-browser open splits the pane its environment names, the pane of the Claude session that wrote the map, and launches nothing outside the Herdr workspace; nothing in the event or the file chooses an executable"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script: the owned rows name edits to files the lineage landed; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the lineage task file is on origin/main at dispatch (present since boundary (15), 727180db, which carried the pair-confirmed pane-open task file)'
    command: 'git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01.md && echo present || echo absent'
    output: |-
      present
  - claim: 'the lineage acceptance record''s Owned-by section is on origin/main at dispatch (present since boundary (16), PR #373 merged as 1d418126 on 2026-10-16: the section exists in the orchestrator''s checkout since the Bot''s review of PR #359''s head 73f51ab2; a record on origin/main without the section would read no rows)'
    command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01.md 2>/dev/null | /usr/bin/grep -q "^## Owned by dotfiles-T128-project-map-pane-open-a01-followup-a01" && echo present || echo absent'
    output: |-
      present
---

# AGMSG-TASK dotfiles-T128-project-map-pane-open-a01-followup-a01 — the residual findings of the project-map pane-open PR (#359) (the owner task of the pane-open lineage; plan 020 step 1, C-32's owner-first pattern; a Codex seat because every touched file is Claude's boundary)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. Under plan 020 a P2 finding (Codex Bot, the orchestrator's local review, the audit, or the worker's own report) on a head of PR #359 is advisory: it is dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a01` and recorded as a row of `.orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01.md` under the heading `## Owned by dotfiles-T128-project-map-pane-open-a01-followup-a01`; this task implements exactly those rows after the lineage's PR merges and after the hook follow-up `dotfiles-T128-project-map-reload-hook-followup-a01`, which edits the same four files, merges. Its first row is `4277695198`, in the owner section since the Bot's review of head 73f51ab2 (2026-10-15 00:2xZ): the hook's suffix-only URL filter (`endswith("/.project-map/index.html")`) selects another repository's map tab when one is open, so `$selection` is non-empty and the branch reloads that tab instead of opening this event's map; the remedy the row names is to compare the selected tab's URL with the normalised event path before deciding the pane is present, with a test whose listing holds two distinct `/.project-map/index.html` URLs.

## What to do

1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-project-map-pane-open-a01-followup-a01` in `.orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01.md` as read from `origin/main` (advisory P2 findings on the lineage's PR heads, each dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a01`, filed as a `local-finding:` or `audit-finding:` line naming this owner, or named in the lineage RESULT's report as advisory); each row's finding text is in the record (the Bot thread, the local review file, the audit receipt or the report the id names). Implement each, with one test per row named in report.md, beside the hook tests in `tests/unit/test_generate_agent_configs.py`. A missing or empty section at dispatch makes this task a no-op: report `no owned rows` and stop; the orchestrator dispatches only after both premises replay `present`.
2. Nothing else changes: no file outside the owned rows' files, no behaviour the rows do not name, no change to what the hook does beyond the row's text; the rule and the SKILL change only where a row names a sentence.

## Validation

- `uv run python -m unittest tests.unit.test_generate_agent_configs -k project_map_reload -v` in the validation file, with the new tests named; `shellcheck home/dot_claude/hooks/executable_project-map-reload.sh`; `make render-check` (the rendered settings are unchanged).
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #359 and the hook follow-up's PR merged, and boundary (16), PR #373 merged as 1d418126). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-project-map-pane-open-a01-followup-a02`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-project-map-pane-open-a01-followup-a02` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/task.md>` and the evidence paths.

## Change (premises, 2026-10-16T06:27:52Z, before dispatch)

Boundary (16) (PR #373, merged as 1d418126 on 2026-10-16) landed the owner section on `origin/main`, so the premise that waited for it now records the post-boundary output that `presend.sh` replays at dispatch; its claim says so. Nothing else changes from the pair-confirmed hash `ace9aebd`; re-confirmed Codex first (C-54).

## Change (Completion, 2026-10-16T08:44:50Z, before dispatch)

The review seat's round on the premise change (P2, P3): the Completion clause still had the single-review form written before T13's amendment 6 (no `open:<thread id>`, no `bot_rounds=2`, "every P2 as advisory", the pre-C-51 owner wording). It is now the task template's clause of 2026-10-16 (`.orchestration/templates/task-short.md`, Completion): the Bot's review at PR open and once more on `@codex review` after a P0/P1 fix round, a surviving P0/P1 listed as `open:<thread id>` with `bot_rounds=2`, the C-50 revise round for a small in-scope P2, every other P2 advisory and owned by `dotfiles-T128-project-map-pane-open-a01-followup-a02` (written when the first advisory P2 appears, C-51) under `## Owned by dotfiles-T128-project-map-pane-open-a01-followup-a02` in this task's acceptance record. Nothing else changes from `ecd3606f`; re-confirmed Codex first (C-54).

