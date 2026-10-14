---
format: 2
task_id: dotfiles-T128-project-map-reload-hook-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_claude/hooks/executable_project-map-reload.sh
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - home/.chezmoitemplates/claude-settings-managed.json
  - tests/unit/test_generate_agent_configs.py
  - home/dot_config/claude/rules/project-map.md
  - home/dot_agents/skills/project-map/SKILL.md
  - scripts/check-agent-runtime.py
  - .orchestration/dotfiles-T128-project-map-reload-hook-a01/**
after: []
threat_table:
  - control: the PR adds home/dot_claude/hooks/executable_project-map-reload.sh, a Claude Code PostToolUse hook that runs after every Write, Edit or MultiEdit, acts only when the edited path ends with /.project-map/index.html, then reads terminal-browser ls --all --json, takes the cdpPort and the tab's CDP targetId of the browser whose tabs hold a url ending with /.project-map/index.html, and drives that browser through the agent-browser binary (the bundled one unless the user's TERMINAL_BROWSER_AGENT overrides it) with --cdp <port> on each call (the form upstream issue 60 names as reliable; terminal-browser action omits --cdp on its final call in v0.13.4 and can launch an invisible Chrome), switching to that tab and reloading it, output discarded; it exits 0 on every path, no browser, no map tab and a failing command included, and it writes nothing (amendment 2, Bot thread 4267187098)
    disposition: "closed: tests/unit/test_generate_agent_configs.py::test_project_map_reload_hook_acts_only_on_the_map_and_never_fails"
  - control: "the agent-browser host daemon that the hook's --session project-map-reload starts or reuses on the first call (agent-browser keeps one daemon per session name in the user's session and ends it after its idle timeout, one hour by default); the hook neither configures nor kills it"
    disposition: "residual: one daemon for the fixed session name, started only when a map tab exists, holding the user's own CDP connection to the user's own browser and nothing else; it idles out on its own; the tests never start one (the agent binary is a stub); a stale daemon is visible in agent-browser session list and is the operator's to close"
  - control: the PR edits home/dot_agents/agent-config.yaml in one key of the claude.hooks block (project_map_reload_hook, beside format_edited_files_hook); nothing under codex changes
    disposition: "residual: the diff is one line in claude.hooks; the renderer's test pins what it produces; the audit compares the diff with this row"
  - control: the PR edits scripts/generate-agent-configs.py in its Claude-rendering part only (the PostToolUse list gains the new hook command when the key is set)
    disposition: "closed: tests/unit/test_generate_agent_configs.py::test_project_map_reload_hook_renders_into_post_tool_use"
  - control: the PR regenerates home/.chezmoitemplates/claude-settings-managed.json (the rendered Claude settings; make render-check requires it in sync with the manifest)
    disposition: "residual: generated output, checked by make render-check in CI and by the orchestrator; no hand edit"
  - control: the PR edits tests/unit/test_generate_agent_configs.py (the PostToolUse assertions and the two new cases)
    disposition: "residual: the oracle of the two closed rows; no existing assertion weakens; the audit reads the diff"
  - control: the PR edits home/dot_config/claude/rules/project-map.md in one sentence (the pane reloads through the hook; no seat and no human reloads by hand), landing with the hook in the same PR
    disposition: "residual: one sentence that names a mechanism landing in the same squash commit; the test of the rendered settings is its evidence"
  - control: the PR edits home/dot_agents/skills/project-map/SKILL.md in one sentence of its Writes section (the map and state files are written with the Write or Edit tool, never through Bash, so the PostToolUse hook sees every write); the Claude skill is a template mirror of this file and needs no edit
    disposition: "residual: one sentence; the agent definition already lists Write and Edit among its tools (home/dot_claude/agents/project-map.md:4); the audit reads the diff"
  - control: the PR edits scripts/check-agent-runtime.py in one block (a check_executable_hook call for the new hook beside the two existing ones), so make doctor and the installed-versus-source parity check know the hook
    disposition: "residual: one block of the existing shape; tests/unit/test_check_agent_runtime.py replaces check_executable_hook wholesale, so no test edit; the audit reads the diff"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-project-map-reload-hook-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-project-map-reload-hook-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests import scripts/generate-agent-configs.py as the existing module tests do and run the hook script as a subprocess with a stub terminal-browser on PATH; nothing else is imported"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the hook runs exactly three executables outside any sandbox (a PostToolUse hook runs as the user): jq, resolved on the user's PATH (installed through mise); terminal-browser, resolved on the user's PATH (pinned in the asset manifest), for ls only; and an agent-browser binary whose path is the value of TERMINAL_BROWSER_AGENT when the user's environment sets that variable, an executable of the user's own choosing that terminal-browser itself honours and the tests use as the stub seam, and otherwise the pinned installer's bundled binary under ~/.local/share/terminal-browser/app/agent-browser/bin/; nothing in the edited file or its content chooses any of the three; agent-browser talks only to a loopback CDP port the listing names (amendment 2)"
  - control: new or renamed scripts
    disposition: "residual: one new hook script under home/dot_claude/hooks/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'terminal-browser v0.13.4 is installed; with no browser running the --json listing has an empty browsers array, the case the hook must swallow'
    command: 'terminal-browser --version 2>/dev/null; terminal-browser ls --all --json 2>/dev/null | jq -c .browsers; echo "ls exit ${PIPESTATUS[0]}"'
    output: |-
      terminal-browser v0.13.4
      []
      ls exit 0
  - claim: "the renderer turns the claude.hooks keys into PreToolUse and PostToolUse entries; the format hook sits under the matcher Write|Edit|MultiEdit, which the test pins exactly"
    command: "grep -n 'format_edited_files_hook\\|\"PostToolUse\"\\|\"PreToolUse\"' scripts/generate-agent-configs.py; grep -n -A1 '\"PostToolUse\"' home/.chezmoitemplates/claude-settings-managed.json | head -2; grep -n 'settings\\[\"hooks\"\\]\\[\"PostToolUse\"\\]' tests/unit/test_generate_agent_configs.py"
    output: |-
      403:    if hooks.get("format_edited_files_hook"):
      407:                "command": hooks["format_edited_files_hook"],
      429:            "PreToolUse": [
      441:            "PostToolUse": [
      99:    "PostToolUse": [
      100-      {
      1479:            settings["hooks"]["PostToolUse"],
      1491:        self.assertEqual(settings["hooks"]["PostToolUse"], [{"matcher": "Write|Edit|MultiEdit", "hooks": []}])
  - claim: 'upstream issue 60 reports that an unselected terminal-browser action can drive a freshly launched Chrome instead of the pane browser, and names repeating --cdp <port> on every invocation as the reliable form (the Codex Bot P1 4267187098 on PR #353)'
    command: 'curl -fsSL https://api.github.com/repos/zenbu-labs/terminal-browser/issues/60 | jq -r ".title, .state"; curl -fsSL https://api.github.com/repos/zenbu-labs/terminal-browser/issues/60 | jq -r .body | grep -n -m 3 -- "--cdp" | cut -c1-160'
    output: |-
      `terminal-browser action` drives a newly launched Chrome instead of the open browser
      open
      26:`cli/src/action.ts` passes `--cdp <port>` only on the probe inside `agentTabs()`:
      29:runAgent(binary, ["--session", session, "--cdp", port, "tab", "list", "--json"]);
      32:That probe **succeeds**, so the `connect` fallback below it is never reached. Every call after it omits `--cdp`:
  - claim: 'in v0.13.4 terminal-browser action lists tabs with --cdp but its final spawnSync passes only --session and the passthrough arguments, and its guardrail rejects a user-supplied --cdp, so no selector makes action reliable'
    command: 'curl -fsSL https://raw.githubusercontent.com/zenbu-labs/terminal-browser/v0.13.4/cli/src/action.ts | grep -n -E "spawnSync|--cdp" | cut -c1-150'
    output: |-
      1:import { execFileSync, spawnSync } from "node:child_process";
      67:  const result = spawnSync(binary, args, {
      96:  const listing = runAgent(binary, ["--session", session, "--cdp", port, "tab", "list", "--json"]);
      205:  ["--cdp", "terminal-browser picks the port from the browser you target"],
      287:  const child = spawnSync(binary, ["--session", session, ...options.passthrough], {
  - claim: 'the ls --json listing is {self, browsers[]} with browsers[].key, cdpPort and tabs[], and a tab carries id, url, title, active and a CDP targetId (string or null), the ref the hook passes to agent-browser'
    command: 'curl -fsSL https://raw.githubusercontent.com/zenbu-labs/terminal-browser/v0.13.4/cli/src/ls.ts | grep -n -E "cdpPort: browser|key: recordKey|tabs: await targets"; curl -fsSL https://raw.githubusercontent.com/zenbu-labs/terminal-browser/v0.13.4/cli/src/instances.ts | grep -n -E "^  (id: number|url: string|title: string|active: boolean|targetId: string \\| null);"'
    output: |-
      24:      key: recordKey(browser),
      26:      cdpPort: browser.cdpPort,
      34:      tabs: await targets(browser).catch(() => []),
      9:  id: number;
      10:  url: string;
      11:  title: string;
      12:  active: boolean;
      13:  targetId: string | null;
  - claim: 'the pinned installer puts agent-browser 0.38.1 beside terminal-browser, and the binary accepts --cdp <port> as a connection, never a launch (a port with nothing listening gives a connection error, not an unknown-option error)'
    command: 'ls ~/.local/share/terminal-browser/app/agent-browser/bin/; ~/.local/share/terminal-browser/app/agent-browser/bin/agent-browser --version; ~/.local/share/terminal-browser/app/agent-browser/bin/agent-browser --cdp 1 --session probe eval 1 2>&1 | head -1 | cut -c1-80; echo "exit ${PIPESTATUS[0]}"'
    output: |-
      agent-browser
      agent-browser 0.38.1
      ✗ All CDP discovery methods failed for 127.0.0.1:1: /json/version: Failed to con
      exit 1
  - claim: "the project-map rule says nothing about reloading the map pane yet"
    command: "grep -c -i 'reload\\|terminal-browser' home/dot_config/claude/rules/project-map.md"
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-project-map-reload-hook-a01 — the project-map pane reloads itself through a Claude Code PostToolUse hook (plan 021 step 7's unit; routed to a Codex seat because every touched file is Claude's boundary)

Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time). The operator views `.project-map/index.html` in a terminal-browser pane split from the orchestrator's Herdr pane and asked that the refresh at rewrite time be a rule in dotfiles, with nothing left to a human or to the orchestrator's habit. The map is written only by the `project-map` subagent's `Write`, so a PostToolUse hook in the orchestrator's Claude Code session is the event: it fires for a subagent's tool calls too and runs outside the sandbox as the user, where terminal-browser's daemon is reachable. Routing: `claude.hooks`, the Claude-rendering part of the renderer and the rendered managed settings are Claude's boundary (SKILL Orchestrator Playbook step 3), so a Codex seat lands this.

## Goal

When the project map's `index.html` is written, the terminal-browser tab showing it reloads within a second, by a hook rendered from the manifest, and no seat and no human reloads by hand.

## Files

1. `home/dot_claude/hooks/executable_project-map-reload.sh` (new, under 60 lines, shdoc comments in English, `#!/bin/bash`): reads the PostToolUse JSON from stdin with `jq -r '.tool_input.file_path // empty'`; when that path ends with `/.project-map/index.html` it runs `terminal-browser ls --all --json` and selects with `jq` the browser whose `tabs[]` holds a `url` ending with `/.project-map/index.html` (premise 5 pins the keys: `browsers[].cdpPort`, `browsers[].key`, `tabs[].targetId`, `tabs[].url`, `tabs[].active`; a tab whose `targetId` is null is skipped), then runs the bundled agent-browser twice with `--cdp <cdpPort> --session project-map-reload` on each call (the binary `"${TERMINAL_BROWSER_AGENT:-$HOME/.local/share/terminal-browser/app/agent-browser/bin/agent-browser}"`, premise 6; `--cdp` on every call is the form upstream issue 60 names as reliable, and the `--session` name keeps the connection apart from terminal-browser's own): `tab <targetId>` to bring the map tab to the front (the first call starts or reuses agent-browser's host daemon for that session name, which idles out after its default timeout; the hook leaves it alone; agent-browser accepts a CDP target id as a tab ref, its `tab --help`: "CDP target ids (from tab list --json) are also accepted as tab refs; unlike t<N> ids they stay stable across daemon restarts"; terminal-browser's numeric `tabs[].id` is its own id space and is never passed), then `eval 'location.reload()'`, output discarded; never `terminal-browser action`, which omits `--cdp` on its final call in v0.13.4 and can launch an invisible Chrome (premises 3 and 4); Failure paths, each ending in `exit 0` with empty stdout and stderr: (a) an event with no `file_path`; (b) a path that is not the map; (c) `jq` missing; (d) `terminal-browser` missing, or `ls` failing; (e) a listing with no browser; (f) a listing with no map tab; (g) a map tab whose `targetId` is null; (h) the agent binary missing (`TERMINAL_BROWSER_AGENT` naming a path that does not exist); (i) the `tab` call failing; (j) the `eval` call failing after a successful `tab`. The hook prints nothing and writes nothing on any path.
2. `home/dot_agents/agent-config.yaml`: in `claude.hooks`, one key `project_map_reload_hook: ~/.claude/hooks/project-map-reload.sh` beside `format_edited_files_hook`.
3. `scripts/generate-agent-configs.py`, the Claude-rendering part: when the key is set, the PostToolUse entry for `Write|Edit|MultiEdit` gains a second command hook (`{"type": "command", "command": <the key's value>}`) after the format hook; the key absent renders exactly what renders today.
4. `home/.chezmoitemplates/claude-settings-managed.json`: regenerated by the renderer (`make render-check` green).
5. `tests/unit/test_generate_agent_configs.py`: the existing PostToolUse assertions take the second hook; `test_project_map_reload_hook_renders_into_post_tool_use` (key set: two command hooks in order; key absent: today's output); `test_project_map_reload_hook_acts_only_on_the_map_and_never_fails` (the script run as a subprocess with a stub `terminal-browser` on PATH that answers `ls --all --json` with a listing in premise 5's shape holding one browser whose tabs include the map url and one that does not, and a stub agent binary named by `TERMINAL_BROWSER_AGENT` that records its argv and can be told to fail on a given call): two success cases, a Write event and an Edit event on `<tmp>/.project-map/index.html`, each calling the agent stub exactly twice, in order `--cdp <that browser's cdpPort> --session project-map-reload tab <that tab's targetId>` then `--cdp <the same port> --session project-map-reload eval location.reload()`, never `terminal-browser action`; and one case per failure path (a) to (j) of item 1, each asserting exit 0, empty stdout and empty stderr, and for (i) and (j) that no further agent call follows the failing one.
6. `home/dot_config/claude/rules/project-map.md`, one sentence added to the first bullet: "The terminal-browser pane that shows the map reloads through the `project-map-reload` PostToolUse hook; no seat and no human reloads it by hand."
7. `home/dot_agents/skills/project-map/SKILL.md`, one sentence added to the Writes section's first bullet: "Write `index.html` and `state.json` with the Write or Edit tool, never through Bash (a heredoc or a redirect), so the session's PostToolUse hook sees the write and reloads the pane." The Claude copy is a symlink template of this file (`home/dot_claude/skills/project-map/symlink_SKILL.md.tmpl`) and needs no edit.
8. `scripts/check-agent-runtime.py`: one `check_executable_hook(SOURCE_ROOT / "dot_claude/hooks/executable_project-map-reload.sh", HOME / ".claude/hooks/project-map-reload.sh", "Claude project-map-reload hook")` block beside the two existing ones (lines 813 to 826 on origin/main).

## Out of scope

Opening the browser pane itself (a later short task may make the workspace launcher open the split; today the operator runs `terminal-browser open ~/Workspace/dotfiles/.project-map/index.html --split right --size 0.5` once from the orchestrator's pane, which puts the browser in that terminal tab), `terminal-browser action` in any form (premises 3 and 4), a fix of upstream issue 60, the map's content or style, any other hook or settings key, the Codex side of the manifest, T704 and the gate wrapper tasks.

## Check

`uv run python -m unittest tests/unit/test_generate_agent_configs.py -v` green and `make render-check` green, both pasted in the validation file with `shellcheck home/dot_claude/hooks/executable_project-map-reload.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2; the task copy and the evidence records under `.orchestration/` are committed on the branch as every task does and are never capped, INV-2's convention) and 1000 added lines under `tests/` (INV-2); the regenerated managed settings count toward the first cap.

## Completion

One PR from a fresh branch off `origin/main`. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; P2 are advisory and owned by `dotfiles-T128-project-map-reload-hook-followup-a01`, which the orchestrator writes when the first P2 appears and lands by the next boundary before the merge. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`; after the merge the operator's next `make update` installs the hook and the orchestrator verifies it once by running the project-map agent. The RESULT names head, base, branch, files, every Bot thread with its disposition, the two test names, items 7 and 8, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-project-map-reload-hook-a01/task.md>` and the evidence paths.

## Change of 2026-10-14 (amendment 1, after the worker's question of 05:29Z, before any push)

1. The Check's 200-line cap reads "outside `tests/` and outside `.orchestration/`": the worker read the text literally (the task copy alone is 110 lines) and asked; records and the task copy were never capped (INV-2's convention, as a05 and a06 reported their caps). Nothing else changes.

## Change of 2026-10-14 (amendment 2, after the Codex Bot's P1 4267187098 on PR #353, before the worker's fix round)

1. Item 1 no longer uses `terminal-browser action`: in v0.13.4 its final call omits `--cdp` and can drive a freshly launched invisible Chrome (upstream issue 60; premises 3 and 4). The hook now takes the browser whose tab shows the map from `terminal-browser ls --all --json` (keys pinned in premise 5; the tab addressed by its CDP targetId, which agent-browser accepts as a tab ref) and drives it through the bundled agent-browser with `--cdp <cdpPort>` on each call (premise 6): `tab <targetId>`, then `eval 'location.reload()'`.
2. The hook row and the environment-inputs row say so (three executables, a loopback CDP port); item 5's test stubs the listing and the agent binary; premise 1 probes the empty listing instead of the action form; the out-of-scope list names `terminal-browser action` in any form.
3. Nothing else changes; amendment 1 stands.
