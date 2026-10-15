#!/usr/bin/env bash
# pr-cost.sh <pr>: plan 020 step 0. One ledger line per PR: Bot reviews, Bot threads by priority, local reviews, revises (RESULTs - 1 for the task), resets (task files in the lineage - 1), first push → merge wall. Appends to .orchestration/metrics/pr-cost.tsv (header once). Runs outside the sandbox (gh).
set -euo pipefail
pr=$1
cd "$(git rev-parse --show-toplevel)"
mkdir -p .orchestration/metrics
F=.orchestration/metrics/pr-cost.tsv
[ -s "$F" ] || printf 'pr\tbranch\tcreated\tmerged\twall_h\tcommits\tbot_reviews\tp1\tp2\tlocal_reviews\tboundary_updates\trecorded_at\n' > "$F"
j=$(gh api "repos/mryfmo/dotfiles/pulls/$pr")
branch=$(jq -r .head.ref <<<"$j"); created=$(jq -r .created_at <<<"$j"); merged=$(jq -r '.merged_at // ""' <<<"$j"); commits=$(jq -r .commits <<<"$j")
end=${merged:-$(date -u +%FT%TZ)}
wall=$(uv run --no-project python -c "import sys,datetime as d;a,b=[d.datetime.fromisoformat(x.replace('Z','+00:00')) for x in sys.argv[1:3]];print(round((b-a).total_seconds()/3600,1))" "$created" "$end")
bot=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/reviews" --paginate --jq '[.[] | select(.user.login=="chatgpt-codex-connector[bot]")] | length')
p1=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/comments" --paginate --jq '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]") | select(.body | test("P[01] Badge"))] | length')
p2=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/comments" --paginate --jq '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]") | select(.body | test("P[23] Badge"))] | length')
local_n=$({ /usr/bin/grep -l -E "^pr: $pr\$" .orchestration/validation/*local-review-*.md 2>/dev/null || true; } | wc -l | tr -d " ")
upd=$(gh api "repos/mryfmo/dotfiles/pulls/$pr/commits" --paginate --jq '[.[] | select(.commit.message | test("^Merge branch .main. into|^Merge remote-tracking branch"))] | length')
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$pr" "$branch" "$created" "${merged:-open}" "$wall" "$commits" "$bot" "$p1" "$p2" "$local_n" "$upd" "$(date -u +%FT%TZ)" >> "$F"
tail -1 "$F"
