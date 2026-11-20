#!/usr/bin/env bash
# @file round-advance.sh
# @brief Run one round's mechanics after a worker commit in one command: fetch and merge the moved branch, push, update-branch, the carry, the rows, the sweep TASK, the audit and the CI watch.
# @description
#   Regime-cutover U624 (standing orders 59 and 60, wave 2). Measured 2026-11-19: after each worker commit the
#   coordinator ran the same twelve commands by hand, twelve times (fetch the GitHub branch into the worker tree and
#   merge it when GitHub had moved it, a push rejected once when this was skipped; push through the credential route;
#   `pr-update-branch.sh`; the units row; the sweep seat positioned; the sweep brief; the TASK; `pr-audit.sh` to a
#   file; the CI watch; the decisions row), 10 to 15 minutes and one or two mistakes per round. This lever is the one
#   command: `round-advance.sh <store> <unit> <pr> --tree <worker tree> (--sweep-brief <file> --sweep-seat <seat>
#   --sweep-to <hcom name> | --no-sweep) [--no-audit] [--no-ci] [--team <thread>] [--from <sender>] [--seats-root
#   <dir>] [--sweep-note <text>]`, run from the coordinator's main checkout (the repository of the current directory,
#   `git rev-parse --show-toplevel`, where `pr-audit.sh` must run and `scripts/orchestrator/audit-carry.py` lies). It
#   runs the steps below in order, reads every step's status (standing order 21), prints one receipt line per step on
#   stdout, `round-advance: <step> <result>`, and stops at the first failure with one stderr line naming the step,
#   what failed and what was already done before it, exit 1; the coordinator finishes the named step by hand and runs
#   the rest, or fixes the cause and runs the lever again (every step before the failure is idempotent: a fetched
#   branch, a pushed head, an up-to-date branch and a set row change nothing the second time).
#
#   The steps. (a) `fetch`: in the worker tree, `git fetch origin <branch>` (`<branch>` the tree's current branch,
#   `git symbolic-ref --short HEAD`) and, when GitHub's branch is not an ancestor of the tree's head (`git merge-base
#   --is-ancestor FETCH_HEAD HEAD` exit 1; exit 0 is an ancestor, anything else a failure), `git -c
#   commit.gpgsign=false merge --no-ff --no-edit FETCH_HEAD` (GitHub's merge of main from an earlier round into the
#   worker's new commit, so the push below is a fast-forward of GitHub's branch); a merge that fails is a failure
#   naming the conflicted files (`git diff --name-only --diff-filter=U`) and the tree is left in that merge for the
#   coordinator to resolve or abort, nothing else is resolved, nothing was pushed. (b) `push`: in the main checkout,
#   `git fetch <tree> <branch>` (the tree is a repository of its own, fetched by path) and the head it fetched compared
#   with the tree's head, then the route that works on this laptop (decisions.tsv 2026-11-19T18:56:00Z):
#   `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null git -c 'credential.helper=!gh auth git-credential' push
#   https://github.com/<owner>/<repo> FETCH_HEAD:refs/heads/<branch>`, the owner and repository read from `gh repo
#   view --json owner,name` in the checkout and held to `[A-Za-z0-9._-]+/[A-Za-z0-9._-]+`. (c) `update-branch`:
#   `pr-update-branch.sh <pr>` (the lever on PATH, the installed copy on the coordinator's) and its receipt `updated
#   pr=<pr> old=<old> new=<new>` read; `<old>` must be the pushed head (GitHub's merge was made onto it), and when
#   `<new>` equals `<old>` the head is read again with `gh pr view <pr> --json headRefOid` every
#   ROUND_ADVANCE_POLL_SECONDS (default 5) until it changes or ROUND_ADVANCE_HEAD_WAIT_SECONDS (default 60) pass
#   (GitHub makes the merge commit after the call returns; `gh pr update-branch` on a branch already up to date
#   prints `already up-to-date` and makes no commit, so an unchanged head after the wait is the pushed head, the
#   round's head). (d) `carry`: `git fetch origin <branch>` in the main checkout (the new head must be local before
#   anything reads it; unfetched, `audit-carry.py` fails `not our ref`), the fetched head compared with the round's
#   head, then `python3 -I <checkout>/scripts/orchestrator/audit-carry.py <store> <unit> <pr> <head> --repo
#   <checkout> --base origin/main`: exit 0 with the line `carried <earlier> <head> <digest>` is the carried head (the
#   diff against main is the last audited head's, standing order 38), recorded at once through `ledger-row.py <store>
#   carried --pr <pr> --head <head> --unit <unit> --line <the line> --note <text>` beside this lever, after which the
#   sweep and the audit are skipped (U620, PR 815: a carried head needs neither); exit 1 is `not carried` (its stdout
#   names why: no earlier audited head, or the first path that differs) and the round goes on; any other exit is a
#   failure. (e) `units`: `units-row.py <store> set --id <unit> --head <head>` beside this lever. (f) `sweep`, with
#   `--sweep-brief`: the seat checkout `<seats root>/<seat>` positioned at the head (`git -C <seat> fetch`, `git -C
#   <seat> checkout --detach <head>`, `git -C <seat> status --porcelain` must print nothing and `rev-parse HEAD` must
#   be the head), the next run number from the seat's state directory `<seats root>/.state/<seat>/security-audit/`
#   (one more than the largest `run-<n>` entry there; a directory without one is a failure, since the seat's `prev`
#   would be unknown), the sweep unit's `units.tsv` row (`units-row.py <store> add --id <sweep unit> --track sweep
#   --state in-flight --head <head> --brief briefs/<brief file> --note <text>`, the sweep unit the `U<n>` the brief's
#   file name starts with, the brief a regular file under `<store>/briefs/` the coordinator wrote before the run from
#   the previous one), then the TASK line as one argument through `hcom-dispatch <team> <from> <to> <line>` on PATH:
#   `TASK v1 task_id=<sweep unit> brief=<brief path> head=<head> pr=<pr> branch=<branch> unit=<unit> run=run-<n>
#   prev=run-<n-1> seat=<seat> (read the brief whole; the seat checkout is positioned at the head[; <--sweep-note>])`,
#   the form of every sweep TASK on the bus since run-150 (bus rows 22208, 22235, 22252), its receipt `id=<n> at=<ts>
#   to=<to> kind=TASK` kept in the receipt line and the decisions row. The sweep seat is named twice because hcom
#   names a seat (`rose`) and the seats root names its checkout (`sweep-3`): `--sweep-seat` is the checkout and state
#   directory, `--sweep-to` the hcom name the TASK is addressed to. (g) `audit`, unless `--no-audit`: `pr-audit.sh
#   <pr> --records <store> --cyber-program daybreak_blue` (on PATH) started in the background from the checkout with
#   stdin closed and its output to `<store>/audits/<unit>-<sha8>.txt` (the directory made when missing; a file already
#   there, an earlier run at this head, is left alone and the output goes to `<unit>-<sha8>.<UTC clock>.txt`), its pid
#   printed with how to read the file (the last two lines are the verdict path and `Verdict: <word>`; the coordinator
#   copies the file and writes the ledger row as the hcom-orchestration SKILL step 4 says). (h) `ci`, unless `--no-ci`:
#   `gh pr checks <pr> --repo <owner>/<repo> --watch --interval 60 --fail-fast` started the same way to
#   `<store>/audits/<unit>-<sha8>-ci.txt`. These two are the lever's only background children, and each receipt
#   begins `pid=<n> output=<file>` so the coordinator can find or stop the child (`kill -0 <n>`, `kill <n>`) and a
#   test can wait for its exit. The lever waits for neither. (i) `decisions`: one row of phase `round` in
#   `<store>/decisions.tsv` (`ts phase decision why evidence result`) naming the pushed head, the update-branch
#   receipt, the carry's outcome, the sweep unit and run with its receipt or `no sweep`, the audit's pid and output
#   file or `no audit`, the CI watch's or `no CI watch`; the row is appended through `python3 -I -S` with
#   `os.open(O_WRONLY | O_APPEND | O_NOFOLLOW)` and an `fstat` for a regular file, one `os.write` of the whole line
#   (stall-watch.sh's append). Nothing else is written: the lever never merges a pull request, never edits a body,
#   never kills a process, writes no brief (the body and the sweep brief are the coordinator's, written before the
#   run), and reads nothing from the bus.
#
#   Before anything the lever refuses (exit 2, one stderr line `round-advance.sh: refused: <reason>`, nothing on
#   stdout, nothing written): an argument holding a tab, a newline or a carriage return (the rows are tab-separated
#   lines), a `--sweep-note` holding a backtick or `$(` (a line pasted into a shell later must hold none; one was
#   executed on 2026-11-19), a missing or second store, unit or pull request, a unit outside `U<n>` or `U<n><letter>`,
#   a pull request that is not 1 to 10 decimal digits, an unknown option or a repeated one, no `--tree`, a tree that
#   is not a git work tree on a branch, `--sweep-brief` with `--no-sweep` (two answers), neither of them (the round's
#   sweep is an explicit choice: pr-merge.sh requires it by path class), `--sweep-brief` without `--sweep-seat` or
#   `--sweep-to`, a brief that is not a regular file directly under `<store>/briefs/` named `U<n>-<slug>.md`, a seat,
#   hcom name, team or sender outside hcom-dispatch's identifier grammar `^[a-z0-9][a-z0-9_-]{0,63}$`, a seat checkout
#   or its `security-audit` state directory that is missing, a wait or poll that is not 1 to 86400 seconds, a store
#   that cannot be entered (resolved with `pwd -P`) or whose `units.tsv`, `ledger.tsv` or `decisions.tsv` is not a
#   regular file (a link included) or whose `briefs` is not a directory, a current directory outside a git work tree
#   or whose top level has no `scripts/orchestrator/audit-carry.py`, no `units-row.py` or `ledger-row.py` beside this
#   lever, or no `python3`, `gh`, `hcom-dispatch`, `pr-update-branch.sh` or `pr-audit.sh` on PATH (the ones the chosen
#   steps need). Installed as `~/.local/bin/common/round-advance.sh` by the generator's copy and pin
#   (`claude.levers.sha256.round-advance.sh`), with no allow rule and no seat policy row: the coordinator runs it
#   outside every seat; `tests/unit/test_round_advance.py` runs the checkout script and the installed layout over a
#   scratch store, a bare fake origin and a worker tree with `gh`, `hcom-dispatch`, `pr-update-branch.sh`,
#   `pr-audit.sh` and `audit-carry.py` as recording stubs, and waits for the pids the `audit` and `ci` receipts name
#   before the scratch store is removed.
# @arg $1 path The program store directory holding units.tsv, ledger.tsv, decisions.tsv and briefs/.
# @arg $2 string The unit, `U<n>` or `U<n><letter>`.
# @arg $3 int The pull request number.
# @option --tree <dir> The worker tree, a repository of its own on the unit's branch.
# @option --sweep-brief <file> The sweep unit's brief under `<store>/briefs/`, written before the run; names the sweep unit by its file name and turns the sweep step on.
# @option --sweep-seat <seat> The sweep seat's directory name under the seats root (`sweep-3`): its checkout and its `.state/<seat>/security-audit/` runs.
# @option --sweep-to <name> The sweep seat's hcom name (`rose`), the TASK's recipient.
# @option --no-sweep No sweep this round (the explicit alternative to `--sweep-brief`).
# @option --no-audit Start no `pr-audit.sh`.
# @option --no-ci Start no CI watch.
# @option --team <thread> The hcom thread of the TASK (default `$HCOM_TEAM`, else `regime`).
# @option --from <sender> The TASK's sender identity (default `coordinator`).
# @option --seats-root <dir> The seats root (default `$REGIME_SEATS_ROOT`, else `~/.local/state/omp-seats/<slug of the checkout>`, regime-env's rule).
# @option --sweep-note <text> Appended to the TASK's parenthesis after `; `.
# @env ROUND_ADVANCE_HEAD_WAIT_SECONDS Seconds to wait for the head to change after `pr-update-branch.sh` (default 60).
# @env ROUND_ADVANCE_POLL_SECONDS Seconds between two head reads in that wait (default 5).
# @env HCOM_TEAM The default `--team`.
# @env REGIME_SEATS_ROOT The default `--seats-root`.
# @stdout One line per step done, `round-advance: <step> <result>`: `fetch`, `push`, `update-branch`, `carry`, `units`, `sweep`, `audit`, `ci`, `decisions`; the `audit` and `ci` receipts begin `pid=<n> output=<file>`, the background child's pid and its output file.
# @exitcode 0 Every chosen step ran and the decisions row is appended.
# @exitcode 1 A step failed: one stderr line names it, what failed and what was done before it; the receipts of the steps done are on stdout.
# @exitcode 2 Refused before the first step: a bad argument, a store that is not a store, a missing tree, tool or lever.
# @example
#   round-advance.sh ~/.local/state/regime-store/dotfiles/regime-cutover U624 816 --tree /tmp/dotfiles-wt/U624 --sweep-brief ~/.local/state/regime-store/dotfiles/regime-cutover/briefs/U644-security-audit-sweep-u624-head.md --sweep-seat sweep-3 --sweep-to rose
#   round-advance.sh ~/.local/state/regime-store/dotfiles/regime-cutover U620 815 --tree /tmp/dotfiles-wt/U620 --no-sweep --no-audit
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

