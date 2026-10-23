#!/usr/bin/env python3
"""One fake for `hcom`, `herdr` and `omp` in the hcom-seat tests; the test symlinks it under each name.

Every call appends `{"argv": [...], "cwd": ..., "env": {HCOM_*}}` as one JSON line to `$FAKE_CALLS/<tool>`.
`hcom omp` plays hcom 0.7.30's herdr terminal preset (`herdr tab create --label <tag>`, then
`herdr pane run <pane> ...`): the omp tool-args after `--` run in `--dir` with HCOM_LAUNCHED=1 and HCOM_TAG set,
the `--` itself dropped as hcom's `extract_launch_flags` drops it (`src/commands/launch.rs:572-581` at v0.7.30),
HCOM_DIR inherited. `herdr pane run` executes the command it is given. `omp` records and exits 0.
"""

import json
import os
import subprocess
import sys

tool = os.path.basename(sys.argv[0])
argv = sys.argv[1:]
with open(os.path.join(os.environ["FAKE_CALLS"], tool), "a", encoding="utf-8") as calls:
    hcom_env = {key: value for key, value in os.environ.items() if key.startswith("HCOM_")}
    calls.write(json.dumps({"argv": argv, "cwd": os.getcwd(), "env": hcom_env}) + "\n")

if tool == "hcom" and argv[:1] == ["omp"] and "--" in argv:
    flags, tool_args = argv[1 : argv.index("--")], argv[argv.index("--") + 1 :]
    option = {flags[i]: flags[i + 1] for i in range(0, len(flags), 2)}
    if option.get("--terminal") != "herdr":
        sys.exit(f"fake-hcom: terminal preset {option.get('--terminal')} is not played here")
    env = {**os.environ, "HCOM_LAUNCHED": "1", "HCOM_TAG": option["--tag"]}
    pane = subprocess.run(
        ["herdr", "tab", "create", "--label", option["--tag"]], capture_output=True, text=True, check=False
    )
    sys.exit(
        subprocess.run(
            ["herdr", "pane", "run", pane.stdout.strip(), "omp", *tool_args],
            cwd=option["--dir"],
            env=env,
            check=False,
        ).returncode
    )
if tool == "herdr" and argv[:2] == ["tab", "create"]:
    print("w1:p9")
elif tool == "herdr" and argv[:2] == ["pane", "run"]:
    sys.exit(subprocess.run(argv[3:], check=False).returncode)
elif tool not in ("herdr", "omp", "hcom"):
    sys.exit(f"fake-tool: unknown tool {tool}")
