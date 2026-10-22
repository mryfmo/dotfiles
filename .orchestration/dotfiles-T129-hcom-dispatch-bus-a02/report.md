---
task_id: dotfiles-T129-hcom-dispatch-bus-a02
seat: claude-standard-dot-a008
branch: tools/hcom-dispatch-bus-a02
base: d06d94fd8eedcd0770c1c80c2b1596ec36109ef8
pr: PR_PLACEHOLDER
task_sha256: acfc72e24cccd8ce750b9d25ed35000db271953ce7dd94e85a9521fed49ccabe
---

# Report: dotfiles-T129-hcom-dispatch-bus-a02

- **Producer:** worker (Claude seat a008, worktree worker-f), unless an item names the orchestrator (Claude seat, sandboxed Bash). The TASK of 2026-10-22T07:46:43Z names seat a008 instead of the text's a009.
- **Branch:** fresh from `origin/main` `d06d94fd`. The task copy `task.md` hashes to the TASK line's `acfc72e2…` (validation §0).
- **PR #407 (a01's draft, records only):** replaced by this fresh branch and PR, and closed (validation §20).
- **Commits:** `a37127dd` item 0 records; `5d75a5cb` item 6 red; `2db3d4f8` item 6 fix; `7b75af70` hold records; `88c03f8d` the red fixtures; `7d10c89f` the fix; `38daedb0` a fixture's uv warm-up pins its interpreter; `563e6912` an error message; `8f6613bb` the orchestrator's Q2 contract; `7ad4d56d` the worker-side review's fixes; then the records.

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
   - `--thread <team>` stores `data.thread` (§7), and the reader's three SQL templates run on real hcom 0.7.30 (§9): the team filter, the exact id (`AND id = 9` gave one row) and the read subquery over `instances` (no row read before `listen`, both after it). An injection attempt reached hcom's parser as SQL text, so the value grammar is the guard (§9).
7. **Read state (§6):** there is no per-message read column and no read time. A recipient has read a message when its `instances.last_event_id` is at or past the message `id`.
   - `listen --name w1` moved the cursor from 1 to 3 and `unread_count` from 1 to 0.
   - The two status events it logged carry no message id, so nothing records when a given message was read.
8. **Tags (§4, §5, §7):** a message row carries no tag (`data` holds `from`, `text`, `scope`, `sender_kind`, `delivered_to`, `mentions`, and `thread` when given). A tag lives only in `instances.tag`; a01 measured that hcom deletes that row when an agent stops.
9. **The read command (§7):** `hcom events --type message --full --last <n>` prints JSON Lines with `id`, `ts` (ISO-8601, `+00:00`), `data.from`, `data.delivered_to` and `data.text`. Run under `env -i`, it left every file of the store byte-identical (sha256 of each file before and after). `--sql <expr>` filters `events_v`: `msg_thread = 'dotfiles-conformance'` selected exactly the message sent with `--thread dotfiles-conformance`. The expression is SQL text, so a value can be validated but not bound.

## Questions and the orchestrator's answers

The question PONG (message 3145, 08:04:00Z) asked five questions before any code. Answer 3147 (08:11:41Z, no count) accepted the defaults with these terms, and clarification 3150 (09:36:06Z, no count) fixed the reply route. The text is frozen; amendment 3 carries these at acceptance.

1. **read_at:** the dispatcher's UTC time when `instances.last_event_id >= id` is first seen, else null; documented as observed, not stored.
2. **Team scope, and the bus contract (3150):** hcom-dispatch sends every TASK, ACCEPTANCE and PING as `@<to> --thread <team>`; hcom adds the recipients to the thread's members on a successful `--thread` send. A worker answers with `hcom send --thread <team>` and no `@target`, since an external orchestrator is not addressable. bus-history reads `msg_thread = '<team>'`; a reply that names no recipient is a row with recipient `-`, unread.
3. **SQL text:** `hcom events --sql` from a fixed template; only the grammar-checked team (`[a-z0-9-]`) and an integer id are interpolated. A test feeds a hostile team string and asserts that no SQL is built (threat row below).
4. **The fixture seam:** an explicit `--passwd-home <dir>` argument, no environment variable and no file under the checkout. Production callers pass none, and one test asserts it.
5. **tests/unit/test_check_regime_boundary.py:** adapted; the wildcard covers it.
6. **Amendment 2's `<checkout>`:** the checkout the script runs in, by its own location; validated in this worktree's `.agents/worklog/uv-tools`. The main-checkout install is the orchestrator's acceptance step.

