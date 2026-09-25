# refkit-P0-05 acceptance record

status: accepted (2026-09-23T10:5xZ)
reviewer: claude-remediation-dot

## Verified independently (in dotfiles-w2 at bd3b6a6)
- `.prettierignore` (`references/`) and `ruff.toml` (`extend-exclude = ["references"]`, `force-exclude = true`).
- Decisive prettier check: with the ignore file, `prettier@2 --check references/01_ADVERSARIAL_REVIEW.md` reports no matched issues and `-l` lists nothing; with `--ignore-path /dev/null` the same file is flagged `[warn]`. So the hook's explicit-path invocation is now ignored for the kit.
- `uvx ruff format --check references/tools/kit_lint.py` → `No Python files found under the given path(s)`.
- Deviation (`force-exclude = true`) is necessary and correctly justified: ruff does not apply `exclude`/`extend-exclude` to explicitly passed paths unless force-exclude is set, and the hook always passes explicit paths. validate-agent-assets ok, unit tests 392 OK.

cost: n/a
