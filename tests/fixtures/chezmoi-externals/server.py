"""A local HTTP server for the chezmoi externals tests: it serves only the URL paths a test registers.

python3 server.py <plan.json> <port-file> listens on 127.0.0.1 at a free port, written to <port-file> once listening.
plan.json maps a URL path to {"file": <absolute path of the body>, "plan": [behaviour, ...]}. The request path is
looked up in that mapping as an exact string and never touches the filesystem, so `..`, an encoded path or any
unregistered path gets a 404. Each request for a path takes the next behaviour of its plan (the last repeats):
- "ok": the whole body, with its Content-Length.
- "truncate": the body's full Content-Length, then half of its bytes and a closed connection, as a dropped transfer
  looks to a client (Go: unexpected EOF; curl: exit 18).
- "corrupt": a complete response of the same length whose bytes differ from the body's, as a wrong archive looks.
- "503": an HTTP 503 with no body.
Every request is appended to the file named by plan.json's "log" key as one line, its path; the requests already
logged for a path decide which behaviour comes next, so removing the log starts every plan again.
"""

import http.server
import json
import sys
from pathlib import Path

PLAN, PORT_FILE = (Path(arg) for arg in sys.argv[1:3])


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        config = json.loads(PLAN.read_text())
        log_path = Path(config["log"])
        count = log_path.read_text().splitlines().count(self.path) if log_path.exists() else 0
        with log_path.open("a") as log:
            log.write(self.path + "\n")
        route = config.get("paths", {}).get(self.path)
        if route is None:
            self.respond(404)
            return
        behaviour = route["plan"][min(count, len(route["plan"]) - 1)]
        if behaviour == "503":
            self.respond(503)
            return
        body = Path(route["file"]).read_bytes()
        if behaviour == "corrupt":
            body = bytes(byte ^ 0xFF for byte in body)
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if behaviour == "truncate":
            self.wfile.write(body[: len(body) // 2])
            self.wfile.flush()
            self.close_connection = True
            self.connection.shutdown(2)
            return
        self.wfile.write(body)

    def respond(self, status: int) -> None:
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, *_: object) -> None:
        pass


server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
PORT_FILE.write_text(str(server.server_address[1]))
server.serve_forever()
