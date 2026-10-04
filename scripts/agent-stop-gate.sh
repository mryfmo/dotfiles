#!/usr/bin/env bash
# @file agent-stop-gate.sh
# @brief Claude Code Stop hook that keeps an agmsg seat from idling with work pending.
# @description
#   Reads the Stop hook JSON on stdin and classifies the session's checkout:
#   the main checkout is the orchestrator seat, a worktree under
#   `.claude/worktrees/` is a worker seat, and anything else passes.
#
#   Orchestrator seat: blocks on `git status` entries outside `.orchestration/`
#   and `.agents/worklog/` (skipped when `stop_hook_active` is true), and on an
#   `AGMSG-RESULT` addressed to the seat's unsuffixed claude-code identity that
#   has no later `AGMSG-ACCEPTANCE` or `AGMSG-TASK` re-dispatch from it.
#
#   Worker seat: blocks on every task_id whose latest `AGMSG-TASK` (or
#   `AGMSG-ACCEPTANCE status=revise`) addressed to a claude-code identity
#   registered at the worktree has no later `AGMSG-RESULT` or `AGMSG-PONG
#   status=blocked` for that task_id from it.
#
#   Every team the identity belongs to is checked. Messages come from the
#   whole team history through agmsg's own storage facade, the one
#   `history.sh` reads (the agmsg skill forbids reading its database
#   directly). The hook never writes and needs no network. Without an agmsg
#   install it passes; a failing identity lookup or an unreadable store blocks
#   unless `stop_hook_active` is true.
# @exitcode 0 Nothing is pending, or the checkout is not an agmsg seat.
# @exitcode 2 Work is pending; one reason line per violation on stderr.
# @example
#   echo '{"stop_hook_active":false,"cwd":"'"$PWD"'"}' | scripts/agent-stop-gate.sh
set -uo pipefail

# Same bounded stdin read as agmsg check-inbox.sh; jq decodes JSON escapes.
input=""
if [[ ! -t 0 ]]; then
    if command -v timeout > /dev/null 2>&1; then
        input="$(timeout 2 cat 2> /dev/null || true)"
    else
        input="$(cat 2> /dev/null || true)"
    fi
fi
active="$(jq -r '.stop_hook_active // false' <<< "${input}" 2> /dev/null)"
[[ ${active} == true ]] || active=false
cwd="$(jq -r '.cwd // empty' <<< "${input}" 2> /dev/null)"
cwd="${cwd:-${PWD}}"

# Main checkout as in check-regime-boundary.sh.
top="$(git -C "${cwd}" rev-parse --show-toplevel 2> /dev/null)" || exit 0
common="$(git -C "${cwd}" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)" || exit 0
main="${common%/.git}"
if [[ ${top} == "${main}" ]]; then
    seat=orchestrator
