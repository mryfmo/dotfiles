#!/usr/bin/env bash
# @file worktree-gc.sh
# @brief List, and with --apply remove, the clean agent worktrees under .claude/worktrees/ whose work landed.
# @description
#   Regime-cutover U16. Agent worktrees stay behind under `<checkout>/.claude/worktrees/`
#   after their unit lands, and a `git worktree remove` loop from the coordinator
#   is refused by the auto-mode classifier as irreversible local destruction
#   (measured 2026-10-23). This lever judges each tree from evidence, never from
#   its name. The checkout is the main worktree of the repository the cwd belongs
#   to, the first row of `git worktree list --porcelain`, so the lever runs the
#   same from any of its worktrees. The first matching line decides a tree:
#
#     keep    locked       `git worktree lock`, or an agent session that holds it
#     keep    prunable     git reports the directory gone; `--apply` prunes the entry
#     keep    dirty        `git status --porcelain --untracked-files=all` prints anything
#     remove  reachable    the head is an ancestor of the local `origin/main`
#     remove  pr-merged    a merged pull request's head is the tree's head or a
#                          descendant of it: `gh pr list --state merged --head <branch>
#                          --json number,headRefOid`, or `--search <sha>` for a detached tree
#     keep    not-landed   none of the above
#
#   The dirty check runs before any network call, so a tree with work in it is
#   never a candidate and costs no `gh` round trip. The pull-request check
#   compares commits, not names, so a branch with commits past its merged head is
#   kept. `origin/main` is the local ref; a stale one only keeps more trees, so
#   fetch first when the list looks short. Removal is `git worktree remove <path>`
#   without `--force`, after the whole scan, then one `git worktree prune`; git
#   itself refuses a locked or dirty tree a second time. A positional path narrows
#   the scan and must lie under `.claude/worktrees/`. Every `gh` call is bounded
#   to 60 seconds, and a failed one ends the run before any removal.
# @option --dry-run Print the rows and remove nothing (the default; the flag lets the allow rule match a bare run).
# @option --apply Remove every tree the dry run lists as remove, then prune.
# @arg $@ path Worktree paths to judge (default: every worktree under `<checkout>/.claude/worktrees/`).
# @stdout One row per tree, `<keep|remove><TAB><path><TAB><branch or detached@<sha>><TAB><reason>`; with --apply, `removed<TAB><path>` per removal.
# @exitcode 0 Listed, or every removal succeeded (also when nothing qualifies).
# @exitcode 1 A removal or the prune failed (git's error on stderr).
# @exitcode 2 Usage error, a path outside `.claude/worktrees/`, or a failed `gh` call.
# @example
#   scripts/orchestrator/worktree-gc.sh --dry-run
#   scripts/orchestrator/worktree-gc.sh --apply
set -euo pipefail

usage='usage: worktree-gc.sh [--dry-run|--apply] [<path>...]'
refuse() {
    echo "worktree-gc: $*" >&2
    exit 2
}
bounded() {
    perl -e 'alarm shift; exec @ARGV' 60 "$@"
}

apply=0 wanted=()
while (($#)); do
    case $1 in
    --apply) apply=1 ;;
    --dry-run) apply=0 ;;
    -*) refuse "${usage}" ;;
    *) wanted+=("$(realpath "$1")") ;;
    esac
    shift
done

porcelain=$(git worktree list --porcelain)
root=$(head -n 1 <<< "${porcelain}")
prefix=${root#worktree }/.claude/worktrees
for path in ${wanted[@]+"${wanted[@]}"}; do
    [[ ${path} == "${prefix}"/* ]] || refuse "${path} is outside ${prefix}"
done

removals=()
row() {
    printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4"
    [[ $1 != remove ]] || removals+=("$2")
}
judge() {
    local path=$1 head=$2 branch=$3 flags=$4 where query merged number oid
    where=${branch:-detached@${head:0:12}}
    if [[ ${flags} == *' locked'* ]]; then
        row keep "${path}" "${where}" locked
    elif [[ ${flags} == *' prunable'* ]]; then
        row keep "${path}" "${where}" prunable
    elif [[ -n $(git -C "${path}" status --porcelain --untracked-files=all) ]]; then
        row keep "${path}" "${where}" dirty
    elif git merge-base --is-ancestor "${head}" origin/main 2> /dev/null; then
        row remove "${path}" "${where}" reachable-from-origin/main
    else
        query=(pr list --state merged --json 'number,headRefOid')
        if [[ -n ${branch} ]]; then
            query+=(--head "${branch}")
        else
            query+=(--search "${head}")
        fi
        merged=$(bounded gh "${query[@]}") || refuse "gh ${query[*]} failed for ${path}"
        while IFS=$'\t' read -r number oid; do
            [[ -n ${number} ]] || continue
            if [[ ${oid} == "${head}" ]] || git merge-base --is-ancestor "${head}" "${oid}" 2> /dev/null; then
                row remove "${path}" "${where}" "pr-merged #${number}"
                return
            fi
        done <<< "$(jq -r '.[] | "\(.number)\t\(.headRefOid)"' <<< "${merged}")"
        row keep "${path}" "${where}" not-landed
    fi
}

path='' head='' branch='' flags=''
flush() {
    [[ -z ${path} || ${path} != "${prefix}"/* ]] || judge "${path}" "${head}" "${branch}" "${flags}"
    path='' head='' branch='' flags=''
}
while IFS= read -r line; do
    case ${line} in
    'worktree '*)
        flush
        path=${line#worktree }
        if ((${#wanted[@]})); then
            printf '%s\n' "${wanted[@]}" | grep -qxF -- "${path}" || path=''
        fi
        ;;
    'HEAD '*) head=${line#HEAD } ;;
    'branch refs/heads/'*) branch=${line#branch refs/heads/} ;;
    locked*) flags+=' locked' ;;
    prunable*) flags+=' prunable' ;;
    esac
done <<< "${porcelain}"
flush

((apply)) || exit 0
status=0
for path in ${removals[@]+"${removals[@]}"}; do
    [[ ${path} == "${prefix}"/* ]] || refuse "refusing to remove ${path}: outside ${prefix}"
    if git worktree remove "${path}"; then
        printf 'removed\t%s\n' "${path}"
    else
        status=1
    fi
done
git worktree prune || status=1
exit "${status}"
