---
format: 2
task_id: dotfiles-T128-validator-offline-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - Makefile
  - tests/unit/test_makefile_offline.py
  - .orchestration/dotfiles-T128-validator-offline-a01/**
after: []
threat_table:
  - control: the PR edits Makefile in one place (one variable UV_PYYAML, used by the validate-agent-assets and render-check recipes), which runs the two validators through the uv cache when it holds PyYAML and through the index only when it does not
    disposition: "closed: tests/unit/test_makefile_offline.py::test_the_recipe_falls_back_only_when_the_cache_is_cold"
  - control: the PR adds tests/unit/test_makefile_offline.py, the oracle of the row above (a stub uv first on PATH that appends its argv to a file and exits with the code the test chose for the probe and for the run; make runs the repository target with that PATH)
    disposition: "residual: the stub records and answers, nothing else; the audit reads each case against the Files items"
  - control: "the uv cache (uv cache dir) and the network: the probe and the cached form read the cache only (uv run --offline); the index form reaches the index exactly as both recipes do today, and only when the probe failed"
    disposition: "residual: the cached form cannot install anything new, and the index form is today's recipe; the closed row's case two shows the index form running only after a failed probe and case one shows it absent after a successful one"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-validator-offline-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-validator-offline-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the test module imports only the standard library and runs make as a subprocess with a temporary PATH prefix holding the stub uv; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the recipes run uv by name from PATH, as today, and uv runs the two repository scripts by their paths relative to the repository root, as today; the test's seam is PATH, which puts the stub uv first; a PR checkout as cwd chooses nothing: make reads the Makefile of the checkout it runs in, which is the trusted main checkout for the orchestrator's D10 and the worker's own worktree in the test"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the Makefile on origin/main runs both validators as bare uv run --with pyyaml recipes, which resolve against the index on every run'
    command: 'git show origin/main:Makefile | /usr/bin/grep -c "uv run --with pyyaml scripts/validate-agent-assets.py\|uv run --with pyyaml scripts/generate-agent-configs.py --check"'
    output: |-
      2
  - claim: 'the test module is new on origin/main'
    command: 'git cat-file -e origin/main:tests/unit/test_makefile_offline.py 2>/dev/null && echo present || echo absent'
    output: |-
      absent
  - claim: 'the lifecycle bats suite pins neither recipe text, so it stays out of allowed_files'
    command: 'git show origin/main:tests/install/common/lifecycle.bats | /usr/bin/grep -c "make validate-agent-assets\|make render-check"'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-validator-offline-a01 — the two validator recipes run from the uv cache when it holds PyYAML and reach the index only when it does not (plan 022 T5, definition of done D10; a Claude seat)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. `make validate-agent-assets` and `make render-check` run `uv run --with pyyaml <script>`, which resolves PyYAML against the index on every run; inside the Claude sandbox, which allows only the GitHub hosts, uv fails with `Failed to fetch: https://pypi.org/simple/...` and exit 2 although the cache holds PyYAML, so the orchestrator seat has run both validators by hand as `uv run --offline --with pyyaml` all session. Plan 022 T5 had proposed falling back on uv's exit 2; the orchestrator's replay on 2026-10-15 shows why that cannot work: `uv run --offline --with <uncached package>` exits 1 (`No solution found when resolving --with dependencies`, the network-disabled hint), the same code as a validator finding, while the index form exits 2 only when the network is denied. The recipe therefore decides by a probe that runs no validator: `uv run --offline --with pyyaml python -c 'import yaml'` succeeds exactly when the cache holds PyYAML.

## Goal

Both validators run with the exit status of the validator alone, from the cache whenever it holds PyYAML and through the index only when it does not, so D10 (`make validate-agent-assets` and `make render-check` exit 0 from the sandboxed orchestrator seat) holds without a by-hand form.

## Files

1. `Makefile`: one recursively expanded variable, `UV_PYYAML = $(if $(shell uv run --offline --with pyyaml python -c 'import yaml' 2> /dev/null && echo y),uv run --offline --with pyyaml,uv run --with pyyaml)`, defined once above the two recipes with a one-line comment stating why (the index form fails inside the Claude sandbox while the cache holds PyYAML); the `validate-agent-assets` recipe becomes `$(UV_PYYAML) scripts/validate-agent-assets.py` and the `render-check` recipe `$(UV_PYYAML) scripts/generate-agent-configs.py --check`. The variable is recursive (`=`, not `:=`), so the probe runs only when a recipe expands it, never at parse time for other targets. Failure modes stated: the probe succeeds and the validator runs from the cache, its exit status returned as is (make exits 2 for a failed recipe, as today); the probe fails (cold cache, or uv missing) and the validator runs through the index, exactly today's recipe, its exit status returned as is; a validator finding is never retried, because the probe runs no validator. Nothing else in the Makefile changes.
2. `tests/unit/test_makefile_offline.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library: `test_validator_targets_try_the_offline_form_first` reads the Makefile text and asserts that the `UV_PYYAML` definition holds both `uv run --offline --with pyyaml` and `uv run --with pyyaml` and that the two recipes run `$(UV_PYYAML) scripts/validate-agent-assets.py` and `$(UV_PYYAML) scripts/generate-agent-configs.py --check`; `test_the_recipe_falls_back_only_when_the_cache_is_cold` writes a stub `uv` into a temporary directory put first on PATH, which appends its argv as one line to a file and exits with `PROBE_RC` when its argv ends with `-c` `import yaml` and with `RUN_RC` otherwise, then runs `make -C <repository root> validate-agent-assets` with that environment: case one, `PROBE_RC=0 RUN_RC=0`: two lines, the probe and `run --offline --with pyyaml scripts/validate-agent-assets.py`, make exit 0; case two, `PROBE_RC=1 RUN_RC=0`: two lines, the probe and `run --with pyyaml scripts/validate-agent-assets.py` (no `--offline`), make exit 0; case three, `PROBE_RC=0 RUN_RC=1`: two lines, the second the offline form, make exit non-zero, and no third line (the finding is not retried). The test asserts the whole argv list each time.

## Out of scope

The two validator scripts, `uv` itself and its cache, the sandbox manifest's hosts, the README's by-hand commands under `home/dot_agents/README.md`, every other Makefile target.

## Check

`uv run python -m unittest tests/unit/test_makefile_offline.py -v` green, pasted in the validation file with `make -n render-check` and `make -n validate-agent-assets` (the expanded recipe lines) and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after 59599783). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-validator-offline-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-validator-offline-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-validator-offline-a01/task.md>` and the evidence paths. After the merge the orchestrator runs `make validate-agent-assets` and `make render-check` from its sandboxed seat (D10) and pastes both exit statuses into the acceptance record.
