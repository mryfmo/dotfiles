# Validation: dotfiles-T67-audit-task-level-a01

- **task_rev:** `sha256:df653369e911fb0e6d99c55fa037b5f46d833640daf752f4b955f3e33e56dd73`. `sha256sum` of the task file in the main checkout matches.
- **Branch:** `feat/audit-task-level` from `origin/main` 3a0816e6.
- **PR:** #242, https://github.com/mryfmo/dotfiles/pull/242.
- **Commits:**
  - `28373e27`: the change.
  - `58f5677a`: `gh pr update-branch` merge of `main` 40d9eb6c (T73).
  - `9476141f`: Codex P1, `.txt` worker artifacts.
- **Final head:** `9476141f9d0d5405a0bf0d53f8a8c261e9ddf385`.

## Validation commands (verbatim, on the final head; unit tests run in the Claude sandbox)

```
$ git log -1 --format=%H
9476141f9d0d5405a0bf0d53f8a8c261e9ddf385
$ git diff origin/main --stat
 README.md                                         |  23 ++++-
 home/dot_local/bin/common/executable_herdr-agents |  71 +++++++++++++--
 tests/unit/test_herdr_agents.py                   | 105 ++++++++++++++++++++++
 3 files changed, 188 insertions(+), 11 deletions(-)
$ uv run python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
Ran 229 tests in 133.714s

OK (skipped=1)
$ make unit-test (tail -3)
Ran 726 tests in 164.400s

OK (skipped=2)
$ mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents; shellcheck home/dot_local/bin/common/executable_herdr-agents
shfmt exit=0
shellcheck exit=0
$ mise x node npm:prettier -- prettier --check README.md
Checking formatting...
All matched files use Prettier code style!
$ herdr-agents --help | grep -n -- '--task'   (branch copy: bash home/dot_local/bin/common/executable_herdr-agents --help)
5:       herdr-agents --audit <sha> [--task ID] [--out PATH] [--timeout SECONDS] [DIR]
40:incorrect verdict); it exits 2 without a managed workspace. With --task ID the
```

## New tests fail against the code they guard

```
$ (launcher from origin/main 3a0816e6) uv run python -m unittest -k audit_task -k rejects_unsafe tests.unit.test_herdr_agents
FAIL: test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff
FAIL: test_audit_task_names_only_the_task_file_when_no_artifact_exists
FAIL: test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work
Ran 4 tests in 0.117s
FAILED (failures=3)
$ (launcher from 58f5677a) uv run python -m unittest -k txt_artifact tests.unit.test_herdr_agents
FAIL: test_audit_task_names_a_txt_artifact_when_no_md_one_exists
Ran 1 test in 0.291s
FAILED (failures=1)
```

`test_audit_rejects_unsafe_arguments_before_calling_herdr` passes on the old launcher too, because it exits 2 on the unknown `--task` as a stray argument. Its two new subtests (a path-like id and an empty id) guard the new validation. The existing `AUDIT_PROMPT` tests for the no-`--task` path pass unchanged.

## make validate-agent-assets (run in the main checkout, which is on main)

```
$ make validate-agent-assets; echo exit=$?
exit=0
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: crit review server still running (pgrep -f 'crit _serve')
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-e (herdr-agents --remove-worker)
agent asset validation ok
(untracked .orchestration WARN lines omitted; the boundary commit is the orchestrator's)
```

## Codex review

| Head | Result |
|---|---|
| `28373e27` | 👍 2026-10-04T01:13:48Z |
| `58f5677a` (merge of main) | P1 "Include task-declared validation artifacts in the audit" (comment 4175659540): `.txt` artifacts such as T24's validation file were not named. Fixed in `9476141f`. |
| `9476141f` (final) | 👍 2026-10-04T01:34:27Z, no inline finding |

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T67 (operator 2026-10-03): `herdr-agents --audit <sha> --task <id>` audits a task once on its final head with the task file, the worker artifacts, the PR feedback JSON (CI and Bot threads) and the full PR diff from the merge-base, across specification conformance, implementation and evidence reality; output `<id>-audit-<sha7>.md`; per-commit audits are no longer the default.'
0de2f024-59c6-48dd-ba90-b85a669cc0cc
```

## CI, mergeable_state and branch (final head `9476141f`)

```
$ gh pr checks 242
CodeRabbit	pass
changes	pass
nix	skipping
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
$ gh api repos/mryfmo/dotfiles/pulls/242 --jq '.mergeable_state'
blocked
$ gh api repos/mryfmo/dotfiles/compare/main...feat/audit-task-level
behind_by=0 ahead_by=3
```

`blocked` is only the one unresolved Codex P1 thread (4175659540, fixed in `9476141f`), which is left for the orchestrator.
