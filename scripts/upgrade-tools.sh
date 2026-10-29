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
#   (Homebrew, mise self-update, uv tools, unpinned gh extensions) only warn when they
#   fail, so an offline host still converges; installing the declared mise tools
#   stays required, while a per-tool upgrade that fails only warns. It edits no repository file, and exits 0 without changes
#   on a GitHub Actions runner (is_ci_runner from scripts/lib/ci-runner.sh); an agent shell's CI=true still updates.

set -Eeuo pipefail

# dirname is captured on its own line: inside the cd its status would be lost.
script_dir="$(dirname -- "${BASH_SOURCE[0]}")" || {
    echo "upgrade-tools: dirname failed on ${BASH_SOURCE[0]}; the repository root is unknown" >&2
    exit 1
}
repo_root="$(cd "${script_dir}/.." && pwd)" || exit 1
# shellcheck source=scripts/lib/ci-runner.sh
source "${script_dir}/lib/ci-runner.sh"
# shellcheck source=scripts/lib/npm-release-age.sh
source "${script_dir}/lib/npm-release-age.sh"
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
# @exitcode 1 Also exits the script when uname fails: a failed read is not "another OS".
#
function is_macos() {
    local kernel
    kernel="$(uname)" || {
        echo "uname failed; cannot tell whether this host is macOS" >&2
        exit 1
    }
    [ "${kernel}" = "Darwin" ]
}

#
# @description Return success when the current OS is Linux.
# @exitcode 1 Also exits the script when uname fails: a failed read is not "another OS".
#
function is_linux() {
    local kernel
    kernel="$(uname)" || {
        echo "uname failed; cannot tell whether this host is Linux" >&2
        exit 1
    }
    [ "${kernel}" = "Linux" ]
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
    local mise_dir
    local mise_prefix

    has_command mise || return 1
    mise_executable="$(type -P mise)" || return 1
    mise_dir="$(dirname -- "${mise_executable}")" || return
    mise_prefix="$(cd "${mise_dir}/.." && pwd -P)" || return

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
    local listing

    # Captured first: a failed `mise ls` is a failure of the inventory, never an empty one.
    listing="$(run_mise_with_isolated_git_config ls --current --no-header)" || return 1
    awk '{print $1}' <<< "${listing}"
}

#
# @description Print the tools the applied mise config holds, one per line: an entry whose comment block
#   directly above it says "Held" (home/dot_mise/config.toml keeps every hold reason there). The config is
#   the one source, so a hold released there leaves no skip behind here. scripts/pin_records.py reads it
#   strictly: the config must be valid TOML and every Held entry a tool.
# @exitcode 2 When the applied config cannot be read or a Held comment names no tool.
#
function held_mise_tools() {
    python3 -I "${repo_root}/scripts/pin_records.py" mise-holds "${MISE_CONFIG_DIR}/config.toml"
}

