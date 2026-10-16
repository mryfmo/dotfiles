#!/usr/bin/env bash
# @file chain-finish.sh
# @brief Finish a PR's integration after the audit's dispositions from the main checkout's scripts, logging every step.
# @description
#   Plan 022 T8 (D7): Orchestrator Playbook step 10 after the audit as one command. After its preconditions (the
#   arguments, the binaries resolved outside shims, the main checkout on main at origin/main with HEAD's scripts,
#   the canonical clean review worktree at the PR's head, that head's audit summary, the record and every gate
#   input) it checks one `audit-finding: <sha7>:<n>` line per audit finding, resolves the threads, re-runs the
#   sweep, writes the record block, runs the gate, merges the audited head with `--match-head-commit`,
#   fast-forwards the main checkout, appends the cost line and prints the AGMSG-ACCEPTANCE line, which it never
#   sends. Each command is appended to T7's `.orchestration/validation/<task>-chain-<sha7>.log` as
#   `<utc> <step> rc=<n>: <command>`, repository paths relative; a refusal before the head is known goes to stderr
#   only. A refusal before the thread step leaves GitHub as it was; a later failure leaves the resolved threads (and,
#   after the merge, the merge) standing. An exit trap removes the comments JSON and both TSVs whatever the exit.
#   The repository scripts run from the main checkout, never the head, and the script never changes directory into
#   the review worktree. Run ff-main.sh and pr-cost.sh by hand after a failure past the merge, once each.
# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
# @arg $2 int PR number.
# @arg $3 path The main checkout.
# @arg $4 path The review worktree, `<main>/.claude/worktrees/orchestrator-review`.
# @arg $5 path The extra dispositions TSV for resolve-threads.sh and fill_sweep.py, in the main checkout (may be empty).
# @exitcode 0 Merged, fast-forwarded and costed; the last line is the AGMSG-ACCEPTANCE line to send.
# @exitcode 1 A step's command failed: `step <name> failed rc=<n>` on stderr and in the log.
# @exitcode 10 A refused precondition (argument, main checkout, review worktree, head, audit summary, gate input).
# @exitcode 11 A thread left open.
# @exitcode 12 An audit finding without its audit-finding line, or an unexpected verdict.
# @exitcode 13 The sweep has gaps after the replies.
# @example
#   scripts/orchestrator/chain-finish.sh dotfiles-T128-x-a01 370 "$PWD" "$PWD/.claude/worktrees/orchestrator-review" "$PWD/.orchestration/x.tsv"
set -euo pipefail
log='' lines=() && export NO_COLOR=1 && unset CLICOLOR_FORCE GH_FORCE_TTY # no ANSI from gh, as pr-feedback.py's gh_env
say() { lines+=("$1") && { [ -z "${log}" ] || printf '%s\n' "$1" >> "${log}"; }; }
refuse() { echo "chain-finish: $2" >&2 && { [ -z "${log}" ] || say "chain-finish: $2"; } && exit "$1"; } # <exit> <message>
# <command…>: a precondition read; sets out, and a failure is exit 1
pre() { out=$("$@") || { echo "step prepare failed rc=$?" >&2 && exit 1; }; }
step() { # <name> <accepted statuses, comma-separated> <command…>: sets out and rc; any other status is exit 1
    local name=$1 ok=",$2," shown
    shift 2
    rc=0
    out=$("$@") || rc=$?
    shown="${1##*/} ${*:2}"
    shown=${shown//"${main}"\//}
    say "$("${date}" -u +%FT%TZ) ${name} rc=${rc}: ${shown//"${main}"/.}"
    echo "${name} rc=${rc}"
    [ -z "${out}" ] || printf '%s\n' "${out}"
    [[ ${ok} == *",${rc},"* ]] || {
        echo "step ${name} failed rc=${rc}" >&2
        say "step ${name} failed rc=${rc}"
        exit 1
    }
}
(($# == 5)) || refuse 10 "invalid argument: chain-finish.sh <task> <pr> <main> <review> <extra tsv>"
task=$1 pr=$2
# The id becomes path segments under .orchestration/ and record content; the leading class excludes . and ..
[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || refuse 10 "invalid argument: ${task}"
[[ ${pr} =~ ^[0-9]+$ ]] || refuse 10 "invalid argument: ${pr}"
main=$(cd -- "$3" 2> /dev/null && pwd -P) || refuse 10 "invalid argument: $3"
cd -- "${main}"
# Resolved before anything else and run by absolute path, as chain-integrate.sh resolves them.
pick() { env -i PATH="${PATH}" HOME="${HOME}" mise which "$1" 2> /dev/null || command -v "$1" || true; }
gh=$(pick gh) git=$(pick git) uv=$(pick uv) date=$(pick date)
for found in "${gh}" "${git}" "${uv}" "${date}"; do
    [[ ${found} == /* && ${found} != */shims/* ]] || refuse 10 "no binary outside a shims directory: ${found:-none}"
done
[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || refuse 10 "main checkout is not on main"
pre "${git}" -C "${main}" fetch -q origin main
pre "${git}" -C "${main}" rev-parse HEAD origin/main
[ "${out%%$'\n'*}" = "${out##*$'\n'}" ] || refuse 10 "main checkout is not origin/main: run scripts/orchestrator/ff-main.sh"
# They run with the orchestrator's credentials, so each must be HEAD's own copy (as chain-integrate.sh, PR #372).
for s in scripts/orchestrator/{resolve-threads.sh,fill_sweep.py,acceptance-front-matter.py,orch-gate.sh,ff-main.sh,pr-cost.sh} scripts/pr-feedback.py; do
    "${git}" -C "${main}" ls-files --error-unmatch -- "${s}" > /dev/null 2>&1 || refuse 10 "${s} is not tracked in the main checkout"
done
"${git}" -C "${main}" diff --quiet HEAD -- scripts || refuse 10 "scripts/ in the main checkout differs from HEAD"
pre "${git}" -C "${main}" rev-parse --show-toplevel
canonical=${out}/.claude/worktrees/orchestrator-review
review=$(cd -- "$4" 2> /dev/null && pwd -P) || review=$4
[ "${review}" = "${canonical}" ] || refuse 10 "review worktree is not the canonical one: ${canonical}"
[ -e "${review}/.git" ] || refuse 10 "review worktree is not a worktree root"
pre "${git}" -C "${review}" status --porcelain
[ -z "${out}" ] || refuse 10 "review worktree is not clean"
# The log names repository paths only, so the extra TSV must be in the main checkout (as chain-integrate.sh).
extra=$(cd -- "$(dirname -- "$5")" 2> /dev/null && pwd -P)/${5##*/}
[[ -f ${extra} && ${extra} == "${main}"/* ]] || refuse 10 "extra dispositions TSV is not a file in the main checkout: $5"
pre "${git}" -C "${review}" rev-parse HEAD
head=${out} sha7=${out:0:7} v=${main}/.orchestration/validation
summary=${v}/${task}-audit-${sha7}.md.last.md
pre "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid
[[ ${out} == "${head}" && -f ${summary} ]] || refuse 10 "head differs from the audit: ${head} (PR ${out}, summary ${summary#"${main}"/})"
record=${main}/.orchestration/acceptance/${task}.md sweep=${v}/${task}-pr-feedback.json
# The gate's own inputs, checked before the thread step writes to GitHub.
for f in "${record}" "${sweep}" "${v}/${task}-audit-${sha7}.md" "${v}/${task}-review-receipt.md" "${v}/${task}-crit.json"; do
    [ -f "${f}" ] || refuse 10 "gate input missing: ${f#"${main}"/}"
done
pre "${uv}" run --no-project python -I -c 'import json, sys; print(json.load(open(sys.argv[1]))["pr"])' "${sweep}"
[ "${out}" = "${pr}" ] || refuse 10 "the sweep JSON is PR ${out}'s, not ${pr}'s"
log=${v}/${task}-chain-${sha7}.log # T7's log, appended; nothing is logged before the head is known
comments=${v}/${task}-pr-comments.json ledger=${v}/${task}-ledger-${sha7}.tsv dispositions=${v}/${task}-audit-dispositions-${sha7}.tsv
cost=${v}/${task}-pr-cost-${sha7}.sh
trap 'rm -f -- "${comments}" "${ledger}" "${dispositions}" "${cost}"' EXIT
# (1) Every finding, under either verdict, needs its line: the gate's ledger check adds audit:<sha7>:<n> for each.
verdict=$(tail -n 1 -- "${summary}")
[[ ${verdict} == "Verdict: correct" || ${verdict} == "Verdict: incorrect" ]] || refuse 12 "unexpected audit verdict: ${verdict}"
findings=$(/usr/bin/grep -c -E '^[[:space:]]*([-*+][[:space:]]+)?\[P[0-3]\]' "${summary}" || true)
: > "${dispositions}"
for ((n = 1; n <= findings; n++)); do
    line=$(/usr/bin/grep -m 1 -E "^audit-finding: ${sha7}:${n} not-applicable:" "${record}" || true)
    [ -n "${line}" ] || refuse 12 "audit finding ${n} of ${sha7} has no audit-finding line"
    body=${line#*not-applicable:}
    printf '%s\t%s\t%s\n' "${n}" "${body%%; evidence=*}" "${body#*; evidence=}" >> "${dispositions}"
done
say "$("${date}" -u +%FT%TZ) verdict rc=0: ${verdict}, ${findings} finding(s), each with its audit-finding line"
# (2) A thread without a disposition stays open, and the gate would refuse it.
step resolve-threads 0,3 "${main}/scripts/orchestrator/resolve-threads.sh" "${pr}" "${extra}" - "${sweep}"
((rc == 0)) || refuse 11 "threads left open"
# (3) The replies are sweep items of their own.
step pr-feedback 0 "${uv}" run --no-project python -I "${main}/scripts/pr-feedback.py" "${pr}" --json "${sweep}"
step fill-sweep 0 "${gh}" api user --jq .login
login=${out}
# One compact object per line, joined into one array, so a second page does not end the JSON after the first.
step fill-sweep 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/comments" --paginate --jq '.[]'
printf '[%s]\n' "${out//$'\n'/,}" > "${comments}"
step fill-sweep 0,1 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/fill_sweep.py" "${sweep}" "${comments}" "${extra}" --orchestrator-login "${login}"
gaps=unknown
[[ ! ${out} =~ gaps\ ([0-9]+) ]] || gaps=${BASH_REMATCH[1]}
((rc == 0)) || refuse 13 "sweep gaps after the replies: ${gaps}"
# (4) The gate's LEDGER_ID: a thread id of ten or more digits or audit:<sha7>:<n>; local: rows stay in the prose.
step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
printf '%s\n' "${out}" > "${ledger}"
# The record script requires the dispositions for an incorrect audit and refuses them for a correct one.
extra_args=()
[[ ${verdict} == "Verdict: correct" ]] || extra_args=(--audit-dispositions "${dispositions}")
step record 0 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/acceptance-front-matter.py" "${task}" "${sweep}" "${review}" --ledger "${ledger}" ${extra_args[@]+"${extra_args[@]}"}
# (5) The gate, (6) the merge bound to the audited head, (7) the fast-forward, (8) the cost line.
step gate 0 "${main}/scripts/orchestrator/orch-gate.sh" "${task}" "${review}" "${pr}"
# The fast-forward puts the merged head's scripts in place, so pr-cost.sh runs from HEAD's copy, taken before the
# merge (PR #378 thread 4300324931); ff-main.sh runs before it moves, and bash keeps reading the file it opened.
pre "${git}" -C "${main}" show HEAD:scripts/orchestrator/pr-cost.sh
printf '%s\n' "${out}" > "${cost}"
step merge 0 "${gh}" pr merge --squash --match-head-commit "${head}" "${pr}"
step merge 0 "${git}" -C "${main}" fetch -q origin main
step merge 0 "${git}" -C "${main}" rev-parse origin/main
merged=${out}
step ff-main 0 "${main}/scripts/orchestrator/ff-main.sh"
step pr-cost 0 "${BASH}" "${cost}" "${pr}"
# (9) Printed for the orchestrator to send (C-53); this script sends nothing.
accept="AGMSG-ACCEPTANCE v1 task_id=${task} status=accepted reason=merged-as-${merged}-pr-${pr}-head-${sha7} next_action=<the orchestrator fills this before sending>"
say "chain-finish: ${task} ${head} merged as ${merged}"
echo "${accept}"
