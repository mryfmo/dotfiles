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
#   stays required, while a per-tool upgrade that fails only warns. It edits no repository file, and exits 0 without changes
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
    # A backup left by a run killed past its traps is the working install: put it back, never delete it.
    restore_npm_install "${install_dir}" "${backup}" || return 1
    [[ -d "${install_dir}" ]] || return 1
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
        rm -rf "${backup}"
        return 0
    fi
    trap - INT TERM EXIT
    restore_npm_install "${install_dir}" "${backup}"
    return 1
}

#
# @description Put a moved-aside npm: install back, replacing whatever a failed or interrupted install left.
# @arg $1 path The install directory.
# @arg $2 path The moved-aside working install.
#
function restore_npm_install() {
    [ -d "$2" ] || return 0
    rm -rf "$1"
    mv "$2" "$1"
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

# ponytail: dead until T119 deletes them with tests/unit/test_release_asset_pins.py; nothing calls these from main().
#
# @description Print the current manifest pin of one asset.
# @arg $1 string Asset name under assets: in home/dot_agents/agent-config.yaml.
# @arg $2 path Repository root.
# @stdout The pin value.
#
function asset_manifest_pin() {
    awk -v header="  $1:" '
        $0 == header { in_asset = 1; next }
        in_asset && /^  [^ ]/ { exit }
        in_asset && $1 == "pin:" { print $2; exit }
    ' "$2/home/dot_agents/agent-config.yaml" | grep .
}

#
# @description Print the newest version outside the supply-chain window that is newer than the current pin.
#   A release published within the last 7 days is skipped (the asset pins' own
#   window), and the pin never moves backwards.
# @arg $1 string Asset name, for log lines.
# @arg $2 string Current pin.
# @arg $3 number Window cutoff as Unix epoch seconds.
# @stdin Tab-separated `version<TAB>published-epoch` lines in any order.
# @stdout The chosen version, or the current pin when nothing qualifies.
# @stderr One line per release skipped by the window.
#
function pick_windowed_pin() {
    local asset="$1" current="$2" cutoff="$3"
    local version published eligible=()

    [ -n "${current}" ] || return 1
    while IFS=$'\t' read -r version published; do
        if [ -z "${version}" ] || [ "${version}" = "${current}" ]; then
            continue
        fi
        [ "$(printf '%s\n%s\n' "${current}" "${version}" | sort -V | tail -n 1)" = "${version}" ] || continue
        if [ "${published}" -le "${cutoff}" ]; then
            eligible+=("${version}")
        else
            printf 'release window: skipping %s %s (published %d day(s) ago, under 7)\n' \
                "${asset}" "${version}" "$(((cutoff + 604800 - published) / 86400))" >&2
        fi
    done
    if [ "${#eligible[@]}" -gt 0 ]; then
        printf '%s\n' "${eligible[@]}" | sort -V | tail -n 1
    else
        printf '%s\n' "${current}"
    fi
}

#
# @description Print published GitHub releases of one repository.
# @arg $1 string GitHub `owner/name`.
# @stdout Tab-separated `tag<TAB>published-epoch` lines.
#
function github_release_versions() {
    gh api "repos/$1/releases?per_page=30" \
        --jq '.[] | select((.draft or .prerelease) | not) | [.tag_name, (.published_at | fromdateiso8601)] | @tsv'
}

#
# @description Print non-yanked crates.io versions of one crate.
# @arg $1 string Crate name.
# @stdout Tab-separated `version<TAB>published-epoch` lines.
#
function crate_versions() {
    curl -fsSL -A 'mryfmo-dotfiles upgrade-tools (https://github.com/mryfmo/dotfiles)' \
        "https://crates.io/api/v1/crates/$1/versions" |
        python3 -c '
import datetime, json, sys
for v in json.load(sys.stdin)["versions"]:
    if not v["yanked"]:
        created = datetime.datetime.fromisoformat(v["created_at"].replace("Z", "+00:00"))
        print(v["num"], int(created.timestamp()), sep="\t")
'
}

#
# @description Print AWS CLI v2 versions newer than the current pin, newest first, with download dates.
#   AWS publishes v2 builds only as downloads, so the date is the Linux x86_64
#   archive's Last-Modified header. Stops after the first version outside the
#   window to keep HEAD requests few.
# @arg $1 string Current pin.
# @arg $2 number Window cutoff as Unix epoch seconds.
# @stdout Tab-separated `version<TAB>published-epoch` lines.
#
function aws_cli_versions() {
    local current="$1" cutoff="$2" version modified published

    while IFS= read -r version; do
        modified="$(curl -fsSI "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${version}.zip" |
            tr -d '\r' | sed -n 's/^[Ll]ast-[Mm]odified: //p')" || return 1
        published="$(python3 -c 'import email.utils, sys; print(int(email.utils.parsedate_to_datetime(sys.argv[1]).timestamp()))' "${modified}")" || return 1
        printf '%s\t%s\n' "${version}" "${published}"
        [ "${published}" -gt "${cutoff}" ] || return 0
    done < <(gh api "repos/aws/aws-cli/tags?per_page=100" --jq '.[].name' |
        grep -E '^2\.[0-9]+\.[0-9]+$' | sort -V -r | awk -v current="${current}" '$0 == current { exit } { print }')
}

