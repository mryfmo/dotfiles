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
