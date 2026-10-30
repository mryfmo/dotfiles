#!/usr/bin/env bash
# @file producer-status-check.sh
# @brief Refuse a command substitution outside the accepted grammar, a status-blind producer without its stderr capture, a missing `set -euo pipefail`, a `read` from a file, an alias, a function or rebinding that shadows a word the rules read, and a write to a guarded name outside the accepted writes.
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
#      own `!` aside) or is a `coproc`, and no process substitution (`<(…)`, `>(…)`) is on that path: `! x=$(…) ||
#      exit 1` reads the failure as success, `x=$(…) || exit 1 &`, `{ x=$(…) || exit 1; } &` and `( x=$(…) || exit
#      1 ) &` end only the background job, `coproc { x=$(…); } || exit 1` tests the coprocess's start, `cat <(x=$(…)
#      || exit 1)` and `tee >(x=$(…) || exit 1)` run the read in a child whose status the parent never sees (measured:
#      bash goes on with exit 0), and each is a finding naming the flagged statement's or the substitution's line. A
#      function body is not the top level: `f() { x=$(…) || return 1; }` is judged by its own path, whatever `f &`
#      does at the call. The branches that handle the status are a closed list:
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
#      foreground and not negated, with no process substitution on the path: `git ls-files > l 2> e &` lets the next
#      statement test `e` before the listing has finished, `! git ls-files > l 2> e` reads its failure as success, `{
#      git ls-files > l 2> e; } &` ends only the job, `coproc git ls-files > l 2> e` tests the coprocess's start and
#      `done < <(git ls-files)` runs it in a child whose failure the parent never sees, so each is a finding naming
#      the flag and its line whatever follows it; `! [[ ! -s err ]] || exit 1` reads a non-empty file as clean, `[[ !
#      -s err ]] &` ends only the job, and an `&&` list or a pipeline is not a test, so a producer whose only such
#      statement is one of those is a finding naming that statement's line and why. Stderr is captured only when the
#      last redirect of the statement that touches fd 2 is `2>`, `2>>` or `2>|` to a word whose known text is not
#      /dev/null, or whose parts are literals and parameter expansions (a process substitution, `2> >(tee e)`, is
#      neither, and one among a producer's words, `ls <(…)`, has no known text). The descriptor written before an
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
#   f. `shadow` and `binding`: the rules above trust a closed set of names by their spelling, GUARDED_NAMES below, one
#      dict with a reason per name: the builtins the rules read (`set`, c; `exit`, `return`, a form i; `echo`,
#      `printf`, the refusal grammar; `read`, d), the refusal functions (`refuse`, `fail`, a form ii), the rebinders of
#      this rule (REBINDERS, so the set is closed over itself: `alias command=eval` had passed, and `command 'refuse()
#      { return 0; }'` then redefined the refusal function through a word this rule read as its own), the library's
#      arrays (`GIT_ISOLATED_ENV`, exported word by word before every git; `GIT_ISOLATED_ARGS`,
#      `GIT_ISOLATED_SCRUB_NAMES`), the directory the one accepted `source` reads from (`LEVER_DIR`), the variables
#      that bind a command word (`PATH`, `BASH_ALIASES`, `BASH_CMDS`) and the ones bash itself reads when it runs a
#      lever (`BASH_ENV`, `ENV`, `SHELLOPTS`, `BASHOPTS`, `IFS`, `CDPATH`, `BASH_LOADABLES_PATH`, `EXECIGNORE`, `PS4`).
#      tests/unit/test_producer_status_check.py holds every literal name this walk compares against to that set, so
#      it cannot drift; the producers' first words come from the table and are protected as command words only.
#      `shadow`, the command words: a function definition of any name the rules read as a command word (interpreted:
#      the builtins, the producers, the refusal names, the rebinders), at any depth and in any spelling (`set() { :;
#      }` lets a warned listing pass a bare `[[ ! -s err ]]`, since the `set -euo pipefail` the test relies on ran a
#      function; `exit() { :; }`, `git() { command git "$@"; return 0; }`, `eval() { :; }`), is a finding at its
#      definition line naming what it shadows (a refusal name's definitions are judged by form ii: one, at top level,
#      before the read). So is every other way bash offers to rebind a word or to run text this walk has not read, a
#      plain command whose known first word is one of REBINDERS, read as bash reads that word (SKIPS_OPTIONS: for a
#      NAMER, a FORWARDER, `trap`, `mapfile` and `readarray` the leading `-` words are options read for their letters,
#      `--` ends them, a letter with an argument takes it, `hash -p /x`, and a `+` word is an argument; `source`, `.`
#      and `eval` skip nothing, every argument word is the file or the text; a call left with no argument to judge,
#      `source`, `enable -n`, `hash -p /usr/bin/true`, is a finding, `hash -r`, whose option is the whole job, aside):
#      an ALIASER (`alias`, `unalias`) in any form, `alias -p` and `alias ll='ls -l'` included, since no lever defines
#      an alias and non-interactive bash expands none unless `shopt -s expand_aliases` is set, so the rule has no
#      alias to accept (measured: the auditor's bypass exits 127 without that option and runs on with exit 0 under
#      it); the EXPANDER (`shopt`) with `expand_aliases` among its arguments in any spelling (`-s`, `-qs`, `-u`, after
#      `--`) or with an argument that has no known text (`shopt -s inherit_errexit` and `shopt -q nullglob` pass); a
#      NAMER (`enable`, `hash`, `unset`) with an argument whose known text, before any `=`, is such a name (`enable -n
#      echo`, `enable -n command`, `hash -p /x/true refuse`, `unset -f refuse`, and `unset refuse`, which removes the
#      function when no variable has the name) or with an argument that has no known text (`unset "$name"`; `unset
#      -v` names variables only and binds nothing, INERT_OPTIONS); a FORWARDER (`builtin`, `command`) whose arguments
#      name such a word or have no known text (`command git ls-files` runs past rule b), and whose command is judged
#      again when its own first word is a rebinder (`command unset -f refuse`, `command alias x=y`; `command -v` and
#      `-V` print and run nothing); a RUNNER whose text or file this walk has not read: `eval` with any argument,
#      `source` and `.` with any argument but the one accepted shape, `. "${LEVER_DIR}/git-isolated.sh"` or `.
#      "${LEVER_DIR}/read-lib.sh"`, the two libraries every lever sources (LIBRARY_DIR, LIBRARY_FILES; the parts of
#      the one argument, nothing else), `trap` with an action that is not empty, `-` or one simple command whose
#      first word is no rebinder (`trap cleanup EXIT` and `trap 'rm -f "${f}"' EXIT` are read whole; `trap 'refuse()
#      { :; }' DEBUG` redefines the function before the next command runs), `mapfile` or `readarray` with `-C` (the
#      callback is text bash runs).
#      `binding`, the writes: a write to a guarded name is (a) an Assign node whose name is guarded, with or without
#      a value, wherever it sits (a plain assignment, a command's prefix, `IFS= read -r x`, a declaration's argument,
#      `export PATH=/x/bin`, `declare -a GIT_ISOLATED_ENV=(x)`; shfmt writes no Value for `PATH=`, which writes the
#      empty string, nor for the bare name of `export PATH` or `declare +x -a GIT_ISOLATED_ENV`, each a write too);
#      (b) the variable of a `for` or `select`, and an expansion that assigns its parameter (`${PATH=x}`,
#      `${PATH:=x}`); (c) a word in any position (an argument of any command, a prefix's value, an array element, a
#      `for` list, a `case` pattern, a test or arithmetic operand, a redirect target, a coprocess name, a heredoc body
#      bash expands) whose leading literal parts spell an assignment to a guarded name (WRITES: `export
#      'PATH=/x/bin:$PATH'`, `env PATH=/x/bin git ls-files`, `'GIT_ISOLATED_ENV=PATH=/x/bin'`, `alias fail=true`) or
#      its literal parts hold the name of a guarded variable as a token (every guarded name the shadow part does not
#      read as a command word: `read -r PATH`, `printf -v PATH x`, `unset PATH`, `mapfile PATH`, `local -n ref=PATH`,
#      `(( PATH = 1 ))`, `${a[PATH=1]}`, `let 'PATH = 1'`, `unset 'a[PATH=1]'`, `bash -c 'cd /; PATH=x git'`, a
#      message that names it); a bare literal, a single-quoted, double-quoted, ANSI-C or locale string is a literal
#      part, the name is matched in the concatenation of every literal part, quotes removed and in order (`printf -v
#      PA"TH" x`, `PA'TH'=1`, `'PA'TH=1`; measured: each sets PATH), and in each part alone, and an expansion among
#      them contributes no text and hides none; (d) a word of a declaration (`declare`, `typeset`, `readonly`,
#      `export`, `local`, directly or through `builtin` or `command`) with no known text, which may spell any write
#      (`export "$binding"`, `export "${GIT_ISOLATED_ENV[@]}"`; a forwarder's own unknown argument is the shadow
#      finding above as well); (e) a declaration option under which a later assignment writes elsewhere (`declare
#      -i`, `local -n`; ATTRIBUTE_OPTIONS); (f) an operand where bash evaluates arithmetic (`(( ))`, `$(( ))`, `let`,
#      a C-style `for`, an array index or a slice, an operand of `-eq`, `-ne`, `-lt`, `-le`, `-gt`, `-ge`, of `-v` or
#      `-R`) that is not digits, operators and whitespace alone (ARITHMETIC_INERT): bash evaluates a name there
#      recursively (measured on bash 3.2: `y='PATH=1'` then `(( y, 1 ))`, `(( $y, 1 ))`, `[[ y -eq 1 ]]`, `a[y]=1`,
#      `let 'y + 1'` and `declare -i x; x=$y` each set PATH), so a name, a `$`, an expansion or a substitution there is
#      a write to any guarded name unless the exact text of its statement, in its file, is a row of
#      ACCEPTED_ARITHMETIC (the statements of the adopted set, measured and listed there: the `$#` tests, the status
#      and counter comparisons and increments, `exit $((128 + $2))`, the fetch retry `for`; `$#`, `$?` and `${#name}`
#      are rows too, no reading of which parameters are numbers is kept). The walk visits every node of every
#      statement and asks those questions of each; there is no list of positions. A write is accepted only when the
#      exact text of its statement, in its file, is a row of ACCEPTED_WRITES, the writes the adopted set makes
#      (measured and listed there: the `IFS=` prefixes of the levers' `read` lines, `LEVER_DIR=${dir}` of every
#      self-check, the library's three arrays, their `declare`, the `unset` loop over their names, `export
#      "${GIT_ISOLATED_ENV[@]}"`, the messages that name a guarded variable); any other is a finding naming the name,
#      how it is written, the statement's kind and the line. Not read: an expansion handed to an external command
#      (`env "$x" git`, `sudo "$x"`: that command's argument, which the shell does not bind; the one the library hands
#      `env` is the array a row pins), a name an expansion carries into a builtin that is no declaration (`unset -v
#      "$name"` of the scrubs, `printf -v "$3"` of the readers, `read -r "$name"`: the caller's name, by design), and a
#      literal heredoc body (data, skipped by every scan). An allow comment exempts nothing in rule f.
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
SHADOW = "shadow"  # rule f, a command word rebound
BINDING = "binding"  # rule f, a write to a guarded name outside the accepted writes
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
# body), and every process substitution around it (`<(…)`, `>(…)`: a child whose status the parent never sees, so
# the substitution itself is the flag; measured: `cat <(x=$(false) || exit 1); echo ran` prints `ran` and exits 0);
# a statement is flagged when it runs in the background (`&`), is negated (`!`) or runs a `coproc` clause.
BACKGROUND, NEGATED, COPROCESS, PROCESS = "Background", "Negated", "CoprocClause", "ProcSubst"
BRANCH_FLAGS = {  # how a finding names a flagged statement in a `||` branch
    BACKGROUND: "a command run in the background (`&`), which lets the script go on",
    NEGATED: "a negated command (`!`), whose failure status is read as success",
    COPROCESS: "a `coproc`, whose status is its start, not its command's",
    PROCESS: "a process substitution (`<(…)`, `>(…)`), whose failure the parent never sees",
}
DEFINITION_FLAGS = {  # how a finding names the flagged top-level definition of the function a `||` branch calls
    BACKGROUND: "runs in the background (`&`), so the function exists in a child shell only",
    NEGATED: "is negated (`!`), a flagged statement",
    COPROCESS: "runs in a coprocess, a child shell",
    PROCESS: "runs in a process substitution, a child shell",
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
    "LetClause": "a `let`",
    "TimeClause": "a `time`",
    "CoprocClause": "a `coproc`",
}
LIST_SHAPES = {"|": "a pipeline", "&&": "an `&&` list", "||": "a `||` list"}
PROLOGUE_WORDS = ["set", "-euo", "pipefail"]
READER = "read"  # the builtin rule d holds away from a file; a function of that name shadows it
STDERR = 2  # a descriptor is read as a decimal, so `02>` and `002>` name it too
FILE_OPS = (">", ">>", ">|")  # the only operators that, on fd 2, capture stderr to the word's file
BOTH_OPS = ("&>", "&>>")  # touch fd 2 with no descriptor written
DUP_OP = ">&"  # the operator a refusal body writes to stderr with (`>&2`, `1>&2`)
DUP_OPS = (DUP_OP, "<&")  # to a plain descriptor (`>&1`, `>&-`) each moves the one before it; to any other word fd 2
UNCAPTURED = object()  # the stderr target when the last redirect touching fd 2 is not one of FILE_OPS
# Rule f's rebinders: every plain command bash offers that binds a command word to other text, a file, a builtin or
# nothing, or runs text this walk has not read, each read as bash reads it (measured on /bin/bash 3.2.57; the bash 4
# builtins by the manual). An ALIASER defines, prints or removes an alias (`alias`, `unalias`): no lever defines one,
# and non-interactive bash expands none unless `shopt -s expand_aliases` is set (or BASHOPTS is inherited), so every
# call is a finding, in any form, and so is the EXPANDER (`shopt`) naming EXPAND_ALIASES (measured: `alias
# command=eval` then `command 'refuse() { return 0; }'` exits 127 without the option and redefines the function under
# it). A NAMER's arguments are names: `enable` (`-n` disables a builtin, `-f` loads one), `hash` (`-p` binds a word to
# a file) and `unset` (`-f` names a function, and so does a name with no variable; `-v` names variables only). A
# FORWARDER runs its arguments as a command past any function (`command unset -f refuse`, `builtin unset -f refuse`;
# `command -v`/`-V` print and run nothing). A RUNNER's argument is text or a file: `eval`, `source` and `.` (the one
# accepted shape is sourced_library), `trap` (an action read whole is trap_action), `mapfile` and `readarray` (`-C`
# names a callback). Every rebinder is itself a word interpreted protects (the set is closed over itself), so `enable
# -n command`, `hash -p /usr/bin/true command`, `unset -f eval` or `eval() { :; }` is a finding like `enable -n echo`.
# A `declare`, `typeset`, `readonly`, `export` or `local` acts on variables, and with `-f` on a function it leaves
# bound (`export -f refuse`, `readonly -f refuse`, measured), so none is a rebinder.
ALIASERS = ("alias", "unalias")
ALIAS_ACTS = {"alias": "defines or prints an alias", "unalias": "removes an alias"}  # how a finding names an ALIASER
EXPANDER = "shopt"
EXPAND_ALIASES = "expand_aliases"  # the one shopt option under which a script expands aliases
NAMERS = ("enable", "hash", "unset")
FORWARDERS = ("builtin", "command")
RUNNERS = ("eval", "source", ".", "trap", "mapfile", "readarray")
REBINDERS = ALIASERS + (EXPANDER,) + NAMERS + FORWARDERS + RUNNERS
INERT_OPTIONS = {"unset": "v", "command": "vV"}  # the option letters under which the word binds and runs nothing
# How rule f reads a rebinder's leading arguments, as bash reads that word (measured on bash 3.2). Under
# `skips_options` a leading argument whose known text starts with `-` and is longer than it is a cluster of option
# letters, `--` ends the options, and a letter of OPTION_ARGUMENTS takes the rest of its cluster or the next word
# (`hash -p /x`, `enable -f file`, `mapfile -C cb`); a `+` word is an argument to every rebinder (`hash +r` is looked
# up as a name, `unset +f` is not a valid identifier), and so is a word with no known text, which ends the options.
# `source`, `.` and `eval` skip nothing: every argument word is the file or the text bash reads (`source -- file` and
# `source +file` read the file; the audit's `source +payload.sh` had been read as an option with no file after it, and
# passed). An ALIASER and the EXPANDER are not here: every call of the one, and every argument of the other, is judged.
SKIPS_OPTIONS = {
    "enable": True,
    "hash": True,
    "unset": True,
    "builtin": True,
    "command": True,
    "trap": True,
    "mapfile": True,
    "readarray": True,
    "eval": False,
    "source": False,
    ".": False,
}
OPTION_ARGUMENTS = {"hash": "p", "enable": "f", "mapfile": "CcdnOsu", "readarray": "CcdnOsu"}  # the letters with one
# The option letters that are a rebinder's whole job with no name: `hash -r` flushes the table (`alias -p`, which
# prints it, is an ALIASER's call and a finding since round 16). A rebinder left with no argument after its options,
# and not only such letters, has no argument to judge and is a finding (`source`, `enable -n`, `hash -p
# /usr/bin/true`, `trap -p`: bash prints or binds nothing for most, measured, but the rule judges names and has none),
# so a word the option reading took for an option is never silence.
BARE_OPTIONS = {"hash": "r"}
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
# Rule f's guarded names, one closed set: every name the rules above trust by its spelling (the refusal names, the
# builtins, the rebinders, the library arrays and the directory the accepted `source` reads from) and the variables
# bash itself reads when it runs a lever (measured on /bin/bash 3.2.57; the bash 4 ones by the manual), name -> why a
# write to it is judged. tests/unit/test_producer_status_check.py holds every literal name this walk compares against
# to this set, so it cannot drift. A write to one of them is a finding unless its statement is in ACCEPTED_WRITES.
GUARDED_NAMES = {
    "PATH": "the directories bash searches for `git`, `find`, `ls` and every other command word",
    "BASH_ALIASES": "the alias table of bash 4, which `alias` writes",
    "BASH_CMDS": "the hash table of bash 4, which `hash -p` writes",
    "GIT_ISOLATED_ENV": "the array git_isolated of git-isolated.sh exports word by word before it execs git",
    "GIT_ISOLATED_ARGS": "the array git_isolated passes to git before the caller's arguments",
    "GIT_ISOLATED_SCRUB_NAMES": "the names git_env_scrub of git-isolated.sh removes from the environment",
    "LEVER_DIR": "the directory the one accepted `source` reads the two libraries from (rule f)",
    "refuse": "a refusal function a `||` branch calls (rule a, form ii)",
    "fail": "a refusal function a `||` branch calls (rule a, form ii)",
    "set": "the builtin the prologue `set -euo pipefail` relies on (rule c)",
    "exit": "the builtin a `||` branch ends a failed read with (rule a, form i)",
    "return": "the builtin a `||` branch ends a failed read with (rule a, form i)",
    "echo": "the builtin the refusal grammar writes to stderr with (rule a)",
    "printf": "the builtin the refusal grammar writes to stderr with (rule a)",
    "read": "the builtin rule d holds away from a file",
    "declare": "a declaration rule f reads the words and attribute options of",
    "typeset": "a declaration rule f reads the words and attribute options of",
    "readonly": "a declaration rule f reads the words and attribute options of",
    "export": "a declaration rule f reads the words and attribute options of",
    "local": "a declaration rule f reads the words and attribute options of",
    "alias": "a rebinder rule f reads a rebinding by",
    "unalias": "a rebinder rule f reads a rebinding by",
    "shopt": "a rebinder rule f reads a rebinding by",
    "enable": "a rebinder rule f reads a rebinding by",
    "hash": "a rebinder rule f reads a rebinding by",
    "unset": "a rebinder rule f reads a rebinding by",
    "builtin": "a rebinder rule f reads a rebinding by",
    "command": "a rebinder rule f reads a rebinding by",
    "eval": "a rebinder rule f reads a rebinding by",
    "source": "a rebinder rule f reads a rebinding by",
    ".": "a rebinder rule f reads a rebinding by (no identifier: bash cannot assign it, so no write spells it)",
    "trap": "a rebinder rule f reads a rebinding by",
    "mapfile": "a rebinder rule f reads a rebinding by",
    "readarray": "a rebinder rule f reads a rebinding by",
    "BASH_ENV": "the file every non-interactive bash reads before its script (a child `bash` of a lever)",
    "ENV": "the file a POSIX-mode shell (`sh`, `bash --posix`) reads before its script",
    "SHELLOPTS": "the `set -o` options a child bash inherits when it is exported (`posix`, `xtrace`)",
    "BASHOPTS": "the `shopt` options a child bash inherits when it is exported (`expand_aliases`)",
    "IFS": "the characters word splitting and `read` split on (`for name in ${names}` of git_env_scrub)",
    "CDPATH": "the directories `cd` searches for a relative argument",
    "BASH_LOADABLES_PATH": "the directories `enable -f` searches for a loadable builtin",
    "EXECIGNORE": "the paths bash skips when it searches PATH (bash 4.4)",
    "PS4": "the prompt bash expands, command substitutions included, before each traced command (`set -x`)",
}
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
# A word's first literal part that spells an assignment to a guarded name: the name, an index and a `+` allowed, then
# `=` (`PATH=/x/bin:`, `PATH[0]=x`, `PATH+=:x`, `GIT_ISOLATED_ENV=PATH=/x/bin`, `fail=true` as an `alias` word).
WRITES = re.compile(
    "(" + "|".join(re.escape(name) for name in GUARDED_NAMES if IDENTIFIER.fullmatch(name)) + r")(?:\[[^]]*\])?\+?="
)
# The text bash evaluates as arithmetic, where any name may be assigned (`(( PATH = 1 ))`, `a[PATH=1]=x`, `let 'PATH
# = 1'`, `${a[PATH=1]}`, `${x:PATH=1}`, and `[[ $y -eq 1 ]]`, whose operands bash evaluates): the node kinds that open
# one, the fields of an Assign or ParamExp that hold one, the test operators whose operands are one, and the test
# operators whose operand is a name with a subscript bash evaluates (`[[ -v 'a[PATH=1]' ]]`). Bash evaluates a name
# there recursively, so a bare identifier is a write to whatever its value spells (measured on bash 3.2: `y='PATH=1'`
# then `(( y, 1 ))`, `(( $y, 1 ))`, `[[ y -eq 1 ]]`, `[[ $y -eq 1 ]]`, `a[y]=1`, `a[$y]=1` and `let 'y + 1'` each set
# PATH). An operand is inert only when every part is a literal and its text is digits, operators and whitespace alone
# (ARITHMETIC_INERT: `1`, `128`, `'1 + 2'`, the `@` and `*` of a whole-array subscript); any other operand (a name, a
# `$`, a letter, a backquote, an expansion, a substitution) is a write to any guarded name unless the exact text of its
# statement, in its file, is a row of ACCEPTED_ARITHMETIC. `$#`, `$?`, `${#name}` and a hex literal are not inert: a
# parameter bash alone sets is accepted by a row, never by a reading of which parameters those are.
ARITHMETIC_KINDS = ("ArithmCmd", "ArithmExp", "LetClause", "CStyleLoop")
ARITHMETIC_FIELDS = ("Index", "Slice")
ARITHMETIC_TESTS = ("-eq", "-ne", "-lt", "-le", "-gt", "-ge")
NAME_TESTS = ("-v", "-R")
ARITHMETIC_INERT = re.compile(r"[0-9\s+\-*/%<>=!&|^~?:(),@]*")
ASSIGNING_OPS = ("=", ":=")  # the parameter expansions that write their parameter (`${PATH=x}`, `${PATH:=x}`)
DECLARERS = ("declare", "typeset", "readonly", "export", "local")  # the words shfmt parses as a DeclClause
# The declaration options under which a later plain assignment writes elsewhere: `-i` evaluates the value as
# arithmetic (`declare -i x; x=$y` with `y='PATH=1'` sets PATH, measured on bash 3.2), `-n` makes the name a reference
# that writes the variable its value names (`local -n r=PATH; r=x`). `export -n` removes the export attribute only.
ATTRIBUTE_OPTIONS = {"declare": "in", "typeset": "in", "local": "in"}
# The accepted writes: the exact text of each statement of the adopted set (this lint, scripts/orchestrator/read-lib.sh,
# git-isolated.sh and the five levers) that writes a guarded name, as (the file names it is accepted in, the statement
# text from its first byte to its last, why). A statement is accepted only when its file and its bytes both match: a
# changed flag of the library, a new `IFS=` prefix in a lever, the same text in another file is a finding until a row
# names it. Measured on head fb2774e9 (U112 round 20), plus the rows of the pr-merge.sh disposition gate (U119 round
# 5) and of the pr-audit.sh round cap (U120 round 4); nothing else writes a guarded name there. This Python sits in a
# command substitution around a heredoc: bash 3.2 scans the body for quotes and backticks before the heredoc is read,
# so a row text must keep them balanced as bash counts them (a text holding both kinds of quote is a double-quoted
# Python string with the inner double quotes escaped), else the lint refuses to start and the enforced-set test fails.
LEVERS = ("records-sync.sh", "pr-audit.sh", "pr-merge.sh", "pr-threads-check.sh", "pr-body-edit.sh")
LIBRARIES = ("read-lib.sh", "git-isolated.sh")
ACCEPTED_WRITES = (
    (
        LIBRARIES + LEVERS,
        r"""LEVER_DIR=${dir}""",
        "lever_self_check of every lever and library sets the directory the libraries are sourced from, from its own "
        "resolved path",
    ),
    (
        ("git-isolated.sh",),
        r"""for git_isolated_name in GIT_ISOLATED_ENV GIT_ISOLATED_ARGS GIT_ISOLATED_SCRUB_NAMES; do
    unset -v "${git_isolated_name}" 2> /dev/null || {
        echo "git-isolated.sh: refused: ${git_isolated_name} is readonly in the sourcing shell; the library cannot assign it" >&2
        exit 2
    }
done""",
        "the library unsets its three arrays before it assigns them, so a caller's export of one is not kept (audit "
        "round 2 P1)",
    ),
    (
        ("git-isolated.sh",),
        r"""declare +x -a GIT_ISOLATED_ENV GIT_ISOLATED_ARGS GIT_ISOLATED_SCRUB_NAMES""",
        "the library declares its three arrays unexported",
    ),
    (
        ("git-isolated.sh",),
        r"""GIT_ISOLATED_ENV=(
    # No global config file: no `url.*.insteadOf`, credential helper, hook path, identity or include of ~/.gitconfig
    # or $XDG_CONFIG_HOME/git/config (research 01 section 1.1; records-sync.sh U101, the redirected push).
    GIT_CONFIG_GLOBAL=/dev/null
    # No system config file $(prefix)/etc/gitconfig (research 01 section 1.1).
    GIT_CONFIG_NOSYSTEM=1
    # No system attributes file $(prefix)/etc/gitattributes, so it names no filter driver (research 01 section 1.4
    # item 3; pr-audit.sh U71b audit round 1, a filter driver run on the audited tree).
    GIT_ATTR_NOSYSTEM=1
    # No credential or passphrase prompt on the terminal: a transport that needs one fails instead of waiting
    # (pr-audit.sh U71b, the bounded fetch).
    GIT_TERMINAL_PROMPT=0
)""",
        "the library's environment of every isolated git, the flag set the levers document",
    ),
    (
        ("git-isolated.sh",),
        r"""GIT_ISOLATED_ARGS=(
    # No replacement refs: a `refs/replace/*` of the repository cannot stand in for an object (pr-audit.sh U71b audit
    # round 7, with GIT_NO_REPLACE_OBJECTS).
    --no-replace-objects
    # No hook of any repository runs: git's documented off switch (research 01 section 1.1; records-sync.sh U101 round
    # 6, a post-checkout hook that planted files in the sync).
    -c core.hooksPath=/dev/null
    # No fsmonitor program: a hook path in core.fsmonitor ran inside `git ls-files` (measured, research 01 section 1.1;
    # records-sync.sh U101 round 12).
    -c core.fsmonitor=false
    # No user attributes file ($XDG_CONFIG_HOME/git/attributes), so no filter, diff or merge driver comes from it
    # (research 01 section 1.4 item 3; pr-audit.sh git_tree).
    -c core.attributesFile=/dev/null
    # No commit-graph file of the repository: an ancestry read (merge-base) must not trust a file the checkout wrote
    # (pr-audit.sh git_safe and git_tree).
    -c core.commitGraph=false
    # No ssh program: the ssh transport fails, whatever `core.sshCommand` any config names (research 01 section 1.1;
    # scripts/lint-comparisons.py GIT_C).
    -c core.sshCommand=false
    # Every transport off by default (file, git, ext, and any `insteadOf` rewrite to one); a caller re-opens one per
    # command, as the tests do with `-c protocol.file.allow=always` (research 01 section 1.1; hcom-seat U85).
    -c protocol.allow=never
    # https is the one transport left on: the levers fetch and push over https only (scripts/lint-comparisons.py GIT_C).
    -c protocol.https.allow=always
    # The empty helper resets the helper list, so no helper of any config answers; a caller adds its own after it
    # (records-sync.sh: `!gh auth git-credential`, standing order 19; research 01 section 1.1).
    -c credential.helper=
    # No credential prompt (research 01 section 1.1).
    -c credential.interactive=false
    # No automatic gc in a scratch repository that is removed on exit (records-sync.sh git_scratch; tests U100).
    -c gc.auto=0
    # No detached maintenance process left behind a command (records-sync.sh git_scratch; tests U100).
    -c maintenance.auto=false
)""",
        "the library's arguments before the caller's, the flag set the levers document",
    ),
    (
        ("git-isolated.sh",),
        r"""GIT_ISOLATED_SCRUB_NAMES=(http_proxy HTTPS_PROXY https_proxy HTTP_PROXY NO_PROXY no_proxy SSL_CERT_FILE SSL_CERT_DIR CURL_CA_BUNDLE)""",
        "the names the library's scrub removes besides GIT_*",
    ),
    (
        ("git-isolated.sh",),
        "echo \"${who}: refused: GIT_ISOLATED_ENV is empty; the library's flag set is gone\" >&2",
        "a refusal message naming the array (a word, not a write)",
    ),
    (
        ("git-isolated.sh",),
        "echo \"${who}: refused: GIT_ISOLATED_ARGS is empty; the library's flag set is gone\" >&2",
        "a refusal message naming the array (a word, not a write)",
    ),
    (
        ("git-isolated.sh",),
        "echo \"${who}: refused: GIT_ISOLATED_SCRUB_NAMES is empty; the library's flag set is gone\" >&2",
        "a refusal message naming the array (a word, not a write)",
    ),
    (
        ("git-isolated.sh",),
        r'''export "${GIT_ISOLATED_ENV[@]}"''',
        "git_isolated exports the pinned array word by word in the subshell that execs git",
    ),
    (
        ("records-sync.sh",),
        r"""IFS= read -r -d '' dir;""",
        "an empty IFS for the one `read` of a NUL-separated listing, restored after it",
    ),
    (
        ("records-sync.sh",),
        r"""IFS= read -r -d '' path;""",
        "an empty IFS for the one `read` of a NUL-separated listing, restored after it",
    ),
    (
        ("records-sync.sh",),
        r"""IFS= read -r -d '' entry;""",
        "an empty IFS for the one `read` of a NUL-separated listing, restored after it",
    ),
    (
        ("pr-audit.sh",),
        r"""IFS= read -r git_name;""",
        "an empty IFS for the one `read` of the environment listing, restored after it",
    ),
    (
        ("pr-audit.sh", "pr-body-edit.sh", "pr-merge.sh"),
        r"""IFS= read -r line;""",
        "an empty IFS for the one `read` of a line, restored after it",
    ),
    (
        ("pr-audit.sh",),
        r"""refuse 'no codex on PATH'""",
        "a refusal message naming PATH (a word, not a write)",
    ),
    (
        ("pr-audit.sh",),
        r"""refuse 'no python3 on PATH (it runs the codex supervisor)'""",
        "a refusal message naming PATH (a word, not a write)",
    ),
    (
        ("pr-audit.sh",),
        r'''IFS=$'\t' read -r state base want pr_url <<< "${view}"''',
        "a tab IFS for the one `read` of gh's TSV row, restored after it",
    ),
    (
        ("pr-audit.sh",),
        r"""IFS= read -r path;""",
        "an empty IFS for the one `read` of a line, restored after it",
    ),
    (
        ("pr-audit.sh",),
        r"""IFS=' ' read -r access path;""",
        "a space IFS for the one `read` of an access and a path, restored after it",
    ),
    (
        ("pr-merge.sh",),
        r'''IFS=$'\t' read -r state base head draft <<< "${view}"''',
        "a tab IFS for the one `read` of gh's TSV row, restored after it",
    ),
    (
        ("pr-merge.sh",),
        r'''IFS=$'\t' read -r again again_base <<< "${again}"''',
        "a tab IFS for the one `read` of gh's TSV row, restored after it",
    ),
    (
        ("pr-merge.sh",),
        r"""IFS=$'\t' read -r bucket name;""",
        "a tab IFS for the one `read` of gh's TSV rows, restored after it",
    ),
    (
        ("pr-merge.sh",),
        r'''IFS=$'\t' read -r state commit merged_base merged_head <<< "${after}"''',
        "a tab IFS for the one `read` of gh's TSV row, restored after it",
    ),
    (
        ("pr-merge.sh",),
        r"""IFS= read -r row;""",
        "an empty IFS for the one `read` of a units.tsv row, restored after it (the disposition gate, U119)",
    ),
    (
        ("pr-merge.sh",),
        r'''IFS=$'\t' read -ra cols <<< "${line}"''',
        "a tab IFS for the `read` of a validated dispositions.tsv row into its eight columns, restored after it (the "
        "disposition gate, U119)",
    ),
    (
        ("pr-threads-check.sh",),
        r"""IFS=$'\t' read -r first resolved created severity count reply;""",
        "a tab IFS for the one `read` of gh's TSV rows, restored after it",
    ),
    (
        ("pr-body-edit.sh",),
        r'''IFS=$'\t' read -r number head state <<< "${view}"''',
        "a tab IFS for the one `read` of gh's TSV row, restored after it",
    ),
)
# The accepted arithmetic: the exact text of each statement of the adopted set that holds an operand bash evaluates as
# arithmetic which is not inert (ARITHMETIC_INERT), as (the file names, the statement text, why), measured on head
# fb2774e9 (U112 round 20) with this table empty, plus the rows of the pr-merge.sh disposition gate (U119 round 5)
# and of the pr-audit.sh round cap (U120 round 4).
# Every operand there is a name the statement itself assigned a decimal to, a count of `$#` or `${#array[@]}`, or the
# signal number a trap passes; a row holds in its file alone, and a changed character is a finding until a row names
# it. The same quoting rule as ACCEPTED_WRITES applies.
ACCEPTED_ARITHMETIC = (
    (("producer-status-check.sh",), r"""(($# == 0));""", "this lint refuses an empty argument list"),
    (("read-lib.sh",), r"""(($# >= 1))""", "a reader's argument count"),
    (
        ("read-lib.sh",),
        r"""((rc_status != 0 && rc_status != 1));""",
        "the status of `git config --get`, assigned `$?` by the statement before it",
    ),
    (("read-lib.sh",), r"""((rc_status == 0))""", "the same status"),
    (("read-lib.sh",), r"""((rf_status != 0));""", "the status of a `cat`, assigned `$?` by the statement before it"),
    (
        ("read-lib.sh",),
        r"""((rl_status != 0));""",
        "the status of a `git ls-files`, assigned `$?` by the statement before it",
    ),
    (("git-isolated.sh",), r"""((listed))""", "a count the library's own loop incremented"),
    (("records-sync.sh", "pr-threads-check.sh"), r"""(($#));""", "the argument count of an option loop"),
    (("records-sync.sh", "pr-threads-check.sh"), r"""(($# >= 2))""", "an option that takes a value needs two words"),
    (("records-sync.sh",), r"""((${#programs[@]} == 1))""", "the count of the program directories found"),
    (("records-sync.sh",), r"""((${#files[@]} + ${#gone[@]} > 0))""", "the counts of the files to sync and to remove"),
    (("records-sync.sh",), r"""((${#masked[@]}));""", "the count of the masked copies"),
    (
        ("records-sync.sh", "pr-audit.sh", "pr-merge.sh"),
        r"""((status == 0))""",
        "a status the statement before it assigned `$?` or 0",
    ),
    (("records-sync.sh",), r"""((status != 1))""", "the same status"),
    (
        ("records-sync.sh",),
        r"""n=$((last + 1))""",
        "the next record number after the last one listed, a decimal by regex",
    ),
    (
        ("pr-audit.sh",),
        r"""((status == 125))""",
        "the status of the audit run, assigned `$?` by the statement before it",
    ),
    (("pr-audit.sh",), r"""exit $((128 + $2))""", "the signal number the lever's own trap passes as $2, added to 128"),
    (("pr-audit.sh",), r"""((signal_hold));""", "a flag the trap sets to 1"),
    (("pr-audit.sh",), r"""((${#text} == size))""", "the byte count of AGENTS.md against the size git reported"),
    (("pr-audit.sh",), r"""headings=$((headings + 1))""", "a counter of `## Audit` headings"),
    (("pr-audit.sh",), r"""((inside));""", "a flag the heading loop sets to 1 or 0"),
    (("pr-audit.sh",), r"""((headings == 1))""", "the same counter"),
    (("pr-audit.sh",), r"""[[ $# -eq 1 ]]""", "the lever's argument count"),
    (
        ("pr-audit.sh",),
        r"""[[ ${template_entries} -gt 0 ]]""",
        "an arithmetic test of a grep count; the `fail` after the count takes every status but 0 and 1, so the value is "
        "a decimal",
    ),
    (("pr-audit.sh",), r"""((root_denies == 1))""", "a grep count of the sandbox profile's root denial"),
    (("pr-audit.sh",), r"""count=$((count + 1))""", "a counter of the settings lines"),
    (("pr-audit.sh",), r"""((count == 1))""", "the same counter"),
    (
        ("pr-audit.sh",),
        # The one row with a continuation line: bash 3.2 joins a backslash-newline of this quoted heredoc inside its
        # command substitution (measured), so the backslash and the newline are Python escapes here, not source bytes.
        "for ((try = 1; try <= wait_tries; try++)); do\n"
        "    # `bounded` is a perl exec, which cannot run a shell function, so the fetch carries the library's own "
        "arrays, and\n"
        "    # after them the gh helper, the shape of records-sync.sh's push: the library's empty helper resets the "
        "list and the\n"
        "    # later `-c` wins, so a private origin answers to the gh login and to no helper of the operator's "
        "configuration.\n"
        '    bounded "${gh_timeout}" env "${GIT_ISOLATED_ENV[@]}" git "${GIT_ISOLATED_ARGS[@]}" -c '
        "'credential.helper=!gh auth git-credential' \\\n"
        '        -C "${clone}" fetch -q --no-tags "${url}" "+refs/pull/${pr}/head:refs/audit/head" '
        "'+refs/heads/main:refs/audit/main' || # git-isolated: allow bounded exec of the library's own arrays\n"
        '        fail "git fetch of refs/pull/${pr}/head and main from ${url} failed"\n'
        "    head=$(git_isolated -C \"${clone}\" rev-parse --verify --quiet 'refs/audit/head^{commit}') || head='' "
        "# producer-status: allow the head test after the loop refuses an empty head\n"
        '    [[ ${head} != "${want}" ]] || break\n'
        '    ((try == wait_tries)) || sleep "${wait_seconds}"\n'
        "done",
        "the fetch retry loop: `try` is the loop's own counter and `wait_tries` a decimal of the lever; the whole `for` "
        "is the statement, so its body is pinned byte for byte too",
    ),
    (("pr-audit.sh",), r"""((try == wait_tries))""", "the last try of that loop"),
    (("pr-audit.sh",), r"""entries=$((entries + 1))""", "a counter of the template's filesystem entries"),
    (("pr-audit.sh",), r"""((entries == template_entries))""", "that counter against the grep count"),
    (("pr-audit.sh",), r"""((rendered == resolved))""", "two counts of the rendered config's paths"),
    (
        ("pr-audit.sh",),
        r"""((status != 0))""",
        "the status of the sandbox probe, assigned `$?` by the statement before it",
    ),
    (("pr-audit.sh",), r"""(($# > 0));""", "the argument count of the option loop (the round cap, U120)"),
    (
        ("pr-audit.sh",),
        r"""[[ $# -ge 2 && -n $2 && ${records_given} == 0 ]]""",
        "an option that takes a value needs two words, and `--records` is given once (its own sentinel, U120 round 5)",
    ),
    (("pr-audit.sh",), r"""unit_lines=$((unit_lines + 1))""", "a counter of the body's Program-Unit lines"),
    (("pr-audit.sh",), r"""((unit_lines <= 1))""", "the same counter, at most one line"),
    (("pr-audit.sh",), r"""((unit_lines == 1));""", "the same counter, one line names a program pull request"),
    (("pr-merge.sh",), r"""[[ $# -ge 1 ]]""", "the lever's argument count"),
    (("pr-merge.sh",), r"""[[ $# -eq 2 && $1 == --records && -n $2 ]]""", "the lever's argument count and words"),
    (
        ("pr-merge.sh",),
        r"""((merge_status == 0))""",
        "the status of `gh pr merge`, assigned `$?` by the statement before it",
    ),
    (("pr-merge.sh",), r"""((seen == 0));""", "a flag the Findings loop of the disposition gate sets to 1 (U119)"),
    (("pr-merge.sh",), r"""((section == 1))""", "a flag the same loop sets to 1 or 0"),
    (("pr-merge.sh",), r"""((seen == 1))""", "the same flag, after the loop"),
    (("pr-merge.sh",), r"""((${#findings[@]} > 0))""", "the count of the Findings lines collected"),
    (("pr-merge.sh",), r"""((${#pending[@]} > 0))""", "the count of the P2 and P3 findings collected"),
    (("pr-merge.sh",), r"""n=$((n + 1))""", "a counter of the dispositions.tsv lines"),
    (
        ("pr-merge.sh",),
        r"""((status == 0));""",
        "the status of unit_row_exists, assigned 0 or `$?` by the statements before it",
    ),
    (("pr-merge.sh",), r"""((satisfied == 1))""", "a flag the disposition loop sets to 1"),
    (("pr-threads-check.sh",), r"""((fix_time < created));""", "two epoch seconds `date` printed"),
    (("pr-threads-check.sh",), r"""((seen_head))""", "a flag the listing loop sets to 1"),
    (("pr-threads-check.sh",), r"""((count <= 100))""", "the comment count of a thread, a field of gh's TSV row"),
    (("pr-threads-check.sh",), r"""threads=$((threads + 1))""", "a counter of the threads listed"),
    (("pr-threads-check.sh",), r"""open=$((open + 1))""", "a counter of the open threads"),
    (("pr-threads-check.sh",), r"""((open == 0))""", "the same counter"),
    (
        ("pr-body-edit.sh",),
        r"""((size == 0 || size > 65536))""",
        "the body's byte count, a decimal by the regex before it",
    ),
    (("pr-body-edit.sh",), r"""[[ $# -eq 2 && $1 == --body-file ]]""", "the lever's argument count and word"),
)
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
    """The command words the rules read as bash builtins, as the producers of the table, as the refusal functions or
    as the rebinders of rule f, name -> what a rebinding of that name shadows: `set` (the prologue, rule c), `exit`
    and `return` (form i of rule a), `echo` and `printf` (the refusal grammar, forms ii and iii), the first word of
    every producer row (rule b), REFUSAL_NAMES (form ii) and REBINDERS (rule f reads a rebinding by them, so the set
    is closed over itself: `alias command=eval` had rebound one unseen). Built from the data those rules hold, so a
    word added to one of them is covered without a second list. A function definition of a refusal name is judged by
    form ii (one, at top level, before the read), of any other word by Walk.run."""
    words = {PROLOGUE_WORDS[0]: "the builtin the prologue `set -euo pipefail` relies on (rule c)"}
    for name in REFUSAL_NAMES:
        words[name] = "the refusal function a `||` branch calls (rule a, form ii)"
    for name in TERMINATORS:
        words[name] = "the builtin a `||` branch ends a failed read with (rule a, form i)"
    for name in WRITERS:
        words[name] = "the builtin the refusal grammar writes to stderr with (rule a, forms ii and iii)"
    words[READER] = "the builtin rule d holds away from a file (`read < file` is a finding)"
    for name in DECLARERS:
        words[name] = "the declaration whose words and attribute options rule f reads (rule f)"
    for name in REBINDERS:
        words[name] = "a rebinder of the lint's own rebinders, the words rule f reads a rebinding by (rule f)"
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


