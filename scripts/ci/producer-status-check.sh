#!/usr/bin/env bash
# @file producer-status-check.sh
# @brief Refuse a command substitution outside the accepted grammar, a status-blind producer without its stderr capture, a missing `set -euo pipefail`, a `read` from a file, and a function or rebinding that shadows a word the rules read.
# @description
#   Regime-cutover U112 (plan P-21): standing order 21 made checkable. ShellCheck's check-extra-masked-returns
#   never flags a plain `x=$(producer)`, never looks at a file redirection, exempts echo, dirname, basename, printf,
#   set and shopt, and sees nothing when a producer exits 0 on a partial failure. This check parses each file with
#   shfmt (`shfmt -ln bash --to-json`) and walks its typed tree under six rules, each a closed set; a finding is
#   printed as `file:line: <rule>: <message>`:
#   a. `substitution`: a command substitution (`$(…)` or backquotes) is accepted only as the whole value of the one
#      assignment of a statement with no command word, where that statement is the last of an `if` or `while`
#      condition (negated or not) or the left side of a `||` whose branch handles the status, and no statement on
#      the path from the tested statement to the top level (the statement itself, the `||` list, and every block,
#      subshell, list, `if`, loop or function body around it) runs in the background, is negated (the condition's
#      own `!` aside) or is a `coproc`: `! x=$(…) || exit 1` reads the failure as success, `x=$(…) || exit 1 &`,
#      `{ x=$(…) || exit 1; } &` and `( x=$(…) || exit 1 ) &` end only the background job, `coproc { x=$(…); } ||
#      exit 1` tests the coprocess's start, and each is a finding naming the flagged statement's line. A function
#      body is not the top level: `f() { x=$(…) || return 1; }` is judged by its own path, whatever `f &` does at
#      the call. The branches that handle the status are a closed list:
#      (i) a plain command whose known first word is `exit` or `return`, as the whole branch, with no argument (the
#      status of the failed substitution propagates), with one argument whose known text is a decimal from 1 to 255,
#      or with one argument that is the bare `$?` (`exit 0`, `exit "$x"`, `exit $(cmd)`, `exit 1 2` and `return 0`
#      are findings: a zero turns the failed read into success); (ii) a plain command whose known first word is one of
#      REFUSAL_NAMES below (`refuse`, `fail`: the two refusal functions the adopted levers define, a closed allowlist;
#      a denylist of bash builtins and reserved words cannot be complete, and `fc` was the one the tuple this lint
#      carried missed, so `fc() { exit 2; }; unset -f fc; x=$(false) || fc -l` ran the builtin and the script went
#      on) and names a function this file defines exactly once, at the top level, in the foreground and not negated,
#      before the tested statement in file order, whose body is the refusal grammar:
#      zero or more statements, each a plain command whose known first word is `echo` or `printf` with a redirect that
#      sends fd 1 to fd 2 (`>&2` or `1>&2`), then exactly one last statement, a plain command `exit` with one argument
#      whose known text is a decimal from 1 to 255, every statement in the foreground and not negated, and nothing
#      else of any kind: no `return`, no `$?`, no `local`, no `if`, no assignment, no second `exit`, no call of another
#      function, no command substitution anywhere in the body. Every definition of the name counts, at any depth: a
#      second one inside an `if`, a loop, a block, a subshell or another function (`refuse() { exit 2; }; if true;
#      then refuse() { return 0; }; fi`) or a second spelling (`function refuse { …; }`) is a finding naming both
#      lines, since bash runs whichever ran last; a definition run in the background (`fail() { exit 2; } &`) exists
#      in a child shell only; one after the tested statement has not run when the read fails; a call of any other
#      defined name (`die`, `true`, `fc`, …) is a finding saying the name is not a refusal name, whatever its body;
#      each is a finding naming the duplicate's line, the flag or the name. The body is matched, not analysed: `f()
#      { echo failed >&2; return $?; }`, `f() { return 0; exit 1; }`, `f() { echo x; exit 2; }` and `f() { local
#      m=$1; echo "$m" >&2; exit 2; }` are each a finding naming the function and the first statement outside the
#      grammar, by line, whatever they would do when run (a name no function defines is a plain command; a function that
#      cleans up before it exits is not a refusal function: the cleanup goes in a trap, or the call carries an allow
#      comment naming the cleanup line); (iii) a block or subshell whose statements are that grammar (`{ echo no >&2;
#      exit 1; }`), so a bare `exit`, a `return`, a call of a refusal function or a `$?` inside one is a finding; (iv) a
#      bare plain assignment (`=`, not `+=`) of exactly `$?` (`status=$?`; `status+=$?` adds the status to the value, 25
#      and 6 making 256, and is a finding naming the append). A branch statement run in the background (`exit 2 &`) or
#      negated (`! exit 1`, `! (exit 1)`) handles nothing.
#      Any other branch leaves the substitution a finding that names the branch's shape: a pipeline, an `&&` or `||`
#      list, an `if`, a `case`, `true`, `:`, `false` or any other plain command, a block or subshell outside the
#      grammar, an assignment of anything else, a first word with no known text. A later line that handles an
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
#      stderr to a file, and a later statement of the same list must test `[[ ! -s <that file> ]]` in a shape whose
#      failure stops the script: the last statement of an `if` condition, or the left side of a `||` whose branch is
#      one of the forms of rule a; a bare `[[ ! -s <file> ]]` statement is accepted only at the top level of a file
#      whose prologue (rule c) runs `set -euo pipefail` before it, where `set -e` ends the script on its failure, and
#      anywhere else (a function body, a block, a file with no prologue before it) is not a test. The producer
#      statement, the test statement and every statement on the path of each to the top level must be in the
#      foreground and not negated: `git ls-files > l 2> e &` lets the next statement test `e` before the listing has
#      finished, `! git ls-files > l 2> e` reads its failure as success, `{ git ls-files > l 2> e; } &` ends only the
#      job and `coproc git ls-files > l 2> e` tests the coprocess's start, so each is a finding naming the flag and
#      its line whatever follows it; `! [[ ! -s err ]] || exit 1` reads a non-empty file as clean, `[[ ! -s err ]] &`
#      ends only the job, and an `&&` list or a pipeline is not a test, so a producer whose only such statement is one
#      of those is a finding naming that statement's line and why. Stderr is captured
#      only when the last redirect of the statement that touches fd 2 is `2>`, `2>>` or `2>|` to a word whose known
#      text is not /dev/null, or whose parts are literals and parameter expansions. The descriptor written before an
#      operator is read as bash reads it, a decimal (`02>&1` and `002> err` name fd 2; one that is not all digits,
#      `{fd}>`, refuses the file, exit 2). A redirect touches fd 2 when that descriptor is 2 whatever the operator,
#      when it is `&>` or `&>>`, or when it is `>&` or `<&` to a word that is not a plain descriptor (all digits or
#      `-`), whatever the descriptor before it: `>&file` and `1>&file` send both streams to the file, `>&2-`, `1>&2-`
#      and `<&2-` move fd 2 and close it, `>&$fd` may be any of them when it runs; `>&2`, `1>&2`, `01>&2` and `>&-`
#      leave fd 2 alone. Any other operator there (`2>&N`, `2<&-`, `2<`, `2<>`, `2<<<`, `&>`, `>&file`, a move, one
#      shfmt adds later) leaves stderr uncaptured, and the word of a `>&` or `<&` is never the captured file. The
#      tested word names the same file only when both texts are known and
#      equal, or both hold a parameter expansion and their parts are equal. `read_listing` of
#      scripts/orchestrator/read-lib.sh is that shape by construction, and a producer the table does not name is not
#      held to this rule.
#   c. `prologue`: the file runs `set -euo pipefail` at top level, in the foreground and not negated, before its
#      first statement holding a command substitution (a function body counts), else a finding at line 1 naming why
#      the first `set -euo pipefail` the file holds does not count: `set -euo pipefail &`, `{ set -euo pipefail; } &`
#      and `( set -euo pipefail )` set the options of a child shell only, one inside a function, block or `if` is
#      not at the top level. `shopt -s inherit_errexit` is not required: bash 3.2 has no such option.
#   d. `read`: a `read` that carries its own `<` redirect is a finding naming `read_file` (`done < file` redirects
#      the loop, not the `read`; a here-string is not a file).
#   e. `allow`: `# producer-status: allow <reason>` on the statement's first line exempts that statement from a, b
#      and d; an allow comment with no reason is itself a finding and exempts nothing. The enforced file set is
#      tests/unit/test_producer_status_check.py (the library and the five levers), not a Makefile target.
#   f. `shadow`: the rules above read a closed set of command words as bash builtins, as the table's producers or as
#      the refusal functions: `set` (c), `exit` and `return` (a, form i), `echo` and `printf` (the refusal grammar),
#      the first word of every producer row (`git`, `find`, `ls`; b) and REFUSAL_NAMES (`refuse`, `fail`; a, form
#      ii). The set is built from that data (interpreted), not listed twice. A function definition of a builtin's or
#      a producer's name, at any depth and in any spelling (`set() { :; }` lets a warned listing pass a bare `[[ ! -s
#      err ]]`, since the `set -euo pipefail` the test relies on ran a function; `exit() { :; }`, `echo() { exit 0;
#      }`, `git() { command git "$@"; return 0; }`), is a finding at its definition line naming what it shadows (a
#      refusal name's definitions are judged by form ii: one, at top level, before the read). So is every other way
#      bash offers to rebind a word or to run text this walk has not read, a plain command whose known first word is
#      one of REBINDERS, read as bash reads that word (the leading options for their letters, `--` ending them): a
#      NAMER (`alias`, `enable`, `hash`, `unset`) with an argument whose known text, before any `=`, is such a name
#      (`alias fail=true`, `enable -n echo`, `hash -p /x/true refuse`, `unset -f refuse`, and `unset refuse`, which
#      removes the function when no variable has the name) or with an argument that has no known text (`unset
#      "$name"`; `unset -v` names variables only and binds nothing, INERT_OPTIONS); a FORWARDER (`builtin`,
#      `command`) whose arguments name such a word or have no known text (`command git ls-files` runs past rule b),
#      and whose command is judged again when its own first word is a rebinder (`command unset -f refuse`; `command
#      -v` and `-V` print and run nothing); a RUNNER whose text or file this walk has not read: `eval` with any
#      argument, `source` and `.` with any argument but the one accepted shape, `. "${LEVER_DIR}/git-isolated.sh"`
#      or `. "${LEVER_DIR}/read-lib.sh"`, the two libraries every lever sources (LIBRARY_DIR, LIBRARY_FILES; the
#      parts of the one argument, nothing else), `trap` with an action that is not empty, `-` or one simple command
#      whose first word is no rebinder (`trap cleanup EXIT` and `trap 'rm -f "${f}"' EXIT` are read whole; `trap
#      'refuse() { :; }' DEBUG` redefines the function before the next command runs), `mapfile` or `readarray` with
#      `-C` (the callback is text bash runs); and an assignment with a value, anywhere (plain, a command's prefix, a
#      declaration's argument), to a variable that binds a command word (BINDING_VARIABLES: PATH, where `git`,
#      `find` and `ls` are found; BASH_ALIASES and BASH_CMDS, the alias and hash tables of bash 4). A `declare`,
#      `typeset`, `readonly`, `export` or `local` acts on variables, and with `-f` on a function it leaves bound
#      (`export -f refuse`, `readonly -f refuse`, measured on bash 3.2), so none is a rebinder: `export PATH` and
#      `declare -r y=1` pass. Not read: an indirect write to a binding variable (`read`, `printf -v`, `for`, a
#      nameref, `${name=value}`), which this rule does not close. An allow comment exempts nothing here.
#   A heredoc body whose delimiter has any quoted or escaped part is literal and skipped, as bash reads it (shfmt
#   expands the body of a partly quoted delimiter such as `<<'E'OF`), by every scan of this walk: one function,
#   children, is the only descent into a node, so a `$(refuse() { return 0; })` or a `# producer-status: allow` in
#   such a body defines and exempts nothing. The files are parsed as bash. A file shfmt
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
#   (empty or comment-only) or a redirect descriptor that is not a decimal (`{fd}>`), or this walk saw none of a
#   listed file's statements or none of its kinds in the contract fixtures: the list is refused, never read as clean.
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
import re
import subprocess
import sys
from collections import Counter

