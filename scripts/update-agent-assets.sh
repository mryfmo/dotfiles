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
    local candidate script_dir

    if [[ -n "${DOTFILES_SOURCE_DIR:-}" ]] && [[ -d "${DOTFILES_SOURCE_DIR}/vendor/compactiondb" ]]; then
        printf '%s\n' "${DOTFILES_SOURCE_DIR}"
        return 0
    fi

    # dirname is captured on its own line: inside the cd its status would be lost.
    script_dir="$(dirname -- "${BASH_SOURCE[0]}")" || {
        printf 'dirname failed on %s; the dotfiles source root is unknown.\n' "${BASH_SOURCE[0]}" >&2
        return 1
    }
    candidate="$(cd "${script_dir}/.." && pwd)" || return 1
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
# Rendered from assets.claude-plugins, assets.codex-plugins and assets.gh-extensions in
# home/dot_agents/agent-config.yaml by scripts/generate-agent-configs.py.
readonly AGENT_PLUGIN_PINS="${AGENT_ASSET_SCRIPT_DIR}/plugin-pins.json"
# Each tool's record directory, resolved once by the resolver make doctor uses (pin_records.py agent_home):
# CLAUDE_CONFIG_DIR, CODEX_HOME and GH_DATA_DIR/XDG_DATA_HOME are honoured the same way on both sides.
AGENT_CLAUDE_DIR="$(python3 -I "${AGENT_ASSET_SCRIPT_DIR}/pin_records.py" agent-home claude)" || exit 1
AGENT_CODEX_DIR="$(python3 -I "${AGENT_ASSET_SCRIPT_DIR}/pin_records.py" agent-home codex)" || exit 1
readonly AGENT_CLAUDE_DIR AGENT_CODEX_DIR

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
readonly CODEX_PONYTAIL_MARKETPLACE_NAME="ponytail"
readonly CODEX_PONYTAIL_MARKETPLACE_SOURCE="https://github.com/DietrichGebert/ponytail.git"
# Versions and installer checksums for both URLs are pinned in
# scripts/lib/installer-pins.sh, rendered from assets: in agent-config.yaml.
# Rendered from assets.pi-claude-bridge in home/dot_agents/agent-config.yaml; change the version and sha256 there
# together after reviewing the upstream diff, then regenerate bun.lock and re-check the patches.
PI_CLAUDE_BRIDGE_PIN_VERSION="0.9.3"
PI_CLAUDE_BRIDGE_TARBALL_SHA256="8d582b2fee1615b64a59890e3ac0af03c1e11bd06ba1997accdb767969556d67"
PI_CLAUDE_BRIDGE_ASSET_DIR="${DOTFILES_REPO_SOURCE_DIR}/home/dot_agents/assets/pi-claude-bridge"
# Rendered from assets.security-audit-skill in home/dot_agents/agent-config.yaml; change the commit and sha256 there
# together after reviewing the upstream diff. The archive is GitHub's source archive of that commit, never a branch head.
SECURITY_AUDIT_SKILL_COMMIT="c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
SECURITY_AUDIT_SKILL_SHA256="53e708ebf770dfe35b57df0586a5058707081a870cd149ce30a2d57c51ed29b6"
readonly SECURITY_AUDIT_SKILL_ARCHIVE_URL="https://codeload.github.com/cloudflare/security-audit-skill/tar.gz/${SECURITY_AUDIT_SKILL_COMMIT}"
# Rendered from assets.deepseek-harness in home/dot_agents/agent-config.yaml through scripts/lib/installer-pins.sh
# (DSH_PIN_TAG, DSH_ARCHIVE_SHA256); the archive is GitHub's tag archive, never a branch head.
readonly DSH_ARCHIVE_URL="https://github.com/deepseek-ai/deepseek-harness/archive/refs/tags/${DSH_PIN_TAG}.tar.gz"
# Install paths below assume the default XDG layout; the upstream installers
# honor XDG_*_HOME/TODE_INSTALL_ROOT overrides that this lifecycle does not.
HCOM_DARWIN_ARM64_URL="https://files.pythonhosted.org/packages/05/92/12d18a45357ef2a9765342203d5031b08dcd67bc988814428c10b46f6a3d/hcom-0.7.31-py3-none-macosx_11_0_arm64.whl"
HCOM_DARWIN_AMD64_URL="https://files.pythonhosted.org/packages/5b/bb/ca9ae354c9e2ded1f028ae663ee8d43e3e61c87fcd9b3d0df034d5f7aa5e/hcom-0.7.31-py3-none-macosx_10_12_x86_64.whl"
HCOM_LINUX_AMD64_URL="https://files.pythonhosted.org/packages/1d/de/02ef910a9f6776363c9042cdff965a772a09f9678289c30c320b1e976d6c/hcom-0.7.31-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
HCOM_LINUX_ARM64_URL="https://files.pythonhosted.org/packages/c3/53/27da25db38b9f079f4998d98b274ba50bf7da96b8b3904c5c24c7ab82504/hcom-0.7.31-py3-none-manylinux_2_28_aarch64.whl"
readonly OMP_TARBALL_URL="https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-${OMP_PIN_VERSION}.tgz"
readonly PI_CLAUDE_BRIDGE_TARBALL_URL="https://registry.npmjs.org/pi-claude-bridge/-/pi-claude-bridge-${PI_CLAUDE_BRIDGE_PIN_VERSION}.tgz"
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
# @description Prove that a destination the updater deletes or syncs into lies in the asset tree it manages,
#   before anything is removed through it: a path under ~/.agents or ~/.local whose parent is a directory whose
#   physical path (pwd -P) is its spelling under the physical HOME, so no component between the asset root and
#   the destination is a link, and whose own entry, when present, is no link either. A link at any of those places
#   is refused naming the path, so an rsync --delete or an rm -rf never reaches through it (verdicts/U276b: a
#   ~/.agents/compactiondb linked outside ~/.agents lost a file there).
# @arg $1 path The destination, without a trailing slash.
# @exitcode 0 The destination's parent is a real directory under the asset root and the destination is no link.
# @exitcode 1 Otherwise, or when a physical path cannot be read; nothing is written.
#
function assert_asset_destination() {
    local destination="$1" parent physical physical_home
    case ${destination} in
    "${HOME}/.agents/"?* | "${HOME}/.local/"?*) ;;
    *)
        printf 'ERROR: %s is not under %s/.agents or %s/.local; the updater writes only there.\n' "${destination}" "${HOME}" "${HOME}" >&2
        return 1
        ;;
    esac
    parent="${destination%/*}"
    if [ -L "${parent}" ] || [ ! -d "${parent}" ]; then
        printf 'ERROR: %s is a link or no directory; refusing to write %s through it.\n' "${parent}" "${destination}" >&2
        return 1
    fi
    physical_home="$(cd -P -- "${HOME}" && pwd -P)" || {
        printf 'ERROR: the physical path of %s could not be read; refusing to write %s.\n' "${HOME}" "${destination}" >&2
        return 1
    }
    physical="$(cd -P -- "${parent}" && pwd -P)" || {
        printf 'ERROR: the physical path of %s could not be read; refusing to write %s.\n' "${parent}" "${destination}" >&2
        return 1
    }
    if [ "${physical}" != "${physical_home}${parent#"${HOME}"}" ]; then # lint-comparisons: allow both sides are pwd -P physical paths
        printf 'ERROR: %s resolves to %s, outside the asset root; refusing to write %s through a link.\n' "${parent}" "${physical}" "${destination}" >&2
        return 1
    fi
    if [ -L "${destination}" ]; then
        printf 'ERROR: %s is a symbolic link; the updater writes only into a real directory; refusing.\n' "${destination}" >&2
        return 1
    fi
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
    local cli_version install_path

    if has_command "${cli}" && "${cli}" --version > /dev/null 2>&1; then
        return 0
    fi
    has_command mise || return 0

    printf 'Repairing %s through the mise npm backend.\n' "${cli}"
    # Both cooldowns hold: mise picks a release past minimum_release_age, npm's min-release-age covers its dependencies.
    MISE_NPM_PACKAGE_MANAGER=npm mise install --force "${mise_tool}"
    hash -r
    "${cli}" --version > /dev/null
    # A version the repaired CLI cannot print is recorded as unknown; its path must resolve.
    cli_version="$("${cli}" --version 2> /dev/null || printf 'unknown\n')"
    cli_version="${cli_version:-unknown}"
    # An empty answer is no location either: the manifest records only an absolute path.
    install_path="$(mise where "${mise_tool}" 2> /dev/null)" && [ -n "${install_path}" ] ||
        install_path="$(command -v "${cli}")" || {
        printf 'Cannot locate the repaired %s for the asset manifest.\n' "${cli}" >&2
        return 1
    }
    manifest_record "ensure_mise_npm_agent_cli:${cli}" installer "${cli_version}" "${install_path}" -- "MISE_NPM_PACKAGE_MANAGER=npm mise install --force ${mise_tool}" ||
        record_claude_failure "recording ensure_mise_npm_agent_cli:${cli} in the installed asset manifest"
}

#
# @description Install configured GitHub CLI extensions when authentication is ready.
#
function ensure_gh_extensions() {
    local repository

    bash "${DOTFILES_REPO_SOURCE_DIR}/install/common/gh_extensions.sh" || record_claude_failure "install/common/gh_extensions.sh"
    # The doctor judges each pinned extension; "not installed" (no gh login yet) is its warning, not a failure.
    if ! repository="$(pin_record plugin-ids "${AGENT_PLUGIN_PINS}" gh_extensions)"; then
        record_claude_failure "reading the pinned gh extensions"
        return 0
    fi
    while IFS= read -r repository; do
        [ -n "${repository}" ] || continue
        doctor_pin_check gh "${repository}" < /dev/null || record_claude_failure "the make doctor pin check of ${repository}"
    done <<< "${repository}"
}

#
# @description Tell whether a Codex marketplace is configured from the expected Git origin. Every probe's
#   output and status are captured separately: a `codex plugin marketplace list` or `git config` that fails
#   is "cannot tell", never "absent", so no marketplace is added over one that could not be read.
# @arg $1 string Marketplace name.
# @arg $2 string Expected HTTPS origin URL.
# @exitcode 0 Configured, and its clone's origin is the expected one.
# @exitcode 1 Not configured.
# @exitcode 2 Configured from another origin (or a root that is no Git clone): a foreign marketplace.
# @exitcode 3 The marketplace list or the clone's origin cannot be read.
#
function codex_marketplace_has_source() {
    local marketplace="$1"
    local expected_source="$2"
    local expected_ssh="git@github.com:${expected_source#https://github.com/}"
    local listing root remote status=0

    if ! listing="$(codex plugin marketplace list 2> /dev/null)"; then
        printf 'ERROR: codex plugin marketplace list failed; cannot tell whether %s is configured.\n' "${marketplace}" >&2
        return 3
    fi
    root="$(awk -v name="${marketplace}" '$1 == name { print $2; exit }' <<< "${listing}")" || return 3
    if [ -z "${root}" ]; then
        return 1
    fi
    if [ ! -d "${root}/.git" ]; then
        return 2
    fi
    remote="$(git -C "${root}" config --get remote.origin.url 2> /dev/null)" || status=$?
    if [ "${status}" -eq 1 ]; then
        return 2
    elif [ "${status}" -ne 0 ]; then
        printf 'ERROR: cannot read the origin of %s (git exit %s).\n' "${root}" "${status}" >&2
        return 3
    fi
    case "${remote}" in
    "${expected_source}" | "${expected_source%.git}" | "${expected_ssh}" | "${expected_ssh%.git}") return 0 ;;
    esac
    return 2
}

#
# @description Ensure the official Claude Code plugin marketplace is configured.
#
# @description Download the pinned Crit release binary, verify it against its reviewed sha256 and
#   the release's checksums.txt, and atomically install it.
# @arg $1 string Release artifact name.
# @arg $2 string The reviewed sha256 of that artifact (scripts/lib/installer-pins.sh).
# @arg $3 path Destination executable path.
#
function install_crit_release() (
    local artifact="$1"
    local pinned="$2"
    local target="$3"
    local tag="${CRIT_PIN_VERSION}"
    local actual base_url checksums download expected staged_version staging=""

    base_url="https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}"
    download="$(mktemp)" || return
    checksums="$(mktemp)" || return
    trap 'rm -f "${download}" "${checksums}" ${staging:+"${staging}"}' EXIT
    # Every download here gets 30 s to connect and fails a transfer under 1 KB/s for 60 s, so a stalled one ends.
    curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/${artifact}" -o "${download}" || return
    curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/checksums.txt" -o "${checksums}" || return
    expected="$(awk -v name="${artifact}" '$2 == name { print $1; exit }' "${checksums}")"
    actual="$(shasum -a 256 "${download}" | awk '{ print $1 }')"
    # The release is mutable, so the reviewed sha256 is the check; checksums.txt only re-checks the download.
    if [ -z "${pinned}" ] || [ "${actual}" != "${pinned}" ] || [ "${actual}" != "${expected}" ]; then
        printf 'Crit checksum mismatch for %s %s.\n' "${artifact}" "${tag}" >&2
        return 1
    fi

    mkdir -p "$(dirname "${target}")" || return
    staging="$(mktemp "${target}.XXXXXX")" || return
    install -m 0755 "${download}" "${staging}" || return
    staged_version="$(crit_version "${staging}")" || return
    [ "${staged_version}" = "${tag#v}" ] || return
    mv -f "${staging}" "${target}"
)

#
# @description Print the version a Crit binary reports, without a leading v, or nothing when it
#   is absent or cannot report one, so a broken install is replaced like a missing one.
# @arg $1 path Crit executable.
#
function crit_version() {
    local output
    [ -x "$1" ] || return 0
    # A binary that exits non-zero is broken whatever it printed, so it reports no version.
    output="$("$1" --version 2> /dev/null)" || return 0
    printf '%s\n' "${output}" | awk '$1 == "crit" { sub(/^v/, "", $2); print $2; exit }'
}

#
# @description Print the host's kernel name and machine (`uname -s`, `uname -m`), space-separated,
#   for the platform cases below.
# @exitcode 1 uname failed; the message names the flag, and no platform is guessed.
#
function uname_platform() {
    local kernel machine
    kernel="$(uname -s)" || {
        printf 'uname -s failed; the platform is unknown.\n' >&2
        return 1
    }
    machine="$(uname -m)" || {
        printf 'uname -m failed; the platform is unknown.\n' >&2
        return 1
    }
    printf '%s %s\n' "${kernel}" "${machine}"
}

#
# @description Ensure the Crit CLI is the pinned release for agent integrations.
#
function ensure_crit_cli() {
    local artifact checksum installed kernel machine platform tag="${CRIT_PIN_VERSION}" target

    platform="$(uname_platform)" || return 1
    read -r kernel machine <<< "${platform}"
    case "${kernel}-${machine}" in
    Linux-x86_64 | Linux-amd64) artifact="crit-linux-amd64" checksum="${CRIT_LINUX_AMD64_SHA256}" ;;
    Linux-aarch64 | Linux-arm64) artifact="crit-linux-arm64" checksum="${CRIT_LINUX_ARM64_SHA256}" ;;
    Darwin-x86_64 | Darwin-amd64) artifact="crit-darwin-amd64" checksum="${CRIT_DARWIN_AMD64_SHA256}" ;;
    Darwin-arm64 | Darwin-aarch64) artifact="crit-darwin-arm64" checksum="${CRIT_DARWIN_ARM64_SHA256}" ;;
    *)
        printf 'Skipping Crit integrations: unsupported platform %s %s.\n' "${kernel}" "${machine}"
        return 1
        ;;
    esac

    target="${HOME}/.local/bin/crit"
    installed="$(crit_version "${target}")" || return 1
    if [ "${installed}" != "${tag#v}" ]; then
        section "Crit CLI"
        install_crit_release "${artifact}" "${checksum}" "${target}" || return 1
    fi
    export PATH="${HOME}/.local/bin:${PATH}"
    hash -r
    manifest_record "ensure_crit_cli" installer "${tag}" "${target}" -- "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/${artifact}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/checksums.txt" "shasum -a 256 <binary>" "install -m 0755 <binary> ${target}" ||
        record_claude_failure "recording ensure_crit_cli in the installed asset manifest"
}

#
# @description Ensure the Crit Claude Code plugin marketplace is configured.
#
# @description Ensure the Ponytail Claude Code plugin marketplace is configured.
#
# @description Run scripts/pin_records.py, the one strict reader of every record the pin checks use: it prints
#   the parsed value, or exits 2 with `ERROR: <record>: <field>: <why>` for a record it cannot read, one of an
#   unknown shape, or one naming a foreign identity (an absent record is not an error).
# @arg $@ string A pin_records.py command and its arguments.
#
function pin_record() {
    python3 -I "${AGENT_ASSET_SCRIPT_DIR}/pin_records.py" "$@"
}

#
# @description Print one recorded field of a plugin pin from scripts/plugin-pins.json.
# @arg $1 string Agent: `claude` or `codex`.
# @arg $2 string Fully qualified plugin ID.
# @arg $3 string Field: `pin` or `ref`.
# @exitcode 1 When the pins file cannot be read or does not record the field.
#
function plugin_pin() {
    pin_record plugin-pin "${AGENT_PLUGIN_PINS}" "$@"
}

#
# @description Run `claude` from a fresh empty directory, so no project's .claude settings take part in what
#   it reads or writes; the directory is removed afterwards.
# @arg $@ string Arguments for `claude`.
# @exitcode 1 When the scratch directory cannot be made; otherwise claude's own exit status.
#
function claude_outside_projects() {
    (
        neutral="$(mktemp -d "${TMPDIR:-/tmp}/claude-neutral.XXXXXX")" || exit 1
        trap 'rm -rf "${neutral}"' EXIT
        cd "${neutral}" || exit 1
        claude "$@"
    )
}

#
# @description Print `enabled` when ~/.claude/settings.json (user scope) holds the boolean true for a plugin,
#   `disabled` only for the boolean false, `unset` when it names the plugin not at all (Claude Code then
#   applies the plugin's default, which may be enabled), and `invalid:<type>` for any other value (a string
#   "false" included). Only `disabled` proves a plugin off. A missing file names nothing.
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 1 When the settings file exists but is not a readable JSON object.
#
function claude_user_enabled() {
    pin_record claude-enabled "${AGENT_CLAUDE_DIR}/settings.json" "$1"
}

#
# @description Print every installation of a Claude Code plugin from installed_plugins.json, one
#   `<scope>\t<version>\t<project path>` line each, or nothing when it is not installed.
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 1 When installed_plugins.json exists but cannot be parsed: a failed read is never "not installed".
#
function claude_plugin_installs() {
    pin_record claude-installs "${AGENT_CLAUDE_DIR}/plugins/installed_plugins.json" "$1"
}

#
# @description The one parser of a Claude Code plugin's user-scope installation state: print exactly `absent`
#   (the list names no user-scope installation) or `installed <version>` with a version that is one strict
#   component ([A-Za-z0-9][A-Za-z0-9._+-]*). Every caller reads its output in a `case` whose default is an
#   error, and only into a variable named user_install (the structural test checks both).
# @arg $1 string The JSON list claude_plugin_installs prints.
# @exitcode 1 When the list is not JSON (a failure is never "absent").
# @exitcode 3 When the list yields anything else (an empty, malformed or non-component version).
#
function claude_user_install() {
    local reply

    reply="$(jq -er '[.[] | select(.scope == "user")] | if length == 0 then "absent" else "installed \(.[0].version | if type == "string" then . else "" end)" end' <<< "$1")" || return 1
    case "${reply}" in
    absent) printf 'absent\n' ;;
    "installed "*)
        if [[ ${reply#installed } =~ ^[A-Za-z0-9][A-Za-z0-9._+-]*$ ]]; then
            printf '%s\n' "${reply}"
        else
            printf 'ERROR: the user-scope installation record holds no valid version: %q\n' "${reply}" >&2
            return 3
        fi
        ;;
    *)
        printf 'ERROR: unexpected user-scope installation state: %q\n' "${reply}" >&2
        return 3
        ;;
    esac
}

#
# @description Print what the user-scope installation of a Claude Code plugin is compared with its pin by
#   (pin_records.claude_observed): its version for a version pin; for a content pin, the content digest of its
#   installPath together with its catalog entry in the installed marketplace clone (pin_records.content_digest),
#   whatever commit its version names.
# @arg $1 string The JSON list claude_plugin_installs prints, holding a user-scope installation.
# @arg $2 string The pin.
# @exitcode 1 When there is no user-scope installation, or it cannot be read or hashed (a symlink or special
#   file in it included); nothing is printed, so an unknown state is never compared.
#
function claude_user_observed() {
    local user_install install_path
    user_install="$(claude_user_install "$1")" || return 1
    case "${user_install}" in
    "installed "?*) ;;
    *) return 1 ;;
    esac
    install_path="$(jq -er 'first(.[] | select(.scope == "user") | .installPath)' <<< "$1")" || return 1
    pin_record claude-observed "$2" "${user_install#installed }" "${install_path}"
}

#
# @description Print the user-scope installed version of a Claude Code plugin for the asset manifest. A
#   failure is never a version: nothing is printed for it, and `unknown` is never produced.
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 4 When installed_plugins.json names no user-scope installation (`absent`): nothing to record.
# @exitcode 1 When the record cannot be read or parsed, or names an unexpected state.
#
function claude_user_plugin_version() {
    local installs user_install

    if ! installs="$(claude_plugin_installs "$1")"; then
        printf 'ERROR: cannot read the installation records of %s for the asset manifest.\n' "$1" >&2
        return 1
    fi
    user_install="$(claude_user_install "${installs}")" || return 1
    case "${user_install}" in
    "installed "?*) printf '%s\n' "${user_install#installed }" ;;
    absent) return 4 ;;
    *)
        printf 'ERROR: unexpected installation state of %s: %s\n' "$1" "${user_install}" >&2
        return 1
        ;;
    esac
}

#
# @description Record a converged Claude Code plugin step in the installed asset manifest with the version
#   installed_plugins.json records. A version that cannot be read is a counted failure, never `unknown`; a
#   plugin with no user-scope installation has nothing to record (a WARN).
# @arg $1 string Install step name.
# @arg $2 string Fully qualified Claude Code plugin ID.
# @arg $@ string The manifest paths, `--`, and the command lines (manifest_record after its version).
#
function record_claude_plugin_step() {
    local step="$1" plugin_id="$2" plugin_version status=0
    shift 2

    plugin_version="$(claude_user_plugin_version "${plugin_id}")" || status=$?
    case "${status}" in
    0)
        manifest_record "${step}" plugin "${plugin_version}" "$@" ||
            record_claude_failure "recording ${step} in the installed asset manifest"
        ;;
    4) printf 'WARN: %s has no user-scope installation; %s is not recorded in the installed asset manifest.\n' "${plugin_id}" "${step}" >&2 ;;
    *) record_claude_failure "reading the installed version of ${plugin_id} for the asset manifest" ;;
    esac
}

#
# @description Register the marketplace a pinned Claude Code plugin comes from (its `marketplace` in
#   assets.claude-plugins), unless a marketplace of that name is already registered.
# @arg $1 string Fully qualified Claude Code plugin ID (`<plugin>@<marketplace name>`).
# @exitcode 1 When the pin records no source, the list cannot be parsed, or `marketplace add` fails.
# @exitcode 3 When a marketplace of that name is registered from another source: a foreign identity.
# @exitcode 4 When `claude plugin marketplace list --json` itself fails; its exit status and stderr are printed.
#
function ensure_claude_plugin_marketplace() {
    local plugin_id="$1"
    local name="${1#*@}" source listing state errors status=0

    if ! source="$(plugin_pin claude "${plugin_id}" marketplace)"; then
        printf 'ERROR: %s records no marketplace for %s.\n' "${AGENT_PLUGIN_PINS}" "${plugin_id}" >&2
        return 1
    fi
    errors="$(mktemp)" || return 1
    listing="$(claude_outside_projects plugin marketplace list --json 2> "${errors}")" || status=$?
    if [ "${status}" -ne 0 ]; then
        printf 'claude plugin marketplace list --json failed (exit %s), so %s cannot be verified for %s; its stderr:\n' "${status}" "${source}" "${plugin_id}" >&2
        sed -n '1,20s/^/    /p' "${errors}" >&2 || true
        rm -f "${errors}"
        return 4
    fi
    rm -f "${errors}"
    if ! state="$(pin_record claude-marketplace "${name}" "${source}" <<< "${listing}")"; then
        return 1
    fi
    if [ "${state}" = "registered" ]; then
        return 0
    fi
    if [ "${state}" = "foreign" ]; then
        printf 'ERROR: the Claude Code marketplace %s is registered from another source than %s.\n' "${name}" "${source}" >&2
        return 3
    fi
    if ! claude_outside_projects plugin marketplace add "${source}"; then
        printf 'ERROR: claude plugin marketplace add %s failed; %s cannot be installed.\n' "${source}" "${plugin_id}" >&2
        return 1
    fi
}

#
# @description Run make doctor's own pin check for one asset (check-agent-runtime.py --pin-check), the only
#   judge of whether a convergence step reached its pin: the updater never decides that itself, so it and
#   the doctor cannot disagree. Its errors are printed.
# @arg $1 string Agent: claude, codex or gh.
# @arg $2 string Plugin id, or <owner>/<repository> for a gh extension.
# @exitcode 1 When the doctor's check reports drift or cannot read a record.
#
function doctor_pin_check() {
    python3 -I "${AGENT_ASSET_SCRIPT_DIR}/check-agent-runtime.py" --pin-check "$1" "$2" > /dev/null
}

