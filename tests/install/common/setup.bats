#!/usr/bin/env bats

@test "[common] setup.sh keeps macOS sudo alive without Keychain password storage" {
    run grep -Eq "add-generic-password|find-generic-password|delete-generic-password|SUDO_ASKPASS|security -i" setup.sh
    [ "$status" -eq 1 ]

    grep -q "/usr/bin/sudo -v" setup.sh
    grep -q "/usr/bin/sudo -n true" setup.sh
}

@test "[common] setup.sh updates an existing chezmoi source before applying" {
    local update_count
    local update_line
    local apply_count
    local apply_line
    local update_block

    update_count="$(grep -c '"${chezmoi_cmd}" update' setup.sh)"
    apply_count="$(grep -c '"${chezmoi_cmd}" apply' setup.sh)"
    [ "${update_count}" -eq 1 ]
    [ "${apply_count}" -eq 1 ]

    update_line="$(grep -n '"${chezmoi_cmd}" update' setup.sh | head -n 1 | cut -d: -f1)"
    apply_line="$(grep -n '"${chezmoi_cmd}" apply' setup.sh | head -n 1 | cut -d: -f1)"

    [ -n "${update_line}" ]
    [ -n "${apply_line}" ]
    [ "${update_line}" -lt "${apply_line}" ]

    update_block="$(sed -n "${update_line},${apply_line}p" setup.sh)"
    grep -q -- '--apply=false' <<< "${update_block}"
    grep -q -- '--init' <<< "${update_block}"
}
