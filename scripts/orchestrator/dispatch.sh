#!/usr/bin/env bash
# @file dispatch.sh
# @brief Send one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING line after checking its sha256 fields, and record it.
# @description
#   Plan 007 T718 (C-20). Reads exactly one physical line from a file (a second
#   line, blank or not, is refused). Every `<name>_sha256=<64 hex>` token is
#   recomputed from the file its sibling token names, `<name>_file=` or else
#   `<name>=` (`task_sha256` from `task_file=`, `design_sha256` from `design=`,
#   `amended_task_sha256` from `amended_task=`); an AGMSG-TASK line must carry
#   `task_file=` and `task_sha256=`. A relative path is read from the root of
#   the checkout this script lives in (`git rev-parse --show-toplevel` there),
#   never from the caller's directory. A missing field or file, a malformed value
#   or a mismatch exits 1 naming the field, and nothing is sent. Otherwise the
#   line goes to `agmsg-dispatch` as one argument, byte for byte.
#   With an acceptance record, the record is checked before the send and, once
#   the line is on the bus, `<the line> read_at=<read|unread>` is appended to
#   the `dispatch` list of
#   the record's JSON block, the object between its first two `---` lines. The
#   block is read and written with Python's standard json (a duplicate key, NaN
#   or Infinity is refused; `sort_keys`, `indent=2`); the key is created when
#   absent, and a record without a block, or a missing record file, gets a block
#   holding only `dispatch`. The prose after the block is kept byte for byte.
#   The read state is the marker `history.sh <team> <to> 200` prints for that
#   message (`●` unread, `○` read): agmsg's scripts expose no read_at time, and
#   this script never reads the message database.
# @arg $1 string agmsg team.
# @arg $2 string Sender identity.
# @arg $3 string Recipient identity.
# @arg $4 string Recipient pane id (for example `w5:pA`).
# @arg $5 path File holding the line.
# @arg $6 path Optional acceptance record (`.orchestration/acceptance/<task>.md`), relative to the current directory.
# @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
# @exitcode 0 Sent, and recorded when a record was given (agmsg-dispatch's own status otherwise).
# @exitcode 1 A field check failed, the record is malformed, or the sent line was not recorded.
# @exitcode 2 Usage error, or the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line.
# @example
#   scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot claude-standard-dot-a003 w5:pA \
#     "$TMPDIR/task-line.txt" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01.md
set -euo pipefail

usage() {
    echo "usage: dispatch.sh <team> <from> <to> <pane> <line-file> [<acceptance-record>]" >&2
    exit 2
}
(($# == 5 || $# == 6)) || usage
team=$1 from=$2 to=$3 pane=$4 file=$5 record=${6:-}
[[ -f ${file} ]] || usage
# The sentinel keeps every trailing newline, which $( ) alone would drop (thread 4254107304).
line="$(cat -- "${file}" && printf x)" && line=${line%x} && line=${line%$'\n'}
[[ ${line} != *$'\n'* ]] || {
    echo "dispatch: ${file} holds more than one line" >&2
    exit 2
}
[[ ${line} =~ ^AGMSG-(TASK|ACCEPTANCE|PING)\ v1\  ]] || {
    echo "dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line" >&2
    exit 2
}
root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"

read -ra tokens <<< "${line}"
# @description Print the value of the first `<key>=` token, or fail.
# @arg $1 string Key.
value_of() {
    local t
    for t in "${tokens[@]}"; do
        [[ ${t} == "$1="* ]] && printf '%s' "${t#*=}" && return 0
    done
    return 1
}
# Thread 4254163604: a TASK whose file is not hash-bound is never sent.
if [[ ${line} == "AGMSG-TASK "* ]]; then
    for field in task_file task_sha256; do
        value_of "${field}" > /dev/null || {
            echo "dispatch: an AGMSG-TASK line needs ${field}=" >&2
            exit 1
        }
    done
fi
for t in "${tokens[@]}"; do
    [[ ${t} =~ ^([a-z_]+)_sha256=(.*)$ ]] || continue
    name=${BASH_REMATCH[1]} want=${BASH_REMATCH[2]}
    field="${name}_sha256"
    [[ ${want} =~ ^[0-9a-f]{64}$ ]] || {
        echo "dispatch: ${field} is not 64 lowercase hex digits" >&2
        exit 1
    }
    path="$(value_of "${name}_file" || value_of "${name}")" || {
        echo "dispatch: ${field} has no ${name}_file= or ${name}= field naming its file" >&2
        exit 1
    }
    [[ ${path} == /* ]] || path="${root}/${path}"
    [[ -f ${path} ]] || {
        echo "dispatch: ${field}: ${path} does not exist" >&2
        exit 1
    }
    got="$(shasum -a 256 "${path}")" && got=${got%% *}
    [[ ${got} == "${want}" ]] || {
        echo "dispatch: ${field} mismatch: the line has ${want}, ${path} hashes to ${got}" >&2
        exit 1
    }
done
[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"

# Modes: `check` parses the record; `append` finds the sent line in history.sh's
# output on stdin, takes its read marker (● unread, ○ read) and appends it.
read -r -d '' recorder << 'PY' || true
import json, re, sys
from pathlib import Path

mode, path, line, sender, to = sys.argv[1:6]
record = Path(path)

def refuse(pairs):
    keys = [k for k, _ in pairs]
    dup = next((k for k in keys if keys.count(k) > 1), None)
    if dup is not None:
        sys.exit(f"dispatch: {path}: duplicate key {dup}")
    return dict(pairs)

def constant(name):
    sys.exit(f"dispatch: {path}: non-finite number {name}")

text = record.read_text() if record.exists() else ""
block, rest = {}, text
if text.startswith("---\n"):
    end = text.find("\n---\n", 3)
    if end < 0:
        sys.exit(f"dispatch: {path}: the block between the first two --- lines is not closed")
    block = json.loads(text[4:end], object_pairs_hook=refuse, parse_constant=constant)
    rest = text[end + 5:]
    if not isinstance(block, dict):
        sys.exit(f"dispatch: {path}: the block is not a JSON object")
entries = block.setdefault("dispatch", [])
if not isinstance(entries, list):
    sys.exit(f"dispatch: {path}: dispatch is not a list")
if mode == "check":
    sys.exit(0)
row = re.compile(r"^\s*(\S+)\s+\[[^\]]+\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
marks = [m.group(1) for m in map(row.match, sys.stdin.read().splitlines())
         if m and (m.group(2), m.group(3), m.group(4)) == (sender, to, line)]
if not marks:
    sys.exit(f"dispatch: the sent line is not in the bus history; {path} is unchanged")
entries.append(f"{line} read_at={'read' if marks[-1] == '○' else 'unread'}")
body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
record.write_text(f"---\n{body}\n---\n{rest}")
PY
[[ ${record} == /* ]] || record="${PWD}/${record}"
python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" < /dev/null
rc=0
agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
"${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "${to}" 200 \
    | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}"
exit "${rc}"
