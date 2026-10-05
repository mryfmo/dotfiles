# dotfiles-T78-dead-docs-adh-a01 — validation

PR #261 (https://github.com/mryfmo/dotfiles/pull/261), branch `chore/dead-docs-adh`, final head `8d536a3860044eee629da063ca1ce08eae050c31`, base `origin/main` 6534df0f (#258).

## Task file verification

```text
$ sha256sum ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T78-dead-docs-adh-a01.md
51154a41101b6bb996db170be812a87fae19dc67a21738cba90607cdc2b6c8f6  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T78-dead-docs-adh-a01.md
dispatched task_rev 8262026d… (initial) and 51154a41… (PONG decision); the sha256 above matches the latest
```

## Validation commands on the final head (verbatim)

Notes on the outputs below:

- `git diff --stat` is split so the 198 deleted `reviews/` files are summarised rather than listed.
- The `.claude/loop.md` permission line is the sandbox denying a read of a non-tracked file; it is not a match.
- The four remaining "Conventional Commit" files are: the rules file itself; its owning skill (description and two one-line format reminders); and the two pointers this PR adds (`commit.md`, `plans/README.md`).
- `plans/` is in `.prettierignore`, so prettier skips `plans/README.md` and `plans/004-*`.

```text
$ git rev-parse HEAD; echo "rc=$?"
8d536a3860044eee629da063ca1ce08eae050c31
rc=0
$ git diff origin/main --stat -- . ':!reviews'; echo "rc=$?"   (reviews/ summarised by the next command)
 .coderabbit.yaml                                   |   1 -
 .github/copilot-instructions.md                    |  70 --------------
 .prettierignore                                    |   1 -
 AGENTS.md                                          |   7 --
 docs/plans/nix-first-architecture.md               |   3 +
 docs/plans/nix-migration.md                        |   3 +
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  10 +-
 home/dot_claude/commands/commit.md                 | 104 +--------------------
 home/dot_config/codex/AGENTS.md                    |   6 --
 plans/004-harden-and-lock-the-supply-chain.md      |   3 +
 plans/README.md                                    |   4 +-
 11 files changed, 16 insertions(+), 196 deletions(-)
rc=0
$ git diff origin/main --shortstat -- reviews; git ls-tree -r --name-only origin/main reviews | wc -l; git ls-files reviews | wc -l
 198 files changed, 114046 deletions(-)
198
0
$ git diff origin/main --shortstat; echo "rc=$?"
 209 files changed, 16 insertions(+), 114242 deletions(-)
rc=0
$ /usr/bin/grep -rln "Hermes\|learn_index\|ADH" AGENTS.md home/dot_agents/skills home/dot_config/codex ; echo "rc=$?"
rc=1
$ git ls-files | /usr/bin/grep learn_index; echo "rc=$?"
rc=1
$ test ! -d reviews/ADH_Integrated_Plan && echo "reviews gone"
reviews gone
$ test ! -f .github/copilot-instructions.md && echo "copilot gone"
copilot gone
$ /usr/bin/grep -rl "Conventional Commit" --include='*.md' . | /usr/bin/grep -v '^./.orchestration\|^./.agents\|^./.ua\|worktrees'
./home/dot_claude/commands/commit.md
./home/dot_agents/skills/gh-first-workflow/SKILL.md
./home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md
/usr/bin/grep: ./.claude/loop.md: 許可がありません
./plans/README.md
$ /usr/bin/grep -n "Conventional Commit" home/dot_agents/skills/gh-first-workflow/SKILL.md home/dot_claude/commands/commit.md plans/README.md
home/dot_agents/skills/gh-first-workflow/SKILL.md:3:description: Enforce gh-first GitHub investigation, pull request maintenance, and Conventional Commit output rules. Use when investigating GitHub issues or pull requests, creating or updating pull requests, summarizing investigation results, or preparing commit messages.
home/dot_agents/skills/gh-first-workflow/SKILL.md:25:7. Write commit messages in Conventional Commit format.
home/dot_agents/skills/gh-first-workflow/SKILL.md:34:- Keep commit subject in Conventional Commit form: `<type>(<scope>): <summary>`.
home/dot_claude/commands/commit.md:9:- Step 5: Write a commit message following the Conventional Commit policy in `~/.agents/skills/gh-first-workflow/references/gh-git-rules.md`.
plans/README.md:18:- Use Conventional Commits as
$ mise x node npm:prettier -- prettier --check AGENTS.md home/dot_claude/commands/commit.md plans/README.md; echo "rc=$?"
Checking formatting...
All matched files use Prettier code style!
rc=0
$ mise x node npm:prettier -- prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/codex/AGENTS.md docs/plans/nix-first-architecture.md docs/plans/nix-migration.md; echo "rc=$?"
Checking formatting...
All matched files use Prettier code style!
rc=0
$ uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v 2>&1 | tail -4; echo "rc=$?"
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
rc=0
$ make validate-agent-assets 2>&1 | grep -v "^WARN: regime-boundary" | tail -3; echo "rc=$?"   (exit status captured without a pipe)
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
rc=0
$ make unit-test 2>&1 | tail -4; echo "rc=$?"   (exit status captured without a pipe)
----------------------------------------------------------------------
Ran 773 tests in 176.125s

OK (skipped=1)
rc=0
```

