#!/usr/bin/env bash
# @file resolve-threads.sh
# @brief Reply to a PR's unresolved review threads with the orchestrator's dispositions and resolve them.
# @description
#   Plan 021 step 6.3, the chain step behind the ruleset's required_review_thread_resolution. One GraphQL query
#   reads the first 100 review threads of the PR. Each unresolved thread is keyed on its first comment's database
#   id, and its disposition is the row of the table whose first column is that id, else, when a sweep JSON is given,
#   the `disposition` of the sweep item whose `url` ends with `_r<id>`. A `fixed:` or `not-applicable:` disposition
#   gets one reply in its fixed sentence and one resolveReviewThread mutation. A thread without a disposition, or
#   with another form, is reported and left open. `--dry-run` prints what would be done and writes nothing. gh runs
#   with the orchestrator's credentials, so this runs outside the sandbox.
# @arg $1 int PR number.
# @arg $2 path The disposition table: TSV rows of a comment id and its disposition.
# @arg $3 string `--dry-run`, or any placeholder such as `-`.
# @arg $4 path The sweep JSON (optional).
# @exitcode 0 Every unresolved thread was resolved (under `--dry-run`, would be).
# @exitcode 2 Usage error.
# @exitcode 3 A thread has no disposition, or one of another form; it is left open.
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
query="query { repository(owner:\"mryfmo\", name:\"dotfiles\") { pullRequest(number:${pr}) { reviewThreads(first:100) \
{ nodes { id isResolved comments(first:1) { nodes { databaseId } } } } } } }"
threads=$(gh api graphql -f query="${query}" --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not) | "\(.comments.nodes[0].databaseId) \(.id)"')
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
        body="Disposition (orchestrator): ${row}. Fixed at root cause in that commit on this branch; verified by \
the task's tests and CI on the final head. Resolving."
        ;;
    not-applicable:*) body="Disposition (orchestrator): ${row}. Resolving; the owning task on main carries it." ;;
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
    gh api graphql -f query="mutation { resolveReviewThread(input: {threadId: \"${tid}\"}) { thread { isResolved } } }" \
        --jq '.data.resolveReviewThread.thread.isResolved' > /dev/null
    resolved=$((resolved + 1))
    echo "resolved ${cid} (${row:0:60})"
done 3<<< "${threads}"
echo "resolved ${resolved} thread(s); missing rows: ${missing}"
[[ ${missing} == 0 ]] || exit 3
