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
#   The tree's owner record (regime-cutover U509, U509e, U509f; standing order 27, one writer per tree): twice on 2026-11-12
#   and twice on 2026-11-13 a worker that had been cancelled kept editing while its successor was dispatched into the
#   same tree (decisions.tsv lessons 2026-11-12T11:31:15Z and 2026-11-13T01:39:15Z); the rule was prose and failed
#   four times, so it is a refusal of this tool. `claim <unit> <owner> [--stale <minutes>]` writes
#   `<root>/<unit>/.git/regime-owner`, the two lines `owner=<name>` (over `[A-Za-z0-9._-]{1,64}`, matched whole) and
#   `claimed=<YYYY-MM-DDTHH:MM:SSZ>`, mode 0600; its presence is the claim, and it lives under the tree's `.git`
#   under a name git never writes, so no worker commit or `git status` sees it. Liveness is the record's age against
#   `--stale` (default 20 minutes, the 10-minute progress rule doubled; 1 to 6 digits): a younger record refuses the
#   claim with exit 3, a code of its own, naming the owner, the claim time and the age; an older one is taken over
#   with one stdout line naming the stale owner (a dead worker leaves a record; the coordinator's kill path runs
#   `release`, and a crash is covered by the age). Both claim lines end in `claimed=<stamp>`, the claim time, which
#   the release presents: `release <unit> <owner> <claimed>` removes the record when it holds that owner and that
#   claim time, refuses with exit 3 when it holds another claim (another name, or the same name's later claim: round
#   2 compared the name alone, and the names are reused, so a successor that reused its predecessor's name had its
#   fresh claim deleted by the predecessor's delayed release; verdicts/U509e-d8529b25.md, U509f), and prints `no claim
#   <unit>` with exit 0 when there is none, so the coordinator's kill path can always run it. The coordinator claims
#   right after the creation subcommand and before every dispatch, keeps the claim time the line printed, and
#   releases with it after the worker's return or kill; the creation subcommand does not claim,
#   so a tree made for one owner and dispatched to another still passes through `claim`. The tree is `<root>/<unit>`
#   as the creation subcommand places it (the same root checks). Every record operation runs in one program,
#   `worker-worktree-owner.py` beside this file (pinned like this file; the lever reads its bytes once, hashes them
#   against the pin and runs those same bytes, acting on the exit status alone), the form of `ledger-row.py` and
#   `profile-config-place.py`: the tree and its `.git` opened `O_DIRECTORY | O_NOFOLLOW` (the open is the check; a
#   link at either name refuses, exit 2) and `fstat`ed as a directory of this user, every later name relative to that
#   descriptor; one `flock` on `regime-owner.lock` beside the record (created 0600 and `fchmod`ed after the open, so
#   the umask never leaves a lock no later run can open; it stays; an ENOENT from the open, macOS's answer to the
#   loser of a concurrent first creation through one directory descriptor, is retried up to 10 times 0.05 s apart
#   before it is a refusal, verdicts/U509f-f21a9f7f.md P2 :269, U509g) held over the read, the decision and the write
#   or removal, so of two claimers on one stale record exactly one takes over and the other reads the fresh record
#   and is refused, and a release delayed past a successor's claim reads a claim it does not present and is refused;
#   the record read as bytes and matched whole (a NUL or any byte outside the two lines is malformed, refused and
#   left for the operator; the stamp parsed with `strptime` and printed back, so 2026-02-31 is malformed); every
#   write an exclusive 0600 temporary written, synced and renamed over the record, a failed step removing the
#   temporary with exit 1 and the previous record standing; every argument grammar matched whole (`re.fullmatch`: a
#   value ending in a newline is outside it) and every refusal one stderr line, a rejected value folded into it with
#   its newline escaped. Round 1 (verdicts/U509-e343a569.md) kept these steps in the shell: the read and the write
#   were unheld between them, `$(…)` dropped a NUL, `((10#n))` overflowed, a day of 31 passed in every month, and a
#   failed write left an empty record with exit 3. These subcommands run no git, and the record and its lock file are
#   all they write or remove.
#   The dispatch text and the return check (regime-cutover U573; standing orders 27 and 29). On 2026-11-17 two
#   round-2 workers worked outside the tree their dispatch named: one edited the sweep seat's checkout under the
#   seats root, one made a linked worktree of the main checkout at `/private/tmp/dotfiles-wt/<unit>` and left a
#   local branch there. Neither ever ran a command on the given path (decisions.tsv lessons 2026-11-17T16:10:24Z and
#   17:24:01Z, the WorkerTreeReader row); both looked for the round-1 commit with `git worktree list`, which cannot
#   show a worker tree, and the path lived in a hand-written prompt alone. So the path reaches the worker through one
#   rendered text, and the return is checked by one command. `task <unit> <brief> [--round <text>]` prints the task
#   text the coordinator pastes into the worker's Task call: line 1 `Tree: <root>/<unit> (every command runs here;
#   your first command is \`cd <tree> && pwd -P\`, and the report's first line is its output)`, then the brief (an
#   absolute path to a readable file), the branch the tree is on (the full ref `symbolic-ref HEAD` prints in the tree,
#   `refs/heads/` stripped: `--short` would print `heads/<name>` beside a tag of the same name, and the lookups below
#   would miss the branch) with the base it was made from (the oldest reflog entry of that branch, the commit
#   `checkout -b` made it at, which `git fetch origin` in the tree never moves), the no-push rule, the forbidden paths
#   (the main checkout by its physical path and every seat checkout under `regime-env`'s seats root, the directories
#   there not beginning with `.`, each by name), the note that the tree is a repository of its own that `git worktree
#   list` cannot show, and the round text when given. The tree must exist and be this lever's: `.git` a directory and
#   no symbolic link (a linked worktree holds a file there), `objects/info/alternates` naming the checkout's objects
#   directory by identity (device and inode), `remote.origin.url` the checkout's and `remote.origin.pushurl` the
#   refusal, else the refusal names the tree (exit 2), so a task is never rendered for a tree that is not there.
#   `verify <unit>` is the coordinator's check after the worker's return: exit 0 when (a) the main checkout's `git
#   worktree list --porcelain -z`, read NUL-separated so a path holding a newline is one entry, names no worktree at
#   or under `$DOTFILES_WT` as placed or `${TMPDIR}/dotfiles-wt`, judged by identity (the listed path and each
#   directory above it against each root with `-ef`, device and inode, after the directories on the way are held
#   searchable, so a case alias or a link that names the root is the root; round 2 compared spellings, and a root
#   spelled in another letter case on a case-insensitive volume passed over the tree under it, verdict U573-5f983ea2
#   P2 :677), then by spelling for an entry whose directory and root are both gone (as printed and as `pwd -P`
#   resolves it), and none whose path, in either form, has a `dotfiles-wt` component: the default root under any
#   other TMPDIR (the system's temporary directory, where U566's stray worktree stood) is covered so, and the lever
#   spells no temporary directory of its own, which the repository's sandbox-portability guard refuses in a tracked
#   script (a lever-made tree is a repository of its own and never appears in that list, so every such entry is
#   foreign; the main worktree, listed first, is the checkout itself and is not judged); and (b) every seat checkout
#   under the seats root has nothing changed, deleted, untracked or staged: `git ls-files -z -m -d -o
#   --exclude-standard --deduplicate` and `git diff-index --cached --name-only -z HEAD`, under `-c
#   core.fsmonitor=false -c core.hooksPath=/dev/null --no-optional-locks` and with every filter driver the seat's
#   config defines closed by name (`-c filter.<name>.clean= -c filter.<name>.smudge= -c filter.<name>.process= -c
#   filter.<name>.required=false` for each `filter.<name>.*` its config lists), so the read writes nothing in the
#   seat, not even its index, and runs nothing of the seat's: no fsmonitor, no hook, no clean or smudge filter (round
#   2's `git status` hashed a same-length change through the seat's clean filter, which wrote a file during the
#   check, P2 :700 and Codex thread 4604459522; `ls-files -m` hashes such a change too, so the drivers are closed
#   rather than the read trusted). A stray worktree's branch is read from its `branch refs/heads/<name>` line in the
#   same list, and that worktree's clearing step names `git branch -D <name>` after the `worktree remove`, the
#   leftover of that stray add alone; round 2 judged a local branch of the checkout named like the tree's as such a
#   leftover, and the checkout may hold that branch from before the tree was made (the creation subcommand's own test
#   makes a tree on a branch the checkout holds), so that rule, whose advice could discard commits, is gone (Codex
#   thread 4604357806). Each failure is one stdout line naming the path (a newline, carriage return, vertical tab or
#   form feed in it escaped, `\n` and the like, so the line is one line for any reader; the command names the path
#   exactly, quoted for the shell) and the step that clears it, every finding printed once every read is done (a
#   refusal leaves nothing on stdout), exit 1; a read that fails (the worktree list, a seats root or a directory
#   above it that cannot be searched or listed, a link on the way whose target or a directory above the target
#   cannot be searched, a file where a directory should be (ENOTDIR), a seat whose status or filter drivers cannot
#   be read, a seat directory that is no repository, the tree's branch or its reflog, a directory above a listed
#   worktree that cannot be searched) is a refusal with exit 2 naming it, never an absence: only a clean ENOENT is
#   one (standing order 21; round 2 of U573, verdicts/U573-32986760.md, and round 3, verdicts/U573-5f983ea2.md, found
#   each of these read as an absence). Both subcommands run from the main checkout, source `regime-env` beside this
#   file after the scrub every git of this lever runs under (`git_env_scrub`: every `GIT_*` name removed, the global
#   and system configuration closed), since regime-env runs git of its own and a caller's `GIT_DIR` would otherwise
#   derive the seats root from another repository and its `GIT_TRACE` would write a file; read regime-env's
#   toplevel through its own `regime_toplevel` with the status judged (`regime_env` keeps that read's failure to
#   itself under an explicit `HCOM_DIR`, round 3 P1 :597) and hand the value read to `regime_env`, which runs in a
#   captured substitution so its refusal reaches stderr through `refuse` as one line (P3 :597); derive the seats
#   root as regime-env documents it (`REGIME_SEATS_ROOT` when set, else `~/.local/state/omp-seats/<slug>`, the slug
#   `regime_slug` prints for that toplevel; an absent root holds no seat) and list it NUL-separated (`find -print0`,
#   so a seat whose name holds a newline is one path, P2 :605); run every other git through `git_run`, print every
#   refusal as one stderr line (a line boundary in interpolated text folded to a space), and write nothing anywhere.
# @arg $3 string The base, a revision the checkout resolves to a commit (`origin/main`).
# @arg $1 string `claim` or `release` selects the owner subcommands (U509): then the unit, the owner's name over
#   `[A-Za-z0-9._-]{1,64}`, and for `claim` an optional `--stale <minutes>` (default 20), for `release` the claim
#   time the claim printed (`claimed=<YYYY-MM-DDTHH:MM:SSZ>`).
# @arg $1 string `task` renders the dispatch text (U573): then the unit and the brief's absolute path, and an optional
#   `--round <text>`; `verify` checks the return (U573): then the unit.
# @env DOTFILES_WT The directory the worker trees live in (default `${TMPDIR:-/tmp}/dotfiles-wt`): an absolute path
#   without `.` or `..` components or a newline, outside the checkout and its git directory by device and inode (its
#   longest existing directory and each directory above it); made when absent, and printed as `pwd -P` resolves it,
#   a resolved form holding a newline refused.
# @stdout `worktree=<path>`, `branch=<branch>`, `head=<sha>` and `push=git -C <checkout> fetch <path> <branch> &&
#   git -C <checkout> push <origin url> FETCH_HEAD:refs/heads/<branch>`, the line the coordinator runs from the main
#   checkout, one per line; the paths and the URL are quoted for the shell (`printf %q`), the branch's character set
#   needs none.
# @stdout For `claim`: `claimed <unit> owner=<name> claimed=<stamp>`, or `taken over <unit> from=<old> age=<min>m
#   owner=<name> claimed=<stamp>`, the stamp the release presents; for `release`: `released <unit> owner=<name>`, or
#   `no claim <unit>` when there is no record.
# @stdout For `task`: the task text, line 1 `Tree: <root>/<unit> (every command runs here; your first command is
#   \`cd <tree> && pwd -P\`, and the report's first line is its output)`, then `Brief:`, `Branch:` (with the base),
#   `No push:`, `Forbidden paths:` and, when given, `Round:`; the tree's path in the `cd` is quoted for the shell
#   (`printf %q`, the plain path over `[A-Za-z0-9._/-]`); a seat path in the forbidden-paths line is shown with a line
#   boundary escaped. For `verify`: one line per finding (`foreign worktree <path> ...`, `dirty seat checkout <path>
#   ...`, each ending in the commands that clear it), else one `verified <unit>: ...` line.
# @exitcode 0 The repository exists at the base on the branch with the refusals and the upstream set.
# @exitcode 2 Refused: usage, a unit, branch or base outside the grammar, a working directory that is not the main
#   checkout or has no `origin` or a relative origin URL, a root inside the checkout or its git directory by identity,
#   or holding a `.`, `..` or a newline (its resolved form included), a checkout path holding a newline, the target
#   path present (the reservation failed), a read (`git rev-parse`, `git config`, the resolver's `cd` and `pwd -P`,
#   `uname -s`, `stat`) that failed, or the manifest pin differing from this file, each before anything is made; or a
#   step after the reservation that failed, after which the directory this run made is removed again and nothing else;
#   for the owner subcommands, an owner outside the grammar, a `--stale` that is not 1 to 6 digits, a `release`
#   without its claim time or with one outside `YYYY-MM-DDTHH:MM:SSZ` (each grammar matched whole), a tree that is
#   absent or no repository this lever made (`.git` not a directory of this user, or a symbolic link), no `python3` on
#   PATH, the program beside this file unreadable or off its pin, the lock not taken within 10 s, or a record outside
#   its two exact lines or unreadable (left for the operator), nothing written.
# @exitcode 3 Refused by the owner record: a `claim` while a record younger than `--stale` holds the tree (`the tree
#   <path> is owned by <old> (claimed <ts>, <age> min ago); release it or wait past --stale`), or a `release` whose
#   owner and claim time are not the record's (another name, or the same name's later claim); the record is untouched.
# @exitcode 1 For the owner subcommands, a write or removal that failed after the decision: the temporary removed,
#   the previous record standing, one stderr line `worker-worktree.sh: failed: ...`.
# @exitcode 0 For `task`, the text printed; for `verify`, no foreign worktree and every seat checkout clean.
# @exitcode 1 For `verify`, at least one finding, each one stdout line, all of them printed.
# @exitcode 2 For `task` and `verify`: usage, a unit outside the grammar, a brief that is not an absolute path to a
#   readable file, `--round` without a text, a working directory that is not the main checkout, a tree absent or not
#   this lever's (`.git` a link or no directory, the alternates not the checkout's objects directory by identity, the
#   origin not the checkout's, the push url not the refusal), a detached tree, `regime-env` unreadable beside this
#   file or refusing (its line through `refuse`), or a read that failed (the worktree list, a directory above a listed
#   worktree that cannot be searched, regime-env's toplevel read, the seats root's listing, a directory above the root
#   that cannot be searched, a link on the way whose target cannot be searched, a file where a directory should be, a
#   seat's status or filter drivers, a seat that is no repository, the tree's branch or reflog, `uname -s`, `stat`);
#   nothing written.
# @example
#   ~/.local/bin/common/worker-worktree.sh U123 feat/refusals-not-sentences origin/main
#   ~/.local/bin/common/worker-worktree.sh claim U123 U123Worker
#   ~/.local/bin/common/worker-worktree.sh release U123 U123Worker 2026-11-14T01:00:00Z
#   ~/.local/bin/common/worker-worktree.sh task U573 ~/.local/state/regime-store/dotfiles/regime-cutover/briefs/U573-worker-tree-named-in-the-task-and-verified-after.md --round 'round 2: the verdict ...'
#   ~/.local/bin/common/worker-worktree.sh verify U573
set -euo pipefail

# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
# @set LEVER_DIR The physical directory of this file, where the owner subcommands' program sits (U509e).
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

lever='worker-worktree.sh'
usage='usage: worker-worktree.sh <unit> <branch> <base> | claim <unit> <owner> [--stale <minutes>] | release <unit> <owner> <claimed> | task <unit> <brief> [--round <text>] | verify <unit>'
pushurl='refused://never-push-from-a-worker-worktree'
hook_message='standing order 29: the coordinator pushes'
path=''

# @description Print a refusal on stderr and exit 2; nothing was made. The refusal is one line: a line boundary (a
#   newline, a carriage return, a vertical tab or a form feed) in the interpolated text (a unit, a path, a producer's
#   words) is folded to a space, so a unit holding a newline is one stderr line and not two (round 2 of U573).
# @arg $@ string The reason.
refuse() {
    local reason=$*
    echo "${lever}: refused: ${reason//[$'\n\r\v\f']/ }" >&2
    exit 2
}

# @description Print a failed step on stderr and exit 2, one line as `refuse` prints it; the EXIT trap removes the
#   directory this run reserved.
# @arg $@ string The reason.
fail() {
    local reason="$*; the repository ${path} this run made is removed again"
    echo "${lever}: refused: ${reason//[$'\n\r\v\f']/ }" >&2
    exit 2
}

