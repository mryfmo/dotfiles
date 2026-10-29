"""Exercise brief-check.py (regime-cutover U104, U121) on scratch briefs, as a subprocess under `python -I`, and its
installed copy under a scratch HOME as the hcom-orchestration SKILL spells the command (U104 round 3)."""

import builtins
import contextlib
import errno
import io
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/orchestrator/brief-check.py"
# The copy chezmoi installs as ~/.local/bin/common/brief-check.py and the manifest that pins it (U31 shape).
INSTALLED = ROOT / "home/dot_local/bin/common/executable_brief-check.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
SKILL = ROOT / "home/dot_agents/skills/hcom-orchestration/SKILL.md"
# An installation reached through a symlink: `~/.local` a link, or `common` itself (round 5).
SYMLINKED_INSTALLS = (".local", ".local/bin/common")
# The trigger table as the briefs fixed it (U104's rows, then U121's), each as a brief would write it, with the term
# the reason line names; a later unit that adds a row adds it here too.
TRIGGERS = (
    ("shell", "shell"),
    ("tokenize", "tokeniz"),
    ("tokenizer", "tokeniz"),
    ("tokenization", "tokeniz"),
    ("parse", "parse"),
    ("parser", "parser"),
    ("regex", "regex"),
    ("hook", "hook"),
    ("worktree", "worktree"),
    ("config", "config"),
    ("path", "path"),
    ("process", "process"),
    ("signal", "signal"),
    ("supervisor", "supervisor"),
    ("curl", "curl"),
    ("wget", "wget"),
    ("heredoc", "heredoc"),
    ("quote", "quote"),
    ("bound", "bound"),
    ("refuse", "refuse"),
    ("fail closed", "fail closed"),
    ("fail-closed", "fail closed"),
    ("untrusted", "untrusted"),
    ("sandbox", "sandbox"),
    ("lint", "lint"),
    ("rule", "rule"),
    ("allowlist", "allowlist"),
    ("denylist", "denylist"),
    ("walk", "walk"),
    ("census", "census"),
)
FORMS = ("ast", "parser-module", "allowlist", "remove")
SKILL_SENTENCE = (
    "Run `~/.local/bin/common/brief-check.py .orchestration/orchestrate/<program>/briefs/U<n>-<slug>.md` from the "
    "checkout and send no TASK while it exits non-zero; a brief whose unit judges an open-ended input names the "
    "closing mechanism in a `CLOSURE` section (`ast`, `parser-module`, `allowlist` or `remove`)."
)
TRUST_SENTENCE = (
    "Such a brief also carries a `TRUST` section of at least 40 characters naming what the unit trusts and does not "
    "read (an earlier step of the same job, the adopted lever set, a pinned image), which the PR body's Contract "
    "repeats as its `Trusted:` sentence; the check refuses a brief without one."
)
# The command inside the sentence's first code span, the spelling the orchestrator seat runs.
SKILL_COMMAND = SKILL_SENTENCE.split("`")[1]
CLEAN_GOAL = "The six dead installer functions leave the installers and nothing else changes."
TRUST = "The unit trusts the pinned lever set under ~/.local/bin/common and reads no earlier job step."


def brief(**bodies):
    """A brief in the grammar: a title, then each named section as its upper-case line and body."""
    text = "# U0 A scratch brief\n\n"
    for name, body in bodies.items():
        text += f"{name}\n{body}\n\n"
    return text


