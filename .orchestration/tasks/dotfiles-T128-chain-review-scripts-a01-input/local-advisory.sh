#!/usr/bin/env bash
# local-advisory.sh <task> <head40> <owner-task-id>: plan 020 step 1.2 for the local review. Reads .orchestration/validation/<task>-local-review-<head7>.md; for each finding: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2), a P2/P3 appends a row `local:<head7>:<n>\tadvisory-p2` under the heading `## Owned by <owner>` of the acceptance record (created when missing) and a `local-finding: <head7>:<n> not-applicable:advisory P2 owned by <owner>; evidence=…` line. Exit 3 on a P0/P1, 0 otherwise.
set -euo pipefail
task=$1; head=$2; owner=$3
cd "$(git rev-parse --show-toplevel)"
h7=${head:0:7}
LR=".orchestration/validation/$task-local-review-$h7.md"
A=".orchestration/acceptance/$task.md"
[ -s "$LR" ] || { echo "no local review file $LR"; exit 2; }
n=$(sed -n 's/^findings: //p' "$LR" | head -1)
[ "${n:-0}" != "0" ] || { echo "local review of $h7: no findings"; exit 0; }
/usr/bin/grep -q "^## Owned by $owner" "$A" || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
i=0; stop=0
while IFS= read -r line; do
  i=$((i+1))
  case "$line" in
    *"[P0]"*|*"[P1]"*) echo "STOP: local finding $i of $h7 is P0/P1: $line"; stop=1;;
    *) /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
       /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A";;
  esac
done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
[ "$stop" = 0 ] || exit 3
