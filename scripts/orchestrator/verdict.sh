#!/usr/bin/env bash
# @file verdict.sh
# @brief Decide accept, revise or hold for one PR from its nine acceptance conditions and write the verdict JSON.
# @description
#   Plan 024 5.12 (1) (T133). Every condition `{id, ok, evidence}` is ok only on a positive check of a read input:
#   (1) `.orchestration/<task>/precheck.json` at the head hashes to the record's `precheck:` and names the head or an
#   ancestor the head changes only under `.orchestration/<task>/` (a warning while PRECHECK_REQUIRED is unset or 0);
#   (2) gh's checks name the seven required ones SUCCESS; (3) `<task>-audit-<sha7>.json` passes `.schemas/audit.json`,
#   names this task and head, and is correct or leaves only records findings unfixed (blocked holds); (4) every item of
#   a fresh `scripts/pr-feedback.py` sweep has a `fixed:<sha>` or `not-applicable:…; evidence=…` disposition in
#   `<task>-pr-feedback.json`, by url; (5) the merge-base diff stays in the front matter's allowed_files and the Check
#   caps (`at most <n> changed lines outside <paths>`, `<n> under tests/`); (6) `regime-counters.sh <task> --pr <pr>`
#   prints no `S1:` line and revises below 2; (7) no P0/P1 finding is unfixed; (8) a security task's review ends
#   `Verdict: correct`; (9) the record has sha256 lines and each matches its file. accept when all hold; hold when (6)
#   or (7) fails or an input is missing, unreadable or fails its schema; revise otherwise, with the revise line. The
#   verdict JSON (`<task>-verdict-<sha7>.json`) is checked against `.schemas/verdict.json`. --apply (accept only, from a
#   checkout the PR does not control, after four agreeing machine and human rows of verdict-shadow.tsv) sends the
#   ACCEPTANCE line through dispatch.sh and merges with --match-head-commit; --admin or --auto anywhere is refused first.
#   --shadow appends `pr head machine human agree at` and never sends or merges. --loop runs each ready PR in order.
# @arg $1 int PR number (none with --loop).
# @option --task <id> The task, when no record's block names the PR.
# @option --apply With --team, --from, --to and --pane: send the ACCEPTANCE line and merge, on accept only.
# @option --shadow Write the verdict and its machine column only.
# @option --loop Run every ready PR.
# @env PRECHECK_REQUIRED 1 makes condition 1 a failure; unset or 0, a warning.
# @exitcode 0 accept.
# @exitcode 10 revise.
# @exitcode 20 hold.
# @exitcode 2 Usage or internal error (treated as hold).
set -Eeuo pipefail
shopt -s nullglob
for a in "$@"; do
    [[ ${a} != *--admin* && ${a} != *--auto* ]] || {
        echo "verdict: ${a} is refused" >&2
        exit 2
    }