lever='round-advance.sh'
usage='usage: round-advance.sh <store> <unit> <pr> --tree <worker tree> (--sweep-brief <file> --sweep-seat <seat> --sweep-to <hcom name> | --no-sweep) [--no-audit] [--no-ci] [--team <thread>] [--from <sender>] [--seats-root <dir>] [--sweep-note <text>]'

# @description Print the refusal in the levers' one-line form on stderr and exit 2; nothing was printed on stdout
#   and nothing written.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# The receipts of the steps done so far, for the failure line: the coordinator reads what stands and finishes the rest.
done_so_far=''

# @description Stop the sequence at a failed step: one stderr line names the step, what failed and what was done
#   before it; the receipts already printed stay on stdout; exit 1.
# @arg $1 string The step.
# @arg $@ string What failed.
fail() {
    local step=$1
    shift
    echo "${lever}: ${step} failed: $*; done before it: ${done_so_far:-nothing}" >&2
    exit 1
}

# @description Print one step's receipt on stdout and remember it for the failure line.
# @arg $1 string The step.
# @arg $@ string The result.
receipt() {
    local step=$1
    shift
    printf 'round-advance: %s %s\n' "${step}" "$*"
    done_so_far="${done_so_far:+${done_so_far}; }${step}"
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

# The shapes every value is held to before it reaches a command line or a row.
unit_shape='^U[0-9]+[a-z]?$'
pr_shape='^[1-9][0-9]{0,9}$'
sha_shape='^[0-9a-f]{40}$'
seconds_shape='^(0|[1-9][0-9]{0,9})$'
# hcom-dispatch's identifier grammar, for the team, the sender, the seat and its hcom name.
identifier_shape='^[a-z0-9][a-z0-9_-]{0,63}$'
# A sweep brief's file name: the sweep unit, a dash, a slug, `.md` (units-row.py's brief cell grammar).
brief_shape='^(U[0-9]+[a-z]?)-[A-Za-z0-9._-]+\.md$'
# The owner and repository `gh repo view` names, the one text that enters the push URL.
repo_shape='^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$'
# The receipt pr-update-branch.sh prints.
update_shape='^updated pr=([0-9]+) old=([0-9a-f]{40}) new=([0-9a-f]{40})$'
# The line audit-carry.py prints for a carried head (ledger-row.py's CARRIED_LINE).
carried_shape='^carried ([0-9a-f]{40}) ([0-9a-f]{40}) ([0-9a-f]{64})$'
# A run directory of the sweep seat's state.
run_shape='^run-([1-9][0-9]{0,8})$'

for argument in "$@"; do
    case ${argument} in
    *$'\t'* | *$'\n'* | *$'\r'*) refuse 'an argument holds a tab, a newline or a carriage return; the rows are tab-separated lines' ;;
    esac
