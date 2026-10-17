"""Exercise chain-integrate.sh (plan 022 T7) against a temporary origin, main checkout and review worktree.

git is the real one: a bare origin holds `main` and `refs/pull/7/head`, the main checkout and the review worktree are
clones of it, the review worktree at the canonical `<main>/.claude/worktrees/orchestrator-review`. The repository
scripts the chain calls are stubs in the main checkout's `scripts/`: each appends `argv:`, `cwd:` and `path:` lines
(and the content of a `.tsv` or comments argument) to `<calls>/<name>.log`, prints `<calls>/<name>.out` and exits with
`<calls>/<name>.status` (0 when absent). `gh`, `uv`, `codex` and `mise` (failing, so `command -v` resolves) are stubs
first on PATH; `gh` answers from files the case writes and its `update-branch` merges `main` into the pull ref.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parents[2] / "scripts/orchestrator/chain-integrate.sh"
FINISH = CHAIN.with_name("chain-finish.sh")
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
TASK, OWNER = "dotfiles-T128-x-a01", "dotfiles-T128-x-followup-a01"
STUB = (
    "#!/usr/bin/env bash\n"
    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\npath: %s\\nreview: %s\\n" "$(pwd -P)" "$PATH" "${{ORCH_REVIEW_WORKTREE:-}}"\n'
    '  for a; do case $a in *.tsv | *-pr-comments.json) cat -- "$a" ;; esac; done; }} >> "$CALLS/{name}.log"\n'
    'echo {name} >> "$CALLS/order.log"\n'
    '[ ! -x "$CALLS/{name}-hook" ] || "$CALLS/{name}-hook"\n'
    'cat "$CALLS/{name}.out" 2> /dev/null || true\n'
    'exit "$(cat "$CALLS/{name}.status" 2> /dev/null || echo 0)"\n'
)
GH = """#!/usr/bin/env bash
{ printf "argv:"; printf " %s" "$@"; printf "\\n"; } >> "$CALLS/gh.log"
# gh colours its output when forced (a Herdr pane's CLICOLOR_FORCE=1, or GH_FORCE_TTY) unless NO_COLOR is set.
paint() { if [ -z "${NO_COLOR:-}" ] && { [ "${CLICOLOR_FORCE:-0}" != 0 ] || [ -n "${GH_FORCE_TTY:-}" ]; }; then sed $'s/.*/\\e[32m&\\e[0m/'; else cat; fi; }
jq=; prev=; for a; do [ "$prev" != --jq ] || jq=$a; prev=$a; done
case "$1 $2" in
"pr view") if [[ " $* " == *" isDraft "* ]]; then cat "$CALLS/draft" 2> /dev/null || echo false; else cat "$CALLS/head"; fi | paint ;;
"pr checks")
    [ ! -x "$CALLS/checks-hook" ] || "$CALLS/checks-hook"
    exit "$(cat "$CALLS/checks-status" 2> /dev/null || echo 0)" ;;
"pr update-branch")
    git -C "$SEED" fetch -q origin +refs/pull/7/head:refs/remotes/pr/7 main
    git -C "$SEED" checkout -q --detach pr/7
    git -C "$SEED" -c commit.gpgsign=false merge -q --no-edit origin/main
    git -C "$SEED" push -q origin HEAD:refs/pull/7/head
    git -C "$SEED" rev-parse HEAD > "$CALLS/head"
    [ ! -x "$CALLS/update-hook" ] || "$CALLS/update-hook" ;;
"pr merge")
    echo "gh pr merge" >> "$CALLS/order.log"
    exit "$(cat "$CALLS/merge-status" 2> /dev/null || echo 0)" ;;
"api user") paint < "$CALLS/login" ;;
"api "*)
    case $2 in *reviews) f=$CALLS/reviews.json ;; *) f=$CALLS/comments.json ;; esac
    if [ -n "$jq" ]; then JQ -rc "$jq" "$f"; else cat "$f"; fi | paint ;;
