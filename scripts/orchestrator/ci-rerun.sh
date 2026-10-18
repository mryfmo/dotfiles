#!/usr/bin/env bash
# @file ci-rerun.sh
# @brief Rerun a CI run's failed jobs once, and only when every failure is a known flake.
# @description
#   Plan 024 P1-3 (T133 item 4). Reads the run's jobs with `gh run view <run-id> --json`, the
#   `--log-failed` output of each job whose conclusion is `failure`, and the signatures of
#   `.github/flakes.yaml` (a list of `{id, job, log_regex, note}`; `job` and `log_regex` are
#   extended regular expressions, matched with `grep -E` against the job name and its log).
#   When every failed job matches a signature it runs `gh run rerun <run-id> --failed` once and
#   appends `<utc>\t<run-id>\t<headSha>\t<job>\t<signature id>` per job to
#   `.orchestration/validation/ci-reruns.tsv`. A failed job that matches nothing is a real
#   failure: nothing is rerun. A run already in that file is never rerun again. Both files are
#   read in the checkout this script lives in (`git rev-parse --show-toplevel` there).
# @arg $1 int The workflow run id.
# @exitcode 0 Every failed job matched a signature; the run was rerun once and recorded.
# @exitcode 1 A gh call or the signature file failed.
# @exitcode 2 Usage error, or the run has no failed job.
# @exitcode 3 A failed job matched no signature (`real failure: <job>`); nothing was rerun.
# @exitcode 4 The run is already in ci-reruns.tsv; nothing was rerun.
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

if [[ -f ${ledger} ]] && awk -F '\t' -v id="${run_id}" '$2 == id { found = 1 } END { exit !found }' "${ledger}"; then
    echo "already rerun once: run ${run_id} is in ${ledger}" >&2
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

run="$(gh run view "${run_id}" --json jobs,status,conclusion,headSha,event)"
head_sha="$(jq -r '.headSha' <<< "${run}")"
failed="$(jq -r '.jobs[] | select(.conclusion == "failure") | [.databaseId, .name] | @tsv' <<< "${run}")"
if [[ -z ${failed} ]]; then
    echo "run ${run_id} has no failed job" >&2
    exit 2
fi
known="$(signatures "${flakes}")"

matched=() real=0
while IFS=$'\t' read -r job_id job; do
    log="$(gh run view "${run_id}" --job "${job_id}" --log-failed)"
    signature=""
    while IFS=$'\t' read -r id job_regex log_regex; do
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
done <<< "${failed}"
((real == 0)) || exit 3

gh run rerun "${run_id}" --failed
mkdir -p "$(dirname -- "${ledger}")"
now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
for row in "${matched[@]}"; do
    printf '%s\t%s\t%s\t%s\n' "${now}" "${run_id}" "${head_sha}" "${row}" >> "${ledger}"
done
printf 'rerun: run %s, %d failed job(s), recorded in %s\n' "${run_id}" "${#matched[@]}" "${ledger}"
