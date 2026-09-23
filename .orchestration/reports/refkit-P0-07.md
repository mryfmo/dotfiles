# refkit-P0-07 report

Status: ready_for_review

## Result

`scripts/validate-agent-assets.py::validate_no_obvious_secrets()` now scans exactly the
files `git` would let get committed from `ROOT` — tracked files plus untracked files not
covered by `.gitignore` (`git -C ROOT ls-files -z --cached --others --exclude-standard`)
— instead of every file on disk. `make validate-agent-assets` now passes locally with
`references/examples/flowapprove_core/.venv` still present (left untouched, per this
task's forbidden actions), since that directory is gitignored
(`.gitignore:34:references/examples/flowapprove_core/.venv/`) and no longer walked.

## Files changed, with reasons

- `scripts/validate-agent-assets.py`:
  - New `git_visible_files(root) -> list[Path] | None`: runs the `git ls-files` command
    above (argv list, no shell) and returns the decoded, NUL-split file list; returns
    `None` when the subprocess itself can't start (`OSError`, i.e. `git` isn't on
    `PATH`) or exits non-zero (root isn't a git repository).
  - `validate_no_obvious_secrets()`: calls `git_visible_files(ROOT)` first; on `None`
    prints one stderr line naming `ROOT` and falls back to the original
    `list(ROOT.rglob("*"))` walk (unchanged behavior otherwise: same `.git`/`site`/
    `__pycache__` exclusion, same CompactionDB dummy-fixture allowlist, same
    placeholder/secret-pattern logic).
  - `validate_no_removed_claude_skill()` (a few lines above, same `ROOT.rglob("*")`
    pattern) is untouched — this task's scope named only
    `validate_no_obvious_secrets()`; flagged below for the orchestrator since it has
    the same class of false-positive exposure.
- `tests/unit/test_validate_agent_assets.py`: added `subprocess` import and
  `init_git_repo()` (`git init -q` in the test's temp dir — no commit needed; `git
ls-files --cached` reads the index, and `--others --exclude-standard` needs no
  staging at all) plus two tests: `test_secret_scan_ignores_gitignored_files` (a
  `.gitignore`-covered file with a fake secret pattern next to a clean visible file →
  `validate_no_obvious_secrets()` returns normally) and
  `test_secret_scan_checks_git_visible_files` (the same fake secret in a file that
  isn't gitignored → raises `SystemExit`, same as before this change). The five
  pre-existing `test_secret_scan_*` tests run in a plain (non-git) temp dir, so they
  now exercise the fallback path instead — no test needed changing.

## Item 3 (optional hook change) — skipped, already true

The task asked, optionally, to make a formatter's non-zero exit count as a hook failure
"only if the formatter actually processed at least one file." Checked
`home/dot_claude/hooks/executable_format-edited-files.py`'s `run_commands` (rewritten in
refkit-P0-06): it already returns `status = 0` immediately when a suffix group's file
list is empty, and only invokes a command (and folds its return code into `status`)
once there is at least one file in that group's argument list. There is no code path
where a non-zero `status` can result from zero files being passed to a command, so this
requirement already holds without any change. No edit made to that file.

## Bookkeeping commit (before the functional commit)

`f560b48` — `chore(orchestration): record refkit P0-01/P1/P2-A/P2-B worker artifacts`
(20 files, all previously-untracked `.orchestration/**/refkit-{P0-01,P1,P2-A,P2-B}.md`
artifacts from earlier tasks this session).

## Validation

`make validate-agent-assets`: `agent asset validation ok` (was failing before this
change, with the `.venv` present and untouched).

`make unit-test`: 395 tests (up from 393), `OK (skipped=1)` — includes the two new
secret-scan tests.

Both changed files are `ruff format`/`ruff check --force-exclude` clean for the lines
this task touched; `ruff check` (no filters) also reports several pre-existing findings
elsewhere in `scripts/validate-agent-assets.py` and `tests/unit/test_validate_agent_assets.py`
(`EXE001`, `SIM102`, `C401`, `UP022`, `FLY002`) — none on lines this task added or
touched, none fixed (out of scope).

Exact command output in the validation file.

## Commit

`2beb7cd` — `fix(validate-agent-assets): scan only git-visible files for secrets`
(amended once, to add the `git show --stat HEAD~1 HEAD` output to the validation file
after the first commit). Bookkeeping commit: `f560b48`.

## CompactionDB

`[memory:decision] validate-agent-assets secret scan uses git ls-files (tracked +
untracked-not-ignored)`

Memory ID: `a9f9095f-a5a3-407b-bbb3-9d95e82bd518`

## Editing discipline

Both files were edited via Bash-invoked Python scripts (`pathlib.Path.read_text()`/
`.write_text()`, each replacement asserted unique before applying), never the Edit/Write
tools. Ran `uvx ruff format` afterward (no `--fix`, so only whitespace/line-wrapping
changed) on just the one new long line in `scripts/validate-agent-assets.py`; confirmed
via `git diff` that only the intended new/changed lines were touched.

## Notes for the orchestrator

- `validate_no_removed_claude_skill()` has the identical `ROOT.rglob("*")` pattern (same
  file, a few lines above `validate_no_obvious_secrets`) and would have the same
  gitignored-content blind spot in reverse (it could flag or miss content depending on
  what's on disk vs. tracked) — not touched here since it's outside this task's named
  scope, but worth a follow-up task if it matters.

cost: n/a