# @description Remove every `GIT_*` name from this shell's environment and close the global and system configuration
#   (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`): the environment every git this lever causes runs in.
#   The names are subtracted by prefix, not listed: round 4 listed `GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`,
#   `GIT_CONFIG_COUNT`, `GIT_DIR`, `GIT_WORK_TREE` and `GIT_COMMON_DIR`, and the audit of that round found
#   `GIT_INDEX_FILE` (the fresh repository's index written into the checkout, or the checkout's index reused, so the
#   tree had no README) and `GIT_OBJECT_DIRECTORY` (another objects directory named by `rev-parse --git-path
#   objects`, so the alternates pointed elsewhere); every other `GIT_*` name steers a read or a write too (`GIT_TRACE`
#   writes a file). `${!GIT_@}` is the shell's own list of the names, so no producer's status is at stake. `git_run`
#   calls this in the subshell that execs git, so the caller's environment stays as it was; `seats_read` calls it in
#   the lever's own shell before `regime-env` is sourced, since regime-env runs git of its own outside `git_run`
#   (round 2 of U573: a caller's `GIT_DIR` pointing at the worker tree derived the seats root from the tree's slug,
#   so no seat was judged, and its `GIT_TRACE` made a file). The closed configuration holds for the reads in the
#   checkout as well: none of them needs the operator's global config, and no `core.hooksPath`, `hook.<name>.event`
#   or `filter.<name>.smudge` of it is read by any git this lever runs.
# @exitcode 2 A name cannot be removed (readonly).
git_env_scrub() {
    local name
    for name in "${!GIT_@}"; do
        unset -v "${name}" || {
            echo "${lever}: refused: cannot remove ${name} from git's environment" >&2
            exit 2
        }
    done
    export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
}

