#!/usr/bin/env python3
"""A fake `codex` for tests/unit/test_pr_audit.py: records each call and plays `codex sandbox` and `codex exec`.

FAKE_CODEX_CALLS names the file that gets one JSON object per call: the argv, the cwd, HOME, CODEX_HOME, TMPDIR, the
XDG base-directory variables it saw, the text of `$CODEX_HOME/config.toml` and the target of `$CODEX_HOME/auth.json`.
`sandbox` runs the lever's real read and write probe script under an emulated sandbox: `/bin/sh` with links to
`sandbox-tool.py` as `cat`, `ls` and `mkdir` first on PATH, reading only the absolute `read` and `write` paths of its
config and writing only the `write` ones and TMPDIR (`:tmpdir`); FAKE_CODEX_PROBE `readable` also opens the first
`--read` path, `toolexit<n>` makes every denial a bare exit n (a tool that could not run), `controlexit<n>` fails every
tool call so, the positive controls included, and `failrun` exits 1 after a passing run. The network probe is
answered: curl exit 6 by default, `curl<n>` (curl exits n, e.g. `curl0` for a reachable network or `curl127` for a
curl that could not run) or `nocurl`. `exec`
reads the prompt from stdin into `prompt` of the record and writes FAKE_CODEX_VERDICT (default a finding-free
`Verdict: correct` message) to its `-o` file, then exits FAKE_CODEX_EXEC_EXIT (default 0). With FAKE_CODEX_REFRESH set,
`exec` first plays Codex's own token refresh: it rewrites `$CODEX_HOME/auth.json` in place (open with truncate, as
codex-cli 0.163.0 saves the login) with that value. With FAKE_CODEX_HANG naming a marker path, `exec` plays the
launcher whose native child outlives it: it starts a child that touches the marker after 3 seconds, records the call,
and sleeps 60 seconds.
"""

import json
import os
import re
import subprocess
import sys
import time

TOOL = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sandbox-tool.py")


def run_probe(script, args, config_text):
    """Run the probe script as `codex sandbox` would, under the emulated sandbox; return its output and status."""
    reads, writes = [], [os.environ["TMPDIR"]]
    for key, access in re.findall(r'^"(/[^"]*)" = "(read|write)"$', config_text, re.MULTILINE):
        (reads if access == "read" else writes).append(key)
    if mode == "readable":
        reads.append(args[args.index("--read") + 1])
    bindir = os.path.join(os.environ["TMPDIR"], "fake-sandbox-bin")
    os.makedirs(bindir, exist_ok=True)
    for name in ("cat", "ls", "mkdir"):
        if not os.path.lexists(os.path.join(bindir, name)):
            os.symlink(TOOL, os.path.join(bindir, name))
    env = {
        **os.environ,
        "PATH": f"{bindir}:{os.environ['PATH']}",
        "FAKE_SANDBOX_READ": os.pathsep.join(reads),
        "FAKE_SANDBOX_WRITE": os.pathsep.join(writes),
    }
    if mode.startswith("toolexit"):
        env["FAKE_SANDBOX_EXIT"] = mode[len("toolexit") :]
    if mode.startswith("controlexit"):
        env["FAKE_SANDBOX_EXIT_ALL"] = mode[len("controlexit") :]
    done = subprocess.run(["/bin/sh", "-c", script, "sh", *args], env=env, capture_output=True, text=True, check=False)
    return done.stdout + done.stderr, done.returncode


argv = sys.argv[1:]
codex_home = os.environ.get("CODEX_HOME", "")
record = {
    "argv": argv,
    "cwd": os.getcwd(),
    "env": {
        name: os.environ.get(name)
        for name in ("HOME", "CODEX_HOME", "TMPDIR", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME")
    },
}
config = os.path.join(codex_home, "config.toml")
if os.path.isfile(config):
    with open(config, encoding="utf-8") as handle:
        record["config"] = handle.read()
auth = os.path.join(codex_home, "auth.json")
if os.path.islink(auth):
    record["auth_link"] = os.readlink(auth)
elif os.path.exists(auth):
    record["auth_link"] = None
mode = os.environ.get("FAKE_CODEX_PROBE", "denied")
status = 0
if argv[:1] == ["sandbox"]:
    script = argv[argv.index("-c") + 1] if "-c" in argv else ""
    if "for p do" in script:
        args = argv[argv.index("-c") + 3 :]
        record["probe_paths"] = args
        output, status = run_probe(script, args, record.get("config", ""))
        record["probe_output"] = output
        sys.stdout.write(output)
    elif "curl" in script:
        if mode == "nocurl":
            print("pr-audit-probe: no curl")
        else:
            print(f"pr-audit-probe: curl {mode[4:] if mode.startswith('curl') else 6}")
    if mode == "failrun":
        status = 1
elif argv[:1] == ["exec"]:
    record["prompt"] = sys.stdin.read()
    marker = os.environ.get("FAKE_CODEX_HANG")
    if marker:
        subprocess.Popen(["/bin/sh", "-c", 'sleep 3; touch "$1"', "sh", marker])
        with open(os.environ["FAKE_CODEX_CALLS"], "a", encoding="utf-8") as calls:
            calls.write(json.dumps(record) + "\n")
        time.sleep(60)
    refreshed = os.environ.get("FAKE_CODEX_REFRESH")
    if refreshed is not None:
        with open(auth, "w", encoding="utf-8") as handle:
            handle.write(refreshed)
    out = argv[argv.index("-o") + 1]
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(
            os.environ.get("FAKE_CODEX_VERDICT", "No findings; the head meets its contract.\n\nVerdict: correct\n")
        )
    status = int(os.environ.get("FAKE_CODEX_EXEC_EXIT", "0"))
else:
    status = 9
with open(os.environ["FAKE_CODEX_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(record) + "\n")
sys.exit(status)
