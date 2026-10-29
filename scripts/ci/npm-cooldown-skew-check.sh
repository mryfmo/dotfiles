#!/usr/bin/env bash
# @file npm-cooldown-skew-check.sh
# @brief Refuse an npm tool whose meta package, or whose platform package for this runner, is younger than mise's release-age window plus 60 s.
# @description
#   A multi-package npm tool publishes its platform binaries as `optionalDependencies`, often minutes after the
#   meta package (ccusage 20.0.38: the meta package at 2026-10-21T10:49:51Z, its linux-x64 package at 10:54:25Z).
#   mise applies `minimum_release_age` to the version it resolves and passes the same cutoff to npm for the
#   dependencies, and npm's rule for an optional dependency it cannot fetch is to proceed without it. A job that
#   starts inside that skew after the cutoff (run 40087404553, 2026-10-24T10:49:49Z) therefore installs the tool
#   without its native binary, and only the smoke test after the install notices. This check runs before the
#   install and refuses the version until every package npm would fetch for this runner clears the window.
#   For each tool it reads, in this order, every answer parsed by Python's json with an exact shape check and
#   never by a regular expression over npm's output:
#   1. the version mise would install: the config's request (`mise tool --json`, `requested_versions`) unless the
#      argument carries one, resolved by `mise latest npm:<name>@<request>` ("Nothing is installed and no config
#      changes"). `mise latest npm:<name>` alone ignores the config's pin (mise 2026.10.19 printed 20.0.44 for a
#      config holding 20.0.37 on 2026-10-29), so the request is read first;
#   2. the window: `mise settings get minimum_release_age`, exactly `<N>h` or `<N>d`, passed to
#      npm_release_age_verdict as days (72h is 3; hours round up to the microday, so the window never shrinks);
#   3. the meta package's publish time (`npm view --json <name> time`) through npm_release_age_verdict;
#   4. its `optionalDependencies` (`npm view --json <name>@<version> optionalDependencies`): empty output is "no
#      optional dependencies", otherwise an object of package name to one version;
#   5. for each of them, `npm view --json <dep>@<ver> os cpu`, an object whose `os` and `cpu` are lists of strings.
#      The package is this runner's when both lists hold `node -p process.platform` and `process.arch`; a
#      `!`-prefixed entry is an unknown shape. Each matching package's publish time goes through
#      npm_release_age_verdict, and no matching package at all is a refusal naming the runner.
#   npm and node are the config's own, `mise -C <dir> exec node -- …`. Naming the tool keeps mise from installing
#   the config's other tools first: an unnamed `mise exec` installed all 35 of them on 2026-10-29.
#   Every refusal is printed, never the first alone, so one run names every package to wait for.
# @option --now <unix seconds> A frozen clock for npm_release_age_verdict (its third argument); nothing else reads the
#   clock. For tests.
# @arg $1 path The mise config directory (`mise -C`), holding the mise.toml whose requests and settings decide.
# @arg $@ string Tools, `npm:<name>` (the config's request) or `npm:<name>@<request>`; at least one.
# @stdout One `refuse: <package>@<version>: <reason>` line per package younger than the window plus 60 s, the reason
#   naming its publish time and the time it clears; `<name>@<version>: no optional dependencies` when there are none;
#   one `pass: <tool>: …` line per tool that passed, naming every package checked with its publish time.
# @stderr The command or field that could not be read, prefixed `npm-cooldown-skew-check:`.
# @exitcode 0 Every package is old enough.
# @exitcode 1 A package is younger than the window plus 60 s, or no optional dependency is built for this runner.
# @exitcode 2 An answer cannot be read: a mise or npm command failed or printed another shape, the window is not
#   `<N>h` or `<N>d`, the version is not one SemVer version, or the usage is wrong. Never read as "old enough".
# @example
#   scripts/ci/npm-cooldown-skew-check.sh "${RUNNER_TEMP}/statusline-mise" npm:ccstatusline npm:ccusage
set -euo pipefail

#
# @description Stop with exit 2: an answer cannot be read, so nothing is "old enough".
# @arg $1 string What could not be read, naming the command or the field.
#
function cannot_tell() {
    printf 'npm-cooldown-skew-check: %s; cannot tell whether the tools are old enough\n' "$1" >&2
    exit 2
}

function usage() {
    echo 'usage: npm-cooldown-skew-check.sh [--now <unix seconds>] <mise config dir> <tool>...' >&2
    exit 2
}

