#!/usr/bin/env bash
# @file stall-watch.sh
# @brief Run stall-check.py over a program store on a schedule and record each new stall once in decisions.tsv.
# @description
#   Regime-cutover U621 (standing orders 57 and 59). Measured 2026-11-19: four Task subagents went silent after a
#   tool result (one died on the network's TLS proxy error, two produced no transcript entry for 30 to 38 minutes,
#   one parked on a `wait` whose job result never arrived) and each cost 30 to 40 minutes before the coordinator
#   noticed by hand, about 2.5 hours in the day. `stall-check.py` (U496) names the in-flight units silent past a
#   deadline, but nothing ran it on a schedule and nothing acted on its rows. This lever is that schedule and that
#   record: `stall-watch.sh <store> [--deadline-minutes <n>] [--interval-seconds <n>] [--once]` runs the
#   `stall-check.py` beside it (`python3 -I <dir>/stall-check.py <store> --progress-root <store>/progress
#   --deadline-minutes <n>`) every interval (default 60 seconds) with the deadline (default 25 minutes), and for
#   each `stalled` or `no-file` row it prints it appends one row to the store's `decisions.tsv` (header `ts phase
#   decision why evidence result`: the UTC clock, phase `stall`, a decision naming the unit and the age, the why
#   naming this lever and the standing orders, the evidence the unit's progress file and its last line, result
#   `open`) exactly once per stall and prints the row on stdout, `unit<TAB>state<TAB>age_minutes<TAB>last_line` as
#   `stall-check.py` printed it, so the coordinator's `wait` on this process wakes on that line. The record is made
#   once per stall by a marker file `<store>/progress/<unit>-stalled-<ts>`, `<ts>` the timestamp of the stalled last
#   line (`none` for a `no-file` row), created exclusively (`set -C`, so two watchers never record one stall twice):
#   a marker that exists is a recorded stall and the row is neither appended nor printed again; a worker that moves
#   again and stalls later has a later last line, so a new marker and a new row. The progress root is
#   `<store>/progress`, the directory the coordinator's worker contract names (`hcom-orchestration` SKILL step 1:
#   every delegated worker writes `<store>/progress/<unit>-progress.txt`), so the markers lie beside the files they
#   judge. The lever kills and restarts nothing: the coordinator's Task subagents are not processes it owns, and the
#   hcom seats have `stall-check.py` already; its job is detection and the record, and the coordinator stops the
#   worker and starts a fresh one with the same consolidated brief when the row arrives. Every read has its status
#   read (standing order 21): a `stall-check.py` exit other than 0 or 1 (its refusal, or an `unreadable` or
#   `malformed` row) is printed on stderr as `stall-watch.sh: stall-check.py exited <n>; the loop continues` after
#   the checker's own stderr, which passes through, and the rows it printed are still read, so one worker's garbage
#   file never hides another worker's stall; an `unreadable` or `malformed` row is printed on stderr with its unit
#   and recorded as no stall. A failed `date` or a failed append is printed on stderr, the marker of that stall is
#   removed so the next tick records it, and the loop continues. With `--once` the lever runs one tick and exits:
#   0 when the check ran and no new stall was recorded, 1 when a new stall was recorded (the row is on stdout), 3
#   when `stall-check.py` exited other than 0 or 1 or a record could not be made (whatever else the tick
#   recorded), so the coordinator's
#   verification run against the live store reads as one code. Without `--once` the loop runs until a signal ends
#   it; between ticks it sleeps in the background and waits, so a TERM or an INT ends it at once. Before anything
#   the lever refuses (exit 2, one stderr line `stall-watch.sh: refused: <reason>`, nothing on stdout, nothing
#   written) an argument holding a tab, a newline or a carriage return (the rows and the record are tab-separated
#   lines), a missing or second store, an unknown option, a `--deadline-minutes` that is not 1 to 10 decimal digits
#   without a leading zero or is outside 1 to 1440 (24 hours; `stall-check.py`'s own bound), an `--interval-seconds`
#   of the same shape outside 1 to 86400, a store that cannot be entered (it is resolved with `pwd -P`, so the
#   checker sees a clean absolute path), a `units.tsv` or `decisions.tsv` under it that is not a regular file (a
#   link included), a `progress` directory that is missing or a link, a `decisions.tsv` or `progress` that cannot be
#   written, no `stall-check.py` beside this lever, or no `python3` on PATH. Installed as
#   `~/.local/bin/common/stall-watch.sh` by the generator's copy and pin (`claude.levers.sha256.stall-watch.sh`),
#   with no allow rule and no seat policy row: the coordinator runs it outside every seat, in the background for
#   the program; `tests/unit/test_stall_watch.py` runs the checkout script and the installed layout over a scratch
#   store.
# @arg $1 path The program store directory holding units.tsv, decisions.tsv and progress/.
# @option --deadline-minutes <n> The age in whole minutes a moving worker's last line may have (default 25, 1 to 1440).
# @option --interval-seconds <n> Seconds between two ticks (default 60, 1 to 86400).
# @option --once Run one tick and exit with its result instead of looping.
# @stdout One `unit<TAB>state<TAB>age_minutes<TAB>last_line` row per newly recorded stall, as stall-check.py printed it.
# @exitcode 0 `--once`: the check ran and no new stall was recorded.
# @exitcode 1 `--once`: a new stall was recorded this tick.
# @exitcode 3 `--once`: stall-check.py exited other than 0 or 1, or a record could not be made, this tick (printed on stderr).
# @exitcode 2 Refused before the first tick: a bad argument, a store that is not a store, no checker, no python3.
# @example
#   scripts/orchestrator/stall-watch.sh ~/.local/state/regime-store/dotfiles/regime-cutover --once
#   scripts/orchestrator/stall-watch.sh ~/.local/state/regime-store/dotfiles/regime-cutover &
set -euo pipefail

# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
lever_self_check() {
    local src dir self name pin digest home
    # The directory is split from the path in the shell, so no external producer (dirname) can fail unseen.
    src=${BASH_SOURCE[0]}
    case ${src} in
    */*) dir=${src%/*} ;;
    *) dir=. ;;
    esac
    [[ -n ${dir} ]] || dir=/
    dir=$(cd "${dir}" && pwd -P) || {
        echo "${src##*/}: refused: cannot resolve the script directory of ${src}" >&2
        exit 2
    }
    self=${dir}/${BASH_SOURCE[0]##*/}
    name=${self##*/}
    home=$(cd "${HOME}" 2> /dev/null && pwd -P) || home=''
    if [[ -n ${home} && ${dir} == "${home}/.local/bin/common" ]]; then # lint-comparisons: allow both sides are pwd -P forms
        LEVER_MANIFEST=${HOME}/.agents/agent-config.yaml
    else
        LEVER_MANIFEST=${dir}/../../home/dot_agents/agent-config.yaml
    fi
    [[ -r ${LEVER_MANIFEST} ]] || {
        echo "${name}: refused: manifest unreadable: ${LEVER_MANIFEST}" >&2
        exit 2
    }
    pin=$(sed -n -E "s/^      ${name//./\\.}: ([0-9a-f]{64})\$/\\1/p" "${LEVER_MANIFEST}") || {
        echo "${name}: refused: cannot read ${LEVER_MANIFEST}" >&2
        exit 2
    }
    [[ ${pin} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: no single sha256 pin for ${name} in ${LEVER_MANIFEST}" >&2
        exit 2
    }
    if command -v sha256sum > /dev/null; then
        digest=$(sha256sum < "${self}") || digest=''
    else
        digest=$(shasum -a 256 < "${self}") || digest=''
    fi
    digest=${digest%% *}
    [[ ${digest} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: cannot hash ${self}" >&2
        exit 2
    }
    [[ ${digest} == "${pin}" ]] || {
        echo "${name}: refused: sha256 ${digest} of ${self} differs from the pin in ${LEVER_MANIFEST}" >&2
        exit 2
    }
}
lever_self_check

# @description Print the refusal in the levers' one-line form on stderr and exit 2; nothing was printed on stdout.
# @arg $@ string The reason.
refuse() {
    printf 'stall-watch.sh: refused: %s\n' "$*" >&2
    exit 2
}

# @description Print a problem of one tick on stderr; the loop continues.
# @arg $@ string The message.
complain() {
    printf 'stall-watch.sh: %s\n' "$*" >&2
}

# @description Set a variable to text as one cell of a tab-separated row: a tab, a newline or a carriage return is
#   one space. The result is assigned, not printed, so no command substitution stands in the row's printf.
# @arg $1 string The variable to set.
# @arg $2 string The text.
cell() {
    local text=$2
    text=${text//$'\t'/ }
    text=${text//$'\n'/ }
    text=${text//$'\r'/ }
    printf -v "$1" '%s' "${text}"
}

usage='usage: stall-watch.sh <store> [--deadline-minutes <n>] [--interval-seconds <n>] [--once]'
# The two integer options share stall-check.py's shape (1 to 10 decimal digits, no leading zero), judged as text
# before any arithmetic sees the value.
digits='^(0|[1-9][0-9]{0,9})$'
given='' deadline=25 interval=60 once=0
for argument in "$@"; do
    case ${argument} in
    *$'\t'* | *$'\n'* | *$'\r'*) refuse 'an argument holds a tab, a newline or a carriage return; the rows and the record are tab-separated lines' ;;
    esac
done
while (($#)); do
    case $1 in
    --deadline-minutes | --interval-seconds)
        (($# >= 2)) || refuse "$1 needs a value; ${usage}"
        [[ $2 =~ ${digits} ]] || refuse "$1 $2 is not 1 to 10 decimal digits without a leading zero"
        if [[ $1 == --deadline-minutes ]]; then
            ((1 <= $2 && $2 <= 1440)) || refuse "$1 $2 is outside 1 to 1440"
            deadline=$2
        else
            ((1 <= $2 && $2 <= 86400)) || refuse "$1 $2 is outside 1 to 86400"
            interval=$2
        fi
        shift
        ;;
    --once) once=1 ;;
    -*) refuse "unknown option $1; ${usage}" ;;
    *)
        [[ -z ${given} ]] || refuse "one store, not two (${given} and $1); ${usage}"
        given=$1
        ;;
    esac
    shift
done
[[ -n ${given} ]] || refuse "a store path is needed; ${usage}"

# The checker is the stall-check.py beside this file, found by the same split as the self-check's.
case ${BASH_SOURCE[0]} in
*/*) here=${BASH_SOURCE[0]%/*} ;;
*) here=. ;;
esac
[[ -n ${here} ]] || here=/
here=$(cd "${here}" && pwd -P) || refuse "the script directory of ${BASH_SOURCE[0]} cannot be resolved"
checker=${here}/stall-check.py
[[ -f ${checker} && ! -L ${checker} ]] || refuse "no stall-check.py beside ${here}/stall-watch.sh"
command -v python3 > /dev/null || refuse 'no python3 on PATH to run stall-check.py'

# The store as a clean absolute path (no trailing or repeated separator, no `.` or `..` component), the form
# stall-check.py accepts, and its three entries: the register, the record and the progress root.
store=$(cd -- "${given}" 2> /dev/null && pwd -P) || refuse "the store ${given} is not a directory that can be entered"
[[ -f ${store}/units.tsv && ! -L ${store}/units.tsv ]] || refuse "${store}/units.tsv is not a regular file"
record=${store}/decisions.tsv
[[ -f ${record} && ! -L ${record} ]] || refuse "${record} is not a regular file"
[[ -w ${record} ]] || refuse "${record} cannot be written; the stall rows go there"
progress=${store}/progress
[[ -d ${progress} && ! -L ${progress} ]] || refuse "${progress} is not a directory; the workers' progress files and the stall markers live there"
[[ -w ${progress} ]] || refuse "${progress} cannot be written; the stall markers go there"

# The unit id shape stall-check.py prints (U<n> or U<n><letter>), the one shape that names a marker file.
unit_shape='^U[0-9]+[a-z]?$'
# The timestamp a stalled last line starts with, the identity of its stall.
stamp_shape='^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)'
recorded=0 failed=0

# @description Record one stall once: create its marker exclusively, append the decisions row, print the row. A
#   marker that exists is a recorded stall and nothing is printed. A failed clock read or append removes the marker
#   and complains, so the next tick records the stall.
# @arg $1 string The unit.
# @arg $2 string The state, `stalled` or `no-file`.
# @arg $3 string The age in minutes, `-` for no file.
# @arg $4 string The last line, `-` for no file.
record_stall() {
    local unit=$1 state=$2 age=$3 last=$4 stamp marker now decision why evidence
    if [[ ${last} =~ ${stamp_shape} ]]; then
        stamp=${BASH_REMATCH[1]}
    else
        stamp=none
    fi
    marker=${progress}/${unit}-stalled-${stamp}
    if ! (
        set -C
        : > "${marker}"
    ) 2> /dev/null; then
        [[ -e ${marker} ]] && return 0
        complain "the marker ${marker} cannot be created; the stall of ${unit} is not recorded"
        failed=1
        return 0
    fi
    if ! now=$(date -u +%Y-%m-%dT%H:%M:%SZ) || [[ ! ${now} =~ ${stamp_shape}$ ]]; then
        rm -f "${marker}"
        complain "the clock cannot be read (date -u failed); the stall of ${unit} is not recorded"
        failed=1
        return 0
    fi
    if [[ ${state} == no-file ]]; then
        decision="${unit} stalled: no progress file ${progress}/${unit}-progress.txt since dispatch, past the ${deadline}-minute deadline"
        evidence="stall-check.py row: ${unit} ${state} ${age} ${last}"
    else
        decision="${unit} stalled: the last progress line is ${age} minutes old, past the ${deadline}-minute deadline"
        evidence="${progress}/${unit}-progress.txt last line: ${last}"
    fi
    why="stall-watch.sh tick (standing orders 57 and 59; U621): the coordinator stops the worker and starts a fresh one with the same consolidated brief"
    cell decision "${decision}"
    cell why "${why}"
    cell evidence "${evidence}"
    if ! printf '%s\t%s\t%s\t%s\t%s\t%s\n' "${now}" stall "${decision}" "${why}" "${evidence}" open >> "${record}"; then
        rm -f "${marker}"
        complain "the row cannot be appended to ${record}; the stall of ${unit} is not recorded"
        failed=1
        return 0
    fi
    printf '%s\t%s\t%s\t%s\n' "${unit}" "${state}" "${age}" "${last}"
    recorded=$((recorded + 1))
}

# @description One tick: run the checker, read every row it printed, record the stalls. Sets `failed` to 1 when the
#   checker exited other than 0 or 1 or a record could not be made.
tick() {
    local rows status unit state age last
    failed=0
    if rows=$(python3 -I "${checker}" "${store}" --progress-root "${progress}" --deadline-minutes "${deadline}"); then
        status=0
    else
        status=$?
    fi
    if ((status != 0 && status != 1)); then
        failed=1
        complain "stall-check.py exited ${status}; the loop continues"
    fi
    [[ -n ${rows} ]] || return 0
    while IFS=$'\t' read -r unit state age last; do
        [[ -n ${unit} ]] || continue
        [[ ${unit} =~ ${unit_shape} ]] || {
            complain "a row names no unit: ${unit} ${state} ${age} ${last}"
            continue
        }
        case ${state} in
        stalled | no-file) record_stall "${unit}" "${state}" "${age}" "${last}" ;;
        moving | done) ;;
        *) complain "${unit} ${state}: ${last}" ;;
        esac
    done <<< "${rows}"
}

# A signal between ticks ends the loop at once: the sleep runs in the background and `wait` returns on the signal;
# the sleeper ends by itself within one interval, so nothing is killed.
trap 'exit 143' TERM
trap 'exit 130' INT
trap 'exit 129' HUP
while :; do
    recorded=0
    tick
    if ((once)); then
        ((! failed)) || exit 3
        ((! recorded)) || exit 1
        exit 0
    fi
    sleep "${interval}" &
    wait $! || true
done
