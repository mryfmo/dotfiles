#!/usr/bin/env bash
# @file worktree-gc.sh
# @brief List, and with --apply remove, the clean agent worktrees under .claude/worktrees/ whose work landed.
# @description
#   Regime-cutover U16, a coordinator lever pre-authorized by
#   `Bash(scripts/orchestrator/worktree-gc.sh *)` (scripts/orchestrator/README.md,
#   "Pre-authorized levers"). The candidates are the worktrees of this checkout
#   (`git worktree list --porcelain -z`) under `<toplevel>/.claude/worktrees/`;
#   every other worktree, the main one and the omp seats included, is never
#   listed. A candidate qualifies when its tree is clean (`git status --porcelain
#   --untracked-files=all` prints nothing) and its work landed, the first of:
#   its head is reachable from `origin/main` (`git merge-base --is-ancestor`), its
#   branch has a merged pull request (`gh pr list --state merged --head <branch>
#   --json number --limit 1`), or, detached, its head is the head commit of a
#   merged pull request (`gh pr list --state merged --search <sha> --json
#   number,headRefOid`, then `headRefOid == <sha>`). A locked or missing worktree
#   is kept. The listing is read field by field on its NUL separators, so a path
#   cannot forge a record; a candidate whose path contains a newline is an
#   `error` row. Each candidate prints one row `<verdict>\t<path>\t<ref>\t<reason>`
#   (a newline in the path printed as `\n`), verdict `gc` (qualifies), `keep` or
#   `error`, then one `summary` row. Nothing
#   is removed without `--apply`; with it each qualifying path is removed with
#   `git worktree remove <path>`, never forced, so git itself still refuses a
#   tree that changed since the check, then `git worktree prune` runs, and each
#   step prints a `removed`, `failed` or `pruned` row. A `gh` error fails closed:
#   the run removes nothing and exits 1. `origin/main` is read as it is; run
#   `git fetch origin` first for a current answer. Every `gh` call is bounded by
#   WORKTREE_GC_GH_TIMEOUT seconds (perl `alarm`, because `timeout` is not on
#   every host). A path argument narrows the run to those worktrees and is
#   refused unless it is one of them.
# @arg $@ path Optional worktree paths under .claude/worktrees/; default: all of them.
# @option --apply Remove the qualifying worktrees (default: list only).
# @env WORKTREE_GC_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One TSV row per candidate, the removal rows with --apply, then `summary`.
# @exitcode 0 Listed (and removed with --apply), including when nothing qualifies.
# @exitcode 1 A git or gh query failed, a path holds a newline, or a removal failed.
# @exitcode 2 Usage error, not in a git checkout, or a path outside .claude/worktrees/.
# @example
#   scripts/orchestrator/worktree-gc.sh
#   scripts/orchestrator/worktree-gc.sh --apply
set -euo pipefail

# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
lever_self_check() {
    local dir self name pin digest home
    dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P) || {
        echo "${0##*/}: refused: cannot resolve the script directory" >&2
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

usage='usage: worktree-gc.sh [--apply] [<path>...]'
apply=0
paths=()
while (($#)); do
    case $1 in
    --apply) apply=1 ;;
    --) ;;
    -*)
        echo "${usage}" >&2
        exit 2
        ;;
    *) paths+=("$1") ;;
    esac
    shift
done
gh_timeout=${WORKTREE_GC_GH_TIMEOUT:-60}
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || {
    echo 'worktree-gc: WORKTREE_GC_GH_TIMEOUT must be a positive integer' >&2
    exit 2
}

toplevel=$(git rev-parse --show-toplevel 2> /dev/null) || {
    echo 'worktree-gc: not in a git checkout' >&2
    exit 2
}
toplevel=$(cd "${toplevel}" && pwd -P)
base=${toplevel}/.claude/worktrees
git -C "${toplevel}" rev-parse --verify --quiet 'origin/main^{commit}' > /dev/null || {
    echo 'worktree-gc: origin/main is absent; run git fetch origin' >&2
    exit 1
}

# @description Print the physical form of a path, or the path itself when it no longer exists.
# @arg $1 path A path.
physical() {
    if [[ -d $1 ]]; then (cd "$1" && pwd -P); else printf '%s\n' "$1"; fi
}

# @description Succeed when a physical path lies strictly under .claude/worktrees/ of this checkout.
# @arg $1 path A physical path.
under_base() {
    [[ $1 == "${base}/"?* ]]
}

# @description Run gh in the checkout, killed after WORKTREE_GC_GH_TIMEOUT seconds.
# @arg $@ string gh arguments.
bounded_gh() {
    (cd "${toplevel}" && perl -e 'alarm shift; exec @ARGV or die "exec gh: $!\n"' "${gh_timeout}" gh "$@")
}

selected=()
for path in "${paths[@]+"${paths[@]}"}"; do
    resolved=$(physical "${path}")
    under_base "${resolved}" || {
        echo "worktree-gc: refused: ${path} is outside ${base}/" >&2
        exit 2
    }
    selected+=("${resolved}")
done

