#!/usr/bin/env bash
# @file worker-worktree.sh
# @brief Create a worker's tree as a repository of its own that borrows the checkout's objects, with its push path removed: a worker tree cannot push.
# @description
#   Regime-cutover U123 (standing order 29: workers never push; the coordinator pushes). The order was text in the
#   first line of every TASK, and on 2026-10-30 six owners pushed anyway; the one stopped was the one whose push
#   route had no key. This lever makes the order a refusal of the tool. Run it from the main checkout:
#   `worker-worktree.sh <unit> <branch> <base>` makes `<root>/<unit>` (the root `$DOTFILES_WT` when set, else
#   `${TMPDIR:-/tmp}/dotfiles-wt`) as a fresh repository, not a linked worktree of the checkout (rounds 1 to 3
#   hardened `git worktree add` inside the checkout, and each audit found another channel of the checkout's
#   configuration that runs during creation: `post-checkout` hooks, `hook.<name>.event` hooks, a required smudge
#   filter, a locked tree; round 4 removes the linked worktree from the design). The fresh repository shares the
#   checkout's objects alone:
#   - `git init -q --template=` makes it with no template, under `GIT_CONFIG_GLOBAL=/dev/null` and
#     `GIT_CONFIG_NOSYSTEM=1`, the environment every git this lever runs inside the fresh repository has (`git_fresh`
#     below), so neither the operator's global configuration (a `core.hooksPath`, a `hook.<name>.event`, a
#     `filter.<name>.smudge`, an `init.templateDir`) nor the checkout's is read while the tree is made;
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
#     object is sent), `remote.pushDefault = origin` and `push.default = current` (a bare `git push` goes to the
#     refusal URL whatever the worker's global config says: a local value wins over a global one), and
#     `branch.<branch>.remote = origin`, `branch.<branch>.merge = refs/heads/<branch>`.
#   Nothing in the checkout changes at any point: its refs, config, hooks and `git worktree list` are the same after
#   a failed and after a successful run, and the worker tree is not in that list. The coordinator fetches the worker's
#   head by path and pushes it from the checkout: `git -C <checkout> fetch <repository> <branch> && git -C <checkout>
#   push <origin url> FETCH_HEAD:refs/heads/<branch>`, the line this lever prints.
#   Every input is checked before anything is made (exit 2, nothing created): the unit `U<n>` or `U<n><letter>`, a
#   branch `git check-ref-format --branch` accepts, taken as the normalized name it prints, over `[A-Za-z0-9._/-]`
#   (the shell reads nothing in the printed push line), a base that names a commit, the working directory a main
#   checkout (not a linked worktree) with an `origin` remote, and `<root>/<unit>` absent; an existing directory is
#   never touched. A read that fails before anything is made (`git rev-parse`, `git config`) is a refusal with exit
#   2, never an absence (standing order 21). When a step after `git init` fails, the repository this run made is
#   removed again (`rm -rf` of `<root>/<unit>`, a directory that was absent before and that only this lever wrote)
#   and the exit is 2 naming the step: no tree without the refusals is ever left, and nothing else is removed.
#   Every git this lever runs has `GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`, `GIT_DIR`,
#   `GIT_WORK_TREE` and `GIT_COMMON_DIR` removed from its environment (`git_direct`): the first redirects a config
#   write or read into another file, the next two add a config scope every read would see, and the last three point
#   every command at another repository.
#   Trusted: the worker is a non-adversarial actor whose reflex the refusals stop, not an attacker. A worker that
#   rewrites the fresh repository's config or hooks directory can restore the push path; the tree is the worker's,
#   and the refusal removes the path a push takes by habit, which is the failure that happened.
# @arg $1 string The unit, `U<n>` or `U<n><letter>` (`U7`, `U7b`); the repository is `<root>/<unit>`.
# @arg $2 string The branch to create: a name `git check-ref-format --branch` accepts (its normalized output is the
#   name made, so `@{-1}` names the checkout's previous branch), over `[A-Za-z0-9._/-]`.
# @arg $3 string The base, a revision the checkout resolves to a commit (`origin/main`).
# @env DOTFILES_WT The directory the worker trees live in (default `${TMPDIR:-/tmp}/dotfiles-wt`); made when absent.
# @stdout `worktree=<path>`, `branch=<branch>`, `head=<sha>` and `push=git -C <checkout> fetch <path> <branch> &&
#   git -C <checkout> push <origin url> FETCH_HEAD:refs/heads/<branch>`, the line the coordinator runs from the main
#   checkout, one per line; the paths and the URL are quoted for the shell (`printf %q`), the branch's character set
#   needs none.
# @exitcode 0 The repository exists at the base on the branch with the refusals and the upstream set.
# @exitcode 2 Refused: usage, a unit, branch or base outside the grammar, a working directory that is not the main
#   checkout or has no `origin`, the target path present, a read (`git rev-parse`, `git config`) that failed, or the
#   manifest pin differing from this file, each before anything is made; or a step after `git init` that failed,
#   after which the repository this run made is removed again and nothing else.
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

