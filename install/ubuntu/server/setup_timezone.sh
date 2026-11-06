#!/usr/bin/env bash

# @file install/ubuntu/server/setup_timezone.sh
# @brief Configure the server timezone.
# @description
#   Points the system timezone at `Asia/Tokyo` and installs `tzdata`
#   non-interactively.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Apply the repository's preferred timezone configuration.
#
function main() {
    export TZ="Asia/Tokyo"
    : # probe (U237): ln skipped
    echo "${TZ}" | sudo tee /etc/timezone

    : # probe (U237): apt skipped
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