#
# @description Judge the version a plugin step left installed against its pin, for Claude Code and Codex alike.
#   Off its pin, a WARN names the plugin, both versions and the review bump the pin needs.
# @arg $1 string Agent: claude or codex.
# @arg $2 string Fully qualified plugin ID.
# @arg $3 string The installed version.
# @arg $4 string The pin.
# @arg $5 number 1 when the step installed it fresh (nothing of it was installed or enabled before), else 0.
# @exitcode 0 At the pin.
# @exitcode 11 (PLUGIN_FRESH_OFF_PIN) Off its pin after a fresh install; converge_or_disable disables it.
# @exitcode 1 Off its pin otherwise.
#
function judge_installed_version() {
    local agent="$1" plugin_id="$2" version="$3" pin="$4" fresh="$5"

    if [ "${version}" = "${pin}" ]; then
        return 0
    fi
    printf 'WARN: %s plugin %s is at %s, not its pin %s; the pin needs a review bump: review that release and record its version in assets.%s-plugins (home/dot_agents/agent-config.yaml).\n' "${agent}" "${plugin_id}" "${version}" "${pin}" "${agent}" >&2
    if [ "${fresh}" -eq 1 ]; then
        return "${PLUGIN_FRESH_OFF_PIN}"
    fi
    return 1
}

#
# @description Move the user-scope installation of a Claude Code plugin towards its recorded pin (assets.claude-plugins).
# @description
#   Only ever called through converge_or_disable, which decides the outcome and disables the plugin on any
#   failure. This repository installs plugins at user scope only, so only that installation is managed; a
#   project- or local-scope installation belongs to its project and is reported as not managed, never
#   converged. Claude Code installs only a marketplace's current release and takes no version: a missing
#   plugin is installed at user scope from its recorded marketplace (registered first when absent); a
#   user-scope installation at another version is updated. Nothing is installed or updated from a
#   marketplace whose identity is not verified. Every `claude` call runs from an empty directory, so no
#   project settings take part. The enabled state is never changed here.
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 0 When the re-read user-scope installation is at the pin.
# @exitcode 10 (PLUGIN_SKIPPED) When the marketplace list cannot be read and the records show the plugin
#   neither installed at any scope nor enabled: nothing to verify, nothing changed.
# @exitcode 11 (PLUGIN_FRESH_OFF_PIN) When a fresh install (no installation at any scope, not enabled
#   before) landed on a release other than the pin (judge_installed_version); converge_or_disable disables it.
# @exitcode 1 Otherwise: the pin or a record cannot be read, the marketplace is foreign or cannot be
#   registered, the install fails, or the installation is still off its pin.
#
function move_claude_plugin_to_pin() {
    local plugin_id="$1"
    local pin installs user_install observed marketplace enabled fresh=0

    if ! pin="$(plugin_pin claude "${plugin_id}" pin)"; then
        printf 'Cannot read the pin of %s from %s.\n' "${plugin_id}" "${AGENT_PLUGIN_PINS}" >&2
        return 1
    fi
    if ! installs="$(claude_plugin_installs "${plugin_id}")"; then
        printf 'ERROR: cannot read the installation records of %s (installed_plugins.json).\n' "${plugin_id}" >&2
        return 1
    fi
    jq -r --arg id "${plugin_id}" '.[] | select(.scope != "user")
        | "WARN: plugin \($id) installed in \(.scope) scope at \(.projectPath // .installPath): not managed (make update manages user scope only)."' \
        <<< "${installs}" >&2 || return 1
    user_install="$(claude_user_install "${installs}")" || return 1
    # The marketplace identity is verified before anything is installed or updated from it; a foreign one may
    # serve a release under the pinned version, so its plugin fails (and is disabled) at any version.
    # Fresh: no installation at any scope and not enabled in the user settings (as the doctor's readers see it),
    # so nothing of this plugin can be running before this step.
    if [ "${installs}" = "[]" ] && enabled="$(claude_user_enabled "${plugin_id}")" && [ "${enabled}" != "enabled" ]; then
        fresh=1
    fi
    marketplace=0
    ensure_claude_plugin_marketplace "${plugin_id}" || marketplace=$?
    if [ "${marketplace}" -eq 4 ] && [ "${fresh}" -eq 1 ]; then
        # A failure to verify matters only when something could run; here nothing can, so the step is skipped.
        return "${PLUGIN_SKIPPED}"
    fi
    if [ "${marketplace}" -ne 0 ]; then
        printf 'ERROR: %s is not installed or updated from an unverified marketplace.\n' "${plugin_id}" >&2
        return 1
    fi
    case "${user_install}" in
    absent)
        if ! claude_outside_projects plugin install "${plugin_id}" --scope user < /dev/null; then
            printf 'ERROR: claude plugin install %s failed; the pinned plugin is not installed.\n' "${plugin_id}" >&2
            return 1
        fi
        ;;
    "installed "?*)
        # An installation whose pin state cannot be computed is a failure: nothing is updated from an unknown
        # state, and converge_or_disable disables it.
        if ! observed="$(claude_user_observed "${installs}" "${pin}")"; then
            printf 'ERROR: cannot read the installed content of %s to compare it with its pin; nothing is updated.\n' "${plugin_id}" >&2
            return 1
        fi
        if [ "${observed}" != "${pin}" ]; then
            claude_outside_projects plugin update "${plugin_id}" --scope user < /dev/null || true
        fi
        ;;
    *)
        printf 'ERROR: unexpected installation state of %s: %s\n' "${plugin_id}" "${user_install}" >&2
        return 1
        ;;
    esac
    if ! installs="$(claude_plugin_installs "${plugin_id}")"; then
        printf 'ERROR: cannot re-read the installation records of %s after changing it.\n' "${plugin_id}" >&2
        return 1
    fi
    user_install="$(claude_user_install "${installs}")" || return 1
    case "${user_install}" in
    "installed "?*) ;;
    absent)
        printf 'ERROR: %s has no user-scope installation after claude plugin install.\n' "${plugin_id}" >&2
        return 1
        ;;
    *)
        printf 'ERROR: unexpected installation state of %s: %s\n' "${plugin_id}" "${user_install}" >&2
        return 1
        ;;
    esac
    if ! observed="$(claude_user_observed "${installs}" "${pin}")"; then
        printf 'ERROR: cannot read the installed content of %s to compare it with its pin.\n' "${plugin_id}" >&2
        return 1
    fi
    judge_installed_version claude "${plugin_id}" "${observed}" "${pin}" "${fresh}"
}

#
# @description Disable a plugin that did not reach its pin, and prove it off.
# @description
#   Claude Code runs a plugin's hooks with no trust step, so the plugin is disabled at user scope and the
#   user settings file must then hold the boolean false. Codex has no disable command and chezmoi manages
#   `[plugins."<id>"] enabled = true`, so its copy is removed (`codex plugin remove`), and no cached copy may
#   remain; the next make update that can reach the pin installs it again. Records that readably name no
#   installation leave nothing to disable; unreadable ones never mean "not installed".
# @arg $1 string Agent: claude or codex.
# @arg $2 string Fully qualified plugin ID.
# @exitcode 1 When the plugin cannot be proven disabled.
#
function disable_plugin() {
    local agent="$1" plugin_id="$2"
    local installs user_install enabled codex_copy

    case "${agent}" in
    claude)
        # Nothing to disable only on the readers' explicit `absent`. A state that cannot be read is still
        # disabled (best effort), and fails: it cannot be proven.
        user_install="unreadable"
        if installs="$(claude_plugin_installs "${plugin_id}" 2> /dev/null)"; then
            user_install="$(claude_user_install "${installs}" 2> /dev/null)" || user_install="unreadable"
        fi
        case "${user_install}" in
        absent) return 0 ;;
        "installed "?*) ;;
        *)
            printf 'ERROR: cannot tell whether Claude Code plugin %s is installed (%s); disabling it anyway.\n' "${plugin_id}" "${user_install}" >&2
            claude_outside_projects plugin disable "${plugin_id}" --scope user < /dev/null || true
            return 1
            ;;
        esac
        # Idempotent: a plugin already disabled may make the command fail; the settings file shows the result.
        claude_outside_projects plugin disable "${plugin_id}" --scope user < /dev/null || true
        if ! enabled="$(claude_user_enabled "${plugin_id}")" || [ "${enabled}" != "disabled" ]; then
            printf 'ERROR: Claude Code plugin %s is not at its pin and ~/.claude/settings.json does not disable it (%s).\n' "${plugin_id}" "${enabled:-unreadable}" >&2
            return 1
        fi
        printf 'WARN: Claude Code plugin %s is disabled at user scope; once make update passes, re-enable it with: claude plugin enable %s --scope user\n' "${plugin_id}" "${plugin_id}" >&2
        ;;
    codex)
        # Nothing to remove only on the reader's explicit `absent`. A state that cannot be read is still removed
        # (best effort), and fails: it cannot be proven.
        codex_copy="$(codex_plugin_copy "${plugin_id}" 2> /dev/null)" || codex_copy="unreadable"
        case "${codex_copy}" in
        absent) return 0 ;;
        "copy "?*) ;;
        *)
            printf 'ERROR: cannot tell whether Codex plugin %s is cached (%s); removing it anyway.\n' "${plugin_id}" "${codex_copy}" >&2
            codex plugin remove "${plugin_id}" < /dev/null || true
            return 1
            ;;
        esac
        codex plugin remove "${plugin_id}" < /dev/null || true
        codex_copy="$(codex_plugin_copy "${plugin_id}")" || codex_copy="unreadable"
        case "${codex_copy}" in
        absent) ;;
        *)
            printf 'ERROR: Codex plugin %s is not at its pin and codex plugin remove left a copy (%s).\n' "${plugin_id}" "${codex_copy}" >&2
            return 1
            ;;
        esac
        printf 'WARN: Codex plugin %s was removed; the next make update that reaches its pin installs it again.\n' "${plugin_id}" >&2
        ;;
    *)
        printf 'ERROR: no way to disable a %s plugin (%s).\n' "${agent}" "${plugin_id}" >&2
        return 1
        ;;
    esac
}

#
# @description The one fail-safe of every Claude Code and Codex plugin step: run the step, then make
#   doctor's pin check for the plugin (doctor_pin_check). The plugin stays as the step left it only when both
#   exit 0; on every other outcome (an error or early return of the step, drift, a record that cannot be
#   read, a check that cannot run) it is disabled (disable_plugin) before the failure is returned and counted.
#   One rule decides what fails the run: unreviewed code that could be active, or an active state that cannot
#   be verified. So two outcomes are a WARN, not a failure: a step that could not verify a plugin that was
#   neither installed nor enabled (PLUGIN_SKIPPED), and an install that landed off its pin and is proven
#   disabled (PLUGIN_FRESH_OFF_PIN: a fresh Claude install, or any Codex copy the doctor rejects after the
#   step; make doctor still reports it as drift). Both agents take the same path: a Claude plugin is disabled
#   at user scope, a Codex copy removed (disable_plugin), and either is proven.
#   The step runs in a subshell, so an `exit` or a `set -u` abort inside it comes back here too.
# @arg $1 string Agent: claude or codex.
# @arg $2 string Fully qualified plugin ID.
# @arg $@ string The step's command and arguments.
# @exitcode 0 When the step and the doctor's pin check both pass.
# @exitcode 2 When the step skipped the plugin (PLUGIN_SKIPPED: nothing installed or enabled to verify)
#   and the doctor's check passes, or a fresh off-pin install is proven disabled: a WARN, not counted, and the
#   caller records nothing.
# @exitcode 1 Otherwise, after the disable; counted in PIN_FAILURES, so the run fails.
#
function converge_or_disable() {
    local agent="$1" plugin_id="$2"
    local status=0 check=0
    shift 2

    ("$@") || status=$?
    doctor_pin_check "${agent}" "${plugin_id}" < /dev/null || check=$?
    if [ "${status}" -eq 0 ] && [ "${check}" -eq 0 ]; then
        printf '%s plugin %s is at its pin (make doctor agrees).\n' "${agent}" "${plugin_id}"
        return 0
    fi
    if [ "${status}" -eq "${PLUGIN_FRESH_OFF_PIN}" ]; then
        # make doctor keeps reporting this copy as drift: that is the signal for the review bump.
        if disable_plugin "${agent}" "${plugin_id}"; then
            printf 'WARN: %s plugin %s is off its pin and is proven disabled (Claude) or removed (Codex), so nothing unreviewed is active; not a run failure. make doctor reports it until its pin gets a review bump.\n' "${agent}" "${plugin_id}" >&2
            return 2
        fi
        printf 'ERROR: %s plugin %s landed off its pin and cannot be proven disabled.\n' "${agent}" "${plugin_id}" >&2
        PIN_FAILURES=$((PIN_FAILURES + 1))
        return 1
    fi
    if [ "${status}" -eq "${PLUGIN_SKIPPED}" ] && [ "${check}" -eq 0 ]; then
        printf 'WARN: %s plugin %s was not installed: its marketplace cannot be verified on this host, and it is neither installed nor enabled, so nothing unreviewed is active. Run make update once "%s plugin marketplace list" works.\n' "${agent}" "${plugin_id}" "${agent}" >&2
        return 2
    fi
    if [ "${check}" -ne 0 ]; then
        printf 'ERROR: make doctor still reports %s off its pin after this step.\n' "${plugin_id}" >&2
    fi
    printf 'ERROR: %s plugin %s did not reach its pin (step exit %s, make doctor pin check exit %s); disabling it.\n' "${agent}" "${plugin_id}" "${status}" "${check}" >&2
    disable_plugin "${agent}" "${plugin_id}" || true
    PIN_FAILURES=$((PIN_FAILURES + 1))
    return 1
}

#
# @description Keep the user-scope installation of a Claude Code plugin at its recorded pin, or disable it.
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 1 When it did not reach its pin (disabled and counted by converge_or_disable).
#
function converge_claude_plugin() {
    converge_or_disable claude "$1" move_claude_plugin_to_pin "$1"
}

# Plugin IDs converged in this run, space-delimited (bash 3.2 has no associative arrays), and the
# count of plugins whose convergence failed for any reason; main fails the run when it is not zero.
CLAUDE_CONVERGED=" "
PIN_FAILURES=0
# The exit statuses a plugin step returns for the two outcomes converge_or_disable reports as a WARN: a plugin
# it could not verify and found neither installed nor enabled, and an install that landed off its pin and can
# be proven disabled or removed (a fresh Claude install; a Codex copy, cached before the step or not). Any other
# non-zero status is a failure.
readonly PLUGIN_SKIPPED=10
readonly PLUGIN_FRESH_OFF_PIN=11

#
# @description Count a failed step (a plugin setup step, a pin check, an asset manifest record) and keep
#   going, so the run still reaches the convergence of every pinned plugin and fail_on_pin_failures
#   still fails it at the end. A step that runs in a subshell returns its failure instead, which stops the run.
# @arg $1 string What failed.
#
function record_claude_failure() {
    printf 'ERROR: %s failed; continuing so every pinned plugin is still checked, and the run will fail.\n' "$1" >&2
    PIN_FAILURES=$((PIN_FAILURES + 1))
}

#
# @description Converge one Claude Code plugin once per run (converge_claude_plugin counts a failure).
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 1 When the plugin did not reach its pin and was disabled.
#
function converge_claude_step() {
    CLAUDE_CONVERGED="${CLAUDE_CONVERGED}$1 "
    converge_claude_plugin "$1"
}

#
# @description Fail the run when any plugin, Claude Code or Codex, could not be checked or kept at its pin
#   (counted by converge_or_disable and record_claude_failure for either agent).
# @exitcode 1 When PIN_FAILURES is not zero.
#
function fail_on_pin_failures() {
    if [ "${PIN_FAILURES}" -gt 0 ]; then
        printf 'ERROR: %s plugin(s) (Claude Code or Codex) could not be checked or kept at their pin; see the errors above.\n' "${PIN_FAILURES}" >&2
        return 1
    fi
}

#
# @description Converge every Claude Code plugin scripts/plugin-pins.json records that no step above handled.
# @description
#   The pinned list in assets.claude-plugins is the one source: a plugin with a setup step of its own
#   (marketplace, Crit CLI) was converged there, and every other one, pstack included, is converged here,
#   so each pinned plugin is checked and disabled when it is off its pin.
# @exitcode 0 Always; a pins file that cannot be read counts as a failure that main reports.
#
function converge_claude_plugins() {
    local ids plugin_id

    has_command claude || return 0
    if ! ids="$(pin_record plugin-ids "${AGENT_PLUGIN_PINS}" claude)"; then
        printf 'ERROR: cannot read the Claude Code plugin pins from %s; no plugin was checked against its pin.\n' "${AGENT_PLUGIN_PINS}" >&2
        PIN_FAILURES=$((PIN_FAILURES + 1))
        return 0
    fi
    section "Claude Code plugin pins"
    while IFS= read -r plugin_id; do
        case "${CLAUDE_CONVERGED}" in
        *" ${plugin_id} "*) continue ;;
        esac
        converge_claude_step "${plugin_id}" < /dev/null || true
    done <<< "${ids}"
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
    # The manifest declares no trust for herdr's hook (README.md, the hook trust paragraph): it is herdr's own file.
    printf "Codex runs herdr's SessionStart hook (~/.codex/hooks.json) only after you trust it with /hooks once per profile.\n"
    # A herdr that cannot print its version is recorded as unknown, as before.
    local herdr_output herdr_version
    herdr_output="$(herdr --version 2> /dev/null)" || herdr_output=""
    herdr_version="$(awk 'NF { version = $NF } END { print version ? version : "unknown" }' <<< "${herdr_output}")" || return 1
    manifest_record "ensure_herdr_integrations" integration "${herdr_version}" "${HOME}/.claude/hooks/herdr-agent-state.sh" "${HOME}/.codex/herdr-agent-state.sh" -- "herdr integration install claude" "herdr integration install codex" ||
        record_claude_failure "recording ensure_herdr_integrations in the installed asset manifest"
}

#
# @description Re-apply only the managed Codex config files, so their modify scripts hash the
#   plugin hooks this run has just installed (Codex runs a hook only when its trust hash is current).
#   Runs last and unattended: `chezmoi apply --force`, no prompt, no network. Inside a chezmoi run
#   (`CHEZMOI=1`, exported to every script chezmoi runs) the outer apply holds the persistent state lock,
#   so the nested apply would only time out on it: the refresh is skipped with a note, and the standalone
#   `./scripts/update-agent-assets.sh` run that `make update` makes right after the apply does it.
# @exitcode 0 Always; a failed refresh only warns, and the next apply retries it.
#
function refresh_codex_hook_trust() {
    local managed target
    local pattern='/\.codex/([a-z0-9_]+\.)?config\.toml$'
    local -a targets=()

    if [ "${CHEZMOI:-}" = "1" ]; then
        printf 'Codex hook trust: not refreshed inside chezmoi apply (it holds the state lock); the standalone ./scripts/update-agent-assets.sh run of make update refreshes it.\n'
        return 0
    fi
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
# @description Keep the Claude Code Superpowers plugin at its recorded pin.
#
function update_claude_superpowers() {
    if ! has_command claude; then
        printf 'Skipping Claude Code plugins: claude command not found.\n'
        return 0
    fi

    section "Claude Code plugins"
    # Refreshed only once its identity is verified; converge_claude_step verifies again and reports and judges
    # any failure, so this call\'s own messages are not repeated.
    if ensure_claude_plugin_marketplace "${CLAUDE_SUPERPOWERS_PLUGIN}" 2> /dev/null; then
        claude_outside_projects plugin marketplace update claude-plugins-official || true
    fi
    converge_claude_step "${CLAUDE_SUPERPOWERS_PLUGIN}" || return 0
    record_claude_plugin_step "update_claude_superpowers" "${CLAUDE_SUPERPOWERS_PLUGIN}" "${AGENT_CLAUDE_DIR}/plugins/cache/claude-plugins-official/superpowers" "${AGENT_CLAUDE_DIR}/settings.json" -- "claude plugin marketplace add ${CLAUDE_SUPERPOWERS_MARKETPLACE}" "claude plugin marketplace update claude-plugins-official" "claude plugin install ${CLAUDE_SUPERPOWERS_PLUGIN}" "claude plugin update ${CLAUDE_SUPERPOWERS_PLUGIN}"
}

#
# @description Keep the Claude Code Crit plugin at its recorded pin.
#
function update_claude_crit() {
    if ! has_command claude; then
        printf 'Skipping Claude Code Crit plugin: claude command not found.\n'
        return 0
    fi

    section "Claude Code Crit plugin"
    # The Crit CLI is optional for the plugin; its failure never skips the pin check below.
    ensure_crit_cli || printf 'WARN: the Crit CLI is not installed; the Claude Code Crit plugin is still checked against its pin.\n' >&2
    # Refreshed only once its identity is verified; converge_claude_step verifies again and reports and judges
    # any failure, so this call\'s own messages are not repeated.
    if ensure_claude_plugin_marketplace "${CLAUDE_CRIT_PLUGIN}" 2> /dev/null; then
        claude_outside_projects plugin marketplace update "${CLAUDE_CRIT_MARKETPLACE_NAME}" || true
    fi
    converge_claude_step "${CLAUDE_CRIT_PLUGIN}" || return 0
    record_claude_plugin_step "update_claude_crit" "${CLAUDE_CRIT_PLUGIN}" "${AGENT_CLAUDE_DIR}/plugins/cache/crit/crit" "${AGENT_CLAUDE_DIR}/settings.json" -- "ensure_crit_cli" "claude plugin marketplace add ${CLAUDE_CRIT_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_CRIT_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_CRIT_PLUGIN}" "claude plugin update ${CLAUDE_CRIT_PLUGIN}"
}

#
# @description Keep the Claude Code Ponytail plugin at its recorded pin.
#
function update_claude_ponytail() {
    if ! has_command claude; then
        printf 'Skipping Claude Code Ponytail plugin: claude command not found.\n'
        return 0
    fi

    section "Claude Code Ponytail plugin"
    # Refreshed only once its identity is verified; converge_claude_step verifies again and reports and judges
    # any failure, so this call\'s own messages are not repeated.
    if ensure_claude_plugin_marketplace "${CLAUDE_PONYTAIL_PLUGIN}" 2> /dev/null; then
        claude_outside_projects plugin marketplace update "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" || true
    fi
    converge_claude_step "${CLAUDE_PONYTAIL_PLUGIN}" || return 0
    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
    record_claude_plugin_step "update_claude_ponytail" "${CLAUDE_PONYTAIL_PLUGIN}" "${AGENT_CLAUDE_DIR}/plugins/cache/ponytail/ponytail" "${AGENT_CLAUDE_DIR}/settings.json" -- "claude plugin marketplace add ${CLAUDE_PONYTAIL_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin update ${CLAUDE_PONYTAIL_PLUGIN}"
}

#
# @description The one parser of the Codex plugin copy Codex loads (pin_records.py codex-copy: Codex's own
#   choice among the cached versions, its plugin.json read strictly). It maps the reader's reply to exactly
#   `absent` or `copy <version>` with a version that is one strict component ([A-Za-z0-9][A-Za-z0-9._+-]*).
#   Every caller reads its output in a `case` whose default is an error, and only into a variable named
#   codex_copy; no caller reads the reader itself (the structural test checks all three).
# @arg $1 string Fully qualified Codex plugin ID.
# @exitcode 2 When the reader fails: the cache cannot be read, or its copy names another plugin or holds no
#   (or an empty) version.
# @exitcode 3 When the reader's reply is neither `absent` nor `copy <component>`.
#
function codex_plugin_copy() {
    local plugin="${1%@*}" marketplace="${1#*@}" reply

    reply="$(pin_record codex-copy "${AGENT_CODEX_DIR}/plugins/cache/${marketplace}/${plugin}" "${plugin}" \
        "${DOTFILES_REPO_SOURCE_DIR}/home/dot_codex/modify_private_config.toml")" || return 2
    case "${reply}" in
    absent) printf 'absent\n' ;;
    "copy "*)
        if [[ ${reply#copy } =~ ^[A-Za-z0-9][A-Za-z0-9._+-]*$ ]]; then
            printf '%s\n' "${reply}"
        else
            printf 'ERROR: the cached copy of %s holds no valid version: %q\n' "$1" "${reply}" >&2
            return 3
        fi
        ;;
    *)
        printf 'ERROR: unexpected cache state of %s: %q\n' "$1" "${reply}" >&2
        return 3
        ;;
    esac
}

#
# @description After a Codex plugin step, judge the copy it left cached by make doctor's own pin check
#   (doctor_pin_check), the one judge of a pin, so the two never disagree: a copy the doctor rejects, for the
#   version its manifest declares or for its content (content_sha256: every regular file of the copy except the
#   inert ones, inert being what the copy's manifest does not point at and Codex never loads by convention: a file
#   a manifest reference reaches, by filesystem identity, is pinned and the pin_records.py INERT globs apply only
#   to the files no reference reaches), is off its pin, whether the step
#   installed it or found it cached.
#   `codex plugin marketplace upgrade` rewrites the copy from upstream main (incident 2026-10-30), so a copy that
#   was there before is no more reviewed than a fresh one and takes the same outcome:
#   removed by converge_or_disable, a WARN, make doctor's drift until the review bump, not a run failure. The
#   commit the copy came from is not compared with the marketplace `ref`, which pins the catalog snapshot only.
# @arg $1 string Fully qualified Codex plugin ID.
# @exitcode 11 (PLUGIN_FRESH_OFF_PIN) When make doctor rejects the copy; converge_or_disable removes it.
# @exitcode 1 When the copy or the pin cannot be read, or the doctor's check cannot run (any status but its
#   0 or 1); never a pass.
#
function judge_codex_copy() {
    local plugin_id="$1" pin codex_copy check=0

    if ! pin="$(plugin_pin codex "${plugin_id}" pin)"; then
        printf 'Cannot read the pin of %s from %s.\n' "${plugin_id}" "${AGENT_PLUGIN_PINS}" >&2
        return 1
    fi
    if ! codex_copy="$(codex_plugin_copy "${plugin_id}")"; then
        printf 'ERROR: cannot read the cached copy of %s after installing it.\n' "${plugin_id}" >&2
        return 1
    fi
    case "${codex_copy}" in
    # Nothing installed (no catalog, no login): make doctor reports it as a warning only.
    absent) return 0 ;;
    "copy "?*) ;;
    *)
        printf 'ERROR: unexpected cache state of %s: %s\n' "${plugin_id}" "${codex_copy}" >&2
        return 1
        ;;
    esac
    doctor_pin_check codex "${plugin_id}" < /dev/null || check=$?
    case "${check}" in
    0) return 0 ;;
    1)
        printf 'WARN: codex plugin %s landed at %s and make doctor rejects that copy: version or content off the pin %s (its finding above names what differs); the pin needs a review bump: review that release and record its version and content_sha256 in assets.codex-plugins (home/dot_agents/agent-config.yaml).\n' "${plugin_id}" "${codex_copy#copy }" "${pin}" >&2
        return "${PLUGIN_FRESH_OFF_PIN}"
        ;;
    *)
        printf 'ERROR: make doctor'"'"'s pin check of codex plugin %s could not run (exit %s), so its copy at %s is unjudged.\n' "${plugin_id}" "${check}" "${codex_copy#copy }" >&2
        return 1
        ;;
    esac
}

