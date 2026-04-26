#!/usr/bin/env bash

# @file home/dot_local/bin/server/ssh_agent.sh
# @brief Start `ssh-agent` and load the default SSH key when present.
# @description
#   Starts a new `ssh-agent` process and adds the default ed25519 private key
#   for the current user when the key exists. This file is sourced by sheldon,
#   so it must not enable strict shell options in the parent interactive shell.
#   Private keys are intentionally not stored in the public chezmoi source state.

function _dotfiles_start_ssh_agent() {
    local default_ssh_key="${HOME}/.ssh/id_ed25519"

    eval "$(ssh-agent)" > /dev/null 2>&1 || return 0

    if [[ -r "${default_ssh_key}" ]]; then
        ssh-add "${default_ssh_key}" > /dev/null 2>&1 || \
            printf 'Failed to add default SSH key: %s\n' "${default_ssh_key}" >&2
    else
        printf 'Default SSH key not found: %s\n' "${default_ssh_key}" >&2
        printf 'Skipping ssh-add; restore the key from private state or create one with ssh-keygen.\n' >&2
    fi
}

_dotfiles_start_ssh_agent
unset -f _dotfiles_start_ssh_agent
