import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_codex-orchestrate"
FAKE = r"""#!/usr/bin/env bash
if [[ ${0##*/} == codex ]]; then cat > "$FAKE_STATE.prompt"; fi
python3 - "$0" "$@" <<'PYFAKE'
import json, os, sys, time
from pathlib import Path
p = Path(os.environ["FAKE_STATE"])
s = json.loads(p.read_text())
name, args = Path(sys.argv[1]).name, sys.argv[2:]
s["calls"].append([name, args, os.environ.get("AGMSG_RESOLVE_PROJECT")])
rc = 0
if name == "identities.sh":
    for team, agent, kind, project in s["members"]:
        if [project, kind] == args:
            print(team + "\t" + agent)
elif name in {"team.sh", "leave.sh"}:
    raise RuntimeError("forbidden pane read or whole-member removal")
elif name == "reset.sh":
    snapshots = list((Path(os.environ["HOME"]) / ".agents/skills/agmsg/run").glob("codex-orchestrate.*/registrations.tsv"))
    s.setdefault("snapshots_at_reset", []).append([f.read_text() for f in snapshots])
    matching = [r for r in s["members"] if [r[3], r[2], r[1]] == args]
    if s.pop("reset_failure", False):
        matching = matching[:1]
        rc = 5
    s["members"] = [r for r in s["members"] if r not in matching]
elif name == "join.sh":
    if (s.get("join_failure") and args[2] == "codex") or (s.get("restore_failure") and args[2] == "claude-code"):
        rc = 7
    elif args not in s["members"]:
        s["members"].append(args)
elif name == "delivery.sh":
    rc = 8 if args[1] == s.get("delivery_failure") else 0
    if not rc:
        s.setdefault("delivery_modes", {})[args[2]] = args[1]
elif name == "herdr-agents":
    print("agmsg-orchestration: fake directive")
elif name == "inbox.sh":
    if s["messages"]:
        print(s["messages"].pop(0), end="")
elif name == "codex":
    s.setdefault("prompts", []).append(Path(str(p) + ".prompt").read_text())
    print(s.get("raw_stream", ""))
    print(s.get("raw_stream", ""), file=sys.stderr)
    if s.get("replace_public_paths"):
        for target in list(Path(".orchestration/validation").glob("codex-orchestrate-*.md")) + list((Path(os.environ["HOME"]) / ".agents/skills/agmsg/run").glob("codex-orchestrate.*/context.txt")):
            target.unlink()
            target.symlink_to(s["replace_public_paths"])
    s.setdefault("published_during_exec", []).append([p.read_text() for p in Path(".orchestration/validation").glob("codex-orchestrate-*.md")])
    s.setdefault("members_during_exec", []).append(s["members"][:])
    s.setdefault("delivery_during_exec", []).append(s.get("delivery_modes", {}).copy())
    answer = s["answers"].pop(0) if s["answers"] else "waiting"
    Path(args[args.index("-o") + 1]).write_text(answer)
    rc = s.get("codex_failure", 0)
elif name == "sleep":
    time.sleep(0.02)
p.write_text(json.dumps(s))
sys.exit(rc)
PYFAKE
"""


class CodexOrchestrateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="codex-orchestrate-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.repo = self.base / "repo with spaces"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.home = self.base / "home"
        self.scripts = self.home / ".agents/skills/agmsg/scripts"
        self.scripts.mkdir(parents=True)
        self.bin = self.base / "bin"
        self.bin.mkdir()
        for name in ("identities.sh", "inbox.sh", "join.sh", "reset.sh", "leave.sh", "team.sh", "delivery.sh"):
            self.fake(self.scripts / name)
        for name in ("codex", "herdr-agents", "sleep"):
            self.fake(self.bin / name)
        self.profile = self.home / ".agents/model-profiles.env"
        self.profile.write_text(
            'HERDR_AGENTS_ORCHESTRATOR_KIND="codex"\n'
            'MODEL_PROFILE_INTERACTIVE="fixture"\n'
            'MODEL_PROFILE_FIXTURE_CODEX_ARGS="--profile from-env"\n'
            'HERDR_AGENTS_WORKER_WORKTREE=".claude/worktrees/worker-c"\n'
        )
        self.member = ["team", "claude-orchestrator-dot", "claude-code", str(self.repo)]
        self.state = self.base / "state.json"
        self.save(members=[self.member], messages=["worker result\n"], answers=["waiting", "ORCHESTRATION-DONE"])
        self.env = dict(
            os.environ, HOME=str(self.home), PATH=f"{self.bin}:{os.environ['PATH']}", FAKE_STATE=str(self.state)
        )
        self.env.pop("CODEX_ORCHESTRATE_DELIVERY", None)
        self.env.pop("XDG_STATE_HOME", None)
        self.env["TMPDIR"] = str(self.base / "tmp")
        Path(self.env["TMPDIR"]).mkdir()
        self.private = self.home / ".local/state/codex-orchestrate"

    def fake(self, path):
        path.write_text(FAKE)
        path.chmod(0o755)

    def save(self, **updates):
        state = json.loads(self.state.read_text()) if self.state.exists() else {"calls": []}
        state.update(updates)
        self.state.write_text(json.dumps(state))
        if "members" in updates:
            teams = self.scripts.parent / "teams"
            for config in teams.glob("*/config.json"):
                config.unlink()
            configs = {}
            for team, name, kind, project in updates["members"]:
                agent = configs.setdefault(team, {}).setdefault(name, {"registrations": []})
                agent["registrations"].append({"type": kind, "project": project})
            for team, agents in configs.items():
                config = teams / team / "config.json"
                config.parent.mkdir(parents=True, exist_ok=True)
                config.write_text(json.dumps({"name": team, "agents": agents}))

    def run_script(self, *args, cwd=None, task="operator task `literal` $value"):
        return subprocess.run(
            ["bash", str(SCRIPT), *args, task],
            cwd=cwd or self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=12,
            check=False,
        )

    def calls(self, name):
        return [c[1] for c in json.loads(self.state.read_text())["calls"] if c[0] == name]

    def test_exec_resume_profile_transcript_and_restore(self):
        result = self.run_script("--max-turns", "3", "--timeout", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        first, second = self.calls("codex")
        self.assertEqual(
            json.loads(self.state.read_text())["members_during_exec"],
            [[["team", "codex-fixture-dot", "codex", str(self.repo)]]] * 2,
        )
        self.assertEqual(first[:5], ["--profile", "from-env", "exec", "-C", str(self.repo)])
        self.assertEqual(second[:5], ["--profile", "from-env", "exec", "resume", "--last"])
        self.assertEqual(
            json.loads(self.state.read_text())["prompts"][0],
            "agmsg-orchestration: fake directive\noperator task `literal` $value\n"
            "When the orchestration is complete, end your final message with the line `ORCHESTRATION-DONE`; "
            "otherwise end the turn and wait for the next agmsg delivery.",
        )
        self.assertEqual(first[-2:], ["--", "-"])
        self.assertEqual(second[-2:], ["--", "-"])
        self.assertEqual(json.loads(self.state.read_text())["prompts"][1], "worker result")
        self.assertEqual(self.calls("herdr-agents"), [["--directive"]])
        self.assertEqual(
            self.calls("delivery.sh"),
            [["set", "turn", "codex", str(self.repo)], ["set", "both", "claude-code", str(self.repo)]],
        )
        state = json.loads(self.state.read_text())
        self.assertEqual(state["delivery_during_exec"], [{"codex": "turn"}] * 2)
        self.assertEqual(state["delivery_modes"]["claude-code"], "both")
        names = [c[0] for c in state["calls"]]
        self.assertLess(names.index("join.sh"), names.index("delivery.sh"))
        self.assertEqual(names[-2:], ["join.sh", "delivery.sh"])

        self.assertEqual(self.calls("inbox.sh"), [["team", "codex-fixture-dot", "--quiet"]])
        self.assertEqual(json.loads(self.state.read_text())["members"], [self.member])
        transcript = next(
            p
            for p in (self.repo / ".orchestration/validation").glob("codex-orchestrate-*.md")
            if not p.name.endswith(".last.md")
        )
        self.assertNotIn("operator task `literal` $value", transcript.read_text())
        self.assertIn("done=true", transcript.read_text())
        self.assertIn("turn=2", transcript.read_text())
        for call in json.loads(self.state.read_text())["calls"]:
            if call[0] in {"join.sh", "reset.sh", "identities.sh"}:
                self.assertEqual(call[2], "0")

    def test_only_the_final_nonblank_line_completes_orchestration(self):
        for waiting in ("The worker said `ORCHESTRATION-DONE`, but I am waiting.", "ORCHESTRATION-DONE\nStill waiting"):
            with self.subTest(waiting=waiting):
                self.save(calls=[], messages=["worker result"], answers=[waiting, "ORCHESTRATION-DONE\n\n \t\n"])
                result = self.run_script()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(len(self.calls("codex")), 2)
                self.assertEqual(len(self.calls("inbox.sh")), 1)

    def test_raw_content_stays_private_with_status_only_publication(self):
        secret = (
            "AWS_SECRET_ACCESS_KEY="
            + "A" * 40
            + "\n-----BEGIN "
            + "PRIVATE KEY-----\nQUJD\n-----END "
            + "PRIVATE KEY-----"
        )
        self.save(answers=[secret, "ORCHESTRATION-DONE"], raw_stream=secret)
        result = self.run_script(task=secret)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(secret, result.stdout + result.stderr)
        outputs = list((self.repo / ".orchestration/validation").glob("codex-orchestrate-*.md"))
        self.assertEqual(len(outputs), 1)
        status = outputs[0].read_text()
        self.assertNotIn(secret, status)
        self.assertIn("exit=0", status)
        self.assertIn("done=false", status)
        self.assertIn("done=true", status)
        run = next(self.private.iterdir())
        self.assertEqual(run.stat().st_mode & 0o777, 0o700)
        for filename in ("1.prompt.txt", "1.final.md", "1.console.txt"):
            path = run / filename
            self.assertIn(secret, path.read_text())
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertIn(str(path), status)
        self.assertIn(f"prompt_bytes={(run / '1.prompt.txt').stat().st_size}", status)
        self.assertIn(f"final_bytes={(run / '1.final.md').stat().st_size}", status)
        self.assertRegex(status, r"started=\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ")
        self.assertRegex(status, r"ended=\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ")
        snapshots = json.loads(self.state.read_text())["published_during_exec"]
        self.assertTrue(all(secret not in text for files in snapshots for text in files))
        self.assertEqual(list((self.scripts.parent / "run").glob("codex-orchestrate.*/*.md")), [])

    def test_large_inbox_body_uses_stdin(self):
        message = "X" * (140 * 1024)
        self.save(messages=[message])
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.state.read_text())["prompts"][1], message)
        self.assertEqual(self.calls("codex")[1][-2:], ["--", "-"])

    def test_private_path_rejects_repo_agmsg_and_temp_including_symlinks(self):
        for index, root in enumerate((self.repo, self.scripts.parent, Path(self.env["TMPDIR"]))):
            with self.subTest(root=root):
                alias = self.base / f"alias-{index}"
                alias.symlink_to(root, target_is_directory=True)
                self.env["XDG_STATE_HOME"] = str(alias / "state")
                result = self.run_script()
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("private state", result.stderr)
                self.assertEqual(self.calls("reset.sh"), [])
                self.assertEqual(self.calls("join.sh"), [])
                self.assertFalse((root / "state").exists())

    def test_relative_xdg_state_is_rejected(self):
        self.env["XDG_STATE_HOME"] = "relative-state"
        result = self.run_script()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(self.calls("reset.sh"), [])

    def test_existing_private_run_is_not_reused(self):
        self.save(answers=["ORCHESTRATION-DONE"])
        self.assertEqual(self.run_script().returncode, 0)
        first = next(self.private.iterdir())
        sentinel = first / "sentinel"
        sentinel.write_text("preserve")
        for status in (self.repo / ".orchestration/validation").glob("codex-orchestrate-*.md"):
            status.unlink()
        self.save(answers=["ORCHESTRATION-DONE"])
        self.assertEqual(self.run_script().returncode, 0)
        self.assertEqual(len(list(self.private.iterdir())), 2)
        self.assertEqual(sentinel.read_text(), "preserve")

    def test_private_allocation_failure_precedes_exchange(self):
        self.private.parent.mkdir(parents=True)
        self.private.write_text("occupied")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls("reset.sh"), [])
        self.assertEqual(self.calls("join.sh"), [])

    def test_child_cannot_redirect_parent_status_or_restore_writes(self):
        victim = self.base / "unrelated.txt"
        victim.write_text("preserve")
        self.save(answers=["ORCHESTRATION-DONE"], replace_public_paths=str(victim))
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(victim.read_text(), "preserve")

    def test_codex_delivery_failure_restores_claude_without_starting_a_turn(self):
        self.save(delivery_failure="turn")
        result = self.run_script()
        self.assertEqual(result.returncode, 8, result.stderr)
        self.assertEqual(self.calls("codex"), [])
        state = json.loads(self.state.read_text())
        self.assertEqual(state["members"], [self.member])
        self.assertEqual(state["delivery_modes"]["claude-code"], "both")

    def test_claude_delivery_restore_failure_keeps_recovery_lock(self):
        self.save(delivery_failure="both", answers=["ORCHESTRATION-DONE"])
        result = self.run_script()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(self.state.read_text())["members"], [self.member])
        self.assertTrue((self.repo / ".orchestration/validation/codex-orchestrate.lock").exists())
        context = next((self.home / ".agents/skills/agmsg/run").glob("codex-orchestrate.*/context.txt"))
        self.assertIn("restore_exit=1", context.read_text())

    def test_repeated_runs_restore_and_increment_transcripts(self):
        for _ in range(2):
            self.save(answers=["ORCHESTRATION-DONE"])
            self.assertEqual(self.run_script().returncode, 0)
            self.assertEqual(json.loads(self.state.read_text())["members"], [self.member])
        files = [
            p
            for p in (self.repo / ".orchestration/validation").glob("codex-orchestrate-*.md")
            if not p.name.endswith(".last.md")
        ]
        self.assertEqual(len(files), 2)

    def test_existing_codex_seat_is_not_rejoined_or_removed(self):
        member = ["team", "codex-fixture-dot", "codex", str(self.repo)]
        self.save(members=[member], answers=["ORCHESTRATION-DONE"])
        self.assertEqual(self.run_script().returncode, 0)
        self.assertEqual(self.calls("join.sh"), [])
        self.assertEqual(self.calls("reset.sh"), [])
        self.assertEqual(json.loads(self.state.read_text())["members"], [member])
        self.assertEqual(self.calls("delivery.sh"), [["set", "turn", "codex", str(self.repo)]])

    def test_worker_seats_and_multiple_previous_identities_are_preserved(self):
        worker = ["team", "claude-standard-dot-a001", "claude-code", str(self.repo)]
        alias = ["team", "claude-worker-dot", "claude-code", str(self.repo)]
        alias_at_worker = [*alias[:3], str(self.repo / ".claude/worktrees/worker-c")]
        other = ["team", "claude-old-dot", "claude-code", str(self.repo)]
        members = [self.member, worker, alias, alias_at_worker, other]
        self.save(members=members, answers=["ORCHESTRATION-DONE"])
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertCountEqual(json.loads(self.state.read_text())["members"], members)
        self.assertNotIn([str(self.repo), "claude-code", worker[1]], self.calls("reset.sh"))
        self.assertNotIn([str(self.repo), "claude-code", alias[1]], self.calls("reset.sh"))

    def test_max_turns_does_not_poll_after_last_turn(self):
        self.save(answers=["waiting"])
        result = self.run_script("--max-turns", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("max-turns", result.stderr)
        self.assertEqual(len(self.calls("codex")), 1)
        self.assertEqual(self.calls("inbox.sh"), [])

    def test_timeout_restores_identity_and_polls_at_fifteen_seconds(self):
        self.save(messages=[], answers=["waiting"])
        result = self.run_script("--timeout", "1")
        self.assertEqual(result.returncode, 124, result.stderr)
        self.assertIn("timeout", result.stderr)
        self.assertTrue(self.calls("sleep"))
        self.assertTrue(all(0 < int(c[0]) <= 15 for c in self.calls("sleep")))
        self.assertEqual(json.loads(self.state.read_text())["members"], [self.member])

    def test_unvalidated_hook_mode_refuses_before_exchange(self):
        self.env["CODEX_ORCHESTRATE_DELIVERY"] = "hook"
        result = self.run_script("--max-turns", "2")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("not validated; T87", result.stderr)
        for name in ("inbox.sh", "codex", "reset.sh", "join.sh"):
            self.assertEqual(self.calls(name), [])

    def test_exec_failure_restores_seat(self):
        self.save(codex_failure=9)
        self.assertEqual(self.run_script().returncode, 9)
        self.assertEqual(json.loads(self.state.read_text())["members"], [self.member])

    def test_join_failure_restores_previous_seat(self):
        self.save(join_failure=True)
        self.assertNotEqual(self.run_script().returncode, 0)
        self.assertIn([str(self.repo), "claude-code", self.member[1]], self.calls("reset.sh"))
        self.assertEqual(json.loads(self.state.read_text())["members"], [self.member])

    def test_empty_poll_waits_fifteen_seconds_and_preserves_option_like_body(self):
        self.save(messages=["", "--config dangerous=literal\n"])
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls("sleep"), [["15"]])
        self.assertEqual(self.calls("codex")[1][-2:], ["--", "-"])
        self.assertEqual(json.loads(self.state.read_text())["prompts"][1], "--config dangerous=literal")

    def test_team_selection_restores_all_exchanged_registrations(self):
        other = ["other-team", "claude-other-dot", "claude-code", str(self.repo)]
        self.save(members=[self.member, other], answers=["ORCHESTRATION-DONE"])
        self.assertEqual(self.run_script().returncode, 2)
        self.assertEqual(self.calls("reset.sh"), [])
        result = self.run_script("--team", "team")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertCountEqual(json.loads(self.state.read_text())["members"], [self.member, other])

    def test_existing_lock_refuses_exchange(self):
        (self.repo / ".orchestration/validation/codex-orchestrate.lock").mkdir(parents=True)
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("another launcher", result.stderr)
        self.assertEqual(self.calls("reset.sh"), [])

    def test_cross_project_claude_registration_is_preserved(self):
        members = [self.member, [*self.member[:3], "/another/project"]]
        self.save(members=members, answers=["ORCHESTRATION-DONE"])
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertCountEqual(json.loads(self.state.read_text())["members"], members)
        self.assertEqual(self.calls("team.sh"), [])
        self.assertEqual(self.calls("leave.sh"), [])

    def test_target_codex_registration_elsewhere_is_refused_before_mutation(self):
        for team, already_here in (("team", False), ("team", True), ("unrelated-team", True)):
            with self.subTest(team=team, already_here=already_here):
                target = ["team", "codex-fixture-dot", "codex", str(self.repo)]
                members = [self.member, [team, target[1], "codex", "/another/project"]]
                if already_here:
                    members.insert(1, target)
                self.save(members=members, calls=[], answers=["ORCHESTRATION-DONE"])
                result = self.run_script()
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("/another/project", result.stderr)
                self.assertEqual(json.loads(self.state.read_text())["members"], members)
                for command in ("join.sh", "reset.sh", "delivery.sh", "codex"):
                    self.assertEqual(self.calls(command), [])

    def test_legacy_target_registration_elsewhere_is_refused(self):
        config = self.scripts.parent / "teams/legacy/config.json"
        config.parent.mkdir()
        config.write_text(json.dumps({"agents": {"codex-fixture-dot": {"type": "codex", "project": "/legacy"}}}))
        result = self.run_script()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("/legacy", result.stderr)
        self.assertEqual(self.calls("reset.sh"), [])

    def test_malformed_global_registration_fails_before_mutation(self):
        config = self.scripts.parent / "teams/broken/config.json"
        config.parent.mkdir()
        config.write_text("{invalid")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls("reset.sh"), [])
        self.assertEqual(self.calls("join.sh"), [])

    def test_existing_codex_seat_in_multiple_teams_is_reused(self):
        members = [[team, "codex-fixture-dot", "codex", str(self.repo)] for team in ("team", "other-team")]
        for team in ("team", "other-team"):
            with self.subTest(team=team):
                self.save(
                    members=members, calls=[], messages=["worker result"], answers=["waiting", "ORCHESTRATION-DONE"]
                )
                result = self.run_script("--team", team)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.calls("inbox.sh"), [[team, "codex-fixture-dot", "--quiet"]])
                self.assertEqual(self.calls("join.sh"), [])
                self.assertEqual(self.calls("reset.sh"), [])
                self.assertEqual(json.loads(self.state.read_text())["members"], members)

    def test_existing_codex_seat_requires_membership_in_selected_team(self):
        members = [self.member, ["other-team", "codex-fixture-dot", "codex", str(self.repo)]]
        self.save(members=members)
        result = self.run_script("--team", "team")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("select a team", result.stderr)
        self.assertEqual(self.calls("join.sh"), [])
        self.assertEqual(self.calls("reset.sh"), [])

    def test_different_codex_identity_at_checkout_is_refused(self):
        members = [self.member, ["team", "codex-other-dot", "codex", str(self.repo)]]
        self.save(members=members)
        result = self.run_script()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("another Codex seat", result.stderr)
        self.assertEqual(self.calls("join.sh"), [])
        self.assertEqual(self.calls("reset.sh"), [])

    def test_snapshot_covers_all_teams_before_partial_reset_and_restores_them(self):
        other = ["other-team", *self.member[1:]]
        members = [self.member, other]
        self.save(members=members, reset_failure=True)
        result = self.run_script("--team", "team")
        self.assertEqual(result.returncode, 5, result.stderr)
        state = json.loads(self.state.read_text())
        self.assertCountEqual(state["members"], members)
        snapshot = state["snapshots_at_reset"][0][0]
        for row in members:
            self.assertIn("\t".join(row), snapshot)
        path = next((self.home / ".agents/skills/agmsg/run").glob("codex-orchestrate.*/registrations.tsv"))
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_restore_failure_keeps_lock_and_snapshot_for_recovery(self):
        self.save(answers=["ORCHESTRATION-DONE"], restore_failure=True)
        result = self.run_script()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue((self.repo / ".orchestration/validation/codex-orchestrate.lock").exists())
        context = next((self.home / ".agents/skills/agmsg/run").glob("codex-orchestrate.*/context.txt"))
        self.assertIn(str(self.repo), context.read_text())
        self.assertIn("restore_exit=1", context.read_text())

    def test_worker_alias_is_excluded_across_teams(self):
        alias = ["team", "claude-worker-dot", "claude-code", str(self.repo)]
        at_worker = [*alias[:3], str(self.repo / ".claude/worktrees/worker-c")]
        other = ["other-team", *alias[1:]]
        members = [self.member, alias, at_worker, other]
        self.save(members=members, answers=["ORCHESTRATION-DONE"])
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertCountEqual(json.loads(self.state.read_text())["members"], members)
        self.assertNotIn([str(self.repo), "claude-code", alias[1]], self.calls("reset.sh"))

    def test_subdirectory_is_rejected_before_exchange(self):
        child = self.repo / "child"
        child.mkdir()
        result = self.run_script(cwd=child)
        self.assertEqual(result.returncode, 2)
        self.assertIn("main checkout root", result.stderr)
        self.assertEqual(self.calls("reset.sh"), [])

    def test_wrong_kind_and_invalid_arguments_fail_before_exchange(self):
        for args in [("--timeout", "no"), ("--max-turns", "0"), ("--timeout", "99999999999999999999"), ("--unknown",)]:
            with self.subTest(args=args):
                self.assertEqual(self.run_script(*args).returncode, 2)
        self.profile.write_text(self.profile.read_text().replace('KIND="codex"', 'KIND="claude"'))
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("herdr-agents", result.stderr)
        self.assertEqual(self.calls("reset.sh"), [])

    def test_missing_generated_environment_names_herdr_and_exits_two(self):
        self.profile.unlink()
        result = self.run_script()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("herdr-agents", result.stderr)
        self.assertEqual(self.calls("reset.sh"), [])

    def test_no_literal_model_or_profile_flags_and_bounded_size(self):
        text = SCRIPT.read_text()
        self.assertNotIn("--model", text)
        self.assertNotIn("--profile", text)
        self.assertLessEqual(len(text.splitlines()), 150)


if __name__ == "__main__":
    unittest.main()