esac
"""
UV = """#!/usr/bin/env bash
{ printf "argv:"; printf " %s" "$@"; printf "\\n"; } >> "$CALLS/uv.log"
shift 4
[ "$1" != -c ] || exec python3 -I "$@"
exec "$@"
"""
SCRIPTS = {
    "orchestrator/sandbox-scan.sh": "sandbox-scan",
    "orchestrator/local-review.sh": "local-review",
    "orchestrator/local-advisory.sh": "local-advisory",
    "orchestrator/fill_sweep.py": "fill_sweep",
    "orchestrator/acceptance-front-matter.py": "acceptance-front-matter",
    "orchestrator/orch-audit.sh": "orch-audit",
    "pr-feedback.py": "pr-feedback",
    "orchestrator/resolve-threads.sh": "resolve-threads",
    "orchestrator/orch-gate.sh": "orch-gate",
    "orchestrator/ff-main.sh": "ff-main",
    "orchestrator/pr-cost.sh": "pr-cost",
}
SCAN_HIT = "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
STEPS = [
    "fetch",
    "base",
    "checks",
    "bot",
    "sandbox-scan",
    "local-review",
    "local-advisory",
    "pr-feedback",
    "fill-sweep",
    "receipt",
    "record",
    "audit",
]


class ChainIntegrateTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.calls, bin_dir = self.temp / "calls", self.temp / "bin"
        self.calls.mkdir()
        bin_dir.mkdir()
        (self.temp / "home").mkdir()
        origin, self.seed = self.temp / "origin.git", self.temp / "seed"
        self.git("init", "-q", "--bare", "-b", "main", str(origin), cwd=self.temp)
        self.git("clone", "-q", str(origin), str(self.seed), cwd=self.temp)
        # The stubs are tracked on main, so the main checkout's copies are HEAD's (PR #372 thread 4291474880).
        for rel, name in SCRIPTS.items():
            # The calls directory is baked in as the default, since pr-cost.sh runs under env -i.
            stub = STUB.format(name=name).replace("$CALLS", f"${{CALLS:-{self.calls}}}")
            self.executable(self.seed / "scripts" / rel, stub)
        self.git("add", "scripts", cwd=self.seed)
        self.commit(self.seed, "a.txt")
        self.git("push", "-q", "origin", "HEAD:main", cwd=self.seed)
        self.commit(self.seed, "b.txt")
        self.git("push", "-q", "origin", "HEAD:refs/pull/7/head", cwd=self.seed)
        self.head = self.git("rev-parse", "HEAD", cwd=self.seed)
        self.git("checkout", "-q", "main", cwd=self.seed)
        self.main = self.temp / "main"
        self.git("clone", "-q", str(origin), str(self.main), cwd=self.temp)
        self.review = self.main / ".claude/worktrees/orchestrator-review"
        self.git("clone", "-q", str(origin), str(self.review), cwd=self.temp)
        self.v = self.main / ".orchestration/validation"
        self.v.mkdir(parents=True)
        rows = "# Acceptance\n\n4280648512\tclass-a\naudit:abcdef1:2\tclass-b\nlocal:abcdef1:1\tadvisory-p2\n123456789\tshort-id\n"
        self.write(f".orchestration/acceptance/{TASK}.md", rows)
        self.write(f".orchestration/tasks/{OWNER}.md", "owner\n")
        self.executable(bin_dir / "gh", GH.replace("JQ", shutil.which("jq") or "jq"))
        self.executable(bin_dir / "uv", UV)
        self.executable(bin_dir / "codex", STUB.format(name="codex"))
        self.executable(bin_dir / "mise", "#!/bin/sh\nexit 1\n")
        # chain-finish.sh resolves jq for pr-cost.sh; macOS 14 has none in /usr/bin, so the test's own jq is linked.
        (bin_dir / "jq").symlink_to(shutil.which("jq") or "/usr/bin/jq")
        for name in ("send.sh", "agmsg-dispatch"):
            self.executable(bin_dir / name, f'#!/bin/sh\necho "{name} $*" >> "$CALLS/send.log"\n')
        bot = {"user": {"login": "chatgpt-codex-connector[bot]"}, "commit_id": self.head}
        (self.calls / "head").write_text(self.head + "\n")
        (self.calls / "reviews.json").write_text(json.dumps([bot]))
        (self.calls / "comments.json").write_text(json.dumps([{"id": 1, "body": "a"}, {"id": 2, "body": "b,\nc"}]))
        (self.calls / "login").write_text("orch\n")
        (self.calls / "orch-audit.out").write_text("audit written\nVerdict: correct\n")
        self.env = {
            **GIT_ENV,
            "CALLS": str(self.calls),
            "SEED": str(self.seed),
            "HOME": str(self.temp / "home"),
            "TMPDIR": str(self.temp),
            "PATH": f"{bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin",
            "CHAIN_POLL_SECONDS": "0",
            "CHAIN_BOT_WAIT": "0",
        }

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=cwd or self.main,
            env={**os.environ, **GIT_ENV},
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def commit(self, repo, name, text=None):
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text or f"{name}\n")
        if text:
            (repo / name).chmod(0o755)
        self.git("add", name, cwd=repo)
        self.git("commit", "-q", "-m", name, cwd=repo)

    def write(self, rel, text):
        path = self.main / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def executable(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        path.chmod(0o755)

    def chain(self, *args, code=0, env=None, review=None):
        argv = args or (TASK, "7", self.main, review or self.review, OWNER)
        result = subprocess.run(
            ["bash", str(CHAIN), *map(str, argv)],
            cwd=self.temp,
            env={**self.env, **(env or {})},
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        return result

    def calls_of(self, name):
        path = self.calls / f"{name}.log"
        return re.findall(r"^argv: ?(.*)$", path.read_text(), re.MULTILINE) if path.exists() else []

    def log(self, head=None):
        path = self.v / f"{TASK}-chain-{(head or self.head)[:7]}.log"
        return path.read_text() if path.exists() else ""

    def steps(self, text):
        return list(dict.fromkeys(re.findall(r"^\S+ (\S+) rc=\d+: ", text, re.MULTILINE)))

    def test_integrate_refuses_when_main_is_not_on_main(self):
        def refused(message, **kwargs):
            self.assertIn(message, self.chain(code=10, **kwargs).stderr)

        # Before the head is known: stderr only, no log, no stub, no pull ref fetched.
        def untouched():
            self.assertEqual([], list(self.v.glob("*.log")))
            self.assertEqual([], [p.name for p in self.calls.glob("*.log") if p.name != "gh.log"])
            self.assertNotIn("refs/remotes/pr/7", self.git("for-each-ref"))

        for bad in ("a/b", "..", ".x"):
            with self.subTest(task=bad):
                result = self.chain(bad, "7", self.main, self.review, OWNER, code=10)
                self.assertIn("invalid argument", result.stderr)
        self.assertIn("invalid argument", self.chain(TASK, "7a", self.main, self.review, OWNER, code=10).stderr)
        other = self.temp / "other"
        self.git("clone", "-q", str(self.temp / "origin.git"), str(other), cwd=self.temp)
        refused("not the canonical one", review=other)
        (self.calls / "draft").write_text("true\n")
        refused("draft PR")
        untouched()
        (self.calls / "draft").unlink()
        self.git("switch", "-q", "-c", "x")
        refused("main checkout is not on main")
        untouched()
        self.git("switch", "-q", "main")
        # A head already audited: the fetches are logged, nothing after them runs.
        (self.v / f"{TASK}-audit-{self.head[:7]}.md.last.md").write_text("Verdict: correct\n")
        refused("head already audited")
        self.assertEqual(["fetch"], self.steps(self.log()))
        self.assertEqual([], self.calls_of("sandbox-scan"))
        (self.v / f"{TASK}-audit-{self.head[:7]}.md.last.md").unlink()
        # One commit behind origin/main after the chain's own fetch.
        self.commit(self.seed, "c.txt")
        self.git("push", "-q", "origin", "HEAD:main", cwd=self.seed)
        refused("scripts/orchestrator/ff-main.sh")

    def test_integrate_refuses_a_main_checkout_script_that_is_not_heads(self):
        # PR #372 thread 4291474880: a called script modified or untracked in the main checkout never runs.
        stub = self.main / "scripts/orchestrator/local-review.sh"
        stub.write_text(stub.read_text() + "# changed\n")
        self.assertIn("scripts/ in the main checkout differs from HEAD", self.chain(code=10).stderr)
        self.git("checkout", "--", "scripts")
        self.git("rm", "-q", "--cached", "scripts/pr-feedback.py")
        self.assertIn("scripts/pr-feedback.py is not tracked in the main checkout", self.chain(code=10).stderr)
        self.assertEqual([], [p.name for p in self.calls.glob("*.log") if p.name != "gh.log"])
        self.assertEqual([], list(self.v.glob("*.log")))

    def test_integrate_runs_the_steps_in_order_and_logs_each(self):
        (self.calls / "local-review.out").write_text("- [P2] x\nlocal-review: 1 findings (f)\n")
        (self.calls / "local-review.status").write_text("3")
        out = self.chain().stdout
        log = self.log()
        self.assertEqual(STEPS, self.steps(log))
        self.assertEqual(f"chain-integrate: {TASK} {self.head} Verdict: correct", out.splitlines()[-1])
        self.assertIn("bot review: present", log)
        self.assertNotIn(str(self.temp), log)
        sweep, comments = self.v / f"{TASK}-pr-feedback.json", self.v / f"{TASK}-pr-comments.json"
        expected = {
            "sandbox-scan": [TASK],
            "local-review": [f"{TASK} {self.head} 7"],
            "local-advisory": [f"{TASK} {self.head} {OWNER}"],
            "pr-feedback": [f"7 --json {sweep}"],
            "fill_sweep": [f"{sweep} {comments} --orchestrator-login orch"],
            "acceptance-front-matter": [
                f"{TASK} {sweep} {self.review} --ledger {self.v}/{TASK}-ledger-{self.head[:7]}.tsv"
            ],
            "orch-audit": [f"{TASK} {self.review} 7"],
        }
        self.assertEqual(expected, {name: self.calls_of(name) for name in expected})
        for name in expected:
            self.assertIn(f"cwd: {self.main}\n", (self.calls / f"{name}.log").read_text())
        self.assertIn(f"review: {self.review}\n", (self.calls / "local-review.log").read_text())
        self.assertIn("pr checks 7 --required --watch", self.calls_of("gh"))
        # The ledger holds the gate's ids only; the comments are one array across pages.
        ledger = (self.calls / "acceptance-front-matter.log").read_text()
        self.assertIn("4280648512\tclass-a\naudit:abcdef1:2\tclass-b\n", ledger)
        self.assertNotIn("local:", ledger)
        self.assertNotIn("short-id", ledger)
        fill = (self.calls / "fill_sweep.log").read_text()
        self.assertEqual([{"id": 1, "body": "a"}, {"id": 2, "body": "b,\nc"}], json.loads(fill.split("\n", 4)[4]))
        self.assertFalse(comments.exists())
        self.assertEqual([], list(self.v.glob("*.tsv")))
        [record] = json.loads((self.v / f"{TASK}-crit.json").read_text())
        self.assertEqual((f"{TASK}-pr7-review-1", self.head, "7"), (record["id"], record["head"], record["pr"]))
        self.assertIn("local review 1 finding(s)", record["body"])
        receipt = (self.v / f"{TASK}-review-receipt.md").read_text()
        self.assertIn(
            f"review_surface: crit-data\nreviewer: claude-code\nreview_source: .orchestration/validation/{TASK}-crit.json\nreview_outcome: approved\nhead: {self.head}\npr: 7\n",
            receipt,
        )

    def test_integrate_restarts_after_update_branch(self):
        self.commit(self.seed, "c.txt")
        self.git("push", "-q", "origin", "HEAD:main", cwd=self.seed)
        self.git("pull", "-q", "--ff-only")
        out = self.chain().stdout
        merged = (self.calls / "head").read_text().strip()
        self.assertNotEqual(self.head, merged)
        self.assertEqual(f"chain-integrate: {TASK} {merged} Verdict: correct", out.splitlines()[-1])
        gh = self.calls_of("gh")
        self.assertEqual(1, gh.count("pr update-branch 7"))
        self.assertIn("pr view 7 --json headRefOid --jq .headRefOid", gh[gh.index("pr update-branch 7") + 1 :])
        # The first head's log ends at the update-branch; the merged head's log holds both rounds.
        self.assertEqual(1, self.log().count("+pull/7/head:refs/remotes/pr/7\n"))
        self.assertNotIn(" checks rc=", self.log())  # a head behind the base waits for no CI
        log = self.log(merged)
        self.assertEqual(2, log.count("git -C . fetch -q origin +pull/7/head:refs/remotes/pr/7\n"))
        self.assertEqual(2, log.count("git -C .claude/worktrees/orchestrator-review fetch -q origin +pull/7/head\n"))
        self.git("cat-file", "-e", f"{merged}^{{commit}}")
        self.git("cat-file", "-e", f"{merged}^{{commit}}", cwd=self.review)
        self.assertEqual(merged, self.git("rev-parse", "HEAD", cwd=self.review))

    def test_integrate_restarts_when_the_base_moves_during_the_waits(self):
        # PR #372 thread 4291474885: origin/main advances during the required-checks wait, after the first ancestry
        # test; the chain fetches it again before the local review, update-branches and restarts at the fetch.
        hook = f"""#!/bin/bash
