"""Exercise scripts/orchestrator/pre-send.sh, the final-byte task preflight (T133 pre-send-check-a01, reset as a02).

The real script, consistency checker and validator are linked into a temporary repository root, so owner records
resolve there and no live record changes. The script's pinned interpreter path, under a temporary HOME, links to
this interpreter; UV_CACHE_DIR keeps the real uv cache, so uv runs offline. Every run's output must be fixed labels
and line numbers only, on both streams. Refused secret and home fixtures are built from fragments.
"""

import ast
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TID = "dotfiles-T999-fixture-a01"
LINKS = ("scripts/orchestrator/pre-send.sh", "scripts/orchestrator/task-consistency-check.py")
LINKS += ("scripts/validate-agent-assets.py",)
LEAK = "=".join(("pass" + "word ", " 'hunt" + "er2x'"))  # the validator's pattern matches only once assembled
TOKEN = hashlib.sha256(b"pre-send fixture").hexdigest()[:30]  # made at run time; no 8-character run may leak
HOMES = ("/Us" + "ers/alice/notes", "see /ho" + "me/bob", "/ro" + "ot/.ssh/id", "/var/ro" + "ot/Library")
GRAMMAR = re.compile(r"[a-z-]+: refused( line\(s\) \d+(,\d+)*)?|sha256: [0-9a-f]{64}")


def validator_pattern():  # this test's own reading of the validator's one assignment, parsed and never run
    tree = ast.parse((ROOT / "scripts/validate-agent-assets.py").read_text())
    names = {n.targets[0].id: n.value for n in tree.body if isinstance(n, ast.Assign) and hasattr(n.targets[0], "id")}
    return re.compile(*map(ast.literal_eval, names["SECRET_PATTERN"].args))


class PreSendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cache = subprocess.run([shutil.which("uv"), "cache", "dir"], capture_output=True, text=True, check=True)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.tmp = Path(temp.name).resolve()
        self.root, home = self.tmp / "repo", self.tmp / "home"
        for rel in LINKS:
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.root / rel).symlink_to(ROOT / rel)
        pinned = home / ".local/share/mise/installs/python/3.15.0/bin/python3"
        pinned.parent.mkdir(parents=True)
        pinned.symlink_to(os.path.realpath(sys.executable))
        self.env = {"PATH": os.environ["PATH"], "HOME": str(home), "TMPDIR": str(self.tmp), "LANG": "C.UTF-8"}
        self.env["UV_CACHE_DIR"] = self.cache.stdout.strip()

    def task(self, body="", items=1, name=TID, front=""):  # the fixture's line 12 is its last Item heading
        text = f"---\nformat: 2\ntask_id: {TID}\nkind: code\nsecurity: false\n{front}allowed_files:\n"
        text += f"  - .orchestration/{TID}/**\n---\n\n# Fixture\n" + "".join(f"\n## Item {i}\n" for i in range(items))
        path = self.tmp / f"{name}.md"
        path.write_text(text + body)
        return path

    def run_send(self, *args):  # every run: labels and numbers only, on both streams
        cmd = ["/bin/bash", str(self.root / LINKS[0]), *map(str, args)]
        result = subprocess.run(cmd, env=self.env, capture_output=True, text=True, timeout=120, check=False)
        self.assertEqual("", result.stderr)
        self.assertTrue(all(GRAMMAR.fullmatch(x) for x in result.stdout.splitlines()), result.stdout)
        return result

    def refused(self, result, reason, lines=None):
        self.assertEqual(1, result.returncode, result.stdout)
        got = result.stdout.splitlines() if lines else [x.split(" line")[0] for x in result.stdout.splitlines()]
        self.assertIn(f"{reason}: refused" + (f" line(s) {lines}" if lines else ""), got)

    def passed(self, path):
        result = self.run_send(path)
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertEqual(f"sha256: {hashlib.sha256(path.read_bytes()).hexdigest()}", result.stdout.splitlines()[-1])

    def test_consistency_refusal(self):
        self.refused(self.run_send(self.task(name="dotfiles-T999-other-a01")), "consistency")

    def test_secret_pattern_matches_validator(self):
        path = self.task(f"\nkeep {LEAK}\npassword: none\n\n## Checks\n\n```\n{LEAK}\n```\n")
        lines = [i for i, line in enumerate(path.read_text().split("\n"), 1) if validator_pattern().search(line)]
        self.assertEqual([14, 20], lines)  # the body line and the last Checks line, not the near miss
        self.refused(self.run_send(path), "secret-pattern", "14,20")

    def test_secret_spanning_two_lines(self):
        path = self.task("\n" + LEAK.replace("= ", "=\n"))
        self.assertFalse(any(map(validator_pattern().search, path.read_text().split("\n"))))
        self.refused(self.run_send(path), "secret-pattern", "14,15")

    def test_literal_home_refusal(self):
        # the validator's pattern: user and root homes on both platforms, a bare home name too (PR #442 4322154981)
        body = f"\n{HOMES[0]}\n$HOME/ok and <home>/ok and /Users/<home>\n{HOMES[1]}\n{HOMES[2]}\n{HOMES[3]}\n"
        self.refused(self.run_send(self.task(body)), "literal-home", "14,16,17,18")
        self.passed(self.task("\n$HOME/ok and <home>/ok\n"))

    def test_self_cap(self):
        for spelling in ("at or under **{} lines**", "at or under {} lines"):
            with self.subTest(spelling=spelling):
                path = self.task(f"\nThis text stays {spelling.format('CAP')}.\n")
                text, n = path.read_text(), path.read_text().count("\n")
                path.write_text(text.replace("CAP", str(n)))
                self.passed(path)  # equal to the cap
                path.write_text(text.replace("CAP", str(n - 1)))
                self.refused(self.run_send(path), "self-cap", "14")  # the declaration's line
        self.passed(self.task("\nNo cap here.\n"))
        path = self.task("\nThis text stays at or under CAP lines.")  # no final newline: wc -l is one under
        path.write_text(path.read_text().replace("CAP", str(path.read_text().count("\n"))))
        self.passed(path)

    def test_fenced_bash_syntax(self):
        sentinel = self.tmp / "sentinel"
        blocks = (f"touch {sentinel}", "if then", "fi )")
        path = self.task("".join(f"\n```bash\n{b}\n```\n" for b in blocks))
        self.refused(self.run_send(path), "bash-syntax", "18,22")  # each failing block's opener
        self.assertFalse(sentinel.exists())  # parsed, never run
        self.passed(self.task(f"\n```bash\n{blocks[0]}\n```\n\n```sh\necho two\n```\n"))
        self.assertFalse(sentinel.exists())

    def fence(self, opener, closer, info):  # a valid block, then a failing one in the given form at line 18
        body = f"\n```sh\necho ok\n```\n\n{opener}{info}\nif then\n{closer}"
        self.refused(self.run_send(self.task(body)), "bash-syntax", "18")

    def test_complete_fences_before_shell_selection(self):
        # a bash-looking example inside a larger non-shell fence is data; attributes on a shell opener still select it
        self.passed(self.task("\n````markdown\n```bash\nif then\n```\n````\n"))
        self.refused(self.run_send(self.task("\n```bash {.example}\nif then\n```\n")), "bash-syntax", "14")

    def test_owner_section_and_rows(self):
        body = f"\nFix the rows under `## Owned by {TID}` in .orchestration/acceptance/r.md.\n"
        record = self.root / ".orchestration/acceptance/r.md"
        record.parent.mkdir(parents=True)
        head = f"## Owned by {TID}"
        cases = [
            (None, 2, True),
            ("# r\n\n## Other\n- x\n", 2, True),
            (f"{head}\n\n## Next\n", 1, True),
            (f"{head} (rows id<TAB>class)\nlocal:abc1234:1\tfix\n", 1, False),
            (f"# r\n\n{head}\n- one bullet\n\n## Next\n", 1, False),
            (f"{head}\n\n## Next\n- outside\nlocal:abc1234:2\tfix\n", 1, True),
            (f"{head}\n\n## Next\n", 2, False),
        ]
        for text, items, refuses in cases:
            with self.subTest(text=text, items=items):
                record.unlink(missing_ok=True)
                if text is not None:
                    record.write_text(text)
                path = self.task(body, items=items)
                if refuses:  # the task's reference line
                    self.refused(self.run_send(path), "owner-section", str(12 + 2 * items))
                else:
                    self.passed(path)

    def test_task_id_yaml_comment(self):
        # local:d067910:3: a trailing YAML comment is no part of task_id, so the owner check still runs
        path = self.task(f"\nFix the rows under `## Owned by {TID}` in .orchestration/acceptance/none.md.\n")
        path.write_text(path.read_text().replace(f"task_id: {TID}\n", f"task_id: {TID} # owner\n"))
        self.refused(self.run_send(path), "owner-section", "14")

    def test_checker_exit_and_line_numbers_only(self):
        # PyYAML marks the open sequence (task line 6) and where its close was due (7); only those numbers are printed
        self.refused(self.run_send(self.task(front="bad: [ unclosed\n")), "consistency", "6,7")

    def test_checker_diagnostics_never_echo_secret_fragments(self):
        # local:d067910:1 and local:09e2e95:1 (P1): a clipped excerpt of a secret-shaped line leaks no 8-character run
        result = self.run_send(self.task(front="bad: [ " + "=".join(("tok" + "en ", f" '{TOKEN}'")) + "\n"))
        self.refused(result, "consistency")
        self.assertFalse([i for i in range(len(TOKEN) - 7) if TOKEN[i : i + 8] in result.stdout + result.stderr])

    def test_output_is_labels_and_numbers_only(self):
        body = f"\n{LEAK}\n{HOMES[0]}\nat or under 3 lines\n\n```bash\nif then\n```\n"
        result = self.run_send(self.task(body, name="dotfiles-T999-other-a01", front=f"bad: [ {TOKEN}\n"))
        self.assertEqual(1, result.returncode)
        for line in result.stdout.splitlines():  # run_send holds both streams to the grammar; no input text at all
            self.assertTrue(GRAMMAR.fullmatch(line) and not any(w in line for w in ("hunt", "alice", TOKEN[:8], "if")))

    def test_all_refusals_are_reported(self):
        sentinel = self.tmp / "sentinel"
        body = f"\n{LEAK}\n{HOMES[0]}\nat or under 3 lines\n`## Owned by {TID}` in .orchestration/acceptance/x.md\n"
        path = self.task(body + f"\n```bash\ntouch {sentinel}\nif then\n```\n", name="dotfiles-T999-other-a01")
        result = self.run_send(path)
        for reason in ("consistency", "secret-pattern", "literal-home", "self-cap", "bash-syntax", "owner-section"):
            self.refused(result, reason)
        self.assertEqual(f"sha256: {hashlib.sha256(path.read_bytes()).hexdigest()}", result.stdout.splitlines()[-1])
        self.assertFalse(sentinel.exists())

    def test_passes_and_prints_final_sha256(self):
        path = self.task("\nRun `$HOME/x`, at or under **40 lines**.\n\n```bash\necho ok\n```\n")
        self.passed(path)  # and nothing but the digest
        self.assertEqual(1, len(self.run_send(path).stdout.splitlines()))

    def test_input_refusal(self):
        for args in ((), (self.task(), self.task()), (self.tmp / "absent.md",), (self.tmp,)):
            with self.subTest(args=args):
                result = self.run_send(*args)
                self.assertEqual((1, "input: refused\n"), (result.returncode, result.stdout))


FENCES = {  # one test per fence form, bash and sh both
    "backtick": ("```", "```\n", "bash"),
    "tilde": ("~~~", "~~~\n", "sh"),
    "longer_opener": ("`````", "`````\n", "bash"),
    "longer_closer": ("~~~", "~~~~~~\n", "sh"),
    "indented_opener": ("   ```", "```\n", "bash"),
    "indented_closer": ("```", "   ```\n", "sh"),
    "open_at_the_end": ("````", "", "bash"),
}
for _name, _form in FENCES.items():
    setattr(PreSendTest, f"test_fence_{_name}", lambda self, form=_form: self.fence(*form))


if __name__ == "__main__":
    unittest.main()
