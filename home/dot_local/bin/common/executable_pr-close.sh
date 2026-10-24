#!/usr/bin/env bash
# @file pr-close.sh
# @brief Close the pull requests a clean-up table marks `close:`, with the row's text as the comment.
# @description
#   Regime-cutover U28, a lever of the omp orchestrator seat, allowed only in the form
#   `~/.local/bin/common/pr-close.sh --from-table *` by `home/dot_agents/omp/policies/orchestrator.yml`
#   (scripts/orchestrator/README.md, "Seat levers for GitHub writes"). The table is a table the orchestrator
#   wrote: a regular file (not a symlink) whose real path is under
#   `<toplevel>/.orchestration/orchestrate/<program>/handouts/` of the main checkout, where the orchestrator seat
#   runs (a linked worktree, a worker's clone, is refused). The lever reads its `## Open pull requests` section,
#   whose header row must be `| PR | branch | opened | files | title | default |`; every row must carry a `#<n>`
#   PR cell and a backticked branch cell, else the whole table is refused before any `gh` call. The selected rows
#   are those whose `default` cell starts with `close:`; `--only <pr>` narrows them to that one row and is refused
#   when the table has no such `close:` row. Then, per row, read-only: `gh pr view <n>` must report `OPEN` and the
#   table's branch as `headRefName`, and `gh pr list --state open --head <branch>` must list no other pull
#   request (#396 and #412 share `tools/anthropic-auth-route-structured`); a row failing that is refused with its
#   own line. A failed `gh` read aborts the run before any close. Only then does each remaining row get
#   `gh pr close <n> --comment <default cell>`. The lever never passes `--delete-branch` (closing one of two pull
#   requests on a shared branch that way would close the other) and never deletes a branch. Each `gh` call is
#   bounded by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
# @option --from-table <file> The clean-up table.
# @option --only <pr> Close only this row.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One line per selected row, `closed pr=<n> branch=<b>` or `refused pr=<n> reason=<why>`, then
#   `summary closed=<n> refused=<n>`.
# @exitcode 0 Every selected row was closed.
# @exitcode 1 A `gh` read failed (nothing was closed) or a close failed (the lines say which were closed).
# @exitcode 2 Refused: usage, the table's path or shape, no selected row, or at least one row refused (its line
#   says why; the other rows were closed).
# @example
#   ~/.local/bin/common/pr-close.sh --from-table .orchestration/orchestrate/regime-cutover/handouts/cleanup-table.md
#   ~/.local/bin/common/pr-close.sh --from-table .orchestration/orchestrate/regime-cutover/handouts/cleanup-table.md --only 378
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

