---
format: 2
task_id: dotfiles-T128-seat-liveness-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/check-regime-boundary.sh
  - tests/unit/test_check_regime_boundary.py
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T128-seat-liveness-a01/**
after: []
threat_table:
  - control: the PR edits scripts/check-regime-boundary.sh in its worker-seat loop, which asks the terminal driver for each seated worker's pane state through the seat's placement record and names the stale removal when the pane is gone
    disposition: "closed: tests/unit/test_check_regime_boundary.py::test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal"
  - control: the PR edits tests/unit/test_check_regime_boundary.py (one new test beside the nine, which stay as they are; fakes for identities.sh, lib/actas-lock.sh and lib/terminal-registry.sh under the test's HOME answer the state the case chooses)
    disposition: "residual: the fakes record and answer, nothing else; the audit reads each case against item 1"
  - control: the PR edits home/dot_local/bin/common/executable_herdr-agents in two places, the attach path printing one seat_stale= line per seated worker whose pane is gone and the remove-worker path gaining --stale, which retires only such a seat
    disposition: "closed: tests/unit/test_herdr_agents.py::test_remove_worker_stale_retires_a_seat_whose_pane_is_gone"
  - control: the PR edits tests/unit/test_herdr_agents.py (two new tests beside the 189, which stay as they are; the module's fake agmsg scripts gain a fake lib/terminal-registry.sh and a fake agmsg_spawn_path answering from files the case writes)
    disposition: "residual: the fakes record and answer, nothing else; the audit reads each case against item 2"
  - control: "the placement record under the agmsg run directory (the seat's retry authority for despawn) and herdr's agent list: the lookup reads the record through upstream agmsg_spawn_path and asks the driver's terminal_pane_state, which reads herdr's agent list and never a pane's content"
    disposition: "residual: gone is the only state that retires a seat, only on an explicit --stale call, and the record is moved into the run directory's stale/ subdirectory with a timestamp suffix, never deleted and no longer in the spawn.* scan; present and unknown leave everything as it is and name the despawn path; the closed rows' cases cover gone, present and unknown"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-seat-liveness-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-seat-liveness-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: both test modules import only the standard library and run the two scripts as bash subprocesses with HOME set to a temporary tree holding the fake agmsg scripts and a fake herdr; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; both scripts run bash, git, awk, sed and the agmsg scripts under HOME/.agents/skills/agmsg/scripts by that fixed path, as today, and the new lookup sources that directory's lib/actas-lock.sh and lib/terminal-registry.sh in a child bash with SKILL_DIR set, which the driver then uses to run herdr and sqlite3 (it parses herdr's JSON with sqlite3; either absent yields unknown) from PATH, as despawn.sh does; the tests' seam is HOME; a PR checkout as cwd chooses nothing, because the boundary check reads the worktree list of the checkout it runs in and the launcher the main checkout it is given"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the boundary check on origin/main reports a seated worker with one fixed line that names the despawn path only'
    command: 'git show origin/main:scripts/check-regime-boundary.sh | /usr/bin/grep -c "worker still seated at"'
    output: |-
      1
  - claim: 'the launcher on origin/main has neither a --stale option nor a seat_stale= line'
    command: 'git show origin/main:home/dot_local/bin/common/executable_herdr-agents | /usr/bin/grep -c -e "--stale" -e "seat_stale="'
    output: |-
      0
  - claim: 'the launcher test module on origin/main holds 189 tests, which this task keeps'
    command: 'git show origin/main:tests/unit/test_herdr_agents.py | /usr/bin/grep -c "def test_"'
    output: |-
      189
  - claim: 'the boundary check test module on origin/main holds nine tests, which this task keeps'
    command: 'git show origin/main:tests/unit/test_check_regime_boundary.py | /usr/bin/grep -c "def test_"'
    output: |-
      9
---

# AGMSG-TASK dotfiles-T128-seat-liveness-a01 — the boundary check and the launcher tell a seated worker whose pane is gone from a live one, and `--remove-worker --stale` retires the dead seat (plan 022 T6, correction C-49 of M-20261015-01; a Claude seat)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. M-20261015-01: after the Claude Code restart of 2026-10-14 the four worker seats' Herdr workspace was gone, but their agmsg identities, delivery hooks and placement records remained; `herdr-agents --remove-worker` stopped at the despawn (`status=needs-force`, then `force-teardown-unconfirmed`, because the herdr driver's despawn of a pane that no longer exists is an ordinary error, not a confirmed teardown) and never reached `delivery.sh set off`, `leave.sh` or the record, and `make check-regime-boundary` counted the identities as seated workers with the despawn hint. The sanctioned existence lookup is the one upstream `despawn.sh` already uses: the driver's `terminal_pane_state <pane id>` prints `present`, `gone` or `unknown` (`gone` only when herdr's agent list was read whole and decidable; `unknown` with exit 10 otherwise), reads herdr's agent list and never a pane's content, and the placement record is found with upstream `agmsg_spawn_path <team> <member>` (`lib/actas-lock.sh`, id-keyed records). Plan 022 T6 had named the driver's `where` capability and raw `herdr workspace list`/`agent list` readings; `where` answers a pane's location and leaves existence deliberately outside (its own comment), so the task uses the pane state. Verified by the orchestrator on 2026-10-15 from its sandboxed seat (the herdr socket is allowlisted), the chain `agmsg_spawn_path` → first field of the record's first line → `agmsg_terminal_ref_terminal`, `agmsg_terminal_ref_id`, `agmsg_terminal_load`, `terminal_pane_state`: `herdr:…:wA:p5` (a live seat) `present` rc 0, `herdr:…:wA:p3` (a live seat) `present` rc 0, `herdr:…:wA:p77` (no such pane) `gone` rc 0.

## Goal

At a boundary, `make check-regime-boundary` names the stale removal for a seated worker whose pane is gone and the despawn path for every other seated worker; `herdr-agents --attach` prints one `seat_stale=<worktree>` line per such seat; `herdr-agents --remove-worker <worktree> --stale` retires exactly such a seat (delivery off, identity left, placement record moved aside) and refuses every other.

## Files

1. `scripts/check-regime-boundary.sh`: a function `seat_pane_state <team> <name>` that prints `present`, `gone` or `unknown`: it runs `env SKILL_DIR="${HOME}/.agents/skills/agmsg" bash -c '…' _ "${scripts}" "${team}" "${name}"`, where the child sources `"$1/lib/actas-lock.sh"` and `"$1/lib/terminal-registry.sh"`, takes the record from `agmsg_spawn_path "$2" "$3"`, the pane id as the first tab-separated field of the record's first line, the terminal from `agmsg_terminal_ref_terminal`, the bare id from `agmsg_terminal_ref_id`, loads the driver with `agmsg_terminal_load` and prints `terminal_pane_state`'s output; any failing step, an empty output or an output other than `present` or `gone` prints `unknown` (fail safe: an unreadable state never retires anything). In the worker-seat loop, for a worktree with a seated identity, the first `<team>\t<name>` row of `identities.sh` for that worktree (the type that produced it) decides: when the state is `gone` the violation reads `worker seated but its pane is gone at <worktree> (herdr-agents --remove-worker <worktree> --stale)`; otherwise the existing line stays as it is. Nothing else in the script changes.
2. `home/dot_local/bin/common/executable_herdr-agents`: (a) the same `seat_pane_state` function (the launcher is installed under `~/.local/bin`, so it cannot call a repository script), in the `env SKILL_DIR=… bash -c 'source "$1" && …'` form `check_worker_linkage` already uses for `agmsg_spawn_path`; (b) `--remove-worker <worktree> [--force] [--stale]`: `--stale` is parsed beside `--force` and documented in `usage()` and the shdoc header; in the remove block, when `--stale` is given the states of every identity row of the worktree are read before anything changes and each must be `gone`, otherwise the launcher prints `herdr-agents: <name> at <worktree> is <state>, not gone; use --remove-worker without --stale.` to stderr and exits 2 with nothing changed; when every row is `gone` the despawn is skipped and the launcher runs, per row, `delivery.sh set off <type> <worktree>`, `leave.sh <team> <name>`, moves the placement record (`agmsg_spawn_path`'s path) to `<run directory>/stale/<record basename>.<UTC timestamp, %Y%m%dT%H%M%SZ>` (moved out of the `spawn.*` scan of upstream's placement code, never deleted: the record is the evidence M-20261015-01 lacked, and a later seat on the same pane id must not read it as a rival claim), closes the tab best-effort as today, and prints `Herdr agents worker retired (stale): <name> (<worktree>)`; without `--stale` the block runs as today; the dirty-worktree refusal and the orchestrator-identity check (`leader`) stay before both paths; (c) in `claim_seat_and_print_directive`, only when the claim was not skipped (the orchestrator's own pane; a worker pane's SessionStart stays quiet as today), after the claim line is printed and before the directive, for each linked worktree of the main checkout under `.claude/worktrees/` (`git worktree list --porcelain`) that holds an identity of either type, when its state is `gone` one line `seat_stale=<worktree relative to the main checkout>` is printed. Failure modes stated: an `unknown` state (herdr unreachable, a missing or unreadable record, the libraries missing) prints no `seat_stale=` line and refuses `--stale`, so the despawn path stays the default; a `present` state refuses `--stale`.
3. `tests/unit/test_check_regime_boundary.py`: one new test, `test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal`, beside the nine, in the module's style (the temporary HOME holding fake agmsg scripts, the script run as a subprocess): the temporary repository gains a linked worktree under `.claude/worktrees/` (`git worktree add`), since the loop inspects only the paths `git worktree list` reports; fakes under `HOME/.agents/skills/agmsg/scripts/` for `identities.sh` (one row `dotfiles\tclaude-standard-dot-a009` for the seated worktree path and type claude-code, nothing for other paths), `lib/actas-lock.sh` (an `agmsg_spawn_path` that prints the path of a record the test writes, whose first line is `herdr:<a socket path>:wA:p9\t<worktree>\tclaude-code`) and `lib/terminal-registry.sh` (the four functions, `terminal_pane_state` printing the content of a state file); three cases: `gone` prints the stale-removal line and not the despawn line; `present` prints the despawn line only; `unknown` prints the despawn line only; the test asserts the full set of violation lines about that worktree each time.
4. `tests/unit/test_herdr_agents.py`: two new tests beside the 189, in the module's style (`write_worktree_seat`, `write_seat_lifecycle_fakes`, `add_seat_worktree`, `run_helper`, the calls file): `test_attach_names_stale_seats` (the fake libraries above under the test's HOME; state `gone`: stdout holds `seat_stale=.claude/worktrees/b1` after the `seat_claim=` line; state `present`: no `seat_stale=` line) and `test_remove_worker_stale_retires_a_seat_whose_pane_is_gone` (state `gone`: `--remove-worker .claude/worktrees/b1 --stale` exits 0, the calls are `delivery set off claude-code <worktree>` then `leave dotfiles claude-standard-dot-a007` in that order with no `despawn` call, the record path no longer exists and exactly one file `stale/<record basename>.<timestamp>` exists under the run directory; state `present`: exit 2, no `delivery`, `leave` or `despawn` call, the record untouched); each test asserts the whole calls list.

## Out of scope

Upstream agmsg (`despawn.sh`, the drivers, `agmsg_spawn_path`); the actas lock of a dead seat (`--add-worker` replaces a stale lock today); `team.sh`; the pane-less start summary; the Stop checklist text in the skill; every other option of the launcher.

## Check

`uv run python -m unittest tests/unit/test_check_regime_boundary.py tests/unit/test_herdr_agents.py -v` green (the 198 existing tests plus the three new ones), pasted in the validation file with `shellcheck scripts/check-regime-boundary.sh home/dot_local/bin/common/executable_herdr-agents` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after 59599783). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-seat-liveness-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-seat-liveness-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-seat-liveness-a01/task.md>` and the evidence paths. After the merge the operator runs `make update` (the launcher lives under `home/`); the next `herdr-agents --attach` prints `seat_stale=` for a dead seat or nothing, and `make check-regime-boundary` from the orchestrator seat names the stale removal for one.

## Change (round 2, 2026-10-15 05:5xZ)

The review seat's round 1 (one P2, five P3 clauses; the Codex half confirmed round 1): the retired record is moved into the run directory's `stale/` subdirectory instead of renamed in place, so upstream's `spawn.*` placement scan (a later seat naming its pane) never reads it as a rival claim; `--stale` reads every identity row's state before anything changes; the orchestrator-identity check stays before both remove paths; `seat_stale=` lines print only when the claim was not skipped; the boundary test adds a linked worktree; the environment row names sqlite3; item 2(a) points at the form `check_worker_linkage` already uses.
