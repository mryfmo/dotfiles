#!/bin/bash -p
# @file bus-history.sh
# @brief Print one team's hcom messages as marker rows, or as JSON objects keeping each message's hcom id.
# @description
#   Plan 023 PR C stage 1 (T129 hcom-dispatch bus a02): the bus reader of dispatch.sh, bus-read.sh and
#   regime-counters.sh, through hcom's write-free `events` read (`sqlite3 -readonly` cannot open its idle WAL store).
#   The team is hcom-dispatch's `--thread` label, and the SQL a fixed template into which only the checked team
#   (`^[a-z0-9][a-z0-9-]{0,63}$`) and message id (`^[1-9][0-9]{0,18}$`) go. A row is read (`○`) when every
#   recipient's `instances.last_event_id` is at or past its id, else unread (`●`, also a thread reply naming no
#   recipient, shown `-`). hcom runs only from this checkout's `.agents/worklog/uv-tools/hcom/bin/hcom`, with the
#   sha256 update_hcom_private recorded beside it. The store is the deployed declaration's
#   `assets.hcom.store_relative_path` under the passwd home: hcom's default `.hcom` (HCOM_DIR is never set), resolving
#   inside the declared location, at user_version 18. Every row is checked before any output: a field outside its
#   grammar, or NUL or a str.splitlines() separator in a body, fails the whole read. Children get only
#   PATH=/usr/bin:/bin, HOME (the passwd home), LANG, TMPDIR and UV_CACHE_DIR.
# @arg $1 string Team.
# @option --limit <n> Only the newest n messages.
# @option --json One JSON object per message: id, at, from, to (a list), body, read.
# @option --message-id <id> With --json: exactly that hcom id's message.
# @option --passwd-home <dir> Test fixtures only: the directory standing for the passwd home.
# @env UV_CACHE_DIR The caller's private uv cache, an absolute path; children get it.
# @exitcode 0 Printed.
# @exitcode 1 Refused: hcom binding, an inherited HCOM_DIR, the declaration, store or schema, hcom, or a row.
# @exitcode 2 Usage error, or UV_CACHE_DIR absent or relative.
set -euo pipefail

