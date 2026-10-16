#!/usr/bin/env bash
# @file resolve-threads.sh
# @brief Reply to a PR's unresolved review threads with the orchestrator's dispositions and resolve them.
# @description
#   Plan 021 step 6.3, the chain step behind the ruleset's required_review_thread_resolution. One GraphQL query
#   reads the first 100 review threads of the PR. Each unresolved thread is keyed on its first comment's database
#   id, and its disposition is the row of the table whose first column is that id, else, when a sweep JSON is given,
#   the `disposition` of the sweep item whose `url` ends with `_r<id>`. A `fixed:` or `not-applicable:` disposition
#   gets one reply in its fixed sentence, the disposition in backticks as fill_sweep.py reads a reply back, and one
#   resolveReviewThread mutation, the thread id passed as a GraphQL variable; the thread counts as resolved only when
#   the mutation answers `isResolved` true. A thread without a disposition, with another form, or not answered true
#   is reported and left open. `--dry-run` prints what would be done and writes nothing. gh runs with the
#   orchestrator's credentials, so this runs outside the sandbox. A disposition holding a backtick in either local
#   source refuses the run before any gh call because the reply cannot carry it losslessly.
# @arg $1 int PR number.
# @arg $2 path The disposition table: TSV rows of a comment id and its disposition.
# @arg $3 string `--dry-run`, or any placeholder such as `-`.
# @arg $4 path The sweep JSON (optional).
# @exitcode 0 Every unresolved thread was resolved (under `--dry-run`, would be).
# @exitcode 2 Usage error, or a local disposition holds a backtick that the reply cannot carry losslessly.
# @exitcode 3 A thread has no disposition, one of another form, or a resolve answer other than true; it is left open.
# @example
#   scripts/orchestrator/resolve-threads.sh 355 extra.tsv - .orchestration/validation/t-a01-pr-feedback.json
set -euo pipefail

usage() {
    echo "usage: resolve-threads.sh <pr> <extra.tsv> [--dry-run|-] [<sweep.json>]" >&2
    exit 2
}
(($# >= 2 && $# <= 4)) || usage
pr=$1 tsv=$2 dry=${3:-} sweep=${4:-}
[[ ${pr} =~ ^[0-9]+$ && -f ${tsv} ]] || usage
bad=$(awk -F'\t' '!/^#/ && index($2, "`") {print $1; exit}' "${tsv}")
if [[ -z ${bad} && -s ${sweep} ]]; then
    bad=$(jq -r 'first(.items[] | select((.url // "") | test("_r[0-9]+$")) |
        select((.disposition // "") | contains("`")) | .url | capture("_r(?<id>[0-9]+)$").id) // ""' "${sweep}")
fi
if [[ -n ${bad} ]]; then
    echo "resolve-threads: disposition for ${bad} holds a backtick; the reply cannot carry it losslessly" >&2
    exit 2
fi
query="query { repository(owner:\"mryfmo\", name:\"dotfiles\") { pullRequest(number:${pr}) { reviewThreads(first:100) \
{ nodes { id isResolved comments(first:1) { nodes { databaseId } } } } } } }"
threads=$(gh api graphql -f query="${query}" --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not) | "\(.comments.nodes[0].databaseId) \(.id)"')
# The thread id travels as a GraphQL variable, never inside the query text.
# shellcheck disable=SC2016 # $threadId is GraphQL's variable, not the shell's
resolve='mutation ($threadId: ID!) { resolveReviewThread(input: {threadId: $threadId}) { thread { isResolved } } }'
missing=0 resolved=0
# The threads come in on fd 3, so a command in the loop that reads stdin cannot swallow the rest of them.
while read -r cid tid <&3; do
    [[ -n ${cid} ]] || continue
    row=$(awk -F'\t' -v id="${cid}" '$1 == id {print $2; exit}' "${tsv}")
    if [[ -z ${row} && -s ${sweep} ]]; then
        row=$(jq -r --arg suffix "_r${cid}" \
            'first(.items[] | select((.url // "") | endswith($suffix)) | .disposition // "") // ""' "${sweep}")
    fi
    if [[ -z ${row} ]]; then
        echo "no disposition row for thread ${cid} (table or sweep); left open"
        missing=1
        continue
    fi
    case ${row} in
    fixed:*)
        body="Disposition (orchestrator): \`${row}\`. Fixed at root cause in that commit on this branch; verified by \
the task's tests and CI on the final head. Resolving."
        ;;
    not-applicable:*) body="Disposition (orchestrator): \`${row}\`. Resolving; the owning task on main carries it." ;;
    *)
        echo "row for ${cid} has an unknown form: ${row}"
        missing=1
        continue
        ;;
    esac
    if [[ ${dry} == --dry-run ]]; then
        echo "would reply+resolve ${cid}: ${row:0:90}"
        continue
    fi
    gh api -X POST "repos/mryfmo/dotfiles/pulls/${pr}/comments/${cid}/replies" -f body="${body}" --jq '.id' > /dev/null
    state=$(gh api graphql -f query="${resolve}" -f threadId="${tid}" --jq '.data.resolveReviewThread.thread.isResolved')
    if [[ ${state} != true ]]; then
        echo "thread ${cid} not resolved (isResolved: ${state:-none}); left open"
        missing=1
        continue
    fi
    resolved=$((resolved + 1))
    echo "resolved ${cid} (${row:0:60})"
done 3<<< "${threads}"
echo "resolved ${resolved} thread(s); missing rows: ${missing}"
[[ ${missing} == 0 ]] || exit 3
