---
format: 2
task_id: dotfiles-T132-make-update-followups-a01
kind: code
security: false
allowed_files:
  - scripts/update-agent-assets.sh
  - scripts/upgrade-tools.sh
  - tests/unit/test_update_agent_assets.py
  - tests/unit/test_upgrade_tools.py
  - .orchestration/dotfiles-T132-make-update-followups-a01/**
after: [dotfiles-T129-assets-omp-hcom-a01]
threat_table:
  - control: the PR edits scripts/update-agent-assets.sh only in update_omp (item 1)
    disposition: "residual: before the npm install, a dangling symlink at the install path is removed and reported; a real file, a directory or a live symlink is never touched; the removal is a plain rm of one symlink path the manifest names, logged with its former target; one fixture per case, red before and green after"
  - control: the PR edits scripts/upgrade-tools.sh only in upgrade_uv_tools (item 2)
    disposition: "residual: the uv upgrade phase skips the tools the manifest pins from a local wheel (hcom) instead of upgrading all; the skip list is read from the manifest's assets, never hard-coded beyond a documented fallback; the phase stays optional"
  - control: tests/unit/test_update_agent_assets.py only for the new update_omp cases
    disposition: "residual: fixtures only, beside the existing omp and hcom tests, with a fake npm on PATH and a temporary HOME; nothing reaches ~/.local"
  - control: tests/unit/test_upgrade_tools.py (new module; none exists on origin/main)
    disposition: "residual: a new unittest module in the repository's conventions, fixtures only, with a fake uv on PATH recording its argv; nothing reaches the live uv tool directory"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T132-make-update-followups-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T132-make-update-followups-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: both scripts are exercised as subprocesses in the tests with fake npm and uv on PATH and HOME under a temporary directory; no test runs make update or touches the live install"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; both scripts run under bash as today"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through the pinned squash form after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: an update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'update_omp installs the verified tarball with npm into ~/.local (the install line and the manifest_record string that quotes it), and nothing removes a stale symlink first'
    command: '/usr/bin/grep -c "npm install -g --prefix" scripts/update-agent-assets.sh; /usr/bin/grep -c "dangling" scripts/update-agent-assets.sh'
    output: |-
      2
      0
  - claim: 'the uv phase of upgrade-tools.sh upgrades every uv tool at once, as an optional phase'
    command: '/usr/bin/grep -n "uv tool upgrade --all" scripts/upgrade-tools.sh; /usr/bin/grep -c "run_optional_phase \"uv tool upgrade\"" scripts/upgrade-tools.sh'
    output: |-
      424:    uv tool upgrade --all
      1
---

# AGMSG-TASK dotfiles-T132-make-update-followups-a01 — the two `make update` defects of 2026-10-18 08:1x JST (the operator's items ii and iii)

Written 2026-10-18 by the orchestrator seat from the operator's batch of 08:1x JST. The operator's `make update` (omp 18.11.3, hcom 0.7.30, claude-code 2.1.300, herdr 0.9.5) hit two defects in the tracked scripts: (ii) `update_omp` failed with npm `EEXIST` because `~/.local/bin/omp` was a dangling symlink from an old Tern install (the operator moved it aside by hand); (iii) the optional `uv tool upgrade` phase failed on hcom, which the manifest installs from a verified local wheel, so an index upgrade has nothing to upgrade from. The operator's item (i), a stale PreToolUse entry kept by the settings modify script, is a Claude-boundary file (`home/dot_claude/modify_private_settings.json`) and goes to a Codex seat as its own task; it is out of scope here.

## Goal

`make update` on a machine with a dangling `~/.local/bin/omp` symlink installs omp (the link is replaced and the replacement is logged), and its uv phase upgrades the index-installed tools while skipping the wheel-pinned ones, reporting the skip, so the phase no longer warns on hcom.

## Files

1. `scripts/update-agent-assets.sh`, `update_omp()` (lines 921 to 951 on origin/main): before `npm install -g --prefix "${HOME}/.local" "${tarball}"`, when the install path (`${HOME}/.local/bin/omp`, the manifest's `install_path`) is a symlink whose target does not exist (`[ -L "$p" ] && [ ! -e "$p" ]`), remove that symlink and print one line naming its former target (`readlink`); a regular file, a directory or a live symlink is left alone (npm's own behaviour applies; a live symlink to another omp is reported in the summary as today). Test (fake `npm` on PATH that fails with `EEXIST` when the path exists as a symlink and succeeds otherwise, HOME under a temporary directory): (a) a dangling link is removed, the install succeeds and the log names the old target; (b) a live symlink is not removed and the existing behaviour is unchanged; (c) no link, unchanged path.
2. `scripts/upgrade-tools.sh`, `upgrade_uv_tools()` (line 424): replace `uv tool upgrade --all` by an upgrade of each installed tool that the manifest does not pin from a wheel: list the tools (`uv tool list`), read the wheel-pinned tool names from the manifest's assets (`source: https-download` with a `.whl` upstream, today `hcom`; VERIFY 1 names the key to read), upgrade the rest one by one, and print `skip: <tool> (manifest pins <version> from a wheel)` for each skipped one. The phase stays `run_optional_phase`. Test (fake `uv` recording argv, a fixture manifest): (a) hcom is skipped with the line and the others are upgraded; (b) no pinned tool, every tool upgraded; (c) an empty tool list, no call.
3. The update_omp tests live beside the existing omp and hcom tests in `tests/unit/test_update_agent_assets.py`; the uv-phase tests go in a new `tests/unit/test_upgrade_tools.py` (no such module exists on origin/main: `git ls-files tests/unit/test_upgrade_tools.py` prints nothing), written in the repository's unittest conventions (see the neighbouring modules) and run by the same `make unit-test` discovery.

## Out of scope

Item (i) of the operator's list (the settings modify script), a Codex seat's task; any change to the manifest; the omp or hcom pins; `remove-agent-asset`; the a02 follow-up's own items on `update-agent-assets.sh` (uninstall through uv, the install retry, the non-npm omp entry: branch `tools/assets-hcom-followup-a02`, pushed, PR after #398 merges).

## Check

Pasted in the validation file: `uv run python -m unittest tests/unit/test_update_agent_assets.py tests/unit/test_upgrade_tools.py -v` green; `shellcheck -x scripts/update-agent-assets.sh scripts/upgrade-tools.sh` and `shfmt --indent 4 --space-redirects --diff` on both clean; `make render-check` (nothing generated changes); `git diff --numstat origin/main...HEAD`. Caps: under 40 changed lines in each script, under 160 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` now. The branch `tools/assets-hcom-followup-a02` (accepted work of the a02 follow-up, PR after #398 merges) edits `update_omp`'s neighbourhood in the same script and the same test module; its worker is finished, so the edits are not concurrent (the D-D-overlap-394 reading), and this branch rebases onto `origin/main` after that PR merges and before its RESULT; a textual conflict is a `PONG status=blocked`, never a hand merge. Under the morning merge-gate policy the worker opens its own draft PR with the plain create form (explicit `--base main` and `--head`, `--title`, `--body-file`, `--draft`; one command, no shell metacharacters) and marks it ready with the plain ready form when CI is green; comment, review and edit still prompt a human and are not run. The Completion clause of `.orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md` applies otherwise, with `dotfiles-T132-make-update-followups-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T132-make-update-followups-a01/task.md>` in the RESULT.

## VERIFY (the worker closes each in report.md with the command and output)

- VERIFY 1: the manifest key that distinguishes a wheel-pinned uv tool (`home/dot_agents/agent-config.yaml` `assets.hcom`: `source`, `upstream` ending in `.whl`, `pin`); if `upgrade-tools.sh` cannot read the manifest without a new dependency, a documented fallback list in the script (`hcom`) with a comment naming the manifest key is acceptable, said so in report.md.
- VERIFY 3: how `uv tool upgrade <name>` behaves for a tool installed from a local wheel (`uv tool upgrade hcom` on the worker's machine is read-only enough to try once; paste the output).

## Checks (pasted by the orchestrator before each send)

```
(pending)
```
