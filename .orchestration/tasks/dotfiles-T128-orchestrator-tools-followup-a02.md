---
format: 2
task_id: dotfiles-T128-orchestrator-tools-followup-a02
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/boundary.sh
  - scripts/orchestrator/fill_sweep.py
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T128-orchestrator-tools-followup-a02/**
after: [dotfiles-T128-orchestrator-tools-followup-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/boundary.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/fill_sweep.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits tests/unit/test_orchestrator_tools.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-followup-a02/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the pair's receipts name this file's hash"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-followup-a02/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: the worker's untrusted claims; acceptance re-checks each against the diff, CI and the test output"
  - control: in-process effects
    disposition: "residual: the tests import fill_sweep.py into their process (the declared change, read line by line by the orchestrator and the audit) and run boundary.sh as a subprocess with real git in a temporary repository; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts resolve exactly these host binaries, a closed list the tests stub or the audit replays from the diff: git, gh, make, codex, uv and the interpreter it resolves as `python` under `uv run --no-project` (the attached inputs' form; the first slice's `python3 -I` is the other accepted form, and the implementation uses one of the two, never a bare `python` outside uv), shasum, jq (regime-counters.sh's ledger parsing), env, bash, agmsg-dispatch, the agmsg history.sh, and the coreutils awk, cat, cp, cut, date, dirname, find, grep, head, ls, mkdir, mktemp, mv, rm, rmdir, sed, sort, tail, tee, tr, wc, xargs; a script that needs another binary adds it to this row by amendment before it is written as the SKILL's own commands do; fill_sweep.py and acceptance-front-matter.py read and write the acceptance record's JSON block with the standard library's json module, as amendment 1 of dotfiles-T128-gate-evidence-a03 defines it (plan 013 A′); two scripts use PyYAML through uv run --no-project --with pyyaml (the uv cache; a network fetch only when the cache is empty): design-keydiff.py for the design file's front matter, and boundary.sh for scripts/validate-agent-assets.py --mask-secrets and make validate-agent-assets, the repository's own masker and validator; neither is the gate (PR #329 thread 4250238721 is about the gate); replay.sh runs the given command with env -i PATH=/usr/bin:/bin bash -c; the tests stub every host binary on PATH"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the first owner task of the lineage is merged (PR #361, f0faa33a) and its task file is on origin/main (this task runs after it)"
    command: "git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a01.md && echo present"
    output: |-
      present
  - claim: "the lineage's acceptance record with the owner section is on origin/main; the four rows this task implements that are not yet there (the audits of 2e77a33, 39c186a and e9404a6) are read from the attached copy, whose sha256 is a fact of this file"
    command: "git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md | /usr/bin/grep -c '^## Owned by dotfiles-T128-orchestrator-tools-followup-a01'"
    output: |-
      1
  - claim: "the section on origin/main holds the six f48593d audit rows this task reads as closed (landed or record-side) in the attached copy"
    command: "git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md | /usr/bin/grep -c '^audit:f48593d:'"
    output: |-
      6

---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-followup-a02 — the three open defects of the tools lineage after PR #361 (the second owner task of the T718 tools lineage; plan 020 step 1, C-32's owner-first pattern; the two P1 of operator decision A first)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. The lineage record `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md` carries the owner section `## Owned by dotfiles-T128-orchestrator-tools-followup-a01` with 37 rows (36 ids, `audit:8576645:2` listed twice): PR #361 (the first owner task, merged f0faa33a) implemented 15 of them, PR #350 and PR #346 had already landed 7 (the three Bot threads `fixed:e30cbed0`, orch-gate.sh's interpreter pin, EXIT trap and `-I -P` run, the counters' whitespace split), and 10 are record-side findings naming no file of the lineage's `allowed_files`; each of those 32 ids carries a closure line beneath its row in the record (the review seat's round-1 reading of this task, `dotfiles-T128-orchestrator-tools-followup-a02-review-a01.md`). Four rows remain, three defects: the two P1 the audit of PR #361's head 2e77a33 left, which operator decision A (2026-10-15 04:1xZ, AskUserQuestion) sent to this task instead of a fix round, and the `evidence-command-null-url` pair. Because those four rows were added after boundary (15), the task reads them from the attached copy of the record, `.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/a05-record.md` (sha256 `b8e90801c5a20fbdd97f9b06a298e320e1bbabf3288cff6881a5b5dfdc5e6f43`, masked), and the three audit receipts not yet on `origin/main` are attached beside it (`dotfiles-T128-orchestrator-tools-followup-a01-audit-2e77a33.last.md`, `dotfiles-T128-validator-offline-a01-audit-39c186a.last.md`, `dotfiles-T128-chain-github-scripts-followup-a01-audit-e9404a6.last.md`; sha256 prefixes `fc57b78e…`, `80939ee0…`, `9b4f1098…`).

## What to do

1. The owned rows, four ids and three defects, implemented in this order: `audit:2e77a33:1` (P1, class `pathspec-globbing`): `boundary.sh` passes each deleted name of its status listing to `git rm` as a pathspec (line 54 on `origin/main`), so a deleted name holding a glob character acts as a pattern; pass each name literally with the `:(literal)` pathspec magic or `git --literal-pathspecs rm` (the `--pathspec-from-file` form stops nothing by itself: each element stays a pathspec with its magic; it works only with `:(literal)` inside the list), with one test whose deleted names hold `*` and `[` beside the names they would match; `audit:2e77a33:2` (P1, class `collision-key-order`): `fill_sweep.py` builds its collision set from the raw url fragments (lines 62-63) while the lookup (line 81) uses the stripped key, so two fragments that differ before the `discussion_r` strip and share the key after it (a review fragment `discussion_r123` and a status fragment `123`) are not seen as a collision and one TSV row `123` fills both items; build the set from the stripped keys the lookup uses, with one test whose two fragments differ and whose stripped keys collide (`discussion_r123` and `123`, one TSV row `123`): both items stay gaps, or the shared-key path takes over; `audit:e9404a6:2` and `audit:39c186a:2` (P3, class `evidence-command-null-url`, one defect): the evidence template writes `select(.url == "None")` for a status item whose url is JSON null (line 74); select the status item by `source` and `check` instead, keeping the gate's masked-body comparison intact, with one test on a null-url status item. Each row's finding text is in the attached audit receipts; one test per defect named in report.md. A row whose finding the worker judges wrong is not skipped silently: report.md states the reading and the orchestrator decides at acceptance.
2. Nothing else changes: no file outside the three, no behaviour the rows do not name.

## Validation

- `uv run python -m unittest tests/unit/test_orchestrator_tools.py -v` in the validation file, with the three new tests named; `shellcheck scripts/orchestrator/boundary.sh`.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

A fresh branch from `origin/main` (after 907522c2), one new PR. The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on the PR's own change whose fix stays within these files and is small is fixed in a revise round the orchestrator sends with a `check=` before the gate (correction C-50), so integration readiness is reached only after that round; any other P2 is advisory and recorded under the same heading in `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md` for the lineage's next owner task. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-orchestrator-tools-followup-a02/task.md>` and the evidence paths.

## Change (round 2, 2026-10-15 07:4xZ)

The review seat's round 1 (P1, three P3; the Codex half confirmed round 1): 17 of the 21 rows had no code work (7 landed in PRs #346 and #350, 10 record-side), so the record now closes each of them beneath its row, the attached copy is re-exported and re-hashed, the task names the four remaining ids (three defects) with the audit's lines, `allowed_files` narrows to the three files the defects live in (the twelve other file rows dropped), premise 3 reads the tracked record on `origin/main`, and the pathspec row names `git rm` of each deleted name.

## Change (round 3, 2026-10-15 08:0xZ)

The review seat's round 2 (two P2, one P3) and the Codex half's round 2 (P1, P2): the pathspec remedy names `:(literal)` magic or `git --literal-pathspecs` (the from-file form alone stops nothing); the collision test is the audit's case (two fragments that differ before the `discussion_r` strip and collide after it); the Completion clause no longer says every P2 is advisory while C-50 sends a small in-scope P2 to a revise round; the intro counts 37 rows as 36 ids with one listed twice.
