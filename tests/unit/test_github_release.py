#!/usr/bin/env python3
"""Verify scripts/lib/github-release.sh: the 72-hour release window, its fetch paths, and gh attestation checks."""

from __future__ import annotations

import datetime
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/lib/github-release.sh"


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


if __name__ == "__main__":
    unittest.main()
