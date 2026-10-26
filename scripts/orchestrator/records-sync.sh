#!/usr/bin/env bash
# @file records-sync.sh
# @brief Carry the program's records from the main checkout to a `records/sync-<n>` pull request.
# @description
#   Regime-cutover U28 (ADDENDUM), the orchestrator seat's lever, allowed by the rows
#   `~/.local/bin/common/records-sync.sh *` and the bare `~/.local/bin/common/records-sync.sh` of
#   `home/dot_agents/omp/policies/orchestrator.yml` (the seat's own `git push` and `gh pr create` stay denied;
#   `worker.yml` denies every form, bare included, U28b F3). It runs in the main checkout, where the orchestrator
#   writes its records (a linked worktree is refused), and `.orchestration` there must be a real directory.
#   The copy set (U101) is exactly the program store `.orchestration/orchestrate/<program>/`: its files on disk,
#   tracked or untracked and not ignored (`git ls-files --cached --others --exclude-standard`), compared with the
#   same paths in `origin/main` by content, so a file the store lacks but `origin/main` holds is deleted and the
#   checkout's `HEAD`, however stale, is never the base. `.orchestration/validation/` files go in only when a
#   `--validation <path>` names them. The store's `redact-words.txt` (one literal word per line, `#` comments) is
#   never copied, deleted or published. Every path must lie under `.orchestration/`, no component of it may be a
#   symlink (git lists the files below a linked directory too, U28b F2), and an existing source must be a regular
#   file whose directory resolves (`pwd -P`) inside the store, else the run is refused before anything is created.
#   In a new detached worktree under `$TMPDIR` at `origin/main` it copies the set, deletes what the store lacks,
#   masks the copies with the worktree's own `scripts/validate-agent-assets.py --mask-secrets` (the checkout's files
#   are never changed; a masking failure aborts), then refuses the run if that validator's `--scan-identifiers`
#   still finds a secret pattern, a home directory path or a redact word (in a copy's text or path), and refuses a
#   staged path outside `.orchestration/` and an empty change. `<n>` is then one more than the largest number among
#   the remote heads, the local branches (U28b F6) and the heads of the newest 1000 pull requests named
#   `records/sync-<n>`, `records/program-store-<n>` or `records/<program>-sync-<n>` (the earlier syncs), and the
#   branch must match `records/sync-<n>`. It commits `chore(records): <program> sync <n>` with the footer and the
#   identity `git config user.name`/`user.email` read once at the start, pushes that branch only to origin's
#   configured URL as written (https or a local path), and opens the pull request with
#   `gh pr create --base main --head records/sync-<n> --title ... --body-file ...`. The commit, the push and the
#   `gh` calls run with `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1` and the push with the credential helper
#   `!gh auth git-credential` only (U101), so no `url.*.pushInsteadOf` of the user config redirects them; a `url.*`
#   rewrite in the config left (the repository's own) is refused. The body lists the `units.tsv` ids and the
#   `decisions.tsv` timestamps the sync adds or changes and the line `Program-Unit: <program>/<unit>`, which the
#   `regime` check requires (U28c F2). The worktree is removed on every exit (`git worktree remove --force`, only on
#   the path this run created), and a run that exits before its push deletes the branch it created (only that one),
#   so a retry takes the same number; a pushed branch stays. Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT
#   seconds.
# @option --base <ref> The start point; only `origin/main` (the default) is accepted.
# @option --program <name> The program directory under `.orchestration/orchestrate/`; default: the only one.
# @option --unit <U<n>> The unit the body's `Program-Unit:` line names; default: U20, the records unit.
# @option --validation <path> A file under `.orchestration/validation/` to carry too; repeatable.
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `synced branch=records/sync-<n> files=<n> pr=<url>`.
# @exitcode 0 The pull request was opened.
# @exitcode 1 A `git` or `gh` step, or the masking, failed; nothing was pushed unless the receipt says so.
# @exitcode 2 Refused: usage, a linked worktree, the program, the copy set, the identifier scan, the identity, the
#   push URL or a URL rewrite, or nothing to sync.
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
usage='usage: records-sync.sh [--base origin/main] [--program <name>] [--unit U<n> (default U20)] [--validation <path>]...'
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
    # U28b F6: a run that created its branch and never pushed it deletes exactly that branch, so a retry is not
    # blocked by it; a pushed branch stays (the remote holds it, and the next run numbers past it).
    if [[ -n ${created_branch:-} && ${pushed:-0} == 0 ]]; then
        git -C "${toplevel}" branch -D "${created_branch}" > /dev/null 2>&1 ||
            echo "${lever}: could not delete the unpushed branch ${created_branch}" >&2
    fi
}

