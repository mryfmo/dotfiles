"""Verify scripts/lib/chezmoi-externals.sh: the bootstrap's and make update's retried, verified fetch of chezmoi's
archive externals into its cache, against a local server that truncates, fails or serves wrong bytes (U96), and the
check that follows it, which proves chezmoi reads that cache with the network denied (U111)."""

from __future__ import annotations

import faulthandler
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


# The library's own sha256 helper, kept as orig_chezmoi_external_sha256 so an injected one can delegate to it.
KEEP_HASH = 'eval "orig_$(declare -f chezmoi_external_sha256)"; '
# Local producers of prefetch_chezmoi_external made to fail, as shell definitions run after the library is sourced:
# (name, definitions, exit code of the function, its message, requests made before the failure). mktemp fails only for
# the download file, so a whole-step run still gets its scratch directory (mktemp -d).
PRODUCER_CASES = (
    (
        "the URL hash fails",
        KEEP_HASH + 'chezmoi_external_sha256() { case "${1:-}" in *chezmoi-external-url.*) return 1 ;; esac; '
        'orig_chezmoi_external_sha256 "$@"; }; ',
        1,
        "cannot hash the URL",
        0,
    ),
    # Audit of ef512c88: under make update (no pipefail) a failed write of the URL into the hash was masked, and the
    # key became the sha256 of nothing. The write fails here: printf of exactly the URL, the bytes the key is made of.
    (
        "the URL cannot be written for its hash",
        (
            'printf() { if [ "$#" -eq 2 ] && [ "$1" = %s ] && [[ "$2" == http://127.0.0.1:* ]]; then return 1; fi; '
            'builtin printf "$@"; }; '
        ),
        1,
        "cannot hash the URL",
        0,
    ),
    (
        "the URL scratch file cannot be made",
        'mktemp() { case "${1:-}" in *chezmoi-external-url.*) return 1 ;; esac; command mktemp "$@"; }; ',
        1,
        "cannot hash the URL",
        0,
    ),
    (
        "the URL hashes to the key of no bytes",
        KEEP_HASH + 'chezmoi_external_sha256() { case "${1:-}" in *chezmoi-external-url.*) '
        'builtin printf "%s\\n" "$CHEZMOI_EXTERNAL_EMPTY_SHA256"; return 0 ;; esac; orig_chezmoi_external_sha256 "$@"; }; ',
        1,
        "cannot hash the URL",
        0,
    ),
    (
        "the hash tool prints a non-digest",
        'sha256sum() { printf "zz  -\\n"; }; shasum() { printf "zz  -\\n"; }; ',
        1,
        "cannot hash the URL",
        0,
    ),
    (
        "the download hash fails",
        KEEP_HASH + 'chezmoi_external_sha256() { case "${1:-}" in *.prefetch.*) return 1 ;; esac; '
        'orig_chezmoi_external_sha256 "$@"; }; ',
        1,
        "cannot hash the download; nothing cached",
        1,
    ),
    (
        "the download hash is no digest",
        KEEP_HASH + 'chezmoi_external_sha256() { case "${1:-}" in *.prefetch.*) printf "zz\\n"; return 0 ;; esac; '
        'orig_chezmoi_external_sha256 "$@"; }; ',
        2,
        "SHA256 mismatch after a complete download: expected",
        1,
    ),
    (
        "mktemp fails",
        'mktemp() { case "${1:-}" in *.prefetch.*) return 1 ;; esac; command mktemp "$@"; }; ',
        1,
        "cannot create a download file in",
        0,
    ),
    ("mkdir fails", "mkdir() { return 1; }; ", 1, "mkdir -p", 0),
    ("chmod 700 fails", 'chmod() { [ "$1" != 700 ] || return 1; command chmod "$@"; }; ', 1, "chmod 700 on", 0),
    (
        "chmod 600 fails",
        'chmod() { [ "$1" != 600 ] || return 1; command chmod "$@"; }; ',
        1,
        "chmod 600 on the download failed; nothing cached",
        1,
    ),
    ("mv fails", "mv() { return 1; }; ", 1, "mv of the download into", 1),
)
# The two ways the library runs: setup.sh's own options, and make update's `bash -c 'source …'` with bash's defaults
# (no pipefail, no errexit). Every producer table runs both ways, so a check that leans on the caller's options fails.
SHELL_MODES = (("setup.sh: set -Eeuo pipefail", "set -Eeuo pipefail; "), ("make update: bash defaults", ""))


def both_ways(cases):
    """Each case once per SHELL_MODES entry: its name gains the mode, its shell definitions the mode's options."""
    for label, options in SHELL_MODES:
        for case in cases:
            yield (f"{case[0]} [{label}]", options + case[1], *case[2:])


# Producers of a fresh existing entry's age and digest: (name, definitions, whether the entry is fetched again).
# A failed or garbled date is fatal; a failed stat or entry hash makes the entry stale, so it is fetched again.
AGE_CASES = (
    ("date fails", "date() { return 1; }; ", False),
    ("date prints garbage", "date() { printf 'soon\\n'; }; ", False),
    ("stat fails", "stat() { return 1; }; ", True),
    ("stat prints garbage", "stat() { printf 'yesterday\\n'; }; ", True),
    (
        "the entry hash fails",
        KEEP_HASH + 'chezmoi_external_sha256() { [ "${1:-}" != "$ENTRY" ] || return 1; '
        'orig_chezmoi_external_sha256 "$@"; }; ',
        True,
    ),
)

