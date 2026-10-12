# Validation: dotfiles-T128-process-rules-a07

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This branch copy covers the task-copy commit; the main-checkout copy adds the final head (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a07.md .orchestration/dotfiles-T128-process-rules-a07/task.md | cut -c1-64
d5d499cead2297a8357b243d46172f8fea7cb929b4e4a62addb71633f3babb6a
d5d499cead2297a8357b243d46172f8fea7cb929b4e4a62addb71633f3babb6a
$ diff ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a06.md .orchestration/dotfiles-T128-process-rules-a07/task.md | grep -E "^> +(- control|disposition|- \.orchestration|receipt)" | cut -c1-150
>   receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
>   - .orchestration/dotfiles-T128-process-rules-a07/**
>   - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, the rules Claude seats follow once it is applied
>   - control: the task-file copies on the branch (.orchestration/dotfiles-T128-process-rules-a01/task.md, -a02/task.md, -a03/task.md, -a04/task.md, -
>     disposition: "residual: each copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchest
>   - control: the branch evidence records under .orchestration/dotfiles-T128-process-rules-a07/ and the a01 to a06 directories (report.md, validation
>     disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and GitHub, the counters, t
```

## 2. Checks at `f755d714` (no content change in this task)

```
$ git log --oneline -1; git diff --stat f755d714 -- home AGENTS.md tests; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1
f755d714 chore(orchestration): task file for dotfiles-T128-process-rules-a06, Amendment 1
Ran 42 tests in 0.012s

OK
All matched files use Prettier code style!
```

The empty `git diff --stat` is the "no content change". The removal proofs of items 1 to 10 are in the a02 to a05 evidence directories; nothing they cover changed.

## 3. CompactionDB (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a07 …'
2ac58f54-4cf8-46f8-9ec9-b90695510582
```