sys.path.insert(0, sys.argv[1])
import shfmt_json_contract as contract  # noqa: E402

NAME = "producer-status-check"
TABLE = sys.argv[2]
SUBSTITUTION, PRODUCER, PROLOGUE, READ, ALLOW = "substitution", "producer", "prologue", "read", "allow"
SHADOW = "shadow"  # rule f
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
# The names form (ii) accepts, a closed allowlist: the two refusal functions the adopted levers define. A denylist of
# bash builtins and reserved words cannot be complete (bash adds and loads them); the one this lint carried missed
# `fc`, so `fc() { exit 2; }; unset -f fc; x=$(false) || fc -l` ran the builtin and the script went on.
REFUSAL_NAMES = ("refuse", "fail")
# A bare literal is a known text only over this set: a glob character, a brace, a tilde, `$`, a backquote, a backslash
# or whitespace is expanded or read by bash and is not decoded here. Inside double quotes bash expands none of them,
# so the set does not apply there.
KNOWN_CHARACTERS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-./:=+@%,")
# The last status as a whole word, `$?` or `${?}` (form iv); `${?:-0}` and `"$?"` are not it.
STATUS_PARAMETERS = (
    {"Type": "ParamExp", "Short": True, "Param": {"Value": "?"}},
    {"Type": "ParamExp", "Param": {"Value": "?"}},
)
# A tested read whose path to the top level holds a flagged statement: its failure stops nothing. The path is the
# read's own statement and every statement around it (a `||` list, a block, a subshell, an `if`, a loop, a function
# body); a statement is flagged when it runs in the background (`&`), is negated (`!`) or runs a `coproc` clause.
BACKGROUND, NEGATED, COPROCESS = "Background", "Negated", "CoprocClause"
BRANCH_FLAGS = {  # how a finding names a flagged statement in a `||` branch
    BACKGROUND: "a command run in the background (`&`), which lets the script go on",
    NEGATED: "a negated command (`!`), whose failure status is read as success",
    COPROCESS: "a `coproc`, whose status is its start, not its command's",
}
DEFINITION_FLAGS = {  # how a finding names the flagged top-level definition of the function a `||` branch calls
    BACKGROUND: "runs in the background (`&`), so the function exists in a child shell only",
    NEGATED: "is negated (`!`), a flagged statement",
    COPROCESS: "runs in a coprocess, a child shell",
}
WRITERS = ("echo", "printf")  # the plain commands a refusal body may run before its `exit`, each sending fd 1 to fd 2
STDOUT = 1  # the descriptor `1>&2` writes, as a number; `>&2` writes none
GRAMMAR = "`echo`/`printf` to stderr, then one `exit <1-255>`"  # how a finding names the refusal grammar (forms ii, iii)
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
STDERR = 2  # a descriptor is read as a decimal, so `02>` and `002>` name it too
FILE_OPS = (">", ">>", ">|")  # the only operators that, on fd 2, capture stderr to the word's file
BOTH_OPS = ("&>", "&>>")  # touch fd 2 with no descriptor written
DUP_OP = ">&"  # the operator a refusal body writes to stderr with (`>&2`, `1>&2`)
DUP_OPS = (DUP_OP, "<&")  # to a plain descriptor (`>&1`, `>&-`) each moves the one before it; to any other word fd 2
UNCAPTURED = object()  # the stderr target when the last redirect touching fd 2 is not one of FILE_OPS
# Rule f's rebinders: every plain command bash offers that binds a command word to other text, a file, a builtin or
# nothing, or runs text this walk has not read, each read as bash reads it (measured on /bin/bash 3.2.57; the bash 4
# builtins by the manual). A NAMER's arguments are names: `alias` (expanded under `shopt -s expand_aliases` or an
# inherited BASHOPTS), `enable` (`-n` disables a builtin, `-f` loads one), `hash` (`-p` binds a word to a file) and
# `unset` (`-f` names a function, and so does a name with no variable; `-v` names variables only). A FORWARDER runs its
# arguments as a command past any function (`command unset -f refuse`, `builtin unset -f refuse`; `command -v`/`-V`
# print and run nothing). A RUNNER's argument is text or a file: `eval`, `source` and `.` (the one accepted shape is
# sourced_library), `trap` (an action read whole is trap_action), `mapfile` and `readarray` (`-C` names a callback).
# A `declare`, `typeset`, `readonly`, `export` or `local` acts on variables, and with `-f` on a function it leaves
# bound (`export -f refuse`, `readonly -f refuse`, measured), so none is a rebinder.
NAMERS = ("alias", "enable", "hash", "unset")
FORWARDERS = ("builtin", "command")
RUNNERS = ("eval", "source", ".", "trap", "mapfile", "readarray")
REBINDERS = NAMERS + FORWARDERS + RUNNERS
INERT_OPTIONS = {"unset": "v", "command": "vV"}  # the option letters under which the word binds and runs nothing
CALLBACK_OPTION = "C"  # `mapfile`/`readarray`: the option whose argument is text bash runs per line
SOURCES = ("source", ".")
RUNS = {  # how a finding names what a RUNNER runs
    "eval": "runs text",
    "source": "reads a file",
    ".": "reads a file",
    "trap": "runs an action",
    "mapfile": "runs a callback (`-C`)",
    "readarray": "runs a callback (`-C`)",
}
# The one `source` the rules accept: every lever sources the two libraries beside it, `. "${LEVER_DIR}/git-isolated.sh"`
# and `. "${LEVER_DIR}/read-lib.sh"` (scripts/orchestrator/README.md); the argument's parts are the bare expansion of
# LIBRARY_DIR and one literal of LIBRARY_FILES, in any quoting name_parts flattens. Nothing else is read as that file.
LIBRARY_DIR = "LEVER_DIR"
LIBRARY_FILES = ("/git-isolated.sh", "/read-lib.sh")
# A simple command as a trap's action, read whole: one identifier, then arguments holding no second command, no
# substitution and no assignment (`;`, `&`, `|`, `(`, `)`, a backquote, `=`, a newline). `trap cleanup EXIT` and `trap
# 'rm -f "${file}"' EXIT` are read; `trap 'refuse() { :; }' DEBUG`, which redefines the function before the next
# command runs (measured), is not.
SIMPLE_COMMAND = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)(?:[ \t][^;&|()\x60=\n]*)?")  # \x60 is the backquote
BINDING_VARIABLES = {  # an assignment to one binds a command word, as the rebinders do (rule f)
    "PATH": "the directories bash searches for `git`, `find` and `ls`",
    "BASH_ALIASES": "the alias table of bash 4, as `alias` does",
    "BASH_CMDS": "the hash table of bash 4, as `hash -p` does",
}
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
    """Every JSON object at or below tree, iteratively (a long && chain nests deeper than Python recurses), by
    children: the one traversal definitions, Walk.comments and refusal_break scan with."""
    todo = [tree]
    while todo:
        node = todo.pop()
        if isinstance(node, dict):
            yield node
            todo.extend(children(node))
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


