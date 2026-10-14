# Report: dotfiles-T128-orchestrator-tools-a05

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on PR #346's branch `tools/orchestrator-scripts-2`, continuing from `7b574d32`. That head and every commit before it stay (validation §1).
- Task file sha256 `eaac8e4b…` matches the TASK's `task_sha256`. It is copied byte-identical to `.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md`. The a02 task copy and evidence records are not edited.
- The delta is items 7 to 9 with their tests (`608b38a2`), this task copy, and this evidence. a02's items 1 to 6 stand as implemented at `7b574d32`. PR-B (`acceptance-front-matter.py`, `orch-gate.sh`) waits for PR-A's merge.

## Items 7 to 9 (`608b38a2`)

| Item | Finding (the audit of `7b574d32`) | Fix | Closing test |
|---|---|---|---|
| 7 | P1 `fill_sweep.py:49`: a thread reply by any account that is not the Codex Bot supplied a disposition, the latest reply winning | A reply supplies a disposition only when its author is `--orchestrator-login <login>`. A reply by any other login is printed as `ignored-reply <comment id> <login>` and supplies nothing. The option is required, given once, and must match `^[A-Za-z0-9-]{1,39}$`; otherwise the script exits 2 before reading or writing a file. The login appears nowhere in the script | `test_fill_sweep_ignores_a_disposition_reply_from_another_login` (F1 to F5) |
| 8 | P1 `fill_sweep.py:60`: the rule table auto-dispositioned `review`, `codex_review` and `issue_comment` items whatever their body carried | No rule applies to a body that carries `![P<n> Badge](` with `<n>` in 0 to 3. The item stays a gap unless `extra.tsv` has its row. The neutral-level rule stays for badge-free annotations and statuses. A bare `P0`, as in the review summary's hidden `"blockingSeverityThreshold":"P0"`, is not a badge | `test_fill_sweep_leaves_a_badged_review_body_a_gap` (F6, F7) |
| 9 | P1 `orch-audit.sh:62` to 72: the lineage copy brought this head's earlier receipt into the review checkout, and the receipt was removed in the main checkout only | Before the run:<br>- this head's receipt and `.last.md` are removed in both checkouts;<br>- the lineage copy skips them;<br>- a timestamp file is written with `mktemp`.<br>After the run, the script exits 3 unless `.last.md` exists, is non-empty, and is newer than that file (`find -newer`). | `test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt` (A1, A2; it fails against `7b574d32`, validation §4) |

Two changes go beyond the items' literal text, both on purpose:

- **Item 7's own-reply rule.** At `7b574d32` an item took this rule when it was a review comment by any non-bot account whose body starts with `Disposition (orchestrator`. That is the same trust gap as the reply path, so the rule now requires `author` (the sweep's login field) to equal `--orchestrator-login`. A look-alike comment by another login is a gap. The item 7 test covers it (F3).
- **Item 8's badge gate.** The gate sits on the one line that picks a rule, so it applies to every rule source, the own-reply rule included, not only the five sources item 8 names. An orchestrator reply that quoted a badge would become a gap that `extra.tsv` fills. That is the safe direction.

Item 9's test runs three times with stubbed codex modes:

- `codex-silent` exits 0 and writes nothing. The earlier receipt is in the main checkout and tracked on `origin/main`, so the review checkout has it too.
- `codex-stale` writes a receipt dated 2000.
- The normal mode writes a fresh receipt.

The first two must exit 3 with no verdict line and leave the review checkout clean. The third must print the verdict. That third run also shows `find -newer` resolves a write a few milliseconds after the timestamp, on macOS here; CI covers Linux.

Mutation proofs (validation §3):

- 11 mutants: 9 killed by assertions, 2 survived.
- A3 (the review-checkout `rm`) and A4 (the lineage skip) survive alone because the other guards cover them.
- A2 (the review `rm` and the freshness check both removed) is killed.
- Validation §3 explains each survivor.

## The size cap

The drafted fixes first came to 506 added lines outside `tests/`, 6 over the cap of 500. The task does not allow moving a script out of PR-A: a02's items 1 to 6 stand as implemented, and no new branch or PR is made for PR-A. So the two files under edit were tightened, with no behavior change:

