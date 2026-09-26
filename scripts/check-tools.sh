#!/usr/bin/env bash

# @file scripts/check-tools.sh
# @brief Print a read-only health summary for managed dotfiles tools.
# @description
#   Reports the availability and versions of the commands that participate in
#   the dotfiles lifecycle. This script does not install, upgrade, or modify
#   tools; use `scripts/upgrade-tools.sh` for explicit upgrades.

set -Eeuo pipefail

required_failures=0
optional_warnings=0

#
# @description Print a section heading.
# @arg $1 string Heading text.
#
function section() {
    printf '\n==> %s\n' "$1"
}

#
# @description Require a command and a successful version command.
# @arg $1 string Command name.
# @arg $@ string Optional version command arguments.
#
function check_command() {
    local command_name="$1"
    shift || true

    if ! command -v "${command_name}" > /dev/null 2>&1; then
        printf 'required missing: %s\n' "${command_name}" >&2
        ((required_failures += 1))
        return 0
    fi

    printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"

    local output first_line

    if [ "$#" -gt 0 ]; then
        if ! output="$("${command_name}" "$@" 2>&1)"; then
            printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
            ((required_failures += 1))
            return 0
        fi
    else
        if ! output="$("${command_name}" --version 2>&1)"; then
            printf 'required failed: %s --version\n' "${command_name}" >&2
            ((required_failures += 1))
            return 0
        fi
    fi

    IFS= read -r first_line <<< "${output}"
    printf '%s\n' "${first_line}"
}

#
# @description Run a required read-only doctor command when its tool is available.
# @arg $1 string Command name.
# @arg $@ string Doctor command arguments.
#
function run_required_doctor() {
    local command_name="$1"
    shift || true

    if command -v "${command_name}" > /dev/null 2>&1 && ! "${command_name}" "$@"; then
        printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
        ((required_failures += 1))
    fi
}

#
# @description Record an optional warning.
# @arg $1 string Warning text.
#
function warn_optional() {
    printf 'optional warning: %s\n' "$1" >&2
    ((optional_warnings += 1))
}

#
# @description Return success when the rendered chezmoi config enables the private layer.
#   Defaults to enabled when chezmoi/jq are unavailable or the config predates the
#   usePrivate key, matching the owner's existing machines' behavior.
#
function private_layer_enabled() {
    local use_private

    if ! command -v chezmoi > /dev/null 2>&1 || ! command -v jq > /dev/null 2>&1; then
        return 0
    fi

    use_private="$(chezmoi data 2> /dev/null | jq -r '.usePrivate' 2> /dev/null)"
    [ "${use_private}" != "false" ]
}

#
# @description Print the configured private chezmoi source state.
#
function check_private_chezmoi() {
    local private_source="${HOME%/}/.local/share/chezmoi-private"
    local private_config="${HOME%/}/.config/chezmoi-private/chezmoi.yaml"

    if ! private_layer_enabled; then
        printf 'not applicable: private layer (usePrivate=false)\n'
        return 0
    fi

    if [ -d "${private_source}" ]; then
        printf 'found:   private source -> %s\n' "${private_source}"
        if [ -f "${private_config}" ]; then
            printf 'found:   private config -> %s\n' "${private_config}"
        else
            warn_optional "private config is missing: ${private_config}"
        fi
    else
        warn_optional "private source is missing: ${private_source}"
        if [ ! -f "${private_config}" ]; then
            warn_optional "private config is missing: ${private_config}"
        fi
    fi
}

#
# @description Require Homebrew on macOS and skip it on other platforms.
#
function check_homebrew() {
    if [ "$(uname)" != "Darwin" ]; then
        printf 'not applicable: Homebrew (non-Darwin)\n'
        return 0
    fi

    check_command brew --version
}

#
# @description Print whether the per-machine signing/push SSH key exists.
#
function check_machine_ssh_key() {
    local key_path="${HOME%/}/.ssh/id_ed25519.pub"

    if [ -f "${key_path}" ]; then
        printf 'found:   machine SSH key -> %s\n' "${key_path}"
    else
        warn_optional "machine SSH key is missing: ${key_path} (run provision-machine-key)"
    fi
}

#
# @description Report the managed Crit CLI's pinned version and origin, when installed.
#   Installed by ensure_crit_cli in scripts/update-agent-assets.sh from the pinned
#   GitHub release on every OS; not required, so a missing binary is not a failure.
#
function check_crit_cli() {
    local target="${HOME%/}/.local/bin/crit"

    if [ ! -x "${target}" ]; then
        printf 'not applicable: Crit CLI (not installed)\n'
        return 0
    fi

    printf 'found:   crit -> %s (pinned release)\n' "${target}"
    "${target}" --version || warn_optional "crit --version failed; the managed binary may be corrupt (try REPAIR=1 make doctor)"
}

#
# @description Print the current GitHub CLI extension state when gh is installed.
#
function check_gh_extensions() {
    if command -v gh > /dev/null 2>&1 && ! gh extension list; then
        warn_optional "unable to list installed GitHub CLI extensions"
    fi
}

#
# @description Report the installed agmsg skill's version against the pinned
#   manifest version. Installed by update_agmsg in
#   scripts/update-agent-assets.sh from the pinned upstream commit; not
#   required, so a missing install is not a failure.
#
function check_agmsg() {
    local target="${HOME%/}/.agents/skills/agmsg"
    local script_dir pin installed

    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    pin="$(awk -F'"' '/^AGMSG_PIN_VERSION=/ { print $2; exit }' "${script_dir}/update-agent-assets.sh" 2> /dev/null || true)"

    if [ ! -f "${target}/VERSION" ]; then
        printf 'not applicable: agmsg (not installed)\n'
        return 0
    fi

    installed="$(cat "${target}/VERSION")"
    if [ "${installed}" = "${pin:-unknown}" ]; then
        printf 'found:   agmsg -> %s (version %s, matches pin)\n' "${target}" "${installed}"
    else
        printf 'found:   agmsg -> %s (version %s, pin %s)\n' "${target}" "${installed}" "${pin:-unknown}"
        warn_optional "agmsg version ${installed} does not match the pinned ${pin:-unknown}; run make update"
    fi
}

#
# @description Run the read-only dotfiles health checks.
#
function main() {
    section "Core commands"
    check_command git --version
    check_command chezmoi --version
    check_command mise --version
    check_command uv --version
    check_command gh --version

    section "Chezmoi"
    run_required_doctor chezmoi doctor
    check_private_chezmoi

    section "Mise"
    run_required_doctor mise doctor
    run_required_doctor mise ls --current

    section "Homebrew"
    check_homebrew

    section "Crit CLI"
    check_crit_cli

    section "SSH"
    check_machine_ssh_key

    section "GitHub CLI extensions"
    check_gh_extensions

    section "agmsg"
    check_agmsg

    printf '\nTool check summary: required failures: %d; optional warnings: %d\n' \
        "${required_failures}" "${optional_warnings}"
    [ "${required_failures}" -eq 0 ]
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
