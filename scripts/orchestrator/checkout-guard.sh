#!/usr/bin/env bash
# @file checkout-guard.sh
# @brief Install into the coordinator's checkout the pre-commit that refuses every commit there and in its linked worktrees while a program store exists, and the post-checkout that warns after a `git worktree add`; or check that both are in place.
# @description
#   Regime-cutover U129 (standing orders 27 and 29). On 2026-10-31 three owners acted in the coordinator's checkout
#   against the first line of their task: one committed on its local `main`, two ran `git worktree add` there and
#   committed in the linked worktrees. The worker tree of U123 cannot push, but nothing in the checkout refused a
#   commit: its `core.hooksPath` is unset and its `.git/hooks/` holds samples alone, the directory every linked
#   worktree of it shares. A rule holds when the tool refuses. `checkout-guard.sh install <checkout>` writes two
#   hooks into that directory, mode 0755, and reads them back:
#   - `pre-commit`: while `.orchestration/orchestrate/<program>/units.tsv` exists under the toplevel of the worktree
#     the commit is made in or under the main worktree's, it prints `checkout-guard: this checkout is the
#     coordinator's; commits belong in a worker tree: ~/.local/bin/common/worker-worktree.sh <unit> <branch>
#     origin/main makes one under $TMPDIR/dotfiles-wt/<unit> (standing order 29)` and exits 1; otherwise it exits 0.
#     No environment variable bypasses it; a read that fails (the toplevel, the worktree list, a store directory
#     that cannot be listed) refuses the commit (standing order 21).
#   - `post-checkout`: when its third argument is 1 (a branch checkout, which `git worktree add` performs) and the
#     worktree is a linked one, it prints the same route as a warning and exits 0; a hook cannot undo the add.
#   Both hooks run inside the user's git and cannot isolate themselves from the repository they guard, so their
#   reads are plain `git` with a `# git-isolated: allow` reason; they write nothing but their own stdout and stderr
#   and run no network command. The hook bodies are the heredocs of hook_body below, so this file's sha256 pin
#   covers them, and `checkout-guard.sh check <checkout>` reports, per hook, `installed` (byte-equal to the copy here
#   and executable), `absent`, `differs` or `not-executable`, exit 0 when both are installed, else 1.
#   `install` refuses (exit 2, nothing written) unless `<checkout>` is in a main checkout (`git rev-parse --git-dir`
#   equals `--git-common-dir`; a linked worktree's hooks directory is the main checkout's, so it is installed there),
#   `core.hooksPath` is unset as the operator's git reads it (the global and system configuration included: a set
#   path means these hooks would never run, and it is refused naming the path), and each of the two hooks is absent
#   or already this lever's own; any other file, or a symlink, at either path is refused and never overwritten. A
#   second run finds its own hooks, prints `unchanged` for each and exits 0, so regime-init calls it on every run.
#   Every read is checked (standing order 21): `git rev-parse`, `git config` (exit 1 is "unset", any other failure
#   is a refusal), the `cat` of an existing hook and of each written one; each failure exits 2 naming the file.
#   The isolated git of the levers (git-isolated.sh, `-c core.hooksPath=/dev/null`) never runs these hooks, so
#   records-sync.sh and the other levers are untouched. Left out, by design: `git commit --no-verify` (the operator's
#   own hand), a `core.hooksPath` the operator sets after the install (`check` reads it again and refuses), and a
#   worker that edits `.git/hooks` of the checkout (the worker tree is a repository of its own and never sees these
#   hooks).
#   Trusted: the coordinator is the only committer in the checkout and commits nothing there by design (records
#   move through records-sync.sh's scratch repository, code through worker trees), and git runs
#   `.git/hooks/pre-commit` for the checkout and every linked worktree when `core.hooksPath` is unset; the worker's
#   identity is not read, and `--no-verify` is the operator's own hand.
# @arg $1 string `install` or `check`.
# @arg $2 string The checkout: a directory inside the main worktree of the repository.
# @stdout One row per hook, `<state>\t<path>`: `installed` or `unchanged` (install); `installed`, `absent`, `differs` or `not-executable` (check).
# @exitcode 0 Done: both hooks installed (install), or both in place (check).
# @exitcode 1 `check`: at least one hook is absent, differs or is not executable.
# @exitcode 2 A refusal, before anything is written: usage, not a main checkout, `core.hooksPath` set, a foreign hook, a failed read or write, or the manifest pin differing from this file.
# @example
#   ~/.local/bin/common/checkout-guard.sh install ~/Workspace/dotfiles
#   ~/.local/bin/common/checkout-guard.sh check ~/Workspace/dotfiles
set -euo pipefail

# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
# @set LEVER_DIR The physical directory of this file, where the sourced git-isolated.sh library sits.
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
    LEVER_DIR=${dir}
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

lever='checkout-guard.sh'
usage='usage: checkout-guard.sh install|check <checkout>'

# @description Print a refusal on stderr and exit 2; nothing was written.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

(($# == 2)) || refuse "${usage}"
action=$1
checkout=$2
case ${action} in
install | check) ;;
*) refuse "${usage}" ;;
esac
[[ -d ${checkout} ]] || refuse "${checkout} is not a directory"

# The identity reads run through the isolated git (U113), with every `GIT_*` and transport variable removed first:
# a `GIT_DIR` or `GIT_COMMON_DIR` of the caller would point them at another repository.
[[ -r ${LEVER_DIR}/git-isolated.sh ]] || refuse "git-isolated.sh unreadable beside this script: ${LEVER_DIR}/git-isolated.sh"
# shellcheck source=scripts/orchestrator/git-isolated.sh
. "${LEVER_DIR}/git-isolated.sh"
# shellcheck disable=SC2119 # no name is kept: every GIT_* and transport variable goes
git_env_scrub

toplevel=$(git_isolated -C "${checkout}" rev-parse --show-toplevel 2> /dev/null) || refuse "${checkout} is not inside a git working tree"
git_dir=$(git_isolated -C "${checkout}" rev-parse --path-format=absolute --git-dir) || refuse "cannot read the git directory of ${toplevel}"
common=$(git_isolated -C "${checkout}" rev-parse --path-format=absolute --git-common-dir) || refuse "cannot read the git common directory of ${toplevel}"
[[ ${git_dir} == "${common}" ]] || # lint-comparisons: allow both sides are git's absolute forms of one checkout
    refuse "${toplevel} is a linked worktree (git dir ${git_dir}, common ${common}); install in the main checkout, whose hooks every linked worktree shares"
hooks=${common}/hooks
[[ ! -L ${hooks} ]] || refuse "${hooks} is a symlink; nothing is written through it"

# The effective hooks path is the value the operator's git reads when a commit is made: the repository, global and
# system configuration, which the isolated git closes while setting a `core.hooksPath` of its own, so this one read
# is a plain git (after the scrub, so no `GIT_DIR` of the caller points it elsewhere). git config exits 1 for a key
# that is unset and otherwise for a read that failed (standing order 21): only 1 is absence.
status=0
hooks_path=$(git -C "${toplevel}" config --get core.hooksPath 2>&1) || status=$? # git-isolated: allow the operator's git decides whether .git/hooks runs, so its configuration is read as it stands, which the isolated git closes
case ${status} in
0) refuse "core.hooksPath is ${hooks_path} in ${toplevel}, so the hooks under ${hooks} would not run; unset it first" ;;
1) ;;
*) refuse "cannot read core.hooksPath in ${toplevel}: ${hooks_path}" ;;
esac

