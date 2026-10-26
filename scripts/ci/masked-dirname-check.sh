#!/usr/bin/env bash
# @file masked-dirname-check.sh
# @brief Refuse a command substitution nested inside another one, the shape SC2312 lets through for dirname and basename.
# @description
#   ShellCheck's SC2312 (check-extra-masked-returns) exempts dirname and basename, so the U31 shape
#   `dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)` passes it although the inner status is
#   lost. This check parses each file with shfmt (`shfmt -ln bash --to-json`) and reports every
#   command substitution (`$(…)` or backquotes) that opens inside another one, as `file:line: …` at
#   the line where the inner one opens; capture the inner result first, or split a path in the shell
#   (`${path%/*}`, `${path##*/}`). The rule does not look at the command name: matching names lost
#   four audit rounds to spellings bash resolves at run time (`$'\544irname'`, `command -p dirname`,
#   `exec -a x dirname`, `/usr/bin/dirname`), and SC2312 already refuses the other commands in this
#   shape, so the linted groups held no nested substitution when the rule was set (regime-cutover
#   U38b). A heredoc body whose delimiter has any quoted or escaped part is literal and skipped, as
#   bash reads it (shfmt expands the body of a partly quoted delimiter such as `<<'E'OF`).
#   The files are parsed as bash: `make shellcheck` passes only bash scripts, and bash also parses
#   the repository's POSIX scripts. A file shfmt cannot parse is refused, never read as clean; that
#   includes a heredoc delimiter with ANSI-C escapes (`<<$'\x45OF'`), which shfmt 3.14.1 and
#   ShellCheck 0.11.0 both fail to terminate.
# @arg $@ path The files to check (the ShellCheck groups of `make shellcheck`).
# @description The shfmt is PATH's, the one scripts/ci/pinned-tool-version.sh checks before `make shellcheck`
#   runs this ([tools."http:shfmt"], U97); no variable selects another.
# @exitcode 0 No command substitution nested inside another.
# @exitcode 1 At least one finding, each printed as `file:line: …`.
# @exitcode 2 No file given, a listed file cannot be read or parsed, or shfmt or python3 is missing:
#   the list is refused, never read as clean.
# @example
#   scripts/ci/masked-dirname-check.sh scripts/orchestrator/hcom-seat
set -euo pipefail

if (($# == 0)); then
    echo "masked-dirname-check: no file to check; an empty list is refused" >&2
    exit 2
fi

for tool in shfmt python3; do
    if ! command -v "${tool}" > /dev/null; then
        echo "masked-dirname-check: ${tool} not found; the list is refused" >&2
        exit 2
    fi
done

for file in "$@"; do
    if [[ ! -f ${file} || ! -r ${file} ]]; then
        echo "masked-dirname-check: cannot read ${file}; the list is refused" >&2
        exit 2
    fi
done

# Reads shfmt's typed JSON on stdin; argv[1] names the file. Exits 1 when it prints a finding.
walk=$(
    cat << 'PY'
import json
import sys

MESSAGE = "a command substitution inside another one loses its status; capture it first, or split a path in the shell"


def quoted(word):
    """Whether any part of the word is quoted or escaped."""
    return any(
        part.get("Type") in ("SglQuoted", "DblQuoted") or (part.get("Type") == "Lit" and "\\" in part["Value"])
        for part in word.get("Parts") or []
    )


findings = set()


def walk(node, depth):
    if isinstance(node, list):
        for item in node:
            walk(item, depth)
        return
    if not isinstance(node, dict):
        return
    if node.get("Type") == "CmdSubst":
        if depth:
            findings.add(node["Pos"]["Line"])
        depth += 1
    elif node.get("Hdoc") and quoted(node["Word"]):
        # shfmt 3.14.1 parses the body of a partly quoted delimiter (`<<'E'OF`, `<<E"O"F`) as expanded text;
        # bash makes the body literal once any part of the delimiter is quoted.
        node = {key: value for key, value in node.items() if key != "Hdoc"}
    for value in node.values():
        walk(value, depth)


walk(json.load(sys.stdin), 0)
for line in sorted(findings):
    print(f"{sys.argv[1]}:{line}: {MESSAGE}")
sys.exit(1 if findings else 0)
PY
)

status=0
for file in "$@"; do
    if ! tree=$(shfmt -ln bash --to-json < "${file}"); then
        echo "masked-dirname-check: shfmt cannot parse ${file}; the list is refused" >&2
        exit 2
    fi
    python3 -c "${walk}" "${file}" <<< "${tree}" || {
        code=$?
        if ((code != 1)); then
            echo "masked-dirname-check: cannot walk the syntax tree of ${file} (python3 exit ${code}); the list is refused" >&2
            exit 2
        fi
        status=1
    }
done
exit "${status}"
