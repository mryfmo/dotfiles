#!/usr/bin/env python3
"""Exercise the Understand-Anything core build in update-agent-assets.sh with fake CLIs."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UPDATER = ROOT / "scripts/update-agent-assets.sh"
MAKEFILE = ROOT / "Makefile"
CHECKER = ROOT / "scripts/check-agent-runtime.py"
VERSION = "2.9.7"


class UnderstandAnythingCoreBuildTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="ua-core-build-test-"))
        self.home = self.temp / "home"
        self.bin = self.temp / "bin"
        self.bin.mkdir()
        self.log = self.temp / "calls.log"
        self.clone = self.home / ".understand-anything/repo/understand-anything-plugin"
        self.release = self.home / ".claude/plugins/cache/understand-anything/understand-anything" / VERSION
        self.make_plugin_tree(self.clone)
        (self.bin / "python3").symlink_to(sys.executable)
        for tool in ("bash", "cat", "cp", "dirname", "find", "mkdir", "rm"):
            found = shutil.which(tool)
            if found:
                (self.bin / tool).symlink_to(found)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def make_plugin_tree(self, root: Path) -> None:
        (root / ".claude-plugin").mkdir(parents=True)
        (root / ".claude-plugin/plugin.json").write_text(json.dumps({"version": VERSION}))
        (root / "packages/core/src").mkdir(parents=True)
        (root / "packages/core/src/index.ts").write_text("export {};\n")

    def write_fake(self, name: str, body: str) -> None:
        path = self.bin / name
        path.write_text(f'#!/bin/sh\nprintf \'%s|%s\\n\' "$PWD" "{name} $*" >> {self.log}\n{body}\n')
        path.chmod(0o755)

    def write_fake_pnpm(self, *, frozen_exit: int = 0, build_exit: int = 0) -> None:
        self.write_fake(
            "pnpm",
            textwrap.dedent(
                f"""
                case "$*" in
                  "install --frozen-lockfile") exit {frozen_exit} ;;
                  "--filter @understand-anything/core build")
                    [ {build_exit} -eq 0 ] || exit {build_exit}
                    mkdir -p packages/core/dist && printf 'built\\n' > packages/core/dist/index.js ;;
                esac
                exit 0
                """
            ),
        )

    def provision(self) -> subprocess.CompletedProcess[str]:
        env = {"HOME": str(self.home), "PATH": str(self.bin)}
        return subprocess.run(
            [
                "/bin/bash",
                "-c",
                f"source {UPDATER}; provision_codex_understand_anything_runtime",
            ],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def calls(self) -> list[str]:
        return self.log.read_text().splitlines() if self.log.exists() else []

    def test_builds_missing_core_in_the_release_artifact_then_copies_it(self) -> None:
        self.make_plugin_tree(self.release)
        self.write_fake_pnpm()

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.calls(),
            [
                f"{self.release}|pnpm install --frozen-lockfile",
                f"{self.release}|pnpm --filter @understand-anything/core build",
            ],
        )
        self.assertEqual((self.clone / "packages/core/dist/index.js").read_text(), "built\n")

    def test_frozen_install_failure_falls_back_to_plain_install(self) -> None:
        self.make_plugin_tree(self.release)
        self.write_fake_pnpm(frozen_exit=1)

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            [call.split("|", 1)[1] for call in self.calls()],
            [
                "pnpm install --frozen-lockfile",
                "pnpm install",
                "pnpm --filter @understand-anything/core build",
            ],
        )

    def test_skips_the_build_when_the_release_artifact_already_has_dist(self) -> None:
        self.make_plugin_tree(self.release)
        (self.release / "packages/core/dist").mkdir(parents=True)
        (self.release / "packages/core/dist/index.js").write_text("prebuilt\n")
        (self.release / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n")
        self.set_mtime(self.release / "packages/core/src/index.ts", 1_000_000)
        self.set_mtime(self.release / "pnpm-lock.yaml", 1_000_000)
        self.set_mtime(self.release / "packages/core/dist/index.js", 2_000_000)
        self.write_fake_pnpm()

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.calls(), [])
        self.assertEqual((self.clone / "packages/core/dist/index.js").read_text(), "prebuilt\n")

    @staticmethod
    def set_mtime(path: Path, seconds: int) -> None:
        os.utime(path, (seconds, seconds))

    def stale_dist(self, root: Path, *, newer: str) -> None:
        """Give root a prebuilt dist that is older than `newer` (src or lockfile)."""
        (root / "packages/core/dist").mkdir(parents=True)
        (root / "packages/core/dist/index.js").write_text("stale\n")
        (root / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n")
        for path in (root / "packages/core/src/index.ts", root / "pnpm-lock.yaml"):
            self.set_mtime(path, 1_000_000)
        self.set_mtime(root / "packages/core/dist/index.js", 2_000_000)
        target = root / "packages/core/src/index.ts" if newer == "src" else root / "pnpm-lock.yaml"
        self.set_mtime(target, 3_000_000)

    def test_rebuilds_a_release_dist_older_than_its_sources(self) -> None:
        for newer in ("src", "lockfile"):
            with self.subTest(newer=newer):
                shutil.rmtree(self.release, ignore_errors=True)
                shutil.rmtree(self.clone / "packages/core/dist", ignore_errors=True)
                self.log.unlink(missing_ok=True)
                self.make_plugin_tree(self.release)
                self.stale_dist(self.release, newer=newer)
                self.write_fake_pnpm()

                result = self.provision()

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(
                    [call.split("|", 1)[1] for call in self.calls()],
                    [
                        "pnpm install --frozen-lockfile",
                        "pnpm --filter @understand-anything/core build",
                    ],
                )
                self.assertEqual((self.clone / "packages/core/dist/index.js").read_text(), "built\n")

    def test_doctor_stale_warning_is_cleared_by_the_update_build(self) -> None:
        spec = importlib.util.spec_from_file_location("check_agent_runtime", CHECKER)
        assert spec is not None and spec.loader is not None
        doctor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(doctor)
        self.stale_dist(self.clone, newer="src")
        self.write_fake_pnpm()

        before = doctor.understand_anything_core_warnings(self.home)
        result = self.provision()
        after = doctor.understand_anything_core_warnings(self.home)

        self.assertEqual(len(before), 1, before)
        self.assertIn("Understand-Anything core build is stale", before[0])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(after, [])

    def test_builds_in_the_clone_when_no_release_artifact_exists(self) -> None:
        self.write_fake_pnpm()

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact",
            result.stdout,
        )
        self.assertEqual(
            self.calls(),
            [
                f"{self.clone}|pnpm install --frozen-lockfile",
                f"{self.clone}|pnpm --filter @understand-anything/core build",
            ],
        )
        self.assertTrue((self.clone / "packages/core/dist/index.js").is_file())

    def test_uses_mise_exec_when_pnpm_is_not_on_path(self) -> None:
        self.make_plugin_tree(self.release)
        self.write_fake(
            "mise",
            textwrap.dedent(
                """
                case "$*" in
                  "exec npm:pnpm -- pnpm --filter @understand-anything/core build")
                    mkdir -p packages/core/dist && printf 'built\\n' > packages/core/dist/index.js ;;
                esac
                exit 0
                """
            ),
        )

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            [call.split("|", 1)[1] for call in self.calls()],
            [
                "mise exec npm:pnpm -- pnpm install --frozen-lockfile",
                "mise exec npm:pnpm -- pnpm --filter @understand-anything/core build",
            ],
        )
        self.assertTrue((self.clone / "packages/core/dist/index.js").is_file())

    def write_fake_mise_exec_pnpm(self) -> None:
        """A mise whose `exec npm:pnpm -- pnpm ...` behaves like a working pnpm."""
        self.write_fake(
            "mise",
            textwrap.dedent(
                """
                case "$*" in
                  "exec npm:pnpm -- pnpm --filter @understand-anything/core build")
                    mkdir -p packages/core/dist && printf 'built\\n' > packages/core/dist/index.js ;;
                esac
                exit 0
                """
            ),
        )

    def test_prefers_mise_exec_over_an_unbacked_pnpm_shim(self) -> None:
        # The mise shim exists before the pinned version is installed.
        self.make_plugin_tree(self.release)
        self.write_fake(
            "pnpm",
            "printf 'mise ERROR No version is set for shim: pnpm\\n' >&2\nexit 1",
        )
        self.write_fake_mise_exec_pnpm()

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("WARN", result.stderr)
        self.assertEqual(
            [call.split("|", 1)[1] for call in self.calls()],
            [
                "mise exec npm:pnpm -- pnpm install --frozen-lockfile",
                "mise exec npm:pnpm -- pnpm --filter @understand-anything/core build",
            ],
        )
        self.assertEqual((self.clone / "packages/core/dist/index.js").read_text(), "built\n")

    def test_uses_path_pnpm_only_when_mise_is_absent(self) -> None:
        self.make_plugin_tree(self.release)
        self.write_fake_pnpm()

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.bin / "mise").exists())
        self.assertTrue(all("|pnpm " in call for call in self.calls()), self.calls())
        self.assertTrue((self.clone / "packages/core/dist/index.js").is_file())

    def test_make_update_installs_the_pinned_pnpm(self) -> None:
        result = subprocess.run(
            ["make", "-n", "-f", str(MAKEFILE), "update"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("mise install --locked npm:ccstatusline npm:ccusage npm:pnpm\n", result.stdout)

    def test_warns_and_continues_when_no_pnpm_is_resolvable(self) -> None:
        self.make_plugin_tree(self.release)

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN: Understand-Anything core not built: pnpm not found", result.stderr)
        self.assertIn("pnpm --filter @understand-anything/core build", result.stderr)
        self.assertFalse((self.clone / "packages/core/dist").exists())

    def test_warns_and_continues_when_the_build_fails(self) -> None:
        self.make_plugin_tree(self.release)
        self.write_fake_pnpm(build_exit=2)

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN: Understand-Anything core build failed", result.stderr)
        self.assertFalse((self.clone / "packages/core/dist").exists())


if __name__ == "__main__":
    unittest.main()
