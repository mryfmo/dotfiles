# AGMSG-TASK dotfiles-T81-compactiondb-vendor-a01

Drafted 2026-10-05 by the orchestrator seat from the approved correction plan (Phase 5, dotfiles-T81). Depends on T77 (merged 67451fc6). Shares `home/dot_agents/agent-config.yaml` and `scripts/validate-agent-assets.py` with T90 (Codex security seat, in flight) and `scripts/validate-agent-assets.py` with T80; dispatch after T90 merges, serialized against T80.

## Objective

Principle 7: CompactionDB records Codex lifecycle events with a real event type and session id, and the ledger stays bounded.

1. **Notify payload normalisation** (`vendor/compactiondb/.claude/contextdb/contextdb/normalize.py`, `normalize_hook_payload`): a payload without `hook_event_name` whose `type` is `agent-turn-complete` (Codex `notify`) maps to the `Stop` hook name (`event_type` `turn_stop`), `session_id` from `thread-id`, `agent_id` from `client`, and `last-assistant-message` carried as `last_assistant_message` in the normalised record. Existing Claude payloads are unchanged. VERIFY the Codex `notify` payload field names against the official Codex config reference and paste the source.
2. **Bounded ledger** (`vendor/compactiondb/.claude/contextdb/contextdb/storage.py`): (a) the explicit `prune` CLI path only: after deleting expired rows, `VACUUM` when `freelist_count * page_size > 64 MiB`; (b) new config key `capture.max_db_bytes` (default 512 MiB): when the database file exceeds it, delete the oldest events until it fits, then `VACUUM`. Neither runs inside the SessionEnd hook's ingest transaction or its timeout; both run only from `contextdb_cli.py prune`.
3. **Vendor tests** (`vendor/compactiondb/tests/**`): the Codex payload case (both fields and the `unknown` fallback no longer hit), the VACUUM threshold and the size cap (small fixtures with a tiny `max_db_bytes`).
4. **Release bookkeeping:** `vendor/compactiondb/CHANGELOG.md` entry; regenerate `vendor/compactiondb/MANIFEST.sha256` with the vendor `Makefile` target (VERIFY its name; paste the command); `home/dot_agents/agent-config.yaml` `assets.compactiondb.pin: 2.0.0+dotfiles.7` (the `verify: manifest-sha256` contract; not an upstream bump).
5. **Project copy:** refresh `.claude/contextdb/contextdb/**` and `.claude/hooks/contextdb_*.py` in this repository from the vendor tree with `compactiondb-install .` (or the documented equivalent; paste the command). Add a parity check to `scripts/validate-agent-assets.py`: every file under the project `.claude/contextdb/contextdb/` and the two hook scripts must be byte-identical to the vendor copy (fail with the differing path).
6. `make render-check`, `make validate-agent-assets`, `make unit-test`, `uv run python -m unittest discover -s vendor/compactiondb/tests` all pass. Live check in your worktree (paste): `printf '%s' '{"type":"agent-turn-complete","thread-id":"t1","cwd":"'"$PWD"'","last-assistant-message":"x"}' | python3 .claude/hooks/contextdb_cli.py --project-root . ingest --ingested-from codex` then `sqlite3 .claude/contextdb/state/context.db "select event_type,session_id from events where ingested_from='codex' order by id desc limit 1"` → `turn_stop|t1`; `python3 .claude/hooks/contextdb_cli.py prune` exits 0.

Forbidden: `.claude/settings.json`; gitignoring the project copy; changing hook wiring or the Claude-side event mapping; the `notify` profile entries in `agent-config.yaml` (T82 adds the Codex hooks); any secret in test fixtures.

