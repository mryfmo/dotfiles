"""Exercise scripts/orchestrator/pr-audit.sh, the Codex audit route (regime-cutover U71b, operator decision G18).

The lever runs from the checkout (its self-check reads the checkout's manifest and the generated
`home/dot_agents/codex-audit/config.toml` beside it) in a scratch repository whose `origin` is a local bare repository
holding `main` and `refs/pull/7/head`, with `tests/fixtures/pr-levers/fake-gh.py` as `gh` and
`tests/fixtures/pr-audit/fake-codex.py` as `codex` first on PATH, under a scratch HOME (agent_home_isolation). The
tests assert the exact codex argv (never `-s`), the config each call saw, the probe paths, the refusals (exit 2, no
`codex exec`) and that nothing outside the run directory under TMPDIR is written. The real `codex` and `gh` are never
called.
"""

import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes, scratch_env
from test_generate_agent_configs import load_generator, sample_manifest
from test_pr_levers import JQ

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/pr-audit.sh"
TEMPLATE = ROOT / "home/dot_agents/codex-audit/config.toml"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
FAKE_GH = ROOT / "tests/fixtures/pr-levers/fake-gh.py"
FAKE_CODEX = ROOT / "tests/fixtures/pr-audit/fake-codex.py"
RULES = "## Audit\n\nThe standing audit rules.\n"
BODY = "First paragraph.\n\nProgram-Unit: regime-cutover/U7\n\n## Contract\n\nIt guarantees one thing.\n"


def setUpModule():
    isolate_agent_homes()


def tearDownModule():
    restore_agent_homes()


