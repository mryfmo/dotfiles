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

## `omp-run.sh`: one non-interactive omp turn per role

Plan 025 W6a (U8). The orchestrator seat, and the coordinator today, runs a headless omp turn in a seat role with one command. The script composes `omp --profile <role> --config ~/.agents/omp/policies/<role>.yml -e <dir>... --no-session --max-time <s> [--model <provider/id>] --mode <text|json> -p "<prompt file contents>"` (omp 18.11.3; `omp --help` lists every flag), runs it in `--cwd`, and fails closed: an unknown role, an absent or empty prompt file, an absent overlay, extension directory or cwd is exit 2 with the path, before omp starts. omp's stderr is held and replayed after the run; a `Failed to load extension <path>: <error>` line in it is exit 2 too, with the path in the refusal (U1 report F5). Otherwise omp's own exit status is returned. HOME is the caller's, so the seats run as the operator, and `--approval-mode` is never passed: the role's overlay owns it (`home/dot_agents/omp/policies/README.md`).

| Role           | Profile and overlay                                                       | Approval, from the overlay                                                                                          | Used for                                      |
| -------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `orchestrator` | `--profile orchestrator --config ~/.agents/omp/policies/orchestrator.yml` | `yolo`, merge and push rules in `bash.patterns`                                                                     | tasking, acceptance, the audited squash merge |
| `worker`       | `--profile worker --config ~/.agents/omp/policies/worker.yml`             | `yolo`, every push to `main` denied                                                                                 | implementing a unit in its worktree           |
| `audit`        | `--profile audit --config ~/.agents/omp/policies/audit.yml`               | `always-ask` with the write tools denied; a denied call returns omp's "requires approval" text to the model (#G1-2) | the read-only task-level audit of a head      |

`--mode text` (default) passes omp's own print-mode text through and `--mode json` passes its event stream through unchanged, one JSON object per line (`tool_execution_start`, `tool_execution_end`, `turn_end`, `agent_end`; measured in `.orchestration/validation/025-pilot-facts.md` #G1-3). Nothing is parsed, so a caller that wants only the final text reads the last `turn_end` of the JSON stream itself. Extensions default to the bridge `~/.local/lib/omp-extensions/pi-claude-bridge` and the SIWC `~/.agents/omp/extensions/openai-siwc`; `--ext <dir>` (repeatable) replaces that list. `--max-time` defaults to 600 seconds. omp reads a prompt that starts with `-` as a flag, so start a prompt file with a word or a heading.

```bash
# The audit seat reviews a head: JSON stream to a file, 15-minute bound.
scripts/orchestrator/omp-run.sh --role audit --prompt-file audit-U8.md --cwd /path/to/worktree --mode json --max-time 900 > audit-U8.jsonl

# The worker seat runs a task with a model override and the bridge staged elsewhere.
scripts/orchestrator/omp-run.sh --role worker --prompt-file task.md --cwd /path/to/worktree --model claude-bridge/claude-haiku-4-5 --ext /path/to/pi-claude-bridge
```

`tests/unit/test_omp_run.py` runs the script against `tests/fixtures/omp-run/fake-omp.py`, which records argv, cwd and HOME and replays `tests/fixtures/omp-run/stream.jsonl`; the real omp is never started by the tests.

### Threat table

The script starts a seat that acts under its role's policy on a caller-supplied prompt in a caller-supplied worktree, so it is trust-boundary code. Each test name is in `tests/unit/test_omp_run.py`.

| Control                                                   | Disposition                                                                                                                                                                                                                             |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `omp-run.sh`, the composed command                        | closed: `test_the_audit_argv_is_composed_field_by_field_and_the_json_stream_passes_through` (exact argv, `--approval-mode` absent) and `test_text_mode_the_timeout_and_the_two_extension_directories_are_the_defaults`                  |
| `omp-run.sh`, the refusals                                | closed: `test_missing_inputs_are_refused_before_omp_runs` (role, mode, prompt, overlay, extension directory, cwd, omp absent; nothing recorded) and `test_a_failed_extension_load_is_a_refusal_naming_the_path`                         |
| the `omp` executable                                      | closed: resolved by `command -v` and made absolute before the `cd`, so a relative PATH entry cannot pick `<cwd>/bin/omp` from a PR head; `test_omp_is_resolved_before_the_chdir_so_a_worktree_bin_cannot_replace_it`                    |
| the policy overlay                                        | closed: the file must exist here and omp's `--config` is strict (`home/dot_agents/omp/policies/README.md`); the `missing overlay` case of the refusal test                                                                              |
| the extension directories                                 | closed: each must exist, relative paths are made absolute before the `cd` (`test_a_relative_extension_path_is_made_absolute_before_the_chdir`), and a `Failed to load extension` line is exit 2                                         |
| the prompt file                                           | residual: the prompt reaches the model whole; what its tool calls may do is bounded by the role's overlay and omp's approval gate, not here; owner: the caller that writes the prompt                                                   |
| `--cwd` and the inherited HOME                            | residual: omp runs in the named worktree as the operator, reading the operator's `~/.agents/omp/policies`; the account and the worktree stay the boundary (U6, "approval is not containment"); owner: the seat policies                 |
| the orchestrator effect: a `yolo` seat acts on the prompt | residual: the orchestrator and worker overlays deny the merge, push and publish commands (`home/dot_agents/omp/policies/README.md`); `--approval-mode` is never widened here, asserted by the exact argv test; owner: the seat policies |
| `tests/unit/test_omp_run.py`                              | residual: runs only the fake under a scratch HOME, so a divergence from the real omp shows up in a live seat; owner: the first seat run                                                                                                 |
| `tests/fixtures/omp-run/fake-omp.py`, `stream.jsonl`      | residual: the stream's event names follow the measured #G1-3 run, not a verbatim capture; owner: the first seat run                                                                                                                     |
| `README.md`                                               | residual: prose; owner: this directory                                                                                                                                                                                                  |
