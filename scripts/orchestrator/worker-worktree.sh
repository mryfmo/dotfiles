#!/usr/bin/env bash
# @file worker-worktree.sh
# @brief Create a worker's worktree from the main checkout with its push path removed: a worker worktree cannot push.
# @description
#   Regime-cutover U123 (standing order 29: workers never push; the coordinator pushes). The order was text in the
#   first line of every TASK, and on 2026-10-30 six owners pushed anyway; the one stopped was the one whose push
#   route had no key. This lever makes the order a refusal of the tool. Run it from the main checkout:
#   `worker-worktree.sh <unit> <branch> <base>` runs `git worktree add --no-track -b <branch> <root>/<unit> <base>`,
#   the root being `$DOTFILES_WT` when set, else `${TMPDIR:-/tmp}/dotfiles-wt`, and then, in that worktree's own
#   configuration only (`git config --worktree`, which needs `extensions.worktreeConfig`, set to true in the
#   checkout's config when it is not yet; `core.worktree` set there is refused, since a linked worktree would read it
#   once the extension is on):
#   - `remote.origin.pushurl` is `refused://never-push-from-a-worker-worktree`, so `git push`, `git push origin
#     <ref>` and `git push -u origin <branch>` fail on a remote helper that does not exist, before any ref leaves;
#   - `credential.helper` is the empty string, which clears the helper list for an https push that spells the URL
#     (the operator's `gh auth git-credential` is global, and a worktree-local empty value clears it in that tree);
#   - `core.hooksPath` is `<worktree git dir>/hooks`, a directory of this lever's own holding one `pre-push` hook
#     that prints `standing order 29: the coordinator pushes` and exits 1, so a push that spells any URL is refused
#     after git has read the remote's refs and before any object is sent;
#   - `branch.<branch>.remote` is `origin` and `branch.<branch>.merge` is `refs/heads/<branch>` (the add runs with
#     `--no-track`, so the checkout's config gets no upstream for the branch), so a bare `git push` under
#     `push.default` simple reaches the refusal URL instead of stopping on its own upstream message.
#   No hook of the source checkout runs while the worktree is made: the hooks directory is made first, empty, under
#   the checkout's git directory, `git worktree add` runs with `-c core.hooksPath=<that directory>` (a
#   `post-checkout` or `reference-transaction` hook of the checkout, one that locks the new tree, writes into it or
#   exits 1, never runs), and the directory is then moved under the worktree's git directory and the `pre-push` hook
#   written into it. Every git this lever runs has `GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`,
#   `GIT_DIR`, `GIT_WORK_TREE` and `GIT_COMMON_DIR` removed from its environment (`git_direct` below): the first would
#   send the `extensions.worktreeConfig` write into another file, the next two add a config scope every read would
#   see, and the last three point every command at another repository.
#   The main checkout and every other worktree keep their configuration: `config.worktree` is read by its own
#   worktree alone, and the hooks directory lies under that worktree's git directory. The coordinator therefore pushes
#   the worker's head from the main checkout, whose objects the worktree shares: `git -C <toplevel> push <origin url>
#   <head>:refs/heads/<branch>`, the line this lever prints with the worktree's path, branch and head.
#   Every input is checked before anything is made (exit 2, nothing created): the unit `U<n>` or `U<n><letter>`, a
#   branch `git check-ref-format --branch` accepts, taken as the normalized name it prints, over `[A-Za-z0-9._/-]`
#   (the shell reads nothing in the printed push line) and not yet a local branch, a base that names a commit, the
#   working directory a main checkout (not a linked worktree) with an `origin` remote whose `pushurl` no scope sets
#   (git pushes to every pushurl of a remote, and the worktree's scope cannot shadow one), and `<root>/<unit>` absent;
#   an existing worktree is never touched. A read that fails before anything is made (`git rev-parse`, `git
#   show-ref`, `git config`) is a refusal with exit 2, never an absence (standing order 21). When a step after `git
#   worktree add` fails, the tree and the branch this run made are removed again (`git worktree remove --force`, `git
#   branch -D`, on the lever's own fresh tree only; a `show-ref` that fails there is said so and the branch deleted
#   all the same), and the empty hooks directory is removed when it was not yet moved, so a worktree without the
#   refusals is never left behind: exit 1 names the step. An add that exits non-zero made nothing: with no hook
#   running, git removes its own partial tree.
#   Trusted: the worker is a non-adversarial actor whose reflex the refusals stop, not an attacker. A worker that
#   rewrites its own `config.worktree` or hooks directory can restore the push path; the worktree is the worker's,
#   and the refusal removes the path a push takes by habit, which is the failure that happened.
# @arg $1 string The unit, `U<n>` or `U<n><letter>` (`U7`, `U7b`); the worktree is `<root>/<unit>`.
# @arg $2 string The branch to create: a name `git check-ref-format --branch` accepts (its normalized output is the
#   name made, so `@{-1}` names the previous branch), over `[A-Za-z0-9._/-]`, not yet a local branch.
# @arg $3 string The base, a revision naming a commit (`origin/main`).
# @env DOTFILES_WT The directory the worktrees live in (default `${TMPDIR:-/tmp}/dotfiles-wt`); made when absent.
# @stdout `worktree=<path>`, `branch=<branch>`, `head=<sha>` and `push=git -C <toplevel> push <origin url>
#   <head>:refs/heads/<branch>`, the line the coordinator runs from the main checkout after replacing `<head>`, one
#   per line; the path and the URL are quoted for the shell (`printf %q`), the branch's character set needs none.
# @exitcode 0 The worktree exists at the base on the branch with the refusals and the upstream set.
# @exitcode 1 A git step after the checks failed; what this run made was removed again, and the message names the
#   step.
# @exitcode 2 Refused before anything was made: usage, a unit, branch or base outside the grammar, a branch that
#   exists, a working directory that is not the main checkout or has no `origin`, `core.worktree` or
#   `remote.origin.pushurl` set in a scope the worktree would read, the target path present, a read (`git rev-parse`,
#   `git show-ref`, `git config`) that failed, or the manifest pin differing from this file.
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

