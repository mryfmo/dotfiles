#!/usr/bin/env bash
# @file records-sync.sh
# @brief Carry the program's records from the main checkout to a `records/sync-<n>` pull request.
# @description
#   Regime-cutover U28 (ADDENDUM), the orchestrator seat's lever, allowed by the rows
#   `~/.local/bin/common/records-sync.sh *` and the bare `~/.local/bin/common/records-sync.sh` of
#   `home/dot_agents/omp/policies/orchestrator.yml` (the seat's own `git push` and `gh pr create` stay denied;
#   `worker.yml` denies every form, bare included, U28b F3). It runs in the main checkout, where the orchestrator
#   writes its records (a linked worktree is refused), and `.orchestration` there must be a real directory.
#   The copy set (U101) is exactly the program store `.orchestration/orchestrate/<program>/`: its files on disk,
#   tracked or untracked and not ignored (`git ls-files --cached --others --exclude-standard`), compared with the
#   same paths in `origin/main` by content, so a file the store lacks but `origin/main` holds is deleted and the
#   checkout's `HEAD`, however stale, is never the base; nothing outside the store is carried. Both listings are
#   read NUL-delimited from files: a git failure, even after output, or a listing that ends mid-entry refuses the
#   run before anything is created. The store's `redact-words.txt` (one literal word per line, `#` comments) is
#   never copied, deleted or published. Every path must lie under `.orchestration/`, hold no control character
#   (a newline would hide a component from the symlink check) and no `..`. A path the store listing names must also
#   have no symlink component (git lists the files below a linked directory too, U28b F2), and an existing one must
#   be a regular file whose directory resolves (`pwd -P`) inside the store, or a directory (a file that became one),
#   else the run is refused before anything is created. A deletion candidate (a path of `origin/main` the store no
#   longer holds as a regular file) gets the name checks only: it is never read, only removed. A file that became a
#   directory, or the reverse, is mirrored as the deletion plus the additions in the one commit.
#   In a new detached worktree under `$TMPDIR` at `origin/main`, made and used with `core.hooksPath=/dev/null` so no
#   hook of the checkout's repository runs there (U101), it deletes what the store lacks, then copies the set,
#   masks the copies with the worktree's own `scripts/validate-agent-assets.py --mask-secrets` (the checkout's files
#   are never changed; a masking failure aborts), then refuses the run if that validator's `--scan-identifiers`
#   still finds a secret pattern, a home directory path or a redact word (in a copy's text or path). Neither tool's
#   output is shown (it may name a copy's path or an original key): both go to files in the scratch directory, and
#   a failure prints a fixed message with the exit status only (U101). It stages exactly the copy set by explicit
#   paths, and refuses unless the staged paths equal, as a sorted NUL list, every deletion and every copy whose mode
#   and object id differ from origin/main's; an empty change is refused. `<n>` is then one more than the largest
#   number among
#   the remote heads, the local branches (U28b F6) and the heads of the newest 1000 pull requests named
#   `records/sync-<n>`, `records/program-store-<n>` or `records/<program>-sync-<n>` (the earlier syncs), and the
#   branch must match `records/sync-<n>`. It commits `chore(records): <program> sync <n>` with the footer, author and
#   committer both the identity `git config user.name`/`user.email` read once at the start, set for the commit
#   alone as GIT_AUTHOR_*/GIT_COMMITTER_*, which outrank every `user.*`, `author.*` and `committer.*` config key of
#   the repository, an include or the worktree. Every `GIT_*` variable the caller exported (GIT_AUTHOR_*,
#   GIT_COMMITTER_*, GIT_CONFIG_*, GIT_DIR and the rest) is removed before anything else runs (U101), by a loop over
#   `compgen -e` with no here-string, and a second pass refuses if any is left. The push never runs in the
#   checkout's repository, whose config and includes (an `includeIf "gitdir:…/worktrees/**"` switches on only in the
#   sync worktree) could rewrite its URL: the one commit is fetched by object id into a new empty bare repository
#   in the scratch directory (`git init --bare --template=`, so no hooks), and pushed from there to origin's https
#   URL, read once from the checkout (any other scheme is refused), as `<oid>:refs/heads/records/sync-<n>`, with
#   `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1` and the credential helper `!gh auth git-credential` only, so
#   no config at all can redirect it. It then opens the pull request with
#   `gh pr create --base main --head records/sync-<n> --title ... --body-file ...`, `gh` also reading no user or
#   system git config. The body lists the `units.tsv` ids and the
#   `decisions.tsv` timestamps the sync adds or changes and the line `Program-Unit: <program>/<unit>`, which the
#   `regime` check requires (U28c F2). The worktree is removed on every exit (`git worktree remove --force`, only on
#   the path this run created), and a run that exits before its push deletes the branch it created (only that one),
#   so a retry takes the same number; a pushed branch stays. Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT
#   seconds.
# @option --base <ref> The start point; only `origin/main` (the default) is accepted.
# @option --program <name> The program directory under `.orchestration/orchestrate/`; default: the only one.
# @option --unit <U<n>> The unit the body's `Program-Unit:` line names; default: U20, the records unit.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `synced branch=records/sync-<n> files=<n> pr=<url>`.
# @exitcode 0 The pull request was opened.
# @exitcode 1 A `git` or `gh` step, or the masking, failed; nothing was pushed unless the receipt says so.
# @exitcode 2 Refused: usage, a linked worktree, the program, the copy set, the identifier scan, the identity, a
#   push URL that is not https, or nothing to sync.
# @example
#   ~/.local/bin/common/records-sync.sh --program regime-cutover --unit U20
set -euo pipefail

