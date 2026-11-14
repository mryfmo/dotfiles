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
# @description Report the installed srt (`@anthropic-ai/sandbox-runtime`, the omp seat boundary, regime-cutover U85)
#   beside its mise pin (U141). srt is resolved as hcom-seat resolves it (`mise which srt`, else PATH). The pin is the
#   exact version of the applied mise config (`~/.config/mise/config.toml`); when that file is absent or still tracks
#   `latest` (the host has not run `make update` since the pin landed), the checkout's `home/dot_mise/config.toml`
#   beside this script is read instead. A pin that cannot be read, a `--version` that fails or prints nothing, and a
#   version whose first token differs from the pin are required failures (a failed read is never a pass); an absent
#   srt is an optional warning.
#
function check_srt() {
    local target pin='' config output first_line version
    if ! target="$(mise which srt 2> /dev/null)" || [ -z "${target}" ]; then
        target="$(command -v srt 2> /dev/null || true)"
    fi
    if [ -z "${target}" ] || [ ! -x "${target}" ]; then
        warn_optional "srt not installed; run make update"
        return 0
    fi
    for config in "${HOME%/}/.config/mise/config.toml" "${BASH_SOURCE[0]%/*}/../home/dot_mise/config.toml"; do
        [ -r "${config}" ] || continue
        pin="$(awk -F'"' '/^"npm:@anthropic-ai\/sandbox-runtime" = "/ { print $4; exit }' "${config}")" || pin=''
        if [[ ${pin} =~ ^[0-9]+(\.[0-9]+)+$ ]]; then break; fi
        pin=''
    done
    if [ -z "${pin}" ]; then
        printf 'required failed: srt -> %s; no exact sandbox-runtime pin in ~/.config/mise/config.toml or the checkout\n' "${target}" >&2
        ((required_failures += 1))
        return 0
    fi
    printf 'found:   srt -> %s (pin %s)\n' "${target}" "${pin}"
    if ! output="$("${target}" --version 2> /dev/null)" || [ -z "${output}" ]; then
        printf 'required failed: srt --version printed no version (pin %s); run make update\n' "${pin}" >&2
        ((required_failures += 1))
        return 0
    fi
    IFS= read -r first_line <<< "${output}"
    printf '%s\n' "${first_line}"
    version="${first_line%% *}"
    if [ "${version}" != "${pin}" ]; then
        printf 'required failed: srt %s differs from the pin %s; run make update\n' "${version}" "${pin}" >&2
        ((required_failures += 1))
    fi
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
# @description The login group of a seat profile (regime-cutover U498, U498d):
#   the one table `login_group_of_role` of `scripts/orchestrator/hcom-seat` and
#   `scripts/orchestrator/seat-login-preflight`, copied here as the same text
#   (`tests/unit/test_runtime_health.py` holds the copy equal to the lever's),
#   so the doctor names a group's login step from the table and not from a
#   guess: the worker, orchestrator and audit roles are each their own group,
#   the dsh and router roles the `router` group (the dsh gateway child is the
#   Router's). Any other name is no role of the table (status 1, nothing
#   printed).
# @arg $1 string The role (a seat profile's name).
# @stdout The group.
# @exitcode 1 The role is not in the table.
#
function login_group_of_role() {
    case $1 in
    worker) printf 'worker\n' ;;
    orchestrator) printf 'orchestrator\n' ;;
    audit) printf 'audit\n' ;;
    dsh | router) printf 'router\n' ;;
    *) return 1 ;;
    esac
}

