"""Exercise verified artifact updates using fake downloads and installers only."""

import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UPDATER = ROOT / "scripts/update-agent-assets.sh"
# The rendered omp pin: update_omp builds its tarball URL from it when the script is sourced (OMP_TARBALL_URL is
# readonly), so the fixtures install at that version rather than at a literal one.
INSTALLER_PINS = (ROOT / "scripts/lib/installer-pins.sh").read_text()
OMP_PIN = re.search(r'^OMP_PIN_VERSION="([^"]+)"$', INSTALLER_PINS, re.MULTILINE)[1]
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
from codex_plugin_fixture import PONYTAIL, install_ponytail_copy, reviewed_content_sha256
from scratch_git import git_init

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
            pin = OMP_PIN if tool == "omp" else "0.7.30"
            search_path = str(binary) + os.pathsep + os.environ["PATH"]
            if shadow_version is not None:
                shadows = home / "shadows"
                shadows.mkdir()
                shadow = shadows / tool
                version = pin if shadow_version == "pin" else shadow_version
                shadow.write_text(f"#!/usr/bin/env bash\nprintf '{tool} {version}\\n'\n")
                shadow.chmod(0o755)
                search_path = str(shadows) + os.pathsep + search_path
            constants = f'OMP_PIN_VERSION={OMP_PIN}; HCOM_PIN_VERSION=0.7.30; OMP_TARBALL_SHA256="$2"; '
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
            argv = records[0]["argv"]
            url = argv[argv.index("-o") - 1]  # the URL comes right before the output file
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
            ["bash", "-c", f'source "$1"; OMP_PIN_VERSION={OMP_PIN}; OMP_TARBALL_SHA256="$2"; update_omp']
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
            result = self.update_omp_in(home, OMP_PIN, tmpdir=sandbox_tmp)
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
            result = self.update_omp_in(home, OMP_PIN)
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
            for version in (OMP_PIN, "0.0.1"):
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
                    elif version == OMP_PIN or not moved:
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
            result = self.update_omp_in(home, OMP_PIN, spelling="/")
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
            (f"omp/{OMP_PIN}", True),
            (OMP_PIN, True),
            (f"other/{OMP_PIN}", False),
            (f"omp/omp/{OMP_PIN}", False),
            (f"omp/{OMP_PIN}-extra", False),
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
                        f'source "$1"; OMP_PIN_VERSION={OMP_PIN}; has_command() {{ return 0; }}; curl() {{ return 42; }}; update_omp',
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


