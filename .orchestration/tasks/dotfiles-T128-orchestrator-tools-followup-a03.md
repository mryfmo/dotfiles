---
format: 2
task_id: dotfiles-T128-orchestrator-tools-followup-a03
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/dispatch.sh
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/**
after: [dotfiles-T128-orchestrator-tools-followup-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/dispatch.sh in two places, the pre-send refusal of a TASK line whose task file fails the task-consistency check (item 1) and the bounded history reads before and after the send (item 2)
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_refuses_a_task_file_failing_the_checker"
  - control: "the history reads (item 2): both reads take the last BUS_READ_WINDOW rows (default 200) instead of the whole bus, so the count of identical rows and the read marker come from that window"
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_reads_a_bounded_history_window"
  - control: "the pre-send window file (item 1b): bus rows the recorder keeps between its two reads, under TMPDIR"
    disposition: "residual: created by mktemp with a random name and mode 0600, holding the four fields of each row (no marker, no record content), removed by an EXIT trap on every exit path, so a concurrent dispatch, another user or a failed run can neither read, replace nor keep it; the bounded-window test runs with TMPDIR under the temporary tree and asserts the directory holds no dispatch-window file after the run"
  - control: the PR edits tests/unit/test_orchestrator_tools.py (two new tests beside the 52, which stay as they are; the module's fake agmsg-dispatch and fake history.sh record their arguments and answer from files the case writes)
    disposition: "residual: the fakes record and answer, nothing else; the audit reads each case against items 1 and 2"
  - control: "the checker call (item 1): dispatch.sh runs scripts/orchestrator/task-consistency-check.py from its own checkout through uv with PyYAML, as presend.sh does today"
    disposition: "residual: the checker is the tracked script beside dispatch.sh, run with python -I, its file argument the hashed task file; a non-zero exit refuses the send and nothing reaches agmsg-dispatch; only a file whose front matter parses under a duplicate-refusing loader to a mapping with kind equal to review is exempt, since C2 requires an evidence directory a brief has no reason to own; a parse failure, a duplicate key and every other value are checked, so the exemption cannot be reached by a spelling, a decoy line or a malformed block"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: "the inputs of the checker invocation dispatch.sh makes through uv (the interpreter, the project, the configuration, the cache, the environment, the working directory, the checkout root)"
    disposition: "residual: every input is named by the script and none is read from the caller: --offline (no index: PyYAML comes from the pinned cache the validator recipes warm, T5; a cold cache is exit 2 with the make validate-agent-assets guidance), --python pinned to the interpreter resolved at the script's checkout root, --no-project, --no-config, UV_CACHE_DIR pinned under the orchestrator's real home, HOME set to that real home rather than inherited, env -i with PATH, HOME, UV_CACHE_DIR, LANG/LC_ALL and the AGMSG_* variables only, the import probe with -I, the cd to the checkout root resolved under the same environment (operator decision D-S2-374-5 after six caller-state findings, M-20261017-02, C-57); the test asserts identity, not absence: the exact argv and the exact environment key set the script passes to uv and to the probe (a new input source is impossible by construction), with the planted sources as one case; a further finding of the class is advisory under dotfiles-T128-orchestrator-tools-followup-a04"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
  - control: in-process effects
    disposition: "residual: the test module imports only the standard library and runs dispatch.sh as a bash subprocess with a fake agmsg-dispatch and a fake history.sh under AGMSG_SCRIPTS and PATH; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; dispatch.sh runs shasum, python3 and agmsg-dispatch from PATH and history.sh from AGMSG_SCRIPTS (else the fixed agmsg scripts path) as today, and the checker through the Makefile's UV_PYYAML form (uv run --offline --with pyyaml when the cache holds PyYAML, else uv run --with pyyaml through the index: the validator-offline pattern of PR #366); the tests' seams are PATH and AGMSG_SCRIPTS; a PR checkout as cwd chooses nothing because dispatch.sh resolves its root from its own location; after the fix round of D-P1-374 both uv commands run from the trusted script root (uv --directory <root>, the root from git rev-parse --show-toplevel of the script), so a caller cwd's .python-version or venv chooses nothing (the Bot's P1 4299651928 on PR #374)"
premises:
  - claim: 'dispatch.sh on origin/main reads the whole bus (BUS_READ_LIMIT default 100000) before and after a send'
    command: 'git show origin/main:scripts/orchestrator/dispatch.sh | /usr/bin/grep -c "BUS_READ_LIMIT:-100000"'
    output: |-
      1
  - claim: 'dispatch.sh on origin/main never runs the task-consistency check'
    command: 'git show origin/main:scripts/orchestrator/dispatch.sh | /usr/bin/grep -c "task-consistency-check"'
    output: |-
      0
  - claim: 'the tools test module on origin/main holds 52 tests, which this task keeps'
    command: 'git show origin/main:tests/unit/test_orchestrator_tools.py | /usr/bin/grep -c "def test_"'
    output: |-
      52
---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-followup-a03 — dispatch.sh refuses a task file that fails the checker and reads a bounded history window (corrections C-52 (2) and C-53 (2); the orchestrator-tools lineage's next owner task; a Claude seat)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. Two corrections of today name this task as the landing of their tool half. C-52 (M-20261015-04): a TASK line was sent whose task file failed `task-consistency-check.py` C2, because the pre-send chain discarded the checker's exit; the glue's `presend.sh` stops that chain today, and the repository's `dispatch.sh` must refuse such a line itself. C-53 (M-20261015-05): `dispatch.sh`'s pre-send read of the whole bus through `history.sh <team> "" 100000` took 56 minutes on a 1385-row team (upstream `history.sh` doubles the quotes of the whole slice with a bash 3.2 substitution: 4.1 s at 500 rows, 390 s at 1000); the glue's `dispatch-direct.sh` sends with a bounded read today, and `dispatch.sh` must bound its own reads.

## Change (round 2, 2026-10-15T21:59:03Z)

The Codex half's round 1 (on `ffb4a6db`): P1 exempting by a literal `kind: code` line was not fail-closed; only a front matter that says `kind: review` is exempt now, and the test adds the quoted and absent `kind` cases; P2 `uv run --offline` contradicted the index fallback; the uv form is the Makefile's `UV_PYYAML` probe.

## Change (round 3, 2026-10-15T22:03:29Z)

The Codex half's round 2 (on `bddbeaff`): P1 the first `kind:` line could be a decoy before a second one; the exemption now needs exactly one `kind:` line in a closed front matter with the value `review`, anything else is checked. P2 the test adds the duplicate-key case and asserts the checker call through the fake uv's log.

## Change (round 4, 2026-10-15T22:17:15Z)

The review seat's round 1 (on `7f2f4239`): P2-1 a count within a sliding window fails at the window's edge, so the recorder's pre-send read prints the newest row and the post-send read finds the new rows by position after that row's last occurrence, refusing when it left the window; P3-1 the failing-file case asserts the checker's own C2 line, printed by a stub checker beside the copied script (the module's style), the fake uv running python without PyYAML; P3-2 `presend.sh` keeps the premise replay and the mask check after the merge, and the `@exitcode 1` line names the checker's refusal.

## Change (round 5, 2026-10-15T22:19:28Z)

The Codex half's round 4 (on `bf59ae9d`): P2 an anchor matched by its last occurrence would mistake a new identical row of the same second for itself; the pre-send read now also prints the count `k` of rows identical to the newest row, the post-send read anchors on the `k`-th occurrence from the oldest, and the test adds the same-second collision case.

## Change (round 6, 2026-10-15T22:22:41Z)

The Codex half's round 5 (on `829ec8e9`): P1 the k-th-occurrence anchor shifts when an older identical row leaves the window; the recorder now aligns the whole post-send window with the whole pre-send window by the smallest shift, requires the newest new row to equal the sent line, and refuses every other case with the record unchanged, so a sent line is never recorded wrongly and never silently dropped; the test holds the eviction-plus-collision, same-second, left-the-window and no-new-row cases.

## Change (round 7, 2026-10-15T22:26:29Z)

The Codex half's round 6 (on `efd1ab96`): P1 a closed but unparsable front matter with one literal `kind: review` line would have been exempt; the exemption now requires a successful PyYAML parse under a duplicate-key-refusing loader yielding `review` for `kind`, every other outcome runs the checker, and the test adds the malformed case.

## Change (round 8, 2026-10-15T22:28:40Z)

The Codex half's round 7 (on `141d0113`): P1 the fake uv ran python without PyYAML, so the parse that identifies a brief could not run in the tests; the fake uv now records its argv and delegates to the real uv found later on PATH, PyYAML present as in production, the checker staying the stub beside the copied script.

## Change (round 9, 2026-10-15T22:30:15Z)

The Codex half's round 8 (on `01ad84d6`): P1 the alignment allowed both compared slices to be empty, so a pre-send window that left the post-send window entirely could align falsely; a nonempty overlap is now required (`j < m`, `e < n`) unless the pre-send window itself was empty, so the left-the-window case cannot align.

## Change (round 10, 2026-10-15T22:32:11Z)

The Codex half's round 9 (on `2785ac02`): P2 the pre-send window file under `$TMPDIR` had no collision-safe creation, no cleanup and no control row; it is now a private `mktemp` file (mode 0600) removed by an EXIT trap on every exit path, with its own threat row and a cleanup assertion in the test.

## Change (round 11, 2026-10-15T22:34:38Z)

The Codex half's round 10 (on `3f5caedf`): P1 the smallest fitting shift is not fail-closed on a periodic bus (a window of identical rows fits shift 1 as well as no change); every shift from no change to `m − 1` is now tried and exactly one may fit: a unique no-change fit refuses as no new row, zero or several fits refuse as ambiguous, and the test adds the periodic-bus case.

## Change (round 12, 2026-10-15T22:42:43Z)

The review seat's round 2 (on `296f35d9`): P2-1 the acceptance rule took only the newest new row for the send, while another seat's line can land newer before the post-send read; this send is now the last new row equal to the line, refused only when none is, and the test adds the newer-row case; P3-1 the fake uv runs the `UV_PYYAML` probe form itself and the sentence names the module's real-uv dependency as new.

## Goal

After the merge, `dispatch.sh` sends no TASK line whose task file fails the checker, and both of its history reads take the last `BUS_READ_WINDOW` rows, so a send on a 1385-row team completes within the agmsg-dispatch timeout.

## Files

1. `scripts/orchestrator/dispatch.sh`: (a) after the hash checks and before any read or send, for an AGMSG-TASK line, parse the front matter of the file `task_file=` names (the text between the first two `---` lines) with PyYAML through the same uv form as the checker below, under a `SafeLoader` whose mapping constructor refuses a duplicate key; the file is a review brief, and is not checked, only when that parse succeeds, yields a mapping, and the mapping's `kind` value is the string `review`; otherwise (a parse error, a duplicate key, no closed front matter, no `kind`, or any other value, a quoted `"code"` included) run `scripts/orchestrator/task-consistency-check.py --root <root> <file>` beside this script, through the Makefile's `UV_PYYAML` form (`uv run --offline --with pyyaml` when `uv run --offline --with pyyaml python -c 'import yaml'` succeeds, else `uv run --with pyyaml`, which reaches the index), as `python -I <checker>`, and on a non-zero exit print `dispatch: <file> fails the task-consistency check` with the checker's output and exit 1, nothing sent, so only a positively identified brief is exempt and a duplicate, malformed or unparsable front matter is checked, never exempted; (b) the two history reads (`bus()`) take the newest `BUS_READ_WINDOW` rows (default 200; a positive integer, else usage) instead of `BUS_READ_LIMIT`, and the cap refusal (`the history read is capped at …`) is removed; because a count within a sliding window fails at its edge and a single anchor row fails under eviction and same-second collisions, the recorder aligns the two windows as two views of one bus: the `check` mode writes the whole pre-send window (each row's timestamp, sender, recipient and text, never its marker, which flips when a row is read between the reads) to a private file dispatch.sh creates with `mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX"` (mode 0600, a fresh name, never a predictable path) before the first read and removes with an EXIT trap whatever the exit, so the window is neither overwritten by another process, readable by another user, nor left behind; the `append` mode reads that file; `append` tries every shift `j` from `0` (no new row) to `m − 1` and keeps those for which the post-send window without its `j` newest rows (a nonempty slice) equals, row for row in those four fields, the pre-send window without its `e` oldest rows, where `e` is the number of pre-send rows the post-send window no longer shows (`e = n + j − m` for `n` pre-send and `m` post-send rows, `0 ≤ e < n`); the alignment must be unique: exactly one `j` may fit, and a periodic bus (a window of identical rows, which fits `j = 0` and `j = 1` alike) therefore never aligns; when the unique fit is `j ≥ 1`, those `j` rows are the new rows, every one provably after the pre-send read, and this send is the last of them whose sender, recipient and text equal the line (another seat's RESULT or PONG may land newer before the post-send read, since `agmsg-dispatch` returns only after the recipient's `read_at`; a second identical new row can only be this sender's own second dispatch, recorded the same way), whose marker is recorded; when the unique fit is `j = 0` the recorder exits 1 with `dispatch: this send added no bus row`; when zero or several shifts fit it exits 1 with `dispatch: the post-send window does not align uniquely with the pre-send one; the line may be on the bus unrecorded; raise BUS_READ_WINDOW or check the bus`, and when the fit is unique but none of the new rows equals the line it exits 1 with `dispatch: no new row equals the line; the line may be on the bus unrecorded; check the bus`; the one exception is an empty pre-send window (`n = 0`), where `j = m` and the rule on the new rows is the same; in every refusal the record is unchanged, so the recorder never records a wrong row and never silently drops a sent one; a nonempty pre-send window that left the post-send window entirely therefore never aligns and is refused; the shdoc header, the `@env` line for `BUS_READ_WINDOW` and the `@exitcode 1` line (which also names the checker's refusal of item 1a) say so, and `BUS_READ_LIMIT` disappears from the script.
2. `tests/unit/test_orchestrator_tools.py`: two new tests beside the 52, in the module's dispatch style (the fake `agmsg-dispatch` and fake `history.sh` recording their arguments, a temporary repository with a task file and an acceptance record): `test_dispatch_refuses_a_task_file_failing_the_checker` (in the module's copy-and-stub style, `dispatch.sh` copied into a temporary `scripts/orchestrator/` beside a stub `task-consistency-check.py` that prints `<file>: FAIL` and `C2 allowed_files lacks .orchestration/<id>/**` and exits 1 for a file whose `allowed_files` lacks its own evidence directory, else `OK` and exit 0, and a fake `uv` first on PATH that appends its argv to the calls log and then runs the real `uv` (the next `uv` on PATH after its own directory) in the Makefile's `UV_PYYAML` probe form itself (`uv run --offline --with pyyaml` when `uv run --offline --with pyyaml python -c 'import yaml'` succeeds, else `uv run --with pyyaml`), so the front-matter parse of item 1a runs with PyYAML as in production and a sandboxed seat with a warm uv cache never reaches the index; this is a new dependency of the module, which today stubs `uv` and runs no real one, and the module's docstring says so; while the checker path dispatch.sh passes is the stub beside the copied script, and the log shows the checker path and the file: a task file whose `allowed_files` lacks its own evidence directory, kind code: exit 1, `fails the task-consistency check` and the checker's own line `C2 allowed_files lacks .orchestration/<id>/**` on stderr (the discriminating assertion: a checker dying on an import prints the first and not the second), the uv log holds `task-consistency-check.py` and the file, the fake agmsg-dispatch never called, the record unchanged; the same file with `kind: "code"` in quotes, with no `kind:` line, with `kind: review` followed by a second `kind: code` line (the duplicate key), and with a closed but unparsable front matter holding one literal `kind: review` line beside a line that is not YAML (`: broken`): refused likewise, each with the checker call logged; the same file with a single `kind: review` and no `allowed_files`: sent, the uv log holding no checker call) and `test_dispatch_reads_a_bounded_history_window` (the fake history.sh records a limit argument of 200 on both reads and answers the windows the case writes; with `BUS_READ_WINDOW=50` the argument is 50; the eviction-plus-collision case: a full pre-send window whose oldest row is identical to the line in sender, recipient and text and whose post-send window is the pre-send one shifted by that one row with the new row at the end, recorded once with the new row's marker; the same-second case: the newest pre-send row identical to the line down to the second, the post-send window ending with two such rows, recorded once with the second one's marker; the newer-row case: the post-send window ending with the line and then another seat's row, recorded once with the line's row's marker; the left-the-window case: a post-send window sharing no row with the pre-send one, exit 1 naming `BUS_READ_WINDOW`, the record unchanged; the no-new-row case: a post-send window equal to the pre-send one (distinct rows), exit 1 `added no bus row`, the record unchanged; and the periodic-bus case: a full window of rows identical in the four fields, unchanged after the send, exit 1 `does not align uniquely`, the record unchanged; after every case the temporary directory holds no `dispatch-window.*` file).

## Out of scope

`presend.sh` and `dispatch-direct.sh` (the orchestrator's glue): after this merge `dispatch-direct.sh` retires and `presend.sh` keeps running the premise replay and the mask check before a send (C-52's two other pre-send checks; only its checker step becomes redundant with item 1a), until a later task lands those two in the repository; upstream `history.sh` (D-history-upstream, the operator's); the other dispatch.sh checks (hash fields, the record block, the read marker form), which stay as they are.

## Check

`uv run python -m unittest tests/unit/test_orchestrator_tools.py -v` green (the 52 tests and the two new ones), pasted in the validation file with `shellcheck scripts/orchestrator/dispatch.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after 8b25f9ca; the tools a02 PR #368 is merged). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-orchestrator-tools-followup-a04`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-orchestrator-tools-followup-a04` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md>` and the evidence paths.

## Change (bot_rounds, 2026-10-16T06:21:47Z)

The Completion clause's `bot_rounds=1` becomes the template's `bot_rounds=2` form (the Bot's review at PR open and its re-review after the fix round): T13's amendment 6 after the Bot's P2 4290644781 on PR #371, applied to every undispatched task text right before its dispatch and re-confirmed Codex first (C-54). Nothing else changes from the pair-confirmed hash `5a741e63`.

## Change (threat row, 2026-10-16T22:07:03Z, after the RESULT)

The Codex Bot's P1 4299651928 on PR #374's head 57d3577c: uv run from the caller's cwd executes a caller-controlled `.python-version` or venv interpreter even with `--no-project`, which the environment threat row's claim that the cwd chooses nothing did not cover. Operator decision D-P1-374 A: the fix round runs uv from the trusted script root; the row now says so. The dispatched hash `b291ba85` stands (the branch's task copy is byte-identical to it by design); this row is the orchestrator's record, carried by the next boundary.

## Change (window algorithm, 2026-10-17T00:55:53Z, after the audit of ef74eaea)

The audit of PR #374's head ef74eaea (P2, specification): the bounded-window alignment as item 2 prescribes it considers evictions from an underfull window (with limit 200, two rows becoming three yields shifts 1 and 2 and a refusal), where no row can have been evicted; and timestamp-ordered history lets concurrent rows interleave inside the window (a false negative: a successful send left unrecorded). Both are the owner task `dotfiles-T128-orchestrator-tools-followup-a04`'s rows (advisory P2 of the final head); the algorithm the owner lands considers eviction only when the pre-window is full and aligns on the sent line's own row rather than the window's shift. The dispatched hash `b291ba85` stands.

## Change (complete inputs, 2026-10-17T01:39:50Z)

Operator decision D-S2-374-5 (A) after the sixth caller-state finding (the Bot's P1 4300738707: uv reads `$HOME/.config/uv/uv.toml`): the threat table gains the row above naming every input of the uv invocation, and the final round implements it. The dispatched hash `b291ba85` stands.

## Change (re-plan, 2026-10-17T01:53:20Z)

The operator's correction at 2026-10-17T01:53Z: S1's three-repeat rule means re-examining the specification, the design, the implementation and the verification, not a sixth single-source patch. Re-plan: (specification) the checker invocation's inputs are an open set while uv may resolve or fetch, so the specification names a closed set and forbids the network (`--offline`); (design) PyYAML comes from the orchestrator-owned cache the validator recipes already warm (T5), never from an index, so a configuration or HOME redirect has nothing to redirect; (implementation) the complete-inputs row above; (verification) the test asserts the exact argv and environment the script passes (identity), not the absence of known sources. The supplement to the final round carries this; the rounds 2 to 5 stay recorded as M-20261017-04's evidence.

