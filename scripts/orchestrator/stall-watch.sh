#!/usr/bin/env bash
# @file stall-watch.sh
# @brief Run stall-check.py over a program store on a schedule and record each new stall once in decisions.tsv.
# @description
#   Regime-cutover U621 (standing orders 57 and 59; round 2 after verdict U621-942e9a16, round 3 after verdict
#   U621-b368fced, round 4 after verdict U621-4edab4b0). Measured 2026-11-19: four Task subagents went silent after a
#   tool result (one died on the network's TLS proxy error, two produced no transcript entry for 30 to 38 minutes, one
#   parked on a `wait` whose job result never arrived) and each cost 30 to 40 minutes before the coordinator noticed by
#   hand, about 2.5 hours in the day. `stall-check.py` (U496) names the in-flight units silent past a deadline, but
#   nothing ran it on a schedule and nothing acted on its rows. This
#   lever is that schedule and that record: `stall-watch.sh <store> [--deadline-minutes <n>] [--interval-seconds
#   <n>] [--once | --until-stall]` runs the `stall-check.py` beside it (`python3 -I <dir>/stall-check.py <store>
#   --progress-root <store>/progress --deadline-minutes <n>`) every interval (default 60 seconds) with the deadline
#   (default 25 minutes), and for each stall it finds it appends one row to the store's `decisions.tsv` (header `ts
#   phase decision why evidence result`: the tick's UTC clock, phase `stall`, a decision naming the unit and the age,
#   the why naming this lever and the standing orders, the evidence the unit's progress file and its last line,
#   result `open`) exactly once per stall and prints the row on stdout, `unit<TAB>state<TAB>age_minutes<TAB>last_line`
#   as `stall-check.py` printed it. The progress root is `<store>/progress`, the directory the coordinator's worker
#   contract names (`hcom-orchestration` SKILL step 1: every delegated worker writes
#   `<store>/progress/<unit>-progress.txt`), so the markers below lie beside the files they judge.
#
#   A `stalled` row (a file whose last line is older than the deadline) is a stall at once, identified by the
#   timestamp its last line starts with. A `no-file` row is a stall only after the deadline: a worker dispatched a
#   minute ago has written nothing yet, so the first tick that finds a unit in flight without a file records when it
#   saw it, by a marker `<store>/progress/<unit>-seen-<ts>` created exclusively with that tick's UTC clock as `<ts>`,
#   and reports `no-file` only when the current tick is at least `--deadline-minutes` after that first-seen time (the
#   earliest `seen` marker of the unit counts); a unit whose file appears later (any row of it other than `no-file`)
#   gets its `seen` markers removed on that tick. The stall's identity is that first-seen time, so the no-file marker
#   is `<unit>-stalled-seen-<ts>`: after the coordinator ran `stall-watch.sh <store> reset <unit>`, a replacement
#   worker's own silence is a later first-seen time, a new marker and a new row. `reset <unit>` takes no option
#   (one given is refused naming it) and makes the replacement start clean as one transaction ordered to fail safe:
#   it reads the clock; moves the unit's progress file aside, `<unit>-progress.txt` to `<unit>-progress.<UTC clock of
#   the reset>.txt` in the same directory (a rename, nothing deleted, so the previous worker's lines stay for the
#   record and the replacement has no file, which the first-seen rule above counts from its first tick instead of
#   reporting the old file's last line as a stall at once), when there is one; only after the archive stands, removes
#   the unit's `seen` and `stalled` markers, partial ones included; and prints only at the end, after every step
#   succeeded, each removed marker in the order removed and the archived file's name last on stdout (nothing about
#   the file when there is none), exit 0. Any failure (the clock, the rename, an archive name already taken, a marker
#   removal) stops the sequence there: one stderr line names the step and what was already done before it, nothing
#   is printed on stdout, the exit is 3, and the coordinator finishes the named step by hand or fixes the store, runs
#   `reset` again and dispatches the replacement only after an exit 0. The archive comes before the markers because
#   a marker removed before a failed rename would let the next tick record the same stall again from the old file.
#
#   The record is made once per stall by a marker file `<store>/progress/<unit>-stalled-<ts>`, `<ts>` the timestamp of
#   the stalled last line or `seen-<first-seen ts>` for a no-file stall, and the row is written before the marker is
#   made permanent: the marker is created exclusively (`set -C`, so two watchers never record one stall twice) under
#   the partial name `<marker>.partial`, the row is appended, then the partial marker is renamed to its final name. A
#   final marker is a recorded stall and the row is neither appended nor printed again; a partial marker younger than
#   one interval is another watcher between its two writes and is left alone; a partial marker older than one interval
#   (its mtime, read with `date -r`) is a watcher killed between the two writes: the tick removes it, says so on
#   stderr, and records the stall again, so the row may appear twice and a stall is never lost. A partial marker whose
#   age cannot be read (`date -r` failed or printed no number while the marker still stands) is never read as young:
#   the failure is printed on stderr, counted as the record's failure (`--once` and `--until-stall` exit 3) and the
#   marker is left for the next tick, so a stale marker can suppress a stall for one tick, not for ever. A worker that
#   moves again and stalls later has a later last line, so a new marker and a new row. The row is appended through
#   `python3 -I -S -c` with `os.open(path, O_WRONLY | O_APPEND | O_NOFOLLOW | O_CLOEXEC)`, an `fstat` that the opened
#   file is regular and one `os.write` of the whole line, so a link put in `decisions.tsv`'s place after the preflight
#   check is a failed append naming it, never a write outside the store (the store's `decisions.tsv` is a regular file
#   the coordinator owns); nothing else is written through Python, the markers are the shell's own exclusive creates.
#
#   The lever kills and restarts nothing: the coordinator's Task subagents are not processes it owns, and the hcom
#   seats have `stall-check.py` already; its job is detection and the record. A background job's output reaches the
#   coordinator only when the job exits, so with `--until-stall` the lever loops as without it and exits 1 at the end
#   of the first tick that records a new stall, exits 3 on a checker or record failure, and otherwise keeps running;
#   the tick that records a stall records every new stall it finds in that tick (each with its marker and its row) and
#   prints every one of those rows on stdout before the one exit 1, so each printed row is one stalled worker. The
#   coordinator runs it as a background job whose exit is the wake and reads the exit: 1 is a stall, each row on
#   stdout one stalled worker to replace (stop that worker, run `reset <unit>`, start a fresh worker with the same
#   consolidated brief), and the lever is started again only after every row's unit was reset; 3 is this lever's own
#   failure (the checker or the record), named on stderr, from which nothing about any worker is known (a row on
#   stdout beside it is a stall the tick did record, handled as under 1): the coordinator fixes the store or the
#   checker and starts the lever again without touching a worker that has no row; 2 is a refusal of the arguments.
#   With `--once` the lever runs one tick and exits: 0 when the check ran and no new stall was recorded, 1 when a new
#   stall was recorded (every row is on stdout), 3 when `stall-check.py` exited other than 0 or 1 or a record could
#   not be made (whatever else the tick recorded), so the coordinator's verification run against the live store reads
#   as one code; `--once` and `--until-stall` together are refused. Without either the loop runs until a signal ends it;
#   between ticks it sleeps in the background and waits, so a TERM or an INT ends it at once. Every read has its
#   status read (standing order 21): a `stall-check.py` exit other than 0 or 1 (its refusal, or an `unreadable` or
#   `malformed` row) is printed on stderr as `stall-watch.sh: stall-check.py exited <n>; the loop continues` after the
#   checker's own stderr, which passes through, and the rows it printed are still read, so one worker's garbage file
#   never hides another worker's stall; an `unreadable` or `malformed` row is printed on stderr with its unit and
#   recorded as no stall. A failed `date` at the start of a tick is printed and the tick records nothing; a failed
#   marker create or a failed append is printed, the partial marker of that stall is removed so the next tick records
#   it, and the plain loop continues (`--once` and `--until-stall` exit 3).
#
#   Before anything the lever refuses (exit 2, one stderr line `stall-watch.sh: refused: <reason>`, nothing on stdout,
#   nothing written) an argument holding a tab, a newline or a carriage return (the rows and the record are
#   tab-separated lines), a missing or second store, an unknown option or command, `--once` with `--until-stall`,
#   `reset` without a unit of the shape `U<n>` or `U<n><letter>` or with an option, a `--deadline-minutes` that is not
#   1 to 10 decimal digits without a leading zero or is outside 1 to 1440 (24 hours; `stall-check.py`'s own bound), an
#   `--interval-seconds` of the same shape outside 1 to 86400, a store that cannot be entered (it is resolved with
#   `pwd -P`, so the checker sees a clean absolute path), a `units.tsv` or `decisions.tsv` under it that is not a
#   regular file (a link included), a `progress` directory that is missing or a link, a `decisions.tsv` or `progress`
#   that cannot be written, no `stall-check.py` beside this lever, or no `python3` on PATH. Installed as
#   `~/.local/bin/common/stall-watch.sh` by the generator's copy and pin (`claude.levers.sha256.stall-watch.sh`),
#   with no allow rule and no seat policy row: the coordinator runs it outside every seat, in the background for
#   the program; `tests/unit/test_stall_watch.py` runs the checkout script and the installed layout over a scratch
#   store.
# @arg $1 path The program store directory holding units.tsv, decisions.tsv and progress/.
# @arg $2 string `reset`, followed by the unit whose progress file is moved aside and whose `seen` and `stalled` markers are then removed, one transaction (no option with it).
# @option --deadline-minutes <n> The age in whole minutes a moving worker's last line, or a unit's first sighting without a file, may have (default 25, 1 to 1440).
# @option --interval-seconds <n> Seconds between two ticks (default 60, 1 to 86400).
# @option --once Run one tick and exit with its result instead of looping.
# @option --until-stall Loop, and exit 1 at the end of the first tick that records a new stall (every row of that tick on stdout) or 3 on a checker or record failure.
# @stdout One `unit<TAB>state<TAB>age_minutes<TAB>last_line` row per newly recorded stall, as stall-check.py printed it; `reset`, on exit 0 only: each removed marker path in the order removed, then the archived progress file's path last.
# @exitcode 0 `--once`: the check ran and no new stall was recorded; `reset`: its progress file, if there was one, is archived and every marker of the unit is gone.
# @exitcode 1 `--once` or `--until-stall`: a new stall was recorded this tick (every row of the tick is on stdout).
# @exitcode 3 `--once` or `--until-stall`: stall-check.py exited other than 0 or 1, or a record could not be made or a partial marker's age read, this tick (printed on stderr); `reset`: the clock, the rename (an archive name already taken included) or a marker removal failed, the sequence stopped there, one stderr line names the step and what was done before it, nothing on stdout.
# @exitcode 2 Refused before the first tick: a bad argument, a store that is not a store, no checker, no python3.
# @example
#   scripts/orchestrator/stall-watch.sh ~/.local/state/regime-store/dotfiles/regime-cutover --once
#   scripts/orchestrator/stall-watch.sh ~/.local/state/regime-store/dotfiles/regime-cutover --until-stall &
#   scripts/orchestrator/stall-watch.sh ~/.local/state/regime-store/dotfiles/regime-cutover reset U621
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