class SecurityAuditSkillTest(unittest.TestCase):
    """update_security_audit_skill over an archive built here, never downloaded (U144): the pin, the digest check,
    the atomic replace of the skills/security-audit subtree and the manifest record the doctor reads."""

    # The rendered pin; a tree without the constant (the red proof against origin/main) gets a placeholder so the
    # module still imports and the tests themselves fail on the absent step.
    COMMIT_MATCH = re.search(r'^SECURITY_AUDIT_SKILL_COMMIT="([0-9a-f]{40})"$', UPDATER.read_text(), re.MULTILINE)
    COMMIT = COMMIT_MATCH[1] if COMMIT_MATCH else "0" * 40
    URL = f"https://codeload.github.com/cloudflare/security-audit-skill/tar.gz/{COMMIT}"
    SKILL = "---\nname: security-audit\ndescription: fixture of the upstream skill\n---\n"

    MEMBERS = {
        "LICENSE": "fixture licence\n",
        "README.md": "fixture readme\n",
        "skills/security-audit/SKILL.md": SKILL,
        "skills/security-audit/validate-findings.cjs": "// fixture validator\n",
    }

    def archive(self, home: Path, members: dict[str, str] | None = None) -> tuple[Path, str]:
        """A codeload-shaped tarball: <repository>-<commit>/{LICENSE,README.md,skills/security-audit/...}."""
        if members is None:
            members = self.MEMBERS
        payload = home / "archive.tgz"
        with tarfile.open(payload, "w:gz") as tar:
            for name, text in members.items():
                data = text.encode()
                info = tarfile.TarInfo(f"security-audit-skill-{self.COMMIT}/{name}")
                info.size = len(data)
                tar.addfile(info, io.BytesIO(data))
        return payload, hashlib.sha256(payload.read_bytes()).hexdigest()

    def run_step(self, home: Path, payload: Path, digest: str, *, curl: str | None = None, **env: str):
        # curl is a shell function that writes $PAYLOAD to its -o path and logs its arguments; nothing is downloaded.
        # A test may replace its body (a failed download) or hand the step an environment (TMPDIR, PATH).
        download = curl or 'cp "$PAYLOAD" "${@: -1}"'
        stubs = f"SECURITY_AUDIT_SKILL_SHA256={digest}; " + 'curl() { echo "curl $*" >> "$CALLS"; ' + download + "; }; "
        return subprocess.run(
            ["bash", "-c", 'source "$1"; ' + stubs + "update_security_audit_skill", "bash", str(UPDATER)],
            env=os.environ | {"HOME": str(home), "PAYLOAD": str(payload), "CALLS": str(home / "calls")} | env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def calls(self, home: Path) -> list[str]:
        log = home / "calls"
        return log.read_text().splitlines() if log.exists() else []

    def test_the_pinned_security_audit_archive_installs_the_skill_subtree_and_records_the_step(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            payload, digest = self.archive(home)
            install = home / ".agents/skills/security-audit"
            result = self.run_step(home, payload, digest)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(self.SKILL, (install / "SKILL.md").read_text())
            # The subtree alone: no LICENSE or README from the archive root, and no staging or previous tree beside it.
            self.assertEqual(["SKILL.md", "validate-findings.cjs"], sorted(path.name for path in install.iterdir()))
            self.assertEqual(["security-audit"], sorted(path.name for path in install.parent.iterdir()))
            calls = self.calls(home)
            self.assertEqual(1, len(calls), calls)
            self.assertIn(f" {self.URL} -o ", calls[0])
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            step = manifest["steps"]["update_security_audit_skill"]
            self.assertEqual("installer", step["kind"])
            self.assertEqual(self.COMMIT, step["source_version"])
            self.assertEqual([str(install), str(install / "SKILL.md")], step["paths"])
            self.assertTrue(any("--strip-components=3" in command for command in step["commands"]), step["commands"])

    def test_a_security_audit_digest_mismatch_installs_nothing_records_nothing_and_keeps_the_previous_tree(self):
        for previous in (None, "the previous tree\n"):
            with self.subTest(previous=previous), tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                payload, _ = self.archive(home)
                install = home / ".agents/skills/security-audit"
                if previous is not None:
                    install.mkdir(parents=True)
                    (install / "SKILL.md").write_text(previous)
                result = self.run_step(home, payload, "0" * 64)
                self.assertNotEqual(0, result.returncode, result.stdout)
                self.assertIn("security-audit skill checksum mismatch", result.stderr)
                self.assertEqual(1, len(self.calls(home)))
                self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")
                if previous is None:
                    self.assertFalse(install.exists(), "no partial tree")
                    self.assertEqual([], list(install.parent.iterdir()) if install.parent.exists() else [])
                else:
                    self.assertEqual(previous, (install / "SKILL.md").read_text())
                    self.assertEqual(["SKILL.md"], [path.name for path in install.iterdir()])
                    self.assertEqual(["security-audit"], [path.name for path in install.parent.iterdir()])

    def test_a_skills_directory_that_is_a_link_is_refused_before_anything_is_written_beside_it(self):
        # U283: the destination's parent must be a real directory under ~/.agents (assert_asset_destination), so a
        # staging tree, a .previous rename or an rm -rf never lands where a link points.
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            payload, digest = self.archive(home)
            outside = home / "outside"
            outside.mkdir()
            (outside / "sentinel").write_text("kept\n")
            (home / ".agents").mkdir()
            (home / ".agents/skills").symlink_to(outside)
            result = self.run_step(home, payload, digest)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"{home}/.agents/skills is a link or no directory", result.stderr)
            self.assertIn(f"refusing to write {home}/.agents/skills/security-audit", result.stderr)
            self.assertEqual(["sentinel"], [path.name for path in outside.iterdir()], "nothing beside the sentinel")
            self.assertEqual("kept\n", (outside / "sentinel").read_text())
            self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")
            self.assertEqual(["skills"], [path.name for path in (home / ".agents").iterdir()], "no staging tree")
            self.assertEqual(["curl"], [call.split()[0] for call in self.calls(home)], "the download, then nothing")

    def test_a_security_audit_tree_recorded_at_the_pin_is_skipped_and_any_other_state_is_reinstalled(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            payload, digest = self.archive(home)
            install = home / ".agents/skills/security-audit"
            manifest_path = home / ".agents/.installed-manifest.json"
            first = self.run_step(home, payload, digest)
            self.assertEqual(0, first.returncode, first.stdout + first.stderr)
            skipped = self.run_step(home, payload, digest)
            self.assertEqual(0, skipped.returncode, skipped.stdout + skipped.stderr)
            self.assertIn(f"security-audit skill {self.COMMIT} is already installed", skipped.stdout)
            self.assertEqual(1, len(self.calls(home)), "the skip downloads nothing")
            # A record at another commit is no match: the tree is replaced and the record moves to the pin.
            manifest = json.loads(manifest_path.read_text())
            manifest["steps"]["update_security_audit_skill"]["source_version"] = "0" * 40
            manifest_path.write_text(json.dumps(manifest))
            (install / "SKILL.md").write_text("an older tree\n")
            replaced = self.run_step(home, payload, digest)
            self.assertEqual(0, replaced.returncode, replaced.stdout + replaced.stderr)
            self.assertEqual(self.SKILL, (install / "SKILL.md").read_text())
            self.assertEqual(2, len(self.calls(home)))
            manifest = json.loads(manifest_path.read_text())
            self.assertEqual(self.COMMIT, manifest["steps"]["update_security_audit_skill"]["source_version"])
            # A record at the pin whose tree is gone is no match either.
            shutil.rmtree(install)
            restored = self.run_step(home, payload, digest)
            self.assertEqual(0, restored.returncode, restored.stdout + restored.stderr)
            self.assertEqual(self.SKILL, (install / "SKILL.md").read_text())
            self.assertEqual(3, len(self.calls(home)))

    def test_a_failed_or_unavailable_security_audit_download_warns_installs_nothing_and_lets_the_run_continue(self):
        # The update_terminal_code precedent: an offline host still converges. One WARN line names the step, nothing
        # is installed or recorded, the download directory is gone, the step returns 0 so main goes on. The digest and
        # archive-shape refusals below stay hard failures: a tampered archive is not a missing one.
        cases = (
            ("http failure", "return 22", None),
            ("offline", "return 6", "the previous tree\n"),
            ("no curl on PATH", None, "the previous tree\n"),
        )
        for name, body, previous in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                payload, digest = self.archive(home)
                scratch = home / "tmp"
                scratch.mkdir()
                install = home / ".agents/skills/security-audit"
                if previous is not None:
                    install.mkdir(parents=True)
                    (install / "SKILL.md").write_text(previous)
                env = {"TMPDIR": str(scratch)}
                if body is None:
                    # The step runs on a PATH that holds what it needs before the download and no curl at all.
                    bin_dir = home / "bin"
                    bin_dir.mkdir()
                    for tool in ("jq", "mktemp", "rm"):
                        (bin_dir / tool).symlink_to(shutil.which(tool))
                    body = f'unset -f curl; PATH={bin_dir}; command curl "$@"'
                result = self.run_step(home, payload, digest, curl=body, **env)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                warnings = [line for line in result.stderr.splitlines() if line.startswith("WARN")]
                self.assertEqual(1, len(warnings), result.stderr)
                self.assertIn("update_security_audit_skill", warnings[0])
                self.assertIn("nothing installed, nothing recorded", warnings[0])
                self.assertNotIn("installed into", result.stdout)
                self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")
                self.assertEqual([], list(scratch.iterdir()), "the download directory is removed")
                if previous is None:
                    self.assertFalse((home / ".agents").exists(), "nothing installed")
                else:
                    self.assertEqual(previous, (install / "SKILL.md").read_text())
                    self.assertEqual(["SKILL.md"], [path.name for path in install.iterdir()])
                    self.assertEqual(["security-audit"], [path.name for path in install.parent.iterdir()])

    def test_a_security_audit_archive_of_the_right_digest_without_the_skill_tree_is_refused_and_keeps_the_previous_tree(
        self,
    ):
        # Failure injection for the atomic replace: the digest passes, the unpack or the shape check refuses, and the
        # previous tree is byte-identical afterwards with no staging, previous or download directory left behind.
        shapes = {
            "no SKILL.md": {name: text for name, text in self.MEMBERS.items() if not name.endswith("SKILL.md")},
            "no skills/security-audit subtree": {name: text for name, text in self.MEMBERS.items() if "/" not in name},
        }
        for shape, members in shapes.items():
            for previous in (None, "the previous tree\n"):
                with self.subTest(shape=shape, previous=previous), tempfile.TemporaryDirectory() as directory:
                    home = Path(directory)
                    payload, digest = self.archive(home, members)
                    scratch = home / "tmp"
                    scratch.mkdir()
                    install = home / ".agents/skills/security-audit"
                    if previous is not None:
                        install.mkdir(parents=True)
                        (install / "SKILL.md").write_text(previous)
                    result = self.run_step(home, payload, digest, TMPDIR=str(scratch))
                    self.assertNotEqual(0, result.returncode, result.stdout)
                    self.assertNotIn("checksum mismatch", result.stderr, "the digest passed")
                    if shape == "no SKILL.md":
                        self.assertIn("holds no skills/security-audit/SKILL.md; install refused", result.stderr)
                    self.assertNotIn("installed into", result.stdout)
                    self.assertEqual(1, len(self.calls(home)))
                    self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")
                    self.assertEqual([], list(scratch.iterdir()), "the download directory is removed")
                    if previous is None:
                        self.assertFalse(install.exists(), "no partial tree")
                        self.assertEqual([], list(install.parent.iterdir()), "no staging tree beside the target")
                    else:
                        self.assertEqual(previous, (install / "SKILL.md").read_text())
                        self.assertEqual(["SKILL.md"], [path.name for path in install.iterdir()])
                        self.assertEqual(["security-audit"], [path.name for path in install.parent.iterdir()])


class DeepseekHarnessTest(unittest.TestCase):
    """update_deepseek_harness over an archive built here, never downloaded (U172): the opt-in, the digest check before
    anything is unpacked, the archive version check, the build inside the new tree, the wrapper, the profile's plugin
    install and the manifest record the doctor reads. mise is a stub that logs its arguments, so no pnpm runs. Round 2
    (U172c): each producer the step reads gets a failure injection that prints the right value and exits 77, and the
    already-installed check converges. Round 3 (U172d): a relative DSH_HOME and one the step cannot enter, a current
    that is a real directory, the wrapper's single-quoted home and the EXIT trap after a failed record. U178: the step
    is one transaction. The tree is built whole under dsh/<tag>.<suffix>, the profile install runs before anything the
    host runs changes, the wrapper is replaced by a rename, current is pointed at the new tree by one link call, the
    record is written and only then are the older trees pruned; every producer (two pwd -P, the receipt as a JSON
    object and its row, three jq, shasum, two readlink, three mktemp) has an injection that refuses the step. Round 2
    (U178b): current is linked before the wrapper is renamed, a failed link or rename after it puts current back on
    its prior target, a failed restore keeps the tree current names, the download directory goes before the profile
    install, bin/dsh must be a regular file and the receipt exactly one object, bin/ is made in repair mode too, and
    the prune (dsh_prune_older) removes only the step's own name shapes, on the already-installed path as well. Round 3
    (U178c): the step accepts exactly one layout and refuses every other before any download (current absent or a
    symlink to a non-symlink directory directly under dsh/), so the prune resolves no path; the already-installed exit
    rewrites a receipt whose paths are not this layout's two before it prunes; no cleanup changes the exit status; a
    restore that left current absent says so. Round 4 (U178d): every input the step reads is a row of one table,
    checked by type and by identity (-ef, a jq array comparison) before any download; a bin/ or dsh/ that is a symlink,
    a profile that is not the rendered directory, a current whose target name ends in a newline or is not dsh-v*, a
    directory, a FIFO or a symlink at the receipt path, and a paths array that equals the two only as joined text each
    have a refusal or rewrite test here. U227b: the dsh-omp-gateway plugin link (one relative symlink in the profile's
    node_modules, written on the install, the repair and the already-installed exit) is created, converges on every
    run, is recorded, and is refused before any download when the plugin directory is absent or the link path is
    not a symlink. Round 3 (U227c): the link joins the two physical paths (a symlinked profiles/ parent gets a target
    that resolves; a plugin or a profile that resolves outside DSH_HOME is refused before any download) and is
    written beside its name and renamed into place, so a failed relink leaves the previous link standing."""

    # The rendered pin; a tree without the constant (the red proof against origin/main) gets a placeholder so the
    # module still imports and the tests themselves fail on the absent step.
    TAG_MATCH = re.search(r'^DSH_PIN_TAG="([^"]+)"$', INSTALLER_PINS, re.MULTILINE)
    TAG = TAG_MATCH[1] if TAG_MATCH else "dsh-v0.0.0"
    URL = f"https://github.com/deepseek-ai/deepseek-harness/archive/refs/tags/{TAG}.tar.gz"
    COMMIT_MATCH = re.search(r'^DSH_COMMIT="([^"]+)"$', INSTALLER_PINS, re.MULTILINE)
    COMMIT = COMMIT_MATCH[1] if COMMIT_MATCH else ""
    BUILD_CALLS = [
        "mise exec -- pnpm install --frozen-lockfile",
        "mise exec -- pnpm run build",
        "mise exec -- pnpm install",
    ]

    def archive(self, home: Path, version: str | None = None) -> tuple[Path, str]:
        """A GitHub tag archive: <repository>-<tag>/{package.json, apps/cli/lib/bin.js, pnpm-lock.yaml}."""
        version = self.TAG.removeprefix("dsh-v") if version is None else version
        members = {
            "package.json": json.dumps({"name": "deepseek-harness", "version": version}) + "\n",
            "apps/cli/lib/bin.js": "// fixture cli\n",
            "pnpm-lock.yaml": "lockfileVersion: '9.0'\n",
        }
        payload = home / "archive.tgz"
        with tarfile.open(payload, "w:gz") as tar:
            for name, text in members.items():
                data = text.encode()
                info = tarfile.TarInfo(f"deepseek-harness-{self.TAG}/{name}")
                info.size = len(data)
                tar.addfile(info, io.BytesIO(data))
        return payload, hashlib.sha256(payload.read_bytes()).hexdigest()

    def opted_in_home(self, directory: str) -> tuple[Path, Path]:
        """A scratch HOME with ~/.dsh created (the opt-in), the deployed thak profile beside the install and the
        deployed dsh-omp-gateway plugin the profile links."""
        home = Path(directory)
        dsh_home = home / ".dsh"
        (dsh_home / "profiles/thak").mkdir(parents=True)
        (dsh_home / "profiles/thak/package.json").write_text('{"name": "thak"}\n')
        (dsh_home / "plugins/omp-gateway").mkdir(parents=True)
        (dsh_home / "plugins/omp-gateway/package.json").write_text('{"name": "dsh-omp-gateway"}\n')
        (home / "tmp").mkdir()
        return home, dsh_home

    def plugin_link(self, dsh_home: Path) -> Path:
        return dsh_home / "profiles/thak/node_modules/dsh-omp-gateway"

    def assert_plugin_linked(self, dsh_home: Path) -> None:
        """The link as the step makes it: a symlink whose text is the relative target, reaching the deployed plugin."""
        link = self.plugin_link(dsh_home)
        self.assertTrue(link.is_symlink(), f"{link} is a symlink")
        self.assertEqual("../../../plugins/omp-gateway", os.readlink(link), "the target is relative")
        self.assertEqual((dsh_home / "plugins/omp-gateway").resolve(), link.resolve())
        self.assertEqual('{"name": "dsh-omp-gateway"}\n', (link / "package.json").read_text())

    def run_step(
        self,
        home: Path,
        payload: Path,
        digest: str,
        *,
        dsh_home: Path | None,
        curl: str | None = None,
        mise: str | None = None,
        shasum: str | None = None,
        jq: str | None = None,
        manifest_record: str | None = None,
        prelude: str | None = None,
        cwd: Path | None = None,
    ):
        # curl is a shell function that writes $PAYLOAD to its -o path and logs its arguments; mise logs its arguments,
        # writes the DSH_CLIENT_COMMIT_HASH the build call sees (or <unset>) to $HOME/build-commit, and succeeds unless
        # a test hands it a body; nothing is downloaded, built or installed through pnpm. shasum and jq are the real
        # producers unless a test hands one a body (a failure injection over `command shasum` or `command jq`). The
        # prelude is any shell text placed before the stubs: a test defines pwd, readlink, mktemp, bash, ln or mv there
        # as functions (failing_call makes one whose n-th call fails), or overrides a sourced pin such as DSH_COMMIT.
        download = curl or 'cp "$PAYLOAD" "${@: -1}"'
        stubs = (
            f"DSH_ARCHIVE_SHA256={digest}; "
            'curl() { echo "curl $*" >> "$CALLS"; ' + download + "; }; "
            'mise() { echo "mise $*" >> "$CALLS"; '
            'if [ "$*" = "exec -- pnpm run build" ]; then '
            'printf "%s\\n" "${DSH_CLIENT_COMMIT_HASH-<unset>}" > "$HOME/build-commit"; fi; '
            + (mise or "return 0")
            + "; }; "
            + (f"shasum() {{ {shasum}; }}; " if shasum else "")
            + (f"jq() {{ {jq}; }}; " if jq else "")
            + (f"manifest_record() {{ {manifest_record}; }}; " if manifest_record else "")
        )
        env = os.environ | {"HOME": str(home), "PAYLOAD": str(payload), "CALLS": str(home / "calls")}
        if (home / "tmp").is_dir():
            env["TMPDIR"] = str(home / "tmp")
        env.pop("DSH_HOME", None)
        if dsh_home is not None:
            env["DSH_HOME"] = str(dsh_home)
        script = 'source "$1"; ' + (prelude + "\n" if prelude else "") + stubs + "update_deepseek_harness"
        return subprocess.run(
            ["bash", "-c", script, "bash", str(UPDATER)],
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def failing_call(self, name: str, nth: int, on_failure: str, real: str | None = None) -> str:
        """`name` as a shell function for run_step's prelude: its n-th call runs `on_failure` (text that prints what a
        healthy call prints and returns non-zero), every other call runs the real command. The counter is a file under
        the scratch HOME, so the subshells the step reads in share it."""
        real = real or f"command {name}"
        return (
            f'{name}() {{ local n; n="$(cat "$HOME/{name}-calls" 2> /dev/null || echo 0)"; n=$((n + 1)); '
            f'printf "%s\\n" "$n" > "$HOME/{name}-calls"; if [ "$n" -eq {nth} ]; then {on_failure}; fi; {real} "$@"; }}'
        )

    def calls(self, home: Path) -> list[str]:
        log = home / "calls"
        return log.read_text().splitlines() if log.exists() else []

    def installed_tree(self, dsh_home: Path) -> Path:
        """The tree current resolves to: a directory under dsh/ named <tag>.<suffix>, the one layout the step makes."""
        current = dsh_home / "dsh/current"
        self.assertTrue(current.is_symlink(), "current is a symlink")
        tree = Path(os.readlink(current))
        self.assertEqual(dsh_home / "dsh", tree.parent)
        self.assertTrue(tree.name.startswith(f"{self.TAG}."), tree.name)
        self.assertTrue(tree.is_dir() and not tree.is_symlink(), "current resolves to a directory")
        return tree

    def test_without_the_opt_in_the_step_skips_downloads_nothing_and_creates_nothing(self):
        for case in ("DSH_HOME unset", "DSH_HOME names no directory"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                payload, digest = self.archive(home)
                dsh_home = None if case == "DSH_HOME unset" else home / ".dsh"
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("Skipping DeepSeek harness: DSH_HOME is unset or names no directory", result.stdout)
                self.assertEqual([], self.calls(home))
                self.assertFalse((home / ".dsh").exists())
                self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_a_dsh_home_elsewhere_than_the_rendered_profile_warns_and_installs_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            payload, digest = self.archive(home)
            elsewhere = home / "elsewhere"
            elsewhere.mkdir()
            result = self.run_step(home, payload, digest, dsh_home=elsewhere)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            warnings = [line for line in result.stderr.splitlines() if line.startswith("WARN")]
            self.assertEqual(1, len(warnings), result.stderr)
            self.assertIn("update_deepseek_harness", warnings[0])
            self.assertIn(str(elsewhere), warnings[0])
            self.assertIn(str(home / ".dsh"), warnings[0])
            self.assertEqual([], self.calls(home), "no download")
            self.assertEqual([], list(elsewhere.iterdir()))
            self.assertFalse((home / ".dsh").exists())

    def test_a_reference_path_whose_physical_path_cannot_be_read_refuses_the_step(self):
        # Round-3 defect: a failed `cd ~/.dsh` became expected="" and a WARN with exit 0, so an unreadable reference
        # path passed as "elsewhere". The second pwd -P is the reference path's; the first, DSH_HOME's, answers.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            prelude = self.failing_call("pwd", 2, 'builtin pwd "$@"; return 77', real="builtin pwd")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"the reference path {home}/.dsh could not be read; step refused", result.stderr)
            self.assertEqual([], [line for line in result.stderr.splitlines() if line.startswith("WARN")])
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertEqual(
                ["plugins", "profiles"], sorted(path.name for path in dsh_home.iterdir()), "nothing installed"
            )
            self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_a_failed_download_warns_installs_nothing_records_nothing_and_lets_the_run_continue(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, curl="return 22")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            warnings = [line for line in result.stderr.splitlines() if line.startswith("WARN")]
            self.assertEqual(1, len(warnings), result.stderr)
            self.assertIn("update_deepseek_harness", warnings[0])
            self.assertIn(self.URL, warnings[0])
            self.assertIn("nothing installed, nothing recorded", warnings[0])
            self.assertEqual(1, len(self.calls(home)))
            self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")
            self.assertEqual(["plugins", "profiles"], sorted(path.name for path in dsh_home.iterdir()))
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_digest_mismatch_fails_before_anything_is_unpacked_or_built(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, _ = self.archive(home)
            result = self.run_step(home, payload, "0" * 64, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("DeepSeek harness checksum mismatch: expected " + "0" * 64, result.stderr)
            self.assertEqual(1, len(self.calls(home)), "one download, no mise call")
            self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked")
            self.assertFalse((dsh_home / "bin").exists())
            self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_an_archive_whose_version_is_not_the_pin_is_refused_before_the_build(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home, version="0.0.0")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"archive version 0.0.0 is not the pin {self.TAG.removeprefix('dsh-v')}; install refused", result.stderr
            )
            self.assertEqual(1, len(self.calls(home)), "one download, no mise call")
            self.assertEqual([], list((dsh_home / "dsh").iterdir()), "the new tree is removed")
            self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")

    def test_every_mise_exec_runs_with_automatic_tool_installation_off(self):
        # U283 (verdicts/U276b): a Node or pnpm mise has not installed must refuse the build, not land in mise's tool
        # trees; mise 2026.10.25's `mise exec --help` names exec_auto_install as the setting, MISE_EXEC_AUTO_INSTALL
        # its variable. The stub records the value each call sees.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            mise = 'printf "%s\\n" "${MISE_EXEC_AUTO_INSTALL-<unset>}" >> "$HOME/auto-install"; return 0'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, mise=mise)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(self.BUILD_CALLS, [call for call in self.calls(home) if call.startswith("mise ")])
            self.assertEqual(["false"] * len(self.BUILD_CALLS), (home / "auto-install").read_text().splitlines())

    def test_a_failed_build_leaves_no_install_no_wrapper_and_no_record(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            failing = 'case "$*" in *"run build"*) return 1 ;; esac; return 0'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, mise=failing)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertEqual(self.BUILD_CALLS[:2], [call for call in self.calls(home) if call.startswith("mise ")])
            self.assertEqual([], list((dsh_home / "dsh").iterdir()), "the new tree is removed")
            self.assertFalse((dsh_home / "dsh/current").is_symlink(), "no current link")
            self.assertFalse((dsh_home / "bin/dsh").exists(), "no wrapper")
            self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")

    def test_the_pinned_archive_installs_under_dsh_home_links_current_writes_the_wrapper_and_records_the_step(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            install = self.installed_tree(dsh_home)
            self.assertIn(f"DeepSeek harness {self.TAG} installed into {install}.", result.stdout)
            self.assertEqual(
                self.TAG.removeprefix("dsh-v"), json.loads((install / "package.json").read_text())["version"]
            )
            self.assertTrue((install / "apps/cli/lib/bin.js").is_file())
            wrapper = dsh_home / "bin/dsh"
            self.assertTrue(os.access(wrapper, os.X_OK), "the wrapper is executable")
            # mktemp makes the temporary at 0600, so the mode is set, not added: the wrapper is a program, not a secret.
            self.assertEqual(0o755, wrapper.stat().st_mode & 0o777)
            self.assertEqual(
                f"#!/bin/bash\nexec mise exec -- node '{dsh_home}'/dsh/current/apps/cli/lib/bin.js \"$@\"\n",
                wrapper.read_text(),
            )
            self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no wrapper temporary")
            calls = self.calls(home)
            self.assertEqual(1, len([call for call in calls if call.startswith("curl ")]))
            self.assertIn(f" {self.URL} -o ", calls[0])
            self.assertEqual(self.BUILD_CALLS, [call for call in calls if call.startswith("mise ")])
            # The tag archive has no .git, so the build reads the commit from DSH_CLIENT_COMMIT_HASH, the rendered pin.
            self.assertEqual(f"{self.COMMIT}\n", (home / "build-commit").read_text())
            # Nothing beside the one tree under dsh/: no staging, previous or failed tree.
            self.assertEqual(["current", install.name], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            step = manifest["steps"]["update_deepseek_harness"]
            self.assertEqual("installer", step["kind"])
            self.assertEqual(self.TAG, step["source_version"])
            # The recorded paths exist whatever the tree's name: the doctor reads them.
            self.assertEqual([str(dsh_home / "dsh/current"), str(wrapper)], step["paths"])
            self.assertTrue(all(Path(path).exists() for path in step["paths"]), step["paths"])
            self.assertTrue(any("--strip-components=1" in command for command in step["commands"]), step["commands"])
            self.assertTrue(any(command.startswith("mktemp -d ") for command in step["commands"]), step["commands"])
            # A second run finds the record and the tree current names: nothing is downloaded again.
            skipped = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, skipped.returncode, skipped.stdout + skipped.stderr)
            self.assertIn(f"DeepSeek harness {self.TAG} is already installed", skipped.stdout)
            self.assertEqual(calls, self.calls(home), "the skip downloads nothing and runs no mise")
            self.assertEqual(install, self.installed_tree(dsh_home), "the skip keeps the tree")

    def test_the_plugin_link_is_a_relative_symlink_in_the_profile_recorded_and_converged_on_every_run(self):
        # U227b: `dsh plugin add link:` fails on the mise pnpm shim, so the step writes the link itself; relative, so a
        # DSH_HOME moved whole keeps working. The already-installed exit and the repair relink it, so a host that
        # installed before the row existed, or one whose link was pointed elsewhere, converges without a download.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assert_plugin_linked(dsh_home)
            step = json.loads((home / ".agents/.installed-manifest.json").read_text())["steps"][
                "update_deepseek_harness"
            ]
            self.assertIn("ln -s ../../../plugins/omp-gateway <link tmp>", step["commands"])
            self.assertIn(
                f"os.replace <link tmp> {(dsh_home / 'profiles/thak/node_modules').resolve()}/dsh-omp-gateway"
                f" (resolves to {(dsh_home / 'plugins/omp-gateway').resolve()})",
                step["commands"],
                "the receipt records the physical target",
            )
            calls = self.calls(home)
            receipt = (home / ".agents/.installed-manifest.json").read_text()
            for case in ("as it was", "pointed elsewhere", "dangling", "node_modules gone", "the wrapper gone"):
                with self.subTest(case=case):
                    link = self.plugin_link(dsh_home)
                    if case == "pointed elsewhere":
                        link.unlink()
                        os.symlink(home / "own-profile", link)
                    elif case == "dangling":
                        link.unlink()
                        os.symlink("../../../plugins/gone", link)
                    elif case == "node_modules gone":
                        shutil.rmtree(link.parent)
                    elif case == "the wrapper gone":
                        (dsh_home / "bin/dsh").unlink()
                    again = self.run_step(home, payload, digest, dsh_home=dsh_home)
                    self.assertEqual(0, again.returncode, again.stdout + again.stderr)
                    if case == "the wrapper gone":
                        self.assertIn("its wrapper is rewritten", again.stdout)
                    else:
                        self.assertIn(f"DeepSeek harness {self.TAG} is already installed", again.stdout)
                        self.assertEqual(receipt, (home / ".agents/.installed-manifest.json").read_text())
                    self.assertEqual(calls, self.calls(home), "no download, no mise call")
                    self.assert_plugin_linked(dsh_home)

    def test_a_missing_plugin_directory_refuses_the_step_before_any_download(self):
        # The plugins/omp-gateway row: the link's one target is what chezmoi deploys; without it the profile could reach
        # no model, so nothing is installed and a prior install is left as it is.
        for case, prior in (("absent", False), ("a file", False), ("absent over a prior install", True)):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                plugin = dsh_home / "plugins/omp-gateway"
                shutil.rmtree(plugin)
                if case == "a file":
                    plugin.write_text("not a directory\n")
                if prior:
                    install, previous = self.previous_install(dsh_home)
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(
                    f"update_deepseek_harness: {plugin} is absent or not a directory; the thak profile loads the"
                    " dsh-omp-gateway plugin from there (chezmoi apply deploys it; then rerun make update); nothing"
                    " installed, nothing recorded.",
                    result.stderr,
                )
                self.assertEqual([], self.calls(home), "no curl call, no mise call")
                self.assertFalse(self.plugin_link(dsh_home).parent.exists(), "no node_modules made")
                self.assertFalse((dsh_home / "bin").exists(), "no wrapper")
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                if prior:
                    self.assert_previous_install_untouched(dsh_home, install, previous)
                else:
                    self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked, no current link")
                if case == "a file":
                    self.assertEqual("not a directory\n", plugin.read_text(), "the file as it was")

    def test_a_node_modules_that_is_not_a_directory_or_a_link_path_that_is_not_a_symlink_is_refused(self):
        # ln -sfn onto a real directory makes a link inside it and succeeds, and node_modules is pnpm's directory, so
        # a symlink or a file at either path is refused before any download, and left as it is.
        node_modules = Path("profiles/thak/node_modules")
        for case in (
            "node_modules a symlink",
            "node_modules a file",
            "the link path a directory",
            "the link path a file",
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                elsewhere = home / "elsewhere"
                elsewhere.mkdir()
                if case == "node_modules a symlink":
                    os.symlink(elsewhere, dsh_home / node_modules)
                    path, state = dsh_home / node_modules, "a symlink or not a directory"
                elif case == "node_modules a file":
                    (dsh_home / node_modules).write_text("not a directory\n")
                    path, state = dsh_home / node_modules, "a symlink or not a directory"
                else:
                    (dsh_home / node_modules).mkdir()
                    path, state = self.plugin_link(dsh_home), "not a symlink"
                    if case == "the link path a directory":
                        path.mkdir()
                    else:
                        path.write_text("not a symlink\n")
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"update_deepseek_harness: {path} is {state}; the step ", result.stderr)
                self.assertIn(
                    "(move it aside and rerun make update); nothing installed, nothing recorded.", result.stderr
                )
                self.assertEqual([], self.calls(home), "no curl call, no mise call")
                self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked, no current link")
                self.assertFalse((dsh_home / "bin").exists(), "no wrapper")
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                if case == "node_modules a symlink":
                    self.assertTrue((dsh_home / node_modules).is_symlink(), "the symlink as it was")
                    self.assertEqual([], list(elsewhere.iterdir()), "nothing written through it")
                elif case == "the link path a directory":
                    self.assertEqual([], list(path.iterdir()), "no link made inside the directory")
                else:
                    self.assertIn("not a", path.read_text(), "the file as it was")

    def test_a_plugin_link_that_cannot_be_written_leaves_current_the_wrapper_the_trees_and_the_receipt_as_they_were(
        self,
    ):
        # The link is written after the profile install and before anything the host runs changes, so its failure
        # needs no rollback on the install; on the already-installed exit it keeps the receipt and the older trees.
        prelude = (
            'ln() { case "${@: -1}" in */node_modules/dsh-omp-gateway.tmp.*) return 77 ;; esac; command ln "$@"; }'
        )
        with self.subTest(path="the install"), tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"update_deepseek_harness: the plugin link {self.plugin_link(dsh_home)} could not be written (its"
                f" temporary {self.plugin_link(dsh_home)}.tmp.",
                result.stderr,
            )
            self.assertIn(
                "the previous link is untouched; nothing recorded; current, the wrapper and the older trees are"
                " untouched.",
                result.stderr,
            )
            self.assertEqual(self.BUILD_CALLS, [call for call in self.calls(home) if call.startswith("mise ")])
            self.assert_previous_install_untouched(dsh_home, install, previous)
            self.assertFalse(self.plugin_link(dsh_home).exists(), "no link")
            self.assertEqual([], list(self.plugin_link(dsh_home).parent.iterdir()), "no temporary beside it")
            self.assertFalse((dsh_home / "bin/dsh").exists(), "no wrapper")
            self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")
        with self.subTest(path="the already-installed exit"), tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            tree, text = self.canonical_install(dsh_home)
            older = dsh_home / "dsh" / self.TAG
            older.mkdir()
            wrapper, wrapper_text = self.own_wrapper(dsh_home)
            _, receipt = self.receipt(home, self.TAG)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"DeepSeek harness {self.TAG} is already installed", result.stdout)
            self.assertIn(
                f"update_deepseek_harness: the plugin link {self.plugin_link(dsh_home)} could not be written (its"
                f" temporary {self.plugin_link(dsh_home)}.tmp.",
                result.stderr,
            )
            self.assertIn("the previous link is untouched; the receipt and the older trees are kept.", result.stderr)
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            self.assertEqual(receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was")
            self.assertEqual(["current", self.TAG, tree.name], sorted(p.name for p in (dsh_home / "dsh").iterdir()))
            self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")
            self.assertEqual(wrapper_text, wrapper.read_text(), "the wrapper as it was")

    def test_a_symlinked_profiles_parent_gets_a_link_that_resolves_and_one_outside_dsh_home_is_refused(self):
        # Round-3 finding f1 s5: the constant target ../../../plugins/omp-gateway counted three levels from the link's
        # logical path, so a profiles/ that is a symlink elsewhere passed every row and left a dangling link with exit
        # 0. The target is now computed between the two physical paths; a profile that resolves outside DSH_HOME is
        # refused before any download, since the step links the plugin only inside DSH_HOME.
        for case in ("under DSH_HOME", "outside DSH_HOME"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                store = dsh_home / "store" if case == "under DSH_HOME" else home / "elsewhere"
                store.mkdir()
                shutil.move(dsh_home / "profiles", store / "profiles")
                os.symlink(store / "profiles", dsh_home / "profiles")
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                link = self.plugin_link(dsh_home)
                if case == "under DSH_HOME":
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    self.installed_tree(dsh_home)
                    self.assertTrue(link.is_symlink(), f"{link} is a symlink")
                    self.assertEqual(
                        "../../../../plugins/omp-gateway", os.readlink(link), "counted from the physical place"
                    )
                    self.assertEqual((dsh_home / "plugins/omp-gateway").resolve(), link.resolve())
                    self.assertEqual('{"name": "dsh-omp-gateway"}\n', (link / "package.json").read_text())
                    step = json.loads((home / ".agents/.installed-manifest.json").read_text())["steps"][
                        "update_deepseek_harness"
                    ]
                    self.assertIn("ln -s ../../../../plugins/omp-gateway <link tmp>", step["commands"])
                    again = self.run_step(home, payload, digest, dsh_home=dsh_home)
                    self.assertEqual(0, again.returncode, again.stdout + again.stderr)
                    self.assertIn(f"DeepSeek harness {self.TAG} is already installed", again.stdout)
                    self.assertEqual("../../../../plugins/omp-gateway", os.readlink(link), "converged")
                else:
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn(
                        f"update_deepseek_harness: {dsh_home}/profiles/thak resolves to"
                        f" {(store / 'profiles/thak').resolve()}, outside {dsh_home.resolve()}; the step links the"
                        " plugin only into a profile under DSH_HOME (move the profile back and rerun make update);"
                        " nothing installed, nothing recorded.",
                        result.stderr,
                    )
                    self.assertEqual([], self.calls(home), "no download, no mise call")
                    self.assertEqual(
                        ["package.json"],
                        [path.name for path in (store / "profiles/thak").iterdir()],
                        "nothing made under the profile",
                    )
                    self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked, no current link")
                    self.assertFalse((dsh_home / "bin").exists(), "no wrapper")
                    self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_a_plugin_directory_that_resolves_outside_dsh_home_is_refused_and_one_inside_is_linked_physically(self):
        # Round-3 finding f1 s6: -d follows a symlink, so a plugins/omp-gateway linked to a directory outside DSH_HOME
        # was accepted and a turn would import whatever stands there. The plugin's physical path must lie under
        # DSH_HOME's; a link to another directory under DSH_HOME is accepted and the link is written to that physical
        # directory.
        for case in ("outside DSH_HOME", "under DSH_HOME"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                plugin = dsh_home / "plugins/omp-gateway"
                real = home / "external-plugin" if case == "outside DSH_HOME" else dsh_home / "plugins/omp-gateway-real"
                shutil.move(plugin, real)
                os.symlink(real, plugin)
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                if case == "outside DSH_HOME":
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn(
                        f"update_deepseek_harness: {plugin} resolves to {real.resolve()}, outside {dsh_home.resolve()};"
                        " the thak profile loads the dsh-omp-gateway plugin only from a directory under DSH_HOME"
                        " (chezmoi apply deploys it there; move the link aside and rerun make update); nothing"
                        " installed, nothing recorded.",
                        result.stderr,
                    )
                    self.assertEqual([], self.calls(home), "no download, no mise call")
                    self.assertEqual(
                        ["package.json"],
                        [path.name for path in (dsh_home / "profiles/thak").iterdir()],
                        "nothing under the profile changed",
                    )
                    self.assertEqual(real, Path(os.readlink(plugin)), "the plugin link as it was")
                    self.assertEqual(["package.json"], [path.name for path in real.iterdir()], "nothing written there")
                    self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked, no current link")
                    self.assertFalse((dsh_home / "bin").exists(), "no wrapper")
                    self.assertFalse((home / ".agents").exists(), "nothing recorded")
                else:
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    link = self.plugin_link(dsh_home)
                    self.assertEqual("../../../plugins/omp-gateway-real", os.readlink(link), "the physical directory")
                    self.assertEqual(real.resolve(), link.resolve())
                    self.assertEqual('{"name": "dsh-omp-gateway"}\n', (link / "package.json").read_text())

    def test_a_relink_that_fails_leaves_the_previous_link_standing_and_names_the_state(self):
        # Round-3 finding f2 s4: ln -sfn unlinked the previous link before it failed, so the live profile lost its
        # plugin, and the failure test injected before the unlink. The link is now a temporary beside the name renamed
        # into place: a failure at the temporary (node_modules read-only) or at the rename (the python3 rename call
        # fails) leaves the previous link as it was, by inode, with no temporary beside it, and exits 1 naming the state.
        rename_fails = (
            'python3() { case "${@: -1}" in */node_modules/dsh-omp-gateway) return 77 ;; esac; command python3 "$@"; }'
        )
        for case in ("the rename fails", "node_modules is read-only"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                if case == "node_modules is read-only" and os.geteuid() == 0:
                    self.skipTest("root writes into a read-only directory")
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                tree, text = self.canonical_install(dsh_home)
                wrapper, wrapper_text = self.own_wrapper(dsh_home)
                _, receipt = self.receipt(home, self.TAG)
                link = self.plugin_link(dsh_home)
                link.parent.mkdir()
                os.symlink("../../../plugins/omp-gateway", link)
                before = os.lstat(link)
                try:
                    if case == "node_modules is read-only":
                        link.parent.chmod(0o555)
                    prelude = rename_fails if case == "the rename fails" else None
                    result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
                finally:
                    link.parent.chmod(0o755)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"DeepSeek harness {self.TAG} is already installed", result.stdout)
                failed = (
                    f"could not be renamed into place from {link}.tmp."
                    if case == "the rename fails"
                    else f"could not be written (its temporary {link}.tmp."
                )
                self.assertIn(f"update_deepseek_harness: the plugin link {link} {failed}", result.stderr)
                self.assertIn("the previous link is untouched", result.stderr)
                self.assertIn("the receipt and the older trees are kept.", result.stderr)
                self.assertTrue(link.is_symlink(), "the previous link stands")
                self.assertEqual("../../../plugins/omp-gateway", os.readlink(link))
                self.assertEqual('{"name": "dsh-omp-gateway"}\n', (link / "package.json").read_text(), "and resolves")
                self.assertEqual(before.st_ino, os.lstat(link).st_ino, "the same inode: never unlinked")
                self.assertEqual(["dsh-omp-gateway"], [path.name for path in link.parent.iterdir()], "no temporary")
                self.assertEqual([], self.calls(home), "no download, no mise call")
                self.assertEqual(
                    receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was"
                )
                self.assertEqual(wrapper_text, wrapper.read_text(), "the wrapper as it was")
                self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")

    def test_a_real_directory_at_the_link_name_is_refused_and_left_alone_on_the_already_installed_exit(self):
        # A rename onto a real directory would move the temporary inside it, so a directory at the link name is refused
        # before anything is written and its contents stay as they were. The U227b refusal test covers the fresh host;
        # this is the installed host, whose rows are read before the receipt.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            tree, text = self.canonical_install(dsh_home)
            wrapper, wrapper_text = self.own_wrapper(dsh_home)
            _, receipt = self.receipt(home, self.TAG)
            link = self.plugin_link(dsh_home)
            link.mkdir(parents=True)
            (link / "index.js").write_text("// the operator's own\n")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"update_deepseek_harness: {link} is not a symlink; the step refuses to replace it (move it aside and"
                " rerun make update); nothing installed, nothing recorded.",
                result.stderr,
            )
            self.assertNotIn("is already installed", result.stdout, "refused before the receipt is read")
            self.assertTrue(link.is_dir() and not link.is_symlink(), "the directory as it was")
            self.assertEqual("// the operator's own\n", (link / "index.js").read_text())
            self.assertEqual(["index.js"], [path.name for path in link.iterdir()], "nothing moved inside it")
            self.assertEqual(["dsh-omp-gateway"], [path.name for path in link.parent.iterdir()], "no temporary")
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertEqual(receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was")
            self.assertEqual(wrapper_text, wrapper.read_text(), "the wrapper as it was")
            self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")

    def test_the_build_sees_the_pinned_commit_as_dsh_client_commit_hash_and_the_receipt_names_it(self):
        # The first host install of 2026-11-06 failed in `pnpm run build`: the upstream build runs `git rev-parse HEAD`
        # unless DSH_CLIENT_COMMIT_HASH is set, and the tag archive carries no .git.
        self.assertRegex(self.COMMIT, r"^[0-9a-f]{40}$", "installer-pins.sh renders DSH_COMMIT from ref_commit")
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(f"{self.COMMIT}\n", (home / "build-commit").read_text())
            commands = json.loads((home / ".agents/.installed-manifest.json").read_text())["steps"][
                "update_deepseek_harness"
            ]["commands"]
            self.assertIn(f"DSH_CLIENT_COMMIT_HASH={self.COMMIT} pnpm run build", commands)
            self.assertNotIn("pnpm run build", commands)

    def assert_commit_refused(self, prelude: str, given: str) -> None:
        """The step with DSH_COMMIT overridden by `prelude` refuses before any download, build or record."""
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "update_deepseek_harness: DSH_COMMIT (assets.deepseek-harness ref_commit, rendered into "
                f"scripts/lib/installer-pins.sh) is unset or not 40 lowercase hex ({given} given), so the build has no "
                "DSH_CLIENT_COMMIT_HASH; nothing installed, nothing recorded.",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no curl and no mise call")
            self.assertFalse((home / "build-commit").exists(), "no build ran")
            self.assertEqual(
                ["plugins", "profiles"], sorted(path.name for path in dsh_home.iterdir()), "nothing installed"
            )
            self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_an_empty_or_unset_dsh_commit_refuses_the_step_before_any_download(self):
        for prelude in ("DSH_COMMIT=", "unset DSH_COMMIT"):
            with self.subTest(prelude=prelude):
                self.assert_commit_refused(prelude, "")

    def test_a_dsh_commit_that_is_not_40_lowercase_hex_refuses_the_step_before_any_download(self):
        for value in ("not-a-sha", self.COMMIT.upper(), self.COMMIT[:-1], f"{self.COMMIT}0"):
            with self.subTest(value=value):
                self.assert_commit_refused(f"DSH_COMMIT={value}", value)

    def receipt(self, home: Path, version: str, paths: list[str] | None = None) -> tuple[Path, str]:
        """The installed-manifest receipt recording the step at `version` with `paths` (this layout's two unless a test
        hands it the earlier form), and its text as written."""
        path = home / ".agents/.installed-manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        paths = [f"{home}/.dsh/dsh/current", f"{home}/.dsh/bin/dsh"] if paths is None else paths
        text = json.dumps({"steps": {"update_deepseek_harness": {"source_version": version, "paths": paths}}}) + "\n"
        path.write_text(text)
        return path, text

    def previous_install(self, dsh_home: Path) -> tuple[Path, str]:
        """The layout a host carries from U172: a tree at dsh/<tag> itself with current linked to it; its package.json
        carries a version of its own so a test can tell it from the archive's tree."""
        install = dsh_home / "dsh" / self.TAG
        install.mkdir(parents=True)
        text = json.dumps({"name": "deepseek-harness", "version": "previous"}) + "\n"
        (install / "package.json").write_text(text)
        os.symlink(install, dsh_home / "dsh/current")
        return install, text

    def own_wrapper(self, dsh_home: Path) -> tuple[Path, str]:
        """A live wrapper the operator already has, so a test can tell whether the step changed one byte of it."""
        wrapper = dsh_home / "bin/dsh"
        wrapper.parent.mkdir(parents=True, exist_ok=True)
        text = "#!/bin/bash\necho 'the wrapper before this run'\n"
        wrapper.write_text(text)
        wrapper.chmod(0o755)
        return wrapper, text

    def assert_nothing_installed_or_recorded(self, home: Path, dsh_home: Path, receipt: str | None = None) -> None:
        """No tree and no current link under dsh/, no wrapper, and the receipt file as it was (or absent)."""
        if (dsh_home / "dsh").exists():
            self.assertEqual([], list((dsh_home / "dsh").iterdir()), "no tree, no current link")
        self.assertFalse((dsh_home / "dsh/current").is_symlink(), "no current link")
        self.assertFalse((dsh_home / "bin/dsh").exists(), "no wrapper")
        manifest = home / ".agents/.installed-manifest.json"
        if receipt is None:
            self.assertFalse(manifest.exists(), "nothing recorded")
        else:
            self.assertEqual(receipt, manifest.read_text(), "the receipt is unchanged")

    def assert_previous_install_untouched(self, dsh_home: Path, install: Path, text: str) -> None:
        """The U172 layout as previous_install made it: current on dsh/<tag>, its package.json as written, and no tree
        of the new layout beside it."""
        self.assertEqual(str(install), os.readlink(dsh_home / "dsh/current"), "current is on the prior tree")
        self.assertEqual(text, (install / "package.json").read_text(), "the prior tree is as it was")
        self.assertEqual(["current", self.TAG], sorted(path.name for path in (dsh_home / "dsh").iterdir()))

    def test_a_digest_producer_that_prints_the_right_digest_and_exits_nonzero_refuses_the_install(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, shasum='command shasum "$@"; exit 77')
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("the digest of the downloaded archive could not be read; install refused", result.stderr)
            self.assertNotIn("installed into", result.stdout)
            self.assertEqual(1, len(self.calls(home)), "one download, no mise call")
            self.assert_nothing_installed_or_recorded(home, dsh_home)

    def test_an_archive_version_producer_that_prints_the_pin_and_exits_nonzero_refuses_the_install(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            # The archive's package.json is read from the new tree (dsh/<tag>.<suffix>); every other jq call answers
            # as jq does.
            version = self.TAG.removeprefix("dsh-v")
            injected = (
                f'case "$*" in *"/dsh/{self.TAG}."*) printf "%s\\n" "{version}"; exit 77 ;; esac; command jq "$@"'
            )
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, jq=injected)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("the version of the archive could not be read; install refused", result.stderr)
            self.assertNotIn("installed into", result.stdout)
            self.assertEqual(1, len(self.calls(home)), "one download, no mise call")
            self.assert_nothing_installed_or_recorded(home, dsh_home)

    def test_a_receipt_producer_that_prints_the_pin_and_exits_nonzero_refuses_the_step_before_any_download(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            _, receipt = self.receipt(home, self.TAG)
            # jq fails on the receipt's row alone (its filter reads the step's source_version), printing the pin as a
            # healthy read would; every other jq call, the object check's and manifest_record's, answers as jq does.
            injected = f'case "$2" in *".source_version // empty") printf "%s\\n" "{self.TAG}"; exit 77 ;; esac; command jq "$@"'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, jq=injected)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "update_deepseek_harness: the installed-manifest receipt could not be read; step refused", result.stderr
            )
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked")
            self.assert_nothing_installed_or_recorded(home, dsh_home, receipt)

    def test_a_zero_byte_receipt_refuses_the_step_before_any_download_and_leaves_the_file_as_it_is(self):
        # The round-3 reproduction: jq answers a zero-byte file with exit 0 and no output, so the step read it as an
        # empty receipt, installed, and manifest_record left the file empty while the step reported an install.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            receipt = home / ".agents/.installed-manifest.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_bytes(b"")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "update_deepseek_harness: the installed-manifest receipt could not be read as a JSON object; step refused",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked")
            self.assertEqual(b"", receipt.read_bytes(), "the file stays zero bytes")
            self.assert_nothing_installed_or_recorded(home, dsh_home, "")

    def test_a_receipt_that_is_a_json_array_refuses_the_step_before_any_download(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            receipt = home / ".agents/.installed-manifest.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_text("[]\n")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("receipt could not be read as a JSON object; step refused", result.stderr)
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked")
            self.assert_nothing_installed_or_recorded(home, dsh_home, "[]\n")

    def test_an_installed_tree_version_producer_that_prints_the_pin_and_exits_nonzero_refuses_the_step(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            self.assertEqual(0, self.run_step(home, payload, digest, dsh_home=dsh_home).returncode)
            install = self.installed_tree(dsh_home)
            receipt = (home / ".agents/.installed-manifest.json").read_text()
            calls = self.calls(home)
            version = self.TAG.removeprefix("dsh-v")
            injected = (
                f'case "$*" in *"{install}/package.json"*) printf "%s\\n" "{version}"; exit 77 ;; esac; command jq "$@"'
            )
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, jq=injected)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"the version of the installed tree {install} could not be read; step refused", result.stderr)
            self.assertEqual(calls, self.calls(home), "no download, no mise call")
            self.assertEqual(install, self.installed_tree(dsh_home), "the install is untouched")
            self.assertEqual(
                receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt is unchanged"
            )

    def test_a_readlink_of_current_that_fails_for_the_installed_state_refuses_the_step_before_any_download(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            prelude = self.failing_call("readlink", 1, 'command readlink "$@"; return 77')
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"the target of {dsh_home}/dsh/current could not be read; step refused", result.stderr)
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assert_previous_install_untouched(dsh_home, install, previous)
            self.assertFalse((dsh_home / "bin").exists(), "no wrapper")
            self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_a_missing_wrapper_is_rewritten_for_the_tree_current_names_without_a_download(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            wrapper = dsh_home / "bin/dsh"
            self.assertEqual(0, self.run_step(home, payload, digest, dsh_home=dsh_home).returncode)
            install = self.installed_tree(dsh_home)
            expected = wrapper.read_text()
            calls = self.calls(home)
            wrapper.unlink()
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"DeepSeek harness {self.TAG} is at {install}; its wrapper is rewritten", result.stdout)
            self.assertTrue(os.access(wrapper, os.X_OK), "the wrapper is back")
            self.assertEqual(expected, wrapper.read_text())
            self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no wrapper temporary")
            self.assertEqual(install, self.installed_tree(dsh_home), "current still names the same tree")
            self.assertEqual(["current", install.name], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertEqual(calls, self.calls(home), "no curl call, no mise call")
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            self.assertEqual(self.TAG, manifest["steps"]["update_deepseek_harness"]["source_version"])
            # With current gone the step has no tree to read its state from, so it installs again: one download, a
            # new tree under its own name, the orphaned tree pruned after the record.
            (dsh_home / "dsh/current").unlink()
            again = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, again.returncode, again.stdout + again.stderr)
            reinstalled = self.installed_tree(dsh_home)
            self.assertNotEqual(install, reinstalled)
            self.assertFalse(install.exists(), "the orphaned tree is pruned")
            self.assertEqual(["current", reinstalled.name], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertEqual(2, len([call for call in self.calls(home) if call.startswith("curl ")]))
            # Converged: the next run finds everything in place and changes nothing.
            calls = self.calls(home)
            converged = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertIn(f"DeepSeek harness {self.TAG} is already installed", converged.stdout)
            self.assertEqual(calls, self.calls(home))

    def test_a_current_link_on_a_tree_of_another_version_is_reinstalled_from_the_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            self.assertEqual(0, self.run_step(home, payload, digest, dsh_home=dsh_home).returncode)
            install = self.installed_tree(dsh_home)
            # The receipt says the pin, but current points at a directory whose package.json says 0.0.0. The directory
            # carries an older tag's name, one of the shapes the prune removes.
            stale = dsh_home / "dsh/dsh-v0.0.0"
            install.rename(stale)
            (stale / "package.json").write_text(json.dumps({"name": "deepseek-harness", "version": "0.0.0"}) + "\n")
            os.unlink(dsh_home / "dsh/current")
            os.symlink(stale, dsh_home / "dsh/current")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(2, len([call for call in self.calls(home) if call.startswith("curl ")]), "a download")
            reinstalled = self.installed_tree(dsh_home)
            self.assertEqual(
                self.TAG.removeprefix("dsh-v"), json.loads((reinstalled / "package.json").read_text())["version"]
            )
            self.assertEqual(
                ["current", reinstalled.name],
                sorted(path.name for path in (dsh_home / "dsh").iterdir()),
                "the stale tree is pruned after the record",
            )

    def test_a_failed_profile_install_leaves_the_previous_tree_current_and_the_wrapper_as_they_were(self):
        # The profile install runs before anything the host runs changes, so its failure needs no rollback: the
        # previous tree stays under its name and on the current link, and no wrapper is written.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            failing = 'case "$*" in "exec -- pnpm install") return 1 ;; esac; return 0'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, mise=failing)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "the profile install failed; nothing recorded; current, the wrapper and the older trees are untouched",
                result.stderr,
            )
            self.assertEqual(self.BUILD_CALLS, [call for call in self.calls(home) if call.startswith("mise ")])
            self.assert_previous_install_untouched(dsh_home, install, previous)
            self.assertFalse((install / "apps").exists(), "nothing of the archive's tree is under the prior tree")
            self.assertFalse((dsh_home / "bin/dsh").exists(), "no wrapper")
            self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")

    def test_a_replaced_previous_tree_leaves_no_previous_directory_after_the_record(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            tree = self.installed_tree(dsh_home)
            self.assertTrue((tree / "apps/cli/lib/bin.js").is_file())
            self.assertNotEqual(previous, (tree / "package.json").read_text(), "current names the archive's tree")
            self.assertFalse(install.exists(), "the prior tree at dsh/<tag> is pruned after the record")
            self.assertEqual(["current", tree.name], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            self.assertEqual(self.TAG, manifest["steps"]["update_deepseek_harness"]["source_version"])

    def test_the_older_trees_under_dsh_go_only_after_the_record_whatever_their_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, _ = self.previous_install(dsh_home)
            older = [
                "dsh-v0.1.0",
                f"{self.TAG}.previous",
                f"{self.TAG}.failed",
                ".staging.abc123",
                f"{self.TAG}.old001",
            ]
            for name in older:
                (dsh_home / "dsh" / name).mkdir()
                (dsh_home / "dsh" / name / "package.json").write_text('{"version": "older"}\n')
            # With a failing record the older trees all stay, current included.
            failed = self.run_step(home, payload, digest, dsh_home=dsh_home, manifest_record="return 1")
            self.assertEqual(1, failed.returncode, failed.stdout + failed.stderr)
            self.assertEqual(
                sorted(["current", self.TAG, *older]), sorted(path.name for path in (dsh_home / "dsh").iterdir())
            )
            self.assertEqual(str(install), os.readlink(dsh_home / "dsh/current"))
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            tree = self.installed_tree(dsh_home)
            self.assertEqual(["current", tree.name], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertEqual([], [line for line in result.stderr.splitlines() if line.startswith("WARN")])
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            self.assertEqual(self.TAG, manifest["steps"]["update_deepseek_harness"]["source_version"])

    def test_a_relative_dsh_home_warns_and_installs_nothing_even_when_it_resolves_to_the_rendered_profile(self):
        # Round 3 (U172d), finding (c): `.dsh` from the scratch HOME passes the pwd -P comparison but would stay
        # relative in the link target, the wrapper and the receipt, so the spelling is refused before the identity.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=Path(".dsh"), cwd=home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "WARN: update_deepseek_harness: DSH_HOME must be an absolute path (.dsh given); nothing installed.",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertEqual(
                ["plugins", "profiles"], sorted(path.name for path in dsh_home.iterdir()), "nothing installed"
            )
            self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_a_dsh_home_the_step_cannot_enter_fails_the_opt_in_read_and_installs_nothing(self):
        # The weight-20 finding of round 2: the `pwd -P` producers decide the opt-in, so their failure is injected. A
        # DSH_HOME without its search bit passes `-d` (its parent is readable) and fails the `cd` inside the read.
        if os.geteuid() == 0:
            self.skipTest("root enters a mode-0 directory")
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            dsh_home.chmod(0)
            try:
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            finally:
                dsh_home.chmod(0o755)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"the physical path of DSH_HOME {dsh_home} could not be read; step refused", result.stderr)
            self.assertNotIn("installed into", result.stdout)
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertEqual(
                ["plugins", "profiles"], sorted(path.name for path in dsh_home.iterdir()), "nothing installed"
            )
            self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_a_current_that_is_a_real_directory_is_refused_before_any_download_or_move(self):
        # Round-2 finding (b): `ln -sfn` onto a directory makes a link inside it and succeeds, so the step recorded an
        # install whose current never reached the pin and whose wrapper had no entrypoint.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            current = dsh_home / "dsh/current"
            current.mkdir(parents=True)
            (current / "keep").write_text("the operator's directory\n")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"update_deepseek_harness: {current} is not a symlink; the step refuses to replace it", result.stderr
            )
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertTrue(current.is_dir() and not current.is_symlink(), "current is still that directory")
            self.assertEqual("the operator's directory\n", (current / "keep").read_text())
            self.assertEqual(["current"], [path.name for path in (dsh_home / "dsh").iterdir()], "no tree")
            self.assertFalse((dsh_home / "bin/dsh").exists(), "no wrapper")
            self.assertFalse((home / ".agents").exists(), "no receipt")

    def test_a_failed_profile_install_after_an_upgrade_leaves_current_on_the_older_tag_s_tree(self):
        # Round-2 finding (a): the rollback put back only a tree displaced from the new pin's own path, so an upgrade
        # from an older tag left current on the new tree. Now nothing the host runs changes before the profile
        # install, so current never leaves the older tag's tree.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            older = dsh_home / "dsh/dsh-v0.1.0"
            older.mkdir(parents=True)
            (older / "package.json").write_text(json.dumps({"name": "deepseek-harness", "version": "0.1.0"}) + "\n")
            os.symlink(older, dsh_home / "dsh/current")
            failing = 'case "$*" in "exec -- pnpm install") return 1 ;; esac; return 0'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, mise=failing)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("the profile install failed; nothing recorded; current, the wrapper", result.stderr)
            self.assertEqual(str(older), os.readlink(dsh_home / "dsh/current"))
            self.assertEqual("0.1.0", json.loads((older / "package.json").read_text())["version"])
            self.assertEqual(
                ["current", "dsh-v0.1.0"],
                sorted(path.name for path in (dsh_home / "dsh").iterdir()),
                "the new tree is gone",
            )
            self.assertFalse((dsh_home / "bin/dsh").exists(), "no wrapper")
            self.assertFalse((home / ".agents").exists(), "no receipt")

    def test_a_failed_record_after_an_upgrade_puts_current_back_on_the_older_tag_s_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            older = dsh_home / "dsh/dsh-v0.1.0"
            older.mkdir(parents=True)
            (older / "package.json").write_text(json.dumps({"name": "deepseek-harness", "version": "0.1.0"}) + "\n")
            os.symlink(older, dsh_home / "dsh/current")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, manifest_record="return 1")
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"the record failed; current is back on {older} and the new tree is removed; nothing recorded",
                result.stderr,
            )
            self.assertEqual(str(older), os.readlink(dsh_home / "dsh/current"))
            self.assertEqual("0.1.0", json.loads((older / "package.json").read_text())["version"])
            self.assertEqual(["current", "dsh-v0.1.0"], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertFalse((home / ".agents").exists(), "no receipt")

    def test_two_failed_records_over_a_prior_install_leave_it_current_and_the_receipt_as_they_were(self):
        # Round-3 defect: a retry after a failed record deleted the last good .previous tree before any record
        # succeeded. The older trees are not touched until the record is written, so a second failing run finds the
        # same prior tree as the first.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            _, receipt = self.receipt(home, "dsh-v0.1.0")
            for attempt in (1, 2):
                with self.subTest(attempt=attempt):
                    result = self.run_step(home, payload, digest, dsh_home=dsh_home, manifest_record="return 1")
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn(
                        f"the record failed; current is back on {install} and the new tree is removed; nothing recorded",
                        result.stderr,
                    )
                    self.assert_previous_install_untouched(dsh_home, install, previous)
                    self.assertEqual(receipt, (home / ".agents/.installed-manifest.json").read_text())
                    self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_wrapper_that_does_not_parse_leaves_the_live_wrapper_byte_identical_and_no_temporary_beside_it(self):
        # Round-3 defect: the wrapper was written straight to its path, so a failed parse left a truncated launcher.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            wrapper, text = self.own_wrapper(dsh_home)
            prelude = 'bash() { case "$1" in -n) return 1 ;; esac; command bash "$@"; }'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"the wrapper parse failed; nothing recorded; the live wrapper at {wrapper}, current and the older"
                " trees are untouched",
                result.stderr,
            )
            self.assertEqual(text, wrapper.read_text(), "the live wrapper is byte-identical")
            self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no .dsh.* left")
            self.assertEqual([], list((dsh_home / "dsh").iterdir()), "the new tree is removed, no current link")
            self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_a_wrapper_mktemp_that_fails_leaves_the_live_wrapper_current_and_the_older_trees_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            wrapper, text = self.own_wrapper(dsh_home)
            # The third mktemp is the wrapper's (after the download directory and the tree): it prints a path of the
            # right shape, makes nothing and exits 77.
            prelude = self.failing_call("mktemp", 3, 'printf "%s\\n" "${@: -1}"; return 77')
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"a wrapper file under {dsh_home}/bin could not be made; nothing recorded", result.stderr)
            self.assertEqual(text, wrapper.read_text(), "the live wrapper is byte-identical")
            self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()])
            self.assert_previous_install_untouched(dsh_home, install, previous)
            self.assertFalse((home / ".agents").exists(), "nothing recorded")
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_download_directory_mktemp_that_fails_refuses_the_step_before_any_download(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            prelude = self.failing_call("mktemp", 1, 'printf "%s\\n" "${@: -1}"; return 77')
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("the download directory could not be made; step refused", result.stderr)
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assert_nothing_installed_or_recorded(home, dsh_home)
            self.assertEqual([], list((home / "tmp").iterdir()))

    def test_a_tree_mktemp_that_fails_refuses_the_install_and_leaves_nothing_under_dsh(self):
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            prelude = self.failing_call("mktemp", 2, 'printf "%s\\n" "${@: -1}"; return 77')
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"the install tree under {dsh_home}/dsh could not be made; install refused", result.stderr)
            self.assertEqual(1, len(self.calls(home)), "one download, no mise call")
            self.assert_nothing_installed_or_recorded(home, dsh_home)
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_readlink_of_current_that_fails_before_publication_refuses_the_install_and_leaves_the_prior_tree(self):
        # The residual of round 3: the readlink before the link had no failure injection. The second readlink is that
        # one (the first read the installed state); it prints the prior target and exits 77.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            prelude = self.failing_call("readlink", 2, 'command readlink "$@"; return 77')
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"the target of {dsh_home}/dsh/current could not be read; install refused", result.stderr)
            self.assertEqual(self.BUILD_CALLS, [call for call in self.calls(home) if call.startswith("mise ")])
            self.assert_previous_install_untouched(dsh_home, install, previous)
            self.assertFalse((home / ".agents").exists(), "nothing recorded")
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_current_link_that_cannot_be_written_removes_the_new_tree_and_records_nothing(self):
        # U178b: the rename over bin/dsh follows the link, so a failed link leaves the live wrapper byte-identical and
        # the trap removes the wrapper temporary with the new tree.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            wrapper, text = self.own_wrapper(dsh_home)
            # The plugin link is an ln call of its own before current's and is not what this test fails.
            prelude = 'ln() { case "${@: -1}" in */dsh/current) return 1 ;; esac; command ln "$@"; }'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "the current link could not be written; nothing recorded; the live wrapper and the older trees are"
                " untouched",
                result.stderr,
            )
            self.assertEqual(text, wrapper.read_text(), "the live wrapper is byte-identical")
            self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no .dsh.* left")
            self.assertEqual([], list((dsh_home / "dsh").iterdir()), "the new tree is removed, no current link")
            self.assertFalse((home / ".agents").exists(), "nothing recorded")
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_the_wrapper_quotes_the_home_so_a_command_substitution_in_its_path_never_runs(self):
        # Round-2 finding (d): the home was interpolated into the wrapper's shell source unescaped. HOME itself holds
        # the sequence here (a directory name holds no slash, so the marker is named from the wrapper's cwd, the
        # scratch directory); a stub mise prints its arguments, so the node path the wrapper hands over is read as text.
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "marker"
            home = Path(directory) / '$(touch "marker")'
            home.mkdir()
            home, dsh_home = self.opted_in_home(str(home))
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            stub_bin = Path(directory) / "stub-bin"
            stub_bin.mkdir()
            (stub_bin / "mise").write_text("#!/bin/bash\nprintf '%s\\n' \"$@\"\n")
            (stub_bin / "mise").chmod(0o755)
            run = subprocess.run(
                [str(dsh_home / "bin/dsh"), "--probe"],
                cwd=directory,
                env=os.environ | {"PATH": f"{stub_bin}:{os.environ['PATH']}"},
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stdout + run.stderr)
            self.assertFalse(marker.exists(), "the command substitution in the home path never ran")
            self.assertEqual(
                ["exec", "--", "node", f"{dsh_home}/dsh/current/apps/cli/lib/bin.js", "--probe"],
                run.stdout.splitlines(),
                "the node path starts with the literal home",
            )

    def test_a_failed_record_leaves_no_download_directory_and_reads_no_unwound_local_in_the_exit_trap(self):
        # Round-2 finding (g): on macOS bash the subshell's locals are unwound before the EXIT trap runs after a failed
        # return, so `${download_dir}` was unbound under set -u and the download directory stayed. manifest_record is
        # replaced by a function that fails, as the finding's injection did. With no prior link, the new tree and the
        # current link go together.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, manifest_record="return 1")
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertNotIn("unbound variable", result.stderr)
            self.assertNotIn("rm:", result.stderr)
            self.assertIn(
                "the record failed; the new tree and the current link are removed; nothing recorded", result.stderr
            )
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")
            self.assertEqual([], list((dsh_home / "dsh").iterdir()), "no tree, no current link")
            self.assertFalse((home / ".agents/.installed-manifest.json").exists(), "nothing recorded")

    def test_a_wrapper_rename_that_fails_after_the_link_puts_current_back_and_keeps_the_live_wrapper(self):
        # Round-1 finding f3 s4 (Codex thread 4475961648): the wrapper was renamed over bin/dsh before current was
        # linked, so a failure between the two left the live launcher changed. The rename now follows the link and its
        # failure is undone like a failed record. mv fails on the wrapper rename alone (its last argument is bin/dsh).
        prelude = 'mv() { case "${@: -1}" in */bin/dsh) return 1 ;; esac; command mv "$@"; }'
        for case in ("over a prior install", "fresh"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                wrapper, text = self.own_wrapper(dsh_home)
                if case == "over a prior install":
                    install, previous = self.previous_install(dsh_home)
                result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                if case == "over a prior install":
                    self.assertIn(
                        f"the wrapper rename failed after the link; current is back on {install} and the new tree is"
                        " removed; the live wrapper is unchanged; nothing recorded",
                        result.stderr,
                    )
                    self.assert_previous_install_untouched(dsh_home, install, previous)
                else:
                    self.assertIn(
                        "the wrapper rename failed after the link; the new tree and the current link are removed; the"
                        " live wrapper is unchanged; nothing recorded",
                        result.stderr,
                    )
                    self.assertEqual([], list((dsh_home / "dsh").iterdir()), "no tree, no current link")
                self.assertEqual(text, wrapper.read_text(), "the live wrapper is byte-identical")
                self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no .dsh.* left")
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_current_link_that_unlinks_current_and_fails_puts_it_back_on_the_prior_tree_or_names_the_absence(self):
        # Round-1 finding f2 s5: ln -sfn unlinks current before it links, so a failure could leave no current and the
        # step returned without a restore. The stub removes its last argument (the link) and fails; the first ln call
        # is the plugin link (U227b) and behaves; in the first case the third call, the restore, behaves, in the
        # second it fails the same way.
        unlink_and_fail = 'command rm -f "${@: -1}"; return 1'
        spare_plugin_link = 'case "${@: -1}" in */node_modules/dsh-omp-gateway.tmp.*) command ln "$@"; return ;; esac'
        for case in ("the restore succeeds", "the restore fails too"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                install, previous = self.previous_install(dsh_home)
                wrapper, text = self.own_wrapper(dsh_home)
                if case == "the restore succeeds":
                    prelude = self.failing_call("ln", 2, unlink_and_fail)
                else:
                    prelude = f"ln() {{ {spare_plugin_link}; {unlink_and_fail}; }}"
                result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                if case == "the restore succeeds":
                    self.assertIn(
                        f"the current link could not be written; current is back on {install} and the new tree is"
                        " removed; nothing recorded",
                        result.stderr,
                    )
                    self.assertEqual("3", (home / "ln-calls").read_text().strip(), "the restore is one ln call")
                    self.assert_previous_install_untouched(dsh_home, install, previous)
                else:
                    self.assertIn(
                        f"the current link could not be written; current is absent; the prior tree {install} is on"
                        " disk under dsh/ and the next make update reinstalls",
                        result.stderr,
                    )
                    self.assertFalse((dsh_home / "dsh/current").is_symlink(), "current is absent")
                    self.assertFalse((dsh_home / "dsh/current").exists())
                    self.assertEqual(previous, (install / "package.json").read_text(), "the prior tree is on disk")
                    self.assertEqual([self.TAG], [path.name for path in (dsh_home / "dsh").iterdir()])
                self.assertEqual(text, wrapper.read_text(), "the live wrapper is byte-identical")
                self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no .dsh.* left")
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_failed_record_whose_restore_fails_keeps_the_new_tree_current_names(self):
        # Round-1 finding f2 s5: when the restore after a failed record failed, the EXIT trap still removed the tree
        # current names, leaving the host a dangling launcher. The third ln call is the restore (the first is the
        # plugin link, U227b).
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            prelude = self.failing_call("ln", 3, "return 1")
            result = self.run_step(
                home, payload, digest, dsh_home=dsh_home, manifest_record="return 1", prelude=prelude
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            tree = self.installed_tree(dsh_home)
            self.assertIn(
                f"the record failed and current could not be put back on {install}; current still names the new tree"
                f" {tree}, which is kept; nothing recorded; the next make update reinstalls",
                result.stderr,
            )
            self.assertTrue((tree / "apps/cli/lib/bin.js").is_file(), "the new tree is whole")
            self.assertEqual(previous, (install / "package.json").read_text(), "the prior tree is as it was")
            self.assertEqual(
                sorted(["current", self.TAG, tree.name]), sorted(path.name for path in (dsh_home / "dsh").iterdir())
            )
            self.assertFalse((home / ".agents").exists(), "nothing recorded")
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_download_directory_that_cannot_be_removed_is_a_warn_and_the_step_still_publishes_and_records(self):
        # Round-1 finding f2 s5: the download directory went after publication and its rm's status ended the subshell
        # under set -e (exit 77, no record, no rollback). It now goes right after the build, before the profile
        # install, and its removal never changes the step's flow.
        with self.subTest(case="rm fails on the download directory"), tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            prelude = 'rm() { case "${@: -1}" in "$TMPDIR"/update-agent-assets.*) return 77 ;; esac; command rm "$@"; }'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            warnings = [line for line in result.stderr.splitlines() if line.startswith("WARN")]
            self.assertEqual(1, len(warnings), result.stderr)
            self.assertIn(
                "the download directory " + str(home / "tmp/update-agent-assets."),
                warnings[0],
            )
            self.assertIn(
                "could not be removed; it holds only the verified archive and the next make update makes a new one",
                warnings[0],
            )
            tree = self.installed_tree(dsh_home)
            self.assertIn(f"DeepSeek harness {self.TAG} installed into {tree}.", result.stdout)
            self.assertTrue(os.access(dsh_home / "bin/dsh", os.X_OK), "the wrapper is live")
            self.assertEqual(self.BUILD_CALLS, [call for call in self.calls(home) if call.startswith("mise ")])
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            self.assertEqual(self.TAG, manifest["steps"]["update_deepseek_harness"]["source_version"])
            self.assertEqual(1, len(list((home / "tmp").iterdir())), "the directory the WARN names is left")
        with (
            self.subTest(case="the directory is gone before the profile install"),
            tempfile.TemporaryDirectory() as directory,
        ):
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            # The mise stub lists the temporary directory at the profile install, the first call after the build.
            listing = 'case "$*" in "exec -- pnpm install") ls -A "$TMPDIR" > "$HOME/listing-at-profile-install" ;; esac; return 0'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, mise=listing)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual("", (home / "listing-at-profile-install").read_text(), "no download directory by then")
            self.assertEqual([], [line for line in result.stderr.splitlines() if line.startswith("WARN")])
            self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            self.assertEqual(self.TAG, manifest["steps"]["update_deepseek_harness"]["source_version"])

    def test_a_bin_dsh_that_is_not_a_regular_file_is_refused_before_any_download(self):
        # Round-1 finding f2 s5: mv -f onto a directory at bin/dsh put the wrapper inside it and the step recorded an
        # install without a launcher; a symlink there would be replaced by the rename. Both shapes are refused as a
        # current that is a real directory is.
        for case in ("a directory", "a symlink to a file"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                launcher = dsh_home / "bin/dsh"
                launcher.parent.mkdir()
                if case == "a directory":
                    launcher.mkdir()
                    (launcher / "keep").write_text("the operator's directory\n")
                else:
                    elsewhere = home / "own-launcher"
                    elsewhere.write_text("#!/bin/bash\necho the operator launcher\n")
                    elsewhere.chmod(0o755)
                    os.symlink(elsewhere, launcher)
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(
                    f"update_deepseek_harness: {launcher} is not a regular file; the step refuses to replace it (move"
                    " it aside and rerun make update); nothing installed, nothing recorded",
                    result.stderr,
                )
                self.assertEqual([], self.calls(home), "no download, no mise call")
                self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked, no current link")
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                self.assertEqual(["dsh"], [path.name for path in launcher.parent.iterdir()], "no .dsh.* left")
                if case == "a directory":
                    self.assertTrue(launcher.is_dir() and not launcher.is_symlink(), "bin/dsh is still that directory")
                    self.assertEqual("the operator's directory\n", (launcher / "keep").read_text())
                else:
                    self.assertTrue(launcher.is_symlink(), "bin/dsh is still the symlink")
                    self.assertEqual(str(elsewhere), os.readlink(launcher))
                    self.assertEqual("#!/bin/bash\necho the operator launcher\n", elsewhere.read_text())

    def test_a_valid_install_whose_bin_directory_is_gone_gets_its_wrapper_back_without_a_download(self):
        # Round-1 finding f2 s4: the repair branch made no bin/ before the wrapper mktemp, so a valid install whose
        # bin/ was removed could never get its wrapper back.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            self.assertEqual(0, self.run_step(home, payload, digest, dsh_home=dsh_home).returncode)
            install = self.installed_tree(dsh_home)
            wrapper = dsh_home / "bin/dsh"
            expected = wrapper.read_text()
            calls = self.calls(home)
            wrapper.unlink()
            wrapper.parent.rmdir()
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"DeepSeek harness {self.TAG} is at {install}; its wrapper is rewritten", result.stdout)
            self.assertTrue(os.access(wrapper, os.X_OK), "the wrapper is back")
            self.assertEqual(expected, wrapper.read_text())
            self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no wrapper temporary")
            self.assertEqual(calls, self.calls(home), "no curl call, no mise call")
            self.assertEqual(install, self.installed_tree(dsh_home), "current still names the same tree")
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            self.assertEqual(self.TAG, manifest["steps"]["update_deepseek_harness"]["source_version"])

    def test_a_receipt_of_two_objects_refuses_the_step_before_any_download_and_leaves_the_file_as_it_is(self):
        # Round-1 finding f2 s4: jq -e judged each document of the file on its own, so two objects passed as one and
        # the step installed over a receipt no JSON reader accepts.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            receipt = home / ".agents/.installed-manifest.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_text("{}\n{}\n")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "update_deepseek_harness: the installed-manifest receipt could not be read as a JSON object; step refused",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no download, no mise call")
            self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked")
            self.assert_nothing_installed_or_recorded(home, dsh_home, "{}\n{}\n")

    def good_tree(self, tree: Path) -> str:
        """A tree carrying the pin's version and its entrypoint at `tree`; the text of its package.json is returned so a
        test can tell it was not touched."""
        (tree / "apps/cli/lib").mkdir(parents=True)
        text = json.dumps({"name": "deepseek-harness", "version": self.TAG.removeprefix("dsh-v")}) + "\n"
        (tree / "package.json").write_text(text)
        (tree / "apps/cli/lib/bin.js").write_text("// hand-placed cli\n")
        return text

    def canonical_install(self, dsh_home: Path) -> tuple[Path, str]:
        """The layout the step makes: a good tree at dsh/<tag>.<suffix> with current an absolute link to it."""
        tree = dsh_home / "dsh" / f"{self.TAG}.abc123"
        text = self.good_tree(tree)
        os.symlink(tree, dsh_home / "dsh/current")
        return tree, text

    def test_a_current_that_does_not_name_a_directory_directly_under_dsh_is_refused_before_any_download(self):
        # Round-2 finding f2 s5: a current that reached its tree indirectly passed the shape checks, and the prune
        # removed the directory the link traverses, leaving current dangling with exit 0. The step now accepts the one
        # layout it makes and refuses every other up front, with the wrapper present (the already-installed path) or
        # absent (the repair); round 2's nested container and a dangling link are refused the same way.
        for shape in ("relay", "dot-dot", "symlinked child", "nested", "dangling"):
            for wrapper_present in (True, False):
                with (
                    self.subTest(shape=shape, wrapper_present=wrapper_present),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    home, dsh_home = self.opted_in_home(directory)
                    payload, digest = self.archive(home)
                    tree = dsh_home / "dsh" / ("nested/tree" if shape == "nested" else f"{self.TAG}.abc123")
                    text = None if shape == "dangling" else self.good_tree(tree)
                    older = dsh_home / "dsh/dsh-v0.1.0"
                    if shape == "relay":
                        older.mkdir()
                        os.symlink(tree, older / "relay")
                        link, target = "dsh-v0.1.0/relay", f"{dsh_home}/dsh/dsh-v0.1.0/relay"
                    elif shape == "dot-dot":
                        older.mkdir()
                        link = target = f"{dsh_home}/dsh/dsh-v0.1.0/../{tree.name}"
                    elif shape == "symlinked child":
                        os.symlink(tree, older)
                        link = target = str(older)
                    elif shape == "nested":
                        link, target = "nested/tree", f"{dsh_home}/dsh/nested/tree"
                    else:
                        (dsh_home / "dsh").mkdir()
                        link = target = f"{dsh_home}/dsh/gone"
                    os.symlink(link, dsh_home / "dsh/current")
                    _, receipt = self.receipt(home, self.TAG)
                    if wrapper_present:
                        wrapper, wrapper_text = self.own_wrapper(dsh_home)
                    else:
                        (dsh_home / "bin").mkdir()
                    before = sorted(os.listdir(dsh_home / "dsh"))
                    result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn(
                        f"update_deepseek_harness: {dsh_home}/dsh/current points at {target}, which is not a directory"
                        f" directly under {dsh_home}/dsh named dsh-v* that the link itself reaches; the step repairs only"
                        " the layout it makes (move the link aside and rerun make update); nothing installed, nothing"
                        " recorded.",
                        result.stderr,
                    )
                    self.assertEqual([], self.calls(home), "no curl call, no mise call")
                    self.assertEqual(link, os.readlink(dsh_home / "dsh/current"), "current as it was")
                    self.assertEqual(before, sorted(os.listdir(dsh_home / "dsh")), "dsh/ as it was")
                    if text is not None:
                        self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")
                        self.assertTrue((tree / "apps/cli/lib/bin.js").is_file())
                    if wrapper_present:
                        self.assertEqual(wrapper_text, wrapper.read_text(), "the wrapper as it was")
                    self.assertEqual(
                        ["dsh"] if wrapper_present else [], [path.name for path in (dsh_home / "bin").iterdir()]
                    )
                    self.assertEqual(
                        receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was"
                    )
                    self.assertEqual([], list((home / "tmp").iterdir()), "no download directory")

    def test_the_prune_after_the_record_removes_only_the_names_the_step_makes(self):
        # Round-1 finding f2 s6: every directory under dsh/ but the one current named went. Only the two shapes the
        # step or its earlier layout made go now; any other name is the operator's and stays.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            for name in ("dsh-v0.1.0", ".staging.abc123", "keep-me"):
                (dsh_home / "dsh" / name).mkdir(parents=True)
                (dsh_home / "dsh" / name / "notes").write_text(f"{name}\n")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            tree = self.installed_tree(dsh_home)
            self.assertEqual(
                sorted(["current", "keep-me", tree.name]), sorted(path.name for path in (dsh_home / "dsh").iterdir())
            )
            self.assertEqual("keep-me\n", (dsh_home / "dsh/keep-me/notes").read_text(), "keep-me is as it was")
            self.assertEqual([], [line for line in result.stderr.splitlines() if line.startswith("WARN")])
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            self.assertEqual(self.TAG, manifest["steps"]["update_deepseek_harness"]["source_version"])

    def test_a_prune_that_fails_once_warns_and_the_next_already_installed_run_prunes(self):
        # Round-1 finding f2 s2: after a prune failure the next run returned through the already-installed path
        # before any prune, so the WARN's promised retry never came. rm fails on the prior tree alone.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install, previous = self.previous_install(dsh_home)
            prelude = f'rm() {{ case "${{@: -1}}" in */dsh/{self.TAG}) return 1 ;; esac; command rm "$@"; }}'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            tree = self.installed_tree(dsh_home)
            warnings = [line for line in result.stderr.splitlines() if line.startswith("WARN")]
            retry = f"the older tree {install} could not be removed; the next make update prunes again."
            self.assertEqual([f"WARN: update_deepseek_harness: {retry}"], warnings)
            self.assertEqual(
                sorted(["current", self.TAG, tree.name]), sorted(path.name for path in (dsh_home / "dsh").iterdir())
            )
            self.assertEqual(previous, (install / "package.json").read_text(), "the prior tree is as it was")
            manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
            self.assertEqual(self.TAG, manifest["steps"]["update_deepseek_harness"]["source_version"])
            calls = self.calls(home)
            again = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, again.returncode, again.stdout + again.stderr)
            self.assertIn(f"DeepSeek harness {self.TAG} is already installed", again.stdout)
            self.assertEqual([], [line for line in again.stderr.splitlines() if line.startswith("WARN")])
            self.assertEqual(calls, self.calls(home), "no download, no mise call")
            self.assertEqual(["current", tree.name], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertEqual(tree, self.installed_tree(dsh_home), "current still names the same tree")

    def test_a_valid_u172_layout_at_the_pin_is_already_installed_and_untouched_but_for_the_receipt_s_paths(self):
        # What U172 left on an opted-in host: the receipt at the pin naming dsh/<tag>, the tree at dsh/<tag> itself with
        # the pin's version and its entrypoint, current on it, an executable wrapper. The already-installed path leaves
        # every path as it is and rewrites the receipt's paths to this layout's two (dsh/current, bin/dsh), so no
        # recorded path can be pruned later; the layout changes only at a reinstall or an upgrade.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            install = dsh_home / "dsh" / self.TAG
            package = self.good_tree(install)
            (install / "apps/cli/lib/bin.js").write_text("// the U172 cli\n")
            os.symlink(install, dsh_home / "dsh/current")
            wrapper, text = self.own_wrapper(dsh_home)
            self.receipt(home, self.TAG, paths=[str(install), f"{dsh_home}/bin/dsh"])
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"DeepSeek harness {self.TAG} is already installed", result.stdout)
            self.assertEqual([], [line for line in result.stderr.splitlines() if line.startswith("WARN")])
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            self.assertEqual(str(install), os.readlink(dsh_home / "dsh/current"), "current as it was")
            self.assertEqual(package, (install / "package.json").read_text(), "the tree as it was")
            self.assertEqual("// the U172 cli\n", (install / "apps/cli/lib/bin.js").read_text())
            self.assertEqual(["current", self.TAG], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertEqual(text, wrapper.read_text(), "the wrapper as it was")
            self.assertTrue(os.access(wrapper, os.X_OK))
            self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()])
            step = json.loads((home / ".agents/.installed-manifest.json").read_text())["steps"][
                "update_deepseek_harness"
            ]
            self.assertEqual(self.TAG, step["source_version"])
            self.assertEqual(
                [f"{dsh_home}/dsh/current", f"{dsh_home}/bin/dsh"], step["paths"], "the paths are this layout's"
            )
            self.assertEqual([], list((home / "tmp").iterdir()), "no download directory")

    def test_a_receipt_naming_the_earlier_layout_is_rewritten_before_the_older_tree_it_names_is_pruned(self):
        # Round-2 finding f2 s6: after a failed record whose restore failed, the next run took the already-installed
        # exit and pruned the tree the receipt still named (the U172 form, dsh/<tag>), so the doctor read a missing
        # path for good. The exit now rewrites a receipt whose paths are not this layout's two before any prune, and
        # records nothing when they are.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            tree, text = self.canonical_install(dsh_home)
            older = dsh_home / "dsh" / self.TAG
            older.mkdir()
            (older / "package.json").write_text(json.dumps({"name": "deepseek-harness", "version": "previous"}) + "\n")
            self.own_wrapper(dsh_home)
            self.receipt(home, self.TAG, paths=[str(older), f"{dsh_home}/bin/dsh"])
            # The record stub lists dsh/ at record time and then writes the real record.
            record = 'ls -A "$DSH_HOME/dsh" > "$HOME/listing-at-record"; _manifest_record "$@"'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, manifest_record=record)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"DeepSeek harness {self.TAG} is already installed", result.stdout)
            self.assertEqual([], [line for line in result.stderr.splitlines() if line.startswith("WARN")])
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            step = json.loads((home / ".agents/.installed-manifest.json").read_text())["steps"][
                "update_deepseek_harness"
            ]
            self.assertEqual(self.TAG, step["source_version"])
            self.assertEqual([f"{dsh_home}/dsh/current", f"{dsh_home}/bin/dsh"], step["paths"])
            self.assertEqual(
                sorted(["current", self.TAG, tree.name]),
                sorted((home / "listing-at-record").read_text().split()),
                "the older tree is still on disk when the record is written",
            )
            self.assertEqual(["current", tree.name], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertEqual(str(tree), os.readlink(dsh_home / "dsh/current"), "current as it was")
            self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")
            # Converged: a record that would fail proves the next run writes none.
            again = self.run_step(home, payload, digest, dsh_home=dsh_home, manifest_record="return 1")
            self.assertEqual(0, again.returncode, again.stdout + again.stderr)
            self.assertIn(f"DeepSeek harness {self.TAG} is already installed", again.stdout)
            self.assertEqual([], self.calls(home), "no curl call, no mise call")

    def test_a_receipt_rewrite_that_fails_on_the_already_installed_exit_keeps_the_older_tree_and_the_receipt(self):
        for case in ("the record fails", "the recorded paths cannot be read"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                tree, text = self.canonical_install(dsh_home)
                older = dsh_home / "dsh" / self.TAG
                older.mkdir()
                previous = json.dumps({"name": "deepseek-harness", "version": "previous"}) + "\n"
                (older / "package.json").write_text(previous)
                self.own_wrapper(dsh_home)
                _, receipt = self.receipt(home, self.TAG, paths=[str(older), f"{dsh_home}/bin/dsh"])
                if case == "the record fails":
                    result = self.run_step(home, payload, digest, dsh_home=dsh_home, manifest_record="return 1")
                    expected = "the record could not be rewritten; the older trees are kept"
                else:
                    # The fourth jq call reads the paths, after the receipt's shape, its row and the tree's version.
                    prelude = self.failing_call("jq", 4, 'command jq "$@"; return 77')
                    result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=prelude)
                    expected = "the recorded paths could not be read from the installed-manifest receipt; step refused"
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"update_deepseek_harness: {expected}", result.stderr)
                self.assertEqual([], self.calls(home), "no curl call, no mise call")
                self.assertEqual(
                    sorted(["current", self.TAG, tree.name]), sorted(path.name for path in (dsh_home / "dsh").iterdir())
                )
                self.assertEqual(previous, (older / "package.json").read_text(), "the older tree is as it was")
                self.assertEqual(str(tree), os.readlink(dsh_home / "dsh/current"), "current as it was")
                self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")
                self.assertEqual(
                    receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was"
                )

    def test_a_cleanup_that_fails_in_the_exit_trap_leaves_the_step_s_status_as_it_was(self):
        # Round-2 finding f2 s4: set -e is in force inside the EXIT trap, so a download directory the trap could not
        # remove after a failed download turned the WARN's exit 0 into the rm's 77.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            prelude = 'rm() { case "${@: -1}" in "$TMPDIR"/update-agent-assets.*) return 77 ;; esac; command rm "$@"; }'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, curl="return 22", prelude=prelude)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            warnings = [line for line in result.stderr.splitlines() if line.startswith("WARN")]
            self.assertEqual(1, len(warnings), result.stderr)
            self.assertIn("could not be downloaded", warnings[0])
            self.assertIn("nothing installed, nothing recorded", warnings[0])
            self.assertEqual(1, len(list((home / "tmp").iterdir())), "the directory the trap could not remove is left")
            self.assertFalse((home / ".agents").exists(), "nothing recorded")
            self.assertEqual(["plugins", "profiles"], sorted(path.name for path in dsh_home.iterdir()))

    def test_a_current_link_that_cannot_be_removed_after_a_failed_record_or_rename_keeps_the_new_tree_it_names(self):
        # Round-2 finding f2 s3: the rollback's bare rm -f of current ended the subshell under set -e with the rm's
        # status before the step said what it left, and the trap then removed the tree current named.
        rm = 'rm() { case "${@: -1}" in */dsh/current) return 77 ;; esac; command rm "$@"; }'
        mv = 'mv() { case "${@: -1}" in */bin/dsh) return 1 ;; esac; command mv "$@"; }'
        for case in ("the record fails", "the wrapper rename fails"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                wrapper, text = self.own_wrapper(dsh_home)
                if case == "the record fails":
                    result = self.run_step(
                        home, payload, digest, dsh_home=dsh_home, manifest_record="return 1", prelude=rm
                    )
                    failed = "the record failed and current could not be removed and still names the new tree"
                else:
                    result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=f"{rm}\n{mv}")
                    failed = "the wrapper rename failed after the link and current could not be removed and still names the new tree"
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                tree = self.installed_tree(dsh_home)
                self.assertIn(f"{failed} {tree}, which is kept;", result.stderr)
                self.assertIn("nothing recorded; the next make update reinstalls", result.stderr)
                self.assertTrue((tree / "apps/cli/lib/bin.js").is_file(), "the new tree is whole")
                self.assertEqual(["current", tree.name], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
                if case == "the wrapper rename fails":
                    self.assertEqual(text, wrapper.read_text(), "the live wrapper is byte-identical")
                self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no .dsh.* left")
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_restore_that_unlinks_current_and_fails_names_the_absence_and_keeps_both_trees(self):
        # Round-2 finding f2 s3: a restoring ln -sfn unlinks current before it links, so a restore that failed could
        # leave no current while the line said current still named the new tree. The line now reads the link, and the
        # new tree is kept either way. The third ln call is the restore, after a failed record or a failed rename
        # (the first is the plugin link, U227b).
        unlink_and_fail = 'command rm -f "${@: -1}"; return 1'
        mv = 'mv() { case "${@: -1}" in */bin/dsh) return 1 ;; esac; command mv "$@"; }'
        for case in ("the record fails", "the wrapper rename fails"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                install, previous = self.previous_install(dsh_home)
                wrapper, text = self.own_wrapper(dsh_home)
                prelude = self.failing_call("ln", 3, unlink_and_fail)
                if case == "the record fails":
                    result = self.run_step(
                        home, payload, digest, dsh_home=dsh_home, manifest_record="return 1", prelude=prelude
                    )
                    failed = "the record failed and current could not be put back on"
                else:
                    result = self.run_step(home, payload, digest, dsh_home=dsh_home, prelude=f"{prelude}\n{mv}")
                    failed = "the wrapper rename failed after the link and current could not be put back on"
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                names = sorted(path.name for path in (dsh_home / "dsh").iterdir())
                new = [name for name in names if name.startswith(f"{self.TAG}.")]
                self.assertEqual(1, len(new), names)
                tree = dsh_home / "dsh" / new[0]
                self.assertIn(
                    f"{failed} {install}; current is absent; the prior tree {install} and the new tree {tree} are on disk"
                    " under dsh/;",
                    result.stderr,
                )
                self.assertIn("nothing recorded; the next make update reinstalls", result.stderr)
                self.assertFalse((dsh_home / "dsh/current").is_symlink(), "current is absent")
                self.assertFalse((dsh_home / "dsh/current").exists())
                self.assertEqual([self.TAG, tree.name], names, "both trees are on disk")
                self.assertEqual(previous, (install / "package.json").read_text(), "the prior tree is as it was")
                self.assertTrue((tree / "apps/cli/lib/bin.js").is_file(), "the new tree is whole")
                if case == "the wrapper rename fails":
                    self.assertEqual(text, wrapper.read_text(), "the live wrapper is byte-identical")
                self.assertEqual(["dsh"], [path.name for path in (dsh_home / "bin").iterdir()], "no .dsh.* left")
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                self.assertEqual([], list((home / "tmp").iterdir()), "the download directory is removed")

    def test_a_bin_that_is_a_symlink_into_an_older_tree_is_refused_before_any_download(self):
        # Round-3 verdict f2 s6 (the auditor's fixture): bin/ a symlink into an older tree passed every check, the
        # already-installed exit pruned that tree, and the launcher went with it. bin/ is a row of the input table now,
        # absent or a directory that is not a symlink, read by type before anything else.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            tree, text = self.canonical_install(dsh_home)
            older = dsh_home / "dsh/dsh-v0.1.0"
            (older / "bin").mkdir(parents=True)
            launcher_text = "#!/bin/bash\necho 'the launcher inside the older tree'\n"
            (older / "bin/dsh").write_text(launcher_text)
            (older / "bin/dsh").chmod(0o755)
            os.symlink(older / "bin", dsh_home / "bin")
            _, receipt = self.receipt(home, self.TAG)
            before = sorted(os.listdir(dsh_home / "dsh"))
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"update_deepseek_harness: {dsh_home}/bin is a symlink or not a directory; the step uses only a directory"
                " of its own there (move it aside and rerun make update); nothing installed, nothing recorded.",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            self.assertTrue((dsh_home / "bin").is_symlink(), "bin/ is still the symlink")
            self.assertEqual(str(older / "bin"), os.readlink(dsh_home / "bin"))
            self.assertEqual(launcher_text, (older / "bin/dsh").read_text(), "the launcher as it was")
            self.assertEqual(before, sorted(os.listdir(dsh_home / "dsh")), "every tree as it was")
            self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")
            self.assertEqual(str(tree), os.readlink(dsh_home / "dsh/current"), "current as it was")
            self.assertEqual(receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was")
            self.assertEqual([], list((home / "tmp").iterdir()), "no download directory")

    def test_a_dsh_or_bin_that_is_a_regular_file_is_refused_before_any_download(self):
        # The other refused state of the dsh/ and bin/ rows: a file there is no place for mkdir -p to make the tree or
        # the wrapper directory, and the step says so instead of failing inside the install.
        for row in ("dsh", "bin"):
            with self.subTest(row=row), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                (dsh_home / row).write_text("the operator's file\n")
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(
                    f"update_deepseek_harness: {dsh_home}/{row} is a symlink or not a directory; the step uses only a"
                    " directory of its own there (move it aside and rerun make update); nothing installed, nothing"
                    " recorded.",
                    result.stderr,
                )
                self.assertEqual([], self.calls(home), "no curl call, no mise call")
                self.assertEqual("the operator's file\n", (dsh_home / row).read_text(), "the file as it was")
                self.assertEqual(sorted(["plugins", "profiles", row]), sorted(path.name for path in dsh_home.iterdir()))
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                self.assertEqual([], list((home / "tmp").iterdir()), "no download directory")

    def test_a_dsh_directory_that_is_a_symlink_is_refused_before_any_download(self):
        # The dsh/ row: a symlink there would have the tree made and the prune run behind a path the operator linked.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            elsewhere = home / "elsewhere"
            elsewhere.mkdir()
            (elsewhere / "keep").write_text("the operator's file\n")
            os.symlink(elsewhere, dsh_home / "dsh")
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"update_deepseek_harness: {dsh_home}/dsh is a symlink or not a directory; the step uses only a directory"
                " of its own there (move it aside and rerun make update); nothing installed, nothing recorded.",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            self.assertTrue((dsh_home / "dsh").is_symlink(), "dsh/ is still the symlink")
            self.assertEqual(["keep"], [path.name for path in elsewhere.iterdir()], "nothing made behind the link")
            self.assertFalse((dsh_home / "bin").exists(), "no wrapper")
            self.assertFalse((home / ".agents").exists(), "nothing recorded")
            self.assertEqual([], list((home / "tmp").iterdir()), "no download directory")

    def test_a_profile_directory_that_is_a_symlink_or_a_file_is_refused_and_an_absent_one_warns(self):
        # The profiles/thak row: the kit renders that directory, so a symlink or a file there is not the kit's and is
        # refused; an absent one is the host the kit has not rendered on, the WARN with exit 0 of the elsewhere case.
        for case in ("a symlink", "a file", "absent"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                profile = dsh_home / "profiles/thak"
                shutil.rmtree(profile)
                if case == "a symlink":
                    elsewhere = home / "own-profile"
                    elsewhere.mkdir()
                    (elsewhere / "package.json").write_text('{"name": "own"}\n')
                    os.symlink(elsewhere, profile)
                elif case == "a file":
                    profile.write_text("not a directory\n")
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                if case == "absent":
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    warnings = [line for line in result.stderr.splitlines() if line.startswith("WARN")]
                    self.assertEqual(1, len(warnings), result.stderr)
                    self.assertIn(
                        f"{profile} is absent, so the kit has not rendered the thak profile here; nothing installed",
                        warnings[0],
                    )
                else:
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn(
                        f"update_deepseek_harness: {profile} is a symlink or not a directory; the step installs the"
                        " profile plugins only into the directory the kit renders (move it aside and rerun make update);"
                        " nothing installed, nothing recorded.",
                        result.stderr,
                    )
                self.assertEqual([], self.calls(home), "no curl call, no mise call")
                self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked, no current link")
                self.assertFalse((dsh_home / "bin").exists(), "no wrapper")
                self.assertFalse((home / ".agents").exists(), "nothing recorded")
                if case == "a symlink":
                    self.assertTrue(profile.is_symlink(), "the profile path is still the symlink")
                    self.assertEqual(["package.json"], [path.name for path in elsewhere.iterdir()])
                elif case == "a file":
                    self.assertEqual("not a directory\n", profile.read_text(), "the file as it was")
                else:
                    self.assertFalse(profile.exists())

    def test_a_current_whose_target_name_ends_in_a_newline_is_refused_before_any_download(self):
        # Round-3 verdict f2 s5 (the auditor's fixture): $(readlink) strips a trailing newline, so a current on the
        # directory `dsh-v0.1.0` plus a newline was checked as the good dsh-v0.1.0 beside it and reported already
        # installed while current ran the other tree. The link and the leaf the text read names are now compared by
        # inode (-ef), which no text read can mangle.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            good = dsh_home / "dsh/dsh-v0.1.0"
            good_text = self.good_tree(good)
            other = dsh_home / "dsh" / "dsh-v0.1.0\n"
            (other / "apps/cli/lib").mkdir(parents=True)
            other_text = json.dumps({"name": "deepseek-harness", "version": "other"}) + "\n"
            (other / "package.json").write_text(other_text)
            (other / "apps/cli/lib/bin.js").write_text("// the other cli\n")
            os.symlink("dsh-v0.1.0\n", dsh_home / "dsh/current")
            wrapper, wrapper_text = self.own_wrapper(dsh_home)
            _, receipt = self.receipt(home, self.TAG)
            before = sorted(os.listdir(dsh_home / "dsh"))
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertNotIn("is already installed", result.stdout)
            self.assertIn(
                f"update_deepseek_harness: {dsh_home}/dsh/current points at {good}, which is not a directory directly"
                f" under {dsh_home}/dsh named dsh-v* that the link itself reaches; the step repairs only the layout it"
                " makes (move the link aside and rerun make update); nothing installed, nothing recorded.",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            self.assertEqual("dsh-v0.1.0\n", os.readlink(dsh_home / "dsh/current"), "current as it was")
            self.assertEqual(before, sorted(os.listdir(dsh_home / "dsh")), "both trees as they were")
            self.assertEqual(good_text, (good / "package.json").read_text())
            self.assertEqual(other_text, (other / "package.json").read_text())
            self.assertEqual(wrapper_text, wrapper.read_text(), "the wrapper as it was")
            self.assertEqual(receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was")
            self.assertEqual([], list((home / "tmp").iterdir()), "no download directory")

    def test_a_current_on_a_directory_of_another_name_under_dsh_is_refused_before_any_download(self):
        # The current row names dsh-v* as the one accepted leaf: a real directory of another name under dsh/ (the
        # operator's keep-me, which the prune leaves) is not the step's tree even when it carries the pin's files.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            keep = dsh_home / "dsh/keep-me"
            text = self.good_tree(keep)
            os.symlink(keep, dsh_home / "dsh/current")
            wrapper, wrapper_text = self.own_wrapper(dsh_home)
            _, receipt = self.receipt(home, self.TAG)
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"update_deepseek_harness: {dsh_home}/dsh/current points at {keep}, which is not a directory directly"
                f" under {dsh_home}/dsh named dsh-v* that the link itself reaches; the step repairs only the layout it"
                " makes (move the link aside and rerun make update); nothing installed, nothing recorded.",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            self.assertEqual(str(keep), os.readlink(dsh_home / "dsh/current"), "current as it was")
            self.assertEqual(["current", "keep-me"], sorted(path.name for path in (dsh_home / "dsh").iterdir()))
            self.assertEqual(text, (keep / "package.json").read_text(), "keep-me as it was")
            self.assertEqual(wrapper_text, wrapper.read_text(), "the wrapper as it was")
            self.assertEqual(receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was")

    def test_a_receipt_that_is_a_directory_a_fifo_or_a_dangling_symlink_is_refused_before_any_download(self):
        # Round-3 verdict f2 s5: `-f` alone let a directory, a FIFO or a dangling symlink at the receipt path pass as
        # the fresh host, and the install reached manifest_record over it. The row is read by type first, and the
        # step never opens the path, so the FIFO never blocks it.
        for case in ("a directory", "a FIFO", "a dangling symlink"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                receipt = home / ".agents/.installed-manifest.json"
                receipt.parent.mkdir(parents=True)
                if case == "a directory":
                    receipt.mkdir()
                    (receipt / "keep").write_text("the operator's file\n")
                    shape = "is not a regular file"
                elif case == "a FIFO":
                    os.mkfifo(receipt)
                    shape = "is not a regular file"
                else:
                    os.symlink(home / "gone", receipt)
                    shape = "is a symlink"
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(
                    f"update_deepseek_harness: the installed-manifest receipt {receipt} {shape}; the step reads and"
                    " writes only a regular file there (move it aside and rerun make update); nothing installed, nothing"
                    " recorded.",
                    result.stderr,
                )
                self.assertEqual([], self.calls(home), "no curl call, no mise call")
                self.assertFalse((dsh_home / "dsh").exists(), "nothing unpacked, no current link")
                self.assertFalse((dsh_home / "bin").exists(), "no wrapper")
                self.assertEqual(
                    [".installed-manifest.json"], [path.name for path in receipt.parent.iterdir()], "no temporary"
                )
                if case == "a directory":
                    self.assertTrue(receipt.is_dir() and not receipt.is_symlink(), "the receipt path is that directory")
                    self.assertEqual("the operator's file\n", (receipt / "keep").read_text())
                elif case == "a FIFO":
                    self.assertTrue(receipt.is_fifo(), "the receipt path is still the FIFO")
                else:
                    self.assertTrue(receipt.is_symlink() and not receipt.exists(), "the receipt path is still dangling")
                    self.assertEqual(str(home / "gone"), os.readlink(receipt))
                self.assertEqual([], list((home / "tmp").iterdir()), "no download directory")

    def test_a_receipt_symlinked_into_an_older_tree_is_refused_before_any_download(self):
        # Round-3 verdict f2 s6: a receipt that was a symlink into an older tree dangled once the already-installed exit
        # pruned that tree. A symlink at the receipt path is refused as such, so nothing is pruned and the link stays.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            tree, text = self.canonical_install(dsh_home)
            older = dsh_home / "dsh/dsh-v0.1.0"
            older.mkdir()
            _, receipt_text = self.receipt(home, self.TAG)
            receipt = home / ".agents/.installed-manifest.json"
            receipt.rename(older / "receipt.json")
            os.symlink(older / "receipt.json", receipt)
            wrapper, wrapper_text = self.own_wrapper(dsh_home)
            before = sorted(os.listdir(dsh_home / "dsh"))
            result = self.run_step(home, payload, digest, dsh_home=dsh_home)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"update_deepseek_harness: the installed-manifest receipt {receipt} is a symlink; the step reads and"
                " writes only a regular file there (move it aside and rerun make update); nothing installed, nothing"
                " recorded.",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            self.assertEqual(before, sorted(os.listdir(dsh_home / "dsh")), "the older tree is not pruned")
            self.assertTrue(receipt.is_symlink() and receipt.exists(), "the receipt link is as it was")
            self.assertEqual(str(older / "receipt.json"), os.readlink(receipt))
            self.assertEqual(receipt_text, (older / "receipt.json").read_text(), "the file behind it as it was")
            self.assertEqual(str(tree), os.readlink(dsh_home / "dsh/current"), "current as it was")
            self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")
            self.assertEqual(wrapper_text, wrapper.read_text(), "the wrapper as it was")

    def test_a_receipt_whose_paths_equal_the_two_only_as_joined_text_is_rewritten_on_the_already_installed_exit(self):
        # Round-3 verdict f2 s4: the recorded paths were compared as a newline-joined string, so a third empty entry or
        # the two paths inside one entry read as equal and the promised rewrite was skipped. jq compares the array.
        for case in ("an extra empty entry", "the two joined by a newline"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, dsh_home = self.opted_in_home(directory)
                payload, digest = self.archive(home)
                tree, text = self.canonical_install(dsh_home)
                self.own_wrapper(dsh_home)
                current, launcher = f"{dsh_home}/dsh/current", f"{dsh_home}/bin/dsh"
                paths = [current, launcher, ""] if case == "an extra empty entry" else [f"{current}\n{launcher}"]
                self.receipt(home, self.TAG, paths=paths)
                result = self.run_step(home, payload, digest, dsh_home=dsh_home)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"DeepSeek harness {self.TAG} is already installed", result.stdout)
                self.assertEqual([], self.calls(home), "no curl call, no mise call")
                step = json.loads((home / ".agents/.installed-manifest.json").read_text())["steps"][
                    "update_deepseek_harness"
                ]
                self.assertEqual([current, launcher], step["paths"], "the paths are rewritten to this layout's two")
                self.assertEqual(self.TAG, step["source_version"])
                self.assertEqual(str(tree), os.readlink(dsh_home / "dsh/current"), "current as it was")
                self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")

    def test_a_jq_that_fails_on_the_paths_comparison_refuses_the_step_and_prunes_nothing(self):
        # The comparison's status is read three ways: 0 equal, 1 not equal (the rewrite), any other a failed read. A jq
        # that exits 5 on that read alone (the receipt's shape, its row and the tree's version answer as jq does)
        # refuses the step before the prune, so the older tree and the receipt stay as they were.
        with tempfile.TemporaryDirectory() as directory:
            home, dsh_home = self.opted_in_home(directory)
            payload, digest = self.archive(home)
            tree, text = self.canonical_install(dsh_home)
            older = dsh_home / "dsh" / self.TAG
            older.mkdir()
            previous = json.dumps({"name": "deepseek-harness", "version": "previous"}) + "\n"
            (older / "package.json").write_text(previous)
            self.own_wrapper(dsh_home)
            _, receipt = self.receipt(home, self.TAG)
            # The function runs in the step's own subshell, not a command substitution, so it returns rather than exits.
            injected = 'case "$*" in *\'.paths == [$c, $w]\'*) return 5 ;; esac; command jq "$@"'
            result = self.run_step(home, payload, digest, dsh_home=dsh_home, jq=injected)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "update_deepseek_harness: the recorded paths could not be read from the installed-manifest receipt;"
                " step refused",
                result.stderr,
            )
            self.assertEqual([], self.calls(home), "no curl call, no mise call")
            self.assertEqual(
                sorted(["current", self.TAG, tree.name]), sorted(path.name for path in (dsh_home / "dsh").iterdir())
            )
            self.assertEqual(previous, (older / "package.json").read_text(), "the older tree is as it was")
            self.assertEqual(str(tree), os.readlink(dsh_home / "dsh/current"), "current as it was")
            self.assertEqual(text, (tree / "package.json").read_text(), "the tree as it was")
            self.assertEqual(receipt, (home / ".agents/.installed-manifest.json").read_text(), "the receipt as it was")


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
            'converge_claude_step "crit@crit" || true; fail_on_pin_failures'
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
        step = 'converge_claude_step "crit@crit" || true; fail_on_pin_failures'
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
                gate = f'{body}; converge_or_disable claude crit@crit step; printf "rc=%s failures=%s\\n" "$?" "${{PIN_FAILURES}}"'
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
                f'source "$1"; has_command() {{ return 0; }}; {fake}\nupdate_codex_superpowers; fail_on_pin_failures',
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
        'converge_claude_plugins; printf "failures=%s\\n" "${PIN_FAILURES}"; '
        "fail_on_pin_failures"
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
                step = "converge_claude_step crit@crit || true; fail_on_pin_failures"
                result, calls, _ = self.converge_listed(step, installs, enabled, LIST_FAILS="sandbox unavailable")
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("not installed or updated from an unverified marketplace", result.stderr)
                if name == "installed at its pin":
                    self.assertEqual(["plugin disable crit@crit --scope user @neutral"], calls)

    def test_a_fresh_install_that_lands_off_its_pin_is_disabled_and_warned_not_failed(self):
        # CI public-bootstrap (macos-15): pstack's marketplace had moved to 0.15.32 past the 0.15.30 pin, and
        # Claude Code installs only the current release.
        pin = self.pin_of("pstack@cursor-plugins")
        step = 'converge_claude_step pstack@cursor-plugins || true; printf "failures=%s\\n" "${PIN_FAILURES}"; fail_on_pin_failures'
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
        self.assertIn("is off its pin and is proven disabled (Claude) or removed (Codex)", result.stderr)
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
            'printf "failures=%s\\n" "${PIN_FAILURES}"; fail_on_pin_failures'
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
                        'printf "failures=%s\\n" "${PIN_FAILURES}"; fail_on_pin_failures',
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
                        f"superpowers@openai-curated landed at 99.0.0 and make doctor rejects that copy: version or "
                        f"content off the pin {pin}",
                        result.stderr,
                    )
                    self.assertIn(
                        "is off its pin and is proven disabled (Claude) or removed (Codex)",
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
                    'printf "failures=%s\\n" "${PIN_FAILURES}"; '
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
            'printf "failures=%s\\n" "${PIN_FAILURES}"'
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
                f'source "$1"; has_command() {{ return 0; }}; {fake}\nupdate_codex_ponytail; fail_on_pin_failures',
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

    def repo_pinned_to_the_fixture(self, work: Path) -> Path:
        """A scratch dotfiles source root (what DOTFILES_SOURCE_DIR names) holding scripts/ and the Codex modify
        script, whose plugin-pins.json records the fixture's content_sha256 for ponytail@ponytail: the copies the
        fake codex writes from tests/fixtures/ponytail are then at their pin, as a reviewed upstream copy is against
        the recorded one. Every other pin and the updater itself are the repository's."""
        repo = work / "repo"
        shutil.copytree(ROOT / "scripts", repo / "scripts")
        (repo / "home/dot_codex").mkdir(parents=True)
        shutil.copy(ROOT / "home/dot_codex/modify_private_config.toml", repo / "home/dot_codex")
        (repo / "vendor/compactiondb").mkdir(parents=True)
        pins_path = repo / "scripts/plugin-pins.json"
        pins = json.loads(pins_path.read_text())
        pins["codex"]["ponytail@ponytail"]["content_sha256"] = reviewed_content_sha256(PONYTAIL)
        pins_path.write_text(json.dumps(pins))
        return repo

    def run_ponytail_bootstrap(
        self,
        before: str | None,
        cache_version: str = "99.0.0",
        manifest_version=None,
        from_another_commit: bool = False,
        remove_fails: bool = False,
        hook_change: str | None = None,
    ):
        # update_codex_ponytail with [marketplaces.ponytail] at its pinned ref, against a fake codex whose
        # `marketplace upgrade` installs the enabled plugin's copy at CACHE_VERSION (what Codex does for a
        # plugin the managed config enables) and the marketplace clone at the ref, and whose `plugin remove`
        # empties the cache. Every copy is the fixture tree (tests/fixtures/ponytail, install_ponytail_copy) and the
        # scratch source root's pins record its content_sha256 (repo_pinned_to_the_fixture), so a copy at the pinned
        # version is at its pin. BEFORE is the version of the copy
        # cached before the step, None for a fresh bootstrap; MANIFEST_VERSION, when given, is what that copy's
        # plugin.json declares instead. FROM_ANOTHER_COMMIT gives the copy (the cached one and the upgrade's) the
        # `.git` of a clone at a commit other than the pinned ref (the copy Codex writes from upstream main);
        # HOOK_CHANGE names a hook file both copies hold changed; REMOVE_FAILS makes `plugin remove` fail and leave
        # the copy.
        pins = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["codex"]["ponytail@ponytail"]
        work = Path(tempfile.mkdtemp(prefix="ponytail-bootstrap-"))
        self.addCleanup(shutil.rmtree, work)
        repo = self.repo_pinned_to_the_fixture(work)
        (work / "home/.codex").mkdir(parents=True)
        (work / "home/.codex/config.toml").write_text(
            f'[marketplaces.ponytail]\nref = "{pins["ref"]}"\nsource_type = "git"\nsource = "{pins["marketplace"]}"\n'
        )
        cache = work / "home/.codex/plugins/cache/ponytail/ponytail"
        change = {hook_change: (PONYTAIL / hook_change).read_bytes() + b"changed\n"} if hook_change else None
        if before is not None:
            declared = before if manifest_version is None else manifest_version
            install_ponytail_copy(cache / before, None if declared == pins["pin"] else declared, change)
        copy_git = ""
        if from_another_commit:
            clone = git_init(work / "clone", "-b", "main")
            git = ["git", "-C", str(clone), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"]
            subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "x"], check=True)
            copy_git = str(clone / ".git")
            if before is not None:
                shutil.copytree(copy_git, cache / before / ".git")
        record = work / "home/.codex/.tmp/marketplaces/ponytail/.codex-marketplace-install.json"
        record_text = json.dumps({"source_type": "git", "source": pins["marketplace"], "revision": pins["ref"]})
        fake = (
            'codex() { printf "%s\\n" "$*" >> "${WORK}/calls"; case "$1 $2 $3" in '
            '"plugin marketplace upgrade") for dir in "${CACHE}/${CACHE_VERSION}" "${RECORD%/*}"; do '
            'mkdir -p "${dir}"; cp -R "${FIXTURE}/." "${dir}/"; done; '
            '[ "${CACHE_VERSION}" = "${PIN}" ] || printf \'{"name": "ponytail", "version": "%s"}\' "${CACHE_VERSION}" '
            '> "${CACHE}/${CACHE_VERSION}/.codex-plugin/plugin.json"; '
            '[ -z "${HOOK_CHANGE}" ] || printf "changed\\n" >> "${CACHE}/${CACHE_VERSION}/${HOOK_CHANGE}"; '
            'printf "%s" "${RECORD_TEXT}" > "${RECORD}"; '
            '[ -z "${COPY_GIT}" ] || cp -R "${COPY_GIT}" "${CACHE}/${CACHE_VERSION}/.git" ;; '
            '"plugin remove "*) if [ -n "${REMOVE_FAILS}" ]; then echo "codex: cannot remove" >&2; return 1; fi; '
            'rm -rf "${CACHE}" ;; esac; }'
        )
        result = subprocess.run(
            [
                "bash",
                "-c",
                f'source "$1"; has_command() {{ return 0; }}; {fake}\nupdate_codex_ponytail; '
                'printf "failures=%s\\n" "${PIN_FAILURES}"; fail_on_pin_failures',
                "bash",
                str(repo / "scripts/update-agent-assets.sh"),
            ],
            env=os.environ
            | scratch_env(work / "home")
            | {
                "DOTFILES_SOURCE_DIR": str(repo),
                "WORK": str(work),
                "CACHE": str(cache),
                "CACHE_VERSION": cache_version,
                "PIN": pins["pin"],
                "FIXTURE": str(PONYTAIL),
                "HOOK_CHANGE": hook_change or "",
                "RECORD": str(record),
                "RECORD_TEXT": record_text,
                "COPY_GIT": copy_git,
                "REMOVE_FAILS": "1" if remove_fails else "",
            },
            text=True,
            capture_output=True,
            check=False,
        )
        calls = (work / "calls").read_text().splitlines() if (work / "calls").exists() else []
        return result, calls, cache, pins["pin"]

    def test_a_fresh_ponytail_copy_the_marketplace_upgrade_installs_off_its_pin_is_judged_not_failed(self):
        # Incident 2026-10-29: the marketplace ref pins the catalog snapshot only, and the catalog names upstream
        # main as the plugin source, so on a fresh bootstrap the upgrade itself installed v5.3.3 against the 5.3.2
        # pin. The copy was then read as "already installed", never judged, and the bootstrap failed.
        result, calls, cache, pin = self.run_ponytail_bootstrap(before=None)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertEqual(["plugin marketplace upgrade ponytail", "plugin remove ponytail@ponytail"], calls)
        self.assertFalse(cache.exists())
        self.assertIn("Codex Ponytail plugin was installed by the marketplace upgrade.", result.stdout)
        self.assertNotIn("already installed", result.stdout)
        self.assertIn(
            f"ponytail@ponytail landed at 99.0.0 and make doctor rejects that copy: version or content off the "
            f"pin {pin}",
            result.stderr,
        )
        self.assertIn("is off its pin and is proven disabled (Claude) or removed (Codex)", result.stderr)
        # A fresh copy that lands at the pin is simply installed and stays.
        result, calls, cache, pin = self.run_ponytail_bootstrap(before=None, cache_version=pin)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("plugin marketplace upgrade ponytail", calls[0], calls)
        self.assertFalse([call for call in calls if call.startswith(("plugin remove", "plugin add"))], calls)
        self.assertTrue((cache / pin).is_dir())
        self.assertIn("codex plugin ponytail@ponytail is at its pin (make doctor agrees).", result.stdout)

    def test_a_ponytail_copy_cached_before_the_upgrade_and_off_its_pin_is_removed_and_warned_not_failed(self):
        # U118 round 2: `codex plugin marketplace upgrade` rewrites the copy from upstream main whether one was cached
        # or not, so a copy that was there before is no more reviewed than a fresh one. Both take one outcome: judged
        # by make doctor after the upgrade (version and content), removed when rejected, a WARN, the doctor's
        # drift until the review bump, not a counted run failure. Round 1 left an existing copy to the doctor alone
        # and counted it, which is what turned the host's `make update` red.
        pin = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["codex"]["ponytail@ponytail"]["pin"]
        named = "files that differ from the marketplace clone at the pinned ref: hooks/ponytail-activate.js"
        for name, before, cache_version, hook_change, finding in (
            ("cached at another version", "98.0.0", "99.0.0", None, "installed at 99.0.0, not its pin"),
            ("cached at the pin, a hook file changed", pin, pin, "hooks/ponytail-activate.js", named),
            ("fresh at the pin, a hook file changed", None, pin, "hooks/ponytail-activate.js", named),
        ):
            with self.subTest(case=name):
                result, calls, cache, _ = self.run_ponytail_bootstrap(
                    before=before, cache_version=cache_version, hook_change=hook_change
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("failures=0", result.stdout)
                self.assertIn(
                    "Codex Ponytail plugin is already installed." if before else "was installed by the marketplace",
                    result.stdout,
                )
                self.assertEqual(["plugin marketplace upgrade ponytail", "plugin remove ponytail@ponytail"], calls)
                self.assertFalse(cache.exists())
                self.assertIn(finding, result.stderr)  # make doctor's finding names what is off the pin
                self.assertIn(f"make doctor rejects that copy: version or content off the pin {pin}", result.stderr)
                self.assertIn("is off its pin and is proven disabled (Claude) or removed (Codex)", result.stderr)
                self.assertNotIn("did not reach its pin", result.stderr)
                self.assertNotIn("could not be checked or kept at their pin", result.stderr)

    def test_a_ponytail_cache_that_cannot_be_read_before_the_upgrade_stops_it_and_names_the_path(self):
        # Failure injection (standing order 21): a plugin.json without a version fails the reader. That is never
        # "absent": no upgrade runs (it would install a copy nothing judges), the step fails naming the cache path.
        result, calls, cache, _ = self.run_ponytail_bootstrap(before="5.3.2", manifest_version="")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("failures=1", result.stdout)
        self.assertFalse([call for call in calls if call.startswith("plugin marketplace upgrade")], calls)
        self.assertIn(
            f"cannot read the cached copy of ponytail@ponytail under {cache} before upgrading its marketplace",
            result.stderr,
        )
        self.assertNotIn("already installed", result.stdout)
        self.assertFalse(cache.exists())  # converge_or_disable removes what it could not verify

    def test_a_fresh_ponytail_copy_at_its_pinned_version_from_another_commit_is_accepted(self):
        # Incident 2026-10-30: the marketplace ref pins the catalog snapshot only, and the upgrade installs the copy
        # from upstream main, so after any upstream push every host's copy comes from a commit other than the
        # ref while its manifest still declares the pinned version. That copy is at its pin: judged by version,
        # as the Claude copy of the same plugin is; the commit is not compared (what a hook may run is decided
        # by the trusted_hash pins). Round 2 of 2026-10-29 had the doctor reject such a copy, and U117 then
        # removed it on every fresh bootstrap.
        pin = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["codex"]["ponytail@ponytail"]["pin"]
        result, calls, cache, _ = self.run_ponytail_bootstrap(before=None, cache_version=pin, from_another_commit=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertEqual("plugin marketplace upgrade ponytail", calls[0], calls)
        self.assertFalse([call for call in calls if call.startswith(("plugin remove", "plugin add"))], calls)
        self.assertTrue((cache / pin / ".git").exists())
        self.assertIn("codex plugin ponytail@ponytail is at its pin (make doctor agrees).", result.stdout)
        self.assertNotIn("not the pinned ref", result.stderr)
        self.assertNotIn("make doctor rejects", result.stderr)
        # A copy cached before the upgrade from another commit, at the pinned version, is at its pin too.
        result, calls, cache, _ = self.run_ponytail_bootstrap(before=pin, cache_version=pin, from_another_commit=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("failures=0", result.stdout)
        self.assertEqual("plugin marketplace upgrade ponytail", calls[0], calls)
        self.assertFalse([call for call in calls if call.startswith(("plugin remove", "plugin add"))], calls)
        self.assertIn("Codex Ponytail plugin is already installed.", result.stdout)
        self.assertTrue((cache / pin).is_dir())

    def run_hook_trust_refresh(self, chezmoi_env: dict[str, str]) -> tuple[subprocess.CompletedProcess, list[str]]:
        # refresh_codex_hook_trust against a fake chezmoi on PATH that logs every call and lists two managed Codex
        # config files; CHEZMOI_ENV is what the caller's environment says about a chezmoi run (chezmoi exports
        # CHEZMOI=1 to every script it runs).
        work = Path(tempfile.mkdtemp(prefix="hook-trust-"))
        self.addCleanup(shutil.rmtree, work)
        (work / "bin").mkdir()
        calls = work / "calls"
        fake = work / "bin/chezmoi"
        fake.write_text(
            "#!/bin/sh\n"
            f'printf "%s\\n" "$*" >> {str(calls)!r}\n'
            'if [ "$1" = managed ]; then printf "/h/.codex/config.toml\\n/h/.codex/standard.config.toml\\n/h/.zshrc\\n"; fi\n'
            "exit 0\n"
        )
        fake.chmod(0o755)
        env = {key: value for key, value in os.environ.items() if key != "CHEZMOI"}
        env["PATH"] = f"{work / 'bin'}{os.pathsep}{env['PATH']}"
        result = subprocess.run(
            ["bash", "-c", 'source "$1" && refresh_codex_hook_trust', "bash", str(UPDATER)],
            env=env | chezmoi_env,
            text=True,
            capture_output=True,
            check=False,
        )
        return result, calls.read_text().splitlines() if calls.exists() else []

    def test_the_hook_trust_refresh_is_left_to_the_standalone_run_inside_chezmoi_apply(self):
        # Incident 2026-10-30: run_once_after_06-install-agent-assets.sh runs this script inside chezmoi apply,
        # where the outer apply holds the persistent state lock, so the nested apply always timed out on it and
        # warned (since #284). make update runs the script standalone right after the apply, where the refresh
        # works, so inside a chezmoi run the step says so in one line and does nothing.
        result, calls = self.run_hook_trust_refresh({"CHEZMOI": "1"})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], calls)
        self.assertEqual(1, len(result.stdout.splitlines()), result.stdout)
        self.assertIn("standalone ./scripts/update-agent-assets.sh run of make update refreshes it", result.stdout)
        self.assertEqual("", result.stderr)
        # Standalone (no CHEZMOI, or another value), the managed Codex config files are re-applied as before.
        for name, chezmoi_env in (("unset", {}), ("other value", {"CHEZMOI": "0"})):
            with self.subTest(case=name):
                result, calls = self.run_hook_trust_refresh(chezmoi_env)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(
                    [
                        "managed --path-style=absolute --include=files",
                        "apply --force /h/.codex/config.toml /h/.codex/standard.config.toml",
                    ],
                    calls,
                )
                self.assertNotIn("not refreshed", result.stdout + result.stderr)

    def test_a_fresh_ponytail_copy_whose_removal_fails_fails_the_run(self):
        # Failure injection for the PLUGIN_FRESH_OFF_PIN path of converge_or_disable: `codex plugin remove` fails
        # and the off-pin copy stays, so nothing proves it inactive. That is an error, counted, and the run fails;
        # the WARN that reports nothing unreviewed active is never printed.
        result, calls, cache, _ = self.run_ponytail_bootstrap(before=None, remove_fails=True)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("failures=1", result.stdout)
        self.assertIn("plugin remove ponytail@ponytail", calls)
        self.assertTrue((cache / "99.0.0").is_dir())
        self.assertIn("codex plugin remove left a copy (copy 99.0.0)", result.stderr)
        self.assertIn("codex plugin ponytail@ponytail landed off its pin and cannot be proven disabled", result.stderr)
        self.assertNotIn("so nothing unreviewed is active", result.stderr)

    def test_the_codex_judge_follows_make_doctor_and_never_passes_a_check_that_cannot_run(self):
        # The judge is a table over make doctor's pin check: 0 at the pin, 1 rejected (PLUGIN_FRESH_OFF_PIN), any
        # other status a check that could not run, which fails the step and never passes (standing order 21).
        pin = json.loads((ROOT / "scripts/plugin-pins.json").read_text())["codex"]["ponytail@ponytail"]["pin"]
        for doctor_exit, expected, message in (
            ("0", "rc=0", None),
            ("1", "rc=11", f"ponytail@ponytail landed at {pin} and make doctor rejects that copy: version or content"),
            ("2", "rc=1", "make doctor's pin check of codex plugin ponytail@ponytail could not run (exit 2)"),
            ("127", "rc=1", "make doctor's pin check of codex plugin ponytail@ponytail could not run (exit 127)"),
        ):
            with self.subTest(doctor_exit=doctor_exit):
                work = Path(tempfile.mkdtemp(prefix="codex-judge-"))
                self.addCleanup(shutil.rmtree, work)
                copy = work / "home/.codex/plugins/cache/ponytail/ponytail" / pin / ".codex-plugin"
                copy.mkdir(parents=True)
                (copy / "plugin.json").write_text(json.dumps({"name": "ponytail", "version": pin}))
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        'source "$1"; doctor_pin_check() { return "${DOCTOR_EXIT}"; }; set +e; '
                        'judge_codex_copy ponytail@ponytail; echo "rc=$?"',
                        "bash",
                        str(UPDATER),
                    ],
                    env=os.environ | scratch_env(work / "home") | {"DOCTOR_EXIT": doctor_exit},
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual([expected], result.stdout.splitlines(), result.stderr)
                if message is None:
                    self.assertEqual("", result.stderr)
                else:
                    self.assertIn(message, result.stderr)

    def test_the_ponytail_trusted_hashes_cover_upstreams_hooks_file(self):
        # Trust boundary: the trusted_hash pins under codex.hooks.state trust Ponytail's three hook commands only as
        # reviewed. tests/fixtures/ponytail/hooks/claude-codex-hooks.json is upstream's hooks file at the pinned ref
        # verbatim (the rest of the fixture is synthetic), so a mistyped trusted_hash, or a hooks file that is not the
        # one the pins were recorded from, fails here, and any other hook command is untrusted. The content_sha256
        # pin's provenance is a scratch clone of upstream at the pinned ref (the PR body's Verification), no fixture.
        all_pins = json.loads((ROOT / "scripts/plugin-pins.json").read_text())
        pins = all_pins["codex"]["ponytail@ponytail"]
        self.assertEqual(pins["pin"], all_pins["claude"]["ponytail@ponytail"]["pin"])
        self.assertEqual(pins["pin"], json.loads((PONYTAIL / ".codex-plugin/plugin.json").read_text())["version"])
        hook_bytes = (PONYTAIL / "hooks/claude-codex-hooks.json").read_bytes()
        home = Path(tempfile.mkdtemp(prefix="ponytail-hooks-"))
        self.addCleanup(shutil.rmtree, home)
        installed = home / ".codex/plugins/cache/ponytail/ponytail" / pins["pin"] / "hooks/claude-codex-hooks.json"
        installed.parent.mkdir(parents=True)
        installed.write_bytes(hook_bytes)
        script = ROOT / "home/dot_codex/modify_private_config.toml"
        block = script.read_text().split("# >>> codex hook trust", 1)[1].split("# <<< codex hook trust", 1)[0]
        namespace = {"sys": sys, "Path": Path}
        exec(block.split("\n", 1)[1], namespace)

        def ponytail_trust():
            return {
                key: (kind, digest, entry.get("trusted_hash"))
                for key, entry, digest, kind, _ in namespace["declared_hook_trust"](str(home))
                if key.startswith("ponytail@ponytail:")
            }

        trust = ponytail_trust()
        self.assertEqual(3, len(trust), trust)
        for key, (kind, digest, pin) in trust.items():
            with self.subTest(key=key):
                self.assertEqual("trusted", kind)
                self.assertEqual(pin, digest)
        installed.write_bytes(hook_bytes.replace(b'"timeout": 15', b'"timeout": 16'))
        self.assertEqual({"changed"}, {kind for kind, _, _ in ponytail_trust().values()})

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
        step = 'converge_claude_step "crit@crit" || true; printf "failures=%s\\n" "${PIN_FAILURES}"'
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
                gate = f"ensure_crit_cli() {{ :; }}; ensure_claude_crit_marketplace() {{ :; }}; {step}; fail_on_pin_failures"
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
        step = 'converge_claude_plugins; printf "failures=%s\\n" "${PIN_FAILURES}"'
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
        ):
            with self.subTest(step=step):
                installs = {plugin_id: [{"scope": "user", "version": "999.0.0"}]}
                gate = (
                    "ensure_crit_cli() { return 1; }; "
                    f'{step}; printf "reached failures=%s\\n" "${{PIN_FAILURES}}"; fail_on_pin_failures'
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
        ):
            with self.subTest(step=step):
                installs = {plugin_id: [{"scope": "user", "version": pins[plugin_id]["pin"]}]}
                gate = (
                    'printf x > "${HOME}/.agents"; ensure_crit_cli() { :; }; '
                    f'{step}; printf "reached failures=%s\\n" "${{PIN_FAILURES}}"; fail_on_pin_failures'
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
                    'printf "reached failures=%s\\n" "${PIN_FAILURES}"; fail_on_pin_failures'
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


class RetireUnderstandAnythingTest(unittest.TestCase):
    """retire_understand_anything against a fake claude that logs its arguments and working directory: every read
    before the first change, a host whose marketplace list does not work warned and left unchanged, user scope only on
    every command, the marketplace's source checked before an uninstall, and a stale enabled entry disabled (U224c,
    U224d, U224e)."""

    PLUGIN = "understand-anything@understand-anything"
    LIST = "plugin marketplace list --json"
    REGISTERED = [{"name": "understand-anything", "source": "github", "repo": "Egonex-AI/Understand-Anything"}]
    FAKE_CLAUDE = r"""
claude() {
    printf '%s\n' "$*" >> "${CALLS}"
    printf '%s\n' "${PWD}" >> "${CWDS}"
    case "$*" in
    "plugin marketplace list --json")
        [ -z "${LIST_FAILS:-}" ] || return 1
        cat "${MARKETS}"
        ;;
    "plugin uninstall "*) [ -z "${UNINSTALL_FAILS:-}" ] || return 1 ;;
    "plugin marketplace remove understand-anything --scope user --json")
        # The refusals Claude Code 2.1.316 prints as its --json result line.
        if [ -n "${NOT_DECLARED:-}" ]; then
            printf '%s\n' '{"command":"marketplace-remove","marketplace":"understand-anything","outcome":"failed","message":"Marketplace '"'"'understand-anything'"'"' is not declared in user settings. Omit --scope to remove it from all scopes.","failureCode":"not_configured"}'
            return 1
        fi
        if [ -n "${REMOVE_FAILS:-}" ]; then
            printf '%s\n' '{"command":"marketplace-remove","marketplace":"understand-anything","outcome":"failed","message":"write failed"}'
            return 1
        fi
        ;;
    "plugin marketplace remove "*)
        # Without --scope the declaration goes from every scope and the project records with it (Claude Code 2.1.316).
        printf '{"version": 2, "plugins": {}}\n' > "${HOME}/.claude/plugins/installed_plugins.json"
        ;;
    "plugin disable "*) [ -z "${DISABLE_FAILS:-}" ] || return 1 ;;
    esac
}
"""

    def run_step(self, installs, markets, *, has_claude=True, enabled=None, extra=None, settings=None, **env):
        """INSTALLS: [{scope, projectPath?}] for the plugin, or raw text for installed_plugins.json; MARKETS: the
        listing, or raw text; ENABLED: the plugin's user enabledPlugins value; EXTRA: more installed_plugins.json
        entries by id; SETTINGS: raw text for settings.json."""
        work = Path(tempfile.mkdtemp(prefix="retire-ua-"))
        self.addCleanup(shutil.rmtree, work)
        home = work / "home"
        (home / ".claude/plugins").mkdir(parents=True)
        (work / "tmp").mkdir()
        (work / "project").mkdir()
        record = home / ".claude/plugins/installed_plugins.json"
        if isinstance(installs, str):
            record.write_text(installs)
        else:
            entries = [
                {
                    "version": "2.9.7",
                    "installPath": f"{home}/.claude/plugins/cache/understand-anything/understand-anything/2.9.7",
                    **({"projectPath": str(work / "project")} if entry["scope"] != "user" else {}),
                    **entry,
                }
                for entry in installs
            ]
            extra = {
                key: [{**entry, "installPath": entry["installPath"].format(home=home)} for entry in value]
                for key, value in (extra or {}).items()
            }
            plugins = ({self.PLUGIN: entries} if entries else {}) | extra
            record.write_text(json.dumps({"version": 2, "plugins": plugins}))
        if settings is not None:
            (home / ".claude/settings.json").write_text(settings)
        elif enabled is not None:
            (home / ".claude/settings.json").write_text(json.dumps({"enabledPlugins": {self.PLUGIN: enabled}}))
        (work / "markets.json").write_text(markets if isinstance(markets, str) else json.dumps(markets))
        stubs = (
            self.FAKE_CLAUDE
            if has_claude
            else 'has_command() { [ "$1" != claude ] && command -v "$1" > /dev/null 2>&1; }\n'
        )
        result = subprocess.run(
            ["bash", "-c", f'source "$1"; {stubs}\nretire_understand_anything', "bash", str(UPDATER)],
            env=os.environ
            | scratch_env(home)
            | {
                "CALLS": str(work / "calls"),
                "CWDS": str(work / "cwds"),
                "MARKETS": str(work / "markets.json"),
                "TMPDIR": str(work / "tmp"),
            }
            | env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        calls = (work / "calls").read_text().splitlines() if (work / "calls").exists() else []
        cwds = (work / "cwds").read_text().splitlines() if (work / "cwds").exists() else []
        return result, calls, cwds, work

    def assert_list_warning(self, result, calls):
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual([self.LIST], calls)
        self.assertIn(f"WARN: claude plugin {self.PLUGIN} was not retired", result.stderr)
        self.assertIn('Run make update once "claude plugin marketplace list" works.', result.stderr)
        self.assertNotIn("ERROR", result.stderr)
        self.assertEqual("", result.stdout)

    def test_retire_understand_anything_warns_and_changes_nothing_when_the_list_fails(self):
        result, calls, _, _ = self.run_step([{"scope": "user"}], self.REGISTERED, enabled=True, LIST_FAILS="1")
        self.assert_list_warning(result, calls)

    def test_retire_understand_anything_warns_and_changes_nothing_on_a_list_that_is_not_json(self):
        result, calls, _, _ = self.run_step(
            [{"scope": "user"}], "mise ERROR claude is not a valid shim\n", enabled=True
        )
        self.assert_list_warning(result, calls)

    def test_retire_understand_anything_warns_on_a_list_entry_without_a_name(self):
        result, calls, _, _ = self.run_step([{"scope": "user"}], [{"source": "github"}], enabled=True)
        self.assert_list_warning(result, calls)

    def test_retire_understand_anything_uninstalls_then_removes_the_marketplace(self):
        result, calls, cwds, work = self.run_step([{"scope": "user"}], self.REGISTERED)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            [
                self.LIST,
                f"plugin uninstall {self.PLUGIN} --scope user",
                "plugin marketplace remove understand-anything --scope user --json",
            ],
            calls,
        )
        self.assertIn(f"Ran: claude plugin uninstall {self.PLUGIN} --scope user", result.stdout)
        self.assertIn("Ran: claude plugin marketplace remove understand-anything --scope user", result.stdout)
        self.assertNotIn("already retired", result.stdout + result.stderr)
        # Every command runs from a scratch directory, never a project's.
        self.assertTrue(all(Path(cwd).resolve().parent == (work / "tmp").resolve() for cwd in cwds), cwds)

    def test_retire_understand_anything_stops_when_the_marketplace_remove_fails(self):
        result, calls, _, _ = self.run_step([{"scope": "user"}], self.REGISTERED, REMOVE_FAILS="1")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            [
                self.LIST,
                f"plugin uninstall {self.PLUGIN} --scope user",
                "plugin marketplace remove understand-anything --scope user --json",
            ],
            calls,
        )
        self.assertIn(
            "ERROR: claude plugin marketplace remove understand-anything --scope user failed (exit 1).", result.stderr
        )

    def test_retire_understand_anything_stops_when_the_uninstall_fails(self):
        result, calls, _, _ = self.run_step([{"scope": "user"}], self.REGISTERED, UNINSTALL_FAILS="1")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"claude plugin uninstall {self.PLUGIN} --scope user failed", result.stderr)
        self.assertEqual([self.LIST, f"plugin uninstall {self.PLUGIN} --scope user"], calls)

    def test_retire_understand_anything_leaves_a_project_scope_installation_to_the_operator(self):
        result, calls, cwds, work = self.run_step([{"scope": "project"}], [])
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([self.LIST], calls)
        self.assertIn(f"WARN: {self.PLUGIN} has a project-scope installation in {work / 'project'}", result.stderr)
        self.assertNotIn(str((work / "project").resolve()), [str(Path(cwd).resolve()) for cwd in cwds])
        self.assertNotIn("already retired", result.stderr)

    def test_retire_understand_anything_removes_the_marketplace_at_user_scope_beside_a_project_installation(self):
        # Reaches the remove branch with a project record present: an unscoped remove would drop that record.
        result, calls, _, work = self.run_step([{"scope": "project"}], self.REGISTERED)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([self.LIST, "plugin marketplace remove understand-anything --scope user --json"], calls)
        record = json.loads((work / "home/.claude/plugins/installed_plugins.json").read_text())
        self.assertEqual(["project"], [entry["scope"] for entry in record["plugins"][self.PLUGIN]])
        self.assertIn(f"WARN: {self.PLUGIN} has a project-scope installation in {work / 'project'}", result.stderr)

    def test_retire_understand_anything_leaves_a_marketplace_declared_outside_the_user_settings(self):
        result, calls, _, _ = self.run_step([], self.REGISTERED, NOT_DECLARED="1")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual([self.LIST, "plugin marketplace remove understand-anything --scope user --json"], calls)
        self.assertIn(
            "WARN: the Claude Code marketplace understand-anything is not declared in the user settings", result.stderr
        )
        self.assertNotIn("ERROR", result.stderr)
        self.assertEqual("", result.stdout)

    def test_retire_understand_anything_names_the_user_scope_on_every_plugin_command(self):
        text = UPDATER.read_text()
        body = text[text.index("function retire_understand_anything() {") :]
        body = body[: body.index("\n}\n")]
        commands = [line.strip() for line in body.splitlines() if "claude_outside_projects plugin" in line]
        self.assertEqual(4, len(commands), commands)
        # `marketplace list` is the one read and takes no --scope (Claude Code 2.1.316); every command that changes
        # state names the user scope.
        unscoped = [line for line in commands if "--scope user" not in line]
        self.assertEqual(1, len(unscoped), unscoped)
        self.assertIn("claude_outside_projects plugin marketplace list --json", unscoped[0])
        # No claude plugin call bypasses claude_outside_projects (message text and comments aside).
        code = [line.strip() for line in body.splitlines() if not line.strip().startswith(("#", "printf"))]
        self.assertEqual([], [line for line in code if re.search(r"(^|[\s(;])claude\s+plugin", line)])

    def test_retire_understand_anything_leaves_a_plugin_whose_marketplace_is_another_source(self):
        # The understand-anything marketplace comes from other/..., and a same-name plugin of the other marketplace
        # is installed too: neither is touched, and the source is named before any uninstall could run.
        foreign = [
            {"name": "understand-anything", "source": "github", "repo": "other/Understand-Anything"},
            {"name": "other", "source": "github", "repo": "other/plugins"},
        ]
        other = {
            "understand-anything@other": [
                {
                    "scope": "user",
                    "version": "1.0.0",
                    "installPath": "{home}/.claude/plugins/cache/other/understand-anything/1.0.0",
                }
            ]
        }
        result, calls, _, _ = self.run_step([{"scope": "user"}], foreign, extra=other)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([self.LIST], calls)
        self.assertIn(
            f"WARN: the user-scope {self.PLUGIN} comes from the marketplace understand-anything", result.stderr
        )
        self.assertIn("registered from another source than Egonex-AI/Understand-Anything", result.stderr)
        self.assertEqual("", result.stdout)

    def test_retire_understand_anything_leaves_a_user_installation_whose_marketplace_is_not_registered(self):
        result, calls, _, _ = self.run_step([{"scope": "user"}], [], enabled=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([self.LIST], calls)
        self.assertIn("which is not registered, so its source cannot be verified; left in place.", result.stderr)

    def test_retire_understand_anything_leaves_a_foreign_marketplace_of_that_name(self):
        foreign = [{"name": "understand-anything", "source": "github", "repo": "someone/else"}]
        result, calls, _, _ = self.run_step([], foreign, enabled=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([self.LIST], calls)
        self.assertIn("registered from another source", result.stderr)

    def test_retire_understand_anything_disables_a_stale_enabled_entry(self):
        result, calls, _, _ = self.run_step([], [], enabled=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([self.LIST, f"plugin disable {self.PLUGIN} --scope user"], calls)
        self.assertIn(f"Ran: claude plugin disable {self.PLUGIN} --scope user", result.stdout)
        self.assertNotIn("already retired", result.stderr)

    def test_retire_understand_anything_stops_when_the_disable_fails(self):
        result, calls, _, _ = self.run_step([], [], enabled=True, DISABLE_FAILS="1")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"ERROR: claude plugin disable {self.PLUGIN} --scope user failed.", result.stderr)

    def test_retire_understand_anything_changes_nothing_when_nothing_is_present(self):
        for enabled in (None, False):
            with self.subTest(enabled=enabled):
                result, calls, _, _ = self.run_step([], [], enabled=enabled)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual([self.LIST], calls)
                self.assertIn("Understand-Anything: already retired.", result.stderr)
                self.assertEqual("", result.stdout)

    def test_retire_understand_anything_refuses_an_unreadable_installation_record(self):
        result, calls, _, work = self.run_step("{not json", self.REGISTERED)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"cannot read {work}/home/.claude/plugins/installed_plugins.json", result.stderr)
        self.assertEqual([self.LIST], calls)

    def test_retire_understand_anything_refuses_unreadable_user_settings(self):
        result, calls, _, work = self.run_step([], [], settings="{not json")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"cannot read {work}/home/.claude/settings.json", result.stderr)
        self.assertEqual([self.LIST], calls)

    def test_retire_understand_anything_skips_a_host_without_claude(self):
        result, calls, _, _ = self.run_step([{"scope": "user"}], self.REGISTERED, has_claude=False)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Skipping the Understand-Anything retirement: claude command not found.", result.stderr)
        self.assertEqual([], calls)


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


class SingleStepModeTest(unittest.TestCase):
    """The updater run with one step's name (make doctor's checks, the coordinator's deploy of one pin) carries the
    full run's contract (U283, from verdicts/U276b): the run ends with fail_on_pin_failures, so a step whose rsync or
    manifest record failed exits non-zero instead of reporting success; a destination that is a link, or whose parent
    resolves outside the asset root, is refused before rsync runs; a misuse prints the usage naming every step and runs
    nothing. The updater runs as a program here, the way make doctor and the coordinator call it."""

    STEPS = (
        "update_omp",
        "update_hcom",
        "update_pi_claude_bridge",
        "update_security_audit_skill",
        "update_deepseek_harness",
        "update_compactiondb",
        "prune_retired_manifest_steps",
        "check_pi_claude_bridge",
        "check_pstack",
        "retire_shared_pstack_copies",
        "retire_marketplace_dev_workflows",
        "retire_agmsg_shim",
    )
    # The real rsync by its absolute path: main prepends the mise shims to PATH, so a stub that strips one PATH entry
    # would call itself again.
    REAL_RSYNC = f'exec "{shutil.which("rsync")}" "$@"'

    def fixture(self, directory: str, rsync: str = "exit 0") -> tuple[Path, Path, Path]:
        """A scratch HOME with ~/.agents, a source root whose vendored CompactionDB holds one CHANGELOG entry and one
        file and whose scripts/ is the repository's, and a bin/ whose rsync logs its arguments and runs RSYNC's body
        (REAL_RSYNC hands the call to the real one)."""
        root = Path(directory)
        home, source, bin_dir = root / "home", root / "source", root / "bin"
        (home / ".agents").mkdir(parents=True)
        (source / "vendor/compactiondb").mkdir(parents=True)
        (source / "vendor/compactiondb/CHANGELOG.md").write_text("## 1.2.3\n\n- fixture entry\n")
        (source / "vendor/compactiondb/README.md").write_text("fixture payload\n")
        (source / "scripts").symlink_to(ROOT / "scripts")
        bin_dir.mkdir()
        (bin_dir / "rsync").write_text(f'#!/bin/bash\nprintf "rsync %s\\n" "$*" >> "$CALLS"\n{rsync}\n')
        (bin_dir / "rsync").chmod(0o755)
        return home, source, bin_dir

    def run_updater(self, args: list[str], home: Path, source: Path, bin_dir: Path):
        env = os.environ | scratch_env(home)
        env |= {
            "CALLS": str(home / "calls"),
            "DOTFILES_SOURCE_DIR": str(source),
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        }
        return subprocess.run(
            ["bash", str(UPDATER), *args],
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def calls(self, home: Path) -> list[str]:
        log = home / "calls"
        return log.read_text().splitlines() if log.exists() else []

    def manifest(self, home: Path) -> dict:
        return json.loads((home / ".agents/.installed-manifest.json").read_text())

    def test_update_compactiondb_alone_syncs_records_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            home, source, bin_dir = self.fixture(directory, rsync=self.REAL_RSYNC)
            result = self.run_updater(["update_compactiondb"], home, source, bin_dir)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual("", result.stderr)
            self.assertEqual("fixture payload\n", (home / ".agents/compactiondb/README.md").read_text())
            step = self.manifest(home)["steps"]["update_compactiondb"]
            self.assertEqual("rsync", step["kind"])
            self.assertEqual("1.2.3", step["source_version"])
            self.assertEqual([str(home / ".agents/compactiondb")], step["paths"])
            # A local rsync forks its receiving side as `rsync --server ...` through PATH, so that call is its own.
            self.assertEqual(1, len([call for call in self.calls(home) if not call.startswith("rsync --server")]))

    def rsync_stub(self, bin_dir: Path, body: str) -> None:
        (bin_dir / "rsync").write_text(f'#!/bin/bash\nprintf "rsync %s\\n" "$*" >> "$CALLS"\n{body}\n')

    def doctor_findings(self, home: Path) -> list[str]:
        """make doctor's manifest lines for HOME: scripts/check-agent-runtime.py's own reader, so the test judges
        what the doctor reports, not what the manifest holds."""
        spec = importlib.util.spec_from_file_location("check_agent_runtime", ROOT / "scripts/check-agent-runtime.py")
        assert spec and spec.loader
        doctor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(doctor)
        return [doctor.asset_failure_message(finding) for finding in doctor.manifest_asset_findings(home)]

    def assert_marked_failed(self, home: Path, version: str) -> None:
        step = self.manifest(home)["steps"]["update_compactiondb"]
        self.assertEqual("rsync", step["kind"])
        self.assertEqual(version, step["source_version"])
        self.assertEqual([f"{home}/.agents/compactiondb/.sync-incomplete"], step["paths"])
        # The doctor prints the recorded path as spelled (abspath, not realpath).
        self.assertEqual(
            [
                f"asset manifest step 'update_compactiondb' has missing paths: {home}/.agents/compactiondb/.sync-incomplete"
            ],
            self.doctor_findings(home),
        )

    def test_update_compactiondb_alone_fails_when_rsync_fails_and_marks_the_step_failed(self):
        # verdicts/U276b: the real updater exited 0 after rsync exited 77 and recorded an installation whose payload
        # was absent. The failure is counted, the step is marked failed and the single-step run ends with
        # fail_on_pin_failures.
        with tempfile.TemporaryDirectory() as directory:
            home, source, bin_dir = self.fixture(directory, rsync="exit 77")
            result = self.run_updater(["update_compactiondb"], home, source, bin_dir)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"syncing the CompactionDB tree to {home}/.agents/compactiondb (rsync exit 77) failed", result.stderr
            )
            self.assertIn("1 plugin(s) (Claude Code or Codex) could not be checked or kept at their pin", result.stderr)
            self.assert_marked_failed(home, "1.2.3")
            self.assertEqual(
                ["rsync exit 77: the sync did not complete"],
                self.manifest(home)["steps"]["update_compactiondb"]["commands"],
            )
            self.assertEqual(1, len(self.calls(home)), "one rsync call")

    def test_a_partial_failed_sync_replaces_the_older_record_and_the_doctor_reports_it_until_a_sync_completes(self):
        # verdicts/U283 (P2 :2818): a failed sync into a destination an earlier run had filled kept that run's record,
        # the recorded directory existed, and the doctor reported nothing while the payload was missing. The record
        # is the last write of a completed sync; a failed one replaces it with the failure mark the doctor reports.
        with tempfile.TemporaryDirectory() as directory:
            home, source, bin_dir = self.fixture(directory, rsync=self.REAL_RSYNC)
            first = self.run_updater(["update_compactiondb"], home, source, bin_dir)
            self.assertEqual(0, first.returncode, first.stdout + first.stderr)
            self.assertEqual(
                [str(home / ".agents/compactiondb")], self.manifest(home)["steps"]["update_compactiondb"]["paths"]
            )
            self.assertEqual([], self.doctor_findings(home))

            (source / "vendor/compactiondb/CHANGELOG.md").write_text("## 1.2.4\n\n- next entry\n")
            (source / "vendor/compactiondb/README.md").write_text("next payload\n")
            self.rsync_stub(bin_dir, 'printf "half" > "$HOME/.agents/compactiondb/README.md"; exit 23')
            partial = self.run_updater(["update_compactiondb"], home, source, bin_dir)
            self.assertEqual(1, partial.returncode, partial.stdout + partial.stderr)
            self.assertIn(
                f"syncing the CompactionDB tree to {home}/.agents/compactiondb (rsync exit 23) failed", partial.stderr
            )
            self.assertTrue((home / ".agents/compactiondb").is_dir(), "the partial destination exists")
            self.assert_marked_failed(home, "1.2.4")

            self.rsync_stub(bin_dir, self.REAL_RSYNC)
            repaired = self.run_updater(["update_compactiondb"], home, source, bin_dir)
            self.assertEqual(0, repaired.returncode, repaired.stdout + repaired.stderr)
            self.assertEqual("next payload\n", (home / ".agents/compactiondb/README.md").read_text())
            step = self.manifest(home)["steps"]["update_compactiondb"]
            self.assertEqual(("1.2.4", [str(home / ".agents/compactiondb")]), (step["source_version"], step["paths"]))
            self.assertEqual([], self.doctor_findings(home))

    def test_a_sync_whose_payload_is_absent_is_marked_failed(self):
        # An rsync that exits 0 without the payload (nothing copied): the record waits for the synced CHANGELOG.md to
        # name the source's version, so the step is marked failed and counted.
        with tempfile.TemporaryDirectory() as directory:
            home, source, bin_dir = self.fixture(directory, rsync="exit 0")
            result = self.run_updater(["update_compactiondb"], home, source, bin_dir)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"verifying the CompactionDB tree at {home}/.agents/compactiondb (its CHANGELOG.md names no version, the source 1.2.3) failed",
                result.stderr,
            )
            self.assertIn("1 plugin(s) (Claude Code or Codex) could not be checked or kept at their pin", result.stderr)
            self.assert_marked_failed(home, "1.2.3")

    def test_update_compactiondb_alone_fails_when_the_manifest_record_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            home, source, bin_dir = self.fixture(directory, rsync=self.REAL_RSYNC)
            manifest_path = home / ".agents/.installed-manifest.json"
            manifest_path.write_text("not json\n")
            result = self.run_updater(["update_compactiondb"], home, source, bin_dir)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("ERROR: failed to record asset manifest step update_compactiondb", result.stderr)
            self.assertIn("1 plugin(s) (Claude Code or Codex) could not be checked or kept at their pin", result.stderr)
            self.assertEqual("not json\n", manifest_path.read_text(), "the manifest as it was")

    def test_prune_retired_manifest_steps_alone_fails_on_a_corrupt_manifest_and_prunes_a_retired_record(self):
        with tempfile.TemporaryDirectory() as directory:
            home, source, bin_dir = self.fixture(directory)
            manifest_path = home / ".agents/.installed-manifest.json"
            manifest_path.write_text("not json\n")
            result = self.run_updater(["prune_retired_manifest_steps"], home, source, bin_dir)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("pruning the retired steps from the installed asset manifest failed", result.stderr)
            self.assertIn("1 plugin(s) (Claude Code or Codex) could not be checked or kept at their pin", result.stderr)
            self.assertEqual("not json\n", manifest_path.read_text(), "the manifest as it was")

            record = {
                "installed_at": "2026-01-01T00:00:00Z",
                "kind": "rsync",
                "paths": [],
                "commands": [],
                "source_version": "1",
            }
            manifest_path.write_text(json.dumps({"version": 1, "steps": {"update_agmsg": record}}))
            result = self.run_updater(["prune_retired_manifest_steps"], home, source, bin_dir)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual("Pruned retired asset manifest step update_agmsg.\n", result.stdout)
            self.assertEqual({}, self.manifest(home)["steps"])
            self.assertEqual([], self.calls(home), "no rsync")

    def test_prune_retired_manifest_steps_alone_refuses_a_directory_or_a_dangling_link_at_the_manifest_path(self):
        # verdicts/U283 (P2 :2834): the library pruner returned 0 for a directory or a dangling link at the manifest
        # path, so the wrapper's exit 0 did not mean "no retired record". Both are refused naming the path.
        for case in ("a directory", "a dangling link"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, source, bin_dir = self.fixture(directory)
                manifest_path = home / ".agents/.installed-manifest.json"
                if case == "a directory":
                    manifest_path.mkdir()
                    (manifest_path / "kept").write_text("kept\n")
                else:
                    manifest_path.symlink_to(home / "absent")
                result = self.run_updater(["prune_retired_manifest_steps"], home, source, bin_dir)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(
                    f"ERROR: {manifest_path} is a link or no regular file; refusing to prune the installed asset manifest.",
                    result.stderr,
                )
                self.assertIn("pruning the retired steps from the installed asset manifest failed", result.stderr)
                self.assertEqual("", result.stdout)
                if case == "a directory":
                    self.assertEqual(["kept"], [path.name for path in manifest_path.iterdir()])
                else:
                    self.assertEqual(home / "absent", Path(os.readlink(manifest_path)))
                self.assertEqual([".installed-manifest.json"], [path.name for path in (home / ".agents").iterdir()])

    def test_a_linked_compactiondb_destination_is_refused_before_rsync_runs(self):
        # verdicts/U276b: with ~/.agents/compactiondb linked outside ~/.agents, rsync --delete ran through the link
        # and removed a file there. The destination itself, and every directory between it and the asset root,
        # must be real (assert_asset_destination).
        for case in ("the destination is a link", "the asset root is a link"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                home, source, bin_dir = self.fixture(directory, rsync=self.REAL_RSYNC)
                outside = Path(directory) / "outside"
                outside.mkdir()
                (outside / "sentinel").write_text("kept\n")
                if case == "the destination is a link":
                    (home / ".agents/compactiondb").symlink_to(outside)
                    refused = f"{home}/.agents/compactiondb is a symbolic link"
                else:
                    (home / ".agents").rmdir()
                    (home / ".agents").symlink_to(outside)
                    refused = f"{home}/.agents is a link or no directory; refusing to write {home}/.agents/compactiondb"
                result = self.run_updater(["update_compactiondb"], home, source, bin_dir)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(refused, result.stderr)
                self.assertEqual([], self.calls(home), "rsync never ran")
                self.assertEqual(["sentinel"], [path.name for path in outside.iterdir()], "nothing written outside")
                self.assertEqual("kept\n", (outside / "sentinel").read_text())

    def test_assert_asset_destination_accepts_real_directories_under_the_roots_and_refuses_every_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home, outside = root / "home", root / "outside"
            (home / ".agents/skills/security-audit").mkdir(parents=True)
            (home / ".local/share").mkdir(parents=True)
            outside.mkdir()
            (outside / "skills").mkdir()
            home_link = root / "home-link"
            home_link.symlink_to(home)
            (home / ".agents/linked-root").symlink_to(outside)
            (home / ".agents/skills/linked").symlink_to(outside)
            cases = (
                ("a new entry under ~/.agents", home, home / ".agents/compactiondb", 0, ""),
                ("an entry that is a directory", home, home / ".agents/skills/security-audit", 0, ""),
                ("a new entry under ~/.local", home, home / ".local/share/agent-assets", 0, ""),
                ("HOME spelled through a link", home_link, home_link / ".agents/compactiondb", 0, ""),
                ("outside the roots", home, home / ".config/x", 1, "is not under"),
                ("an absent parent", home, home / ".local/lib/omp-extensions/x", 1, "is a link or no directory"),
                ("a parent that is a link", home, home / ".agents/linked-root/x", 1, "is a link or no directory"),
                ("a link above the parent", home, home / ".agents/linked-root/skills/x", 1, "outside the asset root"),
                ("the entry is a link", home, home / ".agents/skills/linked", 1, "is a symbolic link"),
            )
            for case, fixture_home, destination, status, message in cases:
                with self.subTest(case=case):
                    result = subprocess.run(
                        [
                            "bash",
                            "-c",
                            'source "$1"; assert_asset_destination "$2"',
                            "bash",
                            str(UPDATER),
                            str(destination),
                        ],
                        env=os.environ | scratch_env(fixture_home),
                        capture_output=True,
                        text=True,
                        timeout=30,
                        check=False,
                    )
                    self.assertEqual(status, result.returncode, result.stdout + result.stderr)
                    self.assertEqual("", result.stdout)
                    if status == 0:
                        self.assertEqual("", result.stderr)
                    else:
                        self.assertIn(message, result.stderr)
                        self.assertIn(str(destination), result.stderr)
            self.assertEqual(["skills"], [path.name for path in outside.iterdir()], "nothing written outside")

    def test_assert_asset_destination_refuses_when_a_physical_path_cannot_be_read(self):
        # verdicts/U283 (P2 :141): the helper's two producers, `cd -P ... && pwd -P` of HOME and of the destination's
        # parent, each refuse when they fail. `pwd` and `cd` are shell functions that fail for one path (the shell
        # finds a function before its builtin), so each producer is broken on its own; the control case proves the
        # stubs change nothing when neither fails.
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            (home / ".agents").mkdir(parents=True)
            destination = home / ".agents/compactiondb"
            physical_home, physical_parent = os.path.realpath(home), os.path.realpath(home / ".agents")
            cases = (
                ("pwd -P fails for HOME", "pwd", physical_home, 1, f"the physical path of {home} could not be read"),
                (
                    "pwd -P fails for the parent",
                    "pwd",
                    physical_parent,
                    1,
                    f"the physical path of {home}/.agents could not be read",
                ),
                ("cd -P fails for HOME", "cd", str(home), 1, f"the physical path of {home} could not be read"),
                (
                    "cd -P fails for the parent",
                    "cd",
                    str(home / ".agents"),
                    1,
                    f"the physical path of {home}/.agents could not be read",
                ),
                ("neither fails (control)", "pwd", str(home / "elsewhere"), 0, ""),
            )
            for case, producer, fail_at, status, message in cases:
                with self.subTest(case=case):
                    result = subprocess.run(
                        [
                            "bash",
                            "-c",
                            'source "$1"; '
                            'pwd() { [ "$PWD" != "$FAIL_AT" ] || return 1; builtin pwd "$@"; }; '
                            'cd() { [ "${*: -1}" != "$FAIL_AT" ] || return 1; builtin cd "$@"; }; '
                            f'[ "{producer}" = pwd ] || unset -f pwd; [ "{producer}" = cd ] || unset -f cd; '
                            'assert_asset_destination "$2"',
                            "bash",
                            str(UPDATER),
                            str(destination),
                        ],
                        env=os.environ | scratch_env(home) | {"FAIL_AT": fail_at},
                        capture_output=True,
                        text=True,
                        timeout=30,
                        check=False,
                    )
                    self.assertEqual(status, result.returncode, result.stdout + result.stderr)
                    self.assertEqual("", result.stdout)
                    if status == 0:
                        self.assertEqual("", result.stderr)
                    else:
                        self.assertIn(f"ERROR: {message}; refusing to write {destination}.", result.stderr)
            self.assertEqual([".agents"], [path.name for path in home.iterdir()], "nothing written")

    def test_a_misuse_prints_the_usage_naming_every_step_and_runs_nothing(self):
        for args in (["nope"], ["update_compactiondb", "check_pstack"], [""]):
            with self.subTest(args=args), tempfile.TemporaryDirectory() as directory:
                home, source, bin_dir = self.fixture(directory, rsync=self.REAL_RSYNC)
                result = self.run_updater(args, home, source, bin_dir)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertEqual("", result.stdout)
                self.assertRegex(result.stderr, r"^Usage: scripts/update-agent-assets\.sh \[.*\]\n$")
                listed = result.stderr.strip().removeprefix("Usage: scripts/update-agent-assets.sh [").removesuffix("]")
                self.assertEqual(list(self.STEPS), listed.split(" | "))
                self.assertEqual([], self.calls(home), "no function ran")
                self.assertEqual([], list((home / ".agents").iterdir()), "nothing written")

    def test_the_dispatch_names_the_same_steps_as_the_usage_and_each_is_a_function(self):
        lines = UPDATER.read_text().splitlines()
        dispatch = [index for index, line in enumerate(lines) if line.strip() == 'case "$#:$1" in']
        self.assertEqual(1, len(dispatch), "one single-step dispatch in main")
        self.assertEqual(list(self.STEPS), re.findall(r"1:([a-z_]+)", lines[dispatch[0] + 1]))
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                ["bash", "-c", 'source "$1"; shift; declare -F "$@"', "bash", str(UPDATER), *self.STEPS],
                env=os.environ | scratch_env(Path(directory)),
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(list(self.STEPS), result.stdout.split())


class DestinationGuardCallSiteTest(unittest.TestCase):
    """Each step that deletes or syncs under the asset roots refuses a linked destination before its first write
    (verdicts/U283 P3 :1648: the helper's own cases do not prove a call site calls it). The real step runs against
    a linked destination with its tools as shell functions that log to $CALLS, so the recorder shows no install, sync
    or removal call after the refusal. update_compactiondb's and update_security_audit_skill's call sites are
    SingleStepModeTest.test_a_linked_compactiondb_destination_is_refused_before_rsync_runs and
    SecurityAuditSkillTest.test_a_skills_directory_that_is_a_link_is_refused_before_anything_is_written_beside_it."""

    def payload(self, home: Path) -> tuple[Path, str]:
        payload = home / "payload.tgz"
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
            info = tarfile.TarInfo("package/package.json")
            text = b'{"name":"fixture"}\n'
            info.size = len(text)
            tar.addfile(info, io.BytesIO(text))
        payload.write_bytes(buffer.getvalue())
        return payload, hashlib.sha256(payload.read_bytes()).hexdigest()

    def run_step(self, home: Path, step: str, stubs: str, payload: Path):
        download = 'curl() { echo "curl $*" >> "$CALLS"; cp "$PAYLOAD" "${@: -1}"; }; '
        return subprocess.run(
            ["bash", "-c", 'source "$1"; ' + download + stubs + step, "bash", str(UPDATER)],
            env=os.environ | scratch_env(home) | {"PAYLOAD": str(payload), "CALLS": str(home / "calls")},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def calls(self, home: Path) -> list[str]:
        log = home / "calls"
        return log.read_text().splitlines() if log.exists() else []

    def test_update_pi_claude_bridge_refuses_a_linked_omp_extensions_directory_before_it_unpacks(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            outside = Path(directory) / "outside"
            outside.mkdir()
            (outside / "sentinel").write_text("kept\n")
            (home / ".local/lib/node_modules/@oh-my-pi/pi-coding-agent").mkdir(parents=True)
            (home / ".local/lib/omp-extensions").symlink_to(outside)
            assets = home / "assets"
            (assets / "patches").mkdir(parents=True)
            (assets / "patches/01-fixture.patch").write_text("--- a\n+++ b\n")
            (assets / "bun.lock").write_text("fixture lockfile\n")
            payload, digest = self.payload(home)
            stubs = (
                f"PI_CLAUDE_BRIDGE_TARBALL_SHA256={digest}; PI_CLAUDE_BRIDGE_ASSET_DIR={assets}; "
                'bun() { echo "bun $*" >> "$CALLS"; }; '
            )
            result = self.run_step(home, "update_pi_claude_bridge", stubs, payload)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"ERROR: {home}/.local/lib/omp-extensions is a link or no directory; "
                f"refusing to write {home}/.local/lib/omp-extensions/pi-claude-bridge through it.",
                result.stderr,
            )
            self.assertEqual(["curl"], [call.split()[0] for call in self.calls(home)], "the download, then nothing")
            self.assertEqual(["sentinel"], [path.name for path in outside.iterdir()], "no staging tree, no install")
            self.assertEqual("kept\n", (outside / "sentinel").read_text())
            self.assertFalse((home / ".agents").exists(), "nothing recorded")

    def test_update_omp_refuses_a_linked_agent_assets_omp_directory_before_the_aside_and_the_install(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            outside = Path(directory) / "outside"
            outside.mkdir()
            (outside / "omp.previous").write_text("kept\n")
            (home / ".local/bin").mkdir(parents=True)
            (home / ".local/share/agent-assets").mkdir(parents=True)
            (home / ".local/share/agent-assets/omp").symlink_to(outside)
            foreign = home / ".local/bin/omp"
            foreign.write_text("#!/usr/bin/env bash\nprintf 'omp/0.0.1\\n'\n")
            foreign.chmod(0o755)
            payload, digest = self.payload(home)
            stubs = f"OMP_TARBALL_SHA256={digest}; " + 'npm() { echo "npm $*" >> "$CALLS"; }; '
            result = self.run_step(home, "update_omp", stubs, payload)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"Moving {foreign} to {home}/.local/share/agent-assets/omp/omp.previous", result.stdout)
            self.assertIn(
                f"ERROR: {home}/.local/share/agent-assets/omp is a link or no directory; "
                f"refusing to write {home}/.local/share/agent-assets/omp/omp.previous through it.",
                result.stderr,
            )
            self.assertEqual(["curl"], [call.split()[0] for call in self.calls(home)], "the download, then no npm")
            self.assertEqual(["omp.previous"], [path.name for path in outside.iterdir()])
            self.assertEqual("kept\n", (outside / "omp.previous").read_text(), "the rm -rf never ran through the link")
            self.assertEqual("#!/usr/bin/env bash\nprintf 'omp/0.0.1\\n'\n", foreign.read_text(), "the entry stays")
            self.assertFalse((home / ".agents").exists(), "nothing recorded")
