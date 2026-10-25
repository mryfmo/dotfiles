#!/usr/bin/env bash

# @file scripts/check-tools.sh
# @brief Print a read-only health summary for managed dotfiles tools.
# @description
#   Reports the availability and versions of the commands that participate in
#   the dotfiles lifecycle. This script does not install, upgrade, or modify
#   tools; use `scripts/upgrade-tools.sh` for explicit upgrades.

set -Eeuo pipefail

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
# @description Require a command and a successful version command.
# @arg $1 string Command name.
# @arg $@ string Optional version command arguments.
#
function check_command() {
    local command_name="$1" command_path
    shift || true

    if ! command_path="$(command -v "${command_name}" 2> /dev/null)"; then
        printf 'required missing: %s\n' "${command_name}" >&2
        ((required_failures += 1))
        return 0
    fi

    printf 'found:   %s -> %s\n' "${command_name}" "${command_path}"

    local output first_line

    if [ "$#" -gt 0 ]; then
        if ! output="$("${command_name}" "$@" 2>&1)"; then
            printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
            ((required_failures += 1))
            return 0
        fi
    else
        if ! output="$("${command_name}" --version 2>&1)"; then
            printf 'required failed: %s --version\n' "${command_name}" >&2
            ((required_failures += 1))
            return 0
        fi
    fi

    IFS= read -r first_line <<< "${output}"
    printf '%s\n' "${first_line}"
}

#
# @description Run a required read-only doctor command when its tool is available.
# @arg $1 string Command name.
# @arg $@ string Doctor command arguments.
#
function run_required_doctor() {
    local command_name="$1"
    shift || true

    if command -v "${command_name}" > /dev/null 2>&1 && ! "${command_name}" "$@"; then
        printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
        ((required_failures += 1))
    fi
}

#
# @description Record an optional warning.
# @arg $1 string Warning text.
#
function warn_optional() {
    printf 'optional warning: %s\n' "$1" >&2
    ((optional_warnings += 1))
}

#
# @description Return success when the rendered chezmoi config enables the private layer.
#   Defaults to enabled when chezmoi/jq are unavailable or the config predates the
#   usePrivate key, matching the owner's existing machines' behavior.
#
function private_layer_enabled() {
    local use_private

    if ! command -v chezmoi > /dev/null 2>&1 || ! command -v jq > /dev/null 2>&1; then
        return 0
    fi

    use_private="$(chezmoi data 2> /dev/null | jq -r '.usePrivate' 2> /dev/null)"
    [ "${use_private}" != "false" ]
}

#
# @description Print the configured private chezmoi source state.
#
function check_private_chezmoi() {
    local private_source="${HOME%/}/.local/share/chezmoi-private"
    local private_config="${HOME%/}/.config/chezmoi-private/chezmoi.yaml"

    if ! private_layer_enabled; then
        printf 'not applicable: private layer (usePrivate=false)\n'
        return 0
    fi

    if [ -d "${private_source}" ]; then
        printf 'found:   private source -> %s\n' "${private_source}"
        if [ -f "${private_config}" ]; then
            printf 'found:   private config -> %s\n' "${private_config}"
        else
            warn_optional "private config is missing: ${private_config}"
        fi
    else
        warn_optional "private source is missing: ${private_source}"
        if [ ! -f "${private_config}" ]; then
            warn_optional "private config is missing: ${private_config}"
        fi
    fi
}

#
# @description Require Homebrew on macOS and skip it on other platforms.
#
function check_homebrew() {
    local kernel
    if ! kernel="$(uname)"; then
        printf 'required failed: uname; cannot tell whether Homebrew applies\n' >&2
        ((required_failures += 1))
        return 0
    fi
    if [ "${kernel}" != "Darwin" ]; then
        printf 'not applicable: Homebrew (non-Darwin)\n'
        return 0
    fi

    check_command brew --version
}

#
# @description Check the key git signs commits with. The managed git config renders
#   commit.gpgsign only when ~/.ssh/id_ed25519.pub exists at apply time, so signing that is off
#   is an optional notice. With commit.gpgsign=true (now only through a hand edit) a missing
#   user.signingkey file makes every commit fail, so it is a required failure; a git config
#   read that fails (other than "unset") is one too.
#
function check_git_signing_key() {
    local gpgsign key status=0

    gpgsign="$(git config --get --type=bool commit.gpgsign 2> /dev/null)" || status=$?
    if [ "${status}" -eq 1 ]; then
        warn_optional "commit signing is off (no signing key when the git config was applied); run provision-machine-key, register the key, then chezmoi apply"
        return 0
    fi
    if [ "${status}" -eq 0 ] && [ "${gpgsign}" != "true" ]; then
        printf 'not applicable: commit signing key (commit.gpgsign is false)\n'
        return 0
    fi
    if [ "${status}" -ne 0 ]; then
        printf 'required failed: git config --get commit.gpgsign (exit %d)\n' "${status}" >&2
        ((required_failures += 1))
        return 0
    fi

    status=0
    key="$(git config --get user.signingkey 2> /dev/null)" || status=$?
    if [ "${status}" -ne 0 ]; then
        printf 'required failed: commit.gpgsign is true but user.signingkey cannot be read (exit %d); run provision-machine-key\n' "${status}" >&2
        ((required_failures += 1))
        return 0
    fi
    # A literal key ("key::ssh-ed25519 ...") needs no file.
    if [[ "${key}" == key::* ]]; then
        printf 'found:   commit signing key (literal user.signingkey)\n'
        return 0
    fi
    # git expands a leading ~/ in user.signingkey; do the same.
    key="${key/#\~\//${HOME%/}/}"
    if [ -f "${key}" ]; then
        printf 'found:   commit signing key -> %s\n' "${key}"
    else
        printf 'required missing: commit signing key %s (commit.gpgsign=true, so commits fail); run provision-machine-key and register the key with GitHub\n' "${key}" >&2
        ((required_failures += 1))
    fi
}