[memory:decision] dotfiles-T81 (operator 2026-10-03): CompactionDB normalises the Codex `notify` payload (`agent-turn-complete` → `Stop`/`turn_stop`, `thread-id` → session, `client` → agent), bounds the ledger (`capture.max_db_bytes` 512 MiB, VACUUM over 64 MiB of free pages, both only on the explicit `prune`), ships as vendored `2.0.0+dotfiles.7`, and the project copy is validated byte-identical to the vendor tree.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/compactiondb-codex-ingest --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `vendor/compactiondb/**` (normalize.py, storage.py, tests, CHANGELOG.md, MANIFEST.sha256; the Makefile only if the manifest target needs a fix), `.claude/contextdb/contextdb/**` and `.claude/hooks/contextdb_*.py` (project copy, refreshed by the installer only), `home/dot_agents/agent-config.yaml` (`assets.compactiondb.pin` only), `scripts/validate-agent-assets.py` (the parity check), `tests/unit/test_validate_agent_assets.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T81-compactiondb-vendor-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
make validate-agent-assets
uv run python -m unittest discover -s vendor/compactiondb/tests 2>&1 | tail -3
make unit-test 2>&1 | tail -3
git ls-files -z "*.py" | xargs -0 mise x ruff -- ruff format --config ruff.toml --check
sha256sum -c vendor/compactiondb/MANIFEST.sha256 --quiet; echo "rc=$?"
<the item-6 live check>
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, the VERIFY sources.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T81` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=40.

## Dispatch

- 2026-10-05 05:10Z to `claude-standard-dot-a005` (worker-c, wT:p2) after T79 merged as 62d0771f (manifest and validator free; T77, T80 on main). Branch from `origin/main` 62d0771f or later with `--no-track`. T82 and T84 queue behind this PR on the shared manifest and validator. Reminder from T80: SessionEnd hooks are capped at 3 seconds, so the SessionEnd handler must never run prune; this task keeps pruning on the explicit CLI path only.

## Revise round 1 (orchestrator, 2026-10-05 06:25Z) — task-level audit of 8c8cf691 is `incorrect` (7; three reproduced defects)

Code, one commit (vendor tree first, then refresh the project copy with the installer and regenerate the manifest; `make manifest`, `sha256sum -c` rc 0):

1. **P1, optimize before deciding (over-deletion).** `enforce_size_cap` measures in-use pages that still include dead FTS segment pages, so it deletes far more events than the cap requires (auditor: 1,000 events, 3,500,000-byte cap → all 1,000 deleted; optimizing between batches keeps 300). Run the FTS `optimize` (when the tokenizer is not `none`) **before** the first size check and again after each deleted batch, before re-measuring; stop as soon as in-use pages fit. Correct the `ponytail:` ceiling comment (the 99-event overshoot claim was wrong under FTS).
2. **P2, VACUUM decision independent of the cap counter.** In `cli.py` `prune`, decide the VACUUM from the file state after retention and cap: `vacuum_if_fragmented` with `force=True` whenever the file size (`page_count * page_size`) still exceeds `max_db_bytes` **or** any events were deleted by either path, else the 64 MiB free-page threshold (auditor: 720,896-byte cap left 2,367,488 bytes with `capped=0`, `vacuumed=False`).
3. **P2, optimize when retention emptied the table.** The FTS optimize must also run when `prune_expired` (or candidate cleanup) removed rows and the cap then found nothing to delete (`removed == 0`); auditor: zero events still occupied 2,744,320 bytes against a 1,000,000-byte cap, optimize + VACUUM → 204,800. Simplest: in `prune`, optimize once after retention and once after the cap when either removed rows, then VACUUM per item 2.
4. **Tests (vendor `test_storage`/`test_cli`):** reproduce the three auditor scenarios with small fixtures and assert the new outcomes (partial retention under FTS; VACUUM after retention-only shrink; optimize+VACUUM after retention empties the table). Keep the existing cases green.
5. **Evidence:** paste the timestamped Bot-wait loop output (start, each poll, end) for the final head; paste the task's vendor-test command output once more and the `make -C vendor/compactiondb test` output (both; the import failure is pre-existing and accepted).

Accepted without change (dispositioned at acceptance): `tests/unit/test_asset_manifest.py` literal edit; the installer's reorder of `.claude/settings.json` (restored; vendor follow-up); the unsandboxed installer run (record it in the sandbox file as a deviation with the denied write). Then `gh pr update-branch 268` if `main` moved, CI, Bot wait on the new diff head (15 min, timestamped), RESULT.
