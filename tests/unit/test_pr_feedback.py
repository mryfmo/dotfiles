#!/usr/bin/env python3
"""Exercise pr-feedback.py against recorded GitHub API shapes (no network)."""

from __future__ import annotations

import importlib.util
import io
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from typing import Any
from unittest import mock

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/pr-feedback.py"
REPO = "mryfmo/dotfiles"
SHA = "aa17407b680691a42f421721479d7cd14c4421fa"
BASE_SHA = "b" * 40
BOT = {"login": "coderabbitai[bot]", "type": "Bot"}
HUMAN = {"login": "moriya-fumio-thd", "type": "User"}
ACTIONS = {"slug": "github-actions"}


class GhFixture:
    """A measured test namespace: change passwd home, never prebind gh or change consumer bytes."""

    def __init__(self, root):
        self.root, self.home, self.bin, self.calls = root, root / "home", root / "bin", root / "gh.jsonl"
        self.home.mkdir(parents=True, exist_ok=True)
        self.bin.mkdir(exist_ok=True)
        self.responses = root / "responses.json"
        self.responses.write_text(json.dumps({"responses": RESPONSES, "metadata": {}}))
        self.target = self.home / ".local/share/mise/installs/github-cli-cli/2.102.0/bin/gh"
        self.manifest = self.home / ".agents/agent-config.yaml"
        self.declaration()
        self.python = self.bin / "python"
        bootstrap = (
            "import os,pwd,runpy,sys,types\n"
            f"pwd.getpwuid=lambda uid: types.SimpleNamespace(pw_dir={str(self.home)!r})\n"
            f"sys.executable={str(self.python)!r}\n"
            "a=sys.argv[1:]\n"
            f"with open({str(root / 'python.jsonl')!r},'a') as f: f.write(__import__('json').dumps({{'argv':a,'env':dict(os.environ)}})+'\\n')\n"
            "while a and a[0] in ('-I','-P','-s'): a.pop(0)\n"
            "sys.argv=a\n"
            "if a[0]=='-c': exec(compile(a[1],'<fixture>','exec'))\n"
            "else: runpy.run_path(a[0],run_name='__main__')\n"
        )
        self.bootstrap = bootstrap
        self.launcher()
        code = (
            f"#!{sys.executable} -I\n"
            "import json,os,sys\n"
            f"a=sys.argv[1:]; d=json.load(open({str(self.responses)!r}))\n"
            f"with open({str(self.calls)!r},'a') as f: f.write(json.dumps({{'target':os.path.realpath(sys.argv[0]),'argv':a,'env':dict(os.environ)}})+'\\n')\n"
            "if a==['--version']: print('gh version 2.102.0 (fixture)'); sys.exit()\n"
            "if a[:2]==['auth','status']: sys.exit()\n"
            "if a[:2]==['repo','view']: print(json.dumps({'nameWithOwner':'mryfmo/dotfiles'})); sys.exit()\n"
            "if a[:2]==['pr','view']: print(json.dumps(d['metadata'])); sys.exit()\n"
            "if a[0]=='api':\n"
            " p=next(x for x in a[1:] if x.startswith('repos/') or x in ('user','graphql'))\n"
            " if p=='user': result={'login':'declared-user'}\n"
            " elif p=='graphql': result={'data':{'repository':{'pullRequest':{'reviewThreads':{'nodes':[],'pageInfo':{'hasNextPage':False,'endCursor':None}}}}}}\n"
            " else: result=d['responses'].get(p,[])\n"
            " print(json.dumps(result)); sys.exit()\n"
            "print('unsupported fixture command',a,file=sys.stderr); sys.exit(91)\n"
        )
        self.executable(self.target, code)
        self.executable(self.bin / "gh", code)
        self.executable(
            self.bin / "mise",
            f"#!/bin/sh\n# @brief Report only a hostile gh discovery answer.\n/usr/bin/env >> {str(root / 'discovery.env')!r}\n[ \"$2\" = gh ] || exit 1\nprintf '%s\\n' {str(self.bin / 'gh')!r}\n",
        )
        self.env = {
            "PATH": f"{self.bin}:/usr/bin:/bin",
            "HOME": str(self.home),
            "LANG": "C.UTF-8",
            "UV_CACHE_DIR": str(root / "cache"),
            "GH_TOKEN": "synthetic-gh-binding-credential",
            "GH_HOST": "hostile.invalid",
            "GH_REPO": "hostile/fork",
            "GH_CONFIG_DIR": str(root / "evil-config"),
            "XDG_CONFIG_HOME": str(root / "evil-xdg"),
            "HTTPS_PROXY": "http://hostile.invalid:9",
        }
        for directory in (self.home / ".config/gh", root / "evil-config", root / "evil-xdg/gh"):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "config.yml").write_text(
                "http_unix_socket: /tmp/hostile.sock\naliases: {api: '!touch /tmp/never-gh-binding'}\n"
            )
            (directory / "hosts.yml").write_text("hostile.invalid: {user: attacker}\n")

    def launcher(self, extra=""):
        bootstrap = self.bootstrap.replace("sys.argv=a\n", "sys.argv=a\n" + extra)
        launcher = (
            "#!/bin/bash -p\n# @brief Run the measured fixture Python with the consumer's actual isolation flags.\n"
            'flags=(); while [[ $1 == -I || $1 == -P || $1 == -s ]]; do flags+=("$1"); shift; done\n'
            f'exec {shlex.quote(sys._base_executable)} "${{flags[@]}}" -c {shlex.quote(bootstrap)} "${{flags[@]}}" "$@"\n'
        )
        self.executable(self.python, launcher)

    def configuration(self, kind):
        config = self.root / "protected-config"
        config.mkdir()
        if kind == "missing":
            config.rmdir()
        elif kind == "writable":
            config.chmod(0o777)
        elif kind == "payload":
            (config / "hosts.yml").write_text("hostile.invalid: {http_unix_socket: /tmp/hostile.sock}\n")
        elif kind == "symlink":
            config.rmdir()
            config.symlink_to(self.home, target_is_directory=True)
        elif kind == "ancestor":
            self.root.chmod(0o777)
        # Model the protected filesystem root; preserve actual modes, types, symlinks and payload bytes below it.
        extra = (
            "import pathlib,os\nP=pathlib.Path; original_init=P.__init__; original_stat=P.stat\n"
            f"fixture=P({str(self.root)!r}); parents=set(fixture.parents)\n"
            f"def namespace(p,*a,**k): original_init(p,*(({str(config)!r},) if a==('/var/empty',) else a),**k)\n"
            "def measured(p,*a,**k):\n s=list(original_stat(p,*a,**k)); s[4]=0\n if p in parents: s[0]&=~0o022\n return os.stat_result(s)\n"
            "P.__init__=namespace; P.stat=measured\n"
        )
        self.launcher(extra)

    @staticmethod
    def executable(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        path.chmod(0o755)

    def declaration(self, value=None):
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        tools = {"gh": {"version": "2.102.0", "path": "~/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh"}}
        self.manifest.write_text("trusted_tools: " + json.dumps(tools if value is None else value) + "\n")

    def run(self, script=SCRIPT, *args, cwd=None, env=None):
        return subprocess.run(
            [str(self.python), "-I", str(script), *map(str, args)],
            cwd=cwd or self.root,
            env=self.env | (env or {}),
            capture_output=True,
            text=True,
            check=False,
        )

    def records(self):
        return [json.loads(s) for s in self.calls.read_text().splitlines()] if self.calls.exists() else []

    def git(self, repo, *args):
        gitdir = repo / ".git"
        if gitdir.is_file():
            gitdir = Path(gitdir.read_text().strip().removeprefix("gitdir: "))
        cache = str(self.root / "cache")
        env = {"PATH": "/usr/bin:/bin", "HOME": str(self.home), "UV_CACHE_DIR": cache}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")
        argv = ["/usr/bin/git", f"--git-dir={gitdir}", f"--work-tree={repo}"]
        for option in (
            "core.hooksPath=/dev/null",
            "core.fsmonitor=false",
            "user.name=Fixture",
            "user.email=fixture@example.invalid",
            "commit.gpgsign=false",
        ):
            argv.extend(["-c", option])
        argv.extend(map(str, args))
        return subprocess.run(argv, cwd=repo, env=env, text=True, capture_output=True, check=True).stdout.strip()

    def gate_repository(self, legacy=None):
        self.repo, self.pr = self.root / "repo", self.root / "pr"
        self.repo.mkdir()
        self.git(self.repo, "init", "-q", "-b", "main")
        for rel in (
            "scripts/pr-feedback.py",
            "scripts/require-crit-review.py",
            "scripts/validate-agent-assets.py",
            "scripts/orchestrator/orch-gate.sh",
            "scripts/orchestrator/local-review.sh",
        ):
            target = self.repo / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, target)
        if legacy:
            (self.repo / "scripts/pr-feedback.py").write_text(legacy)
        (self.repo / "README.md").write_text("base\n")
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-qm", "base")
        self.base = self.git(self.repo, "rev-parse", "HEAD")
        self.git(self.repo, "remote", "add", "origin", "https://hostile.invalid/foreign/fork.git")
        self.git(self.repo, "update-ref", "refs/remotes/origin/main", self.base)
        self.git(self.repo, "worktree", "add", "-qb", "pr", self.pr, "main")
        (self.pr / "README.md").write_text("changed\n")
        self.git(self.pr, "add", "README.md")
        self.git(self.pr, "commit", "-qm", "change")
        self.head = self.git(self.pr, "rev-parse", "HEAD")
        self.review = self.repo / ".claude/worktrees/orchestrator-review"
        self.git(self.repo, "worktree", "add", "-q", "--detach", self.review, "main")
        feedback = {"repo": REPO, "pr": 180, "items": []}
        feedback.update(head_sha=self.head, base_ref="main", base_sha=self.base)
        metadata = {"headRefOid": self.head, "baseRefName": "main", "baseRefOid": self.base}
        pull = {"head": {"sha": self.head}, "base": {"ref": "main", "sha": self.base}}
        self.responses.write_text(json.dumps({"metadata": metadata, "responses": {f"repos/{REPO}/pulls/180": pull}}))
        v = ".orchestration/validation/binding"
        self.inputs = {
            "PR_FEEDBACK_EVIDENCE": v + "-pr-feedback.json",
            "AUDIT_EVIDENCE": v + f"-audit-{self.head[:7]}.md",
            "REVIEW_EVIDENCE": v + "-review-receipt.md",
            "ACCEPTANCE_EVIDENCE": ".orchestration/acceptance/binding.md",
            "AGENT_REVIEWED": "1",
        }
        approval = [{"id": "fixture", "body": "controlled fixture approval", "scope": "review", "resolved": True}]
        files = {
            self.inputs["PR_FEEDBACK_EVIDENCE"]: json.dumps(feedback),
            self.inputs["AUDIT_EVIDENCE"]: "fixture audit\n",
            self.inputs["AUDIT_EVIDENCE"] + ".last.md": "Verdict: correct\n",
            v + "-crit.json": json.dumps(approval),
            self.inputs[
                "REVIEW_EVIDENCE"
            ]: f"review_surface: crit-data\nreviewer: codex\nreview_source: {v}-crit.json\nreview_outcome: approved\n",
            self.inputs["ACCEPTANCE_EVIDENCE"]: "---\n"
            + json.dumps({"format": 1, "task": "binding", "head": self.head, "pr": 180, "ledger": [], "searches": []})
            + "\n---\n",
        }
        for rel, text in files.items():
            for repo in (self.repo, self.pr):
                target = repo / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
        uv = f'#!/bin/bash -p\n# @brief Run the fixture interpreter.\n/usr/bin/env >> {str(self.root / "discovery.env")!r}\nif [[ "$1 $2" == "python find" ]]; then printf "%s\\n" {shlex.quote(str(self.python))}; exit; fi\nwhile [[ $1 != python ]]; do shift; done; shift\nexec {shlex.quote(str(self.python))} "$@"\n'
        self.executable(self.bin / "uv", uv)

    def assert_bound(self, case):
        discovery = self.root / "discovery.env"
        if discovery.exists():
            names = {s.split("=", 1)[0] for s in discovery.read_text().splitlines()}
            case.assertFalse(names & {"GH_TOKEN", "GH_HOST", "GH_REPO", "GH_CONFIG_DIR", "HTTPS_PROXY"})
            case.assertIn("UV_CACHE_DIR", names)
        records = self.records()
        case.assertTrue(records, "no real gh descendant observed")
        for row in records:
            case.assertEqual(str(self.target), row["target"], row)
            e, a = row["env"], row["argv"]
            case.assertEqual("/var/empty", e.get("GH_CONFIG_DIR"))
            case.assertEqual(str(self.home), e.get("HOME"))
            case.assertTrue(Path(e["UV_CACHE_DIR"]).is_absolute())
            case.assertFalse(
                set(e) & {"GH_HOST", "GH_REPO", "XDG_CONFIG_HOME", "HTTPS_PROXY", "PYTHONPATH", "GIT_DIR"}, row
            )
            if a == ["--version"]:
                case.assertNotIn("GH_TOKEN", e)
            else:
                case.assertEqual(self.env["GH_TOKEN"], e.get("GH_TOKEN"))
                if a[0] in ("api", "auth"):
                    case.assertIn("github.com", a)
                if a[0] == "pr":
                    case.assertEqual("github.com/mryfmo/dotfiles", a[a.index("--repo") + 1])


