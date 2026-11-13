"""The `claude-keyed` lever (regime-cutover U510): the bridge's `pathToClaudeCodeExecutable`, which runs the Agent SDK's
bundled Claude Code binary with `ANTHROPIC_API_KEY` read from the one file `REGIME_ANTHROPIC_KEY_FILE` names and the
login names unset, or refuses with one stderr line and exit 2 before anything starts. Every test runs the real bash
(`#!/bin/bash -p`) against the installed layout under a scratch root: a fixture manifest naming a fixture bridge
directory whose `claude-agent-sdk-<host platform>/claude` (the platform the lever's closed table gives this host, so
the real `uname` is read) records its argv, its PATH and the names (never the values) of the variables it received; the
other rows of the table run under a fixture `uname` and a fixture `stat` (U510c). The lever runs its producers on the
system directories alone (U510d), so a fixture tool reaches them only through a variant of the lever whose one change
is that PATH line (hcom-seat's form in tests/unit/test_lever_self_check.py), re-pinned in the fixture manifest; the
pristine copy is what the PATH test and every real-tool test run. No test reads the real `~/.agents`, `~/.local/bin`
or a real key, and the fixture key is built at runtime so this file holds no literal a secret scan matches."""

import glob
import hashlib
import os
import platform
import re
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
# The lever's PATH pin (hcom-seat's form, U85) and the one line the injectable test variant changes.
SYSTEM_PATH_LINE = "\nPATH=${system_path}\n"
CALLER_PATH_LINE = "\nPATH=${caller_path}\n"
# Names assigned on the exec line or as a prefix to one builtin: exported by design, or no value survives the command.
EXEC_LINE_NAMES = {"PATH", "ANTHROPIC_API_KEY", "LC_ALL", "IFS"}


def assigned_names(text: str) -> set[str]:
    """Every variable name the lever's text assigns: `name=`, `local` declarations, `for` and `read -r` targets, off
    comment lines; the exec-line and prefix names excepted."""
    names: set[str] = set()
    for line in text.splitlines():
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        names.update(re.findall(r"(?:^|(?<=[\s(]))([A-Za-z_]\w*)=(?!=)", line))
        local = re.match(r"\s*local\s+(.*)$", line)
        if local:
            names.update(word.split("=", 1)[0] for word in local.group(1).split())
        names.update(re.findall(r"\bfor\s+(\w+)\s+in\b", line))
        names.update(re.findall(r"\bread\s+-r\s+(\w+)", line))
    return names - EXEC_LINE_NAMES


