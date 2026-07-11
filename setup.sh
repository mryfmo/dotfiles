#!/usr/bin/env bash

# @file setup.sh
# @brief Bootstrap the public dotfiles on supported macOS and Ubuntu systems.

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

declare -r DOTFILES_REPO_URL="${DOTFILES_REPO_URL:-https://github.com/mryfmo/dotfiles}"
declare -r BRANCH_NAME="${BRANCH_NAME:-main}"
declare -r HOMEBREW_INSTALL_COMMIT="c7952e40b7957268f61643152f4db725379b292e"
declare -r HOMEBREW_INSTALL_SHA256="99287f194a8b3c9e6b0203a11a5fa54518be57209343e6bb954dec4635796d9d"
declare -r CHEZMOI_VERSION="2.70.4"

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

# @description Download one URL to standard output, preferring curl over wget.
# @arg $1 url URL to download.
function fetch_url() {
    local url="$1"

    if command -v curl > /dev/null 2>&1; then
        curl -fsLS "${url}"
    elif command -v wget > /dev/null 2>&1; then
        wget -qO - "${url}"
    else
        echo "Neither curl nor wget is available; cannot download ${url}." >&2
        return 1
    fi
}

# @description Download one URL to a file, preferring curl over wget.
# @arg $1 url URL to download.
# @arg $2 output Destination file.
function fetch_file() {
    local url="$1" output="$2"
    if command -v curl > /dev/null 2>&1; then
        curl -fsLS "${url}" -o "${output}"
    elif command -v wget > /dev/null 2>&1; then
        wget -qO "${output}" "${url}"
    else
        printf 'Neither curl nor wget is available; cannot download %s.\n' "${url}" >&2
        return 1
    fi
}

# @description Print the SHA-256 digest of a file.
# @arg $1 path File to hash.
function sha256_file() {
    if command -v sha256sum > /dev/null 2>&1; then
        sha256sum "$1" | awk '{ print $1 }'
    else
        shasum -a 256 "$1" | awk '{ print $1 }'
    fi
}

# @description Verify a file against an expected SHA-256 digest.
# @arg $1 path File to verify.
# @arg $2 expected Expected lowercase digest.
function verify_sha256() {
    local path="$1" expected="${2:-}"
    [ -n "${expected}" ] || {
        printf 'Missing checksum for %s\n' "${path}" >&2
        return 1
    }
    [ "$(sha256_file "${path}")" = "${expected}" ] || {
        printf 'Checksum mismatch for %s\n' "${path}" >&2
        return 1
    }
}

# @description Verify an artifact against its entry in an upstream manifest.
# @arg $1 artifact Artifact path.
# @arg $2 manifest Checksum manifest path.
# @arg $3 name Artifact filename in the manifest.
function verify_checksum_manifest() {
    local artifact="$1" manifest="$2" name="$3" expected
    expected="$(awk -v name="${name}" '$2 == name { print $1 }' "${manifest}")"
    verify_sha256 "${artifact}" "${expected}"
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

    if [ "${DOTFILES_SUDO_KEEPALIVE_STARTED:-}" ]; then
        return
    fi

    ostype="$(get_os_type)"

    if [ "${ostype}" == "Darwin" ]; then
        keepalive_sudo_macos
    elif [ "${ostype}" == "Linux" ]; then
        keepalive_sudo_linux
    else
        echo "Invalid OS type: ${ostype}" >&2
        exit 1
    fi

    DOTFILES_SUDO_KEEPALIVE_STARTED=1
}