done
usage() {
    echo "usage: verdict.sh <pr> [--task <id>] [--shadow | --apply --team <t> --from <f> --to <to> --pane <p>] | --loop [...]" >&2
    exit 2
}
pr="" task="" team="" from="" to="" pane="" apply=false shadow=false loop=false
while (($#)); do
    case $1 in
    --apply | --shadow | --loop) printf -v "${1#--}" true ;;
    --task | --team | --from | --to | --pane)
        (($# >= 2)) || usage
        printf -v "${1#--}" '%s' "$2"
        shift
        ;;
    *)
        [[ $1 =~ ^[1-9][0-9]*$ && -z ${pr} ]] || usage
        pr=$1
        ;;
    esac
    shift
done
[[ (${loop} == true || -n ${pr}) && ! (${apply} == true && ${shadow} == true) ]] || usage
[[ ${apply} == false || (-n ${team} && -n ${from} && -n ${to} && -n ${pane}) ]] || usage
[[ -z ${task} || ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || usage
trap '((BASH_SUBSHELL)) || echo "verdict: internal error at line ${LINENO}" >&2; exit 2' ERR
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd -- "$(git -C "${here}" rev-parse --show-toplevel)"
v=.orchestration/validation
block() { awk 'NR == 1 { if ($0 != "---") exit; next } $0 == "---" { exit } { print }' "$1"; }
if [[ ${loop} == true ]]; then
    opts=()
    [[ ${apply} == false ]] || opts=(--apply --team "${team}" --from "${from}" --to "${to}" --pane "${pane}")
    [[ ${shadow} == false ]] || opts=(--shadow)
    list="$(gh pr list --base main --state open --limit 200 --json number,headRefOid,isDraft \
        --jq '.[] | select(.isDraft | not) | "\(.number) \(.headRefOid)"' | sort -n)"
    while read -r n h; do
        for f in .orchestration/acceptance/*.md; do
            [[ -n ${n} && "$(block "${f}" | jq -r --argjson p "${n}" 'select(.pr == $p) | .head' 2> /dev/null)" == "${h}" ]] || continue
            "${here}/verdict.sh" "${n}" ${opts[@]+"${opts[@]}"} || true
            git fetch -q origin
            break
        done
    done <<< "${list}"
    exit 0
fi
stop() {
    echo "verdict: $1: hold" >&2
    exit 20
}
view="$(gh pr view "${pr}" --json headRefOid,isDraft,baseRefName,state,number)" || stop "gh pr view ${pr} failed"
head="$(jq -r .headRefOid <<< "${view}")"
[[ ${head} =~ ^[0-9a-f]{40}$ ]] || stop "PR ${pr} has no head"
git cat-file -e "${head}^{commit}" 2> /dev/null || git fetch -q origin "pull/${pr}/head" 2> /dev/null || true
git cat-file -e "${head}^{commit}" 2> /dev/null || stop "the head ${head} is not in this checkout"
if [[ ${apply} == true ]]; then # a merge: only from a checkout the PR does not control, after Q-C's four agreeing rows
    { git diff --quiet origin/main -- scripts .schemas .orchestration/tasks && [[ -z $(git ls-files -o --exclude-standard -- scripts .schemas) ]]; } ||
        stop "--apply runs only from a checkout whose scripts/, .schemas/ and tracked task files equal origin/main"
    [[ "$(tail -n 4 "${v}/verdict-shadow.tsv" 2> /dev/null | awk -F '\t' '$3 == $4 && $4 != "" {print $1}' | sort -u | wc -l)" -eq 4 ]] ||
        stop "--apply waits for four agreeing machine and human rows at the end of ${v}/verdict-shadow.tsv"
fi
for f in .orchestration/acceptance/*.md; do
    [[ -z ${task} ]] || break
    task="$(block "${f}" | jq -r --argjson p "${pr}" 'select(.pr == $p) | .task' 2> /dev/null)" || task=""
done
[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || stop "no acceptance record names PR ${pr}"
rec=.orchestration/acceptance/${task}.md tf=.orchestration/tasks/${task}.md audit=${v}/${task}-audit-${head:0:7}.json
fb=${v}/${task}-pr-feedback.json sec=${v}/${task}-security-${head:0:7}.md.last.md out=${v}/${task}-verdict-${head:0:7}.json
conds=() hold=""
cond() { conds+=("$(jq -cn --argjson id "$1" --argjson ok "$2" --arg e "$3" '{id: $id, ok: $ok, evidence: $e}')"); }
lack() { hold+="${hold:+; }$1"; }
fresh="$(mktemp "${TMPDIR:-/tmp}/verdict-sweep.XXXXXX")" line_file=""
trap 'rm -f -- "${fresh}" "${line_file}"' EXIT
[[ "$(block "${rec}" 2> /dev/null | jq -r '"\(.task) \(.pr) \(.head) \(.ledger | type)"' 2> /dev/null)" == "${task} ${pr} ${head} array" ]] ||
    lack "the record ${rec} is not this task's at the head"
[[ "$(jq -r '"\(.state) \(.baseRefName) \(.isDraft)"' <<< "${view}")" == "OPEN main false" ]] || lack "PR ${pr} is not open, non-draft, on main"

want="$(sed -n 's/^precheck: \([0-9a-f]\{64\}\)$/\1/p' "${rec}" 2> /dev/null | tail -n 1 || true)" got="" ph=""
if git cat-file -e "${head}:.orchestration/${task}/precheck.json" 2> /dev/null; then
    got="$(git show "${head}:.orchestration/${task}/precheck.json" | shasum -a 256)" got=${got%% *}
    ph="$(git show "${head}:.orchestration/${task}/precheck.json" | jq -r '.head // empty' 2> /dev/null)" || ph=""
fi
if [[ -n ${want} && ${got} == "${want}" && ${ph} =~ ^[0-9a-f]{40}$ ]] && { [[ ${ph} == "${head}" ]] ||
    { git merge-base --is-ancestor "${ph}" "${head}" && [[ -z $(git diff --name-only "${ph}" "${head}" -- . ":!.orchestration/${task}") ]]; }; }; then
    cond 1 true "precheck.json hashes to the record's precheck and names ${ph:0:7}"
elif [[ ${PRECHECK_REQUIRED:-0} == 0 ]]; then
    cond 1 true "warning: precheck.json is not bound to the record and the head (PRECHECK_REQUIRED=0)"
else
    cond 1 false "precheck.json does not hash to the record's precheck: or names neither the head nor an evidence-only ancestor"
fi

required='["validate", "test (ubuntu-24.04, server)", "test (ubuntu-24.04, client)", "test (macos-14, client)",
  "public-bootstrap (ubuntu-24.04, server)", "public-bootstrap (ubuntu-24.04, client)", "public-bootstrap (macos-14, client)"]'
checks="$(gh pr checks "${pr}" --json name,state 2> /dev/null)" || true
if miss="$(jq -er --argjson req "${required}" 'if type != "array" or length == 0 then error("no checks") else . as $c
    | [$req[] | select(. as $n | [$c[] | select(.name == $n) | .state] | length > 0 and all(. == "SUCCESS") | not)] | join(", ") end' <<< "${checks}" 2> /dev/null)"; then
    cond 2 "$([[ -z ${miss} ]] && echo true || echo false)" "required checks not SUCCESS: ${miss:-none}"
else
    lack "gh pr checks ${pr}" && cond 2 false "gh pr checks is unreadable"
fi

if [[ -f ${audit} ]] && "${here}/orch-audit.sh" --validate .schemas/audit.json "${audit}" > /dev/null 2>&1; then
    a3="$(jq -r --arg h "${head}" --arg t "${task}" '[.findings[] | select((.status // "new") != "fixed")] as $open
        | if [.head, .task_id] != [$h, $t] then "the audit is of \(.task_id) at \(.head[0:7])" elif .verdict == "blocked" then "blocked: not assessed"
        elif .verdict == "correct" or ($open | length > 0 and all(.[]; .scope == "records")) then "" else "verdict \(.verdict), unfixed \($open | map(.scope))" end' "${audit}")"
    [[ ${a3} != blocked:* ]] || lack "the audit ${audit} is blocked"
    a7="$(jq -r '[.findings[] | select(.priority == "P0" or .priority == "P1") | select((.status // "new") != "fixed") | .id] | join(",")' "${audit}")"
    cond 3 "$([[ -z ${a3} ]] && echo true || echo false)" "${a3:-the audit of the head is correct or leaves only records findings}"
    cond 7 "$([[ -z ${a7} ]] && echo true || echo false)" "unfixed P0/P1 findings: ${a7:-none}"
else
    lack "${audit} is missing or fails .schemas/audit.json" && cond 3 false "no valid audit ${audit}" && cond 7 false "no valid audit"
fi

if uv run --offline --no-project python -I scripts/pr-feedback.py "${pr}" --json "${fresh}" > /dev/null 2>&1 && [[ -f ${fb} ]] &&
    a4="$(jq -rn --slurpfile f "${fresh}" --slurpfile d "${fb}" '([$d[0].items[] | {key: (.url // ""), value: (.disposition // "")}] | from_entries)
      as $m | [$f[0].items[] | (.url // "") as $u | select(($m[$u] // "") | test("^fixed:[0-9a-f]{7,40}$") or (startswith("not-applicable:")
      and contains("; evidence=")) | not) | $u] | join(" ")' 2> /dev/null)"; then
    cond 4 "$([[ -z ${a4} ]] && echo true || echo false)" "items without a disposition or evidence: ${a4:-none}"
else
    lack "the fresh sweep or ${fb}" && cond 4 false "no fresh sweep or no ${fb}"
fi

read_front='import json, sys, yaml; t = open(sys.argv[1]).read(); f = yaml.safe_load(t.split("\n---\n", 1)[0][4:]) if t.startswith("---\n") else 0
print(json.dumps(f if isinstance(f, dict) else {}))'
# Offline only: a cold cache leaves front empty, which holds (conditions 5 and 8); never an online resolution.
front="$(uv run --offline --no-project --with pyyaml python -I -c "${read_front}" "${tf}" 2> /dev/null)" || front=""
if [[ -n ${front} && "$(jq -r '.allowed_files | type' <<< "${front}")" == array ]] &&
    base="$(git merge-base origin/main "${head}")" && numstat="$(git diff --numstat --no-renames "${base}" "${head}")"; then
    allowed=() stray="" outside=0 under=0 excluded=()
    cap_out="$(sed -n 's/.*at most \([0-9][0-9]*\) changed lines outside.*/\1/p' "${tf}" | head -n 1)"
    cap_tests="$(sed -n 's/.* \([0-9][0-9]*\) under .\{0,1\}tests\/.*/\1/p' "${tf}" | head -n 1)"
    # The paths the Check sentence lists after "outside", up to "(" or ", <n> under", leave the outside count.
    listed="$(sed -n 's/.*at most [0-9][0-9]* changed lines outside \([^(]*\).*/\1/p' "${tf}" | head -n 1)"
    # shellcheck disable=SC2016 # the backticks are literal: the sentence quotes each path in them
    while IFS= read -r x; do [[ -z ${x} ]] || excluded+=("${x}"); done <<< "$(grep -o '`[^`]*`' <<< "${listed%%, [0-9]*}" | tr -d '`' || true)"
    ((${#excluded[@]})) || excluded=(tests/ .orchestration/)
    while IFS= read -r a; do allowed+=("${a}"); done <<< "$(jq -r '.allowed_files[] | strings' <<< "${front}")"
    while IFS=$'\t' read -r add del path; do
        [[ -n ${path} ]] || continue
        in=no
        for a in "${allowed[@]}"; do
            # shellcheck disable=SC2053 # an allowed_files entry is a glob
            [[ ${path} != ${a} ]] || in=yes
        done
        [[ ${in} == yes ]] || stray+=" ${path}"
        [[ ${add} != - ]] || add=0 del=0
        counted=yes
        for x in "${excluded[@]}"; do
            [[ ${path} != "${x}" && (${x} != */ || ${path} != "${x}"*) ]] || counted=no
        done
        [[ ${path} != tests/* ]] || under=$((under + add + del))
        [[ ${counted} == no ]] || outside=$((outside + add + del))
    done <<< "${numstat}"
    over=""
    [[ -z ${cap_out} ]] || ((outside <= cap_out)) || over+=" ${outside}>${cap_out} outside tests/"
    [[ -z ${cap_tests} ]] || ((under <= cap_tests)) || over+=" ${under}>${cap_tests} under tests/"
    cond 5 "$([[ -z ${stray}${over} ]] && echo true || echo false)" "outside allowed_files:${stray:- none}; over the caps:${over:- none}"
else
    lack "the task file ${tf} or the merge-base diff" && cond 5 false "no readable front matter in ${tf} or no merge-base diff"
fi

if counters="$(scripts/regime-counters.sh "${task}" --pr "${pr}" 2> /dev/null)" &&
    revises="$(sed -n '1s/.* revises=\([0-9][0-9]*\) .*/\1/p' <<< "${counters}")" && [[ -n ${revises} ]]; then
    s1="$(grep '^S1:' <<< "${counters}" | tr '\n' ' ' || true)"
    cond 6 "$([[ -z ${s1} && ${revises} -lt 2 ]] && echo true || echo false)" "revises=${revises}; ${s1:-no S1 line}"
else
    lack "regime-counters.sh ${task}" && cond 6 false "the counters are unreadable"
fi

if [[ -z ${front} ]]; then
    cond 8 false "no front matter, so no security reading"
elif [[ "$(jq -r '.security' <<< "${front}")" != true ]]; then
    cond 8 true "not a security task"
elif [[ -f ${sec} ]]; then
    last="$(grep -v '^[[:space:]]*$' "${sec}" | tail -n 1)"
    cond 8 "$([[ ${last} == "Verdict: correct" ]] && echo true || echo false)" "the security review: ${last}"
else
    lack "${sec}" && cond 8 false "no security review ${sec}"
fi

bad="" n=0
while read -r want_sum path; do
    [[ -n ${path} ]] && n=$((n + 1))
    [[ -z ${path} || "$(shasum -a 256 -- "${path}" 2> /dev/null)" == "${want_sum}  ${path}" ]] || bad+=" ${path}"
done <<< "$(sed -n 's/^sha256:\([0-9a-f]\{64\}\) \(.*\)$/\1 \2/p' "${rec}" 2> /dev/null || true)"
cond 9 "$([[ -z ${bad} && ${n} -gt 0 ]] && echo true || echo false)" "${n} sha256 lines; mismatches:${bad:- none}"

inputs='{}'
for f in "${rec}" "${tf}" "${audit}" "${fb}" "${sec}" "${fresh}"; do
    [[ -s ${f} ]] || continue
    sum="$(shasum -a 256 -- "${f}")"
    inputs="$(jq -c --arg k "$([[ ${f} == "${fresh}" ]] && echo fresh-sweep || echo "${f}")" --arg s "${sum%% *}" '. + {($k): $s}' <<< "${inputs}")"
done
all="$(printf '%s\n' "${conds[@]}" | jq -cs 'sort_by(.id)')"
failed="$(jq -r '[.[] | select(.ok | not) | .id] | join(",")' <<< "${all}")"
line=""
if [[ -n ${hold} ]] || jq -e 'any(.[]; (.id == 6 or .id == 7) and (.ok | not))' <<< "${all}" > /dev/null; then
    verdict=hold code=20
elif [[ -z ${failed} ]]; then
    verdict=accept code=0
else
    verdict=revise code=10
    next="$(jq -r 'first(.[] | select(.ok | not) | .evidence)' <<< "${all}" | tr -c 'A-Za-z0-9._:/,=+-' '-' | cut -c 1-160)"
    line="AGMSG-ACCEPTANCE v1 task_id=${task} status=revise previous_head=${head} reason=conditions-${failed} next_action=${next%-}"
fi
[[ -z ${hold} ]] || echo "verdict: hold: ${hold}" >&2
now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
jq -n --arg verdict "${verdict}" --argjson pr "${pr}" --arg head "${head}" --arg task "${task}" --argjson c "${all}" \
    --argjson i "${inputs}" --arg at "${now}" --arg line "${line}" '{verdict: $verdict, pr: $pr, head: $head, task_id: $task,
    conditions: $c, inputs_sha256: $i, generated_at: $at} + (if $line == "" then {} else {revise_line: $line} end)' > "${out}"
"${here}/orch-audit.sh" --validate .schemas/verdict.json "${out}" > /dev/null
echo "verdict: ${verdict} ${out}"
[[ ${shadow} == false ]] || printf '%s\t%s\t%s\t\t\t%s\n' "${pr}" "${head}" "${verdict}" "${now}" >> "${v}/verdict-shadow.tsv"
if [[ ${apply} == true && ${verdict} == accept ]]; then
    line_file="$(mktemp "${TMPDIR:-/tmp}/verdict-line.XXXXXX")"
    echo "AGMSG-ACCEPTANCE v1 task_id=${task} status=accepted reason=verdict-${head:0:7} next_action=merge" > "${line_file}"
    "${here}/dispatch.sh" "${team}" "${from}" "${to}" "${pane}" "${line_file}" "${rec}"
    gh pr merge "${pr}" --squash --match-head-commit "${head}"
fi
exit "${code}"
