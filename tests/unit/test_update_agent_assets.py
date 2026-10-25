"""Exercise verified artifact updates using fake downloads and installers only."""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UPDATER = ROOT / "scripts/update-agent-assets.sh"
PLATFORMS = {
    "Darwin/arm64": "DARWIN_ARM64",
    "Darwin/x86_64": "DARWIN_AMD64",
    "Linux/x86_64": "LINUX_AMD64",
    "Linux/aarch64": "LINUX_ARM64",
}
STUB = r"""#!@PYTHON@
import hashlib, json, os, shlex, sys
from pathlib import Path
name, args = Path(sys.argv[0]).name, sys.argv[1:]
if name == "uname":
    print(os.environ["FIXTURE_OS" if args == ["-s"] else "FIXTURE_ARCH"])
    sys.exit(0)
entry = {"tool": name, "argv": args, "min_release_age": os.environ.get("npm_config_min_release_age")}
if name == "curl":
    Path(args[args.index("-o") + 1]).write_bytes(Path(os.environ["PAYLOAD"]).read_bytes())
else:
    artifact = Path(args[-1])
    if not artifact.is_file():
        sys.exit("fixture installer requires an already downloaded file: " + str(artifact))
    entry["sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
    tool = "omp" if name == "npm" else "hcom"
    target = Path(os.environ["HOME"]) / ".local/bin" / tool
    if name == "npm":  # npm links its own bin and refuses with EEXIST to replace an entry it does not own
        own = "lib/node_modules/@oh-my-pi/pi-coding-agent/"
        link = os.readlink(target) if target.is_symlink() else ""  # bin-links resolves it before the ownership check
        resolved = os.path.normpath(os.path.join(target.parent, link)) if link else ""
        if (target.exists() or link) and not resolved.startswith(str(target.parent.parent / own) + os.sep):
            sys.exit("npm error code EEXIST: " + str(target))
        target.unlink(missing_ok=True)
        target.symlink_to("../" + own + "bin/omp")
        target = target.parent.parent / own / "bin/omp"
        target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("#!/usr/bin/env bash\nprintf '%s\\n' " + shlex.quote(tool + ("/" if tool == "omp" else " ") + os.environ["FIXTURE_VERSION"]) + "\n")
    target.chmod(0o755)
with open(os.environ["CALLS"], "a") as log:
    log.write(json.dumps(entry) + "\n")
"""


sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes, scratch_env
from claude_plugin_fixture import CONTENT_VERSION, REVIEWED

OFFICIAL_CLONE = REVIEWED / "marketplaces/claude-plugins-official"


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


