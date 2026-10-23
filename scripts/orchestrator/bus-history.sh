#!/usr/bin/env bash
# @file bus-history.sh
# @brief Print a team's hcom bus history as TSV rows the records can paste.
# @description
#   Plan 025 W2b (C-1). Reads `hcom events --type message --thread <team> --full
#   --last <limit> [--after <since>]` (`hcom events --help`; hcom 0.7.30
#   src/commands/events.rs:33 last, :39 full; `--last` is `ORDER BY id DESC LIMIT
#   n`, events.rs:185, so the newest rows) and prints one row per message,
#   ascending by id: `id<TAB>at<TAB>from<TAB>to<TAB>kind<TAB>body`. `at` is hcom's
#   `ts` as printed, `to` the delivered_to names joined with commas (`-` when
#   none), `kind` the first word of the text, and `body` the text with backslash,
#   tab, CR and LF escaped as `\\`, `\t`, `\r` and `\n`, so every row is one line
#   of five tabs. `--kind` keeps only the rows whose kind equals it. Never writes:
#   the store `$HCOM_DIR/hcom.db` must already exist, because `hcom events`
#   creates one on first use (observed with 0.7.30).
# @arg $1 string Team, the hcom thread (`^[a-z0-9][a-z0-9_-]{0,63}$`).
# @option --limit <n> Newest rows to read (default 200, a positive integer).
# @option --since <ts> Only rows after this time, hcom's `--after` (`YYYY-MM-DD[THH:MM:SS[Z]]`).
# @option --kind <kind> Only rows of this kind, the first word of the line (e.g. AGMSG-RESULT).
# @env HCOM_DIR The private hcom store directory (required).
# @stdout TSV rows `id<TAB>at<TAB>from<TAB>to<TAB>kind<TAB>body`, possibly none.
# @exitcode 0 Printed.
# @exitcode 1 Usage error, store absent, or hcom failed (its error on stderr).
# @example
#   HCOM_DIR=/path/to/.hcom scripts/orchestrator/bus-history.sh dotfiles --limit 50 --kind AGMSG-RESULT
set -euo pipefail

usage='usage: bus-history.sh <team> [--limit <n>] [--since <ts>] [--kind <kind>]'
(($# >= 1)) || {
    echo "${usage}" >&2
    exit 1
}
team=$1
shift
limit=200 since='' kind=''
while (($#)); do
    (($# >= 2)) || {
        echo "${usage}" >&2
        exit 1
    }
    case $1 in
    --limit) limit=$2 ;;
    --since) since=$2 ;;
    --kind) kind=$2 ;;
    *)
        echo "${usage}" >&2
        exit 1
        ;;
    esac
    shift 2
done
[[ ${team} =~ ^[a-z0-9][a-z0-9_-]{0,63}$ ]] || {
    echo "bus-history: team '${team}' is outside ^[a-z0-9][a-z0-9_-]{0,63}\$" >&2
    exit 1
}
[[ ${limit} =~ ^[1-9][0-9]*$ ]] || {
    echo 'bus-history: --limit must be a positive integer' >&2
    exit 1
}
[[ -n ${HCOM_DIR:-} && -f ${HCOM_DIR:-}/hcom.db ]] || {
    echo "bus-history: store absent: \${HCOM_DIR}/hcom.db (HCOM_DIR=${HCOM_DIR:-unset})" >&2
    exit 1
}

query=(events --type message --thread "${team}" --full --last "${limit}")
[[ -z ${since} ]] || query+=(--after "${since}")
rows=$(hcom "${query[@]}") || exit 1
jq -rn --arg kind "${kind}" '
  def kind_of: [splits("[ \t]+") | select(. != "")][0] // "-";
  def escaped: gsub("\\\\"; "\\\\") | gsub("\t"; "\\t") | gsub("\r"; "\\r") | gsub("\n"; "\\n");
  [inputs | select(.type == "message")] | sort_by(.id)[]
  | select($kind == "" or (.data.text | kind_of) == $kind)
  | [(.id | tostring), .ts, (.data.from // "-"),
     ((.data.delivered_to // []) | if length == 0 then "-" else join(",") end),
     (.data.text | kind_of), (.data.text | escaped)]
  | join("\t")' <<< "${rows}"
