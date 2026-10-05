# Acceptance: dotfiles-T81b-compactiondb-vendor-hygiene-a01

- **Decision:** ACCEPTED. PR #275 squash-merged to `main` as `794a80db`; final head `a536af5b` (round 2). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-05 06:08Z). Round 1 (03:30Z) came from the audit's P2 on installer hook ordering; round 2 (05:17Z) carried the docstring correction (PONG decision 6) that arrived after the round-1 RESULT, and absorbed one Bot P2 (decision 7). **Operator:** after `make update` deploys 2.0.0+dotfiles.9, trust the three Codex CompactionDB hooks and the permgate hook in Codex `/hooks` (T82 sequencing satisfied).
- **Worker:** `codex-security-dot-a007` (worker-e, wT:p8). task_rev matched at dispatch and after each of the three PONG-decision appends (final `5297e736…`).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping (seven artifact files copied from worker-e into the main checkout).
- **Plan reference:** Phase 5 follow-up to T81/T82 (vendor 2.0.0+dotfiles.9); unblocks the operator's Codex `/hooks` trust step sequenced in the T82 record.

## What was accepted (PR #275; round-0 head `b9acaa39`: 4b9cf2a3 (items 1–7), 771b9b4b (macOS test-only canonical-path fix), 597e851c (merge of main b63b8202), b9acaa39 (Bot P2 fixes + retention bound); round 1: 79e88d81, 6f7dfdb2, 634cb327, 3d478877 (merge of main 61806f56), 9f9b26f4; round 2: f6c47e8a, a536af5b)

