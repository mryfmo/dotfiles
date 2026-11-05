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
#   `--ff` (regime-cutover U192) is the other direction, the step after a sync merged: the coordinator's checkout
#   fast-forwards `main` while its live store holds rows appended since the sync and files that differ from main
#   only by the sync's masking. It shares the self-check, the scrub, the main-checkout refusal, the program, the
#   scratch directory and the fetch of origin's main, then refuses (exit 2, nothing written) unless the branch is
#   `main`, no merge, rebase or cherry-pick is in progress, `HEAD` is an ancestor of the fetched main, and every path
#   the fast-forward touches outside the store is clean in the work tree and the index. Each touched store path is
#   classified by one table (classify): `untracked-equal` (untracked, its bytes or its masked bytes equal main's
#   blob: removed before the merge, which checks it out again), `clean` (tracked and unmodified, or absent locally:
#   nothing), `table-append` (`ledger.tsv`, `decisions.tsv` or `dispositions.tsv`, modified, main's N lines equal
#   to the first N masked local lines: main's N lines then the local tail), `units-local` (`units.tsv`, modified,
#   the header equal and every id of main's rows a local id: the local file), `once-adopt` (any other modified
#   file whose masked bytes equal main's blob: main's blob), and every other state refuses naming the path, the
#   class attempted and the first differing line. Only after every path is classified, a backup of every file to be
#   removed or replaced is made under the scratch directory, the `untracked-equal` files are removed, `checkout --`
#   discards the modified store files, `merge --ff-only` moves `HEAD` (a failure restores the backup, exit 1), the
#   resolved files are written, and the store is verified with the checkout's `ledger.py` (exit 0 or 1, never 2),
#   `rounds-check.py --all` (exit 0) and `diff --name-only HEAD` over the store listing exactly the `table-append`
#   and `units-local` paths; a failed verification restores the backup over the replaced files and exits 1 naming
#   the check (`HEAD` stays moved). The scratch directory is kept on exit 1 and named; nothing is stashed.
# @option --base <ref> The start point; only `origin/main` (the default) is accepted.
# @option --program <name> The program directory under `.orchestration/orchestrate/`; default: the only one.
# @option --unit <U<n>> The unit the body's `Program-Unit:` line names; default: U20, the records unit.
# @option --ff Fast-forward the main checkout past a merged sync (U192); with `--base` or `--unit` a usage refusal.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `synced branch=records/sync-<n> files=<n> pr=<url>`; with `--ff`, `fast-forwarded
#   from=<old head> to=<new head> removed=<n> appended=<n> adopted=<n> kept=<n>`, or `up to date head=<sha>`.
# @exitcode 0 The pull request was opened; with `--ff`, `HEAD` moved and the store verified, or nothing to do.
# @exitcode 1 A `git` or `gh` step, or the masking, failed; nothing was pushed unless the receipt says so. With
#   `--ff`: the checkout, the merge or a verification failed; the backup was restored and the scratch directory kept.
# @exitcode 2 Refused: usage, a linked worktree, the program, the copy set, the identifier scan, the identity, a
#   push URL that is not https, or nothing to sync; with `--ff`, the branch, a merge in progress, a local commit,
#   a dirty path outside the store, or a store path outside the table. Nothing was written.
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
keep_scratch=0
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

