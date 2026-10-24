#!/usr/bin/env bash

# @file tests/install/helpers/apt_record.bash
# @brief Real apt installs that undo only what the case installed, and apt calls recorded without running apt.
# @description
#   Loaded by the Ubuntu client install tests. A case that proves a real install calls install_real_packages,
#   and its file's teardown calls remove_real_packages: the teardown then removes only the packages that case
#   installed, so a case that installs nothing removes nothing, and no teardown takes the runner image's own
#   packages (and what depends on them, such as its browsers and JDKs) with it. A case that checks the command
#   an installer builds calls record_apt_calls instead of apt.

#
# @description Run the installer under test for real, after noting which of its packages are not installed yet.
# @arg $@ string The packages the installer installs; at least one.
# @set REAL_PACKAGES_NEW array The given packages that were not installed before this call.
# @exitcode 1 No package was given: the teardown could not undo the install, so the case fails instead.
# @exitcode The installer's exit status otherwise.
#
function install_real_packages() {
    local package
    if [ "$#" -eq 0 ]; then
        printf 'install_real_packages: no package given for %s; its teardown could not remove what it installs\n' \
            "${SCRIPT_PATH}" >&2
        return 1
    fi
    REAL_PACKAGES_NEW=()
    for package in "$@"; do
        if [ "$(dpkg-query -W -f='${Status}' "${package}" 2> /dev/null)" != "install ok installed" ]; then
            REAL_PACKAGES_NEW+=("${package}")
        fi
    done
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"
}

#
# @description Remove the packages install_real_packages found missing; nothing in a case that did not call it.
# @noargs
#
function remove_real_packages() {
    # The installers under test run `set -u`, and a case that installed nothing never set the array.
    [ -n "${REAL_PACKAGES_NEW+set}" ] && [ "${#REAL_PACKAGES_NEW[@]}" -gt 0 ] || return 0
    run sudo apt-get remove -y "${REAL_PACKAGES_NEW[@]}"
}

#
# @description Call an installer function with sudo and apt-get replaced, printing each apt-get call.
# @arg $1 path The installer script to source.
# @arg $2 string The function to call.
# @stdout One line per apt-get call: `apt-get` and its arguments, space-separated.
# @exitcode The function's exit status.
#
function record_apt_calls() {
    bash -c '
        source "$1"
        sudo() {
            while [ "$#" -gt 0 ] && [[ $1 == -* ]]; do
                shift
            done
            "$@"
        }
        apt-get() {
            printf "apt-get %s\n" "$*"
        }
        "$2"
    ' _ "$1" "$2"
}
