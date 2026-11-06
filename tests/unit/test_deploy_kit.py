"""Exercise scripts/deploy-kit.sh against a fake chezmoi and a fake asset updater that record their calls."""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/deploy-kit.sh"
UPDATER = ROOT / "scripts/update-agent-assets.sh"
KIT_ROOTS = (".local/bin", ".agents", ".dsh")
# The kit asset function table of scripts/deploy-kit.sh, in its order: the updater steps whose writes stay under
# the kit roots. A change here is a boundary change and needs the table, the whitelist and the body changed too.
KIT_ASSET_FUNCTIONS = (
    "retire_shared_pstack_copies",
    "retire_marketplace_dev_workflows",
    "retire_agmsg_shim",
    "update_security_audit_skill",
    "update_deepseek_harness",
    "update_compactiondb",
    "manifest_prune_retired",
)
# The recorder: every call appends its argv; managed and status answer from fixture files; FAIL names the one
# subcommand that exits non-zero (failure injection, FAIL_STATUS the status); anything else the script never calls
# is refused.
FAKE_CHEZMOI = r"""#!/usr/bin/env bash
printf '%s\n' "chezmoi $*" >> "${CALLS}"
[ "$1" != "${FAIL:-}" ] || exit "${FAIL_STATUS:-1}"
case "$1" in
managed) cat "${MANAGED}" ;;
status) cat "${STATUS}" ;;
apply) shift; printf 'fake apply: %s\n' "$*" ;;
verify) ;;
*) exit 9 ;;
esac
"""
# The fake updater: records its argv, refuses a call without exactly one function name (the updater's main would
# run every step, the operator's included), and fails on the function FAIL names.
FAKE_ASSETS = r"""#!/usr/bin/env bash
printf '%s\n' "update-agent-assets.sh $*" >> "${CALLS}"
[ "$#" -eq 1 ] || exit 2
[ "$1" != "${FAIL:-}" ]
"""
FAKE_DIRNAME = "#!/usr/bin/env bash\nexit 1\n"

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes, scratch_env


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


def asset_calls(names):
    return [f"update-agent-assets.sh {name}" for name in names]


