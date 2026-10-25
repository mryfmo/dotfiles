#!/usr/bin/env python3
"""The root CLAUDE.md is a Claude-only shim: the AGENTS.md import and the CompactionDB block, nothing else."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BEGIN = "<!-- compactiondb:begin -->"
END = "<!-- compactiondb:end -->"


def outside_compactiondb_block(text: str) -> list[str]:
    """The non-blank lines of `text` outside its one CompactionDB block; raises when the block is not exactly one."""
    if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) > text.index(END):
        raise ValueError("CLAUDE.md must hold exactly one CompactionDB block")
    before, rest = text.split(BEGIN, 1)
    _block, after = rest.split(END, 1)
    return [line for line in (before + after).splitlines() if line.strip()]


class ClaudeMdShimTest(unittest.TestCase):
    def test_root_claude_md_holds_only_the_agents_import_and_the_compactiondb_block(self) -> None:
        """AGENTS.md "Canonical Instructions": repository rules belong in AGENTS.md, never in CLAUDE.md (F158)."""
        text = (ROOT / "CLAUDE.md").read_text()

        self.assertEqual(["@AGENTS.md"], outside_compactiondb_block(text))
        self.assertTrue(text.startswith("@AGENTS.md\n"))

    def test_the_shape_check_refuses_a_rule_outside_the_block_and_a_second_block(self) -> None:
        block = f"{BEGIN}\nrecovery\n{END}\n"
        self.assertEqual(["@AGENTS.md"], outside_compactiondb_block(f"@AGENTS.md\n\n{block}"))
        self.assertEqual(
            ["@AGENTS.md", "- Always run make lint."],
            outside_compactiondb_block(f"@AGENTS.md\n\n{block}\n- Always run make lint.\n"),
        )
        for text in ("@AGENTS.md\n", f"@AGENTS.md\n{block}{block}", f"@AGENTS.md\n{END}\n{BEGIN}\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                outside_compactiondb_block(text)


if __name__ == "__main__":
    unittest.main()
