#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/common/setup_locale.sh"
readonly TMPL_PATH="./home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl"

@test "[ubuntu-common] setup_locale generates only missing required locales" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        locale() {
            [ "$1" = "-a" ]
            printf "C\nen_US.utf8\n"
        }
        sudo() {
            printf "%s\n" "$*"
        }
        main
    '

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"apt-get install -y locales"* ]]
    [[ "${output}" == *"locale-gen ja_JP.UTF-8"* ]]
    [[ "${output}" != *"locale-gen en_US.UTF-8"* ]]
    [[ "${output}" == *"update-locale LANG=en_US.UTF-8"* ]]
}

@test "[ubuntu-common] setup_locale runs for both Ubuntu roles" {
    grep -Fq 'include "../install/ubuntu/common/setup_locale.sh"' "${TMPL_PATH}"

    run grep -F '.system' "${TMPL_PATH}"
    [ "${status}" -ne 0 ]
}
