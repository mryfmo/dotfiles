"""Exercise the real checker in temporary repositories; API fixtures provide no live authority."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/orchestrator/task-consistency-check.py"
PYTHON = str(Path(sys.executable).resolve())
UV = str(Path(shutil.which("uv")).resolve())
GIT = shutil.which("git")
MAIN = "a" * 40
DESIGN = ".orchestration/plans/design.md"
NAMES = "task metadata|metadata separators|in-process effects|workflow and interpreter or environment inputs|new or renamed scripts|orchestrator effect merge|orchestrator effect update-branch|orchestrator effect forced worker removal".split(
    "|"
)
RESIDUAL = "residual: fixture data and checked boundaries"
REFERENCE = "Design 5.14 applies by reference."
_CACHE = None


def uv(offline=True):
    args = [UV, "run", "--no-config", "--no-project", "--offline"][: 4 + offline]
    return [*args, "--python", PYTHON, "--with", "pyyaml", "python", "-I"]


def fixture_cache():
    global _CACHE
    if _CACHE is None:
        _CACHE = tempfile.TemporaryDirectory(prefix="checker-deps-")
        seed = os.environ.get("UV_CACHE_DIR", "")
        if os.path.isabs(seed) and Path(seed).is_dir():
            shutil.copytree(seed, _CACHE.name, dirs_exist_ok=True, symlinks=True)
        command = [*uv(bool(seed)), "-c", "import yaml"]
        env = {**os.environ, "UV_CACHE_DIR": _CACHE.name, "PATH": os.defpath}
        result = subprocess.run(command, env=env, capture_output=True, text=True, check=False)
        print("fixture-seed", PYTHON, UV, result.returncode, result.stdout, result.stderr, flush=True)
        if result.returncode:
            raise RuntimeError("PyYAML fixture provisioning failed; this is not a behavioral test result")
    return _CACHE.name


class TaskConsistencyC11C15Test(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="checker-case-")
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo, self.trust = self.temp / "repo", self.temp / "trusted"
        self.repo.mkdir()
        self.script = self.trust / "scripts/orchestrator/task-consistency-check.py"
        self.script.parent.mkdir(parents=True)
        self.script.write_bytes(CHECKER.read_bytes())
        self.bin = self.temp / "bin"
        self.bin.mkdir(mode=0o700)
        for name, source in (("git", GIT), ("uv", UV)):
            (self.bin / name).symlink_to(Path(source).resolve())
        self.data, self.calls = self.temp / "api.json", self.temp / "api-calls.jsonl"
        self.canonical = {DESIGN: "---\ndesign_review:\n  receipt: r1\ninvariants:\n  INV-1: exact sentence\n---\n"}
        gh = self.temp / "gh"
        gh.write_text(
            f"#!{PYTHON} -I\nimport sys,json,base64,os,hashlib\nfrom urllib.parse import unquote\n"
            f"data=json.load(open({str(self.data)!r}));a=sys.argv[1:]\n"
            f"with open({str(self.calls)!r},'a') as f: f.write(json.dumps(dict(argv=a,cache=os.environ.get('UV_CACHE_DIR'),tokens={{k:hashlib.sha256(os.environ[k].encode()).hexdigest() for k in ('GH_TOKEN','GITHUB_TOKEN') if k in os.environ}},host=os.environ.get('GH_HOST')))+'\\n')\n"
            "assert a[0]=='api';p=a[1];prefix='repos/mryfmo/dotfiles/'\n"
            f"if p==prefix+'git/ref/heads/main': print({MAIN!r})\n"
            "elif p.startswith(prefix+'contents/'):\n"
            " name=unquote(p[len(prefix+'contents/'):].split('?ref=')[0])\n"
            " if name in data: print(json.dumps(dict(encoding='base64',content=base64.b64encode(data[name].encode()).decode())))\n"
            " else:\n"
            "  children={key[len(name)+1:].split('/')[0] for key in data if key.startswith(name+'/')}\n"
            "  if children: print(json.dumps([dict(path=name+'/'+v) for v in sorted(children)]))\n"
            "  else: print('gh: Not Found (HTTP 404)',file=sys.stderr);sys.exit(1)\n"
            "else: sys.exit(71)\n"
        )
        gh.chmod(0o700)
        (self.bin / "gh").symlink_to(gh)
        self.env = {
            **os.environ,
            "PATH": str(self.bin),
            "UV_CACHE_DIR": fixture_cache(),
            "TRUSTED_PYTHON": PYTHON,
            "TRUSTED_BIN_DIR": str(self.bin),
            "GIT_CONFIG_GLOBAL": "/dev/null",
        }
        self.env.update(dict.fromkeys(("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"), "fixture"))
        self.env.update(dict.fromkeys(("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"), "fixture@example.test"))
        self.git("init", "-q", "-b", "main")
        self.put("scripts/tool.py", "print('tool')\n")
        self.put(DESIGN, self.canonical[DESIGN])
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.task()

    def git(self, *args):
        return subprocess.check_output(
            [GIT, "-c", "commit.gpgsign=false", *args], cwd=self.repo, env=self.env, text=True
        )

    def put(self, name, text):
        p = self.repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def task(self, allowed=None, extra=(), body="", **updates):
        allowed = [*(allowed or ["scripts/tool.py"]), ".orchestration/t-a01/**"]
        rows = [{"control": p, "disposition": RESIDUAL} for p in [*allowed, *NAMES]]
        fm = dict(format=2, task_id="t-a01", kind="code", design_review=dict(design=DESIGN))
        fm.update(allowed_files=allowed, threat_table=rows + list(extra))
        fm.update(updates)
        self.fm = fm
        self.path = self.put(".orchestration/tasks/t-a01.md", "---\n" + json.dumps(fm) + "\n---\n" + body)
        return self.path

    def check(self, digest=False, env=None, prefix=""):
        self.data.write_text(json.dumps(self.canonical))
        args = [str(self.script), "--root", str(self.repo), str(self.path)]
        if digest:
            args[1:1] = ["--premises-sha", hashlib.sha256(self.path.read_bytes()).hexdigest()]
        if prefix:
            prefix += "\nimport sys,runpy;sys.argv.pop(0);runpy.run_path(sys.argv[0],run_name='__main__')"
            args[:0] = ["-c", prefix]
        env = self.env if env is None else env
        result = subprocess.run([*uv(), *args], env=env, cwd=self.repo, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr

    def finding(self, name, **kwargs):
        rc, out = self.check(**kwargs)
        self.assertEqual(rc, 1, out)
        self.assertIn(name + " ", out)
        return out

    def test_private_cache_when_unset(self):
        rc, out = self.check(prefix="import os;os.environ.pop('UV_CACHE_DIR',None)")
        self.assertEqual(rc, 0, out)
        for call in map(json.loads, self.calls.read_text().splitlines()):
            cache = Path(call["cache"])
            self.assertTrue(cache.is_absolute() and not cache.exists())
        self.assertNotEqual(self.check(prefix="import os;os.environ['UV_CACHE_DIR']='relative'")[0], 0)

    def test_interpreter_resolution_order(self):
        resolver = self.script.with_name("trusted-interpreter.sh")
        marker = self.temp / "resolver-ran"
        resolver.write_text(f"#!/bin/bash -p\nprintf called > '{marker}'\nprintf '%s\\n' '{PYTHON}'\n")
        resolver.chmod(0o700)
        env = {**self.env, "TRUSTED_PYTHON": "invalid"}
        self.assertEqual(self.check(env=env)[0], 0)
        self.assertTrue(marker.exists())
        resolver.write_text("#!/bin/bash -p\nexit 19\n")
        self.assertNotEqual(self.check()[0], 0)
        for value in ("relative/python", str(self.repo)):
            resolver.write_text(f"#!/bin/bash -p\nprintf '%s\\n' '{value}'\n")
            self.assertNotEqual(self.check()[0], 0)
        resolver.unlink()
        self.assertEqual(self.check()[0], 0)
        for value in ("relative/python", str(self.temp / "absent"), str(self.repo)):
            self.assertNotEqual(self.check(env={**self.env, "TRUSTED_PYTHON": value})[0], 0)
        env = {k: v for k, v in self.env.items() if k != "TRUSTED_PYTHON"}
        rc, out = self.check(env=env)
        self.assertEqual(rc, 0, out)
        self.assertIn("sys.executable", out)
        self.assertIn("warning", out)

    def test_dispatch_env_i_invocation(self):
        self.data.write_text(json.dumps(self.canonical))
        env = {k: self.env[k] for k in ("PATH", "HOME", "UV_CACHE_DIR")}
        env.update(LANG="C.UTF-8", AGMSG_FIXTURE="retained")
        result = subprocess.run(
            [
                os.path.realpath("/usr/bin/env"),
                "-i",
                *(f"{k}={v}" for k, v in env.items()),
                *uv(),
                str(self.script),
                "--root",
                str(self.repo),
                str(self.path),
            ],
            cwd=self.repo,
            env={},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("t-a01.md: OK", result.stdout)
        self.assertNotIn("TRUSTED_PYTHON", env)
        self.assertNotIn("TRUSTED_BIN_DIR", env)
        for call in map(json.loads, self.calls.read_text().splitlines()):
            self.assertEqual(call["cache"], env["UV_CACHE_DIR"])

    def test_c14_rejects_failed_probe_with_matching_stdout(self):
        for command, output in (("test -e missing", ""), ("test -f scripts", ""), ("git rev-parse no-such-ref", "")):
            with self.subTest(command=command):
                self.task(premises=[dict(command=command, output=output)])
                self.finding("C14", digest=True)
        self.task(premises=[dict(command="test -f scripts/tool.py", output="")])
        self.assertEqual(self.check(digest=True)[0], 0)

    def test_gh_child_preserves_parent_tokens(self):
        trace = self.temp / "launch-boundary.jsonl"
        prefix = (
            "import subprocess,json;_run=subprocess.run\n"
            f"def run(args,**kw):\n with open({str(trace)!r},'a') as stream:stream.write(json.dumps(any(str(a).startswith(tuple(k+'=' for k in ('GH_TOKEN','GITHUB_TOKEN'))) for a in args))+'\\n')\n return _run(args,**kw)\n"
            "subprocess.run=run"
        )
        for names in ((), ("GH_TOKEN",), ("GITHUB_TOKEN",), ("GH_TOKEN", "GITHUB_TOKEN")):
            env = {k: v for k, v in self.env.items() if k not in ("GH_TOKEN", "GITHUB_TOKEN")}
            expected = {k: hashlib.sha256(("synthetic-" + k).encode()).hexdigest() for k in names}
            env.update({k: "synthetic-" + k for k in names})
            self.calls.unlink(missing_ok=True)
            trace.unlink(missing_ok=True)
            self.assertEqual(self.check(env=env, prefix=prefix)[0], 0)
            observed = [json.loads(line) for line in trace.read_text().splitlines()]
            self.assertTrue(observed)
            self.assertFalse(any(observed), "token values entered subprocess argv")
            for call in map(json.loads, self.calls.read_text().splitlines()):
                self.assertEqual(call["tokens"], expected)

    def test_c15_uses_canonical_main_only(self):
        self.canonical.pop(DESIGN)
        self.finding("C15")
        self.canonical[DESIGN] = "---\ninvariants: {}\n---\n"
        env = {
            **self.env,
            "GH_HOST": "attacker.invalid",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "url.https://attacker.invalid/.insteadOf",
            "GIT_CONFIG_VALUE_0": "https://github.com/",
        }
        self.calls.unlink()
        self.assertEqual(self.check(env=env)[0], 0)
        for call in map(json.loads, self.calls.read_text().splitlines()):
            argv = call["argv"]
            self.assertEqual(argv[argv.index("--hostname") + 1], "github.com")
            self.assertTrue(argv[1].startswith("repos/mryfmo/dotfiles/"))
            self.assertIsNone(call["host"])
            if "/contents/" in argv[1]:
                self.assertTrue(argv[1].endswith("?ref=" + MAIN))
        self.canonical[".orchestration/learning/mistakes/cafe\u0301.md"] = "classes: fixture\n"
        self.task(kind="docs", body='"classes: must be present."')
        self.assertEqual(self.check()[0], 0)

    def test_path_grammar_distinguishes_globs_from_git_pathspecs(self):
        for name in ("scripts/a.py", "scripts/nested/b.py", "scripts/x.txt"):
            self.put(name, "fixture\n")
        for pattern in ("scripts/*.py", "scripts/**/?.py", "scripts/[ab].py"):
            self.task(allowed=[pattern])
            out = self.finding("C12")
            if pattern == "scripts/*.py":
                self.assertNotIn("nested/b.py", out)
            if "**" in pattern:
                self.assertIn("nested/b.py", out)
                self.assertIn("scripts/a.py", out)
        invalid = r":(glob)scripts/** :(exclude)scripts/** :!scripts/** /scripts/** ./:!scripts/** scripts/\*.py"
        for pattern in invalid.split():
            self.task(allowed=[pattern])
            self.finding("C12")

    def test_c6_receipt_uses_canonical_design_bytes(self):
        local = (self.repo / DESIGN).read_text()
        dr = dict(design=DESIGN, receipt="r1", design_sha256=hashlib.sha256(local.encode()).hexdigest())
        self.task(design_review=dr)
        self.canonical.pop(DESIGN)
        self.finding("C6")
        self.canonical[DESIGN] = local + "canonical-only bytes\n"
        self.finding("C6")
        dr["design_sha256"] = hashlib.sha256(self.canonical[DESIGN].encode()).hexdigest()
        self.task(design_review=dr)
        self.calls.unlink()
        self.assertEqual(self.check()[0], 0)
        calls = [json.loads(line)["argv"][1] for line in self.calls.read_text().splitlines()]
        self.assertEqual(sum("/contents/" + DESIGN in name for name in calls), 1)
        for value in (None, "bad", "A" * 64, "0" * 64):
            self.task(design_review={**dr, "design_sha256": value})
            self.finding("C6")
        self.task(design_review={k: v for k, v in dr.items() if k != "receipt"})
        self.finding("C6")
        self.task(design_review={**dr, "receipt": "forged"})
        self.finding("C6")
        dr.pop("design_sha256")
        self.task(design_review=dr)
        rc, out = self.check()
        self.assertEqual(rc, 0, out)
        self.assertIn("warning", out)
        self.assertIn("design_sha256", out)
        raw = ".orchestration/plans/cafe\u0301.md"
        other = local.replace("r1", "nfd").replace("invariants:", "implementing_tasks:\n  t-a01: [INV-1]\ninvariants:")
        self.canonical[".orchestration/plans/caf\u00e9.md"] = local
        self.canonical[raw] = other
        dr.update(design=raw, design_sha256=hashlib.sha256(local.encode()).hexdigest())
        self.task(design_review=dr)
        self.assertIn("\n  C15 ", self.finding("C6"))
        self.canonical.pop(raw)
        self.assertIn("\n  C15 ", self.finding("C6"))
        self.canonical[raw] = other
        dr.update(receipt="nfd", design_sha256=hashlib.sha256(other.encode()).hexdigest())
        self.task(design_review=dr, invariants={"INV-1": "exact sentence"})
        self.assertEqual(self.check()[0], 0)

    def test_path_grammar_covers_root_files(self):
        self.put("AGENTS.md", "instructions\n")
        self.put("Makefile", "all:\n")
        self.task(allowed=["*"])
        out = self.finding("C12")
        self.assertIn("AGENTS.md", out)
        self.assertIn("Makefile", out)
        self.task(allowed=["AGENTS.md", "Makefile"])
        self.assertEqual(self.check()[0], 0)

    def test_path_grammar_separates_directory_and_child_rows(self):
        self.task(allowed=["scripts/", "scripts/tool.py"])
        self.assertEqual(self.check()[0], 0)
        row = dict(control="scripts/ and scripts/tool.py", disposition=RESIDUAL)
        self.task(allowed=["scripts/", "scripts/tool.py"], extra=[row])
        self.finding("C7b")
        self.put("scripts/tool.sh", "fixture\n")
        row = dict(control="scripts/tool.py and scripts/tool.sh", disposition=RESIDUAL)
        self.task(allowed=["scripts/*.py", "scripts/*.sh"], extra=[row])
        self.finding("C7b")

    def test_path_grammar_normalises_dot_spellings(self):
        self.task(allowed=["./scripts/./tool.py"])
        self.fm["threat_table"][0]["control"] = "scripts/tool.py"
        self.path.write_text("---\n" + json.dumps(self.fm) + "\n---\n")
        self.assertEqual(self.check()[0], 0)
        self.task(allowed=["./scripts/*.py"])
        self.assertIn("scripts/tool.py", self.finding("C12"))

    def test_path_grammar_rejects_escaping_scopes(self):
        self.task(allowed=["../../outside/*.py"])
        self.assertIn("confin", self.finding("C12"))
        outside = self.put(self.temp / "outside.py", "outside\n")
        (self.repo / "scripts/escape.py").symlink_to(outside)
        for scope in ("scripts/*.py", "scripts/", "scripts/**"):
            self.task(allowed=[scope])
            self.assertIn("confin", self.finding("C12"))
        directory = self.put(self.temp / "external/tool.py", "outside\n").parent
        (self.repo / "scripts/link").symlink_to(directory, target_is_directory=True)
        self.task(allowed=["scripts/link/*.py"])
        self.assertIn("confin", self.finding("C12"))

    def test_exempt_symlink_to_applied_file_is_finding(self):
        self.put("tests/fixtures/data.txt", "data\n")
        self.task(allowed=["tests/fixtures/**"])
        self.assertEqual(self.check()[0], 0)
        (self.repo / "tests/fixtures/hidden.py").symlink_to(self.repo / "scripts/tool.py")
        self.assertIn("hidden.py", self.finding("C12"))

    def test_security_c12_prunes_with_normalised_directory_names(self):
        raw = "scripts/cafe\u0301/tool.py"
        self.put(raw, "applied\n")
        self.task(allowed=["scripts/cafe\u0301/*.py"])
        prefix = (
            "import os,unicodedata;_walk=os.walk\n"
            "def walk(*a,**k):\n for folder,dirs,names in _walk(*a,**k):\n  dirs[:]=[unicodedata.normalize('NFD',n) for n in dirs]\n  yield folder,dirs,names\n"
            "os.walk=walk"
        )
        self.assertIn("tool.py", self.finding("C12", prefix=prefix))
        row = dict(control=raw, disposition=RESIDUAL)
        outside = self.put(self.temp / "outside.py", "outside\n")
        alias = self.repo / "scripts/cafe\u0301/escape.py"
        alias.symlink_to(outside)
        self.task(allowed=["scripts/cafe\u0301/*.py"], extra=[row])
        self.assertIn("confin", self.finding("C12", prefix=prefix))
        alias.unlink()
        self.assertEqual(self.check(prefix=prefix)[0], 0)

    def test_security_c16_uses_resolved_literal_alias(self):
        target = self.put("scripts/orchestrator/tool.py", "applied\n")
        alias = self.repo / "tests/fixtures/audit-alias.py"
        alias.parent.mkdir(parents=True)
        alias.symlink_to(target)
        self.task(allowed=["tests/fixtures/audit-alias.py"], security=True)
        self.finding("C16")
        items = [dict(control=f"5.14 item {i}: reference", disposition=RESIDUAL) for i in range(11)]
        self.task(allowed=["tests/fixtures/audit-alias.py"], extra=items, security=True, body=REFERENCE)
        self.assertEqual(self.check()[0], 0)

    def test_canonical_path_pipeline_rejects_normalised_collisions(self):
        nfc, nfd = "scripts/caf\u00e9.py", "scripts/cafe\u0301.py"
        first = self.put(nfd, "applied\n")
        rows = [dict(control=n, disposition=RESIDUAL) for n in ("scripts/tool.py", nfd)]
        self.task(allowed=["scripts/**"], extra=rows)
        self.assertEqual(self.check()[0], 0)
        self.task(allowed=["scripts/**", nfd], extra=rows)
        self.assertEqual(self.check()[0], 0)
        targets = [self.put(f"tests/fixtures/target-{i}.py", "fixture\n") for i in range(2)]
        for destinations in (targets, [targets[0]] * 2):
            prefix = (
                "import os,pathlib,unicodedata;_walk=os.walk;_resolve=pathlib.Path.resolve;_exists=pathlib.Path.exists;_is_file=pathlib.Path.is_file\n"
                f"mapping={dict(zip([str(self.repo / n) for n in (nfc, nfd)], map(str, destinations)))!r}\n"
                "def resolve(p,*a,**k):\n return pathlib.Path(mapping[str(p)]) if str(p) in mapping else _resolve(p,*a,**k)\n"
                f"def walk(*a,**k):\n for folder,dirs,names in _walk(*a,**k):\n  if folder=={str(self.repo / 'scripts')!r}:names=[n for n in names if unicodedata.normalize('NFC',n)!={Path(nfc).name!r}]+{[Path(nfc).name, Path(nfd).name]!r}\n  yield folder,dirs,names\n"
                f"os.walk=walk;pathlib.Path.resolve=resolve;pathlib.Path.exists=lambda p:False if str(p)=={str(self.repo / nfc)!r} else _exists(p);pathlib.Path.is_file=lambda p:False if str(p)=={str(self.repo / nfc)!r} else _is_file(p)"
            )
            self.assertIn("path collision:", self.finding("C12", prefix=prefix))
            if destinations is targets:
                one = prefix.replace(repr([Path(nfc).name, Path(nfd).name]), repr([Path(nfc).name]))
                self.assertNotIn("path collision:", self.finding("C12", prefix=one))
        second = self.put(nfc, "different applied file\n")
        distinct = not first.samefile(second)
        print(f"native-NFC-NFD-distinct={distinct}", flush=True)
        with self.subTest("native two-file collision"):
            if not distinct:
                self.skipTest("observed NFC/NFD samefile alias; modeled collision and one-file control ran")
            out = self.finding("C12")
            self.assertIn("path collision:", out)
            for name in (nfc, nfd):
                self.assertIn(name, out)

    def test_c10_confines_original_unicode_script_paths(self):
        outside = self.put(self.temp / "outside.py", "outside\n")
        for name in ("scripts/cafe\u0301.py", "scripts/caf\u00e9.py"):
            path = self.repo / name
            path.unlink(missing_ok=True)
            path.symlink_to(outside)
            self.task(kind="docs", body=f'"{name} must support mode=1 once the separate feature lands."')
            self.finding("C10")
            path.unlink()
            self.put(name, "confined control\n")
            self.assertEqual(self.check()[0], 0)

    def test_canonical_path_pipeline_preserves_identity(self):
        raw = [".orchestration/plans/cafe\u0301.md", "tests/cafe\u0301.py", "scripts/cafe\u0301.py"]
        benign = self.put("tests/fixtures/benign.txt", "marker\n")
        outside = self.put(self.temp / "outside", "outside secret\n")
        for name in raw:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(outside)
        self.canonical[raw[0]] = self.canonical[DESIGN]
        prefix = (
            "import pathlib,unicodedata;_resolve=pathlib.Path.resolve\n"
            f"nfc={{unicodedata.normalize('NFC',str(p)) for p in {[str(self.repo / n) for n in raw]!r}}}\n"
            f"def resolve(p,*a,**k):\n return pathlib.Path({str(benign)!r}) if str(p) in nfc else _resolve(p,*a,**k)\n"
            "pathlib.Path.resolve=resolve"
        )
        self.task(
            extra=[dict(control="selector", disposition=f"closed: {raw[1]}::test_ok")],
            design_review=dict(design=raw[0], receipt="r1"),
            premises=[dict(command=f"grep -c marker {raw[2]}", output="1")],
        )
        rc, out = self.check(digest=True, prefix=prefix)
        self.assertEqual(rc, 1, out)
        for finding in ("C6 ", "C11 ", "C14 "):
            self.assertIn("\n  " + finding, out)
        for name in raw:
            (self.repo / name).unlink()
            self.put(name, "marker\n")
        self.assertEqual(self.check(digest=True, prefix=prefix)[0], 0)

    def test_security_c12_resolves_original_unicode_path(self):
        benign = self.put("tests/fixtures/ordinary.py", "fixture\n")
        outside = self.put(self.temp / "outside.py", "outside\n")
        (self.repo / "tests/fixtures/cafe\u0301.py").symlink_to(outside)
        nfc = self.repo / "tests/fixtures/caf\u00e9.py"
        self.task(allowed=["tests/fixtures/**"])
        # Model distinct Unicode spellings even on normalization-insensitive hosts.
        prefix = (
            "import pathlib,os,unicodedata;_resolve=pathlib.Path.resolve;_walk=os.walk\n"
            f"def resolve(p,*a,**k):\n return pathlib.Path({str(benign)!r}) if str(p)=={str(nfc)!r} else _resolve(p,*a,**k)\n"
            "def walk(*a,**k):\n for folder,dirs,names in _walk(*a,**k):\n  yield folder,dirs,[unicodedata.normalize('NFD',n) for n in names]\n"
            "pathlib.Path.resolve=resolve;os.walk=walk"
        )
        self.assertIn("confin", self.finding("C12", prefix=prefix))

    def test_security_c12_rejects_internal_directory_alias(self):
        self.put("tests/fixtures/data.txt", "fixture\n")
        alias = self.repo / "tests/fixtures/alias"
        alias.symlink_to(self.repo / "scripts", target_is_directory=True)
        for scope in ("tests/fixtures/**", "tests/fixtures/alias"):
            self.task(allowed=[scope])
            self.assertIn("alias", self.finding("C12"))
        row = dict(control="tests/fixtures/alias", disposition=RESIDUAL)
        self.task(allowed=["tests/fixtures/**"], extra=[row])
        self.finding("C12")
        alias.unlink()
        self.task(allowed=["tests/fixtures/**"])
        self.assertEqual(self.check()[0], 0)

    def test_security_c16_rejects_multi_item_rows(self):
        self.put("scripts/orchestrator/tool.py", "fixture\n")
        items = [dict(control=f"5.14 item {i}: reference", disposition=RESIDUAL) for i in range(11)]
        concrete = dict(control="scripts/orchestrator/tool.py", disposition=RESIDUAL)
        allowed = ["scripts/orchestrator/*.py"]
        for pair, trim in (((0, 1), 0), ((0, 0), 0), ((11, 12), 0), ((0, 1), 2)):
            combined = dict(control=" and ".join(f"5.14 item {i}" for i in pair), disposition=items[0]["disposition"])
            self.task(allowed=allowed, extra=[concrete, *items[trim:], combined], security=True, body=REFERENCE)
            out = self.finding("C16")
            if pair == (0, 0):
                self.assertIn("item 0: count 3", out)

    def test_exempt_case_alias_to_applied_file_is_finding(self):
        self.put("Tests/Fixtures/agent.py", "applied\n")
        self.task(allowed=["tests/fixtures/**"])
        prefix = "import os;os.path.normcase=lambda value:os.fspath(value).casefold()"
        self.assertIn("agent.py", self.finding("C12", prefix=prefix))
        alias = self.repo.with_name(self.repo.name.swapcase())
        native = alias.exists() and alias.samefile(self.repo)
        print(f"native-case-insensitive={native}", flush=True)
        if native:
            self.assertIn("agent.py", self.finding("C12"))

    def test_c12_classifies_backslash_filenames_from_resolved_ancestry(self):
        weird = self.put("scripts/evil\\name", "applied\n")
        self.put("scripts/named", "named applied control\n")
        rows = [dict(control=n, disposition=RESIDUAL) for n in ("scripts/tool.py", "scripts/named")]
        self.task(allowed=["scripts/**"], extra=rows)
        self.assertIn("scripts/evil\\name", self.finding("C12"))
        weird.unlink()
        self.assertEqual(self.check()[0], 0)

    def test_c12_covers_applied_skill_instructions(self):
        self.put(".claude/skills/example/SKILL.md", "instructions\n")
        self.task(allowed=[".claude/skills/**"])
        self.assertIn("SKILL.md", self.finding("C12"))

    def test_c16_requires_reference_and_all_item_rows(self):
        allowed = ["scripts/orchestrator/*.py"]
        self.put("scripts/orchestrator/tool.py", "fixture\n")
        items = [dict(control=f"5.14 item {i}: reference", disposition=RESIDUAL) for i in range(11)]
        concrete = dict(control="scripts/orchestrator/tool.py", disposition=RESIDUAL)
        self.task(allowed=allowed, extra=[concrete, *items], security=True)
        self.finding("C16")
        for rows in (items[:-1], [*items, items[1]]):
            self.task(allowed=allowed, extra=[concrete, *rows], security=True, body=REFERENCE)
            self.finding("C16")
        combined = dict(control=" and ".join(r["control"] for r in items), disposition=items[0]["disposition"])
        self.task(allowed=allowed, extra=[concrete, combined], security=True, body=REFERENCE)
        self.finding("C16")
        self.task(allowed=allowed, extra=[concrete, *items], security=True, body=REFERENCE)
        self.assertEqual(self.check()[0], 0)
        self.task(security=False)
        self.assertEqual(self.check()[0], 0)
        self.task(allowed=["AGENTS.md"], security=True)
        self.assertEqual(self.check()[0], 0)
        base = dict(control="scripts/tool.py", disposition=RESIDUAL)
        for scope in ("scripts/**", "**/tool.py"):
            self.task(allowed=[scope], extra=[base, concrete, *items], security=True)
            self.finding("C16")
            self.task(allowed=[scope], extra=[base, concrete, *items], security=True, body=REFERENCE)
            self.assertEqual(self.check()[0], 0)

    def test_reset_scope_rejects_hidden_predecessor_artifacts(self):
        copies = ".orchestration/t-a00/task.md and .orchestration/t-a01/task.md"
        row = dict(control=f"task metadata reset copies: {copies}", disposition=RESIDUAL)
        self.task(extra=[row], reset_of=["t-a00"], retained_predecessor_directories=[])
        self.assertEqual(self.check()[0], 0)
        self.task(
            allowed=["./.orchestration/t-a00/**"], extra=[row], reset_of=["t-a00"], retained_predecessor_directories=[]
        )
        self.finding("C2")

    def test_retained_c11_c13_and_fixed_probe_controls(self):
        for disposition, name in (
            ("residual: short", "C11"),
            ("closed: tests/../../outside.py::Suite::test_ok", "C11"),
            ("closed: tests/unit/test.py::two words", "C11"),
            ("out-of-scope: nonexistent-task", "C11"),
            ("accepted: fixture approval", "C13"),
        ):
            self.task(extra=[dict(control="extra", disposition=disposition)])
            self.finding(name)
        self.put(".orchestration/tasks/owner-a01.md", "owner\n")
        self.task(extra=[dict(control="extra", disposition="out-of-scope: owner-a01")])
        self.assertEqual(self.check()[0], 0)
        marker = self.repo / "ran"
        self.put("probe.py", f"open({str(marker)!r},'w').close()\n")
        for command in ("python -I probe.py", f"test -f scripts/tool.py; touch {marker}"):
            self.task(premises=[dict(command=command, output="")])
            self.finding("C14", digest=True)
            self.assertFalse(marker.exists())
        self.task(premises=[dict(command="test -e missing", output="")])
        rc, out = self.check()
        self.assertEqual(rc, 0, out)
        self.assertIn("C14: not run (no trusted sha)", out)
        self.put("literal", "[\n[a\nplain\n")
        self.task(premises=[dict(command="grep -c '[' literal", output=" 2 ")])
        self.assertEqual(self.check(digest=True)[0], 0)

    def test_checker_rejects_untrusted_bindings_and_git_configuration(self):
        marker = self.temp / "ran"
        bad = self.put("git", f"#!/bin/sh\ntouch '{marker}'\n")
        bad.chmod(0o700)
        (self.bin / "git").unlink()
        (self.bin / "git").symlink_to(bad)
        rc, out = self.check()
        self.assertNotEqual(rc, 0, out)
        self.assertIn("checkout executable", out)
        self.assertFalse(marker.exists())
        (self.bin / "git").unlink()
        (self.bin / "git").symlink_to(Path(GIT).resolve())
        shim = self.temp / "shims/python"
        shim.parent.mkdir()
        shim.symlink_to(PYTHON)
        worker = self.put(self.temp / ".claude/worktrees/seat/python", "invalid")
        for path, named in ((shim, "shim"), (worker, "worker-root")):
            rc, out = self.check(env={**self.env, "TRUSTED_PYTHON": str(path)})
            self.assertNotEqual(rc, 0, out)
            self.assertIn(named, out)
        self.env.update(GIT_DIR=str(self.temp), GIT_WORK_TREE=str(self.temp), GIT_CONFIG_PARAMETERS="hostile")
        self.assertEqual(self.check()[0], 0)
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_PARAMETERS"):
            self.env.pop(key)
        self.git("config", "filter.fixture.clean", f"touch '{marker}'")
        rc, out = self.check()
        self.assertNotEqual(rc, 0, out)
        self.assertIn("Git configuration", out)
        self.assertFalse(marker.exists())
        self.git("config", "--unset", "filter.fixture.clean")
        self.put(".gitmodules", "[submodule]\n")
        self.assertIn(".gitmodules", self.check()[1])

    def test_isolated_child_and_same_bytes_survive_hostile_startup_inputs(self):
        marker = self.temp / "startup-ran"
        for name in (".venv/bin/python", "site/usercustomize.py", "site/sitecustomize.py", "site/evil.pth"):
            self.put(name, f"open({str(marker)!r},'w').close()\n")
        self.put("uv.toml", f'cache-dir = "{self.repo / "bad-cache"}"\n')
        env = {
            **self.env,
            "VIRTUAL_ENV": str(self.repo / ".venv"),
            "PYTHONPATH": str(self.repo / "site"),
            "PYTHONUSERBASE": str(self.repo / "site"),
        }
        self.assertEqual(self.check(env=env)[0], 0)
        self.assertFalse(marker.exists())
        self.assertFalse((self.repo / "bad-cache").exists())
        self.assertEqual(uv()[-2:], ["python", "-I"])
        for flag in ("--no-config", "--no-project", "--offline", "--python"):
            self.assertIn(flag, uv())
        self.assertEqual(uv()[uv().index("--python") + 1], PYTHON)
        self.task(premises=[dict(command="test -f scripts/tool.py", output="")])
        prefix = (
            "import pathlib;_read=pathlib.Path.read_bytes\n"
            f"def read(p):\n data=_read(p)\n if str(p)=={str(self.path)!r}:p.write_text('replaced after reading')\n return data\n"
            "pathlib.Path.read_bytes=read"
        )
        rc, out = self.check(digest=True, prefix=prefix)
        self.assertEqual(rc, 0, out)
        self.assertNotIn("C14: not run (no trusted sha)", out)
        self.assertEqual(self.path.read_text(), "replaced after reading")


if __name__ == "__main__":
    unittest.main()