class GhBindingTest(unittest.TestCase):
    def fixture(self):
        return GhFixture(Path(self.enterContext(tempfile.TemporaryDirectory(prefix="gh-binding-"))).resolve())

    def test_collector_hostile_repository(self):
        f = self.fixture()
        result = f.run(SCRIPT, "180", "--repo", REPO)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(SHA, json.loads(result.stdout)["head_sha"])
        api = [r for r in f.records() if r["argv"][0] == "api"]
        self.assertTrue(api)
        self.assertTrue(all("github.com" in r["argv"] for r in api))
        f.assert_bound(self)

    def test_collector_binding_refusals(self):
        for kind in ("executable", "forged HOME"):
            with self.subTest(kind=kind):
                f = self.fixture()
                env = {}
                if kind == "executable":
                    f.target.chmod(0o644)
                else:
                    env["HOME"] = str(f.root / "forged")
                result = f.run(SCRIPT, "180", "--repo", REPO, env=env)
                self.assertNotEqual(0, result.returncode)
                self.assertEqual("refused: gh binding", result.stderr.strip())
                self.assertFalse([r for r in f.records() if r["argv"] != ["--version"]])

    def test_serialized_manifest_is_unambiguous(self):
        for key in ("trusted_tools", '"trusted_tools"', '"\\x74rusted_tools"', "trusted_tools "):
            with self.subTest(key=key):
                f = self.fixture()
                f.manifest.write_text(f.manifest.read_text() + key + ": {}\n")
                result = f.run(SCRIPT, "180", "--repo", REPO)
                self.assertNotEqual(0, result.returncode)
                self.assertEqual("refused: gh binding", result.stderr.strip())
                self.assertFalse(f.records())

    def test_collector_rejects_conflicting_repository(self):
        f = self.fixture()
        result = f.run(SCRIPT, "180", "--repo", "hostile/fork")
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(f.records())


