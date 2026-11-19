"""Exercise scripts/orchestrator/sweep-scope.py (regime-cutover U597, the operator's sweep rule C of 2026-11-18): the
one predicate `sweep_required(paths)` over the four path classes (`credential`, `policy`, `lever`,
`deployed-executable`, one frozen tuple of prefixes each, in that precedence, held equal to a literal copy here), a
mixed head's class, a docs-only head that requires nothing, and the CLI forms pr-merge.sh and the coordinator run
under `python3 -I -S`: `<base> <head>` (the paths `git diff --name-only --no-renames <base>...<head>` lists, from the
toplevel whatever `diff.relative` says or where the command runs; round 3) and `--files-json` (the audited head's
files as the lever's one read of the compare API prints them after the merge-base line the lever strips, `gh api
'repos/{owner}/{repo}/compare/<main tip>...<head>' --jq '("merge-base " + (.merge_base_commit.sha | if type == "string"
then . else error("merge_base_commit.sha is " + type + ", not a string") end)), ((if (.files | type) == "array" then
.files else error("files is " + (.files | type) + ", not an array") end) | .[] | [.status, .filename, (if
has("previous_filename") then .previous_filename else null end)] | @json)'`, one JSON array per file, keyed by main's
tip and the head's sha (round 4; round 6 holds `files` to an array before iterating; round 7 reads the tip once and
holds the merge base to it, so the listing is the diff the squash lands); round 5:
completeness read from the listing itself, 300 or more entries, the API's cap, answering `required cap`, and the
`--changed-files <n>` count of rounds 3 and 4 gone), each printing `required <class>`, `required cap` or
`not-required`, and exit 2 with one stderr line on a failed git read, an empty listing, a path git would not list, a
C-quoted name (round 2), a line that is not the API's shape, a rename without its source, a `previous_filename` that
is neither a string nor null (round 4), or usage (standing order 21: never `not-required` by failure). The documents
that state the rule (AGENTS.md, the hcom-orchestration skill, the orchestrator README) are read against CLASSES, the
one definition (round 2), against the listing keyed by the head and the daily sweep row (round 4), and against the
one call and the cap answer (round 5), and against the compare keyed by main's tip with the up-to-date requirement
(round 7)."""

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
READER = ROOT / "scripts/orchestrator/sweep-scope.py"
LEVER = ROOT / "scripts/orchestrator/pr-merge.sh"
AGENTS = ROOT / "AGENTS.md"
SKILL = ROOT / "home/dot_agents/skills/hcom-orchestration/SKILL.md"
README = ROOT / "scripts/orchestrator/README.md"
# The four classes as the documents name them, in the rule's words.
CLASS_WORDS = ("lever", "policy", "credential handling", "deployed executable")
# One path per class as the AGENTS.md sweep bullet names them.
CREDENTIAL = "home/dot_local/bin/common/executable_hcom-seat"
POLICY = "home/dot_agents/omp/policies/worker.yml"
LEVER_PATH = "scripts/orchestrator/pr-merge.sh"
DEPLOYED = "install/bootstrap.sh"
DOCS = ("docs/plan.md", "README.md", "tests/unit/test_x.py", ".github/workflows/test.yml", "Makefile")
# The operator's classification (decisions-four-points-2026-11-18.md, sweep rule C), written out here so that an
# added or missing prefix in the module fails this test (round 3, verdict finding 8); the per-prefix test below
# derives its cases from the module and could not see one.
CLASSES_LITERAL = (
    (
        "credential",
        (
            "scripts/orchestrator/hcom-seat",
            "scripts/orchestrator/acp-broker",
            "scripts/orchestrator/seat-token-place",
            "scripts/orchestrator/seat-login-preflight",
            "home/dot_local/bin/common/executable_hcom-seat",
            "home/dot_local/bin/common/executable_acp-broker",
            "home/dot_local/bin/common/executable_seat-token-place",
            "home/dot_local/bin/common/executable_seat-login-preflight",
            "home/.chezmoiscripts/",
        ),
    ),
    (
        "policy",
        (
            "home/dot_agents/omp/policies/",
            "home/dot_agents/agent-config.yaml",
        ),
    ),
    (
        "lever",
        (
            "scripts/orchestrator/",
            "home/dot_local/bin/common/",
        ),
    ),
    (
        "deployed-executable",
        (
            "home/dot_local/bin/",
            "home/dot_dsh/plugins/",
            "install/",
        ),
    ),
)
# The lever's jq form and the reader's call, as pr-merge.sh spells them (round 3; round 4 passes previous_filename
# through as it is, so a boolean reaches the reader and is refused instead of being mapped to null; round 5 requires
# the `files` key; round 6 holds `files` to an array before `.[]` iterates it, so an object, a string, a number, a
# boolean or null there is the jq's error naming the type and never a listing; round 7 emits the response's merge base
# as the first line, `merge-base <sha>`, which the lever holds equal to main's tip before the file lines reach the
# reader).
FILES_JQ = (
    '\'("merge-base " + (.merge_base_commit.sha | if type == "string" then . else error("merge_base_commit.sha is "'
    ' + type + ", not a string") end)), ((if (.files | type) == "array" then .files else error("files is " + (.files'
    ' | type) + ", not an array") end) | .[] | [.status, .filename, (if has("previous_filename") then'
    " .previous_filename else null end)] | @json)'"
)
# The reader run is the lever's pinned copy of the checkout's file (round 8: reader_copy).
READER_CALL = '"${scope_copy}" --files-json <<< "${files}"'
# The compare API's cap on `files` (round 5), as the reader names it.
CAP = 300


