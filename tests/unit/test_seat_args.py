"""Compare profile arguments through fixture ps/lsof probes, never real processes."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/orchestrator/seat-args.sh"
CLAUDE_ARGS = "--model claude-opus-5-5 --effort xhigh --advisor fable"


class SeatArgsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name)
        self.home = self.temp / "home"
        self.profiles = self.home / ".agents/model-profiles.env"
        self.profiles.parent.mkdir(parents=True)
        self.ps = self.temp / "ps"
        self.ps.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$HOME/ps-calls"\ncat "$HOME/ps-lines"\n')
        self.ps.chmod(0o755)
        self.lsof = self.temp / "lsof"
        self.lsof.write_text(
            '#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$HOME/lsof-calls"\n'
            "while (($#)); do\n  if [[ $1 == -p ]]; then pid=$2; shift; fi\n  shift\ndone\n"
            'cat "$HOME/cwd-$pid"\n'
        )
        self.lsof.chmod(0o755)

    def test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one(self):
        claude = "claude-standard-dot-a001"
        codex = "codex-standard-dot-a004"
        project = str(self.temp / "project with spaces")
        match = f"claude {CLAUDE_ARGS} -n t-{claude} /agmsg actas {claude}"
        low = match.replace("--effort xhigh", "--effort high")
        profiles = (
            f'MODEL_PROFILE_STANDARD_CLAUDE_ARGS="{CLAUDE_ARGS}"\n'
            'MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"\n'
        )
        cases = [
            ("claude match", claude, "claude-code", "t", f"200 {match}\n", 0, "process=200 args=ok"),
            ("second team", claude, "claude-code", "other,t", f"200 {match}\n", 0, "process=200 args=ok"),
            ("wrong team", claude, "claude-code", "other", f"200 {match}\n", 3, "process=none args=unlaunched"),
            ("resumed", claude, "claude-code", "t", "100 claude --resume abc\n", 3, "process=none args=unlaunched"),
            (
                "different effort",
                claude,
                "claude-code",
                "t",
                f"200 {low}\n",
                2,
                f"process=200 args=differs expected={CLAUDE_ARGS} found={low.removeprefix('claude ')}",
            ),
            ("pid order", claude, "claude-code", "t", f"300 {low}\n100 {match}\n", 0, "process=100 args=ok"),
            ("absolute claude", claude, "claude-code", "t", f"200 /opt/bin/{match}\n", 0, "process=200 args=ok"),
            (
                "codex cwd",
                codex,
                "codex",
                "t",
                "10 codex --profile review\n20 codex --profile standard /agmsg\n",
                0,
                "process=20 args=ok",
            ),
            (
                "codex differs",
                codex,
                "codex",
                "t",
                "10 codex --profile standard\n20 codex --profile review\n",
                2,
                "process=20 args=differs expected=--profile standard found=--profile review",
            ),
            (
                "codex resume",
                codex,
                "codex",
                "t",
                "20 codex resume abc\n",
                2,
                "process=20 args=differs expected=--profile standard found=resume abc",
            ),
            (
                "npm wrapper",
                codex,
                "codex",
                "t",
                "20 node /opt/bin/codex --profile standard\n",
                0,
                "process=20 args=ok",
            ),
            ("absolute codex", codex, "codex", "t", "20 /opt/bin/codex --profile standard\n", 0, "process=20 args=ok"),
            ("codex absent", codex, "codex", "t", "10 codex --profile standard\n", 3, "process=none args=unlaunched"),
        ]
        for label, identity, kind, teams, processes, code, tail in cases:
            with self.subTest(label=label):
                self.profiles.write_text(profiles)
                result = self.run_probe(identity, kind, teams, project, processes)
                self.assertEqual(code, result.returncode, result.stderr)
                runtime = "claude" if kind == "claude-code" else "codex"
                self.assertEqual(f"seat {identity} profile=standard kind={runtime} {tail}\n", result.stdout)

        with self.subTest(label="underscore profile"):
            identity = "claude-my_profile-dot-a001"
            self.profiles.write_text(f'MODEL_PROFILE_MY_PROFILE_CLAUDE_ARGS="{CLAUDE_ARGS}"\n')
            result = self.run_probe(identity, "claude-code", "t", project, f"200 {match.replace(claude, identity)}\n")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(f"seat {identity} profile=my_profile kind=claude process=200 args=ok\n", result.stdout)

        for label, identity, kind, profile_text, seam, expected in [
            (
                "missing key",
                claude,
                "claude-code",
                'OTHER="x"\n',
                {},
                "profile=standard kind=claude args=unknown-profile",
            ),
            (
                "literal substitution",
                claude,
                "claude-code",
                'MODEL_PROFILE_STANDARD_CLAUDE_ARGS="$(touch pwned)"\n',
                {},
                f"profile=standard kind=claude process=200 args=differs expected=$(touch pwned) found={match.removeprefix('claude ')}",
            ),
            ("unknown identity", "claude-a005", "claude-code", profiles, {}, "args=unknown-identity"),
            ("kind mismatch", claude, "codex", profiles, {}, "args=unknown-identity"),
            (
                "missing ps",
                claude,
                "claude-code",
                profiles,
                {"SEAT_ARGS_PS": str(self.temp / "absent")},
                "profile=standard kind=claude args=unknown-probe",
            ),
            (
                "missing lsof",
                codex,
                "codex",
                profiles,
                {"SEAT_ARGS_LSOF": str(self.temp / "absent")},
                "profile=standard kind=codex args=unknown-probe",
            ),
        ]:
            with self.subTest(label=label):
                self.profiles.write_text(profile_text)
                result = self.run_probe(identity, kind, "t", project, f"200 {match}\n", **seam)
                self.assertEqual(4 if seam else 2, result.returncode, result.stderr)
                self.assertEqual(f"seat {identity} {expected}\n", result.stdout)
                self.assertFalse((self.temp / "pwned").exists())
        calls = (self.home / "lsof-calls").read_text().splitlines()
        self.assertIn("-a -p 10 -d cwd -Fn", calls)
        self.assertIn("-a -p 20 -d cwd -Fn", calls)
        self.assertEqual({"-axo pid=,command="}, set((self.home / "ps-calls").read_text().splitlines()))

    def run_probe(self, identity, kind, teams, project, processes, **seams):
        (self.home / "ps-lines").write_text(processes)
        (self.home / "cwd-10").write_text("p10\nn/another/repository\n")
        (self.home / "cwd-20").write_text(f"p20\nn{project}\n")
        return subprocess.run(
            ["bash", str(SCRIPT), teams, identity, kind, project],
            cwd=self.temp,
            env={
                **os.environ,
                "HOME": str(self.home),
                "SEAT_ARGS_PS": str(self.ps),
                "SEAT_ARGS_LSOF": str(self.lsof),
                **seams,
            },
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
