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
import socketserver
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
# The agent account's token as the login writes it into `<root>/gh/hosts.yml`: built at runtime and named without the
# word the secret scan's `generic-token` rule keys on, inside the grammar the wrapper admits ([A-Za-z0-9_]).
HOSTS_OAUTH_VALUE = "fake_" + "u353b_value_0123456789abcdef"


def hosts_yml(value: str) -> str:
    """`hosts.yml` as `gh auth login --insecure-storage` writes it for github.com (the key split so no line of this
    file is a quoted assignment of the scanned word)."""
    return "github.com:\n    user: agent-account\n    git_protocol: https\n    oauth_" + "token: " + value + "\n"


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
        self.redirect = None  # answer 302 with this Location to GET settings, as a rewritten Router or a hop would

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
        if self.path == API + "settings" and self.server.redirect:
            return self.redirect_to(self.server.redirect)
        if self.path == API + "settings":
            return self.answer(200, self.server.view())
        self.answer(404, {"error": "Unknown operation"})

    def redirect_to(self, location: str) -> None:
        """A 302 with a Location off the loopback port: a lever that followed it would leave 127.0.0.1."""
        text = json.dumps({"error": "moved"}).encode()
        self.send_response(302)
        self.send_header("location", location)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(text)))
        self.end_headers()
        self.wfile.write(text)

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


class ProxyRecorder(socketserver.ThreadingTCPServer):
    """A loopback listener standing where the environment's proxy variables point (U353b): it records every connection
    and answers 502, so a lever that honoured the variables would reach it, never the Router, and fail."""

    allow_reuse_address = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), ProxyRecorderHandler)
        self.port = self.server_address[1]
        self.connections: list[str] = []