# The chezmoi stub for the cache check: it records every call with the guard's mark, answers --version, and for
# anything else prints STUB_OUTPUT and exits STUB_EXIT.
STUB_CHEZMOI = """#!/bin/sh
printf '%s|%s\\n' "${GUARDED:-}" "$*" >> "$CALLS"
if [ "$1" = --version ]; then
    [ -z "${FAIL_VERSION:-}" ] || exit 7
    printf 'chezmoi version v9.9.9-stub\\n'
    exit 0
fi
printf '%s' "$STUB_OUTPUT"
exit "$STUB_EXIT"
"""
# What the stub prints and exits, and what the check must conclude: (name, output, exit, passes, reason fragment).
# The listed strings fail the check whatever the exit status; another failure is reported by chezmoi's last line.
VERDICT_CASES = (
    ("exits 0 and prints nothing", "", 0, True, ""),
    ("exits 0 with status lines", " A .ext\n A .ext/blob\n", 0, True, ""),
    ("prints unexpected EOF and exits 1", "chezmoi: unexpected EOF\n", 1, False, "chezmoi: unexpected EOF"),
    *(
        (f"exits 0 but prints {text}", f" A .ext\nchezmoi: {text} x\n", 0, False, f"chezmoi: {text} x")
        for text in ("unexpected EOF", "dial tcp", 'Get "http', "no such host")
    ),
    ("exits 1 with another message", "chezmoi: config: parse error\n", 1, False, "chezmoi: config: parse error"),
    ("exits 1 and prints nothing", "", 1, False, "no output"),
)
# Producers of the cache check made to fail: (name, shell definitions, environment, the reason).
CHECK_PRODUCER_CASES = (
    ("chezmoi --version fails", "", {"FAIL_VERSION": "1"}, "cannot read chezmoi's version"),
    ("the output file cannot be made", "mktemp() { return 1; }; ", {}, "cannot create a file for chezmoi's output"),
    ("the scan fails", "grep() { return 2; }; ", {}, "cannot scan chezmoi's output"),
    (
        "the last line cannot be read",
        "tail() { return 1; }; ",
        {"STUB_OUTPUT": "chezmoi: config: parse error\n", "STUB_EXIT": "1"},
        "cannot read chezmoi's output",
    ),
)


# Every wait in this module is bounded, so a hang fails the test that hit it instead of the CI job (U96: the macos-15
# job was cancelled at its 30-minute limit). Each subprocess call has its own timeout; the whole module has one more.
COMMAND_SECONDS = 60
SERVER_START_SECONDS = 30
MODULE_SECONDS = 900


def setUpModule() -> None:
    # Past MODULE_SECONDS the module prints every thread's stack, the running test included, and exits.
    faulthandler.dump_traceback_later(MODULE_SECONDS, exit=True)


def tearDownModule() -> None:
    faulthandler.cancel_dump_traceback_later()


