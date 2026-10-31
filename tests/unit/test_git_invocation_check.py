"""Exercise scripts/ci/git-invocation-check.sh, the lint that refuses a `git` word outside `git_isolated` (regime-cutover
U113, plan P-22), and enforce it: the library and the five adopted levers must be clean, with the two allowed lines.

The fixtures under tests/fixtures/git-invocation are parsed as bash by the lint; they carry no shebang and no `.sh`
suffix, so the formatting gate (scripts/ci/run-on-lint-files.sh) never reads them, the unparsable one included. The
contract run before every walk (U105) is exercised with the other walkers in tests/unit/test_shfmt_json_contract.py.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts/ci/git-invocation-check.sh"
FIXTURES = ROOT / "tests/fixtures/git-invocation"
LIBRARY = ROOT / "scripts/orchestrator/git-isolated.sh"
# The five levers the brief adopts, and pr-thread-resolve.sh, whose `disposition` is one text with
# pr-threads-check.sh's (U28b F1) and so runs the same isolated git.
LEVERS = tuple(
    ROOT / "scripts/orchestrator" / name
    for name in (
        "records-sync.sh",
        "pr-audit.sh",
        "pr-merge.sh",
        "pr-threads-check.sh",
        "pr-body-edit.sh",
        "pr-thread-resolve.sh",
    )
)
CALL = "a git call outside git_isolated; run it through the library, or carry `# git-isolated: allow <reason>`"
REASONLESS = "an allow comment without a reason; `# git-isolated: allow <reason>` names why this git is not isolated"
# fixture -> the findings (line, message) the lint prints, in that order; an empty list is a clean file
FINDINGS = {
    "bare-git": [(1, CALL)],
    "command-git": [(1, CALL)],
    "exec-git": [(1, CALL)],
    "absolute-git": [(1, CALL)],
    "bounded-git": [(1, CALL)],
    "array-git": [(1, CALL)],
    "assignment-and-redirect": [(1, CALL), (2, CALL)],
    "heredocs": [(5, CALL)],  # the quoted body is text; the `$(git …)` of the unquoted body runs
    "shadowed-function": [(2, CALL)],  # a `git_isolated` of its own, outside the library, hides nothing
    "allow-without-reason": [(1, CALL), (1, REASONLESS)],
    "quoted-git": [],
    "allow-with-reason": [],
    "allow-on-a-continued-statement": [],
}
# The allow lines the five levers may carry, by lever: the reason each line must spell (brief U113, CHANGE 2).
ALLOWED = {
    "records-sync.sh": ["the identity is read from the user configuration on purpose"] * 2,
    "pr-audit.sh": ["bounded exec of the library's own arrays"],
    "pr-merge.sh": [],
    "pr-threads-check.sh": [],
    "pr-body-edit.sh": [],
    "pr-thread-resolve.sh": [],
}


def check(*files, env=None):
    return subprocess.run(
        ["bash", str(CHECK), *(str(file) for file in files)], capture_output=True, text=True, check=False, env=env
    )


@unittest.skipUnless(shutil.which("shfmt"), "needs shfmt (CI puts the pinned version on PATH)")
class GitInvocationCheckTest(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="git-invocation-check-"))
        self.addCleanup(shutil.rmtree, self.temp)

    def test_the_library_and_the_adopted_levers_are_clean(self):
        result = check(LIBRARY, *LEVERS)
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def test_the_only_allow_lines_are_the_identity_reads_and_the_bounded_fetch(self):
        marker = "# git-isolated: allow "

        def allow_lines(path):  # the reasons on statement lines; a comment line that quotes the marker is prose
            lines = [line for line in path.read_text().splitlines() if not line.lstrip().startswith("#")]
            return [line.split(marker, 1)[1] for line in lines if marker in line]

        self.assertEqual(ALLOWED, {lever.name: allow_lines(lever) for lever in LEVERS})
        self.assertEqual([], allow_lines(LIBRARY), "the library needs no allow line: its function is the exemption")

    def test_each_fixture_yields_its_findings(self):
        for name, wants in FINDINGS.items():
            with self.subTest(fixture=name):
                result = check(FIXTURES / name)
                expected = "".join(f"{FIXTURES / name}:{line}: {message}\n" for line, message in wants)
                self.assertEqual((int(bool(wants)), expected, ""), (result.returncode, result.stdout, result.stderr))

    def test_every_fixture_is_in_the_table(self):
        self.assertEqual(set(FINDINGS) | {"unparsable"}, {path.name for path in FIXTURES.iterdir()})

    def test_the_library_s_function_is_the_exemption_only_in_the_library_itself(self):
        """The same bytes elsewhere are not the library: the exemption rests on the file's identity, so a copy that
        carries a `git_isolated` of its own is reported at its `exec git` line."""
        copy = self.temp / "git-isolated.sh"
        shutil.copy(LIBRARY, copy)
        lines = LIBRARY.read_text().splitlines()
        (at,) = [n for n, line in enumerate(lines, 1) if "exec git " in line]
        result = check(copy)
        self.assertEqual((1, f"{copy}:{at}: {CALL}\n", ""), (result.returncode, result.stdout, result.stderr))

    def test_the_list_is_refused_not_read_as_clean(self):
        """No file, a file shfmt cannot parse (whatever its position), an unreadable file and a missing shfmt each exit
        2 with no finding on stdout: a list the lint could not judge is never clean."""
        result = check()
        self.assertEqual(2, result.returncode)
        self.assertIn("no file to check; an empty list is refused", result.stderr)
        for files in (
            (FIXTURES / "quoted-git", FIXTURES / "unparsable"),
            (FIXTURES / "unparsable", FIXTURES / "bare-git"),
        ):
            with self.subTest(files=[file.name for file in files]):
                result = check(*files)
                self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
                self.assertIn(f"shfmt cannot parse {FIXTURES / 'unparsable'}; the list is refused", result.stderr)
        if os.geteuid() != 0:
            unreadable = self.temp / "unreadable"
            unreadable.write_text("git status\n")
            unreadable.chmod(0)
            result = check(FIXTURES / "bare-git", unreadable)
            self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
            self.assertIn(f"cannot read {unreadable}; the list is refused", result.stderr)
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        for tool in ("bash", "python3"):
            (bin_dir / tool).symlink_to(shutil.which(tool))
        result = check(FIXTURES / "bare-git", env={"PATH": str(bin_dir), "HOME": str(self.temp)})
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertIn("shfmt not found; the list is refused", result.stderr)


if __name__ == "__main__":
    unittest.main()