#
# @description Install the Codex Superpowers plugin from the OpenAI-curated catalog when no copy is cached.
#   Only ever called through converge_or_disable. A catalog that is unavailable (no `codex login`) leaves it
#   missing, which make doctor reports as a warning only.
# @exitcode 1 When the cached copy cannot be read.
#
function install_codex_superpowers() {
    local codex_output codex_copy

    if ! codex_copy="$(codex_plugin_copy "${CODEX_SUPERPOWERS_PLUGIN}")"; then
        printf 'ERROR: cannot read the cached copy of %s.\n' "${CODEX_SUPERPOWERS_PLUGIN}" >&2
        return 1
    fi
    case "${codex_copy}" in
    absent) ;;
    "copy "?*)
        printf 'Codex Superpowers plugin is already installed.\n'
        return 0
        ;;
    *)
        printf 'ERROR: unexpected cache state of %s: %s\n' "${CODEX_SUPERPOWERS_PLUGIN}" "${codex_copy}" >&2
        return 1
        ;;
    esac
    if codex_output="$(codex plugin add "${CODEX_SUPERPOWERS_PLUGIN}" 2>&1)"; then
        if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
            printf '%s\n' "${codex_output}" >&2
        fi
        printf 'Codex Superpowers plugin installed.\n'
        judge_codex_copy "${CODEX_SUPERPOWERS_PLUGIN}"
    else
        if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
            printf '%s\n' "${codex_output}" >&2
        fi
        printf 'Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.\n'
        # shellcheck disable=SC2016 # Backticks are literal operator guidance.
        printf 'Run `codex login`, then `codex plugin add %s`.\n' "${CODEX_SUPERPOWERS_PLUGIN}"
    fi
}

#
# @description Keep the Codex Superpowers plugin at its recorded pin, or remove it (converge_or_disable).
#
function update_codex_superpowers() {
    if ! has_command codex; then
        printf 'Skipping Codex plugins: codex command not found.\n'
        return 0
    fi

    section "Codex plugins"
    converge_or_disable codex "${CODEX_SUPERPOWERS_PLUGIN}" install_codex_superpowers || return 0
    local plugin_version
    plugin_version="$(manifest_codex_plugin_version "${CODEX_SUPERPOWERS_PLUGIN}")" || return 1
    manifest_record "update_codex_superpowers" plugin "${plugin_version}" "${AGENT_CODEX_DIR}/.tmp/plugins/plugins/superpowers" "${AGENT_CODEX_DIR}/config.toml" -- "codex plugin add ${CODEX_SUPERPOWERS_PLUGIN}" ||
        record_claude_failure "recording update_codex_superpowers in the installed asset manifest"
}

#
# @description Ensure the Ponytail Codex plugin marketplace is configured at its reviewed catalog commit.
# @description
#   chezmoi apply writes `ref` into [marketplaces.ponytail] (rendered from assets.codex-plugins). That ref pins
#   the marketplace catalog snapshot only: `codex plugin marketplace upgrade` fetches the plugin copy from the
#   source the catalog names (upstream main for ponytail), whatever the ref says, so the copy is judged by the
#   version its manifest declares and by its content (content_sha256), by make doctor's check after each
#   update (judge_codex_copy) and at any time, never by the commit it came from. What a hook command may run is
#   pinned by the codex.hooks.state trusted_hash pins (the hooks.json command strings); every file of the copy
#   but the inert ones (READMEs, docs/, i18n/, images, upstream CI: what Codex never loads) is pinned by
#   content_sha256, instruction files (skills, AGENTS.md) included.
#
function ensure_codex_ponytail_marketplace() {
    local codex_config="${AGENT_CODEX_DIR%/}/config.toml"
    local ref recorded state

    if ! ref="$(plugin_pin codex "${CODEX_PONYTAIL_PLUGIN}" ref)" ||
        ! recorded="$(plugin_pin codex "${CODEX_PONYTAIL_PLUGIN}" marketplace)"; then
        printf 'Cannot read the marketplace pin of %s from %s.\n' "${CODEX_PONYTAIL_PLUGIN}" "${AGENT_PLUGIN_PINS}" >&2
        return 1
    fi
    # The source this script uses is the one the manifest pins (and the doctor checks), or nothing happens.
    if [ "${recorded}" != "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}" ]; then
        printf 'ERROR: %s pins %s from %s, not %s.\n' "${AGENT_PLUGIN_PINS}" "${CODEX_PONYTAIL_PLUGIN}" "${recorded}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}" >&2
        return 1
    fi
    # config.toml's [marketplaces.ponytail], read strictly: another source there is an error, not "absent".
    if ! state="$(pin_record codex-marketplace "${codex_config}" "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}")"; then
        printf 'Codex Ponytail marketplace exists with an unexpected source or an unreadable config; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
        return 1
    fi
    if [ "${state}" = "registered" ]; then
        return 0
    fi

    state=0
    codex_marketplace_has_source "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}" || state=$?
    case "${state}" in
    0) return 0 ;;
    1) ;;
    2)
        printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}" >&2
        return 1
        ;;
    *) return 1 ;;
    esac

    codex plugin marketplace add "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}" --ref "${ref}"
}

#
# @description Install the Codex Ponytail plugin from its marketplace at the reviewed catalog commit. Only ever
#   called through converge_or_disable. The marketplace upgrade itself installs or rewrites the copy of an
#   enabled plugin from the source the catalog names (upstream main), so the cache is read before it (a copy that
#   cannot be read stops the upgrade: it would install a copy nothing judges) and the copy is judged after it
#   (judge_codex_copy), whether it was cached before or not; `already installed` only says which.
# @exitcode 11 (PLUGIN_FRESH_OFF_PIN) When make doctor rejects the copy; converge_or_disable removes it.
# @exitcode 1 When the marketplace cannot be registered or is not pinned to the manifest's ref, the ref cannot
#   be read, or the cached copy cannot be read before or after the upgrade.
#
function install_codex_ponytail() {
    local ref pinned codex_copy cached_before

    if ! ensure_codex_ponytail_marketplace; then
        printf 'ERROR: the Codex Ponytail marketplace registration failed.\n' >&2
        return 1
    fi
    if ! ref="$(plugin_pin codex "${CODEX_PONYTAIL_PLUGIN}" ref)"; then
        printf 'ERROR: cannot read the pinned ref of %s.\n' "${CODEX_PONYTAIL_PLUGIN}" >&2
        return 1
    fi
    # An upgrade fetches the catalog [marketplaces.ponytail] names; without the manifest's ref there it would move
    # to the branch head. chezmoi apply writes the ref (the Codex modify script), so a missing or other ref stops here.
    pinned=0
    pin_record codex-marketplace-pinned "${AGENT_CODEX_DIR}/config.toml" "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}" "${ref}" || pinned=$?
    if [ "${pinned}" -ne 0 ]; then
        printf 'ERROR: [marketplaces.%s] in the Codex config is not pinned to %s; run chezmoi apply, then make update. The marketplace was not upgraded.\n' "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${ref}" >&2
        return 1
    fi
    # A read that fails is never "absent": the upgrade would then install a copy nothing judges.
    if ! codex_copy="$(codex_plugin_copy "${CODEX_PONYTAIL_PLUGIN}")"; then
        printf 'ERROR: cannot read the cached copy of %s under %s before upgrading its marketplace; nothing was upgraded.\n' "${CODEX_PONYTAIL_PLUGIN}" "${AGENT_CODEX_DIR}/plugins/cache/${CODEX_PONYTAIL_PLUGIN#*@}/${CODEX_PONYTAIL_PLUGIN%@*}" >&2
        return 1
    fi
    case "${codex_copy}" in
    absent) cached_before=0 ;;
    "copy "?*) cached_before=1 ;;
    *)
        printf 'ERROR: unexpected cache state of %s: %s\n' "${CODEX_PONYTAIL_PLUGIN}" "${codex_copy}" >&2
        return 1
        ;;
    esac
    codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}" || true

    if ! codex_copy="$(codex_plugin_copy "${CODEX_PONYTAIL_PLUGIN}")"; then
        printf 'ERROR: cannot read the cached copy of %s after upgrading its marketplace.\n' "${CODEX_PONYTAIL_PLUGIN}" >&2
        return 1
    fi
    case "${codex_copy}" in
    absent) codex plugin add "${CODEX_PONYTAIL_PLUGIN}" || true ;;
    "copy "?*)
        if [ "${cached_before}" -eq 1 ]; then
            printf 'Codex Ponytail plugin is already installed.\n'
        else
            printf 'Codex Ponytail plugin was installed by the marketplace upgrade.\n'
        fi
        ;;
    *)
        printf 'ERROR: unexpected cache state of %s: %s\n' "${CODEX_PONYTAIL_PLUGIN}" "${codex_copy}" >&2
        return 1
        ;;
    esac
    judge_codex_copy "${CODEX_PONYTAIL_PLUGIN}"
}

#
# @description Keep the Codex Ponytail plugin at its recorded pin, or remove it (converge_or_disable).
#
function update_codex_ponytail() {
    local ref

    if ! has_command codex; then
        printf 'Skipping Codex Ponytail plugin: codex command not found.\n'
        return 0
    fi

    section "Codex Ponytail plugin"
    converge_or_disable codex "${CODEX_PONYTAIL_PLUGIN}" install_codex_ponytail || return 0
    printf 'Ponytail lifecycle hooks are trusted only at their reviewed trusted_hash pins; the Codex config refresh at the end of this run applies them.\n'
    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
    if ! ref="$(plugin_pin codex "${CODEX_PONYTAIL_PLUGIN}" ref)"; then
        record_claude_failure "reading the pinned ref of ${CODEX_PONYTAIL_PLUGIN}"
        return 0
    fi
    local plugin_version
    plugin_version="$(manifest_codex_plugin_version "${CODEX_PONYTAIL_PLUGIN}")" || return 1
    manifest_record "update_codex_ponytail" plugin "${plugin_version}" "${AGENT_CODEX_DIR}/plugins/cache/ponytail/ponytail" "${AGENT_CODEX_DIR}/config.toml" -- "codex plugin marketplace add ${CODEX_PONYTAIL_MARKETPLACE_SOURCE} --ref ${ref}" "codex plugin marketplace upgrade ${CODEX_PONYTAIL_MARKETPLACE_NAME}" "codex plugin add ${CODEX_PONYTAIL_PLUGIN}" ||
        record_claude_failure "recording update_codex_ponytail in the installed asset manifest"
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
    # A crit that cannot print its version is recorded with an empty version, as before.
    local crit_output plugin_version
    crit_output="$(crit --version 2> /dev/null)" || crit_output=""
    plugin_version="$(awk 'NR == 1 { print $2 }' <<< "${crit_output}")" || return 1
    manifest_record "update_codex_crit" plugin "${plugin_version}" "${AGENT_CODEX_DIR}/plugins/crit" "${AGENT_CODEX_DIR}/config.toml" "${HOME}/.agents/skills/crit" "${HOME}/.agents/skills/crit-cli" "${HOME}/.agents/skills/crit-story" -- "ensure_crit_cli" "crit install codex-plugin --force" ||
        record_claude_failure "recording update_codex_crit in the installed asset manifest"
}

#
# @description Return success when the zenbu-labs installers support this platform.
# @description
#   Upstream publishes darwin-arm64, linux-x64, and linux-arm64 builds only;
#   Intel macOS has no release asset, so it is skipped rather than failed.
# @arg $1 string Kernel name (`uname -s`).
# @arg $2 string Machine (`uname -m`).
#
function zenbu_platform_supported() {
    case "$1-$2" in
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
    curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${url}" -o "${installer}" || {
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
    local installed kernel machine platform

    platform="$(uname_platform)" || return 1
    read -r kernel machine <<< "${platform}"
    zenbu_platform_supported "${kernel}" "${machine}" || {
        printf 'Skipping terminal-code: unsupported platform %s %s.\n' "${kernel}" "${machine}"
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
    manifest_record "update_terminal_code" installer "${TERMINAL_CODE_PIN_VERSION}" "${HOME}/.local/lib/tode" "${HOME}/.local/bin/tode" "${HOME}/.local/state/tode/install.json" -- "curl -fsSL ${TERMINAL_CODE_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer>" ||
        record_claude_failure "recording update_terminal_code in the installed asset manifest"
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
    local installed kernel machine platform

    platform="$(uname_platform)" || return 1
    read -r kernel machine <<< "${platform}"
    zenbu_platform_supported "${kernel}" "${machine}" || {
        printf 'Skipping terminal-browser: unsupported platform %s %s.\n' "${kernel}" "${machine}"
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
    manifest_record "update_terminal_browser" installer "${TERMINAL_BROWSER_PIN_VERSION}" "${HOME}/.local/share/terminal-browser/app" "${HOME}/.local/bin/terminal-browser" "${HOME}/.local/state/terminal-browser/skills.links" -- "curl -fsSL ${TERMINAL_BROWSER_INSTALLER_URL}" "shasum -a 256 <installer>" "TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 bash <installer>" ||
        record_claude_failure "recording update_terminal_browser in the installed asset manifest"
}

#
# @description Resolve path segments lexically as Node's path.resolve does, which npm applies to a bin link and to its
#   prefix before its ownership check (bin-links check-bin): an absolute segment restarts the path, empty and `.`
#   segments drop, and `..` drops its parent.
# @arg $@ path Segments, the first one absolute.
# @stdout The resolved path.
#
function normalize_node_path() {
    local segment part resolved=""
    local -a parts=()
    for segment in "$@"; do
        [ -z "${segment}" ] || [ -n "${segment%%/*}" ] || resolved="" # an absolute segment starts with its separator
        IFS=/ read -ra parts <<< "${segment}"
        for part in ${parts[@]+"${parts[@]}"}; do # empty for ""; bash before 4.4 calls "${parts[@]}" unbound then
            case "${part}" in
            "" | .) ;;
            ..) resolved="${resolved%/*}" ;;
            *) resolved="${resolved}/${part}" ;;
            esac
        done
    done
    printf '%s\n' "${resolved:-/}"
}

#
# @description Verify the pinned omp tarball before npm installs it.
# @exitcode 1 The download checksum or installed version differs from its pin.
#
function update_omp() (
    local installed download_dir tarball actual entry="${HOME}/.local/bin/omp" aside="" link resolved package_dir
    has_command npm || {
        printf 'Skipping omp: npm command not found.\n'
        return 0
    }
    section "omp"
    installed="$("${HOME}/.local/bin/omp" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
    installed="${installed#omp/}"
    if [ "${installed}" = "${OMP_PIN_VERSION}" ]; then
        printf 'omp %s is already installed.\n' "${installed}"
        return 0
    fi
    download_dir="$(mktemp -d "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX")" || return
    trap 'rm -rf "${download_dir}"' EXIT
    tarball="${download_dir}/omp-${OMP_PIN_VERSION}.tgz"
    curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${OMP_TARBALL_URL}" -o "${tarball}" || return
    actual="$(shasum -a 256 "${tarball}" | awk '{ print $1 }')" || return
    if [ "${actual}" != "${OMP_TARBALL_SHA256}" ]; then
        printf 'omp checksum mismatch: expected %s, got %s.\n' "${OMP_TARBALL_SHA256}" "${actual}" >&2
        return 1
    fi
    # npm refuses with EEXIST to replace a bin entry it does not own, so a standalone file or a link outside this
    # prefix's package (a mise or manual install, a dangling link included) moves to a kept path, and comes back when
    # the install fails; a directory stays for npm to judge.
    # npm resolves the link against the bin directory, and its prefix, before its ownership check (bin-links check-bin),
    # so both fold here too, and a target that leaves this prefix's package is not npm's own (the Bot's 4307029052).
    link="$(readlink "${entry}")" || link=""
    resolved="$(normalize_node_path "${entry%/*}" "${link}")" || return
    package_dir="$(normalize_node_path "${HOME}/.local/lib/node_modules/@oh-my-pi/pi-coding-agent")" || return
    if { [ -f "${entry}" ] || [ -L "${entry}" ]; } &&
        [[ "${resolved}" != "${package_dir}/"* ]]; then # lint-comparisons: allow both sides are normalize_node_path forms
        aside="${HOME}/.local/share/agent-assets/omp/omp.previous"
        printf 'Moving %s to %s: npm does not own it%s.\n' "${entry}" "${aside}" "${link:+ (it points to ${link} and resolves to ${resolved})}"
        mkdir -p "${aside%/*}" && assert_asset_destination "${aside}" && rm -rf "${aside}" && mv "${entry}" "${aside}" || return
    fi
    # The verified local tarball has no registry release date, so npm's min-release-age (~/.npmrc, three days)
    # applies only to the dependencies it resolves: none newer than the cooldown, as for every other install.
    npm install -g --prefix "${HOME}/.local" "${tarball}" &&
        installed="$("${entry}" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
    installed="${installed#omp/}"
    if [ "${installed}" != "${OMP_PIN_VERSION}" ]; then
        [ -z "${aside}" ] || { rm -f "${entry}" && mv "${aside}" "${entry}" && printf 'Put the previous %s back.\n' "${entry}"; }
        printf 'omp version mismatch: expected %s, got %s.\n' "${OMP_PIN_VERSION}" "${installed}" >&2
        return 1
    fi
    manifest_record "update_omp" installer "${OMP_PIN_VERSION}" "${HOME}/.local/bin/omp" -- "npm install -g --prefix ${HOME}/.local <verified-omp-tarball>"
)

#
# @description Verify the pinned platform wheel before uv installs hcom, and keep it where uv's receipt points.
# @exitcode 1 The download checksum or installed version differs from its pin.
#
function update_hcom() (
    local url expected installed download_dir wheel actual wheel_dir kernel machine platform
    platform="$(uname_platform)" || return 1
    read -r kernel machine <<< "${platform}"
    case "${kernel}-${machine}" in
    Darwin-arm64 | Darwin-aarch64) url="${HCOM_DARWIN_ARM64_URL}" expected="${HCOM_DARWIN_ARM64_SHA256}" ;;
    Darwin-x86_64 | Darwin-amd64) url="${HCOM_DARWIN_AMD64_URL}" expected="${HCOM_DARWIN_AMD64_SHA256}" ;;
    Linux-x86_64 | Linux-amd64) url="${HCOM_LINUX_AMD64_URL}" expected="${HCOM_LINUX_AMD64_SHA256}" ;;
    Linux-aarch64 | Linux-arm64) url="${HCOM_LINUX_ARM64_URL}" expected="${HCOM_LINUX_ARM64_SHA256}" ;;
    *)
        printf 'Skipping hcom: unsupported platform %s %s.\n' "${kernel}" "${machine}"
        return 0
        ;;
    esac
    has_command uv || {
        printf 'Skipping hcom: uv command not found.\n'
        return 0
    }
    section "hcom"
    # uv's receipt records the wheel's path as hcom's source and `uv tool upgrade` re-reads it, so the verified wheel
    # lives at a managed path that outlives the run.
    wheel_dir="${HOME}/.local/share/agent-assets/hcom"
    installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
    # A pinned install without the retained wheel (one from before the wheel was kept) is reinstalled to repair it.
    if [ "${installed}" = "${HCOM_PIN_VERSION}" ] && [ -f "${wheel_dir}/${url##*/}" ]; then
        printf 'hcom %s is already installed.\n' "${installed}"
        return 0
    fi
    download_dir="$(mktemp -d "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX")" || return
    trap 'rm -rf "${download_dir}"' EXIT
    wheel="${download_dir}/${url##*/}"
    curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${url}" -o "${wheel}" || return
    actual="$(shasum -a 256 "${wheel}" | awk '{ print $1 }')" || return
    if [ "${actual}" != "${expected}" ]; then
        printf 'hcom checksum mismatch: expected %s, got %s.\n' "${expected}" "${actual}" >&2
        return 1
    fi
    mkdir -p "${wheel_dir}" && mv -f "${wheel}" "${wheel_dir}/" || return
    wheel="${wheel_dir}/${url##*/}"
    # A failed install drops the retained wheel, so the next run retries instead of skipping on it (4303338055).
    uv tool install --force "${wheel}" || {
        rm -f "${wheel}"
        return 1
    }
    installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
    if [ "${installed}" != "${HCOM_PIN_VERSION}" ]; then
        printf 'hcom version mismatch: expected %s, got %s.\n' "${HCOM_PIN_VERSION}" "${installed}" >&2
        return 1
    fi
    manifest_record "update_hcom" installer "${HCOM_PIN_VERSION}" "${HOME}/.local/bin/hcom" "${wheel}" -- "uv tool install --force <verified-hcom-wheel>"
)

#
# @description Print the inputs an installed pi-claude-bridge must match: the pinned tarball's sha256, then one
#   line per patch in application order, then bun.lock. The install writes these lines as the head of its RECEIPT.
# @stdout One `<file name> <sha256>` line per input.
# @exitcode 1 A patch or the lockfile is missing from home/dot_agents/assets/pi-claude-bridge.
#
function pi_claude_bridge_inputs() {
    local file sum
    printf 'pi-claude-bridge-%s.tgz %s\n' "${PI_CLAUDE_BRIDGE_PIN_VERSION}" "${PI_CLAUDE_BRIDGE_TARBALL_SHA256}"
    for file in "${PI_CLAUDE_BRIDGE_ASSET_DIR}"/patches/*.patch "${PI_CLAUDE_BRIDGE_ASSET_DIR}/bun.lock"; do
        [ -f "${file}" ] || {
            printf 'pi-claude-bridge asset file missing: %s\n' "${file}" >&2
            return 1
        }
        sum="$(shasum -a 256 "${file}")" || {
            printf 'shasum -a 256 could not hash %s; the pi-claude-bridge inputs are unknown\n' "${file}" >&2
            return 1
        }
        printf '%s %s\n' "${file##*/}" "${sum%% *}"
    done
}

