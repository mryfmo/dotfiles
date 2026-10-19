# Learning triage: dotfiles-T133-regime-ci-a01

These are candidates only; nothing is promoted.

1. [memory:failure] Exit code 1 is ambiguous for a Python subprocess.
   - What happened: the checker exits 1 for FAIL, and Python also exits 1 on an unhandled exception. Treating `returncode in (0, 1)` as "the checker ran" let a crash pass as clean.
   - Remedy: a caller of a verdict-printing tool parses the verdict line and requires the matching exit code, and treats anything else as a violation.
   - This is the third time the fail-open class has reached this lineage (T133 verdict-audit-pool a01, then here). The mechanism is the re-plan's rule: a check is ok only on a positive check of parsed, validated input.
2. [memory:failure] A precheck record committed to the branch cannot name the commit that adds it, so a "precheck head equals the PR head" rule fails every PR that carries one.
   - The verdict.sh evidence-only ancestor rule applies here too: the precheck names an ancestor, and every path between it and the head is under the task's evidence directory.
   - Read the producer's real records (PR #411's precheck.json and result.txt) before writing the consumer's rule.
3. [memory:decision] A new workflow file also needs its entry in `tests/unit/test_workflow_security.py`'s `EXPECTED_PERMISSIONS` allowlist.
   - A task that adds a workflow should list that test file in allowed_files from the start; this task needed an amendment for it.
   - Run `uv run python -m unittest tests.unit.test_workflow_security` before the first push of any workflow change.
4. [memory:decision] `uv run --no-project` still reads `uv.toml`, `pyproject.toml` and `.python-version` from the working directory. In CI that runs on a pull request's checkout, pass `--no-config`.
5. [memory:failure] `git diff … -- <paths>` turns PR-controlled file names into pathspecs: `:(…)` magic, and `:!` exclusions. Diff without a pathspec and filter in code, or set `GIT_LITERAL_PATHSPECS=1`.