def children(node):
    """The values of a node this walk descends into: every value, less the body of a heredoc whose delimiter is quoted
    or escaped (without_literal_body). The one descent: every and Walk.visit step by it, and no other function reads
    a node's values, so no scan of this walk reads a literal body as code."""
    return without_literal_body(node).values()


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


class Unread(Exception):
    """A value of the tree this walk does not read, so the file is refused (exit 2), never judged: a redirect
    descriptor that is not a decimal (`{fd}>`, the variable form bash 4.1 fills)."""


def descriptor_number(redirect):
    """The descriptor written before a redirect's operator (`2>`, `02>&1`, `002> err`, `1>&2-`) as the number bash
    reads, a decimal: `02` and `002` are fd 2. None when none is written. One that is not all digits (`{fd}>`) is not
    read here, and the file is refused (Unread), never passed."""
    value = (redirect.get("N") or {}).get("Value")
    if value is None:
        return None
    if not (value.isascii() and value.isdigit()):
        raise Unread(f"the redirect descriptor `{value}` at line {redirect['Pos']['Line']} is not a decimal")
    return int(value, 10)


def plain_descriptor(word):
    """Whether the word of a `>&` or `<&` is a plain descriptor, its known text all digits or exactly `-` (`>&1`,
    `>&2`, `2>&-`), so the redirect duplicates or closes the descriptor before its operator and no other. Any other
    word moves fd 2 or is not shown not to: `2-` and `1-` are moves that close the descriptor they name (`1>&2-`,
    `>&2-` and `<&2-` close fd 2), a path sends both streams to its file (`>&file`, and `1>&file` on bash 3.2), and a
    word with no known text (`>&$fd`) is any of them when it runs."""
    text = word_text(word)
    return text is not None and ((text.isascii() and text.isdigit()) or text == "-")


