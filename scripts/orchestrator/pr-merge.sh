#!/usr/bin/env bash
# @file pr-merge.sh
# @brief Squash-merge a pull request only at a head the program's ledger records as `correct` and CI passed, the orchestrator seat's merge lever.
# @description
#   Regime-cutover U71 (finding F010), the orchestrator seat's only merge path: `home/dot_agents/omp/policies/orchestrator.yml`
#   allows `~/.local/bin/common/pr-merge.sh *` and denies the `gh pr merge` command text (a speed bump: text rows do
#   not stop a glob spelling; a seat running `gh` itself is the residual unit U88 removes). `<pr>` is decimal and
#   checked before the first `gh` call. The lever runs in the main checkout (a linked worktree is refused) and reads
#   only that checkout's store: `<toplevel>/.orchestration/orchestrate/<program>/ledger.tsv` (header
#   `ts unit pr head_sha verdict verifier evidence`), `<program>` taken from the pull request body's one
#   `Program-Unit: <program>/U<n>` line, no directory of that chain nor the ledger a symlink, each owned by this user;
#   `--records` must resolve (`pwd -P`) to exactly that store, so a ledger written anywhere else is never read. It reads
#   `gh pr view <pr> --json state,baseRefName,headRefOid,isDraft` and refuses unless the pull request is `OPEN`, not a
#   draft and based on `main`. The verdict is the newest `ledger.tsv` row whose `pr` is `<pr>` and whose `head_sha` is
#   the full 40-hex sha it judged (a short sha never matches): it must start with the word `correct`, so a later
#   `incorrect` or `blocked` row for the same head voids an earlier `correct`. Without `--carry-from` that sha is the
#   head itself. With `--carry-from <sha>` (`preferences.md` standing order 18: a `pr-update-branch.sh` merge from main
#   does not void a verdict while the diff against main is unchanged) the row is the one for `<sha>`, which must be an
#   ancestor of the head, and the lever fetches `main` and `refs/pull/<pr>/head` into `refs/pr-merge/<pr>/` and
#   compares the raw tree diff (`git diff-tree -r --raw --no-abbrev`, full blob ids and modes of every changed path,
#   run at the top level with `--no-relative` and the other settings-sensitive options pinned) of each commit against
#   its merge base with main: any byte of difference is a refusal, whatever the caller's cwd or git configuration.
#   CI is `gh pr checks <pr> --json bucket,name` between two reads of `headRefOid` that must both equal
#   the head: at least one check, every bucket `pass` or `skipping`, and `gh` exiting 0; a pending, failed or
#   cancelled check is a refusal. The one write is `gh pr merge <pr> --squash --match-head-commit <head>`, so GitHub
#   refuses the merge if the head moved after these reads; it never passes `--admin`, `--auto` or
#   `--delete-branch`. After the merge, or after a merge error, `gh pr view <pr> --json state,mergeCommit` decides:
#   `MERGED` prints the receipt (the merge happened; never run the merge twice), anything else is a failure. The
#   thread check (`pr-threads-check.sh`) stays a separate step before this lever (`hcom-orchestration` SKILL step 6).
#   Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
# @arg $1 int The pull request number.
# @option --records <dir> The program store holding `ledger.tsv` (required; must be the checkout's own store, above).
# @option --carry-from <sha> The audited earlier head (40 hex) whose `correct` row carries to the current head.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `merged pr=<pr> head=<head> commit=<merge commit> verdict=<ledger row ts> carried-from=<sha or ->`.
# @exitcode 0 The pull request is merged at the head.
# @exitcode 1 A `gh` or `git` read, or the merge, failed.
# @exitcode 2 Refused: usage, the pull request's state, no `correct` row for the head, a carry whose diff changed,
#   or CI that is not green on the head.
# @example
#   ~/.local/bin/common/pr-merge.sh 480 --records .orchestration/orchestrate/regime-cutover
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

# Object substitution (U71 audit round 6): the git common directory is shared with, and writable by, the worker seats
# (U85), so a planted `refs/replace/*` ref, an `info/grafts` file, an alternate object store or a forged commit-graph
# could make the objects git reads here differ from the sha GitHub reports. Every git call of this lever, and every
# process it starts, runs with replace objects off (`GIT_NO_REPLACE_OBJECTS`, and `--no-replace-objects` through the
# `git` function), grafts read from /dev/null, the commit-graph off, and none of the caller's object-store or
# repository-location variables; `git_objects_guard` refuses a checkout that holds grafts, alternates or a shallow cut.
unset GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_OBJECT_DIRECTORY GIT_REPLACE_REF_BASE GIT_DIR GIT_WORK_TREE GIT_COMMON_DIR \
    GIT_INDEX_FILE GIT_NAMESPACE GIT_CONFIG_PARAMETERS
export GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false

# @description Run git with replace objects and the commit-graph off, whatever the caller's environment or config.
# @arg $@ string The git arguments.
git() {
    command git --no-replace-objects -c core.commitGraph=false "$@"
}

lever='pr-merge.sh'
usage='usage: pr-merge.sh <pr> --records <dir> [--carry-from <sha>]'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
ledger_header=$'ts\tunit\tpr\thead_sha\tverdict\tverifier\tevidence'
# The body's program marker, the grammar regime-ci.py and pr-body-edit.sh read.
program_unit_re='^Program-Unit: ([a-z0-9][a-z0-9_-]{0,63})/U[0-9]+$'

# A verdict column that starts with the word `correct` (never `incorrect`): `correct`, `correct (…)`, `correct;…`.
correct_re='^correct($|[[:space:](;,])'

# @description Print the refusal on stderr and exit 2; nothing was merged.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print the failure on stderr and exit 1: a read or the merge failed.
# @arg $@ string The reason.
fail() {
    echo "${lever}: $*" >&2
    exit 1
}

# @description Refuse unless the git common directory of checkout $1 holds no grafts file, no non-empty alternates
#   file and no shallow file: each would substitute or cut the objects this lever reads (U71 audit round 6).
# @arg $1 path The checkout.
git_objects_guard() {
    local common path
    common=$(git -C "$1" rev-parse --path-format=absolute --git-common-dir) || refuse "cannot read the git common directory of $1"
    [[ -d ${common} ]] || refuse "the git common directory ${common} is no directory"
    for path in "${common}/info/grafts" "${common}/shallow"; do
        [[ ! -e ${path} && ! -L ${path} ]] || refuse "${path} exists; it rewrites the history this lever reads"
    done
    path=${common}/objects/info/alternates
    [[ ! -L ${path} && ! -s ${path} ]] || refuse "${path} names alternate object stores; this lever reads only the checkout's own objects"
}
# @description Run `gh` with its wait bounded by PR_LEVER_GH_TIMEOUT seconds.
# @arg $@ string The `gh` arguments.
gh_bounded() {
    perl -e 'alarm shift; exec @ARGV or die "exec gh: $!\n"' "${gh_timeout}" gh "$@"
}

# @description Print `<ts>\t<verdict>` of the newest ledger row for pull request $1 at the full sha $2, or nothing
#   when no row names that pair. A ledger whose first line is not the header is a refusal; a failed read exits 1.
#   Both sides of every comparison are strings (`""` appended): awk compares two numeric-looking values as numbers,
#   so two different all-digit shas would otherwise match (U71 audit round 1).
# @arg $1 int The pull request number.
# @arg $2 string The 40-hex head sha.
ledger_verdict() {
    local out status=0
    out=$(LEDGER_HEADER=${ledger_header} awk -F'\t' -v pr="$1" -v sha="$2" '
        { sub(/\r$/, "") }
        NR == 1 { if ($0 != ENVIRON["LEDGER_HEADER"]) { bad = 1; exit 3 } next }
        ($3 "") == (pr "") && ($4 "") == (sha "") { found = $1 "\t" $5 }
        END { if (!bad && found != "") print found }
    ' "${ledger}") || status=$?
    case ${status} in
    0) printf '%s' "${out}" ;;
    3) refuse "${ledger} does not start with the ledger header (${ledger_header//$'\t'/ })" ;;
    *) fail "cannot read ${ledger}" ;;
    esac
}

