#!/usr/bin/env bash

# @file scripts/upgrade-tools.sh
# @brief Update installed tools to the latest safe versions; `make update` runs it after `chezmoi apply`.
# @description
#   Each manager's own safety features decide what the latest safe version is:
#   mise's minimum_release_age and verification settings in the applied
#   ~/.config/mise/config.toml, and a manager's own hold (an exact version in
#   that config, brew pin, uv tool install <pkg>==<version>, apt-mark hold).
#   The default mode updates user-level tooling and Homebrew-managed packages
#   when those managers are available. Pass `--system` to include
#   operating-system package upgrades such as apt. The network-only phases
#   (Homebrew, mise self-update, uv tools, gh extensions) only warn when they
#   fail, so an offline host still converges; installing the declared mise tools
#   stays required, while a per-tool upgrade that fails only warns. After the mise
#   phase, every npm: tool's registry signature and provenance attestation are
#   checked at its installed version, and a failed check is required. It edits no repository file, and exits 0 without changes
#   when CI=true.

set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# chezmoi applies home/dot_config/mise/config.toml.tmpl to ~/.config/mise whatever XDG_CONFIG_HOME
# says, so mise reads exactly that config: no inherited MISE_CONFIG_DIR, and the isolated Git
# config's XDG_CONFIG_HOME below cannot redirect it.
export MISE_CONFIG_DIR="${HOME}/.config/mise"
# No project config from this checkout upward joins the inventory, so only the host config's tools move.
export MISE_CEILING_PATHS="${repo_root}"

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
    if has_command gh; then
        # Homebrew verifies bottle build-provenance attestations through gh (HOMEBREW_VERIFY_ATTESTATIONS).
        local -x HOMEBREW_VERIFY_ATTESTATIONS=1
    else
        printf 'gh not found; Homebrew bottle attestation verification is skipped.\n'
    fi
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
        # Homebrew asks for confirmation by default (brew upgrade --help); make update must not wait.
        HOMEBREW_NO_ASK=1 HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --formula "${upgrade_formulae[@]}" || return
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
        HOMEBREW_NO_ASK=1 HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1 brew upgrade --cask --skip-cask-deps "${outdated_casks[@]}" || return
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

    # Plugin updates are branch moves the release-age cooldown does not cover.
    mise self-update --yes --no-plugins
}

#
# @description Run mise while hiding user-level Git config from package backend operations.
# @arg $@ string Mise command and arguments.
#
function run_mise_with_isolated_git_config() {
    local isolated_xdg_config_home
    local mise_config_dir
    local status

    mise_config_dir="${MISE_CONFIG_DIR}"
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
# @description Run a mise lifecycle command for each current tool; only upgrade is per tool.
# @arg $1 string Mise command name: upgrade.
# @exitcode 1 When the current tools cannot be listed.
# @exitcode 2 When the command failed for at least one tool.
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

        if [[ "${mise_tool}" == http:* ]]; then
            printf 'Skipping mise upgrade for pinned HTTP tool: %s.\n' "${mise_tool}"
            continue
        fi
        # ponytail: keep fd pinned until upstream publishes macOS x64 assets again.
        if [ "${mise_tool}" = "fd" ]; then
            printf 'Skipping mise upgrade for fd: newer releases lack a macOS x64 asset.\n'
            continue
        fi
        # A plain upgrade keeps the config's "latest" or exact request as written.
        if ! run_mise_with_isolated_git_config upgrade --yes "${mise_tool}"; then
            printf 'warning: mise %s failed for %s; continuing\n' "${mise_command}" "${mise_tool}" >&2
            failed=2
        fi
    done <<< "${mise_tools}"

    return "${failed}"
}

