"""The nine knowledge-work skills (regime-cutover U148) against their recorded upstream text.

Each `home/dot_agents/skills/kwp-<name>/SKILL.md` is the anthropics/knowledge-work-plugins file at one recorded commit
with an exact list of line edits: the name carries the `kwp-` prefix, the Claude Code `argument-hint` field becomes the
usage line of the body, the license and the provenance land in the frontmatter, the connector placeholders Codex and
omp never expand become plain prose, and every reference to a skill by its upstream name (the title, the usage line,
the mode examples, a cross-skill pointer) names the installed `kwp-<name>` or says the skill is not part of this set.
The fixtures under `tests/fixtures/kwp-upstream` are the upstream bytes, pinned by their sha256; the copies are read as
bytes with no newline translation, so a copy that differs from the fixture by any other byte, a line ending included,
fails under the skill's own test name with a unified diff, and a fixture that drifts fails by path. The manifest gives
the nine to every skill consumer, and one skills root serves them. The unit run has no PyYAML of its own, so the
one-root test loads the manifest through a `uv run --offline --with pyyaml` subprocess when the import is missing; a
failed load is a failure, never a pass, and a producer that exits non-zero is refused whatever it prints.
"""

import difflib
import hashlib
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
COPIES = ROOT / "home/dot_agents/skills"
FIXTURES = ROOT / "tests/fixtures/kwp-upstream"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
COMMIT = "2574e29377c7173d0cecffef29a6ecbd7f8ccb5d"
REPOSITORY = "https://github.com/anthropics/knowledge-work-plugins"
LICENSE_SHA256 = "a6946284993aeec75c7d75906064b66210c46051e562077efb30eb6dcfe72e26"
CONSUMERS = "[claude, codex, omp, omp-orchestrator, omp-worker]"

# (plugin, name, argument-hint value or None, sha256 of the upstream SKILL.md at COMMIT).
SKILLS = (
    (
        "engineering",
        "architecture",
        "<decision or system to design>",
        "de7db3170a3ae1a894c70ef6cb555fe15618ed9b9674d20895eda3d2a0a5f9a2",
    ),
    (
        "engineering",
        "deploy-checklist",
        "[service or release name]",
        "85ca53dc471970e3e12c36ec814ebf5f6cb9419016c55adb05ff34789bae3be9",
    ),
    (
        "engineering",
        "incident-response",
        "<incident description or alert>",
        "9eaa7a974c90395ac7116e82710f74546f38e69f735d78f684ee13fd79646e9a",
    ),
    ("engineering", "tech-debt", None, "ed3b4b1450c0fd9b8dad17313b5a4fafd8e6947d380b79b36a2e8259f3b1df0f"),
    ("engineering", "testing-strategy", None, "5c5e95830754bbdd838213fa05fc8f07523f591fd558fd3c86031ffd479f7a9e"),
    (
        "operations",
        "change-request",
        "<change description>",
        "b1ee71cc1fecb22c7d27e2e00171f5d62fb54c405095b51098dacfea0447d8d7",
    ),
    ("operations", "risk-assessment", None, "82e29810a762c396a56f92bbd5c5afd252f7a07c6be69a246c28f7b82c4086d9"),
    (
        "operations",
        "runbook",
        "<process or task name>",
        "c5c3eaa4c22fff96ec7239ce67eb3e100661b20a2818749e2f7ee21787233185",
    ),
    (
        "operations",
        "status-report",
        "[weekly | monthly | quarterly] [project or team]",
        "8c3a21075294a5c5b7a1a7930613e53f0afbdbc12cf9e05d4bd08e6950c0a0d9",
    ),
)
NAMES = tuple(row[1] for row in SKILLS)

# The body edits, as whole lines. The title and usage pairs come from the row; the connectors pair is literal; the
# placeholder pairs come from each `~~<kind>` line the fixture holds; the installed-name pairs below are per skill.
# Anything else in a copy that differs from upstream is drift.
CONNECTORS_LINE = (
    "> If you see unfamiliar placeholders or need to check which tools are connected, "
    "see [CONNECTORS.md](../../CONNECTORS.md)."
)
CONNECTORS_REPLACEMENT = (
    '> The "If Connectors Available" section below names kinds of tools; use the ones available in this session.'
)
PLACEHOLDER_LINE = re.compile(r"^If \*\*~~(?P<kind>.+)\*\* is connected:$")
PLACEHOLDER_REPLACEMENT = "If {kind} tools are available in this session:"
FORBIDDEN_MARKS = ("argument-hint", "~~", "$ARGUMENTS", "@$1", "CONNECTORS.md")

