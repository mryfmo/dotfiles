#!/usr/bin/env bash
# @file pr-cost.sh
# @brief Append one cost ledger line for a PR to `.orchestration/metrics/pr-cost.tsv`.
# @description
#   Plan 020 step 0, a chain step since plan 021 step 6.3. In the repository that holds the current directory, it
#   creates `.orchestration/metrics/pr-cost.tsv` with its header once and reads the PR, its reviews, its review
#   comments and its commits from the GitHub API. It appends one line with these fields:
#   the PR; its branch; when it was created; when it merged, or `open`; the wall hours from creation to the merge
#   or to now; its commits; the Codex Bot's reviews; the Bot's top-level comments badged P0 or P1, and those badged
#   P2 or P3; the local-review files whose `pr:` line names the PR; the update-branch merge commits; and when the
#   line was recorded. gh runs with the orchestrator's credentials, so this runs outside the sandbox.
# @arg $1 int PR number.
# @stdout The appended line.
# @exitcode 0 The line was appended.
# @exitcode 2 Usage error.
# @example
#   scripts/orchestrator/pr-cost.sh 355
set -euo pipefail

usage() {
    echo "usage: pr-cost.sh <pr>" >&2
    exit 2
}
(($# == 1)) || usage
pr=$1
[[ ${pr} =~ ^[0-9]+$ ]] || usage
api="repos/mryfmo/dotfiles/pulls/${pr}"
# --paginate applies --jq to each page, so the per-page counts are summed.
count() {
    gh api "$1" --paginate --jq "$2" | awk '{n += $1} END {print n + 0}'
}
cd -- "$(git rev-parse --show-toplevel)"
mkdir -p .orchestration/metrics
ledger=.orchestration/metrics/pr-cost.tsv
[[ -s ${ledger} ]] || printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' pr branch created merged wall_h commits \
    bot_reviews p1 p2 local_reviews boundary_updates recorded_at > "${ledger}"
j=$(gh api "${api}")
branch=$(jq -r .head.ref <<< "${j}")
created=$(jq -r .created_at <<< "${j}")
merged=$(jq -r '.merged_at // ""' <<< "${j}")
commits=$(jq -r .commits <<< "${j}")
end=${merged:-$(date -u +%FT%TZ)}
wall=$(jq -rn --arg a "${created}" --arg b "${end}" '(($b | fromdate) - ($a | fromdate)) / 3600' |
    awk '{printf "%.1f", $1}')
bot=$(count "${api}/reviews" '[.[] | select(.user.login=="chatgpt-codex-connector[bot]")] | length')
# The --jq expressions are the input's, byte for byte.
p1=$(count "${api}/comments" '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]") | select(.body | test("P[01] Badge"))] | length')
p2=$(count "${api}/comments" '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]") | select(.body | test("P[23] Badge"))] | length')
local_n=$({ /usr/bin/grep -l -E "^pr: ${pr}\$" .orchestration/validation/*local-review-*.md 2> /dev/null || true; } |
    wc -l | tr -d ' ')
upd=$(count "${api}/commits" '[.[] | select(.commit.message | test("^Merge branch .main. into|^Merge remote-tracking branch"))] | length')
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "${pr}" "${branch}" "${created}" "${merged:-open}" \
    "${wall}" "${commits}" "${bot}" "${p1}" "${p2}" "${local_n}" "${upd}" "$(date -u +%FT%TZ)" >> "${ledger}"
tail -1 "${ledger}"
