# T59b: REPAIR gaps found in T61 live verification

task_id: T59b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-harness-composability-integration.md (Phase 5; defects found in T61 E2E-3')

[memory: failure — Live REPAIR verification exposed three gaps: shared-skill missing-file findings had no repair mapping (deleted files stayed missing -> non-convergent), plain `chezmoi apply` prompts for a TTY on deleted targets (headless repair fails), and legacy agmsg runtime files at the skill root (messages.db, 2026-08-07) are flagged as ERROR instead of tolerated runtime.]

## Defects (orchestrator-verified live)

1. `rm ~/.agents/skills/agmsg/scripts/history.sh` -> REPAIR=1 repaired an
   unrelated codex-config drift but NOT the deleted file; run ended
   `non-convergent after repair` (exit 2). The
   "shared skill directory is missing files" category has no repair
   mapping.
2. Restoring the deleted file needed `chezmoi apply --force`; plain apply
   died with "could not open a new TTY" (chezmoi prompts when the target
   was deleted since last write). Headless REPAIR must always pass
   --force on its chezmoi invocations (safe: targets are single,
   source-derived, and were just detected as drifted).
3. `~/.agents/skills/agmsg/messages.db` (mtime 2026-08-07, predates the
   db/ relocation) is reported as
   "shared skill directory has unexpected files: agmsg/messages.db" —
   an ERROR. Legacy agmsg runtime artifacts at the skill root should be
   tolerated like db/run/teams, not treated as drift.

## Fix (exact)

1. Wire the shared-skill categories into the repair mapping:
   - missing files -> `chezmoi apply --force <the skill file target>`
     (single-target, per file);
   - unexpected files -> NOT repaired (report-only), except rule 3 below.
2. ALL repair-mode chezmoi invocations gain `--force` (including the
   existing missing/content mappings). Report-only mode unchanged.
3. Tolerance: in the shared-skill unexpected-file check, treat these
   agmsg-root runtime patterns as accounted (no finding):
   `messages.db`, `messages.db-wal`, `messages.db-shm` directly under
   skills/agmsg/ — mirroring the existing db/run/teams tolerance. Do NOT
   broaden beyond these exact names. The stray file itself is left on
   disk untouched (operator decision later).
4. Tests: deleted-skill-file repair converges; --force present on every
   chezmoi repair invocation (spy asserts argv); agmsg-root runtime
   names produce no finding while another unexpected file still does;
   existing tests unchanged.

## Allowed files

- scripts/check-agent-runtime.py
- tests/unit/ (matching modules)
- Your artifact paths (T59b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply (in dev; tests stub it); bats;
dependency changes; touching the stray messages.db; guard weakening;
changes outside the three fixes.

## Validation

1. `make unit-test` all green (totals + new count); `make format`;
   `make validate-agent-assets`.
2. Fake-HOME transcript: deleted-file repair now converges (exit 0).
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T59b set); memory add with the failure fact
(--kind failure); effects=none expected.
Reply `AGMSG-RESULT v1 task_id=T59b status=ready_for_review`. max_turns=15.