class ServerFixture(unittest.TestCase):
    """One local server per class; each test starts with an empty request log and its own cache."""

    @classmethod
    def setUpClass(cls) -> None:
        # Physical, as the step reports paths (macOS's TMPDIR sits behind the /var symlink).
        cls.temp = Path(tempfile.mkdtemp(prefix="chezmoi-externals-test-")).resolve()
        cls.addClassCleanup(shutil.rmtree, cls.temp, True)
        cls.www = cls.temp / "www"
        cls.www.mkdir()
        cls.data = archive()
        cls.sha256 = hashlib.sha256(cls.data).hexdigest()
        cls.plan = cls.temp / "plan.json"
        cls.log = cls.temp / "requests.log"
        cls.plan.write_text(json.dumps({"log": str(cls.log), "paths": {}}))
        port_file = cls.temp / "port"
        server_log = cls.temp / "server.log"
        # The server never holds the test's stdout or stderr: unittest-shards reads those pipes to EOF, so a server
        # left running on them blocked the shard for good. Its output goes to a file in the class's directory.
        with server_log.open("wb") as log:
            cls.server = subprocess.Popen(
                [sys.executable, str(SERVER), str(cls.plan), str(port_file)],
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
        # A class cleanup runs even when setUpClass fails below, unlike tearDownClass, so the server always stops.
        cls.addClassCleanup(cls.stop_server)
        deadline = time.monotonic() + SERVER_START_SECONDS
        while not (port_file.exists() and port_file.read_text().isdigit()):
            if time.monotonic() > deadline or cls.server.poll() is not None:
                raise RuntimeError(
                    f"the fixture server did not start within {SERVER_START_SECONDS}s "
                    f"(exit {cls.server.poll()}): {server_log.read_text(errors='replace')}"
                )
            time.sleep(0.05)
        cls.base = f"http://127.0.0.1:{port_file.read_text()}"

    @classmethod
    def stop_server(cls) -> None:
        cls.server.terminate()
        try:
            cls.server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            cls.server.kill()
            cls.server.wait(timeout=10)

    def setUp(self) -> None:
        self.case = Path(tempfile.mkdtemp(prefix="case-", dir=self.temp))
        self.cache = self.case / "cache"
        self.sleeps = self.case / "sleeps"
        self.routes: dict[str, dict] = {}
        self.log.unlink(missing_ok=True)

    def serve(self, name: str, *behaviours: str) -> str:
        # Registers one URL path: the server answers the registered paths from their files and nothing else.
        (self.www / name).write_bytes(self.data)
        self.routes[f"/{name}"] = {"file": str(self.www / name), "plan": list(behaviours)}
        self.plan.write_text(json.dumps({"log": str(self.log), "paths": self.routes}))
        return f"{self.base}/{name}"

    def requests(self, url: str | None = None) -> int:
        lines = self.log.read_text().splitlines() if self.log.exists() else []
        return len(lines) if url is None else lines.count(url.removeprefix(self.base))

    def entry(self, url: str) -> Path:
        # chezmoi's cache key: the sha256 of the URL as written (chezmoi 2.73.3 sourcestate.go:1921-1923).
        return self.cache / "external" / hashlib.sha256(url.encode()).hexdigest()

    def bash(self, script: str, *args: str, **extra: str) -> subprocess.CompletedProcess[str]:
        # The waits between attempts are recorded instead of slept: the library's delays are constants.
        env = {**os.environ, "HOME": str(self.case), "TMPDIR": str(self.case), "SLEEPS": str(self.sleeps), **extra}
        wait = 'sleep() { printf "%s\\n" "$1" >> "$SLEEPS"; }; '
        return subprocess.run(
            ["bash", "-c", f'source "$1"; shift; {wait}{script}', "_", str(LIB), *args],
            env=env,
            capture_output=True,
            text=True,
            timeout=COMMAND_SECONDS,
            check=False,
        )

    def prefetch_one(
        self, url: str, seconds: str = "0", sha256: str | None = None, *, inject: str = ""
    ) -> subprocess.CompletedProcess[str]:
        # inject: shell definitions run after the library is sourced, replacing a producer the step calls.
        return self.bash(
            f'{inject}prefetch_chezmoi_external .ext "$@"', url, sha256 or self.sha256, seconds, str(self.cache)
        )

    def cached(self) -> list[str]:
        directory = self.cache / "external"
        return sorted(path.name for path in directory.iterdir()) if directory.exists() else []


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

    def test_the_retry_bound_and_backoff_are_constants_no_environment_changes(self) -> None:
        # Audit of f2c724a6: an attempt count read from the environment could be non-numeric and unbound the loop.
        url = self.serve("bounded.tar.gz", "truncate")
        for value in ("abc", "0", "-1", "999999999999", ""):
            with self.subTest(value=value):
                self.log.unlink(missing_ok=True)
                self.sleeps.unlink(missing_ok=True)
                result = self.bash(
                    'prefetch_chezmoi_external .ext "$@"',
                    url,
                    self.sha256,
                    "0",
                    str(self.cache),
                    CHEZMOI_EXTERNAL_ATTEMPTS=value,
                    CHEZMOI_EXTERNAL_RETRY_DELAY=value,
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(4, self.requests())
                self.assertEqual(["5", "10", "20"], self.sleeps.read_text().split())

    def test_the_url_key_is_the_sha256_of_its_bytes_and_never_of_nothing(self) -> None:
        url = f"{self.base}/key.tar.gz"
        for name, options, *_ in both_ways((("key", ""),)):
            with self.subTest(name):
                result = self.bash(options + 'chezmoi_external_url_key "$1"', url)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(hashlib.sha256(url.encode()).hexdigest() + "\n", result.stdout)
                empty = self.bash(options + 'chezmoi_external_url_key ""')
                self.assertEqual((1, ""), (empty.returncode, empty.stdout), empty.stderr)
                self.assertEqual([], sorted(self.case.glob("chezmoi-external-url.*")))

    def test_every_hash_time_temp_and_install_producer_that_fails_stops_closed(self) -> None:
        # Audit of 0f69d7af: each producer the cache decision rests on, made to fail. Each case names its producer,
        # leaves no cache entry and no partial download, and makes no request when the failure comes before one.
        url = self.serve("producers.tar.gz", "ok")
        for name, inject, code, message, requests in both_ways(PRODUCER_CASES):
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.cache, ignore_errors=True)

                result = self.prefetch_one(url, inject=inject)

                self.assertEqual(code, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertEqual(requests, self.requests())
                self.assertEqual([], self.cached())

    def test_an_existing_entry_whose_age_or_digest_cannot_be_read_is_never_kept(self) -> None:
        # The time producers: a date that fails or prints garbage stops the step; a stat or an entry hash that fails
        # makes the entry stale, so it is fetched again and replaced, never kept.
        url = self.serve("aged.tar.gz", "ok")
        entry = self.entry(url)
        for name, inject, refetched in both_ways(AGE_CASES):
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                entry.parent.mkdir(parents=True, exist_ok=True)
                entry.write_bytes(b"fresh but unread")

                result = self.bash(
                    inject + 'prefetch_chezmoi_external .ext "$@"',
                    url,
                    self.sha256,
                    "2592000",
                    str(self.cache),
                    ENTRY=str(entry),
                )

                self.assertEqual(0 if refetched else 1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(int(refetched), self.requests())
                if refetched:
                    self.assertEqual(self.data, entry.read_bytes())
                else:
                    self.assertIn("date +%s failed; cannot tell the cache entry's age", result.stderr)
                    self.assertEqual(b"fresh but unread", entry.read_bytes())
                self.assertEqual([entry.name], self.cached())

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

    def run_codes(self, status: str, http: str) -> subprocess.CompletedProcess[str]:
        # chezmoi_external_download replaced by one that fails with a fixed curl exit and HTTP code, counting calls.
        self.log.unlink(missing_ok=True)
        self.sleeps.unlink(missing_ok=True)
        inject = 'chezmoi_external_download() { printf "x\\n" >> "$CALLS"; printf "%s" "$HTTP"; return "$STATUS"; }; '
        return self.bash(
            inject + 'prefetch_chezmoi_external .ext "$@"',
            f"{self.base}/coded.tar.gz",
            self.sha256,
            "0",
            str(self.cache),
            CALLS=str(self.log),
            STATUS=status,
            HTTP=http,
        )

    def test_a_local_or_unlisted_curl_failure_is_fatal_without_a_retry(self) -> None:
        # Round 4: curl 23 (write error) and 27 (out of memory) are local; they and every code outside the allowlist
        # fail at once, naming the code. Mutant check: a retry on any non-zero exit fails this test.
        for status, http in (
            ("23", "200"),
            ("27", "200"),
            ("1", "000"),
            ("3", "000"),
            ("47", "301"),
            ("22", "404"),
            ("22", "403"),
        ):
            with self.subTest(status=status, http=http):
                result = self.run_codes(status, http)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(1, self.requests())
                self.assertFalse(self.sleeps.exists())
                self.assertIn(
                    f"download failed after 1 attempt(s) (last: curl exit {status}, HTTP {http})", result.stderr
                )
                self.assertEqual([], self.cached())

    def test_each_allowlisted_transient_failure_is_retried_up_to_the_bound(self) -> None:
        # curl(1) "Exit codes": 6, 7, 18, 28, 35, 52, 55, 56, 92; and through --fail's 22, HTTP 408, 429 and 5xx.
        for status, http in (
            *((code, "000") for code in ("6", "7", "18", "28", "35", "52", "55", "56", "92")),
            ("22", "408"),
            ("22", "429"),
            ("22", "500"),
            ("22", "503"),
            ("22", "599"),
        ):
            with self.subTest(status=status, http=http):
                result = self.run_codes(status, http)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(4, self.requests())
                self.assertEqual(["5", "10", "20"], self.sleeps.read_text().split())
                self.assertIn(
                    f"download failed after 4 attempt(s) (last: curl exit {status}, HTTP {http})", result.stderr
                )
                self.assertEqual([], self.cached())

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


class FixtureServerTest(ServerFixture):
    def test_the_server_answers_only_registered_paths(self) -> None:
        # Audit of f2c724a6: a `..` request path served the repository's Makefile. The server now looks the path up in
        # the registered mapping and never in the filesystem.
        url = self.serve("only.tar.gz", "ok")
        (self.www / "other.tar.gz").write_bytes(b"not registered")
        for path in (
            "/../../../Makefile",
            "/%2e%2e/%2e%2e/Makefile",
            "/other.tar.gz",
            "/only.tar.gz/../only.tar.gz",
            "/" + str(ROOT / "Makefile").lstrip("/"),
        ):
            with self.subTest(path=path):
                code = subprocess.run(
                    [
                        "curl",
                        "--silent",
                        "--path-as-is",
                        "--output",
                        "/dev/null",
                        "--write-out",
                        "%{http_code}",
                        self.base + path,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=COMMAND_SECONDS,
                    check=False,
                ).stdout
                self.assertEqual("404", code)
        fetched = subprocess.run(
            ["curl", "--silent", "--fail", url], capture_output=True, timeout=COMMAND_SECONDS, check=False
        )
        self.assertEqual(self.data, fetched.stdout)


@unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
class ChezmoiSourceExternalsTest(ServerFixture):
    """The whole step against a chezmoi source: chezmoi renders and lists the externals, and the status that follows
    reads only the cache."""

    def source(
        self, url: str, sha256: str | None = None, *, extra: str = "", urls: tuple[str, ...] = (), link: bool = False
    ) -> Path:
        # link: chezmoi is given a symlink to the source, which it keeps as its source path.
        source = self.case / "source"
        (source / ".chezmoitemplates").mkdir(parents=True)
        checksum = sha256 or self.sha256
        fallbacks = f"  urls: {json.dumps(list(urls))}\n" if urls else ""
        (source / ".chezmoitemplates/ext.yaml.tmpl").write_text(
            f'".ext":\n  type: archive\n  url: {json.dumps(url)}\n{fallbacks}  checksum:\n    sha256: "{checksum}"\n'
            '  stripComponents: 1\n  refreshPeriod: "720h"\n'
        )
        # As the repository's own: the root file includes a named template.
        (source / ".chezmoiexternal.yaml.tmpl").write_text('{{ template "ext.yaml.tmpl" . }}' + extra)
        (source / "dot_plain").write_text("plain\n")
        (self.case / "chezmoi.yaml").write_text("")
        wrapper = self.case / "chezmoi"
        # The real chezmoi, but each producer the step reads can be made to fail: FAIL_SOURCE_PATH, EMPTY_SOURCE_PATH,
        # FAIL_RENDER (the declaration on stdin), FAIL_DECODE and SHORT_DECODE (the listing template: fails, or exits
        # 0 with a line missing its fields) and FAIL_CACHE_DIR.
        given = source
        if link:
            given = self.case / "linked-source"
            given.symlink_to(source, target_is_directory=True)
        wrapper.write_text(
            "#!/bin/sh\n"
            'case "$1:$#:$2" in\n'
            '  source-path:*) [ -z "$FAIL_SOURCE_PATH" ] || exit 7; [ -z "$EMPTY_SOURCE_PATH" ] || exit 0 ;;\n'
            '  execute-template:1:) [ -z "$FAIL_RENDER" ] || exit 7 ;;\n'
            '  execute-template:2:*include*) [ -z "$FAIL_DECODE" ] || exit 7\n'
            '    [ -z "$SHORT_DECODE" ] || { printf "only-a-name\\n"; exit 0; } ;;\n'
            '  execute-template:2:*cacheDir*) [ -z "$FAIL_CACHE_DIR" ] || exit 7 ;;\n'
            "esac\n"
            f'exec "{CHEZMOI}" --source "{given}" --destination "{self.case}/home" '
            f'--cache "{self.cache}" --config "{self.case}/chezmoi.yaml" "$@"\n'
        )
        wrapper.chmod(0o755)
        return wrapper

    def test_status_reads_the_prefetched_cache_after_a_truncated_transfer(self) -> None:
        url = self.serve("status.tar.gz", "truncate", "ok")
        chezmoi = self.source(url)

        result = self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi))
        status = subprocess.run(
            [str(chezmoi), "status"], capture_output=True, text=True, timeout=COMMAND_SECONDS, check=False
        )

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

    def test_a_symlinked_source_root_is_discovered_and_prefetched(self) -> None:
        # U96 round 9: chezmoi keeps a symlinked source path, and find does not descend into a symlinked start, so
        # discovery listed nothing and the prefetch was skipped. The step reads the physical path.
        url = self.serve("linked.tar.gz", "ok")
        chezmoi = self.source(url, link=True)
        source_path = subprocess.run(
            [str(chezmoi), "source-path"], capture_output=True, text=True, timeout=COMMAND_SECONDS, check=True
        ).stdout.strip()
        self.assertEqual(str(self.case / "linked-source"), source_path)  # chezmoi keeps the symlink
        for name, options, *_ in both_ways((("symlinked root", ""),)):
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.cache, ignore_errors=True)
                result = self.bash(options + 'prefetch_chezmoi_externals "$1"', str(chezmoi))
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(f"chezmoi external .ext: downloaded from {url}, sha256 verified", result.stdout)
                self.assertEqual(1, self.requests(url))
                self.assertEqual(self.data, self.entry(url).read_bytes())

    def test_a_root_declaration_that_find_does_not_list_is_refused(self) -> None:
        # The root's declaration is a symlink to a file elsewhere: find's -type f does not list it, chezmoi would read
        # it. Discovery is empty while the root declares one, so the step stops instead of skipping the externals.
        url = self.serve("hidden.tar.gz", "ok")
        chezmoi = self.source(url)
        declaration = self.case / "source/.chezmoiexternal.yaml.tmpl"
        moved = self.case / "elsewhere.yaml.tmpl"
        declaration.rename(moved)
        declaration.symlink_to(moved)
        for name, options, *_ in both_ways((("symlinked declaration", ""),)):
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                result = self.bash(options + 'prefetch_chezmoi_externals "$1"', str(chezmoi))
                self.assert_refused(
                    result,
                    f"{self.case / 'source'} holds a .chezmoiexternal file or a .chezmoiexternals directory, "
                    "but find listed no declaration",
                )

    def assert_refused(self, result: subprocess.CompletedProcess[str], message: str) -> None:
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(message, result.stderr)
        self.assertNotIn("downloaded from", result.stdout)
        self.assertEqual(0, self.requests())
        self.assertFalse((self.cache / "external").exists())

    def test_every_discovery_producer_that_fails_stops_the_step_naming_it(self) -> None:
        # Audit of f2c724a6: discovery decides what is fetched and checked, so a producer that fails is an error,
        # never an empty list. Each producer's status is checked; nothing is fetched or cached after one fails.
        url = self.serve("discovery.tar.gz", "ok")
        chezmoi = self.source(url)
        declaration = self.case / "source/.chezmoiexternal.yaml.tmpl"
        cases = (
            ("chezmoi source-path fails", "", {"FAIL_SOURCE_PATH": "1"}, "chezmoi source-path failed"),
            ("chezmoi source-path prints nothing", "", {"EMPTY_SOURCE_PATH": "1"}, "named no directory"),
            ("find fails", "find() { return 1; }; ", {}, "cannot list the declarations under"),
            # U96 round 9: an empty listing is checked against the root with builtins, never taken as none.
            (
                "find lists nothing while the root declares externals",
                "find() { :; }; ",
                {},
                "holds a .chezmoiexternal file or a .chezmoiexternals directory, but find listed no declaration",
            ),
            (
                "the source cannot be resolved to its physical path",
                "cd() { return 1; }; ",
                {},
                "cannot resolve the source directory",
            ),
            # A find that lists some files and then fails (an unreadable directory) is a failure too.
            (
                "find fails after listing",
                'find() { command find "$@"; return 1; }; ',
                {},
                "cannot list the declarations",
            ),
            (
                "the scratch directory cannot be created",
                'mktemp() { [ "$1" != -d ] || return 1; command mktemp "$@"; }; ',
                {},
                "cannot create a scratch directory",
            ),
            ("the render fails", "", {"FAIL_RENDER": "1"}, f"cannot render {declaration}"),
            ("the decode fails", "", {"FAIL_DECODE": "1"}, f"cannot decode {declaration} as yaml"),
            (
                "the decode succeeds with a short line",
                "",
                {"SHORT_DECODE": "1"},
                "decoded without its fields: only-a-name",
            ),
            (
                "the cache directory cannot be read",
                "",
                {"FAIL_CACHE_DIR": "1"},
                "cannot read chezmoi's cache directory",
            ),
        )
        for name, prefix, env, message in both_ways(cases):
            with self.subTest(name):
                # Each case starts clean, so one case that fetched cannot fail the cases after it.
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.cache, ignore_errors=True)
                result = self.bash(f'{prefix}prefetch_chezmoi_externals "$1"', str(chezmoi), **env)
                self.assert_refused(result, message)

    def test_a_malformed_declaration_or_entry_is_refused(self) -> None:
        url = self.serve("malformed.tar.gz", "ok")
        chezmoi = self.source(url)
        source = self.case / "source"
        declaration = source / ".chezmoiexternal.yaml.tmpl"
        good = declaration.read_text()
        cases = (
            ("invalid YAML", '".ext": [unclosed\n', f"cannot decode {declaration} as yaml"),
            ("an entry that is not a mapping", '".ext": "an archive"\n', f"cannot decode {declaration} as yaml"),
            ("an unknown type", '".ext":\n  type: tarball\n  url: "https://x.invalid/a"\n', "unknown type tarball"),
            ("a missing type", '".ext":\n  url: "https://x.invalid/a"\n', "unknown type -"),
            ("no url", '".ext":\n  type: archive\n', "chezmoi external .ext: no url"),
        )
        for name, text, message in cases:
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                declaration.write_text(text)
                self.assert_refused(self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi)), message)
        declaration.write_text(good)
        unknown = source / ".chezmoiexternal.ini"
        unknown.write_text("")
        self.log.unlink(missing_ok=True)
        self.assert_refused(
            self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi)),
            f"{unknown} has a format this step does not read",
        )

    def test_an_external_with_urls_or_a_url_that_is_not_http_is_left_whole_to_chezmoi(self) -> None:
        # Round 4 (decisions.tsv treadmill-u96-fallback): no fallback hand-over. An external whose declaration lists
        # `urls`, or whose url is not http(s), is not prefetched at all: one line, no request, no cache entry.
        http = self.serve("whole.tar.gz", "ok")
        local = f"file://{self.case}/local.tar.gz"
        for name, url, urls, line in (
            ("http url, http urls", http, (http,), "left to chezmoi: its declaration lists fallback urls"),
            ("http url, file urls", http, (local,), "left to chezmoi: its declaration lists fallback urls"),
            ("file url, http urls", local, (http,), "left to chezmoi: its declaration lists fallback urls"),
            ("file url alone", local, (), f"left to chezmoi: {local} is not http(s)"),
            (
                "ftp url alone",
                "ftp://x.invalid/a.tar.gz",
                (),
                "left to chezmoi: ftp://x.invalid/a.tar.gz is not http(s)",
            ),
        ):
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.case / "source", ignore_errors=True)
                chezmoi = self.source(url, urls=urls)

                result = self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi))

                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual([f"chezmoi external .ext: {line}"], result.stdout.splitlines())
                self.assertEqual(0, self.requests())
                self.assertEqual([], self.cached())
        # Only `urls`, no `url`: chezmoi's own fallback list again, left whole.
        shutil.rmtree(self.case / "source")
        chezmoi = self.source(http, urls=(http,))
        tmpl = self.case / "source/.chezmoitemplates/ext.yaml.tmpl"
        tmpl.write_text(tmpl.read_text().replace(f"  url: {json.dumps(http)}\n", ""))
        result = self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            ["chezmoi external .ext: left to chezmoi: its declaration lists fallback urls"], result.stdout.splitlines()
        )
        self.assertEqual(0, self.requests())

    def test_a_producer_failure_stops_the_whole_step(self) -> None:
        # Every prefetch failure of a single-URL http(s) external is fatal; an unreadable entry age or digest refetches.
        url = self.serve("first.tar.gz", "ok")
        entry = self.entry(url)
        for name, inject, _code, message, requests in both_ways(PRODUCER_CASES):
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.cache, ignore_errors=True)
                shutil.rmtree(self.case / "source", ignore_errors=True)
                chezmoi = self.source(url)

                result = self.bash(inject + 'prefetch_chezmoi_externals "$1"', str(chezmoi))

                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertEqual(requests, self.requests())
                self.assertEqual([], self.cached())
        for name, inject, refetched in both_ways(AGE_CASES):
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.case / "source", ignore_errors=True)
                chezmoi = self.source(url)
                entry.parent.mkdir(parents=True, exist_ok=True)
                entry.write_bytes(b"fresh but unread")

                result = self.bash(inject + 'prefetch_chezmoi_externals "$1"', str(chezmoi), ENTRY=str(entry))

                self.assertEqual(0 if refetched else 1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(int(refetched), self.requests())
                self.assertEqual(self.data if refetched else b"fresh but unread", entry.read_bytes())

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

    def test_after_the_prefetch_chezmoi_reads_the_externals_from_its_cache_and_fetches_nothing(self) -> None:
        url = self.serve("cached.tar.gz", "ok")
        chezmoi = self.source(url)
        for name, options, *_ in both_ways((("cache check", ""),)):
            with self.subTest(name):
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.cache, ignore_errors=True)
                result = self.bash(
                    options + 'prefetch_chezmoi_externals "$1" && assert_chezmoi_externals_cached "$1"', str(chezmoi)
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("chezmoi externals: cache check ", result.stdout)
                self.assertIn(" with chezmoi version v", result.stdout)
                self.assertIn("chezmoi externals: chezmoi read the externals from its cache (", result.stdout)
                self.assertEqual(1, self.requests())  # the prefetch's download; chezmoi's read fetched nothing

    def test_a_cache_chezmoi_does_not_find_fails_the_check_naming_the_url(self) -> None:
        # The failure U111 closes: the prefetch wrote the entry, but chezmoi looks elsewhere (a release that moved or
        # re-keyed its cache), so its read is a download. With the network denied it fails here, before any apply.
        url = self.serve("moved.tar.gz", "ok")
        chezmoi = self.source(url)
        prefetch = self.bash('prefetch_chezmoi_externals "$1"', str(chezmoi))
        self.assertEqual(0, prefetch.returncode, prefetch.stderr)
        shutil.rmtree(self.cache)

        result = self.bash('assert_chezmoi_externals_cached "$1"', str(chezmoi))

        if "the check runs unguarded" in result.stdout:
            self.skipTest("no network-denial tool runs on this host; the check cannot deny chezmoi the download")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("chezmoi externals: chezmoi did not read the externals from its cache (under ", result.stderr)
        self.assertIn(url, result.stderr)
        self.assertIn(" with chezmoi version v", result.stdout)
        self.assertEqual(1, self.requests())  # the prefetch's; the denied read reached no server


class ChezmoiCacheCheckTest(unittest.TestCase):
    """assert_chezmoi_externals_cached against a chezmoi stub: the verdict table, each producer's failure, the
    guards."""

    def setUp(self) -> None:
        self.case = Path(tempfile.mkdtemp(prefix="chezmoi-cache-check-")).resolve()
        self.addCleanup(shutil.rmtree, self.case, True)
        self.calls = self.case / "calls"
        self.chezmoi = self.case / "chezmoi"
        self.chezmoi.write_text(STUB_CHEZMOI)
        self.chezmoi.chmod(0o755)

    def check(self, inject: str = "", **extra: str) -> subprocess.CompletedProcess[str]:
        # The stub is found on PATH under chezmoi's own name, the way make update names it.
        env = {**os.environ, "HOME": str(self.case), "TMPDIR": str(self.case), "CALLS": str(self.calls)}
        env.update({"PATH": f"{self.case}{os.pathsep}{env['PATH']}", "STUB_OUTPUT": "", "STUB_EXIT": "0", **extra})
        self.calls.unlink(missing_ok=True)
        return subprocess.run(
            [
                "bash",
                "-c",
                f'source "$1"; shift; {inject}assert_chezmoi_externals_cached "$1"',
                "_",
                str(LIB),
                "chezmoi",
            ],
            env=env,
            capture_output=True,
            text=True,
            timeout=COMMAND_SECONDS,
            check=False,
        )

    def recorded(self) -> list[str]:
        return self.calls.read_text().splitlines() if self.calls.exists() else []

    def test_the_verdict_follows_chezmoi_s_exit_status_and_the_listed_strings(self) -> None:
        cases = (
            (f"{case[0]} [{label}]", options, *case[1:]) for label, options in SHELL_MODES for case in VERDICT_CASES
        )
        for name, options, output, code, passes, reason in cases:
            with self.subTest(name):
                result = self.check(options, STUB_OUTPUT=output, STUB_EXIT=str(code))
                self.assertEqual(0 if passes else 1, result.returncode, result.stdout + result.stderr)
                # The version is named in both outcomes, so the log says which release a layout change arrived with.
                self.assertIn(" with chezmoi version v9.9.9-stub\n", result.stdout)
                if passes:
                    self.assertIn("chezmoi externals: chezmoi read the externals from its cache (", result.stdout)
                    self.assertEqual("", result.stderr)
                else:
                    self.assertEqual(1, len(result.stderr.splitlines()), result.stderr)
                    self.assertIn(
                        "chezmoi externals: chezmoi did not read the externals from its cache (", result.stderr
                    )
                    self.assertIn(f"status exited {code}): {reason}", result.stderr)
                    self.assertNotIn("read the externals from its cache (", result.stdout)
                # chezmoi is asked for its version, then for the status of the externals without refreshing them.
                version, status = (line.split("|", 1)[1] for line in self.recorded())
                self.assertEqual("--version", version)
                self.assertEqual("--refresh-externals=never status --include=externals", status)

    def test_every_producer_that_fails_stops_the_check_naming_it(self) -> None:
        for name, inject, env, reason in both_ways(CHECK_PRODUCER_CASES):
            with self.subTest(name):
                result = self.check(inject, **env)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"chezmoi externals: {reason}", result.stderr)
                self.assertNotIn("read the externals from its cache (", result.stdout)

    def test_the_first_guard_whose_probe_runs_wraps_the_chezmoi_call(self) -> None:
        # The table is probed in order with `true`; the chosen guard runs chezmoi, not only the probe.
        table = "CHEZMOI_EXTERNAL_NETWORK_GUARDS=('false' $'env\\tGUARDED=1' $'env\\tGUARDED=2'); "
        for name, options, *_ in both_ways((("guard table", ""),)):
            with self.subTest(name):
                result = self.check(options + table)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("chezmoi externals: cache check under env GUARDED=1 with chezmoi version", result.stdout)
                self.assertIn(
                    "chezmoi externals: chezmoi read the externals from its cache (under env GUARDED=1)", result.stdout
                )
                self.assertNotIn("unguarded", result.stdout)
                self.assertEqual(
                    ["|--version", "1|--refresh-externals=never status --include=externals"], self.recorded()
                )

    def test_without_a_working_guard_the_check_runs_unguarded_and_says_so(self) -> None:
        # The named limitation: no network-denial tool, so the check runs anyway and the log says it proves less.
        table = "CHEZMOI_EXTERNAL_NETWORK_GUARDS=('false'); "
        for name, options, *_ in both_ways((("no guard", ""),)):
            with self.subTest(name):
                result = self.check(options + table)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn(
                    "chezmoi externals: cache check unguarded with chezmoi version v9.9.9-stub", result.stdout
                )
                self.assertIn("the check runs unguarded and cannot tell a download from a cache read", result.stdout)
                self.assertIn("chezmoi externals: chezmoi read the externals from its cache (unguarded)", result.stdout)
                self.assertEqual(
                    ["|--version", "|--refresh-externals=never status --include=externals"], self.recorded()
                )
                failed = self.check(options + table, STUB_OUTPUT="chezmoi: unexpected EOF\n", STUB_EXIT="1")
                self.assertEqual(1, failed.returncode)
                self.assertIn("(unguarded, status exited 1): chezmoi: unexpected EOF", failed.stderr)


