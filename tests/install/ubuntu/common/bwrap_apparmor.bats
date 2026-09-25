#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/common/bwrap_apparmor.sh"
readonly TMPL_PATH="./home/.chezmoiscripts/ubuntu/run_once_before_51-setup-bwrap-apparmor.sh.tmpl"

function run_bwrap_apparmor() {
    local sysctl_value="$1"
    local apparmor_active="${2:-0}"
    local sysctl_path="${BATS_TEST_TMPDIR}/apparmor_restrict_unprivileged_userns"

    if [ "${sysctl_value}" != "absent" ]; then
        printf '%s\n' "${sysctl_value}" > "${sysctl_path}"
    fi

    run env BWRAP_APPARMOR_SYSCTL="${sysctl_path}" \
        BWRAP_APPARMOR_PROFILE="${BATS_TEST_TMPDIR}/bwrap" \
        APPARMOR_ACTIVE="${apparmor_active}" bash -c '
        source "'"${SCRIPT_PATH}"'"
        sudo() {
            printf "sudo %s\n" "$*"
            "$@"
        }
        systemctl() {
            printf "systemctl %s\n" "$*"
            [ "$1" != "is-active" ] || [ "${APPARMOR_ACTIVE}" -eq 0 ]
        }
        main
    '
}

@test "[ubuntu-common] bwrap_apparmor skips when user namespaces are not restricted" {
    for sysctl_value in absent 0; do
        run_bwrap_apparmor "${sysctl_value}"
        [ "${status}" -eq 0 ]
        [[ "${output}" == *"skipping the bwrap AppArmor profile"* ]]
        [[ "${output}" != *"sudo"* ]]
        [ ! -e "${BATS_TEST_TMPDIR}/bwrap" ]
    done
}

@test "[ubuntu-common] bwrap_apparmor installs the documented profile and reloads AppArmor" {
    run_bwrap_apparmor 1
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"sudo tee ${BATS_TEST_TMPDIR}/bwrap"* ]]
    [[ "${output}" == *"sudo systemctl reload apparmor"* ]]
    grep -Fqx 'profile bwrap /usr/bin/bwrap flags=(unconfined) {' "${BATS_TEST_TMPDIR}/bwrap"
    grep -Fqx '  userns,' "${BATS_TEST_TMPDIR}/bwrap"
}

@test "[ubuntu-common] bwrap_apparmor is idempotent once the profile matches" {
    run_bwrap_apparmor 1
    [ "${status}" -eq 0 ]

    run_bwrap_apparmor 1
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"already installed"* ]]
    [[ "${output}" != *"sudo"* ]]
}

@test "[ubuntu-common] bwrap_apparmor defers the reload when AppArmor is inactive" {
    run_bwrap_apparmor 1 1
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"sudo tee"* ]]
    [[ "${output}" != *"reload apparmor"* ]]
    [[ "${output}" == *"takes effect when AppArmor starts"* ]]
}

@test "[ubuntu-common] bwrap_apparmor runs for both Ubuntu roles" {
    grep -Fq 'include "../install/ubuntu/common/bwrap_apparmor.sh"' "${TMPL_PATH}"

    run grep -F '.system' "${TMPL_PATH}"
    [ "${status}" -ne 0 ]
}