#
# @description Set `login_step` to the operator's step for an absent login
#   line of `seat-login-preflight --check` (regime-cutover U498d; verdict
#   U498-8f2cca8c P2 `:413`). The line is `<profile> <route>: <state>`
#   (the pre-flight's `profile_line`), so the profile is its first word and
#   the group the table's (login_group_of_role). The pre-flight's profile
#   mode accepts the seat profiles alone (`seat_profiles` there, the values
#   of `omp.roles`: orchestrator, worker, audit; copied here as the same
#   text), so for those the step is `seat-login-preflight <profile>`, which
#   prints the group's `CLAUDE_CONFIG_DIR=<dir> claude auth login` or runs
#   the SIWC login. The dsh profile's group `router` has no profile mode
#   (`seat-login-preflight dsh` and `seat-login-preflight router` exit 2 as
#   unknown profiles), so its step is `claude auth login` under the group's
#   directory, the one this line names and `hcom-seat router --dry-run`
#   prints as CLAUDE_CONFIG_DIR (every group of the table is a role of
#   hcom-seat). A profile outside the table (a `no route` overlay that is no
#   seat) keeps the general sentence. A claude-bridge line carries two states
#   (regime-cutover U512): the login's, then the seats' API key's, `key ok
#   (<file>)` when the key passed; the step names what the line lacks: the
#   login's step when the login is not present, the key's step (the handout's
#   placement commands, which the pre-flight's profile mode prints for any
#   seat profile, the key file being one for every seat) when the key state is
#   not `key ok`, both when both are missing, the login's first. A mixed state
#   (regime-cutover U512f, verdict U512e-a120aeff P2) names the missing half's
#   command and says what happens meanwhile: beside a present login the
#   pre-flight passes but hcom-seat starts no seat until the key is placed
#   (its key_file_check refuses every role without the key; regime-cutover
#   U512g, verdict U512f-b6a3e2c0 P2: until this head the sentence said the
#   seat starts on the login), and the key's placement commands are the step;
#   beside an accepted key the seat starts on the key and the login is
#   information, its command the group's (the pre-flight's profile mode prints
#   both as information on its pass, U512f).
# @arg $1 string The `--check` line.
# @set login_step The sentence the warning carries in parentheses.
#
function login_step_of() {
    local profile="${1%% *}" group mode login_missing=1 key_missing=0 key_ok=0 key_step
    local -a seat_profiles=(orchestrator worker audit)
    login_step="log in on this host, once per login group: seat-login-preflight <profile> prints the group's command, docs/remote-host-logins.md"
    case "$1" in
    *' claude-bridge: '*)
        case "$1" in *': login present ('*) login_missing=0 ;; esac
        # A second state on the line is the key's (U512); any state but `key ok` wants the key placed.
        case "$1" in *'; key ok ('*) key_ok=1 ;; *'; '*) key_missing=1 ;; esac
        ;;
    esac
    key_step="place the seats' API key on this host (one file for every seat): seat-login-preflight <seat profile> prints the placement commands (handouts/anthropic-api-key-u510.md, steps 2 and 3), docs/remote-host-logins.md"
    if [ "${login_missing}" -eq 0 ] && [ "${key_missing}" -eq 0 ]; then
        return 0
    fi
    group="$(login_group_of_role "${profile}")" || {
        if [ "${key_missing}" -eq 1 ]; then login_step="${key_step}"; fi
        return 0
    }
    for mode in "${seat_profiles[@]}"; do
        if [ "${profile}" = "${mode}" ]; then
            login_step="log in on this host, once per login group: seat-login-preflight ${profile} prints the ${group} group's command, docs/remote-host-logins.md"
            key_step="place the seats' API key on this host (one file for every seat): seat-login-preflight ${profile} prints the placement commands (handouts/anthropic-api-key-u510.md, steps 2 and 3), docs/remote-host-logins.md"
            break
        fi
    done
    if [ "${profile}" != "${mode}" ]; then
        login_step="log in on this host, once per login group: the ${profile} profile is the ${group} group, which has no seat-login-preflight profile mode; run claude auth login with CLAUDE_CONFIG_DIR set to the directory this line names (hcom-seat ${group} --dry-run prints it; BROWSER=regime-open-url first on a remote host), docs/remote-host-logins.md"
    fi
    if [ "${key_missing}" -eq 1 ]; then
        if [ "${login_missing}" -eq 1 ]; then
            login_step="${login_step}; ${key_step}"
        else
            login_step="the preflight passes on the group's login, but hcom-seat starts no seat until the key is placed; ${key_step}"
        fi
    elif [ "${key_ok}" -eq 1 ]; then
        login_step="the seat starts on the accepted key (U512e), so the login is information: ${login_step#log in on this host, once per login group: }"
    fi
}

