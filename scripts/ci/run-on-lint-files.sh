#!/usr/bin/env bash
# @file run-on-lint-files.sh
# @brief Run a lint or format check on exactly one named set of the repository's tracked files.
# @description
#   The one definition of which files each formatting check reads (regime-cutover U97). `make format` and CI's
#   `Run shfmt` and formatting steps call this with the same set and command, so a local run and CI check the same
#   files. The sets come from git's index (`git ls-files -s`): an untracked or gitignored file, such as a worklog
#   copy, is never read. The listing's status is checked and an empty set is refused, so no check passes on no files.
#   Nothing here needs a temporary file (round-5 audit of cdf72bb6: bash 3.2 backs here-strings and here-documents
#   with one, and an `or-colon` hid its failure): the listing is a command substitution, and every split is word
#   splitting with globbing off, so the script runs the same with TMPDIR unwritable.
#   Each path reaches the command as `./<path>`, so a tracked file named like an option (`-version`, `--help`, `-l`)
#   is read as a file: shfmt, ruff and prettier all take `./`-prefixed paths as paths, ruff's force-exclude and
#   .prettierignore still match them, and the form needs no `--` support from the command. An unmerged index (a
#   conflict in progress) is refused: a path with several stages has no one content to check.
#   - shell: every tracked bash or sh script, decided by in_shell_set from the index entry's mode, the path's name and
#     the first line's interpreter, never by probing the work tree. An entry that cannot be decided stops the run.
#   - python: every tracked `*.py`.
#   - markdown: every tracked `*.md`.
# @arg $1 string The set: shell, python or markdown.
# @arg $@ string The command and its arguments, after the set; the set's paths are appended.
# @exitcode 0 The command passed on the set.
# @exitcode 2 An unknown set, no command, a failed listing, an unmerged index, a shell-set entry that cannot be decided
#   (an unknown mode, a file the index holds that cannot be read, an env option this script does not know), or an
#   empty set: nothing was checked.
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
# @description Name the interpreter a first line's shebang runs, by tokens (round-4 audit of 3b293cd5: a substring
#   match read `env -S bash # zsh …` as zsh). The line must start with `#!`; the rest is split on blanks, as env -S
#   splits its string and as macOS passes the words. The first token is the interpreter. When its basename is `env`,
#   env's own words are skipped: `-S`/`--split-string` (the words after it are the split string), `-i`, `-0`, `-v`,
#   `--ignore-environment`, `--null`, `--debug`, `-u NAME`/`-uNAME`/`--unset[=]NAME`, `-C DIR`/`-CDIR`/`--chdir[=]DIR`,
#   `--`, and `NAME=VALUE`; the next word is the interpreter.
# @arg $1 string The first line.
# @set interpreter string The interpreter's basename; empty when the line has no shebang or names none.
# @exitcode 0 Decided.
# @exitcode 1 env carries an option this function does not know, so the interpreter cannot be told.
#
function shebang_interpreter() {
    local line=$1 index=1 word IFS=$' \t'
    local -a words=()
    interpreter=
    [[ ${line} == '#!'* ]] || return 0
    # Word splitting on blanks, with globbing off so a `*` in the line stays a word; the noglob state is restored.
    if [[ $- == *f* ]]; then
        # shellcheck disable=SC2206 # split on purpose: IFS is blanks and globbing is off
        words=(${line#??})
    else
        set -f
        # shellcheck disable=SC2206 # split on purpose: IFS is blanks and globbing is off
        words=(${line#??})
        set +f
    fi
    ((${#words[@]} > 0)) || return 0
    word=${words[0]}
    if [[ ${word##*/} != env ]]; then
        interpreter=${word##*/}
        return 0
    fi
    while ((index < ${#words[@]})); do
        word=${words[index]}
        case ${word} in
        --)
            index=$((index + 1))
            break
            ;;
        -S | --split-string | -i | -0 | -v | --ignore-environment | --null | --debug) ;;
        -u | -C | --unset | --chdir) index=$((index + 1)) ;;
        -u?* | -C?* | --unset=* | --chdir=*) ;;
        -S?*)
            # -Sbash: the split string starts inside the option word.
            word=${word#-S}
            interpreter=${word##*/}
            return 0
            ;;
        -*) return 1 ;;
        *=*) [[ ${word%%=*} =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || break ;;
        *) break ;;
        esac
        index=$((index + 1))
    done
    if ((index < ${#words[@]})); then
        interpreter=${words[index]##*/}
    fi
}

#
# @description Whether an index entry belongs to the shell set: a bash or sh script that shfmt formats.
#   - Type comes from the index mode, never from the work tree: 100644 and 100755 are regular files, 120000 (a
#     symlink) and 160000 (a gitlink, a submodule) are excluded by rule, any other mode is an error.
#   - Excluded by name, never read: `.orchestration/**` (records, copies of scripts as a review received them),
#     `*.bats` (their @test blocks need shfmt's bats dialect, and CI's shfmt set never held them) and `*.tmpl`
#     (chezmoi templates are Go template text: 5 of the 34 `*.sh.tmpl` do not parse, shfmt re-indents the template
#     actions of the rest, and the scripts most of them include are in the set).
#   - Every other regular entry is read: its first line comes from head, whose status is checked. A missing file, an
#     unreadable one, an unsearchable parent or a read error stops the run; it is never an exclusion.
#   - Included: a `*.sh` or `*.bash` file unless its shebang names zsh (shfmt does not parse zsh), and any file whose
#     shebang's interpreter is exactly `bash` or `sh`. The extension wins over any other interpreter: a `*.sh` file
#     with another shebang is checked, and shfmt says so if it is not shell. Only zsh takes a file back out.
# @arg $1 string The index mode.
# @arg $2 path The tracked path, relative to the repository root.
# @set reason string Why the entry cannot be decided, when the function returns 2.
# @exitcode 0 It belongs to the set.
# @exitcode 1 It does not.
# @exitcode 2 It cannot be decided: the caller stops, never drops the entry.
#
function in_shell_set() {
    local mode=$1 path=$2 first
    reason=
    case ${mode} in
    100644 | 100755) ;;
    120000 | 160000) return 1 ;;
    *)
        reason="the index gives ${path} mode ${mode}, which this script does not know"
        return 2
        ;;
    esac
    case ${path} in # lint-comparisons: allow git ls-files paths, repository-relative and never resolved
    .orchestration/* | *.bats | *.tmpl) return 1 ;;
    esac
    # bash's `read` returns 1 at end of file and on a read error alike, so the first line comes from head, whose exit
    # status is non-zero on an open or read error and 0 at a short or empty file (POSIX head, EXIT STATUS). tr drops
    # NUL bytes, which a binary file's first line may hold and a command substitution would warn about; the pipeline
    # sets its own pipefail, so head's status is never masked by tr's, whatever the caller's options. LC_ALL=C keeps
    # both byte-wise on any file.
    if ! first=$(
        set -o pipefail
        LC_ALL=C head -n 1 -- "./${path}" | LC_ALL=C tr -d '\000'
    ); then
        reason="cannot read ${path} to tell whether it is a shell script"
        return 2
    fi
    if ! shebang_interpreter "${first}"; then
        reason="cannot tell the interpreter of ${path}: its env shebang carries an option this script does not know"
        return 2
    fi
    [[ ${interpreter} != zsh ]] || return 1
    case ${path} in # lint-comparisons: allow git ls-files paths, repository-relative and never resolved
    *.sh | *.bash) return 0 ;;
    esac
    [[ ${interpreter} == bash || ${interpreter} == sh ]]
}

#
# @description Decode a path git printed in C style (core.quotePath=true): the text between the double quotes, with
#   \a \b \t \n \v \f \r \" \\ and three-digit octal escapes, the forms git's quote_c_style writes. Byte-wise.
# @arg $1 string The quoted path, quotes included.
# @set decoded string The path's bytes.
# @exitcode 1 The text is not a quoted path in that form.
#
function unquote_path() {
    local quoted=$1 rest character code LC_ALL=C
    decoded=
    if ((${#quoted} < 2)) || [[ ${quoted:0:1} != '"' || ${quoted: -1} != '"' ]]; then
        return 1
    fi
    rest=${quoted:1:${#quoted}-2}
    while [[ -n ${rest} ]]; do
        character=${rest:0:1}
        if [[ ${character} != "\\" ]]; then
            decoded+=${character}
            rest=${rest:1}
            continue
        fi
        character=${rest:1:1}
        case ${character} in
        a) decoded+=$'\a' ;;
        b) decoded+=$'\b' ;;
        t) decoded+=$'\t' ;;
        n) decoded+=$'\n' ;;
        v) decoded+=$'\v' ;;
        f) decoded+=$'\f' ;;
        r) decoded+=$'\r' ;;
        '"' | "\\") decoded+=${character} ;;
        [0-3])
            code=${rest:1:3}
            [[ ${code} =~ ^[0-3][0-7][0-7]$ ]] || return 1
            printf -v character '%b' "\\0${code}"
            decoded+=${character}
            rest=${rest:4}
            continue
            ;;
        *) return 1 ;;
        esac
        rest=${rest:2}
    done
}

# The listing is a command substitution (a pipe, never a file) with its status checked. core.quotePath=true makes git
# print every path holding a control character, a quote, a backslash or a non-ASCII byte in double quotes, so a line
# is never split inside a path and an unquoted path is the path as given; unquote_path decodes the rest.
# No EXIT trap: under bash 3.2 (macOS's /bin/bash) an expansion error with an EXIT trap set exits 0, so a failed run
# could read as a passed check.
if ! listing=$(git -c core.quotePath=true ls-files -s -- "${pathspecs[@]}"); then
    printf 'run-on-lint-files: git ls-files failed for the %s set; nothing was checked\n' "${set_name}" >&2
    exit 2
fi
entries=()
if [[ -n ${listing} ]]; then
    saved_ifs=${IFS}
    IFS=$'\n'
    set -f
    # shellcheck disable=SC2206 # split on purpose: one entry per line, globbing off
    entries=(${listing})
    set +f
    IFS=${saved_ifs}
fi
files=()
failure=
# Each entry is `<mode> <object> <stage>\t<path>`.
for entry in ${entries[@]+"${entries[@]}"}; do
    meta=${entry%%$'\t'*}
    path=${entry#*$'\t'}
    if [[ ${path} == '"'* ]]; then # lint-comparisons: allow git's C-style quote mark, not a path comparison
        if ! unquote_path "${path}"; then
            failure="git printed the path ${path} in a form this script does not decode"
            break
        fi
        path=${decoded}
    fi
    mode=${meta%% *}
    stage=${meta##* }
    if [[ ${stage} != 0 ]]; then
        failure="${path} is unmerged in the index"
        break
    fi
    member=0
    if [[ ${set_name} == shell ]]; then
        in_shell_set "${mode}" "${path}" || member=$?
    fi
    case ${member} in
    0) files+=("./${path}") ;;
    1) ;;
    *)
        failure=${reason}
        break
        ;;
    esac
done
if [[ -n ${failure} ]]; then
    printf 'run-on-lint-files: %s; nothing was checked\n' "${failure}" >&2
    exit 2
fi
if ((${#files[@]} == 0)); then
    printf 'run-on-lint-files: the %s set lists no tracked file; nothing was checked\n' "${set_name}" >&2
    exit 2
fi
"$@" "${files[@]}"
