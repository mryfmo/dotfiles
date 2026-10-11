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
#   one on the base. An implementation PR (a task id not ending in
#   -contract-a01) must have removed the contract decorator from its own copy
#   of each declared module. A unittest run counts only by the result file its
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
# --no-renames: a script moved away still shows its old path.
changed="$(git -c core.quotePath=false diff --name-only --no-renames "${merge_base}" HEAD)"
# Assigned first, so a failing helper stops the run instead of reading as "no script change".
scripts_changed="$(markers scripts <<< "${changed}")"
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
tasks="$(git -c core.quotePath=false diff --name-only --no-renames --diff-filter=d "${merge_base}" HEAD -- ':(glob).orchestration/*/task.md')"
if [ "$(grep -c . <<< "${tasks}")" -gt 1 ]; then
    echo "main-tests: more than one task.md in the range: ${tasks//$'\n'/ }"
    exit 1
fi
if [ -n "${tasks}" ]; then
    parsed="$(markers task "${tmp}/${tasks}")"
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
        esac
    done <<< "${parsed}"
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
    elif [[ "${task_id}" != *-contract-a01 ]] && ! markers dormant "${tmp}/${module}"; then
        echo "main-tests: contract still dormant in ${module}"
        status=1
    fi
done <<< "${declared}"

# Exactly main's tests/unit: a file the PR adds there (a unittest.py, say) must not shadow main's.
rm -rf "${tmp}/tests/unit"
git archive "${base}" tests/unit | tar -x -C "${tmp}"

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
# @arg $@ string The unittest ids, after an optional -v.
run_unittest() {
    local expected="$1" nonce
    shift
    nonce="$(od -An -N16 -tx1 /dev/urandom | tr -d ' \n')"
    rm -f "${tmp}.result"
    # -P keeps the tree's root off sys.path; tests/unit comes only from PYTHONPATH.
    PYTHONPATH=tests/unit uv run --no-config --no-project --python "${python}" python -P "${helper}" run "${tmp}.result" "$@" 3<<< "${nonce}" || return 1
    markers result "${tmp}.result" "${nonce}" "${expected}"
}

cd "${tmp}"
if [ "${#undeclared[@]}" -gt 0 ]; then
    echo "main-tests: undeclared mode, main's modules as they are: ${undeclared[*]}"
    run_unittest 0 "${undeclared[@]}" || status=1
fi
if [ "${#contract_ids[@]}" -gt 0 ]; then
    echo "main-tests: declared mode, main's contracts with REGIME_CONTRACT=1: ${contract_ids[*]}"
    REGIME_CONTRACT=1 run_unittest "${#contract_ids[@]}" -v "${contract_ids[@]}" || status=1
fi
exit "${status}"
