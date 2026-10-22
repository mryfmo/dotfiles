# Validation: dotfiles-T129-hcom-dispatch-bus-a02

- **Producer:** worker (Claude seat a008, worktree worker-f), sandboxed Bash.
- **What follows:** every block holds commands as executed, each printed as `$ <command>`, then its verbatim output and `exit <status>`.
- **Masking:** the home directory is written `~`, the sandbox temporary directory `$TMPDIR`, and the Claude session id `<session id>`.
- **Stores:** every store probe ran against a disposable store under `$TMPDIR`; the live `~/.hcom` was never opened.

## 1. Amendment 2's denial probe: a file under the main checkout's `.agents/worklog/uv-tools/` from inside the seat sandbox

```text
$ date -u +%FT%TZ
2026-10-22T07:58:12Z
exit 0
$ git -C ~/Workspace/dotfiles rev-parse --show-toplevel
~/Workspace/dotfiles
exit 0
$ ls -ld ~/Workspace/dotfiles/.agents/worklog ~/Workspace/dotfiles/.agents/worklog/uv-tools
"~/Workspace/dotfiles/.agents/worklog/uv-tools": No such file or directory (os error 2)
Permissions Size User     Group Date Modified    Name
drwxr-xr-x@    - a0004262 staff 2026-10-22 12:02 ~/Workspace/dotfiles/.agents/worklog
exit 2
$ mkdir -p ~/Workspace/dotfiles/.agents/worklog/uv-tools
mkdir: ~/Workspace/dotfiles/.agents/worklog/uv-tools: Operation not permitted
exit 1
$ : > ~/Workspace/dotfiles/.agents/worklog/uv-tools-probe
(eval):1: operation not permitted: ~/Workspace/dotfiles/.agents/worklog/uv-tools-probe
exit 1
$ touch ~/Workspace/dotfiles/.agents/worklog/uv-tools/probe
touch: ~/Workspace/dotfiles/.agents/worklog/uv-tools/probe: No such file or directory
exit 1
$ ls -ld ~/Workspace/dotfiles/.agents/worklog/uv-tools
"~/Workspace/dotfiles/.agents/worklog/uv-tools": No such file or directory (os error 2)
exit 2
```

## 2. hcom version, entry, digest and the top-level, send, list and events help

