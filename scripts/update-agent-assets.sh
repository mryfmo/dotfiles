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
# Rendered from assets.pi-claude-bridge in home/dot_agents/agent-config.yaml; change the version and sha256 there
# together after reviewing the upstream diff, then regenerate bun.lock and re-check the patches.
PI_CLAUDE_BRIDGE_PIN_VERSION="0.9.3"
PI_CLAUDE_BRIDGE_TARBALL_SHA256="8d582b2fee1615b64a59890e3ac0af03c1e11bd06ba1997accdb767969556d67"
PI_CLAUDE_BRIDGE_ASSET_DIR="${DOTFILES_REPO_SOURCE_DIR}/home/dot_agents/assets/pi-claude-bridge"
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
# @description Ensure the Understand-Anything Claude Code plugin marketplace is configured.
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
# @description Keep the Claude Code Understand-Anything plugin at its recorded pin.
#
function update_claude_understand_anything() {
    if ! has_command claude; then
        printf 'Skipping Claude Code Understand-Anything plugin: claude command not found.\n'
        return 0
    fi

    section "Claude Code Understand-Anything plugin"
    # Refreshed only once its identity is verified; converge_claude_step verifies again and reports and judges
    # any failure, so this call\'s own messages are not repeated.
    if ensure_claude_plugin_marketplace "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" 2> /dev/null; then
        claude_outside_projects plugin marketplace update "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" || true
    fi
    converge_claude_step "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || return 0
    record_claude_plugin_step "update_claude_understand_anything" "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "${AGENT_CLAUDE_DIR}/plugins/cache/understand-anything/understand-anything" "${AGENT_CLAUDE_DIR}/settings.json" -- "claude plugin marketplace add ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin update ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}"
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
#   inert ones, inert being what the copy's manifest does not point at and Codex never loads by convention; the
#   pin_records.py INERT globs apply outside the trees the manifest names only), is off its pin, whether the step
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
    claude_cache="${AGENT_CLAUDE_DIR}/plugins/cache/understand-anything/understand-anything"
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
        curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" \
            -o "${installer}" || {
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
    manifest_record "update_codex_understand_anything" installer "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}" "${HOME}/.understand-anything/repo" "${HOME}/.agents/skills/understand" "${HOME}/.agents/skills/understand-chat" "${HOME}/.agents/skills/understand-dashboard" "${HOME}/.agents/skills/understand-diff" "${HOME}/.agents/skills/understand-domain" "${HOME}/.agents/skills/understand-explain" "${HOME}/.agents/skills/understand-figma" "${HOME}/.agents/skills/understand-knowledge" "${HOME}/.agents/skills/understand-onboard" -- "curl -fsSL ${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer> codex" ||
        record_claude_failure "recording update_codex_understand_anything in the installed asset manifest"
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
        mkdir -p "${aside%/*}" && rm -rf "${aside}" && mv "${entry}" "${aside}" || return
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
        mkdir -p "${install_dir%/*}" && staging="$(mktemp -d "${install_dir}.staging.XXXXXX")" || return
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
# @description Sync the vendored CompactionDB tree without deleting project runtime state.
#
function update_compactiondb() {
    local source_root version
    source_root="${DOTFILES_REPO_SOURCE_DIR}/vendor/compactiondb/"
    rsync -a --delete --exclude '.claude/contextdb/state/' --exclude '.claude/contextdb/spool/' --exclude '.claude/contextdb/health/' --exclude '.claude/contextdb/contextdb.sqlite3*' "${source_root}" "${HOME}/.agents/compactiondb/" || true
    version="$(awk '/^## / { print $2; exit }' "${source_root}CHANGELOG.md")" || {
        printf 'Cannot read the CompactionDB version from %sCHANGELOG.md.\n' "${source_root}" >&2
        return 1
    }
    manifest_record "update_compactiondb" rsync "${version}" "${HOME}/.agents/compactiondb" -- "rsync -a --delete --exclude .claude/contextdb/state/ --exclude .claude/contextdb/spool/ --exclude .claude/contextdb/health/ --exclude .claude/contextdb/contextdb.sqlite3* ${source_root} ${HOME}/.agents/compactiondb/" ||
        record_claude_failure "recording update_compactiondb in the installed asset manifest"
}

#
# @description Install and refresh managed agent plugin assets.
# @arg $1 string Optional single step to run alone: update_pi_claude_bridge, check_pi_claude_bridge, check_pstack, retire_shared_pstack_copies, retire_marketplace_dev_workflows or retire_agmsg_shim.
#
function main() {
    if [ "$#" -gt 0 ]; then
        case "$#:$1" in
        1:update_pi_claude_bridge | 1:check_pi_claude_bridge | 1:check_pstack | 1:retire_shared_pstack_copies | 1:retire_marketplace_dev_workflows | 1:retire_agmsg_shim)
            export PATH="${HOME}/.local/share/mise/shims:${PATH}"
            "$1"
            return
            ;;
        esac
        printf 'Usage: scripts/update-agent-assets.sh [update_pi_claude_bridge | check_pi_claude_bridge | check_pstack | retire_shared_pstack_copies | retire_marketplace_dev_workflows | retire_agmsg_shim]\n' >&2
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
    update_claude_understand_anything
    converge_claude_plugins
    ensure_mise_npm_agent_cli codex "npm:@openai/codex"
    ensure_gh_extensions
    update_codex_superpowers
    update_codex_crit
    update_codex_ponytail
    update_codex_understand_anything
    update_terminal_code
    update_terminal_browser
    update_omp
    update_pi_claude_bridge
    update_hcom
    update_compactiondb
    ensure_herdr_integrations
    manifest_prune_retired
    # After every plugin update above, so the trust hashes follow the plugin content of this run.
    refresh_codex_hook_trust
    # Last, so every other step still ran: a plugin that may stay enabled off its pin fails the whole run.
    fail_on_pin_failures
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
