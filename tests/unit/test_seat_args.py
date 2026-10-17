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
        self.ps.write_text(
            '#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$HOME/ps-calls"\n'
            '[[ ${FIXTURE_PS_HIDE_CALLER:-0} == 1 ]] || printf "%s fixture caller\\n" "$FIXTURE_PS_CALLER_PID"\n'
            'cat "$HOME/ps-lines"\n'
        )
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
                f"process=200 args=differs expected={CLAUDE_ARGS} found=--model:ok --effort:differs --advisor:ok",
            ),
            (
                "equals effort conflict",
                claude,
                "claude-code",
                "t",
                f"200 {match} --effort=high\n",
                2,
                f"process=200 args=differs expected={CLAUDE_ARGS} found=--model:ok --effort:differs --advisor:ok",
            ),
            (
                "equals effort match",
                claude,
                "claude-code",
                "t",
                f"200 {match.replace('--effort xhigh', '--effort=xhigh')}\n",
                0,
                "process=200 args=ok",
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
                "process=20 args=differs expected=--profile standard found=--profile:differs",
            ),
            (
                "codex resume",
                codex,
                "codex",
                "t",
                "20 codex resume abc\n",
                2,
                "process=20 args=differs expected=--profile standard found=--profile:missing",
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
            (
                "managed flag order",
                claude,
                "claude-code",
                "t",
                f"200 claude --effort high --advisor fable --model claude-opus-5-5 -n t-{claude}\n",
                2,
                f"process=200 args=differs expected={CLAUDE_ARGS} found=--effort:differs --advisor:ok --model:ok",
            ),
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

        for label, identity, kind, processes, code in [
            ("conflicting model", claude, "claude-code", f"200 {match} --model wrong\n", 2),
            (
                "earlier conflicting model",
                claude,
                "claude-code",
                f"200 claude --model wrong {CLAUDE_ARGS} -n t-{claude}\n",
                2,
            ),
            ("agreeing model", claude, "claude-code", f"200 {match} --model claude-opus-5-5\n", 0),
            ("conflicting profile", codex, "codex", "20 codex --profile standard --profile review\n", 2),
        ]:
            with self.subTest(label=label):
                self.profiles.write_text(profiles)
                result = self.run_probe(identity, kind, "t", project, processes)
                self.assertEqual(code, result.returncode, result.stderr)
                self.assertIn("args=differs" if code else "args=ok", result.stdout)
                if code:
                    self.assertEqual(1, result.stdout.count("--model:" if kind == "claude-code" else "--profile:"))

        for prompt in (
            "SYNTHETIC_PRIVATE_PROMPT_MARKER --unmanaged UNMANAGED_MARKER",
            "SYNTHETIC_PRIVATE_PROMPT_MARKER --profile MANAGED_LOOKING_PRIVATE_MARKER",
        ):
            with self.subTest(label="private positional prompt", prompt=prompt):
                self.profiles.write_text(profiles)
                result = self.run_probe(codex, "codex", "t", project, f"20 codex --profile review {prompt}\n")
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertEqual(
                    f"seat {codex} profile=standard kind=codex process=20 args=differs expected=--profile standard found=--profile:differs\n",
                    result.stdout,
                )
                for marker in ("SYNTHETIC_PRIVATE_PROMPT_MARKER", "UNMANAGED_MARKER", "MANAGED_LOOKING_PRIVATE_MARKER"):
                    self.assertNotIn(marker, result.stdout + result.stderr)

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
                "profile=standard kind=claude process=200 args=differs expected=$(touch pwned) found=$(touch:missing",
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

        seat_pid = os.getpid() + 1_000_000
        for hidden, processes, code, tail in (
            (True, f"{seat_pid} {match}\n", 4, "args=unknown-probe"),
            (True, f"{seat_pid} unrelated\n", 4, "args=unknown-probe"),
            (False, f"{seat_pid} unrelated\n", 3, "process=none args=unlaunched"),
            (False, f"{seat_pid} {match}\n", 0, f"process={seat_pid} args=ok"),
        ):
            with self.subTest(caller_hidden=hidden, processes=processes):
                self.profiles.write_text(profiles)
                result = self.run_probe(
                    claude, "claude-code", "t", project, processes, FIXTURE_PS_HIDE_CALLER=str(int(hidden))
                )
                self.assertEqual(code, result.returncode, result.stderr)
                self.assertEqual(f"seat {claude} profile=standard kind=claude {tail}\n", result.stdout)
                self.assertEqual("seat-args: ps hides the caller's own process\n" if hidden else "", result.stderr)

        original_ps, original_lsof = self.ps.read_text(), self.lsof.read_text()
        for profile, all_unavailable, code, tail in [
            ("standard", False, 0, "process=20 args=ok"),
            ("review", False, 2, "process=20 args=differs expected=--profile standard found=--profile:differs"),
            ("standard", True, 4, "args=unknown-probe"),
        ]:
            with self.subTest(decoy_cwd_unavailable=True, profile=profile, all_unavailable=all_unavailable):
                lookup = "exit 1" if all_unavailable else '[[ $pid != 10 ]] || exit 1\ncat "$HOME/cwd-$pid"'
                self.lsof.write_text(original_lsof.replace('cat "$HOME/cwd-$pid"', lookup))
                (self.home / "lsof-calls").unlink()
                self.profiles.write_text(profiles)
                result = self.run_probe(
                    codex, "codex", "t", project, f"10 codex --profile standard\n20 codex --profile {profile}\n"
                )
                self.assertEqual(code, result.returncode)
                self.assertEqual(f"seat {codex} profile=standard kind=codex {tail}\n", result.stdout)
                self.assertEqual("seat-args: lsof failed (exit 1)\n" if all_unavailable else "", result.stderr)
                self.assertEqual(
                    ["-a -p 10 -d cwd -Fn", "-a -p 20 -d cwd -Fn"],
                    (self.home / "lsof-calls").read_text().splitlines(),
                )

        for probe, code, kind, diagnostic in [
            (self.ps, 1, "claude-code", "ps failed (exit 1)"),
            (self.ps, 0, "claude-code", "ps listed no process"),
            (self.lsof, 1, "codex", "lsof failed (exit 1)"),
            (self.lsof, 0, "codex", "lsof failed (exit 0)"),
        ]:
            with self.subTest(probe=probe.name, exit=code):
                self.ps.write_text(original_ps)
                self.lsof.write_text(original_lsof)
                probe.write_text(f"#!/bin/bash\nexit {code}\n")
                self.profiles.write_text(profiles)
                identity = claude if kind == "claude-code" else codex
                result = self.run_probe(identity, kind, "t", project, f"200 {match}\n20 codex --profile standard\n")
                runtime = "claude" if kind == "claude-code" else "codex"
                self.assertEqual(4, result.returncode)
                self.assertEqual(f"seat {identity} profile=standard kind={runtime} args=unknown-probe\n", result.stdout)
                self.assertEqual(f"seat-args: {diagnostic}\n", result.stderr)

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
                "FIXTURE_PS_CALLER_PID": str(os.getpid()),
                **seams,
            },
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
