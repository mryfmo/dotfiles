#!/usr/bin/env bash
# @file worker-worktree.sh
# @brief Create a worker's tree as a repository of its own that borrows the checkout's objects, with its push path removed: a worker tree cannot push.
# @description
#   Regime-cutover U123 (standing order 29: workers never push; the coordinator pushes). The order was text in the
#   first line of every TASK, and on 2026-10-30 six owners pushed anyway; the one stopped was the one whose push
#   route had no key. This lever makes the order a refusal of the tool. Run it from the main checkout:
#   `worker-worktree.sh <unit> <branch> <base>` makes `<root>/<unit>` (the root `$DOTFILES_WT` when set, else
#   `${TMPDIR:-/tmp}/dotfiles-wt`, resolved through its longest existing directory with `pwd -P`) as a fresh
#   repository, not a linked worktree of the checkout (rounds 1 to 3 hardened `git worktree add` inside the checkout,
#   and each audit found another channel of the checkout's configuration that runs during creation: `post-checkout`
#   hooks, `hook.<name>.event` hooks, a required smudge filter, a locked tree; round 4 removes the linked worktree from
#   the design). The fresh repository shares the checkout's objects alone:
#   - `git init -q --template=` makes it with no template, under `GIT_CONFIG_GLOBAL=/dev/null` and
#     `GIT_CONFIG_NOSYSTEM=1`, the environment every git this lever runs has (`git_run` below), so neither the
#     operator's global configuration (a `core.hooksPath`, a `hook.<name>.event`, a `filter.<name>.smudge`, an
#     `init.templateDir`) nor the checkout's is read while the tree is made;
#   - `objects/info/alternates` names the checkout's objects directory (`git rev-parse --git-path objects` there), so
#     the fetch below transfers nothing and a worker's commits are written into the fresh repository's own store;
#   - `git fetch <checkout> <base sha>:refs/remotes/origin/main`, the sha the checkout's `rev-parse --verify
#     <base>^{commit}` printed, gives the tree the `origin/main` the workers' tests read, and `git checkout --no-track
#     -b <branch> origin/main` makes the branch in the fresh repository: the checkout's own branches are never read or
#     written, so a branch of the same name in the checkout is no conflict;
#   - the fresh repository's own config then holds `remote.origin.url` (the checkout's, so `git fetch origin` works
#     and `origin/main` moves), `remote.origin.fetch` for `refs/heads/*`, `remote.origin.pushurl =
#     refused://never-push-from-a-worker-worktree` (so `git push`, `git push origin <ref>` and `git push -u origin
#     <branch>` fail on a remote helper that does not exist, before any remote is contacted), an empty
#     `credential.helper` (clears the helper list for an https push that spells the URL), `core.hooksPath =
#     <repository>/.git/hooks-lever` holding one `pre-push` hook that prints `standing order 29: the coordinator
#     pushes` and exits 1 (a push that spells any URL is refused after git has read the remote's refs and before any
#     object is sent), `branch.<branch>.remote = origin`, `branch.<branch>.merge = refs/heads/<branch>`, and the
#     three keys a bare `git push` resolves its remote from, in git's order (git-push(1)): `branch.<branch>.pushRemote
#     = origin`, then `remote.pushDefault = origin`, then `branch.<branch>.remote`, with `push.default = current`; all
#     are local values, and a local value wins over a global one, so a bare push goes to the refusal URL whatever the
#     worker's global config says (a global `branch.<branch>.pushRemote = upstream` included).
#   Nothing in the checkout changes at any point: its refs, config, hooks and `git worktree list` are the same after
#   a failed and after a successful run, and the worker tree is not in that list. The coordinator fetches the worker's
#   head by path and pushes it from the checkout: `git -C <checkout> fetch <repository> <branch> && git -C <checkout>
#   push <origin url> FETCH_HEAD:refs/heads/<branch>`, the line this lever prints.
#   Every input is checked before anything is made (exit 2, nothing created): the unit `U<n>` or `U<n><letter>`, a
#   branch `git check-ref-format --branch` accepts, taken as the normalized name it prints, over `[A-Za-z0-9._/-]`
#   (the shell reads nothing in the printed push line), a base that names a commit, the working directory a main
#   checkout (not a linked worktree) with an `origin` remote whose URL is absolute (`scheme://`, `[user@]host:` or
#   `/`-rooted: a relative URL copied into the fresh repository would resolve from there, not from the checkout; the
#   program's origin is https), the root absolute, without a `.` or `..` component, and, resolved through its longest
#   existing directory (`cd` and `pwd -P`), outside the checkout's working tree and git directory by identity: the
#   device and inode (`stat`) of that directory and of each directory above it, up to `/`, differ from the checkout's
#   and its git directory's, so no spelling of the checkout's path (a case alias on a case-insensitive volume, a
#   symlink, a trailing slash) names it without being it (`<checkout>/.git/hooks` is no root: a tree made there would
#   write the checkout; round 5 compared the resolved strings, and the audit made the tree through a case alias), and
#   neither the checkout's path nor the root holding a newline, each in its resolved form (a symlink whose name holds
#   none may point at a directory whose name holds one; the alternates file is one path per line); every path read
#   (`git rev-parse`'s and `pwd -P`'s) is captured exactly, a sentinel after the output keeping the trailing newline
#   `$(…)` would strip, so a directory named `trees<LF>` is never read as its newline-free sibling `trees` (round 2 of
#   U123b: the checks ran on the sibling and the tree was made under it). A read that fails
#   before anything is made (`git rev-parse`, `git config`, the resolver's `cd` and `pwd -P`, the `uname -s` that
#   chooses `stat`'s format flag, `stat` itself) is a refusal with exit 2, never an absence
#   (standing order 21). Then `mkdir <root>/<unit>` (no `-p`) reserves the target: success means this run owns the
#   directory and may remove it on failure; failure (a directory or symlink there, or mkdir's own error) is a refusal
#   that touched nothing, so two runs for one unit never both proceed and one run's cleanup never removes the other's
#   repository. When a step after the reservation fails, the directory this run reserved is removed again (`rm -rf`
#   of `<root>/<unit>`, which this run's mkdir made and only this lever wrote) and the exit is 2 naming the step: no
#   tree without the refusals is ever left, and nothing else is removed.
#   Every git this lever runs has every `GIT_*` name removed from its environment and the global and system
#   configuration closed (`git_run`): round 4 listed six names, and the audit found `GIT_INDEX_FILE`, which writes the
#   fresh repository's index into the checkout, and `GIT_OBJECT_DIRECTORY`, which names another objects directory for
#   the alternates; the names are subtracted by prefix, so no list of them can be short.
#   Trusted: the worker is a non-adversarial actor whose reflex the refusals stop, not an attacker. A worker that
#   rewrites the fresh repository's config or hooks directory can restore the push path; the tree is the worker's,
#   and the refusal removes the path a push takes by habit, which is the failure that happened.
# @arg $1 string The unit, `U<n>` or `U<n><letter>` (`U7`, `U7b`); the repository is `<root>/<unit>`.
# @arg $2 string The branch to create: a name `git check-ref-format --branch` accepts (its normalized output is the
#   name made, so `@{-1}` names the checkout's previous branch), over `[A-Za-z0-9._/-]`.
# @arg $3 string The base, a revision the checkout resolves to a commit (`origin/main`).
# @env DOTFILES_WT The directory the worker trees live in (default `${TMPDIR:-/tmp}/dotfiles-wt`): an absolute path
#   without `.` or `..` components or a newline, outside the checkout and its git directory by device and inode (its
#   longest existing directory and each directory above it); made when absent, and printed as `pwd -P` resolves it,
#   a resolved form holding a newline refused.
# @stdout `worktree=<path>`, `branch=<branch>`, `head=<sha>` and `push=git -C <checkout> fetch <path> <branch> &&
#   git -C <checkout> push <origin url> FETCH_HEAD:refs/heads/<branch>`, the line the coordinator runs from the main
#   checkout, one per line; the paths and the URL are quoted for the shell (`printf %q`), the branch's character set
#   needs none.
# @exitcode 0 The repository exists at the base on the branch with the refusals and the upstream set.
# @exitcode 2 Refused: usage, a unit, branch or base outside the grammar, a working directory that is not the main
#   checkout or has no `origin` or a relative origin URL, a root inside the checkout or its git directory by identity,
#   or holding a `.`, `..` or a newline (its resolved form included), a checkout path holding a newline, the target
#   path present (the reservation failed), a read (`git rev-parse`, `git config`, the resolver's `cd` and `pwd -P`,
#   `uname -s`, `stat`) that failed, or the manifest pin differing from this file, each before anything is made; or a
#   step after the reservation that failed, after which the directory this run made is removed again and nothing else.
# @example
#   ~/.local/bin/common/worker-worktree.sh U123 feat/refusals-not-sentences origin/main
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

