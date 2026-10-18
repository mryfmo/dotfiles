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
#   `task_file=` and `task_sha256=`. Tokens are separated by any run of spaces
#   and tabs, and every token after `v1` is `<key>=<value>` (exit 2 otherwise,
#   so a repeated prefix or a value split by a space is refused); the
#   recorder takes `task_id` from that one parse (thread 4255272793). A relative path is read from the root of
#   the checkout this script lives in (`git rev-parse --show-toplevel` there, under the allowlisted environment),
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
#   only `dispatch`. The prose after the block is kept byte for byte, CRLF
#   included (thread 4256987087), and the record is replaced atomically (a
#   temporary file in its directory, fsync, rename) under an exclusive `flock`
#   of that directory, so two dispatches to one record never lose an entry
#   (thread 4255272797). A record that is not an existing regular file writable in a
#   writable directory, or whose `task` is not the line's `task_id`, is refused
#   before the send, and nothing is sent.
#   An AGMSG-TASK line whose `task_file=` fails `task-consistency-check.py`
#   (beside this script, run as `python -I` through `uv run --offline`, PyYAML from the pinned cache only,
#   with `--no-config`, `--no-project` and a pinned `--python`, from the root, under `env -i` with only
#   `PATH`, `HOME` (the script owner's passwd home), `UV_CACHE_DIR` (under it), `LANG`, `LC_ALL` and the `AGMSG_*`
#   variables) is refused with the checker's output, and nothing is sent (C-52).
#   Only a review brief is exempt: a front matter (the text between the first
#   two `---` lines) that PyYAML parses, refusing a duplicate key, to a mapping
#   whose `kind` is the string `review`; every other outcome runs the checker.
#   Only a bus row this send created is recorded. Both reads of the team-wide
#   `history.sh <team> "" <BUS_READ_WINDOW>` take the newest rows (C-53: a
#   whole-bus read took 56 minutes on a 1385-row team), and the recorder aligns
#   them as two views of one bus: the pre-send window (each row's timestamp,
#   sender, recipient and text) goes to a private `mktemp` file removed on exit;
#   after the send every shift j from 0 to m-1 of the m post-send rows is tried,
#   and exactly one may leave the post-send window, without its j newest rows,
#   equal to the pre-send window without the rows that left it (all m new rows
#   when the pre-send window was empty). This send is the last of those j new
#   rows equal to the line, sender and recipient. No fit, several fits (a
#   periodic bus), j = 0 or no equal new row leaves the record unchanged and
#   exits 1. The read state is the marker history.sh prints for that row
#   (`●` unread, `○` read): agmsg's scripts expose no read_at time, this script
#   never reads the message database, and it never passes an agent to
#   history.sh, whose agent argument renames the caller's pane after it.
#   Plan 024 P1-5: before an `AGMSG-ACCEPTANCE ... status=accepted` send, the task's newest `AGMSG-RESULT v1` in the
#   pre-send window (none without a record) needs one `head=` (a commit here) and one `precheck=`, the sha256 of the
#   head's `.orchestration/<task>/precheck.json`, whose `head` is the head or an ancestor whose diff to it is only under
#   `.orchestration/<task>/`. A failure prints `precheck: <field> <reason>` (exit 1, nothing sent) under
#   `PRECHECK_REQUIRED=1`, else `precheck: warning <field> <reason>`, and sends (plan 024 0d).
# @arg $1 string agmsg team.
# @arg $2 string Sender identity.
# @arg $3 string Recipient identity.
# @arg $4 string Recipient pane id (for example `w5:pA`).
# @arg $5 path File holding the line.
# @arg $6 path Optional acceptance record (`.orchestration/acceptance/<task>.md`), relative to the current directory.
# @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
# @env BUS_READ_WINDOW The newest rows each history read takes (default 200, a positive integer).
# @env PRECHECK_REQUIRED `1` refuses (exit 1) an accepted ACCEPTANCE without a matching precheck; unset or `0` warns; any
#   other value is a usage error.
# @exitcode 0 Sent, and recorded when a record was given (agmsg-dispatch's own status otherwise).
# @exitcode 1 A field check failed, the task file fails the task-consistency check, the record is malformed, or the sent line was not recorded.
# @exitcode 2 Usage error, the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line, or PyYAML is not in
#   the pinned uv cache (run `make validate-agent-assets` to warm it).
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
[[ ${line} =~ ^AGMSG-(TASK|ACCEPTANCE|PING)[[:blank:]]+v1[[:blank:]] ]] || {
    echo "dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line" >&2
    exit 2
}
# One allowlisted environment for git and uv: no inherited GIT_DIR, GIT_WORK_TREE or other GIT_*, VIRTUAL_ENV, UV_* or
# PYTHON* variable chooses the root, the interpreter or the code they run (audit:ef74eae:1, C-57).
# HOME is the script owner's passwd home and the uv cache sits under it, never inherited values (4300738707).
owner="$(stat -c %U -- "${BASH_SOURCE[0]}" 2> /dev/null || stat -f %Su -- "${BASH_SOURCE[0]}")" || owner=
[[ ${owner} =~ ^[A-Za-z0-9._][A-Za-z0-9._-]*$ ]] || {
    echo "dispatch: cannot tell the owner of ${BASH_SOURCE[0]}" >&2
    exit 1
}
home=
eval "home=~${owner}" # the name is checked above; ~name is its passwd home
[[ ${home} == /* ]] || {
    echo "dispatch: no passwd home for ${owner}" >&2
    exit 1
}
clean=(env -i PATH="${PATH}" HOME="${home}" UV_CACHE_DIR="${home}/.cache/uv")
for v in LANG LC_ALL; do
    [[ -z ${!v:-} ]] || clean+=("${v}=${!v}")
done
while IFS= read -r v; do
    [[ ${v} != AGMSG_* ]] || clean+=("${v}=${!v}")
done < <(compgen -e)
root="$("${clean[@]}" git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"

read -ra tokens <<< "${line}"
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
required=${PRECHECK_REQUIRED:-0}
[[ ${required} == 0 || ${required} == 1 ]] || usage
# Plan 024 P1-5: argv is the task id and the pre-send window file ('' when none was read); git runs in the root.
read -r -d '' prechecker << 'PY' || true
import hashlib, json, re, subprocess, sys
task, window = sys.argv[1:3]
REQUIRED = "unit-test render-check format shellcheck secrets local-review"
git = lambda *args: subprocess.run(["git", *args], capture_output=True)
def problem():
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", task): return f"task_id {task} is not a task id"
    if not window: return "result no history window was read (no acceptance record was given)"
    rows = [row[3].split() for row in json.load(open(window))]
    found = [i for i, t in enumerate(rows) if t[:2] == ["AGMSG-RESULT", "v1"] and f"task_id={task}" in t[2:]]
    if not found: return f"result no AGMSG-RESULT v1 row for task_id={task} in the window"
    result = rows[found[-1]]
    # The newest status=revise ACCEPTANCE before that RESULT names the selectors whose proofs the record must carry.
    revises = [t for t in rows[: found[-1]] if t[:2] == ["AGMSG-ACCEPTANCE", "v1"] and f"task_id={task}" in t and "status=revise" in t]
    requested = [t[6:] for t in revises[-1] if t.startswith("check=")] if revises else []
    if "status=ready_for_review" not in result: return "result the newest RESULT is not status=ready_for_review"
    heads = [t[5:] for t in result if t.startswith("head=")]
    wants = [t[9:] for t in result if t.startswith("precheck=")]
    if len(heads) != 1 or not re.fullmatch(r"[0-9a-f]{40}", heads[0]): return "head the RESULT needs one head= of 40 hex digits"
    if len(wants) != 1 or not re.fullmatch(r"[0-9a-f]{64}", wants[0]): return "precheck the RESULT needs one precheck= of 64 hex"
    head, want, path = heads[0], wants[0], f".orchestration/{task}/precheck.json"
    if git("cat-file", "-e", f"{head}^{{commit}}").returncode: return f"head {head} is not a commit in this checkout"
    blob = git("cat-file", "blob", f"{head}:{path}")
    got = hashlib.sha256(blob.stdout).hexdigest() if blob.returncode == 0 else "nothing (no such file)"
    if got != want: return f"precheck mismatch: the RESULT has {want}, {path} at {head} hashes to {got}"
    try:
        doc = json.loads(blob.stdout)
    except ValueError:
        doc = None
    field = doc.get("head") if isinstance(doc, dict) else None
    if not isinstance(field, str) or not re.fullmatch(r"[0-9a-f]{40}", field): return f"precheck.json:head {path} has no 40-hex head"
    checks, selectors, required = doc.get("checks"), doc.get("selectors"), REQUIRED.split()
    if not (isinstance(checks, list) and checks): return f"precheck.json:checks {path} lists no checks"
    if not all(isinstance(c, dict) and isinstance(c.get("name"), str) and "ok" in c for c in checks): return f"precheck.json:checks {path} at {head} has an entry without a name and an ok"
    names = [c["name"] for c in checks]
    if len(set(names)) != len(names) or not set(required) <= set(names): return f"precheck.json:checks {path} at {head} must name each of {required} once: {names}"
    # Every executed check passed as the JSON boolean true; only the exact deferred local-review record is null.
    failed = [c["name"] for c in checks if c["ok"] is not True and c != {"name": "local-review", "ok": None, "deferred": "orchestrator"}]
    if failed: return f"precheck.json:checks {path} at {head} records checks that did not pass: {failed}"
    if not isinstance(selectors, list) or not all(isinstance(s, dict) and isinstance(s.get("selector"), str) and s.get("ok") is True for s in selectors):
        return f"precheck.json:selectors {path} at {head} is not a list of passing selector proofs"
    missing = [r for r in requested if [s["selector"] for s in selectors].count(r) != 1]
    if missing: return f"precheck.json:selectors {path} at {head} lacks exactly one proof of the requested {missing}"
    if field != head and git("merge-base", "--is-ancestor", field, head).returncode: return f"precheck.json:head {field} is not an ancestor of {head}"
    if field != head and git("diff", "--quiet", field, head, "--", ".", f":(exclude).orchestration/{task}/").returncode:
        return f"precheck.json:head {field}..{head} changes paths outside .orchestration/{task}/"
    return ""
print(problem())
PY
# @description Refuse (PRECHECK_REQUIRED=1) or warn about an accepted ACCEPTANCE whose precheck does not match.
# @arg $1 path The pre-send window file, or empty when no history was read.
precheck_gate() {
    local problem
    [[ ${tokens[0]} == AGMSG-ACCEPTANCE && "$(value_of status || true)" == accepted ]] || return 0
    problem="$(cd -- "${root}" && "${clean[@]}" python3 -I -c "${prechecker}" "$(value_of task_id)" "$1")" ||
        problem="checker the precheck check itself failed"
    [[ -n ${problem} ]] || return 0
    ((required)) || {
        echo "precheck: warning ${problem}" >&2
        return 0
    }
    echo "precheck: ${problem}" >&2
    exit 1
}
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
if [[ ${tokens[0]} == AGMSG-TASK ]]; then
    tf="$(value_of task_file)" && [[ ${tf} == /* ]] || tf="${root}/${tf}"
    # Offline only: PyYAML comes from the pinned cache the validator recipes warm, and a cold cache stops the send,
    # never a fetch. --no-project: a pyproject.toml in the caller's directory is never discovered, synced or built.
    # The interpreter is named, python3 as mise answers it under env -i at the root, else python3 on PATH, and uv
    # runs under env -i with an allowlist, so no VIRTUAL_ENV, CONDA_PREFIX, UV_* or PYTHON* variable reaches it
    # (local:9df6b0c:1, C-57, the Bot's P1 4300102967).
    py="$(cd -- "${root}" && { env -i PATH="${PATH}" HOME="${home}" mise which python3 2> /dev/null || command -v python3; })" || py=
    [[ ${py} == /* ]] || {
        echo "dispatch: no python3 interpreter to pin for uv" >&2
        exit 1
    }
    uvy=(uv run --no-config --no-project --offline --python "${py}" --with pyyaml)
    here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
    # Run from the trusted root, so a caller's .python-version or virtual environment picks no interpreter (4299651928).
    uvr() { (cd -- "${root}" && "${clean[@]}" "${uvy[@]}" "$@"); }
    uvr python -I -c 'import yaml' > /dev/null 2>&1 || {
        echo "dispatch: PyYAML is not in the uv cache ${home}/.cache/uv; run make validate-agent-assets to warm it" >&2
        exit 2
    }
    read -r -d '' brief << 'PY' || true
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
PY
    # Fail-closed: only a parsed front matter whose kind is review skips the checker.
    if ! uvr python -I -c "${brief}" "${tf}" > /dev/null 2>&1; then
        out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" "${tf}" 2>&1)" || {
            echo "dispatch: ${tf} fails the task-consistency check" >&2
            printf '%s\n' "${out}" >&2
            exit 1
        }
    fi
fi
if [[ -z ${record} ]]; then
    precheck_gate ''
    exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"
fi

# Modes: `check` parses the record and writes the pre-send window to the window file; `append` aligns
# history.sh's post-send window on stdin with it, takes the sent row's read marker (● unread, ○ read) and appends it.
read -r -d '' recorder << 'PY' || true
import fcntl, json, os, re, shutil, sys, tempfile
from pathlib import Path

mode, path, line, sender, to, window, task = sys.argv[1:8]
record = Path(path)
rows = [r for r in sys.stdin.read().splitlines() if r]

def refuse(pairs):
    keys = [k for k, _ in pairs]
    dup = next((k for k in keys if keys.count(k) > 1), None)
    if dup is not None:
        sys.exit(f"dispatch: {path}: duplicate key {dup}")
    return dict(pairs)

def constant(name):
    sys.exit(f"dispatch: {path}: non-finite number {name}")

def load():
    # newline="": a CRLF record keeps its line endings (thread 4256987087).
    with open(record, newline="") as f:
        text = f.read()
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
    # Thread 4254844587: another task's record never takes this task's dispatch.
    if "task" in block and block["task"] != task:
        sys.exit(f"dispatch: {path} is the record of task {block['task']}, the line is task {task}")
    return block, rest

row = re.compile(r"^\s*(\S+)\s+\[([^\]]+)\]\s+(\S+)\s+→\s+(\S+):\s(.*)$")
# (marker, [timestamp, sender, recipient, text]); the marker is left out of the alignment, a read flips it.
seen = [(m.group(1), list(m.group(2, 3, 4, 5))) for m in map(row.match, rows) if m]
if mode == "check":
    load()
    with open(window, "w") as f:
        json.dump([fields for _, fields in seen], f)
    sys.exit(0)
with open(window) as f:
    pre = json.load(f)
post = [fields for _, fields in seen]
n, m = len(pre), len(post)
# Shift j: the post-send window without its j newest rows equals the pre-send one without its e = n + j - m oldest.
fits = [m] if n == 0 else [j for j in range(m) if 0 <= n + j - m < n and post[: m - j] == pre[n + j - m :]]
if len(fits) != 1:
    sys.exit(
        "dispatch: the post-send window does not align uniquely with the pre-send one; "
        "the line may be on the bus unrecorded; raise BUS_READ_WINDOW or check the bus"
    )
if fits[0] == 0:
    sys.exit(f"dispatch: this send added no bus row; {path} is unchanged")
# Another seat's row may land after this send, so the send is the last new row equal to the line.
marks = [mark for mark, (_, s, r, text) in seen[m - fits[0] :] if (s, r, text) == (sender, to, line)]
if not marks:
    sys.exit("dispatch: no new row equals the line; the line may be on the bus unrecorded; check the bus")
# Thread 4255272797: the read-modify-write holds the record directory's lock, so a second dispatch waits.
lock = os.open(record.parent, os.O_RDONLY)
fcntl.flock(lock, fcntl.LOCK_EX)
block, rest = load()
block["dispatch"].append(f"{line} read_at={'read' if marks[-1] == '○' else 'unread'}")
body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
# Thread 4254844595: the line is already sent, so the record is replaced whole or not at all.
fd, tmp = tempfile.mkstemp(dir=record.parent, prefix=f".{record.name}.")
try:
    with os.fdopen(fd, "w", newline="") as f:
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
limit=${BUS_READ_WINDOW:-200}
[[ ${limit} =~ ^[1-9][0-9]*$ ]] || usage
task="$(value_of task_id)"
# A private window file (mode 0600, a fresh name), removed whatever the exit.
window="$(mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX")"
trap 'rm -f -- "${window}"' EXIT
# Team-wide: history.sh renames the calling pane after an agent argument (thread 4254399805).
bus() { "${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}"; }
bus | python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" "${window}" "${task}"
precheck_gate "${window}"
rc=0
agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
bus | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}" "${window}" "${task}"
exit "${rc}"