def literal_texts(word):
    """(the text of the word's leading literal parts, joined; the text of every literal part, in order): what rule f
    scans a word for a write with. A literal part is a bare literal, a single-quoted string (ANSI-C included, as
    written), or a literal inside double quotes (a locale string included). An expansion, a substitution or a glob
    part contributes no text and hides none: the parts around it are read, and it ends the leading run."""
    leading = []
    texts = []
    still_leading = True
    todo = list(word.get("Parts") or [])
    while todo:
        part = todo.pop(0)
        kind = part.get("Type")
        if kind == "DblQuoted":
            todo = list(part.get("Parts") or []) + todo
        elif kind in ("Lit", "SglQuoted"):
            texts.append(part.get("Value") or "")
            if still_leading:
                leading.append(texts[-1])
        else:
            still_leading = False
    return "".join(leading), texts


def inert_operand(word):
    """Whether a word where bash evaluates arithmetic evaluates no text of a script's choosing: every part a literal
    (a bare literal, a quoted string, double quotes around them) whose text is digits, operators and whitespace alone
    (ARITHMETIC_INERT): `1`, `128`, `'1 + 2'`, the `@` or `*` of a whole-array subscript. A name (bash evaluates it
    recursively: `y='PATH=1'; (( y, 1 ))` sets PATH), a `$` in any part, a letter, a backquote, an expansion or a
    substitution is not inert; `$#`, `$?` and `${#name}` are not read as numbers here, a row accepts their statements."""
    todo = list(word.get("Parts") or [])
    while todo:
        part = todo.pop(0)
        kind = part.get("Type")
        if kind == "DblQuoted":
            todo = list(part.get("Parts") or []) + todo
        elif kind in ("Lit", "SglQuoted"):
            if not ARITHMETIC_INERT.fullmatch(part.get("Value") or ""):
                return False
        else:
            return False
    return True


