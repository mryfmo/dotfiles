#!/usr/bin/env bash

# @file scripts/update-agent-assets.sh
# @brief Install and refresh shared AI-agent plugins and skills.
# @description
#   Converges Codex and Claude Code marketplaces and plugins, GitHub CLI
#   extensions, pinned Crit/tode/terminal-browser releases, the vendored
#   CompactionDB tree, and Herdr integrations that cannot be represented as
#   plain chezmoi-managed files.

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
# shellcheck source=scripts/lib/github-release.sh
source "${AGENT_ASSET_SCRIPT_DIR}/lib/github-release.sh"

readonly CLAUDE_SUPERPOWERS_PLUGIN="superpowers@claude-plugins-official"
readonly CLAUDE_SUPERPOWERS_MARKETPLACE="anthropics/claude-plugins-official"
readonly CLAUDE_CRIT_PLUGIN="crit@crit"
readonly CLAUDE_CRIT_MARKETPLACE="tomasz-tomczyk/crit"
readonly CLAUDE_CRIT_MARKETPLACE_NAME="crit"
readonly CRIT_RELEASE_REPO="tomasz-tomczyk/crit"
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
# Rendered from assets.understand-anything-installer in
# home/dot_agents/agent-config.yaml; change the commit and sha256 there together
# after reviewing the upstream installer diff.
readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT="6df3065f1d8ddc2ce3615314d1d493f36d6b1c80"
readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256="cb84ca53ced03f41662c5c86edf11fa598a0403c347f1e815f987ccaae5bc464"
readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL="https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}/install.sh"
# Versions and installer checksums for both URLs are pinned in
# scripts/lib/installer-pins.sh, rendered from assets: in agent-config.yaml.
# Rendered from assets.agmsg in home/dot_agents/agent-config.yaml; change the
# commit, sha256, and version there together after reviewing the upstream diff.
# Assignments stay non-readonly, like scripts/lib/installer-pins.sh, so tests
# can override them after sourcing this file.
AGMSG_PIN_COMMIT="c487be269c1973aeb01ca831806eb3f65ff3366d"
AGMSG_PIN_SHA256="9201cb5ff23ddd9ddaa19ff821dce0d0f2d58c6c292aade252a8d824b3dfc059"
AGMSG_PIN_VERSION="1.5.0"
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
        mise install --force "${mise_tool}"
    hash -r
    "${cli}" --version > /dev/null
    manifest_record "ensure_mise_npm_agent_cli:${cli}" installer "$("${cli}" --version 2> /dev/null || printf 'unknown\n')" "$(mise where "${mise_tool}" 2> /dev/null || command -v "${cli}")" -- "MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 mise install --force ${mise_tool}"
}

