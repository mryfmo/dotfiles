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
    install_path="$(mise where "${mise_tool}" 2> /dev/null || command -v "${cli}")" || {
        printf 'Cannot locate the repaired %s for the asset manifest.\n' "${cli}" >&2
        return 1
    }
    manifest_record "ensure_mise_npm_agent_cli:${cli}" installer "${cli_version}" "${install_path}" -- "MISE_NPM_PACKAGE_MANAGER=npm mise install --force ${mise_tool}"
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
    curl -fsSL "${base_url}/${artifact}" -o "${download}" || return
    curl -fsSL "${base_url}/checksums.txt" -o "${checksums}" || return
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
    manifest_record "ensure_crit_cli" installer "${tag}" "${target}" -- "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/${artifact}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/checksums.txt" "shasum -a 256 <binary>" "install -m 0755 <binary> ${target}"
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
    pin_record claude-enabled "${CLAUDE_CONFIG_DIR:-${HOME}/.claude}/settings.json" "$1"
}

#
# @description Print every installation of a Claude Code plugin from installed_plugins.json, one
#   `<scope>\t<version>\t<project path>` line each, or nothing when it is not installed.
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 1 When installed_plugins.json exists but cannot be parsed: a failed read is never "not installed".
#
function claude_plugin_installs() {
    pin_record claude-installs "${CLAUDE_CONFIG_DIR:-${HOME}/.claude}/plugins/installed_plugins.json" "$1"
}

#
# @description Print the user-scope installed version of a Claude Code plugin, or nothing when there is none.
# @arg $1 string Lines from claude_plugin_installs.
#
# @description Print the user-scope installed version of a Claude Code plugin, or nothing when there is none.
# @arg $1 string The JSON list claude_plugin_installs prints.
# @exitcode 1 When the list is not JSON (it always is from pin_records.py; a failure is never "no version").
#
function claude_user_install() {
    jq -er 'first(.[] | select(.scope == "user") | .version) // ""' <<< "$1"
}

#
# @description Print the user-scope installed version of a Claude Code plugin for the asset manifest, or
#   `unknown` when installed_plugins.json does not record one.
# @arg $1 string Fully qualified Claude Code plugin ID.
#
function claude_user_plugin_version() {
    local installs version

    installs="$(claude_plugin_installs "$1")" || installs="[]"
    version="$(claude_user_install "${installs}")" || version=""
    printf '%s\n' "${version:-unknown}"
}

