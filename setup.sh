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
declare -r HOMEBREW_INSTALL_COMMIT="09c62fc577ec170172b0a184060f141a2c622dc1"
declare -r HOMEBREW_INSTALL_SHA256="5f333bbe53bc490e51e7ccb1df8779b3dd6ee73a1a7379efda216edb08ccb148"
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
    local PATH="${HOME}/.local/share/mise/shims:${PATH}" version version_output
    command -v gh > /dev/null 2>&1 || return 1
    if ! version_output="$(github_dotcom_gh --version 2> /dev/null)"; then
        printf 'gh --version failed, so gh is not used for attestations.\n' >&2
        return 1
    fi
    read -r _ _ version _ <<< "${version_output}"
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
    local actual base="https://github.com/$1/releases/download/$2" dir expected sum
    github_attestation_ready || return 2
    dir="$(mktemp -d "${TMPDIR:-/tmp}/github-release.XXXXXX")" || return 1
    trap 'rm -rf "${dir}"' EXIT
    curl -fsSL "${base}/$3" -o "${dir}/$3" || return 1
    curl -fsSL "${base}/$4" -o "${dir}/$4" || return 1
    expected="$(awk -v name="$3" '$2 == name { print $1; exit }' "${dir}/$4")"
    if command -v sha256sum > /dev/null 2>&1; then
        sum="$(sha256sum "${dir}/$3")" || {
            printf 'sha256sum could not hash %s\n' "$3" >&2
            return 1
        }
    else
        sum="$(shasum -a 256 "${dir}/$3")" || {
            printf 'shasum -a 256 could not hash %s\n' "$3" >&2
            return 1
        }
    fi
    actual="${sum%% *}"
    if [ -z "${expected}" ] || [ "${actual}" != "${expected}" ]; then
        printf 'Checksum mismatch for %s\n' "$3" >&2
        return 1
    fi
    github_release_attestation "$1" "$2" "${dir}/$3" || return 1
    printf '%s\n' "${actual}"
)
# --- github-release.sh end ---

# --- ci-runner.sh begin ---
#
# @description Succeed on a GitHub Actions runner, whatever `CI` holds.
# @exitcode 0 `GITHUB_ACTIONS` is `true` and `RUNNER_TEMP` is set.
# @exitcode 1 Anywhere else, an agent shell exporting `CI=true` included.
#
function is_ci_runner() {
    [ "${GITHUB_ACTIONS:-}" = true ] && [ -n "${RUNNER_TEMP:-}" ]
}
# --- ci-runner.sh end ---

# Copied from scripts/lib/chezmoi-externals.sh, because setup.sh runs before the repository
# exists; tests/unit/test_chezmoi_externals.py keeps the copy equal to the original.
# --- chezmoi-externals.sh begin ---
# The sha256 of no bytes: a cache key equal to it hashed nothing, whatever the URL was.
CHEZMOI_EXTERNAL_EMPTY_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
# Download attempts per URL, and the first wait between them in seconds (doubled after each failure): constants,
# never read from the environment, so no caller can unbound the retries. Tests replace `sleep` instead.
CHEZMOI_EXTERNAL_ATTEMPTS=4
CHEZMOI_EXTERNAL_RETRY_DELAY=5

#
# @description Print the lowercase sha256 of one file. It never reads standard input, so no caller hashes through a
#   pipeline whose first stage's status depends on the caller's `pipefail` (U96 round 5: `make update` runs without it).
# @arg $1 path The file to hash.
# @stdout The digest.
# @exitcode 1 When no file is named, or the hash tool fails or prints no 64-digit lowercase hex digest.
#
function chezmoi_external_sha256() {
    local digest
    if ! { [ "$#" -eq 1 ] && [ -f "$1" ]; }; then
        return 1
    fi
    if command -v sha256sum > /dev/null 2>&1; then
        digest="$(sha256sum "$1")" || return 1
    else
        digest="$(shasum -a 256 "$1")" || return 1
    fi
    digest="${digest%% *}"
    [[ "${digest}" =~ ^[0-9a-f]{64}$ ]] || return 1
    printf '%s\n' "${digest}"
}