def load_reader():
    """The module imported from beside the levers, as a test of its predicate reads it."""
    spec = importlib.util.spec_from_file_location("sweep_scope", READER)
    module = importlib.util.module_from_spec(spec)
    sys.modules["sweep_scope"] = module
    spec.loader.exec_module(module)
    return module


def entry(filename, status="modified", previous=None):
    """One line of the files listing as the lever's jq form prints it."""
    return json.dumps([status, filename, previous], separators=(",", ":"))


def listing(*paths, status="modified"):
    """A listing of files at `paths`, one array per line with the trailing newline."""
    return "".join(entry(path, status) + "\n" for path in paths)


class SweepScopePredicateTest(unittest.TestCase):
    def setUp(self):
        self.reader = load_reader()

    def test_the_classes_are_frozen_tuples_in_the_order_of_precedence(self):
        self.assertEqual(
            self.reader.CLASS_NAMES, ("credential", "policy", "lever", "deployed-executable"), "the precedence"
        )
        for name, prefixes in self.reader.CLASSES:
            with self.subTest(name):
                self.assertIsInstance(prefixes, tuple)
                self.assertTrue(prefixes, "a class has at least one prefix")
                self.assertRegex(name, r"^[a-z][a-z-]*$", "the class is one lowercase word, as the lever reads it")
                for prefix in prefixes:
                    self.assertNotIn("//", prefix)
                    self.assertFalse(prefix.startswith("/"))

    def test_the_classes_equal_the_operator_s_classification_written_out(self):
        """Round 3 (verdict finding 8): CLASSES is the literal copy above, tuple for tuple and in order, so a prefix
        added to or dropped from the module fails here, where the derived tests passed with an unrelated directory
        added to the lever class."""
        self.assertEqual(self.reader.CLASSES, CLASSES_LITERAL)
        self.assertEqual(
            tuple(len(prefixes) for _, prefixes in self.reader.CLASSES), (9, 2, 2, 3), "the prefix count per class"
        )
        # the literal is itself a copy, not a reference: a change to the module alone is seen
        self.assertIsNot(self.reader.CLASSES, CLASSES_LITERAL)
        self.assertEqual(self.reader.path_class("scripts/orchestratorx/a.sh"), None)

    def test_each_prefix_of_each_class_puts_a_path_in_that_class(self):
        """A representative under each prefix (the prefix itself for an exact entry, a child for a directory) falls
        in its own class: no entry is shadowed by an earlier class."""
        for name, prefixes in self.reader.CLASSES:
            for prefix in prefixes:
                path = prefix + "x" if prefix.endswith("/") else prefix
                with self.subTest(path):
                    self.assertEqual(self.reader.path_class(path), name)
                    self.assertEqual(self.reader.sweep_required([path]), name)
                    self.assertEqual(self.reader.answer([path]), f"required {name}")

    def test_the_classes_of_the_brief(self):
        """The brief's classes: lever (`scripts/orchestrator/`, `home/dot_local/bin/common/`), policy
        (`home/dot_agents/omp/policies/`, the manifest file), credential handling (the four seat levers in both
        places and `home/.chezmoiscripts/`), deployed executables (`home/dot_local/bin/`, `home/dot_dsh/plugins/`,
        `install/`)."""
        for path, name in (
            ("scripts/orchestrator/ledger.py", "lever"),
            ("scripts/orchestrator/README.md", "lever"),
            ("home/dot_local/bin/common/executable_pr-merge.sh", "lever"),
            ("home/dot_agents/omp/policies/orchestrator.yml", "policy"),
            ("home/dot_agents/agent-config.yaml", "policy"),
            ("scripts/orchestrator/hcom-seat", "credential"),
            ("scripts/orchestrator/acp-broker", "credential"),
            ("scripts/orchestrator/seat-token-place", "credential"),
            ("scripts/orchestrator/seat-login-preflight", "credential"),
            ("home/dot_local/bin/common/executable_hcom-seat", "credential"),
            ("home/dot_local/bin/common/executable_acp-broker", "credential"),
            ("home/dot_local/bin/common/executable_seat-token-place", "credential"),
            ("home/dot_local/bin/common/executable_seat-login-preflight", "credential"),
            ("home/.chezmoiscripts/run_once_before_10-install.sh.tmpl", "credential"),
            ("home/dot_local/bin/executable_tool", "deployed-executable"),
            ("home/dot_dsh/plugins/thak/index.js", "deployed-executable"),
            ("install/bootstrap.sh", "deployed-executable"),
        ):
            with self.subTest(path):
                self.assertEqual(self.reader.path_class(path), name)

    def test_a_mixed_head_takes_the_first_class_in_precedence(self):
        self.assertEqual(self.reader.sweep_required([*DOCS, LEVER_PATH]), "lever")
        self.assertEqual(self.reader.sweep_required([LEVER_PATH, CREDENTIAL]), "credential")
        self.assertEqual(self.reader.sweep_required([DEPLOYED, LEVER_PATH]), "lever")
        self.assertEqual(self.reader.sweep_required([DEPLOYED, POLICY, *DOCS]), "policy")
        self.assertEqual(self.reader.sweep_required([*DOCS, DEPLOYED]), "deployed-executable")
        self.assertEqual(self.reader.answer([*DOCS, DEPLOYED]), "required deployed-executable")

    def test_a_head_outside_every_class_requires_nothing(self):
        """Docs, tests, CI scripts and workflows, the Makefile, a sibling whose name only starts with a prefix, the
        manifest's neighbours and a prefix without its slash are no class."""
        outside = (
            *DOCS,
            "scripts/ci/run-on-lint-files.sh",
            "scripts/generate-agent-configs.py",
            "scripts/orchestratorx/a.sh",
            "scripts/orchestrator",
            "home/dot_agents/agent-config.yaml.bak",
            "home/dot_agents/permgate-policy.yaml",
            "home/dot_local/binx/a",
            "home/dot_local/share/a",
            "install",
            "installer/a.sh",
            "home/dot_dsh/profiles/thak/package.json",
            "home/chezmoiscripts/a",
        )
        for path in outside:
            with self.subTest(path):
                self.assertIsNone(self.reader.path_class(path))
        self.assertIsNone(self.reader.sweep_required(outside))
        self.assertEqual(self.reader.answer(outside), "not-required")

    def test_a_quoted_or_backslashed_path_is_unreadable_never_a_class(self):
        """U597 round 2 (verdict finding 3): git prints a path with a tab or a non-ASCII byte C-quoted, with the
        quotes, and such a text matched no prefix, so a quoted lever path skipped the sweep. check_path refuses a path
        that starts with `"` or holds a backslash; the plain paths beside it stay readable."""
        for path in (
            '"scripts/orchestrator/a\\tb.sh"',
            '"docs/\\303\\244.md"',
            "scripts/orchestrator/a\\b.sh",
            "docs/a\\b.md",
            '"',
            '"docs/a.md"',
        ):
            with self.subTest(path):
                with self.assertRaises(self.reader.Unreadable) as caught:
                    self.reader.check_path(path)
                self.assertIn("is C-quoted or holds a backslash", str(caught.exception))
                with self.assertRaises(self.reader.Unreadable):
                    self.reader.paths_from_files_json(listing("docs/plan.md", path))
        self.assertEqual(self.reader.check_path("scripts/orchestrator/a b.sh"), "scripts/orchestrator/a b.sh")
        self.assertEqual(self.reader.check_path("docs/ä.md"), "docs/ä.md")

    def test_the_files_listing_is_read_as_data_both_paths_of_a_rename_counting(self):
        """Round 3 (verdict finding 2): each line is `[status, filename, previous_filename]`; the filename and, for a
        rename or a copy, the source are the paths; every status of the API is accepted with a null source; round 5:
        the entries are counted beside the paths, and nothing is held to a count from outside the listing."""
        text = (
            entry("docs/a.md", "added")
            + "\n"
            + entry("docs/b.md", "removed")
            + "\n"
            + entry("docs/c.md", "modified")
            + "\n"
            + entry("docs/d.md", "renamed", "scripts/orchestrator/d.py")
            + "\n"
            + entry("docs/e.md", "copied", "docs/c.md")
            + "\n"
            + entry("docs/f.md", "changed")
            + "\n"
            + entry("docs/g.md", "unchanged")
            + "\n"
        )
        paths, entries = self.reader.paths_from_files_json(text)
        self.assertEqual(
            paths,
            [
                "docs/a.md",
                "docs/b.md",
                "docs/c.md",
                "docs/d.md",
                "scripts/orchestrator/d.py",
                "docs/e.md",
                "docs/c.md",
                "docs/f.md",
                "docs/g.md",
            ],
        )
        self.assertEqual(entries, 7, "the entries, not the paths: a rename is one entry")
        self.assertEqual(self.reader.answer(paths), "required lever")
        self.assertEqual(self.reader.files_answer(text), "required lever")
        self.assertEqual(self.reader.paths_from_files_json(text.rstrip("\n")), (paths, 7), "no trailing newline")

    def test_a_listing_at_the_compare_api_s_cap_answers_required_cap_whatever_its_paths(self):
        """Round 5 (the round-4 P1 and its first P2): the compare response carries `files` on its first page alone,
        at most 300, so a listing of 300 or more entries may be cut short: `required cap`, for docs paths alone, for
        a lever path among them, and for 301 entries; 299 docs entries are whole and `not-required`, 299 with a lever
        path `required lever`; a malformed line among 300 is still refused for its shape, never answered."""
        self.assertEqual(self.reader.COMPARE_FILES_CAP, CAP)
        self.assertEqual(self.reader.CAP, "cap")
        docs = [f"docs/f{n}.md" for n in range(CAP)]
        self.assertEqual(self.reader.files_answer(listing(*docs)), "required cap")
        self.assertEqual(self.reader.files_answer(listing(*docs[:-1], LEVER_PATH)), "required cap", "the cap first")
        self.assertEqual(self.reader.files_answer(listing(*docs, "docs/more.md")), "required cap", "301 entries")
        self.assertEqual(self.reader.files_answer(listing(*docs[:-1])), "not-required", "299 entries are whole")
        self.assertEqual(self.reader.files_answer(listing(*docs[:-2], LEVER_PATH)), "required lever")
        renamed = listing(*docs[:-1]) + entry("docs/new.md", "renamed", "docs/old.md") + "\n"
        self.assertEqual(self.reader.files_answer(renamed), "required cap", "a rename is one entry of 300")
        with self.assertRaises(self.reader.Unreadable) as caught:
            self.reader.files_answer(listing(*docs[:-1]) + "garbage\n")
        self.assertIn("line 300 of the files listing is not JSON", str(caught.exception))
        self.assertNotIn("changed-files", self.reader.USAGE)

    def test_a_files_listing_of_another_shape_is_unreadable(self):
        """Round 3: a line that is not JSON, not an array of three, an unknown or non-string status, a filename that
        is no string, a rename or a copy without its source, a source on any other status, a source or a filename
        `check_path` refuses (an embedded newline is a control character of the decoded string), an empty line and an
        empty listing are each Unreadable naming the line, never a class."""
        plain = entry("docs/plan.md")
        for name, text, message in (
            ("empty", "", "names no file"),
            ("a newline alone", "\n", "line 1 of the files listing is empty"),
            ("an empty line between", f"{plain}\n\n{plain}\n", "line 2 of the files listing is empty"),
            ("not JSON", "docs/plan.md\n", "line 1 of the files listing is not JSON"),
            ("a string", '"docs/plan.md"\n', "line 1 of the files listing is not an array of three"),
            ("an object", '{"filename": "docs/plan.md"}\n', "line 1 of the files listing is not an array of three"),
            ("two items", '["modified", "docs/plan.md"]\n', "is not an array of three"),
            ("four items", '["modified", "docs/plan.md", null, 1]\n', "is not an array of three"),
            ("an unknown status", '["moved", "docs/plan.md", null]\n', "has the status 'moved', not one of added"),
            ("a null status", '[null, "docs/plan.md", null]\n', "has the status None"),
            ("a numeric filename", '["modified", 7, null]\n', "has no filename string"),
            ("a null filename", '["modified", null, null]\n', "has no filename string"),
            (
                "a rename without its source",
                f"{plain}\n" + entry("docs/old.py", "renamed") + "\n",
                "line 2 of the files listing is renamed without its source (previous_filename)",
            ),
            ("a copy without its source", entry("docs/old.py", "copied") + "\n", "is copied without its source"),
            (
                "a numeric source",
                '["renamed", "docs/new.py", 7]\n',
                "has a previous_filename that is neither a string nor null: 7",
            ),
            (
                "a boolean false source on a rename",
                '["renamed", "docs/new.py", false]\n',
                "line 1 of the files listing has a previous_filename that is neither a string nor null: False",
            ),
            (
                "a boolean false source on a modified file (the round-3 P3)",
                '["modified", "docs/plan.md", false]\n',
                "line 1 of the files listing has a previous_filename that is neither a string nor null: False",
            ),
            (
                "an object source",
                '["modified", "docs/plan.md", {}]\n',
                "has a previous_filename that is neither a string nor null: {}",
            ),
            (
                "a source on a modified file",
                entry("docs/plan.md", "modified", "scripts/orchestrator/x.py") + "\n",
                "is modified yet carries a previous_filename",
            ),
            ("a source on an added file", entry("docs/a.md", "added", "docs/b.md") + "\n", "is added yet carries"),
            ("a .. source", entry("docs/new.py", "renamed", "../etc/passwd") + "\n", "holds a '.', '..' or empty"),
            ("an absolute filename", entry("/etc/passwd") + "\n", "is absolute"),
            ("an embedded newline", entry("scripts/orchestrator/a\nb.sh") + "\n", "holds a control character"),
            ("a carriage return", entry("docs/a\r.md") + "\n", "holds a control character"),
            ("an empty filename", entry("") + "\n", "the listing holds an empty line"),
            ("a quoted filename", entry('"docs/a.md"') + "\n", "is C-quoted or holds a backslash"),
        ):
            with self.subTest(name):
                with self.assertRaises(self.reader.Unreadable) as caught:
                    self.reader.paths_from_files_json(text)
                self.assertIn(message, str(caught.exception))
                self.assertNotIn("\n", str(caught.exception), "one stderr line, the newline not echoed")

    def test_the_lever_reads_this_module_from_the_checkout_as_data(self):
        """pr-merge.sh names the module by its checkout path and runs its `--files-json` form over the compare API's
        arrays (round 4: the listing keyed by the head's sha itself, status, filename and previous_filename as data;
        round 5: one call without `--paginate`, the `files` key required by the jq, no count read of the pull request
        and no `--changed-files`), reads `required cap` as a required class with its own reason, prints the one skip
        line (U597), asks the daily sweep once on `not-required` (round 4), runs no `--stdin` form, and keeps no
        number-keyed listing and no `headRefOid,changedFiles` reread."""
        text = LEVER.read_text()
        self.assertIn("scope_reader=${toplevel}/scripts/orchestrator/sweep-scope.py", text)
        self.assertIn(READER_CALL, text)
        self.assertIn(
            f'gh_bounded api "repos/{{owner}}/{{repo}}/compare/${{base_tip}}...${{head}}" --jq {FILES_JQ}',
            text,
        )
        self.assertIn(
            "base_tip=$(gh_bounded api \"repos/{owner}/{repo}/git/ref/heads/${base}\" --jq '.object.sha') ||", text
        )
        self.assertNotIn("compare/${base}...${head}", text, "the compare is keyed by the tip read once (round 7)")
        self.assertNotIn("--paginate", text, "one compare call: the files are on the first page alone (round 5)")
        self.assertNotIn("changedFiles", text, "no count of the pull request is read (round 5)")
        self.assertNotIn("--changed-files", text, "the reader's count option is gone (round 5)")
        self.assertNotIn("pulls/${pr}/files", text, "the files endpoint keyed by the number is gone (round 4)")
        self.assertNotIn("--stdin", text, "the raw line-per-path form is gone")
        self.assertNotIn(
            "gh_bounded pr diff", text, "the name listing of gh pr diff printed a rename's destination alone"
        )
        self.assertIn("    'required cap')\n        # The listing is at the compare API's cap (round 5)", text)
        self.assertIn("        sweep_class=cap\n", text)
        self.assertIn(
            "sweep_reason=\"the head changes 300 or more files, the compare API's cap, so the listing may be cut short"
            ' and the per-head sweep stands"',
            text,
        )
        self.assertIn("sweep: not required (no lever, policy, credential or deployed-executable path changed)", text)
        self.assertEqual(text.count("require_sweep_scope\n"), 1, "called once")
        self.assertEqual(text.count("        require_daily_sweep\n"), 1, "the daily sweep asked once, on not-required")
        self.assertIn('"${ledger_copy}" "${store}" daily "${DAILY_SWEEP_MAX_AGE}"', text)
        self.assertIn("DAILY_SWEEP_MAX_AGE=86400\n", text)
        self.assertIn("[[ -z ${sweep_reason} ]] || require_sweep_row\n", text)
        self.assertEqual(self.reader.USAGE, "usage: sweep-scope.py <base> <head> | sweep-scope.py --files-json")


