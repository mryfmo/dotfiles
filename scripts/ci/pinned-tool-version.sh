#!/usr/bin/env bash
# @file pinned-tool-version.sh
# @brief Refuse a lint tool whose version is not the one the mise config pins.
# @description
#   The lint gates run this before they lint (regime-cutover U97): `make shellcheck` for shellcheck and shfmt
#   (scripts/ci/masked-dirname-check.sh parses with shfmt), `make format` for shfmt, ruff and prettier, and CI's shfmt
#   and formatting steps for theirs. Each pin is one value in home/dot_mise/config.toml: the `version` of the
#   `[tools."http:shellcheck"]`, `[tools."http:shfmt"]` or `[tools."http:ruff"]` table, or the exact version of
#   `"npm:prettier"` under `[tools]`. mise installs it on every host, and CI's test jobs install it from a copy of the
#   same file. Releases disagree on findings and formatting (the apt ShellCheck on CI reported SC2015 where the local
#   mise release did not, in U71b and U96), so a run under any other version is refused, naming both, instead of
#   passing locally and failing in CI. The config is read as text, with no TOML library, so the check runs before uv
#   or a recent python3 is on PATH.
# @arg $1 path The mise config that holds the pins (the Makefile and CI pass home/dot_mise/config.toml).
# @arg $@ string The tools to check, after the config: shellcheck, shfmt, ruff or prettier.
# @stdout One line per tool naming the accepted version.
# @exitcode 0 Each tool's `--version` reports its pinned version.
# @exitcode 1 A tool reports another version or none, or fails; or the config cannot be read or pins no version.
# @exitcode 2 No tool is named, or a tool this check does not know.
# @example
#   scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml shfmt ruff prettier
set -euo pipefail

config=${1:-}
if (($# < 2)); then
    printf 'pinned-tool-version: usage: pinned-tool-version.sh <mise config> <tool>...\n' >&2
    exit 2
fi
shift
if [[ ! -r ${config} ]]; then
    printf 'pinned-tool-version: cannot read the mise config %s\n' "${config}" >&2
    exit 1
fi

#
# @description Print the version a config pins for one mise tool: the `version` line of its `[tools."<key>"]` table,
#   or its `"<key>" = "<version>"` line under `[tools]`. Every match is printed, so a doubled pin reads as no pin.
# @arg $1 string The mise tool key, such as http:shfmt or npm:prettier.
# @stdout The matching values, one per line.
# @exitcode 1 When awk cannot read the config.
#
function pinned_version() {
    awk -v key="$1" '
        /^[[:space:]]*\[/ { table = $0; sub(/[[:space:]]*(#.*)?$/, "", table); next }
        table == "[tools.\"" key "\"]" && /^version[[:space:]]*=/ {
            value = $0
            sub(/^version[[:space:]]*=[[:space:]]*"/, "", value)
            sub(/".*$/, "", value)
            print value
        }
        table == "[tools]" && index($0, "\"" key "\"") == 1 {
            value = substr($0, length(key) + 3)
            if (sub(/^[[:space:]]*=[[:space:]]*"/, "", value)) { sub(/".*$/, "", value) } else { value = "" }
            print value
        }
    ' "${config}"
}

status=0
for tool in "$@"; do
    # The mise key of each tool's pin, and the prefix its `--version` puts before the bare version on one line.
    case ${tool} in
    shellcheck) key=http:shellcheck prefix='version: ' ;;
    shfmt) key=http:shfmt prefix=v ;;
    ruff) key=http:ruff prefix='ruff ' ;;
    prettier) key=npm:prettier prefix= ;;
    *)
        printf 'pinned-tool-version: %s is not a pinned lint tool (shellcheck, shfmt, ruff, prettier)\n' "${tool}" >&2
        exit 2
        ;;
    esac
    if ! pin=$(pinned_version "${key}"); then
        printf 'pinned-tool-version: cannot read %s\n' "${config}" >&2
        exit 1
    fi
    if ! [[ ${pin} =~ ^[0-9]+(\.[0-9]+)+$ ]]; then
        printf 'pinned-tool-version: %s pins no %s version (one exact version for "%s")\n' "${config}" "${tool}" "${key}" >&2
        status=1
        continue
    fi
    if ! banner=$("${tool}" --version 2>&1); then
        printf 'pinned-tool-version: "%s --version" failed; %s pins %s %s\n' "${tool}" "${config}" "${tool}" "${pin}" >&2
        status=1
        continue
    fi
    installed=
    while IFS= read -r line; do
        if [[ ${line} == "${prefix}"* && ${line#"${prefix}"} =~ ^[0-9]+(\.[0-9]+)+$ ]]; then
            installed=${line#"${prefix}"}
        fi
    done <<< "${banner}"
    if [[ ${installed} != "${pin}" ]]; then
        printf 'pinned-tool-version: the %s on PATH is version %s, but %s pins %s %s; run "mise install %s" and put it first on PATH\n' \
            "${tool}" "${installed:-unknown}" "${config}" "${tool}" "${pin}" "${key}" >&2
        status=1
        continue
    fi
    printf '==> %s %s, the version %s pins\n' "${tool}" "${pin}" "${config}"
done
exit "${status}"