#
# @description Register the marketplace a pinned Claude Code plugin comes from (its `marketplace` in
#   assets.claude-plugins), unless a marketplace of that name is already registered.
# @arg $1 string Fully qualified Claude Code plugin ID (`<plugin>@<marketplace name>`).
# @exitcode 1 When the marketplace list cannot be read, the pin records no source, or `marketplace add` fails.
#
function ensure_claude_plugin_marketplace() {
    local plugin_id="$1"
    local name="${1#*@}" source listing state

    if ! source="$(plugin_pin claude "${plugin_id}" marketplace)"; then
        printf 'ERROR: %s records no marketplace for %s.\n' "${AGENT_PLUGIN_PINS}" "${plugin_id}" >&2
        return 1
    fi
    if ! listing="$(claude_outside_projects plugin marketplace list --json 2> /dev/null)"; then
        printf 'ERROR: claude plugin marketplace list --json failed; cannot register %s for %s.\n' "${source}" "${plugin_id}" >&2
        return 1
    fi
    # A marketplace of that name registered from another source is foreign: an error, never "registered".
    if ! state="$(pin_record claude-marketplace "${name}" "${source}" <<< "${listing}")"; then
        return 1
    fi
    if [ "${state}" = "registered" ]; then
        return 0
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
# @description Keep the user-scope installation of a Claude Code plugin at its recorded pin (assets.claude-plugins).
# @description
#   This repository installs plugins at user scope only, so only that installation is managed; a project- or
#   local-scope installation belongs to its project and is reported as not managed, never converged.
#   Claude Code installs only a marketplace's current release and takes no version: a missing plugin is
#   installed at user scope from its recorded marketplace (registered first when absent); a user-scope
#   installation at another version is updated. One still off its pin afterwards is disabled at user scope
#   (idempotent): Claude Code runs a plugin's hooks with no trust step, so only the reviewed version may stay
#   enabled. Whether the step reached the pin is decided by make doctor's own check (doctor_pin_check), never
#   here, so an off-pin plugin fails the run even once disabled. Every `claude` call runs from an empty
#   directory, so no project settings take part. The enabled state of a user-scope installation at its pin is
#   never changed (an operator's disable stays); a fresh install is left as `claude plugin install` leaves it.
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 0 When the doctor's pin check passes for the plugin.
# @exitcode 1 Otherwise: the pin or a record cannot be read, the marketplace cannot be registered, the install
#   fails, or the doctor's check reports drift. Every caller counts it as a run failure.
#
function converge_claude_plugin() {
    local plugin_id="$1"
    local pin installs version enabled failed=0

    if ! pin="$(plugin_pin claude "${plugin_id}" pin)"; then
        printf 'Cannot read the pin of %s from %s; the plugin was not changed.\n' "${plugin_id}" "${AGENT_PLUGIN_PINS}" >&2
        return 1
    fi
    if ! installs="$(claude_plugin_installs "${plugin_id}")"; then
        printf 'ERROR: cannot read the installation records of %s (installed_plugins.json); it was not changed.\n' "${plugin_id}" >&2
        return 1
    fi
    jq -r --arg id "${plugin_id}" '.[] | select(.scope != "user")
        | "WARN: plugin \($id) installed in \(.scope) scope at \(.projectPath // .installPath): not managed (make update manages user scope only)."' \
        <<< "${installs}" >&2 || return 1
    version="$(claude_user_install "${installs}")" || return 1
    if [ "${version}" != "${pin}" ] && ! ensure_claude_plugin_marketplace "${plugin_id}"; then
        failed=1
    fi
    if [ -z "${version}" ]; then
        [ "${failed}" -eq 0 ] || return 1
        if ! claude_outside_projects plugin install "${plugin_id}" --scope user < /dev/null; then
            printf 'ERROR: claude plugin install %s failed; the pinned plugin is not installed.\n' "${plugin_id}" >&2
            return 1
        fi
    elif [ "${version}" != "${pin}" ]; then
        claude_outside_projects plugin update "${plugin_id}" --scope user < /dev/null || true
    fi
    if ! installs="$(claude_plugin_installs "${plugin_id}")"; then
        printf 'ERROR: cannot re-read the installation records of %s after changing it.\n' "${plugin_id}" >&2
        return 1
    fi
    version="$(claude_user_install "${installs}")" || return 1
    if [ -z "${version}" ]; then
        printf 'ERROR: %s has no user-scope installation after claude plugin install.\n' "${plugin_id}" >&2
        return 1
    fi
    if [ "${version}" != "${pin}" ]; then
        printf 'WARN: Claude Code plugin %s is at %s, not its pin %s; disabling it until that release is reviewed and its version recorded in assets.claude-plugins (home/dot_agents/agent-config.yaml).\n' "${plugin_id}" "${version}" "${pin}" >&2
        # Idempotent: a plugin already disabled may make the command fail; the settings file shows the result.
        claude_outside_projects plugin disable "${plugin_id}" --scope user < /dev/null || true
        if ! enabled="$(claude_user_enabled "${plugin_id}")" || [ "${enabled}" != "disabled" ]; then
            printf 'ERROR: Claude Code plugin %s is off its pin and ~/.claude/settings.json does not disable it (%s).\n' "${plugin_id}" "${enabled:-unreadable}" >&2
        fi
    fi
    # Success is the doctor's verdict on this plugin, never this function's own reading.
    if ! doctor_pin_check claude "${plugin_id}"; then
        printf 'ERROR: make doctor still reports %s off its pin after this step.\n' "${plugin_id}" >&2
        return 1
    fi
    printf 'Claude Code plugin %s is at its pin %s (enabled state left as is).\n' "${plugin_id}" "${pin}"
    return "${failed}"
}

# Plugin IDs converged in this run, space-delimited (bash 3.2 has no associative arrays), and the
# count of plugins whose convergence failed for any reason; main fails the run when it is not zero.
CLAUDE_CONVERGED=" "
CLAUDE_PIN_FAILURES=0

#
# @description Count a failed Claude Code plugin setup step and keep going, so the run still reaches the
#   convergence of every pinned plugin and fail_on_claude_pin_failures still fails it at the end.
# @arg $1 string What failed.
#
function record_claude_failure() {
    printf 'ERROR: %s failed; continuing so every pinned plugin is still checked, and the run will fail.\n' "$1" >&2
    CLAUDE_PIN_FAILURES=$((CLAUDE_PIN_FAILURES + 1))
}

#
# @description Converge one Claude Code plugin once per run; any failure of converge_claude_plugin is counted.
# @arg $1 string Fully qualified Claude Code plugin ID.
# @exitcode 0 When the plugin is at its pin or proven disabled; nonzero otherwise, counted in CLAUDE_PIN_FAILURES.
#
function converge_claude_step() {
    local plugin_id="$1"
    local status=0

    CLAUDE_CONVERGED="${CLAUDE_CONVERGED}${plugin_id} "
    converge_claude_plugin "${plugin_id}" || status=$?
    if [ "${status}" -ne 0 ]; then
        CLAUDE_PIN_FAILURES=$((CLAUDE_PIN_FAILURES + 1))
    fi
    return "${status}"
}

#
# @description Fail the run when any Claude Code plugin could not be checked or kept at its pin (counted by converge_claude_step).
# @exitcode 1 When CLAUDE_PIN_FAILURES is not zero.
#
function fail_on_claude_pin_failures() {
    if [ "${CLAUDE_PIN_FAILURES}" -gt 0 ]; then
        printf 'ERROR: %s Claude Code plugin(s) could not be checked or kept at their pin; see the errors above.\n' "${CLAUDE_PIN_FAILURES}" >&2
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
        CLAUDE_PIN_FAILURES=$((CLAUDE_PIN_FAILURES + 1))
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
    manifest_record "ensure_herdr_integrations" integration "${herdr_version}" "${HOME}/.claude/hooks/herdr-agent-state.sh" "${HOME}/.codex/herdr-agent-state.sh" -- "herdr integration install claude" "herdr integration install codex"
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
# @description Keep the Claude Code Superpowers plugin at its recorded pin.
#
function update_claude_superpowers() {
    if ! has_command claude; then
        printf 'Skipping Claude Code plugins: claude command not found.\n'
        return 0
    fi

    section "Claude Code plugins"
    ensure_claude_plugin_marketplace "${CLAUDE_SUPERPOWERS_PLUGIN}" || record_claude_failure "the superpowers marketplace registration"
    claude_outside_projects plugin marketplace update claude-plugins-official || true
    converge_claude_step "${CLAUDE_SUPERPOWERS_PLUGIN}" || return 0
    local plugin_version
    plugin_version="$(claude_user_plugin_version "${CLAUDE_SUPERPOWERS_PLUGIN}")"
    manifest_record "update_claude_superpowers" plugin "${plugin_version}" "${HOME}/.claude/plugins/cache/claude-plugins-official/superpowers" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_SUPERPOWERS_MARKETPLACE}" "claude plugin marketplace update claude-plugins-official" "claude plugin install ${CLAUDE_SUPERPOWERS_PLUGIN}" "claude plugin update ${CLAUDE_SUPERPOWERS_PLUGIN}" ||
        record_claude_failure "recording update_claude_superpowers in the installed asset manifest"
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
    ensure_claude_plugin_marketplace "${CLAUDE_CRIT_PLUGIN}" || record_claude_failure "the crit marketplace registration"
    claude_outside_projects plugin marketplace update "${CLAUDE_CRIT_MARKETPLACE_NAME}" || true
    converge_claude_step "${CLAUDE_CRIT_PLUGIN}" || return 0
    local plugin_version
    plugin_version="$(claude_user_plugin_version "${CLAUDE_CRIT_PLUGIN}")"
    manifest_record "update_claude_crit" plugin "${plugin_version}" "${HOME}/.claude/plugins/cache/crit/crit" "${HOME}/.claude/settings.json" -- "ensure_crit_cli" "claude plugin marketplace add ${CLAUDE_CRIT_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_CRIT_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_CRIT_PLUGIN}" "claude plugin update ${CLAUDE_CRIT_PLUGIN}" ||
        record_claude_failure "recording update_claude_crit in the installed asset manifest"
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
    ensure_claude_plugin_marketplace "${CLAUDE_PONYTAIL_PLUGIN}" || record_claude_failure "the ponytail marketplace registration"
    claude_outside_projects plugin marketplace update "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" || true
    converge_claude_step "${CLAUDE_PONYTAIL_PLUGIN}" || return 0
    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
    local plugin_version
    plugin_version="$(claude_user_plugin_version "${CLAUDE_PONYTAIL_PLUGIN}")"
    manifest_record "update_claude_ponytail" plugin "${plugin_version}" "${HOME}/.claude/plugins/cache/ponytail/ponytail" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_PONYTAIL_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin update ${CLAUDE_PONYTAIL_PLUGIN}" ||
        record_claude_failure "recording update_claude_ponytail in the installed asset manifest"
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
    ensure_claude_plugin_marketplace "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || record_claude_failure "the understand-anything marketplace registration"
    claude_outside_projects plugin marketplace update "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" || true
    converge_claude_step "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || return 0
    local plugin_version
    plugin_version="$(claude_user_plugin_version "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}")"
    manifest_record "update_claude_understand_anything" plugin "${plugin_version}" "${HOME}/.claude/plugins/cache/understand-anything/understand-anything" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin update ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" ||
        record_claude_failure "recording update_claude_understand_anything in the installed asset manifest"
}