class DeployKitTest(unittest.TestCase):
    def run_deploy(self, status_rows, *, managed=None, fail="", fail_status=1, dry_run=False, roots=None):
        """Run a copy of the script beside a fake asset updater, with HOME a scratch directory.

        status_rows: `XY <target relative to HOME>` lines; managed: the relative targets chezmoi lists (defaults
        to every status target plus two of the operator's); fail: the chezmoi subcommand, the kit function or the
        producer (`dirname`) that fails; roots: how each kit root is laid out (`dir`, `link`, `missing`,
        `parent-link`; every root a real directory by default). Returns (result, recorded calls, home).
        """
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory)
            home = scratch / "home"
            home.mkdir()
            elsewhere = scratch / "elsewhere"
            elsewhere.mkdir()
            for name in KIT_ROOTS:
                layout = (roots or {}).get(name, "dir")
                if layout == "dir":
                    (home / name).mkdir(parents=True)
                elif layout == "link":
                    (home / name).parent.mkdir(parents=True, exist_ok=True)
                    (home / name).symlink_to(elsewhere)
                elif layout == "parent-link":
                    (home / name).parent.parent.mkdir(parents=True, exist_ok=True)
                    (home / name).parent.symlink_to(elsewhere)
                    (elsewhere / Path(name).name).mkdir()
                else:
                    assert layout == "missing", layout
            scripts = scratch / "scripts"
            scripts.mkdir()
            shutil.copy(SCRIPT, scripts / "deploy-kit.sh")
            assets = scripts / "update-agent-assets.sh"
            assets.write_text(FAKE_ASSETS)
            assets.chmod(0o755)
            fakes = scratch / "bin"
            fakes.mkdir()
            chezmoi = fakes / "chezmoi"
            chezmoi.write_text(FAKE_CHEZMOI)
            chezmoi.chmod(0o755)
            if fail == "dirname":
                dirname = fakes / "dirname"
                dirname.write_text(FAKE_DIRNAME)
                dirname.chmod(0o755)
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
                    "PATH": str(fakes) + os.pathsep + os.environ["PATH"],
                    "CALLS": str(calls),
                    "MANAGED": str(managed_file),
                    "STATUS": str(status_file),
                    "FAIL": fail,
                    "FAIL_STATUS": str(fail_status),
                },
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            return result, calls.read_text().splitlines(), home

    @staticmethod
    def read_calls(home):
        roots = " ".join(str(home / name) for name in KIT_ROOTS)
        return [
            f"chezmoi managed --path-style absolute --refresh-externals=never -- {roots}",
            f"chezmoi status --path-style absolute --refresh-externals=never -- {roots}",
        ]

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
            self.read_calls(home)
            + [
                f"chezmoi apply --verbose --refresh-externals=never {lever} {profile}",
                f"chezmoi verify --refresh-externals=never {lever} {profile}",
            ]
            + asset_calls(KIT_ASSET_FUNCTIONS),
            calls,
        )
        self.assertIn("deploy-kit: managed kit targets: 3\n", result.stdout)
        self.assertIn("deploy-kit: pending: 2\n", result.stdout)
        self.assertIn(f"deploy-kit: applied: 2\n  {lever}\n  {profile}\n", result.stdout)
        self.assertNotIn(".codex", "".join(call for call in calls if call.startswith("chezmoi apply")))

    def test_the_asset_step_calls_the_updater_once_per_kit_function_by_name_and_never_without_an_argument(self):
        result, calls, _ = self.run_deploy(["   .local/bin/pr-merge.sh"])
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        updater_calls = [call for call in calls if call.startswith("update-agent-assets.sh")]
        self.assertEqual(asset_calls(KIT_ASSET_FUNCTIONS), updater_calls)
        self.assertNotIn("update-agent-assets.sh ", updater_calls)
        self.assertEqual(len(KIT_ASSET_FUNCTIONS), len(set(updater_calls)))
        for name in KIT_ASSET_FUNCTIONS:
            self.assertRegex(result.stdout, rf"deploy-kit: \S*update-agent-assets\.sh {name}\n")

    def test_a_failing_kit_function_stops_the_asset_step_with_its_name(self):
        failing = KIT_ASSET_FUNCTIONS[3]
        result, calls, _ = self.run_deploy(["   .local/bin/pr-merge.sh"], fail=failing)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"update-agent-assets.sh {failing} failed; the later kit asset steps not run", result.stderr)
        self.assertEqual(asset_calls(KIT_ASSET_FUNCTIONS[:4]), calls[2:])
        self.assertNotIn("deploy-kit: applied:", result.stdout)

    def test_every_kit_function_is_in_the_updaters_single_function_whitelist(self):
        text = UPDATER.read_text()
        match = re.search(r'case "\$#:\$1" in\n\s*((?:1:\w+(?: \| )?)+)\)', text)
        self.assertIsNotNone(match, "the updater's main has no single-function case")
        whitelist = [entry.removeprefix("1:") for entry in match.group(1).split(" | ")]
        main_body = text[text.index("function main()") :]
        for name in KIT_ASSET_FUNCTIONS:
            self.assertIn(name, whitelist)
            self.assertIn(f"\n    {name}\n", main_body, f"{name} is not a step of the updater's main")

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
                self.assertEqual(self.read_calls(home), calls)

    def test_a_failing_producer_refuses_before_anything_is_applied(self):
        rows = [" M .local/bin/pr-merge.sh"]
        expected = {
            "dirname": (1, 0, "dirname failed"),
            "managed": (1, 1, "chezmoi managed failed"),
            "status": (3, 2, "chezmoi status failed"),
        }
        for fail, (fail_status, read_count, message) in expected.items():
            with self.subTest(fail=fail):
                result, calls, home = self.run_deploy(rows, fail=fail, fail_status=fail_status)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertIn("nothing applied", result.stderr)
                self.assertEqual(self.read_calls(home)[:read_count], calls)

    def test_a_linked_or_missing_kit_root_refuses_with_its_path_before_any_read(self):
        rows = [" M .local/bin/pr-merge.sh", " M .agents/permgate-policy.yaml", " M .dsh/profiles/thak/package.json"]
        cases = [(name, layout) for name in KIT_ROOTS for layout in ("link", "missing")] + [
            (".local/bin", "parent-link")
        ]
        for name, layout in cases:
            with self.subTest(root=name, layout=layout):
                result, calls, home = self.run_deploy(rows, roots={name: layout})
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(str(home / name), result.stderr)
                self.assertIn(
                    {"link": "is a symbolic link", "missing": "is missing", "parent-link": "resolves to"}[layout],
                    result.stderr,
                )
                self.assertIn("nothing applied", result.stderr)
                self.assertEqual([], calls)

    def test_managed_and_status_are_called_with_the_three_roots_and_no_refresh(self):
        result, calls, home = self.run_deploy(["   .local/bin/pr-merge.sh"], dry_run=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(self.read_calls(home), calls)
        for call in calls:
            self.assertTrue(call.endswith(" -- " + " ".join(str(home / name) for name in KIT_ROOTS)), call)
            self.assertIn(" --refresh-externals=never ", call)

    def test_no_managed_kit_target_refuses(self):
        result, calls, home = self.run_deploy([" M .zshrc"], managed=[".zshrc", ".codex/config.toml"])
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("chezmoi manages no target under the kit roots", result.stderr)
        self.assertEqual(self.read_calls(home)[:1], calls)

    def test_a_dry_run_lists_the_pending_rows_and_applies_nothing(self):
        rows = [" M .local/bin/pr-merge.sh", " A .agents/omp/profiles/dsh.yml", " M .codex/config.toml"]
        result, calls, home = self.run_deploy(rows, dry_run=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(self.read_calls(home), calls)
        self.assertIn(
            f"deploy-kit: pending: 2\n   M {home / '.local/bin/pr-merge.sh'}\n   A {home / '.agents/omp/profiles/dsh.yml'}\n",
            result.stdout,
        )
        self.assertIn("deploy-kit: dry run; nothing applied", result.stdout)

    def test_the_asset_step_runs_only_after_a_successful_apply_and_verify(self):
        rows = [" M .local/bin/pr-merge.sh"]
        for fail, message in (("apply", "chezmoi apply failed"), ("verify", "chezmoi verify finds")):
            with self.subTest(fail=fail):
                result, calls, _ = self.run_deploy(rows, fail=fail)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertEqual([], [call for call in calls if call.startswith("update-agent-assets.sh")])

    def test_a_second_run_with_nothing_pending_applies_nothing_and_still_runs_the_asset_step(self):
        rows = ["   .local/bin/pr-merge.sh", " M .codex/config.toml"]
        result, calls, home = self.run_deploy(rows)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(self.read_calls(home) + asset_calls(KIT_ASSET_FUNCTIONS), calls)
        self.assertIn("deploy-kit: pending: 0\n", result.stdout)
        self.assertIn("deploy-kit: applied: 0\n", result.stdout)

    def test_the_script_has_no_here_string_and_no_bare_updater_call(self):
        text = SCRIPT.read_text()
        self.assertNotIn("<<<", text)
        self.assertIsNone(re.search(r'update-agent-assets\.sh"?\s*$', text, re.MULTILINE))
        self.assertNotIn("<(", text)


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
