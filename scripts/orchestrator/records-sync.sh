#!/usr/bin/env bash
# @file records-sync.sh
# @brief Carry the program's records from the main checkout to a `records/sync-<n>` pull request.
# @description
#   Regime-cutover U28 (ADDENDUM), the orchestrator seat's lever, allowed by the row
#   `~/.local/bin/common/records-sync.sh *` of `home/dot_agents/omp/policies/orchestrator.yml` (the seat's own
#   `git push` and `gh pr create` stay denied). It runs in the main checkout, where the orchestrator writes its
#   records (a linked worktree is refused). The copy set is the tracked changes against `HEAD` (`git diff
#   --name-only HEAD`) and the untracked, not ignored files (`git ls-files --others --exclude-standard`) under
#   `.orchestration/orchestrate/<program>/` and `.orchestration/validation/`; every path must lie under
#   `.orchestration/` and be a regular file or a deletion (a symlink is refused, since its target could lie
#   anywhere), else the run is refused before anything is created. `<n>` is one more than the largest number
#   among the remote heads and the heads of the newest 1000 pull requests named `records/sync-<n>`, `records/program-store-<n>` or
#   `records/<program>-sync-<n>` (the earlier syncs), and the branch must match `records/sync-<n>`. In a new
#   worktree under `$TMPDIR` on that branch from `origin/main` it copies the set, masks the copies with the
#   worktree's own `scripts/validate-agent-assets.py --mask-secrets` (the checkout's files are never changed;
#   a masking failure aborts), refuses a staged path outside `.orchestration/`, commits
#   `chore(records): <program> sync <n>` with the footer, pushes that branch only, and opens the pull request
#   with `gh pr create --base main --head records/sync-<n> --title ... --body-file ...`; the body lists the
#   `units.tsv` ids and the `decisions.tsv` timestamps the sync adds or changes and, with `--unit`, the line
#   `Program-Unit: <program>/<unit>`. The worktree is removed on every exit (`git worktree remove --force`, only
#   on the path this run created; the branch stays). Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds.
# @option --base <ref> The start point; only `origin/main` (the default) is accepted.
# @option --program <name> The program directory under `.orchestration/orchestrate/`; default: the only one.
# @option --unit <U<n>> The unit the body's `Program-Unit:` line names (the records unit, U20 for regime-cutover).
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `synced branch=records/sync-<n> files=<n> pr=<url>`.
# @exitcode 0 The pull request was opened.
# @exitcode 1 A `git` or `gh` step, or the masking, failed; nothing was pushed unless the receipt says so.
# @exitcode 2 Refused: usage, a linked worktree, the program, the copy set, or nothing to sync.
# @example
#   ~/.local/bin/common/records-sync.sh --program regime-cutover --unit U20
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

lever='records-sync.sh'
usage='usage: records-sync.sh [--base origin/main] [--program <name>] [--unit U<n>]'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
footer='Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>'
pr_footer='🤖 Generated with [Claude Code](https://claude.com/claude-code)'

# @description Print the refusal on stderr and exit 2.
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

# @description Remove the worktree this run created, and its scratch directory.
cleanup() {
    if [[ -n ${scratch:-} && -d ${scratch} ]]; then
        if [[ -d ${scratch}/tree ]]; then
            git -C "${toplevel}" worktree remove --force "${scratch}/tree" > /dev/null 2>&1 ||
                echo "${lever}: could not remove the worktree ${scratch}/tree" >&2
        fi
        rm -r "${scratch}" 2> /dev/null || echo "${lever}: could not remove ${scratch}" >&2
    fi
}

base=origin/main
program=''
unit=''
while (($#)); do
    case $1 in
    --base | --program | --unit)
        (($# >= 2)) || refuse "${usage}"
        case $1 in
        --base) base=$2 ;;
        --program) program=$2 ;;
        --unit) unit=$2 ;;
        esac
        shift 2
        ;;
    *) refuse "${usage}" ;;
    esac
done
[[ ${base} == origin/main ]] || refuse "--base accepts only origin/main: ${base}"
[[ -z ${unit} || ${unit} =~ ^U[0-9]+$ ]] || refuse "--unit is not a plain unit id U<n>: ${unit}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'

