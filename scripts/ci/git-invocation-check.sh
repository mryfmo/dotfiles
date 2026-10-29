#!/usr/bin/env bash
# @file git-invocation-check.sh
# @brief Refuse a `git` word outside `git_isolated` in the levers, found on shfmt's syntax tree.
# @description
#   Regime-cutover U113 (plan P-22). The levers run git through scripts/orchestrator/git-isolated.sh, whose
#   `git_isolated` carries the one flag set that isolates git from the operator's and the repository's configuration.
#   This check parses each file with shfmt (`shfmt -ln bash --to-json`) and reports every word that is one plain
#   literal spelling `git` or a path ending in `/git`, wherever it stands under a statement: a command word, an
#   argument after `command`, `exec`, `env`, `bounded` or any other wrapper, an assignment value, an array element,
#   a redirect target, a word inside `$(…)`. The rule is structural, not a command-name match of the first word: the
#   wrappers are open-ended, and a `git` handed to one runs as surely as a bare one. Two shapes are accepted: a word
#   inside the `git_isolated` function of the library file itself, and a word whose statement spans a line carrying
#   `# git-isolated: allow <reason>`; an allow comment without a reason is itself a finding. A quoted `'git'` or
#   `"git …"` is a SglQuoted or DblQuoted part and is not a plain literal (`refuse 'git ls-files failed'` passes); a
#   heredoc body is one line-shaped literal and is not `git`; a `$(git …)` inside an unquoted heredoc body is code and
#   is reported.
#   Before any file is read, scripts/ci/shfmt_json_contract.py proves that the pinned shfmt still produces the node
#   kinds and fields this walk reads, and this walk then visits the contract fixtures itself and is refused if it sees
#   no command and no literal there (regime-cutover U105): "no findings" on the listed files is never "saw nothing".
#   A file shfmt cannot parse is refused, never read as clean. The enforced file set is a test,
#   tests/unit/test_git_invocation_check.py (the library and the five adopted levers); the other scripts under
#   scripts/orchestrator keep their own wrappers until a follow-up unit and are reported, not fixed.
# @arg $@ path The files to check.
# @description The shfmt is PATH's, the one scripts/ci/pinned-tool-version.sh checks ([tools."http:shfmt"], U97); no
#   variable selects another. The library is scripts/orchestrator/git-isolated.sh beside this script's repository,
#   recognised by file identity, so a copy elsewhere that defines its own `git_isolated` is reported.
# @exitcode 0 Every `git` word is inside the library's function or on an allowed statement.
# @exitcode 1 At least one finding, each printed as `file:line: …`.
# @exitcode 2 No file given, a listed file cannot be read or parsed, shfmt or python3 is missing, shfmt's JSON does not
#   match the pinned node table, or this walk visited no command or no literal in the contract fixtures: the list is
#   refused, never read as clean.
# @example
#   scripts/ci/git-invocation-check.sh scripts/orchestrator/git-isolated.sh scripts/orchestrator/records-sync.sh
set -euo pipefail