function initialize_os_macos() {
    local brew_prefix
    local installer
    local installer_sha256

    function is_homebrew_exists() {
        command -v brew &> /dev/null
    }

    function get_homebrew_prefix() {
        local prefix

        if is_homebrew_exists; then
            brew --prefix
            return
        fi

        for prefix in ${HOMEBREW_PREFIX_CANDIDATES:-/opt/homebrew /usr/local}; do
            if [[ -x "${prefix}/bin/brew" ]]; then
                printf '%s\n' "${prefix}"
                return
            fi
        done

        return 1
    }

    # Install Homebrew without letting its interactive prompts consume the outer
    # bootstrap session. The installer still prints its upstream "Next steps"
    # block, so explicitly continue by loading brew from the installation prefix.
    if ! is_homebrew_exists; then
        if ! is_ci_or_not_tty; then
            keepalive_sudo
        fi

        installer="$(mktemp)"
        at_exit "rm -f '${installer}'"
        fetch_file "https://raw.githubusercontent.com/Homebrew/install/${HOMEBREW_INSTALL_COMMIT}/install.sh" "${installer}"
        installer_sha256="$(sha256_file "${installer}")"
        [ "${installer_sha256}" = "${HOMEBREW_INSTALL_SHA256}" ] || {
            printf 'Homebrew installer checksum mismatch\n' >&2
            return 1
        }
        NONINTERACTIVE=1 /bin/bash "${installer}"
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
    local archive
    local artifact
    local base_url="https://github.com/twpayne/chezmoi/releases/download/v${CHEZMOI_VERSION}"
    local chezmoi_cmd
    local checksums
    local local_drift=false
    local no_tty_option
    local stage
    local status_line
    local status_output
    local tmpdir
    export PATH="${PATH}:${bin_dir}"

    case "$(get_os_type)/$(uname -m)" in
    Darwin/x86_64) artifact="chezmoi_${CHEZMOI_VERSION}_darwin_amd64.tar.gz" ;;
    Darwin/arm64) artifact="chezmoi_${CHEZMOI_VERSION}_darwin_arm64.tar.gz" ;;
    Linux/x86_64) artifact="chezmoi_${CHEZMOI_VERSION}_linux_amd64.tar.gz" ;;
    Linux/aarch64 | Linux/arm64) artifact="chezmoi_${CHEZMOI_VERSION}_linux_arm64.tar.gz" ;;
    *)
        printf 'Unsupported chezmoi platform: %s/%s\n' "$(get_os_type)" "$(uname -m)" >&2
        return 1
        ;;
    esac
    tmpdir="$(mktemp -d)"
    at_exit "rm -rf '${tmpdir}'"
    archive="${tmpdir}/${artifact}"
    checksums="${tmpdir}/chezmoi_${CHEZMOI_VERSION}_checksums.txt"
    fetch_file "${base_url}/${artifact}" "${archive}"
    fetch_file "${base_url}/chezmoi_${CHEZMOI_VERSION}_checksums.txt" "${checksums}"
    verify_checksum_manifest "${archive}" "${checksums}" "${artifact}"
    tar -xzf "${archive}" -C "${tmpdir}" chezmoi
    mkdir -p "${bin_dir}"
    stage="$(mktemp "${bin_dir}/chezmoi.tmp.XXXXXX")"
    at_exit "rm -f '${stage}'"
    install -m 0755 "${tmpdir}/chezmoi" "${stage}"
    mv -f "${stage}" "${bin_dir}/chezmoi"
    chezmoi_cmd="${bin_dir}/chezmoi"

    if is_ci_or_not_tty; then
        no_tty_option="--no-tty" # /dev/tty is not available (especially in the CI)
    else
        no_tty_option="" # /dev/tty is available OR not in the CI
    fi
    # run `chezmoi init` to setup the source directory,
    # generate the config file, and optionally update the destination directory
    # to match the target state.
    "${chezmoi_cmd}" init "${DOTFILES_REPO_URL}" \
        --branch "${BRANCH_NAME}" \
        --use-builtin-git true \
        ${no_tty_option}

    # Pull the latest source before applying so repeating the README snippet in
    # the same terminal picks up fixes merged after a previous failed run.
    "${chezmoi_cmd}" update \
        --apply=false \
        --init \
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

    if ! status_output="$("${chezmoi_cmd}" status --path-style absolute --exclude=scripts)"; then
        echo "chezmoi status failed; no destination targets were changed." >&2
        return 1
    fi

    while IFS= read -r status_line; do
        if [ -n "${status_line}" ] && [ "${status_line:0:1}" != " " ]; then
            local_drift=true
            break
        fi
    done <<< "${status_output}"

    if ! "${chezmoi_cmd}" diff; then
        echo "chezmoi diff failed; no destination targets were changed." >&2
        return 1
    fi

    if "${local_drift}"; then
        echo "Local changes detected; no destination targets were changed. Resolve them and rerun setup." >&2
        return 1
    fi

    if is_ci && { [ -z "${RUNNER_TEMP:-}" ] || [[ "${HOME}/" != "${RUNNER_TEMP%/}/"* ]]; }; then
        echo "Refusing to apply in CI outside RUNNER_TEMP: ${HOME}" >&2
        return 1
    fi

    if ! "${chezmoi_cmd}" apply ${no_tty_option}; then
        echo "chezmoi apply failed; completed target operations may remain." >&2
        return 1
    fi

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

# @description Restart an interactive shell, or defer when setup input is piped.
function restart_shell() {
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

if [[ -z "${BASH_SOURCE[0]:-}" || "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
