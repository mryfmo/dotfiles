#!/usr/bin/env bash
# @file ci-rerun.sh
# @brief Rerun a CI run's failed jobs once, and only when every failure is a known flake of the current head.
# @description
#   Plan 024 P1-3 (T133). Reads the run with `gh run view <run-id> --json`, the log of each job
#   whose conclusion is `failure` (`--log-failed`), `timed_out` or `cancelled` (`--log`), and the
#   signatures of `.github/flakes.yaml` (a list of `{id, job, log_regex, note}`; `job` and
#   `log_regex` are extended regular expressions, matched with `grep -E` against the job name and
#   its log). A job with no log matches nothing. A pull-request run must belong to exactly one
#   pull request whose current head is the run's `headSha`, checked before the logs are read and
#   again right before the rerun: a superseded head's rerun would re-enter `pr-<N>` and cancel the
#   newest head's run. When every such job matches a signature, the run is reserved by an atomic
#   mkdir(2) of `.orchestration/validation/ci-reruns.lock.d/<run-id>` (through python3's os.mkdir), one
#   `<utc>\t<run-id>\t<headSha>\t<job>\t<signature id>` row per job is appended to
#   `.orchestration/validation/ci-reruns.tsv`, and only then `gh run rerun <run-id> --failed`
#   runs. The reservation stays after success, failure or interruption, so a run is rerun at most
#   once, and it blocks only its own run. All of these live in the checkout this script lives in
#   (`git rev-parse --show-toplevel` there). Before reading anything, uv, python3, gh, jq, git and mkdir are resolved
#   as `mise which` answers them under env -i from / (else `command -v`). Each answer is followed through every link
#   to its physical file, which must be an executable regular file and no shim: neither a file named mise in any
#   letter case nor the mise binary itself (same device and inode; a mise shim is a link to it), nor a file in a
#   directory named shims in any letter case, as found or as resolved. An answer (captured with its own trailing
#   newlines), link or directory whose path holds a control character is refused too; otherwise the script exits 1.
#   Only the checked physical file is ever run: all but python3 are linked by it into a private directory, created
#   under TMPDIR when it is absolute with no ':' or control character, else wherever mktemp puts it with TMPDIR unset,
#   then used only by its physical path, which must have no ':' either (else exit 1) and be this user's with mode 0700
#   (removed on exit and on HUP, INT or TERM), and PATH becomes those links then /usr/bin:/bin.
#   python3 is always started by its physical path, never a link (CPython reads a pyvenv.cfg beside and above the
#   path it starts by), as `python3 -I` and as uv's `--python` for `uv run --no-config --no-project` under env -i
#   from the root, so no checkout's `.python-version`, `.venv` or executable and no inherited UV_*, VIRTUAL_ENV or
#   PYTHON* variable picks the interpreter (security:4fe2438:1). Before PATH is pinned, every other command (mktemp,
#   env, find, ln and the EXIT trap's rm) runs by its absolute system path; mise, the resolver itself, is the one
#   program found through PATH.
# @arg $1 int The workflow run id.
# @exitcode 0 Every candidate job matched a signature; the run was reserved and rerun once.
# @exitcode 1 A tool resolves to a shim, a relative path or no executable regular file, a gh or jq call or the
#   signature file failed (never gh's own codes), or the reserved rerun failed.
# @exitcode 2 Usage error, a run not completed yet, or a run with no failed, timed-out or cancelled job.
# @exitcode 3 A job matched no signature (`real failure: <job>`) or the head is superseded (`superseded: run <id>`).
# @exitcode 4 The run is already reserved or in ci-reruns.tsv; nothing was rerun.
# @exitcode 129/130/143 Hung up, interrupted or terminated; the private directory is removed.
# @example
#   scripts/orchestrator/ci-rerun.sh 39046848147
set -euo pipefail