# @description Print a failed step on stderr and exit 2; the EXIT trap removes the repository this run made.
# @arg $@ string The reason.
fail() {
    echo "${lever}: refused: $*; the repository ${path} this run made is removed again" >&2
    exit 2
}

# @description Run git in the checkout with the environment names that would send it elsewhere removed: `GIT_CONFIG`
#   redirects a `git config` write or read into another file, `GIT_CONFIG_PARAMETERS` and `GIT_CONFIG_COUNT` add a
#   scope after every config file, and `GIT_DIR`, `GIT_WORK_TREE` and `GIT_COMMON_DIR` point every command at another
#   repository. The names are unset in a subshell that execs git, so the caller's environment stays as it was.
#   `git_env_scrub` of git-isolated.sh removes every `GIT_*` name, the operator's `GIT_CONFIG_GLOBAL`,
#   `GIT_SSH_COMMAND` and identity among them, which the reads in the operator's own checkout have no reason to drop;
#   so the six names are listed here.
# @arg $@ string git's arguments.
# @exitcode 2 A name cannot be removed (readonly).
# @exitcode * git's own status.
git_direct() {
    (
        unset -v GIT_CONFIG GIT_CONFIG_PARAMETERS GIT_CONFIG_COUNT GIT_DIR GIT_WORK_TREE GIT_COMMON_DIR || {
            echo "${lever}: refused: cannot remove GIT_CONFIG, GIT_CONFIG_PARAMETERS, GIT_CONFIG_COUNT, GIT_DIR, GIT_WORK_TREE or GIT_COMMON_DIR from git's environment" >&2
            exit 2
        }
        exec git "$@"
    )
}