#
# @description Install the pinned pi-claude-bridge tarball with this repository's patches and locked dependencies
#   as an omp extension directory, loaded with `omp -e <install dir>` (plan 025 decisions 30, 37, 38).
# @description
#   The tarball is verified against its reviewed sha256, the patches under
#   home/dot_agents/assets/pi-claude-bridge/patches apply in name order, Bun installs the dependency set the
#   committed bun.lock pins (peers excluded: omp's legacy pi compat layer provides them), and gap-check.ts refuses
#   a tree whose legacy pi imports omp's shims do not export, so an omp upgrade that drops one fails here instead
#   of in the first session. The staged tree replaces the install directory only after every check passes, and
#   a run whose RECEIPT already matches the pinned inputs changes nothing.
# @exitcode 1 A checksum, patch, dependency install or import check failed; the existing install is unchanged.
#
function update_pi_claude_bridge() (
    local install_dir="${HOME}/.local/lib/omp-extensions/pi-claude-bridge"
    local omp_dir="${HOME}/.local/lib/node_modules/@oh-my-pi/pi-coding-agent"
    local inputs receipt download_dir tarball actual staging="" patch_file previous
    has_command bun || {
        printf 'Skipping pi-claude-bridge: bun command not found.\n'
        return 0
    }
    [ -d "${omp_dir}" ] || {
        printf 'Skipping pi-claude-bridge: omp is not installed at %s.\n' "${omp_dir}"
        return 0
    }
    section "pi-claude-bridge"
    inputs="$(pi_claude_bridge_inputs)" || return
    # No readable RECEIPT is no match: the verified install runs again and writes it.
    receipt="$(sed -n '1,/^bun.lock /p' "${install_dir}/RECEIPT" 2> /dev/null)" || receipt=""
    if [ -d "${install_dir}/node_modules/@anthropic-ai/claude-agent-sdk" ] &&
        [ "${receipt}" = "${inputs}" ]; then
        printf 'pi-claude-bridge %s is already installed.\n' "${PI_CLAUDE_BRIDGE_PIN_VERSION}"
    else
        download_dir="$(mktemp -d "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX")" || return
        trap 'rm -rf "${download_dir}" ${staging:+"${staging}"}' EXIT
        tarball="${download_dir}/pi-claude-bridge-${PI_CLAUDE_BRIDGE_PIN_VERSION}.tgz"
        curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${PI_CLAUDE_BRIDGE_TARBALL_URL}" \
            -o "${tarball}" || return
        actual="$(shasum -a 256 "${tarball}" | awk '{ print $1 }')" || return
        if [ "${actual}" != "${PI_CLAUDE_BRIDGE_TARBALL_SHA256}" ]; then
            printf 'pi-claude-bridge checksum mismatch: expected %s, got %s.\n' "${PI_CLAUDE_BRIDGE_TARBALL_SHA256}" "${actual}" >&2
            return 1
        fi
        # Staged beside the target so the final rename stays on one filesystem.
        mkdir -p "${install_dir%/*}" || return
        assert_asset_destination "${install_dir}" || return 1
        staging="$(mktemp -d "${install_dir}.staging.XXXXXX")" || return
        tar xzf "${tarball}" -C "${staging}" --strip-components=1 || return
        for patch_file in "${PI_CLAUDE_BRIDGE_ASSET_DIR}"/patches/*.patch; do
            # -F0: GNU patch would apply a patch whose context drifted with fuzz and exit 0; Apple patch refuses either way.
            patch -p1 -s -F0 -d "${staging}" -i "${patch_file}" || {
                printf 'pi-claude-bridge patch %s did not apply.\n' "${patch_file##*/}" >&2
                return 1
            }
        done
        cp "${PI_CLAUDE_BRIDGE_ASSET_DIR}/bun.lock" "${staging}/bun.lock" || return
        (cd "${staging}" && bun install --production --omit=peer --frozen-lockfile) || return
        bun run "${PI_CLAUDE_BRIDGE_ASSET_DIR}/gap-check.ts" "${staging}/src" "${omp_dir}" || {
            printf 'pi-claude-bridge imports a name omp does not export (rows above); install refused.\n' >&2
            return 1
        }
        {
            printf '%s\n' "${inputs}"
            jq -r '"\(.name) \(.version)"' "${staging}"/node_modules/@anthropic-ai/*/package.json | LC_ALL=C sort
        } > "${staging}/RECEIPT" || return
        previous="${install_dir}.previous"
        rm -rf "${previous}"
        if [ -e "${install_dir}" ]; then
            mv "${install_dir}" "${previous}" || return
        fi
        mv "${staging}" "${install_dir}" || {
            [ ! -e "${previous}" ] || mv "${previous}" "${install_dir}"
            return 1
        }
        staging=""
        rm -rf "${previous}"
        printf 'pi-claude-bridge %s installed into %s.\n' "${PI_CLAUDE_BRIDGE_PIN_VERSION}" "${install_dir}"
        cat "${install_dir}/RECEIPT"
    fi
    manifest_record "update_pi_claude_bridge" installer "${PI_CLAUDE_BRIDGE_PIN_VERSION}" "${install_dir}" "${install_dir}/RECEIPT" "${install_dir}/node_modules/@anthropic-ai/claude-agent-sdk" -- "curl -fsSL ${PI_CLAUDE_BRIDGE_TARBALL_URL}" "shasum -a 256 <tarball>" "patch -p1 -F0 -d <staging> -i <each home/dot_agents/assets/pi-claude-bridge/patches/*.patch in order>" "bun install --production --omit=peer --frozen-lockfile" "bun run gap-check.ts <staging>/src ${omp_dir}"
)

#
# @description Install the pinned cloudflare/security-audit-skill tree as the shared skill
#   ~/.agents/skills/security-audit (assets.security-audit-skill), the sweep the AGENTS.md "Audit" section names for
#   the omp worker seat (skills.audience gives it to omp-worker alone).
# @description
#   GitHub's source archive of the pinned commit (never the branch head, never the npx skills installer) is downloaded into a
#   mktemp directory under TMPDIR and verified against its reviewed sha256 before anything is unpacked; the
#   skills/security-audit subtree alone is unpacked beside the install path and replaces it with one rename, so a
#   failed download, digest check or unpack leaves the previous tree as it was. A download that fails or cannot run
#   (offline, no download tool on PATH) degrades and continues like update_terminal_code: one WARN line naming the
#   step, nothing installed, nothing recorded, and make update goes on (the next run retries). A digest mismatch or an
#   archive without skills/security-audit/SKILL.md is a hard failure of the step: fail closed on a tampered archive. A
#   tree whose manifest record already names the pinned commit is skipped. The record names the install path: make
#   doctor reads it, and the doctor's installer_owned_skill_names (scripts/check-agent-runtime.py) keeps the tree out
#   of the unmanaged-skill WARN.
# @exitcode 0 Installed, already installed, or the download failed (a WARN; nothing installed or recorded).
# @exitcode 1 The digest check, the unpack, the archive shape or the rename failed; the existing install is unchanged.
#
function update_security_audit_skill() (
    local install_dir="${HOME}/.agents/skills/security-audit"
    local recorded download_dir tarball actual staging="" previous
    section "security-audit skill"
    # A record that cannot be read is no record: the verified install runs again and writes it.
    recorded="$(jq -r '.steps["update_security_audit_skill"].source_version // empty' "${HOME}/.agents/.installed-manifest.json" 2> /dev/null)" || recorded=""
    if [ "${recorded}" = "${SECURITY_AUDIT_SKILL_COMMIT}" ] && [ -f "${install_dir}/SKILL.md" ]; then
        printf 'security-audit skill %s is already installed.\n' "${SECURITY_AUDIT_SKILL_COMMIT}"
        return 0
    fi
    download_dir="$(mktemp -d "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX")" || return
    trap 'rm -rf "${download_dir}" ${staging:+"${staging}"}' EXIT
    tarball="${download_dir}/security-audit-skill-${SECURITY_AUDIT_SKILL_COMMIT}.tar.gz"
    curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${SECURITY_AUDIT_SKILL_ARCHIVE_URL}" -o "${tarball}" || {
        printf 'WARN: update_security_audit_skill: the security-audit skill archive could not be downloaded (%s); nothing installed, nothing recorded; the existing install is unchanged and the next make update retries.\n' "${SECURITY_AUDIT_SKILL_ARCHIVE_URL}" >&2
        return 0
    }
    actual="$(shasum -a 256 "${tarball}" | awk '{ print $1 }')" || return
    if [ "${actual}" != "${SECURITY_AUDIT_SKILL_SHA256}" ]; then
        printf 'security-audit skill checksum mismatch: expected %s, got %s.\n' "${SECURITY_AUDIT_SKILL_SHA256}" "${actual}" >&2
        return 1
    fi
    # Staged beside the target so the final rename stays on one filesystem; the three leading components
    # (<repository>-<commit>/skills/security-audit) are stripped so the skill tree lands at the install path itself.
    mkdir -p "${install_dir%/*}" || return
    assert_asset_destination "${install_dir}" || return 1
    staging="$(mktemp -d "${install_dir}.staging.XXXXXX")" || return
    tar xzf "${tarball}" -C "${staging}" --strip-components=3 "security-audit-skill-${SECURITY_AUDIT_SKILL_COMMIT}/skills/security-audit" || return
    [ -f "${staging}/SKILL.md" ] || {
        printf 'security-audit skill archive holds no skills/security-audit/SKILL.md; install refused.\n' >&2
        return 1
    }
    previous="${install_dir}.previous"
    rm -rf "${previous}"
    if [ -e "${install_dir}" ]; then
        mv "${install_dir}" "${previous}" || return
    fi
    mv "${staging}" "${install_dir}" || {
        [ ! -e "${previous}" ] || mv "${previous}" "${install_dir}"
        return 1
    }
    staging=""
    rm -rf "${previous}"
    printf 'security-audit skill %s installed into %s.\n' "${SECURITY_AUDIT_SKILL_COMMIT}" "${install_dir}"
    manifest_record "update_security_audit_skill" installer "${SECURITY_AUDIT_SKILL_COMMIT}" "${install_dir}" "${install_dir}/SKILL.md" -- "curl -fsSL ${SECURITY_AUDIT_SKILL_ARCHIVE_URL}" "shasum -a 256 <archive>" "tar xzf <archive> -C <staging> --strip-components=3 security-audit-skill-${SECURITY_AUDIT_SKILL_COMMIT}/skills/security-audit" "mv <staging> ${install_dir}"
)

#
# @description Remove the older DeepSeek harness trees under $1/dsh once the install current names is recorded.
# @description
#   A directory goes only when all hold: its name is one of the two shapes this step or its earlier layout made
#   (dsh-v* for <tag>, <tag>.XXXXXX, <tag>.previous and <tag>.failed; .staging.* for the earlier staging tree), it is
#   a directory and not a symlink, and it is not the inode of current's target (-ef). No path is resolved here:
#   update_deepseek_harness refuses, before any download, every current whose target is not a non-symlink directory
#   directly under dsh/, so by the time the prune runs the active tree is one direct child of dsh/ and no directory
#   the link traverses exists to protect; the one inode comparison tells it from every candidate. Any other name
#   under dsh/ is not the step's and stays. The prune runs after a successful record and on the already-installed
#   path, so a removal that failed once is retried by the next make update.
#   This helper owns one row of update_deepseek_harness's input table, the entries under dsh/: it compares identity
#   by inode, never by text, and repairs nothing.
# @arg $1 string DSH_HOME.
# @stderr One WARN line when a removal fails (the next make update prunes again).
# @exitcode 0 Always; the prune never fails the step whose install is already recorded.
#
function dsh_prune_older() {
    local dsh_home="$1" older
    for older in "${dsh_home}/dsh"/*/ "${dsh_home}/dsh"/.*/; do
        older="${older%/}"
        case ${older##*/} in
        dsh-v* | .staging.*) ;;
        *) continue ;;
        esac
        if [ ! -d "${older}" ] || [ -L "${older}" ] || [ "${older}" -ef "${dsh_home}/dsh/current" ]; then
            continue
        fi
        rm -rf "${older}" || printf 'WARN: update_deepseek_harness: the older tree %s could not be removed; the next make update prunes again.\n' "${older}" >&2
    done
}

