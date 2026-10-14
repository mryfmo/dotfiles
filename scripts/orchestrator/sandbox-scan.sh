#!/usr/bin/env bash
# @file sandbox-scan.sh
# @brief Print the unsandboxed mutation calls of a worker's sandbox record, so a hit is judged before the audit (C-29).
# @description
#   Reads `.orchestration/sandboxes/<task>.md`, a trailing `-fixtures` of the task id stripped. A line that names
#   `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` and a mutation (`git commit`, `git switch -c`,
#   `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> `, `tee `) but none of `counts`, `reads`, `lists`,
#   matched case-insensitively, is printed with its line number, then the judge line; with no such line, one line says
#   none. A missing record prints nothing.
# @arg $1 string Task id.
# @exitcode 0 Always.
# @example
#   scripts/orchestrator/sandbox-scan.sh dotfiles-T128-x-a01
set -euo pipefail
task=$1
cd "$(git rev-parse --show-toplevel)"
sb=".orchestration/sandboxes/${task%-fixtures}.md"
if [ -f "$sb" ]; then
    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then
        echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
    else
        echo "sandbox scan: no unsandboxed mutation call in $sb"
    fi
fi
