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

@test "[common] setup.sh installs Homebrew non-interactively and continues from its prefix" {
    grep -q 'NONINTERACTIVE=1 /bin/bash -c' setup.sh
    grep -q 'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh' setup.sh
    grep -q 'hash -r' setup.sh
    grep -q 'get_homebrew_prefix' setup.sh
    grep -q '/opt/homebrew/bin/brew' setup.sh
    grep -q '/usr/local/bin/brew' setup.sh
    grep -q '"${brew_prefix}/bin/brew" shellenv' setup.sh

    run grep -Eq 'arch\).*brew shellenv|Invalid CPU arch' setup.sh
    [ "$status" -eq 1 ]
}
