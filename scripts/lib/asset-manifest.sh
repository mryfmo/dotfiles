#!/usr/bin/env bash

# @file scripts/lib/asset-manifest.sh
# @brief Record installed agent assets in a private atomic JSON manifest.

#
# @description Return the installed version of a Claude Code plugin.
# @arg $1 string Fully qualified Claude Code plugin ID.
#
function manifest_claude_plugin_version() {
    local plugin_id="$1"
    local version

    version="$(claude plugin list --json 2> /dev/null | jq -er --arg id "${plugin_id}" 'first(.[] | select(.id == $id) | .version)' 2> /dev/null)" || version="unknown"
    printf '%s\n' "${version}"
}

#
# @description Return the installed version of a Codex plugin.
# @arg $1 string Fully qualified Codex plugin ID.
#
function manifest_codex_plugin_version() {
    local plugin_id="$1"
    local version

    version="$(codex plugin list --json 2> /dev/null | jq -er --arg id "${plugin_id}" 'first(.installed[] | select(.pluginId == $id) | .version)' 2> /dev/null)" || version="unknown"
    printf '%s\n' "${version}"
}

#
# @description Return the installed Homebrew formula version.
# @arg $1 string Homebrew formula name.
#
function manifest_brew_formula_version() {
    local formula="$1"
    local version

    version="$(brew list --versions "${formula}" 2> /dev/null | awk -v formula="${formula}" '$1 == formula { print $2; exit }')"
    printf '%s\n' "${version:-unknown}"
}

#
# @description Atomically replace one step in the installed asset manifest.
# @arg $1 string Install step name.
# @arg $2 string Asset kind.
# @arg $3 string Installed source version.
# @arg $@ string Absolute paths followed by an optional `--` and command lines.
#
function _manifest_record() {
    [ "$#" -ge 3 ] || return 1

    local step="$1"
    local kind="$2"
    local source_version="$3"
    local manifest_directory manifest_path temporary_path paths_json commands_json installed_at path
    local -a paths=()
    local -a commands=()
    shift 3

    case "${kind}" in
    plugin | rsync | brew | installer | integration) ;;
    *) return 1 ;;
    esac
    [ -n "${step}" ] && [ -n "${source_version}" ] && [ -n "${HOME:-}" ] || return 1

    while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do
        paths+=("$1")
        shift
    done
    if [ "${1:-}" = "--" ]; then
        shift
        commands=("$@")
    fi
    for path in "${paths[@]}"; do
        [[ "${path}" == /* ]] || return 1
    done

    paths_json="$(jq -cn --args '$ARGS.positional' "${paths[@]}")" || return 1
    commands_json="$(jq -cn --args '$ARGS.positional' "${commands[@]}")" || return 1
    installed_at="$(date -u '+%Y-%m-%dT%H:%M:%SZ')" || return 1
    manifest_directory="${HOME}/.agents"
    manifest_path="${manifest_directory}/.installed-manifest.json"
    mkdir -p "${manifest_directory}" || return 1
    temporary_path="$(mktemp "${manifest_path}.tmp.XXXXXX")" || return 1
    chmod 600 "${temporary_path}" || {
        rm -f "${temporary_path}"
        return 1
    }

    local -a jq_arguments=(
        --arg step "${step}"
        --arg installed_at "${installed_at}"
        --arg kind "${kind}"
        --argjson paths "${paths_json}"
        --argjson commands "${commands_json}"
        --arg source_version "${source_version}"
    )
    # shellcheck disable=SC2016 # jq expands these jq variables; the shell must not expand them.
    local jq_filter='
        if type != "object" or ((.steps // {}) | type) != "object" then error("invalid manifest") else . end
        | .version = 1
        | .steps = (.steps // {})
        | .steps[$step] = {
            installed_at: $installed_at,
            kind: $kind,
            paths: $paths,
            commands: $commands,
            source_version: $source_version
        }
    '

    if [ -f "${manifest_path}" ]; then
        jq "${jq_arguments[@]}" "${jq_filter}" "${manifest_path}" > "${temporary_path}" || {
            rm -f "${temporary_path}"
            return 1
        }
    else
        printf '{"version":1,"steps":{}}\n' | jq "${jq_arguments[@]}" "${jq_filter}" > "${temporary_path}" || {
            rm -f "${temporary_path}"
            return 1
        }
    fi
    mv "${temporary_path}" "${manifest_path}" || {
        rm -f "${temporary_path}"
        return 1
    }
}

#
# @description Record one install step without propagating manifest failures.
# @arg $1 string Install step name.
# @arg $2 string Asset kind.
# @arg $3 string Installed source version.
# @arg $@ string Absolute paths followed by an optional `--` and command lines.
# @stderr Prints one warning line when recording fails.
#
function manifest_record() {
    local step="${1:-unknown}"

    if ! _manifest_record "$@" 2> /dev/null; then
        printf 'warning: failed to record asset manifest step %s\n' "${step}" >&2
    fi
    return 0
}