#
# @description Ask scripts/pin_records.py whether the applied mise config holds one tool.
# @arg $1 string mise tool name.
# @exitcode 0 Held.
# @exitcode 1 Not held.
# @exitcode 2 The config cannot be read or has an unknown shape: never read as "not held".
#
function mise_tool_is_held() {
    python3 -I "${repo_root}/scripts/pin_records.py" is-held "${MISE_CONFIG_DIR}/config.toml" "$1"
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
    local held
    local failed=0

    if ! mise_tools="$(current_mise_tools)"; then
        printf 'warning: unable to list current mise tools for %s; continuing\n' "${mise_command}" >&2
        return 1
    fi
    # Read once up front, so an unreadable config stops the phase before any tool moves.
    if ! held_mise_tools > /dev/null; then
        printf 'warning: unable to read the held tools from %s/config.toml; no mise tool was upgraded\n' "${MISE_CONFIG_DIR}" >&2
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
        held=0
        mise_tool_is_held "${mise_tool}" || held=$?
        if [ "${held}" -eq 0 ]; then
            printf 'Skipping mise upgrade for held tool: %s (see its Held comment in the mise config).\n' "${mise_tool}"
            continue
        elif [ "${held}" -ne 1 ]; then
            printf 'warning: cannot tell whether %s is held; no further mise tool was upgraded\n' "${mise_tool}" >&2
            return 1
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
# @description Report that one npm: tool keeps its previous install instead of being rebuilt on the current node.
# @arg $1 string mise npm tool name.
# @arg $2 string The reason.
# @stderr One skip line.
#
function npm_rebuild_skipped() {
    printf 'skip: %s is not rebuilt on the current node (%s); its previous install stays, and the next make update tries again\n' "$1" "$2" >&2
}

#
# @description Rebuild one npm: tool on the current node, keeping its working install until the new one succeeds.
#   mise install --force would delete the install before downloading its
#   replacement, so a rebuild without a network would leave the tool missing.
#   The rebuild reinstalls the exact version already installed, under npm's own min-release-age like every other
#   install: no package is exempt from it. npm refuses a version younger than that window (ETARGET), although the
#   host already runs it, so the rebuild first asks npm for the window and the version's publish time
#   (npm_release_age_verdict) and skips a version that is younger, or whose age it cannot tell, before anything
#   moves. An install npm still refuses (a dependency younger than the window) restores the previous install.
# @arg $1 string mise npm tool name, for example npm:ccusage.
# @stderr A skip line naming the reason when the tool is not rebuilt.
# @exitcode 1 When the tool was not rebuilt.
#
function rebuild_mise_npm_tool() {
    local mise_tool="$1"
    local version install_dir backup min_age times verdict

    version="$(run_mise_with_isolated_git_config current "${mise_tool}")" || {
        npm_rebuild_skipped "${mise_tool}" "mise cannot name its current version"
        return 1
    }
    install_dir="$(run_mise_with_isolated_git_config where "${mise_tool}")" || {
        npm_rebuild_skipped "${mise_tool}" "mise cannot name its install directory"
        return 1
    }
    # Only an existing absolute install directory is moved or removed.
    [[ -n "${version}" && "${install_dir}" == /* ]] || { # lint-comparisons: allow an absolute-path prefix test
        npm_rebuild_skipped "${mise_tool}" "no version or no absolute install directory"
        return 1
    }
    backup="${install_dir}.before-node-rebuild"
    # restore_interrupted_npm_rebuilds put any leftover backup back; never move an install into one.
    [[ -d "${install_dir}" && ! -e "${backup}" ]] || {
        npm_rebuild_skipped "${mise_tool}" "${install_dir} is missing or a backup of it exists"
        return 1
    }
    # Decided before anything moves, with the npm that mise's npm backend runs (the current node's).
    min_age="$(run_mise_with_isolated_git_config exec -- npm config get min-release-age)" || {
        npm_rebuild_skipped "${mise_tool}" "npm config get min-release-age failed"
        return 1
    }
    times="$(run_mise_with_isolated_git_config exec -- npm view --json "${mise_tool#npm:}" time)" || {
        npm_rebuild_skipped "${mise_tool}" "npm view cannot read the publish time of ${version}"
        return 1
    }
    local age_status=0
    verdict="$(npm_release_age_verdict "${version}" "${min_age}" <<< "${times}")" || age_status=$?
    if [ "${age_status}" -ne 0 ]; then
        npm_rebuild_skipped "${mise_tool}" "${verdict:-its release age cannot be told}"
        return 1
    fi
    mv "${install_dir}" "${backup}" || {
        npm_rebuild_skipped "${mise_tool}" "${install_dir} cannot be moved aside"
        return 1
    }
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
        mv "${backup}" "${discard}" || {
            printf 'warning: %s was rebuilt, but its previous install %s cannot be set aside\n' "${mise_tool}" "${backup}" >&2
            return 1
        }
        rm -rf "${discard}" || printf 'warning: could not delete %s; nothing uses it\n' "${discard}" >&2
        return 0
    fi
    trap - INT TERM EXIT
    restore_npm_install "${install_dir}" "${backup}" &&
        npm_rebuild_skipped "${mise_tool}" "npm refused or could not fetch ${mise_tool#npm:}@${version}, its error is above; a dependency younger than npm's min-release-age is still refused"
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
# @description Rebuild the current npm: tools so they run on the current node; each one not rebuilt says why.
# @exitcode 1 When the tools cannot be listed or at least one was not rebuilt.
#
function reinstall_mise_npm_tools() {
    local mise_tool
    local mise_tools
    local failed=0

    mise_tools="$(current_mise_tools)" || return 1
    while IFS= read -r mise_tool; do
        [[ "${mise_tool}" == npm:* ]] || continue
        rebuild_mise_npm_tool "${mise_tool}" || failed=1
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
# @description Print the manifest pin of an asset installed from a wheel (an assets.<name>.files URL ending in .whl), or nothing.
# @arg $1 string Asset name.
#
function manifest_wheel_pin() {
    # shortcut: reads the unquoted block style of home/dot_agents/agent-config.yaml line by line, not as YAML; use a parser if assets: gains quotes or flow style.
    awk -v name="$1" '
        /^[^ #]/ { in_assets = ($0 ~ /^assets:/) }
        in_assets && /^  [^ #]/ { asset = $1; sub(/:$/, "", asset) }
        in_assets && asset == name && /^    pin:/ { pin = $2 }
        in_assets && asset == name && /\.whl$/ { wheel = 1 }
        END { if (wheel) print pin }
    ' "${repo_root}/home/dot_agents/agent-config.yaml"
}

#
# @description Upgrade uv tool installations when uv is available, except the ones the manifest pins from a wheel.
#
function upgrade_uv_tools() {
    local tools tool pin failed=0
    has_command uv || return 1

    section "uv tools"
    # Plain text even where FORCE_COLOR or CLICOLOR_FORCE is set: uv colours tool names there.
    tools="$(uv tool list --color never)" || return
    # Tool lines read "<name> v<version>"; their entry points follow as "- <command>".
    for tool in $(printf '%s\n' "${tools}" | awk '/^[^- ]/ { print $1 }'); do
        pin="$(manifest_wheel_pin "${tool}")" || return
        if [ -n "${pin}" ]; then
            # uv's receipt names the local wheel, so an index upgrade has nothing to move; update-agent-assets.sh does.
            printf 'skip: %s (manifest pins %s from a wheel)\n' "${tool}" "${pin}"
        else
            uv tool upgrade "${tool}" || failed=1
        fi
    done
    return "${failed}"
}

#
# @description Upgrade the GitHub CLI extensions this repository does not pin, one by one, when gh is available.
# @description
#   An extension recorded in scripts/plugin-pins.json (assets.gh-extensions) stays at its reviewed tag:
#   install/common/gh_extensions.sh installs it with --pin, and no blanket `gh extension upgrade --all` runs.
# @exitcode 1 When the pins or the extension list cannot be read (nothing is upgraded), or an upgrade fails.
#
function upgrade_gh_extensions() {
    local listing repository pinned failed=0

    if ! has_command gh; then
        return 0
    fi

    section "GitHub CLI extensions"
    if ! listing="$(gh extension list)"; then
        printf 'warning: gh extension list failed; no extension was upgraded\n' >&2
        return 1
    fi
    while IFS=$'\t' read -r _ repository _; do
        [ -n "${repository}" ] || continue
        # pin_records.py answers exit 0 pinned, 1 not pinned; anything else (unreadable pins, a row that is not
        # <owner>/<name>) is a failure, and the extension is not upgraded.
        pinned=0
        python3 -I "${repo_root}/scripts/pin_records.py" is-pinned-extension "${repo_root}/scripts/plugin-pins.json" "${repository}" || pinned=$?
        if [ "${pinned}" -eq 0 ]; then
            printf 'Skipping gh extension %s: pinned in assets.gh-extensions.\n' "${repository}"
            continue
        elif [ "${pinned}" -ne 1 ]; then
            printf 'warning: cannot tell whether gh extension %s is pinned; it was not upgraded\n' "${repository}" >&2
            failed=1
            continue
        fi
        gh extension upgrade "${repository##*/}" || failed=1
    done <<< "${listing}"
    return "${failed}"
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
    if is_ci_runner; then
        printf 'GitHub Actions runner: skipping installed-tool updates.\n'
        return 0
    fi

    # Network-only phases warn and continue, so make update still converges offline.
    run_optional_phase "Homebrew" upgrade_homebrew
    run_optional_phase "mise self-update" upgrade_mise_self
    run_required_phase "mise inventory/install/upgrade" upgrade_mise_tools
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
