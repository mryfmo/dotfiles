# AGMSG-TASK refkit-P0-06: make the managed formatter hook honour repository exclusions regardless of cwd

## Why
`home/dot_claude/hooks/executable_format-edited-files.py` (deployed as `~/.claude/hooks/format-edited-files.py`) runs `uvx ruff format` / `ruff check --fix` / `ty check` on edited `.py` and `npx prettier@2 --write` on edited `.md` with explicit file paths and **the hook's inherited cwd**. Verified on 2026-09-23: prettier 2 reads `.prettierignore` only from its cwd, so with cwd = `references/` or `/tmp` the repository-root `.prettierignore` is not applied and the kit files are rewritten; `uvx ruff format --check <abs path>` from `/tmp` also reports the kit file as reformattable despite root `ruff.toml` (`extend-exclude` + `force-exclude = true`). refkit-P0-05's root config is therefore only effective when the session's shell cwd happens to be the repository root.

## Change (repository source; deployment to `$HOME` happens later via the user's `chezmoi apply`, not in this task)
Edit `home/dot_claude/hooks/executable_format-edited-files.py`:
1. Group the collected files by repository root: for each existing path run `git -C <parent> rev-parse --show-toplevel` (no shell); files outside any git repository fall back to their parent directory as the group key.
2. Run each formatter once per group with `cwd=<group root>` and file paths made **relative to that root** (so prettier's ignore matching and ruff's config discovery behave as they do from the root).
3. Prettier: pass `--ignore-path <root>/.prettierignore` when that file exists (explicit, cwd-independent); otherwise omit the flag.
4. Ruff: append `--force-exclude` to both `ruff format` and `ruff check --fix` invocations (documented ruff behaviour: explicit CLI paths bypass `exclude`/`extend-exclude` unless force-exclude is set — cite the ruff docs page you fetched in the report; if the official docs page is unreachable, quote `uvx ruff format --help`). Keep `ty check` unchanged apart from cwd.
5. Keep the shdoc-style/module docstring current and describe the grouping behaviour.
6. Tests: add `tests/unit/test_format_edited_files.py` (unittest, like the neighbours) that (a) builds a temp git repo with `.prettierignore` containing `kit/` and a file `kit/a.md` plus `other/b.md`, (b) monkeypatches `subprocess.run` to record `(argv, cwd)`, (c) feeds a hook payload with absolute paths, and asserts: one prettier call per repo root with `cwd=root`, relative paths, `--ignore-path` pointing at the root ignore file; ruff calls include `--force-exclude`; a file outside any repo is grouped by its parent. No real ruff/prettier execution in tests.
7. `make unit-test` and `make validate-agent-assets` pass; `scripts/check-agent-runtime.py`/`validate-agent-assets.py` references to the hook still hold (they only check presence/hash of managed assets — confirm and say so).
8. Commit: `fix(claude-hooks): run formatters from each file's repository root and force ruff exclusions`.

## Scope (allowed_files)
`home/dot_claude/hooks/executable_format-edited-files.py`, `tests/unit/test_format_edited_files.py` (new), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P0-06.md`.

## Forbidden
push; pr-create; `chezmoi apply`; writes under `$HOME`; changes under `references/`; changing which formatters run or their versions.

## Validation file
verbatim: `make unit-test` (with the new test visible), `make validate-agent-assets`, a manual demonstration from a non-root cwd: `cd /tmp && printf '%s' '{"tool_input":{"file_path":"<abs path to a scratch copy of references/01_ADVERSARIAL_REVIEW.md inside your worktree>"}}' | python3 home/dot_claude/hooks/executable_format-edited-files.py` followed by `git status --short references/` showing no change (this worktree must have `.prettierignore`/`ruff.toml` at its root — they are on branch feat/references-kit-v4-p3; if your branch lacks them, cherry-pick bd3b6a6 first and say so), `git show --stat HEAD`, contextdb memory-add (`[memory:decision] format-edited-files hook groups files by git toplevel, runs with cwd=root, prettier --ignore-path, ruff --force-exclude`).

## Editing discipline
Bash/python writes; the hook itself may reformat your edits to this very file — verify `git diff` is only the intended change (ruff format on a file that already conforms is a no-op; if it reflows, keep the reflowed result only if `ruff format --check` on the original would have flagged it, and say so).

max_turns=25
