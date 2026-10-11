# Validation: dotfiles-T128-process-rules-a03

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This main-checkout copy covers the a03 commits through `b9a9da7d`, §6 the final head (design INV-8).

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

## 5. Bot fix round 1 at `7524e001` (thread 4240646079)

```
$ git log --oneline -1; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
7524e001 docs(regime): gh pr ready runs only while the PR is a draft
Ran 36 tests in 0.010s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
```

Removal proof (`scratchpad/mutate-a03-b1.sh`: the a02 wording of the step 15 bullet pasted back):

```
== removed rule: ready-only-while-draft (SKILL, diff lines: 2) -> test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first
FAIL: test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first) (<redacted:secret-pattern>)
AssertionError: 'Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft' not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Mark the PR ready for review with `gh pr ready <n>` before the wait: the Codex Bot reviews non-draft PRs, and a draft only on an explicit `@codex review` comment. When no Bot review of the final head arriv
FAILED (failures=1)
== restored: OK
```

## 6. Final head `b9a9da7d` (main-checkout copy)

```
$ gh pr checks 318 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	0	https://dashboard.gitguardian.com	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/38120890062/job/114415208579	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/38120890085/job/114415208821	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38120890085/job/114415208856	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38120890085/job/114415208831	
public-bootstrap (macos-14, client)	pass	8m15s	https://github.com/mryfmo/dotfiles/actions/runs/38120890085/job/114415208800	
public-bootstrap (ubuntu-24.04, client)	pass	7m32s	https://github.com/mryfmo/dotfiles/actions/runs/38120890085/job/114415208687	
public-bootstrap (ubuntu-24.04, server)	pass	8m7s	https://github.com/mryfmo/dotfiles/actions/runs/38120890085/job/114415208810	
test (macos-14, client)	pass	5m44s	https://github.com/mryfmo/dotfiles/actions/runs/38120890062/job/114415231868	
test (ubuntu-24.04, client)	pass	7m55s	https://github.com/mryfmo/dotfiles/actions/runs/38120890062/job/114415231888	
test (ubuntu-24.04, server)	pass	4m32s	https://github.com/mryfmo/dotfiles/actions/runs/38120890062/job/114415231867	
test (ubuntu-26.04, client)	pass	6m55s	https://github.com/mryfmo/dotfiles/actions/runs/38120890062/job/114415231925	
validate	pass	1m33s	https://github.com/mryfmo/dotfiles/actions/runs/38120890096/job/114415208704	
$ bash scratchpad/bot-wait.sh 318 b9a9da7d406fd6f210537c63369b8257dd1f954f 2026-10-11T07:17:48Z   # last poll
poll 5 07:20:04Z head b9a9da7d406fd6f210537c63369b8257dd1f954f asked=no
reviews: 
comments: 
code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T07:19:51.265559Z">2026-10-11T07:19:51.265559Z</relative-time> | `b9a9da7` | New commits |
DONE
$ # final recheck right before the RESULT
2026-10-11T07:26:43Z
$ gh pr view 318 --json headRefOid,state,isDraft
b9a9da7d406fd6f210537c63369b8257dd1f954f	OPEN	false
$ gh api --paginate repos/mryfmo/dotfiles/pulls/318/reviews --jq '.[]|select(.user.type=="Bot" and .submitted_at > "2026-10-11T06:30:00Z")|[.id,.commit_id[0:8],.submitted_at]|@tsv'
5482212241	108b43bd	2026-10-11T06:44:25Z
5482250375	97288f6f	2026-10-11T06:57:26Z
5482300822	c4300f47	2026-10-11T07:15:16Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/318/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot" and .created_at > "2026-10-11T06:30:00Z")|[.id,.original_commit_id[0:8],.path,(.original_line|tostring)]|@tsv'
4240566259	108b43bd	home/dot_agents/skills/agmsg-orchestration/SKILL.md	71
4240566263	108b43bd	tests/unit/test_agmsg_orchestration_docs.py	225
4240566266	108b43bd	home/dot_agents/skills/agmsg-orchestration/SKILL.md	201
4240566268	108b43bd	tests/unit/test_agmsg_orchestration_docs.py	285
4240598178	97288f6f	home/dot_agents/skills/agmsg-orchestration/SKILL.md	76
4240598179	97288f6f	home/dot_agents/skills/agmsg-orchestration/SKILL.md	183
4240646079	c4300f47	home/dot_agents/skills/agmsg-orchestration/SKILL.md	201
4240646082	c4300f47	home/dot_agents/skills/agmsg-orchestration/SKILL.md	71
$ gh api --paginate repos/mryfmo/dotfiles/issues/318/comments --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]")|.body' | grep -E 'Code Review|Security Review'
| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T07:19:51.265559Z">2026-10-11T07:19:51.265559Z</relative-time> | `b9a9da7` | New commits |
| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T04:24:27.529578Z">2026-10-11T04:24:27.529578Z</relative-time> | `f7c229f` | Draft marked ready |
$ gh api repos/mryfmo/dotfiles/issues/318/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
chatgpt-codex-connector[bot]	+1	2026-10-11T07:19:56Z
```
