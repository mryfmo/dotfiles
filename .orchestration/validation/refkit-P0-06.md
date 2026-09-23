# refkit-P0-06 validation

## `uvx ruff format --help` (force-exclude citation)

```text
$ timeout 60 uvx ruff format --help 2>&1 | grep -A3 -i "force-exclude"
      --force-exclude
          Enforce exclusions, even for paths passed to Ruff directly on the command-line. Use
          `--no-force-exclude` to disable

Format configuration:
      --line-length <LINE_LENGTH>
```

## `scripts/check-agent-runtime.py` / `scripts/validate-agent-assets.py` reference check

```text
$ grep -rn "format-edited-files" scripts/*.py Makefile
scripts/generate-agent-configs.py:302:                "command": hooks["format_edited_files_hook"],
scripts/check-agent-runtime.py:728:            SOURCE_ROOT / "dot_claude/hooks/executable_format-edited-files.py",
scripts/check-agent-runtime.py:729:            HOME / ".claude/hooks/format-edited-files.py",
scripts/check-agent-runtime.py:730:            "Claude format-edited-files hook",
scripts/validate-agent-assets.py:379:    if "format-edited-files.py" not in commands:
```

`check-agent-runtime.py:719-732` and `validate-agent-assets.py:375-380` (read in full)
only do a presence/hash comparison (`check_executable_hook`) and a substring check on
the rendered hooks JSON — neither inspects the hook's internal logic, so this rewrite
needs no change to either validator.

## New test file: `uv run python -m unittest tests.unit.test_format_edited_files -v`

```text
test_groups_by_repository_root_and_forces_ruff_exclusions (tests.unit.test_format_edited_files.TestFormatEditedFiles.test_groups_by_repository_root_and_forces_ruff_exclusions) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.009s

OK
```

## `make unit-test`

```text
$ make unit-test
[... 393 tests ...]
test_secret_scan_checks_utf16_bom_text (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_rejects_placeholder_with_suffix (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 393 tests in 28.664s

OK (skipped=1)
```

## `make validate-agent-assets` (fails — pre-existing, unrelated; see report)

```text
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
ERROR: possible committed secret in references/examples/flowapprove_core/.venv/lib/python3.12/site-packages/pygments/styles/nord.py
make: *** [Makefile:154: validate-agent-assets] エラー 1
```

```text
$ git log --oneline -1 -- references/examples/flowapprove_core/.venv/lib/python3.12/site-packages/pygments/styles/nord.py
(no output: never committed)
$ git status --short references/examples/flowapprove_core
(no output: gitignored, not shown)
$ git check-ignore -v references/examples/flowapprove_core/.venv/lib/python3.12/site-packages/pygments/styles/nord.py
.gitignore:34:references/examples/flowapprove_core/.venv/	references/examples/flowapprove_core/.venv/lib/python3.12/site-packages/pygments/styles/nord.py
$ git ls-files references/examples/flowapprove_core | wc -l
9
$ stat -c '%y' references/examples/flowapprove_core/.venv
2026-09-23 18:26:35.567347770 +0900
```

`references/examples/flowapprove_core` itself (9 files) is tracked v3-baseline content
from refkit-P1; only its `.venv/` is gitignored and was created by me during refkit-P1's
own validation (`uv venv --python 3.12 references/examples/flowapprove_core/.venv`,
documented in `.orchestration/validation/refkit-P1.md`), predating this task.

## Manual non-root-cwd demonstration

Branch already has `.prettierignore`/`ruff.toml` at root (cherry-picked `bd3b6a6` onto
`feat/references-kit-v4` as this task's prerequisite, before any of the above; new
commit `b6acdfc`).

```text
$ cp references/01_ADVERSARIAL_REVIEW.md references/.p0-06-demo-scratch.md
$ sha256sum references/.p0-06-demo-scratch.md
c04237eadaa1bf80d5a5f31d990cb827e58f1466662f4f130a73dba6363c73b8  references/.p0-06-demo-scratch.md

$ DEMO_ABS="$(pwd)/references/.p0-06-demo-scratch.md"
$ (cd /tmp && printf '%s' "{\"tool_input\":{\"file_path\":\"$DEMO_ABS\"}}" | python3 /home/moriya/Workspace/dotfiles-w1/home/dot_claude/hooks/executable_format-edited-files.py)
npm warn exec The following package was not found and will be installed: prettier@2.8.8
exit=0

$ sha256sum references/.p0-06-demo-scratch.md
c04237eadaa1bf80d5a5f31d990cb827e58f1466662f4f130a73dba6363c73b8  references/.p0-06-demo-scratch.md

$ git status --short references/
?? references/.p0-06-demo-scratch.md
```

