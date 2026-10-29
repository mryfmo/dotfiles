#!/usr/bin/env bash
# @file producer-status-check.sh
# @brief Refuse a command substitution outside the accepted grammar, a status-blind producer without its stderr capture, a missing `set -euo pipefail`, and a `read` from a file.
# @description
#   Regime-cutover U112 (plan P-21): standing order 21 made checkable. ShellCheck's check-extra-masked-returns
#   never flags a plain `x=$(producer)`, never looks at a file redirection, exempts echo, dirname, basename, printf,
#   set and shopt, and sees nothing when a producer exits 0 on a partial failure. This check parses each file with
#   shfmt (`shfmt -ln bash --to-json`) and walks its typed tree under five rules, each a closed set; a finding is
#   printed as `file:line: <rule>: <message>`:
#   a. `substitution`: a command substitution (`$(…)` or backquotes) is accepted only as the whole value of the one
#      assignment of a statement with no command word, where that statement is the last of an `if` or `while`
#      condition (negated or not) or the left side of a `||` whose right side is not `true`, `:` or `false`. Every
#      other position is a finding at the line where the substitution opens: an argument, a `local`, `export`,
#      `declare` or `readonly`, a redirect target, an unquoted heredoc body, `[[ ]]`, an arithmetic expansion, a
#      `for` list, a `case` word, a plain assignment whose status only `set -e` sees, two assignments in one
#      statement, and a substitution inside another one.
#   b. `producer`: a command whose leading words (bare literals) match a row of status-blind-producers.tsv beside
#      this script (`git ls-files`, `git config -f`, `git config --file`, `find`, `ls`) must send its stderr with
#      `2>` to a file other than /dev/null, and a later statement of the same list must be `[[ ! -s <that file> ]]`
#      (the words compared by their parts, quotes aside); `read_listing` of scripts/orchestrator/read-lib.sh is that
#      shape by construction, and a producer the table does not name is not held to this rule.
#   c. `prologue`: the file runs `set -euo pipefail` at top level before its first statement holding a command
#      substitution (a function body counts), else a finding at line 1. `shopt -s inherit_errexit` is not required:
#      bash 3.2 has no such option.
#   d. `read`: a `read` that carries its own `<` redirect is a finding naming `read_file` (`done < file` redirects
#      the loop, not the `read`; a here-string is not a file).
#   e. `allow`: `# producer-status: allow <reason>` on the statement's first line exempts that statement from a, b
#      and d; an allow comment with no reason is itself a finding and exempts nothing. The enforced file set is
#      tests/unit/test_producer_status_check.py (the library and the five levers), not a Makefile target.
#   A heredoc body whose delimiter has any quoted or escaped part is literal and skipped, as bash reads it (shfmt
#   expands the body of a partly quoted delimiter such as `<<'E'OF`). The files are parsed as bash. A file shfmt
#   cannot parse is refused, never read as clean. Before any listed file is read, scripts/ci/shfmt_json_contract.py
#   proves that the pinned shfmt still produces the node kinds and fields this walk reads, and this walk then visits
#   the contract fixtures itself and is refused if it sees no statement, no assignment or no command substitution
#   there (regime-cutover U105): "no findings" on the listed files is never "saw nothing".
# @arg $@ path The files to check.
# @description The shfmt is PATH's, the one scripts/ci/pinned-tool-version.sh checks ([tools."http:shfmt"], U97);
#   no variable selects another, and no variable selects another producer table.
# @exitcode 0 No finding.
# @exitcode 1 At least one finding, each printed as `file:line: <rule>: <message>`.
# @exitcode 2 No file given, a listed file cannot be read or parsed, shfmt or python3 is missing, shfmt's JSON does
#   not match the pinned node table, the producer table is missing or malformed, or this walk saw no statement in a
#   listed file or none of its kinds in the contract fixtures: the list is refused, never read as clean.
# @example
#   scripts/ci/producer-status-check.sh scripts/orchestrator/read-lib.sh scripts/orchestrator/records-sync.sh
set -euo pipefail

