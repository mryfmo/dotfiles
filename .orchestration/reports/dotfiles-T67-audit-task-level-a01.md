# Report: dotfiles-T67-audit-task-level-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/audit-task-level` from `origin/main` 3a0816e6.
- **task_rev:** `df653369…`, matched.
- **PR:** #242, https://github.com/mryfmo/dotfiles/pull/242.
- **Commits:**
  - `28373e27`: the change.
  - `58f5677a`: `gh pr update-branch` with `main` 40d9eb6c (T73).
  - `9476141f`: Codex P1 fix.
- **Final head:** `9476141f`.
  - **CI:** green; 13 pass including CodeRabbit, and `nix` is skipped.
  - **Branch:** up to date with `main` 40d9eb6c (behind_by=0).
  - **Codex:** 👍.
  - **`mergeable_state`:** `blocked`, only by the unresolved Codex P1 thread 4175659540 (fixed in `9476141f`), which is left for the orchestrator.

## Change

1. **`--task <id>` on `--audit`** (arg loop, usage, header `@option`):
   - The id must be one path segment (`^[A-Za-z0-9][A-Za-z0-9._-]*$`). An explicitly empty `--task` is refused too, through an `audit_task_given` flag, rather than silently falling back to a per-commit audit.
   - Both checks run before any Herdr call.
2. **Resolution relative to DIR, before any Herdr work:**
   - `.orchestration/tasks/<id>.md` is required; when it is missing, the run exits 2 naming the full path.
   - `audit_base=$(git -C DIR merge-base origin/main <sha>)`; when it fails, the run exits 2 with a fetch hint.
   - The worker's report, validation and sandbox are named only when present. Each is `<id>.md`, or `<id>.txt` when no `.md` exists (P1 fix: older tasks such as T24 declared `.txt` artifacts).
   - `<id>-pr-feedback.json` is named only when present.
   - `--out` defaults to `.orchestration/validation/<id>-audit-<sha7>.md`; the `.last.md` sibling is derived as before.
3. **Prompt with `--task`:** the task's text, verbatim. The only change is ASCII colons instead of em dashes after the three dimension names. The base and head are inlined in `git diff <base> <sha>` and `git log --oneline <base>..<sha>`. The AGENTS.md reference is kept.
4. **Unchanged:**
   - Without `--task`: the prompt, default name and flow (the existing `AUDIT_PROMPT` tests pass as they were).
   - The exit-marker mechanics, the masker trust guard (it keys on the validator and the audited commit, not on the output name, so the new name is accepted as is) and the verdict regex.
5. **README audit section:** documents `--task`, the inputs, the three dimensions, the default output name, the one-audit-per-final-head rule and the `.txt` fallback. The headless `codex --profile audit exec --sandbox read-only -C <dir> -o <file> '<prompt>'` block stays.
6. **Tests:** four new tests plus two new subtests:
   - the full prompt with the inlined merge-base and the default output path;
   - only the task file named when no artifact exists;
   - a `.txt` fallback, with `.md` winning when both exist;
   - a missing task file or merge-base exits 2 before any `tab`/`pane run` call;
   - a path-like and an empty `--task` are rejected.
   - Each new test fails against the code it guards.
   - Totals: 229 herdr-agents tests, `make unit-test` 726 OK.

## Notes

- **Phantom `.git/config.lock`:** the main checkout holds an empty read-only `.git/config.lock`, a regular file of 0 bytes created at 10:09:10 local time, the moment of my sandboxed `git switch -c`.
  - It is the Claude sandbox's mount point for its write-deny mask: every sandboxed command bind-mounts over it, so the file reappears.
  - While it exists, unsandboxed git config writes in that repository fail. My `git push -u` printed "could not lock config file … File exists", but the push landed (`git ls-remote` shows the head).
  - I did not delete it: it is a sandbox artifact and comes back with the next sandboxed command. Flagged here for the orchestrator's git operations in the main checkout.
- **Escalation of the Codex P1:** the task file names `<id>.md`, and I extended that to `.txt` because the Bot's P1 is a real evidence gap. Requiring P0/P1 fixes is the task's own rule.

## Codex bot

| Head | Result |
|---|---|
| `28373e27` | 👍 |
| `58f5677a` | P1 (`.txt` artifacts), fixed in `9476141f` |
| `9476141f` (final) | 👍 01:34:27Z |

I did not reply to or resolve any thread.

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T67 (operator 2026-10-03): `herdr-agents --audit <sha> --task <id>` audits a task once on its final head with the task file, the worker artifacts, the PR feedback JSON (CI and Bot threads) and the full PR diff from the merge-base, across specification conformance, implementation and evidence reality; output `<id>-audit-<sha7>.md`; per-commit audits are no longer the default.'
0de2f024-59c6-48dd-ba90-b85a669cc0cc
```

[memory:decision] dotfiles-T67 (operator 2026-10-03): `herdr-agents --audit <sha> --task <id>` audits a task once on its final head with the task file, the worker artifacts, the PR feedback JSON (CI and Bot threads) and the full PR diff from the merge-base, across specification conformance, implementation and evidence reality; output `<id>-audit-<sha7>.md`; per-commit audits are no longer the default.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T67-audit-task-level-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T67-audit-task-level-a01.md`
- learning: `.orchestration/learning/dotfiles-T67-audit-task-level-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T67-audit-task-level-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
