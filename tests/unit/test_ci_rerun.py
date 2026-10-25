"""Exercise scripts/orchestrator/ci-rerun.sh with a stub gh only (plan 024 P1-3, T133).

Each test copies the script into a temporary git repository, its root, beside a fixture .github/flakes.yaml, and runs
it with a stub `gh` first on PATH and stdin closed. The stub answers `gh run view`, the run's pull requests
(`gh api …/actions/runs/<id>`) and a pull request's head (`gh pr view`, a list of heads read in turn) from a JSON map
the test writes; it records every argv and, for `gh run rerun`, whether the run's reservation directory and ledger
rows exist at that moment; any other call fails. No call reaches GitHub. The production-registry test reads the
checked-in .github/flakes.yaml with the script's own YAML loader and matches with `grep -E`, the script's engine.
"""

import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUB = """#!@PYTHON@
import json, os, subprocess, sys, time
from pathlib import Path
args, runs = sys.argv[1:], json.load(open(os.environ["GH_RUNS"]))
entry = {"argv": args}
if args[:2] == ["run", "rerun"]:
    validation = Path(os.environ["GH_REPO_ROOT"]) / ".orchestration/validation"
    ledger = validation / "ci-reruns.tsv"
    entry["reserved"] = (validation / "ci-reruns.lock.d" / args[2]).is_dir()
    entry["rows"] = ledger.read_text().count("\\t" + args[2] + "\\t") if ledger.exists() else 0
with open(os.environ["GH_LOG"], "a") as log:
    log.write(json.dumps(entry) + "\\n")
if os.environ.get("GH_EXIT"):
    sys.exit(int(os.environ["GH_EXIT"]))
if args[:2] == ["run", "rerun"]:
    sys.exit(int(os.environ.get("GH_RERUN_EXIT") or 0))
if args[:2] == ["run", "view"] and "--json" in args:
    print(json.dumps(runs[args[2]]))
elif args[:2] == ["run", "view"]:
    time.sleep(float(os.environ.get("GH_LOG_DELAY") or 0))
    print(runs["logs"].get(args[args.index("--job") + 1], ""))
elif args[0] == "api":  # the script's own --jq filter, run on the run's pull_requests payload
    payload = {"pull_requests": [{"number": n} for n in runs["prs"][args[1].rsplit("/", 1)[1]]]}
    jq = ["jq", "-r", args[args.index("--jq") + 1]]
    sys.exit(subprocess.run(jq, input=json.dumps(payload), text=True, check=False).returncode)
elif args[:2] == ["pr", "view"] and args[2] in runs["heads"]:
    turn = Path(os.environ["GH_LOG"] + "." + args[2])
    seen = len(turn.read_text()) if turn.exists() else 0
    turn.write_text("." * (seen + 1))
    print(runs["heads"][args[2]][min(seen, len(runs["heads"][args[2]]) - 1)])
else:
    sys.exit("stub gh: unexpected call " + " ".join(args))
"""
FLAKES = r"""# Fixture signatures.
- id: snap-timeout
  job: '^public-bootstrap \(ubuntu-'
  log_regex: 'got unexpected HTTP status code 408 via GET to "https://api\.snapcraft\.io/'
  note: fixture
- id: brew-tap
  job: '\(macos-14, '
  log_regex: 'Error: Failed to fetch tap'
  note: fixture
"""
SNAP = 'error: cannot perform: got unexpected HTTP status code 408 via GET to "https://api.snapcraft.io/v2/assertions"'
HEAD, NEWER = "a" * 40, "b" * 40
# measure.md: the measured failed job and log line behind each production signature, keyed by its id.
SAMPLES = {
    "snapcraft-assertion-timeout": (
        "public-bootstrap (ubuntu-24.04, client)",
        (
            '2026-10-17T15:53:34.0927711Z - Fetch and check assertions for snap "gtk-common-themes" (1535) (cannot'
            ' fetch assertion: got unexpected HTTP status code 408 via GET to "https://api.snapcraft.io/v2/assertions/'
            'snap-revision/62rRwo_VHrOdajhLlnNTqUJ8gfWoZZNSFWhxn2AszCKyUAD0d8guxddMFeW5LVKP?max-format=0")'
        ),
    ),
}
# measure.md: run 39079197825's test_validate_agent_assets failure, and a plain test assertion failure.
REAL_FAILURES = (
    (
        "2026-10-17T23:34:03.4319369Z ERROR: test_claude_gh_merge_gate_keeps_writes_on_ask_and_requires_the_hook"
        " (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_gh_merge_gate_keeps_writes_on_ask_and_requires_the_hook)"
        "\n2026-10-17T23:34:03.4320796Z Traceback (most recent call last):\n##[error]Process completed with exit code 1."
    ),
    (
        "FAIL: test_something (tests.unit.test_x.XTest.test_something)\nAssertionError: 1 != 2\n"
        "##[error]Process completed with exit code 1."
    ),
)