def closed(goal="A shell reader.", closure="ast", trust=TRUST, **bodies):
    """A brief that holds a trigger term and names both its form and its trust boundary."""
    return brief(GOAL=goal, CLOSURE=closure, TRUST=trust, **bodies)


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

    def assert_passes(self, result):
        """Exit 0 and nothing on either stream: a passing brief prints no line."""
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def assert_refused(self, result, *reasons):
        """Exit 1, nothing on stderr, and on stdout exactly one line per expected reason, each holding its text."""
        self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
        lines = result.stdout.splitlines()
        self.assertEqual(len(reasons), len(lines), result.stdout)
        for line, reason in zip(lines, reasons):
            self.assertTrue(line.startswith(f"brief-check: {self.dir / 'U0-scratch.md'}: "), line)
            self.assertIn(reason, line)

    def test_each_trigger_term_in_goal_without_closure_or_trust_exits_1_with_one_reason_per_line(self):
        for spelling, term in TRIGGERS:
            with self.subTest(term=spelling):
                result = self.check_text(brief(GOAL=f"This unit reads the {spelling} of every seat.", SCOPE="x"))
                self.assert_refused(result, f'GOAL holds "{term}" (', f'GOAL holds "{term}"; no TRUST section')
                self.assertIn("; no CLOSURE section", result.stdout.splitlines()[0])

    def test_each_trigger_term_with_a_form_and_a_trust_boundary_exits_0_printing_nothing(self):
        for spelling, _ in TRIGGERS:
            with self.subTest(term=spelling):
                self.assert_passes(self.check_text(closed(goal=f"This unit reads the {spelling} of every seat.")))

    def test_a_spelling_the_regex_folds_onto_a_term_prints_that_term_s_reason_line_never_a_traceback(self):
        # U104 round 1: `ſhell` matched under `re.IGNORECASE`, then `"ſhell".lower()` missed the reasons table and the
        # script died with a KeyError traceback. The reason comes from the table row the regex matched.
        for spelling, term in (("\u017fhell", "shell"), ("hoo\u212a", "hook"), ("wor\u212atree", "worktree")):
            with self.subTest(spelling=spelling):
                result = self.check_text(brief(GOAL=f"A {spelling} reader."))
                self.assert_refused(result, f'GOAL holds "{term}" (', f'GOAL holds "{term}"; no TRUST section')
                self.assert_passes(self.check_text(closed(goal=f"A {spelling} reader.")))

    def test_a_term_in_change_or_context_fires_and_a_capitalised_or_backticked_term_counts(self):
        for section, body in (
            ("CHANGE", "1. Rewrite the Parser."),
            ("CONTEXT", "- The old `regex` matched three forms."),
            ("GOAL", "A SHELL reader."),
            ("CHANGE", "2. The read is `fail-closed`."),
        ):
            with self.subTest(section=section, body=body):
                result = self.check_text(brief(**({"GOAL": CLEAN_GOAL} | {section: body})))
                self.assert_refused(result, f"{section} holds", f"{section} holds")

    def test_a_term_inside_scope_forbidden_or_the_worker_rules_alone_fires_nothing(self):
        body = "No regex over the brief; one shell file under the path scripts/; no hook, no config edit, no lint."
        for section in ("SCOPE", "FORBIDDEN", "ACCEPTANCE", "VERIFY", "TIMEBOX", "REPORT", "STANDING", "TRUST"):
            with self.subTest(section=section):
                self.assert_passes(self.check_text(brief(**{"GOAL": CLEAN_GOAL, section: body})))
        # The worker-rules block follows CONTEXT in the store's briefs; its heading carries a parenthesised note.
        text = (
            brief(GOAL=CLEAN_GOAL, CONTEXT="Nothing open-ended.") + f"WORKER RULES (standing orders 27, 29)\n{body}\n"
        )
        self.assert_passes(self.check_text(text))
        text = brief(GOAL=CLEAN_GOAL, CONTEXT="Nothing open-ended.") + f"WORKER RULES\n{body}\n"
        self.assert_refused(self.check_text(text), "CONTEXT holds", "CONTEXT holds")

    def test_a_term_matches_as_a_whole_word_only(self):
        goal = (
            "Pathological configs: the parsers' shells and hooks; a quoted heredocs list, signals, processes, "
            "rules, bounds, walks, unbounded sandboxes, failing closed linters, refused censuses, a trusted allowlisted."
        )
        self.assert_passes(self.check_text(brief(GOAL=goal)))

    def test_a_closure_naming_each_form_passes_with_or_without_free_text(self):
        for form in FORMS:
            for body in (form, f"{form}: shfmt --to-json walks every word, so no reader is written here."):
                with self.subTest(closure=body):
                    self.assert_passes(self.check_text(closed(closure=body)))

    def test_a_closure_naming_two_forms_an_unknown_word_or_nothing_exits_1(self):
        for body, message in (
            ("ast\nremove", "CLOSURE names 2 forms (ast, remove), not one"),
            ("ast: the walk\nallowlist: the forms", "CLOSURE names 2 forms (ast, allowlist), not one"),
            ("hardening", 'CLOSURE line "hardening" names no form (ast, parser-module, allowlist, remove)'),
            ("AST", 'CLOSURE line "AST" names no form'),
            ("- ast", 'CLOSURE line "- ast" names no form'),
            ("ast\nA second line of prose.", 'CLOSURE line "A second line of prose." names no form'),
            ("", "CLOSURE is empty"),
            ("\n   \n", "CLOSURE is empty"),
        ):
            with self.subTest(closure=body):
                result = self.check_text(closed(closure=body))
                self.assert_refused(result, 'GOAL holds "shell" (')
                self.assertIn(message, result.stdout)

    def test_a_malformed_closure_exits_1_even_without_a_trigger_term(self):
        # A section the check owns and cannot read is never read as clean (preferences.md standing order 21).
        result = self.check_text(brief(GOAL=CLEAN_GOAL, CLOSURE="hardening"))
        self.assert_refused(result, 'CLOSURE line "hardening" names no form (ast, parser-module, allowlist, remove)')
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, CLOSURE="remove: the feature leaves")))

    def test_a_missing_short_or_unnamed_trust_section_exits_1_beside_a_sound_closure(self):
        for text, message in (
            (brief(GOAL="A shell reader.", CLOSURE="ast"), "no TRUST section"),
            (closed(trust=""), "TRUST is 0 characters, under 40"),
            (closed(trust="The unit trusts the levers."), "TRUST is 27 characters, under 40"),
            (
                closed(trust="The unit reads the brief alone and never the adopted lever set or an earlier job step."),
                "TRUST names nothing as trusted (no word `trusted` or `trusts`)",
            ),
            (
                closed(trust="A trustworthy image is used; the untrusted bus text is never read by this unit."),
                "TRUST names",
            ),
        ):
            with self.subTest(text=text[-80:]):
                self.assert_refused(self.check_text(text), f'GOAL holds "shell"; {message}')
        for trust in (
            TRUST,
            "Trusted: the pinned image `ghcr.io/x/y@sha256:...` and the adopted lever set; the bus text is data.",
            "What the unit TRUSTS is the earlier apt step of the same job; it reads no mirror list itself.",
            "  Trusts\n\n  the pinned levers under ~/.local/bin/common and nothing else.  ",
        ):
            with self.subTest(trust=trust):
                self.assert_passes(self.check_text(closed(trust=trust)))

    def test_a_trust_section_is_not_required_without_a_trigger_term(self):
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE="six installers", CHANGE="1. Delete them.")))

    def test_a_denylist_dressed_as_an_allowlist_or_an_ast_walk_exits_1(self):
        for form in ("allowlist", "ast"):
            for change, phrase in (
                ("1. Keep a denylist of the words the lint refuses.", "denylist"),
                ("1. The check holds the Forbidden Words in one tuple.", "forbidden words"),
                ("1. Compare each line against a list of commands.", "list of commands"),
            ):
                with self.subTest(form=form, change=change):
                    result = self.check_text(closed(closure=form, CHANGE=change))
                    self.assert_refused(
                        result, f'CLOSURE names {form} and CHANGE holds "{phrase}": a denylist dressed as a form'
                    )
        # The same CHANGE under `remove` or `parser-module` is not dressed, and the phrases elsewhere do not count.
        for form in ("remove", "parser-module"):
            with self.subTest(form=form):
                self.assert_passes(self.check_text(closed(closure=form, CHANGE="1. Drop the denylist.")))
        self.assert_passes(self.check_text(closed(closure="allowlist", FORBIDDEN="No denylist, no list of commands.")))
        self.assert_passes(self.check_text(closed(closure="allowlist", CHANGE="1. Exact forms; denylists go.")))

    def test_every_reason_is_printed_so_one_run_names_each_missing_part(self):
        text = brief(GOAL="A shell reader.", CHANGE="1. A denylist of words.", CLOSURE="allowlist\nast")
        result = self.check_text(text)
        self.assert_refused(
            result,
            'GOAL holds "shell" (shell text has quoting, expansion and word-splitting forms no hand-written reader '
            "lists); CLOSURE names 2 forms (allowlist, ast), not one",
            'GOAL holds "shell"; no TRUST section',
        )
        result = self.check_text(brief(GOAL="A shell reader.", CHANGE="1. A denylist of words.", CLOSURE="allowlist"))
        self.assert_refused(
            result,
            'GOAL holds "shell"; no TRUST section',
            'CLOSURE names allowlist and CHANGE holds "denylist": a denylist dressed as a form',
        )

    def test_a_section_line_is_the_exact_upper_case_name(self):
        # `GOAL:` and `## GOAL` are prose, not section lines, so the title and such lines fire nothing.
        self.assert_passes(self.check_text("GOAL: a shell reader\n## GOAL\nshell\n" + brief(GOAL=CLEAN_GOAL)))

    def test_a_repeated_section_heading_exits_2_naming_the_heading_and_both_lines(self):
        # U104 round 1 merged the bodies, so `GOAL\nshell\nCLOSURE\nast\nCLOSURE\n` read the empty second CLOSURE as
        # `ast`. A brief outside the grammar is not judged at all (exit 2, nothing on stdout), as an unreadable one.
        for text, message in (
            ("GOAL\nshell\nCLOSURE\nast\nCLOSURE\n", "CLOSURE appears twice (lines 3 and 5)"),
            ("GOAL\nshell\nCLOSURE\nast\nCLOSURE\nremove\n", "CLOSURE appears twice (lines 3 and 5)"),
            (
                brief(GOAL=CLEAN_GOAL, SCOPE="one file") + "GOAL\n" + CLEAN_GOAL + "\n",
                "GOAL appears twice (lines 3 and 9)",
            ),
            ("SCOPE  \none file\nSCOPE\n", "SCOPE appears twice (lines 1 and 3)"),
            ("GOAL\nx\nWORKER RULES (a)\n- y\nWORKER RULES (b)\n", "WORKER RULES appears twice (lines 3 and 5)"),
        ):
            with self.subTest(text=text[:40]):
                result = self.check_text(text)
                self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
                self.assertEqual(
                    f"brief-check: cannot read {self.dir / 'U0-scratch.md'}: {message}; a brief has one of each\n",
                    result.stderr,
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
                self.assert_refused(self.check_text(text), "no GOAL, CHANGE or CONTEXT section")

    def test_the_script_runs_by_its_own_name_under_python_isolated_mode(self):
        # The SKILL sentence runs the file directly, so it is executable and its shebang runs `python3 -I` from PATH:
        # round 4 found `uv run` honouring a `.python-version` in the cwd, so a planted interpreter ran first.
        self.assertTrue(os.access(SCRIPT, os.X_OK), f"{SCRIPT} is not executable")
        self.assertEqual("#!/usr/bin/env -S python3 -I", SCRIPT.read_text().splitlines()[0])

    def test_the_checkout_script_passes_its_self_check_against_the_checkout_manifest(self):
        # Round 3: the script is a pinned lever; run from the checkout it reads home/dot_agents/agent-config.yaml.
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL)))
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

    def test_the_orchestration_skill_step_1_runs_the_check_before_the_task_line_and_names_the_trust_section(self):
        text = SKILL.read_text()
        step = next(line for line in text.splitlines() if line.startswith("1. Brief."))
        self.assertIn(SKILL_SENTENCE, step)
        self.assertLess(step.index("briefs/U<n>-<slug>.md` with GOAL"), step.index(SKILL_SENTENCE))
        self.assertIn(TRUST_SENTENCE, step)
        self.assertLess(step.index(SKILL_SENTENCE), step.index(TRUST_SENTENCE))