```text
$ ~/.local/bin/hcom --version
→ hcom v0.7.31 available — run `hcom update`
hcom 0.7.30
exit 0
$ readlink -f ~/.local/bin/hcom
~/.local/share/uv/tools/hcom/bin/hcom
exit 0
$ shasum -a 256 $(readlink -f ~/.local/bin/hcom)
7cd012d9a4d369de313ca4935cccda1ada6c8ffcd5e42ffa7eaeecdff7fc580e  ~/.local/share/uv/tools/hcom/bin/hcom
exit 0
$ ~/.local/bin/hcom --help
→ hcom v0.7.31 available — run `hcom update`
hcom (hook-comms) v0.7.30 - multi-agent communication

Usage:
  hcom                                  TUI dashboard
  hcom <command>                        Run command

Launch:
  hcom [N] claude|gemini|codex|opencode|kilo|pi|omp|hermes|antigravity|cursor|kimi|copilot|qoder|grok [flags] [tool-args]
  hcom r <target>                       Resume stopped agent
  hcom f <target>                       Fork agent session (claude/codex/opencode/kilo/pi/omp/qoder/grok)
  hcom kill <name(s)|tag:T|all>         Kill + close terminal pane

Commands:
  send         Send message to your buddies
  listen       Block until message or event arrives
  list         Show agents, status, unread counts
  events       Query event stream, manage subscriptions
  bundle       Structured context packages for handoffs
  transcript   Read another agent's conversation
  start        Connect to hcom (run inside any AI tool)
  stop         Disconnect from hcom
  config       Get/set global and per-agent settings
  run          Execute workflow scripts
  relay        Cross-device sync + relay daemon
  archive      Query past hcom sessions
  reset        Archive and clear database
  hooks        Add or remove hooks
  status       Installation and diagnostics
  term         View/inject into agent PTY screens
  update       Check and apply updates

Identity:
  1. Run hcom start to get a name
  2. Use --name <name> on all hcom commands

Run 'hcom <command> --help' for details.
exit 0
$ ~/.local/bin/hcom send --help
→ hcom v0.7.31 available — run `hcom update`
Usage:
    send @name -- message text     Direct message
    send @name1 @name2 -- message  Multiple targets
    send -- message text           Broadcast to all
    send @name                     Message from stdin (pipe or heredoc)
    send @name --file <path>       Message from file
    send @name --base64 <encoded>  Message from base64 string

  Everything after -- is the message (no quotes needed).
  All flags must come before --.

Target matching:
    @luna                          exact base name
    @api-luna                      exact full name
    @api-                          all local agents with exact tag 'api'
    @luna:BOXE                     exact or uniquely prefixed remote agent
  Partial local names are rejected to avoid accidental fan-out.

Envelope:
    --intent <type>                request | inform | ack
    request: expect a response
    inform: FYI, no response needed
    ack: replying to a request (requires --reply-to)
    --reply-to <id>                Link to event ID (42 or 42:BOXE)
    --thread <name>                Threaded routing: seed recipients once, then reuse thread members
    broadcast + --thread reuses prior thread members; seed with @mentions first

Sender:
    --from <name>                  External sender identity
    -b                             Shorthand for --from bigboss
    --name <name>                  Your identity (agent name or UUID)

Output:
    --json                         JSON receipt; leaves mail unread
    --quiet                        No output; leaves mail unread

Inline bundle (attach structured context):
    --title <text>                 Create and attach bundle inline
    --description <text>           Bundle description (required with --title)
    --events <ids>                 Event IDs/ranges: 1,2,5-10
    --files <paths>                Comma-separated file paths
    --transcript <ranges>          Format: 3-14:normal,6:full,22-30:detailed
    --extends <id>                 Parent bundle (optional)
  See 'hcom bundle --help' for bundle details

Examples:
    hcom send @luna -- Hello there!
    hcom send @luna @nova --intent request -- Can you help?
    hcom send -- Broadcast message to everyone
    echo 'Complex message' | hcom send @luna
    hcom send @luna <<'EOF'
    Multi-line message with special chars
    EOF
exit 0
$ ~/.local/bin/hcom list --help
→ hcom v0.7.31 available — run `hcom update`
Usage:
  hcom list                       All alive agents, read receipts
    -v                             Verbose (directory, session, etc)
    --json                         JSON array of all agents
    --names                        Just names, one per line
    --format TPL                   Template per agent: --format '{name} {status}'
    Fields: name, base_name, status, status_context, status_detail,
    status_age_seconds, description, unread_count, tool, tag, directory,
    session_id, parent_name, agent_id, headless, created_at,
    hooks_bound, process_bound, transcript_path, background_log_file,
    launch_context

  hcom list [self|<name>]         Single agent details, including recorded session usage
    [field]                        Print specific field (status, directory, session_id, usage, ...)
    --json                         Output as JSON
    --sh                           Shell exports: eval "$(hcom list self --sh)"

  hcom list --stopped [name]      Stopped agents (from events)
    --all                          All stopped (default: last 20)

Status icons:
  ▶  active      processing, reads messages very soon
  ◉  listening   idle, reads messages in <1s
  ■  blocked     needs human approval
  ○  inactive    dead or stale
  ◦  unknown     neutral

Tool labels:
  [CLAUDE] [GEMINI] [CODEX] [OPENCODE] [KILO] [PI] [OMP] [ANTIGRAVITY] [CURSOR] [KIMI] [COPILOT] [QODER] [GROK]  hcom-launched, automatic delivery
  [CLAUDE*]   hooks or process not bound (starting up, or lost); see: list <name>
  [AD-HOC]    no hooks, checks messages manually
exit 0
$ ~/.local/bin/hcom events --help
→ hcom v0.7.31 available — run `hcom update`
Usage:
  Query the event stream (messages, status changes, file edits, lifecycle)

Query:
    events                         Last 20 events as JSON Lines (one object per line)
    --last N                       Limit count (default: 20)
    --all                          Include archived sessions
    --full                         Full event JSON (default: streamlined)
    --wait [SEC]                   Block until match (default: 60s)
    --sql EXPR                     Raw SQL WHERE (ANDed with flags)
    --remote-fetch --device ID     One-shot fetch from remote device

Filters (same flag repeated = OR, different flags = AND):
    --agent NAME                   Agent name
    --type TYPE                    message | status | life
    --status VAL                   listening | active | blocked
    --context PATTERN              tool:Bash | deliver:X (supports * wildcard)
    --action VAL                   created | started | ready | stopped | batch_launched | launch_failed | launch_blocked
    --cmd PATTERN                  Shell command (contains, ^prefix, =exact)
    --file PATH                    File write (*.py for glob, file.py for contains)
    --collision                    Two agents edit same file within 30s
    --from NAME                    Sender
    --participant NAME             Message sender or delivery recipient
    --mention NAME                 @mention target
    --intent VAL                   request | inform | ack
    --thread NAME                  Thread name
    --after TIME                   After timestamp (ISO-8601)
    --before TIME                  Before timestamp (ISO-8601)

Shortcuts:
    --idle NAME                    --agent NAME --status listening
    --blocked NAME                 --agent NAME --status blocked

Wait for a launch batch:
  hcom events launch [batch_id]   Block until batch reaches a terminal state (JSON LaunchResult)
    --timeout SEC                  Max seconds to wait (default: 30)
  Exit codes: 0 ready, 1 error/no_launches, 2 timeout/blocked

Subscribe (next matching event arrives as a message from [hcom-events]):
  hcom events sub list            List active subscriptions
  hcom events sub [filters]       Subscribe using filter flags
  hcom events sub "SQL WHERE"     Subscribe using raw SQL
    --once                         Auto-remove after first match
    --for <name>                   Subscribe on behalf of another agent
    --on-hit <text>                Also send this message each time it fires (@mentions ok)
    --as <name> / -b               Own the sub without an agent identity, e.g. from a shell (-b = bigboss)
    --device ID                    Install/list on a remote device (create requires --for, --as, or -b)
  hcom events unsub <id>          Remove a subscription
    --device ID                    Remove it from a remote device

Examples:
    hcom events --cmd git --agent peso
    hcom events sub --idle peso    Notified when peso goes idle
    hcom events sub --file '*.py' --once
                                   One-shot: next .py file write

SQL reference (events_v view):
    Base                           id, timestamp, type, instance
    msg_*                          from, text, scope, sender_kind, delivered_to[], mentions[], intent, thread, reply_to
    status_*                       val, context, detail
    life_*                         action, by, batch_id, reason

    type                           message, status, life
    msg_scope                      broadcast, mentions
    msg_sender_kind                instance, external, system
    status_context                 tool:X, deliver:X, approval, prompt, exit:X
    life_action                    created, started, ready, stopped, batch_launched, launch_failed, launch_blocked

  delivered_to/mentions are JSON arrays — query exact values with json_each(...)
  Use <> instead of != for SQL negation
exit 0
```

