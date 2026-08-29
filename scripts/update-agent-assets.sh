#!/usr/bin/env bash

# @file scripts/update-agent-assets.sh
# @brief Install and refresh shared AI-agent plugins and skills.
# @description
#   Keeps Codex and Claude Code agent assets aligned with the dotfiles-managed
#   skill tree. Skills are applied by chezmoi from `home/dot_agents/skills`;
#   this script handles CLI-managed plugin marketplace refreshes and plugin
#   installation that cannot be represented as plain files.

set -Eeuo pipefail

#
# @description Resolve the dotfiles repository source root.
# @stdout Absolute source root containing the vendored CompactionDB tree.
# @exitcode 0 A valid source root was found.
# @exitcode 1 Neither the wrapper export nor direct script path was valid.
#
function resolve_dotfiles_source_dir() {
    local candidate

    if [[ -n "${DOTFILES_SOURCE_DIR:-}" ]] && [[ -d "${DOTFILES_SOURCE_DIR}/vendor/compactiondb" ]]; then
        printf '%s\n' "${DOTFILES_SOURCE_DIR}"
        return 0
    fi

    candidate="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    if [[ -d "${candidate}/vendor/compactiondb" ]]; then
        printf '%s\n' "${candidate}"
        return 0
    fi

    printf 'Unable to resolve dotfiles source root: vendor/compactiondb was not found via DOTFILES_SOURCE_DIR or BASH_SOURCE.\n' >&2
    return 1
}

DOTFILES_REPO_SOURCE_DIR="$(resolve_dotfiles_source_dir)" || exit 1
readonly DOTFILES_REPO_SOURCE_DIR
AGENT_ASSET_SCRIPT_DIR="${DOTFILES_REPO_SOURCE_DIR}/scripts"
readonly AGENT_ASSET_SCRIPT_DIR
if ! declare -F manifest_record > /dev/null 2>&1; then
    # shellcheck source=scripts/lib/asset-manifest.sh
    source "${AGENT_ASSET_SCRIPT_DIR}/lib/asset-manifest.sh"
fi
# shellcheck source=scripts/lib/installer-pins.sh
source "${AGENT_ASSET_SCRIPT_DIR}/lib/installer-pins.sh"

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
readonly CLAUDE_UNDERSTAND_ANYTHING_PLUGIN="understand-anything@understand-anything"
readonly CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE="Egonex-AI/Understand-Anything"
readonly CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME="understand-anything"
# Pinned like HOMEBREW_INSTALL_COMMIT in install/macos/common/brew.sh; bump both
# values together after reviewing the upstream installer diff.
readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT="797ce7969312411be2e125c39628854166f055d7"
readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256="54f0350d09f43fcc8245f3f1fb2057bd322c36c6f158483dd47dcaf5f4a44eba"
readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL="https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}/install.sh"
# Versions and installer checksums for both URLs are pinned in
# scripts/lib/installer-pins.sh and bumped by scripts/upgrade-tools.sh.
# Install paths below assume the default XDG layout; the upstream installers
# honor XDG_*_HOME/TODE_INSTALL_ROOT overrides that this lifecycle does not.
readonly TERMINAL_CODE_INSTALLER_URL="https://tode.sh/install"
readonly TERMINAL_BROWSER_INSTALLER_URL="https://terminal-browser.sh/install"

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
# @description Remove node-global agent CLIs that shadow their dedicated mise tools.
#
function remove_node_global_agent_cli_shadows() {
    local npm_package

    has_command npm || return 0
    for npm_package in "@openai/codex" "@anthropic-ai/claude-code"; do
        if npm list -g "${npm_package}" --depth=0 > /dev/null 2>&1; then
            npm uninstall -g "${npm_package}"
        fi
    done
}

