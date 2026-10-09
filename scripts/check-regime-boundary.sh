#!/usr/bin/env bash
# @file check-regime-boundary.sh
# @brief Check the agmsg regime Stop checklist at a session boundary.
# @description
#   Verifies the Stop list of the agmsg-orchestration skill for this
#   repository and prints one line per violation:
#   untracked `.orchestration` files in every registered checkout
#   (`git worktree list`); exactly one agmsg identity name across claude-code
#   and codex at the only active seat, the main checkout (an empty seat is
#   reported too); any identity at a linked worktree under `.claude/worktrees/`
#   (a worker still seated: `herdr-agents --remove-worker <worktree>`), and
#   more than one name per type at any other checkout; a seated main checkout whose HEAD is
#   not the `main` branch (a detached HEAD or another branch; a checkout with
#   no identity, such as a CI checkout, is never flagged); running
#   `crit _serve` review servers; a canonical clone (`chezmoi source-path`,
#   when it is not this working clone) with unmerged entries, a stash, or a
#   tracked or untracked difference from `origin/main` (else `HEAD`) under
#   `home/`, `install/` or `scripts/`, or uncommitted changes there that
#   already match `origin/main` while `HEAD` is behind it; leftover `<repo> worker <name>` Herdr
#   workspaces and worker tabs in the managed workspace (only when `herdr`
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

if [[ -x ${scripts}/identities.sh ]]; then
    # The only active seat is the main checkout (orchestrator): it holds
    # exactly one identity across both runtime types. Workers are seated on
    # demand in linked worktrees, so an identity left at one at a boundary is
    # a worker still seated; any other checkout is flagged only for a
    # per-type surplus.
    names="$({
        AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" claude-code 2> /dev/null || true
        AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${main}" codex 2> /dev/null || true
    } | cut -f 2 | sort -u | grep -c . || true)"
    if ((names == 0)); then
        violations+=("no agmsg identity at the active seat ${main} (expected one)")
    elif ((names > 1)); then
        violations+=("stray identities at the active seat ${main}: ${names} names across claude-code and codex (expected one)")
    fi
    # Only a seated orchestrator checkout must stay on main; a CI checkout
    # with no identity may sit at a detached HEAD.
    if ((names > 0)); then
        branch="$(git -C "${main}" symbolic-ref -q --short HEAD 2> /dev/null || true)"
        if [[ ${branch} != main ]]; then
            violations+=("orchestrator seat is not on main: ${branch:-detached at $(git -C "${main}" rev-parse --short HEAD 2> /dev/null || echo unknown)}")
        fi
    fi
    resolved_main="$(cd -- "${main}" && pwd -P)"
    for checkout in "${checkouts[@]}"; do
        resolved="$(cd -- "${checkout}" 2> /dev/null && pwd -P)" || resolved="${checkout}"
        [[ ${resolved} != "${resolved_main}" ]] || continue
        seated=0
        for agent_type in claude-code codex; do
            names="$(count_names "${checkout}" "${agent_type}")"
            seated=$((seated + names))
            if ((names > 1)); then
                violations+=("stray ${agent_type} identities at ${checkout}: ${names} names (expected one)")
            fi
        done
        if ((seated > 0)) && [[ ${resolved} == "${resolved_main}/.claude/worktrees/"* ]]; then
            worktree=".claude/worktrees/${resolved#"${resolved_main}/.claude/worktrees/"}"
            violations+=("worker still seated at ${worktree} (herdr-agents --remove-worker ${worktree})")
        fi
    done
fi

if command -v pgrep > /dev/null 2>&1 && pgrep -f 'crit _serve' > /dev/null 2>&1; then
    violations+=("crit review server still running (pgrep -f 'crit _serve')")
fi

# Canonical clone: the chezmoi source checkout, when it is not this working
# clone. It stays pull/apply only, so a diff, stash or unmerged entry there
# means something ran where it must not, and it blocks the operator's next
# pull and apply.
if command -v chezmoi > /dev/null 2>&1 &&
    src="$(chezmoi source-path 2> /dev/null)" &&
    canon="$(git -C "${src}" rev-parse --show-toplevel 2> /dev/null)" &&
    [[ "$(cd -- "${canon}" && pwd -P)" != "$(cd -- "${main}" && pwd -P)" ]]; then
    ref=HEAD
    if git -C "${canon}" rev-parse -q --verify origin/main > /dev/null 2>&1; then
        ref=origin/main
    fi
    if [[ -n "$(git -C "${canon}" ls-files -u 2> /dev/null)" ]]; then
        violations+=("canonical clone ${canon} has unmerged entries (git ls-files -u); finish or abort its pull")
    fi
    if [[ -n "$(git -C "${canon}" stash list 2> /dev/null)" ]]; then
        violations+=("canonical clone ${canon} carries a stash (git stash list); drop only the autostash entry once its content is on origin/main, and leave any other stash to its owner")
    fi
    files="$({
        git -C "${canon}" diff --name-only "${ref}" -- home install scripts 2> /dev/null || true
        git -C "${canon}" diff --cached --name-only "${ref}" -- home install scripts 2> /dev/null || true
        git -C "${canon}" ls-files --others --exclude-standard -- home install scripts 2> /dev/null || true
    } | sort -u | paste -sd , -)"
    if [[ -n ${files} ]]; then
        violations+=("canonical clone ${canon} differs from ${ref} under home/, install/ or scripts/: ${files}; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C ${canon} restore -SW --source=${ref} -- <files> and drop its autostash")
    else
        # Bytes equal to the ref still leave a stale HEAD with a dirty tree
        # after the pins PR merged; only a pull makes the clone clean.
        files="$({
            git -C "${canon}" diff --name-only HEAD -- home install scripts 2> /dev/null || true
            git -C "${canon}" diff --cached --name-only HEAD -- home install scripts 2> /dev/null || true
        } | sort -u | paste -sd , -)"
        if [[ -n ${files} ]]; then
            violations+=("canonical clone ${canon} has uncommitted changes under home/, install/ or scripts/ that already match ${ref} while HEAD is behind it: ${files}; pull it (git -C ${canon} pull) so its autostash re-applies as a no-op")
        fi
    fi
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
    # herdr-agents --add-worker seats a worker in its own tab of the managed
    # workspace (the one with a pane in the main checkout itself; attach mode
    # keeps the workspace's own label): a pane there whose cwd is a linked
    # worktree is a worker tab still open.
    while IFS=$'\t' read -r workspace_id label; do
        [[ -n ${workspace_id} ]] || continue
        herdr pane list --workspace "${workspace_id}" 2> /dev/null |
            jq -e --arg main "${main}" '.result.panes[]? | select(.cwd == $main)' > /dev/null 2>&1 || continue
        while IFS= read -r pane_label; do
            violations+=("additional worker tab still open in ${label}: ${pane_label} (herdr-agents --remove-worker)")
        done < <(herdr pane list --workspace "${workspace_id}" 2> /dev/null |
            jq -r --arg worktrees "${main}/.claude/worktrees/" \
                '[.result.panes[]? | select((.cwd // "") | startswith($worktrees)) | (.label // .pane_id)] | unique[]' 2> /dev/null)
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
