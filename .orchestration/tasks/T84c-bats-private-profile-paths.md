# T84c: bats スイートの旧 modify\_ パス参照更新 (PR #140 CI fail + P1)

task_id: T84c
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: T84 follow-up; branch fix/chezmoi-drift-resolution (checked out)
depends: T84b (accepted)

[memory: decision — Renames of chezmoi source files must sweep every test surface including the CI-only bats suites; the sweep greps the whole tests/ tree for the old and new source names, not just the suites that run locally.]

## Finding (chatgpt-codex-connector P1 + 3 CI matrix fails, REAL; task-spec gap: T84 allowed_files omitted tests/install)

tests/install/common/lifecycle.bats:384 greps the removed
home/dot*codex/modify_standard.config.toml; the modify_private* rename
makes it fail on every CI matrix job. Repo policy runs bats only in CI,
so local gates could not catch it.

## Fix (exact; class = complete rename sweep)

1. Grep the ENTIRE tests/ tree (all suites, fixtures, helper scripts)
   for `modify_(deep|express|review|security|standard)` without the
   `private_` infix; update every hit to the renamed source. Record the
   full hit list (expect at least lifecycle.bats:384; report zero-miss).
2. Also grep for the literal old filenames anywhere else in the repo
   (docs, scripts) and update or justify remaining hits.
3. Do NOT run bats locally (repo policy). Verify with bash -n on edited
   bats files and the unit suite.
4. Gates: make format / validate-agent-assets / unit-test.

## Allowed files

tests/\*\* (including tests/install), docs if hits found, artifact paths
(T84c set).

## Forbidden actions

git commit; git push; chezmoi apply; local bats execution; source
renames beyond reference updates.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line.
Reply `AGMSG-RESULT v1 task_id=T84c`. max_turns=10.
