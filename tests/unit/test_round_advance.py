"""Exercise scripts/orchestrator/round-advance.sh (regime-cutover U624), the one command that runs a round's mechanics
after a worker commit, against a scratch store, a bare fake origin and a worker tree.

Each test builds a bare `origin.git`, a main checkout pushed to it (the directory the lever runs from, holding a stub
`scripts/orchestrator/audit-carry.py`), a worker tree cloned from the origin on `feat/x` with one commit the origin
does not hold, a sweep seat checkout and its `security-audit/run-<n>` state, and a store with the unit's `units.tsv`
row, an empty ledger and decisions file and two briefs. `gh`, `hcom-dispatch`, `pr-update-branch.sh` and `pr-audit.sh`
are recording stubs on PATH (each appends its argv to `STUB_CALLS`): the `gh` stub answers `repo view` with
`owner/repo` and `pr view` with the origin's branch head, as GitHub would; the update-branch stub merges `main` into
the branch on the origin when `STUB_UPDATE_MERGE` is set (GitHub's merge commit), prints the stale head when
`STUB_UPDATE_LAG` is set (the read-back path) and fails when `STUB_UPDATE_FAIL` is set; the carry stub answers from
`STUB_CARRY`. The push to `https://github.com/owner/repo` reaches the bare origin through a `url.<origin>.insteadOf`
entry in `GIT_CONFIG_COUNT`, which git reads after every config file, so the lever's `GIT_CONFIG_GLOBAL=/dev/null`
push route is the one under test. `units-row.py` and `ledger-row.py` are the real levers beside the script. Nothing
reads the live store, the real `~/.agents` or `~/.local/bin`, and nothing is pushed anywhere but the scratch origin.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_clone, git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/round-advance.sh"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
# The levers the installed layout needs beside the lever: the two row writers and the module the ledger writer imports.
BESIDE = ("units-row.py", "ledger-row.py", "ledger.py")
UNITS_HEADER = "id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote\n"
LEDGER_HEADER = "ts\tunit\tpr\thead_sha\tverdict\tverifier\tevidence\n"
DECISIONS_HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult\n"
UNIT, PR, BRANCH, SWEEP_UNIT = "U7", "42", "feat/x", "U8"
SWEEP_BRIEF = f"{SWEEP_UNIT}-security-audit-sweep-u7-head.md"
OWNER_REPO = "owner/repo"
PUSH_URL = f"https://github.com/{OWNER_REPO}"
DISPATCH_RECEIPT = "id=4242 at=2026-11-20T00:00:00Z to=rose kind=TASK"
NOT_CARRIED = f"not carried: no earlier audited head of {UNIT}"
REFUSED = "round-advance.sh: refused: "
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

STUB_PRELUDE = """#!/usr/bin/env python3
import json, os, subprocess, sys
NAME = {name!r}
with open(os.environ["STUB_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps({{"stub": NAME, "argv": sys.argv[1:]}}) + "\\n")
def origin_head():
    return subprocess.run(
        ["git", "-C", os.environ["STUB_ORIGIN"], "rev-parse", "refs/heads/" + os.environ["STUB_BRANCH"]],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
"""
STUBS = {
    "gh": """
argv = sys.argv[1:]
if argv[:2] == ["repo", "view"]:
    print(os.environ.get("STUB_OWNER_REPO", "owner/repo"))
elif argv[:2] == ["pr", "view"]:
    print(origin_head())
elif argv[:2] == ["pr", "checks"]:
    print("all checks have passed (stub)")
else:
    print("gh stub: unknown form " + " ".join(argv), file=sys.stderr)
    sys.exit(1)
""",
    "pr-update-branch.sh": """
if os.environ.get("STUB_UPDATE_FAIL"):
    print("pr-update-branch.sh: gh pr update-branch failed (stub)", file=sys.stderr)
    sys.exit(1)
old = os.environ.get("STUB_UPDATE_OLD") or origin_head()
new = old
if os.environ.get("STUB_UPDATE_MERGE") or os.environ.get("STUB_UPDATE_LAG"):
    scratch = os.path.join(os.environ["STUB_SCRATCH"], "update-branch-" + str(os.getpid()))
    run = lambda *a: subprocess.run(["git", *a], check=True, capture_output=True, text=True)
    run("clone", "-q", os.environ["STUB_ORIGIN"], scratch)
    run("-C", scratch, "checkout", "-q", os.environ["STUB_BRANCH"])
    run("-C", scratch, "merge", "--no-ff", "--no-edit", "-m", "Merge main into the branch (GitHub)", "origin/main")
    run("-C", scratch, "push", "-q", "origin", os.environ["STUB_BRANCH"])
    new = origin_head()
    if os.environ.get("STUB_UPDATE_LAG"):
        new = old  # GitHub answered the view before its merge commit was visible
print(f"updated pr={sys.argv[1]} old={old} new={new}")
""",
    "hcom-dispatch": """
if os.environ.get("STUB_DISPATCH_FAIL"):
    print("hcom-dispatch: hcom send failed (stub)", file=sys.stderr)
    sys.exit(1)
print("id=4242 at=2026-11-20T00:00:00Z to=" + sys.argv[3] + " kind=TASK")
""",
    "pr-audit.sh": """
print("/tmp/pr-audit-stub/verdict.md")
print("Verdict: correct")
""",
    "audit-carry.py": """
mode = os.environ.get("STUB_CARRY", "not")
head = sys.argv[4]
if mode == "carried":
    print(f"carried {'a' * 40} {head} {'b' * 64}")
elif mode == "not":
    print("not carried: no earlier audited head of " + sys.argv[2])
    sys.exit(1)
else:
    print("audit-carry.py: refused: the ledger cannot be read (stub)", file=sys.stderr)
    sys.exit(2)
""",
}
PATH_STUBS = ("gh", "pr-update-branch.sh", "hcom-dispatch", "pr-audit.sh")


def unit_row(unit: str, track: str = "feat", state: str = "in-flight", **cells: str) -> str:
    values = {"branch": "", "pr": "", "head_sha": "", "brief": f"briefs/{unit}-x.md", "note": "", **cells}
    return "\t".join((unit, track, state, *values.values())) + "\n"


class RoundAdvanceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.calls = self.root / "stub-calls"
        self.calls.write_text("")
        self.origin = self.root / "origin.git"
        self.checkout = self.root / "checkout"
        self.tree = self.root / "wt" / UNIT
        self.seats = self.root / "seats"
        self.store = self.root / "store"
        for name in PATH_STUBS:
            (self.bin / name).write_text(STUB_PRELUDE.format(name=name) + STUBS[name])
            (self.bin / name).chmod(0o755)
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        # The push route rewrites GitHub's URL to the bare origin through GIT_CONFIG_COUNT, read after every file.
        self.env = quiet_git_env(
            {
                "PATH": f"{self.bin}:{os.environ['PATH']}",
                "HOME": str(self.home),
                "LC_ALL": "C",
                "GIT_CONFIG_GLOBAL": str(gitconfig),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": f"url.{self.origin}.insteadOf",
                "GIT_CONFIG_VALUE_0": PUSH_URL,
                "STUB_CALLS": str(self.calls),
                "STUB_ORIGIN": str(self.origin),
                "STUB_BRANCH": BRANCH,
                "STUB_SCRATCH": str(self.root),
                "ROUND_ADVANCE_HEAD_WAIT_SECONDS": "1",
                "ROUND_ADVANCE_POLL_SECONDS": "1",
                "REGIME_SEATS_ROOT": str(self.seats),
            }
        )
        # The origin and the main checkout: README at main, then a second main commit the update-branch merges.
        git_init(self.origin, "--bare", env=self.env, cwd=self.root)
        git_init(self.checkout, env=self.env, cwd=self.root)
        (self.checkout / "README").write_text("main\n")
        carry = self.checkout / "scripts/orchestrator/audit-carry.py"
        carry.parent.mkdir(parents=True)
        carry.write_text(STUB_PRELUDE.format(name="audit-carry.py") + STUBS["audit-carry.py"])
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "main")
        self.git("remote", "add", "origin", str(self.origin))
        self.git("push", "-q", "origin", "main")
        self.main = self.git("rev-parse", "HEAD")
        # The worker tree: a clone on feat/x with commit A pushed (the pull request's head on GitHub) and commit B
        # not yet pushed (the worker's new commit).
        self.tree.parent.mkdir()
        git_clone(self.origin, self.tree, env=self.env, cwd=self.root)
        self.git("checkout", "-q", "-b", BRANCH, cwd=self.tree)
        (self.tree / "worker.txt").write_text("A\n")
        self.git("add", "worker.txt", cwd=self.tree)
        self.git("commit", "-q", "-m", "worker A", cwd=self.tree)
        self.git("push", "-q", "origin", BRANCH, cwd=self.tree)
        self.a = self.git("rev-parse", "HEAD", cwd=self.tree)
        (self.tree / "worker.txt").write_text("A\nB\n")
        self.git("commit", "-q", "-a", "-m", "worker B", cwd=self.tree)
        self.b = self.git("rev-parse", "HEAD", cwd=self.tree)
        # main moves on (the commit GitHub's update-branch merges into the branch).
        (self.checkout / "main2.txt").write_text("main2\n")
        self.git("add", "main2.txt")
        self.git("commit", "-q", "-m", "main 2")
        self.git("push", "-q", "origin", "main")
        self.main2 = self.git("rev-parse", "HEAD")
        # The sweep seat: a clone at main and two runs of its state, the larger number not the lexically last.
        self.seat = self.seats / "sweep-3"
        self.seats.mkdir()
        git_clone(self.origin, self.seat, env=self.env, cwd=self.root)
        self.seat_state = self.seats / ".state/sweep-3/security-audit"
        for run in ("run-9", "run-12"):
            (self.seat_state / run).mkdir(parents=True)
        # The store: the unit's row at A, an empty ledger and decisions file, the unit's brief and the sweep brief.
        (self.store / "briefs").mkdir(parents=True)
        (self.store / "units.tsv").write_text(
            UNITS_HEADER
            + unit_row("U1", state="landed", pr="7", head_sha="c" * 40)
            + unit_row(UNIT, branch=BRANCH, pr=PR, head_sha=self.a, note="the unit")
        )
        (self.store / "ledger.tsv").write_text(LEDGER_HEADER)
        (self.store / "decisions.tsv").write_text(DECISIONS_HEADER)
        (self.store / "briefs" / f"{UNIT}-x.md").write_text("# U7\n")
        self.sweep_brief = self.store / "briefs" / SWEEP_BRIEF
        self.sweep_brief.write_text("# U8 sweep\n")
        self.before = self.snapshot()

    # -- helpers -----------------------------------------------------------------------------------------------------

    def git(self, *args: str, cwd: Path | None = None) -> str:
        run = subprocess.run(
            ["git", *args], cwd=cwd or self.checkout, env=self.env, capture_output=True, text=True, check=False
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        return run.stdout.strip()

    def run_lever(self, *args: str, lever: Path = LEVER, cwd: Path | None = None, **env: str | None):
        merged = {key: value for key, value in {**self.env, **env}.items() if value is not None}
        return subprocess.run(
            [str(lever), *args],
            cwd=cwd or self.checkout,
            env=merged,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def sweep_args(self) -> list[str]:
        return ["--sweep-brief", str(self.sweep_brief), "--sweep-seat", "sweep-3", "--sweep-to", "rose"]

    def advance(self, *extra: str, **env: str | None):
        return self.run_lever(str(self.store), UNIT, PR, "--tree", str(self.tree), *extra, **env)

    def stub_calls(self) -> list[tuple[str, list[str]]]:
        return [
            (record["stub"], record["argv"])
            for record in (json.loads(line) for line in self.calls.read_text().splitlines() if line)
        ]

    def calls_of(self, stub: str) -> list[list[str]]:
        return [argv for name, argv in self.stub_calls() if name == stub]

    def origin_head(self) -> str:
        return self.git("rev-parse", f"refs/heads/{BRANCH}", cwd=self.origin)

    def receipts(self, run) -> list[str]:
        lines = run.stdout.splitlines()
        for line in lines:
            self.assertTrue(line.startswith("round-advance: "), line)
        return lines

    def steps(self, run) -> list[str]:
        return [line.split(" ", 2)[1] for line in self.receipts(run)]

    def rows(self, name: str) -> list[list[str]]:
        return [line.split("\t") for line in (self.store / name).read_text().splitlines()[1:]]

    def snapshot(self) -> dict[str, str]:
        """The digests of everything a refused or stopped run must leave as it was."""
        files = {
            name: hashlib.sha256((self.store / name).read_bytes()).hexdigest()
            for name in ("units.tsv", "ledger.tsv", "decisions.tsv")
        }
        files["origin"] = self.origin_head()
        files["tree"] = self.git("rev-parse", "HEAD", cwd=self.tree)
        files["seat"] = self.git("rev-parse", "HEAD", cwd=self.seat)
        files["audits"] = str((self.store / "audits").exists())
        return files

    def wait_for(self, predicate, what: str, seconds: float = 10.0) -> None:
        """The background stubs the lever starts finish on their own; the test waits for their trace, bounded."""
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.05)
        self.fail(f"{what} did not appear within {seconds} seconds")

    def move_origin_branch(self, text: str = "A\nB\n", merge_main: bool = True) -> str:
        """GitHub moved the branch while the worker committed: a merge of main (or a plain commit changing
        worker.txt to TEXT) pushed to the origin's feat/x on top of A. Returns the new origin head."""
        scratch = self.root / "moved"
        git_clone(self.origin, scratch, env=self.env, cwd=self.root)
        self.git("checkout", "-q", BRANCH, cwd=scratch)
        if merge_main:
            self.git("merge", "--no-ff", "--no-edit", "-m", "Merge main into the branch", "origin/main", cwd=scratch)
        else:
            (scratch / "worker.txt").write_text(text)
            self.git("commit", "-q", "-a", "-m", "moved", cwd=scratch)
        self.git("push", "-q", "origin", BRANCH, cwd=scratch)
        return self.origin_head()

    def install_layout(self) -> Path:
        """The installed layout under the scratch HOME from the checkout's bytes: the lever, the two row writers and
        the ledger module beside it, and the deployed manifest."""
        bindir = self.home / ".local/bin/common"
        bindir.mkdir(parents=True)
        (self.home / ".agents").mkdir()
        shutil.copy2(MANIFEST, self.home / ".agents/agent-config.yaml")
        for name in ("round-advance.sh", *BESIDE):
            source = ROOT / "home/dot_local/bin/common" / (name if name == "ledger.py" else f"executable_{name}")
            shutil.copy2(source, bindir / name)
        return bindir / "round-advance.sh"

    # -- the happy path -----------------------------------------------------------------------------------------------

    def test_the_happy_path_prints_a_receipt_per_step_and_leaves_the_files(self):
        """An unmoved branch: B pushed, GitHub's merge of main read back as the head, the carry declined, the unit's
        row set, the seat positioned and the sweep TASK sent with the next run number, the audit and the CI watch
        started to files under the store, one decisions row; the seats root comes from REGIME_SEATS_ROOT."""
        run = self.advance(*self.sweep_args(), "--sweep-note", "the new ground is worker.txt", STUB_UPDATE_MERGE="1")
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        self.assertEqual("", run.stderr)
        self.assertEqual(
            ["fetch", "push", "update-branch", "carry", "units", "sweep", "audit", "ci", "decisions"], self.steps(run)
        )
        head = self.origin_head()
        self.assertNotEqual(head, self.b, "GitHub made a merge commit on top of the pushed head")
        parents = self.git("rev-list", "--parents", "-n", "1", head, cwd=self.origin).split()
        self.assertEqual(sorted(parents[1:]), sorted([self.b, self.main2]), "the merge of main into B")
        receipts = self.receipts(run)
        self.assertEqual(
            f"round-advance: fetch origin/{BRANCH} {self.a[:8]} is an ancestor of the tree head {self.b}; nothing to merge",
            receipts[0],
        )
        self.assertEqual(f"round-advance: push {self.b} to {PUSH_URL} refs/heads/{BRANCH}", receipts[1])
        self.assertEqual(f"round-advance: update-branch pr={PR} old={self.b} new={head}", receipts[2])
        self.assertEqual(f"round-advance: carry {NOT_CARRIED}; the head gets its own sweep and audit", receipts[3])
        self.assertEqual(f"round-advance: units set {UNIT} line 3 cells=head_sha", receipts[4])
        self.assertEqual(
            f"round-advance: sweep {SWEEP_UNIT} run-13 prev run-12 on sweep-3 at {head}; added {SWEEP_UNIT} line 4; {DISPATCH_RECEIPT}",
            receipts[5],
        )
        audit_out = self.store / "audits" / f"{UNIT}-{head[:8]}.txt"
        ci_out = self.store / "audits" / f"{UNIT}-{head[:8]}-ci.txt"
        self.assertRegex(
            receipts[6], rf"^round-advance: audit pid=\d+ output={re.escape(str(audit_out))}; read it with: tail -n 2 "
        )
        self.assertRegex(
            receipts[7], rf"^round-advance: ci pid=\d+ output={re.escape(str(ci_out))}; read it with: cat "
        )
        self.assertRegex(
            receipts[8],
            rf"^round-advance: decisions appended \d{{4}}-\d{{2}}-\d{{2}}T\d{{2}}:\d{{2}}:\d{{2}}Z round {UNIT} {SWEEP_UNIT} to {re.escape(str(self.store))}/decisions.tsv$",
        )
        # the tree was not merged into (the branch had not moved), and the head is local in the checkout
        self.assertEqual(self.b, self.git("rev-parse", "HEAD", cwd=self.tree))
        self.assertEqual("commit", self.git("cat-file", "-t", head))
        # the seat is at the head and clean
        self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=self.seat))
        self.assertEqual("", self.git("status", "--porcelain", cwd=self.seat))
        # the rows
        units = self.rows("units.tsv")
        self.assertEqual([UNIT, "feat", "in-flight", BRANCH, PR, head, f"briefs/{UNIT}-x.md", "the unit"], units[1])
        self.assertEqual(
            [
                SWEEP_UNIT,
                "sweep",
                "in-flight",
                "",
                "",
                head,
                f"briefs/{SWEEP_BRIEF}",
                f"the security-audit sweep of {UNIT} head {head} (PR {PR}) on sweep-3 (run-13, prev run-12), required by pr-merge.sh; dispatched by round-advance.sh",
            ],
            units[2],
        )
        self.assertEqual([], self.rows("ledger.tsv"), "not carried: no ledger row")
        decisions = self.rows("decisions.tsv")
        self.assertEqual(1, len(decisions))
        ts, phase, decision, why, evidence, result = decisions[0]
        self.assertRegex(ts, TS)
        self.assertEqual("round", phase)
        self.assertIn(
            f"{UNIT} round advanced by round-advance.sh: PR {PR} head {head} (pushed {self.b}; update-branch old={self.b} new={head}; {NOT_CARRIED}); sweep {SWEEP_UNIT} run-13 (prev run-12) on sweep-3 to rose, receipt {DISPATCH_RECEIPT}; audit pid ",
            decision,
        )
        self.assertRegex(decision, r"audit pid \d+ -> .*; CI watch pid \d+ -> ")
        self.assertIn("standing orders 59 and 60", why)
        self.assertEqual(str(audit_out), evidence)
        self.assertEqual(f"{UNIT} {SWEEP_UNIT}", result)
        # the stubs saw the documented forms
        self.assertEqual(
            [["repo", "view", "--json", "owner,name", "--jq", '.owner.login + "/" + .name']],
            [argv for argv in self.calls_of("gh") if argv[:2] == ["repo", "view"]],
        )
        self.assertEqual([[PR]], self.calls_of("pr-update-branch.sh"))
        self.assertEqual(
            [[str(self.store), UNIT, PR, head, "--repo", str(self.checkout), "--base", "origin/main"]],
            self.calls_of("audit-carry.py"),
        )
        self.assertEqual(
            [
                [
                    "regime",
                    "coordinator",
                    "rose",
                    f"TASK v1 task_id={SWEEP_UNIT} brief={self.sweep_brief} head={head} pr={PR} branch={BRANCH} unit={UNIT} run=run-13 prev=run-12 seat=sweep-3 (read the brief whole; the seat checkout is positioned at the head; the new ground is worker.txt)",
                ]
            ],
            self.calls_of("hcom-dispatch"),
        )
        self.wait_for(lambda: audit_out.exists() and "Verdict: correct" in audit_out.read_text(), "the audit output")
        self.assertEqual(
            [[PR, "--records", str(self.store), "--cyber-program", "daybreak_blue"]], self.calls_of("pr-audit.sh")
        )
        self.wait_for(lambda: ci_out.exists() and "stub" in ci_out.read_text(), "the CI watch output")
        self.assertIn(
            ["pr", "checks", PR, "--repo", OWNER_REPO, "--watch", "--interval", "60", "--fail-fast"],
            self.calls_of("gh"),
        )

    def test_a_moved_github_branch_is_merged_into_the_tree_before_the_push(self):
        """GitHub's branch moved (a merge of main from an earlier round) while the worker committed B on A: the lever
        merges FETCH_HEAD into the tree with --no-ff and pushes the merge, a fast-forward on GitHub; with no second
        update-branch merge the head is read back unchanged and the pushed head is the round's head."""
        moved = self.move_origin_branch()
        run = self.advance("--no-sweep", "--no-audit", "--no-ci")
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        new_tree_head = self.git("rev-parse", "HEAD", cwd=self.tree)
        self.assertNotIn(new_tree_head, (self.b, moved))
        parents = self.git("rev-list", "--parents", "-n", "1", new_tree_head, cwd=self.tree).split()
        self.assertEqual([self.b, moved], parents[1:], "a --no-ff merge of GitHub's branch into B")
        self.assertEqual(new_tree_head, self.origin_head())
        receipts = self.receipts(run)
        self.assertEqual(
            f"round-advance: fetch origin/{BRANCH} {moved[:8]} merged into the tree, new head {new_tree_head}",
            receipts[0],
        )
        self.assertEqual(f"round-advance: push {new_tree_head} to {PUSH_URL} refs/heads/{BRANCH}", receipts[1])
        self.assertEqual(
            f"round-advance: update-branch pr={PR} old={new_tree_head} new={new_tree_head} (unchanged after 1s: the branch was already up to date, the pushed head is the round's head)",
            receipts[2],
        )
        self.assertEqual(["fetch", "push", "update-branch", "carry", "units", "decisions"], self.steps(run))
        self.assertEqual(new_tree_head, self.rows("units.tsv")[1][5])
        decision = self.rows("decisions.tsv")[0][2]
        self.assertIn("; no sweep; no audit; no CI watch", decision)
        self.assertFalse((self.store / "audits").exists(), "nothing started, no directory made")
        self.assertEqual([], self.calls_of("hcom-dispatch") + self.calls_of("pr-audit.sh"))
        self.assertEqual([], [argv for argv in self.calls_of("gh") if argv[:2] == ["pr", "checks"]])
        # the sweep seat was not touched
        self.assertEqual(self.before["seat"], self.git("rev-parse", "HEAD", cwd=self.seat))

    def test_a_lagging_head_is_read_back_until_it_changes(self):
        """GitHub answers the view before its merge commit shows: the receipt names the stale head as new, and the
        lever reads the head again until it changes."""
        run = self.advance("--no-sweep", "--no-audit", "--no-ci", STUB_UPDATE_LAG="1")
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        head = self.origin_head()
        self.assertNotEqual(head, self.b)
        self.assertEqual(f"round-advance: update-branch pr={PR} old={self.b} new={head}", self.receipts(run)[2])
        self.assertEqual(head, self.rows("units.tsv")[1][5])
        self.assertEqual("commit", self.git("cat-file", "-t", head), "the read-back head is fetched into the checkout")

    def test_a_carried_head_is_recorded_and_skips_the_sweep_and_the_audit(self):
        """audit-carry.py's `carried` line is recorded through ledger-row.py at once, and the sweep and the audit are
        skipped (U620: a carried head needs neither); the CI watch still runs and the decisions row says so."""
        run = self.advance(*self.sweep_args(), STUB_UPDATE_MERGE="1", STUB_CARRY="carried")
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        head = self.origin_head()
        self.assertEqual(["fetch", "push", "update-branch", "carry", "units", "ci", "decisions"], self.steps(run))
        line = f"carried {'a' * 40} {head} {'b' * 64}"
        ledger = self.rows("ledger.tsv")
        self.assertEqual(1, len(ledger))
        ts, unit, pr, head_sha, verdict, verifier, evidence = ledger[0]
        self.assertEqual(
            f"round-advance: carry {line}; appended {ts} line 2; the sweep and the audit are skipped",
            self.receipts(run)[3],
        )
        self.assertRegex(ts, TS)
        self.assertEqual([UNIT, PR, head, "carried", line], [unit, pr, head_sha, verdict, evidence])
        self.assertEqual(
            f"audit-carry.py (GitHub merge of main into the branch by pr-update-branch.sh through round-advance.sh; the diff against main is the audited head {'a' * 8})",
            verifier,
        )
        self.assertEqual(2, len(self.rows("units.tsv")), "no sweep row")
        self.assertEqual([], self.calls_of("hcom-dispatch") + self.calls_of("pr-audit.sh"))
        self.assertEqual(
            self.before["seat"], self.git("rev-parse", "HEAD", cwd=self.seat), "the seat was not positioned"
        )
        decision = self.rows("decisions.tsv")[0][2]
        self.assertIn(f"carried from {'a' * 8} (ledger appended", decision)
        self.assertIn("; no sweep (carried head); no audit (carried head); CI watch pid ", decision)
        self.assertFalse((self.store / "audits" / f"{UNIT}-{head[:8]}.txt").exists())

    # -- the stops -----------------------------------------------------------------------------------------------------

    def test_a_conflict_stops_at_fetch_with_nothing_pushed(self):
        """GitHub's branch and the tree changed the same line: the merge conflicts, one stderr line names the file and
        the step, the tree is left in the merge for the coordinator, and nothing else ran: no push, no stub call, no
        row."""
        moved = self.move_origin_branch(text="A\nconflict\n", merge_main=False)
        run = self.advance(*self.sweep_args())
        self.assertEqual(run.returncode, 1, run.stderr + run.stdout)
        self.assertEqual("", run.stdout)
        self.assertEqual(
            f"round-advance.sh: fetch failed: the merge of origin/{BRANCH} {moved[:8]} into {self.tree} conflicts in: worker.txt; the tree is left in that merge for the coordinator to resolve (git -C {self.tree} merge --abort undoes it); nothing was pushed; done before it: nothing\n",
            run.stderr,
        )
        self.assertTrue((self.tree / ".git/MERGE_HEAD").exists(), "the merge is left for the coordinator")
        self.assertEqual(moved, self.origin_head())
        self.assertEqual([], self.stub_calls())
        after = self.snapshot()
        after["origin"] = self.before["origin"]  # the test moved it; everything else is as it was
        self.assertEqual(self.before, after)

    def test_a_failed_push_stops_with_nothing_else_done(self):
        """A push the remote refuses stops the round after the fetch: no update-branch, no row, no TASK."""
        run = self.advance(*self.sweep_args(), GIT_CONFIG_KEY_0=f"url.{self.root}/nowhere.git.insteadOf")
        self.assertEqual(run.returncode, 1, run.stderr + run.stdout)
        self.assertEqual(
            [
                f"round-advance: fetch origin/{BRANCH} {self.a[:8]} is an ancestor of the tree head {self.b}; nothing to merge"
            ],
            self.receipts(run),
        )
        self.assertEqual(
            f"round-advance.sh: push failed: git push {PUSH_URL} FETCH_HEAD:refs/heads/{BRANCH} failed (the head {self.b} is fetched into {self.checkout} as FETCH_HEAD); done before it: fetch\n",
            run.stderr,
        )
        self.assertEqual(self.a, self.origin_head(), "nothing was pushed")
        self.assertEqual(["gh"], [name for name, _ in self.stub_calls()], "only the repository read ran")
        self.assertEqual(self.before, self.snapshot())

    def test_a_failed_update_branch_stops_after_the_push(self):
        run = self.advance(*self.sweep_args(), STUB_UPDATE_FAIL="1")
        self.assertEqual(run.returncode, 1, run.stderr + run.stdout)
        self.assertEqual(["fetch", "push"], self.steps(run))
        self.assertEqual(
            f"round-advance.sh: update-branch failed: pr-update-branch.sh {PR} failed; the head {self.b} is pushed; done before it: fetch; push\n",
            run.stderr.splitlines(keepends=True)[-1],
        )
        self.assertEqual(self.b, self.origin_head())
        self.assertEqual(self.a, self.rows("units.tsv")[1][5], "the row is not set")
        self.assertEqual(
            [], self.calls_of("audit-carry.py") + self.calls_of("hcom-dispatch") + self.calls_of("pr-audit.sh")
        )

    def test_a_carry_lever_failure_stops_before_any_row(self):
        run = self.advance(*self.sweep_args(), STUB_CARRY="fail")
        self.assertEqual(run.returncode, 1, run.stderr + run.stdout)
        self.assertEqual(["fetch", "push", "update-branch"], self.steps(run))
        self.assertIn(f"round-advance.sh: carry failed: audit-carry.py exited 2 for {self.b}", run.stderr)
        self.assertTrue(run.stderr.endswith("; done before it: fetch; push; update-branch\n"), run.stderr)
        self.assertEqual([], self.rows("ledger.tsv"))
        self.assertEqual(self.a, self.rows("units.tsv")[1][5])

    def test_a_failed_dispatch_names_the_added_row_and_starts_no_audit(self):
        """The sweep row is added before the TASK: a failed dispatch names the row so the coordinator sends the TASK
        by hand, and the audit and the decisions row wait for the next run."""
        run = self.advance(*self.sweep_args(), STUB_UPDATE_MERGE="1", STUB_DISPATCH_FAIL="1")
        self.assertEqual(run.returncode, 1, run.stderr + run.stdout)
        head = self.origin_head()
        self.assertEqual(["fetch", "push", "update-branch", "carry", "units"], self.steps(run))
        self.assertEqual(
            f"round-advance.sh: sweep failed: hcom-dispatch to rose failed; the seat is positioned at {head} and the units row for {SWEEP_UNIT} is added (added {SWEEP_UNIT} line 4), the TASK was not sent; done before it: fetch; push; update-branch; carry; units\n",
            run.stderr.splitlines(keepends=True)[-1],
        )
        self.assertEqual(SWEEP_UNIT, self.rows("units.tsv")[2][0])
        self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=self.seat))
        self.assertEqual([], self.calls_of("pr-audit.sh"))
        self.assertEqual([], self.rows("decisions.tsv"))

    def test_a_seat_state_without_a_run_stops_the_sweep_after_positioning(self):
        for run_dir in ("run-9", "run-12"):
            (self.seat_state / run_dir).rmdir()
        (self.seat_state / "notes").mkdir()
        run = self.advance(*self.sweep_args())
        self.assertEqual(run.returncode, 1, run.stderr + run.stdout)
        self.assertIn(
            f"round-advance.sh: sweep failed: no run-<n> entry under {self.seat_state}; the seat's prev run is unknown, no row and no TASK (the seat is positioned at {self.b})",
            run.stderr,
        )
        self.assertEqual(2, len(self.rows("units.tsv")))
        self.assertEqual([], self.calls_of("hcom-dispatch"))

    # -- the refusals -----------------------------------------------------------------------------------------------

    def test_refusals_name_the_reason_and_write_nothing(self):
        """Each refusal is exit 2 with one stderr line in the levers' form, nothing on stdout, no stub call and no
        change to the store, the origin, the tree or the seat."""
        store = str(self.store)
        tree = ["--tree", str(self.tree)]
        sweep = self.sweep_args()
        other_dir = self.root / "elsewhere"
        other_dir.mkdir()
        shutil.copy2(self.sweep_brief, other_dir / SWEEP_BRIEF)
        (self.store / "briefs" / "sweep.md").write_text("x\n")
        empty_store = self.root / "empty-store"
        empty_store.mkdir()
        cases = [
            ("a tab in an argument", [store, UNIT, PR, *tree, "--no-sweep", "--sweep-note", "a\tb"], "holds a tab, a newline or a carriage return"),
            ("a missing tree", [store, UNIT, PR, "--tree", str(self.root / "no-such-tree"), "--no-sweep"], f"the worker tree {self.root}/no-such-tree is not a directory"),
            ("a tree that is no work tree", [store, UNIT, PR, "--tree", str(other_dir), "--no-sweep"], "is not a git work tree"),
            ("a store without units.tsv", [str(empty_store), UNIT, PR, *tree, "--no-sweep"], f"{empty_store}/units.tsv is not a regular file"),
            ("a store that is no directory", [str(self.store / "units.tsv"), UNIT, PR, *tree, "--no-sweep"], "is not a directory that can be entered"),
            ("no store", [UNIT, PR, *tree, "--no-sweep"], "a store, a unit and a pull request are needed, 2 given"),
            ("a unit outside the shape", [store, "U7x1", PR, *tree, "--no-sweep"], "the unit U7x1 is not U<n> or U<n><letter>"),
            ("a pull request that is no number", [store, UNIT, "0", *tree, "--no-sweep"], "the pull request 0 is not a decimal number"),
            ("no --tree", [store, UNIT, PR, "--no-sweep"], "--tree <worker tree> is needed"),
            ("an unknown option", [store, UNIT, PR, *tree, "--no-sweep", "--rebase"], "unknown option --rebase"),
            ("an option twice", [store, UNIT, PR, *tree, *tree, "--no-sweep"], "--tree is given twice"),
            ("an option without its value", [store, UNIT, PR, *tree, "--no-sweep", "--sweep-note"], "--sweep-note needs a value"),
            ("--sweep-brief with --no-sweep", [store, UNIT, PR, *tree, *sweep, "--no-sweep"], "--sweep-brief and --no-sweep are two answers to one question"),
            ("neither --sweep-brief nor --no-sweep", [store, UNIT, PR, *tree], "the round's sweep is an explicit choice"),
            ("--sweep-brief without --sweep-to", [store, UNIT, PR, *tree, *sweep[:4]], "--sweep-brief needs --sweep-to <hcom name>"),
            ("--sweep-brief without --sweep-seat", [store, UNIT, PR, *tree, *sweep[:2], *sweep[4:]], "--sweep-brief needs --sweep-seat <seat>"),
            ("an hcom name outside the grammar", [store, UNIT, PR, *tree, *sweep[:4], "--sweep-to", "Rose"], "the identifier Rose is outside hcom-dispatch's"),
            ("a team outside the grammar", [store, UNIT, PR, *tree, "--no-sweep", "--team", "-regime"], "the identifier -regime is outside hcom-dispatch's"),
            ("a backtick in the note", [store, UNIT, PR, *tree, *sweep, "--sweep-note", "run `rm`"], "the sweep note holds a backtick or a dollar-parenthesis"),
            ("a dollar-parenthesis in the note", [store, UNIT, PR, *tree, *sweep, "--sweep-note", "$(date)"], "the sweep note holds a backtick or a dollar-parenthesis"),
            ("a brief outside the store's briefs", [store, UNIT, PR, *tree, "--sweep-brief", str(other_dir / SWEEP_BRIEF), *sweep[2:]], f"is not directly under {self.store}/briefs"),
            ("a brief named outside the shape", [store, UNIT, PR, *tree, "--sweep-brief", str(self.store / "briefs/sweep.md"), *sweep[2:]], "the sweep brief's name sweep.md is not U<n>-<slug>.md"),
            ("a missing brief", [store, UNIT, PR, *tree, "--sweep-brief", str(self.store / "briefs/U9-x.md"), *sweep[2:]], "is not a regular file"),
            ("a seat without a checkout", [store, UNIT, PR, *tree, *sweep[:2], "--sweep-seat", "sweep-9", *sweep[4:]], f"the sweep seat checkout {self.seats}/sweep-9 is not a directory"),
            ("a seats root that is missing", [store, UNIT, PR, *tree, *sweep, "--seats-root", str(self.root / "no-seats")], "is not a directory; give --seats-root"),
        ]  # fmt: skip
        for label, argv, message in cases:
            with self.subTest(case=label):
                run = self.run_lever(*argv)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertEqual("", run.stdout)
                self.assertTrue(run.stderr.startswith(REFUSED), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual(1, run.stderr.count("\n"), run.stderr)
        with self.subTest(case="a seat state directory that is missing"):
            shutil.rmtree(self.seat_state)
            run = self.advance(*self.sweep_args())
            self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
            self.assertIn(f"the sweep seat's state directory {self.seat_state} is missing", run.stderr)
            self.seat_state.mkdir()
        with self.subTest(case="a wait outside its bounds"):
            run = self.advance("--no-sweep", ROUND_ADVANCE_HEAD_WAIT_SECONDS="0")
            self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
            self.assertIn("are 1 to 86400 seconds, not 0", run.stderr)
        with self.subTest(case="outside a git work tree"):
            run = self.run_lever(store, UNIT, PR, *tree, "--no-sweep", cwd=other_dir)
            self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
            self.assertIn("the current directory is not inside a git work tree", run.stderr)
        with self.subTest(case="a tool missing from PATH"):
            thin = self.root / "thin-bin"
            thin.mkdir()
            for name in ("gh", "hcom-dispatch", "pr-audit.sh"):
                shutil.copy2(self.bin / name, thin / name)
            tools = ":".join(
                sorted({str(Path(shutil.which(tool)).parent) for tool in ("git", "python3", "sed", "tr", "date")})
            )
            run = self.advance("--no-sweep", PATH=f"{thin}:{tools}")
            self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
            self.assertIn("no pr-update-branch.sh on PATH", run.stderr)
        self.assertEqual([], self.stub_calls())
        self.assertEqual(self.before, self.snapshot())

    def test_a_rewritten_copy_refuses_before_reading_an_argument(self):
        copy_dir = self.root / "copy/scripts/orchestrator"
        copy_dir.mkdir(parents=True)
        copy = copy_dir / "round-advance.sh"
        copy.write_text(LEVER.read_text() + "echo rewritten\n")
        copy.chmod(0o755)
        (self.root / "copy/home/dot_agents").mkdir(parents=True)
        shutil.copy2(MANIFEST, self.root / "copy/home/dot_agents/agent-config.yaml")
        run = self.run_lever(str(self.store), UNIT, PR, "--tree", str(self.tree), "--no-sweep", lever=copy)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused: sha256", run.stderr)
        self.assertNotIn("rewritten", run.stdout)
        self.assertEqual(self.before, self.snapshot())

    # -- the installed layout ----------------------------------------------------------------------------------------

    def test_the_installed_copy_runs_the_round_against_the_deployed_manifest(self):
        """The copy under `~/.local/bin/common` passes its self-check against `~/.agents/agent-config.yaml`, finds
        the row writers beside it (each self-checked against the same manifest) and runs the round from the
        checkout."""
        installed = self.install_layout()
        run = self.run_lever(
            str(self.store), UNIT, PR, "--tree", str(self.tree), "--no-sweep", "--no-audit", "--no-ci", lever=installed
        )
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        self.assertEqual(["fetch", "push", "update-branch", "carry", "units", "decisions"], self.steps(run))
        self.assertEqual(self.b, self.origin_head())
        self.assertEqual(self.b, self.rows("units.tsv")[1][5])
        self.assertEqual("round", self.rows("decisions.tsv")[0][1])

    def test_the_deployed_twin_equals_the_source_and_hashes_to_its_pin(self):
        twin = ROOT / "home/dot_local/bin/common/executable_round-advance.sh"
        self.assertEqual(LEVER.read_bytes(), twin.read_bytes())
        self.assertTrue(os.access(twin, os.X_OK))
        pins = re.findall(r"^      round-advance\.sh: ([0-9a-f]{64})$", MANIFEST.read_text(), re.MULTILINE)
        self.assertEqual([hashlib.sha256(LEVER.read_bytes()).hexdigest()], pins)


if __name__ == "__main__":
    unittest.main()
