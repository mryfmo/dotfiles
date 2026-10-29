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
had made the file's real `refuse` a duplicate).
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_shfmt_json_contract import CAPTURES, captures, hidden_tree, pinned_version  # noqa: E402

CHECK = ROOT / "scripts/ci/producer-status-check.sh"
TABLE = ROOT / "scripts/ci/status-blind-producers.tsv"
LIB = ROOT / "scripts/orchestrator/read-lib.sh"
LEVERS = tuple(
    ROOT / "scripts/orchestrator" / name
    for name in ("records-sync.sh", "pr-audit.sh", "pr-merge.sh", "pr-threads-check.sh", "pr-body-edit.sh")
)
ANSI_C_HEREDOC = ROOT / "tests/fixtures/shfmt-json/heredoc-ansi-c-delimiter"
PROLOGUE = "set -euo pipefail\n"
PRODUCERS = ("git ls-files", "git config -f", "git config --file", "find", "ls")
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
            ("n=$((1 + $(a))) || exit 1", "substitution"),
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
        every name outside the allowlist `refuse`, `fail` (round 12), is a finding naming the name, whatever its body."""
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
        result = self.assert_findings(shadowed, [(6, "substitution")])
        self.assertIn(
            "a call of `exit`, defined at line 3, a name that is not a refusal name (`refuse`, `fail`)",
            result.stdout,
        )
        # A top-level function named `echo` takes that name from the grammar too: `echo x >&2` in a body is then a call.
        shadowed = "echo() {\n    :\n}\nfail() {\n    echo no >&2\n    exit 1\n}\nx=$(a) || fail\n"
        result = self.assert_findings(shadowed, [(10, "substitution")])
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
        result = self.assert_findings("IFS= read -r x < unreadable || exit 1\n", [(3, "read")])
        self.assert_findings("'read' -r x < unreadable || exit 1\n", [(3, "read")])
        self.assertIn("read_file", result.stdout)
        clean = 'while IFS= read -r l; do :; done < file\nread -r a b <<< "${v}"\nread -r -p "x" answer || exit 1\n'
        self.assert_findings(clean, [])

    def test_the_allow_comment_exempts_a_b_and_d_with_a_reason_and_is_a_finding_without_one(self) -> None:
        allowed = (
            "x=$(a) # producer-status: allow the status is read from the file below\n"
            "git ls-files > l # producer-status: allow the listing is advisory\n"
            "IFS= read -r y < f # producer-status: allow a reason\n"
        )
        self.assert_findings(allowed, [])
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
        """The enforced set: zero findings over read-lib.sh and the five levers, nothing printed."""
        result = self.run_check(LIB, *LEVERS)
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))


if __name__ == "__main__":
    unittest.main()
