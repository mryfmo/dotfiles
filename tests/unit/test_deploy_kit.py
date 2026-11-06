"""Exercise scripts/deploy-kit.sh against a fake chezmoi that records its calls."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/deploy-kit.sh"
KIT_ROOTS = (".local/bin", ".agents", ".dsh")
# The recorder: every call appends its argv; managed and status answer from fixture files, and MANAGED_AFTER, when
# set, is the listing every managed call after the first answers (the source changed during the run); FAIL names
# the one subcommand that exits non-zero (failure injection, FAIL_STATUS the status) from its FAIL_NTH-th call on
# (1: every call); SWAP_ROOT names a kit root the fake replaces with a link to SWAP_TO when status is called (the
# root changes between the two reads); anything else the script never calls is refused.
FAKE_CHEZMOI = r"""#!/usr/bin/env bash
printf '%s\n' "chezmoi $*" >> "${CALLS}"
[ "$1" != "${FAIL:-}" ] || [ "$(grep -c "^chezmoi $1 " "${CALLS}")" -lt "${FAIL_NTH:-1}" ] || exit "${FAIL_STATUS:-1}"
[ "$1" != status ] || [ -z "${SWAP_ROOT:-}" ] || { rmdir "${SWAP_ROOT}" && ln -s "${SWAP_TO}" "${SWAP_ROOT}"; }
case "$1" in
managed) cat "${MANAGED}"; [ -z "${MANAGED_AFTER:-}" ] || cp "${MANAGED_AFTER}" "${MANAGED}" ;;
status) cat "${STATUS}" ;;
apply) shift; printf 'fake apply: %s\n' "$*" ;;
verify) ;;
*) exit 9 ;;
esac
"""
# Failure injection for the physical-path reads: `pwd` is a bash builtin, so a PATH stub never reaches it; bash
# reads BASH_ENV before a non-interactive script runs, and a function named pwd shadows the builtin. The function
# fails for the one physical directory FAIL_PWD names and answers as the builtin otherwise.
FAKE_PWD_ENV = r"""pwd() {
    [[ ${PWD} != "${FAIL_PWD}" ]] || return 1
    builtin pwd "$@"
}
"""

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes, scratch_env


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


class DeployKitTest(unittest.TestCase):
    def run_deploy(
        self,
        status_rows,
        *,
        managed=None,
        managed_after=None,
        fail="",
        fail_nth=1,
        fail_status=1,
        dry_run=False,
        roots=None,
        swap_root=None,
        present=None,
    ):
        """Run a copy of the script with HOME a scratch directory and a fake chezmoi first on PATH.

        status_rows: `XY <target relative to HOME>` lines; managed: the relative targets chezmoi lists (defaults
        to every status target plus two of the operator's); managed_after: the relative targets every managed call
        after the first lists; fail: the chezmoi subcommand that fails from its fail_nth-th call on, or
        `pwd:<relative directory>` (`pwd:.` for HOME) for a failing physical-path read; roots: how each kit root
        is laid out (`dir`, `link`, `missing`, `parent-link`; every root a real directory by default); swap_root:
        the kit root the fake replaces with a link when status is called; present: relative targets that exist
        under HOME before the run (`file` or `dangling-link`; the fake apply deletes nothing, so a `D` row's
        target stays as laid out). Returns (result, recorded calls, home).
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
            for name, kind in (present or {}).items():
                (home / name).parent.mkdir(parents=True, exist_ok=True)
                if kind == "file":
                    (home / name).write_text("retired\n")
                else:
                    assert kind == "dangling-link", kind
                    (home / name).symlink_to(scratch / "gone")
            scripts = scratch / "scripts"
            scripts.mkdir()
            shutil.copy(SCRIPT, scripts / "deploy-kit.sh")
            fakes = scratch / "bin"
            fakes.mkdir()
            chezmoi = fakes / "chezmoi"
            chezmoi.write_text(FAKE_CHEZMOI)
            chezmoi.chmod(0o755)
            injection = {}
            if fail.startswith("pwd:"):
                env_file = scratch / "bash_env"
                env_file.write_text(FAKE_PWD_ENV)
                injection = {"BASH_ENV": str(env_file), "FAIL_PWD": os.path.realpath(home / fail[4:])}
            status_lines = [row[:3] + str(home / row[3:]) for row in status_rows]
            if managed is None:
                managed = [row[3:] for row in status_rows] + [".zshrc", ".codex/config.toml"]
            managed_file = scratch / "managed"
            managed_file.write_text("".join(str(home / name) + "\n" for name in managed))
            after = {}
            if managed_after is not None:
                managed_after_file = scratch / "managed_after"
                managed_after_file.write_text("".join(str(home / name) + "\n" for name in managed_after))
                after = {"MANAGED_AFTER": str(managed_after_file)}
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
                    "FAIL_NTH": str(fail_nth),
                    "FAIL_STATUS": str(fail_status),
                }
                | after
                | ({"SWAP_ROOT": str(home / swap_root), "SWAP_TO": str(elsewhere)} if swap_root else {})
                | injection,
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

    @staticmethod
    def apply_call(home, *names):
        return "chezmoi apply --verbose --recursive=false --refresh-externals=never " + " ".join(
            str(home / name) for name in names
        )

    @classmethod
    def verify_calls(cls, home, *names):
        """The post-apply managed re-read, then one verify over the names it still lists."""
        return [
            cls.read_calls(home)[0],
            "chezmoi verify --recursive=false --refresh-externals=never "
            + " ".join(str(home / name) for name in names),
        ]

    def test_only_the_pending_kit_targets_are_applied_by_name_then_verified(self):
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
            + [self.apply_call(home, ".local/bin/pr-merge.sh", ".agents/omp/profiles/dsh.yml")]
            + self.verify_calls(home, ".local/bin/pr-merge.sh", ".agents/omp/profiles/dsh.yml"),
            calls,
        )
        self.assertIn("deploy-kit: managed kit targets: 3\n", result.stdout)
        self.assertIn("deploy-kit: pending: 2\n", result.stdout)
        self.assertIn(f"deploy-kit: applied: 2\n  {lever}\n  {profile}\n", result.stdout)
        self.assertNotIn(".codex", "".join(call for call in calls if call.startswith("chezmoi apply")))

    def test_a_pending_name_outside_the_managed_kit_set_refuses_by_name_and_applies_nothing(self):
        rows = [" M .local/bin/pr-merge.sh", " A .agents/skills/new/SKILL.md", " M .dsh/profiles/thak/package.json"]
        managed = [".local/bin/pr-merge.sh", ".dsh/profiles/thak/package.json", ".zshrc"]
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                result, calls, home = self.run_deploy(rows, managed=managed, dry_run=dry_run)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("deploy-kit: refused: 1 pending names are not in the managed kit set", result.stderr)
                self.assertIn(f"   A {home / '.agents/skills/new/SKILL.md'}\n", result.stderr)
                self.assertIn("nothing applied", result.stderr)
                self.assertNotIn("deploy-kit: applied:", result.stdout)
                self.assertEqual(self.read_calls(home), calls)

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

    def test_a_failing_chezmoi_read_refuses_before_anything_is_applied(self):
        rows = [" M .local/bin/pr-merge.sh"]
        expected = {
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

    def test_a_failing_physical_path_read_of_home_or_a_root_refuses_before_any_chezmoi_call(self):
        rows = [" M .local/bin/pr-merge.sh", " M .agents/permgate-policy.yaml", " M .dsh/profiles/thak/package.json"]
        for directory in (".",) + KIT_ROOTS:
            with self.subTest(directory=directory):
                result, calls, home = self.run_deploy(rows, fail=f"pwd:{directory}")
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("pwd -P", result.stderr)
                self.assertIn("nothing applied", result.stderr)
                if directory == ".":
                    self.assertIn(f"the physical path of HOME {home} could not be read", result.stderr)
                else:
                    self.assertIn(
                        f"the physical path of the kit root {home / directory} could not be read", result.stderr
                    )
                self.assertEqual([], calls)
        # The injection is the one named directory: the same BASH_ENV with a directory the script never enters
        # leaves the run untouched, so a passing case above is the script's refusal and not a broken fixture.
        result, calls, home = self.run_deploy(rows, fail="pwd:elsewhere", dry_run=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(self.read_calls(home), calls)

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
        self.assertIn("deploy-kit: dry run; nothing applied.\n", result.stdout)

    def test_a_failed_apply_or_verify_exits_1_with_the_producer_named_and_no_applied_list(self):
        rows = [" M .local/bin/pr-merge.sh"]
        for fail, message, call_count in (("apply", "chezmoi apply failed", 3), ("verify", "chezmoi verify finds", 5)):
            with self.subTest(fail=fail):
                result, calls, home = self.run_deploy(rows, fail=fail)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertNotIn("deploy-kit: applied:", result.stdout)
                self.assertEqual(call_count, len(calls), calls)
                self.assertIn(f"--refresh-externals=never {home / '.local/bin/pr-merge.sh'}", calls[2])

    def test_a_second_run_with_nothing_pending_applies_nothing_and_exits_0(self):
        rows = ["   .local/bin/pr-merge.sh", " M .codex/config.toml"]
        result, calls, home = self.run_deploy(rows)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(self.read_calls(home), calls)
        self.assertIn("deploy-kit: pending: 0\n", result.stdout)
        self.assertIn("deploy-kit: applied: 0\n", result.stdout)

    def test_the_script_has_no_here_string_and_never_names_the_asset_updater(self):
        text = SCRIPT.read_text()
        self.assertNotIn("<<<", text)
        self.assertNotIn("<(", text)
        self.assertNotIn("update-agent-assets", text)

    def test_a_retired_target_is_verified_by_its_absence_and_never_passed_to_verify(self):
        rows = [" D .agents/skills/understand", " M .local/bin/pr-merge.sh"]
        result, calls, home = self.run_deploy(rows)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            self.read_calls(home)
            + [self.apply_call(home, ".agents/skills/understand", ".local/bin/pr-merge.sh")]
            + self.verify_calls(home, ".local/bin/pr-merge.sh"),
            calls,
        )
        self.assertIn("deploy-kit: applied: 2\n", result.stdout)
        # Nothing but retirements: no managed re-read and no verify call at all.
        result, calls, home = self.run_deploy([" D .agents/skills/understand", " D .dsh/profiles/old/package.json"])
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            self.read_calls(home)
            + [self.apply_call(home, ".agents/skills/understand", ".dsh/profiles/old/package.json")],
            calls,
        )
        self.assertIn("deploy-kit: applied: 2\n", result.stdout)

    def test_a_retired_target_still_present_after_the_apply_refuses_before_any_verify(self):
        rows = [" D .agents/skills/understand", " M .local/bin/pr-merge.sh"]
        for kind in ("file", "dangling-link"):
            with self.subTest(kind=kind):
                result, calls, home = self.run_deploy(rows, present={".agents/skills/understand": kind})
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("deploy-kit: 1 retired targets are still present after the apply", result.stderr)
                self.assertIn(f"  {home / '.agents/skills/understand'}\n", result.stderr)
                self.assertNotIn("deploy-kit: applied:", result.stdout)
                self.assertEqual(
                    self.read_calls(home)
                    + [self.apply_call(home, ".agents/skills/understand", ".local/bin/pr-merge.sh")],
                    calls,
                )

    def test_a_root_swapped_for_a_link_between_the_reads_refuses_naming_the_root(self):
        rows = [" M .local/bin/pr-merge.sh", " M .agents/permgate-policy.yaml", " M .dsh/profiles/thak/package.json"]
        for name in KIT_ROOTS:
            for dry_run in (False, True):
                with self.subTest(root=name, dry_run=dry_run):
                    result, calls, home = self.run_deploy(rows, swap_root=name, dry_run=dry_run)
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn(f"the kit root {home / name} is a symbolic link", result.stderr)
                    self.assertIn(
                        f"the kit root {home / name} changed between the managed read and the status read",
                        result.stderr,
                    )
                    self.assertIn("nothing applied", result.stderr)
                    self.assertNotIn("deploy-kit: pending:", result.stdout)
                    self.assertEqual(self.read_calls(home), calls)

    def test_a_status_row_on_a_root_itself_refuses_unless_it_is_a_plain_pending_change(self):
        for row in ("MM .agents", "DA .dsh", " D .local/bin"):
            for dry_run in (False, True):
                with self.subTest(row=row, dry_run=dry_run):
                    result, calls, home = self.run_deploy([row, " M .local/bin/pr-merge.sh"], dry_run=dry_run)
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn("deploy-kit: refused: 1 kit roots are not what chezmoi last wrote", result.stderr)
                    self.assertIn(f"  {row[:3]}{home / row[3:]}\n", result.stderr)
                    self.assertIn("nothing applied", result.stderr)
                    self.assertEqual(self.read_calls(home), calls)
        # A plain pending change to the root's directory entry is applied as that entry alone.
        result, calls, home = self.run_deploy([" M .agents", " M .local/bin/pr-merge.sh"])
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            self.read_calls(home)
            + [self.apply_call(home, ".agents", ".local/bin/pr-merge.sh")]
            + self.verify_calls(home, ".agents", ".local/bin/pr-merge.sh"),
            calls,
        )

    def test_apply_and_verify_run_without_recursion_so_a_pending_directory_is_applied_alone(self):
        managed = [".agents/skills", ".agents/skills/old/SKILL.md", ".zshrc"]
        result, calls, home = self.run_deploy([" M .agents/skills"], managed=managed)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            self.read_calls(home)
            + [self.apply_call(home, ".agents/skills")]
            + self.verify_calls(home, ".agents/skills"),
            calls,
        )
        for call in calls:
            if call.startswith(("chezmoi apply", "chezmoi verify")):
                self.assertIn(" --recursive=false ", call)
                self.assertTrue(call.endswith(" " + str(home / ".agents/skills")), call)
                self.assertNotIn("SKILL.md", call)

    def test_an_applied_target_the_managed_re_read_no_longer_lists_refuses_before_verify(self):
        rows = [" M .local/bin/pr-merge.sh", " M .agents/permgate-policy.yaml"]
        result, calls, home = self.run_deploy(rows, managed_after=[".agents/permgate-policy.yaml", ".zshrc"])
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("deploy-kit: 1 applied targets are no longer in the managed kit set", result.stderr)
        self.assertIn(f"  {home / '.local/bin/pr-merge.sh'}\n", result.stderr)
        self.assertNotIn("deploy-kit: applied:", result.stdout)
        self.assertEqual(
            self.read_calls(home)
            + [self.apply_call(home, ".local/bin/pr-merge.sh", ".agents/permgate-policy.yaml")]
            + self.read_calls(home)[:1],
            calls,
        )

    def test_a_failing_managed_re_read_after_the_apply_refuses_before_verify(self):
        rows = [" M .local/bin/pr-merge.sh"]
        result, calls, home = self.run_deploy(rows, fail="managed", fail_nth=2, fail_status=3)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(
            "deploy-kit: chezmoi managed failed after the apply; the applied targets are unverified", result.stderr
        )
        self.assertNotIn("deploy-kit: applied:", result.stdout)
        self.assertEqual(
            self.read_calls(home) + [self.apply_call(home, ".local/bin/pr-merge.sh")] + self.read_calls(home)[:1], calls
        )


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
