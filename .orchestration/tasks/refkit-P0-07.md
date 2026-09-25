# AGMSG-TASK refkit-P0-07: make the secret scanner honour .gitignore, and commit the orchestration bookkeeping

## Why
`scripts/validate-agent-assets.py::validate_no_obvious_secrets()` walks `ROOT.rglob("*")` (skipping only `.git`/`site`/`__pycache__`), so any gitignored virtualenv or tool cache under the repo (e.g. `references/examples/flowapprove_core/.venv`, created by P1 as documented) trips a false positive (`pygments/styles/nord.py`) and `make validate-agent-assets` fails locally although CI (clean checkout) passes. The essential fix is to scan exactly what git would commit.

## Change
1. Replace the `ROOT.rglob("*")` walk in `validate_no_obvious_secrets()` with the set of paths from `git -C ROOT ls-files -z --cached --others --exclude-standard` (tracked + untracked-but-not-ignored), decoded as NUL-separated, keeping the existing `.git`/`site`/`__pycache__` and CompactionDB fixture exclusions. If `git` is unavailable or ROOT is not a repository, fall back to the current rglob behaviour and print one stderr line saying so.
2. Add a unit test in `tests/unit/` (follow the neighbours' style; `test_validate_agent_assets.py` already exists — extend it): a temp repo where a gitignored file contains a fake secret pattern and a tracked file does not → validation passes; then the same fake secret in a tracked file → validation fails.
3. Optional (do it if it is a one-line change): in `home/dot_claude/hooks/executable_format-edited-files.py`, treat a formatter's non-zero exit as a hook failure only if the formatter actually processed at least one file — NOT required; skip if it needs more than trivial logic, and say so.
4. Bookkeeping: in this worktree, `git add` and commit all currently untracked `.orchestration/**/refkit-*.md` artifacts (P0-01, P1, P2-A, P2-B) as one `chore(orchestration): record refkit P0-01/P1/P2-A/P2-B worker artifacts` commit BEFORE your functional commit.
5. Functional commit: `fix(validate-agent-assets): scan only git-visible files for secrets`.

## Scope (allowed_files)
`scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`, optionally `home/dot_claude/hooks/executable_format-edited-files.py` + its test, `.orchestration/**`.

## Forbidden
push; pr-create; chezmoi apply; home writes; changes under `references/`; deleting the example venv (leave it; the scanner must cope).

## Validation file
verbatim `make validate-agent-assets` (must pass now with the venv present), `make unit-test`, `git ls-files --others --exclude-standard | head`, `git show --stat HEAD~1 HEAD`, contextdb memory-add (`[memory:decision] validate-agent-assets secret scan uses git ls-files (tracked + untracked-not-ignored)`).

max_turns=20