# @description Refuse unless the newest ledger row for pull request ${pr} at sha $1 is `correct`.
# @arg $1 string The 40-hex sha the verdict must name.
# @set verdict_ts The row's ts.
require_correct_row() {
    local row verdict
    row=$(ledger_verdict "${pr}" "$1") || exit $?
    [[ -n ${row} ]] || refuse "${ledger} has no row for pull request ${pr} at head ${1} (a short sha never matches)"
    verdict_ts=${row%%$'\t'*}
    verdict=${row#*$'\t'}
    [[ ${verdict} =~ ${correct_re} ]] ||
        refuse "the newest ${ledger} row for pull request ${pr} at ${1} (${verdict_ts}) is not correct: ${verdict}"
}

# @description Run git at the repository's top level, whatever the caller's cwd.
# @arg $@ string The git arguments.
git_top() {
    git -C "${toplevel}" "$@"
}

# @description Write the raw tree diff from the merge base with main to commit $1 (NUL-separated, full object ids:
#   modes, blob ids, status and path of every changed entry) to file $2. It is plumbing (`diff-tree`) run at the top
#   level with every option that a user or repository setting could change spelled out (`--no-relative`,
#   `--no-renames`, `--ignore-submodules=none`, `-O/dev/null` against `diff.orderFile`), so neither `diff.relative`,
#   a subdirectory cwd, rename detection, an external diff nor a textconv driver can hide a changed path
#   (U71 audit round 2).
# @arg $1 string The commit.
# @arg $2 path The output file.
diff_against_main() {
    local base
    base=$(git_top merge-base "refs/pr-merge/${pr}/main" "$1") || fail "git merge-base main $1 failed"
    git_top diff-tree -r -z --raw --no-abbrev --no-renames --no-relative --ignore-submodules=none -O/dev/null \
        "${base}" "$1" > "$2" || fail "git diff-tree ${base} $1 failed"
}

# @description Set `ledger` to the one store the merge may read (U71, bot P1 4370212009: a caller-chosen ledger.tsv
#   could hold a fabricated row): `<toplevel>/.orchestration/orchestrate/<program>/ledger.tsv` of this main checkout,
#   `<program>` taken from the pull request body's one `Program-Unit: <program>/U<n>` line. No directory from the
#   checkout down and not the ledger is a symlink, each is owned by this user, and `--records` must resolve
#   (`pwd -P`) to exactly that directory; anything else is a refusal.
# @set ledger The canonical ledger path.
resolve_store() {
    local body markers line program path given part
    body=$(gh_bounded pr view "${pr}" --json body --jq .body) || fail "cannot read the body of pull request ${pr}"
    markers=''
    while IFS= read -r line; do
        line=${line%$'\r'}
        [[ ${line} == Program-Unit:* ]] && markers+="${line}"$'\n'
    done <<< "${body}"
    markers=${markers%$'\n'}
    [[ -n ${markers} && ${markers} != *$'\n'* && ${markers} =~ ${program_unit_re} ]] ||
        refuse "the body of pull request ${pr} must hold exactly one line 'Program-Unit: <program>/U<n>'; it holds: ${markers:-none}"
    program=${BASH_REMATCH[1]}
    path=${toplevel}
    for part in .orchestration orchestrate "${program}"; do
        path=${path}/${part}
        [[ -d ${path} && ! -L ${path} && -O ${path} ]] ||
            refuse "${path} is not a directory of this user (a symlink or a missing store); the merge reads only the checkout's own store"
    done
    given=$(cd "${records}" 2> /dev/null && pwd -P) || refuse "--records ${records} is no directory"
    [[ ${given} == "${path}" ]] || # lint-comparisons: allow both sides are pwd -P forms
        refuse "--records ${records} is not the program's store ${path} (named by the body's Program-Unit line)"
    ledger=${path}/ledger.tsv
    [[ -f ${ledger} && ! -L ${ledger} && -O ${ledger} && -r ${ledger} ]] ||
        refuse "${ledger} is not a readable regular file of this user"
}

[[ $# -ge 1 ]] || refuse "${usage}"
pr=$1
shift
[[ ${pr} =~ ^[1-9][0-9]{0,9}$ ]] || refuse "the pull request is not a decimal number: ${pr}"
records=''
carry=''
while [[ $# -gt 0 ]]; do
    case $1 in
    --records | --carry-from)
        [[ $# -ge 2 && -n $2 ]] || refuse "${usage}"
        if [[ $1 == --records ]]; then records=$2; else carry=$2; fi
        shift 2
        ;;
    *) refuse "${usage}" ;;
    esac
done
[[ -n ${records} ]] || refuse "${usage}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'
[[ -z ${carry} || ${carry} =~ ^[0-9a-f]{40}$ ]] || refuse "--carry-from must be a full 40-hex sha: ${carry}"
# The checkout the lever runs in, by its physical path, and it must be the main checkout: a linked worktree (a
# worker's clone) holds a copy of the store that is not the orchestrator's record (U71, bot P1 4370212009).
toplevel=$(git rev-parse --show-toplevel 2> /dev/null) || refuse 'run from the repository checkout that holds the program store'
[[ -n ${toplevel} && -d ${toplevel} ]] || refuse 'run from the repository checkout that holds the program store'
toplevel=$(cd "${toplevel}" && pwd -P) || refuse "cannot resolve ${toplevel}"
git_objects_guard "${toplevel}"
git_dir=$(git_top rev-parse --absolute-git-dir) || refuse 'cannot read the git directory'
common_dir=$(git_top rev-parse --path-format=absolute --git-common-dir) || refuse 'cannot read the git common directory'
git_dir=$(cd "${git_dir}" && pwd -P) || refuse "cannot resolve ${git_dir}"
common_dir=$(cd "${common_dir}" && pwd -P) || refuse "cannot resolve ${common_dir}"
[[ ${git_dir} == "${common_dir}" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse "${toplevel} is a linked worktree; run from the main checkout, where the orchestrator keeps its store"

view=$(gh_bounded pr view "${pr}" --json state,baseRefName,headRefOid,isDraft \
    --jq '[.state, .baseRefName, .headRefOid, (.isDraft | tostring)] | @tsv') || fail "cannot read pull request ${pr}"
IFS=$'\t' read -r state base head draft <<< "${view}"
[[ ${state} == OPEN ]] || refuse "pull request ${pr} is ${state:-unreadable}, not OPEN"
[[ ${base} == main ]] || refuse "pull request ${pr} targets ${base:-nothing}, not main"
[[ ${draft} == false ]] || refuse "pull request ${pr} is a draft (isDraft=${draft:-unreadable})"
[[ ${head} =~ ^[0-9a-f]{40}$ ]] || fail "pull request ${pr} has no readable head: ${head}"
resolve_store

if [[ -z ${carry} ]]; then
    require_correct_row "${head}"
else
    [[ ${carry} != "${head}" ]] || refuse "--carry-from ${carry} is the head itself; drop --carry-from"
    require_correct_row "${carry}"
    perl -e 'alarm shift; exec @ARGV or die "exec git: $!\n"' "${gh_timeout}" git --no-replace-objects -C "${toplevel}" fetch -q --no-tags origin \
        "+refs/heads/main:refs/pr-merge/${pr}/main" "+refs/pull/${pr}/head:refs/pr-merge/${pr}/head" ||
        fail "git fetch of main and refs/pull/${pr}/head failed"
    fetched=$(git_top rev-parse --verify --quiet "refs/pr-merge/${pr}/head^{commit}") || fetched=''
    [[ ${fetched} == "${head}" ]] || refuse "refs/pull/${pr}/head is ${fetched:-unreadable}, the pull request's head is ${head}"
    git_top cat-file -e "${carry}^{commit}" 2> /dev/null || refuse "--carry-from ${carry} is no commit in this checkout"
    status=0
    git_top merge-base --is-ancestor "${carry}" "${head}" || status=$?
    case ${status} in
    0) ;;
    1) refuse "--carry-from ${carry} is not an ancestor of the head ${head}" ;;
    *) fail "git merge-base --is-ancestor ${carry} ${head} failed" ;;
    esac
    scratch=$(mktemp -d "${TMPDIR:-/tmp}/pr-merge.XXXXXX") || fail 'mktemp failed'
    trap 'rm -f "${scratch}/audited.diff" "${scratch}/head.diff"; rmdir "${scratch}"' EXIT
    diff_against_main "${carry}" "${scratch}/audited.diff"
    diff_against_main "${head}" "${scratch}/head.diff"
    status=0
    cmp -s "${scratch}/audited.diff" "${scratch}/head.diff" || status=$?
    case ${status} in
    0) ;;
    1) refuse "the diff against main of ${head} differs from the audited ${carry}; the carry does not hold (standing order 18)" ;;
    *) fail "cmp of the two diffs failed" ;;
    esac
fi

status=0
checks=$(gh_bounded pr checks "${pr}" --json bucket,name --jq '.[] | [.bucket, .name] | @tsv') || status=$?
again=$(gh_bounded pr view "${pr}" --json headRefOid --jq .headRefOid) || fail "cannot read the head of ${pr} again"
[[ ${again} == "${head}" ]] || refuse "the head of pull request ${pr} moved from ${head} to ${again:-unreadable} during the checks"
[[ -n ${checks} ]] || {
    ((status == 0)) && refuse "no check is reported on the head ${head}"
    fail "gh pr checks ${pr} failed (exit ${status}) and printed nothing"
}
red=''
while IFS=$'\t' read -r bucket name; do
    case ${bucket} in
    pass | skipping) ;;
    *) red+="${red:+, }${name}=${bucket}" ;;
    esac
done <<< "${checks}"
[[ -z ${red} ]] || refuse "CI is not green on the head ${head}: ${red}"
((status == 0)) || fail "gh pr checks ${pr} exited ${status} although every listed check passed"

merge_status=0
gh_bounded pr merge "${pr}" --squash --match-head-commit "${head}" >&2 || merge_status=$?
after=$(gh_bounded pr view "${pr}" --json state,mergeCommit --jq '[.state, (.mergeCommit.oid // "")] | @tsv') ||
    fail "cannot read pull request ${pr} after the merge command (exit ${merge_status}); read it before anything else"
IFS=$'\t' read -r state commit <<< "${after}"
[[ ${state} == MERGED && ${commit} =~ ^[0-9a-f]{40}$ ]] ||
    fail "pull request ${pr} is ${state:-unreadable} after the merge command (exit ${merge_status})"
((merge_status == 0)) || echo "${lever}: the merge command exited ${merge_status}, but the pull request is MERGED" >&2
echo "merged pr=${pr} head=${head} commit=${commit} verdict=${verdict_ts} carried-from=${carry:--}"
