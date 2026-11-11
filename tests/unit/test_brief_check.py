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
# U249 (standing order 44): an ACCEPTANCE naming one gate of each class, the lint forms and the test forms as a brief
# pastes them, and the reason line for each class it misses.
GATED = (
    "1. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.\n"
    "2. `uv run python -m unittest tests.unit.test_x tests.unit.test_scratch_git` OK."
)
LINT_GATES = ("`scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.", "`make format` exit 0.")
TEST_GATES = (
    "`uv run python -m unittest tests.unit.test_x` OK (paste the count).",
    "`make unit-test` OK.",
    "`node --test home/dot_dsh/plugins/omp-gateway/` exit 0.",
    "`python3 -I U0-tables/check-tables.py U0-tables/*.tsv` exit 0 and its row counts pasted.",
)
NO_LINT_GATE = "ACCEPTANCE names no lint gate (run-on-lint-files.sh, make format)"
NO_TEST_GATE = "ACCEPTANCE names no test gate (python -m unittest, make unit-test, node --test, records-check)"
# U280: a records-only brief (U274's shape: tables under the store's `tests/`, no repository file, SCOPE naming its
# branch) names its own check script as the test gate, under `python3 -I` alone.
RECORDS_SCOPE = (
    "A scratch tree `/tmp/dotfiles-wt/U0` (a worktree of `origin/main`). You write under `/tmp/dotfiles-wt/U0-tables/`."
)
RECORDS_LINT = "`scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0."
# U130: three lever sources as a SCOPE names them, the reason line that refuses them (names sorted), and the SKILL
# sentence that says a brief naming more than two is split before it is sent.
THREE_LEVERS = (
    "scripts/orchestrator/pr-merge.sh",
    "scripts/orchestrator/brief-check.py",
    "scripts/orchestrator/hcom-seat",
)
SPLIT_REASON = (
    "SCOPE names 3 levers (brief-check.py, hcom-seat, pr-merge.sh); split into sequenced units of at most two levers "
    "each (plan P-41: multi-lever briefs took 6.5 audits, single-surface ones 2)"
)
SPLIT_SENTENCE = (
    "A brief whose SCOPE names more than two levers (the manifest's `claude.levers.sha256` names; a source and its "
    "generated copy count once, tests and READMEs never) is refused and is split into sequenced units of at most two "
    "levers each before any TASK is sent (plan P-41: multi-lever briefs took 6.5 audits, single-surface ones 2)."
)


def brief(**bodies):
    """A brief in the grammar: a title, then each named section as its upper-case line and body."""
    text = "# U0 A scratch brief\n\n"
    for name, body in bodies.items():
        text += f"{name}\n{body}\n\n"
    return text


def closed(goal="A shell reader.", closure="ast", trust=TRUST, **bodies):
    """A brief that holds a trigger term and names both its form and its trust boundary."""
    return brief(GOAL=goal, CLOSURE=closure, TRUST=trust, **bodies)