# @description Set a variable to the POSIX seconds of a `YYYY-MM-DDTHH:MM:SSZ` timestamp by arithmetic alone (the
#   days-from-civil formula over the proleptic Gregorian calendar), since GNU `date -d` and BSD `date -j -f` differ
#   and the marker names and the tick's clock are the only clocks compared.
# @arg $1 string The variable to set.
# @arg $2 string The timestamp, already matched by stamp_shape.
epoch_of() {
    local y m d hh mm ss era yoe doy doe days
    y=$((10#${2:0:4})) m=$((10#${2:5:2})) d=$((10#${2:8:2})) hh=$((10#${2:11:2})) mm=$((10#${2:14:2})) ss=$((10#${2:17:2}))
    if ((m <= 2)); then
        y=$((y - 1))
    fi
    era=$(((y >= 0 ? y : y - 399) / 400))
    yoe=$((y - era * 400))
    doy=$(((153 * (m > 2 ? m - 3 : m + 9) + 2) / 5 + d - 1))
    doe=$((yoe * 365 + yoe / 4 - yoe / 100 + doy))
    days=$((era * 146097 + doe - 719468))
    printf -v "$1" '%s' "$((days * 86400 + hh * 3600 + mm * 60 + ss))"
}

usage='usage: stall-watch.sh <store> [--deadline-minutes <n>] [--interval-seconds <n>] [--once | --until-stall]; stall-watch.sh <store> reset <unit>'
# The two integer options share stall-check.py's shape (1 to 10 decimal digits, no leading zero), judged as text
# before any arithmetic sees the value.
digits='^(0|[1-9][0-9]{0,9})$'
# The unit id shape stall-check.py prints (U<n> or U<n><letter>), the one shape that names a marker file.
unit_shape='^U[0-9]+[a-z]?$'
# The timestamp a stalled last line starts with, the identity of its stall; whole, the clock of a tick and the
# first-seen time in a `seen` marker's name.
stamp_shape='^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)'
# `option_seen` is the first option on the line, the one a `reset` refusal names: reset takes none.
given='' verb='' reset_unit='' deadline=25 interval=60 once=0 until_stall=0 option_seen=''
for argument in "$@"; do
    case ${argument} in
    *$'\t'* | *$'\n'* | *$'\r'*) refuse 'an argument holds a tab, a newline or a carriage return; the rows and the record are tab-separated lines' ;;
    esac
done
while (($#)); do
    case $1 in
    --deadline-minutes | --interval-seconds)
        [[ -n ${option_seen} ]] || option_seen=$1
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
    --once)
        [[ -n ${option_seen} ]] || option_seen=$1
        once=1
        ;;
    --until-stall)
        [[ -n ${option_seen} ]] || option_seen=$1
        until_stall=1
        ;;
    -*) refuse "unknown option $1; ${usage}" ;;
    *)
        if [[ -z ${given} ]]; then
            given=$1
        elif [[ -z ${verb} ]]; then
            [[ $1 == reset ]] || refuse "one store, not two (${given} and $1), or the command reset <unit>; ${usage}"
            verb=$1
        elif [[ -z ${reset_unit} ]]; then
            [[ $1 =~ ${unit_shape} ]] || refuse "reset $1: not a unit id of the shape U<n> or U<n><letter>"
            reset_unit=$1
        else
            refuse "reset takes one unit, not two (${reset_unit} and $1); ${usage}"
        fi
        ;;
    esac
    shift
