#!/usr/bin/env python3
"""The pstack skills reach ~/.agents/skills through the chezmoi externals that assets.pstack pins."""

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


import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


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
        # The two pstack entries close the file; the rendered text itself is what the scratch source applies.
        cls.rendered_pstack = rendered[rendered.index('".agents/skills":') :]

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

    def test_both_externals_take_pin_and_sha256_from_the_manifest(self) -> None:
        self.assertRegex(self.asset["pin"], r"^[0-9a-f]{40}$")
        self.assertRegex(self.asset["sha256"], r"^[0-9a-f]{64}$")
        url = f'url: "https://github.com/cursor/plugins/archive/{self.asset["pin"]}.tar.gz"'
        self.assertEqual(2, self.rendered_pstack.count(url), self.rendered_pstack)
        self.assertEqual(2, self.rendered_pstack.count(f'sha256: "{self.asset["sha256"]}"'), self.rendered_pstack)
        self.assertEqual(2, self.rendered_pstack.count("stripComponents: 5"))
        self.assertIn('".agents/docs":\n  type: "archive"', self.rendered_pstack)
        self.assertEqual(
            1,
            self.rendered_pstack.count("exact: true"),
            "only ~/.agents/docs is exact; other installers own siblings under ~/.agents/skills",
        )

    def test_externals_place_the_pinned_skills_and_docs_beside_the_source_skills(self) -> None:
        source = self.scratch_source({"own-skill": "---\nname: own-skill\ndescription: mine\n---\n"})
        home = self.temp_dir / "home"
        home.mkdir()

        result = self.chezmoi(source, home, "apply", "--force")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            ["own-skill", "poteto-mode", "principle-fix-root-causes"],
            sorted(os.listdir(home / ".agents/skills")),
        )
        self.assertEqual("adapter\n", (home / ".agents/docs/harness/claude-code.md").read_text())
        self.assertEqual("notes\n", (home / ".agents/skills/poteto-mode/references/notes.md").read_text())
        self.assertEqual(
            "---\nname: own-skill\ndescription: mine\n---\n", (home / ".agents/skills/own-skill/SKILL.md").read_text()
        )
        self.assertEqual(
            ["docs", "skills"], sorted(os.listdir(home / ".agents")), "plugin.json and the decoy trees stay out"
        )
        again = self.chezmoi(source, home, "apply", "--force", "--verbose")
        self.assertEqual(0, again.returncode, again.stderr)
        self.assertEqual("", again.stdout, "a second apply changes nothing")
        managed = self.chezmoi(
            source, home, "managed", "--include=dirs", "--path-style=absolute", str(home / ".agents/skills")
        )
        self.assertIn(str(home / ".agents/skills/poteto-mode"), managed.stdout.splitlines())

    def test_a_pstack_skill_named_like_a_source_skill_is_refused_not_overwritten(self) -> None:
        source = self.scratch_source({"poteto-mode": "---\nname: poteto-mode\ndescription: ours\n---\n"})
        home = self.temp_dir / "home"
        home.mkdir()

        result = self.chezmoi(source, home, "apply", "--force")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("inconsistent state", result.stderr)
        self.assertIn(".agents/skills/poteto-mode/SKILL.md", result.stderr)
        self.assertIn(str(source / "dot_agents/skills/poteto-mode/SKILL.md"), result.stderr, "both sources are named")
        self.assertFalse((home / ".agents").exists(), "nothing is written when the two sets collide")

    def test_pstack_skill_names_stay_disjoint_from_the_source_skills(self) -> None:
        source_skills = {path.name for path in (ROOT / "home/dot_agents/skills").iterdir() if path.is_dir()}
        self.assertEqual(57, len(PSTACK_SKILLS_AT_PIN))
        self.assertEqual(
            set(),
            source_skills & PSTACK_SKILLS_AT_PIN,
            f"a skill under home/dot_agents/skills shares its name with a pstack skill; source skills: {sorted(source_skills)}",
        )

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
        (home / ".agents/skills/poteto-mode").mkdir(parents=True)
        (home / ".agents/skills/poteto-mode/SKILL.md").write_text("---\nname: poteto-mode\n---\n")
        listed = (
            '{"skills":[{"name":"poteto-mode","hide":true,"warnings":[]},{"name":"unslop","hide":true}],"warnings":[]}'
        )

        missing = self.check_pstack(home, listed)
        self.assertEqual(1, missing.returncode)
        self.assertIn(f"{home / '.agents/docs/harness/claude-code.md'} is missing", missing.stderr)

        (home / ".agents/docs/harness").mkdir(parents=True)
        (home / ".agents/docs/harness/claude-code.md").write_text("adapter\n")
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
