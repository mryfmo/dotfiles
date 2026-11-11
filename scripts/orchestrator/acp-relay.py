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
The flag's read and the readiness line are one step under the three signals blocked (regime-cutover U447b), so the
line is printed only when no signal has been handled, and a signal sent meanwhile is delivered after the line and
ends this process as any later one does; a line never follows the listener's closure.
Exit 0 when the socket is gone, 2 when it remains or a refusal happened (every reason on stderr), and nothing else is
written anywhere. The standard library alone, under `-I -S`: no site packages, no `PYTHON*` variable, no script
directory on the path.

The second entry point, `python3 -I -S acp-relay.py --map-session-cwd <task> -- <command...>` (regime-cutover U449b,
table row s22; U449's trace): the connection handler runs it inside the worker's sandbox in place of the bare `omp acp`
command, after the same self-check. dsh-subagent-acp names the Router's own task directory as the ACP `session/new`
cwd, a directory the worker's settings deny by design (R-45), so Claude Code died at its spawn there; the broker's side,
which owns the slot's task, maps that one field onto it before omp reads the request. The mapper starts the command
with a pipe for its stdin and the command's stdout as its own (the connection, untouched), copies its stdin to the
command line by line, and rewrites exactly one shape (`map_session_cwd`): a JSON object whose `method` is `session/new`
and whose `params.cwd` is a string. The rewrite is textual (regime-cutover U449c, verdict U449-6017f53f): a scanner
over the line (json.JSONDecoder.raw_decode member by member at the top level and inside `params`, after a streaming
count of the nesting against NESTING_CAP) locates the cwd string token, and that token alone is replaced by the task,
JSON-quoted; every other byte of the line, the spacing, the key order, an escaped method, a lone surrogate or a number
beyond a double in another field, the terminator, stays as the Router sent it (the earlier re-serialisation changed
those bytes, raised on a lone surrogate and wrote `Infinity` for a huge number). The mapper is total: whenever the line
is not that shape (no cwd, a non-string cwd, no params object, another method, a JSON value that is no object), is not
valid JSON or not UTF-8, is nested beyond NESTING_CAP, repeats a key at either level, carries bytes after the object or
is longer than LINE_CAP, and whenever anything inside raises, the line passes through byte for byte; the copier forwards
every line it read, the mapped line or the original, and a record that cannot be written costs no line. Each mapping is
recorded on stderr as `acp-relay.py: session cwd <original, JSON-quoted> mapped to <task>`; the handler gives the
launch's stderr a file in the slot and its reaper carries the record into the launch log when omp has ended (an
inherited descriptor does not survive srt, measured for U449b: fd 6 is closed in the sandboxed child, so stderr is the
one channel besides the stream). The command's stderr is a pipe the mapper drains onto the same stderr, with a line that
would begin like the record prefixed `omp: `, so no worker line can be read as the record. The mapper ends when its
stdin ends (the command's stdin closed, so omp reads EOF) or the command exits, and exits with the command's status
(128 plus the signal number when a signal ended it).
"""

import hashlib
import json
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
# A stream line longer than this passes through unparsed, in pieces: the mapper holds no more of the Router's bytes.
LINE_CAP = 1 << 20
RECORD_PREFIX = b"acp-relay.py: session cwd "
# A line that opens more arrays and objects inside one another than this passes through unparsed (a `session/new` is
# five deep): the streaming bound that keeps the parser's recursion out of the copier.
NESTING_CAP = 64
# One JSON string token (the unrolled form: no alternation under a repeat) or one bracket, for the nesting count.
JSON_TOKEN = re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"|[\[{\]}]')
JSON_SPACE = re.compile(r"[ \t\n\r]*")
# A handler is given this long after SIGTERM to end its omp and remove its slot before the relay stops waiting.
STOP_GRACE = 30.0
# The signals that end the relay: handled from before the bind, blocked across the readiness line's print.
STOP_SIGNALS = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)


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
        for signum in STOP_SIGNALS:
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
        # FIFO, the test fixture from the broker's stdout). The flag's read, the print and the flush are one step
        # with the three signals blocked (regime-cutover U447b, verdict U447-a52a1452 P1): a signal that already
        # arrived leaves no line, and one sent meanwhile is delivered at the unblock and ends this process as any
        # post-readiness signal does, so a line never follows the listener's closure.
        signal.pthread_sigmask(signal.SIG_BLOCK, STOP_SIGNALS)
        if not self.stopping:
            print(f"acp-broker: listening on {self.sock_path}", flush=True)
        signal.pthread_sigmask(signal.SIG_UNBLOCK, STOP_SIGNALS)
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


def nesting_exceeds(text, cap):
    """True when the JSON text opens more than `cap` arrays and objects inside one another: a count of the brackets
    outside the string tokens, streamed over the text, never a parse."""
    depth = 0
    for match in JSON_TOKEN.finditer(text):
        token = match.group()
        if token[0] == '"':
            continue
        if token in "[{":
            depth += 1
            if depth > cap:
                return True
        elif depth:
            depth -= 1
    return False


def object_members(text, start):
    """The members of the JSON object at `start` (after any whitespace) as (key, value, value start, value end) and
    the index after its closing brace; ValueError when no object is there (IndexError at the text's end)."""
    decoder = json.JSONDecoder()
    members = []
    i = JSON_SPACE.match(text, start).end()
    if text[i] != "{":
        raise ValueError("no object")
    i = JSON_SPACE.match(text, i + 1).end()
    if text[i] == "}":
        return members, i + 1
    while True:
        if text[i] != '"':
            raise ValueError("no key")
        key, i = decoder.raw_decode(text, i)
        i = JSON_SPACE.match(text, i).end()
        if text[i] != ":":
            raise ValueError("no colon")
        i = JSON_SPACE.match(text, i + 1).end()
        value, end = decoder.raw_decode(text, i)
        members.append((key, value, i, end))
        i = JSON_SPACE.match(text, end).end()
        if text[i] == ",":
            i = JSON_SPACE.match(text, i + 1).end()
            continue
        if text[i] == "}":
            return members, i + 1
        raise ValueError("no comma")


def member_spans(members):
    """{key: (value, value start, value end)}; ValueError on a repeated key (JSON.parse keeps the last; the shape
    is ambiguous and this lever maps neither)."""
    spans = {}
    for key, value, start, end in members:
        if key in spans:
            raise ValueError("repeated key")
        spans[key] = (value, start, end)
    return spans


def map_session_cwd(line, task):
    """The one mapping of the stream (regime-cutover U449b): (the line to pass on, the original cwd or None). A JSON
    object whose `method` is `session/new` and whose `params.cwd` is a string becomes the same bytes with the cwd
    string token alone replaced by `task`, JSON-quoted (regime-cutover U449c: a textual substitution at the token's
    position, so the spacing, the key order and every other field stay byte for byte, a lone surrogate or a huge
    number elsewhere included); every other line is returned as it is, with None. Total: the parse is bounded
    (NESTING_CAP, LINE_CAP) and whatever raises inside yields the identity."""
    try:
        if len(line) > LINE_CAP:
            return line, None
        body = line
        end = b""
        for terminator in (b"\r\n", b"\n"):
            if body.endswith(terminator):
                end = terminator
                body = body[: -len(terminator)]
                break
        text = body.decode("utf-8")
        if nesting_exceeds(text, NESTING_CAP):
            return line, None
        members, after = object_members(text, 0)
        if JSON_SPACE.match(text, after).end() != len(text):
            return line, None
        top = member_spans(members)
        if "method" not in top or "params" not in top:
            return line, None
        method = top["method"][0]
        if method != "session/new":  # lint-comparisons: allow a JSON-RPC method name, not a path
            return line, None
        if not isinstance(top["params"][0], dict):
            return line, None
        _params, params_start, params_end = top["params"]
        inner, inner_end = object_members(text, params_start)
        if inner_end != params_end:
            return line, None
        params = member_spans(inner)
        if "cwd" not in params or not isinstance(params["cwd"][0], str):
            return line, None
        original, cwd_start, cwd_end = params["cwd"]
        mapped = text[:cwd_start] + json.dumps(task) + text[cwd_end:]
        return mapped.encode("utf-8") + end, original
    except Exception:  # the mapper is total: a line the scan or the parse cannot take passes as it came
        return line, None


class MapperStderr:
    """This process's stderr under one lock, shared by the record and the command's forwarded stderr: a record
    always starts a line (a newline closes a forwarded piece that did not end with one), and a forwarded line that
    begins like the record is prefixed `omp: `, so the reaper's read of the launch's stderr file takes the mapper's
    lines alone as records."""

    def __init__(self):
        self.out = sys.stderr.buffer
        self.lock = threading.Lock()
        self.at_start = True

    def forward(self, piece):
        with self.lock:
            if self.at_start and piece.startswith(RECORD_PREFIX):
                self.out.write(b"omp: ")
            self.out.write(piece)
            self.out.flush()
            self.at_start = piece.endswith(b"\n")

    def record(self, original, task):
        with self.lock:
            if not self.at_start:
                self.out.write(b"\n")
            self.out.write(RECORD_PREFIX + json.dumps(original).encode() + f" mapped to {task}\n".encode())
            self.out.flush()
            self.at_start = True


def forward_stderr(pipe, stderr):
    """Copy the command's stderr to `stderr` (MapperStderr), line by line, LINE_CAP pieces for a longer line."""
    try:
        while True:
            piece = pipe.readline(LINE_CAP)
            if not piece:
                break
            stderr.forward(piece)
    except (OSError, ValueError):
        pass


def map_session_cwd_run(task, command):
    """The `--map-session-cwd` entry: run `command` with a pipe for its stdin, copy this process's stdin to it with
    `map_session_cwd` over every whole line (a line beyond LINE_CAP passes through in pieces, unparsed), record each
    mapping on stderr, drain the command's stderr through forward_stderr, and end with the command's status."""
    try:
        child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=None, stderr=subprocess.PIPE, close_fds=True)
    except OSError as exc:
        refuse(f"cannot start {command[0]}: {exc}")
    stderr = MapperStderr()
    drain = threading.Thread(target=forward_stderr, args=(child.stderr, stderr), daemon=True)
    drain.start()

    def copy_stdin():
        source = sys.stdin.buffer
        mid_line = False
        try:
            while True:
                piece = source.readline(LINE_CAP)
                if not piece:
                    break
                whole = piece.endswith(b"\n")
                out = piece
                if not mid_line and (whole or len(piece) < LINE_CAP):
                    out, original = map_session_cwd(piece, task)
                    if original is not None:
                        try:
                            stderr.record(original, task)
                        except Exception:  # a record that cannot be written costs no line of the stream
                            pass
                mid_line = not whole
                child.stdin.write(out)
                child.stdin.flush()
        except Exception:  # the command's stdin is gone (omp exited) or this process's stdin failed: the copy ends
            pass
        finally:
            try:
                child.stdin.close()
            except OSError:
                pass

    copier = threading.Thread(target=copy_stdin, daemon=True)
    copier.start()
    status = child.wait()
    # The copier may still sit in a read of a stdin nobody has closed: the command is gone, so this process ends now.
    drain.join(2.0)
    sys.stderr.flush()
    if status < 0:
        return 128 - status
    return status


def main(argv):
    lever_self_check()
    if len(argv) >= 4 and argv[1] == "--map-session-cwd" and argv[3] == "--":
        task = argv[2]
        command = argv[4:]
        if not os.path.isabs(task):
            refuse(f"the task {task!r} is not an absolute path")
        if not command or not os.path.isabs(command[0]):
            refuse(f"the command {command[:1]!r} is not an absolute path")
        return map_session_cwd_run(task, command)
    if len(argv) < 4 or argv[2] != "--":
        refuse("usage: acp-relay.py <socket path> -- <handler argv...> | --map-session-cwd <task> -- <command...>")
    sock_path = argv[1]
    handler = argv[3:]
    if not os.path.isabs(sock_path):
        refuse(f"the socket path {sock_path!r} is not absolute")
    if not os.path.isabs(handler[0]):
        refuse(f"the handler {handler[0]!r} is not an absolute path")
    return Relay(sock_path, handler).run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
