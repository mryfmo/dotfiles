#!/usr/bin/env bash
# @file check-regime-boundary.sh
# @brief Check the agmsg regime Stop checklist at a session boundary.
# @description
#   Verifies the Stop list of the agmsg-orchestration skill for this
#   repository and prints one line per violation:
#   untracked `.orchestration` files; more than one agmsg identity name per
#   registered checkout (`git worktree list`, claude-code and codex); running
#   `crit _serve` review servers; leftover `<repo> worker <name>` Herdr
#   workspaces (only when `herdr` is reachable); and a bare-id orchestrator
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

while IFS= read -r path; do
    [[ -n ${path} ]] && violations+=("untracked .orchestration file: ${path}")
done < <(git -C "${root}" ls-files --others --exclude-standard -- .orchestration 2> /dev/null)

if [[ -x ${scripts}/identities.sh ]]; then
    while IFS= read -r checkout; do
        for agent_type in claude-code codex; do
            names="$(AGMSG_RESOLVE_PROJECT=0 "${scripts}/identities.sh" "${checkout}" "${agent_type}" 2> /dev/null |
                cut -f 2 | sort -u | grep -c .)" || names=0
            if ((names > 1)); then
                violations+=("stray ${agent_type} identities at ${checkout}: ${names} names (expected one)")
            fi
        done
    done < <(git -C "${root}" worktree list --porcelain 2> /dev/null | sed -n 's/^worktree //p')
fi

if command -v pgrep > /dev/null 2>&1 && pgrep -f 'crit _serve' > /dev/null 2>&1; then
    violations+=("crit review server still running (pgrep -f 'crit _serve')")
fi

if command -v herdr > /dev/null 2>&1 && command -v jq > /dev/null 2>&1 &&
    workspaces="$(herdr workspace list 2> /dev/null)"; then
    while IFS= read -r label; do
        [[ -n ${label} ]] && violations+=("additional worker workspace still open: ${label} (herdr-agents --remove-worker)")
    done < <(jq -r --arg prefix "$(basename -- "${main}") worker " \
        '.result.workspaces[]? | .label // empty | select(startswith($prefix))' <<< "${workspaces}" 2> /dev/null)
fi

while IFS= read -r warning; do
    [[ -n ${warning} ]] && violations+=("${warning#WARN: }")
done < <(
    python3 - "${root}" << 'PY' 2> /dev/null
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("check_agent_runtime", root / "scripts/check-agent-runtime.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print("\n".join(module.orchestrator_seat_lock_warnings(root)))
PY
)

for violation in ${violations[@]+"${violations[@]}"}; do
    printf 'regime-boundary: %s\n' "${violation}"
done
if [[ ${report} == false && ${#violations[@]} -gt 0 ]]; then
    exit 1
fi
exit 0