rm -f "$CALLS/checks-hook"
cd "{self.seed}" && echo d > d.txt && git add d.txt && git -c commit.gpgsign=false commit -q -m d
git -C "{self.seed}" push -q origin HEAD:main
git -C "{self.main}" pull -q --ff-only
"""
        self.executable(self.calls / "checks-hook", hook)
        out = self.chain().stdout
        merged = (self.calls / "head").read_text().strip()
        self.assertNotEqual(self.head, merged)
        self.assertEqual(f"chain-integrate: {TASK} {merged} Verdict: correct", out.splitlines()[-1])
        self.assertEqual(1, self.calls_of("gh").count("pr update-branch 7"))
        first = re.findall(r"^\S+ (\S+) rc=\d+: ", self.log(), re.MULTILINE)
        self.assertEqual(
            ["checks", "bot", "base", "base", "base"], first[first.index("checks") : first.index("checks") + 5]
        )
        self.assertNotIn("sandbox-scan", first)
        self.assertEqual(2, self.log(merged).count(" checks rc=0: "))
        self.assertEqual([f"{TASK} {merged} 7"], self.calls_of("local-review"))
        self.git("cat-file", "-e", f"{self.git('rev-parse', 'origin/main', cwd=self.seed)}^{{commit}}", cwd=self.review)

    def test_integrate_refuses_a_stale_main_checkout_after_the_restart(self):
        # Revise round 2 (the local review of 2fe135c5, P2): origin/main moves again while the PR is updated, so
        # after the restart the main checkout's main, which local-review.sh diffs against, is behind: exit 10.
        self.commit(self.seed, "c.txt")
        self.git("push", "-q", "origin", "HEAD:main", cwd=self.seed)
        self.git("pull", "-q", "--ff-only")
        hook = f"""#!/bin/bash