# Git is steered by no inherited environment (U101, as hcom-seat does since U85): an exported GIT_AUTHOR_NAME would
# name the commit's author, and GIT_CONFIG_* would add config, includes and URL rewrites to every git command. The
# names come from the builtin compgen through a command substitution (a pipe, no temporary file, so bash 3.2 cannot
# skip the loop when no here-string file can be made) and split on the default IFS, which bash never imports: an
# exported name is an identifier, with no blank or glob character. A second pass refuses if any GIT_* name is left.
inherited=$(compgen -e) || {
    echo 'records-sync.sh: refused: cannot list the environment' >&2
    exit 2
}
for inherited_name in ${inherited}; do
    case ${inherited_name} in
    GIT_*) unset "${inherited_name}" ;;
    esac
done
inherited=$(compgen -e) || {
    echo 'records-sync.sh: refused: cannot list the environment' >&2
    exit 2
}
for inherited_name in ${inherited}; do
    case ${inherited_name} in
    GIT_*)
        echo "records-sync.sh: refused: ${inherited_name} is still in the environment after the scrub" >&2
        exit 2
        ;;
    esac
done

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

lever='records-sync.sh'
usage='usage: records-sync.sh [--base origin/main] [--program <name>] [--unit U<n> (default U20)]'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
footer='Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>'
pr_footer='🤖 Generated with [Claude Code](https://claude.com/claude-code)'

# @description Print the refusal on stderr and exit 2.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print the failure on stderr and exit 1.
# @arg $@ string The reason.
fail() {
    echo "${lever}: $*" >&2
    exit 1
}

# @description Run `gh` with its wait bounded by PR_LEVER_GH_TIMEOUT seconds.
# @arg $@ string The `gh` arguments.
gh_bounded() {
    perl -e 'alarm shift; exec @ARGV or die "exec gh: $!\n"' "${gh_timeout}" gh "$@"
}

# @description Remove the worktree this run created, and its scratch directory.
cleanup() {
    if [[ -n ${scratch:-} && -d ${scratch} ]]; then
        if [[ -d ${scratch}/tree ]]; then
            git -C "${toplevel}" worktree remove --force "${scratch}/tree" > /dev/null 2>&1 ||
                echo "${lever}: could not remove the worktree ${scratch}/tree" >&2
        fi
        rm -r "${scratch}" 2> /dev/null || echo "${lever}: could not remove ${scratch}" >&2
    fi
    # U28b F6: a run that created its branch and never pushed it deletes exactly that branch, so a retry is not
    # blocked by it; a pushed branch stays (the remote holds it, and the next run numbers past it).
    if [[ -n ${created_branch:-} && ${pushed:-0} == 0 ]]; then
        git -C "${toplevel}" branch -D "${created_branch}" > /dev/null 2>&1 ||
            echo "${lever}: could not delete the unpushed branch ${created_branch}" >&2
    fi
}

# @description Run git with no user or system config (U101): no `url.*.insteadOf`/`pushInsteadOf`, credential
#   helper or signing setting of the operator's global config reaches the push, the commit or the `gh` steps.
# @arg $@ string The `git` arguments.
git_plain() {
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git "$@"
}

# @description Run `gh` as gh_bounded does, with no user or system git config for the `git` it runs.
# @arg $@ string The `gh` arguments.
gh_plain() {
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 gh_bounded "$@"
}