#
# @description Print the versions in the plugin.json of every installed copy of a Codex plugin, one per line.
# @arg $1 string Fully qualified Codex plugin ID.
#
# @description Print the version of the Codex plugin copy Codex loads (pin_records.py codex-copy: Codex's own
#   choice among the cached versions, its plugin.json read strictly), nothing when no copy is cached.
# @arg $1 string Fully qualified Codex plugin ID.
# @exitcode 2 When the cache cannot be read or its copy names another plugin or holds no string version.
#
function codex_plugin_cache_versions() {
    local plugin="${1%@*}" marketplace="${1#*@}"

    pin_record codex-copy "${CODEX_HOME:-${HOME}/.codex}/plugins/cache/${marketplace}/${plugin}" "${plugin}" \
        "${DOTFILES_REPO_SOURCE_DIR}/home/dot_codex/modify_private_config.toml"
}

#
# @description Warn when the installed copy of a Codex plugin is not its recorded pin.
# @description
#   Codex takes no plugin version, so this compares after the install. A plugin hook of a copy off its pin
#   is not trusted anyway: the modify scripts trust it only at its trusted_hash pin (codex.hooks.state).
# @arg $1 string Fully qualified Codex plugin ID.
#
# @description Install the Codex Superpowers plugin from the OpenAI-curated catalog, then compare it with its pin.
#
function update_codex_superpowers() {
    local codex_output installed

    if ! has_command codex; then
        printf 'Skipping Codex plugins: codex command not found.\n'
        return 0
    fi

    section "Codex plugins"
    installed="$(codex_plugin_cache_versions "${CODEX_SUPERPOWERS_PLUGIN}")" || installed="an unreadable copy"
    if [ -n "${installed}" ]; then
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
    doctor_pin_check codex "${CODEX_SUPERPOWERS_PLUGIN}" || record_claude_failure "the make doctor pin check of ${CODEX_SUPERPOWERS_PLUGIN}"
    local plugin_version
    plugin_version="$(manifest_codex_plugin_version "${CODEX_SUPERPOWERS_PLUGIN}")" || return 1
    manifest_record "update_codex_superpowers" plugin "${plugin_version}" "${CODEX_HOME:-${HOME}/.codex}/.tmp/plugins/plugins/superpowers" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin add ${CODEX_SUPERPOWERS_PLUGIN}"
}

