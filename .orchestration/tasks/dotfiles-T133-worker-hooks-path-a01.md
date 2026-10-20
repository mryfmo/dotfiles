---
format: 2
task_id: dotfiles-T133-worker-hooks-path-a01
kind: code
security: true
allowed_files:
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T133-worker-hooks-path-a01/**
after: [dotfiles-T133-worker-cap-hookspath-a02]
threat_table:
  - control: "the PR edits home/dot_local/bin/common/executable_herdr-agents in two places (item 2: the Claude worker's .claude/settings.local.json gains an env block with GIT_CONFIG_COUNT, GIT_CONFIG_KEY_0 and GIT_CONFIG_VALUE_0 through the writer that already merges that file; item 3: the Codex worker's launch gains the three -c shell_environment_policy.set.<KEY>=<value> flags beside the existing -c flags; no git configuration file is written anywhere and the host's own git is untouched)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_add_worker_sets_the_hooks_path_through_each_seat_kinds_own_configuration_and_writes_no_git_config"
  - control: "tests/unit/test_herdr_agents.py (the one test above and item 1's verification cases, in the file's fixture style)"
    disposition: "residual: fakes record every argv and the settings file is read back from the temporary worktree; no live seat"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-worker-hooks-path-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-worker-hooks-path-a01/ (report.md, validation.md, sandbox.md, learning.md, the item 1 proofs)"
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the only new writes are three environment entries in the seat's own configuration (a file herdr-agents already writes, or flags it already passes); the worker's git reads .githooks from its own worktree as the worker's own process; nothing changes on this Mac before the operator's make update"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the three GIT_CONFIG_* variables are the environment input this task adds, each a fixed literal, never read from the worktree or the worker"
  - control: new or renamed scripts
    disposition: "residual: none; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: the managed Claude settings template already carries an env block, so a per-worktree env block is the same mechanism Claude Code reads today
    command: /usr/bin/grep -c '"env"' home/.chezmoitemplates/claude-settings-managed.json
    output: |-
      1
  - claim: herdr-agents already writes the worker worktree's .claude/settings.local.json (the hooks and deny rules), so item 2 extends an existing writer
    command: /usr/bin/grep -n 'shell_environment_policy\|settings.local.json' home/dot_local/bin/common/executable_herdr-agents | head -5
    output: |-
      352:            "${worktree}/.claude/settings.local.json" > /dev/null 2>&1 && return 0
      370:    local settings="${worktree}/.claude/settings.local.json" input temporary
      1418:    local claude_hooks_file="${workdir}/.claude/settings.local.json"
  - claim: codex exec takes -c/--config overrides, the form item 3 uses for the Codex worker
    command: codex exec --help | /usr/bin/grep -c -- '--config'
    output: |-
      1
---

# AGMSG-TASK dotfiles-T133-worker-hooks-path-a01 — the worker's hooks path through each seat kind's own configuration (plan 024 P1-7 item 3, re-planned)

Written 2026-10-18 by the orchestrator seat as the re-plan of `dotfiles-T133-worker-cap-hookspath-a01` item 3 (Amendment 3): a `core.hooksPath` set in git configuration exposed worker-writable metadata to the host's git (the security P1 4305769826 on PR #408), and the spawn environment does not reach a Herdr worker pane (a010's proof `amendment2/raw/herdr-env-transport-proof.log` in the a01 evidence: the real herdr CLI's `tab.create` transports no caller environment, the installed agmsg driver passes no `--env`). What remains is each seat kind's own configuration, which `herdr-agents` already writes. Seat: a Codex seat (the file is the launcher; the Claude worker's settings file is Claude's boundary, so a Codex seat), after `dotfiles-T133-worker-cap-hookspath-a01` merges; the branch starts from `origin/main` then.

## Goal

Every worker seat's own git runs the repository's `.githooks` (P1-5) because its process environment carries `core.hooksPath=.githooks`, set by the seat kind's configuration at seating; no git configuration file is written and the host's git never loads anything of the worker's.

## Files

1. Item 0, verification with the real CLIs before any code, pasted in `validation.md`: (a) a scratch `.claude/settings.local.json` holding `"env": {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.hooksPath", "GIT_CONFIG_VALUE_0": ".githooks"}` in a temporary git repository, and a headless `claude -p` run there whose Bash prints `git config core.hooksPath`: the output must be `.githooks` (if `claude -p` is unavailable to the seat, the Claude Code documentation sentence on the settings `env` key is fetched and quoted with its URL and date instead, and the live check is the orchestrator's at acceptance); (b) `codex exec --sandbox read-only -c shell_environment_policy.set.GIT_CONFIG_COUNT=1 -c shell_environment_policy.set.GIT_CONFIG_KEY_0=core.hooksPath -c shell_environment_policy.set.GIT_CONFIG_VALUE_0=.githooks 'run: git config core.hooksPath'` in the same repository: `.githooks`. A failing probe is a `status=blocked` PONG with the output, not a workaround.
2. `herdr-agents --add-worker` for a Claude worker: the existing writer of `<worktree>/.claude/settings.local.json` also sets the `env` block's three keys (merged, never replacing other keys; idempotent on a re-seat); `--remove-worker` leaves the file as today.
3. `herdr-agents --add-worker` for a Codex worker: the spawn options gain the three `-c shell_environment_policy.set.<KEY>=<value>` flags beside the existing `-c sandbox_workspace_write.*` flags.
4. `tests/unit/test_herdr_agents.py`: `test_add_worker_sets_the_hooks_path_through_each_seat_kinds_own_configuration_and_writes_no_git_config` (a Claude seat: the settings file holds the three env keys and every pre-existing key; a Codex seat: the fake spawn records the three `-c` flags; both: the fakes record no `git config` write and neither the common config nor the worktree's gains `core.hooksPath` or `extensions.worktreeConfig`; red before).

## Precondition (2026-10-18T08:3xZ, from the P1-5 a02 RESULT)

`.githooks/pre-push` scans every pushed blob's text for the masker's secret pattern, and a009's RESULT (40a053e9) observed that 13 tracked files already match it on origin/main (the list is in `.orchestration/dotfiles-T133-result-precheck-a02/validation.md`), so a seat whose git runs the hook could not push a commit touching them. Before this task enables the hook for any seat, those 13 files are settled (masked, allow-listed by the masker's placeholder rule, or the pattern narrowed) by a task the orchestrator names; this task starts after that task merges, and its item 0 pastes `scripts/orchestrator/result-precheck.sh --secrets <diff of origin/main against its empty tree for those 13 paths>` exiting 0.

## Out of scope

`.githooks/*` (P1-5), the cap and the lock (a01), the upstream agmsg driver, any manifest or rendered settings change, `make update` (the operator's, after the merge).

## Check

`make format`, `shellcheck` and `shfmt -d` on the launcher clean, `uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_agmsg_orchestration_docs -v` green, item 0's two probes pasted, with `git diff --numstat origin/main...HEAD`: at most 60 changed lines outside `tests/` and `.orchestration/`, 150 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after `dotfiles-T133-worker-cap-hookspath-a01` merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-worker-cap-hookspath-followup-a01` (the lineage's existing owner task) as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-hooks-path-a01/task.md>` in the RESULT; a Codex seat writes its evidence at the same relative paths in its worktree and says so. `security: true`: the orchestrator runs the task-level audit and the security-profile review on the final head. No `@codex review` comment; single commands for every gh and git write.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```