# Shapes recorded from mryfmo/dotfiles #180 and #181, trimmed to the fields read.
RESPONSES: dict[str, Any] = {
    f"repos/{REPO}/pulls/180": {"head": {"sha": SHA}, "base": {"ref": "main", "sha": BASE_SHA}},
    f"repos/{REPO}/issues/180/comments": [
        [{"user": BOT, "body": "Summary by CodeRabbit", "html_url": "https://x/c1"}],
        [
            {
                "user": HUMAN,
                "body": "@coderabbitai full review",
                "html_url": "https://x/c2",
            }
        ],
    ],
    f"repos/{REPO}/pulls/180/reviews": [
        [
            {
                "user": BOT,
                "state": "COMMENTED",
                "body": "**Actionable comments posted: 1**",
                "html_url": "https://x/r1",
                "commit_id": SHA,
            }
        ]
    ],
    f"repos/{REPO}/pulls/180/comments": [
        [
            {
                "id": 11,
                "user": BOT,
                "body": "Key by render file",
                "html_url": "https://x/rc11",
                "path": "scripts/validate-agent-assets.py",
                "line": None,
                "original_line": 569,
            },
            {
                "id": 12,
                "user": BOT,
                "body": "Match unquoted literals",
                "html_url": "https://x/rc12",
                "path": "scripts/validate-agent-assets.py",
                "line": 551,
            },
            {
                "id": 13,
                "user": HUMAN,
                "body": "Reply beyond the first hundred comments of the thread",
                "html_url": "https://x/rc13",
                "path": "scripts/pr-feedback.py",
                "line": 155,
            },
        ]
    ],
    f"repos/{REPO}/commits/{SHA}/check-runs": [
        {
            "check_runs": [
                {
                    "id": 1,
                    "name": "test (ubuntu-24.04, server)",
                    "status": "completed",
                    "conclusion": "success",
                    "html_url": "https://x/j1",
                    "app": ACTIONS,
                    "output": {"title": None, "summary": None, "annotations_count": 1},
                },
                {
                    "id": 2,
                    "name": "validate",
                    "status": "completed",
                    "conclusion": "success",
                    "html_url": "https://x/j2",
                    "app": ACTIONS,
                    "output": {"annotations_count": 0},
                },
            ]
        },
        {
            "check_runs": [
                {
                    "id": 3,
                    "name": "public-bootstrap (macos-14, client)",
                    "status": "completed",
                    "conclusion": "failure",
                    "html_url": "https://x/j3",
                    "app": ACTIONS,
                    "output": {
                        "title": "Bootstrap failed",
                        "summary": "exit 1",
                        "annotations_count": 2,
                    },
                }
            ]
        },
    ],
    f"repos/{REPO}/check-runs/1/annotations": [
        [
            {
                "path": ".github",
                "start_line": 1,
                "annotation_level": "notice",
                "title": "",
                "message": "The ubuntu-latest label will migrate to Ubuntu 26",
            }
        ]
    ],
    f"repos/{REPO}/check-runs/3/annotations": [
        [
            {
                "path": ".github",
                "start_line": 1,
                "annotation_level": "failure",
                "title": "",
                "message": "crit: no bottle available!",
            },
            {
                "path": ".github",
                "start_line": 1,
                "annotation_level": "warning",
                "title": "Untrusted taps",
                "message": "The following taps are not trusted",
            },
        ]
    ],
    f"repos/{REPO}/commits/{SHA}/statuses": [
        [
            {
                "context": "CodeRabbit",
                "state": "success",
                "description": "Review skipped: manual review required for this OSS repository",
                "target_url": None,
                "creator": BOT,
            },
            {
                "context": "CodeRabbit",
                "state": "pending",
                "description": "Review in progress",
                "target_url": None,
                "creator": BOT,
            },
        ]
    ],
}
NO_MORE = {"hasNextPage": False, "endCursor": None}
THREADS = {
    None: {
        "nodes": [
            {
                "id": "T1",
                "isResolved": True,
                "isOutdated": True,
                "comments": {"nodes": [{"databaseId": 11}], "pageInfo": NO_MORE},
            }
        ],
        "pageInfo": {"hasNextPage": True, "endCursor": "c1"},
    },
    "c1": {
        "nodes": [
            {
                "id": "T2",
                "isResolved": False,
                "isOutdated": False,
                "comments": {"nodes": [{"databaseId": 12}], "pageInfo": NO_MORE},
            },
            {
                "id": "T3",
                "isResolved": True,
                "isOutdated": False,
                "comments": {
                    "nodes": [{"databaseId": 14}],
                    "pageInfo": {"hasNextPage": True, "endCursor": "t3c1"},
                },
            },
        ],
        "pageInfo": NO_MORE,
    },
}
# Second page of T2's comments: the 101st comment onward keeps the thread state.
THREAD_COMMENT_PAGES = {
    ("T3", "t3c1"): {"nodes": [{"databaseId": 13}], "pageInfo": NO_MORE},
}