def touches_stderr(redirect):
    """Whether the redirect moves fd 2: the descriptor before its operator is 2 whatever the operator (`2>`, `02>&1`,
    `2<&-`), the operator is `&>` or `&>>`, or it is `>&` or `<&` to a word that is not a plain descriptor (`>&file`,
    `>&2-`, `1>&2-`, `<&2-`, `1>&$fd`), whatever the descriptor before it. `>&2`, `1>&2`, `01>&2` and `>&-`
    duplicate or close fd 1 and leave fd 2 alone."""
    if descriptor_number(redirect) == STDERR:
        return True
    if redirect.get("Op") in BOTH_OPS:
        return True
    return redirect.get("Op") in DUP_OPS and not plain_descriptor(redirect["Word"])


def stderr_target(redirects):
    """Where a statement's stderr ends up, decided by the last redirect that touches fd 2: the word when that redirect
    is `2>`, `2>>` or `2>|` (the descriptor 2 in any decimal spelling), UNCAPTURED for any other (`2>&N`, `2<&-`,
    `2<`, `2<>`, `2<<<`, `&>`, `>&file`, a move `1>&2-`, an operator shfmt adds later; the word of a `>&` or `<&` is
    never the target), None when no redirect touches it."""
    target = None
    for redirect in redirects:
        if touches_stderr(redirect):
            captures = redirect.get("Op") in FILE_OPS and descriptor_number(redirect) == STDERR
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


def leftmost(stmt):
    """The statement a statement runs first: the leftmost operand of a `||`, `&&` or `|` chain, else itself."""
    cmd = command_of(stmt)
    while isinstance(cmd, dict) and cmd.get("Type") == "BinaryCmd":
        stmt = cmd["X"]
        cmd = command_of(stmt)
    return stmt


def top_level_functions(tree):
    """The functions the file defines at top level, name -> the statements defining it, in file order; a definition
    inside another statement is counted by definitions below, not here."""
    functions = {}
    for stmt in tree.get("Stmts") or []:
        cmd = command_of(stmt)
        if isinstance(cmd, dict) and cmd.get("Type") == "FuncDecl":
            functions.setdefault(cmd["Name"]["Value"], []).append(stmt)
    return functions


def definitions(tree):
    """Every function definition the file holds, at any depth, name -> the lines of its FuncDecl nodes in file order:
    one inside an `if`, a loop, a block, a subshell, another function or a background job counts (every visits them
    all, less a literal heredoc body), since bash runs whichever definition ran last."""
    lines = {}
    for node in every(tree):
        if node.get("Type") == "FuncDecl":
            lines.setdefault(node["Name"]["Value"], []).append(node["Pos"]["Line"])
    return {name: sorted(found) for name, found in lines.items()}


def interpreted(rows):
    """The command words the rules read as bash builtins, as the producers of the table or as the refusal functions,
    name -> what a rebinding of that name shadows (rule f): `set` (the prologue, rule c), `exit` and `return` (form i
    of rule a), `echo` and `printf` (the refusal grammar, forms ii and iii), the first word of every producer row
    (rule b) and REFUSAL_NAMES (form ii). Built from the data those rules hold, so a word added to one of them is
    covered without a second list. A function definition of a refusal name is judged by form ii (one, at top level,
    before the read), of any other word by Walk.run."""
    words = {PROLOGUE_WORDS[0]: "the builtin the prologue `set -euo pipefail` relies on (rule c)"}
    for name in REFUSAL_NAMES:
        words[name] = "the refusal function a `||` branch calls (rule a, form ii)"
    for name in TERMINATORS:
        words[name] = "the builtin a `||` branch ends a failed read with (rule a, form i)"
    for name in WRITERS:
        words[name] = "the builtin the refusal grammar writes to stderr with (rule a, forms ii and iii)"
    producers = {}
    for row in rows:
        producers.setdefault(row[0], []).append(f"`{' '.join(row)}`")
    for name, named in producers.items():
        plural = "s" if len(named) > 1 else ""
        words.setdefault(name, f"the producer{plural} {', '.join(named)} rule b holds to a stderr capture")
    return words


def sourced_library(args):
    """Whether a `source` or `.` is the one shape rule f accepts: exactly one argument whose parts (name_parts, the
    double quotes flattened) are the bare expansion of LIBRARY_DIR (`${LEVER_DIR}` or `$LEVER_DIR`, with no operator,
    index or length) and one literal of LIBRARY_FILES. Anything else is a file this walk has not read."""
    parts = name_parts(args[0]) if len(args) == 1 else None
    if parts is None or len(parts) != 2:
        return False
    directory, library = parts
    return (
        directory.get("Type") == "ParamExp"
        and set(directory) <= {"Type", "Short", "Param"}
        and (directory.get("Param") or {}).get("Value") == LIBRARY_DIR
        and library.get("Type") == "Lit"
        and library.get("Value") in LIBRARY_FILES
    )


def trap_action(text):
    """Whether a trap's action, a known text, is read whole: empty or `-` (the signal's default), or one simple
    command (SIMPLE_COMMAND) whose first word is no rebinder. Anything else is text this walk has not read."""
    if text in ("", "-"):
        return True
    match = SIMPLE_COMMAND.fullmatch(text)
    return match is not None and match[1] not in REBINDERS


def refusal_function(text, tested, functions, defined):
    """Why a `||` branch calling text is not shown to run one refusal function of this file when the tested statement
    fails, else None: the name is not one of REFUSAL_NAMES (a closed allowlist; any other name, a builtin's among
    them, is refused whatever its body); the file defines the name more than once, at any depth (defined), and bash
    runs whichever ran last; the one definition sits inside another statement (not in functions, the top-level ones),
    runs in the background or is negated (flagged_path), or comes after the tested statement in file order, so it
    has not run when the read fails."""
    lines = defined[text]
    if text not in REFUSAL_NAMES:
        names = ", ".join(f"`{name}`" for name in REFUSAL_NAMES)
        return f"a call of `{text}`, defined at line {lines[0]}, a name that is not a refusal name ({names})"
    if len(lines) > 1:
        return (
            f"a call of `{text}`, defined {len(lines)} times (lines {', '.join(map(str, lines))}), where bash runs "
            "whichever definition ran last"
        )
    stmts = functions.get(text) or []
    if not stmts:
        return f"a call of `{text}`, defined at line {lines[0]} inside another statement, not at the top level"
    flag = flagged_path((stmts[0],))
    if flag is not None:
        return f"a call of `{text}`, whose definition at line {lines[0]} {DEFINITION_FLAGS[flag[0]]}"
    if stmts[0]["Pos"]["Offset"] > tested["Pos"]["Offset"]:
        return (
            f"a call of `{text}`, defined at line {lines[0]}, after the tested statement at line "
            f"{tested['Pos']['Line']}, so the function has not been defined when the read fails"
        )
    return None


