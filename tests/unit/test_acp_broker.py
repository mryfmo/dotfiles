"""Exercise scripts/orchestrator/acp-broker, its relay helper acp-relay.py and the thin client acp-seat (regime-cutover
U343, M-24 part 1; the slot-clone interface of U343e) on the scratch host of tests/unit/test_hcom_seat.py.

The broker runs outside every sandbox and starts one `srt -- omp acp` per connection on a real Unix socket, so the
tests connect to that socket (raw, and through the client) and read what comes back. srt and omp are fakes on PATH:
the fake srt takes its instructions from a file beside it (the broker runs it under `/usr/bin/env -i`, so the
environment carries nothing), answers the canary, and execs the command it is given (the isolated git the broker runs
inside the Router's settings included, so the clone and the push run for real against a scratch repository); the fake
omp records what reached it and echoes its stdin line by line. The Router's slot (its state slot, scratch cwd and the
settings `hcom-seat` renders) is written by hand in the dsh row's shape for most tests, and by a real held `hcom-seat
router` launch for the settings compare. Nothing real starts; nothing outside the scratch is written.
"""

import difflib
import errno
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import re
import select
import shutil
import signal
import socket
import stat
import subprocess
import sys
import textwrap
import threading
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_hcom_seat  # the fixture, as a module attribute so its tests are not collected twice
import test_hcom_seat_dsh  # the dsh fakes, the same way
from scratch_git import git_init

ROOT = test_hcom_seat.ROOT
BROKER = ROOT / "scripts/orchestrator/acp-broker"
CLIENT = ROOT / "scripts/orchestrator/acp-seat"
RELAY = ROOT / "scripts/orchestrator/acp-relay.py"
SYSTEM_PATH = test_hcom_seat.SYSTEM_PATH
BASH_OWN_NAMES = test_hcom_seat_dsh.BASH_OWN_NAMES
FOUR_WORDS = "write-denied read-denied ssh-denied debug-denied"
# The connection's first line (U343g): the broker names the slot, whose name is the record's under `<state>/broker/`.
RECORD_LINE = re.compile(rb"\Aacp-broker: record (acp-[a-z0-9][a-z0-9_-]*-\d{8}-\d{6}-\d+)\n\Z")
SLOT_PARTS = re.compile(r"^acp-(.+)-(\d{8}-\d{6}-\d+)$")
# The reaper's grace between TERM and KILL to omp's process group, `reaper_grace` in the broker (seconds).
GRACE = 5
# The ceiling of every reaper-timing wait and bound (seconds, U440): fixed and generous, not derived from the runner's
# load, so the tests prove "bounded" on any machine and leave the grace's design value to the lever (U441).
REAPER_CEILING = 60
PUSHED_REF = re.compile(r"^refs/acp-seat/([a-z0-9][a-z0-9_-]*)/(\d{8}-\d{6}-\d+)$")
PROJECT_FILES = (".claude/settings.json", ".claude/settings.local.json", ".claude/hooks", ".claude/contextdb", ".omp",
                 ".codex", ".envrc", ".mcp.json")  # fmt: skip
CLAUDE_ROWS = ("settings.json", "settings.local.json", "rules", "hooks", "plugins", "skills", "commands", "agents")
DOMAINS = ["github.com", "api.github.com", "uploads.github.com", "codeload.github.com", "objects.githubusercontent.com",
           "raw.githubusercontent.com", "release-assets.githubusercontent.com", "pypi.org", "files.pythonhosted.org",
           "api.anthropic.com", "claude.ai", "platform.claude.com", "console.anthropic.com", "chatgpt.com",
           "auth.openai.com", "api.openai.com"]  # fmt: skip
PING = b'{"jsonrpc":"2.0","id":1,"method":"ping"}\n'
# The protected host file a Router-planted link points at (U343h; the auditor's reproduction used a scratch `.aws` file).
VICTIM = b"[default]\naws_access_key_id = AKIAEXAMPLE\n# the protected host file a planted link points at\n"
# The fixture's API key file (regime-cutover U516): the bytes `claude-keyed` would read inside the worker; the broker
# holds the path alone, so the distinctive mark must appear in no output of the broker's (the launch log, its streams,
# the worker's launch record).
KEY_MARK = "U516FIXTUREKEYNEVERINANYLOG"
FIXTURE_KEY = f"sk-ant-api03-{KEY_MARK}_000000000000000000000000\n"

# The fake srt: records argv, environment names and cwd; `--version` answers 0.0.81; when `swap-ancestor` exists
# beside the calls it performs the swap that file describes (the Router replacing an ancestor of its repository:
# `ancestor` renamed to `moved`, then a link to `link` put at the name when one is given) at the moment its `at`
# names: `first`, before the first srt call of any kind (the clone's read of the repository, so the clone fails), or
# `canary`, before the canary (after the clone); the swap runs once and the file is consumed. The canary (`/bin/sh
# -c <script> canary <write> <read> <ssh> <debug>`) prints `canary-answer` when that file exists, writes the canary
# file first when `canary-write` exists (a sandbox that lets the write probe succeed), exits 3 when `srt-fail`
# exists (a canary that did not run), else runs the script with the four paths swapped for ones under a directory
# that does not exist, so the probes fail as the sandbox makes them fail; any other command (omp, the isolated git
# the broker runs inside the Router's settings or the worker's) is executed. Two instructions apply to a command
# under a slot's `settings.json` (the worker's settings; the Router's file is `srt-settings.json`), the way the real
# sandbox would act on it (U343f): `pack-sleep` holds a number of seconds a `pack-objects` sleeps before it runs (a
# push in flight for the signal test), and `deny-paths` lists paths made unreadable (mode 0) for the span of the
# command and restored after it (the paths the worker's settings deny; a store named by a planted alternates file).
# One instruction applies to a `pack-objects` under the Router's settings (U343o): `clone-sleep` holds the clone's
# pack that many seconds, `clone-sleeping` written first (a connection held before the canary for the signal test).
FAKE_SRT = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, subprocess, sys, time
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "srt.json")))
    argv = sys.argv[1:]
    with open(os.path.join(conf["calls"], "srt"), "a") as calls:
        calls.write(json.dumps({"argv": argv, "argv0": sys.argv[0], "env": sorted(os.environ), "cwd": os.getcwd()}) + "\\n")
    if argv == ["--version"]:
        print("0.0.81")
        sys.exit(0)
    command = argv[argv.index("--") + 1 :]
    canary = command[:2] == ["/bin/sh", "-c"]
    worker = argv[:1] == ["--settings"] and argv[1].endswith("/settings.json")
    swap = os.path.join(conf["calls"], "swap-ancestor")
    if os.path.exists(swap):
        plan = json.load(open(swap))
        if plan.get("at", "canary") == "first" or canary:
            os.rename(plan["ancestor"], plan["moved"])
            if plan["link"]:
                os.symlink(plan["link"], plan["ancestor"])
            os.unlink(swap)
    if canary:
        if os.path.exists(os.path.join(conf["calls"], "srt-fail")):
            sys.exit(3)
        if os.path.exists(os.path.join(conf["calls"], "canary-write")):
            open(command[4], "w").close()
        answer = os.path.join(conf["calls"], "canary-answer")
        if os.path.exists(answer):
            print(open(answer).read().strip())
            sys.exit(0)
        denied = ["/nonexistent-u343/canary", "/nonexistent-u343/settings", "/nonexistent-u343/.ssh",
                  "/nonexistent-u343/.claude/debug/canary"]
        sys.exit(subprocess.run(["/bin/sh", "-c", command[2], command[3], *denied], check=False).returncode)
    sleep = os.path.join(conf["calls"], "pack-sleep")
    if worker and "pack-objects" in command and os.path.exists(sleep):
        with open(os.path.join(conf["calls"], "pack-sleeping"), "w") as marker:
            marker.write(str(os.getpid()))
        time.sleep(float(open(sleep).read()))
    hold = os.path.join(conf["calls"], "clone-sleep")
    if not worker and "pack-objects" in command and os.path.exists(hold):
        with open(os.path.join(conf["calls"], "clone-sleeping"), "w") as marker:
            marker.write(str(os.getpid()))
        time.sleep(float(open(hold).read()))
    deny = os.path.join(conf["calls"], "deny-paths")
    if worker and os.path.exists(deny):
        paths = open(deny).read().split()
        for path in paths:
            os.chmod(path, 0)
        try:
            sys.exit(subprocess.run(command, check=False).returncode)
        finally:
            for path in paths:
                os.chmod(path, 0o700)
    os.execvp(command[0], command)
    """
)
# The fake omp: records argv, argv0, cwd and the whole environment; `--version` prints 18.12.6 (exit `omp-version-
# status` when that file exists); `acp` writes its pid to `omp-pid`, ignores TERM when `omp-ignore-term` exists (the
# TERM-ignoring worker of verdict U343f-22a81500 P1 :1233), starts a sleeping descendant when `omp-child` exists (its
# pid written to `omp-child-pid`, the tool child of the verdict's P2 at acp-broker:1079), echoes stdin line by line
# until EOF, then writes the bytes of `omp-tail` when that file exists (a worker's unterminated last output, P1
# :1347) and exits `omp-status` when that file exists.
FAKE_OMP = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, signal, subprocess, sys
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "omp.json")))
    calls = conf["calls"]
    with open(os.path.join(calls, "omp"), "a") as record:
        record.write(json.dumps({"argv": sys.argv[1:], "argv0": sys.argv[0], "cwd": os.getcwd(),
                                 "env": dict(os.environ)}) + "\\n")
    if sys.argv[1:] == ["--version"]:
        status = os.path.join(calls, "omp-version-status")
        if os.path.exists(status):
            sys.exit(int(open(status).read()))
        print("18.12.6")
        sys.exit(0)
    with open(os.path.join(calls, "omp-pid"), "w") as handle:
        handle.write(str(os.getpid()))
    if os.path.exists(os.path.join(calls, "omp-ignore-term")):
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    if os.path.exists(os.path.join(calls, "omp-child")):
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
        with open(os.path.join(calls, "omp-child-pid"), "w") as handle:
            handle.write(str(child.pid))
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            break
        sys.stdout.buffer.write(line)
        sys.stdout.buffer.flush()
    tail = os.path.join(calls, "omp-tail")
    if os.path.exists(tail):
        sys.stdout.buffer.write(open(tail, "rb").read())
        sys.stdout.buffer.flush()
    status = os.path.join(calls, "omp-status")
    sys.exit(int(open(status).read()) if os.path.exists(status) else 0)
    """
)
# The bind-race winner (U343j test (a), verdict U343i-76a5c83b P1 `acp-broker:1061`): a listener of the test's that
# stands for a broker which bound `sock` first, with one record no client read yet and one reaper temporary beside
# it; it writes its pid to `winner-pid`, then `winner-ready`, and answers every connection with one line.
BIND_WINNER = textwrap.dedent(
    """\
    import os, socket, sys
    sock, calls = sys.argv[1], sys.argv[2]
    directory, base = os.path.split(sock)
    os.chdir(directory)
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(base)
    os.chmod(base, 0o600)
    listener.listen(4)
    with open(os.path.join(directory, "acp-w9-20260101-000000-1"), "w") as record:
        record.write("ref=refs/acp-seat/w9/20260101-000000-1\\nreaper=1\\n")
    with open(os.path.join(directory, "acp-w9-20260101-000000-1.tmp"), "w") as temp:
        temp.write("")
    with open(os.path.join(calls, "winner-pid"), "w") as handle:
        handle.write(str(os.getpid()))
    with open(os.path.join(calls, "winner-ready"), "w") as handle:
        handle.write("")
    while True:
        conn, _ = listener.accept()
        conn.sendall(b"winner\\n")
        conn.close()
    """
)
# The fake python3 of the bind-race tests: a `#!/bin/sh` wrapper the broker pins as `/bin/sh <file>`; when
# `bind-loser` exists beside the calls and the relay is what it is asked to run, it starts the winner on the socket
# the relay was given (`$4`) and waits for it, then runs the real interpreter with the same arguments, so the real
# relay's bind fails exactly as a second broker's does after both passed the take; every other run (the record
# helper's) goes straight to the real interpreter. The winner's stdio is detached, so it holds no pipe of the broker's.
FAKE_PYTHON3 = textwrap.dedent(
    """\
    #!/bin/sh
    real={python}
    calls={calls}
    case $3 in
    */acp-relay.py)
        if [ -e "$calls/bind-loser" ]; then
            rm -f "$calls/bind-loser"
            "$real" {winner} "$4" "$calls" > /dev/null 2>&1 < /dev/null &
            while [ ! -e "$calls/winner-ready" ]; do sleep 0.02; done
        fi
        ;;
    esac
    exec "$real" "$@"
    """
)