#
# @description Report the managed Crit CLI's pinned version and origin, when installed.
#   Installed by ensure_crit_cli in scripts/update-agent-assets.sh from the pinned
#   GitHub release on every OS; not required, so a missing binary is not a failure.
#
function check_crit_cli() {
    local target="${HOME%/}/.local/bin/crit"

    if [ ! -x "${target}" ]; then
        printf 'not applicable: Crit CLI (not installed)\n'
        return 0
    fi

    printf 'found:   crit -> %s (pinned release)\n' "${target}"
    "${target}" --version || warn_optional "crit --version failed; the managed binary may be corrupt (try REPAIR=1 make doctor)"
}

#
# @description Report omp's installed version beside its manifest pin.
#
function check_omp() {
    local target="${HOME%/}/.local/bin/omp"
    if [ ! -x "${target}" ]; then
        warn_optional "omp not installed; run make update"
        return 0
    fi
    local pin
    pin="$(awk -F'"' '/^OMP_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
    printf 'found:   omp -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
    "${target}" --version || warn_optional "omp --version failed; run make update"
}

#
# @description Report hcom's installed version beside its manifest pin.
#
function check_hcom() {
    local target="${HOME%/}/.local/bin/hcom"
    if [ ! -x "${target}" ]; then
        warn_optional "hcom not installed; run make update"
        return 0
    fi
    local pin
    pin="$(awk -F'"' '/^HCOM_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
    printf 'found:   hcom -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
    "${target}" --version || warn_optional "hcom --version failed; run make update"
}

#
# @description Report Zed on Ubuntu clients. run_after_05-client-install-zed installs it only with an
#   authenticated gh, because a GitHub release attestation is the only verification Zed publishes.
#
function check_zed() {
    local target="${HOME%/}/.local/bin/zed" system kernel
    system="$(chezmoi execute-template '{{ .system }}' 2> /dev/null || true)"
    if ! kernel="$(uname -s)"; then
        printf 'required failed: uname -s; cannot tell whether Zed applies\n' >&2
        ((required_failures += 1))
        return 0
    fi
    if [ "${kernel}" != Linux ] || [ "${system}" != client ]; then
        printf 'not applicable: Zed (installed on Ubuntu clients only)\n'
        return 0
    fi
    if [ ! -x "${target}" ]; then
        warn_optional "zed not installed: run make gh-auth, then make update; its release attestation cannot be verified without an authenticated gh"
        return 0
    fi
    printf 'found:   zed -> %s\n' "${target}"
    "${target}" --version || warn_optional "zed --version failed; the install may be corrupt"
}

#
# @description Verify bwrap can create user namespaces when AppArmor restricts them.
#   Sandboxed Codex runs exec /usr/bin/bwrap, which needs the bwrap-userns profile
#   installed by install/ubuntu/common/apparmor_userns.sh. Loaded profiles are
#   root-only to list, so an unprivileged bwrap probe is the effective check.
#
function check_apparmor_userns() {
    local restrict="${APPARMOR_USERNS_SYSCTL:-/proc/sys/kernel/apparmor_restrict_unprivileged_userns}"
    local bwrap="${APPARMOR_USERNS_BWRAP:-/usr/bin/bwrap}"
    local profile="${APPARMOR_USERNS_PROFILE_TARGET:-/etc/apparmor.d/bwrap-userns}"
    local restricted=""

    # A host without the sysctl has no restriction; one that exists but cannot be read decides nothing.
    if [ -e "${restrict}" ] && ! restricted="$(cat "${restrict}")"; then
        printf 'required failed: cannot read %s; the AppArmor userns restriction is unknown\n' "${restrict}" >&2
        ((required_failures += 1))
        return 0
    fi
    if [ "${restricted}" != "1" ]; then
        printf 'not applicable: AppArmor userns restriction (not enabled)\n'
        return 0
    fi
    if ! command -v codex > /dev/null 2>&1; then
        warn_optional "codex is not installed; skipped the bwrap user-namespace probe"
        return 0
    fi
    if [ ! -x "${bwrap}" ]; then
        printf 'required failed: %s is missing; sandboxed codex runs need it under the AppArmor userns restriction (install the bubblewrap package)\n' "${bwrap}" >&2
        ((required_failures += 1))
        return 0
    fi
    if "${bwrap}" --ro-bind / / true > /dev/null 2>&1; then
        printf 'found:   bwrap user namespaces allowed -> %s\n' "${bwrap}"
        return 0
    fi
    if [ -f "${profile}" ]; then
        printf 'required failed: bwrap user-namespace probe; %s exists but is not effective (sudo apparmor_parser -r %s)\n' "${profile}" "${profile}" >&2
    else
        printf 'required failed: bwrap user-namespace probe; AppArmor profile %s is missing, so sandboxed codex runs fail (sudo -v && bash install/ubuntu/common/apparmor_userns.sh)\n' "${profile}" >&2
    fi
    ((required_failures += 1))
}

