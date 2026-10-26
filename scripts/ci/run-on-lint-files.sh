#!/usr/bin/env bash
# @file run-on-lint-files.sh
# @brief Run a lint or format check on exactly one named set of the repository's tracked files.
# @description
#   The one definition of which files each formatting check reads (regime-cutover U97). `make format` and CI's
#   `Run shfmt` and formatting steps call this with the same set and command, so a local run and CI check the same
#   files. The sets are tracked files only (`git ls-files`): an untracked or gitignored file, such as a worklog copy, is
#   never read. The listing's status is checked and an empty set is refused, so no check passes on no files.
#   - shell: the shell scripts under install/ and scripts/ (`*.sh` at any depth).
#   - python: every tracked `*.py`.
#   - markdown: every tracked `*.md`.
# @arg $1 string The set: shell, python or markdown.
# @arg $@ string The command and its arguments, after the set; the set's paths are appended.
# @exitcode 0 The command passed on the set.
# @exitcode 2 An unknown set, no command, a failed listing or an empty set: nothing was checked.
# @exitcode * The command's own status otherwise.
# @example
#   scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d
set -euo pipefail

if (($# < 2)); then
    printf 'run-on-lint-files: usage: run-on-lint-files.sh <shell|python|markdown> <command> [<argument>...]\n' >&2
    exit 2
fi
set_name=$1
shift
case ${set_name} in
shell) pathspecs=(':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh') ;;
python) pathspecs=('*.py') ;;
markdown) pathspecs=('*.md') ;;
*)
    printf 'run-on-lint-files: %s is not a lint file set (shell, python, markdown)\n' "${set_name}" >&2
    exit 2
    ;;
esac

# The NUL-separated listing goes through a file, so its status is checked and no path is split or lost.
listing=$(mktemp "${TMPDIR:-/tmp}/run-on-lint-files.XXXXXX") || {
    printf 'run-on-lint-files: cannot create a scratch file\n' >&2
    exit 2
}
trap 'rm -f "${listing}"' EXIT
if ! git ls-files -z -- "${pathspecs[@]}" > "${listing}"; then
    printf 'run-on-lint-files: git ls-files failed for the %s set; nothing was checked\n' "${set_name}" >&2
    exit 2
fi
files=()
while IFS= read -r -d '' path; do
    files+=("${path}")
done < "${listing}"
if ((${#files[@]} == 0)); then
    printf 'run-on-lint-files: the %s set lists no tracked file; nothing was checked\n' "${set_name}" >&2
    exit 2
fi
"$@" "${files[@]}"
