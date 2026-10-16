#!/usr/bin/env bash
# @file local-advisory.sh
# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
# @description
#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
# @arg $2 string The reviewed head, 40 hex characters.
# @arg $3 string The task id that owns the advisory findings, in the task id's form.
# @exitcode 0 No P0/P1 finding.
# @exitcode 2 No local review file, or a malformed task id, head or owner task id.
# @exitcode 3 A P0/P1 finding.
# @example
#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
set -euo pipefail
task=$1 head=$2 owner=$3
# Both name the files read and appended, so a / in either would reach outside .orchestration (the audit of b6ce4ff).
# The owner is written into the record verbatim, so it takes the task id's form too.
id='^[A-Za-z0-9][A-Za-z0-9._-]*$'
[[ $task =~ $id && $head =~ ^[0-9a-f]{40}$ && $owner =~ $id ]] || {
    echo "usage: local-advisory.sh <task> <40-hex head> <owner task>"
    exit 2
}
cd "$(git rev-parse --show-toplevel)"
h7=${head:0:7}
LR=".orchestration/validation/$task-local-review-$h7.md"
A=".orchestration/acceptance/$task.md"
[ -s "$LR" ] || {
    echo "no local review file $LR"
    exit 2
}
n=$(sed -n 's/^findings: //p' "$LR" | head -1)
[ "${n:-0}" != "0" ] || {
    echo "local review of $h7: no findings"
    exit 0
}
# A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
i=0 stop=0
while IFS= read -r line; do
    i=$((i + 1))
    case "$line" in
    *"[P0]"* | *"[P1]"*)
        echo "STOP: local finding $i of $h7 is P0/P1: $line"
        stop=1
        ;;
    *)
        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
        ;;
    esac
done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
[ "$stop" = 0 ] || exit 3
