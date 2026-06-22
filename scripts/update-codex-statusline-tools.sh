#!/usr/bin/env bash

# @file scripts/update-codex-statusline-tools.sh
# @brief Install and refresh optional helpers for the Codex status display.
# @description
#   Keeps the tmux Codex status segment useful without making CodexBar a hard
#   dependency. When CodexBar CLI is already installed, the script refreshes it
#   through Homebrew if Homebrew owns it. When only CodexBar.app is installed,
#   the bundled CLI helper is symlinked into the dotfiles-managed user bin path.

set -Eeuo pipefail

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
# @description Return success when a command is available.
# @arg $1 string Command name.
#
function has_command() {
    command -v "$1" > /dev/null 2>&1
}

#
# @description Upgrade CodexBar through Homebrew when the installed CLI is brew-managed.
#
function upgrade_brew_codexbar() {
    if ! has_command brew; then
        return 1
    fi

    if brew list --formula codexbar > /dev/null 2>&1; then
        brew upgrade --formula codexbar || true
        return 0
    fi

    if brew list --formula steipete/tap/codexbar > /dev/null 2>&1; then
        brew upgrade --formula steipete/tap/codexbar || true
        return 0
    fi

    return 1
}

#
# @description Symlink the CodexBar.app bundled CLI helper when the app is installed.
#
function link_codexbar_app_cli() {
    local app_cli="/Applications/CodexBar.app/Contents/Helpers/CodexBarCLI"
    local target="${HOME%/}/.local/bin/common/codexbar"

    if ! is_macos || [ ! -x "${app_cli}" ]; then
        return 1
    fi

    mkdir -p "$(dirname "${target}")"
    ln -sf "${app_cli}" "${target}"
    "${target}" --version || true
}

#
# @description Install or refresh optional Codex status display helpers.
# @arg $@ string Command-line arguments.
#
function main() {
    if [ "$#" -gt 0 ]; then
        printf 'Usage: scripts/update-codex-statusline-tools.sh\n' >&2
        exit 2
    fi

    section "Codex statusline tools"

    if has_command codexbar; then
        upgrade_brew_codexbar || codexbar --version || true
    else
        link_codexbar_app_cli || printf 'CodexBar CLI not found; tmux status will use Codex app-server fallback.\n'
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
