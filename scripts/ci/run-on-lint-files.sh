#!/usr/bin/env bash
# @file run-on-lint-files.sh
# @brief Run a lint or format check on exactly one named set of the repository's tracked files.
# @description
#   The one definition of which files each formatting check reads (regime-cutover U97). `make format` and CI's
#   `Run shfmt` and formatting steps call this with the same set and command, so a local run and CI check the same
#   files. The sets are tracked files only (`git ls-files`): an untracked or gitignored file, such as a worklog copy, is
#   never read. The listing's status is checked and an empty set is refused, so no check passes on no files.
#   - shell: every tracked bash or sh script: a `*.sh` or `*.bash` file, or a file whose first line is a bash or sh
#     shebang (the executable_* scripts and hooks under home/, chezmoi modify_ scripts), less the exclusions
#     in_shell_set names, each with its reason.
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
shell) pathspecs=(':/') ;;
python) pathspecs=('*.py') ;;
markdown) pathspecs=('*.md') ;;
*)
    printf 'run-on-lint-files: %s is not a lint file set (shell, python, markdown)\n' "${set_name}" >&2
    exit 2
    ;;
esac

#
# @description Whether a tracked path belongs to the shell set: a bash or sh script that shfmt formats.
# @arg $1 path The tracked path, relative to the repository root.
# @exitcode 0 It belongs to the set.
# @exitcode 1 It does not.
#
function in_shell_set() {
    local path=$1 first=
    case ${path} in # lint-comparisons: allow git ls-files paths, repository-relative and never resolved
    # Records: copies of scripts as a review received them, kept byte for byte, never formatted.
    .orchestration/*) return 1 ;;
    # Bats files: their @test blocks need shfmt's bats dialect, and CI's shfmt set never held them.
    *.bats) return 1 ;;
    # chezmoi templates are Go template text, not shell: 5 of the 34 *.sh.tmpl do not parse, and shfmt re-indents
    # the template actions of the rest as shell words; the scripts most of them include are in the set themselves.
    *.tmpl) return 1 ;;
    esac
    [[ -f ${path} && ! -L ${path} ]] || return 1
    IFS= read -r first < "${path}" || [[ -n ${first} ]] || return 1
    # zsh: shfmt does not parse zsh (its zsh dialect is incomplete), so a zsh script is never formatted, even one named
    # *.sh. A *.zsh file, or a zsh file without one, has no bash or sh shebang and never enters the set below.
    if [[ ${first} == '#!'*zsh* ]]; then
        return 1
    fi
    case ${path} in # lint-comparisons: allow git ls-files paths, repository-relative and never resolved
    *.sh | *.bash) return 0 ;;
    esac
    [[ ${first} =~ ^#![[:space:]]*(/usr/bin/env[[:space:]]+(-S[[:space:]]+)?)?(/[^[:space:]]*/)?(bash|sh)([[:space:]]|$) ]]
}

# The NUL-separated listing goes through a file, so its status is checked and no path is split or lost.
listing=$(mktemp "${TMPDIR:-/tmp}/run-on-lint-files.XXXXXX") || {
    printf 'run-on-lint-files: cannot create a scratch file\n' >&2
    exit 2
}
# No EXIT trap: under bash 3.2 (macOS's /bin/bash) an expansion error with an EXIT trap set exits 0, so a failed run
# could read as a passed check. The scratch file is removed once read.
if ! git ls-files -z -- "${pathspecs[@]}" > "${listing}"; then
    printf 'run-on-lint-files: git ls-files failed for the %s set; nothing was checked\n' "${set_name}" >&2
    exit 2
fi
files=()
while IFS= read -r -d '' path; do
    if [[ ${set_name} != shell ]] || in_shell_set "${path}"; then
        files+=("${path}")
    fi
done < "${listing}"
rm -f "${listing}"
if ((${#files[@]} == 0)); then
    printf 'run-on-lint-files: the %s set lists no tracked file; nothing was checked\n' "${set_name}" >&2
    exit 2
fi
"$@" "${files[@]}"