def function_body(stmt):
    """The body statement of a function definition, else None."""
    cmd = command_of(stmt)
    return cmd.get("Body") if isinstance(cmd, dict) and cmd.get("Type") == "FuncDecl" else None


def body_statements(stmt):
    """The statements a function body or a `||` branch runs: a block's or subshell's list, else the statement itself
    (`f() exit 2`, a plain command)."""
    cmd = command_of(stmt)
    if isinstance(cmd, dict) and cmd.get("Type") in ("Block", "Subshell"):
        return cmd.get("Stmts") or []
    return [stmt]


def statement_name(stmt):
    """How a finding names the statement a `set -euo pipefail` or a bare `[[ ! -s file ]]` sits inside: the
    command's known first word, else its shape (an assignment, a list, a block, an `if`, a function definition, a
    command whose first word has no known text)."""
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


def flagged_path(stack, negation=True):
    """The first flagged statement on the path from a statement (stack[0]) out to the top level (stack[-1]), as
    (flag, depth) into the stack, else None: a statement run in the background (`&`, so a failure ends only the job),
    negated (`!`, so the failure of what it ends is read as success) or running a `coproc` clause (shfmt 3.14.1 writes
    no Coprocess flag on the statement in bash mode: the clause is the flag). An `if` or `while` condition may negate
    its own statement (negation False passes over the `!` of stack[0] alone); a `!` around it is a flag."""
    for depth, stmt in enumerate(stack):
        if stmt.get("Background"):
            return BACKGROUND, depth
        if stmt.get("Negated") and (negation or depth):
            return NEGATED, depth
        cmd = command_of(stmt)
        if isinstance(cmd, dict) and cmd.get("Type") == "CoprocClause":
            return COPROCESS, depth
    return None


def read_flag(flag, stmt, depth):
    """The message of a tested read whose path holds a flagged statement (stmt, at depth in the path), naming its
    line: the `&`, the `!` or the `coproc` may be on the read's own line or on a statement lines above it."""
    line = stmt["Pos"]["Line"]
    if flag == BACKGROUND:
        return (
            "the tested read runs in the background (`&`), so its failure stops nothing: the test sees the job "
            f"started at line {line}"
        )
    if flag == COPROCESS:
        return (
            "the tested read runs as a coprocess (`coproc`), whose status is read before the read ends: the `coproc` "
            f"is at line {line}"
        )
    if depth:
        return (
            f"the tested read sits in a statement negated (`!`) at line {line}, so a failure that ends that statement "
            "is read as success and the script goes on"
        )
    return (
        "the tested read is negated (`!`), so its failure is read as success and the `||` branch does not run: the "
        f"`!` is at line {line}"
    )


def test_flag(flag, stmt, depth):
    """Why a `[[ ! -s file ]]` test whose path holds a flagged statement (stmt, at depth) closes no producer."""
    line = stmt["Pos"]["Line"]
    if flag == BACKGROUND:
        return f"runs in the background (`&`, the job started at line {line}), so its failure stops nothing"
    if flag == COPROCESS:
        return f"runs in a coprocess started at line {line}, whose status is its start"
    if depth:
        return f"sits in a statement negated (`!`) at line {line}, so a non-empty file is read as success"
    return "is negated (`!`), so a non-empty file is read as clean"


def producer_flag(flag, stmt, depth):
    """Why a producer whose path holds a flagged statement (stmt, at depth) is a finding whatever follows it: a later
    test reads its stderr file before it has finished, or its own failure status is read as success."""
    line = stmt["Pos"]["Line"]
    if flag == BACKGROUND:
        return (
            f"the producer runs in the background (`&`, the job started at line {line}), so a later test reads its "
            "stderr file before the listing has finished"
        )
    if flag == COPROCESS:
        return (
            f"the producer runs in a coprocess started at line {line}, so a later test reads its stderr file before "
            "the listing has finished and its status is the start's"
        )
    if depth:
        return (
            f"the producer sits in a statement negated (`!`) at line {line}, so a failure that ends that statement "
            "is read as success"
        )
    return "the producer is negated (`!`), so its failure status is read as success"


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
        f"argument, a decimal from 1 to 255 or `$?`, a refusal function or a block of this file ({GRAMMAR}), or "
        "`name=$?`"
    )


def terminator_shape(text, args):
    """None when `exit` or `return` (text), as the whole branch, ends the read with the failed status: no argument
    (the status of the failed substitution propagates), one argument whose known text is a decimal from 1 to 255, or
    one bare `$?` or `${?}`; else the shape that names why not. `exit 0` turns the failed read into success; an
    argument with no known text (`"$x"`, `$(cmd)`, `"$?"`) is not shown to be nonzero; `exit 256` is 0 to bash; two
    arguments are an error bash reports before it exits."""
    if not args:
        return None
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


def exit_shape(args):
    """None when the `exit` that ends a refusal body names its status: one argument whose known text is a decimal
    from 1 to 255; else the shape that names why not. A bare `exit` and `exit $?` pass on the status of the statement
    before them (an `echo`'s), so neither is in the grammar."""
    if not args:
        return "a bare `exit`, whose status is the statement's before it"
    if len(args) == 1 and status_parameter(args[0]):
        return "`exit $?`, whose status is the statement's before it"
    return terminator_shape("exit", args)


def sends_stdout_to_stderr(redirect):
    """Whether the redirect is `>&2` or `1>&2` in any decimal spelling (`01>&2`, `>&02`): the `>&` operator with no
    descriptor or descriptor 1, to a word whose known text is all digits and reads as 2."""
    if redirect.get("Op") != DUP_OP or descriptor_number(redirect) not in (None, STDOUT):
        return False
    text = word_text(redirect["Word"])
    return text is not None and text.isascii() and text.isdigit() and int(text, 10) == STDERR