#
# @description Run one command of the DeepSeek harness step inside srt (regime-cutover U322). The upstream tag's install
#   and build scripts and the profile's plugin install are the only upstream code `make update` executes, and each
#   runs under `srt --settings <file>` whose settings this function writes: writes land under the build directory and
#   the pnpm store or fail with srt's EPERM, reads of the credential roots fail, and the network reaches the hosts the
#   caller names and nothing else (no wildcard, no local binding, no nested user namespace, no pty). The form is
#   update_dsh_superagent's build on PR 711 (U317b), whose next round adopts this function.
# @description
#   Every producer is read with its status (standing order 21): `type -P srt` (the kit pins
#   npm:@anthropic-ai/sandbox-runtime in home/dot_mise/config.toml; it is on PATH under mise), `mise which pnpm` and
#   `mise which node` under MISE_EXEC_AUTO_INSTALL=false (nothing is installed on the step's behalf, verdicts/U276b),
#   pwd -P of HOME, of /tmp, of /private/tmp where it is a directory, of the directory and of the store,
#   resolve_dotfiles_source_dir and `git rev-parse --git-common-dir` for the checkout's git directories, and srt's own
#   exit. The settings file is created here
#   (umask 077, noclobber) at a path that holds nothing and is not a link, and is removed after the run; a path that
#   exists is refused, never reused. The read denies are the rows hcom-seat's dsh role denies for every seat
#   (seat_settings_render, by the same spellings, physical): ~/.ssh, ~/.gnupg, ~/.aws, ~/.netrc, ~/.docker, ~/.kube,
#   ~/.config/gcloud, ~/.config/gh, ~/.codex, ~/.omp/agent, ~/.omp/profiles, ~/.hcom, ~/.local/state/hcom, the chezmoi
#   sources, ~/Workspace, ~/.local/state/omp-seats, ~/.claude and ~/.claude.json, then the dotfiles checkout and its git
#   common directory. The write denies are the paths srt 0.0.81 grants on its own when `denyWrite` is empty
#   (sandbox-utils.js SANDBOX_OWN_WRITE_PATHS and HOME_CONVENIENCE_WRITE_DIRS; hcom-seat names the same three as
#   `srt_tmp_roots` and `~/.npm/_logs`): `/tmp/claude`, its pwd -P spelling where /tmp is a link (macOS:
#   `/private/tmp/claude`), srt's second literal `/private/tmp/claude` wherever `/private/tmp` is a directory (a Linux
#   host that has one; U322d), each once, and `~/.npm/_logs` in HOME's pwd -P form (regime-cutover U322b;
#   `~/.claude/debug`, the fourth, srt drops itself under the `~/.claude` read deny). Every path in the settings is
#   clean (components of [A-Za-z0-9._@+-], none . or .., no
#   trailing slash: srt reads a settings path as a pattern) and every host matches [A-Za-z0-9.-]; the JSON is written
#   by the shell and no JSON tool runs.
# @description
#   The environment is sanitised outside srt and completed inside (U322b): `/usr/bin/env -i` starts srt from HOME, a
#   PATH of the mise pnpm and node directories and the system directories, DSH_HOME, and the variables that point every
#   cache and log of the tools inside the two write roots (TMPDIR and CLAUDE_CODE_TMPDIR, which srt 0.0.81 reads as the
#   TMPDIR it hands its child, at <store>/tmpdir; the XDG directories, pnpm's cache-dir and state-dir, npm's cache and
#   logs-dir under the store; the store itself as npm_config_store_dir; pnpm's self-install off). srt 0.0.81 runs its
#   child from its own environment plus what it injects (SANDBOX_RUNTIME, TMPDIR, HTTP_PROXY, HTTPS_PROXY and their
#   lower-case forms, NO_PROXY), and its sandbox reaches the network through that proxy alone, so nothing between srt
#   and the command may drop them: the command follows `--` as it was given, and a leading NAME=value word is read by
#   the `bash -c` srt re-parses its argv with. No variable of the caller (a credential, a profile, a token) reaches srt
#   or the build.
# @arg $1 path The directory the command runs in and may write: a directory of this user that is not a symlink.
# @arg $2 path The settings file to write: absent and not a link; created 0600 and removed after the run.
# @arg $@ string The hosts the command may reach (none for a command that needs no network), then `--`, then the
#   command and its arguments.
# @env DSH_HOME The opt-in directory; ${DSH_HOME}/.pnpm-store is the second write root, made here when absent.
# @stdout The command's.
# @exitcode 1 A producer, a check or the settings write refused before the run; the line names it.
# @exitcode * The command's exit status under srt, passed through.
#
function build_under_srt() {
    local dir="$1" settings="$2" hosts=() host srt pnpm_bin node_bin home_real tmp_real tmp_second tmp_second_real='' dir_real store store_real source_root source_real common common_real path row spelling spellings=() deny=() deny_write=() write_json='' deny_json='' deny_write_json='' hosts_json='' json status=0
    shift 2
    while [ $# -gt 0 ] && [ "$1" != -- ]; do
        hosts+=("$1")
        shift
    done
    if [ $# -lt 2 ]; then
        printf 'build_under_srt: no command after --; nothing run.\n' >&2
        return 1
    fi
    shift
    if [ -z "${DSH_HOME:-}" ]; then
        printf 'build_under_srt: DSH_HOME is unset, so the pnpm store has no place; nothing run.\n' >&2
        return 1
    fi
    case ${DSH_HOME} in # lint-comparisons: allow the case reads the spelling (absolute or not); the step compared the identity
    /*) ;;
    *)
        printf 'build_under_srt: DSH_HOME must be an absolute path (%s given); nothing run.\n' "${DSH_HOME}" >&2
        return 1
        ;;
    esac
    # The containment first: no srt is no run. The kit pins it; the refusal names the pin.
    srt="$(type -P srt)" || {
        printf 'build_under_srt: srt is absent from PATH (the kit pins npm:@anthropic-ai/sandbox-runtime 0.0.81 in home/dot_mise/config.toml; run mise install and rerun make update); nothing run.\n' >&2
        return 1
    }
    if [ ! -f "${srt}" ] || [ ! -x "${srt}" ]; then
        printf 'build_under_srt: %s (srt on PATH) is not an executable file; nothing run.\n' "${srt}" >&2
        return 1
    fi
    pnpm_bin="$(MISE_EXEC_AUTO_INSTALL=false mise which pnpm 2> /dev/null)" || {
        printf 'build_under_srt: pnpm is absent (mise which pnpm failed; the kit pins it in home/dot_mise/config.toml, so run mise install and rerun make update); nothing run.\n' >&2
        return 1
    }
    node_bin="$(MISE_EXEC_AUTO_INSTALL=false mise which node 2> /dev/null)" || {
        printf 'build_under_srt: node is absent (mise which node failed; the kit pins it in home/dot_mise/config.toml, so run mise install and rerun make update); nothing run.\n' >&2
        return 1
    }
    for path in "${pnpm_bin}" "${node_bin}"; do
        case ${path} in # lint-comparisons: allow the case reads the spelling (absolute or not), the file tests below read the entry
        /*) ;;
        *)
            printf 'build_under_srt: mise which answered %s, not an absolute path; nothing run.\n' "${path}" >&2
            return 1
            ;;
        esac
        if [ ! -f "${path}" ] || [ ! -x "${path}" ]; then
            printf 'build_under_srt: %s (mise which) is not an executable file; nothing run.\n' "${path}" >&2
            return 1
        fi
    done
    home_real="$(cd "${HOME}" && pwd -P)" || {
        printf 'build_under_srt: the physical path of HOME %s could not be read; nothing run.\n' "${HOME}" >&2
        return 1
    }
    # srt 0.0.81's own temporary root is the one `/tmp` word of this file (test_sandbox_portability's ALLOWED_TMP names
    # it); its parent is resolved for the deny below, so that where /tmp is a link (macOS: /private/tmp) the spelling
    # the kernel sees is denied as well. `~/.npm/_logs` takes HOME's physical path.
    deny_write=(/tmp/claude)
    tmp_real="$(cd "${deny_write[0]%/*}" && pwd -P)" || {
        printf 'build_under_srt: the physical path of %s could not be read, which the deny of srt'\''s own %s needs; nothing run.\n' "${deny_write[0]%/*}" "${deny_write[0]}" >&2
        return 1
    }
    # srt's second literal spelling of that root is `/private` before the same word (SANDBOX_OWN_WRITE_PATHS), granted
    # wherever it exists: on macOS it is the physical /tmp read above; on a Linux host that has a /private/tmp
    # directory it is a third root unless denied (verdicts/U322c P1 :1940). Where the directory exists, its physical
    # path is read as well and both spellings join the deny below. The predicate is spelled `test` so that the module's
    # tests can stand a Linux host's answer in for this host's (a function shadows `test`; bash 3.2 crashes on one
    # that shadows `[`).
    tmp_second="/private${deny_write[0]%/*}"
    if test -d "${tmp_second}"; then
        tmp_second_real="$(cd "${tmp_second}" && pwd -P)" || {
            printf 'build_under_srt: the physical path of %s could not be read, which the deny of srt'\''s own %s/claude needs; nothing run.\n' "${tmp_second}" "${tmp_second}" >&2
            return 1
        }
    fi
    if [ -L "${dir}" ] || [ ! -d "${dir}" ] || [ ! -O "${dir}" ]; then
        printf 'build_under_srt: %s is not a directory of this user, or is a symlink; nothing run.\n' "${dir}" >&2
        return 1
    fi
    dir_real="$(cd "${dir}" && pwd -P)" || {
        printf 'build_under_srt: the physical path of %s could not be read; nothing run.\n' "${dir}" >&2
        return 1
    }
    # srt on Linux grants writes only to paths that exist, so the store and the TMPDIR inside it are made first.
    store="${DSH_HOME}/.pnpm-store"
    if [ -L "${store}" ] || { [ -e "${store}" ] && [ ! -d "${store}" ]; }; then
        printf 'build_under_srt: %s is a symlink or not a directory; the step writes the pnpm store only in a directory of its own there (move it aside and rerun make update); nothing run.\n' "${store}" >&2
        return 1
    fi
    mkdir -p "${store}/tmpdir" || {
        printf 'build_under_srt: the pnpm store %s could not be made; nothing run.\n' "${store}" >&2
        return 1
    }
    store_real="$(cd "${store}" && pwd -P)" || {
        printf 'build_under_srt: the physical path of %s could not be read; nothing run.\n' "${store}" >&2
        return 1
    }
    source_root="$(resolve_dotfiles_source_dir)" || {
        printf 'build_under_srt: the dotfiles checkout could not be resolved, so its git directories cannot be denied; nothing run.\n' >&2
        return 1
    }
    source_real="$(cd "${source_root}" && pwd -P)" || {
        printf 'build_under_srt: the physical path of the dotfiles checkout %s could not be read; nothing run.\n' "${source_root}" >&2
        return 1
    }
    common="$(git -C "${source_real}" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)" || {
        printf 'build_under_srt: the git common directory of %s could not be read; nothing run.\n' "${source_real}" >&2
        return 1
    }
    common_real="$(cd "${common}" && pwd -P)" || {
        printf 'build_under_srt: the physical path of the git common directory %s could not be read; nothing run.\n' "${common}" >&2
        return 1
    }
    if [ -e "${settings}" ] || [ -L "${settings}" ]; then
        printf 'build_under_srt: the settings path %s exists; the step runs only under a settings file it made (move it aside and rerun make update); nothing run.\n' "${settings}" >&2
        return 1
    fi
    for row in .ssh .gnupg .aws .netrc .docker .kube .config/gcloud .config/gh .codex .omp/agent .omp/profiles .hcom .local/state/hcom .local/share/chezmoi .local/share/chezmoi-private .config/chezmoi .config/chezmoi-private Workspace .local/state/omp-seats .claude .claude.json; do
        deny+=("${home_real}/${row}")
    done
    deny+=("${source_real}" "${common_real}")
    # srt 0.0.81's implicit write grants, closed by name (hcom-seat's form for the operator's Claude Code state, U190b):
    # its own TMPDIR root in every spelling the kernel may see, each once, and npm's log directory under the home.
    spellings=("${tmp_real}/claude")
    if [ -n "${tmp_second_real}" ]; then
        spellings+=("${tmp_second}/claude" "${tmp_second_real}/claude")
    fi
    for spelling in "${spellings[@]}"; do
        for row in "${deny_write[@]}"; do
            [ "${row}" != "${spelling}" ] || continue 2
        done
        deny_write+=("${spelling}")
    done
    deny_write+=("${home_real}/.npm/_logs")
    for path in "${dir_real}" "${store_real}" "${deny[@]}" "${deny_write[@]}"; do
        if [[ ! ${path} =~ ^(/[A-Za-z0-9._@+-]+)+$ ]] || [[ /${path}/ == */./* ]] || [[ /${path}/ == */../* ]]; then # lint-comparisons: allow a component test on one path, no path compare
            printf 'build_under_srt: %s is not a clean absolute path (components of [A-Za-z0-9._@+-], none . or .., no trailing slash), which the srt settings need; nothing run.\n' "${path}" >&2
            return 1
        fi
    done
    for host in ${hosts[@]+"${hosts[@]}"}; do
        if [[ ! ${host} =~ ^[A-Za-z0-9.-]+$ ]]; then
            printf 'build_under_srt: %s is not a host name (letters, digits, dots and hyphens; no wildcard); nothing run.\n' "${host}" >&2
            return 1
        fi
        hosts_json+="${hosts_json:+,}\"${host}\""
    done
    for path in "${dir_real}" "${store_real}"; do write_json+="${write_json:+,}\"${path}\""; done
    for path in "${deny[@]}"; do deny_json+="${deny_json:+,}\"${path}\""; done
    for path in "${deny_write[@]}"; do deny_write_json+="${deny_write_json:+,}\"${path}\""; done
    json="{\"network\":{\"allowedDomains\":[${hosts_json}],\"deniedDomains\":[],\"allowUnixSockets\":[],\"allowMachLookup\":[\"com.apple.trustd.agent\"],\"allowLocalBinding\":false}"
    json+=",\"filesystem\":{\"denyRead\":[${deny_json}],\"allowRead\":[],\"allowWrite\":[${write_json}],\"denyWrite\":[${deny_write_json}]},\"allowPty\":false}"
    # noclobber: the file is created by this open or the open fails, so a path that appeared since the check above is
    # refused too; umask 077 gives it 0600.
    (umask 077 && set -C && printf '%s\n' "${json}" > "${settings}") || {
        printf 'build_under_srt: the settings file %s could not be created; nothing run.\n' "${settings}" >&2
        return 1
    }
    # env -i stands outside srt (verdicts/U322 P1 :1941): srt starts from these variables alone and its child gets them
    # plus what srt injects; the command after -- is handed over as given.
    (cd "${dir_real}" && exec /usr/bin/env -i "HOME=${HOME}" "PATH=${pnpm_bin%/*}:${node_bin%/*}:/usr/bin:/bin" \
        "DSH_HOME=${DSH_HOME}" "TMPDIR=${store_real}/tmpdir" "CLAUDE_CODE_TMPDIR=${store_real}/tmpdir" \
        "XDG_CACHE_HOME=${store_real}/xdg-cache" "XDG_CONFIG_HOME=${store_real}/xdg-config" \
        "XDG_DATA_HOME=${store_real}/xdg-data" "XDG_STATE_HOME=${store_real}/xdg-state" \
        "npm_config_store_dir=${store_real}" "npm_config_cache_dir=${store_real}/cache" \
        "npm_config_state_dir=${store_real}/state" "npm_config_cache=${store_real}/npm-cache" \
        "npm_config_logs_dir=${store_real}/npm-cache/_logs" npm_config_manage_package_manager_versions=false \
        "${srt}" --settings "${settings}" -- "$@") || status=$?
    rm -f "${settings}" || printf 'WARN: build_under_srt: the settings file %s could not be removed; it grants nothing by itself, and the next run refuses it until it is moved aside.\n' "${settings}" >&2
    return "${status}"
}

#
# @description Install the pinned DeepSeek harness (assets.deepseek-harness) under DSH_HOME on a host whose operator
#   opted in, with a wrapper at $DSH_HOME/bin/dsh, the thak profile's plugins and the dsh-omp-gateway plugin link;
#   nothing starts it.
# @description
#   The opt-in is DSH_HOME exported and naming an existing directory: chezmoi deploys the rendered thak profile to
#   ~/.dsh/profiles/thak on every host, so a directory alone cannot be the opt-in, and a DSH_HOME other than ~/.dsh
#   is skipped with a WARN because the profile and the install would live apart. The install is one transaction whose
#   state is read from one place, the target of $DSH_HOME/dsh/current: GitHub's tag archive (never a branch head) is
#   downloaded into a mktemp directory and verified against its reviewed sha256 before anything is unpacked; the
#   archive's own package.json version must equal the pin; the tree is unpacked and built whole in its final place
#   under a name of its own ($DSH_HOME/dsh/<tag>.XXXXXX), the download directory goes, the profile's plugins are
#   installed, the dsh-omp-gateway plugin is linked into the profile's node_modules (one relative symlink the step
#   writes itself between the two physical paths, made beside its name and renamed into place so the previous link
#   stands until its replacement exists; `dsh plugin add link:` fails on the mise pnpm shim; the same link converges
#   on the repair and the already-installed exit, before the receipt is read, so a host installed before the row
#   existed gets it on the next run) and the wrapper is written and parsed beside its path, all before anything the
#   host runs changes; then
#   current is pointed at the new tree by one link call, the wrapper is replaced by one rename, the step is recorded,
#   and only then are the older trees under $DSH_HOME/dsh pruned (dsh_prune_older: the step's own name shapes, never
#   the inode current names). No tree is ever moved. Every input the step reads is one row of a table, checked by
#   type and by identity before any download; a state outside the table is refused, never repaired, and identities
#   are compared by inode (-ef) or by jq, never as text. The table, one line per row with its accepted states:
#   DSH_HOME: exported, absolute, a directory whose physical path (pwd -P) equals ~/.dsh's.
#   DSH_COMMIT: 40 lowercase hex (assets.deepseek-harness ref_commit), the build's DSH_CLIENT_COMMIT_HASH.
#   DSH_HOME/dsh and DSH_HOME/bin: absent, or a directory that is not a symlink.
#   DSH_HOME/profiles/thak: a directory that is not a symlink (the rendered profile); absent is a WARN with exit 0.
#   DSH_HOME/plugins/omp-gateway: a directory whose physical path (pwd -P) is under DSH_HOME's (the plugin chezmoi
#   deploys, the link's one target); absent, not a directory, or resolving outside DSH_HOME is refused, so no
#   harness is installed whose profile could reach no model or would import a tree outside DSH_HOME.
#   DSH_HOME/profiles/thak and its node_modules: physical paths under DSH_HOME's (a profiles/ parent that is itself a
#   symlink elsewhere under DSH_HOME is accepted; the link target is computed between the two physical paths, so it
#   resolves); node_modules absent, or a directory that is not a symlink (pnpm's own directory).
#   DSH_HOME/profiles/thak/node_modules/dsh-omp-gateway: absent, or a symlink whatever its target (replaced by one
#   rename); a directory or a file there is refused, never removed.
#   DSH_HOME/dsh/current: absent, or a symlink whose target is a non-symlink directory directly under dsh/ named
#   dsh-v* and whose inode is that directory's (-ef the leaf readlink named; the text read cannot mangle an inode).
#   The entries under DSH_HOME/dsh: the prune removes only a non-symlink directory named dsh-v* or .staging.* that
#   is not -ef current's target; every other entry stays.
#   DSH_HOME/bin/dsh: absent, or a regular file that is not a symlink.
#   ~/.agents/.installed-manifest.json: absent, or a regular file that is not a symlink holding exactly one JSON
#   object; a symlink, a directory or a FIFO is refused before the path is opened.
#   The receipt's recorded paths for the step: exactly the array [DSH_HOME/dsh/current, DSH_HOME/bin/dsh], read by
#   one jq array comparison whose status is 0 equal, 1 not equal (the rewrite on the already-installed exit, before
#   the prune, so no recorded path is ever pruned), any other a refusal.
#   A failure before the link leaves current, the wrapper and every older tree as they were; a failure after the link
#   (the rename, the record) puts current back on its prior target when it can and says what it left otherwise; no
#   cleanup changes the step's exit status. Every producer the step reads (pwd -P, the receipt as exactly one object,
#   jq, shasum, readlink, mktemp) refuses the step on a failed answer. A download that fails degrades like
#   update_security_audit_skill: one WARN line, nothing installed, nothing recorded, and make update goes on.
#   The upstream install and build scripts and the profile's plugin install run inside srt (build_under_srt,
#   regime-cutover U322): the settings grant writes under the new tree (or the profile) and $DSH_HOME/.pnpm-store
#   alone, deny reads of the credential roots and admit the hosts the lockfile names (the default registry, and the
#   host of every `tarball:` row); before the first build a canary (the U272 form) proves one write beside the tree
#   is denied inside, and a canary that does not run or a write that lands refuses the step.
# @exitcode 0 Installed, already installed, repaired (the wrapper rewritten for the tree current names, no download),
#   no opt-in (a skip line), DSH_HOME elsewhere than ~/.dsh (a WARN), or the download failed (a WARN; nothing
#   installed or recorded).
# @exitcode 1 DSH_COMMIT unset or malformed, a producer read, a shape or layout check, the digest check, the unpack,
#   the archive version, the build, the profile install, the plugin link, the wrapper, the current link or the record
#   failed; the line printed names the state left.
#
function update_deepseek_harness() (
    local recorded download_dir="" tarball actual tree="" version physical expected target="" leaf="" installed repair="" prior_target="" wrapper_tmp="" wrapper_step="" quote="'" quoted_home row record_status=0 plugin_real="" profile_real="" profile_modules_real="" plugin_target="" link_tmp="" hosts=() settings="" profile_settings="" canary="" probe=""
    # One record line for the install and for the rewrite on the already-installed exit, so the two cannot drift; it
    # writes the two paths the table's last row names (dsh/current, bin/dsh).
    dsh_record() {
        manifest_record "update_deepseek_harness" installer "${DSH_PIN_TAG}" "${DSH_HOME}/dsh/current" "${DSH_HOME}/bin/dsh" -- "curl -fsSL ${DSH_ARCHIVE_URL}" "shasum -a 256 <archive>" "mktemp -d ${DSH_HOME}/dsh/${DSH_PIN_TAG}.XXXXXX" "tar xzf <archive> -C <tree> --strip-components=1" "srt --settings <tree>.srt.json -- pnpm install --frozen-lockfile (writes: <tree>, ${DSH_HOME}/.pnpm-store)" "srt --settings <tree>.srt.json -- DSH_CLIENT_COMMIT_HASH=${DSH_COMMIT} pnpm run build" "srt --settings <tree>.profile.srt.json -- pnpm install in ${DSH_HOME}/profiles/thak (writes: that directory, ${DSH_HOME}/.pnpm-store)" "ln -s ${plugin_target} <link tmp>" "os.replace <link tmp> ${profile_modules_real}/dsh-omp-gateway (resolves to ${plugin_real})" "ln -sfn <tree> ${DSH_HOME}/dsh/current" "mv <wrapper tmp> ${DSH_HOME}/bin/dsh"
    }
    # The hosts a pnpm run may reach are its lockfile's, set in `hosts`: pnpm-lock.yaml resolves registry packages by
    # bare integrity, so the default registry is named first, and a dependency fetched by URL carries its host in a
    # `tarball:` row (the pinned tag: cdn.sheetjs.com for xlsx); a host inside a deprecation message is no fetch and
    # is not read. grep's status is read three ways: rows (0), no row (1), a lockfile it could not read (any other,
    # the refusal). The second argument names the state a refusal leaves.
    dsh_lockfile_hosts() {
        local rows="" row host status=0
        hosts=(registry.npmjs.org)
        rows="$(grep -o 'tarball: https\{0,1\}://[A-Za-z0-9.-]*' "$1")" || status=$?
        case ${status} in
        0 | 1) ;;
        *)
            printf 'update_deepseek_harness: the lockfile %s could not be read; %s\n' "$1" "$2" >&2
            return 1
            ;;
        esac
        while IFS= read -r row; do
            host="${row##*://}"
            [ -n "${host}" ] || continue
            case " ${hosts[*]} " in # lint-comparisons: allow a membership test over host names, no path compare
            *" ${host} "*) ;;
            *) hosts+=("${host}") ;;
            esac
        done <<< "${rows}"
    }
    # The link joins two physical paths (pwd -P), so a profiles/ parent that is a symlink elsewhere under DSH_HOME gets
    # a relative target that resolves, and the receipt records what was written. The previous link is replaced by one
    # rename(2): a temporary link beside the name, then python3's os.replace onto it (mv has no -T on macOS and moves
    # the temporary into the directory a link names), so a failure at any point leaves the previous link standing and
    # the profile is never without its plugin. The caller names the state a failure leaves.
    dsh_link_plugin() {
        local link="${DSH_HOME}/profiles/thak/node_modules/dsh-omp-gateway"
        mkdir -p "${profile_real}/node_modules" || {
            printf 'update_deepseek_harness: %s could not be made; %s\n' "${profile_real}/node_modules" "$1" >&2
            return 1
        }
        profile_modules_real="$(cd "${profile_real}/node_modules" && pwd -P)" || {
            printf 'update_deepseek_harness: the physical path of %s could not be read; %s\n' "${profile_real}/node_modules" "$1" >&2
            return 1
        }
        case ${profile_modules_real} in # lint-comparisons: allow both sides are pwd -P physical paths
        "${physical}/"*) ;;
        *)
            printf 'update_deepseek_harness: %s resolves to %s, outside %s; the step links the plugin only inside DSH_HOME; %s\n' "${link%/*}" "${profile_modules_real}" "${physical}" "$1" >&2
            return 1
            ;;
        esac
        plugin_target="$(python3 -I -c 'import os, sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "${plugin_real}" "${profile_modules_real}")" || {
            printf 'update_deepseek_harness: the link target from %s to %s could not be computed; %s\n' "${profile_modules_real}" "${plugin_real}" "$1" >&2
            return 1
        }
        # A temporary of this run's own name left by an interrupted run is cleared first, so every run converges.
        link_tmp="${link}.tmp.$$"
        if ! rm -f "${link_tmp}" || ! ln -s "${plugin_target}" "${link_tmp}"; then
            printf 'update_deepseek_harness: the plugin link %s could not be written (its temporary %s failed); the previous link is untouched; %s\n' "${link}" "${link_tmp}" "$1" >&2
            return 1
        fi
        if ! python3 -I -c 'import os, sys; os.replace(sys.argv[1], sys.argv[2])' "${link_tmp}" "${link}"; then
            rm -f "${link_tmp}"
            printf 'update_deepseek_harness: the plugin link %s could not be renamed into place from %s; the previous link is untouched and the temporary is removed; %s\n' "${link}" "${link_tmp}" "$1" >&2
            return 1
        fi
        link_tmp=""
        if [ ! -d "${link}" ]; then
            printf 'update_deepseek_harness: the plugin link %s was written but does not resolve to %s; %s\n' "${link}" "${plugin_real}" "$1" >&2
            return 1
        fi
    }
    section "DeepSeek harness"
    if [ -z "${DSH_HOME:-}" ] || [ ! -d "${DSH_HOME}" ]; then
        printf 'Skipping DeepSeek harness: DSH_HOME is unset or names no directory (export it and create it to opt in).\n'
        return 0
    fi
    # The tag archive carries no .git, and the upstream build runs `git rev-parse HEAD` unless DSH_CLIENT_COMMIT_HASH
    # names the commit, so the build fails without the pinned one; it is checked here, before any read or download.
    if [[ ! ${DSH_COMMIT:-} =~ ^[0-9a-f]{40}$ ]]; then
        printf 'update_deepseek_harness: DSH_COMMIT (assets.deepseek-harness ref_commit, rendered into scripts/lib/installer-pins.sh) is unset or not 40 lowercase hex (%s given), so the build has no DSH_CLIENT_COMMIT_HASH; nothing installed, nothing recorded.\n' "${DSH_COMMIT:-}" >&2
        return 1
    fi
    # A relative DSH_HOME would pass the pwd -P comparison below and stay relative in the link target, the wrapper
    # and the receipt, so the spelling is checked before the identity.
    case ${DSH_HOME} in # lint-comparisons: allow the case reads the spelling (absolute or not); the pwd -P comparison below reads the identity
    /*) ;;
    *)
        printf 'WARN: update_deepseek_harness: DSH_HOME must be an absolute path (%s given); nothing installed.\n' "${DSH_HOME}" >&2
        return 0
        ;;
    esac
    physical="$(cd "${DSH_HOME}" && pwd -P)" || {
        printf 'update_deepseek_harness: the physical path of DSH_HOME %s could not be read; step refused.\n' "${DSH_HOME}" >&2
        return 1
    }
    # The reference path is a producer of its own: absent, the kit has not rendered the profile here (a WARN, as for
    # any other DSH_HOME); present and unreadable, the step refuses instead of warning over a read it never made.
    if [ ! -e "${HOME}/.dsh" ]; then
        printf 'WARN: update_deepseek_harness: DSH_HOME is %s, not %s, where the kit renders the thak profile; nothing installed.\n' "${DSH_HOME}" "${HOME}/.dsh" >&2
        return 0
    fi
    expected="$(cd "${HOME}/.dsh" && pwd -P)" || {
        printf 'update_deepseek_harness: the reference path %s could not be read; step refused.\n' "${HOME}/.dsh" >&2
        return 1
    }
    if [ "${physical}" != "${expected}" ]; then # lint-comparisons: allow both sides are pwd -P physical paths
        printf 'WARN: update_deepseek_harness: DSH_HOME is %s, not %s, where the kit renders the thak profile; nothing installed.\n' "${DSH_HOME}" "${HOME}/.dsh" >&2
        return 0
    fi
    # The three directories the step writes into are read by type before anything else: a dsh/ or bin/ that is a
    # symlink (into an older tree, say) would have the prune or the rename reach a path the operator linked, and a
    # file there is no place to make the tree or the wrapper; the profile directory is the kit's own rendering, so a
    # symlink or a file there is refused and an absent one is the host the kit has not rendered on.
    for row in dsh bin; do
        if [ -L "${DSH_HOME}/${row}" ] || { [ -e "${DSH_HOME}/${row}" ] && [ ! -d "${DSH_HOME}/${row}" ]; }; then
            printf 'update_deepseek_harness: %s is a symlink or not a directory; the step uses only a directory of its own there (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/${row}" >&2
            return 1
        fi
    done
    if [ -L "${DSH_HOME}/profiles/thak" ] || { [ -e "${DSH_HOME}/profiles/thak" ] && [ ! -d "${DSH_HOME}/profiles/thak" ]; }; then
        printf 'update_deepseek_harness: %s is a symlink or not a directory; the step installs the profile plugins only into the directory the kit renders (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/profiles/thak" >&2
        return 1
    fi
    if [ ! -d "${DSH_HOME}/profiles/thak" ]; then
        printf 'WARN: update_deepseek_harness: %s is absent, so the kit has not rendered the thak profile here; nothing installed.\n' "${DSH_HOME}/profiles/thak" >&2
        return 0
    fi
    # The plugin link's inputs are read physically: -d alone follows a symlink, so a plugins/omp-gateway that is a link
    # to a directory outside DSH_HOME would be accepted and a turn would import whatever stands there, and a profiles/
    # parent that is itself a symlink would get a relative target counted from a place the link does not sit at. The
    # plugin directory is what chezmoi deploys and the link's one target, so a host without it gets no harness whose
    # profile could reach no model; node_modules is pnpm's directory, so a symlink or a file there is not the step's to
    # write into; the link path holds a symlink or nothing, since a rename onto a real directory would move the link
    # inside it or fail.
    if [ ! -d "${DSH_HOME}/plugins/omp-gateway" ]; then
        printf 'update_deepseek_harness: %s is absent or not a directory; the thak profile loads the dsh-omp-gateway plugin from there (chezmoi apply deploys it; then rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/plugins/omp-gateway" >&2
        return 1
    fi
    plugin_real="$(cd "${DSH_HOME}/plugins/omp-gateway" && pwd -P)" || {
        printf 'update_deepseek_harness: the physical path of %s could not be read; step refused.\n' "${DSH_HOME}/plugins/omp-gateway" >&2
        return 1
    }
    case ${plugin_real} in # lint-comparisons: allow both sides are pwd -P physical paths
    "${physical}/"*) ;;
    *)
        printf 'update_deepseek_harness: %s resolves to %s, outside %s; the thak profile loads the dsh-omp-gateway plugin only from a directory under DSH_HOME (chezmoi apply deploys it there; move the link aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/plugins/omp-gateway" "${plugin_real}" "${physical}" >&2
        return 1
        ;;
    esac
    profile_real="$(cd "${DSH_HOME}/profiles/thak" && pwd -P)" || {
        printf 'update_deepseek_harness: the physical path of %s could not be read; step refused.\n' "${DSH_HOME}/profiles/thak" >&2
        return 1
    }
    case ${profile_real} in # lint-comparisons: allow both sides are pwd -P physical paths
    "${physical}/"*) ;;
    *)
        printf 'update_deepseek_harness: %s resolves to %s, outside %s; the step links the plugin only into a profile under DSH_HOME (move the profile back and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/profiles/thak" "${profile_real}" "${physical}" >&2
        return 1
        ;;
    esac
    if [ -L "${DSH_HOME}/profiles/thak/node_modules" ] || { [ -e "${DSH_HOME}/profiles/thak/node_modules" ] && [ ! -d "${DSH_HOME}/profiles/thak/node_modules" ]; }; then
        printf 'update_deepseek_harness: %s is a symlink or not a directory; the step links the plugin only inside the directory pnpm makes there (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/profiles/thak/node_modules" >&2
        return 1
    fi
    if [ -e "${DSH_HOME}/profiles/thak/node_modules/dsh-omp-gateway" ] && [ ! -L "${DSH_HOME}/profiles/thak/node_modules/dsh-omp-gateway" ]; then
        printf 'update_deepseek_harness: %s is not a symlink; the step refuses to replace it (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/profiles/thak/node_modules/dsh-omp-gateway" >&2
        return 1
    fi
    # ln -sfn onto a real directory at current makes a link inside it and succeeds, so a current that is neither a
    # symlink nor absent is refused before anything is downloaded or linked.
    if [ -e "${DSH_HOME}/dsh/current" ] && [ ! -L "${DSH_HOME}/dsh/current" ]; then
        printf 'update_deepseek_harness: %s is not a symlink; the step refuses to replace it (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/dsh/current" >&2
        return 1
    fi
    # The step accepts one layout, the one it makes, and repairs no other: a current that reaches its tree indirectly
    # (dsh/<older>/relay, dsh/<older>/../<tree>, a symlink at dsh/<name>) passes every shape check, and the prune,
    # which removes by name under dsh/, then takes the directory the link traverses and leaves current dangling with
    # exit 0. So the target must be a non-symlink directory directly under dsh/ named dsh-v*, and the link itself
    # must reach that very directory (-ef): $(readlink) strips a trailing newline, so a target whose name ends in one
    # reads as another directory's name, and only the inode comparison tells the two apart. The installed state is
    # read from the target.
    if [ -L "${DSH_HOME}/dsh/current" ]; then
        target="$(readlink "${DSH_HOME}/dsh/current")" || {
            printf 'update_deepseek_harness: the target of %s could not be read; step refused.\n' "${DSH_HOME}/dsh/current" >&2
            return 1
        }
        # A relative target is read from the link's own directory, as the link reads it.
        case ${target} in # lint-comparisons: allow the case reads the spelling (absolute or not) to anchor a relative link target
        /*) ;;
        *) target="${DSH_HOME}/dsh/${target}" ;;
        esac
        case ${target} in # lint-comparisons: allow the case reads the layout (one name directly under dsh/), which is the rule, not an identity
        "${DSH_HOME}/dsh/"*) leaf="${target#"${DSH_HOME}/dsh/"}" ;;
        esac
        case ${leaf} in
        */*) leaf="" ;;
        dsh-v*) ;;
        *) leaf="" ;;
        esac
        if [ -z "${leaf}" ] || [ ! -d "${target}" ] || [ -L "${target}" ] || [ ! "${DSH_HOME}/dsh/current" -ef "${DSH_HOME}/dsh/${leaf}" ]; then
            printf 'update_deepseek_harness: %s points at %s, which is not a directory directly under %s/dsh named dsh-v* that the link itself reaches; the step repairs only the layout it makes (move the link aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/dsh/current" "${target}" "${DSH_HOME}" >&2
            return 1
        fi
    fi
    # mv -f onto a directory at bin/dsh puts the wrapper inside it and succeeds, and a symlink there would make the
    # rename replace something the operator linked by hand, so only a regular file or nothing may stand at the path.
    if [ -L "${DSH_HOME}/bin/dsh" ] || { [ -e "${DSH_HOME}/bin/dsh" ] && [ ! -f "${DSH_HOME}/bin/dsh" ]; }; then
        printf 'update_deepseek_harness: %s is not a regular file; the step refuses to replace it (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/bin/dsh" >&2
        return 1
    fi
    # The receipt is read by type before it is opened: a symlink (dangling, or into an older tree the prune removes)
    # and a directory or a FIFO are no receipt the step can read or manifest_record write, and -f alone would let a
    # directory, a FIFO or a dangling link pass as the fresh host; a FIFO is never opened. Then a receipt file that
    # is not exactly one JSON object is a failed read, not an empty receipt: jq answers a zero-byte file with exit 0
    # and no output, and jq -e without -s judges each document of a file on its own, so the file is slurped and its
    # shape checked before the step's row is read; installing over a record the step could not consult would hide
    # the corruption. A missing file is the fresh host and installs.
    if [ -L "${HOME}/.agents/.installed-manifest.json" ]; then
        printf 'update_deepseek_harness: the installed-manifest receipt %s is a symlink; the step reads and writes only a regular file there (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${HOME}/.agents/.installed-manifest.json" >&2
        return 1
    fi
    if [ -e "${HOME}/.agents/.installed-manifest.json" ] && [ ! -f "${HOME}/.agents/.installed-manifest.json" ]; then
        printf 'update_deepseek_harness: the installed-manifest receipt %s is not a regular file; the step reads and writes only a regular file there (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${HOME}/.agents/.installed-manifest.json" >&2
        return 1
    fi
    if [ -f "${HOME}/.agents/.installed-manifest.json" ]; then
        jq -es 'length == 1 and (.[0] | type) == "object"' "${HOME}/.agents/.installed-manifest.json" > /dev/null 2>&1 || {
            printf 'update_deepseek_harness: the installed-manifest receipt could not be read as a JSON object; step refused.\n' >&2
            return 1
        }
        recorded="$(jq -r '.steps["update_deepseek_harness"].source_version // empty' "${HOME}/.agents/.installed-manifest.json" 2> /dev/null)" || {
            printf 'update_deepseek_harness: the installed-manifest receipt could not be read; step refused.\n' >&2
            return 1
        }
    else
        recorded=""
    fi
    # The installed state is read from current alone, never from a fixed tree path: installed means the receipt at
    # the pin, the tree current names carrying the pin's version and its entrypoint, and an executable wrapper. The
    # doctor's repair runs this step when the wrapper alone is gone, so the tree gets its wrapper back without a
    # download; any other state installs.
    if [ "${recorded}" = "${DSH_PIN_TAG}" ] && [ -n "${target}" ] && [ -f "${target}/package.json" ]; then
        installed="$(jq -r '.version // empty' "${target}/package.json")" || {
            printf 'update_deepseek_harness: the version of the installed tree %s could not be read; step refused.\n' "${target}" >&2
            return 1
        }
        if [ "${installed}" = "${DSH_PIN_TAG#dsh-v}" ] && [ -f "${target}/apps/cli/lib/bin.js" ]; then
            if [ -f "${DSH_HOME}/bin/dsh" ] && [ -x "${DSH_HOME}/bin/dsh" ]; then
                printf 'DeepSeek harness %s is already installed.\n' "${DSH_PIN_TAG}"
                dsh_link_plugin "the receipt and the older trees are kept." || return 1
                # The receipt's paths are what the doctor checks for existence. A receipt from the earlier layout
                # names dsh/<tag>, an older tree the prune below removes, and so does one a failed record left behind
                # a kept new tree; a receipt whose paths are not exactly this layout's two is rewritten first, and
                # nothing is pruned when that write fails. jq compares the recorded array with the two paths as an
                # array (a joined text would read an extra empty entry or a newline inside an entry as equal); its
                # status is read three ways: equal, not equal (the rewrite), and a read that failed (the refusal).
                record_status=0
                jq -e --arg c "${DSH_HOME}/dsh/current" --arg w "${DSH_HOME}/bin/dsh" '.steps["update_deepseek_harness"].paths == [$c, $w]' "${HOME}/.agents/.installed-manifest.json" > /dev/null 2>&1 || record_status=$?
                case ${record_status} in
                0) ;;
                1)
                    dsh_record || {
                        printf 'update_deepseek_harness: the record could not be rewritten; the older trees are kept.\n' >&2
                        return 1
                    }
                    ;;
                *)
                    printf 'update_deepseek_harness: the recorded paths could not be read from the installed-manifest receipt; step refused.\n' >&2
                    return 1
                    ;;
                esac
                # An older tree whose removal failed after the record is retried here, since every later run of a
                # recorded install ends on this path.
                dsh_prune_older "${DSH_HOME}"
                return 0
            fi
            repair=1
        fi
    fi
    if [ -z "${repair}" ]; then
        download_dir="$(mktemp -d "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX")" || {
            printf 'update_deepseek_harness: the download directory could not be made; step refused.\n' >&2
            return 1
        }
        # ${name:+"${name}"}: on macOS bash the subshell's locals are unwound before the EXIT trap runs after a failed
        # return, so a bare name is unbound under set -u and the trap dies before its rm; a name emptied once its path
        # is gone adds no operand. `|| :`: set -e is in force inside the trap, so a cleanup that fails would make its
        # status the step's (a failed download's WARN became exit 77); what the cleanup leaves is the next run's.
        trap 'rm -rf ${download_dir:+"${download_dir}"} ${tree:+"${tree}"} ${wrapper_tmp:+"${wrapper_tmp}"} ${settings:+"${settings}"} ${profile_settings:+"${profile_settings}"} ${canary:+"${canary}"} || :' EXIT
        tarball="${download_dir}/deepseek-harness-${DSH_PIN_TAG}.tar.gz"
        curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${DSH_ARCHIVE_URL}" -o "${tarball}" || {
            printf 'WARN: update_deepseek_harness: the DeepSeek harness archive could not be downloaded (%s); nothing installed, nothing recorded; the existing install is unchanged and the next make update retries.\n' "${DSH_ARCHIVE_URL}" >&2
            return 0
        }
        actual="$(shasum -a 256 "${tarball}")" || {
            printf 'update_deepseek_harness: the digest of the downloaded archive could not be read; install refused.\n' >&2
            return 1
        }
        if [ "${actual%% *}" != "${DSH_ARCHIVE_SHA256}" ]; then
            printf 'DeepSeek harness checksum mismatch: expected %s, got %s.\n' "${DSH_ARCHIVE_SHA256}" "${actual%% *}" >&2
            return 1
        fi
        # The tree is unpacked and built whole in its final place under a name of its own, so publication is one link
        # call and no tree is moved; the one leading component (<repository>-<tag>) is stripped so the package lands
        # at the tree itself.
        mkdir -p "${DSH_HOME}/dsh" || {
            printf 'update_deepseek_harness: the install directory %s could not be made; install refused.\n' "${DSH_HOME}/dsh" >&2
            return 1
        }
        tree="$(mktemp -d "${DSH_HOME}/dsh/${DSH_PIN_TAG}.XXXXXX")" || {
            printf 'update_deepseek_harness: the install tree under %s could not be made; install refused.\n' "${DSH_HOME}/dsh" >&2
            return 1
        }
        tar xzf "${tarball}" -C "${tree}" --strip-components=1 || return 1
        version="$(jq -r '.version // empty' "${tree}/package.json")" || {
            printf 'update_deepseek_harness: the version of the archive could not be read; install refused.\n' >&2
            return 1
        }
        if [ "${version}" != "${DSH_PIN_TAG#dsh-v}" ]; then
            printf 'DeepSeek harness archive version %s is not the pin %s; install refused.\n' "${version}" "${DSH_PIN_TAG#dsh-v}" >&2
            return 1
        fi
        # The frozen install needs the lockfile; a tag without one is no tree this step builds.
        if [ ! -f "${tree}/pnpm-lock.yaml" ]; then
            printf 'update_deepseek_harness: the archive holds no pnpm-lock.yaml, which the frozen install reads; install refused.\n' >&2
            return 1
        fi
        dsh_lockfile_hosts "${tree}/pnpm-lock.yaml" "install refused." || return 1
        settings="${tree}.srt.json"
        profile_settings="${tree}.profile.srt.json"
        canary="${tree}.canary"
        # The canary (the U272 form) proves the sandbox holds before any upstream code runs: one write beside the tree,
        # outside both write roots, must be denied inside, and the word the probe prints is read whole. A canary that
        # does not run (srt absent or refusing its settings) and a write that lands are each refused, and a file the
        # write made is removed here, outside. `true`, not `:`: a failed redirection on a special builtin ends a POSIX
        # shell.
        # shellcheck disable=SC2016 # the text runs inside srt's /bin/sh, where $1 is the canary path
        probe="$(build_under_srt "${tree}" "${settings}" -- /bin/sh -c 'if true 2> /dev/null > "$1"; then echo write-open; else echo write-denied; fi' canary "${canary}")" || {
            rm -f "${canary}" || :
            printf 'update_deepseek_harness: the sandbox canary did not run under srt; nothing installed, nothing recorded; the previous install, when there is one, is unchanged.\n' >&2
            return 1
        }
        if [ "${probe}" != write-denied ] || [ -e "${canary}" ]; then
            rm -f "${canary}" || :
            printf 'update_deepseek_harness: the sandbox does not hold (canary: %s); nothing installed, nothing recorded; the previous install, when there is one, is unchanged.\n' "${probe}" >&2
            return 1
        fi
        # The upstream install and build scripts run inside srt alone (verdicts/U317 P1 :2421, the same class): writes
        # under the new tree and the store, reads outside the credential roots, the lockfile's hosts.
        build_under_srt "${tree}" "${settings}" "${hosts[@]}" -- pnpm install --frozen-lockfile || {
            printf 'update_deepseek_harness: the install of the tree failed inside srt (a write outside %s and %s is refused there; hosts allowed: %s); the new tree is removed; nothing installed, nothing recorded; the previous install, when there is one, is unchanged.\n' "${tree}" "${DSH_HOME}/.pnpm-store" "${hosts[*]}" >&2
            return 1
        }
        build_under_srt "${tree}" "${settings}" "${hosts[@]}" -- "DSH_CLIENT_COMMIT_HASH=${DSH_COMMIT}" pnpm run build || {
            printf 'update_deepseek_harness: the build failed inside srt (a write outside %s and %s is refused there); the new tree is removed; nothing installed, nothing recorded; the previous install, when there is one, is unchanged.\n' "${tree}" "${DSH_HOME}/.pnpm-store" >&2
            return 1
        }
        # The download directory holds only the verified archive, whose tree is now built, so its removal is no read
        # the step decides on: it goes here, before anything the host runs changes, and a removal that fails is a WARN
        # that never changes the step's flow (under set -e a bare failing rm would end the subshell, and a retry of it
        # in the EXIT trap would make its status the step's, so the name is emptied either way).
        rm -rf "${download_dir}" || printf 'WARN: update_deepseek_harness: the download directory %s could not be removed; it holds only the verified archive and the next make update makes a new one.\n' "${download_dir}" >&2
        download_dir=""
        # The profile's plugins go in before anything the host runs changes: a failure here needs no undo, since
        # current, the wrapper and every older tree are still as they were and the trap removes the new tree. The
        # install runs inside srt with the profile directory and the store as its write roots; its hosts are its own
        # lockfile's when pnpm has written one (the kit renders none), else the default registry alone.
        if [ -e "${DSH_HOME}/profiles/thak/pnpm-lock.yaml" ]; then
            dsh_lockfile_hosts "${DSH_HOME}/profiles/thak/pnpm-lock.yaml" "nothing recorded; current, the wrapper and the older trees are untouched." || return 1
        else
            hosts=(registry.npmjs.org)
        fi
        build_under_srt "${DSH_HOME}/profiles/thak" "${profile_settings}" "${hosts[@]}" -- pnpm install || {
            printf 'update_deepseek_harness: the profile install failed inside srt (a write outside %s and %s is refused there); nothing recorded; current, the wrapper and the older trees are untouched.\n' "${DSH_HOME}/profiles/thak" "${DSH_HOME}/.pnpm-store" >&2
            return 1
        }
        dsh_link_plugin "nothing recorded; current, the wrapper and the older trees are untouched." || return 1
    else
        trap 'rm -rf ${wrapper_tmp:+"${wrapper_tmp}"} || :' EXIT
        dsh_link_plugin "nothing recorded; the live wrapper, current and the older trees are untouched." || return 1
    fi
    # The wrapper is written beside its path, parsed and given its mode before the link, and moved over the live one
    # by one rename after it, so a failure before the rename leaves the live launcher byte-identical. It carries the
    # home expanded at write time as a single-quoted literal (every ' in it as '\''), so a $(...) or a " in the path
    # is text when the wrapper runs, and bash -n refuses a wrapper that still does not parse: the harness runs under
    # mise's node, nothing of it on PATH. bin/ is made here in both modes, since a repair finds it gone too.
    mkdir -p "${DSH_HOME}/bin" || {
        printf 'update_deepseek_harness: the wrapper directory %s could not be made; nothing recorded; the live wrapper, current and the older trees are untouched.\n' "${DSH_HOME}/bin" >&2
        return 1
    }
    quoted_home="${quote}${DSH_HOME//${quote}/${quote}\\${quote}${quote}}${quote}"
    wrapper_tmp="$(mktemp "${DSH_HOME}/bin/.dsh.XXXXXX")" || {
        printf 'update_deepseek_harness: a wrapper file under %s could not be made; nothing recorded; the live wrapper, current and the older trees are untouched.\n' "${DSH_HOME}/bin" >&2
        return 1
    }
    if ! printf '#!/bin/bash\nexec mise exec -- node %s/dsh/current/apps/cli/lib/bin.js "$@"\n' "${quoted_home}" > "${wrapper_tmp}"; then
        wrapper_step="the wrapper write"
    elif ! bash -n "${wrapper_tmp}"; then
        wrapper_step="the wrapper parse"
    elif ! chmod 755 "${wrapper_tmp}"; then
        wrapper_step="the wrapper mode"
    fi
    if [ -n "${wrapper_step}" ]; then
        printf 'update_deepseek_harness: %s failed; nothing recorded; the live wrapper at %s, current and the older trees are untouched.\n' "${wrapper_step}" "${DSH_HOME}/bin/dsh" >&2
        return 1
    fi
    if [ -z "${repair}" ]; then
        # What current pointed at before, whatever its version, so a failure after the link can put the link back.
        if [ -L "${DSH_HOME}/dsh/current" ]; then
            prior_target="$(readlink "${DSH_HOME}/dsh/current")" || {
                printf 'update_deepseek_harness: the target of %s could not be read; install refused.\n' "${DSH_HOME}/dsh/current" >&2
                return 1
            }
        fi
        # ln -sfn unlinks current before it links, so a failure can leave no current at all: with a prior tree on
        # disk the link is put back on it once; the line names what is left either way, and the trap removes the new
        # tree and the wrapper temporary.
        if ! ln -sfn "${tree}" "${DSH_HOME}/dsh/current"; then
            if [ -z "${prior_target}" ]; then
                printf 'update_deepseek_harness: the current link could not be written; nothing recorded; the live wrapper and the older trees are untouched.\n' >&2
            elif [ -L "${DSH_HOME}/dsh/current" ] || { (cd "${DSH_HOME}/dsh" && [ -d "${prior_target}" ]) && ln -sfn "${prior_target}" "${DSH_HOME}/dsh/current"; }; then
                printf 'update_deepseek_harness: the current link could not be written; current is back on %s and the new tree is removed; nothing recorded; the live wrapper and the older trees are untouched.\n' "${prior_target}" >&2
            else
                printf 'update_deepseek_harness: the current link could not be written; current is absent; the prior tree %s is on disk under dsh/ and the next make update reinstalls; the new tree is removed; nothing recorded; the live wrapper is untouched.\n' "${prior_target}" >&2
            fi
            return 1
        fi
    fi
    # The rename is the first change to what the host runs in repair mode and the second after the link otherwise:
    # a failure after the link is undone the way a failed record is.
    if ! mv -f "${wrapper_tmp}" "${DSH_HOME}/bin/dsh"; then
        if [ -n "${repair}" ]; then
            printf 'update_deepseek_harness: the wrapper rename failed; nothing recorded; the live wrapper at %s, current and the older trees are untouched.\n' "${DSH_HOME}/bin/dsh" >&2
        elif [ -n "${prior_target}" ] && (cd "${DSH_HOME}/dsh" && [ -d "${prior_target}" ]); then
            if ln -sfn "${prior_target}" "${DSH_HOME}/dsh/current"; then
                printf 'update_deepseek_harness: the wrapper rename failed after the link; current is back on %s and the new tree is removed; the live wrapper is unchanged; nothing recorded.\n' "${prior_target}" >&2
            elif [ -L "${DSH_HOME}/dsh/current" ]; then
                printf 'update_deepseek_harness: the wrapper rename failed after the link and current could not be put back on %s; current still names the new tree %s, which is kept; the live wrapper is unchanged; nothing recorded; the next make update reinstalls.\n' "${prior_target}" "${tree}" >&2
                tree=""
            else
                printf 'update_deepseek_harness: the wrapper rename failed after the link and current could not be put back on %s; current is absent; the prior tree %s and the new tree %s are on disk under dsh/; the live wrapper is unchanged; nothing recorded; the next make update reinstalls.\n' "${prior_target}" "${prior_target}" "${tree}" >&2
                tree=""
            fi
        elif rm -f "${DSH_HOME}/dsh/current"; then
            printf 'update_deepseek_harness: the wrapper rename failed after the link; the new tree and the current link are removed; the live wrapper is unchanged; nothing recorded.\n' >&2
        else
            printf 'update_deepseek_harness: the wrapper rename failed after the link and current could not be removed and still names the new tree %s, which is kept; the live wrapper is unchanged; nothing recorded; the next make update reinstalls.\n' "${tree}" >&2
            tree=""
        fi
        return 1
    fi
    wrapper_tmp=""
    if [ -z "${repair}" ]; then
        printf 'DeepSeek harness %s installed into %s.\n' "${DSH_PIN_TAG}" "${tree}"
    else
        printf 'DeepSeek harness %s is at %s; its wrapper is rewritten.\n' "${DSH_PIN_TAG}" "${target}"
    fi
    if ! dsh_record; then
        if [ -n "${repair}" ]; then
            printf 'update_deepseek_harness: the record failed; nothing recorded; the next make update retries.\n' >&2
            return 1
        fi
        # current returns to its prior target when that is a directory (a relative target is read from the link's own
        # directory, as the link reads it); with none to return to, the link goes with the new tree, which the trap
        # removes. When the link cannot be put back or removed, the tree current names is kept (tree="" keeps it from
        # the trap), since removing it would leave the host a dangling launcher, and the line says whether current is
        # on it or absent (a restoring ln -sfn unlinks before it links). The older trees are not touched, so a second
        # failing run finds the same older tree.
        if [ -n "${prior_target}" ] && (cd "${DSH_HOME}/dsh" && [ -d "${prior_target}" ]); then
            if ln -sfn "${prior_target}" "${DSH_HOME}/dsh/current"; then
                printf 'update_deepseek_harness: the record failed; current is back on %s and the new tree is removed; nothing recorded; the older trees are untouched.\n' "${prior_target}" >&2
            elif [ -L "${DSH_HOME}/dsh/current" ]; then
                printf 'update_deepseek_harness: the record failed and current could not be put back on %s; current still names the new tree %s, which is kept; nothing recorded; the next make update reinstalls.\n' "${prior_target}" "${tree}" >&2
                tree=""
            else
                printf 'update_deepseek_harness: the record failed and current could not be put back on %s; current is absent; the prior tree %s and the new tree %s are on disk under dsh/; nothing recorded; the next make update reinstalls.\n' "${prior_target}" "${prior_target}" "${tree}" >&2
                tree=""
            fi
        elif rm -f "${DSH_HOME}/dsh/current"; then
            printf 'update_deepseek_harness: the record failed; the new tree and the current link are removed; nothing recorded; the next make update retries.\n' >&2
        else
            printf 'update_deepseek_harness: the record failed and current could not be removed and still names the new tree %s, which is kept; nothing recorded; the next make update reinstalls.\n' "${tree}" >&2
            tree=""
        fi
        return 1
    fi
    tree=""
    # Only now, with the record written, do the older trees go.
    dsh_prune_older "${DSH_HOME}"
)

