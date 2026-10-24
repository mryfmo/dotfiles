#!/usr/bin/env bash
# @file pr-thread-reply.sh
# @brief Reply to one review thread of a pull request with a disposition, the orchestrator seat's lever.
# @description
#   Regime-cutover U28, a lever of the omp orchestrator seat, allowed by the row
#   `~/.local/bin/common/pr-thread-reply.sh *` of `home/dot_agents/omp/policies/orchestrator.yml`
#   (scripts/orchestrator/README.md, "Seat levers for GitHub writes"). Every argument is checked before the
#   first `gh` call, and the one write is
#   `gh api -X POST repos/<owner>/<repo>/pulls/<pr>/comments/<comment-id>/replies -F body=@<file>`.
#   `<pr>` and `<comment-id>` are decimal. The body file is a regular file (not a symlink) of 1 to 65536 bytes
#   whose real path is inside `$TMPDIR` or the checkout's `.orchestration/` (the program's store), so no other
#   file of the account can be posted. Its first line is a disposition of `preferences.md` standing order 22:
#   `fixed: <40-hex sha>`, `refuted: <text citing a URL or a file:line>`, `residual: unit=U<n> gate=<clause>`
#   or `residual: operator=<decisions.tsv ts>`; `pr-threads-check.sh` reads the same grammar. `<owner>/<repo>`
#   comes from `gh repo view --json nameWithOwner`, never from an argument. The comment must be a review comment
#   of that pull request (`gh api repos/<owner>/<repo>/pulls/comments/<comment-id>`, its `pull_request_url`
#   ends in `/pulls/<pr>`) and the first comment of its thread (no `in_reply_to_id`), since GitHub takes a reply
#   only to that one. Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
# @arg $1 int The pull request number.
# @arg $2 int The id of the thread's first review comment (`databaseId`, the `#discussion_r<id>` anchor).
# @option --body-file <file> The reply text.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `replied pr=<pr> comment=<id> reply=<new id> url=<html url>`.
# @exitcode 0 The reply was posted.
# @exitcode 1 A `gh` read or the write failed.
# @exitcode 2 Refused: usage, the body file, the disposition, or a comment that is not the thread's first on <pr>.
# @example
#   ~/.local/bin/common/pr-thread-reply.sh 480 4365170609 --body-file "$TMPDIR/reply.md"
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

lever='pr-thread-reply.sh'
usage='usage: pr-thread-reply.sh <pr> <comment-id> --body-file <file>'
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

# @description Succeed when $1, a reply's first line, is a disposition (`preferences.md` standing order 22).
# @arg $1 string The line.
disposition_line() {
    local fixed='^fixed: [0-9a-f]{40}( |$)'
    local refuted='^refuted: .*(https://[^[:space:]]+|[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*:[0-9]+)'
    local unit='^residual: unit=U[0-9]+[a-z]? gate=[^[:space:]]'
    local operator='^residual: operator=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$'
    [[ $1 =~ ${fixed} || $1 =~ ${refuted} || $1 =~ ${unit} || $1 =~ ${operator} ]]
}

# @description Refuse unless $1 is a regular file of 1 to 65536 bytes inside $TMPDIR or <toplevel>/.orchestration.
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
    for root in "${TMPDIR:-}" "${toplevel}/.orchestration"; do
        [[ -n ${root} && -d ${root} ]] || continue
        root=$(cd "${root}" && pwd -P) || continue
        [[ ${body_path} == "${root}"/* ]] && return 0 # lint-comparisons: allow both sides are pwd -P forms
    done
    refuse "the body file is outside \$TMPDIR and the checkout's .orchestration/: ${body_path}"
}

[[ $# -eq 4 && $3 == --body-file ]] || refuse "${usage}"
pr=$1
comment=$2
[[ ${pr} =~ ^[1-9][0-9]{0,9}$ ]] || refuse "the pull request is not a decimal number: ${pr}"
[[ ${comment} =~ ^[1-9][0-9]{0,19}$ ]] || refuse "the comment id is not a decimal number: ${comment}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'
toplevel=$(git rev-parse --show-toplevel 2> /dev/null) || refuse 'not in a git checkout'
body_file_check "$4"
first=$(sed -n '1{s/\r$//;p;}' "${body_path}") || refuse "cannot read ${body_path}"
disposition_line "${first}" ||
    refuse "the first line is not a disposition (fixed: <sha> | refuted: <doc or file:line> | residual: unit=U<n> gate=<clause> | residual: operator=<ts>): ${first}"

repo=$(gh_bounded repo view --json nameWithOwner --jq .nameWithOwner) || fail 'gh repo view failed'
[[ ${repo} =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || fail "gh repo view printed no owner/repo: ${repo}"
owner_pr=$(gh_bounded api "repos/${repo}/pulls/comments/${comment}" \
    --jq '[(.pull_request_url | capture("/pulls/(?<n>[0-9]+)$").n), (.in_reply_to_id // 0 | tostring)] | @tsv') ||
    fail "cannot read review comment ${comment} of ${repo}"
IFS=$'\t' read -r comment_pr reply_to <<< "${owner_pr}"
[[ ${comment_pr} == "${pr}" ]] || refuse "review comment ${comment} belongs to pull request ${comment_pr:-none}, not ${pr}"
[[ ${reply_to} == 0 ]] || refuse "review comment ${comment} is a reply (to ${reply_to}); name the thread's first comment"

posted=$(gh_bounded api -X POST "repos/${repo}/pulls/${pr}/comments/${comment}/replies" -F "body=@${body_path}" \
    --jq '[(.id | tostring), .html_url] | @tsv') || fail "the reply to ${comment} on pull request ${pr} failed"
IFS=$'\t' read -r reply url <<< "${posted}"
echo "replied pr=${pr} comment=${comment} reply=${reply} url=${url}"
