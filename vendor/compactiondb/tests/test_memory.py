from __future__ import annotations

import unittest

from contextdb.memory import extract_candidates


def user_prompt(prompt: str) -> dict[str, object]:
    return {"event_type": "user_prompt", "normalized_detail": {"prompt": prompt}}


class MemoryExtractionTests(unittest.TestCase):
    def test_e2e_markers_are_bounded_and_isolated_from_heuristics(self) -> None:
        prompt = (
            "Read README.md and summarize it in one line. Record two memories: "
            "[memory:decision] Use SQLite for all local storage. And also "
            "[memory: constraint — the E2E2 scratch project must never call external networks]."
        )

        candidates = extract_candidates(user_prompt(prompt))

        self.assertEqual(2, len(candidates))
        self.assertTrue(all(candidate.explicit for candidate in candidates))
        self.assertEqual(("decision", "project"), (candidates[0].kind, candidates[0].scope))
        self.assertIn("Use SQLite for all local storage", candidates[0].content)
        self.assertNotIn("[memory", candidates[0].content)
        self.assertNotIn("external networks", candidates[0].content)
        self.assertEqual(("constraint", "project"), (candidates[1].kind, candidates[1].scope))
        self.assertEqual(
            "the E2E2 scratch project must never call external networks",
            candidates[1].content,
        )

    def test_english_heuristic_is_limited_to_matching_sentence(self) -> None:
        candidates = extract_candidates(
            user_prompt("This sentence is ordinary background. Local storage must use SQLite.")
        )

        self.assertEqual(1, len(candidates))
        self.assertFalse(candidates[0].explicit)
        self.assertEqual("constraint", candidates[0].kind)
        self.assertEqual("Local storage must use SQLite.", candidates[0].content)

    def test_mixed_marker_forms_each_yield_a_candidate(self) -> None:
        candidates = extract_candidates(
            user_prompt(
                "[memory:decision] Use SQLite. "
                "[memory: constraint — Never call external networks.] "
                "[記憶:fact] The project is a scratch fixture."
            )
        )

        self.assertEqual(3, len(candidates))
        self.assertTrue(all(candidate.explicit for candidate in candidates))
        self.assertEqual(["decision", "constraint", "fact"], [candidate.kind for candidate in candidates])


if __name__ == "__main__":
    unittest.main()