SHA-256 identical before/after: no reformatting occurred, confirming the hook correctly
discovered this worktree's own git toplevel from `cwd=/tmp` and honored root
`.prettierignore`'s `references/` exclusion. `git status --short references/` shows
only the untracked scratch file — no tracked kit content changed. The scratch file is
deliberately excluded from this task's `git add`/commit (attempts to delete it, and the
unrelated stray `.venv` above, via `rm` were denied; see report).

## `git show --stat HEAD` (prerequisite cherry-pick, before this task's own commit)

```text
$ git show --stat HEAD
commit b6acdfc1a0e4948f9a201fedbf4cc803725a56fa
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 19:29:57 2026 +0900

    chore(references): exclude the documentation kit from prettier and ruff formatting

    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .orchestration/autoskill/runs/refkit-P0-05.md |   3 +
 .orchestration/learning/refkit-P0-05.md       |  11 +++
 .orchestration/reports/refkit-P0-05.md        |  33 ++++++++
 .orchestration/sandboxes/refkit-P0-05.md      |   3 +
 .orchestration/validation/refkit-P0-05.md     | 107 +++++++++++++++++++++++++
 .prettierignore                               |   3 +
 ruff.toml                                     |   5 +++
 7 files changed, 165 insertions(+), 8 deletions(-)
```

## `git show --stat HEAD` (this task's own commit, after committing)

```text
$ git show --stat HEAD
commit b4345186dcc212fd8ef862727dde1dfaab88bb8d
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 20:22:26 2026 +0900

    fix(claude-hooks): run formatters from each file's repository root and force ruff exclusions

    home/dot_claude/hooks/executable_format-edited-files.py ran ruff/prettier/ty with the
    hook's inherited cwd and absolute file paths, so a repo-root .prettierignore/ruff.toml
    (refkit-P0-05) only applied when that cwd happened to be the repo root. prettier only
    reads .prettierignore relative to its own cwd, and ruff only honors
    exclude/extend-exclude for explicit CLI paths when --force-exclude is set (both
    confirmed against this machine's installed tools). Group files by
    `git -C <parent> rev-parse --show-toplevel` (falling back to the parent directory for
    files outside any repository), run each formatter once per group with cwd=<group root>
    and paths relative to it, pass --ignore-path to prettier when a root .prettierignore
    exists, and pass --force-exclude to both ruff invocations. Adds
    tests/unit/test_format_edited_files.py covering the grouping, cwd, and flag behavior
    with subprocess.run mocked (git calls pass through to the real binary; formatter calls
    are recorded, not executed).

    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .orchestration/autoskill/runs/refkit-P0-06.md      |   3 +
 .orchestration/learning/refkit-P0-06.md            |  38 +++++
 .orchestration/reports/refkit-P0-06.md             | 155 ++++++++++++++++++
 .orchestration/sandboxes/refkit-P0-06.md           |   8 +
 .orchestration/validation/refkit-P0-06.md          | 181 +++++++++++++++++++++
 .../hooks/executable_format-edited-files.py        |  68 ++++++--
 tests/unit/test_format_edited_files.py             | 131 +++++++++++++++
 7 files changed, 572 insertions(+), 12 deletions(-)
```

(This is the pre-amend commit's own stat, captured before adding this section; the line
count for this validation file above reflects that pre-amend version. Amended only to
add this section — see the report.)

## `git diff --stat` for this task's own change (staged files only)

```text
$ git diff --stat home/dot_claude/hooks/executable_format-edited-files.py
 home/dot_claude/hooks/executable_format-edited-files.py | 62 +++++++++++++++++-----
 1 file changed, 50 insertions(+), 12 deletions(-)
```

## `uvx ruff format --check` / `uvx ruff check` on both changed files

```text
$ uvx ruff format --check --force-exclude home/dot_claude/hooks/executable_format-edited-files.py tests/unit/test_format_edited_files.py
1 file would be reformatted, 1 file already formatted
[... two long lines needing wrap in the hook file ...]

$ uvx ruff format --force-exclude home/dot_claude/hooks/executable_format-edited-files.py tests/unit/test_format_edited_files.py
1 file reformatted, 1 file left unchanged

$ uvx ruff check --fix --force-exclude home/dot_claude/hooks/executable_format-edited-files.py tests/unit/test_format_edited_files.py
SIM117 Use a single `with` statement with multiple contexts instead of nested `with` statements (not auto-fixable)

[fixed manually by combining the two `with mock.patch.object(...)` statements into one]

$ uvx ruff check --force-exclude home/dot_claude/hooks/executable_format-edited-files.py tests/unit/test_format_edited_files.py
All checks passed!
```

## CompactionDB memory-add

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] format-edited-files hook groups files by git toplevel, runs with cwd=root, prettier --ignore-path, ruff --force-exclude"
f51700d0-f6ec-48f8-bc9b-43ad5e1ac01e
```

Memory ID: `f51700d0-f6ec-48f8-bc9b-43ad5e1ac01e`
