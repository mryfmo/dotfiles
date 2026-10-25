#!/usr/bin/env python3
"""The pstack skills reach ~/.agents/pstack/skills through the chezmoi external that assets.pstack pins."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import tarfile
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl"
UPDATER = ROOT / "scripts/update-agent-assets.sh"
# `ls harness/pstack/claude-code/skills` at assets.pstack.pin.
# shortcut: a static copy of the pin's listing, refreshed with the pin; chezmoi refuses a collision at apply time either way.
PSTACK_SKILLS_AT_PIN = frozenset(
    """
    architect arena automate-me benchmark-checklist blast-radius bro correct create-formal-verification-skill
    create-verification-skill figure-it-out how in-your-own-words interrogate ketchup maintain-formal-verification-skill
    maintain-verification-skill make-bot-ui no-comments poteto-help poteto-mode principle-attack-the-premise
    principle-boundary-discipline principle-build-the-lever principle-encode-lessons-in-structure
    principle-exhaust-the-design-space principle-experience-first principle-explain-the-number principle-fix-root-causes
    principle-foundational-thinking principle-guard-the-context-window principle-laziness-protocol
    principle-make-operations-idempotent principle-migrate-callers-then-delete-legacy-apis principle-minimize-reader-load
    principle-model-the-domain principle-never-block-on-the-human principle-outcome-oriented-execution
    principle-prove-it-works principle-redesign-from-first-principles principle-separate-before-serializing-shared-state
    principle-sequence-verifiable-units principle-subtract-before-you-add principle-test-behavior-not-implementation
    principle-type-system-discipline recall reflect setup-pstack sharpen show-me-your-work statechart swarm tdd teach
    technical-writing typescript-best-practices unslop why
    """.split()
)


def chezmoi_template(expression: str) -> str:
    result = subprocess.run(
        [
            "chezmoi",
            "execute-template",
            "--source",
            str(ROOT / "home"),
            "--override-data",
            '{"system":"client"}',
            expression,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout


class PstackAssetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.asset = json.loads(
            chezmoi_template('{{ (include "dot_agents/agent-config.yaml" | fromYaml).assets.pstack | toJson }}')
        )
        rendered = chezmoi_template(
            f"{{{{ template {json.dumps(TEMPLATE.relative_to(ROOT / 'home/.chezmoitemplates').as_posix())} . }}}}"
        )
        # The pstack entry closes the file; the rendered text itself is what the scratch source applies.
        cls.rendered_pstack = rendered[rendered.index('".agents/pstack":') :]

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="pstack-asset-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def archive(self, sha: str = "0" * 40) -> tuple[Path, str]:
        """A cursor/plugins source archive: the Claude Code pstack tree, the Cursor tree and a sibling plugin as decoys."""
        tree = self.temp_dir / f"plugins-{sha}"
        files = {
            "harness/pstack/claude-code/skills/poteto-mode/SKILL.md": "---\nname: poteto-mode\ndescription: style\n---\n",
            "harness/pstack/claude-code/skills/principle-fix-root-causes/SKILL.md": (
                "---\nname: principle-fix-root-causes\ndescription: principle\n---\n"
            ),
            "harness/pstack/claude-code/skills/poteto-mode/references/notes.md": "notes\n",
            "harness/pstack/claude-code/docs/harness/claude-code.md": "adapter\n",
            "harness/pstack/claude-code/plugin.json": '{"version": "0.0.0"}\n',
            "pstack/skills/decoy-cursor/SKILL.md": "---\nname: decoy-cursor\ndescription: cursor tree\n---\n",
            "advisor/skills/decoy-advisor/SKILL.md": "---\nname: decoy-advisor\ndescription: other plugin\n---\n",
        }
        for rel, text in files.items():
            path = tree / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        archive = self.temp_dir / "plugins.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(tree, arcname=tree.name)
        return archive, hashlib.sha256(archive.read_bytes()).hexdigest()

    def scratch_source(self, own_skills: dict[str, str]) -> Path:
        archive, digest = self.archive()
        source = self.temp_dir / "source"
        for name, text in own_skills.items():
            skill = source / "dot_agents/skills" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(text)
        externals = self.rendered_pstack.replace(self.asset["sha256"], digest).replace(
            f"https://github.com/cursor/plugins/archive/{self.asset['pin']}.tar.gz", archive.resolve().as_uri()
        )
        (source / ".chezmoiexternal.yaml").write_text(externals)
        return source

    def chezmoi(self, source: Path, destination: Path, *args: str) -> subprocess.CompletedProcess[str]:
        config = self.temp_dir / "config.yaml"
        config.touch()
        return subprocess.run(
            [
                "chezmoi",
                "--source",
                str(source),
                "--destination",
                str(destination),
                "--cache",
                str(self.temp_dir / "cache"),
                "--persistent-state",
                str(self.temp_dir / "state.boltdb"),
                "--config",
                str(config),
                *args,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_the_external_takes_pin_and_sha256_from_the_manifest(self) -> None:
        self.assertRegex(self.asset["pin"], r"^[0-9a-f]{40}$")
        self.assertRegex(self.asset["sha256"], r"^[0-9a-f]{64}$")
        url = f'url: "https://github.com/cursor/plugins/archive/{self.asset["pin"]}.tar.gz"'
        self.assertEqual(1, self.rendered_pstack.count(url), self.rendered_pstack)
        self.assertEqual(1, self.rendered_pstack.count(f'sha256: "{self.asset["sha256"]}"'), self.rendered_pstack)
        self.assertIn("exact: true", self.rendered_pstack)
        # chezmoi extracts every member that matches neither list when both are set (chezmoiexternal-format, rule 5).
        self.assertNotIn("exclude:", self.rendered_pstack)

    def test_the_external_places_the_pinned_skills_and_docs_in_their_own_exact_root(self) -> None:
        source = self.scratch_source({"own-skill": "---\nname: own-skill\ndescription: mine\n---\n"})
        home = self.temp_dir / "home"
        home.mkdir()

        result = self.chezmoi(source, home, "apply", "--force")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            ["own-skill"], sorted(os.listdir(home / ".agents/skills")), "no pstack skill in the shared root"
        )
        self.assertEqual(
            ["poteto-mode", "principle-fix-root-causes"], sorted(os.listdir(home / ".agents/pstack/skills"))
        )
        self.assertEqual("adapter\n", (home / ".agents/pstack/docs/harness/claude-code.md").read_text())
        self.assertEqual("notes\n", (home / ".agents/pstack/skills/poteto-mode/references/notes.md").read_text())
        self.assertEqual(
            ["docs", "skills"], sorted(os.listdir(home / ".agents/pstack")), "plugin.json and the decoy trees stay out"
        )
        again = self.chezmoi(source, home, "apply", "--force", "--verbose")
        self.assertEqual(0, again.returncode, again.stderr)
        self.assertEqual("", again.stdout, "a second apply changes nothing")
        # Exact: a skill the pinned archive does not hold (one upstream dropped) is removed at the next apply.
        (home / ".agents/pstack/skills/dropped-upstream").mkdir()
        (home / ".agents/pstack/skills/dropped-upstream/SKILL.md").write_text("old\n")
        swept = self.chezmoi(source, home, "apply", "--force")
        self.assertEqual(0, swept.returncode, swept.stderr)
        self.assertFalse((home / ".agents/pstack/skills/dropped-upstream").exists())

    def test_pstack_skill_names_stay_disjoint_from_the_declared_skills(self) -> None:
        """A pstack name that skills.audience also declared would be listed twice by omp, namespaced, with a warning."""
        declared = set(
            json.loads(chezmoi_template('{{ (include "dot_agents/agent-config.yaml" | fromYaml).skills | toJson }}'))[
                "audience"
            ]
        )
        source_skills = {path.name for path in (ROOT / "home/dot_agents/skills").iterdir() if path.is_dir()}
        self.assertEqual(57, len(PSTACK_SKILLS_AT_PIN))
        self.assertLessEqual(source_skills, declared)
        self.assertEqual(set(), declared & PSTACK_SKILLS_AT_PIN, f"declared skills: {sorted(declared)}")

    def retire(self, home: Path, prelude: str = "") -> subprocess.CompletedProcess[str]:
        """Run retire_shared_pstack_copies under `home`; `prelude` is shell run after sourcing, to inject a failure."""
        return subprocess.run(
            ["bash", "-c", f"source {UPDATER}; {prelude}\nretire_shared_pstack_copies"],
            cwd=ROOT,
            env={**os.environ, "HOME": str(home)},
            text=True,
            capture_output=True,
            check=False,
        )

    def pstack_home(self, name: str, shared: dict[str, str]) -> Path:
        """A home whose pstack root holds `changed`, `identical` and `zz-last`, and whose ~/.agents/skills holds `shared`."""
        home = self.temp_dir / name
        for skill in ("changed", "identical", "zz-last"):
            (home / ".agents/pstack/skills" / skill).mkdir(parents=True)
            (home / ".agents/pstack/skills" / skill / "SKILL.md").write_text(f"{skill}\n")
        for skill, text in shared.items():
            (home / ".agents/skills" / skill).mkdir(parents=True)
            (home / ".agents/skills" / skill / "SKILL.md").write_text(text)
        return home

    def test_retire_removes_only_identical_copies_the_old_external_left(self) -> None:
        home = self.pstack_home("home", {"identical": "identical\n", "changed": "ours\n", "own": "own\n"})
        result = self.retire(home)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["changed", "own"], sorted(os.listdir(home / ".agents/skills")))
        self.assertIn(f"kept {home / '.agents/skills/changed'}: it differs", result.stderr)
        self.assertEqual(3, len(os.listdir(home / ".agents/pstack/skills")), "the pstack root is never touched")

        bare = self.temp_dir / "bare-home"
        (bare / ".agents/skills/identical").mkdir(parents=True)
        self.assertEqual(0, self.retire(bare).returncode)
        self.assertTrue((bare / ".agents/skills/identical").is_dir(), "without the pstack root nothing is touched")

    def test_retire_refuses_before_removing_anything(self) -> None:
        """A comparison failure or a symlink anywhere on the path to a removal stops the step with nothing deleted."""
        home = self.pstack_home("unreadable", {"identical": "identical\n", "zz-last": "zz-last\n"})
        unreadable = home / ".agents/skills/zz-last/SKILL.md"
        unreadable.chmod(0)
        try:
            failed = self.retire(home)
        finally:
            unreadable.chmod(0o644)
        self.assertEqual(1, failed.returncode, failed.stdout + failed.stderr)
        self.assertIn(f"cannot compare {home / '.agents/skills/zz-last'}", failed.stderr)
        self.assertTrue((home / ".agents/skills/identical").is_dir(), "an identical pair checked earlier stays")

        home = self.pstack_home("linked-child", {"identical": "identical\n"})
        (home / "elsewhere/zz-last").mkdir(parents=True)
        (home / "elsewhere/zz-last/SKILL.md").write_text("zz-last\n")
        (home / ".agents/skills/zz-last").symlink_to(home / "elsewhere/zz-last")
        failed = self.retire(home)
        self.assertEqual(1, failed.returncode, failed.stdout + failed.stderr)
        self.assertIn(f"{home / '.agents/skills/zz-last'} is a symlink", failed.stderr)
        self.assertTrue((home / ".agents/skills/identical").is_dir())
        self.assertTrue((home / "elsewhere/zz-last/SKILL.md").is_file())

        # A symlinked ~/.agents/skills root, and a symlinked ~/.agents: rm -r would delete inside the referent.
        for link in (".agents/skills", ".agents"):
            with self.subTest(link=link):
                label = link.replace("/", "-")
                home = self.pstack_home(f"linked{label}", {})
                referent = self.temp_dir / f"referent{label}"
                if link == ".agents":
                    shutil.move(home / ".agents", referent)
                    copy = referent / "skills/identical"
                else:
                    copy = referent / "identical"
                copy.mkdir(parents=True)
                (copy / "SKILL.md").write_text("identical\n")
                (home / link).symlink_to(referent)
                failed = self.retire(home)
                self.assertEqual(1, failed.returncode, failed.stdout + failed.stderr)
                self.assertIn(f"{home / link} is a symlink", failed.stderr)
                self.assertTrue(copy.is_dir(), "nothing in the referent is removed")

    def test_retire_refuses_when_a_physical_path_cannot_be_read_or_differs(self) -> None:
        """The pwd -P reads that gate removal: a failure or an unexpected answer exits 1 with nothing deleted."""
        shared = {"identical": "identical\n", "zz-last": "zz-last\n"}
        # Each prelude overrides a builtin the gate's command substitutions call, for one path only.
        cases = {
            "home unreadable": (
                'pwd() { case "$PWD" in */.agents/*) builtin pwd "$@" ;; *) return 1 ;; esac; }',
                "cannot resolve the physical path of",
            ),
            "skill unreadable": (
                'pwd() { case "$PWD" in */zz-last) return 1 ;; *) builtin pwd "$@" ;; esac; }',
                "cannot resolve the physical path of",
            ),
            "cd fails": (
                'cd() { case "$1$2$3" in *zz-last) return 1 ;; *) builtin cd "$@" ;; esac; }',
                "cannot resolve the physical path of",
            ),
            "skill resolves elsewhere": (
                'pwd() { case "$PWD" in */zz-last) printf "/elsewhere/zz-last\\n" ;; *) builtin pwd "$@" ;; esac; }',
                "resolves to /elsewhere/zz-last",
            ),
        }
        for label, (prelude, message) in cases.items():
            with self.subTest(case=label):
                home = self.pstack_home(f"physical-{label.replace(' ', '-')}", shared)
                failed = self.retire(home, prelude)
                self.assertEqual(1, failed.returncode, failed.stdout + failed.stderr)
                self.assertIn(message, failed.stderr)
                self.assertEqual(
                    ["identical", "zz-last"], sorted(os.listdir(home / ".agents/skills")), "nothing removed"
                )
        # The same harness without an injected failure removes both copies, so each case above failed at its gate.
        home = self.pstack_home("physical-control", shared)
        self.assertEqual(0, self.retire(home).returncode)
        self.assertEqual([], os.listdir(home / ".agents/skills"))

    def retire_marketplace(self, home: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "-c", f"source {UPDATER}; retire_marketplace_dev_workflows"],
            cwd=ROOT,
            env={**os.environ, "HOME": str(home)},
            text=True,
            capture_output=True,
            check=False,
        )

    def test_the_retired_marketplace_entry_leaves_an_existing_host_marketplace(self) -> None:
        """U87 F127: chezmoi never rewrites the create_ seed, so make update drops exactly the retired entry."""
        home = self.temp_dir / "existing-host"
        marketplace = home / ".agents/plugins/marketplace.json"
        marketplace.parent.mkdir(parents=True)
        crit = {"name": "crit", "source": {"path": "./.codex/plugins/crit", "source": "local"}}
        mine = {"name": "mine", "source": {"path": "./plugins/mine", "source": "local"}}
        retired = {
            "name": "mryfmo-dev-workflows",
            "source": {"path": "./plugins/mryfmo-dev-workflows", "source": "local"},
        }
        marketplace.write_text(json.dumps({"name": "m", "plugins": [retired, crit, mine]}, indent=2) + "\n")
        marketplace.chmod(0o600)

        first = self.retire_marketplace(home)
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual({"name": "m", "plugins": [crit, mine]}, json.loads(marketplace.read_text()))
        self.assertEqual(0o600, stat.S_IMODE(marketplace.stat().st_mode))
        before = marketplace.read_bytes()
        again = self.retire_marketplace(home)
        self.assertEqual((0, "", ""), (again.returncode, again.stdout, again.stderr), "a second run changes nothing")
        self.assertEqual(before, marketplace.read_bytes())

        # Same name, another source: not ours, kept and named.
        other = {"name": "mryfmo-dev-workflows", "source": {"path": "./elsewhere", "source": "local"}}
        marketplace.write_text(json.dumps({"name": "m", "plugins": [other]}) + "\n")
        kept = self.retire_marketplace(home)
        self.assertEqual(0, kept.returncode, kept.stderr)
        self.assertIn("kept mryfmo-dev-workflows", kept.stderr)
        self.assertEqual([other], json.loads(marketplace.read_text())["plugins"])

        for broken in ('{"plugins": [], "plugins": []}', '{"plugins": [NaN]}', '{"plugins": [', '{"plugins": {}}'):
            with self.subTest(broken=broken):
                marketplace.write_text(broken)
                failed = self.retire_marketplace(home)
                self.assertNotEqual(0, failed.returncode)
                self.assertIn("left unchanged", failed.stderr)
                self.assertEqual(broken, marketplace.read_text())

        # Numbers: an exact int survives the rewrite; one a float cannot hold, either way, refuses with the file kept.
        big = {"name": "big", "weight": 123456789012345678901234567890, "ratio": 0.25}
        marketplace.write_text(json.dumps({"name": "m", "plugins": [retired, big]}) + "\n")
        exact = self.retire_marketplace(home)
        self.assertEqual(0, exact.returncode, exact.stderr)
        self.assertEqual([big], json.loads(marketplace.read_text())["plugins"])
        self.assertIn("123456789012345678901234567890", marketplace.read_text())
        for number in ("1e400", "-1e400", "1e-400"):
            with self.subTest(number=number):
                lossy = (
                    '{"name": "m", "plugins": [{"name": "mryfmo-dev-workflows", "source": {"path": '
                    f'"./plugins/mryfmo-dev-workflows", "source": "local"}}}}, {{"name": "x", "n": {number}}}]}}\n'
                )
                marketplace.write_text(lossy)
                failed = self.retire_marketplace(home)
                self.assertEqual(1, failed.returncode, failed.stdout + failed.stderr)
                self.assertIn("left unchanged", failed.stderr)
                self.assertEqual(lossy, marketplace.read_text())
        self.assertEqual(0, self.retire_marketplace(self.temp_dir / "fresh-host").returncode, "no marketplace yet")

    def check_pstack(self, home: Path, omp_listing: str | None) -> subprocess.CompletedProcess[str]:
        bin_dir = self.temp_dir / "bin"
        bin_dir.mkdir(exist_ok=True)
        omp = bin_dir / "omp"
        omp.unlink(missing_ok=True)
        if omp_listing is not None:
            omp.write_text(
                textwrap.dedent(
                    f"""\
                    #!/bin/bash
                    case "$1" in
                    --version) printf 'omp/0.0.0-test\\n' ;;
                    *) printf '%s\\n' {json.dumps(omp_listing)} ;;
                    esac
                    """
                )
            )
            omp.chmod(omp.stat().st_mode | stat.S_IXUSR)
        jq = shutil.which("jq")
        self.assertIsNotNone(jq, "jq is required for check_pstack tests")
        return subprocess.run(
            ["bash", "-c", f"source {UPDATER}; check_pstack"],
            cwd=ROOT,
            env={**os.environ, "HOME": str(home), "PATH": f"{bin_dir}:{Path(jq).parent}:/usr/bin:/bin"},
            text=True,
            capture_output=True,
            check=False,
        )

    def test_check_pstack_reports_the_missing_file_the_absent_skill_and_the_listed_skill(self) -> None:
        home = self.temp_dir / "home"
        (home / ".agents/pstack/skills/poteto-mode").mkdir(parents=True)
        (home / ".agents/pstack/skills/poteto-mode/SKILL.md").write_text("---\nname: poteto-mode\n---\n")
        listed = (
            '{"skills":[{"name":"poteto-mode","hide":true,"warnings":[]},{"name":"unslop","hide":true}],"warnings":[]}'
        )

        missing = self.check_pstack(home, listed)
        self.assertEqual(1, missing.returncode)
        self.assertIn(f"{home / '.agents/pstack/docs/harness/claude-code.md'} is missing", missing.stderr)

        (home / ".agents/pstack/docs/harness").mkdir(parents=True)
        (home / ".agents/pstack/docs/harness/claude-code.md").write_text("adapter\n")
        absent = self.check_pstack(home, '{"skills":[{"name":"unslop","hide":true}],"warnings":[]}')
        self.assertEqual(1, absent.returncode)
        self.assertIn("omp skill list does not name poteto-mode", absent.stderr)
        self.assertIn('"unslop"', absent.stderr, "the listing is printed above the verdict")

        present = self.check_pstack(home, listed)
        self.assertEqual(0, present.returncode, present.stdout + present.stderr)
        self.assertEqual(
            "pstack skills reach omp/0.0.0-test: 2 skills listed, poteto-mode among them.\n", present.stdout
        )

        no_omp = self.check_pstack(home, None)
        self.assertEqual(0, no_omp.returncode, no_omp.stdout + no_omp.stderr)
        self.assertIn("omp is not installed", no_omp.stdout)


if __name__ == "__main__":
    unittest.main()
