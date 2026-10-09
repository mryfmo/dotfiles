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

#
# @description Print the first page of a repository's releases as the GitHub API returns them.
#   GITHUB_TOKEN, GH_TOKEN or `gh auth token` authenticate the request when one is available.
# @arg $1 string owner/repo
#
function github_release_list() {
    local url="https://api.github.com/repos/$1/releases?per_page=30"
    local bearer="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
    if [ -z "${bearer}" ] && command -v gh > /dev/null 2>&1; then
        bearer="$(gh auth token 2> /dev/null)" || bearer=""
    fi
    if command -v curl > /dev/null 2>&1; then
        if [ -n "${bearer}" ]; then
            # The credential goes through curl's config on stdin, never the command line.
            printf 'header = "Authorization: Bearer %s"\n' "${bearer}" |
                curl -fsSL -K - -H 'Accept: application/vnd.github+json' "${url}"
        else
            curl -fsSL -H 'Accept: application/vnd.github+json' "${url}"
        fi
    else
        wget -qO - --header='Accept: application/vnd.github+json' "${url}"
    fi
}

#
# @description Print the tag of the newest release of a GitHub repository that is neither
#   a draft nor a prerelease and was published at least GITHUB_RELEASE_MIN_AGE_HOURS ago.
# @arg $1 string owner/repo
# @stdout The release tag.
# @exitcode 1 When the release list cannot be fetched or no release qualifies.
#
function github_release_tag() {
    local cutoff
    cutoff=$(($(date -u +%s) - GITHUB_RELEASE_MIN_AGE_HOURS * 3600))
    cutoff="$(date -u -d "@${cutoff}" +%Y-%m-%dT%H:%M:%SZ 2> /dev/null ||
        date -u -r "${cutoff}" +%Y-%m-%dT%H:%M:%SZ)" || return 1
    # The API pretty-prints each release's own fields at four spaces; nested objects sit deeper.
    github_release_list "$1" | awk -v cutoff="${cutoff}" '
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
    '
}

#
# @description Succeed when an authenticated gh can verify GitHub release attestations.
#
function github_attestation_ready() {
    command -v gh > /dev/null 2>&1 && gh auth status > /dev/null 2>&1
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
    gh release verify-asset "$2" "$3" --repo "$1" || return 1
}