#
# @description Report each omp seat profile's login on this host through
#   `scripts/orchestrator/seat-login-preflight --check` (regime-cutover U37):
#   presence and mtimes only, never a token. The Claude lines name each
#   profile's login group directory `<seats-root>/.state/claude-<group>`
#   (U498: one line per deployed profile, so one per running group) and, after
#   it on the same line, the seats' API key file's state (U512: `key ok`, or
#   its absence or rejection). An absent login, an absent or rejected key and
#   a profile without a route are optional warnings naming the step
#   (login_step_of, U498d), since a login and the key are per host and the
#   operator's steps; an unreadable record, in either state, and the lever's
#   own refusal are required failures, never read as absent. One failure
#   counts once (regime-cutover U512g, verdict U512f-b6a3e2c0 P1): every
#   `required failed` line counts where it is printed, and the lever's
#   non-zero exit counts only when the loop counted no line, since the exit
#   that follows a printed unreadable or refusal line is the same failure
#   (U512f counted the line and then the exit, so one unreadable key counted
#   twice); the line's own count is what holds an unreadable login beside an
#   accepted key, which the lever passes with exit 0 (verdict U512e-a120aeff
#   P2: that arm once printed without counting, so the doctor exited 0).
#
function check_seat_logins() {
    local lever="${BASH_SOURCE[0]%/*}/orchestrator/seat-login-preflight"
    local output line login_step status=0 counted=0

    if [ ! -x "${lever}" ]; then
        warn_optional "seat login check skipped: ${lever} is missing"
        return 0
    fi
    output="$("${lever}" --check 2>&1)" || status=$?
    while IFS= read -r line; do
        case "${line}" in
        '') ;;
        'not applicable:'*) printf '%s\n' "${line}" ;;
        # The lever's own refusal or failed producer (pin, uname), never a profile line; or either state of a
        # claude-bridge line unreadable (U512), the states matched anywhere after the route. One arm counts both, and
        # marks the count so the lever's exit below is not counted again for the same failure (U512g).
        'seat-login-preflight:'* | *': unreadable'* | *'; unreadable ('*)
            case "${line}" in
            'seat-login-preflight:'*) printf 'required failed: %s\n' "${line}" >&2 ;;
            *) printf 'required failed: seat login %s\n' "${line}" >&2 ;;
            esac
            ((required_failures += 1))
            counted=1
            ;;
        *': absent'* | *'; absent ('* | *'; key rejected ('* | *': no route'* | *': not a seat login route'*)
            login_step_of "${line}"
            warn_optional "seat login ${line} (${login_step})"
            ;;
        *) printf 'found:   seat login %s\n' "${line}" ;;
        esac
    done <<< "${output}"
    # The exit alone counts when no printed line did: a lever that died without a line of its own.
    if [ "${status}" -ne 0 ] && [ "${counted}" -eq 0 ]; then
        printf 'required failed: seat-login-preflight --check exited %d\n' "${status}" >&2
        ((required_failures += 1))
    fi
}

