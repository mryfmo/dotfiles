#!/usr/bin/env python3
"""Exercise scripts/ci/producer-status-check.sh, the lint over the grammar of command substitutions, the status-blind
producers, the prologue and `read` from a file (regime-cutover U112, plan P-21).

The fixtures reproduce the measured shapes of research 01 section 2.5 that a lint can see: a jq error read as "no
hooks" (shape 1, rule a), the bare `git ls-files` without its stderr capture (shape 3, rule b), `read x < unreadable`
(shape 4, rule d) and `local x=$(false)` (shape 5, rule a); the reader halves of shapes 2, 3 and 4 are in
tests/unit/test_read_lib.py. The lint needs shfmt on PATH (the pinned version, which the contract checks first). The
enforcement test runs it over the library and the five levers: that test, not a Makefile target, holds them to zero
findings. Rounds 2 to 5 of the audit each have a test naming their probe lines by line and rule: round 3 inverted the
two readings (a word has a known text only in three quoting forms; stderr is captured only by three operators), round
4 names the `||` branches that handle a tested read's status (exit, return, a top-level function ending in one, a
block or subshell ending so, `name=$?`) and the characters of a known bare literal, so a form the lint does not know
is a finding naming its shape, never decoded, round 5 reads the argument of that `exit` or `return` (none, a known
decimal from 1 to 255, or the bare `$?`), so `|| exit 0` no longer turns a failed read into success, round 6 reads
the tested statement's flags (`!`, `&`, `coproc`) and accepts the bare `exit` or `return` only as the whole branch or
as the only statement of its block or subshell, since after an earlier command `$?` is that command's, and round 7
builds every message that quotes a word of the tree by an f-string, so a word spelled `{y}` is reported, never read
as a format field that makes the walk raise and the lint refuse the file, and round 8 reads the flags of every
statement on the path from the tested read to the top level (`{ x=$(false) || exit 1; } &` ended only the job), of
the `||` branch and every statement inside it (`|| ! (exit 1)` read the refusal as success) and of the prologue
(`set -euo pipefail &` set the options of a child shell only), and round 9 stops analysing a refusal function's body:
a function called from a `||` branch, and a block or subshell branch, are accepted only when their statements match
one closed grammar (zero or more `echo`/`printf` commands sending fd 1 to fd 2, then exactly one `exit <1-255>`,
nothing else of any kind), and rule b's `[[ ! -s file ]]` must be an `if` condition, the left side of a `||` whose
branch is an accepted form, or a bare top-level statement after the prologue, on a path with no `!` or `&`, and round
10 reads the flags of the producer's own path too (`git ls-files > l 2> e &` let the next statement test `e` before
the listing had finished), so a producer run in the background, negated or in a coprocess is a finding whatever
follows it, and round 11 counts every function definition of the file at any depth: a `||` branch may call only a
name defined exactly once, at the top level, in the foreground and not negated, before the tested statement
(`refuse() { exit 2; }` redefined inside an `if`, and `true() { exit 2; } &`, had passed), and form (iv) is a plain
`=` of `$?` (`status+=$?` had passed), and round 12 closes the name: form (ii) accepts only `refuse` and `fail`, the
closed allowlist REFUSAL_NAMES (the builtin denylist of round 11 missed `fc`, so `fc() { exit 2; }; unset -f fc;
x=$(false) || fc -l` had passed), and every scan of the walk (the definitions, the allow comments, the body scan)
descends by the one traversal that skips a literal heredoc body (a `$(refuse() { return 0; })` in a `<< 'E'OF` body
had made the file's real `refuse` a duplicate), and round 13 reads a redirect's descriptor as a decimal (`02>&1` is
fd 2; `{fd}>` refuses the file) and the word of a `>&` or `<&` as a plain descriptor only when all digits or `-`
(`1>&2-`, `>&2-`, `<&2-`, `1>&file` and `1>&$fd` after `2> err` had passed), and adds rule f: a function, `alias`,
`enable` or `hash` naming a word the rules read as a builtin or a producer (`set() { :; }` had let a warned listing
pass a bare `[[ ! -s err ]]`) is a `shadow` finding at its line, and round 14 completes rule f over what bash offers
(the refusal names among the words; `unset`, `builtin`, `command`, `eval`, `source`, `.`, `trap`, `mapfile`,
`readarray` among the rebinders, each read as bash reads it, with the one `source` shape the levers use accepted; an
assignment to PATH, BASH_ALIASES or BASH_CMDS) and validates every redirect the walk meets (`true {fd}>err` had
passed off a producer), and round 15 reads a rebinder's options per word (SKIPS_OPTIONS: `source`, `.` and `eval` skip
none, so `source +payload.sh`, which the option loop had taken for an option with no file after it, is the file bash
reads; the other rebinders read `-` words only, a `+` word is an argument; a call left with no argument to judge is a
finding), and round 16 closes the protected set over the rebinders themselves (`alias command=eval` then `command
'refuse() { return 0; }'` had redefined the refusal function through a word rule f read as its own) and reads `alias`
and `unalias` in any form, and `shopt` with `expand_aliases` among its arguments, as findings: no lever defines an
alias, and non-interactive bash expands none unless that option is set, and round 17 reads a binding spelled as a word
(every argument word of `declare`, `typeset`, `readonly`, `export`, `local` or `env`, through any chain of `builtin` and
`command`: `export 'PATH=/tmp/x:$PATH'` and `builtin export PATH=/tmp/x` had passed while bash ran the spoofed git;
`export "${GIT_ISOLATED_ENV[@]}"` is the one accepted word with no known text, the array's assignments read as the
exported words) and puts a process substitution on the path of the statements inside it (`cat <(x=$(false) || exit 1)`
had passed while bash went on with exit 0), so a tested read or a producer there is a finding naming its line, and
round 18 replaces rule f's binding reading (rounds 14 to 17 each added one more way to write PATH or a trusted name,
and the round-17 audit found two more: `PATH=` with no Value, `export 'GIT_ISOLATED_ENV=PATH=/tmp/x'`) with an
allowlist: GUARDED_NAMES is one closed set of every name the lint trusts by its spelling and every variable bash reads,
a write is any Assign to one, a loop variable, an assigning expansion, a word in any position whose literal parts spell
an assignment to one or name a guarded variable, a declaration word with no known text, an attribute option, or an
unknown word where bash evaluates arithmetic, and ACCEPTED_WRITES holds the exact statement texts of the adopted set
(28 rows, two of them the pr-merge.sh disposition gate's, U119 round 5);
`test_every_name_the_lint_compares_against_is_a_guarded_name` keeps the set from drifting, and round 20 matches a
guarded name in the concatenation of a word's literal parts (`printf -v PA"TH" x` had passed) and reads every
arithmetic operand that is not digits and operators alone as a write (`y=$1; (( y, 1 ))` had passed: bash evaluates
a name there recursively), accepted only by the exact statement texts of ACCEPTED_ARITHMETIC (60 rows: eight of them
that gate's, five the pr-audit.sh round cap's, U120 round 4, and three the `filed:` disposition's of
pr-threads-check.sh, U124).
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_shfmt_json_contract import CAPTURES, captures, contract, hidden_tree, pinned_version  # noqa: E402

CHECK = ROOT / "scripts/ci/producer-status-check.sh"
TABLE = ROOT / "scripts/ci/status-blind-producers.tsv"
LIB = ROOT / "scripts/orchestrator/read-lib.sh"
GIT_LIB = ROOT / "scripts/orchestrator/git-isolated.sh"
LEVERS = tuple(
    ROOT / "scripts/orchestrator" / name
    for name in ("records-sync.sh", "pr-audit.sh", "pr-merge.sh", "pr-threads-check.sh", "pr-body-edit.sh")
)
ANSI_C_HEREDOC = ROOT / "tests/fixtures/shfmt-json/heredoc-ansi-c-delimiter"
PROLOGUE = "set -euo pipefail\n"
PRODUCERS = ("git ls-files", "git config -f", "git config --file", "find", "ls")
# The words rule f protects, as a finding lists them (sorted): the builtins the rules read, the declarations, the
# producers, the refusal names and the lint's own rebinders.
NAMES = (
    "`.`, `alias`, `builtin`, `command`, `declare`, `echo`, `enable`, `eval`, `exit`, `export`, `fail`, `find`, `git`, "
    "`hash`, `local`, `ls`, `mapfile`, `printf`, `read`, `readarray`, `readonly`, `refuse`, `return`, `set`, `shopt`, "
    "`source`, `trap`, `typeset`, `unalias`, `unset`"
)
# The identifier-shaped strings the walk compares a value against that are no name bash binds (round 18's drift test):
# each with its reason; the test asserts the list is exact.
NOT_NAMES = {
    "allow": "the second word of `# producer-status: allow <reason>` (rule e)",
    "pipefail": "the last word of the prologue `set -euo pipefail` (rule c), an option of `set`",
    "expand_aliases": "a `shopt` option rule f reads the word of, not a name bash binds",
    "Type": "the key of every typed node, in the `$?` pattern STATUS_PARAMETERS",
    "Col": "a position field without_positions drops, beside Offset and Line of the contract table",
}
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\.")
# How a finding ends on an `alias` or `unalias` call (round 16: any form), and what a rebinding of a rebinder shadows.
ALIAS = (
    "which no lever does; non-interactive bash expands none unless `shopt -s expand_aliases` is set, and an alias of "
    "a rebinder (`alias command=eval`) runs text this walk has not read"
)
REBINDER = "a rebinder of the lint's own rebinders, the words rule f reads a rebinding by (rule f)"
# The files a copy of the lint needs beside it: the contract module with its pin check and fixtures, and the pin.
COPIED = (
    "scripts/ci/producer-status-check.sh",
    "scripts/ci/shfmt_json_contract.py",
    "scripts/ci/pinned-tool-version.sh",
    "home/dot_mise/config.toml",
    *(f"tests/fixtures/shfmt-json/{fixture.name}" for fixture in CAPTURES),
)


def on_ci_runner() -> bool:
    """scripts/lib/ci-runner.sh decides, never the generic CI variable an agent shell exports."""
    probe = 'source "$1" && is_ci_runner'
    return (
        subprocess.run(["bash", "-c", probe, "_", str(ROOT / "scripts/lib/ci-runner.sh")], check=False).returncode == 0
    )


def findings(result: subprocess.CompletedProcess[str]) -> list[tuple[int, str]]:
    """(line, rule) per finding line of the lint's stdout."""
    out = []
    for line in result.stdout.splitlines():
        _, number, rule, _ = line.split(":", 3)
        out.append((int(number), rule.strip()))
    return out


class ProducerTableTest(unittest.TestCase):
    def test_the_table_names_the_measured_producers_with_their_behaviour_and_source(self):
        lines = TABLE.read_text().splitlines()
        self.assertEqual("words\tmeasured\tsource", lines[0])
        rows = [line.split("\t") for line in lines[1:]]
        self.assertEqual(list(PRODUCERS), [row[0] for row in rows])
        for words, measured, source in rows:
            with self.subTest(words):
                self.assertRegex(measured, r"\d{4}-\d{2}-\d{2}", "the measurement is dated")
                self.assertIn("01-git-shell.md section", source)


