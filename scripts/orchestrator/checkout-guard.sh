#!/usr/bin/env bash
# @file checkout-guard.sh
# @brief Install into the coordinator's checkout the reference-transaction hook that refuses, while a program store exists, every move of a local branch to a commit origin does not hold; or check that it is in place.
# @description
#   Regime-cutover U129 (standing orders 27 and 29). On 2026-10-31 three owners acted in the coordinator's checkout
#   against the first line of their task: one committed on its local `main`, two ran `git worktree add` there and
#   committed in the linked worktrees. The worker tree of U123 cannot push, but nothing in the checkout refused a
#   commit: its `core.hooksPath` is unset and its `.git/hooks/` holds samples alone, the directory every linked
#   worktree of it shares. A rule holds when the tool refuses. Round 1 installed a `pre-commit`, and the audit found
#   four more channels in one census (cherry-pick, merge, the shell's inherited options, an unreadable ancestor), so
#   round 2 moves the guard to the reference layer, where no list of commands is needed: every way of authoring a
#   commit in the checkout moves a local branch to a commit origin does not hold, while every move the coordinator
#   makes there (`pull --ff-only`, `reset --hard origin/main`, `worktree add -b <x> origin/main`) lands on a commit
#   origin holds. `checkout-guard.sh install <checkout>` writes one hook into the checkout's common hooks directory,
#   mode 0755, and reads it back:
#   - `reference-transaction`: a `python3 -I -S` script (the heredoc of write_hook below, so this file's sha256 pin
#     covers it; no shell starts, so no shell startup file, `SHELLOPTS` or `BASH_ENV` reaches it, and no `PYTHON*`
#     variable or planted module is read). Git runs it for every reference transaction; in its `prepared` phase it
#     reads the `<old-value> SP <new-value> SP <ref-name> LF` lines from stdin and, while
#     `.orchestration/orchestrate/<program>/units.tsv` exists under the toplevel of the worktree the command runs in or
#     under the main worktree's, refuses the transaction (exit 1, git then fails with status 128) when any line moves
#     a `refs/heads/*` ref to a commit that no `refs/remotes/origin/*` ref reaches (`git merge-base --is-ancestor`,
#     each status read), printing `checkout-guard: this checkout is the coordinator's; commits belong in a worker tree:
#     ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one under $TMPDIR/dotfiles-wt/<unit>
#     (standing order 29)`. Deletions and every ref outside `refs/heads/` (a detached HEAD, tags, remote-tracking
#     refs, ORIG_HEAD, the stash) pass; the other phases exit 0. `git commit --no-verify` skips no
#     reference-transaction hook. A read that fails refuses the transaction (standing order 21): the store walk is
#     `os.scandir`, where an absent `.orchestration` is no store and any other `OSError` (a mode-000 ancestor, a file
#     where a directory should be) is a refusal naming it; the toplevel and the worktree list come from git as bytes
#     (`worktree list --porcelain -z`), never split on newlines; a git read that exits non-zero is a refusal naming it.
#   The hook runs inside the user's git and cannot isolate itself from the repository it guards, so its reads are the
#   plain `git` with `-c core.hooksPath=/dev/null` (so they run no hook) and a `# git-isolated: allow` reason; it
#   writes nothing but its own stderr and runs no network command. The isolated git of the levers (git-isolated.sh,
#   the same flag) never runs it, so records-sync.sh and the other levers are untouched.
#   `checkout-guard.sh check <checkout>` reports `installed` (byte-equal to the copy here and executable), `absent`,
#   `differs` or `not-executable` for the hook, and `stale` for a round-1 `pre-commit` or `post-checkout` still
#   there (byte-equal to round 1's, kept in write_hook for this comparison alone); exit 0 when the hook is installed
#   and nothing is stale, else 1. `install` refuses (exit 2, nothing written) unless `<checkout>` is in a main
#   checkout (`git rev-parse --git-dir` equals `--git-common-dir`; a linked worktree's hooks directory is the main
#   checkout's, so it is installed there), `core.hooksPath` is unset as the operator's git reads it (the global and
#   system configuration included: a set path means this hook would never run, and it is refused naming the path),
#   and the hook path is absent or already this lever's own; any other file, or a symlink, there is refused and never
#   overwritten. After the hook is in place it removes a round-1 `pre-commit` or `post-checkout` that is byte-equal to
#   round 1's (`removed` rows; the `pre-commit` in either of the two byte forms round 1 wrote, see write_hook), so an
#   upgraded checkout keeps no dead hook; any other file at those two paths is not this lever's and is left alone. A second run finds its own hook, prints `unchanged` and exits 0, so regime-init
#   calls it on every run. Every comparison is `cmp -s` against a copy of the expected bytes written to a scratch
#   directory (NUL-safe: a shell variable cannot hold the NUL a drifted file may), its status read: 0 is equal, 1 is
#   different, anything else is a failed read and a refusal. Every read is checked (standing order 21): `git
#   rev-parse`, `git config` (exit 1 is "unset", any other failure is a refusal), `mktemp`, each write of the
#   expected bytes, each `cmp`; each failure exits 2 naming the file. Left out, by design: a `core.hooksPath` the
#   operator sets after the install (`check` reads it again and refuses), a worker that edits `.git/hooks` of the
#   checkout (the worker tree is a repository of its own and never sees this hook), a commit on a detached HEAD (no
#   branch moves; the rule names local branches), and a repository with no `origin` remote, where no commit is
#   reachable and every branch move is refused while a store exists.
#   Trusted: the coordinator is the only committer in the checkout and commits nothing there by design (records
#   move through records-sync.sh's scratch repository, code through worker trees); git runs the common
#   `hooks/reference-transaction` for the checkout and every linked worktree when `core.hooksPath` is unset, and
#   resolves symbolic refs before the `prepared` phase (githooks(5)); `refs/remotes/origin/*` are origin's refs,
#   whatever wrote them; `python3` on the hook's PATH is a CPython 3; the worker's identity is not read.
# @arg $1 string `install` or `check`.
# @arg $2 string The checkout: a directory inside the main worktree of the repository.
# @stdout One row per hook, `checkout-guard: <state>\t<path>`: `installed`, `unchanged` or `removed` (install); `installed`, `absent`, `differs`, `not-executable` or `stale` (check). regime-init matches the `checkout-guard: installed` and `checkout-guard: removed` rows at line start.
# @exitcode 0 Done: the hook installed and no stale round-1 hook left (install), or in place with nothing stale (check).
# @exitcode 1 `check`: the hook is absent, differs or is not executable, or a round-1 hook is still there.
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
hook=reference-transaction
legacy_hooks=(pre-commit post-checkout)

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

