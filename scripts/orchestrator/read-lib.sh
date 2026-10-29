#!/usr/bin/env bash
# @file read-lib.sh
# @brief The fail-closed readers the levers source: each maps one producer to three outcomes, and a failed read is never an absence.
# @description
#   Regime-cutover U112 (plan P-21, standing order 21). Sourced by `records-sync.sh`, `pr-audit.sh`, `pr-merge.sh`,
#   `pr-threads-check.sh` and `pr-body-edit.sh` from the directory they run from (`LEVER_DIR`), after their own
#   self-check, never run on its own. It checks its own sha256 against its `claude.levers.sha256.read-lib.sh` pin
#   first, like every lever, so a rewritten copy under `~/.local/bin/common` stops the lever that sources it.
#   Three readers, no more: `read_config`, `read_listing` and `read_file`. Each returns 0 with the value in the named
#   variable (or the output file), 1 for an absence (the variable empty), and 2 for a failed read with one line on
#   stderr naming the key, the file or the producer and the status; nothing is printed for 0 and 1. No reader exits
#   or calls a lever function: the call site maps 1 and 2 itself (`status=0; read_config … || status=$?; case
#   ${status} in`), and a 2 stops the lever before any write. bash 3.2 compatible (no inherit_errexit, no associative
#   array, no case-modifying expansion): /bin/bash on macOS is 3.2, and four of the five levers run `#!/usr/bin/env
#   bash`. Every local is prefixed with the reader's initials, so the caller's variable may carry any other name.
#   `scripts/ci/producer-status-check.sh` holds the levers to the grammar these readers satisfy;
#   `tests/unit/test_read_lib.py` holds each reader to a failure-injection test.
# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
# @set LEVER_DIR The physical directory of this file, where the levers that source it sit.
set -euo pipefail

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

# @description Read one git configuration key with three outcomes. `git config --get` exits 1 for a key that is
#   unset and with another status when the configuration cannot be read: measured on git 2.56.0 (2026-10-28), 128
#   for an unparsable file, where the manual says 3. Any status other than 0 and 1 is a failure here, so the reader
#   is right under both. Status 1 is also what an unreadable `-f` file returns, with only a warning on stderr
#   (research 01 section 1.2), so git's stderr goes to a file and anything in it is a failed read, whatever the
#   status; 3 is never special-cased. The value is never printed.
# @arg $1 string The git function to read with (`git` reads the user configuration too, `git_plain` does not).
# @arg $2 string The configuration key.
# @arg $3 string The variable that receives the value.
# @arg $4 path The file that receives git's stderr: truncated first, then required empty.
# @exitcode 0 git exited 0 with a non-empty value and an empty stderr; the variable holds the value.
# @exitcode 1 Absent: git exited 1 with an empty stderr (the key is unset), or 0 with an empty value; the variable is empty.
# @exitcode 2 Failed: any other status, anything on stderr, or a stderr file that cannot be written; one line on
#   stderr names the key and the status.
read_config() {
    local rc_value='' rc_status=0
    printf -v "$3" '%s' ''
    { : > "$4"; } 2> /dev/null || {
        echo "read_config: cannot write ${4} to hold git's stderr for git config ${2}" >&2
        return 2
    }
    rc_value=$("$1" config --get "$2" 2> "$4") || rc_status=$?
    if ((rc_status != 0 && rc_status != 1)); then
        echo "read_config: cannot read git config ${2} (git config exited ${rc_status})" >&2
        return 2
    fi
    if [[ -s $4 ]]; then
        echo "read_config: cannot read git config ${2} (git config exited ${rc_status}); it wrote to its stderr, which a missing key never does" >&2
        return 2
    fi
    ((rc_status == 0)) || return 1
    [[ -n ${rc_value} ]] || return 1
    printf -v "$3" '%s' "${rc_value}"
}

# @description Run a listing producer with its stdout in one file and its stderr in another, with three outcomes.
#   `git ls-files` warns and exits 0 for a directory it cannot open and drops that directory's untracked files, and
#   `find` prints what it could reach before it exits 1 (git 2.56.0 and BSD find, measured for
#   scripts/ci/status-blind-producers.tsv): the status alone cannot clear a listing, so anything on stderr is a
#   failed read as well. Neither file's content is printed (a listed path may hold a redact word). The mid-entry
#   check of a NUL-delimited listing stays at the call site, which reads the file.
# @arg $1 path The file that receives the producer's stdout (truncated first).
# @arg $2 path The file that receives its stderr (truncated first).
# @arg $@ string The producer and its arguments: a command or a function, run as written.
# @exitcode 0 The producer exited 0, wrote nothing to stderr, and the output file is not empty.
# @exitcode 1 Absent: the producer exited 0, wrote nothing to stderr, and the output file is empty.
# @exitcode 2 Failed: a nonzero status (the shell's own when the producer could not be run), anything on stderr, no
#   producer named, or a file that cannot be written; one line on stderr names the producer's first two words and
#   the status.
read_listing() {
    local rl_out=$1 rl_err=$2 rl_status=0 rl_who rl_file
    shift 2
    (($# >= 1)) || {
        echo "read_listing: no producer named for ${rl_out}" >&2
        return 2
    }
    rl_who="$1${2:+ $2}"
    for rl_file in "${rl_out}" "${rl_err}"; do
        { : > "${rl_file}"; } 2> /dev/null || {
            echo "read_listing: cannot write ${rl_file} for ${rl_who}" >&2
            return 2
        }
    done
    "$@" > "${rl_out}" 2> "${rl_err}" || rl_status=$?
    if ((rl_status != 0)); then
        echo "read_listing: ${rl_who} exited ${rl_status}" >&2
        return 2
    fi
    if [[ -s ${rl_err} ]]; then
        echo "read_listing: ${rl_who} exited 0 and wrote to its stderr (kept in ${rl_err})" >&2
        return 2
    fi
    [[ -s ${rl_out} ]] || return 1
}

# @description Read a whole file into a variable, its trailing newlines kept, with three outcomes. The read is one
#   `cat` whose status comes through the substitution (`&& printf .` keeps the final newlines; the dot is removed
#   after), so a read that fails midway is a failure, never the end of the file. cat's own diagnostic is not shown;
#   the line printed here names the path and the status.
# @arg $1 path The file.
# @arg $2 string The variable that receives the content.
# @exitcode 0 The file was read and is not empty; the variable holds every byte.
# @exitcode 1 Absent: the file exists, was read, and is empty; the variable is empty.
# @exitcode 2 Failed: no file at the path, or `cat` exited nonzero (unreadable, a directory, cut short); one line on
#   stderr names the path.
read_file() {
    local rf_text='' rf_status=0
    printf -v "$2" '%s' ''
    [[ -e $1 ]] || {
        echo "read_file: no file at ${1}" >&2
        return 2
    }
    rf_text=$(cat -- "$1" 2> /dev/null && printf .) || rf_status=$?
    if ((rf_status != 0)); then
        echo "read_file: cannot read ${1} (cat exited ${rf_status})" >&2
        return 2
    fi
    rf_text=${rf_text%.}
    [[ -n ${rf_text} ]] || return 1
    printf -v "$2" '%s' "${rf_text}"
}