- `orch-audit.sh`'s `@description` is rewrapped at one width, with the new facts added.
- Its lineage loop uses `[[ … ]] || continue` in place of `if … fi`.
- `fill_sweep.py`'s disposition count is one named line plus its `print`, in place of a four-line call.

The result is 497 added lines outside `tests/` and 493 under it, in 12 files outside `.orchestration/` (validation §2). No other file was touched for the cap.

## Results

- `test_orchestrator_tools.py`: 30 tests OK. `test_regime_counters.py`: 27 tests OK.
- shellcheck 0.11.0, shfmt 3.14.1 (`-i 4 -sr`), ruff format and ruff check: clean.
- The two existing `fill_sweep.py` tests now pass `--orchestrator-login`, since the option is required. They share a `sweep`/`fill_sweep` helper. The codex stub gained the `codex-silent` and `codex-stale` modes, and its default behaviour is unchanged.

## Bot threads on PR #346

The main-checkout copy lists every Bot thread with its disposition, read after the push.

## Not done, or outside scope

- PR-B: after PR-A merges.
- The full `tests/unit` discover is left to CI (validation §4).
- Understand-Anything hook: did not fire. plan-mode-used: no.

cost: n/a

## Revise round on `8576645c` (`5582fa3c`)

- The audit's P1 (`dispatch.sh:80` against `regime-counters.sh:115`): dispatch.sh accepts a tab or a whitespace run between tokens (`[[:blank:]]+` in its header check, `read -ra` for the tokens). The counters split each history body on one space, so such AGMSG-TASK, RESULT and PONG lines escaped the INV-6 counts.
- The fix, `scripts/regime-counters.sh:115`, has two steps:
  1. It undoes the escapes that `read_history`'s `jq @tsv` adds: `\t`, `\n`, `\r` and `\\`, in one left-to-right pass, so an escaped backslash before a `t` stays a backslash and a `t`. Without this step a tab read from the store arrives as the two characters `\t` and never splits.
  2. It splits on runs of whitespace (`\s+`) and drops empty tokens, as `read -ra` does.

  Line 9 of the description says so. `--list-tasks` uses the same `rows` definition.
- The test is `tests/unit/test_regime_counters.py::RegimeCountersTest::test_a_tab_separated_task_counts_as_an_amendment`. It runs through the storage facade (`store()`), the path a live read takes, and expects tasks 3, amendments 2, results 1, questions 1. Its history holds:
  - a TASK with a tab between the kind and `v1`;
  - a TASK with two spaces and a tab;
  - a RESULT with a leading tab;
  - a PONG with two tabs and a trailing tab;
  - a PONG whose `\tstatus=question` is a backslash and a `t`, not a tab.
- Mutation proofs (validation §7): four mutants, all killed:
  - the single-space split, which is the code at `8576645c`;
  - no unescape;
  - empty tokens kept;
  - an unescape of `\t` alone.
- Size, against the INV-2 caps: 499 added lines outside tests (cap 500), 507 under tests (cap 1000), and 12 files outside `.orchestration` (cap 15). The fix edits two existing lines in place.
- The three P2 (the fill_sweep URL key, the record, the report claim): no change, per the ACCEPTANCE.
- Seen, not changed: `scripts/agent-stop-gate.sh:277` also splits each history body on one space (`split($3, w, " ")`). It is not in allowed_files and it is a Claude-boundary hook, so routing it is the orchestrator's call.

## PR-B (`d19ed9be`, `362a9c2b`)

- The branch is `tools/orchestrator-scripts-3`, fresh from `origin/main` at `c586f20d` (PR-A merged), per the orchestrator's PING of 22:34:32Z.
- The scope is a05 item 1's `acceptance-front-matter.py` and `orch-gate.sh` bullets, item 2's tests for them, and these records.
- The task copy is unchanged: it still hashes to `eaac8e4b…`, now from main (validation §9).

### `scripts/orchestrator/acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]`

- **head and pr.** `head` is `git -C <pr-worktree> rev-parse HEAD`. The script refuses (exit 1, nothing written) when the sweep JSON's `head_sha` differs from it. `pr` is the sweep JSON's own `pr`, never an argument.
- **The gate module.** The script imports `scripts/require-crit-review.py` from its own checkout (`git rev-parse --show-toplevel`) and keeps no second copy of a check. It uses that module's:
  - reader (`read_acceptance_record`: duplicate keys and non-finite numbers refused);
  - field checks (`record_field_errors`, identity triple first);
  - finding completeness (`audit_findings_errors`);
  - records search (`mistake_records`);
  - constants (`AUDIT_VERDICT`, `AUDIT_FINDING`, `S6_CLASS_LIMIT`, `RECORD_FORMAT`).
