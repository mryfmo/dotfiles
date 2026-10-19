---
task_id: dotfiles-T133-hold-playbook-a01
seat: claude-standard-dot-a011
branch: tools/hold-playbook-a01
base: b22a5580 (origin/main at the branch point, PR #423's merge)
code_head: a6c073e5 (5e719af3 the task copy; 6a72398c the tests, red; f76db928 the script; a6c073e5 the worker review's fixes)
task_sha256: e33f0aa1927956b7e5d17fe06987d611e8ed50ebb3f09f11bff7f9293b9e3d1c
---

# Report: dotfiles-T133-hold-playbook-a01

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. After a single-command `git fetch origin main`, the branch `tools/hold-playbook-a01` was created with `--no-track` from `origin/main` `b22a5580`. The previous branch, `tools/regime-ci-followup-a01` (PR #425, pending integration), was pushed and clean before the switch.
- Task file: `e33f0aa1…`, copied byte-identical to `.orchestration/dotfiles-T133-hold-playbook-a01/task.md` (`5e719af3`). The task-consistency check passes (validation §1).
- The orchestrator note governs item 1. `.orchestration/learning/classes.yaml` is the orchestrator's record, outside this task's `allowed_files`, so this branch neither adds nor edits it. Item 1 is read as the format the script consumes: a top-level `classes:` mapping of slug to `remedy:` (a string, `unknown` when no procedure is known) and `blast_radius:` (a list of globs). The pinned-vocabulary check is the script's `--check-vocabulary <classes.yaml> <mistakes-dir>` mode, tested with fixtures only. No test reads the real `.orchestration/learning/` tree.

## What the script does

`scripts/orchestrator/hold-playbook.sh <task> <class>` is a bash wrapper with shdoc comments. It checks the task id against `^[A-Za-z0-9][A-Za-z0-9._-]*$` before any path is built. Then it runs one embedded Python helper through `uv run --no-project --with pyyaml python -I -`, which receives the record values only as argv and stdin text. Record text is never seen by a shell.

- **Inputs.** The helper reads `.orchestration/learning/classes.yaml` and the first YAML front-matter document of `.orchestration/tasks/<task>.md`, both with `yaml.safe_load`. The front matter is the lines between the file's first `---` line and the next. The root is the checkout the script lives in.
- **Refusals (exit 2, nothing written):**
  - a class absent from `classes.yaml`, with the supplied slug named, or a class argument holding a tab, newline or carriage return;
  - a class entry without a one-line remedy string (a newline could forge the replan's own sections), or without a `blast_radius` list of globs, each free of tab, newline and carriage return;
  - a task without an `allowed_files` list;
  - a decision ledger that does not start with its six-column header;
  - an unreadable file.
- **The replan.** `.orchestration/tasks/<task>-replan.md` is created with `O_CREAT | O_EXCL`. Any existing entry, including a directory or a dangling link, exits 4 before the ledger is touched. The replan holds:
  - the cause class and the remedy (`unknown` is spelled out as such);
  - every blast-radius glob, with the `allowed_files` entries that cover it or `outside allowed_files`;
  - a Completion sentence with `<fill: the observable result>`, `<fill: test selectors>` and `<fill: evidence paths>`;
  - the four-field line `re-plan: specification — <fill>; design — <fill>; implementation — <fill>; verification — <fill>`, the keys of the `replans` object in `.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a04.md`.
- **Exit 0.** Every glob is covered, including the empty blast radius of an unknown remedy. Exit 0 establishes scope coverage only.
- **Exit 3.** Some glob is uncovered. Exactly one row is appended to `.orchestration/decisions.tsv` with Python's csv writer (tab-delimited, quoted as the ledger's existing rows are). Its six fields:
  - `id`: `D-<task>-replan`;
  - `when`: the UTC time to the second;
  - `what`: names the uncovered globs;
  - `why`: names the class;
  - `basis`: `hold-playbook`;
  - `result`: `pending`. No default and no deadline are written.
  - If the append fails, the helper removes the replan it just created, so a rerun is not refused with exit 4 while no decision was recorded.
- **Never:** it never edits the source task, an existing replan, an acceptance record or the learning records, and it never dispatches.

### Coverage of a glob

A blast-radius glob is covered by an `allowed_files` entry when every path the glob can name, existing or not, matches the entry. Matching follows `regime-ci.py`'s `allowed()`, which the regime job enforces: a trailing `/**` takes any path under its literal prefix, and elsewhere `*` and `?` stay within one path segment.

`covers()` decides this on the two patterns themselves, never by expanding files. Each token of the glob must be absorbed by an entry token whose set holds it:

- a literal, by the same literal;
- one literal other than `/`, or one `?`, by `?`;
- any run of literals other than `/`, `?`s and `*`s, by `*`;
- everything that remains, a trailing `/**` included, by a trailing `/**`.

This is sound. It is not complete: for example, `?*` under `*?` reads as outside. That limit errs toward a pending decision, and the code carries a `shortcut:` comment saying so.

Validation §5 shows that two wrong ways of comparing scope turn the whole-glob test red:

- matching the pattern string as a filename (`fnmatch`);
- expanding only the files that exist.

## Files requirements and their tests

All selectors are in `tests/unit/test_hold_playbook.py::HoldPlaybookTests`. Each was red at `6a72398c`, before the script existed, and is green at the code head (validation §3). §5 names the wrong implementations each one catches: 15 mutations, each red, with an unmutated green baseline.

| Requirement | Test | Wrong implementation it catches (§5) |
| --- | --- | --- |
| Item 1: the pinned vocabulary (the orchestrator note's `--check-vocabulary` mode); exit 2 lists every missing slug | `test_vocabulary_covers_mistake_classes` | missing classes not reported |
| Item 1: `remedy: unknown` and `blast_radius: []` reported, coverage exit | `test_known_class_without_remedy_is_reported` | an unknown remedy not reported |
| Item 2: a replan per class, with the remedy, scope, Completion placeholders and four `re-plan:` fields; the source task unchanged | `test_three_classes_expand_into_replans` (`colored-json-parse`, `concurrent-ff-clobber`, `records-form`) | coverage by existing files only |
| Item 2: an uncovered glob appends one pending six-field row with the UTC time, existing rows kept, no default | `test_uncovered_scope_appends_pending_decision` | no decision row; a default in the row; local time in the row (red where the local zone is not UTC) |
| Item 2: an unknown class exits 2, names the slug, and writes nothing; so does a class key holding a tab | `test_unknown_class_exits_2` | an unknown class not refused; a class with a tab accepted |
| Item 2: an existing destination exits 4, kept; a repeated out-of-scope run appends no second row; a dangling link is not followed | `test_existing_replan_exits_4` | an existing replan overwritten |
| Item 2: an invalid task id exits 2 before any path | `test_invalid_task_id_is_refused` | the task id not checked |
| Item 2: coverage of the whole glob (an exact scope, a scope under an allowed directory glob, broader scopes, and an entry `*` or `?` never taking a `/`) | `test_scope_comparison_covers_the_whole_glob` | coverage by the pattern string as a filename; coverage by existing files only; an entry `*` taking a `/`; an entry `?` taking a `/` |
| Item 2: record text stays text, and a multi-line remedy is refused | `test_record_text_is_never_executed` | record text run by a shell; a multi-line remedy accepted |

## Class-source attribution and counts

This branch adds no class entry: the orchestrator seeded `classes.yaml` (untracked in the main checkout at this run) and attributes each entry with its `records:` list. The three expansion classes in the tests are fixtures; the task names them, and their remedies and globs were written for the tests.

The read-only smoke run of the completed script against the main checkout counted 80 `M-*.md` records and 97 distinct class slugs, all present in the seeded file (validation §8, exit 0). The orchestrator runs that command again at acceptance.

## The Check

- `uv run --no-project --with pyyaml python -m unittest tests.unit.test_hold_playbook -v`: 9 tests OK at the code head, with no warning (§3). Red at `6a72398c`: 9 errors (§3).
- `shellcheck scripts/orchestrator/hold-playbook.sh`: exit 0 (§4).
- `shfmt -d scripts/orchestrator/hold-playbook.sh`: exit 1. This is an inherited mismatch between the Check text and the repository's style (§4).
  - `.editorconfig` sets `indent_size = 4` and `space_redirects = true` for `*.sh` but no `indent_style`. shfmt v3.14.1 then wants tabs, so the bare command flags every four-space script, for example `orch-audit.sh`, `dispatch.sh` and `ci-rerun.sh` on the unchanged base.
  - With the repository's own flags, `shfmt --indent 4 --space-redirects --diff` (`make format`), the script is clean.
  - I did not reformat the script with tabs, which would break the repository style. I report the mismatch instead.
- `make format`: exit 2 (§7). Its whole-tree shfmt step flags 12 files, all unchanged from `b22a5580`. ruff (66 files) and prettier are clean, and `ruff check` passes on the new test module.
- Caps (§6): 231 changed lines outside `tests/` and `.orchestration/` (cap 350), and 243 under `tests/` (cap 400).
- No local Bats ran. Every script execution in the tests uses a temporary fixture tree.

## Threat table

Every row is `residual`, and the change keeps each control:

- The helper reads records only through `yaml.safe_load` and `read_text`. It writes only the replan and, conditionally, one ledger row. It runs no command derived from records, which the literal-data test and the shell mutation in §5 check.
- The tests copy the script into temporary trees.
- No workflow or environment configuration changes.
- `hold-playbook.sh` is the only new script.

## Changed files

- `scripts/orchestrator/hold-playbook.sh` (new);
- `tests/unit/test_hold_playbook.py` (new);
- `.orchestration/dotfiles-T133-hold-playbook-a01/**`: `task.md`, then this report, `validation.md`, `sandbox.md`, `learning.md` and the worker review files.

## Evidence, review, cost

- Evidence in `.orchestration/dotfiles-T133-hold-playbook-a01/`.
- Worker review: `dotfiles-T133-hold-playbook-a01-worker-crit.json` and `dotfiles-T133-hold-playbook-a01-worker-review-receipt.md`. One read-only round by a fresh subagent, on `origin/main..f76db928`, returned `Verdict: correct`. It found no P0 to P2, and its brute-force check found no case where `covers()` reports covered and `allowed()` refuses a path. Its seven P3 are fixed in `a6c073e5`, the one worker-side fix round, which counts toward INV-6.
- For the orchestrator: the dispatched `threat_table` row for `tests/unit/test_hold_playbook.py` says the vocabulary test reads the real learning tree. The orchestrator note and the fixture-only test supersede that. The text is the byte-identical task copy, so it is unchanged here.
- precheck: pending-411 (`scripts/orchestrator/result-precheck.sh` is not on main).
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
