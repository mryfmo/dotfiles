"""Verify scripts/lib/chezmoi-externals.sh: the bootstrap's and make update's retried, verified fetch of chezmoi's
archive externals into its cache, against a local server that truncates, fails or serves wrong bytes (U96)."""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "scripts/lib/chezmoi-externals.sh"
SERVER = ROOT / "tests/fixtures/chezmoi-externals/server.py"
CHEZMOI = shutil.which("chezmoi")


def archive() -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        data = os.urandom(200_000)  # incompressible, so a truncation cuts the archive itself
        member = tarfile.TarInfo("top/blob")
        member.size = len(data)
        tar.addfile(member, io.BytesIO(data))
    return buffer.getvalue()


class ServerFixture(unittest.TestCase):
    """One local server per class; each test starts with an empty request log and its own cache."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = Path(tempfile.mkdtemp(prefix="chezmoi-externals-test-"))
        cls.www = cls.temp / "www"
        cls.www.mkdir()
        cls.data = archive()
        cls.sha256 = hashlib.sha256(cls.data).hexdigest()
        cls.plan = cls.temp / "plan.json"
        cls.plan.write_text("{}")
        port_file = cls.temp / "port"
        cls.server = subprocess.Popen([sys.executable, str(SERVER), str(cls.www), str(cls.plan), str(port_file)])
        deadline = time.monotonic() + 30
        while not (port_file.exists() and port_file.read_text()):
            if time.monotonic() > deadline:
                raise RuntimeError("the fixture server did not start")
            time.sleep(0.05)
        cls.base = f"http://127.0.0.1:{port_file.read_text()}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.terminate()
        cls.server.wait(timeout=30)
        shutil.rmtree(cls.temp)

    def setUp(self) -> None:
        self.case = Path(tempfile.mkdtemp(prefix="case-", dir=self.temp))
        self.cache = self.case / "cache"
        self.log = self.www / "requests.log"
        self.log.unlink(missing_ok=True)

    def serve(self, name: str, *behaviours: str) -> str:
        (self.www / name).write_bytes(self.data)
        self.plan.write_text(json.dumps({f"/{name}": list(behaviours)}))
        return f"{self.base}/{name}"

    def requests(self) -> int:
        return len(self.log.read_text().splitlines()) if self.log.exists() else 0

    def entry(self, url: str) -> Path:
        # chezmoi's cache key: the sha256 of the URL as written (chezmoi 2.73.3 sourcestate.go:1921-1923).
        return self.cache / "external" / hashlib.sha256(url.encode()).hexdigest()

    def bash(self, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        env = {
            **os.environ,
            "HOME": str(self.case),
            "TMPDIR": str(self.case),
            "CHEZMOI_EXTERNAL_RETRY_DELAY": "0",
        }
        return subprocess.run(
            ["bash", "-c", f'source "$1"; shift; {script}', "_", str(LIB), *args],
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )

    def prefetch_one(self, url: str, seconds: str = "0", sha256: str | None = None) -> subprocess.CompletedProcess[str]:
        return self.bash('prefetch_chezmoi_external .ext "$@"', url, sha256 or self.sha256, seconds, str(self.cache))


class ChezmoiExternalsTest(ServerFixture):
    def test_a_truncated_transfer_is_retried_and_the_verified_archive_cached(self) -> None:
        url = self.serve("retry.tar.gz", "truncate", "ok")

        result = self.prefetch_one(url)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(2, self.requests())
        self.assertIn(f".ext: {url}: attempt 1 failed (curl exit 18", result.stderr)
        self.assertEqual(self.data, self.entry(url).read_bytes())
        self.assertEqual(0o600, self.entry(url).stat().st_mode & 0o777)

    def test_a_transfer_that_keeps_failing_names_the_external_and_caches_nothing(self) -> None:
        url = self.serve("dropped.tar.gz", "truncate")

        result = self.prefetch_one(url)

        self.assertEqual(1, result.returncode)
        self.assertEqual(4, self.requests())  # CHEZMOI_EXTERNAL_ATTEMPTS
        self.assertIn(f"chezmoi external .ext: {url}: download failed after 4 attempt(s)", result.stderr)
        self.assertEqual([], list((self.cache / "external").iterdir()))

    def test_a_server_error_is_retried_and_a_missing_file_is_not(self) -> None:
        url = self.serve("busy.tar.gz", "503", "ok")
        self.assertEqual(0, self.prefetch_one(url).returncode)
        self.assertEqual(2, self.requests())

        self.log.unlink()
        missing = f"{self.base}/absent.tar.gz"
        result = self.prefetch_one(missing)
        self.assertEqual(1, result.returncode)
        self.assertEqual(1, self.requests())
        self.assertIn(f"{missing}: download failed after 1 attempt(s) (last: curl exit 22, HTTP 404)", result.stderr)

    def test_a_checksum_mismatch_after_a_complete_download_fails_at_once(self) -> None:
        url = self.serve("wrong.tar.gz", "corrupt", "ok")

        result = self.prefetch_one(url)

        self.assertEqual(2, result.returncode)
        self.assertEqual(1, self.requests())
        self.assertIn(f".ext: {url}: SHA256 mismatch after a complete download", result.stderr)
        self.assertIn("not retried, nothing cached", result.stderr)
        self.assertEqual([], list((self.cache / "external").iterdir()))

    def test_a_fresh_verified_entry_is_kept_and_any_other_is_fetched_again(self) -> None:
        url = self.serve("cached.tar.gz", "ok")
        entry = self.entry(url)
        entry.parent.mkdir(parents=True)
        entry.write_bytes(self.data)
        self.assertEqual(0, self.prefetch_one(url, "2592000").returncode)
        self.assertEqual(0, self.requests())

        # chezmoi caches a download before it checks it, so a wrong entry within the period is replaced.
        entry.write_bytes(b"not the archive")
        self.assertEqual(0, self.prefetch_one(url, "2592000").returncode)
        self.assertEqual(1, self.requests())
        self.assertEqual(self.data, entry.read_bytes())

        # An entry older than the refresh period is what chezmoi would download again.
        old = time.time() - 3 * 3600
        os.utime(entry, (old, old))
        self.assertEqual(0, self.prefetch_one(url, "7200").returncode)
        self.assertEqual(2, self.requests())
        self.assertEqual(0, self.prefetch_one(url, "14400").returncode)
        self.assertEqual(2, self.requests())

    def test_the_refresh_period_is_read_as_go_writes_it(self) -> None:
        for text, seconds in (("", 0), ("0", 0), ("720h", 2592000), ("1h30m", 5400), ("90s", 90)):
            with self.subTest(text=text):
                self.assertEqual(f"{seconds}\n", self.bash('chezmoi_external_seconds "$1"', text).stdout)
        for text in ("1.5h", "300ms", "1d", "h"):
            with self.subTest(text=text):
                self.assertEqual(1, self.bash('chezmoi_external_seconds "$1"', text).returncode)


@unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
class ChezmoiSourceExternalsTest(ServerFixture):
    """The whole step against a chezmoi source: chezmoi renders and lists the externals, and the status that follows
    reads only the cache."""

    def source(self, url: str, sha256: str | None = None, *, extra: str = "") -> Path:
        source = self.case / "source"
        (source / ".chezmoitemplates").mkdir(parents=True)
        checksum = sha256 or self.sha256
        (source / ".chezmoitemplates/ext.yaml.tmpl").write_text(
            f'".ext":\n  type: archive\n  url: {json.dumps(url)}\n  checksum:\n    sha256: "{checksum}"\n'
            '  stripComponents: 1\n  refreshPeriod: "720h"\n'
        )
        # As the repository's own: the root file includes a named template.
        (source / ".chezmoiexternal.yaml.tmpl").write_text('{{ template "ext.yaml.tmpl" . }}' + extra)
        (source / "dot_plain").write_text("plain\n")
        (self.case / "chezmoi.yaml").write_text("")
        wrapper = self.case / "chezmoi"
        wrapper.write_text(
            f'#!/bin/sh\nexec "{CHEZMOI}" --source "{source}" --destination "{self.case}/home" '
            f'--cache "{self.cache}" --config "{self.case}/chezmoi.yaml" "$@"\n'
        )
        wrapper.chmod(0o755)
        return wrapper

    def test_status_reads_the_prefetched_cache_after_a_truncated_transfer(self) -> None:
        url = self.serve("status.tar.gz", "truncate", "ok")
        chezmoi = self.source(url)

        result = self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi))
        status = subprocess.run([str(chezmoi), "status"], capture_output=True, text=True, timeout=120, check=False)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn(f"chezmoi external .ext: downloaded from {url}, sha256 verified", result.stdout)
        self.assertEqual(0, status.returncode, status.stderr)
        self.assertIn("A .ext/blob", status.stdout)
        # The truncated attempt and its retry; chezmoi's own read fetched nothing.
        self.assertEqual(2, self.requests())

    def test_an_external_that_keeps_failing_stops_the_step_naming_it(self) -> None:
        url = self.serve("down.tar.gz", "truncate")
        chezmoi = self.source(url)

        result = self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi))

        self.assertEqual(1, result.returncode)
        self.assertIn(f"chezmoi external .ext: {url}: download failed after 4 attempt(s)", result.stderr)

    def test_an_external_without_a_sha256_is_refused(self) -> None:
        url = self.serve("unverified.tar.gz", "ok")
        chezmoi = self.source(url)
        tmpl = self.case / "source/.chezmoitemplates/ext.yaml.tmpl"
        tmpl.write_text(tmpl.read_text().replace(f'  checksum:\n    sha256: "{self.sha256}"\n', ""))

        result = self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi))

        self.assertEqual(1, result.returncode)
        self.assertIn("has no sha256 checksum", result.stderr)
        self.assertEqual(0, self.requests())

    def test_externals_chezmoi_fetches_itself_are_left_to_it(self) -> None:
        # git-repo and file:// externals never reach chezmoi's download cache.
        url = self.serve("only.tar.gz", "ok")
        chezmoi = self.source(
            url,
            extra='\n".repo":\n  type: git-repo\n  url: "https://invalid.example/repo.git"\n'
            f'".local":\n  type: file\n  url: "file://{self.case}/local"\n',
        )

        result = self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi))

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(1, self.requests())
        self.assertNotIn(".repo", result.stdout + result.stderr)


class ChezmoiExternalsWiringTest(unittest.TestCase):
    def test_setup_sh_carries_an_exact_copy_of_the_helper(self) -> None:
        # setup.sh runs before the repository exists, so it cannot source the helper.
        helper = LIB.read_text()
        body = helper[helper.index("# Download attempts per URL") :]
        setup = (ROOT / "setup.sh").read_text()
        begin = "# --- chezmoi-externals.sh begin ---\n"
        self.assertEqual(
            body, setup[setup.index(begin) + len(begin) : setup.index("# --- chezmoi-externals.sh end ---\n")]
        )

    def test_the_bootstrap_and_make_update_prefetch_before_chezmoi_reads_the_target_state(self) -> None:
        setup = (ROOT / "setup.sh").read_text()
        run = setup[setup.index("function run_chezmoi()") :]
        prefetch = run.index('prefetch_chezmoi_externals "${chezmoi_cmd}"')
        for read in ('"${chezmoi_cmd}" status', '"${chezmoi_cmd}" diff', '"${chezmoi_cmd}" apply'):
            self.assertLess(prefetch, run.index(read), read)
        makefile = (ROOT / "Makefile").read_text()
        tree = makefile[makefile.index("\nupdate-tree:\n") :]
        self.assertLess(
            tree.index("source scripts/lib/chezmoi-externals.sh && prefetch_chezmoi_externals chezmoi"),
            tree.index("chezmoi apply --verbose"),
        )


if __name__ == "__main__":
    unittest.main()
