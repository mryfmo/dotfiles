# scripts/orchestrator

## hcom bus: `hcom-dispatch` and `bus-history.sh`

Plan 025 W2b (C-1). The omp seats talk over one private hcom store per program, selected by `HCOM_DIR` (hcom 0.7.30). Both scripts refuse to run when `HCOM_DIR` is unset or `$HCOM_DIR/hcom.db` is absent, because `hcom events` creates a store on first use and only the seats' launch may do that. Every test runs against a scratch store, never `~/.hcom`.

### Routes

| Direction                                       | Command                                                              | hcom call                                                                     |
| ----------------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| orchestrator to a seat (TASK, ACCEPTANCE, PING) | `hcom-dispatch <team> <from> <to> <pane> <line...>`                  | `hcom send @<to> --thread <team> --from <from> --json -- <line>`              |
| seat to the orchestrator (RESULT, PONG)         | the seat's own `hcom send --thread <team> -- '<line>'`, no target    | the thread the TASK seeded; an external sender is not addressable with `@`    |
| records                                         | `bus-history.sh <team> [--limit <n>] [--since <ts>] [--kind <kind>]` | `hcom events --type message --thread <team> --full --last <n> [--after <ts>]` |

`<to>` is the seat's exact hcom name, so a seat hcom does not know fails with hcom's own `Error: No active agent for @<to>` (exit 1, stderr). hcom accepts any thread name for a mention send and `hcom start` sets no tag (`src/commands/start.rs:486`), so the team of a seat is not checked here; a malformed team is refused by the grammar `^[a-z0-9][a-z0-9_-]{0,63}$`. The pane argument is accepted for agmsg-dispatch's form and unused: hcom delivers to a bound seat itself.

### Receipt and history

`hcom-dispatch` prints one line, `id=<event id> at=<hcom ts> to=<to> kind=<first word>`, read back from the bus by exact id, so the row exists before the receipt does. `bus-history.sh` prints `id<TAB>at<TAB>from<TAB>to<TAB>kind<TAB>body`, ascending by id; `to` is hcom's `delivered_to` joined with commas (`-` when empty, as for a seat's thread reply) and `body` escapes backslash, tab, CR and LF as `\\`, `\t`, `\r` and `\n`, so a row is one line of five tabs.

### hcom 0.7.30 facts the scripts rest on

| Flag or behaviour                                                                   | Source                                                    |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `send @name -- text`, "Everything after -- is the message", `@name` exact base name | `hcom send --help`                                        |
| `--from <name>` external sender identity; the row's `from`                          | `src/commands/send.rs:96`, `:403`                         |
| `--json` receipt `{"delivered_to": [...], "event_id": N}` on stdout                 | `send.rs:1135`; observed                                  |
| `--thread <name>` routing; a thread without members is refused                      | `send.rs:300`                                             |
| `events --type message --thread --last --after --full --sql`                        | `hcom events --help`; `src/commands/events.rs:33, 39, 45` |
| `--last` is `ORDER BY id DESC LIMIT n`                                              | `events.rs:185`                                           |
| `HCOM_DIR` selects the store; `hcom.db` inside it                                   | `hcom start --help`; observed                             |
| an unknown `@name` fails with `Error: No active agent for @name`, exit 1            | observed                                                  |
| `hcom events` creates an absent store                                               | observed                                                  |

Observed means run on 2026-10-23 against hcom 0.7.30 in a scratch store. `tests/fixtures/hcom/events-u5team.jsonl` holds the captured rows and `tests/fixtures/hcom/fake-hcom.py` replays the dialect in CI, where hcom is absent; `tests/unit/test_hcom_dispatch.py` also runs the real binary in a private store when one is on PATH.
