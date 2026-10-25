#!/usr/bin/env python3
"""A fake `bun` for the unit tests: records the call, then prints a canned provider overlay.

Every call appends one JSON line `{"argv": [...], "cwd": ..., "cwd_entries": [...]}` to `$FAKE_OMP_CALLS/bun`.
The stdout is `FAKE_BUN_STDOUT` when set, else `{"disabledProviders": ["native", "agents", "cline"]}`;
`FAKE_BUN_EXIT` is the exit status (default 0). The real script is exercised by the test that runs the real bun.
"""

import json
import os
import sys

with open(os.path.join(os.environ["FAKE_OMP_CALLS"], "bun"), "a", encoding="utf-8") as calls:
    calls.write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd(), "cwd_entries": sorted(os.listdir())}) + "\n")
print(os.environ.get("FAKE_BUN_STDOUT", '{"disabledProviders": ["native", "agents", "cline"]}'))
sys.exit(int(os.environ.get("FAKE_BUN_EXIT", "0")))
