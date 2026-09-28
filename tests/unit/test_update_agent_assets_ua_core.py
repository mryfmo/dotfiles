#!/usr/bin/env python3
"""Exercise the Understand-Anything core build in update-agent-assets.sh with fake CLIs."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UPDATER = ROOT / "scripts/update-agent-assets.sh"
VERSION = "2.9.7"


class UnderstandAnythingCoreBuildTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="ua-core-build-test-"))
        self.home = self.temp / "home"
        self.bin = self.temp / "bin"
        self.bin.mkdir()
        self.log = self.temp / "calls.log"
        self.clone = self.home / ".understand-anything/repo/understand-anything-plugin"
        self.release = (
            self.home
            / ".claude/plugins/cache/understand-anything/understand-anything"
            / VERSION
        )
        self.make_plugin_tree(self.clone)
        (self.bin / "python3").symlink_to(sys.executable)
        for tool in ("bash", "cat", "cp", "dirname", "mkdir", "rm"):
            found = shutil.which(tool)
            if found:
                (self.bin / tool).symlink_to(found)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def make_plugin_tree(self, root: Path) -> None:
        (root / ".claude-plugin").mkdir(parents=True)
        (root / ".claude-plugin/plugin.json").write_text(
            json.dumps({"version": VERSION})
        )
        (root / "packages/core/src").mkdir(parents=True)
        (root / "packages/core/src/index.ts").write_text("export {};\n")

    def write_fake(self, name: str, body: str) -> None:
        path = self.bin / name
        path.write_text(
            f'#!/bin/sh\nprintf \'%s|%s\\n\' "$PWD" "{name} $*" >> {self.log}\n{body}\n'
        )
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
        self.assertEqual(
            (self.clone / "packages/core/dist/index.js").read_text(), "built\n"
        )

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
        self.write_fake_pnpm()

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.calls(), [])
        self.assertEqual(
            (self.clone / "packages/core/dist/index.js").read_text(), "prebuilt\n"
        )

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

    def test_warns_and_continues_when_no_pnpm_is_resolvable(self) -> None:
        self.make_plugin_tree(self.release)

        result = self.provision()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "WARN: Understand-Anything core not built: pnpm not found", result.stderr
        )
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
