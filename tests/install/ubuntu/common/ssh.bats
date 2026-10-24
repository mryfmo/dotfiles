#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/common/ssh.sh"

load "../../helpers/apt_record"

function setup() {
    source "${SCRIPT_PATH}"
}

# Only a case that installed for real removes what it installed (U45, the U41 form): before, every case ran
# uninstall_openssh, which removed the runner image's own openssh-client after the first case.
function teardown() {
    remove_real_packages
}

@test "[ubuntu-common] PACKAGES for ssh" {
    [ ${#PACKAGES[@]} -eq 1 ]
}

@test "[ubuntu-common] install_github_host_key adds the pinned key once" {
    local home_dir="${BATS_TEST_TMPDIR}/home"

    run env HOME="${home_dir}" bash -c '
        source "'"${SCRIPT_PATH}"'"
        install_github_host_key
        install_github_host_key
        cat "${HOME}/.ssh/known_hosts"
    '

    [ "${status}" -eq 0 ]
    [ "${#lines[@]}" -eq 1 ]
    [ "${lines[0]}" = "github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl" ]
}

@test "[ubuntu-common] ssh" {
    install_real_packages "${PACKAGES[@]}"

    run dpkg -s 'openssh-client'
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-common] uninstall_openssh issues apt remove" {
    run bash -c '
        set +x
        unset DOTFILES_DEBUG
        source "'"${SCRIPT_PATH}"'"
        set +x
        sudo() {
            printf "%s\n" "$*"
        }

        uninstall_openssh
    '

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"apt-get remove -y openssh-client"* ]]
}

@test "[ubuntu-common] uninstall_openssh removes exactly the packages install_openssh installs" {
    local installed removed

    run record_apt_calls "${SCRIPT_PATH}" install_openssh
    [ "${status}" -eq 0 ]
    installed="$(apt_call_packages install <<< "${output}")"
    [ -n "${installed}" ]

    run record_apt_calls "${SCRIPT_PATH}" uninstall_openssh
    [ "${status}" -eq 0 ]
    [ "$(grep -c '^apt-get remove ' <<< "${output}")" -eq 1 ]
    removed="$(apt_call_packages remove <<< "${output}")"

    [ "${removed}" = "${installed}" ]
}

@test "[ubuntu-common] the recorded uninstall_openssh call catches an uninstaller that drops a package" {
    local mutant="${BATS_TEST_TMPDIR}/ssh.sh" installed removed
    sed 's/apt-get remove -y "${PACKAGES\[@\]}"/apt-get remove -y "${PACKAGES[@]:1}"/' "${SCRIPT_PATH}" > "${mutant}"
    if cmp -s "${SCRIPT_PATH}" "${mutant}"; then
        false
    fi

    run record_apt_calls "${mutant}" install_openssh
    [ "${status}" -eq 0 ]
    installed="$(apt_call_packages install <<< "${output}")"
    run record_apt_calls "${mutant}" uninstall_openssh
    [ "${status}" -eq 0 ]
    removed="$(apt_call_packages remove <<< "${output}")"

    # The recorder saw the mutant's call, and the comparison above would refuse it.
    [ "$(grep -c '^apt-get remove ' <<< "${output}")" -eq 1 ]
    [ "${removed}" != "${installed}" ]
}
