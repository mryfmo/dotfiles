# dotfiles-T82-codex-compaction-hooks-a01 — report (status: ready_for_review)

- PR: #269 (https://github.com/mryfmo/dotfiles/pull/269), branch `feat/codex-compaction-hooks`.
- Final head (after revise round 3): `9ff2ad52`, on top of the update-branch merge 94761d1a (main f2d4d709, unchanged).
- CI: all 13 checks pass on 9ff2ad52. `mergeable_state` is `blocked` again: unresolved Bot threads, including the two new ones, and the required review.
- Round 0: the final head was 7ee91087, and no Bot review or finding arrived on c8127bd8 or 7ee91087 within their windows. For round 1, see the section below.

## Changes

1. **Manifest** (`codex.hooks.command_hooks`, after `permission_request`): `PreCompact` (timeout 10), `PostCompact` (timeout 10) and `SessionEnd` (timeout 3), each running `{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify` with the status message "Recording to CompactionDB". A two-line comment explains them. `permission_request`, `hooks.state` and the profiles' `notify` entries are unchanged.
2. **Wrapper** (`executable_contextdb-codex-notify`):
   - it reads `payload="${1:-$(cat)}"`, so `notify` passes argv and hooks use stdin;
   - unchanged: the opt-in check, the trusted-CLI `ingest --ingested-from codex`, and exit 0 with one stderr line on failure;
   - correction (round 1): the round-0 claim that it "only ingests, never prunes or vacuums" was wrong. `ingest` ran `process_payload()`'s SessionEnd retention pass (`prune_expired` and the log/quarantine cleanup). Since da04f943 the receiver passes `ingest --no-maintenance` (CompactionDB 2.0.0+dotfiles.8) on every delivery, so it records the event only, never prunes, vacuums or cleans up. Retention stays on the explicit `prune` and on Claude Code's own SessionEnd hook;
   - shdoc `@description` and `@arg` added;
   - fix 7ee91087: the inline script runs with `python3 -I -` (see the Bot threads).
3. **Rendered** `codex-config-managed.toml`: three `[[hooks.<Event>]]` tables (`matcher = "*"`) after `PermissionRequest`, and `make render-check` is clean. The validator's exact-table check and its 3-second SessionEnd cap pass.
4. **Tests**:
   - `test_contextdb_codex_notify.py`: a stdin `PreCompact` payload is ingested; argv wins over a competing stdin payload; invalid stdin reports and exits 0; a `json.py` in the session cwd cannot shadow the stdlib (this test fails without `-I`, which I checked by temporarily reverting the flag);
   - `test_generate_agent_configs.py`: the real managed Codex config holds the three hooks with the expected command and timeouts. The generator fixture does not mirror the manifest, so the real rendered file is pinned instead.
5. **Live check (this worktree)**: `printf … PreCompact … | bash …contextdb-codex-notify` gives `rc=0`, and the `sqlite3` query returns `pre_compact|t82|codex`.
   - A real Codex `/compact` on both hosts is the operator's live E2E (T87). It was not performed here.
6. **README** (PONG decision, c8127bd8): one paragraph after the lifecycle block. Once per machine after `make update`: run Codex `/hooks`, trust the three CompactionDB hooks and the permgate `PermissionRequest` hook, and confirm the `[hooks.state]` entries, which the managed config merge preserves (`RUNTIME_PREFIXES` holds `hooks.state`).

## Codex Bot threads (all unresolved; the orchestrator replies)

- **4179558230** (P1, on 4c388114): new user-config hooks are not trusted.
  - Proposed: `not-applicable:non-managed Codex hooks need the operator's one-time /hooks trust (official docs); the README now documents that step (c8127bd8), per PONG decision option (a)`.
  - The orchestrator notes a follow-up task: hook trust-state pins (record the trusted keys in `codex.hooks.state`, and refresh the drifted ponytail hashes).
- **4179558226** (P2, on 4c388114): the PostCompact payload has no `compact_summary`.
  - Proposed: `not-applicable:Codex PostCompact carries no summary (official field list); the vendor skips empty summaries (memory.py, recovery.py), so the event stays a timeline marker with no empty memory`.
- **4179583256** (Codex Security P1, on 4c388114): `python3 -` in the session cwd lets a committed `json.py` run as the user.
  - Proposed: `fixed:7ee91087` (`python3 -I -`, plus a regression test).
  - The trusted CLI child process runs a script from `~/.agents/compactiondb`, so its `sys.path[0]` is that script's directory, not the cwd.

## Reporting notes