lever='pr-close.sh'
usage='usage: pr-close.sh --from-table <table.md> [--only <pr>]'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
header='| PR | branch | opened | files | title | default |'
# The `## Open pull requests` rows as `<pr>\t<branch>\t<default>`; exit 3 for a missing section or header, 4 for a
# row without a `#<n>` PR cell or a backticked branch cell. `\|` inside a cell is text, not a separator.
# shellcheck disable=SC2016 # awk source, not shell
table_awk='
function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
/^## / { if (in_section) { done = 1 } in_section = ($0 == "## Open pull requests"); next }
!in_section || done { next }
/^[ \t]*$/ { if (rows) { done = 1 } next }
!seen_header { if ($0 != header) { exit 3 } seen_header = 1; next }
/^\|( *:?-+:? *\|)+ *$/ { next }
{
    line = $0
    gsub(/\\\|/, "\001", line)
    n = split(line, cell, "|")
    if (n != 8 || trim(cell[1]) != "" || trim(cell[8]) != "") { exit 4 }
    pr = trim(cell[2]); branch = trim(cell[3]); text = trim(cell[7])
    gsub(/\001/, "|", text); gsub(/\t/, " ", text)
    if (pr !~ /^#[1-9][0-9]*$/ || branch !~ /^`[A-Za-z0-9._\/-]+`$/) { exit 4 }
    rows++
    print substr(pr, 2) "\t" substr(branch, 2, length(branch) - 2) "\t" text
}
END { if (!seen_header) { exit 3 } }
'

# @description Print the refusal on stderr and exit 2; nothing was written to GitHub.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print the failure on stderr and exit 1.
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

table=''
only=''
while (($#)); do
    case $1 in
    --from-table)
        (($# >= 2)) || refuse "${usage}"
        table=$2
        shift 2
        ;;
    --only)
        (($# >= 2)) || refuse "${usage}"
        only=$2
        shift 2
        ;;
    *) refuse "${usage}" ;;
    esac
done
[[ -n ${table} ]] || refuse "${usage}"
[[ -z ${only} || ${only} =~ ^[1-9][0-9]{0,9}$ ]] || refuse "--only is not a decimal number: ${only}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'

toplevel=$(git rev-parse --show-toplevel 2> /dev/null) || refuse 'not in a git checkout'
toplevel=$(cd "${toplevel}" && pwd -P) || refuse "cannot resolve ${toplevel}"
git_dir=$(git rev-parse --path-format=absolute --git-dir) || refuse 'cannot read the git directory'
common_dir=$(git rev-parse --path-format=absolute --git-common-dir) || refuse 'cannot read the git common directory'
git_dir=$(cd "${git_dir}" && pwd -P) || refuse "cannot resolve ${git_dir}"
common_dir=$(cd "${common_dir}" && pwd -P) || refuse "cannot resolve ${common_dir}"
[[ ${git_dir} == "${common_dir}" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse "${toplevel} is a linked worktree; run from the main checkout, where the orchestrator writes its tables"
[[ -f ${table} && ! -L ${table} ]] || refuse "the table is not a regular file: ${table}"
case ${table} in
*/*) table_dir=${table%/*} ;;
*) table_dir=. ;;
esac
[[ -n ${table_dir} ]] || table_dir=/
table_dir=$(cd "${table_dir}" && pwd -P) || refuse "cannot resolve the directory of ${table}"
handouts='^/.+/\.orchestration/orchestrate/[A-Za-z0-9][A-Za-z0-9._-]*/handouts$'
[[ ${table_dir} =~ ${handouts} && ${table_dir} == "${toplevel}/.orchestration/orchestrate/"* ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse "the table is not under ${toplevel}/.orchestration/orchestrate/<program>/handouts/: ${table_dir}"

status=0
rows=$(awk -v header="${header}" "${table_awk}" "${table_dir}/${table##*/}") || status=$?
case ${status} in
0) ;;
3) refuse "no '## Open pull requests' section with the header ${header} in ${table}" ;;
4) refuse "a row of '## Open pull requests' in ${table} has no #<n> PR cell or backticked branch cell" ;;
*) refuse "cannot read ${table} (awk exited ${status})" ;;
esac

selected=()
while IFS=$'\t' read -r pr branch text; do
    [[ -n ${pr} && ${text} == close:* ]] || continue
    [[ -z ${only} || ${pr} == "${only}" ]] || continue
    selected+=("${pr}"$'\t'"${branch}"$'\t'"${text}")
done <<< "${rows}"
if ((${#selected[@]} == 0)); then
    [[ -n ${only} ]] && refuse "the table has no close: row for pull request ${only}"
    refuse "the table has no row whose default starts with close:"
fi

closable=()
refused=0
for row in "${selected[@]}"; do
    IFS=$'\t' read -r pr branch text <<< "${row}"
    view=$(gh_bounded pr view "${pr}" --json state,headRefName --jq '[.state, .headRefName] | @tsv') ||
        fail "cannot read pull request ${pr}; nothing was closed"
    IFS=$'\t' read -r state head <<< "${view}"
    if [[ ${state} != OPEN ]]; then
        echo "refused pr=${pr} reason=state ${state:-unreadable}, not OPEN"
        refused=$((refused + 1))
        continue
    fi
    if [[ ${head} != "${branch}" ]]; then
        echo "refused pr=${pr} reason=head branch ${head} is not the table's ${branch}"
        refused=$((refused + 1))
        continue
    fi
    sharing=$(gh_bounded pr list --state open --head "${branch}" --json number --jq '[.[].number | tostring] | join(",")') ||
        fail "cannot list the open pull requests of ${branch}; nothing was closed"
    if [[ ${sharing} != "${pr}" ]]; then
        echo "refused pr=${pr} reason=branch ${branch} is the head of open pull requests ${sharing:-none}"
        refused=$((refused + 1))
        continue
    fi
    closable+=("${row}")
done

closed=0
for row in ${closable[@]+"${closable[@]}"}; do
    IFS=$'\t' read -r pr branch text <<< "${row}"
    gh_bounded pr close "${pr}" --comment "${text}" >&2 || {
        echo "summary closed=${closed} refused=${refused}"
        fail "gh pr close ${pr} failed after ${closed} closed"
    }
    echo "closed pr=${pr} branch=${branch}"
    closed=$((closed + 1))
done
echo "summary closed=${closed} refused=${refused}"
((refused == 0)) || exit 2
