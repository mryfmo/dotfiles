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
#   bash reads it (shfmt expands the body of a partly quoted delimiter such as `<<'E'OF`;
#   tests/fixtures/shfmt-json/heredoc-partly-quoted-delimiter holds that case).
#   The files are parsed as bash: `make shellcheck` passes only bash scripts, and bash also parses
#   the repository's POSIX scripts. A file shfmt cannot parse is refused, never read as clean; that
#   includes a heredoc delimiter with ANSI-C escapes (`<<$'\x45OF'`), which shfmt 3.14.1 and
#   ShellCheck 0.11.0 both fail to terminate (tests/fixtures/shfmt-json/heredoc-ansi-c-delimiter).
#   Before any file is read, scripts/ci/shfmt_json_contract.py proves that the pinned shfmt still
#   produces the node kinds and fields this walk reads (regime-cutover U105); and a run that visited
#   no command substitution at all, while the contract fixture holds some, is refused rather than
#   read as clean, so "no findings" is never "saw nothing".
# @arg $@ path The files to check (the ShellCheck groups of `make shellcheck`).
# @description The shfmt is PATH's, the one scripts/ci/pinned-tool-version.sh checks before `make shellcheck`
#   runs this ([tools."http:shfmt"], U97); no variable selects another.
# @exitcode 0 No command substitution nested inside another.
# @exitcode 1 At least one finding, each printed as `file:line: …`.
# @exitcode 2 No file given, a listed file cannot be read or parsed, shfmt or python3 is missing, shfmt's JSON
#   does not match the pinned node table, or the walk visited no command substitution: the list is
#   refused, never read as clean.
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

# The directory of this script, where scripts/ci/shfmt_json_contract.py lives: a parameter expansion, so no
# producer's status is at stake.
case ${BASH_SOURCE[0]} in
*/*) here=${BASH_SOURCE[0]%/*} ;;
*) here=. ;;
esac

# Runs the contract, then parses each file with shfmt and walks its typed JSON. argv[1] is the directory of
# shfmt_json_contract.py, the rest are the files. Exits 1 when it prints a finding, 2 when the list is refused.
walk=$(
    cat << 'PY'
import json
import subprocess
import sys

sys.path.insert(0, sys.argv[1])
import shfmt_json_contract as contract  # noqa: E402

MESSAGE = "a command substitution inside another one loses its status; capture it first, or split a path in the shell"


def refuse(reason):
    print(f"masked-dirname-check: {reason}; the list is refused", file=sys.stderr)
    sys.exit(2)


def quoted(word):
    """Whether any part of the word is quoted or escaped."""
    return any(
        part.get("Type") in ("SglQuoted", "DblQuoted") or (part.get("Type") == "Lit" and "\\" in part["Value"])
        for part in word.get("Parts") or []
    )


try:
    contract.verify()
except contract.ContractError as error:
    refuse(f"shfmt's JSON does not match the pinned node table ({error})")

findings = set()
substitutions = 0


def walk(node, depth):
    global substitutions
    if isinstance(node, list):
        for item in node:
            walk(item, depth)
        return
    if not isinstance(node, dict):
        return
    if node.get("Type") == "CmdSubst":
        substitutions += 1
        if depth:
            findings.add(node["Pos"]["Line"])
        depth += 1
    elif node.get("Hdoc") and quoted(node["Word"]):
        # shfmt 3.14.1 parses the body of a partly quoted delimiter (`<<'E'OF`, `<<E"O"F`) as expanded text;
        # bash makes the body literal once any part of the delimiter is quoted.
        node = {key: value for key, value in node.items() if key != "Hdoc"}
    for value in node.values():
        walk(value, depth)


status = 0
for file in sys.argv[2:]:
    try:
        with open(file, "rb") as handle:
            run = subprocess.run(["shfmt", "-ln", "bash", "--to-json"], stdin=handle, capture_output=True, check=False)
    except OSError as error:
        refuse(f"cannot read {file} ({error})")
    sys.stderr.write(run.stderr.decode(errors="replace"))
    if run.returncode != 0:
        refuse(f"shfmt cannot parse {file}")
    try:
        tree = json.loads(run.stdout)
    except ValueError:
        refuse(f"shfmt gave no JSON tree for {file}")
    findings.clear()
    try:
        walk(tree, 0)
    except Exception as error:  # any failure to read the tree is "could not judge", never a clean file
        refuse(f"cannot walk the syntax tree of {file} ({error!r})")
    for line in sorted(findings):
        print(f"{file}:{line}: {MESSAGE}")
    status = 1 if findings else status
if substitutions == 0:
    refuse("the walk visited no command substitution in the listed files, while the contract fixture holds some")
sys.exit(status)
PY
)

python3 -I -c "${walk}" "${here}" "$@"
