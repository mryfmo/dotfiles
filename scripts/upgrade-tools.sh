#!/usr/bin/env bash

# @file scripts/upgrade-tools.sh
# @brief Explicitly upgrade tools managed outside normal `chezmoi apply`.
# @description
#   Keeps the bootstrap path stable by moving package-manager upgrades into an
#   intentional lifecycle command. The default mode upgrades user-level tooling
#   and Homebrew-managed packages when those managers are available. Pass
#   `--system` to include operating-system package upgrades such as apt.

set -Eeuo pipefail

include_system=false

#
# @description Print a section heading.
# @arg $1 string Heading text.
#
function section() {
    printf '\n==> %s\n' "$1"
}

#
# @description Return success when the current OS is macOS.
#
function is_macos() {
    [ "$(uname)" = "Darwin" ]
}

#
# @description Return success when the current OS is Linux.
#
function is_linux() {
    [ "$(uname)" = "Linux" ]
}

#
# @description Return success when a command is available.
# @arg $1 string Command name.
#
function has_command() {
    command -v "$1" > /dev/null 2>&1
}

#
# @description Run a command only when it exists.
# @arg $1 string Command name.
# @arg $@ string Command arguments.
#
function run_if_available() {
    local command_name="$1"
    shift || true

    if ! has_command "${command_name}"; then
        printf 'Skipping %s; command not found.\n' "${command_name}"
        return 0
    fi

    "${command_name}" "$@"
}

#
# @description Upgrade Homebrew packages on macOS when Homebrew is installed.
#
function upgrade_homebrew() {
    if ! is_macos || ! has_command brew; then
        return 0
    fi

    section "Homebrew"
    brew update
    brew upgrade
}

#
# @description Upgrade the standalone mise binary when self-update is available.
#
function upgrade_mise_self() {
    if ! has_command mise; then
        return 0
    fi

    section "mise self-update"
    mise self-update --yes || true
}

#
# @description Upgrade mise-managed tools declared in the repository config.
#
function upgrade_mise_tools() {
    if ! has_command mise; then
        return 0
    fi

    section "mise tools"
    mise trust --yes
    # Keep the npm safety window used by the bootstrap installer so freshly
    # published npm packages are not picked up immediately.
    mise install --before 7d
}

#
# @description Upgrade uv tool installations when uv is available.
#
function upgrade_uv_tools() {
    if ! has_command uv; then
        return 0
    fi

    section "uv tools"
    uv tool upgrade --all || true
}

#
# @description Upgrade GitHub CLI extensions when gh is available.
#
function upgrade_gh_extensions() {
    if ! has_command gh; then
        return 0
    fi

    section "GitHub CLI extensions"
    gh extension upgrade --all || true
}

#
# @description Upgrade tmux plugins when TPM is installed.
#
function upgrade_tmux_plugins() {
    local tpm_update="${HOME%/}/.tmux/plugins/tpm/bin/update_plugins"

    if [ ! -x "${tpm_update}" ]; then
        return 0
    fi

    section "tmux plugins"
    "${tpm_update}" all || true
}

#
# @description Upgrade apt packages only when system upgrades are requested.
#
function upgrade_apt_packages() {
    if ! ${include_system} || ! is_linux || ! has_command apt-get; then
        return 0
    fi

    section "apt"
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get upgrade -y
}

#
# @description Parse command-line options.
# @arg $@ string Command-line arguments.
#
function parse_args() {
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --system)
                include_system=true
                ;;
            -h|--help)
                cat <<'USAGE'
Usage: scripts/upgrade-tools.sh [--system]

Upgrade tools intentionally, outside bootstrap and `chezmoi apply`.

Options:
  --system  Include operating-system package upgrades such as apt.
USAGE
                exit 0
                ;;
            *)
                printf 'Unknown option: %s\n' "$1" >&2
                exit 2
                ;;
        esac
        shift
    done
}

#
# @description Run explicit upgrades for managed tooling.
# @arg $@ string Command-line arguments.
#
function main() {
    parse_args "$@"

    upgrade_homebrew
    upgrade_mise_self
    upgrade_mise_tools
    upgrade_uv_tools
    upgrade_gh_extensions
    upgrade_tmux_plugins
    upgrade_apt_packages
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