def one_mib_line():
    """A JSON-RPC line of exactly 1 MiB, the relay client of the U342 spike."""
    head = '{"jsonrpc":"2.0","id":7,"method":"session/prompt","params":{"blob":"'
    tail = '"}}\n'
    size = 1024 * 1024
    blob = ("0123456789abcdef" * ((size - len(head) - len(tail)) // 16 + 1))[: size - len(head) - len(tail)]
    line = (head + blob + tail).encode()
    assert len(line) == size and json.loads(line)["params"]["blob"] == blob
    return line


def load_relay():
    """acp-relay.py as a module (its `main` is guarded), for the table test of `map_session_cwd` (U449b)."""
    spec = importlib.util.spec_from_file_location("acp_relay", RELAY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AcpBrokerTest(test_hcom_seat.SeatFixture):
    def setUp(self):
        super().setUp()
        for tool, text in (("srt", FAKE_SRT), ("omp", FAKE_OMP)):
            (self.bindir / tool).write_text(text)
            (self.bindir / tool).chmod(0o755)
            (self.bindir / f"{tool}.json").write_text(json.dumps({"calls": str(self.calls)}))
        # The relay and the fakes run under this test's interpreter, resolved by the broker on the caller's PATH.
        self.python = Path(sys.executable).resolve()
        (self.bindir / "python3").symlink_to(self.python)
        self.seats_path = Path(self.seats)
        self.home_real = self.home.resolve()
        self.brokers = []
        self.addCleanup(self.stop_all)
        # The seats' API key file (U516): `<seats-root>/.state/anthropic/api-key`, hcom-seat's `key_file` row (U512),
        # made here as the operator's handout places it (0700 directory, 0600 file), and named in the broker's
        # environment as hcom-seat's router row names it for the broker it starts (the listener inherits it).
        self.key_file = self.seats_path / ".state/anthropic/api-key"
        self.key_file.parent.mkdir(mode=0o700, parents=True)
        self.seats_path.chmod(0o700)
        (self.seats_path / ".state").chmod(0o700)
        self.key_file.touch(mode=0o600)
        self.key_file.write_text(FIXTURE_KEY)
        self.env["REGIME_ANTHROPIC_KEY_FILE"] = str(self.key_file)

    # --- the scratch Router, its repository and the broker ---

    def make_router(self, name="router-20261107-000000-1"):
        """A Router slot in the shape `hcom-seat router` leaves: the state slot with its scratch cwd, the shared Claude
        Code directory, the broker directory `<state>/broker` made 0700 and empty before the settings (U343i: hcom-seat
        makes it; the broker takes it as made), the Router's credential root `<dsh-home>/router-credentials` made 0700
        (U353's cred_root_make; the broker holds it from `DSH_HOME`, which broker_env passes, U343l), and the settings
        file in the dsh row's shape with the router cells (the loopback grant, the state root, the broker directory in
        allowUnixSockets and, U343i, in denyWrite; the credential root in allowRead row 7 and in denyWrite, U353)."""
        seats = self.seats_path
        seats.mkdir(mode=0o700, exist_ok=True)
        state = seats / ".state" / name
        for path in (seats / ".state", state, state / "cwd", seats / ".state/claude", seats / ".sandbox",
                     seats / ".sandbox" / name, state / "broker"):  # fmt: skip
            path.mkdir(mode=0o700, exist_ok=True)
        (state / "broker").chmod(0o700)
        home, repo, store = self.home_real, self.repo.resolve(), self.store.resolve()
        cwd = state / "cwd"
        dsh_home = self.dsh_home_of_the_fixture()
        (dsh_home / "router-credentials").mkdir(mode=0o700, parents=True, exist_ok=True)
        deny_read = [f"{home}/.ssh", f"{home}/.gnupg", f"{home}/.aws", f"{home}/.netrc", f"{home}/.docker",
                     f"{home}/.kube", f"{home}/.config/gcloud", f"{home}/.codex", f"{home}/.omp/agent",
                     f"{home}/.omp/profiles", f"{home}/.hcom", f"{home}/.local/state/hcom",
                     f"{home}/.local/share/chezmoi", f"{home}/.local/share/chezmoi-private",
                     f"{home}/.config/chezmoi", f"{home}/.config/chezmoi-private", f"{home}/Workspace",
                     f"{seats}/.sandbox", f"{home}/.local/state/omp-seats", str(seats), f"{home}/.claude",
                     f"{home}/.claude.json", str(repo), f"{repo}/.git", str(store), f"{repo}/.orchestration"]  # fmt: skip
        # The Router's denyWrite carries the seats' API key file after the shared directory's rows, as hcom-seat
        # renders it since U512 (the worker copies the table and grants the same file for read, U516).
        deny_write = [f"{seats}/.sandbox", *(f"{cwd}/{p}" for p in PROJECT_FILES),
                      *(f"{seats}/.state/claude/{p}" for p in CLAUDE_ROWS), f"{seats}/.state/anthropic/api-key",
                      *(f"{repo}/{p}" for p in PROJECT_FILES),
                      f"{repo}/.git/config", f"{repo}/.git/config.worktree", f"{repo}/.git/info", f"{repo}/.git/hooks",
                      f"{repo}/.git/worktrees/*/config.worktree", f"{repo}/.git/worktrees/*/info",
                      f"{repo}/.git/worktrees/*/commondir", f"{repo}/.git/worktrees/*/gitdir",
                      f"{store}/config.toml", f"{home}/.claude", f"{home}/.claude.json", f"{repo}/.git", str(store),
                      f"{dsh_home}/router-credentials", f"{repo}/.orchestration", f"{state}/broker"]  # fmt: skip
        settings = {
            "network": {"allowedDomains": DOMAINS, "deniedDomains": [], "allowUnixSockets": [f"{state}/broker"],
                        "allowMachLookup": ["com.apple.trustd.agent"], "allowLocalBinding": True},
            "filesystem": {
                "denyRead": deny_read,
                "allowRead": [str(cwd), str(state), f"{seats}/.state/claude", str(dsh_home), f"{home}/.omp/profiles/dsh",
                              f"{home}/.agents/skills", f"{home}/.local/state/hcom-seat/tools", f"{dsh_home}/router-credentials"],
                "allowWrite": [str(cwd), str(state), f"{seats}/.state/claude", str(dsh_home), f"{home}/.omp/profiles/dsh",
                               f"{home}/.omp/run", f"{dsh_home}/router-state", "/tmp/claude", "/private/tmp/claude",
                               f"{home}/.npm/_logs"],
                "denyWrite": deny_write,
            },
            "allowPty": True,
        }  # fmt: skip
        (seats / ".sandbox" / name / "srt-settings.json").write_text(json.dumps(settings, separators=(",", ":")) + "\n")
        return name, cwd

    def scratch_git(self, *args, cwd):
        return subprocess.run(
            ["git", *args], cwd=cwd, env=self.env, capture_output=True, text=True, check=True
        ).stdout.strip()

    def make_repo(self, path):
        """A repository with one commit holding `a.txt`, as the Router would clone one into its scratch cwd; returns
        the path and the commit."""
        path.parent.mkdir(parents=True, exist_ok=True)
        git_init(path, env=self.env)
        (path / "a.txt").write_text("hello\n")
        self.scratch_git("add", "a.txt", cwd=path)
        self.scratch_git("commit", "-q", "-m", "one", cwd=path)
        return path, self.scratch_git("rev-parse", "HEAD", cwd=path)

    def commit_in(self, task, name="b.txt"):
        """One commit by the worker in its tree; returns the new head."""
        (task / name).write_text("world\n")
        self.scratch_git("add", name, cwd=task)
        self.scratch_git("commit", "-q", "-m", "two", cwd=task)
        return self.scratch_git("rev-parse", "HEAD", cwd=task)

    def dsh_home_of_the_fixture(self):
        """The Router's home the scratch Router (make_router) grants and the broker holds its credential root under."""
        return self.home_real / "dsh-home"

    def broker_env(self, **overrides):
        """The broker's environment: the fixture's, `DSH_HOME` the scratch Router's home (hcom-seat sets it in the
        Router's sandbox environment, where the broker runs; U343l) unless a test overrides it (`None` removes a key)."""
        env = {**self.env, "DSH_HOME": str(self.dsh_home_of_the_fixture()),
               **{k: v for k, v in overrides.items() if v is not None}}  # fmt: skip
        for key in (k for k, v in overrides.items() if v is None):
            env.pop(key, None)
        return env

    def launch_broker(self, name, cwd, wrapper=(), broker=BROKER, **overrides):
        """Start the broker for the Router `name` (through the argv prefix `wrapper` when given; the lever at `broker`,
        the checkout's unless a test runs a scratch copy) and return (process, socket path) at once, before it
        listens; the caller waits for the state it needs (start_broker: the readiness line)."""
        proc = subprocess.Popen(
            [*wrapper, str(broker), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(**overrides),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )  # fmt: skip
        proc.first_line = ""
        self.brokers.append(proc)
        self.router = name
        return proc, self.seats_path / ".state" / name / "broker/sock"

    def start_broker(self, name, cwd, wrapper=(), broker=BROKER, **overrides):
        """launch_broker, then return once the broker's stdout carries the readiness line `acp-broker: listening on
        <sock>` (U447: the lever's documented readiness, which hcom-seat reads through its FIFO; until this round the
        fixture took the socket's existence, which precedes the relay's signal handlers, so a test's signal could land
        in that window). The line is gathered under one deadline (first_line_within; U447b, verdict U447-a52a1452 P2:
        `select` then `readline` let a fragment without a newline satisfy the select and block the readline past the
        deadline), kept on the process, and stop_broker returns it at the head of `out`."""
        proc, sock = self.launch_broker(name, cwd, wrapper=wrapper, broker=broker, **overrides)
        text = self.first_line_within(proc, 60)
        line, newline, _rest = text.partition("\n")
        if line + newline != f"acp-broker: listening on {sock}\n":
            out, err = proc.communicate(timeout=60)
            self.fail(f"the broker ended before it listened: {proc.returncode} {text + out!r} {err!r}")
        proc.first_line = text
        return proc, sock

    def first_line_within(self, proc, seconds):
        """The bytes of `proc`'s stdout through its first newline (and whatever came with them), decoded: gathered
        chunk by chunk from the descriptor, each wait bounded by what remains of `seconds`, so a fragment without a
        newline fails at the deadline naming it and never blocks past it; at EOF, whatever arrived. The text wrapper
        has read nothing yet, so its later reads (communicate) continue after these bytes."""
        fd = proc.stdout.fileno()
        deadline = time.monotonic() + seconds
        buffer = b""
        while b"\n" not in buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([fd], [], [], remaining)[0]:
                self.fail(f"the broker did not print its readiness line within {seconds} s (stdout so far: {buffer!r})")
            chunk = os.read(fd, 4096)
            if not chunk:
                break
            buffer += chunk
        return buffer.decode(proc.stdout.encoding, errors="replace")

    def stop_broker(self, proc, sig=signal.SIGTERM):
        if proc.poll() is None:
            proc.send_signal(sig)
        try:
            out, err = proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
        return proc.returncode, getattr(proc, "first_line", "") + out, err

    def stop_all(self):
        for proc in self.brokers:
            self.stop_broker(proc)

    def connect(self, sock, repo=None, name=None, header=None, ref="HEAD"):
        """A raw connection with the header sent; the socket file may exist a moment before the listener accepts."""
        conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        conn.settimeout(120)
        deadline = time.monotonic() + 60
        while True:
            try:
                # By name from the socket's directory, as the client does: the scratch path exceeds the 104-byte cap.
                here = os.getcwd()
                os.chdir(sock.parent)
                try:
                    conn.connect(sock.name)
                finally:
                    os.chdir(here)
                break
            except (ConnectionRefusedError, FileNotFoundError):
                if time.monotonic() > deadline:
                    self.fail(f"cannot connect to {sock}")
                time.sleep(0.02)
        if header is None:
            header = f"ACP-SEAT v1 repo={repo} ref={ref} name={name}\n"
        conn.sendall(header.encode())
        return conn

    def recv_all(self, conn):
        data = bytearray()
        while True:
            chunk = conn.recv(1 << 20)
            if not chunk:
                break
            data += chunk
        conn.close()
        return bytes(data)

    def recv_line(self, conn):
        data = bytearray()
        while not data.endswith(b"\n"):
            chunk = conn.recv(1 << 20)
            if not chunk:
                break
            data += chunk
        return bytes(data)

    def exchange(self, sock, repo, name, payload, ref="HEAD"):
        """One connection: the header, `payload`, EOF; what came back."""
        conn = self.connect(sock, repo, name, ref=ref)
        conn.sendall(payload)
        conn.shutdown(socket.SHUT_WR)
        return self.recv_all(conn)

    def client(self, sock, repo, name, payload, ref="HEAD", **overrides):
        return subprocess.run(
            [str(CLIENT), "--socket", str(sock), "--repo", str(repo), "--ref", ref, "--name", name], input=payload,
            env=self.broker_env(**{"HCOM_SEAT_SANDBOX": "/scratch/sandbox", **overrides}), capture_output=True, check=False,
        )  # fmt: skip

    def client_popen(self, sock, repo, name, ref="HEAD"):
        """The client with its stdin held open, for a session the test drives line by line while the worker runs."""
        return subprocess.Popen(
            [str(CLIENT), "--socket", str(sock), "--repo", str(repo), "--ref", ref, "--name", name],
            env=self.broker_env(HCOM_SEAT_SANDBOX="/scratch/sandbox"), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )  # fmt: skip

    # --- the record (U343g): `<state>/broker/<slot>`, the reaper's exit report, read after the socket closes ---

    def record_path(self, slot):
        return self.seats_path / ".state" / self.router / "broker" / slot

    def record_lines(self, slot):
        """The record's lines, or None when no record exists."""
        path = self.record_path(slot)
        return path.read_text().splitlines() if path.exists() else None

    def record_line(self, conn):
        """The connection's first line, `acp-broker: record <slot>`, read byte by byte so no worker byte is taken with
        it; the slot name."""
        data = bytearray()
        conn.settimeout(30)
        try:
            while not data.endswith(b"\n"):
                chunk = conn.recv(1)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            self.fail(f"no record line within 30 s (received {bytes(data)!r})")
        finally:
            conn.settimeout(120)
        match = RECORD_LINE.match(bytes(data))
        self.assertIsNotNone(match, f"the first line is not the record line: {bytes(data)!r}")
        return match.group(1).decode()

    def finish(self, conn, slot):
        """Half-close the connection, read the stream to its end and then the record, complete once the socket has
        closed: (the bytes after the record line, the record's last line `status=<n> push=<word>`). The record's
        running lines are checked here: `ref=refs/acp-seat/<name>/<stamp>-<pid>` from the slot's parts, `reaper=<pid>`."""
        try:
            conn.shutdown(socket.SHUT_WR)
        except OSError:
            pass
        rest = self.recv_all(conn)
        lines = self.record_lines(slot)
        self.assertIsNotNone(lines, f"no record {self.record_path(slot)} after the socket closed")
        self.assertEqual(len(lines), 3, lines)
        name, suffix = SLOT_PARTS.match(slot).groups()
        self.assertEqual(lines[0], f"ref=refs/acp-seat/{name}/{suffix}")
        self.assertRegex(lines[1], r"^reaper=\d+$")
        self.assertRegex(lines[2], r"^status=\d+ push=\S+$")
        return rest, lines[2]

    def exchange_record(self, sock, repo, name, payload, ref="HEAD"):
        """One connection: the header, `payload`, EOF; (the bytes after the record line, the record's last line)."""
        conn = self.connect(sock, repo, name, ref=ref)
        conn.sendall(payload)
        slot = self.record_line(conn)
        return self.finish(conn, slot)

    @staticmethod
    def alive(pid):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        return True

    def kill_fake_omp(self):
        """End a fake omp that ignores TERM (the cleanup of test (a), so a red run leaves no process behind)."""
        pid_file = self.calls / "omp-pid"
        if pid_file.exists():
            try:
                os.kill(int(pid_file.read_text()), signal.SIGKILL)
            except (ProcessLookupError, ValueError):
                pass

    def remove_slots(self):
        """Remove every per-connection slot left behind (the cleanup of a red run of test (b))."""
        for slot in self.acp_slots():
            path = self.seats_path / ".state" / slot
            subprocess.run(["chmod", "-R", "u+rwX", str(path)], check=False)
            subprocess.run(["rm", "-rf", str(path)], check=False)

    def acp_slots(self):
        """The per-connection slots, `acp-<name>-<stamp>-<pid>` under `.state` (U343e: a broker-owned root no seat
        may write; a write root under `.sandbox` would be denied by the Router's `.sandbox` deny row, which srt's
        macOS profile emits after the allow)."""
        state = self.seats_path / ".state"
        return sorted(p.name for p in state.iterdir() if p.name.startswith("acp-")) if state.exists() else []

    def slot_task(self, slot):
        return self.seats_path / ".state" / slot / "task"

    def state_names(self):
        state = self.seats_path / ".state"
        return sorted(p.name for p in state.iterdir() if not p.name.startswith("acp-")) if state.exists() else []

    def canaries(self):
        return [c for c in self.calls_of("srt") if c["argv"][3:5] == ["/bin/sh", "-c"]]

    def wait_for(self, predicate, what, seconds=60):
        deadline = time.monotonic() + seconds
        while not predicate():
            if time.monotonic() > deadline:
                self.fail(f"{what} did not happen within {seconds} s")
            time.sleep(0.02)

    def log_lines(self, name):
        """The launch log's lines: `<seats-root>/.state/broker-logs/<name>.log` (U343o; until round 12 it was
        `.state/<name>/acp-launch.log`, inside the seat slot of that name)."""
        path = self.seats_path / ".state/broker-logs" / f"{name}.log"
        return path.read_text().splitlines() if path.exists() else []

    def held_connection(self, sock, repo, name, ref="HEAD"):
        """A connection whose record line has arrived and with one line echoed back, so the worker is running and
        its slot exists; returns the connection, the slot name (the record line's) and the worker's tree."""
        conn = self.connect(sock, repo, name, ref=ref)
        slot = self.record_line(conn)
        conn.sendall(PING)
        self.assertEqual(self.recv_line(conn), PING)
        self.assertIn(slot, self.acp_slots())
        return conn, slot, self.slot_task(slot)

    # --- the tests ---

    def test_a_broker_inside_a_seat_is_refused_before_anything_is_made(self):
        """The three markers (hcom's two and the shim's) each refuse before anything is made in the broker directory
        (hcom-seat's, pre-made empty by the fixture as the router launch makes it, U343i); a seat, the Router included,
        never starts a broker."""
        name, cwd = self.make_router()
        for marker in ("HCOM_LAUNCHED", "HCOM_PROCESS_ID", "HCOM_SEAT_SANDBOX"):
            with self.subTest(marker=marker):
                run = subprocess.run(
                    [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(**{marker: "1"}),
                    capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"acp-broker: refused: refused inside a seat ({marker} is set)", run.stderr)
                self.assertEqual(
                    sorted(p.name for p in (self.seats_path / ".state" / name / "broker").iterdir()),
                    [],
                    "the refused broker made nothing in the directory",
                )
        self.assertEqual(self.calls_of("srt"), [])

    def test_a_bad_header_is_refused_with_one_line_and_nothing_made(self):
        """An unclean repository path, a bad ref, a bad name, the name `claude`, the Router's own seat name, a name
        with the slot prefix, a missing field, a sixth field, a wrong version, a header padded to the read limit
        (verdict U343d-136fbe0a P2 `:953`: the newline was never established as consumed): one `acp-broker: refused:`
        line, the connection closed, no slot, no state slot, no srt call."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        padded = f"ACP-SEAT v1 repo={repo} ref=HEAD name=w1"
        padded += " " * (1024 - len(padded))
        cases = (
            ("an unclean repository path", f"ACP-SEAT v1 repo={repo}/../repo ref=HEAD name=w1\n", "is not a clean absolute path"),
            ("a relative repository path", "ACP-SEAT v1 repo=repo ref=HEAD name=w1\n", "is not a clean absolute path"),
            ("a bad ref", f"ACP-SEAT v1 repo={repo} ref=-x name=w1\n", "the header ref '-x' is outside"),
            ("a ref with a range", f"ACP-SEAT v1 repo={repo} ref=a..b name=w1\n", "the header ref 'a..b' is outside"),
            ("a bad name", f"ACP-SEAT v1 repo={repo} ref=HEAD name=W1\n", "is outside ^[a-z0-9][a-z0-9_-]{0,63}$"),
            ("the name claude", f"ACP-SEAT v1 repo={repo} ref=HEAD name=claude\n", "'claude' is taken by the shared Claude Code directory"),
            ("the Router's seat name", f"ACP-SEAT v1 repo={repo} ref=HEAD name={name}\n", "is the Router's own seat name"),
            ("the slot prefix", f"ACP-SEAT v1 repo={repo} ref=HEAD name=acp-w1\n", "begins with 'acp-', the prefix of the broker's slots"),
            ("a missing field", f"ACP-SEAT v1 repo={repo} ref=HEAD\n", "has no 'name=<name>' fifth field"),
            ("a cwd field", f"ACP-SEAT v1 cwd={cwd} name=w1\n", "has no 'repo=<path>' third field"),
            ("a sixth field", f"ACP-SEAT v1 repo={repo} ref=HEAD name=w1 x\n", "has more than five fields"),
            ("a wrong version", f"ACP-SEAT v2 repo={repo} ref=HEAD name=w1\n", "does not begin 'ACP-SEAT v1'"),
            ("an empty line", "\n", "does not begin 'ACP-SEAT v1'"),
            ("a header padded to the read limit, then a sixth field", padded + " x\n", "exceeds 1024 characters"),
        )  # fmt: skip
        for label, header, message in cases:
            with self.subTest(case=label):
                data = self.recv_all(self.connect(sock, header=header)).decode()
                self.assertTrue(data.startswith("acp-broker: refused: "), data)
                self.assertIn(message, data)
                self.assertEqual(data.count("\n"), 1, data)
        self.assertEqual(self.acp_slots(), [])
        self.assertEqual(self.state_names(), ["anthropic", "claude", name])
        self.assertEqual(self.calls_of("srt"), [])
        self.assertEqual(self.calls_of("omp"), [])
        # A good header after the bad ones still works: the broker refused connections, not itself; a name of 64
        # characters, the grammar's longest, launches (verdict P2 `:980`: the limit was applied to the slot name).
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        self.assertEqual(self.exchange_record(sock, repo, "a" * 64, PING), (PING, "status=0 push=none"))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_a_repository_that_does_not_read_or_a_ref_that_does_not_resolve_refuses_with_the_slot_removed(self):
        """A path that holds no repository, a ref the repository has not, a path that is a file: the clone's read
        inside the Router's settings fails and the connection refuses by name (the repository and the ref), the slot
        removed, no canary, no omp, no state slot for the worker."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        (cwd / "empty").mkdir()
        (cwd / "file").write_text("x\n")
        proc, sock = self.start_broker(name, cwd)
        cases = (
            ("no repository", cwd / "empty", "HEAD"),
            ("an absent path", cwd / "nowhere", "HEAD"),
            ("a file", cwd / "file", "HEAD"),
            ("an unknown ref", repo, "refs/heads/nowhere"),
            ("a commit the repository has not", repo, "0123456789012345678901234567890123456789"),
        )
        for label, path, ref in cases:
            with self.subTest(case=label):
                data = self.recv_all(self.connect(sock, path, "w1", ref=ref)).decode()
                self.assertEqual(data.count("\n"), 1, data)
                self.assertIn(f"acp-broker: refused: cannot resolve the ref '{ref}' in the repository {path}", data)
                self.assertIn("read inside the Router's settings", data)
                self.assertEqual(self.acp_slots(), [])
        self.assertEqual(self.canaries(), [], "no canary: the clone refused first")
        self.assertEqual(self.calls_of("omp"), [])
        self.assertEqual(
            self.state_names(), ["anthropic", "claude", name], "no state slot and no log for a refused launch"
        )
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_a_router_moving_or_relinking_its_repository_after_the_header_changes_nothing_the_worker_may_read_or_write(
        self,
    ):
        """U343e test (a) (verdicts U343b-cae04852 P1 `:858` and U343d-136fbe0a P1 `:1149`, class broker-boundary): the
        Router writes every ancestor of a path under its scratch cwd, so a path it names can be moved or relinked
        between the broker's checks and srt's start, and srt resolves the settings' path strings at start; a grant
        written for a Router-named path landed on `~/.aws`. The worker's directory is now the broker's own slot,
        cloned from the repository and ref the header names, and no Router-named path appears in the settings.
        The fixture's Router swaps the repository's parent for a link to `~/.aws` (or renames it away) (1) at the
        canary, after the clone: the launch goes through, the worker's tree is the clone (the repository's file and
        commit), its settings name the slot's task and the role's roots alone, nothing under the scratch cwd, the
        repository or `~/.aws`, and omp runs in the slot's task; (2) at the first srt call, before the clone: the
        clone fails by name (the repository and the ref), no slot remains, no omp runs, and nothing under `~/.aws`
        was made or read as a tree."""
        name, cwd = self.make_router()
        work = cwd / "work"
        repo, base = self.make_repo(work / "repo")
        home = self.home_real
        (home / ".aws/repo").mkdir(parents=True)
        proc, sock = self.start_broker(name, cwd)
        swap = self.calls / "swap-ancestor"
        moved = cwd / "work-moved"
        roles = {str(self.seats_path / ".state/claude"), f"{home}/.omp/profiles/dsh", f"{home}/.omp/run",
                 f"{home}/.agents/skills", f"{home}/.local/state/hcom-seat/tools", f"{home}/.npm/_logs",
                 "/tmp/claude", "/private/tmp/claude", str(self.key_file)}  # fmt: skip
        for label, link in (
            ("the parent replaced by a link to ~/.aws", str(home / ".aws")),
            ("the parent renamed away", None),
        ):
            with self.subTest(case=f"after the clone, {label}"):
                swap.write_text(json.dumps({"ancestor": str(work), "moved": str(moved), "link": link, "at": "canary"}))
                conn, slot, task = self.held_connection(sock, repo, "w1")
                self.assertFalse(swap.exists(), "the fake performed the swap at the canary")
                settings = json.loads((self.seats_path / ".state" / slot / "settings.json").read_text())
                grants = json.dumps(settings["filesystem"]["allowRead"] + settings["filesystem"]["allowWrite"])
                for forbidden in (str(cwd), str(repo), str(home / ".aws"), str(moved)):
                    self.assertNotIn(forbidden, grants, f"{forbidden} among the worker's grants")
                self.assertNotIn(str(cwd), json.dumps(settings), "a row under the Router's scratch cwd survived")
                for kind in ("allowRead", "allowWrite"):
                    for row in settings["filesystem"][kind]:
                        self.assertTrue(
                            row == str(task) or row in roles,
                            f"{kind} row {row} is neither the slot's task nor the role's",
                        )
                self.assertEqual(settings["filesystem"]["allowWrite"][0], str(task))
                self.assertEqual(settings["filesystem"]["allowRead"][0], str(task))
                self.assertEqual((task / "a.txt").read_text(), "hello\n")
                self.assertEqual(self.scratch_git("rev-parse", "HEAD", cwd=task), base)
                self.assertEqual(self.calls_of("omp")[-1]["cwd"], str(task))
                self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
                self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
                if link:
                    self.assertTrue(work.is_symlink())
                    work.unlink()
                moved.rename(work)
        omp_runs = len(self.calls_of("omp"))
        for label, link in (
            ("the parent replaced by a link to ~/.aws", str(home / ".aws")),
            ("the parent renamed away", None),
        ):
            with self.subTest(case=f"before the clone, {label}"):
                swap.write_text(json.dumps({"ancestor": str(work), "moved": str(moved), "link": link, "at": "first"}))
                data = self.recv_all(self.connect(sock, repo, "w1")).decode()
                self.assertFalse(swap.exists(), "the fake performed the swap at the first srt call")
                self.assertEqual(data.count("\n"), 1, data)
                self.assertIn(f"acp-broker: refused: cannot resolve the ref 'HEAD' in the repository {repo}", data)
                self.assertEqual(self.acp_slots(), [])
                self.assertEqual(len(self.calls_of("omp")), omp_runs, "no omp run")
                if link:
                    work.unlink()
                moved.rename(work)
        self.assertEqual(sorted(p.name for p in (home / ".aws/repo").iterdir()), [])
        with self.subTest(case="through the client, after the clone"):
            swap.write_text(
                json.dumps({"ancestor": str(work), "moved": str(moved), "link": str(home / ".aws"), "at": "canary"})
            )
            run = self.client(sock, repo, "w1", PING)
            self.assertEqual((run.returncode, run.stdout, run.stderr), (0, PING, b"acp-seat: push=none\n"))
            work.unlink()
            moved.rename(work)
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_b_the_settings_rendered_for_a_connection_carry_the_slot_task_and_the_roles_roots_and_no_router_path(self):
        """U343e test (b) (the U343c shape rewritten): the settings read from the slot while omp runs. `allowWrite`
        is the slot's task, then the role's own rows (the shared Claude Code directory, `~/.omp/profiles/dsh`,
        `~/.omp/run`, srt's own paths); `allowRead` the task, the shared directory, the profile, the skills and the
        tool directory; no grant row lies under the Router's scratch cwd or its state slot, no deny row under the
        scratch cwd (the Router's project-file denies are re-rooted under the task), and the one deny row under the
        state slot is the Router's broker deny `<state>/broker` (U343i), carried as every Router deny is. The slot is
        0700 under `.state`, its settings 0600, the task a detached checkout of the ref; the slot is gone when the
        connection ends."""
        name, cwd = self.make_router()
        repo, base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        home = self.home_real
        slot_path = self.seats_path / ".state" / slot
        self.assertRegex(slot, r"^acp-w1-\d{8}-\d{6}-\d+$")
        self.assertEqual(stat.S_IMODE(os.lstat(slot_path).st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(os.lstat(slot_path / "settings.json").st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(os.lstat(task).st_mode), 0o700)
        settings = json.loads((slot_path / "settings.json").read_text())
        fs = settings["filesystem"]
        self.assertEqual(fs["allowWrite"][:4], [str(task), str(self.seats_path / ".state/claude"), f"{home}/.omp/profiles/dsh", f"{home}/.omp/run"])  # fmt: skip
        self.assertTrue(
            set(fs["allowWrite"][4:]) <= {"/tmp/claude", "/private/tmp/claude", f"{home}/.npm/_logs"}, fs["allowWrite"]
        )
        self.assertEqual(fs["allowRead"], [str(task), str(self.seats_path / ".state/claude"), f"{home}/.omp/profiles/dsh", f"{home}/.agents/skills", f"{home}/.local/state/hcom-seat/tools", str(self.key_file)])  # fmt: skip
        state = self.seats_path / ".state" / name
        for kind in ("allowRead", "allowWrite", "denyRead", "denyWrite"):
            for row in fs[kind]:
                self.assertFalse(
                    row == str(cwd) or row.startswith(f"{cwd}/"),
                    f"{kind} row {row} lies under the Router's scratch cwd",
                )
                if kind != "denyWrite":
                    self.assertFalse(
                        row == str(state) or row.startswith(f"{state}/"),
                        f"{kind} row {row} lies under the Router's state slot",
                    )
        self.assertEqual(
            [r for r in fs["denyWrite"] if r == str(state) or r.startswith(f"{state}/")],
            [f"{state}/broker"],
            "the one deny row under the Router's state slot is the broker deny",
        )
        self.assertEqual(
            [r for r in fs["denyWrite"] if r.startswith(f"{task}/")], [f"{task}/{p}" for p in PROJECT_FILES]
        )
        self.assertEqual(settings["network"]["allowUnixSockets"], [])
        self.assertEqual(self.scratch_git("rev-parse", "HEAD", cwd=task), base)
        self.assertEqual(self.scratch_git("status", "--porcelain", cwd=task), "")
        self.assertEqual(self.scratch_git("rev-parse", "--abbrev-ref", "HEAD", cwd=task), "HEAD", "detached")
        self.assertEqual(
            sorted(p.name for p in slot_path.iterdir()),
            ["control", "ready", "settings.json", "stderr", "task"],
            "no pack left behind (the two pipes, U343o; the launch's stderr file, U449b)",
        )
        self.assertEqual(stat.S_IMODE(os.lstat(slot_path / "stderr").st_mode), 0o600)
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_c_the_end_of_session_push_lands_the_worker_head_at_refs_acp_seat_and_the_record_names_it(self):
        """U343e test (c), the record form (U343g): a commit the worker made lands in the repository at
        `refs/acp-seat/<name>/<stamp>` when omp exits, written inside the Router's settings, and the record's last
        line (and the log's exit line) names the ref, which the record's first line named before the push began; a
        worker whose HEAD is the ref pushes nothing (`push=none`); a repository made read-only after the clone gives
        `push=failed`, the reason on the broker's stderr; the record's last line follows the slot's removal."""
        name, cwd = self.make_router()
        repo, base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        head = self.commit_in(task)
        rest, last = self.finish(conn, slot)
        self.assertEqual(rest, b"", "nothing of the broker's on the stream after the record line")
        match = re.fullmatch(r"status=0 push=(refs/acp-seat/w1/\d{8}-\d{6}-\d+)", last)
        self.assertIsNotNone(match, last)
        ref = match.group(1)
        self.assertEqual(self.record_lines(slot)[0], f"ref={ref}", "the record named the ref before the push")
        self.assertEqual(ref.rsplit("/", 1)[1], slot[len("acp-w1-") :], "the stamp of the slot")
        self.assertEqual(self.scratch_git("rev-parse", "--verify", ref, cwd=repo), head)
        self.assertEqual(self.scratch_git("show", f"{ref}:b.txt", cwd=repo), "world")
        self.assertEqual(self.scratch_git("rev-parse", "HEAD", cwd=repo), base, "the repository's own HEAD untouched")
        self.assertEqual(self.log_lines("w1")[2].split(" acp-broker: ")[1], f"omp acp exit 0 push={ref}")
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        with self.subTest(case="HEAD equal to the ref"):
            self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
            self.assertEqual(self.scratch_git("for-each-ref", "--format=%(refname)", "refs/acp-seat/", cwd=repo), ref)
        with self.subTest(case="the ref the worker started from"):
            conn, slot, task = self.held_connection(sock, repo, "w1", ref=ref)
            self.assertEqual(self.scratch_git("rev-parse", "HEAD", cwd=task), head)
            head2 = self.commit_in(task, "c.txt")
            _rest, last = self.finish(conn, slot)
            match = re.fullmatch(r"status=0 push=(refs/acp-seat/w1/\S+)", last)
            self.assertIsNotNone(match, last)
            self.assertEqual(self.scratch_git("rev-parse", "--verify", match.group(1), cwd=repo), head2)
        with self.subTest(case="a repository made read-only after the clone"):
            conn, slot, task = self.held_connection(sock, repo, "w1")
            self.commit_in(task, "d.txt")
            subprocess.run(["chmod", "-R", "a-w", str(repo / ".git")], check=True)
            try:
                self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=failed"))
            finally:
                subprocess.run(["chmod", "-R", "u+w", str(repo / ".git")], check=True)
            self.assertEqual(self.log_lines("w1")[-1].split(" acp-broker: ")[1], "omp acp exit 0 push=failed")
            self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        with self.subTest(case="through the client"):
            run = self.client(sock, repo, "w1", PING)
            self.assertEqual((run.returncode, run.stdout, run.stderr), (0, PING, b"acp-seat: push=none\n"))
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertIn("acp-broker: the push of ", err)
        self.assertIn("failed", err)

    # --- U343g, round 5: the exit report is the reaper's record, the teardown is the reaper ---

    def test_a_a_term_ignoring_worker_is_ended_by_the_reaper_and_holds_neither_the_slot_nor_the_record(self):
        """U343g test (a) (verdict U343f-22a81500 P1 `:1233`): the handler's trap waited on omp before the KILL, so a
        worker that ignored TERM held the trap, the slot and the connection open. The teardown is the reaper, not a
        trap, and the reaper polls the group with `kill -0` for the grace, then KILLs: with a TERM-ignoring fake omp,
        a TERM to the handler pid leaves the slot gone and the record complete, `status=2 push=skipped`, within the
        fixed ceiling, the worker dead and one exit line in the log; then the same worker under `stop_broker`: the
        broker ends by its signal within the fixed ceiling with the slot gone. The ceiling is fixed (U440) because the
        grace is counted in forked `/bin/sleep 0.1` iterations (acp-broker `:1727`) and stretched past every budget
        derived from the setup's wall time on the macos-15 runner (7 s twice, then 9.07 s, where the module ran 920 s
        against about 150 s on the development host). The grace's design value is the lever's claim, filed as U441."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        (self.calls / "omp-ignore-term").touch()
        self.addCleanup(self.kill_fake_omp)
        conn, slot, _task = self.held_connection(sock, repo, "w1")
        pid = int(slot.rsplit("-", 1)[1])
        omp_pid = int((self.calls / "omp-pid").read_text())
        started = time.monotonic()
        os.kill(pid, signal.SIGTERM)
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal", seconds=REAPER_CEILING)
        rest = self.recv_all(conn)
        elapsed = time.monotonic() - started
        self.assertLessEqual(elapsed, REAPER_CEILING, f"the slot went in {elapsed:.1f} s, ceiling {REAPER_CEILING} s")
        self.assertEqual(rest, b"", "nothing of the broker's on the stream after the record line")
        self.assertEqual(self.record_lines(slot)[2], "status=2 push=skipped")
        self.assertEqual(len(self.record_lines(slot)), 3)
        self.wait_for(lambda: not self.alive(omp_pid), "the TERM-ignoring worker's end by KILL", seconds=5)
        exits = [line for line in self.log_lines("w1") if " acp-broker: omp acp exit " in line]
        self.assertEqual(len(exits), 1, self.log_lines("w1"))
        self.assertRegex(exits[0], r" acp-broker: omp acp exit 2 push=skipped$")
        (self.calls / "omp-pid").unlink()
        conn, slot, _task = self.held_connection(sock, repo, "w1")
        omp_pid = int((self.calls / "omp-pid").read_text())
        started = time.monotonic()
        status, _out, err = self.stop_broker(proc)
        elapsed = time.monotonic() - started
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertEqual(self.acp_slots(), [], "the slot went with the broker")
        self.assertLessEqual(elapsed, REAPER_CEILING, f"the broker went in {elapsed:.1f} s, ceiling {REAPER_CEILING} s")
        self.assertFalse(self.alive(omp_pid))
        self.assertEqual(
            self.broker_dir_entries(sock), [], "the records went at the broker's end; the directory stands"
        )
        conn.close()

    def test_b_a_termination_during_the_slot_removal_cannot_strand_the_slot(self):
        """U343g test (b) (verdict U343f-22a81500 P1 `:1339`): `trap - HUP INT TERM` ran before `slot_remove`, so a
        TERM during the recursive removal of a large task killed the handler and stranded the slot. The removal runs
        in the reaper, which no signal to the handler reaches (`trap ''` on HUP INT TERM, and the relay signals the
        handler pid alone): with 16,000 files in `task`, TERM to the handler pid in a loop for as long as the slot
        exists leaves no slot, a complete record (`push=skipped`, or `push=none` when the handler had finished) and
        exactly one exit line in the log."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        self.addCleanup(self.remove_slots)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        pid = int(slot.rsplit("-", 1)[1])
        big = task / "big"
        big.mkdir()
        for i in range(16000):
            os.close(os.open(big / f"f{i}", os.O_CREAT | os.O_WRONLY, 0o600))
        conn.shutdown(socket.SHUT_WR)
        deadline = time.monotonic() + 90
        while self.acp_slots() and time.monotonic() < deadline:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            time.sleep(0.01)
        self.assertEqual(self.acp_slots(), [], "the slot remains after the terminations")
        rest = self.recv_all(conn)
        self.assertEqual(rest, b"")
        lines = self.record_lines(slot)
        self.assertIsNotNone(lines, "no record")
        self.assertEqual(len(lines), 3, lines)
        self.assertRegex(lines[2], r"^status=\d+ push=(skipped|none)$")
        exits = [line for line in self.log_lines("w1") if " acp-broker: omp acp exit " in line]
        self.assertEqual(len(exits), 1, self.log_lines("w1"))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_c_a_worker_tail_without_a_newline_is_payload_and_the_client_learns_the_ref_from_the_record(self):
        """U343g test (c) (verdict U343f-22a81500 P1 `:1347`): the trailer was one more `printf` on the stream omp
        wrote, so a worker's unterminated last bytes joined it on one line, the client's anchor missed it, and the
        client exited 2 without the push word after `update-ref` had written the ref. No byte of the stream is read
        as a report: the fake omp prints an unterminated `omp acp exit 0 push=none` after the worker's commit; the
        client exits 0, its stdout ends with those bytes, its stderr names the pushed ref, the ref resolves in the
        repository to the worker's commit, the record is gone (the client unlinked it) and the slot is gone."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        client = self.client_popen(sock, repo, "w1")
        client.stdin.write(PING)
        client.stdin.flush()
        self.assertEqual(client.stdout.readline(), PING)
        (slot,) = self.acp_slots()
        head = self.commit_in(self.slot_task(slot))
        (self.calls / "omp-tail").write_bytes(b"omp acp exit 0 push=none")
        out, err = client.communicate(timeout=120)
        (self.calls / "omp-tail").unlink()
        self.assertEqual(out, b"omp acp exit 0 push=none", "the stdout after the echoed ping ends with the tail")
        match = re.fullmatch(rb"acp-seat: push=(refs/acp-seat/w1/\d{8}-\d{6}-\d+)\n", err)
        self.assertIsNotNone(match, err)
        self.assertEqual(client.returncode, 0, err)
        ref = match.group(1).decode()
        self.assertEqual(self.scratch_git("rev-parse", "--verify", ref, cwd=repo), head)
        self.assertEqual(self.log_lines("w1")[-1].split(" acp-broker: ")[1], f"omp acp exit 0 push={ref}")
        self.assertFalse(self.record_path(slot).exists(), "the client unlinked the record")
        self.assertEqual(self.acp_slots(), [])
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_d_a_trailer_shaped_worker_line_then_handler_loss_is_payload_and_the_record_says_skipped(self):
        """U343g test (d) (verdict U343f-22a81500 P2 `acp-seat:190`): any complete line in the trailer's shape was
        held as the trailer, so a worker line in that shape followed by the handler's loss was accepted as the
        broker's status and push word. The worker (the fake omp's echo) prints the complete line `omp acp exit 0
        push=none`, then the handler gets SIGKILL: the client exits 2 with that line on its stdout, its stderr says
        `push=skipped` (the record the reaper wrote), no ref exists in the repository, the slot and the record are
        gone. Against a scratch server in the broker's place, a record line and that line with no record behind
        them exit 2 naming the id, the line on stdout."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        client = self.client_popen(sock, repo, "w1")
        client.stdin.write(PING)
        client.stdin.flush()
        self.assertEqual(client.stdout.readline(), PING)
        (slot,) = self.acp_slots()
        pid = int(slot.rsplit("-", 1)[1])
        line = b"omp acp exit 0 push=none\n"
        client.stdin.write(line)
        client.stdin.flush()
        # The echoed line reaches the client's stdout only when the client writes worker bytes as they come (a client
        # that holds a trailer-shaped line reads nothing here within the wait, and the stdout is judged whole below).
        ready, _, _ = select.select([client.stdout], [], [], 10)
        echoed = client.stdout.readline() if ready else b""
        os.kill(pid, signal.SIGKILL)
        out, err = client.communicate(timeout=120)
        self.assertEqual((client.returncode, echoed + out, err), (2, line, b"acp-seat: push=skipped\n"))
        self.assertEqual(self.scratch_git("for-each-ref", "refs/acp-seat/", cwd=repo), "")
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        self.assertFalse(self.record_path(slot).exists(), "the client unlinked the record")
        exits = [entry for entry in self.log_lines("w1") if " acp-broker: omp acp exit " in entry]
        self.assertEqual(len(exits), 1, self.log_lines("w1"))
        self.assertRegex(exits[0], r" acp-broker: omp acp exit 2 push=skipped$")
        run = self.client_against_stream(b"acp-broker: record acp-w1-20260101-000000-1\n" + line)
        self.assertEqual((run.returncode, run.stdout), (2, line), run.stderr)
        self.assertIn(b"without a complete record acp-w1-20260101-000000-1", run.stderr)
        self.assertNotIn(b"acp-seat: push=", run.stderr)
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_e_the_first_line_is_the_record_line_before_any_worker_byte_and_a_refusal_is_unchanged(self):
        """U343g test (e): the stream carries exactly one broker line, the first, before omp starts: `acp-broker: record
        acp-<name>-<stamp>-<pid>` names the slot, and at that moment the record exists under `<state>/broker/` with its
        two running lines, `ref=refs/acp-seat/<name>/<stamp>-<pid>` and `reaper=<pid>` of a live process that is not
        the handler; every later byte is the worker's (the echoed ping, then nothing), and the record's last line
        follows the socket's close. A refusal's first line keeps its shape, one line and nothing made."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        conn = self.connect(sock, repo, "w1")
        slot = self.record_line(conn)
        self.assertEqual(self.acp_slots(), [slot])
        lines = self.record_lines(slot)
        self.assertEqual(len(lines), 2, lines)
        self.assertEqual(lines[0], f"ref=refs/acp-seat/w1/{slot[len('acp-w1-') :]}")
        self.assertRegex(lines[1], r"^reaper=\d+$")
        reaper = int(lines[1][len("reaper=") :])
        self.assertTrue(self.alive(reaper), "the reaper runs")
        self.assertNotEqual(reaper, int(slot.rsplit("-", 1)[1]), "the reaper is not the handler")
        self.assertEqual(stat.S_IMODE(os.lstat(self.record_path(slot)).st_mode), 0o600)
        conn.sendall(PING)
        self.assertEqual(self.recv_line(conn), PING)
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
        self.assertEqual(self.record_lines(slot)[:2], lines, "the running lines are kept")
        self.wait_for(lambda: not self.alive(reaper), "the reaper's end", seconds=10)
        self.assertEqual(sorted(p.name for p in sock.parent.iterdir()), [slot, "sock"], "one record, no temporary file")
        data = self.recv_all(self.connect(sock, header="ACP-SEAT v2 x\n")).decode()
        self.assertTrue(data.startswith("acp-broker: refused: "), data)
        self.assertEqual(data.count("\n"), 1, data)
        self.assertEqual(sorted(p.name for p in sock.parent.iterdir()), [slot, "sock"], "a refusal makes no record")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_f_the_broker_end_removes_leftover_records_and_leaves_the_directory_standing(self):
        """U343g test (f), the U343i form: a record no client read (a raw connection's) and a planted record-named
        file stay in the broker directory; the relay removes its socket at its end and `broker_cleanup` the records
        once the socket is gone (U343j: the socket is the relay's alone) and leaves the
        directory, hcom-seat's, standing empty (no `rmdir`), and the broker ends by its signal with nothing named on
        stderr."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        leftover = sorted(p.name for p in sock.parent.iterdir() if p.name != "sock")
        self.assertEqual(len(leftover), 1, leftover)
        (sock.parent / "acp-w9-20260101-000000-1").write_text("ref=refs/acp-seat/w9/20260101-000000-1\n")
        (sock.parent / "acp-w9-20260101-000000-1.tmp").write_text("")
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assert_broker_dir_stands_empty(sock)
        self.assertNotIn("cannot remove", err)

    def test_g_a_record_that_cannot_be_removed_at_the_brokers_end_is_named_and_the_broker_exits_2(self):
        """U344b (verdicts U343j-62c10228 P3 `acp-broker:1000` and U343l-426188c6 P3 `:1028`): until this head
        `broker_cleanup` named a record it could not remove and returned 0, so the broker ended by its signal as if
        the directory were clean. A planted non-empty directory at a record's name (`rm -f` takes no directory)
        stands in for a record the broker cannot remove: the end names the record, names what remains, and the
        broker exits 2 instead of ending by SIGTERM; the socket is gone, the record no client read is gone, and the
        directory stands with the leftover alone."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        stuck = sock.parent / "acp-w9-20260101-000000-1"
        stuck.mkdir()
        (stuck / "inner").write_text("")
        self.addCleanup(lambda: shutil.rmtree(stuck, ignore_errors=True))
        stuck_real, dir_real = stuck.resolve(), sock.parent.resolve()
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, 2, err)
        self.assertIn(f"acp-broker: cannot remove the exit record {stuck_real}", err)
        self.assertIn(
            f"acp-broker: 1 exit record(s) remain in {dir_real} after the removal ({stuck_real}); remove them by hand",
            err,
        )
        self.assertIn("ended by SIGTERM; the broker exits 2 because an exit record remains (named above)", err)
        self.assertFalse(sock.exists() or sock.is_symlink(), "the socket is gone")
        self.assertEqual(self.broker_dir_entries(sock), [stuck.name], "the read record went; the leftover stands")

    def broker_dir_entries(self, sock):
        """The entries of the broker directory, dot names included; the test fails when the directory is gone."""
        self.assertTrue(sock.parent.is_dir() and not sock.parent.is_symlink(), f"{sock.parent} is not a directory")
        return sorted(p.name for p in sock.parent.iterdir())

    def assert_broker_dir_stands_empty(self, sock):
        """After the broker's end (U343i): the socket and every record are gone, and the directory hcom-seat made
        stands, 0700 and empty."""
        self.assertFalse(sock.exists() or sock.is_symlink(), "the socket is gone")
        self.assertEqual(self.broker_dir_entries(sock), [], "the records are gone and nothing else is there")
        self.assertEqual(stat.S_IMODE(os.lstat(sock.parent).st_mode), 0o700)

    # --- U343h, round 6: the record is written through the pinned helper on a held directory descriptor ---

    def plant_victim(self):
        """A scratch protected host file (the auditor's `.aws` file) a planted link points at, and its stat before."""
        victim = self.home_real / ".aws/credentials"
        victim.parent.mkdir(mode=0o700, exist_ok=True)
        victim.write_bytes(VICTIM)
        return victim, victim.stat()

    def assert_victim_untouched(self, victim, before):
        after = victim.stat()
        self.assertEqual(victim.read_bytes(), VICTIM, "the protected file's bytes")
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
        self.assertEqual(sorted(p.name for p in victim.parent.iterdir()), ["credentials"], "nothing landed beside it")

    def scratch_checkout(self, name="checkout"):
        """A copy of the levers the broker runs beside itself (the broker, the relay, the isolated git library, the
        record helper and the settings writer) under a scratch checkout with the manifest two levels up, so a test can
        alter a lever's bytes without touching the repository; returns the broker's path and the helper's."""
        checkout = Path(self.temp.name).resolve() / name
        (checkout / "scripts/orchestrator").mkdir(parents=True)
        (checkout / "home/dot_agents").mkdir(parents=True)
        for lever in (
            "acp-broker",
            "acp-relay.py",
            "git-isolated.sh",
            "acp-record-place.py",
            "seat-settings-render.sh",
        ):
            shutil.copy2(ROOT / "scripts/orchestrator" / lever, checkout / "scripts/orchestrator" / lever)
        shutil.copy2(ROOT / "home/dot_agents/agent-config.yaml", checkout / "home/dot_agents/agent-config.yaml")
        return checkout / "scripts/orchestrator/acp-broker", checkout / "scripts/orchestrator/acp-record-place.py"

    def test_a_a_link_planted_at_the_records_temporary_name_is_removed_and_its_target_untouched(self):
        """U343h test (a) (verdict U343g-8a049561 P1 `acp-broker:1262`, the auditor's reproduction inverted): the
        Router, which writes the broker directory and learns `<id>` from the first line, plants a link at `<id>.tmp`
        to a protected host file; the reaper's `printf >` followed it. The record is written by `acp-record-place.py`
        relative to the held directory descriptor: the link is unlinked as an entry, the record lands with its final
        line, the protected file keeps its bytes and nothing lands beside it; through the client, with the link
        planted after the record line, the exit status is omp's and the push word the pushed ref."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        victim, before = self.plant_victim()
        conn, slot, _task = self.held_connection(sock, repo, "w1")
        (sock.parent / f"{slot}.tmp").symlink_to(victim)
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
        self.assert_victim_untouched(victim, before)
        self.assertEqual(
            sorted(p.name for p in sock.parent.iterdir()), [slot, "sock"], "the link is gone, no temporary"
        )
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        first = slot
        (self.calls / "omp-status").write_text("3")
        self.addCleanup(lambda: (self.calls / "omp-status").unlink(missing_ok=True))
        client = self.client_popen(sock, repo, "w1")
        client.stdin.write(PING)
        client.stdin.flush()
        self.assertEqual(client.stdout.readline(), PING)
        (slot,) = self.acp_slots()
        head = self.commit_in(self.slot_task(slot))
        (sock.parent / f"{slot}.tmp").symlink_to(victim)
        out, err = client.communicate(timeout=120)
        match = re.fullmatch(rb"acp-seat: push=(refs/acp-seat/w1/\d{8}-\d{6}-\d+)\n", err)
        self.assertIsNotNone(match, err)
        self.assertEqual((client.returncode, out), (3, b""), err)
        self.assertEqual(self.scratch_git("rev-parse", "--verify", match.group(1).decode(), cwd=repo), head)
        self.assert_victim_untouched(victim, before)
        self.assertFalse(self.record_path(slot).exists(), "the client unlinked the record")
        self.assertEqual(
            sorted(p.name for p in sock.parent.iterdir()),
            [first, "sock"],
            "the raw session's record stays; the link is gone",
        )
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_b_a_link_planted_at_the_record_is_replaced_as_an_entry_and_its_target_untouched(self):
        """U343h test (b): the Router replaces its running record `<id>` by a link to a protected host file, or to a
        protected directory (where `mv -f` moved the temporary into that directory and left the link standing). The
        helper's `rename` relative to the held descriptor replaces the entry: the record is a regular 0600 file with
        its three lines, the target keeps its bytes and nothing lands in the directory."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        victim, before = self.plant_victim()
        for label, target in (("a link to a host file", victim), ("a link to a directory", victim.parent)):
            with self.subTest(case=label):
                conn, slot, _task = self.held_connection(sock, repo, "w1")
                record = self.record_path(slot)
                record.unlink()
                record.symlink_to(target)
                self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
                self.assertTrue(record.is_file() and not record.is_symlink(), "the record is a regular file")
                self.assertEqual(stat.S_IMODE(os.lstat(record).st_mode), 0o600)
                self.assert_victim_untouched(victim, before)
                self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
                record.unlink()
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_c_a_helper_whose_digest_differs_from_the_pin_never_runs_and_the_record_stays_incomplete(self):
        """U343h test (c): the reaper holds `acp-record-place.py` to its `claude.levers.sha256` pin through a private
        copy before each run (hcom-seat's form, U310f). With the helper's bytes altered beside the lever before a
        session, the running form is never written: the handler refuses before the record line and before omp
        starts, naming the record, no slot and no record remain, and the client exits 2 with the refusal. Altered
        after the record line, the final form is never written: the record keeps its two running lines, the stream
        carries nothing of the broker's, the slot is removed, and the client exits 2 naming `<id>`; the broker's
        stderr names the digest and the pin each time."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        broker, helper = self.scratch_checkout()
        original = helper.read_bytes()
        tampered = original + b"# one more line\n"
        helper.write_bytes(tampered)
        proc, sock = self.start_broker(name, cwd, broker=broker)
        data = self.recv_all(self.connect(sock, repo, "w1")).decode()
        self.assertTrue(data.startswith("acp-broker: refused: the reaper "), data)
        self.assertEqual(data.count("\n"), 1, data)
        self.assertIn("did not report ready within 10 s; omp acp not started", data)
        self.assertEqual(self.acp_slots(), [], "the slot is removed")
        self.assertEqual(sorted(p.name for p in sock.parent.iterdir()), ["sock"], "no record")
        self.assertNotIn(
            ["acp", "--profile", "dsh"], [c["argv"] for c in self.calls_of("omp")], "omp acp never started"
        )
        run = self.client(sock, repo, "w1", PING)
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-broker: refused: the reaper ", run.stderr)
        helper.write_bytes(original)
        conn, slot, _task = self.held_connection(sock, repo, "w1")
        helper.write_bytes(tampered)
        conn.shutdown(socket.SHUT_WR)
        self.assertEqual(self.recv_all(conn), b"", "nothing of the broker's on the stream")
        lines = self.record_lines(slot)
        self.assertEqual(len(lines), 2, lines)
        self.assertEqual(lines[0], f"ref=refs/acp-seat/w1/{slot[len('acp-w1-') :]}")
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        helper.write_bytes(original)
        client = self.client_popen(sock, repo, "w1")
        client.stdin.write(PING)
        client.stdin.flush()
        self.assertEqual(client.stdout.readline(), PING)
        (slot2,) = self.acp_slots()
        helper.write_bytes(tampered)
        out, err = client.communicate(timeout=120)
        self.assertEqual((client.returncode, out), (2, b""), err)
        self.assertIn(f"without a complete record {slot2}".encode(), err)
        self.assertNotIn(b"acp-seat: push=", err)
        self.assertEqual(len(self.record_lines(slot2)), 2, "the final line was never written")
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertEqual(err.count(f" of {helper} differs from the pin in "), 4, err)
        self.assert_broker_dir_stands_empty(sock)

    # --- U343o, round 12: the reaper owns the slot from its making, omp starts on its ready line, the log moves ---

    def pin_lever(self, broker, lever):
        """Pin a lever of the scratch checkout as it stands: its sha256 written over its own line of the scratch
        manifest two levels above the broker's copy, so an altered copy passes the pin check that reads it
        (lever_self_check for the broker itself, record_helper_pin_check for the record helper)."""
        manifest = broker.parents[2] / "home/dot_agents/agent-config.yaml"
        digest = hashlib.sha256(lever.read_bytes()).hexdigest()
        text, count = re.subn(
            rf"(?m)^(      {re.escape(lever.name)}: )[0-9a-f]{{64}}$", rf"\g<1>{digest}", manifest.read_text()
        )
        self.assertEqual(count, 1, f"one pin line for {lever.name} in the scratch manifest")
        manifest.write_text(text)

    def pin_helper(self, broker, helper):
        """Pin the scratch checkout's helper as it stands (pin_lever), so an altered helper passes
        record_helper_pin_check and runs (the pinned form of U343h test (c)'s tampered copy)."""
        self.pin_lever(broker, helper)

    def held_in_the_clone(self, sock, repo, name, client=False):
        """A connection held inside the clone's pack step by the fixture's `clone-sleep`: the raw connection (or the
        client's process when `client` is set), the slot name, the handler's pid (the slot name's last field) and
        the wall time the hold took to be reached (kept for its callers' records; no budget is derived from it, U440)."""
        (self.calls / "clone-sleeping").unlink(missing_ok=True)
        started = time.monotonic()
        conn = self.client_popen(sock, repo, name) if client else self.connect(sock, repo, name)
        self.wait_for(
            lambda: (self.calls / "clone-sleeping").exists(),
            "the clone's pack-objects under the Router's settings",
            seconds=30,
        )
        (slot,) = self.acp_slots()
        return conn, slot, int(slot.rsplit("-", 1)[1]), time.monotonic() - started

    def test_a_a_term_during_the_clone_leaves_no_slot_and_a_skipped_record(self):
        """U343o test (a) (verdict U343n-fd3db1b3 P1 `acp-broker:1581`): the slot was made at `:1581` and the reaper
        forked at `:1652`, after the settings write, the clone, the canary and the version read, so a TERM to the
        handler in that window ended a process with no trap and stranded the slot (the auditor's delayed clone). The
        reaper is forked as soon as the slot exists and owns its removal in every path: with the clone's pack held
        by the fixture's `clone-sleep`, a TERM to the handler pid leaves the slot gone within the fixed ceiling
        (U440), the record complete with `status=2 push=skipped` (omp never ran, so no exit line and no canary line
        reach the launch log), the raw connection sees EOF with no record line, the client exits 2 naming the
        closed connection, and the next connection on the same broker is served."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        (self.calls / "clone-sleep").write_text("3")
        self.addCleanup(lambda: (self.calls / "clone-sleep").unlink(missing_ok=True))
        self.addCleanup(self.remove_slots)
        conn, slot, pid, _setup = self.held_in_the_clone(sock, repo, "w1")
        started = time.monotonic()
        os.kill(pid, signal.SIGTERM)
        data = self.recv_all(conn)
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal", seconds=REAPER_CEILING)
        elapsed = time.monotonic() - started
        self.assertLessEqual(elapsed, REAPER_CEILING, f"the slot went in {elapsed:.1f} s, ceiling {REAPER_CEILING} s")
        self.assertEqual(data, b"", "EOF with no record line: the handler died before it")
        lines = self.record_lines(slot)
        self.assertIsNotNone(lines, f"no record {self.record_path(slot)}")
        self.assertEqual(len(lines), 3, lines)
        self.assertEqual(lines[2], "status=2 push=skipped")
        self.assertEqual(self.log_lines("w1"), [], "no canary line and no exit line: omp never ran")
        self.assertEqual(self.calls_of("omp"), [], "omp never started")
        client, slot2, pid2, _setup = self.held_in_the_clone(sock, repo, "w1", client=True)
        os.kill(pid2, signal.SIGTERM)
        out, err = client.communicate(timeout=120)
        self.assertEqual((client.returncode, out), (2, b""), err)
        self.assertIn(b"the broker closed the connection before its first line", err)
        self.wait_for(lambda: self.acp_slots() == [], "the second slot's removal", seconds=REAPER_CEILING)
        self.assertEqual(self.record_lines(slot2)[2], "status=2 push=skipped")
        (self.calls / "clone-sleep").unlink()
        conn, slot3, _task = self.held_connection(sock, repo, "w1")
        self.assertEqual(self.finish(conn, slot3), (b"", "status=0 push=none"))
        exits = [line for line in self.log_lines("w1") if " acp-broker: omp acp exit " in line]
        self.assertEqual(len(exits), 1, self.log_lines("w1"))
        self.wait_for(lambda: self.acp_slots() == [], "the third slot's removal")
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assert_broker_dir_stands_empty(sock)

    def test_b_a_record_helper_that_fails_after_its_rename_starts_no_omp_and_leaves_no_slot(self):
        """U343o test (b) (verdict U343n-fd3db1b3 P1 `acp-broker:1657`): the handler took the record's existence as
        the sign that the reaper was up, so a helper that renamed the record into place and then failed (the
        directory fsync) left a visible record while the reaper exited 1, and omp started with no reaper and a slot
        nobody removed. The reaper reports `ready <pid>` on its own pipe after a placement that returned 0, and the
        handler proceeds on that line alone: a copy of `acp-record-place.py` that raises right after its rename,
        pinned in the scratch manifest so it runs, refuses the connection with the ready line, starts no omp (no
        `omp-pid`, no srt call under the slot's settings), leaves no slot within the grace plus two seconds, and the
        record it left in its running form is swept at the broker's end."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        broker, helper = self.scratch_checkout()
        original = helper.read_text()
        rename = "                os.rename(name, record_id, src_dir_fd=dfd, dst_dir_fd=dfd)\n"
        self.assertEqual(original.count(rename), 1, "the helper's one rename of the record into place")
        # The two-argument form: the helper's line prints `strerror` (a message-only OSError prints `failed`).
        injected = '                raise OSError(errno.EIO, "injected after the rename")\n'
        helper.write_text(original.replace(rename, rename + injected))
        self.pin_helper(broker, helper)
        proc, sock = self.start_broker(name, cwd, broker=broker)
        self.addCleanup(self.remove_slots)
        started = time.monotonic()
        conn = self.connect(sock, repo, "w1")
        conn.shutdown(socket.SHUT_WR)
        data = self.recv_all(conn).decode()
        self.assertTrue(data.startswith("acp-broker: refused: the reaper (pid "), data)
        self.assertEqual(data.count("\n"), 1, data)
        self.assertIn("did not report ready", data)
        self.assertIn("omp acp not started", data)
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal", seconds=REAPER_CEILING)
        self.assertLessEqual(time.monotonic() - started, REAPER_CEILING, "the refusal and the removal in time")
        self.assertFalse((self.calls / "omp-pid").exists(), "omp acp never started")
        self.assertEqual(self.calls_of("omp"), [], "not even the version read: the refusal comes first")
        under_slot = [
            c["argv"][1]
            for c in self.calls_of("srt")
            if c["argv"][:1] == ["--settings"] and c["argv"][1].endswith("/settings.json")
        ]
        self.assertEqual(under_slot, [], "no srt call under the slot's settings")
        records = [p.name for p in sock.parent.iterdir() if p.name != "sock"]
        self.assertEqual(len(records), 1, records)
        self.assertRegex(records[0], r"^acp-w1-\d{8}-\d{6}-\d+$", "the record the helper renamed into place")
        lines = self.record_lines(records[0])
        self.assertEqual(len(lines), 2, lines)
        self.assertEqual(lines[0], f"ref=refs/acp-seat/w1/{records[0][len('acp-w1-') :]}")
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertIn("injected after the rename", err)
        self.assert_broker_dir_stands_empty(sock)

    def test_c_the_launch_log_lives_outside_every_seat_slot_and_a_planted_hard_link_is_never_followed(self):
        """U343o test (c) (verdict U343n-fd3db1b3 P1 `acp-broker:1264`): the launch log was
        `<seats-root>/.state/<name>/acp-launch.log`, inside the state slot an hcom-seat seat of that name may write,
        so a seat planted a hard link named `acp-launch.log` to a protected file, the `-L` test passed and this
        unsandboxed process appended to the target. The log is `<seats-root>/.state/broker-logs/<name>.log`, a
        directory this lever makes 0700 that no seat's settings grant: with the link planted before the connection,
        the victim keeps its bytes and its two links, the planted name holds the victim's bytes alone, nothing else
        is made under `.state/w1`, and the three lines of the launch stand in the broker's own directory; the
        header name `broker-logs` is refused by name."""
        name, cwd = self.make_router()
        repo, base = self.make_repo(cwd / "repo")
        victim, before = self.plant_victim()
        seat_slot = self.seats_path / ".state/w1"
        seat_slot.mkdir(mode=0o700)
        os.link(victim, seat_slot / "acp-launch.log")
        self.assertEqual(victim.stat().st_nlink, 2)
        proc, sock = self.start_broker(name, cwd)
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        self.assertEqual(victim.read_bytes(), VICTIM, "the protected file's bytes")
        self.assertEqual(victim.stat().st_nlink, 2, "the planted link still counts; nothing replaced it")
        self.assertEqual((seat_slot / "acp-launch.log").read_bytes(), VICTIM, "the planted name holds the victim alone")
        self.assertEqual(
            sorted(p.name for p in seat_slot.iterdir()), ["acp-launch.log"], "nothing made in the seat slot"
        )
        log_dir = self.seats_path / ".state/broker-logs"
        self.assertTrue(log_dir.is_dir() and not log_dir.is_symlink(), "the broker's log directory")
        self.assertEqual(stat.S_IMODE(os.lstat(log_dir).st_mode), 0o700)
        self.assertEqual(os.lstat(log_dir).st_uid, os.getuid())
        self.assertEqual(stat.S_IMODE(os.lstat(log_dir / "w1.log").st_mode), 0o600)
        stamp = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
        task = rf"{re.escape(str(self.seats_path))}/\.state/acp-w1-\d{{8}}-\d{{6}}-\d+/task"
        expected = [
            rf"^{stamp} acp-broker: canary {FOUR_WORDS}$",
            rf"^{stamp} acp-broker: omp acp start omp 18\.12\.6 cwd {task} repo {re.escape(str(repo))} ref HEAD base {base}$",
            rf"^{stamp} acp-broker: omp acp exit 0 push=none$",
        ]
        lines = self.log_lines("w1")
        self.assertEqual(len(lines), 3, lines)
        for got, want in zip(lines, expected):
            self.assertRegex(got, want)
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        data = self.recv_all(self.connect(sock, repo, "broker-logs")).decode()
        self.assertEqual(data.count("\n"), 1, data)
        self.assertIn("acp-broker: refused: the header name 'broker-logs' is the broker's log directory", data)
        self.assertEqual(self.acp_slots(), [], "nothing made for the refused name")
        self.assertEqual(sorted(p.name for p in log_dir.iterdir()), ["w1.log"], "no log for the refused name")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def sleeping_child(self, pid, seconds=1):
        """Whether the handler `pid` has the injected `/bin/sleep <seconds>` as a child now (`pgrep` by parent and
        argv), so a test's signal lands inside the window the sleep holds open (U344c: CI at a8adad11 sent TERM as
        soon as the slot appeared, which on a loaded runner landed between the `mkdir` and `slot_made=1` for the
        variant whose sleep follows the flag)."""
        run = subprocess.run(["pgrep", "-P", str(pid), "-f", f"/bin/sleep {seconds}"], capture_output=True, check=False)
        return run.returncode == 0

    def term_while_the_slot_is_made(self, after, signal_line):
        """The body of the two handler-window tests: a scratch copy of the lever with one line `/bin/sleep 1` right
        after the line `after` (the copy differs from the source by that line alone, asserted with difflib, and is
        pinned in the scratch manifest so it runs); a TERM to the handler pid once the slot exists and the injected
        sleep is its child (sleeping_child, so the signal lands where the sleep sits: after the flag in variant (a),
        between the `mkdir` and the flag in variant (b)) leaves the slot gone within the ceiling, the client exits 2
        with nothing on stdout and no record line, no record exists for the slot (had the reaper been forked, one
        ending `status=2 push=skipped` that the broker's end sweeps), omp never ran, the next connection on the same
        broker is served, and the broker's stderr carries `signal_line` once. The removal is waited for within the
        fixed ceiling (U440; the fixed 5 s of U343q and the setup-derived budget that replaced it both failed on
        loaded runners). Returns the elapsed seconds."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        broker, _helper = self.scratch_checkout()
        source = BROKER.read_text()
        self.assertEqual(source.count(after), 1, f"the one line the sleep follows: {after!r}")
        broker.write_text(source.replace(after, after + "/bin/sleep 1\n"))
        changed = [
            line
            for line in difflib.unified_diff(source.splitlines(), broker.read_text().splitlines(), lineterm="", n=0)
            if line[:1] in "+-" and line[:3] not in ("+++", "---")
        ]
        self.assertEqual(changed, ["+/bin/sleep 1"], "the copy differs from the source by that one line")
        self.pin_lever(broker, broker)
        proc, sock = self.start_broker(name, cwd, broker=broker)
        self.addCleanup(self.remove_slots)
        client = self.client_popen(sock, repo, "w1")
        self.addCleanup(lambda: client.poll() is None and client.kill())
        self.wait_for(lambda: self.acp_slots() != [], "the slot's making", seconds=30)
        (slot,) = self.acp_slots()
        pid = int(slot.rsplit("-", 1)[1])
        self.wait_for(lambda: self.sleeping_child(pid), "the injected sleep under the handler", seconds=30)
        started = time.monotonic()
        os.kill(pid, signal.SIGTERM)
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal", seconds=REAPER_CEILING)
        elapsed = time.monotonic() - started
        self.assertLessEqual(elapsed, REAPER_CEILING, f"the slot went in {elapsed:.1f} s, ceiling {REAPER_CEILING} s")
        out, err = client.communicate(timeout=120)
        self.assertEqual((client.returncode, out), (2, b""), err)
        self.assertIn(b"the broker closed the connection before its first line", err)
        lines = self.record_lines(slot)
        if lines is not None:
            self.assertEqual((len(lines), lines[-1]), (3, "status=2 push=skipped"), lines)
        self.assertEqual(self.calls_of("omp"), [], "omp never started")
        self.assertEqual(self.log_lines("w1"), [], "no canary line and no exit line: omp never ran")
        conn, slot2, _task = self.held_connection(sock, repo, "w1")
        self.assertEqual(self.finish(conn, slot2), (b"", "status=0 push=none"))
        self.wait_for(lambda: self.acp_slots() == [], "the second slot's removal")
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertEqual(err.count(signal_line), 1, err)
        self.assert_broker_dir_stands_empty(sock)
        return elapsed

    def test_a_a_term_while_the_slot_is_made_leaves_no_slot(self):
        """U343p (verdict U343o-c5c2b968 P1 `acp-broker:1648`, class handler-window, the second strike; the
        mechanism-change row of 2026-11-10T14:56:12Z, form remove): round 12 forked the reaper the moment the slot
        existed, and a TERM to the handler between the slot's `mkdir` and that fork (the two `mkfifo`, the two `exec`)
        still ended a process with no trap and stranded the slot; a shorter window is a window. The slot has an owner
        at every instant: one trap for HUP, INT and TERM, armed before the `mkdir` and disarmed after the reaper's
        ready line, removes the slot and exits 2 (after `slot_made=1` both removers run the idempotent slot_remove).
        The sleep sits right after `slot_made=1`: the trap removes the made slot and names it on stderr. At c5c2b968
        the same copy of that head's lever leaves the slot standing."""
        self.term_while_the_slot_is_made(
            "slot_made=1\n", "acp-broker: the connection ended by a signal before omp started; the slot removed"
        )

    def test_a_b_term_between_the_mkdir_and_the_flag_leaves_no_slot(self):
        """U343q (verdict U343p-901e096a P1 `acp-broker:1669`, class handler-window): a trap runs right after the
        simple command the signal arrived in, before the next command of the same list, so a TERM between the slot's
        `mkdir` and `slot_made=1` ran a trap whose slot_remove read the flag at 0 and returned 0 over a fresh slot.
        Before the flag the trap reads the state the `mkdir` left instead: the one state a bare `mkdir` leaves is an
        empty directory of this user, and `/bin/rmdir` takes exactly that (nothing non-empty, no file, no link). The
        sleep sits between the `mkdir` line and `slot_made=1`: the slot is gone within the ceiling and the broker's
        stderr names the empty slot removed. At 901e096a the same copy of that head's lever leaves the slot standing."""
        self.term_while_the_slot_is_made(
            '/bin/mkdir "${slot}" || refuse "cannot create the per-connection slot ${slot}"\n',
            "acp-broker: the connection ended by a signal as the slot was made; the empty slot removed",
        )

    def test_a_c_a_rmdir_that_fails_with_an_entry_present_between_the_mkdir_and_the_flag_is_named(self):
        """U344b (verdict U343q-668a020e P2 `acp-broker:439`): the pre-flag branch of the trap ran `/bin/rmdir` and
        said nothing when it failed, so an entry it could not take stood unnamed. With the sleep between the `mkdir`
        and `slot_made=1`, a file planted in the fresh slot during the sleep (the one state `rmdir` refuses that a
        test can reach) and a TERM to the handler: the slot stands with the planted file, the broker's stderr names
        the entry once and asks for a removal by hand, the client exits 2 with nothing on stdout, omp never ran, and
        once the slot is removed by hand the next connection on the same broker is served."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        broker, _helper = self.scratch_checkout()
        after = '/bin/mkdir "${slot}" || refuse "cannot create the per-connection slot ${slot}"\n'
        source = BROKER.read_text()
        self.assertEqual(source.count(after), 1, f"the one line the sleep follows: {after!r}")
        broker.write_text(source.replace(after, after + "/bin/sleep 1\n"))
        self.pin_lever(broker, broker)
        proc, sock = self.start_broker(name, cwd, broker=broker)
        self.addCleanup(self.remove_slots)
        client = self.client_popen(sock, repo, "w1")
        self.addCleanup(lambda: client.poll() is None and client.kill())
        self.wait_for(lambda: self.acp_slots() != [], "the slot's making", seconds=30)
        (slot,) = self.acp_slots()
        slot_path = self.seats_path / ".state" / slot
        pid = int(slot.rsplit("-", 1)[1])
        self.wait_for(lambda: self.sleeping_child(pid), "the injected sleep under the handler", seconds=30)
        (slot_path / "planted").write_text("")
        os.kill(pid, signal.SIGTERM)
        out, err = client.communicate(timeout=120)
        self.assertEqual((client.returncode, out), (2, b""), err)
        self.assertIn(b"the broker closed the connection before its first line", err)
        self.assertTrue((slot_path / "planted").exists(), "the slot stands with the planted entry")
        self.assertEqual(self.acp_slots(), [slot])
        self.assertEqual(self.calls_of("omp"), [], "omp never started")
        self.assertEqual(self.log_lines("w1"), [], "no canary line and no exit line: omp never ran")
        self.remove_slots()
        self.assertEqual(self.acp_slots(), [])
        conn, slot2, _task = self.held_connection(sock, repo, "w1")
        self.assertEqual(self.finish(conn, slot2), (b"", "status=0 push=none"))
        self.wait_for(lambda: self.acp_slots() == [], "the second slot's removal")
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        line = (
            f"acp-broker: the connection ended by a signal as the slot was made; the entry at {slot_path.resolve()} "
            "could not be removed (rmdir failed with the entry present); remove it by hand"
        )
        self.assertEqual(err.count(line), 1, err)
        self.assert_broker_dir_stands_empty(sock)

    def push_calls(self, slot):
        """The fake srt's calls after the launch (the push's), as (settings file, the git arguments after the
        library's flags) pairs: the worker's settings for a read of the worker's clone, the Router's for a write of
        the repository."""
        calls = self.calls_of("srt")
        launch = next(i for i, c in enumerate(calls) if c["argv"][-3:] == ["acp", "--profile", "dsh"])
        pairs = []
        for call in calls[launch + 1 :]:
            argv = call["argv"]
            self.assertEqual(argv[0], "--settings", argv)
            self.assertEqual(argv[2:4], ["--", "/usr/bin/env"], argv)
            self.assertIn("GIT_CONFIG_GLOBAL=/dev/null", argv)
            self.assertIn("core.hooksPath=/dev/null", argv)
            self.assertEqual(call["cwd"], str(self.slot_task(slot)), "the handler stays in the task")
            pairs.append((argv[1], argv[argv.index("-C") :]))
        return pairs

    def test_a_the_push_reads_the_worker_repository_inside_the_worker_settings(self):
        """U343f test (a) (verdict U343e-fd94feae P1 `:1146`, class broker-boundary): the push's `rev-parse` and
        `pack-objects` on the worker's clone ran through the isolated git outside every sandbox, so a `.git` the
        worker had written (an alternates file, a gitfile, HEAD) was read with the broker's own reach. They run
        through srt under the slot's `settings.json` (the worker's own sandbox, the form the clone already has on
        the Router's side), in the environment the launch had; `index-pack` and `update-ref` under the Router's
        settings, as before. The fake srt records every argv."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        head = self.commit_in(task)
        _rest, last = self.finish(conn, slot)
        match = re.fullmatch(r"status=0 push=(refs/acp-seat/w1/\S+)", last)
        self.assertIsNotNone(match, last)
        ref = match.group(1)
        settings = str(self.seats_path / ".state" / slot / "settings.json")
        template = str(self.seats_path / ".sandbox" / name / "srt-settings.json")
        self.assertEqual(
            self.push_calls(slot),
            [
                (settings, ["-C", str(task), "rev-parse", "--verify", "HEAD^{commit}"]),
                (settings, ["-C", str(task), "pack-objects", "--revs", "--stdout", "-q"]),
                (template, ["-C", str(repo), "index-pack", "--strict", "--stdin"]),
                (template, ["-C", str(repo), "update-ref", ref, head, ""]),
            ],
        )
        calls = self.calls_of("srt")
        launch = next(c for c in calls if c["argv"][-3:] == ["acp", "--profile", "dsh"])
        reads = [c for c in calls if c["argv"][1] == settings and "-C" in c["argv"]]
        self.assertEqual(len(reads), 2)
        for call in reads:
            self.assertEqual(call["env"], launch["env"], "the worker's git runs in the launch's environment")
        self.assertEqual(self.scratch_git("rev-parse", "--verify", ref, cwd=repo), head)
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_b_an_alternates_file_the_worker_planted_reaches_nothing_the_worker_may_not_read(self):
        """U343f test (b) (verdict U343e-fd94feae P1 `:1146`, Codex's reproduction): the worker writes
        `task/.git/objects/info/alternates` naming an object store under a path its settings deny (a scratch
        repository under `~/.aws` with one commit holding `private.txt`) and points HEAD at that store's commit.
        Outside any sandbox the plant resolves, and the push imported the store's objects into the Router's
        repository. Read inside the worker's own settings the store is unreadable (the fake srt denies the listed
        paths for the span of a command under a slot's settings): the push ends `push=failed` with the step named
        on stderr, the Router's repository holds no object of the store and no new ref, the slot is removed."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        store, _one = self.make_repo(self.home / ".aws" / "store")
        (store / "private.txt").write_text("the operator's secret\n")
        self.scratch_git("add", "private.txt", cwd=store)
        self.scratch_git("commit", "-q", "-m", "secret", cwd=store)
        secret = self.scratch_git("rev-parse", "HEAD", cwd=store)
        proc, sock = self.start_broker(name, cwd)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        rendered = json.loads((self.seats_path / ".state" / slot / "settings.json").read_text())
        self.assertIn(f"{self.home_real}/.aws", rendered["filesystem"]["denyRead"], "the store's root is denied")
        (task / ".git/objects/info").mkdir(exist_ok=True)
        (task / ".git/objects/info/alternates").write_text(f"{store}/.git/objects\n")
        (task / ".git/HEAD").write_text(secret + "\n")
        self.assertEqual(
            self.scratch_git("rev-parse", "HEAD", cwd=task), secret, "outside any sandbox the plant resolves"
        )
        (self.calls / "deny-paths").write_text(f"{self.home_real}/.aws\n")
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=failed"))
        held = subprocess.run(
            ["git", "cat-file", "-e", secret], cwd=repo, env=self.env, capture_output=True, text=True, check=False
        )
        self.assertNotEqual(held.returncode, 0, "the store's commit reached the Router's repository")
        self.assertEqual(self.scratch_git("for-each-ref", "refs/acp-seat/", cwd=repo), "")
        self.assertEqual(self.log_lines("w1")[-1].split(" acp-broker: ")[1], "omp acp exit 0 push=failed")
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        self.assertEqual(stat.S_IMODE(os.stat(self.home / ".aws").st_mode), 0o700, "the fake restored the path")
        settings = str(self.seats_path / ".state" / slot / "settings.json")
        self.assertEqual(
            [s for s, _args in self.push_calls(slot)], [settings], "one read under the worker's settings, no write"
        )
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertIn(f"failed at rev-parse on {task} inside the worker's settings {settings}", err)

    def test_c_the_exit_line_after_a_written_ref_never_refuses(self):
        """U343f test (c) (verdict U343e-fd94feae P2 `:1284`), the record form (U343g): the exit log's append failed
        after the ref was written and the handler refused, so the client read no report and learned no ref. The
        launch log and its directory are made unwritable while the worker runs: the record carries the pushed ref,
        the slot is removed, the log keeps its two lines, and the broker's stderr names the log and the line."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        head = self.commit_in(task)
        log_dir = self.seats_path / ".state/broker-logs"
        log = log_dir / "w1.log"
        before = self.log_lines("w1")
        self.assertEqual(len(before), 2, before)
        log.chmod(0o400)
        log_dir.chmod(0o500)
        try:
            _rest, last = self.finish(conn, slot)
        finally:
            log_dir.chmod(0o700)
            log.chmod(0o600)
        match = re.fullmatch(r"status=0 push=(refs/acp-seat/w1/\S+)", last)
        self.assertIsNotNone(match, last)
        ref = match.group(1)
        self.assertEqual(self.scratch_git("rev-parse", "--verify", ref, cwd=repo), head)
        self.assertEqual(self.log_lines("w1"), before, "the exit line could not be appended")
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertIn(
            f"acp-broker: cannot append the exit line 'omp acp exit 0 push={ref}' to the launch log {log}", err
        )

    def test_d_a_hangup_during_the_push_removes_the_slot_and_logs_one_exit_line(self):
        """U343f test (d) (verdict U343e-fd94feae P2 `:1282`), the reaper form (U343g): the traps were dropped before
        the push, so a hangup during it ended the handler at once with its slot in place and no exit line. The
        handler has no trap and the reaper has the teardown: a HUP while the fake srt's `pack-objects` sleeps ends
        the handler, and the connection ends with the slot removed, exactly one exit line and a complete record,
        `push=skipped` (the push had not finished) or the pushed ref, omp's own status in both."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        (self.calls / "pack-sleep").write_text("3")
        conn, slot, task = self.held_connection(sock, repo, "w1")
        pid = int(slot.rsplit("-", 1)[1])
        self.commit_in(task)
        conn.shutdown(socket.SHUT_WR)
        self.wait_for(
            lambda: (self.calls / "pack-sleeping").exists(),
            "the push's pack-objects under the worker's settings",
            seconds=15,
        )
        os.kill(pid, signal.SIGHUP)
        rest, last = self.finish(conn, slot)
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal", seconds=30)
        exits = [line for line in self.log_lines("w1") if " acp-broker: omp acp exit " in line]
        self.assertEqual(len(exits), 1, self.log_lines("w1"))
        self.assertRegex(exits[0], r" acp-broker: omp acp exit 0 push=(skipped|refs/acp-seat/w1/\S+)$")
        self.assertRegex(last, r"^status=0 push=(skipped|refs/acp-seat/w1/\S+)$")
        self.assertEqual(rest, b"", "ended by the signal: nothing of the broker's on the stream")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_a_slot_that_cannot_be_removed_gives_a_record_of_status_2_after_the_removal(self):
        """Verdict U343d-136fbe0a P2 `:1157`, the record form (U343g): the success report preceded the slot's
        removal, so a slot left behind exited the handler 2 while the client read exit 0. The reaper removes the slot
        first and the record's last line carries the connection's status: `.state` made read-only while the worker
        runs keeps the slot's entry in place, the record reads `status=2 push=none`, the log keeps omp's own status,
        the client exits 2."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        state = self.seats_path / ".state"
        conn, slot, _task = self.held_connection(sock, repo, "w1")
        state.chmod(0o500)
        try:
            self.assertEqual(self.finish(conn, slot), (b"", "status=2 push=none"))
        finally:
            state.chmod(0o700)
        self.assertEqual(self.acp_slots(), [slot], "the slot's entry stayed in the read-only directory")
        self.assertEqual(self.log_lines("w1")[-1].split(" acp-broker: ")[1], "omp acp exit 0 push=none")
        subprocess.run(["chmod", "-R", "u+rwX", str(state / slot)], check=True)
        subprocess.run(["rm", "-rf", str(state / slot)], check=True)
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertIn(f"the per-connection slot {state / slot} remains after its removal", err)

    def test_a_termination_ends_omp_and_its_descendants(self):
        """Verdict U343d-136fbe0a P2 `:1079`: the trap ended the immediate child alone and an omp tool descendant
        outlived the handler. The launch runs in its own process group and the reaper ends the group (U343g): the
        fake omp's sleeping child is gone when the broker has exited."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        (self.calls / "omp-child").touch()
        conn, _slot, _task = self.held_connection(sock, repo, "w1")
        self.wait_for(lambda: (self.calls / "omp-child-pid").exists(), "the descendant's start")
        pid = int((self.calls / "omp-child-pid").read_text())
        os.kill(pid, 0)
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)

        def gone():
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return True
            return False

        try:
            self.wait_for(gone, "the descendant's end", seconds=10)
        finally:
            if not gone():
                os.kill(pid, signal.SIGKILL)
        self.assertEqual(self.acp_slots(), [])
        conn.close()

    def test_a_canary_failure_starts_no_omp_and_removes_the_slot(self):
        """Any answer but the four words, a canary that did not run, and a probe that could write the canary file each
        refuse with one line; omp never starts, the slot is gone, nothing is logged (the state slot is not made)."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        wrong = (
            ("write-open read-denied ssh-denied debug-denied", "the sandbox does not hold (canary: write-open"),
            ("write-denied read-denied ssh-denied", "the sandbox does not hold (canary: write-denied read-denied ssh-denied)"),
            ("write-denied read-denied ssh-denied debug-open", "the sandbox does not hold (operator Claude debug writable)"),
        )  # fmt: skip
        for answer, message in wrong:
            with self.subTest(answer=answer):
                (self.calls / "canary-answer").write_text(answer + "\n")
                data = self.recv_all(self.connect(sock, repo, "w1")).decode()
                self.assertEqual(data.count("\n"), 1, data)
                self.assertIn(f"acp-broker: refused: {message}", data)
                self.assertIn("omp acp not started", data)
        (self.calls / "canary-answer").unlink()
        with self.subTest(answer="the four words, but the write probe made the file"):
            (self.calls / "canary-write").touch()
            data = self.recv_all(self.connect(sock, repo, "w1")).decode()
            self.assertIn(
                f"acp-broker: refused: the sandbox does not hold (canary: {FOUR_WORDS}); omp acp not started", data
            )
            (self.calls / "canary-write").unlink()
        with self.subTest(answer="the canary did not run"):
            (self.calls / "srt-fail").touch()
            data = self.recv_all(self.connect(sock, repo, "w1")).decode()
            self.assertIn("acp-broker: refused: the sandbox canary did not run under", data)
            self.assertIn("omp acp not started", data)
            (self.calls / "srt-fail").unlink()
        self.assertEqual(self.calls_of("omp"), [])
        self.assertEqual(self.acp_slots(), [])
        self.assertEqual(
            self.state_names(), ["anthropic", "claude", name], "no state slot and no log for a refused launch"
        )
        self.assertEqual(len(self.canaries()), 5, "one canary per connection, nothing after it")
        self.assertEqual(len(self.calls_of("srt")), 15, "the clone's two reads and the canary per connection")
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_a_1mib_json_rpc_line_is_relayed_equal_through_the_socket_and_back(self):
        """The U342 relay measurement as a test: a 1 MiB JSON-RPC line through the socket to the fake `omp acp` echo and
        back, equal after the record line, the record `status=0 push=none`; the same through the client, whose
        stdout is the line alone, whose stderr is the record's push word and whose exit status is the record's."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        line = one_mib_line()
        rest, last = self.exchange_record(sock, repo, "w1", line)
        self.assertEqual(len(rest), len(line))
        self.assertEqual(rest, line)
        self.assertEqual(last, "status=0 push=none")
        run = self.client(sock, repo, "w1", line)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(len(run.stdout), len(line))
        self.assertEqual(run.stdout, line)
        self.assertEqual(run.stderr, b"acp-seat: push=none\n")
        # Two launches, three lines each, in order.
        lines = self.log_lines("w1")
        self.assertEqual(len(lines), 6, lines)
        self.assertEqual(self.acp_slots(), [])
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_launch_log_holds_the_three_lines_in_order(self):
        """`<utc> acp-broker: canary <four words>`, `omp acp start omp <version> cwd <task> repo <repo> ref <ref> base
        <commit>`, `omp acp exit <status> push=<word>`, appended per launch to `<seats-root>/.state/broker-logs/<name>.log`,
        a directory the broker makes 0700 (U343o: outside every seat slot)."""
        name, cwd = self.make_router()
        repo, base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        line = b'{"jsonrpc":"2.0","id":1,"method":"initialize"}\n'
        self.assertEqual(self.exchange_record(sock, repo, "w1", line), (line, "status=0 push=none"))
        (self.calls / "omp-status").write_text("7")
        self.assertEqual(self.exchange_record(sock, repo, "w1", line, ref=base), (line, "status=7 push=none"))
        (self.calls / "omp-status").unlink()
        stamp = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
        task = rf"{re.escape(str(self.seats_path))}/\.state/acp-w1-\d{{8}}-\d{{6}}-\d+/task"
        expected = [
            rf"^{stamp} acp-broker: canary {FOUR_WORDS}$",
            rf"^{stamp} acp-broker: omp acp start omp 18\.12\.6 cwd {task} repo {re.escape(str(repo))} ref HEAD base {base}$",
            rf"^{stamp} acp-broker: omp acp exit 0 push=none$",
            rf"^{stamp} acp-broker: canary {FOUR_WORDS}$",
            rf"^{stamp} acp-broker: omp acp start omp 18\.12\.6 cwd {task} repo {re.escape(str(repo))} ref {base} base {base}$",
            rf"^{stamp} acp-broker: omp acp exit 7 push=none$",
        ]
        lines = self.log_lines("w1")
        self.assertEqual(len(lines), len(expected), lines)
        for got, want in zip(lines, expected):
            self.assertRegex(got, want)
        log_dir = self.seats_path / ".state/broker-logs"
        self.assertEqual(stat.S_IMODE(os.lstat(log_dir).st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(os.lstat(log_dir / "w1.log").st_mode), 0o600)
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_session_new_cwd_is_mapped_onto_the_slots_task_and_the_original_is_logged(self):
        """U449b (table row s22; U449's trace): dsh-subagent-acp names the Router's own task as the ACP `session/new`
        cwd, a directory the worker's sandbox denies by design (R-45), so Claude Code died at its spawn. The broker's
        side maps that one field onto the slot's task before omp reads it: the fake omp, which echoes its stdin,
        receives the `session/new` line with `params.cwd` equal to the slot's task and every other member as sent;
        the launch log gains `session cwd "<original>" mapped to <task>` between the start and the exit lines, the
        original JSON-quoted (an untrusted string of the Router's: a control character never reaches the log raw).
        A `session/new` without a cwd, with a non-string cwd, with no params object or none at all, a line that is
        not JSON or not UTF-8, a JSON line that is no object, and every other method pass through byte for byte."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        router_task = f"{cwd}/task"
        request = {"jsonrpc": "2.0", "id": 2, "method": "session/new", "params": {"cwd": router_task, "mcpServers": []}}
        conn.sendall(json.dumps(request, separators=(",", ":")).encode() + b"\n")
        echoed = self.recv_line(conn)
        self.assertEqual(json.loads(echoed), {**request, "params": {"cwd": str(task), "mcpServers": []}})
        self.assertNotIn(router_task.encode(), echoed)
        odd_cwd = "/tmp/x\né y"
        odd = {
            "jsonrpc": "2.0",
            "id": "three",
            "method": "session/new",
            "params": {"cwd": odd_cwd, "mcpServers": [{"name": "m"}]},
        }
        conn.sendall(json.dumps(odd).encode() + b"\r\n")
        echoed = self.recv_line(conn)
        self.assertTrue(echoed.endswith(b"\r\n"), echoed)
        self.assertEqual(json.loads(echoed), {**odd, "params": {"cwd": str(task), "mcpServers": [{"name": "m"}]}})
        rt = router_task.encode()
        through = (
            b'{"jsonrpc":"2.0","id":4,"method":"session/new","params":{"mcpServers":[]}}\n',
            b'{"jsonrpc":"2.0","id":5,"method":"session/new","params":{"cwd":7,"mcpServers":[]}}\n',
            b'{"jsonrpc":"2.0","id":6,"method":"session/new","params":{"cwd":["' + rt + b'"]}}\n',
            b'{"jsonrpc":"2.0","id":7,"method":"session/new","params":"' + rt + b'"}\n',
            b'{"jsonrpc":"2.0","id":8,"method":"session/new"}\n',
            b'{"jsonrpc":"2.0","id":9,"method":"session/prompt","params":{"cwd":"' + rt + b'","sessionId":"s"}}\n',
            b'{"jsonrpc":"2.0","id":10,"method":"session/load","params":{"cwd":"' + rt + b'"}}\r\n',
            b'{"jsonrpc":"2.0","method":"session/cancel","params":{"cwd":"' + rt + b'"}}\n',
            b'["session/new", {"cwd": "' + rt + b'"}]\n',
            b'"session/new"\n',
            b"session/new cwd=" + rt + b"\n",
            b'{"jsonrpc":"2.0","id":11,"method":"session/new","params":{"cwd":"' + rt + b'"}\n',
            b'\xff\xfe{"method":"session/new","params":{"cwd":"' + rt + b'"}}\n',
            PING,
        )
        for raw in through:
            with self.subTest(line=raw[:48]):
                conn.sendall(raw)
                self.assertEqual(self.recv_line(conn), raw)
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
        lines = self.log_lines("w1")
        stamp = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
        self.assertEqual(len(lines), 5, lines)
        self.assertRegex(lines[0], rf"^{stamp} acp-broker: canary {FOUR_WORDS}$")
        self.assertRegex(lines[1], rf"^{stamp} acp-broker: omp acp start omp 18\.12\.6 cwd {re.escape(str(task))} ")
        self.assertRegex(
            lines[2],
            rf"^{stamp} acp-broker: session cwd {re.escape(json.dumps(router_task))} mapped to {re.escape(str(task))}$",
        )
        self.assertRegex(
            lines[3],
            rf"^{stamp} acp-broker: session cwd {re.escape(json.dumps(odd_cwd))} mapped to {re.escape(str(task))}$",
        )
        self.assertNotIn("\né", lines[3], "the control and non-ASCII characters are escaped, never raw")
        self.assertRegex(lines[4], rf"^{stamp} acp-broker: omp acp exit 0 push=none$")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_session_cwd_mapping_is_one_function_from_the_line_to_the_line(self):
        """acp-relay.py `map_session_cwd(line, task)` returns (the line, the original cwd): identity and None for
        every line but a `session/new` object whose `params.cwd` is a string, whose cwd string token alone becomes the
        task and every other byte of the line stays as it came (U449c: the spacing, the key order, an escaped method,
        a lone surrogate or a number beyond a double elsewhere in the request, the terminator; tested by table). The
        mapper is total (verdict U449-6017f53f P1 `:330`, P1 `:340`, P2 `:340`): a line nested beyond NESTING_CAP, a
        repeated key, a line over LINE_CAP, bytes after the object, an invalid escape or a raw control character
        anywhere, an empty line and a bare terminator pass through unchanged and nothing raises."""
        relay = load_relay()
        task = "/seats/.state/acp-w1-20260101-000000-1/task"
        t = task.encode()
        mapped = b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"' + t + b'","mcpServers":[]}}'
        deep = b"[" * 60 + b"]" * 60
        table = (
            # mapped: the cwd token replaced, every other byte kept
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/r","mcpServers":[]}}\n', mapped + b"\n", "/r"),
            (b'{"jsonrpc": "2.0", "id": 1, "method": "session/new", "params": {"cwd": "/r", "mcpServers": []}}\r\n', b'{"jsonrpc": "2.0", "id": 1, "method": "session/new", "params": {"cwd": "' + t + b'", "mcpServers": []}}\r\n', "/r"),
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/r","mcpServers":[]}}', mapped, "/r"),
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"","mcpServers":[]}}\n', mapped + b"\n", ""),
            ('{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/é\\n","mcpServers":[]}}\n'.encode(), mapped + b"\n", "/é\n"),
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"' + t + b'","mcpServers":[]}}\n', mapped + b"\n", task),
            (b'{"params":{"mcpServers":[],"cwd":"/r"},"method":"session/new","id":1,"jsonrpc":"2.0"}\n', b'{"params":{"mcpServers":[],"cwd":"' + t + b'"},"method":"session/new","id":1,"jsonrpc":"2.0"}\n', "/r"),
            (b'{"method":"session\\/new","params":{"cwd":"\\u002fr"}}\n', b'{"method":"session\\/new","params":{"cwd":"' + t + b'"}}\n', "/r"),
            (b'  {"method":"session/new","params":{"cwd":"/r"}}  \n', b'  {"method":"session/new","params":{"cwd":"' + t + b'"}}  \n', "/r"),
            (b'{"jsonrpc":"2.0","id":"\\ud800","method":"session/new","params":{"cwd":"/r","mcpServers":[{"name":"\\udfff"}]}}\n', b'{"jsonrpc":"2.0","id":"\\ud800","method":"session/new","params":{"cwd":"' + t + b'","mcpServers":[{"name":"\\udfff"}]}}\n', "/r"),
            (b'{"method":"session/new","params":{"cwd":"\\ud800/r"}}\n', b'{"method":"session/new","params":{"cwd":"' + t + b'"}}\n', "\ud800/r"),
            (b'{"jsonrpc":"2.0","id":1e1000000,"method":"session/new","params":{"cwd":"/r","n":-1e1000000}}\n', b'{"jsonrpc":"2.0","id":1e1000000,"method":"session/new","params":{"cwd":"' + t + b'","n":-1e1000000}}\n', "/r"),
            (b'{"method":"session/new","params":{"cwd":"/r","x":' + deep + b"}}\n", b'{"method":"session/new","params":{"cwd":"' + t + b'","x":' + deep + b"}}\n", "/r"),
            # identity: not the shape
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"mcpServers":[]}}\n', None, None),
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":null}}\n', None, None),
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":["/r"]}}\n', None, None),
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":[]}\n', None, None),
            (b'{"jsonrpc":"2.0","id":1,"method":"session/new"}\n', None, None),
            (b'{"jsonrpc":"2.0","id":1,"method":"session/prompt","params":{"cwd":"/r"}}\n', None, None),
            (b'{"jsonrpc":"2.0","id":1,"method":["session/new"],"params":{"cwd":"/r"}}\n', None, None),
            (b'{"jsonrpc":"2.0","id":1,"result":{"cwd":"/r"}}\n', None, None),
            (b'["session/new",{"cwd":"/r"}]\n', None, None),
            (b'"session/new"\n', None, None),
            (b"7\n", None, None),
            (b"\n", None, None),
            (b"", None, None),
            (b"not json\n", None, None),
            (b'{"method":"session/new","params":{"cwd":"/r"}\n', None, None),
            (b'\xff{"method":"session/new","params":{"cwd":"/r"}}\n', None, None),
            # identity: the mapper's bounds, an ambiguous shape, a line that is not valid JSON; nothing raises
            (b'{"method":"session/new","params":{"cwd":"/r","x":' + b"[" * 70 + b"]" * 70 + b"}}\n", None, None),
            (b'{"a":' + b"[" * 200000 + b"]" * 200000 + b',"method":"session/new","params":{"cwd":"/r"}}\n', None, None),
            (b'{"method":"session/new","params":{"cwd":"/a","cwd":"/b"}}\n', None, None),
            (b'{"method":"ping","method":"session/new","params":{"cwd":"/r"}}\n', None, None),
            (b'{"method":"session/new","params":{"cwd":"/r"}} x\n', None, None),
            (b'{"method":"session/new","params":{"cwd":"/r"},"x":"\\q"}\n', None, None),
            (b'{"method":"session/new","params":{"cwd":"/r\t"}}\n', None, None),
            (b'{"method":"session/new","params":{"cwd":"/r","pad":"' + b"x" * (1 << 20) + b'"}}\n', None, None),
            (b'{"jsonrpc":"2.0","id":1,"method":"ping"}\r\n', None, None),
            (b"\r\n", None, None),
            (b"   \n", None, None),
        )  # fmt: skip
        for line, expected, original in table:
            with self.subTest(line=line[:60]):
                self.assertEqual(relay.map_session_cwd(line, task), (line if expected is None else expected, original))

    def test_the_copier_forwards_every_line_it_read_whatever_the_mapper_made_of_it(self):
        """U449c (verdict U449-6017f53f P1 `acp-relay.py:330` and P1 `:340`): a 400 KB line of nested arrays raised
        RecursionError in the copier thread, which died with omp's stdin open, so the connection hung; a request with
        an escaped lone surrogate elsewhere raised UnicodeEncodeError at the re-serialisation and the `session/new`
        line was dropped. The mapper is total and the copier forwards every line it read: `map_session_cwd_run` on
        `/bin/cat` with the stream (the nested line, a `session/new`, a `session/new` carrying a lone surrogate and a
        number beyond a double elsewhere, a ping, then EOF) gives cat every line, the first and the last unchanged,
        the second and the third mapped with their other bytes as sent; one record per mapping on stderr; the mapper
        ends 0 when the stream ends (cat reads EOF), within the timeout."""
        task = "/seats/.state/acp-w1-20260101-000000-1/task"
        t = task.encode()
        nested = b'{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/r","x":' + b"[" * 200000 + b"]" * 200000 + b"}}\n"  # fmt: skip
        new = b'{"jsonrpc":"2.0","id":2,"method":"session/new","params":{"cwd":"/r","mcpServers":[]}}\n'
        odd = b'{"jsonrpc":"2.0","id":"\\ud800","method":"session/new","params":{"cwd":"/r","n":1e1000000}}\r\n'
        code = textwrap.dedent(
            f"""\
            import importlib.util, sys
            spec = importlib.util.spec_from_file_location("acp_relay", {str(RELAY)!r})
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.exit(module.map_session_cwd_run({task!r}, ["/bin/cat"]))
            """
        )
        run = subprocess.run(
            [sys.executable, "-I", "-S", "-c", code], input=nested + new + odd + PING, capture_output=True, timeout=30,
            check=False,
        )  # fmt: skip
        self.assertEqual(run.returncode, 0, run.stderr)
        mapped = new.replace(b'"cwd":"/r"', b'"cwd":"' + t + b'"') + odd.replace(b'"cwd":"/r"', b'"cwd":"' + t + b'"')
        self.assertEqual(run.stdout, nested + mapped + PING)
        self.assertEqual(run.stderr, (b'acp-relay.py: session cwd "/r" mapped to ' + t + b"\n") * 2)

    def test_a_launch_stderr_file_the_reaper_cannot_open_is_named_and_the_exit_line_is_still_written(self):
        """U449c (verdict U449-6017f53f P2 `acp-broker:1509`, standing order 21): the reaper read the launch's stderr
        file through a process substitution whose status nothing read (a `head` that failed read as an empty file and
        the loop returned 0; shellcheck SC2312 on every CI leg). The file is read by a plain redirection into a bounded
        loop and the redirection's status is read: with the file made unreadable (mode 0) while the worker runs, after
        a `session/new` the mapper recorded, the broker's stderr names the file it could not open and the log holds the
        start and the exit lines with no mapping line between them; with a directory put at the file's name the
        regular-file gate names it. The exit line, the record and the slot's removal follow each time."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        request = b'{"jsonrpc":"2.0","id":2,"method":"session/new","params":{"cwd":"/r","mcpServers":[]}}\n'
        conn, slot, task = self.held_connection(sock, repo, "w1")
        conn.sendall(request)
        self.assertIn(b'"cwd":"' + str(task).encode() + b'"', self.recv_line(conn))
        unreadable = self.seats_path / ".state" / slot / "stderr"
        unreadable.chmod(0)
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
        conn, slot, task = self.held_connection(sock, repo, "w1")
        conn.sendall(request)
        self.assertIn(b'"cwd":"' + str(task).encode() + b'"', self.recv_line(conn))
        directory = self.seats_path / ".state" / slot / "stderr"
        directory.unlink()
        directory.mkdir(mode=0o700)
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
        self.wait_for(lambda: self.acp_slots() == [], "the slots' removal")
        lines = self.log_lines("w1")
        self.assertEqual(len(lines), 6, lines)
        stamp = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
        for n in (2, 5):
            self.assertRegex(lines[n], rf"^{stamp} acp-broker: omp acp exit 0 push=none$")
        self.assertEqual([line for line in lines if "session cwd" in line], [], "no record was read from either file")
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertIn(
            f"acp-broker: cannot open the launch's stderr file {unreadable} for reading; its lines are not read\n", err
        )
        self.assertIn(
            f"acp-broker: the launch's stderr file {directory} is not a regular file; its lines are not read\n", err
        )

    def test_srt_and_omp_run_by_their_physical_argv_under_the_listed_environment(self):
        """srt, omp and git are found through a link directory first on the caller's PATH and run by their physical
        files (the fake records argv0); omp's environment holds exactly the listed names; the srt argv is `--settings
        <slot settings> -- /usr/bin/env PATH=<seat path> <python3 argv> -I -S <acp-relay.py> --map-session-cwd <task>
        -- <omp argv> acp --profile dsh` in the slot's task (U449b: the mapper runs inside the sandbox); the clone's
        two git runs and the canary run under the Router's own settings file, the push's read of the worker's HEAD
        under the slot's (U343f)."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        links = Path(self.temp.name).resolve() / "links"
        links.mkdir()
        for tool in ("srt", "omp"):
            (links / tool).symlink_to(self.bindir / tool)
        git_real = Path(os.path.realpath("/usr/bin/git"))
        (links / "git").symlink_to(git_real)
        path = f"{links}:{self.bindir}:{SYSTEM_PATH}"
        proc, sock = self.start_broker(name, cwd, PATH=path, USER="u343", LANG="C.UTF-8", SECRET_OF_THE_CALLER="x")
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        version, launch = self.calls_of("omp")
        self.assertEqual(version["argv"], ["--version"])
        self.assertEqual(launch["argv"], ["acp", "--profile", "dsh"])
        self.assertEqual(launch["argv0"], str(self.bindir / "omp"), "the physical file, not the link")
        slots = {
            Path(call["argv"][1]).parent.name
            for call in self.calls_of("srt")
            if call["argv"][1].endswith("/settings.json")
        }
        (slot,) = slots
        self.assertRegex(slot, r"^acp-w1-\d{8}-\d{6}-\d+$")
        task = str(self.slot_task(slot))
        self.assertEqual(launch["cwd"], task)
        seat_path = f"{SYSTEM_PATH.split(':')[0]}:/bin:/usr/sbin:/sbin:{path}"
        # The interpreter's own additions (a framework Python on macOS exports __CF_USER_TEXT_ENCODING) are no input
        # of the broker's: they join the expected set, as in test_hcom_seat_dsh.interpreter_own_names.
        probe = subprocess.run(
            ["/usr/bin/env", "-i", f"PATH={SYSTEM_PATH}", str(self.python), "-c", "import json, os; print(json.dumps(sorted(os.environ)))"],
            capture_output=True, text=True, check=True,
        )  # fmt: skip
        own = set(json.loads(probe.stdout)) - {"PATH"}
        listed = {"HOME": str(self.home), "PATH": seat_path, "OMP_PROFILE": "dsh",
                  "CLAUDE_CONFIG_DIR": str(self.seats_path / ".state/claude"), "AWS_SHARED_CREDENTIALS_FILE": "/dev/null",
                  "AWS_CONFIG_FILE": "/dev/null", "HCOM_SEAT_SANDBOX": str(self.seats_path / ".state" / slot),
                  "REGIME_ANTHROPIC_KEY_FILE": str(self.key_file), "USER": "u343", "LANG": "C.UTF-8"}  # fmt: skip
        self.assertEqual({k: v for k, v in launch["env"].items() if k not in own}, listed)
        self.assertEqual(set(launch["env"]) - own, set(listed))
        resolve, pack, canary, version_call, launch_call, head_read = self.calls_of("srt")
        router_settings = str(self.seats_path / ".sandbox" / name / "srt-settings.json")
        for call in (resolve, pack):
            self.assertEqual(
                call["argv"][:3], ["--settings", router_settings, "--"], "the clone reads inside the Router's settings"
            )
            self.assertEqual(call["argv"][3], "/usr/bin/env")
            self.assertIn(str(git_real), call["argv"], "git by its physical file")
            self.assertIn("GIT_CONFIG_GLOBAL=/dev/null", call["argv"])
            self.assertIn("-c", call["argv"])
            self.assertIn("core.hooksPath=/dev/null", call["argv"])
            self.assertEqual(set(call["env"]) - own, {"HOME", "PATH"})
        self.assertEqual(resolve["argv"][-5:], ["-C", str(repo), "rev-parse", "--verify", "HEAD^{commit}"])
        self.assertEqual(pack["argv"][-6:], ["-C", str(repo), "pack-objects", "--revs", "--stdout", "-q"])
        self.assertEqual(canary["argv0"], str(self.bindir / "srt"))
        settings = str(self.seats_path / ".state" / slot / "settings.json")
        self.assertEqual(canary["argv"][:5], ["--settings", settings, "--", "/bin/sh", "-c"])
        self.assertEqual(canary["argv"][6:], ["canary", f"{self.seats_path}/.state/{slot}/canary", settings,
                                              f"{self.home}/.ssh", f"{self.home_real}/.claude/debug/acp-broker-canary-" + slot.rsplit("-", 1)[1]])  # fmt: skip
        self.assertEqual(version_call["argv"], ["--settings", settings, "--", "/usr/bin/env", f"PATH={seat_path}",
                                                str(self.python), str(self.bindir / "omp"), "--version"])  # fmt: skip
        relay = str(BROKER.resolve().parent / "acp-relay.py")
        self.assertEqual(launch_call["argv"], ["--settings", settings, "--", "/usr/bin/env", f"PATH={seat_path}",
                                               str(self.python), "-I", "-S", relay, "--map-session-cwd", task, "--",
                                               str(self.python), str(self.bindir / "omp"), "acp", "--profile", "dsh"])  # fmt: skip
        self.assertEqual(launch_call["cwd"], task)
        self.assertEqual(
            head_read["argv"][:4],
            ["--settings", settings, "--", "/usr/bin/env"],
            "the push reads inside the worker's settings",
        )
        self.assertIn(str(git_real), head_read["argv"], "git by its physical file")
        self.assertIn("GIT_CONFIG_GLOBAL=/dev/null", head_read["argv"])
        self.assertIn("core.hooksPath=/dev/null", head_read["argv"])
        self.assertEqual(head_read["argv"][-5:], ["-C", task, "rev-parse", "--verify", "HEAD^{commit}"])
        self.assertEqual(head_read["cwd"], task)
        self.assertEqual(set(head_read["env"]) - own, set(listed), "the worker's git sees the launch's names")
        # srt itself saw the listed names and nothing of the caller's (the outer PATH is the system directories).
        self.assertEqual(set(canary["env"]) - own, set(listed))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_two_connections_at_once_hold_two_slots_and_two_settings_files(self):
        """Two workers at once: two per-connection slots, each with its settings file and its clone, two state slots;
        both gone when their connections end, and the socket serves a third."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        c1 = self.connect(sock, repo, "w1")
        c2 = self.connect(sock, repo, "w2")
        s1 = self.record_line(c1)
        s2 = self.record_line(c2)
        c1.sendall(PING)
        c2.sendall(PING)
        self.assertEqual(self.recv_line(c1), PING)
        self.assertEqual(self.recv_line(c2), PING)
        slots = self.acp_slots()
        self.assertEqual(slots, sorted([s1, s2]), "the record lines name the two slots")
        self.assertEqual([s.split("-")[1] for s in slots], ["w1", "w2"])
        for slot in slots:
            path = self.seats_path / ".state" / slot
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700)
            self.assertTrue((path / "settings.json").is_file(), slot)
            self.assertEqual(stat.S_IMODE(os.lstat(path / "settings.json").st_mode), 0o600)
            self.assertEqual((path / "task/a.txt").read_text(), "hello\n")
        settings = [json.loads((self.seats_path / ".state" / s / "settings.json").read_text()) for s in slots]
        self.assertEqual([s["filesystem"]["allowWrite"][0] for s in settings], [str(self.slot_task(s)) for s in slots])
        self.assertEqual(
            self.state_names(), ["anthropic", "broker-logs", "claude", name], "no seat slot is made for a worker"
        )
        self.assertEqual(self.finish(c1, s1), (b"", "status=0 push=none"))
        self.assertEqual(self.finish(c2, s2), (b"", "status=0 push=none"))
        records = sorted(p.name for p in sock.parent.iterdir() if p.name != "sock")
        self.assertEqual(records, slots, "two records, one per connection, until a client reads them")
        self.wait_for(lambda: self.acp_slots() == [], "the two slots' removal")
        self.assertEqual(self.exchange_record(sock, repo, "w3", PING), (PING, "status=0 push=none"))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_socket_and_the_records_are_gone_after_the_broker_exits_and_the_directory_stands(self):
        """A termination while a worker runs: the relay ends the handler, the handler's reaper ends omp, logs the exit,
        writes the record and removes the slot (U343g), the relay removes the socket, the broker the records, the
        directory hcom-seat made stands empty (U343i), and the broker ends by the signal."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        broker_dir = sock.parent
        self.assertEqual(stat.S_IMODE(os.lstat(broker_dir).st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(os.lstat(sock).st_mode), 0o600)
        conn, slot, _task = self.held_connection(sock, repo, "w1")
        self.assertEqual(stat.S_IMODE(os.lstat(self.record_path(slot)).st_mode), 0o600)
        self.assertEqual(len(self.acp_slots()), 1)
        status, out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertEqual(out, f"acp-broker: listening on {sock}\n")
        self.assert_broker_dir_stands_empty(sock)
        self.assertEqual(self.acp_slots(), [], "the live worker's slot went with the broker")
        self.assertEqual(self.recv_all(conn), b"", "nothing of the broker's on the stream after the record line")
        lines = self.log_lines("w1")
        self.assertEqual(len(lines), 3, lines)
        self.assertRegex(lines[2], r" acp-broker: omp acp exit \d+ push=skipped$")
        # A hangup and an interrupt do the same, each ending the broker by its own signal, on the standing directory.
        for sig in (signal.SIGHUP, signal.SIGINT):
            with self.subTest(signal=sig.name):
                proc, sock = self.start_broker(name, cwd)
                self.assertEqual(self.stop_broker(proc, sig)[0], -sig)
                self.assert_broker_dir_stands_empty(sock)

    def relay_pid(self, proc):
        """The relay's pid: the listening broker's one child (`pgrep` by parent), or None until it exists."""
        run = subprocess.run(["pgrep", "-P", str(proc.pid)], capture_output=True, text=True, check=False)
        pids = run.stdout.split()
        return int(pids[0]) if len(pids) == 1 else None

    def test_a_signal_between_the_socket_bind_and_the_readiness_line_ends_the_broker_by_the_signal_with_the_socket_gone(
        self,
    ):
        """U447 (the ubuntu-24.04 leg at PR 757's head 1d447846: `AssertionError: 2 != -1` for HUP, then the socket
        standing for INT): the relay installed its HUP, INT and TERM handlers after the bind, and the fixture took the
        socket's existence for readiness, so a signal to the broker could land while the relay still held the default
        dispositions; the broker's trap sent it TERM, it died with the socket bound, and broker_cleanup read the
        standing socket as another broker's and exited 2. A scratch copy of the relay with one `/bin/sleep 1` right
        after the bind and before the readiness line (the copy differs from the source by that line alone, asserted
        with difflib, and is pinned in the scratch manifest so the broker runs it): a HUP, INT or TERM to the broker
        once the socket exists and the sleep runs under the relay ends the broker by that signal, with nothing on
        stderr, the socket gone and the directory standing empty. At 4fda927c the same copy of that head's relay ends
        the broker with exit 2 and the socket standing."""
        broker, _helper = self.scratch_checkout()
        relay = broker.parent / "acp-relay.py"
        source = relay.read_text()
        after = ".bind(base)\n"
        injected = '            subprocess.run(["/bin/sleep", "1"], check=False)\n'
        self.assertEqual(source.count(after), 1, f"the one line the sleep follows: {after!r}")
        relay.write_text(source.replace(after, after + injected))
        changed = [
            line
            for line in difflib.unified_diff(source.splitlines(), relay.read_text().splitlines(), lineterm="", n=0)
            if line[:1] in "+-" and line[:3] not in ("+++", "---")
        ]
        self.assertEqual(changed, ["+" + injected.rstrip("\n")], "the copy differs from the source by that one line")
        self.pin_lever(broker, relay)
        for n, sig in enumerate((signal.SIGHUP, signal.SIGINT, signal.SIGTERM), start=1):
            with self.subTest(signal=sig.name):
                name, cwd = self.make_router(f"router-20261111-00000{n}-1")
                proc, sock = self.launch_broker(name, cwd, broker=broker)
                self.wait_for(lambda: sock.exists() or proc.poll() is not None, "the socket's bind", seconds=60)
                if proc.poll() is not None:
                    out, err = proc.communicate()
                    self.fail(f"the broker ended before the bind: {proc.returncode} {out!r} {err!r}")
                pid = self.relay_pid(proc)
                self.assertIsNotNone(pid, "the relay runs under the broker once the socket exists")
                self.wait_for(lambda: self.sleeping_child(pid), "the injected sleep under the relay", seconds=30)
                status, _out, err = self.stop_broker(proc, sig)
                self.assertEqual(status, -sig, err)
                self.assertEqual(err, "", "nothing refused and nothing remained")
                self.assert_broker_dir_stands_empty(sock)

    def probe_connections(self, sock, seconds):
        """Connections to `sock` by name from its directory every 0.1 s for `seconds`, each closed again: the errno
        names of the refused ones (an open listener accepts each into its backlog; a closed one refuses)."""
        deadline = time.monotonic() + seconds
        refused = []
        while time.monotonic() < deadline:
            conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            here = os.getcwd()
            os.chdir(sock.parent)
            try:
                conn.connect(sock.name)
            except OSError as exc:
                refused.append(errno.errorcode.get(exc.errno, str(exc)))
            finally:
                os.chdir(here)
                conn.close()
            time.sleep(0.1)
        return refused

    def test_a_signal_between_the_flag_check_and_the_readiness_line_is_delivered_after_the_line_with_the_listener_open(
        self,
    ):
        """U447b (verdict U447-a52a1452 P1 `acp-relay.py:252`): at a52a1452 a signal between the stop-flag check and
        the print ran on_signal at once, which closed the listener, and the line was still printed, so a readiness
        line followed the listener's closure. The relay blocks HUP, INT and TERM across the flag's read, the print
        and the flush: the line is printed only in a state where no signal was handled, and a signal sent meanwhile
        is delivered after the flush and ends the relay as any post-readiness signal does. Measured from the outside
        with a scratch copy of the relay holding one `/bin/sleep 3` right after the flag check and before the print
        (the copy differs from the source by that line alone, asserted with difflib; pinned in the scratch manifest):
        a HUP, INT or TERM to the broker while the sleep runs under the relay, then probe connections for 1 s inside
        the window: every probe is accepted (the listener is open until the line is printed), the line is printed
        once, the broker ends by the signal with nothing on stderr, the socket gone and the directory standing empty.
        At a52a1452 the probes are refused (the handler closed the listener during the sleep) while the line follows:
        red."""
        broker, _helper = self.scratch_checkout()
        relay = broker.parent / "acp-relay.py"
        source = relay.read_text()
        lines = source.splitlines(keepends=True)
        at = [i for i, line in enumerate(lines) if line.strip() == "if not self.stopping:"]
        self.assertEqual(len(at), 1, "the one flag check before the readiness line")
        check = lines[at[0]]
        injected = check[: len(check) - len(check.lstrip())] + '    subprocess.run(["/bin/sleep", "3"], check=False)\n'
        lines.insert(at[0] + 1, injected)
        relay.write_text("".join(lines))
        changed = [
            line
            for line in difflib.unified_diff(source.splitlines(), relay.read_text().splitlines(), lineterm="", n=0)
            if line[:1] in "+-" and line[:3] not in ("+++", "---")
        ]
        self.assertEqual(changed, ["+" + injected.rstrip("\n")], "the copy differs from the source by that one line")
        self.pin_lever(broker, relay)
        for n, sig in enumerate((signal.SIGHUP, signal.SIGINT, signal.SIGTERM), start=1):
            with self.subTest(signal=sig.name):
                name, cwd = self.make_router(f"router-20261111-00001{n}-1")
                proc, sock = self.launch_broker(name, cwd, broker=broker)
                self.wait_for(lambda: sock.exists() or proc.poll() is not None, "the socket's bind", seconds=60)
                if proc.poll() is not None:
                    out, err = proc.communicate()
                    self.fail(f"the broker ended before the bind: {proc.returncode} {out!r} {err!r}")
                pid = self.relay_pid(proc)
                self.assertIsNotNone(pid, "the relay runs under the broker once the socket exists")
                self.wait_for(lambda: self.sleeping_child(pid, 3), "the injected sleep under the relay", seconds=30)
                proc.send_signal(sig)
                refused = self.probe_connections(sock, 1.0)
                self.assertEqual(refused, [], "the listener accepts throughout the window: it closes after the line")
                self.wait_for(lambda: proc.poll() is not None, "the broker's end by the signal", seconds=60)
                status, out, err = self.stop_broker(proc, sig)
                self.assertEqual(status, -sig, err)
                self.assertEqual(out, f"acp-broker: listening on {sock}\n", "the line once, before the signal's end")
                self.assertEqual(err, "", "nothing refused and nothing remained")
                self.assert_broker_dir_stands_empty(sock)

    def relay_pid_by_socket(self, sock):
        """The relay's pid found by the socket path in its argv (`pgrep -f`): the relay alone names the socket, the
        broker's argv names the Router and a connection names no socket; None when none or several run. For the
        window where the broker has two children (the relay and an injected sleep), where relay_pid cannot tell."""
        run = subprocess.run(["pgrep", "-f", str(sock)], capture_output=True, text=True, check=False)
        pids = run.stdout.split()
        return int(pids[0]) if len(pids) == 1 else None

    def end_orphan(self, pid):
        """End a relay a red run left behind (TERM, so it removes its socket; KILL when it stays), so the scratch is
        removable and no process outlives the test."""
        if pid is None or not self.alive(pid):
            return
        os.kill(pid, signal.SIGTERM)
        deadline = time.monotonic() + 10
        while self.alive(pid) and time.monotonic() < deadline:
            time.sleep(0.05)
        if self.alive(pid):
            os.kill(pid, signal.SIGKILL)

    def test_a_signal_during_the_relays_fork_is_deferred_until_the_child_is_known_and_leaves_no_relay_and_no_socket(
        self,
    ):
        """U447c (verdict U447-669dee44 P1 `acp-broker:1280`, class handler-window): bash runs a trap right after the
        simple command the signal arrived in, so a HUP, INT or TERM between the relay's `&` and `child=$!` ran
        broker_signal with `child` empty: nothing was signalled or waited for, broker_cleanup read the socket the
        orphaned relay had bound as another broker's, and the broker exited 2 with the relay alive and the socket
        standing. Bash cannot block a signal, so the window is closed by deferral: `forking=1` before the `&`, cleared
        after `child=$!`; while it is set the handler records the signal and returns, and the recorded signal is
        handled right after the flag is cleared, with the child known. Measured with a scratch copy of the lever
        holding one `/bin/sleep 1` right after the relay's `&` line and before `child=$!` (the copy differs from the
        source by that line alone, asserted with difflib; pinned in the scratch manifest): a HUP, INT or TERM to the
        broker once that sleep runs as its child (the window; the relay runs free meanwhile, so the socket may or may
        not exist at that instant) ends the broker by that signal with nothing on stderr, at most the readiness line
        on stdout, no relay process left (found by the socket path in its argv) and the socket gone, the directory
        standing empty. At 669dee44 the same copy of that head's lever exits 2 naming the standing socket, with the
        relay alive: red."""
        broker, _helper = self.scratch_checkout()
        source = BROKER.read_text()
        lines = source.splitlines(keepends=True)
        fork_tail = ' --connection "${seats_root}" "${router}" "${scratch}" &\n'
        at = [i for i, line in enumerate(lines) if line.endswith(fork_tail)]
        self.assertEqual(len(at), 1, f"the one line the sleep follows: the relay's fork, ending {fork_tail!r}")
        self.assertEqual(lines[at[0] + 1].strip(), "child=$!", "the sleep sits before `child=$!`")
        injected = lines[at[0] + 1][: len(lines[at[0] + 1]) - len(lines[at[0] + 1].lstrip())] + "/bin/sleep 1\n"
        lines.insert(at[0] + 1, injected)
        broker.write_text("".join(lines))
        changed = [
            line
            for line in difflib.unified_diff(source.splitlines(), broker.read_text().splitlines(), lineterm="", n=0)
            if line[:1] in "+-" and line[:3] not in ("+++", "---")
        ]
        self.assertEqual(changed, ["+" + injected.rstrip("\n")], "the copy differs from the source by that one line")
        self.pin_lever(broker, broker)
        for n, sig in enumerate((signal.SIGHUP, signal.SIGINT, signal.SIGTERM), start=1):
            with self.subTest(signal=sig.name):
                name, cwd = self.make_router(f"router-20261111-00003{n}-1")
                proc, sock = self.launch_broker(name, cwd, broker=broker)
                self.wait_for(
                    lambda: self.sleeping_child(proc.pid) or proc.poll() is not None,
                    "the injected sleep under the broker, between the relay's fork and `child=$!`",
                    seconds=60,
                )
                if proc.poll() is not None:
                    out, err = proc.communicate()
                    self.fail(f"the broker ended before the fork window: {proc.returncode} {out!r} {err!r}")
                relay = self.relay_pid_by_socket(sock)
                self.addCleanup(self.end_orphan, relay)
                self.assertIsNotNone(relay, "the relay runs under the broker during the window")
                proc.send_signal(sig)
                self.wait_for(lambda: proc.poll() is not None, "the broker's end by the signal", seconds=60)
                # The relay's state at the broker's end is the observable; an orphan (a red run) holds the broker's
                # stdout pipe open, so it is ended before the pipe is read to EOF, and the socket it stood on is noted.
                orphaned, socket_stood = self.alive(relay), sock.exists()
                self.end_orphan(relay)
                status, out, err = self.stop_broker(proc, sig)
                self.assertEqual(status, -sig, err)
                self.assertEqual(err, "", "nothing refused and nothing remained")
                self.assertIn(out, ("", f"acp-broker: listening on {sock}\n"), "at most the readiness line")
                self.assertFalse(orphaned, f"the relay {relay} ended with the broker, not orphaned")
                self.assertFalse(socket_stood, "the socket is gone at the broker's end")
                self.assertIsNone(self.relay_pid_by_socket(sock), "no process names the socket any more")
                self.assert_broker_dir_stands_empty(sock)

    def test_a_readiness_fragment_without_a_newline_fails_start_broker_by_its_deadline_rather_than_hanging(self):
        """U447b (verdict U447-a52a1452 P2 `test_acp_broker.py:366`): at a52a1452 start_broker waited with `select`
        and then `readline`, so a fragment without a newline satisfied the select and the readline blocked past the
        60 s deadline, until the broker's EOF. The reader gathers bytes chunk by chunk, each wait bounded by what
        remains of the deadline. A fake broker printing `acp-broker: listen` with no newline and then sleeping:
        start_broker, run in a thread, fails by its deadline within 60 s plus a margin, naming the fragment; at
        a52a1452 the thread is still inside readline at the ceiling: red."""
        fake = Path(self.temp.name).resolve() / "fake-acp-broker"
        fake.write_text("#!/bin/bash\nprintf 'acp-broker: listen'\nexec /bin/sleep 600\n")
        fake.chmod(0o755)
        name, cwd = self.make_router("router-20261111-000020-1")
        outcome = {}

        def run():
            started = time.monotonic()
            try:
                self.start_broker(name, cwd, broker=fake)
            except Exception as exc:  # the failure is the thread's result, judged below
                outcome["error"] = exc
            outcome["elapsed"] = time.monotonic() - started

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        thread.join(timeout=75)
        if thread.is_alive():
            self.fail(
                "start_broker did not return within 75 s on a readiness fragment without a newline: "
                "it hangs past its 60 s deadline"
            )
        error = outcome.get("error")
        self.assertIsInstance(error, AssertionError, f"start_broker failed by its deadline: {error!r}")
        self.assertIn("did not print its readiness line within 60 s", str(error))
        self.assertIn("acp-broker: listen", str(error), "the fragment that arrived is named")
        self.assertLess(outcome["elapsed"], 70, "the deadline ended the wait, not a later EOF")

    def broker_refusal(self, name, cwd):
        """The broker started for a refusal: `(status, stdout, stderr)` once it has exited. One that listens instead
        (a red run, where the lever takes a directory it should refuse) is ended by TERM and fails the test."""
        proc = subprocess.Popen(
            [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )  # fmt: skip
        try:
            out, err = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            proc.send_signal(signal.SIGTERM)
            out, err = proc.communicate(timeout=60)
            self.fail(f"the broker listened instead of refusing; ended by TERM: {proc.returncode} {out!r} {err!r}")
        return proc.returncode, out, err

    def test_a_second_broker_on_the_same_slot_refuses(self):
        """While a broker listens for a Router, a second one for the same slot refuses by name and touches nothing
        (verdict U343d-136fbe0a P2 `:854`: a loser never removes a winner's socket); after the first ends, the
        directory stands empty and a new broker takes it (U343i); a directory holding any entry (a crashed broker's
        leftovers) refuses by name and is left in place, and an absent one refuses naming hcom-seat, which makes it."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        run = subprocess.run(
            [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(),
            capture_output=True, text=True, check=False, timeout=60,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"acp-broker: refused: a broker already listens for the Router {name} ({sock} exists)", run.stderr
        )
        self.assertTrue(sock.exists(), "the first broker's socket stays")
        self.assertIsNone(proc.poll())
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)
        self.assert_broker_dir_stands_empty(sock)
        # A directory with an entry (a crashed broker's, or another's between its take and its bind) refuses and stays.
        (sock.parent / "note").write_text("x\n")
        status, out, err = self.broker_refusal(name, cwd)
        self.assertEqual((status, out), (2, ""), err)
        self.assertIn(f"acp-broker: refused: the broker directory {sock.parent} is not empty (note)", err)
        self.assertTrue((sock.parent / "note").exists(), "the refusing broker removed nothing")
        sock.parent.joinpath("note").unlink()
        # Absent: the broker makes nothing and names the lever that does.
        sock.parent.rmdir()
        status, out, err = self.broker_refusal(name, cwd)
        self.assertEqual((status, out), (2, ""), err)
        self.assertIn(f"acp-broker: refused: the broker directory {sock.parent} is absent; hcom-seat", err)
        self.assertFalse(sock.parent.exists() or sock.parent.is_symlink(), "the broker made no directory")
        # Made again as hcom-seat makes it, a new broker takes the slot.
        sock.parent.mkdir(mode=0o700)
        proc, sock = self.start_broker(name, cwd)
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)
        self.assert_broker_dir_stands_empty(sock)

    def test_b_the_listener_takes_the_directory_hcom_seat_made_and_refuses_any_other_state(self):
        """U343i test (b) (verdict U343h-eb648bcd P1 `acp-relay.py:284` and `acp-broker:963`, class record-path; the
        mechanism-change row of 2026-11-10T06:20:28Z, form remove): the broker directory is hcom-seat's, made 0700
        before the Router's settings are written and denied to the Router for write by them, so the listener makes
        nothing there and takes the directory as it finds it: no link, a directory of this user, mode 0700, empty.
        Absent, it refuses naming hcom-seat; a link (to an empty directory elsewhere, nothing made through it), a
        regular file, an entry inside (a dot name included) or another mode each refuse by name, exit 2, with nothing
        made and no srt run; present and empty, it listens, and at its end the socket and every record (a raw
        connection's, never read) are gone and the directory stands, 0700 and empty, for the next broker of the
        launch."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        broker_dir = self.seats_path / ".state" / name / "broker"
        elsewhere = Path(self.temp.name).resolve() / "elsewhere"
        elsewhere.mkdir(mode=0o700)

        def run():
            return self.broker_refusal(name, cwd)

        def reset():
            if broker_dir.is_symlink() or broker_dir.is_file():
                broker_dir.unlink()
            elif broker_dir.is_dir():
                broker_dir.chmod(0o700)
                for entry in broker_dir.iterdir():
                    entry.unlink()
                broker_dir.rmdir()
            broker_dir.mkdir(mode=0o700)

        cases = (
            ("absent", broker_dir.rmdir,
             f"the broker directory {broker_dir} is absent; hcom-seat's router launch makes it (0700) before the"
             " Router's settings are written, and this lever makes nothing there"),
            ("a link to a directory", lambda: (broker_dir.rmdir(), broker_dir.symlink_to(elsewhere)),
             f"the broker directory {broker_dir} is a symbolic link; it must be a real directory"),
            ("a regular file", lambda: (broker_dir.rmdir(), broker_dir.write_text("")),
             f"the broker directory {broker_dir} is not a directory"),
            ("an entry inside", lambda: (broker_dir / "note").write_text("x\n"),
             f"the broker directory {broker_dir} is not empty (note)"),
            ("a dot entry inside", lambda: (broker_dir / ".hidden").write_text(""),
             f"the broker directory {broker_dir} is not empty (.hidden)"),
            ("mode 0755", lambda: broker_dir.chmod(0o755),
             f"the broker directory {broker_dir} has mode 755, not 0700 (hcom-seat makes it 0700)"),
        )  # fmt: skip
        for label, arrange, message in cases:
            with self.subTest(case=label):
                reset()
                arrange()
                status, out, err = run()
                self.assertEqual((status, out), (2, ""), err)
                self.assertIn(f"acp-broker: refused: {message}", err)
                self.assertEqual(self.calls_of("srt"), [], "nothing ran")
                self.assertFalse((self.seats_path / ".state" / name / "broker" / "sock").exists(), "no socket")
        self.assertEqual(sorted(elsewhere.iterdir()), [], "nothing made through the link")
        reset()
        self.assertEqual(sorted(broker_dir.iterdir()), [])
        proc, sock = self.start_broker(name, cwd)
        self.assertEqual(sock.parent, broker_dir)
        self.assertEqual(stat.S_IMODE(os.lstat(sock).st_mode), 0o600)
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        (record,) = [p.name for p in broker_dir.iterdir() if p.name != "sock"]
        self.assertTrue(record.startswith("acp-w1-"), record)
        status, out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertEqual(out, f"acp-broker: listening on {sock}\n")
        self.assertNotIn("cannot remove", err)
        self.assert_broker_dir_stands_empty(sock)
        proc, sock = self.start_broker(name, cwd)
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)
        self.assert_broker_dir_stands_empty(sock)

    # --- U343j, round 8: the bind decides between two brokers, and the take's emptiness is read by a glob ---

    def plant_bind_winner(self):
        """The fake python3 on PATH becomes the `#!/bin/sh` wrapper that, for the relay's start alone, first binds
        the broker socket from a listener of the test's (the winner: a broker that bound first, with one record no
        client read and one reaper temporary beside its socket) and then runs the real relay, whose bind fails as the
        loser's does; returns the names of the winner's two records."""
        winner = self.bindir / "bind-winner.py"
        # The fakes' `#!/usr/bin/env python3` would now resolve to the wrapper, a script the broker refuses as an
        # interpreter, so they name the real interpreter by its absolute path for these tests.
        for tool in ("srt", "omp"):
            path = self.bindir / tool
            path.write_text(path.read_text().replace("#!/usr/bin/env python3\n", f"#!{self.python}\n", 1))
        winner.write_text(BIND_WINNER)
        fake = self.bindir / "python3"
        fake.unlink()
        fake.write_text(FAKE_PYTHON3.format(python=self.python, calls=self.calls, winner=winner))
        fake.chmod(0o755)
        (self.calls / "bind-loser").write_text("")
        self.addCleanup(self.kill_winner)
        return ["acp-w9-20260101-000000-1", "acp-w9-20260101-000000-1.tmp"]

    def kill_winner(self):
        pid_file = self.calls / "winner-pid"
        if pid_file.exists():
            try:
                os.kill(int(pid_file.read_text()), signal.SIGKILL)
            except (ProcessLookupError, ValueError):
                pass

    def losing_broker(self, name, cwd):
        """The broker started on a slot whose relay loses the bind: `(status, stdout, stderr)` once it has exited."""
        proc = subprocess.Popen(
            [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )  # fmt: skip
        try:
            out, err = proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
            self.fail(f"the losing broker did not exit: {out!r} {err!r}")
        return proc.returncode, out, err

    def connect_raw(self, sock):
        """One raw connection to `sock` by its name from its directory, no header; what came back."""
        conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        conn.settimeout(30)
        here = os.getcwd()
        os.chdir(sock.parent)
        try:
            conn.connect(sock.name)
        finally:
            os.chdir(here)
        return self.recv_all(conn)

    def test_a_a_broker_whose_relay_loses_the_bind_removes_nothing_and_leaves_the_winners_socket_standing(self):
        """U343j test (a) (verdict U343i-76a5c83b P1 `acp-broker:1061`): the take is a check before the bind, so two
        brokers started together can both pass it and the bind decides; the relay that loses it refuses `cannot bind
        the broker socket` and exits 2, and the loser's broker, whose cleanup used to `rm -f` the socket whatever
        bound it, removes nothing when the socket stands after its relay's end: the winner's socket (bound here by a
        listener of the test's right before the real relay runs) stands, 0600, and still accepts; the loser exits 2
        with one line naming the socket and the relay's status, nothing on stdout, no `cannot remove` line."""
        name, cwd = self.make_router()
        self.plant_bind_winner()
        sock = self.seats_path / ".state" / name / "broker/sock"
        status, out, err = self.losing_broker(name, cwd)
        self.assertEqual((status, out), (2, ""), err)
        self.assertIn(f"acp-relay.py: refused: cannot bind the broker socket {sock}", err)
        self.assertIn(f"acp-broker: the socket {sock} stands after the relay's end", err)
        self.assertIn(
            "acp-broker: the relay exited 2; the broker exits 2 because the socket stands and nothing was removed", err
        )
        self.assertNotIn("cannot remove", err)
        self.assertTrue(sock.exists(), "the winner's socket stands")
        self.assertEqual(stat.S_IMODE(os.lstat(sock).st_mode), 0o600)
        self.assertTrue(self.alive(int((self.calls / "winner-pid").read_text())), "the winner runs")
        self.assertEqual(self.connect_raw(sock), b"winner\n", "the winner still listens on its socket")

    def test_b_an_entry_named_by_a_newline_alone_refuses_the_take_as_not_empty(self):
        """U343j test (b) (verdict U343i-76a5c83b P2 `acp-broker:1062`): the take read the entries through
        `$(/bin/ls -A …)`, and command substitution strips trailing newlines, so an entry named by one newline alone
        read as an empty directory and the broker listened beside it, and a name ending in a newline lost its last
        character; the emptiness is now a glob (dot names included, no match an empty list), so an entry of any name
        refuses, shown `%q`-quoted in the refusal, and stays in place with no socket beside it and no srt run."""
        name, cwd = self.make_router()
        broker_dir = self.seats_path / ".state" / name / "broker"
        cases = (("a newline alone", "\n", "$'\\n'"), ("a name ending in a newline", "note\n", "$'note\\n'"))
        for label, entry, shown in cases:
            with self.subTest(case=label):
                (broker_dir / entry).write_text("")
                status, out, err = self.broker_refusal(name, cwd)
                self.assertEqual((status, out), (2, ""), err)
                self.assertIn(
                    f"acp-broker: refused: the broker directory {broker_dir} is not empty ({shown}); hcom-seat makes"
                    " it empty",
                    err,
                )
                self.assertEqual(sorted(p.name for p in broker_dir.iterdir()), [entry], "the entry stays, no socket")
                self.assertEqual(self.calls_of("srt"), [], "nothing ran")
                (broker_dir / entry).unlink()

    def test_c_a_broker_whose_relay_loses_the_bind_leaves_the_winners_records_standing(self):
        """U343j test (c): the records beside a standing socket are the winner's (a connection's exit report no client
        read yet, and a reaper's temporary in flight), so the loser's cleanup, which used to sweep `acp-*` before it
        looked at the socket, leaves them: after the loser's exit the directory holds exactly the winner's socket and
        its two records, the record's bytes unchanged."""
        name, cwd = self.make_router()
        names = self.plant_bind_winner()
        sock = self.seats_path / ".state" / name / "broker/sock"
        status, out, err = self.losing_broker(name, cwd)
        self.assertEqual((status, out), (2, ""), err)
        self.assertNotIn("cannot remove", err)
        self.assertEqual(self.broker_dir_entries(sock), sorted([*names, "sock"]))
        self.assertEqual((sock.parent / names[0]).read_text(), "ref=refs/acp-seat/w9/20260101-000000-1\nreaper=1\n")
        self.assertEqual((sock.parent / names[1]).read_text(), "")

    def test_the_client_refuses_outside_a_seat_on_a_refusal_line_and_without_a_socket(self):
        """acp-seat: exit 2 with nothing on stdout outside a seat (no marker), on the broker's refusal line (printed on
        stderr), on a socket it cannot connect to, and on a malformed option set; the four never reach omp."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        run = self.client(sock, repo, "w1", PING, HCOM_SEAT_SANDBOX=None)
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-seat: refused: refused outside a seat (HCOM_SEAT_SANDBOX is unset)", run.stderr)
        run = self.client(sock, cwd / "nowhere", "w1", PING)
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-broker: refused: cannot resolve the ref 'HEAD' in the repository", run.stderr)
        run = self.client(sock, repo, "W1", PING)
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-seat: refused: the name 'W1' is outside", run.stderr)
        run = self.client(sock, repo, "w1", PING, ref="-x")
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-seat: refused: the ref '-x' is outside", run.stderr)
        run = self.client(sock.parent / "nowhere", repo, "w1", PING)
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-seat: refused: cannot connect to the broker socket", run.stderr)
        run = subprocess.run(
            [str(CLIENT), "--socket", str(sock), "--repo", str(repo), "--ref", "HEAD"], input=PING,
            env=self.broker_env(HCOM_SEAT_SANDBOX="x"), capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"usage: acp-seat --socket <path> --name <name> [--repo <path>] [--ref <rev>]", run.stderr)
        run = subprocess.run(
            [str(CLIENT), "--socket", str(sock), "--cwd", str(repo), "--ref", "HEAD", "--name", "w1"], input=PING,
            env=self.broker_env(HCOM_SEAT_SANDBOX="x"), capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertEqual(self.calls_of("omp"), [])
        # The exit status is the record's, and nothing of the broker's reaches stdout after the first line.
        (self.calls / "omp-status").write_text("9")
        run = self.client(sock, repo, "w1", PING)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (9, PING, b"acp-seat: push=none\n"))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def client_against_stream(self, stream, record=None):
        """The client run against a scratch server in the broker's place that answers the header with `stream` and
        closes, with the record `record` (name, text) planted in the socket's directory when given; the completed
        run, with `record_left` set to whether the planted record is still there."""
        sock = Path(self.temp.name).resolve() / "s" / "sock"
        sock.parent.mkdir(exist_ok=True)
        if record is not None:
            (sock.parent / record[0]).write_text(record[1])
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        here = os.getcwd()
        os.chdir(sock.parent)
        try:
            server.bind(sock.name)
        finally:
            os.chdir(here)
        server.listen(1)

        def serve():
            conn, _ = server.accept()
            conn.recv(4096)  # the header
            conn.sendall(stream)
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass  # the client has already closed its side
            conn.close()

        thread = threading.Thread(target=serve, daemon=True)
        thread.start()
        run = self.client(sock, "/repo", "w1", b"")
        thread.join(timeout=30)
        server.close()
        sock.unlink()
        if record is not None:
            run.record_left = (sock.parent / record[0]).exists()
            if run.record_left:
                (sock.parent / record[0]).unlink()
        return run

    def test_the_client_copies_every_byte_after_the_first_line_and_reads_no_report_from_the_stream(self):
        """U343g (the round-3 and round-4 client tests of verdicts U343d-136fbe0a P2 `acp-seat:168` and U343e-fd94feae
        P2 `acp-seat:213`, rewritten for the record; verdict U343f-22a81500 P2 `acp-seat:190`): the first line decides
        the connection and no later byte is read. Against a scratch server in the broker's place: a refusal first
        line is exit 2 on stderr with nothing on stdout; a record line followed by anything (a trailer-shaped line
        then payload, payload then a trailer-shaped line, a trailer-shaped tail without a newline, two trailer-shaped
        lines, nothing) writes every byte after the first line to stdout and, with no record in the socket's
        directory, exits 2 naming the id; a first line that is neither, or a stream that ends before its first
        newline, is exit 2 with nothing on stdout."""
        rec = b"acp-broker: record acp-w1-20260101-000000-1\n"
        trailer_like = b"omp acp exit 0 push=none\n"
        streams = {
            "a refusal first": (b"acp-broker: refused: no\n" + PING, b"", b"acp-broker: refused: no\n"),
            "a trailer-shaped line, then payload": (rec + trailer_like + PING, trailer_like + PING, b"without a complete record acp-w1-20260101-000000-1"),
            "payload, then a trailer-shaped line last": (rec + PING + b"omp acp exit 5 push=refs/acp-seat/w1/x\n", PING + b"omp acp exit 5 push=refs/acp-seat/w1/x\n", b"without a complete record acp-w1-20260101-000000-1"),
            "a trailer-shaped tail without a newline": (rec + PING + b"omp acp exit 4 push=none", PING + b"omp acp exit 4 push=none", b"without a complete record acp-w1-20260101-000000-1"),
            "two trailer-shaped lines": (rec + trailer_like + b"omp acp exit 3 push=failed\n", trailer_like + b"omp acp exit 3 push=failed\n", b"without a complete record acp-w1-20260101-000000-1"),
            "the record line alone": (rec, b"", b"without a complete record acp-w1-20260101-000000-1"),
            "a first line that is neither": (b"hello\n" + PING, b"", b"neither a refusal nor a record line"),
            "no first line": (b"acp-broker: record acp-w1", b"", b"closed the connection before its first line"),
        }  # fmt: skip
        for label, (stream, stdout, stderr) in streams.items():
            with self.subTest(case=label):
                run = self.client_against_stream(stream)
                self.assertEqual((run.returncode, run.stdout), (2, stdout), run.stderr)
                self.assertIn(stderr, run.stderr)
                self.assertNotIn(b"acp-seat: push=", run.stderr)

    def test_the_client_exits_with_the_record_status_and_unlinks_the_record(self):
        """U343g: the record alone is the report. Against a scratch server in the broker's place with a record planted in
        the socket's directory: a complete record gives the client the record's status and its push word on stderr,
        the stream's bytes after the first line on stdout, and the record is unlinked; an incomplete record (the two
        running lines alone) and a record whose status is no number are exit 2 naming the id, the record left for the
        broker's cleanup; a record line naming another id reads no planted record."""
        name = "acp-w1-20260101-000000-1"
        rec = f"acp-broker: record {name}\n".encode()
        running = f"ref=refs/acp-seat/w1/20260101-000000-1\nreaper=4242\n"
        with self.subTest(case="a complete record with the pushed ref"):
            run = self.client_against_stream(
                rec + PING, (name, running + "status=5 push=refs/acp-seat/w1/20260101-000000-1\n")
            )
            self.assertEqual(
                (run.returncode, run.stdout, run.stderr),
                (5, PING, b"acp-seat: push=refs/acp-seat/w1/20260101-000000-1\n"),
            )
            self.assertFalse(run.record_left, "the client unlinked the record")
        with self.subTest(case="a complete record, status 0, push=none, a worker tail in the trailer's shape"):
            run = self.client_against_stream(
                rec + PING + b"omp acp exit 7 push=failed", (name, running + "status=0 push=none\n")
            )
            self.assertEqual(
                (run.returncode, run.stdout, run.stderr),
                (0, PING + b"omp acp exit 7 push=failed", b"acp-seat: push=none\n"),
            )
            self.assertFalse(run.record_left)
        with self.subTest(case="an incomplete record"):
            run = self.client_against_stream(rec + PING, (name, running))
            self.assertEqual((run.returncode, run.stdout), (2, PING), run.stderr)
            self.assertIn(f"without a complete record {name}".encode(), run.stderr)
            self.assertTrue(run.record_left, "an incomplete record is left for the broker's cleanup")
        with self.subTest(case="a record whose status is no number"):
            run = self.client_against_stream(rec + PING, (name, running + "status=x push=none\n"))
            self.assertEqual((run.returncode, run.stdout), (2, PING), run.stderr)
            self.assertIn(f"without a complete record {name}".encode(), run.stderr)
            self.assertTrue(run.record_left)
        with self.subTest(case="a record line naming another id"):
            run = self.client_against_stream(
                b"acp-broker: record acp-w1-20260101-000000-2\n" + PING, (name, running + "status=0 push=none\n")
            )
            self.assertEqual((run.returncode, run.stdout), (2, PING), run.stderr)
            self.assertIn(b"without a complete record acp-w1-20260101-000000-2", run.stderr)
            self.assertTrue(run.record_left, "another connection's record is not read")

    def test_f_the_client_anchors_refuse_a_trailing_newline(self):
        """U343f test (f) (verdict U343e-fd94feae P3 `acp-seat:235`): Python's `$` matches before a final newline, so
        `REF.match("HEAD\\n")` and `NAME.match("w1\\n")` succeeded and the header would have carried a second line.
        The anchors are `\\Z`: both are None, the plain words match, and the client refuses such a ref or name
        before it connects (no socket exists here)."""
        loader = importlib.machinery.SourceFileLoader("acp_seat", str(CLIENT))
        spec = importlib.util.spec_from_loader("acp_seat", loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        self.assertIsNone(module.REF.match("HEAD\n"))
        self.assertIsNone(module.NAME.match("w1\n"))
        self.assertIsNotNone(module.REF.match("HEAD"))
        self.assertIsNotNone(module.NAME.match("w1"))
        nowhere = Path(self.temp.name).resolve() / "nowhere" / "sock"
        run = self.client(nowhere, "/repo", "w1\n", PING)
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-seat: refused: the name 'w1\\n' is outside", run.stderr)
        run = self.client(nowhere, "/repo", "w1", PING, ref="HEAD\n")
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-seat: refused: the ref 'HEAD\\n' is outside", run.stderr)

    def test_every_producer_injection_refuses_by_name(self):
        """Each producer the launch reads fails in turn: the slot mkdir, a physical resolution, the Router settings
        read (a malformed file, an unclean row), the reaper's placement (a file size limit on the broker, which the
        record helper's copy hits before the settings write, U343o), the canary, srt's exit (the record and the log
        carry omp's status), the omp version read, the log append and, U344c (verdict U344-a8adad11 P2
        `test_acp_broker.py:2432`), the settings writer's two functions under the module's injection form (a scratch
        copy of the lever with one line inserted after the judgement, pinned so it runs): a row that is not clean
        reaching `seat_settings_rows_json`, and `seat_settings_json` failing. Each refuses with one line naming what
        failed, starts no omp, writes nothing and leaves no slot."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        state = self.seats_path / ".state"
        template = self.seats_path / ".sandbox" / name / "srt-settings.json"
        good = template.read_text()

        def refused(message, worker="w1"):
            data = self.recv_all(self.connect(sock, repo, worker)).decode()
            self.assertEqual(data.count("\n"), 1, data)
            self.assertIn("acp-broker: refused: " + message, data)
            self.assertEqual(self.acp_slots(), [])
            return data

        with self.subTest(producer="mkdir of the slot"):
            state.chmod(0o500)
            try:
                refused("cannot create the per-connection slot")
            finally:
                state.chmod(0o700)
            self.assertEqual(self.calls_of("srt"), [], "nothing ran")
        with self.subTest(producer="a physical resolution"):
            profile = self.home / ".omp/profiles/dsh"
            profile.parent.mkdir(parents=True)
            profile.symlink_to(profile)  # a link to itself never resolves
            try:
                refused(
                    f"cannot resolve the worker's omp profile {self.home_real}/.omp/profiles/dsh to a clean physical path"
                )
            finally:
                profile.unlink()
            self.assertEqual(self.calls_of("srt"), [], "nothing ran")
        with self.subTest(producer="the Router settings read, malformed"):
            try:
                template.write_text('{"filesystem": {"denyRead": [1, 2]}}\n')
                refused("filesystem.denyRead in the Router's settings")
                template.write_text("not json\n")
                refused(f"cannot read filesystem.denyRead from the Router's settings {template}")
            finally:
                template.write_text(good)
        with self.subTest(producer="the Router settings read, an unclean row"):
            try:
                bad = json.loads(good)
                bad["filesystem"]["denyWrite"].append(str(self.home_real / "a b"))
                template.write_text(json.dumps(bad, separators=(",", ":")) + "\n")
                refused(
                    f"filesystem.denyWrite in the Router's settings {template} holds '{self.home_real}/a b', not a clean absolute path"
                )
                bad = json.loads(good)
                bad["filesystem"]["denyRead"].append(f"{self.home_real}/x*")
                template.write_text(json.dumps(bad, separators=(",", ":")) + "\n")
                refused(
                    f"filesystem.denyRead in the Router's settings {template} holds '{self.home_real}/x*', not a clean absolute path"
                )
            finally:
                template.write_text(good)
            self.assertEqual(self.calls_of("srt"), [], "nothing ran")
        with self.subTest(producer="the canary"):
            (self.calls / "srt-fail").touch()
            try:
                refused("the sandbox canary did not run under")
            finally:
                (self.calls / "srt-fail").unlink()
            self.assertEqual(self.calls_of("omp"), [])
        with self.subTest(producer="the omp version read"):
            (self.calls / "omp-version-status").write_text("1")
            try:
                refused("cannot read the omp version (")
            finally:
                (self.calls / "omp-version-status").unlink()
            self.assertEqual([c["argv"] for c in self.calls_of("omp")], [["--version"]], "omp acp never started")
            self.assertEqual(len(self.log_lines("w1")), 1, "the canary line alone; no start line")
        with self.subTest(producer="the log append"):
            logs = state / "broker-logs"
            logs.chmod(0o500)
            try:
                refused(f"cannot append to the launch log {logs}/w2.log", worker="w2")
            finally:
                logs.chmod(0o700)
            self.assertEqual([c["argv"] for c in self.calls_of("omp")], [["--version"]], "omp acp never started")
            self.assertEqual(self.log_lines("w2"), [])
        with self.subTest(producer="srt's exit, as the record and the log"):
            (self.calls / "omp-status").write_text("5")
            try:
                self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=5 push=none"))
            finally:
                (self.calls / "omp-status").unlink()
            self.assertRegex(self.log_lines("w1")[-1], r" acp-broker: omp acp exit 5 push=none$")
            self.assertEqual(self.acp_slots(), [])
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)
        with self.subTest(producer="the reaper's placement, under a file size limit"):
            # A file size limit of 12 KiB on the broker (inherited by every handler and its reaper): above the
            # settings writer's private copy (8.2 KiB, which the listener and every handler make before anything
            # else, U344c) and the settings (8 KiB, the producer this limit reached until round 12), below the
            # record helper's private copy (13.3 KiB). The reaper is forked as soon as the slot exists (U343o),
            # before the settings write, and its first write is that copy, which fails with EFBIG: the reaper
            # removes the slot and writes no ready line, so the handler refuses with the ready line and the settings
            # are never written. SIGXFSZ is ignored so a write fails instead of ending the shell.
            limit = [
                sys.executable, "-c",
                (
                    "import os, resource, signal, sys\n"
                    "signal.signal(signal.SIGXFSZ, signal.SIG_IGN)\n"
                    "resource.setrlimit(resource.RLIMIT_FSIZE, (12288, 12288))\n"
                    "os.execv(sys.argv[1], sys.argv[1:])\n"
                ),
            ]  # fmt: skip
            proc, sock = self.start_broker(name, cwd, wrapper=limit)
            data = refused("the reaper (pid ")
            self.assertIn("did not report ready within 10 s; omp acp not started", data)
            status, _out, err = self.stop_broker(proc)
            self.assertEqual(status, -signal.SIGTERM, err)
            self.assertIn(f"acp-broker: cannot copy {ROOT}/scripts/orchestrator/acp-record-place.py into ", err)
            self.assertNotIn("seat-settings-render", err, "the settings writer's copies were made under the limit")
            self.assertNotIn("cannot write the worker settings", err, "the settings write was never reached")
        source = BROKER.read_text()
        anchor = (
            "# The four lists and the file's text through the one writer (seat-settings-render.sh, U344), each "
            "producer's status\n"
        )
        self.assertEqual(source.count(anchor), 1, "the one line the injection follows")
        cases = (
            (
                "a row that is not clean reaches seat_settings_rows_json",
                'deny_read+=("${h}/a b")\n',
                "cannot render the worker's denyRead list (seat_settings_rows_json failed)",
            ),
            (
                "seat_settings_json fails",
                "seat_settings_json() { return 1; }\n",
                "cannot render the worker settings text (seat_settings_json failed)",
            ),
        )
        for index, (label, injected, message) in enumerate(cases):
            with self.subTest(producer=label):
                broker, _helper = self.scratch_checkout(f"checkout-renderer-{index}")
                broker.write_text(source.replace(anchor, anchor + injected))
                self.pin_lever(broker, broker)
                srt_before, omp_before = len(self.calls_of("srt")), len(self.calls_of("omp"))
                log_before = self.log_lines("w1")
                proc, sock = self.start_broker(name, cwd, broker=broker)
                refused(message)
                self.assertEqual(list(state.glob("acp-*")), [], "no slot and no settings file were made")
                self.assertEqual(
                    (len(self.calls_of("srt")), len(self.calls_of("omp"))), (srt_before, omp_before), "nothing ran"
                )
                self.assertEqual(self.log_lines("w1"), log_before, "no canary line: the launch log gained nothing")
                self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_worker_settings_are_the_dsh_row_but_the_named_rows(self):
        """The byte-identical compare (U343 ACCEPTANCE 6): the Router's settings come from a real held `hcom-seat
        router` launch on the fixture, the dsh row's from a real held `hcom-seat dsh` launch, and the worker's from
        a broker connection against that Router. The worker's deny lists are the Router's byte for byte (the
        project-file rows re-rooted under the slot's task, the credential root appended to denyRead) and, the
        per-launch names and the cwd normalised, the dsh row's; the grant lists are the dsh row's minus its state slot
        (row 1) and DSH_HOME (row 3) with the slot's task as row 0; the network block is the dsh row's (no binding, no
        socket); everything else is byte-identical."""
        dsh_home = Path(self.temp.name).resolve() / "dsh-home"
        (dsh_home / "bin").mkdir(parents=True)
        (dsh_home / "bin/dsh").write_text(test_hcom_seat_dsh.FAKE_DSH.format(calls=str(self.calls)))
        (dsh_home / "bin/dsh").chmod(0o755)
        # The rendered overlay the dsh role's profile config is placed from (U310): main's hcom-seat refuses a dsh
        # launch without it, so the reference launch places the file test_hcom_seat_dsh.py's fixture writes (U343d).
        (self.profiles / "dsh.yml").write_text(test_hcom_seat_dsh.DSH_OVERLAY.format(extension=self.bridge))
        rendered = {}
        for role in ("dsh", "router"):
            (self.calls / "hold").touch()
            before = len(self.calls_of("dsh"))
            launch = subprocess.Popen(
                [str(test_hcom_seat.SEAT), role, "--seats-root", self.seats, "--home", str(dsh_home), "--", "--version"],
                cwd=self.repo, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )  # fmt: skip
            self.wait_for(
                lambda before=before, launch=launch: len(self.calls_of("dsh")) > before or launch.poll() is not None,
                f"the {role} launch",
            )
            if launch.poll() is not None:
                self.fail(f"the {role} launch ended early: {launch.communicate()}")
            (seat_name,) = [p.name for p in (self.seats_path / ".sandbox").iterdir() if p.name.startswith(role + "-")]
            settings_path = self.seats_path / ".sandbox" / seat_name / "srt-settings.json"
            if role == "router":
                # The broker the router launch started (U344), on the socket the Router's settings open: one
                # connection held open while the settings are read.
                scratch = self.seats_path / ".state" / seat_name / "cwd"
                repo, _base = self.make_repo(scratch / "repo")
                sock = self.seats_path / ".state" / seat_name / "broker/sock"
                self.assertTrue(sock.is_socket(), f"hcom-seat started the broker before dsh: {self.state_names()}")
                self.router = seat_name
                conn, slot, task = self.held_connection(sock, repo, "w1")
                rendered["worker"] = (self.seats_path / ".state" / slot / "settings.json").read_bytes()
                self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
                rendered["task"] = str(task)
                rendered["router_cwd"] = str(scratch)
            rendered[role] = settings_path.read_bytes()
            rendered[role + "_name"] = seat_name
            (self.calls / "release").touch()
            out, err = launch.communicate(timeout=120)
            (self.calls / "hold").unlink()
            (self.calls / "release").unlink()
            self.assertEqual((launch.returncode, out), (0, "0.2.1-rc.5\n"), err)
        dsh, router, worker = (json.loads(rendered[k]) for k in ("dsh", "router", "worker"))
        home = self.home_real
        task, router_cwd = rendered["task"], rendered["router_cwd"]
        dsh_cwd = str(self.seats_path / ".state" / rendered["dsh_name"] / "cwd")
        credentials = f"{dsh_home}/router-credentials"

        def reroot(row, old, new):
            return new + row[len(old) :] if row.startswith(old + "/") else row

        # The deny table: the Router's, byte for byte, but the re-rooted project-file rows and the credential root;
        # the Router's table holds the broker-directory row of U343i, which the worker carries as any Router deny.
        broker_row = str(self.seats_path.resolve() / ".state" / rendered["router_name"] / "broker")
        self.assertEqual(router["filesystem"]["denyWrite"].count(broker_row), 1, "the router row's broker deny")
        self.assertEqual(worker["filesystem"]["denyRead"], router["filesystem"]["denyRead"] + [credentials])
        self.assertEqual(
            worker["filesystem"]["denyWrite"], [reroot(r, router_cwd, task) for r in router["filesystem"]["denyWrite"]]
        )
        self.assertEqual(
            len([r for r in worker["filesystem"]["denyWrite"] if r.startswith(task + "/")]), len(PROJECT_FILES)
        )

        # And the dsh row's, once the per-launch names and the cwd are normalised: the one shape, rendered twice; the
        # one row the dsh row has not is the router row's broker deny (U343i).
        def normalised(settings, cwd, launch_name):
            text = json.dumps(settings, separators=(",", ":")).replace(cwd, "<cwd>").replace(launch_name, "<launch>")
            return json.loads(text)

        dsh_n = normalised(dsh, dsh_cwd, rendered["dsh_name"])
        worker_n = normalised(worker, task, rendered["router_name"])
        broker_n = str(self.seats_path.resolve() / ".state/<launch>/broker")
        self.assertEqual(worker_n["filesystem"]["denyWrite"].count(broker_n), 1)
        worker_deny_write = [r for r in worker_n["filesystem"]["denyWrite"] if r != broker_n]
        self.assertEqual(worker_n["filesystem"]["denyRead"], dsh_n["filesystem"]["denyRead"])
        self.assertEqual(
            json.dumps(worker_n["filesystem"]["denyRead"]).encode(),
            json.dumps(dsh_n["filesystem"]["denyRead"]).encode(),
            "byte-identical denyRead: the dsh row's credential-root deny is its last row, the broker's appended one",
        )
        self.assertEqual(worker["filesystem"]["denyRead"][-1], credentials)
        self.assertEqual(worker_deny_write, dsh_n["filesystem"]["denyWrite"])
        self.assertEqual(
            json.dumps(worker_deny_write).encode(),
            json.dumps(dsh_n["filesystem"]["denyWrite"]).encode(),
            "byte-identical deny tables but the broker row",
        )
        self.assertNotIn("/broker", json.dumps(dsh), "the dsh row has no broker row")
        # The grants: the dsh row's rows 0, 2, 4.. with the slot's task as row 0 (no state slot, no DSH_HOME), and the
        # seats' API key file last (U516; the dsh row carries the same row once U512 lands, so it is matched by value).
        dsh_read, dsh_write = dsh["filesystem"]["allowRead"], dsh["filesystem"]["allowWrite"]
        key_file = str(self.key_file)
        self.assertEqual(dsh_read[1], str(self.seats_path / ".state" / rendered["dsh_name"]))
        self.assertEqual(dsh_read[3], str(dsh_home))
        self.assertEqual(
            worker["filesystem"]["allowRead"],
            [task, dsh_read[2], *(r for r in dsh_read[4:] if r != key_file), key_file],
        )
        self.assertEqual(worker["filesystem"]["allowWrite"], [task, dsh_write[2], *dsh_write[4:]])
        self.assertEqual(worker["filesystem"]["allowRead"][1], str(self.seats_path / ".state/claude"))
        self.assertEqual(worker["filesystem"]["allowWrite"][2:4], [f"{home}/.omp/profiles/dsh", f"{home}/.omp/run"])
        # DSH_HOME reaches the worker's settings as the credential root alone (U343l): once in denyRead, once in
        # denyWrite (the Router's row, copied), and in no grant.
        self.assertEqual(json.dumps(worker).count(str(dsh_home)), 2, json.dumps(worker))
        self.assertEqual(worker["filesystem"]["denyRead"].count(credentials), 1)
        self.assertEqual(worker["filesystem"]["denyWrite"].count(credentials), 1)
        self.assertNotIn(credentials, worker["filesystem"]["allowRead"] + worker["filesystem"]["allowWrite"])
        self.assertEqual(router["filesystem"]["allowRead"][7], credentials, "the Router reads what the worker may not")
        self.assertNotIn(f"{dsh_home}/router-state", worker["filesystem"]["allowWrite"])
        self.assertNotIn(router_cwd, json.dumps(worker), "no Router-named path")
        # The network block and everything else: the dsh row's, byte for byte.
        self.assertEqual(worker["network"], dsh["network"])
        self.assertEqual(worker["network"]["allowLocalBinding"], False)
        self.assertEqual(worker["network"]["allowUnixSockets"], [])
        self.assertEqual(router["network"]["allowLocalBinding"], True)
        self.assertEqual({k: v for k, v in worker.items() if k not in ("filesystem", "network")},
                         {k: v for k, v in dsh.items() if k not in ("filesystem", "network")})  # fmt: skip
        # The file's own bytes: the same key order and the same shape as hcom-seat's, string values aside.
        shape = re.compile(rb'"[^"]*"')
        self.assertEqual(
            shape.sub(b'""', rendered["worker"]).replace(b'"",', b"").replace(b'""', b""),
            shape.sub(b'""', rendered["dsh"]).replace(b'"",', b"").replace(b'""', b""),
        )
        self.assertTrue(rendered["worker"].endswith(b"}\n"))
        self.assertEqual(self.acp_slots(), [])

    def test_one_settings_writer_renders_the_worker_and_the_dsh_row_byte_for_byte(self):
        """The shared-writer compare (U344, test c; the U343 compare above made byte-exact): the Router's settings come
        from a real held `hcom-seat router` launch on the fixture, which starts the broker itself (U344), the dsh row's
        from a real held `hcom-seat dsh` launch, and the worker's from a connection to that launch's broker. Both
        levers source `seat-settings-render.sh`, so the worker's file is, byte for byte, the dsh row's file with the
        worker's rows in the role's positions: the deny lists the Router's (the project-file rows re-rooted under the
        slot's task, the credential root last in denyRead, the router row's broker deny carried), the grant lists the
        dsh row's minus its state slot (row 1) and DSH_HOME (row 3) with the slot's task as row 0, the network block
        the dsh row's (no binding, no socket), and the shape canonical compact JSON so the three files re-serialise
        to themselves. The launch's broker is gone with its directory once the launch has returned."""
        dsh_home = Path(self.temp.name).resolve() / "dsh-home"
        (dsh_home / "bin").mkdir(parents=True)
        (dsh_home / "bin/dsh").write_text(test_hcom_seat_dsh.FAKE_DSH.format(calls=str(self.calls)))
        (dsh_home / "bin/dsh").chmod(0o755)
        (self.profiles / "dsh.yml").write_text(test_hcom_seat_dsh.DSH_OVERLAY.format(extension=self.bridge))
        rendered = {}
        for role in ("dsh", "router"):
            (self.calls / "hold").touch()
            before = len(self.calls_of("dsh"))
            launch = subprocess.Popen(
                [str(test_hcom_seat.SEAT), role, "--seats-root", self.seats, "--home", str(dsh_home), "--", "--version"],
                cwd=self.repo, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )  # fmt: skip
            self.wait_for(
                lambda before=before, launch=launch: len(self.calls_of("dsh")) > before or launch.poll() is not None,
                f"the {role} launch",
            )
            if launch.poll() is not None:
                self.fail(f"the {role} launch ended early: {launch.communicate()}")
            (seat_name,) = [p.name for p in (self.seats_path / ".sandbox").iterdir() if p.name.startswith(role + "-")]
            settings_path = self.seats_path / ".sandbox" / seat_name / "srt-settings.json"
            if role == "router":
                # The broker the launch started, on the socket the Router's settings open: one connection held open
                # while the worker's settings are read.
                scratch = self.seats_path / ".state" / seat_name / "cwd"
                repo, _base = self.make_repo(scratch / "repo")
                sock = self.seats_path / ".state" / seat_name / "broker/sock"
                self.assertTrue(sock.is_socket(), f"hcom-seat started the broker before dsh: {self.state_names()}")
                self.router = seat_name
                conn, slot, task = self.held_connection(sock, repo, "w1")
                rendered["worker"] = (self.seats_path / ".state" / slot / "settings.json").read_bytes()
                self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
                rendered["task"] = str(task)
                rendered["router_cwd"] = str(scratch)
            rendered[role] = settings_path.read_bytes()
            rendered[role + "_name"] = seat_name
            (self.calls / "release").touch()
            out, err = launch.communicate(timeout=120)
            (self.calls / "hold").unlink()
            (self.calls / "release").unlink()
            self.assertEqual((launch.returncode, out), (0, "0.2.1-rc.5\n"), err)
            if role == "router":
                self.assertIn(f"acp-broker: listening on {sock}", err)
                self.assertFalse(sock.parent.exists(), "the launch stopped its broker and its slot took the directory")
        dsh, router, worker = (json.loads(rendered[k]) for k in ("dsh", "router", "worker"))
        task, router_cwd = rendered["task"], rendered["router_cwd"]
        dsh_cwd = str(self.seats_path / ".state" / rendered["dsh_name"] / "cwd")
        credentials = f"{dsh_home}/router-credentials"

        def canonical(settings):
            return json.dumps(settings, separators=(",", ":")).encode() + b"\n"

        # The writer renders canonical compact JSON: each file re-serialises to its own bytes.
        for key in ("dsh", "router", "worker"):
            self.assertEqual(canonical(json.loads(rendered[key])), rendered[key], key)

        def normalised(settings, cwd, launch_name):
            text = json.dumps(settings, separators=(",", ":")).replace(cwd, "<cwd>").replace(launch_name, "<launch>")
            return json.loads(text)

        dsh_n = normalised(dsh, dsh_cwd, rendered["dsh_name"])
        worker_n = normalised(worker, task, rendered["router_name"])
        broker_n = str(self.seats_path.resolve() / ".state/<launch>/broker")
        # The deny table: the dsh row's, byte for byte, but the router row's broker deny the worker carries (U343i).
        self.assertEqual(worker_n["filesystem"]["denyRead"], dsh_n["filesystem"]["denyRead"])
        self.assertEqual(worker_n["filesystem"]["denyRead"][-1], credentials)
        self.assertEqual(worker_n["filesystem"]["denyWrite"].count(broker_n), 1)
        self.assertEqual(
            [r for r in worker_n["filesystem"]["denyWrite"] if r != broker_n], dsh_n["filesystem"]["denyWrite"]
        )
        self.assertNotIn(router_cwd, json.dumps(worker), "no Router-named path")
        # The whole file, byte for byte: the dsh row's file with the worker's rows in the role's positions (the slot's
        # task as row 0, no state slot, no DSH_HOME, the broker deny where the Router renders it) and nothing else.
        dsh_read, dsh_write = dsh["filesystem"]["allowRead"], dsh["filesystem"]["allowWrite"]
        self.assertEqual(dsh_read[1], str(self.seats_path / ".state" / rendered["dsh_name"]))
        self.assertEqual(dsh_read[3], str(dsh_home))
        expected = normalised(dsh, dsh_cwd, rendered["dsh_name"])
        expected["filesystem"]["denyWrite"] = worker_n["filesystem"]["denyWrite"]
        key_file = str(self.key_file)
        expected["filesystem"]["allowRead"] = [task, dsh_read[2], *(r for r in dsh_read[4:] if r != key_file), key_file]
        expected["filesystem"]["allowWrite"] = [task, dsh_write[2], *dsh_write[4:]]
        expected_text = (
            json.dumps(expected, separators=(",", ":"))
            .replace("<cwd>", task)
            .replace("<launch>", rendered["router_name"])
        )
        self.assertEqual(rendered["worker"], expected_text.encode() + b"\n", "one writer, two renderings")
        self.assertEqual(worker["network"], dsh["network"])
        self.assertEqual(worker["network"]["allowUnixSockets"], [])
        self.assertEqual(router["network"]["allowLocalBinding"], True)
        self.assertEqual(
            router["network"]["allowUnixSockets"],
            [str(self.seats_path.resolve() / ".state" / rendered["router_name"] / "broker")],
        )
        self.assertEqual(self.acp_slots(), [])

    def test_a_dsh_profile_linked_into_the_orchestrator_profile_is_refused_before_any_settings_file_is_written(self):
        """U343c (verdict U343b-cae04852 P1 `:740`): the worker's grants were written without hcom-seat's overlap
        judgement, so `~/.omp/profiles/dsh` linked to `~/.omp/profiles/orchestrator` was granted read and write on
        that protected profile and the four canary probes did not see it. Every grant row is now judged against every
        deny row by identity (`settings_judge`, the judge of `hcom-seat`, with its tags): the link refuses with one
        line naming the grant row, its physical path and the deny it lies inside, before the slot and its settings
        file exist (`.state` is read-only for the connection, so a slot mkdir would have refused by its own name)
        and before any srt runs; a link to `~/.aws` refuses the same way; a real profile directory goes through."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        home = self.home_real
        (home / ".aws").mkdir()
        (home / ".omp/profiles/orchestrator").mkdir(parents=True)
        profile = home / ".omp/profiles/dsh"
        proc, sock = self.start_broker(name, cwd)
        state = self.seats_path / ".state"
        cases = (
            ("a link to another profile", home / ".omp/profiles/orchestrator",
             (f"allowRead row {profile} ({home / '.omp/profiles/orchestrator'}) is, contains or lies inside"
              f" {home / '.omp/profiles'}, a row of its denyRead list")),
            ("a link to ~/.aws", home / ".aws",
             f"allowRead row {profile} ({home / '.aws'}) is, contains or lies inside {home / '.aws'}, a row of its denyRead list"),
        )  # fmt: skip
        state.chmod(0o500)
        try:
            for label, target, message in cases:
                with self.subTest(case=label):
                    if profile.is_symlink():
                        profile.unlink()
                    profile.symlink_to(target)
                    data = self.recv_all(self.connect(sock, repo, "w1")).decode()
                    self.assertEqual(data.count("\n"), 1, data)
                    self.assertIn(f"acp-broker: refused: the worker's {message}", data)
                    self.assertIn("; the launch is refused before anything is made", data)
        finally:
            state.chmod(0o700)
        self.assertEqual(self.calls_of("srt"), [], "no clone and no canary: the judge refused first")
        self.assertEqual(self.calls_of("omp"), [])
        self.assertEqual(self.acp_slots(), [])
        self.assertEqual(
            self.state_names(), ["anthropic", "claude", name], "no state slot and no log for a refused launch"
        )
        self.assertTrue(profile.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(sorted(p.name for p in (home / ".aws").iterdir()), [])
        self.assertEqual(sorted(p.name for p in (home / ".omp/profiles/orchestrator").iterdir()), [])
        profile.unlink()
        self.assertEqual(self.exchange_record(sock, repo, "w1", PING), (PING, "status=0 push=none"))
        self.assertTrue(profile.is_dir() and not profile.is_symlink())
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_credential_root_is_held_from_dsh_home_and_checked_against_the_routers_write_deny(self):
        """U343l: the worker's one deny beyond the Router's table is the Router's credential root
        `<DSH_HOME>/router-credentials`, held from the broker's own environment in hcom-seat's form. Without `DSH_HOME`
        (unset or empty) the listener refuses at its start and a connection run by hand refuses on its stream, each
        with the line naming the variable and hcom-seat's sandbox environment; with the Router's settings denying no
        write of that root, the two levers disagree and the connection refuses by that line; a root that is a link,
        a file or absent refuses by name. Nothing is made and no tool runs. The listener holds the same root, so a
        broker started with the Router's environment serves connections (make_router's fixture)."""
        name, cwd = self.make_router()
        dsh_home = self.dsh_home_of_the_fixture()
        cred = f"{dsh_home}/router-credentials"
        sock = self.seats_path / ".state" / name / "broker/sock"
        template = self.seats_path / ".sandbox" / name / "srt-settings.json"
        good = template.read_text()
        header = "ACP-SEAT v1 repo=/x ref=HEAD name=w1\n"
        dsh_home_line = (
            "acp-broker: refused: DSH_HOME did not reach this connection; the broker runs inside the Router's sandbox,"
            " whose environment hcom-seat sets"
        )
        disagree_line = (
            f"acp-broker: refused: the Router's settings deny no write of its credential root {cred}; hcom-seat and"
            " this lever disagree on the root"
        )

        def listener(**overrides):
            run = subprocess.run(
                [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(**overrides),
                capture_output=True, text=True, check=False, timeout=60,
            )  # fmt: skip
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertFalse(sock.exists(), "no socket: the listener refused before it listened")
            return run.stderr

        def connection(**overrides):
            run = subprocess.run(
                [str(BROKER), "--connection", self.seats, name, str(cwd)], cwd=self.repo, input=header,
                env=self.broker_env(**overrides), capture_output=True, text=True, check=False, timeout=60,
            )  # fmt: skip
            self.assertEqual(run.returncode, 2, run.stderr)
            self.assertEqual(run.stdout.count("\n"), 1, run.stdout)
            self.assertEqual(self.acp_slots(), [])
            return run.stdout

        with self.subTest(case="DSH_HOME unset"):
            self.assertIn(dsh_home_line, listener(DSH_HOME=None))
            self.assertEqual(connection(DSH_HOME=None), dsh_home_line + "\n")
        with self.subTest(case="DSH_HOME empty"):
            self.assertIn(dsh_home_line, listener(DSH_HOME=""))
            self.assertEqual(connection(DSH_HOME=""), dsh_home_line + "\n")
        with self.subTest(case="DSH_HOME not a clean path"):
            self.assertIn("DSH_HOME 'relative/dsh' is not a clean absolute path", connection(DSH_HOME="relative/dsh"))
        with self.subTest(case="the Router's settings deny no write of the root"):
            settings = json.loads(good)
            settings["filesystem"]["denyWrite"].remove(cred)
            template.write_text(json.dumps(settings, separators=(",", ":")) + "\n")
            try:
                self.assertIn(disagree_line, listener())
                self.assertEqual(connection(), disagree_line + "\n")
            finally:
                template.write_text(good)
        with self.subTest(case="another DSH_HOME than the Router's"):
            other = Path(self.temp.name).resolve() / "other-dsh-home"
            (other / "router-credentials").mkdir(parents=True)
            self.assertIn(
                f"the Router's settings deny no write of its credential root {other}/router-credentials;",
                connection(DSH_HOME=str(other)),
            )
        root = dsh_home / "router-credentials"
        with self.subTest(case="the root is a link"):
            outside = self.home / ".config/gh"
            outside.mkdir(parents=True)
            root.rmdir()
            root.symlink_to(outside)
            try:
                # The physical form of a link is its target, outside DSH_HOME; the Router's row names the spelled
                # path, so the two disagree (the broker never denies the link's target in the Router's name).
                self.assertIn(
                    f"the Router's settings deny no write of its credential root {outside.resolve()};", connection()
                )
                self.assertEqual(list(outside.iterdir()), [], "nothing written at the link's target")
            finally:
                root.unlink()
        with self.subTest(case="the root is a file"):
            root.write_text("")
            try:
                self.assertIn(f"the Router's credential root {root} is not a real directory of this user", connection())
            finally:
                root.unlink()
        with self.subTest(case="the root is absent"):
            # physical_clean resolves an absent leaf through its nearest existing ancestor (hcom-seat's U353d note),
            # so the directory test refuses, not the resolution.
            self.assertIn(f"the Router's credential root {root} is not a real directory of this user", connection())
        self.assertEqual(self.calls_of("srt"), [], "nothing ran")
        self.assertEqual(self.calls_of("omp"), [])
        self.assertEqual(self.state_names(), ["anthropic", "claude", name], "no slot and no log for a refused launch")
        # Made again, the broker started with the Router's environment serves a connection: the worker's denyRead
        # ends with the held root and its denyWrite carries the Router's row of it.
        root.mkdir(mode=0o700)
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        rendered = json.loads((self.seats_path / ".state" / slot / "settings.json").read_text())
        self.assertEqual(rendered["filesystem"]["denyRead"][-1], cred)
        self.assertEqual(rendered["filesystem"]["denyWrite"].count(cred), 1)
        self.assertEqual(json.dumps(rendered).count(str(dsh_home)), 2)
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_api_key_file_path_reaches_the_worker_and_no_worker_starts_without_it(self):
        """U516 (handoff/47; U510, U512): the Router's subagent turns run on the seats' API key like every other bridge
        turn, so the worker's environment carries `REGIME_ANTHROPIC_KEY_FILE` equal to the broker's own (hcom-seat's
        router row sets it) beside `CLAUDE_CONFIG_DIR`, and the worker's `allowRead` gains the file's physical path
        as its last row and no other list names it. The broker holds the path as data and reads no key: the key's
        bytes appear in no stream, launch record or log line of the broker's. An unset or empty name, a relative path,
        an absent file, a symbolic link and a directory each refuse before any worker starts (fail closed, as
        `claude-keyed` refuses): the listener at its start and a connection run by hand on its stream, one stderr
        line naming the variable and the handout, exit 2, no socket, no slot, no omp run."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        key = str(self.key_file)
        self.assertEqual(self.key_file.read_text(), FIXTURE_KEY)
        proc, sock = self.start_broker(name, cwd)
        conn, slot, _task = self.held_connection(sock, repo, "w1")
        settings = json.loads((self.seats_path / ".state" / slot / "settings.json").read_text())
        self.assertEqual(settings["filesystem"]["allowRead"][-1], key)
        self.assertEqual(settings["filesystem"]["allowRead"].count(key), 1)
        self.assertNotIn(key, settings["filesystem"]["allowRead"][:-1] + settings["filesystem"]["allowWrite"])
        self.assertNotIn(key, settings["filesystem"]["denyRead"])
        # The Router's table denies the file for write (U512's row, which make_router renders as hcom-seat will) and
        # the worker copies that table: the read grant and the write deny of one file are hcom-seat's pair, no overlap.
        self.assertEqual(settings["filesystem"]["denyWrite"].count(key), 1)
        self.assertEqual(self.finish(conn, slot), (b"", "status=0 push=none"))
        _version, launch = self.calls_of("omp")
        self.assertEqual(launch["env"]["REGIME_ANTHROPIC_KEY_FILE"], key)
        self.assertEqual(launch["env"]["REGIME_ANTHROPIC_KEY_FILE"], self.broker_env()["REGIME_ANTHROPIC_KEY_FILE"])
        self.assertEqual(launch["env"]["CLAUDE_CONFIG_DIR"], str(self.seats_path / ".state/claude"))
        status, out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM)
        for where, text in (("stdout", out), ("stderr", err), ("the launch log", "\n".join(self.log_lines("w1"))),
                            ("the worker's launch record", json.dumps(launch))):  # fmt: skip
            self.assertNotIn(KEY_MARK, text, f"the key's bytes reached {where}")
        self.assertEqual(len(self.log_lines("w1")), 3, self.log_lines("w1"))

        header = "ACP-SEAT v1 repo=/x ref=HEAD name=w2\n"
        handout = "handouts/anthropic-api-key-u510.md"

        def refused(part, **overrides):
            run = subprocess.run(
                [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(**overrides),
                capture_output=True, text=True, check=False, timeout=60,
            )  # fmt: skip
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
            self.assertTrue(run.stderr.startswith("acp-broker: refused: REGIME_ANTHROPIC_KEY_FILE"), run.stderr)
            self.assertIn(part, run.stderr)
            self.assertIn(handout, run.stderr)
            self.assertFalse(sock.exists(), "no socket: the listener refused before it listened")
            run = subprocess.run(
                [str(BROKER), "--connection", self.seats, name, str(cwd)], cwd=self.repo, input=header,
                env=self.broker_env(**overrides), capture_output=True, text=True, check=False, timeout=60,
            )  # fmt: skip
            self.assertEqual(run.returncode, 2, run.stderr)
            self.assertEqual(run.stdout.count("\n"), 1, run.stdout)
            self.assertEqual(run.stdout, run.stderr, "the one line on the stream and on stderr")
            self.assertIn(part, run.stdout)
            self.assertEqual(self.acp_slots(), [])
            self.assertEqual(len(self.calls_of("omp")), 2, "no omp run beyond the served connection's two")
            self.assertEqual(sorted(p.name for p in (self.seats_path / ".state/broker-logs").iterdir()), ["w1.log"])

        anthropic = self.key_file.parent
        with self.subTest(case="unset"):
            refused("did not reach this connection", REGIME_ANTHROPIC_KEY_FILE=None)
        with self.subTest(case="empty"):
            refused("did not reach this connection", REGIME_ANTHROPIC_KEY_FILE="")
        with self.subTest(case="a relative path"):
            refused("'relative/api-key' is not a clean absolute path", REGIME_ANTHROPIC_KEY_FILE="relative/api-key")
        with self.subTest(case="an absent file"):
            refused(f"{anthropic}/missing is not a regular file", REGIME_ANTHROPIC_KEY_FILE=f"{anthropic}/missing")
        with self.subTest(case="a directory"):
            refused(f"{anthropic} is not a regular file", REGIME_ANTHROPIC_KEY_FILE=str(anthropic))
        with self.subTest(case="a symbolic link"):
            link = anthropic / "api-key-link"
            link.symlink_to(self.key_file)
            try:
                refused(f"{link} is a symbolic link", REGIME_ANTHROPIC_KEY_FILE=str(link))
            finally:
                link.unlink()
        self.assertEqual(self.key_file.read_text(), FIXTURE_KEY, "the key file is never written")

    def header_sent_by(self, argv, cwd):
        """The client run with `argv` after `--socket <scratch>` in `cwd` (the request's cwd `dsh-subagent-acp`
        spawns it in) against a scratch server in the broker's place that records the header line and answers a
        refusal: (the completed run, the header text or None when none was sent)."""
        sock = Path(self.temp.name).resolve() / "h" / "sock"
        sock.parent.mkdir(exist_ok=True)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        here = os.getcwd()
        os.chdir(sock.parent)
        try:
            server.bind(sock.name)
        finally:
            os.chdir(here)
        server.listen(1)
        headers = []

        def serve():
            conn, _ = server.accept()
            data = bytearray()
            while not data.endswith(b"\n") and len(data) < 4096:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
            headers.append(bytes(data))
            try:
                conn.sendall(b"acp-broker: refused: scratch\n")
                conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            conn.close()

        thread = threading.Thread(target=serve, daemon=True)
        thread.start()
        run = subprocess.run(
            [str(CLIENT), "--socket", str(sock), *argv], cwd=cwd, input=b"",
            env=self.broker_env(HCOM_SEAT_SANDBOX="/scratch/sandbox"), capture_output=True, check=False,
        )  # fmt: skip
        if not headers:
            # The client refused before connecting: one empty connection releases the server's accept.
            poke = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            os.chdir(sock.parent)
            try:
                poke.connect(sock.name)
            finally:
                os.chdir(here)
            poke.close()
            thread.join(timeout=30)
            headers.clear()
        thread.join(timeout=30)
        server.close()
        sock.unlink()
        return run, headers[0].decode() if headers else None

    def test_the_client_defaults_the_repository_to_its_cwd_and_the_ref_to_head(self):
        """U434 (M-22 Part B, table row s21): `dsh-subagent-acp` spawns the client per request in the request's cwd
        with the row's fixed args (`--socket`, `--name`), so a client run in a repository directory without `--repo`
        and `--ref` sends the header `ACP-SEAT v1 repo=<that directory> ref=HEAD name=<name>` (the broker judges the
        path as it judges any header repository); `--repo` and `--ref` given keep their values, singly or together;
        `--socket` or `--name` missing, or a flag outside the four, is refused with the usage line before anything
        is sent, as now; omp never runs."""
        repo, _base = self.make_repo(Path(self.temp.name).resolve() / "u345" / "repo")
        run, header = self.header_sent_by(["--name", "w1"], cwd=repo)
        self.assertEqual(header, f"ACP-SEAT v1 repo={repo} ref=HEAD name=w1\n")
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"acp-broker: refused: scratch\n", run.stderr)
        run, header = self.header_sent_by(["--repo", "/x/y", "--ref", "v1.2", "--name", "w2"], cwd=repo)
        self.assertEqual(header, "ACP-SEAT v1 repo=/x/y ref=v1.2 name=w2\n")
        run, header = self.header_sent_by(["--ref", "main", "--name", "w3"], cwd=repo)
        self.assertEqual(header, f"ACP-SEAT v1 repo={repo} ref=main name=w3\n")
        run, header = self.header_sent_by(["--repo", "/x/y", "--name", "w4"], cwd=repo)
        self.assertEqual(header, "ACP-SEAT v1 repo=/x/y ref=HEAD name=w4\n")
        usage = b"usage: acp-seat --socket <path> --name <name> [--repo <path>] [--ref <rev>]"
        for label, argv in (
            ("--name missing", ["--repo", str(repo), "--ref", "HEAD"]),
            ("--name missing, nothing else", []),
            ("a flag outside the four", ["--name", "w1", "--cwd", str(repo)]),
            ("--name given twice", ["--name", "w1", "--name", "w1"]),
        ):
            with self.subTest(case=label):
                run, header = self.header_sent_by(argv, cwd=repo)
                self.assertIsNone(header, "nothing was sent")
                self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
                self.assertIn(usage, run.stderr)
        run = subprocess.run(
            [str(CLIENT), "--name", "w1"], cwd=repo, input=b"",
            env=self.broker_env(HCOM_SEAT_SANDBOX="/scratch/sandbox"), capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(usage, run.stderr)
        self.assertEqual(self.calls_of("omp"), [])


if __name__ == "__main__":
    unittest.main()