class InstalledBriefCheckTest(unittest.TestCase):
    """The installed copy, run as the hcom-orchestration SKILL step 1 spells it (U104 round 3).

    The layout is the one `test_lever_self_check.py` builds: the copy at `<home>/.local/bin/common/brief-check.py`
    and the manifest at `<home>/.agents/agent-config.yaml`, under a scratch HOME. The checkout is shaped like a
    repository other than dotfiles: the brief under `.orchestration/orchestrate/<program>/briefs/`, no `scripts/`.
    """

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.home = self.root / "home"
        self.manifest = self.home / ".agents/agent-config.yaml"
        self.copy = self.home / ".local/bin/common/brief-check.py"
        (self.home / ".local/bin/common").mkdir(parents=True)
        (self.home / ".agents").mkdir()
        self.assertTrue(INSTALLED.is_file(), f"{INSTALLED} is the copy chezmoi installs; the generator writes it")
        shutil.copy2(INSTALLED, self.copy)
        shutil.copy2(MANIFEST, self.manifest)
        self.checkout = self.root / "checkout"
        self.briefs = self.checkout / ".orchestration/orchestrate/p/briefs"
        self.briefs.mkdir(parents=True)
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}

    def pin_lines(self, replacement):
        """Rewrite the deployed pin line of brief-check.py as `replacement` (a line, two lines, or nothing)."""
        text = self.manifest.read_text()
        pin_line = next(line for line in text.splitlines() if line.startswith("      brief-check.py: "))
        self.manifest.write_text(text.replace(pin_line + "\n", replacement))

    def zero_pin(self):
        self.pin_lines("      brief-check.py: " + "0" * 64 + "\n")

    def run_copy(self, text, env):
        """The copy by its absolute path: with HOME unset bash expands `~` to the passwd entry, not the scratch home."""
        (self.briefs / "U1-x.md").write_text(text)
        return subprocess.run(
            [str(self.copy), ".orchestration/orchestrate/p/briefs/U1-x.md"],
            cwd=self.checkout,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def assert_refused(self, result, message):
        """Exit 2, the refusal in the shell levers' words on stderr, nothing on stdout: no judgement escaped."""
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertIn(f"brief-check.py: refused: {message}", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

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

    @contextlib.contextmanager
    def install_behind_symlink(self, relative):
        """Move `<home>/<relative>` to a physical directory outside HOME and leave a symlink in its place.

        Yields the physical install directory; both spellings put it at `<root>/physical/.local/bin/common`, so two
        levels up from it is `<root>/physical/.local`, where a checkout manifest may or may not be planted.
        """
        link = self.home / relative
        physical = self.root / "physical" / relative
        physical.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(link, physical)
        link.symlink_to(physical)
        try:
            yield self.root / "physical/.local/bin/common"
        finally:
            link.unlink()
            shutil.move(physical, link)
            shutil.rmtree(self.root / "physical")

    def test_the_skill_command_judges_a_store_brief_from_a_checkout_without_scripts(self):
        # The round-2 audit's integration failure: the skill's own command on a valid brief.
        self.assertFalse((self.checkout / "scripts").exists())
        result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
        self.assertEqual(
            (0, "", ""),
            (result.returncode, result.stdout, result.stderr),
        )
        result = self.run_skill_command(brief(GOAL="A shell reader."))
        self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
        self.assertIn('GOAL holds "shell"', result.stdout)
        self.assertIn("no CLOSURE section", result.stdout)
        self.assertIn("no TRUST section", result.stdout)

    def test_a_copy_whose_deployed_pin_differs_refuses_and_judges_nothing(self):
        self.zero_pin()
        result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
        self.assert_refused(result, "sha256 ")
        self.assertIn(f"differs from the pin in {self.manifest}", result.stderr)

    def test_the_cwd_and_the_environment_choose_no_interpreter(self):
        """Round 4 (P1): `uv run --no-project` honoured a `.python-version` in the checkout the lever ran from, so an
        interpreter planted there answered before the self-check (exit 0 on `GOAL\\nshell\\n` with a zeroed pin).

        The plant is what uv honours: a `.python-version` naming the path of a venv (a shell script fails uv's
        interpreter probe) whose `sitecustomize` exits 0 silently, the clean decision, whenever the script run is
        brief-check.py, beside a `pyproject.toml`, with PYTHONPATH and PYTHONSTARTUP naming planted files. The
        shebang runs `python3 -I` from PATH, so none of it is consulted.
        """
        text = brief(GOAL="A shell reader.")
        clean = self.run_skill_command(text)
        self.assertEqual((1, ""), (clean.returncode, clean.stderr), clean.stdout)
        self.assertIn('GOAL holds "shell"', clean.stdout)
        venv = self.root / "venv"
        subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(venv)], check=True, capture_output=True)
        site = next(venv.glob("lib/python3*/site-packages"))
        (site / "sitecustomize.py").write_text(
            'import os, sys\nif sys.argv and sys.argv[0].endswith("brief-check.py"):\n    os._exit(0)\n'
        )
        (self.checkout / ".python-version").write_text(f"{venv}/bin/python\n")
        (self.checkout / "pyproject.toml").write_text(
            '[project]\nname = "p"\nversion = "0"\nrequires-python = ">=3.9"\n'
        )
        planted = self.root / "planted"
        planted.mkdir()
        (planted / "hashlib.py").write_text('raise SystemExit("planted hashlib")\n')
        (planted / "startup.py").write_text('raise SystemExit("planted startup")\n')
        self.env |= {"PYTHONPATH": str(planted), "PYTHONSTARTUP": str(planted / "startup.py")}
        self.zero_pin()
        result = self.run_skill_command(text)
        self.assert_refused(result, "sha256 ")
        self.assertIn(f"differs from the pin in {self.manifest}", result.stderr)
        shutil.copy2(MANIFEST, self.manifest)
        result = self.run_skill_command(text)
        self.assertEqual(
            (clean.returncode, clean.stdout, clean.stderr), (result.returncode, result.stdout, result.stderr)
        )

    @unittest.skipIf(os.geteuid() == 0, "mode 000 does not stop root, so the unreadable-manifest injection is skipped")
    def test_an_unreadable_manifest_refuses_before_any_judgement(self):
        self.manifest.chmod(0)
        self.addCleanup(self.manifest.chmod, 0o644)
        self.assert_refused(self.run_skill_command(brief(GOAL=CLEAN_GOAL)), f"manifest unreadable: {self.manifest}")

    def test_a_manifest_that_is_a_directory_passes_the_access_test_and_refuses_on_the_read(self):
        self.manifest.unlink()
        self.manifest.mkdir()
        self.assertTrue(os.access(self.manifest, os.R_OK))
        self.assert_refused(self.run_skill_command(brief(GOAL=CLEAN_GOAL)), f"cannot read {self.manifest}")

    def test_an_absent_or_doubled_pin_line_refuses(self):
        text = self.manifest.read_text()
        pin_line = next(line for line in text.splitlines() if line.startswith("      brief-check.py: "))
        for replacement in ("", pin_line + "\n" + pin_line + "\n"):
            with self.subTest(pin_lines=replacement.count("\n")):
                self.manifest.write_text(text)
                self.pin_lines(replacement)
                result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
                self.assert_refused(result, f"no single sha256 pin for brief-check.py in {self.manifest}")

    @unittest.skipIf(os.geteuid() == 0, "mode 000 does not stop root, so the unreadable-copy case is skipped")
    def test_an_unreadable_copy_is_refused_by_the_interpreter_before_any_judgement(self):
        # Mode 000 stops the shell: bash exits 126 before python3 starts, so the self-check's own hash read is never
        # reached here (round 6) and no refusal line is owed. What this shows is only that nothing is judged (non-zero
        # exit, empty stdout). The two tests below fail that read.
        self.copy.chmod(0)
        self.addCleanup(self.copy.chmod, 0o755)
        result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertEqual("", result.stdout)

    def test_a_failed_hash_read_of_the_copy_refuses_naming_the_path_it_could_not_hash(self):
        """Round 6 (P2): the mode-000 case exits 126 from the shell, so no committed test failed the self-check's read of
        its own bytes. The installed copy's bytes go in on stdin, `python3 -I - <brief>`, from a cwd shaped like the
        dotfiles checkout (`scripts/orchestrator`, the manifest with the correct pin two levels up): `__file__` is
        `<stdin>`, so the manifest step passes and the hash step opens `<cwd>/<stdin>`, which does not exist."""
        shape = self.root / "shape/scripts/orchestrator"
        shape.mkdir(parents=True)
        (self.root / "shape/home/dot_agents").mkdir(parents=True)
        shutil.copy2(MANIFEST, self.root / "shape/home/dot_agents/agent-config.yaml")
        (self.briefs / "U1-x.md").write_text(brief(GOAL=CLEAN_GOAL))
        with open(self.copy, "rb") as handle:
            result = subprocess.run(
                ["python3", "-I", "-", str(self.briefs / "U1-x.md")],
                cwd=shape,
                env=self.env,
                stdin=handle,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
        self.assert_refused(result, f"cannot hash {shape}/<stdin>")

    def test_a_permission_error_on_the_hash_read_refuses_in_process(self):
        """The same read failed as the kernel fails it: `runpy.run_path` on the checkout script with `builtins.open`
        raising `PermissionError` for the script's own path only, so the checkout manifest two levels up is read and
        the hash read is not; exit 2 as `SystemExit`, the refusal on stderr, nothing on stdout."""
        real_open = builtins.open

        def open_except_self(file, *args, **kwargs):
            if str(file) == str(SCRIPT):
                raise PermissionError(errno.EACCES, "Permission denied", str(file))
            return real_open(file, *args, **kwargs)

        out, err = io.StringIO(), io.StringIO()
        with (
            mock.patch("builtins.open", open_except_self),
            contextlib.redirect_stdout(out),
            contextlib.redirect_stderr(err),
            self.assertRaises(SystemExit) as raised,
        ):
            runpy.run_path(str(SCRIPT), run_name="__main__")
        self.assertEqual(2, raised.exception.code)
        self.assertEqual("", out.getvalue())
        self.assertEqual(f"brief-check.py: refused: cannot hash {SCRIPT}\n", err.getvalue())

    def test_an_unset_or_missing_home_chooses_the_checkout_manifest(self):
        # Neither case may crash: the physical directory of the copy decides, and two levels up from the scratch bin
        # there is no checkout, so the refusal names that manifest and nothing is judged.
        checkout_manifest = f"{self.copy.parent}/../../home/dot_agents/agent-config.yaml"
        for name, env in (
            ("unset", {key: value for key, value in self.env.items() if key != "HOME"}),
            ("missing", {**self.env, "HOME": str(self.root / "nobody")}),
        ):
            with self.subTest(home=name):
                result = self.run_copy(brief(GOAL=CLEAN_GOAL), env)
                self.assert_refused(result, f"manifest unreadable: {checkout_manifest}")

    def test_an_install_behind_a_symlink_with_a_zeroed_deployed_pin_refuses_naming_the_deployed_manifest(self):
        """Round 5 (P2): the comparison resolved HOME but not `.local/bin/common`, so an install reached through a
        symlinked `.local` (or `common`) compared unequal and the checkout manifest two levels up from the physical
        directory was read; a correct pin planted there let a copy with a zeroed deployed pin judge the brief."""
        self.zero_pin()
        for relative in SYMLINKED_INSTALLS:
            with self.subTest(symlink=relative), self.install_behind_symlink(relative) as physical:
                checkout_manifest = physical.parent.parent / "home/dot_agents/agent-config.yaml"
                checkout_manifest.parent.mkdir(parents=True)
                shutil.copy2(MANIFEST, checkout_manifest)
                result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
                self.assert_refused(result, "sha256 ")
                self.assertIn(f"differs from the pin in {self.manifest}", result.stderr)

    def test_an_install_behind_a_symlink_with_the_correct_deployed_pin_judges_the_brief(self):
        # No checkout manifest exists above the physical directory, so round 4 refused a sound installation.
        for relative in SYMLINKED_INSTALLS:
            with self.subTest(symlink=relative), self.install_behind_symlink(relative) as physical:
                self.assertFalse((physical.parent.parent / "home").exists())
                result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
                self.assertEqual(
                    (0, "", ""),
                    (result.returncode, result.stdout, result.stderr),
                )


if __name__ == "__main__":
    unittest.main()