#
# @description Install configured GitHub CLI extensions when authentication is ready.
#
function ensure_gh_extensions() {
    bash "${DOTFILES_REPO_SOURCE_DIR}/install/common/gh_extensions.sh"
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
# @description Download one Crit release binary, verify it against the release's checksums.txt,
#   and atomically install it.
# @arg $1 string Release artifact name.
# @arg $2 string Release tag.
# @arg $3 path Destination executable path.
#
function install_crit_release() (
    local artifact="$1"
    local tag="$2"
    local target="$3"
    local actual base_url checksums download expected staging=""

    base_url="https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}"
    download="$(mktemp)" || return
    checksums="$(mktemp)" || return
    trap 'rm -f "${download}" "${checksums}" ${staging:+"${staging}"}' EXIT
    curl -fsSL "${base_url}/${artifact}" -o "${download}" || return
    curl -fsSL "${base_url}/checksums.txt" -o "${checksums}" || return
    expected="$(awk -v name="${artifact}" '$2 == name { print $1; exit }' "${checksums}")"
    actual="$(shasum -a 256 "${download}" | awk '{ print $1 }')"
    [ -n "${expected}" ] && [ "${actual}" = "${expected}" ] || {
        printf 'Crit checksum mismatch for %s %s.\n' "${artifact}" "${tag}" >&2
        return 1
    }

    mkdir -p "$(dirname "${target}")" || return
    staging="$(mktemp "${target}.XXXXXX")" || return
    install -m 0755 "${download}" "${staging}" || return
    [ "$(crit_version "${staging}")" = "${tag#v}" ] || return
    mv -f "${staging}" "${target}"
)

#
# @description Print the version a Crit binary reports, without a leading v.
# @arg $1 path Crit executable.
#
function crit_version() {
    [ -x "$1" ] || return 0
    "$1" --version 2> /dev/null | awk '$1 == "crit" { sub(/^v/, "", $2); print $2; exit }'
}

#
# @description Ensure the Crit CLI is the newest cooled-down release for agent integrations.
#
function ensure_crit_cli() {
    local artifact installed tag target

    case "$(uname -s)/$(uname -m)" in
    Linux/x86_64 | Linux/amd64) artifact="crit-linux-amd64" ;;
    Linux/aarch64 | Linux/arm64) artifact="crit-linux-arm64" ;;
    Darwin/x86_64 | Darwin/amd64) artifact="crit-darwin-amd64" ;;
    Darwin/arm64 | Darwin/aarch64) artifact="crit-darwin-arm64" ;;
    *)
        printf 'Skipping Crit integrations: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
        return 1
        ;;
    esac

    target="${HOME}/.local/bin/crit"
    installed="$(crit_version "${target}")"
    if ! tag="$(github_release_tag "${CRIT_RELEASE_REPO}")"; then
        [ -n "${installed}" ] || {
            printf 'Could not resolve a %s release.\n' "${CRIT_RELEASE_REPO}" >&2
            return 1
        }
        printf 'warning: could not resolve a Crit release; Crit %s stays.\n' "${installed}" >&2
        tag="v${installed}"
    elif [ "${installed}" != "${tag#v}" ]; then
        section "Crit CLI"
        install_crit_release "${artifact}" "${tag}" "${target}" || return 1
    fi
    export PATH="${HOME}/.local/bin:${PATH}"
    hash -r
    manifest_record "ensure_crit_cli" installer "${tag}" "${target}" -- "github_release_tag ${CRIT_RELEASE_REPO}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/${artifact}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/checksums.txt" "shasum -a 256 <binary>" "install -m 0755 <binary> ${target}"
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
# @description Re-apply only the managed Codex config files, so their modify scripts hash the
#   plugin hooks this run has just installed (Codex runs a hook only when its trust hash is current).
#   Runs last and unattended: `chezmoi apply --force`, no prompt, no network.
# @exitcode 0 Always; a failed refresh only warns, and the next apply retries it.
#
function refresh_codex_hook_trust() {
    local managed target
    local pattern='/\.codex/([a-z0-9_]+\.)?config\.toml$'
    local -a targets=()

    if ! has_command chezmoi; then
        return 0
    fi
    if ! managed="$(chezmoi managed --path-style=absolute --include=files 2> /dev/null)"; then
        printf 'WARN: Codex hook trust not refreshed: chezmoi managed failed; the next apply retries it.\n' >&2
        return 0
    fi
    while IFS= read -r target; do
        if [[ ${target} =~ ${pattern} ]]; then
            targets+=("${target}")
        fi
    done <<< "${managed}"
    if ((${#targets[@]} == 0)); then
        return 0
    fi

    section "codex hook trust"
    if ! chezmoi apply --force "${targets[@]}"; then
        printf 'WARN: Codex hook trust not refreshed: chezmoi apply failed; the next apply retries it.\n' >&2
    fi
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
    manifest_record "update_claude_crit" plugin "$(manifest_claude_plugin_version "${CLAUDE_CRIT_PLUGIN}")" "${HOME}/.claude/plugins/cache/crit/crit" "${HOME}/.claude/settings.json" -- "ensure_crit_cli" "claude plugin marketplace add ${CLAUDE_CRIT_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_CRIT_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_CRIT_PLUGIN}" "claude plugin update ${CLAUDE_CRIT_PLUGIN}" "claude plugin enable ${CLAUDE_CRIT_PLUGIN}"
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
# @description Install the Codex Superpowers plugin from the OpenAI-curated catalog.
#
function update_codex_superpowers() {
    local codex_output

    if ! has_command codex; then
        printf 'Skipping Codex plugins: codex command not found.\n'
        return 0
    fi

    section "Codex plugins"
    if command_output_contains "\"pluginId\":\"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json ||
        command_output_contains "\"pluginId\": \"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json; then
        printf 'Codex Superpowers plugin is already installed.\n'
    elif codex_output="$(codex plugin add "${CODEX_SUPERPOWERS_PLUGIN}" 2>&1)"; then
        if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
            printf '%s\n' "${codex_output}" >&2
        fi
        printf 'Codex Superpowers plugin installed.\n'
    else
        if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
            printf '%s\n' "${codex_output}" >&2
        fi
        printf 'Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.\n'
        # shellcheck disable=SC2016 # Backticks are literal operator guidance.
        printf 'Run `codex login`, then `codex plugin add %s`.\n' "${CODEX_SUPERPOWERS_PLUGIN}"
    fi
    manifest_record "update_codex_superpowers" plugin "$(manifest_codex_plugin_version "${CODEX_SUPERPOWERS_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/.tmp/plugins/plugins/superpowers" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin add ${CODEX_SUPERPOWERS_PLUGIN}"
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
    if [ -f "${HOME}/.agents/plugins/marketplace.json" ]; then
        chmod 644 "${HOME}/.agents/plugins/marketplace.json"
    fi
    manifest_record "update_codex_crit" plugin "$(crit --version 2> /dev/null | awk 'NR == 1 { print $2 }')" "${CODEX_HOME:-${HOME}/.codex}/plugins/crit" "${CODEX_HOME:-${HOME}/.codex}/config.toml" "${HOME}/.agents/skills/crit" "${HOME}/.agents/skills/crit-cli" "${HOME}/.agents/skills/crit-story" -- "ensure_crit_cli" "crit install codex-plugin --force"
}

#
# @description Build Understand-Anything packages/core in a plugin tree when its dist is missing or stale.
# @description
#   Mirrors upstream skills/understand/SKILL.md, which builds in place wherever
#   the plugin root resolves. It rebuilds when dist/index.js is missing or older
#   than any file under packages/core/src or the root pnpm-lock.yaml, the same
#   freshness rule `make doctor` reports, and otherwise skips (idempotent). With
#   mise, pnpm always runs as `mise exec npm:pnpm`, which installs the pinned
#   version on demand: a mise shim can exist before that version is installed
#   ("No version is set for shim"). A bare pnpm from PATH is used only without
#   mise.
#   A missing pnpm or a failed build only warns, so make update never fails
#   for it.
# @arg $1 path Plugin tree that contains packages/core.
# @stderr One WARN line naming the manual command when the build cannot run or fails.
#
function build_understand_anything_core() {
    local root="$1"
    local -a pnpm_cmd

    [ -d "${root}/packages/core" ] || return 0
    if [ -f "${root}/packages/core/dist/index.js" ] &&
        [ -z "$(find "${root}/packages/core/src" "${root}/pnpm-lock.yaml" -type f -newer "${root}/packages/core/dist/index.js" -print -quit 2> /dev/null || true)" ]; then
        return 0
    fi
    if has_command mise; then
        pnpm_cmd=(mise exec npm:pnpm -- pnpm)
    elif has_command pnpm; then
        pnpm_cmd=(pnpm)
    else
        printf 'WARN: Understand-Anything core not built: pnpm not found; run: cd %q && pnpm install --frozen-lockfile && pnpm --filter @understand-anything/core build\n' "${root}" >&2
        return 0
    fi
    if ! (
        cd "${root}" &&
            { "${pnpm_cmd[@]}" install --frozen-lockfile 2> /dev/null || "${pnpm_cmd[@]}" install; } &&
            "${pnpm_cmd[@]}" --filter @understand-anything/core build
    ); then
        printf 'WARN: Understand-Anything core build failed in %s; run: cd %q && %s install --frozen-lockfile && %s --filter @understand-anything/core build\n' \
            "${root}" "${root}" "${pnpm_cmd[*]}" "${pnpm_cmd[*]}" >&2
    fi
    return 0
}

#
# @description Provision Codex Understand-Anything runtime files from the matching Claude release artifact.
# @description
#   Builds packages/core in the release artifact first (upstream builds there
#   in Claude sessions) and copies dist/node_modules into the Codex clone.
#   Without a matching release artifact it builds directly in the clone.
# @stdout Prints a skip message when no matching Claude release artifact is available.
#
function provision_codex_understand_anything_runtime() {
    local plugin_root claude_cache release_root source destination

    plugin_root="${HOME}/.understand-anything/repo/understand-anything-plugin"
    claude_cache="${HOME}/.claude/plugins/cache/understand-anything/understand-anything"
    if ! has_command python3; then
        printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
        build_understand_anything_core "${plugin_root}"
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
        build_understand_anything_core "${plugin_root}"
        return 0
    fi

    build_understand_anything_core "${release_root}"
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
# @description Print sha256 lines for files with sha256sum, or shasum on macOS.
# @arg $@ path Files to hash.
# @exitcode 1 If neither tool exists or hashing fails.
#
function agmsg_sha256() {
    if command -v sha256sum > /dev/null 2>&1; then
        sha256sum -- "$@"
    elif command -v shasum > /dev/null 2>&1; then
        shasum -a 256 -- "$@"
    else
        printf 'agmsg: neither sha256sum nor shasum is available\n' >&2
        return 1
    fi
}

#
# @description Print a sorted sha256 manifest of every file under the given
#   paths of an agmsg skill directory, skipping paths that do not exist. It
#   fails rather than print a short (e.g. empty) manifest, including when find
#   cannot list a subtree.
# @arg $1 path Skill directory (e.g. ~/.agents/skills/agmsg).
# @arg $@ path Paths relative to the skill directory (dirs or files).
# @exitcode 1 If the paths cannot be listed or hashed completely.
#
function agmsg_state_snapshot() {
    local skill_dir="$1"
    local relative list file hashes
    local -a paths=() files=()
    shift

    for relative in "$@"; do
        [ ! -e "${skill_dir}/${relative}" ] || paths+=("${skill_dir}/${relative}")
    done
    ((${#paths[@]})) || return 0
    list="$(mktemp)" || return 1
    if ! find "${paths[@]}" -type f -print0 > "${list}"; then
        rm -f "${list}"
        printf 'agmsg: could not list the live state under %s\n' "${skill_dir}" >&2
        return 1
    fi
    while IFS= read -r -d '' file; do
        files+=("${file}")
    done < "${list}"
    rm -f "${list}"
    ((${#files[@]})) || return 0
    hashes="$(agmsg_sha256 "${files[@]}")" || return 1
    # sha256sum/shasum prefix a line with \ when the name needs escaping.
    if [ "$(printf '%s\n' "${hashes}" | grep -c '^\\\{0,1\}[0-9a-f]\{64\} ')" -ne "${#files[@]}" ]; then
        printf 'agmsg: hashed fewer live-state files than exist under %s\n' "${skill_dir}" >&2
        return 1
    fi
    printf '%s\n' "${hashes}" | LC_ALL=C sort
}

#
# @description Download, verify, and apply one pinned agmsg release through
#   upstream install.sh, which owns SKILL.md/VERSION/scripts/ in place. An
#   existing install (the upstream .agmsg marker) gets `install.sh --update`;
#   anything else, including the marker-less legacy vendored directory, gets
#   the plain installer, never --update. Before any installer run, the live
#   state (teams/, db/, run/, agents/) is copied to
#   ~/.agents/backups/agmsg-state-<UTC time>/ as the rollback. Afterwards every
#   file that existed under teams/ and db/messages.db must be byte-identical
#   (the installer may add files, e.g. create a missing messages.db); run/ is
#   only reported, because live watchers and --update's sync-engine restarts
#   rewrite it by design.
#   Every step checks its own status: this runs on the left of `||`, where
#   `set -e` is inert.
# @arg $1 path Skill directory (e.g. ~/.agents/skills/agmsg).
# @exitcode 1 On any failure, with the reason on stderr.
#
function install_pinned_agmsg() (
    local skill_dir="$1"
    local fetch_url="https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz"
    local tool tarball extract_dir actual before_state after_state before_run after_run changed install_log backup_dir state_dir installed
    local -a install_args=(--cmd agmsg --agent-type claude-code)

    for tool in curl tar; do
        command -v "${tool}" > /dev/null 2>&1 || {
            printf 'agmsg: %s not found; nothing was installed\n' "${tool}" >&2
            return 1
        }
    done
    before_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
        printf 'agmsg: could not snapshot the live state under %s; nothing was installed\n' "${skill_dir}" >&2
        return 1
    }
    before_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
    if [ -f "${skill_dir}/.agmsg" ]; then
        install_args=(--update "${install_args[@]}")
    fi

    tarball="$(mktemp)" || return 1
    extract_dir="$(mktemp -d)" || return 1
    install_log="$(mktemp)" || return 1
    trap 'rm -f "${tarball}" "${install_log}"; rm -rf "${extract_dir}"' EXIT
    curl -fsSL "${fetch_url}" -o "${tarball}" || {
        printf 'agmsg download failed: %s; nothing was installed\n' "${fetch_url}" >&2
        return 1
    }
    actual="$(agmsg_sha256 "${tarball}")" || return 1
    [ "${actual%% *}" = "${AGMSG_PIN_SHA256}" ] || {
        printf 'agmsg checksum mismatch for %s; nothing was installed\n' "${fetch_url}" >&2
        return 1
    }
    tar xzf "${tarball}" -C "${extract_dir}" --strip-components=1 || {
        printf 'agmsg extraction failed for %s; nothing was installed\n' "${fetch_url}" >&2
        return 1
    }

    if [ -d "${skill_dir}" ]; then
        backup_dir="${HOME}/.agents/backups/agmsg-state-$(date -u +%Y%m%dT%H%M%SZ)"
        mkdir -p "${backup_dir}" || return 1
        for state_dir in teams db run agents; do
            [ ! -e "${skill_dir}/${state_dir}" ] || cp -Rp "${skill_dir}/${state_dir}" "${backup_dir}/" || {
                printf 'agmsg: could not back up %s/%s; nothing was installed\n' "${skill_dir}" "${state_dir}" >&2
                return 1
            }
        done
        printf 'agmsg: live state copied to %s before install.sh %s\n' "${backup_dir}" "${install_args[*]}"
    fi
    if ! bash "${extract_dir}/install.sh" "${install_args[@]}" > "${install_log}" 2>&1; then
        cat "${install_log}" >&2
        printf 'agmsg: install.sh %s failed; the skill directory may be partially updated%s\n' \
            "${install_args[*]}" "${backup_dir:+; pre-install state copy: ${backup_dir}}" >&2
        return 1
    fi
    after_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
        printf 'agmsg: install.sh %s finished, but the live state could not be re-checked; pre-install state copy: %s\n' \
            "${install_args[*]}" "${backup_dir:-none}" >&2
        return 1
    }
    changed="$(LC_ALL=C comm -23 <(printf '%s\n' "${before_state}") <(printf '%s\n' "${after_state}") | sed 's/^[^ ]*  *//')"
    if [ -n "${changed}" ]; then
        printf 'agmsg: install.sh %s changed or removed existing live state (the installer or a concurrent writer); pre-install state copy: %s\n%s\n' \
            "${install_args[*]}" "${backup_dir:-none}" "${changed}" >&2
        return 1
    fi
    after_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
    [ "${before_run}" = "${after_run}" ] ||
        printf 'agmsg: note: run/ changed during install.sh %s (watchers and sync engines rewrite it); not treated as a failure\n' "${install_args[*]}"
    installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none')"
    if ! [ -f "${skill_dir}/.agmsg" ] || [ "${installed}" != "${AGMSG_PIN_VERSION}" ]; then
        printf 'agmsg: install.sh %s left VERSION %s (want %s)\n' "${install_args[*]}" "${installed}" "${AGMSG_PIN_VERSION}" >&2
        return 1
    fi
)

#
# @description Install or refresh the pinned upstream agmsg skill in place.
#
function update_agmsg() {
    local skill_dir="${HOME}/.agents/skills/agmsg"
    local installed

    section "agmsg"
    installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')"
    if [ "${installed}" != "${AGMSG_PIN_VERSION}" ] || ! [ -f "${skill_dir}/.agmsg" ] || ! [ -x "${skill_dir}/scripts/send.sh" ]; then
        install_pinned_agmsg "${skill_dir}" ||
            printf 'agmsg installer failed (installed: %s); see the reason above.\n' "${installed}" >&2
    fi

    manifest_record "update_agmsg" installer \
        "$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')" \
        "${skill_dir}/SKILL.md" "${skill_dir}/scripts" "${skill_dir}/VERSION" -- \
        "curl -fsSL https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz" \
        "sha256sum <tarball> (shasum -a 256 on macOS)" \
        "bash <extracted>/install.sh [--update when .agmsg exists] --cmd agmsg --agent-type claude-code"
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
    ensure_gh_extensions
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
    update_agmsg
    ensure_herdr_integrations
    # After every plugin update above, so the trust hashes follow the plugin content of this run.
    refresh_codex_hook_trust
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
