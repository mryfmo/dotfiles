#!/usr/bin/env -S python3 -I -S
"""The Unix-socket listener and byte relay of `acp-broker` (regime-cutover U343, M-24 part 1).

`acp-broker` runs this helper by its pinned physical argv as `python3 -I -S acp-relay.py <socket path> -- <handler
argv...>` after checking its `claude.levers.sha256` pin, and this file checks the same pin itself first (the sourced-
helper rule of `regime-env`: a rewritten helper stops the caller). It binds a stream socket at `<socket path>` (mode
0600; a path that is taken refuses, one listener per Router launch), prints `acp-broker: listening on <socket path>`
once, and per accepted connection starts the handler argv (`/bin/bash <acp-broker> --connection <seats-root> <router
seat> <router scratch cwd>`) with the connection as the handler's stdin and stdout through two pipes, copying bytes
both ways until either side closes: the connection's bytes to the handler's stdin (the header line, then the ACP
stream omp reads), the handler's stdout to the connection (the refusal line, or omp's stream and the `omp acp exit
<status>` trailer). It interprets nothing: the header grammar, the settings, the canary, the launch and the log are
the handler's. When the client closes its side the handler's stdin closes, so omp sees EOF; when the client is gone
the handler's output is drained until it exits, so the handler never dies on a broken pipe before it removes its slot.
A hangup, interrupt or termination closes the listener, terminates every live handler (whose own trap ends its omp
and removes its slot) and waits for each, then removes the socket; the directory is `acp-broker`'s to remove. The
handlers of the three signals are installed before the socket is bound (regime-cutover U447: `acp-broker`'s trap
sends TERM here the moment its own signal arrives, and a TERM between the bind and the handlers' installation ended
this process by the default disposition with the socket bound, which the broker then read as another broker's), so
a signal at any instant after the pin check ends this process through that one path: during the bind or the listen
it only sets the flag, no readiness line is printed, and the start-up ends through the stop with the socket removed.
Exit 0 when the socket is gone, 2 when it remains or a refusal happened (every reason on stderr), and nothing else is
written anywhere. The standard library alone, under `-I -S`: no site packages, no `PYTHON*` variable, no script
directory on the path.
"""

import hashlib
import os
import re
import signal
import socket
import subprocess
import sys
import threading

LEVER = "acp-relay.py"
MAPPING_KEY = re.compile(r"^(\S+):$")
LEVER_PIN = re.compile(r"^(\S+): ([0-9a-f]{64})$")
LEVERS_KEYS = ("claude", "levers", "sha256")
CHUNK = 65536
# A handler is given this long after SIGTERM to end its omp and remove its slot before the relay stops waiting.
STOP_GRACE = 30.0


def refuse(reason):
    """Print the refusal in the shell levers' words on stderr and exit 2."""
    print(f"{LEVER}: refused: {reason}", file=sys.stderr)
    sys.exit(2)


def manifest_pin(lines, manifest):
    """The sha256 pinned for this file under the manifest's `claude.levers.sha256` block, read as text by
    indentation alone (the rule of `brief-check.py`): the top-level `claude:` mapping, its `levers:` key, its
    `sha256:` key, then one pin line per lever at one indentation. None or two pins is a refusal."""
    depth = 0
    indents = []
    pins = []
    pin_indent = None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()
        while indents and indent <= indents[-1]:
            indents.pop()
            depth -= 1
        if depth == len(LEVERS_KEYS):
            if pin_indent is None:
                pin_indent = indent
            if indent != pin_indent:
                break
            match = LEVER_PIN.match(text)
            if match is None:
                refuse(f"the levers block of {manifest} holds a line that is no pin: {text!r}")
            if match.group(1) == LEVER:
                pins.append(match.group(2))
            continue
        match = MAPPING_KEY.match(text)
        if match is not None and depth < len(LEVERS_KEYS) and match.group(1) == LEVERS_KEYS[depth]:
            indents.append(indent)
            depth += 1
            continue
        if depth > 0 and indent > indents[-1]:
            continue
    if depth < len(LEVERS_KEYS) and not pins:
        refuse(f"no claude.levers.sha256 block in {manifest}")
    if len(pins) != 1:
        refuse(f"no single sha256 pin for {LEVER} in {manifest}")
    return pins[0]