done

positional=() tree='' sweep_brief='' sweep_seat='' sweep_to='' no_sweep=0 no_audit=0 no_ci=0
team=${HCOM_TEAM:-regime} sender=coordinator seats=${REGIME_SEATS_ROOT:-} sweep_note=''
seen=''
# @description Refuse an option given twice.
# @arg $1 string The option.
once() {
    case " ${seen} " in
    *" $1 "*) refuse "$1 is given twice; ${usage}" ;;
    esac
    seen="${seen} $1"
}
# @description Refuse an option without its value.
# @arg $1 string The option.
# @arg $2 int The arguments left.
needs_value() {
    (($2 >= 2)) || refuse "$1 needs a value; ${usage}"
}
while (($#)); do
    case $1 in
    --tree | --sweep-brief | --sweep-seat | --sweep-to | --team | --from | --seats-root | --sweep-note)
        once "$1"
        needs_value "$1" $#
        case $1 in
        --tree) tree=$2 ;;
        --sweep-brief) sweep_brief=$2 ;;
        --sweep-seat) sweep_seat=$2 ;;
        --sweep-to) sweep_to=$2 ;;
        --team) team=$2 ;;
        --from) sender=$2 ;;
        --seats-root) seats=$2 ;;
        --sweep-note) sweep_note=$2 ;;
        esac
        shift 2
        ;;
    --no-sweep | --no-audit | --no-ci)
        once "$1"
        case $1 in
        --no-sweep) no_sweep=1 ;;
        --no-audit) no_audit=1 ;;
        --no-ci) no_ci=1 ;;
        esac
        shift
        ;;
    --*) refuse "unknown option $1; ${usage}" ;;
    *)
        positional+=("$1")
        shift
        ;;
    esac
