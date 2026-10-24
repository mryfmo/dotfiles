#!/usr/bin/env bash
# @file pr-threads-check.sh
# @brief Refuse a merge while a review thread of the pull request has no disposition, read-only.
# @description
#   Regime-cutover U28 (ADDENDUM 2), the orchestrator seat's pre-merge check, allowed by the row
#   `~/.local/bin/common/pr-threads-check.sh *` of `home/dot_agents/omp/policies/orchestrator.yml`; the
#   `hcom-orchestration` SKILL runs it before the merge command (step 6). It lists every review thread of the
#   pull request (GraphQL `reviewThreads`, read-only; more than 100 threads, or more than 100 comments in one,
#   is a refusal, never a partial read) and requires `--head` to be the pull request's current `headRefOid` and
#   a commit in this checkout (`git fetch` first). Every thread, resolved or not (GitHub's `isResolved` alone
#   proves nothing, U28b F1), passes only when the first line of its newest reply is a disposition of
#   `preferences.md` standing order 22, checked here:
#   `fixed: <sha>` when `<sha>` is `--head` or an ancestor of it and was committed after the thread's first
#   comment (so a thread opened after the head cannot be `fixed`); `refuted: <text>` citing a URL or a
#   `file:line`; `residual: unit=U<n> gate=<clause>` when the finding is P2 or P3 (the `![P<n> Badge]` of its
#   first comment; no badge counts as P1) and `units.tsv` in `--records` has the row `U<n>`; or
#   `residual: operator=<ts>` when `decisions.tsv` in `--records` has a row at `<ts>`, the only residual for a P1.
#   A residual without `--records` is a refusal. Any other newest reply, or none, is a refusal: the remedy is a
#   `U<n>b` TASK or a `pr-thread-reply.sh` disposition, never a merge. `<owner>/<repo>` comes from
#   `gh repo view --json nameWithOwner`. Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
# @arg $1 int The pull request number.
# @option --head <sha> The head the orchestrator is about to merge (40 hex).
# @option --records <dir> The program's records directory, holding `units.tsv` and `decisions.tsv`.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One line per thread, `thread comment=<id> severity=<P0-P3> state=<disposition>`, then
#   `summary threads=<n> open=<n>`.
# @exitcode 0 Every thread carries a valid disposition.
# @exitcode 1 A `gh` or `git` read failed.
# @exitcode 2 Refused: usage, a moved or unknown head, an unread page, or at least one thread without a valid
#   disposition (its line says `state=open`).
# @example
#   ~/.local/bin/common/pr-threads-check.sh 480 --head 907240ec0f2b1f8b0a6a8b1f1c0b3f0d0e2a4b6c --records .orchestration/orchestrate/regime-cutover
set -euo pipefail

# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
lever_self_check() {
    local src dir self name pin digest home
    # The directory is split from the path in the shell, so no external producer (dirname) can fail unseen.
    src=${BASH_SOURCE[0]}
    case ${src} in
    */*) dir=${src%/*} ;;
    *) dir=. ;;
    esac
    [[ -n ${dir} ]] || dir=/
    dir=$(cd "${dir}" && pwd -P) || {
        echo "${src##*/}: refused: cannot resolve the script directory of ${src}" >&2
        exit 2
    }
    self=${dir}/${BASH_SOURCE[0]##*/}
    name=${self##*/}
    home=$(cd "${HOME}" 2> /dev/null && pwd -P) || home=''
    if [[ -n ${home} && ${dir} == "${home}/.local/bin/common" ]]; then # lint-comparisons: allow both sides are pwd -P forms
        LEVER_MANIFEST=${HOME}/.agents/agent-config.yaml
    else
        LEVER_MANIFEST=${dir}/../../home/dot_agents/agent-config.yaml
    fi
    [[ -r ${LEVER_MANIFEST} ]] || {
        echo "${name}: refused: manifest unreadable: ${LEVER_MANIFEST}" >&2
        exit 2
    }
    pin=$(sed -n -E "s/^      ${name//./\\.}: ([0-9a-f]{64})\$/\\1/p" "${LEVER_MANIFEST}") || {
        echo "${name}: refused: cannot read ${LEVER_MANIFEST}" >&2
        exit 2
    }
    [[ ${pin} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: no single sha256 pin for ${name} in ${LEVER_MANIFEST}" >&2
        exit 2
    }
    if command -v sha256sum > /dev/null; then
        digest=$(sha256sum < "${self}") || digest=''
    else
        digest=$(shasum -a 256 < "${self}") || digest=''
    fi
    digest=${digest%% *}
    [[ ${digest} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: cannot hash ${self}" >&2
        exit 2
    }
    [[ ${digest} == "${pin}" ]] || {
        echo "${name}: refused: sha256 ${digest} of ${self} differs from the pin in ${LEVER_MANIFEST}" >&2
        exit 2
    }
}
lever_self_check

lever='pr-threads-check.sh'
usage='usage: pr-threads-check.sh <pr> --head <sha> [--records <dir>]'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
# shellcheck disable=SC2016 # GraphQL variables, not shell
threads_query='query($owner: String!, $name: String!, $pr: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $pr) {
      headRefOid
      reviewThreads(first: 100) {
        pageInfo { hasNextPage }
        nodes { isResolved comments(first: 100) { totalCount nodes { databaseId createdAt body } } }
      }
    }
  }
}'
# `head <sha> <hasNextPage>`, then per thread `<first id> <resolved> <created epoch> <P0-P3 or -> <count> <newest
# reply's first line>` (TSV; the reply is last because it may be empty).
# shellcheck disable=SC2016 # jq source, not shell
threads_jq='.data.repository.pullRequest
  | (["head", .headRefOid, (.reviewThreads.pageInfo.hasNextPage | tostring)] | @tsv),
    (.reviewThreads.nodes[] | .comments as $c | [($c.nodes[0].databaseId | tostring), (.isResolved | tostring),
      ($c.nodes[0].createdAt | fromdateiso8601 | tostring),
      ([($c.nodes[0].body // "") | capture("!\\[P(?<p>[0-3]) Badge\\]") | "P" + .p] | first // "-"),
      ($c.totalCount | tostring),
      (($c.nodes[1:] | last | .body // "") | split("\n") | (.[0] // "") | rtrimstr("\r"))] | @tsv)'

# @description Print the refusal on stderr and exit 2.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print the failure on stderr and exit 1: a read failed.
# @arg $@ string The reason.
fail() {
    echo "${lever}: $*" >&2
    exit 1
}

# @description Run `gh` with its wait bounded by PR_LEVER_GH_TIMEOUT seconds.
# @arg $@ string The `gh` arguments.
gh_bounded() {
    perl -e 'alarm shift; exec @ARGV or die "exec gh: $!\n"' "${gh_timeout}" gh "$@"
}

# @description Succeed when the TSV file $1 has a row whose first field is $2.
# @arg $1 path The file.
# @arg $2 string The key.
# @exitcode 0 Found. 1 Not found. 2 Unreadable.
has_row() {
    [[ -r $1 ]] || return 2
    ROW_KEY=$2 awk -F '\t' '$1 == ENVIRON["ROW_KEY"] { found = 1 } END { exit !found }' "$1" || return 1
}

# @description Print the disposition a thread's newest reply carries, or `open (<why>)`.
# @arg $1 int The created epoch of the thread's first comment.
# @arg $2 string Its severity, P0-P3 or `-`.
# @arg $3 string The first line of the newest reply.
disposition() {
    local created=$1 severity=$2 line=$3 fix fix_time status
    local fixed='^fixed: ([0-9a-f]{40})( |$)'
    local refuted='^refuted: .*(https://[^[:space:]]+|[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*:[0-9]+)'
    local unit='^residual: unit=(U[0-9]+[a-z]?) gate=[^[:space:]]'
    local operator='^residual: operator=([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)$'
    if [[ ${line} =~ ${fixed} ]]; then
        fix=${BASH_REMATCH[1]}
        git cat-file -e "${fix}^{commit}" 2> /dev/null || {
            echo "open (fixed: ${fix} is not a commit here)"
            return
        }
        status=0
        git merge-base --is-ancestor "${fix}" "${head}" || status=$?
        case ${status} in
        0) ;;
        1)
            echo "open (fixed: ${fix} is not in the head)"
            return
            ;;
        *) fail "git merge-base --is-ancestor ${fix} ${head} failed" ;;
        esac
        fix_time=$(git show -s --format=%ct "${fix}") || fail "git show ${fix} failed"
        if ((fix_time < created)); then
            echo "open (fixed: ${fix} predates the finding)"
            return
        fi
        echo "fixed ${fix}"
    elif [[ ${line} =~ ${refuted} ]]; then
        echo refuted
    elif [[ ${line} =~ ${unit} ]]; then
        fix=${BASH_REMATCH[1]}
        [[ ${severity} == P2 || ${severity} == P3 ]] || {
            echo "open (residual: unit= is for P2 and P3; this is ${severity/-/P1 (no badge)})"
            return
        }
        [[ -n ${records} ]] || refuse "a residual needs --records to check units.tsv"
        status=0
        has_row "${records}/units.tsv" "${fix}" || status=$?
        case ${status} in
        0) echo "residual ${fix}" ;;
        1) echo "open (residual: no units.tsv row ${fix})" ;;
        *) fail "cannot read ${records}/units.tsv" ;;
        esac
    elif [[ ${line} =~ ${operator} ]]; then
        fix=${BASH_REMATCH[1]}
        [[ -n ${records} ]] || refuse "a residual needs --records to check decisions.tsv"
        status=0
        has_row "${records}/decisions.tsv" "${fix}" || status=$?
        case ${status} in
        0) echo "residual operator=${fix}" ;;
        1) echo "open (residual: no decisions.tsv row at ${fix})" ;;
        *) fail "cannot read ${records}/decisions.tsv" ;;
        esac
    elif [[ -z ${line} ]]; then
        echo 'open (no reply)'
    else
        echo 'open (the newest reply is not a disposition)'
    fi
}

