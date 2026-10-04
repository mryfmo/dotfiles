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