- Item 1 `storage.py`: `enforce_size_cap` deletes the project's orphaned `sessions` rows (no remaining events) before evicting newer events and after every 100-row batch; other projects' rows untouched.
- Item 2 `install.py`: managed hook groups are replaced in their existing positions; `settings.json` is written and backed up only when the canonical merge differs (bytes, mtime and backup set preserved on a no-op reinstall).
- Item 3 tests: `from support import TempProject` bootstrap so `uv run python -m unittest discover -s vendor/compactiondb/tests` works from the repository root as well as `make -C vendor/compactiondb test` (101 tests).
- Item 4: CHANGELOG 2.0.0+dotfiles.9, `MANIFEST.sha256` regenerated, pin in `agent-config.yaml`, `test_asset_manifest.py` literals, README "Storage directory safety" section.
- Item 5 `paths.py` `ProjectPaths.ensure()`: fd-relative `mkdir`/`open(O_RDONLY|O_DIRECTORY|O_NOFOLLOW)`/`fchmod(0o700)` from the project root down to `health`, descriptors closed via `ExitStack` on failure, the pre-existing `.claude` directory keeps its mode (independent reviewer's P2, fixed before push). Contract per PONG decision 1: construction-time binding only; the same-user post-construction swap residual is documented in README, CHANGELOG and the receiver's shdoc.
- Item 6 `resolve_project_root()` and the Codex receiver: an implicit cwd walks up to the nearest `.git` directory or gitfile and selects the nearest `.claude/contextdb`; explicit roots and `CLAUDE_PROJECT_DIR` unchanged (PONG decision 2 added the receiver and its test to `allowed_files`).
- Item 7 `hook.py`/`cli.py`: `prune_health_artifacts()` shared by the SessionEnd maintenance pass and the explicit `prune` (errors.jsonl retention and quarantine cleanup, `.gitkeep` kept); `validate_config` requires `operations` to be an object with a non-negative integer `error_log_retention_days` below today's ordinal; the health log is opened `O_RDWR|O_NOFOLLOW|O_NONBLOCK` and must be a regular file; non-object JSON lines are retained as malformed (Codex Bot P2 ×3, fixed b9acaa39).
- Round 1 (audit P2 + PONG decisions 4–5 + Bot threads): `install.py` pairs managed hook groups by identity (`matcher` + managed-script set), replaces in place, drops stale identities, appends new ones; reversed-order reinstall is a byte/mtime/backup no-op (79e88d81). The installer snippet `snippets/CLAUDE_CONTEXTDB.md` and the recovery-packet commands use `uv run --no-project .claude/hooks/contextdb_cli.py` with `uv` documented as a prerequisite of the generated commands (6f7dfdb2, 634cb327; T83's CLAUDE.md block therefore survives the next install). Health retention runs before any event mutation in both the explicit `prune` and the SessionEnd pass; the health log and `append_jsonl` share an exclusive `flock` and the emptied log keeps its inode (634cb327). POSIX-only contract (Linux/macOS): `fcntl` imported inside the two locking functions with a clear `RuntimeError` on other platforms and no unlocked fallback, import regression test, README/CHANGELOG statements (9f9b26f4).
- Round 2 (PONG decisions 6–7): docstring restored above the lazy import (f6c47e8a); the quarantine sweep tolerates only `FileNotFoundError` per entry when a concurrent pruner removed it, other `OSError`s propagate, regression covers stat race, unlink race and a PermissionError that must still fail (a536af5b). Project copy byte-identical to the vendor tree for all seven runtime modules at a536af5b (orchestrator `cmp`).
- PONG decision 3: the worktree's 28 untracked artifact copies from T77b/T86/T90/T90b (all byte-identical to main b63b8202, hashes pasted in the validation) were archived under `/tmp` and removed so `origin/main` could be merged.
- Project copy parity at the head: `cli.py`, `config.py`, `hook.py`, `paths.py`, `storage.py` and the four `.claude/hooks/*.py` scripts byte-identical to the vendor tree (orchestrator `cmp`); `.claude/settings.json` untouched.

## Orchestrator re-derivation

- Read the full diff (vendor runtime, installer, docs, tests, receiver, manifest, unit tests). Refutation attempts: `NOT IN` orphan delete under-deletes on NULL session ids (safe direction); the positional installer replacement removes surplus managed groups and appends missing ones; the retention bound `>= today.toordinal()` is exactly the `datetime - timedelta` overflow edge; `O_NOFOLLOW` on a symlinked health log raises `ELOOP`, which the explicit `prune` surfaces as exit 2 and the SessionEnd pass swallows (pre-existing `except Exception: pass`).
- Observation (not a finding against the task): `ensure()` now also refuses a symlinked `.claude` directory itself, and the SessionEnd hook then fails silently; no such project exists here. Carry as a vendor note in the next CompactionDB change.
- CI 13/13 pass on b9acaa39; mergeable `clean` after the orchestrator resolved the three Bot threads with `fixed:b9acaa39` (fix verified in the diff before replying); `bot: none` on the final head after the 900-second wait.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, b9acaa39 (round-0 head) | incorrect (1) → P2 `install.py:88` managed hook groups paired positionally in fragment order, so an existing `[compact, unrelated, *]` SessionStart list is reordered on reinstall (objective 2); orchestrator reproduced the premise (fragment has two managed SessionStart groups; the live project order equals the fragment order, so no deployed impact) → revise round 1 (identity-matched replacement + reversed-order regression test) |
| task-level, final head a536af5b (round 2) | correct → no actionable findings; auditor independently verified 69 manifest hashes, 19 runtime mirrors, ancestry and diff cleanliness; 108 vendor tests, 10 release checks, 12 CI checks, 8 resolved Bot threads matching the feedback JSON |

Bot threads (all replied to and resolved by the orchestrator after verifying each fix in the diff): round 0 — 4180373615/21/23 `fixed:b9acaa39`; round 1 — 4180596831 (health validation before commit), 4180596834 (`uv` prerequisite documented), 4180596837 (append/prune lock) `fixed:634cb327`; 4180772171 (Windows `fcntl` import, P1) `fixed:9f9b26f4`; round 2 — 4180970545 (vanished quarantine entry) `fixed:a536af5b`.

- Sweep (final head a536af5b): `.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-pr-feedback.json`, 33 items: 8 × `fixed:` (b9acaa39 ×3, 634cb327 ×3, 9f9b26f4, a536af5b), 25 × `not-applicable` (orchestrator reply comments, 12 Codex review containers, CodeRabbit summary and status, 3 macOS capacity notices).
- Crit evidence `…-crit.json` (one resolved review-scope record) and receipt `…-review-receipt.md`; worker-side `…-worker-crit.json` (6 resolved records, reviewer codex) and `…-worker-review-receipt.md` copied from worker-e.

## Follow-ups

- Operator: after `make update` deploys 2.0.0+dotfiles.9 on each host, run `/hooks` in Codex and trust the three CompactionDB hooks plus the permgate hook (T82 record sequencing now satisfied); T87 leg 2 verifies `/compact` rows.
- T82b: hook `trusted_hash` pins and the ponytail refresh.
- Vendor note for the next change: symlinked `.claude` directory behaviour (observation above).

## CompactionDB

- Worker decision: none (Codex seat cannot write the main-checkout DB; PONG decision 2). Orchestrator consolidation `57b2c6d5-4471-42ea-8b37-88ce9e4d3e3a`.
