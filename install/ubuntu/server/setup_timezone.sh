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
    if command -v timedatectl > /dev/null 2>&1 && [ -d /run/systemd/system ]; then
        sudo timedatectl set-timezone "${TZ}" # probe (U237): the systemd route instead of ln and tee
    else
        sudo ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime
        echo "${TZ}" | sudo tee /etc/timezone
    fi

    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
