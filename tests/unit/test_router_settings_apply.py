"""scripts/orchestrator/router-settings-apply against a fake Management API on a loopback port, and the `gh` wrapper
scripts/orchestrator/router-gh the Router's `cli` names (regime-cutover U353, M-26 stage B).

The fake API speaks the grammar of the pinned dsh-superagent archive (8c32a9dc): `GET settings` answers the settings view
(`src/app/views/settings.ts:23-41`: `blocks.eval` and each Source with its `value` and `revision`), `PUT settings/<block>`
takes `{"value", "revision"}` (`src/app/http.ts:149, :196-202`), a stale revision is 409 (`src/app/settings.ts:151`), a
request without the `x-orchestrator-request: 1` header or from another host is 403 (`src/app/http.ts:75-78, :237`), and
a `source:github` save while the agent CLI is signed out is 400 with `setup.code` `agentCliSignedOut`
(`src/app/settings.ts:167`, `src/app/setup.ts:61-66`, `src/deployment.ts:95`, `src/app/http.ts:86`). Every request the
lever makes is recorded, so the tests hold the bodies, the order (the revision read first) and the count (a second run
PUTs nothing). Nothing reaches a network host beyond 127.0.0.1.
"""

from __future__ import annotations

import copy
import hashlib
import http.server
import json
import os
import re
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/router-settings-apply"
WRAPPER = ROOT / "scripts/orchestrator/router-gh"
INSTALLED = ROOT / "home/dot_local/bin/common/executable_router-settings-apply"
INSTALLED_WRAPPER = ROOT / "home/dot_local/bin/common/executable_router-gh"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
PROFILE = ROOT / "home/dot_dsh/profiles/router/cordis.patch.yml"
API = "/orchestrator/api/"
# The eval block as the archive defaults it (src/policy.ts:83-87) with the mode the kit must change.
EVAL_DEFAULT = {"mode": "off", "timeoutSeconds": 120, "model": None}
SIGNED_OUT = {
    "place": "github",
    "code": "agentCliSignedOut",
    "values": {"output": "gh: To get started with GitHub CLI, please run:  gh auth login"},
    "detail": "The agent GitHub CLI cannot read its account.",
}


class FakeApi(http.server.ThreadingHTTPServer):
    """The Management API of one Router: its state, its switches and the requests it received."""

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), FakeHandler)
        self.port = self.server_address[1]
        self.requests: list[dict] = []
        self.source = {"enabled": True, "config": {}}
        self.source_revision = 0
        self.eval = copy.deepcopy(EVAL_DEFAULT)
        self.eval_revision = 0
        self.reject_header = False  # answer 403 to everything, as the host check does for a wrong header
        self.stale = False  # answer 409 to every PUT, as a revision raced by the panel would
        self.signed_out = True  # the agent CLI has no login: a source:github save with new setup fields is 400
        self.setup_pending = True  # every save restarts the Router while setup is pending
        self.view_without = None  # drop one key from the settings view: "github" or "eval"

    def view(self) -> dict:
        view = {
            "policyVersion": "mandate-v3:0",
            "blocks": {
                "policy": {"value": {"rules": [], "sources": {}}, "revision": 0},
                "eval": {"value": copy.deepcopy(self.eval), "revision": self.eval_revision},
                "executor": {"value": {"model": None, "maxWorkers": 3, "directory": "", "prepare": "", "blockedCommands": []}, "revision": 0},
            },
            "sources": [
                {"id": "github", "kind": "github", "installed": True, "value": copy.deepcopy(self.source),
                 "revision": self.source_revision, "restarts": ["repository", "cli"], "fields": [], "facts": {}, "labels": {}}
            ],
            "environment": {"root": "/state/work", "variables": []},
        }  # fmt: skip
        if self.view_without == "github":
            view["sources"] = []
        if self.view_without == "eval":
            del view["blocks"]["eval"]
        return view


