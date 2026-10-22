#!/bin/bash -p
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
#   `task_file=` and `task_sha256=`. Tokens are separated by any run of spaces
#   and tabs, and every token after `v1` is `<key>=<value>` (exit 2 otherwise,
#   so a repeated prefix or a value split by a space is refused); the
#   recorder takes `task_id` from that one parse (thread 4255272793). A relative path is read from the root of
#   the checkout this script lives in (by this script's own path, no git command), never from the caller's
#   directory. A missing field or file, a malformed value or a mismatch exits 1 naming the field, and nothing is
#   sent. Otherwise the line goes to this checkout's `home/dot_local/bin/common/executable_hcom-dispatch` as one
#   argument, byte for byte (plan 023 PR C stage 1, T129 hcom-dispatch bus a02).
#   A `status=revise` ACCEPTANCE (never `verdict=`) needs `previous_head=` (40 lowercase hex) and `check=` once each,
#   `task_sha256=` and a record, and `regime-counters.sh <task_id> --team <team> --history-only` before the send; its
#   lines join the record's `counters` list. A record needs `record_file=` naming it and `record_sha256=` of its
#   bytes: it is opened once, by name under the checkout's own `.orchestration/acceptance/` (no symlinked part),
#   checked and parsed from that one read, and, once the exact-id view of the receipt's id matches the line, sender
#   and recipient, `<the line> read_at=<read|unread>` is appended to the `dispatch` list of
#   the record's JSON block, the object between its first two `---` lines. The
#   block is read and written with Python's standard json (malformed JSON, a
#   duplicate key, NaN or Infinity, a block that is not an object or a
#   `dispatch` that is not a list is refused; `sort_keys`, `indent=2`); the key
#   is created when absent, and a record without a block gets a block holding
#   only `dispatch`. The prose after the block is kept byte for byte, CRLF
#   included (thread 4256987087), and the record is replaced atomically (a
#   temporary file in its directory, fsync, rename) under an exclusive `flock`
#   of that directory, once the name is still the opened inode with the hashed bytes (thread 4255272797), and the
#   new digest is printed as `record_sha256=<hex>`. A record that is not an existing regular file writable in a
#   writable directory, or whose `task` is not the line's `task_id`, is refused
#   before the send, and nothing is sent.
#   An AGMSG-TASK line's `task_file=` is hashed and checked as one private snapshot (constraint 3); a snapshot that
#   fails `task-consistency-check.py` (beside this script, run as `python -I` through `uv run --offline --no-config
#   --no-project --python`, PyYAML from the caller's private UV_CACHE_DIR only, uv and python the absolute installs
#   the passwd home's mise answers outside any project, from the root) is refused with the checker's output, and
#   nothing is sent (C-52).
#   Only a review brief is exempt: a front matter (the text between the first
#   two `---` lines) that PyYAML parses, refusing a duplicate key, to a mapping
#   whose `kind` is the string `review`; every other outcome runs the checker.
#   Only the message this send created is recorded: hcom-dispatch's receipt names its hcom id, and the read state
#   is that id's in `bus-history.sh`'s exact-id view; an unread message is recorded so and keeps the send's
#   non-zero status. Every send first reads the newest BUS_READ_WINDOW rows of the team through
#   `bus-history.sh` (C-53), and a bus that cannot be read is never written. Children run under `env -i` with
#   PATH=/usr/bin:/bin, HOME (the passwd home), LANG, TMPDIR and UV_CACHE_DIR; every tool is an absolute path.
# @option --passwd-home <dir> Test fixtures only, before the team: the directory standing for the passwd home.
# @arg $1 string Team.
# @arg $2 string Sender identity.
# @arg $3 string Recipient identity.
# @arg $4 string Recipient pane id (for example `w5:pA`).
# @arg $5 path File holding the line.
# @arg $6 path Optional acceptance record (`.orchestration/acceptance/<task>.md`), relative to the current directory.
# @env BUS_READ_WINDOW The newest rows the pre-send read takes (default 200, a positive integer).
# @env UV_CACHE_DIR The caller's private uv cache, an absolute path; children get it.
# @exitcode 0 Sent and read, and recorded when a record was given (hcom-dispatch's own status otherwise).
# @exitcode 1 A field check failed, the task file fails the task-consistency check, the bus is unreadable, the record is malformed, the counters failed, or the message is unread (recorded so).
# @exitcode 2 Usage error, the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line, UV_CACHE_DIR is not
#   absolute, or PyYAML is not in the private uv cache.
# @exitcode 3 hcom-dispatch sent nothing usable: no id, or an exact-id view that is not this send's.
# @example
#   scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot claude-standard-dot-a003 w5:pA \
#     "$TMPDIR/task-line.txt" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01.md
set -euo pipefail

