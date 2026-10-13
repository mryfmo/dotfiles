#!/usr/bin/env bash
# @file three-repeat.sh
# @brief Run the three-repeat records search for one finding class and print the record's search line.
# @description
#   Plan 007 T718 (C-23). The class must be a slug of `[a-z0-9-]` (exit 2
#   otherwise), so no review text reaches a command. The records search is the
#   gate's own match: the files under `.orchestration/learning/mistakes/` with a
#   line that begins with `classes:` and contains the class (`grep -rl
#   '^classes:.*<class>'`), printed as `search: <class> -> <basenames, sorted,
#   or none>`. The CompactionDB search runs `uv run --no-project
#   .claude/hooks/contextdb_cli.py memory search <class>` with the class as one
#   argument (no shell), and prints its match count. Both run in the checkout
#   this script lives in (`git rev-parse --show-toplevel` there), never the
#   caller's: a PR worktree's CLI is PR-controlled code (thread 4253994697).
# @arg $1 string Class slug.
# @exitcode 0 Both searches ran.
# @exitcode 1 A search failed (the search line is printed first when it ran).
# @exitcode 2 Usage error, or the class is not a slug.
# @example
#   scripts/orchestrator/three-repeat.sh bookkeeping
set -euo pipefail

if (($# != 1)) || [[ ! $1 =~ ^[a-z0-9-]+$ ]]; then
    echo "usage: three-repeat.sh <class>   (a slug of [a-z0-9-])" >&2
    exit 2
fi
class=$1
root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
dir="${root}/.orchestration/learning/mistakes"
[[ -d ${dir} ]] || {
    echo "three-repeat: ${dir} does not exist" >&2
    exit 1
}
rc=0
files="$(/usr/bin/grep -rl -- "^classes:.*${class}" "${dir}")" || rc=$?
((rc <= 1)) || exit 1
records="$(if [[ -n ${files} ]]; then awk -F/ '{print $NF}' <<< "${files}" | LC_ALL=C sort | paste -sd, - | sed 's/,/, /g'; fi)"
echo "search: ${class} -> ${records:-none}"

memory="$(cd -- "${root}" && uv run --no-project .claude/hooks/contextdb_cli.py memory search "${class}")" || {
    echo "three-repeat: the CompactionDB search failed" >&2
    exit 1
}
echo "compactiondb: ${class} -> $(/usr/bin/grep -cE '^[0-9a-f]{8}-' <<< "${memory}" || true) matches"
