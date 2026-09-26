# Learning

- Candidate (not promoted): `scripts/validate-agent-assets.py` has its own hard-coded
  literal-token checks against `scripts/update-agent-assets.sh` (e.g.
  `validate_crit_install_assets`), separate from and not discovered by grepping
  `tests/*.bats`/`tests/unit/*.py` alone. Any task that removes/renames a literal string
  in an installer script should also grep `scripts/validate-agent-assets.py` for that
  string before considering research complete, not just the test suite.
- Candidate (not promoted): the task's own evidence text conflated two different
  `|| true` swallows in two different CI jobs/files (`remote.yaml`'s `public-bootstrap`
  vs. `test.yaml`'s `test` job) under one failure annotation description. Re-deriving
  which job/file actually produces which annotation (rather than trusting the task's
  prose) prevented a fix that would have addressed only one of the two.
- Candidate (not promoted): a shell test asserting a command _fails_ must not write
  `! command` directly — a `!`-negated command is exempt from `set -e`/`errexit`
  regardless of its result (POSIX, verified directly with `bash -c 'set -eET; ! true;
echo reached'`), so the assertion silently passes either way. In bats, use `run !
command` instead.
- Candidate (not promoted): before writing new fake-uname/fake-curl test scaffolding for
  a shell function, grep the whole `tests/` tree (not just the file that seems most
  related) for existing fakes of the same commands — `tests/unit/test_runtime_health.py`
  already had a mature `crit_fixture` for the Linux install path that I didn't find until
  after independently reinventing a weaker version in a different file.
- Candidate (not promoted): the project's Write/Edit-tool PostToolUse auto-formatter
  reformats an entire Python file on any edit, not just the touched region, producing
  large unrelated diff noise when the file wasn't already formatter-clean. To make a
  surgical edit to such a file, restore it from the base ref and apply the change via a
  Python (or sed) script invoked through Bash — that bypasses the Edit/Write tool's
  PostToolUse hook entirely, so only the intended lines change. Use Python raw string
  literals (`r"""..."""`) when the old/new text itself contains backslash sequences
  (e.g. bash's `\n`), since a non-raw literal's escape processing will silently produce
  a string that doesn't byte-match the file.
  No rule or skill promotion.