- **Previously undetected security risk:** the profiles' `notify` entry ran this same receiver before T82, so the `json.py` vector existed for `notify` too, in whatever cwd Codex invokes notify from. 7ee91087 closes it for both paths.
- **Existing hook probably skipped today:** the deployed `~/.codex/config.toml` `[hooks.state]` has no entry for the existing permgate `PermissionRequest` config hook, so that hook is probably skipped until it is trusted. The README trust step now covers it.
- **Timeout (superseded in round 1):** the round-0 note said the 5 s ingest timeout exceeded Codex's 3 s SessionEnd cap. Round 1 (da04f943) sets it to 2 s.
- **The `enforce-uv.sh` hook from #266 now denies bare `python3` in this Claude seat.** Inline edit scripts and helpers therefore ran through `uv run python`. The first edit attempt was denied before anything ran.
- **Blocked PONG:** I sent one while waiting for the P1 scope decision, because the stop gate does not accept a question PONG.

## Revise round 1 (task_rev 12636547…, PONG decision a3ae5c23…)

Final head `94761d1a` is the `gh pr update-branch` merge of main f2d4d709 (#270). It sits on top of:
- `da04f943`: CompactionDB 2.0.0+dotfiles.8 `ingest --no-maintenance`, the wrapper's flag and 2 s timeout, and the project copy;
- `74a559c7`: symlinked opt-in rejected.

CI: all 13 checks pass on 94761d1a, and the branch is up to date.

1. **Audit P2 (ingest was not ingest-only).**
   - `vendor/compactiondb`: `process_payload(..., maintenance=True)`, and the SessionEnd retention pass runs only when `maintenance` is on. `cli.py ingest` gains `--no-maintenance`, which passes `maintenance=False`; the spool drain and commit still run.
   - New vendor test: `test_ingest_no_maintenance_records_session_end_without_retention` (an aged event, error log and quarantine file all survive a SessionEnd ingest). `make test`: 90 OK. `make validate`: pass after `make clean`, because my test run had left `__pycache__`.
   - CHANGELOG `2.0.0+dotfiles.8`; `make manifest` (`sha256sum -c` passes); the manifest `assets.compactiondb.pin` and both `test_asset_manifest.py` literals move to `2.0.0+dotfiles.8`.
   - Wrapper: `--no-maintenance` on every delivery (notify and hooks), `timeout=2`, and the shdoc updated.
   - Project copy:
     - `install.py --project . --skip-instructions` aborted at its first `.claude/hooks` write (read-only for this seat) and changed nothing;
     - per PONG decision (a), `cli.py` and `hook.py` were copied from the vendor tree into `.claude/contextdb/contextdb/`;
     - the parity check (`validate-agent-assets`) and a `cmp` loop over every parity file are clean, and `.claude/hooks/contextdb_*.py` were already identical.
   - Live check through a temporary HOME holding the dotfiles.8 vendor tree: `pre_compact|t82r1b|codex` and `session_end|t82r1b|codex`, with SessionEnd taking 0.14 s.
   - With the real HOME, the deployed CompactionDB (2.0.0+dotfiles.6) does not know `--no-maintenance` yet. The receiver prints its one failure line and exits 0 until `make update` deploys the wrapper and dotfiles.8 together. The operator should apply both in the same `make update`, which is the normal path.
2. **Audit P3 (negative control).** The validation file pastes the `json.py` regression test with `-I` removed (FAILED, rc=1) and restored (OK, rc=0).

Bot threads, new this round (unresolved):
- **4179749575** (P2 security, on da04f943): a symlinked `.claude/contextdb` opt-in.
  - `fixed:74a559c7`: the opt-in must resolve to itself, and a symlink test fails without the check (verified).
  - This was fixed on my initiative although it is a P2, because it is a trust-boundary check in the receiver under change. Say if you would rather have it as a follow-up.
- **4179789825** (P2, on 94761d1a): symlinked `state`, `spool` or `health` children of a real `.claude/contextdb`, which the CLI's `project_paths.ensure()` follows.
  - Proposed: `not-applicable:the child-path check belongs in vendor project_paths.ensure() (refuse symlinked children before mkdir/chmod) — follow-up with T81b's vendor items`.
- **4179789828** (P2, on 94761d1a): a Codex session started from a subdirectory, whose `cwd` has no `.claude/contextdb`, is a silent no-op.
  - Proposed: `not-applicable:pre-existing notify-receiver behaviour; locating the enclosing opted-in project (git toplevel or nearest ancestor) is a design follow-up`.
- No Bot review of the final merge head 94761d1a beyond the 23:35:12Z one. My diff head 74a559c7's window ended at 23:43:23Z.

Evidence note: a stray `/tmp/claude-1000/types.py` (not mine; mtime 08:28 JST) shadowed the stdlib for my Bot-wait helper run from that directory. I re-ran it with `uv run python -I`, the same class of issue as Bot P1 4179583256.

## Revise round 2 (task_rev 6fbe278d…)

One commit, `c466231a`. CI: all 13 checks pass, the branch is up to date with main f2d4d709, and `mergeable_state` is `clean`.

1. **Audit P2 / Bot 4179789825 (symlinked storage children), now a code change as decided.**
   - Before invoking the CLI, the receiver checks `state`, `spool` and `health` under the opt-in directory. A symlink, or an existing entry that is not a directory, is refused with the usual stderr line (`contextdb-codex-notify: ingest failed`) and exit 0. A missing entry is fine, because the CLI creates it.
   - Tests:
     - `test_symlinked_storage_directory_is_refused`: `state -> outside` is refused, the CLI is never called, and the outside directory stays empty;
     - `test_real_storage_directories_are_accepted`: real `state`/`spool`/`health` are ingested;
     - negative control: with the check replaced by `if False:`, the symlink test fails; restored, both pass. Pasted.
   - Live check through the dotfiles.8 temporary HOME on this worktree, whose storage directories are real: `pre_compact|t82r2|codex`.
   - The `spool/incoming` and `spool/quarantine` grandchildren are not checked by the receiver, per the round text. The vendor-side `project_paths.ensure()` hardening stays with T81b as defense in depth.
   - Proposed disposition for 4179789825: `fixed:c466231a`.
2. The orchestrator's sweep finding needs nothing from me.

Unresolved Bot threads and their dispositions:
- 4179558230: not-applicable, operator trust step in the README (c8127bd8);
- 4179558226: not-applicable, PostCompact stays a timeline marker;
- 4179583256: fixed:7ee91087;
- 4179749575: fixed:74a559c7;
- 4179789825: fixed:c466231a;
- 4179789828: proposed not-applicable, the subdirectory session cwd is a design follow-up.

No Bot review of c466231a arrived within its window (pushed 23:55:17Z, window ended 00:10:17Z, re-polled after).

`make unit-test`: 808 OK.

## Revise round 3 (task_rev b88e75c5…)

One commit, `9ff2ad52`. CI: all 13 checks pass, and the branch is up to date with main f2d4d709.

1. **Audit: symlinked grandchildren.**
   - The receiver walks the opt-in tree with `os.walk(opt_in, followlinks=False)`, top included, and refuses any symlink at any depth among directory or file entries. Regular files (the ledger, spool events) are fine.
   - Each storage directory the CLI uses (`state`, `spool`, `spool/incoming`, `spool/quarantine`, `health`) must be a real directory or absent. A refusal prints the usual stderr line and exits 0.
   - This replaces round 2's three-name check.
   - Tests:
     - `test_symlinked_storage_grandchild_is_refused` (`spool/incoming -> outside`; CLI not called; outside untouched);
     - `test_real_nested_storage_tree_is_accepted` (`state/context.db`, `spool/incoming/event.json`, `spool/quarantine`, `health`);
     - round 2's tests still pass;
     - negative control: with the walk's symlink test replaced by `if False:`, the grandchild test fails; restored, all 12 pass. Pasted.
   - Live check with the dotfiles.8 temporary HOME on this worktree (`find .claude/contextdb -type l` gives 0): `session_end|t82r3|codex` in 0.15 s.
   - `make unit-test`: 810 OK.

New Bot findings on 9ff2ad52 (review at 00:25:58Z), both P2 and not changed here; proposed:
- **4179926397** (Codex-only projects lose `errors.jsonl` and quarantine retention under `--no-maintenance`).
  - Proposed: `not-applicable:valid gap for Codex-only projects, but the cleanup belongs in the vendor CLI (move the log/quarantine retention into the explicit prune) — follow-up with T81b`.
  - Projects that also run Claude Code keep it through Claude's SessionEnd hook.
- **4179926400** (TOCTOU between the walk and the CLI start).
  - Proposed: `not-applicable:exploiting the window needs an attacker process already running as the user inside the tree, which already holds the user's privileges; an atomic no-follow binding belongs in vendor project_paths.ensure() (T81b defense in depth)`.

Earlier threads keep their dispositions (round-2 list). All threads are unresolved.

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)
