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
#   `mkdir .orchestration/validation/ci-reruns.lock.d/<run-id>`, one
#   `<utc>\t<run-id>\t<headSha>\t<job>\t<signature id>` row per job is appended to
#   `.orchestration/validation/ci-reruns.tsv`, and only then `gh run rerun <run-id> --failed`
#   runs. The reservation stays after success, failure or interruption, so a run is rerun at most
#   once, and it blocks only its own run. All of these live in the checkout this script lives in
#   (`git rev-parse --show-toplevel` there).
# @arg $1 int The workflow run id.
# @exitcode 0 Every candidate job matched a signature; the run was reserved and rerun once.
# @exitcode 1 A gh or jq call or the signature file failed (never gh's own codes), or the reserved rerun failed.
# @exitcode 2 Usage error, or the run has no failed, timed-out or cancelled job.
# @exitcode 3 A job matched no signature (`real failure: <job>`) or the head is superseded (`superseded: run <id>`).
# @exitcode 4 The run is already reserved or in ci-reruns.tsv; nothing was rerun.
# @example
#   scripts/orchestrator/ci-rerun.sh 39046848147
set -euo pipefail

if (($# != 1)) || [[ ! $1 =~ ^[0-9]+$ ]]; then
    echo "usage: ci-rerun.sh <run-id>" >&2
    exit 2
fi
run_id=$1
root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
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
    # The index form fails inside the Claude sandbox even with PyYAML cached, so the cache goes first.
    uv run --offline --no-project --quiet --with pyyaml python -I -c "${script}" "$1" < /dev/null 2> /dev/null ||
        uv run --no-project --quiet --with pyyaml python -I -c "${script}" "$1" < /dev/null
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
mkdir -p "${reservation%/*}"
if ! mkdir "${reservation}" 2> /dev/null; then
    echo "already rerun once: run ${run_id} was reserved by a concurrent call" >&2
    exit 4
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
