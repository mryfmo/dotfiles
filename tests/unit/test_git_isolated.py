"""Exercise scripts/orchestrator/git-isolated.sh, the levers' one isolated git (regime-cutover U113, plan P-22; the
acceptance test of research 01 section 1.6).

Each test sources the library from the checkout (its self-check reads the checkout's manifest pin) in a bash process,
once under PATH's bash and once under /bin/bash where it exists (bash 3.2 on macOS, the levers' interpreter). HOME and
XDG_CONFIG_HOME point into a scratch directory, so the hostile user configuration written here is the one a plain git
reads and nothing reads the real ~/.gitconfig.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "scripts/orchestrator/git-isolated.sh"
SHELLS = ("bash", *(["/bin/bash"] if Path("/bin/bash").is_file() else []))
# The flag set the library must hold (brief U113 CHANGE 1; research 01 section 1.6 plus core.commitGraph=false).
ENV = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_ATTR_NOSYSTEM": "1",
    "GIT_TERMINAL_PROMPT": "0",
}
ARGS = [
    "--no-replace-objects",
    *("-c", "core.hooksPath=/dev/null"),
    *("-c", "core.fsmonitor=false"),
    *("-c", "core.attributesFile=/dev/null"),
    *("-c", "core.commitGraph=false"),
    *("-c", "core.sshCommand=false"),
    *("-c", "protocol.allow=never"),
    *("-c", "protocol.https.allow=always"),
    *("-c", "credential.helper="),
    *("-c", "credential.interactive=false"),
    *("-c", "gc.auto=0"),
    *("-c", "maintenance.auto=false"),
]
# The hooks of the hostile hooks directory: each writes a marker named after itself when it runs.
HOOKS = ("pre-commit", "post-index-change", "reference-transaction", "pre-push", "post-checkout", "fsmonitor-watchman")
# Exported names a caller may steer git or its transport with; the scrub removes every one.
STEERED = {
    "GIT_CONFIG_PARAMETERS": "'core.fsmonitor=false'",
    "GIT_CONFIG_COUNT": "1",
    "GIT_CONFIG_KEY_0": "core.hooksPath",
    "GIT_CONFIG_VALUE_0": "/x/hooks",
    "GIT_DIR": "/x/.git",
    "GIT_AUTHOR_NAME": "steered",
    "https_proxy": "http://proxy.invalid:3128",
    "SSL_CERT_FILE": "/x/ca.pem",
}


class GitIsolatedTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        self.xdg = self.root / "xdg"
        self.xdg.mkdir()
        # What a plain git reads here: the scratch HOME and XDG_CONFIG_HOME, no level switch.
        self.plain_env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "XDG_CONFIG_HOME": str(self.xdg)}
        # The tests' own git, for making repositories and reading them back: no user configuration at all.
        self.setup_env = quiet_git_env(
            {
                **self.plain_env,
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_NAME": "setup",
                "GIT_AUTHOR_EMAIL": "setup@example.invalid",
                "GIT_COMMITTER_NAME": "setup",
                "GIT_COMMITTER_EMAIL": "setup@example.invalid",
            }
        )

    def git(self, *args, env=None, cwd=None, check=True):
        return subprocess.run(
            ["git", *args], cwd=cwd, env=env or self.setup_env, capture_output=True, text=True, check=check
        )

    def bash(self, shell, script, env, cwd=None, before=""):
        """SCRIPT after the library is sourced under `set -euo pipefail`; BEFORE runs ahead of the sourcing."""
        return subprocess.run(
            [shell, "-c", f'set -euo pipefail; {before}. "{LIBRARY}"; {script}'],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def hostile(self, label):
        """A work repository holding `data.txt` in its index, an empty bare target, a hooks directory and a markers
        directory, with the hostile configuration in the repository's .git/config, HOME's .gitconfig and
        XDG_CONFIG_HOME's git/config, each including a file that holds the same again. The URL rewrites are in the
        user files only: the repository level has no off switch (research 01 section 1.5), so a rewrite there is
        reached by any git run in that repository and the levers push from a repository they created instead, which
        the second phase of the acceptance test measures."""
        root = self.root / label
        root.mkdir()
        repo = git_init(root / "repo", env=self.setup_env, cwd=root)
        bare = git_init(root / "bare.git", "--bare", env=self.setup_env, cwd=root)
        (repo / "data.txt").write_bytes(b"plain bytes\n")
        self.git("add", "data.txt", cwd=repo)
        markers = root / "markers"
        markers.mkdir()
        hooks = root / "hooks"
        hooks.mkdir()
        for name in (*HOOKS, "fsmonitor"):
            (hooks / name).write_text(f"#!/bin/sh\necho ran >> '{markers}/{name}'\n")
            (hooks / name).chmod(0o755)
        (hooks / "clean").write_text(f"#!/bin/sh\necho ran >> '{markers}/clean'\necho FILTERED\n")
        (hooks / "clean").chmod(0o755)
        (repo / ".gitattributes").write_text("data.txt filter=mark\n")
        programs = (
            f"[core]\n\tfsmonitor = {hooks}/fsmonitor\n\thooksPath = {hooks}\n"
            f"[author]\n\tname = hostile\n"
            f'[filter "mark"]\n\tclean = {hooks}/clean\n'
        )
        rewrites = f'[url "{root}/nonexistent/"]\n\tinsteadOf = {bare}\n\tpushInsteadOf = {bare}\n'
        (self.xdg / "git").mkdir(exist_ok=True)
        for path, text in (
            (repo / ".git/config", programs),
            (self.home / ".gitconfig", programs + rewrites),
            (self.xdg / "git/config", programs + rewrites),
        ):
            include = path.parent / f"{path.name}.more.inc"
            include.write_text(text)
            with path.open("a") as handle:
                handle.write(text + f'[includeIf "gitdir:**"]\n\tpath = {include}\n')
        return repo, bare, markers, rewrites

    def test_a_hostile_repository_and_user_configuration_reach_no_isolated_command(self):
        """Research 01 section 1.6: with every hook, an fsmonitor program, an identity and a clean filter in the
        repository's and the user's configuration and URL rewrites in the user's, `git_isolated ls-files`,
        `hash-object -w --no-filters`, `commit-tree`, `update-ref` and the push to the bare target run no hook, rewrite
        no URL, apply no filter and take the identity from the environment; a push without the caller's
        `-c protocol.file.allow=always` is refused, which is the last-wins rule at work. The control first: a plain git
        under the same HOME runs the fsmonitor program and the filter and is redirected, so the configuration is live.
        Then the one level the library cannot close: a rewrite written into the repository's own config reaches an
        isolated push run in that repository, and not one run through `--git-dir` from a repository the caller
        created, which is how records-sync.sh pushes (research 01 section 1.5)."""
        for shell in SHELLS:
            with self.subTest(shell=shell):
                label = shell.strip("/").replace("/", "-")
                repo, bare, markers, rewrites = self.hostile(label)
                self.git("ls-files", env=self.plain_env, cwd=repo)
                self.git("hash-object", "-w", "data.txt", env=self.plain_env, cwd=repo)
                redirected = self.git("ls-remote", str(bare), env=self.plain_env, cwd=repo, check=False)
                self.assertEqual({"fsmonitor", "clean"}, {path.name for path in markers.iterdir()}, "the control")
                self.assertNotEqual(0, redirected.returncode, "the control: the rewrite is live for a plain git")
                for path in markers.iterdir():
                    path.unlink()
                out = self.root / f"{label}-out"
                out.mkdir()
                identity = (
                    "GIT_AUTHOR_NAME=env-author GIT_AUTHOR_EMAIL=author@example.invalid "
                    "GIT_COMMITTER_NAME=env-committer GIT_COMMITTER_EMAIL=committer@example.invalid"
                )
                script = f"""
