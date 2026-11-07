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

import json
import os
import re
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
SYSTEM_PATH = test_hcom_seat.SYSTEM_PATH
BASH_OWN_NAMES = test_hcom_seat_dsh.BASH_OWN_NAMES
FOUR_WORDS = "write-denied read-denied ssh-denied debug-denied"
TRAILER = re.compile(rb"\nomp acp exit (\d+) push=(\S+)\n$")
PUSHED_REF = re.compile(r"^refs/acp-seat/([a-z0-9][a-z0-9_-]*)/(\d{8}-\d{6}-\d+)$")
PROJECT_FILES = (".claude/settings.json", ".claude/settings.local.json", ".claude/hooks", ".claude/contextdb", ".omp",
                 ".codex", ".envrc", ".mcp.json")  # fmt: skip
CLAUDE_ROWS = ("settings.json", "settings.local.json", "rules", "hooks", "plugins", "skills", "commands", "agents")
DOMAINS = ["github.com", "api.github.com", "uploads.github.com", "codeload.github.com", "objects.githubusercontent.com",
           "raw.githubusercontent.com", "release-assets.githubusercontent.com", "pypi.org", "files.pythonhosted.org",
           "api.anthropic.com", "claude.ai", "platform.claude.com", "console.anthropic.com", "chatgpt.com",
           "auth.openai.com", "api.openai.com"]  # fmt: skip
PING = b'{"jsonrpc":"2.0","id":1,"method":"ping"}\n'

