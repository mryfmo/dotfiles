import ast
import itertools
import re
import shlex
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "home/dot_codex/rules/default.rules"
REQUIRED_PREFIXES = {
    ("sudo",),
    ("/usr/bin/sudo",),
    ("rm", "-rfv"),
    ("rm", "-vrf"),
    ("chezmoi", "update"),
    ("chezmoi", "init"),
    ("chezmoi", "edit"),
    ("terraform", "destroy"),
    ("kubectl", "delete"),
    ("rm", "-r", "-v", "-f"),
    ("rm", "-v", "-r", "-f"),
    ("make", "setup"),
    ("make", "init"),
    ("rm", "-rf"),
    ("rm", "-fr"),
    ("rm", "-r", "-f"),
    ("rm", "-f", "-r"),
    ("gh", "pr", "merge"),
    ("gh", "api", "-X", "PUT"),
    ("gh", "api", "--method", "PUT"),
    ("gh", "api", "graphql"),
    ("gh", "release"),
    ("npm", "publish"),
    ("uv", "publish"),
    ("terraform", "apply"),
    ("kubectl", "apply"),
    ("chezmoi", "apply"),
    ("make", "update"),
    # make update hands everything after its pull to update-tree, which applies and upgrades the host too.
    ("make", "update-tree"),
    ("make", "apply"),
    ("./setup.sh",),
    ("make", "clean"),
    ("make", "deploy"),
}


def prefix_rules(text: str) -> list[dict[str, object]]:
    """Each prefix_rule(...) call as a dict of its keyword arguments."""
    calls = ast.parse(re.sub(r"(?m)^\s*#.*$", "", text)).body
    rules = []
    for statement in calls:
        call = statement.value
        assert isinstance(call, ast.Call) and call.func.id == "prefix_rule", ast.dump(statement)
        rules.append({keyword.arg: ast.literal_eval(keyword.value) for keyword in call.keywords})
    return rules


def expand(pattern: list[object]) -> set[tuple[str, ...]]:
    """Every token sequence a pattern matches; a list element lists alternatives."""
    choices = [item if isinstance(item, list) else [item] for item in pattern]
    return set(itertools.product(*choices))


class CodexExecpolicyTest(unittest.TestCase):
    def test_rules_are_forbidden_only_and_cover_the_declared_prefixes(self) -> None:
        rules = prefix_rules(RULES.read_text())

        self.assertTrue(rules)
        self.assertEqual({rule["decision"] for rule in rules}, {"forbidden"})
        covered = set().union(*(expand(rule["pattern"]) for rule in rules))
        self.assertLessEqual(REQUIRED_PREFIXES, covered)
        for rule in rules:
            with self.subTest(pattern=rule["pattern"]):
                self.assertTrue(rule["justification"])

    def test_rule_examples_agree_with_their_patterns(self) -> None:
        # Codex checks match/not_match at load time; a wrong example would make it reject the file.
        for rule in prefix_rules(RULES.read_text()):
            prefixes = expand(rule["pattern"])
            for example in rule.get("match", []):
                with self.subTest(pattern=rule["pattern"], match=example):
                    words = tuple(shlex.split(example))
                    self.assertTrue(any(words[: len(prefix)] == prefix for prefix in prefixes))
            for example in rule.get("not_match", []):
                with self.subTest(pattern=rule["pattern"], not_match=example):
                    words = tuple(shlex.split(example))
                    self.assertFalse(any(words[: len(prefix)] == prefix for prefix in prefixes))

    def test_worker_seats_cannot_merge_through_the_api(self) -> None:
        # One GitHub login per machine: denying merges in the seat replaces the account separation.
        covered = set().union(*(expand(rule["pattern"]) for rule in prefix_rules(RULES.read_text())))
        for prefix in (
            ("gh", "pr", "merge"),
            ("gh", "api", "-X", "PUT"),
            ("gh", "api", "--method", "PUT"),
            ("gh", "api", "graphql"),
        ):
            with self.subTest(prefix=prefix):
                self.assertIn(prefix, covered)
        self.assertNotIn(("gh", "api", "repos/o/r/pulls/1/reviews"), covered)


if __name__ == "__main__":
    unittest.main()
