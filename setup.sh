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
readonly CHEZMOI_RELEASE_REPO="twpayne/chezmoi"
# The reviewed chezmoi a host without an authenticated gh bootstraps (its attestation cannot be
# checked before it runs), rendered from assets.chezmoi-bootstrap.fallback; change them there.
# Assignments stay non-readonly so tests can override them after sourcing.
CHEZMOI_FALLBACK_VERSION="v2.73.0"
CHEZMOI_FALLBACK_DARWIN_AMD64_SHA256="55e7b0823b40966a239cb418b37201c5f0961bab1b797c933550c97b1ab08221"
CHEZMOI_FALLBACK_DARWIN_ARM64_SHA256="246679a0b200e7e8be4a951be3b95d37c33ecb87eaab5af6f4949f7d0317bcc1"
CHEZMOI_FALLBACK_LINUX_AMD64_SHA256="b597729b687af4488a848240134cb633de8ca0f04e0d26d48f400ee2ac338ffa"
CHEZMOI_FALLBACK_LINUX_ARM64_SHA256="abcb840401d3c1f2356e0f53f5d52aa10d10f572654d9626db9ad0ca4dc03355"

# Copied from scripts/lib/github-release.sh, because setup.sh runs before the repository
# exists; tests/unit/test_github_release.py keeps the copy equal to the original.
# --- github-release.sh begin ---
# Releases younger than this stay out: the same 72 hours as minimum_release_age
# in home/dot_mise/config.toml. Change both together.
GITHUB_RELEASE_MIN_AGE_HOURS=72
# gh releases before this forward credentials to TUF mirror hosts during attestation checks
# (GHSA-8xvp-7hj6-mcj9), so an older gh is not used for them.
GITHUB_ATTESTATION_MIN_GH="2.93.0"
# A release tag is a version: the only shape installers, setup.sh and `make docker` accept, so an
# API answer can never smuggle shell syntax or a path into a URL or a command line.
GITHUB_RELEASE_TAG_PATTERN='^v?[0-9]+(\.[0-9]+)*([-.+][0-9A-Za-z.-]+)?$'

#
# @description Print the first page of a repository's releases as the GitHub API returns them.
#   GITHUB_TOKEN, GH_TOKEN or gh's github.com token authenticate the request when one is available.
#   An xtrace the caller turned on (DOTFILES_DEBUG) is off while the credential is handled, and
#   restored afterwards on every path, so a trace never shows it.
# @arg $1 string owner/repo
#
function github_release_list() {
    local status=0 xtrace=""
    case $- in *x*)
        xtrace=1
        set +x
        ;;
    esac
    github_release_fetch "$1" || status=$?
    [ -z "${xtrace}" ] || set -x
    return "${status}"
}

#
# @description The request behind github_release_list; call github_release_list, which keeps it out of a trace.
# @arg $1 string owner/repo
#
function github_release_fetch() {
    local url="https://api.github.com/repos/$1/releases?per_page=30"
    local bearer="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
    if [ -z "${bearer}" ] && command -v gh > /dev/null 2>&1; then
        # github.com only: GH_HOST or an Enterprise default host must not send its credential here.
        bearer="$(gh auth token --hostname github.com 2> /dev/null)" || bearer=""
    fi
    if command -v curl > /dev/null 2>&1; then
        if [ -n "${bearer}" ]; then
            # The credential goes through curl's config on stdin, never the command line.
            printf 'header = "Authorization: Bearer %s"\n' "${bearer}" |
                curl -fsSL -K - -H 'Accept: application/vnd.github+json' "${url}"
        else
            curl -fsSL -H 'Accept: application/vnd.github+json' "${url}"
        fi
    elif [ -n "${bearer}" ]; then
        # wget reads the credential from a private wgetrc (mktemp creates it 0600), never the command line.
        # A subshell whose EXIT trap removes it, with signals turned into exits, so an interruption
        # cannot strand the credential.
        (
            wgetrc="$(mktemp "${TMPDIR:-/tmp}/github-release.XXXXXX")" || exit 1
            trap 'rm -f "${wgetrc}"' EXIT
            trap 'exit 1' HUP INT TERM
            printf 'header = Authorization: Bearer %s\n' "${bearer}" > "${wgetrc}" || exit 1
            wget --config="${wgetrc}" -qO - --header='Accept: application/vnd.github+json' "${url}"
        )
    else
        wget -qO - --header='Accept: application/vnd.github+json' "${url}"
    fi
}