# The effective hooks path is the value the operator's git reads when a ref moves: the repository, global and
# system configuration, which the isolated git closes while setting a `core.hooksPath` of its own, so this one read
# is a plain git (after the scrub, so no `GIT_DIR` of the caller points it elsewhere). git config exits 1 for a key
# that is unset and otherwise for a read that failed (standing order 21): only 1 is absence.
status=0
hooks_path=$(git -C "${toplevel}" config --get core.hooksPath 2>&1) || status=$? # git-isolated: allow the operator's git decides whether .git/hooks runs, so its configuration is read as it stands, which the isolated git closes
case ${status} in
0) refuse "core.hooksPath is ${hooks_path} in ${toplevel}, so the hook under ${hooks} would not run; unset it first" ;;
1) ;;
*) refuse "cannot read core.hooksPath in ${toplevel}: ${hooks_path}" ;;
esac

# @description Write the text of hook $1 to the path $2: the quoted heredocs below, so nothing in them expands here,
#   each redirected straight into the file (a command substitution would re-parse the body: bash 3.2 and others
#   expand `$'…'` inside a quoted heredoc there, which is how round 1's installed `pre-commit` came to differ from its
#   heredoc by that one token). `pre-commit` and `post-checkout` are round 1's hooks, kept so an upgraded checkout's
#   copies are recognised and removed, never installed: `pre-commit` in the heredoc's own bytes and, as
#   `pre-commit.subst`, in the bytes round 1 wrote through its command substitution (`$'\n'` already a newline inside
#   the quotes); `post-checkout` holds no such token and has one form. A failed write is a refusal naming the path.
# @arg $1 string `reference-transaction`, `pre-commit`, `pre-commit.subst` or `post-checkout`.
# @arg $2 string The path.
write_hook() {
    case $1 in
    reference-transaction)
        cat << 'REFERENCE_TRANSACTION' > "$2" || refuse "cannot write $2"