#
# @description Report the class of the Router's GitHub token through the checkout's
#   `scripts/orchestrator/router-gh api -i user` (regime-cutover U490), one call bounded by
#   perl's alarm (`timeout` is not on every host) to `DOCTOR_ROUTER_TIMEOUT` seconds (an
#   integer of 1 to 600; else 30), with the response headers read for `X-Oauth-Scopes` alone.
#   Five cases, decided by router-gh's exit status and, once gh has answered, by the HTTP status
#   line alone (U490e, U490f; the doctor holds no path test of its own: round 4's `[ ! -e ]` read
#   a login directory under an unreadable parent as absent where router-gh refuses `cannot resolve
#   the credential root`, verdict U490-e90feefa P1):
#   (a) router-gh exits 3, its "not yet" code (the credential root, its gh directory or its
#       hosts.yml absent, or hosts.yml naming no active login for github.com): the operator's
#       step (docs/engagement-handout.md step 2), an optional warning quoting router-gh's one
#       stderr line; gh itself is not run;
#   (b) router-gh exits 2, every other refusal (a DSH_HOME that is not a real, searchable
#       directory of this user, a link in the chain, a wrong owner or mode, a root that cannot be
#       resolved, several oauth_token rows, a token outside the grammar): a required failure
#       quoting router-gh's one stderr line (a broken root the operator must repair, never
#       "pending"; rounds 1 to 3 read every refusal as the pending step and exited 0, verdict
#       U490-f441420d P1);
#   (c) any other non-zero exit whose output's first line is an HTTP status line of class 4xx or
#       5xx (`^HTTP/[0-9.]+ [45][0-9][0-9]`; `gh api -i` prints the status line before the body
#       whatever the class and exits 1 on an error answer): GitHub answered and rejected the token
#       (revoked, expired or never valid), a required failure `GitHub answered <status line>` with
#       the remedy (U490f; round 5 read every exit of gh's own as "unreadable", so a revoked token
#       passed the gate as an optional warning, verdict U490-f6175c44 P1);
#   (d) any other non-zero exit with no HTTP status line in front (the alarm included, the
#       transport's own failure text for a host never reached), or an exit 0 without a 2xx status
#       line and a login: an optional warning `unreadable` (an offline or stalled host);
#   (e) a 2xx answer: no `X-Oauth-Scopes` header is a fine-grained token, whose permissions this
#       check cannot read and which cannot write here (GitHub's fine-grained tokens cannot
#       contribute to a repository where the account is a collaborator, and the Router's account
#       is one by the kit's design, M-25), a required failure (U490c); a header is a classic token,
#       found when its list holds `repo` or `public_repo`, else a required failure. Both failures
#       ask for the classic token of the handout's step 2 (`repo` for the writes, `read:org` and
#       `gist` for `gh auth login --with-token`, `notifications` for the poll; U490b), since no
#       other token lets the Router write (measured 2026-11-12: a `notifications` token read the
#       stream and every write failed `HTTP 403`).
#   The decision reads router-gh's exit status and gh's HTTP status line, never router-gh's text
#   and no path; the login is read from the body's `login` key; no token is printed.
#
function check_router_token() {
    local lever="${BASH_SOURCE[0]%/*}/orchestrator/router-gh"
    local root="${DSH_HOME:-${HOME%/}/.dsh}/router-credentials/gh"
    local output line status=0 in_headers=1 first_line='' body='' login='' scopes='' scopes_seen=0
    local scope writes=0 remedy bound=30
    local -a scope_list=()
    remedy="place the classic token of docs/engagement-handout.md step 2 (scopes repo, read:org, gist, notifications; a fine-grained token cannot write to a repository where the account is a collaborator) under ${root}"

    if [ ! -x "${lever}" ]; then
        warn_optional "router token check skipped: ${lever} is missing"
        return 0
    fi
    if [[ "${DOCTOR_ROUTER_TIMEOUT:-}" =~ ^[0-9]{1,3}$ ]] && [ "${DOCTOR_ROUTER_TIMEOUT}" -ge 1 ] && [ "${DOCTOR_ROUTER_TIMEOUT}" -le 600 ]; then
        bound="${DOCTOR_ROUTER_TIMEOUT}"
    fi
    output="$(perl -e 'my $bound = shift; alarm $bound; exec @ARGV or die "exec router-gh: $!\n"' "${bound}" "${lever}" api -i user 2>&1)" || status=$?
    if [ "${status}" -eq 3 ]; then
        IFS= read -r first_line <<< "${output}"
        warn_optional "router token: ${first_line}"
        return 0
    fi
    if [ "${status}" -eq 2 ]; then
        IFS= read -r first_line <<< "${output}"
        printf 'required failed: router token: %s\n' "${first_line}" >&2
        ((required_failures += 1))
        return 0
    fi
    if [ "${status}" -ne 0 ]; then
        IFS= read -r first_line <<< "${output}"
        first_line="${first_line%$'\r'}"
        if [[ "${first_line}" =~ ^HTTP/[0-9.]+\ [45][0-9][0-9] ]]; then
            printf 'required failed: router token: GitHub answered %s (the token is rejected or expired; %s)\n' \
                "${first_line}" "${remedy}" >&2
            ((required_failures += 1))
            return 0
        fi
        warn_optional "router token: unreadable (router-gh api -i user exited ${status}: ${first_line})"
        return 0
    fi
    # `gh api -i` prints the status line, each header with CRLF, a blank line, then the raw body.
    while IFS= read -r line; do
        line="${line%$'\r'}"
        if [ "${in_headers}" -eq 0 ]; then
            body="${body}${line}"
        elif [ -z "${first_line}" ]; then
            first_line="${line}"
        elif [ -z "${line}" ]; then
            in_headers=0
        elif [[ "${line}" =~ ^[Xx]-[Oo][Aa][Uu][Tt][Hh]-[Ss][Cc][Oo][Pp][Ee][Ss]:[[:space:]]*(.*)$ ]]; then
            scopes="${BASH_REMATCH[1]}"
            scopes_seen=1
        fi
    done <<< "${output}"
    if [[ ! "${first_line}" =~ ^HTTP/[0-9.]+\ 2[0-9][0-9] ]] || [[ ! "${body}" =~ \"login\":[[:space:]]*\"([A-Za-z0-9-]+)\" ]]; then
        warn_optional "router token: unreadable (router-gh api -i user answered without a 2xx status line and a login)"
        return 0
    fi
    login="${BASH_REMATCH[1]}"
    if [ "${scopes_seen}" -eq 0 ]; then
        printf "required failed: router token %s: fine-grained (no X-Oauth-Scopes header), which cannot write here (GitHub's fine-grained tokens cannot contribute to a repository where the account is a collaborator, and the Router's account is one by design); %s\n" \
            "${login}" "${remedy}" >&2
        ((required_failures += 1))
        return 0
    fi
    IFS=', ' read -r -a scope_list <<< "${scopes}"
    for scope in ${scope_list[@]+"${scope_list[@]}"}; do
        case "${scope}" in
        repo | public_repo) writes=1 ;;
        esac
    done
    if [ "${writes}" -eq 1 ]; then
        printf 'found:   router token %s: classic, scopes %s\n' "${login}" "${scopes}"
        return 0
    fi
    printf 'required failed: router token %s: classic token with scopes %s, none of which lets the Router write (the acknowledgement, a pushed ref, a pull request); %s\n' \
        "${login}" "${scopes:-<none>}" "${remedy}" >&2
    ((required_failures += 1))
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
    check_srt

    section "Seat logins"
    check_seat_logins
    check_router_token

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
