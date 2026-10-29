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
#      condition (negated or not) or the left side of a `||` whose branch handles the status, and the tested
#      statement itself runs in the foreground and, under `||`, is not negated: `! x=$(…) || exit 1` reads the
#      failure as success, `x=$(…) || exit 1 &` ends only the background job, `coproc x=$(…) || exit 1` tests the
#      coprocess's start, and each is a finding naming that. The branches that handle the status are a closed list:
#      (i) a plain command whose known first word is `exit` or `return`, with no argument (the status of the failed
#      substitution propagates, so only as the whole branch or as the only statement of its block or subshell), with
#      one argument whose known text is a decimal from 1 to 255, or with one argument that is the bare `$?` (`exit
#      0`, `exit "$x"`, `exit $(cmd)`, `exit 1 2` and `return 0` are findings: a zero turns the failed read into
#      success); (ii) a plain command whose known first word names a function this file defines at top level and
#      whose body's last statement is form (i) with an explicit argument (one level, no recursion; a name no
#      top-level function defines is not accepted; a bare `exit` or `return` there passes on the status of the
#      body's earlier command, and the finding names that command); (iii) a block or subshell whose last statement is
#      (i) or (ii), the bare form only as its only statement; (iv) a bare assignment of exactly `$?` (`status=$?`).
#      A branch statement run in the background (`exit 2 &`) handles nothing.
#      Any other branch leaves the substitution a finding that names the branch's shape: a pipeline, an `&&` or `||`
#      list, an `if`, a `case`, `true`, `:`, `false` or any other plain command, a block or subshell ending
#      otherwise, an assignment of anything else, a first word with no known text. A later line that handles an
#      empty value is not a branch: such a read carries `# producer-status: allow <reason naming that line>` (rule
#      e). A word has a known text only when every part is a bare literal over the closed character set (letters,
#      digits and `_ - . / : = + @ % ,`), a plain single-quoted string, or double quotes around literals (any
#      character there) and such strings; `* ? [ ] { } ~ $`, a backquote, a backslash, whitespace or any other
#      character in a bare literal, an expansion, an ANSI-C `$'…'` or a locale `$"…"` string make the word unknown,
#      and nothing is decoded. Every other position is a finding at the line where the substitution opens: an
#      argument, a `local`, `export`, `declare` or `readonly`, a redirect target, an unquoted heredoc body, `[[ ]]`,
#      an arithmetic expansion, a `for` list, a `case` word, a plain assignment whose status only `set -e` sees, two
#      assignments in one statement, and a substitution inside another one.
#   b. `producer`: a command whose leading words (known texts, as above) match a row of status-blind-producers.tsv
#      beside this script (`git ls-files`, `git config -f`, `git config --file`, `find`, `ls`) must capture its
#      stderr to a file, and a later statement of the same list must be `[[ ! -s <that file> ]]`. Stderr is captured
#      only when the last redirect of the statement that touches fd 2 is `2>`, `2>>` or `2>|` to a word whose known
#      text is not /dev/null, or whose parts are literals and parameter expansions. A redirect touches fd 2 when its
#      descriptor is 2 whatever the operator, when it is `&>` or `&>>`, or when it is `>&` to a word that is not a
#      descriptor; any other operator there (`2>&N`, `2<&-`, `2<`, `2<>`, `2<<<`, `&>`, `>&file`, one shfmt adds
#      later) leaves stderr uncaptured. The tested word names the same file only when both texts are known and
#      equal, or both hold a parameter expansion and their parts are equal. `read_listing` of
#      scripts/orchestrator/read-lib.sh is that shape by construction, and a producer the table does not name is not
#      held to this rule.
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
#   not match the pinned node table, the producer table is missing or malformed, a listed file holds no statement
#   (empty or comment-only), or this walk saw none of a listed file's statements or none of its kinds in the contract
#   fixtures: the list is refused, never read as clean.
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
TERMINATORS = ("exit", "return")  # the plain commands that end the read when the tested substitution fails (form i)
FAILURE_STATUSES = range(1, 256)  # the one argument of a terminator, when its text is known, is a decimal in this range
# A bare literal is a known text only over this set: a glob character, a brace, a tilde, `$`, a backquote, a backslash
# or whitespace is expanded or read by bash and is not decoded here. Inside double quotes bash expands none of them,
# so the set does not apply there.
KNOWN_CHARACTERS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-./:=+@%,")
# The last status as a whole word, `$?` or `${?}` (form iv); `${?:-0}` and `"$?"` are not it.
STATUS_PARAMETERS = (
    {"Type": "ParamExp", "Short": True, "Param": {"Value": "?"}},
    {"Type": "ParamExp", "Param": {"Value": "?"}},
)
# A tested read whose statement does not run in the foreground, or is negated under `||`: its failure stops nothing.
FLAGS = {
    "Negated": "the tested read is negated (`!`), so its failure is read as success and the `||` branch does not run",
    "Background": "the tested read runs in the background (`&`), so its failure stops nothing: the test sees the job",
}
COPROCESS = "the tested read runs as a coprocess (`coproc`), whose status is read before the read ends"
BACKGROUND_BRANCH = "a command run in the background (`&`), which lets the script go on"
IN_FUNCTION = object()  # the `before` of a bare `exit` or `return` that is a function body's only statement
SHAPES = {  # how a finding names the command kind of a branch; a kind not listed is named by shfmt's type
    "Block": "a block",
    "Subshell": "a subshell",
    "IfClause": "an `if`",
    "CaseClause": "a `case`",
    "WhileClause": "a `while`",
    "ForClause": "a `for`",
    "DeclClause": "a declaration",
    "FuncDecl": "a function definition",
    "TestClause": "a `[[ ]]` test",
    "ArithmCmd": "an arithmetic command",
    "TimeClause": "a `time`",
    "CoprocClause": "a `coproc`",
}
LIST_SHAPES = {"|": "a pipeline", "&&": "an `&&` list", "||": "a `||` list"}
PROLOGUE_WORDS = ["set", "-euo", "pipefail"]
STDERR = "2"
FILE_OPS = (">", ">>", ">|")  # the only operators that, on fd 2, capture stderr to the word's file
BOTH_OPS = ("&>", "&>>")  # touch fd 2 with no descriptor written
DUP_OP = ">&"  # with no descriptor written, `>&file` touches fd 2; `>&N` and `>&-` move only stdout
UNCAPTURED = object()  # the stderr target when the last redirect touching fd 2 is not one of FILE_OPS
NAME_KINDS = ("ParamExp",)  # the one expansion a file name may hold: two such words compare by their parts
DEVNULL = "/dev/null"
DOUBLE_QUOTE_ESCAPES = '$`"\\\n'  # inside double quotes bash removes a backslash before these only


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


