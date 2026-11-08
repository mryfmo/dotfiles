#!/usr/bin/env bash
# @file records-sync.sh
# @brief Carry the program's records from the main checkout to a `records/sync-<n>` pull request.
# @description
#   Regime-cutover U28 (ADDENDUM), the orchestrator seat's lever, allowed by the rows
#   `~/.local/bin/common/records-sync.sh *` and the bare `~/.local/bin/common/records-sync.sh` of
#   `home/dot_agents/omp/policies/orchestrator.yml` (the seat's own `git push` and `gh pr create` stay denied;
#   `worker.yml` denies every form, bare included, U28b F3). It runs in the main checkout (a linked worktree is
#   refused), where it reads origin's URL, the identity and the local branch names. The store it carries has two forms
#   (regime-cutover U220, store move 4 of 5, handoff/07-store-move-design.md; the `store_resolve` rule U216 gave
#   pr-merge.sh and pr-close.sh, in this lever's own body): the derived program store `${REGIME_STORE_ROOT}/<program>`
#   when that path exists, a plain directory of this user outside every checkout under the root the sourced
#   `regime-env` derives from the physical HOME and the checkout's slug (U215; a link or anything but such a directory
#   there is refused by name); else, until U221 moves the live store, the checkout subtree
#   `.orchestration/orchestrate/<program>/`, the pre-move form, where `.orchestration` must be a real directory. The
#   form chosen is printed once on stderr (`store: derived <dir>`, or `store: checkout <dir> (pre-move form, removed
#   by U221)`). The copy set (U101) is exactly the program store: in the derived form every entry below the directory
#   that is not a directory, listed by `find` through `read_listing` (a link, a fifo or a socket is refused by name,
#   and so is a name beginning with `.`, which the checkout form's ignore rules skip today and no record carries); in
#   the checkout form its files on disk, tracked or untracked and not ignored (`git ls-files --cached --others
#   --exclude-standard`). Each listed path is mapped to its published path under `.orchestration/orchestrate/<program>/`
#   and compared with the same path in `origin/main` by content, in both forms, so a file the store lacks but
#   `origin/main` holds is deleted and the checkout's `HEAD`, however stale, is never the base; nothing outside the
#   store is carried. Both listings are
#   read NUL-delimited from files: a git failure, even after output, or a listing that ends mid-entry refuses the
#   run before anything is created. The store's `redact-words.txt` (one literal word per line, `#` comments) is
#   never copied, deleted or published. Every path must lie under `.orchestration/`, hold no control character
#   (a newline would hide a component from the symlink check) and no `..`. A path the store listing names must also
#   have no symlink component (git lists the files below a linked directory too, U28b F2), and an existing one must
#   be a regular file whose directory resolves (`pwd -P`) inside the store, or a directory (a file that became one),
#   else the run is refused before anything is created. A deletion candidate (a path of `origin/main` the store no
#   longer holds as a regular file) gets the name checks only: it is never read, only removed. A file that became a
#   directory, or the reverse, is mirrored as the deletion plus the additions in the one commit.
#   The whole commit is built in a new repository in a scratch directory under `$TMPDIR` (U101: rounds 2 to 7 each
#   found another channel by which the checkout's git config acted on a sync worktree, so there is none): `git init
#   --bare --template=` (no hooks, no attributes, no config beyond the init's), every command there through
#   `git_isolated` of `git-isolated.sh` (U113: the one flag set that isolates git from every configuration but the
#   command's own), with every inherited `GIT_*` and transport variable removed first by its `git_env_scrub`. Origin's main
#   is fetched into it from origin's https URL (read once from the checkout; any other scheme is refused) with the
#   credential helper `!gh auth git-credential` only. The checkout is only read: its two listings, its store files
#   and `git config user.name`/`user.email`. The copies are made in the scratch directory and masked there with
#   main's `scripts/validate-agent-assets.py --mask-secrets` (the checkout's files are never changed; a masking
#   failure aborts); the run is refused if that validator's `--scan-identifiers` still finds a secret pattern, a
#   home directory path or a redact word in a copy's text or store path. Neither tool's output is shown (it may name
#   a copy's path or an original key): both go to files in the scratch directory, and a failure prints a fixed
#   message with the exit status only. Under a private `GIT_INDEX_FILE` the lever reads main's tree, removes each
#   deletion (`update-index -z --index-info`, mode 0, which needs no work tree), then writes each masked copy, the
#   very file scanned, with `hash-object -w --no-filters` and enters it by mode and object id (`update-index --add
#   --cacheinfo`), and writes the tree. Its
#   `diff-tree -r --name-only -z` against main's tree must equal, as sorted NUL lists, every deletion and every copy
#   whose mode and object id differ from main's; otherwise, or when it is empty, the run is refused. `<n>` is one
#   more than the largest number among origin's heads, the checkout's local branches (U28b F6) and the heads of the
#   newest 1000 pull requests named `records/sync-<n>`, `records/program-store-<n>` or `records/<program>-sync-<n>`
#   (the earlier syncs), and the branch must match `records/sync-<n>`. `commit-tree` makes
#   `chore(records): <program> sync <n>` with the footer on main, author and committer both the identity read at the
#   start, set as GIT_AUTHOR_*/GIT_COMMITTER_* for that command alone, and the same repository pushes
#   `<commit>:refs/heads/records/sync-<n>` to the https URL. It then opens the pull request with
#   `gh pr create --base main --head records/sync-<n> --title ... --body-file ...`, `gh` also reading no user or
#   system git config. The body lists the `units.tsv` ids and the `decisions.tsv` timestamps the sync adds or changes
#   and the line `Program-Unit: <program>/<unit>`, which the `regime` check requires (U28c F2). Every `GIT_*`
#   variable the caller exported (GIT_AUTHOR_*, GIT_COMMITTER_*, GIT_CONFIG_*, GIT_DIR and the rest) is removed
#   before anything else runs, by a loop over `compgen -e` with no here-string, and a second pass refuses if any is
#   left. No branch, worktree or file of the checkout is created; the scratch directory is removed on every exit.
#   Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds.
# @option --base <ref> The start point; only `origin/main` (the default) is accepted.
# @option --program <name> The program directory, under `${REGIME_STORE_ROOT}` when that root exists, else under
#   `.orchestration/orchestrate/`; default: the only one there.
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
    # shellcheck disable=SC2034 # read by the levers that source regime-env from this directory
    LEVER_DIR=${dir}
    name=${self##*/}
    home=$(cd "${HOME}" 2> /dev/null && pwd -P) || home=''             # producer-status: allow the if below takes an empty home as the checkout layout
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
        digest=$(sha256sum < "${self}") || digest='' # producer-status: allow the regex test below refuses an empty digest
    else
        digest=$(shasum -a 256 < "${self}") || digest='' # producer-status: allow the regex test below refuses an empty digest
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
# The isolated git and the environment scrub come from the library beside this script (U113). The scrub runs here,
# before the first git: an exported GIT_AUTHOR_NAME would name the commit's author, GIT_CONFIG_* would add config,
# includes and URL rewrites to every git command, and a proxy or certificate variable would steer the fetch and push.
[[ -r ${LEVER_DIR}/git-isolated.sh ]] || {
    echo "records-sync.sh: refused: git-isolated.sh unreadable beside this script: ${LEVER_DIR}/git-isolated.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/git-isolated.sh
. "${LEVER_DIR}/git-isolated.sh"
# shellcheck disable=SC2119 # no name is kept: every GIT_* and transport variable goes
git_env_scrub

[[ -r ${LEVER_DIR}/read-lib.sh ]] || {
    echo "records-sync.sh: refused: read-lib.sh unreadable beside this script: ${LEVER_DIR}/read-lib.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/read-lib.sh
. "${LEVER_DIR}/read-lib.sh"

# The store root (regime-cutover U220): the program stores lie under `REGIME_STORE_ROOT`, the root the sourced
# regime-env derives from the physical HOME and this checkout's slug (U215) and holds component by component; the
# helper is sourced from the directory this lever runs from and self-checked like a lever (U33), so a rewritten copy
# stops this lever. The call that derives the root comes after this lever's own checkout checks, below (the pattern
# of pr-merge.sh, U216).
[[ -r ${LEVER_DIR}/regime-env ]] || {
    echo "records-sync.sh: refused: regime-env unreadable beside this script: ${LEVER_DIR}/regime-env" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/regime-env
. "${LEVER_DIR}/regime-env"

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

# @description Remove this run's scratch directory, with the repository the sync was built in.
cleanup() {
    if [[ -n ${scratch:-} && -d ${scratch} ]]; then
        rm -r "${scratch}" 2> /dev/null || echo "${lever}: could not remove ${scratch}" >&2
    fi
}

# @description Run `gh` as gh_bounded does, with no user or system git config for the `git` it runs.
# @arg $@ string The `gh` arguments.
gh_plain() {
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 gh_bounded "$@"
}

# @description Run the isolated git in the sync's own repository (U101): the repository named by `--git-dir`, so no
#   checkout is consulted, and nothing of the user, system or checkout configuration (git-isolated.sh, U113).
# @arg $@ string The `git` arguments.
git_scratch() {
    git_isolated --git-dir="${repo}" "$@"
}

# @description Refuse a path by its name alone: a control character (a newline would end the component split of
#   check_path early and leave the leaf unchecked), a place outside `.orchestration/`, or `..`. A deletion candidate
#   gets only this check (U101): it is never read, only removed from the new tree.
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

# @description Refuse a path the store listing names (check_name, then): a published path outside `${records}/`; in
#   the derived form a component beginning with `.` (U220: the checkout form's ignore rules skip such a file today,
#   and a Finder artifact or a repository's own directory is not a record); a symlink at any component below the
#   chosen store (U28b F2: git lists the files below a linked directory too, and the derived walk is held the same
#   way; the store's own chain is held by store_resolve and regime-env); or, when the source `<store>/<rel>` exists,
#   anything but a regular file whose directory resolves (`pwd -P`) inside the store or a directory. A directory
#   stands where the index still has a file of that name (the file became a directory, U101): its own files are
#   listed as entries of their own, and the file it replaced is carried as a deletion.
# @arg $1 string The published path `.orchestration/orchestrate/<program>/<rel>`; its source is `<store>/<rel>`.
check_path() {
    local path=$1 rel prefix part rest source_dir
    check_name "${path}"
    case ${path} in # lint-comparisons: allow a published path, refused unless under the program's prefix
    "${records}"/?*) ;;
    *) refuse "a path of the copy set is outside ${records}/: ${path}" ;;
    esac
    rel=${path#"${records}/"}
    # Split on `/` by parameter expansion (no here-string, so no temporary file can go missing, U101).
    prefix=${store}
    rest=${rel}
    while [[ -n ${rest} ]]; do
        part=${rest%%/*}
        if [[ ${rest} == */* ]]; then # lint-comparisons: allow splits the path into its components
            rest=${rest#*/}
        else
            rest=''
        fi
        [[ ${store_form} != derived || ${part} != .* ]] || # lint-comparisons: allow a name test on one component of the walk
            refuse "a name of the derived store begins with '.', which the checkout form's ignore rules skip and no record carries: ${path}"
        prefix=${prefix}/${part}
        [[ ! -L ${prefix} ]] || refuse "a component of a path of the copy set is a symlink: ${prefix} (in ${path})"
    done
    if [[ -f ${prefix} ]]; then
        source_dir=$(cd "${prefix%/*}" && pwd -P) || refuse "cannot resolve the directory of ${path}"
        [[ ${source_dir} == "${store}" || ${source_dir} == "${store}"/* ]] || # lint-comparisons: allow both sides are pwd -P forms
            refuse "a path of the copy set resolves outside ${store}: ${path}"
    elif [[ -e ${prefix} && ! -d ${prefix} ]]; then
        refuse "a path of the copy set is not a regular file: ${path}"
    fi
}

# @description Enter one listed path into the copy set (U220: the one reader of both listings): `redact-words.txt` is
#   skipped, the path is held by check_path, and an existing regular file is kept once (`files`, `present`).
# @arg $1 string The published path.
collect_path() {
    local path=$1
    [[ ${path} != "${words}" ]] || return 0 # lint-comparisons: allow both are published paths of the store
    check_path "${path}"
    if [[ -f ${store}/${path#"${records}/"} && ${present} != *$'\n'"${path}"$'\n'* ]]; then # lint-comparisons: allow published paths of the store
        files+=("${path}")
        present+=${path}$'\n'
    fi
}

# @description Choose the program store (regime-cutover U220, store move 4 of 5; the `store_resolve` shape of U216's
#   pr-merge.sh and pr-close.sh, in this lever's own body: no helper file, standing order 36): the derived store
#   `${REGIME_STORE_ROOT}/<program>` when that path exists, which must then be a directory of this user and no symlink
#   (a link is refused by name before anything is read through it; a file or another user's directory is refused by
#   name too), else the checkout subtree `<toplevel>/.orchestration/orchestrate/<program>`, the pre-move form that
#   stands until U221 moves the live store, held as before this unit (U28b F2): `.orchestration` a real directory
#   resolving (`pwd -P`) inside the toplevel, no symlink at `.orchestration/orchestrate` or at the program directory,
#   which must exist. The root's own components are held by regime-env (`regime_store_root`). Nothing is written. The
#   form chosen is printed once on stderr (`store: derived <dir>`, or `store: checkout <dir> (pre-move form, removed
#   by U221)`), the line the coordinator reads after the deploy.
# @arg $1 string The program name.
# @set store The chosen store, `pwd -P` form (the root and the toplevel are both physical).
# @set store_form `derived` or `checkout`.
store_resolve() {
    local program=$1 store_derived store_checkout orchestration_real prefix
    [[ -n ${REGIME_STORE_ROOT:-} ]] ||
        refuse "regime-env derived no store root for ${toplevel}; the program store is judged under it (U216, U220)"
    store_derived=${REGIME_STORE_ROOT}/${program}
    store_checkout=${top_real}/.orchestration/orchestrate/${program}
    [[ ! -L ${store_derived} ]] ||
        refuse "${store_derived} is a symlink; the derived program store is a plain directory of this user under the store root ${REGIME_STORE_ROOT}, and nothing is read through a link"
    if [[ -e ${store_derived} ]]; then
        [[ -d ${store_derived} && -O ${store_derived} ]] ||
            refuse "${store_derived} exists but is not a directory of this user; the derived program store under ${REGIME_STORE_ROOT} is read only as one"
        store=${store_derived}
        store_form=derived
        echo "${lever}: store: derived ${store}" >&2
        return 0
    fi
    # The pre-move form (until U221): the holds on the checkout subtree, as before this unit.
    [[ -d .orchestration && ! -L .orchestration ]] || refuse ".orchestration is missing or a symlink in ${toplevel}"
    orchestration_real=$(cd .orchestration && pwd -P) || refuse "cannot resolve ${toplevel}/.orchestration"
    [[ ${orchestration_real} == "${top_real}/.orchestration" ]] || # lint-comparisons: allow both sides are pwd -P forms
        refuse ".orchestration resolves outside ${top_real}: ${orchestration_real}"
    # U28b F2: no component of the store directory is a symlink (git would list the files below a linked one too).
    for prefix in .orchestration/orchestrate "${records}"; do
        [[ ! -L ${prefix} ]] || refuse "a component of a path of the copy set is a symlink: ${prefix} (in ${records}/)"
    done
    [[ -d ${records} ]] || refuse "no program directory ${records}"
    store=${store_checkout}
    store_form=checkout
    echo "${lever}: store: checkout ${store} (pre-move form, removed by U221)" >&2
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

toplevel=$(git_isolated rev-parse --show-toplevel 2> /dev/null) || refuse 'not in a git checkout'
git_dir=$(git_isolated rev-parse --path-format=absolute --git-dir) || refuse 'cannot read the git directory'
common_dir=$(git_isolated rev-parse --path-format=absolute --git-common-dir) || refuse 'cannot read the git common directory'
git_dir=$(cd "${git_dir}" && pwd -P) || refuse "cannot resolve ${git_dir}"
common_dir=$(cd "${common_dir}" && pwd -P) || refuse "cannot resolve ${common_dir}"
[[ ${git_dir} == "${common_dir}" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse "${toplevel} is a linked worktree; run from the main checkout, where the orchestrator writes its records"
cd "${toplevel}" || refuse "cannot enter ${toplevel}"
# U28b F2: the toplevel is physical, so every canonical path below is measured against the real checkout.
top_real=$(pwd -P) || refuse "cannot resolve ${toplevel}"
# U220: regime-env derives `REGIME_STORE_ROOT` for this checkout (its own refusals name this lever). This lever reads
# nothing in the hcom store, so the store's `origin` binding is not asked of it (`--unbound-ok`, as pr-merge.sh asks
# since U216: the dotfiles program runs on the pre-U33 store pair and its derived hcom store carries no `origin`, so
# the bound form would stop every sync on this host); the collision refusal (an `origin` naming another checkout) and
# every store-root hold stay. The helper's refusal (return 1) is this lever's refusal status, exit 2.
regime_env records-sync.sh --unbound-ok || exit 2
if [[ -z ${program} ]]; then
    # U220: the program is the one directory under the store root when that root exists (the derived form), else the
    # one under the checkout's `.orchestration/orchestrate/` as before; several, or none, refuse naming the place.
    programs=()
    programs_dir=.orchestration/orchestrate
    [[ -z ${REGIME_STORE_ROOT} || ! -d ${REGIME_STORE_ROOT} ]] || programs_dir=${REGIME_STORE_ROOT}
    for dir in "${programs_dir}"/*/; do
        dir=${dir%/}
        [[ -d ${dir} ]] && programs+=("${dir##*/}")
    done
    ((${#programs[@]} == 1)) || refuse "name the program with --program; ${programs_dir}/ holds ${#programs[@]}"
    program=${programs[0]}
fi
[[ ${program} =~ ^[a-z0-9][a-z0-9_-]*$ ]] || refuse "the program name is outside [a-z0-9][a-z0-9_-]*: ${program}"
# The published prefix, where the records lie on origin/main in both forms (U220): the listing of origin/main, the
# deletions and the copies are at these paths.
records=.orchestration/orchestrate/${program}
store='' store_form=''
store_resolve "${program}"
# U101: the words no copy may contain; the file itself is never copied, deleted or published. It lies at the top of
# the chosen store (U220).
words=${records}/redact-words.txt
words_real=${store}/redact-words.txt
if [[ -e ${words_real} || -L ${words_real} ]]; then
    check_path "${words}"
    [[ -f ${words_real} ]] || refuse "${words} is not a regular file"
else
    words_real=''
fi
# @description Read one configuration key the sync needs through read_config (read-lib.sh, U112) and map its three
#   outcomes: unset or empty is refused and a failed read fails, both before any branch, worktree or commit exists
#   (a configured empty identity would otherwise be refused by commit-tree after the branch existed).
# @arg $1 string The git function to read with (`git` reads the user configuration too, `git_isolated` does not).
# @arg $2 string The configuration key.
# @arg $3 string The variable that receives the value.
required_config() {
    local status=0
    read_config "$1" "$2" "$3" "${scratch}/config.err" || status=$?
    case ${status} in
    0) ;;
    1) refuse "git config $2 is unset or empty" ;;
    *) fail "cannot read git config $2" ;;
    esac
}

scratch=$(mktemp -d "${TMPDIR:-/tmp}/records-sync.XXXXXX") || fail 'mktemp failed'
trap cleanup EXIT
# The commit's identity is the operator's, read once here and handed to commit-tree as GIT_AUTHOR_*/GIT_COMMITTER_*;
# git's stderr goes to a file in the scratch directory, which is why the reads follow mktemp. The same reader serves
# origin's URL (audit of 0c7bf092).
author_name='' author_email='' push_url=''
required_config git user.name author_name   # git-isolated: allow the identity is read from the user configuration on purpose
required_config git user.email author_email # git-isolated: allow the identity is read from the user configuration on purpose
# U101: origin's URL, read once here: main is fetched from it and the sync pushed to it (below); https only.
required_config git_isolated remote.origin.url push_url
case ${push_url} in # lint-comparisons: allow the URL's scheme as configured, the push target itself
https://?*) ;;
*) refuse "the push needs an https origin URL, not ${push_url}" ;;
esac
# U101: the whole commit is built in a new repository in the scratch directory, which has no config, includes,
# hooks or attributes of the checkout's: origin's main is fetched into it from the https URL, the copies are hashed
# into it with --no-filters, and the tree, the commit and the push are made there. The checkout is only read: its
# listings, its store files and its config's user.name/user.email (above).
repo=${scratch}/repo.git
git_isolated init --quiet --bare --template= "${repo}" || fail 'git init --bare for the sync failed'
git_scratch -c credential.helper= -c 'credential.helper=!gh auth git-credential' \
    fetch --quiet --no-tags "${push_url}" refs/heads/main || fail 'git fetch main from origin failed'
main=$(git_scratch rev-parse --verify 'FETCH_HEAD^{commit}') || fail 'cannot read the fetched main'
main_tree=$(git_scratch rev-parse --verify "${main}^{tree}") || fail 'cannot read the tree of main'
# U101: the copy set is the store's files on disk (tracked or not, not ignored), compared with origin/main by
# content; the checkout's HEAD, however stale, is never the base. Each listing goes to a file and is read
# NUL-delimited: a git failure, even after output, and a listing whose last entry has no NUL end (cut short) refuse
# here, before any copy, commit or gh call.
listing=${scratch}/listing
# Audit of 0c7bf092: `git ls-files` warns and exits 0 for a directory it cannot open, and a file it then leaves out
# of the listing is absent from the store as far as this lever can see, which is a deletion. So the store is walked
# first (find exits non-zero for a directory it cannot read, and each directory is checked readable and
# searchable), and any warning of either producer refuses the run as well (read_listing, U112); neither output is
# shown (a store path may hold a redact word).
read_listing "${scratch}/dirs" "${scratch}/walk.err" find "${store}" -type d -print0 ||
    refuse "a directory under ${records}/ cannot be read or entered; nothing was created"
dir=''
while IFS= read -r -d '' dir; do
    [[ -r ${dir} && -x ${dir} ]] || refuse "a directory under ${records}/ cannot be read or entered; nothing was created"
done < "${scratch}/dirs"
[[ -z ${dir} ]] || refuse "the walk of ${records}/ ends mid-entry; nothing was created"
files=()
present=$'\n'
if [[ ${store_form} == derived ]]; then # lint-comparisons: allow the form name store_resolve set, not a path
    # U220: the derived store is a plain directory outside every repository, so there is no index to list: find lists
    # every entry below it that is not a directory (`-type f` would skip a symbolic link instead of refusing it), each
    # mapped to its published path under ${records}/ and held by check_path (collect_path). A failure or a warning of
    # the walk refuses as the directory walk's does; an empty walk is no failure (a store whose every file is gone
    # syncs the deletions).
    status=0
    read_listing "${listing}" "${scratch}/listing.err" find "${store}" ! -type d -print0 || status=$?
    case ${status} in
    0 | 1) ;;
    *) refuse "the walk of ${records}/ failed or warned (its output is withheld); nothing was created" ;;
    esac
    entry=''
    while IFS= read -r -d '' entry; do
        case ${entry} in # lint-comparisons: allow a path as find prints it, refused unless below the store
        "${store}"/?*) collect_path "${records}/${entry#"${store}/"}" ;;
        *) refuse "the walk of ${records}/ names a path outside the store; nothing was created" ;;
        esac
    done < "${listing}"
    [[ -z ${entry} ]] || refuse "the walk of ${records}/ ends mid-entry; nothing was created"
else
    # Audit of 7b3c2718: the listing is the one index read in the checkout, and a `core.fsmonitor` hook set in any
    # configuration the checkout reads would run inside it (and could write into the store before the copy). The
    # isolated git turns it off, with the hooks path and the user and system files; the repository level has no off
    # switch, so the checkout's own ignore rules and the default ignore file still shape the listing, which the stderr
    # test below bounds.
    status=0
    read_listing "${listing}" "${scratch}/listing.err" \
        git_isolated ls-files -z --cached --others --exclude-standard -- "${records}/" ||
        status=$?
    case ${status} in
    0 | 1) ;;
    *)
        [[ ! -s ${scratch}/listing.err ]] ||
            refuse "git ls-files warned while listing ${records}/ (its output is withheld); nothing was created"
        fail 'git ls-files failed'
        ;;
    esac
    path=''
    while IFS= read -r -d '' path; do
        collect_path "${path}"
    done < "${listing}"
    [[ -z ${path} ]] || refuse "the listing of ${records}/ ends mid-entry; nothing was created"
