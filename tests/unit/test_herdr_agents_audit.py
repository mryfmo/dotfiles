#!/usr/bin/env python3
"""Exercise the task-level audit: the herdr-agents prompt and warning, and scripts/audit-head.sh (T126 INV-4)."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT_HEAD = ROOT / "scripts/audit-head.sh"
HARNESS_PATH = Path(__file__).resolve().parent / "test_herdr_agents.py"
# Loaded under a private name and never bound as a class here, so discovery
# does not collect the harness's own tests a second time.
_spec = importlib.util.spec_from_file_location("herdr_agents_audit_harness", HARNESS_PATH)
assert _spec and _spec.loader
_harness = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_harness)

GRAMMAR = (
    "`[P<0-3>] <high|medium|low> <specification|implementation|evidence|orchestration|conformance> "
    "<path:line|-> <rationale>`"
)
CATEGORIES = ("specification (", "implementation (", "evidence (", "orchestration (", "conformance (")
FORMAT_2_TASK = "---\nformat: 2\ntask_id: T1\nkind: code\ninvariants:\n  INV-1: x\n---\n# T1\n"
INVARIANT_RULE = "write one line per invariant id of the task front matter, `INV-n: holds|violated <path:line>`"
COUNT_RULE = "then the line `Orchestration findings: <count>`"
INV_WARNING = "WARN: herdr-agents: format 2 task T1: the audit output has no INV-n: holds|violated line."
COUNT_WARNING = "WARN: herdr-agents: format 2 task T1: the audit output has no Orchestration findings: line."


class HerdrAgentsAuditTest(_harness.HerdrAgentsTest):
    def audit_task(self, task: str = "x\n", last: str = "Verdict: correct\n", *extra: str):
        """Run `--audit <head> --task T1` with the given task file, last message and extra .orchestration files."""
        self.write_audit_pair_state(self.audit_tab_pane())
        _, head = self.write_task_audit_repo()
        orchestration = self.workdir.resolve() / ".orchestration"
        for path, text in (("tasks/T1.md", task), *((name, "x\n") for name in extra)):
            (orchestration / path).parent.mkdir(parents=True, exist_ok=True)
            (orchestration / path).write_text(text)
        self.write_audit_evidence(last, orchestration / f"validation/T1-audit-{head[:7]}.md.last.md")
        # audit_inner_command reads the first pane run, so each run starts a fresh call log.
        self.calls_path.unlink(missing_ok=True)
        result = self.run_helper("--audit", head, "--task", "T1")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result, self.audit_codex_words(self.audit_inner_command())[-1]

    def test_prompt_states_the_finding_grammar_and_the_five_categories(self) -> None:
        _, prompt = self.audit_task()

        self.assertIn(f"Report each finding on one line in exactly this grammar: {GRAMMAR};", prompt)
        for category in CATEGORIES:
            self.assertIn(category, prompt)
        self.assertNotIn("confidence dimension file:line", prompt)

    def test_prompt_puts_the_orchestrator_artifacts_in_scope(self) -> None:
        _, prompt = self.audit_task()

        self.assertIn(
            "Your scope covers the orchestrator as well as the worker: the task file with its amendments,", prompt
        )
        self.assertIn(
            "the design task file and review receipts the task front matter names under design_review", prompt
        )
        self.assertIn("orchestration (task wording, scope decisions, dispositions or acceptance claims)", prompt)
        self.assertIn("conformance (a deviation from the regime process)", prompt)

    def test_prompt_names_the_acceptance_record_only_when_it_exists(self) -> None:
        _, prompt = self.audit_task()
        self.assertNotIn("acceptance record `", prompt)

        _, prompt = self.audit_task("x\n", "Verdict: correct\n", "acceptance/T1.md")

        self.assertIn(
            "; the acceptance record `.orchestration/acceptance/T1.md` as it stands (earlier rounds' dispositions "
            "and the PR-feedback dispositions); the final head ",
            prompt,
        )

    def test_prompt_names_the_permgate_extract_only_when_present(self) -> None:
        _, prompt = self.audit_task()
        self.assertNotIn("permgate", prompt)

        _, prompt = self.audit_task("x\n", "Verdict: correct\n", "validation/T1-permgate.jsonl")

        self.assertIn(
            "; the permgate decision extract `.orchestration/validation/T1-permgate.jsonl` "
            "(the permission prompts in the task window); the final head ",
            prompt,
        )

    def test_format_2_prompt_requires_the_invariant_lines_and_the_count_before_the_verdict(self) -> None:
        _, prompt = self.audit_task(FORMAT_2_TASK, "INV-1: holds a.py:1\nOrchestration findings: 0\nVerdict: correct\n")

        self.assertIn(f"This is a format 2 task: before the verdict line, {INVARIANT_RULE}, {COUNT_RULE}.", prompt)
        self.assertLess(prompt.index(COUNT_RULE), prompt.index("End your final message"))

    def test_legacy_prompt_has_no_invariant_or_count_requirement(self) -> None:
        for task in ("x\n", "# T1\n\nformat: 2\n", "---\nformat: '2'\n---\n", "---\nkind: code\n---\nformat: 2\n"):
            with self.subTest(task=task):
                _, prompt = self.audit_task(task)

                self.assertNotIn("format 2 task", prompt)
                self.assertNotIn("Orchestration findings", prompt)

    def test_wrapper_warns_when_a_format_2_last_message_lacks_the_lines(self) -> None:
        cases = (
            ("Verdict: correct\n", [INV_WARNING, COUNT_WARNING]),
            ("Orchestration findings: 0\nVerdict: correct\n", [INV_WARNING]),
            ("INV-1: violated a.py:1\nVerdict: correct\n", [COUNT_WARNING]),
        )
        for last, warnings in cases:
            with self.subTest(last=last):
                result, _ = self.audit_task(FORMAT_2_TASK, last)

                self.assertEqual([line for line in result.stderr.splitlines() if "format 2 task" in line], warnings)
                # The warning never changes the verdict-only gate.
                self.assertIn("Audit verdict: correct\n", result.stdout)

    def test_wrapper_is_silent_when_the_lines_are_present_or_the_task_is_legacy(self) -> None:
        for task, last in (
            (
                FORMAT_2_TASK,
                "[P3] low evidence - x\nINV-1: holds a.py:1\nOrchestration findings: 0\nVerdict: correct\n",
            ),
            ("x\n", "Verdict: correct\n"),
        ):
            with self.subTest(task=task):
                result, _ = self.audit_task(task, last)

                self.assertNotIn("format 2 task", result.stderr)


GOOD_DOCUMENT = {
    "verdict": "incorrect",
    "findings": [
        {
            "priority": "P2",
            "confidence": "high",
            "category": "implementation",
            "path": "a.py",
            "line": 3,
            "rationale": "Broken\n  quoting.",
        },
        {
            "priority": "P1",
            "confidence": "medium",
            "category": "orchestration",
            "path": None,
            "line": None,
            "rationale": "The amendment contradicts the design.",
        },
    ],
    "invariants": {"INV-4": {"status": "holds", "path": "a.py", "line": 1, "note": "tested"}},
    "orchestration_findings": 1,
    "not_checked": ["the live run"],
    "summary": "Two findings.",
}
TASK_FILE = (
    '---\nformat: 2\ntask_id: T1\nkind: code\ninvariants:\n  INV-4: "the audit is schema-validated"\n---\n# T1\n'
)


class AuditHeadTest(unittest.TestCase):
    """scripts/audit-head.sh against a scratch repository and fake codex, claude and agmsg scripts."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="audit-head-test-")).resolve()
        self.addCleanup(shutil.rmtree, self.temp, True)
        self.repo = self.temp / "main"
        self.bin = self.temp / "bin"
        self.home = self.temp / "home"
        self.log = self.temp / "calls.log"
        for path in (self.repo, self.bin, self.home / ".agents/skills/agmsg/scripts"):
            path.mkdir(parents=True)
        # Host git config (signing, URL rewrites) must not reach the scratch repository.
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "PATH": f"{self.bin}{os.pathsep}{os.environ['PATH']}",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "TMPDIR": str(self.temp),
        }
        self.env.pop("ANTHROPIC_API_KEY", None)
        self.git("init", "-q", "-b", "main")
        (self.repo / "f.txt").write_text("base\n")
        self.git("add", "f.txt")
        self.git("commit", "-q", "-m", "base")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("switch", "-q", "-c", "pr")
        (self.repo / "f.txt").write_text("head\n")
        self.git("commit", "-q", "-am", "head")
        self.sha = self.git("rev-parse", "HEAD")
        # The orchestrator's checkout sits on main, never at the audited head.
        self.git("switch", "-q", "main")
        self.write(".orchestration/tasks/T1.md", TASK_FILE)
        self.validation = self.repo / ".orchestration/validation"
        self.out = self.validation / f"T1-audit-{self.sha[:7]}.md"
        self.json = self.validation / f"T1-audit-{self.sha[:7]}.json"
        self.last = Path(f"{self.out}.last.md")
        self.worktree = self.repo / f".claude/worktrees/audit-{self.sha[:7]}"
        self.codex_document(GOOD_DOCUMENT)
        self.claude_document(GOOD_DOCUMENT)
        (self.temp / "send-exit").write_text("0\n")
        self.fake(
            "codex",
            f"""
            import json, os, shutil, sys
            args = sys.argv[1:]
            with open({str(self.log)!r}, "a") as log:
                log.write(json.dumps({{"tool": "codex", "cwd": os.getcwd(), "args": args}}) + "\\n")
            shutil.copy(args[args.index("--output-schema") + 1], {str(self.temp / "codex-schema.json")!r})
            if os.path.exists({str(self.temp / "codex.json")!r}):
                shutil.copy({str(self.temp / "codex.json")!r}, args[args.index("-o") + 1])
            print("codex transcript")
            sys.exit(int(open({str(self.temp / "codex-exit")!r}).read()) if os.path.exists({str(self.temp / "codex-exit")!r}) else 0)
            """,
        )
        self.fake(
            "claude",
            f"""
            import json, os, sys
            with open({str(self.log)!r}, "a") as log:
                log.write(json.dumps({{"tool": "claude", "cwd": os.getcwd(), "args": sys.argv[1:]}}) + "\\n")
            print(open({str(self.temp / "claude.json")!r}).read())
            """,
        )
        scripts = self.home / ".agents/skills/agmsg/scripts"
        for name, body in {
            "identities.sh": f'[[ $1 == {self.repo} && $2 == claude-code ]] && printf "team1\\tclaude-deep-dot\\n"; exit 0',
            "join.sh": f'printf "join %s\\n" "$*" >> {self.log}',
            "send.sh": (
                f"last=no; [[ -e {self.last} ]] && last=yes; "
                f'printf "send %s %s %s last_exists=%s body=%s\\n" "$1" "$2" "$3" "$last" "$(cat "$5")" >> {self.log}; '
                f'exit "$(cat {self.temp / "send-exit"})"'
            ),
            "reset.sh": f'printf "reset %s\\n" "$*" >> {self.log}',
        }.items():
            (scripts / name).write_text(f"#!/usr/bin/env bash\n{body}\n")
            (scripts / name).chmod(0o755)

    def git(self, *args: str, cwd: Path | None = None) -> str:
        return subprocess.run(
            ["git", "-C", str(cwd or self.repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
            check=True,
            capture_output=True,
            text=True,
            env=self.env,
        ).stdout.strip()

    def write(self, relative: str, text: str) -> Path:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def fake(self, name: str, source: str) -> None:
        path = self.bin / name
        path.write_text("#!/usr/bin/env python3\n" + textwrap.dedent(source))
        path.chmod(0o755)

    def codex_document(self, document: dict | None) -> None:
        path = self.temp / "codex.json"
        if document is None:
            path.unlink(missing_ok=True)
        else:
            path.write_text(json.dumps(document))

    def claude_document(self, document: dict) -> None:
        (self.temp / "claude.json").write_text(json.dumps({"type": "result", "structured_output": document}))

    def run_audit(self, *extra: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(AUDIT_HEAD), self.sha[:7], "--task", "T1", *extra],
            cwd=self.repo,
            env={**self.env, **(env or {})},
            check=False,
            capture_output=True,
            text=True,
        )

    def lines(self) -> list[str]:
        return self.log.read_text().splitlines() if self.log.exists() else []

    def calls(self) -> list[dict]:
        """The fake codex and claude invocations, in order."""
        return [json.loads(line) for line in self.lines() if line.startswith("{")]

    def agmsg_calls(self) -> list[str]:
        """The fake agmsg script invocations, in order."""
        return [line for line in self.lines() if not line.startswith("{")]

    def test_a_schema_valid_codex_document_is_rendered_and_exits_by_verdict(self) -> None:
        result = self.run_audit()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        digest = hashlib.sha256(self.json.read_bytes()).hexdigest()
        self.assertEqual(
            self.last.read_text(),
            f"<!-- audit-head v1 task=T1 head={self.sha} auditor=codex sha256={digest} json={self.json.name} -->\n"
            "[P2] high implementation a.py:3 Broken quoting.\n"
            "[P1] medium orchestration - The amendment contradicts the design.\n"
            "INV-4: holds a.py:1 tested\n"
            "Orchestration findings: 1\n"
            "Not checked: the live run\n"
            "Summary: Two findings.\n"
            "Verdict: incorrect\n",
        )
        self.assertIn("codex transcript", self.out.read_text())
        self.assertIn("Audit verdict: incorrect\n", result.stdout)
        self.assertEqual([call["tool"] for call in self.calls()], ["codex"])
        for verdict, code in (("correct", 0), ("blocked", 2)):
            with self.subTest(verdict=verdict):
                self.codex_document({**GOOD_DOCUMENT, "verdict": verdict})

                result = self.run_audit()

                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertTrue(self.last.read_text().endswith(f"Verdict: {verdict}\n"))

    def test_the_schema_rejects_a_bad_codex_document_and_the_claude_fallback_runs(self) -> None:
        cases = {
            "$: missing not_checked": {k: v for k, v in GOOD_DOCUMENT.items() if k != "not_checked"},
            "$.findings[0].category: 'style' is not one of": {
                **GOOD_DOCUMENT,
                "findings": [{**GOOD_DOCUMENT["findings"][0], "category": "style"}],
            },
            "$.invariants.INV-4.status: 'unknown' is not one of": {
                **GOOD_DOCUMENT,
                "invariants": {"INV-4": {**GOOD_DOCUMENT["invariants"]["INV-4"], "status": "unknown"}},
            },
            "$.invariants: missing INV-4": {**GOOD_DOCUMENT, "invariants": {}},
            "$: unexpected key extra": {**GOOD_DOCUMENT, "extra": 1},
        }
        for message, document in cases.items():
            with self.subTest(message=message):
                self.log.unlink(missing_ok=True)
                self.codex_document(document)

                result = self.run_audit()

                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(f"the codex document does not match the schema: {message}", result.stderr)
                self.assertEqual([call["tool"] for call in self.calls()], ["codex", "claude"])
                self.assertIn(" auditor=claude ", self.last.read_text().splitlines()[0])

    def test_a_failing_codex_runs_the_claude_fallback_under_user_settings_only(self) -> None:
        (self.temp / "codex-exit").write_text("1\n")
        self.codex_document(None)

        result = self.run_audit()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("codex exited non-zero; falling back to claude -p", result.stderr)
        claude = self.calls()[-1]
        self.assertEqual((claude["tool"], claude["cwd"]), ("claude", str(self.worktree)))
        args = claude["args"]
        self.assertEqual(args[0], "-p")
        self.assertNotIn("--bare", args)
        for flag, value in (
            ("--setting-sources", "user"),
            ("--permission-mode", "plan"),
            ("--output-format", "json"),
            ("--max-budget-usd", "5"),
            ("--add-dir", str(self.repo / ".orchestration")),
        ):
            self.assertEqual(args[args.index(flag) + 1], value, flag)
        self.assertIn("--strict-mcp-config", args)
        schema = json.loads(args[args.index("--json-schema") + 1])
        self.assertEqual(schema["properties"]["invariants"]["required"], ["INV-4"])
        self.assertIn("Audit auditor: claude\n", result.stdout)
        self.assertIn(" auditor=claude ", self.last.read_text().splitlines()[0])
        self.assertIn("auditor=claude", self.agmsg_calls()[1])
        self.assertIn("join team1 claude-audit-dot-h001 claude-code ", self.agmsg_calls()[0])

        result = self.run_audit(env={"ANTHROPIC_API_KEY": "x"})

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(self.calls()[-1]["args"][:2], ["-p", "--bare"])

    def test_no_schema_valid_document_from_either_auditor_records_no_audit(self) -> None:
        (self.temp / "codex-exit").write_text("1\n")
        self.claude_document({"verdict": "correct"})

        result = self.run_audit()

        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn("the claude document is unusable either ($: missing findings)", result.stderr)
        self.assertFalse(self.json.exists() or self.last.exists())
        self.assertEqual(self.agmsg_calls(), [])

    def test_the_per_task_schema_lists_the_task_invariants_and_has_no_open_map(self) -> None:
        self.assertEqual(self.run_audit().returncode, 1)
        schema = json.loads((self.temp / "codex-schema.json").read_text())
        invariants = schema["properties"]["invariants"]
        self.assertEqual((invariants["required"], list(invariants["properties"])), (["INV-4"], ["INV-4"]))
        self.assertIs(invariants["additionalProperties"], False)
        self.assertNotIn("$defs", schema)

        self.write(".orchestration/tasks/T1.md", "# legacy task, no front matter\n")
        self.codex_document({**GOOD_DOCUMENT, "invariants": {}})

        self.assertEqual(self.run_audit().returncode, 1)
        invariants = json.loads((self.temp / "codex-schema.json").read_text())["properties"]["invariants"]
        self.assertEqual((invariants["required"], invariants["properties"]), ([], {}))

    def test_the_sha256_record_is_sent_before_the_verdict_is_rendered(self) -> None:
        result = self.run_audit()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        digest = hashlib.sha256(self.json.read_bytes()).hexdigest()
        self.assertEqual(
            self.agmsg_calls(),
            [
                f"join team1 codex-audit-dot-h001 codex {self.worktree}",
                f"send team1 codex-audit-dot-h001 claude-deep-dot last_exists=no "
                f"body=AGMSG-AUDIT v1 task_id=T1 head={self.sha} sha256={digest} auditor=codex",
                f"reset {self.worktree} codex codex-audit-dot-h001",
            ],
        )
        self.assertIn(f"sha256={digest} ", self.last.read_text().splitlines()[0])

        (self.temp / "send-exit").write_text("1\n")
        result = self.run_audit()

        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn("could not send the AGMSG-AUDIT record", result.stderr)
        self.assertFalse(self.last.exists())
        self.assertTrue(self.agmsg_calls()[-1].startswith("reset "))

    def test_the_audit_runs_in_a_detached_worktree_at_the_sha(self) -> None:
        self.assertEqual(self.run_audit().returncode, 1)

        codex = self.calls()[0]
        self.assertEqual(codex["cwd"], str(self.worktree))
        self.assertEqual(codex["args"][codex["args"].index("-C") + 1], str(self.worktree))
        self.assertEqual(codex["args"][:4], ["--profile", "audit", "exec", "--sandbox"])
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=self.worktree), self.sha)
        detached = subprocess.run(
            ["git", "-C", str(self.worktree), "symbolic-ref", "-q", "HEAD"], env=self.env, capture_output=True
        )
        self.assertNotEqual(detached.returncode, 0)
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD"), "main")
        self.assertEqual(self.run_audit().returncode, 1, "a clean worktree at the sha is reused")

        self.git("checkout", "-q", "--detach", "main", cwd=self.worktree)
        result = self.run_audit()

        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn(f"{self.worktree} is not at {self.sha}", result.stderr)
        result = self.run_audit("--worktree", ".")
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn("refusing the orchestrator's checkout", result.stderr)

    def test_the_prompt_names_the_inputs_by_absolute_path_and_the_categories_by_who_fixes(self) -> None:
        self.write(".orchestration/acceptance/T1.md", "x\n")
        self.write(".orchestration/reports/T1.md", "x\n")

        self.assertEqual(self.run_audit().returncode, 1)

        prompt = self.calls()[0]["args"][-1]
        orchestration = self.repo / ".orchestration"
        self.assertIn(f"Inputs: the task file `{orchestration}/tasks/T1.md`; the worker's report `", prompt)
        self.assertIn(f"; the acceptance record `{orchestration}/acceptance/T1.md` as it stands", prompt)
        self.assertIn(f"The rules are the Audit section of `{self.repo}/AGENTS.md`", prompt)
        self.assertIn("orchestration (only the orchestrator:", prompt)
        self.assertIn("conformance (no commit:", prompt)
        self.assertNotIn("permgate", prompt)

    def test_a_held_lock_refuses_a_second_audit_of_the_same_sha(self) -> None:
        self.assertEqual(self.run_audit().returncode, 1)
        common = Path(self.git("rev-parse", "--path-format=absolute", "--git-common-dir"))
        lock = common / "audit-head-locks" / self.sha
        self.assertFalse(lock.exists(), "a finished audit releases its lock")
        lock.mkdir(parents=True)
        self.log.unlink()

        result = self.run_audit()

        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn(f"an audit of {self.sha} is already running", result.stderr)
        self.assertFalse(self.log.exists(), "no auditor and no agmsg call runs")
        self.assertTrue(lock.exists(), "the other run's lock is left alone")

    def test_the_masker_runs_before_the_hash_and_after_the_rendering(self) -> None:
        # A tracked masker that re-serialises JSON, as the repository masker does.
        self.write(
            "scripts/validate-agent-assets.py",
            "import json, sys\n"
            f"open({str(self.temp / 'masked')!r}, 'a').write(' '.join(sys.argv[2:]) + '\\n')\n"
            "for path in sys.argv[2:]:\n"
            "    if path.endswith('.json'):\n"
            "        data = json.load(open(path))\n"
            "        data['summary'] = 'masked'\n"
            "        json.dump(data, open(path, 'w'), indent=4)\n",
        )
        self.git("add", "scripts/validate-agent-assets.py")
        self.git("commit", "-q", "-m", "masker")

        result = self.run_audit()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual((self.temp / "masked").read_text(), f"{self.out} {self.json}\n{self.last}\n")
        digest = hashlib.sha256(self.json.read_bytes()).hexdigest()
        self.assertIn(f"sha256={digest} ", self.agmsg_calls()[1])
        self.assertIn("Summary: masked\n", self.last.read_text())

    def test_the_masker_is_refused_when_the_checkout_is_the_audited_commit(self) -> None:
        # The orchestrator's checkout itself at the audited commit, with a tracked masker.
        self.write("scripts/validate-agent-assets.py", "import sys\nsys.exit(0)\n")
        self.git("add", "scripts/validate-agent-assets.py")
        self.git("commit", "-q", "-m", "validator")
        head = self.git("rev-parse", "HEAD")

        result = subprocess.run(
            ["bash", str(AUDIT_HEAD), head, "--task", "T1"],
            cwd=self.repo,
            env=self.env,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn("refusing the masker", result.stderr)
        self.assertEqual(self.agmsg_calls(), [])
        self.assertFalse(Path(f"{self.validation}/T1-audit-{head[:7]}.md.last.md").exists())


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str | None) -> unittest.TestSuite:
    """Run only this file's tests, not the inherited harness suite."""
    names = sorted(name for name in vars(HerdrAgentsAuditTest) if name.startswith("test_"))
    suite = unittest.TestSuite(HerdrAgentsAuditTest(name) for name in names)
    suite.addTests(loader.loadTestsFromTestCase(AuditHeadTest))
    return suite


if __name__ == "__main__":
    unittest.main()
