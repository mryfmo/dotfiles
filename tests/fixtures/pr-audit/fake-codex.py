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
reads the prompt from stdin into `prompt` of the record, reads the `--output-schema` file into `schema` of the record
(null when it cannot be read), and writes the verdict FAKE_CODEX_VERDICT_MODE names to its `-o` file: `conforming`
(the default: a finding-free `correct` object of the lever's schema), `contradiction` (`verdict: correct` with one P1
finding), `invalid-json` (the old free-text last line), `unknown-enum` (a verdict outside the enum) or `none` (no file
at all). FAKE_CODEX_VERDICT, when set, is written verbatim instead. It then exits FAKE_CODEX_EXEC_EXIT (default 0). With FAKE_CODEX_REFRESH set,
`exec` first plays Codex's own token refresh: it rewrites `$CODEX_HOME/auth.json` in place (open with truncate, as
codex-cli 0.163.0 saves the login) with that value. With FAKE_CODEX_HANG naming a marker path, `exec` plays the
launcher whose native child outlives it: it starts a child that touches the marker after 3 seconds, records the call,
and sleeps 60 seconds (FAKE_CODEX_HANG_DELAY replaces the 3). FAKE_CODEX_IGNORE_TERM makes that `exec` and its child ignore TERM (the child then touches the
marker after 8 seconds), so only a KILL stops them. The record then holds `pid` and `child_pid`.
FAKE_CODEX_ESCAPE=`single:<pidfile>` makes `exec` start a `sleep 30` in a session of its own (its own child), and
`double:<pidfile>` the same through a double fork (orphaned at once); the escaped pid goes to the pidfile, and `exec`
then sleeps 60 seconds.
"""

import json
import os
import re
import signal
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
    escape = os.environ.get("FAKE_CODEX_ESCAPE")
    if escape:
        mode, pidfile = escape.split(":", 1)
        if mode == "single":  # a child in a session of its own, still the child of this process
            subprocess.Popen(
                ["/bin/sh", "-c", 'echo $$ > "$1.tmp" && mv "$1.tmp" "$1" && exec sleep 30', "sh", pidfile],
                start_new_session=True,
            )
        else:  # a double fork: the grandchild, in a session of its own, is orphaned at once
            if os.fork() == 0:
                os.setsid()
                if os.fork() == 0:
                    os.execv(
                        "/bin/sh",
                        ["/bin/sh", "-c", 'echo $$ > "$1.tmp" && mv "$1.tmp" "$1" && exec sleep 30', "sh", pidfile],
                    )
                os._exit(0)
            os.wait()
        while not os.path.exists(pidfile):
            time.sleep(0.02)
        with open(os.environ["FAKE_CODEX_CALLS"], "a", encoding="utf-8") as calls:
            calls.write(json.dumps(record) + "\n")
        time.sleep(60)
    marker = os.environ.get("FAKE_CODEX_HANG")
    if marker:
        delay = os.environ.get("FAKE_CODEX_HANG_DELAY", "3")
        if os.environ.get("FAKE_CODEX_IGNORE_TERM"):
            signal.signal(signal.SIGTERM, signal.SIG_IGN)  # inherited by the child through exec
            delay = "8"
        child = subprocess.Popen(["/bin/sh", "-c", f'sleep {delay}; touch "$1"', "sh", marker])
        record["pid"] = os.getpid()
        record["child_pid"] = child.pid
        with open(os.environ["FAKE_CODEX_CALLS"], "a", encoding="utf-8") as calls:
            calls.write(json.dumps(record) + "\n")
        time.sleep(60)
    refreshed = os.environ.get("FAKE_CODEX_REFRESH")
    if refreshed is not None:
        with open(auth, "w", encoding="utf-8") as handle:
            handle.write(refreshed)
    if "--output-schema" in argv:
        try:
            with open(argv[argv.index("--output-schema") + 1], encoding="utf-8") as handle:
                record["schema"] = handle.read()
        except OSError:
            record["schema"] = None
    finding = {
        "priority": "P1",
        "confidence": "high",
        "path": "change.txt",
        "line": 1,
        "rationale": "A blocking finding.",
    }
    verdicts = {
        "conforming": json.dumps(
            {"verdict": "correct", "findings": [], "reproduced": ["python3 -m unittest: passed"], "notes": None}
        ),
        "contradiction": json.dumps({"verdict": "correct", "findings": [finding], "reproduced": [], "notes": None}),
        "invalid-json": "No findings; the head meets its contract.\n\nVerdict: correct\n",
        "unknown-enum": json.dumps({"verdict": "maybe", "findings": [], "reproduced": [], "notes": None}),
        "none": None,
    }
    text = os.environ.get("FAKE_CODEX_VERDICT", verdicts[os.environ.get("FAKE_CODEX_VERDICT_MODE", "conforming")])
    if text is not None:
        with open(argv[argv.index("-o") + 1], "w", encoding="utf-8") as handle:
            handle.write(text)
    status = int(os.environ.get("FAKE_CODEX_EXEC_EXIT", "0"))
else:
    status = 9
with open(os.environ["FAKE_CODEX_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(record) + "\n")
sys.exit(status)
