#!/usr/bin/env bash
# shellcheck shell=bash

# @file scripts/lib/chezmoi-externals.sh
# @brief Fetch chezmoi's archive and file externals into its cache before chezmoi reads them.
# @description
#   chezmoi downloads a `file`, `archive` or `archive-file` external the first time a command reads the target
#   state (`chezmoi status`, `diff`, `apply`) and keeps it in `<cacheDir>/external/<sha256 of the URL>`, which it
#   reuses while the file is younger than the external's `refreshPeriod` (chezmoi 2.73.3
#   internal/chezmoi/sourcestate.go:1921-1942; reference: special-files/chezmoiexternal-format, "chezmoi will cache
#   downloaded URLs"). A dropped transfer there surfaces as a bare `chezmoi: unexpected EOF` (io.ReadAll's error is
#   returned unwrapped, :1954-1961) that names neither the external nor its URL, and nothing retries it.
#   prefetch_chezmoi_externals takes that download out of chezmoi: one bounded, retried download per external, its
#   sha256 checked before it is cached, so the read that follows finds a fresh, verified cache and fetches nothing.
#   A dropped or failed transfer is retried; a complete download whose sha256 differs fails at once.
#   setup.sh runs before the repository exists, so it carries a copy of the functions below;
#   tests/unit/test_chezmoi_externals.py keeps the copies equal. It needs curl, awk and sha256sum or shasum.

# Download attempts per URL, and the first wait between them in seconds (doubled after each failure): constants,
# never read from the environment, so no caller can unbound the retries. Tests replace `sleep` instead.
CHEZMOI_EXTERNAL_ATTEMPTS=4
CHEZMOI_EXTERNAL_RETRY_DELAY=5

#
# @description Print the lowercase sha256 of a file, or of standard input with no argument.
# @arg $1 path Optional file to hash.
# @stdout The digest.
# @exitcode 1 When the hash tool fails or prints no 64-digit lowercase hex digest.
#
function chezmoi_external_sha256() {
    local digest
    if command -v sha256sum > /dev/null 2>&1; then
        digest="$(sha256sum "$@")" || return 1
    else
        digest="$(shasum -a 256 "$@")" || return 1
    fi
    digest="${digest%% *}"
    [[ "${digest}" =~ ^[0-9a-f]{64}$ ]] || return 1
    printf '%s\n' "${digest}"
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
    [ -n "${rest}" ] && [ "${rest}" != 0 ] || {
        printf '0\n'
        return 0
    }
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
    key="$(printf '%s' "${url}" | chezmoi_external_sha256)" || {
        printf 'chezmoi external %s: cannot hash the URL %s for its cache key\n' "${name}" "${url}" >&2
        return 1
    }
    entry="${cache}/external/${key}"
    if [ -f "${entry}" ]; then
        # An entry this step cannot read the age or the digest of is fetched again, never kept.
        modified="$(stat -c %Y "${entry}" 2> /dev/null || stat -f %m "${entry}")" || modified=0
        [[ "${modified}" =~ ^[0-9]+$ ]] || modified=0
        now="$(date +%s)" && [[ "${now}" =~ ^[0-9]+$ ]] || {
            printf 'chezmoi external %s: date +%%s failed; cannot tell the cache entry'\''s age\n' "${name}" >&2
            return 1
        }
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
# @description Print every external a chezmoi source declares, one per line, tab-separated: target path, type,
#   sha256, refresh period, the number of fallback `urls`, and `url`. A missing type, sha256 or url prints as `-` and
#   a missing refresh period as `0`, so no field is empty (a tab is whitespace to `read`, which would merge two tabs
#   into one separator). Every `.chezmoiexternal.<format>` file anywhere in the source and every file
#   in a `.chezmoiexternals/` directory is rendered by chezmoi itself (`execute-template`, with the source's
#   templates) and decoded by its own fromYaml, fromJson, fromJsonc or fromToml. Every producer's status is
#   checked: a failed find, render or decode is an error that names the file, never an empty list.
# @arg $1 path The chezmoi command.
# @arg $2 path The source directory (`chezmoi source-path`).
# @arg $3 path A scratch directory for the rendered files.
# @stdout The externals.
# @exitcode 1 When a declaration file cannot be found, rendered or decoded, or has an unknown format.
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
    local chezmoi="$1" source cache="" scratch listing status=0 name type sha256 refresh seconds fallbacks url
    local -a fields
    if ! command -v curl > /dev/null 2>&1; then
        printf 'chezmoi externals: curl not found; chezmoi fetches them itself, without retries\n' >&2
        return 0
    fi
    source="$("${chezmoi}" source-path)" && [ -d "${source}" ] || {
        printf 'chezmoi externals: chezmoi source-path failed or named no directory\n' >&2
        return 1
    }
    scratch="$(mktemp -d "${TMPDIR:-/tmp}/chezmoi-externals.XXXXXX")" || {
        printf 'chezmoi externals: cannot create a scratch directory\n' >&2
        return 1
    }
    listing="$(chezmoi_external_list "${chezmoi}" "${source}" "${scratch}")" || status=1
    rm -rf "${scratch}"
    [ "${status}" -eq 0 ] || return 1
    while IFS=$'\t' read -r -a fields; do
        [ "${#fields[@]}" -gt 0 ] || continue
        name="${fields[0]}" type="${fields[1]:-}" sha256="${fields[2]:-}" refresh="${fields[3]:-}"
        fallbacks="${fields[4]:-}" url="${fields[5]:-}"
        # A line the decode did not produce whole is refused, never skipped: it decides what is fetched.
        [ "${#fields[@]}" -eq 6 ] && [ -n "${name}" ] && [[ "${fallbacks}" =~ ^[0-9]+$ ]] || {
            printf 'chezmoi externals: an external decoded without its fields: %s\n' "${fields[*]}" >&2
            return 1
        }
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
            cache="$("${chezmoi}" execute-template '{{ .chezmoi.cacheDir }}')" && [[ "${cache}" == /* ]] || { # lint-comparisons: allow an absolute-path prefix test
                printf 'chezmoi externals: cannot read chezmoi'\''s cache directory\n' >&2
                return 1
            }
        fi
        prefetch_chezmoi_external "${name}" "${url}" "${sha256}" "${seconds}" "${cache}" || return 1
    done <<< "${listing}"
}
