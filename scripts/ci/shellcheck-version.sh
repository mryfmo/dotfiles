#!/usr/bin/env bash
# @file shellcheck-version.sh
# @brief Refuse a ShellCheck whose version is not the one the mise config pins.
# @description
#   `make shellcheck` runs this before it lints (regime-cutover U97). The pin is the `version` of the
#   `[tools."http:shellcheck"]` table in home/dot_mise/config.toml: mise installs it on every host, and CI's test
#   jobs install it on every runner from a copy of the same file. ShellCheck releases disagree on findings (the apt
#   release on CI reported SC2015 where the local mise release did not, in U71b and U96), so a run under any other
#   version is refused, naming both, instead of passing locally and failing in CI. The config is read as text, with
#   no TOML library, so the check runs before uv or a recent python3 is on PATH.
# @arg $1 path The mise config that holds the pin (the Makefile passes home/dot_mise/config.toml).
# @stdout One line naming the accepted version.
# @exitcode 0 `shellcheck --version` reports the pinned version.
# @exitcode 1 It reports another version or none, it fails, or the config cannot be read or pins no version.
# @example
#   scripts/ci/shellcheck-version.sh home/dot_mise/config.toml
set -euo pipefail

config=${1:-}
if [[ -z ${config} || ! -r ${config} ]]; then
    printf 'shellcheck-version: cannot read the mise config %s\n' "${config:-(none given)}" >&2
    exit 1
fi

# The version line of the [tools."http:shellcheck"] table; any other table's version is not read.
pin=$(awk '
    /^[[:space:]]*\[/ { table = $0; sub(/[[:space:]]*(#.*)?$/, "", table); next }
    table == "[tools.\"http:shellcheck\"]" && /^version[[:space:]]*=/ {
        value = $0
        sub(/^version[[:space:]]*=[[:space:]]*"/, "", value)
        sub(/".*$/, "", value)
        print value
    }
' "${config}") || {
    printf 'shellcheck-version: cannot read %s\n' "${config}" >&2
    exit 1
}
if ! [[ ${pin} =~ ^[0-9]+(\.[0-9]+)+$ ]]; then
    printf 'shellcheck-version: %s pins no ShellCheck version (one exact version in [tools."http:shellcheck"])\n' "${config}" >&2
    exit 1
fi

if ! banner=$(shellcheck --version 2>&1); then
    printf 'shellcheck-version: "shellcheck --version" failed; %s pins ShellCheck %s\n' "${config}" "${pin}" >&2
    exit 1
fi
installed=
while IFS= read -r line; do
    if [[ ${line} == "version: "* ]]; then
        installed=${line#version: }
    fi
done <<< "${banner}"

if [[ ${installed} != "${pin}" ]]; then
    printf 'shellcheck-version: the shellcheck on PATH is ShellCheck %s, but %s pins ShellCheck %s; run "mise install http:shellcheck" and put it first on PATH\n' \
        "${installed:-of no version}" "${config}" "${pin}" >&2
    exit 1
fi
printf '==> ShellCheck %s, the version %s pins\n' "${pin}" "${config}"
