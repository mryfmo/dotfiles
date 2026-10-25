#!/usr/bin/env bash
# @file pr-update-branch.sh
# @brief Merge main into an open pull request's branch (`gh pr update-branch`), the orchestrator seat's lever.
# @description
#   Regime-cutover U28, a lever of the omp orchestrator seat, allowed by the row
#   `~/.local/bin/common/pr-update-branch.sh *` of `home/dot_agents/omp/policies/orchestrator.yml`
#   (scripts/orchestrator/README.md, "Seat levers for GitHub writes"). `<pr>` is decimal and checked before the
#   first `gh` call. `gh pr view <pr> --json state,baseRefName,headRefOid` must report `OPEN` and base `main`,
#   else the lever refuses; the one write is `gh pr update-branch <pr>`, GitHub's merge form (never `--rebase`,
#   which rewrites the worker's branch), and the head is read again afterwards. The new head needs its own audit
#   and `correct` ledger row before `pr-merge.sh` merges it (U71: no verdict carries over from the old head). Each
#   `gh` call is bounded
#   by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
# @arg $1 int The pull request number.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `updated pr=<pr> old=<head before> new=<head after>`.
# @exitcode 0 The branch was updated (`old` equals `new` when it was already up to date).
# @exitcode 1 A `gh` read or the update failed.
# @exitcode 2 Refused: usage, a pull request that is not open, or a base other than main.
# @example
#   ~/.local/bin/common/pr-update-branch.sh 480
set -euo pipefail

# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
lever_self_check() {
    local src dir self name pin digest home
    # The directory is split from the path in the shell, so no external producer (dirname) can fail unseen.
    src=${BASH_SOURCE[0]}
    case ${src} in
    */*) dir=${src%/*} ;;
    *) dir=. ;;
    esac
    [[ -n ${dir} ]] || dir=/
    dir=$(cd "${dir}" && pwd -P) || {
        echo "${src##*/}: refused: cannot resolve the script directory of ${src}" >&2
        exit 2
    }
    self=${dir}/${BASH_SOURCE[0]##*/}
    name=${self##*/}
    home=$(cd "${HOME}" 2> /dev/null && pwd -P) || home=''
    if [[ -n ${home} && ${dir} == "${home}/.local/bin/common" ]]; then # lint-comparisons: allow both sides are pwd -P forms
        LEVER_MANIFEST=${HOME}/.agents/agent-config.yaml
    else
        LEVER_MANIFEST=${dir}/../../home/dot_agents/agent-config.yaml
    fi
    [[ -r ${LEVER_MANIFEST} ]] || {
        echo "${name}: refused: manifest unreadable: ${LEVER_MANIFEST}" >&2
        exit 2
    }
    pin=$(sed -n -E "s/^      ${name//./\\.}: ([0-9a-f]{64})\$/\\1/p" "${LEVER_MANIFEST}") || {
        echo "${name}: refused: cannot read ${LEVER_MANIFEST}" >&2
        exit 2
    }
    [[ ${pin} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: no single sha256 pin for ${name} in ${LEVER_MANIFEST}" >&2
        exit 2
    }
    if command -v sha256sum > /dev/null; then
        digest=$(sha256sum < "${self}") || digest=''
    else
        digest=$(shasum -a 256 < "${self}") || digest=''
    fi
    digest=${digest%% *}
    [[ ${digest} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: cannot hash ${self}" >&2
        exit 2
    }
    [[ ${digest} == "${pin}" ]] || {
        echo "${name}: refused: sha256 ${digest} of ${self} differs from the pin in ${LEVER_MANIFEST}" >&2
        exit 2
    }
}
lever_self_check

lever='pr-update-branch.sh'
usage='usage: pr-update-branch.sh <pr>'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}

# @description Print the refusal on stderr and exit 2; nothing was written to GitHub.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print the failure on stderr and exit 1: a read or the write failed.
# @arg $@ string The reason.
fail() {
    echo "${lever}: $*" >&2
    exit 1
}

# @description Run `gh` with its wait bounded by PR_LEVER_GH_TIMEOUT seconds.
# @arg $@ string The `gh` arguments.
gh_bounded() {
    perl -e 'alarm shift; exec @ARGV or die "exec gh: $!\n"' "${gh_timeout}" gh "$@"
}

[[ $# -eq 1 ]] || refuse "${usage}"
pr=$1
[[ ${pr} =~ ^[1-9][0-9]{0,9}$ ]] || refuse "the pull request is not a decimal number: ${pr}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'

view=$(gh_bounded pr view "${pr}" --json state,baseRefName,headRefOid --jq '[.state, .baseRefName, .headRefOid] | @tsv') ||
    fail "cannot read pull request ${pr}"
IFS=$'\t' read -r state base old <<< "${view}"
[[ ${state} == OPEN ]] || refuse "pull request ${pr} is ${state:-unreadable}, not OPEN"
[[ ${base} == main ]] || refuse "pull request ${pr} targets ${base:-nothing}, not main"
[[ ${old} =~ ^[0-9a-f]{40}$ ]] || fail "pull request ${pr} has no readable head: ${old}"

gh_bounded pr update-branch "${pr}" >&2 || fail "gh pr update-branch ${pr} failed"
new=$(gh_bounded pr view "${pr}" --json headRefOid --jq .headRefOid) || fail "cannot read the new head of ${pr}"
[[ ${new} =~ ^[0-9a-f]{40}$ ]] || fail "pull request ${pr} has no readable head after the update: ${new}"
echo "updated pr=${pr} old=${old} new=${new}"