git_env_scrub
git_isolated ls-files > '{out}/ls-files'
blob=$(git_isolated hash-object -w --no-filters data.txt)
git_isolated cat-file blob "${{blob}}" > '{out}/blob'
tree=$(printf '100644 blob %s\\tdata.txt\\n' "${{blob}}" | git_isolated mktree)
commit=$({identity} git_isolated commit-tree "${{tree}}" -m isolated)
git_isolated update-ref refs/heads/isolated "${{commit}}"
git_isolated log -1 --format='%an %cn' "${{commit}}" > '{out}/identity'
status=0
git_isolated push -q '{bare}' "${{commit}}:refs/heads/main" 2> '{out}/refused' || status=$?
printf '%s\\n' "${{status}}" > '{out}/refused-status'
git_isolated -c protocol.file.allow=always push -q '{bare}' "${{commit}}:refs/heads/main"
git_isolated -c protocol.file.allow=always ls-remote --heads '{bare}' > '{out}/ls-remote'
printf '%s\\n' "${{commit}}" > '{out}/commit'
"""
                run = self.bash(shell, script, self.plain_env, cwd=repo)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                commit = (out / "commit").read_text().strip()
                self.assertEqual("data.txt\n", (out / "ls-files").read_text())
                self.assertEqual(b"plain bytes\n", (out / "blob").read_bytes(), "no clean filter")
                self.assertEqual("env-author env-committer\n", (out / "identity").read_text())
                self.assertNotEqual("0", (out / "refused-status").read_text().strip(), "no transport but https")
                self.assertIn("not allowed", (out / "refused").read_text())
                self.assertEqual(f"{commit}\trefs/heads/main\n", (out / "ls-remote").read_text(), "no rewrite")
                self.assertEqual(commit, self.git("rev-parse", "refs/heads/main", cwd=bare).stdout.strip())
                self.assertEqual([], list(markers.iterdir()), "no hook, fsmonitor program or filter ran")

                with (repo / ".git/config").open("a") as handle:
                    handle.write(rewrites)
                script = f"""