def job(number, name, conclusion="failure"):
    return {"databaseId": number, "name": name, "conclusion": conclusion, "status": "completed"}


def run(head, *jobs, event="pull_request"):
    return {"status": "completed", "conclusion": "failure", "headSha": head, "event": event, "jobs": list(jobs)}


def egrep(pattern, text):
    """grep -E as the script runs it: 0 a match, 1 none, 2 a pattern that does not compile."""
    return subprocess.run(["grep", "-Eq", "--", pattern], input=text, text=True, check=False).returncode


def real_tool(tool):
    """The tool outside any shims directory: the first such PATH entry, else what the host's mise answers."""
    for entry in os.environ["PATH"].split(os.pathsep):
        if entry.startswith("/") and "/shims/" not in os.path.realpath(entry) + "/":
            found = shutil.which(tool, path=entry)
            if found:
                return found
    answer = subprocess.run(["mise", "which", tool], capture_output=True, text=True, check=False)
    if answer.returncode == 0 and answer.stdout.strip().startswith("/"):
        return answer.stdout.strip()
    raise AssertionError(f"no {tool} outside a shims directory on this host")


def registry(path):
    """The flake file through the script's loader: PyYAML under uv, the offline cache first."""
    script = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1])) or []))"
    for offline in (["--offline"], []):
        command = ["uv", "run", *offline, "--no-project", "--quiet", "--with", "pyyaml", "python", "-I", "-c", script]
        loaded = subprocess.run(
            [*command, str(path)], capture_output=True, text=True, stdin=subprocess.DEVNULL, check=False
        )
        if loaded.returncode == 0:
            return json.loads(loaded.stdout)
    raise AssertionError(loaded.stderr)


class CiRerunTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.t = Path(temp.name).resolve()
        self.repo = self.t / "repo"
        (self.repo / "scripts/orchestrator").mkdir(parents=True)
        (self.repo / ".github").mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        shutil.copy(ROOT / "scripts/orchestrator/ci-rerun.sh", self.repo / "scripts/orchestrator")
        (self.repo / ".github/flakes.yaml").write_text(FLAKES)
        (self.t / "bin").mkdir()
        gh = self.t / "bin/gh"
        gh.write_text(STUB.replace("@PYTHON@", sys.executable))
        gh.chmod(0o755)
        # The script's resolver: a stub mise that answers `mise which <tool>` from mise.json, so every test pins the
        # same real tools whatever shims lead the host's PATH; a tool missing from the map falls back to PATH.
        self.answers = self.t / "mise.json"
        mise = self.t / "bin/mise"
        mise.write_text(
            f"#!{sys.executable}\nimport json, sys\nanswers = json.load(open({str(self.answers)!r}))\n"
            "if sys.argv[1:2] != ['which'] or sys.argv[2] not in answers:\n    sys.exit(1)\nprint(answers[sys.argv[2]])\n"
        )
        mise.chmod(0o755)
        self.real = {tool: real_tool(tool) for tool in ("python3", "uv", "jq", "git", "mkdir")} | {"gh": str(gh)}
        self.answer()
        # The same real tools behind wrappers, for the no-answer fallback under a PATH the test controls.
        self.tools = self.t / "tools"
        self.tools.mkdir()
        for tool, real in self.real.items():
            if tool != "gh":
                (self.tools / tool).write_text(f'#!/bin/sh\nexec "{real}" "$@"\n')
                (self.tools / tool).chmod(0o755)
        self.log = self.t / "gh.log"
        self.ledger = self.repo / ".orchestration/validation/ci-reruns.tsv"
        self.runs = {
            "101": run(
                HEAD,
                job(1, "public-bootstrap (ubuntu-24.04, client)"),
                job(2, "test (macos-14, client)"),
                job(3, "validate", "success"),
            ),
            "202": run(NEWER, job(4, "public-bootstrap (ubuntu-24.04, server)"), job(5, "test (ubuntu-24.04, client)")),
            "303": run(HEAD, job(6, "public-bootstrap (ubuntu-24.04, server)")),
            "logs": {
                "1": SNAP,
                "2": "Error: Failed to fetch tap homebrew/fixture",
                "4": SNAP,
                "5": "FAIL: test_something\nAssertionError: 1 != 2",
                "6": SNAP,
            },
            "prs": {"101": [9], "202": [10], "303": [11]},
            "heads": {"9": [HEAD], "10": [NEWER], "11": [HEAD]},
        }

    def reservation(self, run_id):
        return self.ledger.with_name("ci-reruns.lock.d") / run_id

    def answer(self, **answers):
        """What the stub mise answers: the real tools, overridden by name."""
        self.answers.write_text(json.dumps(self.real | answers))

    def reset(self):
        self.ledger.unlink(missing_ok=True)
        shutil.rmtree(self.ledger.with_name("ci-reruns.lock.d"), ignore_errors=True)
        self.log.write_text("")
        for turn in self.t.glob("gh.log.*"):
            turn.unlink()
        (self.t / "runs.json").write_text(json.dumps(self.runs))

    def start(self, run_id, cwd=None, **env):
        return subprocess.Popen(
            ["bash", str(self.repo / "scripts/orchestrator/ci-rerun.sh"), run_id],
            cwd=cwd,
            env=os.environ
            | {
                "PATH": str(self.t / "bin") + os.pathsep + os.environ["PATH"],
                "GH_LOG": str(self.log),
                "GH_RUNS": str(self.t / "runs.json"),
                "GH_REPO_ROOT": str(self.repo),
                **env,
            },
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def finish(self, process):
        out, err = process.communicate(timeout=120)
        return subprocess.CompletedProcess(process.args, process.returncode, out, err)

    def entries(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def reruns(self):
        return [entry for entry in self.entries() if entry["argv"][:2] == ["run", "rerun"]]

    def run_script(self, run_id, gh_exit="", rerun_exit="", fresh=False):
        if fresh:
            self.reset()
        self.log.write_text("")
        for turn in self.t.glob("gh.log.*"):
            turn.unlink()
        (self.t / "runs.json").write_text(json.dumps(self.runs))
        result = self.finish(self.start(run_id, GH_EXIT=gh_exit, GH_RERUN_EXIT=rerun_exit))
        return result, [entry["argv"] for entry in self.entries()]

    def test_ci_rerun_outside_a_git_checkout_refuses_before_any_gh_call(self):
        shutil.rmtree(self.repo / ".git")
        self.reset()

        result = self.finish(self.start("101", GIT_CEILING_DIRECTORIES=str(self.t)))

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual([], self.entries())
        self.assertFalse(self.ledger.exists())
        self.assertFalse(self.reservation("101").exists())

    def test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature(self):
        result, calls = self.run_script("101")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, calls.count(["run", "rerun", "101", "--failed"]))
        rows = [line.split("\t") for line in self.ledger.read_text().splitlines()]
        self.assertEqual(
            [
                ["101", HEAD, "public-bootstrap (ubuntu-24.04, client)", "snap-timeout"],
                ["101", HEAD, "test (macos-14, client)", "brew-tap"],
            ],
            [row[1:] for row in rows],
        )
        self.assertRegex(rows[0][0], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")

        result, calls = self.run_script("101")
        self.assertEqual(4, result.returncode, result.stdout + result.stderr)
        self.assertEqual([], calls)

        before = self.ledger.read_text()
        result, calls = self.run_script("202")
        self.assertEqual(3, result.returncode, result.stdout + result.stderr)
        self.assertIn("real failure: test (ubuntu-24.04, client)", result.stdout)
        self.assertNotIn("real failure: public-bootstrap", result.stdout)
        self.assertNotIn(["run", "rerun", "202", "--failed"], calls)
        self.assertEqual(before, self.ledger.read_text())

    def test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice(self):
        # The run's reservation and every row exist when gh receives the rerun, so a failed or interrupted rerun stays
        # recorded and is never repeated.
        result, _ = self.run_script("101", rerun_exit="1")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual([{"argv": ["run", "rerun", "101", "--failed"], "reserved": True, "rows": 2}], self.reruns())
        self.assertTrue(self.reservation("101").is_dir())
        self.assertEqual(["101", "101"], [line.split("\t")[1] for line in self.ledger.read_text().splitlines()])
        result, calls = self.run_script("101")
        self.assertEqual(4, result.returncode, result.stdout + result.stderr)
        self.assertEqual([], calls)

    def test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs(self):
        # a01 audit P2: one checkout-wide lock blocked every run while one call ran or after one was killed.
        self.reset()
        same = [self.start("101", GH_LOG_DELAY="1") for _ in range(2)]
        self.assertEqual([0, 4], sorted(self.finish(process).returncode for process in same))
        self.assertEqual(1, len(self.reruns()))
        # PR #409's ubuntu-26.04 canary: uutils' mkdir before bf423f388d (2026-08-28) returned 0 for a directory another
        # call had just created, so the claim must not rest on the mkdir binary.
        (fake := self.t / "uutils").mkdir()
        (fake / "mkdir").write_text('#!/usr/bin/env bash\n/bin/mkdir "$@" 2> /dev/null || [ -d "${!#}" ]\n')
        (fake / "mkdir").chmod(0o755)
        self.reset()
        self.answer(mkdir=str(fake / "mkdir"))  # the resolver pins what mise answers, so the fake goes in there
        racing = [self.start("101", GH_LOG_DELAY="1") for _ in range(2)]
        self.assertEqual([0, 4], sorted(self.finish(process).returncode for process in racing))
        self.assertEqual(1, len(self.reruns()))
        self.answer()
        self.reset()
        distinct = [self.start(run_id, GH_LOG_DELAY="1") for run_id in ("101", "303")]
        self.assertEqual([0, 0], [self.finish(process).returncode for process in distinct])
        self.assertEqual({"101", "303"}, {entry["argv"][2] for entry in self.reruns()})
        self.reset()
        self.reservation("101").mkdir(parents=True)  # abandoned: no ledger row
        result, calls = self.run_script("101")
        self.assertEqual(4, result.returncode, result.stdout + result.stderr)
        self.assertEqual([], calls)
        result, _ = self.run_script("303")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment(self):
        # security:4fe2438:1: run from a PR checkout, uv took its .python-version (or .venv, UV_PYTHON, VIRTUAL_ENV).
        checkout, marker = self.t / "checkout", self.t / "planted.log"
        python = checkout / ".venv/bin/python"
        python.parent.mkdir(parents=True)
        python.write_text(f'#!/bin/sh\necho "$0" >> "{marker}"\nexec "{sys.executable}" "$@"\n')  # works, leaves a mark
        python.chmod(0o755)
        (checkout / ".venv/pyvenv.cfg").write_text(f"home = {Path(sys.executable).parent}\n")
        (checkout / ".python-version").write_text(f"{python}\n")
        for tool in ("mktemp", "ln"):  # the checkout's own, reached through the empty PATH entry below
            (checkout / tool).write_text(f'#!/bin/sh\necho "{tool}" >> "{marker}"\nexit 1\n')
            (checkout / tool).chmod(0o755)
        self.reset()
        selectors = {"UV_PYTHON": str(python), "VIRTUAL_ENV": str(checkout / ".venv")}
        selectors["PATH"] = os.pathsep + str(self.t / "bin") + os.pathsep + os.environ["PATH"]
        result = self.finish(self.start("101", cwd=checkout, **selectors))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, len(self.reruns()))
        self.assertFalse(marker.exists(), "a checkout or inherited selector ran the planted interpreter")

    def test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path(self):
        # Worker review P1: CPython reads pyvenv.cfg beside, and one directory above, the path it was started by, so a
        # link under a shared TMPDIR would let ${TMPDIR}/pyvenv.cfg choose its standard library.
        python, seen = self.t / "py/python3", self.t / "started.log"
        python.parent.mkdir()
        python.write_text(f'#!/bin/sh\necho "$0" >> "{seen}"\nexec "{sys.executable}" "$@"\n')
        python.chmod(0o755)
        self.reset()
        self.answer(python3=str(python))
        path = f"{python.parent}{os.pathsep}{self.t / 'bin'}{os.pathsep}{os.environ['PATH']}"
        result = self.finish(self.start("101", PATH=path))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual({str(python)}, set(seen.read_text().split()))

    def test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin(self):
        # Revise 1 (the chain's P1 on 7329f0e): before PATH is pinned, the EXIT trap's rm and the env around mise ran
        # whatever the caller's PATH named. mise is the resolver the design names; setUp's stub stands in for it, and
        # here it answers nothing (or a shim), so every tool falls back to a PATH this test controls.
        planted, shims, marker = self.t / "planted", self.t / "shims", self.t / "planted.log"
        for tool, real in (("rm", "/bin/rm"), ("env", "/usr/bin/env")):  # each works, and leaves a mark
            (planted / tool).parent.mkdir(exist_ok=True)
            (planted / tool).write_text(f'#!/bin/sh\necho "{tool}" >> "{marker}"\nexec {real} "$@"\n')
            (planted / tool).chmod(0o755)
        shims.mkdir()
        (shims / "jq").write_text("#!/bin/sh\nexit 1\n")
        (shims / "jq").chmod(0o755)
        base = os.pathsep.join(map(str, (planted, self.t / "bin", self.tools, "/usr/bin", "/bin")))
        (self.t / "linked").symlink_to(shims)  # a PATH entry that links to a shims directory is a shims directory
        cases = [
            ("refused before the pin", shims, {}, 1),
            ("refused through a link", self.t / "linked", {}, 1),
            ("refused as mise's answer", "", {"jq": str(shims / "jq")}, 1),
            ("a full run", "", {}, 0),
        ]
        for name, first, answers, code in cases:
            path = f"{first}{os.pathsep}{base}" if first else base
            with self.subTest(name):
                self.reset()
                self.answers.write_text(json.dumps(answers))
                marker.unlink(missing_ok=True)
                result = self.finish(self.start("101", PATH=path))
                self.assertEqual(code, result.returncode, result.stdout + result.stderr)
                self.assertEqual(bool(code), "no jq outside a shims directory" in result.stderr, result.stderr)
                self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")

    def test_ci_rerun_refuses_a_shim_or_a_missing_tool_by_what_the_file_is(self):
        # Audit on e7720d8b: the shims test read the directory's spelling (ShImS passed on case-insensitive APFS and
        # ran a cwd-sensitive mise shim), and a missing or non-executable answer was skipped by PATH lookup, so the
        # script silently ran /usr/bin's tool instead.
        marker = self.t / "planted.log"
        mark = f'#!/bin/sh\necho "$0" >> "{marker}"\nexec "{self.real["jq"]}" "$@"\n'  # works, and leaves a mark
        mixed, lower = self.t / "ShImS/jq", self.t / "lower/shims/jq"
        for shimmed in (mixed, lower):
            shimmed.parent.mkdir(parents=True)
            shimmed.write_text(mark)
            shimmed.chmod(0o755)
        (self.t / "links").mkdir()
        (self.t / "links/jq").symlink_to(self.t / "bin/mise")  # what `mise reshim` makes, here outside any shims dir
        (self.t / "links/dangling").symlink_to(self.t / "nowhere/jq")
        (self.t / "plain").mkdir()
        (self.t / "plain/jq").write_text(mark)  # not executable
        shim, missing = "no jq outside a shims directory", "jq is not an executable file"
        cases = [
            ("a shims directory in mixed case", mixed, shim),
            ("a link to the mise binary", self.t / "links/jq", shim),
            ("a missing file", self.t / "nowhere/jq", missing),
            ("a dangling link", self.t / "links/dangling", missing),
            ("a file that is not executable", self.t / "plain/jq", missing),
            ("a directory", self.t / "plain", missing),
        ]
        alias = self.t / "lower/ShImS/jq"
        if alias.exists():  # a case-insensitive file system: the lower-case directory under another spelling
            cases.append(("a lower-case shims directory spelled ShImS", alias, shim))
        for name, answer, message in cases:
            with self.subTest(name):
                self.reset()
                self.answer(jq=str(answer))
                marker.unlink(missing_ok=True)
                result = self.finish(self.start("101"))
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertEqual([], self.entries())
                self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")

    def test_ci_rerun_refuses_a_link_to_a_mise_binary_when_mise_itself_is_not_found(self):
        # Audit on 7f1776fc: with no mise on PATH the inode check had nothing to compare against, so a link to a mise
        # binary outside any shims directory passed, and mise started as `jq` is a cwd-sensitive shim.
        marker, vendor, decoy, gh_only = self.t / "planted.log", self.t / "vendor", self.t / "decoy", self.t / "gh-only"
        for directory in (vendor, decoy, gh_only):
            directory.mkdir()
        (gh_only / "gh").symlink_to(self.t / "bin/gh")
        path = os.pathsep.join(map(str, (decoy, gh_only, self.tools, "/usr/bin", "/bin")))
        self.assertIsNone(shutil.which("mise", path=path))
        for name in ("mise", "MiSe"):
            with self.subTest(name):
                binary = vendor / name
                binary.write_text(f'#!/bin/sh\necho "$0" >> "{marker}"\nexec "{self.real["jq"]}" "$@"\n')
                binary.chmod(0o755)
                (decoy / "jq").unlink(missing_ok=True)
                (decoy / "jq").symlink_to(binary)
                self.reset()
                marker.unlink(missing_ok=True)
                result = self.finish(self.start("101", PATH=path))
                binary.unlink()
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("no jq outside a shims directory", result.stderr)
                self.assertEqual([], self.entries())
                self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")

    def test_ci_rerun_runs_only_the_file_it_checked_when_a_path_holds_a_newline(self):
        # Audit on 7f1776fc: command substitution strips trailing newlines, so `<dir>\n/jq` was checked as `<dir>/jq`
        # (and a link to `jq\n` as `jq`) while the answer itself, another file, was linked and ran.
        marker = self.t / "planted.log"
        planted = f'#!/bin/sh\necho "$0" >> "{marker}"\nexec "{self.real["jq"]}" "$@"\n'
        checked = f'#!/bin/sh\nexec "{self.real["jq"]}" "$@"\n'
        for file, text in (
            (self.t / "tools\n/jq", planted),
            (self.t / "nl/jq\n", planted),
            (self.t / "nl/jq", checked),
        ):
            file.parent.mkdir(exist_ok=True)
            file.write_text(text)
            file.chmod(0o755)
        (self.t / "nl-link").mkdir()
        (self.t / "nl-link/jq").symlink_to(self.t / "nl/jq\n")
        cases = [
            ("a directory name ending in a newline", self.t / "tools\n/jq"),
            ("a link to a file name ending in a newline", self.t / "nl-link/jq"),
        ]
        for name, answer in cases:
            with self.subTest(name):
                self.reset()
                self.answer(jq=str(answer))
                marker.unlink(missing_ok=True)
                result = self.finish(self.start("101"))
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("jq is not an executable file", result.stderr)
                self.assertEqual([], self.entries())
                self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")

    def test_ci_rerun_keeps_a_caller_tmpdir_out_of_its_pinned_path(self):
        # Audit P2 on d6521941: the private directory heads PATH, so a TMPDIR with a ':' split it into entries the
        # caller chose (a relative one, or an empty one: the cwd), and their commands ran after the pin.
        marker, checkout = self.t / "planted.log", self.t / "checkout"
        planted = self.t / "planted"
        for directory in (planted, checkout):
            directory.mkdir()
            for tool in ("dirname", "git", "jq", "gh", "awk", "grep", "date", "mkdir"):  # each leaves a mark
                (directory / tool).write_text(f'#!/bin/sh\necho "{directory.name} {tool}" >> "{marker}"\nexit 1\n')
                (directory / tool).chmod(0o755)
        Path(f"{planted}:").mkdir()  # mktemp creates only the last component, so the split parent must exist
        (checkout / ":x").mkdir()
        for name, tmpdir in (("a named directory", f"{planted}:"), ("the cwd", ":x")):
            with self.subTest(name):
                self.reset()
                marker.unlink(missing_ok=True)
                result = self.finish(self.start("101", cwd=checkout, TMPDIR=tmpdir))
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
                self.assertEqual(1, len(self.reruns()))

    def test_ci_rerun_removes_its_private_directory_when_signalled(self):
        # Audit P3 on d6521941: an EXIT-only trap is skipped when the shell dies of a signal.
        tmp = self.t / "tmp"
        tmp.mkdir()
        for signum, code in ((signal.SIGHUP, 129), (signal.SIGINT, 130), (signal.SIGTERM, 143)):
            with self.subTest(signal=signum.name):
                self.reset()
                process = self.start("101", TMPDIR=str(tmp), GH_LOG_DELAY="1")
                deadline = time.monotonic() + 60
                while "--job" not in self.log.read_text():  # inside the first log read, after the pin
                    self.assertLess(time.monotonic(), deadline, "the script never reached its log reads")
                    time.sleep(0.05)
                self.assertEqual(1, len(list(tmp.glob("ci-rerun-bin.*"))))
                process.send_signal(signum)
                result = self.finish(process)
                self.assertEqual(code, result.returncode, result.stdout + result.stderr)
                self.assertEqual([], list(tmp.glob("ci-rerun-bin.*")))
                self.assertEqual([], self.reruns())

    def test_ci_rerun_refuses_a_superseded_pull_request_head(self):
        # a01 audit P2: a rerun of a superseded head's run re-enters pr-<N> and would cancel the newest head's run.
        for name, prs, heads, code in (
            ("current", [9], [HEAD], 0),
            ("superseded", [9], [NEWER], 3),
            ("advances during the log reads", [9], [HEAD, NEWER], 3),
            ("no pull request (a fork's run)", [], [HEAD], 1),
            ("two pull requests", [9, 12], [HEAD], 1),
            ("unreadable head", [12], [HEAD], 1),
        ):
            with self.subTest(case=name):
                self.runs["prs"]["101"], self.runs["heads"]["9"] = prs, heads
                result, _ = self.run_script("101", fresh=True)
                self.assertEqual(code, result.returncode, result.stdout + result.stderr)
                self.assertEqual(1 if code == 0 else 0, len(self.reruns()))
                if code == 3:
                    self.assertIn("superseded: run 101", result.stdout)
                # Only a refusal by the second comparison, after the reservation, leaves the run reserved.
                self.assertEqual(name in ("current", "advances during the log reads"), self.reservation("101").is_dir())
        with self.subTest(case="a push run has no pull request to compare"):
            self.runs["101"]["event"], self.runs["prs"]["101"] = "push", []
            result, calls = self.run_script("101", fresh=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse([call for call in calls if call[0] in ("api", "pr")])
        with self.subTest(case="a run still in progress"):  # worker review P2: its jobs are not final yet
            self.runs["101"]["event"], self.runs["101"]["status"] = "pull_request", "in_progress"
            self.runs["prs"]["101"], self.runs["heads"]["9"] = [9], [HEAD]
            result, _ = self.run_script("101", fresh=True)
            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertEqual(([], False), (self.reruns(), self.reservation("101").is_dir()))

    def test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs(self):
        # a01 audit P2: `gh run rerun --failed` also reruns timed-out and cancelled jobs, so each needs a signature too.
        for conclusion in ("timed_out", "cancelled"):
            unmatched = job(7, "test (ubuntu-24.04, server)", conclusion)
            for name, jobs, code in (
                ("mixed", [job(1, "public-bootstrap (ubuntu-24.04, client)"), unmatched], 3),
                ("alone", [unmatched], 3),
                ("matched", [job(8, "public-bootstrap (ubuntu-24.04, server)", conclusion)], 0),
            ):
                with self.subTest(conclusion=conclusion, case=name):
                    self.runs["101"]["jobs"], self.runs["logs"]["8"] = jobs, SNAP
                    result, calls = self.run_script("101", fresh=True)
                    self.assertEqual(code, result.returncode, result.stdout + result.stderr)
                    if code == 3:
                        self.assertIn("real failure: test (ubuntu-24.04, server)", result.stdout)
                        self.assertEqual(
                            ([], False, False), (self.reruns(), self.ledger.exists(), self.reservation("101").is_dir())
                        )
                    else:
                        self.assertEqual("snap-timeout", self.ledger.read_text().rstrip("\n").split("\t")[-1])
                        self.assertIn(["run", "view", "101", "--job", "8", "--log"], calls)
        with self.subTest(case="a missing log matches no signature, however broad"):
            (self.repo / ".github/flakes.yaml").write_text("- {id: any, job: '.*', log_regex: '^', note: fixture}\n")
            self.runs["101"]["jobs"] = [job(9, "test (ubuntu-24.04, server)", "cancelled")]
            result, _ = self.run_script("101", fresh=True)
            self.assertEqual(3, result.returncode, result.stdout + result.stderr)
            self.assertEqual([], self.reruns())

    def test_the_production_flake_registry_matches_its_samples_and_no_real_failure(self):
        # a01 audit P2: the checked-in signatures, not a fixture, against their measured samples and real failures.
        entries = registry(ROOT / ".github/flakes.yaml")
        self.assertEqual(set(SAMPLES), {entry["id"] for entry in entries})
        for entry in entries:
            job_name, line = SAMPLES[entry["id"]]
            with self.subTest(signature=entry["id"]):
                # Each expression compiles (grep -E exits 2 otherwise) and matches no empty line, which a here-string of
                # an empty log is: a missing log is no flake.
                self.assertEqual([1, 1], [egrep(entry[key], "\n") for key in ("job", "log_regex")])
                self.assertEqual([0, 0], [egrep(entry["job"], job_name), egrep(entry["log_regex"], line)])
                # The sample's own job name satisfies `job`, so only the log expression can refuse a real failure.
                for log in REAL_FAILURES:
                    self.assertEqual(1, egrep(entry["log_regex"], log), log)

    def test_a_failing_gh_exits_1_never_with_the_scripts_own_codes(self):
        # gh exits 4 when it needs authentication and 2 when cancelled: neither may read as "already rerun" or usage.
        for code in ("4", "2"):
            with self.subTest(gh_exit=code):
                result, calls = self.run_script("101", gh_exit=code)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertNotIn(["run", "rerun", "101", "--failed"], calls)
                self.assertFalse(self.ledger.exists())


if __name__ == "__main__":
    unittest.main()