# @description Remove this run's scratch directory, with the repository the sync was built in. A `--ff` run that
#   exits 1 keeps it (keep_scratch): the backup it holds is what the coordinator reads next.
cleanup() {
    if [[ -n ${scratch:-} && -d ${scratch} ]]; then
        [[ ${keep_scratch} == 0 ]] || return 0
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

# @description Print the number of the first line at which two differing files differ: the first line whose text
#   differs, one past the shorter file's last line when it is a prefix of the other, or the last line when the two
#   differ in their final newline alone. awk counts: the levers' lint admits no arithmetic over a name in bash
#   itself (scripts/ci/producer-status-check.sh, ACCEPTED_ARITHMETIC).
# @arg $1 path One file.
# @arg $2 path The other.
differing_line() {
    if [[ ! -s $1 || ! -s $2 ]]; then
        echo 1
        return
    fi
    awk 'NR == FNR { a[NR] = $0; na = NR; next }
        { nb = FNR }
        FNR > na || a[FNR] != $0 { print FNR; done = 1; exit }
        END { if (!done) print (nb < na ? nb + 1 : nb) }' "$1" "$2"
}

# @description Classify one store path the fast-forward touches (U192) and print its class word: `untracked-equal`,
#   `clean`, `table-append`, `units-local` or `once-adopt`; every other state is a refusal naming the path, the class
#   attempted and the first differing line (exit 2, nothing written). Main's blob is `${scratch}/main/<path>`, the
#   masked local copy `${scratch}/masked/<path>` (both made by ff_run before the first call); a `table-append` or
#   `units-local` path leaves its resolved file at `${scratch}/resolved/<path>`.
# @arg $1 string The repository-relative store path.
# @arg $2 string Its diff-tree status against main (A, M or D).
classify() {
    local path=$1 status=$2 blob masked_copy resolved n start line last missing tracked=0 listed=0 index_status=0 tree_status=0
    blob=${scratch}/main/${path}
    masked_copy=${scratch}/masked/${path}
    resolved=${scratch}/resolved/${path}
    [[ ! -L ${path} ]] || refuse "${path}: a symlink stands at a store path the fast-forward touches"
    [[ ! -d ${path} ]] || refuse "${path}: a directory stands at a store path the fast-forward touches"
    [[ ! -e ${path} || -f ${path} ]] || refuse "${path}: not a regular file"
    # Tracked has three outcomes (standing order 21): the path listed, an empty listing, a listing that failed.
    read_listing "${scratch}/tracked" "${scratch}/tracked.err" git_isolated ls-files -z --cached -- "${path}" || listed=$?
    case ${listed} in
    0) tracked=1 ;;
    1) tracked=0 ;;
    *) fail "git ls-files ${path} failed" ;;
    esac
    if [[ ${tracked} == 0 ]]; then
        if [[ ! -e ${path} ]]; then
            echo clean
            return
        fi
        [[ -f ${blob} ]] || refuse "${path}: untracked-equal: main deletes the path and the checkout holds an untracked file at it"
        if cmp -s "${path}" "${blob}" || cmp -s "${masked_copy}" "${blob}"; then
            echo untracked-equal
            return
        fi
        line=$(differing_line "${masked_copy}" "${blob}") || fail "cannot compare ${path} with main's"
        refuse "${path}: untracked-equal: the untracked file differs from main's at line ${line} (after masking too); nothing was written"
    fi
    git_isolated diff --quiet --cached HEAD -- "${path}" || index_status=$?
    case ${index_status} in
    0) ;;
    1) refuse "${path}: clean: the index holds a staged change (no row of the table admits one); nothing was written" ;;
    *) fail "git diff --cached ${path} failed" ;;
    esac
    git_isolated diff --quiet HEAD -- "${path}" || tree_status=$?
    case ${tree_status} in
    0)
        echo clean
        return
        ;;
    1) ;;
    *) fail "git diff ${path} failed" ;;
    esac
    [[ -f ${path} ]] || refuse "${path}: clean: the tracked file is missing from the working tree; nothing was written"
    [[ ${status} != D ]] || refuse "${path}: once-adopt: main deletes a path the checkout modified (line 1); nothing was written"
    [[ -f ${blob} ]] || fail "no blob of ${path} was read from main"
    case ${path##*/} in # lint-comparisons: allow the store file's name selects its row of the table
    ledger.tsv | decisions.tsv | dispositions.tsv)
        [[ -s ${blob} ]] || refuse "${path}: table-append: main's file is empty (line 1); nothing was written"
        last=$(tail -c 1 "${blob}") || fail "cannot read ${path} of main"
        [[ -z ${last} ]] || refuse "${path}: table-append: main's last line has no newline end; nothing was written"
        # N and N+1 come from awk (no arithmetic over a name in bash, ACCEPTED_ARITHMETIC); a local file of fewer
        # than N lines differs from main's within the first N and is refused by the comparison below.
        n=$(awk 'END { print NR }' "${blob}") || fail "cannot count the lines of main's ${path}"
        start=$(awk 'END { print NR + 1 }' "${blob}") || fail "cannot count the lines of main's ${path}"
        head -n "${n}" "${masked_copy}" > "${scratch}/prefix" || fail "cannot read the first ${n} lines of ${path}"
        if ! cmp -s "${scratch}/prefix" "${blob}"; then
            line=$(differing_line "${scratch}/prefix" "${blob}") || fail "cannot compare ${path} with main's"
            refuse "${path}: table-append: line ${line} differs from main's (the first ${n} lines must equal main's after masking); nothing was written"
        fi
        mkdir -p "${resolved%/*}" || fail "cannot make the resolved directory of ${path}"
        { cat "${blob}" && tail -n +"${start}" "${path}"; } > "${resolved}" || fail "cannot write the resolved ${path}"
        echo table-append
        ;;
    units.tsv)
        [[ -s ${path} ]] || refuse "${path}: units-local: the local file is empty (line 1); nothing was written"
        head -n 1 "${blob}" > "${scratch}/header.main" || fail "cannot read the header of main's ${path}"
        head -n 1 "${path}" > "${scratch}/header.local" || fail "cannot read the header of ${path}"
        cmp -s "${scratch}/header.main" "${scratch}/header.local" ||
            refuse "${path}: units-local: line 1 (the header) differs from main's; nothing was written"
        # One awk pass over the two files: the first row of main whose id no local row carries, as `<line>TAB<id>`,
        # empty when every id is covered.
        missing=$(awk -F '\t' 'NR == FNR { if (FNR > 1) ids[$1] = 1; next } FNR > 1 && !($1 in ids) { print FNR "\t" $1; exit }' "${path}" "${blob}") ||
            fail "cannot read the ids of ${path}"
        [[ -z ${missing} ]] ||
            refuse "${path}: units-local: the id ${missing#*$'\t'} of main's line ${missing%%$'\t'*} has no local row; nothing was written"
        mkdir -p "${resolved%/*}" || fail "cannot make the resolved directory of ${path}"
        cp -p "${path}" "${resolved}" || fail "cannot copy ${path}"
        echo units-local
        ;;
    *)
        if cmp -s "${masked_copy}" "${blob}"; then
            echo once-adopt
            return
        fi
        line=$(differing_line "${masked_copy}" "${blob}") || fail "cannot compare ${path} with main's"
        refuse "${path}: once-adopt: the local file differs from main's beyond masking at line ${line}; nothing was written"
        ;;
    esac
}

