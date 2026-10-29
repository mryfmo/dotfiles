#!/usr/bin/env bash
# @file pr-thread-resolve.sh
# @brief Resolve one review thread of a pull request after its disposition reply, the orchestrator seat's lever.
# @description
#   Regime-cutover U28, a lever of the omp orchestrator seat, allowed by the row
#   `~/.local/bin/common/pr-thread-resolve.sh *` of `home/dot_agents/omp/policies/orchestrator.yml`
#   (scripts/orchestrator/README.md, "Seat levers for GitHub writes"). `<pr>` and `<comment-id>` are decimal and
#   checked before the first `gh` call. The thread is the one whose first comment's `databaseId` is `<comment-id>`
#   among the pull request's `reviewThreads` (GraphQL, read-only); the lever refuses when no thread has it, when
#   the thread is already resolved, and when the listing has more than 100 threads or a thread more than 100
#   comments (a page it did not read). The thread's newest reply must hold a disposition that is valid by the rule
#   `pr-threads-check.sh` applies before a merge (U28b F1; the function `disposition` is the same in both files):
#   `fixed: <sha>` names a commit of this checkout that is the pull request's head or an ancestor of it and was
#   committed after the thread's first comment; `refuted:` cites a URL or a `file:line`; `residual: unit=U<n>`
#   answers a P2 or P3 finding and `units.tsv` in `--records` has the row; `residual: operator=<ts>` has its
#   `decisions.tsv` row in `--records`. So a resolution never hides a finding the merge check would refuse. The
#   one write is the `resolveReviewThread` mutation on that thread id. `<owner>/<repo>` comes from
#   `gh repo view --json nameWithOwner`. Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
# @arg $1 int The pull request number.
# @arg $2 int The id of the thread's first review comment.
# @option --records <dir> The program's records directory, holding `units.tsv` and `decisions.tsv`.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `resolved pr=<pr> comment=<id> thread=<node id> disposition=<disposition>`.
# @exitcode 0 The thread was resolved.
# @exitcode 1 A `gh` or `git` read or the mutation failed, or the mutation did not report the thread resolved.
# @exitcode 2 Refused: usage, no such thread, already resolved, no valid disposition, or an unread page.
# @example
#   ~/.local/bin/common/pr-thread-resolve.sh 480 4365170609 --records .orchestration/orchestrate/regime-cutover
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
    # shellcheck disable=SC2034 # read by the levers that source regime-env from this directory
    LEVER_DIR=${dir}
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

