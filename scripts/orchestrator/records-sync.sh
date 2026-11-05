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
#   `--ff` (regime-cutover U192; the form of U192b) is the other direction, the step after a sync merged: the
#   coordinator's checkout fast-forwards `main` while its live store holds rows appended since the sync and files that
#   differ from main only by the sync's masking. It shares the self-check, the scrub, the main-checkout refusal, the
#   program, the scratch directory and the fetch of origin's main, then refuses (exit 2, nothing written) unless the
#   branch is `main`, no merge, rebase or cherry-pick is in progress, `<git-dir>/info/grafts` is absent or empty and
#   no `refs/replace/*` ref exists (either would steer the ancestry statement), the index equals `HEAD` (or main's
#   tree: a rerun after a failed write), `HEAD` is an ancestor of the fetched main (`--no-replace-objects merge-base
#   --is-ancestor`; `up to date head=<sha>` when equal), the touched set (`diff-tree -r -z --name-status --no-renames`,
#   read to its end) holds only the statuses A, M, D and T, and every touched path outside the store has no symlink
#   component, is no symlink or directory, and is the clean tracked file or absent (`status --porcelain --ignored
#   --untracked-files=all` over the literal pathspec prints nothing; on a rerun, holds HEAD's or main's bytes by object
#   id). Then the writes, each one repeatable: `read-tree <main>` (the index alone), `checkout-index -f` for every
#   outside path main adds, changes or retypes, `rm` of every outside path main deletes (checked again as a regular
#   file or absent), and `update-ref refs/heads/main <main> <head>` last, so a failure before it leaves `HEAD` where it
#   was and exits 1 naming the step with the note that a rerun converges. Nothing inside the store is written, read
#   through a filter, masked, resolved, removed or backed up: the store's files keep their bytes and show as
#   modifications against main, which is exactly what the next sync publishes. The receipt is `fast-forwarded
#   from=<head> to=<main> outside=<n> store-modified=<n>`, the second count from `diff --name-only -z HEAD` over the
#   store. No stash, merge, checkout, reset or clean runs; the scratch directory is removed on every exit.
# @option --base <ref> The start point; only `origin/main` (the default) is accepted.
# @option --program <name> The program directory under `.orchestration/orchestrate/`; default: the only one.
# @option --unit <U<n>> The unit the body's `Program-Unit:` line names; default: U20, the records unit.
# @option --ff Fast-forward the main checkout past a merged sync (U192); with `--base` or `--unit` a usage refusal.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `synced branch=records/sync-<n> files=<n> pr=<url>`; with `--ff`, `fast-forwarded
#   from=<head> to=<main> outside=<n> store-modified=<n>`, or `up to date head=<sha>`.
# @exitcode 0 The pull request was opened; with `--ff`, `refs/heads/main` and the index are at main and the outside
#   paths hold main's content, or nothing to do.
# @exitcode 1 A `git` or `gh` step, or the masking, failed; nothing was pushed unless the receipt says so. With
#   `--ff`: a write failed before `refs/heads/main` moved (the step is named; a rerun converges), or only the
#   receipt's count could not be read after it moved.
# @exitcode 2 Refused: usage, a linked worktree, the program, the copy set, the identifier scan, the identity, a
#   push URL that is not https, or nothing to sync; with `--ff`, the branch, an operation in progress, grafts or
#   replace refs, a staged change, a local commit, a status outside A, M, D and T, or a touched path outside the
#   store that is not the clean tracked file. Nothing was written.
# @example
#   ~/.local/bin/common/records-sync.sh --program regime-cutover --unit U20
#   ~/.local/bin/common/records-sync.sh --ff --program regime-cutover
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

lever='records-sync.sh'
usage='usage: records-sync.sh [--base origin/main] [--program <name>] [--unit U<n> (default U20)] | records-sync.sh --ff [--program <name>]'
ff_resume=0
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

# @description Remove this run's scratch directory, with the repository the sync was built in, on every exit.
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