def unescaped(value):
    """A double-quoted literal's value without the backslashes bash removes when it reads the word: those before `$`,
    a backquote, a double quote, a backslash or a newline."""
    out = []
    index = 0
    while index < len(value):
        if value[index] == "\\" and index + 1 < len(value) and value[index + 1] in DOUBLE_QUOTE_ESCAPES:
            index += 1
        out.append(value[index])
        index += 1
    return "".join(out)


def word_text(word, in_double_quotes=False):
    """The known text of a word: every part a bare literal over KNOWN_CHARACTERS, a plain single-quoted string, or
    double quotes around literals (any character, their escapes removed) and such strings (`true`, 'true' and "true"
    are one text). None for any other word, whose text exists only when it runs: a bare literal with a glob, a brace,
    a tilde, a backslash or another character outside the set, an expansion, an ANSI-C `$'…'` or a locale `$"…"`
    string (shfmt's Dollar); nothing is decoded."""
    parts = (word.get("Parts") or []) if isinstance(word, dict) else []
    text = ""
    for part in parts:
        kind = part.get("Type")
        if kind == "Lit":
            value = part.get("Value") or ""
            if in_double_quotes:
                text += unescaped(value)
            elif set(value) <= KNOWN_CHARACTERS:
                text += value
            else:
                return None
        elif kind == "SglQuoted" and not part.get("Dollar"):
            text += part.get("Value") or ""  # shfmt writes no Value for ''
        elif kind == "DblQuoted" and not part.get("Dollar"):
            inner = word_text(part, True)
            if inner is None:
                return None
            text += inner
        else:
            return None
    return text