#!/usr/bin/env -S python3 -I -S
# checkout-guard reference-transaction (regime-cutover U129), installed by checkout-guard.sh, whose `check` compares
# these bytes with its copy. The coordinator's checkout and every linked worktree of it share this file, and git runs
# it for every reference transaction (githooks(5)). In the `prepared` phase, the refs locked and symbolic refs
# resolved, it reads the updates from stdin, one `<old-value> SP <new-value> SP <ref-name> LF` per line, and refuses
# the transaction (exit 1, the route to a worker tree on stderr) while a program store
# `.orchestration/orchestrate/<program>/units.tsv` exists under this worktree's toplevel or under the main worktree's
# and any line moves a `refs/heads/*` ref to a commit that no `refs/remotes/origin/*` ref reaches. That is every
# commit authored here (commit, --amend, merge, cherry-pick, rebase; `--no-verify` skips no reference-transaction),
# while `pull --ff-only`, `reset --hard origin/<branch>`, `fetch`, a branch deleted or made at origin's commit, and
# every ref outside refs/heads/ (a detached HEAD, tags, remote-tracking refs, ORIG_HEAD, the stash) pass. The other
# phases exit 0. It runs under `python3 -I -S`: no shell starts, so no shell startup file, SHELLOPTS or BASH_ENV
# reaches it, and no PYTHON* variable, site directory or module planted beside it is read. A read that fails refuses
# the transaction (standing order 21): a store directory that cannot be listed, a line of another shape, a git read
# that exits non-zero. Its git calls carry `-c core.hooksPath=/dev/null`, so they run no hook, and the isolated git
# of the levers (the same flag) never runs this file. It writes nothing but its own stderr.
import os
import subprocess
import sys

ROUTE = (
    "commits belong in a worker tree: ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one "
    "under $TMPDIR/dotfiles-wt/<unit> (standing order 29)"
)
# A hook runs inside the user's git and cannot isolate itself from the repository it guards; the flag keeps its own
# reads from running any hook, this file included.
GIT = ("git", "-c", "core.hooksPath=/dev/null")  # git-isolated: allow a hook cannot isolate itself from its repository
ZERO = (b"0" * 40, b"0" * 64)


def refuse(reason):
    sys.stderr.write("checkout-guard reference-transaction: %s; the update is refused (standing order 21)\n" % reason)
    sys.exit(1)


def git(*args):
    """(exit status, stdout bytes, stderr text) of one git read; a git that cannot start refuses."""
    try:
        run = subprocess.run(GIT + args, stdin=subprocess.DEVNULL, capture_output=True, check=False)
    except OSError as error:
        refuse("cannot run git %s: %s" % (" ".join(args), error))
    return run.returncode, run.stdout, run.stderr.decode("utf-8", "replace").strip()


def read(*args):
    """The stdout bytes of one git read; a non-zero exit refuses the transaction naming the read."""
    status, out, err = git(*args)
    if status != 0:
        refuse("git %s exited %d: %s" % (" ".join(args), status, err))
    return out


def updates(data):
    """The (old, new, ref) of each line of DATA in the shape githooks(5) documents; any other shape refuses."""
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    result = []
    for line in lines:
        fields = line.split(b" ")
        if len(fields) != 3 or not all(fields):
            refuse("a line of the transaction is not <old-value> SP <new-value> SP <ref-name>: %r" % line)
        result.append((fields[0], fields[1], fields[2]))
    return result


