#!/usr/bin/env bash

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

# shellcheck disable=SC2016
declare -r DOTFILES_LOGO='
                          /$$                                      /$$
                         | $$                                     | $$
     /$$$$$$$  /$$$$$$  /$$$$$$   /$$   /$$  /$$$$$$      /$$$$$$$| $$$$$$$
    /$$_____/ /$$__  $$|_  $$_/  | $$  | $$ /$$__  $$    /$$_____/| $$__  $$
   |  $$$$$$ | $$$$$$$$  | $$    | $$  | $$| $$  \ $$   |  $$$$$$ | $$  \ $$
    \____  $$| $$_____/  | $$ /$$| $$  | $$| $$  | $$    \____  $$| $$  | $$
    /$$$$$$$/|  $$$$$$$  |  $$$$/|  $$$$$$/| $$$$$$$//$$ /$$$$$$$/| $$  | $$
   |_______/  \_______/   \___/   \______/ | $$____/|__/|_______/ |__/  |__/
                                           | $$
                                           | $$
                                           |__/

             *** This is setup script for my dotfiles setup ***            
                     https://github.com/mryfmo/dotfiles
'

declare -r DOTFILES_REPO_URL="https://github.com/mryfmo/dotfiles"
declare -r BRANCH_NAME="${BRANCH_NAME:-main}"

function is_ci() {
    "${CI:-false}"
}

function is_tty() {
    [ -t 0 ]
}

function is_not_tty() {
    ! is_tty
}

function is_ci_or_not_tty() {
    is_ci || is_not_tty
}

function at_exit() {
    AT_EXIT+="${AT_EXIT:+$'\n'}"
    AT_EXIT+="${*?}"
    # shellcheck disable=SC2064
    trap "${AT_EXIT}" EXIT
}

function get_os_type() {
    uname
}

function keepalive_sudo_linux() {
    # Might as well ask for password up-front, right?
    echo "Checking for \`sudo\` access which may request your password."
    sudo -v

    # Keep-alive: update existing sudo time stamp if set, otherwise do nothing.
    while true; do
        sudo -n true
        sleep 60
        kill -0 "$$" || exit
    done 2> /dev/null &
}

function keepalive_sudo_macos() {
    # Ask for sudo access up front and keep the sudo timestamp alive without
    # storing the user's login password in Keychain. Keychain writes can fail in
    # fresh macOS bootstrap sessions with Security error -25308.
    echo "Checking for \`sudo\` access which may request your password."
    /usr/bin/sudo -v

    # Keep-alive: update existing sudo time stamp if set, otherwise do nothing.
    while true; do
        /usr/bin/sudo -n true
        sleep 60
        kill -0 "$$" || exit
    done 2> /dev/null &
}

function keepalive_sudo() {

    local ostype
    ostype="$(get_os_type)"

    if [ "${ostype}" == "Darwin" ]; then
        keepalive_sudo_macos
    elif [ "${ostype}" == "Linux" ]; then
        keepalive_sudo_linux
    else
        echo "Invalid OS type: ${ostype}" >&2
        exit 1
    fi
}

function initialize_os_macos() {
    local brew_prefix

    function is_homebrew_exists() {
        command -v brew &> /dev/null
    }

    function get_homebrew_prefix() {
        if is_homebrew_exists; then
            brew --prefix
            return
        fi

        if [[ -x /opt/homebrew/bin/brew ]]; then
            printf '%s\n' /opt/homebrew
            return
        fi

        if [[ -x /usr/local/bin/brew ]]; then
            printf '%s\n' /usr/local
            return
        fi

        return 1
    }

    # Install Homebrew without letting its interactive prompts consume the outer
    # bootstrap session. The installer still prints its upstream "Next steps"
    # block, so explicitly continue by loading brew from the installation prefix.
    if ! is_homebrew_exists; then
        NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL \
            https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        hash -r
    fi

    if ! brew_prefix="$(get_homebrew_prefix)"; then
        echo "Homebrew was not found after installation; cannot continue bootstrap." >&2
        exit 1
    fi

    eval "$("${brew_prefix}/bin/brew" shellenv)"
}