lever='worker-worktree.sh'
usage='usage: worker-worktree.sh <unit> <branch> <base>'
pushurl='refused://never-push-from-a-worker-worktree'
hook_message='standing order 29: the coordinator pushes'
path=''

# @description Print a refusal on stderr and exit 2; nothing was made.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print a failed step on stderr and exit 2; the EXIT trap removes the directory this run reserved.
# @arg $@ string The reason.
fail() {
    echo "${lever}: refused: $*; the repository ${path} this run made is removed again" >&2
    exit 2
}

# @description Run git with every `GIT_*` name removed from its environment and the global and system configuration
#   closed (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`). The names are subtracted by prefix, not listed:
#   round 4 listed `GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`, `GIT_DIR`, `GIT_WORK_TREE` and
#   `GIT_COMMON_DIR`, and the audit of that round found `GIT_INDEX_FILE` (the fresh repository's index written into
#   the checkout, or the checkout's index reused, so the tree had no README) and `GIT_OBJECT_DIRECTORY` (another
#   objects directory named by `rev-parse --git-path objects`, so the alternates pointed elsewhere); every other
#   `GIT_*` name steers a read or a write too. `${!GIT_@}` is the shell's own list of the names, so no producer's
#   status is at stake, and the unset runs in a subshell that execs git, so the caller's environment stays as it was.
#   The closed configuration holds for the reads in the checkout as well: none of them needs the operator's global
#   config, and no `core.hooksPath`, `hook.<name>.event` or `filter.<name>.smudge` of it is read by any git this
#   lever runs.
# @arg $@ string git's arguments.
# @exitcode 2 A name cannot be removed (readonly).
# @exitcode * git's own status.
git_run() {
    (
        for name in "${!GIT_@}"; do
            unset -v "${name}" || {
                echo "${lever}: refused: cannot remove ${name} from git's environment" >&2
                exit 2
            }
        done
        export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
        exec git "$@"
    )
}

