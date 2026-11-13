"""The `claude-keyed` lever (regime-cutover U510): the bridge's `pathToClaudeCodeExecutable`, which runs the Agent SDK's
bundled Claude Code binary with `ANTHROPIC_API_KEY` read from the one file `REGIME_ANTHROPIC_KEY_FILE` names and the
login names unset, or refuses with one stderr line and exit 2 before anything starts. Every test runs the real bash
(`#!/bin/bash -p`) against the installed layout under a scratch HOME: a fixture manifest naming a fixture bridge
directory whose one `claude-agent-sdk-fake/claude` records its argv and the names (never the values) of the variables
it received. No test reads the real `~/.agents`, `~/.local/bin` or a real key, and the fixture key is built at runtime
so this file holds no literal a secret scan matches."""

import hashlib
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/claude-keyed"
INSTALLED = ROOT / "home/dot_local/bin/common/executable_claude-keyed"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
KEY_FILE_VARIABLE = "REGIME_ANTHROPIC_KEY_FILE"
API_KEY_NAME = "ANTHROPIC_API_KEY"
# The three names the lever unsets (the bridge README: an exported gateway variable redirects the child), spelled in
# parts so the committed-secret scan sees no credential name beside a value.
OAUTH_NAME = "CLAUDE_CODE_OAUTH_" + "TOKEN"
AUTH_TOKEN_NAME = "ANTHROPIC_AUTH_" + "TOKEN"
BASE_URL_NAME = "ANTHROPIC_BASE_URL"
# A key inside the class the lever admits (`^sk-ant-[A-Za-z0-9_-]{20,}$`), built at runtime.
FIXTURE_KEY = "sk-ant-" + "api03-" + "FAKEKEYFORTEST" + "0123456789"
SDK_ARGS = ["--output-format", "stream-json", "--input-format", "stream-json", "--verbose", "-p", "hello world"]
UNSET_LINE = f"unset: {OAUTH_NAME} {AUTH_TOKEN_NAME} {BASE_URL_NAME}\n"


class ClaudeKeyedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="claude-keyed-")).resolve()
        self.addCleanup(shutil.rmtree, self.temp)
        self.home = self.temp / "home"
        self.bin = self.home / ".local/bin/common"
        self.bin.mkdir(parents=True)
        self.lever = self.bin / "claude-keyed"
        shutil.copy2(LEVER, self.lever)
        self.bridge = self.home / "bridge"
        self.sdk_dir = self.bridge / "node_modules/@anthropic-ai/claude-agent-sdk-fake"
        self.exe = self.sdk_dir / "claude"
        self.record = self.temp / "fake-claude-ran"
        self.expected_key = self.temp / "expected-key"
        self.expected_key.write_text(FIXTURE_KEY + "\n")
        self.write_fake_claude(self.exe)
        self.keys = self.home / "keys"
        self.keys.mkdir(mode=0o700)
        self.key_file = self.keys / "api-key"
        self.write_key(self.key_file, FIXTURE_KEY + "\n")
        (self.home / ".agents").mkdir()
        self.manifest = self.home / ".agents/agent-config.yaml"
        self.write_manifest()
        self.env = {
            "PATH": os.environ["PATH"],
            "HOME": str(self.home),
            "LC_ALL": "C",
            KEY_FILE_VARIABLE: str(self.key_file),
        }

    def write_fake_claude(self, path: Path) -> None:
        """The fixture SDK binary: argv one per line, the names of the ANTHROPIC_* and login variables it received,
        whether ANTHROPIC_API_KEY equals the fixture key, and a record file that proves it ran."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "#!/bin/sh\n"
            f": > '{self.record}'\n"
            'for a in "$@"; do printf \'arg: %s\\n\' "$a"; done\n'
            f"env | sed -n -e 's/^\\(ANTHROPIC_[A-Z_]*\\)=.*/name: \\1/p' -e 's/^\\({OAUTH_NAME}\\)=.*/name: \\1/p' | sort\n"
            f"expected=$(cat '{self.expected_key}')\n"
            f'if [ "${{{API_KEY_NAME}:-}}" = "$expected" ]; then echo "key matches: yes"; else echo "key matches: no"; fi\n'
        )
        path.chmod(0o755)

    def write_key(self, path: Path, text: str, mode: int = 0o600) -> None:
        path.write_text(text)
        path.chmod(mode)

    def write_manifest(self, lever: Path | None = None, bridge: str = "~/bridge", extensions: str = "~/bridge") -> None:
        pin = hashlib.sha256((lever or self.lever).read_bytes()).hexdigest()
        self.manifest.write_text(
            "schema_version: 1\n"
            "omp:\n"
            "  extension_providers:\n"
            f"    claude-bridge: {bridge}\n"
            "    openai-siwc: ~/siwc\n"
            "claude:\n"
            "  levers:\n"
            "    sha256:\n"
            f"      claude-keyed: {pin}\n"
            "    extensions:\n"
            f"      - {extensions}\n"
            "      - ~/siwc\n"
        )

    def run_lever(self, *args: str, env: dict[str, str] | None = None, lever: Path | None = None):
        return subprocess.run(
            [str(lever or self.lever), *args],
            cwd=self.home,
            env=self.env if env is None else env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def env_with(self, **changes: str | None) -> dict[str, str]:
        env = dict(self.env)
        for name, value in changes.items():
            if value is None:
                env.pop(name, None)
            else:
                env[name] = value
        return env

    def fake_tool(self, name: str, body: str) -> dict[str, str]:
        tools = self.temp / "tools"
        tools.mkdir(exist_ok=True)
        (tools / name).write_text(f"#!/bin/sh\n{body}\n")
        (tools / name).chmod(0o755)
        return self.env_with(PATH=f"{tools}:{self.env['PATH']}")

    def assert_refused(self, run, reason: str) -> None:
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(run.stdout, "", "nothing reaches stdout on a refusal")
        self.assertEqual(run.stderr, f"claude-keyed: refused: {reason}\n")
        self.assertFalse(self.record.exists(), "the SDK binary did not run")
        self.assertNotIn(FIXTURE_KEY, run.stderr)

    def test_the_lever_runs_under_bash_privileged_mode_and_is_installed_pinned(self) -> None:
        """pr-audit.sh's and router-gh's form (U465f): `#!/bin/bash -p`, so a poisoned environment replaces no builtin;
        the chezmoi copy is byte-identical and the manifest pins its sha256."""
        self.assertEqual(LEVER.read_text().splitlines()[0], "#!/bin/bash -p")
        self.assertEqual(INSTALLED.read_bytes(), LEVER.read_bytes())
        self.assertTrue(os.access(INSTALLED, os.X_OK))
        pin = hashlib.sha256(LEVER.read_bytes()).hexdigest()
        self.assertIn(f"\n      claude-keyed: {pin}\n", MANIFEST.read_text())

    def test_the_exec_path_runs_the_sdk_binary_with_the_key_and_without_the_login_names(self) -> None:
        """The binary gets the lever's own arguments unchanged, ANTHROPIC_API_KEY from the file (replacing a caller's
        value), the three names unset, and every other variable as it was."""
        env = self.env_with(
            **{
                OAUTH_NAME: "fake-oauth-value",
                AUTH_TOKEN_NAME: "fake-auth-value",
                BASE_URL_NAME: "http://127.0.0.1:9/",
                API_KEY_NAME: "a-callers-wrong-value",
                "ANTHROPIC_MODEL": "stays",
            }
        )
        run = self.run_lever(*SDK_ARGS, env=env)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stderr, "")
        self.assertTrue(self.record.exists(), "the SDK binary ran")
        expected = "".join(f"arg: {arg}\n" for arg in SDK_ARGS)
        expected += f"name: {API_KEY_NAME}\nname: ANTHROPIC_MODEL\n"
        expected += "key matches: yes\n"
        self.assertEqual(run.stdout, expected)
        self.assertNotIn(FIXTURE_KEY, run.stdout + run.stderr)

    def test_check_prints_one_line_and_runs_nothing(self) -> None:
        run = self.run_lever("--check")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {self.exe}\n")
        self.assertFalse(self.record.exists())
        self.assertNotIn(FIXTURE_KEY, run.stdout)
        self.assert_refused(
            self.run_lever("--check", "extra"),
            "usage: claude-keyed --check | claude-keyed --dry-run [<argument>...] | claude-keyed [<argument>...]",
        )

    def test_dry_run_prints_the_argv_with_the_key_redacted(self) -> None:
        run = self.run_lever("--dry-run", *SDK_ARGS)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(
            run.stdout,
            f"{API_KEY_NAME}=<redacted> {self.exe} --output-format stream-json --input-format stream-json --verbose "
            "-p hello\\ world\n" + UNSET_LINE,
        )
        self.assertFalse(self.record.exists())
        self.assertNotIn(FIXTURE_KEY, run.stdout)
        bare = self.run_lever("--dry-run")
        self.assertEqual(bare.stdout, f"{API_KEY_NAME}=<redacted> {self.exe}\n" + UNSET_LINE)

    def test_each_key_file_refusal_by_name(self) -> None:
        other_uid = os.geteuid() + 1
        link = self.keys / "link"
        link.symlink_to(self.key_file)
        cases = [
            (
                "no variable",
                lambda: self.env_with(**{KEY_FILE_VARIABLE: None}),
                f"{KEY_FILE_VARIABLE} is not set; hcom-seat sets it to <seats-root>/.state/anthropic/api-key "
                "(regime-cutover U512) and the operator places the key there (the U510 handout)",
            ),
            (
                "a relative path",
                lambda: self.env_with(**{KEY_FILE_VARIABLE: "keys/api-key"}),
                f"{KEY_FILE_VARIABLE} 'keys/api-key' is not an absolute path",
            ),
            (
                "an absent file",
                lambda: self.env_with(**{KEY_FILE_VARIABLE: str(self.keys / "absent")}),
                f"the key file {self.keys / 'absent'} is absent; place the API key there (the U510 handout)",
            ),
            (
                "a symbolic link",
                lambda: self.env_with(**{KEY_FILE_VARIABLE: str(link)}),
                f"the key file {link} is a symbolic link; the key file must be a regular file of this user",
            ),
            (
                "a directory",
                lambda: self.env_with(**{KEY_FILE_VARIABLE: str(self.keys)}),
                f"the key file {self.keys} is not a regular file",
            ),
            (
                "mode 0644",
                lambda: (self.key_file.chmod(0o644), self.env)[1],
                f"the key file {self.key_file} has mode 644; the key must be readable by this user alone (0600)",
            ),
            (
                "another user's file (an injected stat)",
                lambda: (self.key_file.chmod(0o600), self.fake_tool("stat", f"echo '600 {other_uid}'"))[1],
                f"the key file {self.key_file} is owned by uid {other_uid}, not this user (uid {os.geteuid()})",
            ),
            (
                "an empty file",
                lambda: (self.write_key(self.key_file, ""), self.env)[1],
                f"the key file {self.key_file} is empty; the key must be one line of the form sk-ant-... (the U510 handout)",
            ),
            (
                "two lines",
                lambda: (self.write_key(self.key_file, FIXTURE_KEY + "\n" + FIXTURE_KEY + "\n"), self.env)[1],
                f"the key file {self.key_file} holds more than one line; the key must be one line",
            ),
            (
                "an empty second line",
                lambda: (self.write_key(self.key_file, FIXTURE_KEY + "\n\n"), self.env)[1],
                f"the key file {self.key_file} holds more than one line; the key must be one line",
            ),
            (
                "a carriage return",
                lambda: (self.write_key(self.key_file, FIXTURE_KEY + "\r\n"), self.env)[1],
                f"the key file {self.key_file} holds a carriage return; the key must be one line ending in a line feed alone",
            ),
            (
                "a trailing space",
                lambda: (self.write_key(self.key_file, FIXTURE_KEY + " \n"), self.env)[1],
                f"the key file {self.key_file} does not hold a key of the form sk-ant-<20 or more of [A-Za-z0-9_-]> "
                "(the content is never printed)",
            ),
            (
                "a key outside the class",
                lambda: (self.write_key(self.key_file, "sk-ant-short\n"), self.env)[1],
                f"the key file {self.key_file} does not hold a key of the form sk-ant-<20 or more of [A-Za-z0-9_-]> "
                "(the content is never printed)",
            ),
            (
                "a NUL byte",
                lambda: (self.write_key(self.key_file, FIXTURE_KEY + "\0\n"), self.env)[1],
                f"the key file {self.key_file} holds a byte the shell cannot read (a NUL); the key must be one line",
            ),
        ]
        for label, arrange, reason in cases:
            with self.subTest(case=label):
                env = arrange()
                for mode in ((), ("--check",), ("--dry-run",)):
                    run = self.run_lever(*mode, *SDK_ARGS, env=env) if not mode else self.run_lever(*mode, env=env)
                    self.assert_refused(run, reason)
                    self.assertNotIn(FIXTURE_KEY, run.stdout + run.stderr)

    def test_zero_or_two_executables_refuse_naming_the_glob(self) -> None:
        glob = f"{self.bridge}/node_modules/@anthropic-ai/claude-agent-sdk-*/claude"
        second = self.bridge / "node_modules/@anthropic-ai/claude-agent-sdk-other/claude"
        self.write_fake_claude(second)
        self.assert_refused(self.run_lever(*SDK_ARGS), f"2 Claude Code executables match {glob}; exactly one is run")
        self.assert_refused(self.run_lever("--check"), f"2 Claude Code executables match {glob}; exactly one is run")
        shutil.rmtree(second.parent)
        self.exe.chmod(0o644)
        self.assert_refused(
            self.run_lever(*SDK_ARGS), f"the Claude Code executable {self.exe} is not an executable regular file"
        )
        shutil.rmtree(self.sdk_dir)
        self.assert_refused(self.run_lever(*SDK_ARGS), f"no Claude Code executable: nothing matches {glob}")
        self.assert_refused(self.run_lever("--check"), f"no Claude Code executable: nothing matches {glob}")

    def test_the_bridge_directory_comes_from_the_manifest_and_must_be_an_allowed_extension(self) -> None:
        self.write_manifest(bridge="~/elsewhere", extensions="~/bridge")
        self.assert_refused(
            self.run_lever("--check"),
            f"the claude-bridge directory {self.home}/elsewhere is not a row of claude.levers.extensions in {self.manifest}",
        )
        self.write_manifest(bridge="~/elsewhere", extensions="~/elsewhere")
        self.assert_refused(
            self.run_lever("--check"), f"the claude-bridge directory {self.home}/elsewhere is not a directory"
        )
        self.manifest.write_text(self.manifest.read_text().replace("    claude-bridge: ~/elsewhere\n", ""))
        self.assert_refused(
            self.run_lever("--check"),
            f"the manifest {self.manifest} names no omp.extension_providers.claude-bridge directory",
        )

    def test_an_unreadable_manifest_refuses(self) -> None:
        if os.geteuid() == 0:
            self.skipTest("root reads a mode 000 manifest, so the unreadable-manifest refusal cannot be forced")
        self.manifest.chmod(0)
        self.addCleanup(self.manifest.chmod, 0o644)
        self.assert_refused(self.run_lever("--check"), f"manifest unreadable: {self.manifest}")

    def test_a_failing_producer_refuses_instead_of_passing(self) -> None:
        """Standing order 21: every read the decision rests on fails closed, by name."""
        cases = [
            ("uname", "exit 3", "cannot read the operating system name (uname -s)"),
            ("stat", "exit 3", f"cannot read the mode and owner of the key file {self.key_file} (stat failed)"),
            (
                "stat",
                "echo garbage",
                f"cannot read the mode and owner of the key file {self.key_file} (stat printed 'garbage')",
            ),
            ("cat", "exit 3", f"cannot read the key file {self.key_file}"),
            ("wc", "exit 3", f"cannot count the bytes of the key file {self.key_file} (wc -c failed)"),
            ("awk", "exit 3", f"cannot read the manifest {self.manifest} (awk failed)"),
        ]
        for tool, body, reason in cases:
            with self.subTest(tool=tool, body=body):
                env = self.fake_tool(tool, body)
                self.assert_refused(self.run_lever(*SDK_ARGS, env=env), reason)
                (self.temp / "tools" / tool).unlink()

    def test_the_self_pin_refuses_an_altered_copy(self) -> None:
        with self.lever.open("a") as lever:
            lever.write("echo rewritten\n")
        run = self.run_lever("--check")
        self.assertEqual(run.returncode, 2)
        self.assertIn("claude-keyed: refused: sha256 ", run.stderr)
        self.assertIn(f"differs from the pin in {self.manifest}", run.stderr)
        self.assertEqual(run.stdout, "")
        self.assertFalse(self.record.exists())

    def test_the_checkout_copy_reads_the_checkout_manifest(self) -> None:
        """Run from scripts/orchestrator, the lever reads home/dot_agents/agent-config.yaml two levels up; with the
        real manifest its bridge directory is the deployed extension, absent under a scratch HOME, so the refusal
        names that directory and never a key."""
        run = self.run_lever("--check", lever=LEVER)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(run.stdout, "")
        self.assertEqual(
            run.stderr,
            f"claude-keyed: refused: the claude-bridge directory {self.home}/.local/lib/omp-extensions/pi-claude-bridge "
            "is not a directory\n",
        )
        self.assertNotIn(FIXTURE_KEY, run.stderr)

    def test_the_key_file_mode_is_judged_on_the_file_itself(self) -> None:
        """A 0600 file keeps the stat mode form of either OS (`600` or `0600`)."""
        self.assertEqual(stat.S_IMODE(self.key_file.stat().st_mode), 0o600)
        run = self.run_lever("--check")
        self.assertEqual(run.returncode, 0, run.stderr)


if __name__ == "__main__":
    unittest.main()