#
# @description Print the current GitHub CLI extension state when gh is installed.
#
function check_gh_extensions() {
    if command -v gh > /dev/null 2>&1 && ! gh extension list; then
        warn_optional "unable to list installed GitHub CLI extensions"
    fi
}

#
# @description Report the Linux prerequisites of the Claude Code Bash sandbox:
#   bwrap and socat on PATH. check_apparmor_userns covers the user-namespace
#   side, so this check has no sysctl or profile logic.
#
function check_claude_sandbox() {
    local command_name command_path kernel

    if ! kernel="$(uname)"; then
        printf 'required failed: uname; cannot tell whether the Claude Code sandbox prerequisites apply\n' >&2
        ((required_failures += 1))
        return 0
    fi
    if [ "${kernel}" != "Linux" ]; then
        printf 'not applicable: Claude Code sandbox prerequisites (non-Linux; macOS uses Seatbelt)\n'
        return 0
    fi

    for command_name in bwrap socat; do
        if command_path="$(command -v "${command_name}" 2> /dev/null)"; then
            printf 'found:   %s -> %s\n' "${command_name}" "${command_path}"
        else
            warn_optional "Claude Code sandbox prerequisite is missing: ${command_name} (run make update)"
        fi
    done
}

#
# @description Report each omp seat profile's login on this host through
#   `scripts/orchestrator/seat-login-preflight --check` (regime-cutover U37):
#   presence and mtimes only, never a token. An absent login is an optional
#   warning, since a login is per host and the operator's step; an unreadable
#   login record is a required failure, never read as absent.
#
function check_seat_logins() {
    local lever="${BASH_SOURCE[0]%/*}/orchestrator/seat-login-preflight"
    local output line status=0

    if [ ! -x "${lever}" ]; then
        warn_optional "seat login check skipped: ${lever} is missing"
        return 0
    fi
    output="$("${lever}" --check 2>&1)" || status=$?
    while IFS= read -r line; do
        case "${line}" in
        '') ;;
        'not applicable:'*) printf '%s\n' "${line}" ;;
        # The lever's own refusal or failed producer (pin, uname), never a profile line.
        'seat-login-preflight:'*) printf 'required failed: %s\n' "${line}" >&2 ;;
        *': unreadable'*) printf 'required failed: seat login %s\n' "${line}" >&2 ;;
        *': absent'* | *': no route'* | *': not a seat login route'*)
            warn_optional "seat login ${line} (log in on this host: seat-login-preflight <profile>, docs/remote-host-logins.md)"
            ;;
        *) printf 'found:   seat login %s\n' "${line}" ;;
        esac
    done <<< "${output}"
    if [ "${status}" -ne 0 ]; then
        printf 'required failed: seat-login-preflight --check exited %d\n' "${status}" >&2
        ((required_failures += 1))
    fi
}

#
# @description Run the read-only dotfiles health checks.
#
function main() {
    section "Core commands"
    check_command git --version
    check_command chezmoi --version
    check_command mise --version
    check_command uv --version
    check_command gh --version

    section "Chezmoi"
    run_required_doctor chezmoi doctor
    check_private_chezmoi

    section "Mise"
    run_required_doctor mise doctor
    run_required_doctor mise ls --current

    section "Homebrew"
    check_homebrew

    section "Crit CLI"
    check_crit_cli

    section "Agent tools"
    check_omp
    check_hcom

    section "Seat logins"
    check_seat_logins

    section "Zed"
    check_zed

    section "SSH"
    check_git_signing_key

    section "AppArmor"
    check_apparmor_userns

    section "Claude Code sandbox"
    check_claude_sandbox

    section "GitHub CLI extensions"
    check_gh_extensions

    printf '\nTool check summary: required failures: %d; optional warnings: %d\n' \
        "${required_failures}" "${optional_warnings}"
    [ "${required_failures}" -eq 0 ]
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