done
[[ -n ${given} ]] || refuse "a store path is needed; ${usage}"
((! (once && until_stall))) || refuse "--once and --until-stall are two ways to end; give one"
if [[ -n ${verb} ]]; then
    [[ -n ${reset_unit} ]] || refuse "reset needs the unit whose markers are removed; ${usage}"
    [[ -z ${option_seen} ]] || refuse "reset takes no option (${option_seen} given); ${usage}"
fi

# The checker is the stall-check.py beside this file, found by the same split as the self-check's.
case ${BASH_SOURCE[0]} in
*/*) here=${BASH_SOURCE[0]%/*} ;;
*) here=. ;;
esac
[[ -n ${here} ]] || here=/
here=$(cd "${here}" && pwd -P) || refuse "the script directory of ${BASH_SOURCE[0]} cannot be resolved"
checker=${here}/stall-check.py
[[ -f ${checker} && ! -L ${checker} ]] || refuse "no stall-check.py beside ${here}/stall-watch.sh"
store=$(cd -- "${given}" 2> /dev/null && pwd -P) || refuse "the store ${given} is not a directory that can be entered"
[[ -f ${store}/units.tsv && ! -L ${store}/units.tsv ]] || refuse "${store}/units.tsv is not a regular file"
record=${store}/decisions.tsv
[[ -f ${record} && ! -L ${record} ]] || refuse "${record} is not a regular file"
[[ -w ${record} ]] || refuse "${record} cannot be written; the stall rows go there"
progress=${store}/progress
[[ -d ${progress} && ! -L ${progress} ]] || refuse "${progress} is not a directory; the workers' progress files and the stall markers live there"
[[ -w ${progress} ]] || refuse "${progress} cannot be written; the stall markers go there"

# @description `reset <unit>`, one transaction ordered to fail safe (round 4 after verdict U621-4edab4b0, P2 at
#   `:314`): read the clock; move the unit's progress file aside, `<unit>-progress.txt` to `<unit>-progress.<UTC clock
#   of the reset>.txt` beside it (a rename, nothing deleted: the previous worker's lines stay for the record, and the
#   replacement starts with no file, so its silence is a new first sighting and a new stall), when there is one; only
#   after the archive stands, remove the unit's `seen` and `stalled` markers, partial ones included; print only at the
#   end, after every step succeeded. The archive comes before the markers because a marker removed before a failed
#   rename would let the next tick record the same stall twice from the old file, while a rename done before a failed
#   removal leaves the final marker that keeps the record single. Any failure (the clock, the rename, a marker
#   removal; an archive name already taken is a failure of the rename) stops the sequence at that step: one stderr
#   line names the step and what was already done before it (the archive made, the markers removed), nothing is
#   printed on stdout, and the exit is 3, so the coordinator finishes the named step by hand or fixes the store and
#   runs `reset` again. Every read has its status read (standing order 21).
# @arg $1 string The unit.
# @stdout On exit 0 only: each removed marker's path in the order it was removed, then the archived file's path last
#   (no line about the file when there was none).
# @exitcode 0 The progress file, if there was one, is archived and every marker of the unit is gone.
# @exitcode 3 The clock could not be read, the progress file could not be renamed (the archive name taken included)
#   or a marker could not be removed: one stderr line names the step and what was done before it; nothing on stdout.
reset_unit_state() {
    local unit=$1 entry file archive='' clock removed_lines='' removed_list='' done_so_far
    file=${progress}/${unit}-progress.txt
    # Step 1, the clock: the archive's name. Nothing is done yet, so a failure leaves nothing to finish by hand.
    if ! clock=$(date -u +%Y-%m-%dT%H:%M:%SZ) || [[ ! ${clock} =~ ${stamp_shape}$ ]]; then
        if [[ -e ${file} || -L ${file} ]]; then
            complain "the clock cannot be read (date -u failed); the progress file ${file} is not archived and no marker of ${unit} is removed"
        else
            complain "the clock cannot be read (date -u failed); no marker of ${unit} is removed (there is no progress file ${file} to archive)"
        fi
        return 3
    fi
    # Step 2, the archive by rename, when a file exists: a taken name is the rename's failure, and `mv -n` with the
    # read-back that the source is gone and the archive stands refuses to overwrite a name taken between the two.
    if [[ -e ${file} || -L ${file} ]]; then
        archive=${progress}/${unit}-progress.${clock}.txt
        if [[ -e ${archive} || -L ${archive} ]]; then
            complain "the rename of the progress file ${file} to ${archive} failed: the archive name is taken; nothing is done (the file stands and no marker of ${unit} is removed)"
            return 3
        fi
        if ! mv -n -- "${file}" "${archive}" 2> /dev/null || [[ -e ${file} || -L ${file} ]] || [[ ! -e ${archive} && ! -L ${archive} ]]; then
            complain "the rename of the progress file ${file} to ${archive} failed; nothing is done (the file stands and no marker of ${unit} is removed)"
            return 3
        fi
    fi
    # Step 3, the markers, each read for its status; the first failure stops the sequence and names what stands done.
    for entry in "${progress}/${unit}-seen-"* "${progress}/${unit}-stalled-"*; do
        [[ -e ${entry} || -L ${entry} ]] || continue
        if ! rm -f -- "${entry}" 2> /dev/null; then
            if [[ -n ${archive} ]]; then
                done_so_far="the progress file ${file} is archived as ${archive}"
            else
                done_so_far="there was no progress file ${file} to archive"
            fi
            if [[ -n ${removed_list} ]]; then
                done_so_far+="; the markers removed before it: ${removed_list}"
            else
                done_so_far+="; no marker was removed before it"
            fi
            complain "the marker ${entry} cannot be removed; done before the failure: ${done_so_far}; finish by hand and run reset ${unit} again"
            return 3
        fi
        removed_lines+="${entry}"$'\n'
        removed_list+="${removed_list:+, }${entry}"
    done
    # Step 4, the print, only now that every step succeeded: the markers in the order removed, the archive line last.
    printf '%s' "${removed_lines}"
    [[ -z ${archive} ]] || printf '%s\n' "${archive}"
    return 0
}
if [[ -n ${verb} ]]; then
    if reset_unit_state "${reset_unit}"; then
        exit 0
    fi
    exit 3
fi

now='' now_epoch=0 recorded=0 failed=0 partial_age=''

# @description Append one row to the record through a descriptor of its own: `O_NOFOLLOW` so a link put in
#   `decisions.tsv`'s place after the preflight check fails here naming it instead of being followed to a file outside
#   the store, `fstat` so only a regular file takes the row, and one `os.write` of the whole line. The reason of a
#   failure is one stderr line; nothing else of this lever writes through Python.
# @arg $1 string The row, tab-separated, ending in its newline.
# @exitcode 0 The whole row was written.
# @exitcode 1 The open, the fstat or the write failed (the reason on stderr).
append_row() {
    python3 -I -S -c '
import os
import stat
import sys

path, row = sys.argv[1], os.fsencode(sys.argv[2])
try:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW | os.O_CLOEXEC)
    except OSError as error:
        raise SystemExit(f"cannot be opened: {error.strerror or error}") from None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise SystemExit("is not a regular file")
        try:
            written = os.write(fd, row)
        except OSError as error:
            raise SystemExit(f"cannot be written: {error.strerror or error}") from None
        if written != len(row):
            raise SystemExit(f"took a short write ({written} of {len(row)} bytes)")
    finally:
        os.close(fd)
except SystemExit as stop:
    if stop.code:
        print(stop.code, file=sys.stderr)
        sys.exit(1)
    raise
' "${record}" "$1" < /dev/null
}

# @description Set `partial_age` to the standing of a partial marker by its mtime (`date -r`, the one form GNU and BSD
#   date share): `stale` when older than one interval (a watcher killed between its two writes, so the stall is
#   recorded again), `young` when not (another watcher between its two writes), `gone` when the marker vanished before
#   the read (that watcher finished its record), or `unknown` when `date -r` failed or printed no number while the
#   marker still stands. The read's status is read (standing order 21): `unknown` is never taken for `young`, since a
#   stale marker read as young would suppress its stall for ever; the caller prints it and counts it as the record's
#   failure.
# @arg $1 path The partial marker.
# @set partial_age `stale`, `young`, `gone` or `unknown`.
partial_marker_age() {
    local mtime
    if ! mtime=$(date -u -r "$1" +%s 2> /dev/null) || [[ ! ${mtime} =~ ^[0-9]+$ ]]; then
        if [[ -e $1 ]]; then
            partial_age=unknown
        else
            partial_age=gone
        fi
        return 0
    fi
    if ((now_epoch - mtime > interval)); then
        partial_age=stale
    else
        partial_age=young
    fi
}

# @description Record one stall once: create its marker exclusively under the partial name, append the decisions
#   row, rename the marker to its final name, print the row. A final marker is a recorded stall and nothing is
#   printed; a partial marker younger than one interval is another watcher's record in progress; an older one is
#   removed and the stall recorded again; one whose age cannot be read is printed, counted as the record's failure and
#   left for the next tick. A failed create or append removes the partial marker and complains, so the next tick
#   records the stall.
# @arg $1 string The unit.
# @arg $2 string The state, `stalled` or `no-file`.
# @arg $3 string The age in minutes, `-` for no file.
# @arg $4 string The last line, `-` for no file.
# @arg $5 string The stall's identity: the last line's timestamp, or `seen-<ts>` for a no-file stall.
record_stall() {
    local unit=$1 state=$2 age=$3 last=$4 stamp=$5 marker partial row decision why evidence reason
    marker=${progress}/${unit}-stalled-${stamp}
    partial=${marker}.partial
    if [[ -e ${marker} ]]; then
        return 0
    fi
    if [[ -e ${partial} ]]; then
        partial_marker_age "${partial}"
        case ${partial_age} in
        young | gone) return 0 ;;
        unknown)
            complain "the age of the partial marker ${partial} cannot be read (date -r failed); it is left for the next tick and the stall of ${unit} is not recorded this tick"
            failed=1
            return 0
            ;;
        esac
        if ! rm -f -- "${partial}" 2> /dev/null; then
            complain "the partial marker ${partial} cannot be removed; the stall of ${unit} is not recorded"
            failed=1
            return 0
        fi
        complain "the partial marker ${partial} was older than one interval (${interval} s); removed, the stall of ${unit} is recorded again"
    fi
    if ! (
        set -C
        : > "${partial}"
    ) 2> /dev/null; then
        [[ -e ${partial} ]] && return 0
        complain "the marker ${partial} cannot be created; the stall of ${unit} is not recorded"
        failed=1
        return 0
    fi
    if [[ ${state} == no-file ]]; then
        decision="${unit} stalled: no progress file ${progress}/${unit}-progress.txt since first seen in flight at ${stamp#seen-}, past the ${deadline}-minute deadline"
        evidence="stall-check.py row: ${unit} ${state} ${age} ${last}; first seen without a file at ${stamp#seen-} (marker ${progress}/${unit}-seen-${stamp#seen-})"
    else
        decision="${unit} stalled: the last progress line is ${age} minutes old, past the ${deadline}-minute deadline"
        evidence="${progress}/${unit}-progress.txt last line: ${last}"
    fi
    why="stall-watch.sh tick (standing orders 57 and 59; U621): the coordinator stops the worker, resets the unit's markers (stall-watch.sh <store> reset ${unit}) and starts a fresh one with the same consolidated brief"
    cell decision "${decision}"
    cell why "${why}"
    cell evidence "${evidence}"
    printf -v row '%s\t%s\t%s\t%s\t%s\t%s\n' "${now}" stall "${decision}" "${why}" "${evidence}" open
    if ! reason=$(append_row "${row}" 2>&1); then
        rm -f -- "${partial}" 2> /dev/null || true
        cell reason "${reason}"
        complain "the row cannot be appended to ${record} (it ${reason}); the stall of ${unit} is not recorded"
        failed=1
        return 0
    fi
    if ! mv -- "${partial}" "${marker}" 2> /dev/null; then
        complain "the marker ${partial} cannot be renamed to ${marker}; the row is appended and the next tick after one interval records the stall of ${unit} again"
        failed=1
    fi
    printf '%s\t%s\t%s\t%s\n' "${unit}" "${state}" "${age}" "${last}"
    recorded=$((recorded + 1))
}

# @description Remove a unit's `seen` markers: its file has appeared (a row other than `no-file`), so a later silence
#   without a file is a new first sighting.
# @arg $1 string The unit.
forget_seen() {
    local entry
    for entry in "${progress}/$1-seen-"*; do
        [[ -e ${entry} || -L ${entry} ]] || continue
        rm -f -- "${entry}" 2> /dev/null || complain "the marker ${entry} cannot be removed"
    done
}

# @description A `no-file` row: record the first sighting when there is none (the marker `<unit>-seen-<tick clock>`,
#   created exclusively), else record the stall once the tick is at least the deadline after the earliest sighting.
# @arg $1 string The unit.
no_file() {
    local unit=$1 entry first='' seen seen_epoch
    for entry in "${progress}/${unit}-seen-"*; do
        [[ -e ${entry} ]] || continue
        seen=${entry##*/}
        seen=${seen#"${unit}-seen-"}
        [[ ${seen} =~ ${stamp_shape}$ ]] || continue
        if [[ -z ${first} || ${seen} < ${first} ]]; then
            first=${seen}
        fi
    done
    if [[ -z ${first} ]]; then
        entry=${progress}/${unit}-seen-${now}
        if ! (
            set -C
            : > "${entry}"
        ) 2> /dev/null && [[ ! -e ${entry} ]]; then
            complain "the marker ${entry} cannot be created; the first sighting of ${unit} without a file is not recorded"
            failed=1
        fi
        return 0
    fi
    epoch_of seen_epoch "${first}"
    ((now_epoch - seen_epoch >= deadline * 60)) || return 0
    record_stall "${unit}" no-file - - "seen-${first}"
}

