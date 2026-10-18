"""Exercise verified artifact updates using fake downloads and installers only."""

import hashlib
import json
import os
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
        if (target.exists() or target.is_symlink()) and own not in (os.readlink(target) if target.is_symlink() else ""):
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
            self.assertEqual("3", records[0]["min_release_age"])
            self.assertEqual("0" if tool == "omp" else "3", records[1]["min_release_age"])
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

    def test_update_omp_moves_an_entry_npm_does_not_own_aside_and_puts_it_back_when_the_install_fails(self):
        # local:fbbc6d9:1: a standalone file or a link outside the package, a dangling one included, makes npm fail
        # with EEXIST; npm's own link stays for npm to replace.
        npm_link = Path("../lib/node_modules/@oh-my-pi/pi-coding-agent/bin/omp")
        for entry in ("dangling", "external", "file", "npm", None):
            for version in ("18.11.3", "0.0.1"):
                with self.subTest(entry=entry, version=version), tempfile.TemporaryDirectory() as directory:
                    home = Path(directory)
                    binary = home / ".local/bin"
                    binary.mkdir(parents=True)
                    for name in ("curl", "npm"):
                        (binary / name).write_text(STUB.replace("@PYTHON@", sys.executable))
                        (binary / name).chmod(0o755)
                    target, old = binary / "omp", home / "tern/bin/omp"
                    old.parent.mkdir(parents=True)
                    old.write_text("#!/bin/sh\necho omp/0.0.1\n")
                    if entry == "external":
                        old.chmod(0o755)
                    links = {"dangling": home / "gone/omp", "external": old, "npm": npm_link}
                    if entry in links:
                        target.symlink_to(links[entry])
                    elif entry == "file":
                        target.write_text("#!/bin/sh\necho omp/0.0.1\n")
                    payload = home / "payload"
                    payload.write_bytes(b"fixture omp tarball\n")
                    result = subprocess.run(
                        ["bash", "-c", 'source "$1"; OMP_PIN_VERSION=18.11.3; OMP_TARBALL_SHA256="$2"; update_omp']
                        + ["bash", str(UPDATER), hashlib.sha256(payload.read_bytes()).hexdigest()],
                        env=os.environ
                        | {
                            "HOME": directory,
                            "PATH": str(binary) + os.pathsep + os.environ["PATH"],
                            "CALLS": str(home / "calls.jsonl"),
                            "PAYLOAD": str(payload),
                            "FIXTURE_VERSION": version,
                        },
                        stdin=subprocess.DEVNULL,
                        capture_output=True,
                        text=True,
                        timeout=30,
                        check=False,
                    )
                    output = result.stdout + result.stderr
                    self.assertEqual(version == "0.0.1", result.returncode != 0, output)
                    self.assertNotIn("EEXIST", output)
                    if version == "18.11.3" or entry in ("npm", None):
                        self.assertEqual(npm_link, target.readlink(), output)
                    elif entry == "file":  # the failed install puts the previous entry back as it was
                        self.assertEqual("#!/bin/sh\necho omp/0.0.1\n", target.read_text(), output)
                    else:
                        self.assertEqual(links[entry], target.readlink(), output)

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
