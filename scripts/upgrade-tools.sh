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
DEFAULT_FORBIDDEN_HOMEBREW_FORMULAE="node node@* python python@* python3 pip npm pnpm yarn claude"
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
# @description Run a required upgrade phase and record failure without stopping later phases.
# @arg $1 string Phase label.
# @arg $2 string Function name.
#
function run_required_phase() {
    local label="$1"
    shift

    if ! "$@"; then
        printf 'required failure: %s\n' "${label}" >&2
        ((required_failures += 1))
    fi
}

#
# @description Run an optional upgrade phase and record warning-only failure.
# @arg $1 string Phase label.
# @arg $2 string Function name.
#
function run_optional_phase() {
    local label="$1"
    shift

    if ! "$@"; then
        printf 'optional warning: %s failed\n' "${label}" >&2
        ((optional_warnings += 1))
    fi
}

#
# @description Return success when the named Homebrew formula is forbidden.
# @arg $1 string Formula name.
#
function is_forbidden_homebrew_formula() {
    local formula="$1"
    local forbidden_formula

    for forbidden_formula in ${DEFAULT_FORBIDDEN_HOMEBREW_FORMULAE} ${HOMEBREW_FORBIDDEN_FORMULAE:-}; do
        # shellcheck disable=SC2254 # Forbidden formula entries intentionally support glob patterns.
        case "${formula}" in
        ${forbidden_formula})
            return 0
            ;;
        esac
    done

    return 1
}

#
# @description Upgrade Homebrew packages on macOS when Homebrew is installed.
#
function upgrade_homebrew() {
    if ! is_macos; then
        return 0
    fi
    has_command brew || return 1

    section "Homebrew"
    brew update || return

    local outdated_formula
    local outdated_formulae_output
    local outdated_formulae=()
    local upgrade_formulae=()
    outdated_formulae_output="$(brew outdated --formula --quiet)" || return
    if [ -n "${outdated_formulae_output}" ]; then
        while IFS= read -r outdated_formula; do
            outdated_formulae+=("${outdated_formula}")
        done <<< "${outdated_formulae_output}"
    fi

    if [ "${#outdated_formulae[@]}" -gt 0 ]; then
        for outdated_formula in "${outdated_formulae[@]}"; do
            if is_forbidden_homebrew_formula "${outdated_formula}"; then
                printf 'Skipping forbidden Homebrew formula: %s\n' "${outdated_formula}"
                continue
            fi

            upgrade_formulae+=("${outdated_formula}")
        done
    fi

    if [ "${#upgrade_formulae[@]}" -gt 0 ]; then
        HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --formula "${upgrade_formulae[@]}" || return
    else
        printf 'No upgradeable Homebrew formulae after forbidden formula filtering.\n'
    fi

    local outdated_cask
    local outdated_casks_output
    local outdated_casks=()
    outdated_casks_output="$(brew outdated --cask --quiet)" || return
    if [ -n "${outdated_casks_output}" ]; then
        while IFS= read -r outdated_cask; do
            outdated_casks+=("${outdated_cask}")
        done <<< "${outdated_casks_output}"
    fi

    if [ "${#outdated_casks[@]}" -gt 0 ]; then
        HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --cask --skip-cask-deps "${outdated_casks[@]}" || return
    else
        printf 'No outdated Homebrew casks.\n'
    fi
}

#
# @description Upgrade standalone mise or skip package-manager-managed installations.
# @stdout Skip message when an official package-manager marker is present.
#
function upgrade_mise_self() {
    local mise_executable
    local mise_prefix

    has_command mise || return 1
    mise_executable="$(type -P mise)" || return 1
    mise_prefix="$(cd "$(dirname "${mise_executable}")/.." && pwd -P)" || return

    section "mise self-update"
    if [[ -f "${mise_prefix}/lib/mise-self-update-instructions.toml" ||
        -f "${mise_prefix}/lib/mise/mise-self-update-instructions.toml" ]]; then
        printf 'Skipping mise self-update: managed by package manager.\n'
        return 0
    fi

    mise self-update --yes
}

