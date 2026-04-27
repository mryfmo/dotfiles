#!/usr/bin/env bats

@test "[common] setup.sh keeps macOS sudo alive without Keychain password storage" {
    run grep -Eq "add-generic-password|find-generic-password|delete-generic-password|SUDO_ASKPASS|security -i" setup.sh
    [ "$status" -eq 1 ]

    grep -q "/usr/bin/sudo -v" setup.sh
    grep -q "/usr/bin/sudo -n true" setup.sh
}

@test "[common] setup.sh updates an existing chezmoi source before applying" {
    grep -q '"${chezmoi_cmd}" update' setup.sh
    grep -q -- '--apply=false' setup.sh
    grep -q -- '--init' setup.sh
    grep -q '"${chezmoi_cmd}" apply' setup.sh
}
