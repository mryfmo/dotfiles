#!/usr/bin/env python3
"""Run the unittest suite in parallel, one `unittest discover` per test module, with one combined summary.

Each module runs as `python -m unittest discover -s <start> -p <module file> -v`, the serial
`make unit-test` command narrowed to one file, so discovery, `load_tests`, `setUpClass` and the
assertions are the serial run's. The run fails when any module fails, when a module prints no
unittest summary, or when the modules together ran a different number of tests than discovery
found in this process: a module that dies or stops early cannot read as a pass.
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

RAN = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)
# The last line unittest prints: "OK", "OK (skipped=2)", "FAILED (failures=1, errors=2)" or "NO TESTS RAN".
VERDICT = re.compile(r"^(OK|FAILED|NO TESTS RAN)(?: \((.*)\))?\s*\Z", re.MULTILINE)
COUNT = re.compile(r"(\w+)=(\d+)")


@dataclass
class Result:
    module: str
    expected: int
    seconds: float = 0.0
    returncode: int | None = None
    ran: int | None = None
    verdict: str | None = None
    counts: Counter = field(default_factory=Counter)
    output: str = ""

    @property
    def problem(self) -> str | None:
        """Why this module fails the run, or None when it passed."""
        if self.ran is None or self.verdict is None:
            return f"exit {self.returncode}, no unittest summary"
        if self.ran != self.expected:
            return f"ran {self.ran} tests, discovery found {self.expected}"
        if self.returncode != 0 or self.verdict != "OK":
            return f"exit {self.returncode}, {self.verdict}"
        return None


def discover(start: Path, pattern: str) -> dict[str, int]:
    """The test count of each module file name, counted by the `-p <file>` discovery its shard runs.

    Files of one name in different packages share a shard, as `-p` matches them all. ValueError when
    the per-file counts do not add up to one discovery of the whole pattern (a `load_tests` that
    answers the file pattern differently, say): the shards would then not run the serial suite.
    """
    whole = unittest.TestLoader().discover(str(start), pattern=pattern).countTestCases()
    names = sorted({path.name for path in start.rglob("*.py") if fnmatch.fnmatch(path.name, pattern)})
    counts = {name: unittest.TestLoader().discover(str(start), pattern=name).countTestCases() for name in names}
    counts = {name: count for name, count in counts.items() if count}
    if sum(counts.values()) != whole:
        raise ValueError(f"per-file discovery found {sum(counts.values())} tests, one discovery of {pattern} {whole}")
    return counts


def run_module(start: Path, name: str, expected: int) -> Result:
    result = Result(module=name, expected=expected)
    started = time.monotonic()
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(start), "-p", name, "-v"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
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
    parser.add_argument("--jobs", default=0, type=int, help="parallel modules; 0 is the CPU count")
    args = parser.parse_args(argv)
    jobs = args.jobs or os.cpu_count() or 1

    started = time.monotonic()
    try:
        expected = discover(args.start, args.pattern)
    except ValueError as error:
        print(f"unittest-shards: {error}", file=sys.stderr)
        return 1
    if not expected:
        print(f"unittest-shards: discovery found no test modules under {args.start}", file=sys.stderr)
        return 1
    total = sum(expected.values())
    print(f"unittest-shards: {total} tests in {len(expected)} modules under {args.start}, {jobs} at a time", flush=True)

    # The biggest modules start first, so a long one does not begin last and set the wall time alone.
    order = sorted(expected, key=lambda name: (-expected[name], name))
    lock = threading.Lock()
    results: list[Result] = []

    def task(name: str) -> None:
        result = run_module(args.start, name, expected[name])
        with lock:
            results.append(result)
            status = result.problem or "ok"
            print(f"\n===== {name}: {result.ran} tests, {result.seconds:.1f}s, {status} =====", flush=True)
            print(result.output.rstrip(), flush=True)

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for future in [pool.submit(task, name) for name in order]:
            future.result()

    wall = time.monotonic() - started
    counts: Counter = Counter()
    for result in results:
        counts.update(result.counts)
    ran = sum(result.ran or 0 for result in results)
    failed = sorted((result for result in results if result.problem), key=lambda result: result.module)

    print("\n===== unittest-shards summary =====")
    print(
        "slowest modules: "
        + ", ".join(f"{r.module} {r.seconds:.1f}s" for r in sorted(results, key=lambda r: -r.seconds)[:8])
    )
    for result in failed:
        print(f"FAILED module {result.module}: {result.problem}")
    if ran != total:
        print(f"FAILED count: ran {ran} tests, discovery found {total}")
    detail = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    print(f"Ran {ran} tests in {wall:.3f}s ({len(results)} modules, {jobs} jobs)")
    ok = not failed and ran == total
    print(("OK" if ok else "FAILED") + (f" ({detail})" if detail else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
