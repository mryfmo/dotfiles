#!/usr/bin/env bash
# @file bus-read.sh
# @brief Read the whole agmsg team history and print every open task with its minutes of silence.
# @description
#   Plan 007 T718 (C-23). Reads the history through agmsg's `history.sh <team>
#   "" <limit>` (its documented positional form; never the database file) with
#   a limit far above the team's size, and refuses a read that reaches the
#   limit, so a truncated view is never taken for the whole bus. A task's state
#   is its last state-bearing message: an AGMSG-TASK (amendments included) or
#   an AGMSG-ACCEPTANCE `status=revise` opens it; an AGMSG-RESULT, or an
#   AGMSG-ACCEPTANCE `status=accepted`, `withdrawn`, `superseded`, `reset` or
#   `parked`, closes it (any other status, `under_review` among them, changes
#   nothing, so an unknown status leaves a task open rather than hiding it).
#   For each open task it prints the seat the last opener went to, the time of
#   the task's latest bus message in either direction, the whole minutes since
#   then, and `silent=yes` at thirty minutes or more (INV-10's figure), else
#   `silent=no`. `open: none` when no task (or not the named one) is open.
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
  def tok($k): [.toks[] | select(startswith($k + "="))][0] // null | if . then .[($k | length) + 1:] else null end;
  [inputs | capture("^\\s*\\S+\\s+\\[(?<at>[^\\]]+)\\]\\s+(?<from>\\S+)\\s+→\\s+(?<to>\\S+):\\s(?<body>.*)$")] as $all
  | if ($all | length) >= $limit then error("bus-read: the read reached its limit of \($limit) rows; raise BUS_READ_LIMIT") else . end
  | [$all | to_entries[] | .value + {i: .key} | .toks = (.body | split(" ")) | .kind = .toks[0]
      | .task = tok("task_id") | .status = tok("status") | select(.task != null and .toks[1] == "v1")]
  | [group_by(.task)[]
      | map(select(.kind == "AGMSG-TASK" or (.kind == "AGMSG-ACCEPTANCE" and .status == "revise"))) as $openers
      | map(select(.kind == "AGMSG-RESULT" or (.kind == "AGMSG-ACCEPTANCE" and (.status | IN("accepted", "withdrawn", "superseded", "reset", "parked"))))) as $closers
      | select(($openers | length) > 0 and (($closers | length) == 0 or $openers[-1].i > $closers[-1].i))
      | select($only == "" or .[0].task == $only)
      | .[-1].at as $last | ((now - ($last | fromdateiso8601)) / 60 | floor) as $min
      | "open: task=\(.[0].task) seat=\($openers[-1].to) last_event=\($last) minutes=\($min) silent=\(if $min >= 30 then "yes" else "no" end)"]
  | if length == 0 then "open: none" else .[] end' <<< "${history}")" || exit 1
printf '%s\n' "${report}"