def scope(*paths):
    """A SCOPE body naming each path in backticks, as a brief lists the paths it may write."""
    return "One branch `feat/x` from `origin/main`. May write: " + ", ".join(f"`{path}`" for path in paths) + "."


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

    def assert_refused_exactly(self, result, *reasons):
        """Exit 1, nothing on stderr, and stdout exactly these reason lines in this order, nothing more or fewer."""
        self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
        prefix = f"brief-check: {self.dir / 'U0-scratch.md'}: "
        self.assertEqual([prefix + reason for reason in reasons], result.stdout.splitlines())

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
        # A line naming no form and a count of forms other than one are two faults of one body, both printed.
        for body, messages in (
            ("ast\nremove", ("CLOSURE names 2 forms (ast, remove), not one",)),
            ("ast: the walk\nallowlist: the forms", ("CLOSURE names 2 forms (ast, allowlist), not one",)),
            (
                "hardening",
                (
                    'CLOSURE line "hardening" names no form (ast, parser-module, allowlist, remove)',
                    "CLOSURE names 0 forms, not one",
                ),
            ),
            ("AST", ('CLOSURE line "AST" names no form', "CLOSURE names 0 forms, not one")),
            ("- ast", ('CLOSURE line "- ast" names no form', "CLOSURE names 0 forms, not one")),
            ("ast\nA second line of prose.", ('CLOSURE line "A second line of prose." names no form',)),
            ("", ("CLOSURE is empty",)),
            ("\n   \n", ("CLOSURE is empty",)),
        ):
            with self.subTest(closure=body):
                result = self.check_text(closed(closure=body))
                self.assert_refused(result, 'GOAL holds "shell" (', *('GOAL holds "shell"; ' for _ in messages[1:]))
                for line, message in zip(result.stdout.splitlines(), messages):
                    self.assertIn(message, line)

    def test_a_malformed_closure_exits_1_even_without_a_trigger_term(self):
        # A section the check owns and cannot read is never read as clean (preferences.md standing order 21).
        result = self.check_text(brief(GOAL=CLEAN_GOAL, CLOSURE="hardening"))
        self.assert_refused_exactly(
            result,
            'CLOSURE line "hardening" names no form (ast, parser-module, allowlist, remove)',
            "CLOSURE names 0 forms, not one",
        )
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, CLOSURE="remove: the feature leaves")))

    def test_a_missing_short_or_unnamed_trust_section_exits_1_beside_a_sound_closure(self):
        for text, messages in (
            (brief(GOAL="A shell reader.", CLOSURE="ast"), ("no TRUST section",)),
            (
                closed(trust=""),
                ("TRUST is 0 characters, under 40", "TRUST names nothing as trusted (no word `trusted` or `trusts`)"),
            ),
            (closed(trust="The unit trusts the levers."), ("TRUST is 27 characters, under 40",)),
            (
                closed(trust="The unit reads the brief alone and never the adopted lever set or an earlier job step."),
                ("TRUST names nothing as trusted (no word `trusted` or `trusts`)",),
            ),
            (
                closed(trust="A trustworthy image is used; the untrusted bus text is never read by this unit."),
                ("TRUST names",),
            ),
        ):
            with self.subTest(text=text[-80:]):
                self.assert_refused(self.check_text(text), *(f'GOAL holds "shell"; {message}' for message in messages))
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

    def test_a_trust_section_both_short_and_without_a_trust_word_prints_both_faults_in_one_run(self):
        # Round 2 (P2): the length check returned first, so `Nothing here.` printed one reason and the missing word
        # surfaced only after the section was lengthened; the Contract promises every reason in one run.
        self.assert_refused_exactly(
            self.check_text(closed(trust="Nothing here.")),
            'GOAL holds "shell"; TRUST is 13 characters, under 40',
            'GOAL holds "shell"; TRUST names nothing as trusted (no word `trusted` or `trusts`)',
        )

    def test_a_closure_with_a_stray_line_and_two_forms_prints_both_faults_in_one_run(self):
        # The same shape in CLOSURE: the stray line hid the count fault until the stray line was fixed.
        self.assert_refused_exactly(
            self.check_text(closed(closure="ast\nremove\nhardening")),
            'GOAL holds "shell" (shell text has quoting, expansion and word-splitting forms no hand-written reader '
            'lists); CLOSURE line "hardening" names no form (ast, parser-module, allowlist, remove)',
            'GOAL holds "shell"; CLOSURE names 2 forms (ast, remove), not one',
        )

    def test_the_check_writes_nothing_and_leaves_the_brief_byte_identical(self):
        # The Contract: the script reads the one brief and writes nothing, so a run over a store edits no brief.
        target = self.dir / "U0-scratch.md"
        text = brief(GOAL="A shell reader.")
        target.write_text(text)
        before = (target.read_bytes(), target.stat().st_mtime_ns, sorted(path.name for path in self.dir.iterdir()))
        self.assertEqual(1, self.check(str(target)).returncode)
        self.assertEqual(
            before, (target.read_bytes(), target.stat().st_mtime_ns, sorted(path.name for path in self.dir.iterdir()))
        )
        self.assertEqual(text.encode(), before[0])

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
        self.assertIn(SPLIT_SENTENCE, step)
        self.assertLess(step.index(TRUST_SENTENCE), step.index(SPLIT_SENTENCE))

    def test_a_scope_naming_three_lever_sources_is_refused_naming_them_sorted(self):
        self.assert_refused_exactly(
            self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS), ACCEPTANCE=GATED)), SPLIT_REASON
        )
        # The installed spelling, the bare name and a `./` prefix name the same levers.
        spellings = ("~/.local/bin/common/pr-merge.sh", "brief-check.py", "./scripts/orchestrator/hcom-seat")
        self.assert_refused_exactly(
            self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*spellings), ACCEPTANCE=GATED)), SPLIT_REASON
        )

    def test_a_scope_naming_two_lever_sources_or_none_passes(self):
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS[:2]), ACCEPTANCE=GATED)))
        self.assert_passes(
            self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope("scripts/ci/run-bats.sh", "Makefile"), ACCEPTANCE=GATED))
        )
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL)))

    def test_a_source_and_its_installed_copy_count_once(self):
        copies = [f"home/dot_local/bin/common/executable_{Path(path).name}" for path in THREE_LEVERS]
        self.assert_passes(
            self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS[:2], *copies[:2]), ACCEPTANCE=GATED))
        )
        # Three sources and their three copies are three levers, not six.
        result = self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS, *copies), ACCEPTANCE=GATED))
        self.assert_refused_exactly(result, SPLIT_REASON)

    def test_tests_readmes_the_generated_outputs_and_the_manifest_never_count(self):
        never = (
            "tests/unit/test_pr_audit.py",
            "scripts/orchestrator/README.md",
            "scripts/generated-agent-outputs.json",
            "home/dot_agents/agent-config.yaml",
            "tests/fixtures/pr-merge.sh",
            "README.md",
        )
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*never), ACCEPTANCE=GATED)))
        # Beside two levers they still add nothing: a counted `tests/fixtures/pr-merge.sh` would make three.
        self.assert_passes(
            self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*never, *THREE_LEVERS[1:]), ACCEPTANCE=GATED))
        )
        # A lever named inside a command span or in prose, and a lever name in another section, count nothing.
        body = "`ls scripts/orchestrator/hcom-seat pr-merge.sh brief-check.py`; hcom-seat, pr-merge.sh, brief-check.py."
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=body, FORBIDDEN=scope(*THREE_LEVERS))))

    def test_the_lever_count_is_printed_beside_the_other_reasons_in_one_run(self):
        result = self.check_text(brief(GOAL="A shell reader.", SCOPE=scope(*THREE_LEVERS), ACCEPTANCE=GATED))
        self.assert_refused(result, 'GOAL holds "shell" (', 'GOAL holds "shell"; no TRUST section', SPLIT_REASON)

    def test_a_scope_naming_a_repository_path_passes_with_a_lint_and_a_test_gate_in_acceptance(self):
        # U249 (standing order 44): each lint form beside each test form, as a brief pastes them.
        for lint_gate in LINT_GATES:
            for test_gate in TEST_GATES:
                with self.subTest(lint=lint_gate, test=test_gate):
                    acceptance = f"1. {lint_gate}\n2. {test_gate}\n3. `make shellcheck` exit 0."
                    text = brief(GOAL=CLEAN_GOAL, SCOPE=scope("scripts/ci/run-bats.sh"), ACCEPTANCE=acceptance)
                    self.assert_passes(self.check_text(text))

    def test_an_acceptance_with_a_lint_gate_alone_is_refused_naming_the_missing_test_gate(self):
        # `bats` is no test gate (AGENTS.md Test Policy forbids a local run), and a `check` row stands in for neither.
        for lint_gate in LINT_GATES:
            with self.subTest(lint=lint_gate):
                acceptance = f"1. {lint_gate}\n2. `bats tests/x.bats` passes.\n3. `make render-check` exit 0."
                text = brief(GOAL=CLEAN_GOAL, SCOPE=scope("tests/unit/test_x.py"), ACCEPTANCE=acceptance)
                self.assert_refused_exactly(self.check_text(text), NO_TEST_GATE)

    def test_an_acceptance_with_a_test_gate_alone_is_refused_naming_the_missing_lint_gate(self):
        for test_gate in TEST_GATES:
            with self.subTest(test=test_gate):
                acceptance = f"1. {test_gate}\n2. `make validate-agent-assets` exit 0."
                text = brief(GOAL=CLEAN_GOAL, SCOPE=scope("AGENTS.md"), ACCEPTANCE=acceptance)
                self.assert_refused_exactly(self.check_text(text), NO_LINT_GATE)
        # Neither class named: one line per class, after the other reasons of the same run.
        text = brief(GOAL="A shell reader.", SCOPE=scope(*THREE_LEVERS), ACCEPTANCE="1. `make shellcheck` exit 0.")
        self.assert_refused(
            self.check_text(text),
            'GOAL holds "shell" (',
            'GOAL holds "shell"; no TRUST section',
            SPLIT_REASON,
            NO_LINT_GATE,
            NO_TEST_GATE,
        )

    def test_a_records_brief_naming_its_own_check_under_python3_isolated_passes_as_the_test_gate(self):
        # U280: `python3 -I <path>/check-<name>.py` is the test gate of a brief that changes no repository file; the
        # lint gate stays required (the store's markdown is synced into the repository, where prettier runs).
        for check in (
            "`python3 -I tests/check-tables.py` exit 0.",
            "`python3 -I tests/check-tables.py`",
            "python3 -I tests/check-tables.py",
            "`python3 -I U0-tables/check-tables.py U0-tables/*.tsv` exit 0 and its row counts per table pasted.",
            "`python3 -I /tmp/dotfiles-wt/U0-tables/check-rows.py` exit 0.",
            "`python3 -I check-x.py` exit 0.",
        ):
            with self.subTest(check=check):
                text = brief(GOAL=CLEAN_GOAL, SCOPE=RECORDS_SCOPE, ACCEPTANCE=f"1. {check}\n2. {RECORDS_LINT}")
                self.assert_passes(self.check_text(text))
        text = brief(GOAL=CLEAN_GOAL, SCOPE=RECORDS_SCOPE, ACCEPTANCE="1. `python3 -I tests/check-tables.py` exit 0.")
        self.assert_refused_exactly(self.check_text(text), NO_LINT_GATE)

    def test_a_check_script_run_without_the_isolated_flag_or_not_named_check_is_no_test_gate(self):
        # The same brief with `python3 tests/check-tables.py` (no `-I`) is refused with the test-gate line; so is a
        # lower-case `-i` (the interactive interpreter), a script not named `check-*.py`, and a `check-` directory.
        for check in (
            "`python3 tests/check-tables.py` exit 0.",
            "`python3 -i tests/check-tables.py` exit 0.",
            "`python3 -I tests/tables.py` exit 0.",
            "`python3 -I tests/check-tables.sh` exit 0.",
            "`python3 -I check-tables/run.py` exit 0.",
            "`python -I tests/check-tables.py` exit 0.",
        ):
            with self.subTest(check=check):
                text = brief(GOAL=CLEAN_GOAL, SCOPE=RECORDS_SCOPE, ACCEPTANCE=f"1. {check}\n2. {RECORDS_LINT}")
                self.assert_refused_exactly(self.check_text(text), NO_TEST_GATE)

    def test_a_check_script_whose_name_goes_on_after_py_is_no_test_gate(self):
        # U280b (round-1 P2, thread 4492381429): the term ends at `.py` followed by the end of the text, whitespace or
        # a closing backtick, so a `.bak` or `.sh` suffix and `check-tables.py` as a directory name are no gate.
        for check in (
            "`python3 -I tests/check-tables.py.bak` exit 0.",
            "`python3 -I tests/check-tables.py.sh` exit 0.",
            "`python3 -I check-tables.py/run.py` exit 0.",
        ):
            with self.subTest(check=check):
                text = brief(GOAL=CLEAN_GOAL, SCOPE=RECORDS_SCOPE, ACCEPTANCE=f"1. {check}\n2. {RECORDS_LINT}")
                self.assert_refused_exactly(self.check_text(text), NO_TEST_GATE)

    def test_a_sweep_shaped_scope_with_no_repository_path_needs_no_gate(self):
        # The U248 sweep shape, writing under ~/.local/state alone, and every other span that is no repository path:
        # an absolute path, a path beside the tree, a `$VAR` path, a bare word, a command span, prose, nothing.
        sweep = (
            "No branch, no commit, no pull request, no file of the repository changes. Writes only under "
            "`~/.local/state/omp-seats/dotfiles/.state/sweep/security-audit/run-54/` and the skill's per-agent "
            "`scratch/` directories below it; the target is `~/.local/state/omp-seats/dotfiles/sweep`, read-only."
        )
        for body in (
            sweep,
            "Writes `/tmp/x/out.md`, `../U0-pr-body.md`, `$HOME/.cache/x`, `Makefile`, `.github/` and `~`.",
            "`ls scripts/ci/run-bats.sh AGENTS.md`; scripts/ci/run-bats.sh and AGENTS.md in prose.",
            "",
        ):
            with self.subTest(scope=body[:40]):
                self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=body, ACCEPTANCE="1. The report.")))
                self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=body)))
        self.assert_passes(self.check_text(brief(GOAL=CLEAN_GOAL, ACCEPTANCE="1. The report pasted.")))

    def test_a_repository_path_in_scope_without_an_acceptance_section_is_refused(self):
        # Two or more names, a directory, a `./` prefix, one file with an extension; a branch ref reads as a path too,
        # so every brief that names its branch is held to the rule (a sweep brief names none).
        for path in (
            "scripts/ci/run-bats.sh",
            "home/dot_dsh/plugins/omp-gateway/",
            "./AGENTS.md",
            "docs/README.md",
            "origin/main",
        ):
            with self.subTest(path=path):
                result = self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=f"May write: `{path}`."))
                self.assert_refused_exactly(result, "no ACCEPTANCE section")
        # An ACCEPTANCE section that is present and empty names no gate: the two class lines, not the section line.
        result = self.check_text(brief(GOAL=CLEAN_GOAL, SCOPE=scope("AGENTS.md"), ACCEPTANCE=""))
        self.assert_refused_exactly(result, NO_LINT_GATE, NO_TEST_GATE)

    def checkout_check(self, manifest_text, text):
        """Run a checkout-shaped copy of the script beside a scratch manifest; returns (result, manifest as named)."""
        checkout = self.dir / "checkout"
        if not checkout.exists():
            (checkout / "scripts/orchestrator").mkdir(parents=True)
            (checkout / "home/dot_agents").mkdir(parents=True)
            shutil.copy2(SCRIPT, checkout / "scripts/orchestrator/brief-check.py")
        (checkout / "home/dot_agents/agent-config.yaml").write_text(manifest_text)
        target = self.dir / "U0-scratch.md"
        target.write_text(text)
        physical = (checkout / "scripts/orchestrator").resolve()
        cmd = [sys.executable, "-I", str(checkout / "scripts/orchestrator/brief-check.py"), str(target)]
        result = subprocess.run(cmd, cwd=self.dir, capture_output=True, text=True, timeout=120, check=False)
        return result, f"{physical}/../../home/dot_agents/agent-config.yaml"

    def assert_refused_to_run(self, result, named, message):
        """Exit 2, the refusal naming the scratch manifest on stderr, nothing on stdout: no judgement escaped."""
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertIn(f"brief-check.py: refused: {message} {named}", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_a_checkout_manifest_without_the_levers_block_or_unreadable_refuses_before_any_judgement(self):
        text = MANIFEST.read_text()
        self.assertEqual(1, text.count("\n  levers:\n"))
        gone = text.replace("\n  levers:\n", "\n  levers_gone:\n")
        result, named = self.checkout_check(gone, brief(GOAL=CLEAN_GOAL))
        self.assert_refused_to_run(result, named, "no claude.levers.sha256 block in")
        if os.geteuid() == 0:
            self.skipTest("mode 000 does not stop root, so the unreadable-manifest case is skipped")
        manifest = self.dir / "checkout/home/dot_agents/agent-config.yaml"
        manifest.write_text(text)
        manifest.chmod(0)
        self.addCleanup(manifest.chmod, 0o644)
        cmd = [
            sys.executable,
            "-I",
            str(self.dir / "checkout/scripts/orchestrator/brief-check.py"),
            str(self.dir / "U0-scratch.md"),
        ]
        result = subprocess.run(cmd, cwd=self.dir, capture_output=True, text=True, timeout=120, check=False)
        self.assert_refused_to_run(result, named, "manifest unreadable:")

    def test_a_levers_block_under_another_key_is_not_the_lever_list(self):
        # U136 (U130 verdict :109): an unrelated `levers:` / `sha256:` block before `claude:`, with `claude.levers`
        # absent, was read as the lever list, so the three-lever brief passed; the reader takes the block under
        # `claude:` alone and refuses to run without it.
        text = MANIFEST.read_text()
        unrelated = "other:\n  levers:\n    sha256:\n      foo: " + "0" * 64 + "\n      bar: " + "1" * 64 + "\n"
        self.assertEqual(1, text.count("\nclaude:\n"))
        planted = text.replace("\n  levers:\n", "\n  levers_gone:\n").replace("\nclaude:\n", f"\n{unrelated}claude:\n")
        result, named = self.checkout_check(
            planted, brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS), ACCEPTANCE=GATED)
        )
        self.assert_refused_to_run(result, named, "no claude.levers.sha256 block in")
        # The same unrelated block beside an intact `claude.levers` changes nothing: the three levers are counted.
        result, _ = self.checkout_check(
            text.replace("\nclaude:\n", f"\n{unrelated}claude:\n"),
            brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS), ACCEPTANCE=GATED),
        )
        self.assert_refused_exactly(result, SPLIT_REASON)

    def test_a_comment_and_a_blank_line_between_pins_end_nothing(self):
        # U136 (U130 verdict :114): a YAML comment or a blank line after the first pin ended the list, so a
        # three-lever brief passed against a one-lever list; every pin after them still counts.
        text = MANIFEST.read_text()
        first = next(line for line in text.splitlines() if line.startswith("      hcom-seat: "))
        for gap in ("      # a comment about the next pin\n\n", "\n# a column-0 comment\n   \n"):
            with self.subTest(gap=gap.strip() or "blank"):
                spaced = text.replace(first + "\n", first + "\n" + gap)
                result, _ = self.checkout_check(
                    spaced, brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS), ACCEPTANCE=GATED)
                )
                self.assert_refused_exactly(result, SPLIT_REASON)
                result, _ = self.checkout_check(
                    spaced, brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS[:2]), ACCEPTANCE=GATED)
                )
                self.assert_passes(result)

    def test_a_malformed_pin_line_in_the_block_refuses_naming_the_line(self):
        text = MANIFEST.read_text()
        lines = text.splitlines()
        number = next(index for index, line in enumerate(lines, 1) if line.startswith("      hcom-dispatch: "))
        malformed_lines = (
            "      hcom-dispatch: not-a-digest",
            "      hcom-dispatch " + "0" * 64,
            "        hcom-dispatch: " + "0" * 64,
        )
        for malformed in malformed_lines:
            with self.subTest(line=malformed.strip()):
                broken = "\n".join(lines[: number - 1] + [malformed] + lines[number:]) + "\n"
                result, named = self.checkout_check(broken, brief(GOAL=CLEAN_GOAL))
                self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
                self.assertIn(
                    f"brief-check.py: refused: line {number} of {named} is not a `<name>: <sha256>` pin",
                    result.stderr,
                )
                self.assertNotIn("Traceback", result.stderr)
        # The list ends at the first line indented less than its entries: a key at the `sha256:` depth before the
        # first pin leaves the block empty, and the pins after it are not read as the list.
        first = number - 2
        self.assertTrue(lines[first].startswith("      hcom-seat: "), lines[first])
        shorter = "\n".join(lines[:first] + ["    extensions_gone:", "      - x"] + lines[first:]) + "\n"
        result, named = self.checkout_check(
            shorter, brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS), ACCEPTANCE=GATED)
        )
        self.assert_refused_to_run(result, named, "no claude.levers.sha256 block in")

    def test_a_manifest_missing_the_block_and_the_pin_names_the_block(self):
        # U136 (U130 verdict :103): with both gone the pin refusal came first; the block is checked before the pin.
        text = MANIFEST.read_text()
        pin = next(line for line in text.splitlines() if line.startswith("      brief-check.py: "))
        both_gone = text.replace("\n  levers:\n", "\n  levers_gone:\n").replace(pin + "\n", "")
        result, named = self.checkout_check(both_gone, brief(GOAL=CLEAN_GOAL))
        self.assert_refused_to_run(result, named, "no claude.levers.sha256 block in")
        self.assertNotIn("no single sha256 pin", result.stderr)
        # The block intact and the pin gone is still the pin refusal.
        result, named = self.checkout_check(text.replace(pin + "\n", ""), brief(GOAL=CLEAN_GOAL))
        self.assert_refused_to_run(result, named, "no single sha256 pin for brief-check.py in")

    def test_every_pin_at_another_consistent_indentation_passes_the_self_check_and_counts_every_lever(self):
        # Round 2 (audit P2 :116): the block reader took every pin at eight spaces while a separate six-space read of
        # the self pin refused the same manifest; the self pin is the block's `brief-check.py` entry, read by the
        # one rule, so any indentation deeper than `sha256:` that every pin shares reads the list and the pin alike.
        lines = MANIFEST.read_text().splitlines()
        block = lines.index("    sha256:", lines.index("  levers:", lines.index("claude:"))) + 1
        end = next(index for index in range(block, len(lines)) if not lines[index].startswith("      "))
        self.assertGreaterEqual(end - block, 3, lines[block:end])
        for width in (5, 8, 12):
            with self.subTest(spaces=width):
                pins = [" " * width + line.lstrip(" ") for line in lines[block:end]]
                spaced = "\n".join(lines[:block] + pins + lines[end:]) + "\n"
                result, _ = self.checkout_check(
                    spaced, brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS), ACCEPTANCE=GATED)
                )
                self.assert_refused_exactly(result, SPLIT_REASON)
                result, _ = self.checkout_check(
                    spaced, brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS[:2]), ACCEPTANCE=GATED)
                )
                self.assert_passes(result)
        # A pin of this lever outside the block is not the pin: at six spaces under another key, with the block's
        # entry gone, the refusal is the absent pin, not a match on indentation.
        text = "\n".join(lines) + "\n"
        pin = next(line for line in lines if line.startswith("      brief-check.py: "))
        elsewhere = text.replace(pin + "\n", "").replace(
            "\nclaude:\n", f"\nother:\n  levers:\n    sha256:\n{pin}\nclaude:\n"
        )
        result, named = self.checkout_check(elsewhere, brief(GOAL=CLEAN_GOAL))
        self.assert_refused_to_run(result, named, "no single sha256 pin for brief-check.py in")


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

    def test_the_installed_copy_counts_levers_from_the_deployed_manifest(self):
        result = self.run_skill_command(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS), ACCEPTANCE=GATED))
        self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
        expected = [f"brief-check: .orchestration/orchestrate/p/briefs/U1-x.md: {SPLIT_REASON}"]
        self.assertEqual(expected, result.stdout.splitlines())
        result = self.run_skill_command(brief(GOAL=CLEAN_GOAL, SCOPE=scope(*THREE_LEVERS[:2]), ACCEPTANCE=GATED))
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def test_a_deployed_manifest_without_the_levers_block_refuses(self):
        text = self.manifest.read_text()
        self.assertEqual(1, text.count("\n  levers:\n"))
        self.manifest.write_text(text.replace("\n  levers:\n", "\n  levers_gone:\n"))
        result = self.run_skill_command(brief(GOAL=CLEAN_GOAL))
        self.assert_refused(result, f"no claude.levers.sha256 block in {self.manifest}")

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


