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
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
TASK, OWNER = "dotfiles-T128-x-a01", "dotfiles-T128-x-followup-a01"
STUB = (
    "#!/usr/bin/env bash\n"
    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\npath: %s\\nreview: %s\\n" "$(pwd -P)" "$PATH" "${{ORCH_REVIEW_WORKTREE:-}}"\n'
    '  for a; do case $a in *.tsv | *-pr-comments.json) cat -- "$a" ;; esac; done; }} >> "$CALLS/{name}.log"\n'
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
"api user") paint < "$CALLS/login" ;;
"api "*)
    case $2 in *reviews) f=$CALLS/reviews.json ;; *) f=$CALLS/comments.json ;; esac
    if [ -n "$jq" ]; then JQ -rc "$jq" "$f"; else cat "$f"; fi | paint ;;
esac
"""
UV = """#!/usr/bin/env bash
{ printf "argv:"; printf " %s" "$@"; printf "\\n"; } >> "$CALLS/uv.log"
shift 4
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
            self.executable(self.seed / "scripts" / rel, STUB.format(name=name))
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

    def test_integrate_inherits_the_audit_across_an_update_branch_only_head(self):
        # Plan 023 F1 (C-61): a merge of main into the audited head with the same PR patch inherits its audit under the
        # head's names, the first line naming the head the audit ran on; a merge that also edits the PR side does not.
        p7, summary = self.head[:7], "[P3] low a.txt:1 nit\nVerdict: correct\n"
        (self.v / f"{TASK}-audit-{p7}.md").write_text("transcript\n")
        (self.v / f"{TASK}-audit-{p7}.md.last.md").write_text(summary)

        def move_main(name):  # on origin/main, since the seed's own main also holds the PR commit
            self.git("checkout", "-q", "--detach", "origin/main", cwd=self.seed)
            self.commit(self.seed, name)
            self.git("push", "-q", "origin", "HEAD:main", cwd=self.seed)
            self.git("pull", "-q", "--ff-only")

        def pr_head(first, edit=False):
            self.git("checkout", "-q", "--detach", first, cwd=self.seed)
            self.git("merge", "-q", "--no-ff", "--no-edit", "--no-commit", "origin/main", cwd=self.seed)
            if edit:
                (self.seed / "b.txt").write_text("b, edited in the merge\n")
                self.git("add", "b.txt", cwd=self.seed)
            self.git("commit", "-q", "--no-edit", cwd=self.seed)
            self.git("push", "-q", "origin", "+HEAD:refs/pull/7/head", cwd=self.seed)
            (self.calls / "head").write_text(self.git("rev-parse", "HEAD", cwd=self.seed) + "\n")
            return self.git("rev-parse", "HEAD", cwd=self.seed)

        def patch_id(rev):
            command = 'git diff-tree -p "$(git merge-base origin/main "$1")" "$1" | git patch-id --stable'
            return subprocess.run(
                ["bash", "-c", command, "-", rev], cwd=self.seed, capture_output=True, text=True, check=True
            ).stdout.split()[0]

        move_main("c.txt")
        merged = pr_head(self.head)
        self.assertEqual(patch_id(self.head), patch_id(merged))
        out = self.chain().stdout
        self.assertEqual([], self.calls_of("orch-audit"))
        for suffix, text in ((".md", "transcript\n"), (".md.last.md", summary)):
            self.assertEqual(
                f"inherited-from: {p7}\n{text}", (self.v / f"{TASK}-audit-{merged[:7]}{suffix}").read_text()
            )
        self.assertIn(f" audit rc=0: audit inherited from {p7}", self.log(merged))
        self.assertEqual(f"chain-integrate: {TASK} {merged} Verdict: correct", out.splitlines()[-1])
        # The same two parents, the merge also editing b.txt: another patch, so the audit runs and nothing is inherited.
        edited = pr_head(self.head, edit=True)
        self.assertNotEqual(patch_id(self.head), patch_id(edited))
        self.chain()
        self.assertEqual([f"{TASK} {self.review} 7"], self.calls_of("orch-audit"))
        self.assertEqual([], list(self.v.glob(f"{TASK}-audit-{edited[:7]}.md*")))
        # A head that inherited passes its marker on unchanged, so the ids stay the head the audit ran on.
        move_main("d.txt")
        again = pr_head(merged)
        self.chain()
        self.assertEqual(1, len(self.calls_of("orch-audit")))
        self.assertEqual(
            f"inherited-from: {p7}\n{summary}", (self.v / f"{TASK}-audit-{again[:7]}.md.last.md").read_text()
        )

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


if __name__ == "__main__":
    unittest.main()
