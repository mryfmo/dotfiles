#!/usr/bin/env python3
"""A fake `omp` 18.11.3 for the unit tests: records the call, then prints a canned print-mode result.

Every call appends one JSON line `{"argv": [...], "cwd": ..., "home": ...}` to `$FAKE_OMP_CALLS/argv`; the run's
`GIT_DIR`, `GIT_WORK_TREE` and `TMPDIR`, the names in its cwd and the text of each `--config` overlay, in order, go to
`$FAKE_OMP_CALLS/env` the same way.
`FAKE_OMP_STDERR` is printed to stderr first, standing in for omp's own lines such as
`Failed to load extension <path>: <error>`; `FAKE_OMP_EXIT` is the exit status (default 0).
With `--mode json` the stdout is `stream.jsonl` next to this file, otherwise the text answer `PONG`. The tests run a
copy at `<package>/dist/cli.js`, the place of omp's own executable in its package.
"""

import json
import os
import sys
from pathlib import Path

argv = sys.argv[1:]
with open(os.path.join(os.environ["FAKE_OMP_CALLS"], "argv"), "a", encoding="utf-8") as calls:
    calls.write(json.dumps({"argv": argv, "cwd": os.getcwd(), "home": os.environ.get("HOME")}) + "\n")
with open(os.path.join(os.environ["FAKE_OMP_CALLS"], "env"), "a", encoding="utf-8") as env:
    names = {name: os.environ.get(name) for name in ("GIT_DIR", "GIT_WORK_TREE", "TMPDIR")}
    configs = [Path(argv[i + 1]).read_text(encoding="utf-8") for i, arg in enumerate(argv[:-1]) if arg == "--config"]
    env.write(json.dumps({**names, "cwd_entries": sorted(os.listdir()), "configs": configs}) + "\n")
if os.environ.get("FAKE_OMP_STDERR"):
    print(os.environ["FAKE_OMP_STDERR"], file=sys.stderr)
if "--mode" in argv and argv[argv.index("--mode") + 1] == "json":
    sys.stdout.write((Path(__file__).resolve().parent / "stream.jsonl").read_text(encoding="utf-8"))
else:
    print("PONG")
sys.exit(int(os.environ.get("FAKE_OMP_EXIT", "0")))