git_env_scrub
status=0
git_isolated -c protocol.file.allow=always push -q '{bare}' "{commit}:refs/heads/in-checkout" 2> '{out}/rewritten' || status=$?
printf '%s\\n' "${{status}}" > '{out}/rewritten-status'
git_isolated init -q --bare --template= '{out}/scratch.git'
git_isolated --git-dir='{out}/scratch.git' -c protocol.file.allow=always fetch -q "${{PWD}}" refs/heads/isolated
git_isolated --git-dir='{out}/scratch.git' -c protocol.file.allow=always push -q '{bare}' FETCH_HEAD:refs/heads/from-scratch
"""
                run = self.bash(shell, script, self.plain_env, cwd=repo)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                self.assertNotEqual("0", (out / "rewritten-status").read_text().strip(), "the repository level")
                self.assertIn("nonexistent", (out / "rewritten").read_text())
                heads = self.git("for-each-ref", "--format=%(refname) %(objectname)", "refs/heads/", cwd=bare).stdout
                self.assertEqual(f"refs/heads/from-scratch {commit}\nrefs/heads/main {commit}\n", heads)
                self.assertEqual([], list(markers.iterdir()), "no hook ran on either side of the transfers")

    def test_the_scrub_removes_git_and_transport_names_and_keeps_the_named_ones(self):
        for shell in SHELLS:
            with self.subTest(shell=shell):
                env = {**self.plain_env, **STEERED, "KEPT": "1"}
                run = self.bash(shell, "git_env_scrub; compgen -e", env)
                self.assertEqual(run.returncode, 0, run.stderr)
                names = set(run.stdout.split())
                self.assertEqual(set(), names & set(STEERED))
                self.assertLessEqual({"KEPT", "PATH", "HOME"}, names, "only the named sets go")
                run = self.bash(shell, "git_env_scrub GIT_DIR https_proxy; compgen -e", env)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual({"GIT_DIR", "https_proxy"}, set(run.stdout.split()) & set(STEERED))

    def test_a_readonly_name_or_an_unlistable_environment_makes_the_scrub_refuse(self):
        """The scrub's producers fail closed (standing order 21): an `unset` that fails and a `compgen` that cannot run
        are each exit 2 naming the cause, and nothing after the call runs."""
        for shell in SHELLS:
            with self.subTest(shell=shell):
                run = self.bash(shell, "export GIT_X=1; readonly GIT_X; git_env_scrub; echo reached", self.plain_env)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertIn("refused: cannot remove GIT_X from the environment", run.stderr)
                self.assertNotIn("reached", run.stdout)
                run = self.bash(shell, "enable -n compgen; git_env_scrub; echo reached", self.plain_env)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertIn("refused: cannot list the environment", run.stderr)
                self.assertNotIn("reached", run.stdout)

    def recording_git(self):
        """A git first on PATH that records its argv and environment as JSON: the PATH entry and the record file."""
        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir(exist_ok=True)
        record = self.root / "git-call.json"
        fake = fake_bin / "git"
        fake.write_text(
            f"#!{sys.executable}\nimport json, os, sys\n"
            f'json.dump({{"argv": sys.argv[1:], "env": dict(os.environ)}}, open({str(record)!r}, "w"))\n'
        )
        fake.chmod(0o755)
        return fake_bin, record

    def test_the_function_runs_git_with_exactly_the_arrays(self):
        """The function and the data agree: a fake git first on PATH records its argv and environment; the argv starts
        with GIT_ISOLATED_ARGS, the environment's GIT_* names are exactly GIT_ISOLATED_ENV, the arrays are the
        documented set, and nothing is exported into the caller."""
        fake_bin, record = self.recording_git()
        script = (
            "git_env_scrub; git_isolated -C /x status; "
            'printf "%s\\n" "${GIT_ISOLATED_ENV[@]}" --- "${GIT_ISOLATED_ARGS[@]}" ===; compgen -e'
        )
        for shell in SHELLS:
            with self.subTest(shell=shell):
                record.unlink(missing_ok=True)
                env = {**self.plain_env, "PATH": f"{fake_bin}:{self.plain_env['PATH']}", **STEERED}
                run = self.bash(shell, script, env)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                lines = run.stdout.splitlines()
                env_entries, flags = lines[: lines.index("---")], lines[lines.index("---") + 1 : lines.index("===")]
                exported = lines[lines.index("===") + 1 :]
                self.assertEqual([f"{name}={value}" for name, value in ENV.items()], env_entries)
                self.assertEqual(ARGS, flags)
                call = json.loads(record.read_text())
                self.assertEqual([*ARGS, "-C", "/x", "status"], call["argv"])
                self.assertEqual(ENV, {name: value for name, value in call["env"].items() if name.startswith("GIT_")})
                self.assertEqual(env["PATH"], call["env"]["PATH"], "the caller's other variables stay")
                self.assertEqual([], [name for name in exported if name.startswith("GIT_")], "nothing exported")

    def test_an_inherited_export_of_the_library_s_own_names_leaves_the_flags_whole(self):
        """Round 2 P1: a GIT_ISOLATED_ENV, GIT_ISOLATED_ARGS or GIT_ISOLATED_SCRUB_NAMES exported in the caller's
        environment (a stray `export`, or a planted one) keeps its export attribute through an array assignment, so
        the scrub, which removes every exported GIT_* name, would remove the library's own arrays and `git_isolated`
        would run git with no isolation. The library unsets the three names before it assigns them, so the scrub
        leaves them and git runs under the whole set."""
        fake_bin, record = self.recording_git()
        inherited = {"GIT_ISOLATED_ENV": "x", "GIT_ISOLATED_ARGS": "x", "GIT_ISOLATED_SCRUB_NAMES": "x"}
        for shell in SHELLS:
            with self.subTest(shell=shell):
                record.unlink(missing_ok=True)
                env = {**self.plain_env, "PATH": f"{fake_bin}:{self.plain_env['PATH']}", **STEERED, **inherited}
                run = self.bash(shell, "git_env_scrub; git_isolated -C /x status; compgen -e", env)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                call = json.loads(record.read_text())
                self.assertEqual([*ARGS, "-C", "/x", "status"], call["argv"])
                self.assertEqual(ENV, {name: value for name, value in call["env"].items() if name.startswith("GIT_")})
                self.assertEqual([], [name for name in run.stdout.split() if name.startswith("GIT_")], "none exported")

    def test_a_readonly_library_name_in_the_sourcing_shell_is_a_refusal(self):
        """A readonly GIT_ISOLATED_ENV, GIT_ISOLATED_ARGS or GIT_ISOLATED_SCRUB_NAMES can be neither unset nor
        assigned: sourcing the library is exit 2 naming it, and nothing after the sourcing runs."""
        for shell in SHELLS:
            for name in ("GIT_ISOLATED_ENV", "GIT_ISOLATED_ARGS", "GIT_ISOLATED_SCRUB_NAMES"):
                with self.subTest(shell=shell, name=name):
                    run = self.bash(shell, "echo reached", self.plain_env, before=f"readonly {name}=stale; ")
                    self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                    self.assertIn(f"git-isolated.sh: refused: {name} is readonly in the sourcing shell", run.stderr)
                    self.assertNotIn("reached", run.stdout)

    def test_an_export_or_an_emptying_of_a_library_name_after_the_sourcing_is_a_refusal(self):
        """The nets behind the first: a name of the library exported after the sourcing is a refusal of the scrub,
        never removed as one more GIT_* name (a kept name included), and `git_isolated` with an array unset or empty
        is exit 2 naming the array, not a git with fewer flags."""
        fake_bin, record = self.recording_git()
        env = {**self.plain_env, "PATH": f"{fake_bin}:{self.plain_env['PATH']}"}
        for shell in SHELLS:
            with self.subTest(shell=shell):
                for scrub in ("git_env_scrub", "git_env_scrub GIT_ISOLATED_SCRUB_NAMES"):
                    run = self.bash(shell, f"export GIT_ISOLATED_SCRUB_NAMES; {scrub}; echo reached", env)
                    self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                    self.assertIn("refused: GIT_ISOLATED_SCRUB_NAMES is exported", run.stderr)
                    self.assertNotIn("reached", run.stdout)
                for name, emptied in (
                    ("GIT_ISOLATED_ENV", "unset -v GIT_ISOLATED_ENV"),
                    ("GIT_ISOLATED_ARGS", "GIT_ISOLATED_ARGS=()"),
                    ("GIT_ISOLATED_SCRUB_NAMES", "unset -v GIT_ISOLATED_SCRUB_NAMES"),
                ):
                    with self.subTest(name=name):
                        record.unlink(missing_ok=True)
                        run = self.bash(shell, f"{emptied}; git_isolated -C /x status; echo reached", env)
                        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                        self.assertIn(f"refused: {name} is empty", run.stderr)
                        self.assertNotIn("reached", run.stdout)
                        self.assertFalse(record.exists(), "no git ran")

    def test_a_refusal_is_prefixed_with_the_sourcing_script_s_name_or_the_library_s_own(self):
        """CI run 40834060550 of af5c1237: sourced by a harness from a `bash -c` string, the library has no
        `BASH_SOURCE[1]`, and under `set -u` the scrub died on its own prefix (`unbound variable`, exit 1) instead of
        refusing. A refusal from the scrub or from `git_isolated` is exit 2, prefixed with the sourcing script's name
        when there is one and with `git-isolated.sh:` when there is none."""
        lever = self.root / "some-lever.sh"
        lever.write_text(
            f'set -euo pipefail\n. "{LIBRARY}"\ncase $1 in\nscrub) export GIT_X=1; readonly GIT_X; git_env_scrub ;;\n'
            "run) GIT_ISOLATED_ARGS=(); git_isolated -C /x status ;;\nesac\necho reached\n"
        )
        cases = (
            ("export GIT_X=1; readonly GIT_X; git_env_scrub", "scrub", "cannot remove GIT_X from the environment"),
            ("GIT_ISOLATED_ARGS=(); git_isolated -C /x status", "run", "GIT_ISOLATED_ARGS is empty"),
        )
        for shell in SHELLS:
            for harness, mode, message in cases:
                with self.subTest(shell=shell, mode=mode):
                    run = self.bash(shell, f"{harness}; echo reached", self.plain_env)
                    self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                    self.assertIn(f"git-isolated.sh: refused: {message}", run.stderr)
                    self.assertNotIn("unbound variable", run.stderr)
                    self.assertNotIn("reached", run.stdout)
                    run = subprocess.run(
                        [shell, str(lever), mode], env=self.plain_env, capture_output=True, text=True, check=False
                    )
                    self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                    self.assertIn(f"some-lever.sh: refused: {message}", run.stderr)
                    self.assertNotIn("reached", run.stdout)


if __name__ == "__main__":
    unittest.main()
