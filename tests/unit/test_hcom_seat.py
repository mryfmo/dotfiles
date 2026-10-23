"""Exercise scripts/orchestrator/hcom-seat against fake hcom, herdr and omp.

The fakes (tests/fixtures/hcom-seat/fake-tool.py under the three names) record argv; the fake hcom plays the herdr
terminal preset so the test sees what omp receives. HOME is a scratch directory holding the three policy overlays and
the two extension directories; the cwd is a scratch git repository with an `origin/main` ref; `HCOM_DIR` is
`$TMPDIR/u7-hcom`. Nothing touches the real `~/.hcom`, `~/.agents` or a herdr pane.
"""

import json
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEAT = ROOT / "scripts/orchestrator/hcom-seat"
FAKE = ROOT / "tests/fixtures/hcom-seat/fake-tool.py"
GIT_IDENTITY = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
}


class HcomSeatTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.home = root / "home"
        self.policies = self.home / ".agents/omp/policies"
        self.policies.mkdir(parents=True)
        for role in ("orchestrator", "worker", "audit"):
            (self.policies / f"{role}.yml").write_text("tools: {}\n")
        self.bridge = self.home / ".local/lib/omp-extensions/pi-claude-bridge"
        self.siwc = self.home / ".agents/omp/extensions/openai-siwc"
        self.bridge.mkdir(parents=True)
        self.siwc.mkdir(parents=True)
        bindir = root / "bin"
        bindir.mkdir()
        for tool in ("hcom", "herdr", "omp"):
            (bindir / tool).symlink_to(FAKE)
        self.calls = root / "calls"
        self.calls.mkdir()
        self.seats = str(root / "seats")
        self.store = Path(os.environ.get("TMPDIR", self.temp.name)) / "u7-hcom"
        self.store.mkdir(exist_ok=True)
        self.repo = root / "repo"
        self.repo.mkdir()
        self.env = {
            **os.environ,
            **GIT_IDENTITY,
            "HOME": str(self.home),
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "HCOM_DIR": str(self.store),
            "FAKE_CALLS": str(self.calls),
        }
        self.git("init", "-q")
        self.git("commit", "-q", "--allow-empty", "-m", "init")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.head = self.git("rev-parse", "HEAD")

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.repo, env=self.env, capture_output=True, text=True, check=True
        ).stdout.strip()

    def seat(self, *args, cwd=None, **overrides):
        env = {**self.env, **{key: value for key, value in overrides.items() if value is not None}}
        for key in (key for key, value in overrides.items() if value is None):
            env.pop(key, None)
        return subprocess.run(
            [str(SEAT), *args], cwd=cwd or self.repo, env=env, capture_output=True, text=True, check=False
        )

    def calls_of(self, tool):
        path = self.calls / tool
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def launch_line(self, role, name, directory, *exts):
        return [
            "hcom", "omp", "--tag", name, "--dir", directory, "--terminal", "herdr", "--",
            "--profile", role, "--config", str(self.policies / f"{role}.yml"),
            *(flag for ext in exts for flag in ("-e", str(ext))),
        ]  # fmt: skip

    def test_the_worker_launch_reaches_omp_in_a_worktree_of_origin_main(self):
        clone = f"{self.seats}/worker"
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        expected = self.launch_line("worker", "worker", clone, self.bridge, self.siwc)
        self.assertEqual([call["argv"] for call in self.calls_of("hcom")], [expected[1:]])
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=clone), self.head)
        common = Path(self.git("rev-parse", "--git-common-dir", cwd=clone)).resolve()
        self.assertEqual(common, (self.repo / ".git").resolve())
        (omp,) = self.calls_of("omp")
        self.assertEqual(omp["argv"], expected[expected.index("--") + 1 :])
        self.assertEqual(Path(omp["cwd"]).resolve(), Path(clone).resolve())
        self.assertEqual(
            {key: omp["env"][key] for key in ("HCOM_LAUNCHED", "HCOM_TAG", "HCOM_DIR")},
            {"HCOM_LAUNCHED": "1", "HCOM_TAG": "worker", "HCOM_DIR": str(self.store)},
        )
        self.assertEqual(self.calls_of("herdr")[0]["argv"], ["tab", "create", "--label", "worker"])
        again = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 2)

    def test_each_role_gets_its_directory_and_extension_order(self):
        for role, name, directory, exts in (
            ("orchestrator", "orchestrator", str(self.repo.resolve()), (self.bridge, self.siwc)),
            ("worker", "worker-2", f"{self.seats}/worker-2", (self.bridge, self.siwc)),
            ("audit", "audit", f"{self.seats}/audit", (self.siwc, self.bridge)),
        ):
            with self.subTest(role=role):
                run = self.seat(role, "--name", name, "--seats-root", self.seats, "--dry-run")
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(shlex.split(run.stdout), self.launch_line(role, name, directory, *exts))
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats).exists())

    def test_an_absent_optional_extension_is_dropped_and_ext_replaces_the_list(self):
        shutil.rmtree(self.siwc)
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            shlex.split(run.stdout), self.launch_line("worker", "worker", f"{self.seats}/worker", self.bridge)
        )
        mine = self.home / "mine"
        mine.mkdir()
        run = self.seat("audit", "--seats-root", self.seats, "--ext", str(mine), "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(shlex.split(run.stdout), self.launch_line("audit", "audit", f"{self.seats}/audit", mine))

    def test_refusals_exit_2_before_anything_is_created_or_started(self):
        (self.policies / "audit.yml").unlink()
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        for label, args, overrides, cwd in (
            ("unknown role", ["reviewer"], {}, None),
            ("no role", [], {}, None),
            ("bad name", ["worker", "--name", "Worker/1"], {}, None),
            ("missing value", ["worker", "--name"], {}, None),
            ("unknown flag", ["worker", "--pane", "w1"], {}, None),
            ("HCOM_DIR unset", ["worker"], {"HCOM_DIR": None}, None),
            ("hcom absent", ["worker"], {"PATH": "/usr/bin:/bin"}, None),
            ("policy absent", ["audit"], {}, None),
            ("required extension absent", ["audit", "--ext", str(self.home / "nowhere")], {}, None),
            ("outside a checkout", ["worker"], {}, outside),
        ):
            with self.subTest(label):
                run = self.seat(*args, "--seats-root", self.seats, cwd=cwd, **overrides)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.startswith("hcom-seat: "), run.stderr)
        shutil.rmtree(self.bridge)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(str(self.bridge), run.stderr)
        self.assertEqual([self.calls_of(tool) for tool in ("hcom", "herdr", "omp")], [[], [], []])
        self.assertFalse(Path(self.seats).exists())


if __name__ == "__main__":
    unittest.main()
