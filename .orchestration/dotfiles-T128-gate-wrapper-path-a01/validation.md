---
task_id: dotfiles-T128-gate-wrapper-path-a01
seat: claude-standard-dot-a003
fix_commit: cb1f9cc4
---

# Validation: dotfiles-T128-gate-wrapper-path-a01

## 1. Task copy and base

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-gate-wrapper-path-a01.md .orchestration/dotfiles-T128-gate-wrapper-path-a01/task.md
3ccbc7bf90f4318cc807a2e14759d60e67ede8d7a0a0ae2d561a9b4c46fb0977  <main checkout>/.orchestration/tasks/dotfiles-T128-gate-wrapper-path-a01.md
3ccbc7bf90f4318cc807a2e14759d60e67ede8d7a0a0ae2d561a9b4c46fb0977  .orchestration/dotfiles-T128-gate-wrapper-path-a01/task.md
$ git log --oneline -3 && git merge-base origin/main HEAD && git log --oneline -1 origin/main
1483fef2 test(orchestrator): the PATH assertions print no environment value on failure
cb1f9cc4 fix(orchestrator): orch-gate.sh runs the gate with a private PATH of gh and git resolved in the trusted root
c15ba668 feat(orchestrator): task-consistency-check.py and ledger-check.py land with their tests (T704 a01) (#352)
c15ba668da20dc2956220077cb0f20054ab352c7
c15ba668 feat(orchestrator): task-consistency-check.py and ledger-check.py land with their tests (T704 a01) (#352)
```

- The TASK's `task_sha256` is `3ccbc7bf90f4318cc807a2e14759d60e67ede8d7a0a0ae2d561a9b4c46fb0977`, and the branch copy hashes to it.
- The branch starts from `c15ba668`, the merge of T704 (#352), as the task's `after:` requires.

## 2. The names the gate and its collector run (item 1's list)

```text
$ grep -n 'subprocess\|run_git\|\["gh"\|"git"' scripts/require-crit-review.py scripts/pr-feedback.py
scripts/pr-feedback.py:21:import subprocess
scripts/pr-feedback.py:74:    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False, env=gh_env())
scripts/pr-feedback.py:96:    result = subprocess.run(
scripts/pr-feedback.py:97:        ["gh", "auth", "status"],
scripts/require-crit-review.py:11:import subprocess
scripts/require-crit-review.py:133:def run_git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
scripts/require-crit-review.py:134:    return subprocess.run(
scripts/require-crit-review.py:135:        ["git", *args],
scripts/require-crit-review.py:139:        stdout=subprocess.PIPE,
scripts/require-crit-review.py:140:        stderr=subprocess.PIPE,
scripts/require-crit-review.py:145:    result = run_git(["rev-parse", "--show-toplevel"])
scripts/require-crit-review.py:209:        result = run_git(command, root)
scripts/require-crit-review.py:221:        result = run_git(command, root)
scripts/require-crit-review.py:231:    untracked = run_git(["ls-files", "--others", "--exclude-standard"], root)
scripts/require-crit-review.py:387:        run_git(["merge-base", "--is-ancestor", commit, head], root).returncode == 0
scripts/require-crit-review.py:388:        and run_git(["merge-base", "--is-ancestor", commit, base], root).returncode != 0
scripts/require-crit-review.py:449:        if commit and run_git(["cat-file", "-e", f"{commit}^{{commit}}"], root).returncode != 0:
scripts/require-crit-review.py:518:        repository = subprocess.run(
scripts/require-crit-review.py:519:            ["gh", "repo", "view", "--json", "nameWithOwner"],
scripts/require-crit-review.py:534:        result = subprocess.run(
scripts/require-crit-review.py:535:            ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "headRefOid,baseRefName,baseRefOid"],
scripts/require-crit-review.py:554:        or run_git(["cat-file", "-e", f"{github_base}^{{commit}}"], root).returncode != 0
scripts/require-crit-review.py:564:    resolved = run_git(["rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}"], root)
scripts/require-crit-review.py:569:        if run_git(["merge-base", "--is-ancestor", base_sha, github_base], root).returncode == 0:
scripts/require-crit-review.py:570:            first_parents = run_git(["rev-list", "--first-parent", head], root)
scripts/require-crit-review.py:574:        if run_git(["merge-base", "--is-ancestor", github_base, base_sha], root).returncode == 0:
scripts/require-crit-review.py:575:            actual = run_git(["merge-base", base_sha, head], root)
scripts/require-crit-review.py:576:            expected = run_git(["merge-base", github_base, head], root)
scripts/require-crit-review.py:605:        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
scripts/require-crit-review.py:609:        result = subprocess.run(
scripts/require-crit-review.py:614:            stdout=subprocess.PIPE,
scripts/require-crit-review.py:615:            stderr=subprocess.PIPE,
scripts/require-crit-review.py:938:    The same match as `grep -rl 'classes:.*<class>'`, without a subprocess; the gate reads its result, never
scripts/require-crit-review.py:973:    verify = run_git(["rev-parse", "--verify", "--quiet", "--end-of-options", f"{base}^{{commit}}"], root)
scripts/require-crit-review.py:996:    head = run_git(["rev-parse", "HEAD"], root).stdout.strip() if args.base else None
scripts/require-crit-review.py:1017:    current_head = head or run_git(["rev-parse", "HEAD"], root).stdout.strip()
```

Every external program is `gh` or `git`. Line 609 starts the collector as `sys.executable` (the pinned interpreter, an absolute path), so it needs no PATH lookup. The list stays `gh git`.

## 3. The resolution on this host, and gh under the private PATH

`scratchpad/path-probe.sh` builds the private directory with orch-gate.sh's loop, run from this worktree, and then makes the gate's first `gh` call and one `git` call under `env -i PATH=<private> HOME=$HOME`. It ran outside the sandbox (sandbox record, call 1), because `gh` reads the keyring. Home paths print as `~`.

```text
$ bash scratchpad/path-probe.sh <worktree>
gh -> ~/.local/share/mise/installs/github-cli-cli/latest/bin/gh
git -> /opt/homebrew/bin/git
PATH has 2 entries
{"nameWithOwner":"mryfmo/dotfiles"}
gh rc=0
1483fef2
git rc=0
```

- `gh` resolves through `mise which` to the installed binary, not the shim.
- `git` is not a mise tool: `mise which git` fails, and `command -v git` gives Homebrew's.
- `gh` authenticates with only those two links on PATH, and `git` runs.

### `mktemp -d` and TMPDIR on this host

The task's `bin="$(mktemp -d)"` failed every orch-gate test here. It ran inside the sandbox:

```text
$ echo "TMPDIR=$TMPDIR"; d=$(mktemp -d 2>&1); echo "plain: $d rc=$?"; d2=$(mktemp -d "${TMPDIR:-/tmp}/orch-gate.XXXXXX"); echo "template: $d2"; rmdir "$d2"
TMPDIR=/tmp/claude-501
plain: mktemp: mkdtemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.qoiNu4mXNy: Operation not permitted rc=1
template: /tmp/claude-501/orch-gate.exkJmW
```

- Without a template, this macOS `mktemp -d` ignores `TMPDIR` and writes under the per-user `/var/folders/…/T`, which the Claude sandbox denies.
- With an explicit template under `${TMPDIR:-/tmp}`, it honours `TMPDIR`, as GNU `mktemp` also does.
- So orch-gate.sh uses `mktemp -d "${TMPDIR:-/tmp}/orch-gate.XXXXXX"`. `test_orch_gate_removes_the_private_bin_on_exit` pins that the directory lies under the caller's `TMPDIR`.

## 4. Tests and linters

The tests ran with `UV_OFFLINE=1 uv run --no-project` from the uv cache, because the sandbox has no pypi. CI runs `make unit-test` online.

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orch_gate_path.py tests/unit/test_orchestrator_tools.py -v
test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory (tests.unit.test_orch_gate_path.OrchGatePathTest.test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory) ... ok
test_orch_gate_removes_the_private_bin_on_exit (tests.unit.test_orch_gate_path.OrchGatePathTest.test_orch_gate_removes_the_private_bin_on_exit) ... ok
test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries (tests.unit.test_orch_gate_path.OrchGatePathTest.test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries) ... ok
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record) ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit) ... ok
test_boundary_commits_pushes_and_queues_the_pr (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_commits_pushes_and_queues_the_pr) ... ok
test_boundary_stops_before_commit_when_the_validator_fails (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_stops_before_commit_when_the_validator_fails) ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_closes_a_task_on_any_non_revise_acceptance) ... ok
test_bus_read_ignores_closers_between_other_endpoints (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_ignores_closers_between_other_endpoints) ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event) ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_refuses_a_read_that_reaches_its_limit) ... ok
test_bus_read_skips_and_counts_malformed_rows (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_skips_and_counts_malformed_rows) ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash) ... ok
test_design_keydiff_names_the_changed_invariant (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_design_keydiff_names_the_changed_invariant) ... ok
test_dispatch_line_grammar_table (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_line_grammar_table) ... ok
test_dispatch_passes_the_line_byte_identical (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_passes_the_line_byte_identical) ... ok
test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history) ... ok
test_dispatch_records_the_sent_line_with_its_read_marker (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_records_the_sent_line_with_its_read_marker) ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file) ... ok
test_dispatch_refuses_a_line_without_a_task_id (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_without_a_task_id) ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_malformed_record_block_before_sending) ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields) ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line) ... ok
test_dispatch_refuses_an_unwritable_record_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_an_unwritable_record_before_sending) ... ok
test_dispatch_refuses_malformed_lines (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_malformed_lines) ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_local_edits_across_the_fast_forward) ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_notice_annotations_and_success_statuses) ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_ignores_a_disposition_reply_from_another_login) ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_leaves_a_badged_review_body_a_gap) ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_refuses_a_not_applicable_without_evidence) ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt) ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap) ... ok
test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree) ... ok
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration) ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves) ... ok
test_orch_gate_restores_the_review_worktree_when_setup_fails (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_restores_the_review_worktree_when_setup_fails) ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree) ... ok
test_orch_gate_runs_the_gate_under_an_explicit_environment (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_runs_the_gate_under_an_explicit_environment) ... ok
test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs) ... ok
test_replay_propagates_the_command_status (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_replay_propagates_the_command_status) ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_prints_body_matches_and_states_a_capped_memory_count) ... ok
test_three_repeat_prints_the_records_search_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_prints_the_records_search_line) ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout) ... ok

----------------------------------------------------------------------
Ran 43 tests in 33.427s

OK
```

```text
$ shellcheck scripts/orchestrator/orch-gate.sh; echo "shellcheck rc=$?"
shellcheck rc=0
$ f="$PWD/scripts/orchestrator/orch-gate.sh"; (cd "$TMPDIR" && shfmt --indent 4 --space-redirects -d "$f"); echo "shfmt rc=$?"
shfmt rc=0
$ ruff format --config ruff.toml --check tests/unit/test_orch_gate_path.py tests/unit/test_orchestrator_tools.py && ruff check --config ruff.toml tests/unit/test_orch_gate_path.py
2 files already formatted
All checks passed!
```

## 5. Mutation proofs (`scratchpad/mutate-path.py`)

The method:

- edit one span of `orch-gate.sh` at `1483fef2`;
- run `tests.unit.test_orch_gate_path` and `test_orch_gate_runs_the_gate_under_an_explicit_environment` by their dotted names;
- count a kill only when the run fails on an `AssertionError`;
- restore the file with `git checkout --`.

The mutants:

- **M1** passes the caller's PATH, the line before this fix.
- **M2** checks the head out before the resolution.
- **M3** drops the shims check.
- **M4** drops the empty-or-relative check.
- **M5** leaves the private directory in place in the trap.
- **M6** resolves with `command -v` only, without mise.
- **M7** runs `mise which` from the review worktree.

```text
$ uv run --no-project python scratchpad/mutate-path.py <worktree>
KILLED M1 the caller's PATH (the pre-fix line) :: FAIL: test_orch_gate_removes_the_private_bin_on_exit, FAIL: test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries, FAIL: test_orch_gate_runs_the_gate_under_an_explicit_environment :: AssertionError: False is not true
KILLED M2 the head checked out before the resolution :: FAIL: test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory, FAIL: test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory, FAIL: test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries :: AssertionError: Lists differ: [] != ['git -C /private/tmp/claude-501/tmp9poq_e[104 chars]567']
KILLED M3 no shims check :: FAIL: test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory, FAIL: test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory, FAIL: test_orch_gate_removes_the_private_bin_on_exit :: AssertionError: 2 != 0 : 
KILLED M4 no empty-or-relative check :: FAIL: test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory :: AssertionError: 2 != 0 : 
KILLED M5 the trap keeps the private directory :: FAIL: test_orch_gate_removes_the_private_bin_on_exit :: AssertionError: Lists differ: [] != ['orch-gate.uCV7xF']
KILLED M6 command -v only, no mise :: FAIL: test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory, FAIL: test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory, FAIL: test_orch_gate_removes_the_private_bin_on_exit, FAIL: test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries :: AssertionError: 2 != 0 : 
KILLED M7 mise run from the review worktree :: FAIL: test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries :: AssertionError: Lists differ: [('mi[50 chars]/root'), ('mise which git', '/private/tmp/clau[21 chars]ot')] != [('mi[50 chars]/root/.claude/worktrees/orchestrato
kills 7/7
DIRTY
```

- **The result: 7/7 killed.** `DIRTY` is the untracked evidence directory, which was not yet committed then. `git checkout --` restored `orch-gate.sh` after each mutant.
- **M4 on macOS.** BSD `ln -s` accepts an empty target, so the gate ran and exited 0 where the test expected 2. GNU `ln -s` refuses an empty target and exits 1. The test fails either way.

## 6. Caps

```text
$ git diff --numstat origin/main...HEAD
18	7	scripts/orchestrator/orch-gate.sh
113	0	tests/unit/test_orch_gate_path.py
13	6	tests/unit/test_orchestrator_tools.py
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^\.orchestration\// {f++; if ($3 ~ /^tests\//) {ta+=$1} else {c+=$1+$2}} END {print "files", f, "changed_non_test", c, "added_test", ta}'
files 3 changed_non_test 25 added_test 126
```

Step 7.2 and INV-2 hold:

- **Outside `tests/`:** 25 changed lines (18 added, 7 deleted) of 200.
- **Under `tests/`:** 126 added lines of 1000.
- **Files:** 3 outside `.orchestration`.
