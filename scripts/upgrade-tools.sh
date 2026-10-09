#!/usr/bin/env bash

# @file scripts/upgrade-tools.sh
# @brief Explicitly upgrade tools managed outside normal `chezmoi apply`.
# @description
#   Keeps the bootstrap path stable by moving package-manager upgrades into an
#   intentional lifecycle command. The default mode upgrades user-level tooling
#   and Homebrew-managed packages when those managers are available. Pass
#   `--system` to include operating-system package upgrades such as apt.
#   Upgrades edit this checkout's home/dot_mise; ~/.config/mise is an applied copy.
#   It refuses the canonical chezmoi clone and a checkout that is dirty or not at origin/main.

set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export MISE_CONFIG_DIR="${MISE_CONFIG_DIR:-${repo_root}/home/dot_mise}"
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
    local mise_pin

    has_command mise || return 1
    mise_executable="$(type -P mise)" || return 1
    mise_prefix="$(cd "$(dirname "${mise_executable}")/.." && pwd -P)" || return

    section "mise self-update"
    if [[ -f "${mise_prefix}/lib/mise-self-update-instructions.toml" ||
        -f "${mise_prefix}/lib/mise/mise-self-update-instructions.toml" ]]; then
        printf 'Skipping mise self-update: managed by package manager.\n'
        return 0
    fi

    mise_pin="$(asset_manifest_pin mise "${repo_root}")" || return 1
    # mise prepends "v" to VERSION itself (src/cli/self_update.rs), so pass the bare pin.
    mise self-update --yes "${mise_pin#v}"
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
            if [[ "${mise_tool}" == http:* ]]; then
                printf 'Skipping mise upgrade for pinned HTTP tool: %s.\n' "${mise_tool}"
                continue
            fi
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
# @description Print the latest npm registry version with the current mise-managed Node runtime.
# @arg $1 string npm package name, for example @scope/package.
# @stdout npm package version.
#
function latest_npm_package_version() {
    mise exec node -- npm view "$1" version
}

