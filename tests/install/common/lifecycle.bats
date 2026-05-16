#!/usr/bin/env bats

@test "[common] Makefile exposes the public lifecycle targets" {
    make -n setup
    make -n update
    make -n doctor
    make -n upgrade
}

@test "[common] Makefile keeps apply as a compatibility alias" {
    make -n apply
}

@test "[common] Makefile force-applies only Hermes runtime config before normal update" {
    run make -n update
    [ "$status" -eq 0 ]
    [[ "$output" == *'chezmoi apply --verbose --force ~/.hermes'* ]]
    grep -xF 'chezmoi apply --verbose' <<<"$output"
}

@test "[common] Makefile treats private chezmoi as optional during update" {
    run make -n update
    [ "$status" -eq 0 ]
    # `make -n` prints the shell branch text without executing it; this asserts
    # the optional-private guard is present in the generated recipe.
    [[ "$output" == *'$HOME/.local/share/chezmoi-private'* ]]
    [[ "$output" == *'$HOME/.config/chezmoi-private/chezmoi.yaml'* ]]
    [[ "$output" == *'--source "$HOME/.local/share/chezmoi-private"'* ]]
    [[ "$output" == *'Skipping private dotfiles'* ]]
    [[ "$output" != *'chezmoi-private apply'* ]]
}

@test "[common] Makefile maps SYSTEM=1 upgrade to system package upgrades" {
    run make -n upgrade SYSTEM=1
    [ "$status" -eq 0 ]
    [[ "$output" == *'./scripts/upgrade-tools.sh --system'* ]]
}

@test "[common] Makefile does not treat SYSTEM=0 as a system package upgrade request" {
    run make -n upgrade SYSTEM=0
    [ "$status" -eq 0 ]
    [[ "$output" == *'./scripts/upgrade-tools.sh '* ]]
    [[ "$output" != *'--system'* ]]
}

@test "[common] Makefile skips private init when chezmoi-private is unavailable" {
    run make -n init
    [ "$status" -eq 0 ]
    [[ "$output" == *'command -v chezmoi-private'* ]]
    [[ "$output" == *'Skipping private dotfiles init'* ]]
}

@test "[common] Makefile does not expose a separate upgrade-system target" {
    run make -n upgrade-system
    [ "$status" -ne 0 ]
}

@test "[common] setup.sh does not upgrade installed tools during bootstrap" {
    run grep -Eq 'brew upgrade|apt-get (dist-upgrade|full-upgrade|upgrade)|mise upgrade|uv tool upgrade|gh extension upgrade|cargo install .*--force|npm update -g' setup.sh
    [ "$status" -eq 1 ]
}

@test "[common] explicit tool lifecycle scripts are present" {
    [ -x scripts/upgrade-tools.sh ]
    [ -x scripts/check-tools.sh ]
}

@test "[common] doctor uses OS-aware mise listing" {
    grep -q 'run_optional_doctor mise ls --current' scripts/check-tools.sh
    ! grep -q 'run_optional_doctor mise current' scripts/check-tools.sh
}

@test "[common] upgrade lifecycle refreshes mise itself before mise-managed tools" {
    local self_update_line
    local install_line

    grep -q 'mise self-update --yes' scripts/upgrade-tools.sh
    self_update_line="$(grep -n 'upgrade_mise_self' scripts/upgrade-tools.sh | tail -n 1 | cut -d: -f1)"
    install_line="$(grep -n 'upgrade_mise_tools' scripts/upgrade-tools.sh | tail -n 1 | cut -d: -f1)"

    [ -n "${self_update_line}" ]
    [ -n "${install_line}" ]
    [ "${self_update_line}" -lt "${install_line}" ]
}

@test "[common] Hermes home is managed as a private directory" {
    [ -d home/private_dot_hermes ]
    [ ! -e home/dot_hermes ]
    [ -f home/private_dot_hermes/private_config.yaml.tmpl ]
}

@test "[common] README documents setup update doctor and upgrade lifecycle" {
    grep -q '### Lifecycle' README.md
    grep -q 'make setup' README.md
    grep -q 'make update' README.md
    grep -q 'make doctor' README.md
    grep -q 'make upgrade' README.md
    grep -q 'make upgrade SYSTEM=1' README.md
    grep -q 'setup.sh' README.md
}