#
# @description Run mise while hiding user-level Git config from package backend operations.
# @arg $@ string Mise command and arguments.
#
function run_mise_with_isolated_git_config() {
    local isolated_xdg_config_home
    local mise_config_dir
    local status

    mise_config_dir="${MISE_CONFIG_DIR:-${XDG_CONFIG_HOME:-${HOME%/}/.config}/mise}"
    isolated_xdg_config_home="$(mktemp -d "${TMPDIR:-/tmp}/mise-git-config.XXXXXX")"
    GIT_CONFIG_NOSYSTEM=1 \
        GIT_CONFIG_GLOBAL=/dev/null \
        XDG_CONFIG_HOME="${isolated_xdg_config_home}" \
        MISE_CONFIG_DIR="${mise_config_dir}" \
        mise "$@"
    status="$?"
    rm -rf "${isolated_xdg_config_home}" 2> /dev/null || true
    return "${status}"
}

#
# @description Print mise tool names from the current configuration.
# @stdout One tool name per line.
#
function current_mise_tools() {
    run_mise_with_isolated_git_config ls --current --no-header | awk '{print $1}'
}

#
# @description Run a mise lifecycle command for each current tool.
# @arg $1 string Mise command name, such as install or upgrade.
#
function run_mise_tool_command() {
    local mise_command="$1"
    local mise_tool
    local mise_tools
    local failed=0

    if ! mise_tools="$(current_mise_tools)"; then
        printf 'warning: unable to list current mise tools for %s; continuing\n' "${mise_command}" >&2
        return 1
    fi

    while IFS= read -r mise_tool; do
        if [ -z "${mise_tool}" ]; then
            continue
        fi

        if [ "${mise_command}" = "upgrade" ]; then
            # ponytail: keep fd pinned until upstream publishes macOS x64 assets again.
            if [ "${mise_tool}" = "fd" ]; then
                printf 'Skipping mise upgrade for fd: newer releases lack a macOS x64 asset.\n'
                continue
            fi
            if ! MISE_LOCKED=0 run_mise_with_isolated_git_config upgrade --bump --yes --before 7d "${mise_tool}"; then
                printf 'warning: mise %s failed for %s; continuing\n' "${mise_command}" "${mise_tool}" >&2
                failed=1
            fi
        elif ! run_mise_with_isolated_git_config install --yes --before 7d "${mise_tool}"; then
            printf 'warning: mise %s failed for %s; continuing\n' "${mise_command}" "${mise_tool}" >&2
            failed=1
        fi
    done <<< "${mise_tools}"

    return "${failed}"
}

#
# @description Upgrade mise-managed tools declared in the repository config.
#
function upgrade_mise_tools() {
    has_command mise || return 1

    section "mise tools"
    local failed=0
    mise trust --yes || failed=1
    # Keep the npm safety window used by the bootstrap installer so freshly
    # published npm packages are not picked up immediately.
    run_mise_tool_command install || failed=1
    run_mise_tool_command upgrade || failed=1
    return "${failed}"
}

#
# @description Print the latest npm registry version for a package.
# @arg $1 string npm package name, for example @scope/package.
# @stdout npm package version.
#
function latest_npm_package_version() {
    npm view "$1" version
}

#
# @description Reinstall a mise-managed npm package version with lifecycle scripts enabled.
# @arg $1 string mise npm tool name, for example npm:@scope/package.
# @arg $2 string npm package name, for example @scope/package.
# @arg $3 string npm package version.
#
function repair_mise_npm_package() {
    local mise_tool="$1"
    local npm_package="$2"
    local package_version="$3"
    local install_prefix

    if ! install_prefix="$(mise where "${mise_tool}")"; then
        return 1
    fi
    npm_config_min_release_age=0 npm install -g \
        --prefix "${install_prefix}" \
        --ignore-scripts=false \
        --include=optional \
        "${npm_package}@${package_version}"
}

