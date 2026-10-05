from __future__ import annotations

import concurrent.futures
import shutil
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401 - bootstrap the vendored runtime import path
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

    def test_nested_cwd_uses_enclosing_opt_in_but_stops_at_gitfile(self) -> None:
        import os
        from unittest.mock import patch
        from contextdb.paths import resolve_project_root

        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {}, clear=True):
            root = Path(temp).resolve()
            (root / ".git").mkdir()
            first = project_paths(explicit=root)
            child = root / "src" / "module"
            child.mkdir(parents=True)
            self.assertEqual(first.project_id, project_paths({"cwd": str(child)}).project_id)
            self.assertFalse((child / ".claude").exists())
            self.assertEqual(child, resolve_project_root(explicit=child))
            (root / "src" / ".git").write_text("gitdir: /irrelevant\n")
            self.assertEqual(child, resolve_project_root({"cwd": str(child)}))

    def test_concurrent_first_run_uses_one_identity(self) -> None:
        with tempfile.TemporaryDirectory(prefix="contextdb-race-") as temp:
            root = Path(temp) / "project"
            with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
                ids = list(pool.map(lambda _: project_paths(explicit=root).project_id, range(64)))
            self.assertEqual(1, len(set(ids)))


class StorageDirectorySafetyTests(unittest.TestCase):
    def test_storage_tree_refuses_existing_symlinks(self) -> None:
        for relative in ("state", "spool", "spool/incoming", "spool/quarantine", "health"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory(prefix="contextdb-link-") as temp:
                root = Path(temp) / "project"
                base = root / ".claude/contextdb"
                target = base / relative
                target.parent.mkdir(parents=True)
                outside = Path(temp) / "outside"
                outside.mkdir(mode=0o755)
                target.symlink_to(outside, target_is_directory=True)
                with self.assertRaises((OSError, ValueError)):
                    project_paths(explicit=root)
                self.assertEqual(list(outside.iterdir()), [])
                self.assertEqual(outside.stat().st_mode & 0o777, 0o755)

    def test_existing_claude_directory_keeps_its_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            claude = root / ".claude"
            claude.mkdir(mode=0o750)
            project_paths(explicit=root)
            self.assertEqual(0o750, claude.stat().st_mode & 0o777)
            self.assertEqual(0o700, (claude / "contextdb").stat().st_mode & 0o777)

    def test_failed_construction_closes_all_open_directory_descriptors(self) -> None:
        import os
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            base = root / ".claude/contextdb"
            base.mkdir(parents=True)
            (base / "state").symlink_to(Path(temp))
            descriptors = []
            original_open = os.open

            def track_open(*args, **kwargs):
                fd = original_open(*args, **kwargs)
                descriptors.append(fd)
                return fd

            with patch("os.open", side_effect=track_open), self.assertRaises(OSError):
                project_paths(explicit=root)
            self.assertGreater(len(descriptors), 0)
            for fd in descriptors:
                with self.assertRaises(OSError):
                    os.fstat(fd)

    def test_storage_swap_during_creation_does_not_follow_the_new_symlink(self) -> None:
        import os
        from unittest.mock import patch

        for child in ("state", "spool", "health"):
            with self.subTest(child=child), tempfile.TemporaryDirectory(prefix="contextdb-swap-") as temp:
                root = Path(temp) / "project"
                base = root / ".claude/contextdb"
                base.mkdir(parents=True)
                outside = Path(temp) / "outside"
                outside.mkdir(mode=0o755)
                mkdir = os.mkdir
                swapped = False

                def swap_after_mkdir(path, mode=0o777, *, dir_fd=None):
                    nonlocal swapped
                    mkdir(path, mode, dir_fd=dir_fd)
                    if not swapped and Path(path).name == child:
                        swapped = True
                        os.rename(path, str(path) + ".original", src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
                        os.symlink(str(outside), path, dir_fd=dir_fd)

                with patch("os.mkdir", side_effect=swap_after_mkdir):
                    with self.assertRaises((OSError, ValueError)):
                        project_paths(explicit=root)
                self.assertTrue(swapped)
                self.assertEqual(list(outside.iterdir()), [])
                self.assertEqual(outside.stat().st_mode & 0o777, 0o755)
