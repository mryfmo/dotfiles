#!/usr/bin/env python3
"""A fake `omp` 18.11.3 for the unit tests: records the call, then prints a canned print-mode result.

Every call appends one JSON line `{"argv": [...], "cwd": ..., "home": ...}` to `$FAKE_OMP_CALLS/argv`.
`FAKE_OMP_STDERR` is printed to stderr first, standing in for omp's own lines such as
`Failed to load extension <path>: <error>`; `FAKE_OMP_EXIT` is the exit status (default 0).
With `--mode json` the stdout is `stream.jsonl` next to this file, otherwise the text answer `PONG`.
"""

import json
import os
import sys
from pathlib import Path

argv = sys.argv[1:]
with open(os.path.join(os.environ["FAKE_OMP_CALLS"], "argv"), "a", encoding="utf-8") as calls:
    calls.write(json.dumps({"argv": argv, "cwd": os.getcwd(), "home": os.environ.get("HOME")}) + "\n")
if os.environ.get("FAKE_OMP_STDERR"):
    print(os.environ["FAKE_OMP_STDERR"], file=sys.stderr)
if "--mode" in argv and argv[argv.index("--mode") + 1] == "json":
    sys.stdout.write((Path(__file__).resolve().parent / "stream.jsonl").read_text(encoding="utf-8"))
else:
    print("PONG")
sys.exit(int(os.environ.get("FAKE_OMP_EXIT", "0")))
