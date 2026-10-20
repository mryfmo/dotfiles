"""Exercise scripts/orchestrator/pre-send.sh, the final-byte task preflight (T133 pre-send-check-a01).

The real script, consistency checker and validator are linked into a temporary repository root, so owner records
resolve there and no live record changes. The script's pinned interpreter path, under a temporary HOME, links to
this interpreter; UV_CACHE_DIR keeps the real uv cache, so uv runs offline. Refused secret and home fixtures are built
from fragments.
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
HOMES = ("/Us" + "ers/alice/notes", "see /ho" + "me/bob", "/ro" + "ot/.ssh/id", "/var/ro" + "ot/Library")


def validator_pattern():  # this test's own reading of the validator's one assignment, parsed and never run
    tree = ast.parse((ROOT / "scripts/validate-agent-assets.py").read_text())
    names = {n.targets[0].id: n.value for n in tree.body if isinstance(n, ast.Assign) and hasattr(n.targets[0], "id")}
    return re.compile(*map(ast.literal_eval, names["SECRET_PATTERN"].args))


class PreSendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cache = subprocess.run(
            [shutil.which("uv"), "cache", "dir"], capture_output=True, text=True, check=True
        ).stdout.strip()

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
        self.env["UV_CACHE_DIR"] = self.cache

    def task(self, body="", items=1, name=TID):
        text = f"---\nformat: 2\ntask_id: {TID}\nkind: code\nsecurity: false\nallowed_files:\n"
        text += f"  - .orchestration/{TID}/**\n---\n\n# Fixture\n" + "".join(f"\n## Item {i}\n" for i in range(items))
        path = self.tmp / f"{name}.md"
        path.write_text(text + body)
        return path

    def run_send(self, *args):
        cmd = ["/bin/bash", str(self.root / LINKS[0]), *map(str, args)]
        return subprocess.run(cmd, env=self.env, capture_output=True, text=True, timeout=120, check=False)

    def refused(self, result, reason, detail=""):
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        lines = [x for x in result.stdout.splitlines() if x.startswith(f"{reason}: refused")]
        self.assertEqual(1, len(lines), result.stdout)
        self.assertIn(detail, lines[0])

    def passed(self, path):
        result = self.run_send(path)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(f"sha256: {hashlib.sha256(path.read_bytes()).hexdigest()}", result.stdout.splitlines()[-1])

    def test_consistency_refusal(self):
        self.refused(self.run_send(self.task(name="dotfiles-T999-other-a01")), "consistency", "C1 task_id")

    def test_secret_pattern_matches_validator(self):
        path = self.task(f"\nkeep {LEAK}\npassword: none\n\n## Checks\n\n```\n{LEAK}\n```\n")
        lines = [i for i, line in enumerate(path.read_text().split("\n"), 1) if validator_pattern().search(line)]
        self.assertEqual(2, len(lines))  # the body line and the last Checks line, not the near miss
        result = self.run_send(path)
        self.refused(result, "secret-pattern", f"2 match(es) on line(s) {lines[0]},{lines[1]}")
        self.assertNotIn("hunter2x", result.stdout + result.stderr)

    def test_literal_home_refusal(self):
        # the validator's own pattern: user and root homes on both platforms, a bare home name too (PR #442 4322154981)
        path = self.task(
            f"\n{HOMES[0]}\n$HOME/ok and <home>/ok and /Users/<home>\n{HOMES[1]}\n{HOMES[2]}\n{HOMES[3]}\n"
        )
        self.refused(self.run_send(path), "literal-home", "line(s) 14,16,17,18")
        self.passed(self.task("\n$HOME/ok and <home>/ok\n"))

    def test_self_cap(self):
        for spelling in ("at or under **{} lines**", "at or under {} lines"):
            with self.subTest(spelling=spelling):
                path = self.task(f"\nThis text stays {spelling.format('CAP')}.\n")
                text, n = path.read_text(), path.read_text().count("\n")
                path.write_text(text.replace("CAP", str(n)))
                self.passed(path)  # equal to the cap
                path.write_text(text.replace("CAP", str(n - 1)))
                self.refused(self.run_send(path), "self-cap", f"{n} lines over the cap of {n - 1}")
        self.passed(self.task("\nNo cap here.\n"))
        path = self.task("\nThis text stays at or under CAP lines.")  # no final newline: wc -l is one under
        path.write_text(path.read_text().replace("CAP", str(path.read_text().count("\n"))))
        self.passed(path)

    def test_fenced_bash_syntax(self):
        sentinel = self.tmp / "sentinel"
        blocks = (f"touch {sentinel}", "if then", "fi )", "done done")
        fences = ("```", "```", "````", "  ```")  # longer and indented openers too (PR #442 4322154977)
        path = self.task("".join(f"\n{f}bash\n{b}\n{f}\n" for f, b in zip(fences, blocks)))
        self.refused(self.run_send(path), "bash-syntax", "block(s) 2,3,4")
        self.assertFalse(sentinel.exists())  # parsed, never run
        self.passed(self.task(f"\n```bash\n{blocks[0]}\n```\n\n```sh\necho two\n```\n"))
        self.assertFalse(sentinel.exists())

    def test_owner_section_and_rows(self):
        body = f"\nFix the rows under `## Owned by {TID}` in .orchestration/acceptance/r.md.\n"
        record = self.root / ".orchestration/acceptance/r.md"
        record.parent.mkdir(parents=True)
        head, refusals = f"## Owned by {TID}", ("missing", "no '## Owned by", "no row")
        cases = [
            (None, 2, refusals[0]),
            ("# r\n\n## Other\n- x\n", 2, refusals[1]),
            (f"{head}\n\n## Next\n", 1, refusals[2]),
            (f"{head} (rows id<TAB>class)\nlocal:abc1234:1\tfix\n", 1, None),
            (f"# r\n\n{head}\n- one bullet\n\n## Next\n", 1, None),
            (f"{head}\n\n## Next\n- outside\nlocal:abc1234:2\tfix\n", 1, refusals[2]),
            (f"{head}\n\n## Next\n", 2, None),
        ]
        for text, items, refusal in cases:
            with self.subTest(text=text, items=items):
                record.unlink(missing_ok=True)
                if text is not None:
                    record.write_text(text)
                path = self.task(body, items=items)
                if refusal:
                    self.refused(self.run_send(path), "owner-section", refusal)
                else:
                    self.passed(path)

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
        self.passed(path)
        self.assertEqual(1, len(self.run_send(path).stdout.splitlines()))

    def test_input_refusal(self):
        for args in ((), (self.task(), self.task()), (self.tmp / "absent.md",), (self.tmp,)):
            with self.subTest(args=args):
                result = self.run_send(*args)
                self.refused(result, "input")
                self.assertNotIn("sha256:", result.stdout)


if __name__ == "__main__":
    unittest.main()
