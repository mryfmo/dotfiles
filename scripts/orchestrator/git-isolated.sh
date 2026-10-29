#!/usr/bin/env bash
# @file git-isolated.sh
# @brief One isolated git for every lever: the flag set as data, the function that runs git under it, the environment scrub.
# @description
#   Regime-cutover U113 (plan P-22, research 01 section 1). Git documents no single switch that removes all
#   configuration from a command: `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM` and `GIT_ATTR_NOSYSTEM` are
#   per-level switches, `GIT_CONFIG_PARAMETERS` and `GIT_CONFIG_COUNT` override every file from the environment, and
#   the repository level has no off switch. Until this file each lever carried a flag set of its own (`git_plain`,
#   `git_scratch`, `git_safe`, `git_tree`), none complete. Here the set is written once, as data: GIT_ISOLATED_ENV and
#   GIT_ISOLATED_ARGS, read by `git_isolated`, by the one `bounded` fetch of pr-audit.sh (a perl exec cannot run a
#   shell function) and by scripts/lint-comparisons.py (from this file's syntax tree, never by sourcing it).
#   Sourced by the levers from the directory they run from (`LEVER_DIR`), never run on its own; it checks its own
#   sha256 against its `claude.levers.sha256.git-isolated.sh` pin first, like every lever, so a rewritten copy under
#   ~/.local/bin/common stops the lever that sources it. scripts/ci/git-invocation-check.sh refuses any `git` word in
#   the levers outside `git_isolated` and outside a line carrying `# git-isolated: allow <reason>`.
#   bash 3.2 (macOS /bin/bash): plain arrays, no here-string, no case-modifying expansion.
# @set GIT_ISOLATED_ENV The environment of every isolated git, a plain array that is never exported (so a scrub leaves it).
# @set GIT_ISOLATED_ARGS The arguments before the caller's; a caller's later `-c` or `--git-dir` wins by git's last-wins rule.
# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
# @set LEVER_DIR The physical directory of this file, beside the lever that sourced it.
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

# The environment of every isolated git: one entry per line, each with the channel it closes and where that channel
# was found. The level switches close the files; the command scope (`GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`) is
# closed by git_env_scrub below, and the repository level by the choice of command alone (research 01 section 1.5).
GIT_ISOLATED_ENV=(
    # No global config file: no `url.*.insteadOf`, credential helper, hook path, identity or include of ~/.gitconfig
    # or $XDG_CONFIG_HOME/git/config (research 01 section 1.1; records-sync.sh U101, the redirected push).
    GIT_CONFIG_GLOBAL=/dev/null
    # No system config file $(prefix)/etc/gitconfig (research 01 section 1.1).
    GIT_CONFIG_NOSYSTEM=1
    # No system attributes file $(prefix)/etc/gitattributes, so it names no filter driver (research 01 section 1.4
    # item 3; pr-audit.sh U71b audit round 1, a filter driver run on the audited tree).
    GIT_ATTR_NOSYSTEM=1
    # No credential or passphrase prompt on the terminal: a transport that needs one fails instead of waiting
    # (pr-audit.sh U71b, the bounded fetch).
    GIT_TERMINAL_PROMPT=0
)
GIT_ISOLATED_ARGS=(
    # No replacement refs: a `refs/replace/*` of the repository cannot stand in for an object (pr-audit.sh U71b audit
    # round 7, with GIT_NO_REPLACE_OBJECTS).
    --no-replace-objects
    # No hook of any repository runs: git's documented off switch (research 01 section 1.1; records-sync.sh U101 round
    # 6, a post-checkout hook that planted files in the sync).
    -c core.hooksPath=/dev/null
    # No fsmonitor program: a hook path in core.fsmonitor ran inside `git ls-files` (measured, research 01 section 1.1;
    # records-sync.sh U101 round 12).
    -c core.fsmonitor=false
    # No user attributes file ($XDG_CONFIG_HOME/git/attributes), so no filter, diff or merge driver comes from it
    # (research 01 section 1.4 item 3; pr-audit.sh git_tree).
    -c core.attributesFile=/dev/null
    # No commit-graph file of the repository: an ancestry read (merge-base) must not trust a file the checkout wrote
    # (pr-audit.sh git_safe and git_tree).
    -c core.commitGraph=false
    # No ssh program: the ssh transport fails, whatever `core.sshCommand` any config names (research 01 section 1.1;
    # scripts/lint-comparisons.py GIT_C).
    -c core.sshCommand=false
    # Every transport off by default (file, git, ext, and any `insteadOf` rewrite to one); a caller re-opens one per
    # command, as the tests do with `-c protocol.file.allow=always` (research 01 section 1.1; hcom-seat U85).
    -c protocol.allow=never
    # https is the one transport left on: the levers fetch and push over https only (scripts/lint-comparisons.py GIT_C).
    -c protocol.https.allow=always
    # The empty helper resets the helper list, so no helper of any config answers; a caller adds its own after it
    # (records-sync.sh: `!gh auth git-credential`, standing order 19; research 01 section 1.1).
    -c credential.helper=
    # No credential prompt (research 01 section 1.1).
    -c credential.interactive=false
    # No automatic gc in a scratch repository that is removed on exit (records-sync.sh git_scratch; tests U100).
    -c gc.auto=0
    # No detached maintenance process left behind a command (records-sync.sh git_scratch; tests U100).
    -c maintenance.auto=false
)
# The non-`GIT_` names git_env_scrub removes: they steer libcurl and OpenSSL under a fetch or push (research 01
# section 1.4 item 2).
GIT_ISOLATED_SCRUB_NAMES=(http_proxy HTTPS_PROXY https_proxy HTTP_PROXY NO_PROXY no_proxy SSL_CERT_FILE SSL_CERT_DIR CURL_CA_BUNDLE)