now=""
if [[ ${1:-} == --now ]]; then
    (($# >= 2)) || usage
    now=$2
    shift 2
fi
(($# >= 2)) || usage
config_dir=$1
shift
[[ -d ${config_dir} ]] || cannot_tell "${config_dir} is not a directory"

# The directory of this script: a parameter expansion, so no producer's status is at stake.
case ${BASH_SOURCE[0]} in
*/*) here=${BASH_SOURCE[0]%/*} ;;
*) here=. ;;
esac
# shellcheck source=scripts/lib/npm-release-age.sh
source "${here}/../lib/npm-release-age.sh"

# The one parser of every mise and npm answer: the mode names the shape, stdin carries the answer, and the result is
# printed in the form the shell needs. Exit 0 readable, 1 "not this runner's" (platform only), 2 unreadable with the
# reason on stderr. Read into a variable like npm_release_age_verdict's program, so stdin stays the answer.
parser=""
IFS= read -r -d '' parser << 'PY' || [ -n "${parser}" ] || cannot_tell "the parser program is empty"
import decimal
import json
import re
import sys

mode, *args = sys.argv[1:]
# One token: a platform or architecture as node prints it, or a version request as mise and npm take it.
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:+-]*", re.ASCII)
# A package name, scoped or not, as the registry lists it.
NAME = re.compile(r"(?:@[A-Za-z0-9._~-]+/)?[A-Za-z0-9._~-]+", re.ASCII)
WINDOW = re.compile(r"(0|[1-9]\d*)([hd])", re.ASCII)


def refuse(reason):
    print(f"npm-cooldown-skew-check: {reason}; cannot tell whether the tools are old enough", file=sys.stderr)
    sys.exit(2)


def read_json(source):
    try:
        return json.load(sys.stdin)
    except ValueError:
        refuse(f"{source} printed no JSON")


def strings(value):
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def requested(tool):
    """`mise tool --json <tool>`: exactly one requested version, the config's."""
    info = read_json(f"mise tool --json {tool}")
    versions = info.get("requested_versions") if isinstance(info, dict) else None
    if not strings(versions) or len(versions) != 1 or not TOKEN.fullmatch(versions[0]):
        refuse(f"mise tool --json {tool} lists {versions!r} as requested_versions, not one version request")
    print(versions[0])


def window():
    """`mise settings get minimum_release_age`: `<N>h` or `<N>d`, printed as the days the verdict takes."""
    text = sys.stdin.read().rstrip("\n")
    match = WINDOW.fullmatch(text)
    if match is None:
        refuse(f"mise settings get minimum_release_age printed {text!r}, not <N>h or <N>d")
    days = decimal.Decimal(match[1])
    if match[2] == "h":
        # Rounded up to the microday the verdict reads, so a window given in hours never shrinks.
        days = (days / 24).quantize(decimal.Decimal("0.000001"), rounding=decimal.ROUND_CEILING)
    print(days.quantize(decimal.Decimal(1)) if days == days.to_integral_value() else days.normalize())


def optional_dependencies(package):
    """`npm view --json <pkg>@<ver> optionalDependencies`: nothing, or an object of package name to one version."""
    text = sys.stdin.read()
    if text.strip() == "":
        return
    try:
        listed = json.loads(text)
    except ValueError:
        refuse(f"npm view --json {package} optionalDependencies printed no JSON")
    if not isinstance(listed, dict) or not all(
        isinstance(name, str) and NAME.fullmatch(name) and isinstance(version, str) and TOKEN.fullmatch(version)
        for name, version in listed.items()
    ):
        refuse(f"npm view --json {package} optionalDependencies printed {listed!r}, not an object of package name to version")
    for name in sorted(listed):
        print(name, listed[name])


def platform(system, arch, package):
    """`npm view --json <pkg>@<ver> os cpu`: exit 0 when both lists name this runner, 1 when they do not."""
    if not (TOKEN.fullmatch(system) and TOKEN.fullmatch(arch)):
        refuse(f"node -p printed {system!r} and {arch!r}, not a platform and an architecture")
    shape = read_json(f"npm view --json {package} os cpu")
    lists = [shape.get(field) for field in ("os", "cpu")] if isinstance(shape, dict) else [None, None]
    if not all(strings(entries) for entries in lists):
        refuse(f"npm view --json {package} os cpu printed {shape!r}, not an object whose os and cpu are lists of strings")
    if any(entry.startswith("!") for entries in lists for entry in entries):
        refuse(f"{package} declares a negated os or cpu entry ({shape!r}), a shape this check does not read")
    sys.exit(0 if system in lists[0] and arch in lists[1] else 1)


def published(package, version):
    """`npm view --json <pkg> time`, after the verdict read it: the version's publish time, for the pass line."""
    times = read_json(f"npm view --json {package} time")
    when = times.get(version) if isinstance(times, dict) else None
    if not isinstance(when, str):
        refuse(f"npm view --json {package} time lists no publish time for {version}")
    print(when)


MODES = {
    "requested": requested,
    "window": window,
    "optional-dependencies": optional_dependencies,
    "platform": platform,
    "published": published,
}
MODES[mode](*args)
PY

#
# @description Run the parser in one mode on stdin.
# @arg $1 string The mode; the rest are its arguments.
#
function parse() {
    python3 -I -c "${parser}" "$@"
}

#
# @description Print one `npm view --json` answer from the config's npm; exit 2 naming the command when it fails.
# @arg $@ string npm view's arguments after --json.
#
function npm_view() {
    local answer
    answer=$(mise -C "${config_dir}" exec node -- npm view --json "$@") ||
        cannot_tell "mise -C ${config_dir} exec node -- npm view --json $* failed"
    printf '%s' "${answer}"
}

#
# @description Judge one package version against the window through npm_release_age_verdict: a refusal is printed
#   and counted, a pass is recorded with its publish time for the tool's pass line.
# @arg $1 string The package name.
# @arg $2 string The version.
# @arg $3 string `npm view --json <package> time`.
# @set refusals integer Incremented when the package is refused.
# @set checked string The packages that passed so far, for the pass line.
#
function judge() {
    local package=$1 version=$2 times=$3 verdict when status=0
    verdict=$(npm_release_age_verdict "${version}" "${days}" ${now:+"${now}"} <<< "${times}") || status=$?
    case ${status} in
    0)
        when=$(parse published "${package}" "${version}" <<< "${times}") || exit 2
        checked="${checked:+${checked}, }${package}@${version} (published ${when})"
        ;;
    1)
        printf 'refuse: %s@%s: %s\n' "${package}" "${version}" "${verdict}"
        refusals=$((refusals + 1))
        ;;
    *) cannot_tell "${package}@${version}: ${verdict:-the release age cannot be told}" ;;
    esac
}

#
# @description Check one tool: the meta package, then every optional dependency built for this runner.
# @arg $1 string `npm:<name>` or `npm:<name>@<request>`.
# @set refused_total integer Incremented by the tool's refusals.
#
function check_tool() {
    local tool=$1 spec name request info version times optional deps dep dep_version shape status matched=0
    case ${tool} in
    npm:?*) ;;
    *) cannot_tell "${tool} is not an npm: tool" ;;
    esac
    spec=${tool#npm:}
    # A scope's leading @ is part of the name; a second @ separates the request.
    case ${spec#@} in
    *@*)
        name=${spec%@*}
        request=${spec##*@}
        ;;
    *)
        name=${spec}
        info=$(mise -C "${config_dir}" tool --json "${tool}") || cannot_tell "mise -C ${config_dir} tool --json ${tool} failed"
        request=$(parse requested "${tool}" <<< "${info}") || exit 2
        ;;
    esac
    version=$(mise -C "${config_dir}" latest "npm:${name}@${request}") ||
        cannot_tell "mise -C ${config_dir} latest npm:${name}@${request} failed"
    refusals=0
    checked=""
    times=$(npm_view "${name}" time) || exit 2
    judge "${name}" "${version}" "${times}"
    optional=$(npm_view "${name}@${version}" optionalDependencies) || exit 2
    deps=$(parse optional-dependencies "${name}@${version}" <<< "${optional}") || exit 2
    if [[ -z ${deps} ]]; then
        printf '%s@%s: no optional dependencies\n' "${name}" "${version}"
    else
        while read -r dep dep_version; do
            shape=$(npm_view "${dep}@${dep_version}" os cpu) || exit 2
            status=0
            parse platform "${platform}" "${arch}" "${dep}@${dep_version}" <<< "${shape}" || status=$?
            case ${status} in
            0) ;;
            1) continue ;;
            *) exit 2 ;;
            esac
            matched=1
            times=$(npm_view "${dep}" time) || exit 2
            judge "${dep}" "${dep_version}" "${times}"
        done <<< "${deps}"
        if ((matched == 0)); then
            printf 'refuse: %s@%s: none of its optional dependencies is built for %s/%s\n' "${name}" "${version}" "${platform}" "${arch}"
            refusals=$((refusals + 1))
        fi
    fi
    if ((refusals == 0)); then
        printf 'pass: %s: %s, at least %s and 60 s old\n' "${tool}" "${checked}" "${window}"
    fi
    refused_total=$((refused_total + refusals))
}

window=$(mise -C "${config_dir}" settings get minimum_release_age) ||
    cannot_tell "mise -C ${config_dir} settings get minimum_release_age failed"
days=$(parse window <<< "${window}") || exit 2
platform=$(mise -C "${config_dir}" exec node -- node -p process.platform) ||
    cannot_tell "mise -C ${config_dir} exec node -- node -p process.platform failed"
arch=$(mise -C "${config_dir}" exec node -- node -p process.arch) ||
    cannot_tell "mise -C ${config_dir} exec node -- node -p process.arch failed"

refusals=0
checked=""
refused_total=0
for tool in "$@"; do
    check_tool "${tool}"
done
((refused_total == 0)) || exit 1
