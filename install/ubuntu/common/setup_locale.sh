#!/usr/bin/env bash

# @file install/ubuntu/common/setup_locale.sh
# @brief Ensure the required locales exist on Ubuntu.
# @description
#   Generates missing English and Japanese UTF-8 locales and keeps English as
#   the system default.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly TARGETS=(
    en_US.UTF-8
    ja_JP.UTF-8
)

#
# @description Generate any required locales that are not already available.
#
function main() {
    local available target target_key
    local missing=()

    available="$(locale -a 2> /dev/null | tr '[:upper:]' '[:lower:]' | tr -d '-')"
    for target in "${TARGETS[@]}"; do
        target_key="$(printf '%s' "${target}" | tr '[:upper:]' '[:lower:]' | tr -d '-')"
        if ! grep -Fqx "${target_key}" <<< "${available}"; then
            missing+=("${target}")
        fi
    done

    if [ "${#missing[@]}" -eq 0 ]; then
        printf 'Required locales already exist.\n'
        return 0
    fi

    printf 'Generating %s ...\n' "${missing[*]}"
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y locales
    sudo locale-gen "${missing[@]}"
    sudo update-locale LANG="${TARGETS[0]}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
