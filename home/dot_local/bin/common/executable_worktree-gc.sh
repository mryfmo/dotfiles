#!/usr/bin/env bash
# @file worktree-gc.sh
# @brief List the clean agent worktrees under .claude/worktrees/ whose work landed; quarantine them with --apply, delete old quarantined ones with --purge.
# @description
#   Regime-cutover U16, a coordinator lever pre-authorized by
#   `Bash(scripts/orchestrator/worktree-gc.sh *)` (scripts/orchestrator/README.md,
#   "Pre-authorized levers"). The candidates are the worktrees of this checkout
#   (`git worktree list --porcelain -z`) under `<toplevel>/.claude/worktrees/`,
#   except the quarantine `<toplevel>/.claude/worktrees/.gc-quarantine/`; every
#   other worktree, the main one and the omp seats included, is never listed.
#   A candidate qualifies when its tree is clean (`git status --porcelain
#   --ignored=matching --untracked-files=all` prints nothing: `git worktree
#   remove` deletes ignored files without asking, so a tree holding one, an
#   `.env` say, is kept; and no index entry carries the `assume-unchanged` or
#   `skip-worktree` flag, `git ls-files -v` tag lowercase or `S`, since an edit
#   to such a file is invisible to `git status` and to the removal's own check)
#   and its work landed, the first of: its head is
#   reachable from `origin/main` (`git merge-base --is-ancestor`); it landed by
#   content (every path `git diff --no-renames --name-only -z <merge-base>
#   <head>` names holds in `origin/main` the entry it holds in the head, mode
#   and object, or is absent from both: the case of a squash merge with no
#   later commit; no merge runs, so no configured merge driver or `merge=`
#   attribute can answer, and a git failure is an `error` row); or its head is
#   the `headRefOid` of a merged pull request of this repository (`gh pr list
#   --state merged --head <branch> --json number,headRefOid --limit 100`,
#   detached `--search <sha>`). A branch name
#   alone never counts: a commit pushed after a squash merge is not in main,
#   and `--head` also matches a fork's branch of the same name. A locked or
#   missing worktree is kept. The listing is read field by field on its NUL
#   separators, so a path cannot forge a record; a candidate whose path
#   contains a newline is an `error` row. Each candidate prints one row
#   `<verdict>\t<path>\t<ref>\t<reason>` (a newline in the path printed as
#   `\n`), verdict `gc` (qualifies), `keep` or `error`, then each quarantined
#   worktree a `quarantine` row with its age, then one `summary` row.
#
#   No check can be made atomic with a deletion, so taking a tree out of use
#   and deleting it are two runs. `--apply` deletes nothing: it renames each
#   qualifying tree with `git worktree move <path>
#   .gc-quarantine/<random>/<name>` (one rename on the same filesystem; git
#   refuses a locked tree), writes `<epoch> <classified head>` to
#   `gc-quarantined-at` in the tree's admin directory (`git rev-parse
#   --absolute-git-dir`, refused unless a plain directory directly under
#   `<common dir>/worktrees/`; the marker goes to a `mktemp` file there,
#   renamed onto its name, so a symlink planted at the name is replaced, never
#   written through), then checks the moved tree clean again (index flags
#   included) and its HEAD equal to the classified one. Both hold: a
#   `quarantined` row. Either fails (a file or commit made after the
#   classification moved with the tree), or the marker cannot be written: a
#   `held` row with the reason; the tree stays in the quarantine, is never
#   moved back and never deleted by this run. A refused move is a `failed`
#   row, exit 1. `--purge <days>` lists only the quarantine: each entry whose
#   marker is at least <days> days old (0: any age) is classified again by the
#   same rules (clean, ignored files included; HEAD read again and landed by
#   ancestry, content or a merged PR's exact head) and then removed with `git
#   worktree remove <path>`; an entry without a marker, younger, locked, or
#   no longer qualifying is kept, a refused removal is a `failed` row, exit 1.
#   Residual: purge, too, cannot check and remove atomically, so a file
#   written into the quarantined tree between its re-check and the removal is
#   lost; nothing has the quarantine path as its own, so that takes a process
#   still writing through its old working directory into the renamed tree
#   <days> days after the move. Nothing ever passes `--force`, and branch refs
#   stay. `git worktree prune` is never run: it would drop the admin data of
#   every worktree whose directory is missing, an unlocked omp seat included.
#   A `gh` error fails closed: the run moves and removes nothing and exits 1.
#   `origin/main` is read as it is; run `git fetch origin` first for a current
#   answer. Every `gh` call is bounded by WORKTREE_GC_GH_TIMEOUT seconds (perl
#   `alarm`, because `timeout` is not on every host). A path argument narrows
#   the listing and `--apply` to those worktrees and is refused unless it is
#   one of the candidates; `--purge` takes none.
# @arg $@ path Optional worktree paths under .claude/worktrees/ (not in the quarantine); default: all of them.
# @option --apply Move the qualifying worktrees into the quarantine (default: list only).
# @option --purge <days> Remove the quarantined worktrees quarantined at least <days> days ago that still qualify.
# @env WORKTREE_GC_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One TSV row per candidate and quarantined worktree, the move or removal rows, then `summary`.
# @exitcode 0 Listed (and quarantined or purged), including when nothing qualifies or a moved tree is held.
# @exitcode 1 A git or gh query failed, a path holds a newline, or a move or removal failed.
# @exitcode 2 Usage error, not in a git checkout, a path outside .claude/worktrees/ or in the quarantine, or a quarantine that is a symlink.
# @example
#   scripts/orchestrator/worktree-gc.sh
#   scripts/orchestrator/worktree-gc.sh --apply
#   scripts/orchestrator/worktree-gc.sh --purge 7
set -euo pipefail

# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
lever_self_check() {
    local src dir self name pin digest home
    # The directory is split from the path in the shell, so no external producer (dirname) can fail unseen.
    src=${BASH_SOURCE[0]}
    case ${src} in
    */*) dir=${src%/*} ;;
    *) dir=. ;;
    esac
    [[ -n ${dir} ]] || dir=/
    dir=$(cd "${dir}" && pwd -P) || {
        echo "${src##*/}: refused: cannot resolve the script directory of ${src}" >&2
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

usage='usage: worktree-gc.sh [--apply] [<path>...] | --purge <days>'
apply=0 purge=''
paths=()
while (($#)); do
    case $1 in
    --apply) apply=1 ;;
    --purge)
        if (($# < 2)) || [[ ! $2 =~ ^(0|[1-9][0-9]{0,4})$ ]]; then
            echo "${usage}" >&2
            exit 2
        fi
        purge=$2
        shift
        ;;
    --) ;;
    -*)
        echo "${usage}" >&2
        exit 2
        ;;
    *) paths+=("$1") ;;
    esac
    shift
done
if [[ -n ${purge} ]] && ((apply || ${#paths[@]})); then
    echo "${usage}" >&2
    exit 2
fi
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
quarantine=${base}/.gc-quarantine
if ! common_dir=$(git -C "${toplevel}" rev-parse --path-format=absolute --git-common-dir) ||
    ! common_dir=$(cd "${common_dir}" && pwd -P); then
    echo 'worktree-gc: cannot resolve the git common directory' >&2
    exit 1
fi
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
    [[ $1 == "${base}/"?* ]] # lint-comparisons: allow both sides are pwd -P forms
}

# @description Succeed when a physical path is the quarantine or lies under it.
# @arg $1 path A physical path.
in_quarantine() {
    [[ $1 == "${quarantine}" || $1 == "${quarantine}/"* ]] # lint-comparisons: allow both sides are pwd -P forms
}

# @description Print the admin directory of a worktree, refusing one outside `<common dir>/worktrees/`.
# @arg $1 path The worktree.
# @exitcode 1 git failed or the admin directory is elsewhere.
admin_dir() {
    local raw dir
    raw=$(git -C "$1" rev-parse --absolute-git-dir) && [[ ! -L ${raw} ]] && dir=$(cd "${raw}" && pwd -P) || return 1
    [[ ${dir} == "${common_dir}/worktrees/"?* && ${dir} != "${common_dir}/worktrees/"*/* ]] || return 1 # lint-comparisons: allow both sides are pwd -P forms
    printf '%s\n' "${dir}"
}

# @description Write the quarantine marker into an admin directory without following a link at its name: the content
#   goes to a fresh `mktemp` file beside it, which is renamed onto the name (a rename replaces a symlink there). A
#   directory at the name, or one a symlink there points at, is refused, since `mv` would move the file into it.
# @arg $1 path The admin directory, from admin_dir.
# @arg $2 string The marker line.
# @exitcode 1 The marker was not written.
write_marker() {
    local tmp
    [[ ! -d $1/${marker} ]] || return 1
    tmp=$(mktemp "$1/${marker}.XXXXXX") || return 1
    if printf '%s\n' "$2" > "${tmp}" && mv -f "${tmp}" "$1/${marker}"; then return 0; fi
    rm -f "${tmp}"
    return 1
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
    ! in_quarantine "${resolved}" || {
        echo "worktree-gc: refused: ${path} is in the quarantine ${quarantine}/; --purge handles it" >&2
        exit 2
    }
    selected+=("${resolved}")
done

# Candidates and quarantined worktrees as parallel arrays: path, head, branch (empty when detached), state (`locked`,
# `missing`, `newline` or empty).
cand_path=() cand_head=() cand_branch=() cand_state=()
q_path=() q_head=() q_branch=() q_state=()
record() {
    [[ -n ${wt_path} ]] || return 0
    local resolved state=${wt_state}
    resolved=$(physical "${wt_path}")
    under_base "${resolved}" || return 0
    if [[ ${wt_path} == *$'\n'* ]]; then state=newline; fi # lint-comparisons: allow a newline-content test, not a path comparison
    if in_quarantine "${resolved}"; then
        ((${#selected[@]})) && return 0
        q_path+=("${resolved}") q_head+=("${wt_head}") q_branch+=("${wt_branch}") q_state+=("${state}")
        return 0
    fi
    if ((${#selected[@]})); then
        local wanted='' item
        for item in "${selected[@]}"; do [[ ${item} == "${resolved}" ]] && wanted=1; done # lint-comparisons: allow both operands are pwd -P forms from physical()
        [[ -n ${wanted} ]] || return 0
    fi
    cand_path+=("${resolved}") cand_head+=("${wt_head}") cand_branch+=("${wt_branch}") cand_state+=("${state}")
}
# The producer writes to a file, not a pipe or a process substitution, so its exit status is checked; the NUL-separated
# fields are read as they are (`read -d ''`), never turned into lines, so a newline inside a path stays in its field.
listing=$(mktemp "${TMPDIR:-/tmp}/worktree-gc.XXXXXX")
changed=$(mktemp "${TMPDIR:-/tmp}/worktree-gc.XXXXXX")
entries=$(mktemp "${TMPDIR:-/tmp}/worktree-gc.XXXXXX")
trap 'rm -f "${listing}" "${changed}" "${entries}"' EXIT
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

# @description Succeed when the head landed in origin/main by content: every path `git diff` names between the merge
#   base and the head holds in origin/main the `git ls-tree -r` entry (mode, type, object) it holds in the head, or is
#   absent from both. Nothing here merges, so no merge driver, `merge=` attribute or `merge.*` setting takes part; the
#   diff is name-only and NUL-separated, renames off and submodules shown, and every pathspec literal.
# @arg $1 string The head sha.
# @exitcode 0 Landed by content (an empty change set included).
# @exitcode 1 Not landed, or the head shares no history with origin/main.
# @exitcode 2 A git call failed.
landed_by_content() {
    local head=$1 mb rc field in_head in_main
    local -a changed_paths=()
    mb=$(git -C "${toplevel}" merge-base origin/main "${head}") && rc=0 || rc=$?
    ((rc != 1)) || return 1
    if ((rc)) || [[ ! ${mb} =~ ^[0-9a-f]{40}([0-9a-f]{24})?$ ]]; then return 2; fi
    git -C "${toplevel}" diff --no-renames --no-relative --no-ext-diff --no-textconv --no-color \
        --ignore-submodules=none --name-only -z "${mb}" "${head}" -- > "${changed}" || return 2
    while IFS= read -r -d '' field; do changed_paths+=("${field}"); done < "${changed}"
    ((${#changed_paths[@]})) || return 0
    # Without -z the quoted listing has one line per entry, so it survives a command substitution; both sides are quoted alike.
    in_head=$(git -C "${toplevel}" -c core.quotePath=true --literal-pathspecs ls-tree -r --full-tree "${head}" \
        -- "${changed_paths[@]}") || return 2
    in_main=$(git -C "${toplevel}" -c core.quotePath=true --literal-pathspecs ls-tree -r --full-tree origin/main \
        -- "${changed_paths[@]}") || return 2
    [[ ${in_head} == "${in_main}" ]] || return 1
}

# @description Set `status` to the `git status --porcelain --ignored=matching --untracked-files=all` of a worktree,
#   and `flagged` to the number of its index entries marked `assume-unchanged` (`git ls-files -v` tag lowercase) or
#   `skip-worktree` (tag `S`), whose edits neither `git status` nor `git worktree remove` sees.
# @arg $1 path The worktree.
# @exitcode 1 git status or git ls-files failed.
tree_status() {
    local entry
    flagged=0
    status=$(git -C "$1" status --porcelain --ignored=matching --untracked-files=all) || return 1
    git -C "$1" ls-files -v -z > "${entries}" || return 1
    while IFS= read -r -d '' entry; do
        if [[ ${entry} == [[:lower:]S]' '* ]]; then flagged=$((flagged + 1)); fi
    done < "${entries}"
}

# @description Set `verdict` and `reason` for one candidate.
# @arg $1 path The worktree.
# @arg $2 string Its head sha.
# @arg $3 string Its branch, empty when detached.
# @arg $4 string Its state: `locked`, `missing`, `newline` or empty.
classify() {
    local path=$1 head=$2 branch=$3 state=$4 rc query prs number
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
        reason='missing (its admin data is left for the operator)'
        return
    fi
    if ! tree_status "${path}"; then
        verdict=error reason='git status failed'
        return
    fi
    if [[ -n ${status} ]] && grep -qv '^!! ' <<< "${status}"; then
        reason='dirty or untracked files'
        return
    fi
    if ((flagged)); then
        reason="${flagged} index entries marked assume-unchanged or skip-worktree (git status cannot see their edits)"
        return
    fi
    if [[ -n ${status} ]]; then
        reason='ignored files (git worktree remove would delete them)'
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
    landed_by_content "${head}" && rc=0 || rc=$?
    if ((rc > 1)); then
        verdict=error reason="comparing head ${head:0:12} with origin/main failed"
        return
    fi
    if ((rc == 0)); then
        verdict=gc reason="every path head ${head:0:12} changed holds the same entry in origin/main"
        return
    fi
    if [[ -n ${branch} ]]; then
        query=(--head "${branch}" --json 'number,headRefOid' --limit 100)
    else
        query=(--search "${head}" --json 'number,headRefOid')
    fi
    if ! prs=$(bounded_gh pr list --state merged "${query[@]}") ||
        ! number=$(jq -r --arg sha "${head}" 'map(select(.headRefOid == $sha))[0].number // empty' <<< "${prs}"); then
        verdict=error reason="gh pr list ${query[0]} ${query[1]:0:12} failed"
        return
    fi
    if [[ -n ${number} ]]; then
        verdict=gc reason="head ${head:0:12} is the head of merged PR #${number}"
    else
        reason="head ${head:0:12} is neither in origin/main nor the head of a merged PR"
    fi
}

marker='gc-quarantined-at'
now=$(date +%s)

# @description Set `quarantined_at` to the epoch the quarantine marker of a worktree records, empty without a readable one.
# @arg $1 path The quarantined worktree.
read_marker() {
    local dir line=''
    quarantined_at=''
    dir=$(admin_dir "$1") || return 0
    [[ -f ${dir}/${marker} && ! -L ${dir}/${marker} ]] || return 0
    IFS= read -r line < "${dir}/${marker}" || [[ -n ${line} ]] || return 0
    if [[ ${line} =~ ^([0-9]{1,12})\ [0-9a-f]{40}([0-9a-f]{24})?$ ]]; then quarantined_at=${BASH_REMATCH[1]}; fi
}

# @description Print an age in seconds as `<d>d <h>h`.
# @arg $1 number Seconds.
age() {
    printf '%dd %dh' $(($1 / 86400)) $(($1 % 86400 / 3600))
}

if [[ -n ${purge} ]]; then
    doomed=() errors=0 kept=0
    for ((i = 0; i < ${#q_path[@]}; i++)); do
        path=${q_path[i]} state=${q_state[i]} verdict=keep
        if [[ ${state} == newline ]]; then
            verdict=error reason='path contains a newline'
        elif [[ ${state} == locked ]]; then
            reason='locked'
        elif [[ ${state} == missing || ! -d ${path} ]]; then
            reason='missing (its admin data is left for the operator)'
        else
            read_marker "${path}"
            if [[ -z ${quarantined_at} ]]; then
                reason="no ${marker} marker in its admin directory"
            elif ((now - quarantined_at < purge * 86400)); then
                reason="quarantined $(age $((now - quarantined_at))) ago, younger than ${purge} days"
            elif ! head=$(git -C "${path}" rev-parse --verify --quiet 'HEAD^{commit}'); then
                verdict=error reason='cannot read HEAD'
            elif [[ ${head} != "${q_head[i]}" ]]; then
                reason="head moved to ${head:0:12} during the run"
            else
                # The same rules as a candidate's: clean (ignored files included) and landed by ancestry, content or a
                # merged PR's exact head.
                classify "${path}" "${head}" "${q_branch[i]}" "${state}"
            fi
        fi
        printf '%s\t%s\t%s\t%s\n' "${verdict}" "${path//$'\n'/\\n}" "${q_branch[i]:-(detached ${q_head[i]:0:12})}" "${reason}"
        case ${verdict} in
        gc) doomed+=("${path}") ;;
        error) errors=$((errors + 1)) ;;
        *) kept=$((kept + 1)) ;;
        esac
    done
    if ((errors)); then
        printf 'summary\t%d qualify, %d kept, %d errors; nothing removed\n' "${#doomed[@]}" "${kept}" "${errors}"
        exit 1
    fi
    removed=0 failed=0
    for path in "${doomed[@]+"${doomed[@]}"}"; do
        in_quarantine "${path}" || {
            echo "worktree-gc: refused: ${path} is outside ${quarantine}/" >&2
            exit 2
        }
        # Residual: no check is atomic with the removal; the tree has sat renamed for at least the purge age.
        if git -C "${toplevel}" worktree remove "${path}"; then
            printf 'removed\t%s\n' "${path}"
            removed=$((removed + 1))
            slot=${path%/*}
            if [[ ${slot} != "${quarantine}" ]] && in_quarantine "${slot}"; then rmdir "${slot}" 2> /dev/null || true; fi # lint-comparisons: allow both sides are pwd -P forms
        else
            printf 'failed\t%s\tgit worktree remove refused\n' "${path}"
            failed=$((failed + 1))
        fi
    done
    printf 'summary\t%d removed, %d failed, %d kept\n' "${removed}" "${failed}" "${kept}"
    ((! failed)) || exit 1
    exit 0
fi

gc=() errors=0 kept=0
for ((i = 0; i < ${#cand_path[@]}; i++)); do
    classify "${cand_path[i]}" "${cand_head[i]}" "${cand_branch[i]}" "${cand_state[i]}"
    shown=${cand_path[i]//$'\n'/\\n}
    printf '%s\t%s\t%s\t%s\n' "${verdict}" "${shown}" "${cand_branch[i]:-(detached ${cand_head[i]:0:12})}" "${reason}"
    case ${verdict} in
    gc) gc+=("${i}") ;;
    error) errors=$((errors + 1)) ;;
    *) kept=$((kept + 1)) ;;
    esac
done
for ((i = 0; i < ${#q_path[@]}; i++)); do
    read_marker "${q_path[i]}"
    if [[ -n ${quarantined_at} ]]; then
        reason="quarantined $(age $((now - quarantined_at))) ago"
    else
        reason="no ${marker} marker in its admin directory (--purge keeps it)"
    fi
    printf 'quarantine\t%s\t%s\t%s%s\n' "${q_path[i]//$'\n'/\\n}" "${q_branch[i]:-(detached ${q_head[i]:0:12})}" "${reason}" "${q_state[i]:+, ${q_state[i]}}"
done

if ((errors)); then
    printf 'summary\t%d qualify, %d kept, %d errors; nothing moved\n' "${#gc[@]}" "${kept}" "${errors}"
    exit 1
fi
if ((! apply)); then
    printf 'summary\t%d qualify, %d kept, %d in quarantine; dry run, rerun with --apply to quarantine\n' "${#gc[@]}" "${kept}" "${#q_path[@]}"
    exit 0
fi

if ((${#gc[@]})); then
    resolved=''
    if mkdir -p "${quarantine}" && [[ ! -L ${quarantine} ]]; then resolved=$(physical "${quarantine}"); fi
    [[ ${resolved} == "${quarantine}" ]] || { # lint-comparisons: allow both sides are pwd -P forms
        echo "worktree-gc: refused: the quarantine ${quarantine} is not a plain directory" >&2
        exit 2
    }
fi
quarantined=0 held=0 failed=0
for i in "${gc[@]+"${gc[@]}"}"; do
    path=${cand_path[i]} head=${cand_head[i]}
    if ! under_base "${path}" || in_quarantine "${path}"; then
        echo "worktree-gc: refused: ${path} is outside ${base}/ or in the quarantine" >&2
        exit 2
    fi
    # A fresh directory per tree, so the destination never exists (git moves into an existing directory) and two trees
    # of the same name never meet.
    if ! slot=$(mktemp -d "${quarantine}/XXXXXXXX"); then
        printf 'failed\t%s\tcannot create a directory in the quarantine\n' "${path}"
        failed=$((failed + 1))
        continue
    fi
    dest=${slot}/${path##*/}
    # One rename: a process inside the tree keeps its working directory, now in the quarantine; nothing is deleted.
    if ! git -C "${toplevel}" worktree move "${path}" "${dest}"; then
        rmdir "${slot}" 2> /dev/null || true
        printf 'failed\t%s\tgit worktree move refused\n' "${path}"
        failed=$((failed + 1))
        continue
    fi
    # The classification may be minutes old (gh calls); whatever changed since moved with the tree and holds it.
    reason=''
    if ! dir=$(admin_dir "${dest}") || ! write_marker "${dir}" "${now} ${head}"; then
        reason="cannot write ${marker} in its admin directory"
    elif ! tree_status "${dest}"; then
        reason='git status failed after the move'
    elif [[ -n ${status} ]]; then
        reason='changed since the check: dirty, untracked or ignored files'
    elif ((flagged)); then
        reason="${flagged} index entries marked assume-unchanged or skip-worktree since the check"
    elif ! moved_head=$(git -C "${dest}" rev-parse --verify --quiet 'HEAD^{commit}'); then
        reason='cannot read HEAD after the move'
    elif [[ ${moved_head} != "${head}" ]]; then
        reason="head moved from ${head:0:12} to ${moved_head:0:12} since the check"
    fi
    if [[ -n ${reason} ]]; then
        printf 'held\t%s\t%s\t%s\n' "${path}" "${dest}" "${reason}"
        held=$((held + 1))
    else
        printf 'quarantined\t%s\t%s\n' "${path}" "${dest}"
        quarantined=$((quarantined + 1))
    fi
done
printf 'summary\t%d quarantined, %d held, %d failed, %d kept\n' "${quarantined}" "${held}" "${failed}" "${kept}"
((! failed)) || exit 1
