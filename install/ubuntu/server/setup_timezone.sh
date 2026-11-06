#!/usr/bin/env bash

# @file install/ubuntu/server/setup_timezone.sh
# @brief Configure the server timezone.
# @description
#   Points `/etc/localtime` and `/etc/timezone` at `Asia/Tokyo` and installs `tzdata` non-interactively, once.
#   It does nothing on a GitHub runner, because replacing `/etc/localtime` there stalled every server bootstrap
#   leg until the 35-minute cancel (regime-cutover U254, bisected by PRs 681 to 690) and the runner's clock is not
#   the kit's to set. It does nothing when `/etc/localtime` already resolves to the zone, so a second run on a host
#   changes no file.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Print the zone file `/etc/localtime` resolves to.
# @stdout The resolved path, `/usr/share/zoneinfo/Asia/Tokyo` on a configured host.
# @exitcode 1 The link cannot be resolved; the caller reads this as an unknown zone.
#
function current_zone_file() {
    readlink -f /etc/localtime 2> /dev/null
}

#
# @description Apply the repository's preferred timezone configuration, or print why it is left as it is.
# @set TZ string `Asia/Tokyo`, exported for the rest of the bootstrap.
# @stdout One line: `timezone: unchanged on a GitHub runner ...`, `timezone: already <TZ>`, or `timezone: setting
#   <TZ> (was <zone file or unknown>)` followed by the commands' own output.
#
function main() {
    export TZ="Asia/Tokyo"

    if [ -n "${GITHUB_ACTIONS:-}" ]; then
        echo "timezone: unchanged on a GitHub runner (GITHUB_ACTIONS is set; replacing /etc/localtime stalls the runner, regime-cutover U254)"
        return 0
    fi

    local current_zone_file
    if ! current_zone_file="$(current_zone_file)"; then
        current_zone_file=""
    fi
    if [[ "${current_zone_file}" == */"${TZ}" ]]; then # lint-comparisons: allow zone-is-the-path-tail (the file was resolved by readlink -f above; tzdata names a zone by its path under zoneinfo, so the tail is the zone, not a path identity)
        echo "timezone: already ${TZ}"
        return 0
    fi

    echo "timezone: setting ${TZ} (was ${current_zone_file:-unknown})"
    sudo ln -snf "/usr/share/zoneinfo/${TZ}" /etc/localtime
    echo "${TZ}" | sudo tee /etc/timezone

    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
