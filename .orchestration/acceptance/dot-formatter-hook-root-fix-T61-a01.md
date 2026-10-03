# Acceptance: dot-formatter-hook-root-fix-T61-a01

- **Decision:** ACCEPTED after three revise rounds. PR #233 squash-merged to `main` as `70090067` (final head `7dff3a5c`, base `3915e327`). Merged without `--delete-branch` while worker-c holds `chore/formatter-root-fix`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `f93ae279…` → `c4c2fb43…` (round 1) → `47e7df20…` (round 2) → `d0836233…` (round 3); all matched.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Operator decision carried:** D3 "後者" (format once, keep formatted in CI) rather than deleting the hook.

## What was accepted (51 files, +1436/−2118; 12 commits)

- **Pins:** `ruff = "0.16.10"` (aqua) and `"npm:prettier" = "3.9.9"` in `home/dot_mise/config.toml` with lock entries; no existing pin changed. `make update` and `install/common/mise.sh` install both (round 1); bats/unit expectations synced.
- **Config:** `ruff.toml` (line-length 120, target py312 = lowest CI Python, `force-exclude`, excludes `vendor .ua .orchestration reviews .agents .claude references`); `.prettierignore` (same set plus `plans/` and `CLAUDE.md`). `plans/` holds command tables whose code spans contain `|`/`*` that prettier corrupts; `CLAUDE.md`'s CompactionDB block would ping-pong with `vendor/compactiondb/install.py`. Both are byte-identical to `origin/main`.
- **Hook** (`format-edited-files.py`): runs only `ruff format --config <root>/ruff.toml` and `prettier --write` from each edited file's repository root with the pinned PATH tools; reports a missing tool without a traceback; `uvx`/`npx`, `ruff check --fix` and `uvx ty check` removed; the dead `python_post_edit`/`markdown_post_edit` manifest lists removed and the generator keys on `format_edited_files_hook`. New `tests/unit/test_format_edited_files_hook.py` (2 tests).
- **CI:** formatters installed in the exact-config step; new "Check Python and Markdown formatting" step (`--config ruff.toml`, `prettier --check`, no version literal); `should_test` set by any changed `.py`/`.md` outside `.orchestration/`, read with `git -c core.quotePath=false` and without a pipe under pipefail (rounds 2–3). `make format` extended with the same checks via PATH shims.
- **Format-only commit e5648fa6:** 46 files, +1288/−2166. Orchestrator reproduced it from bd9a7995 with the PR's pinned tools: identical except one prettier non-idempotent line in plans/005 (later restored with all of plans/). The head is a fixpoint. Markdown changes outside plans/ are list markers (`*`→`-`) and lazy-continuation indentation; the auditor confirmed 35 Python files keep identical syntax trees. 718 → 712 tests, OK.

## Deviations and decisions

- Task said "two commits"; the Bot's findings arrived on the format commit and force-push is forbidden, so fixes followed as separate commits. Accepted; per-commit audits cover them.
- Allowed files extended in round 1 (`Makefile` line 72, `install/common/mise.sh` line 108, their tests) to fix the Bot P1 at its root instead of deferring.
- Round 2 refused the worker's "follow-up" proposal for three new Bot P2s (operator rule: Bot findings are fixed at the root once); all three fixed in 74ade52f.
- `make format`'s pre-existing first line (`shfmt --diff .`) already fails on origin/main; out of scope, noted for the dead-code/lifecycle work.
- A Codex review of the final one-line commit leaves no durable trace (one thumbs-up per user); accepted on the audit instead. The Codex review-activity summary comment is no longer present on the PR.

## Audit (per commit)

| commit | verdict | findings → disposition |
|---|---|---|
| 45d44292 | incorrect | P1 bare binaries → fixed:0827371f; P1 vendored pyproject → fixed:bd9a7995; P1 prettier cwd → fixed:772ff3c6; P2 should_test → fixed:ff37f41d/74ade52f; P2 .agents → fixed:ae806f37 |
| bd9a7995 | correct | — |
| e5648fa6 | incorrect | plans tables corrupted → fixed:b5084de5, 57021632 (plans identical to origin/main) |
| ff37f41d, b5084de5, 57021632, ae806f37 | correct | — |
| 772ff3c6 | incorrect | P3 `strip()` on repo path → fixed:0827371f |
| 0827371f | correct | — |
| 3da4cfad | not audited | update-branch merge; first-parent diff is `.orchestration/` only |
| 74ade52f | incorrect | P2 quoted non-ASCII paths → fixed:7dff3a5c |
| 7dff3a5c | correct | — |

## Codex Bot

- 9 inline threads over 6 pushes (2 × P1, 7 × P2), all fixed in-PR (ff37f41d, b5084de5, 772ff3c6, 57021632, ae806f37, 0827371f, 74ade52f); orchestrator verified each fix in the diff, replied and resolved all nine; `mergeable_state` `clean`. Sweep (head 7dff3a5c): 39 items, 0 failure/warning, all dispositioned.

## Gate

- `.claude/worktrees/orchestrator-review` at 7dff3a5c with evidence copies: `BASE=origin/main PR_FEEDBACK_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` exit 0. Copies removed.

## CompactionDB

- Decision `d7c79b1d-bad6-491b-b0f1-e77c4b54e164` recorded by the worker from the main checkout; cited.

## Operator follow-up

- `make update` on each machine (DGX: `~/Workspace/dotfiles` and `~/.local/share/chezmoi`; Mac clone) installs ruff and prettier and applies the new hook; until then the old hook (`npx prettier@2`) is still the deployed one.
- Learning candidates worth codifying later: prettier corrupts pipe-in-code tables (scan before adopting it on prose); the Codex Bot reviews every push, so workers wait for the review of the final head before RESULT.