def descriptor(word):
    """Whether the word of a `>&` names a descriptor (`1`, `-`), so the redirect duplicates stdout and leaves stderr
    alone; a word with no known text is not shown to, so it counts as `>&file`."""
    text = word_text(word)
    return text is not None and (text.isdigit() or text == "-")


def touches_stderr(redirect):
    """Whether the redirect moves fd 2: its descriptor is 2 whatever the operator, it is `&>` or `&>>`, or it is `>&`
    with no descriptor written to a word that is not one (`>&file` sends both streams there; `>&2` moves stdout)."""
    fd = (redirect.get("N") or {}).get("Value")
    if fd is not None:
        return fd == STDERR
    op = redirect.get("Op")
    return op in BOTH_OPS or (op == DUP_OP and not descriptor(redirect["Word"]))


def stderr_target(redirects):
    """Where a statement's stderr ends up, decided by the last redirect that touches fd 2: the word when that redirect
    is `2>`, `2>>` or `2>|`, UNCAPTURED for any other (`2>&N`, `2<&-`, `2<`, `2<>`, `2<<<`, `&>`, `>&file`, an
    operator shfmt adds later), None when no redirect touches it."""
    target = None
    for redirect in redirects:
        if touches_stderr(redirect):
            captures = redirect.get("Op") in FILE_OPS and (redirect.get("N") or {}).get("Value") == STDERR
            target = redirect["Word"] if captures else UNCAPTURED
    return target


def leading_words(call):
    """The leading arguments of a call that are made of literals, as text, quoting aside."""
    words = []
    for arg in call.get("Args") or []:
        text = word_text(arg)
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


def name_parts(word, in_double_quotes=False):
    """The parts of a word that names a file only when it runs, double quotes flattened and positions dropped, when
    every part is a literal (bare, over KNOWN_CHARACTERS), a plain quoted string or a parameter expansion; None for
    any other word (a bare glob, brace or tilde, an ANSI-C or locale string, a substitution), which is not shown to
    name any file."""
    parts = []
    for part in word.get("Parts") or []:
        kind = part.get("Type")
        if kind == "DblQuoted" and not part.get("Dollar"):
            inner = name_parts(part, True)
            if inner is None:
                return None
            parts.extend(inner)
        elif kind == "Lit":
            if not in_double_quotes and not set(part.get("Value") or "") <= KNOWN_CHARACTERS:
                return None
            parts.append(without_positions(part))
        elif (kind == "SglQuoted" and not part.get("Dollar")) or kind in NAME_KINDS:
            parts.append(without_positions(part))
        else:
            return None
    return parts


def same_word(one, other):
    """Whether two words are shown to name one file: both with a known text and the texts equal, or both naming a file
    only when they run and their parts equal (`"${d}/err"` and `${d}/err`; `'${d}/err'` is a known text, another
    file). A known text and a run-time name are never shown to be one file."""
    texts = (word_text(one), word_text(other))
    if None not in texts:
        return texts[0] == texts[1]
    if texts != (None, None):
        return False
    parts = (name_parts(one), name_parts(other))
    return None not in parts and parts[0] == parts[1]


def captures_to_file(target):
    """Whether the word of a `2>`, `2>>` or `2>|` names a file that holds stderr: a known text other than /dev/null, or
    a name made of literals and parameter expansions; an ANSI-C string or any other word is not shown to."""
    text = word_text(target)
    if text is not None:
        return text != DEVNULL
    return name_parts(target) is not None


