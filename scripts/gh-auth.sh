#!/usr/bin/env bash

# @file gh-auth.sh
# @brief Log in this machine's GitHub account when gh holds no working login.
# @description
#   Every seat on a machine acts as that machine's one GitHub account, stored in
#   gh's default configuration directory. When gh holds a working login whose
#   token sits in gh's own file, only that file's mode is set. Otherwise, on a
#   terminal only, gh runs its own device-code login with `--insecure-storage`.
#   File storage is deliberate: the Claude Linux sandbox cannot reach the OS
#   keyring, so a keyring login leaves every sandboxed seat without gh. The file,
#   hosts.yml, is user-owned and set to mode 0600. Git needs no setup: the managed
#   git config's `!gh auth git-credential` helper serves the login, and
#   `gh auth setup-git` would rewrite that chezmoi-managed file. No credential
#   value is read or printed here.
#   Interactive only: `make update` never runs this.

set -Eeuo pipefail

# @description Set gh's hosts.yml, where the login's token lives, to mode 0600.
# @exitcode 0 The file is absent or now has mode 0600.
# @exitcode 1 chmod failed.
function secure_hosts_file() {
    local dir="${GH_CONFIG_DIR:-${XDG_CONFIG_HOME:-${HOME}/.config}/gh}"
    if [[ ! -f ${dir}/hosts.yml ]]; then
        return 0
    fi
    if ! chmod 600 "${dir}/hosts.yml"; then
        printf 'gh-auth: cannot set %s/hosts.yml to mode 0600; make it yours, then run "make gh-auth"\n' "${dir}" >&2
        return 1
    fi
}

# @description Log in unless gh already holds a working login in its own file.
# @exitcode 0 gh holds a working file-stored login, already or after the login.
# @exitcode 1 gh is missing, there is no terminal, the login did not complete, or chmod failed.
function main() {
    # gh may exist only as a mise shim (a fresh bootstrap, or a shell without mise activated).
    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
    if ! command -v gh > /dev/null 2>&1; then
        printf 'gh-auth: gh is not installed; install it, then run "make gh-auth"\n' >&2
        return 1
    fi
    # A token in the environment would answer for an empty login.
    unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN
    # gh names the file a working token came from; a keyring token shows "keyring".
    local source
    source="$(gh auth status --hostname github.com --active --json hosts \
        --jq '.hosts["github.com"][] | select(.state == "success") | .tokenSource' 2> /dev/null || true)"
    if [[ ${source} == */hosts.yml ]]; then
        printf 'gh-auth: gh already holds a working login; skipped\n'
        secure_hosts_file
        return
    fi
    local reason="gh holds no working login"
    if [[ -n ${source} ]]; then
        reason="gh's working login is in the OS keyring, which the Claude sandbox cannot reach"
    fi
    if [[ ! -t 0 ]]; then
        printf 'gh-auth: %s; run "make gh-auth" in a terminal\n' "${reason}" >&2
        return 1
    fi
    printf 'gh-auth: %s; log in as this machine'"'"'s GitHub account\n' "${reason}"
    gh auth login --hostname github.com --git-protocol https --insecure-storage
    secure_hosts_file
}

main "$@"