#
# @description Print chezmoi's cache key for a URL: the sha256 of its bytes as written (chezmoi 2.73.3
#   internal/chezmoi/sourcestate.go:1921-1922). The URL is written to a scratch file, each step's status checked, and
#   that file is hashed: no pipeline, so the result does not depend on the caller's shell options.
# @arg $1 url The URL; empty is refused.
# @stdout The key.
# @exitcode 1 When the URL is empty, the scratch file cannot be made or written, the hash fails, or the key is the
#   sha256 of no bytes.
#
function chezmoi_external_url_key() {
    local url="$1" scratch key status=0
    [ -n "${url}" ] || return 1
    scratch="$(mktemp "${TMPDIR:-/tmp}/chezmoi-external-url.XXXXXX")" || return 1
    printf '%s' "${url}" > "${scratch}" || status=1
    [ "${status}" -ne 0 ] || key="$(chezmoi_external_sha256 "${scratch}")" || status=1
    rm -f "${scratch}"
    if ! { [ "${status}" -eq 0 ] && [ "${key}" != "${CHEZMOI_EXTERNAL_EMPTY_SHA256}" ]; }; then
        return 1
    fi
    printf '%s\n' "${key}"
}

#
# @description Print a Go duration (chezmoi's refreshPeriod, time.ParseDuration) in whole seconds: an empty value
#   or `0` is 0, which chezmoi reads as "never re-download"; a sum of integer h, m and s parts is accepted.
# @arg $1 string The duration.
# @stdout Seconds.
# @exitcode 1 When the value has another form (a fraction, ms, us, ns): this step cannot tell chezmoi's freshness.
#
function chezmoi_external_seconds() {
    local rest="$1" total=0 amount unit
    if ! { [ -n "${rest}" ] && [ "${rest}" != 0 ]; }; then
        printf '0\n'
        return 0
    fi
    while [ -n "${rest}" ]; do
        [[ "${rest}" =~ ^([0-9]{1,9})([hms])(.*)$ ]] || return 1
        amount="${BASH_REMATCH[1]}" unit="${BASH_REMATCH[2]}" rest="${BASH_REMATCH[3]}"
        case "${unit}" in
        h) total=$((total + 10#${amount} * 3600)) ;;
        m) total=$((total + 10#${amount} * 60)) ;;
        s) total=$((total + 10#${amount})) ;;
        esac
    done
    printf '%s\n' "${total}"
}

#
# @description Download one URL into a file once, bounded in time and speed.
# @arg $1 url The URL.
# @arg $2 path The output file.
# @stdout The HTTP status curl saw.
# @exitcode 0 A complete 2xx response was written.
# @exitcode * curl's exit status (22 for an HTTP error, 18 for a truncated transfer).
#
function chezmoi_external_download() {
    curl --proto '=http,https' --location --fail --silent --show-error \
        --connect-timeout 30 --max-time 900 --speed-limit 1024 --speed-time 60 \
        --output "$2" --write-out '%{http_code}' "$1"
}

#
# @description Put one external's verified download into chezmoi's cache, retrying a failed transfer. A cache
#   entry already younger than the refresh period and holding the right bytes is kept; one with other bytes (chezmoi
#   caches a download before it checks the checksum) is replaced.
# @arg $1 string The external's target path, for messages.
# @arg $2 url The URL.
# @arg $3 string The expected sha256.
# @arg $4 number The refresh period in seconds (0: never re-download).
# @arg $5 path chezmoi's cache directory.
# @stderr What failed, naming the external and its URL.
# @exitcode 1 The download failed, or a local producer did (hash, date, temporary file, cache directory, install):
#   nothing cached.
# @exitcode 2 The sha256 of a complete download differed: not retried, nothing cached.
#
function prefetch_chezmoi_external() {
    local name="$1" url="$2" expected="$3" refresh="$4" cache="$5"
    local key entry modified now partial actual code status retry attempt=1 delay="${CHEZMOI_EXTERNAL_RETRY_DELAY}"
    key="$(chezmoi_external_url_key "${url}")" || {
        printf 'chezmoi external %s: cannot hash the URL %s for its cache key\n' "${name}" "${url}" >&2
        return 1
    }
    entry="${cache}/external/${key}"
    if [ -f "${entry}" ]; then
        # An entry this step cannot read the age or the digest of is fetched again, never kept.
        modified="$(stat -c %Y "${entry}" 2> /dev/null || stat -f %m "${entry}")" || modified=0
        [[ "${modified}" =~ ^[0-9]+$ ]] || modified=0
        if ! { now="$(date +%s)" && [[ "${now}" =~ ^[0-9]+$ ]]; }; then
            printf 'chezmoi external %s: date +%%s failed; cannot tell the cache entry'\''s age\n' "${name}" >&2
            return 1
        fi
        actual="$(chezmoi_external_sha256 "${entry}")" || actual=""
        if [ "${actual}" = "${expected}" ] && { [ "${refresh}" -eq 0 ] || [ $((modified + refresh)) -gt "${now}" ]; }; then
            printf 'chezmoi external %s: cached, sha256 verified\n' "${name}"
            return 0
        fi
    fi
    mkdir -p "${cache}/external" || {
        printf 'chezmoi external %s: mkdir -p %s/external failed; nothing cached\n' "${name}" "${cache}" >&2
        return 1
    }
    chmod 700 "${cache}" "${cache}/external" || {
        printf 'chezmoi external %s: chmod 700 on %s and %s/external failed; nothing cached\n' "${name}" "${cache}" "${cache}" >&2
        return 1
    }
    partial="$(mktemp "${cache}/external/.prefetch.XXXXXX")" || {
        printf 'chezmoi external %s: cannot create a download file in %s/external\n' "${name}" "${cache}" >&2
        return 1
    }
    while :; do
        status=0
        code="$(chezmoi_external_download "${url}" "${partial}")" || status=$?
        if [ "${status}" -eq 0 ]; then
            actual="$(chezmoi_external_sha256 "${partial}")" || {
                rm -f "${partial}"
                printf 'chezmoi external %s: %s: cannot hash the download; nothing cached\n' "${name}" "${url}" >&2
                return 1
            }
            if [ "${actual}" != "${expected}" ]; then
                rm -f "${partial}"
                printf 'chezmoi external %s: %s: SHA256 mismatch after a complete download: expected %s, got %s; not retried, nothing cached\n' \
                    "${name}" "${url}" "${expected}" "${actual}" >&2
                return 2
            fi
            chmod 600 "${partial}" || {
                rm -f "${partial}"
                printf 'chezmoi external %s: chmod 600 on the download failed; nothing cached\n' "${name}" >&2
                return 1
            }
            mv -f "${partial}" "${entry}" || {
                rm -f "${partial}"
                printf 'chezmoi external %s: mv of the download into %s failed; nothing cached\n' "${name}" "${entry}" >&2
                return 1
            }
            printf 'chezmoi external %s: downloaded from %s, sha256 verified\n' "${name}" "${url}"
            return 0
        fi
        # Retried only from an allowlist of transient remote or network faults (curl(1), "Exit codes"): 6 could not
        # resolve host, 7 failed to connect, 18 partial file, 28 operation timeout, 35 SSL connect error, 52 the
        # server did not reply anything, 55 failed sending network data, 56 failure in receiving network data, 92
        # stream error in the HTTP/2 framing layer (a server or proxy resetting an HTTP/2 stream mid-transfer); and,
        # through --fail's 22, HTTP 408, 429 and 5xx. Every other code, a local one such as 23 (write error) or 27
        # (out of memory) included, fails at once.
        retry=0
        case "${status}/${code}" in # lint-comparisons: allow curl's exit status and HTTP code, not a path
        6/* | 7/* | 18/* | 28/* | 35/* | 52/* | 55/* | 56/* | 92/* | 22/408 | 22/429 | 22/5[0-9][0-9]) retry=1 ;;
        esac
        if [ "${retry}" -eq 0 ] || [ "${attempt}" -ge "${CHEZMOI_EXTERNAL_ATTEMPTS}" ]; then
            rm -f "${partial}"
            printf 'chezmoi external %s: %s: download failed after %s attempt(s) (last: curl exit %s, HTTP %s); nothing cached\n' \
                "${name}" "${url}" "${attempt}" "${status}" "${code:-none}" >&2
            return 1
        fi
        printf 'chezmoi external %s: %s: attempt %s failed (curl exit %s, HTTP %s); retrying in %ss\n' \
            "${name}" "${url}" "${attempt}" "${status}" "${code:-none}" "${delay}" >&2
        sleep "${delay}"
        attempt=$((attempt + 1))
        delay=$((delay * 2))
    done
}

#
# @description Whether a source root holds a `.chezmoiexternal.*` file or a `.chezmoiexternals` directory, read with
#   builtins only: the check that an empty discovery is a finding, never a find that saw nothing (U96 round 9).
# @arg $1 path The physical source directory.
# @exitcode 0 It holds one (a symlink, even a dangling one, counts).
# @exitcode 1 It holds none.
#
function chezmoi_external_root_declares() {
    local candidate
    if [ -d "$1/.chezmoiexternals" ] || [ -L "$1/.chezmoiexternals" ]; then
        return 0
    fi
    for candidate in "$1"/.chezmoiexternal.*; do
        if [ -e "${candidate}" ] || [ -L "${candidate}" ]; then
            return 0
        fi
    done
    return 1
}

#
# @description Print every external a chezmoi source declares, one per line, tab-separated: target path, type,
#   sha256, refresh period, the number of fallback `urls`, and `url`. A missing type, sha256 or url prints as `-` and
#   a missing refresh period as `0`, so no field is empty (a tab is whitespace to `read`, which would merge two tabs
#   into one separator). Every `.chezmoiexternal.<format>` file anywhere in the source and every file
#   in a `.chezmoiexternals/` directory is rendered by chezmoi itself (`execute-template`, with the source's
#   templates) and decoded by its own fromYaml, fromJson, fromJsonc or fromToml. Every producer's status is
#   checked: a failed find, render or decode is an error that names the file, never an empty list.
# @arg $1 path The chezmoi command.
# @arg $2 path The source directory (`chezmoi source-path`), resolved to its physical path: find does not descend into
#   a symlinked start directory, and chezmoi keeps a symlinked source path as given.
# @arg $3 path A scratch directory for the rendered files.
# @stdout The externals.
# @exitcode 1 When a declaration file cannot be found, rendered or decoded, or has an unknown format, or when find
#   lists none while the root holds one.
#
function chezmoi_external_list() {
    local chezmoi="$1" source="$2" scratch="$3" declarations declaration format decode relative prefix rendered count=0
    local fields
    # Go template text, not shell: every $ belongs to chezmoi. A missing type or sha256 is `-`, a missing period `0`.
    # shellcheck disable=SC2016
    fields='{{ $name }}{{ "\t" }}{{ dig "type" "-" $e }}{{ "\t" }}{{ dig "checksum" "sha256" "-" $e }}{{ "\t" }}{{ dig "refreshPeriod" "0" $e }}{{ "\t" }}{{ len (dig "urls" list $e) }}{{ "\t" }}{{ dig "url" "-" $e }}'
    declarations="$(find "${source}" \( -type f -name '.chezmoiexternal.*' \) -o \( -type f -path '*/.chezmoiexternals/*' \))" || {
        printf 'chezmoi externals: cannot list the declarations under %s\n' "${source}" >&2
        return 1
    }
    # No declaration is a decision, not a default: a root that holds one while find listed none (a symlinked
    # declaration file, a find that saw nothing) stops the step instead of skipping every external.
    if [ -z "${declarations}" ] && chezmoi_external_root_declares "${source}"; then
        printf 'chezmoi externals: %s holds a .chezmoiexternal file or a .chezmoiexternals directory, but find listed no declaration\n' "${source}" >&2
        return 1
    fi
    while IFS= read -r declaration; do
        [ -n "${declaration}" ] || continue
        format="${declaration%.tmpl}"
        format="${format##*.}"
        case "${format}" in
        yaml | yml) decode=fromYaml ;;
        json) decode=fromJson ;;
        jsonc) decode=fromJsonc ;;
        toml) decode=fromToml ;;
        *)
            printf 'chezmoi externals: %s has a format this step does not read\n' "${declaration}" >&2
            return 1
            ;;
        esac
        relative="${declaration#"${source}"/}"
        prefix="${relative%/*}"
        [ "${prefix}" != "${relative}" ] || prefix=""
        prefix="${prefix%/.chezmoiexternals}"
        prefix="${prefix%.chezmoiexternals}"
        count=$((count + 1))
        rendered="${scratch}/${count}.${format}"
        "${chezmoi}" execute-template < "${declaration}" > "${rendered}" || {
            printf 'chezmoi externals: cannot render %s\n' "${declaration}" >&2
            return 1
        }
        "${chezmoi}" execute-template "{{- range \$name, \$e := (include \"${rendered}\" | ${decode}) -}}
${prefix:+${prefix}/}${fields}
{{ end -}}" || {
            printf 'chezmoi externals: cannot decode %s as %s\n' "${declaration}" "${format}" >&2
            return 1
        }
    done <<< "${declarations}"
}

#
# @description Fetch the `file`, `archive` and `archive-file` externals of a chezmoi source into chezmoi's cache,
#   verified, before any command reads the target state. Only an external with one http(s) `url` and no fallback
#   `urls` is prefetched. One with `urls` (chezmoi tries url, then urls, and keys its cache by each URL, chezmoi 2.73.3
#   internal/chezmoi/sourcestate.go:1861-1886, :1921-1923, which this step does not reproduce) or with a url that is
#   not http(s), and every `git-repo`, is left whole to chezmoi, untouched, with one line saying so. Every failure to
#   prefetch a single-URL http(s) external is fatal. An external without a sha256 is refused: it could not be verified
#   before it is cached. Without curl the step only says so, and chezmoi fetches the externals itself as before.
# @arg $1 path The chezmoi command (its config and source are chezmoi's defaults).
# @stdout One line per external.
# @stderr What failed, naming the external and its URL.
# @exitcode 1 When an external cannot be fetched and verified, the externals cannot be listed, or a listed external
#   has no name, an unknown type or no url.
#
function prefetch_chezmoi_externals() {
    local chezmoi="$1" source physical cache="" scratch listing status=0 name type sha256 refresh seconds fallbacks url
    local -a fields
    if ! command -v curl > /dev/null 2>&1; then
        printf 'chezmoi externals: curl not found; chezmoi fetches them itself, without retries\n' >&2
        return 0
    fi
    if ! { source="$("${chezmoi}" source-path)" && [ -d "${source}" ]; }; then
        printf 'chezmoi externals: chezmoi source-path failed or named no directory\n' >&2
        return 1
    fi
    # chezmoi keeps a symlinked source path as given, and find does not descend into a symlinked start directory, so
    # discovery reads the physical path and every path it prints is physical (U96 round 9).
    if ! { physical="$(cd -P -- "${source}" && pwd -P)" && [[ "${physical}" == /* ]]; }; then # lint-comparisons: allow an absolute-path prefix test
        printf 'chezmoi externals: cannot resolve the source directory %s to its physical path\n' "${source}" >&2
        return 1
    fi
    scratch="$(mktemp -d "${TMPDIR:-/tmp}/chezmoi-externals.XXXXXX")" || {
        printf 'chezmoi externals: cannot create a scratch directory\n' >&2
        return 1
    }
    listing="$(chezmoi_external_list "${chezmoi}" "${physical}" "${scratch}")" || status=1
    rm -rf "${scratch}"
    [ "${status}" -eq 0 ] || return 1
    while IFS=$'\t' read -r -a fields; do
        [ "${#fields[@]}" -gt 0 ] || continue
        name="${fields[0]}" type="${fields[1]:-}" sha256="${fields[2]:-}" refresh="${fields[3]:-}"
        fallbacks="${fields[4]:-}" url="${fields[5]:-}"
        # A line the decode did not produce whole is refused, never skipped: it decides what is fetched.
        if ! { [ "${#fields[@]}" -eq 6 ] && [ -n "${name}" ] && [[ "${fallbacks}" =~ ^[0-9]+$ ]]; }; then
            printf 'chezmoi externals: an external decoded without its fields: %s\n' "${fields[*]}" >&2
            return 1
        fi
        case "${type}" in
        file | archive | archive-file) ;;
        git-repo) continue ;;
        *)
            printf 'chezmoi external %s: unknown type %s\n' "${name}" "${type}" >&2
            return 1
            ;;
        esac
        if [ "${fallbacks}" -ne 0 ]; then
            printf 'chezmoi external %s: left to chezmoi: its declaration lists fallback urls\n' "${name}"
            continue
        fi
        [ "${url}" != - ] || { # lint-comparisons: allow the listing's `-` placeholder for a missing url, not a URL
            printf 'chezmoi external %s: no url\n' "${name}" >&2
            return 1
        }
        if ! [[ "${url}" =~ ^https?:// ]]; then
            printf 'chezmoi external %s: left to chezmoi: %s is not http(s)\n' "${name}" "${url}"
            continue
        fi
        [[ "${sha256}" =~ ^[0-9a-f]{64}$ ]] || {
            printf 'chezmoi external %s: %s has no sha256 checksum; it cannot be verified before it is cached\n' \
                "${name}" "${url}" >&2
            return 1
        }
        seconds="$(chezmoi_external_seconds "${refresh}")" || {
            printf 'chezmoi external %s: refreshPeriod %s is not a sum of whole h, m and s\n' "${name}" "${refresh}" >&2
            return 1
        }
        # Read once, at the first external to fetch: a source without one needs no cache.
        if [ -z "${cache}" ]; then
            if ! { cache="$("${chezmoi}" execute-template '{{ .chezmoi.cacheDir }}')" && [[ "${cache}" == /* ]]; }; then # lint-comparisons: allow an absolute-path prefix test
                printf 'chezmoi externals: cannot read chezmoi'\''s cache directory\n' >&2
                return 1
            fi
        fi
        prefetch_chezmoi_external "${name}" "${url}" "${sha256}" "${seconds}" "${cache}" || return 1
    done <<< "${listing}"
}
# --- chezmoi-externals.sh end ---

function is_tty() {
    [ -t 0 ]
}

function is_not_tty() {
    ! is_tty
}

function is_ci_or_not_tty() {
    is_ci_runner || is_not_tty
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
    local path="$1" expected="${2:-}" actual
    [ -n "${expected}" ] || {
        printf 'Missing checksum for %s\n' "${path}" >&2
        return 1
    }
    actual="$(sha256_file "${path}")" || {
        printf 'sha256_file could not hash %s\n' "${path}" >&2
        return 1
    }
    [ "${actual}" = "${expected}" ] || {
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
    local brew_env
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

    if ! brew_env="$("${brew_prefix}/bin/brew" shellenv)"; then
        echo "${brew_prefix}/bin/brew shellenv failed; cannot continue bootstrap." >&2
        exit 1
    fi
    eval "${brew_env}"
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
    local machine
    local no_tty_option
    local os_type
    local source_path
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
    os_type="$(get_os_type)" || {
        printf 'get_os_type (uname) failed; chezmoi was not installed.\n' >&2
        return 1
    }
    machine="$(uname -m)" || {
        printf 'uname -m failed; chezmoi was not installed.\n' >&2
        return 1
    }
    case "${os_type}/${machine}" in
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
        printf 'Unsupported chezmoi platform: %s/%s\n' "${os_type}" "${machine}" >&2
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
        if ! source_path="$("${chezmoi_cmd}" source-path)"; then
            echo "chezmoi source-path failed; no destination targets were changed." >&2
            return 1
        fi
        find "${source_path}" -type f -name "encrypted_*" -exec rm -fv {} +
    fi

    # Add to PATH for installing the necessary binary files under `$HOME/.local/bin`.
    export PATH="${PATH}:${HOME}/.local/bin"

    # The first read of the target state below would download every archive external itself, and a dropped transfer
    # there fails it with a bare "chezmoi: unexpected EOF" (U96); fetch them first, retried and verified, so the
    # status, diff and apply below read only chezmoi's cache.
    if ! prefetch_chezmoi_externals "${chezmoi_cmd}"; then
        echo "chezmoi externals could not be fetched; no destination targets were changed." >&2
        return 1
    fi

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

    if is_ci_runner && [[ "${HOME}/" != "${RUNNER_TEMP%/}/"* ]]; then
        echo "Refusing to apply on a GitHub Actions runner outside RUNNER_TEMP: ${HOME}" >&2
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