def head(stmt):
    """The command a statement runs first: the leftmost operand of a `||`, `&&` or `|` chain, else its own command."""
    cmd = command_of(stmt)
    while isinstance(cmd, dict) and cmd.get("Type") == "BinaryCmd":
        cmd = command_of(cmd["X"])
    return cmd


def top_level_functions(tree):
    """The functions the file defines at top level, name -> its bodies (a name defined twice has two, and each must
    end the read); a function defined inside another statement is not one of them."""
    functions = {}
    for stmt in tree.get("Stmts") or []:
        cmd = command_of(stmt)
        if isinstance(cmd, dict) and cmd.get("Type") == "FuncDecl":
            functions.setdefault(cmd["Name"]["Value"], []).append(cmd["Body"])
    return functions


def body_statements(stmt):
    """The statements a function body or a `||` branch runs: a block's or subshell's list, else the statement itself
    (`f() exit 2`, a plain command)."""
    cmd = command_of(stmt)
    if isinstance(cmd, dict) and cmd.get("Type") in ("Block", "Subshell"):
        return cmd.get("Stmts") or []
    return [stmt]


def statement_name(stmt):
    """How a finding names the statement before a bare `exit` or `return`: the command's known first word, else its
    shape (an assignment, a list, a block, an `if`, a command whose first word has no known text)."""
    cmd = command_of(stmt)
    kind = cmd.get("Type") if isinstance(cmd, dict) else None
    if kind == "CallExpr":
        args = cmd.get("Args") or []
        if not args:
            return "an assignment" if cmd.get("Assigns") else "an empty command"
        text = word_text(args[0])
        return f"the command `{text}`" if text is not None else "a command whose first word has no known text"
    if kind == "BinaryCmd":
        return LIST_SHAPES.get(cmd.get("Op"), f"a `{cmd.get('Op')}` list")
    return SHAPES.get(kind, f"a {kind}")


def flagged(stmt, negation=True):
    """The flag that takes a tested statement out of the accepted positions, else None: it runs in the background
    (`&`, so its failure stops nothing), or, under `||` (negation), it is negated (`!`, so its failure is read as
    success); an `if` or `while` condition may be negated."""
    if stmt.get("Background"):
        return FLAGS["Background"]
    if negation and stmt.get("Negated"):
        return FLAGS["Negated"]
    return None


def status_parameter(word):
    """Whether the word is exactly `$?` or `${?}`: one parameter expansion of the last status and nothing else."""
    parts = (word.get("Parts") or []) if isinstance(word, dict) else []
    return len(parts) == 1 and parts[0].get("Type") == "ParamExp" and without_positions(parts[0]) in STATUS_PARAMETERS


def branch_reason(shape):
    """The message of a tested read whose `||` branch does not handle its status, naming the branch's shape. Every
    message that quotes text read from the tree is built by an f-string or a join, never by a format template the
    text could be read as: a word spelled `{y}` is a word, not a field."""
    return (
        f"the `||` branch is {shape} and does not end the read with a failure status: exit or return with no "
        "argument, a decimal from 1 to 255 or `$?`, a refusal function of this file ending so, or `name=$?`"
    )


def bare_shape(text, before):
    """How a finding names a refused bare `exit` or `return` (text) where `$?` is no longer the failed read's status
    (forms ii and iii): after the statement `before` names, whose status it passes on, or as the only statement of a
    function body (IN_FUNCTION), which must name its status."""
    if before is IN_FUNCTION:
        return f"a bare `{text}` in a function body, which must name its status (1 to 255 or `$?`)"
    return f"a bare `{text}` after {before}, which passes on that command's status, not the failed read's"


