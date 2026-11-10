#!/usr/bin/env bash
# @file checkout-guard.sh
# @brief Install into the coordinator's checkout the reference-transaction hook that refuses, while its marker lies beside it or a program store exists, every move of a local branch to a commit origin does not hold, and the marker beside it; or check that both are in place.
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
#   origin holds. `checkout-guard.sh install <checkout>` puts one hook and one marker into the checkout's common hooks
#   directory, each by a rename of a temporary file it has written and read back there (below):
#   - `reference-transaction`, mode 0755: a `python3 -I -S` script (the heredoc of write_hook below, so this file's sha256 pin
#     covers it; no shell starts, so no shell startup file, `SHELLOPTS` or `BASH_ENV` reaches it, and no `PYTHON*`
#     variable or planted module is read). Git runs it for every reference transaction; in its `prepared` phase it
#     reads the `<old-value> SP <new-value> SP <ref-name> LF` lines from stdin (each value an object id of 40 or 64
#     lowercase hex or `ref:<ref-target>`; a line of another shape or a value of another form is a refusal naming it,
#     U135) and, while
#     the marker `regime-coordinator` lies beside it (the next item, regime-cutover U219) or
#     `.orchestration/orchestrate/<program>/units.tsv` exists under the toplevel of the worktree the command runs in or
#     under the main worktree's (the pre-move trigger, which U221 removes with the live store's move), refuses the
#     transaction (exit 1, git then fails with status 128) when any line moves
#     a `refs/heads/*` ref to a commit that no `refs/remotes/origin/*` ref reaches (`git --no-replace-objects
#     merge-base --is-ancestor`, each status read), printing `checkout-guard: this checkout is the coordinator's; commits belong in a worker tree:
#     ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one under $TMPDIR/dotfiles-wt/<unit>
#     (standing order 29)`. Deletions and every ref outside `refs/heads/` (a detached HEAD, tags, remote-tracking
#     refs, ORIG_HEAD, the stash) pass; the other phases exit 0. `git commit --no-verify` skips no
#     reference-transaction hook. A read that fails refuses the transaction (standing order 21): the store walk lists
#     `.orchestration`, then `orchestrate`, then every program directory, in that order and to the end (`os.listdir`:
#     a directory is listed, never `stat`-ed for a child, which a mode-0111 directory answers while refusing a
#     listing; no program directory is skipped once a store is found), where an absent `.orchestration` or
#     `orchestrate` is no store and any other `OSError` on any of those listings (a mode-000 or 0111 directory, a
#     file where `.orchestration` or `orchestrate` should be) is a refusal naming it; the toplevel, the git directory
#     and the common directory come from git as bytes (`rev-parse --show-toplevel`, `--path-format=absolute --git-dir`
#     and `--git-common-dir`, one trailing LF removed each), never split on newlines; the main checkout is this
#     worktree when its git directory is the common directory, else the parent of a common directory named `.git`, as
#     git-worktree(1) derives the main worktree (U135: `worktree list` is not read; it named a separate git directory
#     reached through a `.git` symlink as the main worktree, so a linked worktree's moves missed the store and
#     passed); from a linked worktree whose common directory is not named `.git`, git records no name for the main
#     checkout and every move is refused naming the directory, never passed; a git read that exits non-zero is a
#     refusal naming it.
#   - `regime-coordinator`, mode 0644: the marker (regime-cutover U219, store move 3 of 5, handoff/07-store-move-design.md;
#     verdict U215-11a32ed6 P2), a regular file holding the one line `regime-cutover U219: this checkout is the
#     coordinator's`, written beside the hook by the same staged rename and removed by nothing but the operator's hand.
#     It is the hook's trigger once the live store has left the checkout (U221): the hook reads it from its own
#     directory, the one git ran it from (`os.lstat`: a symbolic link, whatever it points at, a directory or any other
#     kind is no marker, an absent one is none, any other read failure refuses the transaction), before the pre-move
#     store trigger. The common hooks directory is shared by every linked worktree of the checkout and write-denied to
#     every seat (hcom-seat's `git_state` rows), so no seat plants or removes the marker, and the guard fires wherever
#     the records live. A regular file of other content at the marker's path is `differs` for `check` and a refusal
#     for `install`, which never overwrites it; a symbolic link or a directory there is refused by both actions naming
#     the kind. The marker row is `checkout-guard: installed`, `unchanged`, `absent` or `differs` with the marker's
#     path, so regime-init counts a marker written into an upgraded checkout as a change like the hook.
#   The hook runs inside the user's git and cannot isolate itself from the repository it guards, so its reads are the
#   plain `git` with `--no-replace-objects` and `GIT_NO_REPLACE_OBJECTS=1` (so no `refs/replace/*` ref and no
#   `GIT_REPLACE_REF_BASE` of the caller rewrites the ancestry it reads), `GIT_GRAFT_FILE=/dev/null` (so neither
#   `.git/info/grafts` nor a `GIT_GRAFT_FILE` of the caller grafts a parent onto a commit it walks: git reads that
#   file in place of `info/grafts`, and `--no-replace-objects` leaves grafts alone, audit round 5 P1; pr-audit.sh
#   closes the same channel by refusing a grafts file in its fresh repository, which a hook in the user's checkout
#   cannot) and `-c core.hooksPath=/dev/null` (so they run no hook), with a `# git-isolated: allow` reason; it writes
#   nothing but its own stderr and runs no network command.
#   The isolated git of the levers (git-isolated.sh, the same flags) never runs it, so records-sync.sh and the other
#   levers are untouched. A transaction line whose new value is the commit the ref already names is a backend update,
#   not a move, and passes: the files backend writes a ref it packs as a creation, `<zero> <value> <ref>`, measured
#   on git 2.56 `pack-refs --all` and `gc`, so the hook reads the ref (`rev-parse --verify -q`) when the old value is
#   zero; a creation of a ref that does not exist is judged like any move.
#   `checkout-guard.sh check <checkout>` reports `installed` (byte-equal to the copy here and executable), `absent`,
#   `older` (byte-equal to an earlier hook text this lever wrote: its sha256 is in EARLIER_HOOKS, the pre-move lever
#   7b570792's first, regime-cutover U219b), `differs` or `not-executable` for the hook, `installed` (byte-equal, a
#   regular file), `absent` or `differs` for the
#   marker, and `stale` for a round-1 `pre-commit` or `post-checkout` still
#   there (byte-equal to round 1's, kept in write_hook for this comparison alone); exit 0 when the hook and the marker are installed
#   and nothing is stale, else 1; a symlink or a file that is not a regular file at the hook path is a refusal (exit
#   2) naming the kind, which `check` does not judge, while a regular file of other content is `differs`. `install`
#   refuses (exit 2, nothing written) unless `<checkout>` is in a main checkout (`git rev-parse --git-dir` equals
#   `--git-common-dir`; a linked worktree's hooks directory is the main checkout's, so it is installed there). The
#   hook goes into `<git-common-dir>/hooks` as the isolated git (git-isolated.sh, U113) names it, with the caller's
#   `GIT_*` and transport variables scrubbed first so no `GIT_DIR` or `GIT_COMMON_DIR` of the caller points the reads
#   at another repository, and each path git prints read whole through one helper (git_path: a sentinel after the
#   output, so the trailing newline a command substitution strips stays and only git's own line end is removed; a
#   separate git directory whose name ends in LF is installed into, not its stripped sibling, audit round 5 P2); the
#   directory is made when absent, and a directory this run made is removed again (`rmdir`, so one that existed
#   before is never touched) when a later step fails before the rename (U135). Nothing here reads `core.hooksPath`:
#   rounds 2 to 4
#   each tried to establish at install time what git resolves for it at the next commit, and each audit named another
#   channel (`GIT_CONFIG_COUNT`; `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`; `GIT_CONFIG`, `GIT_DIR`,
#   `includeIf.onbranch`), since git's configuration is layered and conditional and the caller owns every layer, so
#   the check cannot hold and round 5 removed it; where git resolves its hooks is the trust boundary below. The hooks
#   directory, when it exists, must be a directory that can be read (a mode-000 one is a refusal naming it, never
#   `absent`), and the hook path absent, already this lever's own, or an earlier hook of this lever's (`older`, which
#   the same staged write replaces, printing `upgraded`); a regular file of other content there is
#   refused and never overwritten. The write is one rename per file: the hook's bytes go to a temporary file in the hooks
#   directory (`mktemp` there), its mode is set, it is read back (`cmp -s` against the scratch copy, the execute bit),
#   the marker's bytes go to a second temporary file the same way (mode 0644, read back), and one `mv` each puts them
#   at the hook path and then the marker path; a failure at any step before the first rename exits 2 with both paths exactly
#   as found (absent stays absent, this lever's own hook that lacked its execute bit keeps its bytes) and the EXIT trap
#   removes the temporary files (audit round 5 P2: writing the hook path in place left an empty, a non-executable or an
#   unverified hook behind a refusal); a failed rename of the marker after the hook's leaves the hook in place. After the hook and the marker are in place it removes a round-1 `pre-commit` or `post-checkout`
#   that is byte-equal to round 1's (`removed` rows; the `pre-commit` in either of the two byte forms round 1 wrote,
#   see write_hook), so an upgraded checkout keeps no dead hook; any other file at those two paths is not this
#   lever's and is left alone. A second run finds its own hook and marker, prints `unchanged` for each and exits 0, so regime-init calls
#   it on every run. Every comparison is `cmp -s` against a copy of the expected bytes written to a scratch directory
#   (NUL-safe: a shell variable cannot hold the NUL a drifted file may), its status read: 0 is equal, 1 is different,
#   anything else is a failed read and a refusal. Every read and write is checked (standing order 21): each `mktemp`,
#   each `git rev-parse` (the toplevel, the git directory, the common directory), each write of the expected bytes
#   (`cat`), each `cmp`, the `mkdir` of the hooks directory, the `chmod`, the `mv`, the `rm` of a round-1 hook; each
#   failure exits 2 naming the file. Left out, by design: a worker that edits `.git/hooks` of the
#   checkout (the worker tree is a repository of its own and never sees this hook); a branch made a symbolic ref
#   (`symbolic-ref refs/heads/main refs/tags/x`: the next commit moves the tag, which the rule does not name); a copy
#   or rename of a branch that is already off origin (`branch -c`, `branch -m`: no branch moves to a new commit); a
#   commit on a detached HEAD (no branch moves; the rule names local branches); and a repository with no `origin`
#   remote, where no commit is reachable and every branch move is refused while a store exists.
#   Trusted: the worker is a non-adversarial actor whose reflex the refusal stops, not an attacker: git resolving its
#   hooks to another place under the caller's configuration or environment, whenever and however set, is a
#   standing-order breach the records catch, not a defect this hook closes (the boundary U123 drew for the worker
#   tree); so is a worker who replaces a branch with a symbolic ref or copies a branch that is already off origin.
#   The coordinator is the only committer in the checkout and commits nothing there by design (records move
#   through records-sync.sh's scratch repository, code through worker trees); git runs the common
#   `hooks/reference-transaction` for the checkout and every linked worktree when it resolves no `core.hooksPath`, and
#   resolves symbolic refs before the `prepared` phase (githooks(5)); `refs/remotes/origin/*` are origin's refs,
#   whatever wrote them; `python3` on the hook's PATH is a CPython 3; the worker's identity is not read.
# @arg $1 string `install` or `check`.
# @arg $2 string The checkout: a directory inside the main worktree of the repository.
# @stdout One row per file, `checkout-guard: <state>\t<path>`, the hook's then the marker's: `installed`, `upgraded` (the hook alone: an `older` hook replaced), `unchanged` or `removed` (install); `installed`, `absent`, `differs`, `older` and `not-executable` (the hook alone) or `stale` (check). regime-init matches the `checkout-guard: installed` and `checkout-guard: removed` rows at line start.
# @exitcode 0 Done: the hook and the marker installed and no stale round-1 hook left (install), or both in place with nothing stale (check).
# @exitcode 1 `check`: the hook or the marker is absent or differs, the hook is an earlier hook of this lever's (`older`) or is not executable, or a round-1 hook is still there.
# @exitcode 2 A refusal: usage, not a main checkout, a hooks directory that cannot be read, a symlink or a non-regular file at the hook path or the marker path (`check` too), a regular file of other content at either (`install`), a failed read, a failed write step before the hook's rename (both paths are as they were found and a hooks directory this run made is removed again; a failed rename of the marker, or a failed removal of a round-1 hook, comes after the hook's rename and leaves the hook in place), or the manifest pin differing from this file.
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
marker=regime-coordinator
# The sha256 of each earlier `reference-transaction` text this lever wrote, the pre-move lever's (origin/main 7b570792,
# U215 merged) first: a regular file at the hook path whose bytes hash to one of them is `older` (regime-cutover U219b,
# verdict U219-ce7e875e P2), which `install` replaces through the same staged write (`upgraded` row) and `check`
# reports with exit 1; bytes of neither this lever's nor an earlier text stay `differs`, refused and never overwritten.
# A later hook text appends the digest of the one it replaces here. The digest is read by file_digest, its status read.
EARLIER_HOOKS=(3792cacd54e3aace38d124facc7388f395da55675cafb55de355be76942e7f0f)
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