#
# @description Print the tag of the newest release of a GitHub repository that is neither
#   a draft nor a prerelease and was published at least GITHUB_RELEASE_MIN_AGE_HOURS ago.
# @arg $1 string owner/repo
# @stdout The release tag.
# @exitcode 1 When the release list cannot be fetched, no release qualifies, or the tag is not
#   a version (GITHUB_RELEASE_TAG_PATTERN).
#
function github_release_tag() {
    local cutoff list tag
    cutoff=$(($(date -u +%s) - GITHUB_RELEASE_MIN_AGE_HOURS * 3600))
    cutoff="$(date -u -d "@${cutoff}" +%Y-%m-%dT%H:%M:%SZ 2> /dev/null ||
        date -u -r "${cutoff}" +%Y-%m-%dT%H:%M:%SZ)" || return 1
    # Fetched whole before parsing, so a failed or truncated download never yields a tag.
    list="$(github_release_list "$1")" || return 1
    # The API pretty-prints each release's own fields at four spaces; nested objects sit deeper.
    tag="$(printf '%s\n' "${list}" | awk -v cutoff="${cutoff}" '
        /^  \{/ { tag = ""; draft = ""; prerelease = ""; published = "" }
        /^    "tag_name": "/ { tag = $0; sub(/^    "tag_name": "/, "", tag); sub(/",?$/, "", tag) }
        /^    "draft": / { draft = ($0 ~ /: false,?$/) ? "no" : "yes" }
        /^    "prerelease": / { prerelease = ($0 ~ /: false,?$/) ? "no" : "yes" }
        /^    "published_at": "/ { published = $0; sub(/^    "published_at": "/, "", published); sub(/",?$/, "", published) }
        /^  \}/ {
            if (tag != "" && draft == "no" && prerelease == "no" && published != "" && published <= cutoff && published > newest) {
                newest = published
                chosen = tag
            }
        }
        END { if (chosen == "") exit 1; print chosen }
    ')" || return 1
    if ! [[ "${tag}" =~ ${GITHUB_RELEASE_TAG_PATTERN} ]]; then
        printf 'unexpected release tag %s for %s\n' "${tag}" "$1" >&2
        return 1
    fi
    printf '%s\n' "${tag}"
}

