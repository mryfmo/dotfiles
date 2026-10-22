---
task_id: dotfiles-T129-hcom-dispatch-bus-a02
seat: claude-standard-dot-a008
branch: tools/hcom-dispatch-bus-a02
base: d06d94fd8eedcd0770c1c80c2b1596ec36109ef8
pr: none
task_sha256: acfc72e24cccd8ce750b9d25ed35000db271953ce7dd94e85a9521fed49ccabe
---

# Report: dotfiles-T129-hcom-dispatch-bus-a02

- **Producer:** worker (Claude seat a008, worktree worker-f). The TASK of 2026-10-22T07:46:43Z names seat a008 instead of the text's a009.
- **Branch:** fresh from `origin/main` `d06d94fd`. The task copy `task.md` hashes to the TASK line's `acfc72e2…`.
- **State:** item 0 only. No code is written; the questions below come first, as item 0 asks ("Missing facts/tool/unique send identity means blocked PONG").

## Item 0: facts (hcom 0.7.30), before any code

Every fact is a pasted run in `validation.md`. The store probes used disposable stores under `$TMPDIR`, with `HCOM_DIR` set on the probe's own command line, never in a script. The live `~/.hcom` was never opened.

1. **Amendment 2's denial (validation §1):** from inside this seat's sandbox, `mkdir -p ~/Workspace/dotfiles/.agents/worklog/uv-tools` fails with `Operation not permitted` (exit 1), and so does creating a file in `.agents/worklog/`. The protection premise holds; sandbox.md records the refusal.
2. **Version and entry (§2):** `~/.local/bin/hcom --version` prints `hcom 0.7.30` on stdout, plus an update notice (`→ hcom v0.7.31 available`) on stderr. The entry resolves to `~/.local/share/uv/tools/hcom/bin/hcom`, sha256 `7cd012d9…`, the Checks value.
3. **Commands (§2):** `send`, `listen`, `list`, `events` and the rest. The `send` form is `send @name -- message`; every flag comes before `--`. `--from <name>` names an external sender, and `--json` prints a "JSON receipt; leaves mail unread". `--thread <name>` labels a message.
4. **Default directory and store (§3, §5):** a missing `HCOM_DIR` directory is created by `hcom events`, together with a fresh `hcom.db`. The SQLite basename is `hcom.db`, `PRAGMA user_version` is 18 and the journal mode is WAL.
   - Messages are rows of `events` (`id INTEGER PRIMARY KEY AUTOINCREMENT`, `timestamp`, `type`, `instance`, `data`) with `type = 'message'`.
   - The view `events_v` extracts `msg_from`, `msg_text`, `msg_delivered_to`, `msg_mentions`, `msg_thread` and others.
   - Agents are rows of `instances` (`name` primary key, `tag`, `last_event_id`, …).
5. **`sqlite3 -readonly` (§3):** it cannot open the store once hcom has exited and left no `-wal`/`-shm` files: `unable to open database file (14)`, exit 1.
6. **Send and the stable ID (§4, §8):**
   - `hcom send --from orch --json @w1 -- hello` prints `{"delivered_to":["w1"],"event_id":3}`. The `event_id` is the row's `id`.
   - The row stores `data.from` = `orch`, `instance` = `ext_orch` and `sender_kind` = `external`.
   - A body with a leading `-`, a tab and both quotes is stored byte for byte.
   - An unknown target exits 1 with `Error: No active agent for @nobody`.
7. **Read state (§6):** there is no per-message read column and no read time. A recipient has read a message when its `instances.last_event_id` is at or past the message `id`.
   - `listen --name w1` moved the cursor from 1 to 3 and `unread_count` from 1 to 0.
   - The two status events it logged carry no message id, so nothing records when a given message was read.