class ChezmoiExternalsWiringTest(unittest.TestCase):
    def test_setup_sh_carries_an_exact_copy_of_the_helper(self) -> None:
        # setup.sh runs before the repository exists, so it cannot source the helper.
        helper = LIB.read_text()
        body = helper[helper.index("# The sha256 of no bytes") :]
        setup = (ROOT / "setup.sh").read_text()
        begin = "# --- chezmoi-externals.sh begin ---\n"
        self.assertEqual(
            body, setup[setup.index(begin) + len(begin) : setup.index("# --- chezmoi-externals.sh end ---\n")]
        )

    def test_the_bootstrap_and_make_update_prefetch_then_check_the_cache_before_chezmoi_reads_the_target_state(
        self,
    ) -> None:
        setup = (ROOT / "setup.sh").read_text()
        run = setup[setup.index("function run_chezmoi()") :]
        prefetch = run.index('prefetch_chezmoi_externals "${chezmoi_cmd}"')
        check = run.index('assert_chezmoi_externals_cached "${chezmoi_cmd}"')
        self.assertLess(prefetch, check)
        for read in ('"${chezmoi_cmd}" status', '"${chezmoi_cmd}" diff', '"${chezmoi_cmd}" apply'):
            self.assertLess(check, run.index(read), read)
        makefile = (ROOT / "Makefile").read_text()
        tree = makefile[makefile.index("\nupdate-tree:\n") :]
        self.assertLess(
            tree.index(
                "source scripts/lib/chezmoi-externals.sh && prefetch_chezmoi_externals chezmoi"
                " && assert_chezmoi_externals_cached chezmoi"
            ),
            tree.index("chezmoi apply --verbose"),
        )

    def test_the_public_bootstrap_row_requires_the_cache_check_s_verdict_line(self) -> None:
        # The CI row is the live proof: it fails unless setup.sh printed the verdict, which names the chezmoi version
        # and the guard. The literal it requires is the library's own, so a reworded verdict fails here first.
        workflow = (ROOT / ".github/workflows/remote.yaml").read_text()
        step = workflow[workflow.index("- name: Bootstrap the checked-out public source") :]
        step = step[: step.index("\n      - name: ")]
        verdict = "chezmoi externals: chezmoi read the externals from its cache"
        self.assertIn(f"printf '{verdict} (%s)\\n'", LIB.read_text())
        setup = step.index('bash "${GITHUB_WORKSPACE}/setup.sh" | tee "${RUNNER_TEMP}/setup.log"')
        self.assertLess(step.index("set -euo pipefail"), setup)
        # The Linux rows lift Ubuntu 24.04's user-namespace restriction first, so their check runs under unshare.
        self.assertLess(step.index("sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0"), setup)
        self.assertLess(setup, step.index(f"grep -F '{verdict}' \"${{RUNNER_TEMP}}/setup.log\""))


if __name__ == "__main__":
    unittest.main()