#
# @description Succeed when a gh at least GITHUB_ATTESTATION_MIN_GH, authenticated to
#   github.com, can verify GitHub release attestations. mise's gh shim comes first, so an
#   older system gh earlier on PATH (Ubuntu's apt gh predates 2.93.0) never hides it.
#
function github_attestation_ready() {
    local PATH="${HOME}/.local/share/mise/shims:${PATH}" version
    command -v gh > /dev/null 2>&1 || return 1
    version="$(gh --version 2> /dev/null | awk 'NR == 1 { print $3 }')"
    # Only a stable X.Y.Z counts: a prerelease such as 2.93.0-rc.1 sorts below the 2.93.0 fix.
    if ! [[ "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] ||
        ! printf '%s\n%s\n' "${GITHUB_ATTESTATION_MIN_GH}" "${version}" | awk -F. '
        NR == 1 { split($0, minimum, ".") }
        NR == 2 {
            for (i = 1; i <= 3; i++) {
                if ($i + 0 > minimum[i] + 0) exit 0
                if ($i + 0 < minimum[i] + 0) exit 1
            }
            exit 0
        }'; then
        printf 'gh %s is not a stable release at or after %s (GHSA-8xvp-7hj6-mcj9), so it is not used for attestations.\n' \
            "${version:-unknown}" "${GITHUB_ATTESTATION_MIN_GH}" >&2
        return 1
    fi
    gh auth status --hostname github.com > /dev/null 2>&1
}

#
# @description Verify a downloaded asset against its GitHub release attestation, which is
#   signed by GitHub for an immutable release and lists every asset's digest.
# @arg $1 string owner/repo
# @arg $2 string The release tag.
# @arg $3 path The downloaded asset.
# @exitcode 0 The attestation verified the asset.
# @exitcode 1 The attestation did not verify the asset.
# @exitcode 2 gh is absent or not authenticated, so nothing was verified.
#
function github_release_attestation() {
    # The same gh github_attestation_ready checked: mise's shim first.
    local PATH="${HOME}/.local/share/mise/shims:${PATH}"
    github_attestation_ready || return 2
    # gh prints its verification report on stdout; it goes to stderr so callers get only the status.
    gh release verify-asset "$2" "$3" --repo "github.com/$1" 1>&2 || return 1
}

#
# @description Download a release asset and its checksum file, check the checksum and the asset's
#   GitHub release attestation now (no deferral), and print the asset's sha256, so a build without
#   gh can check the asset against it (`make docker` passes it to the Dockerfile). Needs curl.
# @arg $1 string owner/repo
# @arg $2 string The release tag.
# @arg $3 string The asset name.
# @arg $4 string The name of the release's checksum file.
# @stdout The verified asset's sha256.
# @exitcode 1 A download, the checksum or the attestation failed.
# @exitcode 2 No gh 2.93.0 or newer is authenticated to github.com, so nothing was downloaded.
#
function github_release_verified_sha256() (
    local actual base="https://github.com/$1/releases/download/$2" dir expected
    github_attestation_ready || return 2
    dir="$(mktemp -d "${TMPDIR:-/tmp}/github-release.XXXXXX")" || return 1
    trap 'rm -rf "${dir}"' EXIT
    curl -fsSL "${base}/$3" -o "${dir}/$3" || return 1
    curl -fsSL "${base}/$4" -o "${dir}/$4" || return 1
    expected="$(awk -v name="$3" '$2 == name { print $1; exit }' "${dir}/$4")"
    if command -v sha256sum > /dev/null 2>&1; then
        actual="$(sha256sum "${dir}/$3" | awk '{ print $1 }')"
    else
        actual="$(shasum -a 256 "${dir}/$3" | awk '{ print $1 }')"
    fi
    if [ -z "${expected}" ] || [ "${actual}" != "${expected}" ]; then
        printf 'Checksum mismatch for %s\n' "$3" >&2
        return 1
    fi
    github_release_attestation "$1" "$2" "${dir}/$3" || return 1
    printf '%s\n' "${actual}"
)
# --- github-release.sh end ---

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
    local attestation=0
    local base_url
    local chezmoi_cmd
    local chezmoi_tag
    local chezmoi_version
    local checksums
    local fallback_sha256
    local fallback=""
    local local_drift=false
    local no_tty_option
    local stage
    local status_line
    local status_output
    local tmpdir
    export PATH="${PATH}:${bin_dir}"

    # Nothing runs before a check independent of the release page: the newest cooled-down release
    # only when gh can verify its attestation first, otherwise the reviewed fallback release.
    if github_attestation_ready; then
        chezmoi_tag="$(github_release_tag "${CHEZMOI_RELEASE_REPO}")" || {
            printf 'Could not resolve a %s release.\n' "${CHEZMOI_RELEASE_REPO}" >&2
            return 1
        }
    else
        fallback=1
        chezmoi_tag="${CHEZMOI_FALLBACK_VERSION}"
        printf 'No authenticated gh 2.93.0 or newer: installing the reviewed chezmoi %s (assets.chezmoi-bootstrap.fallback).\n' "${chezmoi_tag}"
    fi
    chezmoi_version="${chezmoi_tag#v}"
    base_url="https://github.com/${CHEZMOI_RELEASE_REPO}/releases/download/${chezmoi_tag}"
    case "$(get_os_type)/$(uname -m)" in
    Darwin/x86_64)
        artifact="chezmoi_${chezmoi_version}_darwin_amd64.tar.gz"
        fallback_sha256="${CHEZMOI_FALLBACK_DARWIN_AMD64_SHA256}"
        ;;
    Darwin/arm64)
        artifact="chezmoi_${chezmoi_version}_darwin_arm64.tar.gz"
        fallback_sha256="${CHEZMOI_FALLBACK_DARWIN_ARM64_SHA256}"
        ;;
    Linux/x86_64)
        artifact="chezmoi_${chezmoi_version}_linux_amd64.tar.gz"
        fallback_sha256="${CHEZMOI_FALLBACK_LINUX_AMD64_SHA256}"
        ;;
    Linux/aarch64 | Linux/arm64)
        artifact="chezmoi_${chezmoi_version}_linux_arm64.tar.gz"
        fallback_sha256="${CHEZMOI_FALLBACK_LINUX_ARM64_SHA256}"
        ;;
    *)
        printf 'Unsupported chezmoi platform: %s/%s\n' "$(get_os_type)" "$(uname -m)" >&2
        return 1
        ;;
    esac
    tmpdir="$(mktemp -d)"
    at_exit "rm -rf '${tmpdir}'"
    archive="${tmpdir}/${artifact}"
    checksums="${tmpdir}/chezmoi_${chezmoi_version}_checksums.txt"
    fetch_file "${base_url}/${artifact}" "${archive}"
    fetch_file "${base_url}/chezmoi_${chezmoi_version}_checksums.txt" "${checksums}"
    verify_checksum_manifest "${archive}" "${checksums}" "${artifact}"
    if [ -n "${fallback}" ]; then
        # The reviewed sha256 is the check; the release's checksum file above only re-checked the download.
        verify_sha256 "${archive}" "${fallback_sha256}"
    else
        github_release_attestation "${CHEZMOI_RELEASE_REPO}" "${chezmoi_tag}" "${archive}" || attestation=$?
        if [ "${attestation}" -ne 0 ]; then
            printf 'GitHub release attestation failed for %s; nothing was installed.\n' "${artifact}" >&2
            return 1
        fi
    fi
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
        --use-builtin-git auto \
        ${no_tty_option}

    # Pull the latest source before applying so repeating the README snippet in
    # the same terminal picks up fixes merged after a previous failed run.
    "${chezmoi_cmd}" update \
        --apply=false \
        --init \
        --use-builtin-git auto \
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

# @description Log in this machine's GitHub account when gh holds no working login (interactive runs only).
#   CI and non-terminal runs skip it; `make gh-auth` in the checkout repeats it later.
function authenticate_github() {
    local script="${HOME}/.local/share/chezmoi/scripts/gh-auth.sh"

    # On a fresh machine gh exists only as a mise shim, which this shell's PATH does not hold yet.
    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
    if is_ci_or_not_tty || ! command -v gh > /dev/null 2>&1 || [ ! -x "${script}" ]; then
        echo "Skipping the GitHub login; run \`make gh-auth\` in the dotfiles checkout once gh is installed."
        return 0
    fi
    if ! "${script}"; then
        echo "The GitHub login did not complete; run \`make gh-auth\` to retry." >&2
    fi
}

function main() {
    echo "${DOTFILES_LOGO}"

    initialize_os_env
    initialize_dotfiles
    authenticate_github
}

if [[ -z "${BASH_SOURCE[0]:-}" || "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
