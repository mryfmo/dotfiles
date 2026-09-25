# AGMSG-TASK refkit-P0-05: protect `references/` from the editor post-write formatters

## Why
The user-level Claude Code hook `~/.claude/hooks/format-edited-files.py` runs `uvx ruff format` + `ruff check --fix` on every edited `.py` and `npx prettier@2 --write` on every edited `.md`. On the kit it rewrites whole files (table realignment, spaces between CJK and Latin/digits, Python reflow), which (a) buries intended hunks under noise (refkit-P3 round 1: 800+ noise lines), and (b) can break the kit's own template↔sample exact-match checks. The kit has its own formatting conventions (`03_CONVENTIONS.md` §7) and must not be reformatted by repo-external tools.

## Change (repo root, this worktree)
1. Create `.prettierignore` at the repository root containing:
```
# The documentation kit under references/ has its own Markdown conventions (references/03_CONVENTIONS.md §7);
# editor formatters must not rewrite it.
references/
```
2. Create `ruff.toml` at the repository root containing only:
```toml
# Keep repository-wide ruff defaults; exclude the vendored documentation kit, which is
# validated by its own tools (references/tools/kit_lint.py, run_examples.py).
extend-exclude = ["references"]
```
   Before adding, confirm no other ruff configuration exists (`pyproject.toml`, `ruff.toml`, `.ruff.toml`, `setup.cfg`) at the root; if one exists, add `extend-exclude` there instead and do not create a second file.
3. Prove it works: in the worktree, run `npx prettier@2 --check references/00_README.md` (expect it to be ignored / no changes reported) and `uvx ruff format --check references/tools/kit_lint.py` (expect "0 files" / excluded). Also run the real hook once against a scratch copy? — not necessary; the two direct checks are the mechanism the hook uses.
4. Make sure `make validate-agent-assets` and `make unit-test` still pass (a root ruff.toml must not change results for `scripts/` and `tests/`; if any test asserts on ruff config discovery, report it).
5. Commit: `chore(references): exclude the documentation kit from prettier and ruff formatting`.

## Scope (allowed_files)
`.prettierignore`, `ruff.toml` (or the existing ruff config file), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/refkit-P0-05.md`.

## Forbidden
push; pr-create; any change under `references/`; changes to `~/.claude/hooks/*`; touching main.

## Validation file
verbatim outputs of steps 3–4, `git show --stat HEAD`, contextdb memory-add (`[memory:decision] references/ excluded from prettier/ruff via root .prettierignore and ruff.toml`).

max_turns=15