done
((${#positional[@]} == 3)) || refuse "a store, a unit and a pull request are needed, ${#positional[@]} given; ${usage}"
given=${positional[0]} unit=${positional[1]} pr=${positional[2]}
[[ ${unit} =~ ${unit_shape} ]] || refuse "the unit ${unit} is not U<n> or U<n><letter>"
[[ ${pr} =~ ${pr_shape} ]] || refuse "the pull request ${pr} is not a decimal number"
[[ -n ${tree} ]] || refuse "--tree <worker tree> is needed; ${usage}"
if [[ -n ${sweep_brief} ]]; then
    ((! no_sweep)) || refuse '--sweep-brief and --no-sweep are two answers to one question; give one'
    [[ -n ${sweep_seat} ]] || refuse '--sweep-brief needs --sweep-seat <seat>, the seat directory under the seats root'
    [[ -n ${sweep_to} ]] || refuse '--sweep-brief needs --sweep-to <hcom name>, the seat as hcom names it'
else
    ((no_sweep)) || refuse "the round's sweep is an explicit choice: give --sweep-brief <file> (with --sweep-seat and --sweep-to) or --no-sweep"
fi
for name in "${team}" "${sender}" ${sweep_seat:+"${sweep_seat}"} ${sweep_to:+"${sweep_to}"}; do
    [[ ${name} =~ ${identifier_shape} ]] || refuse "the identifier ${name} is outside hcom-dispatch's ^[a-z0-9][a-z0-9_-]{0,63}\$"
done
case ${sweep_note} in
*'`'* | *\$\(*) refuse "the sweep note holds a backtick or a dollar-parenthesis; a dispatch text pasted into a shell later must hold neither" ;;
esac
head_wait=${ROUND_ADVANCE_HEAD_WAIT_SECONDS:-60} poll=${ROUND_ADVANCE_POLL_SECONDS:-5}
for value in "${head_wait}" "${poll}"; do
    [[ ${value} =~ ${seconds_shape} ]] || refuse "ROUND_ADVANCE_HEAD_WAIT_SECONDS and ROUND_ADVANCE_POLL_SECONDS are 1 to 86400 seconds, not ${value}"
    ((value >= 1 && value <= 86400)) || refuse "ROUND_ADVANCE_HEAD_WAIT_SECONDS and ROUND_ADVANCE_POLL_SECONDS are 1 to 86400 seconds, not ${value}"
done

# The levers beside this file, found by the same split as the self-check's.
case ${BASH_SOURCE[0]} in
*/*) here=${BASH_SOURCE[0]%/*} ;;
*) here=. ;;
esac
[[ -n ${here} ]] || here=/
here=$(cd "${here}" && pwd -P) || refuse "the script directory of ${BASH_SOURCE[0]} cannot be resolved"
units_row=${here}/units-row.py
ledger_row=${here}/ledger-row.py
[[ -f ${units_row} && ! -L ${units_row} ]] || refuse "no units-row.py beside ${here}/${lever}"
[[ -f ${ledger_row} && ! -L ${ledger_row} ]] || refuse "no ledger-row.py beside ${here}/${lever}"
command -v python3 > /dev/null || refuse 'no python3 on PATH; the rows are written through it'
for tool in gh pr-update-branch.sh; do
    command -v "${tool}" > /dev/null || refuse "no ${tool} on PATH"
done
((no_sweep)) || command -v hcom-dispatch > /dev/null || refuse 'no hcom-dispatch on PATH; the sweep TASK goes through it'
((no_audit)) || command -v pr-audit.sh > /dev/null || refuse 'no pr-audit.sh on PATH; the audit runs through it'

store=$(cd -- "${given}" 2> /dev/null && pwd -P) || refuse "the store ${given} is not a directory that can be entered"
for record in units.tsv ledger.tsv decisions.tsv; do
    [[ -f ${store}/${record} && ! -L ${store}/${record} ]] || refuse "${store}/${record} is not a regular file"
done
[[ -w ${store}/units.tsv && -w ${store}/decisions.tsv ]] || refuse "${store}/units.tsv or decisions.tsv cannot be written; the rows go there"
[[ -d ${store}/briefs && ! -L ${store}/briefs ]] || refuse "${store}/briefs is not a directory"

# The main checkout: the repository of the current directory, where pr-audit.sh runs and audit-carry.py lies.
checkout=$(git rev-parse --show-toplevel 2> /dev/null) || refuse 'the current directory is not inside a git work tree; run from the main checkout'
carry_lever=${checkout}/scripts/orchestrator/audit-carry.py
[[ -f ${carry_lever} && ! -L ${carry_lever} ]] || refuse "no scripts/orchestrator/audit-carry.py in the checkout ${checkout}"

# The worker tree: a work tree of its own on a branch.
[[ -d ${tree} ]] || refuse "the worker tree ${tree} is not a directory"
tree=$(cd -- "${tree}" && pwd -P) || refuse "the worker tree ${tree} cannot be entered"
inside=$(git -C "${tree}" rev-parse --is-inside-work-tree 2> /dev/null) || refuse "the worker tree ${tree} is not a git work tree"
[[ ${inside} == true ]] || refuse "the worker tree ${tree} is not a git work tree"
branch=$(git -C "${tree}" symbolic-ref --short HEAD 2> /dev/null) || refuse "the worker tree ${tree} is not on a branch"
[[ ${branch} =~ ^[A-Za-z0-9._/-]+$ ]] || refuse "the branch ${branch} is outside [A-Za-z0-9._/-]"

sweep_unit='' brief_name='' seat_checkout='' seat_state=''
if [[ -n ${sweep_brief} ]]; then
    [[ -f ${sweep_brief} && ! -L ${sweep_brief} ]] || refuse "the sweep brief ${sweep_brief} is not a regular file"
    brief_name=${sweep_brief##*/}
    [[ ${brief_name} =~ ${brief_shape} ]] || refuse "the sweep brief's name ${brief_name} is not U<n>-<slug>.md"
    sweep_unit=${BASH_REMATCH[1]}
    case ${sweep_brief} in
    */*) brief_dir=${sweep_brief%/*} ;;
    *) brief_dir=. ;;
    esac
    brief_dir=$(cd -- "${brief_dir}" && pwd -P) || refuse "the sweep brief's directory cannot be entered"
    [[ ${brief_dir} == "${store}/briefs" ]] || refuse "the sweep brief ${sweep_brief} is not directly under ${store}/briefs" # lint-comparisons: allow both sides are pwd -P forms
    if [[ -z ${seats} ]]; then
        slug=${checkout##*/}
        slug=$(printf '%s' "${slug}" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9_-' '-') || refuse "cannot derive the seats root slug from ${checkout}"
        slug=${slug:0:40}
        seats=${HOME}/.local/state/omp-seats/${slug}
    fi
    [[ -d ${seats} ]] || refuse "the seats root ${seats} is not a directory; give --seats-root"
    seats=$(cd -- "${seats}" && pwd -P) || refuse "the seats root ${seats} cannot be entered"
    seat_checkout=${seats}/${sweep_seat}
    seat_state=${seats}/.state/${sweep_seat}/security-audit
    [[ -d ${seat_checkout} ]] || refuse "the sweep seat checkout ${seat_checkout} is not a directory"
    inside=$(git -C "${seat_checkout}" rev-parse --is-inside-work-tree 2> /dev/null) || refuse "the sweep seat checkout ${seat_checkout} is not a git work tree"
    [[ ${inside} == true ]] || refuse "the sweep seat checkout ${seat_checkout} is not a git work tree"
    [[ -d ${seat_state} && ! -L ${seat_state} ]] || refuse "the sweep seat's state directory ${seat_state} is missing; the run number comes from it"
fi

# (a) fetch: GitHub's branch into the tree, merged when it moved.
git -C "${tree}" fetch origin "${branch}" > /dev/null 2>&1 || fail fetch "git -C ${tree} fetch origin ${branch} failed; nothing was merged or pushed"
remote_head=$(git -C "${tree}" rev-parse FETCH_HEAD) || fail fetch "cannot read FETCH_HEAD in ${tree}"
[[ ${remote_head} =~ ${sha_shape} ]] || fail fetch "FETCH_HEAD in ${tree} is no sha: ${remote_head}"
tree_head=$(git -C "${tree}" rev-parse HEAD) || fail fetch "cannot read HEAD in ${tree}"
[[ ${tree_head} =~ ${sha_shape} ]] || fail fetch "HEAD in ${tree} is no sha: ${tree_head}"
if git -C "${tree}" merge-base --is-ancestor FETCH_HEAD HEAD; then
    receipt fetch "origin/${branch} ${remote_head:0:8} is an ancestor of the tree head ${tree_head}; nothing to merge"
else
    status=$?
    ((status == 1)) || fail fetch "git merge-base --is-ancestor exited ${status} in ${tree}; nothing was merged or pushed"
    if ! git -C "${tree}" -c commit.gpgsign=false merge --no-ff --no-edit -m "Merge origin/${branch} (GitHub's update of the pull request branch) into the worker tree" FETCH_HEAD > /dev/null 2>&1; then
        conflicted=$(git -C "${tree}" diff --name-only --diff-filter=U) || conflicted='(the conflicted files could not be listed)'
        cell conflicted "${conflicted}"
        if [[ -n ${conflicted} ]]; then
            fail fetch "the merge of origin/${branch} ${remote_head:0:8} into ${tree} conflicts in: ${conflicted// /, }; the tree is left in that merge for the coordinator to resolve (git -C ${tree} merge --abort undoes it); nothing was pushed"
        fi
        fail fetch "the merge of origin/${branch} ${remote_head:0:8} into ${tree} failed with no conflicted file (git -C ${tree} status shows why); nothing was pushed"
    fi
    tree_head=$(git -C "${tree}" rev-parse HEAD) || fail fetch "cannot read HEAD in ${tree} after the merge"
    [[ ${tree_head} =~ ${sha_shape} ]] || fail fetch "HEAD in ${tree} after the merge is no sha: ${tree_head}"
    receipt fetch "origin/${branch} ${remote_head:0:8} merged into the tree, new head ${tree_head}"
fi

# (b) push: the tree's head fetched into the main checkout by path, then pushed through the credential route.
owner_repo=$(gh repo view --json owner,name --jq '.owner.login + "/" + .name') || fail push 'gh repo view could not name the repository; nothing was pushed'
[[ ${owner_repo} =~ ${repo_shape} ]] || fail push "gh repo view named no owner/repository: ${owner_repo}; nothing was pushed"
git fetch "${tree}" "${branch}" > /dev/null 2>&1 || fail push "git fetch ${tree} ${branch} failed in ${checkout}; nothing was pushed"
fetched=$(git rev-parse FETCH_HEAD) || fail push "cannot read FETCH_HEAD in ${checkout}; nothing was pushed"
[[ ${fetched} == "${tree_head}" ]] || fail push "the fetched ${branch} is ${fetched}, not the tree head ${tree_head}; nothing was pushed"
push_url=https://github.com/${owner_repo}
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null git -c 'credential.helper=!gh auth git-credential' push "${push_url}" "FETCH_HEAD:refs/heads/${branch}" > /dev/null 2>&1 ||
    fail push "git push ${push_url} FETCH_HEAD:refs/heads/${branch} failed (the head ${tree_head} is fetched into ${checkout} as FETCH_HEAD)"
receipt push "${tree_head} to ${push_url} refs/heads/${branch}"

# (c) update-branch: GitHub's merge of main into the branch, the new head read back until it changes or the wait passes.
update=$(pr-update-branch.sh "${pr}") || fail update-branch "pr-update-branch.sh ${pr} failed; the head ${tree_head} is pushed"
[[ ${update} =~ ${update_shape} ]] || fail update-branch "pr-update-branch.sh printed no receipt: ${update}; the head ${tree_head} is pushed"
old_head=${BASH_REMATCH[2]} new_head=${BASH_REMATCH[3]}
[[ ${old_head} == "${tree_head}" ]] || fail update-branch "the pull request's head before the update was ${old_head}, not the pushed ${tree_head}; the head is pushed and the update-branch ran"
waited=0 wait_note=''
while [[ ${new_head} == "${old_head}" ]] && ((waited < head_wait)); do
    sleep "${poll}"
    waited=$((waited + poll))
    new_head=$(gh pr view "${pr}" --json headRefOid --jq .headRefOid) || fail update-branch "gh pr view ${pr} could not read the head; the head ${tree_head} is pushed and the update-branch ran"
    [[ ${new_head} =~ ${sha_shape} ]] || fail update-branch "gh pr view ${pr} printed no head: ${new_head}; the head ${tree_head} is pushed and the update-branch ran"
done
head=${new_head}
[[ ${head} != "${old_head}" ]] || wait_note=" (unchanged after ${waited}s: the branch was already up to date, the pushed head is the round's head)"
receipt update-branch "pr=${pr} old=${old_head} new=${head}${wait_note}"

# (d) carry: the head fetched into the main checkout, then audit-carry.py's decision; a carried head is recorded and
# needs no sweep and no audit.
git fetch origin "${branch}" > /dev/null 2>&1 || fail carry "git fetch origin ${branch} failed in ${checkout}; the head ${head} stands on GitHub"
fetched=$(git rev-parse FETCH_HEAD) || fail carry "cannot read FETCH_HEAD in ${checkout}; the head ${head} stands on GitHub"
[[ ${fetched} == "${head}" ]] || fail carry "GitHub's ${branch} is ${fetched}, not the head ${head} read back after the update; the head stands on GitHub"
carried=0 carry_note=''
if carry_line=$(python3 -I "${carry_lever}" "${store}" "${unit}" "${pr}" "${head}" --repo "${checkout}" --base origin/main); then
    [[ ${carry_line} =~ ${carried_shape} ]] || fail carry "audit-carry.py exited 0 without a carried line: ${carry_line}; the head ${head} stands on GitHub"
    earlier=${BASH_REMATCH[1]}
    row=$(python3 -I "${ledger_row}" "${store}" carried --pr "${pr}" --head "${head}" --unit "${unit}" --line "${carry_line}" \
        --note "GitHub merge of main into the branch by pr-update-branch.sh through round-advance.sh; the diff against main is the audited head ${earlier:0:8}") ||
        fail carry "ledger-row.py carried failed for ${head} (audit-carry.py printed: ${carry_line}); the head stands on GitHub"
    carried=1
    carry_note="carried from ${earlier:0:8} (ledger ${row})"
    receipt carry "${carry_line}; ${row}; the sweep and the audit are skipped"
else
    status=$?
    ((status == 1)) || fail carry "audit-carry.py exited ${status} for ${head} (see its stderr above); the head stands on GitHub"
    cell carry_line "${carry_line}"
    carry_note=${carry_line:-not carried: audit-carry.py printed no line}
    receipt carry "${carry_note}; the head gets its own sweep and audit"
fi

# (e) units: the unit's row at the head.
row=$(python3 -I "${units_row}" "${store}" set --id "${unit}" --head "${head}") || fail units "units-row.py set --id ${unit} --head ${head} failed"
receipt units "${row}"

# (f) sweep: the seat positioned, the run numbered, the sweep unit's row, the TASK.
sweep_note_cell='no sweep'
if ((carried)); then
    sweep_note_cell='no sweep (carried head)'
elif ((! no_sweep)); then
    git -C "${seat_checkout}" fetch > /dev/null 2>&1 || fail sweep "git -C ${seat_checkout} fetch failed; the seat is not positioned, no row and no TASK"
    git -C "${seat_checkout}" checkout --detach "${head}" > /dev/null 2>&1 || fail sweep "git -C ${seat_checkout} checkout --detach ${head} failed; the seat is not positioned, no row and no TASK"
    seat_status=$(git -C "${seat_checkout}" status --porcelain) || fail sweep "git -C ${seat_checkout} status failed; the seat is at ${head} but unverified, no row and no TASK"
    [[ -z ${seat_status} ]] || fail sweep "the seat checkout ${seat_checkout} is not clean at ${head}; no row and no TASK"
    seat_head=$(git -C "${seat_checkout}" rev-parse HEAD) || fail sweep "cannot read HEAD in ${seat_checkout}; no row and no TASK"
    [[ ${seat_head} == "${head}" ]] || fail sweep "the seat checkout ${seat_checkout} is at ${seat_head}, not ${head}; no row and no TASK"
    last_run=0
    shopt -s nullglob
    for entry in "${seat_state}"/run-*; do
        name=${entry##*/}
        [[ ${name} =~ ${run_shape} ]] || continue
        ((BASH_REMATCH[1] <= last_run)) || last_run=${BASH_REMATCH[1]}
    done
    shopt -u nullglob
    ((last_run > 0)) || fail sweep "no run-<n> entry under ${seat_state}; the seat's prev run is unknown, no row and no TASK (the seat is positioned at ${head})"
    run=$((last_run + 1))
    row=$(python3 -I "${units_row}" "${store}" add --id "${sweep_unit}" --track sweep --state in-flight --head "${head}" --brief "briefs/${brief_name}" \
        --note "the security-audit sweep of ${unit} head ${head} (PR ${pr}) on ${sweep_seat} (run-${run}, prev run-${last_run}), required by pr-merge.sh; dispatched by round-advance.sh") ||
        fail sweep "units-row.py add --id ${sweep_unit} failed; the seat is positioned at ${head}, no TASK was sent"
    task="TASK v1 task_id=${sweep_unit} brief=${brief_dir}/${brief_name} head=${head} pr=${pr} branch=${branch} unit=${unit} run=run-${run} prev=run-${last_run} seat=${sweep_seat} (read the brief whole; the seat checkout is positioned at the head${sweep_note:+; ${sweep_note}})"
    dispatch=$(hcom-dispatch "${team}" "${sender}" "${sweep_to}" "${task}") || fail sweep "hcom-dispatch to ${sweep_to} failed; the seat is positioned at ${head} and the units row for ${sweep_unit} is added (${row}), the TASK was not sent"
    cell dispatch "${dispatch}"
    sweep_note_cell="sweep ${sweep_unit} run-${run} (prev run-${last_run}) on ${sweep_seat} to ${sweep_to}, receipt ${dispatch}"
    receipt sweep "${sweep_unit} run-${run} prev run-${last_run} on ${sweep_seat} at ${head}; ${row}; ${dispatch}"
fi

# (g) audit and (h) ci: in the background, their output to files under the store, the lever waits for neither.
audit_note='no audit' ci_note='no CI watch'
audits=${store}/audits
if ((carried)); then
    audit_note='no audit (carried head)'
fi
if ((! carried && ! no_audit)) || ((! no_ci)); then
    mkdir -p "${audits}" || fail audit "cannot make ${audits}"
    clock=$(date -u +%Y-%m-%dT%H:%M:%SZ) || fail audit 'the clock could not be read (date -u failed)'
    [[ ${clock} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] || fail audit "the clock is no timestamp: ${clock}"
fi
if ((! carried && ! no_audit)); then
    audit_out=${audits}/${unit}-${head:0:8}.txt
    [[ ! -e ${audit_out} ]] || audit_out=${audits}/${unit}-${head:0:8}.${clock}.txt
    pr-audit.sh "${pr}" --records "${store}" --cyber-program daybreak_blue < /dev/null > "${audit_out}" 2>&1 &
    audit_pid=$!
    audit_note="audit pid ${audit_pid} -> ${audit_out}"
    receipt audit "pid=${audit_pid} output=${audit_out}; read it with: tail -n 2 ${audit_out} (the verdict path, then Verdict: <word>, once the process has exited: kill -0 ${audit_pid})"
fi
if ((! no_ci)); then
    ci_out=${audits}/${unit}-${head:0:8}-ci.txt
    [[ ! -e ${ci_out} ]] || ci_out=${audits}/${unit}-${head:0:8}-ci.${clock}.txt
    gh pr checks "${pr}" --repo "${owner_repo}" --watch --interval 60 --fail-fast < /dev/null > "${ci_out}" 2>&1 &
    ci_pid=$!
    ci_note="CI watch pid ${ci_pid} -> ${ci_out}"
    receipt ci "pid=${ci_pid} output=${ci_out}; read it with: cat ${ci_out} (gh pr checks --watch prints the table when every check has ended, or at the first failure)"
fi

# (i) decisions: one row of phase `round`, appended through a descriptor that follows no link.
clock=$(date -u +%Y-%m-%dT%H:%M:%SZ) || fail decisions 'the clock could not be read (date -u failed)'
[[ ${clock} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] || fail decisions "the clock is no timestamp: ${clock}"
decision='' why='' evidence='' result=''
cell decision "${unit} round advanced by round-advance.sh: PR ${pr} head ${head} (pushed ${tree_head}; update-branch old=${old_head} new=${head}${wait_note}; ${carry_note}); ${sweep_note_cell}; ${audit_note}; ${ci_note}"
cell why "standing orders 59 and 60; round-advance.sh (U624) ran the round's mechanics in one command"
evidence=${audit_out:-${ci_out:-${store}/units.tsv}}
cell evidence "${evidence}"
cell result "${unit}${sweep_unit:+ ${sweep_unit}}"
printf -v row '%s\t%s\t%s\t%s\t%s\t%s\n' "${clock}" round "${decision}" "${why}" "${evidence}" "${result}"
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
        print(f"{path} {stop.code}", file=sys.stderr)
        sys.exit(1)
    raise
' "${store}/decisions.tsv" "${row}" < /dev/null || fail decisions "the row could not be appended to ${store}/decisions.tsv (the reason is above); every other step is done"
receipt decisions "appended ${clock} round ${unit}${sweep_unit:+ ${sweep_unit}} to ${store}/decisions.tsv"