#
# @description Reinstall one broken mise-managed agent CLI through npm.
# @arg $1 string CLI command name.
# @arg $2 string mise npm tool name.
#
function ensure_mise_npm_agent_cli() {
    local cli="$1"
    local mise_tool="$2"

    if has_command "${cli}" && "${cli}" --version > /dev/null 2>&1; then
        return 0
    fi
    has_command mise || return 0

    printf 'Repairing %s through the mise npm backend.\n' "${cli}"
    MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 \
        mise install --force --locked "${mise_tool}"
    hash -r
    "${cli}" --version > /dev/null
    manifest_record "ensure_mise_npm_agent_cli:${cli}" installer "$("${cli}" --version 2> /dev/null || printf 'unknown\n')" "$(mise where "${mise_tool}" 2> /dev/null || command -v "${cli}")" -- "MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 mise install --force --locked ${mise_tool}"
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
# @description Ensure the Understand-Anything Claude Code plugin marketplace is configured.
#
function ensure_claude_understand_anything_marketplace() {
    if command_output_contains "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" claude plugin marketplace list; then
        return 0
    fi

    claude plugin marketplace add "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}"
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
# @description Return success when the Claude Code Understand-Anything plugin is already enabled.
#
function claude_understand_anything_plugin_is_enabled() {
    if ! has_command python3; then
        return 1
    fi

    claude plugin list --json 2> /dev/null | CLAUDE_UNDERSTAND_ANYTHING_PLUGIN_ID="${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" python3 -c '
import json
import os
import sys

try:
    plugins = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

plugin_id = os.environ["CLAUDE_UNDERSTAND_ANYTHING_PLUGIN_ID"]
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
# @description Install or refresh the Herdr agent integrations.
#
function ensure_herdr_integrations() {
    if ! has_command herdr; then
        return 0
    fi

    section "herdr integrations"
    herdr integration install claude
    herdr integration install codex
    manifest_record "ensure_herdr_integrations" integration "$(herdr --version 2> /dev/null | awk 'NF { version = $NF } END { print version ? version : "unknown" }')" "${HOME}/.claude/hooks/herdr-agent-state.sh" "${HOME}/.codex/herdr-agent-state.sh" -- "herdr integration install claude" "herdr integration install codex"
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
    manifest_record "update_claude_superpowers" plugin "$(manifest_claude_plugin_version "${CLAUDE_SUPERPOWERS_PLUGIN}")" "${HOME}/.claude/plugins/cache/claude-plugins-official/superpowers" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_SUPERPOWERS_MARKETPLACE}" "claude plugin marketplace update claude-plugins-official" "claude plugin install ${CLAUDE_SUPERPOWERS_PLUGIN}" "claude plugin update ${CLAUDE_SUPERPOWERS_PLUGIN}"
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
    manifest_record "update_claude_crit" plugin "$(manifest_claude_plugin_version "${CLAUDE_CRIT_PLUGIN}")" "${HOME}/.claude/plugins/cache/crit/crit" "${HOME}/.claude/settings.json" -- "brew install crit" "claude plugin marketplace add ${CLAUDE_CRIT_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_CRIT_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_CRIT_PLUGIN}" "claude plugin update ${CLAUDE_CRIT_PLUGIN}" "claude plugin enable ${CLAUDE_CRIT_PLUGIN}"
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
    manifest_record "update_claude_ponytail" plugin "$(manifest_claude_plugin_version "${CLAUDE_PONYTAIL_PLUGIN}")" "${HOME}/.claude/plugins/cache/ponytail/ponytail" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_PONYTAIL_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin update ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin enable ${CLAUDE_PONYTAIL_PLUGIN}"
}

#
# @description Install or update the Claude Code Understand-Anything plugin.
#
function update_claude_understand_anything() {
    if ! has_command claude; then
        printf 'Skipping Claude Code Understand-Anything plugin: claude command not found.\n'
        return 0
    fi

    section "Claude Code Understand-Anything plugin"
    ensure_claude_understand_anything_marketplace
    claude plugin marketplace update "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" || true

    if command_output_contains "\"id\":\"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json ||
        command_output_contains "\"id\": \"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json; then
        claude plugin update "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
    else
        claude plugin install "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
    fi
    if claude_understand_anything_plugin_is_enabled; then
        printf 'Claude Code Understand-Anything plugin is already enabled.\n'
    else
        claude plugin enable "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
    fi
    manifest_record "update_claude_understand_anything" plugin "$(manifest_claude_plugin_version "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}")" "${HOME}/.claude/plugins/cache/understand-anything/understand-anything" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin update ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin enable ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}"
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
    manifest_record "update_codex_superpowers" plugin "$(manifest_codex_plugin_version "${CODEX_SUPERPOWERS_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/.tmp/plugins/plugins/superpowers" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin marketplace upgrade openai-curated" "codex plugin add ${CODEX_SUPERPOWERS_PLUGIN}"
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
    manifest_record "update_codex_ponytail" plugin "$(manifest_codex_plugin_version "${CODEX_PONYTAIL_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/plugins/cache/ponytail/ponytail" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin marketplace add ${CODEX_PONYTAIL_MARKETPLACE}" "codex plugin marketplace upgrade ${CODEX_PONYTAIL_MARKETPLACE_NAME}" "codex plugin add ${CODEX_PONYTAIL_PLUGIN}"
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
    manifest_record "update_codex_crit" plugin "$(manifest_brew_formula_version crit)" "${CODEX_HOME:-${HOME}/.codex}/plugins/crit" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "brew install crit" "crit install codex-plugin --force"
}

#
# @description Provision Codex Understand-Anything runtime files from the matching Claude release artifact.
# @stdout Prints a skip message when no matching Claude release artifact is available.
#
function provision_codex_understand_anything_runtime() {
    local plugin_root claude_cache release_root source destination

    plugin_root="${HOME}/.understand-anything/repo/understand-anything-plugin"
    claude_cache="${HOME}/.claude/plugins/cache/understand-anything/understand-anything"
    if ! has_command python3; then
        printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
        return 0
    fi
    release_root="$(
        python3 - "${plugin_root}/.claude-plugin/plugin.json" "${claude_cache}" << 'PY'
import json
import sys
from pathlib import Path

plugin_manifest = Path(sys.argv[1])
cache_root = Path(sys.argv[2])
try:
    version = json.loads(plugin_manifest.read_text())["version"]
except (OSError, json.JSONDecodeError, KeyError):
    sys.exit(0)

matches = []
for candidate in cache_root.iterdir() if cache_root.is_dir() else ():
    try:
        if json.loads((candidate / ".claude-plugin/plugin.json").read_text())["version"] == version:
            matches.append(candidate)
    except (OSError, json.JSONDecodeError, KeyError):
        pass
try:
    release_root = max(matches, key=lambda path: tuple(int(part) for part in path.name.split(".")))
except ValueError:
    release_root = max(matches, key=lambda path: path.name, default=None)
print(release_root or "")
PY
    )"
    if [ -z "${release_root}" ]; then
        printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
        return 0
    fi

    for source in "packages/core/dist" "packages/core/node_modules" "node_modules"; do
        destination="${plugin_root}/${source}"
        [ -d "${release_root}/${source}" ] || continue
        rm -rf "${destination}"
        mkdir -p "$(dirname "${destination}")"
        cp -R "${release_root}/${source}" "${destination}"
    done
}

#
# @description Install or update the Codex Understand-Anything skills via the vendor installer.
# @description
#   The installer clones the upstream repo into ~/.understand-anything/repo and
#   symlinks its skills into ~/.agents/skills; check-agent-runtime.py reports
#   those symlinks as an expected unmanaged-skill WARN.
#
function update_codex_understand_anything() {
    if ! has_command codex; then
        printf 'Skipping Codex Understand-Anything skills: codex command not found.\n'
        return 0
    fi

    section "Codex Understand-Anything skills"
    (
        local actual installer
        installer="$(mktemp)"
        trap 'rm -f "${installer}"' EXIT
        curl -fsSL "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" -o "${installer}" || {
            printf 'Skipping Codex Understand-Anything skills: installer download failed.\n'
            return 0
        }
        actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
        [ "${actual}" = "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256}" ] || {
            printf 'Understand-Anything installer checksum mismatch\n' >&2
            return 1
        }
        bash "${installer}" codex < /dev/null || {
            printf 'Understand-Anything installer failed; Codex skills unchanged.\n' >&2
            return 1
        }
        provision_codex_understand_anything_runtime
        # shellcheck disable=SC2016 # $understand is the literal Codex skill invocation, not a variable.
        printf 'Invoke Understand-Anything in Codex with $understand after restarting the CLI.\n'
    ) || true
    manifest_record "update_codex_understand_anything" installer "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}" "${HOME}/.understand-anything/repo" "${HOME}/.agents/skills/understand" "${HOME}/.agents/skills/understand-chat" "${HOME}/.agents/skills/understand-dashboard" "${HOME}/.agents/skills/understand-diff" "${HOME}/.agents/skills/understand-domain" "${HOME}/.agents/skills/understand-explain" "${HOME}/.agents/skills/understand-figma" "${HOME}/.agents/skills/understand-knowledge" "${HOME}/.agents/skills/understand-onboard" -- "curl -fsSL ${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer> codex"
}

#
# @description Return success when the zenbu-labs installers support this platform.
# @description
#   Upstream publishes darwin-arm64, linux-x64, and linux-arm64 builds only;
#   Intel macOS has no release asset, so it is skipped rather than failed.
#
function zenbu_platform_supported() {
    case "$(uname -s)-$(uname -m)" in
    Darwin-arm64 | Linux-x86_64 | Linux-amd64 | Linux-aarch64 | Linux-arm64)
        return 0
        ;;
    esac
    return 1
}

