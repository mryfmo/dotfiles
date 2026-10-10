#!/usr/bin/env python3
"""Verify scripts/lib/github-release.sh: the 72-hour release window, its fetch paths and gh attestation checks;
and the mise and chezmoi bootstraps, which verify the newest release before it runs or install a reviewed fallback."""

from __future__ import annotations

import datetime
import hashlib
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

    def test_an_enterprise_host_token_never_reaches_github_com(self) -> None:
        # A GitHub Enterprise Server job exports its own GITHUB_TOKEN; neither curl nor gh may carry it to github.com.
        self.serve([release("v1.0.0", hours_ago(500))])
        asset = self.temp_dir / "asset.tar.gz"
        asset.write_text("payload\n")
        self.executable(
            "gh",
            f"""
            printf 'gh %s tokens=%s\\n' "$*" "${{GITHUB_TOKEN:-}}${{GH_TOKEN:-}}" >> "{self.log}.gh"
            [ "$1" = --version ] && {{ printf 'gh version 2.93.0 (2026-10-01)\\n'; exit 0; }}
            [ "$*" = "auth token --hostname github.com" ] && {{ printf '%s\\n' "${{GH_TOKEN:-${{GITHUB_TOKEN:-dotcom-credential}}}}"; exit 0; }}
            [ "$*" = "auth status --hostname github.com" ] && exit 0
            [ "$1 $2" = "release verify-asset" ] && exit 0
            exit 1
            """,
        )
        for name, env in (
            ("GHES job", {"GITHUB_SERVER_URL": "https://ghes.example.com", "GITHUB_TOKEN": "enterprise-credential"}),
            ("GH_HOST", {"GH_HOST": "ghes.example.com", "GH_TOKEN": "enterprise-credential"}),
        ):
            with self.subTest(context=name):
                for path in (self.log, Path(f"{self.log}.stdin"), Path(f"{self.log}.gh")):
                    path.unlink(missing_ok=True)

                result = self.run_helper(
                    f'github_release_tag owner/repo && github_release_attestation owner/repo v1.0.0 "{asset}"', **env
                )

                self.assertEqual(0, result.returncode, result.stderr)
                # The fallback is gh's own github.com login, never the Enterprise token.
                self.assertEqual(
                    'header = "Authorization: Bearer dotcom-credential"\n', Path(f"{self.log}.stdin").read_text()
                )
                gh_calls = Path(f"{self.log}.gh").read_text()
                self.assertNotIn("enterprise-credential", gh_calls)
                self.assertIn("release verify-asset v1.0.0", gh_calls)

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

    def test_an_interrupted_wget_never_strands_the_credential_file(self) -> None:
        # wget is killed mid-download (its parent shell gets SIGTERM): the private wgetrc must still go.
        for tool in ("mktemp", "rm", "sleep"):
            (self.bin_dir / tool).symlink_to(shutil.which(tool))
        self.executable("wget", 'kill -TERM "$PPID"\nsleep 2\n')

        result = self.run_helper(
            'github_release_list owner/repo; echo "status=$?"',
            **{"GITHUB_TOKEN": "interrupted-credential", "TMPDIR": str(self.temp_dir)},
        )

        self.assertEqual([], list(self.temp_dir.glob("github-release.*")), result.stdout + result.stderr)
        self.assertNotIn("status=0", result.stdout)

    def test_attestation_needs_an_authenticated_gh_and_fails_hard_on_a_bad_attestation(self) -> None:
        asset = self.temp_dir / "asset.tar.gz"
        asset.write_text("payload\n")
        self.link("basename")
        self.assertEqual(2, self.run_helper(f'github_release_attestation owner/repo v1 "{asset}"').returncode)
        for outcome, version, auth_status, verify_status, expected in (
            ("not authenticated", "2.93.0", 1, 0, 2),
            ("verified", "2.93.0", 0, 0, 0),
            ("verified with a newer gh", "3.0.1", 0, 0, 0),
            ("attestation failed", "2.93.0", 0, 1, 1),
            # gh 2.92.0 and earlier leak credentials to TUF mirrors (GHSA-8xvp-7hj6-mcj9): never used.
            ("gh too old", "2.92.0", 0, 0, 2),
            ("gh version unreadable", "", 0, 0, 2),
            # A prerelease of the fixed version sorts below it (SemVer), so it is not used either.
            ("gh prerelease of the fixed version", "2.93.0-rc.1", 0, 0, 2),
        ):
            with self.subTest(outcome=outcome):
                self.log.unlink(missing_ok=True)
                self.executable(
                    "gh",
                    f"""
                    printf 'gh %s\\n' "$*" >> "{self.log}"
                    [ "$1" = --version ] && {{ [ -n "{version}" ] && printf 'gh version {version} (2026-10-01)\\n'; exit 0; }}
                    [ "$*" = "auth status --hostname github.com" ] && exit {auth_status}
                    if [ "$1 $2" = "release verify-asset" ]; then
                        printf 'Calculated digest for %s: sha256:0000\\n' "$(basename "$4")"
                        [ {verify_status} -ne 0 ] || printf '✓ Verification succeeded! %s is present in release %s\\n' "$(basename "$4")" "$3"
                        exit {verify_status}
                    fi
                    exit 3
                    """,
                )

                result = self.run_helper(f'github_release_attestation owner/repo v1 "{asset}"')

                self.assertEqual(expected, result.returncode, result.stderr)
                # gh's report reaches stderr only, so a caller's stdout carries nothing but its own output.
                self.assertEqual("", result.stdout)
                if expected != 2:
                    self.assertIn(
                        f"gh release verify-asset v1 {asset} --repo github.com/owner/repo", self.log.read_text()
                    )
                else:
                    self.assertNotIn("verify-asset", self.log.read_text())
                if outcome in ("gh version unreadable", "gh too old", "gh prerelease of the fixed version"):
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

    def test_make_docker_verifies_chezmoi_on_the_host_and_passes_its_sha256(self) -> None:
        # A build has no gh: make docker checks the checksum and the attestation, and the Dockerfile trusts only the sha.
        archive = "chezmoi_2.73.0_linux_amd64.tar.gz"
        payload = b"chezmoi archive\n"
        digest = hashlib.sha256(payload).hexdigest()
        page = self.temp_dir / "releases.json"
        page.write_text(json.dumps([release("v2.73.0", hours_ago(100))], indent=2) + "\n")
        (self.temp_dir / "payload").write_bytes(payload)
        self.executable(
            "curl",
            f"""
            printf 'curl %s\\n' "$*" >> "{self.log}"
            out=""; url=""
            while [ "$#" -gt 0 ]; do case "$1" in -o) out="$2"; shift ;; https://*) url="$1" ;; esac; shift; done
            case "$url" in
                https://api.github.com/*) cat "{page}" ;;
                */{archive}) cp "{self.temp_dir}/payload" "$out" ;;
                */chezmoi_2.73.0_checksums.txt) printf '%s  {archive}\\n' "${{CHECKSUM:-{digest}}}" > "$out" ;;
                *) exit 22 ;;
            esac
            """,
        )
        self.executable(
            "gh",
            f"""
            printf 'gh %s\\n' "$*" >> "{self.log}"
            [ "$1" = --version ] && {{ printf 'gh version 2.93.0 (2026-10-01)\\n'; exit 0; }}
            [ "$*" = "auth status --hostname github.com" ] && exit "${{GH_AUTH:-0}}"
            if [ "$1 $2" = "release verify-asset" ]; then
                # gh's real report, on stdout as gh 2.93.0 prints it.
                printf 'Calculated digest for %s: sha256:%s\\n' "$(basename "$4")" "{digest}"
                [ "${{GH_VERIFY:-0}}" -ne 0 ] || printf '✓ Verification succeeded! %s is present in release %s\\n' "$(basename "$4")" "$3"
                exit "${{GH_VERIFY:-0}}"
            fi
            exit 1
            """,
        )
        self.executable(
            "docker",
            f"""
            printf 'docker %s\\n' "$*" >> "{self.log}"
            case "$1:$*" in
                inspect:*chezmoi.version*) [ -n "${{IMAGE_VERSION:-}}" ] || exit 1; printf '%s\\n' "$IMAGE_VERSION" ;;
                inspect:*chezmoi.sha256*) [ -n "${{IMAGE_VERSION:-}}" ] || exit 1; printf '%s\\n' "${{IMAGE_SHA256:-}}" ;;
                version:*) printf 'amd64\\n' ;;
            esac
            exit 0
            """,
        )
        for case, extra, verified in (
            ("verified", {}, True),
            ("attestation refused", {"GH_VERIFY": "1"}, False),
            ("checksum mismatch", {"CHECKSUM": "0" * 64}, False),
            ("gh not ready", {"GH_AUTH": "1"}, False),
            # An image the previous recipe built carries the version but no verified sha256: rebuilt.
            ("old image without the sha256 label", {"IMAGE_VERSION": "2.73.0"}, True),
            ("image this recipe built", {"IMAGE_VERSION": "2.73.0", "IMAGE_SHA256": digest}, "reused"),
        ):
            with self.subTest(case=case):
                self.log.unlink(missing_ok=True)

                result = subprocess.run(
                    ["make", "docker"],
                    cwd=ROOT,
                    env={
                        "PATH": f"{self.bin_dir}:/usr/bin:/bin",
                        "HOME": str(self.temp_dir),
                        "TMPDIR": str(self.temp_dir),
                        **extra,
                    },
                    text=True,
                    capture_output=True,
                    check=False,
                )

                log = self.log.read_text()
                if verified == "reused":
                    # Nothing to verify or build: the image already holds a host-verified chezmoi.
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertNotIn("docker build", log)
                    self.assertNotIn("verify-asset", log)
                    self.assertIn("docker run -it", log)
                    continue
                if verified:
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertIn(f"gh release verify-asset v2.73.0 {self.temp_dir}/github-release.", log)
                    # The build arg is the digest line alone, ending the docker command line.
                    self.assertIn(f"--build-arg CHEZMOI_VERSION=2.73.0 --build-arg CHEZMOI_SHA256={digest}\n", log)
                    self.link("mktemp", "rm", "cp", "sha256sum", "shasum", "basename")
                    verified_sha = self.run_helper(
                        "github_release_verified_sha256 twpayne/chezmoi v2.73.0 "
                        f"{archive} chezmoi_2.73.0_checksums.txt",
                        TMPDIR=str(self.temp_dir),
                    )
                    self.assertEqual(0, verified_sha.returncode, verified_sha.stderr)
                    self.assertRegex(verified_sha.stdout, r"\A[0-9a-f]{64}\n\Z")
                    self.assertEqual(f"{digest}\n", verified_sha.stdout)
                    continue
                self.assertNotEqual(0, result.returncode)
                self.assertNotIn("docker build", log)
                if case == "gh not ready":
                    self.assertIn("run make gh-auth, then make docker", result.stderr)
                    self.assertNotIn(f"/{archive}", log)
                else:
                    self.assertIn("failed its checksum or release attestation; nothing was built", result.stderr)
        # The downloads lived in a private directory that is gone afterwards.
        self.assertEqual([], list(self.temp_dir.glob("github-release.*")))

    def mise_bootstrap(
        self,
        *,
        gpg: str | None,
        gh: str | None = None,
        reviewed: bool = False,
        key_fail: bool = False,
        installed: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run _install_mise_binary against a fake jdx/mise release.

        gpg is None (gpg and gpgv absent), "good", "bad signature", "wrong fingerprint", "expired" or "two keys";
        gh is None (absent), "verifies" or "fails". The fallback pin is the fixture release; reviewed makes its
        reviewed sha256 the fixture archive's, otherwise the manifest's real one stays (a mismatch). key_fail makes
        the release key's download fail; installed puts a mise reporting that version at the install path.
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
        key_step = "exit 22" if key_fail else "printf 'armored key\\n' > \"$out\""
        self.executable(
            "curl",
            f"""
            printf 'curl %s\\n' "$*" >> "{self.log}"
            out=""; url=""
            while [ "$#" -gt 0 ]; do case "$1" in -o) out="$2"; shift ;; https://*) url="$1" ;; esac; shift; done
            case "$url" in
                https://api.github.com/*) cat "{page}" ;;
                https://keys.openpgp.org/*) {key_step} ;;
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
        if installed is not None:
            mise = home / ".local/bin/mise"
            mise.parent.mkdir(parents=True, exist_ok=True)
            mise.write_text(f"#!/bin/sh\nprintf '{installed} macos-arm64 (2026-10-01)\\n'\n")
            mise.chmod(0o755)
        override = 'MISE_FALLBACK_VERSION="v2026.10.3"'
        if reviewed:
            override += f'; MISE_FALLBACK_LINUX_X64_SHA256="{digest}"'
        return subprocess.run(
            [
                "/bin/bash",
                "-c",
                f'source "$1"; {override}; _install_mise_binary',
                "_",
                str(ROOT / "install/common/mise.sh"),
            ],
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

    def test_mise_bootstrap_without_gh_or_gpg_installs_the_reviewed_fallback(self) -> None:
        # Nothing runs before an independent check: no gpg and no gh means the reviewed release, no lookup.
        result = self.mise_bootstrap(gpg=None, reviewed=True)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.temp_dir / "home/.local/bin/mise").exists())
        self.assertIn("installing the reviewed mise v2026.10.3 (assets.mise.fallback)", result.stdout)
        log = self.log.read_text()
        self.assertNotIn("api.github.com", log)
        # SHASUMS256.txt is still checked, as the second check.
        self.assertIn("/v2026.10.3/SHASUMS256.txt", log)
        self.assertNotIn("SHASUMS256.asc", log)

    def test_mise_bootstrap_refuses_a_fallback_archive_that_does_not_match_its_reviewed_sha256(self) -> None:
        # The fixture archive matches its own SHASUMS256.txt but not the manifest's reviewed sha256.
        result = self.mise_bootstrap(gpg=None)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("mise v2026.10.3 does not match its reviewed sha256; nothing was installed.", result.stderr)
        self.assertFalse((self.temp_dir / "home/.local/bin/mise").exists())

    def test_mise_bootstrap_keeps_a_newer_installed_mise_on_the_fallback_path(self) -> None:
        # mise self-update moved it past the fallback; a rerun of the bootstrap must not downgrade it.
        result = self.mise_bootstrap(gpg=None, installed="2026.11.0")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("mise 2026.11.0 stays: it is at or past the reviewed fallback v2026.10.3.", result.stdout)
        self.assertFalse(self.log.exists())
        self.assertIn("2026.11.0", (self.temp_dir / "home/.local/bin/mise").read_text())
        self.tearDown()
        self.setUp()

        # An older one is replaced by the reviewed fallback.
        result = self.mise_bootstrap(gpg=None, installed="2026.9.1", reviewed=True)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("installing the reviewed mise v2026.10.3", result.stdout)
        self.assertNotIn("2026.9.1", (self.temp_dir / "home/.local/bin/mise").read_text())

    def test_mise_bootstrap_verifies_by_attestation_only_when_the_gpg_inputs_cannot_be_fetched(self) -> None:
        # keys.openpgp.org is down: an authenticated gh's attestation verifies instead.
        result = self.mise_bootstrap(gpg="good", key_fail=True, gh="verifies")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("the release attestation verifies mise v2026.10.3 instead", result.stderr)
        log = self.log.read_text()
        self.assertIn("/v2026.10.3/SHASUMS256.txt", log)
        self.assertIn(f"/{MISE_ARTIFACT} --repo github.com/jdx/mise", log)
        self.tearDown()
        self.setUp()

        # Without gh nothing can verify it, so nothing installs.
        result = self.mise_bootstrap(gpg="good", key_fail=True)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Could not fetch the mise release key or SHASUMS256.asc", result.stderr)
        self.assertFalse((self.temp_dir / "home/.local/bin/mise").exists())
        self.tearDown()
        self.setUp()

        # A bad signature is a failed check, not a missing input: the attestation does not replace it.
        result = self.mise_bootstrap(gpg="bad signature", gh="verifies")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("GPG signature check failed", result.stderr)
        self.assertFalse((self.temp_dir / "home/.local/bin/mise").exists())

    def test_mise_bootstrap_with_gpg_takes_the_newest_release_verified_by_its_signature(self) -> None:
        result = self.mise_bootstrap(gpg="good")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.temp_dir / "home/.local/bin/mise").exists())
        log = self.log.read_text()
        self.assertIn("api.github.com/repos/jdx/mise/releases", log)
        self.assertIn(f"https://keys.openpgp.org/vks/v1/by-fingerprint/{MISE_FINGERPRINT}", log)
        self.assertIn("/v2026.10.3/SHASUMS256.asc", log)
        self.assertIn("gpgv --keyring ", log)
        # The checksums come from the signed text, never from the unsigned SHASUMS256.txt.
        self.assertNotIn("SHASUMS256.txt", log)
        self.assertNotIn("reviewed", result.stdout)

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
                if gpg != "bad signature":
                    self.assertNotIn("gpgv ", self.log.read_text())

    def test_mise_bootstrap_with_gh_takes_the_newest_release_verified_by_its_attestation(self) -> None:
        result = self.mise_bootstrap(gpg=None, gh="verifies")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.temp_dir / "home/.local/bin/mise").exists())
        self.assertIn("api.github.com/repos/jdx/mise/releases", self.log.read_text())
        self.assertIn(f"/{MISE_ARTIFACT} --repo github.com/jdx/mise", self.log.read_text())
        self.tearDown()
        self.setUp()

        result = self.mise_bootstrap(gpg=None, gh="fails")

        self.assertNotEqual(0, result.returncode)
        self.assertIn(f"GitHub release attestation failed for {MISE_ARTIFACT}; nothing was installed.", result.stderr)
        self.assertFalse((self.temp_dir / "home/.local/bin/mise").exists())

    def chezmoi_bootstrap(self, *, gh: bool, reviewed: bool) -> tuple[subprocess.CompletedProcess[str], Path]:
        """Run setup.sh's run_chezmoi against a fake twpayne/chezmoi with releases v9.9.9 (rolling) and v8.8.8 (the fallback)."""
        home = self.temp_dir / "home"
        assets = self.temp_dir / "release"
        payload = self.temp_dir / "payload"
        for path in (home, assets, payload, self.temp_dir / "tmp"):
            path.mkdir(exist_ok=True)
        (payload / "chezmoi").write_text(
            f'#!/bin/sh\nprintf "chezmoi %s\\n" "$*" >> "{self.log}.chezmoi"\n'
            '[ "$1" = source-path ] && { mkdir -p "$HOME/source"; printf "%s\\n" "$HOME/source"; }\nexit 0\n'
        )
        (payload / "chezmoi").chmod(0o755)
        digest = ""
        for version in ("9.9.9", "8.8.8"):
            archive = assets / f"chezmoi_{version}_linux_amd64.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(payload / "chezmoi", arcname="chezmoi")
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            (assets / f"chezmoi_{version}_checksums.txt").write_text(f"{digest}  {archive.name}\n")
        (assets / "releases?per_page=30").write_text(json.dumps([release("v9.9.9", hours_ago(100))], indent=2) + "\n")
        self.executable(
            "curl",
            f"""
            out=""; url=""
            while [ "$#" -gt 0 ]; do case "$1" in -o) out="$2"; shift ;; https://*) url="$1" ;; esac; shift; done
            printf 'curl %s\\n' "$url" >> "{self.log}"
            [ -e "{assets}/${{url##*/}}" ] || exit 22
            if [ -n "$out" ]; then cp "{assets}/${{url##*/}}" "$out"; else cat "{assets}/${{url##*/}}"; fi
            """,
        )
        self.executable("uname", '[ "$1" = -m ] && printf "x86_64\\n" || printf "Linux\\n"\n')
        real_mktemp = shutil.which("mktemp")
        # macOS mktemp -d ignores TMPDIR; keep every temporary file under the test directory, as on Linux.
        self.executable(
            "mktemp",
            f'if [ "$*" = -d ]; then exec "{real_mktemp}" -d "$TMPDIR/tmp.XXXXXX"; fi\nexec "{real_mktemp}" "$@"\n',
        )
        gh_body = (
            (
                f'printf "gh %s\\n" "$*" >> "{self.log}"\n'
                '[ "$1" = --version ] && { printf "gh version 2.93.0 (2026-10-01)\\n"; exit 0; }\n'
                '[ "$*" = "auth status --hostname github.com" ] && exit 0\n'
                '[ "$1 $2" = "release verify-asset" ] && { printf "✓ Verification succeeded!\\n"; exit 0; }\n'
                "exit 1\n"
            )
            if gh
            else "exit 1\n"
        )
        self.executable("gh", gh_body)
        override = 'CHEZMOI_FALLBACK_VERSION="v8.8.8"'
        if reviewed:
            override += f'; CHEZMOI_FALLBACK_LINUX_AMD64_SHA256="{digest}"'
        result = subprocess.run(
            ["/bin/bash", "-c", f'source "$1"; {override}; run_chezmoi', "_", str(ROOT / "setup.sh")],
            env={
                "PATH": f"{self.bin_dir}:/usr/bin:/bin",
                "HOME": str(home),
                "TMPDIR": str(self.temp_dir / "tmp"),
                # setup.sh applies in CI only under RUNNER_TEMP.
                "CI": "true",
                "RUNNER_TEMP": str(self.temp_dir),
            },
            text=True,
            capture_output=True,
            check=False,
        )
        return result, Path(f"{self.log}.chezmoi")

    def test_setup_sh_bootstraps_the_reviewed_chezmoi_without_gh(self) -> None:
        result, ran = self.chezmoi_bootstrap(gh=False, reviewed=True)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("installing the reviewed chezmoi v8.8.8 (assets.chezmoi-bootstrap.fallback)", result.stdout)
        log = self.log.read_text()
        self.assertNotIn("api.github.com", log)
        self.assertIn("/v8.8.8/chezmoi_8.8.8_linux_amd64.tar.gz", log)
        self.assertIn("/v8.8.8/chezmoi_8.8.8_checksums.txt", log)
        self.assertIn("chezmoi init", ran.read_text())

    def test_setup_sh_runs_no_chezmoi_whose_archive_misses_its_reviewed_sha256(self) -> None:
        # The archive matches the release's own checksums file, not the manifest's reviewed sha256.
        result, ran = self.chezmoi_bootstrap(gh=False, reviewed=False)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Checksum mismatch", result.stderr)
        self.assertFalse(ran.exists())

    def test_setup_sh_takes_the_newest_chezmoi_when_gh_verifies_it_first(self) -> None:
        result, ran = self.chezmoi_bootstrap(gh=True, reviewed=False)

        self.assertEqual(0, result.returncode, result.stderr)
        log = self.log.read_text()
        self.assertIn("api.github.com/repos/twpayne/chezmoi/releases", log)
        self.assertIn("gh release verify-asset v9.9.9 ", log)
        self.assertNotIn("v8.8.8", log)
        self.assertIn("chezmoi init", ran.read_text())

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
