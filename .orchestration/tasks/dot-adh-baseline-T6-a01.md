# AGMSG-TASK dot-adh-baseline-T6-a01 — commit the ADH Integrated Plan baseline (`reviews/`)

`reviews/ADH_Integrated_Plan/` is the READ-ONLY ADH V4 input baseline (AGENTS.md), verified by its own `SHA256SUMS`. It has sat untracked in the main worktree since 2026-09-18. Commit it as-is so the baseline is versioned; never modify any file under it.

## Steps

1. New worktree `.claude/worktrees/adh-baseline` (branch `docs/adh-integrated-plan-baseline`) from `origin/main`.
2. Copy `reviews/` from the main worktree (`/Users/mryfmo/Workspace/dotfiles/reviews`) into the new worktree byte-for-byte (`rsync -a --exclude .DS_Store`); `.DS_Store` is gitignored and must not be committed.
3. Verify: `cd reviews/ADH_Integrated_Plan && shasum -a 256 -c SHA256SUMS` → every line OK, paste the count of OK lines and any non-OK line (must be none). Confirm every file listed in `PACKAGE_MANIFEST.json` (if it lists files) exists.
4. Secret scan over `reviews/` (`grep -rEn 'ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH) PRIVATE'`) → paste the (empty) result. Report total files and size.
5. Check that no repo validator or unit test is affected: `make unit-test`, `uv run --with pyyaml python scripts/validate-agent-assets.py`, `git diff --check`. If any tool scans `reviews/` (e.g. shfmt/shellcheck over `*.sh` under it, markdown lint), report it; do NOT modify baseline files — instead propose the narrowest exclusion and stop for orchestrator decision.
6. `git add reviews` and stop (no commit; orchestrator commits with a docs commit).

## allowed_files

`reviews/**` (add only, byte-identical), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-adh-baseline-T6-a01.md`.

## forbidden_actions

no git commit; no push; no PR; no edits to any file under `reviews/`; no .gitignore changes without stopping first.

max_turns=15. Reply with `AGMSG-RESULT v1`.