# @description Print a refusal on stderr and exit 2; nothing was made.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print a failure on stderr and exit 1; the EXIT trap removes what this run made.
# @arg $@ string The reason.
fail() {
    echo "${lever}: $*" >&2
    exit 1
}

# @description Run git with the environment names that would send it elsewhere removed: `GIT_CONFIG` redirects a
#   `git config` write or read into another file, `GIT_CONFIG_PARAMETERS` and `GIT_CONFIG_COUNT` add a scope after
#   every config file, and `GIT_DIR`, `GIT_WORK_TREE` and `GIT_COMMON_DIR` point every command at another repository.
#   The names are unset in a subshell that execs git, so the caller's environment stays as it was. `git_env_scrub` of
#   git-isolated.sh removes every `GIT_*` name, the operator's `GIT_CONFIG_GLOBAL`, `GIT_SSH_COMMAND` and identity
#   among them, which this lever, run in the operator's own checkout, has no reason to drop; so the six names are
#   listed here.
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

[[ $# == 3 ]] || refuse "${usage}"
unit=$1
branch=$2
base=$3
[[ ${unit} =~ ^U[0-9]+[a-z]?$ ]] || refuse "the unit ${unit} is not U<n> or U<n><letter>"
[[ -n ${branch} ]] || refuse "the branch is empty"
# check-ref-format --branch prints the name it accepts, normalized (`@{-1}` becomes the branch it denotes), and that
# name is the one checked for existence and made. The character set then excludes what a shell would read in the
# printed push line (`;`, a space, a quote), beyond what git accepts.
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
[[ -d ${common}/objects ]] || refuse "${common} holds no objects directory"
origin_url=$(git_direct remote get-url origin 2> /dev/null) || refuse "no origin remote in ${toplevel}"
git_direct rev-parse --verify --quiet "${base}^{commit}" > /dev/null || refuse "the base ${base} names no commit; run git fetch origin"
# show-ref exits 1 for a ref that is absent and otherwise for a read that failed (standing order 21): only 1 is absence.
status=0
git_direct show-ref --verify --quiet "refs/heads/${branch}" || status=$?
case ${status} in
0) refuse "the branch ${branch} exists; a unit's branch is new" ;;
1) ;;
*) refuse "cannot read refs/heads/${branch} in ${toplevel}: git show-ref exited ${status}" ;;
esac
# A pushurl in any scope the worktree reads (the checkout's config, the global one) stays active beside the refusal
# URL, since git pushes to every pushurl of a remote and a worktree scope cannot shadow one, so it is refused.
status=0
inherited_pushurl=$(git_direct config --get-all remote.origin.pushurl 2>&1) || status=$?
case ${status} in
0) refuse "remote.origin.pushurl is set in the checkout's config (${inherited_pushurl//$'\n'/, }); a worktree reads it beside the refusal URL, so unset it before a worker worktree is made" ;;
1) ;;
*) refuse "cannot read remote.origin.pushurl from the checkout's config: ${inherited_pushurl}" ;;
esac
# core.worktree in the common config would be read by every linked worktree once extensions.worktreeConfig is on
# (git-worktree(1), CONFIGURATION FILE), so it is refused rather than moved.
status=0
core_worktree=$(git_direct config --get core.worktree 2>&1) || status=$?
case ${status} in
0) refuse "core.worktree is set in the checkout's config (${core_worktree}); unset it before a worker worktree is made" ;;
1) ;;
*) refuse "cannot read core.worktree from the checkout's config: ${core_worktree}" ;;
esac

