#!/usr/bin/env bash
# @file audit-pool.sh
# @brief Run queued task-level audits, at most --max at a time, and keep only schema-valid audit records.
# @description
#   Plan 024 5.12 (2) (T133). A request is `<queue>/<task>-<sha7>.request`, `key=value` lines: pr, head, base,
#   task and optionally previous_head. Under fcntl's exclusive lock on `<queue>/.lock` (python -I; macOS ships no
#   flock command) a pick renames the oldest request to `<task>-<sha7>.running-<n>`, n a free slot of --max: slot 1
#   audits in `.claude/worktrees/orchestrator-review`, slot n > 1 in `.claude/worktrees/orchestrator-review-<n>`
#   (added detached at origin/main when missing), passed to orch-audit.sh as ORCH_REVIEW_WORKTREE. A run is
#   `orch-audit.sh <task> --head <head> <pr> --json <v>/<task>-audit-<sha7>.json`, with `--previous-head` and
#   `--previous-findings <v>/<task>-audit-<prev7>.json` only once `<v>/audit-shadow.tsv` holds two rows whose last
#   field (the finding difference between the full and the differential audit) is 0 (plan 024 5.11 Q-C); until then
#   a request with previous_head is audited in full and its differential prompt is written to
#   `<json>.differential-prompt.txt`. A zero exit whose json passes `orch-audit.sh --validate` against
#   .schemas/audit.json renames the request to `.done`; anything else writes the reason to `<request>.rejected` and
#   renames it to `.blocked`. A run whose output mentions 429 is retried after 60, 120 and 240 seconds, then
#   blocked. `--once` (the default) starts what the free slots allow and waits; `--loop` picks every 30 seconds
#   until `<queue>/.stop` exists.
# @option --once Start what the free slots allow, then wait for those runs.
# @option --loop Pick every 30 seconds until `<queue>/.stop` exists.
# @option --max <n> Concurrent audits, 1 to 9 (default 2).
# @option --queue <dir> The queue directory (default .orchestration/validation/audit-queue).
# @exitcode 0 The pass or the loop ended; each request's outcome is its .done or .blocked file.
# @exitcode 2 Usage error.
set -euo pipefail

usage() {
    echo "usage: audit-pool.sh [--once|--loop] [--max <n>] [--queue <dir>]" >&2
    exit 2
}
mode=once max=2 queue=.orchestration/validation/audit-queue
while (($#)); do
    case $1 in
    --once | --loop) mode=${1#--} ;;
    --max | --queue)
        (($# >= 2)) || usage
        printf -v "${1#--}" '%s' "$2"
        shift
        ;;
    *) usage ;;
    esac
    shift
done
[[ ${max} =~ ^[1-9]$ ]] || usage
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd -- "$(git -C "${here}" rev-parse --show-toplevel)"
v=.orchestration/validation
mkdir -p -- "${queue}"
read -r -d '' pick << 'PY' || true
import fcntl, glob, os, sys
q, mx = sys.argv[1], int(sys.argv[2])
with open(os.path.join(q, ".lock"), "a") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    used = {p.rsplit("-", 1)[1] for p in glob.glob(os.path.join(q, "*.running-*"))}
    free = [n for n in range(1, mx + 1) if str(n) not in used]
    todo = sorted(glob.glob(os.path.join(q, "*.request")))
    if free and todo:
        os.rename(todo[0], f"{todo[0][:-len('.request')]}.running-{free[0]}")
        print(todo[0][: -len(".request")], free[0])
PY

# @description Audit one picked request and leave it `.done` or `.blocked`.
# @arg $1 path The request path without `.request`.
# @arg $2 int Its slot.
# @arg $3 path Its review worktree.
run_one() {
    local base=$1 running="$1.running-$2" wt=$3 pr="" head="" task="" previous_head="" k val rc attempt=0
    local delays=(60 120 240) extra=()
    while IFS='=' read -r k val; do
        case ${k} in pr | head | task | previous_head) printf -v "${k}" '%s' "${val}" ;; esac
    done < "${running}"
    local json="${v}/${task}-audit-${head:0:7}.json"
    if ! [[ ${pr} =~ ^[0-9]+$ && ${head} =~ ^[0-9a-f]{40}$ && ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ &&
        ${previous_head} =~ ^([0-9a-f]{40})?$ ]]; then
        echo "the request does not carry a valid pr, head, task and previous_head" > "${base}.request.rejected"
        mv -- "${running}" "${base}.blocked"
        return
    fi
    if [[ -n ${previous_head} ]]; then
        local findings="${v}/${task}-audit-${previous_head:0:7}.json"
        if [[ -f ${v}/audit-shadow.tsv && $(awk -F '\t' '$NF == "0"' "${v}/audit-shadow.tsv" | wc -l) -ge 2 ]]; then
            extra=(--previous-head "${previous_head}" --previous-findings "${findings}")
        else
            echo "Differential audit of ${task} at ${head}: give each finding of ${findings} (head ${previous_head})" \
                "the status fixed or still-open, and report new findings only on the hunks of git diff" \
                "${previous_head} ${head}." > "${json}.differential-prompt.txt"
        fi
    fi
    while true; do
        rc=0
        ORCH_REVIEW_WORKTREE="${wt}" "${here}/orch-audit.sh" "${task}" --head "${head}" "${pr}" --json "${json}" \
            ${extra[@]+"${extra[@]}"} > "${base}.log" 2>&1 || rc=$?
        if ((rc == 0 || attempt >= 3)) || ! grep -q 429 "${base}.log"; then
            break
        fi
        sleep "${delays[attempt]}"
        attempt=$((attempt + 1))
    done
    if ((rc == 0)) && "${here}/orch-audit.sh" --validate .schemas/audit.json "${json}" >> "${base}.log" 2>&1; then
        mv -- "${running}" "${base}.done"
    else
        {
            echo "orch-audit exited ${rc}; the audit json is not kept"
            tail -n 5 -- "${base}.log"
        } > "${base}.request.rejected"
        rm -f -- "${json}"
        mv -- "${running}" "${base}.blocked"
    fi
}

# @description Start a background run for every request the free slots allow.
start_free() {
    local line req slot wt
    while line="$(uv run --no-project python -I -c "${pick}" "${queue}" "${max}")" && [[ -n ${line} ]]; do
        read -r req slot <<< "${line}"
        wt="${PWD}/.claude/worktrees/orchestrator-review"
        ((slot == 1)) || wt+="-${slot}"
        [[ -d ${wt} ]] || git worktree add -q --detach "${wt}" origin/main
        run_one "${req}" "${slot}" "${wt}" &
    done
}

if [[ ${mode} == once ]]; then
    start_free
    wait
    exit 0
fi
until [[ -e ${queue}/.stop ]]; do
    start_free
    sleep 30
done
wait