# @description Run git under `git_env_scrub` in a subshell that execs it, so the caller's environment stays as it was.
# @arg $@ string git's arguments.
# @exitcode 2 A name cannot be removed (readonly).
# @exitcode * git's own status.
git_run() {
    (
        git_env_scrub
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

# @description Place the root the worker trees live in: `$DOTFILES_WT` (default `${TMPDIR:-/tmp}/dotfiles-wt`),
#   absolute, without a `.` or `..` component or a newline, resolved through its longest existing directory
#   (`resolve_root`), the resolved form without a newline either. Shared by the creation subcommand and the owner
#   subcommands (U509); every refusal is exit 2 before anything is made or written.
# @set root The resolved root.
# @set root_prefix The physical path of the root's longest existing directory, the first step of the identity walk.
place_root() {
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
}

# The tree's owner record (regime-cutover U509, U509e, U509f): `claim <unit> <owner> [--stale <minutes>]` and
# `release <unit> <owner> <claimed>` run the program `worker-worktree-owner.py` beside this file and end with its status.
owner_program='worker-worktree-owner.py'

# @description The owner subcommands: the root placed as the creation subcommand places it (`place_root`, exit 2
#   before anything runs), then the one program `worker-worktree-owner.py` beside this file, which checks the
#   arguments, opens the tree's `.git` through descriptors, takes the one lock and reads, writes or removes the record
#   (round 1 kept these steps in the shell, and the audit found the read and the write unheld between them, a NUL
#   dropped by `$(…)`, an overflowed `--stale`, a day of 31 in every month and an empty record after a failed write;
#   verdicts/U509-e343a569.md). The program's bytes are read once into the shell (`cat`, its status checked and its
#   error words in the one refusal line, a sentinel keeping the final newline as `exact_line` keeps one), hashed against the
#   `claude.levers.sha256.worker-worktree-owner.py` pin of the manifest the self-check read (the readers of
#   lever_self_check), and those same bytes are what `python3 -I -S -` runs from its stdin: no path is read twice
#   between the hash and the run, so a file replaced after the hash runs nothing (the pin-then-run class of U344c).
#   This function acts on the program's exit status alone and ends the run with it: 0 claimed, taken over, released
#   or no claim (its one stdout line), 3 refused by the record, 2 refused by shape, 1 a write or removal that failed
#   after the decision; the program's stdout and stderr are the lever's.
# @arg $@ string The verb, then its arguments, as given to the lever.
owner_subcommand() {
    local program=${LEVER_DIR}/${owner_program} content pin digest status=0
    place_root
    command -v python3 > /dev/null || refuse "python3 is not on PATH; the owner subcommands run ${program}"
    content=$(cat -- "${program}" 2>&1 && printf x) || refuse "cannot read ${program}: ${content//$'\n'/ }"
    content=${content%x}
    pin=$(sed -n -E "s/^      ${owner_program//./\\.}: ([0-9a-f]{64})\$/\\1/p" "${LEVER_MANIFEST}") || refuse "cannot read ${LEVER_MANIFEST}"
    [[ ${pin} =~ ^[0-9a-f]{64}$ ]] || refuse "no single sha256 pin for ${owner_program} in ${LEVER_MANIFEST}"
    if command -v sha256sum > /dev/null; then
        digest=$(printf '%s' "${content}" | sha256sum) || digest=''
    else
        digest=$(printf '%s' "${content}" | shasum -a 256) || digest=''
    fi
    digest=${digest%% *}
    [[ ${digest} =~ ^[0-9a-f]{64}$ ]] || refuse "cannot hash ${program}"
    [[ ${digest} == "${pin}" ]] || refuse "sha256 ${digest} of ${program} differs from the pin in ${LEVER_MANIFEST}; the program is not the pinned one"
    printf '%s' "${content}" | python3 -I -S - "${root}" "$@" || status=$?
    exit "${status}"
}

# The dispatch text and the return check (regime-cutover U573): `task <unit> <brief> [--round <text>]` and
# `verify <unit>` read the main checkout, the tree and the seats root, and write nothing.
task_usage='usage: worker-worktree.sh task <unit> <brief> [--round <text>]'
verify_usage='usage: worker-worktree.sh verify <unit>'
findings=()

# @description Read the main checkout the working directory is in, as the creation subcommand reads it: the physical
#   toplevel, the git directory (equal to the common directory, so a linked worktree is refused), the objects
#   directory and the origin URL. Every read is checked (standing order 21); a refusal is exit 2.
# @set toplevel The checkout's physical path.
# @set git_dir Its git directory.
# @set objects Its objects directory.
# @set origin_url Its `remote.origin.url`.
main_checkout_read() {
    local status=0
    exact_line git_run rev-parse --show-toplevel 2> /dev/null || refuse 'run from the main checkout'
    toplevel=${exact}
    exact_line physical_path "${toplevel}" || refuse "cannot resolve ${toplevel}"
    toplevel=${exact}
    exact_line git_run rev-parse --path-format=absolute --git-dir 2> /dev/null || refuse "cannot read the git directory of ${toplevel}"
    git_dir=${exact}
    exact_line git_run rev-parse --path-format=absolute --git-common-dir 2> /dev/null || refuse "cannot read the git common directory of ${toplevel}"
    [[ ${git_dir} == "${exact}" ]] || # lint-comparisons: allow both sides are git's absolute forms of one checkout
        refuse "${toplevel} is a linked worktree (git dir ${git_dir}, common ${exact}); run from the main checkout"
    exact_line git_run rev-parse --path-format=absolute --git-path objects 2> /dev/null || refuse "cannot read the objects directory of ${toplevel}"
    objects=${exact}
    [[ -d ${objects} ]] || refuse "${objects} is not a directory"
    origin_url=$(git_run config --get remote.origin.url 2>&1) || status=$?
    case ${status} in
    0) ;;
    1) refuse "no origin remote in ${toplevel}" ;;
    *) refuse "cannot read remote.origin.url from the checkout's config: ${origin_url}" ;;
    esac
}

# @description Choose `stat`'s format flag for this system (the creation subcommand's read, run again here), so
#   `identity_of` compares two paths by device and inode; a failed or unknown read refuses.
# @set stat_args The flag and format.
stat_format_read() {
    local os
    os=$(uname -s) || refuse 'cannot read the operating system name (uname -s)'
    case ${os} in
    Darwin) stat_args=(-f '%d %i') ;;
    Linux) stat_args=(-c '%d %i') ;;
    *) refuse "no identity read for the system ${os}; stat's format flag is known for Darwin and Linux" ;;
    esac
}

# @description Hold that `<root>/<unit>` is a tree this lever made of this checkout, and read its branch: the
#   directory exists, its `.git` is a directory and no symbolic link (a linked worktree's `.git` is a file), its
#   `objects/info/alternates` names the checkout's objects directory by identity (device and inode), its
#   `remote.origin.url` is the checkout's, its `remote.origin.pushurl` is the refusal, and its HEAD is a branch. Each
#   read is checked, and every refusal names the tree (exit 2); nothing is written.
# @arg $1 string The unit.
# @set path The tree.
# @set tree_branch The branch the tree is on.
tree_read() {
    local alternates alternates_id objects_id value status=0
    path=${root%/}/$1
    [[ -e ${path} || -L ${path} ]] || refuse "the tree ${path} does not exist; make it with worker-worktree.sh $1 <branch> <base> first"
    [[ ! -L ${path} && -d ${path} ]] || refuse "the tree ${path} is not a directory"
    [[ ! -L ${path}/.git ]] || refuse "${path}/.git is a symbolic link; a worker tree's .git is the directory the lever made"
    [[ -d ${path}/.git ]] || refuse "${path} is no worker repository: ${path}/.git is not a directory (a linked worktree holds a file there; a worker tree is a repository of its own)"
    exact_line cat -- "${path}/.git/objects/info/alternates" 2> /dev/null || refuse "${path} is no worker repository of this checkout: cannot read ${path}/.git/objects/info/alternates"
    alternates=${exact}
    [[ -d ${alternates} ]] || refuse "${path} is no worker repository of this checkout: its alternates ${alternates//$'\n'/\\n} is not a directory"
    alternates_id=$(identity_of "${alternates}") || refuse "cannot read the identity (device and inode) of ${alternates//$'\n'/\\n}, the alternates of ${path}"
    objects_id=$(identity_of "${objects}") || refuse "cannot read the identity (device and inode) of the objects directory ${objects}"
    [[ ${alternates_id} == "${objects_id}" ]] || # lint-comparisons: allow compares (device, inode) identities, not paths
        refuse "${path} is no worker repository of this checkout: its alternates ${alternates//$'\n'/\\n} is not the objects directory ${objects} of ${toplevel}"
    value=$(git_run -C "${path}" config --get remote.origin.url 2>&1) || status=$?
    case ${status} in
    0) ;;
    1) refuse "${path} is no worker repository of this checkout: it has no remote.origin.url" ;;
    *) refuse "cannot read remote.origin.url of ${path}: ${value}" ;;
    esac
    [[ ${value} == "${origin_url}" ]] || # lint-comparisons: allow the URL the creation subcommand copied from the checkout, read back
        refuse "${path} is no worker repository of this checkout: its origin ${value} is not the checkout's ${origin_url}"
    status=0
    value=$(git_run -C "${path}" config --get remote.origin.pushurl 2>&1) || status=$?
    case ${status} in
    0) ;;
    1) refuse "${path} is no worker repository: its push path is not removed (no remote.origin.pushurl)" ;;
    *) refuse "cannot read remote.origin.pushurl of ${path}: ${value}" ;;
    esac
    [[ ${value} == "${pushurl}" ]] || # lint-comparisons: allow the refusal URL the creation subcommand wrote, read back
        refuse "${path} is no worker repository: its remote.origin.pushurl is ${value}, not ${pushurl}"
    # The full ref, not `--short`: beside a tag of the same name `--short` prints `heads/<name>`, and the reflog and
    # the branch lookup would then look for `refs/heads/heads/<name>` (round 2 of U573).
    tree_branch=$(git_run -C "${path}" symbolic-ref --quiet HEAD 2>&1) || refuse "cannot read the branch of ${path} (HEAD is detached, or the read failed): ${tree_branch}"
    [[ ${tree_branch} == refs/heads/?* ]] || # lint-comparisons: allow a shape test (a ref under refs/heads/), no path identity is compared
        refuse "HEAD of ${path} is ${tree_branch}, not a branch under refs/heads/"
    tree_branch=${tree_branch#refs/heads/}
    [[ ${tree_branch} =~ ^[A-Za-z0-9._/-]+$ ]] || refuse "the branch ${tree_branch} of ${path} has a character outside [A-Za-z0-9._/-]"
}

