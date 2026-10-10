#!/usr/bin/env python3
"""Verify scripts/lib/github-release.sh: the 72-hour release window, its fetch paths, gh attestation checks,
the mise bootstrap's GPG and deferred-attestation paths, and the upgrade-tools phase that checks deferred ones."""

from __future__ import annotations

import datetime
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/lib/github-release.sh"
MISE_FINGERPRINT = "24853EC9F655CE80B48E6C3A8B81C9D17413A06D"
MISE_ARTIFACT = "mise-v2026.10.3-linux-x64.tar.gz"


def hours_ago(hours: float) -> str:
    moment = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def release(tag: str, published: str | None, *, draft: bool = False, prerelease: bool = False) -> dict:
    # Nested objects carry their own fields deeper, as the API's do.
    return {
        "tag_name": tag,
        "draft": draft,
        "prerelease": prerelease,
        "author": {"login": "bot", "tag_name": "decoy"},
        "published_at": published,
        "assets": [{"name": f"tool-{tag}.tar.gz", "created_at": hours_ago(1)}],
    }


class GithubReleaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="github-release-test-"))
        self.bin_dir = self.temp_dir / "bin"
        self.bin_dir.mkdir()
        self.log = self.temp_dir / "calls.log"
        # Only these tools are on PATH, so a runner's own curl, wget or gh never answers.
        for tool in ("awk", "date", "cat", "env"):
            (self.bin_dir / tool).symlink_to(shutil.which(tool))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def executable(self, name: str, body: str) -> None:
        path = self.bin_dir / name
        path.write_text("#!/bin/bash\n" + textwrap.dedent(body))
        path.chmod(0o755)

    def serve(self, releases: list[dict], tool: str = "curl") -> None:
        page = self.temp_dir / "releases.json"
        page.write_text(json.dumps(releases, indent=2) + "\n")
        self.executable(
            tool,
            f"""
            printf '{tool} %s\\n' "$*" >> "{self.log}"
            [ ! -t 0 ] && [[ " $* " == *" -K - "* ]] && cat >> "{self.log}.stdin"
            [ -z "${{FETCH_FAIL:-}}" ] || exit 22
            cat "{page}"
            """,
        )

    def link(self, *tools: str) -> None:
        for tool in tools:
            found = shutil.which(tool)
            if found and not (self.bin_dir / tool).exists():
                (self.bin_dir / tool).symlink_to(found)

    def run_helper(self, script: str, **env: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/bin/bash", "-c", f'source "$1"\n{script}', "_", str(HELPER)],
            env={"PATH": str(self.bin_dir), "HOME": str(self.temp_dir), **env},
            text=True,
            capture_output=True,
            check=False,
        )

    def test_tag_is_the_newest_stable_release_at_least_72_hours_old(self) -> None:
        self.serve(
            [
                release("v3.0.0", hours_ago(1)),
                release("v2.9.0", hours_ago(71)),
                release("v2.8.0", hours_ago(100), prerelease=True),
                release("v2.7.0", None, draft=True),
                release("v2.5.0", hours_ago(96)),
                release("v2.6.0", hours_ago(80)),
                release("v1.0.0", hours_ago(500)),
            ]
        )

        result = self.run_helper("github_release_tag owner/repo")

        self.assertEqual(0, result.returncode, result.stderr)
        # v2.6.0 is published later than v2.5.0 although the page lists it after.
        self.assertEqual("v2.6.0\n", result.stdout)
        self.assertIn(
            "curl -fsSL -H Accept: application/vnd.github+json https://api.github.com/repos/owner/repo/releases?per_page=30",
            self.log.read_text(),
        )

    def test_tag_fails_when_no_release_qualifies_or_the_fetch_fails(self) -> None:
        self.serve([release("v3.0.0", hours_ago(1)), release("v2.0.0", hours_ago(200), prerelease=True)])
        self.assertEqual(1, self.run_helper("github_release_tag owner/repo").returncode)

        self.serve([release("v1.0.0", hours_ago(500))])
        result = self.run_helper("github_release_tag owner/repo", FETCH_FAIL="1")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("", result.stdout)

    def test_tag_uses_wget_when_curl_is_absent(self) -> None:
        self.serve([release("v1.0.0", hours_ago(500))], tool="wget")

        result = self.run_helper("github_release_tag owner/repo")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("v1.0.0\n", result.stdout)
        self.assertIn("wget -qO - --header=Accept: application/vnd.github+json", self.log.read_text())

    def test_token_reaches_curl_on_stdin_never_on_the_command_line(self) -> None:
        self.serve([release("v1.0.0", hours_ago(500))])
        # The fallback token comes from gh's github.com login, never the default (possibly Enterprise) host.
        self.executable(
            "gh",
            f'''printf 'gh %s\\n' "$*" >> "{self.log}.gh"; [ "$*" = "auth token --hostname github.com" ] && printf "gh-credential\\n"\n''',
        )
        for name, env, expected in (
            ("GITHUB_TOKEN", {"GITHUB_TOKEN": "env-credential"}, "env-credential"),
            ("GH_TOKEN", {"GH_TOKEN": "gh-env-credential"}, "gh-env-credential"),
            ("gh auth token", {}, "gh-credential"),
        ):
            with self.subTest(source=name):
                self.log.unlink(missing_ok=True)
                Path(f"{self.log}.stdin").unlink(missing_ok=True)

                result = self.run_helper("github_release_tag owner/repo", **env)

                self.assertEqual(0, result.returncode, result.stderr)
                self.assertNotIn(expected, self.log.read_text())
                self.assertIn(" -K - ", self.log.read_text())
                self.assertEqual(
                    f'header = "Authorization: Bearer {expected}"\n', Path(f"{self.log}.stdin").read_text()
                )
        self.assertEqual("gh auth token --hostname github.com\n", Path(f"{self.log}.gh").read_text())

    def test_an_xtrace_never_shows_the_credential_and_is_restored(self) -> None:
        # Installers run set -x under DOTFILES_DEBUG; the credential must stay out of the trace.
        page = self.temp_dir / "releases.json"
        page.write_text(json.dumps([release("v1.0.0", hours_ago(500))], indent=2) + "\n")
        for tool in ("mktemp", "rm"):
            (self.bin_dir / tool).symlink_to(shutil.which(tool))
        for fetcher, env, received in (
            ("curl", {"GITHUB_TOKEN": "trace-credential"}, f"{self.log}.stdin"),
            ("wget", {"GH_TOKEN": "trace-credential"}, f"{self.log}.wgetrc"),
            ("curl", {}, f"{self.log}.stdin"),
        ):
            with self.subTest(fetcher=fetcher, source=next(iter(env), "gh auth token")):
                for name in ("curl", "wget", "gh"):
                    (self.bin_dir / name).unlink(missing_ok=True)
                Path(received).unlink(missing_ok=True)
                self.executable(
                    fetcher,
                    f"""
                    [[ " $* " == *" -K - "* ]] && cat > "{self.log}.stdin"
                    for arg in "$@"; do case "$arg" in --config=*) cat "${{arg#--config=}}" > "{self.log}.wgetrc" ;; esac; done
                    cat "{page}"
                    """,
                )
                if not env:
                    self.executable("gh", 'printf "trace-credential\\n"\n')

                result = self.run_helper(
                    'set -x\ngithub_release_tag owner/repo\ncase $- in *x*) echo "xtrace restored" >&2 ;; esac',
                    **env,
                    TMPDIR=str(self.temp_dir),
                )

                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("v1.0.0\n", result.stdout)
                self.assertNotIn("trace-credential", result.stderr)
                self.assertIn("xtrace restored", result.stderr)
                self.assertIn("Authorization: Bearer trace-credential", Path(received).read_text())

    def test_tag_fails_when_the_download_is_truncated(self) -> None:
        # curl emits a complete eligible release and then fails: the lookup must not use it.
        page = self.temp_dir / "releases.json"
        page.write_text(json.dumps([release("v1.0.0", hours_ago(500))], indent=2) + "\n")
        self.executable("curl", f'cat "{page}"\nexit 18\n')

        result = self.run_helper("set +o pipefail\ngithub_release_tag owner/repo")

        self.assertNotEqual(0, result.returncode)
        self.assertEqual("", result.stdout)

    def test_wget_gets_the_token_from_a_private_wgetrc_never_the_command_line(self) -> None:
        page = self.temp_dir / "releases.json"
        page.write_text(json.dumps([release("v1.0.0", hours_ago(500))], indent=2) + "\n")
        self.executable(
            "wget",
            f"""
            printf 'wget %s\\n' "$*" >> "{self.log}"
            for arg in "$@"; do
                case "$arg" in --config=*) cat "${{arg#--config=}}" > "{self.log}.wgetrc"; stat -c %a "${{arg#--config=}}" > "{self.log}.mode" 2> /dev/null || stat -f %Lp "${{arg#--config=}}" > "{self.log}.mode" ;; esac
            done
            cat "{page}"
            """,
        )
        for tool in ("mktemp", "rm", "stat"):
            (self.bin_dir / tool).symlink_to(shutil.which(tool))

        result = self.run_helper(
            "github_release_tag owner/repo", **{"GITHUB_TOKEN": "wget-credential", "TMPDIR": str(self.temp_dir)}
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("v1.0.0\n", result.stdout)
        self.assertNotIn("wget-credential", self.log.read_text())
        self.assertEqual("header = Authorization: Bearer wget-credential\n", Path(f"{self.log}.wgetrc").read_text())
        self.assertEqual("600\n", Path(f"{self.log}.mode").read_text())
        # The wgetrc is removed once wget returns.
        self.assertEqual([], list(self.temp_dir.glob("github-release.*")))

    def test_attestation_needs_an_authenticated_gh_and_fails_hard_on_a_bad_attestation(self) -> None:
        asset = self.temp_dir / "asset.tar.gz"
        asset.write_text("payload\n")
        self.assertEqual(2, self.run_helper(f'github_release_attestation owner/repo v1 "{asset}"').returncode)
        for outcome, version, auth_status, verify_status, expected in (
            ("not authenticated", "2.93.0", 1, 0, 2),
            ("verified", "2.93.0", 0, 0, 0),
            ("verified with a newer gh", "3.0.1", 0, 0, 0),
            ("attestation failed", "2.93.0", 0, 1, 1),
            # gh 2.92.0 and earlier leak credentials to TUF mirrors (GHSA-8xvp-7hj6-mcj9): never used.
            ("gh too old", "2.92.0", 0, 0, 2),
            ("gh version unreadable", "", 0, 0, 2),
        ):
            with self.subTest(outcome=outcome):
                self.log.unlink(missing_ok=True)
                self.executable(
                    "gh",
                    f"""
                    printf 'gh %s\\n' "$*" >> "{self.log}"
                    [ "$1" = --version ] && {{ [ -n "{version}" ] && printf 'gh version {version} (2026-10-01)\\n'; exit 0; }}
                    [ "$*" = "auth status --hostname github.com" ] && exit {auth_status}
                    [ "$1 $2" = "release verify-asset" ] && exit {verify_status}
                    exit 3
                    """,
                )

                result = self.run_helper(f'github_release_attestation owner/repo v1 "{asset}"')

                self.assertEqual(expected, result.returncode, result.stderr)
                if expected != 2:
                    self.assertIn(
                        f"gh release verify-asset v1 {asset} --repo github.com/owner/repo", self.log.read_text()
                    )
                else:
                    self.assertNotIn("verify-asset", self.log.read_text())
                if outcome.startswith("gh version unreadable") or outcome == "gh too old":
                    self.assertIn("GHSA-8xvp-7hj6-mcj9", result.stderr)

    def test_attestation_prefers_mise_gh_over_an_older_system_gh(self) -> None:
        # Ubuntu's apt gh predates 2.93.0; mise's current gh must win even when the old one comes first.
        asset = self.temp_dir / "asset.tar.gz"
        asset.write_text("payload\n")
        self.executable(
            "gh",
            f'printf "system-gh %s\\n" "$*" >> "{self.log}"\n[ "$1" = --version ] && printf "gh version 2.45.0\\n"\nexit 0\n',
        )
        shim = self.temp_dir / ".local/share/mise/shims/gh"
        shim.parent.mkdir(parents=True)
        shim.write_text(
            f'#!/bin/bash\nprintf "mise-gh %s\\n" "$*" >> "{self.log}"\n[ "$1" = --version ] && printf "gh version 2.93.0\\n"\nexit 0\n'
        )
        shim.chmod(0o755)

        result = self.run_helper(f'github_release_attestation owner/repo v1 "{asset}"; echo "rc=$?"; command -v gh')

        self.assertIn("rc=0", result.stdout, result.stderr)
        self.assertIn(f"mise-gh release verify-asset v1 {asset} --repo github.com/owner/repo", self.log.read_text())
        self.assertNotIn("system-gh", self.log.read_text())
        # The caller's PATH is untouched afterwards.
        self.assertTrue(result.stdout.rstrip().endswith(f"{self.bin_dir}/gh"), result.stdout)

    def test_tag_must_be_a_version_or_the_lookup_fails(self) -> None:
        # The tag reaches URLs, file names and command lines, so anything but a version is refused at the source.
        for tag, accepted in (
            ("v2026.10.3", True),
            ("2.73.0", True),
            ("v1.0.0-rc.1", True),
            ("v0.21.1+build.5", True),
            ("v$(printf${IFS}X)", False),
            ("v1.0.0;id", False),
            ("../v1.0.0", False),
            ("v1.0.0 x", False),
            ("latest", False),
        ):
            with self.subTest(tag=tag):
                self.serve([release(tag, hours_ago(100)), release("v1.0.0", hours_ago(500))])

                result = self.run_helper("github_release_tag owner/repo")

                if accepted:
                    self.assertEqual((0, f"{tag}\n"), (result.returncode, result.stdout), result.stderr)
                else:
                    self.assertEqual((1, ""), (result.returncode, result.stdout))
                    self.assertIn(f"unexpected release tag {tag} for owner/repo", result.stderr)

    def test_make_docker_never_runs_the_fetched_tag(self) -> None:
        # The auditor's tag: interpolated into the recipe's shell source, it ran a command.
        marker = self.temp_dir / "ran"
        self.serve([release(f"v$(touch${{IFS}}{marker})", hours_ago(100))])
        self.executable("gh", "exit 1\n")
        self.executable("docker", f'printf "docker %s\\n" "$*" >> "{self.log}.docker"\n')
        env = {"PATH": f"{self.bin_dir}:/usr/bin:/bin", "HOME": str(self.temp_dir)}

        dry = subprocess.run(["make", "-n", "docker"], cwd=ROOT, env=env, text=True, capture_output=True, check=False)

        self.assertEqual(0, dry.returncode, dry.stderr)
        # The recipe resolves the tag itself, so a dry run fetches nothing and prints no fetched text.
        self.assertIn("github_release_tag twpayne/chezmoi", dry.stdout)
        self.assertNotIn("touch", dry.stdout)
        self.assertFalse(self.log.exists())

        real = subprocess.run(["make", "docker"], cwd=ROOT, env=env, text=True, capture_output=True, check=False)

        self.assertNotEqual(0, real.returncode)
        self.assertFalse(marker.exists())
        self.assertIn("unexpected release tag", real.stderr)
        self.assertFalse(Path(f"{self.log}.docker").exists())

    def mise_bootstrap(self, *, gpg: str | None, gh: str | None = None) -> subprocess.CompletedProcess[str]:
        """Run _install_mise_binary against a fake jdx/mise release.

        gpg is None (gpg and gpgv absent), "good", "bad signature", "wrong fingerprint", "expired" or "two keys";
        gh is None (absent), "verifies" or "fails".
        """
        home = self.temp_dir / "home"
        self.state = self.temp_dir / "state"
        (self.temp_dir / "tmp").mkdir(exist_ok=True)
        payload = self.temp_dir / "payload/mise/bin/mise"
        payload.parent.mkdir(parents=True)
        payload.write_text("#!/bin/sh\nprintf 'mise 2026.10.3\\n'\n")
        payload.chmod(0o755)
        self.archive = self.temp_dir / MISE_ARTIFACT
        with tarfile.open(self.archive, "w:gz") as archive:
            archive.add(self.temp_dir / "payload/mise", arcname="mise")
        digest = subprocess.run(
            ["shasum", "-a", "256", str(self.archive)], text=True, capture_output=True, check=True
        ).stdout.split()[0]
        sums = self.temp_dir / "sums"
        sums.write_text(f"{'0' * 64}  ./mise-v2026.10.3-linux-arm64.tar.gz\n{digest}  ./{MISE_ARTIFACT}\n")
        page = self.temp_dir / "releases.json"
        page.write_text(json.dumps([release("v2026.10.3", hours_ago(100))], indent=2) + "\n")
        self.executable(
            "curl",
            f"""
            printf 'curl %s\\n' "$*" >> "{self.log}"
            out=""; url=""
            while [ "$#" -gt 0 ]; do case "$1" in -o) out="$2"; shift ;; https://*) url="$1" ;; esac; shift; done
            case "$url" in
                https://api.github.com/*) cat "{page}" ;;
                https://keys.openpgp.org/*) printf 'armored key\\n' > "$out" ;;
                */SHASUMS256.txt) cp "{sums}" "$out" ;;
                */SHASUMS256.asc) printf 'clearsigned sums\\n' > "$out" ;;
                */{MISE_ARTIFACT}) cp "{self.archive}" "$out" ;;
                *) exit 22 ;;
            esac
            """,
        )
        self.executable("uname", '[ "$1" = -s ] && printf "Linux\\n" || printf "x86_64\\n"\n')
        real_mktemp = shutil.which("mktemp")
        # macOS mktemp -d ignores TMPDIR; keep every temporary file under the test directory, as on Linux.
        self.executable(
            "mktemp",
            f'if [ "$*" = -d ]; then exec "{real_mktemp}" -d "$TMPDIR/tmp.XXXXXX"; fi\nexec "{real_mktemp}" "$@"\n',
        )
        self.link("dirname", "tar", "gzip", "install", "mv", "rm", "mkdir", "cp", "chmod", "sha256sum", "shasum")
        if gpg is not None:
            fingerprint = "0" * 40 if gpg == "wrong fingerprint" else MISE_FINGERPRINT
            expiration = "1000000000" if gpg == "expired" else "1830442114"
            second = (
                f"printf 'pub:-:4096:1:0000000000000000:1704211734:::-:::scESC:::\\nfpr:::::::::{'1' * 40}:\\n'"
                if gpg == "two keys"
                else ":"
            )
            self.executable(
                "gpg",
                f"""
                printf 'gpg %s\\n' "$*" >> "{self.log}"
                case " $* " in
                    *" --import-options show-only --import "*)
                        printf 'pub:-:4096:1:8B81C9D17413A06D:1704211734:{expiration}::-:::scESC:::\\n'
                        printf 'fpr:::::::::{fingerprint}:\\n'
                        printf 'sub:-:4096:1:261143C501F46C5B:1704211734:1830442114:::::e:::\\n'
                        printf 'fpr:::::::::58BBFC6002B54E1829C284F5261143C501F46C5B:\\n'
                        {second} ;;
                    *" --dearmor "*)
                        while [ "$#" -gt 0 ]; do [ "$1" = --output ] && printf 'keyring\\n' > "$2"; shift; done ;;
                esac
                """,
            )
            # A bad signature still streams the signed text: only the exit status may decide.
            self.executable(
                "gpgv",
                f"""
                printf 'gpgv %s\\n' "$*" >> "{self.log}"
                cat "{sums}"
                {"exit 1" if gpg == "bad signature" else "exit 0"}
                """,
            )
        if gh is not None:
            self.executable(
                "gh",
                f"""
                printf 'gh %s\\n' "$*" >> "{self.log}"
                [ "$1" = --version ] && {{ printf 'gh version 2.93.0 (2026-10-01)\\n'; exit 0; }}
                [ "$*" = "auth status --hostname github.com" ] && exit 0
                [ "$1 $2" = "release verify-asset" ] && exit {0 if gh == "verifies" else 1}
                exit 1
                """,
            )
        return subprocess.run(
            ["/bin/bash", "-c", 'source "$1"; _install_mise_binary', "_", str(ROOT / "install/common/mise.sh")],
            env={
                "PATH": str(self.bin_dir),
                "HOME": str(home),
                "XDG_STATE_HOME": str(self.state),
                "TMPDIR": str(self.temp_dir / "tmp"),
            },
            text=True,
            capture_output=True,
            check=False,
        )

    def test_mise_bootstrap_without_gh_defers_the_attestation(self) -> None:
        result = self.mise_bootstrap(gpg=None)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.temp_dir / "home/.local/bin/mise").exists())
        self.assertIn(
            "mise v2026.10.3: attestation deferred: verified by SHASUMS256.txt (no gpg here) only until gh is authenticated.",
            result.stdout,
        )
        record = self.state / "dotfiles/pending-attestation/mise"
        self.assertEqual(f"jdx/mise v2026.10.3 {MISE_ARTIFACT}\n", (record / "release").read_text())
        self.assertEqual(self.archive.read_bytes(), (record / MISE_ARTIFACT).read_bytes())
        self.assertIn("/v2026.10.3/SHASUMS256.txt", self.log.read_text())
        self.assertNotIn("SHASUMS256.asc", self.log.read_text())

    def test_mise_bootstrap_verifies_the_gpg_signature_when_gpg_is_present(self) -> None:
        result = self.mise_bootstrap(gpg="good")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.temp_dir / "home/.local/bin/mise").exists())
        log = self.log.read_text()
        self.assertIn(f"https://keys.openpgp.org/vks/v1/by-fingerprint/{MISE_FINGERPRINT}", log)
        self.assertIn("/v2026.10.3/SHASUMS256.asc", log)
        self.assertIn("gpgv --keyring ", log)
        # The checksums come from the signed text, never from the unsigned SHASUMS256.txt.
        self.assertNotIn("SHASUMS256.txt", log)
        self.assertIn(f"verified by SHASUMS256.asc (GPG key {MISE_FINGERPRINT}) only until", result.stdout)
        self.assertTrue((self.state / "dotfiles/pending-attestation/mise/release").exists())

    def test_mise_bootstrap_installs_nothing_when_the_signature_or_key_is_wrong(self) -> None:
        for gpg, message in (
            ("bad signature", "GPG signature check failed for SHASUMS256.asc of mise v2026.10.3."),
            ("wrong fingerprint", "mise release key validation failed."),
            ("expired", "mise release key validation failed."),
            ("two keys", "mise release key validation failed."),
        ):
            with self.subTest(gpg=gpg):
                self.tearDown()
                self.setUp()

                result = self.mise_bootstrap(gpg=gpg)

                self.assertNotEqual(0, result.returncode)
                self.assertIn(message, result.stderr)
                self.assertFalse((self.temp_dir / "home/.local/bin/mise").exists())
                self.assertFalse((self.state / "dotfiles/pending-attestation").exists())
                if gpg != "bad signature":
                    self.assertNotIn("gpgv ", self.log.read_text())

    def test_mise_bootstrap_with_gh_verifies_the_attestation_now(self) -> None:
        result = self.mise_bootstrap(gpg=None, gh="verifies")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.temp_dir / "home/.local/bin/mise").exists())
        self.assertIn(f"/{MISE_ARTIFACT} --repo github.com/jdx/mise", self.log.read_text())
        self.assertFalse((self.state / "dotfiles/pending-attestation").exists())
        self.tearDown()
        self.setUp()

        result = self.mise_bootstrap(gpg=None, gh="fails")

        self.assertNotEqual(0, result.returncode)
        self.assertIn(f"GitHub release attestation failed for {MISE_ARTIFACT}.", result.stderr)
        self.assertFalse((self.temp_dir / "home/.local/bin/mise").exists())
        self.assertFalse((self.state / "dotfiles/pending-attestation").exists())

    def test_a_deferral_that_cannot_be_recorded_fails(self) -> None:
        # Never a silent downgrade: without the record the attestation would never be checked.
        self.link("rm", "mkdir", "cp")
        asset = self.temp_dir / "asset.tar.gz"
        asset.write_text("payload\n")
        blocker = self.temp_dir / "state"
        blocker.write_text("a file where the state directory belongs\n")

        result = self.run_helper(
            f'github_release_defer_attestation tool owner/repo v1 "{asset}" checksums', XDG_STATE_HOME=str(blocker)
        )

        self.assertEqual(1, result.returncode)
        self.assertEqual("", result.stdout)

    def pending(self, *tools: str) -> Path:
        state = self.temp_dir / "state"
        for tool in tools:
            record = state / "dotfiles/pending-attestation" / tool
            record.mkdir(parents=True)
            (record / f"{tool}.tar.gz").write_text(f"{tool} archive\n")
            (record / "release").write_text(f"owner/{tool} v1.2.3 {tool}.tar.gz\n")
        return state

    def run_upgrade(self, script: str, state: Path, *, gh: bool, fail: str = "") -> subprocess.CompletedProcess[str]:
        self.link("dirname", "rm")
        if gh:
            self.executable(
                "gh",
                f"""
                printf 'gh %s\\n' "$*" >> "{self.log}"
                [ "$1" = --version ] && {{ printf 'gh version 2.93.0 (2026-10-01)\\n'; exit 0; }}
                [ "$*" = "auth status --hostname github.com" ] && exit 0
                [ "$1 $2" = "release verify-asset" ] && {{ [[ -n "{fail}" && "$4" == *"/{fail}.tar.gz" ]] && exit 1; exit 0; }}
                exit 1
                """,
            )
        return subprocess.run(
            ["/bin/bash", "-c", f'source "$1"\n{script}', "_", str(ROOT / "scripts/upgrade-tools.sh")],
            env={"PATH": str(self.bin_dir), "HOME": str(self.temp_dir), "XDG_STATE_HOME": str(state)},
            text=True,
            capture_output=True,
            check=False,
        )

    def test_upgrade_tools_checks_deferred_attestations_once_gh_is_ready(self) -> None:
        phase = (
            'status=0\nverify_pending_attestations || status=$?\necho "status=${status} warnings=${optional_warnings}"'
        )
        pending = self.temp_dir / "state/dotfiles/pending-attestation"

        result = self.run_upgrade(phase, self.temp_dir / "state", gh=False)
        self.assertEqual(("status=0 warnings=0\n", ""), (result.stdout, result.stderr))

        # gh not ready: one warning, and both records wait for the next make update.
        state = self.pending("chezmoi", "mise")
        result = self.run_upgrade(phase, state, gh=False)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("status=0 warnings=1", result.stdout)
        self.assertEqual(
            "warning: the GitHub release attestation of chezmoi, mise is not verified yet: "
            "run make gh-auth, then make update.\n",
            result.stderr,
        )
        self.assertEqual(["chezmoi", "mise"], sorted(path.name for path in pending.iterdir()))

        # One fails: a required failure that names the tool and keeps its record; the verified one is removed.
        result = self.run_upgrade(phase, state, gh=True, fail="mise")
        self.assertIn("status=1 warnings=0", result.stdout)
        self.assertIn("Verified the GitHub release attestation of chezmoi v1.2.3.", result.stdout)
        self.assertIn(
            f"required: mise v1.2.3 failed its GitHub release attestation ({pending}/mise/mise.tar.gz)", result.stderr
        )
        self.assertIn(
            f"gh release verify-asset v1.2.3 {pending}/mise/mise.tar.gz --repo github.com/owner/mise",
            self.log.read_text(),
        )
        self.assertEqual(["mise"], [path.name for path in pending.iterdir()])

        result = self.run_upgrade(phase, state, gh=True)
        self.assertIn("status=0 warnings=0", result.stdout)
        self.assertEqual([], list(pending.iterdir()))

    def test_a_failed_deferred_attestation_stops_make_update_before_mise(self) -> None:
        stubs = (
            'upgrade_homebrew() { :; }\nupgrade_mise_self() { echo "mise self-update ran"; }\n'
            "upgrade_mise_tools() { :; }\nupgrade_uv_tools() { :; }\nupgrade_gh_extensions() { :; }\n"
            'upgrade_apt_packages() { :; }\nstatus=0\nmain || status=$?\necho "status=${status}"'
        )
        state = self.pending("mise")

        result = self.run_upgrade(stubs, state, gh=True, fail="mise")

        self.assertIn("status=1", result.stdout)
        self.assertNotIn("mise self-update ran", result.stdout)
        self.assertIn("required failure: pending release attestations", result.stderr)
        self.assertIn("stopped at the pending release attestations", result.stderr)

        result = self.run_upgrade(stubs, state, gh=True)

        self.assertIn("status=0", result.stdout)
        self.assertIn("mise self-update ran", result.stdout)

    def test_setup_sh_carries_an_exact_copy_of_the_helper(self) -> None:
        # setup.sh runs before the repository exists, so it cannot source the helper.
        helper = HELPER.read_text()
        body = helper[helper.index("# Releases younger than this stay out") :]
        setup = (ROOT / "setup.sh").read_text()
        begin = "# --- github-release.sh begin ---\n"
        copy = setup[setup.index(begin) + len(begin) : setup.index("# --- github-release.sh end ---\n")]
        self.assertEqual(body, copy)

    def test_the_window_is_the_mise_cooldown(self) -> None:
        self.assertIn("GITHUB_RELEASE_MIN_AGE_HOURS=72\n", HELPER.read_text())
        self.assertIn('minimum_release_age = "72h"', (ROOT / "home/dot_mise/config.toml").read_text())
        # CI installs the mise hosts get: every mise-action step takes the same window.
        for workflow in sorted((ROOT / ".github/workflows").glob("*.y*ml")):
            text = workflow.read_text()
            steps = text.count("uses: jdx/mise-action@")
            self.assertEqual(steps, text.count("minimum_release_age: 72h\n"), workflow.name)


if __name__ == "__main__":
    unittest.main()