if [[ -z ${UV_CACHE_DIR:-} || -n ${UV_CACHE_DIR%%/*} ]]; then
    echo "bus-history: UV_CACHE_DIR must be an absolute path" >&2
    exit 2
fi
if [[ -n ${HCOM_DIR:-} ]]; then
    echo "bus-history: refused: an inherited HCOM_DIR names another store" >&2
    exit 1
fi
root="$(cd -P -- "$(/usr/bin/dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
# bash 3.2 keeps here-documents in /tmp, which a sandbox may refuse: the Python below is read from this file instead.
boot='import sys
src = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = src.index(": << \x27PYTHON\x27") + 1
sys.argv = sys.argv[1:]
exec(compile("\n".join(src[start:src.index("PYTHON", start)]), sys.argv[0], "exec"))'
exec /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 TMPDIR="${TMPDIR:-/tmp}" UV_CACHE_DIR="${UV_CACHE_DIR}" /usr/bin/python3 -I -c "${boot}" \
    "${root}/scripts/orchestrator/bus-history.sh" "${root}" "$@"
: << 'PYTHON'
import argparse, hashlib, json, os, pwd, re, stat, subprocess, sys

root, args = sys.argv[1], sys.argv[2:]
TEAM, ID, LIMIT = r"[a-z0-9][a-z0-9-]{0,63}", r"[1-9][0-9]{0,18}", r"[1-9][0-9]{0,8}"
NAME = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")
BREAKS = set("\0\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029")  # NUL and every separator str.splitlines() splits on
READ = ("json_array_length(msg_delivered_to) > 0 AND NOT EXISTS (SELECT 1 FROM json_each(msg_delivered_to) d"
        " LEFT JOIN instances i ON i.name = d.value WHERE COALESCE(i.last_event_id, 0) < events_v.id)")

def refuse(why):
    sys.exit(f"bus-history: {why}")

def usage():
    sys.stderr.write("usage: bus-history.sh [--passwd-home <dir>] <team> [--limit <n>] [--json [--message-id <id>]]\n")
    sys.exit(2)

parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
parser.error = lambda message: usage()
for flag in ("--limit", "--message-id", "--passwd-home"):
    parser.add_argument(flag)
parser.add_argument("--json", action="store_true")
parser.add_argument("team")
a = parser.parse_args(args)
team, as_json, home = a.team, a.json, a.passwd_home
checks = ((TEAM, team), (LIMIT, a.limit or "1"), (ID, a.message_id or "1"))
if not all(re.fullmatch(p, v) for p, v in checks) or (a.message_id and not as_json):
    usage()
if home is not None and not (home.startswith("/") and os.path.isdir(home)):
    usage()
limit, mid = int(a.limit) if a.limit else None, int(a.message_id) if a.message_id else None
home = home or pwd.getpwuid(os.getuid()).pw_dir

def store():
    """The declared store directory, after the declaration, path and header checks."""
    path = os.path.join(home, ".agents/agent-config.yaml")
    try:
        if not stat.S_ISREG(os.lstat(path).st_mode):
            refuse(f"the declaration {path} is not a regular file")
        lines = open(path, encoding="utf-8").read().split("\n")
    except (OSError, UnicodeError):
        refuse(f"no readable declaration at {path}")
    # The one key at assets: (column 0) > hcom: (column 2) > store_relative_path: (column 4), each exactly once.
    found, block = [], None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            block = "assets" if line == "assets:" else None
        elif block and indent == 2:
            block = "hcom" if line == "  hcom:" else "assets"
        elif block == "hcom" and indent == 4 and line.startswith("    store_relative_path:"):
            found.append(line.split(":", 1)[1].strip())
    if len(found) != 1:
        refuse(f"{path} declares assets.hcom.store_relative_path {len(found)} times, not once")
    rel = found[0].strip("'\"") if found[0][:1] in "'\"" and found[0][-1:] == found[0][:1] else found[0]
    if not re.fullmatch(r"[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*", rel) or os.path.normpath(rel) != rel or ".." in rel.split("/"):
        refuse(f"the declared store {rel!r} is not a normalized path under the passwd home")
    if rel != ".hcom":  # item 0: hcom's own default; this reader never sets HCOM_DIR to point it elsewhere
        refuse(f"the declared store {rel} is not hcom's default .hcom")
    directory, real = os.path.join(home, rel), os.path.join(os.path.realpath(home), rel)
    db = os.path.join(directory, "hcom.db")
    try:
        ok = os.path.realpath(directory) == real and os.path.isdir(real) and stat.S_ISREG(os.lstat(db).st_mode)
        ok = ok and os.path.realpath(db) == os.path.join(real, "hcom.db")
        with open(db, "rb") as f:
            head = f.read(100)
    except OSError:
        ok = False
    if not ok:
        refuse(f"the store {directory} is absent or resolves outside the declared location")
    if head[:16] != b"SQLite format 3\0" or int.from_bytes(head[60:64], "big") != 18:
        refuse(f"{db} is not an hcom store at schema revision 18")

def hcom():
    """The verified private hcom entry of this checkout."""
    entry = os.path.join(root, ".agents/worklog/uv-tools/hcom/bin/hcom")
    try:
        regular = stat.S_ISREG(os.lstat(entry).st_mode)
        want = open(entry + ".sha256", encoding="ascii").read().strip()
        got = hashlib.sha256(open(entry, "rb").read()).hexdigest()
    except (OSError, UnicodeError):
        regular, want, got = False, "", None
    if not regular or not re.fullmatch(r"[0-9a-f]{64}", want) or got != want:
        refuse("refused: hcom binding")
    return entry

def events(entry, sql, last):
    env = {"PATH": "/usr/bin:/bin", "HOME": home, "LANG": "C.UTF-8", "TMPDIR": os.environ["TMPDIR"],
           "UV_CACHE_DIR": os.environ["UV_CACHE_DIR"]}
    argv = [entry, "events", "--type", "message", "--full", "--last", str(last), "--sql", sql]
    run = subprocess.run(argv, env=env, cwd="/", stdin=subprocess.DEVNULL, capture_output=True, timeout=120)
    if run.returncode:
        refuse(f"hcom events exited {run.returncode}")
    rows = []
    for line in run.stdout.decode("utf-8", "replace").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except ValueError:
                refuse("hcom events printed a line that is not one JSON object")
    return rows

def row(event):
    """The checked fields of one message event, or a refusal of the whole read."""
    data = event.get("data") if isinstance(event, dict) else None
    eid, ts = event.get("id") if data else None, event.get("ts") if data else None
    if not isinstance(eid, int) or isinstance(eid, bool) or eid < 1 or event.get("type") != "message":
        refuse("a message event without an hcom id")
    if not isinstance(ts, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d{1,9})?\+00:00", ts):
        refuse(f"message {eid}: its time is not UTC ISO-8601")
    sender, to, body = data.get("from"), data.get("delivered_to"), data.get("text")
    names = [sender] + (to if isinstance(to, list) else [None])  # a worker's thread reply may name no recipient
    if not all(isinstance(n, str) and NAME.match(n) for n in names) or data.get("thread") != team:
        refuse(f"message {eid}: a sender, recipient or thread outside the grammar")
    if not isinstance(body, str) or BREAKS & set(body):
        refuse(f"message {eid}: its body holds NUL or a line separator")
    return {"id": eid, "at": ts[:19] + "Z", "from": sender, "to": to, "body": body}

store()
entry = hcom()
where = f"msg_thread = '{team}'" + (f" AND id = {mid}" if mid else "")
last = 2 if mid else limit or 10**9
rows = [row(e) for e in events(entry, where, last)]
read = {row(e)["id"] for e in events(entry, f"{where} AND {READ}", last)}
if mid and len(rows) != 1:
    refuse(f"no message {mid} in the team {team}")
out = []
for r in sorted(rows, key=lambda r: r["id"]):
    r["read"] = r["id"] in read
    if as_json:
        out.append(json.dumps(r, ensure_ascii=False, sort_keys=True))
    else:
        out.append(f"{'○' if r['read'] else '●'} [{r['at']}] {r['from']} → {','.join(r['to']) or '-'}: {r['body']}")
sys.stdout.write("".join(line + "\n" for line in out))
PYTHON
