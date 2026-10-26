"""A local HTTP server for the chezmoi externals tests: each request for a path takes the next behaviour in its plan.

python3 server.py <root> <plan.json> <port-file> serves files under <root> on 127.0.0.1 at a free port, written to
<port-file> once listening. plan.json maps a URL path to a list of behaviours, one per request in order (the last
repeats):
- "ok": the whole file, with its Content-Length.
- "truncate": the file's full Content-Length, then half of its bytes and a closed connection, as a dropped transfer
  looks to a client (Go: unexpected EOF; curl: exit 18).
- "corrupt": a complete response of the same length whose bytes differ from the file's, as a wrong archive looks.
- "503": an HTTP 503 with no body.
Every request is appended to <root>/requests.log as one line, its path; the requests already logged for a path decide
which behaviour comes next, so removing the log starts every plan again.
"""

import http.server
import json
import sys
from pathlib import Path

ROOT, PLAN, PORT_FILE = (Path(arg) for arg in sys.argv[1:4])


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        log_path = ROOT / "requests.log"
        count = log_path.read_text().splitlines().count(self.path) if log_path.exists() else 0
        with log_path.open("a") as log:
            log.write(self.path + "\n")
        plan = json.loads(PLAN.read_text()).get(self.path, ["ok"])
        behaviour = plan[min(count, len(plan) - 1)]
        target = ROOT / self.path.lstrip("/")
        if behaviour == "503" or not target.is_file():
            self.send_response(503 if behaviour == "503" else 404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        body = target.read_bytes()
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

    def log_message(self, *_: object) -> None:
        pass


server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
PORT_FILE.write_text(str(server.server_address[1]))
server.serve_forever()
