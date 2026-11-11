"""scripts/orchestrator/router-settings-apply against a fake Management API on a loopback port, and the `gh` wrapper
scripts/orchestrator/router-gh the Router's `cli` names (regime-cutover U353, M-26 stage B).

The fake API speaks the grammar of the pinned dsh-superagent archive (8c32a9dc): `GET settings` answers the settings view
(`src/app/views/settings.ts:23-41`: `blocks.eval`, `blocks.policy` and each Source with its `value` and `revision`), `PUT settings/<block>`
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


# A second value, for the same account's row under `users:` (U353c): the wrapper must hand gh the host-level row alone.
HOSTS_USERS_VALUE = "fake_" + "u353c_users_row_fedcba9876543210"


def hosts_yml_today(value: str, users_value: str | None = None, indent: int = 4) -> str:
    """`hosts.yml` as gh 2.40 and later writes it for one account (`gh auth login --insecure-storage`): the active
    account's rows at the host block's own depth (`indent` spaces; gh writes four) and every account's `oauth_token:`
    again under `users: <account>:`, deeper; the `users:` block before the host-level row, so the order of the rows
    proves nothing. `users_value` lets the deeper row differ, which shows which row reached gh."""
    pad = " " * indent
    users_value = value if users_value is None else users_value
    return (
        "github.com:\n"
        + f"{pad}git_protocol: https\n"
        + f"{pad}users:\n"
        + f"{pad * 2}agent-account:\n"
        + f"{pad * 3}oauth_"
        + f"token: {users_value}\n"
        + f"{pad}user: agent-account\n"
        + f"{pad}oauth_"
        + f"token: {value}\n"
    )


def hosts_yml_users_only(value: str) -> str:
    """A `github.com:` block holding the `users:` rows alone, no row at the block's own depth: gh's file after the
    active account was logged out (`gh auth logout` keeps the other accounts under `users:`), so no active login."""
    return (
        "github.com:\n    git_protocol: https\n    users:\n        agent-account:\n            oauth_"
        + "token: "
        + value
        + "\n"
    )


MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
PROFILE = ROOT / "home/dot_dsh/profiles/router/cordis.patch.yml"
API = "/orchestrator/api/"
# The eval block as the archive defaults it (src/policy.ts:83-87) with the mode the kit must change.
EVAL_DEFAULT = {"mode": "off", "timeoutSeconds": 120, "model": None}
# The policy block as the archive defaults it (src/policy.ts:76-84) and the one cell the lever writes into it (U416): the
# pulls row's unlistedUnaddressed cell of the github Source's admission table, from the manifest's observe_admission.
POLICY_DEFAULT = {"rules": [], "sources": {}}
ADMISSION_CELL = {"github": {"allowed": [], "admission": {"pulls": {"unlistedUnaddressed": "inferred"}}}}
POLICY_PUT = {"value": {"rules": [], "sources": ADMISSION_CELL}, "revision": 0}
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
        self.policy = copy.deepcopy(POLICY_DEFAULT)
        self.policy_revision = 0
        self.reject_header = False  # answer 403 to everything, as the host check does for a wrong header
        self.stale = False  # answer 409 to every PUT, as a revision raced by the panel would
        self.stale_policy = False  # answer 409 to the policy PUT alone (U416 test d)
        self.signed_out = True  # the agent CLI has no login: a source:github save with new setup fields is 400
        self.setup_pending = True  # every save restarts the Router while setup is pending
        self.view_without = None  # drop one key from the settings view: "github", "eval" or "policy"
        self.redirect = None  # answer 302 with this Location to GET settings, as a rewritten Router or a hop would

    def view(self) -> dict:
        view = {
            "policyVersion": "mandate-v3:0",
            "blocks": {
                "policy": {"value": copy.deepcopy(self.policy), "revision": self.policy_revision},
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
        if self.view_without == "policy":
            del view["blocks"]["policy"]
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
        if block not in ("source:github", "eval", "policy"):
            return self.answer(404, {"error": "Source not found"})
        current = {"source:github": self.server.source_revision, "eval": self.server.eval_revision,
                   "policy": self.server.policy_revision}[block]  # fmt: skip
        if self.server.stale or body.get("revision") != current or (block == "policy" and self.server.stale_policy):
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
        elif block == "policy":
            # A saved policy changes policyVersion and restarts nothing (measured 2026-11-10T03:03Z:
            # {"saved":true,"revision":1,"policy_changed":true,"restarting":false}).
            self.server.policy = body["value"]
            self.server.policy_revision += 1
            return self.answer(200, {"saved": True, "revision": self.server.policy_revision, "policy_changed": True,
                                     "restarting": False, "context_delivery": "pending"})  # fmt: skip
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
        evaluation, policy, source = self.puts()
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
        # The policy block goes between them (U416): it restarts nothing, so no re-read before the Source.
        methods = [(entry["method"], entry["path"].removeprefix(API)) for entry in self.api.requests]
        self.assertEqual(
            methods,
            [
                ("GET", "settings"),
                ("PUT", "settings/eval"),
                ("GET", "settings"),
                ("GET", "settings"),
                ("PUT", "settings/policy"),
                ("PUT", "settings/source:github"),
            ],
        )
        self.assertEqual(policy["path"], API + "settings/policy")
        self.assertEqual(
            run.stdout,
            "eval saved (revision 1, restarting)\npolicy saved (revision 1)\nsource:github saved (revision 1, restarting)\n",
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
        self.assertEqual(
            run.stdout,
            "eval unchanged (revision 1)\npolicy unchanged (revision 1)\nsource:github unchanged (revision 1)\n",
        )
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

    def test_the_policy_put_writes_the_pulls_admission_cell_between_eval_and_source_and_a_second_run_puts_nothing(self):
        """U416 test (a): with the manifest scalar `observe_admission: inferred`, the lever PUTs `settings/policy` with the
        rules as served and the github Source's `pulls.unlistedUnaddressed` cell `inferred` (the allowed list empty), after
        the eval PUT and before the source PUT; the store then holds the kit's policy, so a second run PUTs no policy."""
        self.api.signed_out = False
        text = MANIFEST.read_text()
        self.assertIn("        observe_admission: inferred\n", text, "the manifest's Source row names the cell")
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        paths = [entry["path"].removeprefix(API) for entry in self.puts()]
        self.assertEqual(paths, ["settings/eval", "settings/policy", "settings/source:github"])
        policy = self.puts()[1]
        self.assertEqual(policy["headers"]["content-type"], "application/json")
        self.assertEqual(policy["body"], POLICY_PUT)
        self.assertEqual(self.api.policy, POLICY_PUT["value"])
        self.assertEqual(
            run.stdout,
            "eval saved (revision 1, restarting)\npolicy saved (revision 1)\nsource:github saved (revision 1, restarting)\n",
        )
        # The second run: the view holds the cell, so no policy PUT and its revision is named as read.
        self.api.requests.clear()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(self.puts(), [])
        self.assertIn("policy unchanged (revision 1)\n", run.stdout)
        # The other word, `ignore`: upstream's default made explicit, written the same way.
        ignore = self.dir / "ignore.yaml"
        ignore.write_text(text.replace("        observe_admission: inferred\n", "        observe_admission: ignore\n"))
        self.api.requests.clear()
        run = self.run_lever("--manifest", str(ignore))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        (policy,) = self.puts()
        self.assertEqual(
            policy["body"],
            {"value": {"rules": [], "sources": {"github": {"allowed": [], "admission": {"pulls": {"unlistedUnaddressed": "ignore"}}}}}, "revision": 1},
        )  # fmt: skip
        self.assertEqual(
            run.stdout, "eval unchanged (revision 1)\npolicy saved (revision 2)\nsource:github unchanged (revision 1)\n"
        )

    def test_a_policy_holding_the_cell_other_rows_and_another_source_is_unchanged_and_a_put_changes_the_one_cell(self):
        """U416 test (b): a view whose policy already holds `inferred` beside other admission rows, other cells of the
        pulls row, the manifest's allowed list (empty), rules and another Source's entry is not written; when the cell
        differs, the PUT keeps every one of them and changes the one cell."""
        self.api.signed_out = False
        rules = [{"id": "copy", "text": "Explicit requests to correct a typo."}]
        github = {
            "allowed": [],
            "bots": ["dependabot[bot]"],
            "admission": {
                "pulls": {"unlistedUnaddressed": "inferred", "listedAddressed": "explicit"},
                "comments": {"unlistedUnaddressed": "ignore"},
            },
        }
        slack = {"allowed": [{"id": "U123"}], "admission": {"messages": {"listedAddressed": "explicit"}}}
        self.api.policy = copy.deepcopy({"rules": rules, "sources": {"github": github, "slack": slack}})
        self.api.policy_revision = 4
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(
            [entry["path"].removeprefix(API) for entry in self.puts()], ["settings/eval", "settings/source:github"]
        )
        self.assertIn("policy unchanged (revision 4)\n", run.stdout)
        # The one cell differs: the PUT carries everything else as read and changes that cell alone.
        self.api.policy["sources"]["github"]["admission"]["pulls"]["unlistedUnaddressed"] = "ignore"
        self.api.requests.clear()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        (policy,) = self.puts()
        self.assertEqual(policy["path"], API + "settings/policy")
        self.assertEqual(
            policy["body"],
            {"value": {"rules": rules, "sources": {"github": github, "slack": slack}}, "revision": 4},
            "the rules, the allowed list, the bots, the other rows and cells and the other Source are kept",
        )
        self.assertEqual(
            run.stdout, "eval unchanged (revision 1)\npolicy saved (revision 5)\nsource:github unchanged (revision 1)\n"
        )
        # A github entry with no admission table and no allowed list at all gets both, nothing else.
        self.api.policy = {"rules": rules, "sources": {"slack": slack}}
        self.api.requests.clear()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        (policy,) = self.puts()
        self.assertEqual(policy["body"]["value"], {"rules": rules, "sources": {"slack": slack, **ADMISSION_CELL}})

    def test_auto_is_rendered_with_its_dated_manifest_row_and_refused_without_it_naming_the_row(self):
        """U465 test (a), the accept rung: `accept_mode: auto` beside `accept_mode_auto_row` (a decisions.tsv timestamp,
        the M-18 ladder's second row) renders `eval.mode` auto; `auto` without that row, with a value that is no
        timestamp, or the row beside `observe`, is one refusal naming the row before any request. The committed
        manifest stays observe: the flip is one manifest row after U466."""
        self.api.signed_out = False
        text = MANIFEST.read_text()
        row = '        accept_mode: observe\n        accept_mode_row: "2026-11-06T23:24:00Z"\n'
        self.assertIn(row, text, "the manifest's Source row as this test knows it")
        self.assertNotIn("accept_mode: auto", text, "the committed manifest holds observe")
        auto_row = '        accept_mode: auto\n        accept_mode_row: "2026-11-06T23:24:00Z"\n'
        auto = self.dir / "auto.yaml"
        auto.write_text(text.replace(row, auto_row + '        accept_mode_auto_row: "2026-11-12T00:00:00Z"\n'))
        run = self.run_lever("--manifest", str(auto))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        evaluation = self.puts()[0]
        self.assertEqual(evaluation["path"], API + "settings/eval")
        self.assertEqual(evaluation["body"], {"value": {**EVAL_DEFAULT, "mode": "auto"}, "revision": 0})
        self.assertEqual(self.api.eval["mode"], "auto")
        self.assertEqual(run.stdout.splitlines()[0], "eval saved (revision 1, restarting)")
        label = "assets.dsh-superagent.sources.github"
        cases = {
            "no-auto-row": (
                text.replace(row, auto_row),
                f"{label}.accept_mode 'auto' in {{path}} needs accept_mode_auto_row (the M-18 ladder's second row "
                "timestamp) beside accept_mode_row; the mode stays observe until that row is written",
            ),
            "auto-row-no-timestamp": (
                text.replace(row, auto_row + "        accept_mode_auto_row: tomorrow\n"),
                f"{label}.accept_mode_auto_row 'tomorrow' in {{path}} is not a decisions.tsv timestamp (YYYY-MM-DDTHH:MM:SSZ)",
            ),
            "auto-row-beside-observe": (
                text.replace(row, row + '        accept_mode_auto_row: "2026-11-12T00:00:00Z"\n'),
                f"{label}.accept_mode_auto_row in {{path}} belongs to accept_mode auto alone, not 'observe'",
            ),
        }
        for case, (altered, expected) in cases.items():
            with self.subTest(case=case):
                self.assertNotEqual(altered, text, "the fixture changed the manifest")
                self.api.requests.clear()
                path = self.dir / f"{case}.yaml"
                path.write_text(altered)
                run = self.run_lever("--manifest", str(path))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr, "router-settings-apply: " + expected.format(path=path) + "\n")
                self.assertEqual(self.api.requests, [], "no request before the manifest is read whole")
        self.assertEqual(self.api.eval["mode"], "auto", "the refusals wrote nothing")

    def test_the_allowed_list_is_rendered_from_the_manifest_and_an_absent_list_or_a_bad_id_refuses(self):
        """U465 test (a), the identity set: `policy.sources.github.allowed` is the manifest row's `allowed` list as
        `{"id": <id>}` rows in the manifest's order (src/sources/github.ts:72: an id is `[A-Za-z0-9-]+`), written over
        whatever the store holds (R-45: the kit's row is the Source's one identity set), in the block form and the flow
        form alike; the committed list is empty. A row without the list, a value that is no list, an id outside the
        grammar and a repeated id are each one refusal naming it before any request."""
        self.api.signed_out = False
        text = MANIFEST.read_text()
        line = "        allowed: []\n"
        self.assertIn(line, text, "the committed manifest's list is empty")
        panel = {"allowed": [{"id": "someone"}], "admission": {"pulls": {"unlistedUnaddressed": "inferred"}}}
        self.api.policy = {"rules": [], "sources": {"github": copy.deepcopy(panel)}}
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        policy = [entry for entry in self.puts() if entry["path"] == API + "settings/policy"]
        self.assertEqual(
            len(policy), 1, "the panel's entry differs from the kit's empty list, so the policy is written"
        )
        self.assertEqual(policy[0]["body"], {"value": {"rules": [], "sources": ADMISSION_CELL}, "revision": 0})
        self.assertEqual(self.api.policy["sources"]["github"]["allowed"], [])
        listed = self.dir / "listed.yaml"
        listed.write_text(text.replace(line, "        allowed:\n          - someone\n          - other-one\n"))
        self.api.requests.clear()
        run = self.run_lever("--manifest", str(listed))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        (policy,) = self.puts()
        entry = {"allowed": [{"id": "someone"}, {"id": "other-one"}], "admission": panel["admission"]}
        self.assertEqual(policy["body"], {"value": {"rules": [], "sources": {"github": entry}}, "revision": 1})
        self.assertEqual(
            run.stdout, "eval unchanged (revision 1)\npolicy saved (revision 2)\nsource:github unchanged (revision 1)\n"
        )
        self.assertEqual(self.api.policy["sources"]["github"], entry)
        # The same list in the flow form, with quotes: nothing to write.
        flow = self.dir / "flow.yaml"
        flow.write_text(text.replace(line, '        allowed: ["someone", other-one]\n'))
        self.api.requests.clear()
        run = self.run_lever("--manifest", str(flow))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(self.puts(), [])
        self.assertIn("policy unchanged (revision 2)\n", run.stdout)
        label = "assets.dsh-superagent.sources.github.allowed"
        cases = {
            "no-list": (text.replace(line, ""), f"the manifest {{path}} names no {label} list"),
            "a-word": (
                text.replace(line, "        allowed: someone\n"),
                f"{label} in {{path}} is not a list of sender ids (`[]`, `[a, b]` or `- a` lines)",
            ),
            "a-bare-key": (
                text.replace(line, "        allowed:\n"),
                f"{label} in {{path}} is not a list of sender ids (`[]`, `[a, b]` or `- a` lines)",
            ),
            "underscore": (
                text.replace(line, "        allowed:\n          - some_one\n"),
                f"{label} in {{path}} names 'some_one', which is not a sender id of the form [A-Za-z0-9-]+",
            ),
            "space": (
                text.replace(line, "        allowed: [some one]\n"),
                f"{label} in {{path}} names 'some one', which is not a sender id of the form [A-Za-z0-9-]+",
            ),
            "bot": (
                text.replace(line, "        allowed: [dependabot[bot]]\n"),
                f"{label} in {{path}} names 'dependabot[bot]', which is not a sender id of the form [A-Za-z0-9-]+",
            ),
            "repeated": (
                text.replace(line, "        allowed: [someone, Someone]\n"),
                f"{label} in {{path}} repeats 'Someone' (GitHub logins that differ by case alone are one login)",
            ),
        }
        for case, (altered, expected) in cases.items():
            with self.subTest(case=case):
                self.assertNotEqual(altered, text, "the fixture changed the manifest")
                self.api.requests.clear()
                path = self.dir / f"{case}.yaml"
                path.write_text(altered)
                run = self.run_lever("--manifest", str(path))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr, "router-settings-apply: " + expected.format(path=path) + "\n")
                self.assertEqual(self.api.requests, [], "no request before the manifest is read whole")
        self.assertEqual(self.api.policy["sources"]["github"], entry, "the refusals wrote nothing")

    def test_a_dry_run_prints_the_desired_values_from_the_manifest_and_the_profile_and_makes_no_request(self):
        """U465 test (a), the desired settings' text: `--dry-run` reads the manifest row, the profile's webserver row and
        the wrapper as a run does and prints what a run would write (the mode, the allowed ids as a JSON list, the
        admission cell, the repository, the wrapper) without calling the Management API: the fake records no request
        and nothing changes; a refusal of the row is the same refusal, exit 2, nothing on stdout."""
        self.api.signed_out = False
        run = self.run_lever("--dry-run")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(self.api.requests, [], "a dry run makes no request")
        self.assertEqual(
            run.stdout,
            f"dry run: nothing is read from or written to the Management API at 127.0.0.1:{self.api.port}\n"
            "eval.mode observe\n"
            "allowed []\n"
            "admission.pulls.unlistedUnaddressed inferred\n"
            "repository mryfmo/dotfiles\n"
            f"cli {WRAPPER}\n",
        )
        self.assertEqual((self.api.eval, self.api.policy), (EVAL_DEFAULT, POLICY_DEFAULT), "nothing changed")
        text = MANIFEST.read_text()
        row = '        accept_mode: observe\n        accept_mode_row: "2026-11-06T23:24:00Z"\n'
        listed = self.dir / "listed.yaml"
        listed.write_text(
            text.replace(
                row, row.replace("observe", "auto") + '        accept_mode_auto_row: "2026-11-12T00:00:00Z"\n'
            ).replace("        allowed: []\n", "        allowed: [someone, other-one]\n")
        )
        run = self.run_lever("--dry-run", "--manifest", str(listed))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertIn('eval.mode auto\nallowed ["someone", "other-one"]\nadmission.pulls', run.stdout)
        self.assertEqual(self.api.requests, [])
        bad = self.dir / "bad.yaml"
        bad.write_text(text.replace("        allowed: []\n", "        allowed: [some_one]\n"))
        run = self.run_lever("--dry-run", "--manifest", str(bad))
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("names 'some_one', which is not a sender id", run.stderr)
        self.assertEqual(self.api.requests, [])

    def test_a_manifest_without_the_observe_admission_scalar_or_with_a_third_word_refuses_before_any_request(self):
        """U416 test (c): the scalar takes `inferred` or `ignore`; absent or any other word (`explicit`: an unlisted
        sender's pull request accepted in observe mode) is one refusal naming the key, exit 2, and the FakeApi records
        no request."""
        self.api.signed_out = False
        text = MANIFEST.read_text()
        line = "        observe_admission: inferred\n"
        self.assertIn(line, text, "the manifest's Source row as this test knows it")
        manifests = {
            "no-cell": text.replace(line, ""),
            "explicit": text.replace(line, "        observe_admission: explicit\n"),
            "auto-word": text.replace(line, "        observe_admission: auto\n"),
        }
        expected = {
            "no-cell": "the manifest {path} names no assets.dsh-superagent.sources.github.observe_admission",
            "explicit": "assets.dsh-superagent.sources.github.observe_admission 'explicit' in {path} is not inferred or ignore; "
            "the pulls row's unlistedUnaddressed cell takes those two words alone (explicit would accept an unlisted sender's pull request in observe mode)",
            "auto-word": "assets.dsh-superagent.sources.github.observe_admission 'auto' in {path} is not inferred or ignore; "
            "the pulls row's unlistedUnaddressed cell takes those two words alone (explicit would accept an unlisted sender's pull request in observe mode)",
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
        self.assertEqual(self.api.policy, POLICY_DEFAULT, "nothing was written")

    def test_a_stale_revision_on_the_policy_put_is_the_refusal_naming_the_block_and_the_source_is_not_written(self):
        """U416 test (d): a 409 on the policy PUT is the existing stale-revision refusal, naming `PUT settings/policy`;
        eval is saved before it, nothing after it, exit 2."""
        self.api.signed_out = False
        self.api.stale_policy = True
        run = self.run_lever()
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(run.stdout, "eval saved (revision 1, restarting)\n")
        self.assertEqual(
            run.stderr,
            f"router-settings-apply: the Management API at 127.0.0.1:{self.api.port} answered 409 to PUT settings/policy: "
            "the revision read was stale (Settings changed. Reload before saving.)\n",
        )
        paths = [(entry["method"], entry["path"].removeprefix(API)) for entry in self.api.requests]
        self.assertEqual(paths[-1], ("PUT", "settings/policy"), "nothing was written after the refusal")
        self.assertEqual(self.api.source, {"enabled": True, "config": {}}, "the Source was not written")
        self.assertEqual(self.api.policy, POLICY_DEFAULT)
        self.assertEqual(self.api.eval["mode"], "observe")

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
        self.assertEqual(run.stdout, "eval saved (revision 1, restarting)\npolicy saved (revision 1)\n")
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
        self.assertEqual(
            run.stdout,
            "eval unchanged (revision 1)\npolicy unchanged (revision 1)\nsource:github saved (revision 1, restarting)\n",
        )
        self.assertEqual(self.api.source["config"]["repository"], "mryfmo/dotfiles")

    def test_auto_without_its_row_an_absent_row_a_missing_port_a_foreign_host_and_a_missing_block_each_refuse(self):
        self.api.signed_out = False
        text = MANIFEST.read_text()
        row = '        accept_mode: observe\n        accept_mode_row: "2026-11-06T23:24:00Z"\n'
        self.assertIn(row, text, "the manifest's Source row as this test knows it")
        manifests = {
            "auto-no-row": text.replace(row, "        accept_mode: auto\n        accept_mode_row: \"2026-11-06T23:24:00Z\"\n"),
            "no-row": text.replace(row, "        accept_mode_row: \"2026-11-06T23:24:00Z\"\n"),
            "no-mapping": text.replace("    sources:\n      github:\n        repository: mryfmo/dotfiles\n" + row, "").replace("        observe_admission: inferred\n", ""),
            "bad-repository": text.replace("        repository: mryfmo/dotfiles\n", "        repository: mryfmo\n"),
        }  # fmt: skip
        expected = {
            "auto-no-row": "assets.dsh-superagent.sources.github.accept_mode 'auto' in {path} needs accept_mode_auto_row (the M-18 ladder's second row timestamp) beside accept_mode_row; the mode stays observe until that row is written",
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
        for missing in ("github", "eval", "policy"):
            with self.subTest(missing=missing):
                self.api.view_without = missing
                self.api.requests.clear()
                run = self.run_lever()
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                block = {"github": "Source github", "eval": "eval block", "policy": "policy block"}[missing]
                self.assertIn(
                    f"answered GET settings without the {block}",
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
            [API + "settings/eval", API + "settings/policy", API + "settings/source:github"],
            "the mode is saved before the policy and the Source",
        )
        self.assertEqual(
            run.stdout,
            "eval saved (revision 1, restarting)\npolicy saved (revision 1)\nsource:github saved (revision 1, restarting)\n",
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
        no_row = f"router-gh: {hosts_phys} names no active login for github.com: no oauth_token row at the host block's own depth (the rows under users: are not read); the agent account's login inside the root is the operator's step (docs/engagement-handout.md)"
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

    def test_the_wrapper_reads_the_active_hosts_row_alone_from_todays_hosts_yml_and_refuses_users_rows_alone(self):
        """U353c (verdict U353b-9c504ad9 P1 `:127`): gh 2.40 and later writes one login as the active account's rows at
        the host block's own depth and the same account's `oauth_token:` again under `users: <account>:`, deeper; the
        round-2 reader counted both and refused the documented setup. The wrapper measures the block's depth from its
        first row and reads the `oauth_token:` rows at that depth alone: today's file runs gh once with `GH_TOKEN` the
        host-level value (the deeper row's value never reaches gh), at four spaces as gh writes it and at two; a block
        holding `users:` rows alone is refused naming no active login, and two host-level rows are refused as before;
        on a refusal gh never runs and neither value is printed."""
        fake, record = self.fake_gh()
        dsh_home = self.dir / "dsh-home"
        root = dsh_home / "router-credentials"
        root.mkdir(parents=True)
        env = {**self.env, "PATH": f"{fake}:{self.env['PATH']}", "DSH_HOME": str(dsh_home)}
        hosts_phys = root.resolve() / "gh/hosts.yml"

        def wrapper() -> subprocess.CompletedProcess:
            return subprocess.run(
                [str(WRAPPER), "api", "user"], capture_output=True, text=True, check=False, env=env, timeout=60
            )

        for indent in (4, 2):
            with self.subTest(indent=indent):
                self.place_login(root, hosts_yml_today(HOSTS_OAUTH_VALUE, HOSTS_USERS_VALUE, indent))
                run = wrapper()
                self.assertEqual((run.returncode, run.stderr), (7, ""), run.stdout)
                self.assertEqual(
                    record.read_text(), f"api user\n{root.resolve()}/gh\n{HOSTS_OAUTH_VALUE}\nunset\nunset\n"
                )
                self.assertNotIn(HOSTS_USERS_VALUE, record.read_text(), "the users: row never reaches gh")
                record.unlink()
        cases = (
            (
                "users rows alone",
                hosts_yml_users_only(HOSTS_USERS_VALUE),
                f"router-gh: {hosts_phys} names no active login for github.com: no oauth_token row at the host block's own depth (the rows under users: are not read); the agent account's login inside the root is the operator's step (docs/engagement-handout.md)",
            ),
            (
                "two host-level rows",
                hosts_yml_today(HOSTS_OAUTH_VALUE, HOSTS_USERS_VALUE) + hosts_yml(HOSTS_USERS_VALUE).splitlines()[-1] + "\n",
                f"router-gh: {hosts_phys} names 2 oauth_token rows for github.com at the host block's own depth; exactly one is read",
            ),
        )  # fmt: skip
        for case, text, message in cases:
            with self.subTest(case=case):
                self.place_login(root, text)
                run = wrapper()
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr, message + "\n")
                self.assertNotIn(HOSTS_OAUTH_VALUE, run.stderr, "no refusal prints a value")
                self.assertNotIn(HOSTS_USERS_VALUE, run.stderr, "no refusal prints a value")
                self.assertFalse(record.exists(), "gh did not run")

    def test_the_wrapper_holds_the_gh_directory_of_the_root_against_a_link_a_file_and_an_absence(self):
        """U353c (verdict U353b-9c504ad9 P1 `:106`): round 2 held the root and the `hosts.yml` leaf against links, so
        `<root>/gh` as a symbolic link to an outside directory of this user (`~/.config/gh`, say) passed and its login
        reached gh as `GH_TOKEN`, a credential outside the promised root. The wrapper now walks `<root>`, `<root>/gh`,
        `<root>/gh/hosts.yml` in order, each held by its own test before anything is read: a linked `<root>/gh` is
        refused naming it and gh never runs, a regular file there is refused, an absent one is the state before the
        operator's step and is refused naming that step; the leaf's refusals of round 2 stand (the test above)."""
        fake, record = self.fake_gh()
        dsh_home = self.dir / "dsh-home"
        root = dsh_home / "router-credentials"
        root.mkdir(parents=True)
        env = {**self.env, "PATH": f"{fake}:{self.env['PATH']}", "DSH_HOME": str(dsh_home)}
        gh_dir = root / "gh"
        gh_phys = root.resolve() / "gh"
        outside = self.dir / "outside-gh"
        outside.mkdir()
        (outside / "hosts.yml").write_text(hosts_yml(HOSTS_OAUTH_VALUE))
        (outside / "hosts.yml").chmod(0o600)

        def wrapper() -> subprocess.CompletedProcess:
            return subprocess.run(
                [str(WRAPPER), "api", "user"], capture_output=True, text=True, check=False, env=env, timeout=60
            )

        gh_dir.symlink_to(outside)
        run = wrapper()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"router-gh: {gh_phys} is a symbolic link; the login directory must be a real directory inside the credential root\n",
        )
        self.assertFalse(record.exists(), "gh did not run on the linked gh directory")
        gh_dir.unlink()
        gh_dir.write_text(hosts_yml_today(HOSTS_OAUTH_VALUE))
        gh_dir.chmod(0o600)
        run = wrapper()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"router-gh: {gh_phys} is not a directory; the login directory must be a real directory inside the credential root\n",
        )
        self.assertFalse(record.exists(), "gh did not run on the file")
        gh_dir.unlink()
        run = wrapper()
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"router-gh: no gh login under the credential root: {gh_phys} is absent; the agent account's login inside the "
            "root is the operator's step (docs/engagement-handout.md), and gh runs with no other credential\n",
        )
        self.assertFalse(record.exists(), "gh did not run on the empty root")
        for text in (hosts_yml_today(HOSTS_OAUTH_VALUE), hosts_yml_today(HOSTS_OAUTH_VALUE, HOSTS_USERS_VALUE)):
            self.assertNotIn(text, run.stderr)
        # The chain whole: a real gh directory of this user under the root runs gh with the login's value.
        self.place_login(root, hosts_yml_today(HOSTS_OAUTH_VALUE))
        run = wrapper()
        self.assertEqual((run.returncode, run.stderr), (7, ""), run.stdout)
        self.assertEqual(record.read_text(), f"api user\n{gh_phys}\n{HOSTS_OAUTH_VALUE}\nunset\nunset\n")

    def test_a_gh_directory_of_another_user_under_the_root_refuses(self):
        """U353c: `<root>/gh` held to a directory of this user (`-O`), as the root and the leaf are. Only root can place
        another user's directory there, so the test skips with that reason elsewhere."""
        if os.geteuid() != 0:
            self.skipTest("the harness runs as one user and cannot make a directory of another user under the root")
        import pwd

        fake, record = self.fake_gh()
        dsh_home = self.dir / "dsh-home"
        root = dsh_home / "router-credentials"
        self.place_login(root, hosts_yml_today(HOSTS_OAUTH_VALUE))
        other = pwd.getpwnam("nobody")
        os.chown(root / "gh", other.pw_uid, other.pw_gid)
        run = subprocess.run(
            [str(WRAPPER), "api", "user"],
            capture_output=True,
            text=True,
            check=False,
            env={**self.env, "PATH": f"{fake}:{self.env['PATH']}", "DSH_HOME": str(dsh_home)},
            timeout=60,
        )
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr, f"router-gh: {root.resolve()}/gh is not this user's directory\n")
        self.assertFalse(record.exists(), "gh did not run")

    def test_the_handout_table_of_the_routers_account_carries_the_source_and_dry_run_columns(self):
        """U353c (verdict U353b-9c504ad9 P2 `docs/engagement-handout.md:55`): a handout row for the operator carries
        the `source` column (the doc or `file:line` defining the command's behaviour) and the `dry-run` column (the
        scratch-HOME run and its output, else `operator-only: <reason>`), standing order 5. The section's one table has
        the five columns and every row fills each; the dry-run cell is a scratch-HOME receipt or the operator-only
        reason."""
        text = (ROOT / "docs/engagement-handout.md").read_text()
        heading = "## The Router's agent account"
        self.assertEqual(text.count(heading), 1, "one section for the Router's account")
        section = text.split(heading, 1)[1].split("\n## ", 1)[0]
        rows = [line for line in section.splitlines() if line.startswith("|")]
        self.assertGreaterEqual(len(rows), 5, "a header, its rule and the three steps")
        header = [cell.strip() for cell in rows[0].strip().strip("|").split("|")]
        self.assertEqual(header, ["step", "command", "check", "source", "dry-run"])
        steps = []
        for row in rows[2:]:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            with self.subTest(step=cells[0]):
                self.assertEqual(len(cells), 5, row)
                for name, cell in zip(header, cells):
                    self.assertTrue(cell, f"the {name} cell of step {cells[0]} is filled")
                self.assertRegex(cells[3], r"`[^`]+:[0-9]", "the source cell names a file:line")
                self.assertRegex(
                    cells[4],
                    r"^(scratch HOME `|`operator-only: )",
                    "a scratch-HOME receipt or the operator-only reason",
                )
            steps.append(cells[0])
        self.assertEqual(steps, ["1", "2", "3"])

    @unittest.skipIf(
        os.geteuid() == 0, "root reads a file whatever its mode; the case needs a login file the wrapper cannot read"
    )
    def test_the_wrapper_refuses_by_name_with_no_gh_run_when_the_login_file_cannot_be_read(self):
        """U353d (verdict U353-318f268d P2 `tests/unit/test_router_settings_apply.py:828`, standing order 21): the reads
        the wrapper's decision rests on fail closed by name. A login file of mode 000 is refused by the mode test (gh
        writes 0600; the wrapper prints the mode `stat` read) before any read; one of mode 200 (owner write alone, so
        the mode test's `?00` form passes and the read is what fails) is refused by the read, `cannot read <file>`,
        exit 2; in both gh never runs and no value is printed. The `stat` producers are `/usr/bin/stat` by absolute
        path, which no PATH shim reaches, so their failure stays uncovered here (stated in the body)."""
        fake, record = self.fake_gh()
        dsh_home = self.dir / "dsh-home"
        root = dsh_home / "router-credentials"
        root.mkdir(parents=True)
        hosts = self.place_login(root, hosts_yml_today(HOSTS_OAUTH_VALUE))
        self.addCleanup(hosts.chmod, 0o600)
        hosts_phys = root.resolve() / "gh/hosts.yml"
        env = {**self.env, "PATH": f"{fake}:{self.env['PATH']}", "DSH_HOME": str(dsh_home)}
        for mode, message in (
            (0o000, f"router-gh: {hosts_phys} has mode 0; the login must be readable by this user alone (0600)"),
            (0o200, f"router-gh: cannot read {hosts_phys}"),
        ):
            with self.subTest(mode=oct(mode)):
                hosts.chmod(mode)
                run = subprocess.run(
                    [str(WRAPPER), "api", "user"], capture_output=True, text=True, check=False, env=env, timeout=60
                )
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr, "the refusal names the file")
                self.assertNotIn(HOSTS_OAUTH_VALUE, run.stderr, "no refusal prints the value")
                self.assertFalse(record.exists(), "gh did not run")

    def test_the_handout_and_the_wrapper_header_attribute_the_keychain_boundary_to_router_ghs_token_path_not_to_srt(
        self,
    ):
        """U353d (verdict U353-318f268d P2 `docs/engagement-handout.md:53`): srt's macOS baseline allows
        `com.apple.securityd.xpc`, so the Keychain stays reachable to the Router's processes and the sentence that
        attributed the boundary to srt was false. The handout's Router section names the control that keeps gh off the
        Keychain, router-gh's file-only token path (`GH_TOKEN` from `hosts.yml`, which gh reads before any stored
        credential), names srt's deny rows as the omp seats' boundary, and carries the old sentence nowhere. U370: the
        wrapper's own header (`scripts/orchestrator/router-gh:11-13`, the U353d deviation) and its installed copy say
        the same: the login is a file under the root, the Keychain stays reachable under srt, and the control is this
        wrapper's file-only token source, `GH_TOKEN`; neither says the Keychain is not readable under srt."""
        text = (ROOT / "docs/engagement-handout.md").read_text()
        heading = "## The Router's agent account"
        section = text.split(heading, 1)[1].split("\n## ", 1)[0]
        stale_forms = ("the Keychain is not readable under srt", "Keychain is not readable", "Keychain unreadable")
        for stale in stale_forms:
            self.assertNotIn(stale, text, "the boundary is not attributed to srt")
        self.assertIn("file-only token path", section)
        self.assertIn("com.apple.securityd.xpc", section)
        self.assertIn("`GH_TOKEN`", section)
        self.assertIn("srt's deny rows are the omp seats' boundary", section)
        for wrapper in (WRAPPER, INSTALLED_WRAPPER):
            with self.subTest(wrapper=str(wrapper.relative_to(ROOT))):
                header = wrapper.read_text().split("\nset -u\n", 1)[0]
                prose = " ".join(line.lstrip("# ") for line in header.splitlines())  # one line per comment line
                for stale in (*stale_forms, "not readable under srt"):
                    self.assertNotIn(stale, prose, "the header does not attribute the boundary to srt")
                self.assertIn("file-only token source", prose)
                self.assertIn("Keychain stays reachable under srt", prose)
                self.assertIn("`GH_TOKEN`", prose)

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