class FakeHandler(http.server.BaseHTTPRequestHandler):
    server: FakeApi

    def log_message(self, *_args) -> None:  # quiet
        return

    def answer(self, status: int, body: dict) -> None:
        text = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(text)))
        self.end_headers()
        self.wfile.write(text)

    def record(self, method: str) -> dict:
        length = int(self.headers.get("content-length") or 0)
        raw = self.rfile.read(length) if length else b""
        entry = {"method": method, "path": self.path, "headers": {k.lower(): v for k, v in self.headers.items()},
                 "body": json.loads(raw) if raw else None}  # fmt: skip
        self.server.requests.append(entry)
        return entry

    def same_origin(self) -> bool:
        host = self.headers.get("host")
        if host not in (f"127.0.0.1:{self.server.port}", f"localhost:{self.server.port}"):
            return False
        return self.headers.get("x-orchestrator-request") == "1" and not self.server.reject_header

    def do_GET(self) -> None:  # noqa: N802  # http.server's name
        self.record("GET")
        if not self.path.startswith(API):
            self.send_response(404)
            self.end_headers()
            return
        if not self.same_origin():
            return self.answer(403, {"error": "Same-origin management request required"})
        if self.path == API + "settings":
            return self.answer(200, self.server.view())
        self.answer(404, {"error": "Unknown operation"})

    def do_PUT(self) -> None:  # noqa: N802
        entry = self.record("PUT")
        if not self.same_origin():
            return self.answer(403, {"error": "Same-origin management request required"})
        block = self.path.removeprefix(API + "settings/")
        body = entry["body"] if isinstance(entry["body"], dict) else {}
        if block not in ("source:github", "eval"):
            return self.answer(404, {"error": "Source not found"})
        current = self.server.source_revision if block == "source:github" else self.server.eval_revision
        if self.server.stale or body.get("revision") != current:
            return self.answer(409, {"error": "Settings changed. Reload before saving."})
        if block == "source:github":
            config = body["value"].get("config", {})
            setup_changed = (config.get("repository"), config.get("cli")) != (
                self.server.source["config"].get("repository"), self.server.source["config"].get("cli"))  # fmt: skip
            if setup_changed and self.server.signed_out:
                return self.answer(400, {"error": SIGNED_OUT["detail"], "setup": SIGNED_OUT})
            self.server.source = body["value"]
            self.server.source_revision += 1
            revision = self.server.source_revision
        else:
            self.server.eval = body["value"]
            self.server.eval_revision += 1
            revision = self.server.eval_revision
        self.answer(200, {"saved": True, "revision": revision, "policy_changed": False,
                          "restarting": self.server.setup_pending, "context_delivery": "pending"})  # fmt: skip


class RouterSettingsApplyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(tempfile.mkdtemp(prefix="router-settings-apply-"))
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.api = FakeApi()
        self.thread = threading.Thread(target=self.api.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.api.server_close)
        self.addCleanup(self.api.shutdown)
        self.profile = self.dir / "cordis.patch.yml"
        self.profile.write_text(PROFILE.read_text().replace("    port: 3082\n", f"    port: {self.api.port}\n"))
        self.assertIn(
            f"    port: {self.api.port}\n", self.profile.read_text(), "the rendered port row is the one replaced"
        )
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.dir / "home"), "LC_ALL": "C"}
        (self.dir / "home").mkdir()

    def run_lever(self, *args: str, lever: Path = LEVER, env: dict | None = None) -> subprocess.CompletedProcess:
        argv = [sys.executable, "-I", str(lever), "--profile", str(self.profile), *args]
        return subprocess.run(
            argv, capture_output=True, text=True, check=False, timeout=120, env=env or self.env, cwd=self.dir
        )

    def puts(self) -> list[dict]:
        return [entry for entry in self.api.requests if entry["method"] == "PUT"]

    def test_the_two_put_bodies_follow_upstreams_grammar_after_the_revision_is_read_and_a_second_run_puts_nothing(self):
        # The manifest row: repository mryfmo/dotfiles, accept_mode observe (M-18 row 2026-11-06T23:24:00Z).
        self.api.signed_out = False
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(self.api.requests[0]["method"], "GET", "the revision is read before anything is written")
        self.assertEqual(self.api.requests[0]["path"], API + "settings")
        for entry in self.api.requests:
            with self.subTest(request=(entry["method"], entry["path"])):
                self.assertEqual(entry["headers"]["x-orchestrator-request"], "1")
                self.assertEqual(entry["headers"]["host"], f"127.0.0.1:{self.api.port}")
        source, evaluation = self.puts()
        self.assertEqual(source["path"], API + "settings/source:github")
        self.assertEqual(source["headers"]["content-type"], "application/json")
        self.assertEqual(
            source["body"],
            {
                "value": {
                    "enabled": True,
                    "config": {"repository": "mryfmo/dotfiles", "cli": str(WRAPPER), "observePulls": True},
                },
                "revision": 0,
            },
        )
        self.assertEqual(evaluation["path"], API + "settings/eval")
        self.assertEqual(evaluation["body"], {"value": {**EVAL_DEFAULT, "mode": "observe"}, "revision": 0})
        # The Router restarts after a save while setup is pending: the lever reads the settings again before the next PUT.
        methods = [(entry["method"], entry["path"].removeprefix(API)) for entry in self.api.requests]
        self.assertEqual(
            methods,
            [
                ("GET", "settings"),
                ("PUT", "settings/source:github"),
                ("GET", "settings"),
                ("GET", "settings"),
                ("PUT", "settings/eval"),
            ],
        )
        self.assertEqual(
            run.stdout,
            "source:github saved (revision 1, restarting)\neval saved (revision 1, restarting)\n",
        )
        self.assertEqual(
            self.api.source["config"], {"repository": "mryfmo/dotfiles", "cli": str(WRAPPER), "observePulls": True}
        )
        self.assertEqual(self.api.eval["mode"], "observe")
        self.assertNotIn("auto", json.dumps(self.api.requests))
        # The second run: the store already holds the values, so no PUT and the revisions are named as read.
        self.api.requests.clear()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(self.puts(), [])
        self.assertEqual([entry["method"] for entry in self.api.requests], ["GET"])
        self.assertEqual(run.stdout, "source:github unchanged (revision 1)\neval unchanged (revision 1)\n")
        # A panel setting beside the kit's rows (pollSeconds) is carried, not reset.
        self.api.source["config"]["pollSeconds"] = 120
        self.api.source["config"]["repository"] = "someone/else"
        self.api.requests.clear()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        (source,) = self.puts()
        self.assertEqual(
            source["body"]["value"]["config"],
            {"repository": "mryfmo/dotfiles", "cli": str(WRAPPER), "observePulls": True, "pollSeconds": 120},
        )
        self.assertEqual(source["body"]["revision"], 1)

    def test_a_stale_revision_a_rejected_header_and_an_unreachable_port_are_each_a_refusal_naming_it(self):
        self.api.signed_out = False
        self.api.stale = True
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertIn(
            f"router-settings-apply: the Management API at 127.0.0.1:{self.api.port} answered 409 to PUT settings/source:github: "
            "the revision read was stale (Settings changed. Reload before saving.)",
            run.stderr,
        )
        self.assertEqual(
            [entry["method"] for entry in self.api.requests], ["GET", "PUT"], "the revision was read first"
        )
        self.assertEqual(self.api.eval["mode"], "off", "nothing else was written after the refusal")
        self.api.stale = False
        self.api.reject_header = True
        self.api.requests.clear()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"router-settings-apply: the Management API at 127.0.0.1:{self.api.port} answered 403 to GET settings: the "
            "x-orchestrator-request header or the Host was not accepted (Same-origin management request required)",
            run.stderr,
        )
        self.assertEqual(self.puts(), [], "no PUT after a refused GET")
        self.assertNotIn("Traceback", run.stderr)
        # A port nobody listens on: the refusal names the address and nothing was written anywhere.
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            closed = probe.getsockname()[1]
        self.profile.write_text(PROFILE.read_text().replace("    port: 3082\n", f"    port: {closed}\n"))
        self.api.requests.clear()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"router-settings-apply: the Management API at 127.0.0.1:{closed} is unreachable for GET settings: ",
            run.stderr,
        )
        self.assertEqual(self.api.requests, [])

    def test_a_source_save_before_the_token_names_the_setup_code_saves_the_mode_and_exits_2(self):
        # Upstream probes `<cli> api user` before saving source:github; without the agent account's login the answer is
        # 400 with setup agentCliSignedOut and nothing is saved. The lever names it, still saves eval, and exits 2.
        run = self.run_lever()
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(run.stdout, "eval saved (revision 1, restarting)\n")
        self.assertIn(
            f"router-settings-apply: the Management API at 127.0.0.1:{self.api.port} answered 400 to PUT settings/source:github: "
            "setup agentCliSignedOut: The agent GitHub CLI cannot read its account.; the agent account's gh login under the "
            "credential root router-gh names is the operator's step (docs/engagement-handout.md), after which this lever runs again",
            run.stderr,
        )
        self.assertEqual(self.api.source, {"enabled": True, "config": {}}, "the Router saved no Source row")
        self.assertEqual(self.api.eval["mode"], "observe")
        # After the operator's step the same run saves the Source and finds the mode in place.
        self.api.signed_out = False
        self.api.requests.clear()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(run.stdout, "source:github saved (revision 1, restarting)\neval unchanged (revision 1)\n")
        self.assertEqual(self.api.source["config"]["repository"], "mryfmo/dotfiles")

    def test_auto_an_absent_row_a_missing_port_a_foreign_host_and_a_missing_block_each_refuse(self):
        self.api.signed_out = False
        text = MANIFEST.read_text()
        row = '        accept_mode: observe\n        accept_mode_row: "2026-11-06T23:24:00Z"\n'
        self.assertIn(row, text, "the manifest's Source row as this test knows it")
        manifests = {
            "auto": text.replace(row, "        accept_mode: auto\n        accept_mode_row: \"2026-11-06T23:24:00Z\"\n        accept_mode_auto_row: \"2026-11-07T00:00:00Z\"\n"),
            "no-row": text.replace(row, "        accept_mode_row: \"2026-11-06T23:24:00Z\"\n"),
            "no-mapping": text.replace("    sources:\n      github:\n        repository: mryfmo/dotfiles\n" + row, ""),
            "bad-repository": text.replace("        repository: mryfmo/dotfiles\n", "        repository: mryfmo\n"),
        }  # fmt: skip
        expected = {
            "auto": "assets.dsh-superagent.sources.github.accept_mode 'auto' in {path} is not applied by this lever; it applies off or observe alone, and the M-18 ladder's second rung is the operator's row",
            "no-row": "the manifest {path} names no assets.dsh-superagent.sources.github.accept_mode",
            "no-mapping": "the manifest {path} names no assets.dsh-superagent.sources.github mapping",
            "bad-repository": "assets.dsh-superagent.sources.github.repository 'mryfmo' in {path} is not owner/name",
        }
        for case, altered in manifests.items():
            with self.subTest(case=case):
                self.assertNotEqual(altered, text, "the fixture changed the manifest")
                path = self.dir / f"{case}.yaml"
                path.write_text(altered)
                run = self.run_lever("--manifest", str(path))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr, "router-settings-apply: " + expected[case].format(path=path) + "\n")
                self.assertEqual(self.api.requests, [], "no request before the manifest is read whole")
        run = self.run_lever("--manifest", str(self.dir / "absent.yaml"))
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"router-settings-apply: the manifest {self.dir / 'absent.yaml'} could not be read: ", run.stderr)
        # The profile refusals, each before any request.
        self.profile.write_text(PROFILE.read_text().replace("    port: 3082\n", ""))
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"router-settings-apply: the router profile {self.profile} names no webserver host and port in the rendered form\n",
        )
        self.profile.write_text(
            PROFILE.read_text()
            .replace("    host: 127.0.0.1\n", "    host: 0.0.0.0\n")
            .replace("    port: 3082\n", f"    port: {self.api.port}\n")
        )
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"router-settings-apply: the router profile {self.profile} binds the webserver to 0.0.0.0, not 127.0.0.1\n",
        )
        self.assertEqual(self.api.requests, [])
        # A settings view without the github Source or the eval block is a refusal naming the block, and nothing is PUT.
        self.profile.write_text(PROFILE.read_text().replace("    port: 3082\n", f"    port: {self.api.port}\n"))
        for missing in ("github", "eval"):
            with self.subTest(missing=missing):
                self.api.view_without = missing
                self.api.requests.clear()
                run = self.run_lever()
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"answered GET settings without the {'Source github' if missing == 'github' else 'eval block'}",
                    run.stderr,
                )
                self.assertEqual(self.puts(), [])

    def test_the_wrapper_runs_gh_under_the_credential_roots_config_dir_with_no_caller_token(self):
        # router-gh: GH_CONFIG_DIR is <DSH_HOME>/router-credentials/gh (physical), the token names and GH_HOST are gone,
        # every argument reaches gh; an absent root, a link there, a relative DSH_HOME and an absent gh each refuse.
        fake = self.dir / "fake"
        fake.mkdir()
        record = self.dir / "gh-calls"
        (fake / "gh").write_text(
            "#!/bin/sh\n"
            f'printf \'%s\\n\' "$*" "${{GH_CONFIG_DIR-unset}}" "${{GH_TOKEN-unset}}" "${{GITHUB_TOKEN-unset}}" "${{GH_HOST-unset}}" > {record}\n'
            "exit 7\n"
        )
        (fake / "gh").chmod(0o755)
        dsh_home = self.dir / "dsh-home"
        root = dsh_home / "router-credentials"
        root.mkdir(parents=True)
        env = {**self.env, "PATH": f"{fake}:{self.env['PATH']}", "DSH_HOME": str(dsh_home), "GH_TOKEN": "caller-" + "value",
               "GITHUB_TOKEN": "caller-" + "value", "GH_HOST": "example.invalid"}  # fmt: skip
        run = subprocess.run(
            [str(WRAPPER), "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
            check=False,
            env=env,
            timeout=60,
        )
        self.assertEqual((run.returncode, run.stderr), (7, ""), run.stdout)
        self.assertEqual(record.read_text(), f"api user --jq .login\n{root.resolve()}/gh\nunset\nunset\nunset\n")
        # DSH_HOME unset: ~/.dsh under the scratch HOME.
        home_root = Path(self.env["HOME"]) / ".dsh/router-credentials"
        home_root.mkdir(parents=True)
        run = subprocess.run(
            [str(WRAPPER), "auth", "status"],
            capture_output=True,
            text=True,
            check=False,
            env={k: v for k, v in env.items() if k != "DSH_HOME"},
            timeout=60,
        )
        self.assertEqual(run.returncode, 7, run.stderr)
        self.assertEqual(record.read_text().splitlines()[1], f"{home_root.resolve()}/gh")
        record.unlink()
        # A PATH holding the self-check's tools (sed, the hash tool) and no gh: the refusal names gh.
        tools = self.dir / "tools"
        tools.mkdir()
        for tool in ("sed", shutil.which("sha256sum") and "sha256sum" or "shasum"):
            (tools / tool).symlink_to(Path(shutil.which(tool)).resolve())
        cases = (
            ({"DSH_HOME": "relative/dsh"}, "router-gh: DSH_HOME 'relative/dsh' is not an absolute path"),
            (
                {"DSH_HOME": str(self.dir / "absent")},
                f"router-gh: the credential root {self.dir / 'absent'}/router-credentials is not a directory;",
            ),
            ({"PATH": str(tools)}, "router-gh: gh not found on PATH"),
        )
        for overrides, message in cases:
            with self.subTest(message=message):
                run = subprocess.run(
                    [str(WRAPPER), "api", "user"],
                    capture_output=True,
                    text=True,
                    check=False,
                    env={**env, **overrides},
                    timeout=60,
                )
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertFalse(record.exists(), "gh did not run")
        shutil.rmtree(root)
        root.symlink_to(Path(self.env["HOME"]) / ".config/gh")
        run = subprocess.run(
            [str(WRAPPER), "api", "user"], capture_output=True, text=True, check=False, env=env, timeout=60
        )
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"router-gh: the credential root {root} is a symbolic link; it must be a real directory inside DSH_HOME",
            run.stderr,
        )
        self.assertFalse(record.exists())

    def test_the_installed_copies_are_the_checkout_bytes_the_pins_are_current_and_an_altered_copy_refuses(self):
        # The lever and the wrapper are pinned like every lever (claude.levers.sha256): the chezmoi copy holds the same
        # bytes, the pin is their sha256, and an installed copy whose bytes differ refuses (exit 2, nothing on stdout)
        # before it reads or runs anything, naming the digest and the deployed manifest.
        text = MANIFEST.read_text()
        home = self.dir / "installed"
        (home / ".local/bin/common").mkdir(parents=True)
        (home / ".agents").mkdir()
        shutil.copy2(MANIFEST, home / ".agents/agent-config.yaml")
        env = {**self.env, "HOME": str(home)}
        for name, source, installed in (
            ("router-settings-apply", LEVER, INSTALLED),
            ("router-gh", WRAPPER, INSTALLED_WRAPPER),
        ):
            with self.subTest(lever=name):
                self.assertEqual(source.read_bytes(), installed.read_bytes(), "the deployed copy holds the same bytes")
                self.assertTrue(os.access(source, os.X_OK) and os.access(installed, os.X_OK))
                pin = re.search(rf"^      {re.escape(name)}: ([0-9a-f]{{64}})$", text, re.MULTILINE)
                self.assertIsNotNone(pin, f"one pin row for {name}")
                self.assertEqual(
                    hashlib.sha256(source.read_bytes()).hexdigest(), pin[1], "the committed pin is current"
                )
                copy_path = home / ".local/bin/common" / name
                shutil.copy2(installed, copy_path)
                argv = (
                    [sys.executable, "-I", str(copy_path), "--help"]
                    if name.endswith("apply")
                    else [str(copy_path), "--version"]
                )
                run = subprocess.run(
                    argv, capture_output=True, text=True, check=False, env=env, timeout=60, cwd=self.dir
                )
                self.assertNotIn("refused:", run.stderr, "the pinned copy passes its self-check")
                with copy_path.open("a") as handle:
                    handle.write('print("rewritten")\n' if name.endswith("apply") else "echo rewritten\n")
                altered = hashlib.sha256(copy_path.read_bytes()).hexdigest()
                run = subprocess.run(
                    argv, capture_output=True, text=True, check=False, env=env, timeout=60, cwd=self.dir
                )
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(
                    run.stderr,
                    f"{name}: refused: sha256 {altered} of {copy_path.resolve()} differs from the pin in {home}/.agents/agent-config.yaml\n",
                )
        # The credential root itself is not made by either lever: nothing under the scratch HOME beyond the layout.
        self.assertEqual(sorted(p.name for p in home.iterdir()), [".agents", ".local"])
        self.assertEqual(stat.S_IMODE((home / ".local/bin/common/router-gh").stat().st_mode) & 0o100, 0o100)


if __name__ == "__main__":
    unittest.main()