def lever_self_check():
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31): the
    deployed `~/.agents/agent-config.yaml` when this file's physical directory is the physical `~/.local/bin/common`,
    else the checkout's `home/dot_agents/agent-config.yaml` two levels up. Every read is checked (standing order
    21)."""
    directory = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
    self_path = os.path.join(directory, os.path.basename(__file__))
    home = os.environ.get("HOME", "")
    if home and os.path.isdir(home) and directory == os.path.realpath(os.path.join(home, ".local/bin/common")):
        manifest = os.path.join(home, ".agents/agent-config.yaml")
    else:
        manifest = os.path.join(directory, "../../home/dot_agents/agent-config.yaml")
    if not os.access(manifest, os.R_OK):
        refuse(f"manifest unreadable: {manifest}")
    try:
        with open(manifest, "rb") as handle:
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError:
        refuse(f"cannot read {manifest}")
    pin = manifest_pin(lines, manifest)
    try:
        with open(self_path, "rb") as handle:
            digest = hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        refuse(f"cannot hash {self_path}")
    if digest != pin:
        refuse(f"sha256 {digest} of {self_path} differs from the pin in {manifest}")


class Relay:
    """One listener, one handler process per connection, two copy threads per handler."""

    def __init__(self, sock_path, handler):
        self.sock_path = sock_path
        self.handler = handler
        self.listener = None
        self.stopping = False
        self.lock = threading.Lock()
        self.children = {}
        self.threads = []

    def serve(self, conn):
        """Start the handler for `conn` and copy bytes both ways until the handler exits; then close `conn`.
        The start and the registration happen under the one lock `stop` takes (verdict U343d-136fbe0a P2 `:250`):
        a stop that began first turns the connection away unstarted, and a handler that was started is in the
        table before `stop` reads it, so no handler escapes the termination."""
        with self.lock:
            if self.stopping:
                child = None
            else:
                try:
                    child = subprocess.Popen(
                        self.handler, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None, close_fds=True
                    )
                except OSError as exc:
                    print(f"{LEVER}: cannot start the connection handler {self.handler[0]}: {exc}", file=sys.stderr)
                    child = None
                else:
                    self.children[child.pid] = child
        if child is None:
            try:
                conn.sendall(b"acp-broker: refused: cannot start the connection handler\n")
            except OSError:
                pass
            conn.close()
            return
        sending = [True]

        def to_child():
            # The connection's bytes to the handler's stdin; the client's close (or loss) closes that stdin, so omp
            # reads EOF.
            try:
                while True:
                    chunk = conn.recv(CHUNK)
                    if not chunk:
                        break
                    child.stdin.write(chunk)
                    child.stdin.flush()
            except OSError:
                pass
            try:
                child.stdin.close()
            except OSError:
                pass

        def to_conn():
            # The handler's stdout to the connection, drained to the end even when the client is gone, so the handler
            # never meets a broken pipe before it has logged the exit and removed its slot.
            while True:
                chunk = child.stdout.read1(CHUNK)
                if not chunk:
                    break
                if sending[0]:
                    try:
                        conn.sendall(chunk)
                    except OSError:
                        sending[0] = False
                        try:
                            child.stdin.close()
                        except OSError:
                            pass
            try:
                conn.shutdown(socket.SHUT_WR)
            except OSError:
                pass

        reader = threading.Thread(target=to_child, daemon=True)
        writer = threading.Thread(target=to_conn, daemon=True)
        reader.start()
        writer.start()
        writer.join()
        child.wait()
        # The handler is gone: the connection ends now, which also releases a reader still waiting on the client.
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        conn.close()
        reader.join()
        with self.lock:
            self.children.pop(child.pid, None)

    def on_signal(self, signum, frame):
        self.stopping = True
        # The listener is set once it accepts: a signal during the bind or the listen closes nothing, and run() reads
        # the flag before the readiness line; a signal in the accept loop makes the retried accept fail at once.
        if self.listener is not None:
            try:
                self.listener.close()
            except OSError:
                pass

    def run(self):
        # The socket is bound by its name from its own directory: a Unix socket path is capped at 104 bytes on macOS
        # (108 on Linux), and `<seats-root>/.state/<router seat>/broker/sock` under a long HOME or seats root exceeds
        # it; the directory is the relay's cwd from here on (every handler enters the task cwd itself).
        directory, base = os.path.split(self.sock_path)
        try:
            os.chdir(directory)
        except OSError as exc:
            refuse(f"cannot enter the broker directory {directory}: {exc}")
        # Armed before the socket exists (regime-cutover U447): from here a HUP, INT or TERM ends this process through
        # stop() and remove_socket(), whichever start-up step it lands in.
        for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            signal.signal(signum, self.on_signal)
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            listener.bind(base)
        except OSError as exc:
            refuse(f"cannot bind the broker socket {self.sock_path}: {exc}")
        try:
            os.chmod(self.sock_path, 0o600)
            listener.listen(16)
        except OSError as exc:
            listener.close()
            self.remove_socket()
            refuse(f"cannot listen on the broker socket {self.sock_path}: {exc}")
        self.listener = listener
        # The readiness line is the last start-up step and the one readiness sign (hcom-seat reads it through its
        # FIFO, the test fixture from the broker's stdout): a signal that already arrived leaves no line.
        if not self.stopping:
            print(f"acp-broker: listening on {self.sock_path}", flush=True)
        while not self.stopping:
            try:
                conn, _ = self.listener.accept()
            except OSError:
                # The listener was closed by the signal handler, or accept failed: either way the relay ends.
                break
            thread = threading.Thread(target=self.serve, args=(conn,), daemon=True)
            thread.start()
            self.threads.append(thread)
        self.stop()
        return 0 if self.remove_socket() else 2

    def stop(self):
        """Terminate every live handler and wait for each: its trap ends omp, logs the exit and removes its slot.
        The stopping flag is set under the lock before the table is read, so a `serve` that passed the flag has
        its handler in the table."""
        try:
            self.listener.close()
        except OSError:
            pass
        with self.lock:
            self.stopping = True
            children = list(self.children.values())
        for child in children:
            try:
                child.terminate()
            except OSError:
                pass
        for child in children:
            try:
                child.wait(timeout=STOP_GRACE)
            except subprocess.TimeoutExpired:
                print(
                    f"{LEVER}: a connection handler (pid {child.pid}) did not end within {STOP_GRACE:.0f} s",
                    file=sys.stderr,
                )
                child.kill()
                child.wait()
        for thread in self.threads:
            thread.join(timeout=STOP_GRACE)

    def remove_socket(self):
        """Remove the socket file; True when it is gone (an absence is read from the error, standing order 21)."""
        try:
            os.unlink(self.sock_path)
        except FileNotFoundError:
            pass
        except OSError as exc:
            print(f"{LEVER}: cannot remove the broker socket {self.sock_path}: {exc}", file=sys.stderr)
        if os.path.lexists(self.sock_path):
            print(f"{LEVER}: the broker socket {self.sock_path} remains after its removal", file=sys.stderr)
            return False
        return True


def main(argv):
    lever_self_check()
    if len(argv) < 4 or argv[2] != "--":
        refuse("usage: acp-relay.py <socket path> -- <handler argv...>")
    sock_path = argv[1]
    handler = argv[3:]
    if not os.path.isabs(sock_path):
        refuse(f"the socket path {sock_path!r} is not absolute")
    if not os.path.isabs(handler[0]):
        refuse(f"the handler {handler[0]!r} is not an absolute path")
    return Relay(sock_path, handler).run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