# The lever's reads run through the isolated git (U113), with the caller's `GIT_*` and transport variables removed
# first: a `GIT_DIR` or `GIT_COMMON_DIR` of the caller would point them at another repository, and the hook goes where
# this git names the common hooks directory of the checkout. Each read's status is checked (standing order 21); the
# toplevel read fails for a path outside a working tree too, and git's stderr names which.
[[ -r ${LEVER_DIR}/git-isolated.sh ]] || refuse "git-isolated.sh unreadable beside this script: ${LEVER_DIR}/git-isolated.sh"
# shellcheck source=scripts/orchestrator/git-isolated.sh
. "${LEVER_DIR}/git-isolated.sh"
scratch=$(mktemp -d "${TMPDIR:-/tmp}/checkout-guard.XXXXXX") || refuse 'cannot make a scratch directory for the expected hook bytes'
# The temporary files of the install below, while they exist: made in the hooks directory, renamed onto the hook path
# and the marker path on success, removed here on a refusal before the rename.
staged='' staged_marker=''
# The hooks directory, while this run has made it and not yet renamed the hook into it (U135: a failed install left
# the directory it had made); `rmdir` removes an empty directory alone, so one that existed before is never touched.
made_hooks=''
# The scratch directory and the temporary files a refusal left go on exit. A removal that fails is named on stderr and
# does not replace the exit status (a command that fails inside an EXIT trap would).
cleanup() {
    [[ -z ${staged} ]] || rm -f -- "${staged}" || echo "${lever}: ${staged} could not be removed" >&2
    [[ -z ${staged_marker} ]] || rm -f -- "${staged_marker}" || echo "${lever}: ${staged_marker} could not be removed" >&2
    [[ -z ${made_hooks} ]] || rmdir -- "${made_hooks}" || echo "${lever}: ${made_hooks} could not be removed" >&2
    rm -rf -- "${scratch}" || echo "${lever}: ${scratch} could not be removed" >&2
}
trap cleanup EXIT
# shellcheck disable=SC2119 # no name is kept: every GIT_* and transport variable goes
git_env_scrub

