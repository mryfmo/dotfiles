#!/usr/bin/env python3
"""Verify the pins-only release asset bump path and its 7-day window."""

from __future__ import annotations

import datetime
import email.utils
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOW = int(datetime.datetime(2026, 9, 27, tzinfo=datetime.timezone.utc).timestamp())
DAY = 86400


def days_ago(days: int) -> int:
    return NOW - days * DAY


class ReleaseAssetPinsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="release-asset-pins-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def pick(self, current: str, lines: list[tuple[str, int]]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "bash",
                "-c",
                'source scripts/upgrade-tools.sh; pick_windowed_pin tool "$1" "$2"',
                "_",
                current,
                str(NOW - 7 * DAY),
            ],
            cwd=ROOT,
            env={**os.environ, "LC_ALL": "C"},
            input="".join(f"{version}\t{published}\n" for version, published in lines),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_window_skips_a_young_release_and_takes_an_older_one(self) -> None:
        result = self.pick(
            "v1.25.1",
            [
                ("v1.27.0", days_ago(1)),
                ("v1.26.0", days_ago(90)),
                ("v1.25.1", days_ago(150)),
            ],
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("v1.26.0\n", result.stdout)
        self.assertIn(
            "release window: skipping tool v1.27.0 (published 1 day(s) ago, under 7)",
            result.stderr,
        )

    def test_window_never_moves_a_pin_backwards(self) -> None:
        result = self.pick(
            "v2026.9.12",
            [
                ("v2026.9.14", days_ago(2)),
                ("v2026.9.12", days_ago(6)),
                ("v2026.9.11", days_ago(9)),
            ],
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("v2026.9.12\n", result.stdout)

    def test_window_rejects_an_unknown_current_pin(self) -> None:
        result = self.pick("", [("v1.26.0", days_ago(90))])

        self.assertNotEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertNotIn("command not found", result.stderr)

    def executable(self, path: Path, body: str) -> None:
        path.write_text("#!/bin/bash\n" + textwrap.dedent(body))
        path.chmod(0o755)

    def test_bump_writes_only_the_four_pins_through_set_asset(self) -> None:
        repo = self.temp_dir / "repo"
        (repo / "scripts").mkdir(parents=True)
        (repo / "home/dot_agents").mkdir(parents=True)
        shutil.copy(ROOT / "scripts/upgrade-tools.sh", repo / "scripts/upgrade-tools.sh")
        # Fixed pins keep the fixture independent of the live manifest.
        (repo / "home/dot_agents/agent-config.yaml").write_text(
            "assets:\n"
            "  mise:\n    source: github-release\n    pin: v2026.9.12\n"
            "  sheldon:\n    source: crates\n    pin: 0.8.5\n"
            "  starship:\n    source: github-release\n    pin: v1.25.1\n"
            "  aws-cli:\n    source: https-download\n    pin: 2.35.21\n"
        )
        bin_dir = self.temp_dir / "bin"
        bin_dir.mkdir()
        log = self.temp_dir / "commands.log"
        crates = json.dumps(
            {
                "versions": [
                    {
                        "num": "0.9.0",
                        "created_at": "2026-09-26T00:00:00.123Z",
                        "yanked": False,
                    },
                    {
                        "num": "0.8.9",
                        "created_at": "2026-08-01T00:00:00.123Z",
                        "yanked": True,
                    },
                    {
                        "num": "0.8.6",
                        "created_at": "2026-07-01T00:00:00.123Z",
                        "yanked": False,
                    },
                ]
            }
        )
        aws_dates = {
            "2.37.4": email.utils.formatdate(days_ago(2), usegmt=True),
            "2.36.0": email.utils.formatdate(days_ago(20), usegmt=True),
        }
        self.executable(
            bin_dir / "gh",
            f"""
            printf 'gh %s\\n' "$*" >> "{log}"
            case "$2" in
                repos/jdx/mise/releases*)
                    printf 'v2026.9.14\\t{days_ago(2)}\\nv2026.9.12\\t{days_ago(6)}\\nv2026.9.11\\t{days_ago(9)}\\n' ;;
                repos/starship/starship/releases*)
                    printf 'v1.27.0\\t{days_ago(1)}\\nv1.26.0\\t{days_ago(90)}\\nv1.25.1\\t{days_ago(150)}\\n' ;;
                repos/aws/aws-cli/tags*)
                    printf '2.37.4\\n2.36.0\\n2.35.21\\n2.35.20\\n' ;;
                *) exit 1 ;;
            esac
            """,
        )
        self.executable(
            bin_dir / "curl",
            f"""
            printf 'curl %s\\n' "$*" >> "{log}"
            case "$*" in
                *crates.io/api/v1/crates/sheldon/versions*) printf '%s\\n' '{crates}' ;;
                *awscli-exe-linux-x86_64-2.37.4.zip*) printf 'HTTP/1.1 200 OK\\r\\nLast-Modified: {aws_dates["2.37.4"]}\\r\\n' ;;
                *awscli-exe-linux-x86_64-2.36.0.zip*) printf 'HTTP/1.1 200 OK\\r\\nLast-Modified: {aws_dates["2.36.0"]}\\r\\n' ;;
                *) exit 1 ;;
            esac
            """,
        )
        self.executable(bin_dir / "uv", f'printf \'uv %s\\n\' "$*" >> "{log}"\n')

        result = subprocess.run(
            ["bash", "-c", "source scripts/upgrade-tools.sh; bump_release_asset_pins"],
            cwd=repo,
            env={
                **os.environ,
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "UPGRADE_RELEASE_NOW": str(NOW),
            },
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        uv_calls = [line for line in log.read_text().splitlines() if line.startswith("uv ")]
        self.assertEqual(
            [
                "uv run --with pyyaml scripts/generate-agent-configs.py"
                " --set-asset mise.pin=v2026.9.12"
                " --set-asset sheldon.pin=0.8.6"
                " --set-asset starship.pin=v1.26.0"
                " --set-asset aws-cli.pin=2.36.0"
            ],
            uv_calls,
        )
        self.assertIn("skipping mise v2026.9.14", result.stderr)
        self.assertIn("skipping sheldon 0.9.0", result.stderr)
        self.assertIn("skipping starship v1.27.0", result.stderr)
        self.assertIn("skipping aws-cli 2.37.4", result.stderr)
        # The AWS walk stops at the first version outside the window.
        self.assertNotIn("2.35.21.zip", log.read_text())
        self.assertIn(
            "Pinned mise v2026.9.12, sheldon 0.8.6, starship v1.26.0, and aws-cli 2.36.0",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
