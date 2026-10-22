#!/bin/bash -p
# @file bus-read.sh
# @brief Read the whole agmsg team history and print every open task with its minutes of silence.
# @description
#   Plan 007 T718 (C-23). Reads the history through this checkout's
#   `scripts/orchestrator/bus-history.sh <team> --limit <limit>` (the hcom bus, plan 023 PR C stage 1; never the
#   store file or the agmsg scripts) with a limit far above the team's size, and refuses a read whose non-empty lines
#   reach the limit, counted before any row is skipped (thread 4256987062), so a
#   truncated view is never taken for the whole bus. The open rule
#   is the stop gate's worker-seat branch (`scripts/agent-stop-gate.sh`; threads
#   4255494133, 4255494139): a task's latest opener, its latest AGMSG-TASK (X
#   to Y) or a later AGMSG-ACCEPTANCE `status=revise` between the same X and Y
#   (a revise between other endpoints opens nothing: the orchestrator's local
#   review of 5b99a744), keeps it open until a later AGMSG-RESULT or AGMSG-PONG
#   `status=blocked` from Y to X, or a later AGMSG-ACCEPTANCE from X to Y with
#   any other status or none; a row between other endpoints neither opens nor
#   closes it. A row counts only in the form `<marker> [<at>] <from> → <to>:
#   <body>`, with the marker `●` or `○` (thread 4256541723), an `<at>` jq's
#   `fromdateiso8601` parses and a body of AGMSG-TASK, -ACCEPTANCE, -RESULT or
#   -PONG, then `v1`, exactly one non-empty `task_id=` and at most one
#   `status=`, its tokens split on runs of spaces and tabs as the stop gate's
#   awk splits them (the audit of 3e5cad37); any other non-empty line is
#   skipped and counted, never an exit. For each open task it prints the seat
#   the opener went to, the time of the latest counted row between the opener's
#   two endpoints (thread 4256987076), the whole minutes since then, and `silent=yes`
#   at thirty minutes or more (INV-10's figure), else `silent=no`; `open: none`
#   when no task (or not the named one) is open; then `skipped=<n>`. Both run under `env -i` (jq without HOME, so
#   no ~/.jq library), jq from `/usr/bin/jq`, else Homebrew's.
# @option --passwd-home <dir> Test fixtures only, before the team: the directory standing for the passwd home.
# @arg $1 string agmsg team.
# @arg $2 string Optional task id: report only that task.
# @env BUS_READ_LIMIT The row limit of the read (default 100000).
# @env UV_CACHE_DIR The caller's private uv cache, an absolute path; children get it.
# @exitcode 0 Read and reported.
# @exitcode 1 The history is unreadable, or the read reached the limit.
# @exitcode 2 Usage error, or UV_CACHE_DIR absent or relative.
# @example
#   scripts/orchestrator/bus-read.sh dotfiles-conformance dotfiles-T128-orchestrator-tools-a01
set -euo pipefail

usage() {
    echo "usage: bus-read.sh [--passwd-home <dir>] <team> [<task id>]" >&2
    exit 2
}
fixture=()
if [[ ${1:-} == --passwd-home ]]; then
    (($# >= 3)) && [[ -n $2 && -z ${2%%/*} && -d $2 ]] || usage
    fixture=(--passwd-home "$2")
    shift 2
fi
(($# == 1 || $# == 2)) || usage
if [[ -z ${UV_CACHE_DIR:-} || -n ${UV_CACHE_DIR%%/*} ]]; then
    echo "bus-read: UV_CACHE_DIR must be an absolute path" >&2
    exit 2
fi
root="$(cd -P -- "$(/usr/bin/dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
jq=/usr/bin/jq
[[ -x ${jq} ]] || jq=/opt/homebrew/bin/jq
team=$1 only=${2:-}
limit=${BUS_READ_LIMIT:-100000}
[[ ${limit} =~ ^[1-9][0-9]*$ ]] || {
    echo "bus-read: BUS_READ_LIMIT must be a positive integer" >&2
    exit 2
}
# HCOM_DIR is not dropped here: the reader sees it and refuses a foreign store.
history="$(/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 TMPDIR="${TMPDIR:-/tmp}" UV_CACHE_DIR="${UV_CACHE_DIR}" ${HCOM_DIR:+"HCOM_DIR=${HCOM_DIR}"} \
    /bin/bash --noprofile --norc -p "${root}/scripts/orchestrator/bus-history.sh" ${fixture[@]+"${fixture[@]}"} "${team}" --limit "${limit}")" || {
    echo "bus-read: the history of ${team} is unreadable" >&2
    exit 1
}
# shellcheck disable=SC2016 # a single-quoted jq program, not a shell expansion
report="$(printf '%s\n' "${history}" | /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 "${jq}" -nrR --arg only "${only}" --argjson limit "${limit}" '
  def count($k): [.toks[] | select(startswith($k + "="))] | length;
  def tok($k): [.toks[] | select(startswith($k + "="))][0] // null | if . then .[($k | length) + 1:] else null end;
  [inputs | select(. != "")] as $lines
  | if ($lines | length) >= $limit then error("bus-read: the read reached its limit of \($limit) rows; raise BUS_READ_LIMIT") else . end
  | [$lines[] | capture("^\\s*[●○]\\s+\\[(?<at>[^\\]]+)\\]\\s+(?<from>\\S+)\\s+→\\s+(?<to>\\S+):\\s(?<body>.*)$")] as $all
  | [$all | to_entries[] | .value + {i: .key} | .toks = [.body | splits("[ \\t]+") | select(. != "")] | .kind = .toks[0]
      | select((.kind | IN("AGMSG-TASK", "AGMSG-ACCEPTANCE", "AGMSG-RESULT", "AGMSG-PONG")) and .toks[1] == "v1"
          and count("task_id") == 1 and tok("task_id") != "" and count("status") <= 1
          and (.at | try fromdateiso8601 catch null) != null)
      | .task = tok("task_id") | .status = tok("status")] as $rows
  | [$rows | group_by(.task)[]
      | (map(select(.kind == "AGMSG-TASK")) | max_by(.i)) as $t
      | select($t != null and ($only == "" or $t.task == $only))
      | ([$t] + map(select(.kind == "AGMSG-ACCEPTANCE" and .status == "revise" and .i > $t.i
          and .from == $t.from and .to == $t.to)) | max_by(.i)) as $o
      | select(any(.[]; .i > $o.i and (
          (.from == $o.to and .to == $o.from and (.kind == "AGMSG-RESULT" or (.kind == "AGMSG-PONG" and .status == "blocked")))
          or (.from == $o.from and .to == $o.to and .kind == "AGMSG-ACCEPTANCE" and .status != "revise"))) | not)
      | map(select([.from, .to] | sort == ([$o.from, $o.to] | sort))) | max_by(.i).at as $last
      | ((now - ($last | fromdateiso8601)) / 60 | floor) as $min
      | "open: task=\($o.task) seat=\($o.to) last_event=\($last) minutes=\($min) silent=\(if $min >= 30 then "yes" else "no" end)"]
  | (if length == 0 then "open: none" else .[] end), "skipped=\(($lines | length) - ($rows | length))"')" || exit 1
printf '%s\n' "${report}"