#
# @description Remove a node-global npm package so its dedicated mise npm tool is used.
# @arg $1 string npm package name, for example @scope/package.
#
function remove_node_global_npm_package() {
    local npm_package="$1"

    if ! has_command npm; then
        return 0
    fi

    if npm list -g "${npm_package}" --depth=0 > /dev/null 2>&1; then
        npm uninstall -g "${npm_package}"
    fi
}

#
# @description Install the exact current npm release into a dedicated mise npm tool.
# @arg $1 string mise npm tool name, for example npm:@scope/package.
# @arg $2 string npm package name, for example @scope/package.
#
function upgrade_mise_npm_agent_tool() {
    local mise_tool="$1"
    local npm_package="$2"
    local package_version
    local versioned_mise_tool

    if ! package_version="$(latest_npm_package_version "${npm_package}")"; then
        printf 'warning: unable to resolve latest npm version for %s; continuing\n' "${npm_package}" >&2
        return 1
    fi

    versioned_mise_tool="${mise_tool}@${package_version}"
    if ! MISE_LOCKED=0 npm_config_min_release_age=0 run_mise_with_isolated_git_config use --global --pin --yes --minimum-release-age 0s "${versioned_mise_tool}"; then
        printf 'warning: mise use failed for %s; continuing\n' "${versioned_mise_tool}" >&2
        return 1
    fi

    if ! repair_mise_npm_package "${versioned_mise_tool}" "${npm_package}" "${package_version}"; then
        printf 'warning: npm repair failed for %s@%s; continuing\n' "${npm_package}" "${package_version}" >&2
        return 1
    fi

    return 0
}

#
# @description Upgrade fast-moving agent CLIs managed by mise to the latest npm release.
#
function upgrade_agent_cli_tools() {
    has_command mise || return 1

    section "agent CLI tools"
    local failed=0
    if upgrade_mise_npm_agent_tool "npm:@openai/codex" "@openai/codex"; then
        remove_node_global_npm_package "@openai/codex" || failed=1
    else
        failed=1
    fi
    if upgrade_mise_npm_agent_tool "npm:@anthropic-ai/claude-code" "@anthropic-ai/claude-code"; then
        remove_node_global_npm_package "@anthropic-ai/claude-code" || failed=1
    else
        failed=1
    fi
    return "${failed}"
}

#
# @description Install or update CLI-managed Codex and Claude Code agent assets.
#
function upgrade_agent_assets() {
    local repo_root
    repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

    "${repo_root}/scripts/update-agent-assets.sh"
}

#
# @description Upgrade uv tool installations when uv is available.
#
function upgrade_uv_tools() {
    has_command uv || return 1

    section "uv tools"
    uv tool upgrade --all
}

#
# @description Upgrade GitHub CLI extensions when gh is available.
#
function upgrade_gh_extensions() {
    if ! has_command gh; then
        return 0
    fi

    section "GitHub CLI extensions"
    gh extension upgrade --all
}

#
# @description Upgrade apt packages only when system upgrades are requested.
#
function upgrade_apt_packages() {
    if ! ${include_system} || ! is_linux; then
        return 0
    fi
    has_command apt-get || return 1

    section "apt"
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update || return
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
        -h | --help)
            cat << 'USAGE'
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

    run_required_phase "Homebrew" upgrade_homebrew
    run_required_phase "mise self-update" upgrade_mise_self
    run_required_phase "mise inventory/install/upgrade" upgrade_mise_tools
    run_required_phase "Codex/Claude CLI upgrade" upgrade_agent_cli_tools
    run_required_phase "agent asset regeneration" upgrade_agent_assets
    run_required_phase "uv tool upgrade" upgrade_uv_tools
    run_optional_phase "GitHub CLI extension upgrade" upgrade_gh_extensions
    run_required_phase "apt system upgrade" upgrade_apt_packages

    printf '\nUpgrade summary: required failures: %d; optional warnings: %d\n' \
        "${required_failures}" "${optional_warnings}"
    [ "${required_failures}" -eq 0 ]
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
