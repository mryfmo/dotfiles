#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/misc.sh"

load "../../helpers/apt_record"

# @description Every case runs with a fake snap first on PATH (U210): a case that runs the script's main, or the
#   script as a program, reaches `sudo timeout ... snap install chromium`, and on an Ubuntu runner that was the real
#   snap client against the real store, which stalled the whole test leg for nine minutes on 2026-11-05. The fake
#   records its argv and succeeds at once; a case that needs another behaviour overrides it with fake_snap on the
#   same path.
# @noargs
# @set PATH string The fixture's bin first: the fake snap and the PATH-keeping sudo, before anything of the host.
function setup() {
    source "${SCRIPT_PATH}"
    path_keeping_sudo
    fake_snap 'exit 0'
    PATH="${BATS_TEST_TMPDIR}/bin:${PATH}"
}

# Only a case that installed for real removes what it installed (U41): before, every case ran
# the installer's uninstall function (removed in U46), and the array cases' teardown removed the runner image's own packages.
function teardown() {
    remove_real_packages
}

# @description Write the fake snap the fixture puts first on PATH. It appends `snap <argv>` to
#   ${BATS_TEST_TMPDIR}/snap_calls and then runs $1, whose status is the fake's. The log path is written into the
#   script, because the real sudo drops the caller's environment; the fake is a program and not a shell function,
#   because install_chromium runs snap through `timeout`.
# @arg $1 string The shell text the fake runs after logging; its exit status is the fake's (`exit 0` in setup).
function fake_snap() {
    mkdir -p "${BATS_TEST_TMPDIR}/bin"
    {
        printf '#!/bin/bash\n'
        printf 'SNAP_CALLS=%q\n' "${BATS_TEST_TMPDIR}/snap_calls"
        printf 'printf "snap %%s\\n" "$*" >> "${SNAP_CALLS}"\n'
        printf '%s\n' "$1"
    } > "${BATS_TEST_TMPDIR}/bin/snap"
    chmod +x "${BATS_TEST_TMPDIR}/bin/snap"
}

# @description Write a sudo in front of the real one that hands the caller's PATH to the command it runs as root.
#   The real sudo replaces PATH with its secure_path, so a case that runs the script as a program would otherwise
#   reach the host's snap through it; the apt install itself still runs as root.
# @noargs
# @stderr `path_keeping_sudo: no sudo on PATH` when the lookup fails.
# @exitcode 1 No sudo on PATH: a wrapper around nothing would fail every program run with its own name in place of
#   the real cause, so the fixture refuses here instead of writing it.
function path_keeping_sudo() {
    local real_sudo
    if ! real_sudo="$(command -v sudo)"; then
        printf 'path_keeping_sudo: no sudo on PATH\n' >&2
        return 1
    fi
    mkdir -p "${BATS_TEST_TMPDIR}/bin"
    printf '#!/bin/bash\nexec %q env "PATH=${PATH}" "$@"\n' "${real_sudo}" > "${BATS_TEST_TMPDIR}/bin/sudo"
    chmod +x "${BATS_TEST_TMPDIR}/bin/sudo"
}