# @description Extract main's validator into a tools tree under the scratch directory: the masker and the scanner
#   are main's `scripts/validate-agent-assets.py`, alone in a tree whose `home/` holds main's top-level entry names
#   (empty), so its home-path pattern skips the repository's own `home/<entry>` paths as in a checkout; a main
#   without `home/` gives an empty one. Shared by the sync and `--ff`.
# @set tools The tools tree.
make_tools() {
    local entry
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
}

# @description Refuse a path the fast-forward changes outside the store unless the write can only put main's bytes
#   where HEAD's bytes (or nothing) stand (U192b). The name is checked first (a control character or `..`, as the sync
#   refuses them), then every directory component between the toplevel and the path must be no symlink (`rm` and
#   `checkout-index` through a linked directory would act outside the checkout), and the leaf no symlink and no
#   directory. On a first run the index equals HEAD, so `status --porcelain --ignored --untracked-files=all` over the
#   literal pathspec must print nothing: the path is the clean tracked file, or absent when main adds it (an ignored
#   file there is a write the operator did not ask for). On a rerun after a failed write (ff_resume) the index is
#   already main's and status cannot say "clean", so the file is compared by object id: absent is accepted for a path
#   main adds or deletes, and a regular file whose `hash-object` equals HEAD's or main's blob for it; anything else
#   is a refusal.
# @arg $1 string The repository-relative path, as `diff-tree` prints it.
# @arg $2 string Its status against main (A, M, D or T).
ff_check_outside() {
    local path=$1 kind=$2 prefix='' part rest dirty local_blob blob rev
    [[ ${path} != *[[:cntrl:]]* ]] || refuse 'a path the fast-forward changes holds a control character; nothing was written' # lint-comparisons: allow a character test on the raw git path
    [[ ${path} != *..* ]] || refuse "a path the fast-forward changes holds '..': ${path}; nothing was written"                # lint-comparisons: allow refuses a raw git path that holds ..
    rest=${path}
    while [[ ${rest} == */* ]]; do # lint-comparisons: allow splits the raw git path into its components
        part=${rest%%/*}
        rest=${rest#*/}
        prefix=${prefix:+${prefix}/}${part}
        [[ ! -L ${prefix} ]] || refuse "a component of ${path} is a symlink: ${prefix}; the fast-forward changes the path, nothing was written"
    done
    [[ ! -L ${path} ]] || refuse "a symlink stands at ${path}, which the fast-forward changes; resolve it by hand, nothing was written"
    [[ ! -d ${path} ]] || refuse "a directory stands at ${path}, which the fast-forward changes; resolve it by hand, nothing was written"
    if [[ ${ff_resume} == 0 ]]; then
        dirty=$(git_isolated --no-optional-locks status --porcelain --ignored --untracked-files=all -- ":(literal)${path}") ||
            fail "git status ${path} failed"
        [[ -z ${dirty} ]] ||
            refuse "${path} is not the clean tracked file (status '${dirty%%$'\n'*}') and the fast-forward changes it; resolve it by hand, nothing was written"
        return
    fi
    if [[ ! -e ${path} ]]; then
        case ${kind} in
        A | D) return ;;
        esac
        refuse "${path} is missing from the working tree and the fast-forward changes it; resolve it by hand, nothing was written"
    fi
    [[ -f ${path} ]] || refuse "${path} is not a regular file and the fast-forward changes it; resolve it by hand, nothing was written"
    local_blob=$(git_isolated hash-object -- "${path}") || fail "git hash-object ${path} failed"
    for rev in "${head}" "${main}"; do
        blob=$(git_isolated rev-parse --verify --quiet "${rev}:${path}") || blob='' # producer-status: allow a side that lacks the path has no blob, and the comparison below reads an empty one as unequal
        [[ ${local_blob} != "${blob}" ]] || return 0
    done
    refuse "${path} holds neither HEAD's nor main's bytes and the fast-forward changes it; resolve it by hand, nothing was written"
}