class SweepScopeCliTest(unittest.TestCase):
    """The CLI as pr-merge.sh and the coordinator run it, `python3 -I -S sweep-scope.py ...`, in a scratch
    repository with a base commit and heads that change docs, a lever and a credential lever."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        self.env = quiet_git_env(
            {
                "PATH": os.environ["PATH"],
                "HOME": str(self.root / "home"),
                "LC_ALL": "C",
                "GIT_CONFIG_GLOBAL": str(gitconfig),
                "GIT_CONFIG_NOSYSTEM": "1",
            }
        )
        (self.root / "home").mkdir()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git_init(self.repo, env=self.env)
        for path in (*DOCS, LEVER_PATH, CREDENTIAL, "scripts/orchestrator/old.py"):
            self.write(path, "base\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        self.base = self.git("rev-parse", "HEAD")
        self.docs_head = self.head("docs", {DOCS[0]: "docs\n", DOCS[2]: "tests\n"})
        self.lever_head = self.head("lever", {LEVER_PATH: "lever\n", DOCS[0]: "docs\n"})
        self.mixed_head = self.head("mixed", {LEVER_PATH: "lever\n", CREDENTIAL: "seat\n", DOCS[1]: "readme\n"})

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.repo, env=self.env, check=True, capture_output=True, text=True
        ).stdout.strip()

    def head(self, name, changes):
        """A branch `name` off the base with `changes` committed; returns its sha, main checked out again."""
        self.git("switch", "-q", "-c", name, self.base)
        for path, text in changes.items():
            self.write(path, text)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", name)
        sha = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        return sha

    def run_reader(self, *args, cwd=None, stdin=None):
        return subprocess.run(
            [sys.executable, "-I", "-S", str(READER), *args],
            cwd=cwd or self.repo,
            env=self.env,
            input=stdin,
            capture_output=True,
            timeout=60,
            check=False,
        )

    def assert_answer(self, run, answer):
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, f"{answer}\n".encode(), b""))

    def assert_refused(self, run, message):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(run.stdout, b"", "no answer")
        stderr = run.stderr.decode()
        self.assertEqual(stderr.count("\n"), 1, f"one stderr line: {stderr!r}")
        self.assertTrue(stderr.startswith("sweep-scope: "), stderr)
        self.assertIn(message, stderr)

    def test_the_git_form_answers_from_the_paths_changed_since_the_merge_base(self):
        self.assert_answer(self.run_reader(self.base, self.docs_head), "not-required")
        self.assert_answer(self.run_reader(self.base, self.lever_head), "required lever")
        self.assert_answer(self.run_reader(self.base, self.mixed_head), "required credential")
        # the base may be a ref, and main moved past the merge base changes nothing for the head
        self.assert_answer(self.run_reader("main", self.lever_head), "required lever")
        self.write(CREDENTIAL, "main moved\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "main moved")
        self.assert_answer(self.run_reader("main", self.docs_head), "not-required")
        self.assert_answer(self.run_reader("main", self.lever_head), "required lever")

    def test_the_git_form_lists_both_paths_of_a_rename(self):
        """A lever file renamed out of its directory still changed a lever path (`--no-renames`)."""
        self.git("switch", "-q", "-c", "renamed", self.base)
        self.git("mv", "scripts/orchestrator/old.py", "docs/old.py")
        self.git("commit", "-q", "-m", "renamed")
        renamed = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        self.assert_answer(self.run_reader(self.base, renamed), "required lever")

    def test_the_git_form_ignores_diff_relative_and_the_directory_it_runs_from(self):
        """Round 3 (verdict finding 6): `diff.relative=true` in the repository's config narrows `git diff` to the
        current subdirectory and strips its prefix, so from `tests/unit` the lever head answered `not-required`. The
        command carries `-c diff.relative=false` and `--no-relative`: from the toplevel, from `docs/`, from
        `tests/unit` and from `scripts/orchestrator`, with the setting on and off, every head answers as from the
        toplevel, the lever head `required lever` and the mixed head `required credential`."""
        subdirectories = (self.repo, self.repo / "docs", self.repo / "tests/unit", self.repo / "scripts/orchestrator")
        expected = (
            (self.docs_head, "not-required"),
            (self.lever_head, "required lever"),
            (self.mixed_head, "required credential"),
        )
        for setting in ("true", "false"):
            self.git("config", "diff.relative", setting)
            for cwd in subdirectories:
                for head, answer in expected:
                    with self.subTest(setting=setting, cwd=str(cwd.relative_to(self.repo)) or ".", head=answer):
                        self.assert_answer(self.run_reader(self.base, head, cwd=cwd), answer)
        # the setting on, the same command without the guard would have narrowed the listing: the guard is live
        self.git("config", "diff.relative", "true")
        narrowed = subprocess.run(
            ["git", "diff", "--name-only", "--no-renames", f"{self.base}...{self.lever_head}", "--"],
            cwd=self.repo / "tests/unit",
            env=self.env,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.assertNotIn("scripts/orchestrator", narrowed, "git's own relative listing lacks the lever path")
        self.assert_answer(self.run_reader(self.base, self.lever_head, cwd=self.repo / "tests/unit"), "required lever")

    def test_a_failed_git_read_is_exit_2_with_one_line_never_not_required(self):
        """Standing order 21: a head git cannot resolve, a base it cannot resolve, a directory outside a repository,
        and two revisions with no change between them are each exit 2 naming the read, with no answer."""
        self.assert_refused(self.run_reader(self.base, "f" * 40), "git diff --name-only")
        self.assert_refused(self.run_reader("nonexistent-ref", self.docs_head), "git diff --name-only")
        outside = self.root / "outside"
        outside.mkdir()
        self.assert_refused(self.run_reader(self.base, self.docs_head, cwd=outside), "git diff --name-only")
        self.assert_refused(self.run_reader(self.base, self.base), "names no changed path")
        self.assert_refused(self.run_reader(self.base, "-x"), "is not a revision")
        self.assert_refused(self.run_reader("-x", self.docs_head), "usage: sweep-scope.py")

    def test_the_files_json_form_answers_from_the_listing(self):
        """The files as the lever's compare API read prints them, one JSON array per line, with or without the last
        newline; a rename's or a copy's source counts; 300 entries answer `required cap` and 299 the classes (round 5)."""
        docs = listing("docs/plan.md", "README.md")
        self.assert_answer(self.run_reader("--files-json", stdin=docs.encode()), "not-required")
        self.assert_answer(self.run_reader("--files-json", stdin=docs.rstrip("\n").encode()), "not-required")
        self.assert_answer(self.run_reader("--files-json", stdin=listing(DOCS[0], POLICY).encode()), "required policy")
        self.assert_answer(
            self.run_reader("--files-json", stdin=listing(LEVER_PATH, CREDENTIAL).encode()), "required credential"
        )
        self.assert_answer(
            self.run_reader("--files-json", stdin=listing(DEPLOYED).encode()), "required deployed-executable"
        )
        self.assert_answer(
            self.run_reader("--files-json", stdin=listing("home/dot_agents/agent-config.yaml").encode()),
            "required policy",
        )
        renamed = entry("docs/old.py", "renamed", "scripts/orchestrator/old.py") + "\n" + entry("docs/plan.md") + "\n"
        self.assert_answer(self.run_reader("--files-json", stdin=renamed.encode()), "required lever")
        copied = entry("docs/copy.py", "copied", "install/bootstrap.sh") + "\n"
        self.assert_answer(self.run_reader("--files-json", stdin=copied.encode()), "required deployed-executable")
        capped = listing(*(f"docs/f{n}.md" for n in range(CAP)))
        self.assert_answer(self.run_reader("--files-json", stdin=capped.encode()), "required cap")
        whole = listing(*(f"docs/f{n}.md" for n in range(CAP - 1)))
        self.assert_answer(self.run_reader("--files-json", stdin=whole.encode()), "not-required")

    def test_a_files_listing_of_another_shape_is_exit_2_never_not_required(self):
        """Round 3: an empty listing, a line that is not JSON or not an array of three, a rename without its source, a
        source on a modified file, an embedded newline, a C-quoted name (round 2) and bytes that are not UTF-8 are
        each refused naming the shape, never read as `not-required`; round 5: the `--changed-files` count is gone, so
        a listing is held to no number from outside it, and one of 3,000 entries is `required cap`."""
        plain = entry("docs/plan.md")
        for name, text, message in (
            ("empty", b"", "names no file"),
            ("a newline alone", b"\n", "line 1 of the files listing is empty"),
            ("not JSON", b"docs/plan.md\n", "line 1 of the files listing is not JSON"),
            ("two items", b'["modified", "docs/plan.md"]\n', "is not an array of three"),
            ("an unknown status", b'["moved", "docs/plan.md", null]\n', "has the status 'moved'"),
            (
                "a rename without its source",
                (plain + "\n" + entry("docs/old.py", "renamed") + "\n").encode(),
                "line 2 of the files listing is renamed without its source",
            ),
            (
                "a source on a modified file",
                (entry("docs/plan.md", "modified", "docs/x.md") + "\n").encode(),
                "is modified yet carries a previous_filename",
            ),
            (
                "an embedded newline",
                (entry("scripts/orchestrator/a\nb.sh") + "\n").encode(),
                "holds a control character",
            ),
            ("an absolute path", (entry("/etc/passwd") + "\n").encode(), "is absolute"),
            (
                "a .. component",
                (entry("docs/../scripts/x") + "\n").encode(),
                "holds a '.', '..' or empty component",
            ),
            (
                "a C-quoted lever path",
                (entry('"scripts/orchestrator/a\\tb.sh"') + "\n").encode(),
                "is C-quoted or holds a backslash",
            ),
            ("not UTF-8", b'["modified", "docs/\xff.md", null]\n', "not UTF-8"),
        ):
            with self.subTest(name):
                self.assert_refused(self.run_reader("--files-json", stdin=text), message)
        capped = listing(*(f"docs/f{n}.md" for n in range(3000)))
        self.assert_answer(self.run_reader("--files-json", stdin=capped.encode()), "required cap")

    def test_usage_is_exit_2(self):
        docs = listing("docs/a.md").encode()
        for args in (
            (),
            (self.base,),
            (self.base, self.docs_head, "x"),
            ("--files-json", "x"),
            ("--files-json", "--changed-files"),
            ("--files-json", "--changed-files", "2"),
            ("--files-json", "--count", "1"),
            ("--stdin",),
            ("--other",),
        ):
            with self.subTest(args=args):
                self.assert_refused(self.run_reader(*args, stdin=docs), "usage: sweep-scope.py")


class SweepRuleDocumentsTest(unittest.TestCase):
    """U597 round 2 (verdict finding 5): the module is the one definition of the classes, and the documents that state
    the rule follow it: AGENTS.md's Audit sweep rule line names every prefix of CLASSES and the four classes, the
    hcom-orchestration skill's step 4 and the orchestrator README's pr-merge.sh row name the four classes and the
    module; round 3: the listing as data (status, filename, previous_filename); round 4: the listing keyed by the
    head's sha and the daily row; round 5: one compare call, no count of the pull request, the cap answer, in
    AGENTS.md's line and the README's row. The regime template `home/dot_agents/regime/AGENTS-audit-section.md` is
    AGENTS.md's section byte for byte (tests.unit.test_regime_init), so it is not read here."""

    def setUp(self):
        self.reader = load_reader()

    def rule_line(self):
        """The one line of AGENTS.md's `## Audit` section that states the sweep rule."""
        text = AGENTS.read_text()
        start = text.index("\n## Audit\n") + 1
        end = text.find("\n## ", start)
        lines = [
            line for line in text[start:end].splitlines() if line.startswith("- A unit whose head changes a lever")
        ]
        self.assertEqual(len(lines), 1, "one sweep rule line in the Audit section")
        return lines[0]

    def assert_names_the_classes(self, text, where):
        for word in CLASS_WORDS:
            self.assertIn(word, text, f"{where} names the class {word!r}")
        self.assertIn("`scripts/orchestrator/sweep-scope.py`", text, f"{where} names the one definition")
        self.assertNotIn(
            "Every unit and every program milestone", text, f"{where} no longer states the every-unit rule"
        )

    def assert_describes_the_listing_keyed_by_the_head(self, text, where, pr):
        """The listing keyed by the head's sha (round 4), its three fields as data, one call whose completeness is
        the listing's own, the cap answer (round 5), and no number-keyed listing, head reread or count read."""
        self.assertIn(
            "`gh api 'repos/{owner}/{repo}/compare/<main tip>...<head>'`",
            text,
            f"{where} names the compare API keyed by main's tip and the sha",
        )
        self.assertNotIn("compare/main...<head>", text, f"{where} no longer names the compare keyed by the name main")
        self.assertIn("one call", text, f"{where} names the one call")
        self.assertNotIn(
            "compare/<main tip>...<head>' --paginate", text, f"{where} names no paging of the compare call"
        )
        # round 7: main's tip pinned, the merge base held to it, the up-to-date requirement
        self.assertIn("main's tip", text, f"{where} names main's tip as the base side of the compare")
        self.assertIn("`merge_base_commit.sha`", text, f"{where} names the merge base read beside the files")
        self.assertIn("up to date", text, f"{where} names the up-to-date requirement")
        self.assertIn("the diff the squash lands", text, f"{where} names what the listing is")
        for field in ("`status`", "`filename`", "`previous_filename`"):
            self.assertIn(field, text, f"{where} names the field {field}")
        self.assertIn("`required cap`", text, f"{where} names the cap answer")
        self.assertIn("300", text, f"{where} names the cap")
        self.assertNotIn("changedFiles", text, f"{where} names no count read of the pull request")
        self.assertNotIn("distinct filenames", text, f"{where} holds the listing to no count from outside it")
        self.assertNotIn(f"pulls/{pr}/files", text, f"{where} names no listing keyed by the pull request's number")

    def assert_describes_the_daily_sweep(self, text, where):
        """The exemption bound to its standing control (round 4): the daily row's file, its writer, the window, and
        no sentence saying the lever never reads it."""
        self.assertIn("`daily-sweeps.tsv`", text, f"{where} names the daily sweep file")
        self.assertIn("`ledger-row.py daily`", text, f"{where} names the row's writer")
        self.assertIn("24 hours", text, f"{where} names the window")
        self.assertNotIn("no merge gate reads", text, f"{where} no longer says the lever never reads the daily sweep")
        self.assertNotIn("never reads", text, f"{where} no longer says the lever never reads the daily sweep")

    def test_the_agents_md_rule_line_names_every_prefix_and_the_four_classes(self):
        line = self.rule_line()
        self.assert_names_the_classes(line, "AGENTS.md's sweep rule")
        for name, prefixes in self.reader.CLASSES:
            for prefix in prefixes:
                with self.subTest(prefix):
                    self.assertIn(f"`{prefix}`", line, f"the {name} prefix {prefix} is in the AGENTS.md rule line")
        # the daily sweep of main, the compare API keyed by the sha and the daily row are the rule's, too
        self.assertIn("one full sweep per UTC day", line)
        self.assert_describes_the_listing_keyed_by_the_head(line, "AGENTS.md's sweep rule", "<n>")
        self.assert_describes_the_daily_sweep(line, "AGENTS.md's sweep rule")
        self.assertIn("`home/dot_agents/regime/daily-sweep-brief.md`", line)
        self.assertIn("`ledger.py daily 86400`", line)
        self.assertNotIn("briefs/daily-sweep.md", line, "the template is the kit's, not a store file")
        # round 8: the validators' pins, the daily task's day, the readers' pinned copies and the parent check
        self.assertIn("`assets.security-audit-skill.validators_sha256`", line)
        self.assertIn("task id `daily-<YYYY-MM-DD>` alone naming the UTC day", line)
        self.assertIn("from private copies hashed against their `claude.levers.sha256` pins", line)
        self.assertIn("the merge commit's first parent", line)

    def test_the_skill_s_step_four_names_the_four_classes_and_the_module(self):
        text = SKILL.read_text()
        match = re.search(r"^4\. .*$", text, re.MULTILINE)
        self.assertIsNotNone(match, "step 4 of the loop")
        step = match.group(0)
        self.assert_names_the_classes(step, "the skill's step 4")
        self.assertIn("A unit whose head changes a lever, a policy, credential handling or a deployed executable", step)
        self.assertIn("skips the row for every other head", step)
        # round 3 (verdict finding 9): the daily sweep and the classes cite the operator's sweep rule C, not standing
        # order 44, which governs executed tests
        self.assertIn("the operator's sweep rule C of 2026-11-18", step)
        self.assertNotIn("standing order 44", step)
        # round 4: the coordinator's daily dispatch from the kit's template, its row, and the lever's read of it
        self.assertIn("once per UTC day", step)
        self.assertIn("`~/.agents/regime/daily-sweep-brief.md`", step)
        self.assert_describes_the_daily_sweep(step, "the skill's step 4")

    def test_the_readme_s_pr_merge_row_names_the_four_classes_and_the_module(self):
        rows = [
            line for line in README.read_text().splitlines() if line.startswith("| `~/.local/bin/common/pr-merge.sh *`")
        ]
        self.assertEqual(len(rows), 1, "one pr-merge.sh row in the lever table")
        row = rows[0]
        self.assert_names_the_classes(row, "the README's pr-merge.sh row")
        self.assertNotIn("`gh pr diff <pr> --name-only`", row)
        self.assert_describes_the_listing_keyed_by_the_head(row, "the README's pr-merge.sh row", "<pr>")
        self.assert_describes_the_daily_sweep(row, "the README's pr-merge.sh row")
        # round 8: the readers' pinned copies and the merge commit's parent check
        self.assertIn("private copies", row)
        self.assertIn("`claude.levers.sha256`", row)
        self.assertIn("first parent", row)
        self.assertIn("`strict_required_status_checks_policy`", row)

    def test_the_lever_s_comments_describe_the_listing_as_it_is(self):
        """The lever's header and the three functions' descriptions name the jq form, the reader's form, the one
        call, the cap answer, the daily row, the symlink-free components and no retired form."""
        text = LEVER.read_text()
        self.assertIn(f"--jq {FILES_JQ}", text, "the jq form, in the call")
        self.assertIn("`gh api 'repos/{owner}/{repo}/git/ref/heads/main' --jq '.object.sha'`", text, "the tip read")
        self.assertIn(
            "`gh api 'repos/{owner}/{repo}/compare/<main tip>...<head>'", text, "the compare keyed by the tip"
        )
        self.assertIn(
            "the three-dot diff equals the\n#   two-dot diff against the tip, the diff the squash lands", text
        )
        self.assertNotIn("compare/main...<head>", text, "no compare keyed by the name main (round 7)")
        self.assertIn('[.status, .filename, (if has("previous_filename") then .previous_filename else null end)]', text)
        self.assertIn(
            'error("files is " + (.files | type) + ", not an array")', text, "the array check named in the prose"
        )
        self.assertEqual(
            text.count('(.files // error("no files key"))'),
            1,
            "the round-5 projection, which iterated an object's values, is named once as history and runs nowhere",
        )
        self.assertIn("`sweep-scope.py --files-json`", text)
        # round 8: the readers' pins and copies, and the parent check with the ruleset's policy
        self.assertIn("`claude.levers.sha256.sweep-scope.py`", text)
        self.assertIn("reader_copy", text)
        self.assertIn("`~/.local/bin/common/sweep-scope.py`", text)
        self.assertIn("--jq '.parents[0].sha'`", text)
        self.assertIn("`strict_required_status_checks_policy: false`", text)
        self.assertIn("`required cap`", text)
        self.assertIn("`daily-sweeps.tsv`", text)
        self.assertIn("`ledger-row.py daily`", text)
        self.assertIn("`ledger.py <store> daily 86400`", text)
        self.assertIn("every\n#   directory component between `sweeps/` and the file a directory of this user", text)
        self.assertNotIn("changedFiles", text, "the count read is gone (round 5)")
        self.assertNotIn("--changed-files", text, "the reader's count option is gone (round 5)")
        self.assertNotIn("--paginate", text, "the compare call is one (round 5)")
        self.assertNotIn("(.previous_filename // null)", text, "the round-3 projection mapped a boolean to null")
        self.assertNotIn(".filename, (.previous_filename // empty)", text, "the line-per-path form is gone")
        self.assertNotIn("pulls/<pr>/files", text, "the number-keyed listing is gone")
        self.assertNotIn("--stdin", text)


if __name__ == "__main__":
    unittest.main()