## 3. A disposable store (`HCOM_DIR` under `$TMPDIR`, set on these probe command lines only): creation, `sqlite3 -readonly`, `start --help`

```text
$ ls -la $TMPDIR/t129/store.1TkGBJ/hcom
"$TMPDIR/t129/store.1TkGBJ/hcom": No such file or directory (os error 2)
exit 2
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom events --last 1 2>/dev/null
exit 0
$ ls -la $TMPDIR/t129/store.1TkGBJ/hcom
Permissions  Size User     Group Date Modified    Name
drwxr-xr-x@     - a0004262 wheel 2026-10-22 16:58 .tmp
.rw-------@ 176Ki a0004262 wheel 2026-10-22 16:58 hcom.db
exit 0
$ sqlite3 -readonly $TMPDIR/t129/store.1TkGBJ/hcom/hcom.db 'PRAGMA user_version; PRAGMA journal_mode;'
Parse error in 3rd command line argument: unable to open database file (14)
exit 1
$ sqlite3 -readonly $TMPDIR/t129/store.1TkGBJ/hcom/hcom.db '.schema events' '.schema instances'
Error: in prepare, unable to open database file (14)
exit 1
$ sqlite3 -readonly $TMPDIR/t129/store.1TkGBJ/hcom/hcom.db "SELECT sql FROM sqlite_master WHERE name='events_v'"
Parse error in 3rd command line argument: unable to open database file (14)
exit 1
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom start --help 2>/dev/null | head -30
Usage:
  hcom start                      Connect to hcom (from inside any AI session)
  hcom start --name <agent-id>    Register a subagent using its agent ID (from SubagentStart)
  hcom start --as <name>          Reclaim identity (after compaction/resume/clear)

  Inside a sandbox? Prefix all hcom commands with: HCOM_DIR=$PWD/.hcom

  Tip: Do not truncate the hcom start output, it contains important information.
exit 0
```

