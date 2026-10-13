#!/usr/bin/env bash
# @file bus-read.sh
# @brief Read the whole agmsg team history and print every open task with its minutes of silence.
# @description
#   Plan 007 T718 (C-23). Reads the history through agmsg's `history.sh <team>
#   "" <limit>` (its documented positional form; never the database file) with
#   a limit far above the team's size, and refuses a read whose rows reach the
#   limit, so a truncated view is never taken for the whole bus. The open rule
#   is the stop gate's worker-seat branch (`scripts/agent-stop-gate.sh`; threads
#   4255494133, 4255494139): a task's latest opener, an AGMSG-TASK or an
#   AGMSG-ACCEPTANCE `status=revise` from X to Y, keeps it open until a later
#   AGMSG-RESULT or AGMSG-PONG `status=blocked` from Y to X, or a later
#   AGMSG-ACCEPTANCE from X to Y with any other status or none; a row between
#   other endpoints neither opens nor closes it. A row counts only in the form
#   `<marker> [<at>] <from> → <to>: <body>`, with an `<at>` jq's
#   `fromdateiso8601` parses and a body of AGMSG-TASK, -ACCEPTANCE, -RESULT or
#   -PONG, then `v1`, exactly one non-empty `task_id=` and at most one
#   `status=`; any other non-empty line is skipped and counted, never an exit.
#   For each open task it prints the seat the opener went to, the time of the
#   task's latest counted row, the whole minutes since then, and `silent=yes`
#   at thirty minutes or more (INV-10's figure), else `silent=no`; `open: none`
#   when no task (or not the named one) is open; then `skipped=<n>`.
# @arg $1 string agmsg team.
# @arg $2 string Optional task id: report only that task.
# @env AGMSG_SCRIPTS The agmsg scripts directory (default `$HOME/.agents/skills/agmsg/scripts`).
# @env BUS_READ_LIMIT The row limit of the read (default 100000).
# @exitcode 0 Read and reported.
# @exitcode 1 The history is unreadable, or the read reached the limit.
# @exitcode 2 Usage error.
# @example
#   scripts/orchestrator/bus-read.sh dotfiles-conformance dotfiles-T128-orchestrator-tools-a01
set -euo pipefail

(($# == 1 || $# == 2)) || {
    echo "usage: bus-read.sh <team> [<task id>]" >&2
    exit 2
}
team=$1 only=${2:-}
limit=${BUS_READ_LIMIT:-100000}
[[ ${limit} =~ ^[1-9][0-9]*$ ]] || {
    echo "bus-read: BUS_READ_LIMIT must be a positive integer" >&2
    exit 2
}
history="$("${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}")" || {
    echo "bus-read: the history of ${team} is unreadable" >&2
    exit 1
}
report="$(jq -nrR --arg only "${only}" --argjson limit "${limit}" '
  def count($k): [.toks[] | select(startswith($k + "="))] | length;
  def tok($k): [.toks[] | select(startswith($k + "="))][0] // null | if . then .[($k | length) + 1:] else null end;
  [inputs | select(. != "")] as $lines
  | [$lines[] | capture("^\\s*\\S+\\s+\\[(?<at>[^\\]]+)\\]\\s+(?<from>\\S+)\\s+→\\s+(?<to>\\S+):\\s(?<body>.*)$")] as $all
  | if ($all | length) >= $limit then error("bus-read: the read reached its limit of \($limit) rows; raise BUS_READ_LIMIT") else . end
  | [$all | to_entries[] | .value + {i: .key} | .toks = (.body | split(" ")) | .kind = .toks[0]
      | select((.kind | IN("AGMSG-TASK", "AGMSG-ACCEPTANCE", "AGMSG-RESULT", "AGMSG-PONG")) and .toks[1] == "v1"
          and count("task_id") == 1 and tok("task_id") != "" and count("status") <= 1
          and (.at | try fromdateiso8601 catch null) != null)
      | .task = tok("task_id") | .status = tok("status")] as $rows
  | [$rows | group_by(.task)[]
      | (map(select(.kind == "AGMSG-TASK" or (.kind == "AGMSG-ACCEPTANCE" and .status == "revise"))) | max_by(.i)) as $o
      | select($o != null and ($only == "" or $o.task == $only))
      | select(any(.[]; .i > $o.i and (
          (.from == $o.to and .to == $o.from and (.kind == "AGMSG-RESULT" or (.kind == "AGMSG-PONG" and .status == "blocked")))
          or (.from == $o.from and .to == $o.to and .kind == "AGMSG-ACCEPTANCE" and .status != "revise"))) | not)
      | max_by(.i).at as $last | ((now - ($last | fromdateiso8601)) / 60 | floor) as $min
      | "open: task=\($o.task) seat=\($o.to) last_event=\($last) minutes=\($min) silent=\(if $min >= 30 then "yes" else "no" end)"]
  | (if length == 0 then "open: none" else .[] end), "skipped=\(($lines | length) - ($rows | length))"' <<< "${history}")" || exit 1
printf '%s\n' "${report}"
