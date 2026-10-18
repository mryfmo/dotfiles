---
task_id: dotfiles-T133-task-generator-plan-check-a01
round: 1
status: result
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c). Branch `tools/task-generator-plan-check-a01` from `origin/main` 68f8a70a, rebased onto `origin/main` de3b73cc after #413 merged; PR #417 (draft until CI is green); tested code head d7332ebb9cef85a440a0d7c6a0b8a35136ad0690 (the RESULT names the final evidence-only head). Task copy `.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md` is byte-identical to the amended dispatched file: sha256 `e08bb0afe8d508f5327b0e199108ee1b74efdb5d4a2004faed93b1ca4d1f0c68`. INV-6: amendments=1 questions=1 revises=0.

## What changed

- `scripts/orchestrator/task-from-plan.py` (new, item 1): reads the todo row, the program items `(n)` it names, the Q-A row (`security: true` when the row lists the id or a `P1-a〜P1-b` range holds it) and the section-6 wave row; proposes `allowed_files` from the backtick paths plus `git grep -l -F <script> -- scripts tests` hits (each a `# from:` line in Files) and the task's own directory; drafts one residual row per path entry and copies the task-copy, evidence, non-path and orchestrator-effect rows of `dotfiles-T133-result-precheck-a01.md` with the id replaced; runs every backtick command of the items through the checker's own `rerun` (C14's environment, so C14 reproduces what it pastes; a nonzero exit is a `verify:` claim with its code, a gh, curl or URL command is not run); runs the sibling task file's Check commands once in a detached scratch worktree of `origin/main` and removes it; writes the file and prints the checker's verdict, exit 0 or 1.
- `scripts/orchestrator/task-consistency-check.py` (item 2): C11 to C15 after C10, C1 to C10 and C7b untouched. C14 runs each premise under `bash -c` with `set -o pipefail`, PATH `<root>/bin:/usr/bin:/bin` and HOME kept, timeout 1800 s, and compares after collapsing whitespace runs (amendment 1). A tool absent from that PATH is the warning `C14: tool absent <name>`, read from bash's own `bash: line N: <name>: command not found` line rather than from exit 127, because under pipefail `codex exec --help | grep -c x` exits with grep's 1. The skip note and the tool-absent warning are not findings: they go to stderr as `<file>: <note>`, so stdout keeps the docstring's contract of one `  C<n> …` line per finding (the reason is the historical test below, whose parser reads every indented stdout line as a finding id and is not to change).
- `scripts/orchestrator/plan-check.py` (new, item 3): F1 to F6 form checks, `--drift` (gh `pr view` per cited PR with a sha or state word near it, `024-progress.tsv` state against the latest acceptance status) and `--invariants` (the fixed forbidden patterns and `claude.permissions.ask` entries added against `origin/main`); one line per violation, exit 1.
- Tests (item 4): `tests/unit/test_task_from_plan.py`, `tests/unit/test_plan_check.py`, `tests/unit/test_task_consistency_c11_c15.py` (one red fixture per new check; amendment 1's whitespace and tool-absent cases, the latter for a bare command and a pipeline, asserting stdout holds the verdict alone). None imports PyYAML (`make unit-test` has none); YAML is read back through `uv run --no-project --with pyyaml`.

## The two edits of tests/unit/test_task_checkers.py (amendment 1, option (a))

Applied after the rebase onto #413's merge; the module's diff against `origin/main` is these two hunks and nothing else (validation.md).

1. `test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary`: the fixture row `{"control": "the PR adds scripts/foo.py<after>"}` gains `"disposition": "residual: a compensating control"` (the wording the module's other rows use). Without a disposition C13 reports `disposition is not closed:, residual: or out-of-scope: and a space` on every case; with it the expected sets (`{"C4"}` for `.bak`, empty otherwise) hold.
2. `test_task_consistency_check_detects_the_ten_historical_files`: ids added, each from the new check's finding on that file (pasted in validation.md):
   - process-rules a02, a03, a04, a05, a06 gain C14: their premise `~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep 'AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a01' | cut -c1-140` no longer prints the pasted line, so C14 reports `premise output differs from its rerun` in all three places it runs: in a seat's sandbox C14's environment has no TMPDIR, so the script's `mktemp` falls back to `/tmp`, which the sandbox denies, and it prints nothing; with a writable temp directory it prints the line cut at 140 bytes (C14's environment has no locale, so `cut -c` counts bytes, and `○` and `→` are three each), ending `st` where the paste ends `status`; on CI the script does not exist.
   - regime-counters a01 and a02, ci-skip-orchestration a01 and a02 gain C11 and C15: C11 because their `closed:` payloads are prose, not `tests/<path>::<identifier>` (and regime-counters' `out-of-scope: V2 (…)` names no task file); C15 because their `invariants` (INV-6 on regime-counters, INV-2 on ci-skip-orchestration) are not byte-equal to `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` on `origin/main`.
   - process-rules a01 gains nothing: its network premises are skipped (a note, on stderr) and its `wc -w home/dot_config/claude/rules/agmsg-orchestration.md` premise still prints 447 words after the whitespace collapse.

## Real runs (validation.md)

- The checker on the sixteen `.orchestration/tasks/dotfiles-T133-*.md` files (untracked in the main checkout, so run with `--root <main checkout>`): C1 to C13 and C15 clean on all sixteen. C14 reports seven files, each a premise the repository has moved past since it was pasted (amendment 1 keeps these as findings; five before #413 merged, seven after):
  - result-precheck a01 and a02: `grep -n '^RECORD_KEYS = ' scripts/require-crit-review.py` pasted the set without `"replans"`, which #413 (de3b73cc) added.
  - permission-guard-gate a01 and a02: `grep -c 'scope=permission' .orchestration/decisions.tsv` pasted 0, prints 1 now.
  - worker-cap-hookspath a01 and a02: `grep -c '^worker_cap:' home/dot_agents/agent-config.yaml` pasted 0, prints 1 since #408; the `Keep at most three workers in total|…` count pasted 2, prints 0.
  - worker-hooks-path a01: the `grep -n 'shell_environment_policy\|settings.local.json'` line numbers moved by one (352 to 353, 370 to 371, 1418 to 1419).
  - Warnings (not findings): `C14: tool absent uv` on verdict-audit-pool a01 and a02, `C14: tool absent codex` on worker-hooks-path a01.
  So the Check's "green (C1 to C15)" holds for C1 to C13 and C15 and not for C14 on those seven files.
- `plan-check.py` once against the main checkout (the plan files are untracked there): exit 1 with six violations, reported, not fixed (Out of scope):
  1. `F3 024-todo.md:22 P1-13 names no bottleneck id of 5.0 or 5.10`
  2. `F3 024-todo.md:23 P1-14 names no bottleneck id of 5.0 or 5.10`
  3. `F4 024-checklists.md:9 P1-a holds no backtick command or file path`
  4. `F6 024-omp-cutover-and-corrective-order.md:39 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file`
  5. `F6 024-omp-cutover-and-corrective-order.md:70` (the same id)
  6. `F6 024-todo.md:9` (the same id)

## Observations for the orchestrator (no change made)

- Threat-table wording: the `in-process effects` row says every premise and Check command "runs under python -I or bash with set -euo pipefail, never through a shell string the plan controls". Item 2 mandates C14's `bash -c` with `set -o pipefail` on the premise string, and item 1 pastes what C14 reruns, so both the generator and C14 do run a plan- or task-controlled string in a shell, under `set -o pipefail` (not `-eu`, which would change what a premise like `cmd; other` prints). The row's control is wrong as worded; the residual is that a task file's or plan item's backtick command runs with the caller's user rights, only on an orchestrator-written file. A corrected sentence: "premise and Check commands come from the task or plan text the orchestrator writes and run under `bash -c` with `set -o pipefail` and PATH `<root>/bin:/usr/bin:/bin`".
- C14 runs every premise of every file it is given, including the historical fixtures in `test_task_checkers.py`, whose `run_check` allows 120 s. Inside a seat's sandbox their `history.sh` premise fails at once (no TMPDIR, above). Outside a sandbox it reads the live agmsg bus in full, five times (one run took over 100 s here with a writable temp directory), so `make unit-test` run unsandboxed on a machine with the bus can time that test out. A trial that passed TMPDIR through to C14 (so premises that make temp files work inside a sandbox) turned the sandboxed run into that slow path and was reverted; C14's environment stays PATH and HOME only. A follow-up that runs the historical test with a temporary HOME would remove the bus from the unit suite; it is a test-line change amendment 1 does not allow here. The ten files' C14 ids rest on environment facts: `history.sh` older than 1000 messages or absent, `sha256sum` absent from `/usr/bin:/bin` on macOS (a warning) and present on Linux CI, and `agmsg-orchestration.md` staying at 447 words (a01 gains C14 the day it changes).
- The green-set subtest of `test_task_consistency_c11_c15.py` is skipped in this tree, because the T133 task files exist only untracked in the main checkout and on the unmerged boundary branch. It runs once they land on `main`.

[memory:decision] T133 P1-12: task-consistency-check.py C14 reruns premises under bash -c with pipefail and PATH <root>/bin:/usr/bin:/bin (env PATH and HOME only), compares after collapsing whitespace runs, and prints its skip notes and `C14: tool absent <name>` warnings on stderr, so stdout holds one `  C<n>` line per finding.

## Check (validation.md)

- The four modules: 12 tests OK, 1 skipped (the green-set subtest above).
- `make unit-test` exits 2 in the sandbox on this head (1198 tests) and on a pristine `origin/main` de3b73cc worktree (1195 tests); the 305 failing names are identical (`cmp`), none in this task's modules. CI's `make unit-test` decides the full suite.
- `make format` exits 2 at `shfmt --diff` on both sides with the same twelve pre-existing files; ruff and prettier pass on the changed `.py` and `.md` files.
- Caps (`git diff --numstat origin/main...HEAD`): 503 changed lines outside `tests/` and `.orchestration/` (cap 600), 373 under `tests/` (cap 700).

## Not done yet

The evidence commit, its push, CI on the final head, `gh pr ready`, the Bot window (no `@codex review`) and the RESULT (`task_copy=e08bb0af…`, `precheck=pending-411`).

cost: n/a