fi
# Full entries (`<mode> blob <oid>` TAB path): the deletions come from them, and the expected change set below
# compares each copy with its entry on main.
git_scratch ls-tree -r -z "${main}" -- "${records}/" > "${listing}" || fail "git ls-tree ${base} failed"
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

# The masker and the scanner are main's validator, alone in a tools tree whose `home/` holds main's top-level entry
# names (empty), so its home-path pattern skips the repository's own `home/<entry>` paths as in a checkout; a main
# without `home/` gives an empty one.
tools=${scratch}/tools
mkdir -p "${tools}/scripts" "${tools}/home" || fail 'cannot make the tools tree'
git_scratch cat-file blob "${main}:scripts/validate-agent-assets.py" > "${tools}/scripts/validate-agent-assets.py" ||
    fail "cannot read scripts/validate-agent-assets.py of ${base}"
git_scratch ls-tree -z --name-only "${main}" -- home/ > "${scratch}/home-entries" || fail "cannot list home/ of ${base}"
while IFS= read -r -d '' entry; do
    entry=${entry#home/}
    [[ -n ${entry} && ${entry} != *[/[:cntrl:]]* && ${entry} != . && ${entry} != .. ]] || # lint-comparisons: allow a tree entry name as git prints it
        fail "home/ of ${base} holds an unusable entry name"
    mkdir "${tools}/home/${entry}" || fail 'cannot make the tools tree'
done < "${scratch}/home-entries"
# U101: the copies are masked and scanned in the scratch directory, and these same files are what hash-object
# writes, so the committed bytes are the scanned bytes.
copies=${scratch}/copies
masked=()
for path in ${files[@]+"${files[@]}"}; do
    mkdir -p "${copies}/${path%/*}" || fail "mkdir for ${path} failed"
    cp -p "${store}/${path#"${records}/"}" "${copies}/${path}" || fail "cp ${path} failed"
    masked+=("${copies}/${path}")
done
if ((${#masked[@]})); then
    # U101: neither tool's output is shown. The masker prints each copy's path and, on a key collision, the original
    # keys; either may hold a redact word or a secret. Both go to files in the scratch directory (removed on exit),
    # and a failure says only that it happened and the exit status.
    status=0
    uv run --no-project python -I "${tools}/scripts/validate-agent-assets.py" --mask-secrets "${masked[@]}" \
        > "${scratch}/mask.log" 2>&1 || status=$?
    ((status == 0)) || fail "masking the copies failed (exit ${status}); its output is withheld, nothing was published"
    # U101: after masking, no copy may still name a secret, a home path or a redact word, its path included.
    scan=(--scan-identifiers)
    [[ -z ${words_real} ]] || scan+=(--redact-words "${words_real}")
    (cd "${copies}" && uv run --no-project python -I "${tools}/scripts/validate-agent-assets.py" "${scan[@]}" -- "${files[@]}") \
        > "${scratch}/scan.log" 2>&1 || status=$?
    ((status != 1)) ||
        refuse 'the identifier scan found a secret, a home path or a redact word in the masked copies (exit 1); its output is withheld, nothing was published'
    ((status == 0)) || fail "the identifier scan failed (exit ${status}); its output is withheld, nothing was published"
fi

# U101: the new tree is main's tree in a private index, the deletions removed first (a file that became a directory,
# or the reverse, frees its name), then each masked copy hashed with --no-filters and entered by mode and object id.
# The expected change set is computed alongside: every deletion, and every copy whose `<mode> blob <oid>` differs
# from its entry on main.
export GIT_INDEX_FILE=${scratch}/index
git_scratch read-tree "${main}" || fail 'git read-tree failed'
expected=${scratch}/expected
: > "${expected}" || fail 'cannot write the expected change set'
# A bare repository has no work tree, which `update-index --force-remove` asks for; an `--index-info` line of mode 0
# removes the path from the index without one. The zero object id has main's length (SHA-1 or SHA-256).
zero=${main//?/0}
for path in ${gone[@]+"${gone[@]}"}; do
    printf '0 %s\t%s\0' "${zero}" "${path}" | git_scratch update-index -z --index-info ||
        fail "git update-index removing ${path} failed"
    printf '%s\0' "${path}" >> "${expected}" || fail 'cannot write the expected change set'
done
for path in ${files[@]+"${files[@]}"}; do
    blob=$(git_scratch hash-object -w --no-filters -- "${copies}/${path}") || fail "git hash-object ${path} failed"
    mode=100644
    if [[ -x ${copies}/${path} ]]; then
        mode=100755
    fi
    git_scratch update-index --add --cacheinfo "${mode},${blob},${path}" || fail "git update-index ${path} failed"
    if [[ ${base_entries} != *$'\n'"${path}"$'\t'"${mode} blob ${blob}"$'\n'* ]]; then # lint-comparisons: allow a repository-relative path and an object id as git prints them
        printf '%s\0' "${path}" >> "${expected}" || fail 'cannot write the expected change set'
    fi
done
new_tree=$(git_scratch write-tree) || fail 'git write-tree failed'
unset GIT_INDEX_FILE
# U101: the tree's change against main must be exactly the computed set, as sorted NUL lists.
changed=${scratch}/changed
git_scratch diff-tree -r --no-renames --name-only -z "${main_tree}" "${new_tree}" > "${changed}" ||
    fail 'git diff-tree failed'
LC_ALL=C sort -z "${expected}" > "${expected}.sorted" || fail 'cannot sort the expected change set'
LC_ALL=C sort -z "${changed}" > "${changed}.sorted" || fail 'cannot sort the change set'
cmp -s "${expected}.sorted" "${changed}.sorted" ||
    refuse 'the new tree changes other paths than the copy set; nothing was committed or pushed'
[[ -s ${changed} ]] || refuse 'the copies equal origin/main; nothing to sync'
count=$(tr -cd '\000' < "${changed}" | wc -c) || fail 'cannot count the changed paths'
count=${count//[[:space:]]/}

remote_heads=$(git_scratch -c credential.helper= -c 'credential.helper=!gh auth git-credential' \
    ls-remote --heads "${push_url}" 'refs/heads/records/*') || fail 'git ls-remote origin failed'
# U28b F6: a local branch occupies its number too, whatever left it behind.
local_heads=$(git_isolated for-each-ref --format='%(refname)' 'refs/heads/records/') || fail 'git for-each-ref failed'
pr_heads=$(gh_plain pr list --state all --limit 1000 --json headRefName --jq '.[].headRefName') ||
    fail 'gh pr list failed'
last=$(printf '%s\n%s\n%s\n' "${remote_heads}" "${local_heads}" "${pr_heads}" |
    PROGRAM=${program} awk '{ ref = $NF; sub(/^refs\/heads\//, "", ref) }
        ref ~ "^records/(sync|program-store|" ENVIRON["PROGRAM"] "-sync)-[0-9]+$" { n = ref; sub(/.*-/, "", n); if (n + 0 > max) max = n + 0 }
        END { print max + 0 }') || fail 'cannot number the sync'
n=$((last + 1))
branch=records/sync-${n}
[[ ${branch} =~ ^records/sync-[1-9][0-9]*$ ]] || refuse "the branch is outside records/sync-<n>: ${branch}"

units=$(git_scratch diff --no-ext-diff --no-textconv -U0 "${main_tree}" "${new_tree}" -- "${records}/units.tsv" |
    sed -n -E 's/^\+(U[0-9]+[a-z]?)\t.*/\1/p' | sort -u | paste -sd ' ' -) || fail 'cannot list the units'
decisions=$(git_scratch diff --no-ext-diff --no-textconv -U0 "${main_tree}" "${new_tree}" -- "${records}/decisions.tsv" |
    sed -n -E 's/^\+([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z)\t.*/\1/p' | sort -u | paste -sd ' ' -) ||
    fail 'cannot list the decisions'
title="chore(records): ${program} sync ${n}"
message=$(printf '%s\n\n%s\n\n%s\n' "${title}" \
    "Carries ${count} file(s) of ${records}/ from the program store (${store_form} form), compared with origin/main (records-sync.sh)." \
    "${footer}") || fail 'cannot write the commit message'
# U101: author and committer come only from the environment set here, the identity read at the start.
commit=$(printf '%s\n' "${message}" |
    GIT_AUTHOR_NAME=${author_name} GIT_AUTHOR_EMAIL=${author_email} \
        GIT_COMMITTER_NAME=${author_name} GIT_COMMITTER_EMAIL=${author_email} \
        git_scratch commit-tree "${new_tree}" -p "${main}" -F -) || fail 'git commit-tree failed'
git_scratch -c credential.helper= -c 'credential.helper=!gh auth git-credential' \
    push --quiet "${push_url}" "${commit}:refs/heads/${branch}" || fail "git push ${branch} failed; nothing was opened"
body=${scratch}/body.md
# U220: the contract's first row names the store's form; the derived store's place is a home-directory path, which no
# published text names.
if [[ ${store_form} == derived ]]; then # lint-comparisons: allow the form name store_resolve set, not a path
    listed="the derived program store \`<store root>/${program}/\` (every regular file below it, \`redact-words.txt\` excluded; U220), published at \`.orchestration/orchestrate/${program}/\`"
else
    listed="\`.orchestration/orchestrate/${program}/\`, tracked or untracked and not git-ignored, \`redact-words.txt\` excluded"
fi
# U108: the `## Contract` section is what pr-audit.sh judges the pull request against (a body without one is
# refused), so every records sync gets an orchestrator verdict. Only the program name is interpolated.
# shellcheck disable=SC2016 # the backticks are Markdown code spans
contract=(
    "The changed paths are the store's files (${listed}) whose masked copy or executable mode differs from origin/main, plus every path origin/main holds under that directory that the listing does not hold as a regular file; the new tree's change set against origin/main is checked to equal exactly that set."
    'No path lies outside that directory.'
    'Every copy was masked with `validate-agent-assets.py --mask-secrets` and passed its `--scan-identifiers`, with the program'"'"'s `redact-words.txt` when present.'
    'The commit was built in a repository with no user, system or checkout configuration, and pushed over https with no user configuration.'
    'Left out: the content of the records is not reviewed for truth, only by the identifier scan.'
)
{
    # shellcheck disable=SC2016 # the backticks are Markdown code spans
    printf '## Summary\n\nRecords sync %s of `%s` (%s file(s)), carried by `records-sync.sh` from the program store (%s form) and compared with origin/main; every copy was masked with `validate-agent-assets.py --mask-secrets` and passed its `--scan-identifiers`.\n\n' "${n}" "${program}" "${count}" "${store_form}"
    printf -- '- units.tsv rows added or changed: %s\n' "${units:-none}"
    printf -- '- decisions.tsv rows added or changed: %s\n\n' "${decisions:-none}"
    printf '## Contract\n\n'
    printf -- '- %s\n' "${contract[@]}"
    printf '\nProgram-Unit: %s/%s\n\n' "${program}" "${unit}"
    printf '%s\n' "${pr_footer}"
} > "${body}" || fail 'cannot write the body'
url=$(gh_plain pr create --base main --head "${branch}" --title "${title}" --body-file "${body}") ||
    fail "gh pr create failed; the branch ${branch} is pushed"
echo "synced branch=${branch} files=${count} pr=${url}"
