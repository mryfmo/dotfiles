"""Exercise brief-check.py (regime-cutover U104) on scratch briefs, as a subprocess under `python -I`."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/orchestrator/brief-check.py"
SKILL = ROOT / "home/dot_agents/skills/hcom-orchestration/SKILL.md"
# The trigger table as the brief fixed it; a later unit that adds a row adds it here too.
TRIGGERS = (
    "shell",
    "tokenize",
    "tokenizer",
    "parse",
    "parser",
    "regex",
    "hook",
    "worktree",
    "config",
    "path",
    "process",
    "signal",
    "supervisor",
    "curl",
    "wget",
    "heredoc",
    "quote",
)
MECHANISMS = ("ast", "parser-module", "allowlist", "remove")
SKILL_SENTENCE = (
    "Run `scripts/orchestrator/brief-check.py briefs/U<n>-<slug>.md` and send no TASK while it exits non-zero; "
    "a brief whose unit judges an open-ended input names the closing mechanism in a `CLOSURE` section "
    "(`ast`, `parser-module`, `allowlist` or `remove`)."
)
CLEAN_GOAL = "The six dead installer functions leave the installers and nothing else changes."


def brief(**bodies):
    """A brief in the grammar: a title, then each named section as its upper-case line and body."""
    text = "# U0 A scratch brief\n\n"
    for name, body in bodies.items():
        text += f"{name}\n{body}\n\n"
    return text


class BriefCheckTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)

    def check(self, *args):
        cmd = [sys.executable, "-I", str(SCRIPT), *args]
        return subprocess.run(cmd, cwd=self.dir, capture_output=True, text=True, timeout=120, check=False)

    def check_text(self, text, name="U0-scratch.md"):
        target = self.dir / name
        target.write_text(text)
        return self.check(str(target))

    def test_each_trigger_term_in_goal_without_closure_exits_1_naming_the_section_and_term(self):
        for term in TRIGGERS:
            with self.subTest(term=term):
                result = self.check_text(brief(GOAL=f"This unit reads the {term} of every seat.", SCOPE="one file"))
                self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
                self.assertIn(f'brief-check: GOAL holds "{term}"', result.stdout)
                self.assertIn("no CLOSURE section", result.stdout)

    def test_a_term_in_change_or_context_fires_and_a_capitalised_or_backticked_term_counts(self):
        for section, body in (
            ("CHANGE", "1. Rewrite the Parser."),
            ("CONTEXT", "- The old `regex` matched three forms."),
            ("GOAL", "A SHELL reader."),
        ):
            with self.subTest(section=section):
                result = self.check_text(brief(**({"GOAL": CLEAN_GOAL} | {section: body})))
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertIn(f"brief-check: {section} holds", result.stdout)

    def test_a_term_inside_scope_or_forbidden_alone_fires_nothing(self):
        for section in ("SCOPE", "FORBIDDEN", "ACCEPTANCE", "VERIFY", "REPORT", "STANDING"):
            with self.subTest(section=section):
                body = "No regex over the brief; one shell file under the path scripts/; no hook, no config edit."
                result = self.check_text(brief(**{"GOAL": CLEAN_GOAL, section: body}))
                self.assertEqual(
                    (0, "brief-check: no trigger term in GOAL, CHANGE or CONTEXT\n"),
                    (result.returncode, result.stdout),
                    result.stderr,
                )

    def test_a_term_matches_as_a_whole_word_only(self):
        goal = "Pathological configs: the parsers' shells and hooks; a quoted heredocs list, signals, processes."
        result = self.check_text(brief(GOAL=goal))
        self.assertEqual((0, ""), (result.returncode, result.stderr), result.stdout)
        self.assertIn("no trigger term", result.stdout)

    def test_a_closure_naming_each_mechanism_passes_with_or_without_free_text(self):
        for mechanism in MECHANISMS:
            for body in (mechanism, f"{mechanism}: shfmt --to-json walks every word, so no reader is written here."):
                with self.subTest(closure=body):
                    result = self.check_text(brief(GOAL="A shell reader.", CLOSURE=body))
                    self.assertEqual(
                        (0, f'brief-check: GOAL holds "shell"; closure: {mechanism}\n'),
                        (result.returncode, result.stdout),
                        result.stderr,
                    )

    def test_a_closure_naming_two_mechanisms_an_unknown_word_or_nothing_exits_1(self):
        for body, message in (
            ("ast\nremove", "CLOSURE names 2 mechanisms (ast, remove), not one"),
            ("ast: the walk\nallowlist: the forms", "CLOSURE names 2 mechanisms (ast, allowlist), not one"),
            ("hardening", 'CLOSURE line "hardening" names no mechanism (ast, parser-module, allowlist, remove)'),
            ("AST", 'CLOSURE line "AST" names no mechanism'),
            ("- ast", 'CLOSURE line "- ast" names no mechanism'),
            ("ast\nA second line of prose.", 'CLOSURE line "A second line of prose." names no mechanism'),
            ("", "CLOSURE is empty"),
            ("\n   \n", "CLOSURE is empty"),
        ):
            with self.subTest(closure=body):
                result = self.check_text(brief(GOAL="A shell reader.", CLOSURE=body))
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertIn('brief-check: GOAL holds "shell"', result.stdout)
                self.assertIn(message, result.stdout)

    def test_a_malformed_closure_exits_1_even_without_a_trigger_term(self):
        # A section the check owns and cannot read is never read as clean (preferences.md standing order 21).
        result = self.check_text(brief(GOAL=CLEAN_GOAL, CLOSURE="hardening"))
        self.assertEqual(
            (1, 'brief-check: CLOSURE line "hardening" names no mechanism (ast, parser-module, allowlist, remove)\n'),
            (result.returncode, result.stdout),
            result.stderr,
        )
        result = self.check_text(brief(GOAL=CLEAN_GOAL, CLOSURE="remove: the feature leaves"))
        self.assertEqual(
            (0, "brief-check: no trigger term in GOAL, CHANGE or CONTEXT\n"),
            (result.returncode, result.stdout),
            result.stderr,
        )

    def test_no_trigger_term_and_no_closure_exits_0(self):
        result = self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE="six installers", CHANGE="1. Delete them."))
        self.assertEqual(
            (0, "brief-check: no trigger term in GOAL, CHANGE or CONTEXT\n"), (result.returncode, result.stdout)
        )

    def test_a_section_line_is_the_exact_upper_case_name(self):
        # `GOAL:` and `## GOAL` are prose, not section lines, so the title and such lines fire nothing; a repeated
        # section's bodies are read together, so two CLOSURE sections of one mechanism each name two.
        result = self.check_text("GOAL: a shell reader\n## GOAL\nshell\n" + brief(GOAL=CLEAN_GOAL))
        self.assertEqual(0, result.returncode, result.stdout)
        result = self.check_text(brief(GOAL="A shell reader.", CLOSURE="ast") + "CLOSURE\nremove\n")
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("CLOSURE names 2 mechanisms", result.stdout)

    def test_an_unreadable_or_undecodable_file_and_a_usage_error_exit_2_with_nothing_on_stdout(self):
        missing = self.dir / "absent.md"
        directory = self.dir / "a-directory"
        directory.mkdir()
        binary = self.dir / "binary.md"
        binary.write_bytes(b"GOAL\n\xff\xfe shell\n")
        for args in ((str(missing),), (str(directory),), (str(binary),), (), (str(missing), str(binary))):
            with self.subTest(args=args):
                result = self.check(*args)
                self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
                self.assertNotEqual("", result.stderr)
        result = self.check(str(missing))
        self.assertIn(f"brief-check: cannot read {missing}", result.stderr)

    def test_a_brief_with_no_sections_at_all_exits_1_with_a_message(self):
        for text in ("", "# U0 A title\n\nA paragraph that mentions a shell reader.\n", "SCOPE\none shell file\n"):
            with self.subTest(text=text[:20]):
                result = self.check_text(text)
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertIn("has no GOAL, CHANGE or CONTEXT section", result.stdout)

    def test_the_script_runs_by_its_own_name_under_python_isolated_mode(self):
        # The SKILL sentence runs the file directly, so it is executable and its shebang runs `python -I`.
        self.assertTrue(os.access(SCRIPT, os.X_OK), f"{SCRIPT} is not executable")
        self.assertEqual("#!/usr/bin/env -S uv run --no-project python -I", SCRIPT.read_text().splitlines()[0])

    def test_the_orchestration_skill_step_1_runs_the_check_before_the_task_line(self):
        text = SKILL.read_text()
        step = next(line for line in text.splitlines() if line.startswith("1. Brief."))
        self.assertIn(SKILL_SENTENCE, step)
        self.assertLess(step.index("briefs/U<n>-<slug>.md` with GOAL"), step.index(SKILL_SENTENCE))


if __name__ == "__main__":
    unittest.main()