# Candidates as parallel arrays: path, head, branch (empty when detached), state (`locked`, `missing`, `newline` or empty).
cand_path=() cand_head=() cand_branch=() cand_state=()
record() {
    [[ -n ${wt_path} ]] || return 0
    local resolved
    resolved=$(physical "${wt_path}")
    under_base "${resolved}" || return 0
    if ((${#selected[@]})); then
        local wanted='' item
        for item in "${selected[@]}"; do [[ ${item} == "${resolved}" ]] && wanted=1; done
        [[ -n ${wanted} ]] || return 0
    fi
    cand_path+=("${resolved}") cand_head+=("${wt_head}") cand_branch+=("${wt_branch}")
    if [[ ${wt_path} == *$'\n'* ]]; then cand_state+=(newline); else cand_state+=("${wt_state}"); fi # lint-comparisons: allow a newline-content test, not a path comparison
}
# The producer writes to a file, not a pipe or a process substitution, so its exit status is checked; the NUL-separated
# fields are read as they are (`read -d ''`), never turned into lines, so a newline inside a path stays in its field.
listing=$(mktemp "${TMPDIR:-/tmp}/worktree-gc.XXXXXX")
trap 'rm -f "${listing}"' EXIT
git -C "${toplevel}" worktree list --porcelain -z > "${listing}" || {
    echo 'worktree-gc: git worktree list failed' >&2
    exit 1
}
wt_path='' wt_head='' wt_branch='' wt_state=''
while IFS= read -r -d '' field; do
    case ${field} in
    'worktree '*)
        record
        wt_path=${field#worktree } wt_head='' wt_branch='' wt_state=''
        ;;
    'HEAD '*) wt_head=${field#HEAD } ;;
    'branch refs/heads/'*) wt_branch=${field#branch refs/heads/} ;;
    locked | 'locked '*) wt_state=locked ;;
    prunable | 'prunable '*) [[ -n ${wt_state} ]] || wt_state=missing ;;
    esac
done < "${listing}"
record

for path in "${selected[@]+"${selected[@]}"}"; do
    found=''
    for item in "${cand_path[@]+"${cand_path[@]}"}"; do [[ ${item} == "${path}" ]] && found=1; done # lint-comparisons: allow both operands are pwd -P forms from physical()
    [[ -n ${found} ]] || {
        echo "worktree-gc: refused: ${path} is not a worktree of ${toplevel}" >&2
        exit 2
    }
done

# @description Set `verdict` and `reason` for one candidate.
# @arg $1 path The worktree.
# @arg $2 string Its head sha.
# @arg $3 string Its branch, empty when detached.
# @arg $4 string Its state: `locked`, `missing`, `newline` or empty.
classify() {
    local path=$1 head=$2 branch=$3 state=$4 status prs number
    verdict=keep
    if [[ ${state} == newline ]]; then
        verdict=error reason='path contains a newline'
        return
    fi
    if [[ ${state} == locked ]]; then
        reason='locked'
        return
    fi
    if [[ ${state} == missing || ! -d ${path} ]]; then
        reason='missing (git worktree prune clears it)'
        return
    fi
    if ! status=$(git -C "${path}" status --porcelain --untracked-files=all); then
        verdict=error reason='git status failed'
        return
    fi
    if [[ -n ${status} ]]; then
        reason='dirty or untracked files'
        return
    fi
    if [[ ! ${head} =~ ^[0-9a-f]{40}([0-9a-f]{24})?$ ]]; then
        verdict=error reason="unreadable head '${head}'"
        return
    fi
    if git -C "${toplevel}" merge-base --is-ancestor "${head}" origin/main 2> /dev/null; then
        verdict=gc reason="head ${head:0:12} is in origin/main"
        return
    fi
    if [[ -n ${branch} ]]; then
        if ! prs=$(bounded_gh pr list --state merged --head "${branch}" --json number --limit 1) ||
            ! number=$(jq -r '.[0].number // empty' <<< "${prs}"); then
            verdict=error reason="gh pr list --head ${branch} failed"
            return
        fi
        if [[ -n ${number} ]]; then
            verdict=gc reason="branch PR #${number} merged"
        else
            reason='no merged PR for the branch'
        fi
        return
    fi
    if ! prs=$(bounded_gh pr list --state merged --search "${head}" --json number,headRefOid) ||
        ! number=$(jq -r --arg sha "${head}" 'map(select(.headRefOid == $sha))[0].number // empty' <<< "${prs}"); then
        verdict=error reason="gh pr list --search ${head:0:12} failed"
        return
    fi
    if [[ -n ${number} ]]; then
        verdict=gc reason="detached at the head of merged PR #${number}"
    else
        reason='detached at no merged PR head'
    fi
}

gc=() errors=0 kept=0
for ((i = 0; i < ${#cand_path[@]}; i++)); do
    classify "${cand_path[i]}" "${cand_head[i]}" "${cand_branch[i]}" "${cand_state[i]}"
    shown=${cand_path[i]//$'\n'/\\n}
    printf '%s\t%s\t%s\t%s\n' "${verdict}" "${shown}" "${cand_branch[i]:-(detached ${cand_head[i]:0:12})}" "${reason}"
    case ${verdict} in
    gc) gc+=("${cand_path[i]}") ;;
    error) errors=$((errors + 1)) ;;
    *) kept=$((kept + 1)) ;;
    esac
done

if ((errors)); then
    printf 'summary\t%d qualify, %d kept, %d errors; nothing removed\n' "${#gc[@]}" "${kept}" "${errors}"
    exit 1
fi
if ((! apply)); then
    printf 'summary\t%d qualify, %d kept; dry run, rerun with --apply to remove\n' "${#gc[@]}" "${kept}"
    exit 0
fi

removed=0 failed=0
for path in "${gc[@]+"${gc[@]}"}"; do
    under_base "${path}" || {
        echo "worktree-gc: refused: ${path} is outside ${base}/" >&2
        exit 2
    }
    if git -C "${toplevel}" worktree remove "${path}"; then
        printf 'removed\t%s\n' "${path}"
        removed=$((removed + 1))
    else
        printf 'failed\t%s\tgit worktree remove refused\n' "${path}"
        failed=$((failed + 1))
    fi
done
git -C "${toplevel}" worktree prune
printf 'pruned\tgit worktree prune\n'
printf 'summary\t%d removed, %d failed, %d kept\n' "${removed}" "${failed}" "${kept}"
((! failed)) || exit 1
