#!/usr/bin/env bash
# shellcheck shell=bash

# @file scripts/lib/npm-release-age.sh
# @brief The repository's one reader of a release-age window against an npm version's publish time.
# @description
#   npm_release_age_verdict decides whether one exact version is old enough for a window of N days plus a
#   60-second margin for clock skew, from the registry's `time` map. Two callers source it:
#   scripts/upgrade-tools.sh before it rebuilds an npm: tool on a new node (npm's own min-release-age from
#   ~/.npmrc, as the shdoc below names it), and scripts/ci/npm-cooldown-skew-check.sh before CI installs a
#   multi-package npm tool (mise's minimum_release_age, `72h` passed as `3`). One function, sourced, never
#   copied: a second reading of the window or the publish time would be a second place for the 2026-10-24
#   class of failure (ccusage 20.0.38 without its linux-x64 binary, regime-cutover U114) to hide.
#   Sourced only: `source scripts/lib/npm-release-age.sh`.

#
# @description Decide whether npm's own release-age window (min-release-age, ~/.npmrc) lets npm install one exact
#   version again, from the window npm reports and the version's publish time in the registry. The rebuild of an
#   installed version asks this first, so a version younger than the window is skipped before its install is moved,
#   instead of failing in npm (ETARGET) after it. Every read is strict: an answer that is not exactly what npm prints
#   is "cannot tell", never "old enough". The publish time is compared at its full precision (fractional seconds to
#   the microsecond), and a version counts as old enough only from 60 seconds after the window ends, so a clock that
#   differs from npm's by less than that never lets the rebuild move an install npm then refuses.
# @arg $1 string The version mise reports as installed: one SemVer 2.0.0 version without build metadata.
# @arg $2 string `npm config get min-release-age` output: a number of days, or `null` when npm sets no window.
# @arg $3 number Optional: the current time in Unix seconds, for a frozen clock; the system clock when absent.
# @stdin `npm view --json <package> time`: the registry's map of version to publish time.
# @stdout The reason, when the version is not old enough or the answer cannot be told.
# @exitcode 0 The version is at least min-release-age days and 60 seconds old, or npm sets no window.
# @exitcode 1 The version is younger than that.
# @exitcode 2 The version, the window, the publish time or the given time cannot be read.
#
function npm_release_age_verdict() {
    # The program is read into a variable, so stdin stays npm view's answer; read -d '' ends with status 1 at the end
    # of the here-document by design, so an empty program is the failure checked. (A here-document inside $(...)
    # breaks bash 3.2, the /bin/bash of macOS.)
    local code=""
    IFS= read -r -d '' code << 'PY' || [ -n "${code}" ] || return 2
import datetime
import json
import re
import sys

version, age, *clock = sys.argv[1:]
# Past the end of npm's window by this much before a version counts as old enough: clocks differ.
MARGIN = datetime.timedelta(seconds=60)
# The SemVer 2.0.0 regular expression, verbatim from https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
# (ASCII digits only; fullmatch, so no trailing newline). npm reads anything else, such as 20.0.0-a..b, as a tag.
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
    re.ASCII,
)
# The registry's publish times, as npm view prints them: UTC with optional fractional seconds.
PUBLISHED = re.compile(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?Z", re.ASCII)


def cannot_tell(reason):
    print(reason)
    sys.exit(2)


def microseconds(fraction):
    """A decimal fraction of a second in whole microseconds, rounded up, so a time is never read as earlier."""
    nanoseconds = int((fraction or "").ljust(9, "0"))
    return -(-nanoseconds // 1000)


exact = SEMVER.fullmatch(version)
# npm drops build metadata, so 1.2.3+build would fetch 1.2.3, not the string mise reports.
if exact is None or exact.group(5) is not None:
    cannot_tell(f"mise reports {version!r}, not one exact version")
# timezone.utc, not datetime.UTC: macOS's /usr/bin/python3 is 3.9.
epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
if not clock:
    now = datetime.datetime.now(datetime.timezone.utc)
elif len(clock) == 1 and (given := re.fullmatch(r"(0|[1-9]\d{0,11})(?:\.(\d{1,6}))?", clock[0], re.ASCII)):
    now = epoch + datetime.timedelta(seconds=int(given[1]), microseconds=microseconds(given[2]))
else:
    cannot_tell(f"the given time {clock!r} is not one number of Unix seconds")
if age == "null":
    sys.exit(0)
if not re.fullmatch(r"(?:0|[1-9]\d{0,5})(?:\.\d{1,6})?", age, re.ASCII):
    cannot_tell(f"npm config get min-release-age printed {age!r}, not a number of days")
try:
    times = json.load(sys.stdin)
except ValueError:
    cannot_tell("npm view printed no JSON publish times")
published = times.get(version) if isinstance(times, dict) else None
match = PUBLISHED.fullmatch(published) if isinstance(published, str) else None
if match is None:
    cannot_tell(f"npm view lists no publish time for {version}")
try:
    when = datetime.datetime(*map(int, match.groups()[:6]), tzinfo=datetime.timezone.utc)
except ValueError:
    cannot_tell(f"npm view lists {published!r} for {version}, not a date")
# Full precision: 2026-10-23T21:20:46.540Z is 540 ms later than 21:20:46, and npm compares the whole value.
when += datetime.timedelta(microseconds=microseconds(match[7]))
clears = when + datetime.timedelta(days=float(age)) + MARGIN
if now < clears:
    print(
        f"{version} was published {when:%Y-%m-%dT%H:%M:%S.%fZ}, younger than npm's min-release-age of {age} days"
        f" and a 60-second margin; it can be rebuilt from {clears:%Y-%m-%dT%H:%M:%S.%fZ}"
    )
    sys.exit(1)
PY
    python3 -I -c "${code}" "$@"
}