# Rendered from assets.dsh-superagent in home/dot_agents/agent-config.yaml through scripts/lib/installer-pins.sh
# (DSH_SUPERAGENT_COMMIT, DSH_SUPERAGENT_SHA256); the archive is GitHub's source archive of the pinned commit, never a
# branch head. The repository path is the asset's upstream; the fork (T-M-26-01) moves it with the manifest's upstream.
readonly DSH_SUPERAGENT_REPOSITORY="deepseek-ai/dsh-superagent-prototype"
readonly DSH_SUPERAGENT_ARCHIVE_URL="https://codeload.github.com/${DSH_SUPERAGENT_REPOSITORY}/tar.gz/${DSH_SUPERAGENT_COMMIT}"
# The package registry the archive's lockfile resolves from: pnpm-lock.yaml names no registry host (every resolution is
# a bare `integrity`), so pnpm reads the default, and the build's srt settings admit that one host (regime-cutover
# U317b).
readonly DSH_SUPERAGENT_REGISTRY_HOST="registry.npmjs.org"

#
# @description Refuse a path srt's settings cannot carry as itself (regime-cutover U317b, hcom-seat's clean_path): every
#   component of [A-Za-z0-9._@+-], none `.` or `..`, no trailing slash. srt 0.0.81 turns a settings path into a
#   Seatbelt regex or a glob, so a quote, a space or a `*` would grant more than the path; the JSON below is written by
#   the shell from such paths and no JSON tool runs.
# @arg $1 string The path.
# @exitcode 1 The path is not clean; the line names it.
#
function dsh_superagent_clean_path() {
    if [[ ! $1 =~ ^(/[A-Za-z0-9._@+-]+)+$ ]] || [[ /$1/ == */./* ]] || [[ /$1/ == */../* ]]; then # lint-comparisons: allow a component test on one path, no path compare
        printf 'update_dsh_superagent: %s is not a clean absolute path (components of [A-Za-z0-9._@+-], none . or .., no trailing slash), which the srt settings need; nothing installed, nothing recorded.\n' "$1" >&2
        return 1
    fi
}

#
# @description Resolve one tool the dsh-superagent step runs by `mise which` (the kit's pins in home/dot_mise/config.toml:
#   sandbox-runtime, pnpm, node), with the status read: a failed answer, a relative one or one that is not an executable
#   file refuses the step (standing order 21). MISE_EXEC_AUTO_INSTALL=false keeps mise from installing anything the step
#   asks after (verdicts/U276b).
# @arg $1 string The tool.
# @stdout The tool's absolute path.
# @exitcode 1 No usable answer; the line names the tool.
#
function dsh_superagent_tool() {
    local path
    path="$(MISE_EXEC_AUTO_INSTALL=false mise which "$1" 2> /dev/null)" || {
        printf 'update_dsh_superagent: %s is absent (mise which %s failed; the kit pins it in home/dot_mise/config.toml, so run make update after mise install); nothing installed, nothing recorded.\n' "$1" "$1" >&2
        return 1
    }
    case ${path} in # lint-comparisons: allow the case reads the spelling (absolute or not), the file tests below read the entry
    /*) ;;
    *)
        printf 'update_dsh_superagent: mise which %s answered %s, not an absolute path; nothing installed, nothing recorded.\n' "$1" "${path}" >&2
        return 1
        ;;
    esac
    if [ ! -f "${path}" ] || [ ! -x "${path}" ]; then
        printf 'update_dsh_superagent: %s (mise which %s) is not an executable file; nothing installed, nothing recorded.\n' "${path}" "$1" >&2
        return 1
    fi
    printf '%s\n' "${path}"
}

#
# @description Print the srt settings of one dsh-superagent pnpm run (regime-cutover U317b): writes allowed under the
#   given roots alone; reads denied under the credential roots the dsh role denies (hcom-seat seat_settings_lists:
#   ~/.ssh, ~/.gnupg, ~/.aws, ~/.netrc, ~/.docker, ~/.kube, ~/.config/gcloud, ~/.codex, ~/.omp/agent); network to the
#   registry host alone; no local binding, no unix socket, no pty. Every path is clean (dsh_superagent_clean_path), so
#   the JSON needs no escaping.
# @arg $@ path The write roots.
# @stdout The settings JSON, one line.
# @exitcode 1 A path is not clean.
#
function dsh_superagent_srt_settings() {
    local path write='' deny='' sep=''
    for path in "$@"; do
        dsh_superagent_clean_path "${path}" || return 1
        write+="${sep}\"${path}\""
        sep=,
    done
    sep=''
    for path in .ssh .gnupg .aws .netrc .docker .kube .config/gcloud .codex .omp/agent; do
        dsh_superagent_clean_path "${HOME}/${path}" || return 1
        deny+="${sep}\"${HOME}/${path}\""
        sep=,
    done
    printf '{"network":{"allowedDomains":["%s"],"deniedDomains":[],"allowUnixSockets":[],"allowMachLookup":["com.apple.trustd.agent"],"allowLocalBinding":false},"filesystem":{"denyRead":[%s],"allowRead":[],"allowWrite":[%s],"denyWrite":[]},"allowPty":false}\n' "${DSH_SUPERAGENT_REGISTRY_HOST}" "${deny}" "${write}"
}

#
# @description Run pnpm for the dsh-superagent step inside srt (regime-cutover U317b): one `srt --settings <file>` whose
#   settings (dsh_superagent_srt_settings) grant writes under the given roots alone, running `/bin/sh -c` of the given
#   text in the working directory with the environment reduced by `/usr/bin/env -i` to HOME, a PATH of the mise node
#   and pnpm directories and the system directories, a TMPDIR and the XDG directories under the pnpm store, the store
#   itself (npm_config_store_dir) and pnpm's package-manager self-install off (npm_config_manage_package_manager_versions),
#   so every write of the upstream build lands under the roots or fails with srt's EPERM and fails the run.
# @arg $1 path The settings file to write (removed by the caller).
# @arg $2 path The working directory.
# @arg $3 string The shell text run inside; `"$PNPM"` is pnpm.
# @arg $@ path The write roots after it.
# @env DSH_SUPERAGENT_SRT The srt path (dsh_superagent_tool).
# @env DSH_SUPERAGENT_PNPM The pnpm path.
# @env DSH_SUPERAGENT_PATH The PATH inside.
# @env DSH_SUPERAGENT_STORE The pnpm store, a write root the caller lists.
# @exitcode 1 The settings could not be written, or the text inside failed (srt's own status included).
#
function dsh_superagent_srt_run() {
    local settings="$1" workdir="$2" script="$3" json
    shift 3
    json="$(dsh_superagent_srt_settings "$@")" || return 1
    printf '%s\n' "${json}" > "${settings}" || {
        printf 'update_dsh_superagent: the srt settings %s could not be written; nothing installed, nothing recorded.\n' "${settings}" >&2
        return 1
    }
    "${DSH_SUPERAGENT_SRT}" --settings "${settings}" -- /usr/bin/env -i "HOME=${HOME}" "PATH=${DSH_SUPERAGENT_PATH}" \
        "TMPDIR=${DSH_SUPERAGENT_STORE}/tmp" "XDG_CACHE_HOME=${DSH_SUPERAGENT_STORE}/xdg-cache" \
        "XDG_CONFIG_HOME=${DSH_SUPERAGENT_STORE}/xdg-config" "XDG_DATA_HOME=${DSH_SUPERAGENT_STORE}/xdg-data" \
        "XDG_STATE_HOME=${DSH_SUPERAGENT_STORE}/xdg-state" "npm_config_store_dir=${DSH_SUPERAGENT_STORE}" \
        npm_config_manage_package_manager_versions=false "PNPM=${DSH_SUPERAGENT_PNPM}" \
        /bin/sh -c "cd \"\$1\" && ${script}" sh "${workdir}"
}

#
# @description Install the pinned dsh-superagent bundle (assets.dsh-superagent) under $DSH_HOME/plugins/dsh-superagent
#   on a host whose operator opted in, and install the rendered router profile's plugins, which link it; nothing
#   starts it (the Router is started by `hcom-seat dsh --profile router` under srt).
# @description
#   The opt-in is update_deepseek_harness's: DSH_HOME exported, absolute and a directory whose identity (-ef) is
#   ~/.dsh's, where the kit renders the router profile. The step is the harness step's shape: GitHub's archive of the
#   pinned commit is downloaded into a mktemp directory and verified against its reviewed sha256 before anything is
#   unpacked; every member of the archive lies under its one top-level member, which must name the pinned commit (the
#   git-commit form of "the archive version equals the pin"; verdicts/U317 P2 :2403 read the first member alone); the
#   tree is unpacked under a name of its own ($DSH_HOME/plugins/dsh-superagent.XXXXXX) and built there inside srt
#   (verdicts/U317 P1 :2421: the upstream build scripts ran uncontained): one `srt --settings <tree>.srt-settings.json`
#   over `pnpm install --frozen-lockfile && pnpm build`, the settings granting writes under the tree and the pnpm store
#   $DSH_HOME/.pnpm-store alone, denying the credential roots the dsh role denies and admitting the registry host alone
#   (dsh_superagent_srt_run); srt, pnpm and node are the kit's mise pins, resolved with their status before any
#   download, and an absent one refuses the step; the download directory goes; the previous tree, when there is one,
#   is renamed aside and the new tree renamed into place (one rename publishes it, and a failed publication puts the
#   previous tree back); the router profile's plugins are installed by a second srt run whose writes are the profile
#   directory and the store (its package.json links the tree by a relative link: dependency, so the link follows the
#   directory name); the step is recorded; and only then does the previous tree go. Every input is one row of a table,
#   checked before any download:
#   DSH_HOME: exported, absolute, a directory -ef ~/.dsh (elsewhere is a WARN with exit 0; unset or absent is a skip),
#   with a physical path (pwd -P) that can be read.
#   DSH_SUPERAGENT_COMMIT: 40 lowercase hex; DSH_SUPERAGENT_SHA256: 64 lowercase hex (the rendered constants).
#   DSH_HOME/plugins, DSH_HOME/plugins/dsh-superagent, DSH_HOME/profiles, DSH_HOME/profiles/router: each absent, or a
#   directory that is not a symlink whose physical path is its spelling under the physical DSH_HOME, so no link on the
#   path from DSH_HOME down redirects a write (verdicts/U317 P2 :2347: a linked profiles/ parent passed the leaf check;
#   the rule is hcom-seat's settings_judge, every row physical); anything else is refused, never removed. An absent
#   profiles/router is a WARN with exit 0 (the kit has not rendered the profile here).
#   ~/.agents/.installed-manifest.json: absent, or a regular file that is not a symlink; the step's recorded
#   source_version equal to the pin with the tree in place is the already-installed exit (the profile install is
#   run again, under srt, only when the profile's node_modules holds no dsh-superagent entry).
#   Every producer the step reads (pwd -P, mise which, shasum, tar's member list, jq, the three mktemp) refuses the
#   step on a failed answer (standing order 21); a download that fails is one WARN line, nothing installed, nothing
#   recorded.
# @exitcode 0 Installed, already installed, no opt-in (a skip line), DSH_HOME elsewhere than ~/.dsh or the router
#   profile absent (a WARN), or the download failed (a WARN; nothing installed or recorded).
# @exitcode 1 A constant malformed, a producer read, a shape check, a tool absent, the digest check, the archive member
#   check, the unpack, the build, the publication, the profile install or the record failed; the line printed names
#   the state left.
#
function update_dsh_superagent() (
    local download_dir="" tarball actual tree="" settings="" profile_settings="" members member top previous="" recorded install_dir row
    local dsh_home_real physical srt_bin pnpm_bin node_bin
    install_dir="${DSH_HOME:-}/plugins/dsh-superagent"
    dsh_superagent_record() {
        manifest_record "update_dsh_superagent" installer "${DSH_SUPERAGENT_COMMIT}" "${install_dir}" -- "curl -fsSL ${DSH_SUPERAGENT_ARCHIVE_URL}" "shasum -a 256 <archive>" "tar tzf <archive> (every member under the one root ${DSH_SUPERAGENT_REPOSITORY##*/}-${DSH_SUPERAGENT_COMMIT})" "mktemp -d ${install_dir}.XXXXXX" "tar xzf <archive> -C <tree> --strip-components=1" "srt --settings <tree>.srt-settings.json -- pnpm install --frozen-lockfile && pnpm build (writes: <tree>, ${DSH_HOME}/.pnpm-store)" "mv <tree> ${install_dir}" "srt --settings <settings> -- pnpm install in ${DSH_HOME}/profiles/router (writes: that directory, ${DSH_HOME}/.pnpm-store)"
    }
    case ${DSH_SUPERAGENT_COMMIT:-} in
    [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) ;;
    *)
        printf 'update_dsh_superagent: DSH_SUPERAGENT_COMMIT (assets.dsh-superagent pin, rendered into scripts/lib/installer-pins.sh) is unset or not 40 lowercase hex (%s given); nothing installed, nothing recorded.\n' "${DSH_SUPERAGENT_COMMIT:-}" >&2
        return 1
        ;;
    esac
    if [ "${#DSH_SUPERAGENT_SHA256}" -ne 64 ]; then
        printf 'update_dsh_superagent: DSH_SUPERAGENT_SHA256 is not 64 characters (%s given); nothing installed, nothing recorded.\n' "${DSH_SUPERAGENT_SHA256:-}" >&2
        return 1
    fi
    if [ -z "${DSH_HOME:-}" ] || [ ! -d "${DSH_HOME}" ]; then
        printf 'dsh-superagent: DSH_HOME is not exported to an existing directory, so this host has not opted in; nothing installed.\n'
        return 0
    fi
    case ${DSH_HOME} in # lint-comparisons: allow the case reads the spelling (absolute or not); the -ef comparison below reads the identity
    /*) ;;
    *)
        printf 'WARN: update_dsh_superagent: DSH_HOME must be an absolute path (%s given); nothing installed.\n' "${DSH_HOME}" >&2
        return 0
        ;;
    esac
    if [ ! -d "${HOME}/.dsh" ] || [ ! "${DSH_HOME}" -ef "${HOME}/.dsh" ]; then
        printf 'WARN: update_dsh_superagent: DSH_HOME is %s, not %s, where the kit renders the router profile; nothing installed.\n' "${DSH_HOME}" "${HOME}/.dsh" >&2
        return 0
    fi
    # The physical-path rule (hcom-seat settings_judge; verdicts/U317 P2 :2347): DSH_HOME's physical path is read once,
    # and every directory the step writes under is held, when it exists, to be no link and to resolve to its spelling
    # under that path, so a linked profiles/ or plugins/ parent is refused before any download, like a linked leaf.
    dsh_home_real="$(cd -P -- "${DSH_HOME}" && pwd -P)" || {
        printf 'update_dsh_superagent: the physical path of DSH_HOME %s could not be read; nothing installed, nothing recorded.\n' "${DSH_HOME}" >&2
        return 1
    }
    for row in plugins plugins/dsh-superagent profiles profiles/router; do
        if [ -L "${DSH_HOME}/${row}" ] || { [ -e "${DSH_HOME}/${row}" ] && [ ! -d "${DSH_HOME}/${row}" ]; }; then
            printf 'update_dsh_superagent: %s is a symlink or not a directory; the step writes only under directories of its own there (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/${row}" >&2
            return 1
        fi
        [ -d "${DSH_HOME}/${row}" ] || continue
        physical="$(cd -P -- "${DSH_HOME}/${row}" && pwd -P)" || {
            printf 'update_dsh_superagent: the physical path of %s could not be read; nothing installed, nothing recorded.\n' "${DSH_HOME}/${row}" >&2
            return 1
        }
        if [ "${physical}" != "${dsh_home_real}/${row}" ]; then # lint-comparisons: allow both sides are pwd -P physical paths
            printf 'update_dsh_superagent: %s resolves to %s, not %s; a link on the path would redirect the writes outside DSH_HOME (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${DSH_HOME}/${row}" "${physical}" "${dsh_home_real}/${row}" >&2
            return 1
        fi
    done
    if [ ! -d "${DSH_HOME}/profiles/router" ]; then
        printf 'WARN: update_dsh_superagent: %s is absent, so the kit has not rendered the router profile here; nothing installed.\n' "${DSH_HOME}/profiles/router" >&2
        return 0
    fi
    if [ -L "${HOME}/.agents/.installed-manifest.json" ] || { [ -e "${HOME}/.agents/.installed-manifest.json" ] && [ ! -f "${HOME}/.agents/.installed-manifest.json" ]; }; then
        printf 'update_dsh_superagent: the installed-manifest receipt %s is a symlink or not a regular file; the step reads and writes only a regular file there (move it aside and rerun make update); nothing installed, nothing recorded.\n' "${HOME}/.agents/.installed-manifest.json" >&2
        return 1
    fi
    recorded=""
    if [ -f "${HOME}/.agents/.installed-manifest.json" ]; then
        recorded="$(jq -r '.steps["update_dsh_superagent"].source_version // empty' "${HOME}/.agents/.installed-manifest.json" 2> /dev/null)" || {
            printf 'update_dsh_superagent: the installed-manifest receipt could not be read; step refused.\n' >&2
            return 1
        }
    fi
    # The containment and the build tools, before any download: the upstream code runs only inside srt, so no srt is
    # no build (the kit pins @anthropic-ai/sandbox-runtime, pnpm and node in mise).
    srt_bin="$(dsh_superagent_tool srt)" || return 1
    pnpm_bin="$(dsh_superagent_tool pnpm)" || return 1
    node_bin="$(dsh_superagent_tool node)" || return 1
    DSH_SUPERAGENT_SRT="${srt_bin}" DSH_SUPERAGENT_PNPM="${pnpm_bin}" DSH_SUPERAGENT_STORE="${DSH_HOME}/.pnpm-store"
    DSH_SUPERAGENT_PATH="${pnpm_bin%/*}:${node_bin%/*}:/usr/bin:/bin"
    # ${name:+"${name}"} and `|| :` as in update_deepseek_harness: the subshell's locals may be unwound before the EXIT
    # trap runs on macOS bash, and a failing cleanup must not become the step's status.
    trap 'rm -rf ${download_dir:+"${download_dir}"} ${tree:+"${tree}"} ${settings:+"${settings}"} ${profile_settings:+"${profile_settings}"} || :' EXIT
    # srt on Linux grants writes only to paths that exist, so the store and its scratch directory are made first.
    mkdir -p "${DSH_HOME}/plugins" "${DSH_SUPERAGENT_STORE}/tmp" || {
        printf 'update_dsh_superagent: the plugin directory %s or the pnpm store %s could not be made; nothing installed, nothing recorded.\n' "${DSH_HOME}/plugins" "${DSH_SUPERAGENT_STORE}" >&2
        return 1
    }
    profile_settings="${install_dir}.profile.srt-settings.json"
    if [ "${recorded}" = "${DSH_SUPERAGENT_COMMIT}" ] && [ -f "${install_dir}/package.json" ]; then
        printf 'dsh-superagent %s is already installed at %s.\n' "${DSH_SUPERAGENT_COMMIT}" "${install_dir}"
        if [ ! -e "${DSH_HOME}/profiles/router/node_modules/dsh-superagent" ]; then
            # shellcheck disable=SC2016 # the text runs inside srt, where $PNPM is the environment the run sets
            dsh_superagent_srt_run "${profile_settings}" "${DSH_HOME}/profiles/router" '"$PNPM" install' "${DSH_HOME}/profiles/router" "${DSH_SUPERAGENT_STORE}" || {
                printf 'update_dsh_superagent: the router profile install failed; the installed tree and the record are untouched.\n' >&2
                return 1
            }
        fi
        return 0
    fi
    download_dir="$(mktemp -d "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX")" || {
        printf 'update_dsh_superagent: the download directory could not be made; step refused.\n' >&2
        return 1
    }
    tarball="${download_dir}/dsh-superagent-${DSH_SUPERAGENT_COMMIT}.tar.gz"
    curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${DSH_SUPERAGENT_ARCHIVE_URL}" -o "${tarball}" || {
        printf 'WARN: update_dsh_superagent: the dsh-superagent archive could not be downloaded (%s); nothing installed, nothing recorded; the existing install is unchanged and the next make update retries.\n' "${DSH_SUPERAGENT_ARCHIVE_URL}" >&2
        return 0
    }
    actual="$(shasum -a 256 "${tarball}")" || {
        printf 'update_dsh_superagent: the digest of the downloaded archive could not be read; install refused.\n' >&2
        return 1
    }
    if [ "${actual%% *}" != "${DSH_SUPERAGENT_SHA256}" ]; then
        printf 'dsh-superagent checksum mismatch: expected %s, got %s.\n' "${DSH_SUPERAGENT_SHA256}" "${actual%% *}" >&2
        return 1
    fi
    # GitHub's commit archive has one root member, <repository>-<commit>/; a verified archive whose root names another
    # commit is a constant pairing error (the digest of one pin beside the commit of another) and is refused. Every
    # member is then held under that root (verdicts/U317 P2 :2403: a digest-matching archive with a second root
    # installed the second root's package.json through --strip-components=1), before anything is unpacked.
    members="${download_dir}/members"
    tar tzf "${tarball}" > "${members}" || {
        printf 'update_dsh_superagent: the member list of the archive could not be read; install refused.\n' >&2
        return 1
    }
    IFS= read -r member < "${members}" || {
        printf 'update_dsh_superagent: the archive lists no member; install refused.\n' >&2
        return 1
    }
    top="${member%%/*}"
    if [ "${top}" != "${DSH_SUPERAGENT_REPOSITORY##*/}-${DSH_SUPERAGENT_COMMIT}" ]; then
        printf 'dsh-superagent archive root %s does not name the pin %s; install refused.\n' "${top}" "${DSH_SUPERAGENT_COMMIT}" >&2
        return 1
    fi
    while IFS= read -r member; do
        case ${member} in # lint-comparisons: allow archive member names are data, not paths of this host
        "${top}" | "${top}/" | "${top}/"?*) ;;
        *)
            printf 'dsh-superagent archive member %s lies outside the one root %s that names the pin; install refused before anything is unpacked.\n' "${member}" "${top}" >&2
            return 1
            ;;
        esac
    done < "${members}"
    tree="$(mktemp -d "${install_dir}.XXXXXX")" || {
        printf 'update_dsh_superagent: the install tree under %s could not be made; install refused.\n' "${DSH_HOME}/plugins" >&2
        return 1
    }
    settings="${tree}.srt-settings.json"
    tar xzf "${tarball}" -C "${tree}" --strip-components=1 || return 1
    # The upstream build runs inside srt alone (verdicts/U317 P1 :2421): one invocation over both pnpm steps, writes
    # under the new tree and the pnpm store, reads denied under the credential roots, network to the registry host.
    # shellcheck disable=SC2016 # the text runs inside srt, where $PNPM is the environment the run sets
    dsh_superagent_srt_run "${settings}" "${tree}" '"$PNPM" install --frozen-lockfile && "$PNPM" build' "${tree}" "${DSH_SUPERAGENT_STORE}" || {
        printf 'update_dsh_superagent: the build failed inside srt (a write outside the new tree and %s is refused there); the new tree is removed; nothing installed, nothing recorded; the previous install, when there is one, is unchanged.\n' "${DSH_SUPERAGENT_STORE}" >&2
        return 1
    }
    rm -f "${settings}" || :
    settings=""
    rm -rf "${download_dir}" || printf 'WARN: update_dsh_superagent: the download directory %s could not be removed; it holds only the verified archive and the next make update makes a new one.\n' "${download_dir}" >&2
    download_dir=""
    if [ -d "${install_dir}" ]; then
        previous="$(mktemp -d "${install_dir}.previous.XXXXXX")" || {
            printf 'update_dsh_superagent: a directory for the previous tree could not be made; the new tree is removed; nothing installed, nothing recorded.\n' >&2
            return 1
        }
        if ! rmdir "${previous}" || ! mv "${install_dir}" "${previous}"; then
            printf 'update_dsh_superagent: the previous tree %s could not be renamed aside; the new tree is removed; nothing installed, nothing recorded.\n' "${install_dir}" >&2
            return 1
        fi
    fi
    mv "${tree}" "${install_dir}" || {
        [ -z "${previous}" ] || mv "${previous}" "${install_dir}" || printf 'update_dsh_superagent: the previous tree could not be put back from %s.\n' "${previous}" >&2
        printf 'update_dsh_superagent: the new tree could not be renamed into %s; the new tree is removed; nothing recorded.\n' "${install_dir}" >&2
        return 1
    }
    tree=""
    # shellcheck disable=SC2016 # the text runs inside srt, where $PNPM is the environment the run sets
    dsh_superagent_srt_run "${profile_settings}" "${DSH_HOME}/profiles/router" '"$PNPM" install' "${DSH_HOME}/profiles/router" "${DSH_SUPERAGENT_STORE}" || {
        printf 'update_dsh_superagent: the router profile install failed inside srt; the new tree is at %s but nothing is recorded, so the next make update installs again%s.\n' "${install_dir}" "${previous:+; the previous tree is kept at ${previous}}" >&2
        return 1
    }
    printf 'dsh-superagent %s installed into %s.\n' "${DSH_SUPERAGENT_COMMIT}" "${install_dir}"
    dsh_superagent_record || {
        printf 'update_dsh_superagent: the record failed; the tree at %s stands unrecorded and the next make update installs again%s.\n' "${install_dir}" "${previous:+; the previous tree is kept at ${previous}}" >&2
        return 1
    }
    # Only now, with the record written, does the previous tree go.
    [ -z "${previous}" ] || rm -rf "${previous}" || printf 'WARN: update_dsh_superagent: the previous tree %s could not be removed; remove it by hand.\n' "${previous}" >&2
)

