---
format: 2
task_id: dotfiles-T128-settings-hook-dedupe-followup-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-settings-hook-dedupe-followup-review-a01 — confirm the task text `dotfiles-T128-settings-hook-dedupe-followup-a01` (review seat half; Codex headless runs the same check first, C-54)

Drafted 2026-10-17 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-followup-a01.md` (its sha256 is the `owner_task_sha256` of the TASK line), the owner task of the settings-hook-dedupe lineage (PR #369, merged as 4775f56a): it implements the rows under `## Owned by dotfiles-T128-settings-hook-dedupe-followup-a01` in `.orchestration/acceptance/dotfiles-T128-settings-hook-dedupe-a01.md` on `origin/main`, today one row, `audit:ca892e4:1` (the predicate splits the command with shlex before comparing, so a quoted or escaped tilde path is taken for the managed path; the fix compares the whole command string with the two renderings and drops shlex, C-55 method 3).

## Stop condition

1. Item 1 describes the owned row correctly against `home/dot_claude/modify_private_settings.json` on `origin/main` (the identity predicate of PR #369: one shlex part equal to one of the two renderings of the managed path, `~/.claude/hooks/<name>` and the home directory's absolute form) and against the audit text in `.orchestration/validation/dotfiles-T128-settings-hook-dedupe-a01-audit-ca892e4.md.last.md` (the P2 on the quoted tilde): the whole command string, stripped of surrounding whitespace only, compared with the two renderings, no shlex; a quoted or escaped tilde path (`'~/.claude/hooks/format-edited-files.py'`, `\~/.claude/hooks/format-edited-files.py`) kept as unmanaged.
2. Item 2's test cases name the quoted and the escaped case, both kept, in `tests/unit/test_claude_settings_merge.py` beside the lineage's cases, which stay.
3. The threat table has one row per `allowed_files` entry and the generic rows verbatim from `.orchestration/templates/task-short.md` (id substituted); the Completion clause is the template's clause of 2026-10-16 (the Bot's review at PR open and once more on `@codex review` after a P0/P1 fix round, a surviving P0/P1 as `open:<thread id>` with `bot_rounds=2`, the C-50 revise round, every other P2 advisory and owned by the next owner task); no sentence states an unlanded mechanism as present.
4. The file passes C1 to C10 and C7b (the orchestrator pasted its `OK`), the mask check (`masked 0 match(es)`), and its premises replay from this checkout (`origin/main` fetched) with the outputs recorded in the file.

## Output

`.orchestration/validation/dotfiles-T128-settings-hook-dedupe-followup-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-settings-hook-dedupe-followup-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-settings-hook-dedupe-followup-review-a01 round=<n> verdict=confirm|revise owner_task_sha256=<sha> validation=<path>`.
