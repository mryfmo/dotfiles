#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/common/dependencies.sh"

@test "[ubuntu-common] PACKAGES for dependencies" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        printf "%s\n" "${#PACKAGES[@]}"
        printf "%s\n" "${PACKAGES[@]}"
    '

    [ "${status}" -eq 0 ]
    [ "${lines[0]}" -eq 15 ]

    expected_packages=(
        build-essential
        busybox
        cmake
        curl
        git
        gpg
        htop
        iproute2
        iputils-ping
        perl
        sudo
        unzip
        vim
        wget
        zsh
    )

    for ((i = 0; i < ${#expected_packages[*]}; ++i)); do
        [ "${lines[$((i + 1))]}" = "${expected_packages[$i]}" ]
    done
}

@test "[ubuntu-common] install_apt_packages installs only absent packages after update" {
    run bash -c '
        set +x
        unset DOTFILES_DEBUG
        source "'"${SCRIPT_PATH}"'"
        dpkg-query() {
            [ "$1" = "-W" ]
            [ "$2" = "-f=\${Status}" ]
            case "$3" in
                iproute2|iputils-ping|sudo)
                    printf "install ok installed\n"
                    ;;
                *)
                    return 1
                    ;;
            esac
        }
        run_apt_get() {
            printf "%s\n" "$*"
        }

        install_apt_packages
    '

    [ "${status}" -eq 0 ]
    actual_output="${output}"

    run bash -c '
        source "'"${SCRIPT_PATH}"'"

        install_targets=(update)
        for package in "${PACKAGES[@]}"; do
            if [ "${package}" != "iproute2" ] && [ "${package}" != "iputils-ping" ] && [ "${package}" != "sudo" ]; then
                install_targets+=("${package}")
            fi
        done

        printf "%s\n" "update" "install -y ${install_targets[*]:1}"
    '
    [ "${status}" -eq 0 ]
    [ "${actual_output}" = "${output}" ]
}

@test "[ubuntu-common] install_apt_packages exits early when nothing is missing" {
    run bash -c '
        set +x
        unset DOTFILES_DEBUG
        source "'"${SCRIPT_PATH}"'"
        dpkg-query() {
            printf "install ok installed\n"
        }
        sudo() {
            printf "unexpected:%s\n" "$*"
        }

        install_apt_packages
    '

    [ "${status}" -eq 0 ]
    [ -z "${output}" ]
}
