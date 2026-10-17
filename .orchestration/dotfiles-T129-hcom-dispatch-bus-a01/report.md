---
task_id: dotfiles-T129-hcom-dispatch-bus-a01
seat: claude-standard-dot-a008
branch: tools/hcom-dispatch-bus-a01
base: 99a4a80f
pr: none
task_sha256: 1fed50618ef0815e290115b6e9f85820dcb66376011a9e28fb1f20a194924631
---

# Report: dotfiles-T129-hcom-dispatch-bus-a01

- Seat: `claude-standard-dot-a008` in `.claude/worktrees/worker-f`; AGMSG-TASK 2026-10-17T23:41:50Z with `task_sha256=1fed5061…`, which the dispatched file and the branch copy `task.md` match byte for byte; the task-consistency check passes on it; the six premises replay as recorded (validation §1, §2).
- Branch: `tools/hcom-dispatch-bus-a01`, fresh from `origin/main` `99a4a80f` (#390 not merged yet; the rebase follows its merge, before the RESULT).

## Item 0: facts (hcom 0.7.30), before any code

Every fact below is a pasted run in validation §3. The store runs were made against disposable stores under `$TMPDIR` (`HCOM_DIR` set on my own command line, never in a script); the live `~/.hcom` holds only `.tmp` and was never opened.

1. Version: `~/.local/bin/hcom --version` prints `hcom 0.7.30` (a native arm64 binary, `~/.local/share/uv/tools/hcom/bin/hcom`).
2. Commands: `send`, `listen`, `list`, `events`, `bundle`, `transcript`, `start`, `stop`, `config`, `run`, `relay`, `archive`, `reset`, `hooks`, `status`, `term`, `update` (top-level `--help`).
3. Store: `$HCOM_DIR`, else `~/.hcom` (the binary's embedded `env.get("HCOM_DIR") or os.path.join(os.path.expanduser("~"), ".hcom")`); the SQLite file is `<dir>/hcom.db`, `PRAGMA user_version` 18, journal mode WAL. Messages are rows of `events` (`id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, type TEXT, instance TEXT, data TEXT`) with `type = 'message'` and `data` JSON `{from, text, scope, sender_kind, delivered_to[], mentions[], …}`; the view `events_v` extracts `msg_from`, `msg_text`, `msg_delivered_to`, `msg_mentions`. Agents are rows of `instances` (`name` the base name, `tag`, `last_event_id`, `status`, …).
4. Read marker: there is no per-message read column. A recipient's read cursor is `instances.last_event_id`: a message is read by a recipient when its id is at most that recipient's `last_event_id` (moving `w1`'s cursor from 0 to 5 to 6 takes `hcom list --json`'s `unread_count` from 2 to 1 to 0). `hcom list <name> --json` and `hcom list <name> last_event_id` do not print the cursor.
5. Send: `hcom send --from <from> --json @<target> -- <text>`; `--from` lets a non-seat process name the sender (the row gets `data.from = <from>`, `instance = ext_<from>`, `sender_kind = external`); `--json` prints `{"delivered_to":[…],"event_id":<n>}`; text after `--` is stored byte for byte (a tab, single and double quotes, a leading `-`); a target that matches no active agent exits 1 (`Error: No active agent for @<target>`).
6. Tags: `@<tag>-<base>` targets exactly the agent of that tag and base name (a wrong tag exits 1), `@<tag>-` every agent of the tag; the message records the base names only (`delivered_to`, `mentions`), never the tag. `hcom` deletes an agent's `instances` row (`DELETE FROM instances WHERE name = ?` in the binary) when it stops or is swept as dead.
7. Read command: `hcom events --type message --full --last <n>` prints JSON Lines, oldest first among the newest n, each with `id`, `ts` (ISO-8601 with `+00:00`), `data.from`, `data.delivered_to`, `data.text`; `--sql <expr>` is ANDed into `SELECT * FROM events_v WHERE 1=1 AND (<expr>) ORDER BY id DESC LIMIT n` and accepts subqueries on `instances` (the read cursor); a malformed expression exits 2; `--all` adds archived sessions.
8. Store creation: `hcom events` against a missing `HCOM_DIR` creates the directory and a fresh `hcom.db` and exits 0 with no rows. `sqlite3 -readonly <dir>/hcom.db` cannot open a WAL store whose `-wal` and `-shm` files are absent (hcom leaves none after it exits): `Error … unable to open database file`.

## Decision: the history route

The task's rule: hcom's read command when one prints the five fields for a whole tag, otherwise `sqlite3 -readonly` behind a schema guard. `hcom events --type message --full` prints id, time, from, recipients and body in a machine form (fact 7), and the read state is reachable through its `--sql` (fact 7 with fact 4); `sqlite3 -readonly` cannot open the live store when hcom is idle (fact 8). So the reader uses hcom's read command, after refusing a missing `<dir>/hcom.db` (fact 8: otherwise the read would initialise a store). The schema guard is a separate probe, `hcom events --last 1 --sql "(SELECT user_version FROM pragma_user_version) <> 18"`: a printed row means another revision and the reader exits 1 (a filter `= 18` on the read itself would return no rows at another revision, so the counters would read an empty history; validation §3 shows `= 18` keeping a row and `= 17` dropping it). The reads do not pass `--all`: archived sessions (`hcom reset`, an operator action) are not counted (a residual, named in the RESULT).

## Two premises of the task file that item 0 changes (defaults I proceed on until amendment 1 says otherwise)

1. "read markers come from item 0's column" (item 3) and "a read marker in the history" (item 2): there is no per-message column (fact 4). Default: a row is read when every recipient in its `delivered_to` has `last_event_id` at or past its id (a recipient whose `instances` row is gone counts as unread); `bus-history.sh --read-marks` prints the marker as a leading `○` (read) or `●` (unread) field, the glyph `history.sh` printed, so the recorder's alignment stays as it is; `hcom-dispatch` confirms receipt with the same condition for its own event id.
2. "a whole tag" (item 0, item 1): the history carries no tag (fact 6), and selecting a tag through `instances` loses every message of an agent once hcom deletes its row, so the counters would undercount (fail-open). Default: `bus-history.sh <team>` reads the whole store (`HCOM_DIR`), and `<team>` scopes delivery instead (`hcom-dispatch` targets `@<team>-<to>`, fact 6); the counters key on `task_id` and over-read rather than under-read; `bus-read.sh` may list another project's open task sharing the store, which is visible, never hidden.