def tree_state(root, skip):
    """Every file and symlink under ROOT (directories in SKIP left out) mapped to its sha256 or link target."""
    state = {}
    for path in sorted(root.rglob("*")):
        if any(part in (path, *path.parents) for part in skip):
            continue
        if path.is_symlink():
            state[str(path)] = "-> " + os.readlink(path)
        elif path.is_file():
            state[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return state


@unittest.skipUnless(JQ, "no jq or gojq (gh's --jq dialect) on this host")
class PrAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        (self.bin / "gh").symlink_to(FAKE_GH)
        (self.bin / "codex").symlink_to(FAKE_CODEX)
        self.rec = self.root / "rec"
        self.rec.mkdir()
        self.tmp = self.root / "tmp"
        self.tmp.mkdir()
        self.home = self.root / "home"
        (self.home / ".codex").mkdir(parents=True)
        (self.home / ".ssh").mkdir()
        (self.home / ".ssh/id_ed25519").write_text("not a key\n")
        self.auth = self.home / ".codex/auth.json"
        self.auth.write_text('{"tokens": {}}\n')
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        self.env = {
            **scratch_env(self.home),
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "TMPDIR": str(self.tmp),
            "LC_ALL": "C",
            "GIT_CONFIG_GLOBAL": str(gitconfig),
            "GIT_CONFIG_NOSYSTEM": "1",
            "FAKE_GH_CALLS": str(self.rec / "gh-calls"),
            "FAKE_GH_RESPONSES": str(self.rec / "gh-responses.json"),
            "FAKE_GH_STATE": str(self.rec / "gh-state.json"),
            "FAKE_GH_JQ": JQ,
            "FAKE_CODEX_CALLS": str(self.rec / "codex-calls"),
            "PR_AUDIT_WAIT_TRIES": "1",
            "PR_AUDIT_WAIT_SECONDS": "0",
        }
        self.origin = self.root / "origin.git"
        self.repo = self.root / "repo"
        self.git("init", "-q", "--bare", str(self.origin), cwd=self.root)
        self.git("init", "-q", str(self.repo), cwd=self.root)
        (self.repo / "AGENTS.md").write_text(f"# Rules\n\n{RULES}\n## Other\n\nNot audit rules.\n")
        self.git("add", "AGENTS.md")
        self.git("commit", "-q", "-m", "main")
        self.main = self.git("rev-parse", "HEAD")
        self.git("checkout", "-q", "-b", "feat")
        (self.repo / "AGENTS.md").write_text("# Rules\n\n## Audit\n\nThe head's own rules, which never bind.\n")
        (self.repo / "change.txt").write_text("changed\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "head")
        self.head = self.git("rev-parse", "HEAD")
        self.git("remote", "add", "origin", str(self.origin))
        self.git("push", "-q", "origin", "main", "feat:refs/pull/7/head")
        self.git("checkout", "-q", "main")
        self.answer()

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.repo, env=self.env, check=True, capture_output=True, text=True
        ).stdout.strip()

    def answer(self, head=None, base="main", body=BODY):
        responses = [
            {"match": r"^repo view --json nameWithOwner$", "json": {"nameWithOwner": "acme/widgets"}},
            {
                "match": r"^pr view 7 --repo acme/widgets --json state,baseRefName,headRefOid,url$",
                "json": {
                    "state": "OPEN",
                    "baseRefName": base,
                    "headRefOid": head or self.head,
                    "url": "https://github.com/acme/widgets/pull/7",
                },
            },
            {"match": r"^pr view 7 --repo acme/widgets --json body$", "json": {"body": body}},
        ]
        (self.rec / "gh-responses.json").write_text(json.dumps(responses))

    def run_lever(self, *args, lever=LEVER, **env):
        return subprocess.run(
            [str(lever), *args],
            cwd=self.repo,
            env={**self.env, **env},
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def codex_calls(self):
        path = self.rec / "codex-calls"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def assert_refused(self, run, message, exec_ran=False):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused:", run.stderr)
        self.assertIn(message, run.stderr)
        self.assertEqual([c for c in self.codex_calls() if c["argv"][:1] == ["exec"]], [], "a refusal runs no audit")
        self.assertEqual(list(self.tmp.iterdir()), [], "a refusal leaves no run directory")

    def lever_copy(self, edit):
        """A checkout layout in scratch with the lever, its manifest and the audit config EDIT returns."""
        tree = self.root / "tree"
        (tree / "scripts/orchestrator").mkdir(parents=True)
        (tree / "home/dot_agents/codex-audit").mkdir(parents=True)
        shutil.copy2(LEVER, tree / "scripts/orchestrator/pr-audit.sh")
        shutil.copy2(MANIFEST, tree / "home/dot_agents/agent-config.yaml")
        (tree / "home/dot_agents/codex-audit/config.toml").write_text(edit(TEMPLATE.read_text()))
        return tree / "scripts/orchestrator/pr-audit.sh"

    def test_the_audit_runs_codex_exec_without_a_sandbox_flag_under_the_audit_profile(self):
        before = tree_state(self.root, (self.tmp, self.rec))
        run = self.run_lever("7")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("sandbox probes passed", run.stderr)
        rundirs = list(self.tmp.iterdir())
        self.assertEqual(len(rundirs), 1)
        rundir = rundirs[0]
        verdict = rundir / "verdict.md"
        self.assertEqual(run.stdout, f"{verdict}\nVerdict: correct\n")
        self.assertEqual(sorted(p.name for p in rundir.iterdir()), ["codex.log", "prompt.md", "verdict.md"])
        self.assertEqual(tree_state(self.root, (self.tmp, self.rec)), before, "nothing outside the run dir is written")

        calls = self.codex_calls()
        self.assertEqual([c["argv"][0] for c in calls], ["sandbox", "sandbox", "exec"])
        work = rundir / "work"
        exec_argv = ["exec", "--strict-config", "--skip-git-repo-check", "--ephemeral", "-C", str(work / "cwd")]
        self.assertEqual(calls[2]["argv"], [*exec_argv, "-o", str(verdict), "-"])
        for call in calls:
            self.assertNotIn("-s", call["argv"])
            self.assertFalse(
                any(a.startswith("--sandbox") or a in ("-P", "--permission-profile") for a in call["argv"])
            )
            if call["argv"][0] == "sandbox":
                self.assertEqual(call["argv"][:4], ["sandbox", "--", "/bin/sh", "-c"])
            self.assertEqual(call["cwd"], str(work / "cwd"))
            self.assertEqual(call["env"]["HOME"], str(work / "home"))
            self.assertEqual(call["env"]["CODEX_HOME"], str(work / "codex-home"))
            self.assertEqual(call["env"]["TMPDIR"], str(work / "scratch-tmpdir"))
            self.assertIsNone(call["env"]["XDG_DATA_HOME"])
            self.assertEqual(call["auth_link"], str(self.auth))
            self.assertEqual(call["config"], calls[0]["config"])

        prompt = calls[2]["prompt"]
        self.assertIn("The standing audit rules.", prompt)
        self.assertNotIn("Not audit rules.", prompt)
        self.assertNotIn("The head's own rules", prompt)
        self.assertIn("It guarantees one thing.", prompt)
        self.assertIn(f"diff {self.main}..{self.head}", prompt)

    def test_the_config_is_the_generated_source_with_every_deny_resolved(self):
        link = self.root / "homelink"
        link.symlink_to(self.home)
        env = scratch_env(link)
        run = self.run_lever("7", **env)
        self.assertEqual(run.returncode, 0, run.stderr)
        sandbox, _, exec_call = self.codex_calls()
        config = exec_call["config"]
        codex_home = exec_call["env"]["CODEX_HOME"]
        source = TEMPLATE.read_text()
        kept = [line for line in source.splitlines() if not line.endswith('= "deny"')]
        self.assertEqual([line for line in config.splitlines() if not line.endswith('= "deny"')], kept)
        self.assertIn('default_permissions = "audit"', config.splitlines())
        self.assertNotIn("sandbox_mode", config)
        denied = [line[1 : -len('" = "deny"')] for line in config.splitlines() if line.endswith('" = "deny"')]
        self.assertEqual(len(denied), len(set(denied)), "no path is denied twice")
        for path in denied:
            self.assertTrue(os.path.isabs(path), path)
        for spelling in (link, self.home):  # the HOME as given and its resolved form
            for rel in (
                ".ssh",
                ".codex",
                ".config/gh",
                ".local/share/gh",
                ".claude.json",
                ".netrc",
                "Library/Keychains",
            ):
                self.assertIn(f"{spelling}/{rel}", denied)
        self.assertIn(codex_home, denied)
        self.assertIn(str(self.auth), denied)
        probes = sandbox["probe_paths"]
        self.assertIn(f"{link}/.codex/auth.json", probes)
        self.assertIn(str(self.auth), probes)
        self.assertIn(f"{codex_home}/auth.json", probes)
        self.assertIn(f"{self.home}/.ssh", probes)
        self.assertNotIn(f"{self.home}/.aws", probes, "only paths that exist are probed")

    def test_a_config_that_does_not_select_the_audit_profile_is_refused(self):
        cases = (
            (lambda text: text.replace('default_permissions = "audit"\n', ""), "does not make the permission profile"),
            (lambda text: text.replace('"audit"\n', '":workspace"\n', 1), "does not make the permission profile"),
            (lambda text: 'sandbox_mode = "read-only"\n' + text, "names sandbox_mode"),
            (
                lambda text: text.replace("[permissions.audit]\n", "[permissions.other]\n"),
                "no single [permissions.audit]",
            ),
            (lambda text: text + '"/etc" = "deny"\n', "which is not ~/<path>"),
            (lambda text: text.replace('"~/.ssh" = "deny"', '"~/.ssh"  =  "deny"'), "deny lines"),
        )
        for edit, message in cases:
            with self.subTest(message=message):
                shutil.rmtree(self.root / "tree", ignore_errors=True)
                self.assert_refused(self.run_lever("7", lever=self.lever_copy(edit)), message)

    def test_a_login_that_is_missing_or_not_a_regular_file_is_refused(self):
        (self.root / "dir").mkdir()
        for target in (None, self.root / "dir", Path("/dev/null"), self.root / "absent"):
            with self.subTest(target=target):
                self.auth.unlink(missing_ok=True)
                if target is not None:
                    self.auth.symlink_to(target)
                self.assert_refused(self.run_lever("7"), "missing or not a readable regular file")
                self.assertEqual(self.codex_calls(), [])

    def test_a_probe_that_reads_a_denied_path_or_reaches_the_network_is_refused(self):
        for mode, message in (
            ("readable", "the sandbox read probe did not pass"),
            ("curl0", "did not show the network denied"),
            ("nocurl", "did not show the network denied"),
            ("curl127", "did not show the network denied"),  # curl could not run: no evidence either way
            ("curl126", "did not show the network denied"),
            ("curl28", "did not show the network denied"),  # a timeout is no proof of a denial
        ):
            with self.subTest(mode=mode):
                self.assert_refused(self.run_lever("7", FAKE_CODEX_PROBE=mode), message)

    def test_only_a_resolve_or_connect_failure_counts_as_network_denied(self):
        for mode in ("curl6", "curl7"):
            with self.subTest(mode=mode):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                run = self.run_lever("7", FAKE_CODEX_PROBE=mode)
                self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_template_read_that_fails_midway_runs_nothing(self):
        """A read error is never taken for the end of the file, which would drop the deny keys after it."""
        fake = self.root / "fakecat"
        fake.mkdir()
        cat = fake / "cat"
        cat.write_text(
            '#!/bin/sh\ncase "$*" in *codex-audit/config.toml) /usr/bin/head -n 28 "$2"; exit 1 ;; esac\n'
            'exec /bin/cat "$@"\n'
        )
        cat.chmod(0o755)
        run = self.run_lever("7", PATH=f"{fake}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("cannot read", run.stderr)
        self.assertEqual(self.codex_calls(), [], "no probe and no audit run on a partial config")

    def test_the_head_is_checked_out_without_the_callers_git_filters(self):
        """A .gitattributes in the head cannot make the caller's filter drivers run before confinement."""
        marker = self.root / "smudge-ran"
        self.git("checkout", "-q", "feat")
        (self.repo / ".gitattributes").write_text("* filter=mark\n")
        self.git("add", ".gitattributes")
        self.git("commit", "-q", "-m", "attributes")
        head = self.git("rev-parse", "HEAD")
        self.git("push", "-q", "-f", "origin", "feat:refs/pull/7/head")
        self.git("checkout", "-q", "main")
        with Path(self.env["GIT_CONFIG_GLOBAL"]).open("a") as config:
            config.write(f'[filter "mark"]\n\tsmudge = "touch {marker}; cat"\n\tprocess = "touch {marker}"\n')
        attributes = self.home / ".config/git/attributes"
        attributes.parent.mkdir(parents=True)
        attributes.write_text("* filter=mark\n")
        self.answer(head=head)
        run = self.run_lever("7")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(marker.exists(), "a filter driver ran on the audited tree")

    def test_a_moved_head_a_foreign_base_or_no_contract_is_refused(self):
        for answer, message in (
            ({"head": "c" * 40}, "the head moved"),
            ({"base": "release"}, "not main"),
            ({"body": "Program-Unit: regime-cutover/U7\n\nNo contract here.\n"}, "no '## Contract' section"),
        ):
            with self.subTest(message=message):
                self.answer(**answer)
                self.assert_refused(self.run_lever("7"), message)

    def test_usage_is_checked_before_any_call(self):
        for args in ((), ("x7",), ("7", "8")):
            with self.subTest(args=args):
                self.assert_refused(self.run_lever(*args), "")
                self.assertFalse((self.rec / "gh-calls").exists())

    def test_a_failed_run_or_a_message_without_a_verdict_line_exits_1(self):
        for env in ({"FAKE_CODEX_EXEC_EXIT": "1"}, {"FAKE_CODEX_VERDICT": "Verdict: correct\n\nmore text\n"}):
            with self.subTest(env=env):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                run = self.run_lever("7", **env)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertEqual(run.stdout, "")


class AuditConfigSourceTest(unittest.TestCase):
    """The generator renders codex.audit only with deny entries the lever can resolve, and both login tokens.

    The committed file equals the render of the real manifest through `generate-agent-configs.py --check`."""

    def test_a_deny_entry_the_lever_cannot_resolve_fails_the_render(self):
        module = load_generator()
        manifest = sample_manifest()
        text = module.render_codex_audit_config(manifest)
        self.assertIn('default_permissions = "audit"\n', text)
        self.assertIn('"~/.ssh" = "deny"\n', text)
        deny = manifest["codex"]["audit"]["deny"]
        for entries in (
            [*deny, "/etc"],
            [*deny, "~/../x"],
            [*deny, "~/a/./b"],
            [*deny, '~/a"b'],
            [*deny, "~/.ssh"],
            [entry for entry in deny if entry != "$CODEX_HOME"],
            [entry for entry in deny if entry != "$CODEX_LOGIN_HOME"],
        ):
            with self.subTest(entries=entries):
                manifest["codex"]["audit"]["deny"] = entries
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    module.render_codex_audit_config(manifest)


if __name__ == "__main__":
    unittest.main()