# @description Run git in the sync worktree with every hook off (U101): `core.hooksPath=/dev/null` names no hook
#   (post-checkout, pre-commit, post-commit and the rest), so nothing but this lever writes into the tree or its
#   index; `core.fileMode=true` makes the staged mode the file's, as the expected staged set below assumes.
# @arg $@ string The `git` arguments.
git_tree() {
    git -c core.hooksPath=/dev/null -c core.fileMode=true -C "${tree}" "$@"
}

# @description Refuse a path by its name alone: a control character (a newline would end the component split of
#   check_path early and leave the leaf unchecked), a place outside `.orchestration/`, or `..`. A deletion candidate
#   gets only this check (U101): it is never read, only removed from the sync worktree.
# @arg $1 string The repository-relative path.
check_name() {
    local path=$1
    [[ ${path} != *[[:cntrl:]]* ]] || refuse 'a path of the copy set holds a control character' # lint-comparisons: allow a character test on the raw git path

    case ${path} in # lint-comparisons: allow a repository-relative path as git prints it, refused unless under the store
    .orchestration/*) ;;
    *) refuse "a path of the copy set is outside .orchestration/: ${path}" ;;
    esac
    [[ ${path} != *..* ]] || refuse "a path of the copy set holds '..': ${path}" # lint-comparisons: allow refuses a raw git path that holds ..
}

# @description Refuse a path the store listing names (check_name, then): a symlink component, or, when it exists,
#   anything but a regular file whose directory resolves inside the store (U28b F2) or a directory. A directory
#   stands where the index still has a file of that name (the file became a directory, U101): its own files are
#   listed as entries of their own, and the file it replaced is carried as a deletion.
# @arg $1 string The repository-relative path.
check_path() {
    local path=$1 prefix='' part rest source_dir
    check_name "${path}"
    # Split on `/` by parameter expansion (no here-string, so no temporary file can go missing, U101).
    rest=${path}
    while [[ -n ${rest} ]]; do
        part=${rest%%/*}
        if [[ ${rest} == */* ]]; then # lint-comparisons: allow splits the raw git path into its components
            rest=${rest#*/}
        else
            rest=''
        fi
        prefix=${prefix:+${prefix}/}${part}
        [[ ! -L ${prefix} ]] || refuse "a component of a path of the copy set is a symlink: ${prefix} (in ${path})"
    done
    if [[ -f ${path} ]]; then
        source_dir=$(cd "${path%/*}" && pwd -P) || refuse "cannot resolve the directory of ${path}"
        [[ ${source_dir} == "${store_root}" || ${source_dir} == "${store_root}"/* ]] || # lint-comparisons: allow both sides are pwd -P forms
            refuse "a path of the copy set resolves outside ${store_root}: ${path}"
    elif [[ -e ${path} && ! -d ${path} ]]; then
        refuse "a path of the copy set is not a regular file: ${path}"
    fi
}

base=origin/main
program=''
unit=U20
while (($#)); do
    case $1 in
    --base | --program | --unit)
        (($# >= 2)) || refuse "${usage}"
        case $1 in
        --base) base=$2 ;;
        --program) program=$2 ;;
        --unit) unit=$2 ;;
        esac
        shift 2
        ;;
    *) refuse "${usage}" ;;
    esac
done
[[ ${base} == origin/main ]] || refuse "--base accepts only origin/main: ${base}" # lint-comparisons: allow a git ref name, not a path
[[ ${unit} =~ ^U[0-9]+$ ]] || refuse "--unit is not a plain unit id U<n>: ${unit}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'

toplevel=$(git rev-parse --show-toplevel 2> /dev/null) || refuse 'not in a git checkout'
git_dir=$(git rev-parse --path-format=absolute --git-dir) || refuse 'cannot read the git directory'
common_dir=$(git rev-parse --path-format=absolute --git-common-dir) || refuse 'cannot read the git common directory'
git_dir=$(cd "${git_dir}" && pwd -P) || refuse "cannot resolve ${git_dir}"
common_dir=$(cd "${common_dir}" && pwd -P) || refuse "cannot resolve ${common_dir}"
[[ ${git_dir} == "${common_dir}" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse "${toplevel} is a linked worktree; run from the main checkout, where the orchestrator writes its records"
cd "${toplevel}" || refuse "cannot enter ${toplevel}"
# U28b F2: the store root itself is no symlink, so every canonical path below is measured against the real store.
top_real=$(pwd -P) || refuse "cannot resolve ${toplevel}"
[[ -d .orchestration && ! -L .orchestration ]] || refuse ".orchestration is missing or a symlink in ${toplevel}"
store_root=$(cd .orchestration && pwd -P) || refuse "cannot resolve ${toplevel}/.orchestration"
[[ ${store_root} == "${top_real}/.orchestration" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse ".orchestration resolves outside ${top_real}: ${store_root}"
if [[ -z ${program} ]]; then
    programs=()
    for dir in .orchestration/orchestrate/*/; do
        dir=${dir%/}
        [[ -d ${dir} ]] && programs+=("${dir##*/}")
    done
    ((${#programs[@]} == 1)) || refuse "name the program with --program; .orchestration/orchestrate/ holds ${#programs[@]}"
    program=${programs[0]}
fi
[[ ${program} =~ ^[a-z0-9][a-z0-9_-]*$ ]] || refuse "the program name is outside [a-z0-9][a-z0-9_-]*: ${program}"
records=.orchestration/orchestrate/${program}
# U28b F2: no component of the store directory is a symlink (git would list the files below a linked one too).
for prefix in .orchestration/orchestrate "${records}"; do
    [[ ! -L ${prefix} ]] || refuse "a component of a path of the copy set is a symlink: ${prefix} (in ${records}/)"
done
[[ -d ${records} ]] || refuse "no program directory ${records}"
# U101: the words no copy may contain; the file itself is never copied, deleted or published.
words=${records}/redact-words.txt
if [[ -e ${words} || -L ${words} ]]; then
    check_path "${words}"
    [[ -f ${words} ]] || refuse "${words} is not a regular file"
    words_real=$(cd "${records}" && pwd -P)/redact-words.txt || refuse "cannot resolve ${words}"
else
    words_real=''
fi
# The commit's identity is the operator's, read once here; the commit itself then runs with no user config.
author_name=$(git config user.name) || refuse 'git config user.name is unset'
author_email=$(git config user.email) || refuse 'git config user.email is unset'
# U101: the push URL is origin's, read once here and pushed to from a fresh repository (below); https only.
push_url=$(git_plain config --get remote.origin.url) || refuse 'no remote.origin.url'
case ${push_url} in # lint-comparisons: allow the URL's scheme as configured, the push target itself
https://?*) ;;
*) refuse "the push needs an https origin URL, not ${push_url}" ;;
esac

git fetch --quiet origin main || fail 'git fetch origin main failed'
scratch=$(mktemp -d "${TMPDIR:-/tmp}/records-sync.XXXXXX") || fail 'mktemp failed'
trap cleanup EXIT
# U101: the copy set is the store's files on disk (tracked or not, not ignored), compared with origin/main by
# content; the checkout's HEAD, however stale, is never the base. Each listing goes to a file and is read
# NUL-delimited: a git failure, even after output, and a listing whose last entry has no NUL end (cut short) refuse
# here, before the worktree, the branch or any gh call.
listing=${scratch}/listing
git ls-files -z --cached --others --exclude-standard -- "${records}/" > "${listing}" || fail 'git ls-files failed'
files=()
present=$'\n'
path=''
while IFS= read -r -d '' path; do
    [[ ${path} != "${words}" ]] || continue # lint-comparisons: allow both are repository-relative paths as git prints them
    check_path "${path}"
    if [[ -f ${path} && ${present} != *$'\n'"${path}"$'\n'* ]]; then # lint-comparisons: allow repository-relative paths as git prints them
        files+=("${path}")
        present+=${path}$'\n'
    fi
done < "${listing}"
[[ -z ${path} ]] || refuse "the listing of ${records}/ ends mid-entry; nothing was created"
# Full entries (`<mode> blob <oid>` TAB path): the deletions come from them, and the expected staged set below compares
# each copy with its entry on origin/main.
git ls-tree -r -z "${base}" -- "${records}/" > "${listing}" || fail "git ls-tree ${base} failed"
gone=()
base_entries=$'\n'
entry=''
while IFS= read -r -d '' entry; do
    path=${entry#*$'\t'}
    check_name "${path}"
    base_entries+=${path}$'\t'${entry%%$'\t'*}$'\n'
    [[ ${path} != "${words}" && ${present} != *$'\n'"${path}"$'\n'* ]] || continue # lint-comparisons: allow repository-relative paths as git prints them
    gone+=("${path}")
done < "${listing}"
[[ -z ${entry} ]] || refuse "the listing of ${base}:${records}/ ends mid-entry; nothing was created"
((${#files[@]} + ${#gone[@]} > 0)) || refuse "nothing to sync under ${records}/"

tree=${scratch}/tree
git -c core.hooksPath=/dev/null worktree add --quiet --detach "${tree}" "${base}" || fail 'git worktree add failed'
masked=()
# Deletions first: a file that became a directory (or the reverse) frees its name before the copy needs it, and the
# one commit carries the deletion and the additions (U101).
for path in ${gone[@]+"${gone[@]}"}; do
    git_tree rm --quiet -- "${path}" || fail "git rm ${path} failed"
done
for path in ${files[@]+"${files[@]}"}; do
    mkdir -p "${tree}/${path%/*}" || fail "mkdir for ${path} failed"
    cp -p "${path}" "${tree}/${path}" || fail "cp ${path} failed"
    masked+=("${tree}/${path}")
done
if ((${#masked[@]})); then
    # U101: neither tool's output is shown. The masker prints each copy's path and, on a key collision, the original
    # keys; either may hold a redact word or a secret. Both go to files in the scratch directory (removed on exit),
    # and a failure says only that it happened and the exit status.
    status=0
    uv run --no-project python -I "${tree}/scripts/validate-agent-assets.py" --mask-secrets "${masked[@]}" \
        > "${scratch}/mask.log" 2>&1 || status=$?
    ((status == 0)) || fail "masking the copies failed (exit ${status}); its output is withheld, nothing was published"
    # U101: after masking, no copy may still name a secret, a home path or a redact word, its path included.
    scan=(--scan-identifiers)
    [[ -z ${words_real} ]] || scan+=(--redact-words "${words_real}")
    (cd "${tree}" && uv run --no-project python -I scripts/validate-agent-assets.py "${scan[@]}" -- "${files[@]}") \
        > "${scratch}/scan.log" 2>&1 || status=$?
    ((status != 1)) ||
        refuse 'the identifier scan found a secret, a home path or a redact word in the masked copies (exit 1); its output is withheld, nothing was published'
    ((status == 0)) || fail "the identifier scan failed (exit ${status}); its output is withheld, nothing was published"
fi
# U101: exactly the copy set is staged, by explicit paths (the deletions above, the copies here), never a directory
# pathspec; then the staged paths must equal, as the same sorted NUL list, the set computed independently: every
# deletion, and every copy whose `<mode> blob <oid>` (hash-object, no filters) differs from its origin/main entry.
expected=${scratch}/expected
: > "${expected}" || fail 'cannot write the expected staged set'
for path in ${gone[@]+"${gone[@]}"}; do
    printf '%s\0' "${path}" >> "${expected}" || fail 'cannot write the expected staged set'
done
if ((${#files[@]})); then
    git_tree add -- "${files[@]}" || fail 'git add failed'
    oids=$(git_tree hash-object --no-filters -- "${files[@]}") || fail 'git hash-object failed'
    # shellcheck disable=SC2206 # object ids split on the default IFS: hexadecimal, no blank or glob character
    oid_list=(${oids})
    ((${#oid_list[@]} == ${#files[@]})) || fail 'git hash-object printed a different number of object ids'
    index=0
    for path in "${files[@]}"; do
        mode=100644
        if [[ -x ${tree}/${path} ]]; then
            mode=100755
        fi
        if [[ ${base_entries} != *$'\n'"${path}"$'\t'"${mode} blob ${oid_list[index]}"$'\n'* ]]; then # lint-comparisons: allow a repository-relative path and an object id as git prints them
            printf '%s\0' "${path}" >> "${expected}" || fail 'cannot write the expected staged set'
        fi
        index=$((index + 1))
    done
fi
staged=${scratch}/staged
git_tree diff --cached --no-renames --name-only -z > "${staged}" || fail 'git diff --cached failed'
LC_ALL=C sort -z "${expected}" > "${expected}.sorted" || fail 'cannot sort the expected staged set'
LC_ALL=C sort -z "${staged}" > "${staged}.sorted" || fail 'cannot sort the staged set'
cmp -s "${expected}.sorted" "${staged}.sorted" ||
    refuse 'the staged paths differ from the copy set; nothing was committed or pushed'
[[ -s ${staged} ]] || refuse 'the copies equal origin/main; nothing to sync'
count=$(tr -cd '\000' < "${staged}" | wc -c) || fail 'cannot count the staged paths'
count=${count//[[:space:]]/}

remote_heads=$(git ls-remote --heads origin 'refs/heads/records/*') || fail 'git ls-remote origin failed'
# U28b F6: a local branch occupies its number too, whatever left it behind.
local_heads=$(git for-each-ref --format='%(refname)' 'refs/heads/records/') || fail 'git for-each-ref failed'
pr_heads=$(gh_plain pr list --state all --limit 1000 --json headRefName --jq '.[].headRefName') ||
    fail 'gh pr list failed'
last=$(printf '%s\n%s\n%s\n' "${remote_heads}" "${local_heads}" "${pr_heads}" |
    PROGRAM=${program} awk '{ ref = $NF; sub(/^refs\/heads\//, "", ref) }
        ref ~ "^records/(sync|program-store|" ENVIRON["PROGRAM"] "-sync)-[0-9]+$" { n = ref; sub(/.*-/, "", n); if (n + 0 > max) max = n + 0 }
        END { print max + 0 }') || fail 'cannot number the sync'
n=$((last + 1))
branch=records/sync-${n}
[[ ${branch} =~ ^records/sync-[1-9][0-9]*$ ]] || refuse "the branch is outside records/sync-<n>: ${branch}"
git_tree switch --quiet -c "${branch}" || fail "git switch -c ${branch} failed"
created_branch=${branch}
pushed=0

units=$(git_tree diff --cached -U0 -- "${records}/units.tsv" | sed -n -E 's/^\+(U[0-9]+[a-z]?)\t.*/\1/p' | sort -u | paste -sd ' ' -) ||
    fail 'cannot list the units'
decisions=$(git_tree diff --cached -U0 -- "${records}/decisions.tsv" | sed -n -E 's/^\+([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z)\t.*/\1/p' | sort -u | paste -sd ' ' -) ||
    fail 'cannot list the decisions'
title="chore(records): ${program} sync ${n}"
# U101: author and committer come from the environment, which outranks every config key (user.*, author.*,
# committer.*, in the repository, an include or the worktree's config); the GIT_* scrub above left none inherited.
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 \
    GIT_AUTHOR_NAME=${author_name} GIT_AUTHOR_EMAIL=${author_email} \
    GIT_COMMITTER_NAME=${author_name} GIT_COMMITTER_EMAIL=${author_email} \
    git_tree commit --quiet -m "${title}" \
    -m "Carries ${count} file(s) of ${records}/ from the main checkout, compared with origin/main (records-sync.sh)." -m "${footer}" ||
    fail 'git commit failed'
oid=$(git_tree rev-parse --verify 'HEAD^{commit}') || fail 'cannot read the sync commit'
# U101: the push runs in a repository with no config, includes or hooks, so nothing the checkout or the sync worktree
# reads can rewrite the URL; auto maintenance stays off in it, since the scratch directory is removed on exit.
push_repo=${scratch}/push.git
git_plain init --quiet --bare --template= "${push_repo}" || fail 'git init --bare for the push failed'
git_plain -C "${push_repo}" -c gc.auto=0 -c maintenance.auto=false fetch --quiet --no-tags "${tree}" "${oid}" ||
    fail 'fetching the sync commit into the push repository failed'
git_plain -C "${push_repo}" -c gc.auto=0 -c maintenance.auto=false -c credential.helper= \
    -c 'credential.helper=!gh auth git-credential' push --quiet "${push_url}" "${oid}:refs/heads/${branch}" ||
    fail "git push ${branch} failed; nothing was opened"
pushed=1
body=${scratch}/body.md
{
    # shellcheck disable=SC2016 # the backticks are Markdown code spans
    printf '## Summary\n\nRecords sync %s of `%s` (%s file(s)), carried by `records-sync.sh` from the main checkout and compared with origin/main; every copy was masked with `validate-agent-assets.py --mask-secrets` and passed its `--scan-identifiers`.\n\n' "${n}" "${program}" "${count}"
    printf -- '- units.tsv rows added or changed: %s\n' "${units:-none}"
    printf -- '- decisions.tsv rows added or changed: %s\n\n' "${decisions:-none}"
    printf 'Program-Unit: %s/%s\n\n' "${program}" "${unit}"
    printf '%s\n' "${pr_footer}"
} > "${body}" || fail 'cannot write the body'
url=$(gh_plain pr create --base main --head "${branch}" --title "${title}" --body-file "${body}") ||
    fail "gh pr create failed; the branch ${branch} is pushed"
echo "synced branch=${branch} files=${count} pr=${url}"
