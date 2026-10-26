#!/usr/bin/env bash
# @file install-pinned-lint-tools.sh
# @brief Install the pinned ShellCheck and shfmt from a mise config and put each first on a GitHub Actions PATH.
# @description
#   CI's "Put the pinned `ShellCheck` and `shfmt` on PATH" step (regime-cutover U97). `mise install` installs each
#   tool's `http:` pin from the copied home/dot_mise/config.toml, mise checking every download against its sha256.
#   Each binary's location comes from `mise which --tool`, its status checked, and must be an absolute path to an
#   executable regular file; only then is its directory appended to $GITHUB_PATH. Every lookup is checked before
#   anything is appended, so a failed lookup adds nothing (an unchecked `dirname "$(mise which …)"` turned a failed
#   lookup into `.`, round-1 audit of 35739993).
# @arg $1 path The mise project directory that holds the copied config (mise -C).
# @arg $@ string The tools, after the directory: shellcheck or shfmt.
# @env GITHUB_PATH path The file GitHub Actions reads PATH additions from.
# @exitcode 0 Every tool is installed and its directory appended.
# @exitcode 1 An install, a lookup or the append failed, or a lookup named no executable file by absolute path.
# @exitcode 2 No directory or tool, an unknown tool, or GITHUB_PATH unset: nothing was installed.
# @example
#   scripts/ci/install-pinned-lint-tools.sh "${RUNNER_TEMP}/statusline-mise" shellcheck shfmt
set -euo pipefail

if (($# < 2)) || [[ -z ${GITHUB_PATH:-} ]]; then
    printf 'install-pinned-lint-tools: usage: GITHUB_PATH=<file> install-pinned-lint-tools.sh <mise dir> <tool>...\n' >&2
    exit 2
fi
dir=$1
shift
keys=()
for tool in "$@"; do
    case ${tool} in
    shellcheck | shfmt) keys+=("http:${tool}") ;;
    *)
        printf 'install-pinned-lint-tools: %s is not a pinned lint tool this step installs (shellcheck, shfmt)\n' "${tool}" >&2
        exit 2
        ;;
    esac
done

if ! mise -C "${dir}" install "${keys[@]}"; then
    printf 'install-pinned-lint-tools: mise install %s failed\n' "${keys[*]}" >&2
    exit 1
fi
directories=()
for tool in "$@"; do
    if ! binary=$(mise -C "${dir}" which --tool "http:${tool}" "${tool}"); then
        printf 'install-pinned-lint-tools: mise which --tool http:%s %s failed; PATH is unchanged\n' "${tool}" "${tool}" >&2
        exit 1
    fi
    if ! [[ ${binary} == /* && -f ${binary} && -x ${binary} ]]; then # lint-comparisons: allow an absolute-path prefix test
        printf 'install-pinned-lint-tools: mise named %s for %s, not an executable file by absolute path; PATH is unchanged\n' \
            "${binary:-nothing}" "${tool}" >&2
        exit 1
    fi
    directories+=("${binary%/*}")
done
for directory in "${directories[@]}"; do
    if ! printf '%s\n' "${directory}" >> "${GITHUB_PATH}"; then
        printf 'install-pinned-lint-tools: cannot append %s to %s\n' "${directory}" "${GITHUB_PATH}" >&2
        exit 1
    fi
    printf '==> %s first on PATH\n' "${directory}"
done