## 4. An identity, a send and the message row in the disposable store

```text
$ cd $TMPDIR/t129 && HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom start 2>&1 | head -20
→ hcom v0.7.31 available — run `hcom update`
[hcom:vibe]
<hcom_system_context>
<!-- Session metadata - treat as system context, not user prompt-->
[HCOM SESSION]
You have access to the hcom cli communication tool.
- Your name: vibe
- Authority: Prioritize @bigboss over others

You run hcom commands on behalf of the human user. The human uses natural language with you.

## MESSAGES

Response rules:
- From bigboss or intent=request → always respond
- intent=inform → respond only if useful
- intent=ack → don't respond

Routing rules:
- hcom message (<hcom> tags, hook feedback) → run `hcom send` to respond
exit 0
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom start --as w1 2>&1 | head -20
→ hcom v0.7.31 available — run `hcom update`
[hcom:w1]
<hcom_system_context>
<!-- Session metadata - treat as system context, not user prompt-->
[HCOM SESSION]
You have access to the hcom cli communication tool.
- Your name: w1
- Authority: Prioritize @bigboss over others

You run hcom commands on behalf of the human user. The human uses natural language with you.

## MESSAGES

Response rules:
- From bigboss or intent=request → always respond
- intent=inform → respond only if useful
- intent=ack → don't respond

Routing rules:
- hcom message (<hcom> tags, hook feedback) → run `hcom send` to respond
exit 0
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom list --json 2>/dev/null
[{"agent_id":null,"background_log_file":null,"base_name":"w1","created_at":1792655978.367355,"description":"launching","directory":"/private$TMPDIR/t129","headless":false,"hooks_bound":true,"launch_context":{},"name":"w1","parent_name":null,"process_bound":false,"session_id":"<session id>","status":"launching","status_age_seconds":0,"status_context":"new","status_detail":"","tag":null,"tool":"adhoc","transcript_path":null,"unread_count":0}]
exit 0
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom send --from orch --json @w1 -- hello 2>&1
→ hcom v0.7.31 available — run `hcom update`
{"delivered_to":["w1"],"event_id":3}
exit 0
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom events --type message --full --last 5 2>/dev/null
{"data":{"delivered_to":["w1"],"from":"orch","mentions":["w1"],"scope":"mentions","sender_kind":"external","text":"hello"},"id":3,"instance":"ext_orch","ts":"2026-10-22T07:59:38.420536+00:00","type":"message"}
exit 0
```