if (($# == 0)); then
    echo "producer-status-check: no file to check; an empty list is refused" >&2
    exit 2
fi

for tool in shfmt python3; do
    if ! command -v "${tool}" > /dev/null; then
        echo "producer-status-check: ${tool} not found; the list is refused" >&2
        exit 2
    fi
done

for file in "$@"; do
    if [[ ! -f ${file} || ! -r ${file} ]]; then
        echo "producer-status-check: cannot read ${file}; the list is refused" >&2
        exit 2
    fi
done

# The directory of this script, where scripts/ci/shfmt_json_contract.py and the producer table live: a parameter
# expansion, so no producer's status is at stake.
case ${BASH_SOURCE[0]} in
*/*) here=${BASH_SOURCE[0]%/*} ;;
*) here=. ;;
esac
table=${here}/status-blind-producers.tsv
if [[ ! -f ${table} || ! -r ${table} ]]; then
    echo "producer-status-check: cannot read the producer table ${table}; the list is refused" >&2
    exit 2
fi

# Runs the contract, reads the producer table, then parses each file with shfmt and walks its typed JSON. argv[1]
# is the directory of shfmt_json_contract.py, argv[2] the producer table, the rest are the files. Exits 1 when it
# prints a finding, 2 when the list is refused.
walk=$(
    cat << 'PY'
import json
import subprocess
import sys
from collections import Counter

sys.path.insert(0, sys.argv[1])
import shfmt_json_contract as contract  # noqa: E402

NAME = "producer-status-check"
TABLE = sys.argv[2]
SUBSTITUTION, PRODUCER, PROLOGUE, READ, ALLOW = "substitution", "producer", "prologue", "read", "allow"
MESSAGES = {
    SUBSTITUTION: (
        "a command substitution here loses its status; make it the whole value of the one assignment of a statement "
        "that `if`, `while` or `||` tests, or read through read-lib.sh"
    ),
    READ: "`read` from a file takes a failed read for the end of the file; use read_file of read-lib.sh",
    ALLOW: "`# producer-status: allow` needs a reason after it",
}
ALLOW_WORDS = ["producer-status:", "allow"]
TRIVIAL = ("true", ":", "false")  # `|| true`, `|| :` and `|| false` discard the status of what precedes them
PROLOGUE_WORDS = ["set", "-euo", "pipefail"]


def refuse(reason):
    print(f"{NAME}: {reason}; the list is refused", file=sys.stderr)
    sys.exit(2)


def producers():
    """The rows of the status-blind producer table, each the list of its leading words."""
    try:
        with open(TABLE, encoding="utf-8") as handle:
            lines = handle.read().split("\n")
    except (OSError, UnicodeDecodeError) as error:
        refuse(f"cannot read the producer table {TABLE} ({error})")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or lines[0] != "words\tmeasured\tsource":
        refuse(f"{TABLE} does not start with the header words, measured, source")
    rows = []
    for number, line in enumerate(lines[1:], 2):
        cells = line.split("\t")
        if len(cells) != 3 or any(not cell.strip() for cell in cells) or cells[0] != " ".join(cells[0].split()):
            refuse(f"malformed row {number} of {TABLE} (three non-empty tab-separated cells, the words single-spaced)")
        rows.append(cells[0].split(" "))
    if not rows:
        refuse(f"{TABLE} holds no producer row")
    return rows


def every(tree):
    """Every JSON object at or below tree, iteratively: a long && chain nests deeper than Python recurses."""
    todo = [tree]
    while todo:
        node = todo.pop()
        if isinstance(node, dict):
            yield node
            todo.extend(node.values())
        elif isinstance(node, list):
            todo.extend(node)


def quoted(word):
    """Whether any part of the word is quoted or escaped."""
    return any(
        part.get("Type") in ("SglQuoted", "DblQuoted") or (part.get("Type") == "Lit" and "\\" in part["Value"])
        for part in word.get("Parts") or []
    )


def without_literal_body(redirect):
    """The redirect without the body of a heredoc whose delimiter is quoted or escaped: bash reads that body as
    literal text, while shfmt 3.14.1 parses the body of a partly quoted delimiter (`<<'E'OF`, `<<E"O"F`) as expanded
    text. Any other node is returned as it is."""
    if redirect.get("Hdoc") and quoted(redirect["Word"]):
        return {key: value for key, value in redirect.items() if key != "Hdoc"}
    return redirect


def command_of(stmt):
    """The command a statement runs, else None."""
    return stmt.get("Cmd") if isinstance(stmt, dict) else None


def literal(word):
    """The text of a word that is one bare literal, else None."""
    parts = (word.get("Parts") or []) if isinstance(word, dict) else []
    if len(parts) == 1 and parts[0].get("Type") == "Lit":
        return parts[0]["Value"]
    return None


def leading_words(call):
    """The leading arguments of a call that are bare literals, as text."""
    words = []
    for arg in call.get("Args") or []:
        text = literal(arg)
        if text is None:
            break
        words.append(text)
    return words


def whole_substitution(word):
    """The command substitution that is the whole word (bare, or alone inside double quotes), else None."""
    parts = (word.get("Parts") or []) if isinstance(word, dict) else []
    if len(parts) == 1 and parts[0].get("Type") == "DblQuoted":
        parts = parts[0].get("Parts") or []
    if len(parts) == 1 and parts[0].get("Type") == "CmdSubst":
        return parts[0]
    return None


def position(value):
    return isinstance(value, dict) and set(value) == {"Offset", "Line", "Col"}


def without_positions(node):
    """The node without its position records, so two spellings of one word compare by their parts."""
    if isinstance(node, dict):
        return {key: without_positions(value) for key, value in node.items() if not position(value)}
    if isinstance(node, list):
        return [without_positions(item) for item in node]
    return node


def word_parts(word):
    """The parts of a word with its double quotes flattened and positions dropped: what the file name is made of."""
    parts = []
    for part in word.get("Parts") or []:
        if part.get("Type") == "DblQuoted":
            parts.extend(word_parts(part))
        else:
            parts.append(without_positions(part))
    return parts


def head(stmt):
    """The command a statement runs first: the leftmost operand of a `||`, `&&` or `|` chain, else its own command."""
    cmd = command_of(stmt)
    while isinstance(cmd, dict) and cmd.get("Type") == "BinaryCmd":
        cmd = command_of(cmd["X"])
    return cmd


def trivial(stmt):
    """Whether the statement is `true`, `:` or `false`, which discard the status of what precedes a `||`."""
    cmd = command_of(stmt)
    if not isinstance(cmd, dict) or cmd.get("Type") != "CallExpr":
        return False
    words = leading_words(cmd)
    return bool(words) and words[0] in TRIVIAL


def tested_assignment(stmt):
    """The substitution a statement in a tested position captures: the whole value of its one assignment, when the
    statement has no command word; else None."""
    cmd = command_of(stmt)
    if not isinstance(cmd, dict) or cmd.get("Type") != "CallExpr" or cmd.get("Args"):
        return None
    assigns = cmd.get("Assigns") or []
    if len(assigns) != 1 or "Name" not in assigns[0]:
        return None
    return whole_substitution(assigns[0].get("Value"))


def prologue_statement(stmt):
    """Whether the statement is exactly `set -euo pipefail`."""
    cmd = stmt.get("Cmd") if isinstance(stmt, dict) else None
    if not isinstance(cmd, dict) or cmd.get("Type") != "CallExpr" or cmd.get("Assigns"):
        return False
    return leading_words(cmd) == PROLOGUE_WORDS and len(cmd.get("Args") or []) == len(PROLOGUE_WORDS)


class Walk:
    """One walk of a tree: the findings it reports and the node kinds it visited."""

    def __init__(self, rows):
        self.rows = rows
        self.seen = Counter()
        self.findings = set()
        self.accepted = set()  # ids of the command substitutions in an accepted position
        self.allowed = set()  # lines carrying `# producer-status: allow <reason>`
        self.top = []
        self.top_index = 0
        self.first_substitution = None  # the index of the top-level statement holding the first substitution

    def run(self, tree):
        self.seen.clear()
        self.findings.clear()
        self.accepted.clear()
        self.allowed.clear()
        self.top = tree.get("Stmts") or []
        self.top_index = 0
        self.first_substitution = None
        self.comments(tree)
        self.accept(tree)
        self.visit(tree, None, None)
        self.prologue()
        return sorted(self.findings)

    def comments(self, tree):
        for node in every(tree):
            if "Hash" in node and isinstance(node.get("Text"), str):
                words = node["Text"].split()
                if words[:2] == ALLOW_WORDS:
                    if len(words) > 2:
                        self.allowed.add(node["Hash"]["Line"])
                    else:
                        self.findings.add((node["Hash"]["Line"], ALLOW, MESSAGES[ALLOW]))

    def accept(self, tree):
        """Mark the substitutions in the two accepted positions: the last statement of an `if` or `while` condition,
        and the left side of a `||` whose right side keeps the status."""
        for node in every(tree):
            kind = node.get("Type")
            # An `elif` is an IfClause with no Type key (shfmt types only interface fields); its Cond marks it.
            if kind in ("IfClause", "WhileClause") or (kind is None and "Cond" in node):
                candidates = (node.get("Cond") or [])[-1:]
            elif kind == "BinaryCmd" and node.get("Op") == "||" and not trivial(node["Y"]):
                candidates = [node["X"]]
            else:
                continue
            for stmt in candidates:
                substitution = tested_assignment(stmt)
                if substitution is not None:
                    self.accepted.add(id(substitution))

    def report(self, stmt, line, rule, message):
        if stmt is not None and stmt["Pos"]["Line"] in self.allowed:
            return
        self.findings.add((line, rule, message))

    def visit(self, node, stmt, siblings):
        """Depth first; stmt is the innermost statement holding node, siblings the statement list it sits in and its
        index there (the list a later `[[ ! -s file ]]` is searched in)."""
        if isinstance(node, list):
            for item in node:
                self.visit(item, stmt, siblings)
            return
        if not isinstance(node, dict):
            return
        kind = node.get("Type")
        if kind is None and "Cmd" in node:
            self.seen["Stmt"] += 1
            stmt = node
            if siblings is not None and siblings[0] is self.top:
                self.top_index = siblings[1]
            self.statement(node, siblings)
        elif kind is None and "Name" in node:
            self.seen["Assign"] += 1
        elif kind == "CmdSubst":
            self.seen["CmdSubst"] += 1
            if self.first_substitution is None:
                self.first_substitution = self.top_index
            if id(node) not in self.accepted:
                self.report(stmt, node["Pos"]["Line"], SUBSTITUTION, MESSAGES[SUBSTITUTION])
        node = without_literal_body(node)
        for value in node.values():
            if isinstance(value, list) and any(isinstance(item, dict) and "Cmd" in item for item in value):
                for index, item in enumerate(value):
                    self.visit(item, stmt, (value, index))
            else:
                self.visit(value, stmt, siblings)

    def statement(self, stmt, siblings):
        """Rules b and d on one statement's own command."""
        cmd = stmt.get("Cmd")
        if not isinstance(cmd, dict) or cmd.get("Type") != "CallExpr":
            return
        words = leading_words(cmd)
        redirects = stmt.get("Redirs") or []
        if words[:1] == ["read"] and any(redirect.get("Op") == "<" for redirect in redirects):
            self.report(stmt, stmt["Pos"]["Line"], READ, MESSAGES[READ])
        for row in self.rows:
            if words[: len(row)] != row:
                continue
            target = None
            for redirect in redirects:
                if redirect.get("Op") == ">" and (redirect.get("N") or {}).get("Value") == "2":
                    target = None if literal(redirect["Word"]) == "/dev/null" else redirect["Word"]
            later = siblings[0][siblings[1] + 1 :] if siblings is not None else []
            if target is None or not any(self.tests_empty(other, target) for other in later):
                self.report(
                    stmt,
                    stmt["Pos"]["Line"],
                    PRODUCER,
                    f"`{' '.join(row)}` can fail with exit 0 or after printing (status-blind-producers.tsv); send its "
                    "stderr with `2>` to a file and test `[[ ! -s <that file> ]]` in a later statement of the same "
                    "list, or run it through read_listing of read-lib.sh",
                )
            break

    def tests_empty(self, stmt, target):
        """Whether the statement starts with `[[ ! -s <target> ]]`."""
        cmd = head(stmt)
        if not isinstance(cmd, dict) or cmd.get("Type") != "TestClause":
            return False
        test = cmd.get("X")
        if not isinstance(test, dict) or test.get("Type") != "UnaryTest" or test.get("Op") != "!":
            return False
        inner = test.get("X")
        if not isinstance(inner, dict) or inner.get("Type") != "UnaryTest" or inner.get("Op") != "-s":
            return False
        return word_parts(inner["X"]) == word_parts(target)

    def prologue(self):
        """Rule c: `set -euo pipefail` at top level before the first statement holding a substitution."""
        if self.first_substitution is None:
            return
        if any(prologue_statement(stmt) for stmt in self.top[: self.first_substitution]):
            return
        line = self.top[self.first_substitution]["Pos"]["Line"]
        self.findings.add(
            (
                1,
                PROLOGUE,
                "`set -euo pipefail` must run at top level before the first statement holding a command "
                f"substitution (line {line})",
            )
        )


try:
    fixtures = contract.verified_trees()
except contract.ContractError as error:
    refuse(f"shfmt's JSON does not match the pinned node table ({error})")

walk = Walk(producers())
# The contract proved the parser names the kinds; this proves the walk above still visits them, with its own
# traversal and type tests, before a listed file is read. The fixtures' own findings are not reported.
visited = Counter()
for source, tree in fixtures.items():
    try:
        walk.run(tree)
    except Exception as error:  # a fixture the walk cannot read is "could not judge" for every listed file
        refuse(f"cannot walk the syntax tree of {source} ({error!r})")
    visited.update(walk.seen)
for kind in ("Stmt", "Assign", "CmdSubst"):
    if not visited[kind]:
        refuse(f"the walk visited no {kind} node in the contract fixtures, which hold some")

status = 0
for file in sys.argv[3:]:
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
    try:
        findings = walk.run(tree)
    except Exception as error:  # any failure to read the tree is "could not judge", never a clean file
        refuse(f"cannot walk the syntax tree of {file} ({error!r})")
    listed = len(tree.get("Stmts") or []) if isinstance(tree, dict) else 0
    if listed and not walk.seen["Stmt"]:
        refuse(f"the walk saw none of the {listed} top-level statement(s) of {file}")
    for line, rule, message in findings:
        print(f"{file}:{line}: {rule}: {message}")
    status = 1 if findings else status
sys.exit(status)
PY
) || {
    echo "producer-status-check: cannot read the embedded walk; the list is refused" >&2
    exit 2
}

python3 -I -c "${walk}" "${here}" "${table}" "$@"
