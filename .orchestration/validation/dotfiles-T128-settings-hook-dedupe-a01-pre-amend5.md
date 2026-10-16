---
format: 2
task_id: dotfiles-T128-settings-hook-dedupe-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_claude/modify_private_settings.json
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T128-settings-hook-dedupe-a01/**
after: [dotfiles-T128-project-map-reload-hook-followup-a01]
threat_table:
  - control: the PR edits home/dot_claude/modify_private_settings.json in one place (a constant, a helper, a predicate and one dict entry), adding a PostToolUse predicate to MANAGED_HOOK_PREDICATES so the existing merge_managed_entries replaces a stale managed PostToolUse entry in place instead of the additive branch keeping it beside the managed one
    disposition: "closed: tests/unit/test_claude_settings_merge.py::test_managed_post_tool_use_replaces_stale_format_only_entry"
  - control: the PR edits tests/unit/test_claude_settings_merge.py (one new test beside the nineteen, which stay as they are; the module runs the modify script as a subprocess on a managed template and a current settings document it writes, standard library only)
    disposition: "residual: the test writes both inputs and compares the script's stdout as JSON; nothing else runs; the audit reads the case against item 2"
  - control: "the settings file chezmoi writes at every apply from this script's stdout (~/.claude/settings.json, read by Claude Code at startup): the change removes one duplicate PostToolUse entry and keeps every unmanaged hook where it is"
    disposition: "residual: the merge keeps unmanaged hooks in their entries (merge_managed_entries' mixed-entry rule, covered on main by test_managed_permgate_replaces_stale_current_ccgate_hook and test_managed_session_start_replaces_stale_hard_coded_home_hook) and the new test covers the PostToolUse case; a wrong predicate would drop a user hook, which the new test's unmanaged-command case refuses"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-settings-hook-dedupe-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-settings-hook-dedupe-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the test module runs home/dot_claude/modify_private_settings.json as a python3 subprocess with CHEZMOI_SOURCE_DIR set to a temporary source tree it writes, and imports only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the modify script runs under chezmoi's python3 at apply time with CHEZMOI_SOURCE_DIR from chezmoi, as today; the tests set the same variable to their temporary tree; nothing in the current settings document chooses an executable, the predicate compares the command token for equality with the two renderings of the managed path for this home (the tilde form and the absolute form under CHEZMOI_HOME_DIR, else the home directory) for each basename in the module constant MANAGED_POST_TOOL_USE_SCRIPTS"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the modify script on origin/main has no PostToolUse entry in MANAGED_HOOK_PREDICATES, so a PostToolUse list falls into the additive branch (current entries kept, managed entries appended when not already present)'
    command: 'git show origin/main:home/dot_claude/modify_private_settings.json | /usr/bin/grep -c "\"PostToolUse\""'
    output: |-
      0
  - claim: 'the managed template on origin/main renders one PostToolUse entry whose hooks run format-edited-files.py and project-map-reload.sh'
    command: 'git show origin/main:home/.chezmoitemplates/claude-settings-managed.json | /usr/bin/grep -c "project-map-reload.sh"'
    output: |-
      1
  - claim: 'the test module on origin/main holds nineteen tests, which this task keeps'
    command: 'git show origin/main:tests/unit/test_claude_settings_merge.py | /usr/bin/grep -c "def test_"'
    output: |-
      19
---

# AGMSG-TASK dotfiles-T128-settings-hook-dedupe-a01 — the settings modify script replaces a stale managed PostToolUse entry instead of keeping it beside the managed one (plan 022 T15, the decisions panel's default; a Codex seat because the modify script is Claude's boundary)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. On this machine `~/.claude/settings.json` holds two PostToolUse entries with the matcher `Write|Edit|MultiEdit`: the pre-#353 entry (format-edited-files.py alone) and the managed one (format-edited-files.py and project-map-reload.sh), so the formatter runs twice per edit. The cause is in `home/dot_claude/modify_private_settings.json`: `MANAGED_HOOK_PREDICATES` names PermissionRequest and SessionStart only, so `merge_hooks` sends PostToolUse to the additive branch (`value + [entry for entry in managed_value if entry not in value]`), which keeps the old entry and appends the managed one. The existing `merge_managed_entries` already does the right thing for the two named events: a fully managed entry is swapped for its managed counterpart in place, a mixed entry keeps its unmanaged hooks where they are. This task adds the PostToolUse predicate and its test, nothing else.

## Goal

After `chezmoi apply`, `~/.claude/settings.json` holds one PostToolUse entry for `Write|Edit|MultiEdit`, the managed one, and every unmanaged PostToolUse hook a user added stays where it was.

## Files

1. `home/dot_claude/modify_private_settings.json`: a predicate `is_managed_post_tool_use_hook(hook)` in the shape of `is_managed_session_start_hook`: the hook is a dict with a string `command`, `shlex.split` succeeds, and the command is the exact managed invocation: `shlex.split` yields exactly one part that is a managed hook path, or exactly two parts whose first basename is an interpreter (`python3`, `python`, `bash`, `sh`) and whose second is a managed hook path; a managed hook path is one token equal to a rendering of the managed path for this home: `~/.claude/hooks/<basename>` (the template's form) or `str(home_dir() / ".claude" / "hooks" / basename)` (the absolute form under `CHEZMOI_HOME_DIR`, else `Path.home()`), for each basename in the constant, listed by a helper `managed_post_tool_use_paths()` beside the constant (string equality, no pattern); the template's `~/.claude/hooks/format-edited-files.py` and this home's absolute form are managed, a token under any other prefix (`/workspace/team/.claude/hooks/format-edited-files.py`, the Bot's P1 4290805581 on e5d0141b) is unmanaged; any other shape is unmanaged and kept, so a wrapper (`~/bin/log-hook.sh ~/.claude/hooks/format-edited-files.py`), a managed script with arguments, a managed script followed by a shell operator and a user command (`~/.claude/hooks/format-edited-files.py && ~/bin/audit-edit.sh`, three parts after `shlex.split`), a user script that shares a managed basename (`/opt/team/format-edited-files.py`, the Bot's P1 4290664196 on 72d0e66d) and a token that glues a shell operator to a managed path (`~/bin/audit-edit.sh;~/.claude/hooks/format-edited-files.py`, one token to `shlex.split`, the worker's residual P1 on 72d0e66d) all stay (the managed template renders each hook as the bare script path, so the exact invocation is the one part; the SessionStart predicate keeps its any-part rule, outside this task), a module constant beside `MANAGED_SESSION_START_SCRIPTS` in its shape, `MANAGED_POST_TOOL_USE_SCRIPTS = ("format-edited-files.py", "project-map-reload.sh")`, the basenames of the two commands the managed template's PostToolUse entry renders (a renamed hook is a change to this constant, as it is for the SessionStart set); `MANAGED_HOOK_PREDICATES` gains `"PostToolUse": is_managed_post_tool_use_hook`. `merge_managed_entries` and `merge_hooks` are unchanged. Failure modes stated: a current PostToolUse entry whose hooks are all managed is replaced by the managed entry (the duplicate goes); an entry with an unmanaged command, a wrapper that names a managed script as an argument, a managed script chained with a user command, a user script sharing a managed basename or a glued token included, keeps that command in place and the managed hooks are re-appended with the managed entry (fail safe for user hooks); a current document without a PostToolUse key gets the managed entry as today.
2. `tests/unit/test_claude_settings_merge.py`: one new test, `test_managed_post_tool_use_replaces_stale_format_only_entry`, beside the nineteen tests, which stay as they are, in the module's style (the managed template and the current document written to a temporary tree, the script run as a subprocess, stdout parsed as JSON): case one, the symptom as observed: the current document holds two PostToolUse entries, the stale `{"matcher": "Write|Edit|MultiEdit", "hooks": [format-edited-files.py]}` and then the managed two-command entry itself, and the managed template its two-command entry: the output holds exactly one PostToolUse entry, the managed one (on `origin/main` both entries survive, so this case fails there); case one b, the stale entry alone: the same output; case four, the current entry holds the wrapper `~/bin/log-hook.sh ~/.claude/hooks/format-edited-files.py`: the output keeps that command (on the pre-amendment head bdefcbe4 it is deleted, so this case fails there); case five, the current entry holds the chained command `~/.claude/hooks/format-edited-files.py && ~/bin/audit-edit.sh`: the output keeps that command (on 5bcab1f9 it is deleted, so this case fails there); case six, the current entry holds `/opt/team/format-edited-files.py`: the output keeps that command (on 72d0e66d it is deleted, so this case fails there); case seven, the current entry holds the glued token `~/bin/audit-edit.sh;~/.claude/hooks/format-edited-files.py`: the output keeps that command (on 72d0e66d it is deleted, so this case fails there); case eight, the stale entry holds the absolute form (`<home>/.claude/hooks/format-edited-files.py`, `<home>` the value the script's `home_dir()` resolves in the test: `CHEZMOI_HOME_DIR` when the test sets it, else `Path.home()`): the output holds exactly one PostToolUse entry, the managed one; case nine, the current entry holds `/workspace/team/.claude/hooks/format-edited-files.py`: the output keeps that command (on e5d0141b it is deleted, so this case fails there); case two, the current entry also holds an unmanaged command (`~/bin/my-hook.sh`): the output keeps an entry with that command alone at its position and the managed entry after it; case three, a current document without `hooks.PostToolUse`: the output holds the managed entry; the test asserts the whole PostToolUse list each time.

## Out of scope

The managed template, the renderer and the manifest (the template already renders the right entry); PermissionRequest and SessionStart handling; every other key of the settings file; the hook scripts themselves.

## Check

`uv run python -m unittest tests/unit/test_claude_settings_merge.py -v` green (the nineteen existing tests plus the new one), pasted in the validation file with `make render-check` (the rendered template is unchanged, so it passes as it stands) and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after 59599783). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-settings-hook-dedupe-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-settings-hook-dedupe-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test name, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-settings-hook-dedupe-a01/task.md>` and the evidence paths. After the merge the operator runs `make update` and restarts Claude Code (the settings file is read at startup); `jq '.hooks.PostToolUse|length' ~/.claude/settings.json` then prints 1.

## Change (round 2, 2026-10-15 05:20Z)

The review seat's round 1 (P1, P2): item 1 and the environment row had described the PostToolUse basename set as read from the rendered template at run time "as the SessionStart set is"; on `origin/main` that set is the module constant `MANAGED_SESSION_START_SCRIPTS`, so the set is now a constant in that shape, named in item 1 and row 32; case one of item 2 now holds both entries of the operator's file (the stale one and the managed one), the branch `merge_managed_entries` takes when the queue is exhausted, with the stale-alone input as case one b. The Codex half confirmed round 1; its P3 wording notes (row 30 "python3 subprocess" for `uv run python`; the convergence test keeps passing) need no change.

## Amendment 1 (2026-10-16T01:17:15Z, after dispatch)

The task-level audit of PR #369's head bdefcbe4 (P2, specification): item 1's rule matched any part's basename, so a user wrapper that passes a managed script path as an argument was taken for a managed hook and replaced, against the task's own fail-safe for user hooks; the implementation followed the text. Item 1 now recognises a managed hook by the basename of the command's program only (the first part, or the second after an interpreter), item 2 adds the wrapper case (case three), and the failure mode names the wrapper. The audit's P3 (the committed report still said publication blocked) is the revise round's evidence update. Nothing else changes from the dispatched hash `461643b4` (the pre-amendment copy is `.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend1.md`).

## Amendment 2 (2026-10-16T03:21:35Z, after dispatch)

The Codex Bot's P1 4290538244 on PR #369's head 5bcab1f9: a hook that starts with a managed script and chains a user command (`… && ~/bin/audit-edit.sh`) was classified managed by amendment 1's first-part rule and deleted by `merge_managed_entries`. Item 1 now recognises only the exact managed invocation (one part, or an interpreter and one part), so any further part keeps the hook; item 2 adds the chained case (case five) and numbers the wrapper case four (the seat's round-3 P3). The Bot's P1 is fixed worker-side in the one round, the ACCEPTANCE naming the test as its check. Nothing else changes from the confirmed hash `99fb3dc7` (the pre-amendment copy is `.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend2.md`).

## Amendment 3 (2026-10-16T03:44:09Z, after dispatch)

Two P1 findings on PR #369's head 72d0e66d, both from amendment 2's basename contract: the Codex Bot's 4290664196 (a user's single-token command `/opt/team/format-edited-files.py` shares the managed basename, so the predicate classified it managed and `merge_managed_entries` deleted it) and the worker's own (a hook command with no whitespace, `~/bin/audit-edit.sh;~/.claude/hooks/format-edited-files.py`, is one `shlex` token whose basename is the managed script). Item 1 now matches the managed hook path, not the basename: one plain token ending in `/.claude/hooks/<basename>` (the compiled pattern beside the constant, `re` imported), so a stale rendering under another home directory stays managed while both findings' shapes are unmanaged and kept; item 2 adds cases six to eight; the first threat row counts two constants. Nothing else changes from the confirmed hash `79d2af63` (the pre-amendment copy is `.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend3.md`). The Codex half's round 1 on `15d9a5a9` (2026-10-16T03:50:14Z): the environment threat row had still said the predicate compares basenames; it now states the path matching.

## Amendment 4 (2026-10-16T04:05:59Z, after dispatch)

The Codex Bot's P1 4290805581 on PR #369's head e5d0141b: amendment 3's pattern admits any plain prefix before `/.claude/hooks/<basename>`, so a hook under another project's directory (`/workspace/team/.claude/hooks/format-edited-files.py`) is classified managed and deleted. The managed path has exactly two renderings on a machine, the template's `~/.claude/hooks/<basename>` and this home's absolute form, so item 1 now compares the token for string equality with those two (a helper beside the constant, no pattern, no `re`); the environment threat row says so; item 2 adds case nine and restates case eight. Nothing else changes from the confirmed hash `ae036713` (the pre-amendment copy is `.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-pre-amend4.md`).