#
# @description Download an upstream installer, verify its pinned checksum, and run it.
# @arg $1 string Installer URL.
# @arg $2 string Expected installer script SHA256.
# @arg $@ string Optional NAME=value environment assignments for the installer run.
#
function run_pinned_installer() {
    local url="$1"
    local expected="$2"
    local actual installer
    shift 2

    installer="$(mktemp)"
    # shellcheck disable=SC2064 # Expand the temp path now; it never changes.
    trap "rm -f '${installer}'" RETURN
    curl -fsSL "${url}" -o "${installer}" || {
        printf 'Installer download failed: %s\n' "${url}" >&2
        return 1
    }
    actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
    [ "${actual}" = "${expected}" ] || {
        printf 'Installer checksum mismatch for %s\n' "${url}" >&2
        return 1
    }
    env "$@" bash "${installer}" < /dev/null
}

#
# @description Install or update the terminal-code (tode) CLI at the pinned version.
#
function update_terminal_code() {
    local installed

    zenbu_platform_supported || {
        printf 'Skipping terminal-code: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
        return 0
    }

    section "terminal-code (tode)"
    installed="$(jq -r '.version' "${HOME}/.local/state/tode/install.json" 2> /dev/null || printf 'none\n')"
    # Short-circuit only when every manifest-recorded artifact is present, so a
    # partially deleted install is repaired instead of skipped forever.
    if [ "${installed}" = "${TERMINAL_CODE_PIN_VERSION}" ] &&
        [ -x "${HOME}/.local/bin/tode" ] &&
        [ -d "${HOME}/.local/lib/tode" ]; then
        printf 'tode %s is already installed.\n' "${installed}"
    else
        run_pinned_installer "${TERMINAL_CODE_INSTALLER_URL}" "${TERMINAL_CODE_INSTALLER_SHA256}" ||
            printf 'tode installer failed; existing install unchanged.\n' >&2
    fi
    manifest_record "update_terminal_code" installer "${TERMINAL_CODE_PIN_VERSION}" "${HOME}/.local/lib/tode" "${HOME}/.local/bin/tode" "${HOME}/.local/state/tode/install.json" -- "curl -fsSL ${TERMINAL_CODE_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer>"
}

