"""Exercise the start-up self-check of the coordinator's levers (regime-cutover U31).

Each lever hashes its own bytes and compares the digest with its `claude.levers.sha256.<name>` line in the manifest
beside it: the deployed `~/.agents/agent-config.yaml` for the copy chezmoi installs under `~/.local/bin/common`, the
checkout's `home/dot_agents/agent-config.yaml` otherwise. Every test builds the installed layout under a scratch HOME
from the checkout's own bytes; nothing reads the real `~/.agents` or `~/.local/bin`.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVERS = (
    "hcom-seat",
    "hcom-dispatch",
    "bus-history.sh",
    "worktree-gc.sh",
    "regime-env",
    "regime-init",
    "seat-login-preflight",
    "regime-start",
    "regime-stop",
    "pr-thread-reply.sh",
    "pr-thread-resolve.sh",
    "pr-update-branch.sh",
    "pr-close.sh",
    "pr-body-edit.sh",
    "pr-threads-check.sh",
    "records-sync.sh",
    "pr-merge.sh",
    "omp-run.sh",
)
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"


class LeverSelfCheckTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name).resolve() / "home"
        self.bin = self.home / ".local/bin/common"
        self.bin.mkdir(parents=True)
        (self.home / ".agents").mkdir()
        shutil.copy2(MANIFEST, self.home / ".agents/agent-config.yaml")
        for name in LEVERS:
            shutil.copy2(ROOT / "home/dot_local/bin/common" / f"executable_{name}", self.bin / name)
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}

    def run_lever(self, name, *args, env=None):
        return subprocess.run(
            [str(self.bin / name), *args],
            cwd=self.home,
            env=env or self.env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def fake_tools(self, *names, body="exit 3"):
        bindir = Path(self.temp.name) / "fake"
        bindir.mkdir(exist_ok=True)
        for name in names:
            (bindir / name).write_text(f"#!/bin/sh\n{body}\n")
            (bindir / name).chmod(0o755)
        return {**self.env, "PATH": f"{bindir}:{self.env['PATH']}"}

    def assert_refused(self, run, message):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused:", run.stderr)
        self.assertIn(message, run.stderr)

    def assert_passed(self, run):
        """The self-check let the lever through: none of its refusals is on stderr."""
        for refusal in ("refused: sha256", "refused: manifest", "refused: no single", "refused: cannot"):
            self.assertNotIn(refusal, run.stderr)

    def launch(self, argv, cwd, env):
        return subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=60, check=False)

    def test_the_installed_copies_are_the_checkout_bytes_and_pass(self):
        for name in LEVERS:
            with self.subTest(lever=name):
                self.assertEqual((self.bin / name).read_bytes(), (ROOT / "scripts/orchestrator" / name).read_bytes())
                run = self.run_lever(name)
                self.assertNotIn("refused: sha256", run.stderr)
                self.assertNotIn("refused: manifest", run.stderr)
                self.assertNotIn("refused: no single sha256 pin", run.stderr)

    def test_a_rewritten_installed_lever_refuses_to_run(self):
        for name in LEVERS:
            with self.subTest(lever=name):
                with (self.bin / name).open("a") as lever:
                    lever.write("echo rewritten\n")
                run = self.run_lever(name)
                self.assert_refused(run, "differs from the pin in")
                self.assertNotIn("rewritten", run.stdout)

    def test_the_installed_copy_trusts_the_deployed_manifest_not_the_checkout(self):
        manifest = self.home / ".agents/agent-config.yaml"
        text = manifest.read_text()
        pin_line = next(line for line in text.splitlines() if line.startswith("      bus-history.sh: "))
        manifest.write_text(text.replace(pin_line, "      bus-history.sh: " + "0" * 64))
        self.assert_refused(self.run_lever("bus-history.sh"), str(manifest))

    def test_a_missing_manifest_or_pin_refuses(self):
        manifest = self.home / ".agents/agent-config.yaml"
        text = manifest.read_text()
        pin_line = next(line for line in text.splitlines() if line.startswith("      hcom-dispatch: "))
        manifest.write_text(text.replace(pin_line + "\n", ""))
        self.assert_refused(self.run_lever("hcom-dispatch"), "no single sha256 pin for hcom-dispatch")
        manifest.write_text(text + pin_line + "\n")
        self.assert_refused(self.run_lever("hcom-dispatch"), "no single sha256 pin for hcom-dispatch")
        manifest.unlink()
        for name in LEVERS:
            with self.subTest(lever=name):
                self.assert_refused(self.run_lever(name), "manifest unreadable")

    def test_a_failing_producer_refuses_instead_of_passing(self):
        """Each read the decision rests on fails closed (preferences 21): the hash tools, then sed."""
        env = self.fake_tools("sha256sum", "shasum")
        for name in LEVERS:
            with self.subTest(lever=name, producer="hash"):
                self.assert_refused(self.run_lever(name, env=env), "cannot hash")
        env = self.fake_tools("sed")
        for name in LEVERS:
            with self.subTest(lever=name, producer="sed"):
                self.assert_refused(self.run_lever(name, env=env), "cannot read")

    def test_a_failing_dirname_is_not_consulted(self):
        """The script directory is split in the shell (U31b, audit row 2586): a dirname that prints an existing
        directory and exits nonzero cannot steer the self-check to another manifest, whatever the launch spelling."""
        decoy = Path(self.temp.name) / "decoy"
        (decoy / "home/dot_agents").mkdir(parents=True)
        (decoy / "x/y").mkdir(parents=True)  # an existing directory, as in the audit scenario
        (decoy / "home/dot_agents/agent-config.yaml").write_text("schema_version: 1\n")
        env = self.fake_tools("dirname", body=f"echo {decoy}/x/y; exit 1")
        path_env = {**env, "PATH": f"{self.bin}:{env['PATH']}"}
        for name in LEVERS:
            with self.subTest(lever=name, launch="installed path"):
                self.assert_passed(self.run_lever(name, env=env))
            with self.subTest(lever=name, launch="bare name through PATH"):
                self.assert_passed(self.launch([name], self.home, path_env))
            with self.subTest(lever=name, launch="checkout copy"):
                self.assert_passed(self.launch([str(ROOT / "scripts/orchestrator" / name)], self.home, env))

    def test_an_installed_lever_in_a_checkout_shaped_cwd_reads_the_deployed_manifest(self):
        """A cwd holding scripts/orchestrator and a manifest with other pins changes nothing for the installed copy."""
        checkout = Path(self.temp.name) / "checkout"
        (checkout / "scripts/orchestrator").mkdir(parents=True)
        (checkout / "home/dot_agents").mkdir(parents=True)
        text = MANIFEST.read_text()
        zeroed = text
        for name in LEVERS:
            pin_line = next(line for line in text.splitlines() if line.startswith(f"      {name}: "))
            zeroed = zeroed.replace(pin_line, f"      {name}: " + "0" * 64)
            shutil.copy2(self.bin / name, checkout / "scripts/orchestrator" / name)
        (checkout / "home/dot_agents/agent-config.yaml").write_text(zeroed)
        path_env = {**self.env, "PATH": f"{self.bin}:{self.env['PATH']}"}
        for name in LEVERS:
            with self.subTest(lever=name, deployed="current"):
                self.assert_passed(self.launch([name], checkout, path_env))
        (self.home / ".agents/agent-config.yaml").write_text(zeroed)
        (checkout / "home/dot_agents/agent-config.yaml").write_text(text)
        for name in LEVERS:
            with self.subTest(lever=name, deployed="stale"):
                self.assert_refused(
                    self.launch([name], checkout, path_env), str(self.home / ".agents/agent-config.yaml")
                )


if __name__ == "__main__":
    unittest.main()