# Round 2 (U148b): the cross-skill references and the mode examples name the installed skill, not the upstream one; a
# pointer to an upstream skill outside the nine says so in the sentence's own voice. Whole lines, before and after.
INSTALLED_NAME_EDITS = {
    "architecture": (
        (
            (
                "See the **system-design** skill for detailed frameworks on requirements gathering, scalability "
                "analysis, and trade-off evaluation."
            ),
            (
                "The upstream **system-design** skill, which is not part of this set, holds detailed frameworks on "
                "requirements gathering, scalability analysis, and trade-off evaluation."
            ),
        ),
    ),
    "incident-response": (
        (
            "/incident-response new [description]     # Start a new incident",
            "kwp-incident-response new [description]     # Start a new incident",
        ),
        (
            "/incident-response update [status]       # Post a status update",
            "kwp-incident-response update [status]       # Post a status update",
        ),
        (
            "/incident-response postmortem            # Generate postmortem from incident data",
            "kwp-incident-response postmortem            # Generate postmortem from incident data",
        ),
    ),
    "status-report": (
        (
            (
                "Generate a polished status report for leadership or stakeholders. See the **risk-assessment** skill "
                "for risk matrix frameworks and severity definitions."
            ),
            (
                "Generate a polished status report for leadership or stakeholders. See the **kwp-risk-assessment** "
                "skill for risk matrix frameworks and severity definitions."
            ),
        ),
    ),
}

PYYAML_LOADER = """
import json, sys, yaml
manifest = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
assets = manifest.get("assets") or {}
print(json.dumps({
    "skills_directories": (manifest.get("omp") or {}).get("skills_directories"),
    "install_paths": {key: value.get("install_path") for key, value in assets.items() if isinstance(value, dict)},
}))
"""


def fixture_path(plugin: str, name: str) -> Path:
    return FIXTURES / plugin / "skills" / name / "SKILL.md"


def copy_path(name: str) -> Path:
    return COPIES / f"kwp-{name}" / "SKILL.md"


