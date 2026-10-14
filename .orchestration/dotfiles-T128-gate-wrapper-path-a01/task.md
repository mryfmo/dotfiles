---
format: 2
task_id: dotfiles-T128-gate-wrapper-path-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/orch-gate.sh
  - tests/unit/test_orch_gate_path.py
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T128-gate-wrapper-path-a01/**
after: [dotfiles-T128-orchestrator-tools-a06, dotfiles-T128-task-checkers-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/orch-gate.sh, behaviour one of item 1, the gate's PATH is a private directory of symlinks to the binaries the gate and the base's collector run by name, each resolved in the trusted root before the review worktree is entered
    disposition: "closed: tests/unit/test_orch_gate_path.py::test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries"
  - control: the PR edits scripts/orchestrator/orch-gate.sh, behaviour two of item 1, a binary resolved under a shims directory or not resolved at all is refused (exit 2) before the head checkout
    disposition: "closed: tests/unit/test_orch_gate_path.py::test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory"
  - control: the PR edits scripts/orchestrator/orch-gate.sh, behaviour three of item 1, the private directory is created after the EXIT trap is set and removed by it on every exit, a refusal included
    disposition: "closed: tests/unit/test_orch_gate_path.py::test_orch_gate_removes_the_private_bin_on_exit"
  - control: the PR edits tests/unit/test_orchestrator_tools.py in three places only (item 3), the stub interpreters' shebangs become absolute, the shared stub body records with builtins or absolute paths, and the explicit-environment test expects the private PATH; T704's own case in that module is untouched
    disposition: "residual: the three edits are named in item 3 and nothing else in the module changes; the audit reads the diff against origin/main after T704 merges"
  - control: the PR adds tests/unit/test_orch_gate_path.py, the oracle of item 1 (stub gh, git, mise and python on PATH; the gate stub records its environment and argv)
    disposition: "residual: the stubs record names and paths and run nothing else; the audit reads each case against item 1"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-gate-wrapper-path-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-gate-wrapper-path-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: nothing is imported into another process; the test runs orch-gate.sh as a subprocess with stubs on PATH"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; orch-gate.sh resolves gh, git and (when it is on this host) mise in the trusted root and nothing else by name; the test stubs them"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; the new file is a test module named in allowed_files"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the audit of PR #350's head 6847aa9f rated the gate wrapper's PATH a P1: the caller's PATH can resolve gh through a mise shim, and the gate launches gh with the review worktree (the PR head) as cwd, where a PR-owned mise.toml can point the shim at a PR binary"
    command: "grep -o '^\\[P1\\] high specification .\\{0,230\\}' .orchestration/validation/dotfiles-T128-orchestrator-tools-a06-audit-6847aa9.md.last.md"
    output: |-
      [P1] high specification .orchestration/tasks/dotfiles-T128-orchestrator-tools-a06.md:41 — **The prescribed PATH still permits PR-selected code.** `orch-gate.sh:72` preserves the caller’s PATH; on this host, `gh` resolves through a mise shim. The gate lau
  - claim: "what PATH resolves gh to depends only on PATH order: with the installs directory first it is the binary, with mise's shims directory first it is the shim; mise names the installed binary either way, and git is Homebrew's; so the wrapper must resolve through mise and refuse a shims path (the orchestrator shell holds the installs first, the Codex review sandbox the shims first)"
    command: "PATH=\"$HOME/.local/share/mise/installs/github-cli-cli/latest/bin:$PATH\" command -v gh; PATH=\"$HOME/.local/share/mise/shims:$PATH\" command -v gh; mise which gh; mise which git 2>/dev/null || command -v git"
    output: |-
      ~/.local/share/mise/installs/github-cli-cli/latest/bin/gh
      ~/.local/share/mise/shims/gh
      ~/.local/share/mise/installs/github-cli-cli/latest/bin/gh
      /opt/homebrew/bin/git
  - claim: "a private PATH of two symlinks to those binaries is enough for gh to authenticate (the keyring under HOME), so item 1 loses nothing the gate needs"
    command: "B=$(mktemp -d \"$TMPDIR/gatebin.XXXX\"); ln -s \"$(mise which gh)\" \"$B/gh\"; ln -s \"$(mise which git 2>/dev/null || command -v git)\" \"$B/git\"; env -i PATH=\"$B\" HOME=\"$HOME\" gh auth status 2>&1 | grep -c 'Logged in to github.com'"
    output: |-
        1
  - claim: "mise resolves per working directory: from a directory holding a PR-style mise.toml it no longer answers with the installed gh, which is the path a shim follows when the gate's cwd is the PR head"
    command: "D=$(mktemp -d \"$TMPDIR/prcwd.XXXX\"); printf '[tools]\\n\"github:cli/cli\" = \"path:./payload\"\\n' > \"$D/mise.toml\"; (cd \"$D\" && mise which gh 2>&1 | head -1)"
    output: |-
      mise ERROR gh is a mise bin however it is not currently active. Use `mise use` to activate it in this directory.
---

# AGMSG-TASK dotfiles-T128-gate-wrapper-path-a01 — the gate wrapper's PATH is a private bin of binaries resolved in the trusted root (the audit of 6847aa9f, P1; operator decision C of 2026-10-14; plan 021 step 7's unit)

Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time). The fourth P1 on one boundary of `scripts/orchestrator/orch-gate.sh` (the make target at the head, uv's `.python-version`, the inherited environment, now PATH) is answered as one short task with one mechanism, its own test module and the step-7 caps; the gate module's working directory for `gh` and the collector (`scripts/require-crit-review.py:519` and 610) is the gate lineage's and a separate short task. `orch-gate.sh` is called by no chain step until this lands (plan 021 step 6.3). Dispatch after T704 (`dotfiles-T128-task-checkers-a01`) merges (`after:`), because item 3 edits `tests/unit/test_orchestrator_tools.py`, which T704 holds until then; PR #350 is merged (28eec93c).

## Goal

The gate and every process it starts find `gh` and `git` only in a private directory of symlinks to binaries resolved in the trusted root before the review worktree is entered, so no shim and no configuration in the PR checkout can choose the code that runs with the orchestrator's credentials.

## Files

1. `scripts/orchestrator/orch-gate.sh`: after the interpreter is resolved and the review worktree is checked clean, set the EXIT trap first (it removes `${bin:-}` when set, then cleans and restores the review worktree as today), then create `bin="$(mktemp -d)"` and, for each name the gate module and the base's collector run by name (`gh` and `git`; the worker pastes `grep -n 'subprocess\|run_git\|\["gh"\|"git"' scripts/require-crit-review.py scripts/pr-feedback.py` in the validation file and extends the list only from it), resolve the binary in the trusted root: `mise which <name>` when `command -v <name>` lies under a directory named `shims` or `mise` is on PATH and knows the name, else `command -v <name>`; refuse (exit 2) a result under a `shims` directory or an empty result; `ln -s` it as `$bin/<name>`. The `env -i` line passes `PATH="$bin"` instead of the caller's PATH; everything else in that line stays. A shims refusal therefore also removes the directory. One comment names the audit finding.
2. `tests/unit/test_orch_gate_path.py` (new, its own stubs on PATH: `gh`, `git`, `mise`, and a gate python that records its environment and argv to a file; every stub's shebang is an absolute interpreter such as `#!/bin/bash`, and every stub records argv, cwd and environment with builtins or absolute paths (`export -p`, `pwd -P`, `printf`, `/usr/bin/env`, `/bin/cat`), because under the private PATH neither `bash` nor `env` nor `cat` is found by name):
   - `test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries`: the gate stub's `PATH` is one directory that contains exactly `gh` and `git`, each a symlink to the path the stub `mise which` answered; the caller's PATH directories are absent; and the resolution happened in the trusted root before the head checkout: every stub appends one line `<name> <argv> <cwd>` to a shared log, and the test asserts the `mise which` lines carry the trusted root as cwd and precede the stub git's `checkout` of the head (an implementation that resolves after entering the review worktree fails this assertion).
   - `test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory`: the stub `mise which gh` answers a path containing `/shims/`: orch-gate.sh exits 2 before the head checkout and the review worktree is untouched.
   - `test_orch_gate_removes_the_private_bin_on_exit`: after a run, and after the shims refusal, the directory no longer exists.
3. `tests/unit/test_orchestrator_tools.py`, three edits and nothing else: the orch-gate stubs' shebangs become absolute (`#!/bin/bash`); the shared stub body `RUN` records with builtins or absolute paths (`export -p` or `/usr/bin/env` for the environment, `/bin/cat` for the output file), because under the private PATH `env` and `cat` are not found and the environment file comes out empty; and `test_orch_gate_runs_the_gate_under_an_explicit_environment` expects the gate stub's `PATH` to be the private directory (one entry, containing `gh` and `git`) instead of the caller's PATH; T704's added case in that module stays as T704 lands it.

## Out of scope

Any change to `tests/unit/test_orchestrator_tools.py` beyond item 3's three edits; the gate module's working directory for `gh` and the collector (the gate lineage), the allowlist of names (a06 item 10, landed), T704, plan 021 step 6.3, any rule text.

## Check

`uv run python -m unittest tests/unit/test_orch_gate_path.py tests/unit/test_orchestrator_tools.py -v` green (the second module as T704 leaves it, with item 3's three edits), pasted in the validation file with `shellcheck scripts/orchestrator/orch-gate.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` after T704 merges. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; P2 are advisory and owned by `dotfiles-T128-orchestrator-tools-followup-a01` (rows in the a02 record's owner section). The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the three test names and item 3's three edits, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-gate-wrapper-path-a01/task.md>` and the evidence paths.