# @description One tick: read the clock, run the checker, read every row it printed, record the stalls. Sets `failed`
#   to 1 when the clock could not be read, the checker exited other than 0 or 1 or a record could not be made.
tick() {
    local rows status unit state age last
    failed=0
    if ! now=$(date -u +%Y-%m-%dT%H:%M:%SZ) || [[ ! ${now} =~ ${stamp_shape}$ ]]; then
        complain 'the clock cannot be read (date -u failed); the tick records nothing'
        failed=1
        return 0
    fi
    epoch_of now_epoch "${now}"
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
        no-file)
            no_file "${unit}"
            continue
            ;;
        stalled)
            if [[ ${last} =~ ${stamp_shape} ]]; then
                record_stall "${unit}" "${state}" "${age}" "${last}" "${BASH_REMATCH[1]}"
            else
                complain "the stalled row of ${unit} has a last line without a timestamp; the stall is not recorded: ${last}"
                failed=1
            fi
            ;;
        moving | done) ;;
        *) complain "${unit} ${state}: ${last}" ;;
        esac
        # The unit has a file (whatever the row says of it), so its sightings without one are over.
        forget_seen "${unit}"
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
    if ((once || until_stall)); then
        ((! failed)) || exit 3
        ((! recorded)) || exit 1
        ((! once)) || exit 0
    fi
    sleep "${interval}" &
    wait $! || true
done
