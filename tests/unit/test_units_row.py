"""Exercise scripts/orchestrator/units-row.py (regime-cutover U505), the coordinator's one writer of a `units.tsv` row:
`add` byte for byte with its line number, `set` of each cell kind and `--note-append` on an empty and a non-empty note
with every other row untouched, the two `unchanged` cases, each refusal by name with the register unchanged, the
failed-write paths through an injected short `pwrite` and an injected `fsync` failure on `add` and on `set`, the self
pin refusal of an altered copy, and the argv strict-UTF-8 rule."""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/units-row.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"

UNITS_HEADER = "id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote\n"
A = "a" * 40
B = "b" * 40
C = "c" * 40
D = "d" * 40


def unit_row(unit, track, state, branch, pr, head, brief, note):
    return "\t".join((unit, track, state, branch, pr, head, brief, note)) + "\n"


# Five rows, ids up to U12, one fix unit U12b; U7 has an empty note (the `--note-append` on an empty note case).
ROWS = (
    unit_row("U1", "connections", "done", "", "", "", "briefs/U1-pilot-bridge.md", "measured 31 runs; report written"),
    unit_row("U7", "seats", "landed", "feat/hcom-seat", "470", A, "briefs/U7-hcom-seat.md", ""),
    unit_row("U11", "cutover", "in-flight", "feat/cutover", "478", B, "briefs/U11-cutover.md", "round 1 dispatched"),
    unit_row("U12", "levers", "queued", "", "", "", "briefs/U12-ledger-row.md", "waits on U11"),
    unit_row("U12b", "levers", "in-flight", "feat/ledger-row-fix", "480", C, "briefs/U12b-ledger-row-fix.md", "fix 2"),
)
UNITS = UNITS_HEADER + "".join(ROWS)
NEW = unit_row("U13", "levers", "queued", "feat/units-row-lever", "481", D, "briefs/U13-units-row.md", "the new row")
NEW_ARGS = (
    "add",
    "--id",
    "U13",
    "--track",
    "levers",
    "--state",
    "queued",
    "--branch",
    "feat/units-row-lever",
    "--pr",
    "481",
    "--head",
    D,
    "--brief",
    "briefs/U13-units-row.md",
    "--note",
    "the new row",
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def line_digests(text):
    """The sha256 of every line of the register, keyed by its number (the header is line 1)."""
    return {number: sha256(line.encode()) for number, line in enumerate(text.split("\n"), 1)}


class UnitsRowTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.store = root / "regime-cutover"
        (self.store / "briefs").mkdir(parents=True)
        self.units = self.store / "units.tsv"
        self.units.write_text(UNITS)
        self.home = root / "home"
        self.home.mkdir()
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}
        self.lever = LEVER

    def copy_lever(self):
        """A checkout-shaped copy of the lever two levels below a copy of the manifest, so the self check passes on
        the copy."""
        checkout = Path(self.temp.name).resolve() / "checkout"
        levers = checkout / "scripts/orchestrator"
        levers.mkdir(parents=True)
        (checkout / "home/dot_agents").mkdir(parents=True)
        shutil.copy2(MANIFEST, checkout / "home/dot_agents/agent-config.yaml")
        shutil.copy2(LEVER, levers / LEVER.name)
        self.lever = levers / LEVER.name
        return levers

    def run_raw(self, *argv):
        """The lever under `python3 -I` with exactly `argv` after it (an element may be bytes)."""
        return subprocess.run(
            [sys.executable, "-I", str(self.lever), *argv],
            capture_output=True,
            env=self.env,
            timeout=60,
            check=False,
        )

    def run_lever(self, *argv, store=None):
        run = self.run_raw(str(store or self.store), *argv)
        run.stdout = run.stdout.decode("utf-8", "replace")
        run.stderr = run.stderr.decode("utf-8", "replace")
        return run

    def store_listing(self):
        return sorted((str(path.relative_to(self.store)), path.stat().st_mode) for path in self.store.rglob("*"))

    def assert_written(self, expected_line, *argv, text=None):
        """Exit 0, nothing on stderr, the one stdout line, the register equal to `text` and no other store entry."""
        before = self.store_listing()
        run = self.run_lever(*argv)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        self.assertEqual(run.stdout, expected_line + "\n")
        if text is not None:
            self.assertEqual(self.units.read_text(encoding="utf-8"), text)
        self.assertEqual(self.store_listing(), before, "no new entry and no mode change under the store")
        return run

    def assert_refused(self, *reasons, argv=None, store=None):
        """Exit 2, one stderr line naming each reason, nothing on stdout, the register and the store unchanged."""
        before = self.store_listing()
        units = self.units.read_bytes() if self.units.is_file() else None
        run = self.run_raw(*([str(store or self.store), *argv] if argv is not None else []))
        stderr = run.stderr.decode("utf-8", "replace")
        self.assertEqual((run.returncode, run.stdout), (2, b""), stderr)
        self.assertEqual(stderr.count("\n"), 1, stderr)
        self.assertTrue(stderr.startswith("units-row.py: refused: "), stderr)
        self.assertNotIn("Traceback", stderr)
        for reason in reasons:
            self.assertIn(reason, stderr)
        self.assertEqual(self.store_listing(), before, "nothing written")
        if units is not None:
            self.assertEqual(self.units.read_bytes(), units, "units.tsv unchanged")
        return stderr

    def assert_other_rows_untouched(self, changed_line):
        """Every line of the register but `changed_line` has the sha256 it had in the fixture."""
        before = line_digests(UNITS)
        after = line_digests(self.units.read_text(encoding="utf-8"))
        for number, digest in before.items():
            if number != changed_line:
                self.assertEqual(after[number], digest, f"line {number} changed")

    # (a) add: the row byte for byte and its line number.

    def test_add_appends_the_row_byte_for_byte_and_prints_its_line(self):
        self.assert_written("added U13 line 7", *NEW_ARGS, text=UNITS + NEW)
        self.assert_other_rows_untouched(7)

    def test_add_with_the_optional_cells_left_out_writes_them_empty(self):
        self.assert_written(
            "added U13 line 7",
            "add",
            "--id",
            "U13",
            "--track",
            "levers",
            "--state",
            "queued",
            "--note",
            "no branch yet",
            text=UNITS + unit_row("U13", "levers", "queued", "", "", "", "", "no branch yet"),
        )

    def test_add_to_a_register_without_a_final_newline_gives_the_last_row_one_first(self):
        self.units.write_text(UNITS.rstrip("\n"))
        self.assert_written("added U13 line 7", *NEW_ARGS, text=UNITS + NEW)

    def test_add_of_a_fix_unit_id_and_a_brief_of_that_id(self):
        line = unit_row("U12c", "levers", "queued", "", "", "", "briefs/U12c-ledger-row-fix-3.md", "fix 3")
        self.assert_written(
            "added U12c line 7",
            "add",
            "--id",
            "U12c",
            "--track",
            "levers",
            "--state",
            "queued",
            "--brief",
            "briefs/U12c-ledger-row-fix-3.md",
            "--note",
            "fix 3",
            text=UNITS + line,
        )

    # (b) set: each cell kind, byte for byte, the other rows untouched.

    def test_set_of_each_cell_kind_replaces_that_cell_alone_and_names_it(self):
        cases = (
            ("--track", "cutover-2", 1),
            ("--state", "landed", 2),
            ("--branch", "feat/cutover-2", 3),
            ("--pr", "479", 4),
            ("--head", D, 5),
            ("--brief", "briefs/U11-cutover-2.md", 6),
        )
        for option, value, index in cases:
            with self.subTest(option=option):
                self.units.write_text(UNITS)
                cells = ROWS[2].rstrip("\n").split("\t")
                cells[index] = value
                name = UNITS_HEADER.rstrip("\n").split("\t")[index]
                expected = UNITS.replace(ROWS[2], "\t".join(cells) + "\n")
                self.assert_written(f"set U11 line 4 cells={name}", "set", "--id", "U11", option, value, text=expected)
                self.assert_other_rows_untouched(4)

    def test_set_of_several_cells_names_them_in_the_header_s_order(self):
        cells = ROWS[2].rstrip("\n").split("\t")
        cells[2], cells[4], cells[5] = "landed", "479", D
        expected = UNITS.replace(ROWS[2], "\t".join(cells) + "\n")
        self.assert_written(
            "set U11 line 4 cells=state,pr,head_sha",
            "set",
            "--id",
            "U11",
            "--head",
            D,
            "--pr",
            "479",
            "--state",
            "landed",
            text=expected,
        )

    def test_set_may_empty_a_branch_a_pr_a_head_or_a_brief(self):
        cells = ROWS[2].rstrip("\n").split("\t")
        cells[3] = cells[4] = cells[5] = cells[6] = ""
        expected = UNITS.replace(ROWS[2], "\t".join(cells) + "\n")
        self.assert_written(
            "set U11 line 4 cells=branch,pr,head_sha,brief",
            "set",
            "--id",
            "U11",
            "--branch",
            "",
            "--pr",
            "",
            "--head",
            "",
            "--brief",
            "",
            text=expected,
        )

    def test_set_on_the_last_row_and_on_a_register_without_a_final_newline(self):
        self.units.write_text(UNITS.rstrip("\n"))
        cells = ROWS[4].rstrip("\n").split("\t")
        cells[2] = "landed"
        expected = UNITS.replace(ROWS[4], "\t".join(cells) + "\n")
        self.assert_written("set U12b line 6 cells=state", "set", "--id", "U12b", "--state", "landed", text=expected)

    def test_a_shorter_rewrite_truncates_the_register_to_the_new_length(self):
        # A `set` has no `--note`, so the shortening is measured on the brief cell emptied.
        cells = ROWS[0].rstrip("\n").split("\t")
        cells[6] = ""
        expected = UNITS.replace(ROWS[0], "\t".join(cells) + "\n")
        self.assert_written("set U1 line 2 cells=brief", "set", "--id", "U1", "--brief", "", text=expected)
        self.assertEqual(self.units.stat().st_size, len(expected.encode()))

    def test_note_append_on_an_empty_note_sets_it_and_on_a_non_empty_note_appends_after_a_semicolon(self):
        cells = ROWS[1].rstrip("\n").split("\t")
        cells[7] = "seat pilot ran"
        expected = UNITS.replace(ROWS[1], "\t".join(cells) + "\n")
        self.assert_written(
            "set U7 line 3 cells=note", "set", "--id", "U7", "--note-append", "seat pilot ran", text=expected
        )
        cells = ROWS[2].rstrip("\n").split("\t")
        cells[7] = "round 1 dispatched; round 2 dispatched"
        expected = expected.replace(ROWS[2], "\t".join(cells) + "\n")
        self.assert_written(
            "set U11 line 4 cells=note", "set", "--id", "U11", "--note-append", "round 2 dispatched", text=expected
        )
        after = line_digests(expected)
        self.assertEqual(line_digests(self.units.read_text(encoding="utf-8")), after)

    def test_note_append_together_with_a_cell_names_both_in_the_header_s_order(self):
        cells = ROWS[2].rstrip("\n").split("\t")
        cells[2] = "landed"
        cells[7] = "round 1 dispatched; merged"
        expected = UNITS.replace(ROWS[2], "\t".join(cells) + "\n")
        self.assert_written(
            "set U11 line 4 cells=state,note",
            "set",
            "--id",
            "U11",
            "--note-append",
            "merged",
            "--state",
            "landed",
            text=expected,
        )

    # (c) the two unchanged cases.

    def test_a_set_whose_every_named_value_equals_the_cell_prints_unchanged_and_writes_nothing(self):
        mtime = self.units.stat().st_mtime_ns
        self.assert_written(
            "unchanged U11", "set", "--id", "U11", "--state", "in-flight", "--pr", "478", "--head", B, text=UNITS
        )
        self.assertEqual(self.units.stat().st_mtime_ns, mtime, "the register was not opened for a write of its text")
        # `--note-append` of a text the note already ends with is the same no-op (the second run of one command).
        self.assert_written("unchanged U11", "set", "--id", "U11", "--note-append", "round 1 dispatched", text=UNITS)
        self.assert_written("set U11 line 4 cells=note", "set", "--id", "U11", "--note-append", "pushed")
        self.assert_written("unchanged U11", "set", "--id", "U11", "--note-append", "pushed")

    def test_an_add_of_a_row_byte_equal_to_an_existing_row_prints_unchanged_and_writes_nothing(self):
        self.assert_written(
            "unchanged U12b",
            "add",
            "--id",
            "U12b",
            "--track",
            "levers",
            "--state",
            "in-flight",
            "--branch",
            "feat/ledger-row-fix",
            "--pr",
            "480",
            "--head",
            C,
            "--brief",
            "briefs/U12b-ledger-row-fix.md",
            "--note",
            "fix 2",
            text=UNITS,
        )
        self.assert_written("added U13 line 7", *NEW_ARGS, text=UNITS + NEW)
        self.assert_written("unchanged U13", *NEW_ARGS, text=UNITS + NEW)

    # (d) every refusal by name, the register unchanged byte for byte.

    def test_a_duplicate_id_on_add_refuses_naming_the_line(self):
        argv = list(NEW_ARGS)
        argv[argv.index("--brief") + 1] = ""
        argv[2] = "U12"
        self.assert_refused("U12", "exists", "line 5", argv=argv)
        argv[2] = "U12b"
        self.assert_refused("U12b", "exists", "line 6", argv=argv)
        # Two rows with the id: both lines are named.
        self.units.write_text(UNITS + ROWS[3])
        argv[2] = "U12"
        self.assert_refused("U12", "exists", "lines 5, 7", argv=argv)

    def test_a_missing_or_doubled_id_on_set_refuses_naming_the_count(self):
        self.assert_refused("0 rows", "U99", argv=["set", "--id", "U99", "--state", "done"])
        self.units.write_text(UNITS + ROWS[3])
        self.assert_refused("2 rows", "U12", "lines 5, 7", argv=["set", "--id", "U12", "--state", "done"])

    def test_no_option_after_the_id_on_set_refuses_as_nothing_to_set(self):
        self.assert_refused("nothing to set", argv=["set", "--id", "U11"])

    def test_each_cell_outside_its_class_refuses_naming_the_cell(self):
        cases = (
            ("--id", "u13", "id"),
            ("--id", "U", "id"),
            ("--id", "U13-", "id"),
            ("--id", "U13B", "id"),
            ("--id", "13", "id"),
            ("--track", "Levers", "track"),
            ("--track", "a lever", "track"),
            ("--track", "", "track"),
            ("--state", "Done!", "state"),
            ("--state", "in_flight", "state"),
            ("--branch", "feat/a b", "branch"),
            ("--branch", "feat/ä", "branch"),
            ("--branch", "feat/a;b", "branch"),
            ("--pr", "0", "pr"),
            ("--pr", "0481", "pr"),
            ("--pr", "1234567890", "pr"),
            ("--pr", "x", "pr"),
            ("--head", D[:39], "head_sha"),
            ("--head", D.upper(), "head_sha"),
            ("--head", D + "d", "head_sha"),
            ("--brief", "briefs/U13.md", "brief"),
            ("--brief", "handouts/U13-x.md", "brief"),
            ("--brief", "briefs/U13-x.txt", "brief"),
            ("--brief", "briefs/U13-x y.md", "brief"),
            ("--brief", "briefs/../U13-x.md", "brief"),
        )
        for option, value, cell in cases:
            with self.subTest(option=option, value=value):
                argv = list(NEW_ARGS)
                argv[argv.index(option) + 1] = value
                self.assert_refused(f"the {cell}", repr(value), argv=argv)

    def test_a_brief_path_whose_id_is_another_row_s_refuses_on_add_and_on_set(self):
        argv = list(NEW_ARGS)
        argv[argv.index("--brief") + 1] = "briefs/U12-units-row.md"
        self.assert_refused("the brief", "briefs/U12-units-row.md", "U13", argv=argv)
        self.assert_refused(
            "the brief",
            "briefs/U12b-cutover.md",
            "U11",
            argv=["set", "--id", "U11", "--brief", "briefs/U12b-cutover.md"],
        )

    def test_a_tab_a_carriage_return_and_a_line_separator_in_a_note_refuse(self):
        for value, label in (("a\tb", "a tab"), ("a\rb", "a carriage return"), ("a\nb", "a newline")):
            with self.subTest(label=label):
                argv = list(NEW_ARGS)
                argv[-1] = value
                self.assert_refused("--note", label, argv=argv)
                self.assert_refused("--note-append", label, argv=["set", "--id", "U11", "--note-append", value])
        for value in ("a\u2028b", "a\u2029b", "a\x85b", "a\x0bb", "a\x0cb", "a\x1cb"):
            with self.subTest(value=value):
                argv = list(NEW_ARGS)
                argv[-1] = value
                stderr = self.assert_refused("the note", "line boundary", argv=argv)
                self.assertEqual(len(stderr.splitlines()), 1, "the refusal line folds the boundary")
                self.assert_refused("the note", "line boundary", argv=["set", "--id", "U11", "--note-append", value])
        # A cell of another kind holding one refuses by its class.
        argv = list(NEW_ARGS)
        argv[argv.index("--branch") + 1] = "feat/a\u2028b"
        self.assert_refused("the branch", argv=argv)

    def test_a_register_with_another_header_a_seven_cell_row_or_a_carriage_return_refuses_naming_the_line(self):
        self.units.write_text(UNITS.replace("\tpr\t", "\tpull\t", 1))
        self.assert_refused(f"{self.units}:1", "header", argv=list(NEW_ARGS))
        self.units.write_text(UNITS + "U13\tfix\tlanded\tx\t1\t" + A + "\tbriefs/U13-x.md\n")
        self.assert_refused(f"{self.units}:7", "7 cells", argv=list(NEW_ARGS))
        self.units.write_text(UNITS + "U13\tfix\tlanded\tx\t1\t" + A + "\tbriefs/U13-x.md\tn\textra\n")
        self.assert_refused(f"{self.units}:7", "9 cells", argv=["set", "--id", "U11", "--state", "done"])
        self.units.write_bytes(UNITS.replace("\n", "\r\n").encode())
        self.assert_refused(f"{self.units}:1", "carriage return", argv=list(NEW_ARGS))
        self.units.write_bytes(UNITS.encode() + b"U13\tfix\tlanded\tx\t1\t\xff\tbriefs/U13-x.md\tn\n")
        self.assert_refused(str(self.units), "not UTF-8", argv=list(NEW_ARGS))
        self.units.write_text("")
        self.assert_refused(f"{self.units}:1", "empty", argv=list(NEW_ARGS))
        self.units.unlink()
        self.assert_refused(str(self.units), "regular file", argv=list(NEW_ARGS))

    def test_a_symlinked_register_a_store_that_is_no_directory_and_a_register_of_another_owner_refuse(self):
        real = Path(self.temp.name).resolve() / "real-units.tsv"
        real.write_text(UNITS)
        self.units.unlink()
        self.units.symlink_to(real)
        self.assert_refused(str(self.units), "symbolic link", argv=list(NEW_ARGS))
        self.assertEqual(real.read_text(), UNITS)
        self.units.unlink()
        self.units.write_text(UNITS)
        self.assert_refused("not a directory", argv=list(NEW_ARGS), store=self.units)
        self.assert_refused("cannot be read", argv=list(NEW_ARGS), store=self.store / "missing")
        if os.geteuid() != 0 and Path("/").stat().st_uid != os.getuid():
            self.assert_refused("not a directory of this user", argv=list(NEW_ARGS), store=Path("/"))
        self.units.unlink()
        self.units.mkdir()
        self.assert_refused(str(self.units), "regular file", argv=list(NEW_ARGS))

    def hold_register_lock(self):
        """A subprocess holding `LOCK_EX` on `units.tsv` itself for the test's duration; returns once it holds."""
        holder = subprocess.Popen(
            [
                sys.executable,
                "-I",
                "-c",
                "import fcntl, os, sys, time\n"
                "fd = os.open(sys.argv[1], os.O_RDWR)\n"
                "fcntl.flock(fd, fcntl.LOCK_EX)\n"
                "print('held', flush=True)\n"
                "time.sleep(120)\n",
                str(self.units),
            ],
            stdout=subprocess.PIPE,
            text=True,
        )

        def stop():
            holder.kill()
            holder.wait()
            holder.stdout.close()

        self.addCleanup(stop)
        self.assertEqual(holder.stdout.readline(), "held\n")
        return holder

    def test_a_held_lock_past_lock_wait_refuses_naming_the_register(self):
        self.hold_register_lock()
        start = time.monotonic()
        stderr = self.assert_refused(str(self.units), "held by another writer", argv=[*NEW_ARGS, "--lock-wait", "1"])
        self.assertGreaterEqual(time.monotonic() - start, 1.0)
        self.assertIn("--lock-wait", stderr)
        self.assert_refused(
            str(self.units),
            "held by another writer",
            argv=["set", "--id", "U11", "--state", "done", "--lock-wait", "0"],
        )
        for value in ("-1", "inf", "nan", "x"):
            with self.subTest(value=value):
                self.assert_refused("--lock-wait", argv=[*NEW_ARGS, "--lock-wait", value])

    def test_an_argument_outside_strict_utf_8_or_holding_a_control_refuses_by_the_argument_rule(self):
        for value, label in (("1\t", "a tab"), ("1\n", "a newline"), ("1\r", "a carriage return")):
            with self.subTest(label=label):
                stderr = self.assert_refused("--lock-wait", label, argv=[*NEW_ARGS, "--lock-wait", value])
                self.assertNotIn("usage:", stderr)
        argv = list(NEW_ARGS)
        argv[-1] = b"the \xff row"
        stderr = self.assert_refused("not UTF-8", "--note", argv=argv)
        self.assertNotIn("Traceback", stderr)
        self.assert_refused("the store", "a newline", argv=list(NEW_ARGS), store=Path(str(self.store) + "\nx"))

    def test_an_unknown_subcommand_or_option_refuses_in_one_line_without_a_usage_block(self):
        stderr = self.assert_refused(argv=["drop", "--id", "U11"])
        self.assertNotIn("usage:", stderr)
        stderr = self.assert_refused(argv=["set", "--id", "U11", "--note", "x"])
        self.assertNotIn("usage:", stderr)
        self.assert_refused(argv=["add", "--id", "U13", "--track", "levers", "--state", "queued"])
        self.assert_refused(argv=["add", "--id", "U13", "--track", "levers", "--note", "n"])
        self.assert_refused(argv=[])

    # (e) the failed-write paths through the injected writer: the register byte-identical to before.

    def inject(self, function, body, *argv):
        """The lever run through `runpy` under `python3 -I` with `os.<function>` replaced by `body`, a function over
        `real` (the original) and `calls` (a one-element list counting the calls)."""
        injection = (
            "import errno, os, runpy, sys\n"
            f"real = os.{function}\n"
            "calls = [0]\n"
            "def injected(*args, **kwargs):\n"
            "    calls[0] += 1\n"
            f"{body}\n"
            f"os.{function} = injected\n"
            "sys.argv = sys.argv[1:]\n"
            "runpy.run_path(sys.argv[0], run_name='__main__')\n"
        )
        return subprocess.run(
            [sys.executable, "-I", "-c", injection, str(self.lever), str(self.store), *argv],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )

    SHORT_PWRITE = (
        "    if calls[0] == 1:\n        return real(args[0], args[1][:-1], args[2])\n    return real(*args, **kwargs)"
    )
    FAILING_FSYNC = (
        "    if calls[0] == 1:\n"
        "        raise OSError(errno.EIO, os.strerror(errno.EIO))\n"
        "    return real(*args, **kwargs)"
    )

    def assert_write_failure(self, run, content, before):
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(f"units-row.py: cannot write {self.units}: "), run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        self.assertEqual(self.units.read_bytes(), content, "the register is byte-identical")
        self.assertEqual(self.store_listing(), before, "no other entry and no mode change")
        return run.stderr

    def test_a_short_pwrite_on_add_and_on_set_exits_1_naming_the_register_which_is_byte_identical(self):
        before = self.store_listing()
        content = self.units.read_bytes()
        for argv in (NEW_ARGS, ("set", "--id", "U11", "--state", "landed")):
            with self.subTest(argv[0]):
                stderr = self.assert_write_failure(self.inject("pwrite", self.SHORT_PWRITE, *argv), content, before)
                self.assertIn("short write", stderr)
                self.assertIn("restored", stderr)

    def test_a_failing_fsync_on_add_and_on_set_exits_1_naming_the_register_which_is_byte_identical(self):
        before = self.store_listing()
        content = self.units.read_bytes()
        for argv in (NEW_ARGS, ("set", "--id", "U11", "--state", "landed")):
            with self.subTest(argv[0]):
                stderr = self.assert_write_failure(self.inject("fsync", self.FAILING_FSYNC, *argv), content, before)
                self.assertIn("fsync: Input/output error", stderr)
                self.assertIn("restored", stderr)

    def test_a_failing_pwrite_on_set_of_a_longer_text_exits_1_and_the_register_is_byte_identical(self):
        before = self.store_listing()
        content = self.units.read_bytes()
        body = (
            "    if calls[0] == 1:\n"
            "        real(args[0], args[1][:5], args[2])\n"
            "        raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))\n"
            "    return real(*args, **kwargs)"
        )
        argv = ("set", "--id", "U7", "--note-append", "a long note that makes the whole text longer than before")
        stderr = self.assert_write_failure(self.inject("pwrite", body, *argv), content, before)
        self.assertIn("No space left on device", stderr)

    def test_an_injected_fstat_or_pread_failure_is_a_refusal_exit_2_and_the_register_unchanged(self):
        before = self.store_listing()
        content = self.units.read_bytes()
        for function in ("fstat", "pread"):
            with self.subTest(function):
                run = self.inject(function, self.FAILING_FSYNC, *NEW_ARGS)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertTrue(run.stderr.startswith("units-row.py: refused: "), run.stderr)
                self.assertIn(str(self.units), run.stderr)
                self.assertIn("Input/output error", run.stderr)
                self.assertEqual(self.units.read_bytes(), content)
                self.assertEqual(self.store_listing(), before)

    # (f) the self pin and the file's form.

    def test_an_altered_copy_refuses_on_its_self_pin_before_anything_is_read(self):
        self.copy_lever()
        with open(self.lever, "a", encoding="utf-8") as handle:
            handle.write("# altered\n")
        self.units.unlink()  # unread: the pin refusal comes first
        stderr = self.assert_refused("sha256 ", "differs from the pin in", argv=list(NEW_ARGS))
        self.assertIn("home/dot_agents/agent-config.yaml", stderr)

    def test_a_faithful_copy_under_a_copied_checkout_runs(self):
        self.copy_lever()
        self.assert_written("added U13 line 7", *NEW_ARGS, text=UNITS + NEW)

    def test_the_checkout_lever_is_executable_runs_python3_isolated_and_imports_no_subprocess(self):
        self.assertEqual(LEVER.stat().st_mode & 0o777, 0o755)
        text = LEVER.read_text(encoding="utf-8")
        self.assertEqual(text.splitlines()[0], "#!/usr/bin/env -S python3 -I")
        self.assertNotIn("subprocess", text, "the lever runs no gh and no git")
        self.assertNotIn("tempfile", text, "the lever makes no file but the register")
        self.assertNotIn("os.replace", text)
        self.assertNotIn("O_APPEND", text, "the in-place rewrite needs the offset honoured")
        self.assertEqual(
            sha256(LEVER.read_bytes()),
            sha256((ROOT / "home/dot_local/bin/common/executable_units-row.py").read_bytes()),
        )
        pin = re.search(r"^ {6}units-row\.py: ([0-9a-f]{64})$", MANIFEST.read_text(), re.MULTILINE)
        self.assertIsNotNone(pin, "the manifest pins units-row.py")
        self.assertEqual(pin.group(1), sha256(LEVER.read_bytes()))

    def test_a_successful_write_keeps_the_register_s_mode_and_owner(self):
        self.units.chmod(0o600)
        status = self.units.stat()
        self.assert_written("added U13 line 7", *NEW_ARGS, text=UNITS + NEW)
        after = self.units.stat()
        self.assertEqual((after.st_mode, after.st_uid, after.st_ino), (status.st_mode, status.st_uid, status.st_ino))


if __name__ == "__main__":
    unittest.main()