# @description Run git inside the fresh repository: the six names of `git_direct` removed, and the global and system
#   configuration closed (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`), so that while the tree is made no
#   hook, filter, template or push setting of the operator's configuration is read; the fresh repository's own config,
#   which this lever writes before the fetch and the checkout, is the one git reads. The worker's later git reads the
#   worker's own configuration, under which the local values this lever wrote win.
# @arg $@ string git's arguments.
# @exitcode 2 A name cannot be removed (readonly).
# @exitcode * git's own status.
git_fresh() {
    (
        unset -v GIT_CONFIG GIT_CONFIG_PARAMETERS GIT_CONFIG_COUNT GIT_DIR GIT_WORK_TREE GIT_COMMON_DIR || {
            echo "${lever}: refused: cannot remove GIT_CONFIG, GIT_CONFIG_PARAMETERS, GIT_CONFIG_COUNT, GIT_DIR, GIT_WORK_TREE or GIT_COMMON_DIR from git's environment" >&2
            exit 2
        }
        export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
        exec git "$@"
    )
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
normalized=$(git_direct check-ref-format --branch "${branch}" 2> /dev/null) || refuse "the branch ${branch} is not a name git accepts"
branch=${normalized}
[[ ${branch} =~ ^[A-Za-z0-9._/-]+$ ]] || refuse "the branch ${branch} has a character outside [A-Za-z0-9._/-]"
[[ -n ${base} ]] || refuse "the base is empty"

toplevel=$(git_direct rev-parse --show-toplevel 2> /dev/null) || refuse 'run from the main checkout'
toplevel=$(cd "${toplevel}" && pwd -P) || refuse "cannot resolve ${toplevel}"
git_dir=$(git_direct rev-parse --path-format=absolute --git-dir 2> /dev/null) || refuse "cannot read the git directory of ${toplevel}"
common=$(git_direct rev-parse --path-format=absolute --git-common-dir 2> /dev/null) || refuse "cannot read the git common directory of ${toplevel}"
[[ ${git_dir} == "${common}" ]] || # lint-comparisons: allow both sides are git's absolute forms of one checkout
    refuse "${toplevel} is a linked worktree (git dir ${git_dir}, common ${common}); run from the main checkout"
objects=$(git_direct rev-parse --path-format=absolute --git-path objects 2> /dev/null) || refuse "cannot read the objects directory of ${toplevel}"
[[ -d ${objects} ]] || refuse "${objects} is not a directory"
# git config exits 1 for a key that is absent and otherwise for a read that failed (standing order 21): only 1 is absence.
status=0
origin_url=$(git_direct config --get remote.origin.url 2>&1) || status=$?
case ${status} in
0) ;;
1) refuse "no origin remote in ${toplevel}" ;;
*) refuse "cannot read remote.origin.url from the checkout's config: ${origin_url}" ;;
esac
base_sha=$(git_direct rev-parse --verify --quiet "${base}^{commit}" 2> /dev/null) || refuse "the base ${base} names no commit; run git fetch origin"
[[ ${base_sha} =~ ^[0-9a-f]{40,64}$ ]] || refuse "the base ${base} resolved to ${base_sha}, not an object name"

