#!/usr/bin/env bash
# shellcheck shell=bash

# @file scripts/lib/github-release.sh
# @brief Resolve the newest GitHub release that has cooled down.
# @description
#   Sourced by the installers that take a GitHub release and by `make docker`.
#   setup.sh runs before the repository exists, so it carries a copy of the
#   functions below; tests/unit/test_github_release.py keeps the copies equal.
#   Only curl or wget and awk are needed, so a fresh machine can run it.

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
# @description Succeed when GITHUB_SERVER_URL or GH_HOST names a GitHub host other than github.com,
#   as in a GitHub Enterprise Server job: the environment's GITHUB_TOKEN and GH_TOKEN then belong
#   to that host and must never reach github.com.
#
function github_enterprise_context() {
    [ "${GITHUB_SERVER_URL:-https://github.com}" != https://github.com ] || [ "${GH_HOST:-github.com}" != github.com ]
}

#
# @description Run gh for github.com, without an Enterprise host's environment tokens.
# @arg $@ string gh's arguments.
#
function github_dotcom_gh() {
    if github_enterprise_context; then
        env -u GITHUB_TOKEN -u GH_TOKEN gh "$@"
    else
        gh "$@"
    fi
}

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
    local url="https://api.github.com/repos/$1/releases?per_page=30" bearer=""
    # An environment token counts only off an Enterprise host; there it belongs to that host.
    github_enterprise_context || bearer="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
    if [ -z "${bearer}" ] && command -v gh > /dev/null 2>&1; then
        # github.com only: GH_HOST or an Enterprise default host must not send its credential here.
        bearer="$(github_dotcom_gh auth token --hostname github.com 2> /dev/null)" || bearer=""
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
    version="$(github_dotcom_gh --version 2> /dev/null | awk 'NR == 1 { print $3 }')"
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
    github_dotcom_gh auth status --hostname github.com > /dev/null 2>&1
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
    github_dotcom_gh release verify-asset "$2" "$3" --repo "github.com/$1" 1>&2 || return 1
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