#
# @description Load the installed pi-claude-bridge in one omp session and fail on a load error.
# @description
#   `omp models` never evaluates extension modules, so the check is the session path: a one-prompt run under
#   `--no-extensions -e <install dir>` whose stderr and the omp log files it wrote must not contain `Failed to
#   load extension`, and which must reach the model (`PONG`, or `Not logged in` before the operator's /login).
#   Point HOME at a scratch directory to keep the session out of the real ~/.omp; under the real HOME a logged-in
#   host spends one short model turn.
# @exitcode 1 omp reported a load error or did not reach the model; omp's output is printed above the verdict.
#
function check_pi_claude_bridge() {
    local install_dir="${HOME}/.local/lib/omp-extensions/pi-claude-bridge" marker output failed_logs
    [ -d "${install_dir}" ] || {
        printf 'pi-claude-bridge is not installed at %s; run make update.\n' "${install_dir}" >&2
        return 1
    }
    marker="$(mktemp "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX")" || return
    output="$(perl -e 'alarm 90; exec @ARGV' omp --no-extensions -e "${install_dir}" --no-session --model claude-bridge/claude-haiku-4-5 --max-time 60 -p "Reply with the single word PONG." 2>&1)" || true
    printf '%s\n' "${output}"
    # The stderr line is truncated to the display width; the log carries the full error.
    failed_logs="$(find "${HOME}/.omp/logs" -name 'omp.*.log' -newer "${marker}" -exec grep -l 'Failed to load extension' {} + 2> /dev/null || true)"
    rm -f "${marker}"
    if printf '%s\n' "${output}" | grep -q 'Failed to load extension' || [ -n "${failed_logs}" ]; then
        printf 'pi-claude-bridge did not load in omp%s.\n' "${failed_logs:+; omp log: ${failed_logs}}" >&2
        return 1
    fi
    if ! printf '%s\n' "${output}" | grep -Eq 'PONG|Not logged in'; then
        printf 'pi-claude-bridge loaded but omp did not reach the model.\n' >&2
        return 1
    fi
    local version
    version="$(omp_version_label)"
    printf 'pi-claude-bridge loaded in %s.\n' "${version}"
}

#
# @description Print the version `omp --version` reports on its first line, or `unknown` when omp cannot report
#   one: the version only labels a success message, so its read failing changes no decision.
#
function omp_version_label() {
    local output
    if output="$(omp --version 2> /dev/null)"; then
        awk 'NR == 1 { print $NF }' <<< "${output}"
    else
        printf 'unknown\n'
    fi
}

#
# @description Confirm the pstack skills chezmoi places under ~/.agents/pstack/skills reach the plain omp launch.
# @description
#   No installer step runs for pstack: the external in home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl
#   deploys the pinned plugin's skills/* and docs/** (assets.pstack in the manifest) at every chezmoi apply, into a
#   root only the omp consumers skills.pstack.audience names load. The check fails when the poteto-mode skill or the
#   Claude Code adapter its first paragraph links is missing, or when `omp skill list`, run from an empty directory
#   so no project skill tree takes part, does not name poteto-mode. Without omp the file check alone decides.
# @exitcode 1 A file is missing or omp does not list the skill; omp's listing is printed above the verdict.
#
function check_pstack() {
    local file cwd listing count version
    for file in "${HOME}/.agents/pstack/skills/poteto-mode/SKILL.md" "${HOME}/.agents/pstack/docs/harness/claude-code.md"; do
        [ -f "${file}" ] || {
            printf 'pstack: %s is missing; run make update.\n' "${file}" >&2
            return 1
        }
    done
    has_command omp || {
        printf 'pstack skills are in place; omp is not installed, so the seat listing is not checked.\n'
        return 0
    }
    cwd="$(mktemp -d "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX")" || return
    listing="$(cd "${cwd}" && perl -e 'alarm 60; exec @ARGV' omp --no-session skill list --json 2> /dev/null)" || true
    rmdir "${cwd}"
    if ! printf '%s\n' "${listing}" | jq -e '.skills[] | select(.name == "poteto-mode")' > /dev/null 2>&1; then
        printf '%s\n' "${listing}" >&2
        printf 'pstack: omp skill list does not name poteto-mode.\n' >&2
        return 1
    fi
    count="$(jq '.skills | length' <<< "${listing}")" || return 1
    version="$(omp_version_label)"
    printf 'pstack skills reach %s: %s skills listed, poteto-mode among them.\n' "${version}" "${count}"
}

#
# @description Remove the copies of the pstack skills the retired ~/.agents/skills external left there.
# @description
#   Until U87 the pstack external extracted into ~/.agents/skills, which Codex and omp's agents provider list for
#   every agent; it now extracts into ~/.agents/pstack/skills, and chezmoi does not delete what the old external
#   placed. A directory ~/.agents/skills/<name> goes only when ~/.agents/pstack/skills/<name> exists and the two
#   trees are byte-identical (`diff -r`), so a skill with the same name and other content stays; make doctor then
#   reports it as listed outside its audience. Every path component below $HOME on the way to a removal
#   (~/.agents, ~/.agents/skills and the skill directory) must be a real directory, not a symlink, and the
#   directory's physical path must equal $HOME's physical path plus .agents/skills/<name>; otherwise the step
#   refuses before it removes anything. Every pair is checked first and removal starts only when all passed, so a
#   refusal deletes nothing. Without the pstack root (chezmoi apply has not run) nothing is touched.
# @exitcode 1 A component is a symlink, a physical path differs, diff could not compare a pair (exit 2), or a
#   removal failed; the path is named.
#
function retire_shared_pstack_copies() {
    local pstack_root="${HOME}/.agents/pstack/skills" shared_root="${HOME}/.agents/skills"
    local source name target status physical_home physical dir
    local -a remove=()
    [ -d "${pstack_root}" ] || return 0
    for dir in "${HOME}/.agents" "${shared_root}"; do
        if [ -L "${dir}" ]; then
            printf 'pstack: %s is a symlink; refusing to remove anything under it.\n' "${dir}" >&2
            return 1
        fi
    done
    [ -d "${shared_root}" ] || return 0
    physical_home="$(cd -P -- "${HOME}" && pwd -P)" || {
        printf 'pstack: cannot resolve the physical path of %s.\n' "${HOME}" >&2
        return 1
    }
    for source in "${pstack_root}"/*/; do
        [ -d "${source}" ] || continue
        name="${source%/}"
        name="${name##*/}"
        target="${shared_root}/${name}"
        if [ -L "${target}" ]; then
            printf 'pstack: %s is a symlink; refusing to remove anything.\n' "${target}" >&2
            return 1
        fi
        [ -d "${target}" ] || continue
        status=0
        diff -r -q "${source}" "${target}" > /dev/null 2>&1 || status=$?
        case "${status}" in
        0)
            physical="$(cd -P -- "${target}" && pwd -P)" || {
                printf 'pstack: cannot resolve the physical path of %s.\n' "${target}" >&2
                return 1
            }
            if [ "${physical}" != "${physical_home}/.agents/skills/${name}" ]; then # lint-comparisons: allow both sides are pwd -P physical paths
                printf 'pstack: %s resolves to %s, not under %s/.agents/skills; refusing to remove anything.\n' \
                    "${target}" "${physical}" "${physical_home}" >&2
                return 1
            fi
            remove+=("${physical}")
            ;;
        1) printf 'pstack: kept %s: it differs from %s.\n' "${target}" "${source%/}" >&2 ;;
        *)
            printf 'pstack: cannot compare %s with %s (diff exit %s).\n' "${target}" "${source%/}" "${status}" >&2
            return 1
            ;;
        esac
    done
    for physical in "${remove[@]+"${remove[@]}"}"; do
        rm -r -- "${physical}" || {
            printf 'pstack: cannot remove the retired copy %s.\n' "${physical}" >&2
            return 1
        }
        printf 'pstack: removed the retired copy %s (identical to %s/%s).\n' "${physical}" "${pstack_root}" "${physical##*/}"
    done
}

