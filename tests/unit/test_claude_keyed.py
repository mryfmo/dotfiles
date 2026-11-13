"""The `claude-keyed` lever (regime-cutover U510): the bridge's `pathToClaudeCodeExecutable`, which runs the Agent SDK's
bundled Claude Code binary with `ANTHROPIC_API_KEY` read from the one file `REGIME_ANTHROPIC_KEY_FILE` names and the
login names unset, or refuses with one stderr line and exit 2 before anything starts. Every test runs the real bash
(`#!/bin/bash -p`) against the installed layout under a scratch HOME: a fixture manifest naming a fixture bridge
directory whose `claude-agent-sdk-<host platform>/claude` (the platform the lever's closed table gives this host, so
the real `uname` is read) records its argv and the names (never the values) of the variables it received; the other
rows of the table run under a fixture `uname` and a fixture `stat` (U510c). No test reads the real `~/.agents`,
`~/.local/bin` or a real key, and the fixture key is built at runtime so this file holds no literal a secret scan
matches."""

import glob
import hashlib
import os
import platform
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
# The lever's closed platform table (uname -s, uname -m) and the musl loader marker it reads on Linux.
PLATFORMS = {
    ("Darwin", "arm64"): "darwin-arm64",
    ("Darwin", "x86_64"): "darwin-x64",
    ("Linux", "x86_64"): "linux-x64",
    ("Linux", "aarch64"): "linux-arm64",
}
MUSL_MARKER_VARIABLE = "CLAUDE_KEYED_MUSL_MARKER_GLOB"
MUSL_MARKER_GLOB = "/lib/ld-musl-*.so*"


def host_platform() -> str | None:
    """The table row of this host, as the lever would resolve it with the real uname: None off the table."""
    name = PLATFORMS.get((platform.system(), platform.machine()))
    if name is not None and name.startswith("linux-") and glob.glob(MUSL_MARKER_GLOB):
        name += "-musl"
    return name


HOST_PLATFORM = host_platform()