function initialize_os_linux() {
    :
}

function initialize_os_env() {
    local ostype
    ostype="$(get_os_type)"

    if [ "${ostype}" == "Darwin" ]; then
        initialize_os_macos
    elif [ "${ostype}" == "Linux" ]; then
        initialize_os_linux
    else
        echo "Invalid OS type: ${ostype}" >&2
        exit 1
    fi
}

function run_chezmoi() {
    local bin_dir="${HOME}/.local/bin"
    export PATH="${PATH}:${bin_dir}"

    # download the chezmoi binary from the URL
    sh -c "$(curl -fsLS get.chezmoi.io)" -- -b "${bin_dir}"
    local chezmoi_cmd="${bin_dir}/chezmoi"

    if is_ci_or_not_tty; then
        no_tty_option="--no-tty" # /dev/tty is not available (especially in the CI)
    else
        no_tty_option="" # /dev/tty is available OR not in the CI
    fi
    # run `chezmoi init` to setup the source directory,
    # generate the config file, and optionally update the destination directory
    # to match the target state.
    "${chezmoi_cmd}" init "${DOTFILES_REPO_URL}" \
        --force \
        --branch "${BRANCH_NAME}" \
        --use-builtin-git true \
        ${no_tty_option}

    # Pull the latest source before applying so repeating the README snippet in
    # the same terminal picks up fixes merged after a previous failed run.
    "${chezmoi_cmd}" update \
        --apply=false \
        --init \
        --force \
        --use-builtin-git true \
        ${no_tty_option}

    # the `age` command requires a tty, but there is no tty in the github actions.
    # Therefore, it is currnetly difficult to decrypt the files encrypted with `age` in this workflow.
    # I decided to temporarily remove the encrypted target files from chezmoi's control.
    if is_ci_or_not_tty; then
        find "$(${chezmoi_cmd} source-path)" -type f -name "encrypted_*" -exec rm -fv {} +
    fi

    # Add to PATH for installing the necessary binary files under `$HOME/.local/bin`.
    export PATH="${PATH}:${HOME}/.local/bin"

    # run `chezmoi apply` to ensure that target... are in the target state,
    # updating them if necessary.
    "${chezmoi_cmd}" apply ${no_tty_option}

    # purge the binary of the chezmoi cmd
    rm -fv "${chezmoi_cmd}"
}

function initialize_dotfiles() {

    if ! is_ci_or_not_tty; then
        # - /dev/tty of the github workflow is not available.
        # - We can use password-less sudo in the github workflow.
        # Therefore, skip the sudo keep alive function.
        keepalive_sudo
    fi
    run_chezmoi
}

function get_system_from_chezmoi() {
    local system
    system=$(chezmoi data | jq -r '.system')
    echo "${system}"
}

function restart_shell_system() {
    local system
    system=$(get_system_from_chezmoi)

    # exec shell as login shell (to reload the .zprofile or .profile)
    if [ "${system}" == "client" ]; then
        /bin/zsh --login

    elif [ "${system}" == "server" ]; then
        /bin/bash --login

    else
        echo "Invalid system: ${system}; expected \`client\` or \`server\`" >&2
        exit 1
    fi
}

function restart_shell() {

    # Restart shell if specified "bash -c $(curl -L {URL})"
    # not restart:
    #   curl -L {URL} | bash
    if [ -p /dev/stdin ]; then
        echo "Now continue with Rebooting your shell"
    else
        echo "Restarting your shell..."
        restart_shell_system
    fi
}

function main() {
    echo "${DOTFILES_LOGO}"

    initialize_os_env
    initialize_dotfiles

    # restart_shell # Disabled because the at_exit function does not work properly.
}

main
