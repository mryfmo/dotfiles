#!/usr/bin/env bash
# @file local-advisory.sh
# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
# @description
#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
#   other appends the row `local:<sha7>:<n><TAB><class>` under the heading `## Owned by <owner>` of
#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
#   not-applicable:advisory P2 owned by <owner> (…); evidence=shasum -a 256 .orchestration/tasks/<owner>.md
#   (<sha256>)` line, each only when the record lacks it. A review with findings needs the owner task file. The
#   class is `advisory-p2`, unless the finding's `path:line[-line]` token (backticks ignored) matches a finding of
#   the task's earlier local review files whose `local:` row in the record has another class: then the last such
#   row's class, and the line's parenthesis names it as `repeat of local:<sha7>:<n>` (C-50).
# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
# @arg $2 string The reviewed head, 40 hex characters.
# @arg $3 string The task id that owns the advisory findings, in the task id's form.
# @exitcode 0 No P0/P1 finding.
# @exitcode 2 No local review file, a malformed task id, head or owner task id, or (for a review with findings) no
#   owner task file: `write the owner task <owner> first`.
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
# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
O=".orchestration/tasks/$owner.md"
[ -f "$O" ] || {
    echo "write the owner task $owner first"
    exit 2
}
sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
earlier=""
for f in .orchestration/validation/"$task"-local-review-*.md; do
    [[ -f $f && $f != "$LR" ]] || continue
    e=${f%.md} && e=${e##*-local-review-} && k=0
    while IFS= read -r l; do
        k=$((k + 1))
        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
done
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
        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
        class=advisory-p2 repeat=""
        t=$(token "$line") || t=""
        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
        if [[ -n $t && -n $ids ]]; then
            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
        fi
        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
        ;;
    esac
done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
[ "$stop" = 0 ] || exit 3