class ClaudeKeyedTest(unittest.TestCase):
    def setUp(self) -> None:
        if HOST_PLATFORM is None:
            self.skipTest(f"this host's uname pair {platform.system()} {platform.machine()} is off the lever's table")
        self.temp = Path(tempfile.mkdtemp(prefix="claude-keyed-")).resolve()
        self.addCleanup(shutil.rmtree, self.temp)
        self.home = self.temp / "home"
        self.bin = self.home / ".local/bin/common"
        self.bin.mkdir(parents=True)
        self.lever = self.bin / "claude-keyed"
        shutil.copy2(LEVER, self.lever)
        self.bridge = self.home / "bridge"
        self.sdk_dir = self.sdk_package(HOST_PLATFORM)
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

    def sdk_package(self, name: str) -> Path:
        """The directory of the SDK's platform package `name` under the fixture bridge."""
        return self.bridge / f"node_modules/@anthropic-ai/claude-agent-sdk-{name}"

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

    def fake_tool(self, name: str, body: str, env: dict[str, str] | None = None) -> dict[str, str]:
        tools = self.temp / "tools"
        tools.mkdir(exist_ok=True)
        (tools / name).write_text(f"#!/bin/sh\n{body}\n")
        (tools / name).chmod(0o755)
        base = self.env if env is None else env
        if base.get("PATH", "").startswith(f"{tools}:"):
            return dict(base)
        return {**base, "PATH": f"{tools}:{base['PATH']}"}

    def uname_env(self, system: str, machine: str, env: dict[str, str] | None = None) -> dict[str, str]:
        """A fixture `uname` answering the two words and a fixture `stat` printing a 0600 file of this user, so a table
        row can be exercised on any host (the real stat's dialect follows the fixture's uname -s)."""
        env = self.fake_tool(
            "uname", f"case $1 in -s) echo '{system}' ;; -m) echo '{machine}' ;; *) exit 3 ;; esac", env
        )
        return self.fake_tool("stat", f"echo '600 {os.geteuid()}'", env)

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

    def test_the_executable_is_the_host_platform_package_by_the_closed_table(self) -> None:
        """U510c: the path is `<bridge>/node_modules/@anthropic-ai/claude-agent-sdk-<platform>/claude` for the one
        platform the uname pair maps to; a second platform package beside it (the SDK installs the glibc and the musl
        package of a Linux architecture side by side) changes nothing, and `--check` prints the chosen path."""
        other = "darwin-x64" if HOST_PLATFORM != "darwin-x64" else "darwin-arm64"
        self.write_fake_claude(self.sdk_package(other) / "claude")
        self.write_fake_claude(self.sdk_package("linux-x64-musl") / "claude")
        run = self.run_lever("--check")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {self.exe}\n")
        self.assertIn(f"claude-agent-sdk-{HOST_PLATFORM}/claude", run.stdout)
        run = self.run_lever(*SDK_ARGS)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertTrue(self.record.exists(), "the host platform's binary ran")

    def test_an_absent_or_unfit_platform_package_refuses_naming_the_path(self) -> None:
        self.exe.chmod(0o644)
        self.assert_refused(
            self.run_lever(*SDK_ARGS), f"the Claude Code executable {self.exe} is not an executable regular file"
        )
        self.exe.unlink()
        self.exe.symlink_to(self.sdk_package("other") / "claude")
        self.write_fake_claude(self.sdk_package("other") / "claude")
        self.assert_refused(
            self.run_lever(*SDK_ARGS), f"the Claude Code executable {self.exe} is not an executable regular file"
        )
        shutil.rmtree(self.sdk_dir)
        reason = (
            f"no Claude Code executable at {self.exe}; the SDK's {HOST_PLATFORM} package is not installed under "
            f"{self.bridge}"
        )
        self.assert_refused(self.run_lever(*SDK_ARGS), reason)
        self.assert_refused(self.run_lever("--check"), reason)

    def test_linux_chooses_the_glibc_or_the_musl_package_by_the_loader_marker(self) -> None:
        """U510c: with both linux-x64 and linux-x64-musl installed and a fixture uname of Linux x86_64, the glibc
        package is run when no file matches the musl loader glob and the musl one when one does; the glob is the
        lever's one documented variable, `/lib/ld-musl-*.so*` by default."""
        glibc = self.sdk_package("linux-x64") / "claude"
        musl = self.sdk_package("linux-x64-musl") / "claude"
        self.write_fake_claude(glibc)
        self.write_fake_claude(musl)
        marker_dir = self.temp / "lib"
        marker_dir.mkdir()
        marker_glob = f"{marker_dir}/ld-musl-*.so*"
        env = self.uname_env("Linux", "x86_64")
        if not glob.glob(MUSL_MARKER_GLOB):
            run = self.run_lever("--check", env=env)
            self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
            self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {glibc}\n")
        env[MUSL_MARKER_VARIABLE] = marker_glob
        run = self.run_lever("--check", env=env)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {glibc}\n")
        (marker_dir / "ld-musl-x86_64.so.1").write_text("")
        run = self.run_lever("--check", env=env)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {musl}\n")
        run = self.run_lever("--dry-run", env=env)
        self.assertEqual(run.stdout, f"{API_KEY_NAME}=<redacted> {musl}\n" + UNSET_LINE)
        # A directory of the marker's name is no loader: the glibc package stays.
        (marker_dir / "ld-musl-x86_64.so.1").unlink()
        (marker_dir / "ld-musl-x86_64.so.1").mkdir()
        run = self.run_lever("--check", env=env)
        self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {glibc}\n")
        # With the musl package alone and no marker, the refusal names the glibc path it looked for.
        (marker_dir / "ld-musl-x86_64.so.1").rmdir()
        shutil.rmtree(glibc.parent)
        self.assert_refused(
            self.run_lever("--check", env=env),
            f"no Claude Code executable at {glibc}; the SDK's linux-x64 package is not installed under {self.bridge}",
        )

    def test_the_platform_table_is_closed(self) -> None:
        """Every row of the table under a fixture uname, and a pair off it refused naming both words."""
        for (system, machine), name in PLATFORMS.items():
            with self.subTest(platform=name):
                exe = self.sdk_package(name) / "claude"
                self.write_fake_claude(exe)
                env = self.uname_env(system, machine)
                env[MUSL_MARKER_VARIABLE] = f"{self.temp}/no-such-marker-*"
                run = self.run_lever("--check", env=env)
                self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
                self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {exe}\n")
                if name != HOST_PLATFORM:
                    shutil.rmtree(exe.parent)
        for system, machine in (
            ("FreeBSD", "amd64"),
            ("Linux", "armv7l"),
            ("Darwin", "i386"),
            ("MINGW64_NT", "x86_64"),
        ):
            with self.subTest(pair=(system, machine)):
                self.assert_refused(
                    self.run_lever("--check", env=self.uname_env(system, machine)),
                    f"no Claude Code platform package for the pair '{system}' '{machine}' (uname -s, uname -m); the "
                    "table is Darwin arm64, Darwin x86_64, Linux x86_64 and Linux aarch64",
                )

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
        """Standing order 21: every read the decision rests on fails closed, by name; each fixture prints a diagnostic
        on stderr before failing, and the refusal is still the one stderr line (U510c: every producer's stderr is
        dropped). The self-check's own readers, sed and both hash backends, are among them."""
        noisy = "echo 'fixture: a diagnostic the producer printed' >&2; exit 3"
        cases = [
            (("uname",), noisy, "cannot read the operating system name (uname -s)"),
            (
                ("uname",),
                f"case $1 in -s) echo '{platform.system()}' ;; *) {noisy} ;; esac",
                "cannot read the machine name (uname -m)",
            ),
            (("stat",), noisy, f"cannot read the mode and owner of the key file {self.key_file} (stat failed)"),
            (
                ("stat",),
                "echo garbage",
                f"cannot read the mode and owner of the key file {self.key_file} (stat printed 'garbage')",
            ),
            (("cat",), noisy, f"cannot read the key file {self.key_file}"),
            (("wc",), noisy, f"cannot count the bytes of the key file {self.key_file} (wc -c failed)"),
            (("awk",), noisy, f"cannot read the manifest {self.manifest} (awk failed)"),
            (("sed",), noisy, f"cannot read {self.manifest}"),
            (("sha256sum", "shasum"), noisy, f"cannot hash {self.lever}"),
            (("sha256sum", "shasum"), "echo 'not a digest'", f"cannot hash {self.lever}"),
        ]
        for tools, body, reason in cases:
            with self.subTest(tools=tools, body=body):
                env = self.env
                for tool in tools:
                    env = self.fake_tool(tool, body, env)
                self.assert_refused(self.run_lever(*SDK_ARGS, env=env), reason)
                self.assert_refused(self.run_lever("--check", env=env), reason)
                for tool in tools:
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
