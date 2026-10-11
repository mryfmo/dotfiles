#!/usr/bin/env bash
# @file main-tests.sh
# @brief Run main's unit tests against a pull request's scripts (T128 INV-12).
# @description
#   When the diff from the merge base touches a script path, copies HEAD's tree
#   to a temporary directory, overlays the base's tests/unit on it and runs:
#   every base module the task.md does not exempt, as it is (undeclared mode),
#   and the base's `@contract` tests of each exempt module with
#   REGIME_CONTRACT=1 (declared mode). A module is exempt only when the task.md
#   declares both it and its script. A design-tier task.md (a missing `tier:`
#   stamp counts as design) must also declare a module for each script it
#   declares, keep each declared module, and find a contract for each exempt
#   one on the base. The PR's own copy of each declared module must carry no
#   contract decorator, and a contract wave (a task id ending in -contract-a01)
#   may change no script. A unittest run counts only by the result file its
#   runner writes with this run's nonce. The exit status combines every check.
#   The `main-tests` job of .github/workflows/test.yaml runs the base's copy of
#   this script and of lib/contract_markers.py, never the pull request's.
# @arg $1 string Base ref, for example origin/main.
# @exitcode 0 No script changed, or every check passed.
# @exitcode 1 A check failed.
# @example
#   scripts/main-tests.sh origin/main

set -euo pipefail

base="${1:?usage: main-tests.sh <base-ref>}"
helper="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/contract_markers.py"
# Found from / and passed explicitly: uv's own discovery executes a .venv interpreter the PR plants.
python="$(cd / && uv python find --no-config)"

# @description Run lib/contract_markers.py with PyYAML available. --no-config keeps
#   a uv.toml the PR adds from choosing the index.
# @arg $@ string The helper's subcommand and arguments.
markers() {
    uv run --no-config --no-project --python "${python}" --quiet --with pyyaml python3 "${helper}" "$@"
}

merge_base="$(git merge-base "${base}" HEAD)"
# --no-renames: a script moved away still shows its old path. -z: git C-quotes a name with a line
# break in line mode, which would hide the script; the helper rejects such a name instead.
# Assigned first, so a failing helper stops the run instead of reading as "no script change".
scripts_changed="$(git -c core.quotePath=false diff --name-only -z --no-renames "${merge_base}" HEAD | markers scripts)"
if [ -z "${scripts_changed}" ]; then
    echo "main-tests: no script change"
    exit 0
fi

tmp="$(mktemp -d "${TMPDIR:-/tmp}/main-tests.XXXXXX")"
trap 'rm -rf "${tmp}" "${tmp}.result"' EXIT
# A complete tree, so each module's own-path ROOT lands on HEAD's files.
git archive HEAD | tar -x -C "${tmp}"

status=0
task_id=""
tier=""
# Newline-separated: bash 3.2 (macOS) cannot expand an empty array under set -u.
declared=""
exempt=""
orphans=""
tasks="$(git -c core.quotePath=false diff --name-only --no-renames --diff-filter=d "${merge_base}" HEAD -- ':(glob).orchestration/*/task.md')"
if [ "$(grep -c . <<< "${tasks}")" -gt 1 ]; then
    echo "main-tests: more than one task.md in the range: ${tasks//$'\n'/ }"
    exit 1
fi
# No task.md (a boundary PR) leaves every changed script undeclared.
parsed="$(markers task ${tasks:+"${tmp}/${tasks}"} <<< "${scripts_changed}")"
while IFS=$'\t' read -r kind value module; do
    case "${kind}" in
    task_id) task_id="${value}" ;;
    tier) tier="${value}" ;;
    module) declared+="${value}"$'\n' ;;
    exempt) exempt+="${value}"$'\n' ;;
    uncovered)
        echo "main-tests: design script ${value} has no declared contract module ${module}"
        status=1
        ;;
    undeclared) orphans+="${value}"$'\t'"${module}"$'\n' ;;
    esac
done <<< "${parsed}"
# A contract wave ships dormant tests only, and this point is reached only when a script changed.
if [[ "${task_id}" == *-contract-a01 ]]; then
    echo "main-tests: ${task_id} is a contract wave but changes scripts: ${scripts_changed//$'\n'/ }"
    status=1