# @description Set `body` to the text of hook $1 without its final newline: the heredocs below, whose delimiters are
#   quoted so nothing in them expands here. A hook file is these bytes plus one newline.
# @arg $1 string `pre-commit` or `post-checkout`.
# @set body The hook's text.
hook_body() {
    case $1 in
    pre-commit)
        body=$(
            cat << 'PRE_COMMIT'
#!/usr/bin/env bash
# checkout-guard pre-commit (regime-cutover U129), installed by checkout-guard.sh, whose `check` compares these
# bytes with its copy. The coordinator's checkout and every linked worktree of it share this file: while a program
# store `.orchestration/orchestrate/<program>/units.tsv` exists under the toplevel of the worktree the commit is made
# in or under the main worktree's, every commit is refused with the one accepted route, a worker tree made by
# worker-worktree.sh (standing order 29). No environment variable bypasses it; `git commit --no-verify` is the
# operator's own hand, and the isolated git of the levers (`-c core.hooksPath=/dev/null`) never runs this file. A read
# that fails refuses the commit (standing order 21). This hook writes nothing but its own stdout and stderr.
set -euo pipefail
route="commits belong in a worker tree: ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one under \$TMPDIR/dotfiles-wt/<unit> (standing order 29)"
# Refuse the commit on a failed read, naming it.
refuse() {
    echo "checkout-guard pre-commit: $*; the commit is refused (standing order 21)" >&2
    exit 1
}
# A hook runs inside the user's git, which puts its own exec path first on PATH, and cannot isolate itself from the
# repository it guards; the two reads name this worktree and the main one, nothing else.
toplevel=$(git rev-parse --show-toplevel) || refuse 'cannot read the toplevel of this worktree' # git-isolated: allow a hook runs inside the user's git and cannot isolate itself from the repository it guards
# The first worktree of the porcelain list is the main one (git-worktree(1)).
worktrees=$(git worktree list --porcelain) || refuse 'cannot list the worktrees of this repository' # git-isolated: allow a hook runs inside the user's git and cannot isolate itself from the repository it guards
main=${worktrees%%$'\n'*}
[[ ${main} == 'worktree '* ]] || refuse "the worktree list does not start with the main worktree: ${main}"
main=${main#worktree }
for top in "${toplevel}" "${main}"; do
    stores=${top}/.orchestration/orchestrate
    [[ -d ${stores} ]] || continue
    # A directory that cannot be listed is a failed read, never "no store": the glob below would match nothing.
    [[ -r ${stores} && -x ${stores} ]] || refuse "cannot read ${stores}"
    for program in "${stores}"/*/; do
        [[ -d ${program} ]] || continue # the pattern itself, when nothing matches
        [[ -r ${program} && -x ${program} ]] || refuse "cannot read ${program}"
        [[ -e ${program}units.tsv ]] || continue
        echo "checkout-guard: this checkout is the coordinator's; ${route}" >&2
        exit 1
    done
done
exit 0
PRE_COMMIT
        ) || refuse 'cannot read the pre-commit hook body'
        ;;
    post-checkout)
        body=$(
            cat << 'POST_CHECKOUT'
#!/usr/bin/env bash
# checkout-guard post-checkout (regime-cutover U129), installed by checkout-guard.sh beside its pre-commit. After a
# branch checkout (its third argument is 1, the checkout `git worktree add` performs) in a linked worktree of the
# coordinator's checkout it prints the worker-tree route as a warning and exits 0: a hook cannot undo the add, and
# the pre-commit this checkout shares with the worktree refuses the commits made there. A file checkout, or a branch
# checkout in the main checkout, prints nothing. A read that fails is named and exits 0: this hook refuses nothing,
# so its status never changes the command's outcome. It writes nothing but its own stdout and stderr.
set -euo pipefail
route="commits belong in a worker tree: ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one under \$TMPDIR/dotfiles-wt/<unit> (standing order 29)"
[[ ${3:-0} == 1 ]] || exit 0
# A hook runs inside the user's git and cannot isolate itself from the repository it guards; the two reads name this
# worktree's git directory and the common one.
if ! git_dir=$(git rev-parse --path-format=absolute --git-dir); then # git-isolated: allow a hook runs inside the user's git and cannot isolate itself from the repository it guards
    echo 'checkout-guard post-checkout: cannot read the git directory of this worktree; no warning is printed' >&2
    exit 0
fi
if ! common=$(git rev-parse --path-format=absolute --git-common-dir); then # git-isolated: allow a hook runs inside the user's git and cannot isolate itself from the repository it guards
    echo 'checkout-guard post-checkout: cannot read the git common directory of this worktree; no warning is printed' >&2
    exit 0
fi
[[ ${git_dir} != "${common}" ]] || exit 0 # lint-comparisons: allow both sides are git's absolute forms; equal means the main checkout, which is silent
echo "checkout-guard: warning: this is a linked worktree of the coordinator's checkout, whose pre-commit refuses every commit here; ${route}" >&2
exit 0
POST_CHECKOUT
        ) || refuse 'cannot read the post-checkout hook body'
        ;;
    *) refuse "no hook named $1" ;;
    esac
}

# @description Judge the file at $1 against hook $2: `state` is `absent` (nothing there), `own` (a regular file
#   holding exactly this lever's bytes) or `foreign` (a symlink, a directory, or any other content), and `executable`
#   is 1 when the file has its owner's execute bit. A symlink is foreign whatever it points at: nothing is written
#   through one. A file that cannot be read is a refusal, never an absence (standing order 21).
# @arg $1 string The path.
# @arg $2 string The hook name.
# @set state `absent`, `own` or `foreign`.
# @set executable 0 or 1.
hook_state() {
    local target=$1 existing
    hook_body "$2"
    state=foreign
    executable=0
    if [[ -L ${target} ]]; then
        return 0
    fi
    if [[ ! -e ${target} ]]; then
        state=absent
        return 0
    fi
    [[ -f ${target} ]] || return 0
    [[ ! -x ${target} ]] || executable=1
    existing=$(cat "${target}" && printf x) || refuse "cannot read ${target}"
    existing=${existing%x}
    [[ ${existing} == "${body}"$'\n' ]] || return 0
    state=own
}

# Both hooks are judged before either is written, so a foreign hook at one path leaves the other unwritten.
hook_state "${hooks}/pre-commit" pre-commit
pre_state=${state} pre_executable=${executable}
hook_state "${hooks}/post-checkout" post-checkout
post_state=${state} post_executable=${executable}

# @description Print the `check` row of hook $1 from its state $2 and execute bit $3; `missing` becomes 1 unless the
#   hook is this lever's own and executable.
# @arg $1 string The hook name.
# @arg $2 string `absent`, `own` or `foreign`.
# @arg $3 string 0 or 1.
check_row() {
    local target=${hooks}/$1
    case $2:$3 in
    own:1) printf 'installed\t%s\n' "${target}" ;;
    own:0)
        printf 'not-executable\t%s\n' "${target}"
        missing=1
        ;;
    absent:*)
        printf 'absent\t%s\n' "${target}"
        missing=1
        ;;
    *)
        printf 'differs\t%s\n' "${target}"
        missing=1
        ;;
    esac
}

if [[ ${action} == check ]]; then
    missing=0
    check_row pre-commit "${pre_state}" "${pre_executable}"
    check_row post-checkout "${post_state}" "${post_executable}"
    exit "${missing}"
fi

[[ ${pre_state} != foreign ]] || refuse "${hooks}/pre-commit exists and is not this lever's hook; it is never overwritten (move it away by hand, then rerun)"
[[ ${post_state} != foreign ]] || refuse "${hooks}/post-checkout exists and is not this lever's hook; it is never overwritten (move it away by hand, then rerun)"
if [[ ! -d ${hooks} ]]; then
    mkdir "${hooks}" || refuse "cannot make ${hooks}"
fi

# @description Write hook $1 unless it is already this lever's own and executable (state $2, execute bit $3), set its
#   mode, and read it back: the file holds this lever's bytes and has its execute bit, else the install is refused.
# @arg $1 string The hook name.
# @arg $2 string `absent` or `own`.
# @arg $3 string 0 or 1.
install_hook() {
    local name=$1 target=${hooks}/$1
    if [[ $2 == own && $3 == 1 ]]; then
        printf 'unchanged\t%s\n' "${target}"
        return 0
    fi
    if [[ $2 == absent ]]; then
        hook_body "${name}"
        printf '%s\n' "${body}" > "${target}" || refuse "cannot write ${target}"
    fi
    chmod 755 "${target}" || refuse "cannot make ${target} executable"
    hook_state "${target}" "${name}"
    [[ ${state} == own && ${executable} == 1 ]] || refuse "${target} reads back as ${state} (executable: ${executable}) after the write"
    printf 'installed\t%s\n' "${target}"
}

install_hook pre-commit "${pre_state}" "${pre_executable}"
install_hook post-checkout "${post_state}" "${post_executable}"
