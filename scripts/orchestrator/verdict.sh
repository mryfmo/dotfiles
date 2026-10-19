#!/usr/bin/env bash
# @file verdict.sh
# @brief Decide accept, revise or hold for one PR from its nine acceptance conditions and write the verdict JSON.
# @description
#   Plan 024 5.12 (1) (T133). Each condition `{id, ok, evidence}` is ok only on a positive check of a read input: (1)
#   the head's `.orchestration/<task>/precheck.json` hashes to the record's `precheck:` and names the head or an
#   evidence-only ancestor; (2) the seven required checks succeed; (3) `<task>-audit-<sha7>.json` passes
#   `.schemas/audit.json`, names this task and head, has no open P0/P1, and is correct or leaves only records findings
#   open; (4) the fresh sweep and `<task>-pr-feedback.json` name the head, and require-crit-review.py's helpers give
#   each fresh item its own validly dispositioned saved item; (5) the merge-base diff keeps to allowed_files and the
#   Check caps as last declared (an amendment follows the Check); (6) regime-counters.sh prints no `S1:` and revises
#   below 2; (7) no P0/P1 finding is new, still-open or status-less, whatever its id or scope; (8) a security task's
#   review ends `Verdict: correct`; (9) the record's sha256 lines exist and match. accept when all hold; hold when (6)
#   or (7) fails or an input is missing or invalid; revise otherwise. It first re-runs itself under `env -i`, PATH =
#   links to bash, uv, python3, gh, git and jq resolved from / then /usr/bin:/bin, Python (the schema checker too)
#   = that python3 -I, uv offline with --no-config and --python: no checkout file and no inherited UV_PYTHON or
#   VIRTUAL_ENV picks a tool. --apply (accept only; scripts/, .schemas/ and task files equal origin/main; four distinct
#   agreeing shadow PRs) holds unless orch-gate.sh <task> <head> <pr> exits 0, then dispatches and merges.
# @arg $1 int PR number (none with --loop).
# @option --task <id> The task, when no record's block names the PR.
# @option --apply With --team, --from, --to and --pane: send the ACCEPTANCE line and merge, on accept only.
# @option --shadow Write the verdict and its machine column only.
# @option --loop Run every ready PR; with --apply, fast-forward this checkout to origin/main after each, or hold.
# @option --validate <schema> <json> Check one JSON file against a `.schemas/` schema, then exit.
# @env PRECHECK_REQUIRED 1 makes condition 1 a failure; unset or 0, a warning.
# @exitcode 0 accept.
# @exitcode 10 revise.
# @exitcode 20 hold.
# @exitcode 2 Usage or internal error (treated as hold).
set -Eeuo pipefail
shopt -s nullglob
for a in "$@"; do [[ ${a} != *--admin* && ${a} != *--auto* ]] || { echo "verdict: ${a} is refused" >&2 && exit 2; }; done
trap '((BASH_SUBSHELL)) || echo "verdict: internal error at line ${LINENO}" >&2; exit 2' ERR
usage() { echo "usage: verdict.sh <pr> [--task <id>] [--shadow | --apply --team <t> --from <f> --to <to> --pane <p>] | --loop [...] | --validate <schema> <json>" >&2 && exit 2; }
stop() { echo "verdict: $1: hold" >&2 && exit 20; }
if [[ -z ${VERDICT_BIN:-} || ${PATH} != "${VERDICT_BIN}:/usr/bin:/bin" ]]; then # pin, re-run, then read checkouts
    bin="$(mktemp -d "${TMPDIR:-/tmp}/verdict-bin.XXXXXX")" rc=0
    for t in bash uv python3 gh git jq agmsg-dispatch herdr; do
        p="$(cd / && env -i PATH="${PATH}" HOME="${HOME}" mise which "${t}" 2> /dev/null || command -v "${t}")" || p=""
        [[ ${p} == /* && ${p} != */shims/* ]] && ln -s -- "${p}" "${bin}/${t}" && continue
        [[ ${t} == agmsg-dispatch || ${t} == herdr ]] || { rm -rf -- "${bin}" && stop "no ${t} outside a shims directory ('${p}')"; }
    done
    env -i HOME="${HOME}" TMPDIR="${TMPDIR:-/tmp}" PATH="${bin}:/usr/bin:/bin" VERDICT_BIN="${bin}" \
        PRECHECK_REQUIRED="${PRECHECK_REQUIRED:-0}" "${bin}/bash" "${BASH_SOURCE[0]}" "$@" || rc=$?
    rm -rf -- "${bin}"
    exit "${rc}"
fi
read -r -d '' checker << 'PY' || true # <schema> <json>: the stdlib subset of JSON Schema 2020-12 .schemas/ uses
import json, re, sys
from datetime import datetime
T = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool}
def check(s, v, at="$"):
    t, p = s.get("type"), s.get("pattern")
    if t and (not isinstance(v, T[t]) or isinstance(v, bool) and t == "integer"): return f"{at} is not {t}"
    if "enum" in s and v not in s["enum"]: return f"{at} {v!r} is not in the enum"
    if isinstance(v, str) and p and not re.search(p[:-1] + r"\Z" if p.endswith("$") else p, v): return f"{at} does not match {p}"
    if isinstance(v, str) and len(v) > s.get("maxLength", len(v)): return f"{at} is longer than {s['maxLength']}"
    try:  # RFC 3339 with an offset (a non-match raises TypeError at [0]); fromisoformat then checks the ranges
        s.get("format") != "date-time" or not isinstance(v, str) or datetime.fromisoformat(re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(Z|[+-]\d\d:\d\d)", v)[0].replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return f"{at} is not an RFC 3339 date-time with an offset"
    if type(v) is int and not s.get("minimum", v) <= v <= s.get("maximum", v): return f"{at} is out of range"
    for k in [k for k in s.get("required", []) if k not in v][:1] if isinstance(v, dict) else []: return f"{at} lacks {k}"
    for k, x in v.items() if isinstance(v, dict) else []:
        sub = s.get("properties", {}).get(k, s.get("additionalProperties", True))
        if sub is False or isinstance(sub, dict) and (e := check(sub, x, f"{at}.{k}")):
            return e if sub is not False else f"{at} has the unknown key {k}"
    for i, x in enumerate(v if isinstance(v, list) and "items" in s else []):
        if e := check(s["items"], x, f"{at}[{i}]"): return e
try:
    sys.exit((err := check(*(json.load(open(f)) for f in sys.argv[1:3]))) and f"schema: {err}")
except (OSError, ValueError) as e:
    sys.exit(f"unreadable: {e}")
PY
if [[ ${1:-} == --validate ]]; then (($# == 3)) || usage && exec "${VERDICT_BIN}/python3" -I -c "${checker}" "$2" "$3"; fi
pr="" task="" team="" from="" to="" pane="" apply=false shadow=false loop=false
while (($#)); do
    case $1 in
    --apply | --shadow | --loop) printf -v "${1#--}" true ;;
    --task | --team | --from | --to | --pane) { (($# >= 2)) || usage; } && printf -v "${1#--}" '%s' "$2" && shift ;;
    *) { [[ $1 =~ ^[1-9][0-9]*$ && -z ${pr} ]] || usage; } && pr=$1 ;;
    esac
    shift
done
[[ (${loop} == true || -n ${pr}) && ! (${apply} == true && ${shadow} == true) && ${task} =~ ^([A-Za-z0-9][A-Za-z0-9._-]*)?$ ]] || usage
[[ ${apply} == false || (-n ${team} && -n ${from} && -n ${to} && -n ${pane}) ]] || usage
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd -- "$(git -C "${here}" rev-parse --show-toplevel)"
v=.orchestration/validation uvy=(uv run --no-config --no-project --offline --python "${VERDICT_BIN}/python3" --with pyyaml)
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
            git fetch -q origin # a merge moved origin/main: the trusted checkout follows it, or the loop holds
            [[ ${apply} == false ]] || git merge -q --ff-only origin/main || stop "this checkout cannot fast-forward to origin/main"
            break
        done
    done <<< "${list}"
    exit 0
fi
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
for f in .orchestration/acceptance/*.md; do [[ -n ${task} ]] || task="$(block "${f}" | jq -r --argjson p "${pr}" 'select(.pr == $p) | .task' 2> /dev/null)" || task=""; done
[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || stop "no acceptance record names PR ${pr}"
rec=.orchestration/acceptance/${task}.md tf=.orchestration/tasks/${task}.md audit=${v}/${task}-audit-${head:0:7}.json
fb=${v}/${task}-pr-feedback.json sec=${v}/${task}-security-${head:0:7}.md.last.md out=${v}/${task}-verdict-${head:0:7}.json
cond() { conds+=("$(jq -cn --argjson id "$1" --argjson ok "$2" --arg e "$3" '{id: $id, ok: $ok, evidence: $e}')"); }
lack() { hold+="${hold:+; }$1"; }
fresh="$(mktemp "${TMPDIR:-/tmp}/verdict-sweep.XXXXXX")" line_file="" conds=() hold=""
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
if [[ -f ${audit} ]] && "${VERDICT_BIN}/python3" -I -c "${checker}" .schemas/audit.json "${audit}" > /dev/null 2>&1; then
    a7="$(jq '[.findings[] | select(.priority == "P0" or .priority == "P1") | select(.status // "new" | . == "new" or . == "still-open")] | length' "${audit}")" # counted, never named: no empty id hides one
    a3="$(jq -r --arg h "${head}" --arg t "${task}" --argjson n "${a7}" '[.findings[] | select((.status // "new") != "fixed")] as $open
        | if [.head, .task_id] != [$h, $t] then "the audit is of \(.task_id) at \(.head[0:7])" elif .verdict == "blocked" then "blocked: not assessed"
        elif $n > 0 then "\($n) open P0/P1 findings" elif .verdict == "correct" or ($open | length > 0 and all(.[]; .scope == "records")) then ""
        else "verdict \(.verdict), unfixed \($open | map(.scope))" end' "${audit}")"
    [[ ${a3} != blocked:* ]] || lack "the audit ${audit} is blocked"
    cond 3 "$([[ -z ${a3} ]] && echo true || echo false)" "${a3:-the audit of the head is correct or leaves only records findings}"
    cond 7 "$([[ ${a7} == 0 ]] && echo true || echo false)" "open P0/P1 findings: ${a7}"
else
    lack "${audit} is missing or fails .schemas/audit.json" && cond 3 false "no valid audit ${audit}" && cond 7 false "no valid audit"
fi
base="$(git merge-base origin/main "${head}" 2> /dev/null)" || base=""
read -r -d '' gaps << 'PY' || true # condition 4 by the gate's helpers: a gap per line; a url only labels it
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("gate", "scripts/require-crit-review.py")
spec.loader.exec_module(gate := importlib.util.module_from_spec(spec))
(fresh, saved), head, base = (json.load(open(p)) for p in sys.argv[1:3]), sys.argv[3], sys.argv[4]
for name, doc in (("fresh sweep", fresh), ("saved document", saved)):
    doc.get("head_sha") == head or print(f"the {name} names head {doc.get('head_sha')}, not {head[:7]}")
for key, n in gate.missing_feedback(fresh["items"], saved["items"]).items(): print(f"{n} fresh item(s) without a saved one: {key[0]} {key[1] or ''}")
for item in saved["items"]:
    commit, reason = gate.parse_disposition(item.get("disposition")) or (None, None)
    short = not commit and item.get("level") in gate.STRICT_REASON_LEVELS and len(reason or "") < gate.FAILURE_REASON_MIN_CHARS
    if reason is None and not commit or short or commit and not gate.commit_in_range(gate.Path("."), commit, base, head):
        print(f"no valid disposition: {item.get('source')} {item.get('url') or ''}")
PY
if [[ -n ${base} && -f ${fb} ]] && "${VERDICT_BIN}/python3" -I scripts/pr-feedback.py "${pr}" --json "${fresh}" > /dev/null 2>&1 &&
    a4="$("${VERDICT_BIN}/python3" -I -B -c "${gaps}" "${fresh}" "${fb}" "${head}" "${base}" 2> /dev/null)"; then
    cond 4 "$([[ -z ${a4} ]] && echo true || echo false)" "feedback gaps: ${a4:-none}"
else
    lack "the fresh sweep, ${fb} or the merge base" && cond 4 false "no fresh sweep, no ${fb} or no merge base"
fi
read_front='import json, sys, yaml; t = open(sys.argv[1]).read(); f = yaml.safe_load(t.split("\n---\n", 1)[0][4:]) if t.startswith("---\n") else 0
print(json.dumps(f if isinstance(f, dict) else {}))'
front="$("${uvy[@]}" python -I -c "${read_front}" "${tf}" 2> /dev/null)" || front="" # offline: a cold cache holds
if [[ -n ${front} && "$(jq -r '.allowed_files | type' <<< "${front}")" == array && -n ${base} ]] &&
    numstat="$(git diff --numstat --no-renames "${base}" "${head}")"; then
    allowed=() stray="" outside=0 under=0 excluded=() over=""
    cap_out="$(sed -n 's/.*at most \([0-9][0-9]*\) changed lines outside.*/\1/p' "${tf}" | tail -n 1)"
    cap_tests="$(sed -n 's/.* \([0-9][0-9]*\) under .\{0,1\}tests\/.*/\1/p' "${tf}" | tail -n 1)"
    # Each limit is its last declaration in the task text (an amendment follows the Check); the paths the last
    # "at most" sentence lists after "outside", up to "(" or ", <n> under", leave the outside count.
    listed="$(sed -n 's/.*at most [0-9][0-9]* changed lines outside \([^(]*\).*/\1/p' "${tf}" | tail -n 1)"
    # shellcheck disable=SC2016 # the backticks are literal: the sentence quotes each path in them
    while IFS= read -r x; do [[ -z ${x} ]] || excluded+=("${x}"); done <<< "$(grep -o '`[^`]*`' <<< "${listed%%, [0-9]*}" | tr -d '`' || true)"
    ((${#excluded[@]})) || excluded=(tests/ .orchestration/)
    while IFS= read -r a; do allowed+=("${a}"); done <<< "$(jq -r '.allowed_files[] | strings' <<< "${front}")"
    while IFS=$'\t' read -r add del path; do
        [[ -n ${path} ]] || continue
        in=no counted=yes
        # shellcheck disable=SC2053 # an allowed_files entry is a glob
        for a in "${allowed[@]}"; do [[ ${path} != ${a} ]] || in=yes; done
        [[ ${in} == yes ]] || stray+=" ${path}"
        [[ ${add} != - ]] || add=0 del=0
        for x in "${excluded[@]}"; do [[ ${path} != "${x}" && (${x} != */ || ${path} != "${x}"*) ]] || counted=no; done
        [[ ${path} != tests/* ]] || under=$((under + add + del))
        [[ ${counted} == no ]] || outside=$((outside + add + del))
    done <<< "${numstat}"
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
bad="" n=0 inputs='{}'
while read -r want_sum path; do
    [[ -n ${path} ]] && n=$((n + 1))
    [[ -z ${path} || "$(shasum -a 256 -- "${path}" 2> /dev/null)" == "${want_sum}  ${path}" ]] || bad+=" ${path}"
done <<< "$(sed -n 's/^sha256:\([0-9a-f]\{64\}\) \(.*\)$/\1 \2/p' "${rec}" 2> /dev/null || true)"
cond 9 "$([[ -z ${bad} && ${n} -gt 0 ]] && echo true || echo false)" "${n} sha256 lines; mismatches:${bad:- none}"
for f in "${rec}" "${tf}" "${audit}" "${fb}" "${sec}" "${fresh}"; do
    [[ -s ${f} ]] || continue
    sum="$(shasum -a 256 -- "${f}")"
    inputs="$(jq -c --arg k "$([[ ${f} == "${fresh}" ]] && echo fresh-sweep || echo "${f}")" --arg s "${sum%% *}" '. + {($k): $s}' <<< "${inputs}")"
done
all="$(printf '%s\n' "${conds[@]}" | jq -cs 'sort_by(.id)')"
failed="$(jq -r '[.[] | select(.ok | not) | .id] | join(",")' <<< "${all}")" line=""
if [[ -n ${hold} ]] || jq -e 'any(.[]; (.id == 6 or .id == 7) and (.ok | not))' <<< "${all}" > /dev/null; then
    verdict=hold code=20
elif [[ -z ${failed} ]]; then
    verdict=accept code=0
else
    verdict=revise code=10
    next="$(jq -r 'first(.[] | select(.ok | not) | .evidence)' <<< "${all}" | tr -c 'A-Za-z0-9._:/,=+-' '-' | cut -c 1-160)"
    line="AGMSG-ACCEPTANCE v1 task_id=${task} status=revise previous_head=${head} reason=conditions-${failed} next_action=${next%-}"
fi
if [[ ${apply} == true && ${verdict} == accept ]] && ! "${here}/orch-gate.sh" "${task}" "${head}" "${pr}"; then
    verdict=hold code=20 hold="the integration gate refused ${task} at ${head:0:7} for PR ${pr}" # no receipt, no application
fi
[[ -z ${hold} ]] || echo "verdict: hold: ${hold}" >&2
now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
jq -n --arg verdict "${verdict}" --argjson pr "${pr}" --arg head "${head}" --arg task "${task}" --argjson c "${all}" \
    --argjson i "${inputs}" --arg at "${now}" --arg line "${line}" '{verdict: $verdict, pr: $pr, head: $head, task_id: $task,
    conditions: $c, inputs_sha256: $i, generated_at: $at} + (if $line == "" then {} else {revise_line: $line} end)' > "${out}"
"${VERDICT_BIN}/python3" -I -c "${checker}" .schemas/verdict.json "${out}" > /dev/null
echo "verdict: ${verdict} ${out}"
[[ ${shadow} == false ]] || printf '%s\t%s\t%s\t\t\t%s\n' "${pr}" "${head}" "${verdict}" "${now}" >> "${v}/verdict-shadow.tsv"
if [[ ${apply} == true && ${verdict} == accept ]]; then
    line_file="$(mktemp "${TMPDIR:-/tmp}/verdict-line.XXXXXX")"
    echo "AGMSG-ACCEPTANCE v1 task_id=${task} status=accepted reason=verdict-${head:0:7} next_action=merge" > "${line_file}"
    "${here}/dispatch.sh" "${team}" "${from}" "${to}" "${pane}" "${line_file}" "${rec}"
    gh pr merge "${pr}" --squash --match-head-commit "${head}"
fi
exit "${code}"