# @description Read into the variable named $1 the one path the isolated git query $2... prints, every byte of it:
#   the output is taken with a sentinel after it (`&& printf x`, removed after), so the trailing newline a command
#   substitution would strip stays, and exactly the one LF git ends its line with is removed. A separate git
#   directory whose name ends in LF is then itself, not its stripped sibling (audit round 5 P2). git's status comes
#   through the `&&`; git's stderr goes to the scratch directory's `stderr` file for the caller's refusal to print.
# @arg $1 string The variable that receives the path.
# @arg $@ string The arguments of git_isolated.
# @exitcode 0 The variable holds the path.
# @exitcode 1 git exited non-zero or printed no line; the variable is not written.
git_path() {
    local gp_name=$1 gp_out
    shift
    gp_out=$(git_isolated "$@" 2> "${scratch}/stderr" && printf x) || return 1
    gp_out=${gp_out%x}
    [[ ${gp_out} == *$'\n' ]] || return 1
    printf -v "${gp_name}" '%s' "${gp_out%$'\n'}"
}

# The three paths git_path fills (`printf -v`), declared here so each read's failure is the refusal beside it.
toplevel='' git_dir='' common=''
git_path toplevel -C "${checkout}" rev-parse --show-toplevel || refuse "cannot read the toplevel of ${checkout} (is it inside a git working tree?): $(< "${scratch}/stderr")"
git_path git_dir -C "${checkout}" rev-parse --path-format=absolute --git-dir || refuse "cannot read the git directory of ${toplevel}"
git_path common -C "${checkout}" rev-parse --path-format=absolute --git-common-dir || refuse "cannot read the git common directory of ${toplevel}"
# The one comparison of two paths: both are git's absolute forms for one checkout, read whole by git_path (a trailing
# newline of the name kept), equal byte for byte in a main checkout and differing by the `worktrees/<id>` tail in a
# linked one.
[[ ${git_dir} == "${common}" ]] || # lint-comparisons: allow both sides are git's absolute forms of one checkout
    refuse "${toplevel} is a linked worktree (git dir ${git_dir}, common ${common}); install in the main checkout, whose hooks every linked worktree shares"