def written_in(stmt):
    """How a write's finding names the statement it sits in: a declaration by its word, else statement_name."""
    cmd = command_of(stmt)
    if isinstance(cmd, dict) and cmd.get("Type") == "DeclClause":
        return f"the declaration `{cmd['Variant']['Value']}`"
    return statement_name(stmt)


def leading_options(word, args):
    """The option letters of a rebinder's leading arguments and the arguments after them, as SKIPS_OPTIONS reads that
    word: a leading argument whose known text is `-` and letters is a cluster, `--` ends the options, a letter of
    OPTION_ARGUMENTS takes the rest of its cluster or the next word; a `+` word, a bare `-` and a word with no known
    text are arguments and end the options. For `source`, `.` and `eval` nothing is an option."""
    letters = set()
    if not SKIPS_OPTIONS[word]:
        return letters, args
    while args and (text := word_text(args[0])) is not None and len(text) > 1 and text[0] == "-":
        args = args[1:]
        if text == "--":
            break
        for index, letter in enumerate(text[1:], 1):
            letters.add(letter)
            if letter in OPTION_ARGUMENTS.get(word, ""):
                if index == len(text) - 1:
                    args = args[1:]  # the next word is the option's argument; else the rest of the cluster is
                break
    return letters, args


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


def process_substitution(node):
    """Whether a node on a path is a process substitution (`<(…)`, `>(…)`), which Walk.visit puts on the stack of the
    statements inside it: bash runs them in a child whose status the parent never sees."""
    return isinstance(node, dict) and node.get("Type") == "ProcSubst"