# The isolated git and the environment scrub come from the library beside this script (U113): `disposition` is one
# text with pr-threads-check.sh's (U28b F1), so its ancestry and commit-date reads go through the same git.
[[ -r ${LEVER_DIR}/git-isolated.sh ]] || {
    echo "pr-thread-resolve.sh: refused: git-isolated.sh unreadable beside this script: ${LEVER_DIR}/git-isolated.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/git-isolated.sh
. "${LEVER_DIR}/git-isolated.sh"
# shellcheck disable=SC2119 # no name is kept: every GIT_* and transport variable goes
git_env_scrub

lever='pr-thread-resolve.sh'
usage='usage: pr-thread-resolve.sh <pr> <comment-id> [--records <dir>]'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
# shellcheck disable=SC2016 # GraphQL variables, not shell
threads_query='query($owner: String!, $name: String!, $pr: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $pr) {
      headRefOid
      reviewThreads(first: 100) {
        pageInfo { hasNextPage }
        nodes { id isResolved comments(first: 100) { totalCount nodes { databaseId createdAt body } } }
      }
    }
  }
}'
# `head <sha> <hasNextPage>`, then per thread `<node id> <resolved> <first id> <created epoch> <P0-P3 or -> <count>
# <newest reply's first line>` (TSV; the reply is last because it may be empty).
# shellcheck disable=SC2016 # jq source, not shell
threads_jq='.data.repository.pullRequest
  | (["head", .headRefOid, (.reviewThreads.pageInfo.hasNextPage | tostring)] | @tsv),
    (.reviewThreads.nodes[] | .comments as $c | [.id, (.isResolved | tostring),
      ($c.nodes[0].databaseId | tostring), ($c.nodes[0].createdAt | fromdateiso8601 | tostring),
      ([($c.nodes[0].body // "") | capture("!\\[P(?<p>[0-3]) Badge\\]") | "P" + .p] | first // "-"),
      ($c.totalCount | tostring),
      (($c.nodes[1:] | last | .body // "") | split("\n") | (.[0] // "") | rtrimstr("\r"))] | @tsv)'
# shellcheck disable=SC2016 # GraphQL variables, not shell
resolve_mutation='mutation($thread: ID!) { resolveReviewThread(input: {threadId: $thread}) { thread { id isResolved } } }'

# @description Print the refusal on stderr and exit 2; nothing was written to GitHub.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print the failure on stderr and exit 1: a read or the write failed.
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
        git_isolated cat-file -e "${fix}^{commit}" 2> /dev/null || {
            echo "open (fixed: ${fix} is not a commit here)"
            return
        }
        status=0
        git_isolated merge-base --is-ancestor "${fix}" "${head}" || status=$?
        case ${status} in
        0) ;;
        1)
            echo "open (fixed: ${fix} is not in the head)"
            return
            ;;
        *) fail "git merge-base --is-ancestor ${fix} ${head} failed" ;;
        esac
        fix_time=$(git_isolated show -s --format=%ct "${fix}") || fail "git show ${fix} failed"
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
comment=''
records=''
while (($#)); do
    case $1 in
    --records)
        (($# >= 2)) || refuse "${usage}"
        records=$2
        shift 2
        ;;
    -*) refuse "${usage}" ;;
    *)
        if [[ -z ${pr} ]]; then
            pr=$1
        elif [[ -z ${comment} ]]; then
            comment=$1
        else
            refuse "${usage}"
        fi
        shift
        ;;
    esac
done
[[ -n ${pr} && -n ${comment} ]] || refuse "${usage}"
[[ ${pr} =~ ^[1-9][0-9]{0,9}$ ]] || refuse "the pull request is not a decimal number: ${pr}"
[[ ${comment} =~ ^[1-9][0-9]{0,19}$ ]] || refuse "the comment id is not a decimal number: ${comment}"
[[ -z ${records} || (-f ${records}/units.tsv && -f ${records}/decisions.tsv) ]] ||
    refuse "--records holds no units.tsv and decisions.tsv: ${records}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'

repo=$(gh_bounded repo view --json nameWithOwner --jq .nameWithOwner) || fail 'gh repo view failed'
[[ ${repo} =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || fail "gh repo view printed no owner/repo: ${repo}"
listing=$(gh_bounded api graphql -f "query=${threads_query}" -f "owner=${repo%%/*}" -f "name=${repo#*/}" \
    -F "pr=${pr}" --jq "${threads_jq}") || fail "cannot list the review threads of pull request ${pr}"

head=''
page=''
thread=''
while IFS=$'\t' read -r id resolved first created severity count reply; do
    if [[ ${id} == head ]]; then
        head=${resolved}
        page=${first}
    elif [[ ${first} == "${comment}" ]]; then
        thread=${id}
        thread_resolved=${resolved}
        thread_created=${created}
        thread_severity=${severity}
        thread_count=${count}
        thread_reply=${reply}
    fi
done <<< "${listing}"
[[ ${head} =~ ^[0-9a-f]{40}$ ]] || fail "the listing of pull request ${pr} has no readable head"
[[ ${page} == false ]] || refuse "pull request ${pr} has more than 100 review threads; resolve it by hand"
[[ -n ${thread} ]] || refuse "no review thread of pull request ${pr} starts with comment ${comment}"
[[ ${thread_resolved} == false ]] || refuse "the thread of comment ${comment} is already resolved"
if ! [[ ${thread_count} =~ ^[0-9]+$ ]] || ((thread_count > 100)); then
    refuse "the thread of comment ${comment} has more than 100 comments; resolve it by hand"
fi
[[ ${thread_created} =~ ^[0-9]+$ ]] || fail "unreadable creation time for the thread of comment ${comment}"
git_isolated cat-file -e "${head}^{commit}" 2> /dev/null || refuse "the head ${head} of pull request ${pr} is not a commit here; git fetch first"
state=$(disposition "${thread_created}" "${thread_severity}" "${thread_reply}") || exit $?
[[ ${state} != open* ]] ||
    refuse "the thread of comment ${comment} has no valid disposition, ${state#open }; reply with pr-thread-reply.sh first"

done_id=$(gh_bounded api graphql -f "query=${resolve_mutation}" -f "thread=${thread}" \
    --jq '.data.resolveReviewThread.thread | select(.isResolved) | .id') || fail "resolveReviewThread failed for ${thread}"
[[ ${done_id} == "${thread}" ]] || fail "resolveReviewThread did not report ${thread} resolved"
echo "resolved pr=${pr} comment=${comment} thread=${thread} disposition=${state}"
