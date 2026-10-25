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
            env=os.environ | {"HOME": str(home), "CALLS": str(home / "calls")} | env,
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
    "plugin marketplace list") cat "${WORK}/markets.json" ;;
    "plugin marketplace add") [ -z "${ADD_FAILS}" ] || return 1
        jq --arg name "${ADD_NAME}" '. + [{name: $name}]' "${WORK}/markets.json" > "${WORK}/next" && mv "${WORK}/next" "${WORK}/markets.json" ;;
    "plugin install "*) [ -z "${INSTALL_FAILS}" ] || return 1
        jq --arg id "$3" --arg version "${INSTALL_VERSION}" '.plugins[$id] += [{scope: "user", version: $version}]' \
            "${record}" > "${WORK}/next" && mv "${WORK}/next" "${record}"
        jq --arg id "$3" '.enabledPlugins[$id] = true' "${user}" > "${WORK}/next" && mv "${WORK}/next" "${user}" ;;
    "plugin disable "*) [ -z "${DISABLE_FAILS}" ] || return 1; [ -z "${DISABLE_NOOP}" ] || return 0
        settings="${user}"; [ "$5" = user ] || settings="${PWD}/.claude/settings.json"
        jq --arg id "$3" '.enabledPlugins[$id] = false' "${settings}" > "${WORK}/next" && mv "${WORK}/next" "${settings}" ;;
    esac
}
"""

    def converge_listed(self, step, installs, enabled, markets=None, project=None, cwd=None, **flags):
        """Run STEP against the fake: INSTALLS {id: [{scope, version, projectPath?}]}, user ENABLED {id: bool},
        PROJECT {id: bool} as the enabledPlugins of a project directory (work/project), CWD "project" to run there."""
        work = Path(tempfile.mkdtemp(prefix="converge-listed-"))
        self.addCleanup(shutil.rmtree, work)
        home = work / "home"
        (home / ".claude/plugins").mkdir(parents=True)
        project_dir = work / "project"
        (project_dir / ".claude").mkdir(parents=True)
        (project_dir / ".claude/settings.json").write_text(json.dumps({"enabledPlugins": project or {}}))
        for entries in installs.values() if isinstance(installs, dict) else []:
            for entry in entries:
                if entry.get("projectPath") == "PROJECT":
                    entry["projectPath"] = str(project_dir)
        record = home / ".claude/plugins/installed_plugins.json"
        record.write_text(installs if isinstance(installs, str) else json.dumps({"version": 2, "plugins": installs}))
        (home / ".claude/settings.json").write_text(json.dumps({"enabledPlugins": enabled}))
        pins = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"]
        names = [plugin_id.split("@", 1)[1] for plugin_id in pins] if markets is None else markets
        (work / "markets.json").write_text(json.dumps([{"name": name} for name in names]))
        variables = ("ADD_FAILS", "ADD_NAME", "INSTALL_FAILS", "INSTALL_VERSION", "DISABLE_FAILS", "DISABLE_NOOP")
        result = subprocess.run(
            [
                "bash",
                "-c",
                f'source "$1"; has_command() {{ return 0; }}; {self.FAKE_CLAUDE.strip()}\n{step}',
                "bash",
                str(UPDATER),
            ],
            env=os.environ | {name: "" for name in variables} | {"WORK": str(work), "HOME": str(home)} | flags,
            cwd=project_dir if cwd == "project" else work,
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
        self.assertEqual(0, result.returncode, result.stderr)
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
        self.assertEqual(0, result.returncode, result.stderr)
        # Every claude call runs outside the project, and the user-scope disable is what the user file shows.
        self.assertIn("plugin disable crit@crit --scope user @neutral", calls)
        self.assertTrue(all(call.endswith("@neutral") for call in calls), calls)
        self.assertIs(False, state["user"]["crit@crit"])

    def test_every_installation_of_a_claude_plugin_is_converged(self):
        pin = self.pin_of("crit@crit")
        step = 'converge_claude_plugin "crit@crit"'
        # A user copy at the pin must not hide an enabled project copy off it; the project copy is handled in its project.
        installs = {
            "crit@crit": [
                {"scope": "user", "version": pin},
                {"scope": "project", "version": "999.0.0", "projectPath": "PROJECT"},
            ]
        }
        result, calls, state = self.converge_listed(step, installs, {"crit@crit": True}, project={"crit@crit": True})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            ["plugin update crit@crit --scope project @project", "plugin disable crit@crit --scope project @project"],
            calls,
        )
        self.assertEqual({"user": True, "project": False}, {scope: state[scope]["crit@crit"] for scope in state})

        # A disable that changes nothing leaves the project copy enabled: the settings file decides, so the run fails.
        installs = {
            "crit@crit": [
                {"scope": "user", "version": "999.0.0"},
                {"scope": "project", "version": "999.0.0", "projectPath": "PROJECT"},
            ]
        }
        result, calls, _ = self.converge_listed(
            step, installs, {"crit@crit": False}, project={"crit@crit": True}, DISABLE_NOOP="1"
        )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("plugin disable crit@crit --scope project @project", calls)
        self.assertIn("still enabled off its pin", result.stderr)

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
                "plugin install pstack@cursor-plugins @neutral",
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

    def test_a_claude_plugin_is_not_changed_when_its_records_cannot_be_read(self):
        # Failure injection: an unreadable installed_plugins.json is never read as "not installed".
        result, calls, _ = self.converge_listed('converge_claude_plugin "crit@crit"', "{truncated", {})
        self.assertEqual(1, result.returncode)
        self.assertEqual([], calls)
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
            plugin_id: [{"scope": "user", "version": "999.0.0" if plugin_id.startswith("pstack@") else pin["pin"]}]
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
        self.assertIn("failures=0", result.stdout)
        # A plugin a setup step already converged is not converged twice.
        _, calls, _ = self.converge_listed(
            'CLAUDE_CONVERGED=" pstack@cursor-plugins "; converge_claude_plugins', installs, enabled
        )
        self.assertEqual([], calls)