def body_edits(name: str, hint, fixture_lines: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    if hint is not None:
        pairs += [
            (f"# /{name}", f"# kwp-{name}"),
            (CONNECTORS_LINE, CONNECTORS_REPLACEMENT),
            (f"/{name} $ARGUMENTS", f"kwp-{name} {hint}"),
        ]
        for line in fixture_lines:
            match = PLACEHOLDER_LINE.match(line)
            if match:
                pairs.append((line, PLACEHOLDER_REPLACEMENT.format(kind=match.group("kind"))))
    pairs += INSTALLED_NAME_EDITS.get(name, ())
    return pairs


def load_manifest_facts_through_uv() -> dict:
    """The manifest facts from one `uv run --offline --with pyyaml` subprocess; a non-zero exit raises, whatever it printed."""
    completed = subprocess.run(
        ["uv", "run", "--offline", "--with", "pyyaml", "python", "-c", PYYAML_LOADER, str(MANIFEST)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"manifest loader exited {completed.returncode}: {completed.stderr.strip()}")
    return json.loads(completed.stdout)


def load_manifest_facts() -> tuple[dict, str]:
    """omp.skills_directories and every assets.<id>.install_path, with the loader's status for the caller to judge."""
    try:
        import yaml
    except ModuleNotFoundError:
        yaml = None
    if yaml is not None:
        manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        assets = manifest.get("assets") or {}
        facts = {
            "skills_directories": (manifest.get("omp") or {}).get("skills_directories"),
            "install_paths": {k: v.get("install_path") for k, v in assets.items() if isinstance(v, dict)},
        }
        return facts, "yaml import"
    return load_manifest_facts_through_uv(), "uv run --offline --with pyyaml"


class KnowledgeWorkSkillsDrift(unittest.TestCase):
    maxDiff = None

    def expected_copy(self, plugin: str, name: str, hint, fixture_text: str) -> str:
        lines = fixture_text.split("\n")
        self.assertEqual(lines[0], "---", f"{name}: the upstream file does not open with a frontmatter fence")
        closers = [i for i in range(1, len(lines)) if lines[i] == "---"]
        self.assertTrue(closers, f"{name}: the upstream frontmatter never closes")
        close = closers[0]
        front, body = lines[1:close], lines[close + 1 :]
        self.assertEqual(front.count(f"name: {name}"), 1, f"{name}: the upstream name line is not where expected")
        front[front.index(f"name: {name}")] = f"name: kwp-{name}"
        if hint is not None:
            hint_line = f'argument-hint: "{hint}"'
            self.assertEqual(front.count(hint_line), 1, f"{name}: the upstream argument-hint line is not {hint_line!r}")
            front.remove(hint_line)
        self.assertFalse([line for line in front if line.startswith("argument-hint")], f"{name}: another hint line")
        front += [
            "license: Apache-2.0",
            "metadata:",
            f"  upstream: {plugin}/skills/{name}/SKILL.md",
            f"  commit: {COMMIT}",
            f"  repository: {REPOSITORY}",
        ]
        if hint is None:
            for mark in ("$ARGUMENTS", "~~", "CONNECTORS.md"):
                self.assertFalse([line for line in body if mark in line], f"{name}: upstream holds {mark} but no hint")
        for old, new in body_edits(name, hint, body):
            self.assertEqual(body.count(old), 1, f"{name}: the edit {old!r} must fire exactly once")
            body[body.index(old)] = new
        return "\n".join(["---", *front, "---", *body])

    def assert_copy_matches_upstream(self, plugin: str, name: str, hint, sha256: str, copy: Path | None = None) -> None:
        fixture = fixture_path(plugin, name)
        upstream = fixture.read_bytes()
        self.assertEqual(hashlib.sha256(upstream).hexdigest(), sha256, f"{fixture.relative_to(ROOT)} is not upstream")
        expected = self.expected_copy(plugin, name, hint, upstream.decode("utf-8"))
        copy = copy_path(name) if copy is None else copy
        actual = copy.read_bytes().decode("utf-8")
        if actual != expected:
            diff = difflib.unified_diff(
                expected.splitlines(keepends=True),
                actual.splitlines(keepends=True),
                fromfile=f"expected kwp-{name} (upstream at {COMMIT[:8]} with the recorded edits)",
                tofile=str(copy.relative_to(ROOT)) if copy.is_relative_to(ROOT) else str(copy),
            )
            self.fail(f"kwp-{name} drifted from upstream:\n{''.join(diff)}")

    def test_kwp_architecture_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[0])

    def test_kwp_deploy_checklist_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[1])

    def test_kwp_incident_response_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[2])

    def test_kwp_tech_debt_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[3])

    def test_kwp_testing_strategy_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[4])

    def test_kwp_change_request_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[5])

    def test_kwp_risk_assessment_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[6])

    def test_kwp_runbook_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[7])

    def test_kwp_status_report_matches_upstream_at_the_recorded_commit(self):
        self.assert_copy_matches_upstream(*SKILLS[8])

    def test_the_fixtures_are_the_upstream_bytes_at_the_recorded_commit(self):
        for plugin, name, _hint, sha256 in SKILLS:
            fixture = fixture_path(plugin, name)
            with self.subTest(fixture=str(fixture.relative_to(ROOT))):
                self.assertEqual(hashlib.sha256(fixture.read_bytes()).hexdigest(), sha256)
        license_file = FIXTURES / "LICENSE"
        with self.subTest(fixture=str(license_file.relative_to(ROOT))):
            self.assertEqual(hashlib.sha256(license_file.read_bytes()).hexdigest(), LICENSE_SHA256)
        self.assertTrue(
            license_file.read_text(encoding="utf-8").lstrip().startswith("Apache License"),
            "the LICENSE fixture is not the Apache License text",
        )

    def test_no_copy_holds_a_claude_code_substitution_or_a_connector_placeholder(self):
        for plugin, name, _hint, _sha256 in SKILLS:
            text = copy_path(name).read_bytes().decode("utf-8")
            with self.subTest(skill=f"kwp-{name}"):
                for mark in FORBIDDEN_MARKS:
                    self.assertNotIn(mark, text)
                self.assertIn("\nlicense: Apache-2.0\n", text)
                self.assertIn(f"\n  upstream: {plugin}/skills/{name}/SKILL.md\n", text)
                self.assertIn(f"\n  commit: {COMMIT}\n", text)

    def test_a_copy_with_changed_line_endings_fails_the_drift_test(self):
        """The guarantee is byte-exact: a CRLF or bare-CR rewrite of a copy is drift, not another view of the text."""
        plugin, name, hint, sha256 = SKILLS[7]
        expected = self.expected_copy(plugin, name, hint, fixture_path(plugin, name).read_bytes().decode("utf-8"))
        with tempfile.TemporaryDirectory() as scratch:
            for label, newline in (("CRLF", "\r\n"), ("bare CR", "\r")):
                with self.subTest(line_ending=label):
                    scratch_copy = Path(scratch) / f"{label.replace(' ', '-')}-SKILL.md"
                    scratch_copy.write_bytes(expected.replace("\n", newline).encode("utf-8"))
                    with self.assertRaises(AssertionError) as caught:
                        self.assert_copy_matches_upstream(plugin, name, hint, sha256, copy=scratch_copy)
                    self.assertIn(f"kwp-{name} drifted from upstream", str(caught.exception))
            control = Path(scratch) / "LF-SKILL.md"
            control.write_bytes(expected.encode("utf-8"))
            self.assert_copy_matches_upstream(plugin, name, hint, sha256, copy=control)

    def test_the_manifest_loader_refuses_a_failed_producer_that_prints_valid_json(self):
        """A producer's status is read: a `uv` that prints the right JSON and exits non-zero is a failure, not the facts."""
        with tempfile.TemporaryDirectory() as scratch:
            fake_uv = Path(scratch) / "uv"
            fake_uv.write_text(
                '#!/bin/sh\nprintf \'{"skills_directories": ["~/.agents/skills"], "install_paths": {}}\\n\'\nexit 23\n',
                encoding="utf-8",
            )
            fake_uv.chmod(0o755)
            fake_first = {"PATH": f"{scratch}{os.pathsep}{os.environ.get('PATH', '')}"}
            with mock.patch.dict(os.environ, fake_first), self.assertRaises(RuntimeError) as caught:
                load_manifest_facts_through_uv()
        self.assertIn("manifest loader exited 23", str(caught.exception))

    def test_every_kwp_skill_has_the_five_consumer_audience_line(self):
        manifest_lines = MANIFEST.read_text(encoding="utf-8").split("\n")
        for name in NAMES:
            with self.subTest(skill=f"kwp-{name}"):
                self.assertEqual(manifest_lines.count(f"    kwp-{name}: {CONSUMERS}"), 1)
        kwp_lines = [line for line in manifest_lines if re.match(r"^    kwp-[a-z-]+: ", line)]
        self.assertEqual(len(kwp_lines), 9, "the manifest names a kwp- skill the table does not")

    def test_one_root_serves_every_ported_skill(self):
        try:
            facts, route = load_manifest_facts()
        except (RuntimeError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
            self.fail(f"the manifest could not be loaded: {error}")
        self.assertEqual(facts["skills_directories"], ["~/.agents/skills"], f"omp.skills_directories (via {route})")
        for asset, install_path in facts["install_paths"].items():
            with self.subTest(asset=asset):
                if install_path is None:
                    continue
                self.assertIsInstance(install_path, str)
                self.assertNotIn(install_path.rstrip("/"), ("~/.agents/skills", "~/.agents"))
                self.assertNotIn("kwp-", install_path)
        kwp_dirs = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "home").rglob("kwp-*") if p.is_dir())
        expected = sorted(
            [f"home/dot_agents/skills/kwp-{name}" for name in NAMES]
            + [f"home/dot_claude/skills/kwp-{name}" for name in NAMES]
        )
        self.assertEqual(kwp_dirs, expected)
        for name in NAMES:
            with self.subTest(skill=f"kwp-{name}"):
                self.assertEqual(sorted(p.name for p in copy_path(name).parent.iterdir()), ["SKILL.md"])
                link = ROOT / "home/dot_claude/skills" / f"kwp-{name}" / "symlink_SKILL.md.tmpl"
                self.assertEqual(
                    link.read_text(encoding="utf-8").strip(),
                    "{{ .chezmoi.sourceDir }}/dot_agents/skills/kwp-" + name + "/SKILL.md",
                )