#
# @description Ensure the Ponytail Codex plugin marketplace is configured at its reviewed commit.
# @description
#   chezmoi apply writes `ref` into [marketplaces.ponytail] (rendered from assets.codex-plugins), so an
#   existing marketplace follows the pin on `codex plugin marketplace upgrade`; a new one is added at it.
#
function ensure_codex_ponytail_marketplace() {
    local codex_home="${CODEX_HOME:-${HOME}/.codex}"
    local codex_config="${codex_home%/}/config.toml"
    local ref state

    if ! ref="$(plugin_pin codex "${CODEX_PONYTAIL_PLUGIN}" ref)"; then
        printf 'Cannot read the marketplace ref of %s from %s.\n' "${CODEX_PONYTAIL_PLUGIN}" "${AGENT_PLUGIN_PINS}" >&2
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

    if codex_marketplace_has_source "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"; then
        return 0
    fi
    if command_output_contains "${CODEX_PONYTAIL_MARKETPLACE_NAME}" codex plugin marketplace list; then
        printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
        return 1
    fi

    codex plugin marketplace add "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}" --ref "${ref}"
}

#
# @description Install the Codex Ponytail plugin from its marketplace at the reviewed commit, then compare it with its pin.
#
function update_codex_ponytail() {
    local ref pinned installed

    if ! has_command codex; then
        printf 'Skipping Codex Ponytail plugin: codex command not found.\n'
        return 0
    fi

    section "Codex Ponytail plugin"
    if ! ensure_codex_ponytail_marketplace; then
        record_claude_failure "the Codex Ponytail marketplace registration"
        return 0
    fi
    if ! ref="$(plugin_pin codex "${CODEX_PONYTAIL_PLUGIN}" ref)"; then
        record_claude_failure "reading the pinned ref of ${CODEX_PONYTAIL_PLUGIN}"
        return 0
    fi
    # An upgrade fetches whatever [marketplaces.ponytail] names; without the manifest's ref there it would move
    # to the branch head. chezmoi apply writes the ref (the Codex modify script), so a missing or other ref stops here.
    pinned=0
    pin_record codex-marketplace-pinned "${CODEX_HOME:-${HOME}/.codex}/config.toml" "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}" "${ref}" || pinned=$?
    if [ "${pinned}" -ne 0 ]; then
        printf 'ERROR: [marketplaces.%s] in the Codex config is not pinned to %s; run chezmoi apply, then make update. The marketplace was not upgraded.\n' "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${ref}" >&2
        record_claude_failure "the Codex Ponytail marketplace ref check"
        return 0
    fi
    codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}" || true

    installed="$(codex_plugin_cache_versions "${CODEX_PONYTAIL_PLUGIN}")" || installed="an unreadable copy"
    if [ -n "${installed}" ]; then
        printf 'Codex Ponytail plugin is already installed.\n'
    else
        codex plugin add "${CODEX_PONYTAIL_PLUGIN}" || true
    fi
    doctor_pin_check codex "${CODEX_PONYTAIL_PLUGIN}" || record_claude_failure "the make doctor pin check of ${CODEX_PONYTAIL_PLUGIN}"
    printf 'Ponytail lifecycle hooks are trusted only at their reviewed trusted_hash pins; the Codex config refresh at the end of this run applies them.\n'
    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
    local plugin_version
    plugin_version="$(manifest_codex_plugin_version "${CODEX_PONYTAIL_PLUGIN}")" || return 1
    manifest_record "update_codex_ponytail" plugin "${plugin_version}" "${CODEX_HOME:-${HOME}/.codex}/plugins/cache/ponytail/ponytail" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin marketplace add ${CODEX_PONYTAIL_MARKETPLACE_SOURCE} --ref ${ref}" "codex plugin marketplace upgrade ${CODEX_PONYTAIL_MARKETPLACE_NAME}" "codex plugin add ${CODEX_PONYTAIL_PLUGIN}"
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
    manifest_record "update_codex_crit" plugin "${plugin_version}" "${CODEX_HOME:-${HOME}/.codex}/plugins/crit" "${CODEX_HOME:-${HOME}/.codex}/config.toml" "${HOME}/.agents/skills/crit" "${HOME}/.agents/skills/crit-cli" "${HOME}/.agents/skills/crit-story" -- "ensure_crit_cli" "crit install codex-plugin --force"
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
    manifest_record "update_terminal_browser" installer "${TERMINAL_BROWSER_PIN_VERSION}" "${HOME}/.local/share/terminal-browser/app" "${HOME}/.local/bin/terminal-browser" "${HOME}/.local/state/terminal-browser/skills.links" -- "curl -fsSL ${TERMINAL_BROWSER_INSTALLER_URL}" "shasum -a 256 <installer>" "TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 bash <installer>"
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
    curl -fsSL "${OMP_TARBALL_URL}" -o "${tarball}" || return
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
    curl -fsSL "${url}" -o "${wheel}" || return
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
        curl -fsSL "${PI_CLAUDE_BRIDGE_TARBALL_URL}" -o "${tarball}" || return
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
# @description Confirm the pstack skills chezmoi places under ~/.agents/skills reach an omp seat.
# @description
#   No installer step runs for pstack: the two externals in home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl
#   deploy the pinned plugin's skills/* and docs/** (assets.pstack in the manifest) at every chezmoi apply. The check
#   fails when the poteto-mode skill or the Claude Code adapter its first paragraph links is missing, or when
#   `omp skill list`, run from an empty directory so no project skill tree takes part, does not name poteto-mode.
#   Without omp the file check alone decides.
# @exitcode 1 A file is missing or omp does not list the skill; omp's listing is printed above the verdict.
#
function check_pstack() {
    local file cwd listing count version
    for file in "${HOME}/.agents/skills/poteto-mode/SKILL.md" "${HOME}/.agents/docs/harness/claude-code.md"; do
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
    manifest_record "update_compactiondb" rsync "${version}" "${HOME}/.agents/compactiondb" -- "rsync -a --delete --exclude .claude/contextdb/state/ --exclude .claude/contextdb/spool/ --exclude .claude/contextdb/health/ --exclude .claude/contextdb/contextdb.sqlite3* ${source_root} ${HOME}/.agents/compactiondb/"
}

#
# @description Install and refresh managed agent plugin assets.
# @arg $1 string Optional single step to run alone: update_pi_claude_bridge, check_pi_claude_bridge or check_pstack.
#
function main() {
    if [ "$#" -gt 0 ]; then
        case "$#:$1" in
        1:update_pi_claude_bridge | 1:check_pi_claude_bridge | 1:check_pstack)
            export PATH="${HOME}/.local/share/mise/shims:${PATH}"
            "$1"
            return
            ;;
        esac
        printf 'Usage: scripts/update-agent-assets.sh [update_pi_claude_bridge | check_pi_claude_bridge | check_pstack]\n' >&2
        exit 2
    fi

    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
    remove_node_global_agent_cli_shadows
    ensure_mise_npm_agent_cli claude "npm:@anthropic-ai/claude-code"
    # Claude Code plugin convergence comes before any step that may stop the run (set -e), so every pinned
    # plugin is checked; its own failures are counted and fail the run at the end (fail_on_claude_pin_failures).
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
    fail_on_claude_pin_failures
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
