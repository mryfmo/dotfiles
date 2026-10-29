#!/usr/bin/env python3
"""Exercise scripts/ci/producer-status-check.sh, the lint over the grammar of command substitutions, the status-blind
producers, the prologue and `read` from a file (regime-cutover U112, plan P-21).

The fixtures reproduce the measured shapes of research 01 section 2.5 that a lint can see: a jq error read as "no
hooks" (shape 1, rule a), the bare `git ls-files` without its stderr capture (shape 3, rule b), `read x < unreadable`
(shape 4, rule d) and `local x=$(false)` (shape 5, rule a); the reader halves of shapes 2, 3 and 4 are in
tests/unit/test_read_lib.py. The lint needs shfmt on PATH (the pinned version, which the contract checks first). The
enforcement test runs it over the library and the five levers: that test, not a Makefile target, holds them to zero
findings.
"""

from __future__ import annotations

import os
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
        cases: list[tuple] = [  # (the lines, the rule of the finding or None, the finding's line within the case)
            ("x=$(a) || fail", None),
            ('x="$(a)" || fail', None),
            ("x=`a` || fail", None),
            ("if ! x=$(a); then exit 1; fi", None),
            ("if x=$(a); then :; fi", None),
            ("while x=$(a); do break; done", None),
            ("until x=$(a); do break; done", None),
            ("if true; then :; elif x=$(a); then :; fi", None),
            ("x=$(a) || { echo no; exit 1; }", None),
            ("x=$(a) || x=''", None),
            ("x=$(a) || exit 2", None),
            ("f() { x=$(a) || return 1; }", None),
            ("g() { local y; y=$(a) || return 1; }", None),
            ("x=$(a) || true", "substitution"),
            ("x=$(a) || :", "substitution"),
            ("x=$(a) || false", "substitution"),
            ("x=$(a) && echo ok", "substitution"),
            ("x=$(a)", "substitution"),
            ("x=$(a)/suffix || fail", "substitution"),
            ("x=prefix$(a) || fail", "substitution"),
            ("a=$(x) b=$(y) || exit 1", "substitution"),
            ("x=$(a) || y=$(b) || exit 1", "substitution"),
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
            text, rule = case[0], case[1]
            if rule is not None:
                expected.append((3 + len(body_lines) + (case[2] if len(case) > 2 else 0), rule))
            body_lines.extend(text.split("\n"))
        self.assert_findings("\n".join(body_lines) + "\n", expected)

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
        `2> /dev/null`, `2>&1`, a capture no later `[[ ! -s ]]` tests, a test of another file, a test in another
        statement list or before the call are findings; the capture with its test, in either quoting, the other rows
        with theirs, and the call through read_listing are not."""
        capture = "git ls-files -z > list 2> err || exit 1\n"
        test = "[[ ! -s err ]] || exit 1\n"
        clean = {
            "the capture and its test": capture + test,
            "the test deeper in the list": capture + "echo listed\n" + test,
            "quoted in the redirect, bare in the test": (
                'd=$(pwd) || exit 1\ngit ls-files -z > list 2> "${d}/err" || exit 1\n[[ ! -s ${d}/err ]] || exit 1\n'
            ),
            "the test chained with &&": capture + "[[ ! -s err ]] && echo clean\n",
            "through read_listing": "read_listing list err git ls-files -z || exit 1\n",
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
            "inside a substitution": ("x=$(git ls-files -z) || exit 1\n", [(3, "producer")]),
            "ls and find": ("ls > l || exit 1\nfind . -type f > f || exit 1\n", [(3, "producer"), (4, "producer")]),
            "git config -f and --file": (
                "git config -f f --get k || exit 1\ngit config --file f --get k || exit 1\n",
                [(3, "producer"), (4, "producer")],
            ),
        }
        for name, (body, expected) in found.items():
            with self.subTest(finding=name):
                result = self.assert_findings(body, expected)
                self.assertIn("can fail with exit 0 or after printing", result.stdout)
        result = self.assert_findings("git ls-files -z > list || exit 1\n", [(3, "producer")])
        self.assertIn("`git ls-files`", result.stdout, "the finding names the row")

    def test_shape_4_a_read_from_a_file_is_a_finding_naming_read_file(self) -> None:
        result = self.assert_findings("IFS= read -r x < unreadable || exit 1\n", [(3, "read")])
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