root=${DOTFILES_WT:-${TMPDIR:-/tmp}/dotfiles-wt}
[[ ${root} == /* ]] || refuse "DOTFILES_WT ${root} is not an absolute path" # lint-comparisons: allow a shape test (absolute or not), no path identity is compared
path=${root}/${unit}
[[ ! -e ${path} && ! -L ${path} ]] || refuse "${path} exists; an existing directory is never touched"

# @description Remove the repository this run made when a later step failed, so a tree without the refusals is never
#   left: `<root>/<unit>` was absent before this run and only this lever wrote under it, and nothing in the checkout
#   was written, so nothing else is removed. Runs on EXIT; a completed run has nothing to remove.
created=0
completed=0
cleanup() {
    [[ ${completed} == 0 && ${created} == 1 ]] || return 0
    rm -rf -- "${path}" || echo "${lever}: rm -rf ${path} failed; remove it by hand" >&2
}
trap cleanup EXIT

mkdir -p "${root}" || refuse "cannot make ${root}"
created=1
git_fresh init --quiet --template= "${path}" || fail "git init ${path} exited $?"
fresh_git=$(git_fresh -C "${path}" rev-parse --path-format=absolute --git-dir) || fail "cannot read the git directory of ${path}"
[[ -d ${fresh_git}/objects/info ]] || fail "${fresh_git}/objects/info is not a directory"
printf '%s\n' "${objects}" > "${fresh_git}/objects/info/alternates" || fail "cannot write ${fresh_git}/objects/info/alternates"
hooks=${fresh_git}/hooks-lever
mkdir "${hooks}" || fail "cannot make ${hooks}"
printf '#!/bin/sh\necho "%s" >&2\nexit 1\n' "${hook_message}" > "${hooks}/pre-push" || fail "cannot write ${hooks}/pre-push"
chmod 755 "${hooks}/pre-push" || fail "cannot make ${hooks}/pre-push executable"
# The refusals and the push shape are written before the fetch and the checkout, so the hooks directory git reads
# while the tree is made is this lever's own, holding `pre-push` alone.
git_fresh -C "${path}" config core.hooksPath "${hooks}" || fail "cannot set core.hooksPath in ${path}"
git_fresh -C "${path}" config remote.origin.url "${origin_url}" || fail "cannot set remote.origin.url in ${path}"
git_fresh -C "${path}" config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' || fail "cannot set remote.origin.fetch in ${path}"
git_fresh -C "${path}" config remote.origin.pushurl "${pushurl}" || fail "cannot set remote.origin.pushurl in ${path}"
git_fresh -C "${path}" config credential.helper '' || fail "cannot set credential.helper in ${path}"
git_fresh -C "${path}" config remote.pushDefault origin || fail "cannot set remote.pushDefault in ${path}"
git_fresh -C "${path}" config push.default current || fail "cannot set push.default in ${path}"
# The base by sha, from the checkout by path: the objects are already present through the alternates, so nothing is
# transferred, and the fresh repository gets the `origin/main` the workers' tests read.
git_fresh -C "${path}" fetch --quiet "${toplevel}" "${base_sha}:refs/remotes/origin/main" || fail "git fetch ${base_sha} from ${toplevel} exited $?"
git_fresh -C "${path}" checkout --quiet --no-track -b "${branch}" origin/main || fail "git checkout -b ${branch} origin/main in ${path} exited $?"
git_fresh -C "${path}" config "branch.${branch}.remote" origin || fail "cannot set branch.${branch}.remote in ${path}"
git_fresh -C "${path}" config "branch.${branch}.merge" "refs/heads/${branch}" || fail "cannot set branch.${branch}.merge in ${path}"
# The refusals are read back from the fresh repository's own config, so a value git wrote elsewhere never reads as set.
set_pushurl=$(git_fresh -C "${path}" config --get-all remote.origin.pushurl) || fail "remote.origin.pushurl is not set in ${path}"
[[ ${set_pushurl} == "${pushurl}" ]] || fail "remote.origin.pushurl in ${path} is ${set_pushurl//$'\n'/, }, not ${pushurl} alone"
set_hooks=$(git_fresh -C "${path}" config --get core.hooksPath) || fail "core.hooksPath is not set in ${path}"
[[ ${set_hooks} == "${hooks}" ]] || fail "core.hooksPath in ${path} is ${set_hooks}, not ${hooks}" # lint-comparisons: allow the value written above, read back
set_remote=$(git_fresh -C "${path}" config --get "branch.${branch}.remote") || fail "branch.${branch}.remote is not set in ${path}"
[[ ${set_remote} == origin ]] || fail "branch.${branch}.remote in ${path} is ${set_remote}, not origin"
set_merge=$(git_fresh -C "${path}" config --get "branch.${branch}.merge") || fail "branch.${branch}.merge is not set in ${path}"
[[ ${set_merge} == "refs/heads/${branch}" ]] || fail "branch.${branch}.merge in ${path} is ${set_merge}, not refs/heads/${branch}" # lint-comparisons: allow the value written above, read back
head=$(git_fresh -C "${path}" rev-parse --verify HEAD) || fail "cannot read the head of ${path}"
[[ ${head} == "${base_sha}" ]] || fail "the head of ${path} is ${head}, not the base ${base_sha}"
completed=1

printf 'worktree=%s\nbranch=%s\nhead=%s\n' "${path}" "${branch}" "${head}"
# The paths and the URL are quoted for the shell the coordinator pastes the line into; the branch's character set
# needs no quoting. The fetch by path brings the worker's head into the checkout, and FETCH_HEAD is what is pushed.
printf 'push=git -C %q fetch %q %s && git -C %q push %q FETCH_HEAD:refs/heads/%s\n' "${toplevel}" "${path}" "${branch}" "${toplevel}" "${origin_url}" "${branch}"
