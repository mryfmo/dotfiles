"""Exercise scripts/lint-comparisons.py (C-61 rule 6; plan 023 PR F2): the rule table on fixture files in a temporary
directory, the content-hashed baseline and its changed-file severity, and the files this checkout changes against the
committed baseline.

The lint runs as a subprocess (`python3 -I`), so nothing of it is imported here.
"""

import hashlib
import os
import re
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

# the owned rows of dotfiles-T129-normalised-comparison-lint-followup-a02 (the followup-a01 and followup-a03 records), one
# entry per distinct gap naming its ids (a Bot row and its local twin share the fixture): fixture -> [(rule, line)], or []
# where the form holds no comparison
JQ_AND = (  # a raw comparison between two normalised ones, joined by and
    "jq -r 'def canonical_path: .; select((.a | canonical_path) == ($x | canonical_path) and .url == $p"
    " and (.b | canonical_path) == ($y | canonical_path))'\n"
)
OWNED_ROWS = {
    "4306643800 audit:4f5be51:4": [  # continuation lines are one test; its marker may sit on its last line
        ("c.sh", '[[ "$path" == \\\n  */x ]]\ncase "$url" \\\n  in file://*) ;; esac\n', [("R1", 1), ("R2", 3)]),
        ("c2.sh", '[[ "$path" == \\\n  */x ]] # lint-comparisons: allow the fixture\n', []),
        ("c3.sh", "x=a\\\\\n[[ $path == /x ]]\n", [("R1", 2)]),  # an escaped backslash continues nothing
    ],
    "4306643803 audit:4f5be51:9": [  # a double-quoted jq program is read as the program, across lines too
        (
            "j.sh",
            'jq -r "select(.url == \\"/x\\")"\njq -n --arg p /x "select(.path == \\$p)"\n',
            [("R3", 1), ("R3", 2)],
        ),
        ("j2.sh", 'jq -r "\n  select(.url == \\"/x\\")"\n', [("R3", 2)]),
        ("j3.sh", 'jq -r .url f > o; echo "select(.url == \\"/x\\")"\n', []),  # no program after a separator
    ],
    "4306643804 audit:4f5be51:2": [  # every fragment of a formatted value is escaped, a join's separator too
        (
            "r.py",
            're.search(f"{re.escape(prefix) + name}", t)\nre.search(f"{name + re.escape(suffix)}", t)\n',
            [("R6", 1), ("R6", 2)],
        ),
        ("r2.py", 're.search(f"{sep.join(map(re.escape, xs))}", t)\n', [("R6", 1)]),
    ],
    "4306643808 audit:4f5be51:8": [  # an allow marker counts only in a comment, never in a string
        ("m.py", 'if path == "/x": print("# lint-comparisons: allow reason")\n', [("R4", 1)]),
        ("k.sh", '[[ $path == /x ]] && echo "# lint-comparisons: allow reason"\n', [("R1", 1)]),
        (
            "k2.sh",
            "jq -r '\n  select(.url == $p)' # lint-comparisons: allow the fixture\n",
            [],
        ),  # on the quote's last line
        ("k3.sh", "jq -r 'select(.url == $p)' f && echo \"# lint-comparisons: allow reason\"\n", [("R3", 1)]),
        (
            "k4.sh",
            "jq -r 'select(.url == $p)\n  | .x' # lint-comparisons: allow the fixture\n",
            [],
        ),  # the whole program
    ],
    "audit:4f5be51:1": [  # and/or bound each comparison's operands; if…end is one operand
        ("l.sh", JQ_AND, [("R3", 1)]),
        ("l2.sh", "jq -r 'select(if .a then .url else .path end == $p)'\n", [("R3", 1)]),
    ],
    "audit:4f5be51:3": [  # a single-quoted pattern interpolates nothing; a pattern word with an expanded $ does
        ("g.sh", "grep -E '^$name$' file\n", []),
        ("g2.sh", "grep -E \"^\\\\$name\" f\ngrep -E '^'\"$name\"'$' f\n", [("R6", 1), ("R6", 2)]),
    ],
    "audit:4f5be51:5": [  # a jq string and a jq comment hold no operator; a long literal shifts no later one
        ("s.sh", 'jq -n \'"path == /x" # .url == "/x"\'\n', []),
        ("s2.sh", "jq -r 'select(.name != \"" + "a" * 40 + '") | select(.x == "/y")\'\n', [("R3", 1)]),
    ],
    "audit:4f5be51:6": [  # the whole pattern word, mixed quotes too; an escaped $ expands nothing
        ("p.sh", 'pgrep -f "prefix $name"\n', [("R5", 1)]),
        ("p2.sh", 'pgrep -f x"$name"\npgrep -f "x \\$y"\n', [("R5", 1)]),
    ],
    "audit:4f5be51:7": [("v.sh", '[[ "$x/path" == "$y/path" ]]\n', [("R1", 1)])],  # a literal path after the variable
}


class LintComparisonsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()

    def lint(self, *args, cwd=None, env=None):
        cmd, cwd = [sys.executable, "-I", str(LINT), *args], cwd or self.temp
        return subprocess.run(cmd, check=False, cwd=cwd, env=env, capture_output=True, text=True)

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
        named = [
            re.match(r"warning: (?:stale baseline row (\S+) R\d|(\S+):\d+: R\d )", x)
            for x in result.stdout.splitlines()
        ]
        self.assertEqual([], [m[1] or m[2] for m in named if m and (m[1] or m[2]) in changed])

    def test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails(self):
        # the review's P2: the CI entry point's own changed set, in a repository with a real origin/main
        repo, (_, refused, _) = self.temp / "repo", TABLE["R1"]
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t"}
        env["GIT_COMMITTER_EMAIL"] = "t@t"

        def git(*args):
            subprocess.run(["git", "-C", str(repo), "-c", "commit.gpgsign=false", *args], check=True, env=env)

        (repo / "scripts").mkdir(parents=True)
        shutil.copy(LINT, repo / "scripts/lint-comparisons.py")
        row = hashlib.sha256(refused.strip().encode()).hexdigest()
        (repo / "scripts/lint-comparisons-baseline.tsv").write_text(f"scripts/old.sh\tR1\t{row}\n")
        for name, text in (("main.sh", "true\n"), ("old.sh", refused)):
            (repo / "scripts" / name).write_text(text)
        for args in (("init", "-q", "-b", "main"), ("add", "."), ("commit", "-qm", "base"), ("switch", "-qc", "pr")):
            git(*args)
        (repo / "scripts/pr.sh").write_text(refused)  # the change: a new hit, and a rename that strands old.sh's row
        for args in (
            ("mv", "scripts/old.sh", "scripts/new.sh"),
            ("add", "."),
            ("commit", "-qm", "pr"),
            ("switch", "-q", "main"),
        ):
            git(*args)
        (repo / "scripts/main.sh").write_text(refused)  # main gains a hit in a file the change leaves alone
        for args in (
            ("commit", "-qam", "main"),
            ("update-ref", "refs/remotes/origin/main", "main"),
            ("switch", "-q", "pr"),
        ):
            git(*args)
        git("merge", "-q", "--no-edit", "main")  # update-branch: the PR head now carries main's hit
        run = [sys.executable, "-I", str(repo / "scripts/lint-comparisons.py")]
        result = subprocess.run(run, check=False, capture_output=True, text=True)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        lines = sorted(x.split(" R1")[0] for x in result.stdout.splitlines())
        self.assertEqual(["scripts/new.sh:1:", "scripts/pr.sh:1:", "stale baseline row scripts/old.sh"], lines[:3])
        self.assertEqual(
            ["warning: 1 unbaselined hit(s) and 0 stale row(s) in unchanged files", "warning: scripts/main.sh:1:"],
            lines[3:],
        )
        git("update-ref", "-d", "refs/remotes/origin/main")  # no base to diff against: fail closed, never all-unchanged
        result = subprocess.run(run, check=False, capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertNotIn("warning", result.stdout)

    def test_each_owned_row_is_refused_or_accepted_by_its_fixture(self):
        for rows, fixtures in OWNED_ROWS.items():
            for name, text, wants in fixtures:
                with self.subTest(rows=rows, fixture=name):
                    result = self.run_fixture(name, text)
                    self.assertEqual(int(bool(wants)), result.returncode, result.stdout + result.stderr)
                    found = [line.split(" ", 2)[:2] for line in result.stdout.splitlines()]
                    self.assertEqual([[f"{name}:{n}:", rule] for rule, n in wants], found)

    def test_a_jq_program_continued_by_backslash_newline_is_located_and_r3_applies(self):
        # thread 4313892754: a backslash-newline inside a double-quoted program continues it; it is no stray quote
        for name, text, line in (  # the hit is reported at its operator's own physical line
            ("jc.sh", 'jq -r "select(.url == \\\n  \\"/x\\")"\n', 1),
            ("jc2.sh", 'out="$(jq -r "select(.path \\\n  == \\$p)" f)"\n', 2),
            ("jc3.sh", 'out="$(jq -r "select(.pa\\\nth == \\$v)" f)"\n', 2),  # .path split, in a substitution
        ):
            with self.subTest(fixture=name):
                result = self.run_fixture(name, text)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"{name}:{line}: R3 ", result.stdout)

    def test_a_backslash_newline_joins_the_physical_lines_without_a_separator(self):
        # thread 4313892766: the shell deletes a backslash-newline, so a word continued by one stays one word
        for name, text, rule in (
            ("wj.sh", '[[ "$x" == *\\\n/foo ]]\n', "R1"),
            ("wc.sh", 'case "$x" in */fo\\\no) ;; esac\n', None),
            ("wp.sh", 'pgrep -f "$\\\n1"\n', "R5"),  # $1 split between $ and 1
        ):
            with self.subTest(fixture=name):
                result = self.run_fixture(name, text)
                if rule:
                    self.assertEqual(
                        (1, True), (result.returncode, f"{name}:1: {rule} " in result.stdout), result.stdout
                    )
                else:  # case matches on its word, here the variable: no path operand, as on one line
                    self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))

    def test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment(self):
        # thread 4313892783: shell comments are read with the quote state carried across lines and heredoc bodies skipped
        for name, text in (
            ("ms.sh", 'msg="\n# lint-comparisons: allow\n"\n'),
            ("ms2.sh", "msg='a\n  # lint-comparisons: allow\nb'\n"),
            ("hd.sh", "cat <<EOF\n# lint-comparisons: allow\nEOF\n"),
            ("hd2.sh", "cat <<-'X' > f\n\t# lint-comparisons: allow\n\tX\n"),
            ("hd3.sh", "cat <<'END-DATA'\n# lint-comparisons: allow\nEND-DATA\n"),  # a delimiter with a hyphen
        ):
            with self.subTest(fixture=name):
                result = self.run_fixture(name, text)
                self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))
        # a real comment after both is still one: its reasonless marker is R0
        result = self.run_fixture("rc.sh", 'msg="\na"\ncat <<EOF\nb\nEOF\n# lint-comparisons: allow\n')
        self.assertEqual((1, ["rc.sh:6: R0"]), (result.returncode, [x[:11] for x in result.stdout.splitlines()]))

    def assert_hits(self, fixtures):  # each fixture: (name, text, [(rule, line)]); [] means no output and exit 0
        for name, text, wants in fixtures:
            with self.subTest(fixture=name):
                result = self.run_fixture(name, text)
                self.assertEqual(int(bool(wants)), result.returncode, result.stdout + result.stderr)
                self.assertEqual(
                    [[f"{name}:{n}:", rule] for rule, n in wants],
                    [x.split(" ", 2)[:2] for x in result.stdout.splitlines()],
                )

    def test_process_patterns_include_positional_and_special_parameters(self):
        # audit:b24d313:1: positional and special parameters are expansions; a quoted or escaped $ is a literal
        spellings = ('"$1"', '"${10}"', '"$@"', '"x$?"', '"$$"', "$!")
        self.assert_hits([(f"p{i}.sh", f"pgrep -f {s}\n", [("R5", 1)]) for i, s in enumerate(spellings)])
        self.assert_hits([("pl.sh", "pgrep -f 'x$1'\npgrep -f \"x\\$1\"\n", [])])

    def test_double_quoted_jq_joins_split_operator_and_path(self):
        # audit:b24d313:2: bash deletes a backslash-newline inside "…", so the operator and the field arrive whole
        self.assert_hits(
            [
                ("so.sh", 'jq -r "select(.url =\\\n= \\$v)"\n', [("R3", 1)]),
                ("sp.sh", 'jq -r "select(.pa\\\nth == \\$v)"\n', [("R3", 2)]),
            ]
        )

    def test_jq_program_concatenates_all_word_parts(self):
        # audit:b24d313:3: one shell word, its quoted fragments concatenated in order, is the program
        self.assert_hits(
            [
                ("cw.sh", "jq -r 'select(''.url == $p)'\n", [("R3", 1)]),
                ("cw2.sh", "jq -r 'select('\"(.path == \\$p)\"')'\n", [("R3", 1)]),
            ]
        )

    def test_arithmetic_shift_keeps_following_marker_comments(self):
        # audit:b24d313:4: an arithmetic shift is no heredoc; the comments after it stay comments
        self.assert_hits(
            [
                ("as.sh", "bits=$((1 << shift))\n[[ $path == /x ]] # lint-comparisons: allow the fixture\n", []),
                ("as2.sh", "bits=$((1 << shift))\n# lint-comparisons: allow\n", [("R0", 2)]),
            ]
        )

    def test_heredoc_data_is_excluded_from_shell_rules(self):
        # audit:b24d313:5: a heredoc body is data: no shell rule reads it, nor a command substitution inside it
        body = "[[ $path == /x ]]\n"  # no marker: read as code, it would be R1
        hu = f"cat <<EOF\n{body}$([[ $path == /y ]] && echo y)\n$(true # lint-comparisons: allow\n)\nEOF\n"
        self.assert_hits([("hq.sh", f"cat <<'EOF'\n{body}EOF\n", []), ("hu.sh", hu, [])])

    def test_ansi_c_quotes_preserve_following_marker_comments(self):
        # audit:b24d313:6: $'…' closes at its unescaped quote; the comment after the next statement is one
        self.assert_hits(
            [("ac.sh", "msg=$'it\\'s fine'\n[[ $path == /x ]] # lint-comparisons: allow the fixture\n", [])]
        )

    def test_all_valid_heredoc_delimiters_exclude_body_markers(self):
        # audit:b24d313:7: every delimiter bash accepts ends its body where bash ends it; a body marker is no R0
        marker = "# lint-comparisons: allow\n"
        self.assert_hits(
            [
                (f"d{i}.sh", f"cat <<{open_}\n{marker}{close}\n", [])
                for i, (open_, close) in enumerate(
                    (("'123'", "123"), ("'END-DATA'", "END-DATA"), ('E"N"D', "END"), ("\\EOF", "EOF"), ("-'T'", "\tT"))
                )
            ]
        )

    def test_shfmt_missing_refuses_without_fallback(self):
        (self.temp / "m.sh").write_text("[[ $path == /x ]]\n")
        env = {"PATH": str(self.temp / "empty")}  # neither shfmt nor mise, whatever the host has in /usr/bin
        result = self.lint("--baseline", str(self.temp / "none.tsv"), "m.sh", "--changed", "m.sh", env=env)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("shfmt missing", result.stderr)
        self.assertEqual("", result.stdout)  # no regex scan stands in for the parser

    def test_shfmt_parse_failure_refuses_with_original_message(self):
        result = self.run_fixture("bad.sh", "f() {\n  echo x\n")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("bad.sh: 1:5: reached EOF without matching `{` with `}`", result.stderr)
        result = self.lint("--baseline", str(self.temp / "none.tsv"), "bad.sh", "--all")
        self.assertNotEqual(0, result.returncode)  # --all is no way around a parse failure
        fake = self.temp / "bin/shfmt"  # a shfmt that answers with no JSON, or with JSON that is no file node
        fake.parent.mkdir()
        (self.temp / "ok.sh").write_text("echo ok\n")
        env = {"PATH": f"{fake.parent}:/usr/bin:/bin"}
        for answer in ("not-json", "{}", "null", '{"Type": "Word"}'):
            with self.subTest(answer=answer):
                fake.write_text(f"#!/bin/sh\necho '{answer}'\n")
                fake.chmod(0o755)
                result = self.lint("--baseline", str(self.temp / "none.tsv"), "ok.sh", "--changed", "ok.sh", env=env)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("ok.sh: shfmt gave no JSON AST", result.stderr)

    def test_shfmt_falls_back_to_the_pinned_mise_form_with_the_file_dialect_and_blanked_actions(self):  # amendment 1
        fake = self.temp / "mise-only/mise"  # no shfmt on PATH, so the pinned mise form runs; it logs argv and input
        fake.parent.mkdir()
        fake.write_text(
            '#!/bin/sh\necho "$*" >> "$0.log"\n[ "$5" = --version ] || /bin/cat >> "$0.log"\necho \'{"Type": "File"}\'\n'
        )
        fake.chmod(0o755)
        files = {
            "t.sh.tmpl": '(\n{{ include "x" }}\n)\n{{ includeTemplate "y" }}\necho "{{ .y }}"\n',
            "z.zsh": "echo\n",
            "zs": "#!/bin/zsh\necho\n",
        }
        for name, text in files.items():
            (self.temp / name).write_text(text)
        result = self.lint(
            "--baseline", str(self.temp / "none.tsv"), *files, "--changed", env={"PATH": str(fake.parent)}
        )
        self.assertEqual((0, ""), (result.returncode, result.stdout + result.stderr))
        run, blanked = (
            "x shfmt@3.14.1 -- shfmt",
            f'(\n:{" " * 16}\n)\n:{" " * 24}\necho "{" " * 8}"\n',
        )  # an include alone is `:`
        log = (
            f"{run} --version\n{run} -ln bash --tojson\n{blanked}{run} -ln zsh --tojson\necho\n{run} -ln zsh --tojson\n"
        )
        self.assertEqual(log + "#!/bin/zsh\necho\n", Path(f"{fake}.log").read_text())
        shfmt = fake.parent / "shfmt"  # shfmt on PATH comes first: the mise form runs no more
        shfmt.write_text(fake.read_text())
        shfmt.chmod(0o755)
        args = ("--baseline", str(self.temp / "none.tsv"), "z.zsh", "--changed")
        result = self.lint(*args, env={"PATH": str(fake.parent)})
        found = (result.returncode, result.stdout + result.stderr, Path(f"{shfmt}.log").read_text())
        self.assertEqual((0, "", "--version\n-ln zsh --tojson\necho\n"), found)
        self.assertEqual(log + "#!/bin/zsh\necho\n", Path(f"{fake}.log").read_text())

    def test_jq_hit_lines_follow_the_source_through_escapes_and_continuations(self):
        # worker review round 1: a decoded $'\n' adds no source line and an unquoted backslash-newline still ends one; a
        # double-quoted program is unescaped as the shell hands it over
        self.assert_hits(
            [
                (
                    "an.sh",
                    "jq -n $'.a\\n| select(.url == $p)'\necho ok # lint-comparisons: allow unrelated\n",
                    [("R3", 1)],
                ),
                ("uc.sh", "jq -r .url\\\n==\\$p f\n", [("R3", 2)]),
                ("dq.sh", 'jq -r "select(.a == \\"\\\\\\\\\\") | select(.url == \\$p)"\n', [("R3", 1)]),
            ]
        )

    def test_a_chained_or_continued_statement_is_one_statement_for_markers_and_normalisers(self):
        # worker review round 1: as on one physical line, a marker or a normaliser anywhere in its && chain accepts it
        self.assert_hits(
            [
                ("ch.sh", "[[ $path == /x ]] \\\n  && echo y # lint-comparisons: allow the fixture\n", []),
                ("ch2.sh", 'case "$url" \\\n  in file://*) ;; esac # lint-comparisons: allow the fixture\n', []),
                ("ch3.sh", 'cd -P "$dir" && [[ "$PWD" == /x/* ]]\nx=$(realpath "$p") && [[ $x == /y ]]\n', []),
                ("ch4.sh", 're=$(escape_regex "$x"); grep -E "^$re" f\n', []),
                ("ch5.sh", "[[ $path == /x ]] && echo y\necho z # lint-comparisons: allow the next one\n", [("R1", 1)]),
            ]
        )

    def test_an_extglob_pattern_is_literal_text_and_a_length_is_no_path(self):
        # worker review round 1: @(…) and +(…) keep their literal path pieces; ${#path} is a number; '' is empty
        self.assert_hits(
            [
                ("eg.sh", "[[ $x == @(/a|/b) ]]\n[[ $x == +(/foo) ]]\n", [("R1", 1), ("R1", 2)]),
                ("ln.sh", "[[ ${#path} == 0 ]]\n", []),
                ("e0.sh", "[[ '' == $path ]]\n", [("R1", 1)]),
            ]
        )

    def test_a_long_and_chain_is_read_without_recursion(self):
        # worker review round 1: 300 chained commands nest the AST 300 deep; the walk is iterative
        self.assert_hits([("lc.sh", "true && " * 300 + "[[ $path == /x ]]\n", [("R1", 1)])])

    def test_audit_2_heredoc_data_never_supplies_a_normaliser(self):
        # audit:6434c27:2: a heredoc body is data for acceptance too; a normaliser written in it accepts nothing
        self.assert_hits([("ha.sh", "[[ $path == /x ]] && cat <<EOF\nrealpath\nEOF\n", [("R1", 1)])])
        # blanking a body keeps its newlines, so a later statement's own normaliser still sits on its own line
        self.assert_hits([("hb.sh", 'cat <<EOF\na\nb\nEOF\n[[ "$(realpath "$p")" == /x ]]\n', [])])

    def test_audit_3_a_test_behind_command_or_builtin_is_read(self):
        # audit:6434c27:3: the command word comes after the command, builtin and exec wrappers
        forms = ('command [ "$path" = "$other" ]\n', 'builtin test "$path" = /x\n', "command -p [ $url != /y ]\n")
        self.assert_hits([(f"w{i}.sh", f, [("R1", 1)]) for i, f in enumerate(forms)])

    def test_audit_4_a_ps_producer_inside_a_subshell_or_block_is_read(self):
        # audit:6434c27:4: each pipeline stage resolves through subshells, blocks and inner pipes to its command
        forms = ("(ps aux) | grep needle\n", "{ ps aux; } | grep needle\n", "ps aux | (grep needle)\n")
        self.assert_hits([(f"pp{i}.sh", f, [("R5", 1)]) for i, f in enumerate(forms)])
        self.assert_hits([("pq.sh", "(ps -o pid= -p 1) | grep x\n", [])])

    def test_audit_5_an_expansion_led_word_is_no_option(self):
        # audit:6434c27:5: an option is a word whose first part is literal text starting with -
        self.assert_hits([("ox.sh", 'pgrep -f "$name-x"\n', [("R5", 1)]), ("oy.sh", 'grep -E "$v-x" f\n', [("R6", 1)])])

    def test_audit_6_jq_is_the_command_word_only(self):
        # audit:6434c27:6: a jq inside another command's argument runs no program there; j"q" and command jq do
        self.assert_hits(
            [
                ("jx.sh", "echo \"$(jq -r .name input)\" 'select(.url == $p)'\n", []),
                ("jy.sh", "j\"q\" 'select(.url == $p)'\n", [("R3", 1)]),
                ("jz.sh", "command jq -r 'select(.url == $p)'\n", [("R3", 1)]),
            ]
        )

    def test_audit_7_ansi_c_quotes_decode_by_bash_s_whole_table(self):
        # audit:6434c27:7: $'…' hex, octal and unicode escapes reach jq decoded, as bash hands them over
        forms = ("$'select(.url \\x3d\\x3d $p)'", "$'select(.url \\075\\075 $p)'", "$'select(.url \\u003d\\u003d $p)'")
        self.assert_hits([(f"ae{i}.sh", f"jq -r {f}\n", [("R3", 1)]) for i, f in enumerate(forms)])
        self.assert_hits([("af.sh", "jq -r $'select(.url \\x3e $p)'\n", [])])  # \x3e is >, no string comparison

    def test_audit_8_a_normaliser_counts_only_where_it_is_invoked(self):
        # audit:6434c27:8: a definition or an object key named canonical_path applies nothing; jq is tokenised
        unused = 'def canonical_path: error("unused"); {canonical_path: "/x"} == {canonical_path: $p}'
        self.assert_hits([("nu.sh", f"jq -n '{unused}'\n", [("R3", 1)])])
        used = "def canonical_path: .; (.url | canonical_path) == ($p | canonical_path)"
        self.assert_hits([("nv.sh", f"jq -n '{used}'\n", [])])
        # a jq comment is a comment token: a reasonless marker in one is R0 (audit:6434c27:13)
        self.assert_hits([("nw.sh", "jq -r '. # lint-comparisons: allow'\n", [("R0", 1)])])

    def test_the_job_log_records_the_shfmt_probes(self):  # amendment 1: validation.md quotes these lines from CI
        runs = []
        for cmd in (["shfmt"], ["mise", "x", "shfmt@3.14.1", "--", "shfmt"]):  # the lint's order
            exe = shutil.which(cmd[0])
            run = exe and subprocess.run([exe, *cmd[1:], "--version"], check=False, capture_output=True, text=True)
            runs.append(bool(run) and run.returncode == 0)
            print(
                f"\nshfmt probe: {' '.join(cmd)}: {exe} {run and (run.returncode, run.stdout.strip())}", file=sys.stderr
            )
        self.assertTrue(any(runs), "shfmt missing: the lint refuses every shell file")


if __name__ == "__main__":
    unittest.main()