def store_under(top):
    """Whether `.orchestration/orchestrate/<program>/units.tsv` exists under TOP. An absent `.orchestration` or
    `orchestrate` is no store; a directory that cannot be listed, one that is not a directory, or a program whose
    `units.tsv` cannot be looked up refuses the transaction, never passes it (standing order 21)."""
    stores = os.path.join(top, b".orchestration", b"orchestrate")
    try:
        with os.scandir(stores) as entries:
            programs = list(entries)
    except FileNotFoundError:
        return False
    except OSError as error:
        refuse("cannot read %s: %s" % (os.fsdecode(stores), error.strerror or error))
    for program in programs:
        units = os.path.join(program.path, b"units.tsv")
        try:
            if not program.is_dir():
                continue
            os.stat(units)
        except FileNotFoundError:
            continue
        except OSError as error:
            refuse("cannot read %s: %s" % (os.fsdecode(units), error.strerror or error))
        return True
    return False


def origin_commits():
    """The distinct commits the refs/remotes/origin/* refs name, origin/HEAD's first: the one most moves land on."""
    listing = read("for-each-ref", "--format=%(refname)%09%(objectname)", "refs/remotes/origin/")
    first, rest = [], []
    for line in listing.split(b"\n"):
        if not line:
            continue
        name, _, commit = line.partition(b"\t")
        (first if name == b"refs/remotes/origin/HEAD" else rest).append(commit)
    return list(dict.fromkeys(first + rest))


def reachable(commit, candidates):
    """Whether COMMIT is an ancestor of (or equal to) one of CANDIDATES: `merge-base --is-ancestor` exits 0 for an
    ancestor and 1 for none; any other status is a failed read and refuses."""
    for candidate in candidates:
        status, _, err = git("merge-base", "--is-ancestor", commit, candidate)
        if status == 0:
            return True
        if status != 1:
            refuse(
                "git merge-base --is-ancestor %s %s exited %d: %s" % (commit.decode(), candidate.decode(), status, err)
            )
    return False


def main():
    data = sys.stdin.buffer.read()
    if len(sys.argv) != 2 or sys.argv[1] != "prepared":
        return 0
    moves = [
        (new, ref)
        for _, new, ref in updates(data)
        if ref.startswith(b"refs/heads/") and new not in ZERO and not new.startswith(b"ref:")
    ]
    if not moves:
        return 0
    toplevel = read("rev-parse", "--show-toplevel")
    if toplevel.endswith(b"\n"):
        toplevel = toplevel[:-1]
    # The first record of the NUL-separated porcelain list is the main worktree (git-worktree(1)).
    first = read("worktree", "list", "--porcelain", "-z").split(b"\0", 1)[0]
    if not first.startswith(b"worktree "):
        refuse("the worktree list does not start with the main worktree: %r" % first)
    tops = [toplevel]
    if first[len(b"worktree ") :] != toplevel:
        tops.append(first[len(b"worktree ") :])
    if not any(store_under(top) for top in tops):
        return 0
    candidates = origin_commits()
    for new, ref in moves:
        if not reachable(new, candidates):
            sys.stderr.write("checkout-guard: this checkout is the coordinator's; %s\n" % ROUTE)
            sys.stderr.write(
                "checkout-guard: %s would move to %s, which no refs/remotes/origin/* ref reaches\n"
                % (ref.decode("utf-8", "replace"), new.decode("utf-8", "replace"))
            )
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
REFERENCE_TRANSACTION
        ;;
    pre-commit)
        cat << 'ROUND1_PRE_COMMIT' > "$2" || refuse "cannot write $2"
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
ROUND1_PRE_COMMIT
        ;;
    pre-commit.subst)
        cat << 'ROUND1_PRE_COMMIT_SUBST' > "$2" || refuse "cannot write $2"
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
main=${worktrees%%'
'*}
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
ROUND1_PRE_COMMIT_SUBST
        ;;
    post-checkout)
        cat << 'ROUND1_POST_CHECKOUT' > "$2" || refuse "cannot write $2"
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
ROUND1_POST_CHECKOUT
        ;;
    *) refuse "no hook named $1" ;;
    esac
}