# @description Set `shown` to $1 with every line boundary escaped: a newline as `\n`, a carriage return as `\r`, a
#   vertical tab as `\v` and a form feed as `\f`, the four characters a text reader ends a line at. A path a finding
#   or the task text names is displayed in this form, so the line stays one line (round 3 of U573: round 2 escaped
#   the newline alone, and a worktree path holding a carriage return split its finding in two for a reader); the
#   command in the same line names the path exactly, quoted for the shell (`printf %q`).
# @arg $1 string The text.
# @set shown The escaped text.
display() {
    shown=$1
    shown=${shown//$'\n'/\\n}
    shown=${shown//$'\r'/\\r}
    shown=${shown//$'\v'/\\v}
    shown=${shown//$'\f'/\\f}
}

# @description Hold that a file test on the path $2 under the directory $1 answers for the path and not for a failed
#   look: walk its components and refuse (exit 2) when a directory on the way exists but cannot be searched, since `-e`
#   below such a directory answers false for EACCES as it does for ENOENT, and round 2 of U573 found the seats root
#   under a mode-000 parent read as absent (verdicts/U573-32986760.md P1 :529; standing order 21). A symbolic link on
#   the way is followed to its target (`readlink`, its status read; a relative target is taken from the link's
#   directory) and the target's own path is walked from `/` by the same rule, its links followed in turn, at most 40
#   deep: round 3 (verdicts/U573-5f983ea2.md P1 :575) found a link whose target lay under an unsearchable directory
#   read as absent, since `-L` saw the link and `-d` could not see through it; the walk goes on at the target, so a
#   mode-000 target is refused by the target's name. A component that exists and is not a directory while components
#   remain below it (ENOTDIR: a regular file where a directory should be) is a failed read as well, refused by name,
#   not an absence (the same verdict). The walk ends at the first component that is absent (everything below it is
#   absent: the one clean ENOENT) or at a last component that is no directory (the path itself is a file) and
#   returns 0; the caller's own tests on the path then mean what they say. Nothing is written.
# @arg $1 string A directory that exists (`/`).
# @arg $2 string The path under it, relative, its components as given.
# @arg $3 string What the path is, for the refusal.
# @arg $4 string The number of symbolic links followed so far (the recursion's own; callers give none).
path_read_check() {
    local dir=$1 rest=$2 what=${3:-} links=${4:-0} comp next target
    while [[ -n ${rest} ]]; do
        comp=${rest%%/*}
        if [[ ${rest} == */* ]]; then # lint-comparisons: allow a shape test (a slash left in the remaining path), no path identity is compared
            rest=${rest#*/}
        else
            rest=''
        fi
        [[ -n ${comp} ]] || continue
        [[ -x ${dir} ]] || refuse "cannot search the directory ${dir} (permission denied), so whether ${what} exists cannot be read"
        next=${dir%/}/${comp}
        if [[ -L ${next} ]]; then
            ((links < 40)) || refuse "${next}, which ${what} lies under, is the 41st symbolic link on the way, so whether ${what} exists cannot be read"
            exact_line readlink -- "${next}" || refuse "cannot read the symbolic link ${next}, which ${what} lies under, so whether ${what} exists cannot be read"
            target=${exact}
            [[ ${target} == /* ]] || target=${dir%/}/${target} # lint-comparisons: allow a shape test (absolute or relative link target), no path identity is compared
            path_read_check / "${target#/}" "${what}" $((links + 1))
            next=${target}
        fi
        [[ -e ${next} ]] || return 0
        if [[ ! -d ${next} ]]; then
            [[ -n ${rest//\//} ]] || return 0
            refuse "${next}, which ${what} lies under, is not a directory, so ${what} cannot be read"
        fi
        dir=${next}
    done
}

# @description Source `regime-env` beside this file, derive the seats root and list the seat checkouts under it: the
#   directories not beginning with `.`, sorted (`find -print0`, one level). The toplevel regime-env derives the slug
#   from is read first by this function through regime-env's own `regime_toplevel` (two `git rev-parse` and a `pwd
#   -P`), its status judged: `regime_env` runs that read inside a substitution and, under an explicit `HCOM_DIR`,
#   returns 0 when it fails (the explicit store needs no slug), and under an explicit `REGIME_SEATS_ROOT` as well the
#   lever went on with no checkout read at all (round 3 of U573, verdicts/U573-5f983ea2.md P1 :597); the wrapper
#   refuses a failed read (exit 2), and `regime_toplevel` is then redefined to answer with the value read, so
#   `regime_env` derives the slug, the store root and the store binding from the toplevel this function judged and
#   runs no git of its own. `regime_env` runs in a substitution whose stderr is captured, so its refusal (a slug, a
#   store root component, a store bound to another checkout, an empty HOME) reaches stderr through `refuse`, one
#   line, its own `<lever>: refused: ` prefix removed (round 2 let it print directly, and a HOME holding a newline
#   made three lines, P3 :597). The seats root is then derived here, the derivation regime-env documents:
#   `REGIME_SEATS_ROOT` when set, else `${HOME}/.local/state/omp-seats/<slug>` with the slug `regime_slug` prints for
#   the toplevel read above (its status judged). An absent root holds no seat; a root that cannot be listed, a
#   directory above it that cannot be searched, a link on the way to an unsearchable target, or a file where a
#   directory should be (`path_read_check`) is a refusal (exit 2), never an empty list: only a clean ENOENT is an
#   absence (standing order 21). The listing is NUL-separated (`find -print0`, `sort -z`, `tr` as `worktrees_judge`
#   reads the worktree list), so a seat whose name holds a newline is one path (round 2 split it in two, P2 :605).
#   regime-env's git runs outside `git_run`, so `git_env_scrub` runs first in this shell: a caller's `GIT_DIR` cannot
#   point that read at another repository, and so at another seats root, and its `GIT_TRACE` writes no file; every
#   `git_run` after it scrubs again.
# @set seats_root The seats root.
# @set seats The seat checkouts, an array of paths, possibly empty.
# @set regime_toplevel_read The toplevel regime-env derives from, as its own read printed it.
seats_read() {
    local listing line message slug
    [[ -r ${LEVER_DIR}/regime-env ]] || refuse "regime-env unreadable beside this script: ${LEVER_DIR}/regime-env"
    git_env_scrub
    # shellcheck source=scripts/orchestrator/regime-env
    . "${LEVER_DIR}/regime-env"
    declare -F regime_toplevel > /dev/null || refuse "regime-env beside this script defines no regime_toplevel; the seats root cannot be derived"
    declare -F regime_slug > /dev/null || refuse "regime-env beside this script defines no regime_slug; the seats root cannot be derived"
    regime_toplevel_read=$(regime_toplevel) || refuse "cannot read the toplevel regime-env derives the seats root from (git rev-parse or pwd -P in ${toplevel} failed)"
    [[ -n ${regime_toplevel_read} ]] || refuse "regime-env's toplevel read of ${toplevel} printed nothing"
    # From here regime_env's own regime_toplevel is the value judged above: no git of regime-env's can fail unseen.
    regime_toplevel() {
        printf '%s\n' "${regime_toplevel_read}"
    }
    message=$(regime_env "${lever}" --unbound-ok 2>&1 > /dev/null) || {
        message=${message#"${lever}: "}
        message=${message#refused: }
        refuse "regime-env: ${message}"
    }
    if [[ -n ${REGIME_SEATS_ROOT:-} ]]; then
        seats_root=${REGIME_SEATS_ROOT}
    else
        slug=$(regime_slug "${regime_toplevel_read}") || refuse "cannot derive a repository slug from ${regime_toplevel_read} (it must start with [a-z0-9]), so no seats root can be derived"
        [[ -n ${HOME:-} ]] || refuse 'HOME is empty, so no seats root can be derived under it'
        seats_root=${HOME}/.local/state/omp-seats/${slug}
    fi
    seats=()
    [[ ${seats_root} == /* ]] || # lint-comparisons: allow a shape test (absolute or not), no path identity is compared
        refuse "the seats root ${seats_root} is not an absolute path"
    path_read_check / "${seats_root#/}" "the seats root ${seats_root}"
    [[ -e ${seats_root} || -L ${seats_root} ]] || return 0
    [[ ! -L ${seats_root} && -d ${seats_root} ]] || refuse "the seats root ${seats_root} is not a directory"
    listing=$({ find "${seats_root}" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -print0 2>&1 | LC_ALL=C sort -z | LC_ALL=C tr '\0\n\001' '\n\001\002'; } && printf .) ||
        refuse "cannot list the seats root ${seats_root}: ${listing//[$'\001\002']/ }"
    listing=${listing%.}
    [[ -n ${listing} ]] || return 0
    while IFS= read -r line; do
        [[ -n ${line} ]] || continue
        [[ ${line} != *$'\002'* ]] || refuse "the seats root ${seats_root} holds a name with a \\001 or \\002 byte, which this read cannot tell apart: ${line//[$'\001\002']/ }"
        # A bare assignment: inside a quoted array append bash 3.2 (macOS's /bin/bash) leaves the replacement as it is.
        line=${line//$'\001'/$'\n'}
        seats+=("${line}")
    done <<< "${listing}"
}

# @description The explicit roots a foreign worktree is judged under: `$DOTFILES_WT` as `place_root` placed it and
#   `${TMPDIR}/dotfiles-wt` when `TMPDIR` is absolute, each as given and as `resolve_root` resolves it through its
#   longest existing directory; a root whose existing prefix cannot be entered refuses. The default root under any
#   other TMPDIR (the system's temporary directory included, where U566's stray worktree stood) is covered by the
#   component rule of `worktrees_judge` (a `dotfiles-wt` directory anywhere in the path), so no temporary directory is
#   spelled here: the repository's sandbox-portability guard (tests/unit/test_sandbox_portability.py) refuses a
#   tracked script that names one, since the sandbox's writable temporary directory is `$TMPDIR` alone, and round 1
#   of U573 named two.
# @set roots The array.
roots_read() {
    local candidate
    roots=()
    for candidate in "${root}" ${TMPDIR:+"${TMPDIR%/}/dotfiles-wt"}; do
        [[ ${candidate} == /* && ${candidate} != *$'\n'* ]] || continue # lint-comparisons: allow a shape test (absolute, no newline), no path identity is compared
        roots+=("${candidate%/}")
        resolve_root "${candidate}" || refuse "cannot resolve ${candidate}; its longest existing directory cannot be entered"
        roots+=("${resolved_root%/}")
    done
}

# @description Append the foreign-worktree finding for the path $1, judged $2 (`under <root>`, or `under a dotfiles-wt
#   directory` for the component rule), on the branch $3 (empty when detached, or when it is the main worktree's own
#   branch, which no stray add made): the path is named in `display`'s form and quoted for the shell (`printf %q`) in
#   the remove command, so the line is one line and the command names the path exactly; when the entry is on a
#   branch, the step ends with `git branch -D <branch>` after the remove, the leftover of that stray worktree alone
#   (round 3 of U573, Codex thread 4604357806: round 2 named a branch of the checkout merely for being named like the
#   tree's, and the checkout may hold that branch from before the tree was made).
# @arg $1 string The worktree path, as git printed it.
# @arg $2 string Why it is foreign.
# @arg $3 string The branch the entry is on, `refs/heads/` stripped, or empty.
# @set findings One line appended.
worktree_finding() {
    local finding tail=''
    [[ -z $3 ]] || printf -v tail ', then git -C %q branch -D %q, the branch that worktree was on (the leftover of its worktree add -b; keep a branch the checkout held before the stray add)' "${toplevel}" "$3"
    display "$1"
    printf -v finding 'foreign worktree %s of the main checkout %s %s: a worker tree is a repository of its own and never in this list, so this entry is a stray git worktree add; move any diff out, then git -C %q worktree remove --force %q (git -C %q worktree prune when the directory is gone)%s' \
        "${shown}" "${toplevel}" "$2" "${toplevel}" "$1" "${toplevel}" "${tail}"
    findings+=("${finding}")
}

# @description Judge the main checkout's `git worktree list --porcelain -z` against the roots: every entry after the
#   first (the main worktree, the checkout itself, which git lists first) that is a root or lies under one is a
#   foreign worktree, one stdout line each (a lever-made tree is a repository of its own and never in this list).
#   Containment is decided by identity: the path as printed and each directory above it, up to `/`, is tested against
#   every root with `-ef` (device and inode, links followed), after `path_read_check` has held that each directory on
#   the way can be searched, so a false `-ef` is never a failed look; a spelling of the root that `pwd -P` keeps (a
#   case alias of the root on a case-insensitive volume, round 3 of U573, verdicts/U573-5f983ea2.md P2 :677) or an
#   entry whose directory is gone but was spelled through a link to the root names the same directory and is found.
#   Two spelling nets follow for an entry whose directory and root are both gone: the path as printed and as `pwd -P`
#   resolves it (when it exists) is a root or under one by prefix; and a `dotfiles-wt` component anywhere in either
#   form (the default root under any TMPDIR). The list is read NUL-separated, in hcom-seat's form: `$(…)` drops NULs,
#   and the line form split a path holding a newline, so round 2 of U573 found the finding naming a shortened path
#   and the remove command targeting it. `tr` turns each NUL into a newline, each newline into \001 and each \001
#   into \002 before the substitution, a sentinel `.` keeps the trailing newlines, and a path field is turned back
#   (\001 to a newline) once it is seen to hold no \002, which would stand for a \001 or a \002 of the path itself and
#   is refused by name, since after the mapping the two cannot be told apart. The fields are read into one entry per
#   `worktree` line first, each with the `branch refs/heads/<name>` line that follows it in its record (none when
#   detached), so the finding can name the branch that stray worktree alone made; the first entry's branch is the
#   checkout's own and is never named. The producer's status is the pipeline's (`pipefail`), its stderr in the same
#   text. A failed listing or resolution is a refusal (exit 2).
# @set findings One line appended per finding.
worktrees_judge() {
    local listing field wt form candidate index=-1 forms branch checkout_branch
    local -a wts=() branches=()
    listing=$({ git_run worktree list --porcelain -z 2>&1 | LC_ALL=C tr '\0\n\001' '\n\001\002'; } && printf .) ||
        refuse "cannot read git worktree list of ${toplevel}: ${listing//[$'\001\002']/ }"
    listing=${listing%.}
    while IFS= read -r field; do
        case ${field} in
        'worktree '*)
            [[ ${field} != *$'\002'* ]] || refuse "the worktree list of ${toplevel} names a path holding a \\001 or \\002 byte, which this read cannot tell apart: ${field//[$'\001\002']/ }"
            index=$((index + 1))
            wt=${field#worktree }
            wt=${wt//$'\001'/$'\n'}
            wts+=("${wt}")
            branches+=('')
            ;;
        'branch refs/heads/'?*)
            ((index >= 0)) || refuse "the worktree list of ${toplevel} names a branch before any worktree: ${field//[$'\001\002']/ }"
            branches[index]=${field#branch refs/heads/}
            ;;
        esac
    done <<< "${listing}"
    ((${#wts[@]} > 0)) || refuse "the worktree list of ${toplevel} names no worktree, not even the main one"
    checkout_branch=${branches[0]}
    for ((index = 1; index < ${#wts[@]}; index++)); do
        wt=${wts[index]}
        [[ ${wt} == /* ]] || refuse "the worktree list of ${toplevel} names a relative path: ${wt}" # lint-comparisons: allow a shape test (absolute or not), no path identity is compared
        path_read_check / "${wt#/}" "the worktree ${wt} of ${toplevel}"
        branch=${branches[index]}
        [[ -z ${checkout_branch} || ${branch} != "${checkout_branch}" ]] || branch='' # lint-comparisons: allow a branch name against the main worktree's, no path identity is compared
        candidate=${wt}
        while :; do
            for form in "${roots[@]}"; do
                if [[ ${candidate} -ef ${form} ]]; then
                    worktree_finding "${wt}" "under ${form}" "${branch}"
                    continue 3
                fi
            done
            [[ ${candidate} != / ]] || break # lint-comparisons: allow the walk ends at the filesystem root, a shape test; no path identity is compared
            candidate=${candidate%/*}
            [[ -n ${candidate} ]] || candidate=/
        done
        forms=("${wt}")
        if [[ -d ${wt} ]]; then
            exact_line physical_path "${wt}" || refuse "cannot resolve the worktree ${wt} of ${toplevel}"
            forms+=("${exact}")
        fi
        for form in "${forms[@]}"; do
            for candidate in "${roots[@]}"; do
                if [[ ${form} == "${candidate}" || ${form} == "${candidate}"/* ]]; then # lint-comparisons: allow the listed path and the root are each compared as printed and in their pwd -P forms, after the identity walk above
                    worktree_finding "${wt}" "under ${candidate}" "${branch}"
                    continue 3
                fi
            done
            if [[ /${form}/ == */dotfiles-wt/* ]]; then # lint-comparisons: allow a component test (a dotfiles-wt directory anywhere in the path), no path identity is compared
                worktree_finding "${wt}" 'under a dotfiles-wt directory' "${branch}"
                continue 2
            fi
        done
    done
}

# @description Judge every seat checkout: nothing changed, deleted, untracked or staged there. The read runs nothing
#   of the seat's: `-c core.fsmonitor=false` (round 2 of U573: `--no-optional-locks` alone left a configured
#   `core.fsmonitor` running inside the status) and `-c core.hooksPath=/dev/null`, and every filter driver the seat's
#   config defines is closed by name before the read: `git config --name-only --get-regexp '^filter\.'` lists the
#   `filter.<name>.<key>` entries (exit 1 is none; another failure refuses), and for each name `-c
#   filter.<name>.clean= -c filter.<name>.smudge= -c filter.<name>.process= -c filter.<name>.required=false` is
#   passed, which git reads last and so over the seat's own config: an empty command is no filter to git and
#   `required=false` keeps that from being an error, so no clean filter runs (round 3 of U573,
#   verdicts/U573-5f983ea2.md P2 :700 and Codex thread 4604459522: a same-length change made `git status` hash the file
#   through the seat's clean filter, which wrote a marker during `verify`). The read itself is `git ls-files -z -m -d
#   -o --exclude-standard --deduplicate` (the working tree against the index: changed, deleted and untracked paths)
#   and `git diff-index --cached --name-only -z HEAD` (the index against HEAD: the staged paths), both under
#   `--no-optional-locks` (nothing is written in the seat, not even its index: the seat is another writer's).
#   `ls-files -m` is not a stat-only read: a file whose size differs from the index is reported from the stat alone,
#   and one whose stat differs with the same size (an edit of the same length, a racily clean entry) is read and
#   hashed by git to decide, the step a clean filter would run in, which is why the drivers are closed rather than
#   trusted; an attribute `filter=<name>` with no driver configured runs nothing by itself. `diff-index --cached`
#   compares object names and reads no working-tree file. Each path is one NUL-terminated field (`tr` as the
#   worktree list is read, so a path holding a newline counts once); a non-empty read is one stdout line naming the
#   seat (in `display`'s form), the count and the step that clears it. Before any of it the seat's own toplevel
#   (`rev-parse --show-toplevel` there) must be the seat by identity (`-ef`): git run in a directory that is no
#   repository answers for the nearest repository above it, and that status would be read as the seat's. A read that
#   cannot be made (a directory that is no repository, a driver name holding `=`, which `-c` cannot spell) is a
#   refusal (exit 2).
# @set findings One line appended per finding.
seats_judge() {
    local seat keys key name out newlines finding status
    local -a closed
    for seat in ${seats[@]+"${seats[@]}"}; do
        # The seat's own toplevel first, by identity: git run in a directory that is no repository answers for the
        # nearest repository above it (a seats root under a checkout of the operator's home), and that status would
        # be read as the seat's.
        exact_line git_run -C "${seat}" rev-parse --show-toplevel 2> /dev/null || refuse "cannot read the toplevel of the seat checkout ${seat} (git rev-parse failed there; a seat is a repository)"
        [[ ${exact} -ef ${seat} ]] || refuse "the seat checkout ${seat} is no repository of its own: git's toplevel there is ${exact}"
        status=0
        keys=$(git_run -C "${seat}" config --name-only --get-regexp '^filter\.' 2>&1) || status=$?
        case ${status} in
        0 | 1) ;;
        *) refuse "cannot read the filter drivers of the seat checkout ${seat}: git config exited ${status}: ${keys}" ;;
        esac
        closed=()
        while IFS= read -r key; do
            [[ -n ${key} ]] || continue
            [[ ${key} == filter.*.* ]] || refuse "the config of the seat checkout ${seat} holds ${key}, which is no filter.<name>.<key>, so its filter drivers cannot be closed by name"
            name=${key#filter.}
            name=${name%.*}
            [[ ${name} != *=* ]] || refuse "the seat checkout ${seat} configures a filter driver named ${name}, which holds =, so its commands cannot be closed by name"
            closed+=(-c "filter.${name}.clean=" -c "filter.${name}.smudge=" -c "filter.${name}.process=" -c "filter.${name}.required=false")
        done <<< "${keys}"
        out=$({
            git_run ${closed[@]+"${closed[@]}"} -c core.fsmonitor=false -c core.hooksPath=/dev/null --no-optional-locks -C "${seat}" ls-files -z -m -d -o --exclude-standard --deduplicate 2>&1 &&
                git_run ${closed[@]+"${closed[@]}"} -c core.fsmonitor=false -c core.hooksPath=/dev/null --no-optional-locks -C "${seat}" diff-index --cached --name-only -z HEAD 2>&1
        } | LC_ALL=C tr '\0\n' '\n\001' && printf .) || refuse "cannot read the status of the seat checkout ${seat}: ${out//[$'\001']/ }"
        out=${out%.}
        [[ -n ${out} ]] || continue
        newlines=${out//[^$'\n']/}
        display "${seat}"
        printf -v finding 'dirty seat checkout %s (%s paths changed, deleted, untracked or staged): a worker writes in its own tree alone; move the diff out (git -C %q diff HEAD, the untracked paths by hand), then git -C %q reset -q --hard HEAD and remove the untracked paths (git -C %q clean -n lists them)' \
            "${shown}" "${#newlines}" "${seat}" "${seat}" "${seat}"
        findings+=("${finding}")
    done
}

# @description `task <unit> <brief> [--round <text>]`: the dispatch text (U573), printed once every input and the tree
#   are checked; nothing is written. The base is the oldest reflog entry of the tree's branch, the commit the creation
#   subcommand's `checkout -b` made it at. The seats root and each seat are named in `display`'s form (a line
#   boundary in a name escaped), so the forbidden-paths line is one line.
# @arg $@ string `task`, then its arguments, as given to the lever.
task_subcommand() {
    local unit brief round='' reflog base seat forbidden path_q
    case $# in
    3) ;;
    5)
        [[ $4 == --round ]] || refuse "${task_usage}"
        round=$5
        [[ -n ${round} ]] || refuse '--round needs a text'
        ;;
    *) refuse "${task_usage}" ;;
    esac
    unit=$2
    brief=$3
    [[ ${unit} =~ ^U[0-9]+[a-z]?$ ]] || refuse "the unit ${unit} is not U<n> or U<n><letter>"
    [[ ${brief} == /* ]] || # lint-comparisons: allow a shape test (absolute or not), no path identity is compared
        refuse "the brief ${brief} is not an absolute path; the worker reads it from its tree"
    [[ ${brief} != *$'\n'* ]] || # lint-comparisons: allow a shape test (a newline in the path), no path identity is compared
        refuse "the brief path ${brief//$'\n'/\\n} holds a newline; the task text names it on one line"
    [[ -f ${brief} && -r ${brief} ]] || refuse "the brief ${brief} is not a readable file"
    main_checkout_read
    place_root
    stat_format_read
    tree_read "${unit}"
    reflog=$(git_run -C "${path}" log -g --format=%H "refs/heads/${tree_branch}" 2>&1) || refuse "cannot read the reflog of ${tree_branch} in ${path}: ${reflog//$'\n'/ }"
    [[ -n ${reflog} ]] || refuse "the branch ${tree_branch} of ${path} has no reflog entry; the base it was made from cannot be read"
    base=${reflog##*$'\n'}
    [[ ${base} =~ ^[0-9a-f]{40,64}$ ]] || refuse "the oldest reflog entry of ${tree_branch} in ${path} is ${base}, not an object name"
    seats_read
    display "${seats_root}"
    if ((${#seats[@]} == 0)); then
        forbidden="no seat checkout under the seats root ${shown}"
    else
        forbidden="the seat checkouts under ${shown}:"
        for seat in "${seats[@]}"; do
            display "${seat}"
            forbidden+=" ${shown},"
        done
        forbidden=${forbidden%,}
    fi
    printf -v path_q '%q' "${path}"
    printf '%s\n' \
        "Tree: ${path} (every command runs here; your first command is \`cd ${path_q} && pwd -P\`, and the report's first line is its output)" \
        "Brief: ${brief} (read it whole first; its ACCEPTANCE commands run in the tree)" \
        "Branch: ${tree_branch}, which the tree is on, made by worker-worktree.sh from ${base} (the tree's origin/main at creation). The tree is a repository of its own, not a linked worktree: \`git worktree list\` in any checkout cannot show it, and a commit you look for in the main checkout is in the tree alone; if the tree seems absent, stop and report, never make another and never edit another checkout." \
        "No push: the tree has no push path (remote.origin.pushurl ${pushurl}, a pre-push hook that exits 1); commit in the tree with \`git -c commit.gpgsign=false commit\` and stop at a committed head; the coordinator fetches it by path and pushes (standing order 29). Never open or edit a pull request." \
        "Forbidden paths (standing order 27; never run git or edit files there): the main checkout ${toplevel}; ${forbidden}."
    [[ -z ${round} ]] || printf 'Round: %s\n' "${round}"
    exit 0
}

# @description `verify <unit>`: the coordinator's check after the worker's return (U573): the two judgements (the
#   checkout's worktree list, the seat checkouts), every finding printed once every read is done (so a refusal
#   leaves nothing on stdout), exit 1 when there is one, else one `verified` line and exit 0; nothing is written.
#   Round 2 judged a third thing, a local branch of the checkout named like the tree's, as the `git worktree add`
#   leftover; the checkout may hold that branch from before the tree was made (the creation subcommand's own test
#   makes a tree on a branch the checkout holds), so that advice could discard commits, and a stray worktree's branch
#   is named with that worktree's finding instead (Codex thread 4604357806).
# @arg $@ string `verify`, then the unit, as given to the lever.
verify_subcommand() {
    local unit
    [[ $# == 2 ]] || refuse "${verify_usage}"
    unit=$2
    [[ ${unit} =~ ^U[0-9]+[a-z]?$ ]] || refuse "the unit ${unit} is not U<n> or U<n><letter>"
    main_checkout_read
    place_root
    stat_format_read
    tree_read "${unit}"
    roots_read
    seats_read
    worktrees_judge
    seats_judge
    # The findings are printed once every read is done, so a refusal (exit 2) leaves nothing on stdout and a run that
    # prints a finding has read everything it judges.
    if ((${#findings[@]} > 0)); then
        printf '%s\n' "${findings[@]}"
        exit 1
    fi
    display "${seats_root}"
    printf 'verified %s: no foreign worktree of %s under %s or dotfiles-wt under TMPDIR, none with a dotfiles-wt path component; %s seat checkouts clean under %s\n' \
        "${unit}" "${toplevel}" "${root}" "${#seats[@]}" "${shown}"
    exit 0
}

case ${1:-} in
claim | release) owner_subcommand "$@" ;;
task) task_subcommand "$@" ;;
verify) verify_subcommand "$@" ;;
esac

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

place_root
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
