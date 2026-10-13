#!/usr/bin/env bash
# @file replay.sh
# @brief Replay a command with the executor's binaries in a detached worktree at origin/main.
# @description
#   Plan 007 T718 (C-18). Before a command enters rule or task text, it runs
#   once as an executor would: `env -i PATH=/usr/bin:/bin bash -c "<command>"`
#   inside a new detached worktree of `origin/main` (the ref as last fetched)
#   under `$TMPDIR`. The arguments are joined with spaces into that one command.
#   The command's output passes through, then `exit=<status>` is printed for
#   pasting, the worktree is removed with `git worktree remove --force`, and the
#   script exits with the command's status.
# @arg $@ string The command.
# @exitcode 2 Usage error.
# @example
#   scripts/orchestrator/replay.sh "grep -n -o 'never through a pipe' home/dot_agents/skills/agmsg-orchestration/SKILL.md"
set -euo pipefail

if (($# == 0)); then
    echo "usage: replay.sh <command…>" >&2
    exit 2
fi
root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
tree="$(mktemp -d "${TMPDIR:-/tmp}/replay.XXXXXX")/tree"
git -C "${root}" worktree add -q --detach "${tree}" origin/main
rc=0
(cd -- "${tree}" && env -i PATH=/usr/bin:/bin bash -c "$*") || rc=$?
echo "exit=${rc}"
git -C "${root}" worktree remove --force "${tree}"
rmdir -- "$(dirname -- "${tree}")"
exit "${rc}"
