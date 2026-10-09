# T121 validation

`git fetch origin feat/rolling-tools-single-update` (exit 0):

```text
From https://github.com/mryfmo/dotfiles
 * branch              feat/rolling-tools-single-update -> FETCH_HEAD
```

`git switch -c feat/rolling-tools-single-update --no-track origin/feat/rolling-tools-single-update` (exit 128):

```text
fatal: a branch named 'feat/rolling-tools-single-update' already exists
```

`git rev-parse origin/feat/rolling-tools-single-update feat/rolling-tools-single-update` (exit 0):

```text
b621af77a52d62c2cda4404a9877e53e86ad23f2
b621af77a52d62c2cda4404a9877e53e86ad23f2
```

`git switch feat/rolling-tools-single-update` (exit 128):

```text
fatal: 'feat/rolling-tools-single-update' is already used by worktree at '~/Workspace/dotfiles/.claude/worktrees/worker-c'
```

The absolute home directory in this diagnostic is normalized to `~` for artifact
hygiene. The test, diff-stat and push steps were not reached.

## Amendment 1 implementation

`git fetch origin feat/rolling-tools-single-update && git switch -c t121/hook-hint origin/feat/rolling-tools-single-update --no-track` (exit 0; home paths normalized):

```text
From https://github.com/mryfmo/dotfiles
 * branch              feat/rolling-tools-single-update -> FETCH_HEAD
Switched to a new branch 't121/hook-hint'
error: Unable to create '~/Workspace/dotfiles/.git/packed-refs.lock': Operation not permitted
error: Unable to create '~/Workspace/dotfiles/.git/packed-refs.lock': Operation not permitted
```

`git branch --show-current && git rev-parse HEAD` before editing (exit 0):

```text
t121/hook-hint
b621af77a52d62c2cda4404a9877e53e86ad23f2
```

Initial `uv run` failed on the sandbox-external default cache (exit 2; home paths normalized):

```text
error: Failed to initialize cache at `~/.cache/uv`
  cause: failed to open file `~/.cache/uv/sdists-v9/.git`: Operation not permitted (os error 1)
```

Test-first validation with the new assertion before changing the source:
`set -o pipefail; UV_CACHE_DIR=/private/tmp/uv-dotfiles-t121 uv run python -m unittest tests.unit.test_format_edited_files_hook 2>&1 | tail -12` (exit 1; home paths normalized):

```text
FAIL: test_a_missing_formatter_is_reported_without_a_traceback (tests.unit.test_format_edited_files_hook.FormatEditedFilesHookTest.test_a_missing_formatter_is_reported_without_a_traceback)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-d/tests/unit/test_format_edited_files_hook.py", line 72, in test_a_missing_formatter_is_reported_without_a_traceback
    self.assertIn("ruff is not installed; run `make update` (it installs every declared mise tool)", result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'ruff is not installed; run `make update` (it installs every declared mise tool)' not found in 'ruff is not installed; run `mise install --locked`\n'

----------------------------------------------------------------------
Ran 2 tests in 0.721s

FAILED (failures=1)
```

After the source change (exit 0):

```text
Ran 2 tests in 0.684s

OK
```

Ruff format requested wrapping the new test assertion. After that formatting change,
`set -o pipefail; UV_CACHE_DIR=/private/tmp/uv-dotfiles-t121 uv run python -m unittest tests.unit.test_format_edited_files_hook 2>&1 | tail -3` (exit 0):

```text
Ran 2 tests in 0.726s

OK
```

`ruff format --check home/dot_claude/hooks/executable_format-edited-files.py tests/unit/test_format_edited_files_hook.py && git diff --check && git diff --stat` (exit 0):

```text
2 files already formatted
 home/dot_claude/hooks/executable_format-edited-files.py | 8 +++++---
 tests/unit/test_format_edited_files_hook.py             | 4 +++-
 2 files changed, 8 insertions(+), 4 deletions(-)
```

`ruff check home/dot_claude/hooks/executable_format-edited-files.py tests/unit/test_format_edited_files_hook.py` and parent-source check `git show HEAD:home/dot_claude/hooks/executable_format-edited-files.py | ruff check --stdin-filename home/dot_claude/hooks/executable_format-edited-files.py -` each returned 1 with this existing finding:

```text
F401 [*] `shlex` imported but unused
  --> home/dot_claude/hooks/executable_format-edited-files.py:14:8
   |
13 | import json
14 | import shlex
   |        ^^^^^
15 | import subprocess
16 | import sys
   |
help: Remove unused import: `shlex`
   |
13 | import json
   - import shlex
14 | import subprocess
   |

Found 1 error.
[*] 1 fixable with the `--fix` option.
```

`make require-crit-review` was attempted before Amendment 2 (exit 2):