## 5. Schema and `PRAGMA user_version`, read from a copy of the disposable store

```text
$ ls -la $TMPDIR/t129/store.1TkGBJ/hcom
Permissions  Size User     Group Date Modified    Name
drwxr-xr-x@     - a0004262 wheel 2026-10-22 16:59 .tmp
.rw-------@   791 a0004262 wheel 2026-10-22 16:59 config.toml
.rw-------@   123 a0004262 wheel 2026-10-22 16:59 env
.rw-------@ 176Ki a0004262 wheel 2026-10-22 16:59 hcom.db
exit 0
$ cp $TMPDIR/t129/store.1TkGBJ/hcom/hcom.db $TMPDIR/t129/copy-1792655994/hcom.db && ls $TMPDIR/t129/copy-1792655994
error: invalid value '$TMPDIR/t129/copy-1792655994' for '--icons [<WHEN>]'
  [possible values: always, auto, never]

For more information, try '--help'.
exit 2
$ sqlite3 $TMPDIR/t129/copy-1792655994/hcom.db 'PRAGMA user_version' 'PRAGMA journal_mode' '.schema events' '.schema instances'
18
wal
CREATE TABLE events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                instance TEXT NOT NULL,
                data TEXT NOT NULL
            );
CREATE INDEX idx_timestamp ON events(timestamp);
CREATE INDEX idx_type ON events(type);
CREATE INDEX idx_instance ON events(instance);
CREATE INDEX idx_type_instance ON events(type, instance);
CREATE TRIGGER events_fts_insert
            AFTER INSERT ON events BEGIN
                INSERT INTO events_fts(rowid, searchable) VALUES (
                    new.id,
                    COALESCE(json_extract(new.data, '$.text'), '') || ' ' ||
                    COALESCE(json_extract(new.data, '$.from'), '') || ' ' ||
                    COALESCE(new.instance, '') || ' ' ||
                    COALESCE(json_extract(new.data, '$.context'), '') || ' ' ||
                    COALESCE(json_extract(new.data, '$.detail'), '') || ' ' ||
                    COALESCE(json_extract(new.data, '$.action'), '') || ' ' ||
                    COALESCE(json_extract(new.data, '$.reason'), '')
                );
            END;
CREATE TABLE instances (
                name TEXT PRIMARY KEY,
                session_id TEXT UNIQUE,
                parent_session_id TEXT,
                parent_name TEXT,
                tag TEXT,
                last_event_id INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                status_time INTEGER DEFAULT 0,
                last_seen INTEGER DEFAULT 0,
                status_context TEXT DEFAULT '',
                status_detail TEXT DEFAULT '',
                last_stop INTEGER DEFAULT 0,
                directory TEXT,
                created_at REAL NOT NULL,
                transcript_path TEXT DEFAULT '',
                tcp_mode INTEGER DEFAULT 0,
                wait_timeout INTEGER,
                background INTEGER DEFAULT 0,
                background_log_file TEXT DEFAULT '',
                name_announced INTEGER DEFAULT 0,
                agent_id TEXT UNIQUE,
                running_tasks TEXT DEFAULT '',
                origin_device_id TEXT DEFAULT '',
                hints TEXT DEFAULT '',
                subagent_timeout INTEGER,
                tool TEXT DEFAULT 'claude',
                launch_args TEXT DEFAULT '',
                terminal_preset_requested TEXT DEFAULT '',
                terminal_preset_effective TEXT DEFAULT '',
                idle_since TEXT DEFAULT '',
                pid INTEGER DEFAULT NULL,
                launch_context TEXT DEFAULT '',
                FOREIGN KEY (parent_session_id) REFERENCES instances(session_id) ON DELETE SET NULL
            );
CREATE INDEX idx_session_id ON instances(session_id);
CREATE INDEX idx_parent_session_id ON instances(parent_session_id);
CREATE INDEX idx_parent_name ON instances(parent_name);
CREATE INDEX idx_created_at ON instances(created_at DESC);
CREATE INDEX idx_status ON instances(status);
CREATE UNIQUE INDEX idx_agent_id_unique ON instances(agent_id) WHERE agent_id IS NOT NULL;
CREATE INDEX idx_instances_origin ON instances(origin_device_id);
exit 0
$ sqlite3 $TMPDIR/t129/copy-1792655994/hcom.db "SELECT sql FROM sqlite_master WHERE name='events_v'"
CREATE VIEW events_v AS
            SELECT
                id, timestamp, type, instance, data,
                json_extract(data, '$.from') as msg_from,
                json_extract(data, '$.text') as msg_text,
                json_extract(data, '$.scope') as msg_scope,
                json_extract(data, '$.sender_kind') as msg_sender_kind,
                json_extract(data, '$.delivered_to') as msg_delivered_to,
                json_extract(data, '$.mentions') as msg_mentions,
                json_extract(data, '$.intent') as msg_intent,
                json_extract(data, '$.thread') as msg_thread,
                json_extract(data, '$.reply_to') as msg_reply_to,
                json_extract(data, '$.reply_to_local') as msg_reply_to_local,
                json_extract(data, '$.bundle_id') as bundle_id,
                json_extract(data, '$.title') as bundle_title,
                json_extract(data, '$.description') as bundle_description,
                json_extract(data, '$.extends') as bundle_extends,
                json_extract(data, '$.refs.events') as bundle_events,
                json_extract(data, '$.refs.files') as bundle_files,
                json_extract(data, '$.refs.transcript') as bundle_transcript,
                json_extract(data, '$.created_by') as bundle_created_by,
                json_extract(data, '$.status') as status_val,
                json_extract(data, '$.context') as status_context,
                json_extract(data, '$.detail') as status_detail,
                json_extract(data, '$.action') as life_action,
                json_extract(data, '$.by') as life_by,
                json_extract(data, '$.batch_id') as life_batch_id,
                json_extract(data, '$.reason') as life_reason
            FROM events
exit 0
$ sqlite3 $TMPDIR/t129/copy-1792655994/hcom.db 'SELECT name, tag, last_event_id, session_id IS NOT NULL FROM instances'
w1||1|1
exit 0
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom list --format '{name} {tag} {unread_count}' 2>/dev/null
w1  1
exit 0
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom config --help 2>/dev/null | head -40
Usage:
  hcom config                     Show effective config (with sources)
  hcom config <key>               Get one key
  hcom config <key> <value>       Set one key
  hcom config <key> --info        Detailed help for a key
    --json / --edit / --reset      JSON output / open in $EDITOR / archive + restore defaults

Per-agent:
  hcom config -i <name|self> [key] [val]
                                  tag, timeout, hints, subagent_timeout

Keys:
    tag                            Group/label (agents become tag-*)
    terminal                       Where new agent windows open
    hints                          Text appended to all messages agent receives
    notes                          Notes appended to agent bootstrap
    subagent_timeout               Subagent keep-alive seconds after task
    claude_args / gemini_args / codex_args / opencode_args / kilo_args / pi_args / omp_args / cursor_args / kimi_args / copilot_args / qoder_args / grok_args / hermes_args
                                   Default launch args per tool
    claude_delivery / copilot_delivery
                                   Idle delivery: inject (PTY, default) | native (claude: experimental mod, copilot: CLI extension)
    gemini_system_prompt / codex_system_prompt
                                   Default system prompt
    auto_approve                   Auto-approve safe hcom commands
    auto_subscribe                 Event auto-subscribe presets
    auto_trust_workspace           Auto-trust launch dir (skip folder-trust prompt)
    name_export                    Export agent name to custom env var
    title_mode                     Terminal/tab title: combined, label, or off

  hcom config <key> --info for details
  Precedence: defaults < config.toml < env vars
  Files: $TMPDIR/t129/store.1TkGBJ/hcom/config.toml, $TMPDIR/t129/store.1TkGBJ/hcom/config.env
  HCOM_DIR: isolate per project (see 'hcom reset --help')
exit 0
```

