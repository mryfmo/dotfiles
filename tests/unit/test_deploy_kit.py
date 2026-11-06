"""Exercise scripts/deploy-kit.sh against a fake chezmoi and a fake asset refresh that record their calls."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/deploy-kit.sh"
# The recorder: every call appends its argv; managed and status answer from fixture files; FAIL names the one
# subcommand that exits 1 (failure injection); anything else the script never calls is refused.
FAKE_CHEZMOI = r"""#!/usr/bin/env bash
printf '%s\n' "chezmoi $*" >> "${CALLS}"
[ "$1" != "${FAIL:-}" ] || exit 1
case "$1" in
managed) cat "${MANAGED}" ;;
status) cat "${STATUS}" ;;
apply) shift; printf 'fake apply: %s\n' "$*" ;;
verify) ;;
*) exit 9 ;;
esac
"""
FAKE_ASSETS = r"""#!/usr/bin/env bash
printf '%s\n' "update-agent-assets.sh $*" >> "${CALLS}"
[ "assets" != "${FAIL:-}" ]
"""

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes, scratch_env


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


class DeployKitTest(unittest.TestCase):
    def run_deploy(self, status_rows, *, managed=None, fail="", dry_run=False):
        """Run a copy of the script beside a fake asset refresh, with HOME a scratch directory.

        status_rows: `XY <target relative to HOME>` lines; managed: the relative targets chezmoi lists (defaults
        to every status target plus two of the operator's). Returns (result, recorded calls).
        """
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory)
            home = scratch / "home"
            home.mkdir()
            scripts = scratch / "scripts"
            scripts.mkdir()
            shutil.copy(SCRIPT, scripts / "deploy-kit.sh")
            assets = scripts / "update-agent-assets.sh"
            assets.write_text(FAKE_ASSETS)
            assets.chmod(0o755)
            chezmoi = scratch / "bin/chezmoi"
            chezmoi.parent.mkdir()
            chezmoi.write_text(FAKE_CHEZMOI)
            chezmoi.chmod(0o755)
            status_lines = [row[:3] + str(home / row[3:]) for row in status_rows]
            if managed is None:
                managed = [row[3:] for row in status_rows] + [".zshrc", ".codex/config.toml"]
            managed_file = scratch / "managed"
            managed_file.write_text("".join(str(home / name) + "\n" for name in managed))
            status_file = scratch / "status"
            status_file.write_text("".join(line + "\n" for line in status_lines))
            calls = scratch / "calls"
            calls.touch()
            result = subprocess.run(
                [str(scripts / "deploy-kit.sh")] + (["--dry-run"] if dry_run else []),
                env=os.environ
                | scratch_env(home)
                | {
                    "PATH": str(chezmoi.parent) + os.pathsep + os.environ["PATH"],
                    "CALLS": str(calls),
                    "MANAGED": str(managed_file),
                    "STATUS": str(status_file),
                    "FAIL": fail,
                },
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            return result, calls.read_text().splitlines(), home

    def test_only_the_pending_kit_targets_are_applied_by_name_then_verified_then_the_assets_refreshed(self):
        rows = [
            " M .local/bin/pr-merge.sh",
            " A .agents/omp/profiles/dsh.yml",
            "   .dsh/profiles/thak/package.json",
            " M .codex/config.toml",
            "MM .codex/rules/default.rules",
            " M .zshrc",
            " M .config/herdr/config.toml",
            "R  .chezmoiscripts/common/00-refuse-dirty-source.sh",
        ]
        result, calls, home = self.run_deploy(rows)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        lever = str(home / ".local/bin/pr-merge.sh")
        profile = str(home / ".agents/omp/profiles/dsh.yml")
        self.assertEqual(
            [
                "chezmoi managed --path-style absolute",
                "chezmoi status --path-style absolute",
                f"chezmoi apply --verbose {lever} {profile}",
                f"chezmoi verify {lever} {profile}",
                "update-agent-assets.sh ",
            ],
            calls,
        )
        self.assertIn("deploy-kit: managed kit targets: 3\n", result.stdout)
        self.assertIn("deploy-kit: pending: 2\n", result.stdout)
        self.assertIn(f"deploy-kit: applied: 2\n  {lever}\n  {profile}\n", result.stdout)
        self.assertNotIn(".codex", "".join(call for call in calls if call.startswith("chezmoi apply")))

    def test_a_kit_target_that_is_not_what_chezmoi_last_wrote_refuses_with_its_row_and_applies_nothing(self):
        rows = [
            " M .local/bin/pr-merge.sh",
            "MM .agents/permgate-policy.yaml",
            "DA .dsh/profiles/thak/package.json",
        ]
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                result, calls, home = self.run_deploy(rows, dry_run=dry_run)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("deploy-kit: refused: 2 kit targets are not what chezmoi last wrote", result.stderr)
                self.assertIn(f"  MM {home / '.agents/permgate-policy.yaml'}\n", result.stderr)
                self.assertIn(f"  DA {home / '.dsh/profiles/thak/package.json'}\n", result.stderr)
                self.assertEqual(
                    ["chezmoi managed --path-style absolute", "chezmoi status --path-style absolute"], calls
                )

    def test_a_failing_chezmoi_read_refuses_before_anything_is_applied(self):
        rows = [" M .local/bin/pr-merge.sh"]
        expected = {
            "managed": (["chezmoi managed --path-style absolute"], "chezmoi managed failed"),
            "status": (
                ["chezmoi managed --path-style absolute", "chezmoi status --path-style absolute"],
                "chezmoi status failed",
            ),
        }
        for fail, (calls_expected, message) in expected.items():
            with self.subTest(fail=fail):
                result, calls, _ = self.run_deploy(rows, fail=fail)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertIn("nothing applied", result.stderr)
                self.assertEqual(calls_expected, calls)

    def test_no_managed_kit_target_refuses(self):
        result, calls, _ = self.run_deploy([" M .zshrc"], managed=[".zshrc", ".codex/config.toml"])
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("chezmoi manages no target under the kit roots", result.stderr)
        self.assertEqual(["chezmoi managed --path-style absolute"], calls)

    def test_a_dry_run_lists_the_pending_rows_and_applies_nothing(self):
        rows = [" M .local/bin/pr-merge.sh", " A .agents/omp/profiles/dsh.yml", " M .codex/config.toml"]
        result, calls, home = self.run_deploy(rows, dry_run=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(["chezmoi managed --path-style absolute", "chezmoi status --path-style absolute"], calls)
        self.assertIn(
            f"deploy-kit: pending: 2\n   M {home / '.local/bin/pr-merge.sh'}\n   A {home / '.agents/omp/profiles/dsh.yml'}\n",
            result.stdout,
        )
        self.assertIn("deploy-kit: dry run; nothing applied", result.stdout)

    def test_the_asset_refresh_runs_only_after_a_successful_apply_and_verify(self):
        rows = [" M .local/bin/pr-merge.sh"]
        for fail, message in (("apply", "chezmoi apply failed"), ("verify", "chezmoi verify finds")):
            with self.subTest(fail=fail):
                result, calls, _ = self.run_deploy(rows, fail=fail)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertNotIn("update-agent-assets.sh ", calls)
        with self.subTest(fail="assets"):
            result, calls, _ = self.run_deploy(rows, fail="assets")
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertEqual("update-agent-assets.sh ", calls[-1])
            self.assertIn("update-agent-assets.sh failed", result.stderr)

    def test_a_second_run_with_nothing_pending_applies_nothing_and_still_refreshes_the_assets(self):
        rows = ["   .local/bin/pr-merge.sh", " M .codex/config.toml"]
        result, calls, _ = self.run_deploy(rows)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            [
                "chezmoi managed --path-style absolute",
                "chezmoi status --path-style absolute",
                "update-agent-assets.sh ",
            ],
            calls,
        )
        self.assertIn("deploy-kit: pending: 0\n", result.stdout)
        self.assertIn("deploy-kit: applied: 0\n", result.stdout)


class DeployKitMakeTargetTest(unittest.TestCase):
    def test_make_deploy_kit_runs_the_script_and_dry_passes_dry_run(self):
        for dry, expected in (([], "./scripts/deploy-kit.sh"), (["DRY=1"], "./scripts/deploy-kit.sh --dry-run")):
            with self.subTest(dry=dry):
                result = subprocess.run(
                    ["make", "-n", "-s", "deploy-kit", *dry],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=True,
                )
                self.assertEqual([expected], result.stdout.splitlines())


if __name__ == "__main__":
    unittest.main()