#
# @description Rebuild one npm: tool on the current node, keeping its working install until the new one succeeds.
#   mise install --force would delete the install before downloading its
#   replacement, so a rebuild without a network would leave the tool missing.
# @arg $1 string mise npm tool name, for example npm:ccusage.
#
function rebuild_mise_npm_tool() {
    local mise_tool="$1"
    local version install_dir backup

    version="$(run_mise_with_isolated_git_config current "${mise_tool}")" || return 1
    install_dir="$(run_mise_with_isolated_git_config where "${mise_tool}")" || return 1
    # Only an existing absolute install directory is moved or removed.
    [[ -n "${version}" && "${install_dir}" == /* ]] || return 1
    backup="${install_dir}.before-node-rebuild"
    # restore_interrupted_npm_rebuilds put any leftover backup back; never move an install into one.
    [[ -d "${install_dir}" && ! -e "${backup}" ]] || return 1
    mv "${install_dir}" "${backup}" || return 1
    # Until the new install succeeds, an interruption or exit puts the working install back.
    local restore
    restore="$(printf 'restore_npm_install %q %q' "${install_dir}" "${backup}")"
    # shellcheck disable=SC2064 # Expanded now on purpose: the paths are this function's locals.
    trap "${restore}; exit 130" INT
    # shellcheck disable=SC2064
    trap "${restore}; exit 143" TERM
    # shellcheck disable=SC2064
    trap "${restore}" EXIT
    if run_mise_with_isolated_git_config install --yes "${mise_tool}@${version}"; then
        trap - INT TERM EXIT
        # Renamed before it is deleted, so a backup that cannot be fully deleted is never restored over this
        # install; the dot keeps a leftover out of mise's installed versions.
        local discard="${install_dir%/*}/.${install_dir##*/}.discarded-after-rebuild"
        rm -rf "${discard}"
        mv "${backup}" "${discard}" || return 1
        rm -rf "${discard}" || printf 'warning: could not delete %s; nothing uses it\n' "${discard}" >&2
        return 0
    fi
    trap - INT TERM EXIT
    restore_npm_install "${install_dir}" "${backup}"
    return 1
}

#
# @description Put back every npm: install that a rebuild killed past its traps (SIGKILL, power loss) left
#   moved aside. It runs before any mise command, because mise cannot name an install that is not in place.
#
function restore_interrupted_npm_rebuilds() {
    local backup
    local failed=0
    # mise's own installs directory resolution: MISE_INSTALLS_DIR, then the data directory (MISE_DATA_DIR, then XDG_DATA_HOME).
    local installs="${MISE_INSTALLS_DIR:-${MISE_DATA_DIR:-${XDG_DATA_HOME:-${HOME}/.local/share}/mise}/installs}"
    for backup in "${installs}"/*/*.before-node-rebuild; do
        [ -d "${backup}" ] || continue
        restore_npm_install "${backup%.before-node-rebuild}" "${backup}" || failed=1
    done
    return "${failed}"
}

#
# @description Put a moved-aside npm: install back, replacing whatever a failed or interrupted install left.
# @arg $1 path The install directory.
# @arg $2 path The moved-aside working install.
#
function restore_npm_install() {
    [ -d "$2" ] || return 0
    # The backup moves only onto a path that is gone, so it is never buried inside a partial install that survives.
    if rm -rf "$1" && [ ! -e "$1" ] && mv "$2" "$1"; then
        return 0
    fi
    printf 'required failure: could not restore %s from %s\n' "$1" "$2" >&2
    ((required_failures += 1))
    return 1
}

#
# @description Rebuild the current npm: tools so they run on the current node.
#
function reinstall_mise_npm_tools() {
    local mise_tool
    local mise_tools
    local failed=0

    mise_tools="$(current_mise_tools)" || return 1
    while IFS= read -r mise_tool; do
        [[ "${mise_tool}" == npm:* ]] || continue
        if ! rebuild_mise_npm_tool "${mise_tool}"; then
            printf 'warning: rebuilding %s on the current node failed; its previous install stays; continuing\n' "${mise_tool}" >&2
            failed=1
        fi
    done <<< "${mise_tools}"

    return "${failed}"
}

#
# @description Install missing and upgrade outdated mise tools declared in the applied host config.
#
function upgrade_mise_tools() {
    has_command mise || return 1

    section "mise tools"
    local failed=0
    restore_interrupted_npm_rebuilds || failed=1
    mise trust --yes || failed=1
    # minimum_release_age in the config keeps freshly published releases out of both steps.
    # One bare install: it leaves installed tools alone offline, while a per-tool
    # install re-resolves "latest" over the network and fails without one.
    run_mise_with_isolated_git_config install --yes || failed=1
    # Upgrades need the network; an installed tool that cannot move yet is still converged.
    local upgrade_status=0
    run_mise_tool_command upgrade || upgrade_status=$?
    if [ "${upgrade_status}" -eq 2 ]; then
        printf 'optional warning: mise upgrade failed for at least one tool; its installed version stays\n' >&2
        ((optional_warnings += 1))
    elif [ "${upgrade_status}" -ne 0 ]; then
        failed=1
    fi
    # Neither the bare install nor the upgrades rebuild installed npm: tools, and node can also have moved
    # in an earlier run or under the installer, so a marker records the node they were last built on.
    local marker="${XDG_STATE_HOME:-${HOME}/.local/state}/dotfiles/npm-tools-node"
    local node_built="" node_now="" reinstalled=0
    if [ -r "${marker}" ]; then
        node_built="$(cat "${marker}")"
    fi
    node_now="$(run_mise_with_isolated_git_config current node 2> /dev/null)" || node_now=""
    if [ -n "${node_now}" ] && [ "${node_now}" != "${node_built}" ]; then
        if reinstall_mise_npm_tools; then
            reinstalled=1
        else
            printf 'optional warning: npm: tools were not all reinstalled on node %s\n' "${node_now}" >&2
            ((optional_warnings += 1))
        fi
        # A rebuild keeps or restores the previous install, so this final bare install only has to confirm
        # that every declared tool is present; it decides whether the phase converged.
        if ! run_mise_with_isolated_git_config install --yes; then
            failed=1
        elif [ "${reinstalled}" -eq 1 ]; then
            # Only a complete rebuild is recorded, so a failed one is retried by the next run.
            if ! { mkdir -p "$(dirname "${marker}")" && printf '%s\n' "${node_now}" > "${marker}"; }; then
                printf 'required: could not record the npm-tools node in %s\n' "${marker}" >&2
                failed=1
            fi
        fi
    fi
    return "${failed}"
}

#
# @description Check one npm: tool at a version with npm audit signatures --include-attestations, in a
#   scratch install with lifecycle scripts off. npm checks the registry signature, and a provenance
#   attestation where one is published, over the integrity hash it verified at download; it does not
#   re-hash the files on disk, so this proves the version came from a signed, attested publish.
# @arg $1 string mise tool name, for example npm:@openai/codex.
# @arg $2 string The installed version.
# @arg $3 path A scratch directory for this tool.
# @arg $4 string Non-empty for a tool outside the cooldown, whose install lifted npm's window.
# @exitcode 0 The registry signature and the provenance attestation verified.
# @exitcode 1 A signature or an attestation failed to verify.
# @exitcode 3 The tool could not be fetched or checked, so nothing was verified.
# @exitcode 4 The registry signature verified; the package publishes no attestation.
#
function check_npm_tool_provenance() {
    local mise_tool="$1" version="$2" dir="$3" day_one="$4" output status=0 window=""

    { mkdir -p "${dir}" && printf '{"private":true}\n' > "${dir}/package.json"; } || return 3
    # A tool outside mise's cooldown installs with npm's window lifted (its install_env in the mise
    # config), so its scratch copy is fetched the same way; every other tool keeps ~/.npmrc's window.
    [ -z "${day_one}" ] || window="--min-release-age=0"
    (cd "${dir}" && npm_config_cache="${dir%/*}/cache" mise exec node -- npm install --ignore-scripts --no-audit --no-fund \
        ${window:+"${window}"} "${mise_tool#npm:}@${version}") > /dev/null 2>&1 || return 3
    output="$(cd "${dir}" && npm_config_cache="${dir%/*}/cache" \
        mise exec node -- npm audit signatures --include-attestations 2>&1)" || status=$?
    if grep -qiE 'invalid|missing' <<< "${output}"; then
        printf '%s\n' "${output}" >&2
        return 1
    fi
    if [ "${status}" -ne 0 ]; then
        printf '%s\n' "${output}" >&2
        grep -qE 'npm (ERR!|error) (network|code (ENOTFOUND|ECONNREFUSED|ECONNRESET|ETIMEDOUT|EAI_AGAIN))' <<< "${output}" && return 3
        return 1
    fi
    # npm prints a count line only for a non-zero count.
    grep -qE '^[[:space:]]*[1-9][0-9]* packages? ha(s a|ve) verified registry signatures?$' <<< "${output}" || return 3
    grep -qE '^[[:space:]]*[1-9][0-9]* packages? ha(s a|ve) verified attestations?$' <<< "${output}" || return 4
}

#
# @description Verify every current npm: tool's registry signature and provenance attestation. For a
#   tool behind the cooldown, a failed check is a required failure that names the package and removes
#   that version, a package without an attestation is listed as signature-only, and a tool that cannot
#   be fetched only warns.
#   A tool outside the cooldown (minimum_release_age_excludes) stays installed only with a verified
#   attestation, now or from an earlier run of the same version; any other outcome, a check that
#   cannot run included, is a required failure that removes that version.
#
function verify_npm_provenance() {
    local day_one excludes failed=0 index=0 marker mise_tool mise_tools scratch signature_only="" status version
    local state="${XDG_STATE_HOME:-${HOME}/.local/state}/dotfiles/npm-provenance"

    has_command mise || return 1
    mise_tools="$(current_mise_tools)" || return 1
    grep -q '^npm:' <<< "${mise_tools}" || return 0
    section "npm provenance"
    excludes="$(run_mise_with_isolated_git_config settings get minimum_release_age_excludes 2> /dev/null)" || excludes=""
    scratch="$(mktemp -d "${TMPDIR:-/tmp}/npm-provenance.XXXXXX")" || return 1
    while IFS= read -r mise_tool; do
        [[ "${mise_tool}" == npm:* ]] || continue
        index=$((index + 1))
        day_one=""
        case "${excludes}" in
        *"\"${mise_tool}\""*) day_one=1 ;;
        esac
        version="$(run_mise_with_isolated_git_config current "${mise_tool}" 2> /dev/null)" || version=""
        status=3
        if [ -n "${version}" ]; then
            status=0
            check_npm_tool_provenance "${mise_tool}" "${version}" "${scratch}/${index}" "${day_one}" || status=$?
        fi
        if [ -n "${day_one}" ]; then
            marker="${state}/${mise_tool//[^A-Za-z0-9._-]/_}"
            if [ "${status}" -eq 0 ]; then
                { mkdir -p "${state}" && printf '%s\n' "${version}" > "${marker}"; } ||
                    printf 'warning: could not record the verified %s in %s\n' "${mise_tool}" "${marker}" >&2
            elif [ "${status}" -eq 3 ] && [ -n "${version}" ] && [ "$(cat "${marker}" 2> /dev/null)" = "${version}" ]; then
                printf 'optional warning: could not re-check %s %s; an earlier run verified its provenance\n' "${mise_tool}" "${version}" >&2
                ((optional_warnings += 1))
                continue
            else
                # A release that skipped the cooldown without verified provenance, now or in an earlier run,
                # must not stay runnable, whether its check failed or could not run.
                rm -f "${marker}"
                if [ -z "${version}" ]; then
                    printf 'npm provenance check failed: %s skips the cooldown and is not installed\n' "${mise_tool}" >&2
                else
                    printf 'npm provenance check failed: %s %s skips the cooldown without a verified provenance attestation; removing it\n' "${mise_tool}" "${version}" >&2
                    run_mise_with_isolated_git_config uninstall "${mise_tool}@${version}" ||
                        printf 'required: could not remove %s %s; remove it with mise uninstall %s@%s\n' "${mise_tool}" "${version}" "${mise_tool}" "${version}" >&2
                fi
                failed=1
                continue
            fi
        fi
        case "${status}" in
        0) printf 'verified: %s (registry signature and provenance attestation)\n' "${mise_tool}" ;;
        4) signature_only+=" ${mise_tool}" ;;
        3)
            printf 'optional warning: could not fetch %s to check its provenance\n' "${mise_tool}" >&2
            ((optional_warnings += 1))
            ;;
        *)
            # An invalid signature or attestation means tampering, so that version must not stay runnable.
            printf 'npm provenance check failed: %s %s has an invalid or missing registry signature or attestation; removing it\n' "${mise_tool}" "${version}" >&2
            run_mise_with_isolated_git_config uninstall "${mise_tool}@${version}" ||
                printf 'required: could not remove %s %s; remove it with mise uninstall %s@%s\n' "${mise_tool}" "${version}" "${mise_tool}" "${version}" >&2
            failed=1
            ;;
        esac
    done <<< "${mise_tools}"
    rm -rf "${scratch}"
    if [ -n "${signature_only}" ]; then
        printf 'registry signature only (the publisher attaches no provenance attestation):%s\n' "${signature_only}"
    fi
    return "${failed}"
}

#
# @description Upgrade uv tool installations when uv is available. Python CLIs come through mise
#   pipx: (README), so this only moves uv tools a machine already has and prints nothing without any.
#
function upgrade_uv_tools() {
    has_command uv || return 1
    case "$(uv tool list 2> /dev/null)" in
    "" | "No tools installed"*) return 0 ;;
    esac

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

Update installed tools to the latest safe versions; make update runs it.

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
# @description Update installed tools through each manager.
# @arg $@ string Command-line arguments.
#
function main() {
    parse_args "$@"
    # A CI runner's tools belong to its image, not to this machine's update.
    if [ "${CI:-false}" = true ]; then
        printf 'CI=true: skipping installed-tool updates.\n'
        return 0
    fi

    # Network-only phases warn and continue, so make update still converges offline.
    run_optional_phase "Homebrew" upgrade_homebrew
    run_optional_phase "mise self-update" upgrade_mise_self
    run_required_phase "mise inventory/install/upgrade" upgrade_mise_tools
    run_required_phase "npm provenance" verify_npm_provenance
    run_optional_phase "uv tool upgrade" upgrade_uv_tools
    run_optional_phase "GitHub CLI extension upgrade" upgrade_gh_extensions
    run_required_phase "apt system upgrade" upgrade_apt_packages

    printf '\nUpgrade summary: required failures: %d; optional warnings: %d\n' \
        "${required_failures}" "${optional_warnings}"
    [ "${required_failures}" -eq 0 ]
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