def refusal_break(stmts, defined):
    """What breaks the refusal grammar in the statements of a function body or of a block or subshell branch, as
    (what, line), else None. The grammar: zero or more plain commands whose known first word is `echo` or `printf`
    (not a name a function of this file takes, at any depth) with a redirect that sends fd 1 to fd 2, then exactly one
    plain command `exit` (not such a name either) with one argument whose known text is a decimal from 1 to 255,
    every statement in the foreground and not negated, no command substitution and no `$?` anywhere. The body is
    matched, never analysed: the first statement that is anything else (a `return`, a declaration, an `if`, an
    assignment, a call, an `exit` before the last statement, an `echo` without `>&2`, an `echo` where the `exit` must
    be) is named, whatever it would do when run."""
    for index, stmt in enumerate(stmts):
        line = stmt["Pos"]["Line"]
        flag = flagged_path((stmt,))
        if flag is not None:
            return BRANCH_FLAGS[flag[0]], line
        cmd = command_of(stmt)
        kind = cmd.get("Type") if isinstance(cmd, dict) else None
        if kind == "BinaryCmd":
            return LIST_SHAPES.get(cmd.get("Op"), f"a `{cmd.get('Op')}` list"), line
        if kind != "CallExpr":
            return SHAPES.get(kind, f"a {kind}"), line
        args = cmd.get("Args") or []
        if not args:
            return ("an assignment" if cmd.get("Assigns") else "an empty command"), line
        if cmd.get("Assigns"):
            return "a command with an assignment before it", line
        text = word_text(args[0])
        if text is None:
            return "a command whose first word has no known text", line
        if text in defined:
            return f"a call of `{text}`", line
        last = index == len(stmts) - 1
        if text in WRITERS:
            if last:
                return f"the command `{text}` as the last statement, where the `exit` must be", line
            if not any(sends_stdout_to_stderr(redirect) for redirect in stmt.get("Redirs") or []):
                return f"an `{text}` that does not send fd 1 to fd 2 (`>&2`)", line
        elif text != "exit":
            return f"the command `{text}`", line
        elif not last:
            return "an `exit` before the last statement", line
        else:
            shape = exit_shape(args[1:])
            if shape is not None:
                return shape, line
        inner = [
            node
            for node in every(stmt)
            if node.get("Type") == "CmdSubst"
            or (node.get("Type") == "ParamExp" and without_positions(node) in STATUS_PARAMETERS)
        ]
        if inner:
            node = min(inner, key=lambda node: node["Pos"]["Line"])
            return ("a command substitution" if node["Type"] == "CmdSubst" else "`$?`"), node["Pos"]["Line"]
    return None if stmts else ("no statement", None)


def grammar_break(noun, broken):
    """How a finding names a function body (noun: a call of f, whose body) or a block or subshell (noun: a block that)
    outside the refusal grammar: by the first statement outside it and its line."""
    what, line = broken
    where = f"at line {line} with {what}" if line is not None else f"with {what}"
    return f"{noun} breaks the refusal grammar ({GRAMMAR}) {where}"


