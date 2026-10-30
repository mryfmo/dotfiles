#!/usr/bin/env bash
# @file pr-body-edit.sh
# @brief Replace the body of the open pull request of the current branch, the worker seat's lever.
# @description
#   Regime-cutover U28, the worker seat's lever, allowed only in the form
#   `~/.local/bin/common/pr-body-edit.sh --body-file *` by `home/dot_agents/omp/policies/worker.yml`
#   (scripts/orchestrator/README.md, "Seat levers for GitHub writes"); the orchestrator's policy denies it. It
#   edits only the pull request of the branch the seat has checked out: `git branch --show-current` must name a
#   branch other than `main`, and `gh pr view --json number,headRefName,state` (the pull request of that branch)
#   must report it as `headRefName` and `OPEN`. The body file is a regular file (not a symlink) of 1 to 65536
#   bytes whose real path is inside `$TMPDIR` or the checkout. The new body must hold exactly one line starting
#   `Program-Unit:`, and it must be `Program-Unit: <program>/U<n>`, the line `regime-ci.py` reads: `<program>` in
#   `regime-init`'s grammar (`^[a-z0-9][a-z0-9_-]{0,63}$`) naming a store the checkout holds,
#   `.orchestration/orchestrate/<program>/units.tsv` (U71), and a plain unit id (a fix round writes its parent id,
#   `preferences.md` standing order 24); when the current body already carries one such line, the program and the
#   unit must stay the same, so an edit fixes the line or the text but never moves a pull request to another
#   program or unit. Every `## ` heading line and the `Generated with [Claude Code]` footer line of
#   the current body must still be in the new body, so sections are added or rewritten, never dropped. The one
#   write is `gh pr edit <n> --body-file <file>`. Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds (perl
#   `alarm`).
# @option --body-file <file> The new body.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `edited pr=<n> branch=<b> program=<program> unit=U<n> sha256=<body sha256>`.
# @exitcode 0 The body was replaced.
# @exitcode 1 A `git` or `gh` read, or the edit, failed.
# @exitcode 2 Refused: usage, the branch, the pull request's state, the body file, or the body's content.
# @example
#   ~/.local/bin/common/pr-body-edit.sh --body-file "$TMPDIR/body.md"
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
    # shellcheck disable=SC2034 # read by the levers that source regime-env from this directory
    LEVER_DIR=${dir}
    name=${self##*/}
    home=$(cd "${HOME}" 2> /dev/null && pwd -P) || home=''             # producer-status: allow the if below takes an empty home as the checkout layout
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
        digest=$(sha256sum < "${self}") || digest='' # producer-status: allow the regex test below refuses an empty digest
    else
        digest=$(shasum -a 256 < "${self}") || digest='' # producer-status: allow the regex test below refuses an empty digest
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
# The isolated git and the environment scrub come from the library beside this script (U113): the toplevel and the
# current branch are read by a git no caller variable or configuration steers.
[[ -r ${LEVER_DIR}/git-isolated.sh ]] || {
    echo "pr-body-edit.sh: refused: git-isolated.sh unreadable beside this script: ${LEVER_DIR}/git-isolated.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/git-isolated.sh
. "${LEVER_DIR}/git-isolated.sh"
# shellcheck disable=SC2119 # no name is kept: every GIT_* and transport variable goes
git_env_scrub

[[ -r ${LEVER_DIR}/read-lib.sh ]] || {
    echo "pr-body-edit.sh: refused: read-lib.sh unreadable beside this script: ${LEVER_DIR}/read-lib.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/read-lib.sh
. "${LEVER_DIR}/read-lib.sh"

lever='pr-body-edit.sh'
usage='usage: pr-body-edit.sh --body-file <file>'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
unit_line='^Program-Unit: [a-z0-9][a-z0-9_-]{0,63}/U[0-9]+$'
footer_re='Generated with \[Claude Code\]\(https://claude\.com/claude-code\)'

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

# @description Refuse unless $1 is a regular file of 1 to 65536 bytes inside $TMPDIR or the checkout.
# @arg $1 path The body file.
# @set body_path Its real path.
body_file_check() {
    local file=$1 dir root size
    [[ -f ${file} && ! -L ${file} ]] || refuse "the body file is not a regular file: ${file}"
    case ${file} in # lint-comparisons: allow splits the argument at its last slash; the real path is compared below
    */*) dir=${file%/*} ;;
    *) dir=. ;;
    esac
    [[ -n ${dir} ]] || dir=/
    dir=$(cd "${dir}" && pwd -P) || refuse "cannot resolve the directory of ${file}"
    body_path=${dir}/${file##*/}
    size=$(wc -c < "${body_path}") || refuse "cannot read ${body_path}"
    size=${size//[[:space:]]/}
    if ! [[ ${size} =~ ^[0-9]+$ ]] || ((size == 0 || size > 65536)); then
        refuse "the body file must hold 1 to 65536 bytes: ${body_path}"
    fi
    for root in "${TMPDIR:-}" "${toplevel}"; do
        [[ -n ${root} && -d ${root} ]] || continue
        root=$(cd "${root}" && pwd -P) || continue    # producer-status: allow a root that cannot be entered holds no body file; the refusal after the loop stands
        [[ ${body_path} == "${root}"/* ]] && return 0 # lint-comparisons: allow both sides are pwd -P forms
    done
    refuse "the body file is outside \$TMPDIR and the checkout: ${body_path}"
}

# @description Print the lines of file $2 (CR stripped) that match the ERE $1, one per line. The ERE reaches awk
#   through the environment, since `awk -v` would read its backslashes as escapes.
# @arg $1 string The ERE.
# @arg $2 path The file.
lines_matching() {
    LINES_RE=$1 awk '{ sub(/\r$/, "") } $0 ~ ENVIRON["LINES_RE"]' "$2"
}

[[ $# -eq 2 && $1 == --body-file ]] || refuse "${usage}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'
toplevel=$(git_isolated rev-parse --show-toplevel 2> /dev/null) || refuse 'not in a git checkout'
branch=$(git_isolated branch --show-current) || fail 'git branch --show-current failed'
[[ -n ${branch} ]] || refuse 'HEAD is detached; switch to the branch of your pull request'
[[ ${branch} != main ]] || refuse 'the current branch is main'
body_file_check "$2"
markers=$(lines_matching '^Program-Unit:' "${body_path}") || refuse "cannot read ${body_path}"
[[ -n ${markers} && ${markers} != *$'\n'* && ${markers} =~ ${unit_line} ]] ||
    refuse "the body must hold exactly one line 'Program-Unit: <program>/U<n>' (a plain unit id); it holds: ${markers:-none}"
marker=${markers#Program-Unit: }
program=${marker%/*}
unit=${marker##*/}
[[ -f ${toplevel}/.orchestration/orchestrate/${program}/units.tsv ]] ||
    refuse "the Program-Unit line names ${program}, but the checkout holds no .orchestration/orchestrate/${program}/units.tsv"

view=$(gh_bounded pr view --json number,headRefName,state --jq '[(.number | tostring), .headRefName, .state] | @tsv') ||
    fail "cannot read the pull request of ${branch}"
IFS=$'\t' read -r number head state <<< "${view}"
[[ ${number} =~ ^[1-9][0-9]*$ ]] || fail "gh pr view printed no pull request number: ${number}"
[[ ${head} == "${branch}" ]] || refuse "pull request ${number} is the pull request of ${head}, not of the current branch ${branch}"
[[ ${state} == OPEN ]] || refuse "pull request ${number} is ${state}, not OPEN"

current=$(mktemp "${TMPDIR:-/tmp}/pr-body-edit.XXXXXX") || fail 'mktemp failed'
trap 'rm -f "${current}"' EXIT
gh_bounded pr view "${number}" --json body --jq .body > "${current}" || fail "cannot read the body of pull request ${number}"
old_markers=$(lines_matching "${unit_line}" "${current}") || fail "cannot read ${current}"
if [[ -n ${old_markers} && ${old_markers} != *$'\n'* && ${old_markers#Program-Unit: } != "${marker}" ]]; then
    refuse "the current body names ${old_markers#Program-Unit: }; an edit keeps the program and the unit (the new body names ${marker})"
fi
kept=$(lines_matching "^## |${footer_re}" "${current}") || fail "cannot read ${current}"
new_lines=$(lines_matching '' "${body_path}") || refuse "cannot read ${body_path}"
while IFS= read -r line; do
    [[ -n ${line} ]] || continue
    grep -Fxq -- "${line}" <<< "${new_lines}" || refuse "the new body drops the line of the current body: ${line}"
done <<< "${kept}"

gh_bounded pr edit "${number}" --body-file "${body_path}" >&2 || fail "gh pr edit ${number} failed"
if command -v sha256sum > /dev/null; then
    digest=$(sha256sum < "${body_path}") || fail "the body was pushed; cannot hash ${body_path} for the report"
else
    digest=$(shasum -a 256 < "${body_path}") || fail "the body was pushed; cannot hash ${body_path} for the report"
fi
echo "edited pr=${number} branch=${branch} program=${program} unit=${unit} sha256=${digest%% *}"
