#!/usr/bin/env bash
# local-review.sh <task> <head> <pr>: C-32. Review a PR head's diff against main with the Bot's engine, locally, before the audit.
# Run OUTSIDE the Bash sandbox (inside it codex exits 1: "failed to initialize in-process app-server client: Operation not permitted").
# Writes .orchestration/validation/<task>-local-review-<sha7>.md (findings, then the transcript's final message with the worktree prefix stripped),
# prints one line per unique finding and "local-review: <n> findings" last; exit 0 when n=0, 3 when n>0, 2 on a precondition.
set -euo pipefail
task=$1 head=$2 pr=$3
R="$(git rev-parse --show-toplevel)"
W=$R/.claude/worktrees/orchestrator-review
out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
if [ -s "$out" ]; then
    # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again
    findings=$(/usr/bin/grep -E '^- \[P[0-3]\]' "$out" | sort -u || true)
    n=$(sed -n 's/^findings: //p' "$out" | head -1)
    printf '%s\n' "$findings"
    echo "local-review: $n findings (existing $out)"
    [ "${n:-0}" = 0 ] || exit 3
    exit 0
fi
git -C "$R" cat-file -e "$head^{commit}" 2>/dev/null || { echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"; exit 2; }
[ -z "$(git -C "$W" status --porcelain)" ] || { echo "local-review: $W is not clean"; exit 2; }
git -C "$W" checkout -q --detach "$head"
base=$(git -C "$W" merge-base main HEAD)
t0=$(date -u +%FT%TZ)
tmp=$(mktemp)
(cd "$W" && codex --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp" | sed "s#$W/##g")
findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
{
    printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
    printf '%s\n\n' "$findings"
    echo '```text'; printf '%s\n' "$final" | cut -c1-2000; echo '```'
} > "$out"
rm -f "$tmp"
printf '%s\n' "$findings"
echo "local-review: $n findings ($out)"
[ "$n" = 0 ] || exit 3