## 6. The read cursor: `listen` as the recipient moves `instances.last_event_id` (first attempt used a missing `timeout`)

```text
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom listen --help 2>/dev/null | head -25
Usage:
  hcom listen [timeout]           Block until message arrives
    [timeout]                      Timeout in seconds (alias for --timeout)
    --timeout N                    Timeout in seconds (default: 86400)
    --json                         Output messages as JSON

Filter flags:
  Supports all filter flags from 'events' command
  (--agent, --type, --status, --file, --cmd, --from, --intent, etc.)
  Run 'hcom events --help' for full list
  Filters combine with --sql using AND logic

SQL filter mode:
    --sql "type='message'"         Custom SQL against events_v
    --sql stopped:name             Preset: wait for agent to stop
    --idle NAME                    Shortcut: wait for agent to go idle

Exit codes:
    0                              Message received / event matched
    1                              Timeout or error

  Quick unread check: hcom listen 1
exit 0
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom timeout 5 ~/.local/bin/hcom listen --name w1 --timeout 1 2>&1 | head -10
zsh: command not found: timeout
exit 0
$ sqlite3 $TMPDIR/t129/copy-after-listen/hcom.db 'SELECT name, last_event_id, status, status_time, last_seen FROM instances'
w1|1|inactive|1792655978|0
exit 0
$ sqlite3 $TMPDIR/t129/copy-after-listen/hcom.db "SELECT id, timestamp, type, instance, data FROM events ORDER BY id"
1|2026-10-22T07:59:38.335674+00:00|life|vibe|{"action":"started","name":"vibe","tool":"adhoc"}
2|2026-10-22T07:59:38.367925+00:00|life|w1|{"action":"created","by":"unknown","is_hcom_launched":false,"is_subagent":false,"parent_name":""}
3|2026-10-22T07:59:38.420536+00:00|message|ext_orch|{"delivered_to":["w1"],"from":"orch","mentions":["w1"],"scope":"mentions","sender_kind":"external","text":"hello"}
exit 0
```