- **Writing.** The block is written with `sort_keys` and `indent=2`. Any refusal happens before the one write.
- **An existing record** is handled in one of three ways:
  - it starts with a `---` block the gate reader accepts: the block is replaced and the text after it kept;
  - it starts with `---` but the reader refuses it (not JSON, a duplicate key, YAML front matter): the script refuses and writes nothing;
  - it is a prose record: the block is prepended.
- **dispatch.** The `dispatch` list (and any other key) is carried over. An unknown key then fails the gate's field checks, as the gate would.
- **ledger.** Every row already present is kept. A `--ledger` row (`id<TAB>class`) is added only when its id is new; otherwise it prints `kept-ledger-row <id>`.
- **searches** is recomputed on every run by the gate's rule: each class with three or more rows, with the sorted basenames of the mistake records naming it, and `[]` records when none do.
- **audit_findings.** The audit summary is the `.last.md` that orch-audit.sh writes beside its receipt for this head, and its verdict is the gate's rule (the last non-blank line).
  - When that line is `Verdict: incorrect`, `--audit-dispositions` (`n<TAB>reason<TAB>evidence`, n kept as a string) is required, and the gate's completeness check runs on it.
  - Otherwise, including when no summary exists yet, the option is refused and `audit_findings` is `[]`.

  The record is written before the audit, which reads it, and rewritten after an incorrect audit.
- **Not done.** The S6 coverage of swept ids by the ledger (`acceptance_errors`) is not checked by this script. Item 1 names the field checks, and the gate checks coverage at the gate.

### `scripts/orchestrator/orch-gate.sh <task> <pr-worktree> <pr>`

This is the input `orch-gate.sh` (`.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/`) parameterised:

- The head is `git -C <pr-worktree> rev-parse HEAD`; the root comes from the script's own checkout, with no home-directory literal.
- `<pr>` must equal the sweep JSON's `pr` (jq). The input never used it.
- The six evidence files must exist before the review worktree moves.
- `make require-crit-review` runs in `.claude/worktrees/orchestrator-review` at the head. It gets `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE`, `PR_FEEDBACK_EVIDENCE`, `AGENT_REVIEWED=1`, `REVIEW_EVIDENCE` and `BASE=origin/main`, with `AUDIT_DISPOSITIONS` unset (the input passed the retired variable).
- A failed `cd` exits the subshell instead of gating another tree.
- The gate's status is the script's. Its whole output is shown, not the input's `tail -15`.
- The review worktree is restored with `clean -fdq -- .orchestration` and `checkout -qf --detach origin/main`. The input's `checkout -- .` fails on a tree with no tracked files, which the test fixture has.

### Tests (`tests/unit/test_orchestrator_tools.py`)

The `make` stub now also records its environment and working directory (`make-env`, `make-cwd`); `make.log` is unchanged. Item 2's PR-B rows map to these tests:

- `test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record` covers:
  - `head` is the fixture HEAD and `pr` the sweep's;
  - the `dispatch` list and the text after the block are kept;
  - a present ledger id is kept;
  - a class at three gets a `searches` entry from a fixture mistakes directory, and a class at one gets none;
  - the gate's own loader (`gate_block`, duplicate keys refused) and the gate module's `record_field_errors` pass on the output;
  - three refusals that write nothing: a row the field checks refuse, a sweep of another head, and a record with a duplicate key.
- `test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit` covers:
  - an incorrect summary without `--audit-dispositions` is refused;
  - with dispositions that skip finding 1, it is refused;
  - with the right row it is written (`n` is `"1"`);
  - a correct summary refuses the option and writes `[]`.
- `test_orch_gate_passes_the_gate_inputs_from_the_review_worktree`: the six variables reach the stub `make`, `ACCEPTANCE_EVIDENCE` included; `AUDIT_DISPOSITIONS` set by the caller does not; and make runs in the review worktree.
- `test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree`: a failing make gives exit 2, and the review worktree is clean at `origin/main`.
- `test_orch_gate_refuses_a_sweep_of_another_pr_before_the_review_worktree_moves`: exit 2, and make is never called.