@unittest.skipUnless(shutil.which("shfmt") or on_ci_runner(), "needs shfmt off the CI runner (CI puts the pin on PATH)")
class ProducerStatusCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="producer-status-check-"))
        self.addCleanup(shutil.rmtree, self.temp)

    def script(self, name: str, body: str, prologue: str = PROLOGUE) -> Path:
        path = self.temp / name
        path.write_text("#!/usr/bin/env bash\n" + prologue + body)
        return path

    def run_check(self, *paths: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(CHECK), *map(str, paths)], capture_output=True, text=True, check=False, env=env
        )

    def assert_findings(
        self, body: str, expected: list[tuple[int, str]], prologue: str = PROLOGUE
    ) -> subprocess.CompletedProcess[str]:
        """The lint over one script holding body (after the shebang and the prologue, so body starts at line 3)
        reports exactly expected as (line, rule) pairs; an empty expected is exit 0 with nothing printed."""
        path = self.script("case.sh", body, prologue)
        result = self.run_check(path)
        self.assertEqual("", result.stderr)
        self.assertEqual(1 if expected else 0, result.returncode, result.stdout)
        self.assertEqual(sorted(expected), findings(result), body)
        for line in result.stdout.splitlines():
            self.assertTrue(line.startswith(f"{path}:"), line)
        return result

    def test_shape_1_a_jq_error_read_as_no_hooks_is_a_finding_under_rule_a(self) -> None:
        """U25 F1: `hooks=$(jq -r '.hooks' settings.json)` then `[[ -z ${hooks} ]]` read a jq failure as "no hooks".
        The plain assignment is a finding at its line; the same assignment tested by `||` is not."""
        body = "hooks=$(jq -r '.hooks' settings.json)\n[[ -z ${hooks} ]] || echo \"${hooks}\"\n"
        result = self.assert_findings(body, [(3, "substitution")])
        self.assertIn("loses its status", result.stdout)
        tested = "hooks=$(jq -r '.hooks' settings.json) || exit 1\n[[ -z ${hooks} ]] || echo \"${hooks}\"\n"
        self.assert_findings(tested, [])

    def test_the_two_accepted_positions_pass_and_every_other_position_is_a_finding(self) -> None:
        cases: list[tuple] = [  # (the lines, the rule(s) of the finding(s) or None, the finding's line within the case)
            ('fail() { echo "$1" >&2; exit 1; }', None),
            ("x=$(a) || fail", None),
            ('x="$(a)" || fail', None),
            ("x=`a` || fail", None),
            ("if ! x=$(a); then exit 1; fi", None),
            ("if x=$(a); then :; fi", None),
            ("while x=$(a); do break; done", None),
            ("until x=$(a); do break; done", None),
            ("if true; then :; elif x=$(a); then :; fi", None),
            ("x=$(a) || { echo no >&2; exit 1; }", None),
            ("x=$(a) || x=''", "substitution"),  # an empty value a later line handles is not a branch (allow it)
            ("x=$(a) || exit 2", None),
            ("f() { x=$(a) || return 1; }", None),
            ("g() { local y; y=$(a) || return 1; }", None),
            ("x=$(a) || true", "substitution"),
            ('x=$(a) || "true"', "substitution"),
            ("x=$(a) || 'true'", "substitution"),
            ("x=$(a) || tr\\ue", "substitution"),
            ('x=$(a) || "$(true)"', ("substitution", "substitution")),  # the inner one, and a right side not known
            ('x=$(a) || "${on_failure}"', "substitution"),  # a right side with no known text is not shown to read it
            ('x=$(a) || "$cmd"', "substitution"),
            ("x=$(a) || $'tr\\x75e'", "substitution"),  # ANSI-C: not decoded, not known
            ('x=$(a) || $"true"', "substitution"),  # a locale string: not known either
            ("x=$(a) || tr$'ue'", "substitution"),
            ("x=$(a) || 'fail'", None),
            ('x=$(a) || "fail" now', None),
            ("x=$(a) || :", "substitution"),
            ("x=$(a) || false", "substitution"),
            ("x=$(a) && echo ok", "substitution"),
            ("x=$(a)", "substitution"),
            ("x=$(a)/suffix || fail", "substitution"),
            ("x=prefix$(a) || fail", "substitution"),
            ("a=$(x) b=$(y) || exit 1", "substitution"),
            ("x=$(a) || y=$(b) || exit 1", ("substitution", "substitution")),  # the inner `||` branch is an assignment
            ('echo "$(a)"', "substitution"),
            ("echo `a`", "substitution"),
            ('cat > "$(a)"', "substitution"),
            ("[[ -n $(a) ]] || exit 1", "substitution"),
            (
                "n=$((1 + $(a))) || exit 1",
                ("binding", "substitution"),
            ),  # the output is evaluated as arithmetic (rule f)
            ("for i in $(a); do :; done", "substitution"),
            ("case $(a) in *) ;; esac", "substitution"),
            ('x=$(a "$(b)") || exit 1', "substitution"),
            ("if x=$(a); y=$(b); then :; fi", "substitution"),
            ("cat << EOF\n$(a)\nEOF", "substitution", 1),
            ("cat << 'EOF'\n$(a)\nEOF", None),
            ("cat << 'E'OF\n$(a)\nEOF", None),
        ]
        body_lines: list[str] = []
        expected: list[tuple[int, str]] = []
        for case in cases:
            text, rules = case[0], case[1]
            for rule in (rules,) if isinstance(rules, str) else rules or ():
                expected.append((3 + len(body_lines) + (case[2] if len(case) > 2 else 0), rule))
            body_lines.extend(text.split("\n"))
        result = self.assert_findings("\n".join(body_lines) + "\n", expected)
        self.assertIn("a command whose first word has no known text", result.stdout)

    def test_shape_5_a_declaration_assigned_from_a_substitution_is_a_finding(self) -> None:
        """`local x=$(false)` runs on under set -e, since local's own status wins (SC2155's case); the grammar
        refuses every declaration keyword, and the two-statement form passes."""
        for keyword in ("local", "export", "declare", "readonly", "declare -r", "local -r"):
            with self.subTest(keyword):
                body = f'f() {{\n    {keyword} x=$(false)\n    echo "${{x}}"\n}}\n'
                self.assert_findings(body, [(4, "substitution")])
        self.assert_findings("f() {\n    local x\n    x=$(false) || return 1\n}\n", [])

    def test_shape_3_a_bare_git_ls_files_without_its_stderr_capture_is_a_finding_under_rule_b(self) -> None:
        """`git ls-files` warns and exits 0 for a directory it cannot open (research 01 section 1.1). The bare call,
        `2> /dev/null` in any quoting, `2>&1`, a later redirect that moves stderr away from the captured file, a capture
        no later `[[ ! -s ]]` tests, a test of another file or of an earlier target, a test in another statement list
        or before the call are findings; the capture with its test, in any quoting, by `2>>` or `2>|`, the last of two
        fd-2 redirects, the other rows with theirs, and the call through read_listing are not."""
        capture = "git ls-files -z > list 2> err || exit 1\n"
        test = "[[ ! -s err ]] || exit 1\n"
        clean = {
            "the capture and its test": capture + test,
            "the test deeper in the list": capture + "echo listed\n" + test,
            "quoted in the redirect, bare in the test": (
                'd=$(pwd) || exit 1\ngit ls-files -z > list 2> "${d}/err" || exit 1\n[[ ! -s ${d}/err ]] || exit 1\n'
            ),
            "the test as an if condition": capture + "if [[ ! -s err ]]; then :; else exit 1; fi\n",
            "the bare test at top level after the prologue": capture + "[[ ! -s err ]]\n",
            "the test closed by a refusal function": (
                'fail() {\n    echo "$1" >&2\n    exit 1\n}\n' + capture + "[[ ! -s err ]] || fail 'stderr'\n"
            ),
            "through read_listing": "read_listing list err git ls-files -z || exit 1\n",
            "a glob character inside double quotes in both": (
                'git ls-files -z > list 2> "err*" || exit 1\n[[ ! -s "err*" ]] || exit 1\n'
            ),
            "a dot in the file name": "git ls-files -z > list 2> err.1 || exit 1\n[[ ! -s err.1 ]] || exit 1\n",
            "a glob in a leading word is no row": "git ls-fil* > l || exit 1\n",
            "inside a function with the test in its body": (
                "f() {\n    find . -type d > d 2> e || return 1\n    [[ ! -s e ]] || return 1\n}\n"
            ),
            "every row": (
                "find . -type d > d 2> e || exit 1\n[[ ! -s e ]] || exit 1\n"
                "ls > l 2> e2 || exit 1\n[[ ! -s e2 ]] || exit 1\n"
                "git config -f f --get k > v 2> e3 || exit 1\n[[ ! -s e3 ]] || exit 1\n"
                "git config --file f --get k > v 2> e4 || exit 1\n[[ ! -s e4 ]] || exit 1\n"
            ),
            "a producer the table does not name": (
                "jq -r .x f > o || exit 1\ngit status > s || exit 1\ngit config --get k > v || exit 1\n"
            ),
            "leading words that are not a row": "git -c core.fsmonitor=false ls-files > l || exit 1\n",
            "appended": "git ls-files -z > list 2>> err || exit 1\n" + test,
            "clobbered": "git ls-files -z > list 2>| err || exit 1\n" + test,
            "single-quoted in the redirect, double-quoted in the test": (
                "git ls-files -z > list 2> 'err' || exit 1\n[[ ! -s \"err\" ]] || exit 1\n"
            ),
            "the last fd-2 redirect decides": "git ls-files -z > list 2> a 2> b || exit 1\n[[ ! -s b ]] || exit 1\n",
            "stdout duplicated onto fd 2 leaves stderr's file alone": "git ls-files -z 2> err >&2 || exit 1\n" + test,
        }
        for name, body in clean.items():
            with self.subTest(clean=name):
                self.assert_findings(body, [])
        found = {
            "the bare call": ("git ls-files -z > list || exit 1\n", [(3, "producer")]),
            "stderr to /dev/null": ("git ls-files -z > list 2> /dev/null || exit 1\n" + test, [(3, "producer")]),
            "stderr merged into stdout": ("git ls-files -z > list 2>&1 || exit 1\n" + test, [(3, "producer")]),
            "no later test": (capture, [(3, "producer")]),
            "a test of another file": (capture + "[[ ! -s other ]] || exit 1\n", [(3, "producer")]),
            "a test that is not ! -s": (capture + "[[ -s err ]] && exit 1\n", [(3, "producer")]),
            "a test in another list": (capture + "f() { [[ ! -s err ]] || exit 1; }\n", [(3, "producer")]),
            "a test before the call": (test + capture, [(4, "producer")]),
            "the test chained with &&": (capture + "[[ ! -s err ]] && echo clean\n", [(3, "producer")]),
            "the test negated": (capture + "! [[ ! -s err ]] || exit 1\n", [(3, "producer")]),
            "the test in the background": (capture + "[[ ! -s err ]] &\n", [(3, "producer")]),
            "the test and its branch in the background": (capture + "[[ ! -s err ]] || exit 1 &\n", [(3, "producer")]),
            "a branch that does not end the script": (capture + "[[ ! -s err ]] || true\n", [(3, "producer")]),
            "a negated if condition": (capture + "if ! [[ ! -s err ]]; then exit 1; fi\n", [(3, "producer")]),
            "the bare test inside a function": (
                "f() {\n    find . -type d > d 2> e || return 1\n    [[ ! -s e ]]\n}\n",
                [(4, "producer")],
            ),
            "the bare test inside a block": ("{\n" + capture + "[[ ! -s err ]]\n}\n", [(4, "producer")]),
            "inside a substitution": ("x=$(git ls-files -z) || exit 1\n", [(3, "producer")]),
            "ls and find": ("ls > l || exit 1\nfind . -type f > f || exit 1\n", [(3, "producer"), (4, "producer")]),
            "git config -f and --file": (
                "git config -f f --get k || exit 1\ngit config --file f --get k || exit 1\n",
                [(3, "producer"), (4, "producer")],
            ),
            "a quoted producer word": ('"git" ls-files -z > list || exit 1\n', [(3, "producer")]),
            "a double-quoted /dev/null": (
                'git ls-files -z > list 2> "/dev/null" || exit 1\n[[ ! -s /dev/null ]] || exit 1\n',
                [(3, "producer")],
            ),
            "a single-quoted /dev/null": (
                "git ls-files -z > list 2> '/dev/null' || exit 1\n[[ ! -s '/dev/null' ]] || exit 1\n",
                [(3, "producer")],
            ),
            "stderr merged into stdout after the capture": (
                "git ls-files -z > list 2> err 2>&1 || exit 1\n" + test,
                [(3, "producer")],
            ),
            "stderr to the old stdout": ("git ls-files -z 2> err 2>&1 > out || exit 1\n" + test, [(3, "producer")]),
            "stderr appended elsewhere after the capture": (
                "git ls-files -z > list 2> err 2>> other || exit 1\n" + test,
                [(3, "producer")],
            ),
            "both streams to one file by &>": ("git ls-files -z 2> err &> out || exit 1\n" + test, [(3, "producer")]),
            "both streams to one file by >&": ("git ls-files -z 2> err >& out || exit 1\n" + test, [(3, "producer")]),
            "stderr closed after the capture": ("git ls-files -z 2> err 2>&- || exit 1\n" + test, [(3, "producer")]),
            "the test names the earlier target": (
                "git ls-files -z > list 2> a 2> b || exit 1\n[[ ! -s a ]] || exit 1\n",
                [(3, "producer")],
            ),
            "stderr closed by 2<&- after the capture": (
                "git ls-files > out 2> err 2<&- || exit 1\n" + test,
                [(3, "producer")],
            ),
            "fd 2 opened for reading after the capture": (
                "git ls-files 2> err 2< x || exit 1\n" + test,
                [(3, "producer")],
            ),
            "fd 2 opened read-write after the capture": (
                "git ls-files 2> err 2<> x || exit 1\n" + test,
                [(3, "producer")],
            ),
            "a here-string on fd 2 after the capture": (
                "git ls-files 2> err 2<<< '' || exit 1\n" + test,
                [(3, "producer")],
            ),
            "an ANSI-C /dev/null": (
                "git ls-files 2> $'/dev/n\\x75ll' || exit 1\n[[ ! -s $'/dev/n\\x75ll' ]] || exit 1\n",
                [(3, "producer")],
            ),
            "an ANSI-C target is no known file": ("git ls-files 2> $'err' || exit 1\n" + test, [(3, "producer")]),
            "an ANSI-C word in the test": (
                "git ls-files 2> err || exit 1\n[[ ! -s $'err' ]] || exit 1\n",
                [(3, "producer")],
            ),
            "a locale string in the test": (
                'git ls-files 2> err || exit 1\n[[ ! -s $"err" ]] || exit 1\n',
                [(3, "producer")],
            ),
            "a known text tested against an expansion": (
                "git ls-files 2> err || exit 1\n[[ ! -s ${err} ]] || exit 1\n",
                [(3, "producer")],
            ),
        }
        for name, (body, expected) in found.items():
            with self.subTest(finding=name):
                result = self.assert_findings(body, expected)
                self.assertIn("can fail with exit 0 or after printing", result.stdout)
        result = self.assert_findings("git ls-files -z > list || exit 1\n", [(3, "producer")])
        self.assertIn("`git ls-files`", result.stdout, "the finding names the row")
        # A bare test is accepted only after a top-level `set -euo pipefail`: without one, or before it, nothing reads
        # its failure (no substitution here, so rule c is silent and the producer finding stands alone).
        result = self.assert_findings(capture + "[[ ! -s err ]]\n", [(2, "producer")], prologue="")
        self.assertIn("no `set -euo pipefail` at the top level before it", result.stdout)
        self.assert_findings(capture + "[[ ! -s err ]]\nset -euo pipefail\n", [(2, "producer")], prologue="")

    def test_the_round_2_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The three lines of the c7be7ede audit and their neighbours, which that head read as clean: a trivial right
        side in quotes (rule a), a later redirect that moves stderr off the tested file, and /dev/null in quotes
        (rule b). `|| "$(true)"` is two findings on one line since round 3: the inner substitution, and the left side,
        whose right side has no known command word."""
        body = (
            'x=$(false) || "true"\n'
            "x=$(a) || 'true'\n"
            'x=$(a) || "$(true)"\n'
            "git ls-files > list 2> err 2>&1 || exit 1\n"
            "[[ ! -s err ]] || exit 1\n"
            'git ls-files > list 2> "/dev/null" || exit 1\n'
            "[[ ! -s /dev/null ]] || exit 1\n"
            "git ls-files > list 2> err 2>> other || exit 1\n"
            "[[ ! -s err ]] || exit 1\n"
            "git ls-files > list 2> err &> out || exit 1\n"
            "[[ ! -s err ]] || exit 1\n"
            "git ls-files 2> err 2>&1 > out || exit 1\n"
            "[[ ! -s err ]] || exit 1\n"
            "git ls-files > list 2> '/dev/null' || exit 1\n"
            "[[ ! -s '/dev/null' ]] || exit 1\n"
        )
        expected = [(3, "substitution"), (4, "substitution"), (5, "substitution"), (5, "substitution")]
        expected += [(line, "producer") for line in (6, 8, 10, 12, 14, 16)]
        self.assert_findings(body, expected)

    def test_the_round_3_probes_are_findings_named_by_line_and_rule(self) -> None:
        """The three lines of the 2fc472c6 audit and the next members of both lists, which that head read as clean:
        `2<&-` after the capture (the redirect operators that touch fd 2 were an enumeration), an ANSI-C `true` on the
        right of `||` and an ANSI-C /dev/null (the quoting forms of a literal were one too). Round 3 reads both as
        allowlists, so `2<`, `2<>`, `2<<<`, an ANSI-C word in the test and an expansion on the right are findings
        without being named; the expansion capture compared by parts and the block on the right stay clean."""
        body = (
            "git ls-files > out 2> err 2<&- || exit 1\n"
            "[[ ! -s err ]] || exit 1\n"
            "x=$(false) || $'tr\\x75e'\n"
            "git ls-files 2> $'/dev/n\\x75ll' || exit 1\n"
            "[[ ! -s $'/dev/n\\x75ll' ]] || exit 1\n"
            "git ls-files 2> err 2< x || exit 1\n"
            "[[ ! -s err ]] || exit 1\n"
            "git ls-files 2> err 2<> x || exit 1\n"
            "[[ ! -s err ]] || exit 1\n"
            "git ls-files 2> err 2<<< '' || exit 1\n"
            "[[ ! -s err ]] || exit 1\n"
            "git ls-files 2> err || exit 1\n"
            "[[ ! -s $'err' ]] || exit 1\n"
            'x=$(a) || "$cmd"\n'
            "d=$(pwd) || exit 1\n"
            'git ls-files 2> "${d}/err" || exit 1\n'
            "[[ ! -s ${d}/err ]] || exit 1\n"
            "x=$(a) || { echo no >&2; exit 1; }\n"
        )
        expected = [(5, "substitution"), (16, "substitution")]
        expected += [(line, "producer") for line in (3, 6, 8, 10, 12, 14)]
        result = self.assert_findings(body, expected)
        self.assertIn("a command whose first word has no known text", result.stdout)

    def test_the_round_4_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The two lines of the 03a4d5c6 audit and the next members of both lists, which that head read as clean: a
        pipeline on the right of `||` (the branch was judged by a list of refused words) and a bare glob as the
        captured file (a bare literal had no character rule). Round 4 names the branches that handle the status and
        the characters of a known bare literal: every other branch is a finding naming its shape; a glob, a bracket, a
        brace or a tilde in a bare literal is no file name, while the same characters in double quotes are."""
        body = (
            'refuse() {\n    echo "$1" >&2\n    exit 2\n}\n'  # lines 3 to 6
            'fail() {\n    status=$?\n    echo "failed ${status}"\n}\n'  # 7 to 10
            "x=$(false) || true | cat\n"  # 11
            "x=$(a) || { true; }\n"  # 12
            "x=$(a) || (true)\n"  # 13
            "x=$(a) || echo failed\n"  # 14
            "x=$(a) || other_var=1\n"  # 15
            "x=$(a) || status=$?\n"  # 16
            "x=$(a) || { echo x >&2; exit 2; }\n"  # 17
            "x=$(a) || refuse 'x'\n"  # 18
            "x=$(a) || undefined_refuse 'x'\n"  # 19
            "x=$(a) || fail\n"  # 20
            "git ls-files 2> err* || exit 1\n[[ ! -s err* ]] || exit 1\n"  # 21, 22
            "git ls-files 2> err? || exit 1\n[[ ! -s err? ]] || exit 1\n"  # 23, 24
            "git ls-files 2> err[1] || exit 1\n[[ ! -s err[1] ]] || exit 1\n"  # 25, 26
            "git ls-files 2> e{rr,xx} || exit 1\n[[ ! -s e{rr,xx} ]] || exit 1\n"  # 27, 28
            "git ls-files 2> ~/err || exit 1\n[[ ! -s ~/err ]] || exit 1\n"  # 29, 30
            'git ls-files 2> "err*" || exit 1\n[[ ! -s "err*" ]] || exit 1\n'  # 31, 32
            "git ls-files 2> err.1 || exit 1\n[[ ! -s err.1 ]] || exit 1\n"  # 33, 34
        )
        expected = [(line, "substitution") for line in (11, 12, 13, 14, 15, 19, 20)]
        expected += [(line, "producer") for line in (21, 23, 25, 27, 29)]
        result = self.assert_findings(body, expected)
        for line, shape in (
            (11, "a pipeline"),
            (
                12,
                "a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 12 with the command `true`",
            ),
            (
                13,
                "a subshell that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 13 with the command `true`",
            ),
            (14, "the command `echo`"),
            (15, "an assignment of something other than `$?`"),
            (19, "the command `undefined_refuse`"),
            (
                20,
                "a call of `fail`, whose body breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 8 with an assignment",
            ),
        ):
            self.assertIn(f":{line}: substitution: the `||` branch is {shape} and does not end the read", result.stdout)

    def test_the_round_5_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The residual of the c95367a7 body, which that head read as clean: `exit` and `return` were accepted without
        their argument, so `|| exit 0`, `|| (exit 0)`, a block ending in `exit 0`, a function ending in `exit 0` and
        `|| return 0` turned the failed read into success. Round 5 reads the one argument: none, a known decimal from
        1 to 255 or the bare `$?` end the read; a zero, a 256, an argument with no known text (`"$code"`, `$(cmd)`,
        `"$?"`), a non-decimal or two arguments are findings naming the shape."""
        body = (
            "refuse() {\n    exit 0\n}\n"  # lines 3 to 5
            "x=$(false) || exit 0\n"  # 6
            "x=$(a) || (exit 0)\n"  # 7
            "x=$(a) || { echo x >&2; exit 0; }\n"  # 8
            "x=$(a) || refuse\n"  # 9
            "f() {\n    x=$(a) || return 0\n}\n"  # 10 to 12
            'x=$(a) || exit "$code"\n'  # 13
            "x=$(a) || exit $?\n"  # 14
            "x=$(a) || exit 2\n"  # 15
            "x=$(a) || exit\n"  # 16
            "g() {\n    x=$(a) || return 1\n}\n"  # 17 to 19
            "x=$(a) || exit 1 2\n"  # 20
            "x=$(a) || exit $(cmd)\n"  # 21
            "x=$(a) || exit 256\n"  # 22
            "x=$(a) || exit abc\n"  # 23
            "x=$(a) || exit ${?}\n"  # 24
            "x=$(a) || exit '255'\n"  # 25
            'x=$(a) || exit "$?"\n'  # 26
            "x=$(a) || exit -1\n"  # 27
            "h() {\n    x=$(a) || return $?\n}\n"  # 28 to 30
        )
        expected = [(line, "substitution") for line in (6, 7, 8, 9, 11, 13, 20, 21, 21, 22, 23, 26, 27)]
        result = self.assert_findings(body, expected)
        for line, shape in (
            (6, "`exit 0`, which turns the failed read into success"),
            (
                7,
                "a subshell that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 7 with `exit 0`, which turns the failed read into success",
            ),
            (
                8,
                "a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 8 with `exit 0`, which turns the failed read into success",
            ),
            (
                9,
                "a call of `refuse`, whose body breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 4 with `exit 0`, which turns the failed read into success",
            ),
            (11, "`return 0`, which turns the failed read into success"),
            (13, "an `exit` whose argument has no known text"),
            (20, "an `exit` with 2 arguments"),
            (21, "an `exit` whose argument has no known text"),
            (22, "`exit 256`, which turns the failed read into success"),
            (23, "`exit abc`, whose argument is not a decimal from 1 to 255"),
            (26, "an `exit` whose argument has no known text"),
            (27, "`exit -1`, whose argument is not a decimal from 1 to 255"),
        ):
            self.assertIn(f":{line}: substitution: the `||` branch is {shape} and does not end the read", result.stdout)

    def test_the_round_6_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The two lines of the aa32e0b3 audit and the next members of both lists, which that head read as clean: a
        tested read that is negated or runs in the background (the statement's flags were not read, so `! x=$(false)
        || exit 1` read the failure as success and `x=$(false) || exit 1 &` ended only the job), and a bare `exit` or
        `return` after an earlier command or anywhere in a function body (`$?` is by then that command's, so
        `refuse() { echo failed >&2; return; }` returned 0 and the script went on with an empty x). Round 6 reads the
        flags of the tested statement and of the branch and the `coproc` clause, and accepted the bare form only as
        the whole branch or as the only statement of its block or subshell; since round 9 a block, a subshell or a
        function body is matched against the refusal grammar instead, so `(exit)`, `{ exit; }` and `{ y=1; exit $?; }`
        (lines 20, 21, 29) are findings too, and each finding names the first statement outside the grammar."""
        body = (
            "! x=$(false) || exit 1\n"  # 3
            "x=$(false) || exit 1 &\n"  # 4
            "coproc x=$(true)\n"  # 5: shfmt reads `x=$(true)` as the coprocess's command word, so the plain finding
            "coproc { x=$(true); } || exit 1\n"  # 6
            "refuse() {\n    echo failed >&2\n    return\n}\n"  # 7 to 10
            "x=$(false) || refuse\n"  # 11
            "x=$(a) || { echo x >&2; exit; }\n"  # 12
            "x=$(a) || { echo x >&2; exit 2; }\n"  # 13
            "x=$(a) || exit\n"  # 14
            'fail() {\n    echo "$1" >&2\n    exit 2\n}\n'  # 15 to 18
            "x=$(a) || fail y\n"  # 19
            "x=$(a) || (exit)\n"  # 20
            "x=$(a) || { exit; }\n"  # 21
            "bare() {\n    exit\n}\n"  # 22 to 24
            "x=$(a) || bare\n"  # 25
            "x=$(a) || exit 2 &\n"  # 26
            "if x=$(a) & then :; fi\n"  # 27
            "x=$(a) || { y=1; exit; }\n"  # 28
            "x=$(a) || { y=1; exit $?; }\n"  # 29
            "x=$(a) || { echo x; refuse; }\n"  # 30
            "x=$(a) || { exit 2 & }\n"  # 31
            "if ! x=$(a); then exit 1; fi\n"  # 32: a negated condition is accepted, as before
        )
        expected = [(line, "substitution") for line in (3, 4, 5, 6, 11, 12, 20, 21, 25, 26, 27, 28, 29, 30, 31)]
        result = self.assert_findings(body, expected)
        background = "the tested read runs in the background (`&`), so its failure stops nothing: the test sees the job"
        bare = "a bare `exit`, whose status is the statement's before it"
        for line, message in (
            (3, "the tested read is negated (`!`), so its failure is read as success and the `||` branch does not run"),
            (4, background),
            (5, "a command substitution here loses its status"),
            (6, "the tested read runs as a coprocess (`coproc`), whose status is read before the read ends"),
            (
                11,
                "the `||` branch is a call of `refuse`, whose body breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 9 with the command `return`",
            ),
            (
                12,
                f"the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 12 with {bare}",
            ),
            (
                20,
                f"the `||` branch is a subshell that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 20 with {bare}",
            ),
            (
                21,
                f"the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 21 with {bare}",
            ),
            (
                25,
                "the `||` branch is a call of `bare`, defined at line 22, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (26, background),
            (27, background),
            (
                28,
                "the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 28 with an assignment",
            ),
            (
                29,
                "the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 29 with an assignment",
            ),
            (
                30,
                "the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 30 with an `echo` that does not send fd 1 to fd 2 (`>&2`)",
            ),
            (
                31,
                "the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 31 with a command run in the "
                "background (`&`), which lets the script go on",
            ),
        ):
            self.assertIn(f":{line}: substitution: {message}", result.stdout)

    def test_the_round_7_probes_with_braces_in_a_word_are_findings_naming_the_word(self) -> None:
        """The residual of the 45e66603 report: the message naming a bare `exit` or `return` after another command was
        built by splicing that command's word into a template and then calling `str.format` on it, so a command
        spelled `'{y}'` (a known text holding braces) raised KeyError inside the walk and the lint refused the file
        (exit 2, `cannot walk the syntax tree … KeyError('y')`) instead of reporting the finding. Every message that
        quotes a word of the tree is now an f-string or a join: the word is quoted as it is, exit 1, nothing on
        stderr. The branch and producer messages, built by f-strings before, are pinned to the same reading."""
        for body, line, rule, named in (
            (
                "x=$(false) || { '{y}'; exit; }\n",
                3,
                "substitution",
                "the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 3 with the command `{y}` and "
                "does not end the read",
            ),
            (
                "refuse() {\n    '{y}'\n    return\n}\n"  # 3 to 6
                "x=$(false) || refuse\n",  # 7
                7,
                "substitution",
                "the `||` branch is a call of `refuse`, whose body breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 4 with the command "
                "`{y}` and does not end the read",
            ),
            (
                "x=$(false) || '{a}' 'b}'\n",
                3,
                "substitution",
                "the `||` branch is the command `{a}` and does not end the read",
            ),
            ("git ls-files 2> '{err}'\n", 3, "producer", "`git ls-files` can fail with exit 0 or after printing"),
        ):
            with self.subTest(body=body):
                result = self.assert_findings(body, [(line, rule)])
                self.assertIn(f":{line}: {rule}: {named}", result.stdout)

    def test_the_round_8_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The three lines of the e2a87fef audit and the next members of each list, which that head read as clean:
        only the tested statement's own flags were read, so `{ x=$(false) || exit 1; } &` ended only the background
        job while the parent went on; branch_shape ignored `Negated`, so `|| ! (exit 1)` turned the refusal into
        success; and the prologue check accepted `set -euo pipefail &`, which sets the options of a child shell. Round 8
        reads the flags of every statement on the path from the tested read to the top level (flagged_path), of the
        `||` branch and every statement inside its block or subshell, and of the prologue; each finding names the
        flagged statement's line. A function body is not the top level: `f() { x=$(false) || return 1; }` is judged
        by its own path and accepted, and the `&` of its call `f &` is outside that path (a documented accept: the
        read's failure returns from `f`, whatever the caller does with the job)."""
        body = (
            "{ x=$(false) || exit 1; } &\n"  # 3: the auditor's first probe
            "x=$(false) || ! (exit 1)\n"  # 4: the second
            "( x=$(false) || exit 1 ) &\n"  # 5
            "f() { x=$(false) || return 1; }\n"  # 6: accepted, see the docstring
            "f &\n"  # 7
            "x=$(a) || { ! exit 1; }\n"  # 8
            "x=$(a) || ( ! exit 1 )\n"  # 9
            "x=$(a) || ! exit 1\n"  # 10
            "! { x=$(a) || exit 1; }\n"  # 11
            "! ( x=$(a) || exit 1 )\n"  # 12
            "{\n    x=$(a) || exit 1\n} &\n"  # 13 to 15: the finding at 14 names the job started at 13
            "coproc { if x=$(a); then :; fi; }\n"  # 16
            "x=$(a) || { echo x & exit 1; }\n"  # 17
            "if x=$(a); then :; fi &\n"  # 18
            "while x=$(a); do break; done &\n"  # 19
            "g() { ( x=$(a) || exit 1 ) & }\n"  # 20: the subshell inside the body is on the read's path
            "{ x=$(a) || exit 1; }\n"  # 21: a foreground block, accepted
            "( x=$(a) || exit 1 )\n"  # 22: a foreground subshell, accepted
            "x=$(a) || { exit 1; } &\n"  # 23
        )
        expected = [(line, "substitution") for line in (3, 4, 5, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 23)]
        result = self.assert_findings(body, expected)
        background = "the tested read runs in the background (`&`), so its failure stops nothing: the test sees the job"
        negated_branch = "a negated command (`!`), whose failure status is read as success"
        for line, message in (
            (3, f"{background} started at line 3"),
            (4, f"the `||` branch is {negated_branch} and does not end the read"),
            (5, f"{background} started at line 5"),
            (
                8,
                f"the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 8 with {negated_branch}",
            ),
            (
                9,
                f"the `||` branch is a subshell that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 9 with {negated_branch}",
            ),
            (10, f"the `||` branch is {negated_branch}"),
            (11, "the tested read sits in a statement negated (`!`) at line 11, so a failure that ends that statement"),
            (12, "the tested read sits in a statement negated (`!`) at line 12"),
            (14, f"{background} started at line 13"),
            (
                16,
                "the tested read runs as a coprocess (`coproc`), whose status is read before the read ends: the "
                "`coproc` is at line 16",
            ),
            (
                17,
                "the `||` branch is a block that breaks the refusal grammar (`echo`/`printf` to stderr, then one `exit <1-255>`) at line 17 with a command run in the "
                "background (`&`), which lets the script go on",
            ),
            (18, f"{background} started at line 18"),
            (19, f"{background} started at line 19"),
            (20, f"{background} started at line 20"),
            (23, f"{background} started at line 23"),
        ):
            self.assertIn(f":{line}: substitution: {message}", result.stdout)
        # The prologue: the auditor's third probe and the other ways `set -euo pipefail` is not the script's own.
        read = "x=$(a) || exit 1\n"
        for name, prologue, why in (
            ("in the background", "set -euo pipefail &\n", "runs in a background job started at line 2 (`&`)"),
            ("in a subshell", "( set -euo pipefail )\n", "runs inside a subshell at line 2, not at the top level"),
            (
                "in a block in the background",
                "{ set -euo pipefail; } &\n",
                "runs in a background job started at line 2",
            ),
            ("negated", "! set -euo pipefail\n", "is negated (`!`) at line 2"),
            ("in a block", "{ set -euo pipefail; }\n", "runs inside a block at line 2, not at the top level"),
            ("in a function", "f() { set -euo pipefail; }\n", "runs inside a function definition at line 2"),
            ("after the read", "", "the one at line 3 comes after it"),
            ("absent", "", "the file holds none"),
        ):
            with self.subTest(name):
                tail = "set -euo pipefail\n" if name == "after the read" else ""
                result = self.assert_findings(read + tail, [(1, "prologue")], prologue=prologue)
                if prologue:
                    why = f"substitution (line 3): the one at line 2 {why}"
                self.assertIn("`set -euo pipefail` must run at top level", result.stdout)
                self.assertIn(why, result.stdout)

    def test_the_round_9_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The three P2 of the 10fbb408 audit and the next members of each list, which that head read as clean: a
        refusal function was judged by analysing its body (its last statement, that statement's argument, what `$?`
        held), so `f() { echo failed >&2; return $?; }` returned the echo's 0, `f() { return 0; exit 1; }` was accepted
        on an unreachable `exit`, and rule b read `[[ ! -s err ]]` without its flags or its shape, so `! [[ ! -s err ]]
        || exit 1` and `[[ ! -s err ]] &` closed a producer whose warning reached the next statement. Round 9 stops
        analysing: a function called from a `||` branch, and a block or subshell branch, are accepted only when their
        statements match one grammar (zero or more `echo`/`printf` commands with a redirect sending fd 1 to fd 2, then
        exactly one `exit` whose argument is a known decimal from 1 to 255, nothing else of any kind), each finding
        naming the first statement outside it by line; and rule b's test must be an `if` condition, the left side of
        a `||` whose branch is an accepted form, or a bare top-level statement after the prologue, with no `!` or `&`
        on its path, each finding naming the test's line and why. Round 12 closed form (ii) to the names `refuse` and
        `fail`: the two accepted functions carry those names, every other call here is a finding naming the name, and
        the round-12 test pins the body-break messages of the function path."""
        body = (
            "f1() {\n    echo failed >&2\n    return $?\n}\n"  # lines 3 to 6: the auditor's first probe
            "x=$(false) || f1\n"  # 7
            "f2() {\n    return 0\n    exit 1\n}\n"  # 8 to 11: the second
            "x=$(false) || f2\n"  # 12
            "git ls-files > list 2> err || exit 1\n"  # 13: the third
            "! [[ ! -s err ]] || exit 1\n"  # 14
            "git ls-files > list 2> err2 || exit 1\n"  # 15: and its twin
            "[[ ! -s err2 ]] &\n"  # 16
            "f3() {\n    echo x >&2\n    exit 2\n    exit 3\n}\n"  # 17 to 21
            "x=$(false) || f3\n"  # 22
            "f4() {\n    echo x\n    exit 2\n}\n"  # 23 to 26: no stderr redirect
            "x=$(false) || f4\n"  # 27
            'f5() {\n    local m=$1\n    echo "$m" >&2\n    exit 2\n}\n'  # 28 to 32
            "x=$(false) || f5 m\n"  # 33
            "fail() {\n    printf '%s\\n' \"$@\" >&2\n    exit 2\n}\n"  # 34 to 37: accepted
            "x=$(false) || fail a b\n"  # 38
            'refuse() {\n    echo "$1" 1>&2\n    exit 255\n}\n'  # 39 to 42: accepted
            "x=$(false) || refuse y\n"  # 43
            "git ls-files > list 2> err3 || exit 1\n"  # 44: accepted, the test as an `if` condition
            "if [[ ! -s err3 ]]; then\n    :\nelse\n    exit 1\nfi\n"  # 45 to 49
            "git ls-files > list 2> err4 || exit 1\n"  # 50: accepted, a bare test at top level after the prologue
            "[[ ! -s err4 ]]\n"  # 51
            "git ls-files > list 2> err5 || exit 1\n"  # 52
            "[[ ! -s err5 ]] && echo clean\n"  # 53
            "git ls-files > list 2> err6 || exit 1\n"  # 54
            "[[ ! -s err6 ]] || true\n"  # 55
            "g() {\n    git ls-files > list 2> err7 || return 1\n    [[ ! -s err7 ]]\n}\n"  # 56 to 59
            "git ls-files > list 2> err8 || exit 1\n"  # 60
            "[[ ! -s err8 ]] || exit 1 &\n"  # 61
            "git ls-files > list 2> err9 || exit 1\n"  # 62
            "if ! [[ ! -s err9 ]]; then\n    exit 1\nfi\n"  # 63 to 65: the negated condition at 63
            "git ls-files > list 2> err10 || exit 1\n"  # 66: accepted, the test closed by a refusal function
            "[[ ! -s err10 ]] || refuse stderr\n"  # 67
            "f8() {\n    echo x >&2\n    exit $?\n}\n"  # 68 to 71
            "x=$(false) || f8\n"  # 72
            'f9() {\n    echo x >&2\n    rm -rf "$dir"\n    exit 1\n}\n'  # 73 to 77: a cleanup is not a refusal
            "x=$(false) || f9\n"  # 78
            'f10() {\n    echo "$(date) x" >&2\n    exit 1\n}\n'  # 79 to 82: two findings, the inner one and the call
            "x=$(false) || f10\n"  # 83
            "f11() {\n    echo x >&2\n    exit 1 &\n}\n"  # 84 to 87
            "x=$(false) || f11\n"  # 88
            "f12() {\n    echo x >&2\n    ! exit 1\n}\n"  # 89 to 92
            "x=$(false) || f12\n"  # 93
        )
        expected = [(line, "substitution") for line in (7, 12, 22, 27, 33, 72, 78, 80, 83, 88, 93)]
        expected += [(line, "producer") for line in (13, 15, 52, 54, 57, 60, 62)]
        result = self.assert_findings(body, expected)
        for line, message in (
            (
                7,
                "the `||` branch is a call of `f1`, defined at line 3, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                12,
                "the `||` branch is a call of `f2`, defined at line 8, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                22,
                "the `||` branch is a call of `f3`, defined at line 17, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                27,
                "the `||` branch is a call of `f4`, defined at line 23, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                33,
                "the `||` branch is a call of `f5`, defined at line 28, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                72,
                "the `||` branch is a call of `f8`, defined at line 68, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                78,
                "the `||` branch is a call of `f9`, defined at line 73, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (80, "a command substitution here loses its status"),
            (
                83,
                "the `||` branch is a call of `f10`, defined at line 79, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                88,
                "the `||` branch is a call of `f11`, defined at line 84, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                93,
                "the `||` branch is a call of `f12`, defined at line 89, a name that is not a refusal name (`refuse`, `fail`)",
            ),
        ):
            self.assertIn(f":{line}: substitution: {message}", result.stdout)
        tail = "statement of the same list, as an `if` condition or the left side of a `||` that ends the script, or run it through read_listing of read-lib.sh; the `[[ ! -s ]]` test at line"
        for line, message in (
            (13, f"{tail} 14 is negated (`!`), so a non-empty file is read as clean"),
            (15, f"{tail} 16 runs in the background (`&`, the job started at line 16), so its failure stops nothing"),
            (
                52,
                f"{tail} 53 sits in an `&&` list as neither the left side of a `||` nor the last statement of an `if` condition",
            ),
            (
                54,
                f"{tail} 55 is the left side of a `||` whose branch is the command `true` and does not end the script",
            ),
            (
                57,
                f"{tail} 58 is a bare statement inside a function definition at line 56, not at the top level where `set -e` ends the script on its failure",
            ),
            (60, f"{tail} 61 runs in the background (`&`, the job started at line 61), so its failure stops nothing"),
            (62, f"{tail} 63 is negated (`!`), so a non-empty file is read as clean"),
        ):
            self.assertIn(f":{line}: producer: `git ls-files` can fail", result.stdout)
            self.assertIn(
                f":{line}: producer: `git ls-files` can fail with exit 0 or after printing (status-blind-producers.tsv); send its stderr with `2>`, `2>>` or `2>|` to a file (the last redirect that touches fd 2 decides; any other operator there, and /dev/null, leave it uncaptured) and test `[[ ! -s <that file> ]]` in a later {message}",
                result.stdout,
            )
        # The grammar is a match, not an analysis: a body the lint would otherwise have to reason about (a cleanup
        # before the exit) is a finding, and the lever's answer is a trap or an allow comment naming the cleanup line.
        allowed = (
            'f9() {\n    echo x >&2\n    rm -rf "$dir"\n    exit 1\n}\n'
            "x=$(false) || f9 # producer-status: allow f9 removes the run directory at line 5 before it exits\n"
        )
        self.assert_findings(allowed, [])

    def test_the_round_10_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The residual of the f87a0a79 report, which that head read as clean: rule b read the flags of the test's
        path but not of the producer's own, so `git ls-files > list 2> err &` with `[[ ! -s err ]] || exit 1` after it
        passed while the test ran before the listing had finished, `! git ls-files > list 2> err` read the producer's
        failure as success, and a producer inside a background block, a coprocess or a negated block was a finding
        that named the test or nothing. Round 10 runs flagged_path over the producer's own path: a producer run in the
        background, negated or in a coprocess on any statement of that path is a finding naming the flag and its line
        whatever follows it; the same statements with no flag are accepted."""
        body = (
            "git ls-files > list 2> err &\n"  # 3: the residual, the test runs before the listing has finished
            "[[ ! -s err ]] || exit 1\n"  # 4
            "! git ls-files > list 2> err2\n"  # 5: the negated producer, its failure read as success
            "[[ ! -s err2 ]] || exit 1\n"  # 6
            "{\n    git ls-files > list 2> err3\n} &\n"  # 7 to 9: the block in the background, the flag at 7
            "[[ ! -s err3 ]] || exit 1\n"  # 10
            "coproc git ls-files > list 2> err4\n"  # 11: the coprocess
            "[[ ! -s err4 ]] || exit 1\n"  # 12
            "coproc {\n    git ls-files > list 2> err5 || exit 1\n    [[ ! -s err5 ]] || exit 1\n}\n"  # 13 to 16
            "! {\n    git ls-files > list 2> err6 || exit 1\n    [[ ! -s err6 ]] || exit 1\n}\n"  # 17 to 20
            "git ls-files > list 2> err7 || exit 1 &\n"  # 21: the producer and its branch in the background
            "[[ ! -s err7 ]] || exit 1\n"  # 22
            "( git ls-files > list 2> err8 || exit 1 ) &\n"  # 23: the subshell in the background
            "[[ ! -s err8 ]] || exit 1\n"  # 24
            "git ls-files > list 2> err9\n"  # 25: accepted, the residual's form with no flag
            "[[ ! -s err9 ]] || exit 1\n"  # 26
            "{\n    git ls-files > list 2> err10\n    [[ ! -s err10 ]] || exit 1\n}\n"  # 27 to 30: accepted, the block in the foreground
            "f() {\n    git ls-files > list 2> err11 || return 1\n    [[ ! -s err11 ]] || return 1\n}\nf &\n"  # 31 to 35: accepted, judged by its own path
        )
        expected = [(line, "producer") for line in (3, 5, 8, 11, 14, 18, 21, 23)]
        result = self.assert_findings(body, expected)
        tail = "statement of the same list, as an `if` condition or the left side of a `||` that ends the script, or run it through read_listing of read-lib.sh; the producer"
        background = "runs in the background (`&`, the job started at line {}), so a later test reads its stderr file before the listing has finished"
        coprocess = "runs in a coprocess started at line {}, so a later test reads its stderr file before the listing has finished and its status is the start's"
        for line, message in (
            (3, background.format(3)),
            (5, "is negated (`!`), so its failure status is read as success"),
            (8, background.format(7)),
            (11, coprocess.format(11)),
            (14, coprocess.format(13)),
            (
                18,
                "sits in a statement negated (`!`) at line 17, so a failure that ends that statement is read as success",
            ),
            (21, background.format(21)),
            (23, background.format(23)),
        ):
            self.assertIn(
                f":{line}: producer: `git ls-files` can fail with exit 0 or after printing (status-blind-producers.tsv); send its stderr with `2>`, `2>>` or `2>|` to a file (the last redirect that touches fd 2 decides; any other operator there, and /dev/null, leave it uncaptured) and test `[[ ! -s <that file> ]]` in a later {tail} {message}\n",
                result.stdout,
            )

    def test_the_round_11_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The three P2 of the 3b416298 audit, which that head read as clean: form (ii) looked a name up among the
        top-level definitions only, so a second definition inside an `if` (`refuse() { return 0; }`) was unseen and
        `true() { exit 2; } &` was trusted although it defines the function in a child shell and the parent runs the
        builtin `true`; and form (iv) accepted `status+=$?`, which adds the status to the value (25 and 6 making 256,
        which a later `exit "$status"` turns into success). Round 11 counts every FuncDecl of the file at any depth,
        accepts a call only of a name defined exactly once, at the top level, in the foreground and not negated, before
        the tested statement in file order, and never of a bash builtin's or reserved word's name (round 12 closes that
        to the allowlist `refuse`, `fail`, so every other name here is named as no refusal name), each finding naming
        the duplicate's line, the flag or the name; form (iv) is a plain `=` of `$?` and the append is named."""
        body = (
            "refuse() {\n    exit 2\n}\n"  # 3 to 5
            "if true; then\n    refuse() {\n        return 0\n    }\nfi\n"  # 6 to 10: the nested redefinition, at 7
            "x=$(false) || refuse\n"  # 11
            "true() {\n    exit 2\n} &\n"  # 12 to 14: the background definition of a builtin's name, outside the allowlist
            "x=$(false) || true\n"  # 15
            "x=$(false) || late\n"  # 16: the definition comes after the read
            "late() {\n    exit 2\n}\n"  # 17 to 19
            "function twice {\n    exit 2\n}\n"  # 20 to 22: both spellings present
            "twice() {\n    exit 2\n}\n"  # 23 to 25
            "x=$(false) || twice\n"  # 26
            "outer() {\n    inner() {\n        exit 2\n    }\n}\n"  # 27 to 31: defined inside another function, at 28
            "x=$(false) || inner\n"  # 32
            "x=$(false) || status+=$?\n"  # 33: the append
            "! flagged() {\n    exit 2\n}\n"  # 34 to 36: a negated definition
            "x=$(false) || flagged\n"  # 37
            "fail() {\n    echo no >&2\n    exit 2\n}\n"  # 38 to 41: the single top-level definition before the read
            "x=$(false) || fail\n"  # 42: accepted
            "x=$(false) || status=$?\n"  # 43: accepted
            "job() {\n    exit 2\n} &\n"  # 44 to 46: a background definition of a name outside the allowlist
            "x=$(false) || job\n"  # 47
        )
        expected = [(line, "substitution") for line in (11, 15, 16, 26, 32, 33, 37, 47)]
        result = self.assert_findings(body, expected)
        for line, shape in (
            (11, "a call of `refuse`, defined 2 times (lines 3, 7), where bash runs whichever definition ran last"),
            (
                15,
                "a call of `true`, defined at line 12, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                16,
                "a call of `late`, defined at line 17, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (26, "a call of `twice`, defined at line 20, a name that is not a refusal name (`refuse`, `fail`)"),
            (32, "a call of `inner`, defined at line 28, a name that is not a refusal name (`refuse`, `fail`)"),
            (33, "an append (`+=`) of the status to the value, not a capture of `$?`"),
            (37, "a call of `flagged`, defined at line 34, a name that is not a refusal name (`refuse`, `fail`)"),
            (
                47,
                "a call of `job`, defined at line 44, a name that is not a refusal name (`refuse`, `fail`)",
            ),
        ):
            self.assertIn(f":{line}: substitution: the `||` branch is {shape} and does not end the read", result.stdout)

    def test_the_branches_of_a_tested_read_are_a_closed_list_and_every_other_shape_is_named(self) -> None:
        """Forms i to iv of rule a pass in any quoting of a known first word: `exit` or `return` as the whole branch
        with no argument, one known decimal from 1 to 255 or one bare `$?`; a function this file defines once, at top
        level, before the read, whose body is the refusal grammar (`echo`/`printf` sending fd 1 to fd 2, then one
        `exit <1-255>`; a function ending in a call of another, a name defined inside another statement, a name
        defined twice and a bare `exit` or `return` in a body are not accepted); a block or subshell whose statements
        are that grammar; and `name=$?` or `name=${?}`. Everything else is a finding that names the shape (a body or
        block outside the grammar names its first statement outside it, by line), and a function named `exit`, like
        every name outside the allowlist `refuse`, `fail` (round 12), is a finding naming the name, whatever its body,
        and its definition a `shadow` finding (round 13)."""
        preamble = (
            'refuse() {\n    echo "$1" >&2\n    exit 2\n}\n'
            "fail() exit 2\n"
            'fail_later() {\n    echo "failed"\n}\n'
            "if true; then\n    nested_refuse() {\n        exit 2\n    }\nfi\n"
            "twice() {\n    exit 2\n}\n"
            'twice() {\n    echo "no"\n}\n'
            "deep() {\n    refuse 'x'\n}\n"
            "zero() {\n    exit 0\n}\n"
            "bare_refuse() {\n    echo failed >&2\n    return\n}\n"
            "bare_only() {\n    exit\n}\n"
        )
        cases: list[tuple[str, str | None]] = [  # (the line, the shape the finding names, or None when accepted)
            ("x=$(a) || exit", None),
            ("x=$(a) || 'exit' 2", None),
            ('x=$(a) || "return" 1', None),
            ("x=$(a) || status=${?}", None),
            ("x=$(a) || refuse 'x'", None),
            ("x=$(a) || fail", None),
            ("x=$(a) || (echo no >&2; exit 1)", None),
            ("x=$(a) || { printf '%s\\n' \"$@\" >&2; exit 1; }", None),
            ("x=$(a) || { echo no 1>&2; exit 255; }", None),
            ("x=$(a) || exit $?", None),
            ("x=$(a) || return ${?}", None),
            ("x=$(a) || exit '255'", None),
            ("x=$(a) || { 'echo' no >&2; 'exit' 2; }", None),
            ("x=$(a) || { exit 1; }", None),
            ("x=$(a) || { echo no >&2; exit 2; }", None),
            (
                "x=$(a) || (refuse 'x')",
                "a subshell that breaks the refusal grammar (GRAMMAR) at line LINE with a call of `refuse`",
            ),
            (
                "x=$(a) || { refuse 'x'; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with a call of `refuse`",
            ),
            (
                "x=$(a) || { echo no >&2; return 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with the command `return`",
            ),
            (
                "x=$(a) || (exit)",
                "a subshell that breaks the refusal grammar (GRAMMAR) at line LINE with a bare `exit`, whose status",
            ),
            (
                "x=$(a) || { exit; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with a bare `exit`, whose status",
            ),
            (
                "x=$(a) || { echo no >&2; exit $?; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with `exit $?`, whose status",
            ),
            (
                "x=$(a) || { echo no; exit 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `echo` that does not send fd 1 to fd 2 (`>&2`)",
            ),
            ("x=$(a) || { echo no >&2 2>&1; exit 1; }", None),
            (
                "x=$(a) || { echo no 2>&1; exit 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `echo` that does not send fd 1 to fd 2 (`>&2`)",
            ),
            (
                "x=$(a) || { echo no >&3; exit 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `echo` that does not send fd 1 to fd 2 (`>&2`)",
            ),
            (
                "x=$(a) || { echo no > err; exit 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `echo` that does not send fd 1 to fd 2 (`>&2`)",
            ),
            (
                "x=$(a) || { echo no >&2; exit 1; exit 2; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `exit` before the last statement",
            ),
            (
                "x=$(a) || { echo no >&2; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with the command `echo` as the last statement, where the `exit` must be",
            ),
            (
                'x=$(a) || { echo "$?" >&2; exit 1; }',
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with `$?`",
            ),
            (
                'x=$(a) || { echo "$(b)" >&2; exit 1; }',
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with a command substitution",
            ),
            (
                "x=$(a) || { X=1 echo no >&2; exit 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with a command with an assignment before it",
            ),
            (
                "x=$(a) || { local m=1; echo no >&2; exit 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with a declaration",
            ),
            (
                "x=$(a) || { if true; then :; fi; exit 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `if`",
            ),
            (
                "x=$(a) || { echo no >&2; exit 1 2; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `exit` with 2 arguments",
            ),
            (
                'x=$(a) || { echo no >&2; exit "$c"; }',
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `exit` whose argument has no known text",
            ),
            (
                "x=$(a) || { echo no >&2; exit 256; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with `exit 256`, which turns the failed read into success",
            ),
            (
                "x=$(a) || { echo no >&2; exit abc; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with `exit abc`, whose argument is not a decimal from 1 to 255",
            ),
            ("x=$(a) || exit 0", "`exit 0`, which turns the failed read into success"),
            ("x=$(a) || return 0", "`return 0`, which turns the failed read into success"),
            ("x=$(a) || exit 256", "`exit 256`, which turns the failed read into success"),
            ("x=$(a) || exit abc", "`exit abc`, whose argument is not a decimal from 1 to 255"),
            ('x=$(a) || exit "$?"', "an `exit` whose argument has no known text"),
            ("x=$(a) || exit 1 2", "an `exit` with 2 arguments"),
            (
                "x=$(a) || { echo no >&2; exit 0; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with `exit 0`, which turns",
            ),
            (
                "x=$(a) || zero",
                "a call of `zero`, defined at line 25, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            ('x=$(a) || status="$?"', "an assignment of something other than `$?`"),
            ("x=$(a) || status=${?:-0}", "an assignment of something other than `$?`"),
            ("x=$(a) || status=$? other=1", "an assignment of something other than `$?`"),
            (
                "x=$(a) || { status=$?; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an assignment",
            ),
            ("x=$(a) || true", "the command `true`"),
            ("x=$(a) || :", "the command `:`"),
            ("x=$(a) || false", "the command `false`"),
            ("x=$(a) || true | cat", "a pipeline"),
            (
                "x=$(a) || { echo no && exit 1; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an `&&` list",
            ),
            (
                "x=$(a) || (exit 1 || exit 2)",
                "a subshell that breaks the refusal grammar (GRAMMAR) at line LINE with a `||` list",
            ),
            (
                "x=$(a) || { { exit 1; }; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with a block",
            ),
            ("x=$(a) || if true; then exit 1; fi", "an `if`"),
            ("x=$(a) || case $x in *) exit 1 ;; esac", "a `case`"),
            ("x=$(a) || [[ $? == 1 ]]", "a `[[ ]]` test"),
            ("x=$(a) || [[ $? == 1 ]] || exit 1", "a `[[ ]]` test"),
            ("x=$(a) || local status=$?", "a declaration"),
            ('x=$(a) || "$cmd"', "a command whose first word has no known text"),
            ("x=$(a) || $'exit'", "a command whose first word has no known text"),
            ("x=$(a) || ex\\it", "a command whose first word has no known text"),
            ("x=$(a) || refuse_undefined", "the command `refuse_undefined`"),
            (
                "x=$(a) || fail_later",
                "a call of `fail_later`, defined at line 8, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                "x=$(a) || nested_refuse",
                "a call of `nested_refuse`, defined at line 12, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                "x=$(a) || twice",
                "a call of `twice`, defined at line 16, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                "x=$(a) || deep",
                "a call of `deep`, defined at line 22, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                "x=$(a) || { echo no >&2; exit; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with a bare `exit`, whose status",
            ),
            (
                "x=$(a) || { y=1; return; }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with an assignment",
            ),
            (
                "x=$(a) || bare_refuse",
                "a call of `bare_refuse`, defined at line 28, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                "x=$(a) || bare_only",
                "a call of `bare_only`, defined at line 32, a name that is not a refusal name (`refuse`, `fail`)",
            ),
            (
                "x=$(a) || { exit 2 & }",
                "a block that breaks the refusal grammar (GRAMMAR) at line LINE with a command run in the background (`&`)",
            ),
        ]
        grammar = "`echo`/`printf` to stderr, then one `exit <1-255>`"
        first = 3 + preamble.count("\n")
        expected = [(first + index, "substitution") for index, (_, shape) in enumerate(cases) if shape]
        expected += [
            (first + index, "substitution") for index, (text, _) in enumerate(cases) if "$(b)" in text
        ]  # the inner one
        result = self.assert_findings(preamble + "".join(text + "\n" for text, _ in cases), expected)
        for index, (text, shape) in enumerate(cases):
            if shape:
                with self.subTest(text):
                    shape = shape.replace("GRAMMAR", grammar).replace("LINE", str(first + index))
                    self.assertIn(f":{first + index}: substitution: the `||` branch is {shape}", result.stdout)
        shadowed = "exit() {\n    echo no\n}\nx=$(a) || exit 1\n"
        result = self.assert_findings(shadowed, [(3, "shadow"), (6, "substitution")])
        self.assertIn(
            "a call of `exit`, defined at line 3, a name that is not a refusal name (`refuse`, `fail`)",
            result.stdout,
        )
        # A top-level function named `echo` takes that name from the grammar too: `echo x >&2` in a body is then a call.
        shadowed = "echo() {\n    :\n}\nfail() {\n    echo no >&2\n    exit 1\n}\nx=$(a) || fail\n"
        result = self.assert_findings(shadowed, [(3, "shadow"), (10, "substitution")])
        self.assertIn(
            f"a call of `fail`, whose body breaks the refusal grammar ({grammar}) at line 7 with a call of `echo`",
            result.stdout,
        )

    def test_an_empty_or_comment_only_file_is_refused_naming_it(self) -> None:
        """A tree with no top-level statement is never a clean file: the refusal names the file, before and after a
        clean one in the list, and nothing is printed on stdout."""
        clean = self.script("clean.sh", "x=$(a) || exit 1\n")
        empty = self.temp / "empty.sh"
        empty.write_text("")
        comment = self.temp / "comment.sh"
        comment.write_text("#!/usr/bin/env bash\n# nothing runs here\n")
        for name, paths in {"empty": [clean, empty], "comment-only": [comment, clean]}.items():
            with self.subTest(name):
                result = self.run_check(*paths)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertEqual("", result.stdout)
                self.assertEqual(
                    f"producer-status-check: {paths[name == 'empty']} holds no statement; the list is refused\n",
                    result.stderr,
                )

    def test_shape_4_a_read_from_a_file_is_a_finding_naming_read_file(self) -> None:
        result = self.assert_findings("read -r x < unreadable || exit 1\n", [(3, "read")])
        self.assert_findings("'read' -r x < unreadable || exit 1\n", [(3, "read")])
        self.assertIn("read_file", result.stdout)
        clean = 'while read -r l; do :; done < file\nread -r a b <<< "${v}"\nread -r -p "x" answer || exit 1\n'
        self.assert_findings(clean, [])
        # The `IFS=` prefix of such a read is a write to a guarded name (rule f, round 18), reported beside rule d.
        self.assert_findings("IFS= read -r x < unreadable || exit 1\n", [(3, "binding"), (3, "read")])

    def test_the_allow_comment_exempts_a_b_and_d_with_a_reason_and_is_a_finding_without_one(self) -> None:
        allowed = (
            "x=$(a) # producer-status: allow the status is read from the file below\n"
            "git ls-files > l # producer-status: allow the listing is advisory\n"
            "read -r y < f # producer-status: allow a reason\n"
        )
        self.assert_findings(allowed, [])
        # Rule f is exempted by nothing: the `IFS=` prefix stays a finding under an allow comment.
        self.assert_findings("IFS= read -r y < f # producer-status: allow a reason\n", [(3, "binding")])
        result = self.assert_findings("x=$(a) # producer-status: allow\n", [(3, "allow"), (3, "substitution")])
        self.assertIn("needs a reason", result.stdout)
        # The prologue rule has no exemption.
        self.assert_findings("x=$(a) || exit 1 # producer-status: allow a reason\n", [(1, "prologue")], prologue="")

    def test_a_file_without_set_euo_pipefail_before_its_first_substitution_is_a_finding_at_line_1(self) -> None:
        cases = {
            "no set at all": ("x=$(a) || exit 1\n", [(1, "prologue")]),
            "set after the substitution": ("x=$(a) || exit 1\nset -euo pipefail\n", [(1, "prologue")]),
            "set -eu only": ("set -eu\nx=$(a) || exit 1\n", [(1, "prologue")]),
            "set inside a function": ("f() { set -euo pipefail; }\nx=$(a) || exit 1\n", [(1, "prologue")]),
            "a function holding a substitution before set": (
                "f() { x=$(a) || return 1; }\nset -euo pipefail\n",
                [(1, "prologue")],
            ),
            "the pr-audit shape": (
                "if [[ $- != *p* ]]; then\n    exit 2\nfi\nset -euo pipefail\nx=$(a) || exit 1\n",
                [],
            ),
            "no substitution": ("echo hello\n", []),
            "a quoted heredoc is no substitution": ("cat << 'EOF'\n$(a)\nEOF\n", []),
        }
        for name, (body, expected) in cases.items():
            with self.subTest(name):
                result = self.assert_findings(body, expected, prologue="")
                if expected:
                    self.assertIn("`set -euo pipefail` must run at top level", result.stdout)

    def test_a_file_shfmt_cannot_parse_an_unreadable_or_missing_file_and_an_empty_list_are_refused(self) -> None:
        clean = self.script("clean.sh", "x=$(a) || exit 1\n")
        cases = {"unparsable": [clean, ANSI_C_HEREDOC], "missing": [clean, self.temp / "absent"], "empty list": []}
        if os.geteuid() != 0:
            unreadable = self.script("unreadable.sh", "true\n")
            unreadable.chmod(0o000)
            cases["unreadable"] = [clean, unreadable]
        for name, paths in cases.items():
            with self.subTest(name):
                result = self.run_check(*paths)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertEqual("", result.stdout, "no finding and no clean verdict stands in for the refusal")
                self.assertIn("is refused", result.stderr)
        self.assertIn("shfmt cannot parse", self.run_check(clean, ANSI_C_HEREDOC).stderr)

    def lint_copy(self, table_text: str) -> Path:
        """A copy of the lint with its contract, pin and fixtures under a scratch root, and the producer table as
        given; ROOT is not read."""
        root = self.temp / "copy"
        for rel in COPIED:
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, root / rel)
        (root / "scripts/ci/status-blind-producers.tsv").write_text(table_text)
        return root / "scripts/ci/producer-status-check.sh"

    def test_a_malformed_or_missing_producer_table_refuses_the_list(self) -> None:
        clean = self.script("clean.sh", "x=$(a) || exit 1\n")
        good = TABLE.read_text()
        cases = {
            "a row with two cells": good + "ls\tmeasured only\n",
            "an empty cell": good + "ls\t\tsource\n",
            "another header": good.replace("words\tmeasured\tsource", "word\tmeasured\tsource"),
            "no row": "words\tmeasured\tsource\n",
            "words with two spaces": good + "git  ls-tree\tmeasured\tsource\n",
        }
        for name, text in cases.items():
            with self.subTest(name):
                result = subprocess.run(
                    ["bash", str(self.lint_copy(text)), str(clean)], capture_output=True, text=True, check=False
                )
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertEqual("", result.stdout)
                self.assertIn("the list is refused", result.stderr)
        copy = self.lint_copy(good)
        result = subprocess.run(["bash", str(copy), str(clean)], capture_output=True, text=True, check=False)
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr), "the control: the real table")
        (copy.parent / "status-blind-producers.tsv").unlink()
        result = subprocess.run(["bash", str(copy), str(clean)], capture_output=True, text=True, check=False)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("cannot read the producer table", result.stderr)

    def test_the_round_12_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The two P2 of the 3fed043e audit, which that head read as clean: the builtin denylist of round 11 omitted
        `fc`, so `fc() { exit 2; }; unset -f fc; x=$(false) || fc -l` passed while bash ran the builtin and went on;
        and the definitions and allow-comment scans walked the literal body of a partly quoted heredoc that the main
        walk skips, so `$(refuse() { return 0; })` in a `<< 'E'OF` body made the file's one `refuse` a duplicate and a
        `# producer-status: allow` there was a malformed-allow finding. Round 12 replaces the denylist by the closed
        allowlist REFUSAL_NAMES (`refuse`, `fail`): a call of any other defined name is a finding naming the name,
        whatever the body, and the round-11 definition rule and the body grammar judge those two names; every scan
        descends by the one traversal, so a literal heredoc body defines, exempts and breaks nothing."""
        body = (
            "fc() {\n    exit 2\n}\n"  # 3 to 5: the auditor's probe
            "unset -f fc\n"  # 6
            "x=$(false) || fc -l\n"  # 7
            "die() {\n    echo x >&2\n    exit 2\n}\n"  # 8 to 11: the grammar, under a name outside the allowlist
            "x=$(false) || die\n"  # 12
            "refuse() {\n    echo no >&2\n    exit 2\n}\n"  # 13 to 16
            'fail() {\n    echo "$1" >&2\n    exit 1\n}\n'  # 17 to 20
            "cat << 'E'OF\n$(refuse() { return 0; })\n$(true # producer-status: allow\n)\nEOF\n"  # 21 to 25: literal
            "x=$(false) || refuse\n"  # 26: accepted, the one definition is at 13
            "x=$(false) || fail y\n"  # 27: accepted
            "y=$(cat << 'E'OF\n$(true # producer-status: allow the text is literal\n)\nEOF\n)\n"  # 28 to 32: a plain read
        )
        expected = [(line, "substitution") for line in (7, 12, 28)]
        result = self.assert_findings(body, expected)
        for line, shape in (
            (7, "a call of `fc`, defined at line 3, a name that is not a refusal name (`refuse`, `fail`)"),
            (12, "a call of `die`, defined at line 8, a name that is not a refusal name (`refuse`, `fail`)"),
        ):
            self.assertIn(f":{line}: substitution: the `||` branch is {shape} and does not end the read", result.stdout)
        self.assertIn(":28: substitution: a command substitution here loses its status", result.stdout)
        # The round-11 definition rule and the body grammar still judge the two allowed names, one script each.
        grammar = "`echo`/`printf` to stderr, then one `exit <1-255>`"
        for name, body, line, shape in (
            (
                "after the read",
                "x=$(false) || refuse\nrefuse() {\n    exit 2\n}\n",
                3,
                "a call of `refuse`, defined at line 4, after the tested statement at line 3, so the function has not been defined when the read fails",
            ),
            (
                "inside another statement",
                "if true; then\n    fail() {\n        exit 2\n    }\nfi\nx=$(false) || fail\n",
                8,
                "a call of `fail`, defined at line 4 inside another statement, not at the top level",
            ),
            (
                "negated",
                "! refuse() {\n    exit 2\n}\nx=$(false) || refuse\n",
                6,
                "a call of `refuse`, whose definition at line 3 is negated (`!`), a flagged statement",
            ),
            (
                "in the background",
                "fail() {\n    exit 2\n} &\nx=$(false) || fail\n",
                6,
                "a call of `fail`, whose definition at line 3 runs in the background (`&`), so the function exists in a child shell only",
            ),
            (
                "twice",
                "refuse() {\n    exit 2\n}\nfunction refuse {\n    exit 2\n}\nx=$(false) || refuse\n",
                9,
                "a call of `refuse`, defined 2 times (lines 3, 6), where bash runs whichever definition ran last",
            ),
            (
                "a body outside the grammar",
                "fail() {\n    echo failed >&2\n    return $?\n}\nx=$(false) || fail\n",
                7,
                f"a call of `fail`, whose body breaks the refusal grammar ({grammar}) at line 5 with the command `return`",
            ),
        ):
            with self.subTest(name):
                result = self.assert_findings(body, [(line, "substitution")])
                self.assertIn(
                    f":{line}: substitution: the `||` branch is {shape} and does not end the read", result.stdout
                )

    def test_the_round_13_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The two P2 of the 4f7b58c1 audit, which that head read as clean: a redirect's descriptor was compared with
        the text `2`, so `02>&1` after `2> err` touched nothing while the warnings went to stdout and `[[ ! -s err ]]`
        passed; the word of a `>&` counted as a descriptor whenever its text was digits or `-`, and a written
        descriptor other than 2 never touched fd 2, so the move `1>&2-` (fd 2 closed) passed too; and the prologue
        credited a file-defined `set() { :; }`, so a warned listing with a bare `[[ ! -s err ]]` had zero findings.
        Round 13 reads the descriptor as bash does, a decimal (`02` and `002` are fd 2; `{fd}>` refuses the file, exit
        2), reads the word of a `>&` or `<&` as a plain descriptor only when all digits or exactly `-` (any other word
        touches fd 2 whatever the descriptor before it: a move, a file, which bash 3.2 sends both streams to after
        `1>&` as well, a word with no known text), and adds rule f: a function, `alias`, `enable` or `hash` naming a
        word the rules read as a builtin or a producer (`set`, `exit`, `return`, `echo`, `printf`, `git`, `find`, `ls`,
        built from the rules' own data) is a `shadow` finding at its line, which no allow comment exempts."""
        body = (
            "git ls-files > l 2> err 02>&1\n[[ ! -s err ]]\n"  # 3: the auditor's probe, fd 2 back onto stdout
            "git ls-files > l 2> err 1>&2-\n[[ ! -s err ]]\n"  # 5: the auditor's probe, fd 2 moved onto fd 1, closed
            "git ls-files > l 2> err 2>&1-\n[[ ! -s err ]]\n"  # 7
            "git ls-files > l 2> err >&2-\n[[ ! -s err ]]\n"  # 9
            "git ls-files > l 2> err <&2-\n[[ ! -s err ]]\n"  # 11: fd 2 moved onto fd 0, closed
            "git ls-files > l 2> err 1>&file\n[[ ! -s err ]]\n"  # 13: both streams to the file on bash 3.2
            "git ls-files > l 2> err 1>&$fd\n[[ ! -s err ]]\n"  # 15: no known text, any of them when it runs
            "git ls-files > l 02> err\n[[ ! -s err ]]\n"  # 17: accepted, 02 is fd 2 and err a file
            "git ls-files > l 002> err 01>&1\n[[ ! -s err ]]\n"  # 19: accepted, `01>&1` leaves fd 2 alone
            "git ls-files > l 2> err >&- <&0 2>&1 2> err\n[[ ! -s err ]]\n"  # 21: accepted, the last one captures
        )
        result = self.assert_findings(body, [(line, "producer") for line in (3, 5, 7, 9, 11, 13, 15)])
        for line in result.stdout.splitlines():
            self.assertTrue(line.endswith("or run it through read_listing of read-lib.sh"), line)  # no later test
        # The grammar's `>&2` is read the same way: `1>&02` and `01>&2` send fd 1 to fd 2.
        grammar = (
            "x=$(a) || { echo no 1>&02; exit 1; }\nrefuse() {\n    echo no 01>&2\n    exit 2\n}\ny=$(a) || refuse\n"
        )
        self.assert_findings(grammar, [])
        # A descriptor that is not a decimal is not read: the file is refused, never passed, and nothing is printed.
        variable = self.script("variable.sh", "git ls-files > l {fd}> err\n[[ ! -s err ]]\n")
        result = self.run_check(variable)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)
        self.assertEqual(
            f"producer-status-check: cannot judge {variable}: the redirect descriptor `{{fd}}` at line 3 is not a "
            "decimal; the list is refused\n",
            result.stderr,
        )
        shadow = (
            "set() { :; }\n"  # 3: the auditor's probe
            "git ls-files > l 2> err\n[[ ! -s err ]]\n"  # 4, 5: rule b accepts the bare test after the prologue
            "exit() { :; }\n"  # 6
            "echo() { exit 0; }\n"  # 7
            'git() { command git "$@"; return 0; }\n'  # 8: three findings since round 14 (`command git`, `"$@"`)
            "printf() { :; }\n"  # 9
            "return() { :; }\n"  # 10
            "find() { :; }\n"  # 11
            "ls() { :; }\n"  # 12
            "alias set='true' # producer-status: allow nothing exempts rule f\n"  # 13: any alias since round 16
            "enable -n set\n"  # 14
            "hash -p /tmp/git git\n"  # 15
            'alias "$name"\n'  # 16: an argument with no known text
            "if true; then function set { :; }; fi\n"  # 17: at any depth, in any spelling
            "other() { :; }\n"  # 18: accepted
            "alias ll='ls -l'\n"  # 19: a finding since round 16: no lever defines an alias, so none is accepted
            "hash -r\n"  # 20: accepted
            "unset -f set\n"  # 21: a finding since round 14, like the definition at 3
        )
        shadowed = [(line, "shadow") for line in (3, *range(6, 18), 8, 8, 19, 21)]
        result = self.assert_findings(
            shadow, shadowed + [(13, "binding")]
        )  # 13: `set='true'` spells a write (round 18)
        producers = (
            "the producers `git ls-files`, `git config -f`, `git config --file` rule b holds to a stderr capture"
        )
        for line, message in (
            (
                3,
                "a function named `set` shadows the builtin the prologue `set -euo pipefail` relies on (rule c); bash runs it instead",
            ),
            (6, "a function named `exit` shadows the builtin a `||` branch ends a failed read with (rule a, form i)"),
            (
                7,
                "a function named `echo` shadows the builtin the refusal grammar writes to stderr with (rule a, forms ii and iii)",
            ),
            (8, f"a function named `git` shadows {producers}; bash runs it instead"),
            (11, "a function named `find` shadows the producer `find` rule b holds to a stderr capture"),
            (13, f"`alias` defines or prints an alias, {ALIAS}"),
            (14, "`enable` names `set` and shadows the builtin the prologue"),
            (15, f"`hash` names `git` and shadows {producers}"),
            (16, f"`alias` defines or prints an alias, {ALIAS}"),
            (17, "a function named `set` shadows the builtin the prologue"),
            (19, f"`alias` defines or prints an alias, {ALIAS}"),
        ):
            self.assertIn(f":{line}: shadow: {message}", result.stdout)

    def test_the_round_14_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The two P2 of the d6a0da12 audit, which that head read as clean: rule f's rebinders were three words and
        left out the refusal names, so `refuse() { exit 2; }; unset -f refuse; hash -p /usr/bin/true refuse;
        x=$(false) || refuse` passed while /bin/bash 3.2 ran on with exit 0 (`refuse: command not found`, and the same
        after `unset refuse`: a name with no variable is a function); and descriptor_number ran on a producer's
        redirects only, so `set -euo pipefail; true {fd}>err` passed. Round 14 reads every rebinding form bash offers
        (REBINDERS, each word as bash reads it, and an assignment to PATH, BASH_ALIASES or BASH_CMDS), accepts the one
        `source` shape the levers use, and validates every redirect the walk meets."""
        rebinders = (
            "refuse() { exit 2; }\n"  # 3: a refusal name's one definition is form ii's, not a shadow finding
            "fail() { exit 1; }\n"  # 4
            "unset -f refuse; hash -p /usr/bin/true refuse; x=$(false) || refuse\n"  # 5: the auditor's line, twice
            "alias fail=true\n"  # 6: the auditor's alias
            "y=$(false) || fail\n"  # 7: accepted, the alias is the finding
            "enable -n echo\n"  # 8: the auditor's enable
            'eval "refuse() { :; }"\n'  # 9: the auditor's eval
            "source ./lib.sh\n"  # 10: the auditor's source
            "unset refuse\n"  # 11: a name with no variable is a function
            'unset "$name"\n'  # 12: no known text
            "command unset -f refuse\n"  # 13: `command` names refuse, and the forwarded `unset` does
            "builtin unset -f fail\n"  # 14: the same
            "command git ls-files > l 2> err\n"  # 15: `command git` runs past rule b
            "trap 'refuse() { :; }' DEBUG\n"  # 16: redefined before the next command
            "trap 'cleanup; unset -f refuse' EXIT\n"  # 17: a second command in the action
            'trap "$handler" EXIT\n'  # 18
            "mapfile -C 'unset -f refuse' -c 1 lines\n"  # 19
            "PATH=/tmp/bin\n"  # 20
            "BASH_ALIASES[fail]=true\n"  # 21
            "export PATH=/tmp/bin\n"  # 22: a declaration's argument is an assignment
            "declare -A BASH_CMDS=([git]=/usr/bin/true)\n"  # 23
            'source "${LEVER_DIR}/other.sh"\n'  # 24: not a library
            '. "${LEVER_DIR:-.}/read-lib.sh"\n'  # 25: not the bare expansion
            '. "$dir/read-lib.sh"\n'  # 26: not LEVER_DIR
            'eval "$code"\n'  # 27
            'command "$@"\n'  # 28
            "unset x\n"  # 29: accepted from here on, `alias -p` at 42 aside (a finding since round 16)
            "export PATH\n"  # 30: no value
            "declare -r y=1\n"  # 31
            "hash -r\n"  # 32
            'unset -v "$name"\n'  # 33: variables only
            'command -v "$tool" > /dev/null\n'  # 34: prints, runs nothing
            '. "${LEVER_DIR}/git-isolated.sh"\n'  # 35: the one accepted shape
            '. "${LEVER_DIR}/read-lib.sh"\n'  # 36
            'source "$LEVER_DIR/read-lib.sh"\n'  # 37
            "trap cleanup EXIT\n"  # 38: one simple command
            "trap '' INT TERM HUP\n"  # 39
            "trap 'rm -f \"${file}\"' EXIT\n"  # 40
            "trap - EXIT\n"  # 41
            "alias -p\n"  # 42: any alias call is a finding since round 16
            "mapfile -t lines\n"  # 43
            "export GIT_INDEX_FILE=${scratch}/index\n"  # 44
            'export "${GIT_ISOLATED_ENV[@]}"\n'  # 45
            "export -f refuse\n"  # 46: leaves the function bound
            "readonly -f fail\n"  # 47
            "unset -f other\n"  # 48: no word the rules read
        )
        twice = (5, 13, 14)
        shadowed = (*range(5, 7), *range(8, 20), *range(24, 29), *twice, 42)
        # Round 18: a write to a guarded name is `binding`: the assignments of 20 to 23, the `fail=true` word of the
        # alias at 6, and `export PATH`, `export "${GIT_ISOLATED_ENV[@]}"` outside git-isolated.sh, `export -f refuse`
        # and `readonly -f fail` (30, 45, 46, 47), accepted before, are writes now. Round 20: the subscripts `[fail]`
        # and `[git]` of 21 and 23 are arithmetic operands bash evaluates for an indexed array (twice each).
        bound = (6, 20, 21, 21, 22, 23, 23, 30, 45, 46, 47)
        expected = [(line, "shadow") for line in shadowed] + [(line, "binding") for line in bound]
        result = self.assert_findings(rebinders, expected)
        names = NAMES
        refusal = "and shadows the refusal function a `||` branch calls (rule a, form ii)"
        unread = f"this walk has not read, which may define or rebind one of {names}"
        for line, message in (
            (5, f"`unset` names `refuse` {refusal}"),
            (5, f"`hash` names `refuse` {refusal}"),
            (6, f"`alias` defines or prints an alias, {ALIAS}"),
            (8, "`enable` names `echo` and shadows the builtin the refusal grammar writes to stderr with"),
            (9, f"`eval` runs text {unread}: `refuse() {{ :; }}`"),
            (10, f"`source` reads a file {unread}: `./lib.sh`"),
            (11, f"`unset` names `refuse` {refusal}"),
            (12, f"`unset` has an argument with no known text, which may name one of {names}"),
            (13, f"`command` names `refuse` {refusal}"),
            (13, f"`unset` names `refuse` {refusal}"),
            (
                15,
                "`command` names `git` and shadows the producers `git ls-files`, `git config -f`, `git config --file`",
            ),
            (16, f"`trap` runs an action {unread[:22]} whole{unread[22:]}: `refuse() {{ :; }}`"),
            (18, f"`trap` runs an action with no known text, which may define or rebind one of {names}"),
            (19, f"`mapfile` runs a callback (`-C`) {unread}"),
            (25, f"`.` reads a file with no known text, which may define or rebind one of {names}"),
            (28, f"`command` has an argument with no known text, which may name one of {names}"),
        ):
            self.assertIn(f":{line}: shadow: {message}", result.stdout)
        path = "a write to `PATH` (the directories bash searches for `git`, `find`, `ls` and every other command word)"
        for line, message in (
            (
                6,
                "a write to `fail` (a refusal function a `||` branch calls (rule a, form ii)): a word spelling an assignment, `fail=…`, in the command `alias`",
            ),
            (20, f"{path}: an assignment, in an assignment"),
            (
                21,
                "a write to `BASH_ALIASES` (the alias table of bash 4, which `alias` writes): an assignment, in an assignment",
            ),
            (
                23,
                "a write to `BASH_CMDS` (the hash table of bash 4, which `hash -p` writes): an assignment, in the declaration `declare`",
            ),
            (30, f"{path}: an assignment with no value, or the bare name, in the declaration `export`"),
            (
                45,
                "a write to any guarded name: a word of `export` with no known text, which may spell an assignment to any of them, in the declaration `export`",
            ),
            (
                46,
                "a write to `refuse` (a refusal function a `||` branch calls (rule a, form ii)): an assignment with no value, or the bare name, in the declaration `export`",
            ),
        ):
            self.assertIn(f":{line}: binding: {message}", result.stdout)
        # Every redirect the walk meets is validated: a descriptor that is not a decimal refuses the file on any
        # command, in any statement, never only on a producer; a decimal one passes anywhere.
        for body, line in (
            ("true {fd}>err\n", 3),  # the auditor's line
            ("exec {fd}>err\n", 3),
            ("f() { :; } {fd}>err\n", 3),
            ("if true; then :; fi {fd}>err\n", 3),
            ("x=$(a) || exit 1\n[[ -n x ]] {fd}<err\n", 4),
            ("while :; do break; done {fd}>err\n", 3),
        ):
            with self.subTest(body=body):
                variable = self.script("variable.sh", body)
                result = self.run_check(variable)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertEqual("", result.stdout)
                self.assertEqual(
                    f"producer-status-check: cannot judge {variable}: the redirect descriptor `{{fd}}` at line {line} "
                    "is not a decimal; the list is refused\n",
                    result.stderr,
                )
        self.assert_findings("exec 3>err\ntrue 2>err\nf() { :; } 2>err\nx=$(a) || exit 1\n", [])

    def test_the_round_15_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The P2 of the 861f4577 audit, which that head read as clean: rule f's option loop took a word starting with
        `+` for an option of every rebinder, so `source +payload.sh` had no file left to judge and passed while
        /bin/bash 3.2 sourced the file, whose `refuse() { :; }` let `x=$(false) || refuse` run on with exit 0. Round 15
        reads the options per word (SKIPS_OPTIONS): `source`, `.` and `eval` skip nothing, every argument word is the
        file or the text; the namers, the forwarders, `trap`, `mapfile` and `readarray` read only `-` words for their
        letters, `--` ends them, a letter with an argument (`hash -p /x`) takes it and a `+` word is an argument
        (measured: `hash +r` is looked up, `unset +f` is not a valid identifier); a call left with no argument to judge
        is a finding, `hash -r` and `alias -p`, whose option is the whole job, aside."""
        (self.temp / "+payload.sh").write_text("refuse() { :; }\n")
        auditor = self.script(
            "auditor.sh", "refuse() { exit 2; }\nsource +payload.sh\nx=$(false) || refuse\necho ran\n"
        )
        ran = subprocess.run(["/bin/bash", str(auditor)], cwd=self.temp, capture_output=True, text=True, check=False)
        self.assertEqual((0, "ran\n"), (ran.returncode, ran.stdout), ran.stderr)  # measured: bash reads the file
        rebinders = (
            "refuse() { exit 2; }\n"  # 3
            "source +payload.sh\n"  # 4: the auditor's line
            "x=$(false) || refuse\n"  # 5: accepted; the source is the finding
            ". +payload.sh\n"  # 6
            "source -- payload.sh\n"  # 7: bash skips the `--` and reads the file; every word is the finding's
            "source\n"  # 8: no argument to judge
            'source "$f"\n'  # 9
            "source payload.sh arg\n"  # 10: the one accepted shape has one argument
            "eval +x\n"  # 11
            "eval\n"  # 12
            "enable -n\n"  # 13: no argument after the options
            "hash -p /usr/bin/true\n"  # 14: `-p` takes the path; no name after it
            "unset\n"  # 15
            "trap -p\n"  # 16
            "mapfile -C 'unset -f refuse'\n"  # 17: the callback, and no array after the options (twice)
            "command -- unset -f refuse\n"  # 18: `--` ends the options; `command` names refuse, so does `unset` (twice)
            "hash -- refuse\n"  # 19
            "enable -n -- echo\n"  # 20: disables the builtin (measured)
            "unset -- refuse\n"  # 21
            "alias +fail=true fail=true\n"  # 22: any alias call is a finding since round 16, one per call
            "hash -p /usr/bin/true +refuse\n"  # 23: accepted from here on, 27 aside: binds `+refuse` (measured), not refuse
            'source "${LEVER_DIR}/read-lib.sh"\n'  # 24: the one accepted shape
            'source "${LEVER_DIR}/git-isolated.sh"\n'  # 25
            "hash -r\n"  # 26: the option is the whole job
            "alias -p\n"  # 27: a finding since round 16
            "unset -v x\n"  # 28
            "unset -v\n"  # 29: inert before the count
            'hash -p "$path" other\n'  # 30: the path is the option's argument; `other` is no word the rules read
            'enable -f "$file" other\n'  # 31
            "mapfile -d '' -t lines\n"  # 32: `-d` takes the delimiter
            "trap - EXIT\n"  # 33
            "command -v\n"  # 34
            "trap -- cleanup EXIT\n"  # 35
        )
        twice = (17, 18)
        expected = [(line, "shadow") for line in (4, *range(6, 23), *twice, 27)]
        expected.append((22, "binding"))  # `fail=true` spells a write to a guarded name (round 18)
        result = self.assert_findings(rebinders, expected)
        names = NAMES
        refusal = "and shadows the refusal function a `||` branch calls (rule a, form ii)"
        unread = f"this walk has not read, which may define or rebind one of {names}"
        for line, message in (
            (4, f"`source` reads a file {unread}: `+payload.sh`"),
            (6, f"`.` reads a file {unread}: `+payload.sh`"),
            (7, f"`source` reads a file {unread}: `-- payload.sh`"),
            (8, "`source` has no argument to judge"),
            (9, f"`source` reads a file with no known text, which may define or rebind one of {names}"),
            (10, f"`source` reads a file {unread}: `payload.sh arg`"),
            (11, f"`eval` runs text {unread}: `+x`"),
            (12, "`eval` has no argument to judge"),
            (13, "`enable` has no argument to judge"),
            (14, "`hash` has no argument to judge"),
            (15, "`unset` has no argument to judge"),
            (16, "`trap` has no argument to judge"),
            (17, "`mapfile` has no argument to judge"),
            (17, f"`mapfile` runs a callback (`-C`) {unread}"),
            (18, f"`command` names `refuse` {refusal}"),
            (18, f"`unset` names `refuse` {refusal}"),
            (19, f"`hash` names `refuse` {refusal}"),
            (20, "`enable` names `echo` and shadows the builtin the refusal grammar writes to stderr with"),
            (21, f"`unset` names `refuse` {refusal}"),
            (22, f"`alias` defines or prints an alias, {ALIAS}"),
        ):
            self.assertIn(f":{line}: shadow: {message}", result.stdout)
        self.assertNotIn(":23:", result.stdout)

    def test_the_round_16_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The P2 of the b858f491 audit, which that head read as clean: rule f protected the words the rules interpret
        and the refusal names, not its own rebinders, so `alias command=eval` passed and `command 'refuse() { return
        0; }'` redefined the refusal function through a word the rule read as its own; /bin/bash 3.2 then ran `x=$(false)
        || refuse` on with exit 0 under `shopt -s expand_aliases` (measured below; without that option non-interactive
        bash expands no alias and the line exits 127). Round 16 closes the set over itself (interpreted holds every
        REBINDER, so a function, `enable`, `hash`, `unset` or forwarder naming one is a finding) and reads `alias` and
        `unalias` in any form, and `shopt` with `expand_aliases` among its arguments or an argument with no known text,
        as findings: no lever defines an alias, so the rule has none to accept."""
        bypass = "refuse() { exit 2; }\nalias command=eval\ncommand 'refuse() { return 0; }'\nx=$(false) || refuse\necho ran\n"
        plain = self.script("plain.sh", bypass)
        expanded = self.script("expanded.sh", "shopt -s expand_aliases\n" + bypass)
        ran = subprocess.run(["/bin/bash", str(plain)], cwd=self.temp, capture_output=True, text=True, check=False)
        self.assertEqual((127, ""), (ran.returncode, ran.stdout), ran.stderr)  # measured: the alias is inert
        ran = subprocess.run(["/bin/bash", str(expanded)], cwd=self.temp, capture_output=True, text=True, check=False)
        self.assertEqual((0, "ran\n"), (ran.returncode, ran.stdout), ran.stderr)  # measured: the refusal returns 0
        rebinders = (
            "refuse() { exit 2; }\n"  # 3
            "alias command=eval\n"  # 4: the auditor's alias
            "command 'refuse() { return 0; }'\n"  # 5: accepted on its own: without the alias bash finds no such command
            "x=$(false) || refuse\n"  # 6: accepted; the alias is the finding
            "shopt -s expand_aliases; alias refuse=true\n"  # 7: twice
            "hash -p /usr/bin/true command\n"  # 8: a rebinder of a rebinder
            "enable -n command\n"  # 9
            "eval() { :; }\n"  # 10
            "unalias command\n"  # 11: any form
            "unalias -a\n"  # 12
            "alias -p\n"  # 13
            "alias ll='ls -l'\n"  # 14
            "shopt -qs expand_aliases\n"  # 15: any spelling
            "shopt -u expand_aliases\n"  # 16
            'shopt -s "$option"\n'  # 17: no known text
            "command alias x=y\n"  # 18: the forwarded `alias` is the finding, not `command` naming it
            "builtin shopt -s expand_aliases\n"  # 19: the forwarded `shopt`
            "unset -f command\n"  # 20
            "trap 'alias refuse=true' DEBUG\n"  # 21: the action's first word is a rebinder
            'command() { eval "$@"; }\n'  # 22: the function the `enable -n command` bypass needs, and its eval (twice)
            "hash -p /usr/bin/true shopt\n"  # 23
            "enable -f ./x.so unalias\n"  # 24
            "shopt -s -- expand_aliases\n"  # 25: bash reads the option after `--` (measured)
            "shopt -s inherit_errexit\n"  # 26: accepted from here on
            "command -v git > /dev/null\n"  # 27
            "shopt\n"  # 28: prints the options
            "shopt -q nullglob\n"  # 29
            "hash -p /usr/bin/true other\n"  # 30
            "hash -r\n"  # 31
            "unset -v x\n"  # 32
        )
        twice = (7, 22)
        expected = [(line, "shadow") for line in (4, *range(7, 26), *twice)]
        expected += [(4, "binding"), (7, "binding")]  # `command=eval` and `refuse=true` spell writes (round 18)
        result = self.assert_findings(rebinders, expected)
        option = "`shopt` names `expand_aliases`, under which a script expands aliases and an alias rebinds any word; no lever sets it"
        for line, message in (
            (4, f"`alias` defines or prints an alias, {ALIAS}"),
            (7, f"`alias` defines or prints an alias, {ALIAS}"),
            (7, option),
            (8, f"`hash` names `command` and shadows {REBINDER}"),
            (9, f"`enable` names `command` and shadows {REBINDER}"),
            (10, f"a function named `eval` shadows {REBINDER}; bash runs it instead"),
            (11, f"`unalias` removes an alias, {ALIAS}"),
            (12, f"`unalias` removes an alias, {ALIAS}"),
            (13, f"`alias` defines or prints an alias, {ALIAS}"),
            (15, option),
            (16, option),
            (17, "`shopt` has an argument with no known text, which may name `expand_aliases`"),
            (18, f"`alias` defines or prints an alias, {ALIAS}"),
            (19, option),
            (
                21,
                f"`trap` runs an action this walk has not read whole, which may define or rebind one of {NAMES}: `alias refuse=true`",
            ),
            (22, f"a function named `command` shadows {REBINDER}; bash runs it instead"),
            (22, f"`eval` runs text with no known text, which may define or rebind one of {NAMES}"),
            (23, f"`hash` names `shopt` and shadows {REBINDER}"),
            (24, f"`enable` names `unalias` and shadows {REBINDER}"),
            (25, option),
        ):
            self.assertIn(f":{line}: shadow: {message}", result.stdout)
        self.assertNotIn(":5:", result.stdout)

    def test_the_round_17_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The two P2 of the e0386559 audit, which that head read as clean: rule f read a binding assignment as an
        Assign node only, so `export 'PATH=/tmp/x:$PATH'` (a quoted word) and `builtin export PATH=/tmp/x` (a word
        through a forwarder) passed while /bin/bash 3.2 set PATH and the next `git` was the spoofed one (measured
        below); and a process substitution was no boundary, so `cat <(x=$(false) || exit 1)` passed while bash went
        on with exit 0 after the failed read (measured below). Round 17 reads every argument word of a declaration, of
        `env` and of either through a forwarder (BINDERS, BINDING_WORD; `export "${GIT_ISOLATED_ENV[@]}"` the one
        accepted word with no known text, that array's assignments read as the exported words), and puts a process
        substitution on the path of the statements inside it (flagged_path), so a tested read or a producer there is a
        finding naming the substitution's line. Round 18 replaced the binding reading with the guarded-name allowlist:
        the lines below are kept, judged by it (`binding`; `env "$@"` is an external command's argument, accepted; the
        bare `export PATH`, the library's lines outside git-isolated.sh and `export -f refuse` are writes)."""
        spoof = self.temp / "x"
        spoof.mkdir()
        (spoof / "git").write_text("#!/bin/sh\necho spoofed\n")
        (spoof / "git").chmod(0o755)
        read = 'listing=$(git ls-files) || exit 1\necho "ran ${listing}"\n'
        for binding in (
            f"export 'PATH={spoof}:$PATH'\n",  # the auditor's quoted word: PATH is the literal, git is the spoofed one
            f"builtin export PATH={spoof}\n",  # the auditor's forwarded word
            f"declare -x PATH={spoof}\n",
            f'GIT_ISOLATED_ENV=(GIT_CONFIG_NOSYSTEM=1 PATH={spoof})\nexport "${{GIT_ISOLATED_ENV[@]}}"\n',
        ):
            with self.subTest(binding=binding):
                script = self.script("spoofed.sh", binding + read)
                ran = subprocess.run(
                    ["/bin/bash", str(script)], cwd=self.temp, capture_output=True, text=True, check=False
                )
                self.assertEqual((0, "ran spoofed\n"), (ran.returncode, ran.stdout), ran.stderr)  # measured
        script = self.script("env.sh", f'listing=$(env PATH={spoof} git ls-files) || exit 1\necho "ran ${{listing}}"\n')
        ran = subprocess.run(["/bin/bash", str(script)], cwd=self.temp, capture_output=True, text=True, check=False)
        self.assertEqual((0, "ran spoofed\n"), (ran.returncode, ran.stdout), ran.stderr)  # measured
        for child in ("cat <(x=$(false) || exit 1)\n", "tee >(x=$(false) || exit 1) < /dev/null\n"):
            with self.subTest(child=child):
                script = self.script("child.sh", child + "echo ran\n")
                ran = subprocess.run(
                    ["/bin/bash", str(script)], cwd=self.temp, capture_output=True, text=True, check=False
                )
                self.assertEqual((0, "ran\n"), (ran.returncode, ran.stdout), ran.stderr)  # measured: the parent goes on
        bindings = (
            "refuse() { exit 2; }\n"  # 3
            "export 'PATH=/tmp/x:$PATH'\n"  # 4: the auditor's quoted word
            "builtin export PATH=/tmp/x\n"  # 5: the auditor's forwarded word
            'export "PATH=/tmp/x:$PATH"\n'  # 6: the leading literal spells the write, and the word has no known text (twice)
            'export "$binding"\n'  # 7
            "declare -x PATH=/tmp/x\n"  # 8: an Assign
            "env PATH=/tmp/x git ls-files\n"  # 9: a word of any command
            "env -i PATH=/tmp/x git ls-files\n"  # 10
            "command env PATH=/tmp/x true\n"  # 11: through a forwarder
            "builtin command export PATH=/tmp/x\n"  # 12: through a chain of forwarders
            "readonly 'PATH[0]=/tmp/x'\n"  # 13: an index
            "typeset 'BASH_CMDS[git]=/tmp/x/git'\n"  # 14
            "f() { local 'PATH+=:/tmp/x'; }\n"  # 15: an append
            "export -n 'BASH_ALIASES[git]=true'\n"  # 16
            'env "$@" git ls-files\n'  # 17: accepted since round 18: an expansion handed to an external command
            "GIT_ISOLATED_ENV=(GIT_CONFIG_NOSYSTEM=1 PATH=/tmp/x)\n"  # 18: the assignment, and the element (twice)
            'GIT_ISOLATED_ENV+=("$extra")\n'  # 19
            "GIT_ISOLATED_ENV[0]=PATH=/tmp/x\n"  # 20: the assignment, and the value (twice)
            "GIT_ISOLATED_ENV=(git)\n"  # 21
            'export "${OTHER[@]}"\n'  # 22: a word with no known text
            'export "${GIT_ISOLATED_ENV[0]}"\n'  # 23
            'export "${GIT_ISOLATED_ENV[@]:-}"\n'  # 24
            "x=$(false) || refuse\n"  # 25: accepted
            "export GIT_CONFIG_NOSYSTEM=1\n"  # 26: accepted
            "g() { local status=0; declare -r y=1; local -- z; }\n"  # 27: accepted
            "export PATH\n"  # 28: a finding since round 18: the bare name is a write
            "declare +x -a GIT_ISOLATED_ENV GIT_ISOLATED_ARGS\n"  # 29: not the library's exact line (twice)
            "GIT_ISOLATED_ENV=(GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1)\n"  # 30: not the library's exact array
            "GIT_ISOLATED_ENV+=(GIT_TERMINAL_PROMPT=0)\n"  # 31
            '( export "${GIT_ISOLATED_ENV[@]}" && exec git "${GIT_ISOLATED_ARGS[@]}" "$@" )\n'  # 32: outside git-isolated.sh
            "export -f refuse\n"  # 33: a write to a guarded name
            "env GIT_CONFIG_NOSYSTEM=1 true\n"  # 34: accepted
            'env "${GIT_ISOLATED_ENV[@]}" true\n'  # 35: accepted
        )
        twice = (6, 18, 20, 29)
        expected = [(line, "binding") for line in (*range(4, 17), *range(18, 25), *range(28, 34), *twice)]
        result = self.assert_findings(bindings, expected)
        path = "a write to `PATH` (the directories bash searches for `git`, `find`, `ls` and every other command word)"
        unknown = "a write to any guarded name: a word of `export` with no known text, which may spell an assignment to any of them"
        array = "a write to `GIT_ISOLATED_ENV` (the array git_isolated of git-isolated.sh exports word by word before it execs git)"
        for line, message in (
            (4, f"{path}: a word spelling an assignment, `PATH=…`, in the declaration `export`"),
            (5, f"{path}: a word spelling an assignment, `PATH=…`, in the command `builtin`"),
            (6, f"{path}: a word spelling an assignment, `PATH=…`, in the declaration `export`"),
            (6, f"{unknown}, in the declaration `export`"),
            (7, f"{unknown}, in the declaration `export`"),
            (8, f"{path}: an assignment, in the declaration `declare`"),
            (9, f"{path}: a word spelling an assignment, `PATH=…`, in the command `env`"),
            (11, f"{path}: a word spelling an assignment, `PATH=…`, in the command `command`"),
            (12, f"{path}: a word spelling an assignment, `PATH=…`, in the command `builtin`"),
            (13, f"{path}: a word spelling an assignment, `PATH[0]=…`, in the declaration `readonly`"),
            (
                14,
                "a write to `BASH_CMDS` (the hash table of bash 4, which `hash -p` writes): a word spelling an assignment, `BASH_CMDS[git]=…`, in the declaration `typeset`",
            ),
            (15, f"{path}: a word spelling an assignment, `PATH+=…`, in the declaration `local`"),
            (18, f"{array}: an assignment, in an assignment"),
            (18, f"{path}: a word spelling an assignment, `PATH=…`, in an assignment"),
            (19, f"{array}: an assignment, in an assignment"),
            (21, f"{array}: an assignment, in an assignment"),
            (22, f"{unknown}, in the declaration `export`"),
            (24, f"{unknown}, in the declaration `export`"),
            (28, f"{path}: an assignment with no value, or the bare name, in the declaration `export`"),
            (32, f"{unknown}, in the declaration `export`"),
            (
                33,
                "a write to `refuse` (a refusal function a `||` branch calls (rule a, form ii)): an assignment with no value, or the bare name, in the declaration `export`",
            ),
        ):
            self.assertIn(f":{line}: binding: {message}", result.stdout)
        self.assertNotIn(":17:", result.stdout)
        children = (
            "cat <(x=$(false) || exit 1)\n"  # 3: the auditor's line
            "tee >(x=$(false) || exit 1)\n"  # 4
            "while read -r l; do :; done < <(git ls-files)\n"  # 5: a producer in a child, whatever follows it
            "cat <(if x=$(false); then :; fi)\n"  # 6
            "cat <(y=$(false))\n"  # 7: untested, a finding anywhere
            "cat <(git ls-files > l 2> e; [[ ! -s e ]] || exit 1)\n"  # 8: the test runs in the child too
            "x=$(cat <(y=$(false) || exit 1)) || exit 1\n"  # 9: the outer read is accepted, the inner is the finding
            "git ls-files > l 2> >(tee e) || exit 1\n"  # 10: a substitution is no captured file
            "ls <(true) > l 2> e || exit 1\n"  # 11: a word with no known text; no later test
            "diff <(sort a) <(sort b)\n"  # 12: accepted: no tested read inside
            "cat <(echo x) > /dev/null\n"  # 13
        )
        expected = [(3, "substitution"), (4, "substitution"), (5, "producer"), (6, "substitution"), (7, "substitution")]
        expected += [(8, "producer"), (9, "substitution"), (10, "producer"), (11, "producer")]
        result = self.assert_findings(children, expected)
        opened = "the tested read runs in a process substitution (`<(…)` or `>(…)`) opened at line {}, whose failure the parent never sees"
        for line, message in (
            (3, opened.format(3)),
            (4, opened.format(4)),
            (5, "the producer runs in a process substitution opened at line 5, whose failure the parent never sees"),
            (6, opened.format(6)),
            (8, "the producer runs in a process substitution opened at line 8, whose failure the parent never sees"),
            (9, opened.format(9)),
        ):
            self.assertIn(f":{line}: {'producer' if 'producer' in message else 'substitution'}: ", result.stdout)
            self.assertIn(message, result.stdout)
        result = self.assert_findings("cat <(set -euo pipefail)\nx=$(a) || exit 1\n", [(1, "prologue")], prologue="")
        self.assertIn("the one at line 2 runs in a process substitution opened at line 2, a child shell", result.stdout)

    def test_the_round_18_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The two P2 of the ba8eb39d audit, which that head read as clean: `PATH=` has no Value in shfmt's tree, so
        the guard that asked for one passed it, and `export 'GIT_ISOLATED_ENV=PATH=/tmp/x'` assigned the array the
        lint trusts by name through a quoted word, after which the accepted `export "${GIT_ISOLATED_ENV[@]}"` set
        PATH (measured below: the spoofed git runs). Rounds 14 to 17 each added one more detection; round 18 replaces
        the shape: GUARDED_NAMES is one closed set, a write is any Assign to one (a Value or not), a loop variable, an
        assigning expansion, a word in any position whose literal parts spell `name=` or name a guarded variable, a
        declaration word with no known text, an attribute option, or an unknown word where bash evaluates arithmetic
        (measured below: `(( $y, 1 ))` and `[[ $y -eq 1 ]]` with `y='PATH=1'` run the spoofed git), and only the
        exact statement texts of ACCEPTED_WRITES, in their files, are accepted."""
        spoof = self.temp / "1"  # `PATH=1` names this directory, relative to the cwd the scripts run in
        spoof.mkdir()
        (spoof / "git").write_text("#!/bin/sh\necho spoofed\n")
        (spoof / "git").chmod(0o755)
        read = 'listing=$(git ls-files) || exit 1\necho "ran ${listing}"\n'
        for binding in (
            f"export 'GIT_ISOLATED_ENV=PATH={spoof}'\nexport \"${{GIT_ISOLATED_ENV[@]}}\"\n",  # the auditor's line
            "y='PATH=1'\n(( $y, 1 ))\n",
            "y='PATH=1'\n[[ $y -eq 1 ]]\n",
            "y='PATH=1'\na[$y]=1\n",
            "declare -i x\ny='PATH=1'\nx=$y\n",
        ):
            with self.subTest(binding=binding):
                script = self.script("spoofed.sh", binding + read)
                ran = subprocess.run(
                    ["/bin/bash", str(script)], cwd=self.temp, capture_output=True, text=True, check=False
                )
                self.assertEqual((0, "ran spoofed\n"), (ran.returncode, ran.stdout), ran.stderr)  # measured
        writes = (
            "PATH=\n"  # 3: the auditor's line: no Value, a write to the empty string
            "export 'GIT_ISOLATED_ENV=PATH=/tmp/x'\n"  # 4: the auditor's line: the array, and PATH named (twice)
            'export "${GIT_ISOLATED_ENV[@]}"\n'  # 5: a declaration word with no known text, outside git-isolated.sh
            "IFS=$'\\n'\n"  # 6
            "for PATH in a; do :; done\n"  # 7
            "read -r PATH\n"  # 8
            "printf -v PATH x\n"  # 9
            "declare -a GIT_ISOLATED_ENV=(x)\n"  # 10
            "env PATH=x git ls-files\n"  # 11
            "export PATH=/tmp/x\n"  # 12: the rounds 14 to 17 table, each a `binding` now
            "export 'PATH=/tmp/x:$PATH'\n"  # 13
            "builtin export PATH=/tmp/x\n"  # 14
            "declare -x PATH=/tmp/x\n"  # 15
            "readonly 'PATH[0]=/tmp/x'\n"  # 16
            "typeset 'BASH_CMDS[git]=/tmp/x/git'\n"  # 17
            "f() { local 'PATH+=:/tmp/x'; }\n"  # 18
            "GIT_ISOLATED_ENV=(GIT_CONFIG_NOSYSTEM=1 PATH=/tmp/x)\n"  # 19: twice
            'GIT_ISOLATED_ENV+=("$extra")\n'  # 20
            "GIT_ISOLATED_ENV[0]=PATH=/tmp/x\n"  # 21: twice
            "export PATH\n"  # 22: the bare name
            "unset PATH\n"  # 23: the name as a word, in any command
            "mapfile -t PATH\n"  # 24
            "local -n ref=PATH\n"  # 25: the name, and the nameref option (twice)
            "((PATH = 1))\n"  # 26: arithmetic: the name, and the operand (twice since round 20)
            "let 'PATH = 1'\n"  # 27: twice
            "x=${a[PATH=1]}\n"  # 28: twice
            ': "${PATH:=/tmp/x}"\n'  # 29: an assigning expansion
            "[[ $y -eq 1 ]]\n"  # 30: an operand where bash evaluates arithmetic (an expansion; a name since round 20)
            "a[$y]=1\n"  # 31
            "declare -i n\n"  # 32: the integer attribute
            "bash -c 'cd /; PATH=/tmp/x git ls-files'\n"  # 33: text handed to another program
            "export BASH_ENV=/tmp/x/env\n"  # 34: a variable bash reads
            "LEVER_DIR=/tmp/x\n"  # 35: the directory the accepted source reads from
            "select PATH in a; do :; done\n"  # 36
            "coproc PATH { :; }\n"  # 37
            "unset 'a[PATH=1]'\n"  # 38
            "PATH= git ls-files\n"  # 39: a prefix with no Value (and the producer, rule b)
            "BASH_ALIASES[fail]=true\n"  # 40: the name, and the subscript as an arithmetic operand (twice since round 20)
            "export -f refuse\n"  # 41
            "alias fail=true\n"  # 42: spells a write (and the alias, rule f's shadow reading)
            "g() { local status=0; declare -r y=1; local -- z; }\n"  # 43: accepted from here to 46
            "export GIT_CONFIG_NOSYSTEM=1\n"  # 44
            "[[ $# -eq 1 ]]\n"  # 45: a finding since round 20: a row's shape, but not in a row's file
            "((count == 1))\n"  # 46
            "IFS= read -r line\n"  # 47: a lever's text, but not in a lever's file
            "IFS=$'\\t' read -r state base <<< \"${view}\"\n"  # 48
            'env "${GIT_ISOLATED_ENV[@]}" true\n'  # 49: accepted from here on: an external command's argument
            'unset -v "${name}"\n'  # 50: a name an expansion carries into a builtin that is no declaration
            "printf -v \"$3\" '%s' ''\n"  # 51
            "x=$(a) || exit 1\n"  # 52
        )
        twice = (4, 19, 21, 25, 26, 27, 28, 40)
        expected = [(line, "binding") for line in (*range(3, 43), *twice, 45, 46, 47, 48)]
        expected += [(39, "producer"), (42, "shadow")]
        result = self.assert_findings(writes, expected)
        path = "a write to `PATH` (the directories bash searches for `git`, `find`, `ls` and every other command word)"
        named = (
            "a word spelling its name (an argument of `read`, `printf -v`, `unset` or `mapfile`, a nameref's value, an "
            "arithmetic operand, text handed to another program, a message)"
        )
        unknown = (
            "a write to any guarded name: an operand where bash evaluates arithmetic that is not digits and operators "
            "alone (a name, which bash evaluates recursively, a parameter, an expansion)"
        )
        for line, message in (
            (3, f"{path}: an assignment with no value, or the bare name, in an assignment"),
            (
                4,
                "a write to `GIT_ISOLATED_ENV` (the array git_isolated of git-isolated.sh exports word by word before it "
                "execs git): a word spelling an assignment, `GIT_ISOLATED_ENV=…`, in the declaration `export`",
            ),
            (4, f"{path}: {named}, in the declaration `export`"),
            (
                5,
                "a write to any guarded name: a word of `export` with no known text, which may spell an assignment to any "
                "of them, in the declaration `export`",
            ),
            (
                6,
                "a write to `IFS` (the characters word splitting and `read` split on (`for name in ${names}` of "
                "git_env_scrub)): an assignment, in an assignment",
            ),
            (7, f"{path}: the variable of a `for` or `select`, in a `for`"),
            (8, f"{path}: {named}, in the command `read`"),
            (9, f"{path}: {named}, in the command `printf`"),
            (11, f"{path}: a word spelling an assignment, `PATH=…`, in the command `env`"),
            (23, f"{path}: {named}, in the command `unset`"),
            (25, f"{path}: {named}, in the declaration `local`"),
            (
                25,
                "a write to any guarded name: the option `-n` of `local`, under which a later assignment evaluates its "
                "value as arithmetic (`-i`) or writes the variable its value names (`-n`), in the declaration `local`",
            ),
            (26, f"{path}: {named}, in an arithmetic command"),
            (
                29,
                f"{path}: an expansion that assigns its parameter (`${{name=…}}`, `${{name:=…}}`), in the command `:`",
            ),
            (
                30,
                f"{unknown}, in a `[[ ]]` test; the statement is not an accepted arithmetic statement of the adopted "
                "levers and libraries (ACCEPTED_ARITHMETIC)",
            ),
            (31, f"{unknown}, in an assignment"),
            (32, "a write to any guarded name: the option `-i` of `declare`, under which a later assignment"),
            (33, f"{path}: {named}, in the command `bash`"),
            (
                34,
                "a write to `BASH_ENV` (the file every non-interactive bash reads before its script (a child `bash` of a "
                "lever)): an assignment, in the declaration `export`",
            ),
            (36, f"{path}: the variable of a `for` or `select`, in a `for`"),
            (39, f"{path}: an assignment with no value, or the bare name, in the command `git`"),
            (
                47,
                "a write to `IFS` (the characters word splitting and `read` split on (`for name in ${names}` of "
                "git_env_scrub)): an assignment with no value, or the bare name, in the command `read`; the statement is "
                "not an accepted write of the adopted levers and libraries (ACCEPTED_WRITES)",
            ),
        ):
            self.assertIn(f":{line}: binding: {message}", result.stdout)
        # The allowlist is exact: a row's text passes in a file of the row's name alone, and one character off, or the
        # same text in another file, is a finding.
        accepted = "while IFS=$'\\t' read -r bucket name; do :; done <<< \"${x}\"\n"
        for name, body, findings_expected in (
            ("pr-merge.sh", accepted, []),
            ("pr-merge.sh", accepted.replace("bucket name", "bucket names"), [(3, "binding")]),
            ("pr-audit.sh", accepted, [(3, "binding")]),
            ("read-lib.sh", "f() {\n    LEVER_DIR=${dir}\n}\n", []),
            ("read-lib.sh", "f() {\n    LEVER_DIR=${dir2}\n}\n", [(4, "binding")]),
            ("other.sh", "f() {\n    LEVER_DIR=${dir}\n}\n", [(4, "binding")]),
            ("read-lib.sh", "f() { LEVER_DIR=${dir}; }\n", [(3, "binding")]),  # the `;` is part of the statement's text
        ):
            with self.subTest(name=name, body=body):
                result = self.run_check(self.script(name, body))
                self.assertEqual("", result.stderr)
                self.assertEqual(sorted(findings_expected), findings(result), result.stdout)

    def test_the_round_20_mutations_are_findings_named_by_line_and_rule(self) -> None:
        """The two P2 of the fb2774e9 audit, which that head read as clean: a guarded name was matched in each literal
        part of a word alone, so `printf -v PA"TH" "$1"` spelled PATH across two parts and passed while /bin/bash 3.2
        set PATH and ran the spoofed git (measured below); and only an operand with no known text was a write where
        bash evaluates arithmetic, so `y=$1; (( y, 1 ))` passed while bash evaluated `y` recursively, read `PATH=1`
        as an assignment and ran the spoofed git (measured below, with `[[ y -eq 1 ]]`, `a[y]=1`, `let 'y + 1'` and
        `declare -i n; n=y`). Round 20 matches the name in the concatenation of every literal part, quotes removed and
        in order, and in each part alone, and reads every arithmetic operand that is not digits, operators and
        whitespace alone as a write, accepted only by the exact statement texts of ACCEPTED_ARITHMETIC in their files
        (the 44 statements measured on the adopted set); `$#` and `${#name}` are rows there, not a reading of which
        parameters are numbers."""
        spoof = self.temp / "1"  # `PATH=1` names this directory, relative to the cwd the scripts run in
        spoof.mkdir()
        (spoof / "git").write_text("#!/bin/sh\necho spoofed\n")
        (spoof / "git").chmod(0o755)
        read = 'listing=$(git ls-files) || exit 1\necho "ran ${listing}"\n'
        for binding, argument in (
            ('printf -v PA"TH" "$1"\n', "1"),  # the auditor's line
            ("y=$1; (( y, 1 ))\n", "PATH=1"),  # the auditor's line
            ("y=$1; [[ y -eq 1 ]]\n", "PATH=1"),
            ("y=$1; a[y]=1\n", "PATH=1"),
            ("y=$1; let 'y + 1'\n", "PATH=1"),
            ("declare -i n; y=$1; n=y\n", "PATH=1"),
        ):
            with self.subTest(binding=binding):
                script = self.script("spoofed.sh", binding + read)
                ran = subprocess.run(
                    ["/bin/bash", str(script), argument], cwd=self.temp, capture_output=True, text=True, check=False
                )
                self.assertEqual((0, "ran spoofed\n"), (ran.returncode, ran.stdout), ran.stderr)  # measured
        probes = (
            'printf -v PA"TH" "$1"\n'  # 3: the auditor's line: the name across two literal parts
            'PA"TH"=x\n'  # 4: the leading parts were joined before; the token is now found in the joined text too
            "printf -v PA'TH' x\n"  # 5
            "'PA'TH=1\n"  # 6
            "y=$1; (( y, 1 ))\n"  # 7: the auditor's line: a bare name bash evaluates recursively
            "[[ y -eq 1 ]]\n"  # 8
            "a[y]=1\n"  # 9
            "let 'y + 1'\n"  # 10
            "declare -i n; n=y\n"  # 11: the `-i` option (round 18); the tree shows no arithmetic in `n=y` itself
            "exit $((128 + $2))\n"  # 12: a row's text, but not in a row's file
            "[[ ${template_entries} -gt 0 ]]\n"  # 13
            "[[ $# -eq 1 ]]\n"  # 14
            "((count == 1))\n"  # 15
            "((${#a[@]}))\n"  # 16: a length is a parameter, not a number this walk reads
            "for ((i = 0; i < 3; i++)); do :; done\n"  # 17: a C-style `for`
            "x=${a[i]}\n"  # 18: a subscript
            "x=${s:1:n}\n"  # 19: a slice
            "[[ -v 'a[y]' ]]\n"  # 20: a name test's subscript
            "((1 + 2))\n"  # 21: accepted from here on: digits, operators and whitespace alone
            "x=${a[@]}\n"  # 22
            "x=${a[*]}\n"  # 23
            "let '1 + 2'\n"  # 24
            "exit $((128 + 2))\n"  # 25
            "echo PA TH\n"  # 26: two words, neither the name
            "x=$(a) || exit 1\n"  # 27
        )
        result = self.assert_findings(probes, [(line, "binding") for line in range(3, 21)])
        path = "a write to `PATH` (the directories bash searches for `git`, `find`, `ls` and every other command word)"
        named = (
            "a word spelling its name (an argument of `read`, `printf -v`, `unset` or `mapfile`, a nameref's value, an "
            "arithmetic operand, text handed to another program, a message)"
        )
        operand = (
            "a write to any guarded name: an operand where bash evaluates arithmetic that is not digits and operators "
            "alone (a name, which bash evaluates recursively, a parameter, an expansion)"
        )
        accepted = (
            "the statement is not an accepted arithmetic statement of the adopted levers and libraries "
            "(ACCEPTED_ARITHMETIC)"
        )
        for line, message in (
            (3, f"{path}: {named}, in the command `printf`; the statement is not an accepted write"),
            (4, f"{path}: a word spelling an assignment, `PATH=…`, in the command `PATH=x`"),
            (5, f"{path}: {named}, in the command `printf`"),
            (6, f"{path}: a word spelling an assignment, `PATH=…`, in the command `PATH=1`"),
            (7, f"{operand}, in an arithmetic command; {accepted}"),
            (8, f"{operand}, in a `[[ ]]` test; {accepted}"),
            (9, f"{operand}, in an assignment; {accepted}"),
            (10, f"{operand}, in a `let`; {accepted}"),
            (11, "a write to any guarded name: the option `-i` of `declare`, under which a later assignment"),
            (12, f"{operand}, in the command `exit`; {accepted}"),
            (16, f"{operand}, in an arithmetic command; {accepted}"),
            (17, f"{operand}, in a `for`; {accepted}"),
            (18, f"{operand}, in an assignment; {accepted}"),
            (19, f"{operand}, in an assignment; {accepted}"),
            (20, f"{operand}, in a `[[ ]]` test; {accepted}"),
        ):
            self.assertIn(f":{line}: binding: {message}", result.stdout)
        # The allowlist is exact: a row's text passes in a file of the row's name alone; one character off, or the same
        # text in another file, is a finding; the two rows round 18 held in ACCEPTED_WRITES hold here now.
        for name, body, findings_expected in (
            ("pr-audit.sh", '[[ $# -eq 1 ]] || refuse "${usage}"\n', []),
            ("pr-merge.sh", '[[ $# -eq 1 ]] || refuse "${usage}"\n', [(3, "binding")]),
            ("pr-audit.sh", '[[ $# -eq 2 ]] || refuse "${usage}"\n', [(3, "binding")]),
            ("pr-audit.sh", "exit $((128 + $2))\n", []),
            ("pr-audit.sh", "exit $((128 + $1))\n", [(3, "binding")]),
            ("pr-audit.sh", '[[ ${template_entries} -gt 0 ]] || refuse "${template} has no filesystem entries"\n', []),
            ("records-sync.sh", "((status == 0)) || fail x\n", []),
            ("read-lib.sh", "((status == 0)) || return 1\n", [(3, "binding")]),
            ("records-sync.sh", "while (($#)); do shift; done\n", []),  # the `;` is part of the statement's text
            ("records-sync.sh", "(($#)) || exit 1\n", [(3, "binding")]),
        ):
            with self.subTest(name=name, body=body):
                result = self.run_check(self.script(name, body))
                self.assertEqual("", result.stderr)
                self.assertEqual(sorted(findings_expected), findings(result), result.stdout)

    def test_every_name_the_lint_compares_against_is_a_guarded_name(self) -> None:
        """GUARDED_NAMES cannot drift from the lint: every identifier-shaped string the walk compares a value against
        (a literal, or a module constant holding strings, on either side of `==`, `!=`, `in` or `not in`) is a guarded
        name, a kind or field of the contract table, or one of NOT_NAMES with its reason; and the constants the rules
        read names from are subsets of the guarded set. The constants are read by executing the walk's module-level
        assignments alone."""
        source = re.search(r"cat << 'PY'\n(.*?)\nPY\n", CHECK.read_text(), re.DOTALL)
        assert source is not None
        module = ast.parse(source.group(1))
        assigns: list[ast.stmt] = []
        for node in module.body:  # the constants come before the first function; `walk = Walk(...)` comes after
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                break
            if isinstance(node, ast.Assign):
                assigns.append(node)
        namespace: dict[str, object] = {"re": re, "sys": types.SimpleNamespace(argv=["", "", ""])}
        exec(compile(ast.Module(body=assigns, type_ignores=[]), "walk", "exec"), namespace)
        guarded = namespace["GUARDED_NAMES"]
        assert isinstance(guarded, dict)
        for name, reason in guarded.items():
            self.assertTrue(reason and reason[0].islower(), f"{name} needs a one-line reason")

        def values(value: object) -> set[str]:
            if isinstance(value, str):
                return {value}
            if isinstance(value, dict):
                return set().union(*(values(key) for key in value))
            if isinstance(value, (tuple, list, set, frozenset)):
                return set().union(*(values(item) for item in value))
            return set()

        def strings(node: ast.AST) -> set[str]:
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                return {node.value}
            if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
                return set().union(*(strings(item) for item in node.elts))
            if isinstance(node, ast.Name) and node.id in namespace:
                return values(namespace[node.id])
            if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id in namespace:
                if isinstance(node.slice, ast.Constant):
                    return values(namespace[node.value.id][node.slice.value])  # type: ignore[index]
            return set()

        compared: set[str] = set()
        for node in ast.walk(module):
            if isinstance(node, ast.Compare) and all(
                isinstance(op, (ast.Eq, ast.NotEq, ast.In, ast.NotIn)) for op in node.ops
            ):
                for operand in (node.left, *node.comparators):
                    compared |= strings(operand)
        names = {text for text in compared if IDENT.fullmatch(text) and (len(text) > 1 or text == ".")}
        table = set(contract.TABLE)
        for row in contract.TABLE.values():
            table |= {segment for field in row.fields for segment in field.split(".")}
            table |= {row.marker} if row.marker else set()
        self.assertEqual(
            set(), names - set(guarded) - table - set(NOT_NAMES), "compared, neither guarded nor classified"
        )
        self.assertEqual(set(), set(NOT_NAMES) - names, "a classified word the lint no longer compares against")
        self.assertEqual(set(), set(NOT_NAMES) & set(guarded), "a classified word that is guarded")
        for constant in ("REFUSAL_NAMES", "TERMINATORS", "WRITERS", "REBINDERS", "DECLARERS"):
            self.assertLessEqual(values(namespace[constant]), set(guarded), constant)
        for constant in ("READER", "LIBRARY_DIR"):
            self.assertIn(namespace[constant], guarded, constant)
        self.assertIn(namespace["PROLOGUE_WORDS"][0], guarded)  # type: ignore[index]
        for name in ("PATH", "BASH_ALIASES", "BASH_CMDS", "GIT_ISOLATED_ENV", "GIT_ISOLATED_ARGS", "LEVER_DIR"):
            self.assertIn(name, guarded)
        for name in (
            "BASH_ENV",
            "ENV",
            "SHELLOPTS",
            "BASHOPTS",
            "IFS",
            "CDPATH",
            "BASH_LOADABLES_PATH",
            "EXECIGNORE",
            "PS4",
        ):
            self.assertIn(name, guarded)
        # The accepted writes and arithmetic statements name files of the adopted set only (the lint's own file among
        # the arithmetic ones), and every row has a reason.
        adopted = set(namespace["LEVERS"]) | set(namespace["LIBRARIES"])  # type: ignore[arg-type]
        rows = namespace["ACCEPTED_WRITES"]
        assert isinstance(rows, tuple)
        self.assertEqual(28, len(rows))
        for files, text, reason in rows:
            self.assertLessEqual(set(files), adopted, text)
            self.assertTrue(text and reason, text)
        arithmetic = namespace["ACCEPTED_ARITHMETIC"]
        assert isinstance(arithmetic, tuple)
        self.assertEqual(60, len(arithmetic))
        for files, text, reason in arithmetic:
            self.assertLessEqual(set(files), adopted | {CHECK.name}, text)
            self.assertTrue(text and reason, text)

    def test_the_walk_has_one_descent_and_every_scan_steps_by_it(self) -> None:
        """One function of the embedded walk, children, reads a node's values, through without_literal_body; every
        (which definitions, comments and refusal_break iterate) and Walk.visit descend by children alone. A second
        traversal would read a literal heredoc body as code, as definitions and the allow-comment scan did before
        round 12 (without_positions copies a word's parts for an equality test and finds nothing)."""
        source = re.search(r"cat << 'PY'\n(.*?)\nPY\n", CHECK.read_text(), re.DOTALL)
        assert source is not None
        functions = {
            node.name: node for node in ast.walk(ast.parse(source.group(1))) if isinstance(node, ast.FunctionDef)
        }

        def calls(function: ast.FunctionDef) -> set[str]:
            """The names called in the function: `name` for name(...), `.attr` for x.attr(...)."""
            names = set()
            for node in ast.walk(function):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    names.add(node.func.id)
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    names.add("." + node.func.attr)
            return names

        called = {name: calls(function) for name, function in functions.items()}
        self.assertEqual(["children"], [name for name, names in called.items() if ".values" in names])
        self.assertEqual(["children"], [name for name, names in called.items() if "without_literal_body" in names])
        self.assertEqual({"every", "visit"}, {name for name, names in called.items() if "children" in names})
        self.assertEqual(
            {"definitions", "comments", "refusal_break"}, {name for name, names in called.items() if "every" in names}
        )

    def test_the_walk_refuses_fixtures_in_which_it_sees_none_of_its_kinds(self) -> None:
        """The contract holds (every node is still in each tree), but each tree is the literal body of a quoted
        heredoc, which the walk skips: it sees no assignment and no substitution in the fixtures and refuses before
        the listed file is read, whose plain assignment therefore yields no finding line."""
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        for tool in ("bash", "sh", "awk", "python3", "cat", "sed"):
            (bin_dir / tool).symlink_to(shutil.which(tool))
        answers = "input=$(/bin/cat)\n"
        for fixture in CAPTURES:
            hidden = self.temp / f"{fixture.name}.hidden.json"
            hidden.write_text(hidden_tree(captures()[fixture.name]))
            answers += f'[ "$input" = "$(/bin/cat "{fixture}")" ] && exec /bin/cat "{hidden}"\n'
        fake = bin_dir / "shfmt"
        fake.write_text(
            "#!/bin/sh\n"
            f'[ "$1" = --version ] && {{ echo v{pinned_version()}; exit 0; }}\n'
            f'{answers}exec /bin/cat "{CAPTURES[ROOT / "tests/fixtures/shfmt-json/contract.sh"]}"\n'
        )
        fake.chmod(0o755)
        lever = self.script("lever.sh", "x=$(a)\n")

        result = self.run_check(lever, env={"PATH": str(bin_dir), "HOME": str(self.temp)})

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("the walk visited no", result.stderr)
        self.assertIn("in the contract fixtures", result.stderr)
        self.assertEqual("", result.stdout)

    def test_the_lint_passes_its_own_rules(self) -> None:
        result = self.run_check(CHECK)
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def test_the_library_and_the_five_levers_are_clean(self) -> None:
        """The enforced set: zero findings over read-lib.sh, git-isolated.sh and the five levers, nothing printed."""
        result = self.run_check(LIB, GIT_LIB, *LEVERS)
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))


if __name__ == "__main__":
    unittest.main()