# The fake srt: records argv, environment names and cwd; `--version` answers 0.0.81; when `swap-ancestor` exists
# beside the calls it performs the swap that file describes (the Router replacing an ancestor of its repository:
# `ancestor` renamed to `moved`, then a link to `link` put at the name when one is given) at the moment its `at`
# names: `first`, before the first srt call of any kind (the clone's read of the repository, so the clone fails), or
# `canary`, before the canary (after the clone); the swap runs once and the file is consumed. The canary (`/bin/sh
# -c <script> canary <write> <read> <ssh> <debug>`) prints `canary-answer` when that file exists, writes the canary
# file first when `canary-write` exists (a sandbox that lets the write probe succeed), exits 3 when `srt-fail`
# exists (a canary that did not run), else runs the script with the four paths swapped for ones under a directory
# that does not exist, so the probes fail as the sandbox makes them fail; any other command (omp, the isolated git
# the broker runs inside the Router's settings) is executed.
FAKE_SRT = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, subprocess, sys
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "srt.json")))
    argv = sys.argv[1:]
    with open(os.path.join(conf["calls"], "srt"), "a") as calls:
        calls.write(json.dumps({"argv": argv, "argv0": sys.argv[0], "env": sorted(os.environ), "cwd": os.getcwd()}) + "\\n")
    if argv == ["--version"]:
        print("0.0.81")
        sys.exit(0)
    command = argv[argv.index("--") + 1 :]
    canary = command[:2] == ["/bin/sh", "-c"]
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
    os.execvp(command[0], command)
    """
)
# The fake omp: records argv, argv0, cwd and the whole environment; `--version` prints 18.12.6 (exit `omp-version-
# status` when that file exists); `acp` starts a sleeping descendant when `omp-child` exists (its pid written to
# `omp-child-pid`, the tool child of the verdict's P2 at acp-broker:1079), echoes stdin line by line until EOF and
# exits `omp-status` when that file exists.
FAKE_OMP = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, subprocess, sys
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
    status = os.path.join(calls, "omp-status")
    sys.exit(int(open(status).read()) if os.path.exists(status) else 0)
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

    # --- the scratch Router, its repository and the broker ---

    def make_router(self, name="router-20261107-000000-1"):
        """A Router slot in the shape `hcom-seat router` leaves: the state slot with its scratch cwd, the shared Claude
        Code directory, and the settings file in the dsh row's shape with the router cells (the loopback grant, the
        state root, the broker directory in allowUnixSockets)."""
        seats = self.seats_path
        seats.mkdir(mode=0o700, exist_ok=True)
        state = seats / ".state" / name
        for path in (seats / ".state", state, state / "cwd", seats / ".state/claude", seats / ".sandbox",
                     seats / ".sandbox" / name):  # fmt: skip
            path.mkdir(mode=0o700, exist_ok=True)
        home, repo, store = self.home_real, self.repo.resolve(), self.store.resolve()
        cwd = state / "cwd"
        dsh_home = home / "dsh-home"
        deny_read = [f"{home}/.ssh", f"{home}/.gnupg", f"{home}/.aws", f"{home}/.netrc", f"{home}/.docker",
                     f"{home}/.kube", f"{home}/.config/gcloud", f"{home}/.codex", f"{home}/.omp/agent",
                     f"{home}/.omp/profiles", f"{home}/.hcom", f"{home}/.local/state/hcom",
                     f"{home}/.local/share/chezmoi", f"{home}/.local/share/chezmoi-private",
                     f"{home}/.config/chezmoi", f"{home}/.config/chezmoi-private", f"{home}/Workspace",
                     f"{seats}/.sandbox", f"{home}/.local/state/omp-seats", str(seats), f"{home}/.claude",
                     f"{home}/.claude.json", str(repo), f"{repo}/.git", str(store), f"{repo}/.orchestration"]  # fmt: skip
        deny_write = [f"{seats}/.sandbox", *(f"{cwd}/{p}" for p in PROJECT_FILES),
                      *(f"{seats}/.state/claude/{p}" for p in CLAUDE_ROWS), *(f"{repo}/{p}" for p in PROJECT_FILES),
                      f"{repo}/.git/config", f"{repo}/.git/config.worktree", f"{repo}/.git/info", f"{repo}/.git/hooks",
                      f"{repo}/.git/worktrees/*/config.worktree", f"{repo}/.git/worktrees/*/info",
                      f"{repo}/.git/worktrees/*/commondir", f"{repo}/.git/worktrees/*/gitdir",
                      f"{store}/config.toml", f"{home}/.claude", f"{home}/.claude.json", f"{repo}/.git", str(store),
                      f"{repo}/.orchestration"]  # fmt: skip
        settings = {
            "network": {"allowedDomains": DOMAINS, "deniedDomains": [], "allowUnixSockets": [f"{state}/broker"],
                        "allowMachLookup": ["com.apple.trustd.agent"], "allowLocalBinding": True},
            "filesystem": {
                "denyRead": deny_read,
                "allowRead": [str(cwd), str(state), f"{seats}/.state/claude", str(dsh_home), f"{home}/.omp/profiles/dsh",
                              f"{home}/.agents/skills", f"{home}/.local/state/hcom-seat/tools"],
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

    def broker_env(self, **overrides):
        env = {**self.env, **{k: v for k, v in overrides.items() if v is not None}}
        for key in (k for k, v in overrides.items() if v is None):
            env.pop(key, None)
        return env

    def start_broker(self, name, cwd, wrapper=(), **overrides):
        """Start the broker for the Router `name` (through the argv prefix `wrapper` when given) and return (process,
        socket path) once the socket exists."""
        proc = subprocess.Popen(
            [*wrapper, str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(**overrides),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )  # fmt: skip
        self.brokers.append(proc)
        sock = self.seats_path / ".state" / name / "broker/sock"
        deadline = time.monotonic() + 60
        while not sock.exists():
            if proc.poll() is not None:
                out, err = proc.communicate()
                self.fail(f"the broker ended before it listened: {proc.returncode} {out!r} {err!r}")
            if time.monotonic() > deadline:
                self.fail("the broker did not listen within 60 s")
            time.sleep(0.02)
        return proc, sock

    def stop_broker(self, proc, sig=signal.SIGTERM):
        if proc.poll() is None:
            proc.send_signal(sig)
        try:
            out, err = proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
        return proc.returncode, out, err

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
        path = self.seats_path / ".state" / name / "acp-launch.log"
        return path.read_text().splitlines() if path.exists() else []

    def held_connection(self, sock, repo, name, ref="HEAD"):
        """A connection with one line echoed back, so the worker is running and its slot exists; returns the
        connection, the slot name and the worker's tree."""
        conn = self.connect(sock, repo, name, ref=ref)
        conn.sendall(PING)
        self.assertEqual(self.recv_line(conn), PING)
        (slot,) = self.acp_slots()
        return conn, slot, self.slot_task(slot)

    # --- the tests ---

    def test_a_broker_inside_a_seat_is_refused_before_anything_is_made(self):
        """The three markers (hcom's two and the shim's) each refuse before the broker directory exists; a seat, the
        Router included, never starts a broker."""
        name, cwd = self.make_router()
        for marker in ("HCOM_LAUNCHED", "HCOM_PROCESS_ID", "HCOM_SEAT_SANDBOX"):
            with self.subTest(marker=marker):
                run = subprocess.run(
                    [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(**{marker: "1"}),
                    capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"acp-broker: refused: refused inside a seat ({marker} is set)", run.stderr)
                self.assertFalse((self.seats_path / ".state" / name / "broker").exists())
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
        self.assertEqual(self.state_names(), ["claude", name])
        self.assertEqual(self.calls_of("srt"), [])
        self.assertEqual(self.calls_of("omp"), [])
        # A good header after the bad ones still works: the broker refused connections, not itself; a name of 64
        # characters, the grammar's longest, launches (verdict P2 `:980`: the limit was applied to the slot name).
        self.assertEqual(self.exchange(sock, repo, "w1", PING), PING + b"omp acp exit 0 push=none\n")
        self.assertEqual(self.exchange(sock, repo, "a" * 64, PING), PING + b"omp acp exit 0 push=none\n")
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
        self.assertEqual(self.state_names(), ["claude", name], "no state slot and no log for a refused launch")
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
                 "/tmp/claude", "/private/tmp/claude"}  # fmt: skip
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
                conn.shutdown(socket.SHUT_WR)
                self.assertEqual(self.recv_all(conn), b"omp acp exit 0 push=none\n")
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
        tool directory; no row of any list lies under the Router's scratch cwd or its state slot, and the Router's
        project-file denies are re-rooted under the task. The slot is 0700 under `.state`, its settings 0600, the
        task a detached checkout of the ref; the slot is gone when the connection ends."""
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
        self.assertEqual(fs["allowRead"], [str(task), str(self.seats_path / ".state/claude"), f"{home}/.omp/profiles/dsh", f"{home}/.agents/skills", f"{home}/.local/state/hcom-seat/tools"])  # fmt: skip
        state = self.seats_path / ".state" / name
        for kind in ("allowRead", "allowWrite", "denyRead", "denyWrite"):
            for row in fs[kind]:
                self.assertFalse(
                    row == str(cwd) or row.startswith(f"{cwd}/"),
                    f"{kind} row {row} lies under the Router's scratch cwd",
                )
                self.assertFalse(
                    row == str(state) or row.startswith(f"{state}/"),
                    f"{kind} row {row} lies under the Router's state slot",
                )
        self.assertEqual(
            [r for r in fs["denyWrite"] if r.startswith(f"{task}/")], [f"{task}/{p}" for p in PROJECT_FILES]
        )
        self.assertEqual(settings["network"]["allowUnixSockets"], [])
        self.assertEqual(self.scratch_git("rev-parse", "HEAD", cwd=task), base)
        self.assertEqual(self.scratch_git("status", "--porcelain", cwd=task), "")
        self.assertEqual(self.scratch_git("rev-parse", "--abbrev-ref", "HEAD", cwd=task), "HEAD", "detached")
        self.assertEqual(sorted(p.name for p in slot_path.iterdir()), ["settings.json", "task"], "no pack left behind")
        conn.shutdown(socket.SHUT_WR)
        self.assertEqual(self.recv_all(conn), b"omp acp exit 0 push=none\n")
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_c_the_end_of_session_push_lands_the_worker_head_at_refs_acp_seat_and_the_trailer_names_it(self):
        """U343e test (c): a commit the worker made lands in the repository at `refs/acp-seat/<name>/<stamp>` when
        omp exits, written inside the Router's settings, and the trailer (and the log's exit line) names the ref;
        a worker whose HEAD is the ref pushes nothing (`push=none`); a repository made read-only after the clone
        gives `push=failed`, the reason on the broker's stderr; the trailer follows the slot's removal."""
        name, cwd = self.make_router()
        repo, base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        conn, slot, task = self.held_connection(sock, repo, "w1")
        head = self.commit_in(task)
        conn.shutdown(socket.SHUT_WR)
        data = self.recv_all(conn)
        match = re.fullmatch(rb"omp acp exit 0 push=(refs/acp-seat/w1/\d{8}-\d{6}-\d+)\n", data)
        self.assertIsNotNone(match, data)
        ref = match.group(1).decode()
        self.assertEqual(ref.rsplit("/", 1)[1], slot[len("acp-w1-") :], "the stamp of the slot")
        self.assertEqual(self.scratch_git("rev-parse", "--verify", ref, cwd=repo), head)
        self.assertEqual(self.scratch_git("show", f"{ref}:b.txt", cwd=repo), "world")
        self.assertEqual(self.scratch_git("rev-parse", "HEAD", cwd=repo), base, "the repository's own HEAD untouched")
        self.assertEqual(self.log_lines("w1")[2].split(" acp-broker: ")[1], f"omp acp exit 0 push={ref}")
        self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        with self.subTest(case="HEAD equal to the ref"):
            self.assertEqual(self.exchange(sock, repo, "w1", PING), PING + b"omp acp exit 0 push=none\n")
            self.assertEqual(self.scratch_git("for-each-ref", "--format=%(refname)", "refs/acp-seat/", cwd=repo), ref)
        with self.subTest(case="the ref the worker started from"):
            conn, slot, task = self.held_connection(sock, repo, "w1", ref=ref)
            self.assertEqual(self.scratch_git("rev-parse", "HEAD", cwd=task), head)
            head2 = self.commit_in(task, "c.txt")
            conn.shutdown(socket.SHUT_WR)
            data = self.recv_all(conn)
            match = re.fullmatch(rb"omp acp exit 0 push=(refs/acp-seat/w1/\S+)\n", data)
            self.assertIsNotNone(match, data)
            self.assertEqual(self.scratch_git("rev-parse", "--verify", match.group(1).decode(), cwd=repo), head2)
        with self.subTest(case="a repository made read-only after the clone"):
            conn, slot, task = self.held_connection(sock, repo, "w1")
            self.commit_in(task, "d.txt")
            subprocess.run(["chmod", "-R", "a-w", str(repo / ".git")], check=True)
            try:
                conn.shutdown(socket.SHUT_WR)
                data = self.recv_all(conn)
            finally:
                subprocess.run(["chmod", "-R", "u+w", str(repo / ".git")], check=True)
            self.assertEqual(data, b"omp acp exit 0 push=failed\n")
            self.assertEqual(self.log_lines("w1")[-1].split(" acp-broker: ")[1], "omp acp exit 0 push=failed")
            self.wait_for(lambda: self.acp_slots() == [], "the slot's removal")
        with self.subTest(case="through the client"):
            run = self.client(sock, repo, "w1", PING)
            self.assertEqual((run.returncode, run.stdout, run.stderr), (0, PING, b"acp-seat: push=none\n"))
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertIn("acp-broker: the push of ", err)
        self.assertIn("failed", err)

    def test_a_slot_that_cannot_be_removed_gives_a_trailer_of_exit_2_after_the_removal(self):
        """Verdict U343d-136fbe0a P2 `:1157`: the success trailer preceded the slot's removal, so a slot left behind
        exited the handler 2 while the client read exit 0. The removal comes first and the trailer carries the
        connection's status: `.state` made read-only while the worker runs keeps the slot's entry in place, the
        trailer reads `omp acp exit 2 push=none`, the log keeps omp's own status, the client exits 2."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        state = self.seats_path / ".state"
        conn, slot, _task = self.held_connection(sock, repo, "w1")
        state.chmod(0o500)
        try:
            conn.shutdown(socket.SHUT_WR)
            data = self.recv_all(conn)
        finally:
            state.chmod(0o700)
        self.assertEqual(data, b"omp acp exit 2 push=none\n")
        self.assertEqual(self.acp_slots(), [slot], "the slot's entry stayed in the read-only directory")
        self.assertEqual(self.log_lines("w1")[-1].split(" acp-broker: ")[1], "omp acp exit 0 push=none")
        subprocess.run(["chmod", "-R", "u+rwX", str(state / slot)], check=True)
        subprocess.run(["rm", "-rf", str(state / slot)], check=True)
        status, _out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertIn(f"the per-connection slot {state / slot} remains after its removal", err)

    def test_a_termination_ends_omp_and_its_descendants(self):
        """Verdict U343d-136fbe0a P2 `:1079`: the trap ended the immediate child alone and an omp tool descendant
        outlived the handler. The launch runs in its own process group and the trap ends the group: the fake omp's
        sleeping child is gone when the broker has exited."""
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
        self.assertEqual(self.state_names(), ["claude", name], "no state slot and no log for a refused launch")
        self.assertEqual(len(self.canaries()), 5, "one canary per connection, nothing after it")
        self.assertEqual(len(self.calls_of("srt")), 15, "the clone's two reads and the canary per connection")
        self.assertEqual(self.exchange(sock, repo, "w1", PING), PING + b"omp acp exit 0 push=none\n")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_a_1mib_json_rpc_line_is_relayed_equal_through_the_socket_and_back(self):
        """The U342 relay measurement as a test: a 1 MiB JSON-RPC line through the socket to the fake `omp acp` echo and
        back, equal, the trailer last; the same through the client, whose stdout is the line alone, whose stderr is
        the trailer's push word and whose exit status is the trailer's."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        line = one_mib_line()
        data = self.exchange(sock, repo, "w1", line)
        self.assertEqual(len(data), len(line) + len(b"omp acp exit 0 push=none\n"))
        self.assertEqual(data[: len(line)], line)
        self.assertEqual(data[len(line) :], b"omp acp exit 0 push=none\n")
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
        <commit>`, `omp acp exit <status> push=<word>`, appended per launch under `<seats-root>/.state/<name>/`, a
        directory the broker makes 0700."""
        name, cwd = self.make_router()
        repo, base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        line = b'{"jsonrpc":"2.0","id":1,"method":"initialize"}\n'
        self.assertEqual(self.exchange(sock, repo, "w1", line), line + b"omp acp exit 0 push=none\n")
        (self.calls / "omp-status").write_text("7")
        self.assertEqual(self.exchange(sock, repo, "w1", line, ref=base), line + b"omp acp exit 7 push=none\n")
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
        state = self.seats_path / ".state/w1"
        self.assertEqual(stat.S_IMODE(os.lstat(state).st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(os.lstat(state / "acp-launch.log").st_mode), 0o600)
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_srt_and_omp_run_by_their_physical_argv_under_the_listed_environment(self):
        """srt, omp and git are found through a link directory first on the caller's PATH and run by their physical
        files (the fake records argv0); omp's environment holds exactly the listed names; the srt argv is `--settings
        <slot settings> -- /usr/bin/env PATH=<seat path> <omp argv> acp --profile dsh` in the slot's task; the clone's
        two git runs and the canary run under the Router's own settings file."""
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
        self.assertEqual(self.exchange(sock, repo, "w1", PING), PING + b"omp acp exit 0 push=none\n")
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
                  "USER": "u343", "LANG": "C.UTF-8"}  # fmt: skip
        self.assertEqual({k: v for k, v in launch["env"].items() if k not in own}, listed)
        self.assertEqual(set(launch["env"]) - own, set(listed))
        resolve, pack, canary, version_call, launch_call = self.calls_of("srt")
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
        self.assertEqual(launch_call["argv"], ["--settings", settings, "--", "/usr/bin/env", f"PATH={seat_path}",
                                               str(self.python), str(self.bindir / "omp"), "acp", "--profile", "dsh"])  # fmt: skip
        self.assertEqual(launch_call["cwd"], task)
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
        c1.sendall(PING)
        c2.sendall(PING)
        self.assertEqual(self.recv_line(c1), PING)
        self.assertEqual(self.recv_line(c2), PING)
        slots = self.acp_slots()
        self.assertEqual(len(slots), 2, slots)
        self.assertEqual([s.split("-")[1] for s in slots], ["w1", "w2"])
        for slot in slots:
            path = self.seats_path / ".state" / slot
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700)
            self.assertTrue((path / "settings.json").is_file(), slot)
            self.assertEqual(stat.S_IMODE(os.lstat(path / "settings.json").st_mode), 0o600)
            self.assertEqual((path / "task/a.txt").read_text(), "hello\n")
        settings = [json.loads((self.seats_path / ".state" / s / "settings.json").read_text()) for s in slots]
        self.assertEqual([s["filesystem"]["allowWrite"][0] for s in settings], [str(self.slot_task(s)) for s in slots])
        self.assertEqual(self.state_names(), ["claude", name, "w1", "w2"])
        c1.shutdown(socket.SHUT_WR)
        c2.shutdown(socket.SHUT_WR)
        self.assertEqual(self.recv_all(c1), b"omp acp exit 0 push=none\n")
        self.assertEqual(self.recv_all(c2), b"omp acp exit 0 push=none\n")
        self.wait_for(lambda: self.acp_slots() == [], "the two slots' removal")
        self.assertEqual(self.exchange(sock, repo, "w3", PING), PING + b"omp acp exit 0 push=none\n")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_socket_and_its_directory_are_gone_after_the_broker_exits(self):
        """A termination while a worker runs: the handler's trap ends omp, logs the exit and removes the slot, the relay
        removes the socket, the broker its directory, and the broker ends by the signal."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        broker_dir = sock.parent
        self.assertEqual(stat.S_IMODE(os.lstat(broker_dir).st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(os.lstat(sock).st_mode), 0o600)
        conn = self.connect(sock, repo, "w1")
        conn.sendall(PING)
        self.assertEqual(self.recv_line(conn), PING)
        self.assertEqual(len(self.acp_slots()), 1)
        status, out, err = self.stop_broker(proc)
        self.assertEqual(status, -signal.SIGTERM, err)
        self.assertEqual(out, f"acp-broker: listening on {sock}\n")
        self.assertFalse(sock.exists())
        self.assertFalse(broker_dir.exists())
        self.assertEqual(self.acp_slots(), [], "the live worker's slot went with the broker")
        rest = self.recv_all(conn)
        self.assertRegex(rest, rb"^(omp acp exit \d+ push=\S+\n)?$")
        lines = self.log_lines("w1")
        self.assertEqual(len(lines), 3, lines)
        self.assertRegex(lines[2], r" acp-broker: omp acp exit \d+ push=skipped$")
        # A hangup and an interrupt do the same, each ending the broker by its own signal.
        for sig in (signal.SIGHUP, signal.SIGINT):
            with self.subTest(signal=sig.name):
                proc, sock = self.start_broker(name, cwd)
                self.assertEqual(self.stop_broker(proc, sig)[0], -sig)
                self.assertFalse(sock.exists())
                self.assertFalse(sock.parent.exists())

    def test_a_second_broker_on_the_same_slot_refuses(self):
        """While a broker listens for a Router, a second one for the same slot refuses by name and touches nothing;
        a broker directory that exists without its socket refuses too and is left in place (verdict U343d-136fbe0a
        P2 `:854`: the broker directory is made by this process alone, so a loser never removes a winner's socket)."""
        name, cwd = self.make_router()
        repo, _base = self.make_repo(cwd / "repo")
        proc, sock = self.start_broker(name, cwd)
        run = subprocess.run(
            [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(),
            capture_output=True, text=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"acp-broker: refused: a broker already listens for the Router {name} ({sock} exists)", run.stderr
        )
        self.assertTrue(sock.exists(), "the first broker's socket stays")
        self.assertIsNone(proc.poll())
        self.assertEqual(self.exchange(sock, repo, "w1", PING), PING + b"omp acp exit 0 push=none\n")
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)
        self.assertFalse(sock.parent.exists())
        # A stale directory (a crashed broker's, or another's between its mkdir and its bind) refuses and stays.
        sock.parent.mkdir(mode=0o700)
        (sock.parent / "note").write_text("x\n")
        run = subprocess.run(
            [str(BROKER), self.seats, name, str(cwd)], cwd=self.repo, env=self.broker_env(),
            capture_output=True, text=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"acp-broker: refused: the broker directory {sock.parent} exists without its socket", run.stderr)
        self.assertTrue((sock.parent / "note").exists(), "the refusing broker removed nothing")
        sock.parent.joinpath("note").unlink()
        sock.parent.rmdir()
        # After it is gone, a new broker takes the slot again.
        proc, sock = self.start_broker(name, cwd)
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

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
            [str(CLIENT), "--socket", str(sock), "--repo", str(repo), "--name", "w1"], input=PING,
            env=self.broker_env(HCOM_SEAT_SANDBOX="x"), capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertIn(b"usage: acp-seat --socket <path> --repo <path> --ref <rev> --name <name>", run.stderr)
        run = subprocess.run(
            [str(CLIENT), "--socket", str(sock), "--cwd", str(repo), "--ref", "HEAD", "--name", "w1"], input=PING,
            env=self.broker_env(HCOM_SEAT_SANDBOX="x"), capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, b""), run.stderr)
        self.assertEqual(self.calls_of("omp"), [])
        # The exit status is the trailer's, and the trailer is never printed on stdout.
        (self.calls / "omp-status").write_text("9")
        run = self.client(sock, repo, "w1", PING)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (9, PING, b"acp-seat: push=none\n"))
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)

    def test_the_client_takes_the_trailer_from_the_last_line_alone(self):
        """Verdict U343d-136fbe0a P2 `acp-seat:168`: any matching line was taken as the trailer, so a stream `omp acp
        exit 0`, payload, EOF returned 0 without a final trailer. Against a scratch server in the broker's place:
        a trailer-shaped line followed by payload is payload (written to stdout, in order) and the stream ends
        without a trailer (exit 2); the same line last is the trailer; a refusal first line is exit 2 on stderr."""
        sock = Path(self.temp.name).resolve() / "s" / "sock"
        sock.parent.mkdir()
        streams = {
            "a trailer-shaped line, then payload": (b"omp acp exit 0 push=none\n" + PING, 2, b"omp acp exit 0 push=none\n" + PING, b"acp-seat: the broker closed the connection without an exit trailer\n"),
            "payload, then the trailer last": (PING + b"omp acp exit 5 push=refs/acp-seat/w1/x\n", 5, PING, b"acp-seat: push=refs/acp-seat/w1/x\n"),
            "two trailer-shaped lines": (b"omp acp exit 0 push=none\nomp acp exit 3 push=failed\n", 3, b"omp acp exit 0 push=none\n", b"acp-seat: push=failed\n"),
            "a refusal first": (b"acp-broker: refused: no\n" + PING, 2, b"", b"acp-broker: refused: no\n"),
            "a trailer without a newline": (PING + b"omp acp exit 4 push=none", 4, PING, b"acp-seat: push=none\n"),
        }  # fmt: skip
        for label, (stream, status, stdout, stderr) in streams.items():
            with self.subTest(case=label):
                server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                here = os.getcwd()
                os.chdir(sock.parent)
                try:
                    server.bind(sock.name)
                finally:
                    os.chdir(here)
                server.listen(1)

                def serve(server=server, stream=stream):
                    conn, _ = server.accept()
                    conn.recv(4096)  # the header
                    conn.sendall(stream)
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()

                thread = threading.Thread(target=serve, daemon=True)
                thread.start()
                run = self.client(sock, "/repo", "w1", b"")
                thread.join(timeout=30)
                server.close()
                sock.unlink()
                self.assertEqual((run.returncode, run.stdout, run.stderr), (status, stdout, stderr))

    def test_every_producer_injection_refuses_by_name(self):
        """Each producer the launch reads fails in turn: the slot mkdir, a physical resolution, the Router settings
        read (a malformed file, an unclean row), the settings write (a file size limit on the broker), the canary,
        srt's exit (the trailer and the log carry omp's status), the omp version read and the log append. Each refuses
        with one line naming what failed, starts no omp and leaves no slot."""
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
            w2 = state / "w2"
            w2.mkdir(mode=0o500)
            try:
                refused(f"cannot append to the launch log {w2}/acp-launch.log", worker="w2")
            finally:
                w2.chmod(0o700)
            self.assertEqual([c["argv"] for c in self.calls_of("omp")], [["--version"]], "omp acp never started")
            self.assertEqual(self.log_lines("w2"), [])
        with self.subTest(producer="srt's exit, as the trailer and the log"):
            (self.calls / "omp-status").write_text("5")
            try:
                self.assertEqual(self.exchange(sock, repo, "w1", PING), PING + b"omp acp exit 5 push=none\n")
            finally:
                (self.calls / "omp-status").unlink()
            self.assertRegex(self.log_lines("w1")[-1], r" acp-broker: omp acp exit 5 push=none$")
            self.assertEqual(self.acp_slots(), [])
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)
        with self.subTest(producer="the settings write"):
            # A file size limit of 1 KiB on the broker (inherited by every handler) fails the settings write, which
            # is larger; SIGXFSZ is ignored so the write fails with EFBIG instead of ending the shell.
            limit = [
                sys.executable, "-c",
                (
                    "import os, resource, signal, sys\n"
                    "signal.signal(signal.SIGXFSZ, signal.SIG_IGN)\n"
                    "resource.setrlimit(resource.RLIMIT_FSIZE, (1024, 1024))\n"
                    "os.execv(sys.argv[1], sys.argv[1:])\n"
                ),
            ]  # fmt: skip
            proc, sock = self.start_broker(name, cwd, wrapper=limit)
            refused("cannot write the worker settings")
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
                # The broker against the live Router slot: one connection held open while the settings are read.
                scratch = self.seats_path / ".state" / seat_name / "cwd"
                repo, _base = self.make_repo(scratch / "repo")
                proc, sock = self.start_broker(seat_name, scratch)
                conn, slot, task = self.held_connection(sock, repo, "w1")
                rendered["worker"] = (self.seats_path / ".state" / slot / "settings.json").read_bytes()
                conn.shutdown(socket.SHUT_WR)
                self.assertEqual(self.recv_all(conn), b"omp acp exit 0 push=none\n")
                self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)
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
        credentials = f"{home}/.local/state/dsh-router/credentials"

        def reroot(row, old, new):
            return new + row[len(old) :] if row.startswith(old + "/") else row

        # The deny table: the Router's, byte for byte, but the re-rooted project-file rows and the credential root.
        self.assertEqual(worker["filesystem"]["denyRead"], router["filesystem"]["denyRead"] + [credentials])
        self.assertEqual(
            worker["filesystem"]["denyWrite"], [reroot(r, router_cwd, task) for r in router["filesystem"]["denyWrite"]]
        )
        self.assertEqual(
            len([r for r in worker["filesystem"]["denyWrite"] if r.startswith(task + "/")]), len(PROJECT_FILES)
        )

        # And the dsh row's, once the per-launch names and the cwd are normalised: the one shape, rendered twice.
        def normalised(settings, cwd, launch_name):
            text = json.dumps(settings, separators=(",", ":")).replace(cwd, "<cwd>").replace(launch_name, "<launch>")
            return json.loads(text)

        dsh_n = normalised(dsh, dsh_cwd, rendered["dsh_name"])
        worker_n = normalised(worker, task, rendered["router_name"])
        self.assertEqual(worker_n["filesystem"]["denyRead"], dsh_n["filesystem"]["denyRead"] + [credentials])
        self.assertEqual(worker_n["filesystem"]["denyWrite"], dsh_n["filesystem"]["denyWrite"])
        self.assertEqual(
            json.dumps(worker_n["filesystem"]["denyWrite"]).encode(),
            json.dumps(dsh_n["filesystem"]["denyWrite"]).encode(),
            "byte-identical deny tables",
        )
        # The grants: the dsh row's rows 0, 2, 4.. with the slot's task as row 0 (no state slot, no DSH_HOME).
        dsh_read, dsh_write = dsh["filesystem"]["allowRead"], dsh["filesystem"]["allowWrite"]
        self.assertEqual(dsh_read[1], str(self.seats_path / ".state" / rendered["dsh_name"]))
        self.assertEqual(dsh_read[3], str(dsh_home))
        self.assertEqual(worker["filesystem"]["allowRead"], [task, dsh_read[2], *dsh_read[4:]])
        self.assertEqual(worker["filesystem"]["allowWrite"], [task, dsh_write[2], *dsh_write[4:]])
        self.assertEqual(worker["filesystem"]["allowRead"][1], str(self.seats_path / ".state/claude"))
        self.assertEqual(worker["filesystem"]["allowWrite"][2:4], [f"{home}/.omp/profiles/dsh", f"{home}/.omp/run"])
        self.assertNotIn(str(dsh_home), json.dumps(worker))
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
        self.assertEqual(self.state_names(), ["claude", name], "no state slot and no log for a refused launch")
        self.assertTrue(profile.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(sorted(p.name for p in (home / ".aws").iterdir()), [])
        self.assertEqual(sorted(p.name for p in (home / ".omp/profiles/orchestrator").iterdir()), [])
        profile.unlink()
        self.assertEqual(self.exchange(sock, repo, "w1", PING), PING + b"omp acp exit 0 push=none\n")
        self.assertTrue(profile.is_dir() and not profile.is_symlink())
        self.assertEqual(self.stop_broker(proc)[0], -signal.SIGTERM)


if __name__ == "__main__":
    unittest.main()
