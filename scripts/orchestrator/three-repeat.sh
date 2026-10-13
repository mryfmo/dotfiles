#!/usr/bin/env bash
# @file three-repeat.sh
# @brief Run the three-repeat records search for one finding class and print the record's search line.
# @description
#   Plan 007 T718 (C-23). The class must be a slug of `[a-z0-9-]` (exit 2
#   otherwise), so no review text reaches a command. The records search is the
#   gate's own match: the files under `.orchestration/learning/mistakes/` with a
#   line that begins with `classes:` and contains the class (`grep -rl
#   '^classes:.*<class>'`), printed as `search: <class> -> <basenames, sorted,
#   or none>`; beside it, the files that mention the class anywhere (`grep -rli
#   <class>`), printed as `search-body: <class> -> <basenames or none>`. The
#   CompactionDB search runs `uv run --no-project .claude/hooks/contextdb_cli.py
#   memory search --limit 1000 -- <class>` with the class as one argument after
#   `--` (no shell; a slug like `--help` is a query, never an option: thread
#   4254771284), and prints its match count, `>=1000 matches (capped)` when the
#   count reaches that limit (the CLI's default is 30: thread 4255494137). All
#   run in the checkout this script lives in (`git rev-parse --show-toplevel`
#   there), never the caller's: a PR worktree's CLI is PR-controlled code
#   (thread 4253994697).
# @arg $1 string Class slug.
# @exitcode 0 Every search ran.
# @exitcode 1 A search failed (the lines of the searches before it are printed).
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
# @description Print the sorted basenames of the records grep matches, or `none`.
# @arg $1 string grep options (`-rl` or `-rli`).
# @arg $2 string Pattern.
# @exitcode 1 grep failed (exit 2).
matches() {
    local files rc=0
    files="$(/usr/bin/grep "$1" -- "$2" "${dir}")" || rc=$?
    ((rc <= 1)) || return 1
    files="$(awk -F/ 'NF {print $NF}' <<< "${files}" | LC_ALL=C sort | paste -sd, - | sed 's/,/, /g')"
    printf '%s' "${files:-none}"
}
records="$(matches -rl "^classes:.*${class}")" || exit 1
echo "search: ${class} -> ${records}"
records="$(matches -rli "${class}")" || exit 1
echo "search-body: ${class} -> ${records}"

limit=1000
memory="$(cd -- "${root}" && uv run --no-project "${root}/.claude/hooks/contextdb_cli.py" memory search --limit "${limit}" -- "${class}")" || {
    echo "three-repeat: the CompactionDB search failed" >&2
    exit 1
}
n="$(/usr/bin/grep -cE '^[0-9a-f]{8}-' <<< "${memory}" || true)"
if ((n >= limit)); then
    echo "compactiondb: ${class} -> >=${limit} matches (capped)"
else
    echo "compactiondb: ${class} -> ${n} matches"
fi
