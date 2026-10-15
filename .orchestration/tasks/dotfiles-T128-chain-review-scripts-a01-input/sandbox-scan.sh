#!/usr/bin/env bash
# sandbox-scan.sh <task>: C-29 interim, extracted from the scratchpad integrate-prep.sh (lines 34 to 38). Prints the unsandboxed mutation calls found in the worker sandbox record .orchestration/sandboxes/<task>.md, or one line saying none; a hit is judged before the audit.
set -euo pipefail
task=$1
cd "$(git rev-parse --show-toplevel)"
sb=".orchestration/sandboxes/${task%-fixtures}.md"
if [ -f "$sb" ]; then
  if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"; else echo "sandbox scan: no unsandboxed mutation call in $sb"; fi
fi
