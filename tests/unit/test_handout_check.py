"""Exercise scripts/orchestrator/handout-check.py (regime-cutover U649, standing order 61) as a subprocess under
`python3 -I -S` over a scratch store: a passing set, a file without the sentence, a file with the sentence altered by
one character or split over two lines, files given in place of the glob, the glob default over `handouts/plan-*.md`
and `status-*.md`, the store-shape refusals program-status.py shares (the reader spelled the same in both levers), and
the pinned-module form (the twin byte-identical under its bare name, mode 0644, one pin, an altered copy refused, the
installed copy reading the deployed manifest)."""

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
CHECK = ROOT / "scripts/orchestrator/handout-check.py"
TWIN = ROOT / "home/dot_local/bin/common/handout-check.py"
STATUS = ROOT / "scripts/orchestrator/program-status.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"

GOAL = "omp at the bottom, DSH in control, the whole kit inside the sandbox, both hosts driving other projects on their own."
HANDOFF = f"# Purpose and goal\n\nThe one goal; not a character of it changes.\n\n> {GOAL}\n\n> not the goal\n"
PLAN = f"# Plan\n\n> {GOAL}\n\n- TODO by goal element\n"
STATUS_TEXT = f"# Status at 2026-11-20T08:00Z\n\nThe goal: {GOAL} The distance follows.\n"
LACKING = "# Plan\n\nNo sentence here.\n"


class HandoutCheckTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.store = root / "regime-cutover"
        (self.store / "handoff").mkdir(parents=True)
        (self.store / "handouts").mkdir()
        self.write_handoff(HANDOFF)
        self.home = root / "home"
        self.home.mkdir()
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}
        self.copy_lever()

    def write_handoff(self, text):
        (self.store / "handoff/08-purpose-and-goal.md").write_text(text, encoding="utf-8")

    def write_handout(self, name, text):
        path = self.store / "handouts" / name
        path.write_text(text, encoding="utf-8")
        return str(path)

    def copy_lever(self):
        """A checkout-shaped copy of the lever two levels below a copy of the manifest, so the self check passes on
        the copy and the copy can be altered."""
        checkout = Path(self.temp.name).resolve() / "checkout"
        levers = checkout / "scripts/orchestrator"
        levers.mkdir(parents=True, exist_ok=True)
        (checkout / "home/dot_agents").mkdir(parents=True, exist_ok=True)
        shutil.copy2(MANIFEST, checkout / "home/dot_agents/agent-config.yaml")
        shutil.copy2(CHECK, levers / CHECK.name)
        self.lever = levers / CHECK.name
        return self.lever

    def run_check(self, *argv, lever=None):
        """The lever under `python3 -I -S` with exactly `argv` after it."""
        return subprocess.run(
            [sys.executable, "-I", "-S", str(lever or self.lever), *argv],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )

    def assert_ok(self, run, *paths):
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        expected = "".join(f"handout-check: ok {path}\n" for path in paths) + f"handout-check: {len(paths)} files, ok\n"
        self.assertEqual(run.stdout, expected)

    def assert_refused(self, run, *reasons):
        """Exit 2, one stderr line naming each reason, nothing on stdout."""
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith("handout-check.py: refused: "), run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        for reason in reasons:
            self.assertIn(reason, run.stderr)

    def store_listing(self):
        return sorted(str(path.relative_to(self.store)) for path in self.store.rglob("*"))

    # (a) the verdicts: a passing set, a lacking file, an altered sentence, a split sentence.

    def test_a_passing_set_prints_one_ok_line_per_file_in_name_order_and_the_count_and_writes_nothing(self):
        plan = self.write_handout("plan-current.md", PLAN)
        status = self.write_handout("status-2026-11-20.md", STATUS_TEXT)
        self.write_handout("notes.md", LACKING)  # not a plan or status handout: never read
        self.write_handout("plan-draft.txt", LACKING)  # not markdown: never read
        before = self.store_listing()
        self.assert_ok(self.run_check(str(self.store)), plan, status)
        self.assertEqual(self.store_listing(), before, "the lever writes no file")

    def test_a_file_without_the_sentence_altered_by_one_character_or_split_over_two_lines_fails_by_name(self):
        lacking = self.write_handout("plan-a.md", LACKING)
        altered = self.write_handout("plan-b.md", PLAN.replace("DSH in control", "DSh in control"))
        self.assertEqual(sum(a != b for a, b in zip(GOAL, GOAL.replace("DSH in control", "DSh in control"))), 1)
        split = self.write_handout("plan-c.md", PLAN.replace("the whole kit", "the whole\nkit"))
        passing = self.write_handout("status-d.md", STATUS_TEXT)
        run = self.run_check(str(self.store))
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertEqual(run.stdout, f"handout-check: ok {passing}\n", "the passing file's line, no count")
        self.assertEqual(
            run.stderr,
            "".join(
                f"handout-check: {path} lacks the goal sentence on one line\n" for path in (lacking, altered, split)
            ),
        )
        self.assertNotIn("Traceback", run.stderr)

    def test_the_sentence_is_held_verbatim_wherever_it_sits_on_the_line(self):
        inline = self.write_handout("status-a.md", f"Status. {GOAL} More.\n")
        quoted = self.write_handout("plan-b.md", f"> {GOAL}\n")
        bare = self.write_handout("plan-c.md", GOAL)  # no trailing newline
        self.assert_ok(self.run_check(str(self.store)), quoted, bare, inline)
        # a sentence truncated by its last character, or with one character added inside, is not the sentence
        for name, text in (("plan-d.md", GOAL[:-1] + "\n"), ("plan-e.md", GOAL.replace(", DSH", ",  DSH") + "\n")):
            with self.subTest(name=name):
                path = self.write_handout(name, text)
                run = self.run_check(str(self.store), path)
                self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
                self.assertEqual(run.stderr, f"handout-check: {path} lacks the goal sentence on one line\n")

    def test_a_crlf_handout_whose_line_holds_the_sentence_passes_byte_exact(self):
        path = self.store / "handouts/status-crlf.md"
        path.write_bytes(STATUS_TEXT.replace("\n", "\r\n").encode("utf-8"))
        self.assert_ok(self.run_check(str(self.store)), str(path))

    # (b) files given in place of the glob.

    def test_files_given_are_the_files_checked_and_the_store_s_handouts_are_not_read(self):
        self.write_handout("plan-failing.md", LACKING)  # the glob would fail on it; a given file list skips it
        draft = Path(self.temp.name).resolve() / "draft.md"
        draft.write_text(PLAN, encoding="utf-8")
        other = Path(self.temp.name).resolve() / "other.md"
        other.write_text(LACKING, encoding="utf-8")
        self.assert_ok(self.run_check(str(self.store), str(draft)), str(draft))
        run = self.run_check(str(self.store), str(draft), str(other))
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertEqual(run.stdout, f"handout-check: ok {draft}\n")
        self.assertEqual(run.stderr, f"handout-check: {other} lacks the goal sentence on one line\n")
        # a given file is printed as given, not resolved
        relative = os.path.relpath(draft, self.store)
        run = subprocess.run(
            [sys.executable, "-I", "-S", str(self.lever), str(self.store), relative],
            capture_output=True,
            text=True,
            env=self.env,
            cwd=self.store,
            timeout=60,
            check=False,
        )
        self.assert_ok(run, relative)

    # (c) the glob default.

    def test_the_glob_default_takes_plan_and_status_markdown_files_alone_and_no_file_is_zero_files_ok(self):
        run = self.run_check(str(self.store))
        self.assert_ok(run)
        self.assertEqual(run.stdout, "handout-check: 0 files, ok\n")
        for name in (
            "plan.md",
            "Plan-y.md",  # not `Plan-x.md`: on a case-insensitive file system that is the matched file's own entry
            "plan-x.markdown",
            "x-plan-y.md",
            "statusx.md",
            "status-.txt",
            "README.md",
        ):
            self.write_handout(name, LACKING)  # outside the glob: never read, so their lack fails nothing
        plan = self.write_handout("plan-x.md", PLAN)
        dash = self.write_handout("plan-.md", PLAN)
        status = self.write_handout("status-2026-11-20-codex-outage.md", STATUS_TEXT)
        self.assert_ok(self.run_check(str(self.store)), dash, plan, status)

    # (d) the refusals: the store's shape, the handoff file as program-status.py reads it, the handouts directory.

    def test_a_store_that_is_no_directory_or_cannot_be_read_refuses(self):
        self.assert_refused(self.run_check(str(self.store / "handoff/08-purpose-and-goal.md")), "not a directory")
        self.assert_refused(self.run_check(str(self.store / "missing")), "cannot be read")
        self.assert_refused(self.run_check(str(self.store) + "\nmissing"), "cannot be read")

    def test_the_handoff_file_refusals_are_program_status_py_s_spelled_the_same(self):
        path = str(self.store / "handoff/08-purpose-and-goal.md")
        self.write_handout("plan-current.md", PLAN)
        (self.store / "handoff/08-purpose-and-goal.md").unlink()
        self.assert_refused(self.run_check(str(self.store)), f"{path} is missing", "goal sentence")
        cases = (
            ("# Purpose\n\nno quote line\n", ("no Markdown quote line",)),
            ("", ("no Markdown quote line",)),
            ("# title\n> \n> the real one\n", ("line 2", "empty quote line")),
            ("# title\n> a\tb\n", ("line 2", "holds a tab")),
            ("# title\n> a\x1bb\n", ("line 2", "holds a control character")),
            ("# title\n> the goal\r\n", ("line 2", "holds a control character")),
            ("# title\n> a\u2028b\n", ("line 2", "holds a control character")),
            ("# title\n> " + "x" * 1025 + "\n", ("line 2", "is 1025 bytes, more than 1024")),
        )
        for text, reasons in cases:
            with self.subTest(text=text[:16]):
                self.write_handoff(text)
                self.assert_refused(self.run_check(str(self.store)), path, *reasons)
        (self.store / "handoff/08-purpose-and-goal.md").write_bytes(b"> \xff\n")
        self.assert_refused(self.run_check(str(self.store)), path, "not UTF-8")
        # the bound passes at 1024 bytes and the first quote line is the sentence, a `>` without a space included
        self.write_handoff("> " + "x" * 1024 + "\n")
        passing = self.write_handout("plan-long.md", "x" * 1024 + "\n")
        self.assert_ok(self.run_check(str(self.store), passing), passing)
        self.write_handoff("A > B\n>the sentence\n> not this\n")
        first = self.write_handout("plan-first.md", "the sentence\n")
        second = self.write_handout("plan-second.md", "not this\n")
        run = self.run_check(str(self.store), first, second)
        self.assertEqual((run.returncode, run.stdout), (1, f"handout-check: ok {first}\n"), run.stderr)
        self.assertEqual(run.stderr, f"handout-check: {second} lacks the goal sentence on one line\n")

    def test_the_goal_reader_is_one_text_in_both_levers(self):
        """The two levers read the sentence by one reader spelled the same, so a handout the check passes is the one
        the report prints: the `goal_sentence` function and the constants it reads are byte-identical in both."""
        pattern = re.compile(r"^def goal_sentence\(store\):\n.*?(?=^\S)", re.MULTILINE | re.DOTALL)
        check, status = CHECK.read_text(encoding="utf-8"), STATUS.read_text(encoding="utf-8")
        check_reader, status_reader = pattern.search(check), pattern.search(status)
        self.assertIsNotNone(check_reader)
        self.assertIsNotNone(status_reader)
        self.assertEqual(check_reader.group(0), status_reader.group(0))
        for constant in (
            'GOAL_FILE = os.path.join("handoff", "08-purpose-and-goal.md")\n',
            "GOAL_MAX_BYTES = 1024\n",
            'GOAL_WHY = "the goal sentence is read from its first Markdown quote line"\n',
            'CONTROL = re.compile(r"[\\x00-\\x1f\\x7f-\\x9f\\u2028\\u2029]")\n',
        ):
            self.assertIn(constant, check)
            self.assertIn(constant, status)

    def test_a_missing_or_unlistable_handouts_directory_and_a_matching_entry_that_is_no_regular_file_refuse(self):
        handouts = self.store / "handouts"
        shutil.rmtree(handouts)
        self.assert_refused(self.run_check(str(self.store)), f"{handouts} is missing")
        handouts.write_text("a file, not a directory\n")
        self.assert_refused(self.run_check(str(self.store)), f"cannot list {handouts}")
        handouts.unlink()
        handouts.mkdir()
        self.write_handout("plan-current.md", PLAN)
        (handouts / "plan-dir.md").mkdir()
        self.assert_refused(self.run_check(str(self.store)), f"{handouts / 'plan-dir.md'} is not a regular file")
        (handouts / "plan-dir.md").rmdir()
        (handouts / "status-link.md").symlink_to(handouts / "plan-current.md")
        self.assert_refused(self.run_check(str(self.store)), f"{handouts / 'status-link.md'} is not a regular file")
        (handouts / "status-link.md").unlink()
        if os.geteuid() != 0:
            handouts.chmod(0)
            self.addCleanup(handouts.chmod, 0o755)
            self.assert_refused(self.run_check(str(self.store)), f"cannot list {handouts}")

    def test_a_file_given_or_matched_that_is_missing_unreadable_or_not_utf_8_refuses_and_nothing_prints(self):
        passing = self.write_handout("plan-a.md", PLAN)
        missing = str(self.store / "handouts/plan-missing.md")
        self.assert_refused(self.run_check(str(self.store), passing, missing), f"{missing} is missing")
        binary = self.store / "handouts/status-b.md"
        binary.write_bytes(b"\xff\xfe not text\n")
        self.assert_refused(self.run_check(str(self.store)), f"{binary} is not UTF-8")
        self.assert_refused(self.run_check(str(self.store), passing, str(binary)), f"{binary} is not UTF-8")
        binary.unlink()
        self.assert_refused(self.run_check(str(self.store), str(self.store / "handouts")), "cannot read")
        if os.geteuid() != 0:
            unreadable = self.store / "handouts/status-c.md"
            unreadable.write_text(STATUS_TEXT, encoding="utf-8")
            unreadable.chmod(0)
            self.addCleanup(unreadable.chmod, 0o644)
            self.assert_refused(self.run_check(str(self.store)), f"cannot read {unreadable}")

    def test_a_path_holding_a_line_boundary_prints_on_one_line(self):
        path = self.write_handout("plan-two\nlines.md", LACKING)
        run = self.run_check(str(self.store), path)
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertIn("plan-two lines.md lacks the goal sentence", run.stderr)
        path = self.write_handout("status-two\rlines.md", STATUS_TEXT)
        run = self.run_check(str(self.store), path)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        self.assertNotIn("\r", run.stdout)
        self.assertEqual(run.stdout.count("\n"), 2, run.stdout)

    # (e) the pinned-module form.

    def test_the_twin_is_byte_identical_under_its_bare_name_not_executable_and_pinned_once(self):
        self.assertTrue(TWIN.is_file(), f"{TWIN.relative_to(ROOT)} is missing: the generator writes it")
        self.assertEqual(TWIN.read_bytes(), CHECK.read_bytes())
        self.assertFalse((ROOT / "home/dot_local/bin/common/executable_handout-check.py").exists())
        self.assertFalse(os.access(TWIN, os.X_OK), "a module, run as `python3 -I -S <path>`, never by path")
        self.assertEqual(CHECK.read_text(encoding="utf-8").splitlines()[0], "#!/usr/bin/env -S python3 -I -S")
        pins = re.findall(r"^      handout-check\.py: ([0-9a-f]{64})$", MANIFEST.read_text(encoding="utf-8"), re.M)
        self.assertEqual(pins, [hashlib.sha256(CHECK.read_bytes()).hexdigest()], "one pin, the source's digest")

    def test_an_altered_copy_refuses_on_its_self_pin_before_anything_is_read(self):
        with open(self.lever, "a", encoding="utf-8") as handle:
            handle.write("# altered\n")
        (self.store / "handoff/08-purpose-and-goal.md").unlink()  # unread: the pin refusal comes first
        run = self.run_check(str(self.store))
        self.assert_refused(run, "sha256 ", "differs from the pin in", "home/dot_agents/agent-config.yaml")

    def test_the_installed_copy_reads_the_deployed_manifest_and_a_missing_or_doubled_pin_refuses(self):
        installed = self.home / ".local/bin/common"
        installed.mkdir(parents=True)
        (self.home / ".agents").mkdir()
        manifest = self.home / ".agents/agent-config.yaml"
        shutil.copy2(MANIFEST, manifest)
        shutil.copy2(CHECK, installed / CHECK.name)
        (installed / CHECK.name).chmod(0o644)
        plan = self.write_handout("plan-current.md", PLAN)
        self.assert_ok(self.run_check(str(self.store), lever=installed / CHECK.name), plan)
        text = manifest.read_text(encoding="utf-8")
        pin_line = next(line for line in text.splitlines() if line.startswith("      handout-check.py: "))
        manifest.write_text(text.replace(pin_line, "      handout-check.py: " + "0" * 64), encoding="utf-8")
        self.assert_refused(self.run_check(str(self.store), lever=installed / CHECK.name), str(manifest))
        manifest.write_text(text.replace(pin_line + "\n", ""), encoding="utf-8")
        self.assert_refused(
            self.run_check(str(self.store), lever=installed / CHECK.name), "no single sha256 pin for handout-check.py"
        )
        manifest.write_text(text.replace(pin_line + "\n", pin_line + "\n" + pin_line + "\n"), encoding="utf-8")
        self.assert_refused(
            self.run_check(str(self.store), lever=installed / CHECK.name), "no single sha256 pin for handout-check.py"
        )
        manifest.unlink()
        self.assert_refused(self.run_check(str(self.store), lever=installed / CHECK.name), "manifest unreadable")


if __name__ == "__main__":
    unittest.main()
