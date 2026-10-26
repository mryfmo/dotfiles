#!/usr/bin/env python3
"""One fake for `hcom`, `herdr`, `omp` and `srt` in the hcom-seat tests; the test copies it under each name.

Every call appends `{"argv": [...], "argv0": ..., "cwd": ..., "env": {HCOM_*}}` as one JSON line to `$FAKE_CALLS/<tool>`;
`argv0` is the path the fake was run by, so a test sees whether a launch ran the physical file or a link to it;
`path` is its PATH and `git_config` the `GIT_CONFIG_COUNT`/`_KEY_n`/`_VALUE_n` environment it was given; `git_env`
names every other `GIT_*` variable it was given.
`hcom omp` plays hcom 0.7.30's `--go` gate (without `--go` it prints the launch preview and starts nothing, as hcom
does inside an AI tool, `src/commands/launch.rs:48` at v0.7.30) and its herdr terminal preset (`herdr tab create
--label <tag>`, then `herdr pane run <pane> ...`): the omp tool-args after `--` run in `--dir` with HCOM_LAUNCHED=1
and HCOM_TAG set, the `--` itself dropped as hcom's `extract_launch_flags` drops it (`src/commands/launch.rs:572-581`
at v0.7.30), HCOM_DIR inherited and HCOM_TEAM dropped, as the real hcom drops it (the U33 pilot's pane showed
HCOM_TEAM unset after hcom-seat exported it). `herdr pane run` executes the command it is given. `omp` records and
exits 0. `srt --settings <file> -- <command...>` (regime-cutover U85) plays the sandbox without one. The seat
shim's canary (`/bin/sh -c <script> canary <write> <read> <ssh>`) runs its script for real, under `$FAKE_SRT_SH`
when set (`dash` in the POSIX-shell test) and with the three paths swapped for ones under a directory that does not
exist, so the probes fail as the sandbox makes them fail; `$FAKE_SRT_CANARY`, when set, is printed instead. Any other
command is executed. `bwrap`, `socat` and `rg` only exist on PATH for the Linux prerequisite check.
"""

import json
import os
import subprocess
import sys

tool = os.path.basename(sys.argv[0])
argv = sys.argv[1:]
with open(os.path.join(os.environ["FAKE_CALLS"], tool), "a", encoding="utf-8") as calls:
    hcom_env = {key: value for key, value in os.environ.items() if key.startswith("HCOM_")}
    git_config = {
        k: v
        for k, v in os.environ.items()
        if k == "GIT_CONFIG_COUNT" or k.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))
    }
    record = {"argv": argv, "argv0": sys.argv[0], "cwd": os.getcwd(), "env": hcom_env, "path": os.environ.get("PATH")}
    record["git_config"] = git_config
    record["git_env"] = sorted(k for k in os.environ if k.startswith("GIT_") and k not in git_config)
    calls.write(json.dumps(record) + "\n")

if tool == "hcom" and argv[:1] == ["omp"] and "--" in argv:
    flags, tool_args = argv[1 : argv.index("--")], argv[argv.index("--") + 1 :]
    if "--go" not in flags:
        print("== LAUNCH PREVIEW ==\nAdd --go to proceed.")
        sys.exit(0)
    flags.remove("--go")
    option = {flags[i]: flags[i + 1] for i in range(0, len(flags), 2)}
    if option.get("--terminal") != "herdr":
        sys.exit(f"fake-hcom: terminal preset {option.get('--terminal')} is not played here")
    env = {key: value for key, value in os.environ.items() if key != "HCOM_TEAM"}
    env.update({"HCOM_LAUNCHED": "1", "HCOM_TAG": option["--tag"]})
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
elif tool == "srt":
    command = argv[argv.index("--") + 1 :]
    if command[:2] == ["/bin/sh", "-c"]:
        if "FAKE_SRT_CANARY" in os.environ:
            print(os.environ["FAKE_SRT_CANARY"])
            sys.exit(0)
        denied = ["/nonexistent-u85/canary", "/nonexistent-u85/settings", "/nonexistent-u85/.ssh"]
        shell = os.environ.get("FAKE_SRT_SH", "/bin/sh")
        sys.exit(subprocess.run([shell, "-c", command[2], command[3], *denied], check=False).returncode)
    os.execvp(command[0], command)
elif tool not in ("herdr", "omp", "hcom", "bwrap", "socat", "rg"):
    sys.exit(f"fake-tool: unknown tool {tool}")
