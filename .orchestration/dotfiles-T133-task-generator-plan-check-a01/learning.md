---
task_id: dotfiles-T133-task-generator-plan-check-a01
round: 1
---

# Learning

Task-local triage; nothing promoted.

- C14 is environment- and time-sensitive. Under its PATH `<root>/bin:/usr/bin:/bin`, macOS's BSD `wc -l` pads counts (`       0`) while the pasted outputs were written with an unpadded `wc`, `uv` and `codex` are not on that PATH, and a premise describes write-time state that later merges change (`grep -c '^worker_cap:'` was 0 before #408 and is 1 after). On the sixteen current T133 files C1 to C13 and C15 are clean; before amendment 1 C14 differed on ten, after its whitespace collapse and tool-absent warning on five, and on seven once #413 merged an hour later, each a premise the repository moved past. A generator therefore runs premises through the checker's own `rerun` so its pasted outputs reproduce, and C14 is best read at dispatch, not at acceptance. Applies to P1-12's follow-ups and to dispatch.sh, which runs the checker.
- A tool missing at the head of a pipeline does not exit 127 under `set -o pipefail`: `codex exec --help | grep -c x` exits with grep's 1. The tool-absent warning reads bash's own `bash: line N: <name>: command not found` line instead. Applies to any check that classifies a shell exit.
- A test that parses a tool's output as findings (`test_task_checkers.py` reads every indented line as `  C<n> `) breaks on any other line in the same stream; notes and warnings belong on stderr. Applies to any checker whose stdout an exact-set test reads.
- Adding checks to a checker whose existing test asserts exact finding sets turns that test red even when the old checks are unchanged; the existing module (`tests/unit/test_task_checkers.py`, PR #413's) has to move with the checker. Applies to any extension of a checker with exact-set tests.
- A test module run by `make unit-test` has no PyYAML: fixtures are written as YAML text and read back through `uv run --with pyyaml`.
- Shared refs: a seat's `origin/main` moves when another checkout of the same repository fetches; caps and diffs are read three-dot, against the merge base.
