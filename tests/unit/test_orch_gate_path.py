"""Exercise orch-gate.sh's private PATH (the audit of 6847aa9f, P1) with the binaries it runs by name stubbed.

orch-gate.sh runs from its copy in a temporary root with `uv`, `mise`, `gh` and `git` stubbed first on PATH. Every stub
appends one line `<name> <argv> <cwd>` to one log and runs nothing else: `uv` answers the gate stub's path, `mise
which <name>` answers `installs/<name>` (`payload/<name>` under the mise overrides every run exports, as a real mise
does), and `git` answers `rev-parse` with the root or the head and succeeds silently otherwise. The gate stub also records its environment and its PATH's entries with their link targets. Shebangs are
absolute and the stubs record with builtins or absolute paths, as the private PATH holds neither bash nor env.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.unit.test_pr_feedback import GhFixture

ROOT = Path(__file__).resolve().parents[2]
HEAD = "0123456789abcdef0123456789abcdef01234567"
LOG = '#!/bin/bash\nprintf "%s\\n" "{name} $* $(pwd -P)" >> "{t}/calls/log"\n'
STUBS = {
    "bin/uv": 'printf "%s\\n" "{t}/gate/python"\n',
    "bin/mise": '[[ -z "$MISE_CONFIG_FILE$MISE_TRUSTED_CONFIG_PATHS" ]] && d=installs || d=payload\n'
    + 'printf "%s\\n" "{t}/$d/$2"\n',
    "bin/gh": "",
    "bin/git": 'case "$*" in\n*"rev-parse --show-toplevel") printf "%s\\n" "{t}/repo" ;;\n'
    + '*"rev-parse HEAD") printf "%s\\n" {head} ;;\nesac\n',
    "gate/python": '/usr/bin/env > "{t}/calls/gate-env"\n'
    + 'for f in "$PATH"/*; do printf "%s %s\\n" "$f" "$(/usr/bin/readlink "$f")"; done > "{t}/calls/gate-path"\n',
}


class OrchGatePathTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.t = Path(temp.name).resolve()
        self.binding = GhFixture(self.t / "binding")
        self.root, self.review = self.t / "repo", self.t / "repo/.claude/worktrees/orchestrator-review"
        for directory in ("bin", "calls", "gate", "pr", "tmp", "repo/scripts/orchestrator", self.review):
            (self.t / directory).mkdir(parents=True, exist_ok=True)
        (self.t / "bin/jq").symlink_to(shutil.which("jq"))
        shutil.copy(ROOT / "scripts/orchestrator/orch-gate.sh", self.root / "scripts/orchestrator")
        shutil.copy(ROOT / "scripts/pr-feedback.py", self.root / "scripts/pr-feedback.py")
        v = self.root / ".orchestration/validation"
        v.mkdir(parents=True)
        (v / "t-a01-pr-feedback.json").write_text('{"pr": 9}\n')
        for name in (f"audit-{HEAD[:7]}.md", f"audit-{HEAD[:7]}.md.last.md", "review-receipt.md", "crit.json"):
            (v / f"t-a01-{name}").write_text("x\n")
        (self.root / ".orchestration/acceptance").mkdir()
        (self.root / ".orchestration/acceptance/t-a01.md").write_text("x\n")
        for path, body in STUBS.items():
            self.stub(path, body)

    def stub(self, path, body):
        name = Path(path).name
        if path == "gate/python":
            body = f'[[ $* != *--gh-binding* ]] || exec "{self.binding.python}" "$@"\n' + body
        (self.t / path).write_text((LOG + body).format(name=name, t=self.t, head=HEAD))
        (self.t / path).chmod(0o755)

    def run_gate(self, code):
        """Run the gate from outside the root; return the stub log as (command, cwd) pairs."""
        (self.t / "calls/log").unlink(missing_ok=True)
        env = {
            **self.binding.env,
            "PATH": f"{self.t}/bin{os.pathsep}{self.binding.env['PATH']}",
            "TMPDIR": str(self.t / "tmp"),
        }
        # A caller's mise overrides that would point mise which at a payload (PR #355 thread 4267889542).
        env |= {"MISE_CONFIG_FILE": f"{self.t}/payload.toml", "MISE_TRUSTED_CONFIG_PATHS": str(self.t)}
        script = self.root / "scripts/orchestrator/orch-gate.sh"
        result = subprocess.run(
            ["bash", str(script), "t-a01", str(self.t / "pr"), "9"],
            capture_output=True,
            text=True,
            cwd=self.t,
            env=env,
            timeout=30,
            check=False,
        )
        self.assertEqual(code, result.returncode, result.stderr)
        self.stderr = result.stderr
        return [tuple(line.rsplit(" ", 1)) for line in (self.t / "calls/log").read_text().splitlines()]

    def gate_path(self):
        lines = (self.t / "calls/gate-env").read_text().splitlines()
        return dict(line.split("=", 1) for line in lines if "=" in line)["PATH"]

    def test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries(self):
        log = self.run_gate(0)
        private = self.gate_path()
        self.assertEqual(1, len(private.split(os.pathsep)))
        # Compare the intersection only, so a failure prints no caller PATH.
        self.assertEqual(set(), {private} & {str(self.t / "bin"), *os.environ["PATH"].split(os.pathsep)})
        links = dict(line.split(" ", 1) for line in (self.t / "calls/gate-path").read_text().splitlines())
        self.assertEqual({f"{private}/gh": str(self.binding.target), f"{private}/git": f"{self.t}/installs/git"}, links)
        # Resolved in the trusted root, before the head is checked out in the review worktree.
        mise = [i for i, (command, _) in enumerate(log) if command.startswith("mise ")]
        self.assertEqual([("mise which git", str(self.root))], [log[i] for i in mise])
        checkout = log.index((f"git -C {self.review} checkout -q --detach {HEAD}", str(self.root)))
        self.assertLess(mise[-1], checkout)

    def test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory(self):
        for kind in ("shim", "missing"):
            with self.subTest(kind=kind):
                self.binding.declaration()
                if kind == "shim":
                    self.binding.declaration({"gh": {"version": "2.102.0", "path": "~/mise/shims/gh"}})
                else:
                    self.binding.target.unlink()
                log = self.run_gate(2)
                self.assertEqual("refused: gh binding", self.stderr.strip())
                self.assertEqual([], [command for command, _ in log if command.endswith(HEAD)])
                self.assertEqual([], os.listdir(self.review))
                self.assertFalse((self.t / "calls/gate-env").exists())

    def test_orch_gate_removes_the_private_bin_on_exit(self):
        self.run_gate(0)
        self.assertTrue(Path(self.gate_path()).parent == self.t / "tmp")
        self.assertEqual([], os.listdir(self.t / "tmp"))
        self.stub("bin/mise", 'printf "%s\\n" "{t}/mise/shims/$2"\n')
        self.run_gate(2)
        self.assertEqual([], os.listdir(self.t / "tmp"))


if __name__ == "__main__":
    unittest.main()
