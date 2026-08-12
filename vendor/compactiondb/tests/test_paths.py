from __future__ import annotations

import concurrent.futures
import shutil
import tempfile
import unittest
from pathlib import Path

from contextdb.paths import project_paths


class ProjectIdentityTests(unittest.TestCase):
    def test_identity_is_persistent_when_project_directory_moves(self) -> None:
        with tempfile.TemporaryDirectory(prefix="contextdb-id-") as temp:
            original = Path(temp) / "original"
            moved = Path(temp) / "moved"
            first = project_paths(explicit=original)
            first_id = first.project_id
            shutil.move(str(original), str(moved))
            second = project_paths(explicit=moved)
            self.assertEqual(first_id, second.project_id)
            self.assertEqual(first_id, second.project_id_path.read_text(encoding="utf-8").strip())

    def test_concurrent_first_run_uses_one_identity(self) -> None:
        with tempfile.TemporaryDirectory(prefix="contextdb-race-") as temp:
            root = Path(temp) / "project"
            with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
                ids = list(pool.map(lambda _: project_paths(explicit=root).project_id, range(64)))
            self.assertEqual(1, len(set(ids)))
