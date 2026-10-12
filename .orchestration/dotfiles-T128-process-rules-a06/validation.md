# Validation: dotfiles-T128-process-rules-a06

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This branch copy covers the task-copy commit; the main-checkout copy adds the final head (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a06.md .orchestration/dotfiles-T128-process-rules-a06/task.md | cut -c1-64
c45a1000651933ad8bf418ba809c5c4f7a4fdd703f358e24a1dc6cff03718d5d
c45a1000651933ad8bf418ba809c5c4f7a4fdd703f358e24a1dc6cff03718d5d
$ diff ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a05.md .orchestration/dotfiles-T128-process-rules-a06/task.md | grep -E "^> +- control|^> +disposition" | cut -c1-160   # the fifth row
>   - control: the PR edits tests/fixtures/regime/*.md, the expected values of test_regime_rule_sections_are_pinned_whole, so a rule and its fixture can change 
>     disposition: "residual: a fixture diff is the declared change itself (the test's message requires listing it in the RESULT, INV-12); the orchestrator's di
```

## 2. Checks at `be0afe7e` (no content change in this task)

```
$ git log --oneline -1; git diff --stat be0afe7e -- home AGENTS.md tests; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1
be0afe7e chore(orchestration): evidence for the a05 revise round 1 (item 10)
Ran 42 tests in 0.011s

OK
All matched files use Prettier code style!
```

The empty `git diff --stat` is the "no content change". The removal proofs of items 1 to 10 are in the a02 to a05 evidence directories; nothing they cover changed.

## 3. CompactionDB (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a06 …'
52664f52-3f25-4b15-8fc3-ad49aaeb7612
```
