# Acceptance: dotfiles-T76-ineffective-settings-a01

- **Decision:** ACCEPTED. PR #257 squash-merged to `main` as `40993f20`; final head `26a882ac73b1c31f4e26664f310ea68bc332595b`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, one disposition below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 15:17Z).
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev matched at dispatch and after the revise-round append.
- **Exemption declared:** acceptance and final integration (thread replies after fix verification, sweep, evidence, audit invocation, gate, merge, ACCEPTANCE).
- **Plan reference:** Phase 4, dotfiles-T76 (principle 9: configuration with no effect is deleted). Depends on T71 (merged 65915b93); serialized after T72 (shared `agent-config.yaml`/validator).

## What was accepted (PR #257, final head `26a882ac73b1c31f4e26664f310ea68bc332595b`; commits 526dd18b, f2db43f9, f805ee3a update-branch onto 04bce61b, 26a882ac)

- `enabledPlugins: {}` removed from the manifest, from `render_claude_settings` and from the rendered `claude-settings-managed.json`; `modify_private_settings.json` keeps a runtime `enabledPlugins` key (current-only keys survive), pinned by a new merge test.
- `mcp_servers: {}`: the six never-enabled servers (context7, filesystem_dotfiles, github, time, sequential_thinking, playwright) are gone; the Codex template renders no `[mcp_servers.*]` table, `private_mcp.json.tmpl` renders `{"mcpServers": {}}`; `validate_claude_mcp_config` accepts an empty mapping and rejects a non-mapping; `validate_mcp_parity` passes on empty maps; `DEPRECATED_MCP_PACKAGES` stays.
- gwq `[claude]`, `[claude.execution]`, `[claude.queue]`, `[claude.worktree]` deleted (nothing reads the queue directory); `[finder]` kept.
- Revise round 1 (f2db43f9): `modify_private_config.toml` gains `RETIRED_MCP_SERVERS` (the six names, T76 comment) and `merge_config` drops a current-only `[mcp_servers.<retired>]` chunk that carries `enabled = false`; a re-enabled or re-added table is kept. Test: the five disabled retired tables disappear, a re-enabled `context7` and an unknown disabled `private_server` survive. Simulated merge of the new baseline into the 2ad504e3 baseline leaves zero MCP tables (was six).

- Revise round 2 (26a882ac, after the task-level audit of f805ee3a reproduced two defects): a purged retired parent takes its current-only child tables (`[mcp_servers.<retired>.env]`, …) with it, and enablement is read from `tomllib.loads(chunk)` (an unparseable chunk is kept; `tomllib` imported guardedly, so a Python < 3.11 interpreter purges nothing); the regex and the `re` import are gone. Test extended: disabled `github` with an `.env` child disappears together, re-enabled `context7` with `enabled = false` inside a string value is kept with its child, unknown `private_server` kept.

## Decisions taken during the rounds

- Codex P2 4177937781 (retired tables persist in `~/.codex/config.toml`) was a real convergence gap, not `not-applicable` as the worker proposed: the orchestrator's live Codex config held all six tables; purging in the merge script keeps both hosts converging without operator hand edits. Allowed files were extended to the Codex merge script and its test (a Codex-only rendering source, so a Claude seat may edit it).
- Codex P2 4178090831 (keep customised disabled copies under a retired name): not applicable. While managed, every apply replaced those tables wholesale with the disabled baseline chunk, so no customised copy exists on a converged machine; the purge needs the full table name plus `enabled = false`, and a re-enabled table is kept. Residual by design: a user who later defines a *disabled* custom server under one of the six retired names loses it on apply; a disabled server has no effect, and the names are documented in the constant.

## Orchestrator re-derivation

- Read the full diff against the merge base (10 files, +40/−274 before the rounds; +25/−0 in f2db43f9; the round-2 diff in full: `retired_and_disabled`, the `purged` set computed over current-only chunks, and the child-prefix filter) and the merge-script change in context of `merge_config` (the drop sits in the current-only branch after managed and runtime tables are emitted, so managed and runtime behaviour is untouched).
- Confirmed `grep -c mcp_servers` on the rendered Codex template is 0 at the head, `rc=1` for `gwq/claude` across home/scripts/tests, and that both fix commits are ancestors of f805ee3a before replying on and resolving the threads.
- CI 13/13 green on 26a882ac; branch up to date with `main` 04bce61b (no update-branch needed); PR `clean`; no `.orchestration` file in the PR.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, f805ee3a (round-1 head) | incorrect (2) → both fixed in 26a882ac |
| task-level, final head 26a882ac | incorrect (1) → disposition below |

audit-finding: 1 the child-table purge compares raw header text, so a hand-written `[mcp_servers."github".env]` child survives a purged `[mcp_servers.github]` parent → not-applicable:raw header comparison is this merge script's pre-existing convention for every table match (managed names, runtime prefixes, current-only chunks all compare `table_name()` text, so a quoted-key header never matched its unquoted managed twin before T76 either); the managed baseline only ever wrote unquoted headers, so no converged `~/.codex/config.toml` holds a quoted retired child, and canonicalizing TOML key segments in one comparison alone would make the script inconsistent with itself; a script-wide canonicalization is a separate change class, not part of deleting ineffective settings

- Codex Bot: two threads, 4177937781 `fixed:f2db43f9` (reply 4178118066) and 4178090831 `not-applicable` (reply 4178118166), both resolved by the orchestrator; the final head 26a882ac got a Bot thumbs-up at 14:59:13Z and no new thread.
- Sweep (head 26a882ac): 13 items, 1 `fixed:f2db43f9`, 12 `not-applicable` (the second thread, CodeRabbit summary/status, two Codex and two own review containers, two own replies, three macOS capacity notices). Masked copy: `.orchestration/validation/dotfiles-T76-ineffective-settings-a01-pr-feedback.json`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Live follow-up

- The next `make update` on each host runs the purge; verify with `grep -c '^\[mcp_servers\.' ~/.codex/config.toml` → 0 (orchestrator host after its next `make update` in the canonical clone).

## CompactionDB

- Worker decision `ebdd360d-0bea-450e-a842-23f0313655aa`; orchestrator consolidation `25fcff88-cc71-4a05-ab5b-11c9e19200f0`.

## Live verification (orchestrator host, 2026-10-04 16:05Z)

- `make update` in the canonical clone at f6320f37 (exemption: machine-state deploy, no repository diff): `grep -c '^\[mcp_servers\.' ~/.codex/config.toml` → 0 (was 6). The purge converged this host without a hand edit.
