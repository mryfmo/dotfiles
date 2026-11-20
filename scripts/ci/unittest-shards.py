#!/usr/bin/env python3
"""Run the unittest suite in parallel shards with one combined summary.

A shard is `python -m unittest discover -s <start> -p <module file> -v`, the serial `make unit-test`
command narrowed to one file, so discovery, `load_tests`, `setUpClass` and the assertions are the
serial run's. A module of more than `--split` tests runs as several shards of that file, each
selecting its own tests with exact `-k` patterns. The run fails when any shard fails, when a shard
prints no unittest summary, or when a shard ran a different number of tests than discovery found
for it in this process: a shard that dies or stops early cannot read as a pass.

`--shard K/N` (regime-cutover U622) runs one of N equal parts of the plan: the shards are ordered biggest first (the
plan, deterministic from discovery), and part K is every N-th shard from the K-th, so the N parts partition the plan
without overlap and each gets its share of the long shards. CI runs the parts as matrix rows. `--dry-run` prints the
plan (one line per shard, `  <name>: <n> tests`) and exits 0 without running anything.

`--modules <file>` (regime-cutover U623) restricts the plan to the test modules the file lists, one per line, each a
module file name (`test_x.py`) or its path under the start directory (`tests/unit/test_x.py`), as
scripts/ci/affected-tests.py prints them for a pull request; a line naming no test module under the start directory
is a refusal (exit 1), never a silent narrowing. `--shard K/N` then partitions the restricted plan. A listing that
names no module, or a part of the restricted plan that holds no shard, is nothing to run: one line says so and the
exit is 0, since a selection that reaches no module is the selection's answer, not a failure of the run.

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


def shard_part(text: str) -> tuple[int, int]:
    """`K/N` as (K, N) with 1 <= K <= N; anything else is an argparse usage error (exit 2)."""
    match = re.fullmatch(r"([0-9]+)/([0-9]+)", text)
    if match is None:
        raise argparse.ArgumentTypeError(f"{text!r} is not K/N")
    part, parts = int(match.group(1)), int(match.group(2))
    if not 1 <= part <= parts:
        raise argparse.ArgumentTypeError(f"{text!r}: K must be in 1..N")
    return part, parts


def plan(shards: list[Shard], part: tuple[int, int] | None) -> list[Shard]:
    """The shards in run order, biggest first so a long one does not begin last and set the wall time alone; with
    `part` (K, N), every N-th of that order from the K-th, so the N parts together list every shard once."""
    order = sorted(shards, key=lambda shard: (-shard.expected, shard.name))
    if part is None:
        return order
    return order[part[0] - 1 :: part[1]]


def restrict(shards: list[Shard], listing: Path, start: Path, pattern: str) -> list[Shard]:
    """The shards of the modules `listing` names, one per line (a module file name, or a path to a file under
    `start`; blank lines are skipped), in the plan's order. ValueError names a listing that cannot be read or an
    entry that is no test module under `start`: a module absent from the tree is a refusal."""
    try:
        lines = listing.read_text().splitlines()
    except OSError as error:
        raise ValueError(f"cannot read {listing}: {error.strerror}") from error
    present = {path.name for path in start.rglob("*.py") if path.is_file() and fnmatch.fnmatch(path.name, pattern)}
    names: set[str] = set()
    for line in lines:
        entry = line.strip()
        if not entry:
            continue
        listed = Path(entry)
        under = listed.name == entry or (listed.is_file() and listed.resolve().is_relative_to(start.resolve()))
        if listed.name not in present or not under:
            raise ValueError(f"{listing} names {entry}, which is no test module under {start}")
        names.add(listed.name)
    return [shard for shard in shards if shard.file in names]  # lint-comparisons: allow a module file name, no path


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
    parser.add_argument("--shard", type=shard_part, metavar="K/N", help="run part K of N of the plan (K in 1..N)")
    parser.add_argument("--modules", type=Path, metavar="FILE", help="run the test modules FILE lists, one per line")
    parser.add_argument("--dry-run", action="store_true", help="print the plan and exit 0 without running a test")
    args = parser.parse_args(argv)
    jobs = args.jobs or os.cpu_count() or 1

    started = time.monotonic()
    # The shards run `python -m unittest`, which puts the working directory first on sys.path, where a script
    # gets its own directory; discovery here imports the same way, so `from tests.unit.x import y` resolves.
    sys.path[0] = os.getcwd()
    try:
        found = discover(args.start, args.pattern, args.split)
    except ValueError as error:
        print(f"unittest-shards: {error}", file=sys.stderr)
        return 1
    if not found:
        print(f"unittest-shards: discovery found no test modules under {args.start}", file=sys.stderr)
        return 1
    whole = len({shard.file for shard in found})
    restricted = ""
    if args.modules is not None:
        try:
            found = restrict(found, args.modules, args.start, args.pattern)
        except ValueError as error:
            print(f"unittest-shards: {error}", file=sys.stderr)
            return 1
        restricted = f", {len({shard.file for shard in found})} of {whole} modules listed in {args.modules}"
        if not found:
            print(f"unittest-shards: nothing to run: {args.modules} lists no module of the {whole} under {args.start}")
            return 0
    # The biggest shards start first, so a long one does not begin last and set the wall time alone; with --shard,
    # this process's part of that order (shard_part, plan).
    order = plan(found, args.shard)
    if not order and args.modules is not None:
        print(
            f"unittest-shards: nothing to run: shard {args.shard[0]}/{args.shard[1]} of {len(found)}{restricted} is empty"
        )
        return 0
    if not order:
        print(f"unittest-shards: shard {args.shard[0]}/{args.shard[1]} of {len(found)} is empty", file=sys.stderr)
        return 1
    part = f", shard {args.shard[0]}/{args.shard[1]} of {len(found)}" if args.shard else ""
    total = sum(shard.expected for shard in order)
    modules = len({shard.file for shard in order})
    print(
        f"unittest-shards: {total} tests in {modules} modules, {len(order)} shards under {args.start}{part}"
        f"{restricted}, {jobs} at a time",
        flush=True,
    )
    if args.dry_run:
        for shard in order:
            print(f"  {shard.name}: {shard.expected} tests")
        return 0

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
