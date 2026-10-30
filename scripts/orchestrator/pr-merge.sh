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
#   `incorrect` or `blocked` row for the same head voids an earlier `correct`. That sha is always the current head:
#   there is no carry-over (U71 audit round 10), so a head that `pr-update-branch.sh` moved gets a fresh audit. The
#   lever reads no local git objects or refs; it decides from `gh` reads and the ledger alone, and git only names the
#   checkout (`rev-parse --show-toplevel`, `--absolute-git-dir`, `--git-common-dir`). CI is `gh pr checks <pr> --json bucket,name` between two reads of `headRefOid` that must both equal
#   the head (and whose second read must still report base `main`: `--match-head-commit` pins only the head): at least
#   one check, every bucket `pass` or `skipping`, and `gh` exiting 0; a pending, failed or
#   cancelled check is a refusal. The one write is `gh pr merge <pr> --squash --match-head-commit <head>`, so GitHub
#   refuses the merge if the head moved after these reads; it never passes `--admin`, `--auto` or
#   `--delete-branch`. After the merge, or after a merge error, `gh pr view <pr> --json
#   state,mergeCommit,baseRefName,headRefOid` decides: `MERGED` into `main` at the audited head prints the receipt (the
#   merge happened; never run the merge twice); another state, another base, or another merged head (a merge someone
#   else made after the pinned one failed) is a failure with no receipt that names both shas. The
#   thread check (`pr-threads-check.sh`) stays a separate step before this lever (`hcom-orchestration` SKILL step 6).
#   Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
# @arg $1 int The pull request number.
# @option --records <dir> The program store holding `ledger.tsv` (required; must be the checkout's own store, above).
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `merged pr=<pr> head=<head> commit=<merge commit> verdict=<ledger row ts>`.
# @exitcode 0 The pull request is merged at the head.
# @exitcode 1 A `gh` or `git` read, or the merge, failed.
# @exitcode 2 Refused: usage, the pull request's state, no `correct` row for the head, or CI that is not green on the
#   head.
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
# The isolated git and the environment scrub come from the library beside this script (U113). The checkout is named
# from the cwd alone: a caller's repository-location variables could point git at another checkout's store (U71), so
# every GIT_* and transport variable goes before the first git.
[[ -r ${LEVER_DIR}/git-isolated.sh ]] || {
    echo "pr-merge.sh: refused: git-isolated.sh unreadable beside this script: ${LEVER_DIR}/git-isolated.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/git-isolated.sh
. "${LEVER_DIR}/git-isolated.sh"
# shellcheck disable=SC2119 # no name is kept: every GIT_* and transport variable goes
git_env_scrub

[[ -r ${LEVER_DIR}/read-lib.sh ]] || {
    echo "pr-merge.sh: refused: read-lib.sh unreadable beside this script: ${LEVER_DIR}/read-lib.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/read-lib.sh
. "${LEVER_DIR}/read-lib.sh"

lever='pr-merge.sh'
usage='usage: pr-merge.sh <pr> --records <dir>'
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
[[ $# -eq 2 && $1 == --records && -n $2 ]] || refuse "${usage}"
records=$2
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'
# The checkout the lever runs in, by its physical path, and it must be the main checkout: a linked worktree (a
# worker's clone) holds a copy of the store that is not the orchestrator's record (U71, bot P1 4370212009).
toplevel=$(git_isolated rev-parse --show-toplevel 2> /dev/null) || refuse 'run from the repository checkout that holds the program store'
[[ -n ${toplevel} && -d ${toplevel} ]] || refuse 'run from the repository checkout that holds the program store'
toplevel=$(cd "${toplevel}" && pwd -P) || refuse "cannot resolve ${toplevel}"
git_dir=$(git_isolated -C "${toplevel}" rev-parse --absolute-git-dir) || refuse 'cannot read the git directory'
common_dir=$(git_isolated -C "${toplevel}" rev-parse --path-format=absolute --git-common-dir) ||
    refuse 'cannot read the git common directory'
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

require_correct_row "${head}"

status=0
checks=$(gh_bounded pr checks "${pr}" --json bucket,name --jq '.[] | [.bucket, .name] | @tsv') || status=$?
# The second read checks the base as well as the head (U71 audit round 7): `--match-head-commit` pins only the head,
# and a pull request retargeted from main with the same head would otherwise merge into the new base.
again=$(gh_bounded pr view "${pr}" --json headRefOid,baseRefName --jq '[.headRefOid, .baseRefName] | @tsv') ||
    fail "cannot read the head and base of ${pr} again"
IFS=$'\t' read -r again again_base <<< "${again}"
[[ ${again} == "${head}" ]] || refuse "the head of pull request ${pr} moved from ${head} to ${again:-unreadable} during the checks"
[[ ${again_base} == main ]] || refuse "pull request ${pr} was retargeted from main to ${again_base:-unreadable} during the checks"
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
after=$(gh_bounded pr view "${pr}" --json state,mergeCommit,baseRefName,headRefOid \
    --jq '[.state, (.mergeCommit.oid // ""), .baseRefName, .headRefOid] | @tsv') ||
    fail "cannot read pull request ${pr} after the merge command (exit ${merge_status}); read it before anything else"
IFS=$'\t' read -r state commit merged_base merged_head <<< "${after}"
[[ ${state} == MERGED && ${commit} =~ ^[0-9a-f]{40}$ ]] ||
    fail "pull request ${pr} is ${state:-unreadable} after the merge command (exit ${merge_status})"
# A merge this lever did not make (U71 audit round 9): when the pinned merge failed and someone else merged a later
# head, MERGED alone would credit the audited head with that merge, so the merged head must be the audited one.
[[ ${merged_head} == "${head}" ]] ||
    fail "pull request ${pr} merged at head ${merged_head:-unreadable} as ${commit}, not at the audited head ${head} (merge command exit ${merge_status}); that merge is not this verdict's; tell the operator"
# gh pr merge takes no base (`gh pr merge --help`), so a retarget between the second read and the merge call is
# reported here, loudly, with the base it landed on; it cannot be undone by the lever.
[[ ${merged_base} == main ]] ||
    fail "pull request ${pr} merged into ${merged_base:-an unreadable base}, not main: it was retargeted after the last read; tell the operator"
((merge_status == 0)) || echo "${lever}: the merge command exited ${merge_status}, but the pull request is MERGED" >&2
echo "merged pr=${pr} head=${head} commit=${commit} verdict=${verdict_ts}"