# U436: the store's `units.tsv` as the id register, its header as the store writes it, and one row as the store writes
# one (eight cells; the brief cell is `briefs/<file>`, relative to the store, empty for some rows).
UNITS_HEADER = "id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote"


def unit_row(unit_id, brief_cell, *, cells=8):
    """One `units.tsv` row holding `unit_id` and `brief_cell`, padded or cut to `cells` columns (a malformed row)."""
    row = [unit_id, "fix", "done", "fix/x", "1", "0" * 40, brief_cell, "a note"]
    return "\t".join((row + ["extra"] * cells)[:cells])


def units(*rows, header=UNITS_HEADER):
    """A `units.tsv` text: the header, then each row, one per line."""
    return "\n".join((header, *rows)) + "\n"


class TakenUnitIdTest(unittest.TestCase):
    """A brief whose unit id another row of the store's `units.tsv` holds is refused (regime-cutover U436).

    2026-11-11: the coordinator numbered a new unit U345 while `units.tsv` held U345 as a done sweep unit; the check
    passed the brief, the unit ran for an hour, and pr-audit.sh refused at the pull request because two briefs
    matched `briefs/U345-*.md`. The fixture is a scratch store: `<store>/briefs/<file>` beside `<store>/units.tsv`.
    """

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.store = self.dir / "store"
        self.briefs = self.store / "briefs"
        self.briefs.mkdir(parents=True)
        self.units = self.store / "units.tsv"

    def check(self, rows, name="U7-x.md", text=None):
        """Run the checkout script on `<store>/briefs/<name>` beside a `units.tsv` of `rows` (None writes no file)."""
        if rows is not None:
            self.units.write_text(rows)
        target = self.briefs / name
        target.write_text(brief(GOAL=CLEAN_GOAL) if text is None else text)
        cmd = [sys.executable, "-I", str(SCRIPT), str(target)]
        return subprocess.run(cmd, cwd=self.dir, capture_output=True, text=True, timeout=120, check=False)

    def taken(self, unit_id, line, cell, name="U7-x.md"):
        """The one refusal line: the id, the row's line in the store's file and its brief cell, and this file's path."""
        held = f'brief cell "{cell}"' if cell else "an empty brief cell"
        return (
            f"brief-check: {self.briefs / name}: unit id {unit_id} is taken: line {line} of {self.units} holds it "
            f"with {held}, not briefs/{name}"
        )

    def assert_passes(self, result):
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def assert_refused_exactly(self, result, *lines):
        self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
        self.assertEqual(list(lines), result.stdout.splitlines())

    def assert_cannot_read(self, result, message):
        """Exit 2, nothing on stdout, the store file named on stderr: a store the check cannot read is never a pass."""
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertEqual(f"brief-check: cannot read {self.units}: {message}\n", result.stderr)

    def test_a_row_holding_the_id_with_another_file_refuses_naming_the_row_and_its_brief_cell(self):
        rows = units(unit_row("U6", "briefs/U6-a.md"), unit_row("U7", "briefs/U7-other.md"))
        self.assert_refused_exactly(self.check(rows), self.taken("U7", 3, "briefs/U7-other.md"))
        # The rule is equality with this file's store-relative path: the pre-move spelling of the same file, the bare
        # file name and a path differing in case are other paths, and a letter suffix is another id in both directions.
        for cell in ("orchestrate/p/briefs/U7-x.md", "U7-x.md", "briefs/U7-X.md", "briefs/U7-x.md "):
            with self.subTest(cell=cell):
                self.assert_refused_exactly(self.check(units(unit_row("U7", cell))), self.taken("U7", 2, cell))
        rows = units(unit_row("U7", "briefs/U7-x.md"), unit_row("U7b", "briefs/U7b-other.md"))
        self.assert_refused_exactly(
            self.check(rows, name="U7b-x.md"), self.taken("U7b", 3, "briefs/U7b-other.md", name="U7b-x.md")
        )
        # Every row is read, not the first with the id: a second row of a duplicated id naming another file refuses.
        rows = units(
            unit_row("U7", "briefs/U7-x.md"), unit_row("U8", "briefs/U8-a.md"), unit_row("U7", "briefs/U7-y.md")
        )
        self.assert_refused_exactly(self.check(rows), self.taken("U7", 4, "briefs/U7-y.md"))

    def test_a_row_holding_the_id_with_this_file_passes(self):
        rows = units(unit_row("U6", "briefs/U6-a.md"), unit_row("U7", "briefs/U7-x.md"), unit_row("U8", ""))
        self.assert_passes(self.check(rows))
        self.assert_passes(self.check(units(unit_row("U7b", "briefs/U7b-x.md")), name="U7b-x.md"))

    def test_an_id_with_no_row_passes_and_a_file_without_an_id_is_not_looked_up(self):
        rows = units(unit_row("U6", "briefs/U6-a.md"), unit_row("U70", "briefs/U70-a.md"), unit_row("U7b", ""))
        self.assert_passes(self.check(rows))
        self.assert_passes(self.check(units()))
        # A file whose name starts with no `U<n>` or `U<n><letter>` id names no unit, so no row is looked up.
        for name in ("F1-x.md", "O2-addendum.md", "README.md", "U7.md", "u7-x.md", "U7B-x.md"):
            with self.subTest(name=name):
                self.assert_passes(self.check(units(unit_row("U7", "briefs/U7-other.md")), name=name))

    def test_a_row_holding_the_id_with_an_empty_brief_cell_refuses_the_id_as_taken(self):
        self.assert_refused_exactly(self.check(units(unit_row("U7", ""))), self.taken("U7", 2, ""))
        # The refusal stands beside the other reasons of the same run, first, so one run names every fault.
        result = self.check(units(unit_row("U7", "")), text=brief(GOAL="A shell reader."))
        self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
        lines = result.stdout.splitlines()
        self.assertEqual(3, len(lines), result.stdout)
        self.assertEqual(self.taken("U7", 2, ""), lines[0])
        self.assertIn('GOAL holds "shell" (', lines[1])
        self.assertIn('GOAL holds "shell"; no TRUST section', lines[2])

    def test_a_units_file_with_a_wrong_header_a_short_or_long_row_or_unreadable_refuses_naming_the_line(self):
        # Standing order 21: a store read that fails is a refusal naming the file, never a pass; nothing is judged.
        header = "id, track, state, branch, pr, head_sha, brief, note"
        for text, message in (
            (
                units(unit_row("U6", "briefs/U6-a.md"), header="id\ttrack\tstate"),
                f"line 1 is not the header ({header})",
            ),
            (
                units(header="unit\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote"),
                f"line 1 is not the header ({header})",
            ),
            ("", f"line 1 is not the header ({header})"),
            (
                units(unit_row("U6", "briefs/U6-a.md"), unit_row("U7", "briefs/U7-x.md", cells=5)),
                "line 3 has 5 columns, not 8",
            ),
            (units(unit_row("U6", "briefs/U6-a.md", cells=9)), "line 2 has 9 columns, not 8"),
            (
                units(unit_row("U6", "briefs/U6-a.md"), "", unit_row("U7", "briefs/U7-x.md")),
                "line 3 has 1 columns, not 8",
            ),
        ):
            with self.subTest(text=text[:60]):
                self.assert_cannot_read(self.check(text), message)
        # A header-only file with no trailing newline is the header alone, a sound register with no row.
        self.assert_passes(self.check(UNITS_HEADER))
        self.units.unlink()
        self.units.mkdir()
        result = self.check(None)
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertTrue(result.stderr.startswith(f"brief-check: cannot read {self.units}: "), result.stderr)
        self.units.rmdir()
        self.units.write_bytes(b"id\ttrack\xff\xfe\n")
        result = self.check(None)
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertTrue(result.stderr.startswith(f"brief-check: cannot read {self.units}: "), result.stderr)
        if os.geteuid() == 0:
            self.skipTest("mode 000 does not stop root, so the unreadable-register case is skipped")
        self.units.write_text(units(unit_row("U7", "briefs/U7-x.md")))
        self.units.chmod(0)
        self.addCleanup(self.units.chmod, 0o644)
        result = self.check(None)
        self.assertEqual((2, ""), (result.returncode, result.stdout), result.stderr)
        self.assertTrue(result.stderr.startswith(f"brief-check: cannot read {self.units}: "), result.stderr)

    def test_a_store_without_a_units_file_and_a_brief_outside_a_store_pass_printing_nothing(self):
        # The existing tests' form: a scratch brief outside any store passes with nothing on either stream, so a
        # `briefs/` directory with no `units.tsv` beside it is no register and prints no note either.
        self.assertFalse(self.units.exists())
        self.assert_passes(self.check(None))
        for target in (self.dir / "U7-x.md", self.dir / "other/U7-x.md", self.store / "U7-x.md"):
            with self.subTest(target=str(target.relative_to(self.dir))):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(brief(GOAL=CLEAN_GOAL))
                cmd = [sys.executable, "-I", str(SCRIPT), str(target)]
                self.assert_passes(
                    subprocess.run(cmd, cwd=self.dir, capture_output=True, text=True, timeout=120, check=False)
                )
        # A `units.tsv` outside the `briefs/` directory's parent is not the store's: a brief whose directory is not
        # named `briefs` has no store, even beside such a file.
        (self.dir / "units.tsv").write_text(units(unit_row("U7", "briefs/U7-other.md")))
        cmd = [sys.executable, "-I", str(SCRIPT), str(self.dir / "U7-x.md")]
        self.assert_passes(subprocess.run(cmd, cwd=self.dir, capture_output=True, text=True, timeout=120, check=False))
        # The relative spelling the SKILL command uses locates the same register.
        self.units.write_text(units(unit_row("U7", "briefs/U7-other.md")))
        (self.briefs / "U7-x.md").write_text(brief(GOAL=CLEAN_GOAL))
        cmd = [sys.executable, "-I", str(SCRIPT), "store/briefs/U7-x.md"]
        result = subprocess.run(cmd, cwd=self.dir, capture_output=True, text=True, timeout=120, check=False)
        self.assertEqual((1, ""), (result.returncode, result.stderr), result.stdout)
        self.assertEqual(
            [
                "brief-check: store/briefs/U7-x.md: unit id U7 is taken: line 2 of store/units.tsv holds it with "
                'brief cell "briefs/U7-other.md", not briefs/U7-x.md'
            ],
            result.stdout.splitlines(),
        )


if __name__ == "__main__":
    unittest.main()