# @description Set `exact` to the standard output of the command $@, byte for byte apart from the one newline that
#   ends its line. `$(…)` strips every trailing newline, so `pwd -P` in a directory named `trees<LF>` read as the
#   newline-free sibling `trees`, and the newline check and the identity walk ran on the sibling while the tree was
#   made under it (round 2 of U123b). The command's output is followed by a sentinel `x`, which holds the newlines in
#   place; the sentinel and one newline are removed, and whatever is left of the name, a newline included, reaches the
#   checks. The result is a variable, not output, so no second substitution stands between the read and its reader.
# @arg $@ string The command; its stderr is the caller's.
# @set exact The output.
# @exitcode 1 The command failed.
exact_line() {
    exact=$("$@" && printf x) || return 1
    exact=${exact%x}
    exact=${exact%$'\n'}
}

# @description Print the physical path of the directory $1 (`cd` and `pwd -P`). Run inside `exact_line`'s
#   substitution, so the `cd` is a subshell's and the lever's own directory does not change.
# @arg $1 string A directory.
# @exitcode 1 The directory cannot be entered.
physical_path() {
    cd -- "$1" && pwd -P
}

# @description Resolve $1, an absolute path without `.` or `..` components that may not exist yet, through its longest
#   existing leading directory (`physical_path` through `exact_line`, so a symlink into the checkout is seen for what
#   it is and a trailing newline in the directory's name is kept): `root_prefix`
#   is that directory's physical path and `resolved_root` is it with the rest appended as given, the directories
#   `mkdir -p` would make. The results are variables, not output, so no producer stands between the resolution and its
#   readers, and the prefix is the first directory of the identity walk below.
# @arg $1 string The path.
# @set root_prefix The physical path of the longest existing leading directory.
# @set resolved_root The resolved path.
# @exitcode 1 The existing prefix cannot be entered (`cd` or `pwd -P` failed).
resolve_root() {
    local candidate=$1 rest=''
    while [[ ! -d ${candidate} ]]; do
        rest=${candidate##*/}${rest:+/${rest}}
        candidate=${candidate%/*}
        [[ -n ${candidate} ]] || candidate=/
    done
    exact_line physical_path "${candidate}" || return 1
    root_prefix=${exact}
    resolved_root=${root_prefix%/}${rest:+/${rest}}
    [[ -n ${resolved_root} ]] || resolved_root=/
}

# @description Print the device and inode of $1, one line `<device> <inode>`, as `stat` prints them with the format
#   flag `stat_args` chose for this system; a `stat` that fails or prints another shape is a failed read, never an
#   identity (standing order 21).
# @arg $1 string A path that exists.
# @exitcode 1 The read failed or printed something other than two decimals.
identity_of() {
    local id
    id=$(stat "${stat_args[@]}" -- "$1") || return 1
    [[ ${id} =~ ^[0-9]+' '[0-9]+$ ]] || return 1
    printf '%s\n' "${id}"
}

[[ $# == 3 ]] || refuse "${usage}"
unit=$1
branch=$2
base=$3
[[ ${unit} =~ ^U[0-9]+[a-z]?$ ]] || refuse "the unit ${unit} is not U<n> or U<n><letter>"
[[ -n ${branch} ]] || refuse "the branch is empty"
# check-ref-format --branch prints the name it accepts, normalized (`@{-1}` becomes the branch it denotes), and that
# name is the one made. The character set then excludes what a shell would read in the printed push line (`;`, a
# space, a quote), beyond what git accepts.
normalized=$(git_run check-ref-format --branch "${branch}" 2> /dev/null) || refuse "the branch ${branch} is not a name git accepts"
branch=${normalized}
[[ ${branch} =~ ^[A-Za-z0-9._/-]+$ ]] || refuse "the branch ${branch} has a character outside [A-Za-z0-9._/-]"
[[ -n ${base} ]] || refuse "the base is empty"

exact_line git_run rev-parse --show-toplevel 2> /dev/null || refuse 'run from the main checkout'
toplevel=${exact}
exact_line physical_path "${toplevel}" || refuse "cannot resolve ${toplevel}"
toplevel=${exact}
[[ ${toplevel} != *$'\n'* ]] || refuse "the checkout path ${toplevel//$'\n'/\\n} holds a newline; the alternates file is one path per line" # lint-comparisons: allow a shape test (a newline in the path), no path identity is compared
exact_line git_run rev-parse --path-format=absolute --git-dir 2> /dev/null || refuse "cannot read the git directory of ${toplevel}"
git_dir=${exact}
exact_line git_run rev-parse --path-format=absolute --git-common-dir 2> /dev/null || refuse "cannot read the git common directory of ${toplevel}"
common=${exact}
[[ ${git_dir} == "${common}" ]] || # lint-comparisons: allow both sides are git's absolute forms of one checkout
    refuse "${toplevel} is a linked worktree (git dir ${git_dir}, common ${common}); run from the main checkout"
exact_line physical_path "${git_dir}" || refuse "cannot resolve the git directory ${git_dir}"
git_dir=${exact}
exact_line git_run rev-parse --path-format=absolute --git-path objects 2> /dev/null || refuse "cannot read the objects directory of ${toplevel}"
objects=${exact}
[[ -d ${objects} ]] || refuse "${objects} is not a directory"
[[ ${objects} != *$'\n'* ]] || refuse "the objects directory ${objects//$'\n'/\\n} holds a newline; the alternates file is one path per line" # lint-comparisons: allow a shape test (a newline in the path), no path identity is compared
# git config exits 1 for a key that is absent and otherwise for a read that failed (standing order 21): only 1 is absence.
status=0
origin_url=$(git_run config --get remote.origin.url 2>&1) || status=$?
case ${status} in
0) ;;
1) refuse "no origin remote in ${toplevel}" ;;
*) refuse "cannot read remote.origin.url from the checkout's config: ${origin_url}" ;;
esac
# An absolute URL resolves the same from the fresh repository as from the checkout: a scheme (`https://`, `file://`),
# the scp-like `[user@]host:path` (no slash before the first colon, git-clone(1)), or a `/`-rooted path. A relative
# path (`../origin.git`) is relative to the repository git runs in, and copied into the fresh repository it names
# another place.
[[ ${origin_url} =~ ^([A-Za-z][A-Za-z0-9+.-]*://|[^/:]+:|/) ]] || # lint-comparisons: allow a shape test (absolute or relative), no URL identity is compared
    refuse "the origin URL ${origin_url} of ${toplevel} is not absolute (scheme://, [user@]host: or /-rooted); from the new repository it would name another place"
base_sha=$(git_run rev-parse --verify --quiet "${base}^{commit}" 2> /dev/null) || refuse "the base ${base} names no commit; run git fetch origin"
[[ ${base_sha} =~ ^[0-9a-f]{40,64}$ ]] || refuse "the base ${base} resolved to ${base_sha}, not an object name"

root=${DOTFILES_WT:-${TMPDIR:-/tmp}/dotfiles-wt}
[[ ${root} == /* ]] || refuse "DOTFILES_WT ${root} is not an absolute path" # lint-comparisons: allow a shape test (absolute or not), no path identity is compared
# A `.` or `..` component after the last existing directory would make `mkdir -p` land elsewhere than the resolved
# prefix says (`<tmp>/absent/../checkout`), so the root is taken without either.
[[ ${root} != */./* && ${root} != */../* && ${root} != */. && ${root} != */.. ]] || # lint-comparisons: allow a shape test (a . or .. component), no path identity is compared
    refuse "DOTFILES_WT ${root} has a . or .. component; give the resolved path"
[[ ${root} != *$'\n'* ]] || refuse "DOTFILES_WT ${root//$'\n'/\\n} holds a newline; the alternates file is one path per line" # lint-comparisons: allow a shape test (a newline in the path), no path identity is compared
resolve_root "${root}" || refuse "cannot resolve DOTFILES_WT ${root}; its longest existing directory cannot be entered"
root=${resolved_root}
# The resolved form is checked again: a symlink whose own name holds no newline may point at a directory whose name
# holds one, and the alternates file and the printed `worktree=` line are one path per line.
[[ ${root} != *$'\n'* ]] || refuse "DOTFILES_WT resolves to ${root//$'\n'/\\n}, which holds a newline; the alternates file is one path per line" # lint-comparisons: allow a shape test (a newline in the path), no path identity is compared
# A root inside the checkout's working tree or git directory (`<checkout>/.git/hooks`) would have the tree made
# write the checkout, which this lever never does. Containment is decided by identity, not by spelling: round 5
# compared the resolved strings, and on a case-insensitive volume a case alias of the checkout path
# (`<CHECKOUT>/.git/hooks`) was no prefix match, so the tree was made in the checkout's hooks directory. The device
# and inode of the root's longest existing directory and of each directory above it, up to `/`, are read with `stat`
# and compared with the checkout's and its git directory's; the components `mkdir -p` would make do not exist yet, so
# none of them is a directory of the checkout. `stat`'s format flag is `-f` on macOS and `-c` on Linux; the system
# name is read once, and a failed read refuses.
os=$(uname -s) || refuse 'cannot read the operating system name (uname -s)'
case ${os} in
Darwin) stat_args=(-f '%d %i') ;;
Linux) stat_args=(-c '%d %i') ;;
*) refuse "no identity read for the system ${os}; stat's format flag is known for Darwin and Linux" ;;
esac
checkout_id=$(identity_of "${toplevel}") || refuse "cannot read the identity (device and inode) of the checkout ${toplevel}"
git_dir_id=$(identity_of "${git_dir}") || refuse "cannot read the identity (device and inode) of the git directory ${git_dir}"
dir=${root_prefix}
while :; do
    dir_id=$(identity_of "${dir}") || refuse "cannot read the identity (device and inode) of ${dir}, which DOTFILES_WT ${root} lies under"
    [[ ${dir_id} != "${checkout_id}" && ${dir_id} != "${git_dir_id}" ]] || # lint-comparisons: allow compares (device, inode) identities, not paths
        refuse "DOTFILES_WT ${root} lies inside the checkout ${toplevel} or its git directory ${git_dir} (${dir} has the identity ${dir_id} of one of them); a worker tree is never made in the checkout"
    [[ ${dir} != / ]] || break # lint-comparisons: allow the walk ends at the filesystem root, a shape test; no path identity is compared
    dir=${dir%/*}
    [[ -n ${dir} ]] || dir=/
done
path=${root%/}/${unit}

# @description Remove the directory this run reserved when a later step failed, so a tree without the refusals is
#   never left: `<root>/<unit>` is the directory this run's own mkdir made (the reservation) and only this lever wrote
#   under it, and nothing in the checkout was written, so nothing else is removed. Runs on EXIT; a completed run has
#   nothing to remove, and a run whose reservation failed owns nothing.
created=0
completed=0
cleanup() {
    [[ ${completed} == 0 && ${created} == 1 ]] || return 0
    rm -rf -- "${path}" || echo "${lever}: rm -rf ${path} failed; remove it by hand" >&2
}
trap cleanup EXIT

mkdir -p -- "${root}" || refuse "cannot make ${root}"
# The reservation: `mkdir` without `-p` fails when anything is at the path (a directory, a file, a symlink dangling
# or not), so of two runs for one unit exactly one owns the directory, and the other refuses having touched nothing.
if ! reserve_error=$(mkdir -- "${path}" 2>&1); then
    [[ ! -e ${path} && ! -L ${path} ]] || refuse "${path} exists; an existing directory is never touched"
    refuse "cannot reserve ${path}: ${reserve_error}"
fi
created=1
git_run init --quiet --template= "${path}" || fail "git init ${path} exited $?"
fresh_git=$(git_run -C "${path}" rev-parse --path-format=absolute --git-dir) || fail "cannot read the git directory of ${path}"
[[ -d ${fresh_git}/objects/info ]] || fail "${fresh_git}/objects/info is not a directory"
printf '%s\n' "${objects}" > "${fresh_git}/objects/info/alternates" || fail "cannot write ${fresh_git}/objects/info/alternates"
hooks=${fresh_git}/hooks-lever
mkdir "${hooks}" || fail "cannot make ${hooks}"
printf '#!/bin/sh\necho "%s" >&2\nexit 1\n' "${hook_message}" > "${hooks}/pre-push" || fail "cannot write ${hooks}/pre-push"
chmod 755 "${hooks}/pre-push" || fail "cannot make ${hooks}/pre-push executable"
# The refusals and the push shape are written before the fetch and the checkout, so the hooks directory git reads
# while the tree is made is this lever's own, holding `pre-push` alone.
git_run -C "${path}" config core.hooksPath "${hooks}" || fail "cannot set core.hooksPath in ${path}"
git_run -C "${path}" config remote.origin.url "${origin_url}" || fail "cannot set remote.origin.url in ${path}"
git_run -C "${path}" config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' || fail "cannot set remote.origin.fetch in ${path}"
git_run -C "${path}" config remote.origin.pushurl "${pushurl}" || fail "cannot set remote.origin.pushurl in ${path}"
git_run -C "${path}" config credential.helper '' || fail "cannot set credential.helper in ${path}"
git_run -C "${path}" config remote.pushDefault origin || fail "cannot set remote.pushDefault in ${path}"
git_run -C "${path}" config push.default current || fail "cannot set push.default in ${path}"
# The base by sha, from the checkout by path: the objects are already present through the alternates, so nothing is
# transferred, and the fresh repository gets the `origin/main` the workers' tests read.
git_run -C "${path}" fetch --quiet "${toplevel}" "${base_sha}:refs/remotes/origin/main" || fail "git fetch ${base_sha} from ${toplevel} exited $?"
git_run -C "${path}" checkout --quiet --no-track -b "${branch}" origin/main || fail "git checkout -b ${branch} origin/main in ${path} exited $?"
git_run -C "${path}" config "branch.${branch}.remote" origin || fail "cannot set branch.${branch}.remote in ${path}"
git_run -C "${path}" config "branch.${branch}.merge" "refs/heads/${branch}" || fail "cannot set branch.${branch}.merge in ${path}"
# The first key git-push(1) resolves a bare push's remote from; a global `branch.<branch>.pushRemote` would otherwise
# stand before the local `remote.pushDefault`.
git_run -C "${path}" config "branch.${branch}.pushRemote" origin || fail "cannot set branch.${branch}.pushRemote in ${path}"
# The refusals are read back from the fresh repository's own config, so a value git wrote elsewhere never reads as set.
set_pushurl=$(git_run -C "${path}" config --get-all remote.origin.pushurl) || fail "remote.origin.pushurl is not set in ${path}"
[[ ${set_pushurl} == "${pushurl}" ]] || fail "remote.origin.pushurl in ${path} is ${set_pushurl//$'\n'/, }, not ${pushurl} alone"
set_hooks=$(git_run -C "${path}" config --get core.hooksPath) || fail "core.hooksPath is not set in ${path}"
[[ ${set_hooks} == "${hooks}" ]] || fail "core.hooksPath in ${path} is ${set_hooks}, not ${hooks}" # lint-comparisons: allow the value written above, read back
set_remote=$(git_run -C "${path}" config --get "branch.${branch}.remote") || fail "branch.${branch}.remote is not set in ${path}"
[[ ${set_remote} == origin ]] || fail "branch.${branch}.remote in ${path} is ${set_remote}, not origin"
set_merge=$(git_run -C "${path}" config --get "branch.${branch}.merge") || fail "branch.${branch}.merge is not set in ${path}"
[[ ${set_merge} == "refs/heads/${branch}" ]] || fail "branch.${branch}.merge in ${path} is ${set_merge}, not refs/heads/${branch}" # lint-comparisons: allow the value written above, read back
set_push_remote=$(git_run -C "${path}" config --get "branch.${branch}.pushRemote") || fail "branch.${branch}.pushRemote is not set in ${path}"
[[ ${set_push_remote} == origin ]] || fail "branch.${branch}.pushRemote in ${path} is ${set_push_remote}, not origin"
head=$(git_run -C "${path}" rev-parse --verify HEAD) || fail "cannot read the head of ${path}"
[[ ${head} == "${base_sha}" ]] || fail "the head of ${path} is ${head}, not the base ${base_sha}"
completed=1

printf 'worktree=%s\nbranch=%s\nhead=%s\n' "${path}" "${branch}" "${head}"
# The paths and the URL are quoted for the shell the coordinator pastes the line into; the branch's character set
# needs no quoting. The fetch by path brings the worker's head into the checkout, and FETCH_HEAD is what is pushed.
printf 'push=git -C %q fetch %q %s && git -C %q push %q FETCH_HEAD:refs/heads/%s\n' "${toplevel}" "${path}" "${branch}" "${toplevel}" "${origin_url}" "${branch}"