@test "[ubuntu-client] PACKAGES for misc" {
    num_packages="${#PACKAGES[@]}"
    [ $num_packages -eq 9 ]

    expected_packages=(
        gparted
        language-pack-ja
        fonts-noto-cjk
        fonts-noto-color-emoji
        ibus-mozc
        libnss3
        libgtk-3-0t64
        libasound2t64
        libgbm1
    )
    for ((i = 0; i < ${#expected_packages[*]}; ++i)); do
        [ "${PACKAGES[$i]}" == "${expected_packages[$i]}" ]
    done
}

@test "[ubuntu-client] misc" {
    install_real_packages "${PACKAGES[@]}"

    for package in gparted language-pack-ja fonts-noto-cjk fonts-noto-color-emoji ibus-mozc libnss3 libgtk-3-0t64 libasound2t64 libgbm1; do
        run dpkg -s "${package}"
        [ "${status}" -eq 0 ]
    done

    # The program reached the fixture's snap, once, through sudo; the store was never asked.
    [ "$(grep -c '^snap install chromium$' "${BATS_TEST_TMPDIR}/snap_calls")" -eq 1 ]
}

@test "[ubuntu-client] install_misc refreshes the index before installing" {
    run bash -c 'source "'"${SCRIPT_PATH}"'"; sudo() { echo "$*" >> "'"${BATS_TEST_TMPDIR}"'/sudo.log"; }; install_misc'
    [ "${status}" -eq 0 ]
    [ "$(sed -n 1p "${BATS_TEST_TMPDIR}/sudo.log")" = "apt-get update" ]
    # The frontend must be an argument to sudo: env_reset drops it from the caller's environment.
    [[ "$(sed -n 2p "${BATS_TEST_TMPDIR}/sudo.log")" == "DEBIAN_FRONTEND=noninteractive apt-get install -y "* ]]
}

@test "[ubuntu-client] install_chromium is a no-op when snap is unavailable" {
    run env PATH="${BATS_TEST_TMPDIR}" /bin/bash -c '
        source "'"${SCRIPT_PATH}"'"
        install_chromium
    '
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-client] install_misc asks apt-get for every package in PACKAGES at once" {
    run record_apt_calls "${SCRIPT_PATH}" install_misc
    [ "${status}" -eq 0 ]
    [ "$(grep -c '^apt-get install ' <<< "${output}")" -eq 1 ]
    grep -qxF "apt-get install -y ${PACKAGES[*]}" <<< "${output}"
}

@test "[ubuntu-client] the recorded install_misc call catches an installer that drops a package" {
    local mutant="${BATS_TEST_TMPDIR}/misc.sh" calls
    sed 's/apt-get install -y "${PACKAGES\[@\]}"/apt-get install -y "${PACKAGES[@]:1}"/' "${SCRIPT_PATH}" > "${mutant}"
    if cmp -s "${SCRIPT_PATH}" "${mutant}"; then
        false
    fi
    run record_apt_calls "${mutant}" install_misc
    [ "${status}" -eq 0 ]
    calls="${output}"
    # The recorder saw the mutant's call, and the check above would refuse it.
    grep -qxF "apt-get install -y ${PACKAGES[*]:1}" <<< "${calls}"
    if grep -qxF "apt-get install -y ${PACKAGES[*]}" <<< "${calls}"; then
        false
    fi
}

@test "[ubuntu-client] main reaches the fixture's snap and returns its status, never the host's" {
    # A status no snap client returns: a run that reached the host's snap could not produce it, and a case that
    # loses the fixture shows as an empty snap_calls.
    fake_snap 'if [ "$1" = install ]; then exit 99; fi'
    export SNAP_RETRY_DELAY=0
    run record_apt_calls "${SCRIPT_PATH}" main
    [ "${status}" -eq 99 ]
    grep -qxF "apt-get install -y ${PACKAGES[*]}" <<< "${output}"
    [[ "${output}" == *"install_chromium: snap install chromium failed (attempt 3/3, exit 99)"* ]]
    [ "$(grep -c '^snap install chromium$' "${BATS_TEST_TMPDIR}/snap_calls")" -eq 3 ]
}

# Run install_chromium with sudo as a pass-through and the given environment; the fixture's fake snap is first on PATH.
function run_install_chromium() {
    run env "$@" /bin/bash -c '
        source "$1"
        sudo() {
            "$@"
        }
        install_chromium
    ' _ "${SCRIPT_PATH}"
}

@test "[ubuntu-client] install_chromium retries a failed snap install and succeeds on the third attempt" {
    fake_snap '[ "$(wc -l < "${SNAP_CALLS}")" -ge 3 ]'
    run_install_chromium SNAP_RETRY_DELAY=0
    [ "${status}" -eq 0 ]
    [ "$(grep -c '^snap install chromium$' "${BATS_TEST_TMPDIR}/snap_calls")" -eq 3 ]
}

@test "[ubuntu-client] install_chromium fails after three failed snap installs" {
    fake_snap 'exit 1'
    run_install_chromium SNAP_RETRY_DELAY=0
    [ "${status}" -ne 0 ]
    [ "$(grep -c '^snap install chromium$' "${BATS_TEST_TMPDIR}/snap_calls")" -eq 3 ]
}

@test "[ubuntu-client] install_chromium stops a stalled snap install at SNAP_INSTALL_TIMEOUT and names the step" {
    # The fake snap hangs like a snap client waiting on a stalled store download.
    fake_snap 'exec sleep 60'
    SECONDS=0
    run_install_chromium SNAP_RETRY_DELAY=0 SNAP_INSTALL_TIMEOUT=1
    [ "${status}" -eq 124 ]
    [ "${SECONDS}" -lt 30 ]
    [[ "${output}" == *"install_chromium: snap install chromium timed out after 1 s (SNAP_INSTALL_TIMEOUT)"* ]]
    # Not retried: snapd keeps the change running after its client stops.
    [ "$(grep -c '^snap install chromium$' "${BATS_TEST_TMPDIR}/snap_calls")" -eq 1 ]
}
