#!/usr/bin/env bash
# @file chain-integrate.sh
# @brief Run a PR head's integration chain up to the audit from the main checkout's scripts, logging every step.
# @description
#   Plan 022 T7 (D7): Orchestrator Playbook step 10 up to the audit as one command. After its preconditions (the
#   arguments, the binaries resolved outside shims, the main checkout on main at origin/main, the canonical clean
#   review worktree, the record, a ready PR) it fetches the head into both checkouts, update-branches when the base
#   moved (restarting at the fetch), waits for the required checks and the Bot (never gated), then runs the sandbox
#   scan, the local review, the advisory rows, the sweep, the receipt, the record block and the audit, which an
#   update-branch-only head inherits from the head it merged main into when the PR's patch-id is unchanged. Each command
#   goes to `.orchestration/validation/<task>-chain-<sha7>.log` as `<utc> <step> rc=<n>: <command>`, repository
#   paths relative; a refusal before the head is known goes to stderr only. The repository scripts run from the main
#   checkout, never the head, and the script never changes directory into the review worktree.
# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
# @arg $2 int PR number.
# @arg $3 path The main checkout.
# @arg $4 path The review worktree, `<main>/.claude/worktrees/orchestrator-review`.
# @arg $5 string The task id that owns the advisory findings, in the task id's form.
# @arg $6 path Optional extra dispositions TSV for fill_sweep.py.
# @exitcode 0 The audit is written; the last line is `chain-integrate: <task> <head> <verdict line>`.
# @exitcode 1 A step's command failed: `step <name> failed rc=<n>` on stderr and in the log.
# @exitcode 10 A refused precondition (argument, main checkout, review worktree, record, draft, head mismatch, head
#   already audited, update-branch head not visible).
# @exitcode 11 A P0/P1 local finding.
# @exitcode 12 The required checks failed.
# @exitcode 13 The base moved three times.
# @exitcode 14 The sweep has gaps.
# @exitcode 15 The owner task file is absent.
# @exitcode 16 A sandbox-scan hit not yet judged (`CHAIN_SCAN_JUDGED=<sha7>` after the judgement).
# @example
#   scripts/orchestrator/chain-integrate.sh dotfiles-T128-x-a01 370 "$PWD" "$PWD/.claude/worktrees/orchestrator-review" dotfiles-T128-x-followup-a01
set -euo pipefail
log='' lines=() && export NO_COLOR=1 && unset CLICOLOR_FORCE GH_FORCE_TTY # no ANSI from gh, as pr-feedback.py's gh_env
say() { lines+=("$1") && { [ -z "${log}" ] || printf '%s\n' "$1" >> "${log}"; }; }
refuse() { echo "chain-integrate: $2" >&2 && { [ -z "${log}" ] || say "chain-integrate: $2"; } && exit "$1"; } # <exit> <message>
# <command…>: a precondition read; sets out, and a failure is exit 1
pre() { out=$("$@") || { echo "step prepare failed rc=$?" >&2 && exit 1; }; }
step() { # <name> <accepted statuses, comma-separated, or any> <command…>: sets out and rc; any other status is exit 1
    local name=$1 ok=",$2," shown
    shift 2
    rc=0
    out=$("$@") || rc=$?
    shown="${1##*/} ${*:2}"
    shown=${shown//"${main}"\//}
    say "$("${date}" -u +%FT%TZ) ${name} rc=${rc}: ${shown//"${main}"/.}"
    echo "${name} rc=${rc}"
    [ -z "${out}" ] || printf '%s\n' "${out}"
    [[ ${ok} == ,any, || ${ok} == *",${rc},"* ]] || {
        echo "step ${name} failed rc=${rc}" >&2
        say "step ${name} failed rc=${rc}"
        exit 1
    }
}
(($# == 5 || $# == 6)) || refuse 10 "invalid argument: chain-integrate.sh <task> <pr> <main> <review> <owner> [<extra tsv>]"
task=$1 pr=$2 owner=$5 extra=${6:-}
# Both ids become path segments under .orchestration/ and record content; the leading class excludes . and ..
for v in "${task}" "${owner}"; do
    [[ ${v} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || refuse 10 "invalid argument: ${v}"
done
[[ ${pr} =~ ^[0-9]+$ ]] || refuse 10 "invalid argument: ${pr}"
main=$(cd -- "$3" 2> /dev/null && pwd -P) || refuse 10 "invalid argument: $3"
cd -- "${main}"
# Resolved before any fetch or checkout and run by absolute path, as local-review.sh resolves codex: a mise shim
# would pick its binary by the directory it runs in.
pick() { env -i PATH="${PATH}" HOME="${HOME}" mise which "$1" 2> /dev/null || command -v "$1" || true; }
gh=$(pick gh) git=$(pick git) uv=$(pick uv) shasum=$(pick shasum) date=$(pick date)
for found in "${gh}" "${git}" "${uv}" "${shasum}" "${date}"; do
    [[ ${found} == /* && ${found} != */shims/* ]] || refuse 10 "no binary outside a shims directory: ${found:-none}"
done
[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || refuse 10 "main checkout is not on main"
fresh() { pre "${git}" -C "${main}" fetch -q origin main && pre "${git}" -C "${main}" rev-parse HEAD origin/main && { [ "${out%%$'\n'*}" = "${out##*$'\n'}" ] || refuse 10 "main checkout is not origin/main: run scripts/orchestrator/ff-main.sh"; }; }
fresh
# They run with the orchestrator's credentials, so each must be HEAD's own copy (PR #372 thread 4291474880).
for s in scripts/orchestrator/{sandbox-scan.sh,local-review.sh,local-advisory.sh,fill_sweep.py,acceptance-front-matter.py,orch-audit.sh} scripts/pr-feedback.py; do
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
record=${main}/.orchestration/acceptance/${task}.md
[ -f "${record}" ] || refuse 10 "no acceptance record ${record#"${main}"/}"
pre "${gh}" pr view "${pr}" --json isDraft --jq .isDraft
[ "${out}" = false ] || refuse 10 "draft PR: the worker marks it ready"
pre "${git}" -C "${review}" fetch -q origin main
# The log names repository paths only, so an extra TSV must be in the main checkout (PR #372 thread 4291474891).
[ -z "${extra}" ] || extra=$(cd -- "$(dirname -- "${extra}")" 2> /dev/null && pwd -P)/${extra##*/}
[[ -z ${extra} || ${extra} == "${main}"/* ]] || refuse 10 "extra dispositions TSV is not in the main checkout: $6"
export ORCH_REVIEW_WORKTREE=${review}
v=${main}/.orchestration/validation
for attempt in 1 2 3; do
    step fetch 0 "${git}" -C "${main}" fetch -q origin "+pull/${pr}/head:refs/remotes/pr/${pr}"
    step fetch 0 "${git}" -C "${review}" fetch -q origin "+pull/${pr}/head"
    step fetch 0 "${git}" -C "${review}" checkout -q --detach FETCH_HEAD
    step fetch 0 "${git}" -C "${review}" rev-parse HEAD
    head=${out}
    step fetch 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid
    [ "${out}" = "${head}" ] || refuse 10 "head mismatch: re-run"
    sha7=${head:0:7}
    # The log is named by the head, so the lines before it are written once it is known; a new head's log holds them all.
    [ "${log}" = "${v}/${task}-chain-${sha7}.log" ] || { log=${v}/${task}-chain-${sha7}.log && printf '%s\n' "${lines[@]}" >> "${log}"; }
    [ ! -e "${v}/${task}-audit-${sha7}.md.last.md" ] || refuse 10 "head already audited: one chain per head"
    step base 0,1 "${git}" -C "${review}" merge-base --is-ancestor origin/main HEAD
    if ((rc == 0)); then
        step checks any "${gh}" pr checks "${pr}" --required --watch
        ((rc == 0)) || refuse 12 "required checks failed"
        # Plan 020 step 4: the Bot wait is never gated, so it ends present or absent and the chain goes on.
        q="[.[] | select(.user.login == \"chatgpt-codex-connector[bot]\" and .commit_id == \"${head}\")] | length"
        t0=$("${date}" +%s)
        while step bot 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/reviews" --paginate --jq "${q}"; do
            n=$((${out//$'\n'/+})) # one count per page
            ((n == 0 && $("${date}" +%s) - t0 < ${CHAIN_BOT_WAIT:-900})) || break
            sleep 30
        done
        say "bot review: $( ((n > 0)) && echo present || echo absent)"
        # origin/main can move during the waits (PR #372 thread 4291474885): a moved base is updated, then the fetch.
        step base 0 "${git}" -C "${review}" fetch -q origin main
        step base 0,1 "${git}" -C "${review}" merge-base --is-ancestor origin/main HEAD
        ((rc == 1)) || break
    fi
    ((attempt < 3)) || refuse 13 "base moved three times"
    step base 0 "${gh}" pr update-branch "${pr}"
    t0=$("${date}" +%s) # GitHub builds the merge commit asynchronously: poll the head check's query until it moves.
    while step base 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid && [ "${out}" = "${head}" ]; do
        (($("${date}" +%s) - t0 < ${CHAIN_POLL_MAX:-120})) || refuse 10 "update-branch head not visible"
        sleep "${CHAIN_POLL_SECONDS:-5}"
    done
    fresh  # a moved base may have left the main checkout's main behind, which local-review.sh diffs against
    log='' # the next head's log takes every line; this one ends here
done
# C-29: the scan reports and exits 0, so the chain is the stop its reader used to be.
step sandbox-scan 0 "${main}/scripts/orchestrator/sandbox-scan.sh" "${task}"
[ -z "${out}" ] || say "${out}"
if [[ ${out} == *"sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"* ]]; then
    [ "${CHAIN_SCAN_JUDGED:-}" = "${sha7}" ] || refuse 16 "sandbox scan hit: judge it, then re-run with CHAIN_SCAN_JUDGED=${sha7}"
    say "sandbox scan: judged by the orchestrator"
fi
step local-review 0,3 "${main}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
findings=0
[[ ! ${out} =~ local-review:\ ([0-9]+)\ findings ]] || findings=${BASH_REMATCH[1]}
if ((rc == 3)); then
    [ -f "${main}/.orchestration/tasks/${owner}.md" ] || refuse 15 "write the owner task ${owner} first"
    step local-advisory 0,3 "${main}/scripts/orchestrator/local-advisory.sh" "${task}" "${head}" "${owner}"
    ((rc == 0)) || refuse 11 "a P0/P1 local finding: the one round or the operator"
fi
sweep=${v}/${task}-pr-feedback.json comments=${v}/${task}-pr-comments.json
step pr-feedback 0 "${uv}" run --no-project python -I "${main}/scripts/pr-feedback.py" "${pr}" --json "${sweep}"
step fill-sweep 0 "${gh}" api user --jq .login
login=${out}
# One compact object per line, joined into one array, so a second page does not end the JSON after the first.
step fill-sweep 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/comments" --paginate --jq '.[]'
printf '[%s]\n' "${out//$'\n'/,}" > "${comments}"
step fill-sweep 0,1 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/fill_sweep.py" "${sweep}" "${comments}" ${extra:+"${extra}"} --orchestrator-login "${login}"
rm -f -- "${comments}"
gaps=unknown
[[ ! ${out} =~ gaps\ ([0-9]+) ]] || gaps=${BASH_REMATCH[1]}
((rc == 0)) || refuse 14 "sweep gaps: ${gaps}"
now=$("${date}" -u +%FT%TZ)
body="orchestrator integration review of PR #${pr} at ${head}: local review ${findings} finding(s), each with its line in the acceptance record; sweep complete"
printf '[{"id": "%s", "scope": "review", "resolved": true, "author": "claude-code", "head": "%s", "pr": "%s", "reviewed_at": "%s", "body": "%s"}]\n' \
    "${task}-pr${pr}-review-1" "${head}" "${pr}" "${now}" "${body}" > "${v}/${task}-crit.json"
say "${now} receipt rc=0: printf > .orchestration/validation/${task}-crit.json"
printf 'review_surface: crit-data\nreviewer: claude-code\nreview_source: %s\nreview_outcome: approved\nhead: %s\npr: %s\nreviewed_at: %s\nnote: %s\n' \
    ".orchestration/validation/${task}-crit.json" "${head}" "${pr}" "${now}" \
    "${body} (chain-integrate.sh; the task-level audit of this head is recorded separately in .orchestration/validation/${task}-audit-${sha7}.md)" \
    > "${v}/${task}-review-receipt.md"
say "${now} receipt rc=0: printf > .orchestration/validation/${task}-review-receipt.md"
# The gate's LEDGER_ID: a thread id of ten or more digits or audit:<sha7>:<n>; local: rows stay in the prose.
tsv=${v}/${task}-ledger-${sha7}.tsv
step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
printf '%s\n' "${out}" > "${tsv}"
step record 0 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/acceptance-front-matter.py" "${task}" "${sweep}" "${review}" --ledger "${tsv}"
rm -f -- "${tsv}"
# C-61 (plan 023 F1): an update-branch-only head, a merge of main into the audited head whose PR patch is unchanged,
# inherits that head's audit under its own names; the first line names the head the audit ran on, whose ids it keeps.
patch() { "${git}" -C "${main}" diff-tree -p "$("${git}" -C "${main}" merge-base origin/main "$1")" "$1" | "${git}" -C "${main}" patch-id --stable; }
parent=$("${git}" -C "${main}" rev-parse -q --verify "${head}^1" || true) old='' new=''
from=${v}/${task}-audit-${parent:0:7}
if [[ -n ${parent} && -f ${from}.md && -f ${from}.md.last.md ]] && "${git}" -C "${main}" merge-base --is-ancestor "${head}^2" origin/main 2> /dev/null; then
    old=$(patch "${parent}") || old='' # computed outside the condition, so a failure is an empty id and a fresh audit
    new=$(patch "${head}") || new=''
fi
if [[ -n ${old} && ${old%% *} == "${new%% *}" ]]; then
    for s in .md .md.last.md; do
        # A parent that inherited keeps its marker: the ids stay those of the head the audit ran on.
        { [[ $(head -n 1 -- "${from}${s}") == inherited-from:* ]] || echo "inherited-from: ${parent:0:7}"; } > "${v}/${task}-audit-${sha7}${s}"
        cat -- "${from}${s}" >> "${v}/${task}-audit-${sha7}${s}"
    done
    say "$("${date}" -u +%FT%TZ) audit rc=0: audit inherited from ${parent:0:7} ($(head -n 1 -- "${v}/${task}-audit-${sha7}.md.last.md"))"
    echo "audit inherited from ${parent:0:7}"
    verdict="chain-integrate: ${task} ${head} $(tail -n 1 -- "${v}/${task}-audit-${sha7}.md.last.md")"
else
    step audit 0 "${main}/scripts/orchestrator/orch-audit.sh" "${task}" "${review}" "${pr}"
    verdict="chain-integrate: ${task} ${head} ${out##*$'\n'}"
    step audit 0 "${git}" -C "${review}" checkout -q --detach "${head}" # orch-audit.sh leaves it at origin/main; the gate reads it
fi
say "${verdict}" && echo "${verdict}"