## Items

1. **`scripts/orchestrator/bus-history.sh` (new, item 1, constraints 2 and 6):**
   - Rows are `<marker> [<at>] <from> → <to>: <body>`, chronological; at is UTC second precision; markers come from the recipients' cursors.
   - `--json` keeps the hcom id and the fields, and `--message-id` selects exactly one row: none, or another team's, exits 1.
   - The store declaration is read under the passwd home and must be `.hcom` (hcom's default; HCOM_DIR is never set). The directory and `hcom.db` must resolve inside it, and the SQLite header must say user_version 18; the header is read from the file's first 100 bytes, not by opening SQLite. An inherited HCOM_DIR is refused.
   - Every row is checked before any output, so a failure prints nothing.
   - hcom runs only from `<checkout>/.agents/worklog/uv-tools/hcom/bin/hcom`, after a sha256 comparison with `hcom.sha256` beside it at every invocation (`refused: hcom binding`).
2. **`home/dot_local/bin/common/executable_hcom-dispatch` (new, item 2):**
   - It keeps agmsg-dispatch's `<team> <from> <to> <pane> <words…>` form, word joining and AGMSG_DISPATCH_TIMEOUT deadline; the team must also match the reader's slug.
   - A body holding NUL or a line separator is refused before the send, so no send can poison the history.
   - One `send --from <from> --json --thread <team> @<to> -- <body>`; its `event_id` is the identity. A missing or malformed id exits 3: no resend, no nudge, no sender or body matching.
   - The receipt is confirmed only through the exact-id view; at half the deadline there is one `herdr pane run <pane> "hcom: new message for <to>"`, herdr being the absolute install the passwd home's mise answers. Exit 1 when unread at the deadline.
   - stdout is one `{"id", "read_at"}` receipt.
3. **`scripts/orchestrator/dispatch.sh` (item 3, constraints 3 and 4):**
   - Both send sites go to hcom-dispatch; the bounded pre-send read goes through bus-history (BUS_READ_WINDOW), and a refused read sends nothing. AGMSG_SCRIPTS and the window alignment are gone.
   - The record is opened once through the acceptance directory's descriptor. No symlinked component is allowed: an lstat walk checks each one, opening nothing. The record argument must be the line's `record_file=`, its bytes must hash to `record_sha256=`, and its block is parsed from that one read.
   - After the send: the exact-id view must match the line, sender and recipient; then, under flock, the inode and the digest are rechecked, and a `dir_fd` temporary file replaces the record. The new digest is printed.
   - An unread receipt is recorded unread and keeps exit 1.
   - The task file is hashed and checked as a private snapshot under `<checkout>/.agents/worklog/dispatch-snapshots/` (named like the file, since C1 compares the stem), removed before the send.
4. **Item 4:**
   - A `status=revise` ACCEPTANCE (never `verdict=`) needs `previous_head=` (40 hex) and `check=` once each, `task_sha256=` and a record.
   - `regime-counters.sh <task_id> --team <team> --history-only` runs before the send, with `--record-sha256` when the record is the task's own. A failure refuses, and its stdout joins the record's `counters` list as `<task_id> <UTC time> <lines joined by "; ">`.
   - Other statuses skip only these checks.
5. **`scripts/orchestrator/bus-read.sh` (item 5):** it reads bus-history; the jq classification is byte-identical, and the five existing fixtures were rerun.
6. **`scripts/regime-counters.sh` (item 6):**
   - `read_history` adapts the reader's `--json` view, which keeps hcom's ids, into the existing `id at from to body` input; `storage.sh` is no longer sourced, and the `--history-file` contract and its seam cases are kept.
   - `revises = max(RESULTs − 1, this task's ACCEPTANCE status=revise count, 0)`; T118's fixture now counts 20.
   - The record is read once through the directory's descriptor (`O_NOFOLLOW`, regular file, optional `--record-sha256`).
   - gh calls name `--hostname github.com` and `repos/mryfmo/dotfiles`; the bound gh executable is T133 gh-binding a02's (PR #456, open, no new base yet).
7. **Untouched, item 7:**
   - `scripts/orchestrator/replay.sh` reads no bus (its source has no history.sh, storage.sh or sqlite3).
   - `scripts/agent-stop-gate.sh` is the stage-2 hook.
   - SKILL and rules, agmsg-dispatch and `.chezmoiremove` are PR E's.
   - `test_migration_item_matrix` checks these and runs with the agmsg store absent.
8. **Amendment 2 (`scripts/update-agent-assets.sh` `update_hcom_private`):**
   - It verifies the kept wheel against the pin and installs with UV_TOOL_DIR and UV_TOOL_BIN_DIR inside `<checkout>/.agents/worklog/uv-tools`; the entry's sha256 is recorded beside it.
   - It runs only from a checkout's own updater, not chezmoi's copy, and records no manifest step: `test_asset_manifest.py` pins 17 recording calls, and the files sit in the gitignored worklog.
   - Run in this worktree (validation §12): the entry is a Mach-O binary with sha256 `7cd012d9…`, and the public `~/.local/bin/hcom` keeps that same digest.
9. **Constraint 2's declaration:** `assets.hcom.store_relative_path: .hcom` in `home/dot_agents/agent-config.yaml`; `make render-check` passes.

## Binding constraints and design 5.14

- **Constraint 1 (items 2, 3 and 9):**
  - Every tool is an absolute path: `/usr/bin/*` and `/bin/*` utilities, `/usr/bin/python3 -I` for the embedded Python, jq from `/usr/bin/jq` (else Homebrew's, for the macos-14 runner) under `env -i` without HOME so no `~/.jq` loads, the private hcom, and uv, python and herdr resolved by the passwd home's mise from `/`.
  - The scripts start as `#!/bin/bash -p` and run children as `/bin/bash --noprofile --norc -p` under `env -i`.
  - Each refuses an absent or relative UV_CACHE_DIR and passes it on.
  - TMPDIR joins the contract, because bash 3.2 keeps here-documents in temporary files under `/tmp`, which the sandbox refuses (validation §11). The Python sections therefore sit in here-documents that never run and are read from the file itself.
- **Constraints 3 and 4:** the task snapshot, the record descriptor and the counters' record, as in items 3 and 6.
- **Constraint 5:** no new gh call.
- **Constraint 6:** the framing checks of item 1.
- **Constraint 7:** the revise fixtures use the full line.

## Selectors (red at 88c03f8d, item 6 at 5d75a5cb; green at 7d10c89f, 38daedb0 and the code head 7ad4d56d)

Red runs were made at the red commit with the scripts at its bytes: main's, plus item 6's committed counters rule. The fixture world runs a baseline script, which takes no `--passwd-home`, by its own route (bash on PATH, the fixture home as HOME). So each red is that route's behaviour (it reads no hcom) and never a usage error. The new files, `bus-history.sh` and `hcom-dispatch`, are absent at baseline: their direct tests are red by absence, and the consumer tests carry the behavioural red. Validation §14 (red) and §15 (green) hold every test's line.

| Threat row | Selector | Red | Green |
| --- | --- | --- | --- |
| executable_hcom-dispatch | `test_hcom_dispatch.py::HcomDispatchTest::test_transport_matrix` | absent file | ok |
| bus rows and routing identities | `::HcomDispatchTest::test_identity_and_payload_matrix` | absent file | ok |
| update-agent-assets.sh | `::UpdateHcomPrivateTest::test_update_hcom_private_installs_…_drifted_wheel` | no function | ok |
| bus-history.sh | `test_orchestrator_tools.py::…::test_hcom_history_matrix` | absent file | ok |
| dispatch.sh | `::test_hcom_dispatch_matrix` | agmsg route | ok |
| bus-read.sh | `::test_hcom_bus_read_matrix` | agmsg route | ok |
| regime-counters.sh | `test_regime_counters.py::…::test_hcom_counter_matrix` | agmsg route | ok |
| agent-config.yaml | `::test_production_store_declaration` | no declaration | ok |
| private namespace, 5.14 item 2 | `::test_private_namespace_matrix` | per route | ok |
| store identity | `::test_hostile_hcom_store_refused` | per route | ok |
| consumed-bytes binding, 5.14 item 4 | `::test_consumed_bytes_matrix` | agmsg route | ok |
| history format | `::test_hcom_marker_roundtrip` | agmsg route | ok |
| history framing | `::test_history_forged_row_refused` | per row kind | ok |
| receipt identity | `::test_concurrent_identical_send_receipts` | agmsg route | ok |
| status key | `test_regime_counters.py::…::test_status_revise_matrix` | `[2 RESULTs, 3 revises]` (5d75a5cb) | ok |
| in-process effects | `::test_fixture_route_isolation` | agmsg route | ok |
| new or renamed scripts | `::test_migration_item_matrix` | items 0 to 6 | ok |
| 5.14 item 3 | `::test_trusted_path_matrix` | agmsg route | ok |
| 5.14 item 7 | `::test_contract_attack_matrix` | per route | ok |
| 5.14 item 9 | `::test_private_cache_matrix` | per route | ok |
| lint baseline | `test_lint_comparisons.py::…::test_the_changed_files_are_clean_against_the_baseline` | 3 stale rows | ok |

- **Kept and adapted:** the existing `test_dispatch_*`, `test_bus_read_*`, counters and boundary cases keep their refusals.
- **Rewritten:** the window-alignment case is replaced by the bounded pre-send read and the exact id.
- **Behaviour change by constraint 4:** two concurrent sends to one record now record the first, and the second refuses as "changed during the send", naming its message.
- **Guards at baseline:** the existing field and grammar refusals pass on main.

## Threat row the answer to Q3 asks for

- **control:** the SQL text bus-history.sh hands `hcom events --sql`, built from a fixed template.
- **disposition:** residual. hcom takes SQL text and cannot bind a value, so the only interpolated values are the team, matched against `^[a-z0-9][a-z0-9-]{0,63}$`, and the message id, matched against `^[1-9][0-9]{0,18}$`, before any child runs. `test_hcom_history_matrix` feeds `x' OR 1=1 --`, an uppercase team and a non-integer id, and asserts exit 2 with no hcom call.
- **owner:** dotfiles-T129-hcom-dispatch-bus-a02-followup-a01.

## agmsg mentions left in the five scripts (validation §18)

| Where | What | Why it stays |
| --- | --- | --- |
| dispatch.sh, regime-counters.sh, bus-read.sh | `AGMSG-TASK`, `-ACCEPTANCE`, `-RESULT`, `-PONG`, `-PING` | the message contract v1 kinds, the bus content; no store read |
| bus-read.sh `@brief` and `@arg`, regime-counters.sh `@brief` and `--team` | "agmsg team", "agmsg task" | the team and task naming of the regime |
| hcom-dispatch header, `AGMSG_DISPATCH_TIMEOUT`, and dispatch.sh passing it on | agmsg-dispatch's argument form and deadline | item 2's "preserving agmsg-dispatch's argument form… and deadline"; PR E retires agmsg-dispatch |

No script sources agmsg or reads its store; `AGMSG_SCRIPTS` is gone from all five.

## Stage 1 operation and residuals

- **Operational use waits:**
  - until the main-checkout `update_hcom_private` install (the orchestrator's acceptance step);
  - until the deployed declaration (`chezmoi apply`) and a store at `~/.hcom/hcom.db`;
  - until stage 2 seats hcom agents. Until then a send exits 3 with `No active agent`, and the reader refuses an absent declaration, so dispatch.sh, bus-read.sh and regime-counters.sh refuse.
  - `check-regime-boundary.sh` and the stop gate, out of scope, are among the callers this affects.
- **read_at is observed, not stored:** its time is the confirming poll's, so it can trail the cursor's move by the poll interval (5 s).
- **Same-UID processes (design 5.14 item 0):** a process of the same user can still swap files between the digest checks and their use. The private tool directory and the per-invocation sha256 limit, but do not close, that window.
- **Host scanner:** an outside reader on this host (Spotlight or an endpoint agent) reads a new file once, about 2 s after creation (validation §13). The worker-root case waits until its probe input stays unread before running the route. I first blamed `os.path.realpath()` for that read; §13 shows realpath leaves the file unread once the scanner's read is past.
- **Interpretations I chose:**
  - The consumers take the same leading `--passwd-home` and forward it only when given. Production callers pass none, and `test_production_store_declaration` asserts each route reads the passwd home without it.
  - The updater records no manifest step, and runs only from a checkout's own updater.

## Deferred: stage 2 and PR E

Unchanged from the text:
- stage 2 seats `hcom omp --tag <team>`, and its owner is distinct from this task;
- the worker hcom hook needs a re-plan;
- PR E owns SKILL and rules, agmsg-dispatch, the stop hook and `.chezmoiremove`.

Item 0 changes nothing in hcom's member surface for stage 2: `list`, `config -i <name> tag`, `start --as` (validation §2, §12).

## Worker-side review (`worker-review.json`, `worker-review-receipt.md`)

An independent agent review in a fresh context, given only the code and the binding constraints, read `8f6613bb`. Its verdict was incorrect on two P1s, and it reproduced every finding in fixture worlds. Dispositions:

| # | Finding | Disposition |
| --- | --- | --- |
| r1 P1 | the recorder's `env -i` prefix was rebuilt by `printf \| /usr/bin/python3` outside `env -i`, so a line break in an inherited value, or DEVELOPER_DIR, chose its programs | fixed in `7ad4d56d`: passed as arguments; AGMSG_DISPATCH_TIMEOUT checked |
| r2 P1 | `/usr/bin/shasum` is Perl and ran with PERL5OPT/PERL5LIB, so a digest could be forged | fixed in `7ad4d56d`: run under `env -i` |
| r3 P2 | under the Q2 contract, bus-read never closes a task, and replies cross to the other workers (below) | the orchestrator's decision |
| r4 P2 | `check-regime-boundary.sh` (not in `allowed_files`) runs the counters without UV_CACHE_DIR and skips its INV-6 probe silently | residual, owner dotfiles-T129-hcom-dispatch-bus-a02-followup-a01: the caller exports a private absolute UV_CACHE_DIR |
| r5 P3 | an uncaught `TimeoutExpired` or a negative sleep exited 1 without a receipt | fixed in `7ad4d56d`: exit 3, sleep floored at 0 |
| r6 P3 | an empty `--message-id` or `--limit` counted as absent | fixed in `7ad4d56d` |
| r7 P3 | gh is still found through PATH | residual: T133 gh-binding a02's bound gh (PR #456, open) is constraint 5's prerequisite |
| r8 P3 | the production-callers subtest reaches the passwd home | mitigated in `7ad4d56d`: the fake hcom refuses a home outside the fixture; the read-only declaration and header checks remain, since that subtest exists to show them |

- **Test gap closed:** `test_private_namespace_matrix` now drives the record path with a hashed file under PERL5OPT/PERL5LIB, DEVELOPER_DIR and a line-break value.
- **Red on the pre-fix bytes:** that subtest and the line-break one fail on `8f6613bb`'s dispatch.sh and pass on `7ad4d56d` (validation §19).

## For the orchestrator's decision: the reply route (r3)

Reproduced on real hcom 0.7.30 with two tagged agents (validation §17):
- `send --from orch --thread team @w1` is delivered to `["w1"]`.
- w1's reply, `send --name w1 --thread team` with no target, is delivered to `["w2"]`, the other member, and never to the orchestrator.
- `@orch` exits 1 with `No active agent for @orch`.

The consequences:
- bus-history shows the RESULT as `w1 → w2`.
- bus-read's frozen close rule, a RESULT from the opener's recipient to its sender, never matches, so `open: task=t seat=w1` stays after the RESULT.
- Every reply also lands in the other workers' inboxes.

Item 5 freezes the jq, so nothing here changes it. Default proposed for amendment 3:
- the orchestrator becomes an addressable hcom member (seated with `hcom start` under the team tag), so a worker replies `@<orchestrator> --thread <team>`;
- otherwise, bus-read closes on a RESULT or blocked PONG from the opener's recipient whatever its `to`, and per-worker threads keep replies out of other inboxes.


cost: n/a