# @description A write of the fast-forward failed before `refs/heads/main` moved (`update-ref` is the last write):
#   exit 1 naming the step. The index and the outside paths written so far hold main's content, nothing of the store
#   was written, and a rerun of `--ff` converges: it reads the index as main's (ff_resume), accepts an outside file at
#   HEAD's or main's bytes, and repeats `read-tree`, `checkout-index -f` and the removals, each of which repeats
#   without harm.
# @arg $1 string The step.
ff_write_failed() {
    fail "$1 failed; refs/heads/main is still at ${head} and nothing of the store was written; rerun records-sync.sh --ff, which converges (read-tree, checkout-index -f and the removals repeat without harm)"
}

# @description The `--ff` mode (U192, the form of U192b), entered after the shared setup fetched origin's main into the
#   scratch repository. Every refusal comes before any write (exit 2): the branch, an operation in progress, grafts
#   and replace refs, the index, the ancestry, the touched set and each outside path (ff_check_outside). Then the
#   writes, each idempotent: `read-tree` puts main's tree in the index (the index alone: its `-m` form refuses a
#   working tree that differs from the index, which the store's files do), `checkout-index -f` writes each outside
#   path main adds, changes or retypes from that index, `rm` removes each one main deletes, and `update-ref` moves
#   `refs/heads/main` from the head checked to main as the last write, so a failure before it leaves HEAD where it
#   was and a rerun converges (ff_write_failed). No store path is named to any git command but the `diff
#   --name-only` that counts the receipt; the store's files keep their bytes and show as modifications against
#   main, the next sync's content. Exits.
ff_run() {
    local branch head status kind path entry want touched replaced
    local outside=() gone=() written=() modified=()
    branch=$(git_isolated symbolic-ref --quiet --short HEAD 2> /dev/null) || refuse 'the checkout is not on a branch; --ff runs on main'
    [[ ${branch} == main ]] || refuse "the checkout is on ${branch}, not main; nothing was written"
    for path in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD; do
        [[ ! -e ${git_dir}/${path} ]] || refuse "a merge, rebase or cherry-pick is in progress (${git_dir}/${path}); nothing was written"
    done
    # A grafts file or a replace ref rewrites ancestry for every command that reads it; the library's
    # --no-replace-objects covers the refs and nothing covers the file, so either is a refusal, not a trusted statement.
    [[ ! -s ${git_dir}/info/grafts ]] || refuse "${git_dir}/info/grafts is not empty and would steer the ancestry check; remove it, nothing was written"
    replaced=$(git_isolated for-each-ref --format='%(refname)' refs/replace) || fail 'git for-each-ref refs/replace failed'
    [[ -z ${replaced} ]] || refuse "the checkout holds a replace ref (${replaced%%$'\n'*}) that would steer the ancestry check; remove it, nothing was written"
    head=$(git_isolated rev-parse --verify 'HEAD^{commit}') || refuse 'cannot read HEAD'
    # The fetched main reaches the checkout from the scratch repository over a local transport opened for this one
    # command, never from the network again, into refs/remotes/origin/main: the index test, the ancestry test and the
    # writes see one commit, and the checkout guard's rule for a move of refs/heads/main (a commit origin/* reaches)
    # holds for the operator's later commands.
    git_scratch update-ref refs/heads/main "${main}" || fail 'cannot name the fetched main in the scratch repository'
    git_isolated -c protocol.file.allow=always fetch --quiet --no-tags "${repo}" '+refs/heads/main:refs/remotes/origin/main' ||
        fail 'cannot bring the fetched main into the checkout'
    # The index must be HEAD's tree, or already main's: the read-tree of a run whose later write failed leaves it so,
    # and that run is resumed (ff_check_outside then reads the files by object id). Anything else is a staged change.
    status=0
    git_isolated diff --cached --quiet HEAD || status=$?
    case ${status} in
    0) ;;
    1)
        status=0
        git_isolated diff --cached --quiet "${main}" || status=$?
        case ${status} in
        0) ff_resume=1 ;;
        1) refuse 'the index differs from HEAD (a staged change); resolve it by hand, nothing was written' ;;
        *) fail 'git diff --cached failed' ;;
        esac
        ;;
    *) fail 'git diff --cached failed' ;;
    esac
    status=0
    git_isolated merge-base --is-ancestor "${head}" "${main}" || status=$?
    case ${status} in
    0) ;;
    1) refuse "HEAD ${head} is not an ancestor of origin's main ${main} (a local commit on main, or main behind); nothing was written" ;;
    *) fail 'git merge-base --is-ancestor failed' ;;
    esac
    touched=${scratch}/touched
    git_isolated diff-tree -r -z --name-status --no-renames "${head}" "${main}" > "${touched}" || fail 'git diff-tree failed'
    # The listing alternates a status letter and a path, each NUL-ended; the one accepted `read` of the levers takes
    # them in turn, and a listing that ends mid-entry is refused before any write.
    want=status kind='' entry=''
    while IFS= read -r -d '' entry; do
        if [[ ${want} == status ]]; then
            kind=${entry}
            want=path
            continue
        fi
        want=status
        path=${entry}
        case ${kind} in
        A | M | D | T) ;;
        *) refuse "the touched set holds a status outside A, M, D and T (${kind} ${path}); nothing was written" ;;
        esac
        if [[ ${path} == "${records}"/* ]]; then # lint-comparisons: allow a repository-relative path as git prints it, under the store or not
            continue
        fi
        ff_check_outside "${path}" "${kind}"
        outside+=("${path}")
        if [[ ${kind} == D ]]; then
            gone+=("${path}")
        else
            written+=("${path}")
        fi
    done < "${touched}"
    [[ -z ${entry} && ${want} == status ]] || refuse 'the touched set ends mid-entry; nothing was written'
    if [[ ${head} == "${main}" ]]; then
        echo "up to date head=${head}"
        exit 0
    fi
    # The writes, in the order a rerun repeats them; no store path is named to any of them.
    git_isolated read-tree "${main}" || ff_write_failed 'git read-tree'
    for path in ${written[@]+"${written[@]}"}; do
        # checkout-index takes file names, not pathspecs (measured: a `:(literal)` prefix is read as part of the
        # name), so the path as diff-tree printed it names one index entry and a `*` in it matches no sibling.
        git_isolated checkout-index -f -- "${path}" || ff_write_failed "git checkout-index ${path}"
    done
    for path in ${gone[@]+"${gone[@]}"}; do
        if [[ ! -e ${path} && ! -L ${path} ]]; then
            continue
        fi
        [[ -f ${path} && ! -L ${path} ]] || ff_write_failed "removing ${path} (not a regular file any more)"
        rm -- "${path}" || ff_write_failed "removing ${path}"
    done
    git_isolated update-ref -m 'records-sync.sh --ff' refs/heads/main "${main}" "${head}" ||
        ff_write_failed 'git update-ref refs/heads/main'
    git_isolated diff --name-only -z HEAD -- ":(literal)${records}" > "${scratch}/modified" ||
        fail "git diff --name-only failed; the fast-forward is complete (HEAD is ${main}), only the receipt's count was not read"
    path=''
    while IFS= read -r -d '' path; do
        modified+=("${path}")
    done < "${scratch}/modified"
    [[ -z ${path} ]] || fail "the store listing ends mid-entry; the fast-forward is complete (HEAD is ${main}), only the receipt's count was not read"
    echo "fast-forwarded from=${head} to=${main} outside=${#outside[@]} store-modified=${#modified[@]}"
    exit 0
}

base=origin/main
program=''
unit=U20
ff=0
sync_only=''
while (($#)); do
    case $1 in
    --ff)
        ff=1
        shift
        ;;
    --base | --program | --unit)
        (($# >= 2)) || refuse "${usage}"
        case $1 in
        --base) base=$2 sync_only=$1 ;;
        --program) program=$2 ;;
        --unit) unit=$2 sync_only=$1 ;;
        esac
        shift 2
        ;;
    *) refuse "${usage}" ;;
    esac
done
[[ ${ff} == 0 || -z ${sync_only} ]] || refuse "${usage}"
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
    words_real=$(cd "${records}" && pwd -P) || refuse "cannot resolve ${words}"
    words_real=${words_real}/redact-words.txt
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
if [[ ${ff} == 1 ]]; then
    ff_run
fi
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
read_listing "${scratch}/dirs" "${scratch}/walk.err" find "${records}" -type d -print0 ||
    refuse "a directory under ${records}/ cannot be read or entered; nothing was created"
dir=''
while IFS= read -r -d '' dir; do
    [[ -r ${dir} && -x ${dir} ]] || refuse "a directory under ${records}/ cannot be read or entered; nothing was created"
done < "${scratch}/dirs"
[[ -z ${dir} ]] || refuse "the walk of ${records}/ ends mid-entry; nothing was created"
# Audit of 7b3c2718: the listing is the one index read in the checkout, and a `core.fsmonitor` hook set in any
# configuration the checkout reads would run inside it (and could write into the store before the copy). The isolated
# git turns it off, with the hooks path and the user and system files; the repository level has no off switch, so the
# checkout's own ignore rules and the default ignore file still shape the listing, which the stderr test below bounds.
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

make_tools
# U101: the copies are masked and scanned in the scratch directory, and these same files are what hash-object
# writes, so the committed bytes are the scanned bytes.
copies=${scratch}/copies
masked=()
for path in ${files[@]+"${files[@]}"}; do
    mkdir -p "${copies}/${path%/*}" || fail "mkdir for ${path} failed"
    cp -p "${path}" "${copies}/${path}" || fail "cp ${path} failed"
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
    "Carries ${count} file(s) of ${records}/ from the main checkout, compared with origin/main (records-sync.sh)." \
    "${footer}") || fail 'cannot write the commit message'
# U101: author and committer come only from the environment set here, the identity read at the start.
commit=$(printf '%s\n' "${message}" |
    GIT_AUTHOR_NAME=${author_name} GIT_AUTHOR_EMAIL=${author_email} \
        GIT_COMMITTER_NAME=${author_name} GIT_COMMITTER_EMAIL=${author_email} \
        git_scratch commit-tree "${new_tree}" -p "${main}" -F -) || fail 'git commit-tree failed'
git_scratch -c credential.helper= -c 'credential.helper=!gh auth git-credential' \
    push --quiet "${push_url}" "${commit}:refs/heads/${branch}" || fail "git push ${branch} failed; nothing was opened"
body=${scratch}/body.md
# U108: the `## Contract` section is what pr-audit.sh judges the pull request against (a body without one is
# refused), so every records sync gets an orchestrator verdict. Only the program name is interpolated.
# shellcheck disable=SC2016 # the backticks are Markdown code spans
contract=(
    "The changed paths are the store's files (\`.orchestration/orchestrate/${program}/\`, tracked or untracked and not git-ignored, \`redact-words.txt\` excluded) whose masked copy or executable mode differs from origin/main, plus every path origin/main holds under that directory that the listing does not hold as a regular file; the new tree's change set against origin/main is checked to equal exactly that set."
    'No path lies outside that directory.'
    'Every copy was masked with `validate-agent-assets.py --mask-secrets` and passed its `--scan-identifiers`, with the program'"'"'s `redact-words.txt` when present.'
    'The commit was built in a repository with no user, system or checkout configuration, and pushed over https with no user configuration.'
    'Left out: the content of the records is not reviewed for truth, only by the identifier scan.'
)
{
    # shellcheck disable=SC2016 # the backticks are Markdown code spans
    printf '## Summary\n\nRecords sync %s of `%s` (%s file(s)), carried by `records-sync.sh` from the main checkout and compared with origin/main; every copy was masked with `validate-agent-assets.py --mask-secrets` and passed its `--scan-identifiers`.\n\n' "${n}" "${program}" "${count}"
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
