#!/usr/bin/env bash
# @file dispatch.sh
# @brief Send one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING line after checking its sha256 fields, and record it.
# @description
#   Plan 007 T718 (C-20). Reads exactly one physical line from a file (a second
#   line, blank or not, or a NUL byte is refused). Every `<name>_sha256=<64
#   hex>` token is recomputed from the file its sibling token names,
#   `<name>_file=` or else `<name>=` (`task_sha256` from `task_file=`,
#   `design_sha256` from `design=`, `amended_task_sha256` from `amended_task=`;
#   a line naming the file both ways, or repeating one of these keys, is
#   refused), except a `previous_<name>_sha256=` reference to an earlier
#   version, which is checked as 64 lowercase hex only; every line must carry
#   exactly one non-empty `task_id=`, and an AGMSG-TASK line must carry
#   `task_file=` and `task_sha256=`. A relative path is read from the root of
#   the checkout this script lives in (`git rev-parse --show-toplevel` there),
#   never from the caller's directory. A missing field or file, a malformed value
#   or a mismatch exits 1 naming the field, and nothing is sent. Otherwise the
#   line goes to `agmsg-dispatch` as one argument, byte for byte.
#   With an acceptance record, the record is checked before the send and, once
#   the line is on the bus, `<the line> read_at=<read|unread>` is appended to
#   the `dispatch` list of
#   the record's JSON block, the object between its first two `---` lines. The
#   block is read and written with Python's standard json (malformed JSON, a
#   duplicate key, NaN or Infinity, a block that is not an object or a
#   `dispatch` that is not a list is refused; `sort_keys`, `indent=2`); the key
#   is created when absent, and a record without a block gets a block holding
#   only `dispatch`. The prose after the block is kept byte for byte, and the
#   record is replaced atomically (a temporary file in its directory, fsync,
#   rename). A record that is not an existing regular file writable in a
#   writable directory, or whose `task` is not the line's `task_id`, is refused
#   before the send, and nothing is sent.
#   Only a bus row this send created is recorded: the rows matching the line,
#   sender and recipient are counted before and after the send, and a send that
#   added none leaves the record unchanged and exits 1. The read state is the
#   marker the team-wide `history.sh <team> "" 100000` prints for the new row
#   (`●` unread, `○` read): agmsg's scripts expose no read_at time, this script
#   never reads the message database, and it never passes an agent to
#   history.sh, whose agent argument renames the caller's pane after it.
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
# Thread 4256541716: command substitution drops a NUL byte, so the line sent would not be the file's.
if (($(tr -d '\0' < "${file}" | wc -c) != $(wc -c < "${file}"))); then
    echo "dispatch: ${file} holds a NUL byte" >&2
    exit 2
fi
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
# @description Print how many tokens carry `<key>=`.
# @arg $1 string Key.
count_of() {
    local t n=0
    for t in "${tokens[@]}"; do
        [[ ${t} == "$1="* ]] && n=$((n + 1))
    done
    printf '%s' "${n}"
}
# Thread 4254893065: every message names exactly one task, before any hash or record work.
if (($(count_of task_id) != 1)) || [[ -z "$(value_of task_id)" ]]; then
    echo "dispatch: the line needs exactly one non-empty task_id=" >&2
    exit 1
fi
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
    # Thread 4254771302: any name before _sha256=, digits included (a02_expected_sha256=).
    [[ ${t} =~ ^([^=]+)_sha256=(.*)$ ]] || continue
    name=${BASH_REMATCH[1]} want=${BASH_REMATCH[2]}
    field="${name}_sha256"
    [[ ${want} =~ ^[0-9a-f]{64}$ ]] || {
        echo "dispatch: ${field} is not 64 lowercase hex digits" >&2
        exit 1
    }
    # Thread 4256541725: a previous_<name>_sha256= reference names no file here (a02 item 4's grammar row).
    if [[ ${name} == previous_* ]]; then
        continue
    fi
    # Thread 4254494989: a repeated key leaves a second, unhashed value in the line.
    for key in "${field}" "${name}_file" "${name}"; do
        (($(count_of "${key}") <= 1)) || {
            echo "dispatch: ${field}: ${key}= appears more than once" >&2
            exit 1
        }
    done
    if value_of "${name}_file" > /dev/null && value_of "${name}" > /dev/null; then
        echo "dispatch: ${field}: both ${name}_file= and ${name}= name a file" >&2
        exit 1
    fi
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
import json, os, re, shutil, sys, tempfile
from pathlib import Path

mode, path, line, sender, to, before = sys.argv[1:7]
record = Path(path)

def refuse(pairs):
    keys = [k for k, _ in pairs]
    dup = next((k for k in keys if keys.count(k) > 1), None)
    if dup is not None:
        sys.exit(f"dispatch: {path}: duplicate key {dup}")
    return dict(pairs)

def constant(name):
    sys.exit(f"dispatch: {path}: non-finite number {name}")

text = record.read_text()
block, rest = {}, text
if text.startswith("---\n"):
    end = text.find("\n---\n", 3)
    if end < 0:
        sys.exit(f"dispatch: {path}: the block between the first two --- lines is not closed")
    try:
        block = json.loads(text[4:end], object_pairs_hook=refuse, parse_constant=constant)
    except json.JSONDecodeError as e:
        sys.exit(f"dispatch: {path}: the block is not valid JSON: {e}")
    rest = text[end + 5:]
    if not isinstance(block, dict):
        sys.exit(f"dispatch: {path}: the block is not a JSON object")
entries = block.setdefault("dispatch", [])
if not isinstance(entries, list):
    sys.exit(f"dispatch: {path}: dispatch is not a list")
# Thread 4254844587: another task's record never takes this task's dispatch.
task = next((t[len("task_id="):] for t in line.split(" ") if t.startswith("task_id=")), None)
if task is not None and "task" in block and block["task"] != task:
    sys.exit(f"dispatch: {path} is the record of task {block['task']}, the line is task {task}")
row = re.compile(r"^\s*(\S+)\s+\[[^\]]+\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
marks = [m.group(1) for m in map(row.match, sys.stdin.read().splitlines())
         if m and (m.group(2), m.group(3), m.group(4)) == (sender, to, line)]
if mode == "check":
    print(len(marks))
    sys.exit(0)
# Thread 4254399807: an older identical row is not this send.
if len(marks) <= int(before):
    sys.exit(f"dispatch: this send added no bus row; {path} is unchanged")
entries.append(f"{line} read_at={'read' if marks[-1] == '○' else 'unread'}")
body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
# Thread 4254844595: the line is already sent, so the record is replaced whole or not at all.
fd, tmp = tempfile.mkstemp(dir=record.parent, prefix=f".{record.name}.")
try:
    with os.fdopen(fd, "w") as f:
        f.write(f"---\n{body}\n---\n{rest}")
        f.flush()
        os.fsync(f.fileno())
    shutil.copymode(record, tmp)
    os.replace(tmp, record)
except BaseException:
    Path(tmp).unlink(missing_ok=True)
    raise
PY
[[ ${record} == /* ]] || record="${PWD}/${record}"
# The local review of 0d199475 (C-32): a record mkstemp cannot replace would fail only after the send.
if [[ ! -f ${record} || ! -w ${record} || ! -w "$(dirname -- "${record}")" ]]; then
    echo "dispatch: the record ${record} cannot be written" >&2
    exit 1
fi
# Team-wide: history.sh renames the calling pane after an agent argument (thread 4254399805).
bus() { "${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" 100000; }
before="$(bus | python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" 0)"
rc=0
agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
bus | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}" "${before}"
exit "${rc}"
