# refkit-P0-06 learning

## Reusable

- **Formatter hooks that receive explicit file paths must run from each file's own
  repository root, not the hook's inherited cwd.** Two independent tools share the same
  failure mode: prettier only reads `.prettierignore` relative to its own `cwd` (not the
  target file's location), and ruff only honors `exclude`/`extend-exclude` for explicit
  CLI paths (as opposed to directory arguments) when `--force-exclude` is also passed.
  A repo-root config file (`.prettierignore`, `ruff.toml`) is therefore silently
  ineffective for any hook/CI step that formats specific files from a different
  directory. Fix pattern: group files by `git -C <parent> rev-parse --show-toplevel`,
  run each formatter once per group with `cwd=<group root>` and paths relative to that
  root, and add `--force-exclude` to ruff invocations.
- **Testing a hook that calls `subprocess.run` recursively for its own bookkeeping
  (here: `git rev-parse` to discover a file's repo root) alongside calls you want to
  fake (formatters) needs a monkeypatch that discriminates by argv[0]** — pass `git`
  calls through to the real `subprocess.run` (captured under a different name _before_
  patching, to avoid infinite recursion when the mock and the module-level name are the
  same object) and fake everything else with a `CompletedProcess(returncode=0)`.
- **A validator that walks `ROOT.rglob("*")` for a naive secret-pattern scan needs to
  skip virtualenv directories explicitly** — `scripts/validate-agent-assets.py`'s
  `validate_no_obvious_secrets()` only excludes `.git`/`site`/`__pycache__` path parts,
  so any real Python venv anywhere under the repo (even gitignored, even outside the
  scanned tool's own scope) will false-positive on library files containing hex color
  codes or similar secret-shaped strings (hit here: pygments' `nord.py` theme). Not
  fixed in this task (out of `allowed_files` scope) — flagged for the orchestrator.

## Not promoted (task-specific, not reusable)

- The exact `references/examples/flowapprove_core/.venv` cleanup/no-cleanup decision is
  specific to this worktree's accumulated state this session, not a general rule.

## Rule candidates

None proposed — the two reusable points above are already narrow, project-specific
facts (this repo's specific hook and this repo's specific validator), not general
process rules.