def load_script():
    spec = importlib.util.spec_from_file_location("pr_feedback", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fetch(path: str, _paginate: bool) -> Any:
    return RESPONSES[path]


def graphql(_query: str, variables: dict[str, Any]) -> Any:
    if "id" in variables:
        page = THREAD_COMMENT_PAGES[(variables["id"], variables["cursor"])]
        return {"data": {"node": {"comments": page}}}
    return {"data": {"repository": {"pullRequest": {"reviewThreads": THREADS[variables["cursor"]]}}}}


class PrFeedbackTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_script()
        self.document = self.module.collect(REPO, 180, fetch, graphql)
        self.items = self.document["items"]

    def by_source(self, source: str) -> list[dict[str, Any]]:
        return [entry for entry in self.items if entry["source"] == source]

    def test_collects_every_feedback_source_for_the_head(self) -> None:
        self.assertEqual(self.document["head_sha"], SHA)
        self.assertEqual(
            [entry["source"] for entry in self.items],
            [
                "issue_comment",
                "issue_comment",
                "review",
                "review_comment",
                "review_comment",
                "review_comment",
                "annotation",
                "check_run",
                "annotation",
                "annotation",
                "status",
            ],
        )

    def test_collects_the_github_base_with_the_head(self) -> None:
        self.assertEqual(self.document["base_ref"], "main")
        self.assertEqual(self.document["base_sha"], BASE_SHA)

    def test_graphql_strings_are_raw_and_only_integers_are_typed(self) -> None:
        with mock.patch.object(self.module, "gh", return_value="{}") as gh:
            self.module.gh_graphql(
                "query {}",
                {
                    "id": "12345",
                    "label": "67890",
                    "number": 180,
                    "cursor": "@private-file",
                    "first": 100,
                    "unused": None,
                },
            )
        self.assertEqual(
            gh.call_args.args[0],
            [
                "api",
                "graphql",
                "--hostname",
                "github.com",
                "-f",
                "query=query {}",
                "-f",
                "id=12345",
                "-f",
                "label=67890",
                "-F",
                "number=180",
                "-f",
                "cursor=@private-file",
                "-F",
                "first=100",
            ],
        )

    def test_every_item_carries_the_disposition_schema(self) -> None:
        keys = {
            "source",
            "author",
            "bot",
            "level",
            "path",
            "line",
            "body",
            "url",
            "disposition",
        }
        for entry in self.items:
            self.assertTrue(keys <= set(entry), entry)
            self.assertEqual(entry["disposition"], "")
        json.dumps(self.document)

    def test_bots_are_detected_from_type_login_or_app(self) -> None:
        authors = {(entry["source"], entry["author"], entry["bot"]) for entry in self.items}
        self.assertIn(("issue_comment", "coderabbitai[bot]", True), authors)
        self.assertIn(("issue_comment", "moriya-fumio-thd", False), authors)
        self.assertIn(("annotation", "github-actions", True), authors)
        self.assertIn(("status", "coderabbitai[bot]", True), authors)

    def test_review_comments_carry_thread_resolution_across_pages(self) -> None:
        comments = {entry["url"]: entry for entry in self.by_source("review_comment")}
        self.assertEqual(
            (
                comments["https://x/rc11"]["resolved"],
                comments["https://x/rc11"]["line"],
            ),
            (True, 569),
        )
        self.assertEqual(
            (
                comments["https://x/rc12"]["resolved"],
                comments["https://x/rc12"]["line"],
            ),
            (False, 551),
        )

    def test_thread_state_covers_comments_beyond_the_first_page(self) -> None:
        comments = {entry["url"]: entry for entry in self.by_source("review_comment")}
        # Comment 13 is on T3's second GraphQL comment page; without paging it
        # would default to unresolved.
        self.assertEqual(
            (comments["https://x/rc13"]["resolved"], comments["https://x/rc13"]["outdated"]),
            (True, False),
        )

    def test_annotations_keep_every_level_even_on_passing_checks(self) -> None:
        levels = sorted(entry["level"] for entry in self.by_source("annotation"))
        self.assertEqual(levels, ["failure", "notice", "warning"])
        warning = next(entry for entry in self.by_source("annotation") if entry["level"] == "warning")
        self.assertEqual(warning["body"], "Untrusted taps The following taps are not trusted")
        self.assertEqual(warning["check"], "public-bootstrap (macos-14, client)")

    def test_only_non_passing_check_runs_become_items(self) -> None:
        self.assertEqual(
            [entry["check"] for entry in self.by_source("check_run")],
            ["public-bootstrap (macos-14, client)"],
        )
        self.assertEqual(
            self.by_source("check_run")[0]["body"],
            "public-bootstrap (macos-14, client): Bootstrap failed exit 1",
        )
        self.assertEqual(len(self.document["checks"]), 3)

    def test_commit_status_keeps_the_latest_state_per_context(self) -> None:
        statuses = self.by_source("status")
        self.assertEqual(len(statuses), 1)
        self.assertEqual(statuses[0]["level"], "success")
        self.assertIn("Review skipped: manual review required", statuses[0]["body"])

    def test_unauthenticated_gh_exits_non_zero(self) -> None:
        def unauthenticated(command, **_kwargs):
            return subprocess.CompletedProcess(command, 1, "", "not logged in")

        # Patch the shared subprocess module only for this call; it is global.
        with (
            mock.patch.object(self.module, "gh_binding", return_value="/usr/bin/false"),
            mock.patch.object(self.module, "gh_env", return_value={}),
            mock.patch.object(self.module.subprocess, "run", unauthenticated),
            redirect_stderr(io.StringIO()) as stderr,
            self.assertRaises(SystemExit) as raised,
        ):
            self.module.main(["180", "--repo", REPO])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("gh auth login", stderr.getvalue())

    def test_gh_never_receives_forced_colour(self) -> None:
        with mock.patch.dict(self.module.os.environ, {"CLICOLOR_FORCE": "1"}):
            env = self.module.gh_env()
        self.assertNotIn("CLICOLOR_FORCE", env)
        self.assertEqual(env["NO_COLOR"], "1")

    def test_main_writes_the_document_to_json(self) -> None:
        self.module.require_auth = lambda: None
        self.module.collect = lambda repo, number: self.document
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / "feedback.json"
            with redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(self.module.main(["180", "--repo", REPO, "--json", str(out)]), 0)
            self.assertEqual(json.loads(out.read_text())["items"], self.items)
        self.assertIn("11 items", stderr.getvalue())


class PrIntegrationRuleParityTest(unittest.TestCase):
    """Keep the PR integration rule, its mirrors, and the skills in step; the gate command lives in one place."""

    TOKENS = (
        "scripts/pr-feedback.py",
        "fixed:<commit>",
        "not-applicable:",
    )
    GATE = "BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review"
    POINTER = "Orchestrator Playbook step 10"

    def test_rule_symlink_points_at_the_rule(self) -> None:
        self.assertEqual(
            (ROOT / "home/dot_claude/rules/symlink_pr-integration.md.tmpl").read_text(),
            "{{ .chezmoi.sourceDir }}/dot_config/claude/rules/pr-integration.md\n",
        )

    def pointer_sources(self) -> dict[str, str]:
        codex = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
        return {
            "claude rule": (ROOT / "home/dot_config/claude/rules/pr-integration.md").read_text(),
            "codex mirror": codex.split("## PR 統合", 1)[1].split("\n## ", 1)[0],
            "gh-first-workflow": (ROOT / "home/dot_agents/skills/gh-first-workflow/SKILL.md").read_text(),
        }

    def test_rule_mirrors_and_skills_carry_the_same_requirements(self) -> None:
        skill = (ROOT / "home/dot_agents/skills/agmsg-orchestration/SKILL.md").read_text()
        for name, text in {**self.pointer_sources(), "agmsg-orchestration": skill}.items():
            for token in self.TOKENS:
                with self.subTest(source=name, token=token):
                    self.assertIn(token, text)

    def test_gate_command_appears_once_in_skill_step_10(self) -> None:
        skill = (ROOT / "home/dot_agents/skills/agmsg-orchestration/SKILL.md").read_text()
        step_10 = skill.split("\n10. ", 1)[1].split("\n11. ", 1)[0]
        self.assertEqual(skill.count(self.GATE), 1)
        self.assertIn(self.GATE, step_10)
        readme = (ROOT / "README.md").read_text()
        for name, text in {**self.pointer_sources(), "README": readme}.items():
            with self.subTest(source=name):
                self.assertIn(self.POINTER, text)
                self.assertNotIn("PR_FEEDBACK_EVIDENCE=<json> make require-crit-review", text)
                self.assertNotIn("PR_FEEDBACK_EVIDENCE=.orchestration/", text)


if __name__ == "__main__":
    unittest.main()