def branch_shape(stmt, tested, functions, defined, terminators):
    """None when the `||` branch (stmt) handles the status of the tested statement, else the name of its shape. The
    branches that handle it: (i) a plain command whose known first word is one of terminators (`exit`, `return`; a
    function of that name anywhere in the file takes the name away) with no argument, one known decimal from 1 to 255
    or one bare `$?` (terminator_shape); (ii) a plain command whose known first word is one of REFUSAL_NAMES and names a
    function this file defines once, at top level, unflagged and before the tested statement (refusal_function), whose
    body is the refusal grammar (refusal_break; a name no function has is a plain command); (iii) a block or subshell
    whose statements are that grammar; (iv) a bare `=` assignment of exactly `$?` (`+=` adds the status to the value). A
    statement run in the background or negated handles nothing (the script goes on, or the failure reads as success)."""
    flag = flagged_path((stmt,))
    if flag is not None:
        return BRANCH_FLAGS[flag[0]]
    cmd = command_of(stmt)
    kind = cmd.get("Type") if isinstance(cmd, dict) else None
    if kind == "CallExpr":
        args = cmd.get("Args") or []
        if not args:
            assigns = cmd.get("Assigns") or []
            if len(assigns) == 1 and "Name" in assigns[0]:
                if assigns[0].get("Append"):
                    return "an append (`+=`) of the status to the value, not a capture of `$?`"
                if status_parameter(assigns[0].get("Value")):
                    return None
            return "an assignment of something other than `$?`" if assigns else "an empty command"
        text = word_text(args[0])
        if text is None:
            return "a command whose first word has no known text"
        if text in terminators:
            return terminator_shape(text, args[1:])
        if text in defined:
            reason = refusal_function(text, tested, functions, defined)
            if reason is not None:
                return reason
            broken = refusal_break(body_statements(function_body(functions[text][0])), defined)
            if broken is not None:
                return grammar_break(f"a call of `{text}`, whose body", broken)
            return None
        return f"the command `{text}`"
    if kind in ("Block", "Subshell"):
        broken = refusal_break(body_statements(stmt), defined)
        if broken is None:
            return None
        return grammar_break("a block that" if kind == "Block" else "a subshell that", broken)
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
        self.prologues = []  # the path (statement stack) of every `set -euo pipefail` the file holds
        self.functions = {}  # the top-level functions of the file, name -> defining statements (branch form ii)
        self.defined = {}  # every function of the file, at any depth, name -> the lines of its definitions
        self.terminators = TERMINATORS  # `exit` and `return`, less any name a function of the file takes
        self.set_e = None  # the offset of the first top-level, unflagged `set -euo pipefail` (a bare test of rule b)
        self.shadowed = interpreted(rows)  # rule f: the words the rules read, name -> what a definition of it shadows

    def run(self, tree):
        self.seen.clear()
        self.findings.clear()
        self.accepted.clear()
        self.reasons.clear()
        self.allowed.clear()
        self.prologues.clear()
        self.top = tree.get("Stmts") or []
        self.top_index = 0
        self.first_substitution = None
        self.functions = top_level_functions(tree)
        self.defined = definitions(tree)
        self.terminators = tuple(name for name in TERMINATORS if name not in self.defined)
        for name, lines in self.defined.items():  # rule f: a function of a name the rules read, at any depth
            if name in self.shadowed and name not in REFUSAL_NAMES:  # a refusal name's definitions are form ii's
                for line in lines:
                    self.findings.add(
                        (line, SHADOW, f"a function named `{name}` shadows {self.shadowed[name]}; bash runs it instead")
                    )
        self.set_e = min(
            (stmt["Pos"]["Offset"] for stmt in self.top if prologue_statement(stmt) and flagged_path((stmt,)) is None),
            default=None,
        )
        self.comments(tree)
        self.visit(tree, (), None)
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

    def tested_list(self, stmt, stack):
        """The second accepted position: the left side of a `||` (stmt's command) whose branch handles the status
        (branch_shape), when no statement on the left side's path is flagged (flagged_path over the left side, the
        `||` statement and every statement around it: `x=$(…) || exit 1 &` and `{ x=$(…) || exit 1; } &` end only
        the job). A `coproc` as the left side tests the coprocess's start: the one statement it runs is the candidate,
        and the clause on its path is the flag. Any other branch or flag leaves the substitution a finding naming it."""
        binary = stmt.get("Cmd")
        if not isinstance(binary, dict) or binary.get("Type") != "BinaryCmd" or binary.get("Op") != "||":
            return
        tested = binary["X"]
        path = (tested, *stack)
        run = command_of(tested)
        if isinstance(run, dict) and run.get("Type") == "CoprocClause":
            held = run["Stmt"]
            inner = body_statements(held)
            tested = inner[0] if len(inner) == 1 else held
            path = (tested, held, *path) if tested is not held else (held, *path)
        self.test(tested, path, self.branch(stmt, binary["Y"]))

    def branch(self, stmt, branch):
        """Why the `||` branch of the statement stmt does not handle the status of its tested read, else None."""
        shape = branch_shape(branch, stmt, self.functions, self.defined, self.terminators)
        return None if shape is None else branch_reason(shape)

    def test(self, tested, path, reason, negation=True):
        """A tested statement on its path: a flag on the path is its reason (naming the flagged line), else the
        branch's reason, else the read is accepted."""
        flag = flagged_path(path, negation)
        if flag is not None:
            reason = read_flag(flag[0], path[flag[1]], flag[1])
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

    def visit(self, node, stack, siblings):
        """Depth first; stack is the statements holding node, innermost first (the path flagged_path reads), siblings
        the statement list it sits in, its index there and the stack around that list (the list a later `[[ ! -s
        file ]]` is searched in, and the path it shares with the producer). The two
        accepted positions are marked here, at the statement or clause that tests the read, before its substitution is
        visited."""
        if isinstance(node, list):
            for item in node:
                self.visit(item, stack, siblings)
            return
        if not isinstance(node, dict):
            return
        kind = node.get("Type")
        if kind is None and "Cmd" in node:
            self.seen["Stmt"] += 1
            for redirect in node.get("Redirs") or []:  # on any command: a descriptor that is not a decimal refuses the file
                self.seen["Redirect"] += 1
                descriptor_number(redirect)
            stack = (node, *stack)
            if siblings is not None and siblings[0] is self.top:
                self.top_index = siblings[1]
            self.statement(node, stack, siblings)
            self.tested_list(node, stack)
            if prologue_statement(node):
                self.prologues.append(stack)
        elif kind is None and "Name" in node:
            self.seen["Assign"] += 1
            self.binding(node)
        elif kind in ("IfClause", "WhileClause") or (kind is None and "Cond" in node):
            # An `elif` is an IfClause with no Type key (shfmt types only interface fields); its Cond marks it. The
            # condition's last statement may be negated; a flag on any statement around the clause is a flag.
            for stmt in (node.get("Cond") or [])[-1:]:
                self.test(stmt, (stmt, *stack), None, False)
        elif kind == "CmdSubst":
            self.seen["CmdSubst"] += 1
            if self.first_substitution is None:
                self.first_substitution = self.top_index
            if id(node) not in self.accepted:
                message = self.reasons.get(id(node), MESSAGES[SUBSTITUTION])
                self.report(stack[0] if stack else None, node["Pos"]["Line"], SUBSTITUTION, message)
        for value in children(node):
            if isinstance(value, list) and any(isinstance(item, dict) and "Cmd" in item for item in value):
                for index, item in enumerate(value):
                    self.visit(item, stack, (value, index, stack))
            else:
                self.visit(value, stack, siblings)

    def statement(self, stmt, stack, siblings):
        """Rules b, d and f on one statement's own command. stack is the statement's path to the top level: a producer
        run in the background, negated or in a coprocess on any statement of it (flagged_path) is a finding whatever
        follows it. Else a later `[[ ! -s file ]]` of the same statement list is judged on that list's path to the
        top level (siblings[2]), which it shares with the producer."""
        cmd = stmt.get("Cmd")
        if not isinstance(cmd, dict) or cmd.get("Type") != "CallExpr":
            return
        words = leading_words(cmd)
        redirects = stmt.get("Redirs") or []
        if words[:1] == ["read"] and any(redirect.get("Op") == "<" for redirect in redirects):
            self.report(stmt, stmt["Pos"]["Line"], READ, MESSAGES[READ])
        if words[:1] and words[0] in REBINDERS:
            self.rebinding(stmt, words[0], (cmd.get("Args") or [])[1:])
        for row in self.rows:
            if words[: len(row)] != row:
                continue
            flag = flagged_path(stack)
            if flag is not None:
                why = producer_flag(flag[0], stack[flag[1]], flag[1])
            else:
                target = stderr_target(redirects)
                later = siblings[0][siblings[1] + 1 :] if siblings is not None else []
                outer = siblings[2] if siblings is not None else ()
                tests = []
                if target is not None and target is not UNCAPTURED and captures_to_file(target):
                    tests = [
                        reason
                        for reason in (self.empty_test(other, target, outer) for other in later)
                        if reason is not None
                    ]
                if "" in tests:
                    break
                why = tests[0] if tests else None
            self.report(
                stmt,
                stmt["Pos"]["Line"],
                PRODUCER,
                f"`{' '.join(row)}` can fail with exit 0 or after printing (status-blind-producers.tsv); send its "
                "stderr with `2>`, `2>>` or `2>|` to a file (the last redirect that touches fd 2 decides; any other "
                "operator there, and /dev/null, leave it uncaptured) and test `[[ ! -s <that file> ]]` in a later "
                "statement of the same list, as an `if` condition or the left side of a `||` that ends the script, "
                "or run it through read_listing of read-lib.sh" + (f"; {why}" if why is not None else ""),
            )
            break

    def rebinding(self, stmt, word, args):
        """Rule f on a plain command whose known first word is one of REBINDERS (word), read as bash reads that word.
        The leading arguments that are options are read for their letters (`--` ends them): under one of
        INERT_OPTIONS (`unset -v`, `command -v`) the command binds and runs nothing. Then a NAMER's or a FORWARDER's
        argument whose known text, before any `=`, is a word the rules read is a finding naming what it shadows
        (`alias fail=true`, `enable -n echo`, `hash -p /x/git git`, `unset -f refuse`, `command git`), and so is one
        with no known text, which may name any of them; a FORWARDER's command is judged again when its own first word
        is a rebinder (`command unset -f refuse`). A RUNNER's argument is text or a file this walk has not read:
        `eval` with any argument, `source` or `.` with any but the one accepted shape (sourced_library), `trap` with
        an action that is not read whole (trap_action; the signal names after it are not text), `mapfile` or
        `readarray` with `-C`. No allow comment exempts it."""
        line = stmt["Pos"]["Line"]
        letters = set()
        while args and (text := word_text(args[0])) is not None and len(text) > 1 and text[0] in "-+":
            args = args[1:]
            if text == "--":
                break
            letters.update(text[1:])
        if letters & set(INERT_OPTIONS.get(word, "")):
            return
        names = ", ".join(f"`{name}`" for name in sorted(self.shadowed))
        unknown = f"`{word}` has an argument with no known text, which may name one of {names}"
        if word in RUNNERS:
            unread = f"which may define or rebind one of {names}"
            if word in SOURCES and sourced_library(args):
                return
            if word == "trap":
                args = args[:1]
            elif word not in SOURCES and word != "eval":  # mapfile, readarray: the callback is an option's argument
                if CALLBACK_OPTION in letters:
                    self.findings.add((line, SHADOW, f"`{word}` {RUNS[word]} this walk has not read, {unread}"))
                for arg in args:
                    if word_text(arg) is None:
                        self.findings.add((line, SHADOW, unknown))
                return
            for arg in args:
                text = word_text(arg)
                if text is None:
                    self.findings.add((line, SHADOW, f"`{word}` {RUNS[word]} with no known text, {unread}"))
                elif word != "trap" or not trap_action(text):
                    whole = " whole" if word == "trap" else ""  # one simple command is read; more is not
                    self.findings.add(
                        (line, SHADOW, f"`{word}` {RUNS[word]} this walk has not read{whole}, {unread}: `{text}`")
                    )
            return
        for arg in args:
            text = word_text(arg)
            if text is None:
                self.findings.add((line, SHADOW, unknown))
            elif (name := text.split("=", 1)[0]) in self.shadowed:
                self.findings.add((line, SHADOW, f"`{word}` names `{name}` and shadows {self.shadowed[name]}"))
        if word in FORWARDERS and args and (first := word_text(args[0])) in REBINDERS:
            self.rebinding(stmt, first, args[1:])

    def binding(self, assign):
        """Rule f on an assignment anywhere (plain, a prefix of a command, an argument of a declaration): one that
        gives a value to a variable that binds a command word (BINDING_VARIABLES) is a finding at its line.
        `export PATH` and `declare -A BASH_ALIASES` carry no value and bind nothing. No allow comment exempts it."""
        name = assign["Name"]["Value"]
        if name in BINDING_VARIABLES and ("Value" in assign or "Array" in assign):
            what = BINDING_VARIABLES[name]
            self.findings.add(
                (assign["Pos"]["Line"], SHADOW, f"an assignment to `{name}` binds a command word: {what}")
            )

    def tests_empty(self, stmt, target):
        """Whether the statement's own command is `[[ ! -s <target> ]]`, the two words shown to name one file."""
        cmd = command_of(stmt)
        if not isinstance(cmd, dict) or cmd.get("Type") != "TestClause":
            return False
        test = cmd.get("X")
        if not isinstance(test, dict) or test.get("Type") != "UnaryTest" or test.get("Op") != "!":
            return False
        inner = test.get("X")
        if not isinstance(inner, dict) or inner.get("Type") != "UnaryTest" or inner.get("Op") != "-s":
            return False
        return same_word(inner["X"], target)

    def empty_test(self, stmt, target, outer):
        """Whether a later statement of the producer's list tests `[[ ! -s <target> ]]` in a shape whose failure stops
        the script: None when the statement holds no such test, "" when it closes the producer, else why it does not,
        naming the test's line. The shapes: the last statement of an `if` condition; the left side of a `||` whose
        branch is one rule a accepts (branch_shape); a bare statement at the top level of a file whose prologue runs
        `set -euo pipefail` before it, where `set -e` ends the script on its failure (inside a function body, a block
        or an `if`, or in a file with no such prologue, nothing reads that failure). The test and every statement on
        its path to the top level must be in the foreground and not negated (flagged_path): `! [[ ! -s err ]] || exit
        1` reads a non-empty file as clean, `[[ ! -s err ]] &` ends only the job. The leftmost statement of an `&&`
        list or a pipeline is a test in neither shape."""
        cmd = command_of(stmt)
        kind = cmd.get("Type") if isinstance(cmd, dict) else None
        why = None
        if kind == "IfClause" and (cond := cmd.get("Cond") or []) and self.tests_empty(cond[-1], target):
            path = (cond[-1], stmt, *outer)
        elif kind == "BinaryCmd" and cmd.get("Op") == "||" and self.tests_empty(cmd["X"], target):
            path = (cmd["X"], stmt, *outer)
            shape = branch_shape(cmd["Y"], stmt, self.functions, self.defined, self.terminators)
            if shape is not None:
                why = f"is the left side of a `||` whose branch is {shape} and does not end the script"
        elif kind == "TestClause" and self.tests_empty(stmt, target):
            path = (stmt, *outer)
            if outer:
                around = outer[1] if len(outer) > 1 and function_body(outer[1]) is outer[0] else outer[0]
                why = (
                    f"is a bare statement inside {statement_name(around)} at line {around['Pos']['Line']}, not at the "
                    "top level where `set -e` ends the script on its failure"
                )
            elif self.set_e is None or self.set_e > stmt["Pos"]["Offset"]:
                why = (
                    "is a bare statement with no `set -euo pipefail` at the top level before it, so nothing reads its "
                    "failure"
                )
        elif kind == "BinaryCmd" and self.tests_empty(leftmost(stmt), target):
            path = (leftmost(stmt), stmt, *outer)
            why = (
                f"sits in {LIST_SHAPES.get(cmd.get('Op'), 'a list')} as neither the left side of a `||` nor the last "
                "statement of an `if` condition"
            )
        else:
            return None
        flag = flagged_path(path)
        if flag is not None:
            why = test_flag(flag[0], path[flag[1]], flag[1])
        return "" if why is None else f"the `[[ ! -s ]]` test at line {path[0]['Pos']['Line']} {why}"

    def prologue(self):
        """Rule c: a `set -euo pipefail` at top level, on no flagged path, before the first statement holding a
        substitution; else a finding at line 1 that names why the first one the file holds does not count."""
        if self.first_substitution is None:
            return
        before = self.top[: self.first_substitution]
        for stack in self.prologues:
            if len(stack) == 1 and flagged_path(stack) is None and any(stmt is stack[0] for stmt in before):
                return
        line = self.top[self.first_substitution]["Pos"]["Line"]
        self.findings.add(
            (
                1,
                PROLOGUE,
                "`set -euo pipefail` must run at top level before the first statement holding a command "
                f"substitution (line {line}): {self.prologue_why()}",
            )
        )

    def prologue_why(self):
        """Why the first `set -euo pipefail` of the file (by line) is not the prologue: it runs in a background job,
        is negated or runs in a coprocess (the options are set in a child shell, or not read), it sits inside a
        statement (a block, a subshell, a function definition, an `if`), or it comes after the first substitution."""
        if not self.prologues:
            return "the file holds none"
        stack = min(self.prologues, key=lambda path: path[0]["Pos"]["Offset"])
        line = stack[0]["Pos"]["Line"]
        flag = flagged_path(stack)
        if flag is not None:
            at = stack[flag[1]]["Pos"]["Line"]
            if flag[0] == BACKGROUND:
                return (
                    f"the one at line {line} runs in a background job started at line {at} (`&`), which sets the "
                    "options of a child shell only"
                )
            if flag[0] == NEGATED:
                return f"the one at line {line} is negated (`!`) at line {at}"
            return f"the one at line {line} runs in a coprocess started at line {at}, a child shell"
        if len(stack) > 1:
            outer = stack[-1]
            return (
                f"the one at line {line} runs inside {statement_name(outer)} at line {outer['Pos']['Line']}, not at "
                "the top level"
            )
        return f"the one at line {line} comes after it"


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
for kind in ("Stmt", "Assign", "CmdSubst", "Redirect"):
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
    except Unread as error:  # a value the walk does not read is "could not judge", never a clean file
        refuse(f"cannot judge {file}: {error}")
    except Exception as error:  # any other failure to read the tree is the same, never a clean file
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