def flagged_path(stack, negation=True):
    """The first flagged statement on the path from a statement (stack[0]) out to the top level (stack[-1]), as
    (flag, depth) into the stack, else None: a statement run in the background (`&`, so a failure ends only the job),
    negated (`!`, so the failure of what it ends is read as success) or running a `coproc` clause (shfmt 3.14.1 writes
    no Coprocess flag on the statement in bash mode: the clause is the flag), or a process substitution around the
    statement (a child whose status the parent never sees: the substitution is the flag). An `if` or `while`
    condition may negate its own statement (negation False passes over the `!` of stack[0] alone); a `!` around it is
    a flag."""
    for depth, stmt in enumerate(stack):
        if process_substitution(stmt):
            return PROCESS, depth
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
    if flag == PROCESS:
        return (
            f"the tested read runs in a process substitution (`<(…)` or `>(…)`) opened at line {line}, whose failure "
            "the parent never sees: the script goes on whatever the read's status"
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
    if flag == PROCESS:
        return f"runs in a process substitution opened at line {line}, whose failure the parent never sees"
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
    if flag == PROCESS:
        return (
            f"the producer runs in a process substitution opened at line {line}, whose failure the parent never sees, "
            "and a later test reads its stderr file before the listing has finished"
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
        # Rule f: the guarded names that are variables, every one the shadow part does not read as a command word
        # (`refuse`, `eval`, … run in command position throughout the levers and are written by an assignment
        # spelling alone), as the token pattern Walk.word scans a word's literal parts with.
        variables = [name for name in GUARDED_NAMES if name not in self.shadowed and IDENTIFIER.fullmatch(name)]
        self.variables = re.compile("(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, variables)) + ")(?![A-Za-z0-9_])")
        self.source = None  # the bytes of the file being walked (statement_text); None for the contract fixtures
        self.file = ""  # its name, which a row of ACCEPTED_WRITES or ACCEPTED_ARITHMETIC must list

    def run(self, tree, source=None, file=""):
        self.source = source
        self.file = file
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

    def visit(self, node, stack, siblings, arithmetic=False):
        """Depth first; stack is the statements holding node, innermost first, and the process substitutions among
        them (the path flagged_path reads), siblings the statement list it sits in, its index there and the stack
        around that list (the list a later `[[ ! -s file ]]` is searched in, and the path it shares with the
        producer), arithmetic whether node sits where bash evaluates arithmetic (ARITHMETIC_KINDS, the Index and Slice
        of an expansion or assignment, the operands of an arithmetic or name test; a statement inside, `$(( $(cmd)
        ))`, starts over). The two accepted positions are marked here, at the statement or clause that tests the
        read, before its substitution is visited; rule f's writes are asked of every assignment, loop variable,
        expansion and word met."""
        if isinstance(node, list):
            for item in node:
                self.visit(item, stack, siblings, arithmetic)
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
            arithmetic = False
            if siblings is not None and siblings[0] is self.top:
                self.top_index = siblings[1]
            self.statement(node, stack, siblings)
            self.tested_list(node, stack)
            if prologue_statement(node):
                self.prologues.append(stack)
        elif kind is None and "Name" in node:
            self.seen["Assign"] += 1
            self.assignment(node, stack[0])
        elif kind == "WordIter":
            self.loop(node, stack[0])
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
        elif kind == "ProcSubst":
            # A child whose status the parent never sees: the substitution joins the path of every statement inside
            # it (flagged_path), so a tested read or a producer there is a finding naming the substitution's line.
            self.seen["ProcSubst"] += 1
            stack = (node, *stack)
        elif kind == "ParamExp":
            self.expansion(node, stack[0])
        elif "Parts" in node and kind in (None, "Word"):
            # A word, untyped in a concrete position (an argument, a value, an element, a pattern, a redirect's
            # target, a heredoc body) and typed in an interface one (a test or arithmetic operand).
            self.seen["Word"] += 1
            self.word(node, stack[0], arithmetic)
        inner = (
            arithmetic
            or kind in ARITHMETIC_KINDS
            or (kind == "BinaryTest" and node.get("Op") in ARITHMETIC_TESTS)
            or (kind == "UnaryTest" and node.get("Op") in NAME_TESTS)
        )
        indexed = {id(node.get(field)) for field in ARITHMETIC_FIELDS} - {id(None)}
        for value in children(node):
            inside = inner or id(value) in indexed
            if isinstance(value, list) and any(isinstance(item, dict) and "Cmd" in item for item in value):
                for index, item in enumerate(value):
                    self.visit(item, stack, (value, index, stack), inside)
            else:
                self.visit(value, stack, siblings, inside)

    def statement(self, stmt, stack, siblings):
        """Rules b, d and f on one statement's own command. stack is the statement's path to the top level: a producer
        run in the background, negated, in a coprocess or in a process substitution on any statement of it
        (flagged_path) is a finding whatever follows it. Else a later `[[ ! -s file ]]` of the same statement list is
        judged on that list's path to the top level (siblings[2]), which it shares with the producer."""
        cmd = stmt.get("Cmd")
        if isinstance(cmd, dict) and cmd.get("Type") == "DeclClause":  # rule f: a declaration's words that assign nothing
            naked = [arg["Value"] for arg in cmd.get("Args") or [] if "Name" not in arg and "Value" in arg]
            self.attributes(stmt, cmd["Variant"]["Value"], naked)
        if not isinstance(cmd, dict) or cmd.get("Type") != "CallExpr":
            return
        words = leading_words(cmd)
        redirects = stmt.get("Redirs") or []
        if words[:1] == [READER] and any(redirect.get("Op") == "<" for redirect in redirects):
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
        An ALIASER (`alias`, `unalias`) is a finding in any form: no lever defines an alias, non-interactive bash
        expands none unless `shopt -s expand_aliases` is set, and an alias of a rebinder (`alias command=eval`) runs
        text this walk has not read. The EXPANDER (`shopt`) is a finding with EXPAND_ALIASES among its arguments, in
        any spelling, or with an argument that has no known text. For every other rebinder the leading options are
        read for their letters (leading_options, under SKIPS_OPTIONS: `source`, `.` and `eval` have none): under one
        of INERT_OPTIONS (`unset -v`, `command -v`) the command binds and runs nothing; left with no argument after
        them, and not only BARE_OPTIONS (`hash -r`), it has no argument to judge, a finding. Then a NAMER's or a
        FORWARDER's argument whose known text, before any `=`, is a word the rules read, the rebinders among them, is
        a finding naming what it shadows (`enable -n echo`, `enable -n command`, `hash -p /x/git git`, `unset -f
        refuse`, `command git`), and so is one with no known text, which may name any of them; a FORWARDER's command
        is judged again when its own first word is a rebinder (`command unset -f refuse`, `command alias x=y`), and a
        forwarded declaration's words are read by attributes (`builtin declare -i x`, `builtin export "$x"`). A
        RUNNER's argument is text or a file this walk has not read: `eval` with any argument, `source` or `.` with any
        but the one accepted shape (sourced_library; every argument word counts, `source -- lib.sh` and `source
        +lib.sh` among them), `trap` with an action that is not read whole (trap_action; the signal names after it
        are not text), `mapfile` or `readarray` with `-C`. No allow comment exempts it."""
        line = stmt["Pos"]["Line"]
        if word in ALIASERS:
            self.findings.add(
                (
                    line,
                    SHADOW,
                    f"`{word}` {ALIAS_ACTS[word]}, which no lever does; non-interactive bash expands none unless "
                    f"`{EXPANDER} -s {EXPAND_ALIASES}` is set, and an alias of a rebinder (`alias command=eval`) "
                    "runs text this walk has not read",
                )
            )
            return
        if word == EXPANDER:
            for arg in args:
                text = word_text(arg)
                if text is None:
                    self.findings.add(
                        (line, SHADOW, f"`{word}` has an argument with no known text, which may name `{EXPAND_ALIASES}`")
                    )
                elif text == EXPAND_ALIASES:
                    self.findings.add(
                        (
                            line,
                            SHADOW,
                            f"`{word}` names `{EXPAND_ALIASES}`, under which a script expands aliases and an alias "
                            "rebinds any word; no lever sets it",
                        )
                    )
            return
        letters, args = leading_options(word, args)
        if letters & set(INERT_OPTIONS.get(word, "")):
            return
        if not args and not (letters and letters <= set(BARE_OPTIONS.get(word, ""))):
            self.findings.add((line, SHADOW, f"`{word}` has no argument to judge"))
        names = ", ".join(f"`{name}`" for name in sorted(self.shadowed))
        unknown = f"`{word}` has an argument with no known text, which may name one of {names}"
        if word in RUNNERS:
            unread = f"which may define or rebind one of {names}"
            if word == "trap":
                for arg in args[:1]:
                    text = word_text(arg)
                    if text is None:
                        self.findings.add((line, SHADOW, f"`{word}` {RUNS[word]} with no known text, {unread}"))
                    elif not trap_action(text):  # one simple command is read whole; more is not
                        self.findings.add(
                            (line, SHADOW, f"`{word}` {RUNS[word]} this walk has not read whole, {unread}: `{text}`")
                        )
                return
            if word in SOURCES and sourced_library(args):
                return
            if word in SOURCES or word == "eval":  # every argument word, an option to bash or not, is the file or text
                texts = [word_text(arg) for arg in args]
                if None in texts:
                    self.findings.add((line, SHADOW, f"`{word}` {RUNS[word]} with no known text, {unread}"))
                elif texts:
                    text = " ".join(texts)
                    self.findings.add(
                        (line, SHADOW, f"`{word}` {RUNS[word]} this walk has not read, {unread}: `{text}`")
                    )
                return
            if CALLBACK_OPTION in letters:  # mapfile, readarray: the callback is an option's argument
                self.findings.add((line, SHADOW, f"`{word}` {RUNS[word]} this walk has not read, {unread}"))
            for arg in args:
                if word_text(arg) is None:
                    self.findings.add((line, SHADOW, unknown))
            return
        forwarded = word_text(args[0]) if word in FORWARDERS and args else None  # the command a FORWARDER runs
        for index, arg in enumerate(args):
            text = word_text(arg)
            if text is None:
                self.findings.add((line, SHADOW, unknown))
            elif index == 0 and forwarded in REBINDERS + DECLARERS:
                continue  # a rebinder or declarer run through the forwarder shadows nothing; its own words are judged
            elif word in FORWARDERS and text in DECLARERS:
                continue  # the declaration a chain of forwarders runs (`builtin command export …`); attributes reads it
            elif (name := text.split("=", 1)[0]) in self.shadowed:
                self.findings.add((line, SHADOW, f"`{word}` names `{name}` and shadows {self.shadowed[name]}"))
        if forwarded in REBINDERS:
            self.rebinding(stmt, forwarded, args[1:])
        elif forwarded in DECLARERS:  # rule f: the words of a forwarded declaration (`builtin declare -i x`)
            self.attributes(stmt, forwarded, args[1:])

    def write(self, stmt, name, how, line=None, accepted=None):
        """Rule f on a write to a guarded name (name; None when a word with no known text may write any of them), by
        how, in the statement stmt: a finding at line (the statement's first line when None) unless the statement's
        exact text, in this file, is a row of ACCEPTED_WRITES, or of the table accepted names as (its rows, its name):
        ACCEPTED_ARITHMETIC for an arithmetic operand. No allow comment exempts it."""
        rows, table = (ACCEPTED_WRITES, "ACCEPTED_WRITES") if accepted is None else accepted
        text = self.statement_text(stmt)
        for files, row, _ in rows:
            if self.file in files and text == row:
                return
        guarded = f"`{name}` ({GUARDED_NAMES[name]})" if name is not None else "any guarded name"
        self.findings.add(
            (
                stmt["Pos"]["Line"] if line is None else line,
                BINDING,
                f"a write to {guarded}: {how}, in {written_in(stmt)}; the statement is not an accepted "
                f"{'arithmetic statement' if accepted else 'write'} of the adopted levers and libraries ({table})",
            )
        )

    def statement_text(self, stmt):
        """The statement's source text, first byte to last (shfmt's offsets are bytes; a trailing comment is not
        part of it), or None when the walk has no source (the contract fixtures), where nothing is accepted."""
        if self.source is None:
            return None
        return self.source[stmt["Pos"]["Offset"] : stmt["End"]["Offset"]].decode("utf-8", "replace")

    def assignment(self, assign, stmt):
        """A write by an Assign node, wherever it sits (a plain assignment, a command's prefix, a declaration's
        argument: `PATH=/x/bin`, `IFS= read -r x`, `export PATH=/x/bin`, `declare -a GIT_ISOLATED_ENV=(x)`), with or
        without a value: shfmt writes no Value for `PATH=`, which writes the empty string, nor for the bare name of
        `export PATH` or `declare +x -a GIT_ISOLATED_ENV`, read as writes too."""
        name = assign["Name"]["Value"]
        if name not in GUARDED_NAMES:
            return
        valued = "Value" in assign or "Array" in assign
        how = "an assignment" if valued else "an assignment with no value, or the bare name"
        self.write(stmt, name, how, assign["Pos"]["Line"])

    def loop(self, loop, stmt):
        """A write by the variable of a `for` or `select` (shfmt's WordIter)."""
        name = loop["Name"]["Value"]
        if name in GUARDED_NAMES:
            self.write(stmt, name, "the variable of a `for` or `select`")

    def expansion(self, expansion, stmt):
        """A write by a parameter expansion that assigns its parameter: `${PATH=x}`, `${PATH:=x}` (ASSIGNING_OPS)."""
        if (expansion.get("Exp") or {}).get("Op") in ASSIGNING_OPS:
            name = expansion["Param"]["Value"]
            if name in GUARDED_NAMES:
                how = "an expansion that assigns its parameter (`${name=…}`, `${name:=…}`)"
                self.write(stmt, name, how, expansion["Pos"]["Line"])

    def word(self, word, stmt, arithmetic):
        """A write spelled by a word, in any position: its leading literal parts spell an assignment to a guarded
        name (WRITES: `export 'PATH=/x/bin:$PATH'`, `env PATH=/x/bin git ls-files`, `PATH=/x/bin:$PATH` as any
        command's word, `'GIT_ISOLATED_ENV=PATH=/x/bin'`, `alias fail=true`), or its literal parts hold the name of a
        guarded variable as a token (`read -r PATH`, `printf -v PATH x`, `unset PATH`, `mapfile PATH`, `local -n
        ref=PATH`, `(( PATH = 1 ))`, `let 'PATH = 1'`, `${a[PATH=1]}`, `coproc PATH {…}`, `bash -c 'cd /; PATH=x git'`,
        a message naming it). The name is matched in the concatenation of every literal part, quotes removed and in
        order, so a name spelled across quotes is found (`printf -v PA"TH" x`, `PA'TH'=1`, `'PA'TH=1`), and in each
        part alone, so nothing a part names is lost; an expansion among the parts contributes no text and hides none.
        Where bash evaluates arithmetic (arithmetic) an operand that is not inert (inert_operand: a name, which bash
        evaluates recursively, a `$`, an expansion) is a write to any guarded name unless the statement is a row of
        ACCEPTED_ARITHMETIC (measured: `y='PATH=1'` then `(( y, 1 ))` or `(( $y, 1 ))` sets PATH)."""
        leading, texts = literal_texts(word)
        line = (word.get("Pos") or stmt["Pos"])["Line"]
        writes = {}  # name -> how, one finding per name the word writes
        match = WRITES.match(leading)
        if match is not None:
            writes[match[1]] = f"a word spelling an assignment, `{match[0]}…`"
        for text in ("".join(texts), *texts):
            for found in self.variables.finditer(text):
                writes.setdefault(
                    found[1],
                    "a word spelling its name (an argument of `read`, `printf -v`, `unset` or `mapfile`, a nameref's "
                    "value, an arithmetic operand, text handed to another program, a message)",
                )
        for name, how in writes.items():
            self.write(stmt, name, how, line)
        if arithmetic and not inert_operand(word):
            self.write(
                stmt,
                None,
                "an operand where bash evaluates arithmetic that is not digits and operators alone (a name, which "
                "bash evaluates recursively, a parameter, an expansion)",
                line,
                (ACCEPTED_ARITHMETIC, "ACCEPTED_ARITHMETIC"),
            )

    def attributes(self, stmt, variant, words):
        """A declaration's words that assign nothing (a DeclClause's `Naked` arguments; every argument after a
        forwarded declarer, `builtin export …`): one with no known text may spell any write (`export "$binding"`,
        `export "${GIT_ISOLATED_ENV[@]}"`); an option cluster with a letter of ATTRIBUTE_OPTIONS for the variant makes
        a later assignment write elsewhere (`declare -i x`, `local -n r`)."""
        for word in words:
            text = word_text(word)
            line = (word.get("Pos") or stmt["Pos"])["Line"]
            if text is None:
                how = f"a word of `{variant}` with no known text, which may spell an assignment to any of them"
                self.write(stmt, None, how, line)
            elif len(text) > 1 and text[0] == "-" and set(text[1:]) & set(ATTRIBUTE_OPTIONS.get(variant, "")):
                how = (
                    f"the option `{text}` of `{variant}`, under which a later assignment evaluates its value as "
                    "arithmetic (`-i`) or writes the variable its value names (`-n`)"
                )
                self.write(stmt, None, how, line)

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
            if flag[0] == PROCESS:
                return f"the one at line {line} runs in a process substitution opened at line {at}, a child shell"
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
for kind in ("Stmt", "Assign", "Word", "CmdSubst", "Redirect", "ProcSubst"):
    if not visited[kind]:
        refuse(f"the walk visited no {kind} node in the contract fixtures, which hold some")

status = 0
for file in sys.argv[3:]:
    try:
        with open(file, "rb") as handle:
            source = handle.read()
        run = subprocess.run(["shfmt", "-ln", "bash", "--to-json"], input=source, capture_output=True, check=False)
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
        findings = walk.run(tree, source, file.rsplit("/", 1)[-1])
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
