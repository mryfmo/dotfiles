#!/usr/bin/env python3
"""A fake `hcom` 0.7.30 for the unit tests: `send --json` and `events` in the dialect captured on 2026-10-23.

The store is `$HCOM_DIR/events.jsonl`. Every call appends its argv as one JSON line to `$FAKE_HCOM_CALLS/argv`.
`FAKE_HCOM_AGENTS` (comma-separated) are the active agents; a mention of any other name fails as hcom does.
`FAKE_HCOM_HIDE_EVENTS=1` makes `events` print nothing, standing in for a row the bus lost.
As hcom does, the update notice goes to stderr and the receipt to stdout.
"""

import json
import os
import sys
from datetime import datetime, timezone

STORE = os.path.join(os.environ["HCOM_DIR"], "events.jsonl")


def option(flags, name):
    return flags[flags.index(name) + 1] if name in flags else None


def rows():
    if not os.path.exists(STORE):
        return []
    with open(STORE, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


with open(os.path.join(os.environ["FAKE_HCOM_CALLS"], "argv"), "a", encoding="utf-8") as calls:
    calls.write(json.dumps(sys.argv[1:]) + "\n")
print("→ hcom v0.7.31 available — run `hcom update`", file=sys.stderr)
command, flags = sys.argv[1], sys.argv[2:]
if command == "send":
    separator = flags.index("--")
    flags, text = flags[:separator], " ".join(flags[separator + 1 :])
    targets = [flag[1:] for flag in flags if flag.startswith("@")]
    agents = os.environ.get("FAKE_HCOM_AGENTS", "").split(",")
    missing = [target for target in targets if target not in agents]
    if missing:
        print(f"Error: No active agent for @{missing[0]}\nAvailable: {', '.join(agents)}", file=sys.stderr)
        sys.exit(1)
    event_id = max((row["id"] for row in rows()), default=0) + 1
    sender = option(flags, "--from")
    row = {
        "data": {
            "delivered_to": targets,
            "from": sender,
            "mentions": targets,
            "scope": "mentions",
            "sender_kind": "external",
            "text": text,
            "thread": option(flags, "--thread"),
        },
        "id": event_id,
        "instance": f"ext_{sender}",
        "ts": datetime.now(timezone.utc).isoformat(),
        "type": "message",
    }
    with open(STORE, "a", encoding="utf-8") as store:
        store.write(json.dumps(row) + "\n")
    print(json.dumps({"delivered_to": targets, "event_id": event_id}, separators=(",", ":")))
elif command == "events":
    if os.environ.get("FAKE_HCOM_HIDE_EVENTS"):
        sys.exit(0)
    thread, after, sql = option(flags, "--thread"), option(flags, "--after"), option(flags, "--sql")
    wanted = int(sql.split("=")[1]) if sql else None
    selected = [
        row
        for row in rows()
        if row["type"] == "message"
        and (thread is None or row["data"].get("thread") == thread)
        and (after is None or row["ts"] > after)
        and (wanted is None or row["id"] == wanted)
    ]
    for row in sorted(selected, key=lambda row: row["id"])[-int(option(flags, "--last") or 20) :]:
        print(json.dumps(row, separators=(",", ":"), sort_keys=True))
else:
    print(f"fake-hcom: unsupported command {command}", file=sys.stderr)
    sys.exit(2)