```text
Native agent review required before completion.
- review-sensitive path changed: .orchestration/reports/dotfiles-T121-claude-hook-install-hint-a01.md
- broad diff touches 5 files
Use the active agent's review path, not a browser by default:
- Codex: retrieve Crit comments/status data, review it inside the task, then address findings.
- Claude Code: retrieve Crit comments/status data, review it inside the task, then address findings.
- Use browser Crit review only when the user explicitly asks for Crit web UI or Crit data is unavailable.
Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.
For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file.
Evidence must contain at least one resolved record; for a finding-free review, add and resolve one review-scope approval record.
This local evidence is process evidence, not reviewer authentication.
Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`.
After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.
make: *** [require-crit-review] Error 1
```

`crit status --json` (exit 0; home paths normalized):

```json
{
  "branch": "t121/hook-hint",
  "daemon": {
    "running": false
  },
  "review_file": "~/.crit/reviews/db66f3784cb1/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
```

`crit comments --all --json <reported review file>` (exit 1; home paths normalized):

```text
stat ~/.crit/reviews/db66f3784cb1/review.json: no such file or directory
```

Independent read-only subagent `/root/t121_review` confirmed the final commit and returned:

```text
Approved; no findings. High confidence: `Makefile:65,80` reaches `scripts/upgrade-tools.sh:300`, which performs an unrestricted `mise install --yes`. Hook exit status and formatter execution remain unchanged; the test still checks exit code 1 and absence of a traceback. The unused `shlex` import at hook line 14 predates this change.

Reviewed the initial diff and confirmed the same changes in commit `f25e9eaf4be9f0054922fd9163e00ebdb0b7365f`.
```

`git commit -m 'fix(hook): point the formatter recovery hint at make update'` (exit 128; home paths normalized):

```text
error: Couldn't load public key ~/.ssh/id_ed25519.pub: No such file or directory?

fatal: failed to write commit object
```

`git -c commit.gpgsign=false commit -m 'fix(hook): point the formatter recovery hint at make update'` (exit 0; home paths normalized):

```text
error: Unable to create '~/Workspace/dotfiles/.git/packed-refs.lock': Operation not permitted
[t121/hook-hint f25e9eaf] fix(hook): point the formatter recovery hint at make update
 2 files changed, 8 insertions(+), 4 deletions(-)
```

`git push origin HEAD:feat/rolling-tools-single-update` (exit 128):

```text
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

`GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles HEAD:feat/rolling-tools-single-update` (exit 0):

```text
To https://github.com/mryfmo/dotfiles
   b621af77..f25e9eaf  HEAD -> feat/rolling-tools-single-update
```

`git rev-parse HEAD && git show --stat --oneline HEAD` (exit 0):

```text
f25e9eaf4be9f0054922fd9163e00ebdb0b7365f
f25e9eaf fix(hook): point the formatter recovery hint at make update
 home/dot_claude/hooks/executable_format-edited-files.py | 8 +++++---
 tests/unit/test_format_edited_files_hook.py             | 4 +++-
 2 files changed, 8 insertions(+), 4 deletions(-)
```

GitHub was inspected with `gh` first. PR: https://github.com/mryfmo/dotfiles/pull/310.
The post-push `gh pr checks 310 --watch --interval 30` showed successful build,
private-bootstrap, changes and validate jobs; public bootstrap and unit-test jobs
were pending. No failing check was observed. Final-head paginated Bot reviews
and top-level comments returned empty output. The bounded wait began and logged:

```text
bot: pending head=f25e9eaf4be9f0054922fd9163e00ebdb0b7365f elapsed=1s
```

Amendment 2 requests RESULT now and assigns the integration gate to the
orchestrator. CI/Bot completion is handed to the orchestrator; no passing CI
claim or completed Bot-wait claim is made here. No PR edits, thread resolution,
rebase, force-push or make update occurred.

## Amendment 2 handoff

The CI watcher and Bot polling command were stopped with Ctrl+C (each exit 130)
so the immediate RESULT can hand completion to the orchestrator. Bot output:

```text
bot: pending head=f25e9eaf4be9f0054922fd9163e00ebdb0b7365f elapsed=32s
bot: pending head=f25e9eaf4be9f0054922fd9163e00ebdb0b7365f elapsed=63s
bot: pending head=f25e9eaf4be9f0054922fd9163e00ebdb0b7365f elapsed=94s
bot: pending head=f25e9eaf4be9f0054922fd9163e00ebdb0b7365f elapsed=126s
Traceback (most recent call last):
  File "<stdin>", line 22, in <module>
KeyboardInterrupt
```

Worker JSON evidence shape was read and validated with uv/Python (exit 0):

```text
Worker review evidence: valid; 1 resolved review-scope approval
```

`git diff --stat` returned no output (exit 0): tracked changes are committed.
`git status --short` (exit 0):

```text
?? .orchestration/reports/dotfiles-T121-claude-hook-install-hint-a01.md
?? .orchestration/sandboxes/dotfiles-T121-claude-hook-install-hint-a01.md
?? .orchestration/validation/dotfiles-T121-claude-hook-install-hint-a01-worker-crit.json
?? .orchestration/validation/dotfiles-T121-claude-hook-install-hint-a01-worker-review-receipt.md
?? .orchestration/validation/dotfiles-T121-claude-hook-install-hint-a01.md
```
