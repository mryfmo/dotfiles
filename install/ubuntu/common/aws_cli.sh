#!/usr/bin/env bash

# @file install/ubuntu/common/aws_cli.sh
# @brief Install the pinned AWS CLI from its verified official Linux archive.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly AWS_CLI_VERSION="2.35.21"
readonly AWS_CLI_FINGERPRINT="FB5DB77FD5C118B80511ADA8A6310ACC4672475C"
readonly AWS_CLI_KEY_PATH="${AWS_CLI_KEY_PATH:-${HOME}/.local/share/aws-cli-keys/aws-cli-public-key.asc}"
readonly AWS_CLI_INSTALL_DIR="${HOME}/.local/share/aws-cli"
readonly AWS_CLI_BIN_DIR="${HOME}/.local/bin"

#
# @description Print the versioned AWS CLI archive URL for the current supported architecture.
# @stdout The official x86_64 or aarch64 archive URL.
#
function aws_cli_url() {
    local architecture

    architecture="$(uname -m)"
    case "${architecture}" in
    x86_64 | aarch64)
        printf 'https://awscli.amazonaws.com/awscli-exe-linux-%s-%s.zip\n' "${architecture}" "${AWS_CLI_VERSION}"
        ;;
    *)
        printf 'Unsupported AWS CLI architecture: %s\n' "${architecture}" >&2
        return 1
        ;;
    esac
}

#
# @description Verify that an executable reports the pinned AWS CLI version.
# @arg $1 executable AWS CLI executable path.
# @arg $2 error_prefix Error message prefix.
#
function verify_aws_cli_version() {
    local executable="$1"
    local error_prefix="$2"
    local version_output
    local version_token

    if [[ ! -x "${executable}" ]]; then
        printf '%s: %s is not executable.\n' "${error_prefix}" "${executable}" >&2
        return 1
    fi
    version_output="$("${executable}" --version)" || return
    read -r version_token _ <<< "${version_output}"
    if [[ "${version_token}" != "aws-cli/${AWS_CLI_VERSION}" ]]; then
        printf '%s: expected aws-cli/%s, got %s.\n' \
            "${error_prefix}" "${AWS_CLI_VERSION}" "${version_token}" >&2
        return 1
    fi
}

#
# @description Verify that the installer produced the pinned AWS CLI executable.
#
function verify_aws_cli_install() {
    verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI postcondition failed"
}

#
# @description Verify and install the pinned AWS CLI without modifying a working install on verification failure.
#
function install_aws_cli() (
    local archive_url
    local archive_path
    local signature_path
    local current_time
    local expiration
    local key_data
    local keyring_path
    local fingerprint
    local inspection_home
    local validity
    local temporary_dir

    archive_url="$(aws_cli_url)" || return
    temporary_dir="$(mktemp -d)" || return
    trap 'rm -rf "${temporary_dir}"' EXIT

    archive_path="${temporary_dir}/awscliv2.zip"
    signature_path="${archive_path}.sig"
    inspection_home="${temporary_dir}/gnupg-inspection"
    keyring_path="${temporary_dir}/aws-cli-keyring.gpg"

    curl --fail --location --silent --show-error "${archive_url}" --output "${archive_path}" || return
    curl --fail --location --silent --show-error "${archive_url}.sig" --output "${signature_path}" || return

    mkdir -m 700 "${inspection_home}" || return
    key_data="$(gpg --homedir "${inspection_home}" --batch --with-colons --import-options show-only --import "${AWS_CLI_KEY_PATH}")" || return
    fingerprint="$(awk -F: '$1 == "fpr" { print $10 }' <<< "${key_data}")"
    validity="$(awk -F: '$1 == "pub" { print $2 }' <<< "${key_data}")"
    expiration="$(awk -F: '$1 == "pub" { print $7 }' <<< "${key_data}")"
    current_time="$(date +%s)"
    if [[ "${fingerprint}" != "${AWS_CLI_FINGERPRINT}" || "${validity}" != "-" || ! "${expiration}" =~ ^[0-9]+$ ]] ||
        ((expiration <= current_time)); then
        printf 'AWS CLI signing key validation failed.\n' >&2
        return 1
    fi
    gpg --batch --yes --dearmor --output "${keyring_path}" "${AWS_CLI_KEY_PATH}" || return
    gpgv --keyring "${keyring_path}" "${signature_path}" "${archive_path}" || return

    unzip -q "${archive_path}" -d "${temporary_dir}" || return
    verify_aws_cli_version "${temporary_dir}/aws/dist/aws" "AWS CLI staged artifact verification failed" || return
    mkdir -p "${AWS_CLI_BIN_DIR}" "$(dirname "${AWS_CLI_INSTALL_DIR}")" || return
    "${temporary_dir}/aws/install" \
        --install-dir "${AWS_CLI_INSTALL_DIR}" \
        --bin-dir "${AWS_CLI_BIN_DIR}" \
        --update || return
    verify_aws_cli_install
)

#
# @description Install or update the pinned AWS CLI.
#
function main() {
    install_aws_cli
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
