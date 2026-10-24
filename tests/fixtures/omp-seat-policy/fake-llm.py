#!/usr/bin/env python3
"""A fake OpenAI chat-completions endpoint for tests/unit/test_omp_seat_policy.py (U36).

`fake-llm.py <port> <dir>`: binds 127.0.0.1 (port 0 picks one) and prints `listening <port>`. The first turn answers
with one `task` tool call; a turn whose messages already hold a tool result answers `done`. Every request is written to
`<dir>/req-<n>.json`, so the test reads what omp offered the model and the tool result it sent back.
"""

import http.server
import json
import pathlib
import sys

OUT = pathlib.Path(sys.argv[2])
TASK_CALL = {
    "index": 0,
    "id": "call_1",
    "type": "function",
    "function": {
        "name": "task",
        "arguments": json.dumps({"agent": "explore", "tasks": [{"id": "Scout", "description": "scout"}]}),
    },
}


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return None

    def do_POST(self) -> None:
        request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        count = len(list(OUT.glob("req-*.json")))
        (OUT / f"req-{count}.json").write_text(json.dumps(request))
        answered = any(message.get("role") == "tool" for message in request.get("messages", []))
        delta = (
            {"role": "assistant", "content": "done"} if answered else {"role": "assistant", "tool_calls": [TASK_CALL]}
        )
        finish = "stop" if answered else "tool_calls"
        chunks = [
            {"id": "c", "object": "chat.completion.chunk", "choices": [{"index": 0, "delta": delta}]},
            {
                "id": "c",
                "object": "chat.completion.chunk",
                "choices": [{"index": 0, "delta": {}, "finish_reason": finish}],
            },
        ]
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        for chunk in chunks:
            self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
        self.wfile.write(b"data: [DONE]\n\n")


server = http.server.HTTPServer(("127.0.0.1", int(sys.argv[1])), Handler)
print(f"listening {server.server_address[1]}", flush=True)
server.serve_forever()
