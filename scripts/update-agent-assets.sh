#!/usr/bin/env bash

# @file scripts/update-agent-assets.sh
# @brief Install and refresh shared AI-agent plugins and skills.
# @description
#   Keeps Codex and Claude Code agent assets aligned with the dotfiles-managed
#   skill tree. Skills are applied by chezmoi from `home/dot_agents/skills`;
#   this script handles CLI-managed plugin marketplace refreshes and plugin
#   installation that cannot be represented as plain files.

set -Eeuo pipefail

readonly CLAUDE_SUPERPOWERS_PLUGIN="superpowers@claude-plugins-official"
readonly CLAUDE_SUPERPOWERS_MARKETPLACE="anthropics/claude-plugins-official"
readonly CODEX_SUPERPOWERS_PLUGIN="superpowers@openai-curated"

#
# @description Print a section heading.
# @arg $1 string Heading text.
#
function section() {
    printf '\n==> %s\n' "$1"
}

#
# @description Return success when a command is available.
# @arg $1 string Command name.
#
function has_command() {
    command -v "$1" > /dev/null 2>&1
}

#
# @description Return success when a command's output contains a fixed string.
# @arg $1 string Fixed string to search for.
# @arg $@ string Command and arguments to run.
#
function command_output_contains() {
    local needle="$1"
    shift

    "$@" 2> /dev/null | grep -Fq "${needle}"
}

#
# @description Return success when a Codex marketplace is a configured Git marketplace.
# @arg $1 string Marketplace name.
#
function codex_marketplace_is_configured_git_marketplace() {
    local marketplace="$1"
    local root

    root="$(codex plugin marketplace list 2> /dev/null | awk -v name="${marketplace}" '$1 == name { print $2; exit }')"
    # Built-in/default marketplaces can resolve under Codex's .tmp plugin cache.
    # They may contain Git metadata, but `codex plugin marketplace upgrade` only
    # accepts configured Git marketplaces.
    case "${root}" in
    */.codex/.tmp/plugins | */.codex/.tmp/plugins/*)
        return 1
        ;;
    esac
    if [ -z "${root}" ] || [ ! -d "${root}/.git" ]; then
        return 1
    fi

    return 0
}

#
# @description Ensure the official Claude Code plugin marketplace is configured.
#
function ensure_claude_superpowers_marketplace() {
    if command_output_contains "claude-plugins-official" claude plugin marketplace list; then
        return 0
    fi

    claude plugin marketplace add "${CLAUDE_SUPERPOWERS_MARKETPLACE}"
}

#
# @description Install or update the Claude Code Superpowers plugin.
#
function update_claude_superpowers() {
    if ! has_command claude; then
        printf 'Skipping Claude Code plugins: claude command not found.\n'
        return 0
    fi

    section "Claude Code plugins"
    ensure_claude_superpowers_marketplace
    claude plugin marketplace update claude-plugins-official || true

    if command_output_contains "\"id\":\"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json ||
        command_output_contains "\"id\": \"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json; then
        claude plugin update "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
    else
        claude plugin install "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
    fi
}

#
# @description Install or update the Codex Superpowers plugin from configured marketplaces.
#
function update_codex_superpowers() {
    if ! has_command codex; then
        printf 'Skipping Codex plugins: codex command not found.\n'
        return 0
    fi

    section "Codex plugins"
    if codex_marketplace_is_configured_git_marketplace openai-curated; then
        codex plugin marketplace upgrade openai-curated || true
    else
        printf 'Skipping Codex marketplace upgrade: openai-curated is not a configured Git marketplace.\n'
    fi

    if command_output_contains "\"pluginId\":\"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json ||
        command_output_contains "\"pluginId\": \"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json; then
        printf 'Codex Superpowers plugin is already installed.\n'
    else
        codex plugin add "${CODEX_SUPERPOWERS_PLUGIN}" || true
    fi
}

#
# @description Install and refresh managed agent plugin assets.
# @arg $@ string Command-line arguments.
#
function main() {
    if [ "$#" -gt 0 ]; then
        printf 'Usage: scripts/update-agent-assets.sh\n' >&2
        exit 2
    fi

    update_claude_superpowers
    update_codex_superpowers
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
