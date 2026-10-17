#!/usr/bin/env bash
# @file integrate-seat.sh
# @brief Run one PR's integration on the integration seat, from the worker's RESULT up to the audit, never past it.
# @description
#   Plan 023 F4 item 1, from the seat's own worktree at origin/main and its scripts: update-branch, CI, the Bot wait
#   (the one optional step), sweep, local review, the dispositions from the RESULT's `threads=`, thread resolution,
#   the filled sweep, receipt and record block. Each step goes to `.orchestration/validation/<task>-integration-<sha7>.md`;
#   the artifacts stay here for the orchestrator to move, and the `kind=integration` RESULT goes to the task's
#   orchestrator. Never the audit, the gate or the merge; gh needs the machine's credentials, so it runs unsandboxed.
# @arg $1 string Task id.
# @arg $2 int PR number.
# @option --owner <id> The follow-up task that owns advisory P2 findings.
# @exitcode 0 ready_for_audit sent.
# @exitcode 1 A step failed; blocked sent.
# @exitcode 2 Usage or a precondition (arguments, identity, task or RESULT on the bus, worktree not at origin/main).
set -euo pipefail
export CLICOLOR_FORCE=0 FORCE_COLOR=0 NO_COLOR=1 # gh colours JSON under CLICOLOR_FORCE even with NO_COLOR (C-62)
die() { echo "integrate-seat: $1" >&2 && exit 2; }
[[ $# == 2 || ($# == 4 && $3 == --owner) ]] || die "usage: integrate-seat.sh <task> <pr> [--owner <followup task id>]"
task=$1 pr=$2 owner=${4:-}
for id in "${task}" ${owner:+"${owner}"}; do [[ ${id} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || die "invalid id: ${id}"; done
[[ ${pr} =~ ^[0-9]+$ ]] || die "invalid PR number: ${pr}"
cd -- "$(git rev-parse --show-toplevel)"
main=$(cd -- "$(git rev-parse --path-format=absolute --git-common-dir)/.." && pwd -P) a=${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}
git fetch -q origin main && [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || die "this worktree is not at origin/main"
for type in claude-code codex; do
    who=$(AGMSG_RESOLVE_PROJECT=0 "${a}/whoami.sh" "${PWD}" "${type}" 2> /dev/null) || who=''
    [[ ${who} =~ ^agent=([^ ]+)\ teams=([^ ,]+) ]] && me=${BASH_REMATCH[1]} team=${BASH_REMATCH[2]} && break
done
[ -n "${me:-}" ] || die "no agmsg identity registered at ${PWD}"
history=$("${a}/history.sh" "${team}" "" 100000)
line() { /usr/bin/grep -F "$1 v1 task_id=${task} " <<< "${history}" | tail -n 1 || true; }
[[ $(line AGMSG-TASK) =~ \]\ ([^ ]+)\ →\  ]] || die "no AGMSG-TASK for ${task} on ${team}"
orch=${BASH_REMATCH[1]}
[[ $(line AGMSG-RESULT) =~ \ threads=([^ ]*) ]] || die "no AGMSG-RESULT with threads= for ${task}"
threads=${BASH_REMATCH[1]}
pane=$("${a}/team.sh" "${team}" --json | jq -r --arg m "${orch}" '.[] | select(.member == $m) | .pane // empty')
pane=${pane#"${pane%:*:*}":} # <socket>:<workspace>:<pane> -> <workspace>:<pane>, agmsg-dispatch's form
v=.orchestration/validation review=$(mktemp -d "${TMPDIR:-/tmp}/integrate-seat.XXXXXX")
trap 'git worktree remove --force "${review}" 2> /dev/null || true' EXIT
git fetch -q origin "+pull/${pr}/head:refs/remotes/pr/${pr}"
head=$(git rev-parse "refs/remotes/pr/${pr}") diff_head=$(git rev-parse "refs/remotes/pr/${pr}")
rec=${v}/${task}-integration-${head:0:7}.md && mkdir -p "${v}" && printf '# Integration of PR #%s for %s\n\n' "${pr}" "${task}" > "${rec}"
send() { # <status fields…>: the integration RESULT, by agmsg-dispatch to the orchestrator's pane
    agmsg-dispatch "${team}" "${me}" "${orch}" "${pane}" "AGMSG-RESULT v1 task_id=${task} kind=integration $* record=${rec}"
}
step() { # <name> <accepted statuses, comma-separated> <command…>: logged; any other status sends blocked
    local name=$1 ok=",$2,"
    shift 2
    rc=0
    out=$("$@" 2>&1) || rc=$?
    # shellcheck disable=SC2016 # the fences are literal
    printf '## %s rc=%s\n\n```console\n$ %s\n%s\n```\n\n' "${name}" "${rc}" "$*" "${out}" >> "${rec}"
    [[ ${ok} == *",${rc},"* ]] || { send "status=blocked step=${name} rc=${rc} head=${head}" && exit 1; }
}
step base 0,1 git merge-base --is-ancestor origin/main "${head}"
if ((rc == 1)); then
    step update-branch 0 gh pr update-branch "${pr}"
    for _ in $(seq 40); do
        step update-branch 0 git fetch -q origin "+pull/${pr}/head:refs/remotes/pr/${pr}"
        [ "$(git rev-parse "refs/remotes/pr/${pr}")" = "${head}" ] || break
        sleep 15
    done
    head=$(git rev-parse "refs/remotes/pr/${pr}")
fi
step pr-view 0 gh pr view "${pr}" --json headRefOid --jq .headRefOid
[ "${out}" = "${head}" ] || step head-matches 0 false
for _ in 1 2 3 4 5; do # "no checks reported" right after a push is no CI verdict
    step checks 0,1,8 gh pr checks "${pr}" --watch --interval 30
    [[ ${out} == *"no checks reported"* ]] || break
    sleep 30
done
((rc == 0)) || step checks 0 false
bot='select(.user.login == "chatgpt-codex-connector[bot]")' seen=0
# The diff head's review, or a receipt comment naming it; optional, so it may end absent.
for _ in $(seq 30); do
    seen=$({ gh api --paginate "repos/{owner}/{repo}/pulls/${pr}/reviews" --jq ".[] | ${bot} | select(.commit_id == \"${diff_head}\") | .id" &&
        gh api --paginate "repos/{owner}/{repo}/issues/${pr}/comments" --jq ".[] | ${bot} | select(.body | contains(\"Reviewed commit: \`${diff_head:0:10}\")) | .id"; } | wc -l || true)
    ((seen == 0)) || break
    sleep 30
done
printf -- '- bot review of %s: %s\n\n' "${diff_head:0:7}" "$( ((seen > 0)) && echo present || echo "none within 15 minutes")" >> "${rec}"
sweep=${v}/${task}-pr-feedback.json
step sweep 0 uv run --no-project python -I scripts/pr-feedback.py "${pr}" --json "${sweep}"
git worktree add -q --detach "${review}" "${head}"
step local-review 0,3 env ORCH_REVIEW_WORKTREE="${review}" scripts/orchestrator/local-review.sh "${task}" "${head}" "${pr}"
if ((rc == 3)); then # findings: P2/P3 become the owner's advisory rows, a P0/P1 stops the chain
    [ -n "${owner}" ] || step owner-given 0 false
    step local-advisory 0 scripts/orchestrator/local-advisory.sh "${task}" "${head}" "${owner}"
fi
dispositions=${v}/${task}-dispositions-${head:0:7}.tsv && : > "${dispositions}"
IFS=';' read -ra items <<< "${threads}"
for item in ${items[@]+"${items[@]}"}; do # <id>:<P0-P3>:<fixed:<sha>|…>, the RESULT's thread list
    [[ ${item} =~ ^([0-9]+):(P[0-3]):(.*)$ ]] || step thread-format 0 false
    id=${BASH_REMATCH[1]} p=${BASH_REMATCH[2]} d=${BASH_REMATCH[3]}
    if [[ ${d} =~ ^fixed:([0-9a-f]{7,40}) ]]; then
        printf '%s\tfixed:%s\n' "${id}" "${BASH_REMATCH[1]}" >> "${dispositions}"
    elif [[ ${p} == P[23] && -n ${owner} ]]; then
        printf '%s\tnot-applicable:advisory %s owned by %s; evidence=gh api repos/{owner}/{repo}/pulls/comments/%s\n' "${id}" "${p}" "${owner}" "${id}" >> "${dispositions}"
    else
        step "thread-${id}-${p}-not-fixed" 0 false # a P0/P1 that is not fixed stops the chain
    fi
done
step resolve-threads 0 scripts/orchestrator/resolve-threads.sh "${pr}" "${dispositions}" - "${sweep}"
step sweep 0 uv run --no-project python -I scripts/pr-feedback.py "${pr}" --json "${sweep}"
step fill-sweep 0 gh api "repos/{owner}/{repo}/pulls/${pr}/comments" --paginate --jq '.[]'
printf '[%s]\n' "${out//$'\n'/,}" > "${v}/${task}-pr-comments.json"
step fill-sweep 0 gh api user --jq .login
step fill-sweep 0 uv run --no-project python -I scripts/orchestrator/fill_sweep.py "${sweep}" "${v}/${task}-pr-comments.json" "${dispositions}" --orchestrator-login "${out}"
now=$(date -u +%FT%TZ) summary=$(git diff --shortstat "$(git merge-base origin/main "${head}")" "${head}")
body="integration seat ${me}: PR #${pr} at ${head}, ${summary# }; local review and sweep done, threads resolved"
jq -n --arg id "${task}-pr${pr}-review-1" --arg head "${head}" --arg pr "${pr}" --arg at "${now}" --arg body "${body}" \
    --arg by "${type}" '[{id: $id, scope: "review", resolved: true, author: $by, head: $head, pr: $pr, reviewed_at: $at, body: $body}]' > "${v}/${task}-crit.json"
printf 'review_surface: crit-data\nreviewer: %s\nreview_source: %s\nreview_outcome: approved\nhead: %s\npr: %s\nreviewed_at: %s\nnote: %s\n' \
    "${type}" "${v}/${task}-crit.json" "${head}" "${pr}" "${now}" "${body}" > "${v}/${task}-review-receipt.md"
mkdir -p .orchestration/acceptance # the record block goes onto the main checkout's live record, copied in
step record 0 cp -- "${main}/.orchestration/acceptance/${task}.md" .orchestration/acceptance/
step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' ".orchestration/acceptance/${task}.md"
printf '%s\n' "${out}" > "${v}/${task}-ledger-${head:0:7}.tsv"
step record 0 uv run --no-project python -I scripts/orchestrator/acceptance-front-matter.py "${task}" "${sweep}" "${review}" --ledger "${v}/${task}-ledger-${head:0:7}.tsv"
printf -- '- final head: %s\n- sweep: %s\n- receipt: %s\n- record: .orchestration/acceptance/%s.md\n' "${head}" "${sweep}" "${v}/${task}-review-receipt.md" "${task}" >> "${rec}"
send "status=ready_for_audit head=${head}"
