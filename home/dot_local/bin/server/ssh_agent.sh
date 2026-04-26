#!/usr/bin/env bash

# @file home/dot_local/bin/server/ssh_agent.sh
# @brief Start `ssh-agent` and load the default SSH key when present.
# @description
#   Starts a new `ssh-agent` process and adds the default ed25519 private key
#   for the current user when the key exists. Private keys are intentionally not
#   stored in the public chezmoi source state.

set -Eeuo pipefail

readonly DEFAULT_SSH_KEY="${HOME}/.ssh/id_ed25519"

eval "$(ssh-agent)" > /dev/null 2>&1

if [[ -r "${DEFAULT_SSH_KEY}" ]]; then
    ssh-add "${DEFAULT_SSH_KEY}" > /dev/null 2>&1
else
    printf 'Default SSH key not found: %s\n' "${DEFAULT_SSH_KEY}" >&2
    printf 'Skipping ssh-add; restore the key from private state or create one with ssh-keygen.\n' >&2
fi
