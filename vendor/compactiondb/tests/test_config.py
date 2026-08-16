from __future__ import annotations

import json
import unittest

from contextdb.config import load_config

from tests.support import TempProject


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def load(self, config: dict[str, object]) -> dict[str, object]:
        self.p.paths.config_path.write_text(json.dumps(config), encoding="utf-8")
        return load_config(self.p.paths)

    def test_missing_recovery_budgets_use_defaults(self) -> None:
        config = self.load({"version": 1, "recovery": {"recent_events": 7}})
        self.assertEqual(12000, config["recovery"]["max_chars"])
        self.assertEqual(2000, config["recovery"]["files_budget_chars"])

    def test_explicit_recovery_budgets_override_defaults(self) -> None:
        config = self.load(
            {"version": 1, "recovery": {"max_chars": 16000, "files_budget_chars": 3000}}
        )
        self.assertEqual(16000, config["recovery"]["max_chars"])
        self.assertEqual(3000, config["recovery"]["files_budget_chars"])

    def test_invalid_files_budget_type_matches_sibling_validation(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            r"ContextDB config recovery\.files_budget_chars must be an integer >= 0",
        ):
            self.load({"version": 1, "recovery": {"files_budget_chars": "2000"}})

    def test_unknown_keys_are_preserved(self) -> None:
        config = self.load(
            {"version": 1, "future_section": True, "recovery": {"future_budget": 42}}
        )
        self.assertIs(True, config["future_section"])
        self.assertEqual(42, config["recovery"]["future_budget"])
