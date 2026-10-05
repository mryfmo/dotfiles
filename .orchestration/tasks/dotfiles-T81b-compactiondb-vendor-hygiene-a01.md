# AGMSG-TASK dotfiles-T81b-compactiondb-vendor-hygiene-a01

Drafted 2026-10-05 by the orchestrator seat from the T81 acceptance follow-ups and the final T81 audit finding. Depends on T81 (PR #268). Shares the vendor tree, the project copy and the validator with nobody in flight once T81 merges; disjoint from T82/T84 except `home/dot_agents/agent-config.yaml` (the compactiondb pin) — dispatch after T82 and T84 merge, or restrict the pin bump to a separate commit if dispatched earlier.

## Objective

Vendor CompactionDB release 2.0.0+dotfiles.8: the loose ends T81 left.

1. **Orphaned session rows under the cap** (`storage.py` `enforce_size_cap`): before deleting any newer event, delete `sessions` rows of the project that no longer have events (`session_id NOT IN (SELECT DISTINCT session_id FROM events WHERE project_id=?)`), and repeat after each deleted batch; a vendor test reproduces the auditor's shape (many distinct thread ids, a cap below the session-metadata footprint, zero events) and asserts the rows are reclaimed before newer events are evicted.
2. **Installer idempotency** (`vendor/compactiondb/install.py --project`): never reorder existing hook entries in the project's `.claude/settings.json` and never leave a backup file when nothing changed; a vendor test runs the installer twice on a fixture settings file and asserts byte identity.
3. **Vendor suite from the repository root:** make `uv run python -m unittest discover -s vendor/compactiondb/tests` work from the repository root (package import path), or document the `make -C vendor/compactiondb test` entry as the only supported one in the vendor README and the task template; `validate.py`'s `unittest_suite` regex accepts the real unittest summary line.
4. CHANGELOG entry, `make manifest`, manifest pin `2.0.0+dotfiles.9` (T82 round 1 took `.8`), project copy refreshed, parity check green.

Forbidden: `.claude/settings.json`; hook wiring; the Claude-side event mapping; profile `notify` entries.

[memory:decision] dotfiles-T81b (orchestrator 2026-10-05): CompactionDB 2.0.0+dotfiles.8 reclaims orphaned session rows under the size cap before evicting newer events, installs idempotently into a project's `.claude/settings.json`, and its vendor suite runs from the repository root.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c fix/compactiondb-vendor-hygiene --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.

## Allowed files

- `vendor/compactiondb/**`, `.claude/contextdb/contextdb/**` and `.claude/hooks/contextdb_*.py` (installer output only), `home/dot_agents/agent-config.yaml` (`assets.compactiondb.pin` only), `tests/unit/test_asset_manifest.py` (the version literals), `tests/unit/test_validate_agent_assets.py` if the parity check needs a case
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make -C vendor/compactiondb test 2>&1 | tail -3
uv run python -m unittest discover -s vendor/compactiondb/tests 2>&1 | tail -3
sha256sum -c vendor/compactiondb/MANIFEST.sha256 --quiet; echo "rc=$?"
make render-check; make validate-agent-assets; make unit-test 2>&1 | tail -3
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only, timestamped); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T81b` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=30.

### Items added from T82 (orchestrator, 2026-10-05 09:00Z)

5. `project_paths.ensure()` refuses symlinked `state`, `spool` and `health` children under `.claude/contextdb` (Codex P2 4179789825 on PR #269), with a vendor test.
6. The receivers (`notify` and the hooks) find the opt-in for a session cwd below the repository root by walking up to the git top level (Codex P2 4179789828 on PR #269), with a wrapper test; document the lookup in the wrapper's shdoc.
7. The explicit `prune` also performs the health-artifact retention (`errors.jsonl`, `spool/quarantine` by `operations.error_log_retention_days`) so it no longer depends on which runtime's SessionEnd hook ran (Codex P2 4179926397 on PR #269); item 5's `ensure()` hardening binds the storage paths with no-follow semantics atomically with their creation (Codex P2 4179926400).

### Sequencing (orchestrator, 2026-10-05 09:50Z)

This task must merge and deploy (`make update`) **before** the operator trusts the three T82 Codex hooks in `/hooks`: until then the hooks do not run, so the race the T82 audit named (walk vs. `ensure()`) has no exposure. Item 5 is therefore the first item to implement, with a test that creates the storage directories through file descriptors / no-follow semantics and rejects a path swapped for a symlink.

## Dispatch

- 2026-10-05 11:30Z to `codex-security-dot-a007` (worker-e, wT:p8) after T84 merged as 51c57f19 (manifest pin free; T82 vendor 2.0.0+dotfiles.8 on main, so this release is `.9`). Branch from `origin/main` 51c57f19 or later with `--no-track`. Runs in parallel with T83 (a005, prose only). Item 5 (no-follow storage binding in `project_paths.ensure()`) first; it gates the operator trust step for the T82 hooks. Artifacts in your worktree; the orchestrator transfers them. Bot wait on the diff head only.

### PONG decision (orchestrator, 2026-10-05 11:45Z) — item 5 contract

Option (a): item 5 is **atomic no-follow directory construction** (`dir_fd`, `O_NOFOLLOW`, `mkdir`/`open`/`fchmod` relative to the opt-in directory fd, so a symlink swapped in during construction is never followed), with an **explicit, documented residual**: once `ensure()` returns, the storage paths and `sqlite3.connect` reopen by name, and portable stdlib SQLite cannot be bound to a directory fd, so a same-user process that swaps a storage directory *after* construction is outside what this release closes. State that residual in the CHANGELOG entry, the vendor README and the T82 receiver's shdoc ("the receiver's walk plus the vendor's no-follow construction close the pre-construction races; the post-construction swap by a same-user process remains"). Do not relocate CompactionDB state outside the workspace in this task (a design change the orchestrator would plan separately with the operator; note it as a candidate in the report). Tests: the race-shape tests cover construction (swap before/during `ensure()` is refused); no test claims the post-construction case. Proceed with the other items.

### PONG decision 2 (orchestrator, 2026-10-05 11:55Z) — allowed files for item 6

Allowed files gain `home/dot_local/bin/common/executable_contextdb-codex-notify` and `tests/unit/test_contextdb_codex_notify.py` (item 6, the enclosing-project opt-in lookup, and the receiver's shdoc residual sentence from decision 1), plus your `.orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-worker-crit.json` and `…-worker-review-receipt.md` (in your worktree; the orchestrator transfers them). The main-checkout CompactionDB `memory add` stays orchestrator-owned.

### PONG decision 3 (orchestrator, 2026-10-05 12:00Z) — worktree artifacts vs. the boundary commit

Authorized: the untracked `.orchestration` copies of your earlier tasks (T77b, T86, T90, T90b) in worker-e were already transferred and are now tracked by boundary commit b63b8202; archive them under `/tmp` (or your scratch root) and remove them from the worktree so `git merge origin/main` (or `gh pr update-branch 275`) succeeds. Keep only this task's own artifacts in the worktree. This housekeeping is a standing permission for a Codex seat whenever a boundary commit lands.

## Revise round 1 (orchestrator, 2026-10-05 03:30Z) — audit of head b9acaa39: `incorrect` (1 finding)

- **[P2] `vendor/compactiondb/install.py:88` — managed hook groups are replaced in fragment order, not matched to their existing identities.** Reproduced by the auditor: an existing `SessionStart` list `[compact, unrelated, *]` becomes `[*, unrelated, compact]` on reinstall, which violates objective 2 (existing positions preserved) and causes a needless settings rewrite plus backup. The live project here has `[*, compact]`, the fragment order, so no deployed impact, but the contract must hold for any existing layout.
- **Fix:** in `merge_settings`, pair each existing managed group with the fragment group of the same identity (the `matcher` value, `None` included, plus the managed command set is a sufficient key), replace it in place, drop managed groups whose identity no longer exists in the fragment, and append fragment groups with no existing counterpart at the end. Add a regression test in `vendor/compactiondb/tests/test_install.py` where the existing managed groups are in reversed order with an unrelated group between them: a reinstall must leave bytes, mtime and the backup set unchanged. Keep the no-op invariant test green.
- **Housekeeping:** CHANGELOG `2.0.0+dotfiles.9` entry wording stays (no version bump; .9 is unreleased), regenerate `MANIFEST.sha256`, refresh the project copy if any runtime module changes (installer-only changes leave the runtime copy as is), run the vendor suite from both entry points, push, `gh pr checks --watch`, the 15-minute Bot wait on the new head, then `AGMSG-RESULT v1 … round=1` with the new head. Same allowed files; artifacts appended, not rewritten.

### PONG decision 4 (orchestrator, 2026-10-05 03:45Z) — round 1 scope addition: `uv run --no-project` wording in the vendor's generated text

The Codex Bot on PR #274 (T83, docs) found that `uv run .claude/hooks/contextdb_cli.py …` synchronises a target project's own environment before invoking the stdlib-only CLI; the agreed form is `uv run --no-project .claude/hooks/contextdb_cli.py …` (the Claude-side enforce-uv hook denies bare `python3`). T83 changes the hand-written docs; the installer-generated text is yours, in this round:

- `vendor/compactiondb/snippets/CLAUDE_CONTEXTDB.md` (the CLAUDE.md managed block, otherwise the next `compactiondb-install` rewrites T83's `uv run` lines back to `python3`): every `python3 .claude/hooks/contextdb_cli.py` → `uv run --no-project .claude/hooks/contextdb_cli.py`.
- `vendor/compactiondb/.claude/contextdb/contextdb/recovery.py` recovery-packet "Verification commands" text: the same substitution; refresh the project copy (parity) and `MANIFEST.sha256`; a CHANGELOG line under the .9 entry.
- Add `vendor/compactiondb/snippets/CLAUDE_CONTEXTDB.md` to `allowed_files`. Keep the vendor and unit suites green; include this in the round-1 push (or a follow-on push if 79e88d81 already finished CI; the Bot wait then runs on the newest head).

### PONG decision 5 (orchestrator, 2026-10-05 04:45Z) — platform contract (Bot P1 4180772171 on merge head 3d478877)

Decision: **POSIX-only release contract, option (a).** The dotfiles target is Linux and macOS; the approved `dir_fd`/`O_NOFOLLOW` construction (PONG decision 1) is already POSIX-only, so `fcntl` locking follows the same contract. No native Windows implementation.

- Move `import fcntl` out of module scope in `hook.py` and `util.py` into the functions that lock (`prune_health_artifacts`, `append_jsonl`), so importing `contextdb.*`, `--help` and non-locking commands keep working on any platform; on a platform without `fcntl`, the locking call raises a clear `RuntimeError("ContextDB health-log locking requires a POSIX platform")` (do not fall back to unlocked writes).
- Regression test: importing `contextdb.hook` and `contextdb.util` with `fcntl` absent from `sys.modules` (inject `None`/`ImportError` via `unittest.mock.patch.dict`) succeeds, and the locking function raises the clear error in that state.
- README (vendor) and CHANGELOG .9: one sentence each declaring the runtime POSIX-only (Linux/macOS) as of dotfiles.9, replacing or qualifying any Windows example; the installer and runtime copies refreshed (parity), `MANIFEST.sha256` regenerated.
- Then push, CI, Bot wait on the new diff head (this is a code change, not a base-only merge), `AGMSG-RESULT v1 … round=1`. Same allowed files.

### PONG decision 6 (orchestrator, 2026-10-05 04:52Z) — one correction to 9f9b26f4 before RESULT

In `prune_health_artifacts` (vendor `hook.py` and the project copy) the new `try: import fcntl` block was inserted above the function's docstring, which turns the docstring into a bare string expression. Move the import block below the docstring (first statement after it), refresh parity and `MANIFEST.sha256`, push, and let CI and the Bot wait run on that head; then `AGMSG-RESULT v1 … round=1`. The P1 thread 4180772171 is already resolved by the orchestrator as `fixed:9f9b26f4`.

## Revise round 2 (orchestrator, 2026-10-05 05:17Z) — carries PONG decision 6 only

Your round-1 RESULT for 9f9b26f4 arrived before PONG decision 6 (message 1368, sent 04:49Z) was read. Round 2 is exactly that decision: move the `try: import fcntl` block below the `prune_health_artifacts` docstring (vendor `hook.py` and the project copy), refresh parity and `MANIFEST.sha256`, push, CI, Bot wait on the new diff head, then `AGMSG-RESULT v1 … round=2`. No other change. The orchestrator's review of 9f9b26f4 found nothing else; sweep and audit run on the round-2 head.

### PONG decision 7 (orchestrator, 2026-10-05 05:32Z) — round 2 scope extension for Bot P2 4180970545 (thread PRRT_kwDOSMyAV86o6fwH on f6c47e8a)

Approved as proposed: in the quarantine sweep of `prune_health_artifacts`, tolerate only `FileNotFoundError` from `stat()`/`unlink()` on an individual entry (a concurrent pruner or hook removed it first) and continue with the next entry; every other `OSError` still propagates. Regression test: an entry that disappears between the directory listing and its `stat()`/`unlink()` (patch `Path.stat` or `os.unlink` to raise `FileNotFoundError` once) leaves `prune` exiting 0 with the remaining expired entries removed. Refresh the project copy (parity) and `MANIFEST.sha256`, push, CI, Bot wait on the new diff head, then `AGMSG-RESULT v1 … round=2`. The orchestrator resolves the thread as `fixed:<sha>` after verifying the diff.
