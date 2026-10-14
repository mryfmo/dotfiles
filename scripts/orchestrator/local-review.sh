#!/usr/bin/env bash
# @file local-review.sh
# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
# @description
#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and
#   re-reported. Otherwise the clean review worktree (`$ORCH_REVIEW_WORKTREE`, else
#   `.claude/worktrees/orchestrator-review`), a path with its own `.git` entry, is checked out detached at the head
#   and left there, and the review binary (`$CODEX_BIN`, else codex) runs in it as `--profile review -s read-only
#   review --base main`. The file gets the front matter, the unique `- [P0-3]` findings of the transcript's final
#   message, and that message with the worktree prefix stripped; the findings are printed, then `local-review: <n>
#   findings (<file>)`.
# @arg $1 string Task id.
# @arg $2 string The PR head commit, a local one.
# @arg $3 int PR number.
# @exitcode 0 No finding.
# @exitcode 2 A precondition failed: the head is not a local commit, the review worktree is not a worktree root or not
#   clean, or there is no review binary.
# @exitcode 3 One or more findings.
# @example
#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
set -euo pipefail
task=$1 head=$2 pr=$3
R="$(git rev-parse --show-toplevel)"
cd -- "$R"
W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
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
git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
    exit 2
}
# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
[ -e "$W/.git" ] || {
    echo "local-review: $W is not a worktree root"
    exit 2
}
[ -z "$(git -C "$W" status --porcelain)" ] || {
    echo "local-review: $W is not clean"
    exit 2
}
# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
# binary from the PR head.
codex=$(command -v "${CODEX_BIN:-codex}") || {
    echo "local-review: no review binary ${CODEX_BIN:-codex}"
    exit 2
}
[[ $codex == /* ]] || codex=$R/$codex
git -C "$W" checkout -q --detach "$head"
base=$(git -C "$W" merge-base main HEAD)
t0=$(date -u +%FT%TZ)
tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
(cd "$W" && "$codex" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp" | sed "s#$W/##g")
findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
{
    printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
    printf '%s\n\n' "$findings"
    echo '```text'
    printf '%s\n' "$final" | cut -c1-2000
    echo '```'
} > "$out"
rm -f "$tmp"
printf '%s\n' "$findings"
echo "local-review: $n findings ($out)"
[ "$n" = 0 ] || exit 3