### Mutation proofs and size

- Validation §9 lists 15 mutants, all killed: 9 in `acceptance-front-matter.py` and 6 in `orch-gate.sh`.
- The first run killed 14 of 15. AF6 raised a KeyError rather than an assertion failure. The G1 failure message also printed the captured environment, values included. `362a9c2b` makes both assertions plain: `.get`, and the sorted key names only.
- INV-2: 3 files outside `.orchestration`, 187 added lines outside tests and 151 under tests.

### PR-B fix round (`e30cbed0`): the Codex review of `0749e931` on PR #350

The Bot's one review (23:33:44Z code review, 23:40:27Z security review) left three P1 threads, all on `orch-gate.sh`. Each is fixed at its root:

| Thread | Finding | Disposition |
|---|---|---|
| 4265190252 (P1) | `make require-crit-review` at the PR head runs the head's own Makefile and gate, so a PR can pass itself | `fixed:e30cbed0` |
| 4265190259 (P1) | a head that commits an evidence path as a symlink makes `cp` write outside the review worktree | `fixed:e30cbed0` |
| 4265190267 (P1) | an inherited `CRIT_REVIEW=off` makes the gate return success unchecked | `fixed:e30cbed0` |

- **Thread 4265190252.** The wrapper no longer calls `make` in the review worktree. It runs this checkout's `scripts/require-crit-review.py` with the same inputs: `uv run --no-project python -I <root>/scripts/require-crit-review.py --base origin/main`, the review worktree as its working directory. The gate resolves its repository from the working directory (`git rev-parse --show-toplevel`), so it still reads the head's diff and the copied evidence. The validator it loads ships next to it in this checkout. Before anything moves, the wrapper refuses unless `scripts/require-crit-review.py` and `scripts/validate-agent-assets.py` here equal origin/main's (`git diff --quiet origin/main -- …`).
- **Thread 4265190259.** A head whose tree has any `120000` entry under `.orchestration` (`git ls-tree -r <head> -- .orchestration`) is refused before the review worktree moves. That covers `.orchestration` itself, a directory, or an evidence file. origin/main tracks none: the same command lists 0 entries at `c586f20d`.
- **Thread 4265190267.** `CRIT_REVIEW` and `CRIT_REVIEWED` are unset along with `AUDIT_DISPOSITIONS`. Those three, with the five inputs it sets, are every variable the gate reads (`os.environ` in `require-crit-review.py`).
- **Deviation from item 1's text.** The item says "passes exactly the gate's inputs … to `make require-crit-review`", and the threat row says it "calls make require-crit-review as it is". The fix keeps the inputs and the gate's own refusals, but it runs the trusted base copy of the gate instead of the head's `make` target. The orchestrator should judge this against the row.
- **Tests.** The four orch-gate tests now read:
  - `test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs`: the argv, the working directory, the five inputs, and none of `AUDIT_DISPOSITIONS`, `CRIT_REVIEW` or `CRIT_REVIEWED` although the caller sets all three;
  - `test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree`;
  - `test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves`;
  - `test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration`: the file the link points to stays unchanged.

  The `make` stub is back to its original form. The `uv` stub records its environment and fails on a flag file.
- **Mutation proofs.** Validation §10 lists 11 mutants, all killed: F1 to F5 for the fix, and G1 to G6 for the earlier orch-gate rows.
- **Size.** INV-2: 3 files outside `.orchestration`, 196 added lines outside tests and 174 under tests.
- **Locally,** `test_design_keydiff_names_the_changed_invariant` errors because the real `uv` it runs, offline, finds no PyYAML 6.0.3 in its cache (validation §10). Once the masker fetched PyYAML into the cache, the module passes offline, 36 tests OK (validation §10).

### PR-B revise 1 (`ced110dd`): amendment 1, after the audit of `f48593d6`

