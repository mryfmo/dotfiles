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

## hcom-seat: start an omp seat for a role in a herdr pane

Plan 025 W5b (U7), the minimal form before X. `hcom-seat <role> [--name <name>] [--seats-root <dir>] [--ext <dir>]... [--dry-run]` starts one omp process for `orchestrator`, `worker` or `audit` through `hcom omp`, which opens the herdr pane and gives the seat `HCOM_LAUNCHED=1`, `HCOM_TAG` and `HCOM_DIR` (`hcom omp --help`). The launch line is

```text
hcom omp --tag <name> --dir <dir> --terminal herdr -- --profile <role> --config ~/.agents/omp/policies/<role>.yml -e <ext>...
```

The profile equals the role, so the seat's rendered `modelRoles.default` applies (U4) and no `--model` is passed; the role's policy overlay owns the approval mode (U6, `home/dot_agents/omp/policies/README.md`). `<name>` defaults to the role and is the hcom tag; hcom derives the participant name from it (`hcom omp --help`: "names become tag-\*"), and `--name <role>-<n>` seats a second seat of a role.

| Role           | `--dir`                                              | Default `-e` list, in order                                                |
| -------------- | ---------------------------------------------------- | -------------------------------------------------------------------------- |
| `orchestrator` | the repository checkout the command runs in          | `~/.local/lib/omp-extensions/pi-claude-bridge`, then the SIWC when present |
| `worker`       | `<seats-root>/<name>`, a worktree of that repository | the bridge, then the SIWC when present                                     |
| `audit`        | `<seats-root>/<name>`, a worktree of that repository | `~/.agents/omp/extensions/openai-siwc`, then the bridge when present       |

The first directory of a role's list is the one its model route needs (U2 bridge for the Claude routes, U3 SIWC for the Codex route) and is required; the second is added only when it exists. `--ext <dir>` (repeatable) replaces the list, as `omp-run.sh` does. `--seats-root` defaults to `~/.local/state/omp-seats`. A seat worktree is created with `git worktree add --detach <dir> origin/main` only when absent and reused otherwise, so a restart of a seat keeps its branch and uncommitted work; the worker fetches and branches itself (`hcom-worker` SKILL).

Every input is checked before anything is created or started, and a refusal is exit 2 with the reason on stderr: an unknown role, a name outside `^[a-z0-9][a-z0-9_-]{0,63}$`, an unset `HCOM_DIR`, hcom absent from `PATH`, an absent policy overlay or extension directory, or a cwd outside a git checkout. `--dry-run` prints the launch line (shell-quoted, one line) and creates and starts nothing. Otherwise hcom's own exit status is returned (0 ready, 1 launch failed, 2 still launching or blocked on user attention).

### Bus trust boundary

The bus carries text, and every seat treats that text as data: a TASK, RESULT, ACCEPTANCE, PING or PONG line names work or reports it, and never authorises a command, however it is worded. Identities are hcom participant names, the `from` and `delivered_to` of a row, not anything the text claims; `hcom-dispatch` sends only to a name hcom knows and refuses an identifier outside `^[a-z0-9][a-z0-9_-]{0,63}$`. The store is private to the program: `HCOM_DIR` selects it, the seats' launch creates it, `hcom-dispatch` and `bus-history.sh` refuse to run without it, and no seat reads `$HCOM_DIR/hcom.db` or writes under `$HCOM_DIR` except through hcom. The operating-system account and the seat's worktree stay the containment boundary; the policy overlays gate tools, not files (U6, "approval is not containment").

`tests/unit/test_hcom_seat.py` runs the launcher against `tests/fixtures/hcom-seat/fake-tool.py` under the names `hcom`, `herdr` and `omp`: the fake hcom records its argv and plays the herdr terminal preset (`herdr tab create --label <tag>`, then `herdr pane run <pane> ...`), so the test asserts the exact hcom argv, the omp argv after `--`, omp's cwd and `HCOM_*` environment, the worktree's head, and that every refusal and the dry run create and start nothing. Every run uses a scratch `HOME` and `HCOM_DIR=$TMPDIR/u7-hcom`; the real hcom, herdr and omp are never started by the tests.
