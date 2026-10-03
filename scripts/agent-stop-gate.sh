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
#   Worker seat: blocks when the latest `AGMSG-TASK` addressed to the seat's
#   `-aNNN` claude-code identity is newer than its latest `AGMSG-RESULT` or
#   `AGMSG-PONG`.
#
#   Messages come from the team-wide `history.sh <team>` read (the agmsg skill
#   forbids reading its database directly; without an agent argument the read
#   does not self-name a pane). The hook never writes and needs no network.
# @exitcode 0 Nothing is pending, or the checkout is not an agmsg seat.
# @exitcode 2 Work is pending; one reason line per violation on stderr.
# @example
#   echo '{"stop_hook_active":false,"cwd":"'"$PWD"'"}' | scripts/agent-stop-gate.sh
set -uo pipefail

# Same bounded stdin read and grep/sed field extraction as agmsg check-inbox.sh.
input=""
if [[ ! -t 0 ]]; then
    if command -v timeout > /dev/null 2>&1; then
        input="$(timeout 2 cat 2> /dev/null || true)"
    else
        input="$(cat 2> /dev/null || true)"
    fi
fi
active=false
if grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true' <<< "${input}"; then
    active=true
fi
cwd="$(sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' <<< "${input}" | head -1)"
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
reasons=()

if [[ ${seat} == orchestrator && ${active} == false ]]; then
    # GIT_OPTIONAL_LOCKS=0 keeps `git status` from refreshing the index.
    while IFS= read -r line; do
        path="${line:3}"
        case "${path}" in
        .orchestration/* | .agents/worklog/*) continue ;;
        esac
        reasons+=("uncommitted change outside .orchestration: ${path} (delegate it to a worker task or revert it)")
    done < <(GIT_OPTIONAL_LOCKS=0 git -C "${top}" status --porcelain --untracked-files=all 2> /dev/null)
fi

team=""
name=""
while IFS=$'\t' read -r row_team row_name; do
    suffixed=false
    [[ ${row_name} =~ -a[0-9]{3}$ ]] && suffixed=true
    if [[ ${seat} == worker && ${suffixed} == true ]] || [[ ${seat} == orchestrator && ${suffixed} == false ]]; then
        team="${row_team}"
        name="${row_name}"
        break
    fi
done < <(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${top}" claude-code 2> /dev/null)

if [[ -n ${name} ]]; then
    # ponytail: only the newest 200 team messages are read (~0.7 s) and an
    # unreadable store blocks every turn once; add a timestamp cap if a
    # 200-message window or a down store ever becomes a real problem.
    if ! history="$("${scripts}/history.sh" "${team}" "" 200 2> /dev/null)"; then
        [[ ${active} == true ]] || reasons+=("agmsg history unreadable for team ${team}; check ${scripts}/history.sh ${team}")
    else
        # Rows: `  <mark> [<ts>] <from> → <to>: <KIND> v1 task_id=<id> ...`.
        while IFS= read -r task; do
            [[ -n ${task} ]] || continue
            if [[ ${seat} == orchestrator ]]; then
                reasons+=("AGMSG-RESULT task_id=${task} has no AGMSG-ACCEPTANCE from ${name}; review it and send AGMSG-ACCEPTANCE v1 task_id=${task}")
            else
                reasons+=("AGMSG-TASK task_id=${task} to ${name} has no AGMSG-RESULT/AGMSG-PONG yet; finish it and send AGMSG-RESULT v1 task_id=${task} (or AGMSG-PONG v1 status=blocked) with agmsg-dispatch")
            fi
        done < <(awk -v me="${name}" -v seat="${seat}" '
            {
                from = $3; to = $5; sub(/:$/, "", to); kind = $6; id = ""
                for (i = 7; i <= NF; i++) if ($i ~ /^task_id=/) { id = substr($i, 9); break }
                if (id == "") next
                if (seat == "orchestrator") {
                    if (to == me && kind == "AGMSG-RESULT") pending[id] = 1
                    else if (from == me && (kind == "AGMSG-ACCEPTANCE" || kind == "AGMSG-TASK")) delete pending[id]
                } else if (to == me && kind == "AGMSG-TASK") {
                    open = id
                } else if (from == me && (kind == "AGMSG-RESULT" || kind == "AGMSG-PONG")) {
                    open = ""
                }
            }
            END {
                if (seat == "orchestrator") { for (id in pending) print id }
                else if (open != "") print open
            }' <<< "${history}")
    fi
fi

if [[ ${#reasons[@]} -gt 0 ]]; then
    printf 'agent-stop-gate: %s\n' "${reasons[@]}" >&2
    exit 2
fi
exit 0