#
# @description Remove the retired mryfmo-dev-workflows entry from the live ~/.agents/plugins/marketplace.json.
# @description
#   The marketplace is a create_ seed: chezmoi writes it once and never again, so a host that has it keeps the entry
#   U87 retired while .chezmoiremove deletes the plugin directory it points at. The step parses the file strictly
#   (JSON only, no duplicate keys, no NaN or Infinity, no number that overflows or underflows a float, a top-level
#   object whose plugins is a list), removes exactly the entry named mryfmo-dev-workflows whose source is the local
#   ./plugins/mryfmo-dev-workflows, keeps every other entry and key in its order, and replaces the file atomically
#   with its mode kept. Before the replace, the new text is parsed again with every number read exactly
#   (decimal.Decimal for fractions and exponents) and must equal the old file's exact parse minus the removed entry;
#   any difference (a number the rewrite would change) refuses. A file without that entry is not rewritten, so a
#   second run changes nothing. An entry with that name and another source is kept and named. A missing file is
#   nothing to do.
# @exitcode 1 The file is a symlink, is not valid JSON of that shape, holds a number the rewrite would change, or
#   cannot be rewritten; it is left unchanged.
#
function retire_marketplace_dev_workflows() {
    local marketplace="${HOME}/.agents/plugins/marketplace.json"
    [ -e "${marketplace}" ] || [ -L "${marketplace}" ] || return 0
    if [ -L "${marketplace}" ]; then
        printf 'marketplace: %s is a symlink; left unchanged.\n' "${marketplace}" >&2
        return 1
    fi
    python3 - "${marketplace}" << 'PY'
import decimal
import json
import math
import os
import shutil
import sys
import tempfile

path = sys.argv[1]
RETIRED = {"name": "mryfmo-dev-workflows", "source": {"path": "./plugins/mryfmo-dev-workflows", "source": "local"}}


def unique_keys(pairs):
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ValueError(f"duplicate key in {keys}")
    return dict(pairs)


def no_constant(name):
    raise ValueError(f"{name} is not JSON")


def finite_float(text):
    value = float(text)
    if not math.isfinite(value):
        raise ValueError(f"{text} overflows a float")
    return value


def load(text, parse_float):
    return json.loads(text, object_pairs_hook=unique_keys, parse_constant=no_constant, parse_float=parse_float)


try:
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    data = load(text, finite_float)
    exact = load(text, decimal.Decimal)
except (OSError, UnicodeDecodeError, ValueError) as error:
    sys.exit(f"marketplace: cannot read {path} ({error}); left unchanged.")
if not isinstance(data, dict) or not isinstance(data.get("plugins"), list):
    sys.exit(f"marketplace: {path} is not an object with a plugins list; left unchanged.")
removed = set()
for index, entry in enumerate(data["plugins"]):
    if isinstance(entry, dict) and entry.get("name") == RETIRED["name"]:
        if entry.get("source") == RETIRED["source"]:
            removed.add(index)
            continue
        print(f"marketplace: kept {RETIRED['name']} in {path}: its source is not {RETIRED['source']}", file=sys.stderr)
if not removed:
    sys.exit(0)
data["plugins"] = [entry for index, entry in enumerate(data["plugins"]) if index not in removed]
exact["plugins"] = [entry for index, entry in enumerate(exact["plugins"]) if index not in removed]
new_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
try:
    same = load(new_text, decimal.Decimal) == exact
except ValueError:
    same = False
if not same:
    sys.exit(f"marketplace: removing the entry would change other values in {path}; left unchanged.")
handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=os.path.dirname(path), delete=False)
try:
    with handle:
        handle.write(new_text)
    shutil.copymode(path, handle.name)
    os.replace(handle.name, path)
except OSError as error:
    if os.path.exists(handle.name):
        os.unlink(handle.name)
    sys.exit(f"marketplace: cannot rewrite {path} ({error}); left unchanged.")
print(f"marketplace: removed the retired {RETIRED['name']} entry from {path}.")
PY
}

#
# @description Uninstall the retired Understand-Anything Claude Code plugin and remove its marketplace.
# @description
#   .chezmoiremove deletes the plugin's cache and marketplace clone, but installed_plugins.json and the
#   enabledPlugins entry still name it, and manifest_prune_retired drops the record remove-agent-asset would use,
#   so make doctor would report a plugin with no files on every run. Claude Code owns both files, so only its own
#   commands change them, each run outside any project and naming `--scope user`, the kit's boundary: without it
#   `marketplace remove` drops the declaration from every scope and with it the project and local installation
#   records (Claude Code 2.1.316). The marketplace list carries no scope, so the removal runs with `--json`, and
#   its `not_configured` refusal (no user-scope declaration) is a WARN, not a failure. Every read comes
#   before the first change: the marketplace list (a host where it does not work yet gets the plugin steps' WARN
#   and no change), then the installation records. A user-scope installation is uninstalled only when the
#   understand-anything marketplace is registered from the kit's source; a project or local one is the project's
#   and is only reported. With nothing installed and no marketplace, a stale user enabledPlugins entry is disabled:
#   `claude plugin list` omits a plugin that is not installed and `claude plugin uninstall` refuses one (Claude
#   Code 2.1.316), so `disable --scope user` is the command that clears it. main runs it after the Claude plugin
#   convergence: the claude CLI is repaired by then, and a failure here (set -e) skips no pin check.
# @stdout One line per command run.
# @stderr A WARN per record left in place, `already retired` when nothing was present, or the skip line.
# @exitcode 0 When retired or already retired, and when the marketplace list cannot be read (a WARN).
# @exitcode 1 When installed_plugins.json or settings.json cannot be read, or a claude command fails; no later
#   command runs.
#
function retire_understand_anything() {
    local plugin_id="understand-anything@understand-anything" marketplace="understand-anything"
    local source="Egonex-AI/Understand-Anything" listing state reason installs count index scope project enabled
    local removal failure status=0 users=0 found=0

    if ! has_command claude; then
        printf 'Skipping the Understand-Anything retirement: claude command not found.\n' >&2
        return 0
    fi
    listing="$(claude_outside_projects plugin marketplace list --json)" || status=$?
    reason="exit ${status}"
    if [ "${status}" -eq 0 ]; then
        # The parser's error goes into the WARN, so a host without a working claude logs no ERROR line.
        state="$(pin_record claude-marketplace "${marketplace}" "${source}" <<< "${listing}" 2>&1)" || status=$?
        [ "${status}" -eq 0 ] || reason="${state#ERROR: }"
    fi
    if [ "${status}" -ne 0 ]; then
        printf 'WARN: claude plugin %s was not retired: "claude plugin marketplace list --json" gave no marketplace list (%s), so its marketplace cannot be verified on this host, and nothing was uninstalled, removed or disabled. Run make update once "claude plugin marketplace list" works.\n' "${plugin_id}" "${reason}" >&2
        return 0
    fi
    case "${state}" in
    registered | foreign | absent) ;;
    *)
        printf 'ERROR: unexpected marketplace state %q for %s.\n' "${state}" "${marketplace}" >&2
        return 1
        ;;
    esac
    if ! installs="$(claude_plugin_installs "${plugin_id}")"; then
        printf 'ERROR: cannot read %s; %s is not retired.\n' "${AGENT_CLAUDE_DIR}/plugins/installed_plugins.json" "${plugin_id}" >&2
        return 1
    fi
    count="$(jq -er 'length' <<< "${installs}")" || return 1
    for ((index = 0; index < count; index++)); do
        scope="$(jq -er ".[${index}].scope" <<< "${installs}")" || return 1
        found=1
        case "${scope}" in
        user)
            users=1
            case "${state}" in
            registered)
                if ! claude_outside_projects plugin uninstall "${plugin_id}" --scope user; then
                    printf 'ERROR: claude plugin uninstall %s --scope user failed.\n' "${plugin_id}" >&2
                    return 1
                fi
                printf 'Ran: claude plugin uninstall %s --scope user\n' "${plugin_id}"
                ;;
            foreign)
                printf 'WARN: the user-scope %s comes from the marketplace %s registered from another source than %s; left in place.\n' "${plugin_id}" "${marketplace}" "${source}" >&2
                ;;
            absent)
                printf 'WARN: the user-scope %s names the marketplace %s, which is not registered, so its source cannot be verified; left in place.\n' "${plugin_id}" "${marketplace}" >&2
                ;;
            esac
            ;;
        project | local)
            project="$(jq -er ".[${index}].projectPath // \"(no project path)\"" <<< "${installs}")" || return 1
            printf 'WARN: %s has a %s-scope installation in %s, outside the user scope the kit manages; this step does not uninstall it (in that project: claude plugin uninstall %s --scope %s).\n' "${plugin_id}" "${scope}" "${project}" "${plugin_id}" "${scope}" >&2
            ;;
        *)
            printf 'ERROR: unexpected installation scope %q for %s.\n' "${scope}" "${plugin_id}" >&2
            return 1
            ;;
        esac
    done
    case "${state}" in
    registered)
        removal="$(claude_outside_projects plugin marketplace remove "${marketplace}" --scope user --json)" || status=$?
        if [ "${status}" -eq 0 ]; then
            printf 'Ran: claude plugin marketplace remove %s --scope user\n' "${marketplace}"
        elif failure="$(jq -er '.failureCode' <<< "${removal##*$'\n'}" 2> /dev/null)" && [ "${failure}" = not_configured ]; then
            printf 'WARN: the Claude Code marketplace %s is not declared in the user settings (a project or local declaration); left in place.\n' "${marketplace}" >&2
        else
            printf 'ERROR: claude plugin marketplace remove %s --scope user failed (exit %s).\n' "${marketplace}" "${status}" >&2
            return 1
        fi
        found=1
        ;;
    foreign)
        printf 'WARN: the Claude Code marketplace %s is registered from another source than %s; left in place.\n' "${marketplace}" "${source}" >&2
        found=1
        ;;
    esac
    if [ "${users}" -eq 0 ] && [ "${state}" = absent ]; then
        if ! enabled="$(claude_user_enabled "${plugin_id}")"; then
            printf 'ERROR: cannot read %s; %s is not retired.\n' "${AGENT_CLAUDE_DIR}/settings.json" "${plugin_id}" >&2
            return 1
        fi
        case "${enabled}" in
        enabled)
            if ! claude_outside_projects plugin disable "${plugin_id}" --scope user; then
                printf 'ERROR: claude plugin disable %s --scope user failed.\n' "${plugin_id}" >&2
                return 1
            fi
            printf 'Ran: claude plugin disable %s --scope user\n' "${plugin_id}"
            found=1
            ;;
        disabled | unset) ;;
        *)
            printf 'WARN: the user settings hold %s for %s, which disable cannot clear; left in place.\n' "${enabled}" "${plugin_id}" >&2
            found=1
            ;;
        esac
    fi
    [ "${found}" -eq 1 ] || printf 'Understand-Anything: already retired.\n' >&2
}

#
# @description Remove the launcher shim the retired agmsg skill wrote to ~/.agents/bin/agy-tui.
# @description
#   agmsg wrote ~/.agents/bin/agy-tui outside its skill tree, so .chezmoiremove (which deletes ~/.agents/skills/agmsg)
#   leaves it behind, dangling, and make doctor reports ~/.agents/bin as an orphaned agent asset. Every operation is
#   fd-relative, with no path walked again: $HOME is opened, then `.agents` and `bin` below it with
#   O_DIRECTORY|O_NOFOLLOW (a symlink at either refuses), and the shim is lstat'ed, opened, moved and deleted, and
#   `bin` removed, only relative to those open directories. The shim goes only on positive proof: a regular file
#   (fstatat) opened with O_NOFOLLOW|O_NONBLOCK whose fstat is the same device and inode, read completely, holding
#   the exact line `# agmsg-shim-owner: $HOME/.agents/skills/agmsg/scripts/drivers/types/antigravity/agy-tui.sh`, and
#   an owner (looked up below the open `.agents`) whose lstat fails with ENOENT. Every other outcome keeps the file
#   and fails the step with the reason. Removal is by the verified inode: the entry is renamed (renameat, atomic) into
#   a private quarantine directory created in the open `bin`, and unlinked there only when its device and inode are
#   the verified ones; anything else is linked back under its name (linkat, never over a newer entry) and the step
#   fails. `bin` is then removed (unlinkat AT_REMOVEDIR relative to `.agents`) only when its lstat is still the
#   directory opened above and it is empty; ENOTEMPTY or EEXIST keeps it. A missing `.agents`, `bin` or shim is
#   nothing to do, so a second run changes nothing. Guaranteed: no path is followed through a symlink, and the inode
#   deleted is the verified one. A same-user process racing the step inside the operator's own $HOME is the
#   same-user class accepted under G17: a residual, not a guarantee.
# @exitcode 1 No positive proof for an existing ~/.agents/bin/agy-tui, or a removal failed; the reason is printed.
#
function retire_agmsg_shim() {
    python3 - "${HOME}" << 'PY'
import errno
import os
import secrets
import stat
import sys

home = sys.argv[1]
agents = os.path.join(home, ".agents")
bin_dir = os.path.join(agents, "bin")
shim = os.path.join(bin_dir, "agy-tui")
owner_rel = "skills/agmsg/scripts/drivers/types/antigravity/agy-tui.sh"
owner = os.path.join(agents, owner_rel)
marker = f"# agmsg-shim-owner: {owner}"
DIRECTORY = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


def refuse(reason):
    sys.exit(f"agmsg: kept {shim}: {reason}.")


def open_directory(name, parent_fd, label):
    """The directory NAME below PARENT_FD, opened without following a symlink; None when it does not exist."""
    try:
        return os.open(name, DIRECTORY, dir_fd=parent_fd)
    except FileNotFoundError:
        return None
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            refuse(f"{label} is not a real directory")
        refuse(f"cannot open {label} ({error})")


try:
    home_fd = os.open(home, os.O_RDONLY | os.O_DIRECTORY)
except OSError as error:
    refuse(f"cannot open {home} ({error})")
agents_fd = open_directory(".agents", home_fd, agents)
if agents_fd is None:
    sys.exit(0)
bin_fd = open_directory("bin", agents_fd, bin_dir)
if bin_fd is None:
    sys.exit(0)
bin_status = os.fstat(bin_fd)
try:
    shim_status = os.stat("agy-tui", dir_fd=bin_fd, follow_symlinks=False)
except FileNotFoundError:
    sys.exit(0)
except OSError as error:
    refuse(f"cannot lstat it ({error})")
# Only a regular file is opened (a FIFO would block the open), without following a symlink swapped in and without
# blocking; fstat must then show the same regular file lstat saw.
if not stat.S_ISREG(shim_status.st_mode):
    refuse("it is not a regular file")
verified = (shim_status.st_dev, shim_status.st_ino)
try:
    fd = os.open("agy-tui", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=bin_fd)
except OSError as error:
    refuse(f"cannot open it without following a symlink ({error})")
with os.fdopen(fd, "rb") as handle:
    try:
        opened = os.fstat(handle.fileno())
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != verified:
            refuse("it changed while it was read")
        data = handle.read()
    except OSError as error:
        refuse(f"cannot read it ({error})")
if marker.encode() not in data.split(b"\n"):
    refuse(f"it does not hold the line {marker!r}, so it is not the retired agmsg shim")
try:
    os.stat(owner_rel, dir_fd=agents_fd, follow_symlinks=False)
except FileNotFoundError:
    pass
except OSError as error:
    refuse(f"cannot prove its owner {owner} is gone ({error})")
else:
    refuse(f"its owner {owner} still exists")
# Verified: from here on, nothing is removed by name.
quarantine = f".agmsg-retire-{secrets.token_hex(8)}"
try:
    os.mkdir(quarantine, 0o700, dir_fd=bin_fd)
    quarantine_fd = os.open(quarantine, DIRECTORY, dir_fd=bin_fd)
    os.rename("agy-tui", "agy-tui", src_dir_fd=bin_fd, dst_dir_fd=quarantine_fd)
    moved = os.stat("agy-tui", dir_fd=quarantine_fd, follow_symlinks=False)
except OSError as error:
    try:
        os.rmdir(quarantine, dir_fd=bin_fd)  # only when the move did not happen: rmdir keeps a non-empty one
    except OSError:
        pass
    sys.exit(f"agmsg: cannot move the retired shim {shim} aside to remove it ({error}).")
if (moved.st_dev, moved.st_ino) != verified:
    try:
        # link never replaces an entry that appeared under the name meanwhile; rename would.
        os.link("agy-tui", "agy-tui", src_dir_fd=quarantine_fd, dst_dir_fd=bin_fd, follow_symlinks=False)
        os.unlink("agy-tui", dir_fd=quarantine_fd)
        os.rmdir(quarantine, dir_fd=bin_fd)
    except OSError as error:
        sys.exit(f"agmsg: {shim} changed before its removal; the entry moved aside stays in {bin_dir}/{quarantine} ({error}).")
    refuse("it changed before its removal (another file took its name); the replacement is back in place")
try:
    os.unlink("agy-tui", dir_fd=quarantine_fd)
    os.rmdir(quarantine, dir_fd=bin_fd)
except OSError as error:
    sys.exit(f"agmsg: cannot remove the retired shim moved to {bin_dir}/{quarantine} ({error}).")
print(f"agmsg: removed the retired shim {shim}.")
# Removed: only the bin directory opened above may go.
try:
    current = os.stat("bin", dir_fd=agents_fd, follow_symlinks=False)
except OSError as error:
    sys.exit(f"agmsg: cannot lstat {bin_dir} again ({error}).")
if (current.st_dev, current.st_ino) != (bin_status.st_dev, bin_status.st_ino):
    print(f"agmsg: kept {bin_dir}: it is not the directory the shim was removed from.")
    sys.exit(0)
try:
    os.rmdir("bin", dir_fd=agents_fd)
except OSError as error:
    if error.errno in (errno.ENOTEMPTY, errno.EEXIST):
        print(f"agmsg: kept {bin_dir}: it holds other entries.")
        sys.exit(0)
    sys.exit(f"agmsg: cannot remove the empty {bin_dir} ({error}).")
print(f"agmsg: removed the empty {bin_dir}.")
PY
}

#
# @description Replace a sync step's manifest record with a failure mark the doctor reports. The mark is a record
#   of the step whose one path, under the destination, no sync ever writes, so make doctor shows the step with a
#   missing path and its repair runs the step again; the record of an earlier completed sync goes with it
#   (verdicts/U283: a failed partial sync kept the older record, the recorded directory existed, and the doctor
#   reported nothing while the payload was missing). A mark that cannot be written is counted and returned as the
#   failure it is: the doctor reads the manifest's records, never the directory's mode, so an older record that a
#   0555 ~/.agents keeps readable would show a present payload over a missing one (verdicts/U283b). The caller
#   writes the mark before its sync and syncs nothing when the mark was not written.
# @arg $1 string Step name.
# @arg $2 string Source version the sync attempted.
# @arg $3 path The destination.
# @arg $4 string What failed, kept as the record's command line.
# @exitcode 1 The mark was not written (counted); the manifest holds what it held.
#
function mark_sync_failed() {
    manifest_record "$1" rsync "$2" "$3/.sync-incomplete" -- "$4" || {
        record_claude_failure "marking $1 failed in the installed asset manifest"
        return 1
    }
}

#
# @description Sync the vendored CompactionDB tree without deleting project runtime state.
# @description
#   The version is read first, then the asset root is made and the destination proven (assert_asset_destination),
#   then the failure mark is written, then rsync runs, then the payload is verified present (the synced CHANGELOG.md
#   names the source's version), and the record is the last write: a failed rsync or an absent payload is counted
#   and marks the step failed with its cause (mark_sync_failed), so the run, full or single-step, fails at
#   fail_on_pin_failures and make doctor reports the step until a run syncs the tree (verdicts/U276b: an exit 0
#   after rsync 77 recorded an installation whose payload was absent; verdicts/U283: a failed partial sync kept the
#   older record and the doctor reported nothing). The mark before the sync is the record every later failure
#   leaves behind, the failure of its own rewrite included (verdicts/U283b: ~/.agents mode 0555 after a failed
#   partial sync kept the older record readable and the doctor named nothing); a mark that cannot be written is
#   counted and the sync does not start, so the recorded state and the payload still agree.
# @exitcode 0 Synced and recorded, or a failure counted for the run's end.
# @exitcode 1 The version could not be read or the destination was refused; nothing synced, nothing recorded.
#
function update_compactiondb() {
    local source_root version synced destination="${HOME}/.agents/compactiondb"
    source_root="${DOTFILES_REPO_SOURCE_DIR}/vendor/compactiondb/"
    version="$(awk '/^## / { print $2; exit }' "${source_root}CHANGELOG.md")" || {
        printf 'Cannot read the CompactionDB version from %sCHANGELOG.md.\n' "${source_root}" >&2
        return 1
    }
    mkdir -p "${destination%/*}" || return 1
    assert_asset_destination "${destination}" || return 1
    mark_sync_failed update_compactiondb "${version}" "${destination}" "the sync began and no completed sync has been recorded since" || return 0
    rsync -a --delete --exclude '.claude/contextdb/state/' --exclude '.claude/contextdb/spool/' --exclude '.claude/contextdb/health/' --exclude '.claude/contextdb/contextdb.sqlite3*' "${source_root}" "${destination}/" || {
        synced="rsync exit $?"
        record_claude_failure "syncing the CompactionDB tree to ${destination} (${synced})"
        # The cause replaces the mark's text when it can; a failure of this write is counted inside mark_sync_failed
        # and the mark written before the sync stands, so its status decides nothing more (errexit would end the run).
        mark_sync_failed update_compactiondb "${version}" "${destination}" "${synced}: the sync did not complete" || :
        return 0
    }
    synced="$(awk '/^## / { print $2; exit }' "${destination}/CHANGELOG.md" 2> /dev/null)" || synced=""
    if [ "${synced}" != "${version}" ]; then
        record_claude_failure "verifying the CompactionDB tree at ${destination} (its CHANGELOG.md names ${synced:-no version}, the source ${version})"
        mark_sync_failed update_compactiondb "${version}" "${destination}" "rsync exit 0 but ${destination}/CHANGELOG.md names ${synced:-no version}: the payload is not present" || :
        return 0
    fi
    manifest_record "update_compactiondb" rsync "${version}" "${destination}" -- "rsync -a --delete --exclude .claude/contextdb/state/ --exclude .claude/contextdb/spool/ --exclude .claude/contextdb/health/ --exclude .claude/contextdb/contextdb.sqlite3* ${source_root} ${destination}/" ||
        record_claude_failure "recording update_compactiondb in the installed asset manifest"
}

#
# @description Drop the manifest records of steps this updater no longer defines, counting a failed prune like every
#   other failure the run records. The library's manifest_prune_retired swallows the failure (a warning, exit 0) for
#   callers that prune as housekeeping; here an exit 0 must mean the manifest holds no retired record, so the pruner
#   itself is called and a corrupt manifest or a failed rewrite fails the run at fail_on_pin_failures (verdicts/U276b).
# @stdout One line per pruned step.
#
function prune_retired_manifest_steps() {
    _manifest_prune_retired || record_claude_failure "pruning the retired steps from the installed asset manifest"
}

#
# @description Install and refresh managed agent plugin assets, or run one step alone when its name is the only
#   argument (make doctor's checks, the coordinator's deploy of one pin). The single-step run ends with the full
#   run's exit rule, fail_on_pin_failures, so its exit 0 means the step did what it says.
# @arg $1 string Optional single step: update_omp, update_hcom, update_pi_claude_bridge, update_security_audit_skill, update_deepseek_harness, update_dsh_superagent, update_compactiondb, prune_retired_manifest_steps, check_pi_claude_bridge, check_pstack, retire_shared_pstack_copies, retire_marketplace_dev_workflows, retire_understand_anything or retire_agmsg_shim.
# @exitcode 2 The arguments name no single step; nothing ran.
#
function main() {
    if [ "$#" -gt 0 ]; then
        case "$#:$1" in
        1:update_omp | 1:update_hcom | 1:update_pi_claude_bridge | 1:update_security_audit_skill | 1:update_deepseek_harness | 1:update_dsh_superagent | 1:update_compactiondb | 1:prune_retired_manifest_steps | 1:check_pi_claude_bridge | 1:check_pstack | 1:retire_shared_pstack_copies | 1:retire_marketplace_dev_workflows | 1:retire_understand_anything | 1:retire_agmsg_shim)
            export PATH="${HOME}/.local/share/mise/shims:${PATH}"
            "$1"
            fail_on_pin_failures
            return
            ;;
        esac
        printf 'Usage: scripts/update-agent-assets.sh [update_omp | update_hcom | update_pi_claude_bridge | update_security_audit_skill | update_deepseek_harness | update_dsh_superagent | update_compactiondb | prune_retired_manifest_steps | check_pi_claude_bridge | check_pstack | retire_shared_pstack_copies | retire_marketplace_dev_workflows | retire_understand_anything | retire_agmsg_shim]\n' >&2
        exit 2
    fi

    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
    remove_node_global_agent_cli_shadows
    retire_shared_pstack_copies
    retire_marketplace_dev_workflows
    retire_agmsg_shim
    ensure_mise_npm_agent_cli claude "npm:@anthropic-ai/claude-code"
    # Claude Code plugin convergence comes before any step that may stop the run (set -e), so every pinned
    # plugin is checked; its own failures are counted and fail the run at the end (fail_on_pin_failures).
    update_claude_superpowers
    update_claude_crit
    update_claude_ponytail
    converge_claude_plugins
    retire_understand_anything
    ensure_mise_npm_agent_cli codex "npm:@openai/codex"
    ensure_gh_extensions
    update_codex_superpowers
    update_codex_crit
    update_codex_ponytail
    update_terminal_code
    update_terminal_browser
    update_omp
    update_pi_claude_bridge
    update_security_audit_skill
    update_deepseek_harness
    update_dsh_superagent
    update_hcom
    update_compactiondb
    ensure_herdr_integrations
    prune_retired_manifest_steps
    # After every plugin update above, so the trust hashes follow the plugin content of this run.
    refresh_codex_hook_trust
    # Last, so every other step still ran: a plugin that may stay enabled off its pin fails the whole run.
    fail_on_pin_failures
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