# @description Copy each named backed-up file of the fast-forward back over its path, byte for byte.
# @arg $@ string The repository-relative paths.
ff_restore() {
    local path
    for path in "$@"; do
        mkdir -p "${path%/*}" && cp -p "${backup}/${path}" "${path}" ||
            echo "${lever}: could not restore ${path} from ${backup}" >&2
    done
}

# @description The write phase failed at a step before or at the merge: restore every backed-up file, keep the
#   scratch directory and exit 1 naming the step.
# @arg $1 string The step.
ff_step_failed() {
    keep_scratch=1
    ff_restore ${backed_up[@]+"${backed_up[@]}"}
    fail "$1 failed; the backup under ${backup} was restored over every file it holds; scratch kept at ${scratch}"
}

# @description A verification failed after the merge: restore the backup over every replaced store file (HEAD stays
#   moved), keep the scratch directory and exit 1 naming the check.
# @arg $1 string The check.
ff_verify_failed() {
    keep_scratch=1
    ff_restore ${replaced[@]+"${replaced[@]}"}
    fail "verification failed: $1; HEAD is ${new_head}, the backup under ${backup} was restored over the replaced store files; scratch kept at ${scratch}"
}

# @description The `--ff` mode (U192), entered after the shared setup fetched origin's main into the scratch
#   repository: the state refusals, the touched set, the classification of every touched store path, then the write
#   phase and the verification. Exits.
ff_run() {
    local branch head new_head python touched entry want status path word sorted dirty backup
    local entries=() masked=() removed=() replaced=() appended=() unit_rows=() adopted=() kept=() backed_up=()
    branch=$(git_isolated symbolic-ref --quiet --short HEAD 2> /dev/null) || refuse 'the checkout is not on a branch; --ff runs on main'
    [[ ${branch} == main ]] || refuse "the checkout is on ${branch}, not main; nothing was written"
    for path in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD; do
        [[ ! -e ${git_dir}/${path} ]] || refuse "a merge, rebase or cherry-pick is in progress (${git_dir}/${path}); nothing was written"
    done
    head=$(git_isolated rev-parse --verify 'HEAD^{commit}') || refuse 'cannot read HEAD'
    if [[ ${head} == "${main}" ]]; then
        echo "up to date head=${head}"
        exit 0
    fi
    python=$(command -v python3) || refuse 'no python3 found (it runs the verification, scripts/orchestrator/ledger.py and rounds-check.py)'
    # The fetched main reaches the checkout from the scratch repository (a local transport the lever opens for this
    # one command), never from the network again, so the ancestry test and the merge see the same commit.
    git_scratch update-ref refs/heads/main "${main}" || fail 'cannot name the fetched main in the scratch repository'
    git_isolated -c protocol.file.allow=always fetch --quiet --no-tags "${repo}" refs/heads/main ||
        fail 'cannot bring the fetched main into the checkout'
    git_isolated merge-base --is-ancestor "${head}" "${main}" ||
        refuse "HEAD ${head} is not an ancestor of origin's main ${main} (a local commit on main, or main behind); nothing was written"
    for path in scripts/orchestrator/ledger.py scripts/orchestrator/rounds-check.py; do
        git_scratch cat-file -e "${main}:${path}" 2> /dev/null || refuse "main holds no ${path}; the store cannot be verified after the merge, nothing was written"
    done
    touched=${scratch}/touched
    git_isolated diff-tree -r -z --no-renames --name-status "${head}" "${main}" > "${touched}" || fail 'git diff-tree failed'
    # The listing alternates a status letter and a path, each NUL-ended; the one `read` of the levers' accepted form
    # (ACCEPTED_WRITES of the lint names the `IFS= read` lines by text) takes them in turn. A store entry is kept as
    # `<letter>/<path>` (a letter holds no slash), so no array is indexed by a counter.
    want=status status='' entry=''
    while IFS= read -r -d '' entry; do
        if [[ ${want} == status ]]; then
            status=${entry}
            want=path
            continue
        fi
        want=status
        path=${entry}
        if [[ ${path} == "${records}"/* ]]; then # lint-comparisons: allow a repository-relative path as git prints it, under the store or not
            check_name "${path}"
            entries+=("${status}/${path}")
            continue
        fi
        dirty=$(git_isolated status --porcelain -- "${path}") || fail "git status ${path} failed"
        [[ -z ${dirty} ]] || refuse "${path} is not clean in the working tree or the index and the fast-forward changes it; resolve it by hand, nothing was written"
    done < "${touched}"
    [[ -z ${entry} && ${want} == status ]] || refuse 'the touched set ends mid-entry; nothing was written'
    make_tools
    mkdir -p "${scratch}/main" "${scratch}/masked" "${scratch}/resolved" || fail 'cannot make the scratch directories'
    for entry in ${entries[@]+"${entries[@]}"}; do
        status=${entry%%/*}
        path=${entry#*/}
        if [[ ${status} != D ]]; then
            mkdir -p "${scratch}/main/${path%/*}" || fail "cannot make the scratch directory of ${path}"
            git_scratch cat-file blob "${main}:${path}" > "${scratch}/main/${path}" || fail "cannot read ${path} of main"
        fi
        if [[ -f ${path} && ! -L ${path} ]]; then
            mkdir -p "${scratch}/masked/${path%/*}" || fail "cannot make the scratch directory of ${path}"
            cp -p "${path}" "${scratch}/masked/${path}" || fail "cp ${path} failed"
            masked+=("${scratch}/masked/${path}")
        fi
    done
    if [[ -n ${masked[*]:-} ]]; then
        status=0
        uv run --no-project python -I "${tools}/scripts/validate-agent-assets.py" --mask-secrets "${masked[@]}" \
            > "${scratch}/mask.log" 2>&1 || status=$?
        ((status == 0)) || fail "masking the local copies failed (exit ${status}); its output is withheld, nothing was written"
    fi
    for entry in ${entries[@]+"${entries[@]}"}; do
        path=${entry#*/}
        word=$(classify "${path}" "${entry%%/*}") || exit $?
        case ${word} in
        untracked-equal) removed+=("${path}") ;;
        clean) kept+=("${path}") ;;
        table-append) appended+=("${path}") replaced+=("${path}") ;;
        units-local) unit_rows+=("${path}") replaced+=("${path}") ;;
        once-adopt) adopted+=("${path}") replaced+=("${path}") ;;
        *) fail "classify printed no class word for ${path}" ;;
        esac
    done
    # The write phase: nothing above wrote into the checkout. Every file about to go is copied first.
    backup=${scratch}/backup
    for path in ${removed[@]+"${removed[@]}"} ${replaced[@]+"${replaced[@]}"}; do
        mkdir -p "${backup}/${path%/*}" || fail "cannot back up ${path}; nothing was written"
        cp -p "${path}" "${backup}/${path}" || fail "cannot back up ${path}; nothing was written"
        backed_up+=("${path}")
    done
    for path in ${removed[@]+"${removed[@]}"}; do
        rm "${path}" || ff_step_failed "removing ${path}"
    done
    if [[ -n ${replaced[*]:-} ]]; then
        git_isolated checkout -- "${replaced[@]}" || ff_step_failed 'git checkout --'
    fi
    git_isolated merge --quiet --ff-only "${main}" > "${scratch}/merge.log" 2>&1 || ff_step_failed 'git merge --ff-only'
    # A fast-forward-only merge of one commit leaves HEAD at that commit or fails, so the new head is the fetched
    # main; git is asked once more rather than trusted.
    new_head=${main}
    git_isolated merge-base --is-ancestor "${main}" HEAD || ff_step_failed 'the fast-forward (HEAD is not at the fetched main)'
    for path in ${appended[@]+"${appended[@]}"} ${unit_rows[@]+"${unit_rows[@]}"}; do
        cat "${scratch}/resolved/${path}" > "${path}" || ff_verify_failed "writing the resolved ${path}"
    done
    status=0
    "${python}" -I -S -B scripts/orchestrator/ledger.py "${records}" verdict 1 "${main//?/0}" > "${scratch}/ledger.log" 2>&1 || status=$?
    case ${status} in
    0 | 1) ;;
    *) ff_verify_failed "ledger.py exited ${status} (its output is in ${scratch}/ledger.log)" ;;
    esac
    status=0
    "${python}" -I -S -B scripts/orchestrator/rounds-check.py --all "${records}" > "${scratch}/rounds.log" 2>&1 || status=$?
    ((status == 0)) || ff_verify_failed "rounds-check.py --all exited ${status} (its output is in ${scratch}/rounds.log)"
    git_isolated diff --name-only -z HEAD -- "${records}/" > "${scratch}/changed" || ff_verify_failed 'git diff --name-only'
    : > "${scratch}/expected" || ff_verify_failed 'writing the expected change set'
    for path in ${appended[@]+"${appended[@]}"} ${unit_rows[@]+"${unit_rows[@]}"}; do
        printf '%s\0' "${path}" >> "${scratch}/expected" || ff_verify_failed 'writing the expected change set'
    done
    for sorted in changed expected; do
        LC_ALL=C sort -z "${scratch}/${sorted}" > "${scratch}/${sorted}.sorted" || ff_verify_failed "sorting the ${sorted} set"
    done
    cmp -s "${scratch}/changed.sorted" "${scratch}/expected.sorted" ||
        ff_verify_failed 'the store differs from HEAD at other paths than the table-append and units-local ones'
    echo "fast-forwarded from=${head} to=${new_head} removed=${#removed[@]} appended=${#appended[@]} adopted=${#adopted[@]} kept=${#kept[@]}"
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
