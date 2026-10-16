---
format: 2
task_id: dotfiles-T128-doctor-codex-trust-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/check-agent-runtime.py
  - tests/unit/test_check_agent_runtime.py
  - .orchestration/dotfiles-T128-doctor-codex-trust-a01/**
after: [dotfiles-T128-project-map-reload-hook-followup-a01]
threat_table:
  - control: the PR edits scripts/check-agent-runtime.py in two places (a canonical_source_dir function and a source_dir keyword of same_modified, used by the Codex config comparison alone), so the doctor's expected Codex trust entry is the canonical clone's wherever the doctor runs
    disposition: "closed: tests/unit/test_check_agent_runtime.py::test_codex_config_comparison_uses_the_canonical_source_dir"
  - control: the PR edits tests/unit/test_check_agent_runtime.py (two new tests beside the 52, which stay as they are; the module's style of patching module attributes and subprocess.run, with no real chezmoi)
    disposition: "residual: the patched functions record and answer, nothing else; the audit reads each case against the Files items"
  - control: "the chezmoi binary on PATH and its answer: the doctor runs chezmoi source-path read-only and uses the first line of its stdout only as the CHEZMOI_SOURCE_DIR value for the Codex modify script's expected output; a missing, failing, slow or empty answer, or one that names no directory, falls back to the working clone with one WARN line"
    disposition: "residual: the answer is used as a path value for a comparison, never executed, and the fallback is today's behaviour; the closed row's case two covers the fallback and the WARN line, and the second test covers the four failure answers"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-doctor-codex-trust-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-doctor-codex-trust-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the test module imports the doctor as a module (as today) and patches its attributes and subprocess.run inside each test, restoring them in finally blocks, and imports only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the doctor runs the modify scripts by their source paths under SOURCE_ROOT as today and chezmoi by name from PATH, as its chezmoi drift check already does, under the doctor's own interpreter (uv run python, the Makefile's doctor target); the tests' seam is the module attribute and subprocess.run; a PR checkout as cwd chooses nothing, because the doctor reads SOURCE_ROOT from its own file location and the canonical dir from chezmoi's configuration"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the Codex modify script on origin/main reads CHEZMOI_SOURCE_DIR as its source dir, whose parent is the working tree it writes into the trust entry'
    command: 'git show origin/main:home/dot_codex/modify_private_config.toml | /usr/bin/grep -c "CHEZMOI_SOURCE_DIR"'
    output: |-
      2
  - claim: 'the doctor on origin/main never asks chezmoi for its source path'
    command: 'git show origin/main:scripts/check-agent-runtime.py | /usr/bin/grep -c "source-path"'
    output: |-
      0
  - claim: 'the doctor on origin/main sets CHEZMOI_SOURCE_DIR to the working clone for every modify-script comparison'
    command: 'git show origin/main:scripts/check-agent-runtime.py | /usr/bin/grep -c "env\[\"CHEZMOI_SOURCE_DIR\"\] = str(SOURCE_ROOT)"'
    output: |-
      1
  - claim: 'the doctor test module on origin/main holds 52 tests, which this task keeps'
    command: 'git show origin/main:tests/unit/test_check_agent_runtime.py | /usr/bin/grep -c "def test_"'
    output: |-
      52
---

# AGMSG-TASK dotfiles-T128-doctor-codex-trust-a01 — the doctor compares the Codex config against the canonical clone's trust entry wherever it runs (plan 022 T11, definition of done D2; a Claude seat)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. `make doctor` from the working clone (`~/Workspace/dotfiles`) prints `Codex config managed keys differ or config is missing` while the same command from the canonical clone (`~/.local/share/chezmoi`) does not. The cause is in `scripts/check-agent-runtime.py`: `same_modified()` runs each modify script with `CHEZMOI_SOURCE_DIR` set to `SOURCE_ROOT`, the clone the doctor lives in, and `home/dot_codex/modify_private_config.toml` renders its trust entry as `[projects."<source dir's parent>"]`, so from the working clone the expected entry names `~/Workspace/dotfiles` while the applied file holds the canonical clone's `~/.local/share/chezmoi` (written by `chezmoi apply`, whose source dir is `chezmoi source-path`, today `~/.local/share/chezmoi/home`). The comparison must use the canonical clone's source dir, which `chezmoi source-path` answers wherever the doctor runs.

## Goal

`make doctor` from the working clone and from the canonical clone compare the Codex config against the same expected trust entry, the canonical clone's, so D2 (doctor ERROR count 0 from both clones) no longer fails on that line; without `chezmoi` the doctor says so in one WARN line and compares against the working clone as today.

## Files

1. `scripts/check-agent-runtime.py`: (a) a function `canonical_source_dir() -> Path | None` that runs `["chezmoi", "source-path"]` with `subprocess.run` (capture, text, `timeout=20`, `check=False`) and returns `Path(first stdout line)` when the exit status is 0, the line is non-empty and names an existing directory; it returns `None` on `FileNotFoundError`, any other `OSError`, `subprocess.TimeoutExpired`, a non-zero exit, an empty line or a missing directory (fail safe: a doubtful answer never changes the comparison); (b) `same_modified()` gains a keyword parameter `source_dir: Path | None = None` and sets `env["CHEZMOI_SOURCE_DIR"] = str(source_dir or SOURCE_ROOT)`, so every existing call is unchanged; (c) in `check()`, before the Codex config comparison, `canonical = canonical_source_dir()`; that one comparison (`dot_codex/modify_private_config.toml` against `~/.codex/config.toml`) passes `source_dir=canonical`, and when `canonical` is `None` the messages gain exactly one line `WARN: Codex trust entry compared against the working clone: chezmoi source-path unavailable` (a WARN message in the list, as the unmanaged-skill-dir line is, so `is_warning` keeps it out of the ERROR count); the model-profile and Claude-settings comparisons keep the default. Failure modes stated: chezmoi present and answering, the expected trust entry is the canonical clone's and the line disappears from a correctly applied machine; chezmoi absent or failing, today's comparison and one WARN; chezmoi answering a path that is not a directory, the same fallback. Nothing else in the script changes.
2. `tests/unit/test_check_agent_runtime.py`: two new tests beside the 52, which stay as they are, in the module's style (module attributes patched and restored in `finally`, `check()` run, the returned messages read): `test_codex_config_comparison_uses_the_canonical_source_dir`: `canonical_source_dir` patched to return a temporary directory and `same_modified` patched to record `(source, source_dir)` and return `True`: the record for `dot_codex/modify_private_config.toml` carries that directory and every other record carries `None`, and no WARN line is returned; then `canonical_source_dir` patched to return `None`: the Codex record carries `None` and the returned messages hold exactly one line starting `WARN: Codex trust entry compared against the working clone`; `test_canonical_source_dir_reads_chezmoi_source_path_or_none`: `subprocess.run` patched: a `CompletedProcess` with exit 0 and a temporary directory plus a newline on stdout returns that `Path`; `FileNotFoundError` raised, exit 1, an empty stdout, and a stdout naming a path that does not exist each return `None`; the recorded argv of every call is `["chezmoi", "source-path"]`.

## Out of scope

The modify scripts themselves and the trust entry they render; `chezmoi_drift_warnings()`; the model-profile and Claude-settings comparisons; the Makefile's `doctor` target; `scripts/check-tools.sh`.

## Check

`uv run python -m unittest tests/unit/test_check_agent_runtime.py -v` green (the 52 existing tests plus the two new ones), pasted in the validation file with `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after 907522c2). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P2 on this PR whose fix stays within these files and is small is fixed in a revise round the orchestrator sends with a `check=` (correction C-50); any other P2 is advisory, owned by `dotfiles-T128-doctor-codex-trust-followup-a01`, which the orchestrator writes when the first such P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-doctor-codex-trust-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-doctor-codex-trust-a01/task.md>` and the evidence paths. After the merge the orchestrator runs `make doctor` from the working clone outside its sandbox (the sandbox denies mise's TLS) and pastes the ERROR count and the absence of the `Codex config managed keys differ` line into the acceptance record (D2); the operator's `make update` is not needed for this change (the doctor runs from the clone it lives in).

## Withdrawn (2026-10-15T06:57:32Z)

Not dispatched: the premise does not hold. `CHEZMOI_SOURCE_DIR=<working clone>/home home/dot_codex/modify_private_config.toml < ~/.codex/config.toml` and the same with `CHEZMOI_SOURCE_DIR=~/.local/share/chezmoi/home`: both rc 0, `outputs identical`, `canonical == applied`, `working == applied`; the script's `RUNTIME_PREFIXES` holds `projects` (the trust table is preserved from the current file, never rendered); `make doctor` from the working clone outside the sandbox: rc 0, `ERROR lines: 0`, no `Codex config` line. The task is kept as a record; no PR, no owner task.
