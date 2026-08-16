# T51a: Fix pre-existing repo-wide shfmt drift (T51 all-green prerequisite)

task_id: T51a
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-compactiondb-research-integration.md (Phase 6, all-green gate #1; ruling logged at T48)

## Goal

Make `make format` (shfmt --indent 4 --space-redirects --diff .) exit clean
repo-wide by fixing the pre-existing drift, starting with
home/dot_agents/skills/agmsg/scripts/executable_actas-claim.sh.

## Allowed files

Only shell files that `make format` currently reports as drifted (apply the
exact shfmt formatting, no semantic changes), plus your artifact paths
(T51a five artifacts).

## Forbidden actions

git commit; git push; chezmoi apply; bats; any non-formatting change; any
file `make format` does not report.

## Work order

1. Run `make format`; list every reported file in the report.
2. Apply shfmt's own output (`shfmt --indent 4 --space-redirects -w <file>`)
   to exactly those files.
3. `bash -n` each touched file.
4. Re-run `make format` -> exit 0, no output.

## Validation

1. `make format` exit 0 (paste).
2. `bash -n` results.
3. `git diff` of touched files (must be whitespace/format-only; confirm
   with `git diff -w` being empty).
4. `git status --porcelain` -> only reported files + artifacts.

## Completion / RESULT contract

Five artifacts (reports/validation/sandboxes/learning/autoskill T51a).
Reply AGMSG-RESULT v1 task_id=T51a. max_turns=10.