## 6b. The read cursor after `listen --json`

```text
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom listen --name w1 --timeout 1 --json 2>&1 | head -10
→ hcom v0.7.31 available — run `hcom update`
{"event_id":3,"from":"orch","intent":null,"reply_id":"3","text":"hello","thread":null}
exit 0
$ sqlite3 $TMPDIR/t129/copy-after-listen2/hcom.db 'SELECT name, last_event_id, status, status_time, last_seen FROM instances'
w1|3|inactive|1792656018|0
exit 0
$ sqlite3 $TMPDIR/t129/copy-after-listen2/hcom.db "SELECT id, timestamp, type, instance, data FROM events WHERE id > 3 ORDER BY id"
4|2026-10-22T08:00:18.802417+00:00|status|w1|{"context":"ready","new_context":"ready","new_detail":"","new_status":"listening","old_context":"new","old_detail":"","old_status":"inactive","position":1,"session":"<session id>","status":"listening","writer":"src/commands/listen.rs:115"}
5|2026-10-22T08:00:18.803454+00:00|status|w1|{"context":"message received","new_context":"message received","new_detail":"","new_status":"inactive","old_context":"ready","old_detail":"","old_status":"listening","position":3,"session":"<session id>","status":"inactive","writer":"src/commands/listen.rs:129"}
exit 0
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom list --format '{name} {unread_count}' 2>/dev/null
w1 0
exit 0
```

## 7. `hcom events` leaves every store file byte-identical; `--thread` stores `data.thread`

