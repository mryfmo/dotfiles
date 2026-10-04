#!/usr/bin/env bash
# @file check-regime-boundary.sh
# @brief Check the agmsg regime Stop checklist at a session boundary.
# @description
#   Verifies the Stop list of the agmsg-orchestration skill for this
#   repository and prints one line per violation:
#   untracked `.orchestration` files in every registered checkout
#   (`git worktree list`); exactly one agmsg identity name across claude-code
#   and codex at each active seat (the main checkout and the manifest
#   `worker_worktree`; an empty seat is reported too), and more than one name
#   per type at any other checkout; running `crit _serve` review servers; leftover `<repo> worker <name>` Herdr
#   workspaces and added-worker tabs in the pair workspace (only when `herdr`
#   is reachable); and a bare-id orchestrator
#   seat lock, through the one implementation in
#   scripts/check-agent-runtime.py (`orchestrator_seat_lock_warnings`).
#   Every probe is read-only, and a missing tool skips its check.
# @option --report Print the same lines but always exit 0 (for validate-agent-assets).
# @exitcode 0 If no violation was found, or with --report.
# @exitcode 1 If at least one violation was found.
# @example
#   make check-regime-boundary
set -euo pipefail

report=false
if [[ ${1:-} == --report ]]; then
    report=true
fi
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
# Worker workspace labels are `<main checkout basename> worker <name>`, also
# when this script runs from a linked worktree.
main="${root}"
if common="$(git -C "${root}" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)"; then
    main="${common%/.git}"
fi
scripts="${HOME}/.agents/skills/agmsg/scripts"
violations=()

checkouts=()
while IFS= read -r checkout; do
    [[ -n ${checkout} ]] && checkouts+=("${checkout}")
done < <(git -C "${root}" worktree list --porcelain 2> /dev/null | sed -n 's/^worktree //p')
[[ ${#checkouts[@]} -gt 0 ]] || checkouts=("${root}")

for checkout in "${checkouts[@]}"; do
    while IFS= read -r path; do
        [[ -n ${path} ]] && violations+=("untracked .orchestration file in ${checkout}: ${path}")
    done < <(git -C "${checkout}" ls-files --others --exclude-standard -- .orchestration 2> /dev/null)
done

# @description Print the number of distinct agmsg identity names at a path.
# @arg $1 path Checkout path.
# @arg $2 string Agent type.
count_names() {
    AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "$1" "$2" 2> /dev/null | cut -f 2 | sort -u | grep -c . || true
}

worker_worktree="$(
    # shellcheck source=/dev/null
    [[ ! -f ${HOME}/.agents/model-profiles.env ]] || source "${HOME}/.agents/model-profiles.env"
    printf '%s' "${HERDR_AGENTS_WORKER_WORKTREE:-}"
)"

if [[ -x ${scripts}/identities.sh ]]; then
    # The active seats are the main checkout (orchestrator) and the manifest
    # worker_worktree (worker); each holds exactly one identity across both
    # runtime types. Other worktrees are not seats: only a per-type surplus
    # is flagged there.
    seats=("${main}")
    if [[ -n ${worker_worktree} && -d ${main}/${worker_worktree} ]]; then
        seats+=("${main}/${worker_worktree}")
    fi
    resolved_seats=" "
    for seat in "${seats[@]}"; do
        resolved_seats+="$(cd -- "${seat}" && pwd -P) "
    done
    for seat in "${seats[@]}"; do
        names="$({
            AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${seat}" claude-code 2> /dev/null || true
            AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${seat}" codex 2> /dev/null || true
        } | cut -f 2 | sort -u | grep -c . || true)"
        if ((names == 0)); then
            violations+=("no agmsg identity at the active seat ${seat} (expected one)")
        elif ((names > 1)); then
            violations+=("stray identities at the active seat ${seat}: ${names} names across claude-code and codex (expected one)")
        fi
    done
    for checkout in "${checkouts[@]}"; do
        resolved="$(cd -- "${checkout}" 2> /dev/null && pwd -P)" || resolved="${checkout}"
        [[ ${resolved_seats} != *" ${resolved} "* ]] || continue
        for agent_type in claude-code codex; do
            names="$(count_names "${checkout}" "${agent_type}")"
            if ((names > 1)); then
                violations+=("stray ${agent_type} identities at ${checkout}: ${names} names (expected one)")
            fi
        done
    done