def unset_names(text: str) -> set[str]:
    """The names of the lever's one `unset` statement, its continuation lines joined."""
    statement = text.split("\nunset ", 1)[1]
    joined = ""
    for line in statement.splitlines():
        joined += " " + line.rstrip("\\")
        if not line.endswith("\\"):
            break
    return set(joined.split())


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
        self.names = self.temp / "child-env-names"
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
        whether ANTHROPIC_API_KEY equals the fixture key, the PATH it got, a record file that proves it ran, and every
        name of its environment in a names file (the values never leave the child)."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "#!/bin/sh\n"
            f": > '{self.record}'\n"
            f"env | sed -n 's/^\\([A-Za-z_][A-Za-z0-9_]*\\)=.*/\\1/p' | sort > '{self.names}'\n"
            'for a in "$@"; do printf \'arg: %s\\n\' "$a"; done\n'
            f"env | sed -n -e 's/^\\(ANTHROPIC_[A-Z_]*\\)=.*/name: \\1/p' -e 's/^\\({OAUTH_NAME}\\)=.*/name: \\1/p' | sort\n"
            f"IFS= read -r expected < '{self.expected_key}'\n"
            f'if [ "${{{API_KEY_NAME}:-}}" = "$expected" ]; then echo "key matches: yes"; else echo "key matches: no"; fi\n'
            "printf 'path: %s\\n' \"${PATH-unset}\"\n"
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

    def use_injectable_lever(self, shim: str = "") -> None:
        """Rewrite the installed copy into the variant whose producers run on the caller's PATH (the one line
        `PATH=${system_path}` becomes `PATH=${caller_path}`, hcom-seat's test form) and re-pin it, so a fixture tool
        can stand in for uname, stat, cat, wc or awk; the pristine copy never consults one. `shim` is a function
        definition placed on the line after it, the test_hcom_seat form for a builtin (cd, pwd) no PATH entry
        replaces; the variant is built from the checkout's bytes, so a second call with another shim replaces it."""
        text = LEVER.read_text()
        variant = text.replace(SYSTEM_PATH_LINE, CALLER_PATH_LINE + (f"{shim}\n" if shim else ""))
        if self.lever.read_text() != variant:
            self.lever.write_text(variant)
            self.write_manifest()

    def fake_tool(
        self, name: str, body: str, env: dict[str, str] | None = None, injectable: bool = True
    ) -> dict[str, str]:
        if injectable:
            self.use_injectable_lever()
        tools = self.temp / "tools"
        tools.mkdir(exist_ok=True)
        (tools / name).write_text(f"#!/bin/sh\n{body}\n")
        (tools / name).chmod(0o755)
        base = self.env if env is None else env
        if base.get("PATH", "").startswith(f"{tools}:"):
            return dict(base)
        return {**base, "PATH": f"{tools}:{base['PATH']}"}

    def stat_body(self, file_line: str, dir_line: str = "") -> str:
        """A fixture `stat` answering `file_line` for the key file and `dir_line` (a 0700 directory of this user
        unless given) for every other path: the lever's one stat form puts the path third, after the format."""
        dir_line = dir_line or f"700 {os.geteuid()}"
        return f"case \"$3\" in '{self.key_file}') echo '{file_line}' ;; *) echo '{dir_line}' ;; esac"

    def uname_env(self, system: str, machine: str, env: dict[str, str] | None = None) -> dict[str, str]:
        """A fixture `uname` answering the two words and a fixture `stat` printing a 0600 file of this user in a 0700
        directory of this user, so a table row can be exercised on any host (the real stat's dialect follows the
        fixture's uname -s)."""
        env = self.fake_tool(
            "uname", f"case $1 in -s) echo '{system}' ;; -m) echo '{machine}' ;; *) exit 3 ;; esac", env
        )
        return self.fake_tool("stat", self.stat_body(f"600 {os.geteuid()}"), env)

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
        expected += f"path: {env['PATH']}\n"
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
                lambda: (self.key_file.chmod(0o600), self.fake_tool("stat", self.stat_body(f"600 {other_uid}")))[1],
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
        dropped). The self-check's own readers, sed and both hash backends, are among them. U510e (verdict
        U510-88ae09c6 P2 :479): the file's own stat (the directory's passing), the second manifest read (the
        `claude.levers.extensions` rows, the first passing) and the `cd` and `pwd -P` of the key directory hold each
        carry an injection too; the two builtins are shimmed by a function in the test variant, test_hcom_seat's form,
        since no PATH entry replaces them."""
        noisy = "echo 'fixture: a diagnostic the producer printed' >&2; exit 3"
        real_awk = shutil.which("awk", path="/usr/bin:/bin")
        cases = [
            (("uname",), noisy, "cannot read the operating system name (uname -s)"),
            (
                ("uname",),
                f"case $1 in -s) echo '{platform.system()}' ;; *) {noisy} ;; esac",
                "cannot read the machine name (uname -m)",
            ),
            (
                ("stat",),
                noisy,
                f"cannot read the mode and owner of the directory {self.keys} of the key file {self.key_file} (stat failed)",
            ),
            (
                ("stat",),
                "echo garbage",
                f"cannot read the mode and owner of the directory {self.keys} of the key file {self.key_file} "
                "(stat printed 'garbage')",
            ),
            (
                ("stat",),
                f"case \"$3\" in '{self.key_file}') {noisy} ;; *) echo '700 {os.geteuid()}' ;; esac",
                f"cannot read the mode and owner of the key file {self.key_file} (stat failed)",
            ),
            (
                ("stat",),
                self.stat_body("garbage"),
                f"cannot read the mode and owner of the key file {self.key_file} (stat printed 'garbage')",
            ),
            (("cat",), noisy, f"cannot read the key file {self.key_file}"),
            (("wc",), noisy, f"cannot count the bytes of the key file {self.key_file} (wc -c failed)"),
            (
                ("awk",),
                noisy,
                f"cannot read the omp.extension_providers rows of the manifest {self.manifest} (awk failed)",
            ),
            (
                ("awk",),
                f'case "$1" in *extensions:*) {noisy} ;; *) exec {real_awk} "$@" ;; esac',
                f"cannot read the claude.levers.extensions rows of the manifest {self.manifest} (awk failed)",
            ),
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
        hold = f"cannot resolve the directory of the key file {self.key_file}"
        shims = {
            "cd": f'cd() {{ if [[ $1 == "{self.keys}" ]]; then {noisy}; fi; builtin cd "$@"; }}',
            "pwd": f'pwd() {{ if [[ $PWD == "{self.keys}" ]]; then {noisy}; fi; builtin pwd "$@"; }}',
        }
        for builtin, shim in shims.items():
            with self.subTest(builtin=builtin):
                self.use_injectable_lever(shim)
                self.assert_refused(self.run_lever(*SDK_ARGS), hold)
                self.assert_refused(self.run_lever("--check"), hold)
        self.use_injectable_lever()
        run = self.run_lever("--check")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)

    def test_every_refusal_is_one_stderr_line_whatever_the_path_holds_or_bash_prints(self) -> None:
        """U510e (verdict U510-88ae09c6 P3 :150 and :231): a key path holding a line feed (or a carriage return) is
        refused on one line with the boundary folded to a space, and the key file gone between the cat and the wc
        read (a fixture cat that removes it after reading) yields the one wc refusal, bash's own note about the failed
        redirection dropped with the block's stderr."""
        for label, path in (("a line feed", f"{self.keys}/api\nkey"), ("a carriage return", f"{self.keys}/api\rkey")):
            with self.subTest(path=label):
                env = self.env_with(**{KEY_FILE_VARIABLE: path})
                reason = f"the key file {self.keys}/api key is absent; place the API key there (the U510 handout)"
                for mode in ((), ("--check",), ("--dry-run",)):
                    run = self.run_lever(*mode, *SDK_ARGS, env=env) if not mode else self.run_lever(*mode, env=env)
                    self.assert_refused(run, reason)
                    self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        env = self.fake_tool("cat", '/bin/cat "$@" && rm -f -- "$2"')
        reason = f"cannot count the bytes of the key file {self.key_file} (wc -c failed)"
        for mode in ((), ("--check",)):
            with self.subTest(mode=mode or ("exec",)):
                self.write_key(self.key_file, FIXTURE_KEY + "\n")
                run = self.run_lever(*mode, *SDK_ARGS, env=env) if not mode else self.run_lever(*mode, env=env)
                self.assert_refused(run, reason)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertFalse(self.key_file.exists(), "the fixture cat removed the file after reading it")

    def test_an_exported_name_the_lever_assigns_carries_nothing_into_a_producer_or_the_child(self) -> None:
        """U510e (verdict U510-88ae09c6 P2 :228): a variable exported into the lever's environment keeps its export
        attribute through an assignment, so `key=inherited` in the environment would hand the key itself to awk (which
        runs after the key is read) and to the child under the name `key`, and `mode` would reach the child as `exec`.
        The lever unsets every name it assigns first: the fixture producers' environments and the child's hold none
        of those names, every other variable stays, and the unset list equals the names the text assigns."""
        text = LEVER.read_text()
        self.assertEqual(unset_names(text), assigned_names(text), "the unset list is the names the text assigns")
        self.assertLess(text.index("\nunset "), text.index("\nlever_self_check() {"), "before anything is assigned")
        planted = {
            "key": "inherited",
            "key_text": "x",
            "mode": "sentinel",
            "LEVER_MANIFEST": f"{self.temp}/decoy-manifest",
            "exe": f"{self.temp}/decoy-exe",
            "UNRELATED_SETTING": "stays",
        }
        producer_names = self.temp / "producer-env-names"
        env = self.env_with(**planted)
        for tool in ("uname", "stat", "cat", "wc", "awk"):
            real = shutil.which(tool, path="/usr/bin:/bin")
            env = self.fake_tool(
                tool,
                f"env | sed -n 's/^\\([A-Za-z_][A-Za-z0-9_]*\\)=.*/\\1/p' >> '{producer_names}'; exec {real} \"$@\"",
                env,
            )
        run = self.run_lever(*SDK_ARGS, env=env)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertTrue(self.record.exists(), "the SDK binary ran")
        self.assertIn("key matches: yes\n", run.stdout)
        child = set(self.names.read_text().split())
        producers = set(producer_names.read_text().split())
        self.assertTrue(producers, "the fixture producers ran")
        for name in assigned_names(text):
            self.assertNotIn(name, child, f"the child's environment holds no {name}")
            self.assertNotIn(name, producers, f"no producer's environment holds {name}")
        self.assertIn("UNRELATED_SETTING", child)
        self.assertIn("UNRELATED_SETTING", producers)
        self.assertIn(API_KEY_NAME, child)
        self.assertNotIn(FIXTURE_KEY, run.stdout + run.stderr + producer_names.read_text())
        # The pristine copy under the same environment: the decoy manifest and executable steer nothing.
        self.record.unlink()
        shutil.copy2(LEVER, self.lever)
        self.write_manifest()
        run = self.run_lever("--check", env=self.env_with(**planted))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {self.exe}\n")

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

    def test_the_installed_copy_reads_the_manifest_of_its_own_root_whatever_home_says(self) -> None:
        """U510d (the review of 5594f0e7, finding 3): the installed copy under `<root>/.local/bin/common` reads
        `<root>/.agents/agent-config.yaml` and expands the manifest's `~/` through that root, by its own directory
        alone; a HOME that names another directory, no directory or nothing steers neither the pin nor the bridge
        directory the key reaches. The old fallback path, `<root>/.local/home/dot_agents/agent-config.yaml`, holds a
        decoy manifest pinning this copy and naming a decoy bridge under that HOME, and it is never read."""
        decoy_home = self.temp / "decoy-home"
        decoy_exe = decoy_home / f"decoy/node_modules/@anthropic-ai/claude-agent-sdk-{HOST_PLATFORM}/claude"
        self.write_fake_claude(decoy_exe)
        fallback = self.home / ".local/home/dot_agents/agent-config.yaml"
        fallback.parent.mkdir(parents=True)
        pin = hashlib.sha256(self.lever.read_bytes()).hexdigest()
        fallback.write_text(
            "schema_version: 1\nomp:\n  extension_providers:\n    claude-bridge: ~/decoy\nclaude:\n  levers:\n"
            f"    sha256:\n      claude-keyed: {pin}\n    extensions:\n      - ~/decoy\n"
        )
        for label, home in (
            ("another directory", str(decoy_home)),
            ("no directory", f"{self.temp}/absent"),
            ("unset", None),
        ):
            with self.subTest(home=label):
                env = self.env_with(HOME=home)
                run = self.run_lever("--check", env=env)
                self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
                self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {self.exe}\n")
                run = self.run_lever(*SDK_ARGS, env=env)
                self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
                self.assertTrue(self.record.exists(), "this root's binary ran")
                self.assertIn("key matches: yes\n", run.stdout)
                self.record.unlink()
        # The deployed manifest of that root is the one read: its pin judges the copy.
        self.manifest.write_text(self.manifest.read_text().replace(pin, "0" * 64))
        run = self.run_lever("--check", env=self.env_with(HOME=str(decoy_home)))
        self.assert_refused(run, f"sha256 {pin} of {self.lever} differs from the pin in {self.manifest}")
        # A copy in neither layout refuses by name instead of guessing a manifest.
        elsewhere = self.temp / "elsewhere"
        elsewhere.mkdir()
        shutil.copy2(self.lever, elsewhere / "claude-keyed")
        self.assert_refused(
            self.run_lever("--check", lever=elsewhere / "claude-keyed"),
            f"{elsewhere}/claude-keyed is neither an installed copy under <home>/.local/bin/common nor a checkout copy "
            "under scripts/orchestrator, so no manifest holds its pin",
        )

    def test_the_producers_run_on_the_system_path_and_the_child_gets_the_callers(self) -> None:
        """U510d (finding 4): `bash -p` keeps PATH, and inside a seat PATH holds the seat's tool directory and the
        caller's, so uname, stat, cat, wc and awk run on the system directories alone (hcom-seat's form): a planted
        uname, stat, awk, cat or wc on the caller's PATH changes nothing for the pristine copy, and the exec'd child
        gets the caller's PATH back. The self-check's sed and hash tool stay the kit's shared form
        (tests/unit/test_lever_self_check.py holds every shell lever but hcom-seat to it)."""
        text = LEVER.read_text()
        self.assertEqual(text.count("\nsystem_path=/usr/bin:/bin:/usr/sbin:/sbin\n"), 1)
        self.assertEqual(text.count(SYSTEM_PATH_LINE), 1)
        self.assertLess(text.index("\nlever_self_check\n"), text.index(SYSTEM_PATH_LINE), "pinned after the self-check")
        other_uid = os.geteuid() + 1
        env = self.fake_tool("uname", "echo FreeBSD", injectable=False)
        env = self.fake_tool("stat", f"echo '644 {other_uid}'", env, injectable=False)
        env = self.fake_tool("awk", f"echo '{self.home}/decoy'", env, injectable=False)
        env = self.fake_tool("cat", "echo not-a-key", env, injectable=False)
        env = self.fake_tool("wc", "echo 1", env, injectable=False)
        self.assertEqual(self.lever.read_bytes(), LEVER.read_bytes(), "the pristine copy runs")
        run = self.run_lever("--check", env=env)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(run.stdout, f"key file ok: {self.key_file}; executable: {self.exe}\n")
        run = self.run_lever(*SDK_ARGS, env=env)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertTrue(self.record.exists(), "the SDK binary ran")
        self.assertIn("key matches: yes\n", run.stdout)
        self.assertIn(f"path: {env['PATH']}\n", run.stdout, "the child's PATH is the caller's, planted tools and all")
        self.assertNotIn(FIXTURE_KEY, run.stdout + run.stderr)
        self.record.unlink()
        # The variant the injection tests run is the one line apart, and the planted uname then reaches it.
        self.use_injectable_lever()
        self.assertEqual(self.lever.read_text(), text.replace(SYSTEM_PATH_LINE, CALLER_PATH_LINE))
        self.assert_refused(
            self.run_lever(
                "--check", env=self.fake_tool("uname", "case $1 in -s) echo FreeBSD ;; *) echo amd64 ;; esac")
            ),
            "no Claude Code platform package for the pair 'FreeBSD' 'amd64' (uname -s, uname -m); the "
            "table is Darwin arm64, Darwin x86_64, Linux x86_64 and Linux aarch64",
        )

    def test_the_key_files_directory_is_held_to_this_user_alone(self) -> None:
        """U510d (finding 7): the checks on the key file and its read each open the path anew, so the directory that
        holds it is held too: its spelled last component no link, this user's, mode 0700, else one refusal naming the
        directory and the file; a writer of a looser directory could swap a link in between the checks and the read."""
        other_uid = os.geteuid() + 1
        link = self.home / "keylink"
        link.symlink_to(self.keys)
        cases = [
            (
                "mode 0755",
                lambda: (self.keys.chmod(0o755), self.env)[1],
                f"the directory {self.keys} of the key file {self.key_file} has mode 755; the directory must be this "
                "user's alone (0700)",
            ),
            (
                "mode 0710",
                lambda: (self.keys.chmod(0o710), self.env)[1],
                f"the directory {self.keys} of the key file {self.key_file} has mode 710; the directory must be this "
                "user's alone (0700)",
            ),
            (
                "a symbolic link",
                lambda: (self.keys.chmod(0o700), self.env_with(**{KEY_FILE_VARIABLE: str(link / "api-key")}))[1],
                f"the directory {link} of the key file {link / 'api-key'} is a symbolic link; the directory must be "
                "this user's alone (0700)",
            ),
            (
                "another user's directory (an injected stat)",
                lambda: self.fake_tool("stat", self.stat_body(f"600 {os.geteuid()}", f"700 {other_uid}")),
                f"the directory {self.keys} of the key file {self.key_file} is owned by uid {other_uid}, not this user "
                f"(uid {os.geteuid()})",
            ),
        ]
        for label, arrange, reason in cases:
            with self.subTest(case=label):
                env = arrange()
                for mode in ((), ("--check",), ("--dry-run",)):
                    run = self.run_lever(*mode, *SDK_ARGS, env=env) if not mode else self.run_lever(*mode, env=env)
                    self.assert_refused(run, reason)
        self.keys.chmod(0o700)
        run = self.run_lever("--check")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)


if __name__ == "__main__":
    unittest.main()