elif [[ ${top} == "${main}"/.claude/worktrees/* ]]; then
    seat=worker
else
    exit 0
fi

scripts="${HOME}/.agents/skills/agmsg/scripts"
# Without an agmsg install this is not a regime machine.
[[ -e ${scripts}/identities.sh ]] || exit 0
reasons=()

if [[ ${seat} == orchestrator && ${active} == false ]]; then
    exempt() { [[ $1 == .orchestration/* || $1 == .agents/worklog/* ]]; }
    # -z rows are `XY <path>`; a rename or copy row is followed by its source
    # path, and it is exempt only when both endpoints are. A trailing `rc=<n>`
    # record carries git's exit status (a real row has a space at offset 2).
    # GIT_OPTIONAL_LOCKS=0 keeps `git status` from refreshing the index.
    while IFS= read -r -d '' entry; do
        if [[ ${entry} == rc=* ]]; then
            [[ ${entry} == rc=0 ]] || reasons+=("git status failed in ${top} (${entry}); repair the checkout, the dirty-tree check could not run")
            continue
        fi
        xy="${entry:0:2}"
        path="${entry:3}"
        from=""
        [[ ${xy} == *[RC]* ]] && IFS= read -r -d '' from
        if exempt "${path}" && { [[ -z ${from} ]] || exempt "${from}"; }; then
            continue
        fi
        reasons+=("uncommitted change outside .orchestration: ${path}${from:+ (from ${from})} (delegate it to a worker task or revert it)")
    done < <(
        GIT_OPTIONAL_LOCKS=0 git -C "${top}" status --porcelain -z --untracked-files=all 2> /dev/null
        printf 'rc=%s\0' "$?"
    )
fi

# Team-wide history as `from<TAB>to<TAB>body` rows, chronological. This is the
# storage facade history.sh itself calls, without its per-recipient unread pass
# (~3 s on a 600-message team; the facade reads all of it in ~0.1 s).
# AGMSG_BUSY_TIMEOUT (agmsg's documented knob, default 5000 ms per sqlite call)
# keeps a contended store inside the 5 s hook timeout, so it fails closed
# instead of timing out. storage_history runs storage_init, which writes unless
# the store is already at the current schema revision; for the sqlite driver,
# read that revision first (the same read as storage_init's fast path) and
# treat any other store as unreadable rather than letting it be re-initialized.
read_history() {
    export AGMSG_BUSY_TIMEOUT=1000
    # shellcheck disable=SC1091
    source "${scripts}/lib/storage.sh" && agmsg_storage_load || return 1
    storage_store_exists "$1" || return 0
    if [[ ${_AGMSG_STORAGE_LOADED:-} == sqlite ]]; then
        [[ "$(agmsg_sqlite "$(_sqlite_db "$1")" 'PRAGMA user_version;' 2> /dev/null)" == "${_AGMSG_STORAGE_SCHEMA_REV:-}" ]] || return 1
    fi
    storage_history "$1" | jq -r '[.from, .to, .body] | @tsv'
}

# A lookup that runs but fails must not read as "no seat here"; it blocks once,
# like an unreadable store.
if ! identities="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${top}" claude-code 2> /dev/null)"; then
    identities=""
    [[ ${active} == true ]] || reasons+=("agmsg identity lookup failed for ${top}; check ${scripts}/identities.sh")
fi

# The orchestrator is the unsuffixed identity at the main checkout; any
# identity registered at a worker worktree (solo or -aNNN) is its worker.
while IFS=$'\t' read -r -u 3 team name; do
    [[ -n ${name} ]] || continue
    [[ ${seat} == orchestrator && ${name} =~ -a[0-9]{3}$ ]] && continue
    # ponytail: an unreadable store blocks every turn once; add a timestamp
    # cap or a fail-open switch if a down store ever becomes a real problem.
    if ! history="$(read_history "${team}" 2> /dev/null)"; then
        [[ ${active} == true ]] || reasons+=("agmsg history unreadable for team ${team}; check ${scripts}/history.sh ${team}")
        continue
    fi
    while IFS= read -r task; do
        [[ -n ${task} ]] || continue
        if [[ ${seat} == orchestrator ]]; then
            reasons+=("AGMSG-RESULT task_id=${task} in team ${team} has no AGMSG-ACCEPTANCE from ${name}; review it and send AGMSG-ACCEPTANCE v1 task_id=${task}")
        else
            reasons+=("AGMSG-TASK task_id=${task} in team ${team} to ${name} has no AGMSG-RESULT yet; finish it and send AGMSG-RESULT v1 task_id=${task} (or AGMSG-PONG v1 status=blocked) with agmsg-dispatch")
        fi
    done < <(awk -F '\t' -v me="${name}" -v seat="${seat}" '
        {
            n = split($3, w, " "); kind = w[1]; id = ""; status = ""
            for (i = 2; i <= n; i++) {
                if (id == "" && w[i] ~ /^task_id=/) id = substr(w[i], 9)
                if (status == "" && w[i] ~ /^status=/) status = substr(w[i], 8)
            }
            if (id == "") next
            if (seat == "orchestrator") {
                if ($2 == me && kind == "AGMSG-RESULT") pending[id] = 1
                else if ($1 == me && (kind == "AGMSG-ACCEPTANCE" || kind == "AGMSG-TASK")) delete pending[id]
            } else if ($2 == me && (kind == "AGMSG-TASK" || (kind == "AGMSG-ACCEPTANCE" && status == "revise"))) {
                pending[id] = 1
            } else if ($1 == me && (kind == "AGMSG-RESULT" || (kind == "AGMSG-PONG" && status == "blocked"))) {
                delete pending[id]
            }
        }
        END { for (id in pending) print id }' <<< "${history}")
done 3<<< "${identities}"

if [[ ${#reasons[@]} -gt 0 ]]; then
    printf 'agent-stop-gate: %s\n' "${reasons[@]}" >&2
    exit 2
fi
exit 0
