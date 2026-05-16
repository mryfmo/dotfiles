#!/usr/bin/env bash

# @file scripts/check-tools.sh
# @brief Print a read-only health summary for managed dotfiles tools.
# @description
#   Reports the availability and versions of the commands that participate in
#   the dotfiles lifecycle. This script does not install, upgrade, or modify
#   tools; use `scripts/upgrade-tools.sh` for explicit upgrades.

set -Eeuo pipefail

#
# @description Print a section heading.
# @arg $1 string Heading text.
#
function section() {
    printf '\n==> %s\n' "$1"
}

#
# @description Report whether a command exists and print its version when known.
# @arg $1 string Command name.
# @arg $@ string Optional version command arguments.
#
function check_command() {
    local command_name="$1"
    shift || true

    if ! command -v "${command_name}" > /dev/null 2>&1; then
        printf 'missing: %s\n' "${command_name}"
        return 0
    fi

    printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"

    local output

    if [ "$#" -gt 0 ]; then
        output="$("${command_name}" "$@" 2>&1 || true)"
    else
        output="$("${command_name}" --version 2>&1 || true)"
    fi

    printf '%s\n' "${output}" | head -n 1
}

#
# @description Run an optional read-only doctor command when available.
# @arg $1 string Command name.
# @arg $@ string Doctor command arguments.
#
function run_optional_doctor() {
    local command_name="$1"
    shift || true

    if command -v "${command_name}" > /dev/null 2>&1; then
        "${command_name}" "$@" || true
    fi
}

#
# @description Print the configured private chezmoi source state.
#
function check_private_chezmoi() {
    local private_source="${HOME%/}/.local/share/chezmoi-private"
    local private_config="${HOME%/}/.config/chezmoi-private/chezmoi.yaml"

    if [ -d "${private_source}" ]; then
        printf 'found:   private source -> %s\n' "${private_source}"
        if [ -f "${private_config}" ]; then
            printf 'found:   private config -> %s\n' "${private_config}"
        else
            printf 'missing: private config -> %s\n' "${private_config}"
        fi
    else
        printf 'missing: private source -> %s\n' "${private_source}"
    fi
}

#
# @description Print the current Homebrew state when Homebrew is installed.
#
function check_homebrew() {
    if ! command -v brew > /dev/null 2>&1; then
        printf 'missing: brew\n'
        return 0
    fi

    brew --version | head -n 1
    brew outdated || true
}

#
# @description Print the current GitHub CLI extension state when gh is installed.
#
function check_gh_extensions() {
    if ! command -v gh > /dev/null 2>&1; then
        printf 'missing: gh\n'
        return 0
    fi

    gh --version | head -n 1
    gh extension list || true
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
    check_command tmux -V
    check_command hermes --version

    section "Chezmoi"
    run_optional_doctor chezmoi doctor
    check_private_chezmoi

    section "Mise"
    run_optional_doctor mise doctor
    run_optional_doctor mise ls --current

    section "Homebrew"
    check_homebrew

    section "GitHub CLI extensions"
    check_gh_extensions
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
