#!/usr/bin/env python3
"""assets.graphify is a pinned manifest asset that no update step installs; its reason refuses the hosted route."""

from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.unit.test_generate_agent_configs import load_manifest_fixture

ROOT = Path(__file__).resolve().parents[2]
UPDATER = ROOT / "scripts/update-agent-assets.sh"
# Everything `make update` and the bootstrap run: the updater, the Makefile, setup.sh and the install/ scripts.
INSTALL_STEP_FILES = (
    UPDATER,
    ROOT / "Makefile",
    ROOT / "setup.sh",
    *sorted(p for p in (ROOT / "install").rglob("*") if p.is_file()),
)
ENTRY_KEYS = {"source", "upstream", "pin", "verify", "sha256", "note", "reason", "install_path", "installer"}
INSTALL_PATH = "~/.local/share/uv/tools/graphifyy"
# The reason's two sentences: the pre-1.0 cadence that keeps the pin, and the hosted route's refusal.
REASON_PHRASES = ("pre-1.0", "api.graphify.com", "credentials, scope and network review", "decisions row")
# The reviewed values, from the PyPI release JSON of graphifyy read on 2026-11-04: the newest wheel at least
# 72 hours old at that read. The shape test's regexes accept any well-formed value; these pin the exact one.
PIN = "0.9.99"
WHEEL_SHA256 = "be8e68ca7e8d2115599167cff82d4a3afc8c5f312c45f707fa5d1a35cc9fb7a7"


class GraphifyAssetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # The committed manifest through chezmoi's fromYaml, as the generator reads it: `make unit-test` has no PyYAML.
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="graphify-asset-test-"))
        cls.manifest = load_manifest_fixture(cls.temp_dir)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_dir)

    def entry(self) -> dict:
        self.assertIn("graphify", self.manifest["assets"])
        return self.manifest["assets"]["graphify"]

    def test_the_entry_has_the_validators_shape_for_a_pinned_wheel(self) -> None:
        entry = self.entry()
        self.assertEqual(ENTRY_KEYS, set(entry))
        self.assertEqual("github-release", entry["source"])
        self.assertEqual("Graphify-Labs/graphify", entry["upstream"])
        self.assertIsInstance(entry["pin"], str)
        self.assertRegex(entry["pin"], r"^[0-9]+\.[0-9]+\.[0-9]+$")
        self.assertEqual("sha256", entry["verify"])
        self.assertRegex(entry["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(INSTALL_PATH, entry["install_path"])

    def test_the_installer_is_the_explicit_uv_step_at_the_pin(self) -> None:
        entry = self.entry()
        self.assertTrue(
            entry["installer"].startswith(f"uv tool install graphifyy=={entry['pin']}"),
            entry["installer"],
        )

    def test_the_pin_and_digest_are_the_reviewed_values(self) -> None:
        entry = self.entry()
        self.assertEqual(PIN, entry["pin"])
        self.assertEqual(WHEEL_SHA256, entry["sha256"])
        # The installer is the pinned command, then a parenthetical note on who runs it (CHANGE 1 of the brief).
        self.assertEqual(f"uv tool install graphifyy=={PIN}", entry["installer"].split(" (", 1)[0])

    def test_the_reason_names_the_cadence_and_the_hosted_routes_refusal(self) -> None:
        reason = self.entry()["reason"]
        for phrase in REASON_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, reason)

    def test_no_update_step_installs_graphify(self) -> None:
        self.entry()
        for path in INSTALL_STEP_FILES:
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertNotIn("graphify", path.read_text(errors="replace"))

    def test_the_updaters_single_step_dispatch_names_no_graphify_step(self) -> None:
        lines = UPDATER.read_text().splitlines()
        dispatch = [index for index, line in enumerate(lines) if line.strip() == 'case "$#:$1" in']
        self.assertEqual(1, len(dispatch), "one single-step dispatch in main")
        steps = lines[dispatch[0] + 1]
        self.assertRegex(steps, r"^\s*1:[a-z_]+( \| 1:[a-z_]+)*\)$")
        self.assertNotIn("graphify", steps)

    def test_the_manifest_declares_no_mcp_server(self) -> None:
        self.entry()
        self.assertEqual({}, self.manifest["mcp_servers"])

    def test_understand_anything_stays_pinned_beside_the_trial_candidate(self) -> None:
        self.entry()
        plugins = self.manifest["assets"]["claude-plugins"]["plugins"]
        self.assertIn("understand-anything@understand-anything", plugins)
        self.assertTrue(
            re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", plugins["understand-anything@understand-anything"]["pin"])
        )
        self.assertIn("understand-anything-installer", self.manifest["assets"])


if __name__ == "__main__":
    unittest.main()