8. **Tags (§4, §5, §7):** a message row carries no tag (`data` holds `from`, `text`, `scope`, `sender_kind`, `delivered_to`, `mentions`, and `thread` when given). A tag lives only in `instances.tag`; a01 measured that hcom deletes that row when an agent stops.
9. **The read command (§7):** `hcom events --type message --full --last <n>` prints JSON Lines with `id`, `ts` (ISO-8601, `+00:00`), `data.from`, `data.delivered_to` and `data.text`. Run under `env -i`, it left every file of the store byte-identical (sha256 of each file before and after). `--sql <expr>` filters `events_v`: `msg_thread = 'dotfiles-conformance'` selected exactly the message sent with `--thread dotfiles-conformance`. The expression is SQL text, so a value can be validated but not bound.

## Questions (one PONG; defaults stated)

1. **The receipt's `read_at`:** hcom stores no read time (fact 7). Default: `{id, read_at}`, where `read_at` is the UTC time the dispatcher's exact-ID view first shows the cursor at or past the id, and `null` until then. The markers come from the cursor alone.
2. **The team scope:** a message row carries no tag (fact 8). Default: `hcom-dispatch` sends with `--thread <team>`, and `bus-history.sh <team>` reads `msg_thread = '<team>'` only. A row sent without the label belongs to no team's history; no stage-1 sender sends one.
3. **Binding the query values:** the text says "bind query values, never interpolate SQL", and constraint 2 offers "schema-guarded sqlite3 -readonly" as the alternative, but `sqlite3 -readonly` cannot open the store (fact 5). hcom's write-free read command takes SQL text and cannot bind (fact 9). Default: the reader uses `hcom events --sql`. The only values it interpolates are the team and the message id, and only after each matches its grammar: the existing identity grammar for the team, `^[1-9][0-9]*$` for the id. Every other selection (recipients, cursors) is SQL over the store's own columns, with no caller value in it.
4. **Fixtures versus the passwd home:** constraint 2 binds the declaration to `<passwd home>/.agents/agent-config.yaml` and the store to `<passwd home>/.hcom`, with no HOME or HCOM_DIR override. The validation section asks for isolated fixture roots and "never environment override seams or live stores". A unit test can change neither the passwd home nor the live files under it, and the CI runner has neither file, so no populated-history or declaration fixture can run as written.
   - Default: the scripts find the deployed declaration and store through one realpath-bound checkout sibling, `bus-history.sh`'s own `passwd_home` function. A fixture checkout copies the scripts into an isolated root and replaces only that function's answer with a fixture home, by a file in the fixture root that production never has.
   - This needs the orchestrator's acceptance of that one seam, or another seam named in an amendment.
5. **`tests/unit/test_check_regime_boundary.py`:** it stubs agmsg's `lib/storage.sh` under a fixture HOME and copies `regime-counters.sh`, so item 6 turns its S2 cases red. The text says the test wildcard "expands only to" three other files. Default: adapt that file's stub to the new reader; it sits inside the `tests/unit/test_*.py` wildcard, and an amendment should name it.

cost: n/a

## Done while holding (independent of the questions)

- **Item 6's revise rule:** `revises = max(RESULTs − 1, this task's ACCEPTANCE status=revise count, 0)`.
  - The red tests are `5d75a5cb`, run against main's `regime-counters.sh` bytes: `test_status_revise_matrix [2 RESULTs, 3 revises]` and `test_t118_fixture_counts_revises_from_results` fail.
  - The fix is `2db3d4f8`. Both are green, and so are all 44 tests of `test_regime_counters` and `test_check_regime_boundary`.
  - T118's fixture holds 10 RESULTs and 20 `status=revise` ACCEPTANCEs, so its count moves from 9 to 20; the other three exported fixtures keep their counts.
- **Facts for `update_hcom_private` (amendment 2), found before writing it:**
  1. `tests/unit/test_asset_manifest.py` pins the updater at exactly 17 `manifest_record` calls.
  2. When chezmoi renders the updater into its run script, the source root is `DOTFILES_SOURCE_DIR`, the canonical clone, which no seat touches.
  - Defaults: the target installs only when the updater runs from a git checkout's own `scripts/` directory, and records no manifest step: its files sit in that checkout's gitignored `.agents/worklog/`. Both defaults go in the RESULT unless the answer to the questions changes them.
