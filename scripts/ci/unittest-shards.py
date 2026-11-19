#!/usr/bin/env python3
"""Run the unittest suite in parallel shards with one combined summary.

A shard is `python -m unittest discover -s <start> -p <module file> -v`, the serial `make unit-test`
command narrowed to one file, so discovery, `load_tests`, `setUpClass` and the assertions are the
serial run's. A module of more than `--split` tests runs as several shards of that file, each
selecting its own tests with exact `-k` patterns. The run fails when any shard fails, when a shard
prints no unittest summary, or when a shard ran a different number of tests than discovery found
for it in this process: a shard that dies or stops early cannot read as a pass.

Duration planning (regime-cutover U598) is opt-in by `--shard-seconds N`. `scripts/ci/unittest-durations.tsv` holds
each module's test count and seconds from one `UNIT_TEST_JOBS=6 make unit-test`, so a test of the module costs
`seconds / tests`; with N above 0 a module of the table is cut into shards of at most N seconds at that cost (and
never more than `--split` tests), a module absent from it into shards of `--split` tests, the shards start longest
first, and at most `--heavy-jobs` shards of heavy modules (`--heavy-seconds` a test or more) run at once. The default,
N = 0, is the count order unchanged: shards of `--split` tests, the biggest count first. Measured 2026-11-19 on the
laptop at six jobs, the count order ran 2899 tests in 1087 s (5400 shard-seconds, perfect packing 900 s); planning at
90 s a shard, longest first, then took 1492 s (8952 shard-seconds) and with the heavy cap at four 2269 s (13,613),
but the count order run again as the control took 2372 s (11,954), so the host had slowed by about 2.2x over the
session (CrowdStrike Falcon judges every exec; the suite spawns some 260,000 processes) and the local runs give no
verdict on the planned mode. So the planned mode stays a flag until a run on the CI runner measures it. The table is
advisory: a stale row
costs packing, never a test; a row that cannot be read fails the run by file and line, so the table cannot rot
silently. `--record-durations PATH` writes the measured table of the run just made, which is how the file is refreshed.

Every shard runs with tests/unit/scratch_git.py's settings in its environment (regime-cutover U100), so no git a test
runs in a scratch repository starts background maintenance (`git maintenance run --auto`, detached and holding
maintenance.lock since git 2.55), however the test made the repository.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import platform
import re
import statistics
import subprocess
import sys
import threading
import time
import unittest
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tests/unit"))
from scratch_git import quiet_git_env  # noqa: E402

RAN = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)
# The last line unittest prints: "OK", "OK (skipped=2)", "FAILED (failures=1, errors=2)" or "NO TESTS RAN".
VERDICT = re.compile(r"^(OK|FAILED|NO TESTS RAN)(?: \((.*)\))?\s*\Z", re.MULTILINE)
COUNT = re.compile(r"(\w+)=(\d+)")
# The measured table beside this script: `module<TAB>tests<TAB>seconds` rows under a header, `#` lines being comments.
DEFAULT_DURATIONS = Path(__file__).resolve().with_name("unittest-durations.tsv")
DURATIONS_COLUMNS = ("module", "tests", "seconds")


@dataclass
class Shard:
    name: str
    file: str
    expected: int
    # Exact `-k` patterns for a split module's shard; None runs the whole file.
    patterns: list[str] | None = None
    # The seconds the duration table predicts for it (a module absent from the table costs the table's median a test).
    estimate: float = 0.0


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


def read_durations(path: Path) -> dict[str, float]:
    """Each module's measured seconds per test from the table at PATH; empty when there is no file there.

    ValueError names the file and line of a row that is not `module<TAB>tests<TAB>seconds` with a positive test count
    and a non-negative time: a table that cannot be read is never taken for an empty one (standing order 21).
    """
    if not path.is_file():
        return {}
    costs: dict[str, float] = {}
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("\t")
        if tuple(fields) == DURATIONS_COLUMNS:
            continue
        try:
            name, tests, seconds = fields
            count, total = int(tests), float(seconds)
        except ValueError:
            raise ValueError(f"{path}:{number}: not `module<TAB>tests<TAB>seconds`: {line!r}") from None
        if not name or count <= 0 or total < 0:
            raise ValueError(f"{path}:{number}: tests must be positive and seconds not negative: {line!r}")
        costs[name] = total / count
    return costs


def discover(start: Path, pattern: str, split: int, costs: dict[str, float], shard_seconds: float) -> list[Shard]:
    """The shards of the suite, each with the test count the `-p <file>` discovery it runs finds here.

    Files of one name in different packages share a shard, as `-p` matches them all. A module of more than `split`
    tests (0: never) runs as several shards of contiguous tests; a module `costs` holds (seconds a test) is cut so
    that no shard is planned over `shard_seconds` (0: by `split` alone). ValueError when the per-file counts do not
    add up to one discovery of the whole pattern (a `load_tests` that answers the file pattern differently, say): the
    shards would then not run the serial suite.
    """
    whole = unittest.TestLoader().discover(str(start), pattern=pattern).countTestCases()
    names = sorted({path.name for path in start.rglob("*.py") if fnmatch.fnmatch(path.name, pattern)})
    fallback = statistics.median(costs.values()) if costs else 1.0
    shards: list[Shard] = []
    for name in names:
        tests = tests_of(unittest.TestLoader().discover(str(start), pattern=name))
        if not tests:
            continue
        cost = costs.get(name, fallback)
        limit = split
        if split > 0 and shard_seconds > 0 and name in costs and cost > 0:
            limit = max(1, min(split, int(shard_seconds // cost)))
        if limit <= 0 or len(tests) <= limit or not all(selectable(test) for test in tests):
            shards.append(Shard(name=name, file=name, expected=len(tests), estimate=cost * len(tests)))
            continue
        # Contiguous runs in loader order, so a class's tests stay together where they fit.
        parts = -(-len(tests) // limit)
        size = -(-len(tests) // parts)
        for index in range(parts):
            chunk = tests[index * size : (index + 1) * size]
            # A leading * keeps unittest from wrapping the pattern in *...*, a substring match.
            patterns = [f"*{test.id()}" for test in chunk]
            shards.append(Shard(f"{name}[{index + 1}/{parts}]", name, len(chunk), patterns, cost * len(chunk)))
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


def record_durations(path: Path, results: list[Result], jobs: int) -> None:
    """Write the measured table of this run to PATH: each module's test count and the sum of its shards' seconds."""
    tests: Counter = Counter()
    seconds: dict[str, float] = {}
    for result in results:
        tests[result.shard.file] += result.shard.expected
        seconds[result.shard.file] = seconds.get(result.shard.file, 0.0) + result.seconds
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"# Measured by scripts/ci/unittest-shards.py --jobs {jobs} on {platform.system()} at {stamp}: each module's",
        "# test count and the sum of its shards' seconds. The planner cuts a module into shards of at most",
        "# --shard-seconds at seconds/tests and starts the longest first. Refresh with",
        "# `uv run python scripts/ci/unittest-shards.py --start tests/unit --jobs 6 --record-durations <this file>`.",
        "\t".join(DURATIONS_COLUMNS),
    ]
    lines += [f"{name}\t{tests[name]}\t{seconds[name]:.1f}" for name in sorted(tests)]
    path.write_text("".join(line + "\n" for line in lines))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="tests/unit", type=Path, help="discovery start directory")
    parser.add_argument("--pattern", default="test*.py", help="discovery file pattern")
    parser.add_argument("--jobs", default=0, type=int, help="shards at a time; 0 is the CPU count")
    parser.add_argument("--split", default=50, type=int, help="split a module of more tests; 0 never splits")
    parser.add_argument(
        "--durations",
        default=DEFAULT_DURATIONS,
        type=Path,
        help="the measured table (module, tests, seconds) the shards are planned by; a missing file plans by count",
    )
    parser.add_argument(
        "--shard-seconds",
        default=0.0,
        type=float,
        help="plan by the duration table: cut a module it holds into shards of at most this many planned seconds, "
        "longest first, heavy shards capped; 0 (the default) cuts by --split alone, biggest count first",
    )
    parser.add_argument(
        "--record-durations", default=None, type=Path, help="write this run's measured table here when it ends"
    )
    parser.add_argument(
        "--heavy-seconds",
        default=5.0,
        type=float,
        help="a module the table holds at this many seconds a test or more is heavy (exec-bound)",
    )
    parser.add_argument(
        "--heavy-jobs", default=0, type=int, help="heavy shards at a time; 0 is two thirds of --jobs, at least 1"
    )
    args = parser.parse_args(argv)
    jobs = args.jobs or os.cpu_count() or 1

    started = time.monotonic()
    # The shards run `python -m unittest`, which puts the working directory first on sys.path, where a script
    # gets its own directory; discovery here imports the same way, so `from tests.unit.x import y` resolves.
    sys.path[0] = os.getcwd()
    try:
        costs = read_durations(args.durations)
        shards = discover(args.start, args.pattern, args.split, costs, args.shard_seconds)
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
    planned_mode = args.shard_seconds > 0
    if planned_mode:
        # The longest planned shard starts first, so a long one does not begin last and set the wall time alone;
        # the plan line shows what the table predicts, against which the summary's slowest shards are read.
        order = sorted(shards, key=lambda shard: (-shard.estimate, -shard.expected, shard.name))
    else:
        # The biggest shards start first, so a long one does not begin last and set the wall time alone.
        order = sorted(shards, key=lambda shard: (-shard.expected, shard.name))
    planned = sum(shard.estimate for shard in shards)
    if not planned_mode:
        basis = "test count (--shard-seconds 0)"
    elif costs:
        basis = f"{args.durations}"
    else:
        basis = f"test count (no duration table at {args.durations})"
    # A heavy shard's tests spawn a lever hundreds of times each, so the shard is bound by the host's exec path, one
    # shared queue where an endpoint-security or Gatekeeper daemon judges every exec, and shards of one heavy module
    # slow each other down superlinearly (the module docstring's measurements). So in the planned mode at most
    # heavy_jobs heavy shards run at once, the light shards fill the other slots, and each queue is longest first.
    heavy_jobs = args.heavy_jobs or max(1, jobs * 2 // 3)
    heavy_names = (
        {shard.name for shard in shards if costs.get(shard.file, 0.0) >= args.heavy_seconds} if planned_mode else set()
    )
    heavy_queue = [shard for shard in order if shard.name in heavy_names]
    light_queue = [shard for shard in order if shard.name not in heavy_names]
    print(
        f"unittest-shards: planned by {basis}: {planned:.0f} shard-seconds estimated, longest shard "
        f"{order[0].name} {order[0].estimate:.0f} s, ideal wall {planned / jobs:.0f} s at {jobs} jobs; "
        f"{len(heavy_queue)} heavy shards ({args.heavy_seconds:g} s a test or more) at most {heavy_jobs} at a time",
        flush=True,
    )
    lock = threading.Lock()
    results: list[Result] = []

    def task(shard: Shard) -> None:
        result = run_shard(args.start, shard)
        with lock:
            results.append(result)
            status = result.problem or "ok"
            print(f"\n===== {shard.name}: {result.ran} tests, {result.seconds:.1f}s, {status} =====", flush=True)
            print(result.output.rstrip(), flush=True)

    running: dict[Future, Shard] = {}
    heavy_running = 0
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        while heavy_queue or light_queue or running:
            while len(running) < jobs and (heavy_queue or light_queue):
                if heavy_queue and heavy_running < heavy_jobs:
                    shard = heavy_queue.pop(0)
                    heavy_running += 1
                elif light_queue:
                    shard = light_queue.pop(0)
                else:
                    break  # the heavy shards left wait for a heavy slot
                running[pool.submit(task, shard)] = shard
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for future in done:
                shard = running.pop(future)
                future.result()
                if shard.name in heavy_names:
                    heavy_running -= 1

    wall = time.monotonic() - started
    counts: Counter = Counter()
    for result in results:
        counts.update(result.counts)
    ran = sum(result.ran or 0 for result in results)
    failed = sorted((result for result in results if result.problem), key=lambda result: result.shard.name)
    if args.record_durations is not None:
        record_durations(args.record_durations, results, jobs)

    print("\n===== unittest-shards summary =====")
    slowest = sorted(results, key=lambda result: -result.seconds)[:8]
    print("slowest shards: " + ", ".join(f"{result.shard.name} {result.seconds:.1f}s" for result in slowest))
    print(f"shard-seconds: {sum(result.seconds for result in results):.1f} measured, {planned:.0f} planned")
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
