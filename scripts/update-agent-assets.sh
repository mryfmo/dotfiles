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
readonly CLAUDE_CRIT_PLUGIN="crit@crit"
readonly CLAUDE_CRIT_MARKETPLACE="tomasz-tomczyk/crit"
readonly CLAUDE_CRIT_MARKETPLACE_NAME="crit"
readonly CLAUDE_PONYTAIL_PLUGIN="ponytail@ponytail"
readonly CLAUDE_PONYTAIL_MARKETPLACE="DietrichGebert/ponytail"
readonly CLAUDE_PONYTAIL_MARKETPLACE_NAME="ponytail"
readonly CODEX_SUPERPOWERS_PLUGIN="superpowers@openai-curated"
readonly CODEX_PONYTAIL_PLUGIN="ponytail@ponytail"
readonly CODEX_PONYTAIL_MARKETPLACE="DietrichGebert/ponytail"
readonly CODEX_PONYTAIL_MARKETPLACE_NAME="ponytail"
readonly CODEX_PONYTAIL_MARKETPLACE_SOURCE="https://github.com/DietrichGebert/ponytail.git"
readonly CCGATE_MISE_TOOL="aqua:tak848/ccgate"

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
# @description Return success when the current OS is macOS.
#
function is_macos() {
    [ "$(uname)" = "Darwin" ]
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

    root="$(codex_marketplace_root "${marketplace}")"
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
# @description Print the local root path for a configured Codex marketplace.
# @arg $1 string Marketplace name.
#
function codex_marketplace_root() {
    local marketplace="$1"

    codex plugin marketplace list 2> /dev/null | awk -v name="${marketplace}" '$1 == name { print $2; exit }'
}

#
# @description Return success when a Git root has the expected origin URL.
# @arg $1 string Git working tree root.
# @arg $2 string Expected HTTPS origin URL.
#
function git_remote_origin_matches() {
    local root="$1"
    local expected_source="$2"
    local expected_ssh="git@github.com:${expected_source#https://github.com/}"
    local remote

    remote="$(git -C "${root}" config --get remote.origin.url 2> /dev/null || true)"
    case "${remote}" in
    "${expected_source}" | "${expected_source%.git}" | "${expected_ssh}" | "${expected_ssh%.git}")
        return 0
        ;;
    esac
    return 1
}

