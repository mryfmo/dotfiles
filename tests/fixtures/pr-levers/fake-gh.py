#!/usr/bin/env python3
"""A fake `gh` for tests/unit/test_pr_levers.py: records its argv and answers from a response table.

FAKE_GH_CALLS names the file that gets one JSON argv list per call. FAKE_GH_RESPONSES names a JSON list of
`{"match": <regex>, "json": <value> | "stdout": <text>, "exit": <n>, "stderr": <text>, "seq": [<entry>, ...]}`;
the first entry whose regex `re.search`es the argv joined by spaces (the `--jq` expression left out) answers. A
`seq` entry answers with its items in turn, the last one repeating; FAKE_GH_STATE holds the counters. A `json`
answer goes through the call's `--jq` expression with FAKE_GH_JQ (a jq or gojq, as gh embeds gojq), else it is
printed as JSON. An argv no entry matches exits 9, so an unexpected call fails the test.
"""

import json
import os
import re
import subprocess
import sys

argv = sys.argv[1:]
with open(os.environ["FAKE_GH_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(argv) + "\n")
jq = None
if "--jq" in argv:
    at = argv.index("--jq")
    jq = argv[at + 1]
    argv = argv[:at] + argv[at + 2 :]
joined = " ".join(argv)
with open(os.environ["FAKE_GH_RESPONSES"], encoding="utf-8") as table:
    responses = json.load(table)
for index, entry in enumerate(responses):
    if re.search(entry["match"], joined):
        break
else:
    sys.exit(f"fake-gh: unexpected call {argv}")
if "seq" in entry:
    state_path = os.environ["FAKE_GH_STATE"]
    state = {}
    if os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as saved:
            state = json.load(saved)
    turn = state.get(str(index), 0)
    state[str(index)] = turn + 1
    with open(state_path, "w", encoding="utf-8") as out:
        json.dump(state, out)
    entry = entry["seq"][min(turn, len(entry["seq"]) - 1)]
sys.stderr.write(entry.get("stderr", ""))
if entry.get("exit", 0):
    sys.exit(entry["exit"])
if "json" in entry:
    text = json.dumps(entry["json"])
    if jq is not None:
        run = subprocess.run(
            [os.environ["FAKE_GH_JQ"], "-r", jq], input=text, capture_output=True, text=True, check=False
        )
        sys.stderr.write(run.stderr)
        sys.stdout.write(run.stdout)
        sys.exit(run.returncode)
    print(text)
else:
    sys.stdout.write(entry.get("stdout", ""))