rm -f "$CALLS/update-hook"
git -C "{self.seed}" checkout -q main && cd "{self.seed}" && echo e > e.txt && git add e.txt
git -C "{self.seed}" -c commit.gpgsign=false commit -q -m e && git -C "{self.seed}" push -q origin HEAD:main
"""
        self.executable(self.calls / "update-hook", hook)
        result = self.chain(code=10)
        self.assertIn("main checkout is not origin/main: run scripts/orchestrator/ff-main.sh", result.stderr)
        self.assertEqual(1, self.calls_of("gh").count("pr update-branch 7"))
        for name in ("sandbox-scan", "local-review", "orch-audit"):
            self.assertEqual([], self.calls_of(name))

    def test_integrate_restores_the_review_worktree_after_the_audit(self):
        # Revise round 2 (the local review of 2fe135c5, P1): orch-audit.sh leaves the shared review worktree at
        # origin/main; the chain puts it back at the audited head, which the gate reads next.
        hook = '#!/bin/bash\ngit -C "$ORCH_REVIEW_WORKTREE" checkout -q --detach origin/main\n'
        self.executable(self.calls / "orch-audit-hook", hook)
        out = self.chain().stdout
        self.assertEqual(f"chain-integrate: {TASK} {self.head} Verdict: correct", out.splitlines()[-1])
        self.assertEqual(self.head, self.git("rev-parse", "HEAD", cwd=self.review))
        last = [line for line in self.log().splitlines() if " rc=" in line][-1]
        self.assertTrue(
            last.endswith(
                f" audit rc=0: git -C .claude/worktrees/orchestrator-review checkout -q --detach {self.head}"
            ),
            last,
        )

    def test_integrate_refuses_an_extra_tsv_outside_the_main_checkout(self):
        # PR #372 thread 4291474891: the log names repository paths only, so an extra TSV elsewhere is refused.
        outside = self.temp / "extra.tsv"
        outside.write_text("")
        result = self.chain(TASK, "7", self.main, self.review, OWNER, outside, code=10)
        self.assertIn("extra dispositions TSV is not in the main checkout", result.stderr)
        self.assertEqual([], [p.name for p in self.calls.glob("*.log") if p.name != "gh.log"])
        self.assertEqual([], list(self.v.glob("*.log")))
        self.write(".orchestration/extra.tsv", "")
        self.chain(TASK, "7", self.main, self.review, OWNER, self.main / ".orchestration/extra.tsv")
        [fill] = self.calls_of("fill_sweep")
        self.assertIn(f" {self.main}/.orchestration/extra.tsv --orchestrator-login orch", fill)
        self.assertIn(" .orchestration/extra.tsv --orchestrator-login orch", self.log())
        self.assertNotIn(str(self.temp), self.log())

    def test_integrate_resolves_binaries_before_the_checkout(self):
        decoy = '#!/bin/sh\necho decoy >> "$CALLS/decoy.log"\n'
        self.git("checkout", "-q", "--detach", self.head, cwd=self.seed)
        self.commit(self.seed, "gh", decoy)
        self.commit(self.seed, "scripts/orchestrator/local-review.sh", decoy)
        self.git("push", "-q", "-f", "origin", "HEAD:refs/pull/7/head", cwd=self.seed)
        head = self.git("rev-parse", "HEAD", cwd=self.seed)
        (self.calls / "head").write_text(head + "\n")
        (self.calls / "reviews.json").write_text("[]")
        self.chain(env={"PATH": f".{os.pathsep}{self.env['PATH']}"})
        self.assertTrue((self.review / "gh").exists())
        self.assertFalse((self.calls / "decoy.log").exists())
        self.assertEqual([f"{TASK} {head} 7"], self.calls_of("local-review"))
        self.assertIn("bot review: absent", self.log(head))

    def test_integrate_runs_gh_without_forced_colour(self):
        # Revise round 3 (the local review of 6e4e9aa1, P1): a Herdr pane exports CLICOLOR_FORCE=1, and gh then
        # colours its output, so the comments JSON fill_sweep.py reads (and every compared gh answer) would hold ANSI.
        out = self.chain(env={"CLICOLOR_FORCE": "1", "GH_FORCE_TTY": "1"}).stdout
        self.assertEqual(f"chain-integrate: {TASK} {self.head} Verdict: correct", out.splitlines()[-1])
        fill = (self.calls / "fill_sweep.log").read_text()
        self.assertEqual([{"id": 1, "body": "a"}, {"id": 2, "body": "b,\nc"}], json.loads(fill.split("\n", 4)[4]))
        self.assertIn("--orchestrator-login orch\n", fill)
        self.assertNotIn("\x1b", self.log())

    def test_integrate_refuses_an_absent_owner_task_before_the_advisory_step(self):
        (self.main / f".orchestration/tasks/{OWNER}.md").unlink()
        (self.calls / "local-review.status").write_text("3")
        self.assertIn(f"write the owner task {OWNER} first", self.chain(code=15).stderr)
        self.assertEqual([], self.calls_of("local-advisory"))
        self.assertEqual([], self.calls_of("pr-feedback"))

    def test_integrate_stops_on_a_sandbox_scan_hit(self):
        (self.calls / "sandbox-scan.out").write_text(f"12: dangerouslyDisableSandbox git commit\n{SCAN_HIT}\n")
        result = self.chain(code=16)
        self.assertIn(f"CHAIN_SCAN_JUDGED={self.head[:7]}", result.stderr)
        for name in ("local-review", "local-advisory", "pr-feedback", "fill_sweep", "orch-audit"):
            self.assertEqual([], self.calls_of(name))
        self.chain(env={"CHAIN_SCAN_JUDGED": self.head[:7]})
        self.assertIn("sandbox scan: judged by the orchestrator", self.log())
        self.assertEqual([f"{TASK} {self.head} 7"], self.calls_of("local-review"))

    # chain-finish.sh (plan 022 T8)

    def finish_ready(self, summary="audit\nVerdict: correct\n", lines=""):
        """The review worktree at the PR head, the gate's inputs for it, and the record with the given lines."""
        self.git("fetch", "-q", "origin", "pull/7/head", cwd=self.review)
        self.git("checkout", "-q", "--detach", "FETCH_HEAD", cwd=self.review)
        sha7 = self.head[:7]
        (self.v / f"{TASK}-pr-feedback.json").write_text(json.dumps({"pr": 7, "head_sha": self.head, "items": []}))
        (self.v / f"{TASK}-audit-{sha7}.md").write_text("transcript\n")
        (self.v / f"{TASK}-audit-{sha7}.md.last.md").write_text(summary)
        (self.v / f"{TASK}-review-receipt.md").write_text("review_surface: crit-data\n")
        (self.v / f"{TASK}-crit.json").write_text("[]\n")
        record = self.main / f".orchestration/acceptance/{TASK}.md"
        record.write_text(record.read_text() + lines)
        self.write(".orchestration/extra.tsv", "")

    def finish(self, *args, code=0, env=None):
        argv = args or (TASK, "7", self.main, self.review, self.main / ".orchestration/extra.tsv")
        result = subprocess.run(
            ["bash", str(FINISH), *map(str, argv)],
            cwd=self.temp,
            env={**self.env, **(env or {})},
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        return result

    def finding(self, n, reason="the finding is about a line this PR does not change"):
        return f"audit-finding: {self.head[:7]}:{n} not-applicable:{reason}; evidence=git show HEAD:a.txt\n"

    def test_finish_refuses_a_head_that_differs_from_the_audit(self):
        self.finish_ready()
        summary = self.v / f"{TASK}-audit-{self.head[:7]}.md.last.md"

        def refused(message, *args):
            self.assertIn(message, self.finish(*args, code=10).stderr)
            stubs = [p.name for p in self.calls.glob("*.log") if p.name not in ("gh.log", "uv.log")]
            self.assertEqual([], stubs)
            self.assertNotIn("pr merge", "\n".join(self.calls_of("gh")))

        summary.rename(summary.with_suffix(".bak"))
        refused("head differs from the audit")
        summary.with_suffix(".bak").rename(summary)
        (self.calls / "head").write_text("0" * 40 + "\n")
        refused("head differs from the audit")
        (self.calls / "head").write_text(self.head + "\n")
        refused("invalid argument", "a/b", "7", self.main, self.review, self.main / ".orchestration/extra.tsv")
        other = self.temp / "other"
        self.git("clone", "-q", str(self.temp / "origin.git"), str(other), cwd=self.temp)
        refused("not the canonical one", TASK, "7", self.main, other, self.main / ".orchestration/extra.tsv")
        (self.v / f"{TASK}-review-receipt.md").unlink()
        refused(f"gate input missing: .orchestration/validation/{TASK}-review-receipt.md")
        self.assertEqual("", self.log())

    def test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head(self):
        # The local review of f20826e (P1): the thread step posts the sweep's dispositions, so a sweep of an earlier
        # head of the same PR refuses before any GitHub write; the PR head read is the only gh call.
        self.finish_ready()
        sweep, stale = self.v / f"{TASK}-pr-feedback.json", "0" * 40
        sweep.write_text(json.dumps({"pr": 7, "head_sha": stale, "items": []}))
        result = self.finish(code=10)
        self.assertIn(f"the sweep JSON is head {stale}'s, not the audited head {self.head}'s", result.stderr)
        self.assertEqual([], [p.name for p in self.calls.glob("*.log") if p.name not in ("gh.log", "uv.log")])
        self.assertEqual(["pr view 7 --json headRefOid --jq .headRefOid"], self.calls_of("gh"))
        self.assertEqual("", self.log())
        sweep.write_text(json.dumps({"pr": 7, "head_sha": self.head, "items": []}))
        self.finish()
        self.assertEqual(1, len(self.calls_of("resolve-threads")))

    def test_finish_requires_an_audit_finding_line_per_incorrect_finding(self):
        sha7 = self.head[:7]
        self.finish_ready("- [P2] one\n* [P3] two\nVerdict: incorrect\n", self.finding(1))
        result = self.finish(code=12)
        self.assertIn(f"audit finding 2 of {sha7} has no audit-finding line", result.stderr)
        self.assertEqual([], self.calls_of("resolve-threads"))
        record = self.main / f".orchestration/acceptance/{TASK}.md"
        record.write_text(record.read_text() + self.finding(2, "the second finding names a file outside this PR"))
        self.finish()
        [argv] = self.calls_of("acceptance-front-matter")
        dispositions = f"{self.v}/{TASK}-audit-dispositions-{sha7}.tsv"
        self.assertTrue(
            argv.endswith(f"--ledger {self.v}/{TASK}-ledger-{sha7}.tsv --audit-dispositions {dispositions}")
        )
        logged = (self.calls / "acceptance-front-matter.log").read_text()
        self.assertIn(
            "1\tthe finding is about a line this PR does not change\tgit show HEAD:a.txt\n"
            "2\tthe second finding names a file outside this PR\tgit show HEAD:a.txt\n",
            logged,
        )
        self.assertEqual([], list(self.v.glob("*.tsv")))
        self.assertFalse((self.v / f"{TASK}-pr-comments.json").exists())
        # A correct verdict that still lists findings needs their lines too, and passes no dispositions.
        (self.calls / "acceptance-front-matter.log").unlink()
        summary = self.v / f"{TASK}-audit-{sha7}.md.last.md"
        summary.write_text("[P1] one\n- [P2] two\n+ [P3] three\nVerdict: correct\n")
        self.assertIn(f"audit finding 3 of {sha7} has no audit-finding line", self.finish(code=12).stderr)
        record.write_text(record.read_text() + self.finding(3, "the third finding repeats the first one here"))
        self.finish()
        [argv] = self.calls_of("acceptance-front-matter")
        self.assertNotIn("--audit-dispositions", argv)
        summary.write_text("audit\nVerdict: unclear\n")
        self.assertIn("unexpected audit verdict: Verdict: unclear", self.finish(code=12).stderr)

    def test_finish_checks_each_audit_finding_line_in_full(self):
        # PR #378 thread 4300359437: a correct verdict passes no dispositions to the record script, so the chain reads
        # each line in the gate's grammar: one `; evidence=` with a command, and a reason of 20 or more characters.
        sha7 = self.head[:7]
        self.finish_ready("[P2] one\nVerdict: correct\n")
        record = self.main / f".orchestration/acceptance/{TASK}.md"
        kept = record.read_text()
        good = "the finding is about a line this PR does not change"
        for case, line in (
            ("no evidence", f"audit-finding: {sha7}:1 not-applicable:{good}\n"),
            ("two evidence delimiters", f"audit-finding: {sha7}:1 not-applicable:{good}; evidence=a; evidence=b\n"),
            ("empty evidence", f"audit-finding: {sha7}:1 not-applicable:{good}; evidence= \n"),
            ("a short reason", self.finding(1, "too short")),
            ("a tab", self.finding(1, f"{good}\twith a tab")),
        ):
            with self.subTest(case):
                record.write_text(kept + line)
                self.assertIn(f"audit finding 1 of {sha7}: the line is not", self.finish(code=12).stderr)
                self.assertEqual([], self.calls_of("resolve-threads"))
        record.write_text(kept + self.finding(1, good))
        self.finish()
        self.assertEqual(1, len(self.calls_of("resolve-threads")))

    def test_finish_runs_pr_cost_with_a_path_of_resolved_links(self):
        # The local review of f4d86ee5 (P1): after the fast-forward the main checkout's mise config is the merged
        # head's, so pr-cost.sh runs under env -i with a PATH of one directory of links resolved before any write.
        self.finish_ready()
        self.finish()
        [path] = re.findall(r"^path: (.*)$", (self.calls / "pr-cost.log").read_text(), re.MULTILINE)
        self.assertEqual(f"{self.v}/{TASK}-pr-cost-bin-{self.head[:7]}", path)
        self.assertFalse(Path(path).exists())
        self.assertNotIn(str(self.temp), self.log())
        # A tool that resolves only to a shims directory refuses before any GitHub write.
        shims = self.temp / "shims"
        self.executable(shims / "jq", "#!/bin/sh\nexit 0\n")
        result = self.finish(code=10, env={"PATH": f"{shims}{os.pathsep}{self.env['PATH']}"})
        self.assertIn(f"no jq for pr-cost.sh outside a shims directory: {shims}/jq", result.stderr)
        self.assertEqual(1, len(self.calls_of("resolve-threads")))

    def test_finish_reads_the_last_nonblank_line_as_the_verdict(self):
        # The local review of f4d86ee5 (P2): trailing blank lines and spaces do not hide the verdict, as the gate reads it.
        self.finish_ready("[P2] one\n  Verdict: correct  \n\n \n", self.finding(1))
        self.finish()
        self.assertIn("verdict rc=0: Verdict: correct, 1 finding(s)", self.log())
        self.assertNotIn("--audit-dispositions", self.calls_of("acceptance-front-matter")[0])

    def test_finish_counts_the_trimmed_reason(self):
        # The local review of f4d86ee5 (P2): spaces around a short reason do not reach the 20-character minimum.
        sha7 = self.head[:7]
        self.finish_ready("[P2] one\nVerdict: incorrect\n", self.finding(1, "short" + " " * 30))
        self.assertIn(f"audit finding 1 of {sha7}: the line is not", self.finish(code=12).stderr)
        self.assertEqual([], self.calls_of("resolve-threads"))

    def test_finish_runs_gate_before_merge_and_cost_after(self):
        self.finish_ready()
        self.finish()
        order = [
            "resolve-threads",
            "pr-feedback",
            "fill_sweep",
            "acceptance-front-matter",
            "orch-gate",
            "gh pr merge",
            "ff-main",
            "pr-cost",
        ]
        self.assertEqual(order, (self.calls / "order.log").read_text().splitlines())
        merges = [c for c in self.calls_of("gh") if c.startswith("pr merge")]
        self.assertEqual([f"pr merge --squash --match-head-commit {self.head} 7"], merges)
        extra = self.main / ".orchestration/extra.tsv"
        self.assertEqual([f"7 {extra} - {self.v}/{TASK}-pr-feedback.json"], self.calls_of("resolve-threads"))
        self.assertEqual([f"{TASK} {self.review} 7"], self.calls_of("orch-gate"))
        self.assertEqual(["7"], self.calls_of("pr-cost"))
        for name in ("ff-main", "pr-cost"):
            self.assertIn(f"cwd: {self.main}\n", (self.calls / f"{name}.log").read_text())
        steps = self.steps(self.log())
        self.assertEqual(
            [
                "verdict",
                "resolve-threads",
                "pr-feedback",
                "fill-sweep",
                "record",
                "gate",
                "merge",
                "ff-main",
                "pr-cost",
            ],
            steps,
        )
        self.assertNotIn(str(self.temp), self.log())
        # A failed gate merges nothing and writes no cost line.
        (self.calls / "order.log").unlink()
        (self.calls / "orch-gate.status").write_text("3")
        self.assertIn("step gate failed rc=3", self.finish(code=1).stderr)
        self.assertEqual(order[:5], (self.calls / "order.log").read_text().splitlines())

    def test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward(self):
        # PR #378 thread 4300324931: the fast-forward puts the merged head's pr-cost.sh in the main checkout; the
        # chain runs HEAD's copy taken before the merge, never the PR's.
        self.finish_ready()
        hook = f"""#!/bin/sh
printf '#!/bin/sh\\necho decoy >> "$CALLS/decoy.log"\\n' > "{self.main}/scripts/orchestrator/pr-cost.sh"
"""
        self.executable(self.calls / "ff-main-hook", hook)
        self.finish()
        self.assertFalse((self.calls / "decoy.log").exists())
        self.assertEqual(["7"], self.calls_of("pr-cost"))
        self.assertIn(f"cwd: {self.main}\n", (self.calls / "pr-cost.log").read_text())
        self.assertEqual([], list(self.v.glob("*-pr-cost-*.sh")))

    def test_finish_prints_the_acceptance_line_and_sends_nothing(self):
        self.finish_ready()
        last = self.finish().stdout.splitlines()[-1]
        pattern = rf"^AGMSG-ACCEPTANCE v1 task_id={TASK} status=accepted reason=merged-as-[0-9a-f]{{40}}-pr-7-head-{self.head[:7]} next_action="
        self.assertRegex(last, pattern)
        self.assertIn(f"merged-as-{self.git('rev-parse', 'origin/main')}-", last)
        self.assertFalse((self.calls / "send.log").exists())


if __name__ == "__main__":
    unittest.main()