class UpdateAgentAssetsTest(unittest.TestCase):
    def exercise_update(self, tool, platform="Linux/x86_64", *, unsupported=False, shadow_version=None):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            binary = home / ".local/bin"
            binary.mkdir(parents=True)
            for name in ("curl", "npm", "uv", "uname"):
                path = binary / name
                path.write_text(STUB.replace("@PYTHON@", sys.executable))
                path.chmod(0o755)
            target = binary / tool
            payload = home / "payload"
            payload.write_bytes(b"reproduced artifact bytes; no real package or binary\n")
            digest = hashlib.sha256(payload.read_bytes()).hexdigest()
            log = home / "calls.jsonl"
            pin = "18.11.3" if tool == "omp" else "0.7.30"
            search_path = str(binary) + os.pathsep + os.environ["PATH"]
            if shadow_version is not None:
                shadows = home / "shadows"
                shadows.mkdir()
                shadow = shadows / tool
                version = pin if shadow_version == "pin" else shadow_version
                shadow.write_text(f"#!/usr/bin/env bash\nprintf '{tool} {version}\\n'\n")
                shadow.chmod(0o755)
                search_path = str(shadows) + os.pathsep + search_path
            constants = 'OMP_PIN_VERSION=18.11.3; HCOM_PIN_VERSION=0.7.30; OMP_TARBALL_SHA256="$2"; '
            for key in PLATFORMS.values():
                constants += f'HCOM_{key}_SHA256="$2"; HCOM_{key}_URL="https://fixture.invalid/{key}/hcom-0.7.30-py3-none-any.whl"; '

            def reset():
                if shadow_version is None:
                    target.write_text("#!/usr/bin/env bash\nexit 1\n")
                    target.chmod(0o755)
                else:
                    target.unlink(missing_ok=True)
                log.write_text("")

            def update(checksum=digest, version=pin, prefix=""):
                return subprocess.run(
                    [
                        "bash",
                        "-c",
                        'source "$1"; ' + constants + prefix + f"update_{tool}",
                        "bash",
                        str(UPDATER),
                        checksum,
                    ],
                    env={
                        **os.environ,
                        "HOME": directory,
                        "PATH": search_path,
                        "CALLS": str(log),
                        "PAYLOAD": str(payload),
                        "FIXTURE_VERSION": version,
                        "FIXTURE_OS": platform.split("/")[0],
                        "FIXTURE_ARCH": platform.split("/")[1],
                        "npm_config_min_release_age": "3",
                    },
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )

            def calls():
                return [json.loads(line) for line in log.read_text().splitlines()]

            reset()
            installed = update()
            self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
            if unsupported:
                self.assertEqual([], calls())
                self.assertIn("unsupported platform", installed.stdout)
                return
            records = calls()
            self.assertEqual(["curl", "npm" if tool == "omp" else "uv"], [row["tool"] for row in records])
            # npm's three-day cooldown reaches the install too, so the tarball's dependencies resolve under it.
            self.assertEqual(["3", "3"], [row["min_release_age"] for row in records])
            url = records[0]["argv"][1]
            if tool == "omp":
                self.assertEqual(
                    f"https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-{pin}.tgz", url
                )
                self.assertEqual(["install", "-g", "--prefix", str(home / ".local")], records[1]["argv"][:-1])
            else:
                self.assertIn(PLATFORMS[platform], url)
                self.assertEqual(["tool", "install", "--force"], records[1]["argv"][:-1])
            artifact = Path(records[1]["argv"][-1])
            self.assertEqual(".tgz" if tool == "omp" else ".whl", artifact.suffix)
            self.assertEqual(digest, records[1]["sha256"])
            wheels = home / ".local/share/agent-assets/hcom"
            if tool == "omp":
                self.assertFalse(artifact.exists())
                self.assertFalse(artifact.parent.exists())
            else:
                # uv's receipt names the wheel as hcom's source, so the verified wheel outlives the run (local:b49da6d:1).
                self.assertEqual(wheels, artifact.parent)
                self.assertEqual(digest, hashlib.sha256(artifact.read_bytes()).hexdigest())
            receipt_path = home / ".agents/.installed-manifest.json"
            receipt = json.loads(receipt_path.read_text())["steps"][f"update_{tool}"]
            self.assertEqual(pin, receipt["source_version"])
            self.assertEqual([str(target)] + ([] if tool == "omp" else [str(artifact)]), receipt["paths"])
            repeated = update()
            self.assertEqual(0, repeated.returncode, repeated.stdout + repeated.stderr)
            self.assertIn("already installed", repeated.stdout)
            self.assertEqual(records, calls())

            reset()
            receipt_path.unlink()
            for kept in wheels.glob("*"):
                kept.unlink()
            bad_hash = "0" * 64
            drifted_hash = update(checksum=bad_hash)
            self.assertNotEqual(0, drifted_hash.returncode)
            self.assertIn(bad_hash, drifted_hash.stdout + drifted_hash.stderr)
            self.assertIn(digest, drifted_hash.stdout + drifted_hash.stderr)
            self.assertEqual(["curl"], [row["tool"] for row in calls()])
            self.assertFalse(Path(calls()[0]["argv"][-1]).parent.exists())
            self.assertEqual([], list(wheels.glob("*")))  # a wheel that fails its hash never reaches the managed path
            self.assertFalse(receipt_path.exists())

            reset()
            drifted_version = update(version="0.0.1")
            self.assertNotEqual(0, drifted_version.returncode)
            self.assertIn(pin, drifted_version.stdout + drifted_version.stderr)
            self.assertIn("0.0.1", drifted_version.stdout + drifted_version.stderr)
            self.assertEqual(2, len(calls()))
            # The omp tarball goes with its run; the hcom wheel stays where uv's receipt points.
            self.assertEqual(tool == "hcom", Path(calls()[1]["argv"][-1]).exists())
            self.assertFalse(receipt_path.exists())
            reset()
            skipped = update(prefix="has_command() { return 1; }; ")
            self.assertEqual(0, skipped.returncode, skipped.stdout + skipped.stderr)
            self.assertIn("command not found", skipped.stdout)
            self.assertEqual([], calls())

    def test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin(self):
        self.exercise_update("omp")

    def update_omp_in(self, home, version, spelling="", tmpdir=None):
        # update_omp with the fixture curl and npm on PATH, HOME=<home><spelling> and any TMPDIR; the caller has placed
        # any entry at ~/.local/bin/omp.
        binary = home / ".local/bin"
        binary.mkdir(parents=True, exist_ok=True)
        for name in ("curl", "npm"):
            (binary / name).write_text(STUB.replace("@PYTHON@", sys.executable))
            (binary / name).chmod(0o755)
        payload = home / "payload"
        payload.write_bytes(b"fixture omp tarball\n")
        return subprocess.run(
            ["bash", "-c", 'source "$1"; OMP_PIN_VERSION=18.11.3; OMP_TARBALL_SHA256="$2"; update_omp']
            + ["bash", str(UPDATER), hashlib.sha256(payload.read_bytes()).hexdigest()],
            env=os.environ
            | {
                "HOME": str(home) + spelling,
                "PATH": str(binary) + os.pathsep + os.environ["PATH"],
                "CALLS": str(home / "calls.jsonl"),
                "PAYLOAD": str(payload),
                "FIXTURE_VERSION": version,
            }
            | ({"TMPDIR": str(tmpdir)} if tmpdir else {}),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def test_update_omp_makes_its_download_directory_under_tmpdir(self):
        # audit:9e30542:1: the download directory takes its mktemp template from TMPDIR, as a sandbox sets it, never the
        # per-user default macOS mktemp picks without a template (which the agent sandbox refuses).
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            sandbox_tmp = home / "sandbox-tmp"
            sandbox_tmp.mkdir()
            result = self.update_omp_in(home, "18.11.3", tmpdir=sandbox_tmp)
            log = home / "calls.jsonl"
            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            outputs = [Path(row["argv"][row["argv"].index("-o") + 1]) for row in calls if row["tool"] == "curl"]
            output = result.stdout + result.stderr
            self.assertEqual([sandbox_tmp], [path.parent.parent for path in outputs], output)
            self.assertTrue(outputs[0].parent.name.startswith("update-agent-assets."), output)
            self.assertEqual(0, result.returncode, output)

    def test_a_link_target_escaping_the_npm_prefix_is_refused(self):
        # The Bot's P2 4307029052: npm resolves the link before its ownership check (bin-links check-bin), so a target
        # that starts with this prefix's package but leaves it through `..` is not npm's own and moves to the kept path.
        escaping = Path("../lib/node_modules/@oh-my-pi/pi-coding-agent/../../outside")
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            target = home / ".local/bin/omp"
            target.parent.mkdir(parents=True)
            target.symlink_to(escaping)
            result = self.update_omp_in(home, "18.11.3")
            output = result.stdout + result.stderr
            self.assertEqual(0, result.returncode, output)
            self.assertIn(f"resolves to {home}/.local/lib/node_modules/outside", result.stdout)
            self.assertEqual(escaping, (home / ".local/share/agent-assets/omp/omp.previous").readlink(), output)
            self.assertEqual(Path("../lib/node_modules/@oh-my-pi/pi-coding-agent/bin/omp"), target.readlink(), output)

    def test_update_omp_moves_an_entry_npm_does_not_own_aside_and_puts_it_back_when_the_install_fails(self):
        # local:fbbc6d9:1: a standalone file or a link outside this prefix's package, a dangling one included, makes npm
        # fail with EEXIST; it moves to a kept path, not the run's temporary directory. npm's own link and a directory
        # stay for npm to judge.
        npm_link = Path("../lib/node_modules/@oh-my-pi/pi-coding-agent/bin/omp")
        for entry in ("dangling", "external", "foreign", "file", "npm", "directory", None):
            for version in ("18.11.3", "0.0.1"):
                with self.subTest(entry=entry, version=version), tempfile.TemporaryDirectory() as directory:
                    home = Path(directory)
                    binary = home / ".local/bin"
                    binary.mkdir(parents=True)
                    target, old = binary / "omp", home / "tern/bin/omp"
                    aside = home / ".local/share/agent-assets/omp/omp.previous"
                    old.parent.mkdir(parents=True)
                    old.write_text("#!/bin/sh\necho omp/0.0.1\n")
                    links = {
                        "dangling": home / "gone/omp",
                        "external": old,
                        "foreign": home / "other/lib/node_modules/@oh-my-pi/pi-coding-agent/bin/omp",
                        "npm": npm_link,
                    }
                    if entry in links:
                        target.symlink_to(links[entry])
                    elif entry == "file":
                        target.write_text("#!/bin/sh\necho omp/0.0.1\n")
                    elif entry == "directory":
                        target.mkdir()
                    result = self.update_omp_in(home, version)
                    output = result.stdout + result.stderr
                    moved = entry in ("dangling", "external", "foreign", "file")
                    self.assertEqual(version == "0.0.1" or entry == "directory", result.returncode != 0, output)
                    self.assertEqual(entry == "directory", "EEXIST" in output, output)
                    if entry in ("dangling", "external", "foreign"):
                        self.assertIn(str(links[entry]), result.stdout)
                    if entry == "directory":
                        self.assertTrue(target.is_dir())
                    elif version == "18.11.3" or not moved:
                        self.assertEqual(npm_link, target.readlink(), output)
                        self.assertEqual(moved, aside.is_symlink() or aside.is_file(), output)
                    elif entry == "file":  # the failed install puts the previous entry back as it was
                        self.assertEqual("#!/bin/sh\necho omp/0.0.1\n", target.read_text(), output)
                    else:
                        self.assertEqual(links[entry], target.readlink(), output)

    def assert_npm_s_link_stays_under_a_home_with_a_trailing_slash(self, link):
        # npm folds HOME as it folds the link (Node's path.resolve), so with HOME=<home>/ npm's own link stays put.
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            target = home / ".local/bin/omp"
            target.parent.mkdir(parents=True)
            target.symlink_to(link.format(home=home))
            result = self.update_omp_in(home, "18.11.3", spelling="/")
            output = result.stdout + result.stderr
            self.assertEqual(0, result.returncode, output)
            self.assertNotIn("Moving", result.stdout)
            self.assertFalse((home / ".local/share/agent-assets/omp/omp.previous").is_symlink(), output)

    def test_npm_s_own_absolute_link_stays_under_a_home_with_a_trailing_slash(self):
        # baseline:update-agent-assets.sh:R1:1c780a5: an absolute link restarts the path inside the normaliser.
        self.assert_npm_s_link_stays_under_a_home_with_a_trailing_slash(
            "{home}/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/bin/omp"
        )

    def test_npm_s_own_relative_link_stays_under_a_home_with_a_trailing_slash(self):
        # baseline:update-agent-assets.sh:R1:1d5afaf: the package prefix is folded as the link is.
        self.assert_npm_s_link_stays_under_a_home_with_a_trailing_slash(
            "../lib/node_modules/@oh-my-pi/pi-coding-agent/bin/omp"
        )

    def test_the_platform_cases_read_no_path_operand(self):
        # baseline:update-agent-assets.sh:R2:851db69, both rows: `uname -s` and `uname -m` form a platform pair, not a
        # path, so ensure_crit_cli (row 1) and update_hcom (row 2) join them with `-` and the comparison lint reads no
        # path operand in either case statement.
        lint = [sys.executable, "-I", str(ROOT / "scripts/lint-comparisons.py"), "--all", "--baseline", os.devnull]
        result = subprocess.run(lint + [str(UPDATER)], capture_output=True, text=True, timeout=30, check=True)
        lines = UPDATER.read_text().split("\n")
        flagged = [lines[int(n) - 1].strip() for n in re.findall(r":(\d+): R2 ", result.stdout)]
        self.assertEqual([], [line for line in flagged if "uname" in line])

    def test_omp_version_check_accepts_the_branded_omp_slash_version_form(self):
        for output, valid in (
            ("omp/18.11.3", True),
            ("18.11.3", True),
            ("other/18.11.3", False),
            ("omp/omp/18.11.3", False),
            ("omp/18.11.3-extra", False),
        ):
            with self.subTest(output=output), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / ".local/bin/omp"
                target.parent.mkdir(parents=True)
                target.write_text(f"#!/bin/sh\nprintf '%s\\n' '{output}'\n")
                target.chmod(0o755)
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        'source "$1"; OMP_PIN_VERSION=18.11.3; has_command() { return 0; }; curl() { return 42; }; update_omp',
                        "bash",
                        str(UPDATER),
                    ],
                    env=os.environ | {"HOME": directory},
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0 if valid else 42, result.returncode, result.stdout + result.stderr)
                self.assertEqual(valid, "already installed" in result.stdout)

    def test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin(self):
        for platform in PLATFORMS:
            with self.subTest(platform=platform):
                self.exercise_update("hcom", platform)
        self.exercise_update("hcom", "Plan9/unknown", unsupported=True)

    def test_update_hcom_keeps_the_wheel_uv_records_as_its_source(self):
        # local:b49da6d:1: `uv tool upgrade` re-reads the wheel uv's receipt names, so the verified wheel stays at the
        # managed path and the asset manifest lists it; exercise_update asserts the path, its hash and the entry.
        self.exercise_update("hcom", "Darwin/arm64")

    def update_pinned_hcom(self, home, uv=":"):
        # update_hcom over an hcom installed at the pin; curl, uv and uname are shell functions that log to $CALLS.
        hcom = home / ".local/bin/hcom"
        hcom.parent.mkdir(parents=True, exist_ok=True)
        hcom.write_text("#!/bin/sh\nprintf 'hcom 0.7.30\\n'\n")
        hcom.chmod(0o755)
        payload = "reproduced wheel bytes; no real package\n"
        digest = hashlib.sha256(payload.encode()).hexdigest()
        stubs = (
            "HCOM_PIN_VERSION=0.7.30; HCOM_LINUX_AMD64_URL=https://fixture.invalid/hcom-0.7.30-py3-none-any.whl; "
            f"HCOM_LINUX_AMD64_SHA256={digest}; has_command() {{ return 0; }}; manifest_record() {{ :; }}; "
            'uname() { if [ "$1" = -s ]; then echo Linux; else echo x86_64; fi; }; '
            'curl() { printf %s "$PAYLOAD" > "${@: -1}"; echo curl >> "$CALLS"; }; '
            f'uv() {{ echo "uv $*" >> "$CALLS"; {uv}; }}; '
        )
        result = subprocess.run(
            ["bash", "-c", 'source "$1"; ' + stubs + "update_hcom", "bash", str(UPDATER)],
            env=os.environ | {"HOME": str(home), "PAYLOAD": payload, "CALLS": str(home / "calls")},
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return result, digest

    def test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel(self):
        # The Bot's P2 4303212227: an hcom installed at the pin before the wheel was kept has a receipt that names a
        # deleted temporary wheel, so the version alone does not skip it; once the wheel is retained it is skipped.
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            log, wheel = home / "calls", home / ".local/share/agent-assets/hcom/hcom-0.7.30-py3-none-any.whl"
            repaired, digest = self.update_pinned_hcom(home)
            self.assertEqual(0, repaired.returncode, repaired.stdout + repaired.stderr)
            self.assertNotIn("already installed", repaired.stdout)
            self.assertEqual(["curl", f"uv tool install --force {wheel}"], log.read_text().splitlines())
            self.assertEqual(digest, hashlib.sha256(wheel.read_bytes()).hexdigest())
            log.write_text("")
            skipped, _ = self.update_pinned_hcom(home)
            self.assertEqual(0, skipped.returncode, skipped.stdout + skipped.stderr)
            self.assertIn("hcom 0.7.30 is already installed", skipped.stdout)
            self.assertEqual("", log.read_text())

    def test_update_hcom_drops_the_retained_wheel_when_uv_fails_so_the_next_run_retries(self):
        # The Bot's P2 4303338055 (local:9842d91:1, audit:9842d91:1): when `uv tool install --force` fails after the
        # verified wheel moved into place, the next run retries instead of skipping on the wheel its guard reads.
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            log, wheel = home / "calls", home / ".local/share/agent-assets/hcom/hcom-0.7.30-py3-none-any.whl"
            failed, _ = self.update_pinned_hcom(home, uv="false")
            self.assertNotEqual(0, failed.returncode)
            self.assertFalse(wheel.exists(), failed.stdout + failed.stderr)
            log.write_text("")
            retried, _ = self.update_pinned_hcom(home)
            self.assertEqual(0, retried.returncode, retried.stdout + retried.stderr)
            self.assertEqual(["curl", f"uv tool install --force {wheel}"], log.read_text().splitlines())

    def test_updates_use_managed_binaries_when_path_is_shadowed(self):
        for tool in ("omp", "hcom"):
            for shadow_version in ("pin", "0.0.0"):
                with self.subTest(tool=tool, shadow_version=shadow_version):
                    self.exercise_update(tool, shadow_version=shadow_version)


class ProducerFailureTest(unittest.TestCase):
    """A producer whose read fails stops its step with a message naming it, before anything is downloaded."""

    def run_updater(self, body, home, **env):
        return subprocess.run(
            ["bash", "-c", 'source "$1"; ' + body, "bash", str(UPDATER)],
            env=os.environ | scratch_env(home) | {"CALLS": str(home / "calls")} | env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def test_a_failed_dirname_stops_the_updater_before_any_step(self):
        # A failed dirname used to resolve the source root to /, which then failed as "not found" without naming it.
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            stub = home / "bin/dirname"
            stub.parent.mkdir()
            stub.write_text("#!/usr/bin/env bash\nexit 1\n")
            stub.chmod(0o755)
            env = {k: v for k, v in os.environ.items() if k != "DOTFILES_SOURCE_DIR"}
            result = subprocess.run(
                ["bash", "-c", 'source "$1"; echo sourced', "bash", str(UPDATER)],
                env=env | {"HOME": str(home), "PATH": f"{stub.parent}:/usr/bin:/bin"},
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertEqual(f"dirname failed on {UPDATER}; the dotfiles source root is unknown.\n", result.stderr)
            self.assertNotIn("sourced", result.stdout)

    def test_a_failed_uname_stops_every_platform_step_before_a_download(self):
        for step in ("ensure_crit_cli", "update_terminal_code", "update_terminal_browser", "update_hcom"):
            with self.subTest(step=step), tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                result = self.run_updater(
                    'uname() { return 1; }; curl() { echo curl >> "$CALLS"; }; has_command() { return 0; }; ' + step,
                    home,
                )
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertEqual("uname -s failed; the platform is unknown.\n", result.stderr)
                self.assertNotIn("unsupported platform", result.stdout)
                self.assertFalse((home / "calls").exists())

    def test_update_omp_moves_nothing_and_installs_nothing_when_the_package_path_cannot_be_normalised(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            entry = home / ".local/bin/omp"
            entry.parent.mkdir(parents=True)
            entry.write_text("#!/bin/sh\nexit 1\n")
            entry.chmod(0o755)
            payload = "reproduced tarball bytes; no real package\n"
            digest = hashlib.sha256(payload.encode()).hexdigest()
            result = self.run_updater(
                f"OMP_TARBALL_SHA256={digest}; has_command() {{ return 0; }}; "
                'curl() { printf %s "$PAYLOAD" > "${@: -1}"; }; '
                'npm() { echo "npm $*" >> "$CALLS"; }; '
                'normalize_node_path() { [ "$#" -eq 2 ] && printf "%s\\n" "$1" || return 1; }; '
                "update_omp",
                home,
                PAYLOAD=payload,
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertTrue(entry.is_file())
            self.assertFalse((home / ".local/share/agent-assets/omp/omp.previous").exists())
            self.assertFalse((home / "calls").exists())

    def test_the_bridge_inputs_are_refused_when_a_patch_cannot_be_hashed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_updater("shasum() { return 1; }; pi_claude_bridge_inputs", Path(directory))
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertRegex(
                result.stderr, r"^shasum -a 256 could not hash \S+; the pi-claude-bridge inputs are unknown\n$"
            )

    def test_update_compactiondb_records_no_step_when_its_changelog_cannot_be_read(self):
        with tempfile.TemporaryDirectory() as directory:
            home, source = Path(directory) / "home", Path(directory) / "source"
            (source / "vendor/compactiondb").mkdir(parents=True)
            (source / "scripts").symlink_to(ROOT / "scripts")
            home.mkdir()
            result = self.run_updater(
                'rsync() { :; }; manifest_record() { echo "manifest_record $*" >> "$CALLS"; }; update_compactiondb',
                home,
                DOTFILES_SOURCE_DIR=str(source),
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"Cannot read the CompactionDB version from {source}/vendor/compactiondb/CHANGELOG.md.", result.stderr
            )
            self.assertFalse((home / "calls").exists())

    # A fake claude over the files Claude Code keeps: ~/.claude/plugins/installed_plugins.json, the user and
    # project settings (`enabledPlugins`) and a marketplace list. `plugin list --json` reports enabled the way
    # Claude Code does, from the current directory's project settings over the user settings, so a decision
    # taken from it follows the directory. Calls are logged with the directory they ran in.
    FAKE_CLAUDE = r"""
claude() {
    printf '%s\t%s\n' "$*" "${PWD}" >> "${WORK}/calls"
    local user="${HOME}/.claude/settings.json" record="${HOME}/.claude/plugins/installed_plugins.json" settings
    case "$1 $2 $3" in
    "plugin list --json")
        jq --slurpfile user "${user}" --slurpfile here <(cat "${PWD}/.claude/settings.json" 2> /dev/null || echo '{}') \
            '[.plugins | to_entries[] | .key as $id | .value[] | {id: $id, scope, version,
              enabled: (($here[0].enabledPlugins // {}) as $p | ($user[0].enabledPlugins // {}) as $u
                | if ($p | has($id)) then $p[$id] else ($u[$id] == true) end)}]' "${record}" ;;
    "plugin marketplace list") if [ -n "${LIST_FAILS}" ]; then printf 'Error: %s\n' "${LIST_FAILS}" >&2; return 1; fi
        cat "${WORK}/markets.json" ;;
    "plugin marketplace add") [ -z "${ADD_FAILS}" ] || return 1
        jq --arg name "${ADD_NAME}" --arg repo "$4" '. + [{name: $name, source: "github", repo: $repo}]' "${WORK}/markets.json" > "${WORK}/next" && mv "${WORK}/next" "${WORK}/markets.json" ;;
    "plugin install "*) [ -z "${INSTALL_FAILS}" ] || return 1
        jq --arg id "$3" --arg version "${INSTALL_VERSION}" --arg home "${HOME}" \
            '.plugins[$id] += [{scope: "user", version: $version, installPath: "\($home)/.claude/plugins/cache/\($id | split("@")[1])/\($id | split("@")[0])/\($version)"}]' \
            "${record}" > "${WORK}/next" && mv "${WORK}/next" "${record}"
        jq --arg id "$3" '.enabledPlugins[$id] = true' "${user}" > "${WORK}/next" && mv "${WORK}/next" "${user}"
        if [ -n "${INSTALL_CONTENT}" ]; then
            mkdir -p "${HOME}/.claude/plugins/cache/${3#*@}/${3%@*}"
            cp -R "${INSTALL_CONTENT}" "${HOME}/.claude/plugins/cache/${3#*@}/${3%@*}/${INSTALL_VERSION}"
        fi
        [ -z "${CORRUPT_AFTER}" ] || printf '{truncated' > "${record}" ;;
    "plugin update "*) [ -z "${UPDATE_FIXES}" ] || chmod -R u+rwX "${HOME}/.claude/plugins/cache"
        [ -z "${CORRUPT_AFTER}" ] || printf '{truncated' > "${record}" ;;
    "plugin disable "*) [ -z "${DISABLE_FAILS}" ] || return 1; [ -z "${DISABLE_NOOP}" ] || return 0
        settings="${user}"; [ "$5" = user ] || settings="${PWD}/.claude/settings.json"
        jq --arg id "$3" '.enabledPlugins[$id] = false' "${settings}" > "${WORK}/next" && mv "${WORK}/next" "${settings}" ;;
    esac
}
"""

    def converge_listed(self, step, installs, enabled, markets=None, project=None, cwd=None, catalog=None, **flags):
        """Run STEP against the fake: INSTALLS {id: [{scope, version, projectPath?}]}, user ENABLED {id: bool},
        PROJECT {id: bool} as the enabledPlugins of a project directory (work/project), CWD "project" to run there."""
        work = Path(tempfile.mkdtemp(prefix="converge-listed-"))
        self.addCleanup(shutil.rmtree, work)
        home = work / "home"
        (home / ".claude/plugins").mkdir(parents=True)
        # The installed marketplace clones a content pin reads its catalog entry from: the reviewed ones, or the
        # CATALOG entries {marketplace: [entry, ...]} a test serves instead.
        shutil.copytree(REVIEWED / "marketplaces", home / ".claude/plugins/marketplaces")
        for name, entries in (catalog or {}).items():
            clone = home / ".claude/plugins/marketplaces" / name / ".claude-plugin/marketplace.json"
            clone.write_text(json.dumps({"name": name, "plugins": entries}))
        project_dir = work / "project"
        (project_dir / ".claude").mkdir(parents=True)
        (project_dir / ".claude/settings.json").write_text(json.dumps({"enabledPlugins": project or {}}))
        # A copy: a test may reuse one INSTALLS across runs, each with its own home.
        installs = json.loads(json.dumps(installs)) if isinstance(installs, dict) else installs
        for plugin_id, entries in installs.items() if isinstance(installs, dict) else []:
            plugin, marketplace = plugin_id.split("@", 1)
            for entry in entries:
                # The shape Claude Code writes: installPath names the plugin's own cache directory.
                entry.setdefault(
                    "installPath", f"{home}/.claude/plugins/cache/{marketplace}/{plugin}/{entry['version']}"
                )
                # The reviewed copy (claude_plugin_fixture) for a plugin pinned by content.
                if entry.pop("reviewed", False):
                    shutil.copytree(REVIEWED / plugin, entry["installPath"])
                if entry.get("projectPath") == "PROJECT":
                    entry["projectPath"] = str(project_dir)
        record = home / ".claude/plugins/installed_plugins.json"
        record.write_text(installs if isinstance(installs, str) else json.dumps({"version": 2, "plugins": installs}))
        (home / ".claude/settings.json").write_text(json.dumps({"enabledPlugins": enabled}))
        pins = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"]
        foreign = flags.pop("FOREIGN", "")
        sources = {plugin_id.split("@", 1)[1]: foreign or pin["marketplace"] for plugin_id, pin in pins.items()}
        names = list(sources) if markets is None else markets
        listing = [{"name": name, "source": "github", "repo": sources[name]} for name in names]
        (work / "markets.json").write_text(json.dumps(listing))
        variables = (
            "ADD_FAILS",
            "ADD_NAME",
            "INSTALL_FAILS",
            "INSTALL_VERSION",
            "DISABLE_FAILS",
            "DISABLE_NOOP",
            "CORRUPT_AFTER",
            "LIST_FAILS",
            "INSTALL_CONTENT",
            "UPDATE_FIXES",
        )
        result = subprocess.run(
            [
                "bash",
                "-c",
                f'source "$1"; has_command() {{ return 0; }}; {self.FAKE_CLAUDE.strip()}\n{step}',
                "bash",
                str(UPDATER),
            ],
            env=os.environ | {name: "" for name in variables} | scratch_env(home) | {"WORK": str(work)} | flags,
            cwd=project_dir if cwd == "project" else work,  # lint-comparisons: allow cwd is a mode keyword, not a path
            text=True,
            capture_output=True,
            check=False,
        )
        lines = (work / "calls").read_text().splitlines() if (work / "calls").exists() else []
        calls = []
        for line in lines:
            call, directory = line.split("\t", 1)
            if call.startswith(("plugin list", "plugin marketplace list")):
                continue
            resolved = os.path.realpath(directory)
            if resolved == os.path.realpath(project_dir):
                where = "project"
            else:
                where = "neutral" if "claude-neutral." in resolved else resolved
            calls.append(f"{call} @{where}")
        state = {
            "user": json.loads((home / ".claude/settings.json").read_text())["enabledPlugins"],
            "project": json.loads((project_dir / ".claude/settings.json").read_text())["enabledPlugins"],
        }
        return result, calls, state

    def pin_of(self, plugin_id: str) -> str:
        return json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"][plugin_id]["pin"]

    def test_a_claude_plugin_stays_at_its_recorded_pin(self):
        pin = self.pin_of("crit@crit")
        step = 'converge_claude_plugin "crit@crit"'
        # At its pin: nothing is installed, updated or toggled, so make update no longer takes the newest release.
        at_pin = {"crit@crit": [{"scope": "user", "version": pin}]}
        result, calls, _ = self.converge_listed(step, at_pin, {"crit@crit": True})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], calls)

        # Off its pin and still off after the update: disabled, proven from the user settings file.
        newer = {"crit@crit": [{"scope": "user", "version": "999.0.0"}]}
        result, calls, state = self.converge_listed(step, newer, {"crit@crit": True})
        self.assertEqual(1, result.returncode, result.stderr)  # disabled, and still drift for the doctor
        self.assertEqual(
            ["plugin update crit@crit --scope user @neutral", "plugin disable crit@crit --scope user @neutral"], calls
        )
        self.assertIs(False, state["user"]["crit@crit"])
        self.assertIn(f"not its pin {pin}", result.stderr)

    def test_a_project_override_does_not_hide_a_globally_enabled_off_pin_plugin(self):
        # The current directory's project settings disable crit, so `claude plugin list` there reports it
        # disabled; the user settings still enable the off-pin release everywhere else.
        installs = {"crit@crit": [{"scope": "user", "version": "999.0.0"}]}
        result, calls, state = self.converge_listed(
            'converge_claude_plugin "crit@crit"',
            installs,
            {"crit@crit": True},
            project={"crit@crit": False},
            cwd="project",
        )
        self.assertEqual(1, result.returncode, result.stderr)  # disabled at user scope; still drift for the doctor
        # Every claude call runs outside the project, and the user-scope disable is what the user file shows.
        self.assertIn("plugin disable crit@crit --scope user @neutral", calls)
        self.assertTrue(all(call.endswith("@neutral") for call in calls), calls)
        self.assertIs(False, state["user"]["crit@crit"])

    def test_only_the_user_scope_installation_is_managed(self):
        pin = self.pin_of("crit@crit")
        step = 'converge_claude_plugin "crit@crit"'
        # A project-scope copy belongs to its project: reported as not managed, never converged.
        installs = {
            "crit@crit": [
                {"scope": "user", "version": pin},
                {"scope": "project", "version": "999.0.0", "projectPath": "PROJECT"},
            ]
        }
        result, calls, state = self.converge_listed(step, installs, {"crit@crit": True}, project={"crit@crit": True})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], calls)
        self.assertIn("installed in project scope at", result.stderr)
        self.assertIn(": not managed", result.stderr)
        self.assertIs(True, state["project"]["crit@crit"])

        # A project-only installation is not the user-scope one this repository installs: that is installed.
        installs = {"crit@crit": [{"scope": "project", "version": pin, "projectPath": "PROJECT"}]}
        result, calls, _ = self.converge_listed(step, installs, {}, INSTALL_VERSION=pin)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["plugin install crit@crit --scope user @neutral"], calls)

    def test_an_off_pin_plugin_counts_as_disabled_only_when_the_user_settings_disable_it(self):
        step = 'converge_claude_plugin "crit@crit"'
        installs = {"crit@crit": [{"scope": "user", "version": "999.0.0"}]}
        # A disable that changes nothing: still enabled, not named at all (the plugin's default applies), or a
        # value that only looks false: the JSON string "false", 0 or null is not the boolean false.
        for enabled in ({"crit@crit": True}, {}, {"crit@crit": "false"}, {"crit@crit": 0}, {"crit@crit": None}):
            with self.subTest(enabled=enabled):
                result, calls, _ = self.converge_listed(step, installs, enabled, DISABLE_NOOP="1")
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("plugin disable crit@crit --scope user @neutral", calls)
                # Not the boolean false: either not disabled, or a value the strict reader refuses.
                self.assertRegex(result.stderr, "does not disable it|enabledPlugins.crit@crit: must be a boolean")

    def test_a_marketplace_that_cannot_be_registered_fails_an_off_pin_plugin(self):
        # Failure injection: the existing off-pin installation is still disabled, and the run fails.
        installs = {"crit@crit": [{"scope": "user", "version": "999.0.0"}]}
        result, calls, state = self.converge_listed(
            'converge_claude_plugin "crit@crit"', installs, {"crit@crit": True}, markets=[], ADD_FAILS="1"
        )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("claude plugin marketplace add tomasz-tomczyk/crit failed", result.stderr)
        self.assertIn("plugin disable crit@crit --scope user @neutral", calls)
        self.assertIs(False, state["user"]["crit@crit"])

    def test_a_forged_install_row_cannot_pass_an_off_pin_plugin(self):
        # A project entry whose projectPath carries "\nuser\t<pin>\t" came first, so a tab/newline reader took
        # it for the user row at the pin and left the off-pin user copy enabled.
        pin = self.pin_of("crit@crit")
        forged = {"scope": "project", "version": pin, "projectPath": f"/w\nuser\t{pin}\t"}
        installs = {"crit@crit": [forged, {"scope": "user", "version": "999.0.0"}]}
        result, calls, state = self.converge_listed('converge_claude_plugin "crit@crit"', installs, {"crit@crit": True})
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("projectPath: contains a control character", result.stderr)
        self.assertNotIn("is at its pin", result.stdout)

    def test_duplicate_user_records_are_refused(self):
        # Audit round 18: two user-scope records [pin, 99.0.0] let `first()` pick the pin while the doctor saw drift.
        pin = self.pin_of("crit@crit")
        installs = {"crit@crit": [{"scope": "user", "version": pin}, {"scope": "user", "version": "99.0.0"}]}
        result, calls, _ = self.converge_listed('converge_claude_plugin "crit@crit"', installs, {"crit@crit": True})
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("a second user-scope record", result.stderr)
        self.assertEqual(["plugin disable crit@crit --scope user @neutral"], calls)

    def test_any_drift_the_doctor_reports_after_a_step_fails_the_run(self):
        # The updater's own reading says "at the pin", but the doctor's check sees drift: the doctor wins.
        pin = self.pin_of("crit@crit")
        installs = {"crit@crit": [{"scope": "user", "version": pin}]}
        step = (
            "doctor_pin_check() { printf 'ERROR: injected drift\\n' >&2; return 1; }; "
            'converge_claude_step "crit@crit" || true; fail_on_claude_pin_failures'
        )
        result, _, _ = self.converge_listed(step, installs, {"crit@crit": True})
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("make doctor still reports crit@crit off its pin", result.stderr)
        self.assertIn("could not be checked or kept at their pin", result.stderr)
        # And with the real check, an at-pin plugin passes.
        result, _, _ = self.converge_listed('converge_claude_plugin "crit@crit"', installs, {"crit@crit": True})
        self.assertEqual(0, result.returncode, result.stderr)

    def test_a_record_unreadable_after_install_or_update_disables_the_plugin(self):
        # Audit round 22: the re-read after the change failed and the step returned before any disable, so the
        # release just installed or updated to (never reviewed) stayed enabled.
        cases = (
            ("install", {}, {}, {"INSTALL_VERSION": "999.0.0"}),
            ("update", {"crit@crit": [{"scope": "user", "version": "999.0.0"}]}, {"crit@crit": True}, {}),
        )
        step = 'converge_claude_step "crit@crit" || true; fail_on_claude_pin_failures'
        for action, installs, enabled, flags in cases:
            with self.subTest(action=action):
                result, calls, state = self.converge_listed(step, installs, enabled, CORRUPT_AFTER="1", **flags)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("cannot re-read the installation records of crit@crit", result.stderr)
                self.assertEqual(
                    [
                        f"plugin {action} crit@crit --scope user @neutral",
                        "plugin disable crit@crit --scope user @neutral",
                    ],
                    calls,
                )
                self.assertIs(False, state["user"]["crit@crit"])

    def test_every_way_out_of_a_step_disables_the_plugin(self):
        # One rule: anything but a step and a doctor's check that both pass ends in the disable, including an
        # `exit` or a set -u abort inside the step, and a pass of the step the doctor does not confirm.
        pin = self.pin_of("crit@crit")
        installs = {"crit@crit": [{"scope": "user", "version": pin}]}
        for name, body in (
            ("return", "step() { return 4; }"),
            ("exit", "step() { exit 5; }"),
            ("unbound", 'step() { printf "%s" "${NOT_SET_ANYWHERE}"; }'),
            ("doctor", "step() { :; }; doctor_pin_check() { return 2; }"),
        ):
            with self.subTest(way=name):
                gate = f'{body}; converge_or_disable claude crit@crit step; printf "rc=%s failures=%s\\n" "$?" "${{CLAUDE_PIN_FAILURES}}"'
                result, calls, state = self.converge_listed(f"set +e; {gate}", installs, {"crit@crit": True})
                self.assertIn("rc=1 failures=1", result.stdout, result.stderr)
                self.assertEqual(["plugin disable crit@crit --scope user @neutral"], calls)
                self.assertIs(False, state["user"]["crit@crit"])
        # A step and a check that both pass leave the plugin as it is.
        result, calls, state = self.converge_listed(
            "step() { :; }; converge_or_disable claude crit@crit step", installs, {"crit@crit": True}
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], calls)
        self.assertIs(True, state["user"]["crit@crit"])

    def test_a_codex_plugin_that_misses_its_pin_is_removed(self):
        # Codex has no disable command and chezmoi keeps [plugins."<id>"] enabled, so the copy is removed.
        work = Path(tempfile.mkdtemp(prefix="codex-disable-"))
        self.addCleanup(shutil.rmtree, work)
        body = (
            'codex() { printf "%s\\n" "$*" >> "${WORK}/calls"; [ "$1 $2" != "plugin remove" ] || : > "${WORK}/removed"; }; '
            'codex_plugin_copy() { if [ -e "${WORK}/removed" ]; then echo absent; else echo "copy 5.3.2"; fi; }; '
            "doctor_pin_check() { return 1; }; "
        )
        for name, extra, expected in (
            ("drift", "", ["plugin remove ponytail@ponytail"]),
            ("remove leaves a copy", 'codex_plugin_copy() { echo "copy 5.3.2"; }; ', None),
        ):
            with self.subTest(case=name):
                for leftover in ("calls", "removed"):
                    (work / leftover).unlink(missing_ok=True)
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        f'source "$1"; set +e; {body}{extra}converge_or_disable codex ponytail@ponytail true; echo "rc=$?"',
                        "bash",
                        str(UPDATER),
                    ],
                    env=os.environ | scratch_env(work / "home") | {"WORK": str(work)},
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertIn("rc=1", result.stdout, result.stderr)
                self.assertEqual(["plugin remove ponytail@ponytail"], (work / "calls").read_text().splitlines())
                if expected is None:
                    self.assertIn("codex plugin remove left a copy", result.stderr)
                else:
                    self.assertIn("was removed", result.stderr)

    def test_a_codex_copy_unreadable_after_install_removes_it_and_fails_the_run(self):
        # The Codex side of round 22: `codex plugin add` leaves a copy whose plugin.json cannot be read, so the
        # doctor's real check fails, the copy is removed, and the run fails.
        work = Path(tempfile.mkdtemp(prefix="codex-unreadable-"))
        self.addCleanup(shutil.rmtree, work)
        cache = work / "home/.codex/plugins/cache/openai-curated/superpowers"
        fake = (
            'codex() { printf "%s\\n" "$*" >> "${WORK}/calls"; case "$1 $2" in '
            '"plugin add") mkdir -p "${CACHE}/6.3.0/.codex-plugin"; printf "{truncated" > "${CACHE}/6.3.0/.codex-plugin/plugin.json" ;; '
            '"plugin remove") rm -rf "${CACHE}" ;; esac; }'
        )
        result = subprocess.run(
            [
                "bash",
                "-c",
                f'source "$1"; has_command() {{ return 0; }}; {fake}\nupdate_codex_superpowers; fail_on_claude_pin_failures',
                "bash",
                str(UPDATER),
            ],
            env=os.environ | scratch_env(work / "home") | {"WORK": str(work), "CACHE": str(cache)},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual(
            ["plugin add superpowers@openai-curated", "plugin remove superpowers@openai-curated"],
            (work / "calls").read_text().splitlines(),
        )
        self.assertFalse(cache.exists())

    def test_every_plugin_install_or_update_runs_only_through_converge_or_disable(self):
        # Structural guard: a function that installs, updates or upgrades a Claude Code or Codex plugin is
        # called nowhere but as the step of converge_or_disable, so no path skips the disable.
        text = UPDATER.read_text()
        bodies = dict(re.findall(r"^function (\w+)\(\) \(?\{\n(.*?)^\}", text, re.M | re.S))
        actions = re.compile(r"plugin (install|update) |codex plugin (add|marketplace upgrade) ")
        # Code only: the manifest's command strings and comments name these actions without running them.
        code = {name: re.sub(r'"[^"\n]*"|#.*', "", body) for name, body in bodies.items()}
        movers = sorted(name for name, body in code.items() if actions.search(body))
        self.assertEqual(["install_codex_ponytail", "install_codex_superpowers", "move_claude_plugin_to_pin"], movers)
        for name in movers:
            uses = [line.strip() for line in text.splitlines() if re.search(rf"\b{name}\b", line)]
            calls = [line for line in uses if not line.startswith(("function ", "#"))]
            self.assertTrue(calls, name)
            self.assertEqual(
                [], [line for line in calls if not re.search(rf"converge_or_disable \w+ \S+ {name}\b", line)]
            )

    # Round 27: the run fails only when unreviewed code could be active or the active state cannot be verified.
    ALL_CLAUDE_STEPS = (
        "ensure_crit_cli() { :; }; update_claude_superpowers; update_claude_crit; update_claude_ponytail; "
        'update_claude_understand_anything; converge_claude_plugins; printf "failures=%s\\n" "${CLAUDE_PIN_FAILURES}"; '
        "fail_on_claude_pin_failures"
    )

    def test_a_fresh_host_whose_marketplace_list_fails_skips_every_plugin_with_a_warning(self):
        # CI public-bootstrap (ubuntu-24.04): `claude plugin marketplace list --json` failed on a fresh HOME, so
        # every plugin was disabled and counted and the bootstrap failed, with nothing installed or enabled.
        pins = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"]
        result, calls, _ = self.converge_listed(self.ALL_CLAUDE_STEPS, {}, {}, LIST_FAILS="sandbox unavailable")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertEqual([], calls)  # nothing added, installed, updated or disabled
        self.assertIn("Error: sandbox unavailable", result.stderr)  # the CLI's own stderr is shown
        for plugin_id in pins:
            self.assertIn(f"WARN: claude plugin {plugin_id} was not installed", result.stderr)
        # An installed or enabled plugin that cannot be verified still fails, and an installed one is disabled.
        for name, installs, enabled in (
            (
                "installed at its pin",
                {"crit@crit": [{"scope": "user", "version": pins["crit@crit"]["pin"]}]},
                {"crit@crit": True},
            ),
            ("enabled, not installed", {}, {"crit@crit": True}),
            (
                "project scope only",
                {"crit@crit": [{"scope": "project", "version": "9.9.9", "projectPath": "PROJECT"}]},
                {},
            ),
        ):
            with self.subTest(case=name):
                step = "converge_claude_step crit@crit || true; fail_on_claude_pin_failures"
                result, calls, _ = self.converge_listed(step, installs, enabled, LIST_FAILS="sandbox unavailable")
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("not installed or updated from an unverified marketplace", result.stderr)
                if name == "installed at its pin":
                    self.assertEqual(["plugin disable crit@crit --scope user @neutral"], calls)

    def test_a_fresh_install_that_lands_off_its_pin_is_disabled_and_warned_not_failed(self):
        # CI public-bootstrap (macos-15): pstack's marketplace had moved to 0.15.32 past the 0.15.30 pin, and
        # Claude Code installs only the current release.
        pin = self.pin_of("pstack@cursor-plugins")
        step = 'converge_claude_step pstack@cursor-plugins || true; printf "failures=%s\\n" "${CLAUDE_PIN_FAILURES}"; fail_on_claude_pin_failures'
        result, calls, state = self.converge_listed(step, {}, {}, INSTALL_VERSION="99.0.0")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertEqual(
            [
                "plugin install pstack@cursor-plugins --scope user @neutral",
                "plugin disable pstack@cursor-plugins --scope user @neutral",
            ],
            calls,
        )
        self.assertIs(False, state["user"]["pstack@cursor-plugins"])
        self.assertIn(
            f"pstack@cursor-plugins is at 99.0.0, not its pin {pin}; the pin needs a review bump", result.stderr
        )
        self.assertIn(
            "landed off its pin on a fresh install and is proven disabled (Claude) or removed (Codex)", result.stderr
        )
        # The doctor still reports the copy as drift: that is the signal for the bump.
        self.assertIn("installed at 99.0.0, not its pin", result.stderr)
        # Still a failure: a disable that cannot be proven, an earlier enable, or an installation that was there.
        for name, installs, enabled, flags in (
            ("disable not proven", {}, {}, {"DISABLE_NOOP": "1"}),
            ("enabled before", {}, {"pstack@cursor-plugins": True}, {}),
            ("installed before", {"pstack@cursor-plugins": [{"scope": "user", "version": "98.0.0"}]}, {}, {}),
        ):
            with self.subTest(case=name):
                result, _, _ = self.converge_listed(step, installs, enabled, INSTALL_VERSION="99.0.0", **flags)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("failures=1", result.stdout)

    def content_fixture(self, text: str) -> Path:
        """A plugin tree like frontend-design's (prompt-only skill) whose content is TEXT."""
        root = Path(tempfile.mkdtemp(prefix="content-pin-")) / "plugin"
        self.addCleanup(shutil.rmtree, root.parent)
        (root / ".claude-plugin").mkdir(parents=True)
        (root / ".claude-plugin/plugin.json").write_text('{"name": "frontend-design"}\n')
        (root / "skills/frontend-design").mkdir(parents=True)
        (root / "skills/frontend-design/SKILL.md").write_text(text)
        return root

    @staticmethod
    def content_hash(root: Path) -> str:
        return subprocess.run(
            [
                "python3",
                "-I",
                str(ROOT / "scripts/pin_records.py"),
                "content-sha256",
                str(root),
                str(OFFICIAL_CLONE),
                "frontend-design",
            ],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

    def content_step(self, pin: str) -> str:
        # The pin under test replaces the recorded one; every other field still comes from plugin-pins.json. make
        # doctor's own pin check reads the recorded pins file, so here it repeats the comparison with this pin
        # (the doctor's side has its own test in test_check_agent_runtime).
        return (
            f'plugin_pin() {{ if [ "$3" = pin ]; then printf "%s\\n" "{pin}"; '
            'else pin_record plugin-pin "${AGENT_PLUGIN_PINS}" "$@"; fi; }; '
            'doctor_pin_check() { local installs observed; installs="$(claude_plugin_installs "$2")" && '
            f'observed="$(claude_user_observed "${{installs}}" "{pin}")" && [ "${{observed}}" = "{pin}" ]; }}; '
            "converge_claude_step frontend-design@claude-plugins-official || true; "
            'printf "failures=%s\\n" "${CLAUDE_PIN_FAILURES}"; fail_on_claude_pin_failures'
        )

    def test_a_content_pin_follows_the_files_not_the_commit_version(self):
        # U91: frontend-design's version is the marketplace commit, which moves with unrelated commits.
        plugin_id = "frontend-design@claude-plugins-official"
        reviewed = self.content_fixture("# Frontend Design\nreviewed\n")
        pin = self.content_hash(reviewed)
        self.assertRegex(pin, r"^sha256:[0-9a-f]{64}$")
        # Same content under a commit-version never seen before: installed fresh, left enabled.
        result, calls, state = self.converge_listed(
            self.content_step(pin), {}, {}, INSTALL_VERSION="bbbbbbbbbbbb", INSTALL_CONTENT=str(reviewed)
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertEqual([f"plugin install {plugin_id} --scope user @neutral"], calls)
        self.assertIs(True, state["user"][plugin_id])
        # One changed byte under that version: the existing off-pin path disables it and names both hashes.
        changed = self.content_fixture("# Frontend Design\nreviewes\n")
        result, calls, state = self.converge_listed(
            self.content_step(pin), {}, {}, INSTALL_VERSION="bbbbbbbbbbbb", INSTALL_CONTENT=str(changed)
        )
        self.assertEqual(0, result.returncode, result.stderr)  # a fresh install off its pin warns, as for versions
        self.assertEqual(f"plugin disable {plugin_id} --scope user @neutral", calls[-1])
        self.assertIs(False, state["user"][plugin_id])
        self.assertIn(f"is at {self.content_hash(changed)}, not its pin {pin}", result.stderr)
        # A symlink inside the installed copy cannot be hashed: the step fails and the plugin is disabled.
        (changed / "skills/link").symlink_to("/etc/hosts")
        result, calls, state = self.converge_listed(
            self.content_step(pin), {}, {}, INSTALL_VERSION="bbbbbbbbbbbb", INSTALL_CONTENT=str(changed)
        )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("is a symlink or special file", result.stderr)
        self.assertIs(False, state["user"][plugin_id])

    def test_a_catalog_entry_that_adds_runtime_behaviour_moves_the_plugin_off_its_pin(self):
        # Round-8 audit: with strict: false the catalog entry alone can define an LSP server, hooks or MCP servers,
        # so the pin covers the entry the installed marketplace clone serves, not only the plugin directory.
        plugin_id = "frontend-design@claude-plugins-official"
        entry = json.loads((OFFICIAL_CLONE / ".claude-plugin/marketplace.json").read_text())["plugins"][0]
        installs = {plugin_id: [{"scope": "user", "version": CONTENT_VERSION, "reviewed": True}]}
        step = self.content_step(self.pin_of(plugin_id))
        widened = {**entry, "strict": False, "lspServers": {"x": {"command": "x", "args": []}}}
        result, calls, state = self.converge_listed(
            step, installs, {plugin_id: True}, catalog={"claude-plugins-official": [widened]}
        )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("failures=1", result.stdout)
        self.assertIn(f"not its pin {self.pin_of(plugin_id)}", result.stderr)
        self.assertEqual(f"plugin disable {plugin_id} --scope user @neutral", calls[-1])
        self.assertIs(False, state["user"][plugin_id])
        # The reviewed entry with the same files is at its pin: nothing is called and it stays enabled.
        result, calls, state = self.converge_listed(step, installs, {plugin_id: True})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], calls)
        self.assertIs(True, state["user"][plugin_id])

    def test_a_content_hash_that_cannot_be_read_fails_the_step_before_any_update(self):
        # Round-3 audit: an unreadable installed copy used to trigger an update, and a later readable copy at the
        # pin then passed. An unknown pin state is a failure: no update, the plugin disabled, the step failed.
        if os.geteuid() == 0:
            self.skipTest("root reads a mode-0 file, so the read failure cannot be injected")
        plugin_id = "frontend-design@claude-plugins-official"
        copy = "${HOME}/.claude/plugins/cache/claude-plugins-official/frontend-design/cccccccccccc"
        step = f'chmod 0 "{copy}/README.md"; ' + self.content_step(self.pin_of(plugin_id))
        installs = {plugin_id: [{"scope": "user", "version": "cccccccccccc", "reviewed": True}]}
        # The fake's `plugin update` makes the copy readable again, so only an update could make it pass.
        result, calls, state = self.converge_listed(step, installs, {plugin_id: True}, UPDATE_FIXES="1")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("failures=1", result.stdout)
        self.assertIn("cannot read the installed content", result.stderr)
        self.assertEqual([f"plugin disable {plugin_id} --scope user @neutral"], calls)
        self.assertIs(False, state["user"][plugin_id])
        # The same copy readable is at its pin: nothing is called and it stays enabled.
        result, calls, state = self.converge_listed(
            self.content_step(self.pin_of(plugin_id)), installs, {plugin_id: True}
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], calls)
        self.assertIs(True, state["user"][plugin_id])

    def test_a_fresh_codex_install_that_lands_off_its_pin_is_removed_and_warned_not_failed(self):
        # Audit round 28: the round-27 rule covered Claude only. A fresh Codex copy off its pin is removed
        # (Codex has no disable) and proven gone, through the same converge_or_disable decision.
        pin = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["codex"]["superpowers@openai-curated"]["pin"]
        for name, before, expected_rc, failures in (
            ("fresh", None, 0, "0"),
            ("copy cached before", "98.0.0", 1, "1"),
        ):
            with self.subTest(case=name):
                work = Path(tempfile.mkdtemp(prefix="codex-fresh-"))
                self.addCleanup(shutil.rmtree, work)
                cache = work / "home/.codex/plugins/cache/openai-curated/superpowers"
                if before:
                    (cache / before / ".codex-plugin").mkdir(parents=True)
                    (cache / before / ".codex-plugin/plugin.json").write_text(
                        json.dumps({"name": "superpowers", "version": before})
                    )
                fake = (
                    'codex() { printf "%s\\n" "$*" >> "${WORK}/calls"; case "$1 $2" in '
                    '"plugin add") mkdir -p "${CACHE}/99.0.0/.codex-plugin"; '
                    'printf \'{"name": "superpowers", "version": "99.0.0"}\' > "${CACHE}/99.0.0/.codex-plugin/plugin.json" ;; '
                    '"plugin remove") rm -rf "${CACHE}" ;; esac; }'
                )
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        f'source "$1"; has_command() {{ return 0; }}; {fake}\nupdate_codex_superpowers; '
                        'printf "failures=%s\\n" "${CLAUDE_PIN_FAILURES}"; fail_on_claude_pin_failures',
                        "bash",
                        str(UPDATER),
                    ],
                    env=os.environ | scratch_env(work / "home") | {"WORK": str(work), "CACHE": str(cache)},
                    text=True,
                    capture_output=True,
                    check=False,
                )
                calls = (work / "calls").read_text().splitlines() if (work / "calls").exists() else []
                self.assertEqual(expected_rc, result.returncode, result.stderr)
                self.assertIn(f"failures={failures}", result.stdout)
                self.assertIn("plugin remove superpowers@openai-curated", calls)
                self.assertFalse(cache.exists())
                if before is None:
                    self.assertEqual(
                        ["plugin add superpowers@openai-curated", "plugin remove superpowers@openai-curated"], calls
                    )
                    self.assertIn(
                        f"superpowers@openai-curated is at 99.0.0, not its pin {pin}; the pin needs a review bump",
                        result.stderr,
                    )
                    self.assertIn(
                        "landed off its pin on a fresh install and is proven disabled (Claude) or removed (Codex)",
                        result.stderr,
                    )
                else:
                    self.assertNotIn("plugin add superpowers@openai-curated", calls)

    def test_a_codex_copy_with_an_empty_version_is_removed_not_read_as_absent(self):
        # U90: plugin.json `version: ""` printed a blank line, which disable_plugin took for "no copy", so the
        # removal was skipped. The reader refuses it, and only its explicit `absent` skips the removal.
        for version in ("", " ", "\u00a0"):
            with self.subTest(version=repr(version)):
                work = Path(tempfile.mkdtemp(prefix="codex-empty-"))
                self.addCleanup(shutil.rmtree, work)
                cache = work / "home/.codex/plugins/cache/ponytail/ponytail"
                (cache / "5.3.2/.codex-plugin").mkdir(parents=True)
                (cache / "5.3.2/.codex-plugin/plugin.json").write_text(
                    json.dumps({"name": "ponytail", "version": version})
                )
                fake = 'codex() { printf "%s\\n" "$*" >> "${WORK}/calls"; [ "$1 $2" != "plugin remove" ] || rm -rf "${CACHE}"; }'
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        f'source "$1"; set +e; {fake}\ndisable_plugin codex ponytail@ponytail; echo "rc=$?"',
                        "bash",
                        str(UPDATER),
                    ],
                    env=os.environ | scratch_env(work / "home") | {"WORK": str(work), "CACHE": str(cache)},
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(
                    ["plugin remove ponytail@ponytail"],
                    (work / "calls").read_text().splitlines() if (work / "calls").exists() else [],
                )
                # Removed anyway, and still a failure: the state before the removal could not be read.
                self.assertIn("rc=1", result.stdout, result.stderr)
                self.assertIn("cannot tell whether Codex plugin ponytail@ponytail is cached", result.stderr)
                self.assertFalse(cache.exists())
        # The explicit states the shell reads.
        work = Path(tempfile.mkdtemp(prefix="codex-state-"))
        self.addCleanup(shutil.rmtree, work)
        states = []
        for setup in (None, "5.3.2"):
            if setup:
                (work / "home/.codex/plugins/cache/ponytail/ponytail/5.3.2/.codex-plugin").mkdir(parents=True)
                (work / "home/.codex/plugins/cache/ponytail/ponytail/5.3.2/.codex-plugin/plugin.json").write_text(
                    json.dumps({"name": "ponytail", "version": setup})
                )
            states.append(
                subprocess.run(
                    ["bash", "-c", 'source "$1"; codex_plugin_copy ponytail@ponytail', "bash", str(UPDATER)],
                    env=os.environ | scratch_env(work / "home"),
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout
            )
        self.assertEqual(["absent\n", "copy 5.3.2\n"], states)

    def test_the_claude_user_install_state_is_explicit(self):
        result = subprocess.run(
            [
                "bash",
                "-c",
                'source "$1"; claude_user_install "[]"; '
                'claude_user_install \'[{"scope": "project", "version": "1"}]\'; '
                'claude_user_install \'[{"scope": "user", "version": "1.8.14"}]\'',
                "bash",
                str(UPDATER),
            ],
            env=os.environ | scratch_env(Path(tempfile.mkdtemp(prefix="claude-state-"))),
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(["absent", "absent", "installed 1.8.14"], result.stdout.splitlines())

    MALFORMED_COPY_REPLIES = ("", "garbage", "copy ", "copy a b", "copy ../x", "absent extra", "Copy 1.0")

    def run_with_copy_reply(self, reply: str, body: str) -> tuple[subprocess.CompletedProcess, list[str]]:
        # The reader (pin_record codex-copy) answers REPLY; every other pin_record call keeps its real reader.
        work = Path(tempfile.mkdtemp(prefix="copy-reply-"))
        self.addCleanup(shutil.rmtree, work)
        stub = (
            'eval "real_$(declare -f pin_record)"; '
            'pin_record() { case "$1" in codex-copy) printf "%s\\n" "${REPLY_UNDER_TEST}" ;; '
            'codex-marketplace-pinned) return 0 ;; *) real_pin_record "$@" ;; esac; }; '
            'codex() { printf "%s\\n" "$*" >> "${WORK}/calls"; }; ensure_codex_ponytail_marketplace() { :; }; '
        )
        result = subprocess.run(
            ["bash", "-c", f'source "$1"; set +e; {stub}{body}; echo "rc=$?"', "bash", str(UPDATER)],
            env=os.environ | scratch_env(work / "home") | {"WORK": str(work), "REPLY_UNDER_TEST": reply},
            text=True,
            capture_output=True,
            check=False,
        )
        calls = (work / "calls").read_text().splitlines() if (work / "calls").exists() else []
        return result, calls

    def test_every_codex_copy_reply_but_absent_or_a_strict_copy_is_an_error(self):
        # Audit of 0190e1f6: both installers took any reply but `absent` for "already installed".
        for reply in self.MALFORMED_COPY_REPLIES:
            with self.subTest(step="codex_plugin_copy", reply=reply):
                result, _ = self.run_with_copy_reply(reply, "codex_plugin_copy ponytail@ponytail")
                self.assertIn("rc=3", result.stdout, result.stderr)
                self.assertEqual(["rc=3"], result.stdout.splitlines())
            for step in ("install_codex_superpowers", "install_codex_ponytail"):
                with self.subTest(step=step, reply=reply):
                    result, calls = self.run_with_copy_reply(reply, step)
                    self.assertIn("rc=1", result.stdout, result.stderr)
                    self.assertNotIn("already installed", result.stdout)
                    self.assertFalse([c for c in calls if c.startswith("plugin add")], calls)
            with self.subTest(step="disable_plugin", reply=reply):
                result, calls = self.run_with_copy_reply(reply, "disable_plugin codex ponytail@ponytail")
                self.assertIn("rc=1", result.stdout, result.stderr)
                self.assertEqual(["plugin remove ponytail@ponytail"], calls)  # never read as absent
        for reply, expected in (
            ("absent", "absent"),
            ("copy 5.3.2", "copy 5.3.2"),
            ("copy 1.0.0+b.1", "copy 1.0.0+b.1"),
        ):
            with self.subTest(reply=reply):
                result, _ = self.run_with_copy_reply(reply, "codex_plugin_copy ponytail@ponytail")
                self.assertEqual([expected, "rc=0"], result.stdout.splitlines())
        result, calls = self.run_with_copy_reply("copy 5.3.2", "install_codex_superpowers")
        self.assertIn("already installed", result.stdout)
        self.assertIn("rc=0", result.stdout)

    def test_every_user_install_reply_but_absent_or_a_strict_version_is_an_error(self):
        for listing in (
            '[{"scope": "user", "version": ""}]',
            '[{"scope": "user", "version": "a b"}]',
            '[{"scope": "user"}]',
        ):
            with self.subTest(listing=listing):
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        'source "$1"; set +e; claude_user_install "$2"; echo "rc=$?"',
                        "bash",
                        str(UPDATER),
                        listing,
                    ],
                    env=os.environ | scratch_env(Path(tempfile.mkdtemp(prefix="user-install-"))),
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(["rc=3"], result.stdout.splitlines(), result.stderr)

    def test_no_caller_reads_a_plugin_state_reply_but_through_its_one_parser(self):
        # Structural guard: the Codex copy reader is called only by codex_plugin_copy; the two parsers' output
        # lands only in codex_copy / user_install, which no `[`, `[[` or `test` ever compares: every caller
        # matches them in a `case` whose default is an error.
        text = UPDATER.read_text()
        bodies = dict(re.findall(r"^function (\w+)\(\) \(?\{\n(.*?)^\}", text, re.M | re.S))
        self.assertEqual(
            ["codex_plugin_copy"], [name for name, body in bodies.items() if "pin_record codex-copy" in body]
        )
        for parser, variable in (("codex_plugin_copy", "codex_copy"), ("claude_user_install", "user_install")):
            assigned = re.findall(rf'(\w+)="\$\({parser} ', text)
            self.assertTrue(assigned, parser)
            self.assertEqual({variable}, set(assigned), parser)
            tests = [
                line.strip()
                for line in text.splitlines()
                if re.search(r"(\[\[?|\btest) ", line) and f"${{{variable}" in line
            ]
            self.assertEqual([], tests, variable)
            for name, body in bodies.items():
                if f'{variable}="$({parser} ' in body:
                    self.assertIn(f'case "${{{variable}}}" in', body, name)
        # Every case on a state (and each parser's own case on the reader's reply) has a `*)` default that returns
        # non-zero: an unexpected state is never a success, a version or `unknown`.
        blocks = re.findall(r'^( *)case "\$\{(codex_copy|user_install|reply)\}" in\n(.*?)^\1esac', text, re.M | re.S)
        self.assertGreaterEqual(len(blocks), 9)
        for indent, variable, block in blocks:
            default = re.search(rf"^{indent}\*\)(.*?);;", block, re.M | re.S)
            with self.subTest(variable=variable, block=block[:60]):
                self.assertIsNotNone(default)
                self.assertRegex(default.group(1), r"\b(return|exit) [1-9]")
        # No record read falls back to a made-up value: no `|| printf 'unknown'`-style default in the record readers.
        for function in (
            "claude_user_plugin_version",
            "claude_user_install",
            "codex_plugin_copy",
            "record_claude_plugin_step",
        ):
            self.assertNotIn("unknown", bodies[function], function)

    def test_a_claude_version_that_cannot_be_read_is_never_recorded_as_unknown(self):
        # Audit of 1b93aad9: claude_user_plugin_version turned a read failure, a parser failure and an unexpected
        # state into a successful `unknown`, and manifest_record recorded it.
        for name, stubs in (
            ("read failure", "claude_plugin_installs() { return 1; }"),
            ("parser failure", 'claude_plugin_installs() { printf \'[{"scope": "user", "version": "a b"}]\\n\'; }'),
            ("unexpected state", "claude_user_install() { printf 'garbage\\n'; }"),
        ):
            with self.subTest(case=name):
                step = (
                    f'{stubs}; set +e; claude_user_plugin_version crit@crit; echo "rc=$?"; '
                    'record_claude_plugin_step update_claude_crit crit@crit "${HOME}/x" -- "cmd"; '
                    'printf "failures=%s\\n" "${CLAUDE_PIN_FAILURES}"; '
                    '[ ! -e "${HOME}/.agents/.installed-manifest.json" ] || echo recorded'
                )
                result, _, _ = self.converge_listed(step, {}, {})
                lines = result.stdout.splitlines()
                self.assertEqual(["rc=1", "failures=1"], lines, result.stderr)
                self.assertNotIn("unknown", result.stdout)
                self.assertIn("reading the installed version of crit@crit for the asset manifest", result.stderr)
        # Absent is its own result: nothing is recorded and nothing is counted.
        step = (
            'set +e; claude_user_plugin_version crit@crit; echo "rc=$?"; '
            'record_claude_plugin_step update_claude_crit crit@crit "${HOME}/x" -- "cmd"; '
            'printf "failures=%s\\n" "${CLAUDE_PIN_FAILURES}"'
        )
        result, _, _ = self.converge_listed(step, {}, {})
        self.assertEqual(["rc=4", "failures=0"], result.stdout.splitlines(), result.stderr)
        self.assertIn("is not recorded in the installed asset manifest", result.stderr)
        # And an installed version is recorded as itself.
        pin = self.pin_of("crit@crit")
        installs = {"crit@crit": [{"scope": "user", "version": pin}]}
        result, _, _ = self.converge_listed('claude_user_plugin_version crit@crit; echo "rc=$?"', installs, {})
        self.assertEqual([pin, "rc=0"], result.stdout.splitlines(), result.stderr)

    def run_ponytail_step(self, config: str) -> tuple[subprocess.CompletedProcess, list[str]]:
        # update_codex_ponytail against a fake codex that logs every call; CONFIG is ~/.codex/config.toml.
        work = Path(tempfile.mkdtemp(prefix="ponytail-step-"))
        self.addCleanup(shutil.rmtree, work)
        (work / "home/.codex").mkdir(parents=True)
        (work / "home/.codex/config.toml").write_text(config)
        fake = 'codex() { printf "%s\\n" "$*" >> "${WORK}/calls"; }'
        result = subprocess.run(
            [
                "bash",
                "-c",
                f'source "$1"; has_command() {{ return 0; }}; {fake}\nupdate_codex_ponytail; fail_on_claude_pin_failures',
                "bash",
                str(UPDATER),
            ],
            env=os.environ | scratch_env(work / "home") | {"WORK": str(work)},
            text=True,
            capture_output=True,
            check=False,
        )
        calls = (work / "calls").read_text().splitlines() if (work / "calls").exists() else []
        return result, calls

    def test_a_ponytail_marketplace_without_the_pinned_ref_is_never_upgraded(self):
        # Audit round 18: a marketplace with a missing or stale ref was upgraded to the branch head.
        ref = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["codex"]["ponytail@ponytail"]["ref"]
        source = "https://github.com/DietrichGebert/ponytail.git"
        for name, extra in (("no ref", ""), ("stale ref", f'ref = "{"0" * 40}"\n')):
            with self.subTest(case=name):
                config = f'[marketplaces.ponytail]\nsource_type = "git"\nsource = "{source}"\n{extra}'
                result, calls = self.run_ponytail_step(config)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(f"is not pinned to {ref}", result.stderr)
                self.assertFalse([call for call in calls if call.startswith("plugin marketplace upgrade")], calls)

    def test_a_foreign_marketplace_never_installs_or_updates_and_its_plugin_is_disabled(self):
        # Audit round 19: a marketplace of the recorded name from another repository can serve a release that
        # reports the pinned version. Its plugin is disabled at any version, and nothing is installed or updated.
        pin = self.pin_of("crit@crit")
        for version in (pin, "999.0.0"):
            with self.subTest(version=version):
                installs = {"crit@crit": [{"scope": "user", "version": version}]}
                result, calls, state = self.converge_listed(
                    'converge_claude_plugin "crit@crit"', installs, {"crit@crit": True}, FOREIGN="fork/crit"
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(["plugin disable crit@crit --scope user @neutral"], calls)
                self.assertIs(False, state["user"]["crit@crit"])
                self.assertIn("registered from another source", result.stderr)
        # Not installed: nothing is installed from it either.
        result, calls, _ = self.converge_listed('converge_claude_plugin "crit@crit"', {}, {}, FOREIGN="fork/crit")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual([], calls)

    def test_a_failed_disable_of_an_off_pin_plugin_fails_closed(self):
        installs = {"crit@crit": [{"scope": "user", "version": "999.0.0"}]}
        result, calls, state = self.converge_listed(
            'converge_claude_plugin "crit@crit"', installs, {"crit@crit": True}, DISABLE_FAILS="1"
        )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("plugin disable crit@crit --scope user @neutral", calls)
        self.assertIs(True, state["user"]["crit@crit"])

        # The run counts it, so main exits non-zero instead of reporting success.
        step = 'converge_claude_step "crit@crit" || true; printf "failures=%s\\n" "${CLAUDE_PIN_FAILURES}"'
        result, _, _ = self.converge_listed(step, installs, {"crit@crit": True}, DISABLE_FAILS="1")
        self.assertIn("failures=1", result.stdout)

    def test_a_missing_plugin_installs_from_its_recorded_marketplace(self):
        pstack = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"]["pstack@cursor-plugins"]
        step = 'converge_claude_plugin "pstack@cursor-plugins"'
        # No cursor-plugins marketplace on this host: it is registered from the manifest, then the plugin installs.
        result, calls, state = self.converge_listed(
            step, {}, {}, markets=[], ADD_NAME="cursor-plugins", INSTALL_VERSION=pstack["pin"]
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            [
                f"plugin marketplace add {pstack['marketplace']} @neutral",
                "plugin install pstack@cursor-plugins --scope user @neutral",
            ],
            calls,
        )
        self.assertIs(True, state["user"]["pstack@cursor-plugins"])

        # Failure injection: a marketplace or install that fails leaves the pinned plugin missing, which fails the run.
        for flags, message in (
            ({"ADD_FAILS": "1"}, "marketplace add"),
            (
                {"ADD_NAME": "cursor-plugins", "INSTALL_FAILS": "1"},
                "claude plugin install pstack@cursor-plugins failed",
            ),
        ):
            with self.subTest(flags=flags):
                result, _, _ = self.converge_listed(step, {}, {}, markets=[], **flags)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(message, result.stderr)

    def test_a_claude_plugin_is_disabled_when_its_records_cannot_be_read(self):
        # Failure injection: an unreadable installed_plugins.json is never read as "not installed": nothing is
        # installed or updated, and the plugin it may hold is disabled.
        result, calls, state = self.converge_listed('converge_claude_plugin "crit@crit"', "{truncated", {})
        self.assertEqual(1, result.returncode)
        self.assertEqual(["plugin disable crit@crit --scope user @neutral"], calls)
        self.assertIs(False, state["user"]["crit@crit"])
        self.assertIn("cannot read the installation records of crit@crit", result.stderr)
        # Unchecked is a failure of the run, through every caller: the named step and the manifest loop.
        for step in ("update_claude_crit", "converge_claude_plugins"):
            with self.subTest(step=step):
                gate = f"ensure_crit_cli() {{ :; }}; ensure_claude_crit_marketplace() {{ :; }}; {step}; fail_on_claude_pin_failures"
                result, _, _ = self.converge_listed(gate, "{truncated", {})
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("could not be checked or kept at their pin", result.stderr)

    def test_a_disabled_plugin_at_its_pin_is_left_disabled(self):
        installs = {"pstack@cursor-plugins": [{"scope": "user", "version": self.pin_of("pstack@cursor-plugins")}]}
        result, calls, state = self.converge_listed(
            'converge_claude_plugin "pstack@cursor-plugins"', installs, {"pstack@cursor-plugins": False}
        )
        self.assertEqual(0, result.returncode, result.stderr)
        # An operator's disable of a reviewed release stays: nothing is enabled, updated or installed.
        self.assertEqual([], calls)
        self.assertIs(False, state["user"]["pstack@cursor-plugins"])

    def test_every_pinned_claude_plugin_is_checked_from_the_manifest_list(self):
        pins = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"]
        installs = {
            plugin_id: [
                {"scope": "user", "version": CONTENT_VERSION, "reviewed": True}
                if pin["pin"].startswith("sha256:")
                else {"scope": "user", "version": "999.0.0" if plugin_id.startswith("pstack@") else pin["pin"]}
            ]
            for plugin_id, pin in pins.items()
        }
        enabled = dict.fromkeys(pins, True)
        # pstack has no setup step of its own; the manifest-driven loop still converges it.
        step = 'converge_claude_plugins; printf "failures=%s\\n" "${CLAUDE_PIN_FAILURES}"'
        result, calls, state = self.converge_listed(step, installs, enabled)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            [
                "plugin update pstack@cursor-plugins --scope user @neutral",
                "plugin disable pstack@cursor-plugins --scope user @neutral",
            ],
            calls,
        )
        self.assertEqual(["pstack@cursor-plugins"], [plugin for plugin, on in state["user"].items() if not on])
        self.assertIn("failures=1", result.stdout)  # the off-pin pstack, as the doctor judges it
        # A plugin a setup step already converged is not converged twice.
        _, calls, _ = self.converge_listed(
            'CLAUDE_CONVERGED=" pstack@cursor-plugins "; converge_claude_plugins', installs, enabled
        )
        self.assertEqual([], calls)

    def test_a_failed_marketplace_setup_never_skips_the_pin_check(self):
        # Failure injection: no marketplace is registered and `marketplace add` fails. Under the script's own
        # set -e, each wrapper still reaches the convergence, disables its off-pin plugin, and the run fails.
        pins = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"]
        for step, plugin_id in (
            ("update_claude_superpowers", "superpowers@claude-plugins-official"),
            ("update_claude_crit", "crit@crit"),
            ("update_claude_ponytail", "ponytail@ponytail"),
            ("update_claude_understand_anything", "understand-anything@understand-anything"),
        ):
            with self.subTest(step=step):
                installs = {plugin_id: [{"scope": "user", "version": "999.0.0"}]}
                gate = (
                    "ensure_crit_cli() { return 1; }; "
                    f'{step}; printf "reached failures=%s\\n" "${{CLAUDE_PIN_FAILURES}}"; fail_on_claude_pin_failures'
                )
                result, calls, state = self.converge_listed(
                    gate, installs, {plugin_id: True}, markets=[], ADD_FAILS="1"
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("reached failures=", result.stdout)
                self.assertIn(f"plugin disable {plugin_id} --scope user @neutral", calls)
                self.assertIs(False, state["user"][plugin_id])
                self.assertIn(f"{plugin_id} is not installed or updated from an unverified marketplace", result.stderr)

    def test_a_failed_manifest_write_fails_the_run_and_every_plugin_is_still_converged(self):
        # Audit round 25: manifest_record always returned 0, so the wrappers' failure handler never ran and a
        # failed write left the run green. Failure injection: ~/.agents is a file, so no record can be written.
        pins = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"]
        for step, plugin_id in (
            ("update_claude_superpowers", "superpowers@claude-plugins-official"),
            ("update_claude_crit", "crit@crit"),
            ("update_claude_ponytail", "ponytail@ponytail"),
            ("update_claude_understand_anything", "understand-anything@understand-anything"),
        ):
            with self.subTest(step=step):
                installs = {plugin_id: [{"scope": "user", "version": pins[plugin_id]["pin"]}]}
                gate = (
                    'printf x > "${HOME}/.agents"; ensure_crit_cli() { :; }; '
                    f'{step}; printf "reached failures=%s\\n" "${{CLAUDE_PIN_FAILURES}}"; fail_on_claude_pin_failures'
                )
                result, _, state = self.converge_listed(gate, installs, {plugin_id: True})
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("reached failures=1", result.stdout)
                self.assertIn(f"failed to record asset manifest step {step}", result.stderr)
                self.assertIs(True, state["user"][plugin_id])  # at its pin: the plugin itself is left alone
        # A Codex step and one that is not a plugin step: the same failure, counted, and the run fails.
        for step, stubs in (
            (
                "update_codex_superpowers",
                "codex_plugin_copy() { echo 'copy 6.3.0'; }; doctor_pin_check() { :; }; "
                "manifest_codex_plugin_version() { echo 6.3.0; }; ",
            ),
            ("ensure_herdr_integrations", 'herdr() { echo "herdr 1.0"; }; '),
        ):
            with self.subTest(step=step):
                gate = (
                    f'printf x > "${{HOME}}/.agents"; {stubs}{step}; '
                    'printf "reached failures=%s\\n" "${CLAUDE_PIN_FAILURES}"; fail_on_claude_pin_failures'
                )
                result, _, _ = self.converge_listed(gate, {}, {})
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("reached failures=1", result.stdout)
                self.assertIn(f"failed to record asset manifest step {step}", result.stderr)

    def run_gh_extensions(
        self, tag: str, pinned: str | None, install_fails: bool = False
    ) -> tuple[subprocess.CompletedProcess, list[str], Path]:
        # install/common/gh_extensions.sh against a fake gh listing gh-poi at TAG; PINNED is its manifest.yml
        # ispinned value (None: no manifest), the field gh writes for `gh extension install --pin`. The fake
        # install writes a fresh pinned copy, or (INSTALL_FAILS) leaves a partial directory and fails.
        work = Path(tempfile.mkdtemp(prefix="gh-extensions-"))
        self.addCleanup(shutil.rmtree, work)
        directory = work / "data/gh/extensions/gh-poi"
        directory.mkdir(parents=True)
        (directory / "gh-poi").write_text("old binary\n")
        if pinned is not None:
            (directory / "manifest.yml").write_text(
                f"owner: seachicken\nname: gh-poi\nhost: github.com\ntag: {tag}\nispinned: {pinned}\npath: {directory}/gh-poi\n"
            )
        fake = (
            'gh() { case "$1 $2" in "auth status") return 0 ;; '
            '"extension list") printf "gh poi\\tseachicken/gh-poi\\t%s\\n" "${TAG}" ;; '
            '"extension install") printf "%s\\n" "$*" >> "${WORK}/calls"; '
            'd="${XDG_DATA_HOME}/gh/extensions/gh-poi"; [ ! -e "$d" ] || return 7; mkdir -p "$d"; '
            'if [ -n "${INSTALL_FAILS}" ]; then echo partial > "$d/gh-poi"; return 1; fi; '
            'echo new > "$d/gh-poi"; printf "owner: seachicken\\nname: gh-poi\\nhost: github.com\\ntag: %s\\nispinned: true\\npath: %s\\n" "$5" "$d/gh-poi" > "$d/manifest.yml" ;; '
            '"extension remove") printf "%s\\n" "$*" >> "${WORK}/calls"; rm -rf "${XDG_DATA_HOME}/gh/extensions/$3" ;; '
            '*) printf "%s\\n" "$*" >> "${WORK}/calls" ;; esac; }'
        )
        result = subprocess.run(
            [
                "bash",
                "-c",
                f'source "$1"; activate_mise() {{ :; }}; {fake}; main',
                "bash",
                str(ROOT / "install/common/gh_extensions.sh"),
            ],
            env=os.environ
            | scratch_env(work / "home", XDG_DATA_HOME=str(work / "data"))
            | {
                "WORK": str(work),
                "TAG": tag,
                "INSTALL_FAILS": "1" if install_fails else "",
            },
            text=True,
            capture_output=True,
            check=False,
        )
        calls = (work / "calls").read_text().splitlines() if (work / "calls").exists() else []
        return result, calls, directory

    def test_a_failed_pinned_install_restores_the_previous_gh_extension(self):
        pin = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["gh_extensions"]["seachicken/gh-poi"]
        result, calls, directory = self.run_gh_extensions("v0.0.1", "false", install_fails=True)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual([f"extension install seachicken/gh-poi --pin {pin}"], calls)
        # The old copy is back in place and nothing is left aside.
        self.assertEqual("old binary\n", (directory / "gh-poi").read_text())
        self.assertFalse((directory.parent / ".gh-poi.previous").exists())
        self.assertIn("restoring the previous copy", result.stderr)

        # On success the old copy is replaced and its aside copy deleted; nothing is removed first.
        result, calls, directory = self.run_gh_extensions("v0.0.1", "false")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("new\n", (directory / "gh-poi").read_text())
        self.assertFalse((directory.parent / ".gh-poi.previous").exists())
        self.assertFalse([call for call in calls if call.startswith("extension remove")], calls)

    def test_a_gh_extension_name_that_is_not_one_component_changes_nothing(self):
        # Audit round 23 (the same rule in shell): the name is moved aside and removed under gh's directory.
        work = Path(tempfile.mkdtemp(prefix="gh-component-"))
        self.addCleanup(shutil.rmtree, work)
        canary = work / "home/.local/share/gh/extensions/keep"
        canary.mkdir(parents=True)
        for bad in ("seachicken/..", "seachicken/.", "seachicken/", "/abs", "seachicken/a/b", "../gh-poi"):
            with self.subTest(repository=bad):
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        'source "$1"; set +e; gh() { printf "%s\\n" "$*" >> "${WORK}/calls"; }; replace_gh_extension "$2" v1; echo "rc=$?"',
                        "bash",
                        str(ROOT / "install/common/gh_extensions.sh"),
                        bad,
                    ],
                    env=os.environ | scratch_env(work / "home") | {"WORK": str(work)},
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertIn("rc=1", result.stdout, result.stderr)
                self.assertIn("is not <owner>/<repository>", result.stderr)
                self.assertTrue(canary.is_dir())
                self.assertFalse((work / "calls").exists())

    def test_a_gh_extension_is_kept_pinned_at_its_tag(self):
        pin = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["gh_extensions"]["seachicken/gh-poi"]
        reinstall = [f"extension install seachicken/gh-poi --pin {pin}"]
        # At its tag and pinned: nothing to do.
        result, calls, _ = self.run_gh_extensions(pin, "true")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], calls)
        # At its tag but installed unpinned (or with no readable manifest): reinstalled with --pin,
        # since `gh extension upgrade` could otherwise move it.
        for pinned in ("false", None):
            with self.subTest(pinned=pinned):
                result, calls, _ = self.run_gh_extensions(pin, pinned)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(reinstall, calls)
        # At another tag: reinstalled at the pin.
        result, calls, _ = self.run_gh_extensions("v0.0.1", "true")
        self.assertEqual(reinstall, calls)


