"""Exercise scripts/lint-retired-terms.py (regime-cutover U72): the repository against its one list, and each row kind,
exit status and refusal on scratch git repositories.

The lint runs as a subprocess (`python3 -I`), as CI, `make retired-terms`, `make doctor` and the drift watch run it:
exit 0 clean, exit 1 with one `<file>:<line>: <text>` per hit, any other status a failure to check.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINT = ROOT / "scripts/lint-retired-terms.py"
LIST = ROOT / "scripts/retired-terms.tsv"
GIT_ENV = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
TERM = "term\toldname\tthe old tool\n"


def run_lint(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", str(LINT), *args], capture_output=True, text=True, check=False, timeout=120
    )


class RepositoryTest(unittest.TestCase):
    def test_the_repository_names_no_retired_term_outside_the_allow_list(self) -> None:
        result = run_lint()
        self.assertEqual(("", 0), (result.stdout, result.returncode), result.stdout + result.stderr)

    @unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is not installed")
    def test_apply_removes_every_listed_deployed_copy_and_keeps_a_neighbour(self) -> None:
        # The `removed` rows are the targets a host may still hold; the real .chezmoiremove must take each away.
        rows = [line.split("\t") for line in LIST.read_text().splitlines() if line.startswith("removed\t")]
        self.assertTrue(rows)
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source, home = base / "source", base / "home"
            source.mkdir()
            shutil.copy(ROOT / "home/.chezmoiremove", source / ".chezmoiremove")
            planted = []
            for _, target, _ in rows:
                path = home / (target.removesuffix("/**") + "/x" if target.endswith("/**") else target)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("retired")
                planted.append(home / target.removesuffix("/**"))
            (home / ".local/bin/common/kept").parent.mkdir(parents=True, exist_ok=True)
            (home / ".local/bin/common/kept").write_text("kept")
            (base / "chezmoi.toml").write_text("")
            run = subprocess.run(
                [
                    *("chezmoi", "apply", "--force", "--no-tty", "--source", str(source), "--destination", str(home)),
                    *("--config", str(base / "chezmoi.toml"), "--cache", str(base / "cache")),
                    *("--persistent-state", str(base / "state.boltdb")),
                ],
                env=os.environ | {"HOME": str(home)},
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stderr)
            self.assertEqual([], [str(path) for path in planted if path.is_file()])
            self.assertTrue((home / ".local/bin/common/kept").is_file())


class LintTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / "home").mkdir()
        (self.repo / "home/.chezmoiremove").write_text(".local/bin/common/gone-tool\n")
        self.git("init", "-q")

    def git(self, *args: str) -> None:
        subprocess.run(["git", "-C", str(self.repo), *args], env=os.environ | GIT_ENV, check=True, capture_output=True)

    def write(self, rel: str, text: str) -> Path:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def lint(self, rows: str) -> subprocess.CompletedProcess[str]:
        self.write("scripts/retired-terms.tsv", "# kinds: see the lint\n" + rows)
        self.git("add", "-A")
        return run_lint("--root", str(self.repo))

    def test_a_term_is_found_without_regard_to_case_and_reported_at_its_line(self) -> None:
        self.write("docs/a.md", "fine\nrun OldName here\n")
        result = self.lint(TERM)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual("docs/a.md:2: retired 'oldname': run OldName here\n", result.stdout)

    def test_an_untracked_file_is_read_and_an_ignored_or_deleted_one_is_not(self) -> None:
        self.write(".gitignore", "ignored.md\n")
        self.write("ignored.md", "oldname\n")
        gone = self.write("gone.md", "oldname\n")
        self.write("scripts/retired-terms.tsv", TERM)
        self.git("add", "-A")
        gone.unlink()
        self.write("new.md", "oldname\n")
        result = run_lint("--root", str(self.repo))
        self.assertEqual(("new.md:1: retired 'oldname': oldname\n", 1), (result.stdout, result.returncode))

    def test_an_allow_row_accepts_exactly_its_file_and_term(self) -> None:
        self.write("docs/a.md", "oldname\n")
        self.write("docs/b.md", "oldname\n")
        result = self.lint(TERM + "allow\tdocs/a.md\toldname\thistory\n")
        self.assertEqual(("docs/b.md:1: retired 'oldname': oldname\n", 1), (result.stdout, result.returncode))
        # A path spelled another way is another file: the pair is compared exactly, never normalised.
        result = self.lint(TERM + "allow\t./docs/a.md\toldname\thistory\nallow\tdocs/b.md\toldname\thistory\n")
        self.assertIn("docs/a.md:1: retired 'oldname'", result.stdout)
        self.assertEqual(1, result.returncode)

    def test_an_allow_row_that_matches_nothing_is_a_hit_at_its_list_line(self) -> None:
        self.write("docs/a.md", "clean\n")
        result = self.lint(TERM + "allow\tdocs/a.md\toldname\thistory\n")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual(
            "scripts/retired-terms.tsv:3: allow row docs/a.md 'oldname' matches nothing; remove the row\n",
            result.stdout,
        )

    def test_a_skip_directory_is_not_read(self) -> None:
        self.write("records/r.md", "oldname\n")
        self.write("recordsx/r.md", "oldname\n")
        result = self.lint(TERM + "skip\trecords/\tthe records\n")
        self.assertEqual(("recordsx/r.md:1: retired 'oldname': oldname\n", 1), (result.stdout, result.returncode))

    def test_a_gone_path_that_exists_and_a_removal_missing_from_chezmoiremove_are_hits(self) -> None:
        self.write("scripts/old.sh", "true\n")
        rows = "gone\tscripts/old.sh\tdeleted\nremoved\t.local/bin/common/gone-tool\tdeployed\n"
        rows += "removed\t.local/bin/common/other\tdeployed\n"
        result = self.lint(rows)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual(
            "scripts/retired-terms.tsv:2: retired path scripts/old.sh exists again\n"
            "scripts/retired-terms.tsv:4: home/.chezmoiremove has no line .local/bin/common/other, so hosts keep the "
            "retired copy\n",
            result.stdout,
        )

    def test_a_clean_tree_exits_0_with_no_output(self) -> None:
        self.write("docs/a.md", "clean\n")
        result = self.lint(TERM + "removed\t.local/bin/common/gone-tool\tdeployed\n")
        self.assertEqual(("", "", 0), (result.stdout, result.stderr, result.returncode))

    def test_a_malformed_list_refuses_with_exit_2(self) -> None:
        self.write("docs/a.md", "oldname\n")
        cases = {
            "unknown kind": "word\toldname\twhy\n",
            "missing field": "term\toldname\n",
            "empty field": "term\t\twhy\n",
            "allow of no term": TERM + "allow\tdocs/a.md\tother\twhy\n",
            "duplicate term": TERM + "term\tOLDNAME\tagain\n",
            "skip without slash": TERM + "skip\trecords\twhy\n",
        }
        for name, rows in cases.items():
            with self.subTest(case=name):
                result = self.lint(rows)
                self.assertEqual(("", 2), (result.stdout, result.returncode), result.stderr)
                self.assertIn("lint-retired-terms:", result.stderr)

    def test_a_git_failure_or_an_unreadable_file_refuses_with_exit_2(self) -> None:
        self.write("scripts/retired-terms.tsv", TERM)
        not_git = Path(self.temp.name) / "not-git"
        (not_git / "home").mkdir(parents=True)
        (not_git / "home/.chezmoiremove").write_text("")
        result = run_lint("--root", str(not_git), "--list", str(self.repo / "scripts/retired-terms.tsv"))
        self.assertEqual(("", 2), (result.stdout, result.returncode))
        self.assertIn("git ls-files", result.stderr)
        if os.geteuid() == 0:
            return
        locked = self.write("docs/locked.md", "oldname\n")
        self.git("add", "-A")
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o644)
        result = run_lint("--root", str(self.repo))
        self.assertEqual(("", 2), (result.stdout, result.returncode))
        self.assertIn("cannot read docs/locked.md", result.stderr)

    @unittest.skipIf(os.geteuid() == 0, "root reads through directory permissions")
    def test_a_tracked_file_git_cannot_lstat_refuses_with_exit_2_never_reads_as_deleted(self) -> None:
        # Audit 033c461f P2: `git ls-files --deleted` also lists a path whose lstat failed for another reason (here a
        # directory without search permission), and the lint skipped it as deleted, so a hit in it read as clean.
        self.write("docs/locked/a.md", "oldname\n")
        self.write("scripts/retired-terms.tsv", TERM)
        self.git("add", "-A")
        locked = self.repo / "docs/locked"
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o755)
        result = run_lint("--root", str(self.repo))
        self.assertEqual(("", 2), (result.stdout, result.returncode), result.stderr)
        # git itself warns (`cannot lstat ...`) and the lint refuses on that; either way the path is named.
        self.assertIn("docs/locked/a.md", result.stderr)

    @unittest.skipIf(os.geteuid() == 0, "root reads through directory permissions")
    def test_an_untracked_directory_git_cannot_open_refuses_with_exit_2(self) -> None:
        # Audit b98984d7 P2: git exits 0 with `could not open directory ... Permission denied` and lists nothing from
        # that directory, so the lint read the partial scan as clean.
        self.write("docs/a.md", "clean\n")
        self.write("scripts/retired-terms.tsv", TERM)
        self.git("add", "-A")
        self.write("drafts/b.md", "oldname\n")
        drafts = self.repo / "drafts"
        drafts.chmod(0)
        self.addCleanup(drafts.chmod, 0o755)
        result = run_lint("--root", str(self.repo))
        self.assertEqual(("", 2), (result.stdout, result.returncode), result.stderr)
        self.assertIn("could not open directory 'drafts/'", result.stderr)

    def test_a_gone_path_that_cannot_be_checked_refuses_with_exit_2(self) -> None:
        # Audit 033c461f P2: exists() and is_symlink() read a symlink loop on the way to a `gone` path as absent.
        (self.repo / "loop").symlink_to("loop")
        self.write(".gitignore", "loop\n")
        result = self.lint("gone\tloop/old.sh\tdeleted\n")
        self.assertEqual(("", 2), (result.stdout, result.returncode), result.stderr)
        self.assertIn("cannot check loop/old.sh", result.stderr)
        # A path that is a dangling symlink itself is present: lstat reads the link.
        (self.repo / "dangling").symlink_to("nowhere")
        self.write(".gitignore", "loop\ndangling\n")
        result = self.lint("gone\tdangling\tdeleted\n")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("retired path dangling exists again", result.stdout)

    def test_an_absent_list_or_chezmoiremove_refuses_with_exit_2(self) -> None:
        result = run_lint("--root", str(self.repo))
        self.assertEqual(("", 2), (result.stdout, result.returncode))
        self.assertIn("cannot read the list", result.stderr)
        (self.repo / "home/.chezmoiremove").unlink()
        result = self.lint(TERM)
        self.assertEqual(("", 2), (result.stdout, result.returncode))
        self.assertIn("cannot read home/.chezmoiremove", result.stderr)

    def test_a_cyclic_list_or_root_symlink_refuses_with_exit_2(self) -> None:
        # Audit de9fff57 P2: resolving --list ran outside the handler, so a symlink loop exited 1 (read as hits).
        self.write("docs/a.md", "clean\n")
        self.write("scripts/retired-terms.tsv", TERM)
        self.git("add", "-A")
        loop = Path(self.temp.name) / "loop"
        loop.symlink_to(Path(self.temp.name) / "loop-back")
        (Path(self.temp.name) / "loop-back").symlink_to(loop)
        for args in (("--root", str(self.repo), "--list", str(loop)), ("--root", str(loop))):
            with self.subTest(args=args):
                result = run_lint(*args)
                self.assertEqual(("", 2), (result.stdout, result.returncode), result.stderr)
                self.assertTrue(result.stderr.startswith("lint-retired-terms: "), result.stderr)


if __name__ == "__main__":
    unittest.main()
