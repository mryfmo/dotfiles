#!/usr/bin/env python3
"""Verify the bwrap AppArmor userns install step and its doctor probe."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "install/ubuntu/common/apparmor_userns.sh"
PROFILE = ROOT / "install/ubuntu/common/apparmor/bwrap-userns"
CHECK_TOOLS = ROOT / "scripts/check-tools.sh"
WRAPPER = ROOT / "home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl"


def debian_like() -> bool:
    try:
        release = Path("/etc/os-release").read_text()
    except OSError:
        return False
    return "debian" in release.lower()


class AppArmorUsernsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="apparmor-userns-test-"))
        self.bin = self.temp_dir / "bin"
        self.bin.mkdir()
        self.log = self.temp_dir / "calls.log"
        self.sysctl = self.temp_dir / "apparmor_restrict_unprivileged_userns"
        self.profile_target = self.temp_dir / "etc/apparmor.d/bwrap-userns"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def fake(self, name: str, exit_code: int = 0) -> Path:
        path = self.bin / name
        path.write_text(
            f'#!/bin/bash\necho "{name} $*" >> "{self.log}"\nexit {exit_code}\n'
        )
        path.chmod(0o755)
        return path

    def env(self, restricted: str = "1", bwrap: Path | None = None) -> dict[str, str]:
        self.sysctl.write_text(f"{restricted}\n")
        return {
            "PATH": f"{self.bin}:/usr/bin:/bin",
            "HOME": str(self.temp_dir),
            "APPARMOR_USERNS_SYSCTL": str(self.sysctl),
            "APPARMOR_USERNS_BWRAP": str(bwrap or self.temp_dir / "missing-bwrap"),
            "APPARMOR_USERNS_PROFILE_TARGET": str(self.profile_target),
        }

    def calls(self) -> list[str]:
        return self.log.read_text().splitlines() if self.log.exists() else []

    def run_installer(self, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(INSTALLER)],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_doctor(self, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "bash",
                "-c",
                'source "$1"; check_apparmor_userns; '
                'echo "req=${required_failures} opt=${optional_warnings}"',
                "_",
                str(CHECK_TOOLS),
            ],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_installer_is_a_no_op_when_the_host_does_not_need_the_profile(
        self,
    ) -> None:
        bwrap = self.fake("bwrap")
        for label, restricted, parser, bwrap_path, reason in (
            ("restriction off", "0", True, bwrap, "restriction is not enabled"),
            ("no parser", "1", False, bwrap, "apparmor_parser is not installed"),
            ("no bwrap", "1", True, None, "missing-bwrap is not installed"),
        ):
            with self.subTest(label):
                self.log.unlink(missing_ok=True)
                (self.bin / "apparmor_parser").unlink(missing_ok=True)
                if parser:
                    self.fake("apparmor_parser")
                self.fake("sudo")
                result = self.run_installer(self.env(restricted, bwrap_path))

                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(reason, result.stdout)
                self.assertEqual([], [c for c in self.calls() if c.startswith("sudo")])

    def test_installer_copies_and_reloads_the_profile_with_sudo(self) -> None:
        self.fake("apparmor_parser")
        self.fake("sudo")
        bwrap = self.fake("bwrap")
        for label, extra_env, source in (
            ("repo checkout", {}, str(PROFILE)),
            (
                "chezmoi source dir",
                {"CHEZMOI_SOURCE_DIR": str(ROOT / "home")},
                f"{ROOT / 'home'}/../install/ubuntu/common/apparmor/bwrap-userns",
            ),
        ):
            with self.subTest(label):
                self.log.unlink(missing_ok=True)
                result = self.run_installer({**self.env("1", bwrap), **extra_env})

                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(
                    [
                        f"sudo install -m 0644 {source} {self.profile_target}",
                        f"sudo apparmor_parser -r {self.profile_target}",
                    ],
                    self.calls(),
                )
                self.assertIn("Loaded AppArmor profile bwrap-userns", result.stdout)

    def test_installer_fails_when_loading_the_profile_fails(self) -> None:
        self.fake("apparmor_parser")
        self.fake("sudo", exit_code=1)
        result = self.run_installer(self.env("1", self.fake("bwrap")))

        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            [f"sudo install -m 0644 {PROFILE} {self.profile_target}"], self.calls()
        )
        self.assertNotIn("Loaded AppArmor profile", result.stdout)

    def test_doctor_is_not_applicable_without_the_restriction(self) -> None:
        self.fake("codex")
        result = self.run_doctor(self.env("0", self.fake("bwrap", exit_code=1)))

        self.assertIn("not applicable: AppArmor userns restriction", result.stdout)
        self.assertIn("req=0 opt=0", result.stdout)
        self.assertEqual([], [c for c in self.calls() if c.startswith("bwrap")])

    def test_doctor_warns_optionally_when_codex_is_missing(self) -> None:
        result = self.run_doctor(self.env("1", self.fake("bwrap")))

        self.assertIn("codex is not installed", result.stderr)
        self.assertIn("req=0 opt=1", result.stdout)

    def test_doctor_passes_when_the_bwrap_probe_succeeds(self) -> None:
        self.fake("codex")
        result = self.run_doctor(self.env("1", self.fake("bwrap")))

        self.assertIn("found:   bwrap user namespaces allowed", result.stdout)
        self.assertIn("req=0 opt=0", result.stdout)
        self.assertIn("bwrap --ro-bind / / true", self.calls())

    def test_doctor_fails_when_the_bwrap_probe_fails(self) -> None:
        self.fake("codex")
        bwrap = self.fake("bwrap", exit_code=1)
        for label, installed, message in (
            ("profile missing", False, "is missing, so sandboxed codex runs fail"),
            ("profile not loaded", True, "exists but is not effective"),
        ):
            with self.subTest(label):
                if installed:
                    self.profile_target.parent.mkdir(parents=True, exist_ok=True)
                    self.profile_target.write_text(PROFILE.read_text())
                result = self.run_doctor(self.env("1", bwrap))

                self.assertIn(message, result.stderr)
                self.assertIn("req=1 opt=0", result.stdout)


    def test_doctor_fails_when_bwrap_is_missing_with_codex(self) -> None:
        self.fake("codex")
        result = self.run_doctor(self.env("1"))

        self.assertIn("missing-bwrap is missing; sandboxed codex runs need it", result.stderr)
        self.assertIn("req=1 opt=0", result.stdout)

    @unittest.skipUnless(
        shutil.which("chezmoi") and debian_like(), "needs chezmoi on a Debian-like host"
    )
    def test_wrapper_re_renders_when_prerequisites_change(self) -> None:
        home = self.temp_dir / "chezmoi-home"
        home.mkdir()
        present = self.fake("bwrap")

        def render(bwrap: Path, restricted: str) -> str:
            self.sysctl.write_text(f"{restricted}\n")
            result = subprocess.run(
                ["chezmoi", "execute-template", "--source", str(ROOT / "home")],
                input=WRAPPER.read_text(),
                env={
                    **os.environ,
                    "HOME": str(home),
                    "APPARMOR_USERNS_BWRAP": str(bwrap),
                    "APPARMOR_USERNS_SYSCTL": str(self.sysctl),
                },
                text=True,
                capture_output=True,
                check=True,
            )
            return result.stdout

        skipped = render(self.temp_dir / "missing-bwrap", "1")
        ready = render(present, "1")
        unrestricted = render(present, "0")

        self.assertIn("bwrap=absent", skipped)
        self.assertIn("bwrap=present", ready)
        self.assertIn("restriction=1", ready)
        self.assertIn("restriction=0", unrestricted)
        self.assertEqual(3, len({skipped, ready, unrestricted}))

if __name__ == "__main__":
    unittest.main()