class MaskedStatusTest(unittest.TestCase):
    """Structural guard: no exit status of an agent CLI, gh or mise is lost on its way to a decision."""

    FILES = ("scripts/update-agent-assets.sh", "scripts/upgrade-tools.sh", "install/common/gh_extensions.sh")

    def test_shellcheck_reports_no_masked_return(self):
        result = subprocess.run(
            ["shellcheck", "-x", "-o", "check-extra-masked-returns", "-f", "gcc", *self.FILES],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)

    def test_no_tool_output_is_piped_into_a_decision(self):
        # SC2312 does not see a pipeline's first command; under pipefail its failure reads as "no match". Every
        # call of these tools is captured on its own (status checked) before anything parses its output.
        tool = re.compile(
            r'(^|[\s;(&|])(claude_outside_projects|claude|codex|gh|run_mise_with_isolated_git_config|mise|uv|"\$@")\s[^|#]*\|'
        )
        offenders = []
        for name in self.FILES:
            for number, line in enumerate((ROOT / name).read_text().splitlines(), 1):
                code = line.split(" #", 1)[0]
                if code.lstrip().startswith("#"):
                    continue
                # `||` is a status test, not a pipe; only a single `|` hands output on.
                if tool.search(code.replace("||", "  ")):
                    offenders.append(f"{name}:{number}: {line.strip()}")
        self.assertEqual([], offenders)

    def test_a_failed_codex_marketplace_list_is_never_read_as_absent(self):
        # Failure injection: no [marketplaces.ponytail] in the config and `codex plugin marketplace list` fails.
        work = Path(tempfile.mkdtemp(prefix="ponytail-probe-"))
        self.addCleanup(shutil.rmtree, work)
        (work / "home/.codex").mkdir(parents=True)
        (work / "home/.codex/config.toml").write_text("")
        fake = (
            'codex() { printf "%s\\n" "$*" >> "${WORK}/calls"; '
            '[ "$1 $2 $3" = "plugin marketplace list" ] && return 9; return 0; }'
        )
        result = subprocess.run(
            ["bash", "-c", f'source "$1"; {fake}\nensure_codex_ponytail_marketplace', "bash", str(UPDATER)],
            env=os.environ | scratch_env(work / "home") | {"WORK": str(work)},
            text=True,
            capture_output=True,
            check=False,
        )
        calls = (work / "calls").read_text().splitlines() if (work / "calls").exists() else []
        self.assertNotEqual(0, result.returncode, result.stderr)
        self.assertFalse([call for call in calls if call.startswith("plugin marketplace add")], calls)
        self.assertIn("codex plugin marketplace list failed", result.stderr)