#
# @description Return success when a configured Codex marketplace has a matching Git origin.
# @arg $1 string Marketplace name.
# @arg $2 string Expected HTTPS origin URL.
#
function codex_marketplace_has_source() {
    local marketplace="$1"
    local expected_source="$2"
    local root

    root="$(codex_marketplace_root "${marketplace}")"
    if [ -z "${root}" ] || [ ! -d "${root}/.git" ]; then
        return 1
    fi

    git_remote_origin_matches "${root}" "${expected_source}"
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
# @description Ensure the Crit CLI is available for agent integrations.
#
function ensure_crit_cli() {
    if has_command crit; then
        return 0
    fi

    if is_macos && has_command brew; then
        section "Crit CLI"
        brew install crit || true
    fi

    if ! has_command crit; then
        printf 'Skipping Crit integrations: crit command not found.\n'
        return 1
    fi
}

#
# @description Ensure the Crit Claude Code plugin marketplace is configured.
#
function ensure_claude_crit_marketplace() {
    if command_output_contains "${CLAUDE_CRIT_MARKETPLACE_NAME}" claude plugin marketplace list; then
        return 0
    fi

    claude plugin marketplace add "${CLAUDE_CRIT_MARKETPLACE}"
}

#
# @description Ensure the Ponytail Claude Code plugin marketplace is configured.
#
function ensure_claude_ponytail_marketplace() {
    if command_output_contains "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" claude plugin marketplace list; then
        return 0
    fi

    claude plugin marketplace add "${CLAUDE_PONYTAIL_MARKETPLACE}"
}

#
# @description Return success when the Claude Code Crit plugin is already enabled.
#
function claude_crit_plugin_is_enabled() {
    if ! has_command python3; then
        return 1
    fi

    claude plugin list --json 2> /dev/null | CLAUDE_CRIT_PLUGIN_ID="${CLAUDE_CRIT_PLUGIN}" python3 -c '
import json
import os
import sys

try:
    plugins = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

plugin_id = os.environ["CLAUDE_CRIT_PLUGIN_ID"]
enabled = any(
    isinstance(plugin, dict)
    and plugin.get("id") == plugin_id
    and plugin.get("enabled") is True
    for plugin in plugins
)
sys.exit(0 if enabled else 1)
'
}

#
# @description Return success when the Claude Code Ponytail plugin is already enabled.
#
function claude_ponytail_plugin_is_enabled() {
    if ! has_command python3; then
        return 1
    fi

    claude plugin list --json 2> /dev/null | CLAUDE_PONYTAIL_PLUGIN_ID="${CLAUDE_PONYTAIL_PLUGIN}" python3 -c '
import json
import os
import sys

try:
    plugins = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

plugin_id = os.environ["CLAUDE_PONYTAIL_PLUGIN_ID"]
enabled = any(
    isinstance(plugin, dict)
    and plugin.get("id") == plugin_id
    and plugin.get("enabled") is True
    for plugin in plugins
)
sys.exit(0 if enabled else 1)
'
}

#
# @description Ensure ccgate is available for agent PermissionRequest hooks.
#
function ensure_ccgate_cli() {
    if has_command ccgate; then
        ccgate --version || true
        return 0
    fi

    if has_command mise; then
        section "ccgate"
        mise install --yes "${CCGATE_MISE_TOOL}" || true
    fi

    if has_command ccgate; then
        ccgate --version || true
        return 0
    fi

    printf 'Skipping ccgate hook runtime verification: ccgate command not found.\n'
    return 1
}

#
# @description Install or refresh the Herdr agent integrations.
#
function ensure_herdr_integrations() {
    if ! has_command herdr; then
        return 0
    fi

    section "herdr integrations"
    herdr integration install claude
    herdr integration install codex
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
# @description Install or update the Claude Code Crit plugin.
#
function update_claude_crit() {
    if ! has_command claude; then
        printf 'Skipping Claude Code Crit plugin: claude command not found.\n'
        return 0
    fi

    section "Claude Code Crit plugin"
    if ! ensure_crit_cli; then
        return 0
    fi
    ensure_claude_crit_marketplace
    claude plugin marketplace update "${CLAUDE_CRIT_MARKETPLACE_NAME}" || true

    if command_output_contains "\"id\":\"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json ||
        command_output_contains "\"id\": \"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json; then
        claude plugin update "${CLAUDE_CRIT_PLUGIN}" || true
    else
        claude plugin install "${CLAUDE_CRIT_PLUGIN}" || true
    fi
    if claude_crit_plugin_is_enabled; then
        printf 'Claude Code Crit plugin is already enabled.\n'
    else
        claude plugin enable "${CLAUDE_CRIT_PLUGIN}" || true
    fi
}

#
# @description Install or update the Claude Code Ponytail plugin.
#
function update_claude_ponytail() {
    if ! has_command claude; then
        printf 'Skipping Claude Code Ponytail plugin: claude command not found.\n'
        return 0
    fi

    section "Claude Code Ponytail plugin"
    ensure_claude_ponytail_marketplace
    claude plugin marketplace update "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" || true

    if command_output_contains "\"id\":\"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json ||
        command_output_contains "\"id\": \"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json; then
        claude plugin update "${CLAUDE_PONYTAIL_PLUGIN}" || true
    else
        claude plugin install "${CLAUDE_PONYTAIL_PLUGIN}" || true
    fi
    if claude_ponytail_plugin_is_enabled; then
        printf 'Claude Code Ponytail plugin is already enabled.\n'
    else
        claude plugin enable "${CLAUDE_PONYTAIL_PLUGIN}" || true
    fi
    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
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
# @description Ensure the Ponytail Codex plugin marketplace is configured.
#
function ensure_codex_ponytail_marketplace() {
    local codex_home="${CODEX_HOME:-${HOME}/.codex}"
    local codex_config="${codex_home%/}/config.toml"

    if [ -f "${codex_config}" ] && grep -Fq "[marketplaces.${CODEX_PONYTAIL_MARKETPLACE_NAME}]" "${codex_config}"; then
        if grep -Fq "source = \"${CODEX_PONYTAIL_MARKETPLACE_SOURCE}\"" "${codex_config}"; then
            return 0
        fi
        printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
        return 1
    fi

    if codex_marketplace_has_source "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"; then
        return 0
    fi
    if command_output_contains "${CODEX_PONYTAIL_MARKETPLACE_NAME}" codex plugin marketplace list; then
        printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
        return 1
    fi

    codex plugin marketplace add "${CODEX_PONYTAIL_MARKETPLACE}"
}

#
# @description Install or update the Codex Ponytail plugin from its marketplace.
#
function update_codex_ponytail() {
    if ! has_command codex; then
        printf 'Skipping Codex Ponytail plugin: codex command not found.\n'
        return 0
    fi

    section "Codex Ponytail plugin"
    ensure_codex_ponytail_marketplace
    codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}" || true

    if command_output_contains "\"pluginId\":\"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json ||
        command_output_contains "\"pluginId\": \"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json; then
        printf 'Codex Ponytail plugin is already installed.\n'
    else
        codex plugin add "${CODEX_PONYTAIL_PLUGIN}" || true
    fi
    printf 'Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.\n'
    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
}

#
# @description Install or update the Codex Crit plugin and plan-review hook.
#
function update_codex_crit() {
    if ! has_command codex; then
        printf 'Skipping Codex Crit plugin: codex command not found.\n'
        return 0
    fi
    if ! ensure_crit_cli; then
        return 0
    fi

    section "Codex Crit plugin"
    (
        cd "${HOME}"
        crit install codex-plugin --force
    ) || true
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
    update_claude_crit
    update_claude_ponytail
    update_codex_superpowers
    update_codex_crit
    update_codex_ponytail
    ensure_herdr_integrations
    ensure_ccgate_cli
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
