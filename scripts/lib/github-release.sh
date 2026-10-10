#!/usr/bin/env bash
# shellcheck shell=bash

# @file scripts/lib/github-release.sh
# @brief Resolve the newest GitHub release that has cooled down.
# @description
#   Sourced by the installers that take a GitHub release, scripts/upgrade-tools.sh and `make docker`.
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
        local status=0 wgetrc
        wgetrc="$(mktemp "${TMPDIR:-/tmp}/github-release.XXXXXX")" || return 1
        printf 'header = Authorization: Bearer %s\n' "${bearer}" > "${wgetrc}" &&
            wget --config="${wgetrc}" -qO - --header='Accept: application/vnd.github+json' "${url}" || status=$?
        rm -f "${wgetrc}"
        return "${status}"
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
#   github.com, can verify GitHub release attestations.
#
function github_attestation_ready() {
    local version
    command -v gh > /dev/null 2>&1 || return 1
    version="$(gh --version 2> /dev/null | awk 'NR == 1 { print $3 }')"
    if ! printf '%s\n%s\n' "${GITHUB_ATTESTATION_MIN_GH}" "${version}" | awk -F. '
        NR == 1 { split($0, minimum, ".") }
        NR == 2 {
            for (i = 1; i <= 3; i++) {
                if ($i + 0 > minimum[i] + 0) exit 0
                if ($i + 0 < minimum[i] + 0) exit 1
            }
            exit 0
        }'; then
        printf 'gh %s predates %s (GHSA-8xvp-7hj6-mcj9), so it is not used for attestations.\n' \
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
    github_attestation_ready || return 2
    gh release verify-asset "$2" "$3" --repo "github.com/$1" || return 1
}

#
# @description Keep a bootstrap asset whose GitHub release attestation cannot be checked yet, so
#   scripts/upgrade-tools.sh checks it at the first `make update` with an authenticated gh.
# @arg $1 string The tool; the record is pending-attestation/<tool> under the dotfiles state directory.
# @arg $2 string owner/repo
# @arg $3 string The release tag.
# @arg $4 path The asset, already verified by the mechanism in $5.
# @arg $5 string What verified the asset.
# @exitcode 1 When the record cannot be written, so the asset is never left unchecked silently.
#
function github_release_defer_attestation() {
    local record="${XDG_STATE_HOME:-${HOME}/.local/state}/dotfiles/pending-attestation/${1:?}"
    rm -rf "${record}" && mkdir -p "${record}" && cp "$4" "${record}/" || return 1
    printf '%s %s %s\n' "$2" "$3" "${4##*/}" > "${record}/release" || return 1
    printf '%s %s: attestation deferred: verified by %s only until gh is authenticated.\n' "$1" "$3" "$5"
}
