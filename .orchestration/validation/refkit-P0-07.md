# refkit-P0-07 validation

## Bookkeeping commit (before the functional change)

```text
$ git commit -m "chore(orchestration): record refkit P0-01/P1/P2-A/P2-B worker artifacts" ...
[feat/references-kit-v4 f560b48] chore(orchestration): record refkit P0-01/P1/P2-A/P2-B worker artifacts
 20 files changed, 3841 insertions(+)
```

## `make validate-agent-assets` (now passes, `.venv` still present and untouched)

```text
$ command ls -d references/examples/flowapprove_core/.venv
references/examples/flowapprove_core/.venv

$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
```

## `make unit-test`

```text
$ make unit-test
[... 395 tests ...]
test_secret_scan_allows_exact_placeholder_tokens (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... /tmp/validate-agent-assets-test-3ym_agh1 is not a git repository (or git is unavailable); validate_no_obvious_secrets is scanning every file on disk instead
ok
test_secret_scan_checks_docs_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_git_visible_files (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_git_visible_files) ... ok
test_secret_scan_checks_utf16_bom_text (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_ignores_gitignored_files (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_ignores_gitignored_files) ... ok
test_secret_scan_rejects_placeholder_with_suffix (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
[...]
----------------------------------------------------------------------
Ran 395 tests in 28.215s

OK (skipped=1)
```

(The stderr line printed above during `test_secret_scan_allows_exact_placeholder_tokens`
is the new fallback-path message the task asked for; that one test doesn't wrap the
call in `contextlib.redirect_stderr`, unlike the tests expecting `SystemExit`, so it
surfaces in the runner's own captured output — harmless, the test still passes.)

## Ruff format/check on the two changed files

```text
$ uvx ruff format --force-exclude scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
1 file reformatted, 1 file left unchanged

$ git diff --stat scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
 scripts/validate-agent-assets.py         | 38 +++++++++++++++++++++++++++++++-
 tests/unit/test_validate_agent_assets.py | 20 +++++++++++++++++
 2 files changed, 57 insertions(+), 1 deletion(-)
```

`uvx ruff check --force-exclude` on both files (no filters) also reports pre-existing
findings unrelated to this task's diff (`EXE001` shebang-without-executable-bit on both
files' line 1, `SIM102`/`C401`/`UP022` elsewhere in `validate-agent-assets.py`, `FLY002`
in `test_validate_agent_assets.py`) — none on lines this task touched; not fixed (out of
scope).

## `git ls-files --others --exclude-standard | head`

```text
$ git ls-files --others --exclude-standard | head
(no output — nothing untracked-and-not-ignored in the worktree right now)
```

## Functional commit

```text
$ git add scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py
$ git status --short
M  scripts/validate-agent-assets.py
M  tests/unit/test_validate_agent_assets.py
```

## `git show --stat HEAD~1 HEAD` (after the functional commit)

```text
$ git show --stat HEAD~1 HEAD
commit f560b483aa8853e16967ab35e6312df9095c217f
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 20:26:05 2026 +0900

    chore(orchestration): record refkit P0-01/P1/P2-A/P2-B worker artifacts
    
    These .orchestration/{reports,validation,sandboxes,learning,autoskill/runs}
    files were written when each task completed but never staged/committed
    alongside their functional commits. Recording them now so every accepted
    task has its evidence in history.
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .orchestration/autoskill/runs/refkit-P0-01.md |    5 +
 .orchestration/autoskill/runs/refkit-P1.md    |    4 +
 .orchestration/autoskill/runs/refkit-P2-A.md  |    5 +
 .orchestration/autoskill/runs/refkit-P2-B.md  |    4 +
 .orchestration/learning/refkit-P0-01.md       |   13 +
 .orchestration/learning/refkit-P1.md          |   22 +
 .orchestration/learning/refkit-P2-A.md        |   16 +
 .orchestration/learning/refkit-P2-B.md        |   24 +
 .orchestration/reports/refkit-P0-01.md        |  100 ++
 .orchestration/reports/refkit-P1.md           |  109 ++
 .orchestration/reports/refkit-P2-A.md         |  115 ++
 .orchestration/reports/refkit-P2-B.md         |  178 +++
 .orchestration/sandboxes/refkit-P0-01.md      |    7 +
 .orchestration/sandboxes/refkit-P1.md         |   17 +
 .orchestration/sandboxes/refkit-P2-A.md       |   10 +
 .orchestration/sandboxes/refkit-P2-B.md       |   10 +
 .orchestration/validation/refkit-P0-01.md     |  541 +++++++++
 .orchestration/validation/refkit-P1.md        |  726 ++++++++++++
 .orchestration/validation/refkit-P2-A.md      |  477 ++++++++
 .orchestration/validation/refkit-P2-B.md      | 1458 +++++++++++++++++++++++++
 20 files changed, 3841 insertions(+)

commit 61a19895c1d7bfe81a0192530b6708c0386b07f4
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 20:30:39 2026 +0900

    fix(validate-agent-assets): scan only git-visible files for secrets
    
    validate_no_obvious_secrets() walked every file under ROOT (skipping only
    .git/site/__pycache__), so any gitignored virtualenv or tool cache anywhere
    under the repo (e.g. references/examples/flowapprove_core/.venv, created by
    refkit-P1) could trip a false positive on a vendored library file, making
    make validate-agent-assets fail locally even though a clean checkout (CI)
    never has that directory. Scan git -C ROOT ls-files --cached --others
    --exclude-standard instead — exactly the files git would let get committed
    — falling back to the old rglob walk (with a stderr note) when ROOT isn't a
    git repository or git is unavailable.
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .orchestration/autoskill/runs/refkit-P0-07.md |   3 +
 .orchestration/learning/refkit-P0-07.md       |  24 ++++++
 .orchestration/reports/refkit-P0-07.md        | 103 ++++++++++++++++++++++++++
 .orchestration/sandboxes/refkit-P0-07.md      |   6 ++
 .orchestration/validation/refkit-P0-07.md     |  92 +++++++++++++++++++++++
 scripts/validate-agent-assets.py              |  38 +++++++++-
 tests/unit/test_validate_agent_assets.py      |  20 +++++
 7 files changed, 285 insertions(+), 1 deletion(-)
```

## CompactionDB memory-add

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] validate-agent-assets secret scan uses git ls-files (tracked + untracked-not-ignored)"
a9f9095f-a5a3-407b-bbb3-9d95e82bd518
```

Memory ID: `a9f9095f-a5a3-407b-bbb3-9d95e82bd518`