#
# @description Install or update the terminal-browser CLI at the pinned version.
# @description
#   The installer symlinks its bundled skills into ~/.agents/skills and
#   per-agent skill directories, recording every link in
#   ~/.local/state/terminal-browser/skills.links; check-agent-runtime.py reads
#   that receipt and reports the shared links as expected unmanaged-skill
#   WARNs. Editor setup is always skipped for non-interactive lifecycle runs;
#   run `terminal-browser setup` manually once if wanted.
#
function update_terminal_browser() {
    local installed

    zenbu_platform_supported || {
        printf 'Skipping terminal-browser: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
        return 0
    }

    section "terminal-browser"
    installed="$(cat "${HOME}/.local/share/terminal-browser/app/VERSION" 2> /dev/null || printf 'none\n')"
    # Short-circuit only when every manifest-recorded artifact is present, so a
    # partially deleted install is repaired instead of skipped forever.
    if [ "${installed}" = "${TERMINAL_BROWSER_PIN_VERSION}" ] &&
        [ -x "${HOME}/.local/bin/terminal-browser" ] &&
        [ -f "${HOME}/.local/state/terminal-browser/skills.links" ]; then
        printf 'terminal-browser %s is already installed.\n' "${installed}"
    else
        run_pinned_installer "${TERMINAL_BROWSER_INSTALLER_URL}" "${TERMINAL_BROWSER_INSTALLER_SHA256}" TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 ||
            printf 'terminal-browser installer failed; existing install unchanged.\n' >&2
    fi
    manifest_record "update_terminal_browser" installer "${TERMINAL_BROWSER_PIN_VERSION}" "${HOME}/.local/share/terminal-browser/app" "${HOME}/.local/bin/terminal-browser" "${HOME}/.local/state/terminal-browser/skills.links" -- "curl -fsSL ${TERMINAL_BROWSER_INSTALLER_URL}" "shasum -a 256 <installer>" "TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 bash <installer>"
}

#
# @description Sync the vendored CompactionDB tree without deleting project runtime state.
#
function update_compactiondb() {
    local source_root
    source_root="${DOTFILES_REPO_SOURCE_DIR}/vendor/compactiondb/"
    rsync -a --delete --exclude '.claude/contextdb/state/' --exclude '.claude/contextdb/spool/' --exclude '.claude/contextdb/health/' --exclude '.claude/contextdb/contextdb.sqlite3*' "${source_root}" "${HOME}/.agents/compactiondb/" || true
    manifest_record "update_compactiondb" rsync "$(awk '/^## / { print $2; exit }' "${source_root}CHANGELOG.md")" "${HOME}/.agents/compactiondb" -- "rsync -a --delete --exclude .claude/contextdb/state/ --exclude .claude/contextdb/spool/ --exclude .claude/contextdb/health/ --exclude .claude/contextdb/contextdb.sqlite3* ${source_root} ${HOME}/.agents/compactiondb/"
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

    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
    remove_node_global_agent_cli_shadows
    ensure_mise_npm_agent_cli claude "npm:@anthropic-ai/claude-code"
    ensure_mise_npm_agent_cli codex "npm:@openai/codex"
    update_claude_superpowers
    update_claude_crit
    update_claude_ponytail
    update_claude_understand_anything
    update_codex_superpowers
    update_codex_crit
    update_codex_ponytail
    update_codex_understand_anything
    update_terminal_code
    update_terminal_browser
    update_compactiondb
    ensure_herdr_integrations
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
