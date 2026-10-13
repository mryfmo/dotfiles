#!/usr/bin/env bash
# @file dispatch.sh
# @brief Send one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING line after checking its sha256 fields.
# @description
#   Plan 007 T718 (C-20). Reads exactly one line from a file. Every
#   `<name>_sha256=<64 hex>` token is recomputed from the file its sibling
#   token names, `<name>_file=` or else `<name>=` (`task_sha256` from
#   `task_file=`, `design_sha256` from `design=`, `amended_task_sha256` from
#   `amended_task=`); a relative path is read from the root of the checkout
#   this script lives in (`git rev-parse --show-toplevel` there), never from
#   the caller's directory. A missing sibling, a missing file, a malformed
#   value or a mismatch exits 1 naming the field, and nothing is sent. Otherwise
#   the line goes to `agmsg-dispatch` as one argument, byte for byte.
# @arg $1 string agmsg team.
# @arg $2 string Sender identity.
# @arg $3 string Recipient identity.
# @arg $4 string Recipient pane id (for example `w5:pA`).
# @arg $5 path File holding the line.
# @exitcode 0 Sent (agmsg-dispatch's own status otherwise).
# @exitcode 1 A sha256 field does not match its file, or names none.
# @exitcode 2 Usage error, or the file is not one AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line.
# @example
#   scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot claude-standard-dot-a003 w5:pA "$TMPDIR/task-line.txt"
set -euo pipefail

usage() {
    echo "usage: dispatch.sh <team> <from> <to> <pane> <line-file>" >&2
    exit 2
}
(($# == 5)) || usage
team=$1 from=$2 to=$3 pane=$4 file=$5
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
exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"
