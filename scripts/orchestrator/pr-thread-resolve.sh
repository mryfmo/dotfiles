#!/usr/bin/env bash
# @file pr-thread-resolve.sh
# @brief Resolve one review thread of a pull request after its disposition reply, the orchestrator seat's lever.
# @description
#   Regime-cutover U28, a lever of the omp orchestrator seat, allowed by the row
#   `~/.local/bin/common/pr-thread-resolve.sh *` of `home/dot_agents/omp/policies/orchestrator.yml`
#   (scripts/orchestrator/README.md, "Seat levers for GitHub writes"). `<pr>` and `<comment-id>` are decimal and
#   checked before the first `gh` call. The thread is the one whose first comment's `databaseId` is `<comment-id>`
#   among the pull request's `reviewThreads` (GraphQL, read-only); the lever refuses when no thread has it, when
#   the thread is already resolved, when its newest reply's first line is not a disposition of `preferences.md`
#   standing order 22 (the grammar `pr-thread-reply.sh` posts and `pr-threads-check.sh` reads), so a resolution
#   never hides an undisposed finding, and when the listing has more than 100 threads or a thread more than 100
#   comments (a page it did not read). The one write is the `resolveReviewThread` mutation on that thread id.
#   `<owner>/<repo>` comes from `gh repo view --json nameWithOwner`. Each `gh` call is bounded by
#   PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
# @arg $1 int The pull request number.
# @arg $2 int The id of the thread's first review comment.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `resolved pr=<pr> comment=<id> thread=<node id>`.
# @exitcode 0 The thread was resolved.
# @exitcode 1 A `gh` read or the mutation failed, or the mutation did not report the thread resolved.
# @exitcode 2 Refused: usage, no such thread, already resolved, no disposition reply, or an unread page.
# @example
#   ~/.local/bin/common/pr-thread-resolve.sh 480 4365170609
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

lever='pr-thread-resolve.sh'
usage='usage: pr-thread-resolve.sh <pr> <comment-id>'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
# Each thread as `<id> <resolved> <first comment id> <comment count> <newest reply's first line>` (TSV), after one
# `page <hasNextPage>` row.
# shellcheck disable=SC2016 # GraphQL variables, not shell
threads_query='query($owner: String!, $name: String!, $pr: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        pageInfo { hasNextPage }
        nodes { id isResolved comments(first: 100) { totalCount nodes { databaseId body } } }
      }
    }
  }
}'
threads_jq='.data.repository.pullRequest.reviewThreads
  | (["page", (.pageInfo.hasNextPage | tostring)] | @tsv),
    (.nodes[] | [.id, (.isResolved | tostring), (.comments.nodes[0].databaseId | tostring),
      (.comments.totalCount | tostring),
      ((.comments.nodes[1:] | last | .body // "") | split("\n")[0] | rtrimstr("\r"))] | @tsv)'
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

# @description Succeed when $1, a reply's first line, is a disposition (`preferences.md` standing order 22).
# @arg $1 string The line.
disposition_line() {
    local fixed='^fixed: [0-9a-f]{40}( |$)'
    local refuted='^refuted: .*(https://[^[:space:]]+|[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*:[0-9]+)'
    local unit='^residual: unit=U[0-9]+[a-z]? gate=[^[:space:]]'
    local operator='^residual: operator=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$'
    [[ $1 =~ ${fixed} || $1 =~ ${refuted} || $1 =~ ${unit} || $1 =~ ${operator} ]]
}

[[ $# -eq 2 ]] || refuse "${usage}"
pr=$1
comment=$2
[[ ${pr} =~ ^[1-9][0-9]{0,9}$ ]] || refuse "the pull request is not a decimal number: ${pr}"
[[ ${comment} =~ ^[1-9][0-9]{0,19}$ ]] || refuse "the comment id is not a decimal number: ${comment}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'

repo=$(gh_bounded repo view --json nameWithOwner --jq .nameWithOwner) || fail 'gh repo view failed'
[[ ${repo} =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || fail "gh repo view printed no owner/repo: ${repo}"
listing=$(gh_bounded api graphql -f "query=${threads_query}" -f "owner=${repo%%/*}" -f "name=${repo#*/}" \
    -F "pr=${pr}" --jq "${threads_jq}") || fail "cannot list the review threads of pull request ${pr}"

page=''
thread=''
while IFS=$'\t' read -r id resolved first count reply; do
    if [[ ${id} == page ]]; then
        page=${resolved}
    elif [[ ${first} == "${comment}" ]]; then
        thread=${id}
        thread_resolved=${resolved}
        thread_count=${count}
        thread_reply=${reply}
    fi
done <<< "${listing}"
[[ ${page} == false ]] || refuse "pull request ${pr} has more than 100 review threads (or the listing is unreadable); resolve it by hand"
[[ -n ${thread} ]] || refuse "no review thread of pull request ${pr} starts with comment ${comment}"
[[ ${thread_resolved} == false ]] || refuse "the thread of comment ${comment} is already resolved"
if ! [[ ${thread_count} =~ ^[0-9]+$ ]] || ((thread_count > 100)); then
    refuse "the thread of comment ${comment} has more than 100 comments; resolve it by hand"
fi
disposition_line "${thread_reply}" ||
    refuse "the newest reply in the thread of comment ${comment} is not a disposition; reply with pr-thread-reply.sh first"

done_id=$(gh_bounded api graphql -f "query=${resolve_mutation}" -f "thread=${thread}" \
    --jq '.data.resolveReviewThread.thread | select(.isResolved) | .id') || fail "resolveReviewThread failed for ${thread}"
[[ ${done_id} == "${thread}" ]] || fail "resolveReviewThread did not report ${thread} resolved"
echo "resolved pr=${pr} comment=${comment} thread=${thread}"