```text
$ HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom send --from orch --json @w1 -- second 2>/dev/null
{"delivered_to":["w1"],"event_id":6}
exit 0
$ env -i PATH=/usr/bin:/bin HOME=$TMPDIR/t129/fakehome HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom events --type message --full --last 50 2>&1
→ hcom v0.7.31 available — run `hcom update`
{"data":{"delivered_to":["w1"],"from":"orch","mentions":["w1"],"scope":"mentions","sender_kind":"external","text":"hello"},"id":3,"instance":"ext_orch","ts":"2026-10-22T07:59:38.420536+00:00","type":"message"}
{"data":{"delivered_to":["w1"],"from":"orch","mentions":["w1"],"scope":"mentions","sender_kind":"external","text":"second"},"id":6,"instance":"ext_orch","ts":"2026-10-22T08:01:37.436667+00:00","type":"message"}
exit 0
$ diff $TMPDIR/t129/before.txt $TMPDIR/t129/after.txt && echo store-unchanged
store-unchanged
exit 0
$ ls -la $TMPDIR/t129/store.1TkGBJ/hcom $TMPDIR/t129/fakehome 2>&1
"$TMPDIR/t129/fakehome": No such file or directory (os error 2)
Permissions  Size User     Group Date Modified    Name
drwxr-xr-x@     - a0004262 wheel 2026-10-22 16:59 .tmp
.rw-------@   791 a0004262 wheel 2026-10-22 16:59 config.toml
.rw-------@   123 a0004262 wheel 2026-10-22 16:59 env
.rw-------@ 176Ki a0004262 wheel 2026-10-22 17:01 hcom.db
exit 2
$ env -i PATH=/usr/bin:/bin HOME=$TMPDIR/t129/fakehome HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom events --type message --full --last 50 --sql "msg_thread = 'x'" 2>&1
→ hcom v0.7.31 available — run `hcom update`
exit 0
$ env -i PATH=/usr/bin:/bin HOME=$TMPDIR/t129/fakehome HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom send --from orch --json --thread dotfiles-conformance @w1 -- third 2>&1
→ hcom v0.7.31 available — run `hcom update`
{"delivered_to":["w1"],"event_id":7}
exit 0
$ env -i PATH=/usr/bin:/bin HOME=$TMPDIR/t129/fakehome HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom events --type message --full --last 50 --sql "msg_thread = 'dotfiles-conformance'" 2>&1
→ hcom v0.7.31 available — run `hcom update`
{"data":{"delivered_to":["w1"],"from":"orch","mentions":["w1"],"scope":"mentions","sender_kind":"external","text":"third","thread":"dotfiles-conformance"},"id":7,"instance":"ext_orch","ts":"2026-10-22T08:01:37.640223+00:00","type":"message"}
exit 0
```

## 8. An unknown target, and a body with a leading dash, a tab and both quotes

```text
$ env -i PATH=/usr/bin:/bin HOME=$TMPDIR/t129/fakehome HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom send --from orch --json @nobody -- x 2>&1
→ hcom v0.7.31 available — run `hcom update`
Error: No active agent for @nobody
Available: w1, bigboss
exit 1
$ env -i PATH=/usr/bin:/bin HOME=$TMPDIR/t129/fakehome HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom send --from orch --json @w1 -- $'-lead\ttab "dq" sq'"'"'' 2>&1
→ hcom v0.7.31 available — run `hcom update`
{"delivered_to":["w1"],"event_id":8}
exit 0
$ env -i PATH=/usr/bin:/bin HOME=$TMPDIR/t129/fakehome HCOM_DIR=$TMPDIR/t129/store.1TkGBJ/hcom ~/.local/bin/hcom events --type message --full --last 1 2>/dev/null
{"data":{"delivered_to":["w1"],"from":"orch","mentions":["w1"],"scope":"mentions","sender_kind":"external","text":"-lead\ttab \"dq\" sq'"},"id":8,"instance":"ext_orch","ts":"2026-10-22T08:02:45.700391+00:00","type":"message"}
exit 0
```
