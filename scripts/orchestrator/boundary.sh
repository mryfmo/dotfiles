#!/usr/bin/env bash
# @file boundary.sh
# @brief Commit the main checkout's changed .orchestration files as one boundary PR and queue its auto-merge.
# @description
#   Plan 007 T718 (C-13). Lists the changed files with `git status --porcelain
#   -z --no-renames --untracked-files=all -- .orchestration` in the checkout this
#   script lives in, copies the present ones into a new worktree of `origin/main`
#   under `$TMPDIR` on the branch `orchestration/boundary-<date-suffix>` and
#   deletes the missing ones there with `git rm` (a rename is its old path's
#   deletion and its new path's copy), masks the copies with the
#   repository's masker, runs `make validate-agent-assets`, commits with the
#   message file, pushes to `origin` over HTTPS with the gh credential helper,
#   opens the PR and queues `gh pr merge --squash --auto`. Each step is one
#   command under `set -e`, so a failing masker or validator stops before the
#   commit; the worktree is then left for inspection. The worktree is removed
#   with `git worktree remove` after the PR is queued; nothing is removed with
#   `rm`.
# @arg $1 string Date suffix of the branch, `YYYY-MM-DD-<n>`.
# @arg $2 path Commit message file; its first line is the PR title, the whole file its body.
# @exitcode 0 The PR is open and its auto-merge queued.
# @exitcode 1 No .orchestration change, or a step failed (nothing is committed before the validator passes).
# @exitcode 2 Usage error.
# @example
#   scripts/orchestrator/boundary.sh 2026-10-13-11 "$TMPDIR/boundary-11.txt"
set -euo pipefail

if (($# != 2)) || [[ ! $1 =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]+$ || ! -f $2 ]]; then
    echo "usage: boundary.sh <YYYY-MM-DD-n> <commit-message-file>" >&2
    exit 2
fi
branch="orchestration/boundary-$1"
message="$(cd -- "$(dirname -- "$2")" && pwd -P)/${2##*/}"
root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd -- "${root}"
git fetch -q origin main
files="$(git status --porcelain -z --no-renames --untracked-files=all -- .orchestration | tr '\0' '\n' | cut -c4- | LC_ALL=C sort -u)"
if [[ -z ${files} ]]; then
    echo "boundary: no .orchestration change to commit" >&2
    exit 1
fi
tree="$(mktemp -d "${TMPDIR:-/tmp}/boundary-$1.XXXXXX")/tree"
git worktree add -q --no-track -b "${branch}" "${tree}" origin/main
copied=()
while IFS= read -r f; do
    if [[ -e ${f} || -L ${f} ]]; then
        mkdir -p "${tree}/$(dirname -- "${f}")"
        cp -- "${f}" "${tree}/${f}"
        copied+=("${f}")
    else
        git -C "${tree}" rm -q --ignore-unmatch -- "${f}"
    fi
done <<< "${files}"
cd -- "${tree}"
if ((${#copied[@]} > 0)); then
    uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets "${copied[@]}"
fi
make validate-agent-assets
git add -A .orchestration
git -c commit.gpgsign=false commit -q -F "${message}"
echo "boundary: ${branch} $(git rev-parse --short HEAD), $(wc -l <<< "${files}" | tr -d ' ') files"
GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -q origin "${branch}"
gh pr create --base main --head "${branch}" --title "$(head -n 1 -- "${message}")" --body-file "${message}"
gh pr merge "${branch}" --squash --auto
cd -- "${root}"
git worktree remove "${tree}"
rmdir -- "$(dirname -- "${tree}")"