## `gh pr checks 261` and state (final head 8d536a38)

```text
$ gh pr checks 261 --watch --interval 30; gh pr checks 261
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37218749711/job/111484577314	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37218749549/job/111484576877	
private-bootstrap (ubuntu-24.04, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37218749549/job/111484576841	
private-bootstrap (ubuntu-24.04, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37218749549/job/111484576701	
public-bootstrap (macos-14, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37218749549/job/111484576811	
public-bootstrap (ubuntu-24.04, client)	pass	9m3s	https://github.com/mryfmo/dotfiles/actions/runs/37218749549/job/111484576813	
public-bootstrap (ubuntu-24.04, server)	pass	7m30s	https://github.com/mryfmo/dotfiles/actions/runs/37218749549/job/111484576837	
test (macos-14, client)	pass	5m46s	https://github.com/mryfmo/dotfiles/actions/runs/37218749711/job/111484613369	
test (ubuntu-24.04, client)	pass	7m13s	https://github.com/mryfmo/dotfiles/actions/runs/37218749711/job/111484613323	
test (ubuntu-24.04, server)	pass	4m25s	https://github.com/mryfmo/dotfiles/actions/runs/37218749711/job/111484613350	
test (ubuntu-26.04, client)	pass	6m37s	https://github.com/mryfmo/dotfiles/actions/runs/37218749711/job/111484613415	
validate	pass	28s	https://github.com/mryfmo/dotfiles/actions/runs/37218749641/job/111484576994	
$ gh api repos/mryfmo/dotfiles/pulls/261 --jq '.head.sha, .mergeable_state'; git ls-remote origin refs/heads/main
8d536a3860044eee629da063ca1ce08eae050c31
blocked
6534df0f769fe5c12aa6e26e5355651e7a45f636	refs/heads/main
```

## Bot wait (final head pushed 2026-10-04T16:58:34Z; Bot review of the final head at 17:02:26Z ended the wait)

```text
window 2026-10-04T17:07:54Z .. 2026-10-04T17:07:55Z; final head 8d536a3860044eee629da063ca1ce08eae050c31
$ gh api --paginate repos/mryfmo/dotfiles/pulls/261/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'
8d536a3860044eee629da063ca1ce08eae050c31	2026-10-04T17:02:26Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/261/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.commit_id,.path]|@tsv'
4178539979	8d536a3860044eee629da063ca1ce08eae050c31	.github/copilot-instructions.md
review of final head: yes
$ gh api --paginate repos/mryfmo/dotfiles/pulls/261/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot" and .original_commit_id=="8d536a3860044eee629da063ca1ce08eae050c31")|[.id,.path,.line]|@tsv'
4178539979	.github/copilot-instructions.md	1
$ gh api repos/mryfmo/dotfiles/pulls/comments/4178539979 --jq .body
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Retain Copilot repository instructions**

When this repository is used with GitHub Copilot Chat, code review, cloud agent, or CLI, deleting this file removes the repository-wide instructions that those products automatically load; `AGENTS.md` does not replace its Copilot-specific Conventional Commit, idempotency, security, and cross-platform guidance. Keep this file or migrate its required rules into a Copilot-supported instruction source. [GitHub’s support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support) lists `.github/copilot-instructions.md` as repository-wide instructions for these Copilot surfaces.

Useful? React with 👍 / 👎.
```

## CompactionDB (main checkout, unsandboxed)

```text
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T78 (operator 2026-10-03): the ADH clauses and `reviews/ADH_Integrated_Plan/` leave dotfiles, the Hermes and `learn_index.md` references are deleted, `.github/copilot-instructions.md` is deleted, and the Conventional Commit rules live only in `gh-first-workflow/references/gh-git-rules.md`.'
86309afa-7762-4bb2-8e4b-ed6e6f3b7fb0
```
