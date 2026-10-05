# dotfiles-T82-codex-compaction-hooks-a01 — learning triage

1. **Codex user-config hooks do not run until trusted.**
   - Per the official hooks doc, every non-managed hook (user `config.toml`, project, plugin) needs a review and trust in `/hooks` before it runs. Only system, MDM, cloud or `requirements.toml` hooks are managed.
   - Any task that adds or changes a Codex hook definition must therefore name the operator trust step, or record the trusted `hooks.state` keys.
   - The deployed config already lacked a trust entry for the permgate `PermissionRequest` hook.
2. **Never run `python3 -` (stdin script) from a hook or notify receiver.** It puts the cwd first on `sys.path`, and hooks run in the session's working directory, so any committed stdlib-named module in an untrusted repository executes. Use `python3 -I -` (isolated) and pin it with a planted `json.py` test.
3. **The Codex Bot can post a second, security-focused review minutes after the first.** "Codex Security Review · Automatically triggered" arrived about five minutes after the regular review. The head-filtered listing must run until the window ends, not stop at the first review.
4. **The Claude stop gate accepts only `AGMSG-RESULT` or `AGMSG-PONG status=blocked`.** A `status=question` PONG does not release the turn. When a decision is required to continue, send the question and then a blocked PONG for the same task.
5. **"Ingest" in CompactionDB was not ingest-only.** `process_payload()` ran the SessionEnd retention pass (pruning plus log and quarantine cleanup) for any `session_end` event, including through `contextdb_cli.py ingest`. A short-budget caller needs `ingest --no-maintenance` (2.0.0+dotfiles.8). Verify a callee's side effects in its source before claiming "only ingests" in a report.
6. **The CompactionDB installer cannot run from a Claude seat's worktree.** It writes `.claude/hooks` and `.claude/settings.json`, which are read-only for the seat. When only package files change, copy them from the vendor tree and let the parity check prove byte identity (T81b tracks the installer item).
7. **The deployed CLI lags the wrapper.** A receiver flag that needs a newer vendor CLI fails cleanly (stderr line, exit 0) against the older deployed copy until `make update` deploys both. Live-check the new pair through a temporary HOME holding the vendor tree.
8. **Shared temp directories can hold stdlib-shadowing files.** A stray `/tmp/claude-1000/types.py` broke a helper script run from there. Run ad hoc Python helpers with `-I`.