hooks=${common}/hooks
[[ ! -L ${hooks} ]] || refuse "${hooks} is a symlink; nothing is written through it"

# @description Write the text of hook $1 to the path $2: the quoted heredocs below, so nothing in them expands here,
#   each redirected straight into the file (a command substitution would re-parse the body: bash 3.2 and others
#   expand `$'…'` inside a quoted heredoc there, which is how round 1's installed `pre-commit` came to differ from its
#   heredoc by that one token). `regime-coordinator` is the marker's one line (U219). `pre-commit` and `post-checkout` are round 1's hooks, kept so an upgraded checkout's
#   copies are recognised and removed, never installed: `pre-commit` in the heredoc's own bytes and, as
#   `pre-commit.subst`, in the bytes round 1 wrote through its command substitution (`$'\n'` already a newline inside
#   the quotes); `post-checkout` holds no such token and has one form. A failed write is a refusal naming the path.
# @arg $1 string `reference-transaction`, `regime-coordinator`, `pre-commit`, `pre-commit.subst` or `post-checkout`.
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
# the transaction (exit 1, the route to a worker tree on stderr) while the marker `regime-coordinator` lies beside this
# file as a regular file (regime-cutover U219: written by checkout-guard.sh install into the common hooks directory,
# which every worktree shares and every seat is write-denied; read by `os.lstat` from this file's own directory, so a
# symbolic link, a directory or any other kind there is no marker; the trigger once the live store has left the
# checkout, U221) or a program store
# `.orchestration/orchestrate/<program>/units.tsv` exists under this worktree's toplevel or under the main checkout's
# (the pre-move trigger, which U221 removes; this worktree when its git directory is the common directory, else the parent of a common directory named `.git`,
# as git-worktree(1) derives the main worktree; `worktree list` is not read, U135, since it named a separate git
# directory reached through a `.git` symlink as the main worktree and a linked worktree's moves passed; from a linked
# worktree whose common directory is not named `.git` every move is refused naming it, never passed) and any line
# (each value 40 or 64 lowercase hex or `ref:<ref-target>`, else the line is refused naming the value) moves a
# `refs/heads/*` ref to a commit that no `refs/remotes/origin/*` ref reaches. That is every
# commit authored here (commit, --amend, merge, cherry-pick, rebase; `--no-verify` skips no reference-transaction),
# while `pull --ff-only`, `reset --hard origin/<branch>`, `fetch`, a branch deleted or made at origin's commit, a line
# whose new value is the commit the ref already names (a backend update: `pack-refs` and `gc` write a packed ref as
# `<zero> <value> <ref>` on git 2.56, so the ref is read when the old value is zero; no branch moves), and every ref outside
# refs/heads/ (a detached HEAD, tags, remote-tracking refs, ORIG_HEAD, the stash) pass. The other phases exit 0. It
# runs under `python3 -I -S`: no shell starts, so no shell startup file, SHELLOPTS or BASH_ENV reaches it, and no
# PYTHON* variable, site directory or module planted beside it is read. A read that fails refuses the transaction
# (standing order 21): the marker's directory that cannot be read, `.orchestration`, `orchestrate` or a program directory that cannot be listed (each is listed
# in that order, to the last program directory), a line of another shape, a git read that exits non-zero. Its git
# calls carry `--no-replace-objects` and `GIT_NO_REPLACE_OBJECTS=1`, so no `refs/replace/*` ref and
# no `GIT_REPLACE_REF_BASE` of the caller stands in for a commit when the ancestry is read, `GIT_GRAFT_FILE=/dev/null`,
# so neither `.git/info/grafts` nor a `GIT_GRAFT_FILE` of the caller grafts a parent onto a commit that read walks
# (`--no-replace-objects` leaves grafts alone), and `-c core.hooksPath=/dev/null`, so they run no hook; the isolated
# git of the levers (the same flags) never runs this file. It writes nothing but its own stderr.
import os
import stat
import subprocess
import sys

