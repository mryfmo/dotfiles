# AGMSG-TASK dotfiles-T82-codex-compaction-hooks-a01

Drafted 2026-10-05 by the orchestrator seat from the approved correction plan (Phase 5, dotfiles-T82). Depends on T80 (merged 36ffe6ca) and T81 (PR in flight). Shares `home/dot_agents/agent-config.yaml` with T84; dispatch after T81 merges, serialized against T84.

## Objective

Principle 7: Codex compaction and session end reach CompactionDB like Claude's do.

1. **Manifest** (`home/dot_agents/agent-config.yaml`, the `codex.hooks` block): add `command_hooks` with three entries, each `command: '{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify'` and `status_message: Recording to CompactionDB`: `PreCompact` (timeout 10), `PostCompact` (timeout 10), `SessionEnd` (timeout 3, the Codex cap verified in T80). The `permission_request` entry and `hooks.state` stay as they are; the profiles' `notify` entries stay (they carry the assistant message).
2. **Wrapper** (`home/dot_local/bin/common/executable_contextdb-codex-notify`): hooks deliver the payload on stdin while `notify` passes it as `$1`; read `payload="${1:-$(cat)}"` and keep everything else (cwd opt-in check, the ingest call with `--ingested-from codex`, exit 0 on failure with the stderr line). The SessionEnd path must not run `prune` or anything else beyond the ingest (3-second budget; T81 keeps pruning on the explicit CLI). shdoc comments updated.
3. **Rendered** `home/.chezmoitemplates/codex-config-managed.toml` follows via the generator (`make render-check` clean after regeneration): three `[[hooks.<Event>]]` tables with `matcher = "*"`.
4. **Tests:** the wrapper's unit tests cover argv and stdin payloads and a payload with `hook_event_name: PreCompact`; `tests/unit/test_generate_agent_configs.py` or `test_validate_agent_assets.py` pin the three manifest entries if a fixture mirrors the manifest.
5. **Live check (this host, in your worktree, paste):** after `make render-check`, simulate a hook delivery: `printf '%s' '{"hook_event_name":"PreCompact","session_id":"t82","cwd":"'"$PWD"'"}' | bash home/dot_local/bin/common/executable_contextdb-codex-notify; echo "rc=$?"` then `sqlite3 .claude/contextdb/state/context.db "select event_type,session_id,ingested_from from events order by id desc limit 1"` → `pre_compact|t82|codex`. The real Codex-session `/compact` leg on both hosts is the operator's live E2E (T87) and is not performed here; say so in the report.

Forbidden: profile `notify` entries; the project `.codex/hooks.json`; the vendor tree (T81); any Claude hook; permgate; the `.claude/settings.json`.

