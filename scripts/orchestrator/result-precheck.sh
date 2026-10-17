#!/usr/bin/env bash
# @file result-precheck.sh
# @brief Refuse a worker's RESULT whose head is not ready: `run` writes the receipt, `verify` checks a RESULT line.
# @description
#   Plan 023 F4 item 2. `run <task> <pr> <head>` (the worker) checks (a) the task copy against the TASK line's
#   task_sha256, (b) the changed files against allowed_files, (c) the Check's caps, (d) the Check's commands in the
#   validation file, (e) CI on the head, (f) the Bot's review of the head or `bot: none` in the report, (g) every Bot
#   thread of the PR in the report as `<id>:<P>:<disposition>` (a P0/P1 `fixed:<sha>` or `open:`), (h) the local review and (i) the audit dry run,
#   the last two `unavailable (<reason>)` when they cannot run here. It writes `.orchestration/<task>/precheck-<sha7>.md`
#   and exits 1 naming each `missing`. `verify <task> <RESULT line>` (the orchestrator) finds the receipt whose sha256
#   is the line's `precheck=` in the tree of its `head=`, past which only `.orchestration/<task>/` may change, and
#   requires every check `ok`; else it prints the revise line for the orchestrator to send, exit 1. Mechanical only.
# @exitcode 0 Every check ok.
# @exitcode 1 A check missing (verify: the AGMSG-ACCEPTANCE revise line printed).
# @exitcode 2 Usage: a malformed task id, PR number or head.
# shellcheck disable=SC2016 # backticks are literal: Markdown in the receipt, the Check's spans in the regexes
set -euo pipefail
export CLICOLOR_FORCE=0 FORCE_COLOR=0 NO_COLOR=1 # gh colours JSON under CLICOLOR_FORCE even with NO_COLOR (C-62)
die() { echo "result-precheck: $1" >&2 && exit 2; }
[[ ${2:-} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || die "usage: result-precheck.sh run <task> <pr> <head> | verify <task> <RESULT line>"
task=$2 d=.orchestration/$2
cd -- "$(git rev-parse --show-toplevel)"
if [[ $1 == verify && $# == 3 ]]; then
    read -ra fields <<< "$3"
    for f in "${fields[@]}"; do case ${f} in head=*) head=${f#head=} ;; precheck=*) sum=${f#precheck=} ;; esac done
    [[ ${head:-} =~ ^[0-9a-f]{7,40}$ && ${sum:-} =~ ^[0-9a-f]{64}$ ]] || die "the RESULT line has no head= or precheck="
    git fetch -q origin 2> /dev/null || true # the branch's head, when this checkout lacks it
    miss="receipt" && head=$(git rev-parse -q --verify "${head}^{commit}") || head=''
    for p in $([ -z "${head}" ] || git ls-tree --name-only "${head}" -- "${d}/" | /usr/bin/grep -E '/precheck-[0-9a-f]{7}\.md$'); do
        [ "$(git show "${head}:${p}" | shasum -a 256 | cut -d' ' -f1)" = "${sum}" ] || continue
        h=$(git show "${head}:${p}" | sed -n 's/^head: \([0-9a-f]\{40\}\)$/\1/p')
        miss=$(git show "${head}:${p}" | sed -n 's/^- \([a-i]\) missing.*/\1/p' | tr '\n' ',')
        [ -z "$(git diff --name-only "${h}" "${head}" | /usr/bin/grep -v -F "${d}/" || true)" ] || miss+="code-after-receipt,"
    done
    [ -n "${miss%,}" ] || exit 0
    echo "AGMSG-ACCEPTANCE v1 task_id=${task} status=revise reason=precheck:${miss%,} next_action=run-result-precheck-and-resend" && exit 1
fi
[[ $1 == run && $# == 4 && $3 =~ ^[0-9]+$ && $4 =~ ^[0-9a-f]{40}$ ]] || die "usage: result-precheck.sh run <task> <pr> <head>"
pr=$3 head=$4 out=${d}/precheck-${4:0:7}.md a=${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}
printf -- '---\ntask: %s\npr: %s\nhead: %s\n---\n\n' "${task}" "${pr}" "${head}" > "${out}"
check() { # <letter> <command…>: ok or missing, with the command and its output
    local r=ok o
    o=$("${@:2}" 2>&1) || r=missing
    printf -- '- %s %s: `%s`\n\n```\n%s\n```\n\n' "$1" "${r}" "${*:2}" "${o}" >> "${out}"
}
check_a() {
    for type in claude-code codex; do [[ $(AGMSG_RESOLVE_PROJECT=0 "${a}/whoami.sh" "${PWD}" "${type}" 2> /dev/null) =~ teams=([^ ,]+) ]] && break; done
    want=$("${a}/history.sh" "${BASH_REMATCH[1]:?no agmsg team}" "" 100000 | /usr/bin/grep -F "AGMSG-TASK v1 task_id=${task} " | tail -n 1 | /usr/bin/grep -o -E 'task_sha256=[0-9a-f]{64}')
    shasum -a 256 "${d}/task.md" && [ "${want#task_sha256=}" = "$(shasum -a 256 < "${d}/task.md" | cut -d' ' -f1)" ]
}
check_b() {
    local bad=0 allowed=() # plain items, as C1 to C10 check them; bash 3.2 has no mapfile
    while IFS= read -r g; do allowed+=("${g}"); done < <(sed -n '/^allowed_files:/,/^[a-z_]*:/s/^  - //p' "${d}/task.md")
    for f in $(git diff --name-only "origin/main...${head}"); do
        # shellcheck disable=SC2053 # each allowed_files entry is a glob
        hit=no && for g in ${allowed[@]+"${allowed[@]}"}; do [[ ${f} != ${g} ]] || hit=yes; done
        echo "${hit} ${f}" && [ "${hit}" = yes ] || bad=1
    done
    return "${bad}"
}
check_c() {
    s=$(sed -n '/^## Check/,/^## /p' "${d}/task.md") && ex=$(/usr/bin/grep -o -E 'excluding [^,;]*' <<< "${s}" | /usr/bin/grep -o -E '`[^`]+`' | tr -d '`' || true)
    max=$(/usr/bin/grep -o -E 'at most [0-9]+ changed lines' <<< "${s}" | tr -dc 0-9) tmax=$(/usr/bin/grep -o -E '[0-9]+ added lines under' <<< "${s}" | tr -dc 0-9)
    git diff --numstat "origin/main...${head}" | awk -v ex="${ex//$'\n'/ }" -v max="${max:?}" -v tmax="${tmax:?}" 'BEGIN { split(ex, e, " "); for (i in e) x[e[i]] = 1 }
        $3 ~ /^tests\// { t += $1 } $3 !~ /^(tests|\.orchestration)\// && !($3 in x) { o += $1 + $2 }
        END { print "outside " o + 0 " (cap " max "), tests " t + 0 " (cap " tmax ")"; exit !(o <= max && t <= tmax) }'
}
check_d() {
    local bad=0
    for c in $(sed -n '/^## Check/,/^## /p' "${d}/task.md" | /usr/bin/grep -o -E '`(uv|shellcheck|shfmt|make|git) [^`]+`' | tr ' ' '\001'); do
        c=${c//$'\001'/ } && c=${c//\`/} && echo "${c}" && /usr/bin/grep -q -F -- "${c}" "${d}/validation.md" || bad=1
    done
    return "${bad}"
}
bot='select(.user.login == "chatgpt-codex-connector[bot]")'
check_f() {
    gh api --paginate "repos/{owner}/{repo}/pulls/${pr}/reviews" --jq ".[] | ${bot} | select(.commit_id == \"${head}\") | .id" | /usr/bin/grep . ||
        gh api --paginate "repos/{owner}/{repo}/issues/${pr}/comments" --jq ".[] | ${bot} | .body" | /usr/bin/grep -F "Reviewed commit: \`${head:0:10}" ||
        /usr/bin/grep -E "bot: none.*${head:0:7}|${head:0:7}.*bot: none" "${d}/report.md"
}
check_g() {
    gh api --paginate "repos/{owner}/{repo}/pulls/${pr}/comments" --jq ".[] | ${bot} | select(.in_reply_to_id == null) | \"\(.id) \(.body | capture(\"(?<p>P[0-3]) Badge\").p // \"P3\")\"" |
        {
            bad=0
            while read -r id p; do # the RESULT's thread token: <id>:P0|P1:fixed:<sha> or open:, <id>:P2|P3:<any>
                echo "${id} ${p}"
                /usr/bin/grep -q -E "${id}:${p}:$([[ ${p} == P[01] ]] && echo '(fixed:[0-9a-f]{7}|open:)')" "${d}/report.md" || bad=1
            done
            exit "${bad}"
        }
}
check_h() {
    lr=$(ls ".orchestration/validation/${task}-local-review-${head:0:7}.md" 2> /dev/null) || { echo "local-review: unavailable (no local review of ${head:0:7} here; a Claude seat cannot run codex review)" && return; }
    ! /usr/bin/grep -E '^\s*(- )?\[P[01]\]' "${lr}"
}
check_i() {
    command -v codex > /dev/null && codex exec --sandbox read-only -C . "Audit git diff origin/main...${head} for task ${task} by AGENTS.md's Audit section; end with one Verdict line." < /dev/null 2>&1 | tail -n 3 ||
        echo "audit-dry-run: unavailable (codex is not on PATH or not reachable from this seat)"
}
for x in a b c d; do check "${x}" "check_${x}"; done
check_e() { [ "$(gh pr view "${pr}" --json headRefOid --jq .headRefOid)" = "${head}" ] && gh pr checks "${pr}" --required; }
check e check_e
for x in f g h i; do check "${x}" "check_${x}"; done
missing=$(sed -n 's/^- \([a-i]\) missing.*/\1/p' "${out}" | tr '\n' ' ')
echo "precheck=$(shasum -a 256 < "${out}" | cut -d' ' -f1) ${out}${missing:+ missing: ${missing}}"
[ -z "${missing}" ]