ROUTE = (
    "commits belong in a worker tree: ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one "
    "under $TMPDIR/dotfiles-wt/<unit> (standing order 29)"
)
# A hook runs inside the user's git and cannot isolate itself from the repository it guards; the flag keeps its own
# reads from running any hook, this file included.
# git-isolated: allow a hook cannot isolate itself from its repository
GIT = ("git", "--no-replace-objects", "-c", "core.hooksPath=/dev/null")
# The environment of every read: the hook's own plus git's switches for the same things. A replacement ref is read by
# neither form (git-replace(1): `--no-replace-objects` or `GIT_NO_REPLACE_OBJECTS`), and the grafts file is /dev/null:
# git reads the file GIT_GRAFT_FILE names in place of `.git/info/grafts`, so neither that file nor one the caller
# names grafts a parent onto a commit the ancestry read walks (`--no-replace-objects` leaves grafts alone).
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", GIT_GRAFT_FILE="/dev/null")
ZERO = (b"0" * 40, b"0" * 64)
MARKER = b"regime-coordinator"


def refuse(reason):
    sys.stderr.write("checkout-guard reference-transaction: %s; the update is refused (standing order 21)\n" % reason)
    sys.exit(1)


def git(*args):
    """(exit status, stdout bytes, stderr text) of one git read; a git that cannot start refuses."""
    try:
        run = subprocess.run(GIT + args, stdin=subprocess.DEVNULL, capture_output=True, check=False, env=ENV)
    except OSError as error:
        refuse("cannot run git %s: %s" % (" ".join(args), error))
    return run.returncode, run.stdout, run.stderr.decode("utf-8", "replace").strip()


def read(*args):
    """The stdout bytes of one git read; a non-zero exit refuses the transaction naming the read."""
    status, out, err = git(*args)
    if status != 0:
        refuse("git %s exited %d: %s" % (" ".join(args), status, err))
    return out


def object_id_or_symbolic(value):
    """Whether VALUE is an object id, 40 or 64 lowercase hex (SHA-1 or SHA-256), or a symbolic value `ref:<ref-target>`
    (githooks(5)); anything else is malformed, and the hook refuses rather than judge it."""
    if value.startswith(b"ref:"):
        return len(value) > len(b"ref:")
    return len(value) in (40, 64) and all(c in b"0123456789abcdef" for c in value)


def updates(data):
    """The (old, new, ref) of each line of DATA in the shape githooks(5) documents, each value an object id of 40 or 64
    lowercase hex or `ref:<ref-target>`; any other shape or value refuses naming it (U135: `not-an-oid` passed when
    the field count alone was read)."""
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    result = []
    for line in lines:
        fields = line.split(b" ")
        if len(fields) != 3 or not all(fields):
            refuse("a line of the transaction is not <old-value> SP <new-value> SP <ref-name>: %r" % line)
        for value in fields[:2]:
            if not object_id_or_symbolic(value):
                refuse(
                    "a value of the transaction is not an object id of 40 or 64 lowercase hex or ref:<ref-target>: %r"
                    % value
                )
        result.append((fields[0], fields[1], fields[2]))
    return result


