#!/usr/bin/env python3
"""A fake `hcom` for tests/unit/test_regime_start.py (U36), keeping its seats in the JSON file `$FAKE_HCOM_STATE`.

`list --format TPL` prints one line per alive seat with `{name}`, `{base_name}`, `{tag}`, `{status}` filled in;
`list --stopped <base>` prints hcom's named stop block for that base name, the newest event `(latest)`; `kill <name> --go` stops
an alive seat with hcom's `killed by:cli` record; `omp --tag T ... --go -- ...` records the launch and, unless
FAKE_LAUNCH_FAILS=1 (exit 1) or FAKE_LAUNCH_SILENT=1 (exit 0, no seat), adds a listening seat `T-<word>`.
FAKE_LIST_FAILS=1 makes every `list` exit 1; FAKE_STOPPED_GARBLED=1 prints a stop block without events; FAKE_LAUNCH_PAUSE=<path> makes a launch touch
`<path>.started` and wait for `<path>` before it adds the seat. Every call is appended to the state's `calls` with HCOM_DIR and
HCOM_TEAM.
"""

import json
import os
import sys
import time
from pathlib import Path

WORDS = ["rafa", "zulu", "mira", "tobi", "kale", "suna"]
state_path = Path(os.environ["FAKE_HCOM_STATE"])
state = json.loads(state_path.read_text()) if state_path.exists() else {"alive": [], "stopped": [], "calls": []}
argv = sys.argv[1:]
store = os.environ.get("HCOM_DIR")
state["calls"].append({"argv": argv, "HCOM_DIR": store, "HCOM_TEAM": os.environ.get("HCOM_TEAM")})
# Like the real hcom, every store has its own seats; a seat without a store belongs to the current one.
mine = [seat for seat in state["alive"] if seat.get("store", store) == store]


def save():
    state_path.write_text(json.dumps(state))


if argv[:1] == ["list"]:
    save()
    if os.environ.get("FAKE_LIST_FAILS") == "1":
        sys.exit("fake-hcom: list failed")
    if argv[1:2] == ["--stopped"] and len(argv) == 3:
        # hcom 0.7.30's named form (measured 2026-10-24): a detail block, then the events newest first.
        events = [
            record
            for record in reversed(state["stopped"])
            if record["base"] == argv[2] and record.get("store", store) == store
        ]
        if os.environ.get("FAKE_STOPPED_GARBLED") == "1":
            print(f"Stopped: {argv[2]}")
            sys.exit(0)
        if not events:
            print(f"No stopped agent named {argv[2]}")
            sys.exit(0)
        print(f"Stopped: {argv[2]}\n  Tool:       omp\n  Tag:        {events[0]['tag']}\n")
        print(f"  Stop history ({len(events)} events):")
        for index, record in enumerate(events):
            print(f"    1m ago  [{record['reason']}]" + (" (latest)" if index == 0 else ""))
        sys.exit(0)
    template = argv[argv.index("--format") + 1]
    for seat in mine:
        print(template.format(name=seat["name"], base_name=seat["base"], tag=seat["tag"], status=seat["status"]))
    sys.exit(0)
if argv[:1] == ["kill"]:
    seat = next((seat for seat in mine if seat["name"] == argv[1]), None)
    if seat is None:
        save()
        sys.exit(f"fake-hcom: no seat {argv[1]}")
    state["alive"].remove(seat)
    state["stopped"] += [{**seat, "reason": "exit:shutdown by:session"}, {**seat, "reason": "killed by:cli"}]
    save()
    sys.exit(0)
if argv[:1] == ["omp"] and "--go" in argv:
    tag = argv[argv.index("--tag") + 1]
    pause = os.environ.get("FAKE_LAUNCH_PAUSE")
    if pause:
        # The launch says it began, then holds until the test releases it (at most 60 s).
        Path(pause + ".started").touch()
        for _ in range(600):
            if Path(pause).exists():
                break
            time.sleep(0.1)
    if os.environ.get("FAKE_LAUNCH_FAILS") == "1":
        save()
        sys.exit("fake-hcom: launch failed")
    if os.environ.get("FAKE_LAUNCH_SILENT") != "1":
        used = {seat["base"] for seat in state["alive"] + state["stopped"]}
        word = next(word for word in WORDS if word not in used)
        state["alive"].append(
            {"name": f"{tag}-{word}", "base": word, "tag": tag, "status": "listening", "store": store}
        )
    save()
    sys.exit(0)
save()
sys.exit(f"fake-hcom: unhandled {argv}")