root=${DOTFILES_WT:-${TMPDIR:-/tmp}/dotfiles-wt}
[[ ${root} == /* ]] || refuse "DOTFILES_WT ${root} is not an absolute path" # lint-comparisons: allow a shape test (absolute or not), no path identity is compared
path=${root}/${unit}
[[ ! -e ${path} && ! -L ${path} ]] || refuse "${path} exists; an existing worktree is never touched"

# @description Remove what this run made when a later step failed, so a worktree without the refusals is never left:
#   the empty hooks directory when it was not yet moved under the worktree's git directory, then the tree and the
#   branch (`git worktree add` made both at once; an add that failed made nothing, since no hook ran and git removes
#   its own partial tree). Runs on EXIT; a completed run has nothing to remove. The `show-ref` read of the branch is by
#   value: 1 is absence, 0 presence, and anything else is said so and the branch deleted all the same, this run made it.
created=0
completed=0
staging=''
cleanup() {
    local status
    [[ ${completed} == 0 ]] || return 0
    if [[ -n ${staging} && -d ${staging} ]]; then
        rmdir "${staging}" || echo "${lever}: rmdir ${staging} failed; remove it by hand" >&2
    fi
    [[ ${created} == 1 ]] || return 0
    echo "${lever}: removing the half-made worktree ${path} and the branch ${branch}" >&2
    if [[ -e ${path} || -L ${path} ]]; then
        git_direct -C "${toplevel}" worktree remove --force "${path}" ||
            echo "${lever}: git worktree remove ${path} failed; remove it by hand" >&2
    fi
    status=0
    git_direct -C "${toplevel}" show-ref --verify --quiet "refs/heads/${branch}" || status=$?
    case ${status} in
    0) ;;
    1) return 0 ;;
    *) echo "${lever}: cannot read refs/heads/${branch} in ${toplevel}: git show-ref exited ${status}; deleting the branch this run made all the same" >&2 ;;
    esac
    git_direct -C "${toplevel}" branch -D "${branch}" > /dev/null ||
        echo "${lever}: git branch -D ${branch} failed; delete it by hand" >&2
}
trap cleanup EXIT

mkdir -p "${root}" || fail "cannot make ${root}"
git_direct config extensions.worktreeConfig true || fail "cannot set extensions.worktreeConfig in the checkout's config"
# The hooks directory git reads while the tree is made is this lever's own and empty, so no hook of the source checkout
# runs (round 2 hardened the removal after a failing post-checkout hook, and one that locked the tree still beat it).
# It is made under the checkout's git directory, the filesystem of its final place, so the move below is a rename.
staging=$(mktemp -d "${common}/worker-worktree-hooks.XXXXXX") || fail "cannot make a hooks directory under ${common}"
git_direct -c core.hooksPath="${staging}" worktree add --quiet --no-track -b "${branch}" "${path}" "${base}" ||
    fail "git worktree add ${path} from ${base} exited $?"
created=1
wt_git=$(git_direct -C "${path}" rev-parse --path-format=absolute --git-dir) || fail "cannot read the git directory of ${path}"
[[ ${wt_git} == "${common}"/worktrees/* ]] || # lint-comparisons: allow both sides are git's absolute forms
    fail "the git directory ${wt_git} of ${path} is not under ${common}/worktrees/"
hooks=${wt_git}/hooks
mv "${staging}" "${hooks}" || fail "cannot move the hooks directory ${staging} to ${hooks}"
staging=''
printf '#!/bin/sh\necho "%s" >&2\nexit 1\n' "${hook_message}" > "${hooks}/pre-push" || fail "cannot write ${hooks}/pre-push"
chmod 755 "${hooks}/pre-push" || fail "cannot make ${hooks}/pre-push executable"
# A pushurl already in the worktree's scope would stand beside the refusal URL (git pushes to every pushurl), so the
# scope is cleared first; git config exits 5 when the key to unset is absent, the state of a fresh worktree.
status=0
git_direct -C "${path}" config --worktree --unset-all remote.origin.pushurl || status=$?
[[ ${status} == 0 || ${status} == 5 ]] || fail "cannot clear remote.origin.pushurl in the config.worktree of ${path}: git config exited ${status}"
git_direct -C "${path}" config --worktree remote.origin.pushurl "${pushurl}" || fail "cannot set remote.origin.pushurl in ${path}"
git_direct -C "${path}" config --worktree credential.helper '' || fail "cannot set credential.helper in ${path}"
git_direct -C "${path}" config --worktree core.hooksPath "${hooks}" || fail "cannot set core.hooksPath in ${path}"
# The branch's upstream, in the worktree's scope (the add ran with --no-track, so the checkout's config holds none): a
# bare `git push` under push.default simple needs an upstream of the branch's own name, else it stops on its own
# message before any remote is named; with it the push reaches the refusal URL. The main checkout reads none of it.
git_direct -C "${path}" config --worktree "branch.${branch}.remote" origin || fail "cannot set branch.${branch}.remote in ${path}"
git_direct -C "${path}" config --worktree "branch.${branch}.merge" "refs/heads/${branch}" || fail "cannot set branch.${branch}.merge in ${path}"
# The refusals are read back from the worktree's own view, so a config git wrote elsewhere never reads as set: the
# worktree scope holds the refusal URL alone, and every scope the worktree reads adds up to that one value.
set_pushurl=$(git_direct -C "${path}" config --worktree --get-all remote.origin.pushurl) || fail "remote.origin.pushurl is not set in the config.worktree of ${path}"
[[ ${set_pushurl} == "${pushurl}" ]] || fail "remote.origin.pushurl in the config.worktree of ${path} is ${set_pushurl//$'\n'/, }, not ${pushurl} alone"
seen_pushurl=$(git_direct -C "${path}" config --get-all remote.origin.pushurl) || fail "remote.origin.pushurl is not set in ${path}"
[[ ${seen_pushurl} == "${pushurl}" ]] || fail "${path} reads remote.origin.pushurl as ${seen_pushurl//$'\n'/, }, not ${pushurl} alone"
set_hooks=$(git_direct -C "${path}" config --get core.hooksPath) || fail "core.hooksPath is not set in ${path}"
[[ ${set_hooks} == "${hooks}" ]] || fail "core.hooksPath in ${path} is ${set_hooks}, not ${hooks}" # lint-comparisons: allow the value written one line above, read back
set_remote=$(git_direct -C "${path}" config --get "branch.${branch}.remote") || fail "branch.${branch}.remote is not set in ${path}"
[[ ${set_remote} == origin ]] || fail "branch.${branch}.remote in ${path} is ${set_remote}, not origin"
set_merge=$(git_direct -C "${path}" config --get "branch.${branch}.merge") || fail "branch.${branch}.merge is not set in ${path}"
[[ ${set_merge} == "refs/heads/${branch}" ]] || fail "branch.${branch}.merge in ${path} is ${set_merge}, not refs/heads/${branch}" # lint-comparisons: allow the value written above, read back
head=$(git_direct -C "${path}" rev-parse --verify HEAD) || fail "cannot read the head of ${path}"
completed=1

printf 'worktree=%s\nbranch=%s\nhead=%s\n' "${path}" "${branch}" "${head}"
# The path and the URL are quoted for the shell the coordinator pastes the line into; the branch's character set needs
# no quoting, and `<head>` stays the placeholder the coordinator replaces with the worker's final head.
printf 'push=git -C %q push %q <head>:refs/heads/%s\n' "${toplevel}" "${origin_url}" "${branch}"
