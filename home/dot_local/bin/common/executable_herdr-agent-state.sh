#!/bin/sh
# @file herdr-agent-state.sh
# @brief Report a Claude SessionStart to the fixed Herdr socket.
# @arg $1 path Absolute Python interpreter.
# @arg $2 string Action, currently session.
# @arg $3 string Herdr pane identity.
# @arg $4 path Herdr Unix socket.
set -eu
python="$1"
shift
exec "$python" -I -c '
import json, socket, sys, time
action, pane, address = sys.argv[1:]
event = json.load(sys.stdin)
if action != "session" or not pane or not address or event.get("hook_event_name") != "SessionStart":
    raise SystemExit(0)
if event.get("agent_id") or "cursor_version" in event or not isinstance(event.get("session_id"), str) or not event["session_id"]:
    raise SystemExit(0)
params = dict(pane_id=pane, source="herdr:claude", agent="claude", seq=time.time_ns(), agent_session_id=event["session_id"])
for source, target in (("transcript_path", "agent_session_path"), ("source", "session_start_source")):
    if isinstance(event.get(source), str) and event[source]:
        params[target] = event[source]
request = dict(id="herdr:claude:" + str(time.time_ns()), method="pane.report_agent_session", params=params)
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.settimeout(0.5)
    client.connect(address)
    client.sendall((json.dumps(request) + "\n").encode())
    client.recv(4096)
' "$@"