# @description Run git under GIT_ISOLATED_ENV with GIT_ISOLATED_ARGS before the caller's arguments. A later `-c` of
#   the caller wins for its key by git's last-wins rule (measured, research 01 section 1.1): records-sync.sh adds its
#   credential helper after the empty one, and a test re-opens the local transport with `-c protocol.file.allow=always`.
#   The environment is exported in a subshell that execs git, so nothing is exported into the caller and no `env` from
#   PATH runs. This function body is the one place in the levers where a bare `git` word is accepted
#   (scripts/ci/git-invocation-check.sh).
# @arg $@ string git's arguments.
# @exitcode * git's own status.
git_isolated() {
    (
        export "${GIT_ISOLATED_ENV[@]}" && exec git "${GIT_ISOLATED_ARGS[@]}" "$@"
    )
}

# @description Whether $1 is a name git_env_scrub removes: an exported `GIT_*` name or one of GIT_ISOLATED_SCRUB_NAMES,
#   unless it is among the names to keep ($2...).
# @arg $1 string The name.
# @arg $@ string The names to keep.
# @exitcode 0 Remove it. 1 Leave it.
git_env_scrubbed() {
    local name=$1 listed keep
    shift
    listed=0
    case ${name} in
    GIT_*) listed=1 ;;
    *)
        for keep in "${GIT_ISOLATED_SCRUB_NAMES[@]}"; do
            [[ ${name} != "${keep}" ]] || listed=1
        done
        ;;
    esac
    ((listed)) || return 1
    for keep in "$@"; do
        [[ ${name} != "${keep}" ]] || return 1
    done
    return 0
}

# @description Remove every exported `GIT_*` name and the transport names of GIT_ISOLATED_SCRUB_NAMES from the
#   environment, except the names given as arguments, then list again and refuse if any is left. `GIT_CONFIG_PARAMETERS`
#   and `GIT_CONFIG_COUNT` override every config file and only this closes them (research 01 section 1.3), an exported
#   GIT_AUTHOR_NAME would name a commit's author, and GIT_DIR would point every command at another repository. The names
#   come from the builtin `compgen -e` through a command substitution and are split on the default IFS, which bash never
#   imports (an exported name has no blank or glob character), so bash 3.2 with an unwritable TMPDIR, which cannot make
#   a here-string file, cannot skip the loop (records-sync.sh U101 round 6). GIT_ISOLATED_ENV and GIT_ISOLATED_ARGS are
#   shell variables, never exported, so they stay. The refusal is prefixed with the sourcing script's name.
# @arg $@ string Names to keep.
# @exitcode 2 The environment cannot be listed, an `unset` fails (a readonly name), or a name is still there afterwards.
git_env_scrub() {
    local who names name
    who=${BASH_SOURCE[1]##*/}
    [[ -n ${who} ]] || who=git-isolated.sh
    names=$(compgen -e) || {
        echo "${who}: refused: cannot list the environment" >&2
        exit 2
    }
    for name in ${names}; do
        git_env_scrubbed "${name}" "$@" || continue
        unset "${name}" 2> /dev/null || {
            echo "${who}: refused: cannot remove ${name} from the environment" >&2
            exit 2
        }
    done
    names=$(compgen -e) || {
        echo "${who}: refused: cannot list the environment" >&2
        exit 2
    }
    for name in ${names}; do
        git_env_scrubbed "${name}" "$@" || continue
        echo "${who}: refused: ${name} is still in the environment after the scrub" >&2
        exit 2
    done
}