toplevel=$(git rev-parse --show-toplevel 2> /dev/null) || refuse 'not in a git checkout'
git_dir=$(git rev-parse --path-format=absolute --git-dir) || refuse 'cannot read the git directory'
common_dir=$(git rev-parse --path-format=absolute --git-common-dir) || refuse 'cannot read the git common directory'
git_dir=$(cd "${git_dir}" && pwd -P) || refuse "cannot resolve ${git_dir}"
common_dir=$(cd "${common_dir}" && pwd -P) || refuse "cannot resolve ${common_dir}"
[[ ${git_dir} == "${common_dir}" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse "${toplevel} is a linked worktree; run from the main checkout, where the orchestrator writes its records"
cd "${toplevel}" || refuse "cannot enter ${toplevel}"
if [[ -z ${program} ]]; then
    programs=()
    for dir in .orchestration/orchestrate/*/; do
        dir=${dir%/}
        [[ -d ${dir} ]] && programs+=("${dir##*/}")
    done
    ((${#programs[@]} == 1)) || refuse "name the program with --program; .orchestration/orchestrate/ holds ${#programs[@]}"
    program=${programs[0]}
fi
[[ ${program} =~ ^[a-z0-9][a-z0-9_-]*$ ]] || refuse "the program name is outside [a-z0-9][a-z0-9_-]*: ${program}"
[[ -d .orchestration/orchestrate/${program} && ! -L .orchestration/orchestrate/${program} ]] ||
    refuse "no program directory .orchestration/orchestrate/${program}"
dirs=(".orchestration/orchestrate/${program}/" .orchestration/validation/)

changed=$(git diff --name-only -z HEAD -- "${dirs[@]}" | tr '\0' '\n') || fail 'git diff --name-only HEAD failed'
untracked=$(git ls-files -z --others --exclude-standard -- "${dirs[@]}" | tr '\0' '\n') || fail 'git ls-files --others failed'
listed=$(printf '%s\n%s\n' "${changed}" "${untracked}" | sort -u) || fail 'cannot list the copy set'
files=()
while IFS= read -r path; do
    [[ -n ${path} ]] || continue
    case ${path} in
    .orchestration/*) ;;
    *) refuse "a path of the copy set is outside .orchestration/: ${path}" ;;
    esac
    [[ ${path} != *..* ]] || refuse "a path of the copy set holds '..': ${path}"
    [[ ! -L ${path} ]] || refuse "a path of the copy set is a symlink: ${path}"
    [[ ! -e ${path} || -f ${path} ]] || refuse "a path of the copy set is not a regular file: ${path}"
    files+=("${path}")
done <<< "${listed}"
((${#files[@]} > 0)) || refuse "nothing to sync under ${dirs[*]}"

remote_heads=$(git ls-remote --heads origin 'refs/heads/records/*') || fail 'git ls-remote origin failed'
pr_heads=$(gh_bounded pr list --state all --limit 1000 --json headRefName --jq '.[].headRefName') ||
    fail 'gh pr list failed'
last=$(printf '%s\n%s\n' "${remote_heads}" "${pr_heads}" |
    PROGRAM=${program} awk '{ ref = $NF; sub(/^refs\/heads\//, "", ref) }
        ref ~ "^records/(sync|program-store|" ENVIRON["PROGRAM"] "-sync)-[0-9]+$" { n = ref; sub(/.*-/, "", n); if (n + 0 > max) max = n + 0 }
        END { print max + 0 }') || fail 'cannot number the sync'
n=$((last + 1))
branch=records/sync-${n}
[[ ${branch} =~ ^records/sync-[1-9][0-9]*$ ]] || refuse "the branch is outside records/sync-<n>: ${branch}"

git fetch --quiet origin main || fail 'git fetch origin main failed'
scratch=$(mktemp -d "${TMPDIR:-/tmp}/records-sync.XXXXXX") || fail 'mktemp failed'
trap cleanup EXIT
tree=${scratch}/tree
git worktree add --quiet -b "${branch}" "${tree}" "${base}" || fail "git worktree add ${branch} failed"
masked=()
for path in "${files[@]}"; do
    if [[ -e ${path} ]]; then
        mkdir -p "${tree}/${path%/*}" || fail "mkdir for ${path} failed"
        cp -p "${path}" "${tree}/${path}" || fail "cp ${path} failed"
        masked+=("${tree}/${path}")
    elif [[ -e ${tree}/${path} ]]; then
        git -C "${tree}" rm --quiet -- "${path}" || fail "git rm ${path} failed"
    fi
done
if ((${#masked[@]})); then
    uv run --no-project python -I "${tree}/scripts/validate-agent-assets.py" --mask-secrets "${masked[@]}" >&2 ||
        fail 'masking the copies failed; nothing was committed or pushed'
fi
git -C "${tree}" add -A -- .orchestration || fail 'git add failed'
staged=$(git -C "${tree}" diff --cached --name-only -z | tr '\0' '\n') || fail 'git diff --cached failed'
[[ -n ${staged} ]] || refuse 'the copies equal origin/main; nothing to sync'
while IFS= read -r path; do
    [[ ${path} == .orchestration/* ]] || refuse "a staged path is outside .orchestration/: ${path}"
done <<< "${staged}"
count=$(printf '%s\n' "${staged}" | wc -l) || fail 'wc failed'
count=${count//[[:space:]]/}

records=.orchestration/orchestrate/${program}
units=$(git -C "${tree}" diff --cached -U0 -- "${records}/units.tsv" | sed -n -E 's/^\+(U[0-9]+[a-z]?)\t.*/\1/p' | sort -u | paste -sd ' ' -) ||
    fail 'cannot list the units'
decisions=$(git -C "${tree}" diff --cached -U0 -- "${records}/decisions.tsv" | sed -n -E 's/^\+([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z)\t.*/\1/p' | sort -u | paste -sd ' ' -) ||
    fail 'cannot list the decisions'
title="chore(records): ${program} sync ${n}"
git -C "${tree}" commit --quiet -m "${title}" -m "Carries ${count} file(s) of ${records}/ and .orchestration/validation/ from the main checkout (records-sync.sh)." -m "${footer}" ||
    fail 'git commit failed'
git -C "${tree}" push --quiet origin "refs/heads/${branch}:refs/heads/${branch}" || fail "git push ${branch} failed; nothing was opened"
body=${scratch}/body.md
{
    # shellcheck disable=SC2016 # the backticks are Markdown code spans
    printf '## Summary\n\nRecords sync %s of `%s` (%s file(s)), carried by `records-sync.sh` from the main checkout; every copy was masked with `validate-agent-assets.py --mask-secrets`.\n\n' "${n}" "${program}" "${count}"
    printf -- '- units.tsv rows added or changed: %s\n' "${units:-none}"
    printf -- '- decisions.tsv rows added or changed: %s\n\n' "${decisions:-none}"
    [[ -z ${unit} ]] || printf 'Program-Unit: %s/%s\n\n' "${program}" "${unit}"
    printf '%s\n' "${pr_footer}"
} > "${body}" || fail 'cannot write the body'
url=$(gh_bounded pr create --base main --head "${branch}" --title "${title}" --body-file "${body}") ||
    fail "gh pr create failed; the branch ${branch} is pushed"
echo "synced branch=${branch} files=${count} pr=${url}"