pr=''
head=''
records=''
while (($#)); do
    case $1 in
    --head | --records)
        (($# >= 2)) || refuse "${usage}"
        if [[ $1 == --head ]]; then
            head=$2
        else
            records=$2
        fi
        shift 2
        ;;
    -*) refuse "${usage}" ;;
    *)
        [[ -z ${pr} ]] || refuse "${usage}"
        pr=$1
        shift
        ;;
    esac
done
[[ ${pr} =~ ^[1-9][0-9]{0,9}$ ]] || refuse "the pull request is not a decimal number: ${pr:-none}; ${usage}"
[[ ${head} =~ ^[0-9a-f]{40}$ ]] || refuse "--head is not a 40-hex sha: ${head:-none}"
[[ -z ${records} || (-f ${records}/units.tsv && -f ${records}/decisions.tsv) ]] ||
    refuse "--records holds no units.tsv and decisions.tsv: ${records}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'
git cat-file -e "${head}^{commit}" 2> /dev/null || refuse "${head} is not a commit in this checkout; git fetch first"

repo=$(gh_bounded repo view --json nameWithOwner --jq .nameWithOwner) || fail 'gh repo view failed'
[[ ${repo} =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || fail "gh repo view printed no owner/repo: ${repo}"
listing=$(gh_bounded api graphql -f "query=${threads_query}" -f "owner=${repo%%/*}" -f "name=${repo#*/}" \
    -F "pr=${pr}" --jq "${threads_jq}") || fail "cannot list the review threads of pull request ${pr}"

threads=0
open=0
seen_head=0
while IFS=$'\t' read -r first resolved created severity count reply; do
    if [[ ${first} == head ]]; then
        [[ ${resolved} == "${head}" ]] || refuse "the head of pull request ${pr} is ${resolved}, not ${head}"
        [[ ${created} == false ]] || refuse "pull request ${pr} has more than 100 review threads; check it by hand"
        seen_head=1
        continue
    fi
    ((seen_head)) || fail "the listing of pull request ${pr} does not start with its head"
    [[ ${first} =~ ^[0-9]+$ && ${created} =~ ^[0-9]+$ && ${count} =~ ^[0-9]+$ ]] ||
        fail "unreadable thread row: ${first}"
    ((count <= 100)) || refuse "the thread of comment ${first} has more than 100 comments; check it by hand"
    threads=$((threads + 1))
    # A resolved thread is judged like an open one (U28b F1): GitHub's isResolved says someone clicked, not why.
    state=$(disposition "${created}" "${severity}" "${reply}") || exit $?
    if [[ ${resolved} == true ]]; then
        case ${state} in
        open*) state="open (resolved without a valid disposition: ${state#open (}" ;;
        *) state="resolved ${state}" ;;
        esac
    fi
    [[ ${state} != open* ]] || open=$((open + 1))
    echo "thread comment=${first} severity=${severity/-/none} state=${state}"
done <<< "${listing}"
((seen_head)) || fail "the listing of pull request ${pr} has no head"
echo "summary threads=${threads} open=${open}"
((open == 0)) || exit 2