def path_line(*args):
    """The one path a git read prints, exactly its line end removed: a path may itself end in LF (audit round 5 P2),
    so one trailing LF goes, never more; no line at all refuses."""
    out = read(*args)
    if not out.endswith(b"\n"):
        refuse("git %s printed no path" % " ".join(args))
    return out[:-1]


def marker_beside(hooks_dir):
    """Whether the coordinator marker `regime-coordinator` (regime-cutover U219) lies in HOOKS_DIR, this hook's own
    directory, as a regular file: `lstat`, never a link followed, so a symbolic link (whatever it points at), a
    directory or any other kind is no marker and an absent one is none; any other `OSError` on the read (a directory
    that cannot be searched) refuses the transaction, never passes it (standing order 21). checkout-guard.sh install
    writes the marker into the common hooks directory, which every worktree of the checkout shares and every seat is
    write-denied, so the guard fires wherever the records live."""
    path = os.path.join(hooks_dir, MARKER)
    try:
        found = os.lstat(path)
    except FileNotFoundError:
        return False
    except OSError as error:
        refuse("cannot read %s: %s" % (os.fsdecode(path), error.strerror or error))
    return stat.S_ISREG(found.st_mode)


def store_under(top):
    """Whether `.orchestration/orchestrate/<program>/units.tsv` exists under TOP. The walk lists `.orchestration`,
    then `orchestrate`, then every program directory, in that order and to the end: the listing is the read, never a
    `stat` of a child (which a mode-0111 directory answers while refusing a listing), and no program directory is
    skipped once a store is found. An absent `.orchestration` or `orchestrate` is no store; any other `OSError` on
    any of those listings (mode 000 or 0111, a file where `.orchestration` or `orchestrate` should be) refuses the
    transaction, never passes it (standing order 21). A file among the program directories is not a program."""
    root = os.path.join(top, b".orchestration")
    stores = os.path.join(root, b"orchestrate")
    for directory in (root, stores):
        try:
            names = os.listdir(directory)
        except FileNotFoundError:
            return False
        except OSError as error:
            refuse("cannot read %s: %s" % (os.fsdecode(directory), error.strerror or error))
    found = False
    for name in sorted(names):
        program = os.path.join(stores, name)
        try:
            entries = os.listdir(program)
        except (FileNotFoundError, NotADirectoryError):
            continue
        except OSError as error:
            refuse("cannot read %s: %s" % (os.fsdecode(program), error.strerror or error))
        if b"units.tsv" in entries:
            found = True
    return found


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


def current(ref):
    """The commit REF names now, or None when there is no such ref: `rev-parse --verify -q` exits 0 with the object
    name and 1 for no such ref; any other status is a failed read and refuses."""
    status, out, err = git("rev-parse", "--verify", "-q", ref)
    if status == 0:
        return out.strip()
    if status == 1:
        return None
    refuse("git rev-parse --verify -q %s exited %d: %s" % (ref.decode("utf-8", "replace"), status, err))


def main():
    data = sys.stdin.buffer.read()
    if len(sys.argv) != 2 or sys.argv[1] != "prepared":
        return 0
    moves = [
        (old, new, ref)
        for old, new, ref in updates(data)
        if ref.startswith(b"refs/heads/") and new not in ZERO and not new.startswith(b"ref:") and old != new
    ]
    if not moves:
        return 0
    toplevel = path_line("rev-parse", "--show-toplevel")
    git_dir = path_line("rev-parse", "--path-format=absolute", "--git-dir")
    common = path_line("rev-parse", "--path-format=absolute", "--git-common-dir")
    # The main checkout: this worktree when its git directory is the common directory (the installer's own test),
    # else the parent of a common directory named `.git`, as git-worktree(1) derives the main worktree. `worktree
    # list` is not read (U135): it named a separate git directory reached through a `.git` symlink as the main
    # worktree, so a linked worktree's moves missed the store and passed. From a linked worktree of such a directory
    # git records no name for the main checkout, and the move is refused naming the directory, never passed.
    tops = [toplevel]
    if git_dir != common:
        parent, name = os.path.split(common)
        if name != b".git":
            refuse(
                "the git common directory %s of this linked worktree is not a .git directory, so git records no name "
                "for the main checkout whose store would be read" % os.fsdecode(common)
            )
        if parent != toplevel:
            tops.append(parent)
    # The marker first (U219): a regular file beside this hook, read from the directory git ran it from; then the
    # pre-move trigger, a store under a toplevel (U221 removes it). Every toplevel is walked before that decision: a
    # store that cannot be read under one of them refuses even when the other holds a readable store (no
    # short-circuit).
    hooks_dir = os.path.dirname(os.path.abspath(os.fsencode(__file__)))
    if not marker_beside(hooks_dir) and not any([store_under(top) for top in tops]):
        return 0
    candidates = origin_commits()
    for old, new, ref in moves:
        # The files backend writes a ref it packs as a creation, `<zero> <value> <ref>` (measured on git 2.56
        # `pack-refs --all` and `gc`): a line whose new value is the commit the ref already names moves no branch.
        if old in ZERO and current(ref) == new:
            continue
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
    regime-coordinator)
        cat << 'REGIME_COORDINATOR' > "$2" || refuse "cannot write $2"
