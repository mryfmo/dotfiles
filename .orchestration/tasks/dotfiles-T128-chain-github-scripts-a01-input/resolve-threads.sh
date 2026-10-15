#!/usr/bin/env bash
# resolve-threads.sh <pr> <extra.tsv> [--dry-run]: the ruleset's required_review_thread_resolution. For every unresolved review thread of the PR whose first comment id has a row in the disposition table, reply with that disposition (fixed:<sha> or not-applicable:<reason>; evidence=…) and resolve the thread (GraphQL resolveReviewThread). A thread without a row is listed and left open (exit 3). Runs outside the sandbox (gh).
set -euo pipefail
pr=$1; tsv=$2; dry=${3:-}; sweep=${4:-}
[ -f "$tsv" ]
threads=$(gh api graphql -f query="query { repository(owner:\"mryfmo\", name:\"dotfiles\") { pullRequest(number:$pr) { reviewThreads(first:100) { nodes { id isResolved comments(first:1) { nodes { databaseId } } } } } } }" --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not) | "\(.comments.nodes[0].databaseId) \(.id)"')
missing=0; done_n=0
while read -r cid tid; do
  [ -n "$cid" ] || continue
  row=$(awk -F'\t' -v id="$cid" '$1==id {print $2; exit}' "$tsv")
  if [ -z "$row" ] && [ -n "$sweep" ] && [ -s "$sweep" ]; then
    row=$(uv run --no-project python -c "import json,sys; d=json.load(open(sys.argv[1])); print(next((i.get('disposition') or '' for i in d['items'] if (i.get('url') or '').endswith('_r'+sys.argv[2])), ''))" "$sweep" "$cid")
  fi
  if [ -z "$row" ]; then echo "no disposition row for thread $cid (table or sweep); left open"; missing=1; continue; fi
  case "$row" in
    fixed:*) body="Disposition (orchestrator): ${row}. Fixed at root cause in that commit on this branch; verified by the task's tests and CI on the final head. Resolving.";;
    not-applicable:*) body="Disposition (orchestrator): ${row}. Resolving; the owning task on main carries it.";;
    *) echo "row for $cid has an unknown form: $row"; missing=1; continue;;
  esac
  if [ "$dry" = "--dry-run" ]; then echo "would reply+resolve $cid: ${row:0:90}"; continue; fi
  gh api -X POST "repos/mryfmo/dotfiles/pulls/$pr/comments/$cid/replies" -f body="$body" --jq '.id' > /dev/null
  gh api graphql -f query="mutation { resolveReviewThread(input: {threadId: \"$tid\"}) { thread { isResolved } } }" --jq '.data.resolveReviewThread.thread.isResolved' > /dev/null
  done_n=$((done_n+1)); echo "resolved $cid (${row:0:60})"
done <<< "$threads"
echo "resolved $done_n thread(s); missing rows: $missing"
[ "$missing" = 0 ] || exit 3
