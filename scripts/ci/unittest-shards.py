#!/usr/bin/env python3
"""Run the unittest suite in parallel shards with one combined summary.

A shard is `python -m unittest discover -s <start> -p <module file> -v`, the serial `make unit-test`
command narrowed to one file, so discovery, `load_tests`, `setUpClass` and the assertions are the
serial run's. A module of more than `--split` tests runs as several shards of that file, each
selecting its own tests with exact `-k` patterns. The run fails when any shard fails, when a shard
prints no unittest summary, or when a shard ran a different number of tests than discovery found
for it in this process: a shard that dies or stops early cannot read as a pass.

Every shard runs with tests/unit/scratch_git.py's settings in its environment (regime-cutover U100), so no git a test
runs in a scratch repository starts background maintenance (`git maintenance run --auto`, detached and holding
maintenance.lock since git 2.55), however the test made the repository.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
import threading
import time
import unittest
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tests/unit"))
from scratch_git import quiet_git_env  # noqa: E402

RAN = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)
# The last line unittest prints: "OK", "OK (skipped=2)", "FAILED (failures=1, errors=2)" or "NO TESTS RAN".
VERDICT = re.compile(r"^(OK|FAILED|NO TESTS RAN)(?: \((.*)\))?\s*\Z", re.MULTILINE)
COUNT = re.compile(r"(\w+)=(\d+)")


@dataclass
class Shard:
    name: str
    file: str
    expected: int
    # Exact `-k` patterns for a split module's shard; None runs the whole file.
    patterns: list[str] | None = None


@dataclass
class Result:
    shard: Shard
    seconds: float = 0.0
    returncode: int | None = None
    ran: int | None = None
    verdict: str | None = None
    counts: Counter = field(default_factory=Counter)
    output: str = ""

    @property
    def problem(self) -> str | None:
        """Why this shard fails the run, or None when it passed."""
        if self.ran is None or self.verdict is None:
            return f"exit {self.returncode}, no unittest summary"
        if self.ran != self.shard.expected:
            return f"ran {self.ran} tests, discovery found {self.shard.expected}"
        if self.returncode != 0 or self.verdict != "OK":
            return f"exit {self.returncode}, {self.verdict}"
        return None


def tests_of(suite: unittest.TestSuite) -> list[unittest.TestCase]:
    found = []
    for test in suite:
        found += tests_of(test) if isinstance(test, unittest.TestSuite) else [test]
    return found


def selectable(test: unittest.TestCase) -> bool:
    """Whether a `-k` pattern on its id selects exactly this test: a plain method of a module without load_tests."""
    cls = type(test)
    module = sys.modules.get(cls.__module__)
    name = getattr(test, "_testMethodName", "")
    return (
        module is not None
        and not hasattr(module, "load_tests")
        and test.id() == f"{cls.__module__}.{cls.__qualname__}.{name}"
        and callable(getattr(cls, name, None))
    )


def discover(start: Path, pattern: str, split: int) -> list[Shard]:
    """The shards of the suite, each with the test count the `-p <file>` discovery it runs finds here.

    Files of one name in different packages share a shard, as `-p` matches them all. ValueError when
    the per-file counts do not add up to one discovery of the whole pattern (a `load_tests` that
    answers the file pattern differently, say): the shards would then not run the serial suite.
    """
    whole = unittest.TestLoader().discover(str(start), pattern=pattern).countTestCases()
    names = sorted({path.name for path in start.rglob("*.py") if fnmatch.fnmatch(path.name, pattern)})
    shards: list[Shard] = []
    for name in names:
        tests = tests_of(unittest.TestLoader().discover(str(start), pattern=name))
        if not tests:
            continue
        if split <= 0 or len(tests) <= split or not all(selectable(test) for test in tests):
            shards.append(Shard(name=name, file=name, expected=len(tests)))
            continue
        # Contiguous runs in loader order, so a class's tests stay together where they fit.
        parts = -(-len(tests) // split)
        size = -(-len(tests) // parts)
        for index in range(parts):
            chunk = tests[index * size : (index + 1) * size]
            # A leading * keeps unittest from wrapping the pattern in *...*, a substring match.
            patterns = [f"*{test.id()}" for test in chunk]
            shards.append(Shard(f"{name}[{index + 1}/{parts}]", name, len(chunk), patterns))
    found = sum(shard.expected for shard in shards)
    if found != whole:
        raise ValueError(f"per-file discovery found {found} tests, one discovery of {pattern} {whole}")
    return shards


def run_shard(start: Path, shard: Shard) -> Result:
    result = Result(shard=shard)
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(start), "-p", shard.file, "-v"]
    for pattern in shard.patterns or []:
        command += ["-k", pattern]
    started = time.monotonic()
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        env=quiet_git_env(os.environ),
        text=True,
        errors="replace",
        check=False,
    )
    result.seconds = time.monotonic() - started
    result.returncode = completed.returncode
    result.output = completed.stdout
    ran = RAN.findall(completed.stdout)
    verdict = VERDICT.search(completed.stdout.rstrip() + "\n")
    if len(ran) == 1 and verdict:
        result.ran = int(ran[0])
        result.verdict = verdict.group(1)
        result.counts.update({key: int(value) for key, value in COUNT.findall(verdict.group(2) or "")})
    return result


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="tests/unit", type=Path, help="discovery start directory")
    parser.add_argument("--pattern", default="test*.py", help="discovery file pattern")
    parser.add_argument("--jobs", default=0, type=int, help="shards at a time; 0 is the CPU count")
    parser.add_argument("--split", default=50, type=int, help="split a module of more tests; 0 never splits")
    args = parser.parse_args(argv)
    jobs = args.jobs or os.cpu_count() or 1

    started = time.monotonic()
    # The shards run `python -m unittest`, which puts the working directory first on sys.path, where a script
    # gets its own directory; discovery here imports the same way, so `from tests.unit.x import y` resolves.
    sys.path[0] = os.getcwd()
    try:
        shards = discover(args.start, args.pattern, args.split)
    except ValueError as error:
        print(f"unittest-shards: {error}", file=sys.stderr)
        return 1
    if not shards:
        print(f"unittest-shards: discovery found no test modules under {args.start}", file=sys.stderr)
        return 1
    total = sum(shard.expected for shard in shards)
    modules = len({shard.file for shard in shards})
    print(
        f"unittest-shards: {total} tests in {modules} modules, {len(shards)} shards under {args.start}, "
        f"{jobs} at a time",
        flush=True,
    )

    # The biggest shards start first, so a long one does not begin last and set the wall time alone.
    order = sorted(shards, key=lambda shard: (-shard.expected, shard.name))
    lock = threading.Lock()
    results: list[Result] = []

    def task(shard: Shard) -> None:
        result = run_shard(args.start, shard)
        with lock:
            results.append(result)
            status = result.problem or "ok"
            print(f"\n===== {shard.name}: {result.ran} tests, {result.seconds:.1f}s, {status} =====", flush=True)
            print(result.output.rstrip(), flush=True)

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for future in [pool.submit(task, shard) for shard in order]:
            future.result()

    wall = time.monotonic() - started
    counts: Counter = Counter()
    for result in results:
        counts.update(result.counts)
    ran = sum(result.ran or 0 for result in results)
    failed = sorted((result for result in results if result.problem), key=lambda result: result.shard.name)

    print("\n===== unittest-shards summary =====")
    slowest = sorted(results, key=lambda result: -result.seconds)[:8]
    print("slowest shards: " + ", ".join(f"{result.shard.name} {result.seconds:.1f}s" for result in slowest))
    for result in failed:
        print(f"FAILED shard {result.shard.name}: {result.problem}")
    if ran != total:
        print(f"FAILED count: ran {ran} tests, discovery found {total}")
    detail = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    print(f"Ran {ran} tests in {wall:.3f}s ({modules} modules, {len(results)} shards, {jobs} jobs)")
    ok = not failed and ran == total
    print(("OK" if ok else "FAILED") + (f" ({detail})" if detail else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
