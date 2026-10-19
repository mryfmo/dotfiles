"""Exercise C11 to C15 and the trusted execution contract in temporary repositories."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_CACHE = None
TRACE = "import sys,subprocess,json,runpy; original=subprocess.run; log=sys.argv.pop(1)\ndef run(argv,**kw):\n with open(log,'a') as f: f.write(json.dumps({'argv':argv,'env':kw.get('env',{})})+'\\n')\n return original(argv,**kw)\nsubprocess.run=run\nsys.argv.pop(0);runpy.run_path(sys.argv[0],run_name='__main__')"


def uv_command(offline=True):
    uv = (
        Path(os.environ["TRUSTED_BIN_DIR"]) / "uv" if "TRUSTED_BIN_DIR" in os.environ else Path(shutil.which("uv"))
    ).resolve()
    return [
        str(uv),
        "run",
        "--no-config",
        "--no-project",
        *(["--offline"] if offline else []),
        "--python",
        str(Path(sys.executable).resolve()),
        "--with",
        "pyyaml",
        "python",
        "-I",
    ]


def fixture_cache():
    global _CACHE
    if _CACHE is None:
        _CACHE = tempfile.TemporaryDirectory(prefix="a03-pyyaml-")
        command = [*uv_command(False), "-c", "import yaml"]
        result = subprocess.run(
            command,
            env={**os.environ, "PATH": os.defpath, "UV_CACHE_DIR": _CACHE.name},
            capture_output=True,
            text=True,
            check=False,
        )
        print(
            f"fixture-seed UV_CACHE_DIR={_CACHE.name} {command!r} exit={result.returncode}\n{result.stdout}{result.stderr}",
            flush=True,
        )
        if result.returncode:
            _CACHE.cleanup()
            _CACHE = None
            raise unittest.SkipTest("PyYAML fixture cache seed unavailable: network or package provisioning failed")
    return _CACHE.name


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/orchestrator/task-consistency-check.py"
MAIN_SHA = "a" * 40


def canonical_files(repo):
    paths = subprocess.check_output([shutil.which("git"), "-C", str(repo), "ls-files", "-z"], text=True).split("\0")
    return {
        p: os.readlink(repo / p) if (repo / p).is_symlink() else (repo / p).read_text()
        for p in paths
        if p and (repo / p).is_file()
    }


def parent_env(directory, env=None, files=None):
    directory = Path(directory)
    private = directory / "private-bin"
    private.mkdir(exist_ok=True, mode=0o700)
    for name, source in (
        ("git", shutil.which("git")),
        ("uv", uv_command()[0]),
        ("bash", "/bin/bash"),
        ("sh", "/bin/sh"),
        ("pwd", "/bin/pwd"),
    ):
        if not (private / name).exists():
            (private / name).symlink_to(Path(source).resolve())
    data, calls = directory / "canonical.json", directory / "gh-calls.jsonl"
    data.write_text(json.dumps(files or {}))
    gh = directory / "trusted-gh"
    gh.write_text(
        f"#!{Path(sys.executable).resolve()} -I\nimport sys,json,base64,pathlib\n"
        f"a=sys.argv[1:];p=pathlib.Path({str(data)!r});d=json.loads(p.read_text());"
        f"open({str(calls)!r},'a').write(json.dumps(a)+'\\n')\n"
        "assert a[0]=='api';endpoint=a[1];prefix='repos/mryfmo/dotfiles/';assert endpoint.startswith(prefix)\n"
        f"if endpoint==prefix+'git/ref/heads/main':\n assert a[2:]==['--jq','.object.sha'];print({MAIN_SHA!r})\n"
        "else:\n"
        f" assert endpoint.startswith(prefix+'contents/') and endpoint.endswith('?ref={MAIN_SHA}')\n"
        " name=endpoint[len(prefix+'contents/'):].split('?ref=')[0]\n"
        " if name in d:print(json.dumps(dict(type='file',encoding='base64',content=base64.b64encode(d[name].encode()).decode())))\n"
        " else:\n"
        "  children={}\n"
        "  for key in d:\n"
        "   if key.startswith(name.rstrip('/')+'/'):\n"
        "    tail=key[len(name.rstrip('/'))+1:];part=tail.split('/')[0];children[part]=dict(path=name.rstrip('/')+'/'+part,type='dir' if '/' in tail else 'file')\n"
        "  if children:print(json.dumps(list(children.values())))\n"
        "  else:print('gh: Not Found (HTTP 404)',file=sys.stderr);sys.exit(1)\n"
    )
    gh.chmod(0o700)
    if not (private / "gh").exists():
        (private / "gh").symlink_to(gh)
    return {
        **(os.environ if env is None else env),
        "UV_CACHE_DIR": fixture_cache(),
        "TRUSTED_PYTHON": str(Path(sys.executable).resolve()),
        "TRUSTED_BIN_DIR": str(private),
        "PATH": str(private),
    }


GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
UNTRUSTED = "dotfiles-T9-base-a01.md: warning: C14: not run (no trusted sha)\n"  # the checker's stderr line
NONPATH = "".join(
    f'  - control: {name}\n    disposition: "residual: the fixture\'s control for {name}"\n'
    for name in (
        "metadata separators",
        "in-process effects",
        "workflow and interpreter or environment inputs",
        "new or renamed scripts",
        "orchestrator effect merge",
        "orchestrator effect update-branch",
        "orchestrator effect forced worker removal",
    )
)
BASE = f"""---
format: 2
task_id: dotfiles-T9-base-a01
kind: code
allowed_files:
  - scripts/tool.py
  - .orchestration/dotfiles-T9-base-a01/**
design_review:
  receipt: r1
  design: .orchestration/tasks/dotfiles-T9-design-a01.md
invariants:
  INV-1: "the tool prints one line per finding"
threat_table:
  - control: "scripts/tool.py (the tool)"
    disposition: "closed: tests/unit/test_tool.py::test_tool_prints_findings"
  - control: "the evidence under .orchestration/dotfiles-T9-base-a01/ (report.md)"
    disposition: "residual: prose and pasted command output only"
  - control: task metadata
    disposition: "out-of-scope: dotfiles-T9-design-a01"
  - control: "scripts/a.sh (the one file of the glob fixture a row names)"
    disposition: "residual: a fixture row for the C12 case"
{NONPATH}premises:
  - claim: the fixture's premise prints base
    command: grep -c print scripts/tool.py
    output: |-
      1
---

# AGMSG-TASK dotfiles-T9-base-a01 — the fixture
"""
DESIGN = '---\nformat: 2\ninvariants:\n  INV-1: "the tool prints one line per finding"\n---\n\n# design\n'
CASES = {
    "C11": (
        '"closed: tests/unit/test_tool.py::test_tool_prints_findings"',
        '"closed: tests/unit/test_tool.py::two words"',
    ),
    "C12": ("  - scripts/tool.py\n", "  - scripts/tool.py\n  - scripts/*.sh\n"),
    "C13": ('"residual: prose and pasted command output only"', '"accepted: prose and pasted command output only"'),
    "C14": ("      1\n---", "      edited\n---"),
    "C15": ('INV-1: "the tool prints one line per finding"', 'INV-1: "the tool prints one line per run"'),
}


class RepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_cache()

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo = self.temp / "repo"
        self.env = parent_env(self.temp, {**os.environ, **GIT_ENV, "GIT_CONFIG_GLOBAL": "/dev/null"})

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

    def commit(self, files, message, init=False):
        for rel, text in files.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        if init:
            self.git("init", "-q", "-b", "main")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        if init:
            self.git("init", "-q", "--bare", str(self.temp / "origin.git"))
            self.git("remote", "add", "origin", str(self.temp / "origin.git"))
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")
        (self.temp / "canonical.json").write_text(json.dumps(canonical_files(self.repo)))


class TaskConsistencyC11C15Test(RepositoryTest):
    def test_all_three_scripts_use_parent_supplied_launch_bindings(self):
        from tests.unit.test_task_from_plan import TaskFromPlanTest

        fixture = TaskFromPlanTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        fixture.env = parent_env(fixture.temp, fixture.env, canonical_files(fixture.repo))
        evil = fixture.temp / "evil-ran"
        (fixture.repo / "bin").mkdir()
        for name in ("git", "uv", "gh"):
            shim = fixture.repo / "bin" / name
            shim.write_text(f"#!/bin/sh\ntouch {evil}\nexit 87\n")
            shim.chmod(0o700)
        (fixture.repo / "uv.toml").write_text(f'cache-dir = "{fixture.temp / "evil-cache"}"\n')
        (fixture.repo / ".venv/bin").mkdir(parents=True)
        (fixture.repo / ".venv/bin/python").symlink_to(fixture.repo / "bin/uv")
        site = fixture.temp / f"user/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
        site.mkdir(parents=True)
        payload = f"import pathlib;pathlib.Path({str(evil)!r}).touch()\n"
        (site / "bad.pth").write_text(payload)
        (site / "usercustomize.py").write_text(payload)
        fixture.env.update(
            PYTHONUSERBASE=str(fixture.temp / "user"), PYTHONPATH=str(site), GIT_WORK_TREE=str(fixture.temp)
        )
        marker = fixture.temp / "bound-uv-ran"
        wrapper = fixture.temp / "bound-uv"
        wrapper.write_text(f'#!/bin/sh\nprintf used >> {marker}\nexec {uv_command()[0]} "$@"\n')
        wrapper.chmod(0o700)
        link = fixture.temp / "private-bin/uv"
        link.unlink()
        link.symlink_to(wrapper)
        for name, code, out in fixture.run_three(trace=True):
            self.assertEqual(code, 0, (name, out))
        self.assertFalse(evil.exists())
        self.assertFalse((fixture.temp / "evil-cache").exists())
        self.assertTrue(marker.exists(), "the supplied UV binding was not consumed")
        launches = [
            c
            for c in map(json.loads, (fixture.temp / "trace.jsonl").read_text().splitlines())
            if "--python" in c["argv"]
        ]
        self.assertTrue(launches)
        for call in launches:
            argv = call["argv"]
            self.assertEqual(call["env"], {})
            self.assertIn(str(wrapper), argv)
            self.assertEqual(argv[argv.index("--python") + 1], fixture.env["TRUSTED_PYTHON"])
            for value in (
                "--no-config",
                "--no-project",
                "--offline",
                "-I",
                "UV_CACHE_DIR=" + fixture.env["UV_CACHE_DIR"],
                "TRUSTED_PYTHON=" + fixture.env["TRUSTED_PYTHON"],
            ):
                self.assertIn(value, argv)

        bad = {
            **fixture.env,
            "TRUSTED_BIN_DIR": str(fixture.temp / "absent-bindings"),
            "PATH": str(fixture.repo / "bin"),
        }
        for script, args in (
            ("task-from-plan.py", ["P1-1"]),
            ("plan-check.py", ["--root", str(fixture.repo)]),
            (
                "task-consistency-check.py",
                ["--root", str(fixture.repo), str(fixture.repo / ".orchestration/tasks/dotfiles-T9-base-a01.md")],
            ),
        ):
            result = subprocess.run(
                [*uv_command(), str(fixture.production / script), *args],
                cwd=fixture.repo,
                env=bad,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refused: trusted executable binding missing: git", result.stdout + result.stderr)
        self.assertFalse(evil.exists())

    def interpreter_refusal(self, values):
        from tests.unit.test_task_from_plan import TaskFromPlanTest

        fixture = TaskFromPlanTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        valid = parent_env(fixture.temp, fixture.env)
        for value in values:
            env = {**valid, "UV_CACHE_DIR": str(fixture.temp / "untouched-cache")}
            env.pop("TRUSTED_PYTHON", None)
            if value is not None:
                env["TRUSTED_PYTHON"] = value
            for script, args in (
                ("task-from-plan.py", ["P1-1"]),
                ("plan-check.py", ["--root", str(fixture.repo)]),
                ("task-consistency-check.py", ["--root", str(self.repo), str(self.task(BASE))]),
            ):
                result = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-c",
                        TRACE,
                        str(fixture.temp / "unexpected.jsonl"),
                        str(CHECKER.with_name(script)),
                        *args,
                    ],
                    cwd=fixture.repo,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertFalse((fixture.temp / "untouched-cache").exists())
                self.assertFalse((fixture.temp / "unexpected.jsonl").exists())
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "refused: TRUSTED_PYTHON must be set to an absolute regular file", result.stdout + result.stderr
                )

    def test_all_three_scripts_refuse_an_unset_trusted_python(self):
        self.interpreter_refusal([None])

    def test_all_three_scripts_refuse_an_invalid_trusted_python(self):
        self.interpreter_refusal(["relative/python", str(self.temp / "missing-python"), str(self.temp)])

    def test_c14_interprets_the_probe_vocabulary_without_a_shell(self):
        fake = self.repo / "bin"
        fake.mkdir()
        marker = self.repo / "marker"
        for name in ("bash", "git"):
            (fake / name).write_text(f"#!/bin/sh\ntouch {marker}\nexit 99\n")
            (fake / name).chmod(0o755)
        self.env.update(PATH=str(fake), GIT_WORK_TREE=str(fake), PYTHONPATH=str(fake))
        (self.repo / "literal").write_text("[\n[a\nplain\n")
        (self.repo / "lf-lines").write_bytes(b"needle\vneedle\n")
        for command, output in (
            (
                "git rev-parse HEAD",
                subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo, text=True).strip(),
            ),
            ("test -e scripts/tool.py", ""),
            ("test -f scripts/tool.py", ""),
            ("grep -c '[' literal", "2"),
            ("grep -c needle lf-lines", "1"),
        ):
            text = BASE.replace("command: grep -c print scripts/tool.py", f"command: {command}").replace(
                "      1\n---", f"      {output}\n---"
            )
            self.assertEqual(self.check(self.task(text), trace=True)[0], 0, command)
        for call in map(json.loads, (self.repo / "trace.jsonl").read_text().splitlines()):
            self.assertEqual(call["env"], {})
            self.assertEqual(call["argv"][0], os.path.realpath("/usr/bin/env"))
            if "api" in call["argv"]:
                self.assertTrue(any(str(a).startswith("repos/mryfmo/dotfiles/") for a in call["argv"]))
                continue
            for flag in (
                "GIT_CONFIG_NOSYSTEM=1",
                "GIT_CONFIG_GLOBAL=/dev/null",
                "GIT_NO_LAZY_FETCH=1",
                "core.hooksPath=/dev/null",
                "core.fsmonitor=false",
                "submodule.recurse=false",
                "protocol.allow=never",
                "protocol.https.allow=always",
                f"--git-dir={self.repo / '.git'}",
                f"--work-tree={self.repo}",
            ):
                self.assertIn(flag, call["argv"])
            if "show" in call["argv"] or "diff" in call["argv"]:
                for flag in (
                    "--no-ext-diff",
                    "--no-textconv",
                    "core.attributesFile=/dev/null",
                    "core.sshCommand=false",
                ):
                    self.assertIn(flag, call["argv"])
            self.assertNotIn(str(fake), call["argv"])
        self.assertFalse(marker.exists())
        bound = self.repo / "bound.py"
        bound.write_text("original")
        worker = self.repo / ".claude/worktrees/seat/helper.py"
        worker.parent.mkdir(parents=True)
        worker.write_text("fixture")
        shim = self.repo / "shims/python"
        shim.parent.mkdir()
        shim.symlink_to(Path(sys.executable).resolve())
        for path, action, refusal in (
            (worker, "m.trusted(p)", "worker-root"),
            (shim, "m.trusted(p)", "shim trusted path"),
            (
                bound,
                "b=m.snapshot(p);assert b[0].stat().st_mode & 0o777 == 0o600;b[0].write_text('replaced');m.consume(b)",
                "consumed bytes changed",
            ),
        ):
            code = f"import importlib.util,sys,pathlib;s=importlib.util.spec_from_file_location('m',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);p=pathlib.Path(sys.argv[2]);m.TRUST_ROOT=pathlib.Path({str(self.repo)!r});{action}"
            result = subprocess.run(
                [*uv_command(), "-c", code, str(CHECKER), str(path)],
                env=self.env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(refusal, result.stdout + result.stderr)
        (self.repo / "probe.py").write_text(f"open({str(marker)!r}, 'w').close()")
        (self.repo / "x.sh").write_text(f"touch {marker}")
        for command in (
            "python -I probe.py",
            "source ./x.sh",
            "git status",
            "test -f ../outside",
            "grep -c x ../outside",
            "git rev-parse --help",
            "test -e literal; true",
        ):
            code, out = self.check(
                self.task(BASE.replace("command: grep -c print scripts/tool.py", f"command: {command}"))
            )
            self.assertFalse(marker.exists(), out)
            self.assertEqual(code, 1, out)
            self.assertIn(command, out)

    def test_c11_accepts_the_pytest_node_id_with_a_class(self):
        old = ROOT / ".orchestration/dotfiles-T133-task-generator-plan-check-a03/fixture-a02-task.md"
        target = self.repo / ".orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md"
        target.write_bytes(old.read_bytes())
        _, out = self.check(target, sha=None)
        self.assertNotIn("C11 closed:", out)
        self.assertIn("C14: not run (no trusted sha)", out)
        for selector, accepted in (
            ("test_tool", True),
            ("Suite::test_tool", True),
            ("Suite::two words", False),
            ("Suite::test::extra", False),
        ):
            _, out = self.check(self.task(BASE.replace("test_tool_prints_findings", selector)), sha=None)
            self.assertEqual("C11 closed:" not in out, accepted, out)

    def test_uv_launches_ignore_a_hostile_venv_and_uv_config(self):
        from tests.unit.test_task_from_plan import FILES, PROGRAMS, TaskFromPlanTest

        fixture = TaskFromPlanTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        repo, marker = fixture.repo, fixture.repo / "venv-ran"
        (repo / ".venv/bin").mkdir(parents=True)
        (repo / ".venv/bin/python").write_text(f"#!/bin/sh\ntouch {marker}\nexit 87\n")
        (repo / ".venv/bin/python").chmod(0o755)
        (repo / ".venv/pyvenv.cfg").write_text(f"home = {Path(sys.executable).resolve().parent}\n")
        (repo / "uv.toml").write_text(f'cache-dir = "{repo / "config-selected"}"\n')
        (repo / "bin").mkdir()
        (repo / "bin/uv").symlink_to(uv_command()[0])
        fixture.commit(
            {
                PROGRAMS: FILES[PROGRAMS].replace(
                    "printf known-output",
                    f"uv run --with pyyaml --python {Path(sys.executable).resolve()} python -c 'print(1)'",
                )
            },
            "hostile uv discovery",
        )
        code, out, _, _ = fixture.generate(trace=True)
        self.assertFalse(marker.exists(), out)
        self.assertFalse((repo / "config-selected").exists(), out)
        self.assertEqual(code, 0, out)
        launches = [
            call["argv"]
            for call in map(json.loads, (fixture.temp / "trace.jsonl").read_text().splitlines())
            if "run" in call["argv"] and "--with" in call["argv"]
        ]
        self.assertTrue(launches, "no trusted UV launch was observed")
        for argv in launches:
            for flag in ("--no-config", "--no-project", "--offline", "--python"):
                self.assertIn(flag, argv)
            self.assertTrue(Path(argv[argv.index("--python") + 1]).is_absolute())
            self.assertIn("UV_CACHE_DIR=" + fixture.env["UV_CACHE_DIR"], argv)

    def cache_refusal(self, value):
        from tests.unit.test_task_from_plan import TaskFromPlanTest

        fixture = TaskFromPlanTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        for script, args in (
            ("task-from-plan.py", ["P1-1"]),
            ("plan-check.py", ["--root", str(fixture.repo)]),
            ("task-consistency-check.py", ["--root", str(self.repo), str(self.task(BASE))]),
        ):
            env = dict(os.environ)
            env.pop("UV_CACHE_DIR", None)
            if value is not None:
                env["UV_CACHE_DIR"] = value
            run = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-c",
                    TRACE,
                    str(fixture.repo / "unexpected-child.jsonl"),
                    str(CHECKER.with_name(script)),
                    *args,
                ],
                cwd=fixture.repo,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("refused: UV_CACHE_DIR must be set to an absolute path", run.stdout + run.stderr)
            self.assertFalse((fixture.repo / "relative-uv-cache").exists())
            self.assertFalse((fixture.repo / "unexpected-child.jsonl").exists())

    def test_all_three_scripts_refuse_an_unset_uv_cache_dir(self):
        self.cache_refusal(None)

    def test_all_three_scripts_refuse_a_relative_uv_cache_dir(self):
        self.cache_refusal("relative-uv-cache")

    def setUp(self):
        super().setUp()
        self.commit(
            {
                ".orchestration/tasks/dotfiles-T9-design-a01.md": DESIGN,
                "scripts/tool.py": "print('tool')\n",
                "scripts/a.sh": "echo a\n",
                "scripts/b.sh": "echo b\n",
            },
            "init",
            init=True,
        )

    def check(self, *tasks, root=None, sha=True, trace=False):
        """Run the checker; `sha` True passes the first file's sha256 as --premises-sha, as for the dispatched text."""
        if sha is True:
            sha = hashlib.sha256(Path(tasks[0]).read_bytes()).hexdigest()
        run = [*uv_command(), *(["-c", TRACE, str(self.repo / "trace.jsonl")] if trace else []), str(CHECKER)]
        trusted = ["--premises-sha", sha] if sha else []
        result = subprocess.run(
            [*run, "--root", str(root or self.repo), *trusted, *map(str, tasks)],
            capture_output=True,
            text=True,
            check=False,
            env=self.env,
            cwd=self.repo,
        )
        output = result.stdout + result.stderr
        for line in output.splitlines():
            if line.startswith(("canonical-main ", "api-input-sha256 ")):
                length = 40 if line.startswith("canonical-main ") else 64
                self.assertRegex(line.split()[-1], rf"^[0-9a-f]{{{length}}}$")
        return result.returncode, "".join(
            line
            for line in output.splitlines(keepends=True)
            if not line.startswith(("canonical-main ", "api-input-sha256 "))
        )

    def task(self, text):
        path = self.repo / ".orchestration/tasks/dotfiles-T9-base-a01.md"
        path.write_text(text)
        return path

    def test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged(self):
        code, out = self.check(self.task(BASE))
        self.assertEqual((code, out), (0, "dotfiles-T9-base-a01.md: OK\n"))
        for check, (old, new) in CASES.items():
            with self.subTest(check=check):
                self.assertEqual(BASE.count(old), 1)
                code, out = self.check(self.task(BASE.replace(old, new)))
                findings = out.splitlines()[1:]
                self.assertEqual(code, 1, out)
                self.assertEqual(len(findings), 1, out)
                self.assertTrue(findings[0].strip().startswith(check + " "), out)
        padded = BASE.replace("      1\n---", "      1   \n---")
        self.assertEqual(self.check(self.task(padded)), (0, "dotfiles-T9-base-a01.md: OK\n"))
        for cmd in ("no-such-tool-a01 --list", "no-such-tool-a01 --help | /usr/bin/grep -c x"):
            code, out = self.check(self.task(BASE.replace("command: grep -c print scripts/tool.py", f"command: {cmd}")))
            self.assertEqual(code, 1, out)
            self.assertIn("C14 unsupported", out)
        current = sorted((ROOT / ".orchestration/tasks").glob("dotfiles-T133-*.md"))
        with self.subTest(green="the current dotfiles-T133 task files"):
            if not current:
                self.skipTest("no dotfiles-T133 task file in this tree yet (they land with a boundary records PR)")
            code, out = self.check(*current, root=ROOT, sha=None)
            others = [l for l in out.splitlines() if l.startswith("  ") and not l.strip().startswith("C14")]
            self.assertEqual(others, [], out)

    def test_c14_executes_premise_commands_only_for_the_dispatched_sha(self):
        marker = self.repo / "marker"
        path = self.task(
            BASE.replace("command: grep -c print scripts/tool.py", f"command: touch {marker}; printf base")
        )
        for sha in (None, "0" * 64):
            with self.subTest(sha=sha):
                code, out = self.check(path, sha=sha)
                self.assertEqual((code, marker.exists()), (0, False), out)
                self.assertEqual(out, f"dotfiles-T9-base-a01.md: OK\n{UNTRUSTED}")
        self.assertEqual(self.check(path)[0], 1)
        self.assertFalse(marker.exists())
        edited = self.task(
            BASE.replace("command: grep -c print scripts/tool.py", f"command: touch {marker}; printf edited")
        )
        code, out = self.check(edited)
        self.assertEqual((code, marker.exists()), (1, False), out)
        self.assertIn("C14 unsupported", out)

    def publish(self, files):
        self.commit(files, "publish")

    def test_c14_without_a_trusted_sha_reports_an_explicit_warning(self):
        marker = self.repo / "marker"
        path = self.task(
            BASE.replace("command: grep -c print scripts/tool.py", f"command: touch {marker}; printf base")
        )
        code, out = self.check(path, sha=None)
        self.assertEqual((code, marker.exists(), out), (0, False, f"dotfiles-T9-base-a01.md: OK\n{UNTRUSTED}"))

    def test_c15_requires_the_design_assigned_invariant_id_set(self):
        one, two = '"the tool prints one line per finding"', '"the tool exits 1 on a finding"'
        design = (
            f"implementing_tasks:\n  dotfiles-T9-base-a01: [INV-1, INV-2]\ninvariants:\n  INV-1: {one}\n  INV-2: {two}"
        )
        self.publish({".orchestration/tasks/dotfiles-T9-design-a01.md": f"---\nformat: 2\n{design}\n---\n\n# design\n"})
        block, d = f"invariants:\n  INV-1: {one}\n", ".orchestration/tasks/dotfiles-T9-design-a01.md"
        missing = f"C15 invariant {{}} that {d} assigns to dotfiles-T9-base-a01 is missing"
        cases = {
            "only INV-1": (block, [missing.format("INV-2")]),
            "no map": ("", [missing.format("INV-1"), missing.format("INV-2")]),
            "an extra id": (
                block + f"  INV-2: {two}\n  INV-3: {two}\n",
                [f"C15 invariant INV-3 is not one {d} assigns to dotfiles-T9-base-a01"],
            ),
            "a changed sentence": (
                block + '  INV-2: "the tool exits 2"\n',
                [f"C15 invariant INV-2 is not byte-equal to {d} on origin/main"],
            ),
            "the whole assignment": (block + f"  INV-2: {two}\n", []),
        }
        typo = ".orchestration/tasks/dotfiles-T9-typo-a01.md"  # the pre-push review of eb20d063: no skip by a typo
        cases["a mistyped design"] = ("", [f"C15 design {typo} is not on origin/main"])
        for name, (invariants, want) in cases.items():
            with self.subTest(case=name):
                task = BASE.replace(block, invariants).replace(d, typo if name == "a mistyped design" else d)
                _, out = self.check(self.task(task))
                self.assertEqual([l.strip() for l in out.splitlines() if l.strip().startswith("C15")], want, out)

    def test_c12_classifies_concrete_glob_matches_before_the_glob_spelling(self):
        own = ".orchestration/dotfiles-T9-base-a01/run.sh"
        self.publish({"install/setup.sh": "echo setup\n", "tests/fixtures/x/run.sh": "echo x\n", own: "echo own\n"})
        rows = '  - control: "install/** (the installers)"\n    disposition: "residual: the C12 case\'s glob entry"\n'
        rows += (
            '  - control: "tests/fixtures/x/** (fixtures)"\n    disposition: "residual: the C12 case\'s exempt glob"\n'
        )
        task = BASE.replace("  - scripts/tool.py\n", "  - scripts/tool.py\n  - install/**\n  - tests/fixtures/x/**\n")
        task = task.replace("threat_table:\n", "threat_table:\n" + rows)
        code, out = self.check(self.task(task))
        self.assertEqual(
            (code, out.splitlines()[1:]),
            (1, ["  C12 the glob install/** matches install/setup.sh, which no threat_table row names"]),
        )
        named = '  - control: "install/setup.sh (the setup script)"\n    disposition: "residual: the C12 case\'s concrete row"\n'
        self.assertEqual(
            self.check(self.task(task.replace("threat_table:\n", "threat_table:\n" + named))),
            (0, "dotfiles-T9-base-a01.md: OK\n"),
        )

    def test_c10_never_passes_a_literal_as_a_git_grep_option(self):
        marker = self.repo.parent / "pager-ran"
        (self.repo / "scripts/tool.py").write_text("print('origin/main')\n")
        literal = f"--open-files-in-pager=touch {marker}"
        rule = f'\nThe rule: "scripts/tool.py reads `{literal}` before every run of the gate".\n'
        _, out = self.check(self.task(BASE.replace("kind: code", "kind: docs") + rule))
        self.assertFalse(marker.exists(), out)
        self.assertIn(f"C10 rule sentence names scripts/tool.py beside the literal `{literal}`", out)

    def test_c6_confines_design_paths_to_the_checkout(self):
        outside = self.repo.parent / "outside/design.md"
        outside.parent.mkdir()
        outside.write_text("---\ndesign_review:\n  receipt: r9-outside\n---\n")
        task = BASE.replace("design: .orchestration/tasks/dotfiles-T9-design-a01.md", "design: ../outside/design.md")
        _, out = self.check(self.task(task))
        self.assertIn("C6 design path ../outside/design.md is outside the checkout", out)
        self.assertNotIn("r9-outside", out)


if __name__ == "__main__":
    unittest.main()