if (($# == 0)); then
    echo "git-invocation-check: no file to check; an empty list is refused" >&2
    exit 2
fi

for tool in shfmt python3; do
    if ! command -v "${tool}" > /dev/null; then
        echo "git-invocation-check: ${tool} not found; the list is refused" >&2
        exit 2
    fi
done

for file in "$@"; do
    if [[ ! -f ${file} || ! -r ${file} ]]; then
        echo "git-invocation-check: cannot read ${file}; the list is refused" >&2
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
import os
import subprocess
import sys

sys.path.insert(0, sys.argv[1])
import shfmt_json_contract as contract  # noqa: E402

MESSAGE = "a git call outside git_isolated; run it through the library, or carry `# git-isolated: allow <reason>`"
REASONLESS = "an allow comment without a reason; `# git-isolated: allow <reason>` names why this git is not isolated"
LIBRARY = os.path.join(sys.argv[1], os.pardir, os.pardir, "scripts", "orchestrator", "git-isolated.sh")
FUNCTION = "git_isolated"
MARKER = ["git-isolated:", "allow"]


def refuse(reason):
    print(f"git-invocation-check: {reason}; the list is refused", file=sys.stderr)
    sys.exit(2)


def is_git(word):
    """Whether the word is one plain literal spelling git, or a path ending in /git."""
    parts = word.get("Parts") or []
    if len(parts) != 1 or parts[0].get("Type") != "Lit":
        return False
    value = parts[0].get("Value") or ""
    return value == "git" or value.endswith("/git")


def walk(tree, library):
    """(commands seen, literals seen, [(line, statement lines) per git word], [(line, text) per comment]) of a tree.
    A git word inside the library's git_isolated function is left out; the statement lines are the innermost
    statement's, where an allow comment counts. Iterative: a long && chain nests deeper than Python recurses."""
    calls = lits = 0
    found = []
    comments = []
    todo = [(tree, None, False)]
    while todo:
        node, span, guarded = todo.pop()
        if isinstance(node, list):
            todo.extend((item, span, guarded) for item in node)
            continue
        if not isinstance(node, dict):
            continue
        kind = node.get("Type")
        name = (node.get("Name") or {}).get("Value")
        if kind == "CallExpr":
            calls += 1
        elif kind == "Lit":
            lits += 1
        if "Cmd" in node:
            span = (node["Pos"]["Line"], node["End"]["Line"])
        if "Hash" in node and "Text" in node:
            comments.append((node["Hash"]["Line"], node["Text"]))
        if kind == "FuncDecl" and library and name == FUNCTION:
            guarded = True
        if kind in (None, "Word") and "Parts" in node and is_git(node) and not guarded:
            found.append((node["Pos"]["Line"], span))
        todo.extend((value, span, guarded) for value in node.values())
    return calls, lits, found, comments


try:
    fixtures = contract.verified_trees()
except contract.ContractError as error:
    refuse(f"shfmt's JSON does not match the pinned node table ({error})")

# The contract proved the parser names the kinds; this proves the walk above still visits them, with its own
# traversal and type test, before a listed file is read. The fixtures' own findings are not reported.
seen_calls = seen_lits = 0
for source, tree in fixtures.items():
    try:
        calls, lits, _, _ = walk(tree, False)
    except Exception as error:  # a fixture the walk cannot read is "could not judge" for every listed file
        refuse(f"cannot walk the syntax tree of {source} ({error!r})")
    seen_calls += calls
    seen_lits += lits
if seen_calls == 0 or seen_lits == 0:
    refuse("the walk visited no command or no literal in the contract fixtures, which hold both")

status = 0
for file in sys.argv[2:]:
    try:
        with open(file, "rb") as handle:
            run = subprocess.run(["shfmt", "-ln", "bash", "--to-json"], stdin=handle, capture_output=True, check=False)
        library = os.path.exists(LIBRARY) and os.path.samefile(file, LIBRARY)
    except OSError as error:
        refuse(f"cannot read {file} ({error})")
    sys.stderr.write(run.stderr.decode(errors="replace"))
    if run.returncode != 0:
        refuse(f"shfmt cannot parse {file}")
    try:
        tree = json.loads(run.stdout)
    except ValueError:
        refuse(f"shfmt gave no JSON tree for {file}")
    try:
        _, _, found, comments = walk(tree, library)
    except Exception as error:  # any failure to read the tree is "could not judge", never a clean file
        refuse(f"cannot walk the syntax tree of {file} ({error!r})")
    # An allow comment is the marker's two words then the reason; the comment's text is split on blanks, no pattern.
    allowed = {}
    for line, text in comments:
        words = text.split()
        if words[:2] == MARKER:
            allowed[line] = words[2:]
    findings = set()
    for line, span in found:
        low, high = span or (line, line)
        if not any(allowed.get(at) for at in range(low, high + 1)):
            findings.add((line, MESSAGE))
    findings.update((line, REASONLESS) for line, reason in allowed.items() if not reason)
    for line, message in sorted(findings):
        print(f"{file}:{line}: {message}")
    status = 1 if findings else status
sys.exit(status)
PY
)

python3 -I -c "${walk}" "${here}" "$@"