# The expected bytes of each hook, written once to a scratch directory so every comparison below is `cmp -s`, which
# reads every byte of both files (a command substitution would drop a NUL).
scratch=$(mktemp -d "${TMPDIR:-/tmp}/checkout-guard.XXXXXX") || refuse 'cannot make a scratch directory for the expected hook bytes'
trap 'rm -rf -- "${scratch}"' EXIT
for name in "${hook}" "${legacy_hooks[@]}" pre-commit.subst; do
    write_hook "${name}" "${scratch}/${name}"
done

# @description Judge the file at $1 against hook $2: `state` is `absent` (nothing there), `own` (a regular file
#   holding exactly this lever's bytes) or `foreign` (a symlink, a directory, or any other content), and `executable`
#   is 1 when the file has its owner's execute bit. A symlink is foreign whatever it points at: nothing is written
#   through one. The comparison is `cmp -s` against the scratch copy, and for `pre-commit` against both of its forms:
#   0 equal, 1 different, anything else a failed read and a refusal, never an absence (standing order 21).
# @arg $1 string The path.
# @arg $2 string The hook name.
# @set state `absent`, `own` or `foreign`.
# @set executable 0 or 1.
hook_state() {
    local target=$1 name=$2 same form
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
    for form in "${scratch}/${name}" "${scratch}/${name}.subst"; do
        [[ -e ${form} ]] || continue
        same=0
        cmp -s -- "${form}" "${target}" || same=$?
        case ${same} in
        0)
            state=own
            return 0
            ;;
        1) ;;
        *) refuse "cannot compare ${target} with this lever's ${form##*/}" ;;
        esac
    done
}

# The hook and the two round-1 paths are judged before anything is written.
hook_state "${hooks}/${hook}" "${hook}"
hook_own=${state} hook_executable=${executable}
stale=()
for name in "${legacy_hooks[@]}"; do
    hook_state "${hooks}/${name}" "${name}"
    [[ ${state} != own ]] || stale+=("${name}")
done

if [[ ${action} == check ]]; then
    missing=0
    target=${hooks}/${hook}
    case ${hook_own}:${hook_executable} in
    own:1) printf 'checkout-guard: installed\t%s\n' "${target}" ;;
    own:0)
        printf 'checkout-guard: not-executable\t%s\n' "${target}"
        missing=1
        ;;
    absent:*)
        printf 'checkout-guard: absent\t%s\n' "${target}"
        missing=1
        ;;
    *)
        printf 'checkout-guard: differs\t%s\n' "${target}"
        missing=1
        ;;
    esac
    for name in "${stale[@]+"${stale[@]}"}"; do
        printf 'checkout-guard: stale\t%s\n' "${hooks}/${name}"
        missing=1
    done
    exit "${missing}"
fi

[[ ${hook_own} != foreign ]] || refuse "${hooks}/${hook} exists and is not this lever's hook; it is never overwritten (move it away by hand, then rerun)"
if [[ ! -d ${hooks} ]]; then
    mkdir "${hooks}" || refuse "cannot make ${hooks}"
fi

# Write the hook unless it is already this lever's own and executable, set its mode, and read it back: the file holds
# this lever's bytes and has its execute bit, else the install is refused.
target=${hooks}/${hook}
if [[ ${hook_own} == own && ${hook_executable} == 1 ]]; then
    printf 'checkout-guard: unchanged\t%s\n' "${target}"
else
    [[ ${hook_own} == own ]] || write_hook "${hook}" "${target}"
    chmod 755 "${target}" || refuse "cannot make ${target} executable"
    hook_state "${target}" "${hook}"
    [[ ${state} == own && ${executable} == 1 ]] || refuse "${target} reads back as ${state} (executable: ${executable}) after the write"
    printf 'checkout-guard: installed\t%s\n' "${target}"
fi

# The round-1 hooks go only after the new hook is in place, so no run leaves the checkout unguarded.
for name in "${stale[@]+"${stale[@]}"}"; do
    rm -- "${hooks}/${name}" || refuse "cannot remove the round-1 ${hooks}/${name}"
    [[ ! -e ${hooks}/${name} ]] || refuse "${hooks}/${name} is still there after its removal"
    printf 'checkout-guard: removed\t%s\n' "${hooks}/${name}"
done