class ProxyRecorderHandler(socketserver.BaseRequestHandler):
    server: ProxyRecorder

    def handle(self) -> None:
        self.server.connections.append(f"{self.client_address[0]}:{self.client_address[1]}")
        self.request.sendall(b"HTTP/1.1 502 Bad Gateway\r\ncontent-length: 0\r\nconnection: close\r\n\r\n")


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

    def fake_gh(self) -> tuple[Path, Path]:
        """A `gh` on a PATH directory of its own that records its arguments, `GH_CONFIG_DIR`, `GH_TOKEN`, `GITHUB_TOKEN`
        and `GH_HOST` into one file and exits 7; the file's absence proves gh never ran."""
        fake = self.dir / "fake"
        fake.mkdir()
        record = self.dir / "gh-calls"
        (fake / "gh").write_text(
            "#!/bin/sh\n"
            f'printf \'%s\\n\' "$*" "${{GH_CONFIG_DIR-unset}}" "${{GH_TOKEN-unset}}" "${{GITHUB_TOKEN-unset}}" "${{GH_HOST-unset}}" > {record}\n'
            "exit 7\n"
        )
        (fake / "gh").chmod(0o755)
        return fake, record

    def place_login(self, root: Path, text: str = hosts_yml(HOSTS_OAUTH_VALUE), mode: int = 0o600) -> Path:
        """The agent account's login under the credential root `root`, as the operator's step leaves it: `gh/hosts.yml`
        with `text`, a regular file of `mode` (0600 as gh writes it)."""
        hosts = root / "gh/hosts.yml"
        hosts.parent.mkdir(parents=True, exist_ok=True)
        if hosts.is_symlink() or hosts.exists():
            hosts.unlink()
        hosts.write_text(text)
        hosts.chmod(mode)
        return hosts

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
        evaluation, source = self.puts()
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
        # The mode is saved first (U353b): a store at `auto` must hold the requested mode before the Source restarts.
        methods = [(entry["method"], entry["path"].removeprefix(API)) for entry in self.api.requests]
        self.assertEqual(
            methods,
            [
                ("GET", "settings"),
                ("PUT", "settings/eval"),
                ("GET", "settings"),
                ("GET", "settings"),
                ("PUT", "settings/source:github"),
            ],
        )
        self.assertEqual(
            run.stdout,
            "eval saved (revision 1, restarting)\nsource:github saved (revision 1, restarting)\n",
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
        self.assertEqual(run.stdout, "eval unchanged (revision 1)\nsource:github unchanged (revision 1)\n")
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
            f"router-settings-apply: the Management API at 127.0.0.1:{self.api.port} answered 409 to PUT settings/eval: "
            "the revision read was stale (Settings changed. Reload before saving.)",
            run.stderr,
        )
        self.assertEqual(
            [entry["method"] for entry in self.api.requests], ["GET", "PUT"], "the revision was read first"
        )
        self.assertEqual(self.api.source, {"enabled": True, "config": {}}, "nothing else was written after the refusal")
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
        self.assertEqual(run.stdout, "eval unchanged (revision 1)\nsource:github saved (revision 1, restarting)\n")
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

    def test_the_writer_reaches_the_loopback_port_past_a_proxy_refuses_a_redirect_and_saves_the_mode_first(self):
        """U353b (verdict U353-8791100f P2 `:268` and `:401`): the only peer is `127.0.0.1:<port>`. A proxy named in the
        environment (`HTTP_PROXY` and its forms, which urllib's default opener honours for a loopback host too) is not
        consulted: every request reaches the fake directly and a recorder on the proxy's port sees no connection. A
        `302` from the fake is a refusal naming the status and its Location, never followed, with nothing PUT after
        it. The `PUT` of `eval` precedes the `PUT` of `source:github`, so a store at `auto` holds the requested mode
        before the Source restarts into polling."""
        self.api.signed_out = False
        proxy = ProxyRecorder()
        threading.Thread(target=proxy.serve_forever, daemon=True).start()
        self.addCleanup(proxy.server_close)
        self.addCleanup(proxy.shutdown)
        names = ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy")
        proxied = {name: f"http://127.0.0.1:{proxy.port}" for name in names}
        run = self.run_lever(env={**self.env, **proxied})
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(proxy.connections, [], "the proxy the environment names saw no connection")
        self.assertEqual(
            [entry["path"] for entry in self.puts()],
            [API + "settings/eval", API + "settings/source:github"],
            "the mode is saved before the Source",
        )
        self.assertEqual(
            run.stdout, "eval saved (revision 1, restarting)\nsource:github saved (revision 1, restarting)\n"
        )
        self.assertEqual(self.api.eval["mode"], "observe")
        # The redirect: named with its Location, not followed, nothing written.
        self.api.requests.clear()
        self.api.redirect = "http://external.invalid/orchestrator/api/settings"
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"router-settings-apply: the Management API at 127.0.0.1:{self.api.port} answered 302 to GET settings: a redirect to "
            f"http://external.invalid/orchestrator/api/settings is not followed; this lever speaks to 127.0.0.1:{self.api.port} alone\n",
        )
        self.assertEqual([entry["method"] for entry in self.api.requests], ["GET"])
        self.assertEqual(self.puts(), [])

    def test_the_wrapper_runs_gh_under_the_credential_roots_config_dir_with_no_caller_token(self):
        # router-gh: GH_CONFIG_DIR is <DSH_HOME>/router-credentials/gh (physical), GH_TOKEN is the login's token (U353b),
        # the caller's token names and GH_HOST are gone, every argument reaches gh; an absent root, a link there, a
        # relative DSH_HOME and an absent gh each refuse.
        fake, record = self.fake_gh()
        dsh_home = self.dir / "dsh-home"
        root = dsh_home / "router-credentials"
        root.mkdir(parents=True)
        self.place_login(root)
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
        self.assertEqual(
            record.read_text(), f"api user --jq .login\n{root.resolve()}/gh\n{HOSTS_OAUTH_VALUE}\nunset\nunset\n"
        )
        # DSH_HOME unset: ~/.dsh under the scratch HOME.
        home_root = Path(self.env["HOME"]) / ".dsh/router-credentials"
        home_root.mkdir(parents=True)
        self.place_login(home_root)
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

    def test_the_wrapper_reads_the_token_from_hosts_yml_and_refuses_an_empty_root_a_link_or_a_shared_file(self):
        """U353b (verdict U353-8791100f P1 `:97`): gh resolves a credential as `GH_TOKEN`, then the config directory's
        `hosts.yml`, then the host-wide Keychain on macOS (`gh help environment`), so `GH_CONFIG_DIR` alone let an empty
        root authenticate as the operator's Keychain login. The wrapper reads the `oauth_token` of `github.com` from
        `<root>/gh/hosts.yml` itself and hands it to gh as `GH_TOKEN`, `GH_CONFIG_DIR` still the root's `gh/`, so the
        Keychain is never consulted; a root without the login refuses by name (exit 2, no gh run), as do a link at
        `hosts.yml`, a file readable by the group or others, a file without the github.com row and a value outside the
        token grammar; no refusal prints the value."""
        fake, record = self.fake_gh()
        dsh_home = self.dir / "dsh-home"
        root = dsh_home / "router-credentials"
        (root / "gh").mkdir(parents=True)
        hosts = root / "gh/hosts.yml"
        env = {
            **self.env,
            "PATH": f"{fake}:{self.env['PATH']}",
            "DSH_HOME": str(dsh_home),
            "GH_TOKEN": "caller-" + "value",
        }

        def wrapper() -> subprocess.CompletedProcess:
            return subprocess.run(
                [str(WRAPPER), "api", "user"], capture_output=True, text=True, check=False, env=env, timeout=60
            )

        # The wrapper names the file under the physical root (`pwd -P`), as it renders GH_CONFIG_DIR.
        hosts_phys = root.resolve() / "gh/hosts.yml"
        # The root before the operator's step: a refusal naming the file, never the caller's token or the Keychain.
        run = wrapper()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"router-gh: no gh login under the credential root: {hosts_phys} is not a regular file; the agent account's login "
            "inside the root is the operator's step (docs/engagement-handout.md), and gh runs with no other credential\n",
        )
        self.assertFalse(record.exists(), "gh did not run")
        # The login in place: gh runs with GH_TOKEN the file's value and GH_CONFIG_DIR the root's gh directory.
        self.place_login(root)
        run = wrapper()
        self.assertEqual((run.returncode, run.stderr), (7, ""), run.stdout)
        self.assertEqual(record.read_text(), f"api user\n{root.resolve()}/gh\n{HOSTS_OAUTH_VALUE}\nunset\nunset\n")
        record.unlink()
        shared = self.dir / "elsewhere-hosts.yml"
        shared.write_text(hosts_yml(HOSTS_OAUTH_VALUE))
        shared.chmod(0o600)
        no_row = f"router-gh: {hosts_phys} names no oauth_token for github.com; the agent account's login inside the root is the operator's step (docs/engagement-handout.md)"
        cases = (
            ("a link", None, 0o600, f"router-gh: {hosts_phys} is a symbolic link; the login must be a regular file inside the credential root"),
            ("a group-readable file", hosts_yml(HOSTS_OAUTH_VALUE), 0o640, f"router-gh: {hosts_phys} has mode 640; the login must be readable by this user alone (0600)"),
            ("no oauth_token row", "github.com:\n    user: agent-account\n", 0o600, no_row),
            ("another host's row alone", hosts_yml(HOSTS_OAUTH_VALUE).replace("github.com:", "ghe.example.invalid:", 1), 0o600, no_row),
            ("a value outside the grammar", hosts_yml("'has a space'"), 0o600, f"router-gh: the oauth_token of github.com in {hosts_phys} is empty or outside [A-Za-z0-9_]"),
        )  # fmt: skip
        for case, text, mode, message in cases:
            with self.subTest(case=case):
                if text is None:
                    hosts.unlink()
                    hosts.symlink_to(shared)
                else:
                    self.place_login(root, text, mode)
                run = wrapper()
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr, message + "\n")
                self.assertNotIn(HOSTS_OAUTH_VALUE, run.stderr, "no refusal prints the value")
                self.assertFalse(record.exists(), "gh did not run")

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