def terminator_shape(text, args, before=None):
    """None when `exit` or `return` (text) ends the read with the failed status: no argument (the status of the
    failed substitution propagates; refused, naming `before`, where an earlier statement or a function body sits
    between, since `$?` is then that statement's), one argument whose known text is a decimal from 1 to 255, or one
    bare `$?` or `${?}`; else the shape that names why not. `exit 0` turns the failed read into success; an argument
    with no known text (`"$x"`, `$(cmd)`, `"$?"`) is not shown to be nonzero; `exit 256` is 0 to bash; two arguments
    are an error bash reports before it exits."""
    if not args:
        return None if before is None else bare_shape(text, before)
    if len(args) != 1:
        return f"an `{text}` with {len(args)} arguments"
    if status_parameter(args[0]):
        return None
    value = word_text(args[0])
    if value is None:
        return f"an `{text}` whose argument has no known text"
    if value.isascii() and value.isdigit() and int(value) in FAILURE_STATUSES:
        return None
    if value.isascii() and value.isdigit() and int(value) % 256 == 0:
        return f"`{text} {value}`, which turns the failed read into success"
    return f"`{text} {value}`, whose argument is not a decimal from 1 to 255"


def branch_shape(stmt, functions, terminators, inner=False, before=None):
    """None when the `||` branch handles the status of the tested read, else the name of its shape. The branches that
    handle it: (i) a plain command whose known first word is one of terminators (`exit`, `return`; a top-level
    function of that name takes the name away) with no argument, one known decimal from 1 to 255 or one bare `$?`
    (terminator_shape; `before` names the statement a bare one follows, or is IN_FUNCTION, where it is refused, and
    is None where it is accepted); (ii) a plain command whose known first word names a top-level function of this
    file whose every body ends in a form (i) statement with an explicit argument; (iii) a block or subshell whose last
    statement is (i) or (ii), the bare form only as its only statement; (iv) a bare assignment of exactly `$?`. As the
    last statement of a block or a function body (inner), only (i) and (ii) count: no recursion, no nested block, no
    `$?` that the enclosing read never tests.
    A statement run in the background handles nothing: the script goes on while it runs."""
    if stmt.get("Background"):
        return BACKGROUND_BRANCH
    cmd = command_of(stmt)
    kind = cmd.get("Type") if isinstance(cmd, dict) else None
    if kind == "CallExpr":
        args = cmd.get("Args") or []
        if not args:
            assigns = cmd.get("Assigns") or []
            if len(assigns) == 1 and "Name" in assigns[0] and status_parameter(assigns[0].get("Value")):
                return None if not inner else "an assignment of `$?` that only the block or function body sees"
            return "an assignment of something other than `$?`" if assigns else "an empty command"
        text = word_text(args[0])
        if text is None:
            return "a command whose first word has no known text"
        if text in terminators:
            return terminator_shape(text, args[1:], before)
        if text in functions:
            for body in functions[text]:
                stmts = body_statements(body)
                if not stmts:
                    return f"a call of `{text}`, whose body ends in nothing"
                before = statement_name(stmts[-2]) if len(stmts) > 1 else IN_FUNCTION
                shape = branch_shape(stmts[-1], {}, terminators, True, before)
                if shape is not None:
                    return f"a call of `{text}`, whose body ends in {shape}"
            return None
        return f"the command `{text}`"
    if kind in ("Block", "Subshell") and not inner:
        stmts = body_statements(stmt)
        noun = "block" if kind == "Block" else "subshell"
        if not stmts:
            return f"a {noun} whose last statement is nothing"
        before = statement_name(stmts[-2]) if len(stmts) > 1 else None
        shape = branch_shape(stmts[-1], functions, terminators, True, before)
        if shape is None:
            return None
        return f"a {noun} whose last statement is {shape}"
    if kind == "BinaryCmd":
        op = cmd.get("Op")
        return LIST_SHAPES.get(op, f"a `{op}` list")
    return SHAPES.get(kind, f"a {kind}")


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
        self.reasons = {}  # id of a substitution in a tested position that is still a finding -> why
        self.allowed = set()  # lines carrying `# producer-status: allow <reason>`
        self.top = []
        self.top_index = 0
        self.first_substitution = None  # the index of the top-level statement holding the first substitution
        self.functions = {}  # the top-level functions of the file, name -> bodies (branch form ii)
        self.terminators = TERMINATORS  # `exit` and `return`, less any name a top-level function takes

    def run(self, tree):
        self.seen.clear()
        self.findings.clear()
        self.accepted.clear()
        self.reasons.clear()
        self.allowed.clear()
        self.top = tree.get("Stmts") or []
        self.top_index = 0
        self.first_substitution = None
        self.functions = top_level_functions(tree)
        self.terminators = tuple(name for name in TERMINATORS if name not in self.functions)
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
        and the left side of a `||` whose branch handles the status (branch_shape), when the tested statement runs in
        the foreground and, under `||`, is not negated (flagged) or a coprocess; any other branch or flag leaves the
        left side's substitution a finding that names the branch's shape or the flag."""
        for node in every(tree):
            kind = node.get("Type")
            # An `elif` is an IfClause with no Type key (shfmt types only interface fields); its Cond marks it.
            if kind in ("IfClause", "WhileClause") or (kind is None and "Cond" in node):
                for stmt in (node.get("Cond") or [])[-1:]:
                    self.candidate(stmt, flagged(stmt, False))
            elif kind is None and "Cmd" in node:
                binary = node["Cmd"]
                if not isinstance(binary, dict) or binary.get("Type") != "BinaryCmd" or binary.get("Op") != "||":
                    continue
                # The `&` of `x=$(…) || exit 1 &` is on the whole statement; a `!` is on the tested side.
                tested = binary["X"]
                reason = flagged(node, False) or flagged(tested)
                run = command_of(tested)
                if reason is None and isinstance(run, dict) and run.get("Type") == "CoprocClause":
                    inner = body_statements(run["Stmt"])
                    tested, reason = (inner[0] if len(inner) == 1 else run["Stmt"]), COPROCESS
                elif reason is None:
                    shape = branch_shape(binary["Y"], self.functions, self.terminators)
                    if shape is not None:
                        reason = branch_reason(shape)
                self.candidate(tested, reason)

    def candidate(self, stmt, reason):
        """Accept the substitution a tested statement captures, or record why it is still a finding."""
        substitution = tested_assignment(stmt)
        if substitution is None:
            return
        if reason is None:
            self.accepted.add(id(substitution))
        else:
            self.reasons[id(substitution)] = reason

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
                message = self.reasons.get(id(node), MESSAGES[SUBSTITUTION])
                self.report(stmt, node["Pos"]["Line"], SUBSTITUTION, message)
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
            target = stderr_target(redirects)
            later = siblings[0][siblings[1] + 1 :] if siblings is not None else []
            if (
                target is None
                or target is UNCAPTURED
                or not captures_to_file(target)
                or not any(self.tests_empty(other, target) for other in later)
            ):
                self.report(
                    stmt,
                    stmt["Pos"]["Line"],
                    PRODUCER,
                    f"`{' '.join(row)}` can fail with exit 0 or after printing (status-blind-producers.tsv); send its "
                    "stderr with `2>`, `2>>` or `2>|` to a file (the last redirect that touches fd 2 decides; any other "
                    "operator there, and /dev/null, leave it uncaptured) and test `[[ ! -s <that file> ]]` in a later "
                    "statement of the same list, or run it through read_listing of read-lib.sh",
                )
            break

    def tests_empty(self, stmt, target):
        """Whether the statement starts with `[[ ! -s <target> ]]`, the two words shown to name one file."""
        cmd = head(stmt)
        if not isinstance(cmd, dict) or cmd.get("Type") != "TestClause":
            return False
        test = cmd.get("X")
        if not isinstance(test, dict) or test.get("Type") != "UnaryTest" or test.get("Op") != "!":
            return False
        inner = test.get("X")
        if not isinstance(inner, dict) or inner.get("Type") != "UnaryTest" or inner.get("Op") != "-s":
            return False
        return same_word(inner["X"], target)

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
    if not listed:
        refuse(f"{file} holds no statement")
    if not walk.seen["Stmt"]:
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