#
# @description Bump the mise, sheldon, starship, aws-cli, and chezmoi-bootstrap asset pins outside the 7-day window.
#   Their verify contracts (release-shasums, cargo-locked, release-sha256, gpg
#   fingerprint) keep no per-version hash in the manifest, so only pins change.
#   Writes through scripts/generate-agent-configs.py --set-asset, which renders
#   each installer's version constant; review and commit that diff.
#
function bump_release_asset_pins() {
    local repo_root cutoff mise_pin sheldon_pin starship_pin aws_pin chezmoi_pin

    section "release asset pins"
    repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    cutoff=$((${UPGRADE_RELEASE_NOW:-$(date +%s)} - 604800))
    if ! mise_pin="$(github_release_versions jdx/mise |
        pick_windowed_pin mise "$(asset_manifest_pin mise "${repo_root}")" "${cutoff}")" ||
        ! sheldon_pin="$(crate_versions sheldon |
            pick_windowed_pin sheldon "$(asset_manifest_pin sheldon "${repo_root}")" "${cutoff}")" ||
        ! starship_pin="$(github_release_versions starship/starship |
            pick_windowed_pin starship "$(asset_manifest_pin starship "${repo_root}")" "${cutoff}")" ||
        ! aws_pin="$(aws_cli_versions "$(asset_manifest_pin aws-cli "${repo_root}")" "${cutoff}" |
            pick_windowed_pin aws-cli "$(asset_manifest_pin aws-cli "${repo_root}")" "${cutoff}")" ||
        # chezmoi tags carry a v prefix; setup.sh pins the bare version.
        ! chezmoi_pin="$(github_release_versions twpayne/chezmoi | sed 's/^v//' |
            pick_windowed_pin chezmoi-bootstrap "$(asset_manifest_pin chezmoi-bootstrap "${repo_root}")" "${cutoff}")"; then
        printf 'warning: unable to resolve release asset pins; keeping current pins\n' >&2
        return 1
    fi

    if ! (cd "${repo_root}" && uv run --with pyyaml scripts/generate-agent-configs.py \
        --set-asset "mise.pin=${mise_pin}" \
        --set-asset "sheldon.pin=${sheldon_pin}" \
        --set-asset "starship.pin=${starship_pin}" \
        --set-asset "aws-cli.pin=${aws_pin}" \
        --set-asset "chezmoi-bootstrap.pin=${chezmoi_pin}"); then
        printf 'warning: unable to write the asset manifest pins; keeping current pins\n' >&2
        return 1
    fi
    printf 'Pinned mise %s, sheldon %s, starship %s, aws-cli %s, and chezmoi %s; review and commit the assets and installer diff.\n' \
        "${mise_pin}" "${sheldon_pin}" "${starship_pin}" "${aws_pin}" "${chezmoi_pin}"
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