if (($# != 1)) || [[ ! $1 =~ ^[0-9]+$ ]]; then
    echo "usage: ci-rerun.sh <run-id>" >&2
    exit 2
fi
run_id=$1
# The private directory heads the pinned PATH, so a relative TMPDIR or one with a ':' (which would split it into
# entries the caller chose, an empty one being the cwd) or a control character is dropped for mktemp's own default.
# System paths: PATH is not pinned yet. macOS's -t ignores TMPDIR, so a usable one is named in the template.
if [[ ${TMPDIR-} == /* && ${TMPDIR} != *:* && ${TMPDIR} != *[[:cntrl:]]* ]]; then # lint-comparisons: allow an absolute-path and content test, not a comparison of two paths
    bin=$(/usr/bin/mktemp -d "${TMPDIR}/ci-rerun-bin.XXXXXX")
else
    bin=$(/usr/bin/env -u TMPDIR /usr/bin/mktemp -d -t ci-rerun-bin.XXXXXX)
fi
trap '/bin/rm -rf -- "${bin}"' EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

#
# @description Print the physical path of a directory, refusing one that holds a control character.
# @arg $1 string A directory.
#
function physical_dir() {
    local dir
    # The '.' keeps command substitution from stripping newlines that end the path itself.
    dir=$(cd -P -- "$1" 2> /dev/null && pwd -P && printf .) || return 1
    dir=${dir%.}
    dir=${dir%$'\n'}
    [[ ${dir} != *[[:cntrl:]]* ]] || return 1 # lint-comparisons: allow a control-character content test
    printf '%s\n' "${dir}"
}

#
# @description Print the physical path of a file, following every link of it and of its directories.
# @arg $1 string An absolute path.
# @exitcode 1 The path is relative, it or a link holds a control character, a link cannot be read, the chain is
#   longer than 40 links, or a directory does not exist.
#
function physical() {
    local path=$1 link dir hops=0
    [[ ${path} == /* && ${path} != *[[:cntrl:]]* ]] || return 1 # lint-comparisons: allow an absolute-path and content test
    while [[ -L ${path} ]]; do
        ((++hops <= 40)) || return 1
        # -n adds no delimiter (macOS's plain form drops one for a target that ends in a newline), and the '.' keeps
        # the target's own trailing newlines from command substitution.
        link=$(/usr/bin/readlink -n -- "${path}" && printf .) || return 1
        link=${link%.}
        [[ ${link} != *[[:cntrl:]]* ]] || return 1
        [[ ${link} == /* ]] || link=${path%/*}/${link} # lint-comparisons: allow an absolute-path prefix test
        path=${link}
    done
    dir=$(physical_dir "${path%/*}/") || return 1
    printf '%s/%s\n' "${dir%/}" "${path##*/}"
}

#
# @description Succeed when a tool is a shim: its physical file is named mise in any letter case or is the mise
#   binary, or the directory it was found in or resolves to is named shims in any letter case (a case-insensitive
#   file system accepts every spelling).
# @arg $1 string The path the tool was found at.
# @arg $2 string Its physical path.
#
function is_shim() {
    local dir
    [[ ${2##*/} == [Mm][Ii][Ss][Ee] ]] && return 0 # lint-comparisons: allow a file-name test, not a comparison of two paths
    [[ -n ${mise_bin} && $2 -ef ${mise_bin} ]] && return 0
    for dir in "${1%/*}/" "${2%/*}/"; do
        dir=$(physical_dir "${dir}") || return 0
        [[ ${dir}/ == */[Ss][Hh][Ii][Mm][Ss]/* ]] && return 0 # lint-comparisons: allow a directory-name test, not a comparison of two paths
    done
    return 1
}

# The caller's spelling of TMPDIR may pass through a link it can retarget once mktemp is done, so PATH, the links and
# the cleanup use only the physical directory; a colon-free spelling can still resolve to a path with a ':', which
# would split PATH again, so the rule is applied to the physical path.
physical_bin=$(physical_dir "${bin}") || physical_bin=''
[[ -z ${physical_bin} ]] || bin=${physical_bin}
if [[ ${physical_bin} != /* || ${physical_bin} == *:* ]]; then # lint-comparisons: allow an absolute-path and ':' content test
    echo "ci-rerun: the private directory ${bin} has no physical path that is absolute, without ':' or control characters" >&2
    exit 1
fi
private=$(/usr/bin/find "${bin}" -maxdepth 0 -perm 0700) || private=''
if ! [[ -n ${private} && -d ${bin} && ! -L ${bin} && -O ${bin} ]]; then
    trap - EXIT # not this run's directory: leave it alone
    echo "ci-rerun: the private directory ${bin} is not this user's with mode 0700" >&2
    exit 1
fi
# Each capture keeps the answer's own trailing newlines (the '.'), dropping only the one the resolver ends it with.
mise_bin=$(command -v mise && printf .) && mise_bin=${mise_bin%.} && mise_bin=$(physical "${mise_bin%$'\n'}") || mise_bin=''
for tool in python3 uv gh jq git mkdir; do
    found=$(cd / && { /usr/bin/env -i PATH="${PATH}" HOME="${HOME}" mise which "${tool}" 2> /dev/null || command -v "${tool}"; } && printf .) || found=''
    found=${found%.}
    found=${found%$'\n'}
    # A missing or non-executable link target would be skipped by PATH lookup and fall through to /usr/bin.
    if ! { real=$(physical "${found}") && [[ -f ${real} && -x ${real} ]]; }; then
        echo "ci-rerun: ${tool} is not an executable file ('${found}')" >&2
        exit 1
    fi
    if is_shim "${found}" "${real}"; then
        echo "ci-rerun: no ${tool} outside a shims directory ('${found}')" >&2
        exit 1
    fi
    if [[ ${tool} == python3 ]]; then
        py=${real}
    else
        /bin/ln -s -- "${real}" "${bin}/${tool}"
    fi
done
PATH="${bin}:/usr/bin:/bin"
# dirname is captured on its own line: inside the git call its status would be lost.
script_dir=$(dirname -- "${BASH_SOURCE[0]}") || exit 1
root="$(git -C "${script_dir}" rev-parse --show-toplevel)" || exit 1
flakes="${root}/.github/flakes.yaml"
ledger="${root}/.orchestration/validation/ci-reruns.tsv"
reservation="${root}/.orchestration/validation/ci-reruns.lock.d/${run_id}"

if [[ -d ${reservation} ]] ||
    { [[ -f ${ledger} ]] && awk -F '\t' -v id="${run_id}" '$2 == id { found = 1 } END { exit !found }' "${ledger}"; }; then
    echo "already rerun once: run ${run_id} is reserved in ${reservation%/*} or recorded in ${ledger}" >&2
    exit 4
fi

#
# @description Print each signature of the flake file as `id<TAB>job<TAB>log_regex`, refusing a malformed entry.
# @arg $1 string The flake file.
#
function signatures() {
    local script='import sys, yaml
entries = yaml.safe_load(open(sys.argv[1])) or []
if not isinstance(entries, list):
    sys.exit("ci-rerun: " + sys.argv[1] + " is not a list")
for entry in entries:
    fields = [entry.get(key) for key in ("id", "job", "log_regex")] if isinstance(entry, dict) else [None]
    if not all(isinstance(field, str) and field and "\t" not in field and "\n" not in field for field in fields):
        sys.exit("ci-rerun: malformed signature in " + sys.argv[1] + ": " + repr(entry))
    print("\t".join(fields))'
    local uvr=(env -i PATH="${PATH}" HOME="${HOME}" UV_CACHE_DIR="${HOME}/.cache/uv" uv run --no-config --no-project
        --quiet --python "${py}" --with pyyaml)
    # The index form fails inside the Claude sandbox even with PyYAML cached, so the cache goes first.
    (cd -- "${root}" && "${uvr[@]}" --offline python -I -c "${script}" "$1" < /dev/null 2> /dev/null) ||
        (cd -- "${root}" && "${uvr[@]}" python -I -c "${script}" "$1" < /dev/null)
}

#
# @description Exit 3 when the run's pull request has moved past its head, 1 when that cannot be read.
#
function require_current_head() {
    local prs current
    [[ ${event} == pull_request ]] || return 0
    prs="$(gh api "repos/{owner}/{repo}/actions/runs/${run_id}" --jq '[.pull_requests[].number | tostring] | join(" ")')" || exit 1
    if [[ ! ${prs} =~ ^[0-9]+$ ]]; then
        echo "ci-rerun: run ${run_id} belongs to no single pull request (${prs:-none})" >&2
        exit 1
    fi
    current="$(gh pr view "${prs}" --json headRefOid --jq .headRefOid)" || exit 1
    [[ ${current} =~ ^[0-9a-f]{40}$ ]] || {
        echo "ci-rerun: pull request ${prs} has no readable head" >&2
        exit 1
    }
    if [[ ${current} != "${head_sha}" ]]; then
        echo "superseded: run ${run_id} ran ${head_sha}, pull request ${prs} is at ${current}"
        exit 3
    fi
}

# A failed call exits 1: gh's and jq's own codes (gh 4 needs authentication, 2 cancelled) would read as this script's.
run="$(gh run view "${run_id}" --json jobs,status,conclusion,headSha,event)" || exit 1
head_sha="$(jq -r '.headSha // empty' <<< "${run}")" || exit 1
event="$(jq -r '.event // empty' <<< "${run}")" || exit 1
status="$(jq -r '.status // empty' <<< "${run}")" || exit 1
# A run in progress has jobs that are not final yet: --failed would rerun ones no signature checked.
if [[ ${status} != completed ]]; then
    echo "run ${run_id} is not completed (${status:-unknown}); nothing is rerun before it ends" >&2
    exit 2
fi
[[ ${head_sha} =~ ^[0-9a-f]{40}$ ]] || {
    echo "ci-rerun: run ${run_id} has no head sha" >&2
    exit 1
}
candidates="$(jq -r '.jobs[] | select(.conclusion == ("failure", "timed_out", "cancelled"))
    | [.databaseId, .name, .conclusion] | @tsv' <<< "${run}")" || exit 1
if [[ -z ${candidates} ]]; then
    echo "run ${run_id} has no failed, timed-out or cancelled job" >&2
    exit 2
fi
require_current_head
known="$(signatures "${flakes}")" || exit 1

matched=() real=0
while IFS=$'\t' read -r job_id job conclusion; do
    # --log-failed holds only failed steps; a timed-out or cancelled job's log is read whole.
    option=--log-failed
    [[ ${conclusion} == failure ]] || option=--log
    log="$(gh run view "${run_id}" --job "${job_id}" "${option}")" || exit 1
    signature=""
    while [[ -n ${log} ]] && IFS=$'\t' read -r id job_regex log_regex; do
        if grep -Eq -- "${job_regex}" <<< "${job}" && grep -Eq -- "${log_regex}" <<< "${log}"; then
            signature=${id}
            break
        fi
    done <<< "${known}"
    if [[ -z ${signature} ]]; then
        echo "real failure: ${job}"
        real=1
    else
        matched+=("${job}"$'\t'"${signature}")
    fi
done <<< "${candidates}"
((real == 0)) || exit 3

# Reserve before rerunning: the directory and the rows outlive a rerun that fails, is refused or is interrupted.
# The claim is mkdir(2) itself: uutils' mkdir (Ubuntu 26.04) returned 0 for a directory another call had just created,
# until uutils bf423f388d (2026-08-28), so the mkdir binary cannot decide which of two concurrent calls wins.
mkdir -p "${reservation%/*}"
claim=0
"${py}" -I -c 'import os, sys
try:
    os.mkdir(sys.argv[1])
except FileExistsError:
    sys.exit(4)' "${reservation}" 2> /dev/null || claim=$?
if ((claim == 4)); then
    echo "already rerun once: run ${run_id} was reserved by a concurrent call" >&2
    exit 4
elif ((claim != 0)); then
    echo "ci-rerun: cannot create ${reservation}" >&2
    exit 1
fi
now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
for row in "${matched[@]}"; do
    printf '%s\t%s\t%s\t%s\n' "${now}" "${run_id}" "${head_sha}" "${row}" >> "${ledger}"
done
require_current_head
if ! gh run rerun "${run_id}" --failed; then
    echo "ci-rerun: gh run rerun failed; run ${run_id} stays reserved in ${reservation%/*}" >&2
    exit 1
fi
printf 'rerun: run %s, %d job(s), recorded in %s\n' "${run_id}" "${#matched[@]}" "${ledger}"
