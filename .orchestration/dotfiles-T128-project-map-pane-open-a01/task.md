---
format: 2
task_id: dotfiles-T128-project-map-pane-open-a01
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
  - .orchestration/dotfiles-T128-project-map-pane-open-a01/**
after: [dotfiles-T128-project-map-reload-hook-a01]
threat_table:
  - control: the PR edits home/dot_claude/hooks/executable_project-map-reload.sh in one branch, when terminal-browser ls --all --json lists no browser whose tab shows the map, it runs terminal-browser open <the event's map path> --split right --size 0.5 --no-merge once, output discarded, and exits 0 whether that succeeds or fails, every other path of the merged hook unchanged
    disposition: "closed: tests/unit/test_generate_agent_configs.py::test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map"
  - control: "the agent-browser host daemon that the hook's --session project-map-reload starts or reuses on the first call (agent-browser keeps one daemon per session name in the user's session and ends it after its idle timeout, one hour by default); the hook neither configures nor kills it"
    disposition: "residual: one daemon for the fixed session name, started only when a map tab exists, holding the user's own CDP connection to the user's own browser and nothing else; it idles out on its own; the tests never start one (the agent binary is a stub); a stale daemon is visible in agent-browser session list and is the operator's to close"
  - control: the PR edits tests/unit/test_generate_agent_configs.py (one new test beside the two hook tests; the merged test's nine empty-selection cases gain the one open call in their expected browser calls, the other hook test stays as it is)
    disposition: "residual: the stub terminal-browser records its argv and answers the listing from a variable the test sets; the stub agent records argv; nothing runs; the audit reads each case against item 2"
  - control: the PR edits home/dot_config/claude/rules/project-map.md in one sentence (the pane opens itself at the first map write and reloads at every later one; no seat and no human opens or refreshes it)
    disposition: "residual: prose read by the orchestrator at session start; the one changed sentence is item 3's; no other sentence of the rule changes"
  - control: the PR edits home/dot_agents/skills/project-map/SKILL.md in one sentence of its Writes section (the same statement for the agent that writes the map)
    disposition: "residual: prose read by the project-map agent; the one changed sentence is item 3's; the symlinked Claude copy follows the source"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-project-map-pane-open-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-project-map-pane-open-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests import scripts/generate-agent-configs.py as the existing module tests do and run the hook script as a subprocess with a stub terminal-browser on PATH; nothing else is imported"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the hook runs the same three executables as the merged hook, jq and terminal-browser on the user's PATH and the agent binary of TERMINAL_BROWSER_AGENT else the bundled one; the new branch runs terminal-browser once more, with the open subcommand and the event's map path as its only variable argument (already matched to /.project-map/index.html); terminal-browser open splits the pane its environment names, the pane of the Claude session that wrote the map, and launches nothing outside the Herdr workspace; nothing in the event or the file chooses an executable"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; the hook lineage's script is edited in one branch; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the merged hook on origin/main opens no pane: it has no terminal-browser open call (it reloads an existing map tab and exits 0 silently when none shows the map)'
    command: 'git show origin/main:home/dot_claude/hooks/executable_project-map-reload.sh | /usr/bin/grep -c "terminal-browser open" || true'
    output: |-
      0
  - claim: 'the installed terminal-browser documents --split <direction>, --size <fraction> and --no-merge for open (the form the operator uses by hand today, plus the flag that keeps the pane its own)'
    command: 'terminal-browser open --help 2>&1 | /usr/bin/grep -c -e "--split <direction>" -e "--size <fraction>" -e "--no-merge"'
    output: |-
      3
---

# AGMSG-TASK dotfiles-T128-project-map-pane-open-a01 — the project-map pane opens itself at the first map write (the operator's direction of 2026-10-14 14:1xZ; plan 021 step 7 form; a Codex seat because every touched file is Claude's boundary)

Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time). The merged hook (PR #353, 6a2473f3) reloads the terminal-browser tab that shows `.project-map/index.html` after every Write or Edit of that file and exits 0 silently when no pane shows it, which left opening the pane to a hand-run `terminal-browser open … --split right --size 0.5`. The operator ruled at 14:1xZ that opening the pane when it is absent is the hook's job too, so that neither the operator nor the orchestrator runs anything: this task adds that one branch, its test, and one sentence each in the rule and the SKILL. The hook follow-up `dotfiles-T128-project-map-reload-hook-followup-a01` (pair-confirmed, dispatching after boundary (15)) shares these files and runs after this task merges.

## Goal

The first write of the map in a session opens the split pane beside the Claude session that wrote it, and every later write reloads it, with no step for a human or a seat.

## Files

1. `home/dot_claude/hooks/executable_project-map-reload.sh`: the merged hook's behaviour (jq reads `tool_input.file_path`; a path not ending in `/.project-map/index.html` exits 0; `terminal-browser ls --all --json` failing exits 0; the browser whose tab shows the map is selected by its cdpPort and the tab's CDP targetId; the two agent-browser calls with `--cdp`; every failure exits 0 with empty output) with one change: when the listing parsed cleanly but holds no browser with a map tab (today's `[[ -n "$selection" ]] || exit 0`), the hook runs `terminal-browser open "$file_path" --split right --size 0.5 --no-merge >/dev/null 2>&1` once and exits 0 whether that succeeds or fails; the open uses the event's path (already matched) and nothing else from the event; a listing that fails to parse still exits 0 without opening (the hook cannot know whether a pane exists); the empty selection is also the state of a listing whose map tab fails the jq filter (a cdpPort or targetId the filter rejects), and the branch then opens a second pane: this task accepts that consequence as documented behaviour, and the stricter filter stays the hook follow-up's `target-id-validation` row; `terminal-browser open` returns when the new browser is ready, so a second hook run within the same second finds the tab in the listing, and if it does not, the second open is accepted the same way; the shdoc header's description gains these sentences.
2. `tests/unit/test_generate_agent_configs.py`: one new test, `test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map`, beside the two hook tests; the merged test `test_project_map_reload_hook_acts_only_on_the_map_and_never_fails` changes in one place: its nine empty-selection cases ("no browser", "no map tab", "null target", the five "invalid port" cases and "invalid target") now expect `browser_calls` of `["ls --all --json", "open <the event's path> --split right --size 0.5 --no-merge"]`, and its listed-tab cases keep `["ls --all --json"]`; the other hook test stays as it is: the stub terminal-browser answers `ls --all --json` from a variable the test sets and records every argv to a log; the stub agent on `TERMINAL_BROWSER_AGENT` records its argv; case one, a listing with a browser whose tabs hold no map url: the log holds exactly one `open <path> --split right --size 0.5 --no-merge` call with the event's path, the agent log is empty, the exit is 0 and the output empty; case two, the same listing and the stub's open exiting 1: exit 0, empty output; case three, a listing with the map tab: no open call and the two agent calls as the existing test asserts; case four, an empty browsers list (`{"self":{},"browsers":[]}`): one open call.
3. `home/dot_config/claude/rules/project-map.md` and `home/dot_agents/skills/project-map/SKILL.md`: one sentence each where the reload sentence stands: the hook opens the pane (a right split of half the width, its own pane and never a tab merged into a neighbouring terminal-browser) at the first map write of a session and reloads it at every later write; no seat and no human opens or refreshes it.

## Out of scope

The renderer, the manifest key, the rendered settings, `scripts/check-agent-runtime.py` (the hook is already rendered and checked), the tab-fallback and target-id rows of the hook follow-up (they stay its rows), any other sentence of the rule or the SKILL.

## Check

`uv run python -m unittest tests.unit.test_generate_agent_configs -k project_map_reload -v` green (three hook tests), pasted in the validation file with `shellcheck home/dot_claude/hooks/executable_project-map-reload.sh`, `make render-check` (the rendered settings are unchanged, so it passes as it stands) and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after e3006da7). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-project-map-pane-open-a01-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-project-map-pane-open-a01-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test name, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-project-map-pane-open-a01/task.md>` and the evidence paths.