usage() {
    echo "usage: dispatch.sh [--passwd-home <dir>] <team> <from> <to> <pane> <line-file> [<acceptance-record>]" >&2
    exit 2
}
fixture=()
if [[ ${1:-} == --passwd-home ]]; then
    (($# >= 2)) && [[ -n $2 && -z ${2%%/*} && -d $2 ]] || usage
    fixture=(--passwd-home "$2")
    shift 2
fi
(($# == 5 || $# == 6)) || usage
team=$1 from=$2 to=$3 pane=$4 file=$5 record=${6:-}
[[ -f ${file} ]] || usage
if [[ -z ${UV_CACHE_DIR:-} || -n ${UV_CACHE_DIR%%/*} ]]; then
    echo "dispatch: UV_CACHE_DIR must be an absolute path" >&2
    exit 2
fi
if [[ -n ${HCOM_DIR:-} ]]; then
    echo "dispatch: refused: an inherited HCOM_DIR names another store" >&2
    exit 1
fi
# Thread 4256541716: command substitution drops a NUL byte, so the line sent would not be the file's.
if (($(/usr/bin/tr -d '\0' < "${file}" | /usr/bin/wc -c) != $(/usr/bin/wc -c < "${file}"))); then
    echo "dispatch: ${file} holds a NUL byte" >&2
    exit 2
fi
# The sentinel keeps every trailing newline, which $( ) alone would drop (thread 4254107304).
line="$(/bin/cat -- "${file}" && printf x)" && line=${line%x} && line=${line%$'\n'}
[[ ${line} != *$'\n'* ]] || {
    echo "dispatch: ${file} holds more than one line" >&2
    exit 2
}
[[ ${line} =~ ^AGMSG-(TASK|ACCEPTANCE|PING)[[:blank:]]+v1[[:blank:]] ]] || {
    echo "dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line" >&2
    exit 2
}
# The checkout this script sits in, by its own path: no git command or inherited GIT_* variable chooses it.
root="$(cd -P -- "$(/usr/bin/dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
[[ -e ${root}/.git ]] || {
    echo "dispatch: ${root} is not a checkout" >&2
    exit 1
}
# HOME is the script owner's passwd home (the fixture's with --passwd-home), never an inherited value (4300738707).
owner="$(/usr/bin/stat -c %U -- "${BASH_SOURCE[0]}" 2> /dev/null || /usr/bin/stat -f %Su -- "${BASH_SOURCE[0]}")" || owner=
[[ ${owner} =~ ^[A-Za-z0-9._][A-Za-z0-9._-]*$ ]] || {
    echo "dispatch: cannot tell the owner of ${BASH_SOURCE[0]}" >&2
    exit 1
}
home=
eval "home=~${owner}" # the name is checked above; ~name is its passwd home
((! ${#fixture[@]})) || home=${fixture[1]}
[[ ${home} == /* ]] || {
    echo "dispatch: no passwd home for ${owner}" >&2
    exit 1
}
child=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="${home}" LANG=C.UTF-8 TMPDIR="${TMPDIR:-/tmp}" UV_CACHE_DIR="${UV_CACHE_DIR}")
[[ -z ${AGMSG_DISPATCH_TIMEOUT:-} ]] || child+=("AGMSG_DISPATCH_TIMEOUT=${AGMSG_DISPATCH_TIMEOUT}")
[[ ${AGMSG_DISPATCH_TIMEOUT:-1} =~ ^[1-9][0-9]{0,5}$ ]] || usage
bash_p=(/bin/bash --noprofile --norc -p)
self="${root}/scripts/orchestrator/dispatch.sh"
# bash 3.2 keeps here-documents in /tmp, which a sandbox may refuse: each Python section sits in one that never runs
# (`true || :`) and is read from this file by its marker.
boot='import sys
src = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = next(i for i, line in enumerate(src) if line.endswith(": << \x27" + sys.argv[2] + "\x27")) + 1
end = src.index(sys.argv[2], start)
sys.argv = sys.argv[:1] + sys.argv[3:]
exec(compile("\n".join(src[start:end]), sys.argv[0], "exec"))'
bus_history="${root}/scripts/orchestrator/bus-history.sh"
hcom_dispatch="${root}/home/dot_local/bin/common/executable_hcom-dispatch"

read -ra tokens < <(printf '%s\n' "${line}")
for t in "${tokens[@]:2}"; do
    [[ ${t} == *=* ]] || {
        echo "dispatch: ${t} is not a <key>=<value> token" >&2
        exit 2
    }
done
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
# Thread 4254163604: a TASK whose file is not hash-bound is never sent. The kind is the parsed
# first token, so a tab after it does not skip this check (thread 4260535901).
if [[ ${tokens[0]} == AGMSG-TASK ]]; then
    for field in task_file task_sha256; do
        value_of "${field}" > /dev/null || {
            echo "dispatch: an AGMSG-TASK line needs ${field}=" >&2
            exit 1
        }
    done
fi
# Item 4: a revise names the head it revises, its failing check, the task text and a record, each once.
revise=false
if [[ ${tokens[0]} == AGMSG-ACCEPTANCE && "$(value_of status || true)" == revise ]]; then
    revise=true
    if (($(count_of previous_head) != 1 || $(count_of check) != 1)) || [[ -z "$(value_of check)" ]] ||
        [[ ! "$(value_of previous_head)" =~ ^[0-9a-f]{40}$ ]]; then
        echo "dispatch: a revise needs previous_head= exactly once (40 lowercase hex) and check= exactly once (non-empty)" >&2
        exit 1
    fi
    value_of task_sha256 > /dev/null && [[ -n ${record} ]] || {
        echo "dispatch: a revise needs task_sha256= and needs its acceptance record" >&2
        exit 1
    }
fi
if [[ -n ${record} ]] && ! { value_of record_file && value_of record_sha256; } > /dev/null; then
    echo "dispatch: a line sent with a record needs record_file= and record_sha256=" >&2
    exit 1
fi
snapshots="${root}/.agents/worklog/dispatch-snapshots"
snapdir=
trap '[[ -z ${snapdir} ]] || /bin/rm -rf -- "${snapdir}"' EXIT
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
    # The task text is read once: the snapshot's bytes are hashed and are what the checker reads (constraint 3).
    if [[ ${name} == task && ${tokens[0]} == AGMSG-TASK ]]; then
        /bin/mkdir -p -- "${snapshots}" && snapdir="$(/usr/bin/mktemp -d "${snapshots}/task.XXXXXX")" || exit 1
        snapshot="${snapdir}/${path##*/}"
        (umask 077 && /bin/cat -- "${path}" > "${snapshot}") || exit 1
        path=${snapshot}
    fi
    got="$("${child[@]}" /usr/bin/shasum -a 256 "${path}")" && got=${got%% *} # shasum is Perl: no inherited PERL5*
    [[ ${got} == "${want}" ]] || {
        echo "dispatch: ${field} mismatch: the line has ${want}, ${path} hashes to ${got}" >&2
        exit 1
    }
done
if [[ ${tokens[0]} == AGMSG-TASK ]]; then
    # Offline only: PyYAML comes from the caller's private cache, and a cold cache stops the send, never a fetch.
    # uv and python are the absolute install paths mise answers from / (no project's .python-version or .venv), and
    # uv runs from the root under env -i with --no-config and --no-project (local:9df6b0c:1, C-57, 4300102967).
    mise="${home}/.local/bin/mise"
    which() { (cd / && /usr/bin/env -i PATH=/usr/bin:/bin HOME="${home}" "${mise}" which "$1" 2> /dev/null); }
    uv="$(which uv)" || uv=
    py="$(which python3)" || py=
    installs="$(cd -P -- "${home}/.local/share/mise/installs" 2> /dev/null && pwd -P)" || installs=
    for tool in "${uv}" "${py}"; do
        dir="$(cd -P -- "${tool%/*}" 2> /dev/null && pwd -P)" || dir=
        [[ -n ${installs} && ${dir} == "${installs}"/* && ${dir} != */shims && -f ${tool} ]] || { # lint-comparisons: allow pwd-P-normalised-above
            echo "dispatch: no uv and python3 installed under ${home}/.local/share/mise/installs to pin" >&2
            exit 1
        }
    done
    uvy=("${uv}" run --no-config --no-project --offline --python "${py}" --with pyyaml)
    uvr() { (cd -- "${root}" && "${child[@]}" "${uvy[@]}" "$@"); }
    uvr python -I -c 'import yaml' > /dev/null 2>&1 || {
        echo "dispatch: PyYAML is not in the uv cache ${UV_CACHE_DIR}; warm it with UV_CACHE_DIR=${UV_CACHE_DIR} make validate-agent-assets" >&2
        exit 2
    }
    true || : << 'BRIEF'
import sys, yaml
def unique(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    if len(keys) != len(set(keys)):
        raise yaml.YAMLError("duplicate key")
    return loader.construct_mapping(node, deep)
class Loader(yaml.SafeLoader):
    pass
Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique)
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
end = lines.index("---", 1) if lines[0] == "---" else None
front = yaml.load("\n".join(lines[1:end]), Loader) if end else None
sys.exit(0 if isinstance(front, dict) and front.get("kind") == "review" else 1)
BRIEF
    # Fail-closed: only a parsed front matter whose kind is review skips the checker.
    if ! uvr python -I -c "${boot}" "${self}" BRIEF "${snapshot}" > /dev/null 2>&1; then
        out="$(uvr python -I "${root}/scripts/orchestrator/task-consistency-check.py" --root "${root}" "${snapshot}" 2>&1)" || {
            echo "dispatch: ${snapshot##*/} fails the task-consistency check" >&2
            printf '%s\n' "${out}" >&2
            exit 1
        }
    fi
fi
[[ -z ${snapdir} ]] || /bin/rm -rf -- "${snapdir}" # the checker has read the snapshot; nothing after this reads it
window=${BUS_READ_WINDOW:-200}
[[ ${window} =~ ^[1-9][0-9]*$ ]] || usage
# Constraint 6: a bus that cannot be read (a forged row, a foreign store) is never written.
"${child[@]}" "${bash_p[@]}" "${bus_history}" ${fixture[@]+"${fixture[@]}"} "${team}" --limit "${window}" > /dev/null || {
    echo "dispatch: the bus of ${team} is unreadable; nothing is sent" >&2
    exit 1
}
if [[ -z ${record} ]]; then
    exec "${child[@]}" "${bash_p[@]}" "${hcom_dispatch}" ${fixture[@]+"${fixture[@]}"} "${team}" "${from}" "${to}" "${pane}" "${line}"
fi

# The record path: one process opens the record, sends, confirms the receipt by its id and writes the record.
true || : << 'RECORDER'
import fcntl, hashlib, json, os, re, stat, subprocess, sys
from datetime import datetime, timezone

root, path, line, team, sender, to, pane, task, record_file, record_sha, revise = sys.argv[1:12]
fixture, child = [a for a in sys.argv[12:14] if a], sys.argv[14:]  # child: env -i and its NAME=value arguments
bash_p = ["/bin/bash", "--noprofile", "--norc", "-p"]

def fail(why, code=1):
    sys.stderr.write(f"dispatch: {why}\n")
    sys.exit(code)

def refuse(pairs):
    keys = [k for k, _ in pairs]
    dup = next((k for k in keys if keys.count(k) > 1), None)
    if dup is not None:
        sys.exit(f"dispatch: {path}: duplicate key {dup}")
    return dict(pairs)

def constant(name):
    sys.exit(f"dispatch: {path}: non-finite number {name}")

def load():
    # CRLF keeps its line endings (thread 4256987087); the text is the one read of the opened record (constraint 4).
    text = data.decode("utf-8")
    block, rest = {}, text
    if re.match(r"---\r?\n", text):
        m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
        if not m:
            sys.exit(f"dispatch: {path}: the block between the first two --- lines is not closed")
        try:
            block = json.loads(m.group(1), object_pairs_hook=refuse, parse_constant=constant)
        except json.JSONDecodeError as e:
            sys.exit(f"dispatch: {path}: the block is not valid JSON: {e}")
        rest = text[m.end():]
        if not isinstance(block, dict):
            sys.exit(f"dispatch: {path}: the block is not a JSON object")
    if not isinstance(block.setdefault("dispatch", []), list):
        sys.exit(f"dispatch: {path}: dispatch is not a list")
    if not isinstance(block.get("counters", []), list):
        sys.exit(f"dispatch: {path}: counters is not a list")
    # Thread 4254844587: another task's record never takes this task's dispatch.
    if "task" in block and block["task"] != task:
        sys.exit(f"dispatch: {path} is the record of task {block['task']}, the line is task {task}")
    return block, rest

def read_all(fd):
    os.lseek(fd, 0, os.SEEK_SET)
    return b"".join(iter(lambda: os.read(fd, 1 << 16), b""))

def linked(name):
    """True when a component of the absolute path is a symbolic link: lstat each one, opening nothing."""
    part = "/"
    for piece in name.strip("/").split("/"):
        part = os.path.join(part, piece)
        if stat.S_ISLNK(os.lstat(part).st_mode):
            return True
    return False

def run(script, *args):
    return subprocess.run(child + bash_p + [os.path.join(root, script)] + fixture + list(args), capture_output=True,
                          text=True, stdin=subprocess.DEVNULL, timeout=1000000)

# Constraint 4: the record is a name in the checkout's own acceptance directory, opened once through that
# directory's descriptor; no symlinked part and no alias that leaves the directory reach it.
acc, name = os.path.join(root, ".orchestration/acceptance"), os.path.basename(path)
try:
    given = os.path.dirname(os.path.abspath(path))
    if linked(acc) or linked(given):
        raise OSError("a symlinked part")
    dfd = os.open(acc, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    if (os.stat(given).st_dev, os.stat(given).st_ino) != (os.fstat(dfd).st_dev, os.fstat(dfd).st_ino):
        raise OSError("another directory")
    fd = os.open(name, os.O_RDWR | os.O_NOFOLLOW, dir_fd=dfd)
    st, named = os.fstat(fd), os.stat(os.path.join(root, record_file))
except OSError as e:
    fail(f"the record {path} cannot be written under {acc}: {e}")
# The local review of 0d199475 (C-32): a record the replacement cannot write would fail only after the send.
if not stat.S_ISREG(st.st_mode) or not os.access(acc, os.W_OK) or (named.st_dev, named.st_ino) != (st.st_dev, st.st_ino):
    fail(f"the record {path} cannot be written, or record_file= names another file")
data = read_all(fd)
if hashlib.sha256(data).hexdigest() != record_sha:
    fail(f"record_sha256 mismatch: {path} is not the record the line names")
block, rest = load()
if revise == "true":
    count = run("scripts/regime-counters.sh", task, "--team", team, "--history-only",
                *(["--record-sha256", record_sha] if name == f"{task}.md" else []))
    if count.returncode:
        fail(f"{count.stderr.strip()}; regime-counters.sh failed; nothing is sent")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    block.setdefault("counters", []).append(f"{task} {stamp} " + "; ".join(count.stdout.splitlines()))
send = run("home/dot_local/bin/common/executable_hcom-dispatch", team, sender, to, pane, line)
sys.stderr.write(send.stderr)
if send.returncode not in (0, 1):
    fail(f"hcom-dispatch exited {send.returncode}; {path} is unchanged", send.returncode)
try:
    receipt = json.loads(send.stdout)
    mid = receipt["id"] if set(receipt) == {"id", "read_at"} and type(receipt["id"]) is int and receipt["id"] > 0 else None
except (ValueError, TypeError, KeyError):
    mid = None
if mid is None:
    fail(f"the send printed no receipt; the line may be on the bus unrecorded; {path} is unchanged", 3)
view = run("scripts/orchestrator/bus-history.sh", team, "--json", "--message-id", str(mid))
try:
    got = json.loads(view.stdout) if view.returncode == 0 else {}
except ValueError:
    got = {}
if not isinstance(got, dict) or (got.get("id"), got.get("from"), got.get("to"), got.get("body")) != (mid, sender, [to], line):
    fail(f"message {mid}'s exact-id view is not this send; the line may be on the bus unrecorded", 3)
# Thread 4255272797: the read-modify-write holds the record directory's lock, so a second dispatch waits, and the
# name must still be the opened inode with the bytes the line hashed immediately before the replacement.
fcntl.flock(dfd, fcntl.LOCK_EX)
now = os.stat(name, dir_fd=dfd, follow_symlinks=False)
if (now.st_dev, now.st_ino) != (st.st_dev, st.st_ino) or hashlib.sha256(read_all(fd)).hexdigest() != record_sha:
    fail(f"{path} changed during the send; message {mid} is on the bus unrecorded")
block["dispatch"].append(f"{line} read_at={'read' if got.get('read') is True else 'unread'}")
body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
out, tmp = f"---\n{body}\n---\n{rest}".encode("utf-8"), f".{name}.{os.getpid()}"
# Thread 4254844595: the line is already sent, so the record is replaced whole or not at all.
tfd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, stat.S_IMODE(st.st_mode), dir_fd=dfd)
try:
    os.write(tfd, out)
    os.fsync(tfd)
    os.close(tfd)
    os.replace(tmp, name, src_dir_fd=dfd, dst_dir_fd=dfd)
except BaseException:
    os.unlink(tmp, dir_fd=dfd)
    raise
print(f"record_sha256={hashlib.sha256(out).hexdigest()}")
sys.exit(send.returncode)
RECORDER
exec "${child[@]}" /usr/bin/python3 -I -c "${boot}" "${self}" RECORDER "${root}" "${record}" "${line}" "${team}" "${from}" "${to}" "${pane}" \
    "$(value_of task_id)" "$(value_of record_file)" "$(value_of record_sha256)" "${revise}" \
    "${fixture[0]:-}" "${fixture[1]:-}" "${child[@]}"
