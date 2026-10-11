# Validation: dotfiles-T128-process-rules-a03

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This branch copy covers the a03 commits; the main-checkout copy adds the final head (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a03.md .orchestration/dotfiles-T128-process-rules-a03/task.md | cut -c1-64
867ea4ca7c86f6518432a12254c3befc471184140b46b66aea2c53e6cb5ec78d
867ea4ca7c86f6518432a12254c3befc471184140b46b66aea2c53e6cb5ec78d
```

Both equal TASK 472's `task_sha256=867ea4ca…`.

## 2. Checks at `f4d45983`

```
$ git log --oneline -3; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
f4d45983 chore(orchestration): task file for dotfiles-T128-process-rules-a03
798fa098 docs(regime): scope the push-only exit to Claude seats
97288f6f chore(orchestration): evidence for the a02 revise's fifth item and Bot fix round 1
Ran 36 tests in 0.011s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ git show --stat --format=%h 798fa098
798fa098

 home/dot_agents/skills/agmsg-orchestration/SKILL.md | 2 +-
 tests/unit/test_agmsg_orchestration_docs.py         | 2 ++
 2 files changed, 3 insertions(+), 1 deletion(-)
```

## 3. Removal proofs (`scratchpad/mutate-a03.sh` at `f4d45983`: the step 2 sentence of `798fa098` reverted to its a02 wording, then removed; output cut to three lines of at most 400 characters per rule)

```
== removed rule: codex-seat-pushes-inside (SKILL, diff lines: 2) -> test_workers_commit_inside_the_sandbox
FAIL: test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) (<redacted:secret-pattern>)
AssertionError: 'a Codex seat pushes from inside it (step 4)' not found in " and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR as a draft with 
FAILED (failures=1)
== removed rule: commit-inside-the-sandbox (SKILL, diff lines: 2) -> test_workers_commit_inside_the_sandbox
FAIL: test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) (<redacted:secret-pattern>)
AssertionError: 'Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there' not found in " and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push o
FAIL: test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) (<redacted:secret-pattern>)
== restored: OK
```

## 4. CompactionDB (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a03 …'
ae486f65-e10d-44bd-8680-8261d6fa4492
```