regime-cutover U219: this checkout is the coordinator's
REGIME_COORDINATOR
        ;;
    *) refuse "no hook named $1" ;;
    esac
}

# The expected bytes of each hook, written once to the scratch directory so every comparison below is `cmp -s`, which
# reads every byte of both files (a command substitution would drop a NUL).
for name in "${hook}" "${legacy_hooks[@]}" pre-commit.subst "${marker}"; do
    write_hook "${name}" "${scratch}/${name}"
done

# @description Set `digest` to the sha256 of the file $1, read on stdin by `sha256sum` when there is one, else by
#   `shasum -a 256` (the self-check's pair; on stdin, so no file name is escaped into the output), its status read: a
#   tool that fails, or prints no digest, is a failed read and never a digest (standing order 21).
# @arg $1 string The path.
# @set digest 64 lowercase hex.
# @exitcode 1 The tool failed or printed no digest; `digest` is empty.
file_digest() {
    local out
    digest=''
    if command -v sha256sum > /dev/null; then
        out=$(sha256sum < "$1") || return 1
    else
        out=$(shasum -a 256 < "$1") || return 1
    fi
    digest=${out%% *}
    [[ ${digest} =~ ^[0-9a-f]{64}$ ]]
}

# @description Judge the file at $1 against hook $2: `state` is `absent` (nothing there), `own` (a regular file
#   holding exactly this lever's bytes), `older` (the hook alone: a regular file whose sha256 is in EARLIER_HOOKS, an
#   earlier hook text this lever wrote, U219b), `differs` (a regular file of any other content) or, for a file that is not
#   judged, its kind: `a symlink` (whatever it points at: nothing is written through one), `a directory`, `a fifo`,
#   `a socket`, `a device` or `not a regular file`; `executable` is 1 when a regular file has its owner's execute
#   bit. The comparison is `cmp -s` against the scratch copy, and for `pre-commit` against both of its forms: 0 equal,
#   1 different, anything else a failed read and a refusal, never an absence (standing order 21).
# @arg $1 string The path.
# @arg $2 string The hook name.
# @set state `absent`, `own`, `older` (the hook alone), `differs` or the kind of a file that is not judged.
# @set executable 0 or 1.
hook_state() {
    local target=$1 name=$2 same form earlier
    executable=0
    if [[ -L ${target} ]]; then
        state='a symlink'
        return 0
    fi
    if [[ ! -e ${target} ]]; then
        state=absent
        return 0
    fi
    if [[ ! -f ${target} ]]; then
        if [[ -d ${target} ]]; then
            state='a directory'
        elif [[ -p ${target} ]]; then
            state='a fifo'
        elif [[ -S ${target} ]]; then
            state='a socket'
        elif [[ -b ${target} || -c ${target} ]]; then
            state='a device'
        else
            state='not a regular file'
        fi
        return 0
    fi
    state=differs
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
    # The hook alone may be an earlier text of this lever's: its digest against EARLIER_HOOKS, the read a refusal when
    # the hash tool fails (never `differs`, which install refuses as foreign, nor `older`, which it would overwrite).
    case ${name} in
    "${hook}") ;;
    *) return 0 ;;
    esac
    file_digest "${target}" || refuse "cannot hash ${target}"
    for earlier in "${EARLIER_HOOKS[@]}"; do
        if [[ ${digest} == "${earlier}" ]]; then # lint-comparisons: allow two sha256 digests, no path compare
            state=older
            return 0
        fi
    done
}

# The hooks directory is read before anything in it is judged: one that cannot be listed or entered (mode 000) would
# make every path in it read as absent (audit round 2 P3), so it is a refusal naming it, never an absence; a file
# where the directory should be is foreign and refused. An absent directory is made by `install` below.
if [[ -e ${hooks} ]]; then
    [[ -d ${hooks} ]] || refuse "${hooks} exists and is not a directory"
    [[ -r ${hooks} && -x ${hooks} ]] || refuse "cannot read ${hooks}"
fi