#
# @description Reinstall a mise-managed npm package with the current mise-managed Node runtime and scripts denied by default.
# @arg $1 string mise npm tool name, for example npm:@scope/package.
# @arg $2 string npm package name, for example @scope/package.
# @arg $3 string npm package version.
#
function repair_mise_npm_package() {
    local mise_tool="$1"
    local npm_package="$2"
    local package_version="$3"
    local install_prefix
    local npm_script_args=(--ignore-scripts)

    if ! install_prefix="$(mise where "${mise_tool}")"; then
        return 1
    fi
    if [ "${npm_package}" = "@anthropic-ai/claude-code" ]; then
        npm_script_args=(--ignore-scripts=false --allow-scripts="@anthropic-ai/claude-code")
    fi
    npm_config_min_release_age=0 mise exec node -- npm install -g \
        --prefix "${install_prefix}" \
        "${npm_script_args[@]}" \
        --include=optional \
        "${npm_package}@${package_version}"
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
    if ! upgrade_mise_npm_agent_tool "npm:@openai/codex" "@openai/codex"; then
        failed=1
    fi
    if ! upgrade_mise_npm_agent_tool "npm:@anthropic-ai/claude-code" "@anthropic-ai/claude-code"; then
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
# @description Print the VERSION and script SHA256 of one upstream installer.
# @arg $1 string Installer URL.
# @stdout Two lines: the baked-in VERSION value, then the script SHA256.
#
function fetch_installer_pin() {
    local url="$1"
    local installer version

    installer="$(mktemp)"
    # shellcheck disable=SC2064 # Expand the temp path now; it never changes.
    trap "rm -f '${installer}'" RETURN
    curl -fsSL "${url}" -o "${installer}" || return 1
    version="$(sed -n 's/^VERSION="\(.*\)"$/\1/p' "${installer}" | head -n 1)"
    # The value is upstream-controlled and later written into a sourced shell
    # file; reject anything that is not a plausible version tag so a malicious
    # VERSION line cannot inject executable shell into the rendered pins.
    [[ "${version}" =~ ^[A-Za-z0-9._+-]+$ ]] || return 1
    printf '%s\n' "${version}"
    shasum -a 256 "${installer}" | awk '{ print $1 }'
}

#
# @description Print the latest Crit tag and SHA256 values for Linux and macOS release binaries.
# @stdout Five lines: release tag, then SHA256 for linux-amd64, linux-arm64, darwin-amd64, darwin-arm64.
#
function fetch_crit_pin() {
    local linux_amd64 linux_arm64 darwin_amd64 darwin_arm64 tag

    has_command gh || return 1
    tag="$(gh api repos/tomasz-tomczyk/crit/releases/latest --jq .tag_name)" || return 1
    [[ "${tag}" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || return 1
    linux_amd64="$(mktemp)"
    linux_arm64="$(mktemp)"
    darwin_amd64="$(mktemp)"
    darwin_arm64="$(mktemp)"
    trap 'rm -f "${linux_amd64}" "${linux_arm64}" "${darwin_amd64}" "${darwin_arm64}"' RETURN
    curl -fsSL "https://github.com/tomasz-tomczyk/crit/releases/download/${tag}/crit-linux-amd64" -o "${linux_amd64}" || return 1
    curl -fsSL "https://github.com/tomasz-tomczyk/crit/releases/download/${tag}/crit-linux-arm64" -o "${linux_arm64}" || return 1
    curl -fsSL "https://github.com/tomasz-tomczyk/crit/releases/download/${tag}/crit-darwin-amd64" -o "${darwin_amd64}" || return 1
    curl -fsSL "https://github.com/tomasz-tomczyk/crit/releases/download/${tag}/crit-darwin-arm64" -o "${darwin_arm64}" || return 1
    printf '%s\n' "${tag}"
    shasum -a 256 "${linux_amd64}" | awk '{ print $1 }'
    shasum -a 256 "${linux_arm64}" | awk '{ print $1 }'
    shasum -a 256 "${darwin_amd64}" | awk '{ print $1 }'
    shasum -a 256 "${darwin_arm64}" | awk '{ print $1 }'
}

#
# @description Print the latest Zed tag and SHA256 values for both Linux release tarballs.
# @stdout Three lines: release tag, amd64 SHA256, then arm64 SHA256.
#
function fetch_zed_pin() {
    local amd64 arm64 tag

    has_command gh || return 1
    tag="$(gh api repos/zed-industries/zed/releases/latest --jq .tag_name)" || return 1
    [[ "${tag}" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || return 1
    amd64="$(mktemp)"
    arm64="$(mktemp)"
    trap 'rm -f "${amd64}" "${arm64}"' RETURN
    curl -fsSL "https://github.com/zed-industries/zed/releases/download/${tag}/zed-linux-x86_64.tar.gz" -o "${amd64}" || return 1
    curl -fsSL "https://github.com/zed-industries/zed/releases/download/${tag}/zed-linux-aarch64.tar.gz" -o "${arm64}" || return 1
    printf '%s\n' "${tag}"
    shasum -a 256 "${amd64}" | awk '{ print $1 }'
    shasum -a 256 "${arm64}" | awk '{ print $1 }'
}

#
# @description Bump terminal tool installers, Crit, and Zed binaries to the latest upstream releases.
# @description
#   Writes the fetched pins and SHA256 values into assets: in
#   home/dot_agents/agent-config.yaml through scripts/generate-agent-configs.py,
#   which then renders scripts/lib/installer-pins.sh. Review and commit the
#   manifest and rendered diff like a mise config/lock bump. The subsequent
#   agent asset regeneration phase installs the newly pinned versions.
#
function bump_terminal_tool_pins() {
    local repo_root tode_pin tb_pin crit_pin zed_pin

    section "terminal tool pins"
    repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    tode_pin="$(fetch_installer_pin "https://tode.sh/install")" || {
        printf 'warning: unable to fetch the tode installer pin; keeping current pins\n' >&2
        return 1
    }
    tb_pin="$(fetch_installer_pin "https://terminal-browser.sh/install")" || {
        printf 'warning: unable to fetch the terminal-browser installer pin; keeping current pins\n' >&2
        return 1
    }
    crit_pin="$(fetch_crit_pin)" || {
        printf 'warning: unable to fetch the Crit release pins; keeping current pins\n' >&2
        return 1
    }
    zed_pin="$(fetch_zed_pin)" || {
        printf 'warning: unable to fetch the Zed release pins; keeping current pins\n' >&2
        return 1
    }

    if ! (cd "${repo_root}" && uv run --with pyyaml scripts/generate-agent-configs.py \
        --set-asset "tode.pin=$(sed -n 1p <<< "${tode_pin}")" \
        --set-asset "tode.sha256=$(sed -n 2p <<< "${tode_pin}")" \
        --set-asset "terminal-browser.pin=$(sed -n 1p <<< "${tb_pin}")" \
        --set-asset "terminal-browser.sha256=$(sed -n 2p <<< "${tb_pin}")" \
        --set-asset "crit.pin=$(sed -n 1p <<< "${crit_pin}")" \
        --set-asset "crit.sha256.linux-amd64=$(sed -n 2p <<< "${crit_pin}")" \
        --set-asset "crit.sha256.linux-arm64=$(sed -n 3p <<< "${crit_pin}")" \
        --set-asset "crit.sha256.darwin-amd64=$(sed -n 4p <<< "${crit_pin}")" \
        --set-asset "crit.sha256.darwin-arm64=$(sed -n 5p <<< "${crit_pin}")" \
        --set-asset "zed.pin=$(sed -n 1p <<< "${zed_pin}")" \
        --set-asset "zed.sha256.linux-amd64=$(sed -n 2p <<< "${zed_pin}")" \
        --set-asset "zed.sha256.linux-arm64=$(sed -n 3p <<< "${zed_pin}")"); then
        printf 'warning: unable to write the asset manifest pins; keeping current pins\n' >&2
        return 1
    fi
    printf 'Pinned tode %s, terminal-browser %s, crit %s, and zed %s; review and commit the assets and installer-pins diff.\n' \
        "$(sed -n 1p <<< "${tode_pin}")" "$(sed -n 1p <<< "${tb_pin}")" "$(sed -n 1p <<< "${crit_pin}")" "$(sed -n 1p <<< "${zed_pin}")"
}

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
#   Mirrors the mise tools path (`mise ... --before 7d`): a release published
#   within the last 7 days is skipped, and the pin never moves backwards.
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
# @description Refuse the canonical chezmoi clone, and any git checkout that is dirty or not at origin/main.
#   The pins diff must be produced where it is committed, so the canonical clone
#   stays pull/apply only. CHEZMOI_ALLOW_UPGRADE_IN_SOURCE=1 skips both checks.
# @exitcode 2 When the checkout is refused.
#
function require_pins_checkout() {
    local source_path source_root top head upstream

    if [ "${CHEZMOI_ALLOW_UPGRADE_IN_SOURCE:-0}" = 1 ]; then
        return 0
    fi
    if source_path="$(chezmoi source-path 2> /dev/null)" &&
        source_root="$(git -C "${source_path}" rev-parse --show-toplevel 2> /dev/null)" &&
        [ "$(cd "${source_root}" && pwd -P)" = "$(cd "${repo_root}" && pwd -P)" ]; then
        printf 'make upgrade refused: %s is the canonical chezmoi clone, which stays pull/apply only; run it in a pins worktree of the working clone (herdr-agents --add-worker .claude/worktrees/pins, then make -C <working clone>/.claude/worktrees/pins upgrade) and land the diff through a pull request\n' "${repo_root}" >&2
        exit 2
    fi

    # Only the checkout whose top level is repo_root, never an unrelated enclosing repository.
    top="$(git -C "${repo_root}" rev-parse --show-toplevel 2> /dev/null)" || return 0
    [ "$(cd "${top}" && pwd -P)" = "$(cd "${repo_root}" && pwd -P)" ] || return 0
    git -C "${repo_root}" fetch --quiet origin main ||
        printf 'warning: git fetch origin main failed; comparing with the last-fetched origin/main\n' >&2
    head="$(git -C "${repo_root}" rev-parse -q --verify HEAD)" || head=""
    upstream="$(git -C "${repo_root}" rev-parse -q --verify refs/remotes/origin/main)" || upstream=""
    if [ -n "$(git -C "${repo_root}" status --porcelain --untracked-files=no)" ] ||
        [ -z "${head}" ] || [ "${head}" != "${upstream}" ]; then
        printf 'make upgrade refused: %s is dirty or behind origin/main; in the pins worktree run git switch -c <branch> --no-track origin/main (or git reset --hard origin/main on its own branch) first\n' "${repo_root}" >&2
        exit 2
    fi
}

#
# @description Apply updated mise pins only from the configured chezmoi checkout.
function apply_upgraded_mise_config() {
    local source_path source_root
    if source_path="$(chezmoi source-path 2> /dev/null)" &&
        source_root="$(git -C "$source_path" rev-parse --show-toplevel 2> /dev/null)" &&
        [ "$(cd "$source_root" && pwd -P)" = "$(cd "$repo_root" && pwd -P)" ]; then
        chezmoi apply "${HOME}/.config/mise/config.toml" "${HOME}/.config/mise/mise.lock"
    else
        printf 'pins updated in %s; ~/.config/mise follows after merge and make update\n' "$repo_root"
    fi
}

#
# @description Run explicit upgrades for managed tooling.
# @arg $@ string Command-line arguments.
#
function main() {
    parse_args "$@"
    require_pins_checkout

    run_required_phase "Homebrew" upgrade_homebrew
    run_required_phase "mise self-update" upgrade_mise_self
    run_required_phase "mise inventory/install/upgrade" upgrade_mise_tools
    run_required_phase "Codex/Claude CLI upgrade" upgrade_agent_cli_tools
    run_optional_phase "terminal tool pin bump" bump_terminal_tool_pins
    run_optional_phase "release asset pin bump" bump_release_asset_pins
    run_required_phase "agent asset regeneration" upgrade_agent_assets
    run_required_phase "uv tool upgrade" upgrade_uv_tools
    run_optional_phase "GitHub CLI extension upgrade" upgrade_gh_extensions
    run_required_phase "apt system upgrade" upgrade_apt_packages
    if [ "${required_failures}" -eq 0 ]; then
        run_required_phase "apply upgraded mise config" apply_upgraded_mise_config
    fi

    printf '\nUpgrade summary: required failures: %d; optional warnings: %d\n' \
        "${required_failures}" "${optional_warnings}"
    [ "${required_failures}" -eq 0 ]
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
