"""Exercise scripts/lint-comparisons.py (C-61 rule 6; plan 023 PR F2): the rule table on fixture files in a temporary
directory, the content-hashed baseline and its changed-file severity, and the files this checkout changes against the
committed baseline.

The lint runs as a subprocess (`python3 -I`), so nothing of it is imported here.
"""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINT = ROOT / "scripts/lint-comparisons.py"
# plan 024 5.14 item 2: env -i, a system git by its absolute path, an explicit -C, no system or global config
GIT_ENV = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
GIT_C = ("core.hooksPath=/dev/null", "core.fsmonitor=false", "protocol.allow=never", "protocol.https.allow=always")
GIT_C += ("core.attributesFile=/dev/null", "core.sshCommand=false")
SHELL_NORMALISERS = {
    "realpath": '[[ "$(realpath "$path")" == */x ]]\n',
    "pwd -P": '[[ "$(cd "$dir" && pwd -P)" == */x ]]\n',
    "cd -P": '[[ "$(cd -P "$dir" && pwd)" == */x ]]\n',
    "readlink -f": '[[ "$(readlink -f "$path")" == */x ]]\n',
    "python3 -I -c os.path.realpath": '[[ "$(python3 -I -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$path")" == */x ]]\n',
    "python3 -I -c os.path.normpath": '[[ "$(python3 -I -c "import os, sys; print(os.path.normpath(sys.argv[1]))" "$path")" == */x ]]\n',
    "python3 -I -c urllib.parse": '[[ "$(python3 -I -c "import sys, urllib.parse; print(urllib.parse.unquote(sys.argv[1]))" "$url")" == */x ]]\n',
    "canonical_path": '[[ "$(canonical_path "$path")" == */x ]]\n',
    "normalise_*": '[[ "$(normalise_path "$path")" == */x ]]\n',
    "normalize_*": '[[ "$(normalize_path "$path")" == */x ]]\n',
}
# rule id -> (fixture file name, the refused fixture of the rule table, one accepted form per normaliser of its row)
TABLE = {
    "R0": (
        "r0.sh",
        "[[ $a == $b ]] # lint-comparisons: allow\n",
        {"a reason": "[[ $path == /x ]] # lint-comparisons: allow the fixture\n"},
    ),
    "R1": ("r1.sh", "[[ $path == */x ]]\n", SHELL_NORMALISERS),
    "R2": (
        "r2.sh",
        'case "$url" in file://*) ;; esac\n',
        {
            name: form.replace("[[ ", "case ").replace('" == */x ]]', '/x" in /*) ;; esac')
            for name, form in SHELL_NORMALISERS.items()
        },
    ),
    "R3": (
        "r3.sh",
        "jq -r 'select(.url | endswith(\"/index.html\"))'\n",
        {
            "def canonical_path": "jq -r 'def canonical_path: ascii_downcase; select((.url | canonical_path) == ($p | canonical_path))'\n",
            "def normalise_*": "jq -r 'def normalise_url: ascii_downcase; select((.url | normalise_url) == ($p | normalise_url))'\n",
            "def normalize_*": "jq -r 'def normalize_url: ascii_downcase; select((.url | normalize_url) == ($p | normalize_url))'\n",
        },
    ),
    "R4": (
        "r4.py",
        'if path == "/x":\n    pass\n',
        {
            "os.path.realpath": 'if os.path.realpath(path) == "/x":\n    pass\n',
            "os.path.normpath": 'if os.path.normpath(path) == "/x":\n    pass\n',
            "os.path.abspath": 'if os.path.abspath(path) == "/x":\n    pass\n',
            "Path(...).resolve": 'if Path(path).resolve() == Path("/x"):\n    pass\n',
            "pathlib.Path(...).resolve": 'if pathlib.Path(path).resolve() == Path("/x"):\n    pass\n',
            "urllib.parse.urlsplit": 'if urllib.parse.urlsplit(url).path == "/x":\n    pass\n',
            "urlparse": 'if urlparse(url).path == "/x":\n    pass\n',
            "unquote": 'if unquote(url) == "/x":\n    pass\n',
            "canonical_path": 'if canonical_path(path) == "/x":\n    pass\n',
            "normalise_*": 'if normalise_path(path) == "/x":\n    pass\n',
            "normalize_*": 'if normalize_path(path) == "/x":\n    pass\n',
            "os.path.samefile": 'if os.path.samefile(path, "/x"):\n    pass\n',
        },
    ),
    "R5": (
        "r5.sh",
        "ps -axo pid,command | grep claude\n",
        {"ps -o <fields>= -p <pid>": 'ps -o args= -p "$pid"\n', "pgrep -x <name>": "pgrep -x omp\n"},
    ),
    "R6": (
        "r6.sh",
        'grep -E "^(${ids})\\t"\n',
        {"grep -F": 'grep -F "${ids}"\n', "escape_regex": 'grep -E "^($(escape_regex "$ids"))\\t"\n'},
    ),
}
PYTHON_R6 = ("r6.py", 're.search(f"^{name}$", text)\n', {"re.escape": 're.search(f"^{re.escape(name)}$", text)\n'})
# forms beyond the table's fixtures that the lint also refuses: the test word not first on its line, a jq program inside
# a double-quoted substitution, ps inside a substitution or after if, a jq normaliser applied to one side only
MORE_REFUSED = {
    "R1": ('if [[ "$path" == */x ]]; then :; fi\n', 'x=1 && [ "$1" = "$2/" ]\n'),
    "R2": ('while :; do case "$url" in file://*) ;; esac; done\n',),
    "R3": (
        'x="$(printf %s "$j" | jq -r \'select(.url == $u)\')"\n',
        "jq -r 'def canonical_path: .; select((.url | canonical_path) == $path)'\n",
    ),
    "R5": ("x=$(ps -axo pid,command | grep claude)\n", "if ps -axo pid,command | grep -q claude; then :; fi\n"),
}


class LintComparisonsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()

    def lint(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, "-I", str(LINT), *args], check=False, cwd=cwd or self.temp, capture_output=True, text=True
        )

    def run_fixture(self, name, text, baseline=None, changed=None, mode=()):
        (self.temp / name).write_text(text)
        flags = mode or ("--changed", *(changed or [name]))  # the fixture file is the change unless told otherwise
        return self.lint("--baseline", str(baseline or self.temp / "none.tsv"), name, *flags)

    def test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted(self):
        for rule, (name, refused, accepted) in {**TABLE, "R6 (Python)": PYTHON_R6}.items():
            rule_id = rule.split(" ")[0]
            with self.subTest(rule=rule, form="refused"):
                result = self.run_fixture(name, refused)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(
                    [f"{name}:1: {rule_id}"],
                    [line.rsplit(" ", 1)[0][: len(f"{name}:1: {rule_id}")] for line in result.stdout.splitlines()],
                )
                self.assertIn(f"{name}:1: {rule_id} ", result.stdout)
            for normaliser, form in accepted.items():
                with self.subTest(rule=rule, form=normaliser):
                    result = self.run_fixture(name, form)
                    self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))
            for form in MORE_REFUSED.get(rule_id, ()):
                with self.subTest(rule=rule, form=form):
                    result = self.run_fixture(name, form)
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertTrue(all(f" {rule_id} " in line for line in result.stdout.splitlines()), result.stdout)
        listed = self.lint("--list-rules")
        self.assertEqual(0, listed.returncode)
        self.assertEqual([f"R{i}" for i in range(7)], [line.split(" ")[0] for line in listed.stdout.splitlines()[:7]])
        self.assertTrue(
            listed.stdout.splitlines()[7].startswith("shortcut: the lint is statement-local"), listed.stdout
        )

    def test_a_baseline_row_matching_no_hit_fails_as_stale(self):
        name, refused, _ = TABLE["R1"]
        baseline = self.temp / "baseline.tsv"
        baseline.write_text(f"{name}\tR1\t{hashlib.sha256(refused.strip().encode()).hexdigest()}\n")
        result = self.run_fixture(name, refused, baseline)
        self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))
        result = self.run_fixture(name, refused.replace("*/x", "*/y"), baseline)
        self.assertEqual(1, result.returncode)
        self.assertIn(f"stale baseline row {name} R1\n", result.stdout)
        self.assertIn(f"{name}:1: R1 ", result.stdout)
        # with explicit files, a row of a file that was not scanned is not stale (the default set reports every row)
        baseline.write_text(
            f"other.sh\tR1\t{'0' * 64}\n{name}\tR1\t{hashlib.sha256(refused.strip().encode()).hexdigest()}\n"
        )
        result = self.run_fixture(name, refused, baseline)
        self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))

    def test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails(self):
        name, refused, _ = TABLE["R1"]
        row = f"{name}\tR1\t{hashlib.sha256(refused.strip().encode()).hexdigest()}\n"
        baseline = self.temp / "baseline.tsv"
        baseline.write_text(row)
        result = self.run_fixture(name, refused * 2, baseline)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            [f"{name}:2: R1"], [line.rsplit(" ", 1)[0][: len(f"{name}:2: R1")] for line in result.stdout.splitlines()]
        )
        baseline.write_text(row * 2)
        result = self.run_fixture(name, refused * 2, baseline)
        self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))

    def test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails(self):
        for form, rule in (
            ('if fake.realpath(path) == "/x":\n    pass\n', "R4"),
            ('if fake.resolve(path) == "/x":\n    pass\n', "R4"),
            ('re.search(f"^{fake.escape(name)}$", text)\n', "R6"),
        ):
            with self.subTest(form=form):
                result = self.run_fixture("q.py", form)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"q.py:1: {rule} ", result.stdout)
        for form in ('if os.path.realpath(path) == "/x":\n    pass\n', 're.search(f"^{re.escape(name)}$", text)\n'):
            with self.subTest(form=form):
                result = self.run_fixture("q.py", form)
                self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))

    def test_the_jq_normaliser_is_required_on_each_operand_side(self):
        refused = (
            "jq -r 'def canonical_path: .; select((.url | canonical_path | canonical_path) == $path)'\n",
            "jq -r 'def canonical_path: .; select(.url | endswith($path | canonical_path | canonical_path))'\n",
        )
        for form in refused:
            with self.subTest(form=form):
                result = self.run_fixture("j.sh", form)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("j.sh:1: R3 ", result.stdout)
        accepted = "jq -r 'def canonical_path: .; select((.url | canonical_path) | endswith($path | canonical_path))'\n"
        result = self.run_fixture("j.sh", accepted)
        self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))

    def assert_refused_and_accepted(self, name, rule, refused, accepted):
        result = self.run_fixture(name, refused)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"{name}:1: {rule} ", result.stdout)
        result = self.run_fixture(name, accepted)
        self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))

    def test_a_single_quoted_jq_option_value_is_not_read_as_the_program(self):
        # owned row 4302629300: a single-quoted string that is an option's argument, or sits inside a double-quoted
        # one, is skipped; the program is the next single-quoted string on the jq word's logical line
        self.assert_refused_and_accepted(
            "j.sh",
            "R3",
            "jq -n --arg p '/x' 'select(.url == $p)'\n",
            "jq -n --arg p '/x' 'def canonical_path: .; select((.url | canonical_path) == ($p | canonical_path))'\n",
        )
        result = self.run_fixture("j.sh", "jq -r --arg m \"${s#*$'\\t'}\" 'select(.url == $m)'\n")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("j.sh:1: R3 ", result.stdout)
        # forms the base scan already read stay read: words before the program that are no option, escaped and
        # nested quotes in an option's argument, a continuation, a concatenated program word, jq through a variable
        for form in (
            'jq -r "${opts[@]}" \'select(.url == $u)\' "$f"\n',
            "jq -er 2>/dev/null 'select(.path == $p)'\n",
            'jq -n --arg p "a\\"b" \'select(.url == $p)\'\n',
            'jq -n --arg root "$(cd "$(dirname "$0")/.." && pwd)" \'select(.path == $root)\'\n',
            "jq -r\\\n  'select(.url == $p)'\n",
            "jq -n \"${defs}\"'select(.url == $p)'\n",
            "\"$jq\" -r 'select(.url == $p)'\n",
            "\"${jq}\" -r 'select(.url == $p)'\n",
            "\"$(command -v jq)\" -r 'select(.url == $p)'\n",
            "\"$(command -v jq 2>/dev/null)\" -r 'select(.url == $p)'\n",
            "\"${tools[jq]}\" -r 'select(.url == $p)'\n",
            "\"$bin/jq.exe\" -r 'select(.url == $p)'\n",
        ):
            with self.subTest(form=form):
                result = self.run_fixture("j.sh", form)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertTrue(all(" R3 " in line for line in result.stdout.splitlines()), result.stdout)

    def test_a_jq_normaliser_name_inside_a_string_literal_is_no_application(self):
        # owned row 4302629305: each side must apply the normaliser, not merely contain its name
        self.assert_refused_and_accepted(
            "j.sh",
            "R3",
            "jq -r 'def canonical_path: .; select((.url + \"canonical_path\") == ($path | canonical_path))'\n",
            "jq -r 'def canonical_path: .; select((.url + \"/\" | canonical_path) == ($path | canonical_path))'\n",
        )
        # nor does a jq comment that names it
        result = self.run_fixture(
            "j.sh", "jq -r 'def canonical_path: .;\n  select(.url # canonical_path\n  == ($p | canonical_path))'\n"
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("j.sh:3: R3 ", result.stdout)

    def test_every_f_string_interpolation_in_a_regex_is_escaped(self):
        # owned row 4302629307: one re.escape does not cover the other interpolations of the f-string
        self.assert_refused_and_accepted(
            "r6.py",
            "R6",
            're.search(f"{re.escape(prefix)}{name}", text)\n',
            're.search(f"{re.escape(prefix)}{re.escape(name)}", text)\n',
        )
        # re.escape passed to map escapes each element, as the base accepted
        result = self.run_fixture("r6.py", "re.search(f\"{re.escape(p)}({'|'.join(map(re.escape, names))})\", text)\n")
        self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))

    def test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning(self):
        name, refused, _ = TABLE["R1"]
        result = self.run_fixture(name, refused, changed=["other.sh"])
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"warning: {name}:1: R1 ", result.stdout)
        self.assertIn("warning: 1 unbaselined hit(s) and 0 stale row(s) in unchanged files\n", result.stdout)
        result = self.run_fixture(name, refused, mode=("--all",))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"{name}:1: R1 ", result.stdout)

    def test_a_hit_in_a_changed_file_fails(self):
        name, refused, _ = TABLE["R1"]
        result = self.run_fixture(name, refused, changed=[name, "other.sh"])
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertTrue(result.stdout.startswith(f"{name}:1: R1 "), result.stdout)
        self.assertNotIn("warning", result.stdout)
        result = self.run_fixture(name, refused, mode=("--all",))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"{name}:1: R1 ", result.stdout)

    def stale(self):  # a row for the fixture's hit beside a row for a line the fixture does not have
        name, refused, _ = TABLE["R1"]
        baseline = self.temp / "baseline.tsv"
        rows = (refused.strip(), refused.replace("*/x", "*/y").strip())
        baseline.write_text("".join(f"{name}\tR1\t{hashlib.sha256(r.encode()).hexdigest()}\n" for r in rows))
        return name, refused, baseline

    def test_a_stale_row_for_a_changed_file_fails(self):
        name, refused, baseline = self.stale()
        result = self.run_fixture(name, refused, baseline)
        self.assertEqual((1, f"stale baseline row {name} R1\n"), (result.returncode, result.stdout), result.stderr)
        result = self.run_fixture(name, refused, baseline, mode=("--all",))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"stale baseline row {name} R1\n", result.stdout)

    def test_a_stale_row_for_an_unchanged_file_warns(self):
        name, refused, baseline = self.stale()
        result = self.run_fixture(name, refused, baseline, changed=["other.sh"])
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"warning: stale baseline row {name} R1\n", result.stdout)
        self.assertIn("warning: 0 unbaselined hit(s) and 1 stale row(s) in unchanged files\n", result.stdout)
        result = self.run_fixture(name, refused, baseline, mode=("--all",))  # the matched hit is printed too
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            [f"{name}:1: R1 ", f"stale baseline row {name} R1"],
            [x[: len(name) + 7] if ":" in x else x for x in result.stdout.splitlines()],
        )

    def test_the_changed_files_are_clean_against_the_baseline(self):
        git = [
            os.path.realpath(shutil.which("git", path=os.defpath)),
            "-C",
            str(ROOT),
            *(x for c in GIT_C for x in ("-c", c)),
        ]
        diff = ("diff", "--name-only", "-z", "--no-ext-diff", "--no-textconv", "origin/main...HEAD")
        out = subprocess.run([*git, *diff], env=GIT_ENV, check=True, capture_output=True, text=True).stdout
        changed = set(filter(None, out.split("\0")))
        result = self.lint(cwd=ROOT)  # no mode flag: the lint computes the same changed set itself
        self.assertEqual((0, ""), (result.returncode, result.stderr), result.stdout)
        self.assertEqual([], [x for x in result.stdout.splitlines() if not x.startswith("warning: ")])
        self.assertEqual([], [x for x in result.stdout.splitlines() for f in changed if f"{f}:" in x or f" {f} " in x])


if __name__ == "__main__":
    unittest.main()