[memory:decision] dotfiles-T82 (operator 2026-10-03): Codex PreCompact, PostCompact and SessionEnd hooks are declared in the manifest's `codex.hooks.command_hooks` (SessionEnd within the 3-second Codex cap) and rendered into the managed Codex config; `contextdb-codex-notify` accepts the payload on stdin or argv and only ingests, so Codex compaction and session end land in CompactionDB with a real event type and session id.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/codex-compaction-hooks --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the `codex.hooks.command_hooks` list only), `home/dot_local/bin/common/executable_contextdb-codex-notify`, `home/.chezmoitemplates/codex-config-managed.toml` (generator output only), `tests/unit/**` where they cover the wrapper or mirror the manifest hooks
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T82-codex-compaction-hooks-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
make validate-agent-assets
grep -c '^\[\[hooks\.\(PreCompact\|PostCompact\|SessionEnd\)\]\]' home/.chezmoitemplates/codex-config-managed.toml
shellcheck home/dot_local/bin/common/executable_contextdb-codex-notify; mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_contextdb-codex-notify
make unit-test 2>&1 | tail -3
<the item-5 live check>
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T82` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=30.

## Dispatch

- 2026-10-05 07:10Z to `claude-standard-dot-a006` (worker-d, wY:p2) after T81 merged as 2527be54 (vendor 2.0.0+dotfiles.7 on main; T80 renderer on main). Branch from `origin/main` 2527be54 or later with `--no-track`. T84 queues behind this PR on the shared manifest.

### PONG decision (orchestrator, 2026-10-05 07:55Z) — Codex hook trust and PostCompact

1. **P1 4179558230 (non-managed hooks need one-time trust):** option (a). The three hooks ship as manifest/config hooks; the operator trusts them once per machine in Codex `/hooks` after `make update`, which also covers the existing permgate `PermissionRequest` config hook that has no `hooks.state` entry today. Add one paragraph to README's operator phase (README joins allowed_files for that paragraph only): after `make update`, open Codex, run `/hooks`, trust the four config hooks (three CompactionDB, one permgate), confirm `[hooks.state]` in `~/.codex/config.toml` gained entries for them; the generator's merge keeps those runtime entries across later applies. Do not derive the hash or pre-seed `hooks.state`; do not use `requirements.toml`. Reply on the thread is the orchestrator's; disposition `not-applicable` with the documented operator step, and a follow-up task (hook trust-state pins: record the trusted keys in `codex.hooks.state` and refresh the drifted ponytail hashes) is noted in the report.
2. **P2 4179558226 (PostCompact payload has no summary):** not applicable; keep PostCompact as a timeline marker (the vendor skips empty summaries, no empty memory is created). No transcript extraction.

Then push (one commit for the README paragraph, no code change needed unless CI says otherwise), CI, Bot wait on the diff head (timestamped), RESULT.

## Revise round 1 (orchestrator, 2026-10-05 08:05Z) — task-level audit of 7ee91087 is `incorrect` (2)

1. **P2, ingest is not ingest-only.** `contextdb_cli.py ingest` calls `process_payload()`, which runs `prune_expired()` and the log/quarantine cleanup (`hook.py:29-54`), so the SessionEnd hook does maintenance inside Codex's 3-second budget and a kill mid-transaction can lose the event. Allowed files gain the vendor tree for this: add an `ingest --no-maintenance` option to `vendor/compactiondb/.claude/contextdb/contextdb/cli.py` (skip `prune_expired` and the file cleanup; ingest and commit only), vendor test for it, CHANGELOG entry `2.0.0+dotfiles.8`, `make manifest`, manifest `assets.compactiondb.pin: 2.0.0+dotfiles.8`, `tests/unit/test_asset_manifest.py` literals, project copy refreshed with `install.py --project . --skip-instructions` (restore `.claude/settings.json` if the installer reorders it), parity check green. The wrapper passes `--no-maintenance` on every delivery (hook and `notify` alike; retention stays on the explicit `prune` and on Claude's own SessionEnd hook). Set the receiver's subprocess timeout to 2 seconds so it returns inside the 3-second hook budget. Correct the report's "never prunes" sentence to the new behaviour. T81b moves to `2.0.0+dotfiles.9`.
2. **P3, negative control.** Paste the regression test run without `-I` (the failing output) and with it (passing) in the validation file.

Then push, CI, Bot wait on the new diff head (timestamped), RESULT; `gh pr update-branch 269` only if `main` moved.

### PONG decision (orchestrator, 2026-10-05 08:15Z) — project copy

Option (a): copy `cli.py` and `hook.py` from `vendor/compactiondb/.claude/contextdb/contextdb/` into `.claude/contextdb/contextdb/` yourself (the installer's hooks/settings writes are not needed; the parity check proves byte identity and `.claude/hooks/contextdb_*.py` are already identical). Record in the sandbox file that the installer aborted at its first `.claude/hooks` write under the seat's read-only paths and changed nothing. The installer's inability to run from a Claude seat joins T81b's installer item.

## Revise round 2 (orchestrator, 2026-10-05 09:05Z) — task-level audit of 94761d1a is `incorrect` (2)

1. **P2, storage-path validation before any mutation (Codex thread 4179789825 reopened as a code change).** Deferring the symlinked-children check leaves the trusted lifecycle hooks exposed: a real `.claude/contextdb` with `state -> ~/shared` passes the current guard and the CLI chmods and writes there. In the wrapper, before invoking the CLI, refuse when any of `state`, `spool`, `health` under the opt-in directory is a symlink (lstat; an existing entry must be a real directory; a missing entry is fine, the CLI creates it); refuse with the usual one stderr line and exit 0. Test: a symlinked `state` child is refused, a real one is accepted. T81b keeps the vendor-side `project_paths.ensure()` hardening as defense in depth.
2. The second finding (a feedback item without a disposition) is the orchestrator's sweep error, fixed on the orchestrator side; nothing for you.

One commit, CI, Bot wait on the new diff head (timestamped), RESULT; `gh pr update-branch 269` if `main` moved.

## Revise round 3 (orchestrator, 2026-10-05 09:20Z) — task-level audit of c466231a is `incorrect` (1)

Symlinked grandchildren (`spool/incoming`, `spool/quarantine`) still reach the CLI. Stop enumerating levels: before invoking the CLI, walk the opt-in directory (`os.walk(opt_in, followlinks=False)`, including the top) and refuse if any directory entry at any depth is a symlink or a non-directory where a directory is expected (regular files inside `state`/`spool` are the ledger's own and are fine; only symlinks anywhere are refused). The tree is small, so the walk is cheap inside the 2-second budget. Tests: symlinked `spool/incoming` refused; a real nested tree accepted. One commit, CI, Bot wait on the diff head (timestamped), RESULT.