The task-level audit of `f48593d6` (PR #350 after `update-branch`) returned `incorrect`. The operator's decision A released one fix round, and amendment 1 (task hash `6b238e5a…`) names its two changes. This round makes those two changes and nothing else.

| Audit finding | Change |
|---|---|
| P1 at `orch-gate.sh:67`: `uv run` with the review worktree as its cwd reads the head's `.python-version`, and uv executes a path it names before the trusted gate runs | (a) the interpreter is resolved in this checkout and run directly |
| P2 at `orch-gate.sh:55`: a failing `mkdir` or `cp` after the head checkout leaves the review worktree at the head with partial evidence | (b) an EXIT trap set before the head checkout |

- **The exploit shape, run rather than recalled** (validation §12):
  - In a scratch directory whose `.python-version` reads `./pwn`, the real uv executed `pwn` for `uv python find` and again for `uv run --no-project python`. Each run left a marker, and each reported `Failed to inspect Python interpreter from provided path at ./pwn`.
  - `--no-project` does not stop it.
- **(a) The interpreter.**
  - `python="$(uv python find)" || refuse …` runs with this checkout as its cwd. It comes after the refusals and before the review worktree's clean check, which is the first command that touches the review worktree. The real root has no `.python-version`, `uv.toml` or `.venv`; there `uv python find` names the mise Python (validation §12).
  - The gate then runs as `"${python}" -I <root>/scripts/require-crit-review.py --base origin/main` in the review worktree. No uv runs with the head as its cwd.
  - The gate's own subprocess that runs Python (the `pr-feedback.py` collector) uses `sys.executable`, so it inherits the pinned interpreter.
- **(b) The trap.**
  - `trap 'git -C "${review}" clean -fdq -- .orchestration; git -C "${review}" checkout -qf --detach origin/main' EXIT` is set right after the clean check and before `git -C "${review}" checkout -q --detach "${head}"`. It replaces the two restore lines that ran after the gate.
  - The gate's subshell does not inherit it.
  - Under `set -e`, a failing restore in the trap ends the script non-zero even after a passing gate, so the wrapper fails closed (probe, validation §12).
  - The trap is an inline string, not a function: shellcheck 0.11.0 reports a trap-only function as SC2329 (info), and CI runs shellcheck at its default severity over `scripts/*.sh`, a git pathspec that also matches `scripts/orchestrator/` (`.github/workflows/test.yaml:310`). `scripts/update-agent-assets.sh` uses the same form.
  - Signals stay outside the row, as amendment 1 says.
- **Tests** (`tests/unit/test_orchestrator_tools.py`):
  - A `RUN` stub template records argv, cwd and environment, prints `<name>-output` and fails on `<name>-fails`. `uv` and the new interpreter stub `gate-python` use it.
  - As the probe shows the real uv does, the `uv` stub runs the executable that a `.python-version` in its cwd names.
  - `gate()` makes `uv python find` print the `gate-python` path. `gate(plant=True)` commits `./pwn` (mode 755, it touches `pwned`) and a `.python-version` naming it into the PR head.
  - The four existing orch-gate tests now assert on `gate-python` where they asserted on `uv`. The status test switches `gate-python-fails`.
  - `test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree`: `pwned` never appears; uv's only call is `python find`, with the root as its cwd; the gate runs under `gate-python`.
  - `test_orch_gate_restores_the_review_worktree_when_setup_fails`: a `cp` stub copies the first evidence file into the review worktree, then exits 1. The wrapper exits 1, `run_gate` finds the review worktree clean and at origin/main, and the gate never ran.
- **Mutation proofs.** Validation §12 lists 5 mutants, all killed. P1 is the pre-fix gate line: the PR's `pwn` runs. R1 is the pre-fix code without the trap.
- **Size.** INV-2: 3 files outside `.orchestration`, 198 added lines outside tests and 205 under tests.
- **Task copy.** `.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md` is the amended task, sha256 `6b238e5a958ed5124d997e129391a4e10cc2b61b7b9f57052e8b463b4f549f23`.
- **Observation for the orchestrator** (not changed, outside `allowed_files`):
  - The case: when `git show <base_sha>:scripts/pr-feedback.py` fails (`require-crit-review.py:604-608`), the gate runs the collector at `root / "scripts/pr-feedback.py"`.
  - Why it matters: the root comes from the gate's cwd. Under orch-gate.sh that cwd is the review worktree at the PR head, so the collector that runs is the head's own.
  - What limits it: `pr_base_errors` binds `base_sha` to GitHub's base first, so the fallback runs only when that commit or its collector is missing locally.