# The hook, the marker and the two round-1 paths are judged before anything is written. A symlink or a file that is
# not a regular file at the hook path or the marker path is not judged by either action (audit round 3 P3: `check`
# read both as `differs`): it is a refusal naming the kind, and nothing is written through or over it; a regular file
# of other content is `differs` for `check` and a refusal for `install` below. The marker's execute bit is not
# judged (U219: a regular file of this lever's bytes is the marker). Anything at a round-1 path that is not round 1's
# own is left alone.
hook_state "${hooks}/${hook}" "${hook}"
hook_own=${state} hook_executable=${executable}
case ${hook_own} in
absent | own | older | differs) ;;
*) refuse "${hooks}/${hook} is ${hook_own}, not this lever's hook; ${action} does not judge it and nothing is written through it (move it away by hand, then rerun)" ;;
esac
hook_state "${hooks}/${marker}" "${marker}"
marker_own=${state}
case ${marker_own} in
absent | own | differs) ;;
*) refuse "${hooks}/${marker} is ${marker_own}, not this lever's marker; ${action} does not judge it and nothing is written through it (move it away by hand, then rerun)" ;;
esac
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
    older:*)
        printf 'checkout-guard: older\t%s\n' "${target}"
        missing=1
        ;;
    *)
        printf 'checkout-guard: differs\t%s\n' "${target}"
        missing=1
        ;;
    esac
    case ${marker_own} in
    own) printf 'checkout-guard: installed\t%s\n' "${hooks}/${marker}" ;;
    absent)
        printf 'checkout-guard: absent\t%s\n' "${hooks}/${marker}"
        missing=1
        ;;
    *)
        printf 'checkout-guard: differs\t%s\n' "${hooks}/${marker}"
        missing=1
        ;;
    esac
    for name in "${stale[@]+"${stale[@]}"}"; do
        printf 'checkout-guard: stale\t%s\n' "${hooks}/${name}"
        missing=1
    done
    exit "${missing}"
fi

[[ ${hook_own} != differs ]] || refuse "${hooks}/${hook} exists and is not this lever's hook; it is never overwritten (move it away by hand, then rerun)"
[[ ${marker_own} != differs ]] || refuse "${hooks}/${marker} exists and is not this lever's marker; it is never overwritten (move it away by hand, then rerun)"
if [[ ! -d ${hooks} ]]; then
    mkdir "${hooks}" || refuse "cannot make ${hooks}"
    made_hooks=${hooks}
fi

# The hook path and the marker path are each written by one rename, the hook's first. Unless the hook is already this
# lever's own and executable (an `older` hook, an earlier text of this lever's, is replaced the same way and its row
# is `upgraded`, U219b), its bytes go to a temporary file in the hooks directory (`mktemp` there, so the rename
# stays on one filesystem; a dotfile git runs as no hook), its mode is set, and it is read back (`cmp -s` against the
# scratch copy, the execute bit); unless the marker is already this lever's own, its bytes go to a second temporary
# file the same way (mode 0644, read back; U219). Only then does one `mv` put the hook at its path and one the marker
# at its. A failure at any step before the hook's rename refuses with both paths exactly as found (absent stays
# absent, this lever's own hook that lacked its execute bit keeps its bytes; the trap removes the temporary files):
# writing the hook path in place left an empty, a non-executable or an unverified hook behind a refusal (audit round
# 5 P2). A failed rename of the marker after the hook's leaves the hook in place and is named.
target=${hooks}/${hook}
marker_target=${hooks}/${marker}
hook_row=unchanged marker_row=unchanged
if [[ ${hook_own} != own || ${hook_executable} != 1 ]]; then
    staged=$(mktemp "${hooks}/.${hook}.XXXXXX") || refuse "cannot make a temporary file in ${hooks} for the hook"
    write_hook "${hook}" "${staged}"
    chmod 755 "${staged}" || refuse "cannot make ${staged} executable"
    hook_state "${staged}" "${hook}"
    [[ ${state} == own && ${executable} == 1 ]] || refuse "${staged} reads back as ${state} (executable: ${executable}) after the write; ${target} is as it was"
    hook_row=installed
    [[ ${hook_own} != older ]] || hook_row=upgraded
fi
if [[ ${marker_own} != own ]]; then
    staged_marker=$(mktemp "${hooks}/.${marker}.XXXXXX") || refuse "cannot make a temporary file in ${hooks} for the marker"
    write_hook "${marker}" "${staged_marker}"
    chmod 644 "${staged_marker}" || refuse "cannot make ${staged_marker} mode 0644"
    hook_state "${staged_marker}" "${marker}"
    [[ ${state} == own ]] || refuse "${staged_marker} reads back as ${state} after the write; ${marker_target} is as it was"
    marker_row=installed
fi
if [[ -n ${staged} ]]; then
    mv -f -- "${staged}" "${target}" || refuse "cannot move ${staged} onto ${target}"
    staged=''
fi
made_hooks=''
printf 'checkout-guard: %s\t%s\n' "${hook_row}" "${target}"
if [[ -n ${staged_marker} ]]; then
    mv -f -- "${staged_marker}" "${marker_target}" || refuse "cannot move ${staged_marker} onto ${marker_target}"
    staged_marker=''
fi
printf 'checkout-guard: %s\t%s\n' "${marker_row}" "${marker_target}"

# The round-1 hooks go only after the new hook and its marker are in place, so no run leaves the checkout unguarded.
for name in "${stale[@]+"${stale[@]}"}"; do
    rm -- "${hooks}/${name}" || refuse "cannot remove the round-1 ${hooks}/${name}"
    [[ ! -e ${hooks}/${name} ]] || refuse "${hooks}/${name} is still there after its removal"
    printf 'checkout-guard: removed\t%s\n' "${hooks}/${name}"
done