fi

# The PR's own copies, read before the overlay replaces them.
while IFS= read -r module; do
    if [ -z "${module}" ]; then
        continue
    elif [ ! -f "${tmp}/${module}" ]; then
        if [ "${tier}" = design ]; then
            echo "main-tests: declared module ${module} deleted"
            status=1
        fi
    elif ! markers dormant "${tmp}/${module}"; then
        echo "main-tests: contract still dormant in ${module}"
        status=1
    fi
done <<< "${declared}"

# Exactly main's tests/unit: a file the PR adds there (a unittest.py, say) must not shadow main's.
rm -rf "${tmp}/tests/unit"
git archive "${base}" tests/unit | tar -x -C "${tmp}"

# main's tests judge an undeclared script only through ordinary tests in its module; dormant contracts skip.
while IFS=$'\t' read -r script module; do
    if [ -z "${script}" ]; then
        continue
    elif [ ! -f "${tmp}/${module}" ]; then
        echo "main-tests: undeclared script ${script} has no module on main (${module})"
        status=1
    elif [ -z "$(markers ordinary "${tmp}/${module}")" ]; then
        echo "main-tests: undeclared script ${script} has only dormant contracts on main (${module})"
        status=1
    fi
done <<< "${orphans}"

undeclared=()
main_modules="$(git ls-tree --name-only "${base}" tests/unit/)"
while IFS= read -r module; do
    [[ "${module}" =~ ^tests/unit/test_[^/]+\.py$ ]] || continue
    grep -qxF "${module}" <<< "${exempt}" || undeclared+=("$(basename "${module}" .py)")
done <<< "${main_modules}"

contract_ids=()
while IFS= read -r module; do
    [ -n "${module}" ] || continue
    ids=""
    if git cat-file -e "${base}:${module}" 2> /dev/null; then
        ids="$(markers contracts "${tmp}/${module}")"
    fi
    if [ -n "${ids}" ]; then
        while IFS= read -r id; do contract_ids+=("${id}"); done <<< "${ids}"
    elif [ "${tier}" = design ]; then
        echo "main-tests: no contract on main for ${module}"
        status=1
    fi
done <<< "${exempt}"

# @description Run main's tests from the tree copy through lib/contract_markers.py's runner and count
#   the run only by the result it writes with this run's nonce: output and exit status are the
#   tested code's to forge. The nonce goes in on fd 3, never in argv or the environment.
# @arg $1 int The expected test count; 0 accepts any count above zero.
# @arg $2 string The test ids allowed to skip, newline-separated (main's dormant contracts).
# @arg $@ string The unittest ids, after an optional -v.
run_unittest() {
    local expected="$1" skips="$2" nonce
    shift 2
    nonce="$(od -An -N16 -tx1 /dev/urandom | tr -d ' \n')"
    rm -f "${tmp}.result"
    # -P keeps the tree's root off sys.path; tests/unit comes only from PYTHONPATH.
    PYTHONPATH=tests/unit uv run --no-config --no-project --python "${python}" python -P "${helper}" run "${tmp}.result" "$@" 3<<< "${nonce}" || return 1
    markers result "${tmp}.result" "${nonce}" "${expected}" "${skips}"
}

cd "${tmp}"
if [ "${#undeclared[@]}" -gt 0 ]; then
    echo "main-tests: undeclared mode, main's modules as they are: ${undeclared[*]}"
    modules=()
    for module in "${undeclared[@]}"; do modules+=("tests/unit/${module}.py"); done
    # Only main's dormant contracts may skip here; any other skip could be the PR's code asking for one.
    dormant="$(markers contracts "${modules[@]}")"
    run_unittest 0 "${dormant}" "${undeclared[@]}" || status=1
fi
if [ "${#contract_ids[@]}" -gt 0 ]; then
    echo "main-tests: declared mode, main's contracts with REGIME_CONTRACT=1: ${contract_ids[*]}"
    REGIME_CONTRACT=1 run_unittest "${#contract_ids[@]}" "" -v "${contract_ids[@]}" || status=1
fi
exit "${status}"
