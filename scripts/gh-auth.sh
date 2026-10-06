#!/usr/bin/env bash

# @file gh-auth.sh
# @brief Log in this machine's GitHub account when gh holds no working login.
# @description
#   Every seat on a machine acts as that machine's one GitHub account, stored in
#   gh's default configuration directory. When `gh auth status` succeeds, nothing
#   happens. Otherwise, on a terminal only, gh runs its own device-code login with
#   its default storage: the OS keyring where present, gh's own file fallback
#   elsewhere. Git needs no setup: the managed git config's `!gh auth git-credential`
#   helper serves the login, and `gh auth setup-git` would rewrite that
#   chezmoi-managed file. No credential value is read or printed here.
#   Interactive only: `make update` never runs this.

set -Eeuo pipefail

# @description Log in unless gh already holds a working login.
# @exitcode 0 gh holds a working login, already or after the login.
# @exitcode 1 gh is missing, there is no terminal, or the login did not complete.
function main() {
    # gh may exist only as a mise shim (a fresh bootstrap, or a shell without mise activated).
    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
    if ! command -v gh > /dev/null 2>&1; then
        printf 'gh-auth: gh is not installed; install it, then run "make gh-auth"\n' >&2
        return 1
    fi
    # A token in the environment would answer for an empty login.
    unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN
    if gh auth status --hostname github.com > /dev/null 2>&1; then
        printf 'gh-auth: gh already holds a working login; skipped\n'
        return 0
    fi
    if [[ ! -t 0 ]]; then
        printf 'gh-auth: gh holds no working login; run "make gh-auth" in a terminal\n' >&2
        return 1
    fi
    printf 'gh-auth: gh holds no working login; log in as this machine'"'"'s GitHub account\n'
    gh auth login --hostname github.com --git-protocol https
}

main "$@"