fi

if command -v pgrep > /dev/null 2>&1 && pgrep -f 'crit _serve' > /dev/null 2>&1; then
    violations+=("crit review server still running (pgrep -f 'crit _serve')")
fi

if command -v herdr > /dev/null 2>&1 && command -v jq > /dev/null 2>&1 &&
    workspaces="$(herdr workspace list 2> /dev/null)"; then
    # The label prefix alone also matches another clone with the same
    # basename, so a workspace counts only when one of its panes has its cwd
    # in this main checkout (the find_managed_workspaces rule in herdr-agents).
    while IFS=$'\t' read -r workspace_id label; do
        [[ -n ${workspace_id} ]] || continue
        if herdr pane list --workspace "${workspace_id}" 2> /dev/null |
            jq -e --arg main "${main}" '.result.panes[]? | (.cwd // "") | select(. == $main or startswith($main + "/"))' > /dev/null 2>&1; then
            violations+=("additional worker workspace still open: ${label} (herdr-agents --remove-worker)")
        fi
    done < <(jq -r --arg prefix "$(basename -- "${main}") worker " \
        '.result.workspaces[]? | select(.workspace_id and ((.label // "") | startswith($prefix))) | [.workspace_id, .label] | @tsv' <<< "${workspaces}" 2> /dev/null)
    # herdr-agents --add-worker seats a worker in its own tab of the pair
    # workspace (the one with a pane in the main checkout itself; attach mode
    # keeps the workspace's own label): a pane there whose cwd is another
    # linked worktree than the manifest worker_worktree is an added worker.
    while IFS=$'\t' read -r workspace_id label; do
        [[ -n ${workspace_id} ]] || continue
        herdr pane list --workspace "${workspace_id}" 2> /dev/null |
            jq -e --arg main "${main}" '.result.panes[]? | select(.cwd == $main)' > /dev/null 2>&1 || continue
        while IFS= read -r pane_label; do
            violations+=("additional worker tab still open in ${label}: ${pane_label} (herdr-agents --remove-worker)")
        done < <(herdr pane list --workspace "${workspace_id}" 2> /dev/null |
            jq -r --arg worktrees "${main}/.claude/worktrees/" --arg seat "${worker_worktree:+${main}/${worker_worktree}}" \
                '[.result.panes[]? | select(((.cwd // "") | startswith($worktrees)) and (.cwd | rtrimstr("/")) != $seat)
                  | (.label // .pane_id)] | unique[]' 2> /dev/null)
    done < <(jq -r --arg prefix "$(basename -- "${main}") worker " \
        '.result.workspaces[]? | select(.workspace_id and ((.label // "") | startswith($prefix) | not)) | [.workspace_id, (.label // "")] | @tsv' <<< "${workspaces}" 2> /dev/null)
fi

while IFS= read -r warning; do
    [[ -n ${warning} ]] && violations+=("${warning#WARN: }")
done < <(
    python3 - "${root}" "${main}" << 'PY' 2> /dev/null
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("check_agent_runtime", root / "scripts/check-agent-runtime.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# The seat lock belongs to the main checkout, also when run from a worktree.
print("\n".join(module.orchestrator_seat_lock_warnings(Path(sys.argv[2]))))
PY
)

for violation in ${violations[@]+"${violations[@]}"}; do
    printf 'regime-boundary: %s\n' "${violation}"
done
if [[ ${report} == false && ${#violations[@]} -gt 0 ]]; then
    exit 1
fi
exit 0
