"""Exercise brief-check.py (regime-cutover U104) on scratch briefs, as a subprocess under `python -I`, and its installed
copy under a scratch HOME as the hcom-orchestration SKILL spells the command (round 3)."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/orchestrator/brief-check.py"
# The copy chezmoi installs as ~/.local/bin/common/brief-check.py and the manifest that pins it (U31 shape).
INSTALLED = ROOT / "home/dot_local/bin/common/executable_brief-check.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
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
    "Run `~/.local/bin/common/brief-check.py .orchestration/orchestrate/<program>/briefs/U<n>-<slug>.md` from the "
    "checkout and send no TASK while it exits non-zero; a brief whose unit judges an open-ended input names the "
    "closing mechanism in a `CLOSURE` section (`ast`, `parser-module`, `allowlist` or `remove`)."
)
# The command inside the sentence's first code span, the spelling the orchestrator seat runs.
SKILL_COMMAND = SKILL_SENTENCE.split("`")[1]
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

    def test_a_spelling_the_regex_folds_onto_a_term_prints_that_term_s_decision_line_never_a_traceback(self):
        # Round 1: `ſhell` matched under `re.IGNORECASE`, then `"ſhell".lower()` missed the reasons table and the
        # script died with a KeyError traceback. The reason now comes from the table row the regex matched.
        for spelling, term in (("\u017fhell", "shell"), ("hoo\u212a", "hook"), ("wor\u212atree", "worktree")):
            with self.subTest(spelling=spelling):
                result = self.check_text(brief(GOAL=f"A {spelling} reader."))
                self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
                prefix = f'brief-check: GOAL holds "{term}" ('
                self.assertEqual(prefix, result.stdout[: len(prefix)], result.stdout)
                self.assertIn("; no CLOSURE section\n", result.stdout)
                result = self.check_text(brief(GOAL=f"A {spelling} reader.", CLOSURE="ast"))
                self.assertEqual(
                    (0, f'brief-check: GOAL holds "{term}"; closure: ast\n'), (result.returncode, result.stdout)
                )

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
        # `GOAL:` and `## GOAL` are prose, not section lines, so the title and such lines fire nothing.
        result = self.check_text("GOAL: a shell reader\n## GOAL\nshell\n" + brief(GOAL=CLEAN_GOAL))
        self.assertEqual(
            (0, "brief-check: no trigger term in GOAL, CHANGE or CONTEXT\n"), (result.returncode, result.stdout)
        )

    def test_a_repeated_section_heading_exits_1_naming_the_heading_and_both_lines(self):
        # Round 1 merged the bodies, so `GOAL\nshell\nCLOSURE\nast\nCLOSURE\n` read the empty second CLOSURE as `ast`.
        for text, message in (
            ("GOAL\nshell\nCLOSURE\nast\nCLOSURE\n", "CLOSURE appears twice (lines 3 and 5)"),
            ("GOAL\nshell\nCLOSURE\nast\nCLOSURE\nremove\n", "CLOSURE appears twice (lines 3 and 5)"),
            (
                brief(GOAL=CLEAN_GOAL, SCOPE="one file") + "GOAL\n" + CLEAN_GOAL + "\n",
                "GOAL appears twice (lines 3 and 9)",
            ),
            ("SCOPE  \none file\nSCOPE\n", "SCOPE appears twice (lines 1 and 3)"),
        ):
            with self.subTest(text=text[:40]):
                result = self.check_text(text)
                self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
                self.assertEqual(
                    f"brief-check: {self.dir / 'U0-scratch.md'}: {message}; a brief has one of each\n", result.stdout
                )

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

    def test_the_checkout_script_passes_its_self_check_against_the_checkout_manifest(self):
        # Round 3: the script is a pinned lever; run from the checkout it reads home/dot_agents/agent-config.yaml.
        result = self.check_text(brief(GOAL=CLEAN_GOAL))
        self.assertEqual(
            (0, "brief-check: no trigger term in GOAL, CHANGE or CONTEXT\n", ""),
            (result.returncode, result.stdout, result.stderr),
        )
        # A checkout-shaped copy beside a manifest whose pin differs is refused naming that manifest, so the
        # checkout branch of the manifest choice is the one exercised here, not the cwd.
        checkout = self.dir / "checkout"
        (checkout / "scripts/orchestrator").mkdir(parents=True)
        (checkout / "home/dot_agents").mkdir(parents=True)
        shutil.copy2(SCRIPT, checkout / "scripts/orchestrator/brief-check.py")
        text = MANIFEST.read_text()
        pin_line = next(line for line in text.splitlines() if line.startswith("      brief-check.py: "))
        (checkout / "home/dot_agents/agent-config.yaml").write_text(
            text.replace(pin_line, "      brief-check.py: " + "0" * 64)
        )
        target = self.dir / "U0-scratch.md"
        cmd = [sys.executable, "-I", str(checkout / "scripts/orchestrator/brief-check.py"), str(target)]
        result = subprocess.run(cmd, cwd=self.dir, capture_output=True, text=True, timeout=120, check=False)
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertIn("brief-check.py: refused: sha256 ", result.stderr)
        # The lever names the physical directory (`realpath`), which on macOS differs from the tempdir's spelling.
        physical = (checkout / "scripts/orchestrator").resolve()
        self.assertIn(f"differs from the pin in {physical}/../../home/dot_agents/agent-config.yaml", result.stderr)

    def test_the_orchestration_skill_step_1_runs_the_check_before_the_task_line(self):
        text = SKILL.read_text()
        step = next(line for line in text.splitlines() if line.startswith("1. Brief."))
        self.assertIn(SKILL_SENTENCE, step)
        self.assertLess(step.index("briefs/U<n>-<slug>.md` with GOAL"), step.index(SKILL_SENTENCE))


class InstalledBriefCheckTest(unittest.TestCase):
    """The installed copy, run as the hcom-orchestration SKILL step 1 spells it (U104 round 3).

    The layout is the one `test_lever_self_check.py` builds: the copy at `<home>/.local/bin/common/brief-check.py`
    and the manifest at `<home>/.agents/agent-config.yaml`, under a scratch HOME. The checkout is shaped like a
    repository other than dotfiles: the brief under `.orchestration/orchestrate/<program>/briefs/`, no `scripts/`.
    """

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve()
        self.home = root / "home"
        self.manifest = self.home / ".agents/agent-config.yaml"
        (self.home / ".local/bin/common").mkdir(parents=True)
        (self.home / ".agents").mkdir()
        self.assertTrue(INSTALLED.is_file(), f"{INSTALLED} is the copy chezmoi installs; the generator writes it")
        shutil.copy2(INSTALLED, self.home / ".local/bin/common/brief-check.py")
        shutil.copy2(MANIFEST, self.manifest)
        self.checkout = root / "checkout"
        self.briefs = self.checkout / ".orchestration/orchestrate/p/briefs"
        self.briefs.mkdir(parents=True)
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}

    def run_skill_command(self, text):
        """The SKILL command with `<program>` and `U<n>-<slug>` substituted, through bash so `~` expands as in the seat."""
        (self.briefs / "U1-x.md").write_text(text)
        command = SKILL_COMMAND.replace("<program>", "p").replace("U<n>-<slug>", "U1-x")
        return subprocess.run(
            ["bash", "-c", command],
            cwd=self.checkout,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def test_the_skill_command_judges_a_store_brief_from_a_checkout_without_scripts(self):
        # The round-2 audit's integration failure: the skill's own command on a valid brief.
        self.assertFalse((self.checkout / "scripts").exists())
        result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
        self.assertEqual(
            (0, "brief-check: no trigger term in GOAL, CHANGE or CONTEXT\n", ""),
            (result.returncode, result.stdout, result.stderr),
        )
        result = self.run_skill_command(brief(GOAL="A shell reader."))
        self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
        self.assertIn('brief-check: GOAL holds "shell"', result.stdout)
        self.assertIn("no CLOSURE section", result.stdout)

    def test_a_copy_whose_deployed_pin_differs_refuses_and_judges_nothing(self):
        text = self.manifest.read_text()
        pin_line = next(line for line in text.splitlines() if line.startswith("      brief-check.py: "))
        self.manifest.write_text(text.replace(pin_line, "      brief-check.py: " + "0" * 64))
        result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertIn("brief-check.py: refused: sha256 ", result.stderr)
        self.assertIn(f"differs from the pin in {self.manifest}", result.stderr)


if __name__ == "__main__":
    unittest.main()