# @description Run git with no user or system config (U101): no `url.*.insteadOf`/`pushInsteadOf`, credential
#   helper or signing setting of the operator's global config reaches the push, the commit or the `gh` steps.
# @arg $@ string The `git` arguments.
git_plain() {
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git "$@"
}

# @description Run `gh` as gh_bounded does, with no user or system git config for the `git` it runs.
# @arg $@ string The `gh` arguments.
gh_plain() {
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 gh_bounded "$@"
}

# @description Refuse a path of the copy set that leaves `.orchestration/`, holds `..` or a symlink component, or
#   (when it exists) is no regular file whose directory resolves inside the store (U28b F2).
# @arg $1 string The repository-relative path.
check_path() {
    local path=$1 prefix='' part source_dir
    local -a parts
    case ${path} in # lint-comparisons: allow a repository-relative path as git prints it, refused unless under the store
    .orchestration/*) ;;
    *) refuse "a path of the copy set is outside .orchestration/: ${path}" ;;
    esac
    [[ ${path} != *..* ]] || refuse "a path of the copy set holds '..': ${path}" # lint-comparisons: allow refuses a raw git path that holds ..
    IFS=/ read -r -a parts <<< "${path}"
    for part in "${parts[@]}"; do
        prefix=${prefix:+${prefix}/}${part}
        [[ ! -L ${prefix} ]] || refuse "a component of a path of the copy set is a symlink: ${prefix} (in ${path})"
    done
    if [[ -e ${path} ]]; then
        [[ -f ${path} ]] || refuse "a path of the copy set is not a regular file: ${path}"
        source_dir=$(cd "${path%/*}" && pwd -P) || refuse "cannot resolve the directory of ${path}"
        [[ ${source_dir} == "${store_root}" || ${source_dir} == "${store_root}"/* ]] || # lint-comparisons: allow both sides are pwd -P forms
            refuse "a path of the copy set resolves outside ${store_root}: ${path}"
    fi
}

base=origin/main
program=''
unit=U20
validation=()
while (($#)); do
    case $1 in
    --base | --program | --unit | --validation)
        (($# >= 2)) || refuse "${usage}"
        case $1 in
        --base) base=$2 ;;
        --program) program=$2 ;;
        --unit) unit=$2 ;;
        --validation) validation+=("$2") ;;
        esac
        shift 2
        ;;
    *) refuse "${usage}" ;;
    esac
done
[[ ${base} == origin/main ]] || refuse "--base accepts only origin/main: ${base}" # lint-comparisons: allow a git ref name, not a path
[[ ${unit} =~ ^U[0-9]+$ ]] || refuse "--unit is not a plain unit id U<n>: ${unit}"
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'

toplevel=$(git rev-parse --show-toplevel 2> /dev/null) || refuse 'not in a git checkout'
git_dir=$(git rev-parse --path-format=absolute --git-dir) || refuse 'cannot read the git directory'
common_dir=$(git rev-parse --path-format=absolute --git-common-dir) || refuse 'cannot read the git common directory'
git_dir=$(cd "${git_dir}" && pwd -P) || refuse "cannot resolve ${git_dir}"
common_dir=$(cd "${common_dir}" && pwd -P) || refuse "cannot resolve ${common_dir}"
[[ ${git_dir} == "${common_dir}" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse "${toplevel} is a linked worktree; run from the main checkout, where the orchestrator writes its records"
cd "${toplevel}" || refuse "cannot enter ${toplevel}"
# U28b F2: the store root itself is no symlink, so every canonical path below is measured against the real store.
top_real=$(pwd -P) || refuse "cannot resolve ${toplevel}"
[[ -d .orchestration && ! -L .orchestration ]] || refuse ".orchestration is missing or a symlink in ${toplevel}"
store_root=$(cd .orchestration && pwd -P) || refuse "cannot resolve ${toplevel}/.orchestration"
[[ ${store_root} == "${top_real}/.orchestration" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse ".orchestration resolves outside ${top_real}: ${store_root}"
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
records=.orchestration/orchestrate/${program}
# U28b F2: no component of the store directory is a symlink (git would list the files below a linked one too).
for prefix in .orchestration/orchestrate "${records}"; do
    [[ ! -L ${prefix} ]] || refuse "a component of a path of the copy set is a symlink: ${prefix} (in ${records}/)"
done
[[ -d ${records} ]] || refuse "no program directory ${records}"
# U101: the words no copy may contain; the file itself is never copied, deleted or published.
words=${records}/redact-words.txt
if [[ -e ${words} || -L ${words} ]]; then
    check_path "${words}"
    words_real=$(cd "${records}" && pwd -P)/redact-words.txt || refuse "cannot resolve ${words}"
else
    words_real=''
fi
for path in ${validation[@]+"${validation[@]}"}; do
    [[ ${path} == .orchestration/validation/?* ]] || # lint-comparisons: allow a repository-relative path as the operator names it
        refuse "--validation names a file outside .orchestration/validation/: ${path}"
    check_path "${path}"
    [[ -f ${path} ]] || refuse "--validation names no regular file: ${path}"
done
# The commit's identity is the operator's, read once here; the commit itself then runs with no user config.
author_name=$(git config user.name) || refuse 'git config user.name is unset'
author_email=$(git config user.email) || refuse 'git config user.email is unset'
# U101: the push goes to origin's configured URL as written, with no URL rewrite anywhere in the config git reads.
push_url=$(git_plain config --get remote.origin.url) || refuse 'no remote.origin.url'
case ${push_url} in # lint-comparisons: allow the URL's scheme as configured, the push target itself
https://* | /* | file:///*) ;;
*) refuse "the push needs an https (or local) origin URL, not ${push_url}" ;;
esac
if rewrites=$(git_plain config --name-only --get-regexp '^url\.'); then
    refuse "a url.* rewrite outside the user config would redirect the push: ${rewrites//$'\n'/ }"
elif (($? != 1)); then
    fail 'git config --get-regexp url.* failed'
fi

git fetch --quiet origin main || fail 'git fetch origin main failed'
# U101: the copy set is the store's files on disk (tracked or not, not ignored) and the named validation files,
# compared with origin/main by content; the checkout's HEAD, however stale, is never the base.
listed=$(git ls-files -z --cached --others --exclude-standard -- "${records}/" | tr '\0' '\n' | sort -u) ||
    fail 'git ls-files failed'
on_main=$(git ls-tree -r -z --name-only "${base}" -- "${records}/" | tr '\0' '\n') || fail "git ls-tree ${base} failed"
files=(${validation[@]+"${validation[@]}"})
present=$'\n'
while IFS= read -r path; do
    [[ -n ${path} && ${path} != "${words}" ]] || continue # lint-comparisons: allow both are repository-relative paths as git prints them
    check_path "${path}"
    if [[ -e ${path} ]]; then
        files+=("${path}")
        present+=${path}$'\n'
    fi
done <<< "${listed}"
gone=()
while IFS= read -r path; do
    [[ -n ${path} && ${path} != "${words}" && ${present} != *$'\n'"${path}"$'\n'* ]] || continue # lint-comparisons: allow repository-relative paths as git prints them
    check_path "${path}"
    gone+=("${path}")
done <<< "${on_main}"
((${#files[@]} + ${#gone[@]} > 0)) || refuse "nothing to sync under ${records}/"

scratch=$(mktemp -d "${TMPDIR:-/tmp}/records-sync.XXXXXX") || fail 'mktemp failed'
trap cleanup EXIT
tree=${scratch}/tree
git worktree add --quiet --detach "${tree}" "${base}" || fail 'git worktree add failed'
masked=()
for path in ${files[@]+"${files[@]}"}; do
    mkdir -p "${tree}/${path%/*}" || fail "mkdir for ${path} failed"
    cp -p "${path}" "${tree}/${path}" || fail "cp ${path} failed"
    masked+=("${tree}/${path}")
done
for path in ${gone[@]+"${gone[@]}"}; do
    git -C "${tree}" rm --quiet -- "${path}" || fail "git rm ${path} failed"
done
if ((${#masked[@]})); then
    uv run --no-project python -I "${tree}/scripts/validate-agent-assets.py" --mask-secrets "${masked[@]}" >&2 ||
        fail 'masking the copies failed; nothing was committed or pushed'
    # U101: after masking, no copy may still name a secret, a home path or a redact word, its path included.
    scan=(--scan-identifiers)
    [[ -z ${words_real} ]] || scan+=(--redact-words "${words_real}")
    (cd "${tree}" && uv run --no-project python -I scripts/validate-agent-assets.py "${scan[@]}" -- "${files[@]}" >&2) ||
        refuse 'the identifier scan found the findings above in the masked copies; nothing was committed or pushed'
fi
git -C "${tree}" add -A -- .orchestration || fail 'git add failed'
staged=$(git -C "${tree}" diff --cached --no-renames --name-only -z | tr '\0' '\n') || fail 'git diff --cached failed'
[[ -n ${staged} ]] || refuse 'the copies equal origin/main; nothing to sync'
while IFS= read -r path; do
    [[ ${path} == .orchestration/* ]] || refuse "a staged path is outside .orchestration/: ${path}" # lint-comparisons: allow a repository-relative path as git prints it
done <<< "${staged}"
count=$(printf '%s\n' "${staged}" | wc -l) || fail 'wc failed'
count=${count//[[:space:]]/}

remote_heads=$(git ls-remote --heads origin 'refs/heads/records/*') || fail 'git ls-remote origin failed'
# U28b F6: a local branch occupies its number too, whatever left it behind.
local_heads=$(git for-each-ref --format='%(refname)' 'refs/heads/records/') || fail 'git for-each-ref failed'
pr_heads=$(gh_plain pr list --state all --limit 1000 --json headRefName --jq '.[].headRefName') ||
    fail 'gh pr list failed'
last=$(printf '%s\n%s\n%s\n' "${remote_heads}" "${local_heads}" "${pr_heads}" |
    PROGRAM=${program} awk '{ ref = $NF; sub(/^refs\/heads\//, "", ref) }
        ref ~ "^records/(sync|program-store|" ENVIRON["PROGRAM"] "-sync)-[0-9]+$" { n = ref; sub(/.*-/, "", n); if (n + 0 > max) max = n + 0 }
        END { print max + 0 }') || fail 'cannot number the sync'
n=$((last + 1))
branch=records/sync-${n}
[[ ${branch} =~ ^records/sync-[1-9][0-9]*$ ]] || refuse "the branch is outside records/sync-<n>: ${branch}"
git -C "${tree}" switch --quiet -c "${branch}" || fail "git switch -c ${branch} failed"
created_branch=${branch}
pushed=0

units=$(git -C "${tree}" diff --cached -U0 -- "${records}/units.tsv" | sed -n -E 's/^\+(U[0-9]+[a-z]?)\t.*/\1/p' | sort -u | paste -sd ' ' -) ||
    fail 'cannot list the units'
decisions=$(git -C "${tree}" diff --cached -U0 -- "${records}/decisions.tsv" | sed -n -E 's/^\+([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z)\t.*/\1/p' | sort -u | paste -sd ' ' -) ||
    fail 'cannot list the decisions'
title="chore(records): ${program} sync ${n}"
carried="${records}/"
((${#validation[@]} == 0)) || carried+=" and ${#validation[@]} named file(s) of .orchestration/validation/"
git_plain -C "${tree}" -c "user.name=${author_name}" -c "user.email=${author_email}" commit --quiet -m "${title}" \
    -m "Carries ${count} file(s) of ${carried} from the main checkout, compared with origin/main (records-sync.sh)." -m "${footer}" ||
    fail 'git commit failed'
git_plain -C "${tree}" -c credential.helper= -c 'credential.helper=!gh auth git-credential' \
    push --quiet "${push_url}" "refs/heads/${branch}:refs/heads/${branch}" || fail "git push ${branch} failed; nothing was opened"
pushed=1
body=${scratch}/body.md
{
    # shellcheck disable=SC2016 # the backticks are Markdown code spans
    printf '## Summary\n\nRecords sync %s of `%s` (%s file(s)), carried by `records-sync.sh` from the main checkout and compared with origin/main; every copy was masked with `validate-agent-assets.py --mask-secrets` and passed its `--scan-identifiers`.\n\n' "${n}" "${program}" "${count}"
    printf -- '- units.tsv rows added or changed: %s\n' "${units:-none}"
    printf -- '- decisions.tsv rows added or changed: %s\n\n' "${decisions:-none}"
    printf 'Program-Unit: %s/%s\n\n' "${program}" "${unit}"
    printf '%s\n' "${pr_footer}"
} > "${body}" || fail 'cannot write the body'
url=$(gh_plain pr create --base main --head "${branch}" --title "${title}" --body-file "${body}") ||
    fail "gh pr create failed; the branch ${branch} is pushed"
echo "synced branch=${branch} files=${count} pr=${url}"
