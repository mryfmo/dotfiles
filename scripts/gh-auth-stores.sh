#!/usr/bin/env bash

# @file gh-auth-stores.sh
# @brief Log in each GitHub CLI credential store that holds no token.
# @description
#   Each GitHub account has its own store, a GH_CONFIG_DIR holding one login:
#   OWNER_GH_CONFIG_DIR, WORK_GH_CONFIG_DIR and WORKER_GH_CONFIG_DIR, declared in
#   home/dot_agents/agent-config.yaml and rendered into ~/.agents/model-profiles.env.
#   A store whose `gh auth status` succeeds is skipped, so a hosts.yml that
#   chezmoi-private already decrypted prompts for nothing. Any other store gets
#   gh's own device-code login with file storage (the Claude sandbox cannot reach
#   the keyring), mode 0600, and gh's HTTPS credential helper. No credential value
#   is read or printed here. Interactive only: `make update` never runs this.

set -Eeuo pipefail

# @description Expand a leading `~/` to $HOME.
# @arg $1 string Path as rendered in model-profiles.env.
function expand_home() {
    local path="$1"
    if [[ ${path} == \~/* ]]; then
        printf '%s/%s\n' "${HOME}" "${path#"~/"}"
    else
        printf '%s\n' "${path}"
    fi
}

# @description Log in one store unless it already holds a working token.
# @arg $1 string Account label: owner, work or worker.
# @arg $2 string The store's GH_CONFIG_DIR.
function ensure_store() {
    local label="$1" dir="$2"
    if GH_CONFIG_DIR="${dir}" gh auth status --hostname github.com > /dev/null 2>&1; then
        printf 'gh-auth: %s store %s already holds a token; skipped\n' "${label}" "${dir}"
        return 0
    fi
    if [[ ! -t 0 ]]; then
        printf 'gh-auth: %s store %s has no token; run "make gh-auth" in a terminal\n' "${label}" "${dir}" >&2
        return 1
    fi
    printf 'gh-auth: %s store %s has no token; log in as the %s account\n' "${label}" "${dir}" "${label}"
    mkdir -p "${dir}"
    GH_CONFIG_DIR="${dir}" gh auth login --hostname github.com --git-protocol https --insecure-storage || return 1
    if [[ -f ${dir}/hosts.yml ]]; then
        chmod 600 "${dir}/hosts.yml"
    fi
    GH_CONFIG_DIR="${dir}" gh auth setup-git --hostname github.com
}

# @description Check every declared store and log in the ones without a token.
# @exitcode 0 Every store holds a token.
# @exitcode 1 A store is undeclared, gh is missing, or a login did not complete.
function main() {
    local env_file="${GH_AUTH_STORES_ENV:-${HOME}/.agents/model-profiles.env}"
    local failures=0 pair label var
    if [[ ! -f ${env_file} ]]; then
        printf 'gh-auth: %s is missing; run "make update" first\n' "${env_file}" >&2
        return 1
    fi
    # shellcheck source=/dev/null
    source "${env_file}"
    if ! command -v gh > /dev/null 2>&1; then
        printf 'gh-auth: gh is not installed; install it, then run "make gh-auth"\n' >&2
        return 1
    fi
    # A token in the environment overrides every store and would hide an empty one.
    unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN
    umask 077
    for pair in owner:OWNER_GH_CONFIG_DIR work:WORK_GH_CONFIG_DIR worker:WORKER_GH_CONFIG_DIR; do
        label="${pair%%:*}"
        var="${pair#*:}"
        if [[ -z ${!var:-} ]]; then
            printf 'gh-auth: %s is not set in %s; run "make update" first\n' "${var}" "${env_file}" >&2
            failures=$((failures + 1))
            continue
        fi
        ensure_store "${label}" "$(expand_home "${!var}")" || failures=$((failures + 1))
    done
    [[ ${failures} -eq 0 ]]
}

main "$@"
